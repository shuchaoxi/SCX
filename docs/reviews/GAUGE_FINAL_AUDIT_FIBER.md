# GAUGE FINAL AUDIT: `fiber_bundle.tex` — All 7 Theorems Step-by-Step

**File:** `F:/scx/papers/scx_fiber_bundle/fiber_bundle.tex`  
**Lines:** 1643 (complete)  
**Date:** 2026-07-03  
**Auditor:** Hermes Agent (subagent, rigorous theorem-level audit)  

---

## 0. Executive Summary

| Theorem | Status | Key Finding |
|---------|--------|-------------|
| Thm 1 (d₁d₀=0) | ✅ PASS | Correct telescoping sum proof |
| Thm 2 (Hodge Decomposition) | ✅ PASS | Standard result, correctly stated |
| Thm 3 (Flatness Criterion) | ⚠️ PASS with GAP | Cycle basis generation claim not proved |
| Thm 4 (∑g=0 ≠ Coulomb) | ✅ PASS | Four distinctions correctly argued |
| Thm 5 (Cercis=0) | ✅ PASS | Equivalence chain valid; harmonic condition properly added |
| Thm 6 (Cercis Gauge Invariance) | ✅ PASS | Clean proof |
| Cercis Definition (Def 5.1) | ⚠️ PASS with DISCREPANCY | Mathematically sound but does NOT match code |

**CRITICAL FINDING:** The paper claims (line 1213–1215) that its Cercis definition `C = ‖P^⊥A‖²` "agrees with" the SCX code's `Q+ηN`. This is **false**. The code's `CercisScore` in `cercis.py` computes `S(s) = Q(s) + η(t)·N(s)` where Q is based on binary expert votes (consensus disagreement count) and N is based on feature-space distances to a memory bank. These are completely different mathematical objects. The gauge-fixing computation described in the paper (solving `B^T B g = B^T A`) does not exist anywhere in the `src/scx/` codebase.

---

## 1. Theorem-by-Theorem Verification

### Theorem 1: Fundamental Identity d₁∘d₀ = 0 (lines 290–305)

**Statement:** `d₁ ∘ d₀ = C B = 0`, equivalently `im(d₀) ⊆ ker(d₁)`.

**Proof:** For any `f ∈ Ω⁰(G)` and loop `γ = (v₀ → v₁ → ... → v_k = v₀)`:
```
(d₁d₀f)_γ = Σ_{i=0}^{k-1} (f_{v_{i+1}} - f_{v_i}) = f_{v_k} - f_{v_0} = 0
```

**Verdict: ✅ PASS.** The telescoping sum argument is correct. This is the standard discrete analog of `d² = 0`. The proof does not depend on any specific graph structure — it's purely a consequence of the incidence/cycle matrix definitions. No gaps.

---

### Theorem 2: Discrete Hodge Decomposition (lines 362–382)

**Statement:**
```
Ω¹(G) = im(d₀) ⊕ ker(Δ₁) ⊕ im(d₁^T)
```
where `ker(Δ₁) = ker(d₁) ∩ ker(d₀^T)`.

**Verification:**

1. **Three subspaces defined correctly:**
   - `im(d₀)`: exact 1-forms (gradients of vertex functions) — ✅
   - `ker(Δ₁) = ker(d₁) ∩ ker(d₀^T)`: harmonic 1-forms — ✅
   - `im(d₁^T)`: coexact 1-forms — ✅

2. **Orthogonality:** The subspaces are orthogonal under the standard inner products with positive weights. Proof: `⟨d₀f, d₁^Tβ⟩ = ⟨d₁d₀f, β⟩ = 0`, and `⟨d₀f, h⟩ = ⟨f, d₀^Th⟩ = 0` for `h ∈ ker(d₀^T)`. — ✅

3. **Completeness:** This is a standard theorem from discrete exterior calculus (Lim 2020, Jiang et al. 2011). For connected graphs, `dim(ker(Δ₁)) = β₁` (the first Betti number), and the dimensions add up correctly to `m`. — ✅

4. **ker(Δ₁) = ker(d₁) ∩ ker(d₀^T):** Verified via `⟨α, Δ₁α⟩ = ‖d₀^Tα‖² + ‖d₁α‖²`. So `Δ₁α = 0` iff both terms vanish. — ✅

**Verdict: ✅ PASS.** Standard and correctly presented.

---

### Theorem 3: Flatness Criterion — Harmonic-Corrected (lines 627–660)

**Statement:** *When the harmonic component vanishes*, the following are equivalent:
- (i) `curv(γ) = 0` for all elementary quadrilateral AND triangle loops
- (ii) A is exact: `∃g: A = d₀g`
- (iii) Global gauge alignment exists

