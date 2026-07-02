# NPE（非扩散均衡）博弈论基础：第一原理重建与全面修正

**日期：** 2026年7月2日  
**状态：** 从第一原理重建，修正原论文定理1-2的全部代数错误  
**语言：** 中文  
**参考：** `G:/Xiaogan_Supercomputing_data/SCX/papers/yajie_protocol/main.tex`；`game_theory_review.md`

---

## 0. 执行摘要

原论文的NPE博弈论部分存在五个独立的代数/定义错误。本文件从第一原理重建整个NPE模型，统一κ参数定义，修正定理1-2的全部推导，并提供独立验证。修正后的结论与原文在定性方向上一致（全体采纳均衡存在且随CEC自我强化），但均衡条件、混合策略公式和CEC临界值均有实质性变化。

**关键修正：**
1. 全体采纳均衡条件：$\Delta(|\mathcal{E}|) \geq \lambda - \kappa$ → $\boxed{\Delta(|\mathcal{E}|) \geq -\lambda}$
2. 2人混合策略概率：$p^* = (-\Delta_A - 2\kappa)/(\lambda - \kappa)$ → $\boxed{p^* = (-\Delta - \kappa)/(\lambda - \kappa)}$
3. N人混合策略Γ函数：$\Gamma = -\Delta(|\mathcal{E}|) + \lambda - 2\kappa$ → $\boxed{\lambda p^{n-1} = -\Delta(|\mathcal{E}|) - \kappa}$
4. κ参数：三重矛盾定义 → $\boxed{\text{统一为"每个开发者的自包含扩散成本"}}$
5. 定理2 CEC临界值：$\theta^*$ 表达式重建

---

## 1. 第一原理：统一模型设定

### 1.1 参与者与策略

$N = \{1, 2, \ldots, n\}$ 个辖区（$n \geq 2$）。每个辖区 $i$ 的纯策略空间 $S_i = \{A, D\}$：
- $A$（Adopt）：采纳现有协议
- $D$（Develop）：开发独立协议

### 1.2 支付函数（统一κ定义）

**κ的统一经济含义：** κ > 0 是**每个开发者（包括自身）所承担的扩散成本**。当一个辖区选择开发独立协议时，该辖区自身承担一份κ（代表维护独立协议、兼容现有体系、孤立于互认网络等的持续性成本）；其他开发者同样各自承担κ。采纳者（A）不承担κ——他们处于现有协议的保护伞下。

**λ的经济含义：** λ > 0 是碎片化公共劣品成本。一旦任何辖区选择D，全球审计基础设施碎片化被触发，**所有**辖区（包括首个开发者）均承担λ。

**参数排序：** $\lambda > \kappa > 0$（碎片化的公共劣品效应超过单一扩散的边际成本）。

**形式化支付函数：**

记 $n_D^{\text{all}}(\mathbf{a}) = \sum_{j=1}^{n} \mathbb{I}[a_j = D]$ 为全体开发者的总数。碎片化指标 $\mathbb{I}[n_D^{\text{all}} > 0]$ 当且仅当存在至少一个开发者时为1。

```
π_i(A, a_{-i}) = V[θ(|E|)] - c_adopt - λ · I[n_D^{all} > 0]

π_i(D, a_{-i}) = V[θ(0)] - c_develop - κ · n_D^{all} - λ · I[n_D^{all} > 0]
```

**关键设计决策：** 
- 采纳者不承担κ（被现有协议保护）
- 开发者承担 κ × n_D^{all}：包括自己和其他所有开发者
- 两者均承担λ（若碎片化被触发）

### 1.3 验证：2人支付矩阵

将统一支付函数应用于N=2情形：

| | 玩家2: A | 玩家2: D |
|---|---|---|
| **玩家1: A** | $V[\theta(|\mathcal{E}|)] - c^{\text{adopt}}$ | $V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} - \lambda$ |
| **玩家1: D** | $V[\theta(0)] - c^{\text{develop}} - \kappa - \lambda$ | $V[\theta(0)] - c^{\text{develop}} - 2\kappa - \lambda$ |

