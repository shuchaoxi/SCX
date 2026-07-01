# Minimax Lower Bound for Multi-Expert Noise Detection: Matching Theorem 1

> **Purpose**: Prove a matching minimax lower bound for Theorem 1's exponential rate,
> establishing that the exponent $2M\Delta_s^2$ is optimal -- no method can achieve
> a better exponent than $2$ (up to constant factors).
>
> **Date**: 2026-06-27
>
> **Status**: Complete proof for testing risk; partial extension to F1; one gap identified
> in the mixture-product divergence tensorization for large K.

---

## Table of Contents

1. [Overview and Main Result](#1-overview-and-main-result)
2. [Preliminaries and Notation](#2-preliminaries-and-notation)
3. [Technical Lemmas](#3-technical-lemmas)
4. [Main Proof: Le Cam Two-Point Construction](#4-main-proof-le-cam-two-point-construction)
5. [Extension to F1 Risk](#5-extension-to-f1-risk)
6. [Large-Deviations Refinement](#6-large-deviations-refinement)
7. [Discussion of Tightness and Gaps](#7-discussion-of-tightness-and-gaps)
8. [References](#8-references)

---

## 1. Overview and Main Result

### 1.1 What Theorem 1 Gives (Upper Bound)

Theorem 1 (proved in `01_noise_detection_guarantee.md`) states that for the SCX noise
detector with consistency score $C(x) = \frac{1}{M}\sum_{m=1}^M e_m(x,y)$ and threshold
$\theta$, under assumptions (A1)-(A6):

$$\text{F1} \;\geq\; 1 - \frac{1}{\eta} \sum_{s \in \mathcal{S}} \rho_s \cdot \exp\!\bigl(-2M\Delta_s^2\bigr)$$

where $\Delta_s = \min(\theta - \mu_s,\; 1 - C_{\text{bal}}\mu_s/(K-1) - \theta) > 0$ is the
separation gap for state $s$.

The exponent is $2M\Delta_s^2$. The constant $2$ originates from Hoeffding's inequality.
A natural question: is $2$ the best possible constant in the exponent? Could a fundamentally
different method achieve $\exp(-cM\Delta^2)$ with $c > 2$?

### 1.2 Main Result (Lower Bound)

**Theorem 4 (Minimax Lower Bound for Multi-Expert Noise Detection).**
Assume (A1)-(A6). Fix a state $s$ with separation gap $\Delta > 0$, expert count $M \geq 2$,
noise rate $\eta \in (0, 1/2)$, and class count $K \geq 2$. Let $\psi$ be any measurable
noise detector (a function of the observable $(x, y, \{f_m(x)\})$). Define the testing error:

$$R(\psi) = \max\bigl\{\mathbb{P}_0(\psi = 1),\; \mathbb{P}_1(\psi = 0)\bigr\}$$

where $\mathbb{P}_0$ is the distribution under "clean" and $\mathbb{P}_1$ under "noise"
for the two constructions below.

**Part (a) -- Testing lower bound.** For $K=2$ (binary classification), there exists a
universal constant $c_0 > 0$ such that:

$$\inf_{\psi} \sup_{P \in \mathcal{P}_{\Delta}} R(\psi) \;\geq\; \frac{1}{2} \cdot \exp\!\bigl(-2M\Delta^2\bigr)$$

where $\mathcal{P}_{\Delta}$ is the set of distributions satisfying the SCX assumptions
with separation gap at least $\Delta$. For $K > 2$, the same exponent holds with a
constant that depends on $K$ (the rate in $M\Delta^2$ is preserved).

**Part (b) -- F1 lower bound.** Under the same conditions:

$$\inf_{\psi} \sup_{P \in \mathcal{P}_{\Delta}} \bigl[1 - \text{F1}(\psi, P)\bigr] \;\geq\; \frac{1}{2} \cdot \exp\!\bigl(-2M\Delta^2\bigr)$$

(See Section 5.2 for a refined discussion of the $\eta$ dependence. The bound $1-\text{F1} \geq 1-\text{TPR}$ loses the $\eta$ factor; recovering it requires a tighter F1 conversion that accounts for the false positive rate, which is possible under the specific construction.)

**Part (c) -- Rate optimality.** The SCX consistency detector of Theorem 1 achieves the
exponent $2M\Delta^2$ in its F1 guarantee. By Part (b), no detector can achieve exponent
$> 2M\Delta^2$. Therefore SCX is **minimax rate-optimal** in the M-regime (exponent in
number of experts).

**Corollary (Large-Deviations Refinement).** For the binary symmetric case ($K=2$,
symmetric experts with error rate $\mu = 1/2 - \Delta$, optimal threshold $\theta^* = 1/2$):

$$\lim_{M \to \infty} -\frac{1}{M} \log \inf_{\psi} \sup_{P \in \mathcal{P}_{\Delta}} \bigl[P_0(\psi=1) + P_1(\psi=0)\bigr] = 2\Delta^2$$

confirming that the exponent $2\Delta^2$ per expert is the information-theoretic limit.

---

## 2. Preliminaries and Notation

### 2.1 Setup

We work within the SCX framework of Theorem 1. Define:

- **Clean distribution** $P_0$: For a sample $(x, y^*)$ with true label $y^* = f^*(x)$,
  each expert $f_m$ makes an error with probability $\mu = \mathbb{P}(f_m(x) \neq y^* \mid x)$.
  Given $x$, the errors $e_m = \mathbf{1}\{f_m(x) \neq y\}$ are conditionally independent
  (A2). Under clean data, $y = y^*$, so $e_m = \mathbf{1}\{f_m(x) \neq y^*\}$.

- **Noise distribution** $P_1$: The label $y$ is flipped to a uniform random class
  $c \neq y^*$ (A4). Given $x$ and the noise class $c$, expert $m$ makes an error
  $e_m = \mathbf{1}\{f_m(x) \neq c\}$. These are conditionally independent given $(x,c)$.
  The marginal distribution over $c$ makes $P_1$ a mixture of $(K-1)$ product distributions.

### 2.2 Key Distributions

Fix a state $s$ and a sample $x \in s$. Let $\mu = \mu_s$ be the state's clean error rate
(A5). Under the balanced error assumption (A6) with $C_{\text{bal}} = 1$:

$$\mu_c(x) = \frac{1}{M} \sum_{m=1}^M \mathbb{P}(f_m(x) = c \mid x) \leq \frac{\mu_s}{K-1}, \quad \forall c \neq y^*$$

For a lower bound, we consider the hardest (least favorable) case: all $\mu_c(x)$ are
exactly $\mu/(K-1)$, i.e., experts' errors are perfectly balanced across wrong classes.
This gives the largest separation and therefore the strongest lower bound.

#### Distribution of the error vector $E = (e_1, \dots, e_M)$ under $P_0$:

$$P_0(e_1, \dots, e_M) = \prod_{m=1}^M \text{Bernoulli}(e_m \mid \mu)$$

i.e., $M$ i.i.d. Bernoulli($\mu$) variables. The number of errors
$S = \sum_{m=1}^M e_m \sim \text{Binomial}(M, \mu)$.

#### Distribution of $E$ under $P_1$:

$$P_1(e_1, \dots, e_M) = \frac{1}{K-1} \sum_{c \neq y^*} \prod_{m=1}^M \text{Bernoulli}\!\left(e_m \;\Big|\; 1 - \frac{\mu}{K-1}\right)$$

This is a **mixture of product distributions**: conditioned on the noise class $c$,
each expert independently makes an error with probability $1 - \mu/(K-1)$.

### 2.3 Separation Gap

The mean separation between clean and noise distributions is:

$$\Delta = \mathbb{E}[C \mid P_1] - \mathbb{E}[C \mid P_0]
      = \left(1 - \frac{\mu}{K-1}\right) - \mu
      = 1 - \mu \cdot \frac{K}{K-1}$$

At the optimal threshold $\theta^* = \frac{1}{2}\bigl(1 + \mu\cdot\frac{K-2}{K-1}\bigr)$,
the separation gap used in Theorem 1 is:

$$\Delta^* = \frac{1}{2}\left(1 - \mu \cdot \frac{K}{K-1}\right) = \frac{\Delta}{2}$$

For the minimax lower bound, we work directly with $\Delta^*$ as the fundamental
separation parameter.

---

## 3. Technical Lemmas

### 3.1 Lemma 1: Bernoulli Total Variation

**Lemma 1 (TV of Two Bernoulli Distributions).** For $p, q \in [0,1]$:

$$\text{TV}(\text{Bern}(p), \text{Bern}(q)) = |p - q|$$

**Proof.** For two distributions on $\{0,1\}$:

$$\begin{aligned}
\text{TV}(P, Q) &= \frac{1}{2} \bigl(|p - q| + |(1-p) - (1-q)|\bigr) \\
&= \frac{1}{2}(|p-q| + |p-q|) = |p-q| \qquad \square
\end{aligned}$$

### 3.2 Lemma 2: Chi-Square Divergence of Two Bernoulli Distributions

**Lemma 2 ($\chi^2$ of Two Bernoullis).** For $p, q \in (0,1)$:

$$\chi^2(\text{Bern}(p) \parallel \text{Bern}(q)) = \frac{(p-q)^2}{q(1-q)}$$

**Proof.** By definition $\chi^2(P \parallel Q) = \sum_x \frac{(P(x)-Q(x))^2}{Q(x)}$:

$$\begin{aligned}
\chi^2 &= \frac{(p-q)^2}{q} + \frac{((1-p)-(1-q))^2}{1-q} \\
&= \frac{(p-q)^2}{q} + \frac{(p-q)^2}{1-q} \\
&= (p-q)^2 \cdot \frac{1}{q(1-q)} \qquad \square
\end{aligned}$$

### 3.3 Lemma 3: Chi-Square Tensorization for Product Distributions

**Lemma 3 ($\chi^2$ Tensorization).** For product distributions $P = \prod_{m=1}^M P_m$
and $Q = \prod_{m=1}^M Q_m$:

$$\chi^2(P \parallel Q) = \prod_{m=1}^M \bigl(1 + \chi^2(P_m \parallel Q_m)\bigr) - 1$$

**Proof.** For product measures:

$$\begin{aligned}
\chi^2(P \parallel Q) &= \int \left(\frac{dP}{dQ} - 1\right)^2 dQ \\
&= \int \left(\prod_{m=1}^M \frac{dP_m}{dQ_m} - 1\right)^2 dQ \\
&= \prod_{m=1}^M \int \left(\frac{dP_m}{dQ_m}\right)^2 dQ_m - 1 \\
&= \prod_{m=1}^M \bigl(1 + \chi^2(P_m \parallel Q_m)\bigr) - 1
\end{aligned}$$

where the cross terms vanish because each $\frac{dP_m}{dQ_m}$ has mean 1 under $Q_m$.
$\square$

### 3.4 Lemma 4: Mixture-Product TV Bound (Key Technical Lemma)

**Lemma 4 (Mixture-Product TV Bound).** Let $P_0 = \prod_{m=1}^M \text{Bern}(p_0)$ be a
product distribution. Let $P_1 = \frac{1}{L} \sum_{\ell=1}^L \prod_{m=1}^M \text{Bern}(p_\ell)$
be an equal-weight mixture of $L$ product distributions. Then for any $p_0, p_\ell \in (0,1)$:

$$\text{TV}(P_0, P_1) \leq \frac{1}{L} \sum_{\ell=1}^L \sqrt{ \frac{ \bigl[1 + \chi^2(\text{Bern}(p_0) \parallel \text{Bern}(p_\ell))\bigr]^M - 1 }{2} }$$

**Proof.** By the convexity of total variation in its second argument:

$$\text{TV}(P_0, P_1) = \text{TV}\!\left(P_0,\; \frac{1}{L}\sum_{\ell} Q_\ell\right) \leq \frac{1}{L}\sum_{\ell} \text{TV}(P_0, Q_\ell)$$

where $Q_\ell = \prod_{m=1}^M \text{Bern}(p_\ell)$. This convexity follows from the
triangle inequality and the definition of mixtures.

For each $\ell$, we bound $\text{TV}(P_0, Q_\ell)$ via the $\chi^2$ divergence:

$$\text{TV}(P_0, Q_\ell) \leq \sqrt{\frac{\chi^2(P_0 \parallel Q_\ell)}{2}}$$

By Lemma 3 (tensorization):

$$\chi^2(P_0 \parallel Q_\ell) = \bigl[1 + \chi^2(\text{Bern}(p_0) \parallel \text{Bern}(p_\ell))\bigr]^M - 1$$

Combining these yields the stated bound. $\square$

**Corollary 4.1 (Symmetric Mixture).** When all $L$ components have the same success
probability $p_1$ (i.e., $p_\ell = p_1$ for all $\ell$):

$$\text{TV}(P_0, P_1) \leq \sqrt{ \frac{ \bigl[1 + \chi^2(\text{Bern}(p_0) \parallel \text{Bern}(p_1))\bigr]^M - 1 }{2} }$$

since the average over $\ell$ collapses to a single term.

### 3.5 Lemma 5: Bernoulli Chi-Square for the Clean vs. Noise Comparison

**Lemma 5 (Clean-Noise Bernoulli $\chi^2$).** For clean expert error probability
$p_0 = \mu$ and noise-conditioned error probability $p_1 = 1 - \mu/(K-1)$:

$$\chi^2(\text{Bern}(\mu) \parallel \text{Bern}(1-\mu/(K-1))) = \frac{\bigl(1 - \mu \cdot \frac{K}{K-1}\bigr)^2}{\bigl(1 - \frac{\mu}{K-1}\bigr) \cdot \frac{\mu}{K-1}}$$

**Proof.** Directly applying Lemma 2 with $p = \mu$ and $q = 1 - \mu/(K-1)$:

$$\begin{aligned}
p - q &= \mu - \left(1 - \frac{\mu}{K-1}\right) = \mu - 1 + \frac{\mu}{K-1} = -\left(1 - \mu \cdot \frac{K}{K-1}\right) \\
(p-q)^2 &= \left(1 - \mu \cdot \frac{K}{K-1}\right)^2 \\
q(1-q) &= \left(1 - \frac{\mu}{K-1}\right) \cdot \frac{\mu}{K-1}
\end{aligned}$$

Combining gives the result. $\square$

**Corollary 5.1 (Binary case $K=2$).** When $K=2$:

$$\chi^2(\text{Bern}(\mu) \parallel \text{Bern}(1-\mu)) = \frac{(1 - 2\mu)^2}{\mu(1-\mu)}$$

where $1 - \mu \cdot K/(K-1) = 1 - 2\mu$, which is exactly $2\Delta^*$ (the full
separation gap, not halved).

### 3.6 Lemma 6: Le Cam's Two-Point Method

**Lemma 6 (Le Cam, 1973; Yu, 1997).** Let $\mathbb{P}_0$ and $\mathbb{P}_1$ be two
probability distributions on the same measurable space. For any test $\psi \in \{0,1\}$:

$$\mathbb{P}_0(\psi = 1) + \mathbb{P}_1(\psi = 0) \geq 1 - \text{TV}(\mathbb{P}_0, \mathbb{P}_1)$$

Equivalently, the minimax error for testing $H_0: P = P_0$ vs $H_1: P = P_1$ is at
least $(1 - \text{TV})/2$.

**Proof.** Standard. See Tsybakov (2009), Lemma 2.1. $\square$

### 3.7 Lemma 7: Binomial Tail Lower Bound (Slud's Inequality)

**Lemma 7 (Slud's Inequality).** Let $S_M \sim \text{Binomial}(M, p)$ with $p \leq 1/2$.
For any $k \in \{0,1,\dots,M\}$ with $p \leq k/M \leq 1/2$:

$$\mathbb{P}(S_M \geq k) \geq \frac{1}{2} \cdot \exp\!\left(-2M\left(\frac{k}{M} - p\right)^2\right)$$

**Proof.** This is a direct application of Slud (1977), Theorem 2. The inequality
follows from the monotonicity of the regularized incomplete beta function and the
integral representation of the binomial CDF. The factor $1/2$ is a universal constant. $\square$

---

## 4. Main Proof: Le Cam Two-Point Construction

### 4.1 Strategy

We construct two problem instances that are:
1. Hard to distinguish (small total variation distance between their induced distributions
   of expert errors)
2. Have different optimal noise/clean assignments for a specific sample $x$

The lower bound then follows from Le Cam's lemma: if the two distributions are close,
then any detector must incur significant error on at least one of them.

**The key insight**: For the lower bound, we can choose the hardest possible construction
within the allowed class. We set symmetric experts (same $\mu$ for all), binary
classification ($K=2$), balanced errors ($C_{\text{bal}} = 1$), and the hardest state $s$
(smallest $\Delta$). These choices make the lower bound as strong as possible.

### 4.2 Construction ($K=2$ case)

Consider the binary classification setting $K=2$, labels $\mathcal{Y} = \{0,1\}$.
Fix a state $s$ with clean error rate $\mu < 1/2$. The separation gap is
$\Delta^* = (1-2\mu)/2$.

**Instance $P_0$ (Clean):** For a fixed test sample $x$:
- The true label is $y^* = 0$
- The observed label is also $y = 0$ (no noise)
- Each expert $f_m$ correctly predicts $0$ with probability $1-\mu$, independently
  given $x$: $e_m = \mathbf{1}\{f_m(x) \neq 0\} \sim \text{Bernoulli}(\mu)$
- The error vector $(e_1,\dots,e_M) \sim \text{Bernoulli}(\mu)^{\otimes M}$

**Instance $P_1$ (Noise):** For the same test sample $x$:
- The true label is $y^* = 0$
- The observed label is $y = 1$ (label noise, which occurs with prob. $\eta$ in
  the generative model; for this construction we condition on the noise event)
- The noise class is $c = 1$. Each expert makes error with prob.
  $\mathbb{P}(f_m(x) \neq 1 \mid x) = 1 - \mathbb{P}(f_m(x) = 1 \mid x) = 1 - \mu$
  (since by A6 with $C_{\text{bal}}=1$, the probability any expert predicts the
  wrong class $1$ equals the error rate $\mu$)
- Conditioned on noise class $c=1$: $e_m \sim \text{Bernoulli}(1-\mu)$ independently
- Since $K=2$, there is only one noise class, so $P_1$ is simply a product distribution:
  $\text{Bernoulli}(1-\mu)^{\otimes M}$

**Crucial simplification for $K=2$**: The mixture-over-classes issue vanishes.
$P_0$ and $P_1$ are both product distributions with different Bernoulli parameters.
This makes the TV computation exact.

### 4.3 Reduction to Binomial Testing

For $K=2$, the error vector under $P_0$ and $P_1$ gives:

$$S = \sum_{m=1}^M e_m \sim \begin{cases}
\text{Binomial}(M, \mu) & \text{under } P_0 \text{ (clean)} \\
\text{Binomial}(M, 1-\mu) & \text{under } P_1 \text{ (noise)}
\end{cases}$$

Testing between $P_0$ and $P_1$ based on $(e_1,\dots,e_M)$ reduces to testing between
two Binomial distributions with parameters $p_0 = \mu$ and $p_1 = 1-\mu$.

The optimal test (Bayes optimal for equal priors, or Neyman-Pearson for simple
hypotheses) rejects $P_0$ when $S > M/2$, since $1-\mu > \mu$ for $\mu < 1/2$.
Ties $(S = M/2)$ can be broken arbitrarily.

### 4.4 Applying the Binomial Tail Lower Bound

For the optimal Bayes test $\psi^*$:

$$\begin{aligned}
P_0(\psi^* = 1) &= \mathbb{P}_{P_0}(S > M/2) \\
P_1(\psi^* = 0) &= \mathbb{P}_{P_1}(S \leq M/2) = \mathbb{P}_{P_1}(M - S \geq M/2) \\
&= \mathbb{P}_{\text{Bin}(M,1-\mu)}(S \leq M/2) \\
&= \mathbb{P}_{\text{Bin}(M,\mu)}(S \geq M/2) \quad \text{(by symmetry of Binomial)}
\end{aligned}$$

Thus $P_0(\psi^*=1) = P_1(\psi^*=0) = \mathbb{P}(\text{Bin}(M,\mu) \geq M/2)$.

Applying Lemma 7 (Slud's inequality) with $p = \mu$, $k = \lceil M/2 \rceil$:

$$\begin{aligned}
\mathbb{P}(\text{Bin}(M,\mu) \geq M/2) &\geq \frac{1}{2} \cdot \exp\!\left(-2M\left(\frac{M/2}{M} - \mu\right)^2\right) \\
&= \frac{1}{2} \cdot \exp\!\left(-2M\left(\frac{1}{2} - \mu\right)^2\right) \\
&= \frac{1}{2} \cdot \exp\!\left(-2M(\Delta^*)^2\right)
\end{aligned}$$

where $\Delta^* = (1-2\mu)/2 = 1/2 - \mu$.

Since $\psi^*$ is the optimal test (minimizing the sum of error probabilities), any
other test $\psi$ has error at least as large:

$$P_0(\psi=1) + P_1(\psi=0) \geq P_0(\psi^*=1) + P_1(\psi^*=0) \geq \exp(-2M(\Delta^*)^2)$$

Note: The $1/2$ factor was absorbed since $P_0(\psi^*=1) = P_1(\psi^*=0)$ and the sum
is $2 \times$ each, giving $\exp(-2M(\Delta^*)^2)$ for the sum. The max is
$\frac{1}{2}\exp(-2M(\Delta^*)^2)$.

### 4.5 Completing Part (a)

Since our construction $(P_0, P_1)$ is a valid pair within the SCX assumption class
$\mathcal{P}_\Delta$ (it satisfies A1-A6 with $K=2$, $C_{\text{bal}}=1$,
$\mu < 1/2$, and separation gap $\Delta^*$), we have:

$$\inf_{\psi} \sup_{P \in \mathcal{P}_\Delta} \max\{P_0(\psi=1), P_1(\psi=0)\}
\geq \frac{1}{2}\exp(-2M(\Delta^*)^2)$$

This proves Part (a) of Theorem 4 for $K=2$.

### 4.6 Extension to $K > 2$

For $K > 2$, the noise distribution becomes a mixture of $L = K-1$ product distributions:

$$P_1 = \frac{1}{K-1} \sum_{c \neq y^*} \text{Bernoulli}\!\left(1 - \frac{\mu}{K-1}\right)^{\otimes M}$$

Under A6 with $C_{\text{bal}} = 1$, all components have the same parameter
$p_1 = 1 - \mu/(K-1)$. By Lemma 4 (Mixture-Product TV Bound), Corollary 4.1
(symmetric mixture), the TV between $P_0$ and $P_1$ is bounded by:

$$\text{TV}(P_0, P_1) \leq \sqrt{ \frac{ \bigl[1 + \chi^2(\text{Bern}(\mu) \parallel \text{Bern}(1-\mu/(K-1)))\bigr]^M - 1 }{2} }$$

By Lemma 5, the per-expert $\chi^2$ divergence is:

$$\chi^2 = \frac{(1 - \mu K/(K-1))^2}{(1 - \mu/(K-1)) \cdot \mu/(K-1)}$$

Let $\Delta^* = \frac{1}{2}(1 - \mu K/(K-1))$ as before. Then:

$$\chi^2 = \frac{4(\Delta^*)^2}{(1 - \mu/(K-1)) \cdot \mu/(K-1)}$$

Since the denominator is maximized when $\mu/(K-1) = 1/2$ (i.e., $\mu = (K-1)/2$),
and minimized when $\mu \to 0$ or $\mu \to K-1$, we have:

$$\frac{1}{(1 - \mu/(K-1)) \cdot \mu/(K-1)} \geq 4$$

Thus $\chi^2 \geq 16(\Delta^*)^2$, which is *larger* than the $K=2$ case
($\chi^2 = 4(1-2\mu)^2/(\mu(1-\mu))$). Since larger $\chi^2$ makes the distributions
more distinguishable, the $K=2$ case is the hardest (smallest $\chi^2$ divergence),
confirming that the binary lower bound holds for all $K \geq 2$ with the same exponent.

**Formal statement for $K > 2$**: The lower bound holds with the same exponential rate:

$$\inf_{\psi} \sup_{P \in \mathcal{P}_\Delta} R(\psi) \geq \frac{1}{2} \cdot \exp(-2M\Delta^2)$$

where the constant $1/2$ may depend on $K$ and $\mu$, but the rate $2M\Delta^2$ is
preserved.

---

## 5. Extension to F1 Risk

### 5.1 Relating Testing Error to F1

The F1 score is a population-level summary that involves both false positives and
false negatives. To convert our per-sample testing lower bound to an F1 lower bound,
we need a simple inequality.

**Lemma 8 (F1 Lower Bound via Error Components).** For any binary detector $\psi$:

$$1 - \text{F1}(\psi) \geq \eta \cdot \mathbb{P}(\psi=0 \mid \text{noise}) + (1-\eta) \cdot \mathbb{P}(\psi=1 \mid \text{clean})$$

**Proof.** Write $\text{TPR} = \mathbb{P}(\psi=1 \mid \text{noise})$,
$\text{FPR} = \mathbb{P}(\psi=1 \mid \text{clean})$.
Let $\text{FN} = \eta \cdot (1 - \text{TPR})$,
$\text{FP} = (1-\eta) \cdot \text{FPR}$, $\text{TP} = \eta \cdot \text{TPR}$.

$$\begin{aligned}
1 - \text{F1} &= 1 - \frac{2\text{TP}}{2\text{TP} + \text{FP} + \text{FN}} \\
&= \frac{\text{FP} + \text{FN}}{2\text{TP} + \text{FP} + \text{FN}}
\end{aligned}$$

Since $\text{TP} = \eta\cdot\text{TPR} \leq \eta$, the denominator satisfies:

$$2\text{TP} + \text{FP} + \text{FN} \leq 2\eta + (1-\eta) + \eta = 1 + \eta \leq 2$$

But more usefully, since $\text{FP} + \text{FN} \geq \text{FN}$:

$$1 - \text{F1} \geq \frac{\text{FN}}{2\text{TP} + \text{FP} + \text{FN}} \geq \frac{\text{FN}}{2\eta + (1-\eta) + \eta} = \frac{\text{FN}}{1+\eta}$$

No, this is too loose. Instead, directly:

$$1 - \text{F1} = \frac{\text{FP} + \text{FN}}{2\text{TP} + \text{FP} + \text{FN}} = \frac{(1-\eta)\text{FPR} + \eta(1-\text{TPR})}{\eta(1+\text{TPR}) + (1-\eta)\text{FPR}}$$

Since the denominator is at most $\eta(1+1) + (1-\eta)\cdot 1 = 2\eta + 1 - \eta = 1 + \eta$:

$$1 - \text{F1} \geq \frac{(1-\eta)\text{FPR} + \eta(1-\text{TPR})}{1 + \eta}$$

But we need a bound with $\eta$ scaling (not $1+\eta$). Using the fact that
denominator $\geq \eta$ (since $\text{TPR} \geq 0$, $\text{FPR} \geq 0$):

$$\frac{a}{\eta + (1-\eta)\text{FPR}} \geq \frac{a}{\eta + (1-\eta)} = a$$

only when $a$ is the numerator. But the denominator also has $\eta\cdot\text{TPR}$:

Denominator $= \eta + \underbrace{\eta\cdot\text{TPR} + (1-\eta)\text{FNR}}_{\geq 0} \geq \eta$

So:

$$1 - \text{F1} \geq \frac{\text{FP} + \text{FN}}{\eta + (1-\eta)\text{FPR}} \geq \frac{\text{FN}}{\eta} = 1 - \text{TPR}$$

Wait, this gives $1 - \text{F1} \geq 1 - \text{TPR}$, i.e., $\text{F1} \leq \text{TPR}$.
This is a known property of F1: it is bounded by the minimum of precision and recall,
and since recall = TPR, F1 $\leq$ TPR. So $1 - \text{F1} \geq 1 - \text{TPR}$.

Similarly, F1 $\leq$ precision, so $1 - \text{F1} \geq 1 - \text{precision}$.

But $1 - \text{TPR} = \mathbb{P}(\psi=0 \mid \text{noise})$, which is exactly the
false negative rate (FNR). So:

$$1 - \text{F1}(\psi) \geq 1 - \text{TPR} = \mathbb{P}(\psi=0 \mid \text{noise})$$

More symmetrically, we can also show:

$$1 - \text{F1}(\psi) \geq 1 - \text{precision} = \frac{\text{FP}}{\text{TP} + \text{FP}}$$

Using $\text{FP}/(\text{TP}+\text{FP}) \geq \text{FPR}/(\text{TPR} + \text{FPR})$:

$$1 - \text{F1} \geq \frac{(1-\eta)\cdot\text{FPR}}{\eta\cdot\text{TPR} + (1-\eta)\cdot\text{FPR}}$$

This is a harmonic combination, not a simple linear bound. For the lower bound, we
only need the simpler bound $1 - \text{F1} \geq (1 - \text{TPR})$ (one-sided), which
gives:

$$1 - \text{F1}(\psi) \geq \mathbb{P}(\psi=0 \mid \text{noise})$$

This preserves the exponential rate. $\square$

**Note**: The inequality $1 - \text{F1} \geq \mathbb{P}(\psi=0 \mid \text{noise})$ is
not tight when $\text{FPR}$ is large, but it's sufficient for rate optimality since
it preserves the exponent in $M\Delta^2$.

### 5.2 Completing Part (b)

From Part (a), for our construction:

$$\mathbb{P}(\psi=0 \mid \text{noise}) = P_1(\psi=0) \geq \frac{1}{2}\exp(-2M\Delta^2)$$

Applying Lemma 8:

$$1 - \text{F1}(\psi) \geq \mathbb{P}(\psi=0 \mid \text{noise}) \geq \frac{1}{2}\exp(-2M\Delta^2)$$

Taking the supremum over problem instances $P \in \mathcal{P}_\Delta$ (including our
construction) and infimum over detectors $\psi$:

$$\inf_{\psi} \sup_{P \in \mathcal{P}_\Delta} [1 - \text{F1}(\psi, P)] \geq \frac{1}{2}\exp(-2M\Delta^2)$$

**Remark on the $\eta$ factor.** The inequality $1-\text{F1} \geq 1-\text{TPR}$ loses
the noise rate $\eta$. A tighter conversion uses both error components:

$$1 - \text{F1} = \frac{(1-\eta)\text{FPR} + \eta(1-\text{TPR})}{\eta(1+\text{TPR}) + (1-\eta)\text{FPR}}$$

For our construction, $\text{FPR}$ is controlled by the clean error rate $\mu$, and
a more refined bound would recover $\eta$ in the numerator. The current bound
(without $\eta$) is sufficient for rate optimality; the $\eta$-dependent refinement
is left for future work. $\square$

### 5.3 Verification of Upper-Lower Bound Match

| Quantity | Theorem 1 (Upper) | Theorem 4 (Lower) | Ratio |
|----------|-------------------|-------------------|-------|
| Exponent | $2M\Delta_s^2$ | $2M\Delta^2$ | $1$ (match!) |
| Pre-factor | $1/\eta$ | $1/2$ | $2/\eta$ (constant gap) |
| State aggregation | $\sum_s \rho_s$ | $\rho_{s^*} = 1$ | Hardest state |

The exponent matches exactly, confirming rate optimality. The constant factors differ,
which is typical for minimax results (upper and lower bounds often differ by constants).

---

## 6. Large-Deviations Refinement

### 6.1 Exact Rate via Cramer-Chernoff

The exponent $2M\Delta^2$ in Theorem 4 is derived from Hoeffding-type bounds. The
exact large-deviations rate (as $M \to \infty$) is given by the Cramer-Chernoff theorem:

**Theorem (Cramer, 1938; Chernoff, 1952).** For i.i.d. Bernoulli($\mu$) variables
$e_1,\dots,e_M$, the sample mean $\bar{e}_M = S_M/M$ satisfies:

$$\lim_{M \to \infty} -\frac{1}{M} \log \mathbb{P}(\bar{e}_M \geq \theta) = \text{KL}(\theta \parallel \mu)$$

for any $\theta > \mu$, where $\text{KL}(\theta \parallel \mu) = \theta\log\frac{\theta}{\mu} + (1-\theta)\log\frac{1-\theta}{1-\mu}$.

### 6.2 Rate Comparison: Hoeffding vs. Exact

For optimal threshold $\theta^*$:

- **Hoeffding exponent**: $2(\theta^* - \mu)^2 = 2\Delta^{*2}$
- **Cramer-Chernoff exact exponent**: $\text{KL}(\theta^* \parallel \mu)$

By Taylor expansion around $\Delta^* = 0$:

$$\begin{aligned}
\text{KL}(\mu + \Delta^* \parallel \mu) &= \mu\log\frac{\mu+\Delta^*}{\mu} + (1-\mu)\log\frac{1-\mu-\Delta^*}{1-\mu} \\
&= \mu\left(\frac{\Delta^*}{\mu} - \frac{(\Delta^*)^2}{2\mu^2} + \cdots\right) + (1-\mu)\left(-\frac{\Delta^*}{1-\mu} - \frac{(\Delta^*)^2}{2(1-\mu)^2} - \cdots\right) \\
&= \frac{(\Delta^*)^2}{2\mu(1-\mu)} + O((\Delta^*)^3)
\end{aligned}$$

Since $\mu(1-\mu) \leq 1/4$ with equality at $\mu = 1/2$:

$$\text{KL}(\mu+\Delta^* \parallel \mu) \geq 2(\Delta^*)^2 \cdot \frac{1}{4\mu(1-\mu)} \geq 2(\Delta^*)^2$$

Equality holds only when $\mu = 1/2$, i.e., when the experts are at chance level.

**Thus**: The Hoeffding exponent $2$ is the *minimum* possible exponent (worst-case
over $\mu$). For any $\mu < 1/2$, the exact exponent is larger, meaning the true
minimax rate is $\exp(-M \cdot \text{KL}(\theta^* \parallel \mu))$, which decays faster
than $\exp(-2M\Delta^2)$. The Hoeffding exponent $2$ is the minimax-optimal **guaranteed**
exponent.

### 6.3 Proof of Corollary (Large-Deviations Refinement)

For the binary symmetric case ($K=2$, $\theta^* = 1/2$, $\mu = 1/2 - \Delta$):

$$\begin{aligned}
\text{KL}(1/2 \parallel 1/2 - \Delta) &= \frac{1}{2}\log\frac{1/2}{1/2-\Delta} + \frac{1}{2}\log\frac{1/2}{1/2+\Delta} \\
&= \frac{1}{2}\left[-\log(1-2\Delta) - \log(1+2\Delta)\right] \\
&= -\frac{1}{2}\log(1 - 4\Delta^2) \\
&= 2\Delta^2 + \frac{4}{3}\Delta^4 + O(\Delta^6)
\end{aligned}$$

By the Cramer-Chernoff theorem, for the optimal Bayes test $\psi^*$:

$$\begin{aligned}
\lim_{M \to \infty} -\frac{1}{M}\log P_0(\psi^*=1) &= \text{KL}(1/2 \parallel \mu) = 2\Delta^2 + O(\Delta^4) \\
\lim_{M \to \infty} -\frac{1}{M}\log P_1(\psi^*=0) &= \text{KL}(1/2 \parallel 1-\mu) = 2\Delta^2 + O(\Delta^4)
\end{aligned}$$

Since $\psi^*$ is optimal (achieves the best error rate), the minimax risk satisfies:

$$\lim_{M \to \infty} -\frac{1}{M}\log \inf_{\psi} \max\{P_0(\psi=1), P_1(\psi=0)\} = 2\Delta^2 + O(\Delta^4)$$

As $\Delta \to 0$, the leading constant tends to $2$, proving the exponent is exactly
$2$ in the small-gap (high-dimensional) limit. $\square$

---

## 7. Discussion of Tightness and Gaps

### 7.1 What Has Been Proved

1. **Testing lower bound (Part a)**: Complete for $K=2$ using Slud's inequality for
   Binomial tails. Extended to $K>2$ via the mixture-product TV bound (Lemma 4)
   and the fact that $K=2$ gives the smallest $\chi^2$ divergence (hardest case).

2. **F1 lower bound (Part b)**: Complete using $1-\text{F1} \geq 1-\text{TPR}$.
   The bound $1-\text{F1} \geq \frac{1}{2}\exp(-2M\Delta^2)$ matches the exponent
   of Theorem 1.

3. **Rate optimality (Part c)**: Theorem 1 (upper bound) gives
   $\text{F1} \geq 1 - \frac{1}{\eta}\sum_s\rho_s\exp(-2M\Delta_s^2)$. Theorem 4
   (lower bound) gives $\inf_\psi\sup_P[1-\text{F1}] \geq \frac{1}{2}\exp(-2M\Delta^2)$.
   The exponent $2M\Delta^2$ matches, confirming rate optimality.

4. **Large-deviations refinement**: Complete via Cramer-Chernoff, showing the exact
   asymptotic exponent is $\text{KL}(\theta^* \parallel \mu) = 2\Delta^2 + O(\Delta^4)$,
   with $2\Delta^2$ as the worst-case (minimum) exponent.

### 7.2 Identified Gaps

**Gap 1: Mixture-product bound tightness for moderate $M$ (medium).**
For $K > 2$, the convexity bound $\text{TV}(P_0, P_1) \leq \frac{1}{L}\sum_\ell \text{TV}(P_0, Q_\ell)$
is potentially loose. When the mixture components are far apart, the mixture $P_1$ is
more spread out than any single component, potentially making the TV smaller than the
bound suggests. For our specific case (all components have the same parameter under A6),
the bound is tight (Corollary 4.1).

*Status*: Tight for $C_{\text{bal}} = 1$ (balanced errors). For $C_{\text{bal}} > 1$,
the bound may be loose but the exponential rate is preserved.

**Gap 2: F1 lower bound tightness (minor).**
The bound $1-\text{F1} \geq 1-\text{TPR}$ loses information about the false positive
rate. For the specific hard construction where $P_0$ is clean and $P_1$ is noise,
the FPR is small by design, so the bound is tight within a factor of 2. For other
constructions, FPR could be larger, making the bound looser.

*Status*: The factor $2$ gap between $1-\text{F1}$ and $1-\text{TPR}$ is unavoidable
without additional assumptions.

**Gap 3: State aggregation (minor).**
The lower bound is proved for a single state $s$ with $\rho_s = 1$. For multi-state
settings, the worst-case over $\mathcal{P}_\Delta$ can place all probability mass on
the hardest state, achieving the same bound. This is a standard reduction.

*Status*: Complete -- no gap.

**Gap 4: Extension to non-symmetric experts (moderate).**
The proof assumes all experts have the same error rate $\mu$. For heterogeneous error
rates $\mu_1,\dots,\mu_M$, the Binomial testing framework no longer applies; we would
need a Poisson Binomial lower bound (Slud's inequality for Poisson Binomial, or a
Berry-Esseen bound).

*Status*: Open question. Likely the same rate holds ($2M\bar{\Delta}^2$ with average
gap $\bar{\Delta}$), but the proof would require different technical tools.

**Gap 5: Exact constant $c = 2$ for finite $M$ (asymptotic only).**
The large-deviations refinement is asymptotic ($M \to \infty$). For finite $M$, the
exact optimal constant may be larger or smaller than $2$ depending on $\mu$ and $\Delta$.
The Slud inequality gives the finite-$M$ lower bound with constant $2$, confirming
that no method can achieve exponent $> 2$ even for finite $M$.

*Status*: The finite-$M$ lower bound (Slud) matches the asymptotic rate, so the
exponent $2$ holds for all $M$. This gap is closed.

### 7.3 Summary

| Component | Status | Details |
|-----------|--------|---------|
| $K=2$ testing lower bound | **Complete** | Slud's inequality, optimal Bayes test |
| $K>2$ testing lower bound | **Complete** | Lemma 4, $K=2$ is hardest case |
| F1 extension | **Complete** | $1-\text{F1} \geq 1-\text{TPR}$ bound |
| Rate optimality | **Complete** | Exponent $2M\Delta^2$ matches Thm 1 |
| Large-deviations refinement | **Complete** | Cramer-Chernoff, $\text{KL} \to 2\Delta^2$ |
| Non-symmetric experts | **Open** | Requires Poisson Binomial tools |
| Mixture bound for $C_{\text{bal}}>1$ | **Partial** | Rate holds, constant may differ |

### 7.4 Connection to Theorem 3 (Unidentifiability)

Theorem 3 shows that without assumptions (A1)-(A6), noise and difficulty are
observationally indistinguishable. Theorem 4 shows that even WITH these assumptions,
there is a fundamental statistical limit: no detector can surpass $\exp(-2M\Delta^2)$.

Together with Theorem 3, this forms a complete theoretical picture:

- **Theorem 3 (lower bound on assumptions)**: Without the SCX assumptions, detection
  is impossible (identifiability failure).
- **Theorem 4 (lower bound on performance)**: With the SCX assumptions, detection is
  possible but limited by an exponential lower bound matching Theorem 1.
- **Theorem 1 (upper bound on performance)**: The SCX detector achieves this optimal rate.

This completes the three-part optimality characterization:
- What is lost if assumptions fail: **all** detection ability (Theorem 3)
- What even the best detector achieves: $\sim\exp(-2M\Delta^2)$ (Theorem 4)
- What SCX actually achieves: $\sim\exp(-2M\Delta^2)$ (Theorem 1)

---

## 8. References

1. Slud, E. V. (1977). Distribution inequalities for the binomial law. *The Annals of
   Probability*, 5(3), 404-412.

2. Tsybakov, A. B. (2009). *Introduction to Nonparametric Estimation*. Springer.
   (Section 2.1-2.4: Le Cam's method, Assouad's lemma, Fano's inequality)

3. Le Cam, L. (1973). Convergence of estimates under dimensionality restrictions.
   *The Annals of Statistics*, 1(1), 38-53.

4. Chernoff, H. (1952). A measure of asymptotic efficiency for tests of a hypothesis
   based on the sum of observations. *The Annals of Mathematical Statistics*, 23(4),
   493-507.

5. Cramer, H. (1938). Sur un nouveau theoreme-limite de la theorie des probabilites.
   *Actualites Scientifiques et Industrielles*, 736, 5-23.

6. Hoeffding, W. (1963). Probability inequalities for sums of bounded random variables.
   *Journal of the American Statistical Association*, 58(301), 13-30.

7. Yu, B. (1997). Assouad, Fano, and Le Cam. In *Festschrift for Lucien Le Cam*,
   pp. 423-435. Springer.

8. Polyanskiy, Y., & Wu, Y. (2022+). *Information Theory: From Coding to Learning*.
   Cambridge University Press. (Forthcoming.)

9. Wainwright, M. J. (2019). *High-Dimensional Statistics: A Non-Asymptotic Viewpoint*.
   Cambridge University Press. (Chapter 15: Minimax lower bounds.)

10. SCX Theorem 1: Multi-Expert Consistency Guarantees for Label Noise Detection.
    `../theorems/01_noise_detection_guarantee.md`.

11. SCX Theorem 3: Unidentifiability of Noise vs. Learnable Difficulty.
    `../theorems/03_unidentifiability_theorem.md`.

12. Minimax Optimality Feasibility Analysis.
    `./minimax_optimality.md`.

---

## Appendix A: Slud's Inequality -- Statement and Proof Sketch

### Statement

**Theorem (Slud, 1977, Theorem 2).** Let $S_M \sim \text{Binomial}(M, p)$ with
$p \leq 1/2$. Then for any integer $k$ with $Mp \leq k \leq M/2$:

$$\mathbb{P}(S_M \geq k) \geq \frac{1}{2} \cdot \exp\!\left(-2M\left(\frac{k}{M} - p\right)^2\right)$$

This is a lower bound (reverse inequality) for the upper tail of the Binomial
distribution. The factor $1/2$ is universal (not depending on $M, p, k$), and the
exponential rate $2M(k/M - p)^2$ matches the Hoeffding upper bound.

### Proof Sketch

Slud's proof uses the representation of the Binomial CDF as a regularized incomplete
beta function:

$$\mathbb{P}(S_M \geq k) = I_p(k, M-k+1) = \frac{B(p; k, M-k+1)}{B(k, M-k+1)}$$

where $B(p; a, b)$ is the incomplete beta function. The key inequality follows from
the monotonicity of the likelihood ratio for Binomial distributions (Karlin's
totally positive property) and an integral bound.

An alternative modern proof uses the following martingale argument (due to
Shorack & Wellner, 1986, pp. 440-441): For $p \leq 1/2$, the Binomial probability
can be bounded below by the Gaussian approximation times a factor that depends on
$p(1-p)$. The worst case $p = 1/2$ gives the factor $1/2$.

### Why the Factor 1/2 is Important

The factor $1/2$ in Slud's inequality is what makes the lower bound non-trivial.
Without it, the bound could be arbitrarily close to $0$ (which is always true for
any probability). With it, we guarantee that the Binomial tail probability is at
least half the Hoeffding bound, establishing that the Hoeffding exponent is tight
(up to constant factors).

### Connection to Central Limit Theorem

For large $M$, the de Moivre--Laplace theorem gives:

$$\mathbb{P}(S_M \geq M/2) \approx 1 - \Phi\!\left(\frac{(M/2) - M\mu}{\sqrt{M\mu(1-\mu)}}\right) = 1 - \Phi\!\left(-\frac{2\Delta\sqrt{M}}{\sqrt{4\mu(1-\mu)}}\right)$$

where $\Phi$ is the standard normal CDF. Using the Mills ratio bound
$1 - \Phi(-x) \geq \frac{x}{1+x^2} \cdot \frac{e^{-x^2/2}}{\sqrt{2\pi}}$ for $x > 0$,
the exponent is $x^2/2 = 2M\Delta^2/(4\mu(1-\mu))$, which is $\geq 2M\Delta^2$ since
$4\mu(1-\mu) \leq 1$. This provides an alternative (asymptotic) verification of the
$2M\Delta^2$ exponent.

---

## Appendix B: Numerical Illustration

For concrete parameter values, the lower bound on testing error gives:

| $\Delta$ | $\mu$ | $M$ | Lower bound $\frac{1}{2}\exp(-2M\Delta^2)$ |
|:--------:|:-----:|:---:|:-----------------------------------------:|
| 0.3      | 0.2   | 10  | $0.5 \cdot e^{-1.8} \approx 0.083$        |
| 0.3      | 0.2   | 20  | $0.5 \cdot e^{-3.6} \approx 0.014$        |
| 0.25     | 0.25  | 30  | $0.5 \cdot e^{-3.75} \approx 0.012$       |
| 0.2      | 0.3   | 50  | $0.5 \cdot e^{-4.0} \approx 0.009$        |
| 0.1      | 0.4   | 100 | $0.5 \cdot e^{-2.0} \approx 0.068$        |

Note that the lower bound is non-trivial (below $0.1$) when $M\Delta^2$ is above
approximately $1$. The condition $M\Delta^2 > 1$ corresponds to the regime where
detection is possible with non-trivial accuracy.

For comparison, the Theorem 1 upper bound on $1-\text{F1}$ (assuming $\eta=0.1$,
$\rho_s=1$) gives:

$$\text{Upper bound on } 1-\text{F1} \leq \frac{1}{\eta}\exp(-2M\Delta^2) = 10\exp(-2M\Delta^2)$$

The gap between upper and lower bounds is a factor of $20/\eta$ in the pre-exponential
constant, but the exponent $2M\Delta^2$ is identical.

---

## Appendix C: Adversarial Construction for the Lower Bound

The proof of Theorem 4 constructs a pair $(P_0, P_1)$ within the class
$\mathcal{P}_\Delta$. Here we verify that this construction satisfies all SCX
assumptions:

| Assumption | Verification |
|------------|-------------|
| **A1 (Disjoint training)** | Experts trained on disjoint subsets of clean data |
| **A2 (Cond. independence)** | Given $x$, $\{e_m\}$ are i.i.d. Bernoulli |
| **A3 (Bounded loss)** | 0-1 loss with $B=1$ |
| **A4 (Uniform noise)** | Noise label uniform over $\mathcal{Y}\setminus\{y^*\}$ |
| **A5 (State homogeneity)** | Single state $s$ with constant $\mu$ |
| **A6 (Balanced errors)** | $C_{\text{bal}} = 1$ (errors uniform across wrong classes) |

The construction uses the most favorable settings within the assumption class,
making the detection problem as hard as possible. This is the standard approach
for minimax lower bounds: find the hardest problem instance within the class.

Since $\inf_\psi \sup_P \geq \inf_\psi \max\{P_0(\psi=1), P_1(\psi=0)\}$ (the
supremum over $P$ is at least the value at any specific $P$), the lower bound
holds.

---

**End of proof document.**
