# Verification Report: Exact Constant Minimax Optimality Proof Chain

> **Reviewer**: Adversarial mathematical review for Annals of Statistics.
> **Files reviewed**: exact_constant_minimax.md, lemma_AB_bahadur_rao_f1.md, lemma_CD_chernoff_adaptive.md, lemma_EF_lowerbound_aggregation.md
> **Date**: 2026-06-27

---

## 0. Executive Summary

| Check | Verdict | Severity |
|-------|---------|----------|
| 1. Definition Alignment | FAIL | Critical |
| 2. kappa >= 2Delta^2 Issue | FAIL | High |
| 3. O(1/M) Term Consistency | FAIL | Critical |
| 4. Hidden Assumptions | PASS (with caveats) | Low |
| 5. Numerical Consistency | FAIL | Critical |
| 6. Edge Cases | PASS | Low |

**Overall assessment**: The proof chain has three critical flaws and one high-severity flaw. It is **NOT ready for journal submission** in its current form. The most serious issue is the three-way inconsistency in the definition of C_min (none of the three formulas match each other) and the fact that Lemma D's Theorem D.7 claims to achieve the lower bound but uses an incorrect expression that does not account for the O(1/M) threshold shift.

Below follows a detailed enumeration of every flaw.

---

## 1. Check 1: Definition Alignment -- FAIL (Critical)

### 1.1 C_min is defined inconsistently in THREE places

Three distinct formulas for C_min appear across the manuscripts, and **none of them match**:

| Location | Formula | Numerical value (p0=0.10, p1=0.60, eta=0.10) |
|----------|---------|-----------------------------------------------|
| **Architecture Sec 4.3** (eq 215) | `eta / (2 sqrt(2pi) * sqrt(theta*(1-theta*)) * max(lam0*,|lam1*|))` | **0.0307** |
| **Architecture Theorem 4'** (eq 276) | `eta/sqrt(theta*(1-theta*)) * 1/2 * min_w max(w/lam0*, (1-w)/|lam1*|) * 1/max(lam0*,|lam1*|)` | **0.0252** |
| **Lemma E** (eq 45) | `(eta/2) * ((1-eta)/eta)^s * (1/lam0* + 1/|lam1*|) / sqrt(theta*(1-theta*))` | **0.4591** |

