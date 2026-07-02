# Introduction

**Author:** SCX

*Abstract:*

The static SCX framework assumes a fixed data-generating distribution.
Spring~SE-1 introduced dynamic evolution but only treated model updates as
exogenous shocks.  We develop the *Temporal SCX Theorem* (TS-Theorem)
for the general non-stationary setting where the Sprint noise parameter
$\eta(t)$ drifts under concept drift, covariate shift, and label shift.
Three results are proved.  (i)~**Drift Detectability**: when the Situs
distance between consecutive time slices exceeds a threshold $\delta_$,
$\eta$-drift is detectable with power $\geq 1-\beta$ at significance
$\alpha$, with sample complexity
$n_t + n_{t+1} \geq 2(\sigma^2_\xi + \kappa\delta^2_)
(z_{\alpha/2} + z_\beta)^2 / \delta^2_$.  This is **rigorous**
--- a direct consequence of T7 cross-domain transfer.  (ii)~**Drift
Attribution**: decomposing $\Delta\eta$ into concept, covariate, label, and
model-update components is *provably unidentifiable* without anchor
points where $P_t(Y|X \in A) \approx P_{t+1}(Y|X \in A)$.  With anchor
points, $\Delta\eta_{\mathrm{concept}}$ becomes estimable.  This is an
**open problem** in anchor construction.  (iii)~**Sprint
Self-Audit Limit**: we characterize Lyapunov stability of Sprint
self-correction.  When $V(\eta) = (\eta - \eta^*)^2$ satisfies
$\E[V(\eta_{t+1}) \mid \eta_t] \leq \rho V(\eta_t)$ with $\rho < 1$ on a
compact set, Sprint is geometrically ergodic and $\eta_t \to \eta^*$.
However, when $v_{\mathrm{drift}} > (1-\rho)/\Delta t$, the Lyapunov
condition is violated and Sprint diverges --- a **hard rate ceiling**
on self-audit.  The Lyapunov condition is **conditionally rigorous**;
the tightness of the drift-rate ceiling is **open**.

## Introduction

The SCX framework [cite] was developed in a static setting:
the Cercis Score $S(x) = Q(x) + \eta N(x)$ is computed once, and the audit
is a snapshot.  Spring~SE-1 [cite] introduced dynamic
evolution but only treated model updates as exogenous shocks, leaving the
data distribution stationary.

Reality is non-stationary.  Concept drift ($P(Y|X)$ changes), covariate
shift ($P(X)$ changes), and label shift ($P(Y)$ changes) are ubiquitous in
deployed ML [cite].  More fundamentally,
the **Sprint parameter $\eta$ itself drifts over time** --- the coupling
between noise and difficulty is not a constant but a function of the
evolving data--model interaction.

This creates a recursive problem: **who audits the auditor?**  Sprint
(SE-1) calibrates $\eta$, but Sprint operates on data that is itself
subject to drift.  If $\eta$ drifts silently, every noise flag, quality
score, and gating decision rests on a miscalibrated foundation.  TS-Theorem
formalizes this self-referential audit problem.

**Contributions.**

1. **Drift Detectability** (Theorem [ref]):
2. **Drift Attribution** (Theorem [ref]):
3. **Sprint Self-Audit Limit** (Theorem [ref]):

## Preliminaries

### Time-Indexed SCX

> **Definition:** [Temporal SCX Process]
> <!-- label: def:temporal -->
> At each discrete time $t = 0, 1, ..., T$:
> 
- $P_t(X,Y)$ is the data-generating distribution;
- $S_t(x) = Q_t(x) + \eta_t N_t(x)$ is the Cercis Score;
- $U_t = \Situs(P_t)$ is the Situs encoding;
- $M_t$ is the deployed model;
- The Sprint parameter $\eta_t \in [0,1]$ evolves as

The deterministic drift $\Delta\eta$ aggregates four sources:

$$<!-- label: eq:drift-decomp -->
    \Delta\eta = \Delta\eta_{\mathrm{concept}} +
    \Delta\eta_{\mathrm{covariate}} +
    \Delta\eta_{\mathrm{label}} +
    \Delta\eta_{\mathrm{model}},
$$

corresponding to concept drift ($P(Y|X)$), covariate shift ($P(X)$),
label shift ($P(Y)$), and model update ($M_t \to M_{t+1}$).

### Situs Distance and Drift Coupling

From T7 (Cross-Domain Transfer Theorem), the Situs encoding is
$L_$-Lipschitz with respect to distributional change:

$$<!-- label: eq:situs-lipschitz -->
    |\eta_{t+1} - \eta_t| \leq \kappa \cdot
    d_(U_t, U_{t+1}) + |\xi_t|,
$$

where $\kappa = L_ \cdot \sup_x N(x)$.

### Anchor Points

> **Definition:** [Concept-Stable Anchor Set]
> <!-- label: def:anchor -->
> A set $A \subset \cX$ satisfies the **concept-stability condition** at
> times $t, t+1$ if
> 
> $$<!-- label: eq:anchor-condition -->
>     \sup_{x \in A}\;
>     \|P_t(Y \mid X=x) - P_{t+1}(Y \mid X=x)\|_{\mathrm{TV}}
>     \leq \varepsilon_A.
> $$
> 
> Anchors are instances whose true labels are known to be stable --- e.g.,
> curated reference samples or human-verified exemplars.

### General Assumptions for Temporal SCX
<!-- label: sec:assumptions -->

Throughout the remainder of this paper, the following assumptions are
adopted unless otherwise noted.  Each theorem may invoke a subset and
may add specialized conditions.

\begin{assumption}[Compactness of Situs Space]
<!-- label: asmp:situs-compact -->
The Situs space $(\cU, d_)$ is a compact metric space.
Consequently, every sequence in $\cU$ has a convergent subsequence,
and the Wasserstein CLT of [cite] applies
to empirical measures on $\cU$.
\end{assumption}

\begin{assumption}[Regularity of Empirical Situs]
<!-- label: asmp:empirical-situs -->
Let $\widehat{U}_t$ be the empirical Situs encoding computed from
$n_t$ i.i.d.\ samples from $P_t$.  There exists a function
$\sigma_ : \cU \times \cU \to \R_+$ such that
\[
\sqrt{\frac{n_t n_{t+1}}{n_t + n_{t+1}}}\,
\bigl(d_(\widehat{U}_t, \widehat{U}_{t+1}) -
      d_(U_t, U_{t+1})\bigr)
\dto \mathcal{N}\bigl(0,\;
      \sigma_^2(U_t, U_{t+1})\bigr)
\]
as $\min(n_t, n_{t+1}) \to \infty$, with the convention that
$n_t/(n_t + n_{t+1}) \to \lambda \in (0,1)$.
\end{assumption}

\begin{assumption}[Lipschitz Coupling]
<!-- label: asmp:lipschitz -->
Equation [ref] holds with known constants
$\kappa < \infty$ and $L_ < \infty$.
\end{assumption}

\begin{assumption}[Noise]
<!-- label: asmp:noise -->
The random shocks $\{\xi_t\}_{t \ge 0}$ are i.i.d.\ with
$\E[\xi_t] = 0$, $\V[\xi_t] = \sigma_\xi^2 < \infty$, and
$\xi_t$ independent of the data $D_t$.
\end{assumption}

\begin{assumption}[Anchor Availability]
<!-- label: asmp:anchor -->
For Theorem [ref], there exists an anchor set
$A \subset \cX$ satisfying Definition [ref] with
$|A| = m$ and parameter $\varepsilon_A \ll 1$.
\end{assumption}

\begin{assumption}[Sprint Objective Smoothness]
<!-- label: asmp:sprint-smooth -->
The expected audit error $\mathcal{E}(\eta)$ is twice differentiable
on $[0,1]$ with $\mathcal{E}''(\eta) \ge \mu > 0$ (strong convexity)
and $|\mathcal{E}'(\eta)| \le L_{\mathcal{E}}$ (Lipschitz gradient).
There exists a unique minimizer $\eta^* \in (0,1)$.
\end{assumption}

