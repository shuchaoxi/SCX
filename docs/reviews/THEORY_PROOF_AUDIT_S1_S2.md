# Rigorous Proof Audit: S1 (Theorem 1) + S2 (Theorem 2)

**Date:** 2026-07-02  
**Files audited:**
- `S1_thm1_noise_detection.tex` (682 lines) — Noise Detection Guarantee
- `S2_thm2_weak_features.tex` (659 lines) — Weak Feature Failure Boundary

**Method:** Every step in every proof was traced algebraically. Hoeffding, Pinsker, Chernoff, and Fano applications were verified against the standard forms. All inequalities were checked for direction, sign, and factor correctness. Hidden assumptions were identified and flagged.

---

## Verdict Summary

| Category | Count | Severity |
|----------|-------|----------|
| **Blocking errors** (proof invalid as stated) | 2 | 🔴 Critical |
| **Mathematical gaps** (insufficient justification) | 3 | 🟠 Major |
| **Implicit assumptions** (not stated but needed) | 2 | 🟡 Moderate |
| **Sloppy derivations** (correctable but imprecise) | 4 | 🟢 Minor |
| **Algebraic/logical steps verified correct** | Most | ✅ |

---

## S1 — Theorem 1: Noise Detection Guarantee

### 🔴 CRITICAL ISSUE 1: Proof assumes 0-1 loss despite general bounded-loss setup

**Location:** Lemma 1 proof, lines 164–199; Lemma 3 proof, lines 255–299; implicitly everywhere in Theorem 1.

**The problem:**

The theorem setup (line 47) defines a general bounded loss `ℓ : Y × Y → [0, B]` with threshold `τ > 0`. The error indicator is `e_m = 1{ℓ(f_m(x), y) > τ}`. The setup also mentions both classification and regression (lines 21–24).

However, the proofs of Lemma 1 (noise side) and Lemma 3 immediately convert this to class-level reasoning:

- Lemma 1, line 170: `P(ℓ(f_m(x), y) > τ | noise, x) = P(f_m(x) ≠ y | noise, x) (for 0-1 loss)`
- Lemma 3, line 258: `e_m = 1{f_m(x) ≠ c}`

This equivalence **only holds for 0-1 classification loss with τ ∈ (0, 1)**. For:
- Cross-entropy loss: ℓ > τ does NOT mean class mismatch
- MSE regression: no concept of "class" at all; `K_Y` is undefined
- Any non-0-1 loss: `ℓ(f_m(x), y) > τ` and `f_m(x) ≠ y` are different events

This means:
1. **The entire Theorem 1 only applies to classification with 0-1 loss**, despite the setup claiming generality.
2. **The mention of regression (line 23) is misleading** — the theorem's machinery (K_Y = number of classes, uniform-over-classes noise) doesn't extend to regression.
3. Every subsequent result (Lemma 1 noise mean, Lemma 3 TPR bound, Theorem 1 F1 bound, all corollaries) inherits this restriction.

**Fix required:** Either (a) restrict the theorem statement to classification with 0-1 loss, or (b) generalize the proof to handle arbitrary bounded losses by working with `P(ℓ(f_m(x), c) > τ)` directly rather than `P(f_m(x) = c)`.

---

### 🔴 CRITICAL ISSUE 2: Chernoff-form F1 bound has swapped terms and wrong coefficients

**Location:** Lines 519–528, equation `\eqref{eq:f1-bound-chernoff}`.

**The formula in the text:**

```
F1 ≥ 1 - (1/η) Σ ρ_s [ exp(-M·KL(θ || μ_s)) 
                       + ((1-η)/η) exp(-M·KL(θ || 1 - C_bal·μ_s/(K_Y-1))) ]
```

Expanding:
```
F1 ≥ 1 - (1/η) Σ ρ_s exp(-M·KL(θ || μ_s))
        - (1-η)/η² Σ ρ_s exp(-M·KL(θ || 1 - C_bal·μ_s/(K_Y-1)))
```

**The correct derivation:**

Following the same F1 lower-bound algebra as in the Hoeffding proof (lines 392–418):

- Let `α_s = exp(-M·KL(θ || 1 - C_bal·μ_s/(K_Y-1)))` — bounds FN probability for noise samples (from the Chernoff counterpart of Lemma 3)
- Let `β_s = exp(-M·KL(θ || μ_s))` — bounds FP probability for clean samples (from the Chernoff counterpart of Lemma 2)

Then:
- TPR ≥ 1 − Σ ρ_s α_s = 1 − δ₁
- FPR ≤ Σ ρ_s β_s = δ₂

```
F1 ≥ 2η(1−δ₁) / [η(2−δ₁) + (1−η)δ₂]
   ≥ 1 − δ₁ − ((1−η)/η) δ₂
   = 1 − Σ ρ_s α_s − ((1−η)/η) Σ ρ_s β_s
```

