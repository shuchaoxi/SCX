# Batch 19 Review: spring_framework + spring_limits + spring_md (Round 1)

**Date**: 2026-07-02
**Review Type**: LaTeX Compilation + Content Audit + Cross-Paper Coherence
**Files Reviewed**:
- `papers/scx_spring_framework/spring_framework.tex` (1608 lines)
- `papers/scx_spring_limits/spring_limits.tex` (1592 lines)
- `papers/scx_spring_md/spring_md.tex` (2094 lines)

---

## Executive Summary

All three papers compile to PDF but with **significant LaTeX errors** that damage output quality. The most critical shared issue is the **missing `positioning` TikZ library** — all three papers use `below=of`, `right=of`, `below left=... and ... of` syntax but none load `\usetikzlibrary{positioning}`, causing every TikZ figure to render with broken node placement. `spring_limits` is the most damaged, with ~30+ errors from bracing issues, Unicode characters in non-math mode, and math-mode mismatches. `spring_md` additionally fails to render `\ding{55}` (cross marks in comparison tables) because `pifont` is not loaded. All three share the `\pdfoutput=1`-before-`\documentclass` pattern and `\title` structure issues seen in prior batches.

**Compilation Results**:
| Paper | PDF Pages | PDF Size | LaTeX Errors (approx.) | Critical |
|-------|-----------|----------|----------------------|----------|
| spring_framework | 28 | 423 KB | ~72 (mostly PGF + bracing) | PGF positioning, unmatched braces |
| spring_limits | 26 | 372 KB | ~30+ (bracing, Unicode, math mode) | Extremely broken — see §2 below |
| spring_md | 39 | 496 KB | ~25 (PGF, `\ding`, `\textsc`) | PGF positioning, pifont missing |

---

## 1. spring_framework (spring_framework.tex)

### 1.1 Compilation Status
**Result**: PDF generated (28 pages), but with ~72 LaTeX errors. All TikZ figures have mispositioned nodes.

### 1.2 LaTeX Errors

| # | Type | Severity | Location | Description |
|---|------|----------|----------|-------------|
| **E1** | `Missing \begin{document}` | **Medium** | Line 1 | `\pdfoutput=1` before `\documentclass`. Duplicate with line 2 (`\pdfoutput=1` inside preamble). Remove line 1, keep line 2. |
| **E2** | `There's no line here to end` | **Medium** | Line 127-128 | `\title{\textbf{Spring\\[4pt]}}` — the `\\[4pt]` inside `\textbf{}` followed by empty braces `}` creates a broken line break. Fix: `\title{\textbf{Spring}\\[4pt]...}` |
| **E3** | PGF Math: `Unknown function 'of'` | **Critical** | Lines 316-341 | Every TikZ figure uses `below=of input`, `below=of physics`, `below=of reasoning`, `below=of audit` — requires `\usetikzlibrary{positioning}`. **Not loaded.** All nodes collapse to default positions. |
| **E4** | PGF Math errors × 4+ | **Critical** | Lines 316, 320, 324, 328 | Consequence of E3. |
| **E5** | `Missing $ inserted` / `Extra }` | **High** | Lines 127-134 | Title area brace mismatch cascade. Also `\end occurred inside a group at level 6` — six unmatched `{` starting at lines 207, 230, 573, 649, 812, 1078. Systematic bracing issue. |
| **E6** | Font shape OT1/cmr/bx/sc undefined | **Low** | preamble | `\textsc{}` with bold (`\textbf{\textsc{...}}`) — Computer Modern has no bold+smallcaps shape. Minor cosmetic. |

### 1.3 Content Review

#### Strengths
1. **Clear architectural vision**: Five-layer pipeline (Input → Physics → Reasoning → Audit → Output) is well-motivated and diagrams, though broken, conceptually show the data flow.
2. **Good formalism**: Encoder definition (Def 3.1), contrastive alignment loss (Eq 3.2), and routing function (Eq 3.3) provide mathematical grounding for the multi-modal claims.
3. **Honest critiques present**: `\honestcrit` markers appear at lines 1317-1358 with self-critical assessments (H1-H7) covering cross-modal mapping limitations, LLM brittleness, Mt convergence, etc.
4. **Cross-modal audit theorems**: CM1 (Theorem 7.1) with its `χ²` detection bound provides a substantive mathematical claim about cross-modal verifiability.
5. **Comparison framework**: Tables comparing Spring vs GPT-4/Claude/Gemini on audit dimensions are well-structured conceptually, though many cell contents are empty.

