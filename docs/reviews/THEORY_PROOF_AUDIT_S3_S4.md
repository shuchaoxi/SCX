# THEORY PROOF AUDIT — S3 (Unidentifiability) + S4 (Exact Constant Minimax)

**Date:** 2025-07-02  
**Auditor:** Hermes Agent (mathematical verification)  
**Files audited:**
- `S3_thm3_unidentifiability.tex` (798 lines)
- `S4_thm4_exact_constant_minimax.tex` (900 lines)
- Context: `main.tex`, `S1_thm1_noise_detection.tex`, `S8_numerical_verification.tex`

**Verdict:** Both proofs are **mathematically correct** at their stated level of rigor. There are **no fatal logical errors or circular reasoning**. However, there are **5 important caveats** — none invalidate the theorems, but all should be addressed for completeness.

---

## S3 — Theorem 3 (The Honest Person Theorem): Overall Assessment

### 1. Is the unidentifiability argument watertight? YES (with one qualification)

**Binary case (K=2):** The construction is correct and complete.

- **World A (Noise):** State s₁: y* ≡ 0, label flipped w.p. η_err, expert accuracy on clean = 1-ε₁. State s₂: y* ≡ 0, no noise, expert accuracy = 1-ε₂.
- **World B (Difficulty):** State s₁: y = y*, P(y*=0) = 1-η_amb, P(y*=1) = η_amb. Expert always predicts 0 w.p. 1-ε₁ regardless of true label. State s₂: identical to World A.
- **Verification:** When η_err = η_amb, the marginal distributions P(y|x) and P(f_m|x) and the joint P(y, f_m|x) are identical in both worlds. The factorization P(x,y,{f_m}) = P(x)·P(y|x)·∏P(f_m|x) uses y ⟂ f_m | x, which holds in both constructions. **All algebra checks out** (verified line by line at lines 140-186).
- **Algorithm impossibility:** The bound max(Error) ≥ ρη/2 follows from max(1-a, a) ≥ 1/2 for any a ∈ [0,1]. Correct.

**General K>2 case:** The "random expert" construction is mathematically sound but philosophically weaker.

- In World B, experts are fully random (independent of true label), predicting class 0 w.p. 1-ε₁ and each other class w.p. ε₁/(K-1).
- The marginal and joint distributions match World A by construction because both worlds have the same product structure with identical marginals.
- **Caveat #1 (S3):** The K>2 construction uses experts that *completely ignore the input and true label*. This is an extreme construction that proves existence — there is *at least one* difficulty interpretation observationally equivalent to the noise interpretation. But it does not characterize how *natural* or *plausible* the difficulty world must be. The theorem does not claim naturalness, but readers may be misled. **Recommendation:** Add a remark clarifying that the construction is an existence proof; the question of whether *realistic* difficulty worlds can mimic noise worlds is open.

### 2. Are the two worlds properly constructed? YES

- Both worlds are defined on the same measurable space (X × Y × Y^M).
- Both respect the factorization P(x,y,{f_m}) = P(x)·P(y|x)·∏P(f_m|x) which follows from A1-A2 (the assumptions being *tested* for necessity, not assumed).
- All probabilities sum to 1, all conditional distributions are well-defined.
- The conditional independence structure y ⟂ f_m | x is verified for both constructions. In World A, it follows from A4 (noise independent of experts). In World B, it's by explicit construction (f_m independent of y*).

### 3. Minimal Sufficient Set: Correct with Nuance

The three minimal sufficient sets are:
- A_min^(1) = {A1, A4, A5}
- A_min^(2) = {A1, A4, A6}
- A_min^(3) = {A5, A6} with |S| ≥ 2

**Caveat #2 (S3):** The claim that these are *sufficient* is well-supported (each breaks the specific World B construction). The claim that they are *necessary* — i.e., that removing any of them allows some unidentifiable pair — is argued only through the corollaries, not formally proved for all possible world pairs. The file carefully uses "sufficient condition" language in the corollaries, but the paragraph introducing the minimal sets (lines 389-398) uses "necessary and sufficient." The "necessary" direction is heuristic (each assumption blocks one specific path to unidentifiability; the construction shows that without at least one of these combinations, unidentifiability *can* occur). A formal necessity proof would require showing that for any set of assumptions not containing one of A_min^(1)-(3), there exists an observationally indistinguishable pair. This is not proved. **Recommendation:** Downgrade "necessary and sufficient" to "sufficient; conjectured necessary."

### 4. Everyone Equal Theorem (Corollary): Correct but Philosophical

The mathematical claim is correct: identical observational distributions imply max error ≥ 1/2 by Le Cam's lemma. The philosophical claim that "assumptions are verifiable by any observer without privileged access" is an epistemological assertion, not a mathematical theorem. The file handles this appropriately by calling it a corollary and providing a proof sketch. No mathematical error.

