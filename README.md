# News Digest Skill (中文版)

AI/科技新闻深度解读工作流，适用于 Claude Code。所有依赖已内置，安装即用。

> English version: [news-digest-skill-en](https://github.com/RocStone/news-digest-skill-en)

## 功能

- **/myhn** — 从 Hacker News 筛选 20 条高价值新闻，7 维度深度解读
- **/news** — 全网新闻（GitHub Trending、Product Hunt、36Kr 等），30 条精选深度拆解
- **/洞察** — 单篇文档/链接的深度分析，最大化认知增量

每条新闻的解读框架包含：核心事实/洞察、深度分析、社区讨论、批判性反思、一句话本质、对我的启发等维度。

## 安装

```bash
git clone https://github.com/RocStone/news-digest-skill-cn.git ~/.claude/skills/news-digest-skill-cn
```

无需额外安装依赖。以下工具已内置在 `deps/` 目录中：

- [hn](https://clawhub.ai/gchapim/hackernews) (MIT-0) — Hacker News CLI
- [news-aggregator-skill](https://github.com/cclank/news-aggregator-skill) (MIT) — 全网新闻聚合
- [last30days](https://github.com/mvanhorn/last30days-skill) (MIT) — Reddit + X + Web 研究

### 运行环境要求

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)（HN 工具需要）

## 配置

安装后编辑 prompts 目录下三个文件中的「我的背景」部分：

```
~/.claude/skills/news-digest-skill-cn/prompts/hn-digest.md
~/.claude/skills/news-digest-skill-cn/prompts/global-news-digest.md
~/.claude/skills/news-digest-skill-cn/prompts/deep-dive.md
```

将占位符替换为你自己的信息（职业身份、关注方向、投资偏好等），AI 会据此生成个性化解读。

此外，`global-news-digest.md` 中的「对我的具体价值 (Actionable Value)」部分也需要自定义。默认提供了示例维度（研究方向、开源项目切入点、面试考点、投资标的等），请替换为你自己认为最重要的价值转化方向。这决定了 AI 在解读每条新闻时会从哪些角度为你提炼可执行的行动建议。

## 使用

```
/myhn          # 获取今日 HN 新闻深度解读
/news          # 获取全网新闻深度解读
/洞察 ./path/to/article.md   # 深度分析指定文档
/洞察 https://example.com    # 深度分析指定链接
```

## 输出示例

查看 [daily-news-digest](https://github.com/RocStone/daily-news-digest) 仓库获取每日生成的新闻解读样例。

## 致谢

本项目基于以下开源 skill 构建：

| 工具 | 作者 | License | 原始仓库 |
|------|------|---------|----------|
| hn | gchapim | MIT-0 | [clawhub.ai/gchapim/hackernews](https://clawhub.ai/gchapim/hackernews) |
| news-aggregator-skill | cclank | MIT | [github.com/cclank/news-aggregator-skill](https://github.com/cclank/news-aggregator-skill) |
| last30days | mvanhorn | MIT | [github.com/mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) |

## License

MIT