**Proof structure:**
- `(i) ⇒ (ii)`: quadrilateral + triangle loops generate full cycle space ⇒ `d₁A = 0` ⇒ `A ∈ ker(d₁)` = `im(d₀) ⊕ ker(Δ₁)`. Under vanishing harmonic hypothesis, `ker(Δ₁) = {0}`, so `A ∈ im(d₀)`.
- `(ii) ⇒ (i)`: from `d₁d₀ = 0`.
- `(ii) ⇔ (iii)`: direct algebraic manipulation.

**Verification of cycle basis claim:**

The SCX graph has N layers of K_M (complete graph on M vertices per layer), connected by M parallel parameter edges between adjacent layers.

- **Triangles within each layer:** For each configuration k and each triple of experts `{i, j, ℓ}`, the triangle `(k,i)→(k,j)→(k,ℓ)→(k,i)`. There are `N·C(M,3)` such triangles. These generate the cycle space of K_M within each layer (standard: triangles span the cycle space of a complete graph).
- **Quadrilaterals between adjacent layers:** For each adjacent config pair `(k, k+1)` and expert pair `(i, j)`, the quadrilateral `(k,i)→(k,j)→(k+1,j)→(k+1,i)→(k,i)`. There are `(N-1)·M·(M-1)/2` such undirected quadrilaterals.

**Gap identified:** The paper asserts without proof that "Together, these generate the full cycle space." While this is **plausible** (and likely true for this product-like graph structure), the paper provides no rigorous argument. A proof would need to show that the submatrix of the cycle matrix C restricted to quadrilateral + triangle rows has the same row space as the full C. For a rigorous mathematical paper, this gap should be closed with at least a sketch argument (e.g., by induction on N, using that any cycle decomposes into intra-layer and cross-layer components, and that triangles span intra-layer cycles while quadrilaterals span cross-layer ones).

**Severity: LOW.** The claim is almost certainly true, but the proof is incomplete.

**Harmonic vanishing condition:** Correctly handled. For M=1 or M=2, `β₁ = (M-1)(M-2)/2 = 0` so no harmonic component exists, and the equivalence holds unconditionally. For M ≥ 3, Theorem 5.2 provides the corrected characterization. — ✅

**Verdict: ⚠️ PASS with MINOR GAP.** The cycle basis generation claim needs justification but is almost certainly true.

---

### Theorem 4: ∑g_v = 0 Is Zero-Mode Fixing, Not Coulomb Gauge (lines 743–779)

**Statement:** The constraint `Σ_v g_v = 0` is zero-mode fixing (ensuring solution uniqueness), NOT the discrete analog of Coulomb gauge `∂_μA^μ = 0`.

**Four distinctions verified:**

1. **Different object constrained:** `Σg = 0` constrains `g ∈ Ω⁰` (gauge parameter); Coulomb constrains `A ∈ Ω¹` (gauge potential). — ✅

2. **Different mathematical type:** `Σg = 0` is algebraic (orthogonality to `1`); `d₀^TA = 0` is differential (discrete divergence). — ✅

3. **Different continuous analog:** The continuous analog of `Σg = 0` is `∫ Λ dx = 0` (fixing the integration constant), NOT `∂_μA^μ = 0`. — ✅

4. **Different role in computation:** `Σg = 0` makes the normal equations non-singular (pseudo-inverse); Coulomb gauge is never used in SCX. — ✅

**Minor textual note (line 790–792):** The paper says "The SCX solution g satisfies `B^T B g = B^T A` together with `Σg = 0`, but does not guarantee `B^T(A - Bg) = 0` (in fact the latter IS the normal equation itself, not an additional condition)." This is correct — the normal equation `B^T B g = B^T A` is equivalent to `B^T(A - Bg) = 0`, which means the residual IS divergence-free after LS gauge-fixing. But this is the normal equation condition, not Coulomb gauge (which would constrain A itself, not the residual).

**Verdict: ✅ PASS.** All four distinctions are correctly argued. This is the paper's key conceptual contribution.

---

### Theorem 5: Characterization of Cercis = 0 (lines 939–957)

**Statement:** The following are equivalent:
- (i) `C = 0`
- (ii) A is exact: `∃g: A = d₀g`
- (iii) `A ∈ im(d₀)`
- (iv) Perfect global alignment exists
- (v) `curv(γ) = 0` for all quadrilateral loops AND the harmonic component of A is zero

**Verification:**