**Correct Chernoff F1 formula:**

```
F1 ≥ 1 − Σ_s ρ_s · exp(−M·KL(θ || 1 − C_bal·μ_s/(K_Y−1)))
        − ((1−η)/η) Σ_s ρ_s · exp(−M·KL(θ || μ_s))
```

**What's wrong in the text:**
1. The two KL terms are swapped (clean-side vs. noise-side).
2. Both terms are multiplied by an erroneous `(1/η)` outer factor instead of the noise-side term getting coefficient 1 and the clean-side term getting `(1−η)/η`.
3. The inner `(1−η)/η` factor is on the wrong term and squared by the outer factor.

**Note:** The Hoeffding-form F1 bound (lines 332–346) is algebraically correct. The error is only in the Chernoff variant.

---

## S2 — Theorem 2: Weak Feature Failure Boundary

### 🟠 MAJOR GAP 1: PR-AUC bound transfer is not rigorously justified

**Location:** Lines 401–406 of the proof, Step 5 (PR-AUC).

**What the text says:**

> "The same amplification argument applies at each threshold, yielding the identical bound `\eqref{eq:prauc-bound}`. (A fully rigorous treatment requires additional steps to handle the integral over thresholds, but the bound at the level of the joint distribution is valid.)"

**The problem:**

The AUC bound works because AUC has the representation:
```
AUC = P(score_noise > score_clean)
```
which involves two independent samples from the two conditional distributions. The product-measure TV decomposition then gives:
```
TV(P(·|Z=1)×P(·|Z=0), P̃(·|Z=1)×P̃(·|Z=0)) ≤ TV(P(·|Z=1), P̃(·|Z=1)) + TV(P(·|Z=0), P̃(·|Z=0))
```

PR-AUC does NOT have this product-measure representation. The PR curve is defined pointwise by (Recall(t), Precision(t)) at each threshold t, and the area under it cannot be expressed as a simple probability over independent samples.

**What would be needed:** Either:
- A bound on the expected difference between precision-recall curves under P and P̃, integrated over thresholds, OR
- A Lipschitz-continuity argument for PR-AUC as a functional of the joint distribution P(score, Z), OR
- An explicit derivation showing that |PRAUC_P − PRAUC_P̃| ≤ sqrt(δ/2)·(1/η + 1/(1−η))

The parenthetical remark "(A fully rigorous treatment requires additional steps…)" acknowledges this gap. As written, **the PR-AUC bound is unproven**. The AUC and F1 bounds are fine, but the PR-AUC claim needs a separate proof or should be removed.

---

### 🟠 MAJOR GAP 2: Claim that Δ_φ ≤ sqrt(δ/2) is unsubstantiated

**Location:** Lines 71–79, equation `\eqref{eq:pinsker-tv}`.

**What the text says:**

> `Δ_φ = max_{s1≠s2} TV(P_{φ|S=s1}, P_{φ|S=s2})`  
> and by Pinsker's inequality, `Δ_φ ≤ sqrt(δ/2)` where δ = I(φ; S).

**The problem:**

Pinsker's inequality states: `TV(P, Q) ≤ sqrt(KL(P||Q) / 2)`.

To bound `Δ_φ`, we would need:
```
max_{s1,s2} KL(P_{φ|s1} || P_{φ|s2}) ≤ δ = I(φ; S)
```

But `I(φ; S) = Σ_s P(s) · KL(P_{φ|s} || P_φ)`, where `P_φ = Σ_s P(s) P_{φ|s}` is the **mixture**, not another conditional. The pairwise KL divergence can be arbitrarily larger than I(φ; S). For example, if `P(s1) = ε` and `KL(P_{φ|s1} || P_{φ|s2}) = D`, then `I(φ; S) = ε·D + O(ε)`, which can be much smaller than D.

**In the binary case:** If both states have equal probability 1/2, then:
```
KL(P1 || P2) = KL(P1 || P) + KL(P || P2) + additional cross terms
```
This doesn't give `KL(P1 || P2) ≤ 2·I(φ; S)` either. In general, `KL(P1 || P2)` can be much larger than `I(φ; S)`.

The only safe bound is:
```
TV(P1, P2) ≤ TV(P1, P) + TV(P2, P) ≤ sqrt(KL(P1||P)/2) + sqrt(KL(P2||P)/2)
```
From this we get `Δ_φ ≤ sqrt(2I(φ; S)/P_min)` where P_min = min_s P(s), which is an entirely different scaling: `O(sqrt(δ/P_min))` rather than `O(sqrt(δ))`.

