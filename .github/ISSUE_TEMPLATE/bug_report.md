---
name: 缺陷报告
about: 跑不起来、行为与文档不符、接口报错
title: "[bug] "
labels: bug
---

## 现象

<!-- 一两句话说清发生了什么 -->

## 复现步骤

1.
2.
3.

## 期望结果 / 实际结果

## 环境

| 项 | 值 |
|---|---|
| 操作系统 | |
| Python 版本（`python -V`） | |
| 依赖安装方式 | `uv sync` / `pip install -r requirements.txt` |
| 数据库 | Docker（`docker compose up -d`）/ 本机 MySQL（版本：） |
| 执行过的 seed 命令 | `base` / `demo` / 都没跑 |
| 访问的端 | 后台 8001 / 前台 8000 |

## 报错原文

```
粘贴完整报错（含 traceback）
```

## 配置（务必脱敏）

```
DB_HOST=...        # 不要贴密码与真实域名
SMS_MOCK=...
CORS_ORIGINS=...
```

> 安全问题请勿在此提交，按 [SECURITY.md](../../SECURITY.md) 的渠道私下上报。
