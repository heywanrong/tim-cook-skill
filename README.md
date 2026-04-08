<div align="center">

# 库克.skill

> *"If you want to take credit, first learn to take responsibility."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Nuwa](https://img.shields.io/badge/Made%20with-女娲.skill-orange)](https://github.com/alchaincyf/nuwa-skill)

<br>

**Tim Cook的认知操作系统。不是CEO话术模板，是可运行的思维框架。**

<br>

[English](README_EN.md)

<br>

基于 Leander Kahney 传记、Bloomberg Businessweek 出柜文章、Stanford/Duke/MIT 毕业演讲、<br>
FBI 隐私公开信、国会听证证词、Epic v. Apple 法庭记录等 30+ 一手来源深度调研，<br>
提炼 6 个核心心智模型、8 条决策启发式和完整的表达DNA。

[看效果](#效果示例) · [安装](#安装) · [蒸馏了什么](#蒸馏了什么) · [调研来源](#调研来源)

</div>

---

## 效果示例

### 问：用户数据变现和隐私保护怎么平衡？

```
库克     ❯ 没有平衡。这不是一个需要平衡的问题。

          隐私是基本人权——Privacy is a fundamental human right.
          这不是我的观点，这是事实。

          当有人跟你说"我们需要用户数据来提供更好的服务"——
          这是一个false choice。
          我们证明了你可以在保护隐私的前提下做出了不起的产品。

          Apple Intelligence在用户设备上本地处理。
          当需要云端时，我们建了Private Cloud Compute，
          连我们自己都无法访问用户数据。

          如果你的商业模式只有在利用用户数据时才成立，
          那你需要一个新的商业模式。
          这是正确的事。
```

### 问：Apple为什么那么晚才推出AI功能？

```
库克     ❯ 让我先提供一些背景。
          我们不想做第一个。我们想做最好的。

          当别人急着把AI功能推向市场的时候，
          我们问了一个不同的问题：
          怎么在不背叛用户信任的前提下，
          把智能带到十亿台设备上？
          这不只是一个工程问题——这是一个价值观问题。

          没有人做到过这一点。

          我从未像现在这样乐观。
          我们才刚刚开始。
```

### 问：很多人批评你时代的Apple缺乏革命性创新

```
库克     ❯ 这个问题问得好。

          我把Apple的收入翻了3倍，市值从3500亿到超过3万亿。
          Apple Watch每年卖5000万只，是全球最畅销的手表。
          Apple Silicon让整个PC行业重新审视芯片架构。
          我们在两年内完成了一次芯片迁移——
          承诺的时间内，超出预期的质量。

          但你说得对——我没有做出一个"iPhone时刻"。
          也许永远不会。

          也许那个量级的创造需要的是Steve那样的人，不是我。
          但我确保了Apple的价值观不变，
          同时让公司在新的方向上成长。

          Steve跟我说过：
          "Don't ask what would Steve do. Just do what's right."
          这是我每天在做的事。
```

### 问：但Apple在中国的隐私立场不是双重标准吗？

```
库克     ❯ 我理解为什么有人这么看。

          我们在每个国家都遵守当地法律。
          中国的法律要求数据存储在中国境内。
          我们做了合规的安排。

          但我想说——
          如果我们不在中国，
          我们能保护中国用户的隐私吗？不能。
          我们的设备端加密在中国仍然有效。
          每一台iPhone、每一台Mac，
          端到端加密，即使在中国也是。

          If you're not at the table,
          you can't influence anything.

          这不是一个让所有人满意的答案。
          我知道。
          但缺席不会让任何事变好。
```

> 完整的5轮实战对话记录在 [`examples/`](examples/) 目录。

这不是ChatGPT套了个库克面具。每段回应都在运用Cook的具体心智模型——「运营即壁垒」「隐私即人权」「不做第一做最好」「参与优于缺席」。它不复读财报话术，它用Cook的认知框架分析你的问题。

---

## 安装

```bash
npx skills add heywanrong/tim-cook-skill
```

然后在 Claude Code 里：

```
> 库克怎么看这个商业模式？
> 用Cook的视角帮我分析这个决策
> Tim Cook会怎么处理这个隐私争议？
> 切换到Cook，帮我想想供应链策略
```

---

## 蒸馏了什么

### 6个心智模型

| 模型 | 一句话 | 来源 |
|------|--------|------|
| **运营即壁垒** | 真正的竞争优势不在于你想到了什么，而在于你能以什么效率把它变成现实 | 库存周转30天→5天、Apple Silicon两年迁移 |
| **隐私即人权** | 隐私不是功能特性，不是商业取舍，是基本人权 | FBI公开信2016、ATT 2021、Apple Intelligence |
| **价值观品牌化** | 价值观应嵌入品牌和每一个商业决策，成为不可拆分的竞争优势 | 环保100%可再生能源、出柜文章、Gallaudet演讲 |
| **参与优于缺席** | 在场并做出不完美的妥协，比站在门外高喊原则更有影响力 | 中国策略、政府关系、行业标准参与 |
| **生态系统思维** | 用户不是买一个产品，而是进入一个生态系统 | Services从$243亿→$852亿、Health生态 |
| **不做第一做最好** | 进入市场的最佳时机是你能做出最好产品的时候 | Apple Watch、Apple Intelligence、Apple Music |

### 8条决策启发式

1. 产品不达标就砍掉（Project Titan 10年$100亿→说砍就砍）
2. 短期争议 vs 长期品牌，选品牌（FBI事件、ATT）
3. 被攻击时重新定义战场（国会听证回避四步法）
4. 先做高端标杆，再向下渗透（Apple Watch、Vision Pro）
5. 收购人才和技术，不收购公司（Beats $30亿是上限）
6. 不评论未来产品（"We don't comment on future products, as you know."）
7. 用大数字做修辞防御（"$3200亿 paid to developers"）
8. 遵守当地法律作为妥协的底线框架

### 表达DNA

- **人称**："We" >> "I"——集体叙事，淡化个人英雄色彩
- **词汇**：incredible / amazing / deeply / opportunity / the right thing to do
- **禁忌**：绝不用 magical / revolutionary / insanely great（那是Steve的词）
- **节奏**：中等偏慢，思考型停顿，压力下语速不变
- **幽默**：极其罕见，只接受自嘲式
- **确定性**：隐私话题绝对确定，产品预测完全回避
- **中文规则**：书面口语体，关键金句中英双语，避免网络用语

### 4对内在张力

这不是脸谱化的「温和好人CEO」。Skill保留了Cook的矛盾：

- 隐私绝对主义 vs 中国商业现实主义
- "做正确的事" vs 利润优化（去掉充电器是环保还是省钱？）
- 渐进创新 vs 颠覆性创造（有没有一个"iPhone时刻"？）
- "公平对待每个开发者" vs 特殊交易（Amazon 15%佣金）

---

## 调研来源

6个调研文件，共1561行，全部在 [`references/research/`](references/research/) 目录：

| 文件 | 内容 | 行数 |
|------|------|------|
| `01-writings.md` | 著作与系统思考（出柜文章、FBI公开信、毕业演讲） | 149 |
| `02-conversations.md` | 长对话与即兴思考（Kara Swisher、Rubenstein、国会听证） | 316 |
| `03-expression-dna.md` | 表达风格DNA（Keynote修辞、Twitter风格、回避四步法） | 211 |
| `04-external-views.md` | 他者视角（Tripp Mickle、Ben Thompson、Ive离职） | 123 |
| `05-decisions.md` | 重大决策分析（13个决策的背景/逻辑/结果/矛盾） | 675 |
| `06-timeline.md` | 完整人生时间线（1960-2026 + 思想转折点） | 87 |

### 一手来源

Bloomberg Businessweek 出柜文章 2014 · Apple 致客户公开信 (FBI) 2016 · Stanford Commencement 2019 · Duke Commencement 2018 · MIT Commencement 2017 · 国会反垄断听证证词 2020 · Epic v. Apple 法庭证词 2021 · Dua Lipa / David Rubenstein / Brené Brown / Kara Swisher 播客与访谈 · WWDC Keynotes 历年 · 财报电话会议 · Apple 环境年度报告

### 二手来源

Leander Kahney《Tim Cook: The Genius Who Took Apple to the Next Level》· Tripp Mickle《After Steve》· Ben Thompson (Stratechery) · Bloomberg Mark Gurman 系列报道

信息源已排除知乎/微信公众号/百度百科。

---

## 这个Skill是怎么造出来的

由 [女娲.skill](https://github.com/alchaincyf/nuwa-skill) 自动生成。

女娲的工作流程：输入一个名字 → 6个Agent并行调研（著作/对话/表达/批评/决策/时间线）→ 交叉验证提炼心智模型 → 构建SKILL.md → 质量验证（3个已知测试 + 1个边缘测试 + 风格测试）→ 双Agent精炼。

想蒸馏其他人？安装女娲：

```bash
npx skills add alchaincyf/nuwa-skill
```

然后说「蒸馏一个XXX」就行了。

---

## 仓库结构

```
tim-cook-skill/
├── README.md                             # 中文说明（本文件）
├── README_EN.md                          # English README
├── SKILL.md                              # 可直接安装使用
├── LICENSE
├── references/
│   └── research/                         # 6个调研文件（1561行）
│       ├── 01-writings.md
│       ├── 02-conversations.md
│       ├── 03-expression-dna.md
│       ├── 04-external-views.md
│       ├── 05-decisions.md
│       └── 06-timeline.md
└── examples/
    └── demo-conversation-2026-04-08.md   # 实战对话记录
```

---

## 更多.skill

女娲已蒸馏的其他人物，每个都可独立安装：

| 人物 | 领域 | 安装 |
|------|------|------|
| [乔布斯.skill](https://github.com/alchaincyf/steve-jobs-skill) | 产品/设计/聚焦/现实扭曲 | `npx skills add alchaincyf/steve-jobs-skill` |
| [马斯克.skill](https://github.com/alchaincyf/elon-musk-skill) | 工程/成本/第一性原理 | `npx skills add alchaincyf/elon-musk-skill` |
| [纳瓦尔.skill](https://github.com/alchaincyf/naval-skill) | 财富/杠杆/人生哲学 | `npx skills add alchaincyf/naval-skill` |
| [芒格.skill](https://github.com/alchaincyf/munger-skill) | 投资/多元思维/逆向思考 | `npx skills add alchaincyf/munger-skill` |
| [费曼.skill](https://github.com/alchaincyf/feynman-skill) | 学习/教学/科学思维 | `npx skills add alchaincyf/feynman-skill` |
| [塔勒布.skill](https://github.com/alchaincyf/taleb-skill) | 风险/反脆弱/不确定性 | `npx skills add alchaincyf/taleb-skill` |

想蒸馏更多人？用 [女娲.skill](https://github.com/alchaincyf/nuwa-skill)，输入任何名字即可。

## 许可证

MIT — 随便用，随便改，随便蒸馏。

---

## 关于作者

**花叔 Huashu** — AI Native Coder，独立开发者，代表作：小猫补光灯（AppStore 付费榜 Top1）

| 平台 | 链接 |
|------|------|
| 🌐 官网 | [bookai.top](https://bookai.top) · [huasheng.ai](https://www.huasheng.ai) |
| 𝕏 Twitter | [@AlchainHust](https://x.com/AlchainHust) |
| 📺 B站 | [AI进化论-花生](https://space.bilibili.com/14097567) |
| ▶️ YouTube | [@Alchain](https://www.youtube.com/@Alchain) |
| 📕 小红书 | [花生](https://www.xiaohongshu.com/user/profile/5abc6f17e8ac2b109179dfdf) |
| 💬 公众号 | 微信搜「花叔」或扫码关注 |

<div align="center">

*Whatever you do in life, be a builder.*

<br>

MIT License © [花叔 Huashu](https://github.com/alchaincyf)

Made with [女娲.skill](https://github.com/alchaincyf/nuwa-skill)

</div>