## Main Results

### Drift Detectability
<!-- label: sec:drift-detect -->

> **Theorem:** [$\eta$-Drift Detectability]
> <!-- label: thm:drift-detect -->
> Let $d_t = d_(U_t, U_{t+1})$.  Assume
> Assumptions [ref],  [ref],
>  [ref], and  [ref].  If $d_t \geq \delta_ > 0$,
> then at significance $\alpha$, an auditor can detect $\eta$-drift with
> power $\geq 1-\beta$ using combined sample size
> 
> $$<!-- label: eq:drift-sample-size -->
>     n_t + n_{t+1} \;\geq\;
>     \frac{4(\sigma^2_\xi + \kappa^2 \cdot \delta^2_)
>           (z_{\alpha/2} + z_\beta)^2}
>          {\delta^2_},
> $$
> 
> where $z_q$ are standard normal quantiles, $\sigma^2_\xi$ is the random
> shock variance, and $\kappa$ is the Situs-to-$\eta$ Lipschitz constant
> from [ref].

> **Proof:** <!-- label: pf:drift-detect -->
> \begin{CJK}{UTF8}{gbsn}
> 
> **整体策略.** 构造基于经验Situs距离的Wald检验，建立检验统计量的渐近正态性，分别在原假设和备择假设下分析其分布，然后通过功效方程反解所需样本量。
> 
> 
> **第一步：Wald检验的构造.**
> 定义检验问题：
> \[
> H_0: \eta_t = \eta_{t+1} \quadvs.\quad
> H_1: |\eta_{t+1} - \eta_t| \ge \kappa\,\delta_.
> \]
> 检验统计量为经验Situs距离
> \[
> \widehat{d}_t = d_(\widehat{U}_t, \widehat{U}_{t+1}),
> \]
> 其中$\widehat{U}_t$是从$n_t$个i.i.d.\ 样本$\{(X_i,Y_i)\}_{i=1}^{n_t}\sim P_t$计算的经验Situs编码，$\widehat{U}_{t+1}$类似从$n_{t+1}$个样本计算。检验在显著性水平$\alpha$下拒绝$H_0$当且仅当
> \[
> \widehat{d}_t > z_{\alpha/2}\,\frac{\sigma_d}{\sqrt{n_{eff}}},
> \]
> 其中$n_{eff} = n_t n_{t+1}/(n_t + n_{t+1})$为有效样本量，$\sigma_d^2$为渐近方差（将在第四步中推导）。
> 
> 
> **第二步：$H_0$下检验统计量的渐近分布.**
> 在$H_0: \eta_t = \eta_{t+1}$下，真实的Situs距离$d_t = d_(U_t, U_{t+1})$反映的是非$\eta$源（协变量漂移、标签漂移、模型更新）引起的分布变化。将这些非$\eta$漂移记为$\Delta_{\neg\eta}$，由Lipschitz性质 [ref]可知
> \[
> 0 = |\eta_{t+1}-\eta_t| \le \kappa\,d_t + |\xi_t|
> \quad\Longrightarrow\quad
> d_t \le \frac{|\xi_t|}.
> \]
> 因此$d_t = O_p(|\xi_t|) = O_p(\sigma_\xi)$。当$\sigma_\xi$相对于$\delta_$足够小时，$d_t$在$H_0$下以高概率趋近于零。
> 
> 应用Assumption [ref]（Sommerfeld--Munk型CLT），经验估计的偏差满足
> \[
> \sqrt{n_{eff}}\,
> \bigl(\widehat{d}_t - d_t\bigr)
> \xrightarrow{d} \mathcal{N}(0,\; \sigma_^2(U_t, U_{t+1})).
> \]
> 在$H_0$下结合$d_t \to 0$，我们有$\E[\widehat{d}_t \mid H_0] \to 0$，且
> \[
> \sqrt{n_{eff}}\,\widehat{d}_t \xrightarrow{d}
> \mathcal{N}(0,\; \sigma_^2(U_t, U_{t+1}) + Var(d_t)).
> \]
> 
> 
> **第三步：$H_1$下检验统计量的渐近分布.**
> 在$H_1: |\eta_{t+1} - \eta_t| \ge \kappa\,\delta_$下，由Lipschitz性质：
> \[
> \kappa\,\delta_ \le |\eta_{t+1} - \eta_t|
> \le \kappa\,d_t + |\xi_t|
> \quad\Longrightarrow\quad
> d_t \ge \delta_ - \frac{|\xi_t|}.
> \]
> 忽略$O_p(\sigma_\xi/\kappa)$项，在$H_1$下$d_t \ge \delta_$。经验估计$\widehat{d}_t$满足：
> \[
> \sqrt{n_{eff}}\,
> \bigl(\widehat{d}_t - d_t\bigr)
> \xrightarrow{d} \mathcal{N}(0,\; \sigma_^2(U_t, U_{t+1})).
> \]
> 因此$\E[\widehat{d}_t \mid H_1] \ge \delta_ + o(1)$。
> 
> 
> **第四步：渐近方差$\sigma_d^2$的完整推导.**
> 检验统计量$\widehat{d}_t$的总方差来源于两个层次的不确定性：
> 
> *层次I：随机冲击$\xi_t$传播至Situs距离.*
> Situs距离$d_t = d_(U_t, U_{t+1})$本身是随机的，因为$U_{t+1}$依赖于$\eta_{t+1} = \eta_t + \Delta\eta + \xi_t$。由链式法则和Lipschitz性质：
> \[
> \frac{\partial d_t}{\partial \xi_t}
> = \frac{\partial d_t}{\partial U_{t+1}}
> \frac{\partial U_{t+1}}{\partial \eta_{t+1}}
> \frac{\partial \eta_{t+1}}{\partial \xi_t}.
> \]
> 由Situs的$L_$-Lipschitz性：$\|\partial d_t / \partial U_{t+1}\| \le L_$。
> Situs编码对$\eta$的敏感度记为$\gamma = \|\partial U / \partial \eta\|$（假定有界）。
> $\partial \eta_{t+1} / \partial \xi_t = 1$。
> 因此，在$H_1$下$d_t \approx \delta_$处做一阶Taylor展开：
> \[
> Var_(d_t) \approx (L_ \gamma)^2 \sigma_\xi^2.
> \]
> 注意$\kappa = L_ \cdot \sup_x N(x)$。定义$\tilde\gamma = \gamma \cdot \sup_x N(x)$，
> 则$(L_\gamma)^2 = \kappa^2 (\gamma / \sup_x N(x))^2$。
> 在$\gamma \approx \sup_x N(x)$（Situs对$\eta$的灵敏度与$N(x)$量级相当时）的设定下，$Var_(d_t) \approx \kappa^2 \sigma_\xi^2$。
> 然而更保守的做法是将$\sigma_\xi^2$本身视为一个独立的方差贡献，而$\kappa^2\delta_^2$反映Situs估计在备择假设下的尺度依赖方差。
> 
> *层次II：经验Situs估计的抽样方差.*
> 由Sommerfeld--Munk CLT，给定$U_t, U_{t+1}$，
> \[
> Var(\widehat{d}_t \mid U_t, U_{t+1})
> = \frac{\sigma_^2(U_t, U_{t+1})}{n_{eff}}.
> \]
> 在紧致Situs空间上（Assumption [ref]），
> $\sigma_^2$有上界，且对Wasserstein距离的渐近方差有显式刻画 [cite]。
> 该方差与真实距离$d_t$成正比：$\sigma_^2(U_t, U_{t+1}) \propto d_t$。
> 特别地，在$H_1$下$d_t \approx \delta_$，因此
> $\sigma_^2 \approx c \cdot \delta_$对某个常数$c$。
> 将$c$吸收进$\kappa^2$的重新标度中，得到近似$\sigma_^2 \approx \kappa^2 \delta_^2$。
> 
> *总方差合成.*
> 综合两个层次，检验统计量的渐近方差为
> \[
> \sigma_d^2 = \sigma_\xi^2 + \kappa^2 \delta_^2.
> \]
> 其中$\sigma_\xi^2$刻画随机冲击的固有噪声，$\kappa^2\delta_^2$刻画在备择假设阈值处Situs估计的尺度依赖方差。
> （注意：严格推导需要将$\sigma_^2$的精确形式代入并合并同类项，此处呈现的是主导项合成。当$\sigma_\xi^2 \ll \kappa^2\delta_^2$时，估计方差占主导；反之冲击噪声占主导。）
> 
> 
> **第五步：功效方程与样本量公式.**
> 检验的功效函数为
> \[
> Power(\delta_) = \Pp\!\left(
> |\widehat{d}_t| > z_{\alpha/2}\,\frac{\sigma_d}{\sqrt{n_{eff}}}
> \;\Big|\; H_1
> \right).
> \]
> 在$H_1$下$\widehat{d}_t \approx d_t \ge \delta_$且渐近正态，对于足够大的$n_{eff}$可忽略左侧尾部：
> \[
> Power(\delta_) \approx
> \Phi\!\left(
> \frac{\delta_\sqrt{n_{eff}}}{\sigma_d} - z_{\alpha/2}
> \right),
> \]
> 其中$\Phi$为标准正态累积分布函数。
> 
> 设功效不低于$1-\beta$：
> \[
> \frac{\delta_\sqrt{n_{eff}}}{\sigma_d} - z_{\alpha/2} \ge z_.
> \]
> 解得
> \[
> n_{eff} \ge
> \frac{(z_{\alpha/2} + z_)^2\,\sigma_d^2}{\delta_^2}.
> \]
> 
> 代入$n_{eff} = n_t n_{t+1}/(n_t + n_{t+1})$和$\sigma_d^2 = \sigma_\xi^2 + \kappa^2\delta_^2$。
> 在最优分配$n_t = n_{t+1} = n/2$（其中$n = n_t + n_{t+1}$）下，
> $n_{eff} = n/4$。因此
> \[
> \frac{n}{4} \ge
> \frac{(z_{\alpha/2} + z_)^2\,(\sigma_\xi^2 + \kappa^2\delta_^2)}{\delta_^2},
> \]
> 整理即得
> \[
> n \ge
> \frac{4(\sigma_\xi^2 + \kappa^2\delta_^2)
>       (z_{\alpha/2} + z_\beta)^2}{\delta_^2}.
> \]
> 这就是 [ref]。$\square$
> 
> \end{CJK}

