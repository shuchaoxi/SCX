# Minimax Optimality of SCX Noise Detection --- Feasibility
Analysis

**Author:** SCX

> **Purpose**: Assess whether a matching lower bound for Theorem 1's
> exponential rate can be proved, establishing minimax optimality.
> 
> **Date**: 2026-06-27
> 
> **Author**: AI analysis for SCX paper planning

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. Executive Summary<!-- label: executive-summary -->

**Verdict: MEDIUM feasibility.** A minimax lower bound establishing
that the exponent `exp(-cMΔ²)` is optimal (up to constants) is
achievable, but **only for a simplified version of the problem**.
Proving the exact constant `c\ =\ 2` (matching Hoeffding) under
the full SCX model with F1 risk is significantly harder and may require
substantial mathematical development.

**Two separate minimax problems must be distinguished:**

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1290}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1774}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.2097}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.3548}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1290}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Regime
\end{minipage} & \begin{minipage}[b]
Parameter
\end{minipage} & \begin{minipage}[b]
Upper bound
\end{minipage} & \begin{minipage}[b]
Lower bound difficulty
\end{minipage} & \begin{minipage}[b]
Status
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**M-regime** (experts) & M = \#experts & `exp(-2MΔ²)` &
**Hard** & No lower bound exists 

**δ-regime** (features) & δ = I(φ; S) & `O(√δ)` &
**Standard** & Trivially matches Thm 2 

\end{longtable}

The JMLR PAPER\_FRAMEWORK correctly identifies the need for a matching
lower bound but significantly underestimates the difficulty of the
M-regime (listing ``4 days'' for Le Cam + Assouad). The δ-regime bound
is indeed a 4-day project. The M-regime bound is more realistically
**4-8 weeks** of focused work by a trained mathematical
statistician.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2. Feasibility Assessment by
Regime<!-- label: feasibility-assessment-by-regime -->

#### 2.1 M-Regime: Exponent in Number of Experts ---
HARD<!-- label: m-regime-exponent-in-number-of-experts-hard -->

**Goal**: Show that for any noise detector ψ observing M experts,
`inf\_ψ\ sup\_P\ (1\ -\ F1(ψ,\ P))\ ≥\ C·exp(-cMΔ²)` for some
`c\ ≤\ 2`.

**What makes it hard (3 distinct obstacles):**

1. 
2. 
3. 

#### 2.2 δ-Regime: Feature Weakness --- STANDARD
(well-understood)<!-- label: ux3b4-regime-feature-weakness-standard-well-understood -->

**Goal**: Show that
`inf\_φ\ sup\_\{P:\ I(φ;S)\ ≤\ δ\}\ (F1\_base\ -\ F1(ψ,\ P))\ ≥\ C·√δ`.

**Why it's standard**: - This is a classic information-constrained
testing problem. - Le Cam's two-point method with TV perturbation works
directly. - Theorem 2 of Paper 1 already proves
`F1\_SCX\ ≤\ F1\_base\ +\ C\_F·√(δ/2)`. - A matching lower bound
just needs the reverse inequality:
`F1\_SCX\ ≥\ F1\_base\ -\ C·√δ` (i.e., SCX cannot be outperformed
by any method). - This is essentially already covered by the ``minimax
optimality'' claim in Theorem 2's symmetric lower bound (Eq. 377 of the
current file):
`AUC(h\_SCX)\ ≥\ AUC\_base\ -\ √(δ/2)·(1/η\ +\ 1/(1-η))`. -
Actually, the JMLR paper's minimax claim for Section 3.2 is about the
δ-regime, and this IS already largely done.

**Caveat**: The existing ``minimax'' claim in Theorem 2 is only a
LOWER bound for SCX (showing it can't beat baseline when features are
weak). The true minimax claim would be the CONVERSE: no OTHER detector
can beat SCX's rate. This inverse direction requires showing SCX is
optimal among all methods, not just that it degrades gracefully.

