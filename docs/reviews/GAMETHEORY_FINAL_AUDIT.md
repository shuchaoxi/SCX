# Game Theory Final Audit: protocol_governance.tex & NPE Theorem 1

**Audit date:** 2026-07-03  
**Auditor:** Hermes Agent (independent first-principles verification)  
**Scope:** `yajie_protocol/main.md` (NPE Theorem 1, 1942 lines), `scx_governance/main.md` (M* equation, q_min calibration, 1151 lines), `protocol_governance.tex` (Hoeffding bounds, 2454 lines)  
**Cross-reference:** `scx_theory/main.md` (core Theorem 1 F1 bound, Theorem 4 minimax optimality)  
**Previous reviews consulted:** `game_theory_review.md`, `game_theory_rounds_7_8.md`, `review_protocol_governance.md`, `review_protocol_governance_C3.md`

---

## Executive Summary

**Overall verdict: FAILS rigorous game-theoretic audit.** Despite an AUDIT_STATUS.md claim that NPE Theorem 1 was "reconstructed from first principles" with "5 algebraic errors fixed," the current source files (`yajie_protocol/main.md`) still contain **at least 4 uncorrected algebraic errors** in Theorem 1 alone, and the M* equation in `scx_governance/main.md` has a **missing (1-ρ̄) factor** in its "explicit" solution. The q_min calibration is asserted, not derived. The governance↔SCX detection-rate bridge remains a P1 structural gap.

| Component | Status | Critical Errors |
|-----------|--------|-----------------|
| NPE Theorem 1 (adoption equilibrium condition) | ❌ FAILS | 4 algebraic errors, 2 definition contradictions |
| M* self-referential equation | ❌ FAILS | Missing (1-ρ̄) factor in explicit solution |
| q_min calibration assumption | ❌ FAILS | Unsubstantiated assertion, not derivable from A1-A12 |
| Hoeffding bounds (governance) | ✅ PASSES | Correct after C3 fixes |
| Governance↔SCX detection rate bridge | ❌ GAP | No formal mapping established |

---

## 1. NPE Theorem 1: First-Principles Re-Derivation

### 1.1 The Theorem as Stated (`yajie_protocol/main.md` lines 167-200)

The theorem claims for game Γ^NP with n ≥ 2 jurisdictions:

1. (A,...,A) is a pure-strategy Nash equilibrium iff **Δ(|E|) ≥ λ − κ**
2. (D,...,D) is a pure-strategy NE iff Δ(|E|) ≤ −(n−1)κ
3. No asymmetric pure-strategy NE exists (except on a measure-zero set)
4. In the intermediate region −(n−1)κ < Δ(|E|) < λ − κ, a unique symmetric mixed-strategy NE exists

Where:
- Δ(|E|) ≡ V[θ(|E|)] − V[θ(0)] − (c^adopt − c^develop) + κ   (line 161)
- λ = fragmentation cost (public bad triggered when any jurisdiction develops)
- κ = marginal proliferation cost per other developer
- Assumption A4: λ > κ > 0

### 1.2 Independent Re-Derivation of (A,...,A) NE Condition

**Payoffs under candidate equilibrium (A,...,A):**
- u_i(A, A_{-i}) = V[θ(|E|)] − c^adopt   (no fragmentation: n_D = 0)
- u_i(D, A_{-i}) = V[θ(0)] − c^develop − κ − λ

Justification for u_i(D, A_{-i}): If i unilaterally deviates to D, then n_D = 1 > 0, triggering fragmentation (−λ). The κ term: from equation (5), the payoff under D includes −κ·(n_D(s_{-i}) + 1) = −κ·(0 + 1) = −κ.

**NE condition:** u_i(A, A_{-i}) ≥ u_i(D, A_{-i})

V[θ(|E|)] − c^adopt ≥ V[θ(0)] − c^develop − κ − λ

Rearranging:
V[θ(|E|)] − V[θ(0)] − c^adopt + c^develop + κ ≥ −λ

Substituting Δ(|E|) = V[θ(|E|)] − V[θ(0)] − c^adopt + c^develop + κ:
**Δ(|E|) ≥ −λ**   ← CORRECT CONDITION

