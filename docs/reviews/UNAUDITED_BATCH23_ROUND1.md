# Batch 23 Round 1 Review — llm + ood + hallucination

**Reviewer:** Hermes Agent (automated)
**Date:** 2026-07-02
**Papers Reviewed:**
1. `papers/scx_llm/main.tex` — State-Conditioned Expertise for LLM Data Curation (position paper)
2. `papers/scx_ood/main.tex` — SCX OOD Detection Lower Bound
3. `papers/scx_hallucination/main.tex` — SCX Hallucination Inevitability Theorem

---

## 1. scx_llm — State-Conditioned Expertise for LLM Data Curation

**File:** `papers/scx_llm/main.tex` (764 lines, ~81KB) + `supp.tex` (419 lines, ~30KB)
**Target:** arXiv → ACL/NeurIPS Position Track

### Summary
A position paper arguing that the SCX framework should serve as a *meta-evaluation layer* for LLM data curation—calibrating judge reliability in a state-conditioned manner—rather than as a direct data quality judge. Identifies four fundamental gaps preventing direct transfer from the scientific ML setting, proposes four research directions, a minimal viable experiment (MVE), and a three-phase strategic roadmap (6/12/24 months).

### Strengths
- **Well-structured argument.** The four-gap / four-direction / MVE / roadmap structure is clear and logical.
- **Honest positioning.** The paper is explicit about what it does NOT claim to solve, and acknowledges the null hypothesis that SCX may provide no benefit for LLM data.
- **Rich supplementary material.** `supp.tex` adds substantial rigor: formal definitions of each gap, a detailed comparison table vs. 9 existing method families, reformulated SCX equations, and a theorem applicability table.
- **Self-contained.** The background section recaps SCX theorems 1-3, the uncertainty principle, and establishes the hallucination inevitability argument independently.

### Issues Found

#### Critical
1. **Undefined macro `\rigorFull`** (lines 237, 252): The alignment theorems (lines 226–275) use `\rigorFull` which is defined in the OOD and hallucination papers but NOT in this file's preamble. LaTeX compilation will fail or produce "undefined control sequence" errors.

2. **Missing section label for MVE** (line 496): `\section{Minimal Viable Experiment Design}` has no `\label{sec:mve}`, but `\S\ref{sec:mve}` is referenced at line 535 and in the supplementary material. This will produce `??` in the rendered PDF.

3. **Irrelevant IP statement** (lines 752–753): The Intellectual Property Statement references "AlN interatomic potential function and associated DFT reference data" and "CIFAR-10, DermaMNIST, and MedMNIST" datasets. These are from the original SCX paper about scientific ML and have nothing to do with LLM data curation. This appears to be a copy-paste artifact that must be rewritten.

4. **Stale Data/Code Availability** (lines 755–759): References "AlN v3 dataset," "DrugBank," and placeholder `[repository]`. These are also copy-paste artifacts from the original SCX paper and are inappropriate for an LLM-focused paper.

#### Moderate
5. **Duplicated hallucination content** (lines 119–224): The entire "LLM Hallucination Inevitability Theorem" section (including Definition, Theorem, Corollary, Proof, and H-Bound) also appears as a standalone paper at `papers/scx_hallucination/main.tex`. If both are to be published, this duplication must be resolved—either cite the standalone paper or decide which is the canonical version.

6. **Alignment theorems lack citation of the hallucination paper.** If `scx_hallucination` is being published separately, the alignment discussion should cite it rather than re-deriving the same results.

7. **Unused command `\Fone`** (line 41): Defined via `\providecommand{\Fone}{\mathrm{F1}}` but never used in the text.

#### Minor
8. **Variable name collision potential:** Both the LLM paper and the hallucination paper use `\P` for probability, but the LLM paper redefines it with `\renewcommand{\P}{\mathbb{P}}` (line 38) while the OOD/hallucination papers use `\Pbb`. Not a problem in isolation, but if merged would cause issues.

9. **Section depth confusion:** The `\subsection{LLM Hallucination Inevitability Theorem}` (line 119) is nested under `\section{Background: The SCX Framework}` (line 81), but it's a major self-contained result that could warrant its own section, especially given its length (100+ lines).

10. **No PDF in directory:** Unlike scx_ood and scx_hallucination which have compiled PDFs, the scx_llm directory has no `main.pdf`. Given the `\rigorFull` issue, it likely fails to compile.

