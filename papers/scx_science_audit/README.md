# The SCX Audit Mandate: M-Parameter Declaration for Scientific Publication
## SCX审计宣言：科学发表的M参数声明前置条件

**SCX Manifesto — June 2026**
**SCX Research Collective**

---

## Overview

This paper provides the game-theoretic and information-theoretic foundation for mandatory M-parameter declaration in scientific publishing. Every scientific claim derived from data has a minimum number M of independent verifiers needed to certify its quality. We prove that not declaring M is epistemically equivalent to fraud, and that declaring M while falsifying data is active evil with detection probability → 1.

## Key Results

### Theorem 1 — Separating Equilibrium
Under mandatory M-declaration, a unique separating Perfect Bayesian Equilibrium exists where honest researchers declare M ≥ M_min and dishonest researchers cannot profitably mimic, because fabricating mutually consistent data across M independent verifiers costs exponentially in M.

M_min = ln(1/ε) / (2Δ²)

### Theorem 2 — Non-Declaration = Fraud
Without M-declaration, the posterior probability of fraud for any published claim is unbounded: sup_{priors} P(fraud | C, no M) = 1. M-declaration is information-theoretically necessary for quality certification.

### Theorem 3 — Falsification = Active Evil (声明参数还做假等于作恶)
Researchers who declare M and falsify data face detection probability 1 - exp(-2M·Δ²). As verification accumulates over time, lim_{t→∞} P(detection) = 1. The fraudster's calculated deception is mathematically doomed.

## The M-Parameter Standard

1. Every quantitative paper must declare M_min for its central claims
2. Default ε = 0.05 (matching p < 0.05 tradition)
3. Unverifiable claims → labeled [UNVERIFIABLE]
4. Papers without M → treated as [NOT YET AUDITED]

## Cercis Score

S(paper) = Q(paper) + η·N(paper)
- Q = replicability score (successful independent replications)
- N = novelty of claim
- Papers with M=0 get Q=0 regardless of claimed novelty

## Case Studies

- **High-energy physics (ATLAS/CMS)**: M=2 natural cross-validation
- **Psychology replication crisis**: M was never declared → 50%+ replication failure explained
- **Deep learning benchmarks**: M often = 1 (single seed) — needs M ≥ 17
- **耿同学 (Geng)**: M=1 already changes the equilibrium; now imagine M=100

## Assumptions (8 numbered)

A1. Bounded Publication Benefit
A2. Positive Audit Penalty
A3. Exponential Fabrication Cost
A4. Constant Genuine Data Cost
A5. Independent Verification
A6. Verifier Growth Over Time
A7. M-Declaration is Verifiable
A8. Rational Researcher
A9. Auditor Detection Capability

## Bilingual Content

Chinese-English bilingual throughout: 审计宣言/科学诚信/M参数/耿同学

## Compilation

```bash
xelatex main.tex
# or
pdflatex main.tex  # if Chinese fonts are configured
```

Requires: `ctexart` document class, `amsmath`, `amssymb`, `amsthm`, and standard Chinese fonts (SimSun, SimHei, KaiTi).

## Declaration (宣言)

**No M, no trust.**
**Declare M, earn credibility.**
**Declare M and cheat, get caught.**
**Science is humanity's cumulative intellectual achievement — 人类的精神结晶不允许污染.**
**Every paper without M-declaration is epistemically equivalent to fraud.**
**Every paper with M-declaration is auditable, verifiable, and accountable.**
**The Geng precedent proves the path. The M-Parameter Standard institutionalizes it.**
**The audit gap is closed. The separating equilibrium is here.**