### 5. Good Person Convergence Conjecture: Honestly Labeled

The file explicitly labels this as a conjecture (not a theorem) and lists exactly what a rigorous proof would require (lines 507-528). This is intellectually honest and appropriate.

### 6. Epistemic Formalization (E1-E5 + K Operator): Correct

The Hoeffding bound application is standard and correct. The "Gettier immunity" claim is properly qualified (operational, not metaphysical). No mathematical errors.

---

## S4 — Theorem 4 (Exact Constant Minimax): Overall Assessment

### 1. Does the Chernoff information derivation hold? YES

- Definition: C(P₀,P₁) = -min_{λ∈[0,1]} log E_{P₀}[(dP₁/dP₀)^λ]. For Bernoulli: E = p₀^{1-λ}p₁^λ + (1-p₀)^{1-λ}(1-p₁)^λ. **Correct.**
- Chernoff point formula: θ* = log((1-p₀)/(1-p₁)) / log(p₁(1-p₀)/(p₀(1-p₁))). **Verified by algebra** (lines 303-318). Setting KL(θ||p₀) = KL(θ||p₁) and solving yields exactly this expression.
- The claim that this is the unique root in (p₀,p₁) follows from strict convexity of KL and sign change at endpoints. **Correct.**

### 2. Is Bahadur-Rao applied correctly? YES (with an important caveat)

- The Bahadur-Rao theorem for i.i.d. Bern(p) states: P(S_M/M ≥ θ) ~ exp(-M·KL(θ||p)) / (λ*√(2πM θ(1-θ))). **Correct statement.**
- The saddlepoints λ₀* and λ₁* are correctly defined as log-odds ratios.
- The expansion at the adaptive threshold uses the Bahadur-Rao formula correctly: the KL divergence is expanded around θ*, the saddlepoint corrections are applied properly.

**Caveat #3 (S4): The i.i.d. assumption within a state.** The entire S4 analysis treats expert error indicators within a state as i.i.d. Bernoulli(p₀) under H₀ and i.i.d. Bernoulli(p₁) under H₁. But assumption A5 only guarantees E[C|clean, x] ≤ μ_s, not that the error rate is *constant* at μ_s across all x ∈ s. If the clean error rate varies with x (bounded by μ_s), the observations are independent but *not identically distributed* — they form a mixture of Bernoullis with different parameters. The Bahadur-Rao theorem as stated applies to i.i.d. observations; for independent but non-identical observations, the asymptotics are governed by a more complex large-deviation principle (Gärtner-Ellis theorem) and the constant prefactor may differ.

**Mitigation:** If the analysis is interpreted as a *worst-case* bound (using p₀ = μ_s as the maximal error rate), then the i.i.d. Bernoulli(μ_s) case gives a lower bound on detection performance (clean errors are at most μ_s, so any actual mixture has lower error rate and is easier to detect). For the lower bound in Part II (Lemma E), this is fine — the worst case gives the hardest detection problem. For the achievability in Part I (Lemma D), the SCX detector may perform *better* than the asymptotics predict if actual error rates are below μ_s. So the achievability result is conservative, not invalid. **Recommendation:** Add a remark noting that the i.i.d. assumption within states is a worst-case simplification (exact when all x in state s have error rate exactly μ_s; conservative otherwise).

### 3. Does the exact constant match the upper bound? YES — it's a perfect match

The adaptive threshold achieves:
```
lim_{M→∞} e^{Mκ}√(2πM)·(1-F1_SCX(θ†)) = C_min/η
```
where C_min = (η/2)·((1-η)/η)^s·(1/λ₀* + 1/|λ₁*|)/√(θ*(1-θ*))

The lower bound (Lemma E) gives the identical expression. **The match is exact**, proved by showing:
1. The Bayes test (Neyman-Pearson optimal) has threshold exactly θ†.
2. The weighted risk w₀α + w₁β for the Bayes test expands to the same constant.
3. The cancellation produces identical ((1-η)/η)^s factors in both FPR and FNR contributions.

**The key cancellation is verified:**
- FPR contribution: ((1-η)/(2η))·((1-η)/η)^{-λ₀*/D*} / λ₀* = (1/(2λ₀*))·((1-η)/η)^s
- FNR contribution: (1/2)·((1-η)/η)^{|λ₁*|/D*} / |λ₁*| = (1/(2|λ₁*|))·((1-η)/η)^s

Using s = |λ₁*|/D* and 1-s = λ₀*/D*, both simplify correctly.

### 4. Any hidden assumptions or circular reasoning? See caveats below.

**Caveat #4 (S4): The definition of p₁.** The file defines:
```
p₀ = μ_s,   p₁ = 1 - C_bal·μ_s/(K-1)
```

