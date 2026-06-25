# SCX 数学框架总览

> 状态条件专家性理论 — 从多专家系统的可靠性问题到数据价值定义

---

## 问题

给定 M 个专家 {f_1, ..., f_M}，输入空间 X，标签空间 Y。

**传统做法**：给每个专家一个全局准确率 R_m = E[ℓ(f_m(x), y)]。

**问题**：异质输入空间中，专家的准确度在不同区域差异很大。全局排序无法反映这一点。

## 核心洞察

```
R_m 是不够的。正确的对象是 R_m(s)。
```

其中 s: X → S 是状态映射，将输入分配到潜在状态。

---

## 三个核心定义

### 1. State-Conditioned Expert Risk

```
R_m(s) = E_{x~P(·|s)} [ ℓ(f_m(x), f*(x)) ]
```

### 2. SCX Reliability

```
SCX_m(s) = P( ℓ(f_m(x), y) < τ | x ∈ s )
```

### 3. State Data Value

```
V(s) = r̄(s) · ρ(s) · L(s) · [1 - D(s)] · max_m SCX_m(s)
```

---

## 三个命题

### Proposition 1: 全局排序不足

若 ∃ s₁, s₂: R_a(s₁) < R_b(s₁) 但 R_a(s₂) > R_b(s₂)，则不存在全局最优专家。

→ 专家选择必须状态条件化。

### Proposition 2: 高误差 ≠ 高价值

高误差可能来自可学习困难状态（应补样本）或噪声（应丢弃）。

max-residual sampling (x* = arg max r(x)) 在噪声存在时浪费预算。

→ 应使用 state-value sampling (s* = arg max r̄(s)·ρ(s)·C(s))。

### Proposition 3: 状态条件专家加权

```
w_m(x) ∝ exp( -α · Σ_s γ_s(x) · R̂_m(s) )
```

优于全局固定权重。

---

## 算法: State-Certified Active Learning

```
输入: L (已标注), U (未标注), E (专家), φ (表示映射)

1. 在 φ(X) 中构造状态 S
2. 估计 r̄(s), ρ(s), C(s), D(s)
3. 估计 R̂_m(s) 对所有专家 m 和状态 s
4. 分类每个状态: valuable / redundant / noisy / expert-dependent
5. 对每个状态选择动作:
   a*(s) = arg max_a U(a, s)
   其中 a ∈ {acquire, relabel, downweight, discard, route}
6. 执行动作，更新模型和状态图
7. 重复
```

---

## 动作空间

| 动作 | 适用条件 | 含义 |
|------|----------|------|
| **acquire** | r̄(s)↑, ρ(s)↑, C(s)↑ | 补该状态的样本 |
| **relabel** | r̄(s)↑, ExpertConflict(s)↑ | 找强 oracle 仲裁 |
| **downweight** | r(x)↑, ρ(s)↓, C(s)↓ | 降权疑似噪声 |
| **discard** | r(x)↑, ρ(s)↓, C(s)↓ (极端) | 丢弃坏数据 |
| **route** | SCX_m(s) ≫ SCX_n(s) | 路由到可靠专家 |

---

## 跨领域适用

| 领域 | X | Y | f_m | s |
|------|---|---|-----|---|
| MLIP | 原子结构 | DFT 能量/力 | ACE/NEP/MACE | sp²/sp³/断键/表面 |
| 医学图像 | 影像 | 诊断标签 | 不同模型/医生 | 病灶类型 |
| 遥感 | 图像 | 地物类别 | 不同分类器 | 地貌类型 |
| LLM | 文本 | 标签/评分 | 不同大模型 | 语义/主题/难度 |
| 自动驾驶 | 传感器 | 检测框 | 不同检测器 | 天气/光照/道路 |

---

## 文件结构

```
theory/
├── README.md              ← 本文件
├── definitions/
│   ├── 01_state_space.md          # 状态空间定义
│   ├── 02_expert_risk.md          # 状态条件专家风险
│   ├── 03_scx_reliability.md      # SCX 可靠性
│   ├── 04_state_data_value.md     # 状态数据价值
│   ├── 05_data_classification.md  # 数据四分类
│   └── 06_learnability_noise.md   # 可学习性 vs 噪声
├── propositions/
│   ├── 01_global_ranking_insufficiency.md
│   ├── 02_higherror_suboptimality.md
│   └── 03_state_conditioned_weighting.md
└── algorithm/
    └── 01_state_certified_al.md   # 算法描述
```
