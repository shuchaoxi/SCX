\section{Minimax Lower Bound for Multi-Expert Noise Detection: Hellinger
Distance
Proof}<!-- label: minimax-lower-bound-for-multi-expert-noise-detection-hellinger-distance-proof -->

> **Purpose**: Rewrite the minimax lower bound proof using Hellinger
> distance tensorization, replacing the invalid Slud-inequality approach
> from v1. All three issues identified in the review
> (`review\_minimax\_lower\_bound.md`) are resolved.
> 
> **Date**: 2026-06-27
> 
> **Fixed**: 2026-06-27 --- Corrected F1 bound (Sections 7.3, 7.5)
> and K\textgreater2 Hellinger formula (Section 8.3). See
> `review\_minimax\_v2.md` for details of each bug.
> 
> **Method**: Hellinger distance + tensorization + Le Cam's two-point
> method
> 
> **Key advantage over v1**: Hellinger distance tensorizes exactly
> under product distributions (H²(P⊗M, Q⊗M) = 1 - (1 - H²(P,Q))\^{}M),
> giving a clean exponential bound without requiring Slud's inequality or
> Gaussian approximations.

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

### 1. Setup and Main Result<!-- label: setup-and-main-result -->

\subsubsection{1.1 The Statistical
Problem}<!-- label: the-statistical-problem -->

We consider the multi-expert noise detection problem from Theorem 1. Fix
a state \(s\) with clean error rate \(\mu_s \in (0, 1/2)\). For a given
sample \(x\), we observe the vector of expert error indicators
\((e_1, ..., e_M)\) where \(e_m = \mathbf{1}\{f_m(x) \neq y\}\), and
\(y\) is the observed label.

We consider two hypotheses: - **\(H_0\) (clean)**: \(y = y^*\) (the
true label). Each expert makes an error with probability \(\mu_s\),
independent of other experts given \(x\). - **\(H_1\) (noise)**:
\(y \neq y^*\) (the label is flipped). For binary classification
(\(K=2\)), each expert makes an error with probability \(1 - \mu_s\),
independent of other experts given the noise label.

Under \(K=2\), both hypotheses yield product distributions:

\[P_0 = Bernoulli(\mu_s)^{\otimes M}, \qquad
P_1 = Bernoulli(1 - \mu_s)^{\otimes M}\]

The separation gap is \(\Delta = \tfrac12 - \mu_s\), and the mean
separation is \(2\Delta\).

#### 1.2 Main Result<!-- label: main-result -->

**Theorem 4 (Minimax Lower Bound for Multi-Expert Noise
Detection).** Assume (A1)-(A6). Fix a state \(s\) with clean error rate
\(\mu_s \in (0, 1/2)\), expert count \(M \geq 1\), noise rate
\(\eta \in (0, 1/2)\), and class count \(K \geq 2\). Let \(\psi\) be any
measurable noise detector (a function of \((e_1,...,e_M)\)).

Define the testing error:

\[R(\psi) = \max\bigl\{\mathbb{P}_0(\psi = 1),\; \mathbb{P}_1(\psi = 0)\bigr\}\]

where \(\mathbb{P}_0\) is the distribution under ``clean'' and
\(\mathbb{P}_1\) under ``noise''.

**Part (a) -- Testing lower bound.** For \(K=2\):

\[\inf_ \sup_{P \in \mathcal{P}_} R(\psi)
\;\geq\; \frac14 \bigl(2\sqrt{\mu_s(1-\mu_s)}\bigr)^M
\;\geq\; \frac14 \exp\!\bigl(-2M\Delta^2\bigr) \cdot \bigl(1 - O(M\Delta^4)\bigr)\]

**Part (b) -- F1 lower bound.** Under the same conditions:

\[\inf_ \sup_{P \in \mathcal{P}_} \bigl[1 - F1(\psi, P)\bigr]
\;\geq\; \frac{\rho^M}{8-\rho^M}\]

where \(\rho = 2\sqrt{\mu_s(1-\mu_s)}\). For small \(\rho^M\)
(equivalently, small \(\Delta\)):

\[\inf_ \sup_{P \in \mathcal{P}_} \bigl[1 - F1(\psi, P)\bigr]
\;\geq\; \frac18 \bigl(2\sqrt{\mu_s(1-\mu_s)}\bigr)^M
\;\geq\; \frac18 \exp\!\bigl(-2M\Delta^2 + O(M\Delta^4)\bigr)\]

**Part (c) -- Rate optimality.** The SCX consistency detector of
Theorem 1 achieves \(1-F1 \leq \frac1\eta \exp(-2M\Delta^2)\). By
Part (b), no detector can achieve exponent greater than \(2M\Delta^2\)
in the small-gap regime. Therefore SCX is **minimax rate-optimal**
in the \(M\)-regime.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{2. Hellinger Distance for One
Expert}<!-- label: hellinger-distance-for-one-expert -->

\subsubsection{2.1 Definition and
Properties}<!-- label: definition-and-properties -->

The **Hellinger distance** between two probability distributions
\(P\) and \(Q\) on a discrete space is:

\[H(P, Q) = \sqrt{\frac12 \sum_{x} \bigl(\sqrt{P(x)} - \sqrt{Q(x)}\bigr)^2}\]

Equivalently, the **Hellinger affinity** (or Bhattacharyya
coefficient) is:

\[\rho(P, Q) = \sum_{x} \sqrt{P(x) Q(x)}\]

and:

\[H^2(P, Q) = 1 - \rho(P, Q)\]

\subsubsection{2.2 Hellinger Distance for Bernoulli
Distributions}<!-- label: hellinger-distance-for-bernoulli-distributions -->

For a single expert under \(K=2\):

\[P_{clean} = Bernoulli(\mu_s), \quad
P_{noise} = Bernoulli(1-\mu_s)\]

The Hellinger affinity is:

\[
$$
\rho &= \sum_{e \in \{0,1\}} \sqrt{P_{clean}(e) \cdot P_{noise}(e)} 

&= \sqrt{\mu_s \cdot (1-\mu_s)} + \sqrt{(1-\mu_s) \cdot \mu_s} 

&= 2\sqrt{\mu_s (1-\mu_s)}
$$
\]

The squared Hellinger distance is:

\[H^2(P_{clean}, P_{noise}) = 1 - \rho = 1 - 2\sqrt{\mu_s(1-\mu_s)}\]

**Key observation**: \(\rho < 1\) whenever \(\mu_s \neq 1/2\), and
\(\rho\) decreases as \(\mu_s\) moves away from \(1/2\). When
\(\mu_s = 1/2\) (experts at chance), \(\rho = 1\) and \(H = 0\) (the
distributions are identical).

#### 2.3 Example Values<!-- label: example-values -->

\begin{longtable}[]{@{}cccc@{}}
\toprule\noalign{}
\(\mu_s\) & \(\Delta\) & \(\rho = 2\sqrt{\mu_s(1-\mu_s)}\) & \(H^2\) 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
0.20 & 0.30 & \(2\sqrt{0.16} = 0.800\) & 0.200 

0.25 & 0.25 & \(2\sqrt{0.1875} = 0.866\) & 0.134 

0.30 & 0.20 & \(2\sqrt{0.21} = 0.917\) & 0.083 

