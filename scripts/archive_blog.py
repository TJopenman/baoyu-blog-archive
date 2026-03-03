import re
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from slugify import slugify

BLOG_URL = "https://baoyu.io/blog"
ARCHIVE_DIR = Path("content")
INDEX_FILE = Path("archived.json")


def load_archived():
    if not INDEX_FILE.exists():
        return set()
    try:
        return set(json.loads(INDEX_FILE.read_text(encoding="utf-8")).get("urls", []))
    except:
        return set()


def save_archived(urls):
    INDEX_FILE.write_text(
        json.dumps({"urls": sorted(urls), "last_run": datetime.utcnow().isoformat()}, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def get_slug(url: str) -> str:
    path = url.rstrip("/").split("/")[-1]
    path = re.sub(r'^\d{4}-\d{2}-\d{2}[-_]?', '', path)
    return slugify(path, separator="-", lowercase=False, regex_pattern=r'[^-a-zA-Z0-9\u4e00-\u9fff]+')


def parse_date(text: str) -> str:
    text = text.strip().replace("年", "-").replace("月", "-").replace("日", "")
    for fmt in ("%Y-%m-%d", "%B %d, %Y", "%Y年%m月%d日"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except:
            continue
    return datetime.utcnow().strftime("%Y-%m-%d")


def extract_article(url: str):
    r = requests.get(url, timeout=15, headers={"User-Agent": "BlogArchiver/1.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # 标题
    title = (soup.find("h1") or soup.find("title")).get_text(strip=True)

    # 日期
    date_str = ""
    for sel in ["time", 'meta[property="article:published_time"]', ".date", ".meta", ".published"]:
        tag = soup.select_one(sel)
        if tag:
            date_str = tag.get("datetime") or tag.get_text(strip=True)
            break
    date = parse_date(date_str)

    # 正文（适配 baoyu.io 常见结构）
    article = (
        soup.select_one("article")
        or soup.select_one("div.prose")
        or soup.select_one("main")
        or soup.select_one(".post-content")
        or soup.select_one(".markdown")
    )
    if article:
        for bad in article.find_all(["script", "style", "nav", "footer", "aside", "header"]):
            bad.decompose()
        content = article.get_text(separator="\n\n", strip=True)
    else:
        content = "（正文提取失败，请检查文章结构）"

    return title, date, content


def main():
    archived = load_archived()
    resp = requests.get(BLOG_URL, headers={"User-Agent": "BlogArchiver/1.0"})
    soup = BeautifulSoup(resp.text, "html.parser")

    new_count = 0
    for a in soup.select("h2 a, article a, .post-title a"):
        url = urljoin(BLOG_URL, a.get("href", ""))
        if not url.startswith(BLOG_URL + "/") or url in archived:
            continue

        print(f"正在抓取新文章: {url}")
        try:
            title, date, content = extract_article(url)
            if not title or not content.strip():
                print("  → 跳过（标题或内容为空）")
                continue

            year, month = date[:4], date[5:7]
            slug = get_slug(url)
            filename = f"{date}-{slug}.md"
            filepath = ARCHIVE_DIR / year / month / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # 使用 json.dumps 安全处理标题（解决 f-string 问题）
            front_matter = f"""---
title: {json.dumps(title)}
date: {date}
original_url: {url}
---

"""

            filepath.write_text(front_matter + content, encoding="utf-8")
            archived.add(url)
            new_count += 1
            print(f"  ✓ 保存成功 → {filepath}")

        except Exception as e:
            print(f"  ✗ 处理失败: {e}")

    if new_count > 0:
        save_archived(archived)
        print(f"\n本次成功新增 {new_count} 篇文章！")
    else:
        print("\n暂无新文章")


if __name__ == "__main__":
    main()