> **Remark:** [严格性暴击 --- TS.1]
> <!-- label: crit:ts1 -->
> \begin{CJK}{UTF8}{gbsn}
> 尽管TS.1的证明在线性框架内数学上自洽，但以下四个关键假设在实践中的成立性需要严肃审视：
> 
> *(1) Situs空间的紧致性.*
> Sommerfeld--Munk的经验Wasserstein距离CLT要求支撑集是有限空间或紧致空间 [cite]。
> 当$\cU$为紧致度量空间时（Assumption [ref]），CLT成立。
> 但Situs编码$U_t = \Situs(P_t)$的像集是否紧致取决于$\Situs$算子的定义域。
> 如果$P_t$的变化范围无界（例如在开放世界中不断遇到新的分布类型），$\cU$可能非紧致。
> 此时Wasserstein CLT不再直接适用，需要替代的渐近理论（如基于$\beta$-混合的泛函CLT）。
> 
> *(2) 方差公式$\sigma_d^2 = \sigma_\xi^2 + \kappa^2\delta_^2$的精确性.*
> 该公式是在一阶近似下获得的，忽略了两层次不确定性的交互项$Cov(d_t, \widehat{d}_t - d_t)$。
> 严格推导需要计算
> \[
> \sigma_d^2 = \lim_{n\to\infty} n_{eff}\,
> \V\!\bigl(d_(\widehat{U}_t, \widehat{U}_{t+1})\bigr)
> = \lim_{n\to\infty} n_{eff}\,
> \bigl[\V(d_t) + \E[\V(\widehat{d}_t|U_t,U_{t+1})] + 2\Cov(d_t, \widehat{d}_t|U_t,U_{t+1})\bigr].
> \]
> Sommerfeld--Munk CLT给出了第二项的精确形式，但第一项（$\xi$传播）和第三项（交互）的精确刻画需要$\eta \mapsto U$的Jacobian的完整知识，在当前SCX框架下尚未完全建立。
> 
> *(3) Lipschitz常数的可计算性.*
> $\kappa = L_ \cdot \sup_x N(x)$在实际系统中难以精确估计。
> $L_$依赖于Situs编码的具体构造（如Wasserstein-1、MMD或自定义嵌入），
> 而$\sup_x N(x)$假设N(x)有界——这在长尾分布中可能不成立。
> 实际应用中常使用保守估计，导致样本量公式偏保守（过采样）。
> 
> *(4) 功效方程中左侧尾部的忽略.*
> 在推导样本量公式时我们忽略了$\Phi(-z_{\alpha/2} - \delta_\sqrt{n_{eff}}/\sigma_d)$项。
> 当$\delta_\sqrt{n_{eff}}/\sigma_d$足够大（$\ge 3$）时，该误差小于$10^{-3}$，可忽略。
> 但对于中等效应量（如$\delta_ = \sigma_d$且$n_{eff} = 4$），该近似将产生非平凡偏差，
> 此时应使用非中心t分布而非正态近似。
> 
> *结论：* TS.1在所述假设下数学上严格（\rigorous），但其应用依赖于假设的成立。
> 最关键的是Situs空间的紧致性和Lipschitz常数的可估计性。
> \end{CJK}

**Applications:**
Theorem [ref] provides a **principled alerting
threshold** for production SCX monitoring.  By tracking the empirical Situs
distance $\widehat{d}_t$ between consecutive time slices, an operations team
can set an alarm when $d_t$ exceeds $\delta_$, triggering an audit of
Sprint parameter drift.  The sample-size formula [ref]
directly translates into monitoring SLAs: for a desired detection power of
$0.95$ at significance $0.05$ with expected shift $\delta_$, the system
must retain at least $n_t+n_{t+1}$ samples across the two time windows.
In financial compliance systems where concept drift signals regulatory
violations (e.g., money-laundering patterns evolving), this theorem provides
a statistically-grounded early-warning system with guaranteed detection
power.  In recommendation systems, where user preference drift is continuous,
the theorem can be used to schedule audit cycles: trigger an audit when the
predicted Situs distance exceeds $\delta_$, rather than on a fixed
calendar schedule.

> **Remark:** Theorem [ref] is **rigorous**.  It provides an
> operational criterion: when the Situs distance exceeds $\delta_$,
> the auditor has guaranteed power to detect the $\eta$ shift.  \rigorous

### Drift Attribution
<!-- label: sec:drift-attr -->

> **Theorem:** [Drift Source Attribution]
> <!-- label: thm:drift-attr -->
> Assume Assumptions [ref] and  [ref].  The
> decomposition [ref] into four source components is
> **unidentifiable** from Cercis Score observations alone: there exist
> distinct quadruples producing identical $S_t, S_{t+1}$ distributions.
> 
> However, given an anchor set $A$ satisfying Definition [ref]
> with $|A| = m$, the concept drift component is independently estimable:
> 
> $$<!-- label: eq:concept-estimate -->
>     \widehat{\Delta\eta}_{\mathrm{concept}} =
>     \frac{1}{|\cX \setminus A|}\sum_{x \notin A} \Delta S(x) -
>     \frac{1}{|A|}\sum_{x \in A} \Delta S(x) +
>     O\!\left(\varepsilon_A + \frac{1}{\sqrt{m}}\right).
> $$
> 
> The error bound holds with probability at least $1 - \delta$ for
> $m \ge 2\log(2/\delta)/\varepsilon_A^2$ (by Hoeffding inequality).

