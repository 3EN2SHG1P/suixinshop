import os
import socket
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
APP_DIR = BACKEND_DIR / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
# backend 根也要入 path：test_seed_demo 等需要 import seed 包（seed/ 与 app/ 平级）
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pytest
from fastapi.testclient import TestClient


def _exit_with_hint(message: str):
    """本地友好退出（码 0），CI / REQUIRE_DB 下按失败退出（码 1）。"""
    flags = (os.getenv("CI", ""), os.getenv("REQUIRE_DB", ""))
    strict = any(flag.strip().lower() not in ("", "0", "false", "no") for flag in flags)
    pytest.exit(message, returncode=1 if strict else 0)


def pytest_sessionstart(session):
    """配置或数据库不可用时，先给出能照做的修复提示。

    放在收集（collection）之前：让 client fixture 直接失败会级联成几十条 ERROR，
    报错信息里看不出真正原因。CI 里跳过等于把失败伪装成通过，所以用非零退出码。
    """
    try:
        from core.config import config as app_config
    except RuntimeError as exc:  # 缺 JWT_SECRET 等必填项，config 在 import 期就会抛
        _exit_with_hint(f"配置读取失败：{exc}\n修复：在 backend/.env 补齐必填项后重跑。")
        return

    host, port = app_config.db_host, app_config.db_port
    try:
        with socket.create_connection((host, port), timeout=3):
            return
    except OSError:
        pass
    _exit_with_hint(
        f"连不上 MySQL（{host}:{port}）。\n"
        "修复：项目根目录执行 `docker compose up -d`（或启动本机 MySQL），"
        "确认 backend/.env 的 DB_* 指向该实例后重跑。"
    )


@pytest.fixture(scope="session")
def client():
    import main
    from core.deps import clear_permission_cache

    with TestClient(main.app) as c:
        yield c
    clear_permission_cache()


@pytest.fixture(scope="session")
def admin_password():
    """管理员密码：必须由环境变量显式提供，不做任何默认值兜底。

    这样仓库里不会出现任何「可用弱密码」。未设置时相关用例 skip，
    而不是拿一个猜来的密码去撞库——后者会掩盖「本机还没 seed」这类真实问题。
    本地用法：backend/.env 里设置 ADMIN_INIT_PASSWORD 后执行 `python -m seed.runner base`。
    """
    pwd = os.getenv("ADMIN_INIT_PASSWORD", "").strip()
    if not pwd:
        pytest.skip(
            "未设置 ADMIN_INIT_PASSWORD：请在 backend/.env 中设置一个本机测试密码 "
            "（ADMIN_INIT_PASSWORD=<你的密码>）并执行 `uv run python -m seed.runner base` 后重跑测试"
        )
    return pwd


@pytest.fixture(scope="session")
def admin_token(client, admin_password):
    """登录取 token。

    失败必须是 skip 而不是 assert 失败：一旦这里硬失败，session 级 fixture 会级联成几十条
    ERROR，报错信息还完全看不出真正原因（密码不匹配 / admin 没建 / 被锁定）。
    这里给出可直接照做的修复步骤。
    """
    r = client.post("/api/v1/auth/login", json={"username": "admin", "password": admin_password})
    if r.status_code != 200 or r.json().get("code") != 0:
        pytest.skip(
            f"用 ADMIN_INIT_PASSWORD 登录 admin 失败（响应：{(r.json() or {}).get('message', r.text[:200])}）。\n"
            "常见原因：admin 还没建（没跑 seed base）、密码已被后台改过，或连续失败被锁定。\n"
            "修复：把 backend/.env 的 ADMIN_INIT_PASSWORD 改成想用的密码，再执行 "
            "`uv run python -m seed.runner base` —— base 会按该值覆盖密码并清零失败计数。"
        )
    return r.json()["data"]["token"]


@pytest.fixture(scope="session")
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}
