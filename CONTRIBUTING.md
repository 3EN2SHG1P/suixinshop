# 贡献指南

感谢你想改进这个项目。该项目定位是**学习 / 演示 / 二次开发**，请据此把握改动的尺度。

**维护状态**：个人维护项目，响应时间不保证。文档、错别字、明确的缺陷修复这类小改动欢迎直接提 PR；较大改动请先开 Issue 说明方向，避免白做。

### 1. 先跑起来

```bash
cd backend
uv sync                               # 依赖由 uv 管理（pyproject.toml + uv.lock）
copy .env.example .env                # Windows CMD；PowerShell 与 macOS/Linux 用 cp
uv run python -m seed.runner base     # 自动建库 + 建表 + 管理员
uv run python -m seed.runner demo     # 演示数据
uv run python run.py                  # 8001
cd ../front && python -m http.server 8000
```

测试前置：MySQL 可达且已执行 `base` + `demo`；`uv run pytest -q tests` 需**全部通过**（用例数随功能增长，不设固定数字，以免把「有失败但总数够」误判为通过）。

### 2. 改代码前

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**需求与实现冲突时以 `README.md` 与 `/api/docs` 的接口说明为准；改行为同步更新 README 对应章节与接口文档。**

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>二次开发的架构约定、目录约定与坑位清单见 **[docs/开发指南.md](./docs/开发指南.md)**，动代码前请先读它的「不能踩的坑」。

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>文档口径（端口、命令、账号、页面数）要与 `README.md` / `README.en.md` / `docs/` 下的手册保持一致。

### 3. 提交规范

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>分支：`feat/xxx`、`fix/xxx`、`docs/xxx`

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>commit 前缀：`feat:` `fix:` `docs:` `refactor:` `test:` `chore:`

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>一个 PR 只做一件事，描述里写清「改了什么 / 为什么 / 怎么验证」

### 4. PR 检查清单

- [ ] `uv run pytest -q tests` 全部通过（不设固定数字，用例会随功能增长）
- [ ] 新增/变更的接口已同步 README 与 `seed/base.py` 权限树（若涉及权限码）
- [ ] 新增表已进 `seed/schema.py`，且 seed 幂等（重跑不翻倍、不报错）
- [ ] 前端新增页面已同步菜单（`manager/js/common.js` 的 `menuData` 与 `MENU_PERM`）
- [ ] 未引入真实品牌、真实个人信息、第三方版权素材
- [ ] README 与 `docs/`（索引 / 功能清单 / 操作手册 / 接口手册）的口径已同步；新增文档已在 `docs/README.md` 登记
- [ ] 面向使用者的行为变化已写进 [CHANGELOG.md](./CHANGELOG.md) 的「未发布」小节
- [ ] 改了界面（HTML / CSS / 交互）时，同步更新 `docs/screenshots/` 里受影响的截图

### 5. 不接受的改动

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>引入 GPL/AGPL 等强传染性依赖

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>引入需要联网、需要商业授权的资源（字体、图片、SDK）

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>提交 `.env`、真实密码、密钥、个人信息

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>把演示项目改造成生产级系统的大规模重写（欢迎开 issue 讨论，但请单独分支）

### 6. 报告问题

请附上：复现步骤、期望与实际结果、`.env` 相关配置（**脱敏**）、`seed` 执行过的命令、报错原文。

**安全问题请勿开公开 Issue**：请按 [SECURITY.md](./SECURITY.md) 的渠道私下上报。
