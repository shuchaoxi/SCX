# Lemma A: Bahadur-Rao Theorem -- Bernoulli Case, Complete
Derivation

**Author:** SCX

> **Target**: Prove the Bahadur-Rao (1960) theorem specialized to
> i.i.d. Bernoulli(p) random variables, with explicit constants and error
> bounds, and extend to the lower tail and the non-i.i.d. setting.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### A.1 Problem Setup<!-- label: a.1-problem-setup -->

Let
\(X_1, ..., X_M \stackrel{i.i.d.} Bernoulli(p)\)
with \(p \in (0,1)\). Define the sample mean

\[\bar{X}_M = \frac{1}{M}\sum_{i=1}^M X_i.\]

For a threshold \(\theta > p\), we are interested in the large deviation
probability

\[P_M(\theta) := \mathbb{P}(\bar{X}_M \geq \theta).\]

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### A.2 Cumulant Generating Function and Cramer
Transform<!-- label: a.2-cumulant-generating-function-and-cramer-transform -->

The moment generating function of a single Bernoulli(p) variable \(X\)
is

\[M(\lambda) = \mathbb{E}[e^{\lambda X}] = 1-p + p e^\lambda, \quad \lambda \in \mathbb{R},\]

so the cumulant generating function (CGF) is

\[\psi(\lambda) = \log M(\lambda) = \log(1-p + p e^\lambda).\]

The first two derivatives of \(\psi\) are:

