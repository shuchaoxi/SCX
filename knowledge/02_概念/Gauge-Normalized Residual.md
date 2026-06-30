---
tags: [概念, EGP, ACE]
created: 2026-06-19
aliases: [Gauge-Normalized Residual ACE]
---

# Gauge-Normalized Residual

## 问题

不同 ACE 专家（势函数）在各自训练域上使用了不同的 **gauge**（参考能量零点），不能直接混合或比较。

例如：
- 专家 A 在 AlN bulk 上训练，能量 zero-point 是完美 AlN 晶格
- 专家 B 在 AlN defect 上训练，能量 zero-point 包含缺陷形成能

直接混合两个专家的能量预测会导致非物理的跳跃。

## 方案

$$E_{\text{merged}}(x) = \sum_k w_k(x) \cdot [E_k^{\text{ACE}}(x) - \Delta_k(x)]$$

其中 $\Delta_k(x)$ 是 gauge correction term，依赖局域环境 $x$。

### Gauge Fixing 步骤

1. 为每个专家确定参考结构（如 bulk AlN）
2. 计算专家在参考结构上的能量偏移
3. 将能量偏移模型化为局域环境的平滑函数
4. 在混合前对每个专家的预测应用 gauge correction

## 与 SCX 的关系

Gauge-Normalized Residual 是 [[State-Conditioned eXpertise|SCX]] 的数学前身：
- "不同专家在相同构型上给出不同预测" → 专家可靠性是状态条件的
- "gauge fixing 需要局域环境信息" → 状态空间的定义和发现
- "残差映射" → SCX 中的 error landscape 概念

## 来源

- 概念形成：[[2026-06-19_ACE专家代数|2026-06-19]]
- 框架文档：[gauge_normalized_residual_ace_expert_algebra_framework.md](G:\仿真数据\egp_archive\EGP-milp\EGP-V2agent_discussions\gauge_normalized_residual_ace_expert_algebra_framework.md)

## 相关概念

- [[Element-Guided ACE]] — 并行概念，关注元素引导
- [[State-Conditioned eXpertise]] — 从此概念推广而来
- [[专家路由]] — gauge fixing 后的混合策略
