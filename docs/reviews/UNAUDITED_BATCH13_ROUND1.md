# Batch 13 Round 1 Review — Geopolitics + Journalism + Law

**Date:** 2026-07-02
**Reviewer:** SCX Audit Agent
**Branch:** main
**Status:** All three papers reviewed

---

## Summary

| Check | scx_geopolitics | scx_journalism | scx_law |
|-------|:-----------:|:-------------:|:------------:|
| Chinese(0) | PASS | PASS | PASS |
| `\author{SCX}` | PASS | PASS | PASS |
| No `\textsf` | **FAIL** | **FAIL** | **FAIL** |
| `\pdfoutput=1` | PASS | PASS | PASS |
| `article` class | PASS | PASS | PASS |
| No physics/inputenc | PASS | PASS | PASS |
| pdflatex compile | PASS | PASS | PASS |
| Abstract English | PASS | PASS | PASS |
| **OVERALL** | **FAIL** | **FAIL** | **FAIL** |

**All three papers fail on the same check:** `\textsf` is used in `\assumptionTag` and `\limitationTag` macro definitions (and additionally in geopolitics domain macros). No previously-audited SCX paper uses `\textsf` — this is a new pattern introduced in Batch 13. The fix is mechanically simple: remove `\textsf{}` wrapper from each affected `\newcommand`.

---

## 1. scx_geopolitics — FAIL ✗

**File:** `papers/scx_geopolitics/main.tex` (697 lines, 61 KB)
**pdflatex:** Compiled successfully → 19 pages, 486 KB PDF.

### Issue A: `\textsf` used in 6 macro definitions (FAIL)

**Locations:** Lines 48–49, 89–92

```latex
\newcommand{\assumptionTag}[1]{\textsf{\textbf{[A#1]}}}        % line 48
\newcommand{\limitationTag}[1]{\textsf{\textbf{[L#1]}}}        % line 49
\newcommand{\gpuDominance}{\textsf{GPU-Dom}}                    % line 89
\newcommand{\auditSupremacy}{\textsf{Audit-Sup}}                % line 90
\newcommand{\declaredState}{\textsf{DECLARED}}                  % line 91
\newcommand{\undeclaredState}{\textsf{UNDECLARED}}              % line 92
```

**Fix:** Remove the `\textsf{}` wrapper from each definition. For assumption/limitation tags, change to `\textbf{[A#1]}`; for domain macros, use `\textsc{...}` (consistent with how other SCX papers style component names like `\Situs`, `\Yajie`, `\Spring`, `\Cercis`).

### Issue B: Garbled title text (MODERATE)

**Location:** Line 110

```latex
\normalsize\textbf{SCXGeopolitics: Mutual Audit EquilibriumGPU HegemonyAudit Supremacy}}
```

The Chinese sub-title appears to have been concatenated with the English title, producing garbled compound terms: "EquilibriumGPU", "HegemonyAudit". A proper Chinese title (if intended) should be on a separate line with appropriate formatting, or the concatenated text should be cleaned up.

### Issue C: Garbled acknowledgments (MINOR)

**Location:** Line 558

```latex
2026-7-2SCX.——., .
```

The trailing `——., .` appears to be a garbled placeholder or corrupted Chinese punctuation. Should be a clean date line: `July 2, 2026` or removed.

### Issue D: Stub appendices (MINOR)

**Locations:** Appendices B (lines 566–568), C (lines 569–571), D (lines 572–573)

```latex
\section{Complete Proof of Mutual Audit Equilibrium (Theorem~\ref{thm:mutual_audit}) ...}
[Complete proof: existence via Kakutani fixed-point theorem ...]
```

Three appendices contain bracketed placeholder text rather than actual proofs. The text describes what the proof *would* contain without providing the proof. This is acceptable for a strategic analysis document (the main body sketches proofs) but should be noted.

### Issue E: Duplicated author metadata (MINOR)

**Location:** Line 8

```latex
% Authors: SCX Strategic Analysis Division  SCXStrategic Analysis Division
```

The author field in the comment is duplicated with a double-space and concatenated variant.

### Issue F: "Chinese" columns in tables are mostly empty

**Locations:** Lines 148–149, 418–427, 576–587, 591–611

Multiple tables include a "Chinese" column header but the cells are either empty or contain non-CJK content. Since the paper has zero actual Chinese characters (confirmed by CJK scan), these columns either need actual Chinese translations or the column should be removed.

### Passed checks:
- Chinese(0), `\author{SCX}`, `\pdfoutput=1`, article class, no physics/inputenc, pdflatex compile, abstract English

---

## 2. scx_journalism — FAIL ✗

**File:** `papers/scx_journalism/main.tex` (1000 lines, 76 KB)
**pdflatex:** Compiled successfully → 20 pages, 418 KB PDF.

### Issue A: `\textsf` used in 2 macro definitions (FAIL)

**Locations:** Lines 91–92

```latex
\newcommand{\assumptionTag}[1]{\textsf{\textbf{[A#1]}}}        % line 91
\newcommand{\limitationTag}[1]{\textsf{\textbf{[L#1]}}}        % line 92
```

