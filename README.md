# SCX — State-Conditioned eXpertise

A mathematical framework for certifying data quality through multi-expert consensus. Every claim requires M independent verifiers. No M, no trust.

## Core Discovery

**Theorem 3 — Honest Person Theorem (老实人定理):** Label noise and intrinsic sample difficulty are observationally indistinguishable. No single expert (M=1) can tell them apart.

**SCX Data Quality Bound (数据质量界):** F1 ≥ 1 − (1/η) Σ ρ_s · exp(−2M·Δ²). The multi-expert guarantee — exponential in M.

---

## Papers (48)

### Core Theory (6)
| Paper | Lines | Key |
|-------|-------|-----|
| Theorem 1 — Noise Detection | 685 | Hoeffding F1 bound |
| Theorem 2 — Weak Features | 657 | Lipschitz failure |
| Theorem 3 — Unidentifiability | 796 | Honest Person Theorem |
| Theorem 4 — Exact Minimax | 898 | Bahadur-Rao constant |
| Taxonomic NN | 1,073 | ML derivation + 15 theorems |
| Yajie Protocol | 2,211 | Game theory: NPE + AAE |

### Algorithms (2)
| Paper | Lines | Key |
|-------|-------|-----|
| Spring — Self-Evolving Gatekeeper | 1,365 | Lyapunov + memory pruning |
| Situs — Position Encoding | 1,513 | Lipschitz bound |

### Applications (12)
Pseudopotential, CFD, Multi-Physics, Climate, Governance, Genomics, Personal Ethics, Science Audit Manifesto, Quantitative Finance, Macroeconomics, World Models, Astronomy

### New Domains (8)
Legal Evidence, Education, Journalism, Supply Chain, Cybersecurity, Elections, Medicine, Blockchain

### ML History Verdict (3)
SCX Lens (14 algorithms), SCX Inquisition (29 audited), SCX Verdict (definitive, 29 algorithms, 14 theorems)

### 7 Rigorous Exploration Theorems
| Paper | Core Result |
|-------|------------|
| Hallucination Inevitability | M=1 has lower bound; M>1 exponential detection |
| Alignment Insufficiency | RLHF/Constitutional AI = M=1, fundamentally insufficient |
| Causal Unidentifiability | 3 SCMs observationally equivalent |
| OOD Detection Lower Bound | δ_min = σ/√M |
| P≠NP Oracle Separation | Constructive BGS oracle |
| Turbulence Unidentifiability | 3 theorems, Kolmogorov -5/3 = truncation artifact |
| Quantum Measurement | Multi-observer consensus, Born rule + Hoeffding |

### Additional (10)
Matrix Theory, NV Center, 3 Philosophy papers, Situs Applications, 13 Independent Theorems, EGP Merging, Meta/Manifesto, SCX History

---

## Named Concepts

| Name | Formula |
|------|---------|
| SCX Data Quality Bound | F1 ≥ 1 − (1/η)Σρ_s·exp(−2MΔ²) |
| Expert Dilution Formula | M_eff = M/(1+(M-1)ρ̄) |
| SCX Axiom System | E1-E5 |
| Blame Shedding Theorem | Hash-chain attribution |
| Mutton-Dressed-as-Lamb Theorem | Data substitution infeasible |
| Symbiotic Binding | M = SHA-256(data)[:20] |

---

## Code

```
src/scx/       52 files  — Yajie, Spring, Situs, Cercis, M-Registry
tests/          16 files  — 246 tests pass
theory/         simulation_verify.py — 6/6 PASS
```

---

## How to Read

1. `papers/scx_theory/` — Four core theorems
2. `papers/taxonomic_nn/` — ML derivation + Honest Person Theorem
3. `papers/yajie_protocol/` — Game theory foundation
4. `papers/scx_science_audit/` — M-declaration mandate
5. `papers/scx_ml_verdict/` — 70 years of ML on trial
6. `papers/scx_turbulence/` — Kolmogorov -5/3 is math, not physics

---

## Author

SCX. 2026. No institutional affiliation.