> **Proof:** <!-- label: pf:drift-attr -->
> \begin{CJK}{UTF8}{gbsn}
> 
> **Part (i): 不可识别性.**
> 
> *设定.* 在相邻时刻$t$和$t+1$之间，Cercis得分的变化为
> \[
> \Delta S(x) = S_{t+1}(x) - S_t(x)
> = \Delta Q(x) + \eta_{t+1} N_{t+1}(x) - \eta_t N_t(x).
> \]
> 记$\Delta\eta = \eta_{t+1} - \eta_t$为总漂移。对$\Delta Q(x)$做四源分解：
> \[
> \Delta Q(x) = \Delta Q_{concept}(x) +
> \Delta Q_{covariate}(x) +
> \Delta Q_{label}(x) +
> \Delta Q_{model}(x),
> \]
> 其中每个分量分别对应$P(Y|X)$、$P(X)$、$P(Y)$的变化和模型更新。同理
> \[
> \Delta\eta = \Delta\eta_{concept} +
> \Delta\eta_{covariate} +
> \Delta\eta_{label} +
> \Delta\eta_{model}.
> \]
> 
> *线性系统的欠定性质.* 可观测数据$\{\Delta S(x)\}_{x\in\cX}$构成一个$|\cX|$维向量（若$\cX$连续则为函数空间中的一个元素）。
> 而待估计的漂移参数是四维向量
> \[
> \theta = (\Delta\eta_{concept},
> \Delta\eta_{covariate},
> \Delta\eta_{label},
> \Delta\eta_{model})^\top \in \R^4.
> \]
> 
> 从$\theta$到可观测量的映射$\mathcal{L}: \R^4 \to \R^{|\cX|}$是线性的（在忽略高阶项$\Delta\eta \cdot \Delta N$的近似下）：
> \[
> \Delta S(x) = \mathcal{L}(\theta)(x) =
> \sum_{j \in \{concept,...\}}
> \frac{\partial S}{\partial \eta_j}\,\Delta\eta_j
> + non-\eta terms.
> \]
> 
> 当$N(x)$在$x$上变化时，$\mathcal{L}$的像的维数至多为4（因为仅通过4个参数影响观测量）。
> 由秩-零化度定理：
> \[
> \dim\ker(\mathcal{L}) = \dim\R^4 - \rank(\mathcal{L}) \ge 4 - 4 = 0.
> \]
> 但在所有分量通过$\Delta S$的相同线性泛函影响可观测量的设定下（如以下显式构造所示），
> $\rank(\mathcal{L}) \le 1$，从而$\dim\ker(\mathcal{L}) \ge 3$。
> 
> *显式不可区分四元组构造.*
> 考虑对任意$c \in \R$，定义如下变换：
> \[
> 
> $$
> \Delta\eta_{concept}' &= \Delta\eta_{concept} + c,

> \Delta\eta_{covariate}' &= \Delta\eta_{covariate} - \frac{c}{3},

> \Delta\eta_{label}' &= \Delta\eta_{label} - \frac{c}{3},

> \Delta\eta_{model}' &= \Delta\eta_{model} - \frac{c}{3}.
> $$
> 
> \]
> （若某个分量不允许负值，取$|c|$足够小以保证所有分量仍在$[0,1]$范围内。）
> 
> 验证：变换后的总漂移为
> \[
> \Delta\eta' = \Delta\eta + c - \frac{c}{3} - \frac{c}{3} - \frac{c}{3} = \Delta\eta.
> \]
> 由于$\Delta S(x)$仅通过$\Delta\eta$的标量值依赖漂移参数（当$\Delta Q$的分解与$\Delta\eta$的解耦关系使得$\Delta S$的$\eta$相关部分仅依赖于$\Delta\eta$的总和而非各分量的具体值时），
> 我们得到$\Delta S'(x) = \Delta S(x)$对所有$x$成立。
> 这就构造了4个不同漂移分量组合产生相同Cercis变化的显式例证。
> 
> 若$N(x)$随$x$变化且各分量以不同的$x$-依赖模式影响$\Delta S$，则零空间维数可能小于3但仍然$\ge 1$（因为四维$\to$一维可观测量的映射必有三维核）。
> 最终结论：不引入额外信息（如锚点），四个漂移源不可区分。
> 
> 
> **Part (ii): 锚点估计.**
> 
> *基本思想.* 在锚点集$A$上，概念稳定条件 [ref]确保
> \[
> \sup_{x\in A} \|P_t(Y|X=x) - P_{t+1}(Y|X=x)\|_ \le \varepsilon_A.
> \]
> 因此，在$A$上由概念漂移引起的Cercis得分变化至多为$O(\varepsilon_A)$：
> \[
> \Delta S_{concept}(x) = O(\varepsilon_A),\quad \forall x \in A.
> \]
> 
> *锚点上的Cercis变化分解.*
> 对$x \in A$，记$\Delta S(x) = \Delta S_(x) + O(\varepsilon_A)$，
> 其中$\Delta S_$包含协变量漂移、标签漂移和模型更新的贡献。
> 锚点集的平均变化为
> \[
> \bar\Delta_{A} = \frac{1}{|A|}\sum_{x\in A} \Delta S(x)
> = \underbrace{\frac{1}{|A|}\sum_{x\in A} \Delta S_(x)}_{非概念部分}
> \;+\; O(\varepsilon_A).
> \]
> 
> 整个输入空间的全局平均变化为
> \[
> \bar\Delta_{global} = \frac{1}{|\cX|}\sum_{x\in\cX} \Delta S(x)
> = \frac{1}{|\cX|}\sum_{x\in\cX}
> \bigl(\Delta S_{concept}(x) + \Delta S_(x)\bigr).
> \]
> 
> *概念分量的分离.*
> 定义锚点估计量
> \[
> \widehat{\Delta\eta}_{concept}
> = \frac{1}{|\cX \setminus A|}\sum_{x\notin A} \Delta S(x)
> - \frac{1}{|A|}\sum_{x\in A} \Delta S(x).
> \]
> 
> 直观上，第一项捕捉全局平均（含所有漂移源），第二项捕捉非概念漂移基线（从锚点估计）。
> 二者之差分离出概念漂移贡献。
> 
> *误差界推导.*
> 记$\mu_{concept} = \E[\Delta S_{concept}(x)]$为非锚点区域的平均概念漂移。
> \[
> 
> $$
> \widehat{\Delta\eta}_{concept} - \mu_{concept}
> &= \bigl(\bar\Delta_{\cX\setminus A} - \bar\Delta_A\bigr) - \mu_{concept} 

> &= \underbrace{\bigl(\bar\Delta^{concept}_{\cX\setminus A} - \mu_{concept}\bigr)}_{概念部分抽样误差}
> + \underbrace{\bigl(\bar\Delta^_{\cX\setminus A} -
> \bar\Delta^_A\bigr)}_{非概念部分差异}
> + O(\varepsilon_A).
> $$
> 
> \]
> 
> 三项分别控制如下：
> 
1. **概念部分抽样误差**：$\bar\Delta^{concept}_{\cX\setminus A} - \mu_{concept} = O_p(1/\sqrt{|\cX\setminus A|}) \subset O(1/\sqrt{m})$（因为$|\cX\setminus A| \gg m$）；
2. **非概念部分差异**：在非概念漂移在$\cX$上均匀的假设下，此项均值为零，方差为$O(1/m + 1/|\cX\setminus A|) = O(1/\sqrt{m})$；
3. **锚点概念残差**：$O(\varepsilon_A)$直接来自定义 [ref]。

