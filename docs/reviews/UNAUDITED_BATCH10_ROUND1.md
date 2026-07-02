# UNAUDITED Batch 10 — Round 1 Review

**Date:** 2026-07-02  
**Papers Reviewed:** 3  
**Reviewer:** Hermes Agent

---

## Summary Table

| Check | Paper 1: agentic_audit | Paper 2: acad_mdta_ilh | Paper 3: audit_sword |
|-------|----------------------|------------------------|---------------------|
| Chinese chars (should be 0) | ✅ 0 | ✅ 0 | ✅ 0 |
| `\author{SCX}` | ✅ L53 | ✅ L124 | ✅ L51 |
| `\textsf` used | ❌ NOT FOUND | ❌ NOT FOUND | ❌ NOT FOUND |
| `\pdfoutput=1` | ✅ L2 | ✅ L2 | ✅ L2 |
| `article` class | ✅ | ✅ | ✅ |
| No `physics`/`inputenc` | ✅ | ✅ | ✅ |
| Raw `pdfoutput=1` on L1 | ❌ BUG (L1) | ❌ BUG (L1) | ❌ BUG (L1) |
| pdflatex compile (as-is) | ❌ FATAL | ❌ FATAL | ⚠️ Recovers (2pp PDF) |
| pdflatex compile (L1 fixed) | ❌ Brace error | ❌ Brace error | ✅ Compiles |
| Abstract present | ✅ (empty content) | ✅ (bilingual) | ❌ MISSING |
| Abstract English | ⚠️ Trivial (mostly empty) | ✅ Good | ❌ N/A |

---

## 1. `papers/scx_agentic_audit/main.tex` — Agentic Multi-Agent SCX

**736 lines. Document class: `article(12pt,a4paper)`.**

### Passes
- Zero Chinese characters (only 1 non-ASCII char: `─` U+2500 box-drawing)
- `\author{SCX}` on L53
- `\pdfoutput=1` on L2
- No `physics` or `inputenc` packages

### Fails

| # | Severity | Issue | Details |
|---|----------|-------|---------|
| 1 | 🔴 CRITICAL | Raw `pdfoutput=1` on L1 | Causes `Missing \begin{document}` fatal error. Must be removed or commented out. |
| 2 | 🔴 CRITICAL | Unmatched brace in `\honestcrit` macro (L49-50) | `\newcommand{\honestcrit}[1]{% \textcolor{red}...` — missing closing `}`. Causes `File ended while scanning use of \@argdef` fatal error even after L1 fix. |
| 3 | 🟡 MEDIUM | Missing `\textsf` | No `\textsf{}` usage anywhere in the paper. Expected for SCX branding. |
| 4 | 🟡 MEDIUM | Abstract nearly empty | Abstract (L64-71) contains only bullet placeholders: `(1) ---, SCX Information Asymmetry; (2) ...` — no substantive content. |
| 5 | 🟡 MEDIUM | `% !TEX program = xelatex` on L3 | Conflicts with pdflatex requirement. Comment to change. |

### Compilation
- **As-is:** Fatal — raw `pdfoutput=1` kills it immediately.
- **With L1 fix:** Fatal — `\honestcrit` macro missing closing brace.
- **Verdict:** ❌ Cannot compile.

---

## 2. `papers/scx_acad_mdta_ilh/main.tex` — Beyond Metaphor: ACAD + MDTA + ILH

**1073 lines. Document class: `article(11pt,a4paper)`.**

### Passes
- Zero Chinese characters (100% ASCII)
- `\author{SCX}` on L124
- `\pdfoutput=1` on L2
- No `physics` or `inputenc` packages
- Abstract present with good English content (L136-139, bilingual)

### Fails

| # | Severity | Issue | Details |
|---|----------|-------|---------|
| 1 | 🔴 CRITICAL | Raw `pdfoutput=1` on L1 | Causes `Missing \begin{document}` fatal error. |
| 2 | 🔴 CRITICAL | Unmatched braces in preamble | `\hypersetup{...` (L51-54) missing `}`; `\newtcolorbox{scxbox}[1][]{...` (L91-95) missing `}`; `\newtcolorbox{verdictbox}[1][]{...` (L96-100) missing `}`. Causes `File ended while scanning use of \kvsetkeys` fatal error. |
| 3 | 🟡 MEDIUM | Missing `\textsf` | No `\textsf{}` usage anywhere. |
| 4 | 🟡 MEDIUM | Line-count overstated | Claims "1000+" lines. Actual: 1073. Close enough but worth noting precision. |
| 5 | 🟢 LOW | `\usepackage[T1]{fontenc}` | Present but acceptable (not `inputenc`). |

### Compilation
- **As-is:** Fatal — raw `pdfoutput=1`.
- **With L1 fix:** Fatal — 3 unmatched braces in preamble (`\hypersetup`, `\newtcolorbox` ×2).
- **Verdict:** ❌ Cannot compile. Needs 4 fixes (L1 removal + 3 closing braces).

---

## 3. `papers/scx_audit_sword/main.tex` — The Audit Sword Declaration

**100 lines. Document class: `article(12pt)`.**

### Passes
- Zero Chinese characters (100% ASCII)
- `\author{SCX}` on L51
- `\pdfoutput=1` on L2
- No `physics` or `inputenc` packages
- Compiles to 2-page PDF (with one non-fatal error from raw `pdfoutput=1`)

### Fails

| # | Severity | Issue | Details |
|---|----------|-------|---------|
| 1 | 🔴 CRITICAL | Raw `pdfoutput=1` on L1 | Causes `Missing \begin{document}` error (pdflatex recovers, but error still present). |
| 2 | 🔴 CRITICAL | **No abstract** | No `\begin{abstract}...\end{abstract}` environment anywhere in the document. |
| 3 | 🟡 MEDIUM | Missing `\textsf` | No `\textsf{}` usage anywhere. |

### Compilation
- **As-is:** Produces 2-page PDF (71,964 bytes) but with `Missing \begin{document}` error from raw L1.
- **With L1 fix:** Clean compile, no errors or warnings beyond a re-run-needed label warning.
- **Verdict:** ⚠️ Compiles but with errors. After fix: ✅ clean.

---

## Consolidated Issues (All 3 Papers)

| Issue | Papers Affected |
|-------|----------------|
| Raw `pdfoutput=1` on L1 | ALL THREE |
| Missing `\textsf` usage | ALL THREE |
| Unmatched brace causing fatal compile error | Paper 1 (agentic_audit), Paper 2 (acad_mdta_ilh) |
| No abstract | Paper 3 (audit_sword) |
| Near-empty abstract | Paper 1 (agentic_audit) |
| Multiple unmatched preamble braces | Paper 2 (acad_mdta_ilh) |

---

## Recommendations

1. **All papers:** Delete or comment out raw `pdfoutput=1` on line 1 (already have correct `\pdfoutput=1` on L2).
2. **All papers:** Add `\textsf{}` usage for SCX branding (e.g., `\newcommand{\SCX}{\textsf{SCX}}`).
3. **Paper 1:** Fix `\honestcrit` macro — add closing `}` after its definition. Fill in substantive abstract content.
4. **Paper 2:** Fix `\hypersetup` (add `}` after L54 `citecolor=darkgreen`). Fix both `\newtcolorbox` definitions (add `}` after `title=` lines).
5. **Paper 3:** Add `\begin{abstract}...\end{abstract}` with English abstract content.