**验证 (A,A)：** $n_D^{\text{all}} = 0, \mathbb{I}=0$ → $V[\theta(|\mathcal{E}|)] - c^{\text{adopt}}$ ✓  
**验证 (A,D)：** $n_D^{\text{all}} = 1, \mathbb{I}=1$ → 玩家1(A): $V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} - \lambda$ ✓  
**验证 (D,A)：** $n_D^{\text{all}} = 1, \mathbb{I}=1$ → 玩家1(D): $V[\theta(0)] - c^{\text{develop}} - \kappa - \lambda$ ✓  
**验证 (D,D)：** $n_D^{\text{all}} = 2, \mathbb{I}=1$ → 玩家1(D): $V[\theta(0)] - c^{\text{develop}} - 2\kappa - \lambda$ ✓

此矩阵与原论文（main.tex lines 461-463）**完全一致**。κ的定义现在统一且可扩展到N人。

### 1.4 基本参数定义

**定义1（采纳优势 Δ）：**

$$\Delta(|\mathcal{E}|) \triangleq \pi_i(A, \mathbf{A}_{-i}) - [V[\theta(0)] - c^{\text{develop}} - \kappa]$$

即采纳者收益减去"单独开发者的基本成本"（不含λ碎片化成本）。展开：

$$\boxed{\Delta(|\mathcal{E}|) = V[\theta(|\mathcal{E}|)] - V[\theta(0)] - (c^{\text{adopt}} - c^{\text{develop}}) + \kappa}$$

此定义与原论文方程(7)一致，且κ贡献为正——CEC越大、开发沉没成本越高、κ越大，采纳优势越大。

**性质：** 由假设A1（$V$严格递增凹）和A2（$\theta$随CEC指数增长），$\Delta(|\mathcal{E}|)$ 严格递增，$\Delta'(|\mathcal{E}|) > 0$，且 $\lim_{|\mathcal{E}| \to \infty} \Delta(|\mathcal{E}|) = V(\theta_{\max}) - V(\theta_0) + c^{\text{develop}} - c^{\text{adopt}} + \kappa$（有限上界）。

**定义2（2人博弈的简化符号）：**

$$\Delta_A \triangleq \Delta(|\mathcal{E}|) \quad \text{（在2人情形下，}\Delta_A\text{与}\Delta(|\mathcal{E}|)\text{等价）}$$

---

## 2. 修正定理1：NPE博弈的完整纳什均衡刻画

### 定理1（修正版）

在假设A1--A7下，考虑非扩散博弈 $\Gamma^{\text{NP}}$，$n \geq 2$。

**(i) 均衡存在性：** 纯策略纳什均衡始终存在。由Nash(1951)定理保证（有限博弈）。

**(ii) 全体采纳均衡（修正）：** $s^* = (A, \ldots, A)$ 是纳什均衡当且仅当：

$$\boxed{\Delta(|\mathcal{E}|) \geq -\lambda} \tag{N1}$$

**推导：**

$\pi_i(A, \mathbf{A}_{-i}) = V[\theta(|\mathcal{E}|)] - c^{\text{adopt}}$（$n_D^{\text{all}} = 0$，无碎片化）

$\pi_i(D, \mathbf{A}_{-i}) = V[\theta(0)] - c^{\text{develop}} - \kappa - \lambda$（$i$单边偏离→$n_D^{\text{all}}=1$→碎片化触发且$i$承担κ）

NE条件 $\pi_i(A, \mathbf{A}_{-i}) \geq \pi_i(D, \mathbf{A}_{-i})$：

$$V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} \geq V[\theta(0)] - c^{\text{develop}} - \kappa - \lambda$$

代入 $\Delta$ 的定义（$V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} = \Delta + V[\theta(0)] - c^{\text{develop}} - \kappa$）：

