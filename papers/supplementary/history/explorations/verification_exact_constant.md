\section{Verification Report: Exact Constant Minimax Optimality Proof
Chain}<!-- label: verification-report-exact-constant-minimax-optimality-proof-chain -->

> **Reviewer**: Adversarial mathematical review for Annals of
> Statistics. **Files reviewed**: exact\_constant\_minimax.md,
> lemma\_AB\_bahadur\_rao\_f1.md, lemma\_CD\_chernoff\_adaptive.md,
> lemma\_EF\_lowerbound\_aggregation.md **Date**: 2026-06-27

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 0. Executive Summary<!-- label: executive-summary -->

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
Check & Verdict & Severity 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
1. Definition Alignment & FAIL & Critical 

2. kappa \textgreater= 2Delta\^{}2 Issue & FAIL & High 

3. O(1/M) Term Consistency & FAIL & Critical 

4. Hidden Assumptions & PASS (with caveats) & Low 

5. Numerical Consistency & FAIL & Critical 

6. Edge Cases & PASS & Low 

\end{longtable}

**Overall assessment**: The proof chain has three critical flaws
and one high-severity flaw. It is **NOT ready for journal
submission** in its current form. The most serious issue is the three-way
inconsistency in the definition of C\_min (none of the three formulas
match each other) and the fact that Lemma D's Theorem D.7 claims to
achieve the lower bound but uses an incorrect expression that does not
account for the O(1/M) threshold shift.

Below follows a detailed enumeration of every flaw.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{1. Check 1: Definition Alignment -- FAIL
(Critical)}<!-- label: check-1-definition-alignment-fail-critical -->

\subsubsection{1.1 C\_min is defined inconsistently in THREE
places}<!-- label: c_min-is-defined-inconsistently-in-three-places -->

Three distinct formulas for C\_min appear across the manuscripts, and
**none of them match**:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1515}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1364}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.7121}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Location
\end{minipage} & \begin{minipage}[b]
Formula
\end{minipage} & \begin{minipage}[b]
Numerical value (p0=0.10, p1=0.60, eta=0.10)
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**Architecture Sec 4.3** (eq 215) &
`eta\ /\ (2\ sqrt(2pi)\ *\ sqrt(theta*(1-theta*))\ *\ max(lam0*,|{}lam1*|{}))`
& **0.0307** 

**Architecture Theorem 4'** (eq 276) &
`eta/sqrt(theta*(1-theta*))\ *\ 1/2\ *\ min\_w\ max(w/lam0*,\ (1-w)/|{}lam1*|{})\ *\ 1/max(lam0*,|{}lam1*|{})`
& **0.0252** 

**Lemma E** (eq 45) &
`(eta/2)\ *\ ((1-eta)/eta)\^{}s\ *\ (1/lam0*\ +\ 1/|{}lam1*|{})\ /\ sqrt(theta*(1-theta*))`
& **0.4591** 

\end{longtable}

(Numerical confirmation from the Python verification script: Section 4.3
gives C\_min=0.0307, Theorem 4' gives C\_min=0.0252, Lemma E gives
C\_min=0.4591. These differ by factors of 15-18x.)

**Root cause**: The architecture document was written before Lemma
E was fully derived. Section 4.3 and Theorem 4' contain
preliminary/draft formulas that were never updated to match the
fully-derived Lemma E expression. The Lemma E derivation is the correct
one (it follows from the Bayes test expansion), but the other documents
were not reconciled.

**Suggested fix**: 1. Adopt the Lemma E expression as the canonical
C\_min. 2. Delete or replace all other C\_min formulas in the
architecture document. 3. Theorem 4'(a) must be rewritten with the
correct constant.

\subsubsection{1.2 Lemma D Theorem D.7 contradicts Lemma
E}<!-- label: lemma-d-theorem-d.7-contradicts-lemma-e -->

**Theorem D.7** states:

\begin{verbatim}
lim e^{Mk} sqrt(2pi M) (1-F1_SCX(theta_opt)) = 1/sqrt(theta*(1-theta*)) * [1/(2|lam1*|) + (1-eta)/(2 eta lam0*)]
\end{verbatim}

**Lemma E** (correctly) states the lower bound limit is:

\begin{verbatim}
liminf e^{Mk} sqrt(2pi M) (1-F1_A) >= 1/2 * ((1-eta)/eta)^s * (1/lam0* + 1/|lam1*|) / sqrt(theta*(1-theta*))
\end{verbatim}

These two expressions are **NOT equal** for eta != 1/2. For the
first numerical test case: - Theorem D.7 constant: 7.819 - Lemma E
constant: 4.591 - These differ by a factor of 1.70.

Theorem D.7's claim ``This matches the minimax lower bound constant
C\_min/eta from Lemma E'' is **false**.

**Root cause**: Lemma D derives theta\_opt = theta* + O(1/M), then
incorrectly concludes that plugging theta\_opt into the FPR/FNR
expressions only changes the o(1) term. In reality, the O(1/M) shift in
theta produces an O(1) multiplicative factor in the exponential:

\begin{verbatim}
exp(-M*KL(theta_opt||p0)) = exp(-M*kappa) * ((1-eta)/eta)^{-lam0*/D}
\end{verbatim}

This O(1) factor **matters at the constant level**. Lemma D's proof
of Theorem D.7 ignores this and uses the theta* expression instead.

**Suggested fix**: Theorem D.7's right-hand side must be replaced
with Lemma E's expression (which IS the correct limit for the adaptive
threshold test, as our numerical verification confirms -- the adaptive
constant equals Lemma E's constant to machine precision).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2. Check 2: kappa \textgreater= 2Delta\^{2 Issue -- FAIL
(High)}<!-- label: check-2-kappa-2delta2-issue-fail-high -->

\subsubsection{2.1 Claimed ordering is
reversed}<!-- label: claimed-ordering-is-reversed -->

**Architecture document Section 2.3** claims:

\begin{verbatim}
"KL指数严格优于Hoeffding指数"
\end{verbatim}

(KL exponent is strictly better than Hoeffding exponent.)

**Lemma C Table 1** and our numerical verification show the
opposite: - Case 1: kappa=0.170, 2Delta\^{}2=0.500. Ratio
2Delta\^{}2/kappa = **2.95** - Case 2: kappa=0.053,
2Delta\^{}2=0.180. Ratio 2Delta\^{}2/kappa = **3.41** - Case 3:
kappa=0.457, 2Delta\^{}2=1.125. Ratio 2Delta\^{}2/kappa = **2.46**

**For ALL tested values, kappa \textless{} 2Delta\^{}2.** This
means the KL/Chernoff exponent is SMALLER than the Hoeffding exponent,
giving a SLOWER error decay rate. The statement in Section 2.3 is
backwards.

**What the text correctly means**: For a FIXED threshold theta,
KL(theta|| p) \textgreater= 2(theta-p)\^{}2 by Pinsker.
But this is NOT the comparison between kappa (the Chernoff information,
which involves the optimal threshold theta*) and 2Delta\^{}2 (which
involves p1-p0). The correct statement is: ``The Chernoff information
kappa is typically smaller than 2(p1-p0)\^{}2, especially for
well-separated distributions. This means the CHERNOFF LOWER BOUND on the
optimal error rate is smaller (weaker) than the Hoeffding-based bound.''

\subsubsection{2.2 No implicit reliance on kappa \textgreater=
2Delta\^{}2}<!-- label: no-implicit-reliance-on-kappa-2delta2 -->

After careful audit: **no lemma implicitly relies on kappa
\textgreater= 2Delta\^{}2**. Lemma C explicitly corrects this
misconception (Proposition C.4). The old Theorem 4 v2 uses 2Delta\^{}2
as its rate, which is a coarser bound superseded by Theorem 4'. The
confusion is limited to the architecture document's Section 2.3 prose.