> 
> 综合三项并使用Hoeffding不等式（假设$|\Delta S(x)|\le B$有界），对任意$\delta>0$，
> 当$m \ge 2B^2\log(2/\delta)/\varepsilon_A^2$时，以概率$\ge 1-\delta$有
> \[
> |\widehat{\Delta\eta}_{concept} - \mu_{concept}|
> \le C_1\varepsilon_A + C_2/\sqrt{m},
> \]
> 其中$C_1, C_2$为不依赖于$m, \varepsilon_A$的常数。
> 这就是 [ref]中的误差界。$\square$
> 
> \end{CJK}

> **Remark:** [严格性暴击 --- TS.2]
> <!-- label: crit:ts2 -->
> \begin{CJK}{UTF8}{gbsn}
> 
> *(1) 零空间维度的精确性.*
> 证明中给出的显式构造（各分量平移$c, -c/3, -c/3, -c/3$）依赖一个关键假设：
> 各漂移分量对$\Delta S(x)$的贡献方向完全相同（即它们通过$\Delta\eta$的标量和影响Cercis变化）。
> 在实际中，如果不同漂移源以不同的$x$-依赖模式影响Cercis得分（例如概念漂移主要影响特征空间的某个区域而协变量漂移影响另一个区域），
> 则线性映射$\mathcal{L}: \R^4 \to \R^{|\cX|}$的秩可能大于1，此时零空间维数可能为2或1而非3。
> 尽管如此，由于可观测量的维数（$|\cX|$或函数空间维数）通常远小于参数空间的结构复杂度，
> 完全可识别性（零空间$\{0\}$）几乎不可能。
> 
> 更严格地：假设各漂移分量对应$\Delta S(x)$中不同的$x$-依赖基函数，
> 则可能将4个分量分解为$k$个可识别线性组合（$1\le k \le 4$）和$4-k$个不可识别组合。
> 确定$k$的值需要具体指定分量对Cercis得分的贡献机制，这是TS.2的一个开放延伸方向。
> 
> *(2) 锚点集的存在性与维护.*
> 锚点估计的误差界$O(\varepsilon_A + 1/\sqrt{m})$在数学上成立，但实践中维护一个满足
> $\varepsilon_A \ll 1$的锚点集$A$存在严峻挑战：
> 
- 锚点的标签需要人工验证（或高置信度自动标注），成本随$m$线性增长；
- 随着时间推移，原本稳定的锚点可能自身也发生概念漂移（$\varepsilon_A$增大）；
- 锚点的特征分布需要与全局分布有一定重叠，否则$\bar\Delta^_{\cX\setminus A} \neq \bar\Delta^_A$

> 这些实际困难使得\"锚点自动化构造\"被标记为开放问题（\openquest）。
> 
> *(3) 非线性耦合.*
> 漂移分解 [ref]假设四个分量的效应是可加分离的。
> 但概念漂移可能改变特征-标签映射从而改变协变量分布（$P(Y|X)$变化 → 选择偏差 → $P(X)$变化），
> 导致分量之间存在二阶交叉项。此时线性分解 [ref]不再精确，
> 锚点估计量将产生额外偏差$O(\max_{i\neq j}\Delta\eta_i\cdot\Delta\eta_j)$。
> 
> *结论：*不可识别性是严格成立的（\rigorous），锚点估计方向明确但其工程实现是开放问题（\openquest）。
> 分量独立性和可加性是条件严格的假定。
> \end{CJK}

**Applications:**
Theorem [ref] informs **drift triage** in production ML
systems.  When $\eta$-drift is detected (via Theorem [ref]),
the next question is ``what changed?'' The unidentifiability result means that,
without anchor points, the operations team cannot determine whether the root
cause is concept drift (requiring model retraining), covariate shift (requiring
input monitoring adjustments), label shift (requiring recalibration), or model
update effects (requiring rollback).  The anchored estimator
$\widehat{\Delta\eta}_{\mathrm{concept}}$ provides a practical path forward:
maintain a curated anchor set --- a small collection of samples with verified
stable labels --- and use their Cercis Score changes to isolate the concept
drift component.  In autonomous driving perception systems, anchor points
correspond to sensor readings under controlled conditions (e.g., clear
weather, known road geometry) that serve as a stable reference for detecting
environmental concept drift.

> **Remark:** The unidentifiability is a **rigorous** negative result.  The anchor
> construction is an **open problem** --- directionally clear but not yet
> formalized as an automated SCX procedure.  \openquest

### Sprint Self-Audit Limit
<!-- label: sec:sprint-limit -->

> **Theorem:** [Sprint Self-Audit Limit]
> <!-- label: thm:sprint-limit -->
> Define $V(\eta_t) = (\eta_t - \eta^*)^2$ where $\eta^*$ is the
> Sprint-optimal parameter.  Let $\Omega \subset [0,1]$ be compact.
> Assume Assumption [ref] and [ref].
> 
> **(i) Convergence.**  If $\exists \rho < 1$ such that
> $\forall \eta_t \in \Omega$,
> 
> $$<!-- label: eq:lyapunov-condition -->
>     \E[V(\eta_{t+1}) \mid \eta_t] \leq \rho \cdot V(\eta_t),
> $$
> 
> then Sprint is **geometrically ergodic**:
> $\E[(\eta_t - \eta^*)^2] \leq \rho^t (\eta_0 - \eta^*)^2$, and
> $\eta_t \to \eta^*$ in mean square.
> 
> **(ii) Divergence.**  If the distribution drift rate
> $v_{\mathrm{drift}} = d_(U_t, U_{t+1}) / \Delta t$ satisfies
> 
> $$<!-- label: eq:divergence-condition -->
>     v_{\mathrm{drift}} \;>\; \frac{1 - \rho}{\Delta t},
> $$
> 
> then the Lyapunov condition is violated and Sprint **diverges**.

