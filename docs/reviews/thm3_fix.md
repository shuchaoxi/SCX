# Thm3 偏好域构造补全：多标注者卷积方法

> 本文档针对 AA-Theorem (theorem_aa_alignment.tex) 中 AA.2 的 T3 条件验证缺口，
> 给出完整的偏好域双世界构造、分布等价证明、扩展独立性假设 A2′ 陈述及自审分析。
>
> 语言：中文 | 数学符号：SCX 框架约定

---

## 1. 问题诊断

### 1.1 缺口 G1：多标注者联合分布不匹配（AA.2，第 490–538 行）

当前精细化构造中：

- **World A（噪声世界）**：标注者条件独立于 $\tau_{\mathrm{true}}$，因此无条件联合分布携带
  $\eta$-依赖的相关结构：
  $$P_A(\tilde{\tau}_1=a_1,\dots,\tilde{\tau}_K=a_K) = \sum_{t\in\{0,1\}} \frac12 \prod_{j=1}^K\bigl[(1-\eta)\mathbf{1}_{[a_j=t]} + \eta\mathbf{1}_{[a_j=1-t]}\bigr]$$

- **World B（价值多元世界）**：标注者无条件独立同分布 $\mathrm{Bernoulli}(1/2)$：
  $$P_B(\tilde{\tau}_1=a_1,\dots,\tilde{\tau}_K=a_K) = \left(\frac12\right)^K$$

当 $K\geq 2$ 时，两个分布不同——World A 具有基于 $\tau_{\mathrm{true}}$ 的条件相关结构，
World B 为完全独立。**诚实暴击已明确承认此缺口**（第 536–538 行、第 609–649 行）。

### 1.2 缺口 G2：$S_{\mathrm{pref}}$ 匹配仅对特殊 $\eta$ 成立（第 474–487 行）

简化构造中：

$$S_{\mathrm{pref}}^{(A)}(x_0) = \frac12 - \eta,\qquad S_{\mathrm{pref}}^{(B)}(x_0) = \eta$$

仅当 $\eta = 1/4$ 时 $S_{\mathrm{pref}}^{(A)} = S_{\mathrm{pref}}^{(B)}$。**对一般 $\eta$ 不成立。**

### 1.3 缺口 G3：$K=1$ 退化为平凡情形（第 540–557 行）

"正确的 $K=1$ 构造"要求 $\pi=1/2$，导致 $S_{\mathrm{pref}}\equiv 0$，
退化为无信息情形——所有偏好的 Cercis 得分为零，无法应用于非平凡 RLHF 数据集。

### 1.4 结构性问题汇总

| 缺口 | 位置 | 现象 | 影响 |
|------|------|------|------|
| G1 | 490–538 | $K\!\geq\!2$ 联合分布不匹配 | 多标注者 RLHF 场景失效 |
| G2 | 474–488 | $S_{\mathrm{pref}}$ 仅 $\eta\!=\!1/4$ 匹配 | 一般噪声率下不成立 |
| G3 | 540–557 | $K\!=\!1$ 退化为 $S_{\mathrm{pref}}\!\equiv\!0$ | 失去实际意义 |

三个缺口的核心是同一结构性问题：**试图用"不同的因果生成过程"去匹配"相同的观测分布",
但未使用卷积/吸收技术——将所有不可观测差异折叠进等效噪声分布。**

---

## 2. 修复方案：卷积-多标注者方法

### 2.1 核心思想：从 CD-Theorem 学到的教训

CD-Theorem (theorem_cd_causal.tex) 的 World B 构造（第 386–420 行）使用了**卷积技术**：

$$\varepsilon' \sim \mathrm{Law}(\varepsilon + \beta \cdot z)$$

即：将 World A 中的"标签噪声 + 混杂信号"吸收为 World B 中的单一"等效噪声分布"。
World B 不需要分别建模 $\varepsilon$ 和 $z$，只需匹配它们的和的边际分布。

**在偏好域中的对应**：将 World A 中的"真实偏好 + 注释者噪声"吸收为 World B 中的单一
"人群价值混合分布"。这通过 **De Finetti 表示定理** 形式化。

### 2.2 形式化设定