### Verdict
This is the most substantial paper in the batch. The argument is coherent and the positioning is honest. However, it has **four critical issues** (undefined macro, missing label, irrelevant IP/data statements) that must be fixed before any submission. The hallucination content duplication with the standalone paper also needs resolution.

---

## 2. scx_ood — SCX OOD Detection Lower Bound

**File:** `papers/scx_ood/main.tex` (112 lines, ~3.9KB)
**Compiled PDF:** Present (`main.pdf`)

### Summary
A very short paper proving a finite-expert lower bound for OOD detection via Spring gatekeeper scores. The main result: false alarm probability ≤ 2exp(-2Mε²), detection power ≥ 1−exp(−2M(δ_OOD−ε)²), both controlled by Hoeffding bounds exponential in M.

### Strengths
- **Clean, focused result.** One definition, one theorem, one proof. Does exactly what it claims.
- **Compiles successfully** (PDF present).
- **Self-contained preamble** with all macros defined locally.

### Issues Found

#### Major
1. **No document structure.** The paper has no `\section{}`, only a `\subsection{}`. It lacks: title page content, introduction, related work, discussion, conclusion, references. Even as a short note, it needs at minimum a brief introduction and a conclusion stating the significance.

2. **No standalone narrative.** The text references "CUSUM statistic above" and "Spring gating notes" without context, suggesting this was extracted from a larger document and is not readable as a standalone paper.

3. **Abstract is too thin** (line 25): One sentence stating the result with no context about why OOD detection matters, what Spring is, or what the practical implications are.

#### Moderate
4. **Missing references.** The text mentions "Spring memory bank," "CUSUM statistic," and "Spring gating notes" but provides no citations or bibliography.

5. **Memory calibration not addressed.** The theorem says "the calibration error is handled in Corollary~\\ref{cor:spring_memory_scaling}" but that corollary is not present in this file—it was presumably in the parent document.

#### Minor
6. **Equation label collision** (line 73): `\label{eq:spring_ood_test}` is used for both Definition 1 and the equation within it. The `\ind` command on line 71 is undefined—should be `\mathbf{1}` or `\mathbb{1}`.

### Verdict
This is a fragment, not a paper. It contains a valid mathematical result but lacks the surrounding text needed to be a standalone publication. Suitable as a section in a larger paper (e.g., a Spring framework paper) but not as an independent submission. Needs substantial expansion or should be folded into a parent document.

---

## 3. scx_hallucination — SCX Hallucination Inevitability Theorem

**File:** `papers/scx_hallucination/main.tex` (137 lines, ~7.5KB)
**Compiled PDF:** Present (`main.pdf`)

### Summary
Proves that high-confidence hallucinations are inevitable for any single-model (M=1) LLM, with a lower bound of η·ρ_min. Multi-model auditing (M>1) provides exponential detection guarantees exp(−2MΔ²). Contains H-Problem definition, H-Theorem, H-Corollary, and H-Bound.

### Strengths
- **Rigorous theorem chain.** Definition → Theorem → Corollary → Multi-auditor bound forms a clean logical progression.
- **Compiles successfully** (PDF present).
- **Strong result with practical implications.** The single-model impossibility and multi-model escape route is well-motivated.

### Issues Found

#### Critical
1. **Embedded raw line numbers in content** (lines 31–136): The LaTeX source contains literal line numbers from the parent document, e.g.:
   ```
   119|\label{sec:llm_hallucination_inevitability}
   120|
   121|The same argument gives a token-level...
   ```
   These numbers (`119|`, `120|`, `121|`, etc.) are not LaTeX comments—they are raw text that will appear in the rendered output. This makes the paper unpublishable as-is. **Every line from 31 to 136 has this problem.**

2. **Near-verbatim duplication of scx_llm/main.tex §lines 119–224.** The entire content of this paper is a proper subset of the LLM paper. If both papers are submitted, this is self-plagiarism. The hallucination paper either needs to be:
   - The canonical version cited by the LLM paper, or
   - Merged into the LLM paper as a section, or
   - Significantly differentiated with additional content not in the LLM paper.

3. **Missing `\cS` definition.** The paper uses `\cS` (line 52) but this macro is never defined in the preamble. It's defined in the LLM paper but not here. LaTeX may produce an error depending on whether `\cS` is a standard command (it's not—it's defined as `\mathcal{S}` in the LLM paper).

#### Major
4. **No document structure beyond one subsection.** Like scx_ood, this has no introduction, no motivation section, no related work, no conclusion, and no references. One subsection is not a paper.

