# Theory Proof Audit: S5–S8 (Cluster Consistency + Bootstrap Stability + Experiments + Numerical Verification)

**Date**: 2026-07-02
**Auditor**: Automated mathematical verification
**Files audited**:
- `S5_thm5_cluster_consistency.tex` (1159 lines)
- `S6_prop6_bootstrap_stability.tex` (238 lines)
- `S7_experimental_details.tex` (186 lines)
- `S8_numerical_verification.tex` (274 lines)
**Cross-referenced**: `S4_thm4_exact_constant_minimax.tex`, `main.tex`

---

## EXECUTIVE SUMMARY

**Overall verdict: CONDITIONALLY SOUND — with 4 critical gaps, 3 moderate issues, and 3 minor issues.**

The core mathematical architecture is well-structured and the algebraic identities are consistent. However, several proofs rely on unsubstantiated claims, circular arguments, or hand-wavy asymptotics. S6's Proposition 6 is explicitly labelled as non-rigorous in places, which is honest but undermines its utility as a formal result. S8's numerical "verification" reduces to an algebraic identity check without reproducible code.

---

## PART 1: S5 — Theorem 5 (Cluster Consistency) — 1159 lines

### VERDICT: PLAUSIBLE BUT INCOMPLETE

The theorem statement is reasonable for well-separated Gaussian mixtures, but the proof has significant gaps that would need to be filled for a rigorous journal publication.

---

### ❌ CRITICAL GAP 1: Lemma 1, Step 5 — Circular Contraction Argument

**Location**: S5 lines 248–282

**The issue**:
The proof attempts to bound `‖θ* - μ‖_∞` using a contraction property of the self-consistency operator T:

```
‖T(θ) - T(μ)‖_∞ ≤ ½‖θ - μ‖_∞   whenever ‖θ - μ‖_∞ ≤ Δ_min/4
```

Then derives:
```
‖θ* - μ‖_∞ ≤ ½‖θ* - μ‖_∞ + ε_pop   →   ‖θ* - μ‖_∞ ≤ 2ε_pop
```

**The problem**: This argument assumes `θ*` is already in the ball of radius `Δ_min/4` around `μ` to apply the contraction bound. But the contraction bound is precisely what's being used to establish that `θ*` is close to `μ`. The logic is circular: we need `‖θ* - μ‖ < Δ_min/4` to apply the contraction, but we're applying the contraction to prove `‖θ* - μ‖ < Δ_min/4`.

**Severity**: High. Without this step, Lemma 1 only establishes that T(μ) ≈ μ, not that θ* ≈ μ.

**Possible fix**: Use a separate argument (e.g., perturbation analysis of k-means under strong separation) to first establish that any population minimizer must lie within `Δ_min/4` of the true centers. Alternatively, use a fixed-point theorem on a ball of radius `Δ_min/4` centered at μ to show T has a unique fixed point there, and argue that the global minimizer must be inside that ball because the objective outside is provably worse.

---

### ❌ CRITICAL GAP 2: Lemma 1, Step 4 — Unsubstantiated Noise Expectation Bound

**Location**: S5 lines 232–236

**The claim**:
```
‖E[ε | μ_k + ε ∈ V_k(μ)]‖₂ ≤ C₃ σ √(d_φ) · exp(-Δ_min²/(8σ²))
```

**The problem**: This bound on the conditional expectation of a sub-Gaussian vector restricted to a Voronoi cell is asserted without derivation. The argument that "V_k(μ) differs from the full space by an event of exponentially small probability" does not directly imply a bound of this form. One needs to carefully bound `E[ε · 1{ε in a specific set}]` when the set is a Voronoi cell — a convex polytope defined by linear inequalities involving `ε`. The constant `C₃` is never derived or bounded.

**Severity**: High. This directly affects the bound on ε_pop, which propagates through the entire proof chain.

---

### ❌ CRITICAL GAP 3: Lemma 2, Step 1 — Quadratic Lower Bound / Strong Convexity

**Location**: S5 lines 329–342

**The claim**:
```
W(θ) - W(θ*) ≥ λ · ‖θ - θ*‖²,   λ = π_min/2
```

