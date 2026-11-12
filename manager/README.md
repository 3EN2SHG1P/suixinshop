# 商城后台管理系统 - 静态页面

商城后台管理系统的完整静态页面集合（28 页，含登录页与仪表盘）。

### 快速开始

直接用浏览器打开 `login.html` 可预览静态样式（无需构建工具；但登录联调必须先启动后端，见下文联调提示。联调时由后端统一托管：启动 `backend` 后访问 `http://127.0.0.1:8001`，根路径自动跳转到本登录页）。

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>登录页：`login.html`（演示账号 `admin`，初始密码由 `seed base` 生成并打印；可在 `.env` 用 `ADMIN_INIT_PASSWORD` 指定，重跑 `seed base` 会按该值同步。登录成功写入本地会话）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>仪表盘：`dashboard.html`（登录后默认跳转页）

登录/退出逻辑：

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>登录成功后以当前账号为准渲染顶栏用户信息（姓名/角色/账号），未登录直接访问子页面会跳回登录页。

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>顶栏右侧用户区为下拉菜单，可执行「退出登录」清除会话并返回登录页。

### 技术栈

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**HTML5**：语义化结构

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**CSS3**：完全独立样式文件，CSS变量主题系统

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**原生 JavaScript (ES6+)**：无框架依赖，模块化公共组件

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**响应式布局**：适配桌面端、平板、移动端

### 目录结构

```
manager/
├── login.html                  # 登录页
├── dashboard.html              # 仪表盘（首页）
├── css/
│   ├── common.css              # 全局公共样式（布局/组件/主题）
│   └── login.css               # 登录页专属样式
├── js/
│   ├── common.js               # 公共JS（侧边栏/模态框/抽屉/表格/分页/Toast）
│   └── guard.js                # 登录态守卫（未登录跳登录页）
├── images/                     # 站点 logo（logo.png / logo-transparent.png，版权归作者，授权范围见根目录 NOTICE）
└── pages/
    ├── goods/                  # 商品管理
    │   ├── goods-list.html     # 商品列表
    │   ├── goods-category.html # 商品分类（无限级树）
    │   ├── goods-brand.html    # 品牌管理
    │   ├── goods-spec-attr.html# 规格属性
    │   └── goods-comment.html  # 评论管理
    ├── order/                  # 订单管理
    │   ├── order-list.html     # 订单列表（含详情抽屉/发货/改价）
    │   ├── after-sale.html     # 售后管理
    │   └── logistics.html      # 物流公司
    ├── member/                 # 用户管理
    │   ├── member-list.html    # 会员列表（含详情抽屉）
    │   ├── member-level.html   # 会员等级
    │   └── points.html         # 积分管理
    ├── marketing/              # 营销管理
    │   ├── coupon.html         # 优惠券
    │   ├── seckill.html        # 秒杀活动
    │   ├── full-discount.html  # 满减满折
    │   ├── group-buy.html      # 拼团活动
    │   └── distributor.html    # 分销管理
    ├── content/                # 内容管理
    │   ├── article.html        # 文章管理
    │   ├── ad.html             # 广告管理
    │   └── notice.html         # 公告通知
    ├── settings/               # 系统设置
    │   └── settings.html       # 配置中心（基本/支付/物流/通知/运费 5 个 Tab）
    ├── permission/             # 权限管理
    │   ├── admin.html          # 管理员管理
    │   ├── role.html           # 角色管理（含权限树分配）
    │   ├── resource.html       # 权限资源
    │   ├── dept.html           # 部门管理
    │   └── login-log.html      # 登录日志
    └── logs/
        └── operation-log.html  # 操作日志
```

> 每个页面能干什么、完成度如何，统一见 [docs/功能清单.md](../docs/功能清单.md)（单一事实来源，本文件不再重复罗列）。

### 设计规范

#### 视觉风格

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**主色调**：青绿色 `#1E9E96`（与前台 `front/` 主色一致）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**侧边栏**：白色 `#ffffff`，hover `#EFF9F8`，激活态主色高亮

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**内容区**：浅灰背景 `#f1f5f9`，白色卡片

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**圆角**：统一 6-14px 分级圆角

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**阴影**：轻柔卡片阴影，hover 微浮起

#### 组件库（CSS/JS 内置）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>侧边栏导航（可折叠、多级菜单、当前页高亮）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>顶部栏（面包屑、搜索、通知、用户信息）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>统计卡片（6种配色图标、趋势指示）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>数据表格（全选、批量操作栏、分页）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>筛选栏（多条件组合搜索）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>模态框（标准/大/超大三种尺寸）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>侧边抽屉（订单详情、会员详情、售后审核）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>标签页切换

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>树形结构（分类、部门、权限树）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>Toast 提示

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>开关、徽章、进度条、时间线

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>纯CSS柱状图（仪表盘趋势图）

#### 交互功能

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>侧边栏菜单展开/收起、折叠

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>全选/反选、批量操作计数

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>模态框打开/关闭（遮罩点击关闭）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>抽屉滑入/滑出

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>标签页切换

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>树形节点展开/收起

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>分页控件（页码跳转、每页条数）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>Toast 消息提示

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>确认操作对话框

### 页面与权限码对应

全部页面按「页面 - 路由 - 权限码」一一对应组织，覆盖以下模块：

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>✅ RBAC 四层权限（菜单/按钮/接口/数据）UI 对照

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>✅ 仪表盘指标口径（今日订单/GMV/新增用户/待付款/待发货/库存预警）；转化率与商品浏览量当前仪表盘未实现

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>✅ 商品整单提交结构（基本信息+SKU+图片+SEO；运费模板字段当前固定提交 `null`，未接入模板选择）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>✅ 订单状态机（待付款→待发货→已发货→已完成）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>✅ 售后审核流程（仅退款/退货退款）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>✅ 会员等级体系与积分流水

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>✅ 营销叠加规则的 UI 表达（优惠券+满减可叠加、秒杀/拼团不可叠加由前端下拉与提示体现；**活动叠加 `is_stackable` 未接入结算引擎**，实际结算只走优惠券与积分）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>✅ 系统设置（基本/支付/物流/通知/运费模板）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>✅ 操作日志七类（登录/新增/修改/删除/导出/审核/退出）

> 联调提示：`login.html` 直接双击打开无法登录，必须先启动后端（8001）提供 `/api/v1/auth/login`。

### 数据说明

全部 28 个页面（26 个功能页 + 登录页 + 仪表盘）均已接入真实后端接口（增删改查/筛选/导出均真实落库），接口契约见 `/api/docs`。

自动化回归未覆盖 `marketing` / `content` / `admin_logs` 三个模块（`settings` 只有密钥脱敏回归），这部分的正确性目前依赖人工验证。

登录会话存于 `localStorage`（key 见 `js/common.js`），顶栏用户信息取自会话，不在页面中写死。注意这意味着任何 XSS 都可能窃取令牌 —— 本项目把它列为已知边界，生产应改用 httpOnly Cookie。

列表回填编辑表单统一走 `AdminUI.findRow()`：列表请求返回时按接口缓存行数据，「编辑」优先从缓存取，取不到才退化查询，避免记录数超过单页后在列表里「点编辑没反应」。

### 浏览器兼容性

支持 Chrome、Edge、Firefox、Safari 等现代浏览器的最新两个大版本。
