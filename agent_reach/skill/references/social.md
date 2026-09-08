# 社交媒体 & 社区

小红书、Twitter/X、B站、微信公众号、抖音、知乎、V2EX、Reddit、Facebook、Instagram。

## 小红书 / XiaoHongShu（多后端）

小红书有三个后端，**先跑 `agent-reach doctor --json` 看 xiaohongshu 的 `active_backend` 是哪个**，再用对应命令组。

### 后端 A：OpenCLI（桌面首选）

```bash
# 搜索笔记
opencli xiaohongshu search "query" -f yaml

# 读笔记正文+互动数据（用搜索结果里的完整 URL，含 xsec_token）
opencli xiaohongshu note "NOTE_URL" -f yaml

# 评论（支持楼中楼）
opencli xiaohongshu comments NOTE_ID -f yaml

# 首页推荐 feed
opencli xiaohongshu feed -f yaml

# 用户主页公开笔记
opencli xiaohongshu user USER_ID -f yaml
```

> 要求 Chrome 打开且装了 OpenCLI 扩展。OpenCLI 只使用用户已经存在且明确控制
> 的 Chrome 会话；Agent Reach 不替用户登录，也不读取浏览器 Cookie。
> `agent-reach configure xhs-cookies` 不会把 Cookie 注入 OpenCLI。
> 如果没有现成会话，不要自动登录；改走后端 B/C，并按对应的
> Cookie-Editor 手工导出流程配置。

### 后端 B：xiaohongshu-mcp（服务器场景）

```bash
# 认证前先让用户用 Cookie-Editor 手工导出，再显式导入
agent-reach configure xhs-cookies

# 只读检查当前状态
mcporter call xiaohongshu.check_login_status --timeout 120000

# 搜索
mcporter call xiaohongshu.search_feeds keyword="query" --timeout 120000

# 笔记详情+评论（feed_id 和 xsec_token 从搜索结果取）
mcporter call xiaohongshu.get_feed_detail feed_id="..." xsec_token="..." --timeout 120000
```

> 首次调用会自动下载约 150MB 无头浏览器，务必带 `--timeout 120000`。
> 认证只走 Cookie-Editor 手工导出；导入后先运行 `check_login_status`。
> 该显式命令会保存/导入用户提供的 xiaohongshu.com 同域 Cookie 集，用户应
> 确认范围；非 xiaohongshu.com 域 Cookie 会被忽略。

### 后端 C：xhs-cli（存量备选，上游 2026-03 起停更）

```bash
xhs search "query"          # 搜索
xhs read NOTE_ID_OR_URL     # 读笔记（必须用搜索结果中的 URL/ID，不能裸 note_id）
xhs comments NOTE_ID_OR_URL # 评论
xhs hot                     # 热门
xhs feed                    # 推荐
```

> 已知不稳定：`xhs user` / `xhs user-posts` / `xhs favorites` 可能返回 API error（上游停更无人修）。新装用户建议直接走后端 A/B。

### 通用注意事项

> **认证边界**: Agent Reach 不得替用户执行小红书登录，也不得读取浏览器
> Cookie。OpenCLI 只能使用用户已有且明确控制的 Chrome 会话；
> xiaohongshu-mcp / 存量工具使用 Cookie-Editor 手工导出。
>
> **xsec_token 限制**: 小红书强制 xsec_token 机制，**不能直接用裸 note_id 去读**。正确流程：先搜索/feed 拿结果，再用结果中的完整 URL/ID 去读。三个后端都一样。
>
> **频率控制**: 高频请求（批量搜索、深翻评论）会触发验证码，平台限制无法绕过。每次操作间隔 2-3 秒。
>
> **写操作（发帖/评论/点赞）**: 建议只读。xhs-cli v0.6.x 写操作可能因签名问题返回 406。

## Twitter/X (twitter-cli)

### 认证前置条件

`agent-reach configure twitter-cookies` 通过隐藏输入保存的 Cookie 只供
`agent-reach doctor` 检查显式凭据是否齐全。`doctor` 不执行上游
`twitter status`，也不会设置当前 Shell。运行下面任何 `twitter` 命令前，
必须在同一个 Shell 或子进程环境中显式提供：

```bash
export TWITTER_AUTH_TOKEN="..."
export TWITTER_CT0="..."
```

### 稳定命令

```bash
# 首页时间线（最稳定）
twitter feed -n 20

# 读取单条推文（含回复）
twitter tweet URL_OR_ID

# 读取长文 / X Article
twitter article URL_OR_ID

# 用户时间线
twitter user-posts @username -n 20

# 用户资料
twitter user @username
```

### 可能不稳定的命令

```bash
# 搜索推文（Twitter 频繁改 GraphQL 端点，可能 404）
twitter search "query" -n 10

# likes（2024 年后只能看自己的，平台限制）
twitter likes
```

