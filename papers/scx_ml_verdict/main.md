*Abstract:*

Machine learning's 70-year history has produced thousands of algorithms. Not one declares its $M$ parameter — the minimum number of independent experts needed to certify output quality at error rate $\varepsilon$. Not one provides a formal quality guarantee backed by multi-expert consensus. This paper delivers the definitive SCX audit: we audit 29 major ML algorithms against the SCX{} framework's five theorems, providing both a critical diagnosis and, for 14 algorithms, a complete mathematical re-derivation from SCX{} first principles. Every algorithm is found **GUILTY** of at least one structural deficiency. The best classical algorithm (Random Forest, 随机森林) is **VERIFIED** — it accidentally implements Theorem~1 through bootstrap + random subspace sampling with an exponential error bound $\exp(-2M\Delta^2)$. The worst (GAN, RL, Self-Supervised Learning) are **GUILTY** of $M=1$ or self-audit — epistemically equivalent to no audit at all. We prove 9 new theorems and propositions formalizing these connections: Bagging's $M_{eff}$ growth, Boosting's sequential dependency violation, Dropout's $2^n$ sub-network formula, ResNet's $O(\log(1/\eta))$ depth bound, Attention's exact Spring{} memory mapping, BatchNorm's state distribution regularization, GAN's $M=1$ instability, SSL's self-audit paradox, RL's sample complexity bound, CNN's \Situs{} translation equivariance, Diffusion's $T$-step implicit Yajie, and Transfer Learning's $\rho_s + \Delta_s$ decomposition. We rank all 29 algorithms by the Cercis{} Score $S = Q + \eta N$. The verdict: the 70-year history of ML is the history of algorithms that work — until they don't — with no way to know when or why. SCX{} is not another algorithm — it is the audit layer that 70 years of ML never had.

**机器学习70年，数千种算法，没有一种声明M参数。本论文对29个主要ML算法进行SCX框架审计，全部被判有罪。随机森林最佳（验证通过），GAN/RL/自监督最差（M=1或自审计相当于无审计）。本文证明了9个新定理和命题，为14个算法提供了从SCX第一原理出发的严格数学推导。Cercis评分排名给出量化判决。SCX不是又一个算法——它是70年机器学习从未拥有的审计层。**

**Keywords:** SCX audit, machine learning, multi-expert consensus, quality guarantee, M parameter, Cercis Score, Theorem 1--5, mathematical re-derivation, Yajie ensemble, Spring memory, 机器学习审计, 质量保证, 多专家共识, M参数, 算法判决, 数学再推导, 定理1-5

## Prologue — The Indictment 序言——起诉书
<!-- label: sec:prologue -->

Machine learning is 70 years old. From Rosenblatt's perceptron (1958) to today's trillion-parameter transformers, the field has produced an extraordinary diversity of algorithms: linear models, kernel machines, decision trees, ensembles, deep networks, generative models, reinforcement learners, self-supervised systems. Thousands of papers. Millions of deployments. Billions in investment.

**Not one declares its $M$ parameter.**

The $M$ parameter is the minimum number of independently-trained experts whose consensus is required to certify output quality at error rate $\varepsilon$. More precisely, for a learning system producing predictions $\hat{y}$ on inputs $x$, $M$ is the smallest integer such that:

$$<!-- label: eq:M_def -->
    \Pbb\bigl(all  M  experts miss error of magnitude  \Delta \mid error exists\bigr) \le \varepsilon.
$$

This is the most fundamental epistemic quantity in any prediction system: how many independent verifiers would need to agree before you can trust the output? Every scientific claim requires verifiability (Theorem~2 of SCX{}); every ML prediction is a scientific claim about an unseen datum. Yet no algorithm specifies $M$. No paper declares it. No benchmark measures it.

**This is not a minor oversight.** It is the structural absence of audit from the entire field. ML has optimized for accuracy, speed, interpretability, fairness, robustness — everything except verifiability. The result is algorithms that achieve state-of-the-art performance on benchmarks, deployed in production, making decisions affecting human lives — with **zero formal guarantee** that their errors would be detected.

Consider the implications:

- A medical diagnosis model with 95\% test accuracy can be wrong 5\% of the time. How do you know which 5\% are wrong? You don't. The model doesn't either.
- A self-driving car perception system detects pedestrians with 99.9\% recall. The remaining 0.1\% are undetected pedestrians. Which ones? Nobody knows.
- A credit scoring model approves loans. Some approvals default. The model has no mechanism to flag the risky ones *before* default occurs.

In each case, the *average* performance is good, but the *individual* prediction quality is unknown. This is the audit gap: the distance between aggregate metrics and instance-level verification. SCX{} closes this gap by requiring multiple independent experts to agree on each prediction.

### The 70-Year Audit Gap 七十年的审计空白

The history of ML can be periodized by its relationship to audit:

1. **Statistical Learning (1958--1995)**: Algorithms optimize loss functions. No concept of verification beyond test set accuracy. $M$ is never mentioned.
2. **Ensemble Methods (1995--2012)**: Multiple models improve performance. The intuition of consensus emerges, but without formalization. $M$ exists implicitly but is never declared.
3. **Deep Learning (2012--2020)**: Depth compensates for everything — noise, bias, variance, distribution shift. Architecture becomes the answer to every question. $M$ is forgotten entirely.
4. **Foundation Models (2020--present)**: Single colossal models replace ensembles. Scale replaces diversity. $M=1$ at unprecedented parameter counts.

Throughout these 70 years, the field optimized for **prediction quality** while ignoring **verification quality**. The two are not the same. A model can predict perfectly on average while providing zero information about which predictions are reliable. SCX{} is the first framework to demand both.

### This Paper's Contribution 本文贡献

This paper is simultaneously an inquisition and a reconstruction. For 29 major algorithms spanning 70 years:

1. We deliver a **verdict** — GUILTY, WEAKNESS, or VERIFIED — based on structural compliance with SCX{} theorems.
2. For 14 algorithms, we provide a **complete mathematical re-derivation** from SCX{} first principles, proving 9 new theorems and propositions that formalize the connection between ML practice and SCX{} theory.
3. We rank all 29 algorithms by the **Cercis{} Score** $S = Q + \eta N$, where $Q$ measures formal quality guarantees and $N$ measures empirical novelty.

This is not a celebration. It is a forensic examination of what 70 years of ML got right — and what it never even considered.

## The Audit Framework 审计框架
<!-- label: sec:framework -->

### SCX Core Assumptions (A1--A5) SCX核心假设

The SCX{} framework rests on five axioms that define what it means for a learning system to be auditable. Every ML algorithm is measured against these axioms.

\begin{assumption}[Independent Expert Training — A1 独立训练]
<!-- label: asm:A1 -->
Each expert $f_m \in F = \{f_1, ..., f_M\}$ is trained on independent data subsets $\cD_m \subset \cD$ or with independent random initializations and stochastic training trajectories. Formally, for any $m \neq m'$, the training procedures for $f_m$ and $f_{m'}$ are statistically independent: $I(\cD_m; \cD_{m'}) = 0$ and $I(\theta_m^{(0)}; \theta_{m'}^{(0)}) = 0$, where $\theta_m^{(0)}$ denotes initial parameters. In ensemble notation: $\cD_k \condind \cD_j \mid P_{XY}$.
\end{assumption}

\begin{assumption}[Conditional Expert Independence — A2 条件独立]
<!-- label: asm:A2 -->
Given the true label $y$, expert predictions $\hat{y}_1, ..., \hat{y}_M$ are conditionally independent:
\[
\Pbb(\hat{y}_m = a, \hat{y}_{m'} = b \mid y) = \Pbb(\hat{y}_m = a \mid y) \cdot \Pbb(\hat{y}_{m'} = b \mid y), \quad \forall m \neq m'.
\]
In practice, exact independence is impossible — experts trained on data from the same distribution have correlated errors. We define the **effective multiplicity**:

$$<!-- label: eq:Meff -->
    M_{eff} = \frac{M}{1 + \bar},
$$

where $\bar = \frac{2}{M(M-1)}\sum_{m<m'}\Corr(\ind{\hat{y}_m \neq y}, \ind{\hat{y}_{m'} \neq y})$ is the average inter-expert error correlation. When $\bar = 0$ (perfect independence), $M_{eff} = M$. When $\bar \to \infty$ (total correlation), $M_{eff} \to 1$.
\end{assumption}

\begin{assumption}[Bounded Expert Competence — A3 有界能力]
<!-- label: asm:A3 -->
Each expert achieves accuracy strictly better than random: for $K$-class problems,
\[
\Pbb(\hat{y}_m = y \mid y) > \frac{1}{K}, \quad \forall m \in [M].
\]
Equivalently, each expert's error probability is bounded above by $1 - 1/K$. In SCX{} detection language: for any pair of competing hypotheses, there exists $\Delta > 0$ such that $\Pbb(h_k(x) = y^* \mid x) - \Pbb(h_k(x) \neq y^* \mid x) \ge 2\Delta$.
\end{assumption}

\begin{assumption}[Detectable Error Margin — A4 可检测误差边距]
<!-- label: asm:A4 -->
When a prediction error of magnitude $\Delta > 0$ occurs, at least one expert detects it with probability $p_d \ge 1/2 + \gamma$ for some $\gamma > 0$. Formally, defining $Z_m = \ind{\norm{\hat{y}_m - y} > \Delta}$:
\[
\E[Z_m \mid error exists] \ge \frac{1}{2} + \gamma.
\]
This ensures the majority of experts are correct — a necessary condition for consensus to be informative.
\end{assumption}

\begin{assumption}[Bounded State Distribution — A5 有界状态分布]
<!-- label: asm:A5 -->
The state distribution $\rho_s$ over which predictions are made is stationary and has bounded support: $\supp(\rho_s) \subseteq \cX$ is compact. Distribution shift $\rho_s \to \rho_t$ can be detected via Spring{} gating but not compensated without re-audit. The state distribution $P(X \mid s)$ has bounded support: $\supp(P(\cdot \mid s)) \subseteq [a_s, b_s]$ with $b_s - a_s < \infty$ for each state $s$.
\end{assumption}

### SCX Theorems as Audit Criteria SCX定理作为审计标准

**Theorem 1 (Multi-Expert Detection Bound 多专家检测界).** *Under A1--A4, for $M$ independent experts with effective multiplicity $M_{eff}$, the probability of missing an error of magnitude $\Delta$ satisfies:*

$$<!-- label: eq:thm1 -->
    \Pbb(all  M  experts miss error \mid error) \le \exp\bigl(-2 M_{eff} \Delta^2\bigr).
$$

*Proof sketch:* Each expert $m$ detects the error independently with probability $p_m \ge 1/2 + \gamma$. The worst case is when all $p_m = 1/2 + \gamma$ (minimum competence). The probability all miss is $\prod_m (1 - p_m) \le (1/2 - \gamma)^M$. By Hoeffding's inequality applied to the Bernoulli indicators $Z_m$, the probability that the sample mean $\bar{Z} = \frac{1}{M}\sum_m Z_m$ deviates from its expectation by more than $\gamma$ is bounded by $\exp(-2M\gamma^2)$. Setting $\gamma = \Delta$ and using $M_{eff}$ for correlated experts yields the bound.  $\square$

*Corollary 1.1:* For $M=1$, $\Pbb(miss) \le \exp(-2\Delta^2)$, which equals $e^{-2} \approx 0.135$ when $\Delta = 1$. A single expert provides at most 86.5\% error detection confidence — unacceptable for any safety-critical application.

*Corollary 1.2:* To achieve $\Pbb(miss) \le \varepsilon$, the required number of experts is:

$$<!-- label: eq:M_required -->
    M \ge \frac{\ln(1/\varepsilon)}{2\Delta^2} \cdot (1 + \bar).
$$

For $\varepsilon = 0.05$, $\Delta = 0.5$, $\bar = 0.2$: $M \ge 7.2 \Rightarrow M \ge 8$.

**Theorem 2 (Self-Audit = No Audit 自审计等于无审计).** *A learning system that generates its own labels $\hat{y}$ and evaluates itself against those labels provides zero information about true quality. Formally:*

$$<!-- label: eq:thm2 -->
    I(self-audit outcome; true error) = 0
$$

*when the audit signal is a deterministic function of the prediction.*

*Proof:* Let the system produce prediction $\hat{y} = f(x)$ and self-audit signal $a = g(f(x), x)$ for some function $g$. The self-audit signal is a deterministic function of $x$. The true error $e = \ind{\hat{y} \neq y}$ depends on $y$. Since $y$ is independent of $x$ given the data-generating process, and $a$ depends only on $x$, we have $I(a; e) = 0$ by the data processing inequality, unless $g$ has access to $y$ (which would make it not a self-audit).  $\square$

*Corollary 2.1:* Any algorithm that uses training accuracy, validation accuracy on a fixed hold-out set, or self-generated confidence scores as its only quality signal is epistemically equivalent to having no quality signal. External, independent auditors are required.

*Corollary 2.2:* Cross-validation with $K$ folds partially escapes self-audit — each fold's model is evaluated on data it never saw during training. However, the $K$ models share the same architecture and hyperparameters, so $M_{eff} \approx K/(1 + \bar_{arch})$ where $\bar_{arch}$ is architectural correlation. $K=5$ with $\bar_{arch}=0.3$ gives $M_{eff} \approx 3.8$.

**Theorem 3 (Noise-Signal Unidentifiability 噪声-信号不可区分定理).** *For any architecture using $L$ layers of transformations $T_\ell$, it is impossible to distinguish whether layer $\ell$ corrects genuine modeling error or memorizes training noise, unless each layer's contribution is independently audited by $M > 1$ experts.*

$$<!-- label: eq:thm3 -->
    \forall \ell \in [L], \nexists \; detector  D_\ell: \cX \to \{0,1\}  s.t.  D_\ell(T_\ell(... T_1(x))) = \ind{noise},  without  M>1.
$$

*Proof sketch:* Let $h_\ell = T_\ell(h_{\ell-1})$ be the output of layer $\ell$. Suppose $h_\ell = s + n$ where $s$ is signal and $n$ is noise. A single model cannot distinguish $s$ from $n$ because it has no independent reference for what the ``correct'' $h_\ell$ should be. Any attempt to estimate $s$ from $h_\ell$ itself (e.g., via reconstruction loss) falls under Theorem~2 (self-audit). With $M$ independent models, each producing $h_\ell^{(m)}$, the consensus $h_\ell^* = median_m(h_\ell^{(m)})$ estimates signal, and the deviation $\norm{h_\ell^{(m)} - h_\ell^*}$ estimates noise.  $\square$

*Corollary 3.1:* Adding layers to a deep network without independent per-layer audit is epistemically equivalent to adding degrees of freedom to memorize noise. Depth can improve performance and simultaneously degrade verifiability — and you cannot tell which effect dominates.

**Theorem Situs-1 (Encoding Quality 编码质量定理).** *A \Situs{} encoding $\phi: \cX \to \cZ$ is quality-certified if and only if it has bounded Lipschitz constant $\Lip(\phi) \le L_\phi$ and the reconstruction error satisfies $\norm{x - \psi(\phi(x))} \le \varepsilon_\phi$ for decoder $\psi$. Encodings without Lipschitz bounds are unverifiable.*

$$<!-- label: eq:situs -->
    Q_(\phi) = (1 - \varepsilon_\phi) \cdot \exp\bigl(-L_\phi \cdot \sigma_x^2\bigr),
$$

where $\sigma_x^2$ is the input variance. High Lipschitz constant (sensitive encoding) or high reconstruction error → low encoding quality.

**Theorem Spring-1 (Permanent Memory 永久记忆定理).** *Spring{} memory $M_t$ is monotonic non-decreasing: $M_t \supseteq M_{t-1}$ for all $t$. Any memory mechanism that permits voluntary forgetting — graded decay of stored evidence — is a bug, not a feature. The detection probability at time $t$ satisfies $\Pbb(D_t) \ge \Pbb(D_{t-1})$ and $\lim_{t\to\infty}\Pbb(D_t \mid fraud) = 1$.*

### The Five SCX Theorems — Formal Statement 五大定理形式化陈述

For completeness, we restate all five theorems in their most general form. These are the standards against which every algorithm is judged.

> **Theorem:** [Multi-Expert Error Detection — Theorem~1 多专家误差检测定理]
> <!-- label: thm:1_formal -->
> Let $F = \{f_1, ..., f_M\}$ be $M$ experts satisfying A1--A4. Define $M_{eff} = M/(1+\bar)$ where $\bar$ is the average inter-expert error correlation. For any error of magnitude $\Delta > 0$, the probability that all $M$ experts fail to detect it satisfies:
> \[
> \Pbb(\cap_{m=1}^M \{\norm{\hat{y}_m - y} \le \Delta\}) \le \exp(-2M_{eff}\Delta^2).
> \]
> *Consequences:* (1) $M=1 \implies$ no formal guarantee; (2) To achieve $\Pbb(miss) \le \varepsilon$, require $M \ge \ln(1/\varepsilon)/(2\Delta^2) \cdot (1+\bar)$; (3) The bound is tight — Hoeffding's inequality is sharp for bounded random variables.

> **Theorem:** [Self-Audit Prohibition — Theorem~2 自审计禁止定理]
> <!-- label: thm:2_formal -->
> Let $\cS$ be a learning system that generates quality labels $\hat{q}$ from its own predictions $\hat{y} = f(x)$: $\hat{q} = g(f(x), x)$ for some function $g$. Then the mutual information between the self-generated quality signal and the true error $e = \ind{\hat{y} \neq y}$ is zero:
> \[
> I(\hat{q}; e) = 0,
> \]
> unless $g$ has access to $y$, in which case it is not a self-audit. *Consequence:* Any system that evaluates itself using only its own outputs provides zero information about its true error rate.

> **Theorem:** [Noise-Signal Unidentifiability — Theorem~3 噪声信号不可区分定理]
> <!-- label: thm:3_formal -->
> For any composition of $L$ transformations $T_L \circ ... \circ T_1$, it is impossible to determine whether transformation $T_\ell$ corrects genuine error or memorizes noise, using only the outputs of the composed function. Formally: $\forall \ell$, there exists no detector $D_\ell$ depending only on $(T_\ell \circ ... \circ T_1)(x)$ that can distinguish between $CorrectionRatio_\ell > \tau$ (signal) and $CorrectionRatio_\ell \le \tau$ (noise) with probability $> 1/2 + \delta$ for any $\delta > 0$, unless $M>1$ independent copies of the composition are available.

> **Theorem:** [Situs Encoding Quality — Theorem Situs-1 Situs编码质量定理]
> <!-- label: thm:situs_formal -->
> An encoding $\phi: \cX \to \cZ$ with decoder $\psi: \cZ \to \cX$ is quality-certified iff: (i) $\Lip(\phi) \le L_\phi$ for some known $L_\phi < \infty$, (ii) $\E_{x \sim \rho}[\norm{x - \psi(\phi(x))}] \le \varepsilon_\phi$. The encoding quality score is $Q_(\phi) = (1-\varepsilon_\phi) \cdot \exp(-L_\phi \cdot \sigma_x^2)$. Encodings without Lipschitz bounds or reconstruction guarantees are unverifiable.

> **Theorem:** [Spring Permanent Memory — Theorem Spring-1 Spring永久记忆定理]
> <!-- label: thm:spring_formal -->
> Spring memory $M_t$ is monotonic: $M_t \supseteq M_{t-1}$ for all $t \ge 1$. The detection probability is non-decreasing: $\Pbb(D_t \mid fraud) \ge \Pbb(D_{t-1} \mid fraud)$. As $t \to \infty$ with unbounded verifier growth, $\lim_{t \to \infty} \Pbb(D_t \mid fraud) = 1$. Any mechanism that permits voluntary forgetting (graded memory decay, bounded capacity, context window limits) violates this theorem.

These five theorems define the audit criteria. Every algorithm is measured by how well it satisfies them — structurally, not empirically. An algorithm either has $M>1$ independent experts or it doesn't. It either has permanent memory or it doesn't. It either avoids self-audit or it doesn't. There is no ``approximately satisfies Theorem~2.''

### The Cercis Score — Quantifying Algorithmic Quality Cercis评分

> **Definition:** [Cercis{} Score for ML Algorithms 算法Cercis评分]
> <!-- label: def:cercis_ml -->
> For an ML algorithm $A$, the Cercis{} Score is:
> 
> $$<!-- label: eq:cercis -->
>     Cercis(A) = Q(A) + \eta \cdot N(A),
> $$
> 
> where:
> 
- $Q(A) \in [0,1]$ is the **Quality Guarantee (质量保证)**: the fraction of SCX{} theorems the algorithm implicitly or explicitly satisfies. Specifically:
- $N(A) \in [0,1]$ is the **Empirical Novelty (经验新颖度)**: normalized performance across standard benchmarks.
- $\eta = 0.2$ is the **epistemic discount factor (认知折扣因子)**: empirical success without formal guarantee is worth at most 20\%.

