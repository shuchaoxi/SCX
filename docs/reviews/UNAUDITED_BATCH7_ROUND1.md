# Batch 7 Round 1 Review — Unaudited Papers

**Date:** 2026-07-02  
**Reviewer:** SCX (automated)  
**Papers:** `goodhart_gauge.tex`, `company_valuation.tex`, `auditability_principle.tex`

---

## 1. `papers/scx_goodhart/goodhart_gauge.tex`

### Checklist Results

| Criterion | Status | Detail |
|-----------|--------|--------|
| Chinese(0) | ✅ PASS | 0 CJK characters detected |
| `\author{SCX}` | ✅ PASS | Line 63: `\author{SCX}` |
| `\textsf` | ❌ FAIL | Uses `\text{SCX}`, `\text{Cercis}`, `\text{Situs}` (lines 32–34). Should be `\textsf{SCX}`, etc. |
| `\pdfoutput=1` | ⚠️ PARTIAL | Line 2 has `\pdfoutput=1` ✓. Line 1 has bare `pdfoutput=1` (no `\`) ✗ |
| `article` | ✅ PASS | `\documentclass[11pt,a4paper]{article}` |
| no `physics`/`inputenc` | ✅ PASS | Neither package present |
| pdflatex compile | ⚠️ PARTIAL | Compiles with `-interaction=nonstopmode` → 8 pages, 276 KB PDF. Fails with `-halt-on-error` due to bare `pdfoutput=1` on line 1 |
| abstract English | ✅ PASS | Lines 70–85: English abstract (heading "Chinese Abstract." on line 87 is followed by English content — no actual Chinese) |

### Issues Found

1. **`\text{}` instead of `\textsf{}`**: Custom commands `\SCX`, `\Cercis`, `\Situs` use `\text{}` (roman). Should use `\textsf{}` (sans-serif) per house style.
2. **Bare `pdfoutput=1` on line 1**: Missing backslash. Line 1 `pdfoutput=1` is treated as document body text, causing `Missing \begin{document}` error under strict compilation. Line 2 `\pdfoutput=1` is correct.

### Verdict: **PASS WITH FIXES** — 2 issues to address.

---

## 2. `papers/scx_company_valuation/company_valuation.tex`

### Checklist Results

| Criterion | Status | Detail |
|-----------|--------|--------|
| Chinese(0) | ✅ PASS | 0 CJK characters detected |
| `\author{SCX}` | ✅ PASS | Line 73: `\author{SCX}` |
| `\textsf` | ✅ PASS | `\textsf{SCX}`, `\textsf{Yajie}`, `\textsf{Spring}`, `\textsf{Situs}`, `\textsf{Cercis}` (lines 48–52) |
| `\pdfoutput=1` | ⚠️ PARTIAL | Line 2 has `\pdfoutput=1` ✓. Line 1 has bare `pdfoutput=1` (no `\`) ✗ |
| `article` | ✅ PASS | `\documentclass[12pt,a4paper]{article}` |
| no `physics`/`inputenc` | ✅ PASS | Neither package present |
| pdflatex compile | ❌ FAIL | **Fatal:** `Missing \begin{document}` error at line 1 (bare `pdfoutput=1`). With `-halt-on-error`, no PDF produced. With `-interaction=nonstopmode`, compilation stalls/times out (300s) during longtable/font processing. |
| abstract English | ✅ PASS | Lines 78–86: English abstract |

### Issues Found

1. **Bare `pdfoutput=1` on line 1**: Same as goodhart_gauge. This is the direct cause of the compilation failure. Removing line 1 or adding a `\` should fix it.
2. **Compilation timeout**: Even with `nonstopmode`, compilation stalls. Likely cause: MiKTeX font/package installation triggered by `longtable`, `bbm`, `tikz`, or `makecell` packages. May require pre-installed packages or `-draftmode` first pass.

### Verdict: **FAIL** — Cannot compile. Fix line 1 first, then diagnose timeout.

---

## 3. `papers/scx_capstone/auditability_principle.tex`

### Checklist Results

| Criterion | Status | Detail |
|-----------|--------|--------|
| Chinese(0) | ✅ PASS | 0 CJK characters detected |
| `\author{SCX}` | ✅ PASS | Line 122: `\author{SCX}` |
| `\textsf` | ✅ PASS | Line 78: `\textsf{SCX}` |
| `\pdfoutput=1` | ⚠️ PARTIAL | Line 2 has `\pdfoutput=1` ✓. Line 1 has bare `pdfoutput=1` (no `\`) ✗ |
| `article` | ✅ PASS | `\documentclass[12pt,a4paper]{article}` |
| no `physics`/`inputenc` | ✅ PASS | Neither package present |
| pdflatex compile | ❌ FAIL | **Fatal:** `\hypersetup{}` missing closing `}` at line 42. `File ended while scanning use of \kvsetkeys`. No PDF produced. |
| abstract English | ✅ PASS | Lines 139–148: English abstract present |

### Issues Found

1. **`\hypersetup{}` missing closing brace** (lines 36–43): The `\hypersetup{...}` block never closes. A `}` is needed after `pdfsubject={...}` on line 42, before the `% ====` comment on line 43.
2. **Bare `pdfoutput=1` on line 1**: Same issue as other two papers.
3. **Broken/duplicate section headings**: Many sections have two consecutive `\section{}` commands — one with a garbled/empty title (likely stripped Chinese) followed by one with the English title. Examples:
   - Line 155: `\section{:}` then line 156: `\section{Preamble: Why the Auditability Principle Is Necessary}`
   - Line 206: `\section{Auditability Principle}` then line 207: `\section{The Auditability Principle}`
   - Line 603: `\section{}` (empty) then line 604: `\section{What This Means}`
   - Line 745: `\section{Appendix:}` then line 746: `\section{Appendix: Formal Definitions and Proof Supplements}`
   
   This pattern appears throughout and produces duplicate entries in the table of contents and section numbering. The broken (Chinese-stripped) `\section{}` commands should be removed.
4. **Garbled subsection headings**: Similar pattern in `\subsection{}` commands — e.g., `\subsection{SCXChurch-Turing}` (line 157), `\subsection{APProof}` (line 286), `\subsection{AP---}` (line 303).
5. **Empty/broken inline text**: Throughout the paper, runs of text appear as fragments (e.g., lines 135–136, 160–198, 206–218) where Chinese was apparently stripped leaving punctuation, spaces, and partial LaTeX sequences. These should be reviewed and either removed or replaced with coherent English.

### Verdict: **FAIL** — Fatal compile error. Multiple structural issues beyond the hypersetup brace.

---

## Summary

| Paper | Chinese | Author | textsf | pdfoutput | article | physics/inputenc | Compile | Abstract | **Verdict** |
|-------|---------|--------|--------|-----------|---------|-------------------|---------|----------|-------------|
| goodhart_gauge | ✅ | ✅ | ❌ | ⚠️ | ✅ | ✅ | ⚠️ | ✅ | **FIX** |
| company_valuation | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ❌ | ✅ | **FAIL** |
| auditability_principle | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ❌ | ✅ | **FAIL** |

### Common Issue Across All Three Papers
All three papers have `pdfoutput=1` (without backslash) on line 1, followed by `\pdfoutput=1` on line 2. The bare line 1 causes `Missing \begin{document}` errors. **Fix:** Remove line 1 from all three files, or add the missing `\`.

### Priority Fixes Required

1. **company_valuation.tex** — Remove bare `pdfoutput=1` on line 1. Re-test compilation.
2. **auditability_principle.tex** — (a) Add missing `}` to close `\hypersetup{}`. (b) Remove bare `pdfoutput=1` on line 1. (c) Clean up duplicate/garbled section headings. (d) Re-test compilation.
3. **goodhart_gauge.tex** — (a) Change `\text{SCX}` → `\textsf{SCX}`, etc. in custom commands. (b) Remove bare `pdfoutput=1` on line 1.