**Impact:** Fortunately, the proof of Theorem 2 does NOT use this claim. The proof uses Pinsker on the joint distribution `TV(P, P̃) ≤ sqrt(δ/2)` (Step 2, line 330–332), which is correct. The `Δ_φ` claim is a standalone definitional statement. It should either be removed or corrected to note the dependence on state probabilities.

---

### 🟠 MAJOR GAP 3: "Loss-uninformative noise" claim in Corollary 2 is false in general

**Location:** Lines 507–514 (Corollary 2: Loss-Uninformative Noise).

**What the text says:**

> Under uniform label noise, the loss distribution is independent of the noise indicator:
> `P(ℓ | Z=1) = P(ℓ | Z=0)`
> The loss baseline then reduces to the random baseline.

**The problem:**

Under the noise model of Theorem 1 (uniform label noise: `y ~ Uniform(Y\{y*})` with probability η), the loss distribution is NOT generally independent of Z. Consider:
- Expert predicts correctly (f_m(x) = y*). On a clean sample, loss is low. On a noisy sample, the label is flipped to some c ≠ y*, and the loss becomes high.
- Expert predicts incorrectly (f_m(x) = c ≠ y*). On a clean sample, loss is high. On a noisy sample, the label might coincidentally flip to c, making the loss low.

The loss distribution shifts under noise. The claim `P(ℓ | Z=1) = P(ℓ | Z=0)` is an **additional, unstated assumption** that does not follow from "uniform label noise" alone. It would require:
- The experts to be random guessers (f_m(x) uniformly random over Y), OR
- A specific degeneracy where the loss function and noise interact to cancel out.

**Impact:** Corollary 2's conclusions (AUC ≤ 0.5 + …, PR-AUC ≤ η + …, F1 ≤ 2η/(1+η) + …) are stated as consequences of the theorem, but the premise about the loss baseline being random is undefended. The bounds themselves (as upper bounds from Theorem 2) remain valid; the claim that AUC_base = 0.5 for uniform noise is the problematic part.

**Fix:** Either remove the claim that `P(ℓ|Z=1) = P(ℓ|Z=0)` under uniform noise, or explicitly add the necessary assumption (e.g., "if the experts are random guessers, then under uniform label noise…").

---

## Moderate Issues

### 🟡 IMPLICIT ASSUMPTION 1: Theorem 1 is classification-only (uses K_Y)

**Location:** Setup (lines 21–24) mentions regression, all proofs use class count K_Y.

The noise model `y ~ Uniform(Y \ {y*})` and the use of `K_Y = |Y|` throughout every proof mean the theorem is fundamentally a **classification result**. The mention of regression in the setup should be removed to avoid misleading readers. The theorem does not and cannot apply to regression with Y ⊆ R^d.

### 🟡 IMPLICIT ASSUMPTION 2: Lemma 3's conditioning on noise label c

**Location:** Lemma 3, lines 256–260.

The proof conditions on a specific noise label `c ≠ y*` and asserts that the e_m are conditionally independent given (x, c). This uses A1 (disjoint training sets) and the fact that noise label is independent of D_m (A4). This is correct, but the step from conditioning on (x, c) to applying Hoeffding could be made more explicit. The current text is clear enough but assumes the reader fills in this chain of independence.

---

## Minor Issues (Sloppiness)

### 🟢 Minor 1: Factor of 2 in Lemma 2 (S2) expected difference bound

**Location:** S2, Lemma 2, line 213.

The bound `E[|C(Ŝ) − C(S)| | Ŝ≠S] ≤ 2` uses 2 instead of 1. Since C ∈ [0,1], the maximum absolute difference is 1. Using 2 is still a valid upper bound but looser than necessary. The final result `2·P(Ŝ≠S) + O(1/√n_min)` is slightly weaker than the achievable `P(Ŝ≠S) + O(1/√n_min)`.

### 🟢 Minor 2: Lipschitz constant for F1 is loosely analyzed

**Location:** S2, lines 420–437.

The claimed Lipschitz constants (`C_F ≤ 3` for precision/recall ≥ 0.1, `C_F ≤ 2` for ≥ 0.5, `C_F ≤ 1` for typical) are not derived from the gradient expressions. Actual computation:

|∂F1/∂TP| = 2(FP+FN)/D², where D = 2TP+FP+FN.

For precision=recall=0.1, η=0.1: TP=0.01, FP=0.09, FN=0.09, D=0.20 → |∂F1/∂TP| = 2·0.18/0.04 = **9**.

For precision=recall=0.1, η=0.3: TP=0.03, FP=0.27, FN=0.27, D=0.60 → |∂F1/∂TP| = 2·0.54/0.36 = **3**.

The constant depends heavily on η and the operating point. The claimed values are optimistic for small η. The approach (Lipschitz continuity) is valid, but the claimed constants should be derived explicitly from the parameters or replaced with a parameterized bound: `C_F(η, ε)`.