- `(i) ⇔ (ii) ⇔ (iii)`: `C = ‖P^⊥A‖² = 0 ⇔ P^⊥A = 0 ⇔ A = PA = proj_{im(B)}(A) ⇔ A ∈ im(d₀)`. — ✅
- `(ii) ⇔ (iv)`: As in Theorem 3 proof. — ✅
- `(v)`: `C = 0 ⇒ A ∈ im(d₀) ⇒ d₁A = d₁d₀g = 0` (curvature zero) AND harmonic component automatically zero (since `im(d₀) ∩ ker(Δ₁) = {0}`). Conversely: `curv = 0 ⇒ d₁A = 0 ⇒` (by Hodge) `A = d₀f + h`. If also harmonic=0 (`h=0`), then `A = d₀f ⇒ C = 0`. — ✅

**Key subtlety verified:** The paper correctly adds "AND the harmonic component is zero" because `d₁A = 0` alone (zero curvature) does NOT guarantee `A ∈ im(d₀)` when the graph has non-trivial cycles. For example, on a graph with a single cycle, a constant assignment of 1 around the cycle has zero net curvature (the signed sum around the loop is 1-1=0 in some orientations, or more precisely, a harmonic 1-form on a cycle graph has curvature zero but is not exact). Wait — actually let me reconsider.

On a cycle graph with n vertices and n edges, `ker(d₁) = ℝ` (one cycle), `im(d₀) ≅ ℝ^{n-1}` (dimension n-1). So `dim(ker(Δ₁)) = dim(ker(d₁)/im(d₀)) = 1`. A harmonic 1-form is a constant assignment around the cycle. For such a form, `d₁h = 0` (curvature zero), but `h ∉ im(d₀)` (not exact). So `C = ‖P^⊥h‖² > 0` even though curvature is zero. The condition (v) correctly captures this by also requiring the harmonic component to vanish. — ✅

**Verdict: ✅ PASS.** All logical implications are valid. The "harmonic component zero" condition is necessary and correctly identified.

---

### Theorem 6: Gauge Invariance of Cercis (lines 917–928)

**Statement:** Under `A' = A - d₀h`, the Cercis score is invariant: `C' = C`.

**Proof:**
- Let `g*` be optimal for A. Under `A' = A - d₀h`, optimum shifts to `g'* = g* - h`.
- Then `A' - d₀g'* = (A - d₀h) - d₀(g* - h) = A - d₀h - d₀g* + d₀h = A - d₀g*`.
- So `‖A' - d₀g'*‖² = ‖A - d₀g*‖² = C`. — ✅

**Edge case check:** What if there are multiple optimal `g*` (before zero-mode fixing)? The LS problem with singular `B^T B` has a whole affine space of minimizers. But all of them produce the same residual (since `d₀(g* + c·1) = d₀g*`). The paper uses the pseudo-inverse / minimum-norm solution, which is unique. The proof works for any optimal `g*` because the residual is invariant under the zero-mode shift. — ✅

**Verdict: ✅ PASS.** Clean, correct proof.

---

## 2. Cercis Score Definition: Cross-Reference with Code

### 2.1 The Paper's Definition (Definition 5.1, lines 873–895)

```
C = R[g*] = Σ_e ‖A_e - (d₀g*)_e‖²
  = Σ_a ‖A_a - B(B^TB)^+B^T A_a‖²
  = Σ_a ‖P^⊥ A_a‖²
```

Where `P = B(B^TB)^+B^T` projects onto `im(B) = im(d₀)`, and `P^⊥ = I - P`.

This is the **residual norm after least-squares gauge-fixing** — the squared distance from the edge assignment A to the gradient subspace `im(d₀)`.

### 2.2 The Code's Definition (`cercis.py`, lines 217–464)

```python
class CercisScore:
    """S(s) = Q(s) + η(t)·N(s)"""
    
    def score(self, votes, state, memory, t):
        q = self.quality.score(votes)   # Q(s) = 1 - 2·C(s)/M
        n = self.noise.score(state, memory)
        eta_t = self._schedule.eta(t)
        s = q + eta_t * n
        return s
```

Where:
- `Q(s)` = consensus quality from binary expert votes `v_m(s) ∈ {0,1}`: `Q = 1 - 2·(disagreement_count)/M` (from `ConsensusQualityScore` in `valuation/base.py`)
- `N(s)` = novelty/noise score from state features vs memory bank (from `NoveltyNoiseScore`)
- `η(t)` = time-varying weight schedule

### 2.3 The Discrepancy

