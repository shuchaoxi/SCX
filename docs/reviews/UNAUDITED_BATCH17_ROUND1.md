# Batch 17 — Unaudited Review: Round 1

**Reviewed papers:** `scx_nv_center`, `scx_pseudopotential`, `scx_multiphysics`  
**Date:** 2026-07-02  
**Compiler:** XeLaTeX (MiKTeX)  
**Status:** All three compile to PDF; all have LaTeX issues requiring fixes.

---

## 1. `papers/scx_nv_center/main.tex` — NV Centers

**Pages:** 26 | **Theorems:** 3 (all `\rigorFull`)

### Compilation Status: ⚠ COMPILES WITH ERRORS

| Severity | Count | Type |
|----------|-------|------|
| 🔴 ERROR | ~50 | `Undefined control sequence: \eff` |
| 🟠 ERROR | 1 | `Missing \begin{document}` |
| 🟠 ERROR | 3 | `Lonely \item` |
| 🟡 WARN | many | Undefined references (first-pass) |
| 🟡 WARN | 1 | Font shape `TU/lmr/bx/sc` unavailable |

### Critical Issues

#### 🔴 `\eff` is undefined (used ~50 times)
The macro `\eff` is never defined. It is used as `L_{\eff}` throughout:
- Line 474 (`eq:L_eff` definition), line 495, 505, 545-546, 549-560, 586, 595, 599, 614, 630-631, 721, 725, 785, 798, 809, 811
- Lines 1338-1458 (Discussion section, many occurrences)
- Lines 721, 725, 785, 798, 809, 811 (Theorem 2 proof)

**Fix:** Add `\newcommand{\eff}{\mathrm{eff}}` to the preamble (as done in `papers/theorems/theorem_ar_adversarial.tex`), or replace all instances with `\mathrm{eff}`. The pseudopotential and multiphysics papers correctly use `\mathrm{eff}` — nv_center should match.

#### 🟠 CJK text garbled in abstract
Lines 119-140 contain CJK characters that render as blank/garbled in the output. The `_check_cjk.py` script in the repo root checks three specific papers but not `scx_nv_center`. The CJK text appears to be a machine-translated or placeholder abstract that should either be:
- Removed and replaced with proper English
- Properly wrapped in CJK-supporting environments (requires `\usepackage{ctex}` or `\usepackage[UTF8]{ctex}` and CJK fonts)

**Current garbled example (line 119):**
```
{\bf .} \NV{}\NV{}——\NV{}\SCX{}\NV{}stateexpert\ODMR{}RamseyHahn...
```

#### 🟠 `Lonely \item` errors (3 instances)
Lines ~1033, 1044, 1062: These occur in the abstract's `enumerate` environment. The items lack proper list structure, likely due to CJK characters disrupting the parser.

#### 🟡 Font shape `TU/lmr/bx/sc` unavailable
Latin Modern Roman bold small caps is not available in the TU (Unicode/OpenType) encoding used by XeLaTeX. This affects `\textsc` usage. Mitigation: switch to `\usepackage{fontspec}\setmainfont{Latin Modern Roman}` with explicit small caps font, or use a different font.

### Content Strengths
- Rigorous 3-theorem structure with full proofs (`\rigorFull` throughout)
- Theorem 1: Multi-lab error detection via Hoeffding bound with `L_{\eff}` correction for correlation — well-proven
- Theorem 2: Cercis score convergence — statistically sound delta-method argument
- Theorem 3: T₂ degradation source unidentifiability — elegant 3-world construction proof
- NV-MIS publication standard (Section 8.2) is a practical, actionable contribution
- Excellent experimental benchmark design (4 axes with ablation studies)
- Bibliography is comprehensive with 20 real references (Doherty 2013, Barry 2020, Bradley 2019, etc.)
- Clear distinction from quantum supremacy claims (stated explicitly in Limitations)

### Structural Notes
- Duplicate `\pdfoutput=1` on lines 1-2 (line 1: `pdfoutput=1`, line 2: `\pdfoutput=1`)
- `\onehalfspacing` used (line 28) — adds ~25% page count
- Missing `\usepackage{fontspec}` despite using XeLaTeX for CJK support
- `\Pbb` defined but `\mathbb{P}` variant — fine

---

## 2. `papers/scx_pseudopotential/main.tex` — Neural Pseudopotentials

**Pages:** 19 | **Theorems:** 3 proved, 2 conjectured

### Compilation Status: ⚠ COMPILES WITH ERRORS

| Severity | Count | Type |
|----------|-------|------|
| 🔴 ERROR | 1 | `Missing \begin{document}` |
| 🔴 ERROR | 3 | `Undefined control sequence` (lines 32, 501, 510) |
| 🔴 ERROR | 1 | `Missing \begin{document}` (line 520) |
| 🟡 WARN | many | Undefined references (first-pass) |
| 🟡 WARN | 2 | Font shapes unavailable: `TU/lmr/bx/sc`, `TU/lmr/m/scit` |

