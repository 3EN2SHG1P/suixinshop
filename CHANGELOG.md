# 变更记录

面向使用者的版本变更。版本号与 `backend/pyproject.toml` 的 `version` 保持一致，格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

## [未发布]

### 新增

- `docs/README.md`：文档索引，说明每份文档写给谁、按目的该看哪一份
- `docs/openapi.json`：接口快照（136 条路径 / 186 个操作），无需启动后端即可查阅或导入 Postman / 客户端生成器
- `docs/api-reference.md` 新增「关系图（ER）」：1 张订单主干图 + 7 张分域图，字段取自 `seed/schema.py` 真实 DDL，并标注全部表为逻辑关联、DDL 中无 `FOREIGN KEY` 约束

### 变更

- 项目定位统一为**学习 / 演示 / 二次开发**：中英 README 首屏增加定位说明，声明段补充「可作为后台管理底座」与生产责任归属；`SECURITY.md` 定位改为「代码层按生产标准、外围依赖按演示标准」两层表述；`CONTRIBUTING.md` 增加维护状态（个人维护，响应时间不保证）
- `README` §7 开头由单句「不具备生产可用性」改为按「未接入 / 未常驻 / 未深挖」三类的边界说明，结论不变
- `SECURITY.md` 的「已实现的防护」扩为 15 条「已实现的安全措施」，每条标注真实代码位置（提权拦截、越权单条校验、批量整体拒绝、上传白名单、富文本净化、开放重定向拦截、配置密钥脱敏、售后超额校验、库存乐观锁、取消订单幂等）
- `docs/功能清单.md` 后台表格增加「状态」列（● 完整 / ◐ 部分 / ○ 仅 CRUD），依据是测试实测：`routers/content.py`、`routers/marketing.py`、`routers/admin_logs.py` 在测试中零命中
- 文档一致性修正：中英 README 架构图的接口数 `185` 校正为 `186`（与 `/api/docs` 实际 186 个操作一致）；`CONTRIBUTING.md`（2 处）、PR 模板、`开发指南.md` 共 4 处「不低于 88 passed」改为「全部通过」（实际用例已增至 99 个，固定数字会让「有失败但总数够」蒙混过关）；`backend/.env.example` 中 `STATIC_FRONT_DIR` 的注释由「已停用」更正为「后端不挂载 `/front`，但 `/api/v1/shop/live/version` 仍扫描该目录生成资源指纹」
- `manager/README.md` 删除与 `docs/功能清单.md` 重复的 28 页清单表，改为指向功能清单（页面信息只维护一处）；`docs/README.md` 索引补登 `manager/README.md`
- 品牌 Logo 更换为作者独立设计的最终版（青绿版）：`front/images/`、`manager/images/` 下的 `logo.png`（1024×1024）与 `logo-transparent.png`（256×256，favicon）全部替换，前台 18 页头部/页脚/登录横幅、后台登录页与侧栏、`seed` 站点 Logo 默认值同步生效；`docs/screenshots/` 8 张截图内嵌 Logo 同步更新；PNG 内嵌 `Title/Author/Copyright` 元数据
- 新增 `NOTICE`：Logo 为作者原创美术作品，已提交著作权登记申请，明确排除于 MIT 许可之外；分列允许范围（随源码再分发、部署展示、界面适配缩放、文章/课程/评测引用、衍生版本沿用）与禁止范围（他项目标识、商标商号、改动图形、单独分发），并声明许可不可撤回、按现状提供；`LICENSE` 追加说明段，中英 README 声明同步修正
- 中英 README 顶部加居中 Logo 与版权署名行；全站 78 处 Logo 引用统一加 `?v=2` 版本参数，避免浏览器 favicon 缓存长期显示旧图；新增 `tests/test_brand_assets.py`（11 条）守住四处副本一致、alpha 通道、版权元数据、全站引用、缓存参数与 README/NOTICE 声明

### 修复

- 前台未登录点「我的订单」（及购物车结算、地址、支付、优惠券、积分、售后等 10 个需登录页）原地不动或白屏：`front/js/guard.js` 去掉了会掐掉跳转的 `window.stop()`，改为先隐藏再 `location.replace` 到 `login.html?redirect=<原页>`，并加 600ms 兜底重试与 `pageshow` 可见性恢复；隐藏方式由 `display:none` 改为 `visibility`，避免 bfcache 后退回来是空白页。登录成功后按 `redirect` 回跳原页的逻辑不变（`auth.js gotoAfterLogin`）

## [0.1.0] - 2026-10-30

首个公开版本。

### 新增

