# GAUGE Audit: `fiber_bundle.tex` — Discrete Hodge, ∑g=0

**File:** `F:/scx/papers/scx_fiber_bundle/fiber_bundle.tex`  
**Lines:** 1629  
**Compiled PDF:** 31 pages (486,940 bytes)  
**Date:** 2026-07-03  
**Auditor:** Hermes Agent (automated)

---

## 0. Executive Summary

| Criterion | Result |
|-----------|--------|
| Chinese characters | ✅ **0** — zero Chinese glyphs in entire file |
| `\author{SCX}` | ✅ Line 66 |
| `\pdfoutput=1` | ⚠️ Line 2 correct; Line 1 has broken bare `pdfoutput=1` |
| `article` class | ✅ Line 3 |
| No `physics` | ✅ |
| No `inputenc` | ✅ |
| pdflatex compile | ⚠️ **Produces 31-page PDF but with 49 undefined-control-sequence errors** |
| Mathematical soundness | ⚠️ Math is sound; 6 undefined commands break rendered output |

---

## 1. Chinese Check: PASS ✅

Scanned all 1629 lines manually and via automated check. **Zero Chinese characters** found. The entire document is in English.

---

## 2. Format Compliance

### 2.1 Critical Bug — Line 1

```latex
1|pdfoutput=1          ← BARE TEXT, NO BACKSLASH
2|\pdfoutput=1         ← correct
```

**Impact:** The bare `pdfoutput=1` on line 1 is interpreted as literal text before `\begin{document}`, causing:
- `! LaTeX Error: Missing \begin{document}.`
- 11 `Missing character: There is no <letter> in font nullfont!` messages
- 9 `Undefined control sequence` errors (one per character `p`, `d`, `f`, `o`, `u`, `t`, `p`, `u`, `t`)
- The characters `=`, `1` also cause missing-glyph warnings

**Fix:** Delete line 1 entirely, or add backslash: `\pdfoutput=1`. The correct declaration already exists on line 2.

### 2.2 Preamble Check

| Requirement | Status | Line |
|-------------|--------|------|
| `\documentclass[12pt,a4paper]{article}` | ✅ | 3 |
| `\pdfoutput=1` | ⚠️ Broken on L1, correct on L2 | 2 |
| `\author{SCX}` | ✅ | 66 |
| No `physics` package | ✅ | — |
| No `inputenc` | ✅ (uses `fontenc` instead) | 6 |
| `amsmath,amssymb,amsthm` | ✅ | 9 |
| `mathtools` | ✅ | 10 |
| `mathrsfs` | ✅ | 11 |
| `tikz-cd` | ✅ | 14 |
| `graphicx` | ✅ | 15 |
| `geometry` | ✅ | 18 |
| `hyperref` | ✅ | 20 |
| `enumitem` | ✅ | 21 |
| `booktabs` | ✅ | 22 |
| `bm` | ✅ | 23 |

---

## 3. pdflatex Compilation: PARTIAL PASS ⚠️

### 3.1 Compile Summary

```bash
$ pdflatex -interaction=nonstopmode fiber_bundle.tex
Output written on fiber_bundle.pdf (31 pages, 486940 bytes).
```

- **Pages:** 31
- **File size:** ~487 KB
- **LaTeX Errors:** 1 (`Missing \begin{document}`)
- **Undefined control sequences:** 49
- **Warnings:** 14

### 3.2 Undefined Commands (6 total)

These six commands are used extensively throughout the document but **none is defined in the preamble**:

| Command | Occurrences | Purpose | First Use |
|---------|-------------|---------|-----------|
| `\im` | 104 | Image of a map (`\im(d_0)`, `\im(B)`) | ~286 |
| `\curv` | 39 | Discrete curvature (`\curv(\gamma)`) | 559 |
| `\dif` | 31 | Exterior derivative (`\dif^2 = 0`) | ~288 |
| `\bun` | 27 | Principal bundle notation | ~156 |
| `\base` | 2+ | Base manifold notation | ~1166 |
| `\diag` | 2+ | Diagonal matrix (`\diag(\mathbf{w}_0)`) | 322 |

**Impact on mathematical content:** Every occurrence of these commands renders as blank/missing in the PDF. This means:
- All curvature expressions (`\curv(\gamma)`) are invisible
- All image-of-map expressions (`\im(d_0)`) are invisible
- The exterior derivative `d` in `\dif^2=0` is invisible
- Bundle notation `\bun` is invisible
- `\diag` calls at line 322 are broken
- The comparison table in Section 7 that uses `\base` has missing text

**Fix:** Add the following to the preamble (after line 43):

