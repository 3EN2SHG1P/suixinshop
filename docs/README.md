# 文档索引

本目录是项目文档的入口。每份文档写给谁、讲什么，见下表；不确定该看哪份，直接跳到 §2 按目的找。

### 1. 有哪些文档

| 文件 | 写给谁 | 里面是什么 |
|---|---|---|
| [README.md（根目录）](../README.md) | 第一次来的人 | 项目定位、5 分钟跑起来、排错表、已知限制 |
| [README.en.md（根目录）](../README.en.md) | 非中文读者 | 上者的英文版，结构对称 |
| [功能清单.md](./功能清单.md) | 评估「能不能用」的人 | 每个页面能干什么 + 完成度标记（●/◐/○） |
| [操作手册.md](./操作手册.md) | 已跑起来的人 | 按「我要做一件事」组织的日常操作 |
| [开发指南.md](./开发指南.md) | 二次开发者 | 三层架构、加接口/加表/加页面的步骤、坑位清单 |
| [api-reference.md](./api-reference.md) | 查细节的人 | 环境变量、186 个接口、46 张表与 ER 图 |
| [openapi.json](./openapi.json) | 工具链 | 接口快照（136 条路径 / 186 个操作），可直接导入 Postman 或生成客户端 |
| [需求规划.md](./需求规划.md) | 二次开发者 | 早期需求原文与规划项，供取舍参考，**不是已实现清单** |
| [manager/README.md](../manager/README.md) | 改后台前端的人 | 后台目录结构、设计规范、内置组件库、已知边界 |
| [screenshots/](./screenshots) | README 引用 | 前台 4 张 + 后台 4 张，改界面时同步更新 |
| [CHANGELOG.md（根目录）](../CHANGELOG.md) | 使用者 | 版本变更 |
| [SECURITY.md（根目录）](../SECURITY.md) | 部署与审计的人 | 已实现的安全措施、部署前必改配置、已知不安全项 |
| [CONTRIBUTING.md（根目录）](../CONTRIBUTING.md) | 贡献者 | 维护状态、提交规范、PR 检查清单 |
| [NOTICE（根目录）](../NOTICE) | 用到 Logo 的人 | Logo 的独立授权条款（不在 MIT 范围内） |

`docs/` 下所有中文文档都以 `README.md` 与 `/api/docs` 的实际接口为准；`需求规划.md` 是唯一一份「描述意图而非现状」的文档。

### 2. 按目的找

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**想评估值不值得用** → [功能清单.md](./功能清单.md) 的完成度列 + [../README.md](../README.md) §7 已知限制

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**想跑起来** → [../README.md](../README.md) §2

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**想改代码** → [开发指南.md](./开发指南.md) → [api-reference.md](./api-reference.md)

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**想查表关系** → [api-reference.md](./api-reference.md) 的「关系图（ER）」

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**想上线** → [../SECURITY.md](../SECURITY.md) 的「部署前必须修改的配置」

<span>&nbsp;•&nbsp;&nbsp;&nbsp;</span>**想提 PR** → [../CONTRIBUTING.md](../CONTRIBUTING.md)