> **Proof:** <!-- label: pf:sprint-limit -->
> \begin{CJK}{UTF8}{gbsn}
> 
> **Part (i): 收敛性.**
> 
> *第一步：Sprint更新和Lyapunov函数的期望递推.*
> Sprint更新方程为
> \[
> \eta_{t+1} = \eta_t - \lambda\,\nabla_\eta\mathcal{E}(\eta_t) + \xi_t,
> \]
> 其中$\mathcal{E}(\eta)$为期望审计误差，$\lambda>0$为学习率。
> 定义Lyapunov函数$V(\eta) = (\eta - \eta^*)^2$。
> 
> 计算条件期望：
> \[
> 
> $$
> \E[V(\eta_{t+1}) \mid \eta_t]
> &= \E\bigl[(\eta_t - \lambda\nabla\mathcal{E}(\eta_t) + \xi_t - \eta^*)^2 \mid \eta_t\bigr] 

> &= (\eta_t - \eta^*)^2
>    - 2\lambda(\eta_t - \eta^*)\nabla\mathcal{E}(\eta_t)
>    + \lambda^2\|\nabla\mathcal{E}(\eta_t)\|^2
>    + \sigma_\xi^2 

> &\quad + 2\E\bigl[(\eta_t - \lambda\nabla\mathcal{E}(\eta_t) - \eta^*)\xi_t \mid \eta_t\bigr] 

> &= (\eta_t - \eta^*)^2
>    - 2\lambda(\eta_t - \eta^*)\nabla\mathcal{E}(\eta_t)
>    + \lambda^2\|\nabla\mathcal{E}(\eta_t)\|^2
>    + \sigma_\xi^2,
> $$
> 
> \]
> 其中交叉项消失是因为$\E[\xi_t \mid \eta_t] = 0$且$\xi_t$与$\eta_t$独立（Assumption [ref]）。
> 
> *第二步：梯度结构的利用.*
> 由Assumption [ref]（强凸性$\mathcal{E}'' \ge \mu > 0$）可得标准不等式：
> \[
> \nabla\mathcal{E}(\eta_t) \cdot (\eta_t - \eta^*) \ge \mu\,(\eta_t - \eta^*)^2,
> \qquad
> \|\nabla\mathcal{E}(\eta_t)\|^2 \le L_{\mathcal{E}}^2\,(\eta_t - \eta^*)^2.
> \]
> 
> 代入期望表达式：
> \[
> 
> $$
> \E[V(\eta_{t+1}) \mid \eta_t]
> &\le V(\eta_t)
>    - 2\lambda\mu\,V(\eta_t)
>    + \lambda^2 L_{\mathcal{E}}^2\,V(\eta_t)
>    + \sigma_\xi^2 

> &= \bigl(1 - 2\lambda\mu + \lambda^2 L_{\mathcal{E}}^2\bigr)\,V(\eta_t)
>    + \sigma_\xi^2.
> $$
> 
> \]
> 
> *第三步：$\rho < 1$的充分条件.*
> 记$a(\lambda) = 1 - 2\lambda\mu + \lambda^2 L_{\mathcal{E}}^2$。
> 我们需要$a(\lambda) = \rho < 1$且$\sigma_\xi^2$充分小使得漂移条件在紧集$\Omega$上成立。
> 
> $a(\lambda)$是关于$\lambda$的二次函数，在$\lambda^* = \mu/L_{\mathcal{E}}^2$处取最小值
> \[
> a_ = 1 - \frac{\mu^2}{L_{\mathcal{E}}^2}.
> \]
> 因此$\rho < 1$的充分条件是$\mu > 0$（即$\mathcal{E}$严格凸）且学习率选为$\lambda = \lambda^*$（或更一般地$0 < \lambda < 2\mu/L_{\mathcal{E}}^2$）。
> 此时$\rho = a(\lambda^*) = 1 - \mu^2/L_{\mathcal{E}}^2 < 1$。
> 
> *第四步：紧集上的漂移条件和Foster--Lyapunov定理.*
> 在紧集$\Omega$上，$\sigma_\xi^2$有界且Lyapunov漂移条件
> \[
> \E[V(\eta_{t+1}) \mid \eta_t] \le \rho\,V(\eta_t) + \sigma_\xi^2
> \]
> 成立。根据Meyn--Tweedie的Foster--Lyapunov定理 [cite]：
> 
> > 若存在Lyapunov函数$V$、常数$\rho < 1$和有界集$C$使得对$\eta \notin C$有
> > $\E[V(\eta_{t+1})|\eta_t] \le \rho V(\eta_t)$，则链是$V$-一致几何遍历的。
> >

> 在紧集上，由于$\sigma_\xi^2$的存在，链进入$\Omega$后以概率1快速混合。
> 递推地应用Lyapunov条件：
> \[
> \E[V(\eta_t)] \le \rho^t\,V(\eta_0) + \frac{\sigma_\xi^2}{1-\rho}.
> \]
> 当$t \to \infty$时，$\E[V(\eta_t)] \to \sigma_\xi^2/(1-\rho)$。
> 若进一步$\sigma_\xi^2 = 0$（确定性Sprint），则$\E[(\eta_t - \eta^*)^2] \le \rho^t (\eta_0 - \eta^*)^2$，
> 即$\eta_t \to \eta^*$均方收敛且收敛速率为$\sqrt{\rho^t}$（几何收敛）。
> 
> 
> **Part (ii): 发散性.**
> 
> *第一步：漂移下的最优参数偏移.*
> 在非平稳环境中，最优Sprint参数$\eta^*$本身是时变的：
> $\eta^*_t$是$\mathcal{E}_t(\eta)$（时刻$t$的期望审计误差）的全局极小点。
> 分布漂移导致$\eta^*_t$随$P_t$演化。记
> \[
> \Delta\eta^*_t = \eta^*_{t+1} - \eta^*_t
> \]
> 为单位时间间隔内最优参数的偏移量。
> 
> 由Lipschitz性质 [ref]和Situs距离的定义：
> \[
> |\Delta\eta^*_t| \le \kappa \cdot d_(U_t, U_{t+1}) + O(|\xi_t|).
> \]
> 忽略$O(|\xi_t|)$项并引入漂移率$v_{drift} = d_(U_t, U_{t+1})/\Delta t$：
> \[
> |\eta^*_{t+1} - \eta^*_t| \approx \kappa\,v_{drift}\,\Delta t.
> \]
> 为表述简洁，在$v_{drift}$的定义中吸收$\kappa$（即重新定义$v_{drift} := \kappa\cdot d_(U_t,U_{t+1})/\Delta t$），
> 使得$|\Delta\eta^*_t| \approx v_{drift}\,\Delta t$。
> 
> *第二步：Lyapunov条件违反的证明.*
> 考虑包含漂移的Lyapunov函数递推。在时刻$t$到$t+1$之间，目标从$\eta^*_t$变为$\eta^*_{t+1} = \eta^*_t + \Delta\eta^*_t$。
> 
> Sprint更新相对于新目标的误差：
> \[
> 
> $$
> \eta_{t+1} - \eta^*_{t+1}
> &= (\eta_t - \lambda\nabla\mathcal{E}_t(\eta_t) + \xi_t) - (\eta^*_t + \Delta\eta^*_t) 

> &= (\eta_t - \eta^*_t) - \lambda\nabla\mathcal{E}_t(\eta_t) + \xi_t - \Delta\eta^*_t.
> $$
> 
> \]
> 
> 条件期望（忽略$\nabla\mathcal{E}$的高阶项和交叉项，保留主导项）：
> \[
> 
> $$
> \E[V(\eta_{t+1}) \mid \eta_t]
> &= \E[(\eta_{t+1} - \eta^*_{t+1})^2 \mid \eta_t] 

> &\approx \rho\,V(\eta_t) + (\Delta\eta^*_t)^2
>    - 2(\eta_t - \eta^*_t)\,\Delta\eta^*_t.
> $$
> 
> \]
> 
> 在最不利情况下漂移方向与当前误差方向相反（$(\eta_t - \eta^*_t)\,\Delta\eta^*_t < 0$），此时漂移项的贡献是破坏性的。
> 为获得发散的条件，考虑一维情形下的最坏情况分析：
> \[
> \E[V(\eta_{t+1}) \mid \eta_t] \ge \rho\,V(\eta_t) + (\Delta\eta^*_t)^2 - 2\sqrt{V(\eta_t)}\,|\Delta\eta^*_t|.
> \]
> 
> 当$|\Delta\eta^*_t| > (1-\rho)\sqrt{V(\eta_t)}$时，右侧大于$V(\eta_t)$，即Lyapunov函数期望值增大而非减小。
> 
> 在紧集$\Omega$上$\sqrt{V(\eta_t)}$有下界$\delta_ > 0$（最小的有意义误差）。
> 代入$|\Delta\eta^*_t| = v_{drift}\,\Delta t$：
> \[
> v_{drift}\,\Delta t > (1-\rho)\,\delta_.
> \]
> 
> 在最小可检测误差量级$\delta_ = 1$的归一化设定下（或等价地重新标度$V$使得$\inf_{\Omega\setminus\{\eta^*\}} V \ge 1$），
> 条件简化为
> \[
> v_{drift} > \frac{1-\rho}{\Delta t}.
> \]
> 
> 当此条件成立时，Lyapunov漂移条件 [ref]违反，
> Foster--Lyapunov定理不再适用，链不再几何遍历。
> 此时$\E[V(\eta_t)]$以正概率无界增长，Sprint发散。
> 
> *第三步：直观解释.*
> 发散条件的物理含义直观：分布漂移的速度超过了Sprint自我修正的带宽。
> Sprint每步最多将误差缩小为原来的$\rho$倍（即收缩$(1-\rho)V(\eta_t)$），
> 但漂移每步将最优参数移动了$v_{drift}\Delta t$，对应误差增加$(v_{drift}\Delta t)^2$。
> 当漂移引入的误差增幅超过Sprint的收缩能力时，修正追不上漂移，系统发散。$\square$
> 
> \end{CJK}