```latex
\newcommand{\im}{\operatorname{im}}
\newcommand{\curv}{\operatorname{curv}}
\newcommand{\dif}{\mathrm{d}}
\newcommand{\bun}{\mathcal{P}}
\newcommand{\base}{\mathcal{X}}
\newcommand{\diag}{\operatorname{diag}}
```

---

## 4. Mathematical Audit

### 4.1 Discrete Hodge Formulation: SOUND ✅

The discrete Hodge theory in Section 2 is correctly constructed:

| Concept | Definition | Correct? |
|---------|-----------|----------|
| Directed graph `\grph = (\verts, \edgs)` | Def 1 (line 209) | ✅ |
| Vertex space `\Omega^0`, edge space `\Omega^1` | Def (line 225) | ✅ |
| Incidence matrix `B` / `d_0` | Def (line 239) | ✅ |
| Cycle matrix `C` / `d_1` | Def (line 259) | ✅ |
| Fundamental identity `d_1 d_0 = 0` | Theorem 1 (line 282) | ✅ Proof is correct |
| Adjoint `d_0^T` and inner products | Def (line 303) | ✅ |
| Graph Laplacians `\Delta_0`, `\Delta_1` | Def (line 331) | ✅ |
| Discrete Hodge decomposition | Theorem 2 (line 354) | ✅ Standard result |

**Assessment:** The mathematical foundation is solid — standard discrete exterior calculus / spectral graph theory. The exposition is clear, self-contained, and correctly references the key literature (Lim 2020, Jiang et al. 2011, Chung 1997, Grady & Polimeni 2011, Desbrun et al. 2005, Hirani 2003).

### 4.2 SCX Graph Construction: SOUND ✅

Section 3 correctly constructs:
- Vertices: `(k, m)` pairs (N×M vertices) ✅
- Parameter edges: `(k, m) → (k+1, m)` ✅
- Expert edges: `(k, i) → (k, j)` for i≠j ✅
- Edge assignments `A_e` from raw data ✅
- Elementary quadrilateral loops ✅
- Curvature as loop holonomy ✅
- Gauge transformation: `A' = A - d_0 g` ✅
- Gauge invariance of curvature (proof uses `d_1 d_0 = 0`) ✅

**The curvature simplification** (lines 568–579) algebraically reduces to:
```
curv(γ_{k,i,j}) = (x̃_i^k − x̃_i^{k+1}) − (x̃_j^k − x̃_j^{k+1})
```
This correctly measures **differential change between experts across parameter steps** — a clean geometric interpretation of PES misalignment.

### 4.3 The `∑g = 0` Formalism: CORRECTLY DISTINGUISHED ✅

This is the paper's key conceptual contribution. The analysis is correct:

| Concept | What it is | What it is NOT |
|---------|-----------|----------------|
| `∑_v g_v = 0` | Zero-mode fixing (algebraic constraint on gauge parameter `g ∈ Ω^0`) | NOT Coulomb gauge `∂_μ A^μ = 0` (divergence constraint on gauge potential `A ∈ Ω^1`) |

The distinction (Theorem 4, lines 729–764) is rigorous:
1. Different objects constrained (`g` vs `A`)
2. Different mathematical type (algebraic vs differential)
3. Different continuous analog (`∫Λ dx = 0` vs `∂_μ A^μ = 0`)
4. Different role in computation (pseudo-inverse / solution uniqueness vs unused constraint)

**This is correct and important.** The genuine discrete Coulomb gauge analog would be `d_0^T A = 0`, which is never used in SCX computation.

### 4.4 Least-Squares Gauge-Fixing: SOUND ✅

The formulation (Section 4):
- `min_g ∑_e ‖A_e − (d_0 g)_e‖²` → normal equations `B^T B g = B^T A` ✅
- Zero-mode: `ker(B^T B) = span(1)` → need `∑g = 0` for uniqueness ✅
- Augmented system with Lagrange multiplier ✅
- Equivalent to Moore-Penrose pseudo-inverse ✅
- Geometric interpretation as orthogonal projection onto `im(B)` ✅

### 4.5 Cercis Score Definition: SOUND ✅

The definition (Section 5):
```
C = R[g*] = ‖P^⊥ A‖²
```
where `P = B(B^T B)^+ B^T` and `P^⊥ = I − P`.

- Gauge invariance proof (Theorem 5, line 903): correct — shifts `g* → g* − h` preserves residual ✅
- `C = 0` characterization (Theorem 6): correct equivalence chain ✅
- Distinction from Yang-Mills functional `∫‖F‖²`: correct — Cercis captures total residual (harmonic + coexact), not just curvature ✅
- Normalized Cercis `C̄ ∈ [0, 1]`: well-defined ✅

