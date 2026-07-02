# Batch 8 Review: causal_consensus + blockchain + elections — Round 1

**Date:** 2026-07-02
**Reviewer:** Hermes Agent
**Status:** UNAUDITED — Round 1 Review

---

## Quick Results Matrix

| Paper | Chinese(0) | \author{SCX} | \textsf | \pdfoutput=1 | article | No physics/inputenc | pdflatex | Abstract English | Overall |
|---|---|---|---|---|---|---|---|---|---|
| causal_consensus | PASS | PASS | **FAIL** | PARTIAL* | PASS | PASS | 15 errors | **FAIL** | ❌ |
| blockchain | PASS | PASS | PASS | PARTIAL* | PASS | PASS | 91 errors | PASS | ⚠️ |
| elections | PASS | PASS | PASS | PARTIAL* | PASS | PASS | 13 errors | PASS | ⚠️ |

> * All three papers have `pdfoutput=1` (without backslash) on line 1 before `\documentclass`, causing "Missing \begin{document}" error. The valid `\pdfoutput=1` is on line 2.

---

## 1. scx_causal_consensus/main.tex — ❌ FAIL

### Structural Checks

| Check | Result | Detail |
|---|---|---|
| Chinese(0) | **PASS** | No CJK characters detected (hex-verified, all ASCII/UTF-8 English) |
| `\author{SCX}` | **PASS** | Line 62: `\author{SCX}` |
| `\textsf` | **FAIL** | Not used anywhere in the file. The `\assumptionTag` and `\limitationTag` macros that other papers use with `\textsf` are absent |
| `\pdfoutput=1` | **PARTIAL** | Line 2 has `\pdfoutput=1` ✓. Line 1 has bare `pdfoutput=1` (no backslash), which is treated as plain text and causes "Missing \begin{document}" |
| `article` | **PASS** | Line 9: `\documentclass[11pt,a4paper,twoside]{article}` |
| No physics/inputenc | **PASS** | Neither package is included |

### Compilation (pdflatex)

- **Output:** 9 pages, 315,604 bytes — PDF produced
- **Errors: 15** (nonstopmode masks failures):
  - `! LaTeX Error: Missing \begin{document}.` (×2) — caused by line 1 `pdfoutput=1` before `\documentclass`
  - `! LaTeX Error: Unicode character 🔴 (U+1F534)` (×3) — emoji in honestbox definition (line 41) not supported by pdflatex
  - `! LaTeX Error: \begin{honestbox} on input line 259 ended by \end{document}.` — missing `\end{honestbox}`
  - `! Package natbib Error: Bibliography not compatible with author-year citations.` — natbib configuration mismatch
  - Multiple undefined citations (`scx_causal`, `pearl2009causality`, etc.) and undefined references (`sec:discussion`, `thm:consensus`, etc.)

### Abstract Quality — FAIL

The abstract (lines 67–86) is extremely fragmented, consisting of disjointed sentence fragments with missing words, incomplete phrases, and a cut-off Keywords section:

```
\noindent\textbf{Keywords:
do-calculus, 
\end{abstract}
```

The keywords list is truncated. The abstract does not constitute coherent English prose. It reads as placeholder or machine-generated fragments rather than a proper academic abstract.

### Content Quality

The entire paper is severely fragmented throughout. Sections have empty titles (`\section{}`), theorems are stated with incomplete text, proofs are sketches with missing steps, and much of the content reads as outline notes rather than finished prose. The `honestbox` environments have incomplete content.

**Verdict: FAIL** — `\textsf` missing, abstract is not proper English, 15 LaTeX errors, content is severely fragmented.

---

## 2. scx_blockchain/main.tex — ⚠️ PASS with Issues

### Structural Checks

| Check | Result | Detail |
|---|---|---|
| Chinese(0) | **PASS** | No CJK characters detected |
| `\author{SCX}` | **PASS** | Line 93: `\author{SCX}` |
| `\textsf` | **PASS** | Lines 84–85: `\newcommand{\assumptionTag}[1]{\textsf{\textbf{[A#1]}}}` and `\limitationTag` |
| `\pdfoutput=1` | **PARTIAL** | Line 2 has `\pdfoutput=1` ✓. Line 1 has bare `pdfoutput=1` (same bug as causal_consensus) |
| `article` | **PASS** | Line 4: `\documentclass[11pt,a4paper]{article}` |
| No physics/inputenc | **PASS** | Uses `fontenc` (T1) which is allowed |

### Compilation (pdflatex)

- **Output:** 25 pages, 580,377 bytes — PDF produced
- **Errors: 91** (nonstopmode masks failures):
  - `! LaTeX Error: Missing \begin{document}.` — same line 1 `pdfoutput=1` bug
  - `! LaTeX Error: \mathrm allowed only in math mode.` (×~80) — macros like `\PoW`, `\PoS`, `\PBFT`, `\Tendermint`, `\Nakamoto` all defined with `\DeclareMathOperator{\PoW}{\mathrm{PoW}}` and used outside math mode in titles, captions, and body text
  - `! Undefined control sequence.` (×3) — likely `\Cris` which is referenced but not defined
  - `! Double subscript.` (×6) — subscript syntax errors in equations

