# News Digest Skill

AI/科技新闻深度解读工作流，适用于 Claude Code。

## 功能

- **/myhn** — 从 Hacker News 筛选 20 条高价值新闻，7 维度深度解读
- **/news** — 全网新闻（GitHub Trending、Product Hunt、36Kr 等），30 条精选深度拆解
- **/洞察** — 单篇文档/链接的深度分析，最大化认知增量

每条新闻的解读框架包含：核心事实/洞察、深度分析、社区讨论、批判性反思、一句话本质、对我的启发等维度。

## 安装

```bash
npx skills add RocStone/news-digest-skill
```

### 依赖 Skill

安装本 skill 前，请先安装：

```bash
npx skills add hn
npx skills add news-aggregator-skill
```

## 配置

安装后编辑 prompts 目录下三个文件中的「我的背景」部分：

```
~/.agents/skills/news-digest-skill/prompts/hn-digest.md
~/.agents/skills/news-digest-skill/prompts/global-news-digest.md
~/.agents/skills/news-digest-skill/prompts/deep-dive.md
```

将占位符替换为你自己的信息（职业身份、关注方向、投资偏好等），AI 会据此生成个性化解读。

## 使用

```
/myhn          # 获取今日 HN 新闻深度解读
/news          # 获取全网新闻深度解读
/洞察 ./path/to/article.md   # 深度分析指定文档
/洞察 https://example.com    # 深度分析指定链接
```

## 输出示例

查看 [daily-news-digest](https://github.com/RocStone/daily-news-digest) 仓库获取每日生成的新闻解读样例。

## License

MIT
