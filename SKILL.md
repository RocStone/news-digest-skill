---
name: news-digest-skill
description: "AI/科技新闻深度解读工作流。获取 HN + 全网新闻，7 维度分析框架，支持单篇深度洞察。"
---

# News Digest Skill

AI/科技新闻深度解读工作流，包含三个子命令。

## 依赖

需要安装以下 skill：
- `hn` — 获取 Hacker News 数据
- `news-aggregator-skill` — 获取全网新闻数据源

## 子命令

### /myhn
获取 Hacker News 前 100 条热门新闻，筛选 20 条进行 7 维度深度解读。

读取 `{baseDir}/prompts/hn-digest.md` 执行。

### /news
从 HN 以外的全网信息源获取新闻，精选 30 条进行硬核深度拆解。使用 news-aggregator-skill 覆盖 GitHub Trending、Product Hunt、36Kr、腾讯新闻、华尔街见闻、V2EX、微博等。

读取 `{baseDir}/prompts/global-news-digest.md` 执行。

### /洞察 <路径或链接>
对单篇文档或链接进行深度分析，最大化认知增量。包含核心洞察、定位对比、直觉建立、非显而易见的东西等维度。

读取 `{baseDir}/prompts/deep-dive.md` 执行。

## 首次使用

安装后，请编辑 `prompts/` 目录下三个文件中的「我的背景」部分，替换为你自己的信息。AI 会根据这些生成与你个人相关的解读。

## 深度跟进

看完 digest 后，如果对某条新闻特别感兴趣，可以让 AI 打开原文链接继续深入分析，或使用 `/洞察` 命令。
