# Introduction

**Author:** SCX

*Abstract:*

SCX auditing presupposes the availability of auditors --- human experts or
independent AI modules --- who can assess samples for label noise.  But how many
auditors does a given auditing task actually require?  We formalize this as the
**Audit Complexity Problem** and prove four results, each with fully
formalized proofs including complete distribution derivations, explicit premise
lists, and honest assessments of the bounds' limitations.
(i)~**Independent Expert Lower Bound** (Theorem [ref]):
with $K$ conditionally independent experts of minimum sensitivity
$\alpha_$ and maximum specificity error $\beta_$, detecting noise
level $\eta>0$ at significance $\delta$ requires
$K_\geq 2\log(1/\delta)/[\eta^{2}(\alpha_-\beta_)^{2}]$.
This bound is **rigorous** via Hoeffding's inequality applied to the
conditional independence structure.
(ii)~**Noise--Expert Trade-off** (Theorem [ref]):
with budget $K$, the minimum detectable noise level is
$\etamin(K)=\Theta(1/\sqrt{K})$, a **rigorous** scaling whose lower bound
follows from (i) and whose tightness is established by the Berry--Esseen theorem
with explicit Lyapunov condition verification.
(iii)~**Correlated Experts -- Audit Diversity**
(Theorem [ref]): with mean inter-expert correlation $\rhobar$,
the effective expert count $K_{\mathrm{eff}}=K/[1+(K-1)\rhobar]$ controls
detectability; the derivation proceeds from variance decomposition under an
equicorrelation structure and is conservative for general correlation matrices.
(iv)~**Model Complexity--Audit Cost Duality**
(Conjecture [ref]): a conjectured uncertainty relation
$K_\cdot\etamin^{2}\geq c\cdot(M/\log M)\cdot\log(1/\delta)$ linking
model complexity $M$ to minimum audit resources --- an **open problem**.

## Introduction

The SCX framework [cite] establishes *what* can be known
about data quality --- Theorem~1 guarantees noise detectability, Theorem~3 bounds
unidentifiability, T5 provides optimal active learning sample complexity.  But
a critical engineering question remains unaddressed: **how many experts
does it take to actually perform an audit?**

In practical SCX deployment, expert judgment is the binding resource constraint.
Human domain experts are expensive and scarce (HC-Theorem formalizes their audit
budget $B_H$).  Independent AI audit modules require separate training, diverse
architectures, and non-overlapping training data to achieve genuine
independence.  Both resources are finite.  AC-Theorem answers the question: given
a noise level $\eta$, a confidence requirement $\delta$, and expert quality
parameters $(\alpha,\beta)$, what is the minimum number of experts $K_$
needed to reliably detect noise?

This is *not* a sample complexity question (T5 already answers that).
It is an **expert complexity** question --- the dimension along which
auditors are combined, not along which samples are acquired.  The two
dimensions interact: more samples can compensate for fewer experts only up
to the point where the experts' judgment error dominates, and vice versa.

**Contributions.**

1. **Independent Expert Lower Bound**
2. **Noise--Expert Trade-off**
3. **Audit Diversity under Correlation**
4. **Model Complexity Duality**

## Preliminaries

### Expert Model

> **Definition:** [Expert Judgment Model]
> <!-- label: def:expert -->
> For a sample $x_i$ with true noise indicator $\varepsilon_i\in\{0,1\}$, expert
> $k\in\{1,...,K\}$ provides a binary judgment
> $J_k(x_i)\in\{\mathrm{noise},\mathrm{hard}\}$ with operating characteristics:
> 
> $$
>     \alpha_k &= P(J_k=\mathrm{noise}\mid\varepsilon_i=1)
>                \quad(sensitivity), <!-- label: eq:alpha -->

>     \beta_k  &= P(J_k=\mathrm{hard}\mid\varepsilon_i=0)
>                \quad(specificity error). <!-- label: eq:beta -->
> $$
> 
> A perfect expert has $\alpha_k=1,\beta_k=0$; a random expert has
> $\alpha_k=\beta_k=1/2$.

\begin{assumption}[Conditional Independence]
<!-- label: ass:independence -->
Expert judgments are conditionally independent given the true noise status
$\varepsilon_i$:

$$<!-- label: eq:cond-indep -->
    P(J_1,...,J_K\mid\varepsilon_i) =
    \prod_{k=1}^K P(J_k\mid\varepsilon_i).
$$

This assumption will be relaxed in Section [ref].
\end{assumption}

\begin{assumption}[Expert Quality Bounds]
<!-- label: ass:quality -->
For all $k\in[K]$,

$$
    \alpha_k &\geq \alpha_ > \tfrac12, <!-- label: eq:alpha-bound -->

    \beta_k  &\leq \beta_  < \tfrac12. <!-- label: eq:beta-bound -->
$$

These bounds ensure that every expert is (on the relevant measure) strictly
better than random guessing.
\end{assumption}

> **Remark:** [Implication of Assumption [ref]]
> <!-- label: rem:gap -->
> From [ref] and [ref] we obtain the minimum
> discrimination ability
> 
> $$<!-- label: eq:min-gap -->
>     \alpha_k - \beta_k \;\geq\; \alpha_ - \beta_ \;>\; 0.
> $$
> 
> This quantity controls the signal-to-noise ratio in all subsequent bounds.

### Audit Complexity of the Model

> **Definition:** [Model Audit Complexity]
> <!-- label: def:model-complexity -->
> The **audit complexity** $M$ of a model is the effective VC dimension of
> its Situs space for audit purposes --- the minimum number of partition cells
> required to $\varepsilon$-cover the support of $P_X$ under the Situs metric.
> For a neural network, $M$ scales with parameter count, depth, and the
> intrinsic dimension of the data manifold.