### 🟢 Minor 3: Corollary 4 (S1) uses B for indicator range

**Location:** S1, lines 596–611 (Corollary 4: Finite-Sample Correction).

The Hoeffding bound uses range [0, B] for e_m, but e_m = 1{ℓ > τ} ∈ {0, 1}, not [0, B]. The correct range is [0, 1]. If B ≥ 1 (typical), using B is conservative but looser than needed. If B < 1 (e.g., normalized loss to [0, 0.5]), the bound would be anti-conservative. Should use 1, not B.

### 🟢 Minor 4: Two "equivalent" F1 formulas are identical

**Location:** S1, lines 332–346.

The "boxed" formula (line 336) and the "or equivalently" formula (line 344) are algebraically identical after simplification:
```
1 − Σ ρ_s [exp(−2MΔ_s^2) + ((1−η)/η) exp(−2MΔ_s^2)]
= 1 − Σ ρ_s exp(−2MΔ_s^2) · (1 + (1−η)/η)
= 1 − (1/η) Σ ρ_s exp(−2MΔ_s^2)
```
Both terms inside the brackets are identical (`exp(−2MΔ_s^2)`), which defeats the purpose of showing two forms. This arises because both δ₁ and δ₂ are bounded by the same Δ_s-based exponential. The second formula should either be removed or show the pre-simplification form with distinct δ₁ and δ₂ terms.

---

## Items Verified Correct ✅

The following were checked step by step and found to be mathematically sound:

1. **Hoeffding application in Lemma 2:** Valid. The bound with θ − μ_s (instead of θ − E[C]) is conservative since E[C] ≤ μ_s ⇒ θ − E[C] ≥ θ − μ_s ⇒ exp bound is looser. Correct direction.

2. **Hoeffding application in Lemma 3:** Valid. Same conservative principle.

3. **F1 lower-bound algebra (Hoeffding form):** Fully verified. The chain:
   ```
   F1 ≥ 2η(1−δ₁)/(η(2−δ₁)+(1−η)δ₂) ≥ 1 − δ₁ − ((1−η)/η)δ₂
   ```
   is correct. The simplification to `1 − (1/η) Σ ρ_s exp(−2MΔ_s^2)` is correct.

4. **Lemma 1 mean separation:** Clean side = direct from A5. Noise side derivation is valid under 0-1 loss. Separation condition `μ_s < (K_Y−1)/K_Y` correctly derived. Optimal threshold and maximized gap formulas verified algebraically.

5. **Pinsker on joint distribution (S2, Step 2):** `KL(P || P̃) = I(φ; S)` — standard identity. `TV(P, P̃) ≤ sqrt(KL(P||P̃)/2)` — correct Pinsker application.

6. **Data processing inequality for TV (S2, Step 3):** `TV(P_pred, P̃_pred) ≤ TV(P, P̃)` — correct, since the prediction is a deterministic function.

7. **Fano's inequality (S2, Lemma 1):** Standard form correctly applied. Corollaries for uniform states and K_S=2 are correct.

8. **AUC bound transfer (S2, Step 5):** Correct derivation through product-measure TV decomposition and conditional probability amplification.

9. **Corollary 3 (S2):** Minimum information thresholds `δ_min ≥ 2(Δ/C_F)²` and `δ_min ≥ 2(Δ_AUC·η(1−η))²` correctly derived from the main bounds.

10. **Symmetric lower bound remark (S2):** Correct. TV symmetry gives `AUC_P ≥ AUC_base − sqrt(δ/2)·(1/η + 1/(1−η))`.

11. **Expert dilution formula (S1, Remark):** `M_eff = M/(1 + (M−1)ρ̄)` — standard GEE/Liang-Zeger variance inflation factor. Correctly referenced.

12. **Corollary 1 and 2 algebraic derivations (S1):** All verified.

---

## Recommendations

### Must-fix (before any submission):
1. Restrict Theorem 1 to 0-1 classification loss, or generalize the proof. Remove regression mention.
2. Fix the Chernoff F1 bound formula (lines 519–528).

### Strongly recommended:
3. Either prove the PR-AUC bound properly or remove the PR-AUC claim from Theorem 2.
4. Remove or fix the Δ_φ ≤ sqrt(δ/2) claim (line 77), or note its dependence on state probabilities.
5. Fix Corollary 2's claim about loss-uninformative noise, or add explicit assumptions.

### Nice-to-have:
6. Tighten the factor 2 in Lemma 2 (S2) to 1.
7. Compute actual Lipschitz constants for F1 rather than claiming fixed values.
8. Fix Corollary 4 (S1) to use range [0,1] instead of [0,B] for e_m.
9. Clean up the redundant "or equivalently" F1 formula in Theorem 1.
