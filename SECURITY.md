# 安全说明

### 定位

本项目以学习、演示与二次开发为目的，安全实现分两层：**框架与业务层的校验按生产标准实现**（清单见本文「已实现的安全措施」），**外围依赖与运维环节按演示标准实现**（支付网关、短信服务商、限流、监控、静态托管鉴权）。

因此默认配置只适合本机跑通，**请勿直接对外部署**；二次开发上线前，需先完成「部署前必须修改的配置」，再自行补齐外围环节。

### 部署前必须修改的配置

| 配置 | 位置 | 说明 |
|---|---|---|
| `JWT_SECRET` | `backend/.env` | 后台令牌签名密钥，留空则服务无法启动；**每个环境必须独立生成** |
| `MEMBER_JWT_SECRET` | `backend/.env` | 会员令牌密钥，留空会回退到 `JWT_SECRET` |
| `DB_PASSWORD` | `backend/.env` | 数据库密码；`docker-compose.yml` 的默认值 `DEV_ONLY_123456` 仅限本机 |
| `DB_BIND_HOST` | 项目根 `.env`（仅 `docker compose` 读取） | 默认 `127.0.0.1`（只有本机可连）。改成 `0.0.0.0` 或某块网卡地址后数据库即对局域网开放，必须同时换掉默认口令并用防火墙限制来源 |
| 管理员密码 | 后台「权限管理 → 管理员」 | `seed base` 生成的管理员密码必须立即修改 |
| `SMS_MOCK` | `backend/.env` | **必须设为 `false`**。设为 `true` 时注册验证码通过 `devCode` 直接回显，等于公开注册后门 |
| `CORS_ORIGINS` | `backend/.env` | 收敛为实际前台域名，**禁止 `*`** |

### 已知的默认不安全项

1. **`/manager` 与 `/uploads` 无鉴权**：由后端直接静态托管，生产应由 Nginx 接管并加访问控制。
2. **支付为模拟流程**：`POST /api/v1/shop/pay/{order_key}` 不接真实网关，会员可自助把订单置为已支付。
3. **演示数据含固定密码**：`seed demo` 生成的会员账号密码统一为 `123456`，仅限本地演示库。
4. **`/api/docs` 与 `/api/openapi.json` 默认公开**：对外部署前应关闭或加访问控制。
5. **无全局限流**：除登录失败锁定（`LOGIN_FAIL_LIMIT`）、验证码同号 60 秒间隔（`SMS_INTERVAL_SECONDS`）与商品浏览量同 IP 10 秒频控外，接口层未做统一的速率限制。

### 已实现的安全措施

下表每一条都能对应到具体代码位置，便于二次开发时判断「哪些不用重做」。其中提权与配置脱敏两处有专门的回归用例。

| 类别 | 风险 | 做法 | 位置 |
|---|---|---|---|
| 授权 | 提权：改资料时顺手给自己挂超管角色 | 普通管理员提交的 `role_ids` 一律丢弃（而非 403，避免连改自己手机号都被拒）；角色与权限资源的写操作仅限 `data_scope=3` | `services/permission.py` `strip_role_ids()`、`tests/test_privilege_escalation.py`（10 例） |
| 授权 | 越权：列表看不见却能改 | 数据权限下沉到单条读写，详情 / 编辑 / 删除 / 审核均校验 `created_by` 归属 | `services/goods.py` 单条 scope 校验 |
| 授权 | 越权：批量操作「部分成功」 | 批量先整体校验 id 归属，任一越权即整体拒绝；删除先校验后执行，不会删一半 | `services/goods.py` 批量入口 |
| 认证 | 后台与会员令牌混用 | 两类令牌用 `typ` 区分，互不通用 | `core/deps.py` |
| 认证 | 密码明文存储 | BCrypt 哈希；入参上限 72 字节，避免 BCrypt 静默截断 | `services/auth.py` |
| 认证 | 登录爆破 | 连续失败计数 + 锁定，后台与会员同口径，阈值可配置 | `LOGIN_FAIL_LIMIT` / `LOGIN_FAIL_LOCK_MINUTES` |
| 认证 | 注册环节自助后门 | 验证码 CSPRNG 生成、BCrypt 落库、5 分钟过期、错 5 次作废；**配置中不存在固定验证码开关** | `core/config.py`、`services/shop_auth.py` |
| 注入 | 存储型 XSS（上传） | 扩展名白名单 `_ALLOWED_EXTS`（**不含 `svg`**）+ `Content-Type` 比对 + 文件名 UUID 化 + 大小上限 | `routers/upload.py` |
| 注入 | 存储型 XSS（富文本） | 商品详情等富文本渲染前经 `sanitizeHtml()` 净化 | `front/js/page-detail.js`（`S.sanitizeHtml`） |
| 注入 | 开放重定向 / 伪协议 | 登录回跳 `?redirect=` 只接受站内路径，拦截 `javascript:` 等伪协议 | `front/js/auth.js` |
| 注入 | SQL 注入 | 全部参数化查询；无法参数化的排序字段走方向白名单 | `core/database.py` 及各 service |
| 泄露 | 配置页回显密钥 | 密钥类字段（命中 `password` / `passwd` / `secret` / `private_key` / `api_key` / `access_key` / `auth_code` / `track_key` / `access_token` / `refresh_token`）读取脱敏为 `******`；保存时忽略占位符，避免整组回传把真实值覆盖 | `services/settings.py` `_mask()` / `_is_secret()` |
| 业务 | 售后退款超额 | 可退上限 = 实付 − 已通过 / 进行中退款合计，超出直接拒绝 | `services/shop_after_sale.py` |
| 业务 | 库存超卖 | SKU 单语句条件扣减 `UPDATE ... WHERE stock >= N`，配合 `version` 递增 | `services/shop_order.py` |
| 业务 | 取消订单重复回补 | 校验更新行数，同一订单重复取消不会重复返还库存 / 优惠券 / 积分 | `services/shop_order.py` |

以上均为**代码层**防护。外围依赖（支付网关验签与对账、短信通道、统一限流、WAF、日志集中审计）不在其中，见下一节。

### 报告漏洞

请**不要**通过公开 Issue 报告安全问题。请使用 GitHub 的 [Private vulnerability reporting](https://docs.github.com/zh/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability) 功能，或直接联系仓库维护者。请附：复现步骤、影响范围、建议修复方向。