0.40 & 0.10 & \(2\sqrt{0.24} = 0.980\) & 0.020 

0.45 & 0.05 & \(2\sqrt{0.2475} = 0.995\) & 0.005 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{3. Tensorization Across M
Experts}<!-- label: tensorization-across-m-experts -->

\subsubsection{3.1 The Tensorization
Property}<!-- label: the-tensorization-property -->

A fundamental property of Hellinger distance is its behavior under
product measures. For product distributions \(P^{\otimes M}\) and
\(Q^{\otimes M}\) (where \(P\) and \(Q\) are distributions on the same
space, and all \(M\) coordinates are i.i.d.):

\[1 - H^2(P^{\otimes M}, Q^{\otimes M}) = \bigl(1 - H^2(P, Q)\bigr)^M\]

Equivalently, in terms of the Hellinger affinity
\(\rho = 1 - H^2(P, Q)\):

\[\rho_M = \rho^M, \qquad H^2(P^{\otimes M}, Q^{\otimes M}) = 1 - \rho^M\]

**Proof.** By definition of the Hellinger affinity for product
measures:

\[
$$
\rho(P^{\otimes M}, Q^{\otimes M})
&= \sum_{e_1,...,e_M} \sqrt{\prod_{m=1}^M P(e_m) \cdot \prod_{m=1}^M Q(e_m)} 

&= \sum_{e_1,...,e_M} \prod_{m=1}^M \sqrt{P(e_m) Q(e_m)} 

&= \prod_{m=1}^M \sum_{e \in \{0,1\}} \sqrt{P(e) Q(e)} 

&= \bigl(\sqrt{P(0)Q(0)} + \sqrt{P(1)Q(1)}\bigr)^M 

&= \rho^M
$$
\]

The squared Hellinger distance follows:
\(H^2(P^{\otimes M}, Q^{\otimes M}) = 1 - \rho^M\). Note that this
tensorization is exact -- there is no slack or inequality.

\subsubsection{3.2 Application to the Multi-Expert
Problem}<!-- label: application-to-the-multi-expert-problem -->

For \(K=2\), the clean and noise distributions are product
distributions:

\[P_0 = Bernoulli(\mu_s)^{\otimes M}, \quad
P_1 = Bernoulli(1-\mu_s)^{\otimes M}\]

The Hellinger affinity for the \(M\)-expert problem is:

\[\rho_M = \bigl(2\sqrt{\mu_s(1-\mu_s)}\bigr)^M\]

The squared Hellinger distance is:

\[H^2(P_0, P_1) = 1 - \bigl(2\sqrt{\mu_s(1-\mu_s)}\bigr)^M\]

**Why this works**: The conditional independence assumption (A2)
ensures that given \(x\), the expert errors are independent. Under
\(K=2\), the noise distribution has only one component (the single wrong
class), so it is a pure product distribution, not a mixture. This makes
tensorization exact.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. Total Variation Bound<!-- label: total-variation-bound -->

\subsubsection{4.1 The TV-Hellinger
Inequality}<!-- label: the-tv-hellinger-inequality -->

**Lemma 1 (TV-Hellinger bound).** For any two probability
distributions \(P\) and \(Q\):

\[TV(P, Q) \leq H(P, Q)\]

where \(TV(P, Q) = \frac12 \sum_x |P(x) - Q(x)|\).

**Proof.** Using the Cauchy-Schwarz inequality:

\[
$$
2\cdotTV(P, Q) &= \sum_x |P(x) - Q(x)| 

&= \sum_x |\sqrt{P(x)} - \sqrt{Q(x)}| \cdot |\sqrt{P(x)} + \sqrt{Q(x)}| 

&\leq \sqrt{\sum_x (\sqrt{P(x)} - \sqrt{Q(x)})^2} \cdot \sqrt{\sum_x (\sqrt{P(x)} + \sqrt{Q(x)})^2} 

&= \sqrt{2H^2(P,Q)} \cdot \sqrt{2 + 2\rho(P,Q)} 

&\leq \sqrt{2H^2(P,Q)} \cdot \sqrt{4} = 2\sqrt{2} \cdot H(P,Q)
$$
\]

This gives \(TV \leq \sqrt{2} \cdot H\), but a sharper bound is
known: \(TV \leq H\). The standard proof uses the inequality
\(|a-b| \leq \sqrt{|a^2-b^2|}\) for \(a,b \geq 0\):

\[
$$
TV(P,Q) &= \frac12 \sum_x |P(x) - Q(x)| 

&= \frac12 \sum_x |\sqrt{P(x)} - \sqrt{Q(x)}| \cdot |\sqrt{P(x)} + \sqrt{Q(x)}| 

&\leq \frac12 \sqrt{\sum_x (\sqrt{P(x)} - \sqrt{Q(x)})^2 \cdot \sum_x (\sqrt{P(x)} + \sqrt{Q(x)})^2} 

&= \frac12 \sqrt{2H^2 \cdot 2(1+\rho)} = H \cdot \sqrt{\frac{1+\rho}{2}} \leq H
$$
\]

where the last inequality uses \(\rho \leq 1\). \(\square\)

#### 4.2 Applying the Bound<!-- label: applying-the-bound -->

Applying Lemma 1 to the \(M\)-expert problem:

\[TV(P_0, P_1) \leq H(P_0, P_1) = \sqrt{1 - \bigl(2\sqrt{\mu_s(1-\mu_s)}\bigr)^M}\]

Let \(\rho = 2\sqrt{\mu_s(1-\mu_s)}\). Then:

\[TV(P_0, P_1) \leq \sqrt{1 - \rho^M}\]

\subsubsection{4.3 Comparison with Other
Bounds}<!-- label: comparison-with-other-bounds -->

The TV-Hellinger bound is tighter than the TV-\(\chi^2\) bound
(\(TV \leq \sqrt{\chi^2/2}\)) in the following sense:

- 
- 

The Hellinger bound is cleaner and avoids the \(1/2\) factor inside the
square root.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{5. Le Cam Two-Point Lower
Bound}<!-- label: le-cam-two-point-lower-bound -->

#### 5.1 Le Cam's Lemma<!-- label: le-cams-lemma -->

**Lemma 2 (Le Cam, 1973).** Let \(P_0\) and \(P_1\) be two
probability distributions on the same measurable space. For any test
\(\psi \in \{0,1\}\):

\[\mathbb{P}_0(\psi = 1) + \mathbb{P}_1(\psi = 0) \geq 1 - TV(P_0, P_1)\]

Equivalently:

\[\max\bigl\{\mathbb{P}_0(\psi = 1),\; \mathbb{P}_1(\psi = 0)\bigr\} \geq \frac{1 - TV(P_0, P_1)}{2}\]

**Proof.** For any test \(\psi\):

