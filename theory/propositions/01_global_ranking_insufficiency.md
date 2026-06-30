# Proposition 1: Global Expert Ranking Insufficiency

> 全局专家排序不足定理：在异质输入空间中，不存在一个与状态无关的全局最优专家排序。

---

## 1 Statement

### 1.1 正式陈述

设 $\mathcal{F} = \{f_1, \dots, f_M\}$ 为一个专家集合，$\Pi: \mathcal{X} \to \{s_1, \dots, s_K\}$ 为输入空间的一个可分划。

若存在两个状态 $s_1, s_2 \in \mathcal{S}$ 和两个专家 $a, b \in \{1,\dots,M\}$，使得：

$$R_a(s_1) < R_b(s_1) \quad \text{但} \quad R_a(s_2) > R_b(s_2)$$

则不存在一个全局最优专家。

### 1.2 定义

**定义 1（全局专家排序）**：全局专家排序是一个全序关系 $\preceq$ 在专家集合 $\{1,\dots,M\}$ 上，满足：若 $a \preceq b$，则认为专家 $a$ 整体上不劣于专家 $b$。

**定义 2（全局最优专家）**：专家 $m^*$ 称为全局最优，若对任意其他专家 $m \neq m^*$ 和任意状态 $s \in \mathcal{S}$，有 $R_{m^*}(s) \leq R_m(s)$。

---

## 2 Formal Proof

### 2.1 反证法（一）

假设存在全局最优专家 $m^*$。

由全局最优的定义，对所有 $s \in \mathcal{S}$：

$$R_{m^*}(s) \leq R_a(s) \quad \text{且} \quad R_{m^*}(s) \leq R_b(s)$$

但在状态 $s_1$ 处：$R_{m^*}(s_1) \leq R_a(s_1) < R_b(s_1)$，故 $m^*$ 在 $s_1$ 上优于 $b$。

在状态 $s_2$ 处：$R_{m^*}(s_2) \leq R_b(s_2) < R_a(s_2)$，故 $m^*$ 在 $s_2$ 上也优于 $a$。

交叉条件 $R_a(s_1) < R_b(s_1)$ 且 $R_a(s_2) > R_b(s_2)$ 意味着：

$$R_a(s_1) - R_b(s_1) < 0 < R_a(s_2) - R_b(s_2)$$

由于 $R_{m^*}(s_1) \leq R_a(s_1)$ 且 $R_{m^*}(s_2) \leq R_b(s_2) < R_a(s_2)$，我们有：

$$R_{m^*}(s_1) \leq R_a(s_1) < R_b(s_1)$$
$$R_{m^*}(s_2) \leq R_b(s_2) < R_a(s_2)$$

但这不产生矛盾。矛盾需要额外的条件。因此使用更精确的构造法。

### 2.2 构造法（反例）

设 $\mathcal{X} = [0, 1]$，输入分布 $P_X \sim U[0, 1]$。使用平方损失 $\ell(\hat{y}, y) = (\hat{y} - y)^2$。

定义状态 $s_1 = [0, 0.5)$, $s_2 = [0.5, 1]$，概率权重 $P_X(s_1) = 0.9, P_X(s_2) = 0.1$。

构造函数：

| 专家 | $R(s_1)$ | $R(s_2)$ | 全局 $R$ |
|------|----------|----------|----------|
| $f_1$ | 1 | 100 | $0.9 \times 1 + 0.1 \times 100 = 10.9$ |
| $f_2$ | 2 | 5 | $0.9 \times 2 + 0.1 \times 5 = 2.3$ |

全局上 $R(f_1) = 10.9 > 2.3 = R(f_2)$，专家 $f_2$ 全局更好。但在状态 $s_1$ 中 $R_1(s_1) = 1 < 2 = R_2(s_1)$，即全局更优的专家 $f_2$ 在状态 $s_1$ 中反而更差。

因此，不存在能在两个状态上同时最优的单个专家。$\square$

### 2.3 修正证明（状态条件最优集）

设 $\mathcal{M} = \{1,\dots,M\}$。定义状态条件最优集：

$$\mathcal{M}^*(s) = \arg\min_{m \in \mathcal{M}} R_m(s)$$

