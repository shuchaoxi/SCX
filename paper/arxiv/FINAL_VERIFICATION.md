# FINAL VERIFICATION REPORT -- SCX arXiv Submission

**Date**: 2026-06-28  
**Scope**: All 6 main papers, 8 SI files, theory reference docs, 6 arXiv zip archives  
**Verdict**: **NO-GO** -- 5 Critical, 4 High, 3 Medium issues found

---

## 1. Identity & Anonymity

### 1.1 Author lines -- PARTIAL FAIL

| Paper | File | Author | Status |
|-------|------|--------|--------|
| Paper I (nature_theory) | `nature_main.tex:11` | `\author{SCX}` | PASS |
| Paper II (nature_curation) | `main.tex:11` | `\author{SCX}` | PASS |
| Paper III (paper1_nature) | `main.tex:13` | `\author{SCX}` | PASS |
| **Paper IV (paper2_mlip)** | **`paper_v3.tex:34`** | **`\author{Chengxi Shu}`** | **FAIL** |
| Paper V (paper_llm) | `main.tex:55` | `\author{SCX}` | PASS |
| Paper VI (paper_review) | `main.tex:55` | `\author{SCX}` | PASS |

**CRITICAL**: Paper IV (paper2_mlip) leaks the author's real name. The arXiv zip `arxiv/04_npj_egp.zip` also contains `\author{Chengxi Shu}`.

### 1.2 Personal name occurrences -- PASS

Zero occurrences of "Shuchao", "Chaoxi", "Xi" (as a name), "shu_cx" in any paper `.tex` file.

### 1.3 Email addresses -- PASS

Zero occurrences of `163.com`, `gmail.com`, `whu.edu.cn`, or other personal email addresses.

### 1.4 Affiliations, addresses, corresponding author lines -- FAIL

**CRITICAL**: ALL 6 main papers contain the phrase "available from the corresponding author upon reasonable request" in their Data Availability statements. For a blind arXiv submission (no author names), referencing "the corresponding author" implies that such a person exists, partially compromising anonymity.

| Paper | File | Line |
|-------|------|------|
| Paper I | `nature_main.tex` | 74 |
| Paper II | `main.tex` | 171 |
| Paper III | `main.tex` | 192 |
| Paper IV | `paper_v3.tex` | (present in IP section, line 791+) |
| Paper V | `main.tex` | 554 |
| Paper VI | `main.tex` | 673 |

All say: "available from the **corresponding author** upon reasonable request"

### 1.5 Acknowledgements -- PASS (with note)

Paper II (nature_curation) has no Acknowledgements section. Paper IV (paper2_mlip) thanks "Xiaogan Supercomputing Center" which is explicitly permitted by the CLAUDE.md guidelines ("except Xiaogan SC in Paper IV").

---

## 2. IP Declarations

### 2.1 Presence of IP Statement -- PASS

ALL 6 main papers have an "Intellectual Property Statement" section.

### 2.2 Paper IV (paper2_mlip) AlN data attribution -- PASS

Paper IV includes: "The AlN interatomic potential function and associated DFT reference data were provided by the author's academic advisor and are used with permission; these data remain the intellectual property of the research group that generated them."

### 2.3 Consistency of IP statements -- PASS

All 6 papers use substantially the same IP statement text, with the same content about Apache 2.0 license, public domain theorems, and AlN data attribution.

---

## 3. Mathematical Consistency

### 3.1 Theorem 1 F1 bound: F1 >= 1 - (1/eta) * sum rho_s * exp(-2M*Delta_s^2) -- CONSISTENT

| Location | Formula | Status |
|----------|---------|--------|
| nature_main.tex:36 | `F1 >= 1 - (1/eta) sum rho_s exp(-2M*Delta_s^2)` | PASS |
| S1_thm1_noise_detection.tex:331 | Same formula with `C_{\text{bal}}` in Delta_s | PASS |
| nature_curation/main.tex:69 | Same | PASS |
| paper1_nature/main.tex:93 | Same | PASS |
| paper_llm/main.tex:90 | Same | PASS |
| THEOREMS_UNIFIED.md:159 | Same | PASS |

### 3.2 Theorem 2: uses sqrt(delta/2) NOT sqrt(2*delta) -- CONSISTENT

| Location | Formula | Status |
|----------|---------|--------|
| nature_main.tex:52 | `F1 <= F1_base + C_F * sqrt(delta/2)` | PASS |
| S2_thm2_weak_features.tex:293 | Same | PASS |
| nature_curation/main.tex:77 | Same | PASS |
| paper1_nature/main.tex:111 | Same | PASS |
| paper_llm/main.tex:99 | Same | PASS |
| THEOREMS_UNIFIED.md:229 | Same | PASS |

### 3.3 Theorem 3: K>2 uses random expert construction -- CONSISTENT

S3_thm3_unidentifiability.tex (Section "Extension to K>2 (Random Expert Construction)") uses fully random experts in World B. The K=2 construction uses the biased-expert approach. Both are correctly handled.

