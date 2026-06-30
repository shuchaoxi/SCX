# SCX Personal Ethics: A Game-Theoretic Proof That Honesty Is Strictly Dominant for Individuals Under Multi-Expert Audit

An SCX theoretical paper addressing individual citizens with a mathematical proof that honesty is not a moral virtue but a strictly dominant strategy under multi-expert audit with Spring's permanent memory.

**Title (English):** SCX Personal Ethics: A Game-Theoretic Proof That Honesty Is Strictly Dominant for Individuals Under Multi-Expert Audit

**Title (Chinese):** 个体伦理学：诚实策略在多专家审计下严格占优的博弈论证明

## Core Message

You don't need courage to resist pressure from superiors. You need to understand the math. Under SCX audit, honesty is not moral — it is strategically optimal.

## Theorems

1. **Theorem 1 — Detection Inevitability (§3):** For $M$ independent auditors with uniform bounded noise, the probability of missing a deception of magnitude $\delta > \tau$ is exactly $(\tau/L)^M$, independent of $\delta$. As $M \to \infty$ or $t \to \infty$ (Spring accumulation), detection becomes certain: $\lim_{t\to\infty} \mathbb{P}(D_t \mid \text{dishonest}) = 1$.

2. **Theorem 2 — Scale Invariance of Guilt / 勿以恶小而为之 (§4):** For any two deceptions $\delta_1, \delta_2$ exceeding the noise threshold $\tau$, $\mathbb{P}(\text{detection} \mid \delta_1) = \mathbb{P}(\text{detection} \mid \delta_2)$. A small lie and a big lie face identical detection odds. Liu Bei's (刘备) deathbed maxim is proved as a mathematical identity.

3. **Theorem 3 — Honesty as Strictly Dominant (§5):** Under SCX conditions with $M \geq M_{\min} = \lceil \ln(\kappa/(\kappa-b)) / \ln(L/\tau) \rceil$, the expected payoff of honesty strictly dominates any dishonest strategy: $\mathbb{E}[u \mid \text{honest}] = 0 > \mathbb{E}[u \mid \text{dishonest}]$ for all $\delta > 0$. The threshold $M_{\min}$ is computable from observable parameters $(b, \kappa, L/\tau)$.

4. **Theorem 4 — Irreversibility of Evidence (§6):** Under Spring's monotonic memory, $\mathbb{P}(D_t \mid a_\tau = \text{dishonest}) \geq \mathbb{P}(D_\tau \mid a_\tau = \text{dishonest})$ for all $t > \tau$. Evidence never decays. Detection probability is non-decreasing over time. There is no statute of limitations.

## Assumptions (10 total)

| ID   | Description | Section |
|------|-------------|---------|
| A0   | Motivating gap: no prior computable game-theoretic proof for individual honesty dominance | §1 |
| A1   | Scalar data model (generalizes to $\mathbb{R}^d$) | §2 |
| A2   | Bounded observation noise: $\|\hat{\theta}_j - \theta\| \leq L$ | §2 |
| A3   | Uniform noise distribution: $\varepsilon_j \sim \text{Uniform}[-L, L]$ | §2 |
| A4   | Auditor independence: $\varepsilon_j \perp\!\!\!\perp \varepsilon_k$ | §2 |
| A5   | Any-auditor detection rule (single flag triggers investigation) | §2 |
| A6   | Fixed detection tolerance $\tau > 0$ with $\tau < L$ | §2 |
| A7   | Cost dominates benefit: $\kappa > b > 0$; thresholded benefit structure | §2, §5 |
| A8   | Spring monotonicity: $\mathcal{M}_t \subseteq \mathcal{M}_{t+1}$ | §2 |
| A9   | Ex post auditability: claims can be re-examined using future evidence | §2 |
| A10  | Non-decreasing auditor count: $M_{t+1} \geq M_t$ | §2 |

## Limitations (5 explicit)