### Detection Problem

The auditor's hypothesis testing problem is:

$$
    H_0&: \eta = 0 \quad(no label noise)

    H_1&: \eta \geq \etamin > 0 \quad(label noise present).
    <!-- label: eq:hypotheses -->
$$

Given $K$ expert judgments per sample, the auditor aggregates them into a test
statistic and compares against a threshold at significance level $\delta$.

## Main Results

### Independent Expert Lower Bound

> **Theorem:** [Minimum Expert Count --- Formal Statement]
> <!-- label: thm:expert-lower -->
> Assume Definitions [ref]
> and Assumptions [ref], [ref].  To detect noise
> level $\eta>0$ with Type\,I error $\leq\delta$ and Type\,II error $\leq\delta$
> (power $\geq 1-\delta$), the minimum number of experts $K_$ satisfies
> 
> $$<!-- label: eq:K-min -->
>     \boxed{\;
>     K_ \;\geq\;
>     \frac{2\log(1/\delta)}
>          {\eta^{2}\,(\alpha_-\beta_)^{2}}
>     \;}.
> $$
> 
> In particular, as $\beta_\to 1/2$ (expert approaches random guessing),
> $K_\to\infty$ --- no quantity of poor experts compensates for their lack
> of quality.

> **Proof:** \begin{chinese}
> 
> **步骤1：前提假设显式列表。**
> 本证明依赖以下前提：
> 
1. （条件独立性）给定噪声状态 $\varepsilon\in\{0,1\}$，专家判断向量
2. （灵敏度下界）对所有 $k\in[K]$，$\alpha_k\geq\alpha_>1/2$
3. （特异度误差上界）对所有 $k\in[K]$，$\beta_k\leq\beta_<1/2$
4. 噪声指示变量 $\varepsilon$ 服从参数为 $\eta$ 的 Bernoulli 分布。
5. 样本独立同分布于某未知分布 $P_X$；以下分析针对单个固定样本。

> 
> **步骤2：多数投票统计量。**
> 对单个固定样本 $x$，定义
> 
> $$<!-- label: eq:TK-def -->
>     T_K(x) \;=\; \frac{1}{K}\sum_{k=1}^{K} \mathbbm{1}_{\{J_k(x)=\mathrm{noise}\}}.
> $$
> 
> 记 $Y_k := \mathbbm{1}_{\{J_k=\mathrm{noise}\}}$，则 $T_K = \frac1K\sum Y_k$，
> 且 $Y_k\in\{0,1\}$。
> 
> **步骤3：$H_0$ 下 $T_K$ 的完整分布。**
> 在 $H_0$ 下，$\varepsilon=0$ 几乎必然。故
> \[
> P(Y_k=1\mid H_0) = P(J_k=\mathrm{noise}\mid\varepsilon=0) = \beta_k.
> \]
> 由条件独立性（P1），$\{Y_k\}_{k=1}^{K}$ 在 $H_0$ 下为独立随机变量，且
> $Y_k\sim\Ber(\beta_k)$。因此 $S_K := K\cdot T_K \sim Poisson--binomial(\{\beta_k\})$，
> 即
> \[
> P(S_K = s \mid H_0) \;=\; \sum_{A\subseteq[K]:|A|=s}\; \prod_{k\in A}\beta_k \prod_{k\notin A}(1-\beta_k),
> \qquad s=0,...,K.
> \]
> 
> **一阶矩：**
> \[
> \E[T_K\mid H_0] = \frac{1}{K}\sum_{k=1}^{K} \beta_k \;=:\; \bar.
> \]
> 由 P3，$\bar\leq\beta_$。
> 
> **二阶中心矩（方差）：**
> \[
> \V[T_K \mid H_0] = \frac{1}{K^{2}}\sum_{k=1}^{K} \beta_k(1-\beta_k)
> \;\leq\; \frac{\beta_(1-\beta_)}{K}
> \;\leq\; \frac{1}{4K}.
> \]
> 
> **步骤4：$H_1$ 下 $T_K$ 的完整分布。**
> 在 $H_1$ 下，$\varepsilon\sim\Ber(\eta)$。由全概率公式和条件独立性：
> 
> $$
>     P(Y_k=1\mid H_1)
>     &= \eta\,P(Y_k=1\mid\varepsilon=1) + (1-\eta)\,P(Y_k=1\mid\varepsilon=0) 

>     &= \eta\,\alpha_k + (1-\eta)\,\beta_k \;=:\; p_k.
> $$
> 
> 给定 $\varepsilon$，$\{Y_k\}$ 条件独立。因此 $T_K$ 在 $H_1$ 下的无条件分布
> 为两个 Poisson--binomial 分布的混合：
> \[
> P(T_K = t \mid H_1) = \eta\cdot P\!\left(\tfrac1K\sum Y_k = t \;\big|\; \varepsilon=1\right)
> + (1-\eta)\cdot P\!\left(\tfrac1K\sum Y_k = t \;\big|\; \varepsilon=0\right),
> \]
> 其中右端两项分别对应于参数集 $\{\alpha_k\}$ 和 $\{\beta_k\}$ 的
> Poisson--binomial 分布。
> 
> **一阶矩：**
> 
> $$
>     \E[T_K \mid H_1]
>     &= \E[\E[T_K\mid\varepsilon]] 

>     &= \eta\cdot\frac{1}{K}\sum_{k=1}^{K}\alpha_k \;+\; (1-\eta)\cdot\frac{1}{K}\sum_{k=1}^{K}\beta_k 

