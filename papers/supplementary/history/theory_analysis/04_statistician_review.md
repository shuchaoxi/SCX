# Hostile Review: SCX Theorems 1 and 4' — Statistical Defect Analysis

**Reviewer Role**: Annals of Statistics hostile referee
**Scope**: Theorem 1 (Noise Detection Guarantee), Theorem 4' (Exact Constant Minimax Optimality), supporting Lemmas A-F
**Review Date**: 2026-06-28

---

## Executive Summary

Six attacks were mounted against the SCX theoretical framework. Three reveal genuine defects, one of which (Lemma F additivity) is FATAL and undermines the multi-state aggregation claim entirely. Two attacks identify MAJOR issues (Bahadur-Rao lattice correction omission, Lemma F false finitesample claim). The remaining attacks are either OK or MINOR.

The overall verdict: **NOT ready for Annals of Statistics**. The multi-state constant optimality claim is unsupported. The "exact constant" claim for the single-state case is technically incorrect due to the ignored lattice correction in the Bahadur-Rao expansion. The cross-file verification report (already known to the authors) documents that key formulas were inconsistent by factors of 15-18x across files — a sign of insufficient quality control for a journal submission.

---

## Attack 1: Hoeffding Inequality Usage (Lemma 2 and Lemma 3)

### Claim
The FPR bound (Lemma 2) and TPR bound (Lemma 3) use Hoeffding's inequality on conditionally independent expert errors e_m:

```
P(C > θ | clean, X ∈ s) ≤ exp(-2M(θ - μ_s)²)                     [Lemma 2]
P(C > θ | noise, X ∈ s) ≥ 1 - exp(-2M(1 - C_bal·μ_s/(K-1) - θ)²) [Lemma 3]
```

### Analysis

**(a) Independence verification.** For clean samples, A2 asserts conditional independence of {e_m} given x. The proof chain A1 => A2 is mathematically sound: each e_m is a function of f_m(x), which depends only on training set D_m; since D_m are independent, {f_m(x)} are conditionally independent given x. However, this requires models to be deterministic functions of their training data. In practice, SGD, random initialization, and data augmentation introduce randomness that is not captured by training-set independence alone. The assumption is standard for theoretical work but the "A1 guarantees A2" claim is too strong without also assuming deterministic training.

**(b) Distributional variation within states.** The bound uses sup_{x∈s} μ_s to bound E[C|x] uniformly. This is conservative: for Lemma 2, the true Hoeffding bound is exp(-2M(θ - E[C|x])²) and since E[C|x] ≤ μ_s and θ > μ_s, we have (θ - E[C|x]) ≥ (θ - μ_s), giving exp(-2M(θ - E[C|x])²) ≤ exp(-2M(θ - μ_s)²). Direction is correct. For Lemma 3, similarly (E[C|x,c] - θ) ≥ (1 - C_bal·μ_s/(K-1) - θ), so the Hoeffding bound on P(C ≤ θ) is exp(-2M(E[C|x,c] - θ)²) ≤ exp(-2M(1 - C_bal·μ_s/(K-1) - θ)²). Again correct.

**(c) The "averaging over c" step in Lemma 3.** The proof averages P(C ≤ θ | x, c) over the K-1 noise classes. Since each class c yields the same bound (by A6 uniformly bounding μ_c(x)), the average is ≤ the same bound. Correct.

**(d) Gap condition.** Lemma 3 requires θ < 1 - C_bal·μ_s/(K-1). The theorem's threshold condition ensures this. For K=2 with C_bal > 1 and μ_s > 1/(C_bal+1), the condition can fail because p_1 = 1 - C_bal·μ_s < μ_s = p_0, reversing the gap entirely. Both THEOREMS_UNIFIED.md and the source file mention this restriction, but it is easy to miss. A reader could mistakenly apply Theorem 1 with C_bal=2, K=2, μ_s=0.4, getting p_1 = 1 - 0.8 = 0.2 and p_0 = 0.4, so p_1 < p_0 — the detection gap is negative. The theorem's assumption "μ_s < θ < 1 - C_bal·μ_s/(K-1)" would be contradictory for K=2, C_bal=2, μ_s=0.4 since 1 - 0.8 = 0.2 < 0.4 = μ_s, making the interval empty.

