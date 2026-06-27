---
tags: [项目, EGP, ACE]
status: active
parent: EGP-MLIP
---

# ACE-Expert-Algebra · 项目面板

## 概述

ACE 专家代数是 EGP 的数学核心——用代数方法定义和操作 ACE/PACE 势函数专家的规范化、对齐和合并。

## 当前状态

| 指标 | 数值 |
|------|------|
| 阶段 | 框架设计完成，实现中 |
| 核心模块 | `experts/`, `gauge/`, `export/` |
| 代码位置 | `G:\Xiaogan_Supercomputing_data\egp\ace_expert_algebra\` |

## 模块结构

```
ace_expert_algebra/
├── src/
│   ├── experts/      # 专家定义与注册
│   ├── gauge/        # Gauge fixing 算法
│   └── export/       # 模型导出
├── scripts/          # 执行脚本
├── tests/            # 测试
└── outputs/          # 输出
```

## 核心数学

### Gauge Fixing

不同 ACE 专家的参考能量零点不同，需要 gauge fixing：

$$E_{\text{merged}}(x) = \sum_k w_k(x) \cdot [E_k^{\text{ACE}}(x) - \Delta_k(x)]$$

### Expert Algebra 操作

| 操作 | 数学 | 含义 |
|------|------|------|
| Gauge Fix | $E'_k = E_k - \Delta_k$ | 对齐能量参考系 |
| Merge | $E = \sum w_k E'_k$ | 加权合并专家 |
| Compose | $E_{A \circ B}$ | 组合两个 expert domain |
| Distill | $E_{\text{student}}$ | 将 merged expert 蒸馏为单一模型 |

## 与 SCX 的关系

ACE Expert Algebra 是 [[../02_概念/State-Conditioned eXpertise|SCX]] 数学框架的**材料科学具体化**：
- SCX 提供通用的专家可靠性和路由理论
- ACE Expert Algebra 提供 ACE/PACE 语境下的具体实现

## 相关笔记

- [[EGP-MLIP]] — 父项目
- [[../02_概念/Gauge-Normalized Residual|Gauge-Normalized Residual]]
- [[../02_概念/Element-Guided ACE|Element-Guided ACE]]
- [[../00_入口/论文谱系|论文谱系]] — Paper 1 (EGP) + Paper 3 (SCX-MLIP)
