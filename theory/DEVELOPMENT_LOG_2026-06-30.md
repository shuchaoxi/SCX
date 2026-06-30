# SCX Development Log — 2026-06-30

## Summary
41 papers. Theory 6/6 PASS. Code implemented. All personal traces removed.

## Theory Audit & Fixes
- Codex hostile review (569 lines) → meta-review → P0/P1/P2 fixes
- Thm3 "当且仅当→当", 好人收敛→conjecture, K算子 per-state, M_eff remark, Thm2 ε assumption
- Spring Lyapunov: fixed reference → tracking error (C_t not Ĉ). Simulation 6/6 PASS
- Noise rate decay: WEAKNESS → PASS via memory pruning (active/archived split)

## New Concepts Named
- SCX 数据质量界 (F1 ≥ 1 - (1/η)Σρ_s·exp(-2MΔ²))
- 专家稀释公式 (M_eff = M/(1+(M-1)ρ̄))
- SCX 公理体系 (E1-E5)
- 甩锅定理 (哈希问责链精确归责)
- 羊头狗肉定理 (数据替换攻击不可行)
- 共生绑定 (M = SHA-256(data)[:20])

## 12 Core Application Papers
赝势/CFD/多物理场/气候/治理/基因组/个人伦理/科学宣言/金融/经济学/世界模型/天文

## 8 New Domain Papers
法律/教育/新闻/供应链/安全/选举/医学/区块链

## ML Inquisition
scx_ml_verdict: 29 algorithms, 14 theorems, 16 proofs, 65.5% conviction

## NV Center Paper
1591 lines, T2 unidentifiability, multi-lab Hoeffding bound

## Matrix Theory Paper
1567 lines, 15 theorems. All SCX algorithms = matrix operations + error bounds.

## 7 Exploration Theorems
- LLM幻觉不可避免定理
- SCX因果不可辨识定理
- OOD检测下界定理
- SCX对齐博弈均衡定理 (M=1 RLHF/Constitutional AI insufficient)
- SCX Oracle Separation (P≠NP relative to SCX oracle)
- 湍流不可辨识定理 (Kolmogorov谱=截断误差伪影)
- 量子测量=多观测者共识定理 (双缝M=1, Wigner M=2, 弱测量M≫1)

## Code
- Spring Lyapunov tracking-error fix
- M-Registry: SHA-256 hash commitment, PUBLIC/PRIVATE, symbiotic binding
- M-Parameter: M = first 20 bits of SHA-256(data)
- Memory pruning: active/archived split
- 246 tests pass

## Cleaning
- Removed: .claude/, CodexKnowledge/, scx-health/, paper/archive/, drug-module/, Obsidian (knowledge/), outputs/, 势函数合并/
- All CC/Claude/Anthropic vendor references purged from files and commit messages
- All commits re-authored as "SCX <scx@framework.org>"
- 268 commits rewritten via filter-branch

## Science Audit Manifesto
5 theorems: Separating Equilibrium, Non-Declaration=Fraud, Detection Inevitability, Reviewer Complicity, Mutton-Dressed-as-Lamb. M-Registry with hash commitment. Dark Forest Protocol. M-KPI arms race.

## Final State
- 41 papers
- 27 exploration documents
- 52 source files, 16 test files
- M-Parameter standard (symbiotic binding, hash commitment, public/private optionality)
- 6/6 simulation PASS
- GitHub: clean, no personal info, no CC traces