### 1.3 Comparison: What the Paper Claims vs. What Is Correct

| Source | Condition | Correct? |
|--------|-----------|----------|
| **Theorem statement** (line 172) | Δ(|E|) ≥ λ − κ | ❌ WRONG |
| **Proof** (line 198): "整理得 Δ(|E|) + κ ≥ κ − λ + κ" | Δ(|E|) ≥ κ − λ (= −(λ−κ)) | ❌ WRONG — AND inconsistent with the theorem statement! |
| **First-principles derivation** | Δ(|E|) ≥ −λ | ✅ CORRECT |

The proof on line 198 contains an internal algebraic error: it claims Δ(|E|) + κ ≥ κ − λ + κ, which simplifies to Δ(|E|) ≥ κ − λ = −(λ−κ). This is **the negative** of the theorem's stated condition (λ−κ). The proof and theorem statement are internally contradictory — a red flag that neither was independently verified.

### 1.4 The "Strictly Dominant Nash Equilibrium" Question

The paper claims "unanimous adoption is the unique Nash equilibrium" once |E| > |E|*.

With the correct condition Δ(|E|) ≥ −λ (rather than Δ(|E|) ≥ λ − κ), we have:

- Since λ > 0, the condition Δ(|E|) ≥ −λ is **always satisfied when Δ(|E|) ≥ 0**.
- Since Δ(|E|) = V[θ(|E|)] − V[θ(0)] − c^adopt + c^develop + κ, and given c^develop ≫ c^adopt and κ > 0, Δ(|E|) is typically positive.
- Therefore, with the correct condition, (A,...,A) is **almost always** a NE — it does NOT require a "critical CEC size" as the paper claims.

This means the entire "CEC critical value" (Theorem 2, line 294-313), the "self-reinforcing" corollary (line 315-330), and the "temporal decay of first-mover advantage" corollary (line 332-368) are built on the wrong equilibrium condition. The threshold |E|* that the paper solves for (line 453-457) is based on Δ(|E|*) = λ − κ, which should be Δ(|E|*) = −λ.

**Implication:** (A,...,A) is a NE under far weaker conditions than the paper claims. The "uniqueness" result — that (A,...,A) becomes the only NE once |E| exceeds a critical value — is qualitatively correct (the direction is right) but the quantitative threshold is wrong by a margin of 2κ + λ.

### 1.5 Additional Algebraic Errors in NPE Theorem 1

**Error 2: Mixed-strategy probability formula (line 280-281)**

Paper gives: Γ = −Δ(|E|) + λ − 2κ

Re-derivation from the indifference condition (lines 270-277):
- 𝔼[u_i(A)]: V[θ(|E|)] − c^adopt − κ(n−1)(1−p) − λ[1 − p^{n−1}]
- 𝔼[u_i(D)]: V[θ(0)] − c^develop − κ[(n−1)(1−p) + 1] − λ
- Subtract and set equal: V[θ(|E|)] − c^adopt − λ[1 − p^{n−1}] = V[θ(0)] − c^develop − κ − λ
- Using Δ(|E|) definition: Δ(|E|) + V[θ(0)] − c^develop + κ − c^adopt + c^adopt − λ[1−p^{n−1}] = V[θ(0)] − c^develop − κ − λ
- Actually, let me be more careful:

V[θ(|E|)] − c^adopt − λ[1 − p^{n−1}] = V[θ(0)] − c^develop − κ − λ

Rearranging: λ·p^{n−1} = λ + V[θ(|E|)] − c^adopt − V[θ(0)] + c^develop + κ

Now Δ(|E|) = V[θ(|E|)] − V[θ(0)] − c^adopt + c^develop + κ

So: λ·p^{n−1} = λ + Δ(|E|) − c^adopt + c^adopt
Wait: V[θ(|E|)] − V[θ(0)] − c^adopt + c^develop + κ = Δ(|E|)

So: λ·p^{n−1} = λ + Δ(|E|)

Therefore: Γ = λ + Δ(|E|), and the indifference condition is λ·p^{n−1} = λ + Δ(|E|)

But wait, Δ(|E|) < 0 in the intermediate region (since the paper claims the intermediate region is Δ(|E|) < λ − κ, and for Δ(|E|) to be negative enough, perhaps...). Actually, the mixed strategy is indeed relevant only when both pure strategy conditions fail.