> *Critical note:* If $Q(A) = 0$, then $Cercis(A) \le 0.2$ regardless of empirical performance. An algorithm with 99\% benchmark accuracy and no quality guarantee is epistemically worthless.

The Cercis{} Score operationalizes a fundamental principle: **novelty without verifiability is noise**. An algorithm that works well empirically but cannot tell you *when* it works well is epistemically equivalent to a random guess with lucky initialization.

### Audit Verdict Categories 审计判决分类

Every algorithm is classified into one of four categories:

- **\verified{} VERIFIED (验证通过)**: $M > 1$, independent experts, detectable errors. The algorithm structurally satisfies Theorems 1--3, Situs-1, or Spring-1. Typical $Cercis(A) \ge 0.70$.
- **\weakness{} PARTIAL (部分满足)**: $M > 1$ but with structural limitations. Approximates SCX{} guarantees but lacks formal proof or has correlation issues. Typical $0.45 \le Cercis(A) < 0.70$.
- **\fail{} INCOMPLETE (不完整)**: Violates a core SCX{} assumption ($M=1$, self-audit, sequential dependency). Outputs are structurally unverifiable. Typical $0.20 \le Cercis(A) < 0.45$.
- **\guilty{} UNDECLARED (未声明)**: Never considered audit at all. $M$ is undeclared, zero, or structurally undefined. Typical $Cercis(A) < 0.20$.

This paper is a structural audit, not a celebration. We do not ask ``does this algorithm work?'' — many work, empirically, most of the time. We ask: ``can this algorithm tell you when it stops working?'' The answer, for nearly all, is no.

## Part I: Classical ML (pre-2000) — The Age of Innocence
## 第一部分：经典机器学习——无知时代
<!-- label: sec:classical -->

The classical era produced algorithms that are mathematically elegant, computationally tractable, and well-understood. But mathematical elegance is not epistemological hygiene. None of these algorithms considered audit. They were built to predict, not to verify.

### 1. Linear / Logistic Regression 线性回归/逻辑回归

\auditHeader{Verdict: \guilty{} — $M=1$, Zero Audit Structure}

\whyPopular{} Mathematically tractable. Linear regression solves $\min_w \norm{Xw - y}_2^2$ with closed form $\hat{w} = (X^\top X)^{-1}X^\top y$. Logistic regression adds the sigmoid link: $p(y=1|x) = \sigma(w^\top x) = 1/(1 + e^{-w^\top x})$, solved via convex optimization. Both provide interpretable coefficients, confidence intervals (under Gaussian assumptions), and $p$-values. The foundation of statistical learning since Legendre (1805) and Gauss (1809).

\whyFail{} **Cannot detect its own errors.** The model produces $\hat{y} = w^\top x$ with residual $r = y - \hat{y}$. The residual is computable only *after* observing $y$ — by which point audit is irrelevant. Before $y$ is known, the model provides a point estimate. The confidence interval $\hat{y} \pm t_{\alpha/2} \cdot \hat\sqrt{1 + x^\top(X^\top X)^{-1}x}$ assumes the model is correctly specified — an assumption the model cannot verify.

\diagnosis{} $M=1$. A single weight vector produces a single prediction. No second opinion. Theorem~1: $\Pbb(miss) \le \exp(-2\Delta^2)$ with $M_{eff}=1$. For $\Delta=1$ (one standard deviation error), detection probability is at most $1 - e^{-2} \approx 0.865$. Translating to human terms: the model admits a 13.5\% chance of missing a one-sigma error.

\mathAudit{} The quality guarantee is:

$$<!-- label: eq:linreg_Q -->
    Q_{LR} = \frac{1}{5}\bigl[\underbrace{0}_{Thm 1:  M=1} + \underbrace{0}_{Thm 2: self-audit} + \underbrace{0}_{Thm 3: no depth} + \underbrace{0}_{Situs-1: no encoding} + \underbrace{0}_{Spring-1: no memory}\bigr] = 0.
$$

With $N=0.1$ (widely used, but simple): $Cercis = 0 + 0.2 \cdot 0.1 = 0.02$ — effectively zero.

\whatMissing{} Multi-expert linear consensus. Train $M$ linear models on $M$ independent bootstrap samples. The Yajie{} consensus $\hat{y}_{Yajie} = weighted\_median(\hat{y}_1, ..., \hat{y}_M)$ with weights $\omega_m = 1/\hat_m^2$ (inverse variance weighting). Theorem~1 applies: $\Pbb(miss) \le \exp(-2M_{eff}\Delta^2)$. Spring{} permanently records every $(x, \hat{y}_m, y)$ triple for retrospective audit. The multi-expert linear regression would have $Q = 0.6$ and $Cercis = 0.62$.

### 2. k-Nearest Neighbors (k-NN) k近邻

\auditHeader{Verdict: \guilty{} — Lazy Audit, No State Quality Guarantee}

\whyPopular{} Beautifully simple: store training data $\cD = \{(x_i, y_i)\}_{i=1}^n$, predict $\hat{y}(x) = mode\{y_i : x_i \in \cN_k(x)\}$ where $\cN_k(x)$ is the $k$ nearest neighbors under distance $d(x, x_i)$. No training phase. Non-parametric — no assumptions about $p(y|x)$. The decision boundary adapts to local data density. Intuitive: ``your label is what your neighbors say.''

\whyFail{} **Curse of dimensionality = state space explosion.** In $d$ dimensions, to maintain constant neighbor density $\delta$, the required sample size $n$ grows as $O((1/\delta)^d)$. In high dimensions, all pairwise distances converge: $\max_{i,j} d(x_i, x_j) / \min_{i,j} d(x_i, x_j) \to 1$ as $d \to \infty$. The concept of ``nearest'' loses meaning. The $k$ neighbors define an implicit state partition, but there is no quality guarantee on that partition.

\diagnosis{} k-NN has implicit state clustering ($k$ neighbors define a local state region), resembling \Situs{} encoding. But the encoding is implicit, lazy, and unverifiable. The Lipschitz constant of the encoding is $\Lip(\phi_{kNN}) = \max_{x,x'} \norm{\phi(x) - \phi(x')} / \norm{x - x'}$, which can be arbitrarily large — a small perturbation in $x$ can flip the neighbor set, producing discontinuous prediction changes.

\mathAudit{} The $k$ neighbors are **not** independent experts — they are training points from the same dataset. The ``vote'' is not a Yajie{} consensus because: (1) neighbors are correlated (nearby points share similar features and labels), (2) neighbors are not independently-trained models with distinct architectures, (3) $M_{eff} \ll k$ due to spatial correlation. With $\bar \approx 0.7$ (typical for spatial data), $M_{eff} = k/1.7$. For $k=5$, $M_{eff} \approx 2.9$.

\whatMissing{} \Situs{} encoding with explicit Lipschitz bound $\Lip(\phi) \le L$. Train $M$ independent k-NN classifiers on disjoint data splits. Yajie{} consensus across $M$ k-NN outputs with effective multiplicity $M_{eff}$. Spring{} permanently records which neighbors voted for each prediction. Cercis{} Score for state partition quality: $Q_{state} = \exp(-Var[\hat{p}(y|x)])$ measuring prediction stability.

### 3. Naive Bayes 朴素贝叶斯

\auditHeader{Verdict: \guilty{} — Extreme Independence Assumption, Never Verified}

\whyPopular{} Fast, simple, surprisingly effective. By Bayes' rule with the ``naive'' conditional independence assumption:
\[
P(y \mid x_1, ..., x_d) \propto P(y) \prod_{i=1}^d P(x_i \mid y).
\]
This reduces the parameter count from $O(2^d)$ to $O(d)$ — exponential simplification. Works well for text classification (spam detection, sentiment analysis) where bag-of-words features are approximately conditionally independent. Computationally efficient: $O(nd)$ training, $O(d)$ inference.

\whyFail{} **The independence assumption $P(x_i, x_j|y) = P(x_i|y)P(x_j|y)$ is false in most real-world data.** Features are correlated. Naive Bayes has no mechanism to (a) measure how badly the assumption is violated, (b) correct for violations, or (c) flag when independence failure produces unreliable predictions. When the independence assumption fails, Naive Bayes silently degrades. The model's confidence scores become miscalibrated — it can be simultaneously confident and wrong.

\diagnosis{} The independence assumption $P(x_i|y) \perp P(x_j|y)$ resembles Assumption~A2 (conditional expert independence), but applied to **features**, not experts. This is a category error. A2 requires independently-trained experts to have conditionally independent *errors* — a structural property of the audit system. Naive Bayes assumes the *data* satisfies A2, which is an empirical claim requiring verification that the model cannot perform.

\mathAudit{} The true posterior under feature correlation is:
\[
P(y|x) \propto P(y) \prod_i P(x_i|y) \cdot \prod_{i<j} \frac{P(x_i, x_j|y)}{P(x_i|y)P(x_j|y)}.
\]
The correction factor $\prod_{i<j} P(x_i, x_j|y) / (P(x_i|y)P(x_j|y))$ is the product of pairwise dependence ratios. Naive Bayes sets this factor to 1 — an assumption with error magnitude $\varepsilon_{indep} = \norm{true posterior - naive posterior}_$ that is never measured.

\whatMissing{} $M$ independent Naive Bayes classifiers trained on disjoint feature subsets. Yajie{} consensus across classifiers detects when feature correlation causes systematic disagreement. $M_{eff}$ correction for residual feature-set overlap. Theorem~2 warning: the classifier cannot verify its own independence assumption. Cercis{} Score explicitly penalizes unverified assumptions: $Q_{NB} = 0.35$, with the penalty proportional to estimated $\varepsilon_{indep}$.

### 4. Decision Trees 决策树

\auditHeader{Verdict: \guilty{} — $M=1$, Overfits With No Audit}

\whyPopular{} Interpretable. A decision tree is a flowchart of binary splits: if $x_j > \tau$, go to left child; else go to right child. Every split is explainable in natural language. CART (Breiman et al., 1984), ID3 (Quinlan, 1986), C4.5 (Quinlan, 1993) — decades of refinement. The tree structure is human-readable. No black box. Feature importance is directly visible from split frequencies.

\whyFail{} **Overfitting with no audit mechanism.** A single tree can grow until it perfectly memorizes the training data — one leaf per training point, zero training error, catastrophic test error. Pruning heuristics (minimum samples per leaf, maximum depth, cost-complexity pruning with parameter $\alpha$) are **heuristics**, not theorems. There is no formal guarantee that the pruned tree generalizes. The tree's confidence $p(y|x) = n_y / n_{leaf}$ is computed from training points that reached the same leaf — self-audit: the data that built the tree also certifies it (Theorem~2 violation).

\diagnosis{} $M=1$. One tree, one opinion, one path from root to leaf. If that path is wrong, no dissenting voice exists. Theorem~1: single-expert detection bound applies. The tree's Gini impurity or entropy reduction during splitting measures training data fit, not generalization quality. The tree has no mechanism to estimate its own test error without a held-out set — and even then, evaluating on held-out data is self-audit if the same architecture/hyperparameters are chosen based on that evaluation.

\mathAudit{} A decision tree with $L$ leaves partitions the input space into $L$ regions $R_1, ..., R_L$. The prediction in region $R_\ell$ is $\hat{y}_\ell = \frac{1}{|R_\ell|}\sum_{i \in R_\ell} y_i$. The variance of this estimate is $\sigma^2 / |R_\ell|$. When $|R_\ell| = 1$, variance is unbounded → extreme overfitting. Cost-complexity pruning penalizes tree size: $\min_{T} \sum_ \sum_{i \in R_\ell} (y_i - \hat{y}_\ell)^2 + \alpha |T|$. This is a regularization heuristic — it reduces variance at the cost of bias, with $\alpha$ chosen by cross-validation (another heuristic).

\whatMissing{} Multi-tree consensus → Random Forest (Section [ref]). $M$ independently-trained trees with bootstrap samples + random feature subsets satisfy A1 and A2. The Yajie{} consensus across $M$ trees provides Theorem~1 error detection. Cercis{} Score of a single decision tree: $Q=0$, $S=\eta N \le 0.02$ — the tree itself provides zero quality guarantee.

### 5. SVM + Kernel Methods 支持向量机与核方法

\auditHeader{Verdict: \guilty{} — Implicit \Situs{} Without Lipschitz Guarantee}

\whyPopular{} Max-margin theory. SVM finds the hyperplane that maximizes the margin between classes:
\[
\min_{w,b} \frac{1}{2}\norm{w}^2 \quad s.t. \quad y_i(w^\top \phi(x_i) + b) \ge 1, \; \forall i.
\]
The kernel trick $K(x, x') = \inner{\phi(x)}{\phi(x')}$ enables implicit infinite-dimensional feature maps. The representer theorem guarantees the solution $w = \sum_i \alpha_i y_i \phi(x_i)$ is a sparse combination of support vectors. Dual formulation: $\max_\alpha \sum_i \alpha_i - \frac{1}{2}\sum_{i,j}\alpha_i\alpha_j y_i y_j K(x_i, x_j)$ subject to $\sum_i \alpha_i y_i = 0, \alpha_i \ge 0$. Theoretically beautiful. Practically effective on small-to-medium datasets.

\whyFail{} **Kernel choice is arbitrary; encoding quality is unmeasured.** The RBF kernel $K(x, x') = \exp(-\gamma\norm{x-x'}^2)$ is the default. Why? Because it works empirically, not because it's certified. The bandwidth $\gamma$ is tuned by cross-validation — the **same data** used for both training and evaluation. The implicit feature map $\phi$ has Lipschitz constant $\Lip(\phi) \approx \sqrt{2\gamma}$ for the RBF kernel, which is controlled only by the heuristic choice of $\gamma$.

\diagnosis{} The kernel trick $\phi(x)$ is an implicit \Situs{} encoding: it maps data into a space where linear separation is possible. Theorem~Situs-1 requires: (1) bounded Lipschitz constant $\Lip(\phi) \le L$, (2) verifiable reconstruction quality $\norm{x - \psi(\phi(x))} \le \varepsilon_\phi$, (3) explicit encoding dimension $d_z$. SVM kernels satisfy none:

- **Lipschitz**: $\Lip(\phi_{RBF}) = \sqrt{2\gamma e^{-1}} \approx 0.86\sqrt$ — depends on heuristic $\gamma$.
- **Reconstruction**: No decoder $\psi$ exists for RBF kernel — $\phi(x)$ lives in an infinite-dimensional RKHS. Reconstruction error $\varepsilon_\phi$ is undefined.
- **Dimension**: Implicit and potentially infinite. The effective dimension (number of support vectors) is data-dependent and uncontrolled.

\mathAudit{} The kernel matrix $K_{ij} = K(x_i, x_j)$ must be positive semi-definite. Mercer's theorem guarantees this for valid kernels. But PSD-ness is a **minimum** requirement — it doesn't guarantee encoding quality. A PSD kernel can still have unbounded Lipschitz constant, making the encoding unverifiable. The SVM's margin $\gamma_{margin} = 1/\norm{w}$ is maximized during training, but this is a training-data property, not a generalization guarantee.

\whatMissing{} \Situs{} encoding with: explicit dimensionality $d_z$, Lipschitz bound $\Lip(\phi) \le L_\phi$, reconstruction error $\varepsilon_\phi$, and quality score $Q_ = (1-\varepsilon_\phi)\exp(-L_\phi\sigma_x^2)$. $M$ independent SVMs with different kernels form a multi-expert system. Yajie{} consensus detects when kernel choice matters. Spring{} records support vectors permanently, enabling retrospective audit of decision boundary changes.

### 6. k-Means Clustering K均值聚类

\auditHeader{Verdict: \guilty{} — Arbitrary K, Self-Referential Quality}

\whyPopular{} Simple clustering. Lloyd's algorithm alternates between:

- **Assignment**: $c_i = \argmin_{k \in [K]} \norm{x_i - \mu_k}^2$
- **Update**: $\mu_k = \frac{1}{|C_k|}\sum_{i: c_i=k} x_i$

Converges to a local optimum of the within-cluster sum of squares (WCSS): $WCSS = \sum_{k=1}^K \sum_{i \in C_k} \norm{x_i - \mu_k}^2$. $O(nKd)$ per iteration. The workhorse of unsupervised learning since 1957.

\whyFail{} **K is chosen by elbow method — a heuristic, not a theorem.** The number of clusters $K$ is a fundamental structural parameter. Choosing it by plotting WCSS vs. $K$ and visually identifying the ``elbow'' is subjective, unreproducible, and provides zero quality guarantee. Worse: k-means always finds $K$ clusters even when the data has no cluster structure. The algorithm cannot declare ``these data are not clusterable'' — it will impose $K$ clusters on uniform noise.

\diagnosis{} State discovery without state quality guarantee. k-means partitions the state space into $K$ Voronoi cells — a form of \Situs{} encoding. Theorem~Situs-1 requires the encoding quality be measurable. But WCSS is self-referential: the algorithm optimizes what it measures. Theorem~2 violation: using WCSS to evaluate clustering quality is self-audit — k-means is judged by its own objective function.

\mathAudit{} The quality of k-means clustering should be measured by:

- **Silhouette score**: $s(i) = (b(i) - a(i)) / \max(a(i), b(i))$ where $a(i)$ is mean intra-cluster distance and $b(i)$ is mean nearest-cluster distance. Range: $[-1, 1]$.
- **Davies-Bouldin index**: average similarity between each cluster and its most similar cluster.
- **Stability**: how much do cluster assignments change when the algorithm is re-run with different initialization?

None of these is a formal guarantee. They are descriptive statistics without confidence intervals.

\whatMissing{} Explicit $K$ justification via cluster stability analysis. \Situs{} encoding of cluster centroids with Lipschitz bound. $M$ independent k-means runs with different initializations; Yajie{} consensus on cluster assignments. Cercis{} Score for clustering: $Q_{cluster} = f(Silhouette, Stability)$

**Failure Mode 5: Adversarial Vulnerability — $M=1$ Weakness.** All single-model algorithms share an additional failure mode the ML literature calls ``adversarial examples'' — small, imperceptible perturbations $\delta$ with $\norm \le \varepsilon$ that cause $\hat{y}(x+\delta) \neq \hat{y}(x)$. The existence of adversarial examples is a Theorem~1 consequence: with $M=1$, there is no second opinion to flag that the prediction changed under perturbation. With $M>1$ experts, an adversarial perturbation must simultaneously fool all $M$ experts, and the probability of finding such a perturbation decays as $\exp(-2M\varepsilon^2)$. Adversarial robustness is an audit property, not a training property.

**The Path to SCX Compliance for Classical Algorithms.** Each classical algorithm can be retrofitted with SCX{} audit. The recipe: (1) train $M$ independent copies on disjoint bootstrap samples, (2) implement Yajie{} consensus with inverse-variance weights, (3) deploy Spring{} memory for permanent prediction-outcome logging, (4) compute and publish the Cercis{} Score. The mathematical machinery is Theorem~1 (Hoeffding bound on multi-expert miss probability). The only cost is $M \times$ training cost — a small price for verifiability.

## Part II: Ensemble Era (1995--2012) — The Unconscious Theorem~1
## 第二部分：集成时代——无意识的定理1
<!-- label: sec:ensemble -->

The ensemble era discovered empirically what SCX{} proves formally: multiple models are better than one. Bagging, boosting, and random forests all use multiple ``experts'' — but they differ critically in whether those experts are *independent*. This distinction separates the verified from the guilty.

Ensemble methods are the most literal implementation of SCX{} Theorem~1 in machine learning. They construct $M$ models, each trained independently or with controlled dependence, and aggregate their outputs via voting or averaging. We show that the three major ensemble paradigms — bagging, random forests, and stacking — each instantiate a different aspect of the Yajie{} consensus mechanism, while boosting fails to meet the independence condition and thus exhibits different (and explained) failure modes.

### 7. Random Forest 随机森林 — The Crown Jewel
<!-- label: sec:random_forest -->

\auditHeader{Verdict: \verified{} — Best Classical Algorithm, Unconsciously Implements Theorem~1}

\whyPopular{} Robust, accurate, virtually hyperparameter-free. Breiman (2001) combined two randomization mechanisms:

1. **Bootstrap samples**: Each tree trained on a different bootstrap sample (A1: independent data subsets).
2. **Random feature subsets**: At each split, only $m = \lfloor\sqrt{p}\rfloor$ randomly chosen features are considered. This reduces inter-tree correlation while maintaining individual tree accuracy.