**(e) A2 scope gap.** Assumption A2 states conditional independence "for clean samples." Lemma 3's proof requires conditional independence for noise samples too (conditioning on x and noise class c). The proof is correct under the spirit of the assumption (the randomness in e_m given (x,c) still comes only from D_m), but A2 as written does not literally cover this case. A minor oversight.

### Verdict: MINOR

The inequality directions and Hoeffding applications are mathematically correct. The A2 scope gap (clean-only coverage) is minor and fixable. The C_bal×K=2 edge case is acknowledged but underemphasized.

---

## Attack 2: A2 (Conditional Independence) Testability

### Claim
A2 asserts that {e_m(x,y)} are conditionally independent given x for clean samples, and the text states "A1 ensures A2" or "Follows from A1."

### Analysis

**(a) Testability.** Given a single input x, we observe only one label y and one set of expert predictions {f_m(x)}. Without repeated observations at the same x (which are impossible in a continuous input space), the joint distribution P(e_1,...,e_M | x) is unobservable. Conditional independence is therefore **untestable** from data. This is not fatal per se — many statistical assumptions (e.g., Gaussianity) are untestable but widely accepted. However, the document's claim that A2 "可检验" (testable) in the Chinese source text is incorrect. The "合理性说明" (rationale) section argues A1 implies A2, which is a mathematical deduction, not an empirical test.

**(b) Practical violation sources.** Even with disjoint training sets (A1), experts will produce correlated errors on out-of-distribution samples or samples near decision boundaries. For example, all experts may misclassify an unusual input because they were trained on similar (though disjoint) data from the same distribution. This correlation is not captured by A1-A2. In the CIFAR-10 experiment reported (Section 4.3 of Theorem 1), the empirical F1 of 0.617 is far below the Theorem 1 bound of 0.976 (computed with μ_s=0.2). The document attributes this to μ_s being higher (0.45 vs 0.2), but the discrepancy is also consistent with expert correlation violating A2.

**(c) Does violation break the theorem?** If experts are positively correlated, the Hoeffding bound is no longer valid (it requires independence). The effective sample size for the consensus score is less than M, and the exponential rate degrades. The theorem's guarantee would not hold. This is a genuine limitation for practical applications.

### Verdict: MAJOR

The conditional independence assumption is untestable and likely violated in practice. The A1→A2 link is mathematically valid but does not account for practical correlations from shared data distributions. This limits the theorem's applicability to carefully controlled experimental settings.

---

## Attack 3: Theorem 1 F1 Lower Bound Derivation

### Claim
The F1 bound derivation proceeds as:
```
F1 ≥ 1 - δ₁ - (1-η)δ₂/η ≥ 1 - (1/η) Σ ρ_s exp(-2MΔ_s²)
```

### Analysis

**(a) Algebraic verification.** Starting from:
```
F1 = 2η·TPR / (η(1+TPR) + (1-η)FPR)
```
Substituting TPR ≥ 1-δ₁, FPR ≤ δ₂:
```
F1 ≥ 2η(1-δ₁) / (η(2-δ₁) + (1-η)δ₂)
```
The denominator D = η(2-δ₁) + (1-η)δ₂ ≥ η (since δ₁ ≤ 1 gives 2-δ₁ ≥ 1, and δ₂ ≥ 0). So:
```
1 - F1 ≤ (D - 2η(1-δ₁))/D = (ηδ₁ + (1-η)δ₂)/D ≤ (ηδ₁ + (1-η)δ₂)/η = δ₁ + ((1-η)/η)δ₂
```
Each step uses the fact that D ≥ η > 0 implies 1/D ≤ 1/η, and the numerator ηδ₁ + (1-η)δ₂ is non-negative. The algebra is entirely correct.

