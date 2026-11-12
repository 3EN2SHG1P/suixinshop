"""settings 密钥脱敏回归。

覆盖三条链路：
1. 密钥类配置读取一律脱敏为 MASK，非密钥类不受影响；
2. 前端把 MASK 原样回传时不得覆盖库里的真实值；
3. 库里不存在的密钥键不接受 MASK，避免把占位符写进配置表。

依赖真实 MySQL 与已执行的 seed base + demo（与其余用例一致）；
ADMIN_INIT_PASSWORD 未设置或与 admin 当前密码不一致时由 conftest skip。
用例会临时改写 system_configs 中 logistics 分组的两个键，结束后恢复原值。
"""

import asyncio

import aiomysql
from aiomysql.cursors import DictCursor

from core.config import config
from services.settings import MASK

SECRET_KEY = "logistics.track_key"
PLAIN_KEY = "logistics.ship_time"


def _conn():
    return aiomysql.connect(
        host=config.db_host, port=config.db_port, user=config.db_user,
        password=config.db_password, db=config.db_name, charset=config.db_charset,
        autocommit=True, cursorclass=DictCursor,
    )


def _q1(sql, params=()):
    async def run():
        conn = await _conn()
        try:
            cur = await conn.cursor()
            await cur.execute(sql, params)
            return await cur.fetchone()
        finally:
            conn.close()

    return asyncio.run(run())


def _value_of(key: str):
    row = _q1("SELECT config_value FROM system_configs WHERE config_key=%s", (key,))
    return "" if row is None else (row["config_value"] or "")


def _save(client, headers, items):
    return client.put("/api/v1/settings/logistics", json={"items": items}, headers=headers)


def _restore(client, headers, key, original):
    """清理：把键恢复成用例开始前的值（不是一律清空，避免删掉本机真实配置）。"""
    _save(client, headers, {key: original})


def test_secret_is_masked_on_read(client, admin_headers):
    """写入真实值后，GET 只能拿到 MASK；非密钥项照常返回真实值。"""
    original = _value_of(SECRET_KEY)
    plain_original = _value_of(PLAIN_KEY)
    try:
        assert _save(client, admin_headers, {SECRET_KEY: "TEST_TRACK_KEY"}).json()["code"] == 0
        r = client.get("/api/v1/settings/logistics", headers=admin_headers)
        assert r.json()["code"] == 0
        items = r.json()["data"]["items"]
        assert items[SECRET_KEY] == MASK
        assert items[PLAIN_KEY] == plain_original
        assert _value_of(SECRET_KEY) == "TEST_TRACK_KEY"
    finally:
        _restore(client, admin_headers, SECRET_KEY, original)


def test_mask_echo_does_not_overwrite(client, admin_headers):
    """把回显的 MASK 原样提交，库里真实值必须保持不变。"""
    original = _value_of(SECRET_KEY)
    try:
        assert _save(client, admin_headers, {SECRET_KEY: "TEST_TRACK_KEY"}).json()["code"] == 0
        assert _save(client, admin_headers, {SECRET_KEY: MASK}).json()["code"] == 0
        assert _value_of(SECRET_KEY) == "TEST_TRACK_KEY"
    finally:
        _restore(client, admin_headers, SECRET_KEY, original)


def test_mask_rejected_for_unknown_key(client, admin_headers):
    """库里不存在的密钥键提交 MASK 必须被拒（错误码 2001，而不是权限/校验以外的原因）。"""
    probe = "logistics.probe_new_secret"
    r = _save(client, admin_headers, {probe: MASK})
    body = r.json()
    assert body["code"] == 2001, body
    assert "取值非法" in body["message"], body
    assert _q1("SELECT config_key FROM system_configs WHERE config_key=%s", (probe,)) is None