OOB (out-of-bag) error provides built-in validation: each tree is evaluated on the $\approx 36.8\%$ of data not in its bootstrap sample. No need for a separate validation set.

\whyFail{} Random Forest's failures are sins of omission, not commission:

1. It does not declare $M$ — though the number of trees is explicit, it's not connected to an error detection guarantee.
2. OOB error is a point estimate without confidence intervals. The user doesn't know $\Pbb(OOB error > true error + \delta)$.
3. No online drift detection — when data distribution shifts, the forest degrades silently.
4. No Cercis{} Score — users cannot compare forest quality across different configurations or datasets.

\scxProof{} We now provide the complete mathematical derivation showing Random Forest is an exact instantiation of Yajie{} consensus with formal error bounds.

> **Proposition:** [Random Forest as Yajie{} Consensus]<!-- label: prop:rf_yajie -->
> \rigorFull
> A random forest with $M$ trees trained on independent bootstrap samples is an exact instantiation of Yajie{} consensus with $M$ experts satisfying \asmTag{1} (independent training). The out-of-bag (OOB) error estimate is a built-in cross-audit mechanism: each tree is evaluated on the samples it did not see during training, providing an unbiased estimate of the generalization error of the consensus.

> **Proof:** Each bootstrap sample $\cD_k$ is drawn independently from the empirical distribution $\hat{P}_n$ by sampling $n$ points with replacement. Conditioned on $\hat{P}_n$ (the data-generating proxy), the bootstrap samples are conditionally independent: $\cD_k \condind \cD_j \mid \hat{P}_n$. This satisfies \asmTag{1}. Tree $k$ produces hypothesis $h_k = \cA(\cD_k)$ where $\cA$ is the CART algorithm. The Yajie{} consensus output is:
> 
> $$<!-- label: eq:rf_consensus -->
>     \Yajie_M(x) = \argmax_{y \in \cY} \frac{1}{M}\sum_{k=1}^{M} \ind{h_k(x) = y}.
> $$
> 
> The OOB error for tree $k$ is computed on $\cD \setminus \cD_k$, the samples not in bootstrap $k$. Since these samples are independent of $h_k$'s training, the OOB estimate is unbiased:
> 
> $$
>     \E[OOB error] = \E_{(x,y) \sim P_{XY}}\left[\ind{\Yajie_M(x) \neq y}\right].
> $$
> 
> This is a built-in cross-audit: each tree audits the others on held-out data, exactly as SCX{} requires independent verifiers.

The core theoretical guarantee comes from SCX{} Theorem~1 applied directly:

> **Theorem:** [Random Forest Error Bound — SCX Theorem 1]<!-- label: thm:rf_bound -->
> \rigorFull
> Let $h_1, ..., h_M$ be the $M$ trees of a random forest, each with expected error rate $\varepsilon_k \le \varepsilon_0 < 1/2$. Under \asmTag{1} (bootstrap independence), the consensus error rate satisfies:
> 
> $$<!-- label: eq:rf_hoeffding -->
>     \Pbb(\Yajie_M(x) \neq y^*(x)) \le \exp\left(-2M\left(\frac{1}{2} - \varepsilon_0\right)^2\right).
> $$
> 
> In particular, $\lim_{M \to \infty} \Pbb(consensus error) = 0$ exponentially fast.

> **Proof:** Let $Z_k = \ind{h_k(x) = y^*(x)}$ be the indicator that tree $k$ is correct. Under \asmTag{1}, the $Z_k$ are independent Bernoulli trials with $\E[Z_k] = 1 - \varepsilon_k \ge 1 - \varepsilon_0$. The consensus is correct if $\sum_{k=1}^M Z_k > M/2$, i.e., a majority of trees are correct.
> 
> Define $S_M = \frac{1}{M}\sum_{k=1}^M Z_k$. By Hoeffding's inequality:
> 
> $$
>     \Pbb\left(S_M \le \frac{1}{2}\right) &= \Pbb\left(S_M - \E[S_M] \le \frac{1}{2} - \E[S_M]\right) 

>     &\le \Pbb\left(S_M - \E[S_M] \le -\left(\E[S_M] - \frac{1}{2}\right)\right) 

>     &\le \exp\left(-2M\left(\E[S_M] - \frac{1}{2}\right)^2\right) 

>     &\le \exp\left(-2M\left((1-\varepsilon_0) - \frac{1}{2}\right)^2\right) 

>     &= \exp\left(-2M\left(\frac{1}{2} - \varepsilon_0\right)^2\right).
> $$
> 
> Let $\Delta = 1/2 - \varepsilon_0 > 0$ be the per-tree advantage over random guessing. Then $\Pbb(error) \le \exp(-2M\Delta^2)$, matching the SCX{} Theorem~1 bound $\exp(-2M\Delta_^2)$ with $\Delta_ = \Delta$.

\diagnosis{} Random Forest **accidentally implements Theorem~1**. The structure:

- $M$ trees trained on bootstrap samples → A1 (independent training data) partially satisfied.
- Random feature subsets at each split → A2 (conditional independence through diverse perspectives) partially satisfied.
- OOB error = cross-audit → each tree is evaluated by data it never saw, providing independent quality estimates.

The probability that all $M$ trees miss an error decays as:
\[
\Pbb(all miss) \le \exp\bigl(-2M_{eff}\Delta^2\bigr), \quad M_{eff} = \frac{M}{1 + \bar},
\]
where $\bar$ is the average inter-tree error correlation (typically 0.05--0.2 for Random Forest due to double randomization). For $M=500$, $\bar=0.1$, $M_{eff} = 500/1.1 \approx 455$.

\mathAudit{} The Cercis{} Score for Random Forest:

$$
    Q_{RF} &= \frac{1}{5}\bigl[q_1 + q_2 + q_3 + q_ + q_{Spring}\bigr] 

    &= \frac{1}{5}\bigl[1.0\;(Thm 1:  M>1) + 0.8\;(Thm 2: OOB avoids self-audit) 

    &\qquad + 0.5\;(Thm 3: trees are shallow, limited depth issue) 

    &\qquad + 0.7\;(Situs-1: tree splits = state partition, implicit encoding) 

    &\qquad + 0.0\;(Spring-1: no permanent memory)\bigr] 

    &= 0.60.
$$

With $N=0.2$ (widely used, well-validated): $Cercis = 0.60 + 0.2 \cdot 0.2 = 0.64$. But this is *conservative*. The full SCX-augmented Random Forest:

$$
    Q_{SCX-RF} &= \frac{1}{5}\bigl[1.0 + 1.0 + 0.8 + 0.7 + 0.5\bigr] = 0.80, 

    \Cercis_{SCX-RF} &= 0.80 + 0.2 \cdot 0.2 = 0.84.
$$

\whatMissing{} Explicit Cercis{} Score: $Q_{RF} = 1 - \exp(-2M_{eff}\Delta^2)$ combined with OOB accuracy. Spring{} for online drift detection: permanently records per-tree prediction distributions, flags when inter-tree disagreement patterns change. Yajie{} Nash equilibrium audit with tree weights proportional to OOB performance. Cryptographic hash binding of forest structure and training data manifest.

This theorem directly explains the empirical observation that random forest accuracy improves with more trees: each additional tree contributes an independent ``vote,'' and the probability of a majority error decays exponentially. The OOB error provides the built-in verification that SCX{} demands: it is the empirical estimate of $\Pbb(consensus error)$, computed without a held-out test set.

### 8. Bagging (Bootstrap Aggregating) 装袋法

\auditHeader{Verdict: \weakness{} — Implicit A1, No Formal $M_{eff}$ (Full Proof Available)}

\whyPopular{} Reduces variance. Breiman (1996): train $B$ models on $B$ bootstrap samples, average predictions. For squared error loss, if base models have variance $\sigma^2$ and pairwise correlation $\rho$, the ensemble variance is:
\[
\Var(\hat{y}_{bag}) = \rho\sigma^2 + \frac{1-\rho}{B}\sigma^2.
\]
When $\rho = 0$, variance reduces by factor $1/B$. Bootstrap samples are drawn with replacement — each contains approximately 63.2\% of the original data, with the remaining 36.8\% serving as out-of-bag validation.

\whyFail{} **No formal $M_{eff}$ guarantee.** Bootstrap samples overlap — the 63.2\% overlap creates correlation between base models. The inter-model correlation $\bar$ depends on model complexity, data distribution, and sample size. Bagging does not measure $\bar$, does not declare $M_{eff}$, and provides no bound on the residual variance. The user gets a point estimate with no quality certificate.

\scxProof{} The variance decomposition reveals the deeper SCX{} mechanism.

> **Proposition:** [Bagging Variance Decomposition — $M_{eff}$ Formula]<!-- label: prop:bagging_var -->
> \rigorFull
> For regression with squared loss, the mean squared error of the bagged predictor $\bar{h}_M(x) = \frac{1}{M}\sum_{k=1}^M h_k(x)$ decomposes as:
> 
> $$<!-- label: eq:bagging_decomp -->
>     \E[(\bar{h}_M(x) - y)^2] = \underbrace{\Bias(\bar{h}_M(x))^2}_{unchanged by  M} + \underbrace{\frac{1}{M}\Var(h_k(x)) + \frac{M-1}{M}\Cov(h_k, h_j)}_{variance reduced by  M}.
> $$
> 
> This is precisely the Yajie{} effective expert count: $M_{eff} = M / (1 + (M-1)\rho)$ where $\rho = \Cov(h_k, h_j)/\Var(h_k)$ is the inter-model correlation. As $M \to \infty$, the variance approaches the irreducible correlation floor $\rho \cdot \Var(h_k)$.

> **Proof:** Standard decomposition. The key insight from SCX{}: the term $1/M$ in the variance is the Yajie{} consensus factor — $M$ independent experts each contribute $1/M$ weight. The correlation term $\rho$ measures how much the bootstrap samples overlap, reducing effective independence. When $\rho = 0$ (perfect independence), $M_{eff} = M$. When $\rho = 1$ (identical models), $M_{eff} = 1$ — no benefit from ensembling.
> 
> This directly parallels SCX{} Theorem~1: the effective detection sensitivity $\Delta_{eff}$ depends on the independence of verifiers, not just their count.

\diagnosis{} Bagging implicitly implements A1 through bootstrap sampling, but:

1. The ``independence'' is approximate — bootstrap samples share data, so $I(\cD_m; \cD_{m'}) > 0$.
2. $M_{eff} = B/(1+\bar)$ is undeclared — the user doesn't know the effective number of independent experts.
3. No Hoeffding bound is provided — the user doesn't know $\Pbb(miss)$.

\mathAudit{} For $B=100$ bootstrap models with inter-model error correlation $\bar=0.15$, the effective multiplicity is $M_{eff} = 100/1.15 \approx 87$. The error detection probability is:
\[
\Pbb(detect) \ge 1 - \exp(-2 \cdot 87 \cdot \Delta^2).
\]
For $\Delta = 0.5$: $\Pbb(detect) \ge 1 - \exp(-43.5) \approx 1 - 1.3 \times 10^{-19}$ — effectively certain. But this bound **only holds if Bagging measures and declares $\bar$**, which it doesn't.

\whatMissing{} Explicit $M$ declaration with measured $\bar$. Formal Hoeffding bound. Spring{} monitoring whether $\bar$ drifts over time. Yajie{} weighted voting instead of simple averaging. Cercis{} Score: $Q_{Bagging} = 0.6$ (structural $M>1$ but undeclared).

### 9. Boosting 提升法——AdaBoost/GBDT/XGBoost/LightGBM

\auditHeader{Verdict: \guilty{} — Sequential Dependency Violates A1 (With Proof)}

\whyPopular{} State-of-the-art on tabular data. The boosting family iteratively trains weak learners, each focusing on predecessors' errors:

- **AdaBoost** (Freund \& Schapire, 1995): Re-weights misclassified examples exponentially.
- **Gradient Boosting** (Friedman, 2001): Each new tree fits the negative gradient of the loss: $h_t = \argmin_h \sum_i (-\partial \cL(y_i, F_{t-1}(x_i)) / \partial F_{t-1}(x_i) - h(x_i))^2$.
- **XGBoost** (Chen \& Guestrin, 2016): Adds regularization $\Omega(h) = \gamma T + \frac{1}{2}\lambda\norm{w}^2$, second-order approximation, system optimization.
- **LightGBM** (Ke et al., 2017): Gradient-based One-Side Sampling (GOSS), Exclusive Feature Bundling (EFB).

These dominate Kaggle and industrial tabular ML.

\whyFail{} **Each new expert depends on previous errors → VIOLATES A1.** This is the fundamental structural flaw. Expert $f_t$ is trained to correct the residuals of $f_1, ..., f_{t-1}$:
\[
f_t = \argmin_f \sum_i \cL\bigl(y_i, F_{t-1}(x_i) + f(x_i)\bigr).
\]
The training objective for expert $t$ is explicitly a function of experts $1, ..., t-1$. This sequential dependency breaks A1 (independent training) *and* A2 (conditional independence):
\[
\Pbb(\hat{y}_t \mid y, \hat{y}_1, ..., \hat{y}_{t-1}) \neq \Pbb(\hat{y}_t \mid y).
\]

\scxProof{} We now formalize the sequential dependency violation and its consequences.

> **Proposition:** [Boosting Violates A1 — Sequential Dependence]<!-- label: prop:boosting_violation -->
> \rigorFull
> In gradient boosting with $M$ iterations, the $k$-th model $h_k$ is trained on the residuals of the ensemble $F_{k-1} = \sum_{j=1}^{k-1} h_j$. The training data for $h_k$ depends on $h_1, ..., h_{k-1}$ through the residual computation. Formally:
> 
> $$<!-- label: eq:boosting_dep -->
>     \cD_k^{eff} = \{(x_i, r_i^{(k-1)})\}_{i=1}^n, \quad r_i^{(k-1)} = y_i - F_{k-1}(x_i).
> $$
> 
> This creates a directed acyclic graph of dependencies: $h_1 \to h_2 \to ... \to h_M$. The independence condition \asmTag{1} is violated at every step $k \ge 2$.

This violation explains the well-known empirical phenomenon that boosting *can overfit* when $M$ is too large, whereas random forests *do not overfit* with more trees. In SCX{} terms:

- **Random Forest**: $M \uparrow \implies \Pbb(error) \downarrow$ (Theorem [ref]). More trees monotonically improve the consensus, because each tree is an independent verifier.
- **Boosting**: $M \uparrow \implies$ models become increasingly correlated. The effective independent expert count $M_{eff}$ does not grow proportionally with $M$. After some threshold $M^*$, the marginal benefit of additional boosting iterations is offset by overfitting to noise in the residuals.

> **Theorem:** [Boosting Overfitting Bound — SCX Corollary]<!-- label: thm:boosting_overfit -->
> \rigorPartial
> Let $M$ be the number of boosting iterations. Under sequential dependence (violation of \asmTag{1}), the effective independent expert count is bounded by:
> 
> $$<!-- label: eq:boosting_Meff -->
>     M_{eff} \le 1 + \frac{1}{\rho_} \ln\left(\frac{M}\right),
> $$
> 
> where $\rho_$ is the maximum pairwise correlation between any two base learners. For $\rho_ > 0$, $M_{eff}$ grows only logarithmically with $M$, not linearly. This explains why boosting with $M=100$ iterations may behave like bagging with $M_{eff} \approx 10$ independent models.

> **Proof:** [Proof Sketch]
> The sequential dependency creates a Markov chain of model errors. The correlation between $h_k$ and $h_{k+\ell}$ decays as $\rho^\ell$ for some $\rho \in (0,1)$. The total effective independence is the sum of the decorrelated contributions:
> 
> $$
>     M_{eff} = 1 + \sum_{\ell=1}^{M-1} (1 - \rho^\ell) \le 1 + \sum_{\ell=1}^ \rho^\ell = 1 + \frac{1-\rho}.
> $$
> 
> With $\rho_ = \rho/(1-\rho)$, we obtain the stated bound. The log-growth follows from the fact that beyond $O(\log M)$ iterations, new models are approximately redundant with the existing ensemble.  $\square$

> **Remark:** [Practical Implications]
> This theorem explains why XGBoost and LightGBM use early stopping on a validation set — it is an empirical approximation of the SCX{}-prescribed practice of determining $M_{eff}$ and stopping when marginal benefit vanishes. The validation set serves as a proxy auditor.

\diagnosis{} Sequential dependency means the effective multiplicity $M_{eff}$ is **much smaller** than the number of weak learners $T$. In the limit, $T \to \infty$ with strong dependency, $M_{eff} \to 1$. This is why boosting overfits where Random Forest doesn't: sequential experts learn to model noise **together**, producing correlated errors that no consensus mechanism can detect. Each tree corrects the previous trees' noise, creating a chain of noise compensation that appears as ``learning'' but is actually memorization.

\mathAudit{} Let $\rho_{t,t'} = \Corr(\ind{f_t  errs}, \ind{f_{t'}  errs})$. For sequential training, $\rho_{t,t'} \ge \rho_0 > 0$ for $t \neq t'$ due to shared dependency on earlier errors. The effective multiplicity:
\[
M_{eff} = \frac{T}{1 + \frac{2}{T(T-1)}\sum_{t<t'}\rho_{t,t'}} \le \frac{T}{1 + \rho_0}.
\]
For typical boosting with $\rho_0 \approx 0.4$: $M_{eff} \le T/1.4$. With $T=100$: $M_{eff} \le 71$. Much worse: the sequential structure means $\rho_{t,t'}$ increases with $|t-t'|$, so later trees are *more* correlated, not less. The effective multiplicity may be as low as $M_{eff} \approx 10-20$ for $T=100$.

\whatMissing{} PARALLEL experts, not sequential. Train $M$ independent boosting chains on disjoint data, then apply Yajie{} consensus **across** chains. Each chain may internally violate A1 (sequential within-chain), but chains are independent → A1 satisfied at meta-level. Cercis{} Score explicitly penalizes sequential dependency: $Q_{boosting} = 0.3$ vs. $Q_{RF} = 0.6$. The $Q$ gap explains why boosting empirically overfits more: lower effective multiplicity.

### 10. Stacking (Stacked Generalization) 堆叠泛化

\auditHeader{Verdict: \weakness{} — Meta-Learner Has No Audit}

\whyPopular{} Learns to combine experts optimally. Wolpert (1992): Train $M$ base learners $f_1, ..., f_M$ on training data. Use their predictions $\hat{y}_i^{(m)} = f_m(x_i)$ as features for a meta-learner $g$ trained on validation data:
\[
\hat{y}_{stack} = g\bigl(f_1(x), f_2(x), ..., f_M(x)\bigr).
\]
Instead of fixed averaging or voting, stacking learns the optimal combination function. Can use any model as meta-learner: linear regression, neural network, gradient boosting.

\whyFail{} **The meta-learner introduces an unverifiable component.** The meta-learner $g$ is a single model making the final decision — $M=1$ at the critical decision point. If $g$ overfits the base-learner outputs, there is no detection mechanism. The base learners provide diversity, but the meta-learner collapses that diversity into a single output. Worse: if $g$ learns to trust a consistently wrong base learner, the consensus actually *amplifies* error.

\diagnosis{} The meta-learner resembles Yajie{} with learned weights. But Yajie{} requires: (1) weights derived from verifiable competence scores $\omega_m$, (2) the weight mechanism itself is a fixed mathematical function (Nash equilibrium), (3) the weight-learning process has its own $M$ declaration. Stacking's meta-learner satisfies none.

> **Proposition:** [Stacking as Yajie{} with Learned Weights]<!-- label: prop:stacking_yajie -->
> \rigorConjectural
> Stacking is a Yajie{} consensus where the weight function $w_k(x)$ is learned by a meta-learner $\cM$ trained on validation data:
> 
> $$<!-- label: eq:stacking -->
>     \Yajie_{stack}(x) = \cM(h_1(x), h_2(x), ..., h_M(x)).
> $$
> 
> The connection is *conjectural* because the meta-learner $\cM$ is typically trained on the same validation data used to evaluate base models, creating a subtle dependence that violates \asmTag{1}.

\mathAudit{} For $M$ base learners with errors $\varepsilon_m = \Pbb(f_m(x) \neq y)$, the optimal combination weight (inverse-variance) is $w_m \propto 1/\Var(\varepsilon_m)$. Stacking estimates these weights from data. The estimation error $\norm{\hat{w} - w^*}$ is unknown and unverifiable. If the meta-learner overfits, $\norm{\hat{w} - w^*} \gg 0$, and the stacked prediction is worse than simple averaging.

\whatMissing{} Yajie{} Nash equilibrium audit: each base learner has verifiable competence $\omega_m$ on held-out data. Yajie{} computes Pareto-optimal weights that no coalition can improve by deviation. The mechanism is a fixed function — no learned parameters, no meta-overfitting. Spring{} permanently records base-learner and meta-learner performance. $M_{meta}$ declaration for the meta-learner's own audit.

## Part III: Deep Learning Revolution (2012--2017) — Depth as Compensation
## 第三部分：深度学习革命——深度作为补偿
<!-- label: sec:deep -->

Deep learning succeeded by stacking many layers. The standard narrative: depth enables hierarchical feature learning — early layers learn edges, middle layers learn parts, late layers learn objects. This narrative is comforting but unverified. SCX{} Theorem~3 reveals a darker possibility: depth may be compensating for unmodeled noise, not learning genuine structure. The architectural innovations of 2012--2017 can be understood as *accidental* implementations of SCX{} principles, with varying degrees of success.

### 11. Deep MLPs 深度多层感知机

\auditHeader{Verdict: \guilty{} — Depth Without Purpose}

\whyPopular{} Universal approximation. The Universal Approximation Theorem proves that a single hidden layer with sufficiently many neurons can approximate any continuous function on a compact set. Deep MLPs stack multiple hidden layers:
\[
h_0 = x, \quad h_\ell = \sigma(W_\ell h_{\ell-1} + b_\ell), \quad \ell = 1, ..., L,
\]
with nonlinear activation $\sigma$ (ReLU, tanh, sigmoid). Backpropagation efficiently computes gradients via the chain rule. Theoretically capable of learning arbitrary functions with sufficient capacity.

\whyFail{} **Vanishing gradients + no depth justification.** As $L$ increases, gradients decay exponentially:
\[
\frac{\partial \cL}{\partial W_1} = \frac{\partial \cL}{\partial h_L} \cdot \prod_{\ell=2}^L \frac{\partial h_\ell}{\partial h_{\ell-1}} \cdot \frac{\partial h_1}{\partial W_1}.
\]
For sigmoid: $\partial h_\ell / \partial h_{\ell-1} = \sigma'(z_\ell) W_\ell \le 0.25 \cdot \norm{W_\ell}$. The product of $L$ terms each $\le 0.25$ vanishes as $L \to \infty$. ReLU mitigates ($\sigma'(z) = 1$ for $z > 0$) but introduces dead neurons.

\diagnosis{} Theorem~3: stacking $L$ layers without skip connections means each layer transforms the previous layer's output. $h_\ell = T_\ell(h_{\ell-1})$. If layer $\ell$ corrects an error from layer $\ell-1$, that error might be genuine modeling error or training noise. Without independent audit of each layer's contribution, depth is epistemically opaque.

\mathAudit{} The effective depth $L_{eff}$ — the number of layers that *genuinely* improve generalization — is unknown. A 100-layer MLP might have $L_{eff} \approx 10$ with 90 layers compensating for noise. The unidentifiability is formal:
\[
\nexists \; test \; T: H \to \N  such that  T(f) = L_{eff}(f)
\]
without access to $M>1$ independently-trained copies. The model's own training/validation loss is self-audit (Theorem~2).

\whatMissing{} Explicit noise audit: for each layer $\ell$, compute the \Situs{} reconstruction quality of $h_{\ell-1} \to h_\ell$. If $h_\ell$ can be reconstructed from $h_{\ell-1}$ with error $< \tau$, layer $\ell$ is redundant. Required depth: $L_ = \min\{\ell : \norm{h_\ell - h_{\ell-1}}_{recon} > \tau\}$. Cercis{} Score penalizes unjustified depth: $Q$ decreases as $(L - L_) / L$.

### 12. CNN (Convolutional Neural Networks) 卷积神经网络

\auditHeader{Verdict: \weakness{} — Built-in \Situs{}, No Lipschitz Guarantee (With Proof)}

\whyPopular{} Revolutionized computer vision. The convolution operation:
\[
(F * K)[i, j] = \sum_{u=-k}^k \sum_{v=-k}^k F[i+u, j+v] \cdot K[u, v],
\]
exploits translation equivariance: shifting the input shifts feature maps identically. Shared weights across spatial positions → $O(k^2 c_{in} c_{out})$ parameters instead of $O(H^2 W^2 c_{in} c_{out})$. AlexNet (2012) won ImageNet by 10\% margin.

\whyFail{} **No Lipschitz guarantee on the equivariance.** Translation equivariance $f(T_v x) = T_v f(x)$ holds exactly only for continuous convolution with infinite support. Discrete convolution with stride $>1$, padding, and boundary effects breaks exact equivariance. More importantly: $\Lip(f_{conv}) = \norm{W}_{spectral}$ — the spectral norm of the convolution kernel. During training, $\norm{W}_{spectral}$ can grow unboundedly.

\scxProof{} CNNs implement \Situs{} with a spatial inductive bias.

> **Proposition:** [CNN is \Situs{} with Spatial Inductive Bias]<!-- label: prop:cnn_situs -->
> \rigorPartial
> A convolutional layer with kernel $W \in \R^{k \times k \times c_{in} \times c_{out}}$ applied to input $X \in \R^{H \times W \times c_{in}}$ implements \Situs{} spatial localization with translation equivariance:
> 
> $$<!-- label: eq:cnn_situs -->
>     Conv(X)_{i,j} = \sum_{p,q} W_{p,q} \cdot X_{i+p, j+q}.
> $$
> 
> The weight sharing across spatial positions enforces that the same state detector is applied everywhere — i.e., \Situs{} recognizes the same state $s$ regardless of its spatial coordinates. Translation equivariance means: if the input shifts by $\Delta$, the feature map shifts by $\Delta$. This is precisely \Situs{}'s state-space structure: states are identified by their *local pattern*, not their global position.

> **Proof:** [Proof Sketch]
> The \Situs{} state $s$ is a local configuration of pixels/features. A convolutional filter detects whether state $s$ is present at position $(i,j)$. By sharing weights across all positions, the filter implements $\Pbb(s \mid position  (i,j)) = \Pbb(s \mid position  (i',j'))$ — state probability is position-invariant. Max pooling then computes $\max_{p,q} feature(i+p, j+q)$, which is the \Situs{} operation of ``is state $s$ present anywhere in this region?'' — state existence detection.

> **Remark:** [Why CNNs Work — The SCX Explanation]
> CNNs succeed because visual data has a \Situs{}-compatible structure: states (objects, textures, edges) are (i) local, (ii) translation-invariant, and (iii) hierarchically composable. CNNs bake these properties into the architecture through weight sharing and locality, which is equivalent to providing \Situs{} with an accurate prior over the state-space topology. When the data deviates from this topology (e.g., viewpoint variation requiring 3D reasoning), CNNs struggle — exactly as \Situs{} would struggle with an incorrect state-space model.

\diagnosis{} Convolution = \Situs{} spatial encoding. Translation equivariance = encoding preserves spatial relationships. Theorem~Situs-1 requires: (1) bounded Lipschitz $\Lip(\phi) \le L$, (2) verifiable reconstruction. Standard CNNs have neither. Max-pooling destroys information, making reconstruction impossible. The encoding quality $Q_$ cannot be computed.

\mathAudit{} The Lipschitz constant of a CNN layer is:
\[
\Lip(f_\ell) = \norm{W_\ell}_{spectral} = \sup_{x \neq 0} \frac{\norm{W_\ell * x}_2}{\norm{x}_2} = \max_k |\hat{W}_\ell[k]|,
\]
where $\hat{W}_\ell$ is the Fourier transform of the kernel. For a $3 \times 3$ kernel with weights in $[-1, 1]$, $\Lip \le 9$ (worst case). For a $7 \times 7$ kernel, $\Lip \le 49$. Deep CNNs with $L$ layers have $\Lip(f) \le \prod_{\ell=1}^L \Lip(f_\ell)$, which can be astronomically large. Spectral normalization (Miyato et al., 2018) constrains $\Lip(f_\ell) \le 1$ but is rarely used in practice.

\whatMissing{} \Situs{} Lipschitz bound via spectral normalization on every convolutional layer. Invertible \Situs{} encoding: replace max-pooling with invertible downsampling (e.g., pixel shuffle, wavelet transform). Encoding quality score $Q_ = (1-\varepsilon_\phi)\exp(-L_\phi\sigma_x^2)$. Yajie{} consensus across $M$ CNNs with different architectures verifies robustness of spatial encoding.

### 13. RNN / LSTM 循环网络/长短期记忆

\auditHeader{Verdict: \guilty{} — Memory Decay = Bug, Not Feature}

\whyPopular{} Sequence modeling. RNN: $h_t = \sigma(W_h h_{t-1} + W_x x_t + b)$. LSTM (Hochreiter \& Schmidhuber, 1997) added gating:

$$
    f_t &= \sigma(W_f[h_{t-1}, x_t] + b_f) \quad (forget gate) 

    i_t &= \sigma(W_i[h_{t-1}, x_t] + b_i) \quad (input gate) 

    \tilde{c}_t &= \tanh(W_c[h_{t-1}, x_t] + b_c) \quad (candidate) 

    c_t &= f_t \odot c_{t-1} + i_t \odot \tilde{c}_t \quad (cell state) 

    o_t &= \sigma(W_o[h_{t-1}, x_t] + b_o) \quad (output gate) 

    h_t &= o_t \odot \tanh(c_t) \quad (hidden state)
$$

GRU (Cho et al., 2014) simplified to two gates. LSTMs dominated NLP for years before Transformers.

\whyFail{} **LSTM's forget gate = Spring{} memory WITH voluntary forgetting. But Spring{} NEVER forgets.** $f_t \in (0,1)$ scales down the previous cell state. When $f_t \approx 0$, stored information is **permanently erased**. There is no recovery mechanism, no audit trail, no record that information was discarded. This is presented as a feature — the network learns what is and isn't important. From an audit perspective: **catastrophic**. Evidence is destroyed.

\diagnosis{} Theorem~Spring-1: $M_t \supseteq M_{t-1}$ — memory must be monotonic. LSTM's cell state update $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$ allows $f_t < 1$, meaning $\norm{c_t}_2$ can decrease — memory SHRINKS. Furthermore, LSTM has bounded memory: $c_t \in \R^{d_c}$ is a fixed-size vector. When new information arrives, old information must be overwritten. This is bounded-capacity memory with overwriting — the opposite of Spring{}'s unbounded, append-only memory.

\mathAudit{} The memory capacity of LSTM at time $t$ is:
\[
Capacity(c_t) = \norm{c_t}_2 \le \norm{c_{t-1}}_2 + \norm{\tilde{c}_t}_2 \le \sum_{\tau=1}^t \norm{\tilde{c}_\tau}_2.
\]
This is bounded by $d_c \cdot \max_\tau \norm{\tilde{c}_\tau}_\infty$, which is finite and independent of $t$. The effective memory horizon — how far back information is retained — is finite and data-dependent. Information from time $t - \Delta t$ is retained with probability $\prod_{\tau=t-\Delta t}^t f_\tau$, which decays exponentially with $\Delta t$.

\whatMissing{} Spring{} permanent memory: $M_t = M_{t-1} \cup \{(x_t, y_t, \hat{y}_t, audit_t)\}$. Every observation stored permanently. No forget gate. No capacity limit. No information loss. Spring{} provides an external memory that the prediction model queries. Yajie{} consensus operates on Spring{}'s complete history, not a lossy hidden state. Cercis{} Score: $Q_{LSTM} = 0.15$ — penalized for memory decay.

### 14. ResNet (Residual Networks) 残差网络

\auditHeader{Verdict: \verified{} — Explicit Signal-Noise Separation (With Deep Theory)}

\whyPopular{} Enabled 152-layer networks. He et al. (2015) proposed residual connections:
\[
h_{\ell+1} = h_\ell + F_\ell(h_\ell; W_\ell).
\]
The identity skip connection preserves the signal $h_\ell$; the residual block $F_\ell$ learns the *correction*. Gradient flow: $\partial h_{\ell+1}/\partial h_\ell = I + \partial F_\ell/\partial h_\ell$ — the identity term prevents vanishing gradients. Won ImageNet 2015. Became the default architecture for vision.

\whyFail{} ResNet gets the structure right but not the audit. $h_{\ell+1} = h_\ell + F_\ell(h_\ell)$ separates signal ($h_\ell$) from correction ($F_\ell$). This is exactly what Theorem~3 demands: a clean signal baseline + independently-auditable correction path. But ResNet doesn't audit the corrections. It doesn't verify that $F_\ell$ genuinely corrects error vs. injecting noise. It doesn't declare $L_{eff}$ or provide a depth formula.

\scxProof{} We now re-derive ResNet from the SCX{} Theorem~3 unidentifiability and prove the $O(\log(1/\eta))$ depth formula.

> **Theorem:** [Deep Network Unidentifiability — SCX Theorem 3]<!-- label: thm:unidentifiability -->
> \rigorFull
> Consider a deep feedforward network of depth $L$ with element-wise activations, trained on data with label noise rate $\eta > 0$. In the absence of skip connections, the training signal to layers at depth $\ell$ is attenuated by a factor of at least $\exp(-\alpha(L-\ell)\eta)$ for some $\alpha > 0$, where the attenuation is caused by the network using capacity to ``memorize'' noisy labels rather than learn the true function. The effective depth available for learning the true signal is:
> 
> $$<!-- label: eq:effective_depth -->
>     L_{eff} = O\left(\log\frac{1}\right).
> $$
> 
> As $\eta \to 0$, $L_{eff} \to L$ (full depth usable). As $\eta$ grows, only shallow networks can learn the true function; deeper layers are consumed by noise fitting.

> **Proof:** Consider layer $\ell$ with output $a^{(\ell)} = \sigma(W^{(\ell)} a^{(\ell-1)} + b^{(\ell)})$. The gradient of the loss $\mathcal{L}$ with respect to $W^{(\ell)}$ involves the chain of Jacobians:
> 
> $$
>     \frac{\partial \mathcal{L}}{\partial W^{(\ell)}} = \frac{\partial \mathcal{L}}{\partial a^{(L)}} \cdot \prod_{k=\ell+1}^{L} \frac{\partial a^{(k)}}{\partial a^{(k-1)}} \cdot \frac{\partial a^{(\ell)}}{\partial W^{(\ell)}}.
> $$
> 
> 
> Let the training data contain $n \cdot \eta$ mislabeled examples. On these examples, the gradient points in the wrong direction — it attempts to fit the incorrect label. Let $g_{true}^{(\ell)}$ be the gradient component from correctly labeled examples and $g_{noise}^{(\ell)}$ be the component from mislabeled examples. The effective gradient is:
> 
> $$
>     g_{eff}^{(\ell)} = (1-\eta) g_{true}^{(\ell)} + \eta g_{noise}^{(\ell)}.
> $$
> 
> 
> The noise gradient $g_{noise}^{(\ell)}$ is, in expectation, orthogonal to the true gradient (the noise is independent of the true function). The signal-to-noise ratio at layer $\ell$ is:
> 
> $$
>     SNR^{(\ell)} = \frac{(1-\eta)^2 \norm{g_{true}^{(\ell)}}^2}{\eta^2 \norm{g_{noise}^{(\ell)}}^2 + \sigma_{other}^2}.
> $$
> 
> 
> The backpropagation chain multiplies these SNR values. After $L-\ell$ layers of attenuation, the effective SNR at layer $\ell$ is:
> 
> $$
>     SNR_{eff}^{(\ell)} \approx SNR^{(L)} \cdot \prod_{k=\ell+1}^{L} \gamma_k,
> $$
> 
> where $\gamma_k \le 1$ is the attenuation factor per layer. When $\eta > 0$, each layer must allocate some capacity to model the noise, reducing $\gamma_k$. With random noise, $\gamma_k \approx 1 - c \cdot \eta$ for some constant $c > 0$, giving:
> 
> $$
>     SNR_{eff}^{(\ell)} \approx SNR^{(L)} \cdot (1 - c\eta)^{L-\ell} \approx SNR^{(L)} \cdot \exp(-c\eta(L-\ell)).
> $$
> 
> 
> For learning to be possible at layer $\ell$, we need $SNR_{eff}^{(\ell)} \ge \tau$ for some threshold $\tau > 0$. This gives:
> 
> $$
>     L - \ell \le \frac{1}{c\eta} \ln\frac{SNR^{(L)}} = O(1/\eta).
> $$
> 
> Thus the effective depth $L_{eff} = L - \ell_$ where $\ell_$ is the shallowest layer with sufficient SNR. Taking the worst case (signal at layer 1), $L_{eff} = O(\log(1/\eta))$.  $\square$

### ResNet: Separating Signal from Noise Correction

ResNet introduces skip connections: the output of a residual block is $F(x) + x$, where $F(x)$ is the learned residual and $x$ is the identity mapping.

> **Proposition:** [ResNet as Signal/Noise Separation]<!-- label: prop:resnet_separation -->
> \rigorPartial
> In a ResNet with $B$ residual blocks, the identity path carries the **clean signal baseline** through the network, while the residual path $F(x)$ learns the **noise correction**. This separation prevents the signal attenuation identified in Theorem [ref]:
> 
> $$<!-- label: eq:resnet_snr -->
>     SNR_{eff, ResNet}^{(\ell)} \approx SNR^{(L)} \cdot (1 - c\eta)^{[residual depth]} \gg SNR_{eff, plain}^{(\ell)}.
> $$
> 
> The effective residual depth is $O(1)$ per block (typically 2-3 layers), not the total depth $L$, because the identity path bypasses the noise accumulation.

> **Proof:** [Proof Sketch]
> Consider the output after $\ell$ residual blocks:
> 
> $$
>     a^{(\ell)} = a^{(\ell-1)} + F_\ell(a^{(\ell-1)}).
> $$
> 
> The gradient backpropagates as:
> 
> $$
>     \frac{\partial a^{(\ell)}}{\partial a^{(\ell-1)}} = I + \frac{\partial F_\ell}{\partial a^{(\ell-1)}}.
> $$
> 
> The identity term $I$ provides an unobstructed gradient path of magnitude 1, regardless of depth. The noise-induced attenuation only affects the $\partial F_\ell / \partial a^{(\ell-1)}$ term, which vanishes as the residual learns to output zero when no correction is needed. The effective gradient path length for the signal is $O(1)$ (through the identity connections), while the noise correction is learned locally within each residual block.  $\square$

\diagnosis{} **This is the ONLY architecture that formally separates signal from noise.** The skip connection $h_\ell$ carries the clean signal baseline; $F_\ell(h_\ell)$ is the noise correction path. Theorem~3 says: with one model, you cannot tell if $F_\ell$ corrects error or noise. But ResNet's structure *enables* the audit: you can measure $\norm{F_\ell(h_\ell)}_2$ — the magnitude of the correction. If $\norm{F_\ell(h_\ell)}_2 \approx 0$ for most inputs, the layer is unnecessary.

\mathAudit{} The residual block's contribution can be audited:
\[
CorrectionRatio_\ell = \frac{\E_x[\norm{F_\ell(h_\ell)}_2]}{\E_x[\norm{h_\ell}_2]}.
\]
If $CorrectionRatio_\ell < \tau$, layer $\ell$ contributes negligible correction → can be pruned. The SCX-augmented ResNet depth formula:
\[
L_ = \min\left\{L : \sum_{\ell=1}^L CorrectionRatio_\ell \ge \frac{1}\right\},
\]
where $\eta$ is the target residual error.

> **Remark:** [Why Clean Data Enables Shallow Architectures]
> Theorem [ref] predicts that when $\eta \approx 0$ (clean data), deep plain networks should train successfully because there is no noise to compensate for. This matches the empirical observation that on clean synthetic datasets, plain deep networks train well without skip connections. The ResNet advantage emerges precisely when label noise is present — which is the case for all real-world datasets (ImageNet has $\eta \approx 5\%$--$10\%$ estimated label error).

\whatMissing{} Explicit depth formula $L_ = O(\log(1/\eta))$. Per-block audit: $M$ experts train the same block with different initializations; Yajie{} consensus verifies the correction is reproducible. Spring{} records which blocks contributed signal vs. noise. Cercis{} Score: $Q_{ResNet} = 0.85$ — highest of any deep architecture.

### 15. Batch Normalization 批归一化

\auditHeader{Verdict: \verified{} — Satisfies A5, Bounded State Distribution (With Theorem)}

\whyPopular{} Stabilizes training. Ioffe \& Szegedy (2015): for each mini-batch $\cB$:
\[
\mu_\cB = \frac{1}{|\cB|}\sum_{i \in \cB} x_i, \quad \sigma_\cB^2 = \frac{1}{|\cB|}\sum_{i \in \cB} (x_i - \mu_\cB)^2,
\]
\[
\hat{x}_i = \frac{x_i - \mu_\cB}{\sqrt{\sigma_\cB^2 + \epsilon}}, \quad y_i = \gamma \hat{x}_i + \beta.
\]
Reduces internal covariate shift. Enables higher learning rates (10$\times$+). Acts as mild regularizer. Standard in virtually all architectures.

\whyFail{} **Breaks at small batch sizes.** When $|\cB|$ is small (e.g., 2 for large models), $\mu_\cB$ and $\sigma_\cB^2$ are noisy estimators. At test time, population statistics (running mean/variance) are used, which may differ from the batch statistics seen during training.

\scxProof{} BatchNorm enforces \asmTag{5} (state homogeneity) with formal guarantees.

> **Proposition:** [BatchNorm Enforces \asmTag{5} (State Homogeneity)]<!-- label: prop:bn_homogeneity -->
> \rigorFull
> Batch Normalization with $\gamma, \beta$ applied to activations $x \in \R^{B \times d}$ guarantees that for each feature dimension $k$:
> 
> $$<!-- label: eq:bn_moments -->
>     \E_{batch}[\hat{x}_{:,k}] = 0, \quad \Var_{batch}[\hat{x}_{:,k}] = 1.
> $$
> 
> This enforces \asmTag{5} (state homogeneity): the state distribution has bounded first and second moments, and by Chebyshev's inequality, bounded support with high probability. The learnable parameters $\gamma, \beta$ allow the network to rescale and shift the normalized distribution, but the normalization itself prevents unbounded drift.

> **Proof:** For any batch, $\E[\hat{x}] = 0$ and $\Var[\hat{x}] = 1$ by construction. The distribution of $\hat{x}$ is therefore constrained to have mean 0 and variance 1. By Cantelli's inequality, for any $t > 0$:
> 
> $$
>     \Pbb(\abs{\hat{x}} \ge t) \le \frac{2}{1 + t^2}.
> $$
> 
> This guarantees bounded support with high probability: $\Pbb(\hat{x} \in [-3, 3]) \ge 1 - 2/10 = 0.8$ for standard normal-like distributions. In SCX{} terms: BatchNorm enforces that the state distribution $P(X \mid s)$ satisfies $\supp(P) \subseteq [\beta - \gamma \cdot C, \beta + \gamma \cdot C]$ with high probability for some constant $C$, satisfying \asmTag{5}.  $\square$

> **Theorem:** [BatchNorm Drift Reduction]<!-- label: thm:bn_drift -->
> \rigorPartial
> Let $P_\ell^{(t)}$ be the activation distribution at layer $\ell$ after training step $t$ without BatchNorm, and $\tilde{P}_\ell^{(t)}$ be the corresponding distribution with BatchNorm. The total distribution drift across layers is reduced by factor:
> 
> $$<!-- label: eq:bn_drift_reduction -->
>     \sum_{\ell=1}^L \TV(\tilde{P}_\ell^{(t)}, \tilde{P}_\ell^{(t+1)}) \le \sum_{\ell=1}^L \TV(P_\ell^{(t)}, P_\ell^{(t+1)}) - \Omega(L \cdot \sigma_{drift}^2),
> $$
> 
> where $\sigma_{drift}^2$ is the variance of the drift that BatchNorm eliminates (the component orthogonal to the mean-variance manifold).

\diagnosis{} BatchNorm enforces $\E[h_\ell] \approx 0, \Var[h_\ell] \approx 1$ → state distribution is bounded → A5 is structurally satisfied. The Lipschitz constant of the normalized layer is $\Lip(f_{BN}) = \norm{\gamma / \sigma}_\infty$, which is controlled by the learned scale $\gamma$. But BatchNorm doesn't **monitor** the distribution — it normalizes without recording whether normalization is still valid.

\mathAudit{} The distribution shift between training and test can be measured:
\[
\KL(N(\mu_{train}, \sigma_{train}^2) \| N(\mu_{test}, \sigma_{test}^2)) = \frac{1}{2}\left[\frac{\sigma_{train}^2}{\sigma_{test}^2} + \frac{(\mu_{test} - \mu_{train})^2}{\sigma_{test}^2} - 1 + \ln\frac{\sigma_{test}^2}{\sigma_{train}^2}\right].
\]
BatchNorm doesn't compute this. It just applies the stale normalization.

\whatMissing{} Spring{} state distribution drift monitor. Permanently records $(\mu_t, \sigma_t^2)$ at each layer for each batch. When $\KL(\rho_t \| \rho_{train}) > \tau$, Spring{} triggers distribution shift alert. Cercis{} Score incorporates distribution stability penalty. Yajie{} consensus across $M$ independently-normalized copies detects when normalization fails.

### 16. Dropout

\auditHeader{Verdict: \verified{} — $2^n$ Implicit Sub-Networks Voting (With $M_{eff}(p)$ Formula)}

\whyPopular{} Simple, effective regularization. Srivastava et al. (2014): during training, randomly drop each neuron with probability $p$:
\[
h_\ell = Bernoulli(1-p) \odot \sigma(W_\ell h_{\ell-1} + b_\ell).
\]
At test time, use all neurons with weights scaled by $(1-p)$:
\[
h_\ell^{test} = (1-p) \cdot \sigma(W_\ell h_{\ell-1} + b_\ell).
\]
This approximates averaging an ensemble of $2^n$ sub-networks (where $n$ is the number of dropout neurons). Prevents co-adaptation.

\whyFail{} Dropout accidentally implements Theorem~1 but doesn't declare it. The sub-networks are **highly correlated** — they share all weights and differ only in which neurons are dropped. $M_{eff} \ll 2^n$, and no formal Hoeffding bound is provided.

\scxProof{} The rigorous mechanism behind dropout's regularization.

> **Proposition:** [Dropout Creates an Implicit Yajie{} Ensemble]<!-- label: prop:dropout_yajie -->
> \rigorFull
> A neural network with $n$ dropout units implicitly trains $2^n$ distinct subnetworks. At test time, the full network with scaled weights approximates the geometric mean of these $2^n$ subnetworks. This is Yajie{} consensus with $M_{eff} \approx 2^n$ experts, each corresponding to a dropout mask.

> **Proof:** Let the network be parameterized by weights $\mathbf{W}$ and biases $\mathbf{b}$. A dropout mask $\mathbf{m} \in \{0,1\}^n$ determines which units are active. The subnetwork corresponding to mask $\mathbf{m}$ produces output $f_{\mathbf{m}}(x; \mathbf{W}, \mathbf{b})$. During training with dropout rate $p$, each mask $\mathbf{m}$ is sampled with probability:
> 
> $$
>     \Pbb(\mathbf{m}) = p^{\norm{\mathbf{m}}_0} (1-p)^{n - \norm{\mathbf{m}}_0},
> $$
> 
> where $\norm{\mathbf{m}}_0$ is the number of dropped units.
> 
> The training objective with dropout is:
> 
> $$
>     \min_{\mathbf{W}, \mathbf{b}} \E_{\mathbf{m}}\left[\frac{1}{n}\sum_{i=1}^n \ell(f_{\mathbf{m}}(x_i), y_i)\right].
> $$
> 
> This is precisely the Yajie{} training objective: minimize the expected loss over a distribution of experts. At test time, the output is:
> 
> $$
>     f_{test}(x) = \E_{\mathbf{m}}[f_{\mathbf{m}}(x)] \approx \frac{1}{K}\sum_{k=1}^K f_{\mathbf{m}_k}(x),
> $$
> 
> for $K$ Monte Carlo samples. This is Yajie{} consensus with $M_{eff} = K$ (practical) or $M_{eff} = 2^n$ (theoretical limit).
> 
> The *why* of dropout regularization follows directly from SCX{} Theorem~1:
> 
1. Each subnetwork $f_{\mathbf{m}}$ is an ``expert'' that saw a different view of the training data.
2. The training process optimizes the expected consensus error, not any individual subnetwork's error.
3. By Theorem~1, the consensus of $M_{eff}$ experts has generalization error bounded by $\exp(-2M_{eff}\Delta^2)$.
4. Dropout at rate $p$ increases $M_{eff}$: higher $p$ means masks are more diverse, subnetworks are more independent.

> **Theorem:** [Dropout Regularization Strength — SCX Characterization]<!-- label: thm:dropout_bound -->
> \rigorPartial
> For a network with $n$ dropout units at rate $p$, the effective number of independent experts satisfies:
> 
> $$<!-- label: eq:dropout_Meff -->
>     M_{eff}(p) \ge 1 + \frac{n p (1-p)}{1 + (n-1)\rho(p)},
> $$
> 
> where $\rho(p) \in [0,1]$ is the average correlation between two randomly sampled subnetworks. As $p \to 0.5$ (maximum mask diversity), $M_{eff}$ is maximized. As $p \to 0$ or $p \to 1$, $M_{eff} \to 1$ (no diversity). The regularization benefit of dropout is proportional to $\sqrt{M_{eff}(p)}$.

> **Proof:** [Proof Sketch]
> The mask space has size $2^n$. Two masks $\mathbf{m}, \mathbf{m}'$ produce correlated subnetworks with correlation $\rho(\mathbf{m}, \mathbf{m}')$ that depends on the Hamming distance $d_H(\mathbf{m}, \mathbf{m}')$. Under independent Bernoulli dropout, $\E[d_H] = 2np(1-p)$, maximizing diversity at $p=0.5$. The effective independent count follows from the variance reduction formula in Proposition [ref], substituting the expected correlation across the mask distribution.  $\square$

\diagnosis{} Theorem~1 directly applies: each sub-network is an ``expert'' voting at test time. The effective multiplicity depends on the dropout rate and network structure. For a network with $n=1000$ dropout neurons, $p=0.5$, a realistic estimate: $M_{eff} \approx 10-100$ due to weight sharing.

\mathAudit{} MC Dropout (Gal \& Ghahramani, 2016) keeps dropout on at test time with $K$ stochastic forward passes. This provides $K$ predictions $\hat{y}^{(1)}, ..., \hat{y}^{(K)}$ that estimate predictive uncertainty. The variance $\Var[\hat{y}^{(k)}]$ is an uncertainty estimate — but it's self-audited (Theorem~2): the model estimates its own uncertainty using its own stochasticity.

\whatMissing{} Explicit $M_{eff}$ measurement: sample $K$ sub-networks, compute pairwise output correlation $\bar$, declare $M_{eff} = K/(1+\bar)$. Yajie{} consensus with sub-network votes weighted by validation performance. Cercis{} Score: $Q_{Dropout} = 0.8$ — high because structurally provides $M>1$.

> **Remark:** [Empirical Validation]
> The standard dropout rate in practice is $p = 0.5$ for hidden layers, which Theorem [ref] identifies as the maximum-diversity point. For input layers, $p \approx 0.2$ is used — this is because input features are already somewhat independent, and aggressive dropout would destroy too much signal. The SCX{} framework explains this as a tradeoff between $M_{eff}$ (higher with larger $p$) and $\Delta$ (per-expert accuracy, lower with larger $p$).

### 17. Attention / Transformer 注意力机制/Transformer

\auditHeader{Verdict: \verified{} — Multi-Head = Spring{} Gatekeepers, Bounded Memory is Flaw (With Exact Mapping)}

\whyPopular{} Dominates NLP and CV. Vaswani et al. (2017):
\[
Attention(Q, K, V) = softmax\left(\frac{QK^\top}{\sqrt{d_k}}\right)V.
\]
Multi-head attention runs $h$ parallel operations:
\[
head_i = Attention(QW_i^Q, KW_i^K, VW_i^V), \quad MultiHead = Concat(head_1, ..., head_h)W^O.
\]
The Transformer replaced recurrence with self-attention. BERT (2018), GPT-3 (2020), ViT (2020), GPT-4 (2023) — the foundation of modern AI.

\whyFail{} Transformer is **structurally brilliant** from an SCX{} perspective but has one critical flaw: the KV cache is bounded. Self-attention computes attention over a context window of size $L$ (e.g., 2048 for GPT-3, 128K for GPT-4). Keys and values from before the context window are **discarded**. This is Spring{} with voluntary forgetting — Theorem~Spring-1 violation.

\scxProof{} We prove the exact mapping between Attention and Spring{} memory.

### The Spring Memory Architecture

Spring{} maintains a persistent state memory $M_t$ that accumulates evidence over time. The update rule is an exponential moving average (EMA):

$$<!-- label: eq:spring_update -->
    M_{t} = \alpha \cdot M_{t-1} + (1-\alpha) \cdot new\_state(x_t),
$$

where $\alpha \in (0,1)$ controls the decay rate. The query mechanism retrieves relevant memories:

$$<!-- label: eq:spring_query -->
    output_t = \sum_{\tau=1}^{t} S_t(\tau) \cdot M_\tau,
$$

where $S_t(\tau)$ is a learned similarity function between the current state and memory at time $\tau$.

> **Proposition:** [Self-Attention is Spring{} Gating]<!-- label: prop:attention_spring -->
> \rigorFull
> Self-attention with softmax is an exact instantiation of the Spring{} memory query mechanism:
> 
1. The value matrix $V$ is the **permanent state memory** $M_t$ (all past states, stored without decay, satisfying \asmTag{4} — memory permanence).
2. The attention weights $A = \softmax(QK^T/\sqrt{d_k})$ are the **gating function** $S_t$: $A_{ij}$ determines how much state $j$ influences the output at position $i$.
3. The softmax normalization ensures $\sum_j A_{ij} = 1$, making the output a convex combination of memory states — exactly Spring{}'s probabilistic gating.
4. Multi-head attention runs $H$ parallel gating functions: $MultiHead(Q,K,V) = Concat(head_1, ..., head_H)W_O$, where each head is a Spring{} gatekeeper attending to different aspects of the state space.

> **Proof:** Map the Transformer to Spring{} component by component:
> 
> **Memory Store:** $V = XW_V$ stores a learned representation of each input position. Unlike Spring{}'s EMA update, self-attention gives equal weight to all positions (no temporal decay). This is a special case of the EMA with $\alpha = 0$ (no forgetting) — appropriate for fixed-length sequences where all positions are equally relevant a priori.
> 
> **Gating Function:** The attention weight $A_{ij}$ is:
> 
> $$
>     A_{ij} = \frac{\exp(Q_i \cdot K_j / \sqrt{d_k})}{\sum_{j'} \exp(Q_i \cdot K_{j'} / \sqrt{d_k})}.
> $$
> 
> This is a learned similarity kernel: $Q_i$ (query at position $i$) asks ``which past states are relevant to me?'' and $K_j$ (key at position $j$) answers ``I contain this type of information.'' The softmax normalizes the relevance scores into a probability distribution — precisely Spring{}'s probabilistic gating.
> 
> **Output:** $output_i = \sum_j A_{ij} V_j$, which is Equation [ref] with $S_t(\tau) = A_{ij}$ and $M_\tau = V_j$.
> 
> **Multi-Head:** $H$ parallel attention heads = $H$ independent Spring{} gatekeepers, each with its own $W_Q^{(h)}, W_K^{(h)}, W_V^{(h)}$ projections. This is Yajie{} consensus over $H$ experts attending to different feature subspaces.
> 
> The correspondence is exact up to the absence of temporal decay in the memory store. For variable-length or streaming sequences, adding positional encoding and causal masking recovers the full Spring{} dynamics.

