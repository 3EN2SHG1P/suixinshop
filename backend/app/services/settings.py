from core import audit, database
from core.errors import bad_request, duplicate, not_found, referenced

# 含以下片段的配置项视为密钥：读取时脱敏回显，保存时忽略脱敏占位，避免被明文带出或被覆盖
# 覆盖 system_configs 里全部凭据类键：payment.*_api_key / *_private_key、logistics.track_key、
# notify.sms_access_key_id / sms_access_key_secret、notify.smtp_auth_code 等
SECRET_HINTS = (
    "password",
    "passwd",
    "secret",
    "private_key",
    "api_key",
    "access_key",
    "auth_code",
    "track_key",
    "access_token",
    "refresh_token",
)
MASK = "******"
KEY_MAX_LEN = 100


def _is_secret(key: str) -> bool:
    k = key.lower()
    return any(h in k for h in SECRET_HINTS)


def _mask(key: str, value: str) -> str:
    if value and _is_secret(key):
        return MASK
    return value


async def get_configs(group: str) -> dict:
    rows = await database.fetch_all(
        "SELECT config_key,config_value,remark FROM system_configs WHERE config_group=%s ORDER BY id ASC",
        (group,),
    )
    return {
        "group": group,
        "items": {r["config_key"]: _mask(r["config_key"], r["config_value"] or "") for r in rows},
    }


async def save_configs(group: str, items: dict, user) -> None:
    if not items:
        bad_request("没有可保存的配置项")
    exist_rows = await database.fetch_all(
        "SELECT config_key,config_value FROM system_configs WHERE config_group=%s", (group,)
    )
    exist_map = {r["config_key"]: r["config_value"] for r in exist_rows}

    # 一阶段：全量校验 + 收集待写项。任何一条不合法都在写库前抛出，
    # 避免「前几条已提交、后面报错」的半成功状态（连接为 autocommit，逐条提交）。
    updates: list[tuple[str, str]] = []
    inserts: list[tuple[str, str]] = []
    for key, value in items.items():
        if not key.startswith(f"{group}."):
            bad_request(f"配置项 {key} 不属于 {group} 分组")
        if len(key) > KEY_MAX_LEN:
            bad_request(f"配置项名过长（上限 {KEY_MAX_LEN} 字符）：{key[:20]}…")
        value_str = str(value) if value is not None else ""
        if key in exist_map:
            if value_str == MASK and _is_secret(key):
                # 前端回传的是脱敏占位（用户没改该项），保持原值不变
                continue
            if (exist_map[key] or "") != value_str:
                updates.append((key, value_str))
        else:
            if value_str == MASK and _is_secret(key):
                bad_request(f"配置项 {key} 的取值非法")
            inserts.append((key, value_str))

    if not updates and not inserts:
        # 整组都是未改动的脱敏占位：不写库也不留审计噪声
        return

    # 二阶段：同一事务内写库，避免中途失败留下「改了一半」
    async with database.transaction() as cur:
        for key, value_str in updates:
            await cur.execute(
                "UPDATE system_configs SET config_value=%s WHERE config_key=%s",
                (value_str, key),
            )
        for key, value_str in inserts:
            await cur.execute(
                "INSERT INTO system_configs (config_key,config_value,config_group) VALUES (%s,%s,%s)",
                (key, value_str, group),
            )

    changed = [k for k, _ in updates] + [k for k, _ in inserts]
    summary = f"修改「{group}」分组配置：{','.join(changed)}"
    if len(summary) > 400:
        # params_summary 为 VARCHAR(500)，键名过多时只记总数，避免截断或写库失败
        summary = f"修改「{group}」分组配置：共 {len(changed)} 项"
    await audit.log_action(user.id, "settings", audit.ACTION_EDIT, f"settings/{group}", summary)


# ==================== 运费模板 ====================

FREIGHT_TYPE_TEXT = {1: "包邮", 2: "按重量", 3: "按件数"}


def _freight_item(r: dict) -> dict:
    return {
        "id": r["id"],
        "name": r["name"],
        "type": r["type"],
        "typeText": FREIGHT_TYPE_TEXT.get(r["type"], ""),
        "isFreeShipping": r["is_free_shipping"],
        "regionsJson": r["regions_json"] or "[]",
        "createdAt": r["created_at"],
    }


async def list_freight_templates() -> list[dict]:
    rows = await database.fetch_all("SELECT * FROM freight_templates ORDER BY id DESC")
    return [_freight_item(r) for r in rows]


async def save_freight_template(template_id: int | None, body, user) -> int:
    name = body.name.strip()
    if not name:
        bad_request("模板名称不能为空")
    if body.type == 1:
        body.is_free_shipping = 1
    if template_id:
        row = await database.fetch_one("SELECT id FROM freight_templates WHERE id=%s", (template_id,))
        if not row:
            not_found("运费模板不存在")
        await database.execute(
            "UPDATE freight_templates SET name=%s,type=%s,is_free_shipping=%s,regions_json=%s WHERE id=%s",
            (name, body.type, body.is_free_shipping, body.regions_json, template_id),
        )
        await audit.log_action(user.id, "settings", audit.ACTION_EDIT, f"freight:{template_id}", f"编辑运费模板「{name}」")
        return template_id
    tid = await database.execute_return_id(
        "INSERT INTO freight_templates (name,type,is_free_shipping,regions_json,created_by) "
        "VALUES (%s,%s,%s,%s,%s)",
        (name, body.type, body.is_free_shipping, body.regions_json, user.id),
    )
    await audit.log_action(user.id, "settings", audit.ACTION_ADD, f"freight:{tid}", f"新增运费模板「{name}」")
    return tid


async def delete_freight_template(template_id: int, user) -> None:
    row = await database.fetch_one("SELECT id,name FROM freight_templates WHERE id=%s", (template_id,))
    if not row:
        not_found("运费模板不存在")
    used = await database.fetch_one(
        "SELECT COUNT(*) AS c FROM goods WHERE freight_template_id=%s", (template_id,)
    )
    if used and used["c"]:
        referenced("已有商品使用该运费模板，不可删除")
    await database.execute("DELETE FROM freight_templates WHERE id=%s", (template_id,))
    await audit.log_action(user.id, "settings", audit.ACTION_DELETE, f"freight:{template_id}", f"删除运费模板「{row['name']}」")
