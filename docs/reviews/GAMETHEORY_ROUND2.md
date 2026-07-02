# Game Theory Round 2 Verification: All 21 Fixes + Cascading Errors

**Date:** 2026-07-03
**Scope:** Second-round deep verification of `yajie_protocol/main.md` (NPE Theorem 1 + cascades) and `scx_governance/main.md` (M*, q_min)
**References:** `GAMETHEORY_FINAL_AUDIT.md`, `GAMETHEORY_INVENTORY.md`, `AUDIT_STATUS.md`

---

## Executive Summary

**21 fixes claimed pushed. ~12 verified correct. 1 fix missed. 2 new cascading errors discovered — one CRITICAL.**

The AUDIT_STATUS.md claims "全部21处修正已推送" (all 21 fixes pushed). Most of the algebraic fixes ARE present in the source files. However:

1. **CRITICAL CASCADING ERROR**: Δ(|E|) is **structurally always positive** under A1–A4 — making the entire "CEC critical value" threshold narrative, the mixed-strategy region, and the five-stage lock-in model conceptually broken.
2. **2-player (D,D) NE derivation still wrong**: line 406 omits κ in π_i(A,D), giving −Δ_A ≥ 2κ instead of Δ_A ≤ 0.
3. **q_min calibration still asserted**, not derived.
4. **CEC "explicit" formula still self-referential**.

---

## Section 1: Fix Verification (Fixes 1–21)

I verified each corrected location against the current source files. Results:

| # | Fix Description | Location | Status | Notes |
|---|----------------|----------|--------|-------|
| 1 | (A,...,A) NE: Δ(|E|) ≥ −λ | line 172 | ✅ VERIFIED | Theorem statement corrected |
| 2 | Proof matches: Δ(|E|) ≥ −λ | line 198 | ✅ VERIFIED | Now consistent with statement |
| 3 | (D,...,D) NE: Δ(|E|) ≤ 0 | line 222 | ✅ VERIFIED | Was Δ ≤ −(n−1)κ |
| 4 | N-person mixed Γ: −Δ(|E|) | line 280 | ✅ VERIFIED | Was −Δ + λ − 2κ |
| 5 | 2-player mixed p*: −Δ_A/λ | line 426 | ✅ VERIFIED | Was (−Δ_A−2κ)/(λ−κ) |
| 6 | Δ_A thresholds unified (2p/Np) | lines 398, 447 | ✅ VERIFIED | Both now Δ_A ≥ −λ |
| 7 | Non-asymmetric proof | lines 238–239 | ✅ VERIFIED | Uses Δ(|E|) + κ correctly |
| 8 | Mixed indifference equation | lines 271–280 | ✅ VERIFIED | λ·p^{n−1} = −Δ(|E|) |
| 9 | Stability margin M(|E|) | line 320 | ✅ VERIFIED | M = Δ + λ (was Δ − (λ−κ)) |
| 10 | CEC critical threshold | line 311, 313 | ✅ VERIFIED | Now uses Δ = −λ |
| 11 | M* explicit formula | line 307 | ✅ VERIFIED | Now has (1−ρ̄) factor |
| 12–21 | 10 "cascading corrections" | various | ✅ MOSTLY | See Section 2 for misses |

### Key Verifications in Detail

**NPE Theorem Statement (line 172):**
```
若 Δ(|E|) ≥ −λ，则 (A, ..., A) 是纯策略纳什均衡；
若 Δ(|E|) ≤ 0，则 (D, ..., D) 是纯策略纳什均衡
```
Both conditions now match independent first-principles derivation. ✅

**NPE Proof (lines 182–222):**
The proof correctly derives both conditions. The (A,...,A) deviation payoff correctly includes −κ−λ (developer triggers fragmentation and self-cost). The (D,...,D) derivation correctly cancels −λ and reduces to Δ(|E|) ≤ 0. ✅

**M* Formula (line 307):**
```
M* = ⌈2σ̄²(1−ρ̄) log(κ/(L_B ε)) / ((δ_min − ε)² − 2σ̄² ρ̄ log(κ/(L_B ε)))⌉
```
The (1−ρ̄) factor is present. Algebraically verified: from M* = A·(1+(M*−1)C) where A = 2σ̄² log(κ/(L_Bε))/(δ_min−ε)², C = ρ̄, solving gives M* = A(1−C)/(1−AC), matching the corrected formula. ✅

---

## Section 2: Cascading Errors Discovered

### CASCADE-1 (CRITICAL): Δ(|E|) Is Structurally Always Positive

**Location:** Definition line 161, Theorem statement lines 172–176, Theorem 2 lines 294–313, Stage lock-in lines 817–826

**The Error:**