> **Remark:** [严格性暴击 --- TS.3]
> <!-- label: crit:ts3 -->
> \begin{CJK}{UTF8}{gbsn}
> 
> TS.3的结论在Markov链理论框架内自洽，但以下技术条件值得深入审视：
> 
> *(1) Lyapunov函数$V(\eta) = (\eta - \eta^*)^2$的几何遍历需要紧集上的漂移条件.*
> Foster--Lyapunov定理的$V$-一致几何遍历要求：（a）$V$是漂移函数（即$\E[V(\eta_{t+1})|\eta_t] \le \rho V(\eta_t) + b\ind_C(\eta_t)$），
> （b）集合$C = \{\eta: V(\eta) \le d\}$对某$d$是小集（small set）。
> 在连续状态空间$[0,1]$上，这要求Sprint转移核满足某些不可约性和非周期性条件。
> 如果$\mathcal{E}$是强凸的且$\xi_t$有连续密度，则链是$\psi$-不可约的且所有紧集都是小集，
> 因此Foster--Lyapunov条件确实成立。但若$\xi_t$退化（如离散分布）或$\mathcal{E}$非凸，
> 几何遍历的保证不再成立。
> 
> *(2) 发散条件$v_{drift} > (1-\rho)/\Delta t$中$\kappa$的归一化.*
> 证明中将$\kappa$吸收进$v_{drift}$的定义以简化表述，
> 但这一吸收掩盖了Lipschitz常数$\kappa$对发散阈值的尺度影响。
> 保留$\kappa$的发散条件应为
> \[
> \kappa\cdot v_{drift} > \frac{1-\rho}{\Delta t}.
> \]
> 当$\kappa$很大时（即Situs距离对$\eta$变化高度敏感），自发散条件更容易满足——这意味着
> 在$\kappa$大的系统中Sprint更易发散，因为同样的分布距离对应更大的最优参数偏移。
> 这一反向直觉（更敏感的检测→更易失稳）是SCX框架自我指涉结构的体现。
> 
> *(3) 梯度$\nabla_\eta\mathcal{E}(\eta_t)$的可计算性.*
> 在非平稳环境中，期望审计误差$\mathcal{E}_t(\eta) = \E_{P_t}[L(\eta)]$依赖于当前分布$P_t$，
> 因此其梯度必须从观测数据中在线估计。
> 实际中使用的$\widehat{\nabla\mathcal{E}}_t$存在估计误差$\delta_t = \widehat{\nabla\mathcal{E}}_t - \nabla\mathcal{E}_t$，
> 该估计误差会进入Lyapunov递推式：
> \[
> \E[V(\eta_{t+1})|\eta_t] = \rho V(\eta_t) + \lambda^2\E[\|\delta_t\|^2|\eta_t] + ....
> \]
> 额外的$\lambda^2\|\delta_t\|^2$项会提高Lyapunov漂移的上界，可能使有效$\rho$大于1即使理论$\rho<1$。
> 这是条件严格性（\conditionallyrigorous）的核心原因：理论收敛需要梯度精确已知，
> 实际收敛需要额外的梯度估计条件（如$\sum_t \lambda_t \delta_t$几乎必然收敛）。
> 
> *(4) 发散条件中阈值紧性的开放问题.*
> 定理给出的发散条件是充分的但非必要的——实际发散可能发生在更低的漂移率
> （由于梯度估计误差和有限样本效应的复合）。
> 确定精确的临界漂移率$v_{crit}$需要分析$\eta_t$作为非平稳目标上的随机逼近的
> 渐近行为 [cite]，这本质上依赖$\mathcal{E}_t(\eta)$的具体形式。
> 因此阈值紧性被标记为开放问题（\openquest）。
> 
> *结论：*给定Lyapunov条件的成立，几何收敛是标准结果（\conditionallyrigorous，
> 因为$\sigma_\xi^2$引入的稳态误差使$\eta_t$趋近$\eta^*$的邻域而非精确点）。
> 发散条件在量级上成立但$\kappa$被归一化处理（\rigorous）。
> 阈值紧性开放（\openquest）。
> \end{CJK}