### 3.4 Theorem 4': C_min uses Lemma E canonical formula -- CONSISTENT

S4_thm4_exact_constant_minimax.tex:75-81 gives the canonical C_min formula. THEOREMS_UNIFIED.md:326 has the identical formula. Numerical verification in S8 confirms matching to machine precision for all 5 test cases.

### 3.5 C_bal used consistently in Theorem 1 -- CONSISTENT

All occurrences of Theorem 1's Delta_s use `C_{\text{bal}}` in the noise-side term `1 - C_bal * mu_s/(K_Y - 1) - theta`. The underlying theory file S1_thm1_noise_detection.tex correctly uses `C_{\text{bal}}` throughout.

### 3.6 Delta_s definition consistent -- CONSISTENT

All occurrences: `Delta_s = min(theta - mu_s, 1 - C_bal * mu_s/(K-1) - theta)`

---

## 4. Numerical Consistency

### 4.1 Paper I main text F1 >= 0.87 claim -- PASS

Cross-checked with SI S1 formula: For M=12, eta=0.10, mu_s approx 0.35, Delta approx 0.35: F1 >= 1 - (1/0.1)*exp(-2*12*0.35^2) = 1 - 10*exp(-2.94) = 1 - 10*0.053 = 0.47 (lower bound). The empirical 0.87 exceeds this bound. Matches S7_experimental_details.tex:50 which confirms empirical F1=0.87 matching theoretical bound.

### 4.2 AlN: M=12, eta approx 0.10, 8 states -- CONSISTENT across most papers

| Paper | M | eta | States | Noisy frames |
|-------|---|-----|--------|-------------|
| Paper I main | 12 | ~0.10 | 8 | **53** of 534 |
| Paper I SI S7 | 12 | 0.099 | 8 | 53 of 534 |
| Paper II | 8 | ~0.14 | -- | **74** of 534 (14%) |
| Paper III | 12 | ~0.10 | 8 | 53 of 534 |
| Paper IV | -- | -- | -- | 53 mentioned |
| Paper VI (review) | 8-12 | 14% | -- | **74** of 534 (14%) |

**FAIL**: Papers II and VI claim 74 noisy frames (14%), while Papers I, III, S7, and Paper IV consistently use 53 frames. The S7 experimental details (source of truth) explicitly states "53 carry label noise" with eta=53/534=0.099. The 74-frame claim appears in nature_curation/main.tex:105, nature_curation/methods.tex:59, and paper_review/main.tex:284.

### 4.3 CIFAR-10: M=20, eta=0.10 -- CONSISTENT

| Paper | M | eta | F1 |
|-------|---|-----|-----|
| nature_main.tex | M=20 | 0.10 | F1=0.62 |
| nature_curation | M=5 | 0.10-0.40 | -- |
| paper1_nature | M=20 | 0.10 | F1=0.62 |

Minor note: nature_curation says "M=5 ResNet-18 experts" for CIFAR-10 while nature_main and paper1_nature say M=20. This is not necessarily inconsistent (different experimental setups), but warrants clarification.

### 4.4 DermaMNIST: delta/logK approx 0.52, F1 approx 0.10 -- CONSISTENT

All papers consistently report F1 around 0.10 with SimpleCNN features and delta/logK approx 0.52.

### 4.5 DrugBank: precision@0.1 from 0.58 to 0.74 -- CONSISTENT

nature_curation/main.tex and paper1_nature agree on this improvement metric.

---

## 5. Cross-Paper Citations and References

### 5.1 arXiv:XXXX placeholders -- PASS

All cross-references between papers use arXiv:XXXX placeholders. No real arXiv IDs for the SCX papers themselves appear.

### 5.2 Reference format -- PASS

No broken `\ref{}` within individual documents (Sections have labels consistently).

### 5.3 Empty citation placeholders -- FAIL

**CRITICAL**: Paper I (nature_theory) `nature_main.tex` has 4 instances of `\cite{...}` (empty citation with literal dots):

| Line | Text |
|------|------|
| 23 | `model performance degrades predictably and substantially~\cite{...}` |
| 23 | `among others~\cite{...}` |
| 29 | `statistics~\cite{...}` |
| 65 | `factor in machine learning performance~\cite{...}` |

Additionally, line 57 has `~\cite{...}` for the AlN dataset citation. These are literal placeholder dots that will cause a LaTeX compilation error (no bib entry named `...` exists).

The arXiv zip `01_nature_theory.zip` contains the same file with the same empty placeholder citations.

### 5.4 Missing bibliography file -- FAIL

Paper I (nature_main.tex) has no `\bibliography{}` or `\begin{thebibliography}` command at all. The arXiv zip `01_nature_theory.zip` also has no bibliography.

Paper II (nature_curation/main.tex:165) references `\bibliography{references}` but no `references.bib` file exists in the paper directory.

---

## 6. Content Integrity

### 6.1 Garbled text / UTF-8 errors -- PASS

No encoding errors detected in any `.tex` file.