The entire NPE framework depends on Δ(|E|) being able to cross zero. The (D,...,D) NE region (Δ ≤ 0) and the mixed strategy region (−λ < Δ < 0) are predicated on Δ(|E|) potentially being negative.

But under the stated assumptions:

```
Δ(|E|) = V[θ(|E|)] − V[θ(0)] − c^adopt + c^develop + κ
```

- V[θ(|E|)] − V[θ(0)] ≥ 0 (θ(|E|) ≥ θ₀, V strictly increasing per A1)
- c^develop − c^adopt > 0 (A3: c^develop > c^adopt)
- κ > 0 (A4)

**Therefore Δ(|E|) > 0 for ALL |E| ≥ 0.** At |E| = 0: Δ(0) = c^develop − c^adopt + κ > 0.

**Consequences:**

| Affected Component | Claimed Behavior | Actual Behavior |
|---|---|---|
| (D,...,D) NE condition Δ(|E|) ≤ 0 | Crosses zero at some |E| | **Never satisfied** — (D,...,D) is NEVER a NE |
| Mixed strategy region −λ < Δ < 0 | Exists for some |E| range | **Does not exist** — Δ never below 0 |
| CEC critical value |E|* | inf{|E|: Δ(|E|) > −λ} | **|E|* = 0** — trivial since Δ(0) > 0 > −λ |
| Five-stage lock-in S₂→S₃ | Crosses threshold |E|* at t₂ | **Already crossed at t₀** — no meaningful transition |
| "全体开发均衡" in Theorem 1 | Alternative equilibrium possible | **Impossible under stated assumptions** |

**The (A,...,A) equilibrium is the UNIQUE Nash equilibrium for ALL |E| ≥ 0**, not just after some critical CEC size. This makes the "critical mass" narrative in Stage 2 of the lock-in model conceptually independent of the formal game theory.

**Possible rescue:** The paper could redefine Δ(|E|) to exclude c^develop and κ, or introduce a "baseline utility of developing" that could make Δ(|E|) negative. But as currently defined, Δ(|E|) > 0 is a theorem, not an empirical possibility.

### CASCADE-2 (MODERATE): 2-Player (D,D) Derivation Still Wrong

**Location:** Lines 403–414 (English 2-player section)

**The Error:**

The (D,D) NE derivation at line 406 writes:
```
V[θ(0)] − c^develop − 2κ − λ ≥ V[θ(|E|)] − c^adopt − λ
```

But from the payoff function (line 436): π_i(A, D) = V[θ(|E|)] − c^adopt − κ·n_D − λ. With n_D=1 (other plays D), this should be:
```
V[θ(|E|)] − c^adopt − κ − λ
```

The paper omits the −κ term from π_i(A, D), leading to the condition −Δ_A ≥ 2κ (line 412).

**Correct derivation:**
```
V[θ(0)] − c^develop − 2κ − λ ≥ V[θ(|E|)] − c^adopt − κ − λ
→ −Δ_A ≥ 0  →  Δ_A ≤ 0
```

This matches the N-person condition Δ(|E|) ≤ 0. The current line 412 says −Δ_A ≥ 2κ, which would make (D,D) even harder to satisfy than it already is. With the correction, the 2-player and N-player conditions become self-consistent (both Δ ≤ 0), though as shown in CASCADE-1, Δ ≤ 0 never holds anyway.

### CASCADE-3 (MINOR): Remaining Self-Referential CEC Formula

**Location:** Line 454

The "explicit" formula remains:
```
|E|* = (1/γ) ln((θ_∞ − θ_0)/(θ_∞ − θ(|E|*)))
```

θ(|E|*) on the right side depends on |E|*, making this an implicit equation. While the threshold condition Δ(|E|*) = −λ is now correct (using −λ instead of λ−κ), the formula hasn't been solved to an explicit closed form in terms of the primitive parameters λ, κ, V, c^adopt, c^develop, γ, θ₀, θ_∞.

A proper explicit solution would give |E|* as a function only of known parameters, not referencing itself.

---

## Section 3: Cross-Check: Theorem Statement vs. Proof

### NPE Theorem 1 (lines 167–283)

**Statement (line 172–176):** Claims five items:
1. Pure-strategy NE always exists (Δ ≥ −λ → (A,...,A); Δ ≤ 0 → (D,...,D))
2. (A,...,A) is NE iff Δ ≥ −λ
3. (D,...,D) is NE iff Δ ≤ 0
4. No asymmetric pure-strategy NE
5. Mixed strategy when −λ < Δ < 0

**Proof (lines 178–283):**

Item (ii) at lines 182–198 correctly derives Δ ≥ −λ. ✅
Item (iii) at lines 200–222 correctly derives Δ ≤ 0. ✅
Item (iv) at lines 224–249 correctly shows asymmetric NE only at Δ = −κ (measure zero). ✅
Item (v) at lines 251–283 correctly derives λ·p^{n−1} = −Δ(|E|). ✅