The paper gives: Γ = −Δ(|E|) + λ − 2κ

Let me re-derive more carefully with the payoff functions from lines 256-268:

𝔼[u_i(A)] = V[θ(|E|)] − c^adopt − κ(n−1)(1−p) − λ[1 − p^{n−1}]
𝔼[u_i(D)] = V[θ(0)] − c^develop − κ[(n−1)(1−p) + 1] − λ

Equating:
V[θ(|E|)] − c^adopt − κ(n−1)(1−p) − λ[1 − p^{n−1}] = V[θ(0)] − c^develop − κ(n−1)(1−p) − κ − λ

Cancel −κ(n−1)(1−p):
V[θ(|E|)] − c^adopt − λ[1 − p^{n−1}] = V[θ(0)] − c^develop − κ − λ

λ[1 − p^{n−1}] = V[θ(|E|)] − c^adopt − V[θ(0)] + c^develop + κ + λ
= Δ(|E|) + λ

λ·p^{n−1} = λ − (Δ(|E|) + λ) = −Δ(|E|)

So the correct condition is: **λ·p^{n−1} = −Δ(|E|)**

With Ψ(p) = λ·p^{n−1}, we have: **Γ = −Δ(|E|)** ← CORRECT

Paper gives: Γ = −Δ(|E|) + λ − 2κ ← WRONG (extra λ − 2κ term)

The review (game_theory_review.md line 111-118) identified this correctly.

**Error 3: 2-player mixed-strategy probability (line 426)**

Paper gives: p* = (−Δ_A − 2κ)/(λ − κ)

Re-derivation for the 2-player case: With payoffs from the "支付矩阵与均衡区域" section (lines 371-429), the mixed strategy indifference condition for symmetric 2×2 game with payoffs:

(A,A): a = V[θ(|E|)] − c^adopt
(A,D): b = V[θ(|E|)] − c^adopt − κ − λ   (peer D, fragmentation, plus κ from peer)
(D,A): c = V[θ(0)] − c^develop − κ − λ   (sole D, fragmentation)
(D,D): d = V[θ(0)] − c^develop − 2κ − λ   (both D, fragmentation plus 2κ)

Wait, I need to verify these payoffs from the payoff functions (lines 436-438):
π_i(A, a_{-i}) = V[θ(|E|)] − c^adopt − κ·n_D − λ·𝕀[n_D > 0]
π_i(D, a_{-i}) = V[θ(0)] − c^develop − κ·(n_D + 1) − λ·𝕀[n_D > 0]

For (A,A): n_D = 0, so π_i(A,A) = V[θ(|E|)] − c^adopt ✓
For (A,D): n_D = 1 (other plays D), so π_i(A,D) = V[θ(|E|)] − c^adopt − κ − λ ✓
For (D,A): n_D = 0 (other plays A), so π_i(D,A) = V[θ(0)] − c^develop − κ·1 − λ = V[θ(0)] − c^develop − κ − λ ✓
For (D,D): n_D = 1 (other plays D), so π_i(D,D) = V[θ(0)] − c^develop − κ·2 − λ = V[θ(0)] − c^develop − 2κ − λ ✓

Now Δ_A = V[θ(|E|)] − c^adopt − V[θ(0)] + c^develop + κ  (from line 380-381)

Mixed strategy indifference: p·a + (1−p)·b = p·c + (1−p)·d

p·[V[θ(|E|)] − c^adopt] + (1−p)·[V[θ(|E|)] − c^adopt − κ − λ] = p·[V[θ(0)] − c^develop − κ − λ] + (1−p)·[V[θ(0)] − c^develop − 2κ − λ]

Left side: V[θ(|E|)] − c^adopt − (1−p)(κ + λ) = V[θ(|E|)] − c^adopt − κ − λ + p(κ + λ)
Right side: V[θ(0)] − c^develop − 2κ − λ + p(2κ + λ − κ − λ) = V[θ(0)] − c^develop − 2κ − λ + pκ

Equating:
V[θ(|E|)] − c^adopt − κ − λ + p(κ + λ) = V[θ(0)] − c^develop − 2κ − λ + pκ