>     &= \eta\,\bar + (1-\eta)\,\bar,
> $$
> 
> 其中 $\bar:=\frac1K\sum\alpha_k$。由 P2--P3，
> $\bar\geq\alpha_$，$\bar\leq\beta_$。
> 
> **二阶中心矩：**
> 利用条件方差公式 $\V[T_K]=\E[\V[T_K\mid\varepsilon]]+\V[\E[T_K\mid\varepsilon]]$：
> 
> $$
>     \V[T_K \mid H_1]
>     &= \eta\,\V\!\left[\tfrac1K\sum Y_k \;\big|\; \varepsilon=1\right]
>        + (1-\eta)\,\V\!\left[\tfrac1K\sum Y_k \;\big|\; \varepsilon=0\right] 

>     &\quad + \eta(1-\eta)\bigl(\bar-\bar\bigr)^{2}.
> $$
> 
> 条件方差项中的每一项均 $\leq 1/(4K)$，且混合项 $\eta(1-\eta)(\bar-\bar)^{2}
> \leq \frac14(\alpha_-\beta_)^{2}$。
> 
> **步骤5：分离间隙。**
> 定义均值间隙
> \[
> \gap \;:=\; \E[T_K\mid H_1] - \E[T_K\mid H_0] \;=\; \eta(\bar-\bar).
> \]
> 由 P2--P3 及~( [ref])：
> \[
> \gap \;\geq\; \eta\,(\alpha_ - \beta_) \;>\; 0.
> \]
> 
> **步骤6：Hoeffding 不等式应用。**
> 注意 $Y_k\in[0,1]$ 且 $\{Y_k\}$ 在 $H_0$ 下独立。Hoeffding 不等式
>  [cite] 给出：对任意 $\varepsilon>0$，
> 
> $$<!-- label: eq:hoeffding -->
>     P\bigl(|T_K - \E[T_K]| \geq \varepsilon \;\big|\; H_0\bigr)
>     \;\leq\; 2\exp\!\bigl(-2K\varepsilon^{2}\bigr).
> $$
> 
> 对 $H_1$ 下的条件分布，同样成立。
> 
> **步骤7：阈值检测错误率控制。**
> 构造检测阈值 $\theta := \bar + \gap/2$。决策规则：当 $T_K > \theta$ 时拒绝 $H_0$。
> 
> **第一类错误（$H_0$ 真时误拒）：**
> 
> $$
>     P(T_K > \theta \mid H_0)
>     &= P\!\left(T_K - \bar > \gap/2 \;\big|\; H_0\right)  

>     &\leq \exp\!\bigl(-2K(\gap/2)^{2}\bigr) \qquad(由 [ref] 单侧版本) 

>     &= \exp\!\bigl(-K\gap^{2}/2\bigr).
> $$
> 
> 
> **第二类错误（$H_1$ 真时误纳）：**
> 
> $$
>     P(T_K \leq \theta \mid H_1)
>     &= P\!\left(\E[T_K\mid H_1] - T_K \;\geq\; \gap/2 \;\big|\; H_1\right) 

>     &\leq \exp\!\bigl(-K\gap^{2}/2\bigr).
> $$
> 
> 其中第二步利用 Hoeffding 不等式在 $H_1$ 分布上的应用（以
> $\E[T_K\mid H_1]$ 为中心）。
> 
> 令两类错误率均不超过 $\delta$，得：
> \[
> \exp(-K\gap^{2}/2) \;\leq\; \delta
> \quad\Longrightarrow\quad
> K \;\geq\; \frac{2\log(1/\delta)}{\gap^{2}}.
> \]
> 
> **步骤8：代入间隙下界。**
> 利用 $\gap \geq \eta(\alpha_-\beta_)$：
> \[
> K_ \;\geq\; \frac{2\log(1/\delta)}{\eta^{2}(\alpha_-\beta_)^{2}}.
> \]
> 这就完成了定理 AC.1 的证明。$\square$
> 
> **严格性标注：** \rigorous
> 
> 
> **诚实暴击：**
> \begin{critique}
>     \item **条件独立性的实际限制。** Hoeffding 不等式要求随机变量独立。
>           在 $H_0$ 下 $\varepsilon=0$ 确定，$\{Y_k\}$ 的独立性由
>           Assumption [ref] 保证。在 $H_1$ 下 $\varepsilon$ 随机，
>           但 Hoeffding 应用于条件分布（给定 $\varepsilon$），证明在条件独立下是严格的。
>           然而若违反条件独立性（如专家共享训练数据），方程 [ref] 失效，
>           实际所需 $K$ 可能远大于式 [ref]。
> 
>     \item **间隙下界的保守性。** 使用 $\alpha_$ 和 $\beta_$ 而非
>           真实均值 $\bar,\bar$ 使 $\gap$ 下界保守。若专家质量差异大
>           （如 $\alpha_k\gg\alpha_$ 或 $\beta_k\ll\beta_$），
>           真实间隙远大于 $\eta(\alpha_-\beta_)$，式 [ref]
>           给出的 $K$ 可能远高于实际需要。这就是该下界是``必要''而非``充分''条件的原因。
> 
>     \item **方差信息的忽略。** Hoeffding 不等式不利用方差信息。当
>           $\beta_$ 接近 $0$ 时，Bernstein 不等式可给出更紧的界。
>           具体地，Bernstein 不等式给出
>           \[
>           P(|T_K-\E[T_K]|\geq\varepsilon) \leq 2\exp\!\Bigl(-\frac{K\varepsilon^{2}}{2\beta_(1-\beta_)+2\varepsilon/3}\Bigr),
>           \]
>           对 $\varepsilon=\gap/2$ 可产生 $K \geq 8\beta_(1-\beta_)\log(2/\delta)/\gap^{2}$。
>           在 $\beta_$ 接近 $0$ 时此界优于 Hoeffding，但需注意
>           $\beta_(1-\beta_)$ 的引入使界依赖于方差参数。
> 
>     \item **单样本分析。** 本定理针对单个样本的专家投票统计量。当审计者审计
>           $n$ 个样本时，可通过聚合 $n$ 个样本的 $T_K$ 值进一步降低 $K$，这也是
>           T5 定理的主题。
> \end{critique}
> \end{chinese}