**The problem**: The k-means population objective W(θ) is **not** a convex function. The proof appeals to Lemma S5.1 (in the appendix), whose own proof (lines 1043–1069) relies on:
1. Voronoi cell stability (same issue as Gap 1)
2. An approximation `‖θ - θ*‖ ≈ ‖θ - μ‖` that loses constants
3. Dropping `O(exp(-Δ_min²/(128σ²)))` corrections that are not rigorously bounded

The claim that `W(θ) - W(θ*)` is locally quadratic with curvature `π_min/2` is plausible under strong separation but is not rigorously established. Standard results on local strong convexity of k-means (e.g., Pollard 1981, Chakraborty & Das 2019) require more careful treatment.

**Severity**: High. This is the foundation for the entire empirical process argument in Lemma 2.

---

### ⚠️ MODERATE ISSUE 1: Lemma 4 — Overstated Convergence Rate

**Location**: S5 lines 626–646

**The claim**: Lloyd's algorithm achieves contraction factor `½` per iteration within the good basin.

**The problem**: The contraction factor of exactly 1/2 is asserted without proof. Known results on Lloyd's algorithm (e.g., Bottou & Bengio 1995, Lu & Zhou 2016) show linear convergence under separability conditions, but the exact rate depends on the cluster separation and the initial distance. A factor of 1/2 is a specific numeric claim that needs justification.

**Severity**: Moderate. The qualitative claim (linear convergence) is well-established; only the exact constant matters for sample complexity calculations.

---

### ⚠️ MODERATE ISSUE 2: Lemma 4 — Overstated Initialization Success Probability

**Location**: S5 lines 648–662

**The claim**:
```
p_hit ≥ π_min^K (constant)
```

**The problem**: The probability that a random initialization (K uniformly sampled points) lands within `Δ_min/8` of each true center is substantially lower than `π_min^K`. Even if one point is drawn from each cluster (probability ≈ π_min^K), that point still needs to be within `Δ_min/8` of its cluster center. For sub-Gaussian noise, each such event has probability roughly `1 - exp(-c Δ_min²/σ²)`, but the joint probability over K such events is much smaller than `π_min^K/2`.

The claim that `p_0 = π_min^K / 2` is unjustified. With K=8 and π_min = 0.1, this gives p_0 ≈ 5×10⁻⁹, making R = C_R log n restarts wildly insufficient. For the AlN case (K=8, n=534), even R = 534 log 534 ≈ 3,350 restarts would give ~1.7% chance of success.

**Severity**: Moderate to High. This directly affects the practical guarantee and the claimed `O(log n)` restarts.

---

### ⚠️ MODERATE ISSUE 3: Lemma 2 — Constant Absorption Hand-Waving

**Location**: S5 lines 470–472

**The issue**:
```
using C_L² ≤ C_7 σ² d_φ (the dominant term when σ²d_φ ≫ max‖μ‖², 
or a constant otherwise) to absorb numerical constants
```

This is sloppy. The two cases (dominant noise vs. dominant signal) produce different constants, and the proof should either:
- Track both regimes explicitly, or
- State the bound in terms of `C_L²` directly rather than absorbing into `σ²d_φ`

**Severity**: Moderate. Does not invalidate the result but makes it non-constructive.

---

### ✅ CORRECT ELEMENTS (S5):

1. **Lemma 3 (Deterministic partition recovery)**: Rigorously correct. The triangle inequality argument is clean and verified:
   - `1/8 + 3/8 = 1/2` ✓
   - `7/8 - 3/8 = 1/2` ✓
   - Direction: `‖φ - θ_{j_k}‖ ≤ Δ_min/2 ≤ ‖φ - θ_{j'}‖` ✓

2. **Lemma 2 Peeling argument** (Steps 4–6): Standard technique, correctly applied. The geometric series bound `Σ 4^j` is dominated by the first term.

3. **Exponent negativity check** (Section S5.7): All exponents are verified negative. The self-verification table is correct.

4. **Theorem 5 final assembly**: Given the lemmas, the probability bound assembly is logically correct.

5. **Supporting lemmas (S5 Appendix)**: Lipschitz property, covering number bound, and sub-Gaussian norm bound are standard and correctly stated.

---

## PART 2: S6 — Proposition 6 (Bootstrap ARI Stability) — 238 lines