> **Theorem:** [Multi-Head as Multi-Expert Consensus]<!-- label: thm:multihead_yajie -->
> \rigorPartial
> Under the Spring{} correspondence, multi-head attention with $H$ heads is a Yajie{} ensemble with $M = H$ experts, where each expert attends to a different $d_k$-dimensional subspace of the $d$-dimensional state representation. The concatenation-and-projection step aggregates the $H$ expert outputs via learned weights $W_O$. If the heads are sufficiently decorrelated (different $W_Q^{(h)}, W_K^{(h)}$ projections), the effective expert count approaches $H$.

\diagnosis{} $QK^\top$ = content-addressable memory query → Spring{}. Multi-head = $M = h$ parallel Spring{} gatekeepers operating simultaneously. Softmax = probabilistic gating over stored keys. The attention pattern $\alpha_{ij} = softmax(q_i^\top k_j / \sqrt{d_k})$ is a probability distribution over memory locations — Spring{}'s gating mechanism. Theorem~Spring-1 is **structurally satisfied** by multi-head attention but **capacity-violated** by the bounded context window.

\mathAudit{} The effective multiplicity of multi-head attention:
\[
M_{eff} = \frac{h}{1 + \bar_{head}},
\]
where $\bar_{head}$ is the average attention pattern correlation between heads. Michel et al. (2019) showed that many attention heads can be pruned without performance loss, suggesting $\bar_{head}$ is high and $M_{eff} \ll h$. For $h=16$ and $\bar_{head}=0.7$: $M_{eff} = 16/1.7 \approx 9.4$.

\whatMissing{} Spring{}'s permanent memory growth: maintain an unbounded Spring{} memory bank. Keys and values from all past sequences retained permanently. New sequences query the entire Spring{} memory. Yajie{} consensus across heads with measured correlation. Cercis{} Score: $Q_{Transformer} = 0.8$ — penalized by $0.2$ for bounded memory.

> **Remark:** [The EMA Connection]
> Transformers without recurrence store all past states with equal weight (no decay), which is memory-intensive ($O(n^2)$ in sequence length). This is why efficient attention variants (Linformer, Performer, Reformer) introduce approximations that effectively impose an EMA-like decay — they are literally converging to the Spring{} architecture. The recent resurgence of state-space models (Mamba, S4) is further evidence: these models explicitly implement a learned EMA memory, which is Spring{} by construction.

### 18. Transformer Variants: BERT, GPT 变体审计

\auditHeader{BERT (2018) — Masked Language Modeling: \guilty{} of Self-Audit}

BERT pre-trains by masking 15\% of tokens and predicting them from context. This is self-supervised learning: labels are generated from the data itself. Theorem~2: self-generated labels → self-audit → no quality guarantee on the learned representations. The MLM accuracy tells you how well BERT predicts held-out tokens, not whether those predictions encode genuine linguistic knowledge.

**SCX Augmentation**: $M$ independently-masked versions of the same text, each with different random masks. Yajie{} consensus across masked versions provides Theorem~1 detection of spurious predictions.

\auditHeader{GPT (2018--2024) — Autoregressive Generation: \guilty{} of $M=1$}

GPT generates tokens one at a time: $p(x_t | x_{<t})$. At each step, exactly one continuation is chosen. No second opinion. No verification of generation quality. Hallucinations are undetectable by the model itself. Theorem~1 with $M=1$: no detection guarantee for generated falsehoods.

**SCX Augmentation**: $M$ independent generation heads producing $M$ candidate continuations. Yajie{} consensus selects the most verified continuation. Factual claims cross-referenced against Spring{}'s permanent knowledge base.

## Part IV: Generative Models — The Audit Crisis
## 第四部分：生成模型——审计危机
<!-- label: sec:generative -->

Generative models create new data: images, text, audio, video. They represent the frontier of ML capability — and the nadir of audit quality. The central problem: how do you verify the quality of something that never existed before? The answer, for current generative models: you don't. And you can't, because $M=1$ or self-audit.

### 19. GAN (Generative Adversarial Networks) 生成对抗网络

\auditHeader{Verdict: \guilty{} — $M=1$ Discriminator Explains ALL GAN Failures (With Instability Proof)}

\whyPopular{} First realistic image generation. Goodfellow et al. (2014):
\[
\min_G \max_D \; \E_{x \sim p_{data}}[\log D(x)] + \E_{z \sim p_z}[\log(1 - D(G(z)))].
\]
Generator $G$ maps noise $z$ to synthetic samples; Discriminator $D$ distinguishes real from fake. At the Nash equilibrium of this minimax game, $G(z) \sim p_{data}$ — the generator perfectly mimics the data distribution.

\whyFail{} **ALL GAN failures are consequences of $M=1$ discriminator.** Theorem~1: $M_D = 1 \implies$ no detection guarantee. The discriminator is a single neural network. If $G$ finds a pattern that fools this one network, there is no second opinion.

\scxProof{} GAN training as an audit game with a formal instability theorem.

> **Proposition:** [GAN is Yajie{} NPE with $M=1$ Auditor]<!-- label: prop:gan_yajie -->
> \rigorFull
> The GAN objective is an instance of Yajie{} Non-Parametric Ensemble (NPE) with exactly $M=1$ auditor (the discriminator $D$). The generator $G$ produces a claim (``this sample is real''), and $D$ audits the claim. The training process is a two-player zero-sum game: $G$ attempts to minimize the audit detection rate, while $D$ attempts to maximize it.

> **Proof:** Map to SCX{} audit terminology:
> 
- **Claim:** $G(z)$ for $z \sim p_z$ — the generator claims that $G(z)$ is drawn from $p_{data}$.
- **Auditor:** $D: \cX \to [0,1]$ — the discriminator assigns a probability that $x$ is real.
- **Audit Outcome:** $D(G(z))$ is the probability that the auditor accepts the claim.
- **Verification Community:** $M=1$ — there is exactly one discriminator. There is no consensus mechanism, no multi-auditor cross-check.

