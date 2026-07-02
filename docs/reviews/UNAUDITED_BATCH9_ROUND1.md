# Batch 9 Review — Round 1

**Date:** 2026-07-02
**Papers reviewed:** 3 (governance, civilization, collective_intelligence)
**Status:** UNAUDITED — all 3 papers have critical issues

---

## Summary

| Paper | File | Chinese(0) | \author{SCX} | \textsf | \pdfoutput=1 | article | no physics/inputenc | pdflatex compile | abstract English | Verdict |
|-------|------|:----------:|:------------:|:-------:|:------------:|:-------:|:-------------------:|:----------------:|:----------------:|:-------:|
| governance | `papers/scx_governance/main.tex` | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | ✅ | **PASS with issues** |
| civilization | `papers/scx_civilization/civ_gauge.tex` | ❌ | ❌ | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | ❌ | **FAIL** |
| collective_intelligence | `papers/scx_collective_intelligence/main.tex` | ❌ | ✅ | ❌ | ⚠️ | ✅ | ✅ | ❌ | ❌ | **FAIL** |

---

## 1. Governance (`papers/scx_governance/main.tex`)

### Check Results

| Check | Status | Detail |
|-------|:------:|--------|
| Chinese(0) | ✅ PASS | No Chinese characters; entirely English |
| `\author{SCX}` | ✅ PASS | Line 79: `\author{SCX}` |
| `\textsf` | ✅ PASS | Lines 73-74: `\assumptionTag` and `\limitationTag` use `\textsf{\textbf{...}}` |
| `\pdfoutput=1` | ⚠️ ISSUE | Line 2 has correct `\pdfoutput=1`, but **line 1 has raw `pdfoutput=1`** (no backslash), which triggers `! LaTeX Error: Missing \begin{document}.` |
| `article` class | ✅ PASS | `\documentclass[11pt,a4paper]{article}` |
| no physics/inputenc | ✅ PASS | No `physics` or `inputenc` packages |
| pdflatex compile | ⚠️ PARTIAL | Produces 25-page PDF but with **1 error** (raw `pdfoutput=1` on line 1); also 103 warnings |
| abstract English | ✅ PASS | Abstract (lines 83-87) is entirely English |

### Issues

1. **[Minor] Raw `pdfoutput=1` on line 1:** Line 1 has `pdfoutput=1` without a backslash. LaTeX treats this as text in the preamble, causing a `Missing \begin{document}` error. The correct `\pdfoutput=1` is already on line 2. **Fix:** Delete line 1 or add a `%` comment prefix.

2. **[Note] `\SCX` defined as `\textsc`, not `\textsf`:** The paper defines `\SCX` as `\textsc{SCX}` (small caps, line 40). The `\textsf` requirement is satisfied by `\assumptionTag` and `\limitationTag` (lines 73-74), which do use `\textsf`. No action needed but worth noting.

3. **[Note] 103 warnings in log:** Mostly standard LaTeX warnings (overfull boxes, undefined references on first pass). Not blocking.

### Verdict: **PASS with minor issues** (line 1 raw text fix recommended)

---

## 2. Civilization (`papers/scx_civilization/civ_gauge.tex`)

### Check Results

| Check | Status | Detail |
|-------|:------:|--------|
| Chinese(0) | ❌ FAIL | **Extensive Chinese characters** throughout: abstract, section titles, body text, table captions, appendix. Bilingual Chinese/English paper. |
| `\author{SCX}` | ❌ FAIL | Lines 65-66: `\author{SCX} Research Group}` — `\author` takes `{SCX}`, then ` Research Group}` is raw preamble text with an unmatched `}`. |
| `\textsf` | ✅ PASS | Line 34: `\newcommand{\SCX}{\textsf{SCX}}` |
| `\pdfoutput=1` | ⚠️ ISSUE | Line 2 has correct `\pdfoutput=1`, but line 1 has raw `pdfoutput=1` (same issue as governance) |
| `article` class | ✅ PASS | `\documentclass[11pt,a4paper]{article}` |
| no physics/inputenc | ✅ PASS | No `physics` or `inputenc`. Has `fontenc{T1}` (not `inputenc`). |
| pdflatex compile | ⚠️ PARTIAL | Produces 22-page PDF but with `Missing \begin{document}` error from broken `\author` line; Chinese characters likely rendered as tofu/missing glyphs (T1 encoding cannot handle CJK); 11 "Missing character" errors in log |
| abstract English | ❌ FAIL | Abstract is bilingual: Chinese text first (lines 70-78), then "English Abstract:" (lines 83-96). Chinese present = FAIL. |

### Issues

1. **[CRITICAL] Chinese characters throughout:** The paper is a bilingual Chinese/English paper. Must be converted to English-only or the Chinese portions must be removed. Section titles, abstract, theorem statements, discussion, and appendices all contain Chinese.

2. **[CRITICAL] Broken `\author` declaration:** Line 65-66:
   ```latex
   \author{SCX} Research Group}
   ```
   The `}` after `Group` is unmatched. `\author{SCX}` is correct, but ` Research Group}` is raw text in the preamble that triggers `Missing \begin{document}`. **Fix:** Change to `\author{SCX}`.