V[θ(|E|)] − c^adopt + p(κ + λ) = V[θ(0)] − c^develop − κ + pκ

p(κ + λ − κ) = V[θ(0)] − c^develop − κ − V[θ(|E|)] + c^adopt

p·λ = V[θ(0)] − c^develop − κ − V[θ(|E|)] + c^adopt

p·λ = −[V[θ(|E|)] − c^adopt − V[θ(0)] + c^develop + κ]
p·λ = −Δ_A

**p* = −Δ_A / λ**   ← CORRECT (for 2-player mixed strategy)

Paper gives: p* = (−Δ_A − 2κ)/(λ − κ) ← WRONG

The review (game_theory_review.md line 52) gave p* = (−Δ_A − κ)/(λ − κ), which is ALSO wrong. My derivation gives p* = −Δ_A/λ. Let me double-check...

Actually wait. Let me re-examine. The review's derivation was different. Let me look at the paper's 2-player payoff matrix more carefully.

The paper says (line 386):
π_i(D, A) = V[θ(0)] − c^develop − κ − λ

But should it be? From the payoff function (5): π_i(D, a_{-i}) = V[θ(0)] − c^develop − κ·(n_D + 1_{-i}^D) − λ·𝕀[n_D > 0]

When the other player plays A: n_D = 0, so π_i(D, A) = V[θ(0)] − c^develop − κ·1 − λ = V[θ(0)] − c^develop − κ − λ. This is correct.

And from (4): π_i(A, a_{-i}) = V[θ(|E|)] − c^adopt − κ·n_D − λ·𝕀[n_D > 0]
When the other plays D: n_D = 1, so π_i(A, D) = V[θ(|E|)] − c^adopt − κ − λ

So the 2×2 payoff matrix is:
```
         A                    D
A   (V[θ]−c_ad, V[θ]−c_ad)   (V[θ]−c_ad−κ−λ, V[0]−c_dev−κ−λ)
D   (V[0]−c_dev−κ−λ, V[θ]−c_ad−κ−λ)   (V[0]−c_dev−2κ−λ, V[0]−c_dev−2κ−λ)
```

Where V[θ] = V[θ(|E|)] and V[0] = V[θ(0)].

Now, the review (game_theory_review.md lines 32-52) had a different set of payoffs:
- a = V[θ(|E|)] − c^adopt
- b = V[θ(|E|)] − c^adopt − λ   (NO κ!)
- c = V[θ(0)] − c^develop − κ − λ
- d = V[θ(0)] − c^develop − 2κ − λ

The review's b term was WRONG — they had V[θ(|E|)] − c^adopt − λ without κ. But from the payoff function, when one player is A and the other is D, the A-player suffers κ·n_D = κ·1 = κ plus the λ fragmentation cost, so b should have both κ and λ.

Let me redo my derivation with the correct payoff matrix:

a = V[θ(|E|)] − c^adopt
b = V[θ(|E|)] − c^adopt − κ − λ
c = V[θ(0)] − c^develop − κ − λ
d = V[θ(0)] − c^develop − 2κ − λ

Indifference: p·a + (1−p)·b = p·c + (1−p)·d

p·[V[θ] − c_ad] + (1−p)·[V[θ] − c_ad − κ − λ] = p·[V[0] − c_dev − κ − λ] + (1−p)·[V[0] − c_dev − 2κ − λ]

LHS = V[θ] − c_ad − (1−p)(κ+λ) = V[θ] − c_ad − κ − λ + p(κ+λ)
RHS = V[0] − c_dev − 2κ − λ + p(2κ + λ − κ − λ) = V[0] − c_dev − 2κ − λ + pκ

V[θ] − c_ad − κ − λ + p(κ+λ) = V[0] − c_dev − 2κ − λ + pκ

V[θ] − c_ad + p(κ+λ) = V[0] − c_dev − κ + pκ

p(κ + λ − κ) = V[0] − c_dev − κ − V[θ] + c_ad

p·λ = −V[θ] + c_ad + V[0] − c_dev − κ

p·λ = −(V[θ] − c_ad − V[0] + c_dev + κ)

Now Δ_A = V[θ] − c_ad − V[0] + c_dev + κ (from line 380-381)

