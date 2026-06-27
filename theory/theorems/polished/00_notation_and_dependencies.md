# Unified Notation and Theorem Dependency Graph

> This document consolidates notation across all three SCX theorems and maps the logical dependencies between them. It serves as a quick-reference companion to the polished theorem statements.

---

## 1 Unified Notation Table

### 1.1 Core Objects

| Symbol | Meaning | Thm 1 | Thm 2 | Thm 3 | Domain |
|--------|---------|-------|-------|-------|--------|
| $\mathcal{X}$ | Input space | x | x | x | Measurable space |
| $\mathcal{Y}$ | Label space, $K = \|\mathcal{Y}\|$ | x | x | x | Discrete (classif.) or $\mathbb{R}^d$ (regr.) |
| $X$ | Input random variable | x | x | x | $\mathcal{X}$ |
| $Y$ | Observed label | x | x | x | $\mathcal{Y}$ |
| $Y^*$ | True (latent) label | — | — | x | $\mathcal{Y}$ |
| $f^* : \mathcal{X} \to \mathcal{Y}$ | Ground-truth oracle | x | — | x | — |
| $\{f_m\}_{m=1}^M$ | Expert models | x | x | x | $\mathcal{X} \to \mathcal{Y}$ |
| $\ell : \mathcal{Y} \times \mathcal{Y} \to [0, B]$ | Bounded loss function | x | x | — | $B < \infty$ |
| $\tau > 0$ | Expert error threshold | x | — | — | $\mathbb{R}^+$ |

### 1.2 Noise Model

| Symbol | Meaning | Thm 1 | Thm 2 | Thm 3 | Definition |
|--------|---------|-------|-------|-------|------------|
| $\eta$ | Global noise rate $\mathbb{P}(Y \neq Y^*)$ | x | x | x | $\eta \in (0, 1/2)$ |
| $\eta(x)$ | Input-dependent noise rate | — | — | x | $\eta(x) = \mathbb{P}(Y \neq Y^* \mid X = x)$ |
| $Z$ | Noise indicator ($1$ = noise, $0$ = clean) | — | x | — | $Z \in \{0, 1\}$ |
| $e_m(x, y)$ | Expert error indicator | x | — | — | $e_m = \mathbf{1}\{\ell(f_m(x), y) > \tau\}$ |
| $C(x)$ | Consistency score | x | — | — | $C(x) = \frac{1}{M}\sum_m e_m(x, y)$ |

### 1.3 State and Feature Structure

| Symbol | Meaning | Thm 1 | Thm 2 | Thm 3 | Definition |
|--------|---------|-------|-------|-------|------------|
| $\mathcal{S}$ | State space | x | x | x | Finite set, $\|\mathcal{S}\| = K_S$ |
| $s : \mathcal{X} \to \mathcal{S}$ | State assignment | x | x | x | Partition of $\mathcal{X}$ |
| $\rho_s = \mathbb{P}(X \in s)$ | State probability | x | — | x | $\sum_s \rho_s = 1$ |
| $\mu_s$ | State-level clean error bound | x | — | — | $\mu_s = \sup_{x \in s} \mathbb{E}[C \mid \text{clean}, x]$ |
| $C_{\text{bal}}$ | Error balance constant | x | — | — | $C_{\text{bal}} \geq 1$ |
| $\Delta_s$ | Separation gap for state $s$ | x | — | — | $\Delta_s = \min(\theta - \mu_s, 1 - C_{\text{bal}}\mu_s/(K-1) - \theta)$ |
| $\phi : \mathcal{X} \to \Phi$ | Observed feature map | — | x | — | $\Phi \subseteq \mathbb{R}^{d_\phi}$ |
| $\delta$ | Feature-state mutual information | — | x | — | $\delta = I(\phi(X); S)$ |
| $\varepsilon_\phi$ | Normalized weakness | — | x | — | $\varepsilon_\phi = \delta / \log K_S \in [0, 1]$ |

### 1.4 Detection and Evaluation