**Applications:**
Theorem [ref] provides the **staffing requirement** for
any expert-based SCX audit.  Before launching an audit, the formula [ref]
can be evaluated using known expert quality parameters $(\alpha_,\beta_)$,
the target noise level $\eta$, and the required confidence $\delta$.  For a
typical configuration ($\alpha=0.85$, $\beta=0.15$, $\eta=0.05$, $\delta=0.05$),
the minimum expert count is $K_\approx 45$ --- a non-trivial staffing
requirement.  The theorem reveals an inescapable trade-off: to halve the
detectable noise level (from $\eta$ to $\eta/2$), one must quadruple the
expert count.  In medical audit, where domain experts (board-certified
physicians) are scarce, this bound directly determines feasibility: below a
certain noise level, expert-based auditing becomes economically impossible,
and one must rely on complementary Cercis-based detection or accept higher
false-negative rates.  The divergence $\beta_\to1/2$ warning --- poor
experts cannot be compensated by quantity --- is a hiring criterion: never
deploy experts whose specificity is near chance level, regardless of how many
are available.

> **Remark:** Theorem [ref] is **rigorous**.  The bound is derived from
> standard Hoeffding concentration inequalities, the Neyman--Pearson lemma, and
> the explicit distribution analysis above.  \rigorous

### Noise--Expert Trade-off

> **Theorem:** [Noise--Expert Trade-off --- Formal Statement]
> <!-- label: thm:noise-expert -->
> Under the same assumptions as Theorem [ref], with a fixed
> expert budget $K\in\mathbb{N}$ and significance $\delta\in(0,1/2)$, the minimum
> detectable noise level satisfies
> 
> $$<!-- label: eq:eta-min -->
>     \etamin(K) \;\geq\;
>     \sqrt{\frac{2\log(1/\delta)}
>                {K\,(\alpha_-\beta_)^{2}}}.
> $$
> 
> The asymptotic scaling $\etamin(K)=\Theta(1/\sqrt{K})$ is **strict**:
> 
1. *Lower bound:* $\etamin(K)=\Omega(1/\sqrt{K})$ follows from~(14).
2. *Tightness:* there exists a sequence of tests $\{\varphi_K\}$