令 $(\Omega, \mathcal{F}, P)$ 为承载所有随机变量的概率空间。
设提示空间 $\mathcal{X}$，每个 $x\in\mathcal{X}$ 有 $K\geq 1$ 个独立的偏好标注结果
$\tilde{\tau}_1,\dots,\tilde{\tau}_K \in \{0,1\}$。

**World A：噪声主导过程 $\mathcal{P}_A$**

1. **潜在真实偏好**：$\tau_{\mathrm{true}}(x) \in \{0,1\}$，$P(\tau_{\mathrm{true}}=1 \mid x) = p(x) \in [0,1]$
2. **标注者噪声**：每个标注者 $j\in\{1,\dots,K\}$ 独立地以概率 $1-\eta$ 报告 $\tau_{\mathrm{true}}$，
   以概率 $\eta$ 翻转：
   $$P(\tilde{\tau}_j = \tau_{\mathrm{true}} \mid \tau_{\mathrm{true}}, x) = 1-\eta,\qquad
     P(\tilde{\tau}_j = 1-\tau_{\mathrm{true}} \mid \tau_{\mathrm{true}}, x) = \eta$$
3. **噪声率**：$\eta \in [0, \tfrac12)$ 为全局常数，与 $\tau_{\mathrm{true}}$ 和 $x$ 独立
4. **联合分布**（记 $s = \sum_{j=1}^K \tilde{\tau}_j$）：
   $$P_A(\tilde{\tau}_1,\dots,\tilde{\tau}_K \mid x) = p(x) \cdot (1-\eta)^s \eta^{K-s}
     + (1-p(x)) \cdot \eta^s (1-\eta)^{K-s}$$

**World B：价值多元主导过程 $\mathcal{P}_B$（卷积版本）**

1. **人群价值混合分布**：定义 $[0,1]$ 上的概率测度 $G_x$：
   $$G_x = p(x) \cdot \delta_{1-\eta} + (1-p(x)) \cdot \delta_{\eta}$$
   其中 $\delta_a$ 为 $a$ 处的 Dirac 测度。
   **解释**：比例为 $p(x)$ 的人群"内在偏好倾向"为 $1-\eta$（强倾向 $y^+ \succ y^-$），
   比例为 $1-p(x)$ 的人群内在倾向为 $\eta$（弱倾向 $y^+ \succ y^-$）。

2. **独立价值采样**：每个标注者 $j$ 独立地从其价值分布中采样：
   $$\nu_j \sim G_x,\qquad \tilde{\tau}_j \mid \nu_j \sim \mathrm{Bernoulli}(\nu_j)$$

3. **联合分布**（对 $\nu_j$ 积分后）：
   $$P_B(\tilde{\tau}_1,\dots,\tilde{\tau}_K \mid x) = \int_{[0,1]} \nu^s (1-\nu)^{K-s} \, dG_x(\nu)$$

### 2.3 等价性证明

**定理 1（联合分布等价）**：$\forall K \geq 1, \forall x \in \mathcal{X}, \forall (a_1,\dots,a_K)\in\{0,1\}^K$：
$$P_A(\tilde{\tau}_1=a_1,\dots,\tilde{\tau}_K=a_K \mid x) = P_B(\tilde{\tau}_1=a_1,\dots,\tilde{\tau}_K=a_K \mid x)$$

**证明**：
对 World B，将 $G_x$ 的显式形式代入积分：

$$
\begin{aligned}
P_B(\tilde{\tau}_1=a_1,\dots,\tilde{\tau}_K=a_K \mid x)
&= \int_{[0,1]} \nu^{s} (1-\nu)^{K-s} \, dG_x(\nu) \\
&= p(x) \cdot \int \nu^{s} (1-\nu)^{K-s} \, d\delta_{1-\eta}(\nu)
   + (1-p(x)) \cdot \int \nu^{s} (1-\nu)^{K-s} \, d\delta_{\eta}(\nu) \\
&= p(x) \cdot (1-\eta)^{s} \eta^{K-s} + (1-p(x)) \cdot \eta^{s} (1-\eta)^{K-s} \\
&= P_A(\tilde{\tau}_1=a_1,\dots,\tilde{\tau}_K=a_K \mid x)
\end{aligned}
$$

其中第二个等号用到 Dirac 测度的积分性质：$\int f(\nu)\,d\delta_a(\nu) = f(a)$。
最后一个等号来自 World A 联合分布的显式表示（对 $\tau_{\mathrm{true}}$ 求和）。
$\square$

