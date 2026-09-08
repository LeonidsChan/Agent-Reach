# -*- coding: utf-8 -*-
"""Zhihu search via OpenCLI with an authentication-free site-search fallback."""

import re

from ._opencli_site import OpenCLISiteChannel

_MIN_OPENCLI_VERSION = (1, 8, 5)


def _opencli_supports_zhihu(version: str) -> bool:
    """Return whether the installed OpenCLI version contains the Zhihu adapter."""
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        return False
    return tuple(int(part) for part in match.groups()) >= _MIN_OPENCLI_VERSION


class ZhihuChannel(OpenCLISiteChannel):
    name = "zhihu"
    description = "知乎内容搜索与阅读"
    site = "zhihu"
    domains = ("zhihu.com",)
    usage = 'opencli yahoo search "site:zhihu.com query" --limit 10 -f yaml'
    login_hint = "zhihu.com"
    backends = [
        "OpenCLI Zhihu（登录态）",
        "OpenCLI Yahoo 站点搜索（公开）",
    ]

    def check(self, config=None):
        """Report the public search path as usable without claiming Zhihu login."""
        from agent_reach.backends import opencli_status

        self.active_backend = None
        status = opencli_status()
        if not status.installed:
            return "off", (
                "需要 OpenCLI 1.8.5+。安装：\n"
                "  agent-reach install --channels opencli"
            )
        if status.broken:
            return "error", status.hint
        if not _opencli_supports_zhihu(status.version):
            return "warn", (
                f"OpenCLI {status.version or '版本未知'} 未确认包含知乎适配器。升级：\n"
                "  npm install -g @jackwener/opencli@latest"
            )
        if status.ready:
            self.active_backend = self.backends[1]
            return "ok", (
                "公开站点搜索可用，无需知乎登录。用法："
                f"{self.usage}。登录知乎后可改用 "
                'opencli zhihu search "query" --limit 10 -f yaml，'
                "并读取问题、回答、文章和热榜"
            )
        return "warn", status.hint