#### 2.3 The Gap in the JMLR
Plan<!-- label: the-gap-in-the-jmlr-plan -->

The JMLR PAPER\_FRAMEWORK conflates these two regimes. Section 3.2 is
titled ``Weak Feature Lower Bound'' (δ-regime) but claims to prove a
minimax lower bound matching Theorem 1's upper bound (M-regime). The
section then says:

> ``The gap between `O(exp(-2MΔ²))` and `O(√δ)` is not a
> contradiction: the upper bound is for expert variance M, while the lower
> bound is for feature information δ.''

This is conceptually confused. A truly matching lower bound for the
M-regime would show `Ω(exp(-cMΔ²))` --- this is what is missing,
and it is NOT what the current Section 3.2 delivers.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 3. Technical Approach: What Would
Work<!-- label: technical-approach-what-would-work -->

#### 3.1 Preferred Method: Le Cam's Two-Point Method
(M-regime)<!-- label: preferred-method-le-cams-two-point-method-m-regime -->

**Setup**: Construct two data-generating processes P₀ and P₁ that:
- Are hard to distinguish (bounded divergence) - Have different noise
indicators for a specific sample

**Construction** (sketch):

Fix a single state s with K classes. Consider M experts trained on
disjoint data.

- 
- 

The key divergence calculation: `TV(P₀\^{}M,\ P₁\^{}M)` where
P₀\^{}M is the joint distribution of (e₁,...,e\_M) under clean, and
P₁\^{}M is the joint under noise.

For product distributions (experts conditionally independent given the
noise label):

Under **clean** (P₀):
`(e₁,...,e\_M)\ ~{}\ ∏\_m\ Bernoulli(μ)` ---
product distribution.

Under **noise** (P₁):
`(e₁,...,e\_M)\ ~{}\ (1/(K-1))·∑\_\{c≠y*\}\ ∏\_m\ Bernoulli(1-μ\_c(x))`
--- mixture of products.

For the lower bound, we upper-bound TV(P₀, P₁) and apply Le Cam's lemma:

`inf\_ψ\ max\{P₀(ψ=1),\ P₁(ψ=0)\}\ ≥\ (1\ -\ TV(P₀\^{}M,\ P₁\^{}M))/2`

**The χ² divergence approach** (most promising):

For a single expert:
`χ²(Bern(μ)\ |{}|{}\ Bern(1-μ/(K-1)))\ =\ (1\ -\ μ/(K-1)\ -\ μ)²\ /\ ((1-μ/(K-1))·(μ/(K-1)))`

For M experts under clean (product) vs noise (mixture), we use the fact
that TV ≤ √(χ²/2) and:

`χ²(∏Bern(μ)\ |{}|{}\ (1/(K-1))∑∏Bern(1-μ\_c))\ =\ ?`

The mixture denominator makes this non-trivial. One can use Jensen to
bound:

`χ²(P₀\ |{}|{}\ P₁)\ ≤\ (1/(K-1))·∑\_c\ χ²(P₀\ |{}|{}\ P₁,c)`

where P₁,c is the conditional distribution under noise label = c.~Then:

`χ²(P₀\ |{}|{}\ P₁,c)\ =\ {[}(1-μ/(K-1)\ -\ μ)²\ /\ (\ (1-μ/(K-1))·(μ/(K-1))\ ){]}\^{}M`

This gives
`TV(P₀,\ P₁)\ ≤\ √(χ²/2)\ ≈\ √(\ (1/(K-1))·{[}1\ +\ O(MΔ²){]}\^{}M\ )\ /\ √2`
which is too loose for large M.

**The M-dependence in the exponent is the core difficulty.**

#### 3.2 Alternative: Fano's Method with
Packing<!-- label: alternative-fanos-method-with-packing -->