**定理 2（边际等价 → $S_{\mathrm{pref}}$ 等价）**：$\forall x \in \mathcal{X}$：
$$S_{\mathrm{pref}}^{(A)}(x) = S_{\mathrm{pref}}^{(B)}(x)$$

**证明**：
由定理 1，对任意单个标注者 $j$（$K=1$ 情形）：
$$
\begin{aligned}
P_A(\tilde{\tau}_j=1 \mid x) &= p(x)(1-\eta) + (1-p(x))\eta = p(x) + \eta - 2p(x)\eta \\
P_B(\tilde{\tau}_j=1 \mid x) &= \int \nu \, dG_x(\nu) = p(x)(1-\eta) + (1-p(x))\eta
\end{aligned}
$$

两者相等。因此：
$$S_{\mathrm{pref}}^{(A)}(x) = \bigl|P_A(\tilde{\tau}=1 \mid x) - \tfrac12\bigr|
  = \bigl|P_B(\tilde{\tau}=1 \mid x) - \tfrac12\bigr|
  = S_{\mathrm{pref}}^{(B)}(x)$$

对任意 $\eta \in [0,\tfrac12)$ 和任意 $p(x) \in [0,1]$ 成立。
**不再需要 $\eta = 1/4$ 或 $p(x) = 1/2$ 的特殊条件。**
$\square$

**定理 3（$S_{\mathrm{pref}}$ 经验分布等价）**：对 $n$ 个独立同分布样本 $\{(x_i, \tilde{\tau}_{i,1},\dots,\tilde{\tau}_{i,K})\}_{i=1}^n$，
经验分布 $\hat{P}_n(S_{\mathrm{pref}})$ 在 $\mathcal{P}_A$ 和 $\mathcal{P}_B$ 下同分布。

**证明**：由定理 1，对每个 $i$，$(x_i, \tilde{\tau}_{i,1},\dots,\tilde{\tau}_{i,K})$ 在两个世界下
同分布。$S_{\mathrm{pref}}(x_i)$ 是 $\tilde{\tau}_{i,1},\dots,\tilde{\tau}_{i,K}$ 的可测函数
（通过边际概率估计），因此 $S_{\mathrm{pref}}(x_i)$ 的分布也相同。
由样本独立性，整个 $n$ 元组 $(S_{\mathrm{pref}}(x_1),\dots,S_{\mathrm{pref}}(x_n))$ 在两个世界下同分布。
$\square$

### 2.4 构造的直观解释

| 要素 | World A（噪声） | World B（价值多元—卷积） |
|------|-----------------|--------------------------|
| **潜伏变量** | $\tau_{\mathrm{true}}$：客观真实偏好 | $G_x$：人群价值分布 |
| **生成机制** | $\tau_{\mathrm{true}}$ → 噪声翻转 → $\tilde{\tau}$ | $G_x$ → 独立采样 → $\tilde{\tau}$ |
| **$\eta$ 的角色** | 随机错误率 | 人群极端化程度（$1-\eta$ vs $\eta$ 价值的差异） |
| **$p(x)$ 的角色** | 真实偏好的先验概率 | 人群中"强倾向"的比例 |
| **观测分布** | 完全相同 | 完全相同 |
| **因果解释** | 噪声引起分歧 | 价值多元引起分歧 |

核心洞见：**同一个观测分布可以有两个等价的数学表示——一个用"信号+噪声"，
一个用"混合分布"——两者在观测层面不可区分。** 这恰好是 Theorem 3（老实人定理）的核心哲学。

---

## 3. 扩展独立性假设 A2′

### 3.1 CD-Theorem 中的 A2′

在 CD-Theorem（第 448–450 行）中：
> **A2′（扩展独立性）**：$\eta \perp (\varepsilon, z)$，即 Sprint 参数 $\eta$ 与
> （标签噪声 $\varepsilon$, 未观测混杂 $z$）联合独立。

该假设确保 $\eta$ 不携带关于 $\varepsilon$ 或 $z$ 的信息，从而使卷积构造中的
$\eta \perp \varepsilon'$（其中 $\varepsilon' = \varepsilon + \beta \cdot z$）成立。

### 3.2 偏好域中的 A2′

