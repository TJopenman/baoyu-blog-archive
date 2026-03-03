# scripts/archive_blog.py
import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from slugify import slugify  # 需要 pip install python-slugify


BLOG_URL = "https://baoyu.io/blog"
ARCHIVE_DIR = Path("content")
INDEX_FILE = Path("archived.json")


def load_archived() -> set:
    """加载已归档的文章链接集合（使用规范化链接作为key）"""
    if not INDEX_FILE.exists():
        return set()
    with INDEX_FILE.open(encoding="utf-8") as f:
        data = json.load(f)
        return set(data.get("urls", []))


def save_archived(urls: set):
    INDEX_FILE.write_text(
        json.dumps({"urls": sorted(urls), "last_run": datetime.utcnow().isoformat()}, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def get_article_slug(url: str) -> str:
    """从URL提取slug，并做安全处理"""
    path = url.rstrip("/").split("/")[-1]
    # 去掉可能的日期前缀（如 2026-02-25-xxx）
    path = re.sub(r'^\d{4}-\d{2}-\d{2}[-_]?', '', path)
    # slugify 处理中文 → 拼音 或 保留（这里保留原样但清理非法字符）
    return slugify(path, separator="-", lowercase=False, regex_pattern=r'[^-a-zA-Z0-9\u4e00-\u9fff]+')


def parse_date(date_str: str) -> str:
    """尝试解析常见日期格式 → 返回 YYYY-MM-DD"""
    date_str = date_str.strip().replace("年", "-").replace("月", "-").replace("日", "")
    for fmt in (
        "%B %d, %Y",          # March 2, 2026
        "%Y-%m-%d",           # 2026-03-02
        "%Y年%m月%d日",       # 2026年03月02日
    ):
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    # 兜底使用今天
    print(f"日期解析失败: {date_str} → 使用今日")
    return datetime.utcnow().strftime("%Y-%m-%d")


def extract_article_content(url: str) -> tuple[str, str, str]:
    """抓取单篇文章，返回 (标题, 日期YYYY-MM-DD, markdown正文)"""
    resp = requests.get(url, timeout=15, headers={"User-Agent": "BlogArchiver/1.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # 标题（优先级：h1 > title > meta）
    title_tag = soup.find("h1") or soup.find("title")
    title = (title_tag.get_text() or "").strip()
    if not title and (meta := soup.find("meta", property="og:title")):
        title = meta.get("content", "").strip()

    # 日期（常见位置）
    date = ""
    candidates = [
        soup.find("time", {"datetime": True}),
        soup.find("meta", property="article:published_time"),
        soup.find(string=re.compile(r"(年|月|日|\d{4})")),
        soup.find("p", class_=re.compile("date|meta|pub|time", re.I)),
    ]
    for c in candidates:
        if c:
            text = c.get("datetime") or c.get_text(strip=True)
            if text:
                date = parse_date(text)
                if date:
                    break

    if not date:
        date = datetime.utcnow().strftime("%Y-%m-%d")

    # 正文提取（最重要部分）
    content = ""
    # 尝试常见容器
    article = (
        soup.find("article")
        or soup.find("div", class_=re.compile(r"prose|content|post-body|entry-content|markdown|blog-post", re.I))
        or soup.find("main")
        or soup.find("div", {"id": "content"})
    )

    if article:
        # 移除不需要的部分（常见广告/导航/评论）
        for bad in article.find_all(["script", "style", "iframe", "noscript", "footer", "nav", {"class": re.compile("comment|sidebar|aside|related|footer", re.I)}]):
            bad.decompose()

        content = article.get_text(separator="\n", strip=True)
        # 尝试保留更多结构（可选：转为markdown更友好）
        # 你也可以使用 markdownify 库：from markdownify import markdownify
        # content = markdownify(str(article), heading_style="ATX")

    if not content:
        content = "（正文提取失败，请手动检查文章页面结构）"

    return title, date, content


def main():
    print("开始抓取博客:", BLOG_URL)

    archived_urls = load_archived()
    new_articles = []

    resp = requests.get(BLOG_URL, timeout=15, headers={"User-Agent": "BlogArchiver/1.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # 找到所有文章链接（根据实际结构调整）
    # 常见模式：h2 > a, 或 .post-title a, 或 article a
    links = []
    for h2 in soup.find_all("h2"):
        a = h2.find("a", href=True)
        if a:
            href = a["href"]
            full_url = urljoin(BLOG_URL, href)
            if full_url.startswith(BLOG_URL + "/") and full_url not in archived_urls:
                links.append(full_url)

    if not links:
        # 备选：找所有 /blog/ 开头的链接
        for a in soup.find_all("a", href=re.compile(r"^/blog/[^/]+$")):
            full_url = urljoin(BLOG_URL, a["href"])
            if full_url not in archived_urls:
                links.append(full_url)

    print(f"发现 {len(links)} 篇潜在新文章")

    for url in sorted(links):
        print("处理:", url)
        try:
            title, date, content = extract_article_content(url)
            if not title or not content.strip():
                print("  → 跳过（标题或内容为空）")
                continue

            year, month, _ = date.split("-")
            slug = get_article_slug(url)
            filename = f"{year}-{month}-{date}-{slug}.md"
            filepath = ARCHIVE_DIR / year / month / filename

            # 创建目录
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # YAML front matter
            front_matter = f"""---
title: "{title.replace('"', '\\"')}"
date: {date}
original_url: {url}
---

"""

            filepath.write_text(front_matter + content, encoding="utf-8")
            print(f"  → 保存成功: {filepath}")

            archived_urls.add(url)
            new_articles.append(filepath.name)

        except Exception as e:
            print(f"  → 处理失败: {e}")

    if new_articles:
        save_archived(archived_urls)
        print(f"本次新增 {len(new_articles)} 篇文章")
        # 可选：在这里 git add/commit/push（但建议交给 workflow 处理）
    else:
        print("没有新文章")


if __name__ == "__main__":
    main()