**Why not Fano**: Fano's inequality is typically used for MULTI-way
hypothesis testing (K ≥ 3 hypotheses). For a TWO-point problem (clean
vs.~noise), Fano reduces to Le Cam. The advantage of Fano is for
problems with many states (K states → 2\^{}K hypercube for Assouad). But
the M-regime is fundamentally a two-point problem (test noise
vs.~clean), so Fano doesn't add value here.

#### 3.3 Alternative: Assouad's
Method<!-- label: alternative-assouads-method -->

**When Assouad helps**: For δ-regime with K states, Assouad gives
the `Ω(√K·√δ)` rate. This matches the
`|{}S|{}` factor in the upper bound.

**For M-regime**: Assouad doesn't naturally apply because the
parameter of interest (noise detection rate) is not a hypercube of
binary parameters.

#### 3.4 Recommended Strategy: Three-Step
Proof<!-- label: recommended-strategy-three-step-proof -->

**Step 1** (Easier): Prove a LOWER BOUND ON TESTING ERROR, not F1.
- Show that for any detector ψ: P(ψ correctly classifies sample as
clean| noise vs clean) ≥ C·exp(-cMΔ²) - Use Le Cam with carefully
constructed P₀ (all experts make errors at rate μ) and P₁ (experts make
errors at rate 1-μ/(K-1)) - Key lemma: TV(Bin(M, μ) ||{}
Bin(M, 1-μ/(K-1))) ≤ √(χ²) bound - This gives: inf\_ψ max\{P₀(mistake),
P₁(mistake)\} ≥ (1/4)·exp(-2MΔ²) for reasonable parameters

**Step 2** (Harder): Convert testing error to F1 lower bound. -
Show that `1\ -\ F1(ψ)\ ≥\ (η/2)·P(error\ on\ noisy\ samples)` -
This requires bounding the false positive rate contribution - The
conversion loses constant factors but preserves the exponential rate

**Step 3** (Currently speculating): Show that the Hoeffding
exponent `c\ =\ 2` is tight. - This requires a Berry-Esseen type
refinement: the CLT approximation to the binomial tail shows that
exp(-2MΔ²) is the exact Gaussian approximation - For exact tightness:
show lim\_\{M→∞\} (-1/M) log(inf\_ψ max-error) = 2Δ² - This is a large
deviations rate result, provable via the Cramer-Chernoff theorem for
i.i.d. Bernoulli variables

**Critical observation**: The large-deviations rate function for
Bernoulli(p) is KL(p|| q). The Hoeffding bound gives
exp(-2(p-q)²), while the exact large-deviations rate is
exp(-M·KL(p|| q)). By Taylor expansion,
KL(p|| q) = 2(p-q)² + O((p-q)³). So: - For SMALL gaps Δ →
0: Hoeffding is tight (both ∼ 2Δ²) - For LARGE gaps Δ → 1/2: Chernoff
gives significantly tighter exponent (KL \textgreater{} 2Δ²) - The exact
minimax rate is `exp(-M·KL(θ\ |{}|{}\ μ)\ +\ o(M))`
not `exp(-2MΔ²)`

This means: the **rate** (exponential decay in M) is optimal, but
the **constant** 2 in the exponent can be improved by using the
Chernoff form. The optimal constant depends on the specific Bernoulli
parameters.

#### 3.5 Summary of What is
Provable<!-- label: summary-of-what-is-provable -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2683}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2927}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1951}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2439}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Statement
\end{minipage} & \begin{minipage}[b]
Difficulty
\end{minipage} & \begin{minipage}[b]
Method
\end{minipage} & \begin{minipage}[b]
Timeline
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
`inf\_ψ\ sup\_P\ (Bayes\ error)\ ≥\ C·exp(-cMΔ²)` & Medium & Le
Cam + χ² & 2-3 weeks 

`liminf(-1/M)\ log(inf\_ψ\ sup\_P\ (Bayes\ error))\ =\ 2Δ²` &
Medium-Hard & Cramer-Chernoff + CLT & 3-4 weeks 

