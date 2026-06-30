# Cercis Algorithm (紫荆花算法)

> **Formal name**: Cercis Self-Evolving Gatekeeper (CESG)
> **Location**: /g/Xiaogan_Supercomputing_data/SCX/theory/self_evolution/
> **Paper target**: Nature Computational Science (Paper 2 of two-paper strategy)

---

## Why "Cercis"

*Cercis chinensis* (紫荆) is a **cauliflorous** tree — its flowers bloom directly from old branches and trunks, not from new shoots.

```
Cercis biological metaphor → SCX mathematical reality:

  Old branches & trunk    →  Memory bank M_t (accumulated structures, never deleted)
  Flowers                 →  Gatekeeper evaluations (new scores on old structures)
  Each spring bloom       →  Each iteration: S_t re-scores M_t
  Cauliflory              →  Resurrection: discarded structures "bloom" when S_t matures
  New shoots              →  Novelty bonus η(t) · N_t(s) — exploration
  Deep roots              →  DFT/experimental ground truth (physical anchor)
```

**Tagline for paper**: *"Knowledge does not grow from new data alone — it flowers from the old wood of accumulated experience."*

---

## Paper 2: Cercis Flowers

| Item | Detail |
|------|--------|
| **Title** | *Cercis Flowers: A Self-Evolving Gatekeeper with Provable Convergence* |
| **Core Theorems** | Theorem SE-1 (Convergence), Theorem SE-2 (Completeness Bound) |
| **Target** | Nature Computational Science / Nature Machine Intelligence |
| **Depends on** | SCX framework (Paper 1, JMLR/TMLR) |
| **Location** | `theory/self_evolution/` (theorems), `paper/paper_gatekeeper/` (manuscript) |