#### Issues

| # | Type | Severity | Description |
|---|------|----------|-------------|
| **C1** | **Chinese text — empty in PDF** | **High** | The entire paper is written in Chinese, but no CJK font support is loaded (uses default `fontenc` T1 / OT1). ALL section headings, body text, abstract, ToC entries, and table captions render as **blank** in the PDF. The only visible text is mathematical notation, and English names like "GPT-4", "Claude", "SCX". The paper is essentially unreadable. **Fix**: Switch to `xelatex` (already declared `% !TEX program = xelatex`) with `\usepackage{xeCJK}` and a Chinese font, OR add `\usepackage{CJKutf8}` for pdflatex. |
| **C2** | **Unmatched braces cascade** | **High** | `\end occurred inside a group at level 6` — six `{` opened without matching `}` starting at lines 207, 230, 573, 649, 812, 1078. These correspond to `\cite{...` commands with double-brace patterns like `~\\cite{scx_ml_audit,scx_hamiltonian,yajie_protocol}` — the `~\\` may be causing brace parsing issues, or this is an artifact of the `\honestcrit` environment. |
| **C3** | **`\textbf{}` with empty content** | **Medium** | Lines 143, 160, 166, 182, 202, 224, etc. — dozens of `\textbf{}` commands with no content. Likely placeholders for Chinese bold text that was stripped or never filled. These produce blank bold runs in the output. |
| **C4** | **P1 theorem — M_eff formula** | **Medium** | Theorem P1 (line 596): `M_t^{\text{eff}} = M_t / (1 + \bar{\rho}_t)` — the effective sample size adjustment for correlated experts. Standard Hoeffding bounds for dependent variables require **α-mixing** or **ρ-mixing** conditions, not just pairwise correlation. The denominator form `1 + \bar{ρ}_t` is a heuristic, not a proven bound. The paper should cite a specific dependence-adjustment result (e.g., Bentkus 2005 for dependent sums, or Hoeffding 1963 extension for m-dependent sequences). |
| **C5** | **Yajie score expectation (P2)** | **Low** | Theorem P2 (line 604): `E[s_Yajie | σ_ε > 0] = (1 + σ_ε²/σ̄_expert²)^{-M_t/2}` — this appears to be an unsubstantiated claim. The Yajie consensus score is defined on [0,1] via an exponential kernel, but the expected value formula given uses a rational function form. The derivation is not shown and the connection to the exponential kernel is unclear. |
| **C6** | **Lyapunov convergence (P3)** | **Medium** | Theorem P3 (line 612): Claims `Ψ_{t+1} ≤ Ψ_t` and `lim Ψ_t = 0`. The Lyapunov function is defined as `Var_m[f_m(R_i)]` averaged over data. Monotonic decrease requires that (a) noise removal actually reduces variance, and (b) the re-stratification doesn't increase it — neither is proved. The convergence to 0 is especially strong and would require that expert disagreement vanishes entirely, which contradicts the Höffding residual theorem in spring_limits. |
| **C7** | **Table contents empty** | **High** | Tables at lines 401-422 and 1196-1221 have empty cell contents for most entries. The comparison tables conceptually compare Spring with GPT-4/Claude/Gemini across dimensions like "Physical Grounding", "Audit Status", etc., but the actual text is missing (only `\\` line endings without content). |
| **C8** | **Inconsistent `\textsc{UNDECIDED}` usage** | **Low** | `UNDECIDED` appears both as `\textsc{UNDECIDED}` (small caps) and as plain `UNDECIDED` in different locations. Should be consistent. |
| **C9** | **Cross-modal mapping (Def 7.1) underspecified** | **Medium** | `Φ: C_text → V_phys` is defined as mapping text claims to "the physical variable v for which v corresponds to c", but no construction of Φ is given. For arbitrary natural language claims, this mapping is the entire problem — it requires semantic parsing that is not formalized. |

### 1.4 Fixes Required (Priority Order)
1. **Add `\usetikzlibrary{positioning}`** — fixes all TikZ figures
2. **Add CJK font support** — makes the paper readable (currently ALL Chinese text is blank)
3. **Fix brace matching** — the `\end occurred inside a group at level 6` indicates 6 unmatched `{`
4. **Fix title structure** — `\\[4pt]` inside `\textbf{}` followed by `}` creates E2
5. **Fill empty `\textbf{}` and table cells** — major content gaps
6. **Remove duplicate `\pdfoutput=1`** — delete line 1

