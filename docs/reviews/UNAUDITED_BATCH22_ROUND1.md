# Batch 22 Review — Round 1 (UNAUDITED)

**Reviewer:** Hermes Agent  
**Date:** 2026-07-02  
**Files reviewed:**
- `papers/scx_curation/main.tex` (198 lines)
- `papers/scx_method/main.tex` (221 lines)
- `papers/scx_review/main.tex` (657 lines)

**Review criteria:** Chinese(0), `\author{SCX}`, `\textsf`, `\pdfoutput=1`, `article`, no `physics`/`inputenc`, pdflatex, `abstract`

---

## 1. papers/scx_curation/main.tex

| Criterion         | Status    | Details |
|-------------------|-----------|---------|
| Chinese(0)        | ✅ PASS   | No Chinese characters detected |
| `\author{SCX}`    | ✅ PASS   | Line 24: `\author{SCX}` |
| `\textsf`         | ❌ **FAIL** | No `\textsf` command found anywhere in the file |
| `\pdfoutput=1`    | ⚠️ PASS (bug) | Line 2: `\pdfoutput=1` is present, but line 1 has a bare `pdfoutput=1` (missing backslash) which triggers `! LaTeX Error: Missing \begin{document}.` |
| `article`         | ✅ PASS   | Line 3: `\documentclass[12pt,a4paper]{article}` |
| no physics/inputenc | ✅ PASS | Uses `T1{fontenc}`, `amsmath`, `amssymb`, `amsthm`, `bm`, `graphicx`, `booktabs`, `multirow`, `enumitem`, `xcolor`, `hyperref`, `geometry` — no `physics` or `inputenc` |
| pdflatex          | ⚠️ PARTIAL | Compiles and produces 9-page PDF (main.pdf, 260 KB). However: (a) line 1 bare `pdfoutput=1` causes `Missing \begin{document}` error; (b) 3 undefined citation warnings (`sambasivan2021`, `northcutt2021`, `xi2025fundamental`) |
| `abstract`        | ✅ PASS   | Lines 31–33: `\begin{abstract}...\end{abstract}` |

---

## 2. papers/scx_method/main.tex

| Criterion         | Status    | Details |
|-------------------|-----------|---------|
| Chinese(0)        | ✅ PASS   | No Chinese characters detected |
| `\author{SCX}`    | ✅ PASS   | Line 27: `\author{SCX}` |
| `\textsf`         | ❌ **FAIL** | No `\textsf` command found anywhere in the file |
| `\pdfoutput=1`    | ⚠️ PASS (bug) | Line 2: `\pdfoutput=1` is present, but line 1 has bare `pdfoutput=1` causing same `Missing \begin{document}` error |
| `article`         | ✅ PASS   | Line 3: `\documentclass[12pt,a4paper]{article}` |
| no physics/inputenc | ✅ PASS | Same packages as curation + no `physics`/`inputenc` |
| pdflatex          | ⚠️ PARTIAL | Compiles and produces 12-page PDF (main.pdf, 277 KB). Issues: (a) `Missing \begin{document}` from bare line 1; (b) 3 missing figure files (`figures/cross_domain_comparison.pdf`, `figures/two_layer_tsne.pdf`, `figures/fmax_vs_test_error.pdf`); (c) undefined citation warnings |
| `abstract`        | ✅ PASS   | Lines 34–36: `\begin{abstract}...\end{abstract}` |

---

## 3. papers/scx_review/main.tex

| Criterion         | Status    | Details |
|-------------------|-----------|---------|
| Chinese(0)        | ✅ PASS   | No Chinese characters detected |
| `\author{SCX}`    | ✅ PASS   | Line 56: `\author{SCX}` |
| `\textsf`         | ❌ **FAIL** | No `\textsf` command found anywhere in the file |
| `\pdfoutput=1`    | ⚠️ PASS (bug) | Line 2: `\pdfoutput=1` is present, but line 1 has bare `pdfoutput=1` causing same `Missing \begin{document}` error |
| `article`         | ✅ PASS   | Line 13: `\documentclass[twocolumn]{article}` |
| no physics/inputenc | ✅ PASS | Uses `amsmath`, `amssymb`, `amsthm`, `graphicx`, `geometry`, `hyperref`, `booktabs`, `microtype`, `xcolor`, `enumitem`, `caption`, `subcaption`, `framed` — no `physics` or `inputenc`. Note: also missing `fontenc` (different from other two papers) |
| pdflatex          | ⚠️ PARTIAL | Compiles and produces 13-page PDF (main.pdf, 364 KB). `Missing \begin{document}` from bare line 1. Otherwise clean (24 warnings total, mostly citation/label rerun warnings). Two separate `thebibliography` blocks — second block for SCX-internal refs may be intentional. |
| `abstract`        | ✅ PASS   | Lines 62–65: `\begin{abstract}...\end{abstract}` (inside `\twocolumn[...]` wrapper) |

---

## Issues Summary

### Critical (all three papers)

1. **Missing `\textsf`**: None of the three papers contain the `\textsf` command. This is required per the review criteria. 
   - **Recommended fix:** Add `\renewcommand{\familydefault}{\sfdefault}` to the preamble, or use `\textsf{...}` somewhere in the document (e.g., in the title or a section heading).

### Warning (all three papers)

2. **Bare `pdfoutput=1` on line 1**: All three papers have an unescaped `pdfoutput=1` (missing backslash) as the very first line before `\documentclass`. This is technically outside the preamble and triggers `! LaTeX Error: Missing \begin{document}.` Although pdflatex continues with `-interaction=nonstopmode` and produces usable PDFs, this is an actual LaTeX error that should be fixed.
   - **Recommended fix:** Delete line 1 from all three files (the correct `\pdfoutput=1` on line 2 suffices).

### Informational

3. **Missing figures** (method only): `figures/cross_domain_comparison.pdf`, `figures/two_layer_tsne.pdf`, `figures/fmax_vs_test_error.pdf` are referenced but not present. Expected if figures are generated separately.
4. **Undefined citations**: All three papers have undefined citations on first pass — normal for one-pass pdflatex; a second pass (`bibtex` + two `pdflatex` runs) would resolve these.

---

## Verdict

| Paper                 | `\textsf` | Other Blockers | Overall  |
|-----------------------|:---------:|:--------------:|:--------:|
| scx_curation/main.tex | ❌        | ⚠️ bare pdfoutput=1 | FAIL |
| scx_method/main.tex   | ❌        | ⚠️ bare pdfoutput=1 | FAIL |
| scx_review/main.tex   | ❌        | ⚠️ bare pdfoutput=1 | FAIL |

All three papers fail on the `\textsf` requirement. Once `\textsf` is added and line 1 (bare `pdfoutput=1`) is removed, all other criteria are satisfied.