So: p·λ = −Δ_A

**p* = −Δ_A / λ** ← This is the correct 2-player mixed strategy NE probability.

In the "intermediate region" where both pure strategy NE conditions fail, −Δ_A/λ should be in (0,1).

The paper gives p* = (−Δ_A − 2κ)/(λ − κ), which is wrong. The review gave p* = (−Δ_A − κ)/(λ − κ), which is also wrong. Both are incorrect.

**Error 4: Δ_A definition inconsistency between 2-player and N-player (lines 398 vs 447)**

2-player condition (line 398): Δ_A ≥ λ for (A,A) to be NE
N-player condition (line 447): Δ_A ≥ λ − κ for (A,...,A) to be NE

For N=2, these should be identical, but they differ by κ. This is the definition inconsistency noted in game_theory_review.md issue 1.6. With the corrected condition Δ_A ≥ −λ, both 2-player and N-player versions agree (since both reduce to the same inequality after substituting the payoff functions).

### 1.6 Summary: NPE Theorem 1 Errors

| # | Error | Location | Paper's Claim | Correct Value |
|---|-------|----------|---------------|---------------|
| 1 | (A,...,A) NE condition | Line 172 (theorem) / Line 198 (proof) | Δ(|E|) ≥ λ − κ / Δ(|E|) ≥ κ − λ | **Δ(|E|) ≥ −λ** |
| 2 | N-person mixed-strategy Γ | Line 281 | −Δ(|E|) + λ − 2κ | **−Δ(|E|)** |
| 3 | 2-player mixed-strategy p* | Line 426 | (−Δ_A − 2κ)/(λ − κ) | **−Δ_A / λ** |
| 4 | 2-player vs N-player Δ_A thresholds | Lines 398, 447 | Δ_A ≥ λ vs Δ_A ≥ λ − κ | Both should be Δ_A ≥ −λ (self-consistent) |

**The AUDIT_STATUS.md claim that "NPE Theorem 1: 5 algebraic errors/definition contradictions | Reconstructed from first principles" appears to be FALSE for the current source file.** The errors are still present in `yajie_protocol/main.md`.

---

## 2. M* Self-Referential Equation

### 2.1 Location and Content

`scx_governance/main.md`, Theorem 1 (Transparency Dominance), lines 297-311.

Self-referential form (line 300):
```
M* = ⌈2σ̄² · (1 + (M*-1)ρ̄) · log(κ/(L_B·ε)) / (δ_min − ε)²⌉
```

Claimed "explicit" solution (line 307):
```
M* = ⌈2σ̄² log(κ/(L_B ε)) / ((δ_min − ε)² − 2σ̄² ρ̄ log(κ/(L_B ε)))⌉
```

### 2.2 Independent Derivation

Let A = 2σ̄² log(κ/(L_B ε)) / (δ_min − ε)², C = ρ̄.

From the self-referential equation:
M* = A · (1 + (M* − 1)C)
M* = A · (1 − C + M*C)
M* = A(1−C) + A·C·M*
M* − A·C·M* = A(1−C)
M*(1 − AC) = A(1−C)

**M* = A(1−C) / (1 − AC) = 2σ̄²(1−ρ̄) log(κ/(L_B ε)) / [(δ_min − ε)² − 2σ̄² ρ̄ log(κ/(L_B ε))]**

### 2.3 The Error

The paper's "explicit" solution:
```
M* = 2σ̄² log(κ/(L_B ε)) / ((δ_min − ε)² − 2σ̄² ρ̄ log(κ/(L_B ε)))
```

is **missing the (1−ρ̄) factor** in the numerator. 

Correct: **M* = 2σ̄²(1−ρ̄) log(κ/(L_B ε)) / [(δ_min − ε)² − 2σ̄² ρ̄ log(κ/(L_B ε))]**

### 2.4 Impact