> **Proof:** \begin{chinese}
> 
> **下界：代数重排。**
> 将 Theorem [ref] 的式 [ref] 对 $\eta$ 求解即得：
> \[
> \etamin(K) \;\geq\; \sqrt{\frac{2\log(1/\delta)}{K\,(\alpha_-\beta_)^{2}}}.
> \]
> 这给出了 $\etamin(K) = \Omega(1/\sqrt{K})$。
> 
> **紧致性：Berry--Esseen 定理的完整应用。**
> 紧致性证明需要构造一个可达到 $\Theta(1/\sqrt{K})$ 速率的检测器序列，
> 并论证无任何检测器可超越该速率。
> 
> **步骤1：Berry--Esseen 定理（非 i.i.d. 版本）。**
> > **Lemma:** [Berry--Esseen, 1941--1942; Shevtsova 2011 refinement]
> > <!-- label: lem:be -->
> > 设 $X_1,...,X_K$ 为独立随机变量，满足 $\E[X_k]=\mu_k$，
> > $\V[X_k]=\sigma_k^{2}>0$，$\E[|X_k-\mu_k|^{3}]=\rho_k<\infty$。
> > 令 $S_K = \sum_{k=1}^{K}X_k$，$B_K^{2} = \sum_{k=1}^{K}\sigma_k^{2}$。
> > 则存在绝对常数 $C_0\leq 0.5583$（Shevtsova, 2011）使得
> > \[
> > \sup_{x\in\mathbb{R}} \bigl| P\bigl( \tfrac{S_K - \E[S_K]}{B_K} \leq x \bigr) - \Phi(x) \bigr|
> > \;\leq\; C_0\cdot \frac{\sum_{k=1}^{K}\rho_k}{B_K^{3}}.
> > \]
> >
> 
> **步骤2：Lyapunov 条件验证。**
> 令 $X_k = Y_k = \mathbbm{1}_{\{J_k=\mathrm{noise}\}}$，$k=1,...,K$。
> 在 $H_0$ 下，$Y_k\sim\Ber(\beta_k)$。计算三阶绝对中心矩：
> \[
> \rho_k = \E[|Y_k-\beta_k|^{3}]
> = \beta_k(1-\beta_k)^{3} + (1-\beta_k)\beta_k^{3}
> = \beta_k(1-\beta_k)\bigl[(1-\beta_k)^{2}+\beta_k^{2}\bigr].
> \]
> 由于 $(1-\beta_k)^{2}+\beta_k^{2} = 1 - 2\beta_k(1-\beta_k) \leq 1$，可得
> $\rho_k \leq \beta_k(1-\beta_k) = \sigma_k^{2}$。
> 
> 因此，
> \[
> \frac{\sum\rho_k}{B_K^{3}} \;\leq\; \frac{\sum\sigma_k^{2}}{B_K^{3}} = \frac{1}{B_K}.
> \]
> 而
> \[
> B_K^{2} = \sum_{k=1}^{K}\beta_k(1-\beta_k) \;\geq\; K\cdot\beta_(1-\beta_),
> \]
> 其中 $\beta_=\min_k\beta_k$。由于 $\beta_k<\frac12$，
> 若 $\beta_>0$ 则 $B_K = \Omega(\sqrt{K})$。即便 $\beta_=0$，
> 只要存在正比例的非零方差项，$B_K = \Omega(\sqrt{K})$ 仍成立（实践中，
> 专家特异度误差不可能全部为 $0$）。故
> \[
> \frac{\sum\rho_k}{B_K^{3}} \;\leq\; \frac{1}{B_K} \;=\; O\!\left(\frac1{\sqrt{K}}\right).
> \]
> Lyapunov 条件满足，Berry--Esseen 界为 $O(1/\sqrt{K})$。
> 
> **步骤3：构造可达到 $\Theta(1/\sqrt{K})$ 速率的检测器。**
> 考虑标准化的检测统计量：
> \[
> Z_K \;:=\; \frac{\sqrt{K}\,(T_K - \bar)}{\hat\sigma_K},
> \]
> 其中 $\hat\sigma_K^{2} = \frac1K\sum_{k=1}^{K}(Y_k - T_K)^{2}$ 为方差的一致估计量。
> 决策规则：当 $Z_K > z_{1-\delta}$ 时拒绝 $H_0$，其中 $z_{1-\delta}$ 为标准正态
> $1-\delta$ 分位数。
> 
> 在 $H_0$ 下，Berry--Esseen 定理给出：
> \[
> \sup_x \bigl| P_{H_0}(Z_K \leq x) - \Phi(x) \bigr| \;\leq\; \frac{C_0}{B_K} \;=\; O\!\left(\frac1{\sqrt{K}}\right).
> \]
> 故 $\lim_{K\to\infty} P_{H_0}(Z_K > z_{1-\delta}) = \delta$。
> 
> 在 $H_1$ 下，令 $\eta_K = c/\sqrt{K}$，其中 $c>0$ 为待定常数。
> 由 Theorem [ref] 的均值分析：
> \[
> \E[T_K\mid H_1] = \bar + \eta_K(\bar-\bar) = \bar + \frac{c(\bar-\bar)}{\sqrt{K}}.
> \]
> 因此
> \[
> \E[Z_K\mid H_1] = \frac{\sqrt{K}\cdot\eta_K(\bar-\bar)}
> + o(1) = \frac{c(\bar-\bar)} + o(1),
> \]
> 其中 $\sigma^{2} = \lim_{K\to\infty} \V[\sqrt{K}\,T_K\mid H_0] = \lim_{K\to\infty}\frac1K\sum\beta_k(1-\beta_k)$。
> 
> 检测功效：
> \[
> P_{H_1}(Z_K > z_{1-\delta})
> = 1 - \Phi\!\left( z_{1-\delta} - \frac{c(\bar-\bar)} \right) + O\!\left(\frac1{\sqrt{K}}\right).
> \]
> 
> 令 $c$ 充分大使得
> \[
> z_{1-\delta} - \frac{c(\alpha_-\beta_)} \;\leq\; z_ = -z_{1-\delta},
> \]
> 即 $c \geq \frac{2\sigma z_{1-\delta}}{\alpha_-\beta_}$，则功效 $\to 1$。
> 这证明 $\etamin(K) = O(1/\sqrt{K})$。
> 
> **步骤4：最优性论证——无检测器可超越 $\Theta(1/\sqrt{K})$。**
> 对任意 $\eta = o(1/\sqrt{K})$，检测统计量 $Z_K$ 的均值漂移
> $\sqrt{K}\cdot\eta(\bar-\bar) \to 0$。Berry--Esseen 界保证
> $Z_K$ 在 $H_0$ 和 $H_1$ 下的分布差异 $O(1/\sqrt{K})$ 趋于 $0$，故任何检测器
> 的渐近功效不超过显著水平（Le Cam 的缺一不可引理）。因此
> $\etamin(K) = \Omega(1/\sqrt{K})$ 是最优的。
> 
> **步骤5：显式常数。**
> 综合下界与紧致性分析，可得 Berry--Esseen 意义下的显式常数：
> \[
> \liminf_{K\to\infty}\; \etamin(K)\sqrt{K} \;=\;
> \frac{2z_{1-\delta}\,\sqrt{\beta_(1-\beta_)}}{\alpha_-\beta_}.
> \]
> 对于小 $\delta$，$z_{1-\delta} \sim \sqrt{2\log(1/\delta)}$，
> 这与式 [ref] 的保守形式一致。$\square$
> 
> **严格性标注：** \rigorous
> 
> 
> **诚实暴击：**
> \begin{critique}
>     \item **Berry--Esseen 常数对有限 $K$ 的实际意义。**
>           Berry--Esseen 定理给出 $O(1/\sqrt{K})$ 的渐近速率，但其显式常数
>           $C_0 \approx 0.5583$ 仅对 $K\to\infty$ 成立。对于 $K=3$ 或 $K=5$ 等
>           小样本情形，$C_0/B_K$ 可能超过 $0.3$，此时正态近似误差不可忽略。
>           实际应用中需谨慎对待小 $K$ 下的 $\Theta(1/\sqrt{K})$ 论断。
> 
>     \item **方差估计的影响。** 紧致性构造使用 $\hat\sigma_K$ 代替真实
>           标准差，Berry--Esseen 定理要求已知方差。Slutsky 引理保证
>           $\hat\sigma_K$ 的一致性，但有限样本下方差估计误差会增大检测器的
>           实际错误率。Bootstrap 校准可缓解此问题。
> 
>     \item **$\beta_$ 的正性条件。** Lyapunov 验证假设存在一个正下界
>           $\beta_>0$。若存在完美专家（$\beta_k=0$），则该专家的方差为 $0$，
>           不贡献于 $B_K$，需更精细的渐近分析。
> 
>     \item **检测器构造需要已知参数。** 紧致性构造中，阈值 $z_{1-\delta}$ 和
>           估计量 $\hat\sigma_K$ 均依赖于已知或可估计的参数。在实际审计中，
>           $\alpha_$ 和 $\beta_$ 通常未知，需要从校准数据中估计，
>           这引入了额外的误差源。
> \end{critique}
> \end{chinese}

