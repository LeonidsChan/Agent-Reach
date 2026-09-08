# -*- coding: utf-8 -*-
"""WeChat Official Account article search via OpenCLI/Sogou Weixin."""

from ._opencli_site import OpenCLISiteChannel


class WeChatOfficialChannel(OpenCLISiteChannel):
    name = "wechat_official"
    description = "微信公众号文章搜索"
    site = "weixin"
    domains = ("mp.weixin.qq.com", "weixin.sogou.com")
    usage = 'opencli weixin search "query" --limit 10 -f yaml'
    login_hint = "mp.weixin.qq.com"
    login_required = False