The missing (1−ρ̄) factor means:
- When ρ̄ = 0 (no auditor correlation): the paper's formula and correct formula coincide (1−0=1). OK.
- When ρ̄ > 0: the paper's formula gives a **larger** M* than correct (since the numerator is missing a factor < 1). E.g., with ρ̄ = 0.2, the correct M* is 80% of what the paper claims.
- The numerical example (lines 390-398) uses the incorrect formula, producing a denominator of 0.0016 − 0.0276 = −0.026 < 0, leading to the conclusion that "no finite M suffices." With the corrected formula, the numerator becomes 2·0.01·0.8·6.908 = 0.1105, denominator = −0.026, still negative. So in this specific example, the correction doesn't change the qualitative conclusion — but the formula itself is wrong.

### 2.5 Existence Condition

The denominator must be positive: (δ_min − ε)² > 2σ̄² ρ̄ log(κ/(L_B ε))

The paper notes this condition (line 311: "valid when the denominator is positive") but only in passing. It should be stated as a formal condition of Theorem 1: when this inequality fails, the transparency dominance theorem does NOT hold — the auditor correlation is too high to guarantee honest reporting regardless of how many auditors are added. This is a fundamental limitation of the framework.

---

## 3. q_min Calibration Assumption

### 3.1 Location

`scx_governance/main.md`, Theorem 2 (Opacity Detection Bound), Step 5, lines 491-498.

### 3.2 The Critical Step

The proof proceeds:
- **Step 3** (lines 465-473): q_j ≥ p_min · r_j · (K_total − K_pub)/K_total where r_j is auditor j's coverage ratio
- **Step 4** (lines 475-489): Hoeffding gives P(no detection) ≤ exp(−2M q_min²) where q_min = min_j q_j
- **Step 5** (line 491-492): "A natural calibration is q_min = 1 − K_pub/K_total"

### 3.3 Analysis

The jump from Step 3's lower bound to Step 5's "natural calibration" requires:

**q_min = p_min · r_min · (1 − K_pub/K_total) → set equal to (1 − K_pub/K_total)**

This is valid only if **p_min · r_min = 1**, which means:
1. **p_min = 1**: Every auditor detects every gap they cover with probability exactly 1. This is impossible in practice — auditors have imperfect detection.
2. **r_min = 1**: At least one auditor covers ALL unpublished statistics. This is also unrealistic.

Neither assumption appears in A1-A12. The q_min calibration is **asserted, not derived**.

### 3.4 Proper Treatment

The theorem should state its result as:
```
P(detection) ≥ 1 − exp(−2M · p_min² · r_min² · (1 − K_pub/K_total)²)
```

With the additional parameters p_min and r_min clearly identified as calibration parameters that must be estimated empirically. The current simplified form exp(−2M(1−K_pub/K_total)²) is an upper bound on the detection probability that implicitly assumes perfect auditor coverage and perfect detection — it overstates the actual guarantee.

### 3.5 The "Full Publication = Dominant Strategy" Claim

Step 6 (lines 500-517) claims that the government's best response is full publication K_pub* = K_total. This conclusion depends on the detection probability being high enough. With p_min < 1 and r_min < 1, the detection probability is lower, and the dominance threshold for κ (line 515) becomes correspondingly more demanding. The paper's claim that "the threshold is... easily satisfied for large M" (line 515) remains directionally correct but the quantitative bound is weaker by a factor of p_min²·r_min².

---

## 4. Hoeffding/Chernoff Bounds in Game-Theoretic Context

### 4.1 Protocol Governance (protocol_governance.tex)

The C3 review fixed Theorem 3's derivation of the e^{−2MΔ²} bound using proper one-sided Hoeffding. Verified:
- Step 1: Single auditor one-sided bound: P(not flagged | δ ≥ Δ) ≤ exp(−2Δ²) after normalization. ✅ Correct.
- Step 2: M independent auditors: P(zero flags) ≤ exp(−2MΔ²). ✅ Correct under independence.
- Step 3: n independent events: P(all survive) ≤ exp(−2MΔ²·n). ✅ Correct.

The C3 review also fixed Theorem 2 (detection model) to use median instead of mean, and Theorem 6 (NE) to be about dynamic rotation game. These are separate from the game-theory-in-NPE context.

### 4.2 Governance Paper (scx_governance/main.md)

Theorem 1 (Transparency Dominance) uses a Hoeffding bound for the weighted sum of auditor errors (line 268-271):
P(Σ w_j ε^{(j)} ≥ δ − ε) ≤ exp(−M(δ−ε)²/(2σ̄²))