### VERDICT: HEURISTIC, NOT RIGOROUS

The proposition is presented as a formal mathematical result, but the proof is a sketch and key claims are explicitly disclaimed as non-rigorous. As a practical diagnostic, it's reasonable. As a mathematical proposition, it's incomplete.

---

### ❌ CRITICAL GAP 4: Proposition 6 Is Only a Proof Sketch

**Location**: S6 lines 119–125

The entire "proof" is 7 lines of high-level description:

- Part (a): Cites Ostrovsky et al. (2013), Cañas & Rosasco (2012), Pollard (1981) without deriving any bounds. The claim that "bootstrap resampling perturbs the empirical distribution by at most O(1/√N) in Wasserstein distance" → "k-means solution is Lipschitz" → "ARI between two ε-close partitions is at least 1 - O(εK)" is a chain of implications where no constants or explicit bounds are given.
- Part (b): The `O(K/√N)` bound for expected ARI is cited to Hubert & Arabie (1985) and Morey & Agresti (1983), but the expected ARI between two k-means runs on i.i.d. Gaussian data is not the same as the expected ARI between two completely random K-partitions. K-means on structureless data still produces geometrically constrained (Voronoi) partitions, not arbitrary ones.
- Part (c): **Explicitly stated as non-rigorous** (line 223: "a heuristic approximation, not a proven bound"). This is honest but means the diagnostic threshold has no formal mathematical backing.

**Severity**: High. Proposition 6 should be reclassified as a "Conjecture" or "Heuristic diagnostic" rather than a "Proposition."

---

### ⚠️ MODERATE ISSUE 4: Numerical Inconsistency in δ/log K vs. Stability

**Location**: S6 Table 1 (line 158–167)

| Dataset | S(Φ, K) | δ/log K | SCX F1 |
|---------|---------|---------|--------|
| AlN v3 | 0.93 | 0.15 | 0.87 |
| CIFAR-10 | 0.96 | 0.12 | 0.62 |
| DermaMNIST | 0.48 | 0.52 | 0.10 |

**The issue**: Part (a) of Proposition 6 claims that in the strong-feature regime, `δ/log K ≳ 1 - O(σ²/Δ_min²)`, implying δ/log K should be close to 1 when S ≈ 1. But the data shows S ≈ 0.93–0.96 while δ/log K ≈ 0.12–0.15. This is the opposite direction.

The diagnostic rule in part (c) says `δ/log K ≳ ½(1 - S)`. For AlN (S=0.93): ½(1-0.93) = 0.035, and δ/log K = 0.15 — within a factor of 4x, but the inequality is `≳` (greater than or approximately), and 0.15 > 0.035 holds.

For DermaMNIST (S=0.48): ½(1-0.48) = 0.26, and δ/log K = 0.52. Here 0.52 > 0.26, so the inequality holds but is very loose (2x).

For CIFAR-10 (S=0.96): ½(1-0.96) = 0.02, and δ/log K = 0.12. Again holds but 6x loose.

So the heuristic inequality is satisfied but very loose. This is acceptable for a heuristic but undermines the claim that S provides a tight bound on δ.

**Severity**: Moderate. The relationship exists qualitatively but is quantitatively weak.

---

### ✅ CORRECT ELEMENTS (S6):

1. **Honesty about limitations**: The entire §"Limitations and Practical Guidance" (lines 173–237) is well-written and appropriately caveated. The explicit acknowledgment that "(c) is a heuristic approximation, not a proven bound" and that "stability is sufficient, not necessary" is commendable.

2. **BBP spectral analysis critique**: The five-point critique of why BBP is unsuitable (lines 19–30) is valid and well-reasoned.

3. **Algorithm**: Algorithm 1 (bootstrap stability) is correctly specified.

---

## PART 3: S7 — Experimental Details — 186 lines

### VERDICT: MOSTLY SOUND WITH MINOR INCONSISTENCIES

---

### ⚠️ MODERATE ISSUE 5: DermaMNIST SCX Underperforms Baseline

**Location**: S7 line 91

**Reported**: `SCX F1 = 0.101, loss baseline F1 = 0.105`

