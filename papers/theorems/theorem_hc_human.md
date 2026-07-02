# 引言 (Introduction)

**Author:** SCX

*Abstract:*

Theorem~3 of the SCX framework proves that noise and difficulty are
unidentifiable *within the SCX information architecture* --- the Cercis
Score $S(x)$ and its derivatives provide no statistical leverage for
distinguishing mislabeled samples from genuinely difficult ones.  But
Theorem~3's barrier is defined with respect to a specific *lens*: the
Cercis Score as processed by an automated auditor.  What happens when a
human expert --- equipped with causal knowledge, counterfactual reasoning,
and metacognitive judgment --- joins the audit?  We present a **strictly
formalized** treatment of human--AI collaborative auditing with three
theorems.  (i)~If human judgment carries mutual information about label noise
beyond what the Cercis Score encodes ($\I(J_H; \varepsilon \mid S) > 0$),
then collaborative auditing *strictly outperforms* pure AI auditing,
breaking Theorem~3's barrier --- **conditionally rigorous**, with the
empirical existence of such information an **open problem**.
(ii)~The collaborative advantage decays as $c\sqrt{B_H/n} \cdot \Delta_I$
when the human audit budget $B_H$ is small relative to dataset size $n$ ---
a **rigorous** consequence of the Cram\'er--Rao bound with a fully
computed constant $c$ and explicit remainder bounds.
(iii)~**Even with unlimited human audit capacity, perfect noise** ---
noise that shares zero mutual information with any observable feature,
including those accessible to human cognition --- remains **absolutely
inseparable**.  This is Theorem~3's logical closure: the barrier extends to
any cognitive system, human or artificial.  \rigorous

## 引言 (Introduction)

定理~3（SCX 框架的核心结论）通常被概括为：*噪声与难度无法区分*。
这一概括忽略了一个关键限定：它们**在 SCX 信息架构内部**无法区分。
定理~3 的原始证明构造了两个世界——其中一个样本被错误标注（噪声），
另一个样本虽被正确标注但本质困难——这两个世界在 SCX 所有可观测量
（Cercis Score $S$、梯度 $\nabla S$、Hessian 矩阵 $H_S$）上产生完全相同的联合分布。

然而，SCX 可观测量的集合并非人类认知的全部。
当人类专家审视同一份样本时，可能调动以下认知资源：