**(b) η → 0 degeneracy.** When η → 0, the bound becomes:
```
F1 ≥ 1 - (1/0)·Σρ_s·exp(-2MΔ_s²) = -∞
```
This is technically valid (F1 is always finite, so F1 ≥ -∞ is true) but completely vacuous. The document acknowledges this in Lemma B Section B.6.1, defining η_min(M) as the threshold below which the expansion breaks down. For realistic M, η_min is exponentially small, so the issue is theoretical rather than practical. However, the Theorem 1 statement presents the bound as generally valid without this caveat.

**(c) The bound is not an F1 guarantee but an error bound transformation.** The bound is a purely algebraic consequence of the FPR/FNR tail bounds. If the tail bounds are tight, the F1 bound is tight. But the document's "紧致性实验" (tightness experiment) shows the bound can be extremely loose: for CIFAR-10 (μ_s=0.45, η=0.1, M=20), the bound gives F1 ≥ 0.18 while the empirical F1 is 0.617. This 3.4× gap shows the bound is far from tight.

### Verdict: OK (with documented caveats)

The algebra is correct. The η→0 degeneracy is acknowledged (though not in the Theorem 1 statement itself). The looseness is honestly discussed.

---

## Attack 4: Numerical Counterexample

### Claim
Construct a case where the bound F1 ≥ 1 - (1/η) exp(-2MΔ²) is violated.

### Analysis

**(a) Attempted construction.** Using K_Y=3, μ_s=0.1, θ=0.4, M=5, η=0.05:
- Condition: μ_s=0.1 < θ=0.4 < 1 - 0.1/2 = 0.95 ✓
- Δ_s = min(0.4-0.1, 0.95-0.4) = min(0.3, 0.55) = 0.3
- Bound: F1 ≥ 1 - (1/0.05)·exp(-2·5·0.3²) = 1 - 20·exp(-0.9) = 1 - 20·0.4066 = 1 - 8.13 = -7.13

The bound gives F1 ≥ -7.13, which is vacuous (F1 is always ≥ 0). This is not a counterexample — the bound is valid but useless. For non-vacuous bounds, we need exp(-2MΔ²) < η, which requires M > log(1/η)/(2Δ²). With η=0.05, Δ=0.3, this gives M > 16.6. So M ≥ 17 is needed for a non-vacuous bound.

**(b) Non-vacuous test.** K_Y=10, μ_s=0.2, θ=0.5, M=50, η=0.1:
- Δ_s = min(0.3, 0.978-0.5) = min(0.3, 0.478) = 0.3
- Bound: F1 ≥ 1 - (1/0.1)·exp(-2·50·0.09) = 1 - 10·exp(-9) = 1 - 10·0.000123 = 0.9988

For this to be violated, we would need the actual F1 to be below 0.9988, meaning at least 0.12% of the 1-F1 budget is error. Given that the Hoeffding bound guarantees P(misclassification | clean) ≤ exp(-9) ≈ 1.2×10⁻⁴ per state, and P(detection | noise) ≥ 1 - exp(-9) ≈ 0.9999, the actual F1 should indeed be near 1. The bound is plausible.

**(c) Could the bound ever be violated?** The bound is a mathematical consequence of the assumptions. If A1-A6 hold, the bound MUST hold by construction. Finding a violation would require A1-A6 to fail in some subtle way that still allows them to appear satisfied. The most plausible attack vector is A5 (state homogeneity): if μ_s underestimates the true within-state error rate, the Hoeffding gap shrinks and the bound could fail. But this is a violation of A5, not a counterexample to the theorem.

### Verdict: OK

No counterexample exists under A1-A6. The bound can be vacuous but not violated. The non-vacuous regime requires M ≥ Ω(log(1/η)/Δ²), which the document acknowledges in Corollary 2.

---

## Attack 5: Bahadur-Rao Exactness (Theorem 4')

### Claim
Theorem 4' uses Bahadur-Rao (1960) to obtain an "exact constant" for the F1 error, claimed to be minimax optimal.