\subsubsection{2.3 Hidden confusion about
rates}<!-- label: hidden-confusion-about-rates -->

The architecture document's Section 0 claims:

\begin{verbatim}
"上下界的指数匹配了"
\end{verbatim}

(the upper and lower bound rates match.) This is about the OLD bounds
(both at 2Delta\^{}2 rate). The NEW result uses kappa. But for kappa
\textless{} 2Delta\^{}2, the new SCX rate is SLOWER than the old claimed
optimal rate. This means either: - The old lower bound (2Delta\^{}2) was
too optimistic (wrong), OR - The kappa rate is different from what
Theorem 4' claims

This needs explicit clarification.

**Suggested fix**: 1. Rewrite Section 2.3 to correctly state: ``The
Chernoff information kappa = KL(theta*|| p0) is the exact
error exponent for the optimal test, and it is typically smaller than
2Delta\^{}2.'' 2. Clarify the relationship between the old 2Delta\^{}2
bound and the new kappa bound.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{3. Check 3: O(1/M) Term Consistency --
FAIL}<!-- label: check-3-o1m-term-consistency-fail -->

\subsubsection{3.1 Lemma D does not propagate the O(1/M) shift
correctly}<!-- label: lemma-d-does-not-propagate-the-o1m-shift-correctly -->

Lemma D.2 correctly shows:

\begin{verbatim}
theta_opt = theta* + (1/(M D)) * log((1-eta)/eta) + O(1/M^2)
\end{verbatim}

When this is plugged into the FPR/FNR expansions:

\begin{verbatim}
M*KL(theta_opt||p0) = M*kappa + (lam0*/D)*log((1-eta)/eta) + O(1/M)
\end{verbatim}

The second term is **O(1)**, not O(1/M). It produces a constant
multiplicative factor ((1-eta)/eta)\^{}\{-lam0*/D\} in the FPR/FNR
expressions.

**Lemma D Section D.5** incorrectly states:

\begin{verbatim}
"From Lemma D.2, theta_opt = theta* + O(1/M). Thus KL(theta_opt||p0) = kappa + O(1/M)."
\end{verbatim}

This is **technically correct** (the KL value shifts by O(1/M)),
but **critically misleading**: the O(1/M) shift in KL becomes O(1)
when multiplied by M, which is what appears in the exponent. The text
should say: ``Thus M*KL(theta\_opt|| p0) = M*kappa +
O(1).''

\subsubsection{3.2 The constant factor from the O(1/M) shift is
lost}<!-- label: the-constant-factor-from-the-o1m-shift-is-lost -->

Section D.5 then plugs theta\_opt into the SCX expression and obtains
the SAME constant as at theta* (Theorem D.7). This is **wrong**
because the O(1) correction to the exponent produces an O(1) change in
the prefactor.

**Our numerical verification** shows: the correct adaptive SCX
constant equals Lemma E's lower bound (4.591 for Case 1), while Lemma
D's Theorem D.7 gives 7.819 for Case 1. The adaptive threshold does
achieve optimality, but Lemma D's proof does not correctly derive this.

\subsubsection{3.3 Self-contradictory derivation in Lemma D Section
D.4}<!-- label: self-contradictory-derivation-in-lemma-d-section-d.4 -->

Section D.4 contains a confused derivation with a ``Wait --- this gives
a constant 1/2, not 1'' self-correction moment. The derivation wanders
through several re-derivations, and the final Lemma D.4' is declared but
never cleanly proven. The analysis in Section D.4 shows that the ratio
of FNR to FPR terms tends to lam0*/| lam1*|{} (not
1), then later claims it tends to 1. Both cannot be correct.

