"""品牌素材约束：Logo 四处副本一致、带版权元数据、全站引用齐全。

Logo 为作者原创美术作品，不在 MIT 许可范围内（见 NOTICE）。这里把「换 Logo 时容易漏」
的点固化成测试：只换前台、只换 favicon、漏改页面引用、重新导出时丢掉 alpha 或版权元数据。
纯文件系统断言，不需要数据库。
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
LOGO_PAIRS = [
    (REPO_ROOT / "front" / "images" / "logo.png", REPO_ROOT / "manager" / "images" / "logo.png"),
    (
        REPO_ROOT / "front" / "images" / "logo-transparent.png",
        REPO_ROOT / "manager" / "images" / "logo-transparent.png",
    ),
]
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
COPYRIGHT_HOLDER = "3EN2SHG1P"
LEGACY_LOGO_REF_RE = re.compile(r"""["']([^"']*logo[^"']*\.(?:svg|jpe?g|gif|webp))["']""", re.I)
FAVICON_RE = re.compile(r'href="[^"]*logo-transparent\.png(?:\?v=\d+)?"')
HEADER_LOGO_RE = re.compile(r'class="logo"><img src="images/logo\.png(?:\?v=\d+)?"')


def _logo_files():
    return [p for pair in LOGO_PAIRS for p in pair]


def _png_info(path):
    data = path.read_bytes()
    assert data.startswith(PNG_MAGIC), f"{path} 不是 PNG：{data[:8]!r}"
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    color_type = data[25]
    return width, height, color_type, data


def _pages(*patterns):
    return sorted({p for pattern in patterns for p in REPO_ROOT.glob(pattern)})


@pytest.fixture
def front_pages():
    pages = _pages("front/*.html")
    assert pages, "未扫描到任何前台页面，请检查路径"
    return pages


@pytest.fixture
def manager_pages():
    pages = _pages("manager/*.html", "manager/pages/*/*.html")
    assert pages, "未扫描到任何后台页面，请检查路径"
    return pages


def test_logo_files_present_and_square():
    for path in _logo_files():
        assert path.is_file(), f"缺少 Logo 文件：{path}"
        width, height, color_type, _ = _png_info(path)
        assert width == height, f"{path} 应为正方形（当前 {width}x{height}），否则图标位会被裁切"
        assert width >= 256, f"{path} 分辨率过低（{width}px），至少 256px"
        assert color_type in (4, 6), f"{path} 需带 alpha 通道，否则深色背景下会出现白底方块"


def test_front_and_manager_logo_identical():
    for front_logo, manager_logo in LOGO_PAIRS:
        assert front_logo.read_bytes() == manager_logo.read_bytes(), (
            f"{front_logo.name} 前后台不一致：{front_logo} vs {manager_logo}"
        )


def test_logo_embeds_copyright_metadata():
    for path in _logo_files():
        *_, data = _png_info(path)
        assert b"tEXt" in data, f"{path} 缺少文本元数据块"
        assert b"Copyright" in data, f"{path} 缺少 Copyright 元数据"
        assert COPYRIGHT_HOLDER.encode() in data, f"{path} 的版权署名未包含 {COPYRIGHT_HOLDER}"


def test_front_pages_reference_logo_and_favicon(front_pages):
    missing = []
    for page in front_pages:
        text = page.read_text(encoding="utf-8")
        rel = page.relative_to(REPO_ROOT)
        if not FAVICON_RE.search(text):
            missing.append(f"{rel}: favicon 未指向 images/logo-transparent.png")
        if not HEADER_LOGO_RE.search(text):
            missing.append(f"{rel}: 顶部 logo 未指向 images/logo.png")
    assert not missing, "\n".join(missing)


def test_logo_urls_are_cache_busted():
    """换 Logo 后旧图会被浏览器 favicon 缓存长期钉住，引用需带版本参数。"""
    stale = []
    for page in _pages("front/*.html", "manager/*.html", "manager/pages/*/*.html"):
        for match in re.finditer(r'(?:href|src)="([^"]*logo[^"]*\.png)"', page.read_text(encoding="utf-8")):
            stale.append(f"{page.relative_to(REPO_ROOT)}: {match.group(1)}")
    assert not stale, "Logo 引用缺少 ?v= 版本参数：\n" + "\n".join(stale)


def test_manager_pages_reference_favicon(manager_pages):
    missing = []
    for page in manager_pages:
        text = page.read_text(encoding="utf-8")
        if "logo-transparent.png" not in text:
            missing.append(f"{page.relative_to(REPO_ROOT)}: favicon 未指向 logo-transparent.png")
    assert not missing, "\n".join(missing)


def test_admin_sidebar_injects_logo():
    common_js = (REPO_ROOT / "manager" / "js" / "common.js").read_text(encoding="utf-8")
    assert "images/logo.png" in common_js, "后台侧栏 Logo 由 common.js 注入，引用丢失会导致侧栏空白"


def test_no_legacy_logo_variants_referenced():
    offenders = []
    for page in _pages("front/*.html", "manager/*.html", "manager/pages/*/*.html"):
        for match in LEGACY_LOGO_REF_RE.finditer(page.read_text(encoding="utf-8")):
            offenders.append(f"{page.relative_to(REPO_ROOT)}: 引用了非标准 Logo 文件 {match.group(1)}")
    assert not offenders, "\n".join(offenders)


def test_site_logo_default_points_to_existing_file():
    seed_base = (REPO_ROOT / "backend" / "seed" / "base.py").read_text(encoding="utf-8")
    match = re.search(r'"basic\.site_logo",\s*"([^"]+)"', seed_base)
    assert match, "seed base 未配置 basic.site_logo"
    assert (REPO_ROOT / match.group(1).lstrip("/")).is_file(), (
        f"site_logo 默认值 {match.group(1)} 指向不存在的文件"
    )


def test_readme_shows_logo_and_notice():
    for name in ("README.md", "README.en.md"):
        text = (REPO_ROOT / name).read_text(encoding="utf-8")
        assert "./front/images/logo.png" in text, f"{name} 顶部缺少 Logo"
        assert "./NOTICE" in text, f"{name} 缺少 NOTICE 链接"


def test_notice_declares_logo_ownership():
    notice = (REPO_ROOT / "NOTICE").read_text(encoding="utf-8")
    assert COPYRIGHT_HOLDER in notice, "NOTICE 缺少著作权人署名"
    assert "MIT" in notice, "NOTICE 需说明 Logo 不适用 MIT 许可"
    assert "著作权" in notice, "NOTICE 需说明著作权归属"
    for logo in ("front/images/logo.png", "manager/images/logo.png"):
        assert logo in notice, f"NOTICE 未列明 {logo}"