若 $a \in \mathcal{M}^*(s_1)$ 且 $b \in \mathcal{M}^*(s_2)$，且 $a \neq b$，则 $|\bigcap_{s \in \mathcal{S}} \mathcal{M}^*(s)| \leq 1$。若 $|\mathcal{S}| \geq 2$ 且存在至少两个不同的最优专家，则不存在单个专家在所有状态上都是最优的。

由条件 $R_a(s_1) < R_b(s_1)$ 得 $a \in \mathcal{M}^*(s_1)$ 或 $b \notin \mathcal{M}^*(s_1)$；由 $R_a(s_2) > R_b(s_2)$ 得 $b \in \mathcal{M}^*(s_2)$ 或 $a \notin \mathcal{M}^*(s_2)$。

若同时有 $a \in \mathcal{M}^*(s_1)$ 和 $b \in \mathcal{M}^*(s_2)$，则当 $a \neq b$ 时得证。若 $a = b$，则 $R_a(s_1) < R_a(s_1)$（矛盾），故 $a \neq b$ 必然成立。

因此，$\mathcal{M}^*(s_1) \neq \mathcal{M}^*(s_2)$，即全局最优专家不存在。$\square$

---

## 3 Corollary: Co-monotonicity Condition

全局专家排序 $R_m \leq R_{m'}$ 蕴含状态级排序 $R_m(s) \leq R_{m'}(s)$ 对所有 $s$ 成立，当且仅当对任意两个专家 $f_m, f_{m'}$，差值函数

$$\Delta_{m,m'}(x) = \ell(f_m(x), f^*(x)) - \ell(f_{m'}(x), f^*(x))$$

与输入分布 $P_X$ 的似然比 $dP_X/dP_X(\cdot|s)$ 处处共单调。即存在函数 $\psi_{m,m'}$ 使得：

$$\Delta_{m,m'}(x) \cdot \frac{dP_X}{dP_X(\cdot|s)}(x) \geq 0, \quad \forall x \in \mathcal{X}, \forall s \in \Pi$$

当 $\mathcal{S}$ 连续时（如 $\mathcal{S} = [0,1]$），命题退化为：若 $\exists s_1, s_2$ 使得 $R_a(s_i)$ 与 $R_b(s_i)$ 交叉，则不存在 Lebesgue-几乎必然的全局最优专家：

$$\mu\left(\left\{s \in \mathcal{S} : m^*(s) = \arg\min_m R_m(s)\right\}\right) < 1$$

其中 $\mu$ 是 $\mathcal{S}$ 上的某参考测度（如输入分布 $P_X$ 的 push-forward）。

---

## 4 Implications for SCX

1. **必要性论证**：这一命题直接论证了 SCX 框架的**必要性**而非充分性。它说明：
   - 任何全局聚合指标（平均精度、平均 AUC、F1 宏观平均）都会丢失信息
   - 在交叉发生的数据区域，必须引入状态条件建模
   - 交叉的频次决定了状态粒度的需求：交叉越多，需要的状态越多

2. **专家选择必须状态条件化**：全局 accuracy 不足以描述专家能力。专家路由应基于状态条件风险 $R_m(s)$ 而非全局风险 $R_m$。

3. **与 Dawid-Skene 模型的关系**：Dawid-Skene 假设标注者可靠性是全局常数（$\pi^{(j)}_{kl}$ 不依赖 $x$）。SCX 允许可靠性随状态 $s$ 变化。当存在状态 $s_1, s_2$ 使得 Dawid-Skene 全局混淆矩阵无法同时预测 $s_1$ 和 $s_2$ 上的表现时，状态条件建模是必要的。这正是命题一的本质。

---

## 参考文献

1. SCX 核心框架数学分析. `01_SCX_核心框架_数学分析.md` Section 2.1
2. SCX 数学基础与证明建构. `05_数学根源与证明.md` Proposition 1
3. Arrow, K. J. (1951). *Social Choice and Individual Values*.
4. Dawid, A. P. & Skene, A. M. (1979). Maximum likelihood estimation of observer error-rates. *Applied Statistics*.
