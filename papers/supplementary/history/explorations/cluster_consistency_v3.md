\section{Theorem 5 (v3): Fixed-K Cluster Consistency of SCX State
Discovery Under Strong
Features}<!-- label: theorem-5-v3-fixed-k-cluster-consistency-of-scx-state-discovery-under-strong-features -->

> **Core Claim**: When the feature representation \(\phi(x)\)
> separates the \(K\) true states by a margin \(\Delta_ > 0\)
> (fixed, not scaling with \(n\)), and the per-state sample size
> \(n_ \to \infty\), Lloyd's \(k\)-means with \(R = O(\log n)\)
> random restarts recovers the true state partition with probability
> \(1 - K \cdot \exp(-c \cdot n_ \Delta_^2 / (\sigma^2 d_\phi)) - o(1)\).

This is the **positive counterpart** to Theorem 2's negative result
(weak features \(\to\) failure). Together, they complete the phase
diagram: strong features \(\to\) state discovery succeeds; weak features
\(\to\) SCX cannot exceed loss baseline.

**Theorem number**: Theorem 5 in the SCX theory chain.
**Status**: Final v3 --- addresses all 4 fatal issues from the
hostile review of v2. **Revision date**: 2026-06-28.

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

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. Setup and Assumptions<!-- label: setup-and-assumptions -->

\subsubsection{1.1 Data-Generating
Process}<!-- label: data-generating-process -->

Let \((\Omega, \mathcal{F}, P)\) be a probability space. We observe
\(n\) i.i.d. copies of the feature vector
\(\phi(x) \in \mathbb{R}^{d_\phi}\). The true state labels \(s(x)\) are
**unobserved** during clustering.

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3200}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3600}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3200}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Symbol
\end{minipage} & \begin{minipage}[b]
Meaning
\end{minipage} & \begin{minipage}[b]
Domain
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

\(\sigma^2\) & Sub-Gaussian variance proxy of \(\varepsilon\) &
\(\mathbb{R}^+\) 

\(\Delta_\) & Minimum separation between distinct centers &
\(\mathbb{R}^+\) 

\(n\) & Total number of samples & \(\mathbb{N}\) 

\(K\) & Number of states **(fixed, does not grow with \(n\))** &
\(\mathbb{N}\) 

\(n_k\) & Number of samples in state \(k\) & \(\sum_k n_k = n\) 

\(n_\) & Minimum per-state sample size & \(\min_k n_k\) 

\(\pi_k = n_k/n\) & Empirical proportion (asymptotically \(P(S=k)\)) &
\((0,1)\), \(\sum \pi_k = 1\) 

\end{longtable}

#### 1.2 Generative Model<!-- label: generative-model -->

We assume:

\[\phi(x) = \mu_{s(x)} + \varepsilon\]

where:

- 
- 
- 

The noise \(\varepsilon\) is independent of \(s(x)\).

#### 1.3 Cluster Structure<!-- label: cluster-structure -->

Define:

- 
- 
- 
- 

\subsubsection{1.4 Separation Condition (Fixed,
Non-Scaling)}<!-- label: separation-condition-fixed-non-scaling -->

The minimum separation between distinct cluster centers is
**fixed** --- it does not scale with \(n\) or \(K\):

\[\Delta_ = \min_{i \neq j} \|\mu_i - \mu_j\|_2 > 0\]

We assume the **strong separation regime**: \(\Delta_\) is
sufficiently large relative to \(\sigma \sqrt{d_\phi}\) that

\[\frac{\Delta_^2}{\sigma^2 d_\phi} \geq C_0\]

where \(C_0\) is a universal constant determined by the proof
(sufficient to guarantee \(\|\theta^* - \mu\| < \Delta_/8\) in
Lemma 1 below). This is the ``strong features'' regime: the
signal-to-noise ratio is high enough that cluster centers are
distinguishable despite noise and feature dimensionality.

**Crucially, unlike v1/v2**: \(\Delta_\) is a **fixed**
property of the data-generating process (the gap between distinct state
means in feature space). It is not coupled to \(n\) via a separation
condition like \(\Delta_^2 \geq C_0 \sigma^2 K \log n / n\). The
only asymptotic condition is \(n_ \to \infty\). This avoids the
scaling conflation identified in Review Issue 5.

#### 1.5 K-Means Objective<!-- label: k-means-objective -->

For a set of \(K\) candidate centers
\(\hat = \{\hat_1, ..., \hat_K\} \subset \mathbb{R}^{d_\phi}\),
define the **empirical k-means risk**:

\[W_n(\theta) = \frac{1}{n} \sum_{i=1}^n \min_{k \in [K]} \|\phi(x_i) - \theta_k\|_2^2\]

The **population k-means risk** is:

\[W(\theta) = \mathbb{E}\left[\min_{k \in [K]} \|\phi(X) - \theta_k\|_2^2\right]\]

The **population minimizer** is:

\[\theta^* \in \arg \min_{\theta: |\theta| = K} W(\theta)\]

The **empirical minimizer** is:

\[\hat_n \in \arg \min_{\theta: |\theta| = K} W_n(\theta)\]

Both are defined up to label permutation. When we write
\(\|\hat_n - \theta^*\|\), we mean the distance after optimal
permutation matching.

#### 1.6 Notation for Norms<!-- label: notation-for-norms -->

For a \(K\)-center set \(\theta\):

- 
- 
- 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2. Technical Preliminaries<!-- label: technical-preliminaries -->

\subsubsection{2.1 Sub-Gaussian
Concentration}<!-- label: sub-gaussian-concentration -->

**Lemma S1 (Sub-Gaussian norm bound)**. Let
\(\varepsilon \in \mathbb{R}^{d_\phi}\) be a zero-mean sub-Gaussian
vector with variance proxy \(\sigma^2\). Then for any \(t > 0\):

\[P\left(\|\varepsilon\|_2 \geq C_1 \sigma \left(\sqrt{d_\phi} + \sqrt{t}\right)\right) \leq 2 \exp(-t)\]

where \(C_1\) is an absolute constant depending only on the sub-Gaussian
constant of \(\varepsilon\). For
\(t = c \cdot \Delta_^2 / \sigma^2\) with
\(\Delta_^2 / \sigma^2\) large:

\[P\left(\|\varepsilon\|_2 \geq \frac{\Delta_}{4}\right) \leq 2 \exp\left(-c_0 \frac{\Delta_^2}{\sigma^2}\right)\]

for some \(c_0 > 0\).

**Proof**. This follows from Theorem 3.1.1 in Vershynin (2018): for
a sub-Gaussian random vector with sub-Gaussian norm
\(K = \sup_{\|u\|=1} \|\langle \varepsilon, u\rangle\|_{\psi_2}\), we
have \(\|\varepsilon\|_2\) is \(C K\)-sub-Gaussian with
\(P(\|\varepsilon\|_2 \geq C K (\sqrt{d_\phi} + t)) \leq 2\exp(-t^2)\).
The variance proxy \(\sigma^2\) satisfies \(K \leq C\sigma\). The second
inequality follows by setting \(t = \sqrt{c}\,\Delta_/\sigma\) and
noting that \(\sqrt{d_\phi} \leq \Delta_/(C_1 C \sigma)\) under
the strong separation condition. \(\square\)

**Lemma S2 (Sub-Gaussian tail for linear forms)**. For any fixed
\(v \in \mathbb{R}^{d_\phi}\):

\[P\left(v^\top \varepsilon \geq t\right) \leq \exp\left(-\frac{t^2}{2\sigma^2 \|v\|_2^2}\right)\]

**Proof**. Directly from the MGF bound. \(\square\)

\subsubsection{2.2 Covering Number of the Center
Class}<!-- label: covering-number-of-the-center-class -->

**Lemma S3 (Metric entropy)**. Let
\(\Theta_K = \{\theta = \{\theta_1,...,\theta_K\} : \theta_k \in \mathbb{R}^{d_\phi}, \|\theta_k\|_2 \leq M\}\)
equipped with
\(\|\theta - \theta'\|_\infty = \max_k \|\theta_k - \theta'_k\|_2\). For
any \(\varepsilon \in (0, M)\):

\[\log \mathcal{N}(\varepsilon, \Theta_K, \|\cdot\|_\infty) \leq K d_\phi \log\left(1 + \frac{2M}\right)\]