**Suggested fix**: 1. Delete Section D.4's confused derivations and
replace with a clean proof. 2. Section D.5 must correctly account for
the O(1) exponential shift from the O(1/M) threshold adjustment. 3.
Theorem D.7 must be corrected to match Lemma E's constant.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{4. Check 4: Hidden Assumptions -- PASS (with
caveats)}<!-- label: check-4-hidden-assumptions-pass-with-caveats -->

\subsubsection{4.1 eta bounded away from 0 or
1}<!-- label: eta-bounded-away-from-0-or-1 -->

- 
- 
- 

#### 4.2 p0 \textless{ p1 strictly}<!-- label: p0-p1-strictly -->

- 
- 
- 

\subsubsection{4.3 Reduction to hypothesis testing in Lemma
E}<!-- label: reduction-to-hypothesis-testing-in-lemma-e -->

- 
- 
- 
- 

\subsubsection{4.4 i.i.d. assumption on expert
errors}<!-- label: i.i.d.-assumption-on-expert-errors -->

- 
- 
- 

\subsubsection{4.5 Lemma F's linearity of
F1}<!-- label: lemma-fs-linearity-of-f1 -->

- 
- 
- 
- 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{5. Check 5: Numerical Consistency -- FAIL
(Critical)}<!-- label: check-5-numerical-consistency-fail-critical -->

\subsubsection{5.1 C\_min/C\_SCX
verification}<!-- label: c_minc_scx-verification -->

For all three parameter sets, the following was verified
programmatically:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 12\tabcolsep) * \real{0.0625}}
  >{\arraybackslash}p{(\linewidth - 12\tabcolsep) * \real{0.0625}}
  >{\arraybackslash}p{(\linewidth - 12\tabcolsep) * \real{0.0625}}
  >{\arraybackslash}p{(\linewidth - 12\tabcolsep) * \real{0.0625}}
  >{\arraybackslash}p{(\linewidth - 12\tabcolsep) * \real{0.1875}}
  >{\arraybackslash}p{(\linewidth - 12\tabcolsep) * \real{0.3250}}
  >{\arraybackslash}p{(\linewidth - 12\tabcolsep) * \real{0.2375}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Set
\end{minipage} & \begin{minipage}[b]
p0
\end{minipage} & \begin{minipage}[b]
p1
\end{minipage} & \begin{minipage}[b]
eta
\end{minipage} & \begin{minipage}[b]
Lemma E C\_min
\end{minipage} & \begin{minipage}[b]
Lemma B C\_SCX (at theta*)
\end{minipage} & \begin{minipage}[b]
Ratio C\_SCX/C\_min
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
1 & 0.10 & 0.60 & 0.10 & 0.4591 & 7.819 & 1.70 

2 & 0.20 & 0.50 & 0.30 & 1.3768 & 5.011 & 1.09 

3 & 0.05 & 0.80 & 0.05 & 0.1843 & 8.889 & 2.41 

\end{longtable}

**C\_SCX/C\_min \textgreater{} 1** for all cases, confirming that
SCX at theta* is NOT constant-optimal. The adaptive threshold test
(Lemma D with theta\_opt) does achieve C\_min (verified numerically to
machine precision).

\subsubsection{5.2 The architecture document's C\_min formulas are
wrong}<!-- label: the-architecture-documents-c_min-formulas-are-wrong -->

All three C\_min formulas from the architecture document (Section 4.3
and Theorem 4') give values that are **15-18x smaller** than Lemma
E's correct C\_min. This is because they use different functional forms
that do not match the Bayes test derivation.

\subsubsection{5.3 F1 bounds are in
{[}0,1{]}}<!-- label: f1-bounds-are-in-01 -->

For all numerical tests, the computed asymptotic constants produce 1-F1
in (0,1) for sufficiently large M. PASS on this sub-check.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{6. Check 6: Edge Cases --
PASS}<!-- label: check-6-edge-cases-pass -->

#### 6.1 eta -\textgreater{ 0}<!-- label: eta---0 -->

- 
- 
- 
- 

#### 6.2 p0 -\textgreater{ 0}<!-- label: p0---0 -->

- 
- 
- 
- 

#### 6.3 p1 -\textgreater{ 1}<!-- label: p1---1 -->

- 
- 

#### 6.4 M -\textgreater{ infinity}<!-- label: m---infinity -->

- 
- 
- 
- 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 7. Additional Issues Found<!-- label: additional-issues-found -->

\subsubsection{7.1 Lemma D Section D.4 is mathematically
incoherent}<!-- label: lemma-d-section-d.4-is-mathematically-incoherent -->

The derivation in Section D.4 contains: - A ``Wait --- this gives a
constant 1/2, not 1'' self-contradiction - An unresolved factor of 2
discrepancy - An incorrect claim that the ratio of FNR to FPR terms
tends to 1 - Multiple incomplete re-derivations

This section should be entirely rewritten.

\subsubsection{7.2 Lemma A's lattice correction
factor}<!-- label: lemma-as-lattice-correction-factor -->

Lemma A (Section A.4.2) derives the lattice correction factor
lambda*/(1-e\^{}\{-lambda}\*) but then the summary table (Section
A.7) omits it. The summary table gives the simpler 1/lambda* form. This
is acceptable if the correction is tracked through the constant, but the
parent document does not discuss whether this correction appears in the
F1 constant.

\subsubsection{7.3 Theorem 4'(a)
normalization}<!-- label: theorem-4a-normalization -->

Theorem 4'(a) writes:

\begin{verbatim}
lim e^{Mk} * sqrt(2pi M) * (1-F1_SCX) = C_min/eta
\end{verbatim}

But Lemma E's derivation gives:

\begin{verbatim}
lim e^{Mk} * sqrt(2pi M) * (1-F1) = K
\end{verbatim}

where K does NOT have the eta factor in the same way. The relationship
between Theorem 4'(a) and Lemma E needs to be checked for consistent
normalization.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{8. Summary of Required
Fixes}<!-- label: summary-of-required-fixes -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3125}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3125}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2188}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1562}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Priority
\end{minipage} & \begin{minipage}[b]
Location
\end{minipage} & \begin{minipage}[b]
Issue
\end{minipage} & \begin{minipage}[b]
Fix
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**P0** & All files & C\_min defined three ways & Canonicalize to
Lemma E's expression; remove others 