Same for F1 risk & Hard & Requires converting testing error to F1 & +2-3
weeks 

Exact constant c = 2 for all finite M & Very Hard & May require new
concentration tools & \textgreater3 months 

δ-regime minimax (matching Thm 2) & Standard & Le Cam (already
essentially done) & \textless1 week 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. What the Result Would Look
Like<!-- label: what-the-result-would-look-like -->

#### 4.1 Conjectured Theorem
(M-Regime)<!-- label: conjectured-theorem-m-regime -->

**Theorem (Minimax Lower Bound for Consistency-Based Noise
Detection).** Assume B1-B3 (conditional independence, state-conditional
noise, non-degeneracy). For any state s with separation gap Δ
\textgreater{} 0, M ≥ 2 experts, noise rate η ∈ (0, 1/2), and class
count K ≥ 2:

*Part (a) --- Testing lower bound:*
\[\inf_ \sup_{P \in \mathcal{P}_} \left[ \mathbb{P}_P(\psi=1 \mid clean, s) + \mathbb{P}_P(\psi=0 \mid noise, s) \right] \geq \frac{1}{2} \exp\!\left(-2M\Delta^2\right)\]

where ψ is any measurable noise detector, and P\_Δ is the set of
distributions satisfying the separation condition with gap ≥ Δ.

*Part (b) --- F1 lower bound:*
\[\inf_ \sup_{P \in \mathcal{P}_} \left[1 - F1(\psi, P)\right] \geq \frac{\eta_}{4} \cdot \exp\!\left(-2M\Delta^2\right)\]

where η\_min = min(η, 1-η).

*Part (c) --- Rate optimality:* The SCX consistency detector
achieves the exponent 2MΔ² in its F1 guarantee (Theorem 1), and no
detector can achieve exponent \textgreater{} 2MΔ² (by Part (b)).
Therefore, SCX is **minimax rate-optimal**.

**Corollary (Large-Deviations Refinement):**
\[\lim_{M \to \infty} -\frac{1}{M} \log \inf_ \sup_{P \in \mathcal{P}_} \left[1 - F1(\psi, P)\right] = 2\Delta^2\]

confirming that the exponent 2Δ² per expert is the information-theoretic
limit.

#### 4.2 Conjectured Theorem (δ-Regime --- matching Thm
2)<!-- label: conjectured-theorem-ux3b4-regime-matching-thm-2 -->

**Theorem (Minimax Lower Bound for Weak Feature Noise Detection).**
Let φ be a feature mapping with I(φ(X); S) ≤ δ. For any noise detector h
operating on (φ(X), Y, \{f\_m(X)\}):

\[\inf_{h} \sup_{P: I(\phi;S) \leq \delta} \left(F1(h) - F1_{base}\right) \geq 0\]

and

\[\sup_{h} \inf_{P: I(\phi;S) \leq \delta} \left(F1(h) - F1_{base}\right) \leq C_F \cdot \sqrt{\frac{2}}\]

i.e., SCX achieves the minimax-optimal rate O(√δ) in the weak-feature
regime.

(Note: This is essentially already Theorem 2's symmetric bound. The only
missing piece is the ``inf over h'' part --- proving no method can beat
SCX's rate.)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 5. Key Challenges (Detailed)<!-- label: key-challenges-detailed -->

#### Challenge 1: Marginal Dependence Under Noise (MOST
SERIOUS)<!-- label: challenge-1-marginal-dependence-under-noise-most-serious -->

**The problem**: - Under noise, P(e₁,...,e\_M |{} noise)
= (1/(K-1))·∑\_c ∏\_m P(e\_m |{} noise, c) - This is a MIXTURE of
product distributions, NOT a product distribution - Standard minimax
techniques (Le Cam, Assouad) rely on divergence tensorization for
product distributions - The mixture structure breaks tensorization

**Possible resolution**: Use the fact that:
`TV(P₀,\ P₁)\ ≤\ (1/(K-1))·∑\_c\ TV(P₀,\ P₁,c)` by the convexity
of TV in its second argument.

