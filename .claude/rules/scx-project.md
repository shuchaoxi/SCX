# SCX Project — Naming, Architecture, Publication Plan

> **Last updated**: 2026-06-28
> **This file**: Read by all CC agents and subagents automatically

---

## Three Named Components

```
SCX (State-Conditioned eXpertise)
├── Yajie (雅洁) — 去噪声算法   → Paper 1 (JMLR/TMLR)
└── Spring (春季) — 自进化动力学 → Paper 2 (Nature Comp Sci)
```

### Yajie (雅洁) — Noise Detection Algorithm

**Meaning**: 雅 (elegant, precise) + 洁 (clean, pure) = "elegant purification"

**Core formula** (紫荆花公式 / Cercis Score):
```
S(s) = quality_score(s) + η(t) × novelty_bonus(s)
```

**Key insight**: 多专家一致性 → 标签噪声被指数级可靠地检测出来。

**Belongs to**: Paper 1 — *State-Conditioned Expertise: A Complete Theory of Label Noise Detection via Multi-Expert Consistency*

**Implementation**: `src/scx/yajie.py` — 雅洁数据清理器

---

### Spring (春季) — Self-Evolution Dynamics

**Meaning**: 春天 / 复苏 — the season of resurrection

**Core dynamics** (春季动力学 / Spring Dynamics):
```
(S_t, θ_t, M_t) → (S_{t+1}, θ_{t+1}, M_{t+1})
      冬季休眠           春季复苏
```

**Key insight**: Gatekeeper evolves — discarded structures wait in dormancy, then resurrect when the gatekeeper matures.

**Tagline**: *"Winter does not kill — it waits for spring."*

**Belongs to**: Paper 2 — *Spring: A Self-Evolving Gatekeeper with Provable Convergence*

---

## Two-Paper Publication Strategy

### Paper 1: SCX + Yajie
| Item | Detail |
|------|--------|
| **Title** | *State-Conditioned Expertise: A Complete Theory of Label Noise Detection via Multi-Expert Consistency* |
| **Algorithm name** | Yajie (雅洁) |
| **Core** | Theorem 1, 2, 3 + Yajie formula S(s) = Q(s) + η(t)·N(s) |
| **Target** | JMLR / TMLR |
| **Code** | `src/scx/yajie.py` |

### Paper 2: Spring
| Item | Detail |
|------|--------|
| **Title** | *Spring: A Self-Evolving Gatekeeper with Provable Convergence* |
| **Algorithm name** | Spring (春季) |
| **Core** | Spring-1 (Convergence), Spring-2 (Completeness) |
| **Target** | Nature Computational Science |
| **Depends on** | Cites Paper 1 |
| **Theory** | `theory/self_evolution/` |

---

## Naming Summary

| Name | Chinese | What | Paper | Metaphor |
|------|---------|------|-------|----------|
| **SCX** | 状态条件专家框架 | Framework | Both | — |
| **Yajie** | 雅洁 | Noise detection | Paper 1 | Elegant purification |
| **Spring** | 春季 | Self-evolution | Paper 2 | Winter → resurrection |
| **Cercis Score** | 紫荆花公式 | Static gatekeeper formula | Paper 1 | Old wood blooms |

---

## Publication Timeline
```
Now → June:    Paper 1 manuscript finalized (Yajie)
July:          Paper 1 → arXiv preprint + TMLR submission
July-Aug:      Paper 2 experiments + manuscript (Spring)
Aug-Sep:       Paper 2 → Nature Comp Sci submission
```