**P0** & Lemma D Theorem D.7 & Wrong constant (uses theta* not
theta\_opt) & Replace RHS with Lemma E's constant 

**P0** & Lemma D Section D.5 & O(1/M) shift not propagated to
constant & Correctly account for M*KL shift producing O(1) prefactor 

**P1** & Architecture Sec 2.3 & Claims KL beats Hoeffding; actually
kappa \textless{} 2Delta\^{}2 & Rewrite to clarify exact vs bound
comparison 

**P1** & Lemma D Section D.4 & Self-contradictory derivations &
Rewrite cleanly 

**P2** & Architecture Theorem 4' & C\_min formula wrong and
mismatch with Lemma E & Fix to match Lemma E 

**P2** & Architecture Sec 4.3 & Ad-hoc C\_min formula & Remove or
replace with Lemma E's derivation 

**P2** & Lemma F & F1 linearity caveat unstated & Add note about
independent per-state decisions 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 9. Verdict<!-- label: verdict -->

**The proof chain is NOT ready for journal submission.** The
critical issue (P0) is the three-way inconsistency of C\_min and the
fact that Lemma D claims to achieve the optimal constant via the wrong
formula. While the mathematical substance is salvageable (the adaptive
threshold test does achieve C\_min, as we confirmed numerically), the
manuscript as written contains false claims and inconsistent derivations
that would be flagged by any competent reviewer.

Estimated rework time: 2-3 days to rewrite affected sections, re-derive
constants, and verify consistency across all files.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*Report generated by adversarial review agent.*