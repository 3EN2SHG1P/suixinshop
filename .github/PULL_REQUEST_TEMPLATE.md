## 改动内容

<!-- 一句话说明这个 PR 做了什么、为什么这么做 -->

## 自查（与 CONTRIBUTING.md 的 PR 检查清单一致）

- [ ] `uv run pytest -q tests` 全部通过（不设固定数字，用例会随功能增长）
- [ ] 新增 / 变更的接口已同步 README 与 `seed/base.py` 权限树（若涉及权限码）
- [ ] 新增表已进 `seed/schema.py`，且 seed 幂等（重跑不翻倍、不报错）
- [ ] 前端新增页面已同步菜单（`manager/js/common.js` 的 `menuData` 与 `MENU_PERM`）
- [ ] 未引入真实品牌、真实个人信息、第三方版权素材
- [ ] README 与 `docs/`（功能清单 / 操作手册 / 接口手册）的口径已同步
- [ ] 面向使用者的行为变化已写进 `CHANGELOG.md` 的「未发布」小节
- [ ] 改了界面（HTML / CSS / 交互）时，同步更新 `docs/screenshots/` 里受影响的截图
