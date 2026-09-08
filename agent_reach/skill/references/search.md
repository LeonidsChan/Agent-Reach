# 搜索工具

网页调研默认组合 Exa 与 Tavily，取并集后去重。只有任务明显偏向一种来源，或另一个后端未配置时才单跑。

## 选型

| 引擎 | 擅长 | 何时单跑 |
|------|------|---------|
| **Exa** | 英文内容、技术文档、代码上下文 | 纯技术或代码问题 |
| **Tavily** | 新闻、时效性内容、深度检索 | 纯新闻或时效性查询 |

先用 `agent-reach doctor --json` 和 `mcporter list` 确认后端存在。某个后端未配置时，记录实际降级，不要把配置文件存在当成在线可用。

## Exa AI 搜索

```bash
mcporter call exa.web_search_exa query="query" numResults=5
mcporter call exa.web_search_exa query="library API code example" numResults=5
```

| 场景 | 参数 |
|-----|------|
| 网页搜索 | `web_search_exa(query: "...", numResults: 5)` |
| 技术资料 | `web_search_exa(query: "框架名 API 示例", numResults: 5)` |

> Exa MCP 的 `get_code_context_exa` 已弃用且默认不注册。代码问题也使用
> `web_search_exa`；需要精确搜索仓库内容时，改用 `dev.md` 中的 GitHub 搜索。

## Tavily 搜索

```bash
# 基础网页搜索
mcporter call tavily.tavily_search query="query" max_results=5

# 深度检索
mcporter call tavily.tavily_search query="query" search_depth="advanced"

# 限定域名和日期
mcporter call tavily.tavily_search query="query" include_domains="arxiv.org" start_date="2025-01-01"
```

| 场景 | 参数 |
|-----|------|
| 网页搜索 | `tavily_search(query: "...", max_results: 5)` |
| 深度检索 | `tavily_search(query: "...", search_depth: "advanced")` |
| 限定来源 | `tavily_search(query: "...", include_domains: "domain.com")` |
| 排除来源 | `tavily_search(query: "...", exclude_domains: "domain.com")` |
| 日期范围 | `start_date` / `end_date`，格式为 YYYY-MM-DD |
| 指定国家 | `country: "United States"`，使用国家全称 |

用 `mcporter list tavily --schema` 查看当前注册参数；接口升级后以实时 schema 为准。

## 失败重试

- Exa 429：共享额度已耗尽，切换 Tavily，或检查当前项目/用户级 mcporter 配置。
- Tavily 401/403：检查 API Key 与 mcporter 配置，保留 Exa 结果继续任务。
- `Unknown MCP server`：说明当前工作目录和用户级配置均未注册该后端；不要声称该后端可用。

## 与其他搜索工具对比

| 工具 | 来源 | 适用场景 |
|-----|------|---------|
| Exa | agent-reach | 英文、技术、代码资料 |
| Tavily | agent-reach | 新闻、时效性、深度检索 |
| 智谱搜索 | my-mcp-tools | 中文搜索 |
| GitHub 搜索 | agent-reach (dev.md) | 仓库和代码搜索 |