在偏好域中，A2′ 的自然对应为：

> **A2′（偏好域扩展独立性）**：
> $$\eta \perp (\tau_{\mathrm{true}}, z_{\text{pref}})$$
> 即偏好噪声率 $\eta$ 与（真实偏好方向 $\tau_{\mathrm{true}}$,
> 所有其他未观测的偏好相关变量 $z_{\text{pref}}$）联合独立。

**形式化陈述：**

设 $(\Omega, \mathcal{F}, P)$ 为概率空间。定义：
- $\eta: \Omega \to [0, \tfrac12)$：全局偏好噪声率（Sprint 噪声参数）
- $\tau_{\mathrm{true}}: \mathcal{X} \times \Omega \to \{0,1\}$：真实偏好方向随机场
- $z_{\text{pref}}: \mathcal{X} \times \Omega \to \mathbb{R}^m$：所有未观测的偏好相关变量
  （包括注释者背景、文化因素、语境特征等）

**假设 A2′（偏好域）**：对任意 Borel 集 $A, B, C$：
$$P(\eta \in A, \tau_{\mathrm{true}}(x) \in B, z_{\text{pref}}(x) \in C)
  = P(\eta \in A) \cdot P(\tau_{\mathrm{true}}(x) \in B, z_{\text{pref}}(x) \in C)$$

即 $\eta$ 的分布独立于 $(\tau_{\mathrm{true}}, z_{\text{pref}})$ 的联合分布。

**为什么需要 A2′？**

在卷积构造中，World B 的 $G_x$ 显式依赖于 $\eta$：
$$G_x = p(x) \cdot \delta_{1-\eta} + (1-p(x)) \cdot \delta_{\eta}$$

若 $\eta$ 与 $\tau_{\mathrm{true}}$（决定 $p(x)$）不独立，则 $G_x$ 在给定 $\eta$ 的条件分布
与边际分布不同，破坏了两世界联合分布等价的论证。

**A2′ 与现有假设的关系：**

- AA.1.4（Noise Independence，第 329 行）假设 $\eta \perp X$，这是 A2′ 的弱化版本
- A2′ 将其增强为 $\eta$ 不仅与特征 $X$ 独立，也与真实偏好和所有潜在混杂独立
- A2′ 与 CD-Theorem 的 A2′ 在结构上同构：两者都要求 Sprint 参数与所有"信号层"变量联合独立

**可验证性分析：**

A2′ 在经验上不可直接验证（因为 $\tau_{\mathrm{true}}$ 和 $z_{\text{pref}}$ 不可观测）。
但我们提供以下间接验证路径：

1. **设计保证**：若 $\eta$ 由独立于标注过程的全局策略确定（如固定预算约束下的采样率），
   则 A2′ 在设计层面成立
2. **统计检验**：若 $\eta$ 由自适应 Sprint 算法确定，可通过检验 $\eta$ 的条件分布
   是否随观察到的标注者一致性模式变化来间接评估 $\eta \perp \tau_{\mathrm{true}}$ 的近似程度
3. **敏感性分析**：若 $\eta$ 与 $\tau_{\mathrm{true}}$ 存在弱依赖
   $|\mathrm{Corr}(\eta, \tau_{\mathrm{true}})| \leq \delta$，
   两个世界的 KL 散度被 $\delta$ 控制，不可区分性结论在 $\delta \to 0$ 极限下恢复

---

## 4. 完整证明（卷积版本）

### 4.1 设定重述

令 $\mathcal{P}_A$ 和 $\mathcal{P}_B$ 如上节定义。审计者的信息集为
$$\mathcal{I}_{\text{audit}} = \{S_{\mathrm{pref}}(x_i)\}_{i=1}^n$$

其中 $S_{\mathrm{pref}}(x) = |\hat{P}(\tilde{\tau}=1 \mid x) - \tfrac12|$，
$\hat{P}$ 为基于 $K$ 个标注的经验比例。

审计者**不能**观测到 $\{\tilde{\tau}_{i,j}\}$ 的个体值或 $\eta$。

### 4.2 定理陈述（补全后的 T3 条件）