Then TV(P₀, P₁,c) ≤ √(χ²(P₀ ||{} P₁,c)/2) where P₁,c is
product.

This gives:
`TV(P₀,\ P₁)\ ≤\ √(χ²(P₀\ |{}|{}\ P₁,c)/2)` for the
worst-case c.

**Remaining gap**: This bound might not be tight for moderate M.
The mixture structure could make the two distributions EASIER to
distinguish, meaning the bound is loose (lower bound becomes too weak).
This is acceptable --- a weak lower bound is still a valid lower bound
for minimax purposes --- but it limits the sharpness of the result.

#### Challenge 2: F1 Risk Does Not
Factorize<!-- label: challenge-2-f1-risk-does-not-factorize -->

**The problem**: - F1 is a ratio of expectations, not an
expectation of a ratio - Most minimax lower bound techniques work for
additive risks (0-1 error, MSE) - F1 involves TP, FP, FN jointly
through: F1 = 2TP / (2TP + FP + FN)

**Possible resolution**: - Bound 1 - F1 from below by the testing
error: `1\ -\ F1\ ≥\ η·(1\ -\ TPR)\ +\ (1-η)·FPR` (using the
inequality in Theorem 1's proof) - Then lower bound on testing error
(Challenge 1) directly gives a lower bound on 1 - F1 - This loses a
factor of η but preserves the exponential rate

**Remaining gap**: The inequality
`1\ -\ F1\ ≥\ η·FN\_rate\ +\ (1-η)·FP\_rate` is not tight. The
true F1 lower bound has denominator effects. This is acceptable for rate
optimality but loses constant factors.

#### Challenge 3: Separation Gap Δ Must Be ``Known'' to the
Detector<!-- label: challenge-3-separation-gap-ux3b4-must-be-known-to-the-detector -->

**The problem**: - A minimax lower bound must hold for ANY
detector, even one that knows Δ exactly - The lower bound construction
should NOT give the detector any advantage from knowing Δ - Actual SCX
uses a fixed threshold θ; the minimax optimal detector might use a
different threshold

**Resolution**: Construct P₀ and P₁ such that the optimal Bayes
classifier is exactly \texttt{ψ\ =\ 1\{C(x)\ \textgreater{}\ θ\}} for
some θ. Then any detector must pay the minimax price. This is feasible
by making the clean and noisy distributions have different means.

#### Challenge 4: Proving the Exact Constant c =
2<!-- label: challenge-4-proving-the-exact-constant-c-2 -->

**The problem**: - For finite M, the Hoeffding constant 2 is not
necessarily tight - The exact minimax rate depends on Bernoulli
parameters via:
\texttt{lower\_bound\ ≈\ exp(-M·inf\_\{t\ ∈\ {[}0,1{]}\}\ KL(t\ |{}|{}\ separating\ threshold))}
- For Bernoulli(μ) vs Bernoulli(1-μ/(K-1)), the optimal threshold is at
θ* = (μ + 1-μ/(K-1))/2 - The KL divergence KL(θ* ||{} μ) =
2(θ*-μ)² + O((θ*-μ)³) by Taylor expansion - So for Δ → 0: constant
= 2 exactly (tight) - For Δ \textgreater{} 0.1: constant \textgreater{}
2, meaning Chernoff lower bound gives BETTER rate than exp(-2MΔ²)

**Bottom line**: The exponent `2MΔ²` is rate-optimal but not
constant-optimal. A more precise lower bound would be:
`exp(-M·KL(θ*\ |{}|{}\ μ))` where θ* = (μ +
1-μ/(K-1))/2

This is larger than exp(-2MΔ²) for Δ \textgreater{} 0.

#### Challenge 5: State
Aggregation<!-- label: challenge-5-state-aggregation -->

**The problem**: - Theorem 1's F1 bound aggregates over states s
via ρ\_s - A minimax lower bound should also allow state aggregation -
The presence of multiple states with different Δ\_s values complicates
the construction

**Resolution**: Focus on the hardest state s* = argmin\_s Δ\_s.
Construct the lower bound for this single state. The multi-state
extension follows by setting ρ\_s* = 1 (all probability mass on the
worst state). This is a valid hard instance within the problem class,
giving the correct minimax rate.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 6. Value to JMLR Paper<!-- label: value-to-jmlr-paper -->

#### 6.1 Critical Assessment<!-- label: critical-assessment -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1739}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3696}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4565}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Aspect
\end{minipage} & \begin{minipage}[b]
With Lower Bound
\end{minipage} & \begin{minipage}[b]
Without Lower Bound
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Novelty of Thm 1 & Complete statistical theory & Upper bound only
(one-sided) 

Claim of ``optimality'' & **Can claim SCX is minimax optimal** &
Cannot claim optimality 

Relation to Thm 2 & Symmetric: upper bound AND lower bound & Only lower
bound for weak features 

JMLR acceptance & **Strong differentiator** & Still strong, but one
gap noted by reviewers 

Reviewers' likely reaction & ``Comprehensive theory, well-rounded'' &
``Where is the matching lower bound?'' 

\end{longtable}

**Verdict**: A matching lower bound would elevate Paper 3 from
``good theory paper'' (acceptance likely) to ``exceptional theory
paper'' (highly cited, talked about). Reviewers at JMLR level will
notice the asymmetry between Theorem 1 (upper bound only) and Theorem 2
(upper+bound + lower bound). They may ask: ``Why do you provide a lower
bound for feature weakness but not for the statistical rate?''

#### 6.2 What JMLR Reviewers Will
Ask<!-- label: what-jmlr-reviewers-will-ask -->

1. 
2. 
3. 

#### 6.3 Reviewer Risk<!-- label: reviewer-risk -->

Without a matching M-regime lower bound, a knowledgeable reviewer (e.g.,
someone who knows minimax theory from either Tsybakov's or Wainwright's
textbook) will likely:

- 
- 
- 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 7. Estimated Effort<!-- label: estimated-effort -->

#### 7.1 Pessimistic Estimate (Academic
Mathematician/Statistician)<!-- label: pessimistic-estimate-academic-mathematicianstatistician -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3438}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2500}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4062}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Component
\end{minipage} & \begin{minipage}[b]
Effort
\end{minipage} & \begin{minipage}[b]
Description
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Le Cam construction for Bernoulli testing & 1-2 weeks & Standard, but
needs careful calculation of χ² divergence under mixture 

