"""前台路由守卫口径固化（防「点我的订单没反应」这类回归）。

历史故障：guard.js 在 `location.replace` 之后调 `window.stop()`，跳转被一起掐掉，
页面又被置为不可见，表现为点了链接原地不动或白屏。这里把口径钉死：
- 不出现 window.stop；
- 未登录 → 解析前跳 login.html?redirect=<原页>，且带不可见的兜底恢复；
- 守卫名单与 auth.js 的 NEED_LOGIN 保持一致，避免两处漂移。
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FRONT = os.path.join(ROOT, "front")
GUARD = os.path.join(FRONT, "js", "guard.js")


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _guard_js():
    return _read(GUARD)


def _guard_code():
    """去掉注释后的源码：注释里会提到 window.stop() 这类历史坑，不能当成实现。"""
    js = _guard_js()
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    return re.sub(r"^[ \t]*//.*$", "", js, flags=re.M)


def _list_from(js, name):
    match = re.search(name + r"\s*=\s*\[(.*?)\]", js, re.S)
    assert match, f"未找到 {name} 列表定义"
    return re.findall(r"'([^']+)'", match.group(1))


def test_guard_does_not_stop_navigation():
    js = _guard_code()
    assert "window.stop(" not in js, "window.stop() 会掐掉紧随其后的 location.replace，导致跳转失效"
    assert "location.replace('login.html?redirect=' + encodeURIComponent(back))" in js
    assert "var back = page + window.location.search;" in js


def test_guard_hides_before_redirect_and_recovers():
    js = _guard_code()
    hide_at = js.index("hide();\n    toLogin();")
    assert hide_at > 0, "必须先隐藏再跳转，否则会闪一下被保护的内容"
    assert "setTimeout(function ()" in js, "缺少跳转失败兜底"
    assert "}, 600);" in js, "兜底延时应为 600ms"
    assert "root.style.visibility = 'hidden'" in js, "用 visibility 隐藏，避免 bfcache 恢复后的空白"
    assert "display = 'none'" not in js
    assert "addEventListener('pageshow'" in js, "bfcache 恢复需按登录态修正可见性"
    assert "event.persisted" in js


def test_guard_lists_stay_in_sync_with_auth():
    guard_list = _list_from(_guard_js(), "PROTECTED")
    auth_list = _list_from(_read(os.path.join(FRONT, "js", "auth.js")), "NEED_LOGIN")
    assert sorted(guard_list) == sorted(auth_list), (
        "guard.js 的 PROTECTED 与 auth.js 的 NEED_LOGIN 不一致："
        f"{sorted(set(guard_list) ^ set(auth_list))}"
    )


def test_protected_pages_load_guard_in_head():
    protected = _list_from(_guard_js(), "PROTECTED")
    for name in protected:
        path = os.path.join(FRONT, name)
        assert os.path.isfile(path), f"守卫名单里的 {name} 不存在"
        html = _read(path)
        head = html.split("</head>")[0]
        assert '<script src="js/guard.js"></script>' in head, f"{name} 未在 <head> 同步加载 guard.js"
        # 必须在样式表之前，保证解析前就完成拦截，不闪内容
        assert head.index("js/guard.js") < head.index("css/style.css"), f"{name} 的 guard.js 应排在样式表之前"


def test_guard_target_is_login_page_with_redirect():
    js = _guard_js()
    assert "login.html?redirect=" in js
    assert "encodeURIComponent" in js
    # 登录后回跳仍在 auth.js，且做白名单校验（防开放重定向）
    auth = _read(os.path.join(FRONT, "js", "auth.js"))
    assert "function gotoAfterLogin" in auth
    assert r"^[\w\-./?=&%]+\.html([?#].*)?$" in auth