| Symbol | Meaning | Thm 1 | Thm 2 | Thm 3 | Definition |
|--------|---------|-------|-------|-------|------------|
| $\theta$ | Detection threshold | x | — | — | $\theta \in (0, 1)$ |
| $NS(x)$ | Noise score | — | x | — | SCX noise score for sample $x$ |
| $\hat{z}(x)$ | Predicted noise label | — | x | — | $\hat{z}(x) = \mathbf{1}\{NS(x) > t\}$ |
| $\text{FPR}_s$ | False positive rate (state $s$) | x | — | — | $\mathbb{P}(C > \theta \mid \text{clean}, s)$ |
| $\text{TPR}_s$ | True positive rate (state $s$) | x | — | — | $\mathbb{P}(C > \theta \mid \text{noise}, s)$ |
| F1 | F1 score of detector | x | x | — | $2\text{TP}/(2\text{TP}+\text{FP}+\text{FN})$ |
| AUC | Area under ROC curve | — | x | — | $\mathbb{P}(\text{score}_{\text{noise}} > \text{score}_{\text{clean}})$ |
| PR-AUC | Area under precision-recall curve | — | x | — | $\int \text{Precision}(t) \, d\text{Recall}(t)$ |

### 1.5 Theorem-Specific Parameters

| Symbol | Meaning | Appears In | Defined As |
|--------|---------|-----------|------------|
| $\mathcal{P}_{\text{noise}}, \mathcal{P}_{\text{hard}}$ | Two data-generating processes | Thm 3 | Constructive counterexample |
| $\varepsilon_1, \varepsilon_2$ | Expert error rates in states $s_1, s_2$ | Thm 3 | $\varepsilon_1 \in (0, 1/2)$, $\varepsilon_2 \in (\varepsilon_1, 1/2]$ |
| $\tilde{P}$ | Auxiliary distribution ($\phi \perp S$) | Thm 2 | $\tilde{P}(\phi, S) = P(\phi)P(S)$ |
| $F1_{\text{base}}$ | Loss-baseline detector F1 | Thm 2 | $\max_t \text{F1}(\hat{z}_{\text{loss}}(t))$ |
| $F1_{\text{rand}}$ | Random detector F1 | Thm 2 | $2\eta/(1+\eta)$ |

---

## 2 Assumptions Cross-Reference

| ID | Assumption | Thm 1 | Thm 2 | Thm 3 |
|----|-----------|-------|-------|-------|
| A1 | Disjoint training sets | **Required** | Implicit | Target of Corollary 2 |
| A2 | Clean-data conditional independence | **Required** | Implicit | Technical basis for Cor. 2 |
| A3 | Bounded loss | **Required** | Implicit | — |
| A4 | Uniform independent noise | **Required** | — | Target of Corollary 3 |
| A5 | State homogeneity | **Required** | — | Target of Corollary 4 |
| A6 | Balanced error distribution | **Required** | — | Target of Corollary 5 |

---

## 3 Theorem Dependency Graph

```
                         ┌──────────────────────┐
                         │   Theorem 3           │
                         │  (Unidentifiability)  │
                         │                       │
                         │  Core claim:          │
                         │  Without A1-A6,       │
                         │  noise vs. difficulty │
                         │  is observationally    │
                         │  equivalent           │
                         └──────────┬───────────┘
                                    │
                    "What minimum assumptions
                     are needed to make the
                     problem tractable?"
                                    │
                                    v
               ┌─────────────────────────────────────┐
               │   A1-A6 are the minimal sufficient   │
               │   conditions to break Thm 3's        │
               │   unidentifiability                   │
               └─────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    v                               v
   ┌────────────────────────────┐    ┌────────────────────────────┐
   │   Theorem 1                │    │   Theorem 2                │
   │  (Noise Detection)         │    │  (Weak Feature Failure)    │
   │                            │    │                            │
   │  Positve result:           │    │  Negative result:          │
   │  Under A1-A6, noise is     │    │  Even under A1-A6, if      │
   │  detectable with F1→1      │    │  features are δ-weak,      │
   │  exponentially fast in M   │    │  SCX cannot beat loss      │
   │                            │    │  baseline by more than     │
   │                            │    │  O(√δ)                     │
   └────────────────────────────┘    └────────────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    │
                                    v
                    ┌──────────────────────────────┐
                    │   Unified SCX Picture         │
                    │                               │
                    │  SCX Effectiveness ≈          │
                    │    I(φ; S) - O(1/√n)         │
                    │                               │
                    │  • Thm 3: Why we need A1-A6   │
                    │  • Thm 1: What we gain with   │
                    │    them                       │
                    │  • Thm 2: Where the boundary  │
                    │    lies                      │
                    └──────────────────────────────┘
```