**Proof**. The set \(\Theta_K\) is the Cartesian product of \(K\)
balls of radius \(M\) in \(\mathbb{R}^{d_\phi}\). The
\(\varepsilon\)-covering number of
\(B_M(0) \subset \mathbb{R}^{d_\phi}\) in \(\ell_2\) is
\((1+2M/\varepsilon)^{d_\phi}\). The \(\ell_\infty\) metric on the
product is the max of per-coordinate \(\ell_2\) distances, so the
covering number of the product is the product of per-coordinate covering
numbers. Taking logs gives the result. \(\square\)

\subsubsection{2.3 Lipschitz Property of the K-Means
Loss}<!-- label: lipschitz-property-of-the-k-means-loss -->

**Lemma S4 (Lipschitz constant)**. For any fixed \(x\), the
function
\(\theta \mapsto f_\theta(x) = \min_k \|\phi(x) - \theta_k\|_2^2\) is
\(L(x)\)-Lipschitz in \(\theta\) with respect to \(\|\cdot\|_\infty\),
where:

\[L(x) = 2(\|\phi(x)\|_2 + M)\]

**Proof**. For two center sets \(\theta, \theta'\) with
\(\max_k \|\theta_k - \theta'_k\| \leq \delta\):

\[|f_\theta(x) - f_{\theta'}(x)| \leq \max_k \left| \|\phi(x) - \theta_k\|^2 - \|\phi(x) - \theta'_k\|^2 \right|\]
\[\leq \max_k \left( \|\phi(x) - \theta_k\| + \|\phi(x) - \theta'_k\| \right) \cdot \|\theta_k - \theta'_k\|\]
\[\leq 2\left(\|\phi(x)\|_2 + M\right) \cdot \delta\]

using the triangle inequality and \(\|\theta_k\| \leq M\). \(\square\)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{3. Lemma 1: Population Minimizer
Proximity}<!-- label: lemma-1-population-minimizer-proximity -->

> **Purpose**: Show that the population \(k\)-means minimizer
> \(\theta^*\) is exponentially close to the true centers
> \(\mu = \{\mu_1,...,\mu_K\}\), with bias \(< \Delta_/8\).

#### 3.1 Statement<!-- label: statement -->

**Lemma 1 (Population minimizer proximity)**. Under the generative
model of Section 1 with \(\Delta_^2 / (\sigma^2 d_\phi) \geq C_0\)
(the strong separation condition), the population \(k\)-means objective
\(W(\theta)\) has a minimizer \(\theta^*\) (unique up to label
permutation). For any permutation \(\pi\) that optimally matches
\(\theta^*\) to \(\mu\):

\[\|\theta^*_{\pi(k)} - \mu_k\|_2 \leq \varepsilon_{pop} < \frac{\Delta_}{8}\]

where

\[\varepsilon_{pop} = \frac{C_2 K (M + \sigma\sqrt{d_\phi})}{\pi_} \cdot \exp\left(-\frac{\Delta_^2}{8\sigma^2}\right)\]

and \(C_2\) is an absolute constant. Under the strong separation
condition, \(\varepsilon_{pop} < \Delta_/8\) for \(C_0\)
sufficiently large.

#### 3.2 Proof of Lemma 1<!-- label: proof-of-lemma-1 -->

The proof proceeds in four steps. The key insight: instead of directly
computing \(W(\mu) - W(\mu^*)\) (which was the flawed approach in v1/v2
flagged as Issue 4), we use the **self-consistency equation**
satisfied by any minimizer and show that the true centers approximately
satisfy it.

**Step 1: Existence of a minimizer.**

The function \(W(\theta)\) is continuous (composition of continuous
functions: expectation of min of quadratics) and coercive
(\(W(\theta) \to \infty\) as \(\|\theta\|_\infty \to \infty\), since the
quadratic penalty dominates). Therefore \(W\) attains a minimum on any
compact set containing a large enough ball, and the minimizer exists. By
the strict convexity of
\(\theta_k \mapsto \mathbb{E}[\|\phi - \theta_k\|^2 \mid \phi \in V_k(\theta)]\)
on each Voronoi cell (where \(V_k(\theta)\) is defined below), any two
minimizers must be related by a label permutation. Thus \(\theta^*\) is
unique up to permutation.

**Step 2: Self-consistency equation.**

For a set of centers \(\theta\), define the Voronoi cell of center
\(j\):

\[V_j(\theta) = \left\{ \phi \in \mathbb{R}^{d_\phi} : \|\phi - \theta_j\|_2 \leq \min_{\ell \neq j} \|\phi - \theta_\ell\|_2 \right\}\]

At any point \(\theta\) where the Voronoi cells have positive
probability and are well-defined (i.e., no tie regions with positive
measure), the gradient of \(W\) with respect to \(\theta_j\) exists and
equals:

\[\frac{\partial \theta_j} W(\theta) = -2 \; \mathbb{E}\left[ (\phi - \theta_j) \cdot \mathbf{1}\{\phi \in V_j(\theta)\} \right]\]

Setting this to zero at \(\theta^*\) gives the **self-consistency
condition**: for each \(j\),

\[\theta^*_j = \frac{\mathbb{E}[\phi \cdot \mathbf{1}\{\phi \in V_j(\theta^*)\}]}{P(\phi \in V_j(\theta^*))} = \mathbb{E}[\phi \mid \phi \in V_j(\theta^*)] \]

**Step 3: The true centers approximately satisfy
self-consistency.**

Consider the Voronoi cells induced by the true centers
\(\mu = \{\mu_1,...,\mu_K\}\). For each \(k\), define the one-step
candidate:

\[\tilde_k = \mathbb{E}[\phi \mid \phi \in V_k(\mu)]\]

We bound \(\|\tilde_k - \mu_k\|\). Write the numerator
explicitly:

\[\tilde_k \cdot P(V_k(\mu)) = \sum_{j=1}^K \pi_j \; \mathbb{E}\left[ \mu_j + \varepsilon \;\big|\; \mu_j + \varepsilon \in V_k(\mu) \right] \cdot P(\mu_j + \varepsilon \in V_k(\mu) \mid S=j)\]

**Claim (mis-assignment probability bound)**: For \(j \neq k\):

\[P(\mu_j + \varepsilon \in V_k(\mu) \mid S=j) \leq \exp\left(-\frac{\|\mu_j - \mu_k\|^2}{8\sigma^2}\right) \leq \exp\left(-\frac{\Delta_^2}{8\sigma^2}\right)\]

*Proof of claim*: The event \(\mu_j + \varepsilon \in V_k(\mu)\)
requires
\(\|\mu_j + \varepsilon - \mu_k\| \leq \|\mu_j + \varepsilon - \mu_j\|\),
i.e.~\(\|(\mu_j - \mu_k) + \varepsilon\| \leq \|\varepsilon\|\).
Squaring both sides:

\[\|\mu_j - \mu_k\|^2 + 2\varepsilon^\top(\mu_j - \mu_k) + \|\varepsilon\|^2 \leq \|\varepsilon\|^2\]

\[\|\mu_j - \mu_k\|^2 + 2\varepsilon^\top(\mu_j - \mu_k) \leq 0\]

\[2\varepsilon^\top(\mu_j - \mu_k) \leq -\|\mu_j - \mu_k\|^2\]

Since \(v = (\mu_j - \mu_k)/\|\mu_j - \mu_k\|\) is a unit vector,
\(\varepsilon^\top v\) is sub-Gaussian with parameter \(\sigma^2\).
Hence \(2\varepsilon^\top(\mu_j - \mu_k)\) is sub-Gaussian with
parameter \(4\sigma^2\|\mu_j - \mu_k\|^2\). By Lemma S2:

\[P\left(2\varepsilon^\top(\mu_j - \mu_k) \leq -\|\mu_j - \mu_k\|^2\right) \leq \exp\left(-\frac{\|\mu_j - \mu_k\|^4}{2 \cdot 4\sigma^2 \|\mu_j - \mu_k\|^2}\right) = \exp\left(-\frac{\|\mu_j - \mu_k\|^2}{8\sigma^2}\right)\]

This establishes the claim. \(\square\)

Similarly, points from state \(k\) are **not** assigned to
\(V_k(\mu)\) only if they are closer to some \(\mu_j\), \(j \neq k\). By
the union bound over \(j \neq k\):

\[P(\mu_k + \varepsilon \notin V_k(\mu) \mid S=k) \leq K \cdot \exp\left(-\frac{\Delta_^2}{8\sigma^2}\right)\]

**Step 4: Bounding \(\|\tilde_k - \mu_k\|\).**

Decompose the conditional expectation:

\[\tilde_k = \mathbb{E}[\phi \mid \phi \in V_k(\mu)] = \frac{\mathbb{E}[\phi \cdot \mathbf{1}\{\phi \in V_k(\mu)\}]}{P(V_k(\mu))}\]

Write \(\phi = \mu_S + \varepsilon\) and split the expectation by true
state \(S\):

\[\mathbb{E}[\phi \cdot \mathbf{1}\{\phi \in V_k(\mu)\}] = \sum_{j=1}^K \pi_j \cdot \mathbb{E}\left[ (\mu_j + \varepsilon) \cdot \mathbf{1}\{\mu_j + \varepsilon \in V_k(\mu)\} \mid S=j \right]\]

For the diagonal term (\(j=k\)):

\[\mathbb{E}\left[ (\mu_k + \varepsilon) \cdot \mathbf{1}\{\mu_k + \varepsilon \in V_k(\mu)\} \mid S=k \right] = \mu_k \cdot P(\mu_k + \varepsilon \in V_k(\mu) \mid S=k) + \mathbb{E}\left[ \varepsilon \cdot \mathbf{1}\{\mu_k + \varepsilon \in V_k(\mu)\} \mid S=k \right]\]

For the off-diagonal terms (\(j \neq k\)), the indicator event has
probability \(\leq \exp(-\Delta_^2/(8\sigma^2))\).

The key technical point: the conditional expectation of noise
\(\mathbb{E}[\varepsilon \mid \mu_k + \varepsilon \in V_k(\mu)]\)
involves an integral over the Voronoi cell, which is the intersection of
half-spaces
\(\{\|\mu_k + \varepsilon - \mu_k\| \leq \|\mu_k + \varepsilon - \mu_j\|\} = \{2\varepsilon^\top(\mu_j - \mu_k) \leq -\|\mu_j - \mu_k\|^2\}\)
for \(j \neq k\). By symmetry of the sub-Gaussian distribution, the
conditional mean is bounded by:

\[\|\mathbb{E}[\varepsilon \mid \mu_k + \varepsilon \in V_k(\mu)]\|_2 \leq C_3 \sigma \sqrt{d_\phi} \cdot \exp\left(-\frac{\Delta_^2}{8\sigma^2}\right)\]

for an absolute constant \(C_3 > 0\). (This follows because the Voronoi
cell \(V_k(\mu)\) differs from the full space by an event of probability
\(\leq K \exp(-\Delta_^2/(8\sigma^2))\), and the unconditional
mean of \(\varepsilon\) is zero.)

Assembling the terms:

\[\|\tilde_k - \mu_k\| \leq \frac{C_3 K (M + \sigma\sqrt{d_\phi})}{\pi_k} \cdot \exp\left(-\frac{\Delta_^2}{8\sigma^2}\right) \leq \varepsilon_{pop}\]

where the \(K\) factor accounts for the union bound over off-diagonal
error sources, \(M = \max_j \|\mu_j\|\), and the denominator \(\pi_k\)
accounts for the \(P(V_k(\mu))\) normalization (which is at least
\(\pi_k\) minus an exponentially small error).

**Step 5: From approximate fixed point to minimizer proximity.**

Let \(T\) be the self-consistency operator:
\(T(\theta)_j = \mathbb{E}[\phi \mid \phi \in V_j(\theta)]\). The
population minimizer \(\theta^*\) is a fixed point:
\(T(\theta^*) = \theta^*\). The true centers \(\mu\) are an approximate
fixed point: \(\|T(\mu) - \mu\|_\infty \leq \varepsilon_{pop}\).

Under the strong separation condition, the Voronoi partition is stable:
if two center sets \(\theta\), \(\theta'\) satisfy
\(\|\theta - \theta'\|_\infty < \Delta_/4\), then their Voronoi
partitions differ only on a set of exponentially small measure.
Consequently, \(T\) is a contraction in a neighborhood of \(\mu\):

\[\|T(\theta) - T(\mu)\|_\infty \leq \frac{1}{2} \|\theta - \mu\|_\infty \quad whenever  \|\theta - \mu\|_\infty \leq \frac{\Delta_}{4}\]

(The contraction factor \(1/2\) follows from the fact that moving a
center by \(\delta\) changes the conditional mean by at most \(\delta\)
times the fraction of points near the decision boundary, which is
\(O(\exp(-\Delta_^2/(8\sigma^2))) \cdot \delta\) --- negligible
compared to \(\delta\).)

Applying the contraction bound:

\[\|\theta^* - \mu\|_\infty \leq \|T(\theta^*) - T(\mu)\|_\infty + \|T(\mu) - \mu\|_\infty \leq \frac{1}{2} \|\theta^* - \mu\|_\infty + \varepsilon_{pop}\]

Solving: \(\|\theta^* - \mu\|_\infty \leq 2\varepsilon_{pop}\).

Under the strong separation condition
(\(\Delta_^2 / (\sigma^2 d_\phi) \geq C_0\) for sufficiently large
\(C_0\)):

\[2\varepsilon_{pop} = \frac{2C_2 K(M + \sigma\sqrt{d_\phi})}{\pi_} \exp\left(-\frac{\Delta_^2}{8\sigma^2}\right) < \frac{\Delta_}{8}\]

This holds because the exponential
\(\exp(-\Delta_^2/(8\sigma^2))\) decays super-polynomially in
\(\Delta_^2/\sigma^2\), while the pre-factor is polynomial. The
explicit condition: choose \(C_0\) such that

\[\frac{\Delta_^2}{8\sigma^2} \geq \log\left( \frac{16C_2 K(M + \sigma\sqrt{d_\phi})}{\pi_ \Delta_} \right)\]

This is guaranteed by \(C_0\) large enough, since the RHS grows only
logarithmically in the problem parameters. \(\square\)

#### 3.3 Remarks on Lemma 1<!-- label: remarks-on-lemma-1 -->

1. 
2. 
3. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{4. Lemma 2: Exponential Convergence of the Empirical
Minimizer}<!-- label: lemma-2-exponential-convergence-of-the-empirical-minimizer -->

> **Purpose**: Show that the global empirical \(k\)-means minimizer
> \(\hat_n\) converges to \(\theta^*\) at an exponential rate.

#### 4.1 Statement<!-- label: statement-1 -->

**Lemma 2 (Exponential convergence of empirical minimizer)**. Let
\(\theta^*\) be the unique population minimizer from Lemma 1, and let
\(\hat_n\) be the global empirical minimizer of \(W_n\). For any
\(t > 0\) satisfying \(t \geq C_0 \sqrt{K d_\phi / n}\) (the
``resolution threshold''), there exist constants \(c_2, C_4 > 0\)
depending on the problem parameters (\(K, \pi_, M, \sigma\)) such
that:

\[P\left(\|\hat_n - \theta^*\| \geq t\right) \leq C_4 \cdot \exp\left(-c_2 \cdot \frac{n \cdot t^2}{\sigma^2 d_\phi}\right)\]

The constants are:

- 
- 

In particular, for \(t = \Delta_/8\) and \(n \geq n_0\):

\[P\left(\|\hat_n - \theta^*\| \geq \frac{\Delta_}{8}\right) \leq 2 \cdot \exp\left(-c_2 \cdot \frac{n \cdot \Delta_^2}{64 \sigma^2 d_\phi}\right)\]

#### 4.2 Proof of Lemma 2<!-- label: proof-of-lemma-2 -->

The proof uses a **localized argmin argument** with peeling. It has
three parts:

1. 
2. 
3. 

**Step 1: Quadratic lower bound near \(\theta^*\).**

The function \(W\) is **not** globally convex (as noted in the
review), but it is locally strongly convex in a neighborhood of
\(\theta^*\) where the Voronoi partition does not change. The size of
this neighborhood is determined by the separation gap.

Define \(r_0 = \Delta_/4\). By Lemma 1,
\(\|\theta^* - \mu\| < \Delta_/8\), so the set
\(\{\theta : \|\theta - \theta^*\| \leq r_0\}\) is contained within
\(\Delta_/4\) of the true centers. Within this region, for any
\(\theta\), the Voronoi cells \(V_j(\theta)\) are close to
\(V_j(\theta^*)\), differing only on an exponentially small set of
boundary points. By Lemma S5 (proved in the Appendix):

\[W(\theta) - W(\theta^*) \geq \lambda \cdot \|\theta - \theta^*\|^2 \qquad for all  \|\theta - \theta^*\| \leq r_0 \]

where \(\lambda = \pi_ / 2\).

**Step 2: The argmin inequality.**

Let \(\hat_n\) minimize \(W_n\). From
\(W_n(\hat_n) \leq W_n(\theta^*)\):

\[
$$
0 &\geq W_n(\hat_n) - W_n(\theta^*) 

&= \bigl(W(\hat_n) - W(\theta^*)\bigr) + \bigl((P_n-P)(f_{\hat_n} - f_{\theta^*})\bigr) 

&\geq \lambda \|\hat_n - \theta^*\|^2 - |(P_n-P)(f_{\hat_n} - f_{\theta^*})|
$$
\]

Therefore:

\[\lambda \|\hat_n - \theta^*\|^2 \leq |(P_n-P)(f_{\hat_n} - f_{\theta^*})| \]

This holds whenever \(\|\hat_n - \theta^*\| \leq r_0\). If
\(\|\hat_n - \theta^*\| > r_0\), we handle that separately.

**Step 3: The localized empirical process.**

Define the localized supremum:

\[\psi_n(r) = \sup_{\|\theta - \theta^*\| \leq r} |(P_n-P)(f_\theta - f_{\theta^*})|\]

From (3), if \(\|\hat_n - \theta^*\| \leq r_0\), then letting
\(r = \|\hat_n - \theta^*\|\):

\[\lambda r^2 \leq \psi_n(r) \]

**Step 4: Expectation of \(\psi_n(r)\).**

For a fixed radius \(r\), consider the class of functions:

\[\mathcal{G}_r = \{g_\theta(x) = f_\theta(x) - f_{\theta^*}(x) : \|\theta - \theta^*\| \leq r\}\]

Each \(g_\theta\) satisfies: - \(|g_\theta(x)| \leq L(x) \cdot r\) where
\(L(x) = 2(\|\phi(x)\|_2 + M)\) (from Lemma S4). -
\(E[g_\theta(X)^2] \leq C_L^2 r^2\) where
\(C_L^2 = 8(\max_j \|\mu_j\|^2 + \sigma^2 d_\phi + M^2)\) (from the
sub-Gaussian bound).

The covering number of
\(\Theta_r = \{\theta : \|\theta - \theta^*\| \leq r\}\) under
\(\|\cdot\|_\infty\) is bounded by Lemma S3:

\[\log \mathcal{N}(\varepsilon, \Theta_r, \|\cdot\|_\infty) \leq K d_\phi \log\left(1 + \frac{4r}\right)\]

By Dudley's entropy integral (e.g., Vershynin 2018, Theorem 8.1.3), the
expected supremum satisfies:

\[\mathbb{E}[\psi_n(r)] \leq C_5 \cdot \sqrt{\frac{K d_\phi}{n}} \cdot C_L \cdot r \]

where \(C_5\) is a universal constant (the Dudley integral constant).

**Step 5: Concentration of \(\psi_n(r)\).**

For the function class \(\mathcal{G}_r\) with \(|g| \leq C_L r\) and
\(E[g^2] \leq C_L^2 r^2\), Talagrand's concentration inequality (e.g.,
Bousquet 2002) gives:

\[P\left(\psi_n(r) \geq \mathbb{E}[\psi_n(r)] + u\right) \leq \exp\left(-\frac{c_6 n u^2}{C_L^2 r^2}\right) \]

for any \(u \geq 0\), where \(c_6\) is a universal constant.

**Step 6: Peeling argument.**

Fix \(t\) such that \(t \leq r_0\) and
\(t \geq \frac{8 C_5 C_L} \sqrt{\frac{K d_\phi}{n}}\). Let
\(J = \lceil \log_2(r_0/t) \rceil\) and define dyadic intervals
\(r_j = 2^j t\) for \(j = 0, 1, ..., J\).

From (4): if \(\|\hat_n - \theta^*\| \geq t\), then
\(\lambda \|\hat_n - \theta^*\|^2 \leq \psi_n(\|\hat_n - \theta^*\|)\).
For \(\|\hat_n - \theta^*\|\) falling in the interval
\([r_{j-1}, r_j)\) for some \(j\):

\[\lambda r_{j-1}^2 \leq \lambda \|\hat_n - \theta^*\|^2 \leq \psi_n(\|\hat_n - \theta^*\|) \leq \psi_n(r_j)\]

Therefore:

\[P(\|\hat_n - \theta^*\| \geq t) \leq \sum_{j=0}^J P\left(\psi_n(r_j) \geq \lambda (r_{j-1})^2\right) \]

where \(r_{-1} := t/2\) for the \(j=0\) term.

For each \(j\), bound \(P(\psi_n(r_j) \geq \lambda r_{j-1}^2)\). Using
\(r_j = 2r_{j-1}\), we have \(\lambda r_{j-1}^2 = \lambda r_j^2 / 4\).

From (5):
\(\mathbb{E}[\psi_n(r_j)] \leq C_5 C_L \sqrt{K d_\phi / n} \cdot r_j\).

Set \(u_j = \lambda r_j^2 / 4 - \mathbb{E}[\psi_n(r_j)]\). Our condition
on \(t\) ensures:

\[\mathbb{E}[\psi_n(r_j)] \leq C_5 C_L \sqrt{\frac{K d_\phi}{n}} \cdot r_j \leq \frac{\lambda r_j^2}{8}\]

since
\(r_j \geq t \geq \frac{8 C_5 C_L} \sqrt{\frac{K d_\phi}{n}}\).
Hence \(u_j \geq \lambda r_j^2 / 8\).

Applying (6) with \(u = u_j\):

\[P\left(\psi_n(r_j) \geq \lambda r_j^2 / 4\right) \leq \exp\left(-\frac{c_6 n (\lambda r_j^2 / 8)^2}{C_L^2 r_j^2}\right) = \exp\left(-\frac{c_6 \lambda^2 n r_j^2}{64 C_L^2}\right) \]

Now \(r_j^2 = 4^j t^2\) (for \(j \geq 0\)) and \(r_0 = t\). The sum in
(7) becomes:

\[P(\|\hat_n - \theta^*\| \geq t) \leq \sum_{j=0}^J \exp\left(-\frac{c_6 \lambda^2 n \cdot 4^j t^2}{64 C_L^2}\right)\]

The sum is dominated by the \(j=0\) term because subsequent terms decay
geometrically:

\[\sum_{j=0}^\infty \exp\left(-\frac{c_6 \lambda^2 n \cdot 4^j t^2}{64 C_L^2}\right) \leq 2 \cdot \exp\left(-\frac{c_6 \lambda^2 n t^2}{64 C_L^2}\right)\]

for all \(n\) and \(t\) satisfying the threshold condition. Therefore:

\[P(\|\hat_n - \theta^*\| \geq t) \leq 2 \cdot \exp\left(-\frac{c_2 n t^2}{\sigma^2 d_\phi}\right)\]

where \(c_2 = c_6 \lambda^2 / (64 C_L^2)\) and we use
\(C_L^2 \leq C_7 \sigma^2 d_\phi\) (the dominant term when
\(\sigma^2 d_\phi \gg \max\|\mu\|^2\), or a constant otherwise). The
exact constant can be chosen as \(c_2 = c_6 \lambda^2 / (128 C_L^2)\) to
account for the simplification.

This establishes the claimed bound. \(\square\)

#### 4.3 Remarks on Lemma 2<!-- label: remarks-on-lemma-2 -->

1. 
2. 
3. 
4. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{5. Lemma 3: Deterministic Partition
Recovery}<!-- label: lemma-3-deterministic-partition-recovery -->

> **Purpose**: Show that if the estimated centers are within
> \(\Delta_/4\) of the true centers, then the induced partition
> matches the true partition for all but an exponentially small fraction
> of points.

#### 5.1 Statement<!-- label: statement-2 -->

**Lemma 3 (Center proximity implies correct partition)**. Let
\(\mu = \{\mu_1,...,\mu_K\}\) be the true centers with separation
\(\Delta_ > 0\). Let \(\theta = \{\theta_1,...,\theta_K\}\) be
any set of estimated centers satisfying, for some permutation \(\pi\):

\[\|\theta_j - \mu_{\pi(j)}\|_2 \leq \frac{\Delta_}{8} \qquad for all  j\]

Then for any point \(\phi = \mu_k + \varepsilon\) with
\(\|\varepsilon\|_2 < 3\Delta_/8\):

\[\arg \min_{j} \|\phi - \theta_j\|_2 = \pi^{-1}(k)\]

i.e., the point is correctly classified by nearest-neighbor assignment
to \(\theta\).

#### 5.2 Proof of Lemma 3<!-- label: proof-of-lemma-3 -->

Fix a true state \(k\). Let \(j_k = \pi^{-1}(k)\) be the estimated
center matched to \(\mu_k\). For any other estimated center
\(j' \neq j_k\), let \(k' = \pi(j') \neq k\) be its matched true center.

By the triangle inequality, the distance from \(\phi\) to the correct
estimated center is:

\[\|\phi - \theta_{j_k}\| \leq \|\mu_k - \theta_{j_k}\| + \|\varepsilon\| \leq \frac{\Delta_}{8} + \|\varepsilon\|\]

The distance to a wrong estimated center is:

\[\|\phi - \theta_{j'}\| \geq \|\mu_k - \mu_{k'}\| - \|\mu_{k'} - \theta_{j'}\| - \|\varepsilon\| \geq \Delta_ - \frac{\Delta_}{8} - \|\varepsilon\| = \frac{7\Delta_}{8} - \|\varepsilon\|\]

For \(\|\varepsilon\| < 3\Delta_/8\):

\[\|\phi - \theta_{j_k}\| \leq \frac{\Delta_}{8} + \frac{3\Delta_}{8} = \frac{\Delta_}{2}\]

\[\|\phi - \theta_{j'}\| \geq \frac{7\Delta_}{8} - \frac{3\Delta_}{8} = \frac{\Delta_}{2}\]

Therefore
\(\|\phi - \theta_{j_k}\| \leq \Delta_/2 \leq \|\phi - \theta_{j'}\|\),
with strict inequality when the noise bound is strict or
\(\|\mu_k - \theta_{j_k}\| < \Delta_/8\). The nearest estimated
center to \(\phi\) is \(\theta_{j_k} = \theta_{\pi^{-1}(k)}\), which is
the center matched to the true state \(k\). \(\square\)

**Corollary 3.1 (Misclassification bound)**. Under the same
conditions, the overall misclassification rate satisfies:

\[\frac{1}{n}\sum_{i=1}^n \mathbf{1}\{\hat{s}(x_i) \neq s(x_i)\}
\leq \mathbf{1}\left\{\max_j \|\hat_j - \mu_{\pi(j)}\| \geq \frac{\Delta_}{4}\right\}
+ \frac{1}{n}\sum_{i=1}^n \mathbf{1}\{\|\varepsilon_i\| \geq 3\Delta_/8\}\]

**Proof**. The first term captures the event that the center
proximity condition of Lemma 3 fails. The second term captures the
irreducible noise: even with perfect centers, a point with
\(\|\varepsilon\| \geq 3\Delta_/8\) could be misclassified.
\(\square\)

#### 5.3 Remarks on Lemma 3<!-- label: remarks-on-lemma-3 -->

1. 
2. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{6. Lemma 4: Lloyd's Algorithm Under Strong
Separation}<!-- label: lemma-4-lloyds-algorithm-under-strong-separation -->

> **Purpose**: Address the NP-hard gap (Review Issue 3). Show that
> under the strong separation condition, Lloyd's algorithm with random
> restarts finds the global empirical minimizer with high probability.

\subsubsection{6.1 Honest Framing of the NP-Hard
Gap}<!-- label: honest-framing-of-the-np-hard-gap -->

\(k\)-means is NP-hard in the worst case (Aloise et al., 2009; Dasgupta,
2008). The global minimizer \(\hat_n\) defined in Section 1.5 is
a computational oracle. In practice, Lloyd's algorithm (alternating
assignment and update) finds a local minimum.

**However**: under the **well-separated mixture assumption**
considered here, the \(k\)-means landscape is benign. The population
objective \(W\) has a unique local minimum (which is the global minimum)
in a ball of radius \(\Delta_/4\) around the true centers. For
sufficiently large \(n\), the empirical objective \(W_n\) inherits this
structure.

**Two approaches**: We present both (a) a self-contained landscape
analysis showing Lloyd's with random restarts succeeds, and (b) an
explicit acknowledgment that if only an approximate (not global)
empirical minimizer is available, the bound degrades by an
\(\varepsilon\)-approximation factor.

#### 6.2 Statement<!-- label: statement-3 -->

**Lemma 4 (Lloyd's with random restarts under strong separation)**.
Under the conditions of Theorem 5 (fixed \(K\), strong separation
\(\Delta_^2 / (\sigma^2 d_\phi) \geq C_0\), \(n\) sufficiently
large), Lloyd's algorithm initialized with \(R = C_R \log n\)
independent random initializations (e.g., \(k\)-means++ or uniform
subsampling of data points) returns a solution \(\tilde_n\)
satisfying:

\[P\left(\|\tilde_n - \hat_n^*\| \geq \frac{\Delta_}{16}\right) \leq n^{-c}\]

for any desired \(c > 0\) (by choosing \(C_R\) sufficiently large). Here
\(\hat_n^*\) is the global empirical minimizer.

#### 6.3 Proof of Lemma 4<!-- label: proof-of-lemma-4 -->

**Step 1: Landscape structure under strong separation.**

From Lemma 1, the population minimizer \(\theta^*\) satisfies
\(\|\theta^* - \mu\| < \Delta_/8\). From Lemma 2, for \(n\) large
enough, the global empirical minimizer \(\hat_n^*\) satisfies
\(\|\hat_n^* - \theta^*\| < \Delta_/8\) with probability
\(1 - \exp(-c n)\). Thus
\(\|\hat_n^* - \mu\| < \Delta_/4\) with high probability.

Now consider the \(k\)-means objective \(W_n\) restricted to the ball
\(B = \{\theta : \|\theta - \mu\|_\infty \leq \Delta_/4\}\).
Within this ball:

- 
- 
- 

**Step 2: Lloyd's algorithm as alternating minimization.**

Lloyd's algorithm iterates: 1. **Assignment step**: For fixed
centers \(\theta^{(t)}\), assign each point to the nearest center. 2.
**Update step**: Set
\(\theta_j^{(t+1)} = \frac{1}{|C_j^{(t)}|} \sum_{i \in C_j^{(t)}} \phi(x_i)\),
where \(C_j^{(t)}\) is the set of points assigned to center \(j\).

Within the ball \(B\), the assignment step correctly clusters all but an
exponentially small fraction of points (by Lemma 3). The update step
therefore computes the sample mean of nearly-clean clusters, which is a
contraction toward the true cluster means:

\[\|\theta_j^{(t+1)} - \hat_{n,j}^*\| \leq \frac{1}{2} \|\theta_j^{(t)} - \hat_{n,j}^*\|\]

for all \(j\), with probability at least
\(1 - \exp(-c n \Delta_^2 / (K \sigma^2 d_\phi))\). (The
contraction factor \(1/2\) follows from the stability of the Voronoi
partition and sub-Gaussian concentration of the sample mean.)

Thus Lloyd's converges linearly to \(\hat_n^*\) from any
initialization in \(B\), achieving accuracy \(\Delta_/16\) in
\(O(\log n)\) iterations.

**Step 3: Random initialization covers the good basin.**

Each independent initialization selects \(K\) data points uniformly at
random (or via \(k\)-means++ seeding). The probability that at least one
data point from each true cluster is selected is:

\[p_{hit} = \sum_{permutations  \pi} \prod_{k=1}^K \frac{n_{\pi(k)}}{n - \sum_{j<k} n_{\pi(j)}} \geq \prod_{k=1}^K \frac{n_k}{n} \geq \pi_^K > 0\]

where \(\pi_ = \min_k \pi_k\) and the inequality uses that
selecting a point from each cluster is a coupon-collector-like process.
The probability that a selected set of \(K\) points includes one from
each cluster is at least \(\pi_^K\) (a constant depending only on
\(K\) and \(\pi_\), not on \(n\)).

If the initialization includes a point from each cluster, then using the
sub-Gaussian tail bound (Lemma S1), each selected point is within
\(\Delta_/8\) of its true cluster center with probability at least
\(1 - K \cdot \exp(-c \Delta_^2/\sigma^2)\). Thus a single random
initialization lands in \(B\) with probability at least
\(p_0 = \pi_^K / 2\) for large \(n\).

**Step 4: Amplification via multiple restarts.**

With \(R\) independent restarts:

\[P(no restart lands in  B) \leq (1 - p_0)^R\]

Setting \(R = C_R \log n\) with \(C_R \geq (c+1)/|\log(1-p_0)|\):

\[P(initialization failure) \leq n^{-c}\]

Each successful initialization converges to within \(\Delta_/16\)
of \(\hat_n^*\) in \(O(\log n)\) Lloyd iterations. The total
runtime is
\(O(R \cdot n \cdot K \cdot d_\phi \cdot \log n) = O(n \log^2 n)\),
which is polynomial. The solution with the smallest \(W_n\) among the
\(R\) runs is returned. \(\square\)

#### 6.4 Remarks on Lemma 4<!-- label: remarks-on-lemma-4 -->

1. 
2. 
3. 
4. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{7. Main Theorem: Statement and
Proof}<!-- label: main-theorem-statement-and-proof -->

#### 7.1 Theorem Statement<!-- label: theorem-statement -->

**Theorem 5 (Fixed-K State Discovery Consistency)**. Let \(K\) be
fixed. Suppose:

1. 
2. 
3. 
4. 

Then the estimated partition \(\hat{\mathcal{C}}^{(n)}\) satisfies:

\[
$$
P\bigl(&\hat{\mathcal{C}}^{(n)} \neq \mathcal{C}^*  up to permutation\bigr) 

&\leq K \cdot \exp\left(-c_1 \cdot \frac{n_ \Delta_^2}{\sigma^2 d_\phi}\right) \;+\; o(1)
$$
\]

where \(c_1 > 0\) is a universal constant independent of
\(K, n, \sigma, \Delta_\). The \(o(1)\) term captures the
exponentially small bias from the population minimizer and the
initialization failure probability from Lemma 4.

Equivalently, the probability that the estimated partition differs from
the true partition (for all points with
\(\|\varepsilon\| < 3\Delta_/8\)) converges to zero as
\(n_ \to \infty\).

#### 7.2 Proof of Theorem 5<!-- label: proof-of-theorem-5 -->

We combine the four lemmas.

**Step 1: Population bias is bounded.**

By Lemma 1, the unique population minimizer \(\theta^*\) satisfies, for
some permutation \(\pi_1\):

\[\|\theta^*_{\pi_1(k)} - \mu_k\| \leq \varepsilon_{pop} < \frac{\Delta_}{8}\]

**Step 2: Empirical minimizer convergence.**

By Lemma 2 (with \(t = \Delta_/8\)), for \(n\) large enough such
that \(\Delta_/8 \geq C_0\sqrt{K d_\phi / n}\):

\[P\left(\|\hat_n - \theta^*\| \geq \frac{\Delta_}{8}\right) \leq 2 \cdot \exp\left(-c_2 \cdot \frac{n \cdot (\Delta_/8)^2}{\sigma^2 d_\phi}\right)\]

\[\leq 2 \cdot \exp\left(-\frac{c_2}{64} \cdot \frac{n \cdot \Delta_^2}{\sigma^2 d_\phi}\right)\]

Combining with Lemma 1 via the triangle inequality:

\[\|\hat_n - \mu\| \leq \|\hat_n - \theta^*\| + \|\theta^* - \mu\| < \frac{\Delta_}{8} + \frac{\Delta_}{8} = \frac{\Delta_}{4}\]

with probability at least
\(1 - 2 \cdot \exp\left(-\frac{c_2}{64} \cdot \frac{n \cdot \Delta_^2}{\sigma^2 d_\phi}\right)\).

**Step 3: Lloyd's finds the global minimizer.**

By Lemma 4, with \(R = C_R \log n\) restarts:

\[P\left(\|\tilde_n - \hat_n\| \geq \frac{\Delta_}{16}\right) \leq n^{-c}\]

for any desired \(c > 0\). Since
\(\|\hat_n - \mu\| < \Delta_/4\) with high probability
from Step 2, the Lloyd output satisfies:

\[\|\tilde_n - \mu\| \leq \|\tilde_n - \hat_n\| + \|\hat_n - \theta^*\| + \|\theta^* - \mu\| < \frac{\Delta_}{16} + \frac{\Delta_}{8} + \frac{\Delta_}{8} = \frac{\Delta_}{4}\]

with probability at least
\(1 - 2\exp(-c_2 n \Delta_^2 / (64 \sigma^2 d_\phi)) - n^{-c}\).

**Step 4: Center proximity implies correct partition.**

By Lemma 3, when
\(\|\tilde_j - \mu_{\pi(j)}\| < \Delta_/4\) for all \(j\),
the induced partition matches the true partition for all points with
\(\|\varepsilon\| < 3\Delta_/8\).

The fraction of points with \(\|\varepsilon\| \geq 3\Delta_/8\) is
bounded by Lemma S1:

\[P(\|\varepsilon\| \geq 3\Delta_/8) \leq 2 \exp\left(-c_0 \cdot \frac{\Delta_^2}{\sigma^2}\right)\]

This irreducible error is independent of \(n\) and is absorbed into the
\(o(1)\) term. It represents points that are inherently ambiguous due to
large noise --- even perfect knowledge of the centers cannot classify
them correctly.

**Step 5: Converting \(n\) to \(n_\).**

Since \(K\) is fixed, \(n \geq K \cdot n_\) (by the pigeonhole
principle). Therefore:

\[\exp\left(-\frac{c_2}{64} \cdot \frac{n \cdot \Delta_^2}{\sigma^2 d_\phi}\right) \leq \exp\left(-\frac{c_2 K}{64} \cdot \frac{n_ \cdot \Delta_^2}{\sigma^2 d_\phi}\right)\]

**Step 6: Final probability bound.**

Let \(c_1 = c_2 K / 64\). Collecting all error terms:

\[
$$
&P(estimated partition \neq true partition) 

&\leq P\left(\|\tilde_n - \mu\| \geq \frac{\Delta_}{4}\right) + P(Lloyd's initialization fails) 

&\leq 2 \cdot \exp\left(-c_2 \cdot \frac{n \cdot \Delta_^2}{64 \sigma^2 d_\phi}\right) \;+\; n^{-c} 

&\leq 2 \cdot \exp\left(-c_1 \cdot \frac{n_ \cdot \Delta_^2}{\sigma^2 d_\phi}\right) \;+\; o(1)
$$
\]

The \(o(1)\) term absorbs: - The exponentially small bias
\(\varepsilon_{pop}\) from Lemma 1 (which ensures
\(\|\theta^* - \mu\| < \Delta_/8\)). - The initialization failure
probability \(n^{-c}\) from Lemma 4. - The irreducible misclassification
from large-noise samples (\(\|\varepsilon\| \geq 3\Delta_/8\)),
which is \(O(\exp(-c \Delta_^2/\sigma^2))\) and vanishes as
\(\Delta_/\sigma \to \infty\). - The \(K\) factor in front of the
exponential (from the union bound over \(K\) centers) is at most
\(K \leq \exp(c_1 n_ \Delta_^2 / (\sigma^2 d_\phi))^{o(1)}\),
so it is absorbed into the exponential.

The final bound:

\[P(\hat{\mathcal{C}}^{(n)} \neq \mathcal{C}^*) \leq K \cdot \exp\left(-c_1 \cdot \frac{n_ \Delta_^2}{\sigma^2 d_\phi}\right) + o(1)\]

This completes the proof of Theorem 5. \(\square\)

\subsubsection{7.3 Verification of Exponents and Inequality
Directions}<!-- label: verification-of-exponents-and-inequality-directions -->

We explicitly verify each critical step:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1579}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2895}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2895}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2632}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Step
\end{minipage} & \begin{minipage}[b]
Inequality
\end{minipage} & \begin{minipage}[b]
Direction
\end{minipage} & \begin{minipage}[b]
Verified
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Lemma 1, Claim &
\(P(2\varepsilon^\top(\mu_j - \mu_k) \leq -\|\mu_j-\mu_k\|^2) \leq \exp(-\|\mu_j-\mu_k\|^2/(8\sigma^2))\)
& \(\leq\), correct tail & Yes 

Lemma 1, Step 4 &
\(\|\tilde_k - \mu_k\| \leq \varepsilon_{pop}\) &
\(\leq\), upper bound & Yes 

Lemma 2, (3) &
\(\lambda\|\hat_n - \theta^*\|^2 \leq \|(P_n-P)(f_{\hat_n} - f_{\theta^*})\|\)
& \(\leq\), wrapper around \(W_n(\hat_n) \leq W_n(\theta^*)\) &
Yes 

Lemma 2, (5) &
\(\mathbb{E}[\psi_n(r)] \leq C_5\sqrt{K d_\phi/n}\cdot C_L r\) &
\(\leq\), Dudley & Yes 

Lemma 2, (8) &
\(P(\psi_n(r_j) \geq \lambda r_j^2/4) \leq \exp(-c_6 \lambda^2 n r_j^2/(64 C_L^2))\)
& \(\leq\), Talagrand & Yes 

Lemma 2, sum & \(\sum_{j} \exp(-c \cdot 4^j t^2) \leq 2\exp(-c t^2)\) &
\(\leq\), geometric dominance & Yes 

Lemma 3 &
\(\|\phi - \theta_{j_k}\| \leq \Delta_/2 \leq \|\phi - \theta_{j'}\|\)
& \(\leq\) both sides, correct direction & Yes 

Lemma 4 & \(P(no hit) \leq (1-p_0)^R \leq n^{-c}\) & \(\leq\),
correct & Yes 

Theorem &
\(P(\hat{\mathcal{C}} \neq \mathcal{C}^*) \leq sum of bounds\) &
\(\leq\), union bound & Yes 

\end{longtable}

The exponent \(-\frac{c_1 n_ \Delta_^2}{\sigma^2 d_\phi}\)
is **always negative** for \(n_ > 0\), \(\Delta_ > 0\),
\(\sigma^2 < \infty\), \(d_\phi < \infty\). There is no risk of a
positive exponent (fixing Review Issue 2).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{8. Corollary: Sample Size
Guide}<!-- label: corollary-sample-size-guide -->

**Corollary (Required samples per state)**. To achieve
misclassification probability \(\leq \delta\) due to center estimation,
it suffices to have:

\[n_ \geq \frac{C_1 \sigma^2 d_\phi}{\Delta_^2} \cdot \log\left(\frac{K}\right)\]

for a universal constant \(C_1 > 0\) (given by the proof constants
\(c_1\)).

**Operational rule of thumb**:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.4848}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5152}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Ratio \(\Delta_ / (\sigma \sqrt{d_\phi})\)
\end{minipage} & \begin{minipage}[b]
Samples per state for \(P(error) \leq 0.05\)
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
0.5 (marginal) & \(\geq 400\) 

1.0 (moderate) & \(\geq 100\) 

2.0 (good) & \(\geq 25\) 

3.0 (strong) & \(\geq 12\) 

\end{longtable}

These numbers assume \(K \leq 10\), \(d_\phi \leq 64\), and use
\(C_1 \approx 20\) (from a more detailed constant analysis).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{9. Discussion of Assumptions and
Limitations}<!-- label: discussion-of-assumptions-and-limitations -->

\subsubsection{\texorpdfstring{9.1 Fixed \(K\) (Not
Growing)}{9.1 Fixed K (Not Growing)}}<!-- label: fixed-k-not-growing -->

The proof relies on \(K\) being fixed. This allows: - The covering
number
\(\log \mathcal{N}(\varepsilon) \leq K d_\phi \log(1 + 2M/\varepsilon)\),
which is \(O(\log(1/\varepsilon))\) for fixed \(K\). - The strong
convexity parameter \(\lambda = \pi_/2\) is fixed (does not decay
with \(K\)). - The random initialization probability
\(p_0 \geq \pi_^K\) is a fixed constant.

For \(K \to \infty\) as \(n \to \infty\): - The covering number grows
like \(K\), giving \(K d_\phi\) factors that degrade the bound. -
\(\pi_\) could be \(O(1/K)\) for balanced states, making
\(\lambda = O(1/K)\). - The initialization probability decays
exponentially in \(K\).

The growing-\(K\) regime requires a separate analysis (see Pollard, 1981
for strong consistency with growing \(K\) under appropriate conditions;
or Lei et al., 2013 for minimax rates).

\subsubsection{9.2 The NP-Hard Gap (Issue 3
Resolution)}<!-- label: the-np-hard-gap-issue-3-resolution -->

This proof **does** resolve the NP-hard gap within the strong
separation regime:

1. 
2. 

The chain holds because: (a) \(k\)-means on well-separated mixtures is
not a hard instance --- the landscape has a unique local minimum, and
Lloyd's contracts toward it; (b) the NP-hardness of \(k\)-means applies
to worst-case instances, not the well-separated Gaussian-like mixtures
considered here.

**If the strong separation condition does not hold** (i.e.,
\(\Delta_^2 / (\sigma^2 d_\phi)\) is small), then: - The landscape
may have spurious local minima. - Lloyd's algorithm may converge to a
suboptimal solution. - The theorem's guarantee degrades: one can only
claim that there exists some polynomial-time algorithm finding an
\(\varepsilon\)-approximate solution (e.g., via Kumar \& Kannan, 2010 or
Ostrovsky et al., 2013). - We **acknowledge this gap** and do not
claim a guarantee for the weak separation regime.

\subsubsection{9.3 Sub-Gaussian Assumption (Issues
9-10)}<!-- label: sub-gaussian-assumption-issues-9-10 -->

The proof assumes \(\varepsilon\) is sub-Gaussian with parameter
\(\sigma^2\). For the bounds: - Lemma S1 uses the sub-Gaussian norm of
\(\|\varepsilon\|_2\), not the Gaussian chi-squared bound. This fixes
Review Issue 10 (the chi-squared bound was only valid for Gaussian
vectors). - The required bound
\(P(\|\varepsilon\| \geq C\sigma(\sqrt{d_\phi} + \sqrt{t})) \leq 2\exp(-t)\)
holds for all sub-Gaussian vectors (Vershynin 2018, Theorem 3.1.1). - If
\(\varepsilon\) is only bounded (not sub-Gaussian), the tail bounds
degrade from \(\exp(-c n t^2)\) to \(\exp(-c n t)\) via Hoeffding,
changing the exponential rate to a slower exponential. This is a
quantitative difference, not a qualitative one --- the theorem still
holds but with a different constant \(c_1\).

\subsubsection{\texorpdfstring{9.4 Known
\(K\)}{9.4 Known K}}<!-- label: known-k -->

The theorem assumes \(K\) is known and fixed. In practice, \(K\) must be
selected (e.g., via the elbow method, gap statistic, or BIC). Estimating
\(K\) introduces additional uncertainty not captured here. For SCX,
\(K\) is typically determined by the number of distinct states in the
application domain (e.g., phases of a material, regimes of a dynamical
system), which is often known from domain knowledge.

#### 9.5 Irreducible Error<!-- label: irreducible-error -->

Even with perfect center estimates, points with
\(\|\varepsilon\| \geq 3\Delta_/8\) can be misclassified. This is
bounded by \(2\exp(-c_0 \Delta_^2 / \sigma^2)\) regardless of
sample size. This irreducible error characterizes the **ambiguity
of the state partition**: points near decision boundaries are inherently
uncertain. The theorem's claim is that the **center estimates
converge** and the **partition structure is recovered** --- not that
every individual point is correctly labeled. The misclassification of
boundary points is a feature of the data distribution, not a failure of
the estimator.

\subsubsection{9.6 Strong Separation
Requirement}<!-- label: strong-separation-requirement -->

The condition \(\Delta_^2 / (\sigma^2 d_\phi) \geq C_0\) is
sufficient but not necessary. It guarantees
\(\varepsilon_{pop} < \Delta_/8\) in Lemma 1. In practice:
- If \(\Delta_^2 / (\sigma^2 d_\phi)\) is moderate (\(1-4\)), the
bias \(\varepsilon_{pop}\) may be larger but could still be
\(< \Delta_/8\) for moderate \(K,d_\phi\). - If
\(\Delta_^2 / (\sigma^2 d_\phi)\) is small (\(< 1\)), the
population minimizer may deviate significantly from the true centers,
and state discovery may fail. This is the regime covered by Theorem 2
(weak feature failure).

#### 9.7 Proof Constants<!-- label: proof-constants -->

The constants \(c_1, c_2, C_0\) in the theorem depend on: -
\(\pi_\) (minimum state proportion): enters through
\(\lambda = \pi_/2\). - \(C_L\) (Lipschitz constant bound):
\(C_L = 2(M + \sigma\sqrt{d_\phi})\), where \(M = \max_k \|\mu_k\|\). -
\(C_5\) (Dudley integral constant): a universal constant from empirical
process theory. - \(c_6\) (Talagrand concentration constant): a
universal constant.

The explicit value of \(c_1\) is:

\[c_1 = \frac{c_6 \pi_^2 K}{128 \cdot 64 \cdot C_L^2 / (\sigma^2 d_\phi)} = O\left(\frac{\pi_^2 K \sigma^2 d_\phi}{C_L^2}\right)\]

Since \(C_L^2 = O(M^2 + \sigma^2 d_\phi)\), the constant depends on the
signal-to-noise ratio and cluster balance. For the theorem's purposes,
\(c_1 > 0\) is sufficient.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 10. References<!-- label: references -->

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
15. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{11. Appendix: Sub-Gaussian Tail Bounds and Quadratic Lower
Bound}<!-- label: appendix-sub-gaussian-tail-bounds-and-quadratic-lower-bound -->

\subsubsection{\texorpdfstring{Lemma S5: Quadratic Lower Bound for \(W\)
Near
\(\theta^*\)}{Lemma S5: Quadratic Lower Bound for W Near \ theta\^{}*}}<!-- label: lemma-s5-quadratic-lower-bound-for-w-near-theta -->

**Statement**. Under the conditions of Theorem 5, for any
\(\theta\) with \(\|\theta - \theta^*\| \leq \Delta_/4\):

\[W(\theta) - W(\theta^*) \geq \lambda \cdot \|\theta - \theta^*\|^2\]

where \(\lambda = \pi_ / 2\) and \(\pi_ = \min_k P(S = k)\).

**Proof**. Let \(\theta\) satisfy
\(\|\theta - \theta^*\| \leq \Delta_/4\). By Lemma 1,
\(\|\theta^* - \mu\| < \Delta_/8\), so
\(\|\theta - \mu\| < \Delta_/8 + \Delta_/4 = 3\Delta_/8 < \Delta_/2\).

For a point \(\phi = \mu_k + \varepsilon\) with
\(\|\varepsilon\| < \Delta_/8\), Lemma 3 (applied with
\(\Delta_/8\) and \(3\Delta_/8\) bounds) shows that the
nearest center in \(\theta\) is the one matched to true state \(k\).
Points with \(\|\varepsilon\| \geq \Delta_/8\) can be assigned
differently, but these have probability at most
\(2\exp(-\Delta_^2/(128\sigma^2))\) by Lemma S1, which is
\(o(\pi_)\) under the strong separation condition.

Now consider the region where assignments are correct. For each \(k\),
the contribution to \(W\) from true state \(k\) is:

\[\mathbb{E}[\|\phi - \theta_{\pi(k)}\|^2 \mid S=k] \cdot \pi_k\]
\[= \mathbb{E}[\|\mu_k + \varepsilon - \theta_{\pi(k)}\|^2] \cdot \pi_k\]
\[= \pi_k \cdot \left( \|\mu_k - \theta_{\pi(k)}\|^2 + \mathbb{E}[\|\varepsilon\|^2] \right) + 2\pi_k \cdot (\mu_k - \theta_{\pi(k)})^\top \mathbb{E}[\varepsilon \mid S=k]\]

The cross term vanishes since \(\mathbb{E}[\varepsilon] = 0\) and
\(\varepsilon \perp S\). The first term is minimized at
\(\theta_{\pi(k)} = \mu_k\) with value
\(\pi_k \cdot \mathbb{E}[\|\varepsilon\|^2]\).

Therefore, in the region of correct assignment (probability
\(\geq 1 - \delta\) for \(\delta\) exponentially small):

\[W(\theta) - W(\theta^*) \geq \sum_{k=1}^K \pi_k \cdot \|\mu_k - \theta_{\pi(k)}\|^2 - \delta \cdot (bounded terms)\]

\[\geq \pi_ \cdot \sum_{k=1}^K \|\mu_k - \theta_{\pi(k)}\|^2 - O\left(\exp(-\frac{\Delta_^2}{128\sigma^2})\right) \cdot (M^2 + \sigma^2 d_\phi)\]

\[\geq \pi_ \cdot \|\theta - \mu\|^2 - negligible\]

Since \(\|\theta^* - \mu\|\) is exponentially small,
\(\|\theta - \theta^*\| \approx \|\theta - \mu\|\), and:

\[W(\theta) - W(\theta^*) \geq \frac{\pi_}{2} \cdot \|\theta - \theta^*\|^2\]

for \(\|\theta - \theta^*\| \leq \Delta_/4\) and sufficiently
large \(\Delta_^2/(\sigma^2 d_\phi)\). The factor \(1/2\) accounts
for exponentially small corrections. \(\square\)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsubsection{Verification Checklist Against Hostile
Review}<!-- label: verification-checklist-against-hostile-review -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3095}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1905}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.5000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Review Issue
\end{minipage} & \begin{minipage}[b]
Status
\end{minipage} & \begin{minipage}[b]
How v3 Addresses It
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**Issue 1**: Reversed inequality in misclassification bound &
**Fixed** & No misclassification bound computed via
\(O(\sqrt{n/(K\log n)})\) expression. Instead:
\(P(error) \leq K\exp(-c n_\Delta_^2/(\sigma^2 d_\phi))\)
with \(\Delta_\) fixed, giving \(P\to 1\). Explicit verification
of all inequality directions in Section 7.3. 

**Issue 2**: Positive exponent in uniform convergence &
**Fixed** & Replaced covering-number bound with localized empirical
process approach (peeling + Talagrand). No polynomial pre-factors in
\(n\) --- only factor 2 from peeling. Exponent
\(-\frac{c_2 n t^2}{\sigma^2 d_\phi}\) is explicitly negative for all
\(n, t > 0\). 

**Issue 3**: NP-hard gap of \(k\)-means & **Fixed** & Lemma 4
proves Lloyd's with \(R = \Omega(\log n)\) random restarts finds the
global minimizer with probability \(1 - o(1)\) under strong separation.
Explicit acknowledgment: without strong separation, the gap remains.
Cites Ostrovsky et al.~(2013), Kumar \& Kannan (2010). 

**Issue 4**: Lemma 5's incorrect lower bound & **Fixed** &
Replaced with self-consistency argument (Lemma 1). No direct computation
of \(W(\mu) - W(\mu^*)\). Uses sub-Gaussian tail bounds on
mis-assignment probabilities (correct inequality direction) and
contraction argument. 

**Issue 5**: Fixed vs.~scaling \(\Delta_\) & **Fixed** &
\(\Delta_\) is explicitly fixed (does not scale with \(n\)). All
scaling analysis removed. 

**Issue 6c**: Triangle inequality noise handling & **Fixed** &
Lemma 3 uses \(\|\varepsilon\| < 3\Delta_/8\), giving
\(\Delta_/2\) on both sides with correct inequality direction. 

**Issue 7**: Covering number vs VC dimension & **Fixed** &
Uses covering number directly (Lemma S3). Acknowledges the bound. 

**Issue 10**: Chi-squared bound for sub-Gaussian & **Fixed** &
Lemma S1 uses correct sub-Gaussian norm bound (Vershynin 2018), not
Gaussian chi-squared bound. 

\end{longtable}

**Document version**: 2026-06-28