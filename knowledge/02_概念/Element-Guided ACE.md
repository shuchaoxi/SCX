---
tags: [概念, EGP, ACE]
created: 2026-06-14
aliases: [Element-Guided ACE, EGA]
---

# Element-Guided ACE

## 定义

EGP 的核心框架：用**元素类别**（Al、Ga、N 等）作为先验来组织和初始化 ACE 专家。

## 核心思想

> 不同化学元素周围的局域环境天然形成不同的势能面区域。

元素引导提供了：
- 人类可理解的结构化专家库组织方式
- 自然的专家域划分先验
- 与已有元素特异性 ACE 势函数的兼容性

## 与两层 EGP 的关系

元素引导是**两层 EGP** 的 Layer 0（材料先验层）：
- Layer 0：元素类别 → 粗粒度专家划分
- Layer 1：局域环境描述符（组成、应变、配位）→ 连续路由

## 从 EGA 到 SCX 的演化

Element-Guided ACE 中的"元素"是状态的一种特例。SCX 将其推广为**任意状态空间划分**（不限于化学元素）：

```
Element-Guided (材料特化) → State-Conditioned (通用 ML)
```

## 来源

- EGP 概念提出：[[2026-06-14_EGP概念萌芽|2026-06-14]]
- Agent 讨论：[EGP_AlN_GaN_AlGaN_Agent_Discussion.md](G:\仿真数据\egp_archive\EGP-milp\egp-V1\EGP_AlN_GaN_AlGaN_Agent_Discussion.md)

## 相关概念

- [[Gauge-Normalized Residual]] — ACE 语境下的 gauge fixing
- [[State-Conditioned eXpertise]] — 从此推广而来的通用框架