This is a standard two-sided Hoeffding bound (the paper has factor 2σ̄² in the denominator, which is correct for bounded variables with range [−1,1] after scaling). The one-sided version would use exp(−2M(δ−ε)²/(range)²), losing a factor of 2 in the denominator depending on scaling conventions. The paper's exponent form is internally consistent with the M* derivation that follows.

### 4.3 SCX Core Theorems (scx_theory/main.md)

Theorem 1: F1 ≥ 1 − (1/η)Σρ_s exp(−2MΔ_s²). This uses the two-sided Hoeffding form correctly for the multi-expert consistency-based noise detection.

The governance paper and the core theorems use **different** exponent forms:
- Governance: exp(−M(δ−ε)²/(2σ̄²))
- Core: exp(−2MΔ_s²)

These are not directly comparable without establishing a mapping between the governance detection parameters (δ, ε, σ̄²) and the core theorem's detection gaps (Δ_s). This is the missing bridge (see Section 5).

---

## 5. Governance↔SCX Detection Rate Bridge

### 5.1 The Gap

AUDIT_STATUS.md identifies this as a **P1 structural gap**: "治理↔SCX核心定理检测率桥接引理".

The governance paper's Theorem 1 (Transparency Dominance) claims that with M > M* auditors, honest reporting is strictly dominant. This relies on detection probability bounds derived from Hoeffding inequalities applied to auditor-government deviations.

The SCX core theorems (scx_theory/main.md) prove:
- **Theorem 1**: F1 ≥ 1 − (1/η)Σρ_s exp(−2MΔ_s²) for multi-expert label noise detection
- **Theorem 4**: Exact constant minimax optimality — no algorithm can achieve asymptotically better F1

The NPE paper (yajie_protocol/main.md, line 452) claims: "This uniqueness is underwritten by Theorem 4 (极定理): no alternative algorithm can surpass SCX's minimax-optimal detection rate."

### 5.2 Why the Bridge Is Missing

The core theorems prove detection rates for **label noise in machine learning datasets** — the target is distinguishing mislabeled samples from genuinely difficult samples via multi-expert consistency.

The governance theorems prove dominance of **honest statistical reporting by governments** — the target is detecting deviations between government claims and auditor consensus.

These are fundamentally different detection targets:
1. **Core theorems**: Bernoulli detection events (noisy/clean label), i.i.d. samples, fixed data distribution
2. **Governance**: Continuous deviation detection (∥m − c∥_∞ > ε), strategic government choice, political benefit functions

No formal lemma establishes that the exponential rate 2MΔ² achieved in the label-noise setting translates to the government-reporting setting. The core Theorem 4's minimax optimality applies to label-noise detection with Bernoulli observations — it does NOT automatically extend to detecting continuous strategic deviations in a signaling game with Lipschitz benefit functions.

### 5.3 What Would Be Needed