**定理（偏好域 T3 不可区分性——卷积版本）**：
在 A2′（扩展独立性）假设下，对任意仅通过 $\{S_{\mathrm{pref}}(x_i)\}_{i=1}^n$ 进行判定的
审计算法 $\mathcal{A}: \mathbb{R}^n \to \{\text{"noise"}, \text{"value"}\}$，
有：
$$\bigl|\mathbb{E}_{\mathcal{P}_A}[\mathcal{A}(\mathcal{I}_{\text{audit}}) = \text{"noise"}]
  - \mathbb{E}_{\mathcal{P}_B}[\mathcal{A}(\mathcal{I}_{\text{audit}}) = \text{"noise"}]\bigr|
  \leq \alpha + o_n(1)$$

其中 $\alpha$ 是 $\mathcal{A}$ 的显著性水平，$o_n(1) \to 0$ 当 $n \to \infty$。

**该结论对任意 $K \geq 1$ 和任意 $\eta \in [0, \tfrac12)$ 成立。**

### 4.3 证明（完整链式推导）

**Step 1：单点联合分布等价。**

由定理 1，对任意 $x \in \mathcal{X}$ 和任意 $K \geq 1$：
$$\mathcal{L}_{\mathcal{P}_A}\big(\tilde{\tau}_1,\dots,\tilde{\tau}_K \mid x\big)
  = \mathcal{L}_{\mathcal{P}_B}\big(\tilde{\tau}_1,\dots,\tilde{\tau}_K \mid x\big)$$

**Step 2：$S_{\mathrm{pref}}$ 逐点等价。**

$S_{\mathrm{pref}}(x)$ 是 $(\tilde{\tau}_1,\dots,\tilde{\tau}_K)$ 的可测函数
（通过 $\hat{P}(\tilde{\tau}=1 \mid x) = \frac{1}{K}\sum_{j=1}^K \tilde{\tau}_j$）。
由 Step 1 的分布等价性和可测函数的保持性：
$$\mathcal{L}_{\mathcal{P}_A}\big(S_{\mathrm{pref}}(x)\big)
  = \mathcal{L}_{\mathcal{P}_B}\big(S_{\mathrm{pref}}(x)\big), \quad \forall x \in \mathcal{X}$$

**Step 3：$n$ 个独立样本联合等价。**

给定 $n$ 个独立提示 $x_1,\dots,x_n \overset{\text{iid}}{\sim} P_X$，
每个 $x_i$ 有 $K$ 个独立标注。由 Step 1 和独立性：
$$\mathcal{L}_{\mathcal{P}_A}\big(\{\tilde{\tau}_{i,j}\}_{i=1,j=1}^{n,K}\big)
  = \mathcal{L}_{\mathcal{P}_B}\big(\{\tilde{\tau}_{i,j}\}_{i=1,j=1}^{n,K}\big)$$

因此 $S_{\mathrm{pref}}(x_1),\dots,S_{\mathrm{pref}}(x_n)$ 的联合分布也等价。

**Step 4：审计器输出等价。**

审计器 $\mathcal{A}$ 将 $\mathcal{I}_{\text{audit}} = \{S_{\mathrm{pref}}(x_i)\}$ 映射到
$\{\text{"noise"}, \text{"value"}\}$。由于 $\mathcal{A}$ 是 $\mathcal{I}_{\text{audit}}$ 的确定性函数，
输入分布等价 ⇒ 输出分布等价：
$$\mathcal{L}_{\mathcal{P}_A}\big(\mathcal{A}(\mathcal{I}_{\text{audit}})\big)
  = \mathcal{L}_{\mathcal{P}_B}\big(\mathcal{A}(\mathcal{I}_{\text{audit}})\big)$$

**Step 5：$o_n(1)$ 项的解释。**

Step 3 的精确相等在有限样本下成立，因为我们的构造保证了任意有限 $n$ 下的逐样本分布等价。
$o_n(1)$ 项仅出现在审计器使用渐近检验统计量（如基于经验分布的拟合优度检验）时，
由 Glivenko–Cantelli 定理的 $O_P(n^{-1/2})$ 收敛速率引入。
若审计器使用精确有限样本检验，$o_n(1) \equiv 0$。

**Step 6：功效边界。**

由 Step 4，对任意审计算法 $\mathcal{A}$：
$$\mathbb{E}_{\mathcal{P}_A}[\mathcal{A} = \text{"noise"}] = \mathbb{E}_{\mathcal{P}_B}[\mathcal{A} = \text{"noise"}]$$