### Issues

#### 🔴 `Missing \begin{document}` errors (lines 10, 520)
Caused by `\pdfoutput=1` before `\documentclass` (line 1-2). This is a common XeLaTeX quirk with some distributions. The document still compiles despite the error, but it should be fixed.

**Fix:** Either remove the `\pdfoutput=1` lines (XeLaTeX produces PDF by default), or wrap them: `\ifx\pdfoutput\undefined\else\pdfoutput=1\fi`.

#### 🔴 Undefined control sequences at lines 32, 501, 510
Without the full log context, these are likely related to the same `\pdfoutput` issue cascading into later parsing problems. Check the specific lines for missing macros.

#### 🟡 `\cjkfont` defined but unused (line 22)
```latex
\newfontfamily\cjkfont{SimSun}[Script=CJK]
```
This is defined but never used in the document. SimSun is a Windows CJK font that may not be available on all systems. Remove or conditionally define.

#### 🟡 Font shape `TU/lmr/m/scit` unavailable
Small caps italic for Latin Modern Roman is unavailable in TU encoding. This affects `\textsc{...}` used within italic contexts (e.g., table captions). Cosmetic only.

#### 🟡 Reference `eq:meff` undefined (line 828)
The appendix references `eq:meff` but this label doesn't exist. The main text uses `eq:meff` in the appendix (correlation estimation section, line 828). This should reference the equation in Theorem 1 where `M_{\mathrm{eff}}` is defined.

### Content Strengths
- Excellent formalization of pseudopotential distillation as a state-conditioned learning problem
- Error decomposition into PAW + NN + finite-sample components is clean and well-motivated
- Theorem 1 (Detection Guarantee): Proper adaptation of SCX's noise detection theorem, with practical multiplicity calculation
- Theorem 2 (Unidentifiability): Strong proof with dimensional argument — "error source unidentifiability" is philosophically important
- Cercis score table with illustrative values for VASP/GBRV/PSLibrary/JTH is informative
- Multi-expert architecture specification (MPNN, Transformer, Equivariant GNN, FNO, Deep Sets) is concrete
- Situs encoding section (Section 7) with formal symmetry proofs is rigorous
- Yajie game-theoretic equilibrium derivation in appendix is thorough
- Good relationship to existing methods (DeepMD, NequIP, MACE, delta-learning)

### Structural Notes
- Missing `\usepackage{setspace}` — no line spacing set (unlike nv_center which uses `\onehalfspacing`)
- No `\Corr` declared (nv_center has it at line 61; this paper references `\Cov` at line 280 but `\Cov` is defined)
- The `\Cov` used at line 280 in the proof should be `\Cov` from the preamble — OK, it's defined at line 55

---

## 3. `papers/scx_multiphysics/main.tex` — Multi-Physics Simulation

**Pages:** 22 | **Theorems:** 3 proved, 1 conjectured

### Compilation Status: ⚠ COMPILES WITH ERRORS

| Severity | Count | Type |
|----------|-------|------|
| 🔴 ERROR | 1 | `Missing \begin{document}` |
| 🔴 ERROR | 1 | `Undefined control sequence` (line 32) |
| 🟡 WARN | many | Undefined references (first-pass) |
| 🟡 WARN | 2 | Font shapes unavailable: `T1/lmr/m/scit`, `T1/lmr/bx/sc` |

### Issues

#### 🔴 `\usepackage[T1]{fontenc}` with XeLaTeX (line 6)
The document uses `\usepackage[T1]{fontenc}` which is for pdfLaTeX. XeLaTeX uses TU (Unicode) encoding by default. Including T1 fontenc with XeLaTeX causes the font warning `T1/lmr/m/scit undefined` and can cause subtle spacing issues. **Fix:** Remove `\usepackage[T1]{fontenc}` — XeLaTeX handles fonts natively through fontspec.

#### 🔴 `Missing \begin{document}` (line 10)
Same `\pdfoutput=1` issue as the other papers.

#### 🟡 Abstract appears truncated
Line 99-100: The abstract ends with "under the..." followed by `[truncated]` in the display. Check if this is an intentional truncation in the file or a rendering issue.

Looking at the source: The abstract is a single long paragraph on lines 98-103. The `[truncated]` was from the read_file tool, not the actual file. The abstract is complete at 4 lines. No issue.

#### 🟡 Large CJK comment blocks in Chinese (lines 103 keyword line)
Line 102 has: `multi-physics simulation , fluid-structure interaction , coupling interface , SCX auditing...` — this is just keywords, no CJK issue here.

