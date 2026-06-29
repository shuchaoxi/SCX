---
tags: [决策, IP, 策略]
created: 2026-06-27
---

# IP 保护与开源策略

> 综合来源：GPT 对话 + [IP_NOTE.md](../../IP_NOTE.md) + [CLEAN_ROOM_CHECK.md](../../CLEAN_ROOM_CHECK.md) + [整理_IP保护与开源策略与商业模式.md](../../CodexKnowledge/整理_IP保护与开源策略与商业模式.md)

## 5 层资产分类

| 层级 | 内容 | 策略 |
|------|------|------|
| 数学理论 | SCX 定义、命题、证明 | **发表** — arXiv + 期刊 |
| 算法框架 | pseudocode、核心流程、基本公式 | **发表** — 论文核心 |
| 最小代码 | toy demo、基础 SCX score、简单 coreset | **开源** — GitHub |
| 工程实现 | 高性能 pipeline、自动诊断、可视化、工业接口 | **暂不全开源** — 闭源商业 |
| 数据/模型/专家库 | benchmarks、专家势函数库、校准参数 | **核心商业资产** — 闭源 |

## 操作顺序

```
Step 1: 内部 IP 记录（本仓库的 IP_NOTE.md + DEVELOPMENT_LOG.md + CLEAN_ROOM_CHECK.md）
Step 2: 专利评估（如适用）
Step 3: arXiv 预印本（SCX-Theory）
Step 4: 选择性开源（最小代码，open core 模式）
Step 5: 商业授权（工程实现、数据、专家库）
```

## Clean Room 认证

SCX 的核心贡献全部在个人时间和个人设备上完成（见 [CLEAN_ROOM_CHECK.md](../../CLEAN_ROOM_CHECK.md)）：
- 30 源文件零学校引用
- 所有理论工作、代码生成、实验验证均在个人电脑
- 不依赖学校超算资源、软件许可、研究经费

## 论文署名

| 贡献 | 角色 | 比例 |
|------|------|------|
| 数学框架（定义、命题、证明） | 用户 | 100% |
| 架构设计 | 用户 | 100% |
| 代码实现 | AI (Claude Code) 按用户指导生成 | — |
| 实验设计和执行 | 用户 | 100% |

> AI 工具不享有署名权（根据 COPE, Nature, arXiv 等学术出版规范）。

## 相关笔记

- [[决策日志]] — 决策 7 的详细展开
- [[论文策略]] — 发表顺序与策略
- [[论文谱系|论文谱系]]