$$\Delta + V[\theta(0)] - c^{\text{develop}} - \kappa \geq V[\theta(0)] - c^{\text{develop}} - \kappa - \lambda$$

$$\boxed{\Delta \geq -\lambda}$$

**与原论文对比：** 原论文声称 $\Delta \geq \lambda - \kappa$（main.tex line 208）。这是一个代数错误——原论文在line 247将 $V[\theta(|\mathcal{E}|)] - c^{\text{adopt}}$ 替换为 $\Delta + \kappa$ 时遗漏了正确的代数变换。正确条件是 $\Delta \geq -\lambda$。

**解读：** 在合理参数（$\Delta > 0, \lambda > 0$）下，$-\lambda < 0 < \Delta$，条件 $\Delta \geq -\lambda$ **恒成立**。这意味着全体采纳均衡在几乎所有非退化参数下都存在，且为**严格**纳什均衡（strict NE）。这与原论文的叙事有本质不同：原论文暗示需要CEC增长到一定规模才能触发均衡，但修正后的结论是——只要采纳的基本价值超过开发成本（即 $\Delta > 0$），全体采纳从第一刻起就是均衡。

**(iii) 全体开发均衡：** $s^D = (D, \ldots, D)$ 是纳什均衡当且仅当：

$$\boxed{\Delta(|\mathcal{E}|) \leq -(n-1)\kappa} \tag{N2}$$

**推导：**

$\pi_i(D, \mathbf{D}_{-i}) = V[\theta(0)] - c^{\text{develop}} - n\kappa - \lambda$（所有$n$个辖区均为开发者）

$\pi_i(A, \mathbf{D}_{-i}) = V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} - \lambda$（$i$偏离至A，仍有$n-1$个开发者→$n_D^{\text{all}} > 0$→碎片化=1，但$i$不再承担κ）

NE条件：

$$V[\theta(0)] - c^{\text{develop}} - n\kappa - \lambda \geq V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} - \lambda$$

消去$-\lambda$，代入$\Delta$：

$$V[\theta(0)] - c^{\text{develop}} - n\kappa \geq \Delta + V[\theta(0)] - c^{\text{develop}} - \kappa$$

$$-n\kappa \geq \Delta - \kappa$$

$$\boxed{\Delta \leq -(n-1)\kappa}$$

此条件与原论文一致（main.tex line 216）。在合理参数（$\Delta > 0, \kappa > 0$）下此条件不成立——全体开发不是均衡。

**(iv) 非对称纯策略均衡的不可能性：** 在任何纯策略NE中，所有辖区必须选择相同策略。不存在"部分采纳、部分开发"的纯策略NE（除测度为零的参数配置）。

**推导：**

设存在NE含 $n_D \in \{1, \ldots, n-1\}$ 个开发者。考虑一个采纳者 $i$：

$$\pi_i(A, s_{-i}) = V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} - \lambda \quad (n_D > 0 \Rightarrow \text{碎片化}=1)$$

$$\pi_i(D, s_{-i}) = V[\theta(0)] - c^{\text{develop}} - \kappa(n_D + 1) - \lambda$$

NE条件对采纳者 $i$：

$$V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} \geq V[\theta(0)] - c^{\text{develop}} - \kappa(n_D + 1)$$

代入$\Delta$：

$$\Delta + V[\theta(0)] - c^{\text{develop}} - \kappa \geq V[\theta(0)] - c^{\text{develop}} - \kappa(n_D + 1)$$

$$\Delta - \kappa \geq -\kappa(n_D + 1)$$

$$\boxed{\Delta \geq -\kappa n_D} \tag{C1}$$

考虑一个开发者 $j$：

$$\pi_j(D, s_{-j}) = V[\theta(0)] - c^{\text{develop}} - \kappa n_D - \lambda$$

$$\pi_j(A, s_{-j}) = V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} - \lambda$$

NE条件对开发者 $j$：

$$V[\theta(0)] - c^{\text{develop}} - \kappa n_D \geq V[\theta(|\mathcal{E}|)] - c^{\text{adopt}}$$