### 3.1 Dependency Logic

The three theorems form a logical chain of necessity, sufficiency, and boundary:

1. **Theorem 3 (Fundamental Hardness)** establishes that without structural assumptions, the noise detection problem is ill-posed: noise and intrinsic difficulty are observationally equivalent. This is the **necessity** result -- it explains _why_ assumptions are required, not just convenient.

2. **Theorem 1 (Sufficient Conditions)** shows that under assumptions A1-A6 -- the minimal set identified in Theorem 3 -- noise detection succeeds with exponentially decaying error. This is the **sufficiency** result -- it quantifies _how well_ SCX works when its assumptions hold.

3. **Theorem 2 (Boundary Condition)** shows that even when A1-A6 hold, the feature representation $\phi$ must carry enough mutual information about the true state $S$ for SCX to outperform a simple loss baseline. This is the **boundary** result -- it identifies _when_ SCX ceases to add value despite valid assumptions.

### 3.2 Information-Theoretic Unification

The three theorems can be unified under a single information-theoretic inequality:

$$\underbrace{\text{SCX Advantage}}_{\text{Thm 1: exponential F1} \to 1} \;\leq\; \underbrace{f(I(\phi; S))}_{\text{Thm 2: } O(\sqrt{\delta}) \text{ bound}} \;\leq\; \underbrace{g(\text{A1-A6})}_{\text{Thm 3: minimal conditions}}$$

where $f$ and $g$ are monotone increasing functions. The chain reads:
- Without A1-A6, $g = 0$ and the problem is unidentifiable (Thm 3)
- With A1-A6 but $I(\phi; S) \to 0$, SCX collapses to the baseline (Thm 2)
- With both A1-A6 and strong features, SCX achieves exponential guarantee (Thm 1)

---

## 4 Key Inequalities Reference

| Inequality | Used In | Statement |
|-----------|---------|-----------|
| Hoeffding | Thm 1 (Lemmas 2, 3) | $\mathbb{P}(\bar{X} - \mu \geq t) \leq e^{-2nt^2}$ |
| Chernoff (Sanov) | Thm 1 (tightened) | $\mathbb{P}(\bar{X} \geq \theta) \leq e^{-n \cdot \text{KL}(\theta \|\mu)}$ |
| Pinsker | Thm 2 (original) | $\operatorname{TV}(P, Q) \leq \sqrt{\frac{1}{2}\operatorname{KL}(P\|Q)}$ |
| Bretagnolle-Huber | Thm 2 (tightened) | $\operatorname{TV}(P, Q) \leq \sqrt{1 - e^{-\operatorname{KL}(P\|Q)}}$ |
| Fano | Thm 2 (Lemma 1) | $P(\hat{S} \neq S) \geq \frac{H(S \mid \phi) - \log 2}{\log \|\mathcal{S}\|}$ |
| Data Processing | Thm 2 | $\operatorname{TV}(P_{\text{pred}}, Q_{\text{pred}}) \leq \operatorname{TV}(P, Q)$ |

---

## 5 Quick-Start Guide

| If you want to understand... | Read this combination |
|-----------------------------|----------------------|
| Why SCX needs assumptions | Thm 3 + Section 4 of Thm 3 (A1-A6 mapping) |
| How well SCX detects noise | Thm 1 + Corollaries 1-4 |
| When SCX cannot work | Thm 2 + Diagnostic Section 7 |
| Practical deployment | Thm 1 Corollary 4 (finite-sample) + Thm 2 diagnostics |
| The complete picture | All three + this notation document |

---

**Document version**: 2026-06-27
