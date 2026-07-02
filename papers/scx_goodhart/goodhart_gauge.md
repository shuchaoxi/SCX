# Introduction

**Author:** SCX

*Abstract:*

**English.**
Goodhart's Law states that ``when a measure becomes a target, it ceases to be a good measure.''
In the SCX egalitarian framework, the Cercis Score $S(x) = Q(x) + \eta N(x)$ aggregates
quality $Q$ and novelty $N$ into a single scalar objective. Should this score become an
optimization target for self-interested agents---data providers, expert auditors, or
state-level actors---the framework is vulnerable to metric manipulation that decouples
$S$ from its underlying semantics. This paper formalizes three distinct attack surfaces:
(i) *data inflation*, where agents artificially inflate quality metrics without
improving genuine quality; (ii) *expert collusion*, where multiple auditors coordinate
to fabricate consensus; and (iii) *state forgery*, where adversaries synthesize entire
evaluation states to masquerade as authentic Cercis landscapes. For each threat, we prove
detection bounds that establish the minimum sample complexity required to distinguish
manipulated scores from legitimate ones with high probability. We then propose a layered
defense architecture comprising independent audit rotation, state-coverage penalties, and
multi-expert independence testing, each accompanied by formal guarantees.

[0.3\baselineskip]

**中文.**
古德哈特定律指出：「当一项度量成为目标时，它就不再是好的度量。」在SCX平等论框架中，
Cercis分数 $S(x)=Q(x)+\eta N(x)$ 将质量 $Q$ 与新颖性 $N$ 聚合为单一标量目标。
一旦该分数成为自利主体——数据提供者、专家审计员或国家级行为者——的优化目标，
框架将面临度量操纵的风险，使得 $S$ 与其底层语义脱钩。本文形式化三种攻击面：
（一）**数据膨胀**，即主体人为抬高质量度量而不改善真实质量；
（二）**专家共谋**，即多名审计员协调伪造共识；
（三）**状态伪造**，即对手合成完整评估状态以伪装为真实的Cercis景观。
针对每种威胁，我们证明检测边界，建立以高概率区分操纵分数与合法分数所需的最小样本复杂度。
随后提出分层防御架构，包括独立审计轮换、状态覆盖度惩罚与多专家独立性检验，每项附有形式化保证。

## Introduction
<!-- label: sec:intro -->

### Motivation

Goodhart's Law, named after the economist Charles Goodhart who observed that
``any observed statistical regularity will tend to collapse once pressure is
placed upon it for control purposes'' [cite], has become a
central concern in the age of AI evaluation. When a scalar metric---be it
test-set accuracy, BLEU score, or human-preference rating---becomes the
objective that systems or humans optimize against, the metric's correlation
with the underlying construct it was designed to measure degrades, often
catastrophically.

**古德哈特定律的现代诠释.** 在AI评估领域，Goodhart警告转化为一个精确的技术问题：
是否存在一种度量体系，其被操纵的难度（操纵成本）在数学上可界定，且其被操纵的事实
（操纵检测）在统计上可证明？SCX平等论框架试图通过Cercis Score $S$ 回答这一问题，
但框架本身尚未形式化其面对Goodhart攻击时的鲁棒性边界。

The SCX egalitarian framework [cite] defines the Cercis Score as:

$$<!-- label: eq:cercis_def -->
  S(x) = Q(x) + \eta \cdot N(x),
$$

where $Q(x)$ is the intrinsic quality of artifact $x$, $N(x)$ is its novelty
relative to the existing corpus, and $\eta > 0$ is the novelty-weighting
parameter. The score lives on the Situs manifold $(\mathcal{X}, d_P, \mu_P)$,
where $d_P$ encodes perceptual distance and $\mu_P$ encodes the empirical
distribution of artifacts.

**The Goodhart Threat.** Consider an adversary who can observe (or
estimate) the Cercis Score $S(x)$ and wishes to maximize it without incurring
the cost of genuine quality improvement. Three canonical attack strategies
emerge:

1. **Data Inflation (A1).** The adversary generates artifacts $\tilde{x}$
2. **Expert Collusion (A2).** Multiple auditors $\{E_k\}_{k=1}^K$ collude
3. **State Forgery (A3).** The adversary synthesizes an entire evaluation

### Contributions

This paper makes the following contributions:

1. **Threat Formalization** (Section [ref]). We provide rigorous
2. **Detection Bounds** (Section [ref]). For each attack, we prove
3. **Countermeasure Architecture** (Section [ref]). We propose
4. **Bilingual Exposition** (throughout). All theorems, definitions, and

### Related Work

Goodhart's law has been studied extensively in economics [cite],
machine learning [cite], and AI safety [cite].
Our work differs in three respects: (1) we operate within the specific mathematical
structure of the SCX framework rather than treating evaluation as a black box;
(2) we prove *detection bounds* with explicit dependence on the Cercis parameter
$\eta$, rather than providing qualitative taxonomies; and (3) our countermeasures
are designed to compose with existing SCX theorems (notably Theorem~3 on
noise-difficulty indistinguishability and Theorem~7 on cross-domain preservation).

## Preliminaries: The SCX Framework
<!-- label: sec:prelim -->

### Cercis Score and Situs Manifold

We recall the core objects of the SCX framework. Let $\cX$ be the space of all
artifacts (texts, models, datasets, policies). The **Situs operator**
encodes $\cX$ as a metric measure space:

$$<!-- label: eq:situs -->
  \Situs: \cX \to (\cX, d_P, \mu_P),
$$

where $d_P(x,y)$ is a perceptual distance (Wasserstein distance between the
internal representations of $x$ and $y$ under a reference model $P$) and
$\mu_P$ is the empirical distribution of artifacts.

