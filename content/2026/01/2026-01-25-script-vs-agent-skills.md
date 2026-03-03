---
title: "Skills \u4e0d\u5c31\u662f\u811a\u672c\u5957\u4e2a\u58f3\u5417\uff1f\u6211\u5341\u51e0\u5e74\u524d\u5c31\u73a9 AutoIt \u4e86"
date: 2026-01-25
original_url: https://baoyu.io/blog/2026/01/25/script-vs-agent-skills
---

[See all posts](/translations)

Published on 2026-01-25

# Skills 不就是脚本套个壳吗？我十几年前就玩 AutoIt 了

作者：

宝玉

![Skills 不就是脚本套个壳吗？我十几年前就玩 AutoIt 了](https://s.baoyu.io/imgs/2026-01-25/script-vs-agent-skills/cover.png)

![](https://s.baoyu.io/imgs/2026-01-25/script-vs-agent-skills/cover.png)

程序员看到 Agent Skills，很多人第一反应是：“这不就是脚本换个壳吗？我用 Python 半小时就能写出来，还更稳定。”

比如安替老师：

> 我怎么觉得现在 skills 炫耀的功能，基本上我很快就可以用 Claude Code 手搓一个 Python 程序完成了，而且更稳定、更快、随时可调整订制。当然 Skills 把和 AI 的互动简化了，不过我觉得它增加的不确定性、控制力弱、延迟等问题，超越了它带来的好处。

还有更直接的：

> 就他妈一堆自动化的 bat shell 脚本，JB 吹上天。吐了。我十几年前就玩 AutoIt 了。

拿部分场景来比功能，确实不算错。但把 Skills 等同于脚本，就像把智能手机等同于能打电话的计算器，**功能有重叠，本质变了**。

![脚本 vs Skills 本质对比](https://s.baoyu.io/imgs/2026-01-25/script-vs-agent-skills/01-comparison-script-vs-skill.png)

## 脚本和 Skills 到底差在哪？

先说定义。

**脚本**：你写一段代码，告诉电脑先做 A，再做 B，最后做 C。固定动作，按步执行，遇错停下等你。

**Agent Skills**：给 AI Agent 的技能包。核心是一个 `SKILL.md` 说明文档，写清楚什么情况该用、怎么做更专业、哪些步骤要调代码。还可能引用其他文档或脚本。Agent 读懂之后，自己决定该不该用、怎么用。

**三个关键差异：**

**1. 脚本对 Skills 不是必须的。** 比如我做了一个“宝玉写作风格”的 Skill，只有一个 `SKILL.md`，写清楚风格要求，没有任何脚本。这活你让脚本做，还真做不了。

**2. Skill 里的脚本是 Agent 在调度。** 传统脚本：你写代码 → 你调用 → 遇到问题停下来等你。Agent + Skills：你说目标 → Agent 理解 → Agent 调用 → 遇到问题 Agent 自己解决。

拿处理 PDF 举例。缺 `pdfplumber` 库？脚本报错退出，Agent 自己装一个。PDF 格式有问题？脚本报错退出，Agent 换个解析方式。代码有 bug？脚本报错退出，Agent 读报错信息，改代码重跑。

相当于你电脑上配了一个 **AI 程序员**，能看懂报错、装依赖、改代码、调试。

![遇到错误：脚本 vs Agent](https://s.baoyu.io/imgs/2026-01-25/script-vs-agent-skills/02-flowchart-agent-self-healing.png)

**3. Skills 用自然语言编排工作流。** 脚本用 `if-else`、`for` 循环、`try-catch` 编排，你得把思路翻译成代码。Skills 用自然语言：什么情况下用、注意什么、出错怎么办。

这降低了门槛。以前只有程序员能写自动化，现在产品经理、运营、设计师，需求说得清楚就能做。

也提高了灵活性。比如我写了个“文章配图”的 Skill，不用代码判断文章类型，只在 `SKILL.md` 里写：**配图服务于内容理解，技术内容优先流程图，观点内容优先概念图**。Agent 自己判断当前文章该用哪种。

![编排方式的变革：代码 vs 自然语言](https://s.baoyu.io/imgs/2026-01-25/script-vs-agent-skills/03-comparison-nl-vs-code.png)

## 确定性的事交给代码

Skills 和脚本不是二选一。**确定的事让代码做，不确定的让 Agent 做。**

我的写作工作流里有个格式化步骤：中文引号换全角、中英文之间加空格。规则明确，我写了个脚本。AI 润色完文章后自动调用，比让 AI 做更稳定，成本也更低。

怎么判断该用哪个？想想**银行柜台**和**项目经理**的区别。

**银行柜台**：每一步有标准动作，合规严格，输出必须可预测。这种场景用脚本，Agent 反而添乱。

**项目经理**：需求模糊，步骤随时调整，中间冒出各种意外。这才是 Agent 的舞台。

![什么时候用哪个？银行柜台 vs 项目经理](https://s.baoyu.io/imgs/2026-01-25/script-vs-agent-skills/04-scene-certainty-vs-uncertainty.png)

## 为什么 Skills 突然火了？

在 Agent Skills 之前，我就是脚本自动化爱好者，写了不少小工具。但有两个问题一直没解决。

**写脚本的成本不低。** 我是专业程序员，也没写太多自动化脚本，因为把想法变成代码太繁琐。现在借助 Agent，几句话就自动搞定了。非程序员更是直接受益，就好比《哈利波特》里**麻瓜突然获得了魔法**。以前自动化是少数“魔法师”的专利，现在人人都能做。

![从专利到普惠：自动化的民主化](https://s.baoyu.io/imgs/2026-01-25/script-vs-agent-skills/05-scene-automation-democracy.png)

**分享脚本的成本更高。** 我的脚本很少分享，因为基本只有自己能用。写兼容代码和文档的成本太高，不值得。

现在不一样了。我的 baoyu-skills 刚发布时很多在 Windows 下跑不顺，但网友运行时 Agent 会主动修复兼容问题。热心网友还把修改提成 PR，帮到了更多人。

**Skills 的进化也快。** 一方面背后的 Agent 模型在不断变强。另一方面，Skills 的反馈循环短得多。传统软件要走产品经理 → 开发 → 测试的长链条，用户拿到可能不是想要的。Skills 是每个人量身定制，一边用一边改，Agent 知道全部上下文，遇到问题马上定位，根据反馈实时调整。

![Skills 进化飞轮](https://s.baoyu.io/imgs/2026-01-25/script-vs-agent-skills/06-framework-skills-evolution.png)

## “苦涩的教训”

强化学习之父 Rich Sutton 在 2019 年写过一篇著名文章《The Bitter Lesson》。核心观点：**70 年人工智能研究证明，通用方法最终总是赢。**

他回顾了国际象棋、围棋、语音识别、计算机视觉的历史，发现一个规律：研究者试图把专家知识硬编码进系统，短期有效，长期却停滞甚至阻碍进步。真正的突破来自**让机器自己搜索和学习**。

脚本是“把你的思考过程固化成代码”，Skills 是“告诉 AI 目标和约束，让它自己想办法”。前者是 **hard-coded**，后者是 **learned**。

![苦涩的教训：Hard-coded vs Learned](https://s.baoyu.io/imgs/2026-01-25/script-vs-agent-skills/07-comparison-hardcoded-vs-learned.png)

“我十几年前就玩 AutoIt 了”，没错。但今天变了：**AI 能理解自然语言、能动态规划、能从错误中学习。**

## 别忘了安全

Skills 把脚本加说明书打包分发，本质上是**新的依赖生态，新的攻击面**。恶意 Skills 可能引入漏洞、诱导外联，甚至数据外泄。只装可信来源的 Skills，装之前审计文件和脚本内容。

## 真正的分野

“我用 Python 半小时就能写出来”，没错。但写完只有你能用，你愿意花时间写文档、做兼容、处理边界情况吗？大概率不愿意。

“十几年前就玩 AutoIt 了”，也没错。但十几年过去了，AutoIt 还是那批人在用。

Skills 的意义不在于能做什么新事情，而在于**谁能做这些事情**。以前自动化是程序员的特权，现在是每个人的工具。以前写脚本要考虑十几种边界情况，现在 Agent 帮你兜底。以前分享脚本是技术输出，现在分享 Skills 是知识传递。

程序员看 Skills 觉得没技术含量，就像厨师看预制菜觉得没灵魂。但餐饮业的变革不是让每个人都变成厨师，而是让不会做饭的人也能吃上还不错的菜。

![真正的分野](https://s.baoyu.io/imgs/2026-01-25/script-vs-agent-skills/08-infographic-real-divide.png)

Sutton 那篇文章叫“苦涩的教训”。苦涩在哪？研究者花几十年精心设计的专家系统，被暴力计算加通用学习碾压了。那些精巧的领域知识、引以为傲的工程技巧，在算力和数据面前不值一提。

你花十年练就的脚本技巧，可能正在被一种你不太看得上的新范式取代。承认这一点确实苦涩，但早点看清楚，总比后知后觉强。

---

[See all posts](/translations)