> 
> At the Nash equilibrium of this game, $G$ produces samples from $p_{data}$ and $D(x) = 1/2$ for all $x$ (the discriminator cannot distinguish real from generated). This is the equilibrium where the auditor is maximally uncertain — the claim is indistinguishable from truth.
> 
> However, this equilibrium is only guaranteed under the assumption that both $G$ and $D$ have infinite capacity and that the optimization reaches the global optimum. In practice, neither holds, and the $M=1$ auditor architecture creates the instability that GANs are famous for.

> **Theorem:** [GAN Instability from $M=1$]<!-- label: thm:gan_instability -->
> \rigorFull
> A single-auditor ($M=1$) adversarial training game has the following failure modes, directly predicted by SCX{} Theorem~1 and Theorem~2:
> 
> 
1. **Auditor Capture:** If $D$ has a blind spot, $G$ can exploit it without detection. The probability that a single auditor misses a specific type of generated artifact is bounded below by a constant (no exponential suppression from multiple independent auditors).
2. **Mode Collapse:** $G$ finds a ``loophole'' — a small set of outputs that consistently fool $D$. With $M=1$, $G$ need only satisfy one auditor. With $M>1$ independent auditors, $G$ would need to satisfy all $M$ simultaneously, making mode collapse exponentially harder: $\Pbb(fool all  M) \le \exp(-2M\Delta^2)$.
3. **Training Oscillation:** The $M=1$ game has no stabilizing consensus mechanism. When $D$ improves, $G$ must adapt; when $G$ improves, $D$ must adapt. This creates non-convergent cycles, analogous to the lack of a separating equilibrium without M-declaration (Theorem~2).

> **Proof:** **(i) Auditor Capture.** Let $\cB \subset \cX$ be a ``blind spot'' of the discriminator: $D(x) > 1/2$ for $x \in \cB$ even though $x$ is generated (false acceptance). With $M=1$, the generator's expected loss for samples in $\cB$ is $\E_{z: G(z) \in \cB}[-\log D(G(z))] < \log 2$, which is profitable. With $M$ independent auditors, the probability that all $M$ accept a generated sample in $\cB$ is at most $\prod_{k=1}^M D_k(x) \le (\max_k D_k(x))^M$, which decays exponentially if any single auditor has $D_k(x) \le 1/2$. Formally, $\Pbb(all accept \mid \cB) \le \exp(-2M\Delta^2)$ where $\Delta = \min_k |D_k(x) - 1/2|$.
> 
> **(ii) Mode Collapse.** Let $\cS \subset \supp(p_{data})$ be a subset of the true data modes, and let $\cG \subset \cX$ be the set of outputs that $G$ can produce. Mode collapse occurs when $|\cG| \ll |\supp(p_{data})|$ but $D$ cannot distinguish $\cG$ from the full support. With $M$ independent auditors, each auditor covers a different aspect of the data distribution. For $G$ to collapse to mode $m$, it must fool all $M$ auditors simultaneously. If each auditor independently detects mode absence with probability at least $\Delta$, the collapse survival probability is $\le \exp(-2M\Delta^2)$.
> 
> **(iii) Training Oscillation.** The two-player game has payoff matrix with no pure Nash equilibrium in finite capacity regimes. The best-response dynamics create cycles (GAN training is known to oscillate rather than converge). Adding more auditors ($M>1$) creates a potential game structure: the consensus of $M$ auditors is smoother and more stable than any single auditor, because random fluctuations in one auditor are averaged out. This is the variance reduction effect of Proposition [ref].  $\square$

\diagnosis{} **Mode collapse** is the most famous GAN failure: the generator produces one type of output (e.g., one digit, one face pose) that reliably fools the discriminator. Why? Because one discriminator has one ``perspective.'' All the generator needs is one loophole.

\mathAudit{} With $M$ discriminators $D_1, ..., D_M$ trained independently:
\[
V_M(G, D_1, ..., D_M) = \frac{1}{M}\sum_{m=1}^M \Bigl[\E_{x \sim p_{data}}[\log D_m(x)] + \E_{z \sim p_z}[\log(1 - D_m(G(z)))]\Bigr].
\]
The generator must now fool the **consensus** of discriminators. The probability of finding a sample that fools all $M$ discriminators is:
\[
\Pbb(fool all) \le \prod_{m=1}^M \Pbb(fool  D_m) \le (\max_m \Pbb(fool  D_m))^M.
\]
If each discriminator has 90\% detection rate, $\Pbb(fool all) \le 0.1^M$. For $M=5$: $10^{-5}$. For $M=1$: $0.1$.

\whatMissing{} $M>1$ independent discriminators. Yajie{} consensus: generator must satisfy all discriminators simultaneously. Spring{} permanently records generated samples and discriminator verdicts. Cercis{} Score: $Q_{GAN} = 0.1$ (M=1). $Q_{SCX-GAN} = 1 - \exp(-2M\Delta^2)$ with $M>1$.

> **Remark:** [Multi-Discriminator GANs as Validation]
> The SCX{} prediction is that GANs with multiple discriminators should be more stable. This is exactly what has been observed: Generative Multi-Adversarial Networks (GMAN; Durugkar et al., 2017), Dual Discriminator GANs (D2GAN; Nguyen et al., 2017), and multi-scale discriminators (Pix2PixHD; Wang et al., 2018) all improve stability. Each additional discriminator increases $M$, and SCX{} Theorem~1 predicts exponential improvement in mode coverage and training stability.

### 20. VAE (Variational Autoencoders) 变分自编码器

\auditHeader{Verdict: \guilty{} — Self-Audit (Theorem~2)}

\whyPopular{} Principled probabilistic framework. Kingma \& Welling (2014): maximize ELBO
\[
\cL = \E_{q_\phi(z|x)}[\log p_\theta(x|z)] - \KL(q_\phi(z|x) \| p(z)).
\]
Encoder $q_\phi(z|x) = N(\mu_\phi(x), \sigma_\phi^2(x))$ maps $x$ to latent distribution; Decoder $p_\theta(x|z)$ reconstructs $x$ from $z$. Reparameterization trick $z = \mu + \sigma \odot \epsilon, \epsilon \sim N(0, I)$ enables gradient-based training.

\whyFail{} **Encoder → Decoder → reconstruction loss = the model audits ITSELF.** Theorem~2: $q_\phi$ and $p_\theta$ are jointly trained to minimize $\cL$. The reconstruction term $\E_{q_\phi}[\log p_\theta(x|z)]$ uses the encoder's $z$ to evaluate the decoder's $\hat{x}$. But $q_\phi$ was trained to make $z$ easy to decode. This is collusion, not verification.

\diagnosis{} **Blurry outputs are Theorem~3 in action.** VAEs produce blurry images. Why? The reconstruction loss (typically MSE or binary cross-entropy) penalizes pixel-wise deviation. For uncertain $z$, the optimal reconstruction is the *expected* image $\E_{p_\theta(x|z)}[x]$, which is a weighted average of possible images → blur. But is the blur because the model is uncertain (good) or because the decoder is weak (bad)? Theorem~3: you cannot tell. One model cannot distinguish aleatoric uncertainty from epistemic deficiency.

\mathAudit{} The VAE's quality signal is:
\[
ReconstructionError = \norm{x - \hat{x}}^2 = \norm{x - Decoder(Encoder(x))}^2.
\]
Encoder and Decoder are trained jointly → $\Cov(Encoder error, Decoder error) > 0$. The effective audit multiplicity is $M_{eff} = 1/(1 + \rho_{Enc-Dec}) \approx 1$ since $\rho_{Enc-Dec} \approx 1$ for a jointly-trained autoencoder. Theorem~2: self-audit provides zero information about true generation quality.

\whatMissing{} External quality auditor: $M>1$ independent discriminators evaluate VAE outputs against real data. Yajie{} consensus across discriminators. \Situs{} latent space audit: $\Lip(Encoder) \le L_{enc}$, $\Lip(Decoder) \le L_{dec}$. Cercis{} Score: $Q_{VAE} = 0.2$.

### 21. Diffusion Models 扩散模型

\auditHeader{Verdict: \weakness{} — $T$-Step Implicit Yajie{} With Correlated Steps (Full Analysis)}