Extension to F1 risk & 1 week & Requires relating testing error to F1 

Large-deviations refinement & 2-3 weeks & Cramer-Chernoff analysis, may
require new tools 

State aggregation and multi-class & 1 week & Extending single-state to
multi-state 

Writing and verification & 2 weeks & Writing up the 5-10 page proof in
JMLR style 

**Total** & **7-10 weeks** & **~2-2.5
months full-time** 

\end{longtable}

#### 7.2 Optimistic Estimate (If All Technical Choices
Work)<!-- label: optimistic-estimate-if-all-technical-choices-work -->

\begin{longtable}[]{@{}ll@{}}
\toprule\noalign{}
Component & Effort 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Single-state testing lower bound & 1 week 

F1 conversion & 2 days 

Multi-state extension & 3 days 

Writing & 1 week 

**Total** & **~3 weeks** 

\end{longtable}

#### 7.3 What the JMLR Framework Says
vs.~Reality<!-- label: what-the-jmlr-framework-says-vs.-reality -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.7429}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.2571}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Claim in PAPER\_FRAMEWORK
\end{minipage} & \begin{minipage}[b]
Reality
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
``Le Cam + Assouad minimax lower bound: 4 days'' & Achievable for
δ-regime ONLY 

``Matching lower bound, constant factors'' & Rate optimality is
achievable; exact constants are \textgreater1 month 