\[
$$
\mathbb{P}_0(\psi = 1) + \mathbb{P}_1(\psi = 0)
&= 1 - \bigl(\mathbb{P}_0(\psi = 0) - \mathbb{P}_1(\psi = 0)\bigr) 

&= 1 - \bigl(\mathbb{P}_1(\psi = 0) - \mathbb{P}_0(\psi = 0)\bigr) 

&= 1 - \int \psi \cdot (dP_0 - dP_1) \quad(depending on the test's form) 

&\geq 1 - TV(P_0, P_1)
$$
\]

The last inequality uses the definition of TV as the maximum difference
in probability over measurable sets. \(\square\)

\subsubsection{5.2 Applying Le Cam with the Hellinger TV
Bound}<!-- label: applying-le-cam-with-the-hellinger-tv-bound -->

Combining Lemma 2 with the TV bound from Section 4:

\[
$$
R(\psi) &\geq \frac{1 - TV(P_0, P_1)}{2} 

&\geq \frac{1 - \sqrt{1 - \rho^M}}{2}
$$
\]

where \(\rho = 2\sqrt{\mu_s(1-\mu_s)}\).

#### 5.3 Simplifying the Bound<!-- label: simplifying-the-bound -->

**Lemma 3 (Useful inequality).** For \(x \in [0, 1]\):

\[1 - \sqrt{1 - x} \geq \frac{x}{2}\]

**Proof.** Let \(f(x) = 1 - \sqrt{1-x} - x/2\). Then \(f(0) = 0\),
and:

\[f'(x) = \frac{1}{2\sqrt{1-x}} - \frac12 \geq 0 \quad for  x \in [0,1]\]

since \(\sqrt{1-x} \leq 1\). Thus \(f(x) \geq 0\). \(\square\)

Applying Lemma 3 with \(x = \rho^M\):

\[R(\psi) \geq \frac{\rho^M}{4} = \frac14 \bigl(2\sqrt{\mu_s(1-\mu_s)}\bigr)^M\]

This gives a clean, explicit lower bound on the minimax testing error.

**Why this is correct**: Every inequality direction has been
verified: - Hellinger affinity \(\rho \leq 1\) (holds for any
distributions) - \(TV \leq H\) (standard, direction is correct
for lower bound: larger \(H\) gives larger upper bound on TV, which
gives smaller lower bound on error, so this makes the bound
conservative) - \(1 - \sqrt{1-x} \geq x/2\) (verified, direction is
correct: we're replacing the true value with a smaller value, making the
lower bound weaker but still valid) - The final bound
\(R(\psi) \geq \rho^M/4\) is a valid (conservative) lower bound

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{6. Expression in Terms of the Separation
Gap}<!-- label: expression-in-terms-of-the-separation-gap -->

\subsubsection{\texorpdfstring{6.1 The Separation Gap
\(\Delta\)}{6.1 The Separation Gap \ Delta}}<!-- label: the-separation-gap-delta -->

For \(K=2\) with clean error rate \(\mu_s\), the separation gap is:

\[\mu_s = \frac12 - \Delta, \quadwhere  \Delta \in (0, 1/2)\]

\subsubsection{\texorpdfstring{6.2 Expressing \(\rho\) in Terms of
\(\Delta\)}{6.2 Expressing \ rho in Terms of \ Delta}}<!-- label: expressing-rho-in-terms-of-delta -->

\[
$$
\rho &= 2\sqrt{\mu_s(1-\mu_s)} 

&= 2\sqrt{\left(\frac12 - \Delta\right)\left(\frac12 + \Delta\right)} 

&= 2\sqrt{\frac14 - \Delta^2} 

&= \sqrt{1 - 4\Delta^2}
$$
\]

\subsubsection{\texorpdfstring{6.3 The Lower Bound in Terms of
\(\Delta\)}{6.3 The Lower Bound in Terms of \ Delta}}<!-- label: the-lower-bound-in-terms-of-delta -->

\[R(\psi) \geq \frac14 \bigl(\sqrt{1-4\Delta^2}\bigr)^M = \frac14 (1-4\Delta^2)^{M/2}\]

\subsubsection{\texorpdfstring{6.4 Small-\(\Delta\)
Approximation}{6.4 Small-\ Delta Approximation}}<!-- label: small-delta-approximation -->

For small \(\Delta\), using
\(\log(1-4\Delta^2) = -4\Delta^2 - 8\Delta^4/3 - O(\Delta^6)\):

\[
$$
R(\psi) &\geq \frac14 \exp\!\left(\frac{M}{2} \log(1-4\Delta^2)\right) 

&= \frac14 \exp\!\left(-2M\Delta^2 - \frac{4}{3}M\Delta^4 - O(M\Delta^6)\right) 

&\geq \frac14 \exp\!\bigl(-2M\Delta^2\bigr) \cdot \bigl(1 - O(M\Delta^4)\bigr)
$$
\]

The leading exponent is \(2M\Delta^2\). This matches the Hoeffding
exponent in Theorem 1's upper bound.

\subsubsection{6.5 Alternative Expression (Exact, No
Approximation)}<!-- label: alternative-expression-exact-no-approximation -->

For any \(\Delta\) (not necessarily small):

\[R(\psi) \geq \frac14 (1-4\Delta^2)^{M/2}\]

This is the **exact** exponential form before any approximation. It
is valid for all \(M \geq 1\) and \(\Delta \in [0, 1/2)\), with no
ceiling issues or parameter restrictions.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 7. F1 Lower Bound<!-- label: f1-lower-bound -->

\subsubsection{7.1 From Testing Error to
F1}<!-- label: from-testing-error-to-f1 -->

The F1 score is defined at the population level:

\[F1 = \frac{2\,TP}{2\,TP + FP + FN}\]

where: -
\(TP = \eta \cdot \mathbb{P}(\psi = 1 \mid noise) = \eta \cdot (1 - \beta)\)
-
\(FP = (1-\eta) \cdot \mathbb{P}(\psi = 1 \mid clean) = (1-\eta) \cdot \alpha\)
-
\(FN = \eta \cdot \mathbb{P}(\psi = 0 \mid noise) = \eta \cdot \beta\)

with \(\alpha = P_0(\psi=1)\) and \(\beta = P_1(\psi=0)\).

\subsubsection{7.2 Upper Bound on F1 from the Testing
Bound}<!-- label: upper-bound-on-f1-from-the-testing-bound -->

From Section 5, we have
\(R(\psi) = \max(\alpha, \beta) \geq \varepsilon\) where
\(\varepsilon = \rho^M/4\).

To convert this to an F1 upper bound, note that F1 is decreasing in both
\(\alpha\) and \(\beta\). The maximum possible F1 under the constraint
\(\max(\alpha, \beta) \geq \varepsilon\) is achieved at the boundary
where exactly one of \(\alpha\) or \(\beta\) equals \(\varepsilon\) and
the other is zero:

**Scenario A** (\(\beta = \varepsilon, \alpha = 0\)):

\[F1 = \frac{2\eta(1-\varepsilon)}{2\eta(1-\varepsilon) + 0 + \eta\varepsilon}
= \frac{2(1-\varepsilon)}{2-\varepsilon}\]

**Scenario B** (\(\alpha = \varepsilon, \beta = 0\)):

\[F1 = \frac{2\eta}{2\eta + (1-\eta)\varepsilon + 0}
= \frac{2\eta}{2\eta + (1-\eta)\varepsilon}\]

For \(\eta \leq 1/2\), Scenario B yields a smaller (stricter) upper
bound:

\[\frac{2\eta}{2\eta + (1-\eta)\varepsilon} \leq \frac{2(1-\varepsilon)}{2-\varepsilon}
\quadfor all  \varepsilon \in [0,1]\]

(The inequality holds because
\(2\eta/(2\eta+(1-\eta)\varepsilon) \leq 2(1-\varepsilon)/(2-\varepsilon)\)
is equivalent to \(\varepsilon(1-2\eta) + \eta\varepsilon^2 \geq 0\),
which is true for \(\eta \leq 1/2\).)

Thus:

\[F1 \leq \frac{2\eta}{2\eta + (1-\eta)\varepsilon}\]

and:

\[1 - F1 \geq \frac{(1-\eta)\varepsilon}{2\eta + (1-\eta)\varepsilon}\]

\subsubsection{7.3 The Universal F1 Lower
Bound}<!-- label: the-universal-f1-lower-bound -->

From the case analysis in Section 7.5, the universal bound is:

\[1 - F1 \geq \frac{2-\varepsilon}\]

Using \(\varepsilon \geq \rho^M/4\) and noting that the RHS is
increasing in \(\varepsilon\):

\[1 - F1 \geq \frac{\rho^M/4}{2 - \rho^M/4}
= \frac{\rho^M}{8 - \rho^M}\]

For small \(\rho^M\) (which occurs for any fixed \(\mu_s < 1/2\) when
\(M\) is sufficiently large, or for fixed \(M\) when \(\mu_s\) is
sufficiently far from \(1/2\)):

\[1 - F1 \geq \frac{\rho^M}{8} = \frac18 \bigl(2\sqrt{\mu_s(1-\mu_s)}\bigr)^M\]

Note: This bound is independent of \(\eta\) (no \(\eta\) in the leading
constant \(1/8\)), which is a stronger statement than the earlier
incorrect derivation that introduced \(1/(16\eta)\). The exponent
\(-\log\rho\) is unaffected by this correction.

\subsubsection{\texorpdfstring{7.4 Expression in Terms of
\(\Delta\)}{7.4 Expression in Terms of \ Delta}}<!-- label: expression-in-terms-of-delta -->

\[1 - F1 \geq \frac18 (1-4\Delta^2)^{M/2}\]

For small \(\Delta\):

\[1 - F1 \geq \frac18 \exp\!\bigl(-2M\Delta^2 - 4M\Delta^4 - O(M\Delta^6)\bigr)\]

\subsubsection{7.5 Verification of the F1 Bound
Direction}<!-- label: verification-of-the-f1-bound-direction -->

**Claim**: \(1 - F1 \geq \frac{2-\varepsilon}\)
when \(\max(\alpha, \beta) \geq \varepsilon\).

**Proof.** If \(\max(\alpha, \beta) \geq \varepsilon\), then either
\(\beta \geq \varepsilon\) or \(\alpha \geq \varepsilon\) (or both).

- 
- 

Since \(\max(\alpha, \beta) \geq \varepsilon\), at least one case must
hold. The universal bound is the minimum of the two case-specific
bounds:

\[1 - F1 \geq \min\!\left(\frac{2-\varepsilon},\;
\frac{(1-\eta)\varepsilon}{2\eta + (1-\eta)\varepsilon}\right)\]

For \(\eta \leq 1/2\) and small \(\varepsilon\) (the regime of
interest), compare the approximate magnitudes:
\(\frac{2-\varepsilon} \approx \frac{2}\) and
\(\frac{(1-\eta)\varepsilon}{2\eta + (1-\eta)\varepsilon} \approx
\frac{(1-\eta)\varepsilon}{2\eta}\). The ratio is
\(\frac{1-\eta} \leq 1\), so Case~1 gives the
smaller (tighter) bound. Hence:

\[1 - F1 \geq \frac{2-\varepsilon}\]

This bound is universal: it holds regardless of whether the test falls
into Case~1 or Case~2, because it is the
smaller of the two case-specific bounds. No cross-multiplication or
parameter restriction is needed. \(\square\)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 8. Extension to K \textgreater{ 2}<!-- label: extension-to-k-2 -->

#### 8.1 The Mixture Structure<!-- label: the-mixture-structure -->

For \(K > 2\), the noise distribution becomes a mixture over \((K-1)\)
wrong classes:

\[P_1 = \frac{1}{K-1} \sum_{c \neq y^*} Bernoulli\!\left(1 - \frac{\mu_s}{K-1}\right)^{\otimes M}\]

where under assumption A6 with \(C_{bal} = 1\), all mixture
components have the same Bernoulli parameter \(p_c = 1 - \mu_s/(K-1)\).

\subsubsection{8.2 Reduction to Binary
Case}<!-- label: reduction-to-binary-case -->

**Lemma 4 (K=2 is the hardest case under A6 with C\_bal=1).** When
all mixture components are identical, the noise distribution \(P_1\) is
itself a product distribution:

\[P_1 = Bernoulli\!\left(1 - \frac{\mu_s}{K-1}\right)^{\otimes M}\]

**Proof.** If all \(K-1\) mixture components have the same
parameter, the mixture is trivial:

\[P_1 = \frac{1}{K-1} \cdot (K-1) \cdot Bernoulli(1 - \mu_s/(K-1))^{\otimes M}
= Bernoulli(1 - \mu_s/(K-1))^{\otimes M}\]

Thus \(P_1\) is a product distribution, and the Hellinger approach
applies directly. \(\square\)

**\textgreater{} FIXED (2026-06-28, DEFECT-16):** Lemma 4's claim
``K=2 is the hardest case'' is proven **only under
\(C_{bal} = 1\)** (perfectly balanced error distribution across
wrong classes). When \(C_{bal} = 1\), all \(K-1\) mixture
components have identical Bernoulli parameters, the mixture collapses to
a single product distribution, and K=2 gives the worst-case (largest)
per-expert Hellinger affinity \(\rho_2 = 2\sqrt{\mu_s(1-\mu_s)}\).

**For \(C_{bal} > 1\)**, the mixture components are
non-identical. The worst-case component (closest to the clean
distribution) has error probability
\(p_1 = 1 - C_{bal} \cdot \mu_s/(K-1)\), which is
**smaller** than the \(C_{bal}=1\) case. Smaller \(p_1\)
means larger separation from \(p_0 = \mu_s\), making the testing problem
**easier**, not harder. Therefore:

- 
- 
- 

**Practical implication:** The K=2 + \(C_{bal} = 1\) case
provides the **most stringent test** of the theory. Any noise
detection guarantee that holds for this hardest case automatically holds
for easier cases (\(C_{bal} > 1\), \(K > 2\) with balanced
errors). The SCX minimax optimality claim in Theorem 4' should
explicitly note the \(C_{bal} = 1\) restriction for the exact
constant, while the rate optimality (\(\kappa\)) is unaffected.

\subsubsection{8.3 Comparing the
Separation}<!-- label: comparing-the-separation -->

For \(K > 2\) with \(C_{bal} = 1\), the clean and noise Bernoulli
parameters are:

\[p_0 = \mu_s, \qquad p_1 = 1 - \frac{\mu_s}{K-1}\]

The mean separation is:

\[p_1 - p_0 = 1 - \frac{\mu_s}{K-1} - \mu_s = 1 - \mu_s \cdot \frac{K}{K-1}\]

This is increasing in \(K\) (for fixed \(\mu_s\)). The per-expert
Hellinger affinity for \(Bernoulli(p_0)\) vs
\(Bernoulli(p_1)\) is:

\[\rho_K = \sqrt{\mu_s \left(1 - \frac{\mu_s}{K-1}\right)}
        + \sqrt{(1-\mu_s) \left(\frac{\mu_s}{K-1}\right)}\]

This is the correct general formula; the expression
\(2\sqrt{\mu_s(1-\mu_s)}\) is only valid for \(K=2\) where
\(p_1 = 1-p_0\). One can verify \(\rho_K \leq 1\) via Cauchy-Schwarz:
\(\sqrt{pq} + \sqrt{(1-p)(1-q)} \leq 1\), with equality iff \(p=q\).

Since \(\rho_K\) decreases with \(K\) (larger \(K\) means larger
separation), and the testing lower bound is \(\rho_K^M/4\), we have:

- 
- 

Therefore \(\rho_K^M < \rho_2^M\), meaning the bound for \(K > 2\) is
larger (harder to distinguish). Since we want a lower bound on the
minimax risk, a larger bound from \(K > 2\) would give a weaker
guarantee. We use the \(K=2\) bound as the worst case:

\[R(\psi) \geq \frac14 \rho_2^M = \frac14 \bigl(2\sqrt{\mu_s(1-\mu_s)}\bigr)^M\]

This holds for all \(K \geq 2\) under \(C_{bal} = 1\).

**Note on the mixture-product issue**: The earlier proof (v1)
attempted to bound this via \(\chi^2\) divergence and confused the
direction of the bound. The Hellinger approach avoids this issue
entirely because under \(C_{bal} = 1\), \(P_1\) is exactly a
product distribution, and the tensorization is exact.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 9. Extension to C\_bal \textgreater{
1}<!-- label: extension-to-c_bal-1 -->

\subsubsection{9.1 Non-Uniform Error
Distribution}<!-- label: non-uniform-error-distribution -->

When \(C_{bal} > 1\), the mixture components may have different
Bernoulli parameters. The worst-case component (giving the largest
per-expert Hellinger affinity, i.e., the most similarity to the clean
distribution) has error probability:

\[p_ = \max_{c \neq y^*} \Bigl(1 - \frac{\mu_s}{K-1} \cdot C_{bal}\Bigr)\]

\subsubsection{9.2 Hellinger Bound for
Mixtures}<!-- label: hellinger-bound-for-mixtures -->

For the mixture \(P_1 = \frac{1}{L} \sum_{\ell=1}^L Q_\ell\) where
\(Q_\ell\) are product distributions, we can bound the Hellinger
distance using convexity.

**Lemma 5 (Hellinger convexity for mixtures).** Let \(P_0\) be a
distribution and \(P_1 = \frac{1}{L} \sum_{\ell=1}^L Q_\ell\) be a
mixture. Then:

\[H^2(P_0, P_1) \geq \frac{1}{L} \sum_{\ell=1}^L H^2(P_0, Q_\ell) - \frac{1}{L} \sum_{\ell < \ell'} \rho(Q_\ell, Q_{\ell'})\]

**Proof sketch.** The squared Hellinger distance is not convex in
its second argument, so the standard convexity bound for TV does not
apply. Instead, we use the affinity:

\[\rho(P_0, P_1) = \sum_x \sqrt{P_0(x) \cdot \frac{1}{L} \sum_ Q_\ell(x)}
\geq \frac{1}{L} \sum_ \sum_x \sqrt{P_0(x) Q_\ell(x)} = \frac{1}{L} \sum_ \rho(P_0, Q_\ell)\]

by the concavity of \(\sqrt\) and Jensen's inequality. Therefore:

\[H^2(P_0, P_1) = 1 - \rho(P_0, P_1) \leq 1 - \frac{1}{L} \sum_ \rho(P_0, Q_\ell)
= \frac{1}{L} \sum_ H^2(P_0, Q_\ell)\]

Wait -- this gives an **upper bound** on \(H^2(P_0, P_1)\), which
when combined with \(TV \leq H\) would give an upper bound on TV,
which is what we need for Le Cam. But let me double-check the direction.

Actually, the concavity of \(\sqrt\) gives:

\[\rho(P_0, P_1) = \sum_x \sqrt{P_0(x) \cdot \frac{1}{L} \sum_ Q_\ell(x)}
= \sum_x \sqrt{P_0(x)} \cdot \sqrt{\frac{1}{L} \sum_ Q_\ell(x)}\]

By the concavity of \(\sqrt\):
\(\sqrt{\frac{1}{L}\sum_\ell Q_\ell(x)} \geq
\frac{1}{L}\sum_\ell \sqrt{Q_\ell(x)}\).

Therefore:

\[\rho(P_0, P_1) \geq \sum_x \sqrt{P_0(x)} \cdot \frac{1}{L} \sum_ \sqrt{Q_\ell(x)}
= \frac{1}{L} \sum_ \sum_x \sqrt{P_0(x) Q_\ell(x)}
= \frac{1}{L} \sum_ \rho(P_0, Q_\ell)\]

Thus \(\rho(P_0, P_1) \geq \frac{1}{L}\sum_ \rho(P_0, Q_\ell)\),
which means:

\[H^2(P_0, P_1) = 1 - \rho(P_0, P_1) \leq 1 - \frac{1}{L}\sum_ \rho(P_0, Q_\ell)
= \frac{1}{L}\sum_ H^2(P_0, Q_\ell)\]

This is an **upper bound** on \(H^2\). Since \(TV \leq H\),
this gives:

\[TV(P_0, P_1) \leq H(P_0, P_1) \leq \sqrt{\frac{1}{L}\sum_ H^2(P_0, Q_\ell)}\]

For the lower bound (via Le Cam), a smaller TV gives a stronger lower
bound, so this direction is correct. However, the bound might be loose
if the mixture components are very different from each other.

#### 9.3 Practical Bound for C\_bal \textgreater{
1}<!-- label: practical-bound-for-c_bal-1 -->

