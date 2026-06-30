---
tags: [TODO, 任务, MOC]
created: 2026-06-27
---

# 任务系统 · 总览

> 全面推进 SCX 项目：理论证明 + 论文写作 + 实验 + 代码工程。不只为发论文。

## 文件夹结构

| 文件 | 内容 | 阻塞条件 |
|------|------|---------|
| [[NOW_理论\|🧮 理论证明]] | 待重构/新证的定理 | 无阻塞，CPU 可做 |
| [[NOW_论文\|📝 论文推进]] | Paper 1-4 写作任务 | Paper 2 无阻塞 |
| [[NOW_实验\|🔬 实验任务]] | CPU 可做的实验 | 部分等 GPU |
| [[NOW_代码\|💻 代码工程]] | SCX 代码改进 | 无阻塞 |
| [[GPU_等待\|⏳ GPU 阻塞任务]] | 等显卡才能做的 | 等 GPU |
| [[里程碑\|🎯 里程碑]] | 关键节点追踪 | — |

## 当前环境

| 资源 | 状态 |
|------|------|
| GPU | ❌ 无（torch CPU-only） |
| CPU ML | ✅ numpy, scipy, sklearn, pandas |
| Python | 3.11.9 |
| SCX 包 | ⚠️ 需 `pip install -e .` |
| 超算 | ✅ cxshu (AlN v3 DFT 数据已生成) |
| Obsidian | ✅ 知识库就绪 |

## 优先级速览

```
立即（现在 CPU 可做）:
  🧮 重构定理 1+2 → 理论证明
  📝 完成 Paper 2 (EGP gauge fixing) → 投稿
  📝 Paper 1 理论部分草稿
  🔬 UCI tabular 实验
  💻 修复 V(s) 循环定义

GPU 到手后:
  🔬 AlN v3 去噪重训（最高优先级）
  🔬 CIFAR 完整训练
  🔬 MedMNIST 强 backbone
```

## 使用方式

1. 每天开始：扫一眼 `NOW_*.md`，选 1-3 个任务
2. 完成任务：勾选 `[x]`，在末尾加一行 `完成: YYYY-MM-DD`
3. 遇到阻塞：移到 `GPU_等待.md` 或加 `🚫 阻塞原因`
4. 每周回顾：更新 [[里程碑]]