**Cross-check verdict:** Statement and proof are internally consistent for all five items. ✅

**But:** The proof's claim that the intermediate region −λ < Δ(|E|) < 0 contains both pure-strategy NE and a unique mixed-strategy NE is mathematically correct but **empirically vacuous** under the stated assumptions. As shown in CASCADE-1, Δ(|E|) > 0 always, so this region simply doesn't occur. The proof is formally valid but describes a parameter space that doesn't exist.

### Theorem 2 (lines 294–313)

**Statement:** Claims existence of unique CEC critical size |E|* above which (A,...,A) is the unique NE.

**Proof:** At line 311, says "全体开发均衡的条件 Δ(|E|) ≤ 0 不成立" (the all-develop condition fails because Δ > 0). The proof's logic (Δ(|E|) > −λ → (A,...,A) is unique) is correct given that Δ(|E|) > 0 excludes the other NE conditions.

**Cross-check verdict:** Proof is formally valid. But the "critical value" framing at line 299–300 ("存在唯一的CEC临界规模 |E|*") is misleading because |E|* = 0 under the current definition of Δ.

---

## Section 4: Governance M* Formula Correctness

### Derivation Verification

Self-referential form (line 300):
```
M* = ⌈2σ̄²·(1+(M*−1)ρ̄)·log(κ/(L_B·ε)) / (δ_min−ε)²⌉
```

Let A = 2σ̄²·log(κ/(L_B·ε))/(δ_min−ε)², C = ρ̄.

M* = A·(1 + (M*−1)C) = A·(1−C + M*·C)

M* = A(1−C) + A·C·M*
M*(1 − A·C) = A(1−C)
M* = A(1−C)/(1−A·C)
   = 2σ̄²(1−ρ̄)·log(κ/(L_B·ε)) / ((δ_min−ε)² − 2σ̄²·ρ̄·log(κ/(L_B·ε)))

**This matches line 307.** ✅

### Existence Condition

The formula requires denominator positive:
```
(δ_min − ε)² > 2σ̄²·ρ̄·log(κ/(L_B·ε))
```

This is correctly noted at line 311 ("valid when the denominator is positive"). However, there's an additional unstated requirement: **(1−ρ̄) must be ≤ 1**, which it is since ρ̄ ∈ [0,1]. Also, the log argument requires κ/(L_B·ε) > 1 for the log to be positive, which holds when κ > L_B·ε (penalty > minimum undetectable benefit). These edge cases should be stated explicitly.

### Numerical Example Verification (lines 390–398)

Given: L_B=1, κ=10, ε=0.01, δ_min=0.05, σ̄²=0.01, ρ̄=0.2

With corrected formula:
- Numerator: 2·0.01·(1−0.2)·log(10/(1·0.01)) = 0.02·0.8·log(1000) ≈ 0.02·0.8·6.908 = 0.1105
- Denominator: (0.05−0.01)² − 2·0.01·0.2·log(1000) = 0.0016 − 0.04·6.908 = 0.0016 − 0.02763 = −0.02603

**Denominator negative → no finite M suffices.** Conclusion matches paper. ✅

But the paper's own calculation at line 393–398 uses the uncorrected formula (numerator = 0.02·6.908 = 0.138 instead of 0.1105). The numerical result happens to agree (both negative denominator), but the arithmetic shown is for the **wrong** formula — it doesn't include (1−ρ̄) in the numerator. This is a **presentation inconsistency**: the formula on line 307 is correct, but the worked example on lines 393–398 uses the old formula.

---

## Section 5: Remaining Structural Gaps

### GAP-1: q_min Calibration (Not Fixed)

**Location:** scx_governance/main.md line 491

```
"A natural calibration is q_min = 1 − K_pub/K_total"
```

This assertion jumps from Step 3's derived bound q_j ≥ p_min·r_j·(K_total−K_pub)/K_total to the simplified q_min = 1−K_pub/K_total, which requires p_min·r_min = 1 — that every auditor detects every gap with probability 1. Neither p_min nor r_min are stated as assumptions.

**Status:** ❌ NOT FIXED. Still an assertion, not a derivation.

### GAP-2: p_h → 0 Argument (Not Fixed)

**Location:** scx_governance/main.md lines 322–330

The proof uses Chebyshev: P(|θ^G − c| > ε) ≤ (σ_G² + σ̄²/M_eff)/ε². As M → ∞, this bound → σ_G²/ε² (constant), not zero. The claim that "p_h → 0 as M → ∞" is incorrect unless σ_G = 0 (government has perfect knowledge of θ).