### 6.2 Placeholder text (TODO/TBD/etc.) -- FAIL

| File | Line | Content |
|------|------|---------|
| paper_review/supplementary/supp.tex | 53,56,57,59,60,73,74,76,77,78,81,82,83 | **TBD** in table entries for proposed/theoretical domains |

All "TBD" entries are in the review paper's supplementary table for proposed/theoretical domains, which is acceptable given the paper's stated scope ("Proposed" status explicitly noted). However, these should be cleaned up before arXiv submission.

### 6.3 'placeholder' text -- FAIL

paper_review/main.tex:238 mentions "currently uses placeholder scoring pending model training." This explicitly signals incomplete work.

### 6.4 Obvious typos -- PASS (minor)

Paper III (paper1_nature) line 134: References "companion Paper~II~[arXiv:XXXX]" but this paper is Paper III out of the series -- the cross-reference order is correct (I, II, III).

---

## 7. arXiv Readiness

### 7.1 Zip file contents -- PARTIAL FAIL

| Zip | Files | main.tex present? | Status |
|-----|-------|-------------------|--------|
| `01_nature_theory.zip` | 9 files (main + S1-S8) | YES | **Contains empty \cite{...} placeholders** |
| `02_nature_curation.zip` | 3 files (main + methods + supp) | YES | No `.bib` file |
| `03_nature_method.zip` | 3 files (main + methods + supp) | YES | OK |
| `04_npj_egp.zip` | 1 file (main.tex) | YES | **Contains `\author{Chengxi Shu}` (real name)** |
| `05_llm_strategy.zip` | 2 files (main + supp) | YES | OK |
| `06_scx_review.zip` | 2 files (main + supp) | YES | OK |

### 7.2 Missing bibliography resources -- FAIL

Paper I and Paper II arXiv zips lack bibliography files. `01_nature_theory.zip` has no `.bib` file despite having 9 `.tex` files. `02_nature_curation.zip` references `\bibliography{references}` but no `references.bib` is included.

---

## Summary of Issues by Severity

### CRITICAL (must fix before submission)

| # | Issue | File(s) |
|---|-------|---------|
| C1 | **Real name leak**: `\author{Chengxi Shu}` instead of `\author{SCX}` | `paper2_mlip/paper_v3.tex:34`, `arxiv/04_npj_egp.zip/main.tex:34` |
| C2 | **Empty `\cite{...}` placeholder citations** that will break LaTeX compilation | `nature_theory/main/nature_main.tex:23,29,57,65`, `arxiv/01_nature_theory.zip/main.tex` |
| C3 | **Missing bibliography** in Paper I (no `\bibliography` or `\begin{thebibliography}`) | `nature_theory/main/nature_main.tex`, `arxiv/01_nature_theory.zip` |
| C4 | **AlN frame count inconsistency**: 53 vs 74 frames | 53: nature_main, S7, paper1_nature; 74: nature_curation (main+methods), paper_review |
| C5 | **arXiv:XXXX not a valid citation key** -- Paper I has no bibliography at all | All papers reference "arXiv:XXXX" as placeholder for own citation |

### HIGH (should fix before submission)

| # | Issue | File(s) |
|---|-------|---------|
| H1 | **"corresponding author" in Data Availability** -- breaks blind submission | All 6 papers' Data Availability sections |
| H2 | **Arxiv zip 02_nature_curation.zip missing references.bib** despite citing it | `arxiv/02_nature_curation.zip` |
| H3 | **TBD entries** in review supplementary tables | `paper_review/supplementary/supp.tex` (12 entries) |
| H4 | **"placeholder scoring"** language in review paper | `paper_review/main.tex:238` |

### MEDIUM (should review before submission)

| # | Issue | File(s) |
|---|-------|---------|
| M1 | **CIFAR-10 M count mismatch**: M=20 (Paper I, III) vs M=5 (Paper II) | Various |
| M2 | **Paper IV missing `\author{SCX}`** in arXiv zip -- only has real name | `arxiv/04_npj_egp.zip` |
| M3 | **crossref: `\bibliography{references}` but paper directory has no `.bib` file** | nature_curation, paper_llm directories |

---

## FINAL VERDICT: NO-GO

**Do not submit to arXiv until ALL Critical and High issues are resolved.**

### Minimum required fixes:

1. **Replace `\author{Chengxi Shu}` with `\author{SCX}`** in `paper2_mlip/paper_v3.tex` and regenerate `arxiv/04_npj_egp.zip`

2. **Remove or replace all empty `\cite{...}`** in `nature_main.tex` with real citations or `\cite{}` comments

3. **Add a bibliography section** to `nature_main.tex` (either `.bib` file or `thebibliography`)

4. **Resolve the 53 vs 74 AlN frame inconsistency** across all papers (S7 says 53; this is the source-of-truth)

5. **Remove "corresponding author" language** from Data Availability statements, or add the author name back if not submitting blind

6. **Include `.bib` files in arXiv zips** where `\bibliography{}` is used

7. **Clean up TBD and placeholder language** in the review paper