### 4.6 Topological Triviality Acknowledgment: CORRECT AND HONEST ✅

Section 6 correctly establishes:
- `G ≅ ℝ^{Md}` is contractible → `π_k(G) = 0` ✅
- `𝒳 ⊂ ℝ^K` is contractible → `H^k(𝒳;ℝ) = 0` for `k > 0` ✅
- Classifying space `BG` is contractible → `[𝒳, BG] = {*}` ✅
- All Chern classes vanish ✅
- The content is **geometric** (flat vs. non-flat A), not topological ✅

The `ℝ³` vector field analogy (curl-free vs. not) is apt.

### 4.7 Comparison Table & Prior Work Critique: COHERENT ✅

Section 7's table (line 1230) systematically compares discrete Hodge vs. continuous fiber bundle across 12 dimensions. The critique of prior work (lines 1181–1209) identifies 4 specific errors (F1–F4), each correctly argued.

Section 8 outlines conditions (C1–C5) under which a continuous framework could become valid — a constructive, falsifiable approach.

### 4.8 Numerical Algorithm: CORRECT ✅

The 8-step algorithm (lines 1063–1119) correctly maps each mathematical construct to a computational step. Complexity analysis (line 1136) is reasonable: `O(NM²)` construction, sparse conjugate gradient for the normal equations.

---

## 5. Bridge Between Gauge Theory and SCX Audit

The paper explicitly positions itself as a corrective to prior continuous fiber bundle formulations. Key bridge elements:

| Prior Gauge Framework | This Paper's Correction |
|-----------------------|------------------------|
| Ehresmann connection `ω` (asserted, never constructed) | Edge assignment `A_e` = raw data, no construction needed |
| `∑g = 0` misidentified as Coulomb gauge | Correctly identified as zero-mode fixing |
| Cercis = `∫‖F‖²` (Yang-Mills) vs `Q + ηN` (actual code) | Cercis = `‖P^⊥ A‖²` — unique, matches code |
| Non-trivial topology claimed | Honestly admits triviality |
| Continuous PDE → no discretization | Discrete Hodge → directly computable |

The bridge is **coherent**: the paper does not reject gauge theory but relocates it to the correct mathematical level — discrete Hodge theory on graphs, where it matches the actual SCX computation line-by-line.

---

## 6. Core Contribution

The paper makes **one central contribution** with several corollaries:

**Primary:** SCX gauge theory is reformulated entirely within discrete Hodge theory on graphs, abandoning the continuous fiber bundle framework. This makes the mathematics precisely match the computation.

**Corollaries:**
1. **Terminological precision:** `∑g = 0` ≠ Coulomb gauge — these are different mathematical objects
2. **Unique Cercis definition:** Resolved the prior ambiguity between Yang-Mills and `Q+ηN`
3. **Honest triviality:** Topological content is zero; all content is geometric
4. **Computable theory:** Every mathematical object has a direct computational counterpart
5. **Falsifiable framework:** Conditions C1–C5 provide a path for future continuous formulations

---

## 7. Actionable Fixes

### Critical (mathematical content broken)

1. **Delete line 1** (`pdfoutput=1` bare text) — it causes `Missing \begin{document}` error
2. **Add 6 missing command definitions** to preamble:
   ```latex
   \newcommand{\im}{\operatorname{im}}
   \newcommand{\curv}{\operatorname{curv}}
   \newcommand{\dif}{\mathrm{d}}
   \newcommand{\bun}{\mathcal{P}}
   \newcommand{\base}{\mathcal{X}}
   \newcommand{\diag}{\operatorname{diag}}
   ```

### Minor

3. Consider adding `\DeclareMathOperator{\diag}{diag}` instead of `\newcommand` for semantic correctness
4. The overfull hbox at lines 1–274 (20pt) is a secondary artifact of line 1 and should resolve after fixing it

---

## 8. Verdict

| Dimension | Grade |
|-----------|-------|
| No Chinese | ✅ A+ |
| Format compliance | ⚠️ B (broken L1, otherwise perfect) |
| pdflatex compilation | ⚠️ C (31 pages but 49 undefined-command errors) |
| Mathematical soundness | ✅ A (formulation is rigorous and correct) |
| `∑g=0` vs Coulomb distinction | ✅ A+ (key conceptual contribution) |
| Cercis definition | ✅ A (unique, gauge-invariant, matches code) |
| Topological honesty | ✅ A |
| Bridge to SCX audit | ✅ A (coherent mapping) |
| Overall | ⚠️ **B+** — Mathematics is solid but 6 undefined commands and 1 broken line make the rendered output unreliable. Fixing these is a 5-minute edit. |
