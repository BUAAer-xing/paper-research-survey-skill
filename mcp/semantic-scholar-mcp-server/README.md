# Semantic Scholar MCP Server

基于 [ai4scholar.net](https://ai4scholar.net) API 的 MCP 服务，提供学术论文搜索、作者查询、论文推荐等功能。

## 环境要求

- Python >= 3.10
- [uv](https://github.com/astral-sh/uv) 包管理器

## 安装

```bash
uv sync
```

## 配置

设置 API Key 环境变量：

```bash
export SEMANTIC_SCHOLAR_API_KEY="your_api_key_here"
```

## 运行

```bash
uv run python server.py
```

## MCP 客户端配置示例

```json
{
  "mcpServers": {
    "semantic-scholar": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/semantic-scholar-mcp-server",
      "env": {
        "SEMANTIC_SCHOLAR_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 工具列表

### 论文搜索（Paper）

| 工具 | 说明 | 积分 |
|------|------|------|
| `search_papers` | 关键词搜索论文 | 1 |
| `search_papers_bulk` | 批量搜索，支持 AND/OR 等复杂语法 | 2 |
| `match_paper_by_title` | 精确标题匹配 | 1 |
| `get_autocomplete` | 标题/作者补全建议 | 1 |
| `search_by_topic` | 按主题搜索，支持年份范围过滤 | 1 |

### 论文详情（Paper Detail）

| 工具 | 说明 | 积分 |
|------|------|------|
| `get_paper_details` | 获取论文详细信息 | 1 |
| `get_paper_authors` | 获取论文作者列表 | 1 |
| `get_paper_citations` | 获取引用该论文的文献 | 1 |
| `get_paper_references` | 获取论文的参考文献 | 1 |
| `get_papers_batch` | 批量获取多篇论文详情 | 2 |

### 作者（Author）

| 工具 | 说明 | 积分 |
|------|------|------|
| `search_authors` | 按姓名搜索作者 | 1 |
| `get_author_details` | 获取作者详细信息 | 1 |
| `get_author_papers` | 获取作者发表的论文 | 1 |
| `get_authors_batch` | 批量获取多位作者信息 | 2 |

### 推荐与片段（Recommendation）

| 工具 | 说明 | 积分 |
|------|------|------|
| `search_snippets` | 文本片段搜索 | 1 |
| `get_recommendations_for_paper` | 基于单篇论文推荐相关文献 | 1 |
| `get_recommendations_bulk` | 基于正负例推荐论文 | 1 |

### 积分管理（Credit）

| 工具 | 说明 |
|------|------|
| `get_credit_usage` | 查看当前会话的积分消耗统计 |
| `reset_credit_usage` | 重置积分计数器 |

## 项目结构

```
├── server.py                # 入口，注册工具并启动 MCP 服务
├── api_client.py            # 共享 HTTP 客户端（认证、GET/POST）
├── paper_tools.py           # 论文相关工具（10 个）
├── author_tools.py          # 作者相关工具（4 个）
├── recommendation_tools.py  # 推荐相关工具（3 个）
├── credit_tracker.py        # 积分追踪模块
└── pyproject.toml           # 项目配置
```
