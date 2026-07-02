# Batch 4 Review — Round 1

**Reviewed:** 2026-07-02  
**Papers:** 3 (protein_folding, galois, galois_falsifiability)  
**Status:** UNAUDITED — DO NOT COMMIT

---

## Quick Summary

| Check | protein_folding | galois | galois_falsifiability |
|---|---|---|---|
| Chinese characters | 0 ✅ | 0 ✅ | 0 ✅ |
| `\author{SCX}` | ✅ | ✅ | ✅ |
| `\textsf` | ✅ (15 uses) | ❌ **MISSING** | ❌ **MISSING** |
| `\pdfoutput=1` | ✅ | ❌ Line 1 bare `pdfoutput=1` | ❌ Line 1 bare `pdfoutput=1` |
| `article` class | ✅ | ✅ | ✅ |
| No `physics`/`inputenc` | ✅ | ✅ | ✅ |
| pdflatex compile | ⚠️ 235 errors | ⚠️ 2 errors | ⚠️ 2 errors |
| Abstract English | ✅ | ✅ | ✅ |

---

## 1. `papers/scx_protein_folding/main.tex` (1167 lines)

### Passes
- `\pdfoutput=1` on line 5 — correct.
- `\documentclass[12pt,a4paper]{article}` — correct.
- `\author{SCX}` on line 118 — correct.
- `\textsf` used extensively (15 macro definitions: `\SCX`, `\Cercis`, `\Situs`, `\Yajie`, `\Spring`, `\pLDDT`, `\AF`, `\RF`, `\ESMF`, `\OF`, `\CASP`, `\IDR`, `\cryoEM`, `\NMRspec`, `\Xray`).
- No `\usepackage{physics}` or `\usepackage{inputenc}`.
- Abstract is in English.
- No Chinese characters found.
- Uses `babel` + `fontenc` (English-only, good).
- PDF produced (25 pages, 556 KB).

### Fails / Issues

**CRITICAL: `paralist` + `enumitem` package conflict (235 compilation errors)**
- Lines 29–30 load both `\usepackage{enumitem}` and `\usepackage{paralist}`. These packages are **incompatible** — both redefine LaTeX list internals.
- Result: **169** `Undefined control sequence` errors (all in `\enit@...` enumitem internals) + **66** `Missing number, treated as zero` errors.
- The PDF is generated but likely has rendering defects in enumerate/itemize environments.
- **Fix:** Remove `\usepackage{paralist}` (line 30). `enumitem` already provides all needed list functionality.

**MINOR: `\calD` undefined**
- Line 820 uses `\calD_{\text{cal}}` but `\calD` is never defined in the preamble.
- Standard LaTeX has `\mathcal{D}` but not `\calD`.
- Add `\newcommand{\calD}{\mathcal{D}}` to the preamble, or replace with `\mathcal{D}`.

### Verdict: NEEDS FIX (paralist conflict is severe; \calD also needs fixing)

---

## 2. `papers/scx_galois/main.tex` (594 lines)

### Passes
- `\documentclass[12pt,a4paper]{article}` — correct.
- `\author{SCX}` on line 86 — correct.
- No `\usepackage{physics}` or `\usepackage{inputenc}`.
- Abstract is in English.
- No Chinese characters found.
- PDF produced (13 pages, 270 KB).

### Fails / Issues

**CRITICAL: Missing `\textsf` (0 uses)**
- No `\textsf` anywhere in the file. The SCX paper conventions require use of `\textsf` for key terminology (SCX, Cercis, Situs, etc.).
- **Fix:** Add `\textsf` macro definitions (e.g., `\newcommand{\SCX}{\textsf{SCX}}`) and use them in the body text.

**MODERATE: Bare `pdfoutput=1` on line 1**
- Line 1: `pdfoutput=1` — missing backslash. Line 2 has correct `\pdfoutput=1`.
- The bare `pdfoutput=1` causes 2× `! LaTeX Error: Missing \begin{document}.` because LaTeX tries to typeset it as text before the preamble.
- The PDF is still produced (nonstopmode), but the errors are real.
- **Fix:** Delete line 1 (the bare `pdfoutput=1`), or change to `% pdfoutput=1` (comment).

**MINOR: `% !TEX program = xelatex` comment**
- Line 3 suggests the file was written for XeLaTeX, but it compiles under pdfLaTeX without font issues. Not a real problem, just a stale editor directive.

### Verdict: NEEDS FIX (missing \textsf; bare pdfoutput=1 on line 1)

---

## 3. `papers/scx_galois_falsifiability/main.tex` (637 lines)

### Passes
- `\documentclass[12pt,a4paper]{article}` — correct.
- `\author{SCX}` on line 93 — correct.
- No `\usepackage{physics}` or `\usepackage{inputenc}`.
- Abstract is in English.
- No Chinese characters found.
- PDF produced (15 pages, 293 KB).

### Fails / Issues

**CRITICAL: Missing `\textsf` (0 uses)**
- Same issue as `galois` — no `\textsf` anywhere.
- **Fix:** Add `\textsf` macro definitions and use them.

**MODERATE: Bare `pdfoutput=1` on line 1**
- Line 1: `pdfoutput=1` — same bug as `galois`. Causes 2× `Missing \begin{document}` errors.
- **Fix:** Delete line 1 or comment it out.

**MINOR: `% !TEX program = xelatex` comment**
- Same stale editor directive as `galois`. Not a real issue for pdflatex compilation.

### Verdict: NEEDS FIX (missing \textsf; bare pdfoutput=1 on line 1)

---

## Compilation Results

| Paper | Errors | Warnings | PDF pages | PDF size |
|---|---|---|---|---|
| protein_folding | 235 (169 Undefined + 66 Missing number) | many | 25 | 556 KB |
| galois | 2 (Missing \begin{document}) | some | 13 | 270 KB |
| galois_falsifiability | 2 (Missing \begin{document}) | some | 15 | 293 KB |

All three produce PDFs under `-interaction=nonstopmode`, but all three have **real compilation errors** that should be fixed before commit.

---

## Required Fixes (Priority Order)

1. **protein_folding:** Remove `\usepackage{paralist}` (line 30) — eliminates 235 errors.
2. **protein_folding:** Define `\calD` or replace with `\mathcal{D}`.
3. **galois:** Add `\textsf` macro definitions and usage.
4. **galois_falsifiability:** Add `\textsf` macro definitions and usage.
5. **galois:** Fix/remove bare `pdfoutput=1` on line 1.
6. **galois_falsifiability:** Fix/remove bare `pdfoutput=1` on line 1.