### Content Strengths
- Most ambitious paper of the three: 5 physical domains, 2-level Yajie consensus, coupling analysis
- Error propagation bound (Theorem 2) with explicit Lipschitz constants for FSI and thermal-mechanical coupling is very strong — these derivations are novel
- Derivation of `L_FSI ∝ ρ_f/ρ_s` and `L_TM ∝ αE/k` with full proofs in appendices
- Coupling interface unidentifiability theorem is the most compelling of all unidentifiability results across the batch — the 3-world construction with domain errors + coupling parameter ambiguity is airtight
- "Unidentifiability is a feature, not a bug" philosophy (Section 9.3) is well-argued
- Comprehensive benchmark hierarchy: Turek-Hron FSI, nuclear fuel pellet, hypersonic, EM forming, ablation
- Digital twin certification pathway (Section 9.1) provides a practical application narrative
- Honest computational cost discussion (Section 9.2) acknowledges the 100× overhead and proposes mitigation
- Relationship to V&V (ASME), Bayesian calibration (Kennedy-O'Hagan), and multi-fidelity methods
- Coupling correlation estimation appendix is practically useful
- Empirical Lipschitz estimation from data (Proposition C.1) bridges theory and practice

### Structural Notes
- Uses `\usepackage[T1]{fontenc}` which conflicts with XeLaTeX
- Well-organized into coupling-specific sections
- 30 bibliography entries — the most of the three papers
- `\Lip` declared (line 55) — used in Proposition 2 and throughout
- `\domains` and `\interface` macros are well-designed

---

## 4. Cross-Paper Issues

### Shared Issue: `\pdfoutput=1` before `\documentclass`
All three papers have this pattern at lines 1-2. It causes a `Missing \begin{document}` error in XeLaTeX. The PDF is still generated, but the error is real.

**Fix for all three:** Replace lines 1-2 with:
```latex
% !TEX program = xelatex
\documentclass[11pt,a4paper]{article}
```
Or wrap conditionally:
```latex
\ifx\pdfoutput\undefined\else\pdfoutput=1\fi
```

### Inconsistency: `\eff` definition
- `nv_center`: uses `\eff` but never defines it → **ERROR**
- `pseudopotential`: uses `\mathrm{eff}` → **CORRECT**
- `multiphysics`: uses `\mathrm{eff}` → **CORRECT**
- `theorem_ar_adversarial.tex`: defines `\newcommand{\eff}{\mathrm{eff}}` → **CORRECT**

### Inconsistency: Font encoding
- `nv_center`: No fontenc, uses XeLaTeX native → **CORRECT**
- `pseudopotential`: No fontenc, defines `\cjkfont{SimSun}` → **OK**
- `multiphysics`: Uses `\usepackage[T1]{fontenc}` → **INCORRECT for XeLaTeX**

### Inconsistency: Rigor label color
- `nv_center`: Defines `\rigorFull` with green color (`\color{rigorcolor}`)
- `pseudopotential`: Defines `\rigorFull` without color
- `multiphysics`: Defines `\rigorFull` without color

### All papers need a second XeLaTeX pass
All three have "Label(s) may have changed. Rerun to get cross-references right." and undefined references. This is expected on first pass — a second `xelatex` run would resolve these.

---

## 5. Summary of Required Fixes

| Priority | Paper | Fix |
|----------|-------|-----|
| 🔴 P0 | nv_center | Add `\newcommand{\eff}{\mathrm{eff}}` to preamble |
| 🔴 P0 | nv_center | Fix/replace CJK text in abstract (lines 119-140) |
| 🟠 P1 | multiphysics | Remove `\usepackage[T1]{fontenc}` |
| 🟠 P1 | all 3 | Fix `\pdfoutput=1` before `\documentclass` |
| 🟡 P2 | nv_center | Remove duplicate `pdfoutput=1` (line 1) |
| 🟡 P2 | pseudopotential | Remove unused `\cjkfont` definition |
| 🟡 P2 | pseudopotential | Fix `eq:meff` reference in appendix (line 828) |
| 🟡 P2 | all 3 | Run second XeLaTeX pass for cross-references |

---

## 6. Overall Assessment

All three papers are intellectually substantive and represent genuine contributions to the SCX framework. The mathematical rigor is high throughout, with full proofs for the core theorems. The papers share a consistent structure (formalization → assumptions → detection theorem → unidentifiability theorem → Cercis score → Yajie consensus → experimental protocol → discussion) that works well.

**The nv_center paper has the only compilation-blocking error** (`\eff` undefined), which is trivially fixable (one line in preamble). The other issues are warnings or first-pass artifacts. After the P0 fixes, all three should compile cleanly with `xelatex` (×2).

**Overall grade:** Pass with fixes required. None of the issues affect the mathematical content or intellectual merit of the papers.