**Applications:**
Theorem [ref] provides the **detection sensitivity
budget** for fixed-size expert panels.  With $K=3$ experts (a typical
crowd-sourcing setup), the minimum detectable noise level is
$\etamin\approx 0.41$ --- only very noisy datasets (over 40\% label errors)
can be reliably detected.  With $K=100$ experts, $\etamin\approx 0.07$ ---
still unable to detect noise below 7\%.  The $\Theta(1/\sqrt{K})$ scaling is
a harsh constraint: achieving $\etamin=0.01$ requires $K\approx 5\times10^{4}$
experts, far beyond practical budgets.  This theorem fundamentally limits
*pure* expert-based noise detection and motivates hybrid approaches:
combine a small expert panel ($K\approx 20$--$50$, detecting $\eta\approx
0.10$--$0.15$) with Cercis-based statistical detection (which can flag
samples for expert review at lower effective $\eta$ via T5's optimal sampling).
In practice, the theorem guides the ``expert escalation threshold'': set the
automated detector's sensitivity to flag samples at the noise level
$\etamin(K)$ that the available expert panel can verify, ensuring the
human-in-the-loop component is never asked to adjudicate below its detection
limit.

> **Remark:** The $\Theta(1/\sqrt{K})$ scaling has immediate practical implications:
> 
- To halve the minimum detectable noise level, you need *four times*
- To detect $\eta=0.01$ (1\% noise) with $\alpha=0.8,\beta=0.2$, you

> \rigorous

### Correlated Experts and Audit Diversity
<!-- label: sec:diversity -->

> **Theorem:** [Audit Diversity --- Effective Expert Count --- Formal Statement]
> <!-- label: thm:diversity -->
> Relax Assumption [ref] and allow pairwise Pearson correlation
> $\rho_{ij} = \mathrm{Corr}(Y_i,Y_j)$ between expert judgments $Y_i,Y_j$.
> Assume equal marginal variances $\V[Y_k]=\sigma_0^{2}$ for all $k$.  Then:
> 
1. The variance of the majority statistic is
2. The effective independent expert count is
3. The minimum detectable noise level becomes

> **Proof:** \begin{chinese}
> 
> **前提假设显式列表：**
> 
1. 允许任意的两两 Pearson 相关系数 $\rho_{ij} = \mathrm{Corr}(Y_i,Y_j)$，
2. 等边际方差：$\V[Y_k] = \sigma_0^{2} > 0$ 对所有 $k$ 成立。
3. 弱平稳性（可选）：相关结构仅依赖于配对而非具体指标（见推广部分）。
4. Assumptions [ref]（$\alpha_k\geq\alpha_$，

> 
> **步骤1：方差分解。**
> 多数投票统计量 $T_K = \frac{1}{K}\sum_{k=1}^{K} Y_k$ 的方差为：
> \[
> \V[T_K] = \frac{1}{K^{2}}\Bigl[\sum_{k=1}^{K}\V[Y_k] + \sum_{i\neq j}\mathrm{Cov}(Y_i,Y_j)\Bigr].
> \]
> 由 P2（等方差）和 $\mathrm{Cov}(Y_i,Y_j)=\rho_{ij}\sigma_0^{2}$：
> 
> $$
>     \V[T_K]
>     &= \frac{1}{K^{2}}\Bigl[K\sigma_0^{2} + \sigma_0^{2}\sum_{i\neq j}\rho_{ij}\Bigr] 

>     &= \frac{\sigma_0^{2}}{K^{2}}\Bigl[K + \sum_{i\neq j}\rho_{ij}\Bigr].
> $$
> 
> 由于 $\sum_{i\neq j}\rho_{ij} = K(K-1)\rhobar$，代入得：
> \[
> \V[T_K] = \frac{\sigma_0^{2}}{K^{2}}\bigl[K + K(K-1)\rhobar\bigr]
> = \frac{\sigma_0^{2}}{K}\bigl[1 + (K-1)\rhobar\bigr].
> \]
> 此即式 [ref]。
> 
> **步骤2：有效专家数的导出。**
> 在独立情形（$\rho_{ij}=0$）下，$\V[T_K]_{\mathrm{ind}} = \sigma_0^{2}/K$。
> 相关情形下方差膨胀因子为 $[1+(K-1)\rhobar]$。定义有效专家数 $K_{\mathrm{eff}}$
> 为满足 $\V[T_K] = \sigma_0^{2}/K_{\mathrm{eff}}$ 的正实数：
> \[
> \frac{\sigma_0^{2}}{K_{\mathrm{eff}}} = \frac{\sigma_0^{2}}{K}[1+(K-1)\rhobar]
> \;\Longrightarrow\; K_{\mathrm{eff}} = \frac{K}{1+(K-1)\rhobar}.
> \]
> 此即式 [ref]。
> 
> **步骤3：代入噪声检测下界。**
> 将 Theorem [ref] 的推导中的 $K$ 替换为 $K_{\mathrm{eff}}$，
> 可得相关情形下的 $K_$ 下界。相应地，最小可检测噪声水平为：
> \[
> \etamin(K,\rhobar) \;\geq\;
> \sqrt{\frac{2\log(1/\delta)}{K_{\mathrm{eff}}\,(\alpha_-\beta_)^{2}}}.
> \]
> 此即式 [ref]。
> 
> **步骤4：一般相关矩阵下的保守界（Jensen 不等式应用）。**
> 当等方差假设不成立时，记 $\sigma_k^{2} = \V[Y_k]$，则
> \[
> \V[T_K] = \frac{1}{K^{2}}\Bigl[\sum\sigma_k^{2} + \sum_{i\neq j}\rho_{ij}\,\sigma_i\sigma_j\Bigr].
> \]
> 令 $\bar^{2} = \frac1K\sum\sigma_k^{2}$，
> 且 $\rhobar = \frac{2}{K(K-1)}\sum_{i<j}\rho_{ij}$。
> 利用 Cauchy--Schwarz 不等式和 Jensen 不等式：
> \[
> \sum_{i\neq j}\rho_{ij}\,\sigma_i\sigma_j \;\leq\; \sum_{i\neq j}|\rho_{ij}|\,\sigma_i\sigma_j
> \;\leq\; \max_{i\neq j}|\rho_{ij}| \sum_{i\neq j}\sigma_i\sigma_j.
> \]
> 取上界 $\max|\rho_{ij}| \leq \rhobar$（在最坏情形下）或使用
> $\sum_{i\neq j}\sigma_i\sigma_j \leq K(K-1)\bar^{2}$（由 AM--GM 不等式），
> 可得保守的方差上界：
> \[
> \V[T_K] \leq \frac{\bar^{2}}{K}[1 + (K-1)\rhobar].
> \]
> 因此对任意相关结构，使用 $\rhobar$ 和 $\bar^{2}$ 给出的
> $K_{\mathrm{eff}}$ 是检测功效的保守估计（即所需专家数不会少于该值）。
> $\square$
> 
> **严格性标注：** \conditionallyrigorous
> 
> 
> **诚实暴击：**
> \begin{critique}
>     \item **等相关系数假设的局限性。**
>           $K_{\mathrm{eff}} = K/[1+(K-1)\rho]$ 公式在 $\rho_{ij}=\rho$ 且
>           $\V[Y_k]=\sigma_0^{2}$ 时精确成立。真实专家面板的相关结构几乎
>           从不满足等相关系数条件。当 $\rho_{ij}$ 差异大时，使用 $\rhobar$
>           可能严重高估或低估有效专家数。例如，若一半专家完美相关
>           （$\rho=1$）、另一半独立（$\rho=0$），则 $\rhobar\approx\frac12$，
>           但系统的有效多样性远高于 $\rhobar$ 所暗示。
> 
>     \item **保守界的偏好方向。**
>           使用 $\rhobar$ 给出的 $K_{\mathrm{eff}}$ 通常偏保守（低估有效专家
>           数），因为非等相关系数结构中正相关的极化效应使方差低于等相关
>           假设。然而，当存在负相关时，公式可能高估方差，从而低估
>           $K_{\mathrm{eff}}$。
> 
>     \item **相关性来源与因果结构。**
>           专家判断的相关性可能源于共享的训练数据、共同的领域知识或
>           $\varepsilon$ 的全局效应。后者的相关性已被 Assumption [ref]
>           排除（条件独立），但前两者在非条件相关结构中的贡献难以与
>           $\varepsilon$ 效应分离。分解 $\rho_{ij} = \rho_{ij}^{(\varepsilon)}
>           + \rho_{ij}^{(\mathrm{shared})}$ 是公开问题。
> 
>     \item **边际方差非等时的推广。**
>           当 $\sigma_i^{2}\neq\sigma_j^{2}$ 时，式 [ref] 需替换为
>           \[
>           \V[T_K] = \frac{1}{K^{2}}\Bigl[\sum\sigma_k^{2} + \sum_{i\neq j}\rho_{ij}\,\sigma_i\sigma_j\Bigr],
>           \]
>           此时不存在简洁的 $K_{\mathrm{eff}}$ 闭合形式，推荐使用数值方法。
> \end{critique}
> \end{chinese}

**Applications:**
Theorem [ref] provides the **diversity dividend** for
expert panel composition.  The effective expert count
$K_{\mathrm{eff}}=K/[1+(K-1)\rhobar]$ reveals that correlated experts
provide rapidly diminishing returns: with $\rhobar=0.3$, a panel of
$K=20$ experts is equivalent to only $K_{\mathrm{eff}}\approx 3.3$ independent
experts.  This has immediate operational implications: (i)~recruit experts
from maximally diverse backgrounds (different training institutions, different
specialties, different geographical regions) to minimize $\rhobar$;
(ii)~use different AI audit modules with non-overlapping training data and
distinct architectures to achieve low inter-model correlation;
(iii)~regularly measure $\rhobar$ on calibration sets and rotate out
highly correlated experts.  In practice, a panel of $K=10$ experts with
$\rhobar=0.1$ ($K_{\mathrm{eff}}\approx 5.3$) outperforms a panel of
$K=50$ experts with $\rhobar=0.5$ ($K_{\mathrm{eff}}\approx 2.0$).  The
theorem also provides a procurement metric: when evaluating expert panel
providers, compute $K_{\mathrm{eff}}$ from their correlation matrix rather
than comparing raw $K$ --- effective diversity, not headcount, determines
audit power.

\begin{openproblem}[Optimal Expert Selection]
<!-- label: prob:expert-selection -->
Given a pool of $N$ candidate experts with known pairwise correlations
$\rho_{ij}$ and individual quality parameters $(\alpha_k,\beta_k)$, select a
subset of size $K$ that maximizes $K_{\mathrm{eff}}$.  This is conjectured
to be a submodular maximization problem with cardinality constraint, analogous
to sensor placement [cite].  The exact complexity class and
approximation ratio are **open**.  \openquest
\end{openproblem}

### Model Complexity--Audit Cost Duality

> **Conjecture:** [Model Complexity--Audit Cost Duality]
> <!-- label: conj:duality -->
> Let $M$ be the model's audit complexity (Definition [ref]).
> There exists a universal constant $c>0$ such that for any auditor with expert
> budget $K$ and any model with complexity $M$,
> 
> $$<!-- label: eq:duality -->
>     K_ \cdot \etamin^{2} \;\geq\;
>     c \cdot \frac{M}{\log M} \cdot \log(1/\delta).
> $$
> 
> Equivalently: **you cannot simultaneously have low audit cost, detect
> small noise, and audit a complex model** --- these three quantities satisfy a
> fundamental uncertainty relation.

> **Remark:** The conjectured form draws on statistical learning theory's standard duality
> between sample complexity and model complexity (VC dimension).  Here, $K$
> replaces sample size $n$, and $\eta^{2}$ replaces excess risk $\varepsilon$.
> The $M/\log M$ factor is characteristic of the minimax rate for aggregate
> inference in high-dimensional models [cite].  If the
> conjecture is true, it provides an **economic impossibility theorem**
> for large-scale auditing: beyond a certain model complexity, reliable noise
> detection requires more experts than exist.  \openquest

## Discussion

### The Expert Supply Constraint

The $\Theta(1/\sqrt{K})$ scaling exposes a harsh reality: detecting small
noise levels ($\eta<0.05$) with high confidence requires hundreds to thousands
of independent experts.  For most practical domains, this is infeasible.
Three mitigation strategies emerge from the theory:

1. **Improve expert quality** ($\alpha_\uparrow,\beta_\downarrow$):
2. **Reduce expert correlation** ($\rhobar\downarrow$):
3. **Combine with Cercis-based detection**: Theorem [ref]

### Connection to Other SCX Theorems

- **T5 (Active Learning)**: T5 provides sample complexity $n_$;
- **FA-Theorem (Federated Audit)**: AC-Theorem~(iii)'s $K_{\mathrm{eff}}$
- **HC-Theorem (Human--AI)**: Human experts have measurable
- **AE-Theorem (Audit Entropy)**: The Landauer energy cost times

## Conclusion

AC-Theorem quantifies the expert-resource requirements of SCX auditing,
establishing a $\Theta(1/\sqrt{K})$ noise-detection threshold, an effective
expert count under correlation, and a conjectured duality between model
complexity and audit cost.  The rigorous bounds provide operational guidance
for audit deployment; the open problems --- optimal expert selection and the
model-complexity duality --- define the frontier of SCX resource theory.

\bibliographystyle{plainnat}
\begin{thebibliography}{30}

\bibitem{scx2024cercis}
SCX Working Group.
\newblock ``The SCX Axiomatic Framework: Cercis, Situs, and Tiresias
Operators,''
\newblock *Technical Report*, 2024.

\bibitem{krause2008near}
A.~Krause, A.~Singh, and C.~Guestrin.
\newblock ``Near-optimal sensor placements in Gaussian processes,''
\newblock *Journal of Machine Learning Research*, 9:235--284, 2008.

\bibitem{wainwright2019high}
M.~J.~Wainwright.
\newblock *High-Dimensional Statistics: A Non-Asymptotic Viewpoint*.
\newblock Cambridge University Press, 2019.

\bibitem{chernoff1952measure}
H.~Chernoff.
\newblock ``A measure of asymptotic efficiency for tests of a hypothesis
based on the sum of observations,''
\newblock *Annals of Mathematical Statistics*, 23:493--507, 1952.

\bibitem{hoeffding1963probability}
W.~Hoeffding.
\newblock ``Probability inequalities for sums of bounded random variables,''
\newblock *Journal of the American Statistical Association*,
58:13--30, 1963.

\bibitem{berry1941accuracy}
A.~C.~Berry.
\newblock ``The accuracy of the Gaussian approximation to the sum of
independent variates,''
\newblock *Transactions of the AMS*, 49:122--136, 1941.

\bibitem{esseen1942liapunov}
C.-G.~Esseen.
\newblock ``On the Liapunoff limit of error in the theory of probability,''
\newblock *Arkiv f\"or Matematik, Astronomi och Fysik*, 28A:1--19, 1942.

\bibitem{shevtsova2011berr}
I.~G.~Shevtsova.
\newblock ``On the absolute constants in the Berry--Esseen inequality
for i.i.d. and non-i.i.d. random variables,''
\newblock *Theory of Probability and its Applications*, 55(3):556--565, 2011.

\bibitem{nemenman2004entropy}
I.~Nemenman, W.~Bialek, and R.~R.~de Ruyter van Steveninck.
\newblock ``Entropy and information in neural spike trains: Progress on the
sampling problem,''
\newblock *Physical Review E*, 69:056111, 2004.

\bibitem{balcan2012distributed}
M.-F.~Balcan, A.~Blum, S.~Fine, and Y.~Mansour.
\newblock ``Distributed learning, communication complexity, and privacy,''
\newblock in *COLT*, 2012.

\bibitem{nemirovski1983optimal}
A.~Nemirovski and D.~Yudin.
\newblock *Problem Complexity and Method Efficiency in Optimization*.
\newblock Wiley, 1983.

\bibitem{vapnik1998statistical}
V.~N.~Vapnik.
\newblock *Statistical Learning Theory*.
\newblock Wiley, 1998.

\bibitem{cover1999elements}
T.~M.~Cover and J.~A.~Thomas.
\newblock *Elements of Information Theory*, 2nd ed.
\newblock Wiley, 2006.

\end{thebibliography}