---

## 2. spring_limits (spring_limits.tex)

### 2.1 Compilation Status
**Result**: PDF generated (26 pages), but **~30+ LaTeX errors** — the most broken of the three. Many sections likely render with scrambled or missing content.

### 2.2 LaTeX Errors

| # | Type | Severity | Location | Description |
|---|------|----------|----------|-------------|
| **E1** | `Missing \begin{document}` | **Medium** | Line 1 | Same `\pdfoutput=1` before `\documentclass` pattern. |
| **E2** | `There's no line here to end` | **Medium** | Line 131-132 | `\title{\textbf{Spring\\[4pt]}}\\[12pt]` — same title structure issue. The `}` after `\\[4pt]` doesn't close `\textbf{}` properly. |
| **E3** | `Undefined control sequence` | **High** | Line 987 | An undefined command in the G\"odel section. Possibly a missing macro for a mathematical symbol. |
| **E4** | `\mathcal allowed only in math mode` | **High** | Line 1075 | `\mathcal` used outside math mode — likely inside `\honestcrit{}` or a definition's text body. |
| **E5** | Unicode δ / Δ in text mode | **High** | Lines 1223, 1394 | Greek letters `δ` (U+03B4) and `Δ` (U+0394) used directly as Unicode in text mode. pdflatex with T1 encoding can't handle these. Fix: use `$\delta$` and `$\Delta$` in math mode. |
| **E6** | `\spacefactor` errors | **High** | Lines 1446, 1495 | Internal vertical mode errors — typically caused by `\textbf{}` or `\textcolor{}` used in places where paragraph mode is expected but vertical mode is active (e.g., inside table cells or after `\\` in a title). |
| **E7** | `Missing $ inserted` × 3+ | **High** | Lines 1456, 1482, 1484, 1523 | Math content outside math mode. |
| **E8** | `\textcolor` paragraph error | **High** | Line 1584 | `Paragraph ended before \@textcolor was complete` — a `\textcolor{red}{\textbf{...}}` has mismatched braces causing paragraph breaks inside the color command. |
| **E9** | `Too many }'s` × 2 | **High** | Lines 1593, 1601 | Extra closing braces — cascading from earlier brace mismatch. |
| **E10** | Cite warnings × many | **Low** | throughout | All `\cite` references to `spring_framework`, `hoeffding1963`, `godel1931`, `korzybski1933`, `scx_ml_audit` undefined (first-pass compilation — needs `pdflatex` re-run). |

### 2.3 Content Review

#### Strengths
1. **Ambitious theoretical framework**: Three "ceilings" (Hoeffding residual, Gödel boundary, Map≠Territory) synthesize to a cohesive Boundary Theorem. The idea of self-aware audit limits is genuinely philosophically interesting.
2. **Clear error decomposition**: Theorem 4.1's `ε_total = max(ε_stat, ε_phys)` correctly identifies that infinite expert consensus (`M→∞`) cannot overcome systematic physical approximation error.
3. **Honest self-critique**: `\honestcrit` markers acknowledge that Spring only audits within its formal system (§6-7, the "what Spring CANNOT audit" section is unusually self-aware).
4. **Bilingual appendix**: Appendix B provides Chinese/English side-by-side key statements, which is a thoughtful touch for accessibility.
5. **Well-chosen references**: Hoeffding (1963), Gödel (1931), Korzybski (1933) are the right canonical sources for the three ceilings.

#### Issues