$$\boxed{\Delta \leq -\kappa(n_D - 1)} \tag{C2}$$

条件(C1)和(C2)同时成立要求 $-\kappa n_D \leq \Delta \leq -\kappa(n_D-1)$，即 $\Delta \in [-\kappa n_D, -\kappa(n_D-1)]$。对于固定的 $\Delta$ 和 $\kappa$，至多存在一个整数 $n_D$ 满足此区间——这是一个勒贝格测度为零的参数配置。对几乎所有参数值，非对称纯策略NE不存在。原论文此结论定性正确。

**(v) 对称混合策略均衡（修正）：** 当全体采纳和全体开发均非均衡时，存在唯一的对称混合策略NE。每个辖区以相同概率 $p^* \in (0,1)$ 选择A。

**N人混合策略推导：**

设每个辖区独立以概率 $p$ 选择A，$1-p$ 选择D。则除 $i$ 外其他辖区的开发者数量 $n_D^{\text{other}} \sim \text{Binomial}(n-1, 1-p)$。

辖区内 $i$ 选择A的期望支付：

$$\mathbb{E}[\pi_i(A)] = V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} - \lambda \cdot \mathbb{P}[n_D^{\text{other}} > 0]$$

$$= V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} - \lambda(1 - p^{n-1})$$

辖区内 $i$ 选择D的期望支付（此时 $n_D^{\text{all}} = n_D^{\text{other}} + 1$，碎片化始终=1）：

$$\mathbb{E}[\pi_i(D)] = V[\theta(0)] - c^{\text{develop}} - \kappa \cdot \mathbb{E}[n_D^{\text{other}} + 1] - \lambda$$

$$= V[\theta(0)] - c^{\text{develop}} - \kappa[(n-1)(1-p) + 1] - \lambda$$

无差异条件 $\mathbb{E}[\pi_i(A)] = \mathbb{E}[\pi_i(D)]$：

$$V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} - \lambda + \lambda p^{n-1} = V[\theta(0)] - c^{\text{develop}} - \kappa(n-1)(1-p) - \kappa - \lambda$$

消去 $-\lambda$：

$$V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} + \lambda p^{n-1} = V[\theta(0)] - c^{\text{develop}} - \kappa(n-1)(1-p) - \kappa$$

代入 $\Delta = V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} - [V[\theta(0)] - c^{\text{develop}} - \kappa]$：

$$V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} = \Delta + V[\theta(0)] - c^{\text{develop}} - \kappa$$

$$\Delta + V[\theta(0)] - c^{\text{develop}} - \kappa + \lambda p^{n-1} = V[\theta(0)] - c^{\text{develop}} - \kappa (n-1)(1-p) - \kappa$$

$$\Delta + \lambda p^{n-1} = -\kappa(n-1)(1-p)$$

$$\boxed{\Delta(|\mathcal{E}|) + \lambda p^{n-1} + \kappa(n-1)(1-p) = 0} \tag{N3}$$

此方程隐式定义 $p^*$。对于 $n=2$，可显式求解（见下文2人情形）。

**大群体极限（$n \to \infty$）：** 当 $n \to \infty$，若 $p < 1$，则 $p^{n-1} \to 0$，$(n-1)(1-p)$ 发散→方程(N3)要求 $\Delta \to \infty$（不可能）或 $(1-p) \to 0$。因此极限下 $p^* \to 1$——大群体中混合策略退化为近全体采纳。

### 2.1 2人博弈显式解

对 $n=2$，方程(N3)变为：

$$\Delta + \lambda p + \kappa(1-p) = 0$$

$$\Delta + \kappa + p(\lambda - \kappa) = 0$$

$$\boxed{p^* = \frac{-\Delta - \kappa}{\lambda - \kappa}} \tag{N4}$$

