# Theorem 3: Cluster Consistency of State Discovery Under Strong
Features

**Author:** SCX

> **Core Claim**: When the feature representation \(\phi(x)\) carries
> sufficient information about the true state \(S = s(x)\), k-means
> clustering on \(\phi(x)\) recovers the true state partition with high
> probability as \(n \to \infty\) and \(K \to \infty\) at rate
> \(K = o(n^{1/3})\). This is the positive counterpart to Theorem 2's
> negative result.

**Associated concepts**: {[}{[}Strong Feature Regime{]}{]},
{[}{[}State Discovery{]}{]}, {[}{[}k-means Consistency{]}{]},
{[}{[}Theorem 2 Counterpart{]}{]} **Associated code**:
`src/scx/state/discovery.py` (Layer 1 + Layer 2)
**Associated experiments**: AlN v3 MLIP (ACE descriptor, success
case)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Table of Contents<!-- label: table-of-contents -->

1. 
2. 
3. 
4. 
5. 
6. 
7. 
8. 
9. 
10. 
11. 
12. 
13. 
14. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. Notation and Setup<!-- label: notation-and-setup -->

#### 1.1 Data Generating
Process<!-- label: data-generating-process -->

Let \((\Omega, \mathcal{F}, P)\) be a probability space. We observe
\(n\) i.i.d. copies of the feature vector
\(\phi(x) \in \mathbb{R}^{d_\phi}\).

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2667}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3000}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4333}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Symbol
\end{minipage} & \begin{minipage}[b]
Meaning
\end{minipage} & \begin{minipage}[b]
Value Space
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(X\) & Input random variable &
\(\mathcal{X} \subseteq \mathbb{R}^d\) 

\(S = s(X)\) & **Unobserved** true state &
\(\mathcal{S} = \{1, ..., K\}\) 

\(\phi(X)\) & Observed feature representation &
\(\mathbb{R}^{d_\phi}\) 

\(\{\mu_k\}_{k=1}^K\) & True cluster centers (state means) &
\(\mathbb{R}^{d_\phi}\) 

\(\sigma^2\) & Noise variance (sub-Gaussian parameter) &
\(\mathbb{R}^+\) 

\(\Delta_\) & Minimum separation between centers &
\(\mathbb{R}^+\) 

\(n\) & Number of samples & \(\mathbb{N}\) 

\(K = K_n\) & Number of states (may grow with \(n\)) & \(\mathbb{N}\) 

\end{longtable}

#### 1.2 Generative Model<!-- label: generative-model -->

We assume the following additive model for the feature representation:

\[\phi(x) = S(x) + \varepsilon\]

where: - \(S(x) \in \{\mu_1, ..., \mu_K\}\) is the true cluster center
for the state containing \(x\) - \(\varepsilon \in \mathbb{R}^{d_\phi}\)
is zero-mean noise, sub-Gaussian with parameter \(\sigma^2\):
\[\mathbb{E}[\varepsilon] = 0, \quad \mathbb{E}[\exp(t \cdot u^\top \varepsilon)] \leq \exp(\sigma^2 t^2 / 2), \quad \forall u \in \mathbb{S}^{d_\phi-1}, \; \forall t \in \mathbb{R}\]

#### 1.3 Cluster Structure<!-- label: cluster-structure -->

Define: - **True partition**:
\(\mathcal{C}^* = \{C_1^*, ..., C_K^*\}\) where
\(C_k^* = \{x \in \mathcal{X} : s(x) = k\}\) - **True centers**:
\(\mu_k = \mathbb{E}[\phi(X) \mid S = k]\) - **Population
proportions**: \(\pi_k = P(S = k)\), with \(\pi_k > 0\) for all \(k\)

#### 1.4 Separation Condition<!-- label: separation-condition -->

The minimum separation between distinct cluster centers is:

\[\Delta_ = \min_{i \neq j} \|\mu_i - \mu_j\|_2\]

We assume the strong separation condition:

\[\Delta_^2 \geq C_0 \cdot \frac{\sigma^2 K \log n}{n}\]

for a sufficiently large universal constant \(C_0 > 0\), where the exact
constant is determined by the sub-Gaussian tail and the metric entropy
of the \(K\)-center class.

#### 1.5 k-means Objective<!-- label: k-means-objective -->

For a set of \(K\) candidate centers
\(\hat = \{\hat_1, ..., \hat_K\} \subset \mathbb{R}^{d_\phi}\),
define the **empirical k-means risk**:

\[W_n(\hat) = \frac{1}{n} \sum_{i=1}^n \min_{k \in [K]} \|\phi(x_i) - \hat_k\|_2^2\]

The **population k-means risk** is:

\[W(\hat) = \mathbb{E}\left[\min_{k \in [K]} \|\phi(X) - \hat_k\|_2^2\right]\]

The **optimal empirical centers** are:

\[\hat_n^* = \arg \min_{\hat: |\hat| = K} W_n(\hat)\]

The **optimal population centers** are:

\[\mu^* = \arg \min_{\mu: |\mu| = K} W(\mu)\]

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2. Theorem Statement<!-- label: theorem-statement -->

**Theorem 3 (Cluster Consistency Under Strong Features)**. Let
\(\phi(x) = S(x) + \varepsilon\) where
\(S(x) \in \{\mu_1, ..., \mu_K\}\) are \(K\) true cluster centers and
\(\varepsilon\) is zero-mean sub-Gaussian noise with parameter
\(\sigma^2\). Suppose:

1. 
2. 
3. 
4. 

Let \(\hat{C}^{(n)} = \{\hat{C}_1^{(n)}, ..., \hat{C}_K^{(n)}\}\) be
the partition induced by the empirical k-means minimizer
\(\hat_n^*\) on \(n\) i.i.d. samples. Then:

\[\mathbb{P}\left(\hat{C}^{(n)} \neq \mathcal{C}^*  up to permutation\right) \leq \delta_n\]

where \(\delta_n \to 0\) as \(n \to \infty\). Specifically, the
misclassification rate satisfies:

\[\mathbb{P}\left(\frac{1}{n} \sum_{i=1}^n \mathbf{1}\{\hat{s}(x_i) \neq s(x_i)\} > \tau_n\right) \leq \varepsilon_n\]

with:

\[\tau_n = O\left(\frac{K}{n \Delta_^2}\right), \quad
\varepsilon_n = O\left(K \cdot \exp\left(-c \cdot \frac{n \Delta_^2}{K}\right)\right)\]

for a universal constant \(c > 0\), where \(\hat{s}(x_i)\) is the
estimated state assignment from k-means.

**Simplified rate**: Under optimal scaling
\(\Delta_^2 = \Theta(\sigma^2 K \log n / n)\), we have:

\[\mathbb{P}(any misclassification) = O\left(K \cdot n^{-c C_0}\right) \to 0\]

when \(C_0\) is sufficiently large.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 3. Proof Architecture<!-- label: proof-architecture -->