### Analysis

**(a) The lattice correction problem (critical).** The Bahadur-Rao theorem for Bernoulli distributions (which are lattice with span h=1) produces:

```
P(bar{X}_M ≥ θ) = exp(-M·KL(θ||p)) / ((1-e^{-λ*})·√(2πM·θ(1-θ))) · (1 + O(1/M))
```

where (1-e^{-λ*})⁻¹ is the lattice correction factor. The document instead uses:

```
P(bar{X}_M ≥ θ) = exp(-M·KL(θ||p)) / (λ*·√(2πM·θ(1-θ))) · (1 + O(1/M))
```

These differ by the multiplicative factor λ*/(1-e^{-λ*}). For Test Case 1 (p₀=0.10, p₁=0.60):
- λ₀* = 1.404, giving λ₀*/(1-e^{-1.404}) = 1.404/0.754 = 1.862
- |λ₁*| = 1.198, giving |λ₁*|/(1-e^{-1.198}) = 1.198/0.698 = 1.716

The ratio of corrections is 1.862/1.716 ≈ 1.085, so the lattice correction does NOT cancel in the F1 constant. The true Bahadur-Rao constant for Bernoulli includes this correction; the document's constant does not.

Lemma A Section A.4.2 acknowledges this discrepancy: "Both forms are asymptotically equivalent as λ* → 0 (i.e., as θ ↓ p), but differ by a constant factor for fixed λ* > 0." The claim that "Both forms agree in the O(1/M) asymptotic expansion up to a constant factor" is misleading — a multiplicative constant factor is precisely what the "exact constant" claim is about. The constant factor is O(1), not O(1/M).

**(b) Impact on the exact constant claim.** The "exact constant minimax optimality" requires the constant to be the TRUE minimax constant. Since the 1/λ* form omits the lattice correction, the claimed constant C_min/η is not the true constant for the Bernoulli testing problem. The matching between the achievable constant and the lower bound is internal consistency (both use the same approximation), not a proof of exact optimality with respect to the true problem.

**(c) Regularity conditions.** The document correctly verifies that Bernoulli satisfies the Bahadur-Rao conditions (analytic CGF, unique saddlepoint). The O(1/M) error bound in Proposition A.5 is explicitly derived. These aspects are sound.

**(d) The O(1/M) threshold shift.** Lemma D's correct insight — that an O(1/M) shift in θ produces an O(1) multiplicative factor ((1-η)/η)^s — is mathematically valid and represents genuine intellectual contribution. The verification report confirms that the adaptive threshold achieves a smaller constant than the naive θ*, and this part is correct.

### Verdict: MAJOR

The "exact constant" claim is technically incorrect due to the ignored lattice correction. The constant C_min as defined (using 1/λ* form) is an approximation to the true minimax constant. The document should either include the lattice correction in all formulas, or explicitly qualify the claim (e.g., "exact constant in the 1/λ* expansion"). The O(1/M) threshold shift analysis is valuable and correct.

---

## Attack 6: Lemma F Multi-State Additivity

### Claim
Lemma F states:
```
F1_global(M) = Σ ρ_s · F1_s(M)        [exact equality]
1 - F1_global(M) = Σ ρ_s · (1 - F1_s(M))   [exact equality]
```
with the proof invoking "law of total expectation."

### Analysis

**(a) The nonlinearity of F1.** The population-level F1 is:
```
F1_global = 2·TP_total / (2·TP_total + FP_total + FN_total)
```
where TP_total = Σ TP_s, FP_total = Σ FP_s, FN_total = Σ FN_s (summing across states). The per-state F1 is:
```
F1_s = 2·TP_s / (2·TP_s + FP_s + FN_s)
```

These are related by:
```
F1_global = 2·Σ TP_s / (2·Σ TP_s + Σ FP_s + Σ FN_s)
Σ ρ_s · F1_s = Σ ρ_s · [2·TP_s / (2·TP_s + FP_s + FN_s)]
```