| Aspect | Paper Definition | Code Definition |
|--------|-----------------|-----------------|
| Input data | `A_e = x̃_i^k - x̃_j^k` (continuous displacements in ℝ^d) | `v_m(s) ∈ {0,1}` (binary votes) + state features |
| Computation | Solve `B^TBg = B^TA`, compute residual | Compute consensus fraction + feature distances |
| Mathematical object | Squared distance to `im(d₀)` | Weighted sum of quality score and novelty score |
| Output | Scalar ≥ 0 (unbounded) | Scalar in [0, 1] |

**These are completely different computations producing different mathematical objects.** The paper's claim (line 1213–1215):

> "This paper unifies them as the residual norm C = ‖P^⊥A‖², which agrees with (b) [Q+ηN] and is not confused with (a)."

...is **incorrect**. There is no mathematical relationship, equivalence, or "agreement" between `‖P^⊥A‖²` (a least-squares residual on pairwise displacement data) and `Q + ηN` (a consensus-quality-plus-novelty score on binary votes and feature vectors).

### 2.4 Gauge-Fixing Code: Absent from Codebase

A search of `src/scx/` for any gauge-fixing computation (incidence matrices, Laplacian solves, `B^T B g = B^T A`, pairwise displacements) found **zero matches**. The paper describes a computational pipeline (Algorithm 1, lines 1077–1134) that does not exist in the actual SCX codebase.

**Verdict: ⚠️ DISCREPANCY.** The paper's Cercis definition is mathematically sound as a standalone definition, but it does NOT match the SCX code. The paper's claim of agreement with the code's Q+ηN is false.

---

## 3. Additional Findings

### 3.1 PES Misalignment Theorem (lines 664–678)

Not counted among the 7 main theorems but related to Theorem 3. States: if `curv(γ) ≠ 0` for some elementary loop, then no vertex potential can simultaneously zero all expert edge assignments.

**Verification:** If `curv ≠ 0`, then `d₁A ≠ 0`. If `A = d₀g` were possible, then `d₁A = d₁d₀g = 0`, contradiction. — ✅

### 3.2 Topological Triviality (Section 6, lines 989–1064)

All claims are correct:
- `G ≅ ℝ^{Md}` is contractible → `π_k(G) = 0` → ✅
- `X ⊂ ℝ^K` is contractible → `H^k(X;ℝ) = 0` for `k>0` → ✅
- `BG` weakly contractible → `[X, BG] = {*}` → ✅
- All Chern classes vanish → ✅
- Content is geometric (flat vs. non-flat A), not topological → ✅ correct interpretation

### 3.3 LaTeX Issues (confirmed from prior audit)

These are mechanical issues, not mathematical:
- Line 1: bare `pdfoutput=1` (should be `\pdfoutput=1` or deleted)
- 6 undefined commands: `\im`, `\curv`, `\dif`, `\bun`, `\base`, `\diag` — all need `\DeclareMathOperator` or `\newcommand` in preamble

---

## 4. Verdict Summary

| # | Theorem/Definition | Grade | Notes |
|---|-------------------|-------|-------|
| 1 | d₁d₀ = 0 | ✅ A | Standard, correct proof |
| 2 | Hodge Decomposition | ✅ A | Standard, correctly stated |
| 3 | Flatness Criterion | ⚠️ B+ | Cycle basis claim unproven but likely true |
| 4 | ∑g=0 ≠ Coulomb | ✅ A+ | Key contribution, four correct distinctions |
| 5 | Cercis = 0 | ✅ A | Correct equivalence chain with harmonic condition |
| 6 | Cercis Gauge Invariance | ✅ A | Clean, correct proof |
| 7 | Cercis Definition | ⚠️ C | Mathematically sound but does NOT match code |

### Mathematical Soundness: A-
All mathematical reasoning within the paper is internally consistent and largely correct. The only gap is the unproven cycle basis generation claim in Theorem 3, which is minor.

### Code Alignment: D
The paper's central claim that its Cercis definition "agrees with" the SCX code is false. The code's `CercisScore` computes `Q + ηN` (consensus quality + novelty), which is entirely unrelated to the gauge-fixing residual norm `‖P^⊥A‖²`. Furthermore, the gauge-fixing computation described in the paper does not exist in the codebase.

### Recommendation
1. **Fix the code-alignment claim:** Either (a) remove the claim that `‖P^⊥A‖²` "agrees with" `Q+ηN`, or (b) implement the gauge-fixing pipeline in the code and use the residual norm as one component of the Cercis score.
2. **Prove the cycle basis claim:** Add a brief proof or citation showing that quadrilateral + triangle loops generate the full cycle space of the SCX graph.
3. **Fix LaTeX issues:** Add the 6 missing command definitions and fix line 1.