**The issue**: The text characterizes this as "negligible improvement" and "consistent with Theorem 2's prediction that SCX cannot significantly outperform the baseline." But 0.101 < 0.105 means SCX is **worse** than baseline. Theorem 2 gives an upper bound (`F1_SCX ≤ F1_base + C_F √(δ/2)`), so 0.101 ≤ 0.105 satisfies the bound, but the interpretation should be that SCX **degrades** performance, not that it merely "doesn't help."

For a method whose claim is to detect noise, achieving lower F1 than a loss-threshold baseline is worse than "no improvement" — it means the method introduces false positives that harm precision more than the baseline does.

**Severity**: Moderate. The characterization is misleading but not factually incorrect (the inequality holds).

---

### ⚠️ MINOR ISSUE 1: AlN Sample Sizes Are Tiny

**Location**: S7 lines 10, 26

**The data**: 534 frames, M=12 experts, each expert sees ~44 frames.

**The issue**: Theorem 5 requires `n_min → ∞` and the exponential convergence in Lemma 2 requires `n` large relative to `K d_φ`. With n_min ≈ 44, K=8, d_φ=100, we have n/(K d_φ) ≈ 44/800 ≈ 0.055. This is well below the regime where the asymptotic theory applies. The empirical success at n=534 is encouraging but doesn't validate the asymptotic theory — it validates the practical utility at small n where the proofs don't guarantee anything.

**Severity**: Minor. The theory is asymptotic; the experiments show practical utility at finite n. This is common in ML papers but should be acknowledged.

---

### ⚠️ MINOR ISSUE 2: Inconsistent `δ/log K` Values Across Sections

**Location**: S6 line 163 vs. S7 line 62

- S6 Table says `δ/log K = 0.12` for CIFAR-10
- S7 line 62 says `δ/log K ≈ 0.15` for CIFAR-10

Difference: 0.12 vs 0.15 (25% relative error). This is a significant discrepancy for a "theoretical" quantity. Either the table or the text is wrong.

**Severity**: Minor to Moderate. Creates doubt about which value is correct and how δ was actually estimated.

---

### ✅ CORRECT ELEMENTS (S7):

1. **Noise injection protocol** (§S7.5): Correctly specified uniform-label-flip protocol consistent with Assumption A4.

2. **Evaluation metrics** (§S7.6): Standard precision/recall/F1 definitions, correctly stated.

3. **Computational resources** (Table tab:compute): Reasonable and well-documented.

4. **DermaMNIST ResNet-18 comparison**: Validates that better features restore SCX effectiveness (F1: 0.101 → 0.48 with better features).

---

## PART 4: S8 — Numerical Verification — 274 lines

### VERDICT: ALGEBRAICALLY CORRECT BUT EMPIRICALLY EMPTY

The "verification" reduces to checking algebraic identities that hold by definition. There is no code to inspect, no Monte Carlo simulation, and no finite-sample verification of the Bahadur-Rao asymptotics.

---

### ❌ CRITICAL: No Verifiable Code

**Location**: S8 line 5

**Claim**: "All computations are performed using the Python script `numerical_verify.py` with standard double-precision arithmetic."

**Reality**: No file `numerical_verify.py` exists in `F:/scx/papers/scx_theory/` or anywhere in the repository. The reported results cannot be reproduced or verified. All reported values are taken on faith.

**Severity**: Critical. Without code, S8 is not a verification — it's a claim about a verification.

---

### ❌ CRITICAL: The "Machine-Precision Equality" Is Tautological

**Location**: S8 sections on Test Cases 1–5

**The claim**: `K_ad = C_min/η` to "machine precision" (< 10⁻¹⁵).

**The reality**: From the formulas:

```
C_min = (η/2) · ((1-η)/η)^s · (1/λ₀* + 1/|λ₁*|) / √(θ*(1-θ*))
C_min/η = (1/2) · ((1-η)/η)^s · (1/λ₀* + 1/|λ₁*|) / √(θ*(1-θ*))
K_ad = ((1-η)/η)^s · (1/λ₀* + 1/|λ₁*|) / (2√(θ*(1-θ*)))
```

These are **algebraically identical expressions**. The "verification" that they match to machine precision is simply checking that the same formula computed two ways gives the same result. This is not a mathematical discovery — it's a sanity check on arithmetic.