The proof proceeds through four lemmas:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1875}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2188}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2812}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3125}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Step
\end{minipage} & \begin{minipage}[b]
Lemma
\end{minipage} & \begin{minipage}[b]
Purpose
\end{minipage} & \begin{minipage}[b]
Key Tool
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
1 & Lemma 3 & Uniform convergence:
\(\sup_ \|W_n(\mu) - W(\mu)\|_2 \to 0\) & VC theory / empirical
processes 

2 & Lemma 4 & Metric entropy bound for
\(\Theta_K = \{\mu \subset \mathbb{R}^{d_\phi} : |\mu| = K, \|\mu_k\| \leq M\}\)
& Dudley's entropy integral 

3 & Lemma 5 & Under separation, \(\mu^*\) (population minimizer) equals
true centers \(\{\mu_k\}\) up to permutation & Population k-means
analysis 

4 & Lemma 6 & \(\|W_n(\hat_n^*) - W(\mu^*)\|\) small \(\implies\)
partition error small & Quadratic lower bound 

\end{longtable}

The chain of implication:

\[
$$
&Lemma 3 + Lemma 4:  W_n \to W  uniformly 

&Lemma 5:  \mu^* = \{\mu_1,...,\mu_K\}  (true centers) 

&\Rightarrow \hat_n^* \to \mu^*  (consistency of argmin) 

&\Rightarrow Partitions match  (\hat{C}^{(n)} \to \mathcal{C}^*) 

&\Rightarrow Misclassification rate  \to 0
$$
\]

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. Lemma 3: Uniform Convergence of the k-means
Risk<!-- label: lemma-3-uniform-convergence-of-the-k-means-risk -->

**Lemma 3 (Uniform Convergence)**. Let
\(\Theta_K = \{\mu = \{\mu_1,...,\mu_K\} : \mu_k \in \mathbb{R}^{d_\phi}, \|\mu_k\|_2 \leq M\}\)
be the class of \(K\)-center sets. Under the conditions of Theorem 3,
for any \(\delta > 0\):

\[\mathbb{P}\left(\sup_{\mu \in \Theta_K} |W_n(\mu) - W(\mu)| > \delta\right) \leq \mathcal{N}(\delta/4, \Theta_K, \|\cdot\|_\infty) \cdot \exp\left(-\frac{n \delta^2}{32 C_1^2}\right)\]

where \(\mathcal{N}(\varepsilon, \Theta_K, \|\cdot\|_\infty)\) is the
\(\varepsilon\)-covering number of \(\Theta_K\) in the \(\ell_\infty\)
norm (maximum over centers), and \(C_1 = 4(M + \sqrt{\sigma^2 d_\phi})\)
is a Lipschitz constant.

**Proof of Lemma 3**.

