# SCX 数学框架总览

> 状态条件专家性理论 — 从多专家系统的可靠性问题到数据价值定义

**最后更新**: 2026-06-27

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

## 三个核心定理 (theorems/)

| 定理 | 文件 | 内容 | 状态 |
|------|------|------|------|
| Thm 1 | `theorems/01_noise_detection_guarantee.md` | 多专家一致性噪声检测保证：当 M 个在不相交数据上独立训练的专家对样本的一致性得分 C(x) 超过阈值 θ 时，该样本是标签噪声的置信度以指数速率收敛到 1 | **完整**（2026-06-27 修正） |
| Thm 2 | `theorems/02_weak_feature_failure.md` | 弱特征失效下界：当特征表示 φ(x) 包含的真实状态信息不足时，基于一致性的噪声检测方法无法优于损失基线 | **完整** |
| Thm 3 | `theorems/03_unidentifiability_theorem.md` | 噪声与可学习困难的不可识别性：证明无 A1-A6 时两者不可区分，因此 A1-A6 是打破不可识别性的最小条件 | **完整**（2026-06-27） |

**逻辑闭环**: Theorem 1 为 Prop 4 的循环定义修复提供了理论基础（C(x) 替代 r̄(s)）。Theorem 2 界定边界条件。Theorem 3 从必要性方向提供闭环——证明假设是必须的而非任意的。

---

## 六个命题 (propositions/)

| 命题 | 文件 | 内容 | 状态 |
|------|------|------|------|
| Prop 1 | `propositions/01_global_ranking_insufficiency.md` | **Regret 下界**：异质输入空间中不存在与状态无关的全局最优专家排序。任何全局聚合指标（平均精度、AUC 等）必然丢失信息，其后悔值 (regret) 受状态级排序交叉程度的下界约束 | **已更新**（原 Arrow 类比已归档） |
| Prop 2 | `propositions/02_higherror_suboptimality.md` | 高误差 ≠ 高价值：max-residual sampling 在噪声存在时浪费预算，应使用 state-value sampling | **完整** |
| Prop 3 | `propositions/03_state_conditioned_weighting.md` | 状态条件专家加权优于全局固定权重，w_m(x) ∝ exp(-α · Σ_s γ_s(x) · R̂_m(s)) | **有完整证明** |
| Prop 4 | `propositions/04_compression_fidelity.md` | SCX-Compress 压缩保真定理、安全压缩比条件、与经典 coreset 理论的关系 | **完整**（2026-06-27 循环定义修复） |
| Prop 5 | `propositions/05_expert_governance_protocol.md` | 专家治理协议 | **待完善** |
| Prop 6 | `propositions/06_two_layer_state_discovery.md` | 二层状态发现 | **待完善** |

### 关键变更

- **Prop 1**: 重描述为 regret 下界问题。Section 4（Arrow 不可能定理类比）已归档到 `archive/arrow_analogy_removed.md` —— 该类比虽具启发性，但 SCX 的"不可能性"不要求 Arrow 的普遍性条件，易引起误导。
- **Prop 3**: 已有完整的数学证明，不再只是概念陈述。
- **Prop 4**: 原始 D(s) 依赖 r̄(s)（需真实标签）存在循环定义。已用 Theorem 1 的一致性得分 C̄(s) 替代，使 D(s) 可完全从无监督数据计算，代价是保真界松弛 O(1/√M)。

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

### 3. State Data Value (已弃用)

> **2026-06-27**: V(s) = r̄(s) · ρ(s) · L(s) · [1 - D(s)] · max_m SCX_m(s) 已被弃用。其功能已被更精确的组件分解取代：冗余分数 D(s) 负责压缩决策，一致性得分 C̄(s) 负责噪声检测，状态条件风险 R̂_m(s) 负责专家路由。

---

## 算法: State-Certified Active Learning

```
输入: L (已标注), U (未标注), E (专家), φ (表示映射)

1. 在 φ(X) 中构造状态 S
2. 估计 C̄(s), ρ(s), D(s)
3. 估计 R̂_m(s) 对所有专家 m 和状态 s
4. 分类每个状态: valuable / redundant / noisy / expert-dependent
5. 对每个状态选择动作:
   a*(s) = arg max_a U(a, s)
   其中 a ∈ {acquire, relabel, downweight, discard, route}
6. 执行动作，更新模型和状态图
7. 重复
```

> 步骤 2 中，D(s) 的计算现已不需要真实标签（使用 Theorem 1 的 C̄(s) 替代 r̄(s)）。C̄(s) 直接来自多专家一致性，使算法可在完全无监督环境下运行。

---

## 动作空间

| 动作 | 适用条件 | 含义 |
|------|----------|------|
| **acquire** | r̄(s)↑, ρ(s)↑, C̄(s)↑ | 补该状态的样本 |
| **relabel** | r̄(s)↑, ExpertConflict(s)↑ | 找强 oracle 仲裁 |
| **downweight** | r(x)↑, ρ(s)↓, C̄(s)↓ | 降权疑似噪声 |
| **discard** | r(x)↑, ρ(s)↓, C̄(s)↓ (极端) | 丢弃坏数据 |
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
├── README.md                            ← 本文件
├── definitions/
│   ├── 01_state_conditioned_risk.md     # 状态条件专家风险定义
│   ├── 02_expert_risk.md                # 专家风险
│   ├── 03_scx_reliability.md            # SCX 可靠性
│   ├── 04_state_data_value.md           # 状态数据价值（已弃用）
│   ├── 05_data_classification.md        # 数据四分类
│   └── 06_learnability_noise.md         # 可学习性 vs 噪声
├── theorems/
│   ├── 01_noise_detection_guarantee.md  # Thm 1: 多专家一致性噪声检测
│   ├── 02_weak_feature_failure.md       # Thm 2: 弱特征失效下界
│   └── 03_unidentifiability_theorem.md  # Thm 3: 噪声与困难的不可识别性
├── propositions/
│   ├── 01_global_ranking_insufficiency.md  # Prop 1: 全局排序不足 / regret 下界
│   ├── 02_higherror_suboptimality.md       # Prop 2: 高误差 ≠ 高价值
│   ├── 03_state_conditioned_weighting.md   # Prop 3: 状态条件专家加权
│   ├── 04_compression_fidelity.md          # Prop 4: 压缩保真（循环定义已修复）
│   ├── 05_expert_governance_protocol.md    # Prop 5: 专家治理协议
│   └── 06_two_layer_state_discovery.md     # Prop 6: 二层状态发现
├── archive/
│   └── arrow_analogy_removed.md            # [归档] Prop 1 Arrow 类比（已移除）
└── algorithm/
    └── 01_state_certified_al.md            # 算法描述
```