Similarly, "KL(θ*‖p₀) = KL(θ*‖p₁) holds to ±10⁻¹⁶" merely confirms that θ* was computed correctly — it's the definition of θ*.

**The only non-trivial verification would be**: demonstrating that the Bahadur-Rao asymptotic limit (as M → ∞) matches finite-M Monte Carlo simulations of the SCX detector. The finite-M convergence table (Table tab:finiteM in S8) takes a step in this direction, but:
1. The table only shows Test Case 2 (because the others have error probabilities "below machine epsilon at M=500")
2. The values are computed analytically from the binomial CDF, not from simulated SCX runs
3. There is no demonstration that the SCX detector's actual F1 at finite M matches these theoretical tail probabilities

**Severity**: Critical. S8 should be retitled "Algebraic Consistency Check" not "Numerical Verification."

---

### ⚠️ MODERATE ISSUE 6: Test Case 4 "Prediction" Is Circular

**Location**: S8 lines 173–177

**Claim**: "At η = 1/2, the correction term (1/M)·log((1-η)/η)/D* = 0, so θ† = θ*. The two limits coincide exactly. Theoretical prediction confirmed."

**Reality**: This is a direct algebraic consequence of the formula for θ†, not an empirical confirmation. It's equivalent to checking that log(1) = 0.

**Severity**: Moderate. Framing algebraic identities as empirical confirmations is misleading.

---

### ✅ CORRECT ELEMENTS (S8):

1. **Algebraic self-consistency**: All computed values (θ*, κ, λ₀*, λ₁*, D*, s) satisfy their defining equations. I verified Case 1 analytically:
   - `θ* = log((1-p₀)/(1-p₁)) / log(p₁(1-p₀)/(p₀(1-p₁)))` ✓
   - `KL(θ*‖p₀) = KL(θ*‖p₁)` by construction ✓
   - `D* = λ₀* + |λ₁*|` ✓
   - `s ∈ (0,1)` ✓

2. **Trend validation**: Across test cases, the relationship between separation (Δ) and Chernoff information (κ) is monotonic, and the non-adaptive penalty grows as η deviates from 1/2 — both theoretically correct behaviors.

3. **Finite-M convergence direction**: The trend in Table tab:finiteM (M=50→500 approaching the asymptotic limit from below) is consistent with the O(1/M) Bahadur-Rao correction term.

---

## CROSS-SECTION CONSISTENCY CHECK

### S4 ↔ S8 Consistency:

| Claim in S4 | Check in S8 | Status |
|------------|-------------|--------|
| C_min formula (Eq. in Theorem 4') | C_min values in S8 tables | ✓ Consistent |
| Adaptive threshold θ† | Used implicitly in K_ad computation | ✓ Consistent |
| Bahadur-Rao asymptotic form | Finite-M table in S8 | ✓ Direction correct |

### S5 ↔ S7 Consistency:

| Claim in S5 | Reported in S7 | Status |
|------------|---------------|--------|
| K-means with K discovered via elbow | "K=8 states, elbow method" (S7 line 20) | ✓ |
| Strong separation needed | Δ_min/(σ√d_φ) not reported for AlN | ⚠️ Cannot verify |
| Fixed K assumption | K=8 for AlN, K=10 for CIFAR-10 | ✓ |

### S6 ↔ S7 Consistency:

| Claim in S6 | Reported in S7 | Status |
|------------|---------------|--------|
| CIFAR-10 δ/log K ≈ 0.12 | S7 says δ/log K ≈ 0.15 | ❌ Mismatch |
| DermaMNIST δ/log K ≈ 0.52 | S7 says δ/log K ≈ 0.52 | ✓ |
| DermaMNIST S < 0.5 | S7 reports "S(Φ, K) < 0.5" | ✓ (S6 Table: 0.48) |

### S5 ↔ S6 Consistency:

The theoretical frameworks are loosely coupled. S5 proves state discovery works under strong separation; S6 provides a diagnostic for whether features are strong enough. The connection is conceptual, not formal.

---

## SUMMARY OF FINDINGS

### Critical Gaps (4):

| # | Section | Description | Fix difficulty |
|---|---------|-------------|----------------|
| 1 | S5 Lemma 1, Step 5 | Circular contraction argument for θ* proximity | Hard — needs new argument |
| 2 | S5 Lemma 1, Step 4 | Unsubstantiated noise expectation bound | Medium — needs careful derivation |
| 3 | S5 Lemma 2, Step 1 | Quadratic lower bound / "strong convexity" of k-means | Medium — needs rigorous justification |
| 4 | S6 Proposition 6 | Proof is only a sketch; Part (c) explicitly non-rigorous | Easy — reclassify as Conjecture/Heuristic |

### Moderate Issues (6):

| # | Section | Description |
|---|---------|-------------|
| 1 | S5 Lemma 4 | Overstated Lloyd contraction rate (1/2) |
| 2 | S5 Lemma 4 | Overstated initialization success probability |
| 3 | S5 Lemma 2 | Sloppy constant absorption between noise/signal regimes |
| 4 | S6 Table 1 | δ/log K vs. stability relationship is quantitatively loose |
| 5 | S7 | DermaMNIST SCX underperforms baseline, characterization is misleading |
| 6 | S8 Test Case 4 | Circular "verification" of algebraic identity |

### Minor Issues (3):

| # | Section | Description |
|---|---------|-------------|
| 1 | S7 | AlN sample size (n=534) is far below asymptotic regime |
| 2 | S6/S7 | δ/log K for CIFAR-10: 0.12 vs. 0.15 (inconsistent) |
| 3 | S8 | No reproducible code; all values are unverifiable |

---

## RECOMMENDATIONS

### For S5 (Theorem 5):

1. **Fix Lemma 1**: Remove the circular contraction argument. Instead, use a direct approach: show that outside a ball of radius Δ_min/4 around μ, the population objective W(θ) is provably larger than W(μ) + gap, so the minimizer must lie inside. This avoids the fixed-point circularity.

2. **Justify the noise bound**: Provide a rigorous derivation of the conditional noise expectation bound, or replace it with a cruder but provable bound (e.g., using Hölder's inequality and the sub-Gaussian tail).

3. **Strengthen Lemma S5.1**: The quadratic lower bound needs a rigorous proof. One approach: under strong separation, the Voronoi cells are stable, so W(θ) decomposes into K nearly-independent quadratic forms plus an exponentially small correction. Bound the correction explicitly.

4. **Revisit initialization analysis**: Either provide a tighter bound or acknowledge that more restarts may be needed in practice.

### For S6 (Proposition 6):

5. **Reclassify**: Change from "Proposition" to "Heuristic Diagnostic" or "Conjecture 6." The proof sketch is insufficient for a formal proposition. The practical value is real, but the mathematical status should be honest.

6. **Fix the proof sketch**: If keeping as a proposition, provide a complete proof for parts (a) and (b) with explicit constants. Part (c) should remain as "practical guidance."

### For S7 (Experiments):

7. **Fix the CIFAR-10 δ/log K discrepancy**: Reconcile 0.12 vs. 0.15.

8. **Characterize DermaMNIST honestly**: "SCX F1 (0.101) was slightly below the loss baseline (0.105), indicating the method can actively harm performance when features are very weak."

### For S8 (Numerical Verification):

9. **Provide the code**: `numerical_verify.py` must be included in the repository.

10. **Add real verification**: Run Monte Carlo simulations of the SCX detector at finite M and compare the empirical F1 to the Bahadur-Rao asymptotic prediction. This is the only non-trivial test.

11. **Retitle**: "Algebraic Consistency Check and Finite-M Convergence Analysis" rather than "Numerical Verification of Theoretical Constants."

---

## OVERALL ASSESSMENT

The SCX theoretical framework is coherent. The phase diagram (strong features → state discovery → noise detection; weak features → baseline degradation) is well-motivated and empirically supported. The main gaps are in the rigor of the k-means consistency proof (S5) and the formal status of the bootstrap diagnostic (S6). The experimental results largely support the theory, though S8's "verification" is tautological and needs empirical Monte Carlo validation.

**If these gaps were addressed, the paper would meet the standard of a strong theoretical ML paper (e.g., JMLR, Annals of Statistics). In its current form, the proofs are at the level of a well-argued technical report — the ideas are right, but the details need work.**