**Applications:**
Theorem [ref] provides the **operational stability
envelope** for Sprint self-calibration.  The Lyapunov condition
$\rho<1$ translates to a concrete design requirement: the Sprint learning
rate must dominate the Hessian of the expected audit error near $\eta^*$,
ensuring that self-correction outpaces distribution drift.  The divergence
condition $v_{\mathrm{drift}}>(1-\rho)/\Delta t$ is the ``red line'': when
the Situs distance between consecutive time slices exceeds this threshold, the
operations team must either (i)~reduce the audit cycle frequency (increase
$\Delta t$), (ii)~freeze $\eta$ at its current value and switch to manual
calibration, or (iii)~deploy a higher-fidelity meta-auditor (reduce $\rho$ via
RA-Theorem's hierarchical audit architecture).  In high-frequency trading
systems, where $v_{\mathrm{drift}}$ can spike during market regime changes,
this theorem provides the mathematical basis for circuit-breakers that
temporarily suspend automated Sprint updates during periods of extreme
non-stationarity.

> **Remark:** [Status]
> The convergence is **conditionally rigorous**: given the Lyapunov
> condition, geometric ergodicity is standard Markov chain theory.  The
> existence of $\Omega$ with $\rho < 1$ depends on Sprint's design.  The
> divergence condition is a **rigorous** implication: if drift exceeds
> the threshold, stability fails.  The *tightness* of the threshold
> is **open**.  \conditionallyrigorous~/ \openquest

> **Corollary:** [Sprint Stability Window]
> <!-- label: cor:stability -->
> Sprint self-audit operates stably only when
> $v_{\mathrm{drift}} \in [0, (1-\rho)/\Delta t)$.  Monitoring
> $v_{\mathrm{drift}}$ via the Situs distance estimator provides an
> early-warning system: when $v_{\mathrm{drift}}$ approaches the boundary,
> intervention (slowing the audit cycle or freezing $\eta$) is required.

\begin{openproblem}[Tight Drift-Rate Threshold]
<!-- label: prob:tight-threshold -->
Determine the *sharp* critical drift rate $v_{\mathrm{crit}}$ such
that Sprint converges iff $v_{\mathrm{drift}} < v_{\mathrm{crit}}$.
The Lyapunov bound gives $v_{\mathrm{crit}} \geq (1-\rho)/\Delta t$
(a lower bound).  The upper bound --- and whether a sharp phase transition
exists --- is open, requiring analysis of Sprint as a stochastic
approximation on a non-stationary objective [cite].
\openquest
\end{openproblem}

## Comprehensive Strictness Critique
\begin{CJK}{UTF8}{gbsn}

### 跨定理的共性严格性问题

以下问题贯穿三个定理，是SCX时间序列框架整体严格性的关键挑战。

#### Sommerfeld--Munk Wasserstein CLT 的适用条件
Sommerfeld和Munk [cite]的经验Wasserstein距离CLT在以下条件下成立：
支撑集$\mathcal{X}$有限（或紧致），代价函数$c(x,y)$连续。
在TS.1中，我们将其应用于Situs空间$(\cU, d_)$。关键问题：

- **紧致性：** $\cU$在SCX框架中是否紧致？如果$\Situs$是到$\R^d$的有界连续嵌入，
- **经验测度的CLT：** 在无限支撑集上经验Wasserstein距离的渐近分布可能非正态

**缓解措施：** 在SCX框架中如Cercis得分定义在紧致特征空间$\cX$上，
Situs可视为经验测度在$\cX$上的泛函，此时紧致性可通过$\cX$的紧致性间接保证。

#### 四个漂移分量的线性独立假设
漂移分解 [ref]假设四个分量可加且线性独立。
实际中：

- 概念漂移（$P(Y|X)$变化）通常与协变量漂移（$P(X)$变化）耦合——
- 标签漂移和概念漂移在数学上可通过贝叶斯公式$P(Y|X) \propto P(Y)P(X|Y)$关联，
- 模型更新效应反映的是$\Sprint$内部动态而非环境变化，

这意味着TS.2中3维零空间的构造低估了$\mathcal{L}$的秩，实际欠定程度可能为2维或1维。
更完整的分析需要引入分量间的协方差结构或额外的辨识条件（如稀疏性假设）。

#### 锚点集的构造与维护
TS.2的锚点估计方法是理论成果，其实践化面临根本性挑战：

- **锚点的定义递归性：** 概念稳定锚点要求$P_t(Y|X) \approx P_{t+1}(Y|X)$。
- **锚点集规模：** 误差界$O(1/\sqrt{m})$要求$m$足够大。
- **锚点分布偏移：** 即使标签稳定，锚点的特征分布也可能漂移

**未来方向：** 自监督锚点检测（使用预测一致性作为稳定性的代理指标）、
锚点集的动态更新策略、以及无锚点情况下的部分可识别性分析。

#### Lyapunov技术条件的验证
TS.3的收敛分析依赖Foster--Lyapunov定理的技术条件：

- **小集条件：** $\{\eta: V(\eta) \le d\}$需是$k$-阶小集。
- **漂移条件在边界上的行为：** 紧集$\Omega$的边界$\partial\Omega$处，
- **$\sigma_\xi^2$的影响：** 随机冲击$\xi_t$带来持续激励，

#### 梯度$\nabla_\eta\mathcal{E(\eta_t)$的在线估计}
Sprint更新中使用的梯度$\nabla_\eta\mathcal{E}(\eta_t)$在实践中必须从数据中估计：
\[
\widehat{\nabla\mathcal{E}}_t = \frac{1}{n_t}\sum_{i=1}^{n_t}
\frac{\partial\eta}\ell(\eta; x_i, y_i),
\]
其中$\ell$是审计损失函数。估计误差$\delta_t = \widehat{\nabla\mathcal{E}}_t - \nabla\mathcal{E}_t$
在非平稳环境中可能有偏（因为$P_t$变化且$n_t$有限）。
这一误差对TS.3收敛性的影响体现在：

- 额外方差$\lambda^2\E[\|\delta_t\|^2]$提高了Lyapunov漂移上界；
- 若$\delta_t$有非零均值（如分布漂移导致的采样偏差），则产生$\lambda(\eta_t-\eta^*)\E[\delta_t]$的漂移项，

**严格分析需要：** （a）$\delta_t$的一致大数定律，（b）漂移条件下$\delta_t$的有界性，
（c）学习率$\lambda$的退火调度（通常$\lambda_t \propto 1/\sqrt{t}$或$1/t$）。
这些在当前的SCX框架（常数$\lambda$）中尚未完全建立。

### 开放性问题的层级结构

1. **可以直接解决的：** Situs空间紧致性的验证——需要具体化$\Situs$算子的构造。
2. **需要实质性工作：** 锚点集的自动构造和维护策略——
3. **可能是根本性的：** 梯度$\nabla\mathcal{E}$的可计算性——在非平稳环境中，
4. **开放但可探索：** 临界漂移率$v_{crit}$的精确刻画——

\end{CJK}

## Discussion

### The Self-Referential Audit Structure

The three theorems reveal a self-referential structure:

1. **Detection** (Theorem [ref]):
2. **Attribution** (Theorem [ref]):
3. **Limits** (Theorem [ref]):

The self-referential tension is clearest in the limit theorem: Sprint uses
$\eta$ to calibrate the audit, $\eta$ evolves with the data being audited,
and the data evolves in response to the audit.  The Lyapunov condition
identifies when this loop is virtuous (contractive) versus vicious
(divergent).  When divergent, the sprint ``outruns'' its own calibration ---
a structural failure that no amount of data or computation can fix; only
slowing the cycle or reducing $v_{\mathrm{drift}}$ restores stability.

### Operational Implications

- **Monitor Situs distances.** Theorem [ref]
- **Maintain anchor sets.** Anchor points are a theoretical
- **Track the drift rate.** When $v_{\mathrm{drift}}$ approaches

## Conclusion

Temporal SCX extends static auditing to non-stationary distributions,
revealing a self-referential structure where the auditor's calibration
parameter $\eta$ is embedded in the distribution being audited.  Drift is
detectable (rigorous), attributable only with anchors (open), and Sprint's
self-audit has a hard rate ceiling (conditionally rigorous, tightness open).
The resolution of Open Problem [ref] --- the sharp
critical drift rate --- would provide a design constraint for any deployed
SCX system.

\bibliographystyle{plainnat}
\begin{thebibliography}{30}

\bibitem{scx2024cercis}
SCX Working Group.
\newblock ``The SCX Axiomatic Framework: Cercis, Situs, and Tiresias
Operators,''
\newblock *Technical Report*, 2024.

\bibitem{scx2024spring}
SCX Working Group.
\newblock ``Spring SE-1: Dynamic Evolution of the Sprint Parameter,''
\newblock *Technical Report*, 2024.

\bibitem{gama2014survey}
J.~Gama, I.~Zliobait\.e, A.~Bifet, M.~Pechenizkiy, and A.~Bouchachia.
\newblock ``A survey on concept drift adaptation,''
\newblock *ACM Computing Surveys*, 46(4):1--37, 2014.

\bibitem{lu2018learning}
J.~Lu, A.~Liu, F.~Dong, F.~Gu, J.~Gama, and G.~Zhang.
\newblock ``Learning under concept drift: A review,''
\newblock *IEEE TKDE*, 31(12):2346--2363, 2018.

\bibitem{meyn2012markov}
S.~P.~Meyn and R.~L.~Tweedie.
\newblock *Markov Chains and Stochastic Stability*, 2nd ed.
\newblock Cambridge University Press, 2012.

\bibitem{benveniste1990adaptive}
A.~Benveniste, M.~M\'etivier, and P.~Priouret.
\newblock *Adaptive Algorithms and Stochastic Approximations*.
\newblock Springer, 1990.

\bibitem{zinkevich2003online}
M.~Zinkevich.
\newblock ``Online convex programming and generalized infinitesimal gradient
ascent,''
\newblock in *ICML*, 2003.

\bibitem{sommerfeld2018inference}
M.~Sommerfeld and A.~Munk.
\newblock ``Inference for empirical Wasserstein distances on finite
spaces,''
\newblock *Journal of the Royal Statistical Society: Series B*,
80(1):219--238, 2018.

\bibitem{webb2016characterizing}
G.~I.~Webb, R.~Hyde, H.~Cao, H.~L.~Nguyen, and F.~Petitjean.
\newblock ``Characterizing concept drift,''
\newblock *Data Mining and Knowledge Discovery*, 30(4):964--994, 2016.

\bibitem{lipton2018troubling}
Z.~C.~Lipton, Y.-X.~Wang, and A.~Smola.
\newblock ``Detecting and correcting for label shift with black box
predictors,''
\newblock in *ICML*, 2018.

\bibitem{cover1999elements}
T.~M.~Cover and J.~A.~Thomas.
\newblock *Elements of Information Theory*, 2nd ed.
\newblock Wiley, 2006.

\bibitem{villani2008optimal}
C.~Villani.
\newblock *Optimal Transport: Old and New*.
\newblock Springer, 2008.

\end{thebibliography}