### search 失败时的重试链（按序执行，成功即停）

1. 直接重试一次（偶发失败常见）：`twitter search "query" -n 10`
2. 升级后再试：`pipx upgrade twitter-cli && twitter search "query" -n 10`
3. 换 OpenCLI 备选（桌面，复用浏览器登录态）：`opencli twitter search "query" -f yaml`
4. 都不行就改用 `twitter feed` / `twitter user-posts @somebody` 等稳定命令绕路

### 重要注意事项

> **安装**: `pipx install twitter-cli`（确保 v0.8.5+）
>
> **认证**: 只用 Cookie-Editor 手工导出，再显式设置环境变量
> `TWITTER_AUTH_TOKEN` + `TWITTER_CT0`；不要依赖自动浏览器读取。
>
> **IP 风控**: 不要在 VPS/数据中心 IP 上频繁调用，尤其是 followers/following，有封号风险。使用住宅代理或本地环境。
>
> **OpenCLI 备选**: 桌面装了 OpenCLI 的话，`opencli twitter search/article/user-posts -f yaml` 全套可用（浏览器登录态，无需 cookie 环境变量）。
>
> **输出格式**: 建议用 `--yaml` 或 `--json` 获得结构化输出，对 AI agent 更友好。

## B站 / Bilibili

> ⚠️ **不要用 yt-dlp 读 B站**（风控已全面 412 拦截，实测无解）。用 bili-cli / OpenCLI。

```bash
# 搜索 / 热门 / 视频详情（bili-cli，只读无需登录）
bili search "query" --type video -n 5
bili hot -n 10
bili video BVxxx

# 字幕（OpenCLI，需桌面 Chrome）
opencli bilibili subtitle BVxxx
```

> 详细命令（音频转写、API 直连兜底）见 [references/video.md](video.md)。

## V2EX (公开 API)

无需认证，直接调用公开 API。v2ex.com 部分网络直连被墙，
**直连失败时自动经本地代理重试**（代理发现见 references/web.md 的 arcurl）：

```bash
arcurl() { curl -s -m 15 "$@" || curl -s -m 20 -x http://127.0.0.1:7890 "$@"; }
arcurl "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"
```

### 节点主题

```bash
# node_name 如: python, tech, jobs, qna, programmers
curl -s "https://www.v2ex.com/api/topics/show.json?node_name=python&page=1" -H "User-Agent: agent-reach/1.0"
```

### 主题详情

```bash
# topic_id 从 URL 获取，如 https://www.v2ex.com/t/1234567
curl -s "https://www.v2ex.com/api/topics/show.json?id=TOPIC_ID" -H "User-Agent: agent-reach/1.0"
```

### 主题回复

```bash
curl -s "https://www.v2ex.com/api/replies/show.json?topic_id=TOPIC_ID&page=1" -H "User-Agent: agent-reach/1.0"
```

### 用户信息

```bash
curl -s "https://www.v2ex.com/api/members/show.json?username=USERNAME" -H "User-Agent: agent-reach/1.0"
```

### Python 调用示例

```python
from agent_reach.channels.v2ex import V2EXChannel

ch = V2EXChannel()

# 获取热门帖子
topics = ch.get_hot_topics(limit=10)
for t in topics:
    print(f"[{t['node_title']}] {t['title']} ({t['replies']} 回复)")

# 获取节点帖子
node_topics = ch.get_node_topics("python", limit=5)

# 获取帖子详情 + 回复
topic = ch.get_topic(1234567)
print(topic["title"], "—", topic["author"])

# 获取用户信息
user = ch.get_user("Livid")
```

> **节点列表**: https://www.v2ex.com/planes

## Reddit（多后端，必须登录态）

**Reddit 没有零配置路径**：匿名 `.json` 端点已被封（403），官方 API 自 2025-11 起人工审批基本不批。两个后端都靠登录态，先跑 `agent-reach doctor --json` 看 reddit 的 `active_backend`。中国大陆访问需代理。

### 后端 A：OpenCLI（桌面首选，复用浏览器登录态）

```bash
# 搜索帖子
opencli reddit search "query" -f yaml

# 读帖子全文 + 评论
opencli reddit read POST_ID -f yaml

# 浏览 subreddit / 热门 / Popular
opencli reddit subreddit LocalLLaMA -f yaml
opencli reddit hot -f yaml
opencli reddit popular -f yaml

# subreddit 元信息（订阅数、简介）
opencli reddit subreddit-info LocalLLaMA -f yaml
```

> 要求 Chrome 打开且浏览器里登录过 reddit.com。

### 后端 B：rdt-cli（存量/服务器备选，上游 2026-03 起停更）