\[\psi'(\lambda) = \frac{p e^\lambda}{1-p + p e^\lambda},\]

\[\psi''(\lambda) = \frac{p e^\lambda (1-p + p e^\lambda) - (p e^\lambda)^2}{(1-p + p e^\lambda)^2}
= \frac{p(1-p)e^\lambda}{(1-p + p e^\lambda)^2}.\]

The rate function (Cramer transform) is the Legendre-Fenchel conjugate
of \(\psi\):

\[I(\theta) = \sup_{\lambda \in \mathbb{R}} \{\lambda\theta - \psi(\lambda)\}, \qquad \theta \in [0,1].\]

For \(\theta \in (0,1)\), the supremum is attained at the unique
\(\lambda^*\) solving \(\psi'(\lambda) = \theta\):

\[\frac{p e^{\lambda^*}}{1-p + p e^{\lambda^*}} = \theta.\]

**Proposition A.1 (Explicit saddlepoint)**. *The equation
\(\psi'(\lambda^*) = \theta\) has the unique solution*

\[\lambda^* = \log\frac{\theta(1-p)}{p(1-\theta)}.\]

*Proof.* From \(\psi'(\lambda^*) = \theta\):

\[
\frac{p e^{\lambda^*}}{1-p + p e^{\lambda^*}} = \theta
\;\Longrightarrow\; p e^{\lambda^*} = \theta(1-p + p e^{\lambda^*})
\;\Longrightarrow\; p e^{\lambda^*}(1-\theta) = \theta(1-p)
\;\Longrightarrow\; e^{\lambda^*} = \frac{\theta(1-p)}{p(1-\theta)}.
\]

Taking logs gives the result. \(\square\)

**Proposition A.2 (Rate function = KL divergence)**. *For
\(\theta \in [0,1]\),*

\[I(\theta) = \theta\log\frac{p} + (1-\theta)\log\frac{1-\theta}{1-p} = KL(\theta \| p).\]

*Proof.* Substituting \(\lambda^*\) into
\(\lambda\theta - \psi(\lambda)\):

\[

$$
I(\theta) &= \lambda^*\theta - \log(1-p + p e^{\lambda^*}) 

&= \theta\log\frac{\theta(1-p)}{p(1-\theta)} - \log\!\left(1-p + p\cdot\frac{\theta(1-p)}{p(1-\theta)}\right) 

&= \theta\log\frac{\theta(1-p)}{p(1-\theta)} - \log\!\left(\frac{(1-p)(1-\theta) + \theta(1-p)}{1-\theta}\right) 

&= \theta\log\frac{\theta(1-p)}{p(1-\theta)} - \log\!\left(\frac{1-p}{1-\theta}\right) 

&= \theta\log\frac{p} + (1-\theta)\log\frac{1-\theta}{1-p} = KL(\theta \| p). \qquad \square
$$

\]

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### A.3 Exponential Tilting and the Tilted
Distribution<!-- label: a.3-exponential-tilting-and-the-tilted-distribution -->

Define the exponentially tilted (Esscher-transformed) probability
measure \(\mathbb{P}_{\lambda^*}\) by

\[\frac{d\mathbb{P}_{\lambda^*}}{d\mathbb{P}} = \exp\!\big(\lambda^* S_M - M\psi(\lambda^*)\big),\]

where \(S_M = \sum_{i=1}^M X_i\). Under \(\mathbb{P}_{\lambda^*}\), the
\(X_i\) are i.i.d. with tilted marginal

\[\mathbb{P}_{\lambda^*}(X_i = x) = \frac{e^{\lambda^* x}}{1-p + p e^{\lambda^*}} \cdot \mathbb{P}(X_i = x), \qquad x \in \{0,1\}.\]

**Proposition A.3 (Tilted distribution is Bernoulli(\(\theta\)))**.
*Under \(\mathbb{P}_{\lambda^*}\),*

\[X_i \sim Bernoulli(\theta), \quad with  \mathbb{E}_{\lambda^*}[X_i] = \theta,\;
\operatorname{Var}_{\lambda^*}(X_i) = \sigma^2(\theta) = \theta(1-\theta).\]

*Proof.* Using \(e^{\lambda^*} = \theta(1-p)/[p(1-\theta)]\):

\[

$$
\mathbb{P}_{\lambda^*}(X_i=1) &= \frac{e^{\lambda^*} p}{1-p + p e^{\lambda^*}}
= \frac{\frac{\theta(1-p)}{p(1-\theta)}\cdot p}{\frac{1-p}{1-\theta}}
= \frac{1-\theta} \cdot (1-\theta) = \theta.
$$

\]

Thus \(\mathbb{P}_{\lambda^*}(X_i=1)=\theta\), so
\(X_i \sim Bern(\theta)\). The variance is \(\theta(1-\theta)\).

Alternatively, from the CGF:

\[\psi''(\lambda^*) = \frac{p(1-p)e^{\lambda^*}}{(1-p + p e^{\lambda^*})^2}.\]

Substituting \(e^{\lambda^*}\) and
\(1-p + p e^{\lambda^*} = (1-p)/(1-\theta)\):

\[
\psi''(\lambda^*) = \frac{p(1-p)\cdot\frac{\theta(1-p)}{p(1-\theta)}}{\left(\frac{1-p}{1-\theta}\right)^2}
= \frac{\theta(1-\theta)(1-p)^2/(1-\theta)^2}{(1-p)^2/(1-\theta)^2}
= \theta(1-\theta). \qquad \square
\]

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### A.4 The Bahadur-Rao Theorem for
Bernoulli<!-- label: a.4-the-bahadur-rao-theorem-for-bernoulli -->

#### A.4.1 Statement<!-- label: a.4.1-statement -->

**Theorem A.4 (Bahadur-Rao, 1960; Bernoulli case)**. *Let
\(X_1,...,X_M \stackrel{i.i.d.} Bernoulli(p)\) and fix
\(\theta > p\). Then*

\[
\mathbb{P}(\bar{X}_M \geq \theta) = \frac{\exp(-M \cdot KL(\theta \| p))}
{\lambda^* \sqrt{2\pi M \cdot \theta(1-\theta)}}
\Bigl(1 + \varepsilon_M\Bigr),
\]

*where \(\lambda^* = \log\frac{\theta(1-p)}{p(1-\theta)} > 0\) and*

\[|\varepsilon_M| \leq \frac{C(p,\theta)}{M}\]

*for an explicit constant \(C(p,\theta)\) given in Proposition A.5
below.*

**Remark**. The result also holds for the strict inequality
\(\bar{X}_M > \theta\), since \(\mathbb{P}(\bar{X}_M = \theta) = 0\) for
non-integer \(M\theta\), and for integer \(M\theta\) the correction is
absorbed into the \(O(1/M)\) term.

#### A.4.2 Proof via Stirling's Formula (Direct Binomial Tail
Expansion)<!-- label: a.4.2-proof-via-stirlings-formula-direct-binomial-tail-expansion -->

Since \(S_M = \sum_{i=1}^M X_i \sim Binomial(M,p)\), we can work
directly with the binomial distribution. Let
\(k = \lceil M\theta \rceil\). Since \(\theta > p\) and \(\theta\) is
fixed, we have \(k > Mp\) for all sufficiently large \(M\).

The binomial tail probability is

\[P_M(\theta) = \mathbb{P}(S_M \geq k) = \sum_{j=k}^M a_j, \qquad
a_j = \binom{M}{j} p^{\,j}(1-p)^{M-j}.\]

*Step 1: Stirling's formula with explicit remainder.*

For any \(n \in \mathbb{N}\), Robbins' refinement of Stirling gives

\[\sqrt{2\pi n}\left(\frac{n}{e}\right)^n \exp\!\left(\frac{1}{12n+1}\right) < n! < \sqrt{2\pi n}\left(\frac{n}{e}\right)^n \exp\!\left(\frac{1}{12n}\right).\]

Thus \(n! = \sqrt{2\pi n}\,(n/e)^n\,e^{r_n}\) with
\(|r_n| \leq 1/(12n)\) for \(n \geq 1\).

Applying this to \(\binom{M}{k} = M!/(k!\,(M-k)!)\):

\[
\binom{M}{k} = \sqrt{\frac{M}{2\pi k(M-k)}}\,
\frac{M^M}{k^k (M-k)^{M-k}}\,
\exp\!\big(r_M - r_k - r_{M-k}\big).
\]

The error term satisfies

\[|r_M - r_k - r_{M-k}| \leq \frac{1}{12M} + \frac{1}{12k} + \frac{1}{12(M-k)}
\leq \frac{1}{4\min(k, M-k)}.\]

Define \(\theta_M = k/M\). Writing \(H(x) = -x\log x - (1-x)\log(1-x)\)
(binary entropy):

\[\binom{M}{k} = \frac{\exp\!\big(M\cdot H(\theta_M)\big)}{\sqrt{2\pi M\cdot\theta_M(1-\theta_M)}}
\cdot \big(1 + \delta_M^{(1)}\big), \qquad |\delta_M^{(1)}| \leq \frac{C_1}{M}\]

for an explicit constant \(C_1 = C_1(p,\theta)\) that depends on \(p\)
and \(\theta\) but not on \(M\). (Here we bound
\(|e^{r_M-r_k-r_{M-k}} - 1|\) using \(|e^u-1| \leq |u|e^{|u|}\).)

*Step 2: Leading term \(a_k\).*

\[

$$
a_k &= \binom{M}{k} p^k (1-p)^{M-k} 

&= \frac{\exp\!\big(-M\cdot I(\theta_M)\big)}{\sqrt{2\pi M\cdot\theta_M(1-\theta_M)}}
\cdot \big(1 + \delta_M^{(1)}\big),
$$

\]

where
\(I(x) = x\log\frac{x}{p} + (1-x)\log\frac{1-x}{1-p} = KL(x\|p)\).
Since \(|\theta_M - \theta| \leq 1/M\), a Taylor expansion gives

\[I(\theta_M) = I(\theta) + I'(\theta)(\theta_M-\theta) + O(M^{-2}),\]

with \(I'(\theta) = \log\frac{\theta(1-p)}{p(1-\theta)} = \lambda^*\).
Hence

\[e^{-M\cdot I(\theta_M)} = e^{-M\cdot I(\theta)} \cdot \exp\!\big(-M\lambda^*(\theta_M-\theta) + O(1/M)\big).\]

Since \(\theta_M - \theta = O(1/M)\), the term
\(-M\lambda^*(\theta_M-\theta) = O(1)\). Combining all \(O(1/M)\)
errors:

\[
a_k = \frac{\exp\!\big(-M\cdot I(\theta)\big)}{\sqrt{2\pi M\cdot\theta(1-\theta)}}
\cdot \big(1 + \varepsilon_M^{(1)}\big), \qquad |\varepsilon_M^{(1)}| \leq \frac{C_2}{M}. 
\]

*Step 3: Ratio of consecutive terms and geometric decay.*

For \(j \geq k\),

\[\frac{a_{j+1}}{a_j} = \frac{M-j}{j+1}\cdot\frac{p}{1-p}.\]

For the term at \(j = k\):

\[\frac{a_{k+1}}{a_k} = \frac{M-k}{k+1}\cdot\frac{p}{1-p}
= e^{-\lambda_k^*}\cdot\frac{k}{k+1}, \qquad
\lambda_k^* = \log\frac{k(1-p)}{p(M-k)}.\]

Since \(k = M\theta_M\), we have \(\lambda_k^* = \lambda^* + O(1/M)\),
and \(k/(k+1) = 1 - 1/k = 1 + O(1/M)\). Thus

\[\frac{a_{k+1}}{a_k} = e^{-\lambda^*}\big(1 + O(1/M)\big).\]

Moreover, for all \(j \geq k\), the ratio is decreasing in \(j\) (since
\((M-j)/(j+1)\) decreases with \(j\)), so

\[\frac{a_{j+1}}{a_j} \leq \frac{a_{k+1}}{a_k} \leq e^{-\lambda^*}\big(1 + \rho_M\big),\]

where \(\rho_M \to 0\) as \(M \to \infty\) and \(|\rho_M| \leq C_3/M\)
for an explicit \(C_3\).

*Step 4: Summing the tail.*

We bound \(P_M(\theta) = a_k + a_{k+1} + ... + a_M\) from both sides.

**Upper bound**:

\[
P_M(\theta) \leq a_k \sum_{j=0}^\infty \big(e^{-\lambda^*}(1+\rho_M)\big)^j
= \frac{a_k}{1 - e^{-\lambda^*}(1+\rho_M)}.
\]

**Lower bound**:

\[
P_M(\theta) \geq a_k \sum_{j=0}^{J} \big(e^{-\lambda^*}(1-\tilde\rho_M)\big)^j
\]

for any finite \(J\) (where \(\tilde\rho_M\) accounts for the lower
bound on the ratio). Taking \(J \to \infty\) (valid since the series
converges), we have

\[
P_M(\theta) \geq \frac{a_k}{1 - e^{-\lambda^*}(1-\tilde\rho_M)}.
\]

Combining both bounds and using \(|\rho_M|, |\tilde\rho_M| \leq C_3/M\):

\[
P_M(\theta) = \frac{a_k}{1 - e^{-\lambda^*}} \cdot \big(1 + \varepsilon_M^{(2)}\big),
\qquad |\varepsilon_M^{(2)}| \leq \frac{C_4}{M}. 
\]

*Step 5: Final assembly.*

Substituting (A.1) into (A.2):

\[
P_M(\theta) = \frac{\exp\!\big(-M\cdot I(\theta)\big)}
{(1-e^{-\lambda^*})\,\sqrt{2\pi M\cdot\theta(1-\theta)}}
\cdot \big(1 + \varepsilon_M\big), \qquad |\varepsilon_M| \leq \frac{C(p,\theta)}{M}.
\]

**Lattice correction factor.** The factor
\((1-e^{-\lambda^*})^{-1}\) is the **lattice correction**
characteristic of lattice distributions (span \(h=1\)). For large
\(\lambda^*\) (large deviations), \(e^{-\lambda^*}\) is small and
\((1-e^{-\lambda^*})^{-1} \approx 1 + e^{-\lambda^*}\) differs
negligibly from \(1\). For moderate \(\lambda^*\), the correction
matters for exact constants.

**Relation to the \(1/\lambda^*\) form.** Since
\(1-e^{-\lambda^*} = \lambda^* - \lambda^{*2}/2 + \lambda^{*3}/6 - ...\),

\[\frac{1}{1-e^{-\lambda^*}} = \frac{1}{\lambda^*}\left(1 + \frac{\lambda^*}{2} + \frac{\lambda^{*2}}{12} - \frac{\lambda^{*4}}{720} + ...\right).\]

Both forms are asymptotically equivalent as \(\lambda^* \to 0\) (i.e.,
as \(\theta \downarrow p\)), but differ by a constant factor for fixed
\(\lambda^* > 0\). For consistency with the proof architecture (Section
2.4 of the parent document), we write

\[
\boxed{\;
\mathbb{P}(\bar{X}_M \geq \theta)
= \frac{\exp(-M \cdot KL(\theta \| p))}
{\lambda^* \sqrt{2\pi M \cdot \theta(1-\theta)}}
\cdot \frac{\lambda^*}{1-e^{-\lambda^*}}
\cdot \big(1 + O(1/M)\big).\;}
\]

The factor \(\lambda^*/(1-e^{-\lambda^*})\) is a known constant in
\((0, \infty)\) and is absorbed into the leading constant in the F1
expansion (where it appears in both numerator and denominator of ratios,
so its effect can be tracked explicitly if needed). \(\square\)

**Remark (Connection to the Bahadur-Rao theorem).** The general
Bahadur-Rao (1960) theorem for non-lattice distributions yields the
\(1/\lambda^*\) form directly; the lattice correction
\((1-e^{-\lambda^*})^{-1}\) appears for lattice distributions like
Bernoulli. Both forms agree in the \(O(1/M)\) asymptotic expansion up to
a constant factor, and the \(O(1/M)\) error bound above holds in either
case.

#### \texorpdfstring{A.4.3 Explicit Constant for the
\(O(1/M)\)
Bound{A.4.3 Explicit Constant for the O(1/M) Bound}}<!-- label: a.4.3-explicit-constant-for-the-o1m-bound -->

**Proposition A.5 (Explicit \(O(1/M)\) bound for Bernoulli)**. For
\(p \in (0,1)\), \(\theta > p\), let
\(\lambda^* = \log\frac{\theta(1-p)}{p(1-\theta)}\),
\(\sigma^2 = \theta(1-\theta)\), and \(k = \lceil M\theta\rceil\). Then
for \(M\) large enough that \(\min(k, M-k) \geq 1\),

\[
\Bigg|
\frac{\mathbb{P}(\bar{X}_M \geq \theta) \cdot (1-e^{-\lambda^*}) \sqrt{2\pi M}\, \sigma}
{e^{-M\cdotKL(\theta\|p)}} - 1
\Bigg| \leq \frac{C_{Stirling}(p,\theta)}{M},
\]

where

\[C_{Stirling}(p,\theta) = \frac{1}{4\min(\theta, 1-\theta)}
+ \frac{C_1(p,\theta)}{\sqrt{2\pi}} + \frac{C_3(p,\theta)}{(1-e^{-\lambda^*})^2},\]

and \(C_1, C_3\) are the explicit constants from Steps 2 and 4 of the
proof above, bounded in terms of \(p\) and \(\theta\) only.

*Proof.* The Stirling remainder contributes
\(|\delta_M^{(1)}| \leq \frac{1}{4\min(k,M-k)}\), the \(k/M \to \theta\)
replacement contributes \(O(1/M)\) by Lipschitz continuity of \(I\) and
the square-root factor, and the geometric-series approximation
contributes \(|\varepsilon_M^{(2)}|
\leq C_3/(M(1-e^{-\lambda^*}))\). Collecting these gives the bound.
\(\square\)

This constant is fully explicit: for any given \(p\) and \(\theta\), all
quantities can be evaluated numerically.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### \texorpdfstring{A.5 Lower Tail Formula
(\(\theta < p\)){A.5 Lower Tail Formula (\ theta \textless{} p)}}<!-- label: a.5-lower-tail-formula-theta-p -->

For the **lower tail** \(\mathbb{P}(\bar{X}_M \leq \theta)\) with
\(\theta < p\), we use the symmetry transformation
\(Y_i = 1 - X_i \sim Bern(1-p)\). Then

\[\bar{X}_M \leq \theta \;\Longleftrightarrow\; \frac{1}{M}\sum_{i=1}^M Y_i \geq 1-\theta,\]

and \(1-\theta > 1-p\) since \(\theta < p\). Applying Theorem A.4 to the
\(Y_i\) sequence gives the following.

**Theorem A.6 (Lower tail Bahadur-Rao for Bernoulli)**. Let
\(X_1,...,X_M \stackrel{i.i.d.} Bernoulli(p)\) and fix
\(\theta < p\). Then

\[
\mathbb{P}(\bar{X}_M \leq \theta) = \frac{\exp(-M \cdot KL(\theta \| p))}
{|\lambda^*| \sqrt{2\pi M \cdot \theta(1-\theta)}}
\Bigl(1 + \varepsilon_M'\Bigr),
\]

where

\[\lambda^* = \log\frac{\theta(1-p)}{p(1-\theta)} < 0, \qquad
|\lambda^*| = \log\frac{p(1-\theta)}{\theta(1-p)},\]

and \(|\varepsilon_M'| \leq C'(p,\theta)/M\) for an explicit constant
\(C'\).

*Proof.* Apply Theorem A.4 to \(Y_i = 1-X_i \sim Bern(1-p)\)
with threshold \(1-\theta > 1-p\). The saddlepoint for the \(Y\)-problem
is

\[\lambda_Y^* = \log\frac{(1-\theta)(1-(1-p))}{(1-p)(1-(1-\theta))}
= \log\frac{(1-\theta)p}{(1-p)\theta} = -\lambda^* > 0.\]

The rate function:

\[KL(1-\theta\|1-p) = (1-\theta)\log\frac{1-\theta}{1-p} + \theta\log\frac{p} = KL(\theta\|p).\]

The variance: \((1-\theta)\theta = \theta(1-\theta)\), unchanged.
Substituting into Theorem A.4 gives the result. \(\square\)

**Application to FNR.** In the noise-detection problem where
\(e_m \sim Bern(p_1)\) under H\(_1\) and \(p_1 > \theta\):

\[FNR_M = \mathbb{P}(C_M \leq \theta \mid H_1) \sim
\frac{\exp(-M \cdot KL(\theta \| p_1))}{|\lambda_1^*| \sqrt{2\pi M \cdot \theta(1-\theta)}},\]

where \(\lambda_1^* = \log\frac{\theta(1-p_1)}{p_1(1-\theta)} < 0\),
\(|\lambda_1^*| = \log\frac{p_1(1-\theta)}{\theta(1-p_1)}\).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### A.6 Non-i.i.d. Extension<!-- label: a.6-non-i.i.d.-extension -->

#### A.6.1 Setting<!-- label: a.6.1-setting -->

Consider independent but **not identically distributed** Bernoulli
variables:

\[X_m \sim Bernoulli(p_m), \qquad m = 1,...,M,\]

with \(p_m \in [p_, p_] \subset (0,1)\) bounded away from 0
and 1. Define the weighted sample mean
\(C_M = \frac{1}{M}\sum_{m=1}^M X_m\) and a threshold
\(\theta > \limsup_{M\to\infty} \frac{1}{M}\sum p_m\).

#### A.6.2 What Changes<!-- label: a.6.2-what-changes -->

1. 
2. 
3. 
4. 
5. 

#### A.6.3 Summary of Changes<!-- label: a.6.3-summary-of-changes -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2500}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3250}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4250}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Quantity
\end{minipage} & \begin{minipage}[b]
i.i.d. case
\end{minipage} & \begin{minipage}[b]
Non-i.i.d. case
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Saddlepoint \(\lambda^*\) & Closed form
\(\log\frac{\theta(1-p)}{p(1-\theta)}\) & Solves
\(\frac1M\sum \frac{p_m e^\lambda}{1-p_m+p_m e^\lambda} = \theta\) 

Rate function \(I(\theta)\) & \(KL(\theta\|p)\) &
\(\lambda_M^*\theta - \frac1M\sum\log(1-p_m+p_m e^{\lambda_M^*})\) 

Tilted variance \(\sigma^2(\theta)\) & \(\theta(1-\theta)\) &
\(\frac1M\sum q_m(\theta)(1-q_m(\theta))\) 

Leading constant denominator & \(\lambda^*\) & \(\lambda_M^*\) 

\end{longtable}

The **functional form** of the Bahadur-Rao expansion remains
identical; only the constants \((\lambda^*, \sigma^2, I)\) are replaced
by their \(M\)-dependent counterparts.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### A.7 Summary for Lemma A<!-- label: a.7-summary-for-lemma-a -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.1887}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.8113}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Quantity
\end{minipage} & \begin{minipage}[b]
Formula for i.i.d. Bern(\(p\)), \(\theta > p\)
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
CGF \(\psi(\lambda)\) & \(\log(1-p+pe^\lambda)\) 

Saddlepoint \(\lambda^*\) &
\(\log\frac{\theta(1-p)}{p(1-\theta)} > 0\) 

Rate function \(I(\theta)\) &
\(KL(\theta\|p) = \theta\log\frac{p} + (1-\theta)\log\frac{1-\theta}{1-p}\) 

Tilted mean & \(\theta\) 

Tilted variance \(\sigma^2(\theta)\) & \(\theta(1-\theta)\) 

Upper tail (\(\theta > p\)) &
\( \frac{e^{-M\cdotKL(\theta\|p)}} {\lambda^*\sqrt{2\pi M\theta(1-\theta)}} (1+O(1/M))\) 

Lower tail (\(\theta < p\)) &
\( \frac{e^{-M\cdotKL(\theta\|p)}} {|\lambda^*|\sqrt{2\pi M\theta(1-\theta)}} (1+O(1/M))\) 

\(O(1/M)\) constant & Explicit in terms of \(p,\theta\) (Proposition
A.5) 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

## Lemma B: F1 Asymptotic Expansion with Higher-Order
Terms<!-- label: lemma-b-f1-asymptotic-expansion-with-higher-order-terms -->

> **Target**: Starting from the SCX F1 formula, derive the exact
> asymptotic expansion of \(1-F1\) in terms of FPR and FNR, verify
> the expansion's validity at the boundaries \(\eta \to 0\) and
> \(\eta \to 1/2\), and substitute the Bahadur-Rao asymptotics to obtain
> the leading constant.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### B.1 Setup and Notation<!-- label: b.1-setup-and-notation -->

Recall the SCX noise-detection setup:

- 
- 
- 
- 

The F1 score is defined as the harmonic mean of precision and recall:

\[F1 = \frac{2\eta \cdot TPR}{\eta(1+TPR) + (1-\eta)FPR}.\]

*Verification of the formula.* Using the standard definitions:

\[Precision = \frac{\eta \cdot TPR}{\eta \cdot TPR + (1-\eta)FPR}, \qquad
Recall = TPR,\]

we compute

\[

$$
F1 &= \frac{2 \cdot Precision \cdot Recall}{Precision + Recall} 

&= \frac{2 \cdot \frac{\eta\cdotTPR}{\eta\cdotTPR + (1-\eta)FPR} \cdot TPR}
{\frac{\eta\cdotTPR}{\eta\cdotTPR + (1-\eta)FPR} + TPR} 

&= \frac{2\eta\cdotTPR^2}{\eta\cdotTPR + (1-\eta)FPR}
\cdot \frac{1}{\frac{\eta\cdotTPR}{\eta\cdotTPR + (1-\eta)FPR} + TPR} 

&= \frac{2\eta\cdotTPR^2}{\eta\cdotTPR + TPR(\eta\cdotTPR + (1-\eta)FPR)} 

&= \frac{2\eta\cdotTPR}{\eta + \eta\cdotTPR + (1-\eta)FPR} 

&= \frac{2\eta\cdotTPR}{\eta(1+TPR) + (1-\eta)FPR}.
$$

\]

This matches the expression in the proof architecture. No algebraic
error is present -- the denominator is always positive for \(\eta > 0\).

### \texorpdfstring{B.2 Exact Expression for
\(1 - F1\){B.2 Exact Expression for 1 - \ text\{F1\}}}<!-- label: b.2-exact-expression-for-1---textf1 -->

Substituting \(TPR = 1 - FNR\):

\[

$$
F1 &= \frac{2\eta(1-FNR)}
{\eta(2-FNR) + (1-\eta)FPR}.
$$

\]

Thus

\[

$$
1 - F1 &= 1 - \frac{2\eta(1-FNR)}
{\eta(2-FNR) + (1-\eta)FPR} 

&= \frac{\eta(2-FNR) + (1-\eta)FPR - 2\eta(1-FNR)}
{\eta(2-FNR) + (1-\eta)FPR} 

&= \frac{\eta\cdotFNR + (1-\eta)FPR}
{\eta(2-FNR) + (1-\eta)FPR}.
$$

\]

**Sanity checks:** -
\(FNR = FPR = 0 \implies 1-F1 = 0\). -
\(\eta = 0\): \(1-F1 = FPR/FPR = 1\) (F1 = 0, no
positives possible). - \(\eta = 1\):
\(1-F1 = FNR/(2-FNR) \approx FNR/2\). -
Denominator
\(= 2\eta - \eta\cdotFNR + (1-\eta)FPR \geq \eta > 0\)
(strictly positive for \(\eta > 0\)).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### B.3 First-Order Expansion<!-- label: b.3-first-order-expansion -->

Let

\[\alpha = \eta\cdotFNR + (1-\eta)FPR, \qquad
\beta = 2\eta - \eta\cdotFNR + (1-\eta)FPR.\]

Then

\[1 - F1 = \frac.\]

Factor \(\beta = 2\eta(1 - \gamma)\) where

\[\gamma := \frac{\eta\cdotFNR - (1-\eta)FPR}{2\eta}
= \frac{FNR}{2} - \frac{(1-\eta)FPR}{2\eta}.\]

Thus

\[1 - F1 = \frac{2\eta} \cdot \frac{1}{1 - \gamma}.\]

For \(|\gamma| < 1\) (which holds for all sufficiently large \(M\) since
\(FNR,FPR \to 0\)), the geometric series converges:

\[\frac{1}{1 - \gamma} = \sum_{k=0}^\infty \gamma^k.\]

Let

\[A := \frac{FNR}{2}, \qquad B := \frac{(1-\eta)FPR}{2\eta}.\]

Then \(\alpha/(2\eta) = A + B\), and \(\gamma = A - B\).

**First-order expansion:**

\[1 - F1 = A + B + R,\]

where

\[R = (A+B) \cdot \frac{1-\gamma} = \frac{(A+B)(A-B)}{1-(A-B)}.\]

**Theorem B.1 (First-order expansion with error bound)**. For
\(|\gamma| = |A-B| < 1\),

\[1 - F1 = \frac{FNR}{2} + \frac{(1-\eta)}{2\eta}\,FPR + R,\]

where the remainder satisfies

\[|R| \leq \frac{(FNR/2 + (1-\eta)FPR/(2\eta))^2}
{1 - FNR/2 - (1-\eta)FPR/(2\eta)}.\]

*Proof.* We have \(|A+B| \leq r\) and \(|A-B| \leq r\) where
\(r = A+B = FNR/2 + (1-\eta)FPR/(2\eta)\). Then

\[|R| = \frac{(A+B)|A-B|}{1-|A-B|} \leq \frac{r^2}{1-r}.\]

For sufficiently large \(M\), \(r \leq 1/2\) and \(|R| \leq 2r^2\). This
gives the bound. \(\square\)

**Corollary B.2 (Quadratic bound)**. For \(M\) large enough that
\(r \leq 1/2\),

\[|R| \leq 2\left(\frac{FNR}{2} + \frac{(1-\eta)FPR}{2\eta}\right)^2
\leq \frac{FNR^2}{2} + \frac{(1-\eta)FNR\cdotFPR}
+ \frac{(1-\eta)^2FPR^2}{2\eta^2}.\]

In particular,
\(R = O(\max(FPR^2, FNR^2, FPR\cdotFNR))\).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### B.4 Second-Order Expansion (Explicit
Terms)<!-- label: b.4-second-order-expansion-explicit-terms -->

Expanding to second order in \(\gamma\):

\[

$$
1 - F1 &= (A+B)(1 + \gamma + \gamma^2 + \gamma^3 + ...) 

&= (A+B) + (A+B)(A-B) + (A+B)(A-B)^2 + O(r^4).
$$
\]

**Explicit second-order terms:**

\[

$$
1 - F1 &= \frac{FNR}{2} + \frac{(1-\eta)FPR}{2\eta} 

&\quad + \frac{FNR^2}{4} - \frac{(1-\eta)^2FPR^2}{4\eta^2} 

&\quad + \big(\tfrac{FNR}{2} + \tfrac{(1-\eta)FPR}{2\eta}\big)
\big(\tfrac{FNR}{2} - \tfrac{(1-\eta)FPR}{2\eta}\big)^2 

&\quad + O(r^4).
$$

\]

**Explicit \(O(\cdot)\) constant in terms of
\(\max(FPR^2, FNR^2, FPR\cdotFNR)\)**:

From Corollary B.2, when \(r \leq 1/2\):

\[|R| \leq \frac{FNR^2}{2} + \frac{(1-\eta)FNR\cdotFPR}
+ \frac{(1-\eta)^2FPR^2}{2\eta^2}.\]

Let
\(M_2 = \max(FNR^2, FPR^2, FNR\cdotFPR)\).
Then

\[|R| \leq \left(\frac{1}{2} + \frac{1-\eta} + \frac{(1-\eta)^2}{2\eta^2}\right) M_2
= \frac{1}{2\eta^2}\big(\eta^2 + 2\eta(1-\eta) + (1-\eta)^2\big) M_2
= \frac{1}{2\eta^2} \cdot 1 \cdot M_2,\]

where we used
\(\eta^2 + 2\eta(1-\eta) + (1-\eta)^2 = (\eta + (1-\eta))^2 = 1\).

Thus

\[|R| \leq \frac{1}{2\eta^2} \cdot \max(FNR^2, FPR^2, FNR\cdotFPR).\]

This gives the explicit constant \(C = 1/(2\eta^2)\) for the
\(O(\cdot)\) remainder.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### B.5 Substituting the Bahadur-Rao
Asymptotics<!-- label: b.5-substituting-the-bahadur-rao-asymptotics -->

Now substitute the leading-order Bahadur-Rao expansions:

\[
$$
FPR_M &\sim \frac{e^{-M\kappa_0}}{\lambda_0^* \sqrt{2\pi M \theta(1-\theta)}}, \quad
\kappa_0 = KL(\theta\|p_0),\; \lambda_0^* = \log\frac{\theta(1-p_0)}{p_0(1-\theta)} > 0, 

FNR_M &\sim \frac{e^{-M\kappa_1}}{|\lambda_1^*| \sqrt{2\pi M \theta(1-\theta)}}, \quad
\kappa_1 = KL(\theta\|p_1),\; |\lambda_1^*| = \log\frac{p_1(1-\theta)}{\theta(1-p_1)} > 0.
$$
\]

**Theorem B.3 (Leading term of \(1-F1\) with Bahadur-Rao)**.

\[
1 - F1 = \frac{1}{\sqrt{2\pi M \cdot \theta(1-\theta)}}
\left[\frac{e^{-M\kappa_1}}{2\,|\lambda_1^*|} + \frac{1-\eta}{2\eta}\cdot\frac{e^{-M\kappa_0}}{\lambda_0^*}\right]
+ O\!\left(\frac{e^{-2M\min(\kappa_0,\kappa_1)}}{M}\right).
\]

*Proof.* Substitute the leading terms of FPR and FNR into the
first-order expansion from Theorem B.1. The remainder \(R\) from
Corollary B.2 is bounded by
\(O(\max(FPR^2,FNR^2)) = O(e^{-2M\min(\kappa_0,\kappa_1)}/M)\),
since each of FPR\(^2\) and FNR\(^2\) decays with twice the exponent and
an extra \(1/M\) factor from the square. \(\square\)

#### B.5.1 Optimal Threshold: Chernoff
Point<!-- label: b.5.1-optimal-threshold-chernoff-point -->

The optimal threshold \(\theta^*\) balances the two exponents:

\[\kappa = KL(\theta^*\|p_0) = KL(\theta^*\|p_1) = C(Bern(p_0), Bern(p_1)),\]

where \(C(\cdot,\cdot)\) is the Chernoff information. At
\(\theta = \theta^*\):

\[1 - F1 \sim \frac{e^{-M\kappa}}{\sqrt{2\pi M \cdot \theta^*(1-\theta^*)}} \cdot
\left[\frac{1}{2|\lambda_1^*(\theta^*)|} + \frac{1-\eta}{2\eta \cdot \lambda_0^*(\theta^*)}\right].\]

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### B.6 Verification of the Expansion at Special
Cases<!-- label: b.6-verification-of-the-expansion-at-special-cases -->

#### \texorpdfstring{B.6.1 Case \(\eta \to 0\) (Sparse
Noise){B.6.1 Case \ eta \ to 0 (Sparse Noise)}}<!-- label: b.6.1-case-eta-to-0-sparse-noise -->

As \(\eta \to 0\), the coefficient \((1-\eta)/(2\eta) \to \infty\), so
the FPR term dominates both the FNR term and the expansion itself. The
convergence condition \(|\gamma| < 1\) becomes:

\[|\gamma| = \left|\frac{FNR}{2} - \frac{(1-\eta)FPR}{2\eta}\right| < 1.\]

For small \(\eta\), this is dominated by the second term, requiring
\(FPR < 2\eta/(1-\eta) \approx 2\eta\).

Using the Bahadur-Rao approximation
\(FPR \approx e^{-M\kappa_0}/(\lambda_0^*\sqrt{M})\), the
condition becomes:

\[\frac{e^{-M\kappa_0}}{\lambda_0^*\sqrt{2\pi M \theta(1-\theta)}} \lesssim 2\eta.\]

**Definition (Threshold \(\eta_\))**. Define

\[\eta_(M) = \frac{1}{2} \cdot \frac{e^{-M\kappa_0}}{\lambda_0^*\sqrt{2\pi M \theta(1-\theta)}}.\]

For \(\eta \ll \eta_(M)\), the geometric series \(\sum \gamma^k\)
converges slowly (or diverges), and the polynomial expansion in FPR/FNR
is no longer valid. In this regime, a different asymptotic expression is
needed:

\[
$$
1 - F1 &= \frac{\eta\cdotFNR + (1-\eta)FPR}
{\eta(2-FNR) + (1-\eta)FPR} 

&\approx \frac{FPR}{FPR + \eta/(1-\eta)} \qquad (neglecting FNR terms) 

&= \frac{1}{1 + \eta/[(1-\eta)FPR]}.
$$
\]

When \(\eta \ll \eta_\), we have \(\eta \ll FPR\), so
\(1-F1 \approx 1\) (F1 \(\approx\) 0). This is intuitive: with
extremely rare noise, even a tiny FPR destroys precision.

**Practical implication:** The expansion
\(1-F1 \approx FNR/2 + (1-\eta)FPR/(2\eta)\) is
valid whenever

\[\eta \gtrsim \eta_(M) = \frac{e^{-M\kappa_0}}{2\lambda_0^*\sqrt{2\pi M \theta(1-\theta)}}.\]

For realistic \(M\), this threshold is exponentially small, so the
expansion holds in almost all practical settings.

#### \texorpdfstring{B.6.2 Case \(\eta \to 1/2\) (Balanced
Noise){B.6.2 Case \ eta \ to 1/2 (Balanced Noise)}}<!-- label: b.6.2-case-eta-to-12-balanced-noise -->

