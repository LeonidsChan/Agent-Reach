# 网页阅读

通用网页、RSS。

## 通用网页 (Jina Reader)

`r.jina.ai` 在部分网络下直连被墙。**直连优先，失败自动经本地代理重试**：

```bash
# arcurl: 直连 15s 超时后, 自动走本地代理 (端口按本机实际, 可用 scutil --proxy 查 HTTPSProxy)
arcurl() { curl -s -m 15 "$@" || curl -s -m 20 -x http://127.0.0.1:7890 "$@"; }

# 读取任意网页内容
arcurl "https://r.jina.ai/URL"

# 示例
arcurl "https://r.jina.ai/https://example.com/article"
```

**适用场景**: 大多数网页可以直接用 Jina Reader 读取。不要全局 export
`https_proxy`——会把 tushare/westock 等国内数据源也路由进代理。

## Web Reader (MCP)

```bash
# 读取网页内容 (Markdown 格式)
mcporter call web-reader.webReader url="https://example.com"

# 保留图片
mcporter call web-reader.webReader url="https://example.com" retain_images=true

# 纯文本格式
mcporter call web-reader.webReader url="https://example.com" return_format="text"
```

**适用场景**: 需要更精确控制输出格式时使用。

## RSS (feedparser)

```python
python3 -c "
import feedparser
for e in feedparser.parse('FEED_URL').entries[:5]:
    print(f'{e.title} — {e.link}')
"
```

**适用场景**: 订阅博客、新闻源、播客等 RSS feed。

## 选择指南

| 场景 | 推荐工具 |
|-----|---------|
| 通用网页 | Jina Reader (`curl r.jina.ai`) |
| 需要图片/格式控制 | web-reader MCP |
| RSS 订阅 | feedparser |