(Numerical confirmation from the Python verification script: Section 4.3 gives C_min=0.0307, Theorem 4' gives C_min=0.0252, Lemma E gives C_min=0.4591. These differ by factors of 15-18x.)

**Root cause**: The architecture document was written before Lemma E was fully derived. Section 4.3 and Theorem 4' contain preliminary/draft formulas that were never updated to match the fully-derived Lemma E expression. The Lemma E derivation is the correct one (it follows from the Bayes test expansion), but the other documents were not reconciled.

**Suggested fix**: 
1. Adopt the Lemma E expression as the canonical C_min.
2. Delete or replace all other C_min formulas in the architecture document.
3. Theorem 4'(a) must be rewritten with the correct constant.

### 1.2 Lemma D Theorem D.7 contradicts Lemma E

**Theorem D.7** states:
```
lim e^{Mk} sqrt(2pi M) (1-F1_SCX(theta_opt)) = 1/sqrt(theta*(1-theta*)) * [1/(2|lam1*|) + (1-eta)/(2 eta lam0*)]
```

**Lemma E** (correctly) states the lower bound limit is:
```
liminf e^{Mk} sqrt(2pi M) (1-F1_A) >= 1/2 * ((1-eta)/eta)^s * (1/lam0* + 1/|lam1*|) / sqrt(theta*(1-theta*))
```

These two expressions are **NOT equal** for eta != 1/2. For the first numerical test case:
- Theorem D.7 constant: 7.819
- Lemma E constant: 4.591
- These differ by a factor of 1.70.

Theorem D.7's claim "This matches the minimax lower bound constant C_min/eta from Lemma E" is **false**.

**Root cause**: Lemma D derives theta_opt = theta* + O(1/M), then incorrectly concludes that plugging theta_opt into the FPR/FNR expressions only changes the o(1) term. In reality, the O(1/M) shift in theta produces an O(1) multiplicative factor in the exponential:
```
exp(-M*KL(theta_opt||p0)) = exp(-M*kappa) * ((1-eta)/eta)^{-lam0*/D}
```
This O(1) factor **matters at the constant level**. Lemma D's proof of Theorem D.7 ignores this and uses the theta* expression instead.

**Suggested fix**: Theorem D.7's right-hand side must be replaced with Lemma E's expression (which IS the correct limit for the adaptive threshold test, as our numerical verification confirms -- the adaptive constant equals Lemma E's constant to machine precision).

---

## 2. Check 2: kappa >= 2Delta^2 Issue -- FAIL (High)

### 2.1 Claimed ordering is reversed

**Architecture document Section 2.3** claims:
```
"KL指数严格优于Hoeffding指数"
```
(KL exponent is strictly better than Hoeffding exponent.)

**Lemma C Table 1** and our numerical verification show the opposite:
- Case 1: kappa=0.170, 2Delta^2=0.500. Ratio 2Delta^2/kappa = **2.95**
- Case 2: kappa=0.053, 2Delta^2=0.180. Ratio 2Delta^2/kappa = **3.41**
- Case 3: kappa=0.457, 2Delta^2=1.125. Ratio 2Delta^2/kappa = **2.46**

**For ALL tested values, kappa < 2Delta^2.** This means the KL/Chernoff exponent is SMALLER than the Hoeffding exponent, giving a SLOWER error decay rate. The statement in Section 2.3 is backwards.

**What the text correctly means**: For a FIXED threshold theta, KL(theta||p) >= 2(theta-p)^2 by Pinsker. But this is NOT the comparison between kappa (the Chernoff information, which involves the optimal threshold theta*) and 2Delta^2 (which involves p1-p0). The correct statement is: "The Chernoff information kappa is typically smaller than 2(p1-p0)^2, especially for well-separated distributions. This means the CHERNOFF LOWER BOUND on the optimal error rate is smaller (weaker) than the Hoeffding-based bound."

### 2.2 No implicit reliance on kappa >= 2Delta^2

After careful audit: **no lemma implicitly relies on kappa >= 2Delta^2**. Lemma C explicitly corrects this misconception (Proposition C.4). The old Theorem 4 v2 uses 2Delta^2 as its rate, which is a coarser bound superseded by Theorem 4'. The confusion is limited to the architecture document's Section 2.3 prose.

### 2.3 Hidden confusion about rates

The architecture document's Section 0 claims:
```
"上下界的指数匹配了"
```
(the upper and lower bound rates match.)
This is about the OLD bounds (both at 2Delta^2 rate). The NEW result uses kappa. But for kappa < 2Delta^2, the new SCX rate is SLOWER than the old claimed optimal rate. This means either:
- The old lower bound (2Delta^2) was too optimistic (wrong), OR
- The kappa rate is different from what Theorem 4' claims

This needs explicit clarification.

**Suggested fix**: 
1. Rewrite Section 2.3 to correctly state: "The Chernoff information kappa = KL(theta*||p0) is the exact error exponent for the optimal test, and it is typically smaller than 2Delta^2."
2. Clarify the relationship between the old 2Delta^2 bound and the new kappa bound.

---

## 3. Check 3: O(1/M) Term Consistency -- FAIL

### 3.1 Lemma D does not propagate the O(1/M) shift correctly

Lemma D.2 correctly shows:
```
theta_opt = theta* + (1/(M D)) * log((1-eta)/eta) + O(1/M^2)
```

When this is plugged into the FPR/FNR expansions:
```
M*KL(theta_opt||p0) = M*kappa + (lam0*/D)*log((1-eta)/eta) + O(1/M)
```

The second term is **O(1)**, not O(1/M). It produces a constant multiplicative factor ((1-eta)/eta)^{-lam0*/D} in the FPR/FNR expressions.

**Lemma D Section D.5** incorrectly states:
```
"From Lemma D.2, theta_opt = theta* + O(1/M). Thus KL(theta_opt||p0) = kappa + O(1/M)."
```

This is **technically correct** (the KL value shifts by O(1/M)), but **critically misleading**: the O(1/M) shift in KL becomes O(1) when multiplied by M, which is what appears in the exponent. The text should say: "Thus M*KL(theta_opt||p0) = M*kappa + O(1)."

### 3.2 The constant factor from the O(1/M) shift is lost

Section D.5 then plugs theta_opt into the SCX expression and obtains the SAME constant as at theta* (Theorem D.7). This is **wrong** because the O(1) correction to the exponent produces an O(1) change in the prefactor.

**Our numerical verification** shows: the correct adaptive SCX constant equals Lemma E's lower bound (4.591 for Case 1), while Lemma D's Theorem D.7 gives 7.819 for Case 1. The adaptive threshold does achieve optimality, but Lemma D's proof does not correctly derive this.

### 3.3 Self-contradictory derivation in Lemma D Section D.4

Section D.4 contains a confused derivation with a "Wait — this gives a constant 1/2, not 1" self-correction moment. The derivation wanders through several re-derivations, and the final Lemma D.4' is declared but never cleanly proven. The analysis in Section D.4 shows that the ratio of FNR to FPR terms tends to lam0*/|lam1*| (not 1), then later claims it tends to 1. Both cannot be correct.

**Suggested fix**:
1. Delete Section D.4's confused derivations and replace with a clean proof.
2. Section D.5 must correctly account for the O(1) exponential shift from the O(1/M) threshold adjustment.
3. Theorem D.7 must be corrected to match Lemma E's constant.

---

## 4. Check 4: Hidden Assumptions -- PASS (with caveats)

### 4.1 eta bounded away from 0 or 1
- Lemma B Section B.6.1 explicitly analyzes the validity regime and provides a threshold eta_min(M).
- For eta << eta_min, the expansion breaks down but the document acknowledges this.
- PASS: assumption is stated, not hidden.

### 4.2 p0 < p1 strictly
- Lemma E: "0 <= p0 < p1 <= 1" and "(p0,p1) != (0,1)."
- Edge cases p0=0 and p1=1 are discussed as degenerate.
- PASS: explicit.

### 4.3 Reduction to hypothesis testing in Lemma E
- Lemma E Part 1 states: "Assumption (A5) guarantees that the expert errors are conditionally i.i.d. given the state."
- The reduction assumes the algorithm's decision is a measurable function of the error counts (e_1,...,e_M). This is valid under A1-A2 (expert independence), though A1-A6 are not restated in the lemma files.
- The risk definition 1-F1 ≈ w0*alpha + w1*beta holds up to the F1 expansion error, which is O(e^{-2Mk}) as shown in Lemma B.
- PASS: assumptions are adequately stated.

### 4.4 i.i.d. assumption on expert errors
- The i.i.d. assumption within each state (conditional on H0/H1) is explicitly stated and defended.
- Lemma A's non-i.i.d. extension (Section A.6) addresses the case where this is relaxed.
- PASS: explicit.

### 4.5 Lemma F's linearity of F1
- Lemma F states: F1_global(M) = sum_s rho_s * F1_s(M).
- This holds by the law of total expectation: the EXPECTED F1 over the mixture equals the weighted average of conditional expected F1s. F1 is nonlinear per-sample, but its expectation over the mixture IS linear in the conditional expectations.
- **Caveat**: This requires that the F1 score is computed independently per state. If the algorithm's performance in one state affects the confusion matrix in another (e.g., through a shared threshold), the decomposition fails. Lemma F does not discuss this possibility.
- PASS with caveat: the decomposition holds under the assumption of independent per-state decisions.

---

## 5. Check 5: Numerical Consistency -- FAIL (Critical)

### 5.1 C_min/C_SCX verification

For all three parameter sets, the following was verified programmatically:

| Set | p0 | p1 | eta | Lemma E C_min | Lemma B C_SCX (at theta*) | Ratio C_SCX/C_min |
|-----|-----|-----|-----|---------------|--------------------------|-------------------|
| 1 | 0.10 | 0.60 | 0.10 | 0.4591 | 7.819 | 1.70 |
| 2 | 0.20 | 0.50 | 0.30 | 1.3768 | 5.011 | 1.09 |
| 3 | 0.05 | 0.80 | 0.05 | 0.1843 | 8.889 | 2.41 |

**C_SCX/C_min > 1** for all cases, confirming that SCX at theta* is NOT constant-optimal. The adaptive threshold test (Lemma D with theta_opt) does achieve C_min (verified numerically to machine precision).

### 5.2 The architecture document's C_min formulas are wrong

All three C_min formulas from the architecture document (Section 4.3 and Theorem 4') give values that are **15-18x smaller** than Lemma E's correct C_min. This is because they use different functional forms that do not match the Bayes test derivation.

### 5.3 F1 bounds are in [0,1]

For all numerical tests, the computed asymptotic constants produce 1-F1 in (0,1) for sufficiently large M. PASS on this sub-check.

---

## 6. Check 6: Edge Cases -- PASS

### 6.1 eta -> 0
- C_min -> 0 as eta -> 0 (since C_min proportional to eta^{1-s}).
- C_min/eta -> infinity as eta -> 0 (since proportional to eta^{-s}).
- This means the lower bound becomes vacuous for extremely rare noise. The constant diverges but this is a feature (the problem changes character). Lemma D.6 explicitly discusses this regime.
- PASS: handled.

### 6.2 p0 -> 0
- lam0* -> infinity, 1/lam0* -> 0, and kappa -> infinity.
- The problem becomes trivial (any error reveals noise).
- Lemma E discusses this as a degenerate case.
- PASS: handled.

### 6.3 p1 -> 1
- Symmetric to p0 -> 0.
- PASS: handled.

### 6.4 M -> infinity
- All expansions are valid for M -> infinity with fixed theta, p0, p1, eta.
- The F1 expansion remainder is O(e^{-2Mk}/M), which decays faster than the leading term e^{-Mk}/sqrt{M}.
- The threshold shift delta = O(1/M) -> 0.
- PASS: all asymptotics commute correctly at the leading order.

---

## 7. Additional Issues Found

### 7.1 Lemma D Section D.4 is mathematically incoherent

The derivation in Section D.4 contains:
- A "Wait — this gives a constant 1/2, not 1" self-contradiction
- An unresolved factor of 2 discrepancy
- An incorrect claim that the ratio of FNR to FPR terms tends to 1
- Multiple incomplete re-derivations

This section should be entirely rewritten.

### 7.2 Lemma A's lattice correction factor

Lemma A (Section A.4.2) derives the lattice correction factor lambda*/(1-e^{-lambda*}) but then the summary table (Section A.7) omits it. The summary table gives the simpler 1/lambda* form. This is acceptable if the correction is tracked through the constant, but the parent document does not discuss whether this correction appears in the F1 constant.

### 7.3 Theorem 4'(a) normalization

Theorem 4'(a) writes:
```
lim e^{Mk} * sqrt(2pi M) * (1-F1_SCX) = C_min/eta
```
But Lemma E's derivation gives:
```
lim e^{Mk} * sqrt(2pi M) * (1-F1) = K
```
where K does NOT have the eta factor in the same way. The relationship between Theorem 4'(a) and Lemma E needs to be checked for consistent normalization.

---

## 8. Summary of Required Fixes

| Priority | Location | Issue | Fix |
|----------|----------|-------|-----|
| **P0** | All files | C_min defined three ways | Canonicalize to Lemma E's expression; remove others |
| **P0** | Lemma D Theorem D.7 | Wrong constant (uses theta* not theta_opt) | Replace RHS with Lemma E's constant |
| **P0** | Lemma D Section D.5 | O(1/M) shift not propagated to constant | Correctly account for M*KL shift producing O(1) prefactor |
| **P1** | Architecture Sec 2.3 | Claims KL beats Hoeffding; actually kappa < 2Delta^2 | Rewrite to clarify exact vs bound comparison |
| **P1** | Lemma D Section D.4 | Self-contradictory derivations | Rewrite cleanly |
| **P2** | Architecture Theorem 4' | C_min formula wrong and mismatch with Lemma E | Fix to match Lemma E |
| **P2** | Architecture Sec 4.3 | Ad-hoc C_min formula | Remove or replace with Lemma E's derivation |
| **P2** | Lemma F | F1 linearity caveat unstated | Add note about independent per-state decisions |

---

## 9. Verdict

**The proof chain is NOT ready for journal submission.** The critical issue (P0) is the three-way inconsistency of C_min and the fact that Lemma D claims to achieve the optimal constant via the wrong formula. While the mathematical substance is salvageable (the adaptive threshold test does achieve C_min, as we confirmed numerically), the manuscript as written contains false claims and inconsistent derivations that would be flagged by any competent reviewer.

Estimated rework time: 2-3 days to rewrite affected sections, re-derive constants, and verify consistency across all files.

---

*Report generated by adversarial review agent.*