- 后台管理：26 个功能页 + 登录 + 仪表盘，9 个一级菜单（仪表盘 / 商品 / 订单 / 会员 / 营销 / 内容 / 设置 / 权限 / 日志），全部接真实接口
- 商城前台：18 个页面，覆盖「首页 → 搜索 → 详情 → 购物车 → 结算 → 支付 → 我的订单」完整闭环；游客购物车登录后自动合并
- 后端：`FastAPI + MySQL` 全异步（`aiomysql` 连接池），无 ORM、全部手写参数化 SQL；186 个接口（后台 133 + 前台 52 + 健康检查 1）、46 张表
- RBAC 四级权限（菜单 / 按钮 / 接口 / 数据），`data_scope` 支持仅本人 / 本部门及子部门 / 全部
- `seed/` 幂等初始化：`base`（建库建表 + 权限树 + 管理员）与 `demo`（34 商品 / 31 分类 / 18 订单 / 6 会员）可分别清理；`seed base` 自动建库，克隆后无需手工 `CREATE DATABASE`
- 金额统一 `core/money.py`（`Decimal` + `ROUND_HALF_UP` 量化到分）；时间统一东八区字面量
- `docker-compose.yml`：一条命令起 MySQL 8，端口默认只绑回环地址，口令走变量注入
- 文档：中英双版 README、功能清单、操作手册、开发指南、接口与表结构手册、需求归档；CI（MySQL 8 service + `uv sync --frozen` + 全量 pytest）
- `.editorconfig`、`.gitattributes`（统一 LF、声明二进制）

### 安全

- 角色与权限资源的写操作仅限超管，普通管理员提交的 `role_ids` 被丢弃，`RoleSave.data_scope` 默认值收敛为 1；回归用例 `tests/test_privilege_escalation.py` 覆盖四条提权链路
- 注册验证码：CSPRNG 随机生成 + BCrypt 落库 + 5 分钟过期 + 5 次错误上限，未请求过验证码的注册一律拒绝
- `SMS_MOCK` 代码默认 `false`（`.env.example` 为便于本地演示置 `true`，README / SECURITY 均已标注「开启即公开注册后门」）
- 后台与会员令牌用 `typ` 区分，互不通用；密码 BCrypt 存储，入参上限 72 字节（避免静默截断）
- `GET /permission/admins/{id}` 与商品详情 / 编辑 / 删除 / 批量 / 审核按 `data_scope` 做行级过滤，批量操作对越权 id 整体拒绝
- 商品列表排序方向白名单化；系统配置中的密钥类字段读取脱敏，回传占位符不覆盖真实值
- 上传按扩展名白名单（不含 `svg`，避免存储型 XSS）+ `Content-Type` 校验，文件名 UUID 化，大小上限可配
- 前台富文本经 `sanitizeHtml()` 净化；登录回跳 `?redirect=` 与地址表单 `from` 参数全串锚定 + 字符白名单（修 XSS / 开放重定向）
- `.env.example` 的 `ADMIN_INIT_PASSWORD` 留空，`seed base` 随机生成并打印，仓库内不含可用弱密码

### 修复

- 编辑商品改为 `original_stock` 乐观锁校验，不再用表单快照覆盖并发期间的销量
- 取消订单、优惠券核销改为校验更新行数，并发下不会重复回补库存 / 重复用券
- 积分抵扣与取消返还改用条件更新并检查结果，避免「钱扣了账没记」
- 售后金额按「实付 − 已退与进行中合计」校验，杜绝多次申请超额退款
- 折扣券与售后容差改用量化后的精确比较；`seckill_price` 为 NULL 时不再抛异常
- 批量删除商品中途失败不再「删一半」；后台菜单缺权限前缀时 fail-closed 隐藏
- 演示数据日期改为随种子时刻整体平移：订单、广告、秒杀、拼团、文章、公告、操作日志按「今天 − 数据内最新订单日」的天数平移，项目放置较久后再 clone 也不会出现「仪表盘近 7/30 日全 0、热销榜空、广告全过期」
- 演示广告的跳转链接由小程序式路径改为前台真实页面，后台广告表单的提示同步订正
- 环境变量写成非数字 / 非布尔时明确指出变量名；MySQL < 5.7、连不上、建库无权限时给出可照做的报错
- `.env` 支持 Windows 记事本写入的 UTF-8 BOM，避免配置静默失效

### 清理

- 商品型号与图片文件名改为虚构编号，前端全局变量去掉品牌前缀
- 前台移除真实企业客服号、虚构业务入口与无实现依据的服务承诺，改为示例说明
- 依赖精简：移除三个零引用包（`openpyxl`、`pydantic-settings`、`cryptography`）；`uv.lock` 锁定官方 PyPI

### 已知限制

不具备生产可用性，不做可用性承诺：支付与短信均为模拟、运费模板不参与结算、营销活动未接入结算引擎、`data_scope` 只覆盖商品与管理员、`previewToken` 存进程内存、pytest 依赖真实 MySQL。完整清单见 [README.md 的「已知限制」](./README.md#7-已知限制)。