3. **[Minor] Raw `pdfoutput=1` on line 1:** Same issue as governance paper.

4. **[Note] `fontenc{T1}` incompatible with Chinese:** If Chinese characters are removed, this is a non-issue. If Chinese is kept, the paper must use XeLaTeX/LuaLaTeX with `fontspec`.

### Verdict: **FAIL** — Chinese characters + broken `\author`

---

## 3. Collective Intelligence (`papers/scx_collective_intelligence/main.tex`)

### Check Results

| Check | Status | Detail |
|-------|:------:|--------|
| Chinese(0) | ❌ FAIL | **Extensive Chinese characters** throughout: abstract, section titles, body text, theorem statements, figure captions, keywords |
| `\author{SCX}` | ✅ PASS | Line 60: `\author{SCX}` |
| `\textsf` | ❌ FAIL | **No `\textsf` usage found.** No `\SCX` macro defined. "SCX" appears only as literal text in title/references. |
| `\pdfoutput=1` | ⚠️ ISSUE | Line 1 has raw `pdfoutput=1` (no backslash); line 2 has correct `\pdfoutput=1` |
| `article` class | ✅ PASS | `\documentclass[11pt,a4paper]{article}` |
| no physics/inputenc | ✅ PASS | No `physics` or `inputenc` |
| pdflatex compile | ❌ FAIL | **Fatal errors — no PDF produced:**
| | | 1. `\newtheorem{theorem}Theorem[section]` — missing braces (line 11). Should be `{Theorem}`. Same issue on lines 12, 13, 15, 16. |
| | | 2. `\hypersetup{...` never closed (lines 38-41). Missing `}` absorbs all subsequent commands, causing `File ended while scanning use of \@newenv`. |
| abstract English | ❌ FAIL | Abstract (lines 64-73) is bilingual: Chinese sentences mixed with English fragments. Keywords are Chinese. |

### Issues

1. **[CRITICAL] Unclosed `\hypersetup` (lines 38-41):**
   ```latex
   \hypersetup{
    colorlinks=true,
    citecolor=blue,
    urlcolor=blue
   % === Macros ===
   ```
   Missing closing `}`. All subsequent LaTeX commands are absorbed into `\hypersetup`'s argument. **Fix:** Add `}` after `urlcolor=blue`.

2. **[CRITICAL] Missing braces in `\newtheorem` (lines 11-16):**
   ```latex
   \newtheorem{theorem}Theorem[section]       % should be {Theorem}
   \newtheorem{lemma}[theorem]Lemma           % should be {Lemma}
   \newtheorem{corollary}[theorem]Corollary   % should be {Corollary}
   \newtheorem{definition}[theorem]Definition  % should be {Definition}
   \newtheorem{remark}[theorem]Remark         % should be {Remark}
   ```
   The environment display names must be in braces. **Fix:** Wrap each display name in `{}`.

3. **[CRITICAL] Chinese characters throughout:** Abstract, section titles, theorem statements, keywords, figure captions all contain Chinese. Must be English-only.

4. **[CRITICAL] No `\textsf` usage:** The paper lacks any `\textsf` command. No `\SCX` macro is defined. **Fix:** Add `\newcommand{\SCX}{\textsf{SCX}}` and use it in the title/body.

5. **[Minor] Raw `pdfoutput=1` on line 1:** Same issue as other papers.

### Verdict: **FAIL** — 4 critical issues (compilation failure, Chinese, no \textsf, abstract Chinese)

---

## Consolidated Issues Across Batch

### Shared Issue: Raw `pdfoutput=1` on line 1

All three papers have the same pattern:
```latex
pdfoutput=1       % ← line 1: no backslash (causes error)
\pdfoutput=1      % ← line 2: correct
```
The raw text on line 1 triggers a `Missing \begin{document}` error. **Fix for all 3:** Delete line 1 or prefix with `%`.

### Pattern: Chinese in non-governance papers

Two of three papers (civilization, collective_intelligence) contain extensive Chinese text violating the "Chinese(0)" rule. The governance paper is English-only. These papers appear to have been drafted as bilingual Chinese/English documents and need full English-only conversion.

### Pattern: `\textsf` is present in papers that define `\SCX` but missing in papers that don't

- Governance: Uses `\textsf` in `\assumptionTag`/`\limitationTag` (but `\SCX` itself is `\textsc`)
- Civilization: `\SCX` defined as `\textsf{SCX}` ✅
- Collective intelligence: No `\textsf` at all ❌

---

## Recommended Fixes (by priority)

### P0 — Blocking (must fix before merge)

1. **collective_intelligence:** Fix unclosed `\hypersetup` (missing `}`)
2. **collective_intelligence:** Fix 5 broken `\newtheorem` commands (missing braces)
3. **civilization:** Fix `\author{SCX} Research Group}` → `\author{SCX}`
4. **civilization + collective_intelligence:** Remove all Chinese characters → English-only
5. **collective_intelligence:** Add `\textsf` usage (define `\SCX` macro)

### P1 — Important (fix before merge)

6. **All 3 papers:** Delete `pdfoutput=1` on line 1 (keep `\pdfoutput=1` on line 2)

### P2 — Nice to have

7. **governance:** Consider changing `\SCX` from `\textsc` to `\textsf` for consistency with other papers