**Fix:** Remove the `\textsf{}` wrapper. Change to `\textbf{[A#1]}` and `\textbf{[L#1]}`.

### Additional observations (no action required):

1. **Abstract is very long** (lines 111–112): The abstract contains a single run-on sentence summarizing all four theorems inline. This is acceptable but makes the abstract dense.

2. **Experimental protocol is proposed, not executed** (Section 8, lines 757–803): The section is explicitly labeled as a proposed protocol with "Note: This is a proposed protocol, not a report of completed experiments." This is honest and transparent; no issue.

3. **Well-structured limitations section** (Section 10.3, lines 852–862): Explicit `\limitationTag{L1}`–`\limitationTag{L5}` with clear, honest discussion of assumptions and constraints. This is a strength of the paper.

4. **Strong "what this paper is not" disclaimer** (lines 166–167): Clearly separates mathematical framework from normative claims — a model for other SCX domain papers.

### Passed checks:
- Chinese(0), `\author{SCX}`, `\pdfoutput=1`, article class, no physics/inputenc, pdflatex compile, abstract English

---

## 3. scx_law — FAIL ✗

**File:** `papers/scx_law/main.tex` (954 lines, 64 KB)
**pdflatex:** Compiled successfully → 18 pages, 414 KB PDF.

### Issue A: `\textsf` used in 2 macro definitions (FAIL)

**Locations:** Lines 75–76

```latex
\newcommand{\assumptionTag}[1]{\textsf{\textbf{[A#1]}}}        % line 75
\newcommand{\limitationTag}[1]{\textsf{\textbf{[L#1]}}}        % line 76
```

**Fix:** Remove the `\textsf{}` wrapper. Change to `\textbf{[A#1]}` and `\textbf{[L#1]}`.

### Additional observations (no action required):

1. **Strong conceptual mapping** (Table 1, lines 133–151): The witness↔expert, cross-examination↔audit, hearsay↔self-audit loop mapping is clearly articulated and well-motivated.

2. **Hearsay theorem (Theorem 2)** is particularly elegant: proves that hearsay provides zero independent Shannon information. The corollary on multiple hearsay (mutual information decay as product of fidelities, Corollary 2, line 491–499) is a nice formal result.

3. **Experimental protocol is proposed, not executed** (Section 9, lines 778–804): Same as journalism — explicitly labeled as proposed only. Honest and transparent.

4. **Well-structured discussion** (Section 10, lines 807–863): Relates work to Bayesian evidence evaluation, Dempster-Shafer, legal epistemology, and cryptographic evidence chains. Eight explicit `\limitationTag` items.

5. **"What this paper is not" disclaimer** (lines 170): Similar to journalism — clear boundary between mathematical framework and normative legal theory.

### Passed checks:
- Chinese(0), `\author{SCX}`, `\pdfoutput=1`, article class, no physics/inputenc, pdflatex compile, abstract English

---

## Cross-Paper Observations

### 1. `\textsf` is the only blocking issue (all 3 papers)

This is the sole FAIL across all three papers. The fix is identical and mechanical: remove `\textsf{}` from 2–6 macro definitions per paper. The `\textsf` usage appears intentional (to distinguish assumption/limitation tags from regular text) but is not used in any previously-audited SCX paper. If sans-serif is desired for these tags, the team should establish it as an allowed SCX convention first.

### 2. `\assumptionTag` / `\limitationTag` are new in Batch 13

Previous batches (1–12) did not use these tagged macros. This is a positive addition: explicitly labeling assumptions and limitations improves auditability. However, the `\textsf` wrapper introduces the compliance issue.

### 3. All three papers compile cleanly

No LaTeX errors, no missing references, no font issues. All produce well-formed PDFs of reasonable length (18–20 pages).

### 4. Journalism and Law are structurally strong

Both scx_journalism and scx_law follow the SCX pattern cleanly: formalization → theorems with full proofs → domain-specific protocol/score → experimental protocol → honest limitations. The theorem-level mapping of domain concepts to SCX primitives is well-executed in both.

### 5. Geopolitics has the most cosmetic issues

scx_geopolitics has the most non-blocking cosmetic issues (garbled title, garbled acknowledgments, empty Chinese table columns, stub appendices, duplicated author comment). These don't affect compilation but reduce polish.

---

## Verdict

| Paper | Blocking Issues | Non-Blocking Issues | Verdict |
|-------|:---------------:|:-------------------:|:-------:|
| scx_geopolitics | 1 (`\textsf`) | 5 (garbled title, ack, stub appendices, dup author, empty Chinese cols) | **FAIL** |
| scx_journalism | 1 (`\textsf`) | 0 | **FAIL** |
| scx_law | 1 (`\textsf`) | 0 | **FAIL** |

**Recommended fix workflow:** Apply the same `\textsf` removal to all three papers in a single batch edit, then re-review for Round 2. The geopolitics cosmetic issues can be addressed in the same pass.