A bridging lemma would need to:
1. Map the governance detection event {∥m − c∥_∞ > ε | δ ≥ Δ} to a Bernoulli detection framework
2. Show that the effective Δ in the governance setting relates to the core theorem's Δ_s via the auditor noise parameters
3. Establish that the minimax optimality from Theorem 4 implies optimality in the strategic governance setting (or explain why it doesn't)

Without this bridge, the NPE paper's claim that "Theorem 4 underwrites equilibrium uniqueness" is a hand-waving appeal to authority, not a logical consequence.

---

## 6. Cross-Reference: protocol_governance.tex Use of SCX Noise Detection

The `protocol_governance.tex` (2454 lines) is a different paper from the NPE paper. It covers:
- Maintainer rotation game theory
- Hoeffding bounds for maintainer bias detection
- Zero-sum bias equilibrium (Theorem 6)

This paper does NOT directly use the SCX core theorem's noise detection framework. It develops its own detection mechanism based on maintainer mutual audit with Hoeffding bounds (e^{−2MΔ²}). The C3 review confirmed that after fixes, the Hoeffding derivations in `protocol_governance.tex` are mathematically correct.

However, this paper also does not bridge to the core SCX theorems — it independently derives its own detection bounds rather than importing them from the core framework.

---

## 7. Consolidated Error Register

### CRITICAL (Unfixed in source files)

| # | File | Line(s) | Error | Correction |
|---|------|---------|-------|------------|
| C1 | yajie_protocol/main.md | 172, 198 | (A,...,A) NE condition: Δ(|E|) ≥ λ−κ; proof has Δ(|E|) ≥ κ−λ (internally contradictory) | **Δ(|E|) ≥ −λ** |
| C2 | yajie_protocol/main.md | 280-281 | N-person mixed-strategy Γ = −Δ(|E|) + λ − 2κ | **Γ = −Δ(|E|)** |
| C3 | yajie_protocol/main.md | 426 | 2-player mixed p* = (−Δ_A − 2κ)/(λ−κ) | **p* = −Δ_A/λ** |
| C4 | yajie_protocol/main.md | 398, 447 | Δ_A ≥ λ (2-player) vs Δ_A ≥ λ−κ (N-player) inconsistency | Both should be Δ_A ≥ −λ |
| C5 | scx_governance/main.md | 307 | M* explicit solution missing (1−ρ̄) factor | **M* = 2σ̄²(1−ρ̄)log(κ/(L_B ε)) / [(δ_min−ε)² − 2σ̄² ρ̄ log(κ/(L_B ε))]** |
| C6 | scx_governance/main.md | 491-492 | q_min = 1−K_pub/K_total is asserted, not derived | q_min = p_min·r_min·(1−K_pub/K_total); p_min, r_min must be stated |

### STRUCTURAL GAPS

| # | Gap | Priority | Status |
|---|-----|----------|--------|
| G1 | Governance↔SCX detection rate bridge | P1 | No formal mapping between governance Hoeffding bounds and core Theorem 1/4 |
| G2 | CEC critical value |E|* based on wrong equilibrium condition | P0 | All downstream results (Theorem 2, corollaries) inherit the Δ(|E|) ≥ λ−κ error |
| G3 | q_min calibration not derivable from A1-A12 | P2 | Requires new assumption A13 about auditor coverage |

---

## 8. Recommendations

### Immediate (P0)

1. **Fix NPE Theorem 1 conditions.** The corrected condition Δ(|E|) ≥ −λ makes (A,...,A) a NE under far weaker conditions than claimed. This changes the interpretation of the "CEC critical value" — it may not exist as a threshold at all (if Δ(|E|) starts positive, which it typically does). The "self-reinforcing" narrative may still hold qualitatively but the quantitative justification collapses.

2. **Fix the M* explicit solution** by adding the (1−ρ̄) factor and stating the existence condition formally as part of Theorem 1.

### Important (P1)

3. **Derive q_min properly** or add explicit calibration parameters p_min and r_min to Assumptions A1-A12.

4. **Add the governance↔SCX bridge lemma.** Without it, the NPE paper's appeal to Theorem 4 remains unjustified.

### Nice-to-Have (P2)

5. **Re-derive all downstream NPE results** (CEC critical value, stability margin, first-mover advantage decay, NPT analogy thresholds) using the corrected equilibrium condition.

6. **Unify the 2-player and N-player treatments** of Δ_A to eliminate the κ-difference inconsistency.

---

## 9. Conclusion

The game-theoretic core of the SCX framework — NPE Theorem 1 — contains **uncorrected algebraic errors** in the current source files, despite AUDIT_STATUS.md claiming they were "reconstructed from first principles." The M* equation's explicit solution is missing a factor of (1−ρ̄). The q_min calibration is an assertion, not a derivation. The governance↔SCX detection-rate bridge is a P1 structural gap.

**The claim that "unanimous adoption is a strictly dominant Nash equilibrium" cannot be verified from the current text.** The direction of the claim (that adoption becomes dominant as CEC grows) is intuitively plausible, but the quantitative conditions are incorrect by margins of order λ + κ.

The underlying insight — that cumulative audit data creates a time-accumulated advantage favoring protocol standardization — is conceptually sound. But the formal game-theoretic execution does not meet the standard of a rigorous proof, and the claim of "verification by first-principles reconstruction" in AUDIT_STATUS.md is not supported by the current source files.

---

*Audit completed 2026-07-03. All derivations independently reconstructed.*