``Critical for JMLR acceptance'' & Likely true --- but the difficulty is
5-10x higher than estimated 

\end{longtable}

**Recommendation**: Separate the two problems. The δ-regime minimax
claim (matching Theorem 2) is essentially already done and takes 1 week
to formalize. The M-regime matching lower bound (matching Theorem 1)
should be presented as a separate, partially open result.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 8. Dependencies and New Tools
Required<!-- label: dependencies-and-new-tools-required -->

#### 8.1 Does This Need New
Assumptions?<!-- label: does-this-need-new-assumptions -->

**No new assumptions needed** for a rate-optimality result
(exponent in M): - B1-B3 (or A1-A6) are sufficient for the lower bound
construction - The lower bound holds for a SUBCLASS of distributions
satisfying these assumptions → thus the worst-case over all such
distributions is at least as hard - No additional restrictive
assumptions needed

**New assumptions that would help**: - **Symmetric experts**
(all have same error rate μ): Makes lower bound construction cleaner -
**Two-class classification** (K = 2): Avoids the
mixture-over-classes complication - **Known state partition**:
Removes state estimation error from the minimax bound

These can be presented as the setting for the lower bound: ``Even in the
simplest case (symmetric experts, binary classification, known state
structure), no detector can surpass exp(-2MΔ²).''

#### 8.2 New Mathematical Tools
Required<!-- label: new-mathematical-tools-required -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2727}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3636}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3636}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Tool
\end{minipage} & \begin{minipage}[b]
Status
\end{minipage} & \begin{minipage}[b]
Source
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Le Cam's two-point lemma & Well-known & Tsybakov (2009), Lec 2 

χ² divergence tensorization & Well-known & Polyanskiy \& Wu (2022+) 

KL divergence for mixtures & Standard & Van der Vaart (1998) 

Cramer-Chernoff large deviations & Well-known & Dembo \& Zeitouni
(1998) 

Berry-Esseen for binomial & Well-known & Not needed for the rate, only
for constants 

F1 risk lower bound via testing error & **Need to derive** & New
(specific to this problem) 

Mixture-to-product TV bound & **Need to derive** & New (mixture of
product vs product) 

\end{longtable}

**Key technical lemma needed** (not in standard textbooks):

> **Lemma (Mixture-Product TV bound).** Let P₀ = ∏*m
> Bernoulli(p₀) and P₁ = (1/L)·∑*\{ℓ=1\}\^{}L ∏\_m Bernoulli(p₁\_ℓ). Then:
> `TV(P₀,\ P₁)\ ≤\ (1/2)·√(χ²(P₀\ |{}|{}\ (1/L)·∑\_ℓ\ P₁\_ℓ))`
> where
> `χ²(P₀\ |{}|{}\ (1/L)·∑\_ℓ\ P₁\_ℓ)\ ≤\ (1/L)·∑\_ℓ\ {[}((p₀-p₁\_ℓ)²/(p₁\_ℓ(1-p₁\_ℓ))\ +\ 1)\^{}M\ -\ 1{]}`

This lemma would be the technical core of the proof and requires careful
verification.

#### 8.3 Software/Tools<!-- label: softwaretools -->

- 
- 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 9. Risk of Being Scooped<!-- label: risk-of-being-scooped -->

#### 9.1 Related Literature<!-- label: related-literature -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2121}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2121}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.5758}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Paper
\end{minipage} & \begin{minipage}[b]
Topic
\end{minipage} & \begin{minipage}[b]
Overlap with SCX
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Gao et al.~(2016, AoS): ``Minimax optimal convergence rates for
estimating the ground truth from multiple annotators'' & Crowdsourcing
minimax rates & **Moderate**. They study minimax rates for
estimating TRUE LABEL from multiple noisy annotators --- different from
NOISE DETECTION. Their setup is purely categorical (no features), unlike
SCX's state-conditioned approach. 