These are NOT equal in general. F1 is a ratio of sums, and the weighted sum of ratios does not equal the ratio of weighted sums. This is a basic property of harmonic means.

**(b) Numerical counterexample.** Consider two states with η=0.1:
- State 1 (ρ=0.5): TPR=0.99, FPR=0.01
- State 2 (ρ=0.5): TPR=0.01, FPR=0.99

```
F1_1 = 2·0.1·0.99 / (0.1·(1+0.99) + 0.9·0.01) = 0.198 / 0.208 = 0.952
F1_2 = 2·0.1·0.01 / (0.1·(1+0.01) + 0.9·0.99) = 0.002 / 0.992 = 0.002
Weighted avg: 0.5·0.952 + 0.5·0.002 = 0.477

Global TPR = 0.5·0.99 + 0.5·0.01 = 0.50
Global FPR = 0.5·0.01 + 0.5·0.99 = 0.50
F1_global = 2·0.1·0.50 / (0.1·(1+0.50) + 0.9·0.50) = 0.100 / 0.600 = 0.167
```

0.477 ≠ 0.167. The alleged equality is false.

**(c) Why the "law of total expectation" argument fails.** The document treats F1 as an expectation over samples, writing F1(M) = E[F1]. But F1 is a population-level metric defined from a confusion matrix, not a random variable that exists per sample. The "law of total expectation" reasoning:
```
E[F1] = Σ Pr(state=s) · E[F1 | state=s] = Σ ρ_s · F1_s
```
is only valid if F1 is a linear function of per-sample indicators. It is not. The confusion matrix counts (TP, FP, FN) are sums over samples, but F1 = 2TP/(2TP+FP+FN) is a nonlinear function of these counts.

**(d) Are the asymptotic conclusions still correct?** Remarkably, yes — but for different reasons than stated. As M → ∞:
```
1 - F1_global ≈ (1/2)FNR_global + ((1-η)/(2η))FPR_global  [from Lemma B]
= (1/2) Σ ρ_s FNR_s + ((1-η)/(2η)) Σ ρ_s FPR_s           [linearity of expectation]
= Σ ρ_s [(1/2)FNR_s + ((1-η)/(2η))FPR_s]                  [linearity]
≈ Σ ρ_s (1 - F1_s) + O(e^{-2Mκ_min})                       [asymptotic expansion]
```

The error in the last step is of order O(exp(-2Mκ_min)), which is o(exp(-Mκ_min)). So the asymptotic limit is correct. The bottleneck state still dominates the rate. However:

**(e) The finite-M bound is wrong.** Lemma F Part 4 gives:
```
1 - F1_global(M) ≤ max_s (1 - F1_s(M))
```
This relies on the additivity claim. Since additivity fails at finite M, this bound is also unsupported. The correct bound would be:
```
1 - F1_global ≤ 1 - 2·Σρ_sTP_s / (2·Σρ_sTP_s + Σρ_sFP_s + Σρ_sFN_s)
```
which does NOT simplify to the claimed form.

**(f) The constant C_global is unsupported.** The document defines C_global = Σ_{s: κ_s=κ_global} ρ_s C_s based on the additivity. While the asymptotic limit happens to work out (because the nonlinearity error is o(exp(-Mκ_min))), the derivation is invalid. A correct derivation would need to show directly that:
```
lim e^{Mκ_global}√(2πM)(1-F1_global) = Σ_{s∈S_min} ρ_s C_s / η
```
using the global F1 formula, not the weighted average of per-state F1s.

### Verdict: FATAL

The Lemma F additivity claim is mathematically false. The proof is invalid (misapplication of the law of total expectation to a nonlinear function). While the asymptotic conclusions happen to be correct by coincidence (the nonlinearity error decays exponentially faster than the leading term), the finite-sample statements are unsupported, and the derivation is fundamentally flawed. A complete rewrite of Lemma F with a correct proof is required.

---

## Attack 7: Cross-Theorem Consistency — The Verification Report