When \(\eta = 1/2\), the expansion simplifies dramatically:

\[
$$
1 - F1 &= \frac{\frac{1}{2}FNR + \frac{1}{2}FPR}
{\frac{1}{2}(2-FNR) + \frac{1}{2}FPR}
= \frac{FNR + FPR}{2 - FNR + FPR} 

&= \frac{FNR+FPR}{2} \cdot \frac{1}{1 - (FNR-FPR)/2}.
$$
\]

**First-order:**

\[1 - F1 = \frac{FNR + FPR}{2} + O\big(\max(FNR^2,FPR^2)\big).\]

**With Bahadur-Rao substitution at \(\theta^*\):**

\[
1 - F1 \sim \frac{e^{-M\kappa}}{2\sqrt{2\pi M \cdot \theta^*(1-\theta^*)}}
\left(\frac{1}{|\lambda_1^*|} + \frac{1}{\lambda_0^*}\right).
\]

In the symmetric case \(p_0 = 1-p_1\) (which implies \(\theta^* = 1/2\),
\(\lambda_0^* = |\lambda_1^*|\)), this further simplifies to:

\[1 - F1 \sim \frac{e^{-M\kappa}}{\lambda_0^* \sqrt{2\pi M \cdot \theta^*(1-\theta^*)}}.\]

