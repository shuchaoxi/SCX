---
tags: [项目, SCX]
status: active
version: v0.4.0-pre
updated: 2026-06-27
---

# SCX 框架 · 项目面板

## 当前状态

| 指标 | 数值 |
|------|------|
| 版本 | **v0.4.0-pre**（theorems complete, all bugs fixed, verified） |
| Python 文件 | 37 (`src/scx/` 6 子包 + `yajie/` 模块) |
| 总源文件 | 115（含实验、测试、文档、配置） |
| Python 代码行 | ~17,200 |
| 总行数 | ~45,000 |
| 单元测试 | **427 tests**（10 文件, 全部通过） |
| 核心定理 | **3**：定理 1（噪声检测保证）+ 定理 2（弱特征失败下界）+ 定理 3（噪声不可辨识性），全部验证+bug修复 |
| 旧命题 | 6 个 → 重构完成：Props 1'+3' 在新定理框架下重建，其余归档 |
| 深水区理论 | 3 个方向探索 → v1 全部 reject → v2（收盘前）全部修复/转向：Minimax 下界 ✅ Resurrected（Hellinger）、聚类一致性 ✅ Rewritten（固定 K）、BBP 谱代理 ♻️ Pivoted（Bootstrap ARI 稳定性诊断）（见 [[../../07_任务/深水区理论]]） |
| Agent 分析文档 | 8 份 |
| **08_说明书/** | 7 文件（非专家定理解释），新增 |

## v0.4.0 功能清单

| 功能 | 模块 | 状态 |
|------|------|------|
| SCX 可靠性评估 | `expert/reliability.py` | ✅ |
| 数据四分类 | `valuation/classifier.py` | ✅ |
| 状态发现 | `state/discovery.py` | ✅ |
| 两层状态发现 | `state/two_layer.py` | ✅ |
| **StateValue（重构）** | `state/value.py` | ✅ **v0.4.0** 集成 theorem methods |
| 噪声检测 | `valuation/noise.py` | ✅ |
| 冗余检测 | `valuation/redundancy.py` | ✅ |
| 专家路由 | `expert/router.py` | ✅ |
| 状态条件影响力 | `valuation/influence.py` | ✅ |
| 在线 SCX | `core/online.py` | ✅ |
| 数据压缩 | `action/compress.py` | ✅ |
| 主动学习 | `action/acquisition.py` | ✅ |
| **SCX Forward + Spring Plan** | `yajie/` | ✅ **v0.4.0 新增** |

## 架构演进

| 版本 | 日期 | 关键变化 |
|------|------|---------|
| v0.1.0 | 06-25 | 初始 Python 包：30 files, 259 tests |
| v0.2.0 | 06-26 | 理论扩展：Compress Theorem + Governance Protocol |
| v0.3.0 | 06-26 | Influence + Online SCX + CIFAR/MedMNIST 实验 |
| v4.0 Plan | 06-26 | 通用模块化架构：抽象基类 + YAML 域配置 |
| v0.4.0-pre | 06-27 | **定理 1+2+3 完成**：噪声检测保证 + 弱特征失败下界 + 不可辨识性；StateValue 重构（V(s) deprecated）；Yajie 模块创建；427 tests；独立验证修复 5 bugs；08_说明书/ 7 文件；论文路线图 4→5；Arrow analogy 归档；**深水区理论两轮冲锋**：v1 三方向全部 reject → v2 全部修复/转向（Minimax 下界 ✅ Resurrected via Hellinger，聚类一致性 ✅ Rewritten 固定 K，BBP 谱代理 ♻️ Pivoted to Bootstrap ARI 稳定性诊断） |
| v0.4.0 | ⏳ 待发布 | code review complete, stable API freeze |

## v4+ 路线图

```
Phase A (2-4周) ✅ 已完成: 核心重构, 427 tests 通过, 3 定理完成
Phase B (2-3周) ⏳: 声明式配置 + CLI
Phase C (4-8周): 新领域扩展 (Robot/FEM/LLM)
Phase D (长期): 插件系统 + Benchmark + 社区
```

## 待办重点

- [x] 定理 1（噪声检测保证）完整证明 + Chernoff 收紧 ✅ 2026-06-27
- [x] 定理 2（弱特征失败下界）完整证明 + 3 issues 修复 ✅ 2026-06-27
- [x] 定理 3（噪声不可辨识性）完整证明 ✅ 2026-06-27
- [x] StateValue 重构（集成 theorem methods）✅ 2026-06-27
- [x] Yajie 模块创建 ✅ 2026-06-27
- [x] 独立验证 + 5 bugs 修复 ✅ 2026-06-27
- [x] 08_说明书/ 创建（7 文件）✅ 2026-06-27
- [x] Arrow analogy 归档移除 ✅ 2026-06-27
- [x] Proposition 1'+3' 重构 ✅ 2026-06-27
- [ ] 论文写作：Paper 2（EGP gauge fixing）立即推进，Paper 1 理论部分可开始草稿
- [ ] 代码评审：定理与实现的对齐检查（code review for theorem alignment）
- [ ] v4.0 Phase B: YAML 配置 + CLI (`scx run --config domains/mlip.yaml`)
- [ ] UCI Tabular 实验（CPU 可跑）
- [ ] 新领域接入示范（Robot/FEM/LLM）
- [ ] V(s) 已废弃 → 确认所有引用已替换为 StateValue
- [ ] 深水区理论：已延期至 Paper 1 投稿后（见 [[../../07_任务/深水区理论]]）

## 关键文件

- [README.md](../README.md)
- [SCX_架构清单.md](../CodexKnowledge/SCX_架构清单.md)
- [SCX_TODO_论文框架.md](../CodexKnowledge/SCX_TODO_论文框架.md)
- [SCX_通用模块化架构设计.md](../CodexKnowledge/SCX_通用模块化架构设计.md)

## 相关笔记

- [[../01_时间线/2026-06-25_v0.1.0发布|v0.1.0 发布记录]]
- [[../01_时间线/2026-06-26_v0.3.0_两层描述符|v0.3.0 更新记录]]
- [[../01_时间线/2026-06-27_定理证明与论文规划|v0.4.0-pre 定理完成日]]
- [[SCX-Health]] — 医学子项目
- [[EGP-MLIP]] — EGP 父项目
- [[../00_入口/论文谱系|论文谱系]]
- [[../../theory/theorems/README.md|核心定理目录]] — 定理 1+2+3 完整证明
