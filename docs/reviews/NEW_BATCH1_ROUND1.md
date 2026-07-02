# Batch 1 Round 1 — New Paper Reviews

**Date:** 2026-07-02
**Reviewer:** SCX (Hermes Agent)
**Papers reviewed:** 3 (scx_black_hole, scx_cryptography, scx_number_theory)

---

## Quick Summary

| Paper | Compiles? | Pages | `\author{SCX}` | `\pdfoutput=1` | `article` | `\textsf` | Chinese | `inputenc`/`physics` | Abstract | Status |
|-------|-----------|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| black_hole | ✅ Yes | 24 | ✅ | ✅ | ✅ | ✅ | ✅ 0 | ✅ None | ✅ | ⚠️ enumitem errors |
| cryptography | ✅ Yes | 23 | ✅ | ✅ | ✅ | ✅ | ✅ 0 | ✅ None | ✅ | ❌ `\H` conflict; ⚠️ enumitem |
| number_theory | ✅ Yes | 17 | ✅ | ✅ | ✅ | ✅ | ✅ 0 | ✅ None | ✅ | ❌ `\EuScript` undefined; ❌ theorem/proof mismatch; ❌ TikZ div/0 |

**Verdict:** All three pass the hard criteria (Chinese=0, \author{SCX}, \textsf, \pdfoutput=1, article, no physics/inputenc, pdflatex-compilable, abstract present). But **all three have LaTeX errors** that should be fixed.

---

## 1. `papers/scx_black_hole/main.tex`

**Lines:** 1345 | **PDF:** 24 pages, 531 KB

### Checks Passed
- `\pdfoutput=1` — line 1 ✅
- `\documentclass[12pt,a4paper]{article}` — line 7 ✅
- `\usepackage[english]{babel}` + `\usepackage[T1]{fontenc}` — no `inputenc`, no `physics` ✅
- `\author{SCX}` — line 164 ✅
- `\textsf` used for framework macros (SCX, Yajie, Spring, Cercis, etc.) — lines 109–116 and throughout ✅
- No Chinese characters ✅
- Abstract present — lines 171–175 ✅
- pdflatex compiles ✅

### Errors
- **120 `! Undefined control sequence` / `! Missing number, treated as zero` errors** — all from `\enit@resuming` inside `enumitem`-based environments (enumerate/itemize). This is a version-specific internal command issue in the `enumitem` package. The file compiles to valid output regardless (just cosmetic errors in nonstopmode). **Severity:** Low — output is fine.
- **All citations are undefined** — normal for a draft without a `.bib` file. Warnings only, not errors.

### Verdict
⚠️ **PASS with minor issues.** The enumitem errors should be investigated (possible outdated `enumitem` version); otherwise clean.

---

## 2. `papers/scx_cryptography/main.tex`

**Lines:** 1177 | **PDF:** 23 pages, 502 KB

### Checks Passed
- `\pdfoutput=1` — line 1 ✅
- `\documentclass[12pt,a4paper]{article}` — line 7 ✅
- `\usepackage[english]{babel}` + `\usepackage[T1]{fontenc}` — no `inputenc`, no `physics` ✅
- `\author{SCX}` — line 202 ✅
- `\textsf` used for framework and crypto macros — lines 119–157 and throughout ✅
- No Chinese characters ✅
- Abstract present — lines 209–213 ✅
- pdflatex compiles ✅

### Errors
- **`! LaTeX Error: Command \H already defined.`** — line 92 has `\newcommand{\H}{\mathcal{H}}` which clashes with TeX's built-in `\H` Hungarian double-acute accent command. The file compiled because LaTeX issued a warning and kept the existing definition, but `\H` will produce the accent, not `\mathcal{H}`. **This is a real bug** — every use of `\H` in the paper (e.g., Hilbert space) will be wrong. **Fix:** Use `\renewcommand` or a different macro name like `\Hilb` (which is what the black_hole paper uses).
- **204 enumitem internal errors** — same `\enit@resuming` undefined as in black_hole. **Severity:** Low.
- **All citations undefined** — normal draft warnings.

### Verdict
❌ **FAIL with one real bug.** The `\H` conflict will silently produce wrong output (accented characters instead of `\mathcal{H}`). Must be fixed before publication.