| # | Type | Severity | Description |
|---|------|----------|-------------|
| **C1** | **Chinese text — empty in PDF** | **High** | Same as spring_framework. The entire paper's Chinese body text renders as blank. Only English text in section headings, the English column of Appendix B, and math notation are visible. |
| **C2** | **Multiple fatal LaTeX errors damage content** | **Critical** | E4-E9 (~15 errors) likely render significant portions of the paper incorrect or missing. The `\textcolor` and `\spacefactor` errors in particular can swallow entire paragraphs. The paper needs fixes and recompilation before content review can be fully trusted. |
| **C3** | **Gödel boundary — formal system claim** | **High** | Theorem 3.1 claims that `F_Spring` (the Spring formal system) is "sufficiently strong to encode arithmetic" and thus Gödel's incompleteness applies. The proof states that `F_Spring` includes DFT encodings of arithmetic (atomic numbers Z, positions r). However, the claim that a formal system built on DFT predicates + `E_1 < E_2` + `||f_1|| < ||f_2||` can encode Peano arithmetic (required for Gödel I) is **unsubstantiated**. The proof needs to demonstrate a Gödel numbering and show that Robinson's Q (or equivalent) is representable. Without this, the Gödel ceiling is an analogy, not a theorem. |
| **C4** | **Hoeffding residual — "strictly positive" claim** | **Medium** | Theorem 2.1 claims `R(M,Δ) > 0` for all finite M, based on "the inherent possibility that all M experts agree on wrong answers." This relies on SCX1 Assumption A6 (`η > 0` for sample difficulty). But the proof's lower bound `P(ω*) ≥ η · min(p₀, 1-p₁)^M` requires that experts are independent given ω* — this contradicts the correlated expert assumption used earlier in the paper. |
| **C5** | **Map≠Territory — ε_phys definition** | **Medium** | `ε_phys` is defined as the systematic error from DFT approximation (e.g., PBE vs. exact). But Theorem 4.1 then equates `ε_total = max(ε_stat, ε_phys)`, implying statistical and physical errors are independent and the max dominates. In practice, they compound: the statistical error in learning the DFT surrogate is **orthogonal** to the DFT's systematic error, and the total error is their **sum**, not their max. The `max` formulation is overly optimistic. |
| **C6** | **"What Spring CANNOT Audit" (§7) — some items are tautological** | **Low** | Item 5 ("claims outside F_Spring") is a tautology — "Spring cannot audit what it cannot audit." Item 4 ("100% guarantees") is already covered by Ceiling 1. Items 1-3 are substantive. But item 6 ("insufficient data") and item 7 ("speculative claims") are vague restatements of already-established limits rather than new contributions. |
| **C7** | **`\textsc{UNDECIDED}` appears in many contexts** | **Low** | The term UNDECIDED is used for both (a) the Gödelian formal undecidability and (b) practical "we don't know / out of scope." These are fundamentally different concepts (logical necessity vs. epistemic limitation) and should be distinguished. |
| **C8** | **Example 2 (AlN 500K) has overlapping claims** | **Low** | The AlN example in §8 shows Spring output with `a = 3.115 ± 0.003 Å`, but earlier in the Map≠Territory `\honestcrit` (line 648), it says "if Spring provides a=3.11, the physical truth may be δ=0.004." These are in tension — the framework claims to report both the value AND the uncertainty AND the ε_phys caveat, but the example doesn't clearly demonstrate how all three layers interact. |

### 2.4 Fixes Required (Priority Order)
1. **Fix all LaTeX errors** — E3-E9 collectively destroy output quality
2. **Add CJK font support** — paper is unreadable without it
3. **Fix Unicode characters** — replace raw δ/Δ with `$\delta$`/`$\Delta$`
4. **Substantiate Gödel encoding** — or downgrade from Theorem to Conjecture/Analogy
5. **Clarify ε_total decomposition** — justify `max` vs. `sum`
6. **Fix `\title` structure** — same issue as spring_framework

---

## 3. spring_md (spring_md.tex)

### 3.1 Compilation Status
**Result**: PDF generated (39 pages), with ~25 LaTeX errors. All TikZ figures have broken node placement. Comparison tables use `\ding{55}` which renders as blank (pifont not loaded).

### 3.2 LaTeX Errors

