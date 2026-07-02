\section{Hostile Review: Minimax Lower Bound Proof (Theorem
4)}<!-- label: hostile-review-minimax-lower-bound-proof-theorem-4 -->

**Document reviewed:** `minimax\_lower\_bound\_proof.md`
**Reviewer stance:** Annals of Statistics hostile reviewer
**Overall verdict:** The central claim (rate optimality, exponent
\(2M\Delta^2\)) is **likely correct in spirit but rests on an
invalid inequality in its critical step**. The proof as written is
**not acceptable** for publication.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{Summary of Fatal and Non-Fatal
Issues}<!-- label: summary-of-fatal-and-non-fatal-issues -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2800}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4000}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3200}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Issue
\end{minipage} & \begin{minipage}[b]
Severity
\end{minipage} & \begin{minipage}[b]
Status
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Lemma 7 (Slud's inequality) is false & **Fatal** & The claimed
inequality is not a consequence of Slud (1977) and fails numerically for
many parameter values 

K=2 to K\textgreater2 reduction conflates bound truth with bound
looseness & **Major** & The argument that ``K=2 is hardest'' uses
direction of an inequality opposite to what is needed 

F1 conversion (Lemma 8) derivation is algebraically unsound &
**Major** & The claimed inequality
\(1-F1 \geq 1-TPR\) has an unverified validity
condition 

Mixture-product TV bound (Lemma 4) & **Correct** & Convexity
argument is valid; direction is appropriate for Le Cam 

Le Cam construction and symmetry & **Correct** & Construction is
within the allowed class under A6 with \(C_bal=1\) 

Cramer-Chernoff large deviations & **Correct** & Standard
asymptotic analysis 

\(\chi^2\) tensorization & **Correct** & Convexity bound handles
mixture before tensorization; no independence violation 

\(\eta\) factor gap & **Incomplete** & Acknowledged by author, but
leaves the \(\eta\) characterization unresolved 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{1. Lemma 7 (Slud's Inequality) is False as
Stated}<!-- label: lemma-7-sluds-inequality-is-false-as-stated -->

**Claim (Lemma 7).** Let \(S_M \sim Binomial(M,p)\) with
\(p \leq 1/2\). For any \(k\) with \(p \leq k/M \leq 1/2\):

\[\mathbb{P}(S_M \geq k) \;\geq\; \frac12 \exp\!\Bigl(-2M\bigl(\tfrac{k}{M} - p\bigr)^2\Bigr).\]

**This inequality is not a valid consequence of Slud (1977) and is
numerically false.**

\subsubsection{1.1 What Slud Actually
Proves}<!-- label: what-slud-actually-proves -->

Slud (1977), Theorem 2, gives a **Gaussian comparison** inequality:

\[\mathbb{P}(S_M \geq k) \;\geq\; \frac12 \;\Phi\!\left(-\frac{k-Mp}{\sqrt{Mp(1-p)}}\right),\]

where \(\Phi\) is the standard normal CDF. This is a genuine result.
However, the further step of bounding the Gaussian tail by
\((1/2)\exp(-2M\delta^2)\) uses the inequality

\[\Phi(-t) \;\geq\; \frac{1}{\sqrt{2\pi}}\frac{t}{1+t^2}e^{-t^2/2}, \qquad t > 0.\]

Combining these gives

\[\mathbb{P}(S_M \geq k) \;\geq\; \frac12 \cdot \frac{1}{\sqrt{2\pi}}\frac{t}{1+t^2}\exp\!\bigl(-t^2/2\bigr)\]

where \(t = \delta\sqrt{M}/\sqrt{p(1-p)}\) and \(\delta = k/M - p\). The
exponent here is \(t^2/2 = M\delta^2/(2p(1-p))\), **not**
\(2M\delta^2\). The two exponents differ by the factor \(1/(4p(1-p))\).

Since \(p(1-p) \leq 1/4\), we have \(1/(4p(1-p)) \geq 1\), meaning

\[\exp\!\bigl(-M\delta^2/(2p(1-p))\bigr) \;\leq\; \exp\!\bigl(-2M\delta^2\bigr).\]

The **inequality goes the wrong direction**: Slud's actual bound
gives a Gaussian exponent that is *larger* than \(2M\delta^2\),
producing a *smaller* RHS, not a larger one. The author attempts to
replace the correct Gaussian exponent \(M\delta^2/(2p(1-p))\) with the
smaller Hoeffding exponent \(2M\delta^2\) while *simultaneously*
claiming a *larger* lower bound. This is algebraically impossible
without a compensating factor that would be enormous (roughly
\(\exp(M\delta^2\cdot(1/(2p(1-p))-2))\)), and no such factor appears.

\subsubsection{1.2 Numerical
Counterexamples}<!-- label: numerical-counterexamples -->

The claimed inequality fails for multiple parameter settings:

**Example 1:** \(M=20\), \(p=0.4\), \(k=10\) (so \(\delta=0.1\)).

\[\mathbb{P}(Bin(20,0.4) \geq 10) \approx 0.244, \qquad RHS = 0.5\cdot e^{-40\cdot 0.01} = 0.5\cdot e^{-0.4} \approx 0.335.\]

\(0.244 \not\geq 0.335\). The inequality is violated by nearly 40\%.

**Example 2:** \(M=10\), \(p=0.3\), \(k=5\) (\(\delta=0.2\)).

\[\mathbb{P}(Bin(10,0.3) \geq 5) \approx 0.151, \qquad RHS = 0.5\cdot e^{-20\cdot 0.04}=0.5\cdot e^{-0.8} \approx 0.225.\]

\(0.151 \not\geq 0.225\).

**Example 3:** \(M=100\), \(p=0.4\), \(k=50\) (\(\delta=0.1\)).

\[\mathbb{P}(Bin(100,0.4) \geq 50) \approx 0.027, \qquad RHS = 0.5\cdot e^{-200\cdot 0.01}=0.5\cdot e^{-2} \approx 0.068.\]

\(0.027 \not\geq 0.068\).

These are not edge cases; they are squarely in the parameter regime the
proof requires (\(p=\mu<1/2\), \(\delta=1/2-\mu\)).

\subsubsection{\texorpdfstring{1.3 Ceiling Issue for Odd
\(M\)}{1.3 Ceiling Issue for Odd M}}<!-- label: ceiling-issue-for-odd-m -->

The proof applies Slud's inequality with \(k = \lceil M/2\rceil\), but
Slud's condition requires \(k/M \leq 1/2\). For odd \(M\),
\(\lceil M/2\rceil/M = (M+1)/(2M) = 1/2 + 1/(2M) > 1/2\), violating the
premise. The author silently replaces \(\lceil M/2\rceil/M\) with
\(1/2\) in the exponent, which is an approximation that does not respect
the inequality's domain.

\subsubsection{1.4 Impact on the Main
Proof}<!-- label: impact-on-the-main-proof -->

This is not a minor technical issue. The Binomial tail lower bound is
**the entire content** of the testing lower bound for \(K=2\). If
Lemma 7 is false, the claimed exponent \(2M\Delta^2\) is
unsubstantiated. The correct Slud-based bound gives

\[\mathbb{P}(Bin(M,\mu) \geq M/2) \;\geq\; \frac{1}{2\sqrt{2\pi}}\frac{t}{1+t^2}\exp\!\Bigl(-\frac{M(1/2-\mu)^2}{2\mu(1-\mu)}\Bigr),\]

which has exponent \(M\Delta^2/(2\mu(1-\mu))\) rather than
\(2M\Delta^2\). Since \(\mu(1-\mu) \leq 1/4\), the correct exponent is
*at least* \(2M\Delta^2\) (i.e., the same or faster decay), but the
prefactor depends on \(\mu\) and \(M\) and the bound is much weaker in
finite samples.

The author needs to prove a lower bound, and a bound that decays
*faster* (with larger exponent) is a *stronger* lower bound
for that exponent. Actually, wait -- a larger exponent means the RHS is
*smaller*, which gives a *weaker* lower bound on the
probability. So the correct Slud bound gives a *smaller* RHS than
what the author claims. This makes the author's bound an
*overestimate* of the true minimal possible RHS.

To salvage the result, the author would need to show that the minimax
risk is at least \((1/2)\exp(-2M\Delta^2)\) even though
\(\mathbb{P}(Bin(M,\mu) \geq M/2)\) may be smaller than this.
This would require a different argument entirely, as the current proof
relies on the optimal Bayes test having error exactly
\(\mathbb{P}(Bin(M,\mu) \geq M/2)\).

#### 1.5 Recommendation<!-- label: recommendation -->

Lemma 7 must be either (a) replaced with the correct Slud inequality and
the Gaussian tail bound, which would yield a different (potentially
\(\mu\)-dependent) exponent; or (b) proved from first principles if the
claimed form is actually true (which the counterexamples above suggest
it is not). The author should check whether Slud's proof can be adapted
to yield the claimed bound for the specific case \(p=\mu\), \(k=M/2\) --
perhaps via a sharper inequality that does not go through the Gaussian
approximation -- but as it stands, the proof does not provide this.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{2. The K=2 to K\textgreater2 Reduction is Logically
Inverted}<!-- label: the-k2-to-k2-reduction-is-logically-inverted -->

**Claim (Section 4.6).** For \(K>2\), the per-component \(\chi^2\)
divergence is larger than for \(K=2\), and ``since larger \(\chi^2\)
makes the distributions more distinguishable, the \(K=2\) case is the
hardest.''

\subsubsection{2.1 The Argument's
Structure}<!-- label: the-arguments-structure -->

The author writes:

> For \(K>2\):
> \(\chi^2_{bern} = \frac{4(\Delta^*)^2}{(1-\mu/(K-1))\cdot \mu/(K-1)} \geq 16(\Delta^*)^2\)
> This is *larger* than the \(K=2\) case. Since larger \(\chi^2\)
> makes the distributions more distinguishable, the \(K=2\) case is the
> hardest.

Then concludes the \(K=2\) lower bound holds for \(K>2\).

#### 2.2 The Gap<!-- label: the-gap -->

For \(K=2\), the noise distribution \(P_1\) is a **product**
\(Bernoulli(1-\mu)^{\otimes M}\). For \(K>2\), \(P_1\) is a
**mixture**
\(\frac{1}{K-1}\sum_{c\neq y^*} Bernoulli(1-\mu/(K-1))^{\otimes M}\).
The author uses Lemma 4 to bound

\[TV(P_0, P_1) \;\leq\; \sqrt{\frac{(1+\chi^2_{bern})^M - 1}{2}}.\]

This is an **upper bound** on TV. For the purpose of the Le Cam
lower bound \(\inf R \geq (1 - TV)/2\), a *smaller* upper
bound on TV gives a *stronger* lower bound on risk. A *larger*
upper bound (from larger \(\chi^2\)) gives a *weaker* lower bound.

The author's argument treats the \(\chi^2\) value as if it directly
measures the difficulty of distinguishing \(P_0\) from \(P_1\). But the
bound \(TV \leq \sqrt{((1+\chi^2)^M - 1)/2}\) is not tight in
general; it becomes looser as \(\chi^2\) grows. The author confuses:

- 
- 

For a concrete illustration: if \(\chi^2_1 < \chi^2_2\), it is entirely
possible that \(\sqrt{((1+\chi^2_2)^M - 1)/2} \gg 1\) (bound useless)
while the actual \(TV(P_0, P_1)\) is close to 0 (very hard to
distinguish). The bound does not rule this out.

\subsubsection{2.3 Why the Conclusion is Probably Correct (But Not
Proved
Here)}<!-- label: why-the-conclusion-is-probably-correct-but-not-proved-here -->

The \(K=2\) case is likely the hardest because under
\(C_{bal}=1\), all mixture components for \(K>2\) are identical
(same parameter \(1-\mu/(K-1)\)), making \(P_1\) a single product
distribution, not a true mixture. For \(K>2\), the ``gap'' between
\(\mu\) and \(1-\mu/(K-1)\) is larger, making the product distributions
more separated. This intuition is correct, but the proof as written
**does not make this argument**. Instead, it invokes the \(\chi^2\)
bound in a way that is logically reversed. The author should simply note
that under \(C_{bal}=1\), \(P_1\) is a product (all components
equal), and the per-expert TV is \(|1 - \mu K/(K-1)|\), which exceeds
\(|1-2\mu|\) for \(K>2\), so \(K=2\) gives the smallest separation
(hence hardest). No \(\chi^2\) bounding is needed.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{3. The F1 Lower Bound Derivation is Algebraically
Unsound}<!-- label: the-f1-lower-bound-derivation-is-algebraically-unsound -->

#### 3.1 The Claim<!-- label: the-claim -->

Lemma 8 states:

\[1 - F1(\psi) \;\geq\; \eta \cdot \mathbb{P}(\psi=0 \mid noise) + (1-\eta) \cdot \mathbb{P}(\psi=1 \mid clean),\]

but the derivation that follows does not establish this. Instead, the
author ends with the weaker inequality

\[1 - F1(\psi) \;\geq\; \mathbb{P}(\psi=0 \mid noise).\]

#### 3.2 Tracing the Derivation<!-- label: tracing-the-derivation -->

The author writes the F1 expression, then performs several algebraic
manipulations that appear to be in **draft form** -- incomplete
cancellations, substitutions that don't match definitions, and a
denominator identity that is incorrect. Specifically:

The author writes: ``Denominator
\(= \eta + \eta\cdotTPR + (1-\eta)FNR\)''.

But the actual denominator of \(1-F1\) after substituting
\(TP = \eta\cdotTPR\), \(FP = (1-\eta)FPR\),
\(FN = \eta(1-TPR)\) is:

\[2TP + FP + FN = 2\eta\cdotTPR + (1-\eta)FPR + \eta(1-TPR) = \eta(1+TPR) + (1-\eta)FPR.\]

This does not match the author's
``\(\eta + \eta\cdotTPR + (1-\eta)FNR\)'' unless
\(FNR = 1-TPR = FPR\), which is not generally true.
The derivation contains an algebraic inconsistency.

#### 3.3 The Hidden Condition<!-- label: the-hidden-condition -->

The final inequality \(1-F1 \geq 1-TPR\) is equivalent (by
cross-multiplication, as shown below) to

\[\frac{FP+FN}{2TP+FP+FN} \;\geq\; \frac{FN}{TP+FN} \;\iff\; TP(FP - FN) \geq 0 \;\iff\; FP \geq FN.\]

Substituting \(FP = (1-\eta)FPR\),
\(FN = \eta(1-TPR)\), the condition becomes

\[(1-\eta)FPR \;\geq\; \eta(1-TPR).\]

For the author's construction,
\(FPR \approx FNR = 1-TPR\) (they differ by at most
\(P(S=M/2)\)), so the condition requires \(\eta \leq 1/2\), which holds
by assumption. But the author **never checks this condition**. The
inequality is presented as if it holds universally, which it does not.
For a detector with \(FPR \ll FNR\) (e.g., a conservative
test that rarely flags), the inequality can fail.

#### 3.4 Why This Matters<!-- label: why-this-matters -->

The \(1/\eta\) factor in the upper bound (Theorem 1) creates a potential
gap: the upper bound degrades as \(\eta \to 0\), but the lower bound's
\(\eta\) dependence is lost by the one-sided inequality
\(1-F1 \geq 1-TPR\). A proper F1 lower bound should retain
the \(\eta\) factor to match the upper bound's scaling. The author
acknowledges this in a remark but does not resolve it.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. Other Issues<!-- label: other-issues -->

\subsubsection{4.1 Lemma 4 (Mixture-Product TV Bound) --
Correct}<!-- label: lemma-4-mixture-product-tv-bound-correct -->

The convexity inequality
\(TV(P_0, \frac{1}{L}\sum_\ell Q_\ell) \leq \frac{1}{L}\sum_\ell TV(P_0, Q_\ell)\)
is valid: TV is jointly convex, so it is convex in each argument. The
bound direction (upper bound on TV) is correct for the Le Cam
application. For the symmetric case (\(C_{bal}=1\)), all
\(Q_\ell\) are equal, so the inequality is tight. No issue here.

\subsubsection{4.2 Le Cam Construction --
Correct}<!-- label: le-cam-construction-correct -->

The construction is within the SCX assumption class. Choosing the
hardest instance within \(\mathcal{P}_\Delta\) is standard for minimax
lower bounds. The symmetry assumption \(C_{bal}=1\) is
restrictive but permissible for a lower bound. The construction
correctly satisfies A1-A6.

\subsubsection{4.3 Cramer-Chernoff Analysis --
Correct}<!-- label: cramer-chernoff-analysis-correct -->

The asymptotic analysis is standard and correctly identifies
\(KL(1/2 \| \mu)\) as the exact error exponent for the optimal
Bayes test. The Taylor expansion
\(KL(1/2 \| 1/2-\Delta) = 2\Delta^2 + O(\Delta^4)\) is correct.
The claim that \(2\Delta^2\) is the worst-case (minimum) exponent over
\(\mu\) is also correct, since \(\mu(1-\mu) \leq 1/4\) implies
\(KL \geq 2\Delta^2\). The concern raised in the review prompt
about ``the adversary chooses the threshold'' is not relevant here, as
the author is analyzing the optimal Bayes test (which is
likelihood-ratio based) rather than the threshold-based SCX detector.

\subsubsection{\texorpdfstring{4.4 \(\chi^2\) Tensorization --
Correct}{4.4 \ chi\^{}2 Tensorization -- Correct}}<!-- label: chi2-tensorization-correct -->

The tensorization
\(\chi^2(\prod P_m \| \prod Q_m) = \prod(1+\chi^2(P_m\|Q_m))-1\) is
well-known for products. The proof handles the mixture case by first
applying the convexity bound (Lemma 4), which reduces the mixture to a
sum of per-component TV terms. Each term involves a product \(Q_\ell\),
so the tensorization applies to each term individually. There is no
independence violation.

\subsubsection{\texorpdfstring{4.5 The \(\eta\) Factor
Gap}{4.5 The \ eta Factor Gap}}<!-- label: the-eta-factor-gap -->

The upper bound from Theorem 1 contains a \(1/\eta\) factor:
\(F1 \geq 1 - (1/\eta)\exp(-2M\Delta^2)\). The lower bound in
Theorem 4 gives \(1-F1 \geq (1/2)\exp(-2M\Delta^2)\) without the
\(\eta\) factor. The gap between \(1/\eta\) and \(1/2\) can be
arbitrarily large as \(\eta \to 0\). This does not contradict the rate
optimality claim (which focuses on the exponent in \(M\Delta^2\)), but
it means the lower bound is not tight in \(\eta\), and the claim of
``matching'' in the comparison table (Section 5.3) is overstated for the
pre-factor. The author correctly notes this as a limitation.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{5. Summary: What Would Need to Be
Fixed}<!-- label: summary-what-would-need-to-be-fixed -->

#### Required for Publication<!-- label: required-for-publication -->

1. 
2. 
3. 

#### Cosmetic but Important<!-- label: cosmetic-but-important -->

1. 
2. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 6. Bottom Line<!-- label: bottom-line -->

The proof attempts to show that \(\exp(-2M\Delta^2)\) is the
minimax-optimal rate. The construction and the Le Cam framework are
appropriate. The mixture-product TV bound, the \(\chi^2\) tensorization,
and the Cramer-Chernoff refinement are technically correct.

**However, the proof collapses at Lemma 7.** The claimed inequality
is not a valid consequence of Slud (1977) and is numerically false for
parameters required by the proof. Without a valid Binomial tail lower
bound, the entire lower bound on the testing error is unsupported. The
remaining issues (K\textgreater2 reduction, F1 derivation) are fixable
with rewriting, but Lemma 7 is fundamental and cannot be patched with
cosmetic changes.

**Recommendation:** Major revision required. The author should
either (a) derive the correct lower bound using the Gaussian comparison
form of Slud's inequality, which will yield a \(\mu\)-dependent
exponent, and then show that the minimax rate \(2M\Delta^2\) still
follows (perhaps by a different argument); or (b) use an alternative
technique (e.g., Le Cam combined with a direct TV calculation for
products) that avoids the Binomial tail bound entirely.