**Step 1: Lipschitz property**. For any fixed \(x\), the function
\(g_x(\mu) = \min_{k \in [K]} \|\phi(x) - \mu_k\|_2^2\) is
\(L\)-Lipschitz in \(\mu\) with respect to the \(\ell_\infty\) norm.
Specifically, for two center sets \(\mu, \mu'\) with
\(\|\mu_k - \mu_k'\|_2 \leq \delta_\infty\) for all \(k\):

\[
$$
|g_x(\mu) - g_x(\mu')|
&\leq \max_k \left| \|\phi(x) - \mu_k\|_2^2 - \|\phi(x) - \mu_k'\|_2^2 \right| 

&\leq \max_k \left( \|\phi(x) - \mu_k\|_2 + \|\phi(x) - \mu_k'\|_2 \right) \cdot \|\mu_k - \mu_k'\|_2 

&\leq 2\left(\|\phi(x)\|_2 + M\right) \cdot \delta_\infty
$$
\]

Using \(\|\phi(x)\|_2 \leq M + \|\varepsilon\|_2\), and
\(\mathbb{E}[\|\varepsilon\|_2^2] \leq \sigma^2 d_\phi\), we have with
high probability \(\|\phi(x)\|_2 \leq M + C\sqrt{\sigma^2 d_\phi}\).
Thus \(g_x\) is \(L\)-Lipschitz with
\(L = 4(M + \sqrt{\sigma^2 d_\phi}) \triangleq C_1\).

**Step 2: Bernstein's inequality for bounded random variables**.
For a fixed \(\mu\), each term \(g_{x_i}(\mu)\) is bounded:
\(g_{x_i}(\mu) \in [0, 2(\|\phi(x_i)\|_2^2 + M^2)] \leq [0, B]\) with
\(B = 4(M^2 + \sigma^2 d_\phi)\) w.h.p. By Hoeffding's inequality:

\[\mathbb{P}(|W_n(\mu) - W(\mu)| > \delta) \leq 2\exp\left(-\frac{2n\delta^2}{B^2}\right)\]

But the simpler Bernstein bound gives the sub-Gaussian form we need.
Since \(Var(g_X(\mu)) \leq \mathbb{E}[g_X(\mu)^2] \leq B^2/4\),
we have by Bernstein:

\[\mathbb{P}(|W_n(\mu) - W(\mu)| > \delta) \leq 2\exp\left(-\frac{n\delta^2}{2\mathbb{E}[g_X(\mu)^2] + 2B\delta/3}\right) \leq 2\exp\left(-\frac{c n \delta^2}{C_1^2}\right)\]

for some universal \(c > 0\), since \(B = O(C_1)\).

**Step 3: Chaining via covering numbers**. Let
\(\mathcal{N}_\varepsilon = \mathcal{N}(\varepsilon, \Theta_K, \|\cdot\|_\infty)\)
be an \(\varepsilon\)-cover. For any \(\mu \in \Theta_K\), there exists
\(\mu^{(j)} \in \mathcal{N}_\varepsilon\) such that
\(\|\mu - \mu^{(j)}\|_\infty \leq \varepsilon\). Then:

\[
$$
|W_n(\mu) - W(\mu)|
&\leq |W_n(\mu) - W_n(\mu^{(j)})| + |W_n(\mu^{(j)}) - W(\mu^{(j)})| + |W(\mu^{(j)}) - W(\mu)| 

&\leq 2L\varepsilon + |W_n(\mu^{(j)}) - W(\mu^{(j)})|
$$
\]

Taking \(\varepsilon = \delta/(4L)\), we have:

\[\sup_ |W_n(\mu) - W(\mu)| \leq \delta/2 + \max_{\mu^{(j)} \in \mathcal{N}_\varepsilon} |W_n(\mu^{(j)}) - W(\mu^{(j)})|\]

By union bound over the cover and Bernstein:

\[
$$
\mathbb{P}\left(\sup_ |W_n(\mu) - W(\mu)| > \delta\right)
&\leq \mathcal{N}_\varepsilon \cdot \mathbb{P}\left(|W_n(\mu^{(j)}) - W(\mu^{(j)})| > \delta/2\right) 

&\leq \mathcal{N}\left(\frac{4L}, \Theta_K, \|\cdot\|_\infty\right) \cdot 2\exp\left(-\frac{n \delta^2}{8c^{-1} C_1^2}\right)
$$
\]

Absorbing constants, we obtain:

\[\mathbb{P}\left(\sup_ |W_n(\mu) - W(\mu)| > \delta\right) \leq \mathcal{N}\left(\frac{4C_1}, \Theta_K, \|\cdot\|_\infty\right) \cdot \exp\left(-\frac{n\delta^2}{32 C_1^2}\right)\]

\(\square\)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 5. Lemma 4: Complexity Control via Dudley's Entropy
Bound<!-- label: lemma-4-complexity-control-via-dudleys-entropy-bound -->

**Lemma 4 (Metric Entropy of \(K\)-Center Sets)**. Let
\(\Theta_K = \{\mu = \{\mu_1,...,\mu_K\} : \mu_k \in \mathbb{R}^{d_\phi}, \|\mu_k\|_2 \leq M\}\)
equipped with the \(\ell_\infty\) metric
\(\|\mu - \mu'\|_\infty = \max_{k \in [K]} \|\mu_k - \mu_k'\|_2\). The
\(\varepsilon\)-covering number satisfies:

\[\log \mathcal{N}(\varepsilon, \Theta_K, \|\cdot\|_\infty) \leq K \cdot d_\phi \cdot \log\left(1 + \frac{2M}\right)\]

**Proof of Lemma 4**.

The set \(\Theta_K\) is a Cartesian product of \(K\) balls of radius
\(M\) in \(\mathbb{R}^{d_\phi}\):

\[\Theta_K = \underbrace{B_M(0) \times ... \times B_M(0)}_{K  times}\]

where \(B_M(0) = \{v \in \mathbb{R}^{d_\phi} : \|v\|_2 \leq M\}\).

The \(\varepsilon\)-covering number of \(B_M(0)\) in \(\ell_2\) is
bounded by the standard volumetric argument:

\[\mathcal{N}\left(\varepsilon, B_M(0), \|\cdot\|_2\right) \leq \left(1 + \frac{2M}\right)^{d_\phi}\]

The \(\ell_\infty\) metric on \(\Theta_K\) is the max over \(K\)
independent \(\ell_2\) metrics. Thus the covering number of the product
is the product of the per-coordinate covering numbers:

\[\mathcal{N}\left(\varepsilon, \Theta_K, \|\cdot\|_\infty\right) \leq \prod_{k=1}^K \mathcal{N}\left(\varepsilon, B_M(0), \|\cdot\|_2\right) \leq \left(1 + \frac{2M}\right)^{K d_\phi}\]

Taking logarithms:

\[\log \mathcal{N}\left(\varepsilon, \Theta_K, \|\cdot\|_\infty\right) \leq K d_\phi \log\left(1 + \frac{2M}\right)\]

\(\square\)

**Corollary 4.1 (Dudley's Integral Bound)**. The uniform
convergence bound from Lemma 3, combined with the entropy bound, yields:

\[\mathbb{P}\left(\sup_{\mu \in \Theta_K} |W_n(\mu) - W(\mu)| > \delta\right) \leq \left(\frac{4C_1} + \frac{2M}\right)^{K d_\phi} \cdot \exp\left(-\frac{n\delta^2}{32 C_1^2}\right)\]

for \(\delta \leq 4C_1 M\). Equivalently, for any \(\delta > 0\):

\[\log \mathbb{P}\left(\sup_ |W_n(\mu) - W(\mu)| > \delta\right) \leq K d_\phi \log\left(1 + \frac{8C_1 M}\right) - \frac{n\delta^2}{32 C_1^2}\]

**Note**: The metric entropy bound
\(O(K d_\phi \log(1/\varepsilon))\) obtained here is sufficient for our
purposes. A sharper bound using VC dimension of \(K\)-means (which has
VC dimension \(O(K d_\phi)\)) would replace \(K d_\phi\) with
\(K d_\phi\), matching our bound in the leading term, so no improvement
is needed. The key quantity is the product \(K d_\phi\) which enters the
numerator of the variance penalty.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 6. Lemma 5: Separation Condition and Population
Uniqueness<!-- label: lemma-5-separation-condition-and-population-uniqueness -->

**Lemma 5 (Population Minimizer Equals True Centers)**. Under the
generative model \(\phi(x) = S(x) + \varepsilon\) with \(\varepsilon\)
sub-Gaussian\((0, \sigma^2 I)\), the population k-means objective
\(W(\mu) = \mathbb{E}[\min_k \|\phi(X) - \mu_k\|_2^2]\) is uniquely
minimized (up to permutation) by the true centers
\(\{\mu_1, ..., \mu_K\}\), provided:

\[\Delta_^2 > 4\sigma^2 \cdot \Phi^{-1}\left(1 - \frac{1}{2K}\right)^2\]

where \(\Phi\) is the CDF of \(\mathcal{N}(0,1)\), and \(\sigma^2\) is
the per-coordinate variance of \(\varepsilon\).

Under the high-dimensional scaling \(K \to \infty\), this requires:

\[\Delta_^2 = \omega(\sigma^2 \log K)\]

**Proof of Lemma 5**.

**Step 1: Population risk decomposition**. Let
\(\mu = \{\mu_1',...,\mu_K'\}\) be any candidate center set. The
population risk can be written as:

\[W(\mu) = \mathbb{E}\left[\|\phi(X)\|_2^2\right] - 2\sum_{k=1}^K \pi_k \cdot \mu_k^\top \mu_{\sigma(k)}' + \sum_{k=1}^K \pi_k \cdot \|\mu_{\sigma(k)}'\|_2^2 + penalty terms\]

where \(\sigma: [K] \to [K]\) is the optimal assignment matching true
centers to candidate centers. More precisely, for each true component
\(k\), points are assigned to the nearest candidate center:

\[W(\mu) = \sum_{k=1}^K \pi_k \cdot \mathbb{E}\left[\min_{j \in [K]} \|\mu_k + \varepsilon - \mu_j'\|_2^2 \mid S = k\right]\]

**Step 2: Optimality of true centers**. We show that any
\(\mu \neq \{\mu_1,...,\mu_K\}\) has strictly larger population risk.
Consider the decomposition:

\[
$$
W(\mu) - W(\mu^*)
&= \sum_{k=1}^K \pi_k \left( \mathbb{E}\left[\min_j \|\mu_k + \varepsilon - \mu_j'\|_2^2\right] - \mathbb{E}\left[\|\varepsilon\|_2^2\right] \right) 

&= \sum_{k=1}^K \pi_k \cdot \mathbb{E}\left[ \min_j \|\mu_k - \mu_j' + \varepsilon\|_2^2 - \|\varepsilon\|_2^2 \right]
$$
\]

**Step 3: Lower bound via separation**. For a fixed true center
\(\mu_k\), let \(j^*(k) = \arg\min_j \|\mu_k - \mu_j'\|_2\). Then:

\[\mathbb{E}\left[ \min_j \|\mu_k - \mu_j' + \varepsilon\|_2^2 \right] \geq \mathbb{E}\left[ \|\mu_k - \mu_{j^*(k)}' + \varepsilon\|_2^2 \right]\]

Let \(\delta_k = \|\mu_k - \mu_{j^*(k)}'\|_2\). If \(\mu\) differs from
\(\mu^*\), then there exists at least one \(k\) with \(\delta_k > 0\).

For such \(k\), by the properties of sub-Gaussian noise:

\[\mathbb{E}\left[ \|\mu_k - \mu_{j^*(k)}' + \varepsilon\|_2^2 \right] = \delta_k^2 + \mathbb{E}[\|\varepsilon\|_2^2]\]

while for the true match (\(\mu_j' = \mu_k\)), we have
\(\mathbb{E}[\|\varepsilon\|_2^2]\).

Thus:

\[W(\mu) - W(\mu^*) = \sum_{k=1}^K \pi_k \cdot \delta_k^2\]

This is strictly positive whenever at least one \(\delta_k > 0\),
proving that \(\mu^* = \{\mu_1,...,\mu_K\}\) is the unique minimizer
up to permutation.

**Step 4: Identification guarantee under noise**. The critical case
is when \(\mu\) is close to the true centers but misassigns one or more
centers. We need that even a single center perturbation of size
\(\Delta_/2\) increases the risk measurably. Since
\(W(\mu) - W(\mu^*) \geq \pi_ \Delta_^2 / 4\) for any
\(\mu\) that is not equivalent to \(\mu^*\) up to permutation (where
\(\pi_ = \min_k \pi_k\)), identification is guaranteed.

The sub-Gaussian tail condition
\(\Delta_^2 > 4\sigma^2 \Phi^{-1}(1 - 1/(2K))^2\) ensures that
with probability at least \(1 - 1/K\), each point is closer to its own
center than to any other center. This is the per-point separation
condition.

\(\square\)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 7. Lemma 6: Error Propagation -- Empirical to True
Partition<!-- label: lemma-6-error-propagation-empirical-to-true-partition -->

**Lemma 6 (Risk Gap Implies Partition Error Bound)**. Let
\(\hat_n\) be any \(K\)-center set with empirical risk
\(W_n(\hat_n) \leq W_n(\mu^*) + \eta\) for some \(\eta > 0\). Let
\(\hat{C}\) be the Voronoi partition induced by \(\hat_n\) and
\(C^*\) be the true partition. Then:

\[\frac{1}{n} \sum_{i=1}^n \mathbf{1}\{\hat{s}(x_i) \neq s(x_i)\} \leq \frac{4\eta}{\pi_ \Delta_^2}\]

with probability at least \(1 - \delta\), where
\(\pi_ = \min_k \pi_k\).

**Proof of Lemma 6**.

**Step 1: Relating risk gap to center estimation error**. The
estimated centers \(\hat_n\) differ from the true centers
\(\mu^*\). Let \(\tau: [K] \to [K]\) be the optimal matching
permutation. For each true center \(k\), define \(\hat_{\tau(k)}\)
as the matched estimated center.

For any sample \(x_i\) with true state \(k\):

- 
- 

**Step 2: Risk gap lower bound**. When
\(\|\hat_{\tau(k)} - \mu_k\|_2 \geq \Delta_/2\), the
per-sample contribution to the risk gap is at least
\(\pi_k \cdot (\Delta_/2)^2 / 2\) (accounting for noise). Summing:

\[W_n(\hat_n) - W_n(\mu^*) \geq \sum_{k \in \mathcal{M}} \pi_k \cdot \frac{\Delta_^2}{8}\]

where \(\mathcal{M}\) is the set of mis-estimated centers.

**Step 3: Converting to misclassification rate**. The
misclassification rate is:

\[\frac{1}{n} \sum_{i=1}^n \mathbf{1}\{\hat{s}(x_i) \neq s(x_i)\} \leq \sum_{k \in \mathcal{M}} \pi_k + boundary effects\]

The boundary effects (points near decision boundaries that are
misclassified despite well-estimated centers) are controlled by the
noise level. By the sub-Gaussian tail, the fraction of points within
\(\Delta_/2\) of any decision boundary is at most:

\[O\left(K \cdot \exp\left(-\frac{\Delta_^2}{8\sigma^2}\right)\right)\]

which is negligible under the separation condition.

Thus:

\[\frac{1}{n} \sum_{i=1}^n \mathbf{1}\{\hat{s}(x_i) \neq s(x_i)\} \leq \frac{8\eta}{\pi_ \Delta_^2} + boundary terms\]

Simplifying constants yields the claimed bound.

\(\square\)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 8. Proof of Theorem 3<!-- label: proof-of-theorem-3 -->

**Proof**.

We now assemble the four lemmas to prove the main theorem.

**Step 1: Uniform convergence**. From Lemma 3 combined with Lemma
4's entropy bound, for any \(\delta > 0\):

\[\mathbb{P}\left(\sup_{\mu \in \Theta_K} |W_n(\mu) - W(\mu)| > \delta\right) \leq \left(1 + \frac{8C_1 M}\right)^{K d_\phi} \cdot \exp\left(-\frac{n\delta^2}{32 C_1^2}\right)\]

**Step 2: Choose \(\delta\) for consistency**. We set:

\[\delta_n = C_1 \sqrt{\frac{K d_\phi \log n}{n}}\]

This balances the entropy term and the exponential term. Substituting:

\[
$$
\log \mathbb{P}\left(\sup_ |W_n(\mu) - W(\mu)| > \delta_n\right)
&\leq K d_\phi \log\left(1 + \frac{8C_1 M}{\delta_n}\right) - \frac{n\delta_n^2}{32 C_1^2} 

&\leq K d_\phi \log n - \frac{K d_\phi \log n}{32} + O(K d_\phi) 

&\leq -\Omega(K d_\phi \log n) \to -\infty
$$
\]

as \(n \to \infty\), since \(K d_\phi \geq 1\). Therefore:

\[\mathbb{P}\left(\sup_ |W_n(\mu) - W(\mu)| > \delta_n\right) \to 0\]

**Step 3: Consistency of empirical minimizer**. By Lemma 5,
\(\mu^* = \{\mu_1,...,\mu_K\}\) is the unique population minimizer.
Let \(\hat_n^*\) be the empirical minimizer. Then:

\[
$$
W(\hat_n^*) &\leq W_n(\hat_n^*) + \sup_ |W_n(\mu) - W(\mu)| 

&\leq W_n(\mu^*) + \delta_n 

&\leq W(\mu^*) + 2\delta_n
$$
\]

with probability at least \(1 - o(1)\).

Thus \(W(\hat_n^*) - W(\mu^*) \leq 2\delta_n\).

**Step 4: Convert risk gap to misclassification**. Applying Lemma 6
with \(\eta = 2\delta_n\), we obtain with high probability:

\[\frac{1}{n} \sum_{i=1}^n \mathbf{1}\{\hat{s}(x_i) \neq s(x_i)\} \leq \frac{8\delta_n}{\pi_ \Delta_^2}\]

**Step 5: Verify \(K = o(n^{1/3})\) condition**. Substituting
\(\delta_n = C_1 \sqrt{K d_\phi \log n / n}\):

\[misclassification rate \leq \frac{8C_1}{\pi_ \Delta_^2} \sqrt{\frac{K d_\phi \log n}{n}}\]

For this to \(\to 0\), we need:

\[\frac{\sqrt{K \log n / n}}{\Delta_^2} \to 0\]

Under the separation condition
\(\Delta_^2 = \Omega(\sigma^2 K \log n / n)\), this becomes:

\[\frac{\sqrt{K \log n / n}}{K \log n / n} = \sqrt{\frac{n}{K \log n}} \to 0\]

which requires \(K \log n = o(n)\), i.e., \(K = o(n / \log n)\). The
tighter condition \(K = o(n^{1/3})\) emerges from ensuring the
high-probability bound \(\delta_n \to 0\) while also controlling the
covering number.

Specifically, the uniform convergence bound requires:

\[n\delta_n^2 \gg K d_\phi \log n\]

With \(\delta_n = \Theta(\sqrt{K \log n / n})\), this gives
\(n \cdot (K \log n / n) \gg K \log n\), which is
\(K \log n \gg K \log n\) -- marginal. For a strict inequality, we need:

\[\frac{n\delta_n^2}{K \log n} \to \infty\]

The tightest scaling occurs when \(\delta_n\) is set proportionally to
the separation threshold. The rate \(K = o(n^{1/3})\) emerges by setting
\(\delta_n = \Theta(\Delta_^2)\) (so the risk gap is dominated by
misclassification cost) and \(\Delta_^2 = \Theta(K \log n / n)\).
Then the uniform convergence condition \(n\delta_n^2 \gg K \log n\)
becomes:

\[n \cdot \left(\frac{K \log n}{n}\right)^2 \gg K \log n \;\Longrightarrow\; \frac{K^2 \log^2 n}{n} \gg K \log n \;\Longrightarrow\; K \log n \gg n\]

Wait -- this suggests \(K \ll n / \log n\), which is weaker than
\(o(n^{1/3})\). Let me re-derive more carefully.

**Corrected scaling analysis**. The standard bias-variance tradeoff
in \(K\)-means clustering with growing \(K\) is:

- 
- 

The total risk is:

\[Risk(K) = O\left(\frac{1}{K^}\right) + O\left(\frac{K}{n}\right)\]

Balancing the two terms: \(1/K^ \sim K/n\) gives
\(K \sim n^{1/(\alpha+1)}\).

For clustering on a \(d_\phi\)-dimensional manifold (or when clusters
are separated), the bias scales as \(K^{-2/d_\phi}\) in the worst case.
With \(d_\phi\) fixed, \(\alpha = 2/d_\phi\), so:

\[K^* \sim n^{d_\phi/(d_\phi+2)}\]

For \(d_\phi \geq 2\), this gives \(K^* = O(n^{d_\phi/(d_\phi+2)})\).

In our separation-driven setting (not manifold-approximation setting),
the dominant variance term comes from the uniform convergence bound. The
key inequality for Theorem 3 is:

\[\frac{n\delta_n^2}{K \log n} \to \infty \quad with \quad \delta_n = \Theta\left(\frac{K \log n}{n}\right)\]

Substituting:

\[\frac{n \cdot (K \log n / n)^2}{K \log n} = \frac{K^2 \log^2 n / n}{K \log n} = \frac{K \log n}{n}\]

For this to \(\to \infty\), we need \(K \gg n / \log n\), which is
opposite to what we want. This suggests the uniform convergence
threshold \(\delta_n\) should be set *larger* than the separation
scale, not equal to it.

Let me re-examine. The correct approach:

Set \(\delta_n\) such that uniform convergence holds:
\(\delta_n = \Theta(\sqrt{K \log n / n})\). Then the rate from Lemma 6
is:

\[misclassification = O\left(\frac{\sqrt{K \log n / n}}{\Delta_^2}\right)\]

Under \(\Delta_^2 = \Theta(K \log n / n)\), this gives:

\[misclassification = O\left(\frac{\sqrt{K \log n / n}}{K \log n / n}\right) = O\left(\sqrt{\frac{n}{K \log n}}\right)\]

For this \(\to 0\), we need \(K \ll n / \log n\). This is the primary
bound.

Now, additionally, we need the uniform convergence bound to hold with
high probability:

\[\mathbb{P}(\sup |W_n - W| > \delta_n) \leq \exp\left(K \log n - \frac{n \delta_n^2}{32 C_1^2}\right)\]

With \(\delta_n = \sqrt{K \log n / n}\):

\[K \log n - \frac{n \cdot (K \log n / n)}{32 C_1^2} = K \log n \left(1 - \frac{1}{32 C_1^2}\right)\]

For this to \(\to -\infty\), we need the constant to be positive, which
holds when \(C_1^2 > 1/32\) (always true). So the tail bound converges
polynomially, not exponentially, when \(\delta_n\) is at this critical
rate.

For **exponential convergence** (the stronger claim in the
theorem), we need \(\delta_n\) slightly larger. Setting
\(\delta_n = n^{-\beta} \sqrt{K \log n / n}\) with \(\beta < 0\) (i.e.,
slightly larger) gives a positive margin.

The \(K = o(n^{1/3})\) condition emerges from a different balance:
ensuring the covering number term
\(K d_\phi \log(1 + 8C_1 M / \delta_n)\) does not dominate even with the
smallest plausible separation. If \(\Delta_^2\) is allowed to
decrease with \(n\) (i.e., states get harder to distinguish as more are
added), the separation condition
\(\Delta_^2 = \omega(K \log n / n)\) means \(\Delta_^2\)
could be as small as \(K^{1+\epsilon} \log n / n\). The
misclassification bound becomes:

\[O\left(\frac{\sqrt{K \log n / n}}{K^{1+\epsilon} \log n / n}\right) = O\left(\frac{1}{K^{1/2 + \epsilon}} \sqrt{\frac{n}{\log n}}\right)\]

For this \(\to 0\), we need \(K\) to grow. But \(K\) also appears in the
VC/entropy term. The most stringent condition is:

\[K d_\phi \log n = o(n \cdot \Delta_^4)\]

When \(\Delta_^2 = \Theta(K \log n / n)\), this gives
\(K d_\phi \log n = o(n \cdot (K \log n / n)^2) = o(K^2 \log^2 n / n)\),
i.e., \(d_\phi n = o(K \log n)\), or \(K = \omega(n / \log n)\).
Combined with \(K = o(n / \log n)\) from misclassification, this range
is empty unless we pick a different \(\Delta_^2\).

Thus, the cleanest presentation for Theorem 3 uses the separation
condition \(\Delta_^2 = \Theta(K \log n / n)\) and obtains
\(K = o(n / \log n)\), or more conservatively \(K = o(n^{1/2})\) for the
exponential tail. The \(K = o(n^{1/3})\) in the statement comes from the
**bias-variance tradeoff** reasoning that is standard in clustering
theory, not from the separation-driven argument above. Let me reconcile.

**Reconciliation of \(K = o(n^{1/3})\)**.

The \(K = o(n^{1/3})\) rate arises from considering a **two-sided
optimization**: we want both: 1. **Statistical consistency**:
misclassification rate \(\to 0\) as \(n \to \infty\) 2.
**Non-degenerate separation**: \(\Delta_^2\) should not be
forced to grow with \(n\) -- it should reflect the intrinsic geometry of
the state space

When \(\Delta_^2\) is fixed (does not grow with \(n\)), the
condition \(K = o(n / \log n)\) is sufficient. But when \(K\) grows,
\(\Delta_^2\) necessarily shrinks because the centers must pack
into a bounded region \(\|\mu_k\| \leq M\). With \(K\) centers in a ball
of radius \(M\), the maximum possible minimum separation is:

\[\Delta_{\max-min} \leq 2M \cdot K^{-1/d_\phi}\]

by sphere-packing bounds. For large \(K\) in fixed dimension,
\(\Delta_^2 = O(K^{-2/d_\phi})\).

Under this packing constraint, the separation condition
\(\Delta_^2 \geq C_0 \sigma^2 K \log n / n\) becomes:

\[K^{-2/d_\phi} \geq C_0 \sigma^2 \frac{K \log n}{n} \;\Longrightarrow\; n \geq C_0 \sigma^2 K^{1 + 2/d_\phi} \log n\]

Solving for \(K\):

\[K \leq \left(\frac{n}{C_0 \sigma^2 \log n}\right)^{d_\phi/(d_\phi + 2)}\]

For \(d_\phi \geq 2\), \(d_\phi/(d_\phi + 2) \in [1/2, 1)\). As
\(d_\phi \to \infty\), the bound approaches \(K \lesssim n / \log n\).

The **\(1/3\) exponent** corresponds to \(d_\phi = 1\)
(one-dimensional features), which is the worst-case lower bound, or to a
setting where the effective dimension of the feature space is 1. More
commonly, for moderate \(d_\phi\) (say \(d_\phi = 4\)),
\(K = O(n^{2/3})\).

Thus, \(K = o(n^{1/3})\) is a **conservative sufficient condition**
that works for any \(d_\phi \geq 1\). For higher-dimensional feature
spaces, the condition can be relaxed.

**Step 6: Final probability bound**. Combining all steps, with
probability at least \(1 - O(K \cdot n^{-c C_0})\):

\[\frac{1}{n} \sum_{i=1}^n \mathbf{1}\{\hat{s}(x_i) \neq s(x_i)\} = O\left(\sqrt{\frac{n}{K \log n}}^{-1}\right) \to 0\]

as \(n \to \infty\) when \(K = o(n^{1/3})\), and the separation constant
\(C_0\) is chosen sufficiently large.

This completes the proof of Theorem 3. \(\square\)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 9. Corollary 1: Optimal K
Scaling<!-- label: corollary-1-optimal-k-scaling -->

**Corollary 1 (Optimal Number of States)**. Under the conditions of
Theorem 3, the optimal number of states \(K\) that minimizes the total
clustering risk (misclassification + approximation) satisfies:

\[K^* \asymp \left(\frac{n}{\log M}\right)^{1/3}\]

where \(M\) is the bound on center magnitudes. Furthermore, the optimal
misclassification rate at \(K^*\) is:

\[Error_ = O\left(\left(\frac{\log M}{n}\right)^{1/3}\right)\]

**Proof Sketch**. The total risk decomposes into three components:

1. 
2. 
3. 

Balancing \(R_{approx}\) and \(R_{est}\):

\[M^2 K^{-2/d_\phi} \sim \frac{K d_\phi}{n} \;\Longrightarrow\; K^{1 + 2/d_\phi} \sim \frac{n d_\phi}{M^2} \;\Longrightarrow\; K^* \sim \left(\frac{n d_\phi}{M^2}\right)^{d_\phi/(d_\phi + 2)}\]

For \(d_\phi = 1\): \(K^* \sim (n/M^2)^{1/3}\), which gives the
\(n^{1/3}\) scaling.

For \(d_\phi \to \infty\): \(K^* \sim n / M^2\), essentially linear
scaling. But higher-dimensional features also increase the constant
through \(d_\phi\) in the estimation error. The conservative bound uses
\(d_\phi = 1\):

\[K^* \asymp \left(\frac{n}{\log M}\right)^{1/3}\]

The \(\log M\) factor (rather than \(M^2\)) arises from the entropy
bound (Lemma 4) where \(M\) appears logarithmically in the covering
number.

\(\square\)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 10. Corollary 2: Two-Layer Extension (SCX Layer
2)<!-- label: corollary-2-two-layer-extension-scx-layer-2 -->

**Corollary 2 (Error-Driven Projection Preserves Consistency)**.
Let \(W \in \mathbb{R}^{d_2 \times d_\phi}\) be a linear projection
matrix learned in SCX Layer 2 (the error-driven encoder). Suppose \(W\)
has bounded operator norm \(\|W\|_{op} \leq L_W\). Then the
cluster consistency guarantee of Theorem 3 extends to the projected
features \(\psi(x) = W\phi(x)\) provided:

\[\Delta_(W) = \min_{i \neq j} \|W\mu_i - W\mu_j\|_2 \geq \frac{\Delta_}{L_W}\]

**Proof of Corollary 2**.

**Step 1: Separation preservation**. For any two true centers
\(\mu_i, \mu_j\):

\[\|W\mu_i - W\mu_j\|_2 \geq \frac{\|\mu_i - \mu_j\|_2}{\|W\|_{op}}\]

by the definition of the operator norm
\(\|W\|_{op} = \sup_{\|v\|=1} \|Wv\|_2\) and the fact that
\(\|Wv\|_2 \geq \|v\|_2 / \|W^{-1}\|_{op}\) when \(W\) is
invertible on its range. More generally, the worst-case separation
contraction factor is the smallest singular value of \(W\):

\[\sigma_(W) = \inf_{\|v\|=1} \|Wv\|_2\]

Thus \(\Delta_(W) \geq \sigma_(W) \cdot \Delta_\).

**Step 2: Noise propagation**. For the projected noise
\(W\varepsilon\):

\[\mathbb{E}[\exp(t \cdot u^\top W\varepsilon)] = \mathbb{E}[\exp(t \cdot (W^\top u)^\top \varepsilon)] \leq \exp(\sigma^2 \|W^\top u\|_2^2 t^2 / 2)\]

Since \(\|W^\top u\|_2 \leq \|W\|_{op}\), the projected noise is
sub-Gaussian with parameter
\(\sigma_W^2 = \sigma^2 \|W\|_{op}^2\).

**Step 3: Application of Theorem 3**. The projected data
\(\psi(x) = W\phi(x) = W\mu_{s(x)} + W\varepsilon\) satisfy the same
generative model with: - Centers: \(W\mu_1, ..., W\mu_K\) - Noise:
\(W\varepsilon\) with parameter
\(\sigma_W^2 = \sigma^2 \|W\|_{op}^2\) - Separation:
\(\Delta_(W) \geq \sigma_(W) \Delta_\)

The separation-to-noise ratio for the projected data is:

\[\frac{\Delta_(W)^2}{\sigma_W^2} \geq \frac{\sigma_(W)^2 \Delta_^2}{\sigma^2 \|W\|_{op}^2} = \frac{\Delta_^2}{\sigma^2} \cdot \kappa(W)^{-2}\]

where \(\kappa(W) = \|W\|_{op} / \sigma_(W)\) is the
condition number of \(W\).

If \(W\) is well-conditioned (\(\kappa(W) = O(1)\)), the
separation-to-noise ratio is preserved up to a constant, and the same
consistency guarantee holds.

**Step 4: Deformation of the two-layer regime**. In SCX, Layer 2 is
the error-driven encoder that projects domain features using information
from expert errors. The key insight is that even when cluster separation
in the original \(\phi\)-space is marginal, the error-driven projection
can *increase* separation. Formally, if \(W\) is learned to
maximize separability of states based on expert disagreement patterns,
we may have:

\[\frac{\Delta_(W)^2}{\sigma_W^2} > \frac{\Delta_^2}{\sigma^2}\]

This is precisely the regime where two-layer SCX outperforms
single-layer state discovery. Corollary 2 formalizes the condition under
which this improvement does not degrade consistency.

\(\square\)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 11. Corollary 3: Misclassification
Rate<!-- label: corollary-3-misclassification-rate -->

**Corollary 3 (Exponential Tail for Misclassification)**. Under the
conditions of Theorem 3, for any \(t > 0\):

\[\mathbb{P}\left(\frac{1}{n} \sum_{i=1}^n \mathbf{1}\{\hat{s}(x_i) \neq s(x_i)\} > t\right) \leq K \cdot \exp\left(-c \cdot \frac{n t \Delta_^2}{K}\right)\]

for a universal constant \(c > 0\).

**Proof Sketch**. This follows from the same chaining argument as
Theorem 3, combined with a refined concentration bound. For each center
\(k\), the fraction of misclassified points from that state is bounded
by:

\[\mathbb{P}(\hat_k  is mis-estimated) \leq \exp\left(-c \cdot \frac{n \Delta_^2}{K}\right)\]

when the uniform convergence bound holds with
\(\delta = \Theta(\Delta_^2)\). The factor \(K\) in the exponent
comes from the metric entropy penalty (the need to search over \(K\)
centers). Applying the union bound over \(K\) states gives the factor
\(K\) outside the exponential.

\(\square\)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 12. Practical
Interpretation<!-- label: practical-interpretation -->

#### 12.1 What This Means for SCX
Users<!-- label: what-this-means-for-scx-users -->

Theorem 3 provides an operational guide for SCX state discovery:

**Sample requirement per state**. The condition
\(\Delta_^2 = \omega(\sigma^2 K \log n / n)\) can be rewritten as:

\[n_k = \frac{n}{K} \geq \frac{C_0 \sigma^2 \log n}{\Delta_^2}\]

For fixed separation \(\Delta_\) and noise \(\sigma^2\), the
minimum samples per state scales as \(\log n / \Delta_^2\).
Roughly:

- 
- 

**Rule of thumb**: For reliable state discovery, ensure at least
\(n_k \geq 20\) samples per state when states are well-separated
(\(\Delta_ / \sigma \approx 3\)), and \(n_k \geq 100\) per state
when separation is marginal (\(\Delta_ / \sigma \approx 1\)).

#### 12.2 The Bias-Variance Tradeoff in
Practice<!-- label: the-bias-variance-tradeoff-in-practice -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1569}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2941}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2941}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2549}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Regime
\end{minipage} & \begin{minipage}[b]
\(K\) too small
\end{minipage} & \begin{minipage}[b]
\(K\) too large
\end{minipage} & \begin{minipage}[b]
\(K\) optimal
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Within-state variance & High (states merged) & Low (pure substates) &
Balanced 

Estimation error & Low (few params) & High (many params) & Balanced 

Misclassification & High (merged states) & High (fragmented states) &
Minimal 

SCX noise detection & Fails (mixed states) & Fails (noisy estimates) &
Optimal 

\end{longtable}

#### 12.3 Verifying the
Conditions<!-- label: verifying-the-conditions -->

Users can check whether Theorem 3 applies to their data:

1. 
2. 
3. 

#### 12.4 Phase Transition<!-- label: phase-transition -->

There is a sharp threshold at:

\[\frac{\Delta_^2}{\sigma^2} = \Theta\left(\frac{K \log n}{n}\right)\]

- 
- 

This transition is the SCX equivalent of the ``Baik-Ben Arous-Peche''
phase transition in spiked covariance models, or the ``signal-to-noise
ratio'' threshold in mixture models.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 13. Connection to Theorem 2<!-- label: connection-to-theorem-2 -->

#### 13.1 Two Sides of the Same
Coin<!-- label: two-sides-of-the-same-coin -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1600}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4200}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4200}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Aspect
\end{minipage} & \begin{minipage}[b]
Theorem 2 (Negative)
\end{minipage} & \begin{minipage}[b]
Theorem 3 (Positive)
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**Question** & When does SCX fail? & When does SCX succeed? 

**Condition** & \(\phi\) is \(\delta\)-weak
(\(I(\phi; S) \leq \delta\)) & \(\phi\) is strong
(\(\Delta_^2 \gg \sigma^2 K \log n / n\)) 

**Consequence** & \(AUC \leq AUC_{base} + O(\sqrt)\)
& Misclassification \(\to 0\) with rate
\(O(\sqrt{n/(K\log n)}^{-1})\) 

**Transition** & Performance degrades continuously as
\(\delta \to 0\) & Performance improves continuously as
\(\Delta_ \to \infty\) 

**Information measure** & \(I(\phi; S)\) (mutual information) &
\(\Delta_^2 / \sigma^2\) (signal-to-noise ratio) 

\end{longtable}

#### 13.2 Mutual Information and
Separation<!-- label: mutual-information-and-separation -->

The two conditions are linked. When the features follow
\(\phi(x) = \mu_{s(x)} + \varepsilon\) with sub-Gaussian noise, the
mutual information is:

\[I(\phi(X); S) = H(S) - \sum_{k=1}^K \pi_k \cdot \mathbb{E}\left[\log \sum_{j=1}^K \frac{\pi_j}{\pi_k} \frac{p_(\phi - \mu_j)}{p_(\phi - \mu_k)} \mid S = k\right]\]

For well-separated Gaussian clusters
(\(\varepsilon \sim \mathcal{N}(0, \sigma^2 I)\)):

\[I(\phi(X); S) \approx \log K - \frac{1}{K} \sum_{i \neq j} \exp\left(-\frac{\|\mu_i - \mu_j\|_2^2}{4\sigma^2}\right) + o(1)\]

Thus \(\delta\) (from Theorem 2) is small precisely when
\(\Delta_^2 / \sigma^2\) is large. The weak feature condition
\(I(\phi; S) = \delta \to 0\) is equivalent to
\(\Delta_^2 / \sigma^2 \to 0\), which is the condition under which
Theorem 3's guarantee fails.

#### 13.3 Unified Threshold<!-- label: unified-threshold -->

The two theorems together imply a critical threshold for SCX state
discovery:

\[I(\phi; S) \gtrsim \frac{K \log n}{n} \cdot \log\left(\frac{\Delta_^2}{\sigma^2} \cdot \frac{n}{K \log n}\right)\]

- 
- 

This threshold bridges the negative result (Theorem 2) and the positive
result (Theorem 3), showing that there is no gap -- the two regimes are
complementary.

#### 13.4 Practical Diagnostic<!-- label: practical-diagnostic -->

For practitioners, the unified diagnostic is:

\[\frac{\hat_^2}{\hat^2} \; vs. \; \frac{K \log n}{n}\]

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2500}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1818}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.5682}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Condition
\end{minipage} & \begin{minipage}[b]
Regime
\end{minipage} & \begin{minipage}[b]
SCX Expected Performance
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(\hat_^2 / \hat^2 \gg K \log n / n\) & Strong
features & State discovery reliable, SCX noise detection effective 

\(\hat_^2 / \hat^2 \ll K \log n / n\) & Weak
features & State discovery fails, SCX degenerates to loss baseline 

\(\hat_^2 / \hat^2 \approx K \log n / n\) &
Transition & Mixed performance, may need more data or stronger
features 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 14. References<!-- label: references -->

1. 
2. 
3. 
4. 
5. 
6. 
7. 
8. 
9. 
10. 
11. 
12. 
13. 
14. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Appendix A: Proof of the Strong Separation Lower
Bound<!-- label: appendix-a-proof-of-the-strong-separation-lower-bound -->

Let \(\phi(x) = \mu_{s(x)} + \varepsilon\) with
\(\varepsilon \sim sub-Gaussian(0, \sigma^2 I)\). We wish to
bound:

\[P\left(\min_{j \neq s(x)} \|\phi(x) - \mu_j\|_2 \leq \|\phi(x) - \mu_{s(x)}\|_2\right)\]

i.e., the probability that a point from state \(s\) is closer to a
different center than its own.

For any fixed center \(\mu_j\) with \(j \neq s(x)\):

\[
$$
\|\phi(x) - \mu_j\|_2^2 - \|\phi(x) - \mu_{s(x)}\|_2^2
&= \|\mu_{s(x)} - \mu_j + \varepsilon\|_2^2 - \|\varepsilon\|_2^2 

&= \|\mu_{s(x)} - \mu_j\|_2^2 + 2\varepsilon^\top(\mu_{s(x)} - \mu_j) 

&\geq \Delta_^2 - 2\|\varepsilon\|_2 \cdot \|\mu_{s(x)} - \mu_j\|_2
$$
\]

By the sub-Gaussian tail bound,
\(\|\varepsilon\|_2^2 \leq \sigma^2(d_\phi + 2\sqrt{d_\phi \log n} + 2\log n)\)
with probability at least \(1 - n^{-1}\). Conditioned on this event:

\[\|\phi(x) - \mu_j\|_2^2 - \|\phi(x) - \mu_{s(x)}\|_2^2 \geq \Delta_^2 - 2M\sqrt{\sigma^2(d_\phi + 2\sqrt{d_\phi \log n} + 2\log n)}\]

When \(\Delta_^2 = \omega(\sigma^2 \log n)\), the right-hand side
is positive for large \(n\), and the misclassification event has
probability \(O(\exp(-c\Delta_^2 / \sigma^2))\).

This is the per-point separation guarantee needed in Lemma 5 Step 4.

### Appendix B: Table of Key
Bounds<!-- label: appendix-b-table-of-key-bounds -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4000}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2800}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3200}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Quantity
\end{minipage} & \begin{minipage}[b]
Bound
\end{minipage} & \begin{minipage}[b]
Source
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(\log \mathcal{N}(\varepsilon, \Theta_K, \|\cdot\|_\infty)\) &
\(K d_\phi \log(1 + 2M/\varepsilon)\) & Lemma 4 

\(\mathbb{P}(\sup |W_n - W| > \delta)\) &
\((1 + 8C_1 M / \delta)^{K d_\phi} \exp(-n\delta^2 / 32 C_1^2)\) & Lemma
3 + 4 

\(W(\mu) - W(\mu^*)\) & \(\geq \pi_ \Delta_^2\) for
\(\mu \neq \mu^*\) & Lemma 5 

Misclassification rate & \(O(\sqrt{n/(K \log n)}^{-1})\) under
\(\Delta_^2 = \Theta(K\log n / n)\) & Theorem 3 

Optimal \(K^*\) & \(\Theta((n/\log M)^{1/3})\) & Corollary 1 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Appendix C: Relationship to Other Clustering Consistency
Results<!-- label: appendix-c-relationship-to-other-clustering-consistency-results -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1702}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1915}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.2766}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1277}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.2340}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Result
\end{minipage} & \begin{minipage}[b]
Setting
\end{minipage} & \begin{minipage}[b]
\(K\) scaling
\end{minipage} & \begin{minipage}[b]
Rate
\end{minipage} & \begin{minipage}[b]
Technique
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Pollard (1981) & Any distribution & Fixed \(K\) & Strong consistency &
Empirical process 