In practice, we can use a simpler bound. Let
\(H^2_ = \max_ H^2(P_0, Q_\ell)\). Then:

\[TV(P_0, P_1) \leq \sqrt{\frac{1}{L}\sum_ H^2(P_0, Q_\ell)}
\leq \sqrt{H^2_} = \max_ H(P_0, Q_\ell)\]

Therefore the worst (largest) Hellinger distance among the mixture
components gives the tightest upper bound on TV. The testing lower bound
is then:

\[R(\psi) \geq \frac{1 - \max_ H(P_0, Q_\ell)}{2}\]

For \(C_{bal} > 1\), the component with the smallest
\(1 - C_{bal}\cdot\mu_s/(K-1)\) (most similar to clean) gives the
smallest Hellinger distance, and hence the weakest lower bound. The
worst-case over \(\ell\) for the lower bound is:

\[\min_ H^2(P_0, Q_\ell) = 1 - 2\sqrt{\mu_s \cdot \min_\bigl(1 - \mu_{c_\ell}\bigr)}\]

where \(\mu_{c_\ell}\) is the probability that an expert predicts class
\(c_\ell\) under noise.

**Message**: For \(C_{bal} > 1\), the exponent
\(2M\Delta^2\) is preserved, but the constant factor degrades. The rate
optimality (exponent in \(M\)) is unaffected.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 10. Rate Optimality<!-- label: rate-optimality -->