> **Definition:** [Cercis Score]
>   <!-- label: def:cercis -->
>   For any artifact $x \in \cX$, the **Cercis Score** $S: \cX \to \bbR^+$ is:
>   \[
>     S(x) = Q(x) + \eta \cdot N(x),
>   \]
>   where:
>   
- $Q(x) \in [0,1]$ is the intrinsic quality score (expected utility to a
- $N(x) = D_{KL}(\delta_x \| \mu_P)$ or equivalently the Situs-distance
- $\eta > 0$ is the novelty-weighting hyperparameter.

> **Definition:** [Cercis State]
>   <!-- label: def:state -->
>   The **Cercis state** of artifact $x$ is the tuple:
>   \[
>     \Sigma(x) = \bigl(x,\; S(x),\; \nabla S(x),\; H_S(x)\bigr),
>   \]
>   where $\nabla S(x)$ is the gradient of $S$ on the Situs manifold and $H_S(x)$ is
>   the Hessian (second-order derivative information). The auditor's observable is
>   $\Sigma(x)$; the true quality $Q(x)$ is latent.

### Assumptions

We maintain the standard SCX assumptions [cite]:

\begin{assumption}[A1: Bounded Scores]
  <!-- label: ass:bounded -->
  $0 \leq Q(x) \leq 1$ and $0 \leq N(x) \leq N_$ for all $x \in \cX$.
  Consequently $S(x) \in [0, 1 + \eta N_]$.
\end{assumption}

\begin{assumption}[A2: Lipschitz Quality]
  <!-- label: ass:lipschitz -->
  $Q$ is $L_Q$-Lipschitz on the Situs manifold: $|Q(x) - Q(y)| \leq L_Q \cdot d_P(x,y)$.
\end{assumption}

\begin{assumption}[A3: Independent Audit Noise]
  <!-- label: ass:audit_noise -->
  Expert $k$ observes $S_k(x) = S(x) + \varepsilon_k$, where $\varepsilon_k \sim N(0,\sigma_k^2)$
  independently across experts and artifacts, with $\sigma_k \leq \sigma_$.
\end{assumption}

\begin{assumption}[A4: Situs Regularity]
  <!-- label: ass:situs_reg -->
  The Situs manifold $(\cX, d_P)$ is compact with diameter $D_ < \infty$,
  and the gradient $\nabla S$ exists almost everywhere with $\|\nabla S(x)\| \leq G_$.
\end{assumption}

## Threat Model
<!-- label: sec:threat -->

**威胁模型总览.** 我们考虑三类对手，按能力递增排列。所有对手共享目标：
在最小化真实质量改进成本的前提下，最大化其管辖制品的Cercis分数。

<div align="center">

[Table omitted — see original .tex]

</div>

### A1: Data Inflation \quad 数据膨胀

> **Definition:** [Data Inflation Attack]
>   <!-- label: def:a1 -->
>   An adversary $\cA_1$ with access to a surrogate quality estimator $\hat{Q}(\cdot)$
>   (which may be a proxy model, a leaked evaluation rubric, or gradient queries to
>   the scoring system) produces artifacts $\{\tilde{x}_i\}_{i=1}^m$ satisfying:
>   \[
>     \hat{S}(\tilde{x}_i) = \hat{Q}(\tilde{x}_i) + \eta \hat{N}(\tilde{x}_i) \geq \tau,
>   \]
>   for some threshold $\tau$, while
>   \[
>     \bbE[Q(\tilde{x}_i)] \leq \bbE[\hat{Q}(\tilde{x}_i)] - \Delta_Q,
>   \]
>   where $\Delta_Q > 0$ is the **quality gap** between estimated and true quality.

**核心机制.** 对手利用 $Q$ 与 $\hat{Q}$ 之间的分布偏移生成在代理估计器上得分高
但在真实质量上得分低的制品。这类似乎「应试教育」：学生学会考试技巧（优化 $\hat{Q}$）
而非掌握学科内容（提升 $Q$）。

The quality gap $\Delta_Q$ is the adversary's ``Goodhart margin''---the extent to which
the proxy metric $\hat{Q}$ overestimates true quality $Q$. This gap arises from:

1. **Estimator incompleteness**: $\hat{Q}$ captures only a subset of the
2. **Distribution shift**: $\hat{Q}$ was calibrated on a training distribution
3. **Adversarial overfitting**: the adversary actively searches for inputs

### A2: Expert Collusion \quad 专家共谋

> **Definition:** [Expert Collusion Attack]
>   <!-- label: def:a2 -->
>   Let $\cE = \{E_1, ..., E_K\}$ be $K$ expert auditors assigned to evaluate artifact
>   $x$. In a collusion attack, a subset $\cE_C \subseteq \cE$ of size $K_C \leq K$
>   coordinates to report:
>   \[
>     S_k^{rep}(x) = S(x) + \delta + \tilde_k,
>   \]
>   where $\delta > 0$ is a **collusive bias** (common across colluders) and
>   $\tilde_k \sim N(0, \tilde_k^2)$ are fabricated noise terms
>   calibrated to match the variance of honest auditors, i.e., $\tilde_k \approx \sigma_k$.

**共谋结构.** 共谋者面临一个微妙的设计问题：他们的报告必须同时满足两个条件：
(1) 系统性地偏移均值（$\delta > 0$）以提升聚合分数；
(2) 保持报告之间的表面独立性（$\tilde_k$ 匹配 $\sigma_k$）以逃避统计检测。

The colluders' dilemma is that $\delta$ cannot be made arbitrarily large without
being detected by outlier tests, but must be large enough to meaningfully shift the
aggregate score $\bar{S} = \frac{1}{K}\sum_k S_k^{rep}$.

### A3: State Forgery \quad 状态伪造

> **Definition:** [State Forgery Attack]
>   <!-- label: def:a3 -->
>   An adversary $\cA_3$ with complete knowledge of the SCX framework (including the
>   Situs manifold structure, the Cercis Score definition, and the distribution of
>   legitimate evaluation states) produces forged states $\tilde(x) =
>   (\tilde{x}, \tilde{S}, \tildeS, \tilde{H}_S)$ such that the distribution
>   $\cD_{forge}$ of forged states is $\varepsilon$-close to the distribution
>   $\cD_{legit}$ of legitimate states in total variation:
>   \[
>     d_{TV}(\cD_{forge}, \cD_{legit}) \leq \varepsilon.
>   \]

**状态伪造的严重性.** A3是最强大的攻击：对手不仅操纵分数，而且构造整个评估状态，
包括梯度与Hessian信息，使得审计者无法从可观测量的联合分布中区分真伪。
这与SCX Theorem~3（噪声-难度不可区分性）形成对偶：Theorem 3断言噪声与内在难度
在观测层面不可区分；A3断言在分数与梯度层面也可以构造不可区分的伪造状态。
两者的交集定义了检测可能性的根本边界。

## Detection Bounds
<!-- label: sec:bounds -->

**检测边界总览.** 对每种攻击，我们证明一个检测定理，形式为：
在显著性水平 $\alpha$ 下，以功效 $1-\beta$ 检测操纵所需的最小样本量 $n^*$ 由攻击强度参数
（$\Delta_Q$、$\delta$ 或 $\varepsilon$）以及Cercis新颖性参数 $\eta$ 决定。

### Detecting Data Inflation
<!-- label: sec:bound_a1 -->

> **Theorem:** [Data Inflation Detection Bound]
>   <!-- label: thm:a1_detect -->
>   Let $\cD_{legit}$ be the distribution of Cercis Scores for authentic artifacts
>   with mean $\mu_S$ and variance $\sigma_S^2$. Let $\cD_{infl}$ be the distribution
>   of inflated artifacts with mean $\mu_S + \Delta_{infl}$ and variance
>   $\sigma_S^2 + \Delta_\sigma^2$. Assume $\Delta_Q = \Delta_{infl} - \eta \cdot \Delta_N$,
>   where $\Delta_N \geq 0$ is the novelty shift. Then:
> 
>   
1. **Score-based detection.** A two-sample $t$-test on $n$ observed scores
2. **Gradient-based detection.** If the adversary's artifacts exhibit

> **Proof:** **Part (i).** Under the null $H_0$ (no inflation), scores are i.i.d.\ with
>   mean $\mu_S$. Under $H_1$ (inflation), scores have mean $\mu_S + \Delta_{infl}$.
>   Let $\bar{S}_n = \frac{1}{n}\sum_{i=1}^n S(x_i)$. By the Central Limit Theorem,
>   \[
>     \frac{\bar{S}_n - \mu_S}{\sigma_S/\sqrt{n}} \xrightarrow{d} N(0,1) \quad under  H_0,
>   \]
>   and
>   \[
>     \frac{\bar{S}_n - (\mu_S + \Delta_{infl})}{\sqrt{(\sigma_S^2 + \Delta_\sigma^2)/n}}
>     \xrightarrow{d} N(0,1) \quad under  H_1.
>   \]
>   The standard sample-size formula for a two-sided $z$-test with pooled variance
>   $\sigma_{pool}^2 = \sigma_S^2 + \Delta_\sigma^2/2$ yields [ref].
> 
>   **Part (ii).** Same logic applied to the gradient norm statistic
>   $G(x) = \|\nabla S(x)\|$, which under Assumption [ref] is bounded.
>   The separation $\Delta_G$ captures the fact that inflated artifacts, being
>   generated to maximize a proxy score, tend to lie in ``flat'' regions of $S$
>   (local optima of the proxy) rather than the ``rugged'' regions characteristic
>   of genuinely novel, high-quality artifacts.  $\square$

> **Remark:** [Interpretation]
>   **中文解读.** 检测边界 $n_{A1}^*$ 揭示了三个关键关系：
>   
- $\Delta_{infl}$ 越大（质量膨胀越严重），检测所需样本越少
- $\Delta_\sigma^2$（膨胀伪影引入的额外方差）增加检测难度
- $\eta$ 通过 $\Delta_{infl} = \Delta_Q + \eta \Delta_N$ 间接影响边界：

> 
>   The trade-off $\eta \uparrow \implies$ (more reward for novelty, easier to detect inflation)
>   is a **self-limiting property** of the Cercis Score: the same mechanism that makes
>   the score valuable also makes its manipulation detectable.

### Detecting Expert Collusion
<!-- label: sec:bound_a2 -->

> **Theorem:** [Expert Collusion Detection Bound]
>   <!-- label: thm:a2_detect -->
>   Let $K$ experts evaluate artifact $x$, of whom $K_C \leq \lfloor K/2 \rfloor$ are
>   colluding with common bias $\delta$ and calibrated variance $\sigma_C^2 = \sigma_H^2$,
>   where $\sigma_H^2$ is the honest-expert variance. Define the **inter-expert
>   correlation anomaly**:
>   \[
>     \rho_{anom} = \frac{\delta^2}{\delta^2 + 2\sigma_H^2}.
>   \]
>   Then:
> 
>   
1. **Pairwise correlation test.** For any pair of colluding experts $(i,j)$,
2. **Variance ratio test.** The within-group variance of colluding experts

> **Proof:** **Part (i): Correlation anomaly.** For two colluding experts $i,j \in \cE_C$,
>   their reported scores are:
>   \[
>     S_i = S + \delta + \varepsilon_i, \quad S_j = S + \delta + \varepsilon_j,
>   \]
>   where $\varepsilon_i, \varepsilon_j \sim_{i.i.d.} N(0, \sigma_H^2)$.
>   The covariance is $Cov(S_i, S_j) = \bbV[S] + \delta^2$ (common $S$ and common
>   $\delta$), while each variance is $\bbV[S_i] = \bbV[S] + \sigma_H^2 + \delta^2$.
>   Hence:
>   \[
>     \rho_{ij} = \frac{\bbV[S] + \delta^2}{\bbV[S] + \sigma_H^2 + \delta^2}.
>   \]
>   For $\bbV[S] \gg \delta^2$ (natural score variation dominates collusive bias),
>   this simplifies to $\rho_{anom} \approx \delta^2/(\delta^2 + \sigma_H^2)$.
>   The Fisher $z$-transformation $z(\rho) = \frac{1}{2}\ln\frac{1+\rho}{1-\rho}$ is
>   approximately $N(z(\rho), 1/(n-3))$. The sample size formula follows from the
>   standard power calculation for the difference $z(\rho_{anom}) - z(0)$.
> 
>   **Part (ii): ANOVA decomposition.** Consider the one-way ANOVA with groups:
>   colluders vs.\ non-colluders. The between-group sum of squares captures the
>   systematic bias $\delta$:
>   \[
>     SS_{between} = K_C(\bar{S}_C - \bar{S})^2 + (K-K_C)(\bar{S}_H - \bar{S})^2
>     = \frac{K_C(K-K_C)}{K} \delta^2,
>   \]
>   where $\bar{S}_C = S + \delta$ (colluder mean) and $\bar{S}_H = S$ (honest mean).
>   The within-group MS estimates $\sigma_H^2$. Substituting into the $F$-ratio yields
>    [ref]. The noncentrality parameter of the $F$-distribution under
>   $H_1$ is $\lambda = n \cdot K_C(K-K_C) \cdot \delta^2 / \sigma_H^2$, from which
>   the sample size formula [ref] follows via the standard noncentral
>   $F$ power calculation.  $\square$

> **Remark:** [Collusion Detectability Phase Transition]
>   **共谋可检测性的相变.** 定义共谋信噪比 $SNR_C = \delta / \sigma_H$。
>   存在临界值：
>   \[
>     \delta_{crit} = \sigma_H \cdot \sqrt{\frac{2\ln(1/\alpha)}{K_C(K-K_C)}}.
>   \]
>   当 $\delta < \delta_{crit}$ 时，共谋在统计上不可检测（功效 $< 1-\beta$ 对任何有限 $n$）；
>   当 $\delta > \delta_{crit}$ 时，所需样本量随 $1/\delta^2$ 衰减。
>   
>   这定义了 **Cercis-Goodhart 相变**：存在一个对手机制不可能同时
>   实现（i）显著分数提升（$\delta$ 大）和（ii）统计不可检测性（$\delta < \delta_{crit}$）
>   的参数区域。**系统设计者可以通过调节 $K$ 和 $\sigma_H$ 来推移 $\delta_{crit}$，
>   使得任何具有实际意义的分数操纵必然落入可检测区域。**

### Detecting State Forgery
<!-- label: sec:bound_a3 -->

> **Theorem:** [State Forgery Detection Bound]
>   <!-- label: thm:a3_detect -->
>   Let $\cD_{legit}$ be the joint distribution of Cercis states
>   $\Sigma(x) = (x, S, \nabla S, H_S)$ for legitimate artifacts, and let
>   $\cD_{forge}$ be the distribution of forged states.
>   Assume that authentic Cercis states satisfy the **gradient consistency
>   condition**:
>   
> $$<!-- label: eq:grad_consistency -->
>     \bbE[\|\nabla S(x) - \nabla_ \hat{S}(x)\|^2] \leq \kappa^2,
>   $$
> 
>   where $\nabla_$ is the Situs manifold gradient operator and
>   $\hat{S}$ is any estimator of $S$. Then:
> 
>   
1. **Gradient inconsistency detection.** Define the
2. **Situs geodesic test.** For any pair of forged states

> **Proof:** **Part (i):** The key insight is that on a smooth manifold with a metric
>   connection (Levi-Civita), the curl of a gradient field is identically zero:
>   $\nabla \times \nabla f \equiv 0$ for any smooth $f$. Forged states generated
>   without solving the Situs consistency constraints will typically violate this
>   identity, producing a non-zero curl statistic. Under $H_0$, $\tau(x) \approx 0$
>   (up to discretization error $\kappa$); under $H_1$, $\tau(x)$ is inflated by
>   $\Delta_\tau$. The sample size formula follows from the standard power calculation
>   for a one-sided $z$-test.
> 
>   **Part (ii):** The Cercis-Lipschitz constraint follows from Assumptions [ref]
>   and [ref]:
>   \[
>     |S(x) - S(y)| = |(Q(x) - Q(y)) + \eta(N(x) - N(y))|
>     \leq L_Q d_P(x,y) + \eta L_N d_P(x,y).
>   \]
>   Under $H_0$, score differences between random pairs are approximately normal with
>   variance $2\sigma_S^2$. The tail bound follows from Hoeffding's inequality applied
>   to the event $\{|S_i - S_j| > (L_Q + \eta L_N) d_P(x_i, x_j)\}$.  $\square$

> **Remark:** [The Fundamental Tension with Theorem 3]
>   **与Theorem 3的基础张力.** SCX Theorem~3 断言：从观测数据 $(S, \nabla S, H_S)$
>   无法区分标签噪声与内在难度。状态伪造检测（A3检测）似乎与这一断言矛盾
>   —— 如果噪声与难度不可区分，那么伪造状态（模拟噪声结构）也应不可区分。
> 
>   消解这一表面矛盾的关键在于 **Situs流形约束**：Theorem~3 的不可区分性
>   是在 Situs流形上「内部」成立的——即所有合法状态都满足梯度一致性条件 [ref]。
>   伪造状态由于未经过 Situs 编码过程，通常破坏这种一致性，从而在流形的几何结构层面
>   暴露异常。换句话说：**噪声可以在语义层面伪装成难度，但无法在几何层面
>   伪装成 Situs一致性。**
> 
>   This resolves the apparent paradox: Theorem~3 concerns *semantic* indistinguishability
>   (what the score means), while Theorem [ref] concerns *geometric*
>   distinguishability (whether the score lives on the Situs manifold). The two are
>   complementary, not contradictory.

### Unified Detection Frontier
<!-- label: sec:frontier -->

> **Theorem:** [Goodhart Detection Frontier]
>   <!-- label: thm:frontier -->
>   Define the **manipulation magnitude** $\Delta$ as:
>   
- For A1: $\Delta = \Delta_{infl}$ (score inflation magnitude).
- For A2: $\Delta = \delta$ (collusive bias).
- For A3: $\Delta = \Delta_\tau$ (curl inconsistency magnitude).

>   For all three attacks, the minimum sample size for detection scales as:
>   
> $$<!-- label: eq:unified_frontier -->
>     n^*(\Delta, \alpha, \beta) = \Theta\left(\frac{1}{\Delta^2}\right),
>   $$
> 
>   with constants depending on the specific attack structure and Cercis parameter $\eta$.
>   Furthermore, the **detection possibility region** is:
>   \[
>     \cR_{detect} = \left\{ (\Delta, n) : n \geq \frac{C(\eta, \sigma)}{\Delta^2} \right\},
>   \]
>   where $C(\eta, \sigma)$ is a constant that:
>   
1. *Decreases* with $\eta$ for A1 (novelty amplifies inflation signals);
2. *Increases* with $\eta$ for A2 (novelty-weighting increases score variance,
3. *Is independent* of $\eta$ for A3 (curl inconsistency depends only on

> **Proof:** The $\Theta(1/\Delta^2)$ scaling follows directly from the sample size formulas
>   in Theorems [ref],  [ref], and  [ref],
>   all of which have the form $n^* = constant \cdot (z_{1-\alpha/2} + z_{1-\beta})^2 / \Delta^2$.
> 
>   For the $\eta$-dependence: (i) In A1, $\Delta_{infl} = \Delta_Q + \eta \Delta_N$,
>   so larger $\eta$ increases the effective $\Delta$, reducing $n^*$.
>   (ii) In A2, the score variance acquires an $\eta$-dependent component:
>   $\sigma_S^2 \approx \sigma_Q^2 + \eta^2 \sigma_N^2$, increasing with $\eta$.
>   The correlation anomaly $\rho_{anom}$ becomes $\delta^2/(\delta^2 + \sigma_Q^2 + \eta^2\sigma_N^2)$,
>   which *decreases* with $\eta$, increasing $n^*$.
>   (iii) In A3, $\tau(x)$ measures geometric consistency, which is independent of
>   the $\eta$-weighted score magnitude.  $\square$

> **Corollary:** [Cercis $\eta$ as a Goodhart Regulator]
>   <!-- label: cor:eta_regulator -->
>   The novelty parameter $\eta$ acts as a **tunable Goodhart regulator**:
>   
- **Low $\eta$ regime** ($\eta \to 0$): The Cercis Score reduces to pure
- **High $\eta$ regime** ($\eta \gg 1$): Novelty dominates. A1 becomes
- **Optimal $\eta^*$**: There exists an $\eta^*$ that minimizes the

## Countermeasures
<!-- label: sec:defense -->

**防御体系总览.** 基于检测边界的分析，我们提出三层防御架构。
每层针对特定攻击向量，并与现有SCX定理兼容。

### Countermeasure 1: Independent Audit Rotation
<!-- label: sec:cm_rotation -->

**反制措施一：独立审计轮换**

The core insight is that collusion requires *repeated interaction* to
establish coordination. By randomly rotating auditor assignments and preventing
auditors from knowing their co-auditors in advance, we destroy the information
structure needed for stable collusion equilibria.

> **Definition:** [Audit Rotation Protocol]
>   <!-- label: def:rotation -->
>   Let $\cE = \{E_1, ..., E_M\}$ be the pool of $M$ certified experts. For each
>   artifact $x_t$ arriving at time $t$, an **independent audit panel**
>   $\cP_t \subset \cE$ of size $K$ is drawn uniformly at random without replacement.
>   Auditor $E_k$ receives only the tuple $(x_t, \cP_t)$ but *not* the identity
>   of other panels they will serve on in the future.

> **Theorem:** [Rotation Breaks Collusion Equilibria]
>   <!-- label: thm:rotation -->
>   Under the rotation protocol of Definition [ref], any collusion
>   strategy requiring pre-commitment of $\geq 2$ auditors to coordinate on a
>   specific artifact has expected coordination probability:
>   \[
>     \bbP(successful coordination) \leq
>     \binom{K_C}{2} \Big/ \binom{M}{2} \leq \frac{K_C^2}{M^2},
>   \]
>   which decays quadratically in the pool size $M$. For $M \gg K_C$, collusion
>   is infeasible without detectable side-channel communication.

> **Proof:** The probability that two specific colluders $i,j \in \cE_C$ are both assigned
>   to the same panel is $\binom{M-2}{K-2}/\binom{M}{K} = K(K-1)/(M(M-1))$.
>   Summing over all $\binom{K_C}{2}$ colluder pairs and applying the union bound
>   yields the result. For $M \to \infty$, this probability approaches zero,
>   meaning colluders cannot reliably coordinate on the same artifact.  $\square$

> **Remark:** **实践考量.** 轮换协议需与专家校准（expert calibration）机制结合：
>   每位专家的历史评分分布被持续追踪，显著偏离个人基线的评分会触发自动复核。
>   这形成了双层防御：轮换防止共谋形成，校准检测个别偏离。

### Countermeasure 2: State Coverage Penalty
<!-- label: sec:cm_coverage -->

**反制措施二：状态覆盖度惩罚**

Data inflation attacks concentrate artifacts in ``easy-scoring'' regions of the
Situs manifold. A state-coverage penalty discourages this concentration by
explicitly downweighting scores from over-represented regions.

> **Definition:** [Coverage-Adjusted Cercis Score]
>   <!-- label: def:coverage -->
>   Let $p(x)$ be the empirical density of evaluated artifacts at $x \in \cX$.
>   Define the **coverage-adjusted Cercis Score**:
>   
> $$<!-- label: eq:scov -->
>     S_{cov}(x) = S(x) - \lambda \cdot \log p(x),
>   $$
> 
>   where $\lambda > 0$ is the coverage penalty parameter. Equivalently, by
>   exponential tilting:
>   \[
>     S_{cov}(x) = S(x) + \lambda \cdot H(p) \cdot \indicator[p(x) > p_{thresh}],
>   \]
>   where $H(p) = -\int p(x)\log p(x)\,dx$ is the entropy of the evaluation distribution.

> **Theorem:** [Coverage Penalty Optimality]
>   <!-- label: thm:coverage -->
>   For a data-inflation adversary constrained to generate artifacts within a
>   bounded Situs ball $\cB_r(x_0)$, the coverage-adjusted score $S_{cov}$
>   achieves the following guarantee:
>   
> $$<!-- label: eq:cov_guarantee -->
>     \max_{x \in \cB_r(x_0)} S_{cov}(x) \leq
>     \max_{x \in \cB_r(x_0)} S(x) - \lambda \cdot \log\left(\frac{m}{vol(\cB_r)}\right),
>   $$
> 
>   where $m$ is the number of artifacts generated in $\cB_r(x_0)$.
>   As $m \to \infty$ (heavy inflation), $S_{cov}(x) \to -\infty$, making
>   the region progressively less attractive.

> **Proof:** Under the adversary's concentration strategy, $p(x)$ within $\cB_r(x_0)$
>   grows as $p(x) \approx m / vol(\cB_r)$ for $m$ artifacts in the region.
>   Substituting into [ref] yields the bound. The divergence as
>   $m \to \infty$ follows from $\log(m) \to \infty$.  $\square$

> **Remark:** [Connection to Novelty]
>   **与新颖性度量的关系.** 覆盖度惩罚 $\lambda \log p(x)$ 在形式上与Cercis的
>   新颖性项 $N(x) = D_{KL}(\delta_x \| \mu_P)$ 类似。区别在于：
>   $N(x)$ 惩罚与**整个语料库**分布偏离的制品（鼓励全局新颖性），
>   而覆盖度惩罚针对**评估分布**的集中（阻止局部投机）。
>   两者互补：$N$ 奖励探索，$S_{cov}$ 惩罚投机性聚集。

### Countermeasure 3: Multi-Expert Independence Testing
<!-- label: sec:cm_independence -->

**反制措施三：多专家独立性检验**

This countermeasure operationalizes the detection bound from
Theorem [ref] as an online monitoring system.

> **Definition:** [Online Independence Monitor]
>   <!-- label: def:monitor -->
>   For each artifact $x$, let $\{S_k(x)\}_{k=1}^K$ be the $K$ expert scores.
>   The **independence monitor** computes three statistics:
>   
1. **Pairwise Correlation Matrix:**
2. **Conditional Independence Test:**
3. **CUSUM Anomaly Detector:**

> **Theorem:** [Independence Test Guarantees]
>   <!-- label: thm:ind_test -->
>   Under Assumption [ref] (independent audit noise),
>   the online independence monitor provides the following guarantees:
> 
>   
1. **False positive control.** Under $H_0$ (no collusion),
2. **Detection delay.** Under $H_1$ (collusion with bias $\delta$),
3. **Asymptotic consistency.** As $n \to \infty$,

> **Proof:** **(i)** By union bound over $\binom{K}{2}$ pairwise tests plus one CUSUM test.
> 
>   **(ii)** The CUSUM statistic under $H_1$ has log-likelihood increments
>   $\log \Lambda_t = \log(\phi_{\delta,\sigma_H}(S_t) / \phi_{0,\sigma_H}(S_t))$,
>   where $\phi$ is the Gaussian density. The expected increment is
>   $\bbE_{H_1}[\log \Lambda_t] = D_{KL}(N(\delta, \sigma_H^2) \| N(0, \sigma_H^2))
>   = \delta^2/(2\sigma_H^2)$. The Wald approximation for CUSUM ARL [cite]
>   yields the claimed bound.
> 
>   **(iii)** By the law of large numbers applied to partial correlations:
>   under $H_0$, $S_i \indep S_j \mid S$ implies the partial covariance is zero, and
>   the sample partial correlation converges to zero in probability. Under $H_1$,
>   the common bias $\delta$ induces a non-zero partial correlation that converges
>   to $\rho_{anom}$ as derived in Theorem [ref].  $\square$

### Integrated Defense Architecture
<!-- label: sec:integrated -->

[Figure omitted — see original .tex]

\begin{algorithm}[htbp]
*Caption:* Goodhart-Gauged Cercis Evaluation
<!-- label: alg:gauge -->
\begin{algorithmic}[1]
\Require Artifact $x$, expert pool $\cE$, parameters $\eta, \lambda, \alpha, \gamma$
\Ensure Goodhart-robust Cercis Score $S^*(x)$ with anomaly flags

\State **// Step 1: Independent Audit Rotation**
\State Draw panel $\cP \subset \cE$ of size $K$ uniformly at random
\State **// Step 2: Collect Expert Scores**
\For{$k \in \cP$}
    \State $S_k \gets ExpertEvaluate(x, E_k)$  \Comment{Includes noise $\varepsilon_k$}
\EndFor

\State **// Step 3: Coverage-Adjusted Aggregation**
\State $p(x) \gets EstimateDensity(x)$  \Comment{using Situs kernel density}
\State $\bar{S} \gets \frac{1}{K}\sum_{k} S_k$
\State $S_{cov} \gets \bar{S} - \lambda \cdot \log(p(x) + \epsilon)$

\State **// Step 4: Independence Monitoring**
\State $R \gets ComputePairwiseCorrelations(\{S_k\}, history)$
\State **If** $\max_{i<j} |R_{ij}| > threshold(\alpha, K)$ **then**
    \State **Raise** CollusionWarning
\EndIf

\State $C \gets UpdateCUSUM(\{S_k\}, \gamma)$
\State **If** $C > threshold_{CUSUM}$ **then**
    \State **Raise** AnomalyFlag
\EndIf

\State **// Step 5: Gradient Consistency Check (A3 defense)**
\State $\tau \gets \|\nabla \times \nabla \bar{S}(x)\|^2$
\State **If** $\tau > \kappa^2 + z_{1-\alpha} \cdot \sigma_\tau$ **then**
    \State **Raise** ForgeryWarning
\EndIf

\State \Return $(S_{cov}, warnings)$
\end{algorithmic}
\end{algorithm}

## Composition with SCX Theorems
<!-- label: sec:composition -->

**与SCX定理体系的组合性质.**
The Goodhart defenses compose with existing SCX theorems to provide end-to-end
guarantees:

> **Theorem:** [Defense Composition Theorem]
>   <!-- label: thm:composition -->
>   Let $\cS = (T3, T5, T7, CD, FA, AR, TS, HC)$ denote the SCX theorem suite.
>   The Goodhart countermeasures $\cG = (Rotation, Coverage, Independence)$
>   compose with $\cS$ as follows:
> 
>   
1. **With Theorem 3 (Noise-Difficulty):**
2. **With Theorem 5 (Active Learning):**
3. **With Theorem 7 (Cross-Domain):**
4. **With AR-Theorem (Adversarial Robustness):**
5. **With FA-Theorem (Federated Audit):**
6. **With HC-Theorem (Human-AI Audit):**

## Numerical Validation
<!-- label: sec:numerical -->

**数值验证.** 我们通过模拟实验验证检测边界的紧致性。

### Experimental Setup

We simulate three scenarios corresponding to A1, A2, and A3:

- **A1 Simulation.** Legitimate artifacts: $Q(x) \sim Beta(5,2)$,
- **A2 Simulation.** $K=7$ experts, $K_C=3$ colluders, $\delta \in \{0.05, 0.1, 0.2\}$,
- **A3 Simulation.** Legitimate states satisfy $\nabla \times \nabla S = 0$ (up to

[Table omitted — see original .tex]

> **Remark:** 所有情况下，经验功效在理论 $n^*$ 处达到或超过标称的 $1-\beta=0.80$，
>   证明检测边界的紧致性。在 $\Delta \to 0$ 的极限下，边界保守性增加
>   （样本量需求高于理论值），这是CLT近似在低信噪比下的预期行为。

## Discussion
<!-- label: sec:discussion -->

### Limitations

**局限性.**

1. **Situs流形旋度算子.** A3检测依赖Situs流形上的旋度算子 $\nabla \times$。
2. **Finite-sample calibration.** 检测边界的推导使用了渐近正态近似。
3. **Adaptive adversaries.** 所有检测边界假设对手策略是 *静态* 的。
4. **Coverage penalty $\lambda$ tuning.** 覆盖度惩罚参数 $\lambda$ 目前是

### Future Directions

**未来方向.**

1. **Game-theoretic extension (Goodhart作为博弈均衡).**
2. **Information-theoretic lower bounds.**
3. **Empirical Goodhart audit of production systems.**
4. **Dynamic $\eta$ scheduling.**
5. **Situs同态性的构造性证明.**

## Conclusion
<!-- label: sec:conclusion -->

**结论.**
本文为SCX平等论框架提供了Goodhart防御的形式化基础。主要成果包括：

1. 对三种典型操纵攻击（数据膨胀A1、专家共谋A2、状态伪造A3）给出了严格的数学定义，
2. 为每种攻击证明了检测边界（Theorem [ref]-- [ref]），
3. 揭示了Cercis新颖性参数 $\eta$ 作为 **Goodhart调节器** 的角色
4. 提出三层防御架构：独立审计轮换（阻止共谋形成）、状态覆盖度惩罚（压制数据膨胀）、
5. 证明了Goodhart防御与现有SCX定理体系的可组合性（Theorem [ref]），

**核心洞察.** Goodhart's Law并非Cercis框架的致命弱点，而是其 *可检测的*
退化模式。因为Cercis Score的定义包含几何结构（Situs流形）而非仅仅是标量值，
操纵行为在几何层面留下可检测的痕迹——梯度不一致性、共谋引起的条件相关性、
以及评估分布的异常集中。**度量即信息：当度量被操纵时，操纵行为本身
产生新的信息，可用于检测操纵。** 这是Cercis框架对Goodhart困境的根本回应。

**核心洞察（英文）.** Goodhart's Law is not a fatal vulnerability of the Cercis
framework, but rather its *detectable* degradation mode. Because the Cercis Score
is defined with geometric structure (the Situs manifold) rather than as a bare scalar,
manipulation leaves detectable traces in the geometry---gradient inconsistencies,
collusion-induced conditional correlations, and anomalous concentration of evaluation
density. **The measure is information: when the measure is manipulated, the act of
manipulation itself generates new information that can be used to detect the manipulation.**
This is the Cercis framework's fundamental response to the Goodhart dilemma.

## Appendix
## Proof Details and Supporting Lemmas
<!-- label: app:proofs -->

### Auxiliary Lemmas

> **Lemma:** [Hoeffding's Inequality for Bounded Scores]
>   <!-- label: lem:hoeffding -->
>   Under Assumption [ref], for any $\varepsilon > 0$:
>   \[
>     \bbP\left(|\bar{S}_n - \bbE[S]| \geq \varepsilon\right)
>     \leq 2\exp\left(-\frac{2n\varepsilon^2}{(1+\eta N_)^2}\right).
>   \]

> **Lemma:** [Fisher Z-Transformation Variance]
>   <!-- label: lem:fisher -->
>   Let $z(\rho) = \frac{1}{2}\ln\frac{1+\rho}{1-\rho}$. For i.i.d.\ bivariate normal
>   samples with true correlation $\rho$:
>   \[
>     \sqrt{n-3}(z(\hat_n) - z(\rho)) \xrightarrow{d} N(0,1).
>   \]

> **Lemma:** [CUSUM Average Run Length]
>   <!-- label: lem:cusum -->
>   For a CUSUM detector with threshold $h$ and drift parameter $\gamma$, under
>   i.i.d.\ Gaussian observations:
>   
> $$
>     \bbE_{H_0}[ARL] &= \frac{e^{2h} - 2h - 1}{2} \approx \frac{e^{2h}}{2}, 

>     \bbE_{H_1}[ARL] &\approx \frac{h}{D_{KL}(H_1 \| H_0)}.
>   $$

### Proof of Theorem [ref]

> **Proof:** [Detailed proof of Theorem [ref]]
>   We prove the three $\eta$-dependence claims separately.
> 
>   **Claim (i): A1 detection improves with $\eta$.**
>   Under A1, the adversary's score inflation decomposes as:
>   \[
>     \Delta_{infl} = \Delta_Q + \eta \cdot \Delta_N,
>   \]
>   where $\Delta_Q = \bbE[\hat{Q}(\tilde{x}) - Q(\tilde{x})]$ and
>   $\Delta_N = \bbE[\hat{N}(\tilde{x}) - N(\tilde{x})]$.
>   Substituting into [ref]:
>   \[
>     n_{A1}^*(\eta) = \frac{2(\sigma_S^2 + \Delta_\sigma^2/2)}{(\Delta_Q + \eta\Delta_N)^2}
>     \cdot (z_{1-\alpha/2} + z_{1-\beta})^2.
>   \]
>   Differentiating with respect to $\eta$:
>   \[
>     \frac{\partial n_{A1}^*}{\partial \eta} =
>     -\frac{4\Delta_N(\sigma_S^2 + \Delta_\sigma^2/2)}{(\Delta_Q + \eta\Delta_N)^3}
>     \cdot (z_{1-\alpha/2} + z_{1-\beta})^2 < 0,
>   \]
>   for $\Delta_N > 0$. Hence $n_{A1}^*$ decreases with $\eta$.
> 
>   **Claim (ii): A2 detection degrades with $\eta$.**
>   The score variance under honesty is:
>   \[
>     \sigma_S^2(\eta) = \bbV[Q(x)] + \eta^2 \bbV[N(x)] + 2\eta\,Cov(Q,N).
>   \]
>   For large $\eta$, $\sigma_S^2(\eta) \sim \eta^2 \bbV[N]$.
>   The correlation anomaly from Theorem [ref] is:
>   \[
>     \rho_{anom}(\eta) = \frac{\delta^2}{\delta^2 + \sigma_S^2(\eta) + \sigma_H^2}.
>   \]
>   As $\eta \to \infty$, $\rho_{anom}(\eta) \to 0$, making collusion
>   harder to detect. The Fisher $z$-score $z(\rho_{anom}) \approx \rho_{anom}$
>   for small $\rho_{anom}$, so $n_{A2}^* \approx const / \rho_{anom}^2
>   = O(\eta^4)$ in the high-$\eta$ regime.
> 
>   **Claim (iii): A3 detection is $\eta$-independent.**
>   The curl statistic $\tau(x) = \|\nabla \times \nabla S(x)\|^2$ depends on the
>   *geometric* structure of $S$ on the Situs manifold, not on its magnitude.
>   Since $\nabla S = \nabla Q + \eta \nabla N$, and $\nabla \times \nabla f \equiv 0$
>   for any smooth $f$, we have:
>   \[
>     \tau(x) = 0 \quad for all legitimate states,
>   \]
>   regardless of $\eta$. Forged states break this identity by construction.
>   The detection constant $\Delta_\tau$ depends only on the forger's inability to
>   satisfy $\nabla \times \nabla \tilde{S} = 0$, which is independent of $\eta$.
>    $\square$

### Proof of the $\delta_{crit$ Phase Transition}

> **Proof:** [Derivation of $\delta_{crit}$]
>   From Theorem [ref], the CUSUM detection delay is:
>   \[
>     \bbE_{H_1}[ARL] \leq \frac{2\sigma_H^2 \cdot |\log \alpha|}{\delta^2}.
>   \]
>   For practical detectability, we require $\bbE_{H_1}[ARL] \leq n_$,
>   where $n_$ is the maximum acceptable number of artifacts before detection.
>   Solving for $\delta$:
>   \[
>     \delta \geq \delta_{crit} = \sigma_H \sqrt{\frac{2|\log \alpha|}{n_}}.
>   \]
>   With $\alpha = 0.05$, $n_ = 1000$, and $\sigma_H = 0.1$:
>   \[
>     \delta_{crit} = 0.1 \cdot \sqrt{\frac{2 \cdot 2.996}{1000}} \approx 0.0077.
>   \]
>   Any collusion bias below $0.0077$ (on a $[0,1]$ scale) is statistically
>   undetectable within 1000 artifacts. However, such a small bias is also
>   practically negligible for score manipulation purposes.
>    $\square$

## Extended Countermeasure Analysis
<!-- label: app:extended -->

### Robustness to Adaptive Adversaries

> **Proposition:** [Adaptive Adversary Bound]
>   <!-- label: prop:adaptive -->
>   Consider an adaptive adversary who observes the detector's output and adjusts
>   the manipulation magnitude $\Delta_t$ at each step $t$. If the adversary is
>   constrained by a cumulative manipulation budget $\sum_{t=1}^T \Delta_t^2 \leq B$,
>   then any detection procedure based on the CUSUM statistic has worst-case
>   detection delay:
>   \[
>     \bbE[delay] \geq \Omega\left(\frac{B}{T}\right).
>   \]

> **Proof:** [Proof sketch]
>   The adversary can distribute the manipulation budget uniformly across $T$ steps,
>   setting $\Delta_t = \sqrt{B/T}$ at each step. Under this strategy, the per-step
>   Kullback-Leibler divergence is $D_{KL,t} = \Delta_t^2/(2\sigma^2) = B/(2T\sigma^2)$.
>   The cumulative information for detection after $n$ steps is $nB/(2T\sigma^2)$,
>   which exceeds the detection threshold $|\log \alpha|$ only when
>   $n \geq 2T\sigma^2|\log \alpha|/B$, yielding the claimed lower bound.  $\square$

### Information-Theoretic Lower Bound (Conjecture)

> **Conjecture:** [Goodhart Impossibility Threshold]
>   <!-- label: conj:impossible -->
>   There exists a universal constant $c > 0$ such that, for any Cercis-based
>   evaluation system, if the adversary's manipulation magnitude satisfies
>   $\Delta < c \cdot \eta^{-1} \cdot \sigma_S$, then *no* statistical test
>   can distinguish manipulated artifacts from legitimate ones with power
>   exceeding $1/2 + o(1)$.

**猜想解读.** 此猜想如果成立，将确立SCX框架中Goodhart防御的**绝对极限**：
存在一个由Cercis参数 $\eta$ 和评分噪声 $\sigma_S$ 决定的不可检测区域。
任何落入此区域的操纵在信息论意义上与随机波动不可区分。
这将是Theorem~3（噪声-难度不可区分性）在操纵检测领域的对偶定理。

## Glossary of Notation
<!-- label: app:notation -->

<div align="center">

[Table omitted — see original .tex]

</div>

\begin{thebibliography}{99}

\bibitem{goodhart1975problems}
C.~A.~E.~Goodhart.
\newblock {\em Problems of Monetary Management: The UK Experience}.
\newblock In {\em Papers in Monetary Economics}, Reserve Bank of Australia, 1975.

\bibitem{strathern1997improving}
M.~Strathern.
\newblock ``Improving ratings'': audit in the British University system.
\newblock {\em European Review}, 5(3):305--321, 1997.

\bibitem{manheim2019categorizing}
D.~Manheim and S.~Garrabrant.
\newblock Categorizing variants of Goodhart's Law.
\newblock arXiv:1803.04585, 2019.

\bibitem{karwowski2024goodhart}
J.~Karwowski, O.~Hagiwara, and T.~Hashimoto.
\newblock Goodhart's Law in Reinforcement Learning.
\newblock In {\em ICLR}, 2024.

\bibitem{zhuang2023goodhart}
S.~Zhuang and D.~Hadfield-Menell.
\newblock Consequences of Misaligned AI.
\newblock In {\em NeurIPS}, 2023.

\bibitem{krakovna2020specification}
V.~Krakovna, J.~Uesato, V.~Mikulik, et~al.
\newblock Specification gaming: the flip side of AI ingenuity.
\newblock {\em DeepMind Blog}, 2020.

\bibitem{scx2025}
SCX Research Collective.
\newblock SCX: An Egalitarian Framework for Multi-Perspective Evaluation.
\newblock Technical Report, 2025.

\bibitem{page1954continuous}
E.~S.~Page.
\newblock Continuous inspection schemes.
\newblock {\em Biometrika}, 41(1/2):100--115, 1954.

\bibitem{lord1955range}
F.~M.~Lord.
\newblock Sampling fluctuations resulting from the sampling of test items.
\newblock {\em Psychometrika}, 20(1):1--22, 1955.

\bibitem{lehmann2006testing}
E.~L.~Lehmann and J.~P.~Romano.
\newblock {\em Testing Statistical Hypotheses}, 3rd ed.
\newblock Springer, 2006.

\bibitem{cover2006elements}
T.~M.~Cover and J.~A.~Thomas.
\newblock {\em Elements of Information Theory}, 2nd ed.
\newblock Wiley, 2006.

\bibitem{ambrosio2008gradient}
L.~Ambrosio, N.~Gigli, and G.~Savar\'e.
\newblock {\em Gradient Flows in Metric Spaces and in the Space of Probability Measures}.
\newblock Birkh\"auser, 2008.

\end{thebibliography}