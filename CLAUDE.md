# CLAUDE.md — SCX 项目

> 最后更新：2026-06-28

## 项目概述

SCX (State-Conditioned eXpertise) 是一个数学理论 + 工程框架，核心发现是：**区分标签噪声和样本内在困难——这个问题在不加假设时已被数学证明不可解。** 在最小充分假设下，多专家一致性可以提供精确常数 minimax 最优的噪声检测。

## 论文矩阵（全部直指 Nature 系列）

| # | 目录 | 期刊 | 状态 |
|:--:|------|------|:--:|
| I | `paper/nature_theory/` | **Nature** | 正文已起草, SI 待转译 |
| II | `paper/nature_curation/` | **Nat Comp Sci** | 概念已设计 |
| III | `paper/paper1_nature/` | **Nat Mach Intell** | 已有草稿, 等 GPU |
| IV | `paper/paper2_mlip/` | **npj Comp Mat** | 已完成, 等超算 |

参见 `paper/PAPER_MATRIX.md`。

## 核心定理

| # | 内容 | 文件 | 验证状态 |
|:--:|------|------|:--:|
| 1 | 噪声检测保证 (F1 指数收敛) | `theory/theorems/01_noise_detection_guarantee.md` | ✅ |
| 2 | 弱特征失效边界 (δ→0 退化) | `theory/theorems/02_weak_feature_failure.md` | ✅ |
| 3 | 噪声-困难不可辨识性 | `theory/theorems/03_unidentifiability_theorem.md` | ✅ |
| 4' | 精确常数 minimax 最优性 | `theory/explorations/exact_constant_minimax.md` + 4 lemma 文件 | ✅ |
| 5 | 聚类一致性 (k-means 状态发现) | `theory/explorations/cluster_consistency_v3.md` | ✅ |
| 6 | Bootstrap 稳定性诊断 | `theory/explorations/feature_strength_via_stability.md` | ✅ |

权威参考：`theory/THEOREMS_UNIFIED.md`。

## 关键路径

```
paper/nature_theory/           ← 主攻：数学理论 Nature 投稿
paper/nature_curation/         ← 次攻：实践原则 Nat Comp Sci
paper/paper1_nature/           ← 第三：方法验证 Nat Mach Intell
scx-life/                      ← 应用模块 (health/ + drug/)
```

## 当前阻塞

- GPU 不可用 → Paper III 的 AlN v3 重训、CIFAR/MedMNIST 完整训练
- Nature SI 需要 LaTeX 转译 (~12,000 行 md → tex, ~86 页)

## 关联

- 超算管理：`../.hpc/hpcmgr.py` (作业提交/监控)
- 超算盘符：`W:` → cxshu, `X:/Y:/Z:` → xiyang
- 知识库：`knowledge/` (Obsidian vault)