```bash
rdt search "query" --limit 10   # 搜索帖子
rdt read POST_ID                # 读帖子全文 + 评论
rdt sub python --limit 20       # 浏览 subreddit
rdt popular --limit 10          # 浏览热门
rdt all --limit 10              # 浏览 /r/all
```

> **安装**: `pipx install 'git+https://github.com/public-clis/rdt-cli.git'`（PyPI 版本落后，需从 GitHub 装 v0.4.2+）。先 `rdt login` 才能搜索和阅读（服务器无浏览器时手动写 Cookie，见 doctor 提示）。
> 建议使用 `--yaml` 输出，对 AI agent 更友好。

### 高级选项：官方 API + PRAW（仅限已有凭证的用户）

2025-11 前注册过 Reddit script app（持有 client_id/client_secret）的用户可以用 PRAW 走官方 API（100 QPM 免费）。新申请需人工审批且个人项目基本不批，**不要推荐新用户走这条路**。

## Facebook（OpenCLI，必须登录态）

Facebook 走 OpenCLI，复用用户 Chrome 里的 facebook.com 登录态。先跑 `agent-reach doctor --json` 看 facebook 的 `active_backend`，正常应为 `OpenCLI`。不要推荐 Jina/Exa/Graph API 作为默认路径。

```bash
# 搜索用户 / 主页 / 帖子
opencli facebook search "query" -f yaml

# 用户或主页信息
opencli facebook profile zuck -f yaml

# 当前账号 News Feed
opencli facebook feed --limit 10 -f yaml

# 当前账号可见的群组列表/最近动态
opencli facebook groups --limit 20 -f yaml
```

> 要求 Chrome 打开且装了 OpenCLI 扩展，并已登录 facebook.com。Facebook Groups 当前只承诺读取当前账号可见的群组列表/最近动态，不承诺任意群帖子和评论 API。

## Instagram（OpenCLI，必须登录态）

Instagram 走 OpenCLI，复用用户 Chrome 里的 instagram.com 登录态。先跑 `agent-reach doctor --json` 看 instagram 的 `active_backend`，正常应为 `OpenCLI`。不要默认恢复 instaloader；历史上 cookies/401/429 不稳定。

```bash
# 搜索用户（不是全站帖子关键词搜索）
opencli instagram search "query" -f yaml

# 用户 Profile
opencli instagram profile nasa -f yaml

# 用户最近帖子
opencli instagram user nasa --limit 12 -f yaml

# Explore / Discover
opencli instagram explore --limit 20 -f yaml

# 当前账号收藏
opencli instagram saved --limit 20 -f yaml
```

> 要求 Chrome 打开且装了 OpenCLI 扩展，并已登录 instagram.com。`instagram search` 是用户搜索；读帖子需要先确定 username，再用 `instagram user USERNAME`。若出现 429 / login required，先让用户在 Chrome 里重新登录并降低频率。

## 微信公众号文章（OpenCLI + miku_ai + Camoufox）

将“搜索摘要”和“读取完整正文”分开处理：

| 目标 | 首选后端 | 说明 |
|---|---|---|
| 搜标题/日期/摘要 | OpenCLI | 快速、免登录，但结果 URL 常是搜狗中转链接 |
| 获取真实原文 URL | `miku_ai` | 返回 `mp.weixin.qq.com` URL、公众号名和日期 |
| 读取完整正文 | `wechat-article-for-ai` / Camoufox | 绕过微信反爬并输出 Markdown |

### 1. 快速搜索摘要

```bash
opencli weixin search "关键词" --page 1 --limit 10 -f yaml
```

如果 URL 是 `https://weixin.sogou.com/link?...`，**不要**直接传给
`opencli weixin download`。该下载器只接受 `mp.weixin.qq.com`；搜狗中转常跳到
`/antispider/`，会表现为 `invalid URL`，这不代表微信公众号无法搜索。

### 2. 搜索真实微信原文 URL

本机固定使用独立环境：

```bash
WECHAT_TOOL="$HOME/.agent-reach/tools/wechat-article-for-ai"
"$WECHAT_TOOL/.venv/bin/python" - <<'PY'
import asyncio
from miku_ai import get_wexin_article

async def main():
    for article in await get_wexin_article("关键词", 5):
        print(article["title"], article["source"], article["url"], sep="\t")

asyncio.run(main())
PY
```

注意上游函数名确实拼作 `get_wexin_article`。搜索偶尔因代理频控返回空列表；降低频率，
换同义关键词后重试，不要并发轰炸。

### 3. 用 Camoufox 抓完整正文

```bash
WECHAT_TOOL="$HOME/.agent-reach/tools/wechat-article-for-ai"
cd "$WECHAT_TOOL"
"$WECHAT_TOOL/.venv/bin/python" main.py \
  "https://mp.weixin.qq.com/s/ARTICLE_OR_SIGNED_URL" \
  -o /tmp/weixin-articles --no-images -v
```

