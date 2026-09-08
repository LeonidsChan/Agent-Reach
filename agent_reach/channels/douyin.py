# -*- coding: utf-8 -*-
"""Douyin video search via OpenCLI and the user's Chrome session."""

from ._opencli_site import OpenCLISiteChannel


class DouyinChannel(OpenCLISiteChannel):
    name = "douyin"
    description = "抖音视频搜索"
    site = "douyin"
    domains = ("douyin.com", "iesdouyin.com")
    usage = 'opencli douyin search "query" --limit 10 -f yaml'
    login_hint = "douyin.com"