| # | Type | Severity | Location | Description |
|---|------|----------|----------|-------------|
| **E1** | `Missing \begin{document}` | **Medium** | Line 1 | Same `\pdfoutput=1` before `\documentclass` pattern. |
| **E2** | `There's no line here to end` × 2 | **Medium** | Lines 1022, 1054 | Two instances of the title/heading structure problem — empty `\\` followed by nothing. |
| **E3** | PGF Math: `Unknown operator 'a' or 'an'` | **Critical** | Lines 316-326 | `below left=1.2cm and -2.8cm of root` — the `and` syntax requires `\usetikzlibrary{positioning}`. **Not loaded.** Four nodes mispositioned. |
| **E4** | PGF Math: `Unknown operator 'o' or 'of'` | **Critical** | Lines 329-342 | `below=1.8cm of train`, `below=1.8cm of run` — more `positioning` syntax failures. |
| **E5** | PGF Math: `Unknown function 'of'` × 14+ | **Critical** | Lines 466-469, 735-738, 1028-1029 | Additional TikZ figures: `right=of data`, `below=of load`, `below=of l1`, etc. ALL fail without `positioning`. |
| **E6** | `Undefined control sequence` × 8 | **High** | Lines 1750-1808 | `\ding{55}` used 8+ times in the engineering comparison table (§11). The `pifont` package is **not loaded**. All cross marks (✗) render as blank or raw "55." |
| **E7** | Font shape OT1/cmr/bx/sc undefined | **Low** | Line 987 | Same bold+smallcaps issue as spring_framework. |
| **E8** | Cite warnings × many | **Low** | throughout | First-pass undefined citations (expected, needs re-run). |

### 3.3 Content Review

#### Strengths
1. **Concrete software specification**: This is the most grounded paper of the three — it describes a real CLI tool with 4 subcommands, YAML config formats, JSON output schemas, and Python API. The level of detail (command-line flags, exit codes, file formats) is impressive.
2. **Practical integration**: LAMMPS and ASE integration code is provided (Python snippets for both engines). The "Transparent Audit Injection" pattern (Spring MD wraps existing MD engines, injects Arbiter hooks without modifying them) is well-designed.
3. **Honest cost disclosure**: Table 11.2 shows Spring MD training cost (6-12× vs NEP single-expert), and §12.1 explicitly acknowledges the overhead. The discussion of inference overhead (2-5% for Mt=8 during MD) is unusually transparent.
4. **JSON Schema**: Appendix A provides a full JSON Schema (Draft 2020-12) for the Arbiter report format — this is production-quality documentation.
5. **End-to-end examples**: §10 provides real bash workflows (Si DFT→train→run→audit→compare), a third-party audit scenario, and a high-throughput materials screening loop.

#### Issues

| # | Type | Severity | Description |
|---|------|----------|-------------|
| **C1** | **Chinese text — empty in PDF** | **High** | Same as the other two papers. All Chinese body text, section headings, table captions, and figure captions render blank. Only code listings, math, and English fragments are visible. |
| **C2** | **`\ding{55}` broken — comparison table unreadable** | **High** | The main architectural comparison table (§11.1, Table 11.1) is the paper's centerpiece argument — it shows that NEP/DeepMD/ACE/MACE all get ✗ on every audit dimension while Spring MD gets ✓. With `\ding{55}` broken, the entire table is meaningless. |
| **C3** | **Algorithm 3.1 (Spring Training) — convergence guarantee gap** | **Medium** | The algorithm uses `while t < T_max and Ψ_t > ε_conv` with updates to Mt, noise removal, and re-stratification at each iteration. No proof is given that this loop terminates within `T_max` iterations while achieving `Ψ_T ≤ ε_conv`. The Lyapunov monotonic decrease claim (same P3 from spring_framework) is unproven. |
| **C4** | **Cercis Score formula — η=0.2 justification** | **Low** | `S_Cercis = Q + η · N` with `η = 0.2` is stated as "derived from calibration experiments in the SCX ML Audit paper." The value 0.2 is arbitrary (why not 0.1 or 0.5?) and the calibration methodology is not reproduced here. |
| **C5** | **"Born Audited" — rhetorical vs. substantive** | **Low** | The phrase "BORN AUDITED" appears prominently throughout (abstract, §1.3, conclusion) as a marketing slogan. While the mechanisms (Mt, Yajie, Cercis, Arbiter) are substantive, the repeated capitalization and slogan-like presentation detracts from the technical tone. |
| **C6** | **LAMMPS integration — `pair_style spring_md`** | **Medium** | The LAMMPS integration claims to create a `pair_style spring_md` via TorchScript export. LAMMPS pair styles require C++ implementations following the `Pair` class interface. While TorchScript can export a compute graph, interfacing it with LAMMPS's internal neighbor-list and per-atom force machinery requires a custom C++ wrapper that is not described. The paper mentions "LibTorch C++ TorchScript" but doesn't explain the bridging mechanism. |
| **C7** | **`\textsc{UNDECIDED}` in a software paper** | **Low** | `UNDECIDED` appears at line? (referencing the Gödel boundary from spring_limits) — in a software specification paper, formal undecidability is out of place. The paper would benefit from focusing on its practical contributions (audit middleware, Arbiter hook, compare framework) rather than importing the philosophical claims from spring_limits. |
| **C8** | **Arbiter hook — OOD detection implementation** | **Low** | The OOD detection uses "ACE Mahalanobis distance" on descriptor space with a "95% threshold." The Mahalanobis distance requires a covariance matrix estimated from training data, which assumes multivariate normality — ACE descriptors are known to be non-Gaussian. The calibration of the 95% threshold is not discussed. |