成功标准：日志出现 `Title`、`Author` 和 `Saved`，输出 Markdown 应包含正文段落，
不能只有搜索摘要或验证页。需要图片时去掉 `--no-images`。

### 安装 / 修复完整正文链路

目录不存在或 `miku_ai` 无法导入时：

```bash
mkdir -p "$HOME/.agent-reach/tools"
git clone https://github.com/bzd6661/wechat-article-for-ai.git \
  "$HOME/.agent-reach/tools/wechat-article-for-ai"
python3 -m venv "$HOME/.agent-reach/tools/wechat-article-for-ai/.venv"
"$HOME/.agent-reach/tools/wechat-article-for-ai/.venv/bin/pip" install \
  -r "$HOME/.agent-reach/tools/wechat-article-for-ai/requirements.txt" \
  miku-ai 'playwright==1.60.0'
```

首次运行会自动下载 Camoufox 浏览器。若访问 GitHub Releases API 报
`403 rate limit exceeded`，优先稍后重试；若 `gh auth status` 已登录，可用 `gh release
download` 下载对应 macOS/Linux 架构的 Camoufox release asset 到
`~/Library/Caches/camoufox`（macOS）或平台缓存目录。

### 已验证故障表（2026-07-03）

| 症状 | 原因 | 处理 |
|---|---|---|
| OpenCLI 能搜，download 报 `invalid URL` | 传入搜狗中转 URL | 用 `miku_ai` 获取真实 `mp.weixin.qq.com` URL |
| 跳到 `weixin.sogou.com/antispider` | 搜狗中转反爬 | 不再解析中转，改走 `miku_ai` |
| `ModuleNotFoundError: miku_ai` | 完整正文工具链未安装 | 按上方独立 venv 安装 |
| Camoufox fetch 报 GitHub API 403 | 匿名 Releases API 限流 | 稍后重试或用已认证 `gh` 下载 release asset |
| `Browser.setDefaultViewport` / `isMobile` schema 错误 | Playwright 1.61 与 Camoufox Juggler 不兼容 | 固定 `playwright==1.60.0`；见 daijro/camoufox#653 |
| 微信验证/CAPTCHA | 微信风控 | 加 `--no-headless` 人工完成验证，再重试 |

实测：上述链路成功抓取《量化CTA风格因子跟踪 · 库存指数上涨，期限结构因子筑底回升》，
生成约 5,348 字 Markdown，并正确解析标题、作者、日期与 14 张图片。

> `weixin search` 搜的是公众号文章，不等同于微信联系人、群聊或聊天记录搜索。

## 抖音（OpenCLI，浏览器会话）

抖音搜索走 OpenCLI，复用 Chrome 会话。先跑 doctor；若搜索超时或提示安全状态，先在 Chrome 登录 `douyin.com` 并完成验证码/安全验证。

```bash
# 关键词搜索视频
opencli douyin search "关键词" --limit 10 -f yaml

# 指定作者视频（sec_uid 来自作者主页 URL）
opencli douyin user-videos SEC_UID --limit 20 --with_comments true -f yaml

# 登录及状态检查
opencli douyin login -f yaml
opencli douyin whoami -f yaml
```

> 只把 `search` / `user-videos` 当作读取能力。发布、删除、更新等写操作不属于 Agent Reach 的默认只读范围，必须另行获得用户明确授权。

## 知乎（OpenCLI 原生 + 公开搜索回退）

知乎提供两条读取路径。优先尝试原生适配器；若返回 `AUTH_REQUIRED`，立即切换
Yahoo 的站点限定搜索，基础搜索无需知乎登录。

```bash
# 原生站内搜索（需要 Chrome 中已有知乎登录态）
opencli zhihu search "关键词" --limit 10 -f yaml

# 无登录回退：结果仍限定为知乎问题和专栏文章
opencli yahoo search "site:zhihu.com 关键词" --limit 10 -f yaml
```

登录后还可读取问题、回答、文章和热榜：

```bash
opencli zhihu question QUESTION_ID --limit 10 -f yaml
opencli zhihu answer-detail ANSWER_ID -f yaml
opencli zhihu download --url "https://zhuanlan.zhihu.com/p/ARTICLE_ID" -f yaml
opencli zhihu hot --limit 20 -f yaml
opencli zhihu user USERNAME -f yaml
```

> `agent-reach doctor --json` 的 `active_backend` 默认报告公开回退，因为 Doctor
> 不读取浏览器 Cookie，也不把扩展连通误报成已登录。遇到验证码或风控时降低频率；
> 公开搜索只承诺搜索引擎已索引内容，时效性和结果完整度低于登录后的原生搜索。