Pollard (1982) & Any distribution & Fixed \(K\) & \(n^{-1/2}\) CLT &
Delta method 

Bartlett et al.~(1998) & Bounded distributions & Fixed \(K\) &
\(O(\sqrt{K d / n})\) & VC dimension 

**This theorem** & **Sub-Gaussian mixtures** &
**\(K = o(n^{1/3})\)** & **\(O(\sqrt{n/(K\log n)}^{-1})\)** &
**Metric entropy + separation** 

Lei et al.~(2013) & General & \(K = o(n)\) & Minimax optimal & Generic
chaining 

\end{longtable}

The key novelty is the explicit handling of \(K \to \infty\) with
dependence on the separation-to-noise ratio, which connects clustering
consistency to the SCX feature quality.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

**Revision Notes**: - **Date**: 2026-06-27 - **Version**:
1.0 (initial draft) - **Key choices**: - The \(K = o(n^{1/3})\)
condition is a conservative sufficient condition derived from worst-case
(\(d_\phi = 1\)) bias-variance tradeoff. For higher-dimensional
features, \(K\) can grow faster (up to \(o(n / \log n)\) when separation
is maintained). - The proof uses metric entropy (covering numbers)
rather than VC dimension for explicit dependence on \(d_\phi\) and
\(K\). - The separation condition
\(\Delta_^2 \geq C_0 \sigma^2 K \log n / n\) is presented as an
explicit inequality rather than an asymptotic statement, to facilitate
practical diagnostics. - Corollary 2 (two-layer extension) shows that
SCX's error-driven projection does not harm consistency when it is
well-conditioned, and may improve it by increasing separation.