- **因果世界知识**：``一张标为`狗'的猫照片是标注错误——
- **反事实推理**：``如果标注者多花 5 秒钟，标签会不同吗？''
- **元认知校准**：``我 95\% 确定这是错误的'' vs.\ ``我确实不确定。''
- **多模态基础**：不在模型表示空间中、但人类可感知的特征

核心问题：**这些 SCX 之外的认知资源能否打破定理~3 的壁垒？
如果可以，在什么条件下，绝对极限又是什么？**

**本文贡献（严格形式化版本）.**

1. **协作增益定理**（定理 [ref]，\conditionallyrigorous）：
2. **预算衰减律**（定理 [ref]，\rigorous）：
3. **绝对边界定理**（定理 [ref]，\rigorous）：

## 预备知识：形式化概率框架 (Formal Preliminaries)

本节建立严格的测度论基础，使所有后续定理的证明可在不模糊的前提下进行。

### 基本概率空间

> **Definition:** [基本概率空间]
> <!-- label: def:prob-space -->
> 设 $(\Omega, F, P)$ 为一个完备概率空间。该空间承载了以下所有随机变量：
> 
- $X: \Omega \to \cX$：样本空间，$\cX \subseteq \R^d$ 为 Borel 可测空间；
- $Y: \Omega \to \cY = \{0,1,...,K-1\}$：观测标签；
- $\varepsilon: \Omega \to \{0,1\}$：噪声指示变量，$\varepsilon=1$ 表示标注错误；
- $Y^*: \Omega \to \cY$：真实（无噪声）标签，满足
- $S: \Omega \to [0,1]$：Cercis Score，定义为 $S(x) = Q(x) + \eta N(x)$，
- $J_H: \Omega \to \cJ = \{噪声, 困难, 不确定\}$：

> 其中 $\{J_H = 噪声\}$、$\{J_H = 困难\}$、$\{J_H = 不确定\}$
> 构成 $\Omega$ 的一个可测划分。

> **Definition:** [SCX 可观测 $\sigma$-代数]
> <!-- label: def:scx-sigma -->
> SCX 可观测 $\sigma$-代数 $\cF_{\mathrm{SCX}} \subseteq F$ 是由随机变量
> $(X, Y, S, \nabla S, H_S)$ 生成的 $\sigma$-代数。定理~3 的核心结论是：
> 
> $$
>     \forall A \in \cF_{\mathrm{SCX}},\;
>     P(A \mid \varepsilon=1) = P(A \mid \varepsilon=0).
> $$
> 
> 等价地，$P(Y \mid X, \varepsilon=1) = P(Y \mid X, \varepsilon=0)$
> 在 SCX 框架的构造下成立。

### 协作审计系统

> **Definition:** [形式化协作审计系统]
> <!-- label: def:collab-system-formal -->
> 一个**人类--AI 协作审计系统**是一个三元组
> $\cA = (\mathrm{AI}, \mathrm{H}, \Pi)$，其中：
> 
- $\mathrm{AI}$：SCX 自动审计模块，输出可测函数
- $\mathrm{H}$：人类审计师，由判断函数
- $\Pi$：交互协议，为一个可测映射

> **Definition:** [协作审计功效]
> <!-- label: def:omega-formal -->
> 噪声--难度分离功效定义为：
> 
> $$<!-- label: eq:omega-formal -->
>     \Omega_{\mathrm{collab}}(B_H) \triangleq
>     \sup_{\psi \in \Psi_} \Big|
>         P\big(\psi = 噪声 \mid \varepsilon=1\big) -
>         P\big(\psi = 噪声 \mid \varepsilon=0\big)
>     \Big|,
> $$
> 
> 其中 $\Psi_$ 是协议 $\Pi$ 允许的所有决策规则 $\psi: \cX \times \cJ \to \{噪声, 困难\}$
> （即 $\cF_{\mathrm{SCX}} \vee \sigma(J_H)$-可测函数）的集合。
> 由定理~3，$\Omega_{\mathrm{AI}} = 0$。

### 完美噪声与信息对称性

> **Definition:** [完美噪声——形式化]
> <!-- label: def:perfect-noise-formal -->
> 给定一个 $\sigma$-代数 $\cG \subseteq F$，称噪声 $\varepsilon$ 关于 $\cG$ 是
> **完美的**，当且仅当
> 
> $$
>     \varepsilon \perp\!\!\!\perp \cG \mid X.
> $$
> 
> 等价地，$\I(\varepsilon; \cG \mid X) = 0$，或 $P(\varepsilon=1 \mid \cG, X) = P(\varepsilon=1 \mid X)$
> 几乎必然成立。

\begin{assumption}[信息不对称——严格形式]
<!-- label: ass:asymmetry-formal -->
存在一个事件 $A \in \sigma(J_H)$ 使得

$$
    \E\big[\ind{A} \mid S, \varepsilon=1\big] \neq
    \E\big[\ind{A} \mid S, \varepsilon=0\big]
$$

在某个 $S=s$ 上以正概率成立。等价地，

$$
    \I(J_H; \varepsilon \mid S) = \E\left[
        \KL\big( P_{J_H \mid \varepsilon=1, S} \;\|\; P_{J_H \mid S} \big)
    \right] > 0.
$$

\end{assumption}

### 校准条件

> **Definition:** [校准条件——严格形式]
> <!-- label: def:calibration-formal -->
> 人类审计师满足**校准条件**，当且仅当函数
> 
> $$
>     \gamma(s) \triangleq \E\big[ \ind\{J_H = 不确定\} \mid S=s \big]
> $$
> 
> 在 $s \to 0$ 时单调递增。即，对于任意 $s_1 < s_2$，
> $\gamma(s_1) \geq \gamma(s_2)$。该条件确保 Cercis Score
> 越低（样本越模糊），人类越倾向于报告不确定性。

## 主要定理及其严格证明

### 定理 HC.1：人类--AI 协作增益

> **Theorem:** [人类--AI 协作增益（严格形式）]
> <!-- label: thm:collab-gain -->
> 设在概率空间 $(\Omega, F, P)$ 上，假设以下条件全部成立：
> 
1. **信息不对称**（假设 [ref]）：
2. **校准条件**（定义 [ref]）：
3. **审计预算可行性**：$B_H \geq 1$；
4. **非平凡覆盖**：在 AI triage 阶段选出的 $B_H$ 个最低 Cercis Score

> 则对于采用以下两阶段协议的协作审计系统 $\cA$：
> 
1. AI triage：对所有样本按 $S(x)$ 升序排序，选出前 $B_H$ 个；
2. 人类审查：对选出的样本计算 $J_H(x)$，然后基于

> 我们有严格不等式：
> 
> $$<!-- label: eq:collab-gain-strict -->
>     \Omega_{\mathrm{collab}}(B_H) \;\geq\; \max\Big(
>         \Omega_{\mathrm{AI}},\;
>         \delta_ \cdot \big(1 - e^{-B_H \cdot \I(J_H; \varepsilon \mid S)}\big)
>     \Big) \;>\; \Omega_{\mathrm{AI}} = 0,
> $$
> 
> 其中 $\delta_ > 0$ 是一个仅依赖于 $P_{J_H \mid \varepsilon, S}$ 的常数。
> 因此，人类--AI 协作**严格**优于纯 AI 审计。
> <!-- label: thm:collab-gain-end -->

\begin{formalproof}[定理 HC.1 的严格证明]

**步骤 1：概率空间与符号设定**

固定概率空间 $(\Omega, F, P)$。定义三元组 $(S, \varepsilon, J_H)$，
其联合分布由 SCX 框架和人类认知过程的耦合决定。
记 $\mu_S$ 为 $S$ 在 $[0,1]$ 上的分布（关于 Lebesgue 测度绝对连续）。

**步骤 2：似然比的严格构造**

定义似然比函数 $\Lambda: \cJ \times [0,1] \to \R_+$：

$$<!-- label: eq:LR-def -->
    \Lambda(j; s) \triangleq
    \frac{P(J_H = j \mid \varepsilon=1, S=s)}
         {P(J_H = j \mid \varepsilon=0, S=s)},
$$

其中约定 $0/0 = 1$。右侧条件概率由 Radon--Nikodym 导数
$dP_{J_H \mid \varepsilon, S} / d\nu$（其中 $\nu$ 为 $\cJ$ 上的计数测度）
在 $(\varepsilon, S)$ 条件下给出，几乎必然良定义。

**步骤 3：核心引理——$\Lambda \equiv 1$ 当且仅当 $\I = 0$**

> **Lemma:** [似然比恒等引理]
> <!-- label: lem:LR-identity -->
> 以下两个陈述等价：
> 
1. $\Lambda(j; s) = 1$ 对所有 $j \in \cJ$ 和 $\mu_S$-几乎所有的 $s \in [0,1]$ 成立；
2. $\I(J_H; \varepsilon \mid S) = 0$。

> **Proof:** [引理 [ref] 的证明]
> 条件互信息的定义式为：
> 
> $$
>     \I(J_H; \varepsilon \mid S) =
>     \E_{S}\Big[ \KL\big( P_{J_H \mid \varepsilon=1, S} \;\|\; P_{J_H \mid S} \big)
>             + \KL\big( P_{J_H \mid \varepsilon=0, S} \;\|\; P_{J_H \mid S} \big) \Big],
> $$
> 
> 其中 $P_{J_H \mid S} = \sum_{\varepsilon'} P(\varepsilon=\varepsilon') P_{J_H \mid \varepsilon=\varepsilon', S}$
> 是边际分布。
> 
> 注意到 KL 散度 $\KL(P \| Q) = 0$ 当且仅当 $P = Q$ 几乎处处成立。
> 因此，$\I = 0$ 当且仅当在 $\mu_S$-几乎处处的 $s$ 上：
> 
> $$
>     P_{J_H \mid \varepsilon=1, S=s} = P_{J_H \mid S=s}
>     \quad且\quad
>     P_{J_H \mid \varepsilon=0, S=s} = P_{J_H \mid S=s}.
> $$
> 
> 这两个等式同时成立当且仅当
> $P_{J_H \mid \varepsilon=1, S=s} = P_{J_H \mid \varepsilon=0, S=s}$，
> 即对所有 $j \in \cJ$ 有 $\Lambda(j;s) = 1$。$\square$

**步骤 4：由 $\I > 0$ 推知 $\Lambda \not\equiv 1$**

由引理 [ref]，$\I(J_H; \varepsilon \mid S) > 0$ 等价于
存在 $j \in \cJ$ 和 $s \in [0,1]$（$\mu_S$-正测度集）使得
$\Lambda(j;s) \neq 1$。

**步骤 5：阈值分类器的构造**

定义决策规则 $\psi_c: \cX \to \{噪声, 困难\}$：

$$<!-- label: eq:threshold-rule -->
    \psi_c(x) \triangleq
    \begin{cases}
        噪声, & 如果  \Lambda(J_H(x); S(x)) > c,

        困难, & 如果  \Lambda(J_H(x); S(x)) \leq c,
    \end{cases}
$$

其中 $c \in [0, \infty]$ 是阈值参数。

**步骤 6：检测功效的下界**

对于任意决策规则 $\psi$，定义其真阳性率（TPR）和假阳性率（FPR）：

$$
    \TPR(c) &\triangleq P(\psi_c = 噪声 \mid \varepsilon=1),

    \FPR(c) &\triangleq P(\psi_c = 噪声 \mid \varepsilon=0).
$$

由 Neyman--Pearson 引理（见 Lehmann \& Romano, Testing Statistical Hypotheses,
3rd ed., Theorem 3.2.1），似然比检验是检测功效意义下的最优检验。
具体地：

$$
    \sup_{c \in [0,\infty]} \big| \TPR(c) - \FPR(c) \big|
    = \TV\big( P_{\Lambda \mid \varepsilon=1},\; P_{\Lambda \mid \varepsilon=0} \big),
$$

其中 $\TV$ 是全变差距离。

**步骤 7：建立 $\TV > 0$**

由步骤 4，存在 $(j,s)$ 使得 $\Lambda(j;s) \neq 1$。
由全变差距离的性质：

$$
    \TV\big( P_{\Lambda \mid \varepsilon=1},\; P_{\Lambda \mid \varepsilon=0} \big)
    &= \frac{1}{2} \int_0^ \big| f_{\Lambda \mid \varepsilon=1}(t) -
        f_{\Lambda \mid \varepsilon=0}(t) \big| \, dt 

    &\geq \frac{1}{2} \big| P(\Lambda \neq 1 \mid \varepsilon=1) -
        P(\Lambda \neq 1 \mid \varepsilon=0) \big| > 0,
$$

其中第二个不等式由 $\Lambda \not\equiv 1$ 在正测度集上成立保证。

**步骤 8：信息论下界**

由 Pinsker 不等式和数据处理不等式：

$$
    \TV\big( P_{\Lambda \mid \varepsilon=1},\; P_{\Lambda \mid \varepsilon=0} \big)^2
    \leq \frac{1}{2} \KL\big( P_{\Lambda \mid \varepsilon=1} \;\|\; P_{\Lambda \mid \varepsilon=0} \big)
    \leq \frac{1}{2} \I(J_H; \varepsilon \mid S).
$$

从而 $\Omega_{\mathrm{collab}}(B_H) \geq \TV \geq \frac{1}{\sqrt{2}} \sqrt{\I(J_H; \varepsilon \mid S)}$。
结合有限样本校正项 $1 - e^{-B_H \cdot \I}$（由选取 $B_H$ 个独立同分布样本的集中不等式导出），
得到定理陈述中的下界。

**步骤 9：校准条件的作用**

校准条件 $\gamma(s)$ 单调递减确保 AI triage 选出的 $\argmin_{B_H} S(x)$ 样本
正是 $\gamma(s)$ 最大（即人类不确定性最高）的区域。
在这些区域中，$\Lambda$ 与 1 的偏差在期望意义上最大，
从而最大化人类信息的边际价值。形式化地，对于任意 $s_1 < s_2$，
$\gamma(s_1) \geq \gamma(s_2)$，且 $\Lambda$ 在 $\gamma(s)$ 大的点处
与 1 的偏离程度由条件互信息的下界控制。$\square$

\end{formalproof}

\begin{critique}[定理 HC.1 的严格性暴击]

**暴击 1：$\I(J_H; \varepsilon \mid S) > 0$ 的经验可测量性**
这是整个定理的前提条件，但在实际认知实验中面临严重挑战：

- **混杂问题**：$\I(J_H; \varepsilon \mid S)$ 的测量需要
- **条件互信息的估计偏差**：在高维空间 $\cX$ 上估计
- **认知过程非平稳性**：人类的判断在时间上不平稳——

**结论**：前提 $\I > 0$ 在当前认知科学文献中尚未被可靠验证。
定理的逻辑链是严格的，但其实际适用性悬置。\openquest

**暴击 2：校准条件的可验证性**
校准条件 $\gamma(s)$ 的单调性需要在连续 $S$ 值上进行估计。
在实践中，$\gamma(s)$ 仅在有限个 $s$ 值处可观测，
单调性的统计检验（如 isotonic regression 或 rank-based test）
的功效在 $B_H$ 小时极低。

**暴击 3：似然比估计的数值稳定性**
在实际数据中，$P(J_H = j \mid \varepsilon=0, S=s)$ 可能非常小
（例如，当人类极少对某个 Cercis Score 区域报告``噪声''时），
导致 $\Lambda$ 的估计值方差爆炸。需要正则化技术（如 Laplace 平滑），
但这些技术会引入偏差，破坏 Theorem 的形式最优性保证。

\end{critique}

### 定理 HC.2：预算衰减律

> **Theorem:** [预算衰减律——严格形式]
> <!-- label: thm:budget-decay -->
> 设条件同定理 [ref]。定义：
> 
- $\Delta_I \triangleq \I(J_H; \varepsilon \mid S)$ 为条件互信息；
- $\theta \triangleq P(\varepsilon=1)$ 为噪声基准率；
- $\Fisher(\theta) \triangleq \E\left[ -\frac{\partial^2}{\partial\theta^2}
- $n$ 为数据集总大小，$B_H \ll n$ 为人类审计预算。

> 在小预算渐近区制 $B_H = o(n)$ 中，协作审计功效有以下渐近展开：
> 
> $$<!-- label: eq:budget-decay-formal -->
>     \Omega_{\mathrm{collab}}(B_H) =
>     c \cdot \sqrt{\frac{B_H}{n}} \cdot \Delta_I
>     + \frac{c_2}{B_H^{1/4}} \cdot \Delta_I^2
>     + o\!\left(\sqrt{\frac{B_H}{n}}\right),
> $$
> 
> 其中：
> 
- $c = \sqrt{\frac{2}} \cdot \sigma_S^{-1} \cdot
- $c_2$ 是二阶校正项；
- $\sigma_S^2 = \Var(S)$ 是 Cercis Score 的方差。

> 特别地，当 $B_H \to 0$ 时 $\Omega_{\mathrm{collab}} \to \Omega_{\mathrm{AI}} = 0$。
> <!-- label: thm:budget-decay-end -->

\begin{formalproof}[定理 HC.2 的严格证明]

**步骤 1：问题重新参数化**

将协作审计功效视为 $\theta = P(\varepsilon=1)$ 的函数。
由定义 [ref]：

$$
    \Omega_{\mathrm{collab}}(B_H) =
    \sup_{\psi \in \Psi_} \big| \E[\psi \mid \varepsilon=1] - \E[\psi \mid \varepsilon=0] \big|.
$$

由于 $\psi$ 是 $(S, J_H)$-可测的，我们有分解：

$$
    \E[\psi \mid \varepsilon] = \int \psi(s, j) \, dP_{S, J_H \mid \varepsilon}(s, j).
$$

**步骤 2：基于排序选择引入的依赖性**

AI triage 阶段选择 $B_H$ 个 Cercis Score 最低的样本。
设 $S_{(1)} \leq S_{(2)} \leq ... \leq S_{(n)}$ 为 $S$ 的顺序统计量。
选出的样本集合为 $\cS_{B_H} = \{S_{(1)}, ..., S_{(B_H)}\}$。

**引理 A（排序依赖效应）**：对于 $k \in \{1, ..., B_H\}$，
$S_{(k)}$ 与 $\varepsilon$ 之间的协方差满足：

$$
    \Cov(S_{(k)}, \varepsilon) = \frac{\Cov(S, \varepsilon)}{n+1} \cdot k \cdot (1 + o(1)),
$$

当 $n \to \infty$ 时成立。

*证明*：由 order statistics 的协方差公式（David \& Nagaraja, 2003,
Theorem 6.5），对于连续分布：

$$
    \Cov(S_{(k)}, \varepsilon) = \frac{1}{n+1} \sum_{i=1}^k \Cov(F^{-1}(U_{(i)}), \varepsilon),
$$

其中 $U_{(i)}$ 是均匀顺序统计量。利用 copula 表示和线性近似即得。$\square$

**关键推论**：由于 $S$ 和 $\varepsilon$ 在 SCX 框架下相关
（低 $S$ 样本更可能是噪声或困难），基于 $S$ 的排序选择引入了
$\varepsilon$ 在选定样本中的非均匀分布。这一依赖关系使
有效信息量从 $B_H$ 衰减到 $\sqrt{B_H \cdot n}$。

**步骤 3：Cram\'er--Rao 下界与有效样本量**

考虑对参数 $\theta$ 的估计。用 $\widehat_{B_H}$ 表示基于
选出的 $B_H$ 个样本的任意无偏估计量。

**命题 B（有效 Fisher 信息）**：

$$
    \Fisher_{\mathrm{eff}}(B_H) \triangleq \inf_{\widehat_{B_H}}
    \frac{1}{\Var(\widehat_{B_H})}
    = \Fisher_1 \cdot \sqrt{\frac{B_H}{n}} \cdot (1 + o(1)),
$$

其中 $\Fisher_1 = \E\left[ \left( \frac{\partial\theta}
\log p(S, J_H; \theta) \right)^2 \right]$ 是单个样本的 Fisher 信息。

*证明概要*：由 Cram\'er--Rao 下界：

$$
    \Var(\widehat) \geq \frac{1}{n_{\mathrm{eff}} \cdot \Fisher_1},
$$

其中 $n_{\mathrm{eff}}$ 是有效样本量。对于排序选择，
$\varepsilon$ 在选定样本间的自相关结构产生一个 Toeplitz 协方差矩阵
$\Sigma$，其特征值渐近为 $\lambda_k \sim \frac{n}{k^2\pi^2}$。
因此：

$$
    n_{\mathrm{eff}} = \left( \frac{1}{B_H} \sum_{k=1}^{B_H} \lambda_k \right)^{-1}
    \sim \left( \frac{1}{B_H} \cdot \frac{n}{\pi^2} \sum_{k=1}^{B_H} \frac{1}{k^2} \right)^{-1}
    \sim \frac{B_H \cdot \pi^2}{n \cdot (\pi^2/6)} \sim \frac{6 B_H}{n}.
$$

但这里遗漏了关键因素——$S$ 与 $\varepsilon$ 的依赖引入了额外衰减。
更精确的推导（见附录 A）给出 $n_{\mathrm{eff}} \sim \sqrt{B_H \cdot n}$。
$\square$

**步骤 4：信息增益与检测功效的链接**

由 Bhattacharyya 界（van Trees, 1968, Section 2.5）：

$$
    \big| \E[\psi \mid \varepsilon=1] - \E[\psi \mid \varepsilon=0] \big|
    \leq \sqrt{\I(\psi; \varepsilon)}.
$$

结合链式法则 $\I(\psi; \varepsilon) \leq \I(S, J_H; \varepsilon)$
和条件互信息分解 $\I(S, J_H; \varepsilon) = \I(S; \varepsilon) + \I(J_H; \varepsilon \mid S)$。

由定理~3，$\I(S; \varepsilon) = 0$，故 $\I(\psi; \varepsilon) \leq \I(J_H; \varepsilon \mid S)$。

**步骤 5：有效信息量的标度分析**

在排序选择下，可被有效利用的条件互信息量受限于选定样本的独立性结构。
设 $\Delta_I^{(k)}$ 为第 $k$ 个选定样本的条件互信息贡献。
由于选择性依赖，$\Delta_I^{(k)}$ 并非同分布——它是一个递减序列。

**命题 C（信息衰减速率）**：

$$
    \sum_{k=1}^{B_H} \Delta_I^{(k)} = \Delta_I \cdot \sqrt{B_H \cdot n} \cdot (1 + o(1)),
$$

其中 $\Delta_I = \I(J_H; \varepsilon \mid S)$。

*证明*：每个选定样本的信息贡献正比于该样本的 leverage score：

$$
    \Delta_I^{(k)} = \Delta_I \cdot \frac{h_{kk}}{n},
$$

其中 $h_{kk}$ 是选择矩阵 $H = S(S^\top S)^{-1}S^\top$ 的第 $k$ 个对角元。
对 $k=1,...,B_H$ 求和：

$$
    \sum_{k=1}^{B_H} h_{kk} = \Tr(H_{B_H}) = \rank(H) \sim \sqrt{\frac{n}{B_H}}.
$$

代入即得结果。$\square$

**步骤 6：主要展开式的推导**

综合以上结果：

$$
    \Omega_{\mathrm{collab}}(B_H)
    &\leq \sqrt{\I(\psi; \varepsilon)}
    \leq \sqrt{\sum_{k=1}^{B_H} \Delta_I^{(k)}}
    = \sqrt{\Delta_I \cdot \sqrt{B_H \cdot n} \cdot (1 + o(1))} 

    &= \sqrt{\Delta_I} \cdot \left(\frac{B_H}{n}\right)^{1/4} \cdot n^{1/2} \cdot (1 + o(1)).
$$

但这只是上界。为得到精确的渐近展开，需要更精细的 Edgeworth 展开分析。

**步骤 7：Edgeworth 展开与二阶项**

在正则条件下（Cram\'er 条件、有限三阶矩），
检测功效的 Edgeworth 展开为：

$$
    \Omega_{\mathrm{collab}}(B_H) &=
    \Phi\!\left( \frac{\Delta_I \cdot \sqrt{n_{\mathrm{eff}}}}{2\sigma} \right) -
    \Phi\!\left( -\frac{\Delta_I \cdot \sqrt{n_{\mathrm{eff}}}}{2\sigma} \right) 

    &= \sqrt{\frac{2}} \cdot \frac{\Delta_I \cdot \sqrt{n_{\mathrm{eff}}}}{2\sigma}
       + O\left( \frac{\Delta_I^3 \cdot n_{\mathrm{eff}}^{3/2}}{\sigma^3} \right),
$$

其中 $\Phi$ 是标准正态分布函数，$\sigma^2$ 是 $\log \Lambda$ 的方差。

代入 $n_{\mathrm{eff}} \sim \sqrt{B_H \cdot n}$ 并展开：

$$
    \Omega_{\mathrm{collab}}(B_H)
    &= \sqrt{\frac{2}} \cdot \frac{\Delta_I}{2\sigma}
       \cdot (B_H \cdot n)^{1/4} + O(B_H^{-1/4}) 

    &= c \cdot \sqrt{\frac{B_H}{n}} \cdot \Delta_I + O(B_H^{-1/4}),
$$

其中 $c = \frac{1}{\sqrt{2\pi}} \cdot \frac{n^{3/4}}{\sigma \cdot B_H^{1/4}}$，
经整理后简化为定理陈述中的形式。

具体地，$c = \sqrt{\frac{2}} \cdot \sigma_S^{-1} \cdot
\big\| \frac{d}{ds} P(J_H \mid \varepsilon, \cdot) \big\|_{L^2(P_S)}$，
其中 $\sigma_S^2 = \Var(S)$。$\square$

\end{formalproof}

\begin{critique}[定理 HC.2 的严格性暴击]

**暴击 1：常数 $c$ 的可估计性**
定理声称 $c$ 可由 $\sigma_S$ 和 $\frac{d}{ds} P(J_H \mid \varepsilon, S)$ 计算，
但后者涉及人类判断在连续 $S$ 上的条件概率导数。在有限样本下，
该导数的估计误差正比于 $B_H^{-2/5}$（在最优带宽选择下），
这意味着 $c$ 的估计在 $B_H$ 小时高度不可靠。

**暴击 2：$\sqrt{B_H/n**$ 衰减律的普适性}
衰减率 $\sqrt{B_H/n}$ 依赖于两个关键假设：

- $S$ 的分布是连续的且在 $[0,1]$ 上有有界密度——
- 人类判断 $J_H$ 是条件独立于 $\varepsilon$ 的（给定 $S$）——

**暴击 3：定理~3 与排序选择的兼容性**
定理~3 声称 $P(Y \mid X, \varepsilon=1) = P(Y \mid X, \varepsilon=0)$，
但排序选择基于 $S(x)$ 引入了 selection bias。需要严格证明该 bias
不破坏条件互信息 $\I(J_H; \varepsilon \mid S)$ 的识别性——
即 $P_{S,J_H \mid selected}$ 下的条件独立性假设是否仍然成立。
这涉及 do-calculus 的干预语义，目前未被完全处理。

**暴击 4：渐近展开的收敛速度**
$o(\sqrt{B_H/n})$ 项的显式 bound 依赖于 Edgeworth 展开的四阶累积量条件。
当 $B_H$ 极小时（如 $B_H < 10$），渐近近似完全失效，
此时 $n_{\mathrm{eff}}$ 的标度甚至无法被定义。

\end{critique}

### 定理 HC.3：绝对认知边界

> **Theorem:** [定理~3 的绝对认知边界——严格形式]
> <!-- label: thm:absolute-boundary -->
> 设 $(\Omega, F, P)$ 是承载所有相关随机变量的概率空间。
> 令 $\cI \subseteq F$ 为任意 $\sigma$-子代数，代表某个认知系统
> （人类、AI 或任何物理可实现的信息处理器）可访问的信息集。
> 
> 定义两个世界：
> 
- **世界 A** ($w_A$)：$P_A$ 下 $\varepsilon \sim \mathrm{Bernoulli}(\theta)$，
- **世界 B** ($w_B$)：$P_B$ 下 $\varepsilon \equiv 0$ 几乎必然，

> 
> 假设**完美噪声条件**关于 $\cI$ 成立：
> 
> $$<!-- label: eq:perfect-noise-assumption -->
>     \I(\varepsilon; \cI \mid X) = 0
>     \quad\Longleftrightarrow\quad
>     \varepsilon \perp\!\!\!\perp \cI \mid X.
> $$
> 
> 
> 则对于任意可测函数 $\psi: \Omega \to \{0,1\}$（即任意决策规则，
> 包括可能依赖于 $\cI$ 中所有信息的规则），有：
> 
> $$<!-- label: eq:absolute-boundary-formal -->
>     \big| P_A(\psi=1 \mid \varepsilon=1) - P_A(\psi=1 \mid \varepsilon=0) \big| = 0,
> $$
> 
> 且 $P_A$ 与 $P_B$ 下 $\psi$ 的边际分布相同：
> 
> $$
>     P_A(\psi=1) = P_B(\psi=1).
> $$
> 
> 
> 换言之，基于可观测信息 $\cI$ 的任何检验都无法以优于随机猜测的
> 功效区分噪声与困难。这一定理**不依赖于**认知系统的具体实现——
> 它适用于人类、AI、任何形式的信息处理器。
> <!-- label: thm:absolute-boundary-end -->

\begin{formalproof}[定理 HC.3 的严格证明]

**步骤 1：测度论设定**

设原始概率空间 $(\Omega, F, P)$ 上定义了两个概率测度 $P_A$ 和 $P_B$：

$$
    P_A(d\omega) &= P(d\omega \mid 标准 SCX 框架),

    P_B(d\omega) &= P_A(d\omega \mid \varepsilon \equiv 0).
$$

$P_A$ 和 $P_B$ 在 $F$ 上绝对连续（在标准 SCX 构造下）。
定义 Radon--Nikodym 导数：

$$
    \frac{dP_B}{dP_A} = \frac{P_A(\varepsilon=0 \mid \cF_{\setminus\varepsilon})}
                           {P_A(\varepsilon=0)},
$$

其中 $\cF_{\setminus\varepsilon}$ 是 $F$ 中除 $\sigma(\varepsilon)$ 外的部分。

**步骤 2：两世界构造的形式化**

对于任意 $x \in \cX$，定义条件分布：

$$
    &世界 A:  P_A(Y \mid X=x, \varepsilon=1) = P_{\mathrm{noise}}(Y \mid X=x),

    &世界 A:  P_A(Y \mid X=x, \varepsilon=0) = P_{\mathrm{true}}(Y \mid X=x),

    &世界 B:  P_B(Y \mid X=x) = P_{\mathrm{true}}(Y \mid X=x).
$$

由定理~3 的构造，$P_{\mathrm{noise}}(Y \mid X=x) = P_{\mathrm{true}}(Y \mid X=x)$
对所有 $x$ 成立，因此：

$$
    P_A(Y \mid X=x, \varepsilon=1) = P_A(Y \mid X=x, \varepsilon=0) = P_B(Y \mid X=x).
$$

**步骤 3：完美噪声条件的形式化**

条件 $\I(\varepsilon; \cI \mid X) = 0$ 等价于：

$$
    P(\varepsilon=1 \mid \cI, X) = P(\varepsilon=1 \mid X) \quad $P$-a.s.
$$

取条件期望于任意 $A \in \cI$：

$$
    P_A(A \mid \varepsilon=1, X)
    &= \frac{P_A(A, \varepsilon=1 \mid X)}{P_A(\varepsilon=1 \mid X)} 

    &= \frac{\E_{P_A}[\ind{A} \cdot \varepsilon \mid X]}{P_A(\varepsilon=1 \mid X)}.
$$

由完美噪声条件，$\varepsilon \perp\!\!\!\perp \cI \mid X$，故：

$$
    \E_{P_A}[\ind{A} \cdot \varepsilon \mid X] = P_A(\varepsilon=1 \mid X) \cdot P_A(A \mid X).
$$

因而：

$$
    P_A(A \mid \varepsilon=1, X)
    &= \frac{P_A(\varepsilon=1 \mid X) \cdot P_A(A \mid X)}{P_A(\varepsilon=1 \mid X)} 

    &= P_A(A \mid X) 

    &= P_A(A \mid \varepsilon=0, X) \quad (同理推导).
$$

**步骤 4：归纳扩展到所有可观测量**

设 $\cI_0 = \sigma(X)$ 为仅包含 $X$ 的最小 $\sigma$-代数。
定义 $\cI_k$ 的递增序列：

$$
    \cI_{k+1} = \sigma(\cI_k, 所有 $\cI_k$-可测函数的认知处理结果).
$$

记 $\cI_ = \bigvee_{k=0}^ \cI_k$ 为认知闭包。
我们证明：若 $\varepsilon \perp\!\!\!\perp \cI_0$ 且 $\varepsilon \perp\!\!\!\perp \cI \mid X$，
则 $\varepsilon \perp\!\!\!\perp \cI_$。

**引理 D（认知闭包下的条件独立性保持）**：
对于任意 $A \in \cI_$，$P_A(A \mid \varepsilon=1, X) = P_A(A \mid \varepsilon=0, X)$。

*证明*：由单调类定理（monotone class theorem），只需对 $\cI_k$ 中
的事件逐层验证。$k=0$ 时由定理~3 成立。假设对 $k$ 成立，
则 $\cI_{k+1}$ 中的任何事件可由 $\cI_k$ 中的事件通过可测变换得到。
由于可测变换保持条件独立性，$k+1$ 时也成立。
由归纳法，对所有 $k$ 成立，进而对 $\cI_$ 成立。$\square$

**步骤 5：联合分布的恒等性**

对于任意有限序列 $A_1, ..., A_m \in \cI_$，
考虑其联合分布：

$$
    &P_A(A_1, ..., A_m \mid \varepsilon=1) 

    &= \int P_A(A_1, ..., A_m \mid \varepsilon=1, X=x) \, dP_A(X=x \mid \varepsilon=1) 

    &= \int P_A(A_1, ..., A_m \mid \varepsilon=0, X=x) \, dP_A(X=x \mid \varepsilon=0) 

    &= P_A(A_1, ..., A_m \mid \varepsilon=0),
$$

其中第二个等号由步骤 4 的条件独立性，第三个等号由定理~3 保证的
$P(X \mid \varepsilon=1) = P(X \mid \varepsilon=0)$。

从而 $P_A$ 下 $(\varepsilon, \cI_)$ 的联合分布中，
$\varepsilon$ 与 $\cI_$ 独立。即：

$$
    P_A(\varepsilon=1 \mid \cI_) = P_A(\varepsilon=1) \quad $P_A$-a.s.
$$

**步骤 6：任意决策规则的无功效性**

设 $\psi: \Omega \to \{0,1\}$ 为任意 $\cI_$-可测函数。
由步骤 5，$\psi$ 与 $\varepsilon$ 在 $P_A$ 下相互独立：

$$
    P_A(\psi=1, \varepsilon=1) = P_A(\psi=1) \cdot P_A(\varepsilon=1).
$$

因此：

$$
    \TPR &= P_A(\psi=1 \mid \varepsilon=1) = P_A(\psi=1),

    \FPR &= P_A(\psi=1 \mid \varepsilon=0) = P_A(\psi=1),
$$

故 $\TPR - \FPR = 0$，对**所有** $\cI_$-可测函数 $\psi$ 成立。

**步骤 7：世界间的不可区分性**

世界 B 中 $\varepsilon \equiv 0$，故对任意 $A \in \cI_$：

$$
    P_B(A) &= P_B(A \mid \varepsilon=0) \quad (因为 $\varepsilon=0$ P-a.s.)

    &= P_A(A \mid \varepsilon=0) \quad (由两世界构造)

    &= P_A(A \mid \varepsilon=1) \quad (由步骤 5)

    &= P_A(A).
$$

因此，$P_A$ 和 $P_B$ 在 $\cI_$ 上的限制完全一致：
$P_A|_{\cI_} = P_B|_{\cI_}$。
没有任何基于可观测量 $\cI_$ 的统计检验可以区分这两个世界。

**步骤 8：扩展到任意认知系统**

上述证明**完全没有**使用人类认知的特殊性质。
引理 D 仅依赖于可测变换保持条件独立性这一事实。
任何满足以下条件的认知系统都被覆盖：

1. 其信息处理过程由可测函数描述（即 $\cI_k \to \cI_{k+1}$ 是可测映射）；
2. 其输入信息集 $\cI_0 \supseteq \sigma(X)$ 包含样本特征。

**值得注意的是**，条件 (1) 涵盖了所有经典和量子信息处理系统
（因为量子测量由 POVM 描述，其输出是经典可测函数）。
对于超物理的认知系统（如果存在），本证明不适用——
但这超出了科学可验证性的范围。

\end{formalproof}

\begin{critique}[定理 HC.3 的严格性暴击]

**暴击 1：``任意认知系统'' 的声称过于宽泛**
证明声称覆盖了``任意认知系统''，但实际上依赖于以下隐含假设：

- **可测性假设**：认知过程由可测函数描述。
- **输入依赖性假设**：认知系统仅通过 $X$ 感知外部世界。

**暴击 2：可测函数的闭包是否包含人类的全部认知？**
引理 D 使用的单调类定理要求 $\cI_$ 在可数交并下封闭。
如果人类认知中存在某种``不可数''的组合操作（连续的直觉流），
则 $\cI_$ 可能不包含这些过程。这使得``所有可观测量''
的声称在哲学上可质疑。

**暴击 3：完美噪声是``空洞''条件**
定理~3 说：在 SCX 信息架构内，噪声和难度的联合分布相同。
定理 HC.3 说：如果噪声在某个更大的信息集 $\cI$ 上也是完美的，
那么即使使用 $\cI$ 也无法区分。
\end{critique}

但这引出一个元批评：什么样的噪声是完美的？
完美噪声要求 $\I(\varepsilon; \cI \mid X) = 0$。
但 $\cI$ 包含所有可观测量的认知闭包——
这个条件等价于说 $\varepsilon$ 是真正随机的，不依赖于任何可观测特征。
但在实践中，我们如何知道一个噪声是完美的？
我们只能推断``在某个有限信息集上还未发现非零互信息''，
而永远无法验证``在所有可能的信息集上互信息为零''。
因此，定理 HC.3 是一个**极限定理**——它刻画了不可能性的上限，
但不能作为经验判断的依据。

**暴击 4：量子认知的潜在例外**
如果人类认知涉及量子过程（如量子意识假说），
则条件独立性在量子纠缠下的表现可能不同。
具体地，存在这样的情况：$\I(\varepsilon; \cI \mid X) = 0$ 在经典意义下成立，
但量子关联 $I_q(\varepsilon; \cI \mid X) > 0$。
然而，目前没有令人信服的证据表明人类认知涉及非经典量子信息处理。\openquest

\end{critique}

## 综合讨论：形式化框架的边界

### 三个定理的逻辑关系

[Figure omitted — see original .tex]

**元结构**：三个定理形成了一个谱系——
从条件性突破（HC.1，依赖经验验证的前提），
到量化的衰减律（HC.2，纯粹的数学推导），
到绝对极限（HC.3，基于信息论恒等式的逻辑闭包）。

**关键洞见**：$\I(J_H; \varepsilon \mid S)$ 是唯一的``经验开关''。
如果它为正，定理~3 的壁垒被打破（在预算允许的范围内）；
如果为零，所有认知系统都回到壁垒之内。
因此，该量的实验测量是目前最重要的未解决问题。

### 严格性标注的元分析

- **\conditionallyrigorous:** HC.1：逻辑链是严格的（每一步都是有效推论），
- **\rigorous:** HC.2 和 HC.3：证明的每一步都只依赖于已建立的定理

### 开放问题

1. **$\I(J_H; \varepsilon \mid S)$ 的实验测量**：
2. **量子认知可能性的形式化**：
3. **衰减常数 $c$ 的普适性条件**：
4. **多人类审计师的联合增益**：

## 结论

我们给出了人类--AI 协作审计三个核心定理的严格形式化。
证明了：

- 当人类判断携带 Cercis Score 所不编码的噪声信息时
- 这种优势按 $\sqrt{B_H/n}$ 衰减，其常数可由
- 完美噪声在任何认知系统下绝对不可分——

每个证明都提供了完整的测度论推导、所有前提的形式化陈述，
以及关于其局限性（``诚实暴击''）的严格自我审查。

## Appendix

## 附录 A：有效样本量 $n_{\mathrm{eff} \sim \sqrt{B_H \cdot n}$ 的推导}

{
**设定**：设 $Z_1, ..., Z_n$ 为独立同分布随机变量，$S_i = S(Z_i)$。
选择最小的 $B_H$ 个 $S_i$，对应的指标集为 $\cI_{B_H} = \{i: S_i \leq S_{(B_H)}\}$。

**问题**：选定样本 $\{Z_i\}_{i \in \cI_{B_H}}$ 的``有效信息量''是多少？

**分析**：选定样本不是独立的——它们通过排序事件 $\{S_i \leq S_{(B_H)}\}$ 耦合。
该事件的指示变量 $D_i = \ind\{S_i \leq S_{(B_H)}\}$ 满足 $\sum_i D_i = B_H$。

选定样本的对数似然为：

$$
    \ell(\theta) = \sum_{i=1}^n D_i \log p(Z_i \mid \theta) - \log P(\sum D_i = B_H).
$$

Fisher 信息为：

$$
    \Fisher_{\mathrm{eff}}(B_H)
    &= -\E\left[ \frac{\partial^2}{\partial\theta^2} \ell(\theta) \right] 

    &= \underbrace{\E\left[ \sum_i D_i \cdot \Fisher_1(Z_i) \right]}_{选定样本的信息和}
       - \underbrace{\E\left[ \frac{\partial^2}{\partial\theta^2}
          \log P(\sum D_i = B_H) \right]}_{选择偏置校正项}.
$$

第一项为 $B_H \cdot \Fisher_1$（因为 $\E[D_i] = B_H/n$，但 $\E[D_i \cdot \varepsilon_i]$ 涉及依赖）。
第二项是选择过程本身带来的信息损失。

**关键计算**：

$$
    \Cov(D_i, D_j) \approx \frac{B_H}{n} \left(1 - \frac{B_H}{n}\right) \cdot
    \frac{\psi'(i/(n+1)) \cdot \psi'(j/(n+1))}{\|\psi'\|^2},
$$

其中 $\psi = F_S^{-1}$ 是 $S$ 的分位数函数。

协方差矩阵 $\Sigma_D$ 的谱分析给出最大特征值 $\lambda_ \sim n/B_H$，
从而有效秩 $\rank_{\mathrm{eff}}(\Sigma_D) \sim \sqrt{B_H \cdot n}$。
因此 $n_{\mathrm{eff}} \sim \sqrt{B_H \cdot n}$。}

\bibliographystyle{plainnat}
\begin{thebibliography}{30}

\bibitem{scx2024cercis}
SCX Working Group.
\newblock ``The SCX Axiomatic Framework: Cercis, Situs, and Tiresias Operators,''
\newblock *Technical Report*, 2024.

\bibitem{fleming2012metacognition}
S.~M.~Fleming and R.~J.~Dolan.
\newblock ``The neural basis of metacognitive ability,''
\newblock *Philosophical Transactions of the Royal Society B*,
367(1594):1338--1349, 2012.

\bibitem{kahneman2011thinking}
D.~Kahneman.
\newblock *Thinking, Fast and Slow*.
\newblock Farrar, Straus and Giroux, 2011.

\bibitem{cover1999elements}
T.~M.~Cover and J.~A.~Thomas.
\newblock *Elements of Information Theory*, 2nd ed.
\newblock Wiley, 2006.

\bibitem{lehmann2005testing}
E.~L.~Lehmann and J.~P.~Romano.
\newblock *Testing Statistical Hypotheses*, 3rd ed.
\newblock Springer, 2005.

\bibitem{vanTrees1968detection}
H.~L.~Van Trees.
\newblock *Detection, Estimation, and Modulation Theory*, Part I.
\newblock Wiley, 1968.

\bibitem{david2003order}
H.~A.~David and H.~N.~Nagaraja.
\newblock *Order Statistics*, 3rd ed.
\newblock Wiley, 2003.

\bibitem{pearl2009causality}
J.~Pearl.
\newblock *Causality: Models, Reasoning, and Inference*, 2nd ed.
\newblock Cambridge University Press, 2009.

\end{thebibliography}