# SCX 核心数学定义速查

> 内容来源：AI 对话（2026-06-25），待形式化整理到 `theory/` 目录

---

## 1. 问题设定

设：
- 输入空间 X，标签空间 Y
- 未知真实标注函数 f*: X → Y
- M 个专家 E = {f_1, f_2, ..., f_M}
- 状态映射 s: X → S（或软分配 p(s|x)）
- 表示映射 φ: X → R^d

## 2. 核心对象

### Definition 1: State-Conditioned Expert Risk

```
R_m(s) = E_{x~P(·|s)} [ ℓ(f_m(x), f*(x)) ]
```

专家的风险不是全局量 R_m，而是状态条件量 R_m(s)。

### Definition 2: SCX Reliability

```
SCX_m(s) = P( ℓ(f_m(x), y) < τ | x ∈ s )
```

即专家 m 在状态 s 下做出可接受预测的概率。

### Definition 3: State Data Value

```
V(s) = r̄(s) · ρ(s) · L(s) · [1 - D(s)] · max_m SCX_m(s)
```

其中：
- `r̄(s) = E[ℓ(f(x), y) | s]` — 当前模型在该状态的平均误差
- `ρ(s) = P(x ∈ s)` — 状态出现概率/质量
- `L(s)` — 可学习性（状态内一致、非噪声）
- `D(s)` — 冗余度（已充分覆盖程度）

### Definition 4: Learnability Score

```
L(s) = C(s) · [1 - N(s)]
```

- C(s): 状态内一致性（标签一致、专家预测一致）
- N(s): 噪声分数

### Definition 5: Noise Score (per sample)

```
NoiseScore(x_i) = r_i · (1/ρ(s_i)+ε) · [1 - C(s_i)]
```

- 高误差 + 低密度 + 低一致性 → 更像噪声
- 高误差 + 高密度 + 高一致性 → 更像可学习困难状态

## 3. 数据四分类

| 类别 | 条件 | 动作 |
|------|------|------|
| **Valuable** | r̄(s)↑, ρ(s)↑, C(s)↑, D(s)↓ | acquire |
| **Redundant** | r̄(s)↓, ρ(s)↑, Coverage(s)↑ | skip |
| **Noisy** | r(x)↑, ρ(s)↓, C(s)↓ | downweight/discard |
| **Expert-dependent** | ∃m: R_m(s) ≪ R_n(s) for n≠m | route to expert m |

## 4. 专家路由

```
m*(x) = arg min_m Σ_s γ_s(x) · R_m(s) + λ · C_m
```

或权重形式：

```
w_m(x) ∝ exp( -α · Σ_s γ_s(x) · R̂_m(s) )
```

## 5. State-Wise Acquisition

```
s* = arg max_s  r̄(s) · ρ(s) · L(s) · [1 - D(s)]
```

先选高价值状态，再在状态内选代表点。

## 6. 三个核心命题

### Proposition 1: Global Expert Ranking Insufficiency

若存在 s₁, s₂ 使得：
```
R_a(s₁) < R_b(s₁)  但  R_a(s₂) > R_b(s₂)
```
则不存在全局最优专家排序。专家选择必须状态条件化。

### Proposition 2: High-Error Sampling Suboptimality under Noise

高误差集合 H = H_learnable ∪ H_noise。若：
```
P(ΔR < 0 | H_learnable) > P(ΔR < 0 | H_noise)
```
则 max-residual sampling (x* = arg max r(x)) 浪费标注预算。
应改用 state-value sampling (s* = arg max r̄(s)·ρ(s)·C(s))。

### Proposition 3: State-Conditioned Weighting

最优专家权重不是全局常数，而是：
```
w_m(x) ∝ exp( -α · Σ_s γ_s(x) · R̂_m(s) )
```

## 7. 与材料 MLIP 的实例化

| 数学对象 | 材料实例 |
|----------|----------|
| x | 原子结构/局域环境 |
| y | DFT 能量/力 |
| f_m | ACE/NEP/MACE expert |
| φ(x) | ACE/SOAP/描述符 |
| s | sp², sp³, 断键, 表面, Al-Ga mixed, 高应变 |
| R_m(s) | expert 在该结构状态下的误差 |
| acquire | 补 DFT 样本 |
| relabel | DFT 仲裁 |
| downweight | 清理坏点 |
| route | 选择最合适的 expert 标注 |

## 8. 论文标题建议

> **SCX: State-Conditioned eXpertise for Data Valuation and Expert-Guided Learning**

中文：**SCX：用于数据价值评估与专家引导学习的状态条件专家性框架**