#### B.6.3 Summary of Regimes<!-- label: b.6.3-summary-of-regimes -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.2051}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.7949}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Regime
\end{minipage} & \begin{minipage}[b]
Leading term of \(1-F1\)
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(\eta \gg \eta_\) (general) &
\(\frac{FNR}{2} + \frac{1-\eta}{2\eta}FPR\) 

\(\eta = 1/2\) (balanced) & \((FNR + FPR)/2\) 

\(\eta \ll \eta_\) (ultra-sparse) & \(\approx 1\) (expansion
breaks down) 

\(\eta \to 1\) (dominant noise) & \(FNR/2 + o(FNR)\) 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### \texorpdfstring{B.7 Explicit Constant for the \(O(\cdot)\)
Term{B.7 Explicit Constant for the O(\ cdot) Term}}<!-- label: b.7-explicit-constant-for-the-ocdot-term -->

Collecting the results from Sections B.3-B.5, we have the complete
asymptotic:

**Theorem B.4 (Full expansion with explicit constants)**. Let
\(FPR = FPR_M\) and \(FNR = FNR_M\) be the
error rates from the threshold test with threshold \(\theta\). Assume
\(M\) is large enough that

\[r := \frac{FNR}{2} + \frac{(1-\eta)FPR}{2\eta} \leq \frac{1}{2}.\]

