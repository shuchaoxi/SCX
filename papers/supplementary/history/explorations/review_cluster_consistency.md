\section{Review of ``Theorem 3: Cluster Consistency of State Discovery
Under Strong
Features''}<!-- label: review-of-theorem-3-cluster-consistency-of-state-discovery-under-strong-features -->

**Reviewer:** Hostile reviewer for the Annals of Statistics
**Manuscript:** Theorem 3 + Corollaries 1-3, SCX Theory
**Decision: REJECT**

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. Overall Assessment<!-- label: overall-assessment -->

**Recommendation: Reject.** The proof contains at least two fatal
mathematical errors that invalidate the main result. The algebra in the
central calculation is wrong, the inequality directions are reversed in
the critical step, and the derivation of the claimed \(K = o(n^{1/3})\)
rate is incoherent -- the author walks through multiple
self-contradictory calculations and never arrives at a consistent
argument. Beyond these fatal errors, the proof relies on at least five
unstated or unjustified assumptions, confuses the population parameter
\(\Delta_\) (a fixed property of the data) with an asymptotic
scaling parameter, and never addresses the elephant in the room:
\(k\)-means is NP-hard, but the proof requires the global empirical
minimizer.

I do not recommend resubmission in the current form. The authors should
either (a) restructure the proof around a tractable algorithm (e.g.,
Lloyd's with a suitable initialization) or (b) weaken the claim to
``there exists a polynomial-time algorithm that...{}'' -- and then
prove it.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{2. Critical Issues (Fatal If
True)}<!-- label: critical-issues-fatal-if-true -->

\subsubsection{Issue 1 (FATAL): The main misclassification bound
diverges, not
converges}<!-- label: issue-1-fatal-the-main-misclassification-bound-diverges-not-converges -->

This is the single most serious error. The algebra in the proof implies
the opposite of the claimed result.

The proof establishes (lines 391-397):

\[misclassification \leq \frac{8\delta_n}{\pi_ \Delta_^2}, \qquad \delta_n = C_1 \sqrt{\frac{K \log n}{n}}\]

Under the separation condition
\(\Delta_^2 \geq C_0 \sigma^2 \frac{K \log n}{n}\), plugging the
worst case (tightest bound, where
\(\Delta_^2 = \Theta(K \log n / n)\)) gives:

\[misclassification \leq O\left(\frac{\sqrt{K \log n / n}}{K \log n / n}\right) = O\left(\sqrt{\frac{n}{K \log n}}\right)\]

The author writes in line 459 that this \(\to 0\) requires
\(K \ll n / \log n\). **The inequality direction is reversed.** The
quantity \(\sqrt{n / (K \log n)} \to 0\) iff \(K \log n\) grows faster
than \(n\), i.e., \(K \gg n / \log n\). For any \(K\) that grows
sublinearly in \(n\) (including \(K = o(n^{1/3})\)),
\(\sqrt{n / (K \log n)} \to \infty\). The bound explodes.

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
\(K\) scaling & \(\sqrt{n / (K \log n)}\) & Behavior 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Fixed \(K\) & \(\Theta(\sqrt{n})\) & Diverges 

\(K = n^{1/3}\) & \(\Theta(n^{1/3} / \sqrt{\log n})\) & Diverges 

\(K = n / \log n\) & \(\Theta(1)\) & Constant 

\(K = n^{0.9}\) & \(\Theta(n^{0.05})\) & Diverges (slowly) 

\(K = n / \sqrt{\log n}\) & \(\Theta(n^{-1/4})\) & **Converges** 

\end{longtable}

The only way to get convergence is \(K = \omega(n / \log n)\), which is
a *faster* growth rate -- opposite to the claimed \(o(n^{1/3})\),
and would violate the separation condition (since centers would need to
pack into a bounded region).

**This is fatal.** The theorem's central claim -- that
misclassification \(\to 0\) under \(K = o(n^{1/3})\) -- is
mathematically impossible under the stated bounds.

\subsubsection{Issue 2 (FATAL): The uniform convergence bound does not
converge}<!-- label: issue-2-fatal-the-uniform-convergence-bound-does-not-converge -->

In Step 2 of the proof of Theorem 3 (lines 362-377), the author sets:

\[\delta_n = C_1 \sqrt{\frac{K d_\phi \log n}{n}}\]

and claims:

\[\log \mathbb{P}(\sup |W_n - W| > \delta_n) \leq K d_\phi \log\left(1 + \frac{8C_1 M}{\delta_n}\right) - \frac{n \delta_n^2}{32 C_1^2}\]

Substituting \(\delta_n\):

- 
- 
- 
- 

The total:
\(K d_\phi \log n \left(\frac{1}{2} - \frac{1}{32}\right) + lower order = \frac{15}{32} K d_\phi \log n + o(K d_\phi \log n)\)

**This is positive, not negative.** The claimed value of
\(K d_\phi \log n - (K d_\phi \log n)/32\) (line 371) would require the
log term to equal \(\log n\), which it does not -- it equals
\(\frac{1}{2}\log n + o(\log n)\). The author made an algebraic mistake
in simplifying the covering number term.

As \(n \to \infty\), the probability bound tends to \(+\infty\), meaning
the bound is vacuous. The uniform convergence does not hold at this
\(\delta_n\) rate.

\subsubsection{Issue 3 (FATAL): The proof assumes the global optimum of
an NP-hard
problem}<!-- label: issue-3-fatal-the-proof-assumes-the-global-optimum-of-an-np-hard-problem -->

Line 89 defines \(\hat_n^* = \arg\min W_n(\hat)\) -- the
global empirical minimizer. The proof never addresses that \(k\)-means
is NP-hard (Aloise et al., 2009; Dasgupta, 2008). In practice, Lloyd's
algorithm finds a local optimum, and the gap between local and global
minima can be arbitrarily large.

The author cites Pollard (1981), but Pollard's strong consistency result
is for the *global* \(k\)-means minimizer, which Pollard himself
notes is a theoretical construct. Extending Pollard's result to local
optima is non-trivial -- local minima can fail to be consistent even
when the global minimum is (see e.g., Rakhlin \& Caponnetto, 2007, who
show that stability of Lloyd's requires additional conditions).

**The paper claims a result about the algorithm SCX uses (Lloyd's
/ \(k\)-means), but proves a result about a computationally intractable
oracle.** This is a bridge too far.

\subsubsection{Issue 4 (FATAL): Lemma 5's core calculation is
incorrect}<!-- label: issue-4-fatal-lemma-5s-core-calculation-is-incorrect -->

The argument that
\(W(\mu) - W(\mu^*) = \sum_{k=1}^K \pi_k \cdot \delta_k^2\) (lines
277-298) is not mathematically justified. The author writes:

\[W(\mu) - W(\mu^*) = \sum_{k=1}^K \pi_k \cdot \mathbb{E}\left[ \min_j \|\mu_k - \mu_j' + \varepsilon\|_2^2 - \|\varepsilon\|_2^2 \right]\]

then replaces \(\min_j\) with
\(j^*(k) = \arg\min_j \|\mu_k - \mu_j'\|_2\), obtaining:

\[\mathbb{E}\left[ \min_j \|\mu_k - \mu_j' + \varepsilon\|_2^2 \right] \geq \mathbb{E}\left[ \|\mu_k - \mu_{j^*(k)}' + \varepsilon\|_2^2 \right]\]

and then computes this as
\(\delta_k^2 + \mathbb{E}[\|\varepsilon\|_2^2]\).

**Three problems:** 1. The inequality is reversed. Since \(\min_j\)
gives the *smallest* value,
\(\min_j \|a + \varepsilon\| \leq \|a_{j^*(k)} + \varepsilon\|\) for
*any fixed* \(j^*(k)\), not \(\geq\). The author should have
\(\leq\) here. 2. Even with the correct direction, \(j^*(k)\) depends on
\(\varepsilon\) through the \(\min\) -- it is the index of the estimated
center closest to \(\mu_k + \varepsilon\), not the center closest to
\(\mu_k\). These can differ when noise is large relative to separation.
3. The expectation of \(\|\mu_k - \mu_j' + \varepsilon\|_2^2\) is
\(\|\mu_k - \mu_j'\|_2^2 + \mathbb{E}[\|\varepsilon\|_2^2]\) only when
\(\varepsilon\) is independent of the center choice, which would require
\(j\) to be fixed. But \(j^*(k)\) depends on \(\varepsilon\) (it is
defined by the argmin), so cross-terms like
\(\mathbb{E}[\varepsilon^\top(\mu_k - \mu_{j^*(k)}')]\) do not vanish in
general.

**This invalidates Lemma 5, which is the cornerstone of the
identifiability argument.**

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{3. Major Issues (Need Substantial
Work)}<!-- label: major-issues-need-substantial-work -->

\subsubsection{\texorpdfstring{Issue 5: Confusion between fixed and
scaling
\(\Delta_\)}{Issue 5: Confusion between fixed and scaling \ Delta\_\{\ min\}}}<!-- label: issue-5-confusion-between-fixed-and-scaling-delta_min -->

The document oscillates between two incompatible interpretations of
\(\Delta_\):

- 
- 

The separation condition
\(\Delta_^2 \geq C_0 \sigma^2 K \log n / n\) makes sense as a
finite-sample sufficient condition under Interpretation A but becomes
self-contradictory under Interpretation B (where \(\Delta_\) is
determined by \(K\), not \(n\)).

The ``reconciliation'' section (lines 486-510) mixes both
interpretations and the algebra is inconsistent. The sphere-packing
argument imposes an *upper* bound on \(\Delta_\) given \(K\),
while the separation condition imposes a *lower* bound. For large
\(K\), these bounds can conflict, preventing any such \(K\) from
existing.

The derivation of the \(1/3\) exponent only works under a very specific
set of coupled scaling assumptions that are never stated explicitly.

\subsubsection{Issue 6: Lemma 6's conversion from risk gap to
misclassification is not
rigorous}<!-- label: issue-6-lemma-6s-conversion-from-risk-gap-to-misclassification-is-not-rigorous -->

Three specific problems:

**(a) The \(\pi_k \cdot (\Delta_/2)^2 / 2\) factor (line
328) is pulled from thin air.** The author states ``accounting for
noise'' but doesn't show the calculation. Where does the factor of
\(1/2\) come from? Why \((\Delta_/2)^2\) and not
\((\Delta_/2)^2\)? This is a critical quantitative claim that
directly enters the main theorem's rate, but it's unsupported.

**(b) The ``boundary effects'' handling (lines 335-341) is
hand-wavy.** The author writes that boundary effects are:

\[O\left(K \cdot \exp\left(-\frac{\Delta_^2}{8\sigma^2}\right)\right)\]

and claims this is ``negligible under the separation condition.'' But: -
The constant \(8\) in the denominator is never derived. - The \(K\)
factor outside the exponential could dominate if \(K\) grows quickly. -
Under the scaling \(\Delta_^2 = \Theta(K \log n / n)\), the
exponential becomes \(\exp(-c K \log n / n)\), which is close to \(1\)
when \(K \log n / n\) is small, not negligible.

**(c) The argument that misclassification only occurs when
\(\|\hat_{\tau(k)} - \mu_k\| \geq \Delta_/2\) (lines 321-325)
ignores cumulative effects.** A point from state \(k\) could be
misclassified even if all centers are well-estimated, if it falls closer
to a different estimated center due to noise. The triangle inequality
argument is:

\[\|\phi(x) - \hat_{\tau(k)}\| \leq \|\mu_k + \varepsilon - \mu_k\| + \|\mu_k - \hat_{\tau(k)}\| < \|\varepsilon\| + \frac{\Delta_}{2}\]
\[\|\phi(x) - \hat_j\| \geq \|\mu_k + \varepsilon - \mu_j\| - \|\mu_j - \hat_j\| \geq \Delta_ - \|\varepsilon\| - \frac{\Delta_}{2}\]

The comparison is \(\|\varepsilon\| + \frac{\Delta_}{2}\)
vs.~\(\frac{\Delta_}{2} - \|\varepsilon\|\), and the inequality
\(\|\varepsilon\| + \frac{\Delta_}{2} < \frac{\Delta_}{2} - \|\varepsilon\|\)
requires \(\|\varepsilon\| < 0\) (impossible). The argument as stated
does not work. The bound needs a more careful treatment of noise.

\subsubsection{Issue 7: The covering number bound is
insufficient}<!-- label: issue-7-the-covering-number-bound-is-insufficient -->

Lemma 4 bounds the covering number of \(K\)-center sets, but the
relevant function class for \(k\)-means is
\(f_\mu(x) = \min_k \|x - \mu_k\|_2^2\). The covering number of this
function class in the \(L_\infty(P_n)\) metric may be larger than the
covering number of the center class in the \(\ell_\infty\) metric,
because:

- 
- 

The author acknowledges that VC dimension would give a similar bound
(line 249), but this is misleading. The VC dimension of \(k\)-means in
\(\mathbb{R}^d\) is not \(O(Kd)\) -- it grows super-linearly in \(K\)
because the number of possible labelings grows as \(K^{nd}\) (the number
of Voronoi partitions). A proper VC bound would give
\(\log \mathcal{N} = \Omega(K \log K)\), not \(O(K)\).

\subsubsection{Issue 8: Two-layer extension (Corollary 2) assumes the
result}<!-- label: issue-8-two-layer-extension-corollary-2-assumes-the-result -->

Corollary 2 requires \(\kappa(W) = O(1)\), which is asserted without
proof (line 591). Since \(W\) is learned from data -- specifically from
expert error patterns -- there is no guarantee it is well-conditioned.
In fact: - If \(W\) is estimated from finite data, it has estimation
error that degrades the signal-to-noise ratio. - The claim that \(W\)
can *increase* separation (line 595) is stated without any proof or
reference. - The singular values of \(W\) depend on the eigenstructure
of the cross-covariance between features and expert errors, which is
itself estimated. No finite-sample bounds are provided.

**Corollary 2 does not prove anything about the two-layer
extension.** It merely re-states Theorem 3 under the assumption that
\(W\) is well-conditioned and then asserts (without proof) that this
condition holds in practice.

\subsubsection{Issue 9: The sub-Gaussian assumption is
unverified}<!-- label: issue-9-the-sub-gaussian-assumption-is-unverified -->

The proof assumes \(\varepsilon\) is sub-Gaussian with parameter
\(\sigma^2\) (line 56). For SCX's actual features:

- 
- 
- 

If the features are only bounded (not sub-Gaussian), the tail bounds
degrade from \(\exp(-c n \delta^2)\) to \(\exp(-c n \delta)\) (via
Hoeffding), which would change the rates entirely.

\subsubsection{Issue 10: Appendix A's sub-Gaussian norm bound is for
Gaussians, not
sub-Gaussians}<!-- label: issue-10-appendix-as-sub-gaussian-norm-bound-is-for-gaussians-not-sub-gaussians -->

Line 770 uses the bound
\(\|\varepsilon\|_2^2 \leq \sigma^2(d_\phi + 2\sqrt{d_\phi \log n} + 2\log n)\),
which is a standard chi-squared concentration bound for *Gaussian*
vectors. For sub-Gaussian vectors, the concentration of the Euclidean
norm is different: it depends on the sub-Gaussian norm
\(K = \sup_{\|u\|=1} \|\langle \varepsilon, u\rangle\|_{\psi_2}\), and
the bound is:

\[\|\varepsilon\|_2 \leq C K (\sqrt{d_\phi} + t) \quad with probability  1 - 2\exp(-t^2)\]

but the constant \(C\) depends on the specific sub-Gaussian definition
and the covariance structure. The chi-squared-like bound used by the
author only holds for *exact* Gaussian vectors, not general
sub-Gaussian vectors.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. Minor Issues<!-- label: minor-issues -->

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

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{5. Recommended Fixes for Each
Issue}<!-- label: recommended-fixes-for-each-issue -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.3182}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.6818}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Issue
\end{minipage} & \begin{minipage}[b]
Recommendation
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**1 (FATAL)** & Re-derive the misclassification rate. The bound
must be expressed as \(O(\sqrt{K \log n / n} / \Delta_^2)\). If
\(\Delta_\) is fixed (does not scale with \(n\)), the rate is
\(O(\sqrt{K \log n / n})\), which gives \(K = o(n / \log n)\) for
convergence -- not \(o(n^{1/3})\). If \(\Delta_\) scales, state
the scaling explicitly and re-derive all bounds. 

**2 (FATAL)** & Re-do the uniform convergence calculation. The
correct choice of \(\delta_n\) should make the exponent negative. Either
increase \(\delta_n\) (to say
\(\delta_n = C \sqrt{K d_\phi (\log n)^2 / n}\) to get an extra
\(\log n\) factor) or use a sharper entropy bound. 

**3 (FATAL)** & This is a structural issue. Two options: (a)
Restrict to algorithms that provably find the global \(k\)-means
minimizer (only possible for small \(K\) or special structure). (b)
Prove that Lloyd's algorithm with appropriate initialization finds a
solution that is ``good enough'' -- this would require stability of the
local minimum (following Rakhlin \& Caponnetto, 2007) or a perturbation
analysis. Option (c): acknowledge the gap and frame the result as about
the oracle. 

**4 (FATAL)** & Re-do Lemma 5 properly. The key calculation is:
\(W(\mu) - W(\mu^*) = \sum_k \pi_k \mathbb{E}[\min_j \|\mu_k + \varepsilon - \mu_j'\|^2 - \|\varepsilon\|^2]\).
The correct lower bound requires a ``gap'' condition: for any
\(\mu \neq \mu^*\), there exists at least one \(k\) such that
\(\|\mu_k - \mu_{\sigma(k)}'\| \geq \Delta_/2\) for any
permutation \(\sigma\), and then one must lower-bound the expectation
over \(\varepsilon\) using sub-Gaussian tail bounds on the assignment
probabilities. This is doable but non-trivial. 

**5** & Clarify which interpretation is intended. If
\(\Delta_\) is a fixed property of the data, delete all scaling
analysis (lines 486-515). If \(\Delta_\) scales, derive this from
explicit assumptions about how the centers change as \(K\) grows. 

**6** & (a) Derive the constant \(1/2\) or replace with a properly
bounded expression. (b) Provide an explicit bound on boundary effects
using the sub-Gaussian tail, not an \(O(\cdot)\) statement. (c) Fix the
triangle inequality argument. 

**7** & Either (a) bound the metric entropy of the function class
\(\{f_\mu\}\) directly, or (b) cite a known VC bound for \(k\)-means
(e.g., the Natarajan dimension). The note in line 249 suggesting VC
dimension gives the same bound is misleading -- the VC dimension of
\(k\)-means is \(O(K d \log(K d))\) at minimum. 

**8** & Provide finite-sample bounds on \(\kappa(W)\) or drop
Corollary 2 until such bounds are available. The current version proves
nothing about the two-layer extension. 

**9** & Verify the sub-Gaussian assumption empirically for SCX
features, or replace with a boundedness assumption (which gives weaker
rates but requires fewer assumptions). 

**10** & Use the correct sub-Gaussian norm concentration bound. The
chi-squared bound is only valid for Gaussian vectors. 

**Structural** & Remove the working-draft scaffolding in the proof
of Theorem 3 (lines 392-515). A published proof should not contain
phrases like ``Wait -- this suggests...{}'' or ``Let me re-derive
more carefully.'' 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 6. Summary<!-- label: summary -->

The document attempts to prove a non-trivial extension of Pollard's
(1981) \(k\)-means consistency to the setting \(K \to \infty\), with
explicit rates depending on the separation-to-noise ratio. This is a
worthy goal. However, the proof as written contains:

- 
- 
- 
- 

The paper should not be published in its current form. The core idea is
interesting but the technical execution does not meet the standard of
the Annals of Statistics.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*Review completed 2026-06-27.*