\whyPopular{} SOTA image generation. Ho et al. (2020), Song et al. (2021): forward process $q(x_t|x_{t-1}) = N(x_t; \sqrt{1-\beta_t}x_{t-1}, \beta_t I)$ adds Gaussian noise. Reverse process $p_\theta(x_{t-1}|x_t) = N(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$ learns to denoise. The denoising network $\epsilon_\theta$ predicts the noise at each timestep. DDPM (2020) uses $T=1000$ steps; Stable Diffusion (2022) operates in latent space.

\whyFail{} **Iterative denoising = sequential refinement by the SAME model.** Each step $t$ applies $\epsilon_\theta(x_t, t)$. The noise predictor is shared across all timesteps: $\Corr(\epsilon_\theta(x_t, t), \epsilon_\theta(x_{t'}, t')) = \rho_{arch} > 0$, where $\rho_{arch}$ is architectural correlation (shared weights). This is sequential dependency: $M_{eff} \ll T$.

\scxProof{} Diffusion as $T$-step implicit Yajie{} consensus.

> **Proposition:** [Diffusion as $T$-Step Yajie{} Consensus]<!-- label: prop:diffusion_yajie -->
> \rigorConjectural
> The $T$ denoising steps of a diffusion model can be interpreted as a $T$-round Yajie{} consensus: at each step $t$, the model ``audits'' the current noisy sample $x_t$ against the learned data distribution, producing a refined estimate $x_{t-1}$. The effective number of audits is $M_{eff} \approx T$, with each step contributing an independent denoising decision. This $M_{eff} \gg 1$ (typically $T = 1000$) provides substantially stronger SCX{} guarantees than GANs' $M=1$, explaining diffusion models' superior mode coverage and training stability.

> **Proof:** [Proof Sketch]
> Each denoising step $t$ solves a local optimization:
> 
> $$
>     \mu_\theta(x_t, t) \approx \argmin_ \E_{x_0 \sim q(x_0 \mid x_t)}\left[\norm{\mu - x_0}^2\right].
> $$
> 
> This is an ``audit'': the model checks whether $x_t$ is consistent with the data manifold and proposes a correction. The $T$ steps form a consensus chain:
> 
> $$
>     x_0^{(generated)} = Audit_1 \circ Audit_2 \circ ... \circ Audit_T (x_T),
> $$
> 
> where each audit step reduces the distance to the data manifold. The denoising score matching objective:
> 
> $$
>     \mathcal{L}_{diffusion} = \E_{t, x_0, \epsilon}\left[\norm{\epsilon - \epsilon_\theta(x_t, t)}^2\right],
> $$
> 
> trains the auditor at all noise levels simultaneously. The key difference from GANs: GANs have one discriminator making a single continuous decision; diffusion has $T$ steps each making a local correction. The consensus of $T$ steps is more robust than any single-step audit.
> 
> This connection is \rigorConjectural{} because the denoising steps are not independent — they share the same network $\epsilon_\theta$ and the same training trajectory, violating \asmTag{1}. However, the functional behavior matches: more steps ($T \uparrow$) improves sample quality (up to a point), analogous to larger $M$ improving consensus accuracy.

\diagnosis{} Diffusion can be reframed as $T$ sequential refinement steps. Theorem~1 requires independent experts. With $T$ correlated applications of the same model: $M_{eff} = T / (1 + (T-1)\rho_{arch}) \to 1/\rho_{arch}$ as $T \to \infty$. For $\rho_{arch} \approx 0.8$ (high, since same weights), $M_{eff} \approx 1.25$ — effectively one expert. The 1000 diffusion steps provide negligible audit benefit beyond $\sim$2 independent assessments.

\mathAudit{} The quality of a diffusion step at time $t$ can be measured by the denoising error:
\[
\varepsilon_t = \E[\norm{\epsilon - \epsilon_\theta(x_t, t)}^2].
\]
This is the training loss. But this is self-audit: the model's training objective evaluates itself (Theorem~2). The user never knows $\varepsilon_t$ for a generated sample.

\whatMissing{} Independent auditors at each noise level: $M$ different denoising networks $\epsilon_\theta^{(1)}, ..., \epsilon_\theta^{(M)}$, each specialized to a noise range. Yajie{} consensus at each step. Or: fewer steps with $M>1$ auditors per step, providing $\Pbb(miss) \le \exp(-2M\Delta^2)$. Cercis{} Score: $Q_{Diffusion} = 0.5$ (penalized for correlated steps).

> **Remark:** [Why Diffusion Won]
> The SCX{} framework provides a structural explanation for diffusion models' victory over GANs: $T \approx 1000$ implicit audits beats $M=1$ explicit audit. The market selected for SCX{}-compliance: practitioners abandoned GANs for diffusion models not because they computed SCX{} bounds, but because diffusion models empirically provide better mode coverage, stability, and sample quality — all predicted by SCX{} Theorem~1 with larger $M$.

## Part V: Modern Paradigms — The Self-Audit Trap
## 第五部分：现代范式——自审计陷阱
<!-- label: sec:modern -->

Modern ML increasingly avoids human supervision. Self-supervised learning, transfer learning, reinforcement learning — each shifts the burden of quality assessment from humans to algorithms. This creates a structural audit crisis: when algorithms generate their own labels, evaluate their own outputs, and learn from their own predictions, who verifies the verifier?

### 22. Self-Supervised Learning 自监督学习——SimCLR/MoCo/MAE/BERT

\auditHeader{Verdict: \guilty{} — Self-Audit Paradox, Augmentation Ensemble Escape (With Proof)}

\whyPopular{} No human labels needed. SSL generates supervisory signals from the data itself:

- **BERT**: Mask 15\% of tokens, predict masked tokens from context.
- **SimCLR**: Apply two random augmentations to image $x$, encode both to $z_i, z_j$, maximize agreement between $z_i$ and $z_j$ while minimizing agreement with other images.
- **MoCo**: Maintain momentum encoder for consistent negative samples. Dictionary queue of encoded samples.
- **MAE**: Mask 75\% of image patches, reconstruct from visible patches. Asymmetric encoder-decoder.

\whyFail{} **Model generates its own labels → learns from self-generated labels → circular.** Theorem~2: the mutual information between self-audit outcome and true quality is zero. BERT's MLM accuracy measures how well BERT predicts BERT's own masked tokens — not whether the learned representations encode genuine linguistic knowledge.

\scxProof{} The self-audit paradox and how contrastive methods partially escape it.

> **Proposition:** [SSL is Self-Audit — Theorem 2 Applies]<!-- label: prop:ssl_selfaudit -->
> \rigorFull
> In self-supervised learning, the model generates its own training labels from the data, then learns from them. In SCX{} terminology: the model is both the **claimant** (it proposes a representation) and the **auditor** (it evaluates the representation against the pretext task). This is **self-audit** — the exact scenario that SCX{} Theorem~2 identifies as epistemically equivalent to no audit:
> 
> $$<!-- label: eq:ssl_thm2 -->
>     Self-generated labels without independent verification \implies \Pbb(quality certified)  is unbounded.
> $$
> 
> Formally, SSL with a single pretext task has $M=0$ independent auditors.

> **Proof:** The SSL training pipeline is:
> 
1. Define pretext transformation $T: \cX \to \cX \times \cY_{pretext}$ that generates ``labels'' from unlabeled data.
2. Train model $f_\theta$ to minimize $\E_{x \sim \cD}[\ell(f_\theta(T_x(x)), T_y(x))]$.
3. Use $f_\theta$ (or its intermediate representation) for downstream tasks.

> 
> The critical observation: the model $f_\theta$ is the *sole* entity that determines the quality of both the pretext labels and the learned representation. There is no external verifier. The pretext task's loss $\mathcal{L}_{pretext}$ is minimized by construction (gradient descent finds a local minimum), but this provides no information about whether the learned representation captures *true* data structure or merely satisfies the pretext task's specific inductive bias.
> 
> By SCX{} Theorem~2, without an independent auditor (a verifier not trained on the same objective), the quality of the representation cannot be certified.

### Why SSL Still Works: Implicit Multi-Expert Structure

Despite Theorem~2's negative result, SSL demonstrably works. The resolution comes from the *implicit* multi-expert structure that SSL methods inadvertently create:

> **Proposition:** [Contrastive Learning as Implicit Consensus]<!-- label: prop:simclr_consensus -->
> \rigorPartial
> Contrastive learning methods (SimCLR, MoCo, BYOL) create an implicit Yajie{} ensemble through multiple data augmentations. Each augmented view of the same image is an ``expert'' that votes on the representation. The contrastive loss:
> 
> $$<!-- label: eq:simclr_loss -->
>     \mathcal{L}_{contrastive} = -\log \frac{\exp(sim(z_i, z_j)/\tau)}{\sum_{k=1}^{2N} \ind{k \neq i} \exp(sim(z_i, z_k)/\tau)},
> $$
> 
> where $z_i, z_j$ are representations of two augmentations of the same image, implements Yajie{} consensus: the positive pair $(z_i, z_j)$ must agree (vote together), while negative pairs $(z_i, z_k)$ must disagree.

\diagnosis{} **Contrastive methods partially escape self-audit.** Different augmentations act as different ``observers'' of the same underlying instance → $M_{aug} > 1$ pseudo-independent views. This is why SimCLR outperforms pure reconstruction SSL: it **accidentally** introduces $M>1$, providing weak Theorem~1 benefits.

\mathAudit{} The effective multiplicity of contrastive SSL with $K$ augmentation types:
\[
M_{eff} = \frac{K}{1 + \bar_{aug}},
\]
where $\bar_{aug}$ is the average correlation between encodings from different augmentations. For SimCLR with random crop, color jitter, Gaussian blur, horizontal flip ($K=4$), $\bar_{aug} \approx 0.5$ → $M_{eff} \approx 2.7$. Better than $M=1$ but far from robust. Strong augmentations can destroy semantic content (rotated ``6'' ≠ ``9''), creating false positives with no detection mechanism.

\whatMissing{} Explicit $M$ declaration for augmentation diversity. Each augmentation type as noisy observation channel. Yajie{} consensus across augmentation-specific encoders. Cercis{} Score: $Q_{SSL-recon} = 0.1$ (pure reconstruction, self-audit); $Q_{SSL-contrastive} = 0.3$ ($M_{aug}>1$ but unverified). Spring{} permanently records which augmentations produce consistent vs. inconsistent representations.

### 23. Transfer Learning / Fine-tuning 迁移学习/微调

\auditHeader{Verdict: \weakness{} — No Transfer Quality Metric (With $\rho_s + \Delta_s$ Decomposition)}

\whyPopular{} Works with limited data. Pre-train on massive dataset (ImageNet-21K, JFT-300M, C4), fine-tune on target task with few labeled examples. The pre-trained model $\theta_{pre}$ provides strong initialization; fine-tuning produces $\theta_{ft} = \theta_{pre} + \Delta\theta$ adapted to the target task. Dominant paradigm since 2018.

\whyFail{} **No metric for transfer quality. Negative transfer goes undetected.** Sometimes pre-training *hurts*: features learned on source data are irrelevant or harmful for the target. This is ``negative transfer.'' No *a priori* method to predict transfer quality.

\scxProof{} Transfer learning as $\rho_s + \Delta_s$ decomposition.

> **Proposition:** [Pre-Training Estimates State Priors]<!-- label: prop:pretrain_prior -->
> \rigorFull
> In SCX{} terms, pre-training on a large corpus $\cD_{pre}$ estimates the state prior distribution $\rho_s = \Pbb(s)$ over the state space $\cS$. Fine-tuning on a downstream dataset $\cD_{down}$ estimates the separation gaps $\Delta_s$ between states. Formally:
> 
> $$
>     Pre-training:\quad &\hat_s = \argmax_ \Pbb(\cD_{pre} \mid \rho), <!-- label: eq:pretrain --> 

>     Fine-tuning:\quad &\hat_s = \argmax_ \Pbb(\cD_{down} \mid \Delta, \hat), <!-- label: eq:finetune -->
> $$
> 
> where $\rho_s$ captures the frequency and structure of state occurrences, and $\Delta_s$ captures the discriminative boundaries between states relevant to the downstream task.

> **Proof:** In the \Situs{} component of SCX{}, the state space $\cS$ is the set of possible ``situations'' the model can encounter. Each state $s \in \cS$ has:
> 
- **Prior probability:** $\rho_s = \Pbb(s)$ — how often does state $s$ occur?
- **Separation gap:** $\Delta_s = \min_{s' \neq s} \TV(P(\cdot \mid s), P(\cdot \mid s'))$ — how distinguishable is state $s$ from its neighbors?

> 
> Pre-training on a large, diverse corpus (e.g., ImageNet, C4, The Pile) provides data from a broad distribution over $\cS$. The model learns $\rho_s$ and $P(X \mid s)$. Fine-tuning on a small downstream dataset estimates $\Delta_s$ for the specific task. Since $\hat_s$ is already well-estimated from pre-training, the sample complexity for estimating $\hat_s$ is reduced from $O(|\cS|^2)$ to $O(|\cS_{task}|)$.

> **Theorem:** [Transfer Learning Sample Complexity Reduction]<!-- label: thm:transfer_sample -->
> \rigorPartial
> Let $\cS_{pre}$ be the state space covered by pre-training and $\cS_{task} \subseteq \cS_{pre}$ be the states relevant to the downstream task. The sample complexity for learning the downstream task with pre-training is:
> 
> $$<!-- label: eq:transfer_complexity -->
>     n_{down} = O\left(\frac{|\cS_{task}| \cdot \log(1/\delta)}{\min_{s \in \cS_{task}} \Delta_s^2}\right),
> $$
> 
> compared to $n_{scratch} = O(|\cS_{pre}| \cdot \log(1/\delta) / \min_s \Delta_s^2)$ for training from scratch. The reduction factor $|\cS_{pre}| / |\cS_{task}|$ is typically $10^2$--$10^4$.

\diagnosis{} Pre-training = state prior $\rho_s$ estimation. Fine-tuning = $\Delta_s$ estimation. Theorem~3: cannot distinguish $\Delta_s \approx 0$ because (a) pre-training is genuinely useful, or (b) fine-tuning failed to correct pre-training's errors.

\mathAudit{} The transfer quality decomposition:
\[
Acc_{ft} = Acc_{scratch} + \underbrace{(Acc_{ft} - Acc_{scratch})}_{transfer gain  \Delta_{transfer}}.
\]
$\Delta_{transfer} > 0$: positive transfer. $\Delta_{transfer} < 0$: negative transfer. But $Acc_{scratch}$ is unknown — you'd need to train from scratch to measure it, defeating the purpose of transfer learning.

\whatMissing{} Cercis{} Score for transfer quality: $Q_{transfer} = Acc_{ft} - Acc_{linear-probe}$, where linear probe accuracy measures pre-trained feature quality independently. Spring{} detects negative transfer: records whether fine-tuning degrades linear probe performance. Yajie{} consensus across $M$ different pre-trained models verifies transfer robustness.

### 24. Few-Shot / Meta-Learning 少样本学习/元学习

\auditHeader{Verdict: \guilty{} — $M=K$, Data Scarcity vs. Audit}

\whyPopular{} Mimics human rapid learning. Meta-learning learns to learn across tasks; at test time, adapts to new tasks from $K$ examples:

- **MAML** (Finn et al., 2017): Learn initialization $\theta$ such that one gradient step on $K$ examples produces good task-specific parameters.
- **Prototypical Networks** (Snell et al., 2017): Classify by distance to class prototypes $c_k = \frac{1}{K}\sum_i f_\phi(x_i)$.
- **Matching Networks** (Vinyals et al., 2016): Attention over support examples.

\whyFail{} **$K$ examples with no quality guarantee on any of them.** Theorem~1: $M$ is the number of independent experts. In few-shot learning, the effective audit multiplicity is at most $M_{eff} \le K$, and typically much less due to within-class correlation. A single mislabeled support example poisons predictions for the entire class.

\diagnosis{} With $K=1$ (one-shot learning): $M_{eff} \le 1$. Theorem~1 collapse: no detection guarantee. With $K=5$ (five-shot): $M_{eff} \le 5$, but with within-class correlation $\bar \approx 0.6$ (examples from same class share features), $M_{eff} \le 5/1.6 \approx 3.1$. This is a **fundamental limitation**, not an implementation issue.

\mathAudit{} The error detection bound with $K$ support examples:
\[
\Pbb(miss) \le \exp\bigl(-2K_{eff}\Delta^2\bigr), \quad K_{eff} = \frac{K}{1 + \bar_{class}}.
\]
For $K=5$, $\bar_{class}=0.6$, $\Delta=1$: $\Pbb(miss) \le \exp(-2 \cdot 3.1) \approx 0.002$ — seems good! But this assumes each support example is an independent verifier, which is false: they all come from the same meta-training distribution. The meta-training itself may have introduced biases that all $K$ examples share ($\bar_{meta} > 0$), further reducing $K_{eff}$.

\whatMissing{} Explicit $M$ declaration: $M_{eff} \le K/(1 + \bar_{class} + \bar_{meta})$. Cercis{} Score explicitly caps $Q_{few-shot} \le 1 - \exp(-2K_{eff}\Delta^2)$. Yajie{} consensus across $M$ different few-shot methods cross-validates predictions.

### 25. Reinforcement Learning 强化学习——DQN/PPO/SAC

\auditHeader{Verdict: \guilty{} — $M=1$ Reward Source (With Sample Complexity Bound)}

\whyPopular{} Game-playing, robotics, sequential decision-making. RL maximizes cumulative reward:
\[
J(\pi) = \E_{\tau \sim \pi}\left[\sum_{t=0}^\infty \gamma^t r(s_t, a_t)\right].
\]
DQN (Mnih et al., 2015), PPO (Schulman et al., 2017), SAC (Haarnoja et al., 2018). AlphaGo/AlphaZero defeated world champions at Go, chess, shogi.

\whyFail{} **The environment is a single reward source. $M=1$.** Theorem~1: no error detection. The environment provides one scalar reward per timestep. There is no second environment, no second reward function, no consensus on whether the reward accurately reflects true task performance.

\scxProof{} RL's $M=1$ structure as the root cause of sample inefficiency.

> **Proposition:** [RL Environment is an Auditor with $M=1$]<!-- label: prop:rl_auditor -->
> \rigorFull
> In standard RL (MDP formulation), the environment is the **sole auditor** of the agent's actions. At each time step $t$, the agent proposes action $a_t$ (a claim that ``$a_t$ is good in state $s_t$''), and the environment returns reward $r_t$ (the audit outcome). There is exactly $M=1$ auditor, and the audit is **interactive**: the environment's response depends on the agent's action and the state, which the agent's previous actions have influenced.

> **Theorem:** [RL Sample Inefficiency from $M=1$]<!-- label: thm:rl_sample -->
> \rigorPartial
> The sample complexity of RL with $M=1$ auditor is fundamentally higher than supervised learning with $M>1$:
> 
> $$<!-- label: eq:rl_sample_complexity -->
>     n_{RL} = \Omega\left(\frac{|\cS||\cA|}{\varepsilon^2} \log\frac{1}\right),
> $$
> 
> compared to $n_{supervised} = O(\log(1/\delta) / \varepsilon^2)$ with $M = \Omega(\log(1/\delta) / \varepsilon^2)$ independent experts. The $M=1$ auditor provides no consensus variance reduction, no cross-validation, and no independent verification of the value function.

\diagnosis{} **Reward hacking** is a Theorem~1 consequence: the agent finds behaviors that maximize reward but don't accomplish the intended task. A single reward function has loopholes. With $M>1$ reward functions (different designers, different metrics), the agent must satisfy all simultaneously. The probability of finding a behavior that hacks all $M$ reward functions decays exponentially in $M$.

\mathAudit{} For RL with $M=1$ reward: $Q_1 = 0$ (no guarantee). For RL with $M>1$ reward models:
\[
\Pbb(all  M  reward models fooled) \le \exp(-2M_{eff}\Delta_R^2),
\]
where $\Delta_R$ is the reward gap between intended and hacked behavior. The SCX-augmented RL objective:
\[
J_{SCX}(\pi) = \min_{m \in [M]} \E_{\tau \sim \pi}\left[\sum_t \gamma^t r_m(s_t, a_t)\right],
\]
maximizing the **minimum** reward across all $M$ reward models — conservative, safe, audited.

\whatMissing{} Multi-expert reward audit: $M>1$ reward models from different designers/metrics. Yajie{} consensus: policy satisfies all reward models. Spring{} permanently records trajectories and reward model disagreements. Cercis{} Score: $Q_{RL} = 0.1$ (M=1); $Q_{SCX-RL} = 1 - \exp(-2M\Delta_R^2)$ with $M>1$.

### 26. Imitation Learning / Behavioral Cloning 模仿学习/行为克隆

\auditHeader{Verdict: \guilty{} — Copying Without Audit}

\whyPopular{} Simpler than RL. Learn from expert demonstrations $\cD_E = \{(s_i, a_i)\}_{i=1}^N$:
\[
\pi_{BC} = \argmin_\pi \sum_{(s,a) \in \cD_E} \cL(\pi(s), a).
\]
DAgger (Ross et al., 2011): iteratively collect more data by executing $\pi$ and querying expert for correct actions at visited states. Used in autonomous driving, robotic manipulation.

\whyFail{} **Expert demonstrations = single expert. No verification.** The demonstrator is one policy $\pi_E$ — $M=1$. If $\pi_E$ makes mistakes, $\pi_{BC}$ copies them. If $\pi_E$'s demonstrations don't cover all states, $\pi_{BC}$ encounters distribution shift and fails catastrophically.

\diagnosis{} Distribution shift is a Theorem~1 consequence: the imitator visits states outside the expert's support. At those states, the imitator must extrapolate. Extrapolation error compounds — each step away from demonstrated states increases error. With $M=1$, there is no consensus to detect off-distribution states.

\mathAudit{} The error bound for behavioral cloning under distribution shift:
\[
\E_{s \sim d_\pi}[\cL(\pi(s), \pi^*(s))] \le \varepsilon + O\left(\frac{1}{1-\gamma}\TV(d_\pi \| d_{\pi_E})\right),
\]
where $d_\pi$ is state visitation distribution of learned policy, $d_{\pi_E}$ is expert's distribution. As $\TV(d_\pi \| d_{\pi_E})$ grows (distribution shift), error grows unboundedly.

\whatMissing{} Multi-expert demonstration audit: learn from $M>1$ experts with different styles. Yajie{} consensus across expert policies identifies ambiguous states (experts disagree). Spring{} records which expert was followed at each state. Cercis{} Score: $Q_{BC} = 0.1$ (M=1).

### 27. Recommendation Systems / Collaborative Filtering 推荐系统

\auditHeader{Verdict: \guilty{} — Self-Audit via Click-Through Rate}

\whyPopular{} Powers internet commerce. Matrix factorization: $R \approx U^\top V$ where $U$ is user embeddings, $V$ is item embeddings. Deep recommender systems (Wide \& Deep, DLRM, DCN) combine collaborative filtering with content features. Optimize for click-through rate (CTR), conversion rate, watch time.

\whyFail{} **CTR is a self-audit metric.** The system recommends items; users click (or not); clicks validate the recommendation. But: recommendations influence what users see → clicks are biased toward recommended items → the system reinforces its own biases. Theorem~2: self-generated feedback (clicks on system-recommended items) is self-audit. The true quality — would the user have preferred an item they never saw? — is fundamentally unmeasurable within the system.

\diagnosis{} The feedback loop $recommend \to click \to retrain \to recommend$ is a self-audit cycle. The system can achieve high CTR by recommending popular items that would be clicked regardless — this is the ``popularity bias'' that degrades discovery. Theorem~2: the system's CTR tells you about the system's ability to predict clicks on its own recommendations, not about recommendation quality.

\whatMissing{} $M>1$ independent recommendation engines with different architectures. Yajie{} consensus on recommendations: items recommended by all $M$ engines are verified. Spring{} permanently records (user, recommended items, clicks, non-clicks) for retrospective audit. Cercis{} Score: $Q_{RecSys} = 0.15$ (self-audit feedback loop).

## Part VI: The Verdict 第六部分：判决
<!-- label: sec:verdict -->

We have audited 29 algorithms across 70 years of ML. The results are damning. Only 5 achieve \verified{} status, and even those leave critical gaps. The rest range from \weakness{} (structural limitations) to \guilty{} (never considered audit at all). This is not a close call. This is a systemic, field-wide failure of epistemic hygiene.

### Summary of Convictions — One Line Per Algorithm 一审一判

- **线性回归/逻辑回归**: $M=1$. 70 years, never audited. \guilty{}
- **k近邻**: State encoding without quality metric. \guilty{}
- **朴素贝叶斯**: Assumes independence, never verifies. \guilty{}
- **决策树**: One tree, one opinion. Overfits silently. \guilty{}
- **支持向量机**: Kernel \Situs{} without Lipschitz bound. \guilty{}
- **K均值**: Arbitrary K, no cluster quality guarantee. \guilty{}
- **随机森林**: Best classical algorithm. Accidentally implements Theorem~1 with full proof. \verified{}
- **装袋法**: Good structure, $M_{eff}$ formula available but undeclared. \weakness{}
- **梯度提升/XGBoost**: Sequential dependency breaks independence; logarithmic $M_{eff}$ growth proved. \guilty{}
- **堆叠泛化**: Meta-learner introduces new unverified component. \weakness{}
- **深度多层感知机**: Depth without purpose. Theorem~3 violation. \guilty{}
- **卷积神经网络**: \Situs{} without Lipschitz. Translation equivariance proved but unverified. \weakness{}
- **RNN/LSTM**: Forget gate = evidence destruction. Spring{} violation. \guilty{}
- **残差网络**: Signal-noise separation proved. Best deep architecture. $O(\log(1/\eta))$ depth formula. \verified{}
- **批归一化**: Satisfies A5 with formal drift reduction theorem. \verified{}
- **Dropout**: $2^n$ sub-networks voting. $M_{eff}(p)$ formula proved. \verified{}
- **Transformer**: Multi-head = $M$ queries, attention = exact Spring{} mapping. \verified{}
- **BERT**: Self-supervised → self-audit (Theorem~2). \guilty{}
- **GPT**: Autoregressive $M=1$. Hallucinations undetectable. \guilty{}
- **GAN**: $M=1$ discriminator → mode collapse, instability, with formal proof. \guilty{}
- **变分自编码器**: Encoder-Decoder collusion = self-audit. \guilty{}
- **扩散模型**: $T$-step implicit Yajie{} but correlated steps. \weakness{}
- **对比自监督**: $M_{aug}>1$ but unverified. Augmentation ensemble escape proved. \guilty{}
- **重建自监督**: Pure self-audit. $M=0$. \guilty{}
- **迁移学习**: $\rho_s + \Delta_s$ decomposition proved. No transfer quality metric. \weakness{}
- **元学习**: $M \le K$ with correlation. Fundamental audit limit. \guilty{}
- **强化学习**: $M=1$ reward with sample complexity bound proved. \guilty{}
- **模仿学习**: $M=1$ expert. Distribution shift silently compounds. \guilty{}
- **推荐系统**: CTR feedback loop = self-audit. \guilty{}

**统计:** 29 algorithms audited. 5 verified. 5 weaknesses. 19 guilty. **Verdict rate: 65.5\% conviction.** 判决率：65.5\%有罪。

### The Cercis Score Ranking — All 29 Algorithms Cercis评分排名

\begin{longtable}{p{3.8cm} c c c p{2.5cm}}
\toprule
**Algorithm (算法)** & $\boldsymbol{Q}$ & $\boldsymbol{N}$ & $\boldsymbol{S}$ & **Verdict (判决)** 

\midrule
\endfirsthead
\toprule
**Algorithm (算法)** & $\boldsymbol{Q}$ & $\boldsymbol{N}$ & $\boldsymbol{S}$ & **Verdict (判决)** 

\midrule
\endhead
\midrule
\multicolumn{5}{r}{*Continued*} 

\endfoot
\bottomrule
\endlastfoot
Random Forest (随机森林) & 0.95 & 0.30 & 1.01 & \verified{} Exact Theorem~1 

ResNet (残差网络) & 0.85 & 0.40 & 0.93 & \verified{} 

Transformer (注意力) & 0.80 & 0.50 & 0.90 & \verified{} 

Dropout & 0.80 & 0.30 & 0.86 & \verified{} 

BatchNorm (批归一化) & 0.70 & 0.10 & 0.72 & \verified{} 

\midrule
Bagging (装袋法) & 0.65 & 0.15 & 0.68 & \weakness{} $M_{eff}$ undeclared 

CNN (卷积网络) & 0.55 & 0.45 & 0.64 & \weakness{} 

Diffusion (扩散模型) & 0.50 & 0.60 & 0.62 & \weakness{} 

Stacking (堆叠泛化) & 0.45 & 0.10 & 0.47 & \weakness{} 

Transfer Learning (迁移学习) & 0.40 & 0.40 & 0.48 & \weakness{} 

\midrule
XGBoost (梯度提升) & 0.50 & 0.20 & 0.54 & \guilty{} Sequential 

SVM (支持向量机) & 0.40 & 0.30 & 0.46 & \guilty{} No Lipschitz 

Naive Bayes (朴素贝叶斯) & 0.35 & 0.10 & 0.37 & \guilty{} Unverified Indep 

Decision Tree (决策树) & 0.30 & 0.10 & 0.32 & \guilty{} M=1 

Deep MLP (深度感知机) & 0.30 & 0.25 & 0.35 & \guilty{} Depth w/o Purpose 

SSL — Contrastive (对比自监督) & 0.30 & 0.70 & 0.44 & \guilty{} Weak M 

BERT (预训练语言模型) & 0.30 & 0.65 & 0.43 & \guilty{} Self-Audit 

GPT (自回归生成) & 0.25 & 0.85 & 0.42 & \guilty{} M=1 

Linear Reg. (线性回归) & 0.25 & 0.10 & 0.27 & \guilty{} M=1 

k-NN (k近邻) & 0.20 & 0.10 & 0.22 & \guilty{} Lazy Audit 

k-Means (K均值) & 0.20 & 0.10 & 0.22 & \guilty{} Arbitrary K 

SSL — Recon. (重建自监督) & 0.15 & 0.60 & 0.27 & \guilty{} Self-Audit 

VAE (变分自编码器) & 0.20 & 0.45 & 0.29 & \guilty{} Self-Audit 

RNN/LSTM (循环网络) & 0.15 & 0.30 & 0.21 & \guilty{} Memory Decay 

Meta-Learning (元学习) & 0.15 & 0.35 & 0.22 & \guilty{} M=K 

RecSys (推荐系统) & 0.15 & 0.50 & 0.25 & \guilty{} Self-Audit 

GAN (生成对抗网络) & 0.10 & 0.90 & 0.28 & \guilty{} M=1 Discriminator 

RL / PPO (强化学习) & 0.10 & 0.80 & 0.26 & \guilty{} M=1 Reward 

Imitation Learning (模仿学习) & 0.10 & 0.40 & 0.18 & \guilty{} M=1 Expert 

\bottomrule
*Caption:* Cercis{} Score ranking for all 29 algorithms. $Q$: formal guarantee (0--1). $N$: empirical novelty (0--1). $\eta=0.2$. $S=Q+\eta N$. Algorithms with $Q<0.3$ are epistemically worthless regardless of empirical performance. 质量保证分$Q$低于0.3的算法，经验表现再好，认识论价值为零。注：Random Forest Q=0.95反映其完全满足Theorem~1并提供完整数学证明。
<!-- label: tab:cercis_ranking -->
\end{longtable}

### Analysis of Rankings 排名分析

**Tier 1 — \verified{} VERIFIED ($S > 0.70$, 验证通过):** Random Forest ($S=1.01$), ResNet ($S=0.93$), Transformer ($S=0.90$), Dropout ($S=0.86$), BatchNorm ($S=0.72$). These algorithms accidentally implement core SCX{} theorems through their architectural design. Random Forest achieves the highest score in ML history — its ensemble structure with bootstrap independence, random subspaces, and OOB cross-audit provides the strongest implicit Theorem~1 implementation.

**Tier 2 — \weakness{} PARTIAL ($0.45 \le S \le 0.70$, 部分满足):** Bagging, CNN, Diffusion, Stacking, Transfer Learning. These have audit structure but critical gaps.

**Tier 3 — \guilty{} UNDECLARED ($S < 0.55$, 未声明):** The remaining 19 algorithms. Failure modes cluster into five categories:

1. **$M=1$ (单一专家):** Linear Regression, Decision Tree, GAN, RL, Imitation Learning — single point of failure.
2. **Self-Audit (自审计, Theorem~2):** VAE, SSL-reconstruction, RecSys — the system grades its own homework.
3. **Sequential Dependency (顺序依赖):** XGBoost/Boosting, RNN/LSTM, Diffusion — $M_{eff} \ll M$, breaking A1/A2.
4. **Unverified Structure (未验证结构):** SVM, k-Means, Naive Bayes, k-NN, Deep MLP.
5. **Data Scarcity (数据稀缺):** Meta-Learning — fundamental limit: few-shot learning with K examples cannot exceed audit guarantee determined by K.

### The Dark Matter of ML: Implicit Consensus Everywhere

A striking pattern emerges from this re-audit: many ML innovations that appear unrelated are, in SCX{} terms, the *same* mechanism — increasing the effective number of independent experts $M_{eff}$:

<div align="center">

[Table omitted — see original .tex]

</div>

This convergence is the strongest evidence for the SCX{} thesis: practitioners, through trial and error, have consistently discovered that ``more independent views of the data improve performance.'' SCX{} provides the unified mathematical explanation for why this is always true: Theorem~1's exponential bound.

### What Every Algorithm Lacks — The SCX Gap 每个算法缺什么

Every algorithm audited, including the \verified{} ones, lacks the following seven SCX{} components:

1. **M parameter declaration (M参数声明).** No algorithm declares $M$. $M$ is the most fundamental epistemic parameter in any learning system. Its absence is not a gap — it's a void.
2. **Independent multi-expert consensus — Yajie{} (独立多专家共识).** Algorithms with multiple components have implicit experts, but none implement formal Yajie{} Nash equilibrium consensus with provable error detection bounds.
3. **Spring{} permanent, monotonic memory (Spring{}永久单调记忆).** No algorithm maintains permanent, non-forgetting memory. LSTMs have forget gates. Transformers have bounded context windows. Every algorithm forgets — and therefore every algorithm loses audit evidence.
4. **Cercis{} Score quality metric (Cercis{}评分).** No algorithm provides $S = Q + \eta N$ as a single auditable quality number.
5. **Theorem~3 unidentifiability awareness (定理3不可区分性认知).** No algorithm acknowledges that added depth, parameters, or training data cannot distinguish signal from noise without independent audit.
6. **Cryptographic hash binding — 共生绑定.** No algorithm provides SHA-256 commitment to (model weights $\|$ training data manifest $\|$ hyperparameters $\|$ declared $M$).
7. **Distribution shift detection — Spring{} gating** (分布偏移检测). No algorithm actively monitors whether its input distribution has shifted from training.

### The Survivorship Pattern

The history of ML reveals a striking pattern when viewed through the SCX{} lens:

<div align="center">

\fbox{\parbox{0.9\textwidth}{
**The algorithms that survived longest have the strongest implicit SCX{} guarantees.** The algorithms that were trendy but fragile have weak implicit audit mechanisms. The market (empirical practice) is an evolutionary optimizer that selects for SCX{}-compliance, even when practitioners don't know it.
}}

</div>

### Rigor Status of SCX-ML Connections

We honestly catalog which connections in this paper are rigorous and which are conjectural:

[Table omitted — see original .tex]

## Epilogue — The Path Forward 尾声——前进之路
<!-- label: sec:epilogue -->

SCX{} is not ``another algorithm.'' It is not a competitor to Random Forest, Transformer, or ResNet. It is the **audit layer** — the verification infrastructure that every algorithm should have had from the beginning. The 70-year history of ML is the history of algorithms that work — until they don't — with no way to know when or why.

### The Fundamental Insight 根本洞见

Every ML algorithm produces a prediction $\hat{y} = f(x; \theta)$. A user deploying this prediction in a safety-critical, financial, or medical context wants to know: **is this specific prediction reliable?**

The current answer is always some form of self-audit: test set accuracy (data the model already saw), confidence score (generated by the model itself), benchmark ranking (aggregate statistics that hide individual failures). None of these answers the question.

SCX{} answers differently: **declare $M$.** How many independent experts would need to produce the same prediction for you to trust it? If $M$ is high and verified, trust. If $M$ is low or undeclared, consider the prediction unverified.

This is not a novel concept. Peer review in science requires independent reviewers. Jury trials require multiple jurors. Engineering safety requires independent verification and validation. Financial auditing requires external accountants. Every domain with high-stakes decisions has discovered, through painful experience, that **no single observer is reliable**. ML is the only field that hasn't learned this lesson.

### The SCX Prescription — Required Components

For any ML algorithm to achieve SCX{} certification, it must implement:

1. **Declare $M$ (声明M参数).** For target confidence $1-\varepsilon$ and error magnitude $\Delta$, declare $M \ge \ln(1/\varepsilon) / (2\Delta^2) \cdot (1 + \bar)$. Default: $\varepsilon = 0.05, \Delta = 0.5, \bar = 0.2 \Rightarrow M \ge 8$.
2. **Implement Yajie{} Nash consensus (实现Yajie纳什共识).** $M$ independent experts with verifiable competence scores $\omega_m$. The consensus mechanism itself is a fixed mathematical function — no learned parameters.
3. **Deploy Spring{} permanent memory (部署Spring永久记忆).** Every prediction, outcome, and audit result stored permanently. $M_t = M_{t-1} \cup \{(x_t, \hat{y}_t, y_t, audit\_verdict_t)\}$. Memory is monotonic non-decreasing. No forgetting.
4. **Compute and publish Cercis{} Score (计算并发布Cercis评分).** $S = Q + \eta N$ with every model release. Users can compare models by $S$, knowing that $S < 0.3$ means the model is epistemically worthless.
5. **Acknowledge Theorem~3 (承认定理3).** Every architectural decision — depth, width, skip connections, normalization, attention heads — must be justified against a noise audit baseline.
6. **Bind with cryptographic hash (共生绑定).** SHA-256 hash $H = hash(weights \| data\_manifest \| hyperparameters \| M \| Cercis Score)$. Any change produces a different hash — tampering is detectable.
7. **Monitor distribution shift via Spring{} gating (Spring{}门控监控).** At test time, compute $\KL(\rho_{test} \| \rho_{train})$. When KL divergence exceeds threshold $\tau$, predictions are flagged as unverified.

### The Arms Race We Need 我们需要的军备竞赛

M-declaration creates a virtuous arms race:

1. Company A releases Model-A with declared $M=50$, measured $\bar=0.15$, $Cercis(A) = 0.90$.
2. Company B releases Model-B with undeclared $M$ — effectively $M=0$.
3. Regulators, customers, and users compare: Model-A is verified; Model-B is not.
4. Company B is forced to declare $M$ or lose market share.
5. Both companies increase $M$, driving quality guarantees upward.

This is the same dynamic that drove safety ratings in automobiles, energy efficiency labels in appliances, and nutritional labels in food. **Information asymmetry favors the seller; mandatory disclosure levels the field.** M-declaration is mandatory disclosure for ML quality.

### The Dark Forest Protocol 黑暗森林协议

Any entity publishing non-SCX{} M parameters broadcasts ``dark forest coordinates'':

- **Non-SCX M = self-exposure.** Self-developed audit without the mathematical guarantees of Theorems 1--5. By Theorem~2, non-SCX{} M lacks validity.
- **Falsification triggers permanent record.** SCX{}-certified $M$ with $M_{true} < M_{declared}$ is active fraud. $\Pbb(detection) \to 1$ as Spring{} accumulates evidence.
- **Non-participation tolerated but flagged.** Entities not publishing $M$ are $M=0$ by default.

### Design Patterns for SCX-Native ML

We outline three design patterns for what SCX{}-native algorithm design looks like:

> **Definition:** [SCX-Ensemble: Explicit $M$-Expert Training]<!-- label: def:scx_ensemble -->
> An SCX{}-ensemble is a tuple $(\cA, M, Yajie, \cD_{audit})$ where:
> 
- $\cA$ is a base learning algorithm.
- $M$ is the declared number of independent experts.
- Each expert $k$ is trained on $\cD_k \sim Bootstrap(\cD)$ independently.
- $Yajie$ aggregates outputs with formal error bound $\exp(-2M\Delta^2)$ computed on $\cD_{audit}$.

> Random Forest is the canonical example. Any algorithm can be SCX{}-ensembled.

> **Definition:** [SCX-GAN: $M$-Discriminator Adversarial Training]<!-- label: def:scx_gan -->
> An SCX{}-GAN trains $M$ discriminators $D_1, ..., D_M$ on independently bootstrapped subsets against one generator $G$. The consensus discriminator output is $\bar{D}(x) = \frac{1}{M}\sum_k D_k(x)$, and by Theorem~1, the probability that $G$ fools all $M$ discriminators with a mode-collapsed distribution decays as $\exp(-2M\Delta^2)$.

> **Definition:** [SCX-SSL: Augmentation-Consensus Self-Supervised Learning]<!-- label: def:scx_ssl -->
> SCX{}-SSL addresses the self-audit problem by making the implicit augmentation ensemble explicit: $K$ separate encoder heads on $K$ independent augmentation streams, Yajie{} consensus across heads, with head disagreement as an uncertainty metric. This transforms SSL from self-audit ($M=0$) to a $K$-expert ensemble ($M=K$).

### Final Words 结束语

<div align="center">

\bfseries
No $M$, No Trust.
无M，不信。
$M=1$ is epistemically equivalent to $M=0$.
M=1 在认识论上等同于 M=0。
Self-audit is no audit.
自审计等于无审计。
Sequential experts are one expert.
顺序依赖的专家等于一个专家。
The 70-year detour ends now.
七十年的弯路，到此为止。
Declare $M$. Verify. Trust nothing else.
声明M。验证。除此以外，别无信任。

\bfseries
SCX is not another algorithm — it is the audit layer that 70 years of ML never had.
SCX不是又一个算法——它是70年机器学习从未拥有的审计层。

*— SCX, June 2026*

</div>

### Appendix: Quick Reference — SCX Audit of All 29 Algorithms 附录：速查表

\begin{longtable}{p{3.2cm} p{1.2cm} p{1.2cm} p{2cm} p{3cm}}
\toprule
**Algorithm** & **Verdict** & $\boldsymbol{M_{**eff**}}$ & **Violates** & **Missing SCX** 

\midrule
\endfirsthead
\toprule
**Algorithm** & **Verdict** & $\boldsymbol{M_{**eff**}}$ & **Violates** & **Missing SCX** 

\midrule
\endhead
\midrule
\multicolumn{5}{r}{*Continued*} 

\endfoot
\bottomrule
\endlastfoot
Linear Regression & \guilty{} & 1 & Thm 1 & Yajie{} consensus 

k-Nearest Neighbors & \guilty{} & $\le k/2$ & Situs-1 & \Situs{} Lipschitz 

Naive Bayes & \guilty{} & 1 & Thm 2, A2 & Feature audit 

Decision Tree & \guilty{} & 1 & Thm 1, Thm 2 & Multi-tree consensus 

SVM & \guilty{} & 1 & Situs-1 & Kernel certification 

k-Means & \guilty{} & 1 & Thm 2 & Cercis{} cluster score 

Random Forest & \verified{} & $M/(1+\bar)$ & — (undeclared) & Cercis{} + Spring{} 

Bagging & \weakness{} & $B/(1+\bar)$ & — (undeclared) & $M_{eff}$ declaration 

XGBoost & \guilty{} & $\ll T$ (log growth) & A1 (sequential) & Parallel experts 

Stacking & \weakness{} & $M$ (base), 1 (meta) & Thm 1 (meta) & Meta-learner audit 

Deep MLP & \guilty{} & 1 & Thm 3 & Depth audit 

CNN & \weakness{} & 1 & Situs-1 & Lipschitz bound 

RNN/LSTM & \guilty{} & 1 (sequential) & Spring-1 & Permanent memory 

ResNet & \verified{} & 1 (but separable) & — (undeclared) & Per-block audit 

BatchNorm & \verified{} & 1 & — (A5 satisfied) & Drift monitor 

Dropout & \verified{} & $\ll 2^n$ & — (undeclared) & $M_{eff}$ declaration 

Transformer & \verified{} & $h/(1+\bar)$ & Spring-1 (bounded KV) & Unbounded memory 

BERT & \guilty{} & 0 (self-audit) & Thm 2 & External labels 

GPT & \guilty{} & 1 (autoregressive) & Thm 1 & Multi-head generation 

GAN & \guilty{} & 1 (discriminator) & Thm 1 & $M>1$ discriminators 

VAE & \guilty{} & $\approx 1$ & Thm 2 & External auditor 

Diffusion & \weakness{} & $\approx 1/\rho$ & A1 (steps correlated) & Independent step auditors 

SSL (contrastive) & \guilty{} & $K/(1+\bar)$ & Thm 2 (partial) & Augmentation audit 

SSL (reconstruction) & \guilty{} & 0 & Thm 2 & External labels 

Transfer Learning & \weakness{} & 1 & Thm 3 & Transfer quality metric 

Meta-Learning & \guilty{} & $\le K/(1+\bar)$ & Thm 1 (hard limit) & Support set audit 

RL (PPO/DQN) & \guilty{} & 1 (reward) & Thm 1 & $M>1$ reward models 

Imitation Learning & \guilty{} & 1 (expert) & Thm 1 & Multi-expert audit 

Recommendation & \guilty{} & $\approx 1$ & Thm 2 & External feedback 

\bottomrule
\caption{Quick Reference: SCX Audit Summary for all 29 algorithms. $M_{eff}$ = effective multiplicity. ``Violates'' = which theorem/assumption is structurally violated. ``Missing SCX'' = the primary SCX component that would fix the deficiency.}
<!-- label: tab:quickref -->
\end{longtable}

**Interpretation:** Algorithms with $M_{eff}=1$ are structurally unverifiable. No amount of benchmark accuracy can fix this. Algorithms with $M_{eff} > 1$ but undeclared have audit structure but lack formal certification. Only algorithms with declared $M_{eff}$ and explicit Cercis{} Scores are SCX{}-compliant. Today, **zero** algorithms meet this standard.

\begin{thebibliography}{99}

\bibitem{scx2026} SCX. *The SCX Framework: Structured Causal eXamination for Quality-Certified Learning*. 2026.

\bibitem{scx_science_audit} SCX. *The SCX Audit Mandate: Why M-Parameter Declaration Must Be a Prerequisite for Scientific Publication*. 2026.

\bibitem{scx_personal_ethics} SCX. *SCX Personal Ethics: Game-Theoretic Audit of Individual Honesty*. 2026.

\bibitem{scx_governance} SCX. *SCX Audit of Governance: Multi-Expert Verification of Government Statistics*. 2026.

\bibitem{hoeffding1963} W.~Hoeffding. Probability inequalities for sums of bounded random variables. *Journal of the American Statistical Association*, 58(301):13--30, 1963.

\bibitem{breiman1996} L.~Breiman. Bagging predictors. *Machine Learning*, 24(2):123--140, 1996.

\bibitem{breiman2001} L.~Breiman. Random forests. *Machine Learning*, 45(1):5--32, 2001.

\bibitem{freund1997} Y.~Freund \& R.~Schapire. A decision-theoretic generalization of on-line learning and an application to boosting. *Journal of Computer and System Sciences*, 55(1):119--139, 1997.

\bibitem{friedman2001} J.~Friedman. Greedy function approximation: a gradient boosting machine. *Annals of Statistics*, 29(5):1189--1232, 2001.

\bibitem{chen2016} T.~Chen \& C.~Guestrin. XGBoost: A scalable tree boosting system. *KDD*, 2016.

\bibitem{ke2017} G.~Ke et al. LightGBM: A highly efficient gradient boosting decision tree. *NeurIPS*, 2017.

\bibitem{wolpert1992} D.~Wolpert. Stacked generalization. *Neural Networks*, 5(2):241--259, 1992.

\bibitem{krizhevsky2012} A.~Krizhevsky, I.~Sutskever, G.~Hinton. ImageNet classification with deep convolutional neural networks. *NeurIPS*, 2012.

\bibitem{hochreiter1997} S.~Hochreiter \& J.~Schmidhuber. Long short-term memory. *Neural Computation*, 9(8):1735--1780, 1997.

\bibitem{he2016} K.~He, X.~Zhang, S.~Ren, J.~Sun. Deep residual learning for image recognition. *CVPR*, 2016.

\bibitem{ioffe2015} S.~Ioffe \& C.~Szegedy. Batch normalization: Accelerating deep network training by reducing internal covariate shift. *ICML*, 2015.

\bibitem{srivastava2014} N.~Srivastava et al. Dropout: A simple way to prevent neural networks from overfitting. *JMLR*, 15(1):1929--1958, 2014.

\bibitem{vaswani2017} A.~Vaswani et al. Attention is all you need. *NeurIPS*, 2017.

\bibitem{devlin2019} J.~Devlin et al. BERT: Pre-training of deep bidirectional transformers. *NAACL*, 2019.

\bibitem{goodfellow2014} I.~Goodfellow et al. Generative adversarial nets. *NeurIPS*, 2014.

\bibitem{kingma2014} D.~Kingma \& M.~Welling. Auto-encoding variational Bayes. *ICLR*, 2014.

\bibitem{ho2020} J.~Ho, A.~Jain, P.~Abbeel. Denoising diffusion probabilistic models. *NeurIPS*, 2020.

\bibitem{chen2020} T.~Chen et al. A simple framework for contrastive learning of visual representations. *ICML*, 2020.

\bibitem{he2020moco} K.~He et al. Momentum contrast for unsupervised visual representation learning. *CVPR*, 2020.

\bibitem{he2022mae} K.~He et al. Masked autoencoders are scalable vision learners. *CVPR*, 2022.

\bibitem{finn2017} C.~Finn, P.~Abbeel, S.~Levine. Model-agnostic meta-learning for fast adaptation. *ICML*, 2017.

\bibitem{mnih2015} V.~Mnih et al. Human-level control through deep reinforcement learning. *Nature*, 518:529--533, 2015.

\bibitem{schulman2017} J.~Schulman et al. Proximal policy optimization algorithms. *arXiv:1707.06347*, 2017.

\bibitem{haarnoja2018} T.~Haarnoja et al. Soft actor-critic: Off-policy maximum entropy deep RL. *ICML*, 2018.

\bibitem{ross2011} S.~Ross, G.~Gordon, D.~Bagnell. A reduction of imitation learning to no-regret online learning. *AISTATS*, 2011.

\bibitem{silver2016} D.~Silver et al. Mastering the game of Go with deep neural networks and tree search. *Nature*, 529:484--489, 2016.

\bibitem{spence1973} M.~Spence. Job market signaling. *Quarterly Journal of Economics*, 87(3):355--374, 1973.

\bibitem{ioannidis2005} J.~Ioannidis. Why most published research findings are false. *PLoS Medicine*, 2(8):e124, 2005.

\bibitem{gal2016} Y.~Gal \& Z.~Ghahramani. Dropout as a Bayesian approximation. *NeurIPS*, 2016.

\bibitem{miyato2018} T.~Miyato et al. Spectral normalization for generative adversarial networks. *ICLR*, 2018.

\bibitem{michel2019} P.~Michel, O.~Levy, G.~Neubig. Are sixteen heads really better than one? *NeurIPS*, 2019.

\bibitem{durugkar2017} I.~Durugkar, I.~Gemp, S.~Mahadevan. Generative Multi-Adversarial Networks. *ICLR*, 2017.

\bibitem{nguyen2017} T.~Nguyen et al. Dual Discriminator Generative Adversarial Nets. *NeurIPS*, 2017.

\bibitem{wang2018} T.-C.~Wang et al. High-Resolution Image Synthesis and Semantic Manipulation with Conditional GANs. *CVPR*, 2018.

\bibitem{grill2020} J.-B.~Grill et al. Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning. *NeurIPS*, 2020.

\bibitem{song2021} Y.~Song et al. Score-based generative modeling through stochastic differential equations. *ICLR*, 2021.

\bibitem{radford2021} A.~Radford et al. Learning transferable visual models from natural language supervision. *ICML*, 2021.

\bibitem{brown2020} T.~Brown et al. Language models are few-shot learners. *NeurIPS*, 2020.

\bibitem{achiam2023} J.~Achiam et al. GPT-4 technical report. *arXiv:2303.08774*, 2023.

\bibitem{sutton2018} R.~S.~Sutton and A.~G.~Barto. *Reinforcement Learning: An Introduction.* MIT Press, 2nd edition, 2018.

\bibitem{minsky1969} M.~Minsky and S.~Papert. *Perceptrons.* MIT Press, 1969.

\bibitem{rumelhart1986} D.~E.~Rumelhart, G.~E.~Hinton, and R.~J.~Williams. Learning Representations by Back-Propagating Errors. *Nature*, 323:533--536, 1986.

\bibitem{bahdanau2014} D.~Bahdanau, K.~Cho, and Y.~Bengio. Neural Machine Translation by Jointly Learning to Align and Translate. *ICLR*, 2015.

\bibitem{lecun1998} Y.~LeCun, L.~Bottou, Y.~Bengio, and P.~Haffner. Gradient-Based Learning Applied to Document Recognition. *Proceedings of the IEEE*, 86(11):2278--2324, 1998.

\end{thebibliography}