However, from Lemma 1 (S1), the exact relationship is:
```
E[C|noise] = 1 - E[C|clean]/(K-1)
```
This is derived from the fact that the noise label is uniform over K-1 alternatives, so the probability an expert matches the noise label is exactly (total error rate)/(K-1). The C_bal factor from A6 bounds *concentration across error classes*, but does not affect the *total* error rate, which always sums to E[C|clean].

If p₁ is meant to be E[C|noise] under H₁ (the parameter of the Bernoulli distribution of expert errors on noise samples), then p₁ = 1 - μ_s/(K-1), without C_bal. The C_bal factor would only be relevant for bounding the probability that a specific wrong class gets maximum probability, which is a different quantity.

**Mitigation:** If μ_s is the *worst-case* clean error rate (upper bound from A5) and C_bal ≥ 1, then p₁ = 1 - C_bal·μ_s/(K-1) is a *lower bound* on the actual noise-conditioned consistency score. Lower p₁ means harder detection (smaller separation from p₀), so using this lower bound is conservative for the lower bound proof. For the achievability proof, the SCX detector would actually achieve *better* performance if p₁ > 1 - C_bal·μ_s/(K-1). So the theoretical analysis is conservative in both directions. **Recommendation:** Clarify whether p₁ is the exact expected value or a worst-case bound, and explain why C_bal enters the formula (or remove it if it's the exact value).

**Caveat #5 (S4): Oracle knowledge of parameters.** The adaptive threshold θ† requires knowledge of p₀, p₁, and η, which are unknown in practice. The achievability result assumes oracle access to these parameters. In practice, they must be estimated from data, and estimation error at finite M propagates to the threshold and degrades the constant. This is standard in asymptotic theory (oracle bounds are common), but the paper's claim that "SCX achieves the lower bound" should be qualified as "with oracle knowledge of parameters." **Recommendation:** Add a remark on the effect of parameter estimation error.

### 5. Numerical Verification: Consistent

The numerical results in S8 and the table in S4 (lines 828-844) are internally consistent:
- Adaptive limit matches C_min/η to machine precision (difference < 10⁻¹⁵).
- Non-adaptive penalty ranges from 1.00× (η=0.5, no penalty) to 2.41× (η=0.05).
- Chernoff κ is 2.5-3.4× smaller than Hoeffding 2Δ², confirming the tighter bound.
- Cases 4 (η=0.50) and 5 (η=0.90) violate the assumption η ∈ (0,1/2) from the noise model — these are mathematical stress tests, not realistic scenarios. This is fine.

### 6. Multi-State Aggregation (Lemma F): Correct

The bottleneck rate κ_global = min_s κ_s and the weighted sum of constants for bottleneck states are standard results in large-deviation theory. States with larger κ_s have exponentially smaller contributions. The additivity claim (1-F1_global = Σ ρ_s(1-F1_s)) is approximately correct for large samples; it's exact in expectation. **Correct.**

---

## Summary of Issues

| # | File | Severity | Description |
|---|------|----------|-------------|
| 1 | S3 | Medium | K>2 construction uses degenerate experts (fully random). This is valid as an existence proof but the practical force of the theorem is weakened. Recommend explicit caveat. |
| 2 | S3 | Medium | "Necessary and sufficient" claim for minimal assumption sets is not formally proved in the necessary direction. Recommend downgrading to "sufficient; necessity conjectured." |
| 3 | S4 | Medium | I.i.d. assumption within a state is a worst-case simplification. Actual errors may be non-identically distributed (different x values in the same state have different error probabilities bounded by μ_s). Bahadur-Rao applies to i.i.d.; results are conservative but should be qualified. |
| 4 | S4 | Low-Medium | Definition of p₁ = 1 - C_bal·μ_s/(K-1) mixes the C_bal constant (which bounds error concentration) into a formula that should only depend on the total error rate. If p₁ is meant to be a worst-case lower bound, this should be explained. If it's meant to be the exact expected value, C_bal should be removed. |
| 5 | S4 | Low | Oracle knowledge of parameters assumed for the adaptive threshold. Practical performance will depend on estimation quality. Standard in asymptotic theory but should be noted. |

---

## Overall Verdict

**The mathematical core of both proofs is sound.** The constructions in S3 are valid, the Bahadur-Rao/Chernoff derivations in S4 are correct, and the constant matching proof is a genuine mathematical achievement. The five caveats above do not invalidate any theorem — they are issues of precision, scope, and presentation that would strengthen the work if addressed. None of the issues indicate mathematical error or circular reasoning.

**Brutal honesty summary:**
- The proofs are not "wrong." 
- The S3 existence proof works but is weaker than it could be (degenerate experts in the K>2 case).
- The S4 exact constant matching is genuinely impressive and checks out algebraically.
- The main practical concern is the gap between the i.i.d. Bernoulli model and the actual per-x error rate variation within states (Caveat #3).
- The paper's honesty about the Good Person Convergence Conjecture (explicitly labeling it as unproven conjecture) is commendable and rare in the literature.