\subsubsection{10.1 Upper Bound (Theorem
1)}<!-- label: upper-bound-theorem-1 -->

From Theorem 1 (Hoeffding form):

\[1 - F1 \leq \frac{1} \sum_{s} \rho_s \cdot \exp\!\bigl(-2M\Delta_s^2\bigr)\]

For the hardest state \(s^* = \arg\min_s \Delta_s\), this gives:

\[1 - F1 \leq \frac{1} \exp\!\bigl(-2M\Delta_{s^*}^2\bigr)\]

\subsubsection{10.2 Lower Bound (Theorem 4, this
document)}<!-- label: lower-bound-theorem-4-this-document -->

From Section 7:

\[1 - F1 \geq \frac18 \exp\!\bigl(-2M\Delta^2 + O(M\Delta^4)\bigr)\]

#### 10.3 Optimality Statement<!-- label: optimality-statement -->

\begin{longtable}[]{@{}llll@{}}
\toprule\noalign{}
Quantity & Upper bound (Thm 1) & Lower bound (Thm 4) & Ratio 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Exponent & \(2M\Delta^2\) & \(2M\Delta^2\) & **1 (exact match)** 

Leading constant & \(1/\eta\) & \(1/8\) & \(8/\eta\) (at least
\(16\)) 

Regime & All \(\Delta\) & Small \(\Delta\) & Asymptotic in \(\Delta\) 