### 3.4 Fixes Required (Priority Order)
1. **Add `\usetikzlibrary{positioning}`** — fixes ALL TikZ figures (the paper has 4 diagrams)
2. **Add `\usepackage{pifont}`** — fixes the comparison table (all ✗ marks)
3. **Add CJK font support** — makes the paper readable
4. **Remove duplicate `\pdfoutput=1`**
5. **Fix `\title` structure** — two `There's no line here to end` errors

---

## 4. Cross-Paper Coherence Issues

### 4.1 Shared Problems (All Three Papers)

| Issue | spring_framework | spring_limits | spring_md |
|-------|:---:|:---:|:---:|
| `\pdfoutput=1` before `\documentclass` | ✓ | ✓ | ✓ |
| Missing `\usetikzlibrary{positioning}` | ✓ | — | ✓ |
| CJK fonts not loaded (Chinese invisible) | ✓ | ✓ | ✓ |
| `\title` brace structure broken | ✓ | ✓ | ✓ |
| Unmatched braces cascade (`\end occurred inside a group`) | ✓ (6 levels) | ✓ (massive) | ✓ (minor) |
| `\textsc{UNDECIDED}` used across papers | ✓ | ✓ | ✓ |
| Empty `\textbf{}` placeholders | ✓ | ✓ | ✓ |

### 4.2 Conceptual Tensions

1. **P3 vs. Hoeffding residual**: `spring_framework` Theorem P3 claims `lim Ψ_t = 0` (expert disagreement vanishes). `spring_limits` Theorem 2.1 claims `R(M,Δ) > 0` for all finite M (error probability is strictly positive). These are in direct tension — if expert variance can converge to zero, then the audit error probability shouldn't have a positive lower bound.

2. **"Born Audited" vs. Gödel ceiling**: `spring_md` and `spring_framework` emphasize "BORN AUDITED" as a property that distinguishes Spring from GPT/Claude/Gemini. But `spring_limits` proves that Spring has fundamental audibility limits (Gödel undecidability, Map≠Territory). The rhetorical claim "BORN AUDITED" should be qualified as "BORN AUDITED within F_Spring, with explicitly declared boundaries."

3. **Mt binding across papers**: All three reference `Mt = Ξ(hash(D); Ψ, s_Yajie, Σ₀)`, but none define Ξ concretely. `spring_md` Algorithm 3.1 shows `Mt` being updated in a training loop, but the actual function Ξ is a black box. This is the central mechanism of the entire framework and it's undefined.

---

## 5. Overall Assessment

| Paper | Grade | Key Issue |
|-------|-------|-----------|
| spring_framework | **C** | Chinese invisible, all TikZ broken, 6 unmatched braces |
| spring_limits | **D** | ~30+ LaTeX errors likely corrupt output; most critical theoretical claims (Gödel encoding) unsubstantiated |
| spring_md | **C+** | Chinese invisible, all TikZ broken, comparison table blank; but has the most concrete/implementable content |

**Recommendations**:
1. **Immediate**: Add `\usetikzlibrary{positioning}` to spring_framework and spring_md preambles.
2. **Immediate**: Add `\usepackage{pifont}` to spring_md preamble.
3. **High Priority**: Resolve CJK font rendering — all three papers are currently unreadable in PDF form. Consider switching to xelatex (already declared in `% !TEX`) with `\usepackage{xeCJK}` and `\setCJKmainfont{SimSun}` or similar.
4. **High Priority**: Fix the ~30+ bracing/math-mode/Unicode errors in spring_limits — this paper's output is severely damaged.
5. **Substantive**: Define Ξ (the Mt binding function) concretely in at least one paper.
6. **Substantive**: Resolve the P3 vs. Hoeffding residual tension between spring_framework and spring_limits.

---

*Review by SCX, 2026-07-02*
