---
name: paper-research-survey-skill
description: 针对用户给定的研究方向或主题，通过 MCP 工具搜索学术论文，生成带评分的论文列表和研究脉络分析。默认搜索最近2年，也支持用户指定年份（如"2020年的论文"、"2019-2021年"）。当用户提到"调研"、"文献综述"、"研究进展"、"最新论文"、"survey"、"literature review"、"research trend"、"这个方向有哪些工作"、"帮我找论文"、"相关研究"、"某年的论文"、"papers from YYYY"等意图时触发。即使用户只是随口问某个技术方向"最近有什么新进展"，也应该触发此 skill。
---

# Research Survey

根据用户给定的研究方向，通过 arXiv MCP、Google Scholar MCP、Semantic Scholar MCP 搜索论文，生成结构化的调研报告。默认搜索最近 2 年，支持用户指定任意年份或年份范围。

## 工作流程

### 第一步：理解研究方向

从用户的描述中提取：
- 核心研究主题和关键词（中英文）
- 细分方向或约束条件（如果有）
- 用户关注的侧重点（方法、应用、理论等）
- 时间范围：
  - 用户指定了具体年份（如"2020年的论文"）→ 搜索该年份
  - 用户指定了年份范围（如"2019到2021年"）→ 搜索该范围
  - 用户未指定年份 → 默认搜索最近 2 年，以最新工作优先

如果用户描述模糊（主题不清），先追问确认再开始搜索。年份不明确时直接使用默认值，无需追问。

### 第二步：多源搜索论文

使用 MCP 工具搜索论文。优先使用免费的 arXiv MCP 和 Google Scholar MCP，再用 Semantic Scholar MCP 做补充。

#### 搜索源优先级（按成本排序）

1. **arXiv MCP（免费，首选）**
   - 使用 `mcp__arxiv-mcp-server__search_papers` 搜索论文
   - 利用 `categories` 参数限定领域（如 `cs.AI`, `cs.LG`, `cs.CL` 等）提高相关性
   - 利用 `date_from` / `date_to` 参数控制时间范围
   - 使用引号短语精确匹配关键概念，如 `"multi-agent systems"`
   - 用 `ti:` / `abs:` / `au:` 前缀做字段级搜索
   - 每组关键词发起 2-3 次不同组合的搜索，`max_results` 设为 15-20
   - 对重要论文可用 `mcp__arxiv-mcp-server__download_paper` 下载并用 `mcp__arxiv-mcp-server__read_paper` 阅读全文

2. **Google Scholar MCP（免费，补充）**
   - 使用 `mcp__google-scholar-mcp-server__search_google_scholar_key_words` 做关键词搜索
   - 使用 `mcp__google-scholar-mcp-server__search_google_scholar_advanced` 做高级搜索，支持 `author` 和 `year_range` 过滤
   - 每组关键词发起 1-2 次搜索，`num_results` 设为 10
   - 用于发现 arXiv 之外的顶会/顶刊论文，以及获取引用量信息

3. **Semantic Scholar MCP（有积分消耗，补充用）**
   - 使用 `mcp__semantic-scholar-mcp-server__search_papers` 或 `mcp__semantic-scholar-mcp-server__search_by_topic` 搜索
   - 使用 `mcp__semantic-scholar-mcp-server__get_paper_details` 获取单篇论文的详细信息（引用量、venue 等）
   - 使用 `mcp__semantic-scholar-mcp-server__get_papers_batch` 批量获取论文详情（更高效）
   - 使用 `mcp__semantic-scholar-mcp-server__get_paper_citations` 和 `mcp__semantic-scholar-mcp-server__get_paper_references` 探索引用网络
   - 如果返回错误或限流，直接跳过，不要重试，不要阻塞流程
   - 优先使用批量的命令，减少请求次数
   - 主要用于：补充引用量、venue 信息，以及发现 arXiv/Google Scholar 未覆盖的论文

#### 搜索策略
- 使用英文关键词搜索（学术论文是英文，不用搜索中文论文）
- 组合多组关键词以覆盖不同表述
- 默认情况下以最新工作优先；用户指定年份时才做精确限定
- 研究基础工作除外!
- 目标：去重后保留 15-25 篇最相关的论文
- 尽量并行调用多个 MCP 工具以提高效率

#### 容错规则
- 任何单一搜索源失败都不应阻塞整个流程，跳过并继续
- 如果 Semantic Scholar 不可用，引用量可标记为 "N/A"，评分时该维度使用中间值
- 至少要从 arXiv MCP 或 Google Scholar MCP 获取到足够的论文才能继续后续步骤

### 第三步：收集论文元数据

对搜索到的每篇论文，尽可能收集以下信息：
- 标题
- 作者
- 发表时间
- 发表venue（会议/期刊名称，或 arXiv preprint）
- 引用量（优先从 Google Scholar 结果获取，或通过 Semantic Scholar MCP 补充，不可用时标记 N/A）
- arXiv ID 或 DOI
- 摘要（简要）
- 核心方法：一句话概括论文提出的方法、框架或核心思路
- 关键结果：最突出的实验贡献，如 SOTA 指标提升、关键发现等

元数据获取策略（按优先级）：

1. **arXiv MCP 搜索结果**：`search_papers` 返回的结果已包含标题、作者、摘要、日期、categories 等
2. **Google Scholar MCP 结果**：包含标题、作者、年份、引用量等
3. **Semantic Scholar MCP 补充**：使用 `get_paper_details` 或 `get_papers_batch` 获取引用量、venue 等详细信息。如果限流，跳过不重试
4. **arXiv 全文阅读**：对关键论文，使用 `download_paper` + `read_paper` 获取完整内容以提取核心方法和关键结果

### 第四步：论文评分

