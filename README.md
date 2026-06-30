# SCX — State-Conditioned eXpertise

A mathematical framework for certifying data quality through multi-expert consensus. Every claim about data requires M independent verifiers. No M, no trust.

## Core Discovery

**Theorem 3 — The Honest Person Theorem (老实人定理):** Label noise and intrinsic sample difficulty are observationally indistinguishable without declared assumptions. No single expert (M=1) can tell them apart.

**SCX Data Quality Bound (数据质量界):** F1 ≥ 1 − (1/η) Σ ρ_s · exp(−2M·Δ_s²). The multi-expert guarantee — exponential in M.

---

## Papers (41)

### Core Theory (6)
| Paper | Lines | Theorems | Key |
|-------|-------|----------|-----|
| Theorem 1 — Noise Detection | 685 | 1 | Hoeffding F1 bound |
| Theorem 2 — Weak Features | 657 | 1 | Lipschitz failure bound |
| Theorem 3 — Unidentifiability | 796 | 3 | Honest Person Theorem |
| Theorem 4 — Exact Minimax | 898 | 1 | Bahadur-Rao sharp constant |
| Taxonomic NN | 1,073 | 15 | ML derivation + flagship |
| Yajie Protocol | 2,211 | 9 | Game theory: NPE + AAE + Audit Sword |

### Algorithm Theory (2)
| Paper | Lines | Theorems | Key |
|-------|-------|----------|-----|
| Spring — Self-Evolving Gatekeeper | 1,365 | 13 | Lyapunov convergence, memory pruning |
| Situs — Physical Position Encoding | 1,513 | 4 | Lipschitz encoding bound |

### Applications (12)
| Domain | Lines | Key Insight |
|--------|-------|------------|
| Pseudopotential Distillation | 905 | PAW multi-functional audit |
| CFD Aerodynamics | 1,047 | Turbulence model consensus |
| Multi-Physics Coupling | 970 | Cross-domain error propagation |
| Climate Modeling | 848 | ECS unidentifiability, CMIP6 audit |
| Government Transparency | 1,207 | M-KPI, blame-shedding theorem |
| Genomics | 1,462 | Variant pathogenicity consensus |
| Personal Ethics | 966 | Honesty strictly dominant, 勿以恶小 |
| Science Audit Manifesto | 644 | 5 theorems, M-Registry, Dark Forest |
| Quantitative Finance | 1,790 | Model risk unidentifiability |
| Macroeconomics | 2,594 | Lucas Critique formalized |
| World Models | 1,326 | Cross-module physics audit |
| Multi-Messenger Astronomy | 1,312 | Fisher-weighted Hoeffding |

### New Domains (8)
| Domain | Lines | Key Insight |
|--------|-------|------------|
| Legal Evidence | 955 | Multi-witness certification |
| Educational Assessment | 984 | Grade inflation detection |
| News Verification | 1,001 | Multi-source fact-checking |
| Supply Chain Traceability | 915 | Hash chain from farm to shelf |
| Cybersecurity | 1,048 | False alarm vs zero-day unidentifiability |
| Electoral Integrity | 1,141 | Multi-method vote certification |
| Medical Diagnosis | 1,710 | Multi-physician consensus, rare disease |
| Blockchain Consensus | 1,238 | Fork boundary theorem, 51% attack |

### ML History Audit (3)
| Paper | Lines | Verdict |
|-------|-------|--------|
| SCX Lens (re-interpretation) | 1,206 | 14 algorithms re-derived from SCX |
| SCX Inquisition (indictment) | 1,513 | 29 algorithms audited, 62% GUILTY |
| SCX Verdict (merged definitive) | 2,050 | 29 algorithms, 14 theorems, 16 proofs |

### Additional (10)
| Paper | Lines |
|-------|-------|
| Matrix Theory (SCX linear algebra) | 1,567 |
| NV Center Quantum Sensing | 1,591 |
| Philosophy of Science | 1,073 |
| Philosophy of Law | 1,416 |
| Philosophy of Education | 972 |
| Situs Applications (12 domains) | — |
| Independent Theorems (13 papers) | — |
| EGP Merging (ACE potentials) | — |
| Meta / SCX Manifesto | — |
| SCX History | — |

---

## Named Concepts

| Name | Formula / Meaning |
|------|-------------------|
| SCX Data Quality Bound (数据质量界) | F1 ≥ 1 − (1/η)Σρ_s·e^(−2MΔ²) |
| Expert Dilution Formula (专家稀释公式) | M_eff = M/(1+(M-1)ρ̄) |
| SCX Axiom System (公理体系) | E1-E5 knowledge axioms |
| Blame Shedding Theorem (甩锅定理) | Hash-chain precise attribution |
| Mutton-Dressed-as-Lamb (羊头狗肉定理) | Data substitution attack infeasible |
| Symbiotic Binding (共生绑定) | M = SHA-256(data)[:20] |

---

## Exploration Theorems (theory/explorations/)

| Theorem | Status |
|---------|--------|
| LLM Hallucination Inevitability | \rigorFull |
| Causal Unidentifiability (3 SCMs) | \rigorFull |
| OOD Detection Lower Bound (δ_min = σ/√M) | \rigorFull |
| Alignment M=1 Insufficiency (RLHF/Constitutional AI) | \rigorFull |
| P≠NP Oracle Separation (constructive BGS) | \rigorFull + Conjecture |
| Turbulence Unidentifiability (3 theorems, Burgers verified) | \rigorFull |
| Quantum Measurement = Multi-Observer Consensus | \rigorFull |

---

## Code

```
src/scx/        52 files  — Yajie, Spring, Situs, Cercis, M-Registry
tests/          16 files  — 246 tests passing
theory/          simulation_verify.py — 6/6 PASS
```

---

## Theory Status

- Simulation: 6/6 PASS (Lyapunov tracking error, noise decay, memory, F1, convergence)
- Proof chain audit: updated with all fixes
- Hostile review: Codex 569-line review → meta-review → all P0/P1/P2 fixed

---

## How to Read

1. `papers/scx_theory/` — The four core theorems
2. `papers/taxonomic_nn/` — ML derivation + Honest Person Theorem
3. `papers/spring_config/` — Self-evolving gatekeeper
4. `papers/yajie_protocol/` — Game theory foundation
5. `papers/scx_science_audit/` — Why all science needs M-declaration
6. `papers/scx_ml_verdict/` — 70 years of ML on trial

---

## Author

SCX. 2026.

All papers attributed to SCX. No institutional affiliation. No personal information. No vendor references.