**Status:** ❌ NOT FIXED. The argument needs to show that the consensus variance σ̄²/M_eff → 0, making the detection probability of honest reporting decrease, not use the Chebyshev bound.

### GAP-3: Governance↔SCX Detection Bridge (Not Fixed)

**Status:** ❌ NOT FIXED. No formal lemma connects governance Hoeffding bounds to core Theorem 1/4.

---

## Section 6: Phase Description Cross-Check

### Stage S₃ Definition (line 823)

```
S₃: Moat Formation — Δ(|E|) ≥ −λ satisfied, NPE is unique NE
```

With CASCADE-1 (Δ always > 0), this condition is always satisfied. S₃ doesn't represent a meaningful phase transition — at least not one driven by the formal NPE conditions. The transition from S₂ to S₃ would need to be redefined on some other basis (e.g., accuracy gap exceeding development cost, ecosystem lock-in, regulatory recognition).

### Stage S₂ Definition (line 822)

```
S₂: Critical Mass — |E| ≥ |E|*, θ(t) − θ₀ ≥ ε_θ
```

If |E|* = 0 (CASCADE-1), then S₂ is entered immediately. The threshold ε_θ needs independent calibration. The paper doesn't specify ε_θ quantitatively.

### Stability Margin Interpretation

M(|E|) = Δ(|E|) + λ is correct and monotonically increasing with |E|. This provides a valid quantitative measure of how "strong" the (A,...,A) equilibrium is. The self-reinforcing property (Corollary 2.1) is valid. But the claim that M crosses zero at some critical |E|* is wrong — M(|E|) > λ > 0 always, so the equilibrium is always in the "stable" region.

---

## Section 7: Summary of Findings

### Verified Correct (12+ fixes)

| # | What | Where |
|---|------|-------|
| F1 | (A,...,A) NE: Δ ≥ −λ | line 172 |
| F2 | Proof consistency | line 198 |
| F3 | (D,...,D) NE: Δ ≤ 0 | line 222 |
| F4 | N-person mixed Γ: −Δ | line 280 |
| F5 | 2-player mixed p*: −Δ_A/λ | line 426 |
| F6 | Δ_A thresholds unified | lines 398, 447 |
| F7 | Non-asymmetric proof | lines 238–239 |
| F8 | Mixed indifference equation | lines 271–280 |
| F9 | Stability margin M = Δ+λ | line 320 |
| F10 | CEC threshold uses −λ | line 311 |
| F11 | M* with (1−ρ̄) factor | line 307 |
| F12 | Cascading fixes (phase desc, etc.) | various |

### New Errors Found

| # | Severity | Error | Impact |
|---|----------|-------|--------|
| **CE1** | 🔴 **CRITICAL** | Δ(|E|) always > 0 under A1–A4 | Destroys CEC threshold narrative, mixed region, and S₂→S₃ transition logic |
| **CE2** | 🟡 **MODERATE** | 2-player (D,D) derivation omits κ (line 406) | Gives wrong condition −Δ_A ≥ 2κ instead of Δ_A ≤ 0; already moot due to CE1 |
| **CE3** | 🟢 **MINOR** | M* numerical example uses old (incorrect) formula | Presentation error; correct formula gives same qualitative conclusion for those parameters |
| **CE4** | 🟢 **MINOR** | CEC explicit formula still self-referential | Line 454; condition corrected but not solved |

### Still Not Fixed (from Round 1)

| # | What |
|---|------|
| NF1 | q_min calibration: asserted, not derived |
| NF2 | p_h → 0 argument: Chebyshev bound doesn't converge to 0 |
| NF3 | Governance↔SCX bridge: no formal lemma |

---

## Section 8: Recommendations

### P0 (Immediate)

1. **Address CASCADE-1**: Either (a) redefine Δ(|E|) to allow negativity (e.g., subtract some baseline development benefit), or (b) acknowledge that (A,...,A) is the unique NE from day one and restructure the lock-in model around continuous strengthening rather than threshold crossing. The qualitative insight — that adoption becomes increasingly dominant — is salvageable; the threshold narrative is not.

2. **Fix 2-player (D,D) derivation**: Add κ to π_i(A,D) at line 406.

### P1 (Important)

3. **Fix p_h → 0 argument**: Replace Chebyshev bound with consensus variance argument.

4. **Fix M* numerical example**: Use the corrected formula in the worked example (lines 393–398).

### P2 (Nice-to-Have)

5. Derive q_min from stated assumptions or add p_min, r_min as new assumptions.

6. Solve CEC critical value to explicit closed form.

7. Add existence condition for M* as part of Theorem 1 statement.

### P3 (Structural)

8. Add governance↔SCX bridge lemma.

---

*Second-round verification completed. All algebra independently re-derived. Source files cross-checked line by line.*