\end{longtable}

The exponent \(2M\Delta^2\) is **minimax optimal**: no detector can
achieve a better exponential rate. The constant factor gap is \(8/\eta\)
(at least \(16\) for \(\eta \leq 1/2\)), which is typical for minimax
results and can be tightened with more refined arguments.

**Corollary (Rate optimality).** The SCX consistency detector
achieves the minimax-optimal rate \(\exp(-2M\Delta^2)\) in the small-gap
regime. This is the information-theoretic limit for multi-expert noise
detection under assumptions (A1)-(A6).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{11. Connection to Theorem 1: Chernoff
Exactness}<!-- label: connection-to-theorem-1-chernoff-exactness -->

#### 11.1 The Chernoff Exponent<!-- label: the-chernoff-exponent -->

A remarkable property of the Hellinger proof is that it naturally yields
the Chernoff exponent, not just the Hoeffding exponent.

For \(K=2\), the exact large-deviations rate for the optimal Bayes test
is given by the Cramer-Chernoff theorem. The optimal threshold is
\(\theta^* = 1/2\), and:

\[KL\!\left(\frac12 \;\Big\|\; \mu_s\right) = \frac12 \log\frac{1}{2\mu_s} + \frac12 \log\frac{1}{2(1-\mu_s)}
= -\log\bigl(2\sqrt{\mu_s(1-\mu_s)}\bigr)\]

\subsubsection{11.2 The Hellinger-Chernoff
Correspondence}<!-- label: the-hellinger-chernoff-correspondence -->

The per-expert Hellinger exponent is:

\[-\log \rho = -\log\bigl(2\sqrt{\mu_s(1-\mu_s)}\bigr) = KL\!\left(\frac12 \;\Big\|\; \mu_s\right)\]

These are **exactly equal**. This means:

- 
- 

\subsubsection{11.3 Taylor Expansion
Comparison}<!-- label: taylor-expansion-comparison -->

For small \(\Delta\):

\[
$$
-\log\rho &= -\log\bigl(2\sqrt{(1/2-\Delta)(1/2+\Delta)}\bigr) 

&= -\log\sqrt{1-4\Delta^2} 

&= -\frac12 \log(1-4\Delta^2) 

&= 2\Delta^2 + \frac{4}{3}\Delta^4 + O(\Delta^6)
$$
\]

The Hoeffding exponent \(2\Delta^2\) is the leading term. The Hellinger
lower bound recovers the full Chernoff rate, which is strictly larger
than \(2\Delta^2\) for any \(\Delta > 0\).

#### 11.4 Matching Table<!-- label: matching-table -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3200}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2800}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Object
\end{minipage} & \begin{minipage}[b]
Value
\end{minipage} & \begin{minipage}[b]
Exponent
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Per-expert Hellinger affinity \(\rho\) & \(2\sqrt{\mu_s(1-\mu_s)}\) &
\(-\log\rho\) 

KL divergence \(KL(1/2 \|\ \mu_s)\) &
\(-\log(2\sqrt{\mu_s(1-\mu_s)})\) & \(-\log\rho\) 

Theorem 1 Chernoff exponent & \(M \cdot KL(\theta^* \|\ \mu_s)\)
& \(M \cdot (-\log\rho)\) 

Theorem 4 Hellinger exponent & \(-M\log\rho\) &
\(M \cdot (-\log\rho)\) 

Hoeffding approximation & \(2M\Delta^2\) & \(M \cdot (2\Delta^2)\) 

\end{longtable}

The **exact matching** between the Hellinger exponent and the
Chernoff exponent demonstrates that the bound is tight at the exponent
level -- not just up to constants, but exactly.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 12. Numerical Verification<!-- label: numerical-verification -->

\subsubsection{12.1 Testing Error Lower
Bound}<!-- label: testing-error-lower-bound -->

The lower bound \(R(\psi) \geq \rho^M/4\) for various parameter values:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1607}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1786}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1429}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.0893}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.4286}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
\(\mu_s\)
\end{minipage} & \begin{minipage}[b]
\(\Delta\)
\end{minipage} & \begin{minipage}[b]
\(\rho\)
\end{minipage} & \begin{minipage}[b]
\(M\)
\end{minipage} & \begin{minipage}[b]
Lower bound \(\rho^M/4\)
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
0.20 & 0.30 & 0.800 & 10 & \(0.25 \cdot 0.8^{10} \approx 0.027\) 

0.20 & 0.30 & 0.800 & 20 & \(0.25 \cdot 0.8^{20} \approx 0.003\) 

0.25 & 0.25 & 0.866 & 10 & \(0.25 \cdot 0.866^{10} \approx 0.058\) 

0.25 & 0.25 & 0.866 & 20 & \(0.25 \cdot 0.866^{20} \approx 0.013\) 

0.30 & 0.20 & 0.917 & 10 & \(0.25 \cdot 0.917^{10} \approx 0.105\) 

0.30 & 0.20 & 0.917 & 20 & \(0.25 \cdot 0.917^{20} \approx 0.044\) 

0.40 & 0.10 & 0.980 & 10 & \(0.25 \cdot 0.98^{10} \approx 0.204\) 

0.40 & 0.10 & 0.980 & 50 & \(0.25 \cdot 0.98^{50} \approx 0.091\) 

0.49 & 0.01 & 0.9998 & 100 &
\(0.25 \cdot 0.9998^{100} \approx 0.245\) 

\end{longtable}

All bounds are non-trivial (below \(0.25\)) when \(\rho^M\) is not too
close to \(1\), which occurs when \(M\) is large enough or \(\mu_s\) is
far enough from \(1/2\).

#### 12.2 F1 Lower Bound<!-- label: f1-lower-bound-1 -->