为每篇论文计算一个综合评分（满分 10 分），评分依据：

**引用量可用时：**

| 维度 | 权重 | 评分规则 |
|------|------|----------|
| 引用量 | 40% | 根据该领域论文的引用分布相对评分，引用量越高分越高 |
| 发表venue | 35% | 顶会/顶刊 = 高分，知名会议/期刊 = 中分，arXiv preprint = 基础分 |
| 时效性 | 15% | 越近期的论文分越高 |
| 相关性 | 10% | 与用户查询主题的匹配程度 |

**引用量不可用时（Semantic Scholar 限流）：**

| 维度 | 权重 | 评分规则 |
|------|------|----------|
| 发表venue | 50% | 同上 |
| 时效性 | 25% | 同上 |
| 相关性 | 25% | 同上 |

> 引用量不可用时在报告中注明，引用量列标记为 "N/A"。

venue 评分参考（可根据领域调整）：
- 顶级（9-10）：NeurIPS, ICML, ICLR, CVPR, ACL, Nature, Science 等
- 优秀（7-8）：AAAI, IJCAI, ECCV, EMNLP, NAACL 等
- 良好（5-6）：其他知名会议/期刊
- 基础（3-4）：arXiv preprint（未正式发表）

### 第五步：生成调研报告

输出一份 Markdown 文件，结构如下：

```markdown
# [研究方向] 文献调研报告

> 调研时间：YYYY-MM-DD
> 搜索范围：[根据实际情况填写，如"最近2年（YYYY-MM ~ YYYY-MM）"或"指定年份：YYYY年"或"指定范围：YYYY ~ YYYY年"]
> 论文来源：arXiv MCP, Google Scholar MCP, Semantic Scholar MCP

## 一、论文列表

| ID | 标题 | 作者 | 年份 | Venue | 核心方法 | 关键结果 | 引用量 | 评分 |
|----|------|------|------|-------|----------|----------|--------|------|
| P01 | ... | ... | ... | ... | 一句话概括论文提出的核心方法/框架 | 最突出的实验结果或贡献（如SOTA指标提升） | ... | 8.5 |
| P02 | ... | ... | ... | ... | ... | ... | ... | 7.2 |

> 评分说明：满分10分，综合考虑引用量(40%)、发表venue(35%)、时效性(15%)、相关性(10%)

### PDF 获取方式
- arXiv 论文：访问 `https://arxiv.org/pdf/{arxiv_id}` 直接下载
- 其他论文：通过 DOI 在 Sci-Hub 或出版商网站获取
- 如需我帮你下载某篇论文的 PDF，请告诉我对应的 ID（如 P01）

## 二、研究关联分析

### 2.1 背景与问题起源

简要介绍该研究方向的起源：这个方向要解决什么核心问题？为什么这个问题重要？早期的经典工作（即使超出2年范围）是什么？为入门者建立基本认知框架。

### 2.2 技术演进脉络

按时间线或方法流派梳理研究的演进路径，使用论文简称而非完整标题。清晰展示：
- 哪些工作是奠基性的，后续工作在其基础上发展
- 方法之间的继承与改进关系（如 MethodB 改进了 MethodA 的哪个局限）
- 不同技术路线之间的分支与竞争
- 关键的范式转变节点（如从 X 范式转向 Y 范式的标志性工作）

### 2.3 研究主题聚类

将论文按研究子主题或技术路线分组，说明每组关注的核心问题和采用的主要思路，以及组间的关系和差异。帮助读者建立该方向的全景认知。

## 三、发展趋势

总结该方向目前的发展趋势：
- 主流方法的演进方向
- 尚未解决的关键问题
- 可能的未来研究方向
```

### 第六步：输出 Semantic Scholar 积分消耗

如果本次调研使用了 Semantic Scholar MCP，在报告生成完毕后：
1. 调用 `mcp__semantic-scholar-mcp-server__get_credit_usage` 获取本次会话的积分消耗情况
2. 在终端输出中附上积分消耗摘要，格式如下：

```
📊 Semantic Scholar API 积分消耗：共 X credits
   - search_papers: N 次, X credits
   - get_paper_details: N 次, X credits
   - ...
```

如果本次调研未使用 Semantic Scholar MCP，则跳过此步骤。

### 第七步：终端输出摘要

Markdown 文件生成后，在终端中输出论文列表的前 5 行（评分最高的 5 篇），格式与报告中的表格一致，然后附上一行提示：

```
详细调研报告已保存至：[文件路径]，包含完整论文列表、研究关联分析和发展趋势。
```

### 论文 ID 规则
- 使用 P01, P02, P03... 作为文章 ID
- ID 按评分从高到低排列
- 用户后续可通过 ID 指定下载对应论文的 PDF

### PDF 下载

当用户要求下载某篇论文时（如"下载 P01"）：
1. 根据 ID 找到对应论文
2. 如果是 arXiv 论文，优先使用 `mcp__arxiv-mcp-server__download_paper` 下载
3. 如果有 DOI，尝试通过公开渠道获取
4. 将 PDF 保存到当前目录，文件名格式：`P{ID}_{简短标题}.pdf`
5. 如果无法直接下载，提供可访问的链接供用户手动下载

## 注意事项

- 搜索时使用英文关键词，但报告用中文撰写
- 论文简称应简洁易记，优先使用论文中提出的方法名称
- 如果某个方向论文数量很多，优先保留评分高的，控制在 15-25 篇
- 研究关联分析中避免罗列，要体现论文之间的逻辑关系
- 发展趋势部分要有洞察，不要只是简单总结
- 尽量并行调用不同 MCP 源的搜索，减少等待时间
- Semantic Scholar 有积分消耗，非必要不频繁调用；优先用 arXiv 和 Google Scholar 的免费结果