5. **"The same argument gives..."** (line 33/121): The text begins mid-thought with "The same argument gives a token-level impossibility result..."—it assumes the reader has just read Theorem 3 of the SCX paper. Not self-contained.

#### Moderate
6. **No references/bibliography.** Cites "SCX Theorem~3" and "SCX assumptions A1--A6" without a bibliography entry.

7. **Proof sketches, not full proofs.** Both the H-Theorem and H-Bound are labeled "Proof sketch." For a paper whose core contribution is these theorems, full proofs would be expected (or at least a note that full proofs appear in the SCX parent paper).

### Verdict
This paper has a valid and interesting mathematical result, but it is **not publishable in its current state**. The embedded line numbers are a formatting catastrophe, the content is fully duplicated in the LLM paper, and it lacks the scaffolding of a proper paper. If this is to be a standalone publication, it needs: (a) line numbers removed, (b) substantial differentiation from the LLM paper, (c) a full paper structure (intro, background, related work, discussion, conclusion, references), and (d) self-contained definitions.

---

## Cross-Paper Issues

### Content Duplication
The hallucination paper is a **verbatim subset** of the LLM paper (scx_llm §2.2, lines 119–224). The OOD paper may also be a fragment extracted from a larger Spring framework paper (it references CUSUM and Spring gating notes without context). This suggests a pattern where sections are being carved out into standalone papers without sufficient differentiation.

**Recommendation:** Decide on a publication strategy:
- **Option A:** Keep the LLM paper as the comprehensive document. Fold OOD and hallucination results into it (or cite them as internal sections). Do not publish OOD/hallucination separately.
- **Option B:** Publish three separate papers, but each must be fully self-contained with introduction, related work, discussion, and references. The hallucination paper must be differentiated from the LLM paper's §2.2. The OOD paper must explain Spring/CUSUM context.
- **Option C:** Publish the LLM paper as the main paper and the others as short technical notes, with cross-citations. Even then, the hallucination paper needs its line numbers stripped and its content differentiated.

### LaTeX Hygiene
| Issue | scx_llm | scx_ood | scx_hallucination |
|---|---|---|---|
| `\rigorFull` defined? | ❌ (used but not defined) | ✅ | ✅ |
| `\cS` defined? | ✅ | N/A | ❌ (used but not defined) |
| `\ind` defined? | N/A | ❌ (used, undefined) | N/A |
| Line numbers in source? | ❌ | ❌ | ❌ (CRITICAL) |
| PDF compiles? | Unknown (likely fails) | ✅ | ✅ (but with line numbers visible) |

### Compilation Status
- `scx_ood/main.pdf`: Present, 112 lines → compiles
- `scx_hallucination/main.pdf`: Present, 137 lines → compiles (but line numbers are visible in output)
- `scx_llm/main.pdf`: **Not present** — likely fails due to undefined `\rigorFull` and other issues

---

## Summary of Required Actions

### scx_llm (Priority: HIGH)
- [ ] Define `\rigorFull` macro in preamble (or remove its use)
- [ ] Add `\label{sec:mve}` to the MVE section
- [ ] Rewrite IP Statement, Data Availability, and Code Availability to be LLM-relevant
- [ ] Remove or replace unused `\Fone` command
- [ ] Verify compilation and produce `main.pdf`

### scx_ood (Priority: MEDIUM)
- [ ] Add introduction, conclusion, and references
- [ ] Define `\ind` or replace with `\mathbf{1}`
- [ ] Fix duplicate `\label{eq:spring_ood_test}`
- [ ] Either add Corollary~\ref{cor:spring_memory_scaling} or remove the reference to it
- [ ] Add context explaining Spring, CUSUM, and memory bank for standalone readability
- [ ] Consider whether this should be a section in a larger paper rather than standalone

### scx_hallucination (Priority: HIGH)
- [ ] **URGENT:** Remove all embedded line numbers (lines 31–136)
- [ ] Define `\cS` in preamble
- [ ] Resolve duplication with scx_llm §2.2 — differentiate content or fold into LLM paper
- [ ] Add introduction, motivation, related work, conclusion, references
- [ ] Upgrade proof sketches to full proofs or cite parent paper for full proofs
- [ ] Make self-contained (don't start with "The same argument gives...")

### Cross-Paper (Priority: MEDIUM)
- [ ] Decide on publication strategy: one paper vs. three
- [ ] If three papers, ensure each is fully self-contained and non-overlapping
- [ ] If one paper, fold OOD into a Spring paper and hallucination into the LLM paper