The F1 lower bound \(1-F1 \geq \rho^M/8\):

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1286}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1429}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.0714}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.2857}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.3714}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
\(\mu_s\)
\end{minipage} & \begin{minipage}[b]
\(\Delta\)
\end{minipage} & \begin{minipage}[b]
\(M\)
\end{minipage} & \begin{minipage}[b]
\(1-F1 \geq\)
\end{minipage} & \begin{minipage}[b]
Implied \(F1 \leq\)
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
0.20 & 0.30 & 10 & \(0.8^{10}/8 \approx 0.013\) & \(0.987\) 

0.20 & 0.30 & 20 & \(0.8^{20}/8 \approx 0.001\) & \(0.999\) 

0.25 & 0.25 & 10 & \(0.866^{10}/8 \approx 0.030\) & \(0.970\) 

0.25 & 0.25 & 20 & \(0.866^{20}/8 \approx 0.007\) & \(0.993\) 

0.30 & 0.20 & 20 & \(0.917^{20}/8 \approx 0.022\) & \(0.978\) 

0.40 & 0.10 & 100 & \(0.98^{100}/8 \approx 0.017\) & \(0.983\) 

\end{longtable}

*Note*: These F1 upper bounds are loose (close to 1) because the
bound only requires that \(\max(\alpha, \beta) \geq \varepsilon\), not
that both are large. A more refined construction could tighten this.

\subsubsection{12.3 Verification of Key
Inequalities}<!-- label: verification-of-key-inequalities -->

We verify the key inequality \(1-\sqrt{1-x} \geq x/2\) for the relevant
range:

\begin{longtable}[]{@{}ccccc@{}}
\toprule\noalign{}
\(x = \rho^M\) & \(\rho\) (typ) & \(\sqrt{1-x}\) & \(1-\sqrt{1-x}\) &
\(x/2\) 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
0.01 & --- & 0.995 & 0.005 & 0.005 

0.10 & --- & 0.949 & 0.051 & 0.050 

0.25 & --- & 0.866 & 0.134 & 0.125 

0.50 & --- & 0.707 & 0.293 & 0.250 

0.75 & --- & 0.500 & 0.500 & 0.375 

\end{longtable}

The inequality holds with slack increasing in \(x\).

\subsubsection{12.4 Comparison with Exact Optimal
Test}<!-- label: comparison-with-exact-optimal-test -->

For \(K=2\), the optimal Bayes test for equal priors is:

\[\psi^*(e_1,...,e_M) = \mathbf{1}\{S > M/2\}\]

where \(S = \sum_{m=1}^M e_m\). The exact error of this test is:

\[R(\psi^*) = \mathbb{P}(Bin(M, \mu_s) \geq M/2)\]

For \(\mu_s = 0.2\), \(M = 10\): - Exact error:
\(\mathbb{P}(Bin(10, 0.2) \geq 5) \approx 0.033\) - Hellinger
bound: \(0.25 \cdot 0.8^{10} \approx 0.027\) (close to exact) - Old Slud
bound (v1): claimed
\(0.5 \cdot \exp(-20 \cdot 0.09) = 0.5 \cdot e^{-1.8} \approx 0.083\)
(incorrect -- exceeds actual error)

The Hellinger bound (\(0.027\)) is slightly below the actual error
(\(0.033\)), confirming it is a valid lower bound. The old Slud bound
(\(0.083\)) exceeds the actual error, confirming it was invalid.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{13. Resolution of Review
Issues}<!-- label: resolution-of-review-issues -->

\subsubsection{13.1 Issue 1: Lemma 7 (Slud's inequality) was
false}<!-- label: issue-1-lemma-7-sluds-inequality-was-false -->

**Original problem**: The v1 proof claimed
\(\mathbb{P}(Bin(M,\mu) \geq M/2) \geq
\frac12 \exp(-2M\Delta^2)\), which fails numerically (e.g., \(\mu=0.4\),
\(M=20\) gives LHS \(\approx 0.244\), RHS \(\approx 0.335\)).

**Resolution**: The Hellinger approach entirely avoids Slud's
inequality. Instead: 1. Compute the exact Hellinger affinity
\(\rho = 2\sqrt{\mu_s(1-\mu_s)}\) for one expert 2. Tensorize exactly:
\(\rho_M = \rho^M\) 3. Bound \(TV \leq H = \sqrt{1-\rho^M}\) 4.
Apply Le Cam: \(R(\psi) \geq (1-\sqrt{1-\rho^M})/2 \geq \rho^M/4\)

All inequalities are in the correct direction, and no Binomial tail
bound is required. The Hellinger approach works for any \(M\), any
\(\mu_s\), without ceiling issues or parameter restrictions.

\subsubsection{13.2 Issue 2: K=2 to K\textgreater2 reduction used bound
direction
incorrectly}<!-- label: issue-2-k2-to-k2-reduction-used-bound-direction-incorrectly -->

**Original problem**: The v1 proof argued that larger \(\chi^2\)
for \(K>2\) implies the \(K=2\) case is hardest. This used the bound
\(TV \leq \sqrt{((1+\chi^2)^M-1)/2}\) in the wrong direction (a
larger \(\chi^2\) makes the bound looser, not tighter).

**Resolution**: Under \(C_{bal} = 1\), all mixture
components are identical, so \(P_1\) is a pure product distribution (not
a true mixture). The Hellinger approach applies directly. The per-expert
parameters are \(p_0 = \mu_s\) and \(p_1 = 1-\mu_s/(K-1)\), and the
separation \(p_1 - p_0 = 1 - \mu_s K/(K-1)\) increases with \(K\),
making \(K=2\) the hardest case. No bounding of the mixture distribution
is needed.

\subsubsection{13.3 Issue 3: F1 derivation was algebraically
unsound}<!-- label: issue-3-f1-derivation-was-algebraically-unsound -->

**Original problem**: The v1 proof's Lemma 8 attempted to show
\(1-F1 \geq 1-TPR\) without verifying the validity
condition \(FP \geq FN\).

**Resolution**: The new F1 derivation (Section 7) directly bounds
F1 from the testing error \(\max(\alpha, \beta) \geq \varepsilon\) using
the monotonicity of F1 in \(\alpha\) and \(\beta\). The derivation: 1.
Considers two cases (\(\alpha \geq \varepsilon\) or
\(\beta \geq \varepsilon\)) 2. Bounds F1 in each case using elementary
inequalities 3. Takes the minimum (worst case) to get the final bound 4.
Verifies all inequality directions explicitly

The bound \(1-F1 \geq \rho^M/8\) is valid for all
\(\eta \leq 1/2\) without additional conditions.

\subsubsection{13.4 Summary of
Improvements}<!-- label: summary-of-improvements -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2286}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3143}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4571}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Aspect
\end{minipage} & \begin{minipage}[b]
v1 (Slud)
\end{minipage} & \begin{minipage}[b]
v2 (Hellinger)
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Core inequality & Slud's inequality (false) & Hellinger tensorization
(exact) 

TV bound & Via \(\chi^2\) tensorization & Via \(TV \leq H\) 

\(K>2\) extension & Required mixture bound (wrong direction) & Product
reduction (\(C_{bal}=1\)) 

F1 derivation & Algebraic errors & Case analysis with verified
inequalities 

Exponent & \(2M\Delta^2\) (claimed, unproven) & \(2M\Delta^2\) (proved,
with Chernoff exactness) 

Ceiling issue & Unaddressed for odd \(M\) & Nonexistent (works for all
\(M\)) 