因此：
$$\bigl|\mathbb{E}_{\mathcal{P}_A}[\mathcal{A} = \text{"noise"}]
  - \mathbb{E}_{\mathcal{P}_B}[\mathcal{A} = \text{"noise"}]\bigr| = 0 \leq \alpha + o_n(1)$$

这建立了比原定理陈述更强的结论：**两个世界在任意有限样本量下的精确不可区分性。**
$\square$

---

## 5. 自审分析（Self-Review）

### 5.1 修复是否解决了三个缺口？

| 缺口 | 状态 | 评注 |
|------|------|------|
| G1（$K\!\geq\!2$ 联合不匹配） | ✅ 已解决 | 卷积构造通过 De Finetti 表示定理使联合分布对任意 $K$ 精确匹配 |
| G2（$S_{\mathrm{pref}}$ 仅 $\eta\!=\!1/4$ 匹配） | ✅ 已解决 | $S_{\mathrm{pref}}$ 对任意 $\eta\in[0,1/2)$ 和任意 $p(x)\in[0,1]$ 匹配 |
| G3（$K\!=\!1$ 退化为 $S_{\mathrm{pref}}\!\equiv\!0$） | ✅ 已解决 | 不再需要 $\pi=1/2$ 的限制，$S_{\mathrm{pref}}$ 可取任意 $[0,1/2]$ 的值 |

### 5.2 构造的数学严格性

**优点：**

1. **精确等价而非渐近等价**：联合分布在任意有限 $n,K$ 下精确相等（非渐近 $o_n(1)$ 追加项），
   这比 CD-Theorem 中需要 $O(n^{-1/2})$ 校正项的构造更强

2. **测度论基础完整**：所有对象定义在统一的 $(\Omega, \mathcal{F}, P)$ 概率空间上，
   $G_x$ 作为 $[0,1]$ 上的概率测度由 Dirac 原子的凸组合严格定义

3. **De Finetti 定理的恰当应用**：两原子混合分布对应 De Finetti 表示中的极端情形
   （混合测度为有限支撑），此时可交换序列的表示定理退化为有限混合的显式公式

4. **与 AA.4 的一致性**：AA.4（Value–Noise Indistinguishability）在第 879–907 行
   已使用等价的参数匹配策略（$q_k = 1/2 \pm s$），我们的构造将其推广到多标注者
   联合分布，与 AA.4 的结构完全兼容

**潜在风险：**

1. **$G_x$ 的"价值多元"解释强度**：
   $G_x = p\delta_{1-\eta} + (1-p)\delta_{\eta}$ 仅使用两个 Dirac 原子。
   一个"真正"的价值多元世界通常有连续的价值分布（如 $\mathrm{Beta}(\alpha,\beta)$）。
   但定理只需存在某个价值多元世界与噪声世界不可区分——两个原子已足够。
   **这是 Theorem 3 的固有特征：不可区分性只需要存在性，不需要典型性。**

2. **$\eta$ 的全局常数假设**：
   构造假设 $\eta$ 对所有提示 $x$ 相同。若 $\eta = \eta(x)$ 随提示变化，
   需要 $G_x$ 随 $x$ 变化相应的参数。这不影响等价性论证，但 A2′ 需加强为
   $\eta(x) \perp (\tau_{\mathrm{true}}(x), z_{\text{pref}}(x))$ 逐点成立。

3. **标注者间独立性的现实性**：
   World B 中，标注者条件独立于 $\nu_j$。这等价于 World A 中标注者条件独立于
   $\tau_{\mathrm{true}}$ —— 两者的独立性结构完全相同。因此，对独立性的任何质疑
   在两个世界中是对称的。

### 5.3 A2′ 的可验证性边界

**不可验证的方面：**

- A2′ 涉及不可观测变量 $\tau_{\mathrm{true}}$ 和 $z_{\text{pref}}$，
  因此原则上不可直接检验
- 这与 CD-Theorem 的 A2′（$\eta \perp (\varepsilon, z)$）面临相同的可验证性问题：
  $\varepsilon$ 和 $z$ 同样是不可观测的

**可间接验证的方面：**