**与原文对比：**
- 原论文（line 507）：$p^* = \dfrac{-\Delta_A - 2\kappa}{\lambda - \kappa}$ — **分子多了一个κ**
- 审查意见（§1.1）：$p^* = \dfrac{-\Delta_A - \kappa}{\lambda - \kappa}$ — **正确**
- 本修正推导：一致确认为 $p^* = \dfrac{-\Delta - \kappa}{\lambda - \kappa}$（$\Delta_A = \Delta$ 在本统一框架下）

**概率合法性条件：** $p^* \in (0,1)$ 要求：

$$0 < \frac{-\Delta - \kappa}{\lambda - \kappa} < 1$$

由 $\lambda > \kappa > 0$，分母为正。因此：
- $p^* > 0 \iff -\Delta - \kappa > 0 \iff \boxed{\Delta < -\kappa}$
- $p^* < 1 \iff -\Delta - \kappa < \lambda - \kappa \iff -\Delta < \lambda \iff \boxed{\Delta > -\lambda}$

**混合策略均衡存在区域：** $-\lambda < \Delta < -\kappa$。

**关键洞察：** 由于在合理参数下 $\Delta = V[\theta(|\mathcal{E}|)] - V[\theta(0)] + c^{\text{develop}} - c^{\text{adopt}} + \kappa > 0$（因为 $V[\theta(|\mathcal{E}|)] > V[\theta(0)]$ 且 $c^{\text{develop}} > c^{\text{adopt}}$），我们有 $\Delta > 0 > -\kappa$，因此 $\Delta < -\kappa$ **不成立**。混合策略区域为空——在合理参数下不存在混合策略均衡。

这与原论文的声称（"For plausible parameter values...$p^*$ increases with $\Delta_A$...approaches 1"）**相矛盾**。原论文错误地认为混合策略在 $\Delta_A > 0$ 区域存在，但实际上在该区域混合策略的 $p^*$ 要么为负，要么大于1——均不构成合法概率。

---

## 3. 修正定理2：CEC临界值与均衡唯一性

### 定理2（修正版）

在假设A1--A7下：

**(i) 全体采纳均衡的条件验证：**

全体采纳均衡条件 $\Delta(|\mathcal{E}|) \geq -\lambda$ 不定义有意义的CEC临界值——由于 $\Delta(|\mathcal{E}|)$ 对所有 $|\mathcal{E}| \geq 0$ 成立 $\Delta(|\mathcal{E}|) > 0 > -\lambda$（在合理参数下），条件恒成立。

但是，原论文定义的 **CEC临界规模** 应当重新定义为满足 "全体采纳是**唯一**均衡" 的CEC规模。具体而言，当 $\Delta(|\mathcal{E}|) \geq -\lambda$ **且** $\Delta(|\mathcal{E}|) > -(n-1)\kappa$（即全体开发非均衡）时，全体采纳为唯一纯策略均衡。由于 $-\lambda < 0 < -(n-1)\kappa$ 不可能同时成立（因为 $-(n-1)\kappa < 0 < -\lambda$ 意味着 $\lambda < (n-1)\kappa$，与假设 $\lambda > \kappa$ 在 $n=2$ 时矛盾），我们需要重新分析：

- 条件(N1)：$\Delta \geq -\lambda$ — 由于 $\Delta > 0 > -\lambda$，始终成立 ✓
- 条件(N2)：$\Delta \leq -(n-1)\kappa$ — 由于 $\Delta > 0 > -(n-1)\kappa$，始终不成立 ✓

因此在所有合理参数下，**全体采纳是唯一纯策略纳什均衡**。不存在混合策略均衡（因为混合策略区域 $-\lambda < \Delta < -\kappa$ 与 $\Delta > 0$ 不相交）。

**(ii) 重新解释CEC的作用：**

CEC的增长不改变均衡的存在性（全体采纳从一开始就是均衡），但增强均衡的**稳定性裕度**。定义：

$$M(|\mathcal{E}|) \triangleq \Delta(|\mathcal{E}|) + \lambda$$