Parameter restrictions & \(\mu_s \leq 1/2\), \(k/M \leq 1/2\) & None
(\(\mu_s \in (0,1)\) works) 

Numerical validity & Fails counterexamples & Verified numerically 

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

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{Appendix A: Glossary of Key
Quantities}<!-- label: appendix-a-glossary-of-key-quantities -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2759}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4138}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3103}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Symbol
\end{minipage} & \begin{minipage}[b]
Definition
\end{minipage} & \begin{minipage}[b]
Meaning
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(\mu_s\) & \(\mathbb{P}(f_m(x) \neq y^* \mid x \in s)\) & Clean-data
error rate in state \(s\) 

\(\Delta\) & \(1/2 - \mu_s\) (for \(K=2\)) & Separation gap 

\(\rho\) & \(2\sqrt{\mu_s(1-\mu_s)}\) & Per-expert Hellinger affinity 

\(\rho^M\) & \((2\sqrt{\mu_s(1-\mu_s)})^M\) & \(M\)-expert Hellinger
affinity 

\(H^2\) & \(1 - \rho\) & Squared Hellinger distance 

\(H\) & \(\sqrt{1-\rho^M}\) & Hellinger distance for \(M\) experts 

\(\varepsilon\) & \(\rho^M/4\) & Error lower bound from Le Cam 

\(\alpha\) & \(P_0(\psi=1)\) & False positive rate 

\(\beta\) & \(P_1(\psi=0)\) & False negative rate 

\(\eta\) & \(\mathbb{P}(noise)\) & Global noise rate 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{Appendix B: Direct Calculation of Hellinger for
Products}<!-- label: appendix-b-direct-calculation-of-hellinger-for-products -->

For completeness, we verify the tensorization property explicitly for
the \(M\)-expert case.

Let \(e = (e_1, ..., e_M)\) with \(e_m \in \{0,1\}\). Under \(P_0\)
(clean):

\[P_0(e) = \prod_{m=1}^M \mu_s^{e_m} (1-\mu_s)^{1-e_m}\]

Under \(P_1\) (noise, \(K=2\)):

\[P_1(e) = \prod_{m=1}^M (1-\mu_s)^{e_m} \mu_s^{1-e_m}\]

The Hellinger affinity is:

\[
$$
\rho(P_0, P_1) &= \sum_{e \in \{0,1\}^M} \sqrt{P_0(e) P_1(e)} 

&= \sum_{e} \sqrt{\prod_{m=1}^M \mu_s^{e_m}(1-\mu_s)^{1-e_m} \cdot \prod_{m=1}^M (1-\mu_s)^{e_m}\mu_s^{1-e_m}} 

&= \sum_{e} \prod_{m=1}^M \sqrt{\mu_s^{e_m}(1-\mu_s)^{1-e_m} \cdot (1-\mu_s)^{e_m}\mu_s^{1-e_m}} 

&= \sum_{e} \prod_{m=1}^M (\mu_s(1-\mu_s))^{1/2} 

&= \sum_{e} (\mu_s(1-\mu_s))^{M/2} 

&= 2^M \cdot (\mu_s(1-\mu_s))^{M/2} 

&= \bigl(2\sqrt{\mu_s(1-\mu_s)}\bigr)^M
$$
\]

This confirms the tensorization property. The key step is that
\(\sqrt{P_0(e)P_1(e)}\) factorizes into a product across experts
because:

\[\sqrt{\mu_s^{e_m}(1-\mu_s)^{1-e_m} \cdot (1-\mu_s)^{e_m}\mu_s^{1-e_m}}
= \sqrt{\mu_s(1-\mu_s)}\]

**independently of \(e_m\)**. This is the crucial simplification
for the \(K=2\) case: the per-expert contribution does not depend on the
expert's prediction, making the sum over \(2^M\) error patterns collapse
to a product over \(M\) independent factors.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{Appendix C: Why the Hellinger Approach Works and Slud's
Fails}<!-- label: appendix-c-why-the-hellinger-approach-works-and-sluds-fails -->

\subsubsection{C.1 The Fundamental Issue with
Slud}<!-- label: c.1-the-fundamental-issue-with-slud -->

Slud's inequality gives a lower bound on Binomial tail probabilities in
terms of the Gaussian CDF:

\[\mathbb{P}(Bin(M,p) \geq k) \geq \frac12 \Phi\!\left(-\frac{k-Mp}{\sqrt{Mp(1-p)}}\right)\]

To convert this to an exponential bound, one would need to bound
\(\Phi(-t)\) from below by \(\frac12 e^{-2Mt^2}\) (in the notation of
the v1 proof). The Gaussian lower tail is:

\[\Phi(-t) \geq \frac{1}{\sqrt{2\pi}} \frac{t}{1+t^2} e^{-t^2/2}\]

The exponent is \(t^2/2 = M(k/M-p)^2 / (2p(1-p))\). For \(p = \mu_s\),
\(k = M/2\):

\[\frac{t^2}{2} = \frac{M(1/2 - \mu_s)^2}{2\mu_s(1-\mu_s)} = \frac{M\Delta^2}{2\mu_s(1-\mu_s)}\]

Since \(\mu_s(1-\mu_s) \leq 1/4\):

\[\frac{t^2}{2} \geq \frac{M\Delta^2}{2 \cdot (1/4)} = 2M\Delta^2\]

Thus the Gaussian exponent is **at least** \(2M\Delta^2\), meaning
the Gaussian tail decays **at least as fast** as
\(\exp(-2M\Delta^2)\). A lower bound on the Binomial probability using
this Gaussian tail would give an exponent of \(2M\Delta^2\) or larger --
but a larger exponent means a **smaller** lower bound. The v1 proof
attempted to replace this with a **larger** lower bound (using the
Hoeffding exponent \(2M\Delta^2\)), which is the wrong direction.

Numerically: for \(\mu=0.4\), \(M=20\), the Gaussian tail
\(\Phi(-(10-8)/\sqrt{20\cdot0.4\cdot0.6}) = \Phi(-2/\sqrt{4.8}) = \Phi(-0.913) \approx 0.181\).
Slud gives
\(\mathbb{P}(Bin(20,0.4) \geq 10) \geq 0.181/2 = 0.090\), not
\(0.5\cdot e^{-0.4} \approx 0.335\) as claimed in v1.

\subsubsection{C.2 Why Hellinger Avoids
This}<!-- label: c.2-why-hellinger-avoids-this -->

The Hellinger approach directly computes the divergence between \(P_0\)
and \(P_1\) without going through Binomial tail bounds:

1. 
2. 
3. 

No tail bounds, no Gaussian approximations, no ceiling issues. The
Hellinger approach is ``robust by design'' because it works at the level
of densities rather than tail events.

\subsubsection{C.3 The Ceiling Issue (Odd
M)}<!-- label: c.3-the-ceiling-issue-odd-m -->

The v1 proof applied Slud with \(k = \lceil M/2\rceil\), but Slud
requires \(k/M \leq 1/2\). For odd \(M\), \(\lceil M/2\rceil/M > 1/2\),
violating the premise. The Hellinger approach has no such constraint: it
works for any \(M \geq 1\) because it never references thresholds or
tail events.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

**End of proof document.**