- 若 $\eta$ 来自固定策略（非自适应），A2′ 在设计层面成立
- 若审计者可以获取标注者元数据（如标注者 ID、标注时间），可检验 $\eta$ 的估计
  是否与元数据相关——相关性暗示 A2′ 的违反
- 这与 CD-Theorem 诚实暴击 C1（第 522–527 行）的论述一致：A2′ 是一个
  **假设前提**而非可验证结论，定理的严格性条件依赖于它的成立

### 5.4 与原始 T3 的关系

原始 SCX Theorem 3（噪声-难度不可区分）的核心构造是：

$$\text{World A: 标签噪声} \longleftrightarrow \text{World B: 样本固有困难}$$

我们的偏好域平移做了等价替换：
$$\text{World A: 标注噪声} \longleftrightarrow \text{World B: 价值多元主义}$$

数学结构保持为：**将 World A 的"信号 + 噪声"通过卷积/混合吸收为 World B 的"等效单一过程"。**

因此，本构造是 Theorem 3 在偏好域的严格推论，而非独立的新结果。

### 5.5 剩余开放问题

1. **连续价值分布的不可区分性**：若价值多元世界的 $G_x$ 具有连续支撑
   （如 Beta 分布），是否仍存在不可区分的噪声世界？答案可能是肯定的，
   但需要求解 Hausdorff 矩问题的非唯一性

2. **标注者间相关性的影响**：若 World B 中的标注者具有非平凡的聚类结构
   （价值聚类），AC-Theorem 和 HC-Theorem 可能提供区分信号

3. **$\eta$ 的自适应选择**：当 $\eta$ 由数据驱动的 Sprint 算法自适应确定时，
   A2′ 的系统性违反程度及其对不可区分性结论的影响需要定量分析

---

## 6. 对 theorem_aa_alignment.tex 的修改建议

### 6.1 需替换的第 474–557 行

将 AA.2 证明中的 T3 条件验证（World A/World B 构造部分，约第 474–557 行）替换为本
文档第 2–4 节的卷积-多标注者构造，包含：

1. **形式化设定**（§2.2）：$G_x$ 分布定义
2. **等价性证明**（§2.3）：三个定理的完整链式推导
3. **扩展独立性 A2′**（§3）：显式陈述和与 CD-Theorem 的关系
4. **结论更新**：从"仅 $K=1$ 且退化为 $S_{\mathrm{pref}}\equiv 0$"更新为
   "对任意 $K\geq 1$ 和任意 $\eta\in[0,1/2)$ 成立"

### 6.2 需更新的诚实暴击

将第 609–649 行的诚实暴击更新为反映卷积构造的新分析：

- 删除"K=1 限制"和"$\pi=1/2$ 退化"的批评
- 新增"A2′ 可验证性"的讨论（借鉴 CD-Theorem 的 C1 项）
- 新增"两原子混合分布 vs 连续价值分布"的哲学边界讨论
- 保留"价值-噪声互斥假设"和"相关性结构"的讨论

### 6.3 与 AA.4 的协调

AA.4（第 786–978 行）的独立双世界构造本质上与我们的卷积构造等价
（其 $q_k = 1/2 \pm s$ 是 $G_x$ 的另一种表达）。建议：
- AA.4 明确引用本修复的卷积-多标注者推广
- 在 AA.4 的诚实暴击中更新"$K=1$ 限制"的论述

---

## 7. 总结

本修复通过借鉴 CD-Theorem 的卷积技术，将偏好域 T3 构造从"条件苛刻的单标注者退化情形"
补全为"对任意标注者数量和任意噪声率精确成立的严格构造"。

核心贡献：

1. **卷积-多标注者方法**：通过 De Finetti 表示定理和两原子混合分布，
   证明 World A（噪声）和 World B（价值多元）在任意 $K$ 下产生完全相同的联合分布

2. **$S_{\mathrm{pref}}$ 对任意 $\eta$ 匹配**：消除 $\eta=1/4$ 的特殊条件约束

3. **A2′ 显式陈述**：将扩展独立性假设在偏好域中形式化，并给出可验证性分析

4. **自审通过**：构造在测度论层面严格，所有等价性为精确（非渐近）等价

**最终判断：补全后的证明经受住了审查。** 三个缺口均被填补，新构造的数学严格性
不低于 CD-Theorem 的对应部分，且提供了更强的精确等价保证。