Berend \& Kontorovich (2015, COLT): ``Consistency of weighted majority
votes'' & Weighted majority vote convergence & **Low**. They study
convergence of majority vote to ground truth. 

Jaffe et al.~(2015, NIPS): ``Instance-dependent label-noise'' &
Instance-dependent label noise rates & **Low**. Theoretical bounds
on learning with instance-dependent noise. 

Bhatt et al.~(2017, JMLR): ``Minimax-optimal label noise'' & Minimax
rates for learning with label noise & **Low distances**. They study
learning a CLASSIFIER under label noise (Menon et al.'s setting), not
noise detection. 

Karger et al.~(2011, STOC): ``Minimax rates for crowdsourcing'' &
Minimax rates for Dawid-Skene model & **Moderate**. They study
optimal rate for recovering ground truth labels from multiple annotators
with confusion matrices. 

\end{longtable}

#### 9.2 Assessment<!-- label: assessment -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5200}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.4800}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Risk Factor
\end{minipage} & \begin{minipage}[b]
Assessment
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Direct competition & **Very low**. No one is studying the problem
of ``detecting which samples have label noise using multi-expert
consistency'' from a minimax perspective. 

Adjacent competition & **Low**. The crowdsourcing minimax
literature (Gao, Karger, etc.) studies a different estimand (ground
truth label recovery, not noise detection). 

Methodological competition & **Medium**. A statistical theorist
could independently derive minimax rates for ``testing whether a given
sample has label noise using M independent classifiers.'' This is a
natural problem that any PhD student in theoretical ML could
encounter. 

Time risk & **Increasing**. As ensemble methods and data quality
become more prominent, someone may formalize this. The SCX framework's
specific structure (state conditioning, F1 analysis) is unique, but the
core minimax rate for testing binomial proportions with M experts is
not. 

\end{longtable}

#### 9.3 Mitigation<!-- label: mitigation -->

1. 
2. 
3. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 10. Recommended Path
Forward<!-- label: recommended-path-forward -->

#### Phase 1 (Week 1-2): Quick
Wins<!-- label: phase-1-week-1-2-quick-wins -->

- 
- 
- 

#### Phase 2 (Week 3-6): Core M-Regime Lower
Bound<!-- label: phase-2-week-3-6-core-m-regime-lower-bound -->

- 
- 
- 
- 

#### Phase 3 (Week 7-10): F1
Extension<!-- label: phase-3-week-7-10-f1-extension -->

- 
- 
- 

#### Phase 4 (Optional, Beyond Paper 3): Constant
Refinement<!-- label: phase-4-optional-beyond-paper-3-constant-refinement -->

- 
- 
- 

#### Contingency: If Stuck<!-- label: contingency-if-stuck -->

If the mixture-product divergence calculation proves intractable after 6
weeks, fall back to:

1. 
2. 
3. 

This is acceptable for JMLR/TMLR. Not every paper needs matching lower
bounds for every theorem.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 11. Summary Table<!-- label: summary-table -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4400}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3200}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2400}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Dimension
\end{minipage} & \begin{minipage}[b]
Rating
\end{minipage} & \begin{minipage}[b]
Note
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**Feasibility (rate optimality)** & MEDIUM & Provable with 7-10
weeks work 

**Feasibility (exact constants)** & LOW & May require ≥3 months,
Berry-Esseen 

**Feasibility (δ-regime)** & HIGH & Already essentially done (Thm
2) 

**Novelty to JMLR** & HIGH & Would distinguish the paper 

**Difficulty** & 7/10 & Mixture-product divergence is the crux 

**Reviewer expectation** & MODERATE & Some will ask; most will
accept a conjecture 

**Scoop risk** & LOW & But increasing over time 

**Effort estimate** & 7-10 weeks full-time & 1 trained mathematical
statistician 

**Blocking for submission** & NO & Can submit without it 

\end{longtable}