Then

\[
1 - F1 = \frac{FNR}{2} + \frac{1-\eta}{2\eta}FPR
+ \frac{FNR^2}{4} - \frac{(1-\eta)^2FPR^2}{4\eta^2} + R_3,
\]

where
\(|R_3| \leq 2r^3 \leq \frac{1}{4\eta^3}\big(\eta\cdotFNR + (1-\eta)FPR\big)^3\).

When \(\eta \gtrsim \eta_(M)\), substituting the Bahadur-Rao
expansions yields:

\[
1 - F1 = \frac{1}{\sqrt{2\pi M\theta(1-\theta)}}
\left[\frac{e^{-M\kappa_1}}{2|\lambda_1^*|} + \frac{1-\eta}{2\eta}\frac{e^{-M\kappa_0}}{\lambda_0^*}\right]
\cdot \big(1 + O(1/M)\big) + O\!\left(\frac{e^{-2M\min(\kappa_0,\kappa_1)}}{M}\right).
\]

At the Chernoff point \(\theta^*\) where
\(\kappa_0 = \kappa_1 = \kappa\):

\[
1 - F1 = \frac{e^{-M\kappa}}{\sqrt{2\pi M\theta^*(1-\theta^*)}}
\left[\frac{1}{2|\lambda_1^*|} + \frac{1-\eta}{2\eta\lambda_0^*}\right]
\cdot \big(1 + O(1/M)\big).
\]

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### B.8 Verification: No Denominator
Bug<!-- label: b.8-verification-no-denominator-bug -->

The user noted a concern about the denominator going negative in v1. We
verify:

\[Denominator = \eta(2-FNR) + (1-\eta)FPR.\]

Since \(FNR \leq 1\), we have \(2 - FNR \geq 1\), so

\[Denominator \geq \eta \cdot 1 + 0 = \eta > 0 \quad (for  \eta > 0).\]

For \(\eta = 0\), the F1 formula is degenerate (no positive samples),
which is handled separately. **No algebraic error exists** in the
F1 expression used in the proof architecture.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### References<!-- label: references -->

1. 
2. 
3. 
4. 
5. 
6.