则 $M(|\mathcal{E}|)$ 严格递增，$M'(|\mathcal{E}|) = V'[\theta(|\mathcal{E}|)] \cdot \theta'(|\mathcal{E}|) > 0$。$M(|\mathcal{E}|)$ 衡量采纳者的偏离损失：

$$\pi_i(A, \mathbf{A}_{-i}) - \pi_i(D, \mathbf{A}_{-i}) = M(|\mathcal{E}|) > 0$$

CEC越大→ $M(|\mathcal{E}|)$ 越大→均衡越稳健（偏离的惩罚越大）。

**(iii) CEC临界值的替代定义：**

原论文的 $|\mathcal{E}|^*$ 对应于 $\Delta(|\mathcal{E}|) \geq \lambda - \kappa$ 的阈值，但这是基于错误的均衡条件。在修正框架下，若要保持"临界CEC"概念，可将其定义为**均衡稳定性裕度达到某个外生阈值**的时刻：

$$|\mathcal{E}|_M^* \triangleq \inf\{|\mathcal{E}| \geq 0 : M(|\mathcal{E}|) \geq M_0\}$$

其中 $M_0 > 0$ 是政策目标决定的稳定性阈值。或者，将其定义为**首次使 $\Delta(|\mathcal{E}|)$ 超过某个战略阈值的CEC规模**（如 $\Delta(|\mathcal{E}|) \geq \kappa$ 以确保单边偏离严格无利可图且稳健）。

**原定理2的错误：** 原论文（line 336）给出的显式解  

$$\theta^* = V^{-1}\left(V[\theta(0)] + c^{\text{adopt}} - c^{\text{develop}} - \kappa + \lambda - \kappa\right)$$

是基于错误条件 $\Delta = \lambda - \kappa$ 推导的，且 $\theta^*$ 表达式中的 "$-\kappa + \lambda - \kappa$" 应为 "$-\kappa$"（若基于修正条件 $\Delta = -\lambda$），但如上所述 $\Delta = -\lambda$ 在合理参数下无解（$\Delta > 0 > -\lambda$）。

---

## 4. 自我审查：新证明是否成立？

### 4.1 内部一致性检查

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 支付矩阵与N人函数一致 | ✅ | 统一κ定义后，(A,D)和(D,D)条目匹配 |
| Δ定义与使用一致 | ✅ | Δ始终= $V[\theta(\vert\mathcal{E}\vert)] - V[\theta(0)] - (c^{\text{adopt}} - c^{\text{develop}}) + \kappa$ |
| 全体采纳均衡条件 | ✅ | 正确推导为 $\Delta \geq -\lambda$，独立验证通过 |
| 全体开发均衡条件 | ✅ | 正确推导为 $\Delta \leq -(n-1)\kappa$，与原论文一致 |
| 非对称均衡不可能 | ✅ | 严格的测度为零论证，与原论文定性一致 |
| 2人混合策略 | ✅ | $p^* = (-\Delta-\kappa)/(\lambda-\kappa)$，与独立审查一致 |
| N人混合策略 | ✅ | 方程(N3)正确但隐式，$n=2$时退化为显式 |
| 参数一致性 | ✅ | $\lambda > \kappa > 0$，$c^{\text{develop}} > c^{\text{adopt}}$，$V$递增凹 |

### 4.2 关键定性结论的变化

| 原论文声称 | 修正后结论 | 变化性质 |
|-----------|-----------|---------|
| 全体采纳均衡需要 $\Delta \geq \lambda - \kappa$ | 全体采纳均衡需要 $\Delta \geq -\lambda$（恒成立） | **条件大幅弱化** |
| CEC需达到临界值才能触发均衡 | 均衡从 $t=0$ 即存在 | **时间线前移** |
| 混合策略在中间区域存在 | 混合策略区域 $\Delta < -\kappa$ 与 $\Delta > 0$ 不相交 | **混合策略不存在** |
| CEC临界值 $|\mathcal{E}|^*$ 有显式解 | $|\mathcal{E}|^*$ 在原意义下无解，需重新定义 | **定理2需重写** |
| 均衡稳定性裕度 $M = \Delta - (\lambda - \kappa)$ | 均衡稳定性裕度 $M = \Delta + \lambda$ | **表达式变化** |

