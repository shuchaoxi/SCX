---
tags: [项目, EGP, MLIP]
status: active
---

# EGP-MLIP · 项目面板

## 概述

EGP（Error-Guided Partitioned MLIP）是 SCX 的"父项目"。核心目标：通过 error landscape 分析 + 多专家拆分 + gauge-normalized merging 构建氮化物半导体（AlN/GaN/AlGaN/InN）的高精度机器学习势函数。

## 当前状态

| 指标 | 数值 |
|------|------|
| 阶段 | AlN ModelB v3 已训练；Paper 2 起草中 |
| 数据 | AlN v3 DFT（孝感超算生成） |
| GaN/AlGaN DFT | 待生成 |
| 论文 | **Paper 2 (EGP Gauge Fixing): 1-2 周投稿** — 当前焦点 |
| 理论 | Paper 1 定理 1+2 已完成（SCX 框架），不影响 Paper 2 |
| 代码位置 | `G:\Xiaogan_Supercomputing_data\egp\` |

## 项目架构

```
egp/
├── ace_expert_algebra/    # ACE 专家代数框架
│   ├── src/experts/       # Expert 实现
│   ├── src/gauge/         # Gauge fixing
│   └── src/export/        # 模型导出
├── VASP/                   # DFT 计算
│   ├── AlN_v4_targeted/   # AlN 靶向结构
│   ├── AlGaN_v2_error_guided/  # AlGaN 误差引导
│   ├── GaN_structures_v1/ # GaN 结构
│   ├── submission_sets/   # 提交集管理
│   └── training_workspaces/    # 训练工作区
├── CodexKnowledge/        # EGP 项目知识库
│   └── agent_outputs/     # 论文实验重设计
├── papers/                # 论文与参考文献
└── images/                # 概念图与执行难点
```

## 核心概念（已迁移到 SCX）

以下概念起源于 EGP，但已被泛化为 SCX 中的通用概念：

| EGP 概念 | SCX 对应 |
|----------|---------|
| Error Landscape | [[../02_概念/State-Conditioned eXpertise\|SCX 可靠性评估]] |
| Two-Layer EGP | [[../02_概念/两层描述符\|两层描述符]] |
| Gauge-Normalized ACE | [[../02_概念/Gauge-Normalized Residual\|Gauge-Normalized Residual]] |
| Element-Guided Expert | [[../02_概念/Element-Guided ACE\|Element-Guided ACE]] |
| Router + Expert Mixing | [[../02_概念/专家路由\|专家路由]] |

## 超算资源

| 项目 | 值 |
|------|-----|
| 超算 | 孝感超算 (cxshu) |
| SSH | `ssh -p 24678 cxshu@219.139.78.251` |
| 本地盘符 | `W:` → `/home/cxshu` |
| CPU | 240 cores (Intel Xeon Platinum 8582C) |
| 调度器 | 无（tmux + mpirun 模式） |

## 下一步

### 🔴 立即行动：Paper 2 (EGP Gauge Fixing)

- [x] 定理 1+2 完成（SCX 框架，不影响 Paper 2）✅ 2026-06-27
- [ ] **P2.1 止损收窄** — 移除 SCX Figs + 理论提及，收窄 claims
- [ ] **P2.2 Results + Discussion 写作** — 3.1-3.5 + 讨论
- [ ] **P2.3 图表整理** — 最终版 Fig 1-4 + fair comparison 表
- [ ] **P2.4 投稿** — Cover Letter → arXiv → npj Comput. Mater.

### 🟡 并行准备（等 GPU）

- [ ] Paper 1 实验重设计（见 agent_outputs 中的 M1-M6 方案）
- [ ] GaN/AlGaN DFT 数据生成
- [ ] ACE 专家代数的 gauge fixing 实现
- [ ] 为 Paper 3 (SCX-MLIP) 准备 MLIP 实验数据

## 关键文件

- [EGP.md](G:\仿真数据\egp_archive\EGP-milp\egp-V1\EGP.md) — 原始项目定义
- [agent_outputs/](../egp/CodexKnowledge/agent_outputs/) — 论文重设计

## 相关笔记

- [[SCX-框架]] — 从 EGP 衍生的通用框架
- [[ACE-Expert-Algebra]] — ACE 专家代数子项目
- [[../00_入口/论文谱系|论文谱系]] — EGP = Paper 1