| ID   | Description | Section |
|------|-------------|---------|
| L0   | Pre-detection retaliation: SCX cannot protect against superior's retaliation before audit detects dishonesty | §1, §7 |
| L1   | Uniform noise assumption: general sub-Gaussian noise changes constants but preserves exponential decay | §3 |
| L2   | Scale invariance exact equality relies on uniform noise; qualitative conclusion holds for bounded symmetric distributions | §4 |
| L3   | Thresholded benefit structure is conservative; continuous $\text{benefit}(\delta)$ strengthens dominance for small $\delta$ | §5 |
| L4   | Evidence quality monotonicity assumes digital-native data; physical evidence may degrade | §6 |
| L5   | Pre-detection retaliation revisited: institutional complements required (whistleblower laws, employment protections) | §7 |

## Structure

| Section | Content |
|---------|---------|
| §1 | Introduction — The Individual's Dilemma (你、你的上级、与那张表格) |
| §2 | Formal Model — Agent in Repeated Audit Game (10 assumptions declared) |
| §3 | Theorem 1 — Detection Inevitability (full proof, 3 cases, Hoeffding connection) |
| §4 | Theorem 2 — Scale Invariance of Guilt / 勿以恶小而为之 (Liu Bei formalized, full proof) |
| §5 | Theorem 3 — Honesty as Strictly Dominant (full proof, $M_{\min}$ derivation, numerical examples) |
| §6 | Theorem 4 — Irreversibility of Evidence / Spring's Monotonicity (full proof) |
| §7 | The Personal Corollary — What This Means for You (你不需要勇气, 上级不是审计者, Spring永不遗忘) |
| §8 | Discussion — Dual Role (agent + auditor), Symmetric Equilibrium, Convergence, Open Problems |

## Key Features

- **Personal tone:** Directly addresses the reader as "you" (你) throughout
- **Bilingual:** All section headers, key terms, and abstract in Chinese + English
- **Not political:** Pure game theory with formal proofs — no political commentary
- **Honest:** Explicitly states SCX cannot protect against pre-detection retaliation
- **Historical grounding:** Liu Bei's (刘备) 勿以恶小而为之 quoted and proved as Theorem 2
- **Computable:** $M_{\min}$ derived as a function of observable parameters

## Mathematical Tools

- Uniform distribution integration for exact closed-form detection probabilities
- Hoeffding inequality connection: $\exp(-2M\Delta^2)$ recovered as approximation
- Game-theoretic strict dominance (Nash equilibrium, best response)
- Monotonicity arguments for Spring memory
- Yajie NPE (Nash Payoff Equilibrium) payoff structure

## Numerical Example

With $\kappa = 10b$ (penalty = 10× benefit) and $L/\tau = 5$ (auditor noise = 5× detection tolerance):
$M_{\min} = \lceil \ln(10/9) / \ln(5) \rceil = \lceil 0.0655 \rceil = 1$. **One auditor suffices.**

Conservative scenario: $\kappa = 1.5b$, $L/\tau = 2$: $M_{\min} = \lceil \ln(3) / \ln(2) \rceil = 2$. Two auditors suffice.

## Building

Requires XeLaTeX or pdfLaTeX with CJK support (ctex package):

```bash
xelatex main.tex
xelatex main.tex  # second pass for references
```

Or with pdfLaTeX:
```bash
pdflatex main.tex
pdflatex main.tex
```

## Dependencies

Standard LaTeX distribution with: ctex (UTF8), amsmath, amssymb, amsthm, mathtools, bm, graphicx, booktabs, hyperref, geometry, natbib, enumitem, xcolor, cleveref.

## SCX Conventions

- **Rigor markers:** `\rigorFull` — all four theorems carry full proofs
- **Assumptions:** A0--A10, explicitly labeled with `\assumptionTag{}`
- **Limitations:** L0--L5, explicitly labeled with `\limitationTag{}`
- **SCX components:** Spring (permanent memory), Yajie (NPE payoff structure)
- **Bilingual:** Chinese terms used alongside English throughout section headers
- **No metaphors:** All claims stated with mathematical precision, proofs are self-contained