### 4.3 模型是否存在根本性问题？

**如果NPE本质上不成立，什么成立？**

修正后的模型实际上**强化**了论文的核心主张：非扩散均衡比原论文声称的**更稳健**。

- 原论文：均衡需要在CEC积累到一定程度后才出现（动态故事）
- 修正后：均衡从协议诞生的第一刻就存在（静态占优）

但这也带来了新的问题：
1. **模型过于简单**——$\Delta > 0$ 在几乎所有合理参数下成立，使得博弈退化为"采纳是严格占优策略"的平凡博弈
2. **κ的战略作用被架空**——κ只在全体开发均衡条件中出现，而该条件在合理参数下从不成立
3. **λ的战略作用有限**——由于 $\Delta > 0 > -\lambda$，碎片化成本λ的大小不影响均衡存在性

**结论：** NPE在修正框架下成立，但博弈的策略深度被严重削弱。模型从最初的"策略性互动产生非扩散均衡"退化为"采纳是占优策略，均衡是平凡的"。这并不否定论文的政策结论（仍应采纳现有协议），但它质疑了"博弈论提供了对NPE的深刻洞见"这一声称——任何满足 $c^{\text{develop}} > c^{\text{adopt}}$ 和 $V[\theta(|\mathcal{E}|)] > V[\theta(0)]$ 的模型都会产生同样的结论。

---

## 5. 修正建议：恢复策略深度

为使博弈恢复有意义的策略互动，建议以下一项或多项修改：

### 5.1 引入异质性开发成本

假设各辖区有不同的 $c_i^{\text{develop}}$（如大国开发成本低、小国开发成本高）。则对于部分辖区，$\Delta_i(|\mathcal{E}|) < 0$ 可能成立，使得这些辖区有偏离激励。

### 5.2 引入κ的采纳者成本

若采纳者也承担κ（逻辑：即使采纳现有协议，其他辖区的开发行为仍造成标准混乱），则：

$$\pi_i(A, a_{-i}) = V[\theta(|\mathcal{E}|)] - c^{\text{adopt}} - \kappa \cdot n_D^{\text{other}} - \lambda \cdot \mathbb{I}$$

这将使κ不总是抵消，恢复策略互动。

### 5.3 引入不完全信息

若 $c_i^{\text{develop}}$ 为私人信息，则存在贝叶斯-纳什均衡，其中 $\Delta$ 的临界值不再是确定性的。这将产生非平凡的均衡选择问题。

### 5.4 序贯行动

若辖区序贯决策而非同时行动，则可出现先行者优势、信号传递和信息级联，产生比同时行动博弈更丰富的均衡结构。

---

## 6. 错误溯源表

| 错误编号 | 原论文位置 | 错误描述 | 修正 | 严重性 |
|---------|-----------|---------|------|--------|
| E1 | 定理1(ii), line 208 | 全体采纳条件 $\Delta \geq \lambda - \kappa$ | $\Delta \geq -\lambda$ | 🔴 致命 |
| E2 | 定理1证明, line 247 | 代数变换 $\Delta+\kappa \geq \kappa-\lambda+\kappa$ | 应为 $\Delta \geq -\lambda$ | 🔴 致命 |
| E3 | 2人混合策略, line 507 | $p^* = (-\Delta_A - 2\kappa)/(\lambda-\kappa)$ | $(-\Delta-\kappa)/(\lambda-\kappa)$ | 🔴 致命 |
| E4 | N人混合策略, line 305 | $\Gamma = -\Delta(|\mathcal{E}|) + \lambda - 2\kappa$ | 见方程(N3)，无简单Γ形式 | 🔴 致命 |
| E5 | 定理2, line 336 | $\theta^*$ 表达式含 $-\kappa+\lambda-\kappa$ | 基于错误条件，需重建 | 🔴 致命 |
| E6 | κ定义, lines 134/461/517 | 三重矛盾定义 | 统一为"每开发者自含成本" | 🟡 严重 |
| E7 | N人扩展, lines 516-517 | 支付函数与2人矩阵不一致 | 统一后一致 | 🟡 严重 |
| E8 | 推论, line 356 | $M(|\mathcal{E}|) = \Delta - (\lambda - \kappa)$ | $M(|\mathcal{E}|) = \Delta + \lambda$ | 🟡 严重 |