---

## 3. `papers/scx_number_theory/main.tex`

**Lines:** 1138 | **PDF:** 17 pages, 431 KB

### Checks Passed
- `\pdfoutput=1` — line 1 ✅
- `\documentclass[12pt,a4paper]{article}` — line 2 ✅
- `\usepackage[english]{babel}` + `\usepackage[T1]{fontenc}` — no `inputenc`, no `physics` ✅
- `\author{SCX}` — line 95 ✅
- `\textsf` used for framework macros — lines 58–66 and throughout ✅
- No Chinese characters ✅
- Abstract present — lines 99–121 ✅
- pdflatex compiles ✅

### Errors
- **`! Undefined control sequence: \EuScript`** — line 55 defines `\newcommand{\ExpertSet}{\EuScript{E}}` but the `euscript` package is **never loaded**. This means `\ExpertSet` (used in definition 298, 393) resolves to garbage. **Fix:** Add `\usepackage{euscript}` or change to a different font command.
- **`! LaTeX Error: \begin{theorem} on input line 744 ended by \end{proof}`** — structural error in the theorem environment:
  ```latex
  \begin{theorem}[Cercis Score Lower Bound for Verified Zeros]   % line 744
  % ... theorem text ...
  \end{proof}   % line 754 ← WRONG: should be \end{theorem}
  \end{theorem} % line 755
  \begin{proof}[Sketch]  % line 756
  ```
  **Fix:** Remove line 754 (`\end{proof}`) — it's a stray command. The `\end{theorem}` at line 755 correctly closes the theorem, and `\begin{proof}[Sketch]` at 756 correctly opens the proof.
- **`! Package PGF Math Error: divide by 0`** — line ~780, the TikZ pair correlation plot uses `\x` in `sin(pi*\x r)` but `\x` starts at 0. This crashes the plot. **Fix:** Use `{1 - (sin(pi*(\x+0.001) r)/(pi*(\x+0.001)))^2}` or start the domain from a small epsilon.
- **`\tableofcontents`** on line 122 — unusual for a paper; generates a TOC page. Not an error but atypical for an `article` class paper.

### Verdict
❌ **FAIL with three real bugs:** `\EuScript` undefined, theorem/proof mismatch, TikZ divide-by-zero.

---

## Summary Table

| Requirement | black_hole | cryptography | number_theory |
|:---|---:|:---:|:---:|
| Chinese count = 0 | ✅ | ✅ | ✅ |
| `\author{SCX}` present | ✅ | ✅ | ✅ |
| `\textsf` used | ✅ | ✅ | ✅ |
| `\pdfoutput=1` | ✅ | ✅ | ✅ |
| `article` documentclass | ✅ | ✅ | ✅ |
| No `physics`/`inputenc` | ✅ | ✅ | ✅ |
| pdflatex compiles to PDF | ✅ | ✅ | ✅ |
| Abstract present | ✅ | ✅ | ✅ |
| **No LaTeX errors** | ⚠️ (120 enumitem) | ❌ (`\H` conflict + 204 enumitem) | ❌ (8 errors: \EuScript, theorem/proof, TikZ) |

## Recommended Fixes

### cryptography
1. **Line 92:** Change `\newcommand{\H}{\mathcal{H}}` to `\newcommand{\Hilb}{\mathcal{H}}` (or use `\renewcommand`) and update all uses of `\H` → `\Hilb`.

### number_theory
1. **Line 55:** Add `\usepackage{euscript}` to preamble (before `\newcommand{\ExpertSet}{\EuScript{E}}`).
2. **Line 754:** Delete the stray `\end{proof}` line. Replace with nothing (let `\end{theorem}` on line 755 close the environment).
3. **Line 779:** Fix the TikZ plot to avoid `sin(pi*0)/0` — e.g., change domain to `[0.01:5]` or add a small epsilon guard.
4. (Optional) Remove `\tableofcontents` on line 122 for a cleaner article format.

### black_hole
1. Investigate enumitem version — the `\enit@resuming` errors suggest an older or newer `enumitem` package where the internal API changed. Update MiKTeX packages or pin the enumitem version.