### Abstract Quality — PASS

Well-written, comprehensive English abstract that clearly states the three core theorems, the mapping to SCX framework, and keywords. Proper academic prose.

### Content Quality

Well-structured paper with 12 explicit assumptions, full proofs for all theorems, protocol analysis across PoW/PoS/PBFT, Nakamoto comparison, Cercis scoring, Spring gating, and honest limitations. High-quality academic content.

### Issues to Fix

1. **Line 1 `pdfoutput=1`**: Comment out or delete (line 2 has the correct `\pdfoutput=1`)
2. **Math-mode macros in text**: `\PoW`, `\PoS`, `\PBFT`, `\Tendermint`, `\Nakamoto` should either be used only in math mode or redefined without `\mathrm` for text-mode use
3. **Undefined `\Cris`**: Reference found but not defined
4. **Double subscripts**: Fix in affected equations

**Verdict: PASS with issues** — all structural checks pass, good content quality, but 91 LaTeX errors need fixing (mostly mechanical `\mathrm`-in-text-mode issue).

---

## 3. scx_elections/main.tex — ⚠️ PASS with Issues

### Structural Checks

| Check | Result | Detail |
|---|---|---|
| Chinese(0) | **PASS** | No CJK characters detected |
| `\author{SCX}` | **PASS** | Line 81: `\author{SCX}` |
| `\textsf` | **PASS** | Lines 75–76: `\assumptionTag` and `\limitationTag` both use `\textsf` |
| `\pdfoutput=1` | **PARTIAL** | Line 2 has `\pdfoutput=1` ✓. Line 1 has bare `pdfoutput=1` (same bug) |
| `article` | **PASS** | Line 4: `\documentclass[11pt,a4paper]{article}` |
| No physics/inputenc | **PASS** | Neither package included |

### Compilation (pdflatex)

- **Output:** 23 pages, 472,834 bytes — PDF produced
- **Errors: 13** (nonstopmode):
  - `! LaTeX Error: Missing \begin{document}.` — same line 1 `pdfoutput=1` bug
  - `! Undefined control sequence.` (×3) — likely `\Cris` reference
  - `! Double subscript.` (×7) — subscript syntax errors
  - `! Extra }, or forgotten $.` — brace/grouping error
  - `! Missing $ inserted.` — math mode issue

### Abstract Quality — PASS

Well-written English abstract clearly stating three core theorems, observer community detection, and keywords. Proper academic prose.

### Content Quality

Well-structured paper with 10 explicit assumptions, three theorems with full proofs, Yajie certification protocol, Cercis electoral integrity score, Spring gating for irregularity detection, specific applications (precinct-level, mail-in, multi-jurisdiction), and honest limitations. High-quality academic content.

### Issues to Fix

1. **Line 1 `pdfoutput=1`**: Comment out or delete
2. **Undefined control sequences**: Fix undefined macro references
3. **Double subscripts**: Fix in affected equations
4. **Brace/grouping errors**: Fix in affected section

**Verdict: PASS with issues** — all structural checks pass, good content quality, 13 LaTeX errors need fixing.

---

## Common Cross-Paper Issues

### 1. Line 1 `pdfoutput=1` Without Backslash (ALL)

All three papers have:
```latex
pdfoutput=1          % ← Line 1: BARE, no backslash — causes "Missing \begin{document}"
\pdfoutput=1         % ← Line 2: CORRECT
```

The line 1 bare text is interpreted as literal content before `\begin{document}`, triggering a LaTeX error. It also appears as literal "pdfoutput=1" text in the PDF output (visible at the top of page 1 in all three papers).

**Fix:** Either comment out line 1 (`% pdfoutput=1`) or delete it entirely. The correct `\pdfoutput=1` on line 2 suffices.

### 2. Macro Definition Patterns

- **blockchain** and **elections** both use `\newcommand{\assumptionTag}[1]{\textsf{\textbf{[A#1]}}}` pattern → consistent ✓
- **causal_consensus** has no such macros → inconsistent with the other two papers

---

## Summary

| Paper | Pages | Errors | Critical Issues |
|---|---|---|---|
| causal_consensus | 9 | 15 | \textsf missing, abstract not English, emoji compile error, severely fragmented content |
| blockchain | 25 | 91 | Mostly `\mathrm`-in-text errors (fixable), good content |
| elections | 23 | 13 | Few undefined control sequences (fixable), good content |

**Recommendation:**
- **causal_consensus**: Requires major rewrite — add `\textsf` macros, rewrite abstract in proper English, fix emoji/honestbox/natbib errors, and substantially complete the fragmented content.
- **blockchain**: Fix `\mathrm` macro definitions for text-mode use (~80 errors will resolve), fix line 1 `pdfoutput=1`.
- **elections**: Minor fixes — undefined control sequences, double subscripts, line 1 `pdfoutput=1`.