---

## 7. 附录：完整推导链（独立验证用）

以下为从第一原理到所有结论的紧凑推导链，供独立验证。

### A. 支付结构

$$\pi_i(A, \mathbf{a}) = V[\theta(|\mathcal{E}|)] - c_A - \lambda \cdot \mathbb{I}[n_D > 0]$$

$$\pi_i(D, \mathbf{a}) = V[\theta(0)] - c_D - \kappa \cdot n_D^{\text{all}} - \lambda \cdot \mathbb{I}[n_D > 0]$$

其中 $n_D^{\text{all}} = \sum_j \mathbb{I}[a_j = D]$。

### B. 采纳优势

$$\Delta = \pi_i(A, \mathbf{A}_{-i}) - [V[\theta(0)] - c_D - \kappa]$$

$$= V[\theta(|\mathcal{E}|)] - V[\theta(0)] - (c_A - c_D) + \kappa$$

### C. 全体采纳NE

$$\pi_i(A, \mathbf{A}_{-i}) \geq \pi_i(D, \mathbf{A}_{-i})$$

$$V[\theta(|\mathcal{E}|)] - c_A \geq V[\theta(0)] - c_D - \kappa - \lambda$$

$$(\Delta + V[\theta(0)] - c_D - \kappa) \geq V[\theta(0)] - c_D - \kappa - \lambda$$

$$\Delta \geq -\lambda \quad \blacksquare$$

### D. 全体开发NE

$$\pi_i(D, \mathbf{D}_{-i}) \geq \pi_i(A, \mathbf{D}_{-i})$$

$$V[\theta(0)] - c_D - n\kappa - \lambda \geq V[\theta(|\mathcal{E}|)] - c_A - \lambda$$

$$V[\theta(0)] - c_D - n\kappa \geq \Delta + V[\theta(0)] - c_D - \kappa$$

$$\Delta \leq -(n-1)\kappa \quad \blacksquare$$

### E. 2人混合策略

$$\mathbb{E}[A] = V[\theta(|\mathcal{E}|)] - c_A - (1-p)\lambda$$

$$\mathbb{E}[D] = V[\theta(0)] - c_D - \kappa[p \cdot 1 + (1-p) \cdot 2] - \lambda$$

$$= V[\theta(0)] - c_D - \kappa(2-p) - \lambda$$

无差异：

$$V[\theta(|\mathcal{E}|)] - c_A - (1-p)\lambda = V[\theta(0)] - c_D - \kappa(2-p) - \lambda$$

$$V[\theta(|\mathcal{E}|)] - c_A - \lambda + p\lambda = V[\theta(0)] - c_D - 2\kappa + p\kappa - \lambda$$

$$V[\theta(|\mathcal{E}|)] - c_A + p\lambda = V[\theta(0)] - c_D - 2\kappa + p\kappa$$

$$\Delta + V[\theta(0)] - c_D - \kappa + p\lambda = V[\theta(0)] - c_D - 2\kappa + p\kappa$$

$$\Delta - \kappa + p\lambda = -2\kappa + p\kappa$$

$$\Delta + \kappa + p(\lambda - \kappa) = 0$$

$$p^* = \frac{-\Delta - \kappa}{\lambda - \kappa} \quad \blacksquare$$

---

**文件结束。** 本修正文件应替代原论文§3.1-§3.2（定理1-2及其证明），并与 `game_theory_review.md` 中的审查结论交叉验证。
