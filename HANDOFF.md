# SCX Handoff — Dual Hermes Workstream

**Date:** 2026-07-02
**For:** Second Hermes instance (English conversion)
**Repo:** `github.com/shuchaoxi/SCX`

---

## Current State

| Item | Count |
|------|:--:|
| `.tex` papers | 212 |
| `.md` copies | 253 |
| Verification scripts | 36 (ALL PASS) |
| Tests | 676 passed |
| Review rounds | 120+ |
| Bib references | 12 entries |

**Problem:** Most `.tex` files are Chinese+English bilingual. CC/Codex has partially converted 1 paper (moe_gauge). 211 papers remain. Many still have `\mathsf` macros that fail in text mode. Several papers have `\begin{compactenum}` without `\usepackage{paralist}`.

**Goal:** ALL `.tex` papers → English-only, compiling cleanly with `pdflatex` (or `xelatex` for ctexart papers).

---

## Your Task: English Conversion

### Priority Order

1. **CRITICAL — Large papers with Chinese (>500 lines):**
   - `papers/scx_moe_gauge/main.tex` (2210 lines — partially done by CC, Codex finishing)
   - `papers/scx_unified_field/main.tex` (2383 lines)
   - `papers/scx_gauge_formalized/gauge_formalized.tex`
   - `papers/scx_gauge_physics/gauge_physics.tex`
   - `papers/scx_fiber_bundle/fiber_bundle.tex`

2. **HIGH — Core theory papers:**
   - `papers/scx_theory/` (9 files)
   - `papers/theorems/` (16 files)
   - `papers/scx_quantum_audit/quantum_audit.tex`

3. **MEDIUM — All remaining `.tex` files**

### Rules

1. **Reference template:** `SCX_TEMPLATE.tex` (pdflatex-compatible, `\textsf` macros)
2. **Bib file:** `docs/tex/sample.bib` (12 entries, author=SCX)
3. **For ctexart papers:** keep `\documentclass{ctexart}` and compile with `xelatex`
4. **For article papers:** use `\documentclass{article}` and compile with `pdflatex`
5. **Chinese → English:** ALL Chinese text (sections, theorems, content, comments) → English
6. **Math preservation:** NEVER change any equation, symbol, or LaTeX math command
7. **Theorem names:** 定理→Theorem, 引理→Lemma, 推论→Corollary, 定义→Definition, 注记→Remark
8. **Macro fix:** Replace `\mathsf{SCX}` → `\textsf{SCX}` (works in both math and text mode)
9. **Missing packages:** If `compactenum` used, add `\usepackage{paralist}`
10. **Compile verification:** After each file, run `pdflatex` (or `xelatex` for ctexart) to verify zero errors
11. **Context check:** For papers >1000 lines, verify that English conversion is complete from start to end (CC often converts front but misses back half)
12. **English quality:** Use precise mathematical English — do NOT let translation distort theorem statements, formulas, or dataset descriptions
13. **Do NOT touch .md files** — only work on `.tex`
14. **Author is ALWAYS `SCX`** — `\author{SCX}`

### Workflow per paper

```bash
# 1. Read the paper
# 2. Convert Chinese → English
# 3. Fix macros (\mathsf→\textsf, missing packages)
# 4. Compile and fix errors
xelatex -interaction=nonstopmode paper.tex
# or: pdflatex -interaction=nonstopmode paper.tex
# 5. Commit
git add -A && git commit -m "refactor: <paper_name>英文化" && git push origin main
```

---

## My Task: New Directions

- New `.tex` papers using ONLY `SCX_TEMPLATE.tex` format
- Continuing discussions, iterations, reviews
- Pushing 10-round convergence for all items
- Physics explorations (Monte Carlo, Phase Field, String, Tokamak, QFT)

---

## Folder Structure

```
SCX/
├── SCX_TEMPLATE.tex          ← use this template
├── README.md
├── AUDIT_STATUS.md
├── ATTACK_SURFACE.md
├── PAPER_SCRIPT_INDEX.md
├── docs/
│   └── tex/
│       ├── sample.bib        ← reference library
│       └── main.tex          ← Overleaf base
├── papers/                   ← ALL papers here
│   ├── scx_moe_gauge/        ← most important
│   ├── scx_unified_field/
│   ├── scx_theory/
│   └── ... (94 directories)
└── tests/                    ← 676 tests
```

---

## Communication

After completing a batch, update the handoff status. If you encounter a paper that CANNOT be converted without breaking math, flag it and move on. Prioritize volume over perfection — better 200 papers at 95% English than 10 papers at 100%.

**Current handoff state:**
- moe_gauge: Codex working on completion (partial CC conversion)
- All others: NOT STARTED
- Template: SCX_TEMPLATE.tex (verified compiles)
- Bib: sample.bib (12 entries)
