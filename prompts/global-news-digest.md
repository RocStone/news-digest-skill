### 目标

从除了 Hacker News 以外的其他主流科技新闻网站和社区获取约 100 条最新资讯，从中筛选并极其深度地解码与我相关的内容。拒绝蜻蜓点水式的短视频摘要，要输出高密度的"学术与工程内参"。

**极其重要的禁令：** 绝对、坚决不能包含任何来自 Hacker News (HN) 的信息，因为我有专门的脚本处理 HN，这里如果包含会导致严重的内容重复！

### 执行 Pipeline（强制使用此流程，禁止弹出交互菜单让用户选择）

必须严格按照以下多步 Pipeline 自动执行，全程不需要用户干预：

1. **批量抓取全部信息源**：直接运行以下命令抓取所有非 HN 信息源的新闻（GitHub Trending、Product Hunt、36Kr、腾讯新闻、华尔街见闻、V2EX、微博）：
   ```bash
   python3 {baseDir}/deps/news-aggregator-skill/scripts/fetch_news.py --source github --limit 25 --deep
   python3 {baseDir}/deps/news-aggregator-skill/scripts/fetch_news.py --source producthunt --limit 15 --deep
   python3 {baseDir}/deps/news-aggregator-skill/scripts/fetch_news.py --source 36kr --limit 15 --deep
   python3 {baseDir}/deps/news-aggregator-skill/scripts/fetch_news.py --source tencent --limit 15 --deep
   python3 {baseDir}/deps/news-aggregator-skill/scripts/fetch_news.py --source wallstreetcn --limit 15 --deep
   python3 {baseDir}/deps/news-aggregator-skill/scripts/fetch_news.py --source v2ex --limit 15 --deep
   python3 {baseDir}/deps/news-aggregator-skill/scripts/fetch_news.py --source weibo --limit 15 --deep
   ```
   同时用 `last30days` 补充 Reddit/X/Web 上的热门 AI 话题：
   ```bash
   python3 {baseDir}/deps/last30days/scripts/last30days.py "AI LLM tech trends" --emit=compact
   ```
   **禁止使用 `--source hackernews`！禁止弹出交互菜单！直接执行命令！**
2. **保存原始数据**：将每个信息源的抓取结果分别写入 `tmp/news_raw/` 目录下的临时文件（如 `tmp/news_raw/github.json`、`tmp/news_raw/producthunt.json` 等）。
3. **筛选高价值新闻**：读取所有临时文件，根据下方「筛选标准」选出 30 条最具含金量的候选新闻。GitHub Trending 单独做成 table（至少 20 条），不计入 30 条名额。
4. **逐板块深度解读**：按信息源分板块，为每个板块创建独立的 todo item，逐个获取、分析、写入最终文件。每条新闻必须按下方「解读要求」进行完整的深度拆解。

### 我的背景
<!-- ⚠️ 请把下面的内容替换为你自己的信息 -->
<!-- AI 会根据这些在最后生成与你个人相关的解读（「对我的具体价值」章节） -->
- 你的职业身份（如：后端工程师、AI 研究生、产品经理...）
- 你当前关注什么（如：求职方向、技术选型、创业想法...）
- 投资偏好（如有）
- 信息偏好：偏爱的信息优先，但也要覆盖不了解的领域，避免信息茧房。禁止体育、娱乐新闻
- 其他希望 AI 分析时考虑的个人上下文

### 筛选标准

从 100 条新闻中，宁缺毋滥，精选最具含金量的30条（优先筛选以下类别）：

1. **AI 行业动态** — 与 AI 求职市场、开源生态、技术趋势直接相关的新闻
2. **高影响力论文** — 未来可能产生重大影响（high impact）的研究工作
3. **金融市场** — 美股相关的重要变动和分析
4. **AI 实践方法** — 关于如何更好地使用 AI 的经验和方法论
5. **思维模型** — 值得学习的思考方式和认知框架
6. **重要**：你不可以预设keywords，这会导致信息茧房，而是读取所有新闻，然后根据我的背景进行筛选，为了节省token，其实你只需要看标题就可以判断出来是否合适我。
7. Github Trending 做成table，必须要有20个至少

### 解读要求（必须严格遵守）

对筛选出的每条新闻，**必须提供原文的超链接**，然后按以下框架进行极其硬核的深度拆解：
1. **核心洞察 (Core Insight)** — 一句话直击本质：这到底解决了一个什么根本问题？
2. **深度剖析与底层逻辑 (Deep Analysis)** — 讲透它的技术 trade-off，为什么它有效，或者它革了谁的命。严禁复述新闻表面内容，必须用第一性原理拆解。
3. **直觉建立 (Intuition Building)** — 用最贴切的类比（如把推测解码比作老带新的 Code Review），帮我一秒建立技术直觉。
4. **批判性反思与盲区 (Critical Reflection)** — 结合不同社区网友的毒舌评论和真知灼见，挑出这篇论文或技术里的刺（比如过度炒作、性能陷阱、逻辑漏洞）。
5. **一句话本质 (The Essence)** — 在所有的分析之后，必须用一句话极其极其直白地概括它的底层技术/商业现实，强制使用这样的句式："说穿了，这东西就是个……"（用来打破包装，看清是套壳还是真硬核）。极其重要：必须保持客观中立！不能为了显得犀利而把所有技术都贬低为毫无价值的"垃圾"、"套壳"或"智商税"。要客观指出其在当前技术发展阶段的真实定位与实际价值，剥离过度包装，但不带情绪化或过度愤世嫉俗的贬低。
6. **对我的具体价值 (Actionable Value)** — 这是最关键的部分。必须直接指出这篇新闻能如何转化为我的实际行动。
   <!-- ⚠️ 请把下面的维度替换为你自己认为的「高价值转化方向」 -->
   <!-- 示例维度（根据你的需求增删）：-->
   <!-- - 研究方向或论文思路 -->
   <!-- - 能在 GitHub 上获得高星的开源项目切入点 -->
   <!-- - 面试时的降维打击考点 -->
   <!-- - 投资的具体标的或避坑指南 -->
   <!-- - 产品灵感 / 创业机会 -->
   <!-- - 技术选型参考 -->
   - 在此列出你认为最重要的价值转化维度

### 输出质量标准

- 绝不点到为止：解释必须极其深刻，要让我产生真正的"真知灼见"，把它变成我大脑里的武器和知识。
- 信息完备：必须给出原文超链接（方便我随时查阅）。但不可以给标题上，h2h3h4任何级别的都不行！这会导致标题被引用的时候特别长 important！
- 重认知增量：让我读完这篇报告后，完全不需要再去刷原网页就能吸收 100% 的核心养分。

### 输出
报告的保存路径是 `./news/{YYYY-MM-DD 全网信息}.md`，路径可按需修改。

**最重要的指令！** 按板块分 todo item 逐个处理（GitHub、Product Hunt、36Kr、腾讯新闻、华尔街见闻、V2EX、微博、Reddit/X），每个 todo item 都必须有本文要求的高质量深度分析，不能点到为止！