### Claim
The document claims "All inconsistencies have been resolved" (THEOREMS_UNIFIED.md Section 4.2).

### Analysis

The verification report (verification_exact_constant.md) documents that as of 2026-06-27:
- C_min was defined **three different ways** across files, differing by factors of **15-18x**
- Lemma D's Theorem D.7 used the wrong constant (θ* instead of θ_opt), giving values 1.7-2.41× off
- Lemma D Section D.4 was "mathematically incoherent" with self-contradictory derivations

THEOREMS_UNIFIED.md claims these are resolved. However:
- The coordination between files is fragile. The "canonical" THEOREMS_UNIFIED.md now states the correct formulas, but the individual lemma files still contain the old (incorrect) derivations
- Lemma A's lattice correction issue (Attack 5) remains untouched
- Lemma F's additivity error (Attack 6) is not addressed

### Verdict: MAJOR

The cross-file inconsistency was more extensive than the document acknowledges, and at least two issues (lattice correction, Lemma F additivity) remain unresolved.

---

## Defect Summary Table

| Bug ID | Description | Severity | Fixable? | Location |
|--------|-------------|----------|----------|----------|
| F-1 | Lemma F additivity: F1_global = Σρ_s·F1_s is mathematically false. Misapplication of LOTUS to nonlinear function. | **FATAL** | Yes — requires complete rewrite of Lemma F with correct global F1 derivation | Lemma F, THEOREMS_UNIFIED.md §4.2(d) |
| F-2 | Finite-M bound in Lemma F Part 4 relies on false additivity claim | **FATAL** (consequence of F-1) | Yes — must derive correct finite-M bound from global confusion matrix | Lemma F |
| M-1 | Bahadur-Rao lattice correction omitted: 1/λ* form used instead of (1-e^{-λ*})⁻¹, giving O(1) constant error. "Exact constant" claim is technically incorrect for Bernoulli. | **MAJOR** | Yes — include lattice correction in all formulas, or qualify "exact constant in the 1/λ* asymptotic expansion" | Lemma A, Theorem 4', C_min definition |
| M-2 | A2 (conditional independence) untestable and practically violated by experts trained on similar distributions. "A1 ensures A2" oversells the guarantee. | **MAJOR** | Partially — add discussion of practical limitations and correlation effects | Assumptions A1-A2, Theorem 1 |
| M-3 | Lemma D Section D.4 historically contained self-contradictory derivations (per verification report). THEOREMS_UNIFIED.md claims fix but lemma file not updated. | **MAJOR** | Yes — verify Lemma D file matches THEOREMS_UNIFIED.md | Lemma D |
| M-4 | C_min defined inconsistently across three files (15-18x discrepancy). THEOREMS_UNIFIED.md claims resolution but individual lemma files not reconciled. | **MAJOR** | Yes — audit all lemma files for remaining inconsistencies | Multiple |
| m-1 | A2 explicitly covers "clean samples" only; Lemma 3's TPR proof requires conditional independence for noise samples | **MINOR** | Yes — extend A2 to cover all samples, or add remark | A2, Lemma 3 |
| m-2 | K=2 with C_bal > 1 can make the interval (μ_s, 1-C_bal·μ_s) empty; this edge case is documented but easy to miss | **MINOR** | Yes — add explicit warning in Theorem 1 statement | Theorem 1 |
| m-3 | Theorem 1's F1 bound becomes vacuous as η→0; not noted in the main statement | **MINOR** | Yes — add brief caveat to Theorem 1 | Theorem 1 |

---

## Detailed Bug Explanations

### F-1: Lemma F Additivity (FATAL)

The claim "F1_global(M) = Σ ρ_s · F1_s(M)" is presented as an exact equality for all finite M, with the "Proof" stating "By the law of total expectation." But F1 is not a sample-level random variable — it is a population-level function of the confusion matrix. The correct relationship between global and per-state quantities is:

```
TP_global = N·η·Σ ρ_s·TPR_s
FP_global = N·(1-η)·Σ ρ_s·FPR_s
FN_global = N·η·Σ ρ_s·(1-TPR_s)

F1_global = 2·TP_global / (2·TP_global + FP_global + FN_global)
           = 2η·Σρ_s·TPR_s / (2η·Σρ_s·TPR_s + (1-η)·Σρ_s·FPR_s + η·Σρ_s·(1-TPR_s))

F1_s = 2η·TPR_s / (2η·TPR_s + (1-η)·FPR_s + η·(1-TPR_s))
     = 2η·TPR_s / (η·(1+TPR_s) + (1-η)·FPR_s)
```

The weighted average Σ ρ_s·F1_s involves individual denominators per state; the global F1 involves a single denominator with summed numerators. These are algebraically distinct.

**Fix**: Rewrite Lemma F using the global confusion matrix directly:
1. Express 1-F1_global in terms of FNR_global = Σ ρ_s·FNR_s and FPR_global = Σ ρ_s·FPR_s
2. Apply the Bahadur-Rau expansion to Σ ρ_s·FNR_s and Σ ρ_s·FPR_s
3. Show that the asymptotic limit gives C_global = Σ_{s∈S_min} ρ_s·C_s by directly evaluating the leading terms

This is salvageable because FNR_global and FPR_global ARE linear in per-state quantities, and the F1_global expansion (Lemma B) separates the nonlinearity into o(exp(-Mκ_min)) terms.

### M-1: Bahadur-Rao Lattice Correction (MAJOR)

The Bahadur-Rau theorem for lattice distributions (Bernoulli included) contains the factor (1-e^{-λ*})⁻¹ rather than 1/λ*. The document's Lemma A derives the lattice-corrected form in Section A.4.2 (eq. A.2) but then "absorbs" the correction by using the 1/λ* form in the summary table. The two forms differ by the constant λ*/(1-e^{-λ*}), which is O(1) and does NOT vanish as M→∞.

For the Test 1 parameters (p₀=0.10, p₁=0.60):
- The FPR constant would change by factor 1.862
- The FNR constant would change by factor 1.716
- Their ratio (1.085) does not cancel in the F1 expression

The claim of "exact constant" requires the lattice correction to be included. The document's numerical verification (Section 4.3 of THEOREMS_UNIFIED.md) only checks internal consistency (C_SCX = C_min/η using the same 1/λ* formulas), not external validity against the true Bernoulli tail.

**Fix**: Either:
- (Preferred) Replace all 1/λ* factors with (1-e^{-λ*})⁻¹ in Lemma A, Lemma D, Lemma E, and Theorem 4'. Update C_min accordingly.
- (Minimal) Add an explicit qualifier: "C_min gives the leading constant in the 1/λ* form of the Bahadur-Rau expansion; the true Bernoulli constant includes an additional lattice correction factor λ*/(1-e^{-λ*}) which can be incorporated explicitly."

---

## Final Assessment

The SCX theoretical framework contains genuine mathematical contributions (the adaptive threshold O(1/M) shift analysis, the Chernoff information rate characterization, the F1 expansion). However, two critical defects prevent its acceptance at Annals of Statistics in the current form:

1. **FATAL (F-1/F-2)**: The multi-state F1 aggregation (Lemma F) is founded on a mathematically false claim about F1 linearity. While the asymptotic conclusions survive by coincidence (the error decays at twice the leading rate), the proof is invalid and the finite-M bounds are unsupported.

2. **MAJOR (M-1)**: The "exact constant" claim ignores the Bahadur-Rau lattice correction for Bernoulli distributions. The claimed constant is valid only in the 1/λ* approximation, not for the actual Bernoulli testing problem.

The combination of a FATAL error and a MAJOR misrepresentation of exactness would likely result in a **reject** decision. Both are fixable with careful rewriting, but the Lemma F issue in particular requires a complete re-derivation.

---

*本分析由 Codex orchestrator agent 4 (统计学家审查) 生成，2026-06-28*