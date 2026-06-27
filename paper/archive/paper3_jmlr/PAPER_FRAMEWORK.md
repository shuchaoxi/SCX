# Paper 3: State-Conditioned Expert Reliability — Full Paper Framework

> **Target venue**: JMLR / TMLR  
> **Series position**: Paper 3 of 5 (deep theory paper)  
> **Title direction**: *"State-Conditioned Expert Reliability: When Multi-Expert Consistency Detects Noise and When It Cannot"*  
> **Status**: Framework design — all sections draftable (pure theory, no GPU required)  
> **Date**: 2026-06-27

---

## Table of Contents

1. [Paper Identity and Positioning](#1-paper-identity-and-positioning)
2. [How Paper 3 Differs from Paper 1](#2-how-paper-3-differs-from-paper-1)
3. [Complete Paper Anatomy](#3-complete-paper-anatomy)
4. [Existing Material Inventory](#4-existing-material-inventory)
5. [New Mathematical Contributions Required](#5-new-mathematical-contributions-required)
6. [Theorem Mapping: Paper 1 to Paper 3](#6-theorem-mapping-paper-1-to-paper-3)
7. [Drafting Priority and Readiness](#7-drafting-priority-and-readiness)
8. [Timeline and Milestones](#8-timeline-and-milestones)

---

## 1. Paper Identity and Positioning

### 1.1 Core Contribution Statement

This paper develops the **complete statistical theory** of state-conditioned expert reliability for label noise detection. We:

1. **Relax** the strong assumptions of Paper 1 (A1-A6) to minimal identifiable conditions (3 assumptions), proving that the SCX framework is essentially the unique solution to the noise-detection problem under natural statistical constraints.

2. **Sharpen** all three main theorems with optimal concentration inequalities: Bernstein for Theorem 1 (replacing Hoeffding), Le Cam and Fano lower bounds for Theorem 2 (tightening the minimax rate), and a semiparametric identifiability extension for Theorem 3.

3. **Connect** SCX theory to four established literatures: Dawid-Skene models, PAC-Bayes generalization, coreset theory (Feldman-Langberg), and the information bottleneck principle — proving that SCX subsumes or improves each.

4. **Prove minimax optimality**: The SCX noise detector achieves the optimal detection rate up to constant factors; no algorithm operating under the same information constraints can asymptotically outperform SCX.

### 1.2 Relation to Paper 1 (Nature/Empirical Flagship)

| Aspect | Paper 1 | Paper 3 |
|--------|---------|---------|
| Purpose | Introduce SCX framework, empirical validation | Full mathematical foundation |
| Theorems | Stated in ~1000 words, proofs in SI | Complete proofs with optimal inequalities |
| Assumptions | 6 strong (A1-A6) | 3 minimal, then relaxed versions |
| Proof techniques | Hoeffding, Fano, constructive | Bernstein, Talagrand, empirical process, Le Cam, semiparametric theory |
| New connections | None | PAC-Bayes, Dawid-Skene comparison, coreset theory, information bottleneck |
| Length | ~800 words + 8pp SI | 30-40 pages |
| Experiments | Real-world (AlN, CIFAR, MedMNIST) | Synthetic bound-tightness validation + reference to Paper 1 results |
| Figures | 5-6 empirical figures | 3-4 theoretical figures (bound behavior, schematic) |

### 1.3 Series Context (Paper 3 of 5)

```
Paper 1 (Nature/Empirical): SCX framework + experiments        [submitted]
Paper 2 (NeurIPS/Applications): SCX in 5+ domains              [planning]
Paper 3 (JMLR): Theory — THIS PAPER                             [drafting]
Paper 4 (AIStats): SCX active learning + compression theory     [planned]
Paper 5 (COLT): Expert construction + feature learning theory   [planned]
```

Paper 3 establishes the theoretical bedrock upon which Papers 4 and 5 build. It can be written independently of Papers 2, 4, 5.

### 1.4 Target Audience

- **Primary**: Machine learning theorists (JMLR/TMLR readership)
- **Secondary**: Statisticians working on label noise, crowdsourcing, multiple annotation
- **Tertiary**: Practitioners seeking theoretical guarantees for data cleaning

The paper assumes graduate-level familiarity with: empirical process theory, concentration inequalities, information theory (Fano, Pinsker), minimax lower bounds, and semiparametric statistics.

---

## 2. How Paper 3 Differs from Paper 1

### 2.1 Assumption Structure Comparison

**Paper 1 assumptions (A1-A6)**:

| Assumption | Content | Role |
|------------|---------|------|
| A1 | Disjoint training sets | Ensures conditional independence of experts |
| A2 | Conditional independence given clean data | Technical basis for concentration |
| A3 | Bounded loss | Technical (Hoeffding inequality) |
| A4 | Uniform independent noise | Noise mechanism specified |
| A5 | State homogeneity | State-level error rate constant |
| A6 | Balanced error distribution | Prevents expert bias from mimicking noise |

**Paper 3 reduced assumptions (B1-B3)**:

| Assumption | Content | How it relaxes Paper 1 |
|------------|---------|----------------------|
| B1 | Experts are conditionally independent given state and true label | Generalizes A1+A2: allows overlapping training sets, only requires conditional independence structure |
| B2 | Noise is independent of features given state | Generalizes A4: allows state-dependent noise rates, only requires noise-feature conditional independence within state |
| B3 | State partition is measurable and experts are non-degenerate | New: minimal technical condition; replaces A5+A6 with a single non-degeneracy condition |

**Theorem: B1-B3 are necessary and sufficient for SCX to break the noise-difficulty unidentifiability (Theorem 3)**. Any relaxation of B1-B3 admits a counterexample where noise and intrinsic difficulty are observationally equivalent.

### 2.2 Proof Technique Comparison

| Component | Paper 1 | Paper 3 |
|-----------|---------|---------|
| Thm 1 (noise detection) | Hoeffding + Chernoff | Bernstein + Talagrand empirical process bound + local Rademacher complexity |
| Thm 2 (weak feature) | Fano + Pinsker | Le Cam + Assouad + Fano (triple) for minimax optimality; matching upper bound |
| Thm 3 (unidentifiability) | Constructive for K=2 | General semiparametric: noise-difficulty decomposition is a non-parametric identifiability problem; show tangent space is rank-deficient |
| New: Minimax lower bound | None | Matching lower bound proving SCX achieves optimal rate |
| New: PAC-Bayes | None | PAC-Bayes bound for noise detector with data-dependent prior |
| New: Adaptive bound | None | Adaptive threshold selection without A5 (state homogeneity), using empirical Bernstein |

### 2.3 Mathematical Depth Comparison

```
Paper 1:  Hoeffding → exponential convergence of F1
          Fano → state estimation error lower bound
          Constructive → unidentifiability

Paper 3:  Bernstein + empirical process → sharp concentration with variance dependence
          Talagrand's inequality → uniform deviation bound over states
          Le Cam's method → minimax lower bound matching upper bound
          Semiparametric tangent space → identifiability as rank condition
          PAC-Bayes → generalization bound for noise detector
          Information bottleneck → rate-distortion interpretation
```

### 2.4 Novelty Claims (for JMLR)

1. **First complete statistical theory for multi-expert noise detection** with state-conditioned reliability. Existing theory (Dawid-Skene, 1979) requires global confusion matrices; existing label-noise theory (Menon et al., 2015; Patrini et al., 2017) requires anchor points or known noise rates.

2. **Minimax optimality proof**: We show the SCX consistency detector achieves the minimax-optimal detection rate. Specifically, for any state with expert error rate $\mu_s$ and noise rate $\eta$, the optimal detection rate is $\Theta(\exp(-2M\Delta_s^2))$, and SCX achieves this up to constant factors.

3. **Semiparametric identifiability framework**: We formulate the noise-vs-difficulty distinction as a semiparametric identifiability problem, proving that the SCX assumptions (B1-B3) correspond exactly to the condition that the nuisance tangent space is orthogonal to the parameter of interest.

4. **Generalized Dawid-Skene equivalence**: We prove that SCX weighting reduces to Dawid-Skene weighting under trivial state partition, and that the improvement is lower-bounded by the mutual information $I(S; W)$ between states and optimal weights.

5. **Adaptive, assumption-free bounds**: We provide bounds that do not require knowledge of $\mu_s$ (state error rate), $\eta$ (noise rate), or $K$ (number of classes), using empirical Bernstein and adaptive threshold selection.

---

## 3. Complete Paper Anatomy

### 3.1 Overall Structure

| Section | Pages | Purpose | New Material |
|---------|-------|---------|-------------|
| 1. Introduction | 3 | Motivation, problem, contributions | — |
| 2. Problem Formulation | 4 | Statistical model, B1-B3, identifiability challenge | B1-B3, Thm 3' (semiparametric) |
| 3. Main Results | 14 | Theorems 1-3, Propositions 1 & 3 | All relaxed proofs |
| 3.1 Multi-Expert Consistency | 5 | Thm 1' (Bernstein + empirical process) | Bernstein, adaptive bound |
| 3.2 Weak Feature Lower Bound | 4 | Thm 2' (minimax + Le Cam) | Minimax optimality proof |
| 3.3 State-Conditioned Weighting | 3 | Prop 3' (Jensen, gap, monotonicity) | Gap lower bound, granularity |
| 3.4 Regret Lower Bound | 2 | Prop 1' (risk crossing) | Risk crossing characterization |
| 4. Connections to Existing Theory | 7 | Dawid-Skene, PAC-Bayes, coreset, IB | All new |
| 4.1 Dawid-Skene | 2 | Formal comparison theorem | Thm 4 (SCX $\supseteq$ DS) |
| 4.2 PAC-Bayes | 2 | PAC-Bayes generalization bound | Thm 5 (PAC-Bayes SCX) |
| 4.3 Coreset Theory | 1.5 | Compression fidelity connection | Thm 6 (Feldman-Langberg) |
| 4.4 Information Bottleneck | 1.5 | Rate-distortion view | Proposition on IB-SCX equivalence |
| 5. Simulations | 5 | Bound tightness validation | New synthetic experiments |
| 6. Discussion | 3 | Decision framework, open problems | — |
| A-H. Appendices | 10 | All proofs | Full proofs |

**Total**: ~46 pages (30 main + 10 appendices + 4 references)

### 3.2 Section-by-Section Specification

---

#### Section 1: Introduction (~3 pages)

**1.1 The Data Cleaning Problem as Statistical Inference**

- Opening: Every labeled dataset used for supervised learning contains noise. The question is not *whether* but *where*.
- Formalize: Given $(x_i, y_i)$ pairs and $M$ expert models $\{f_m\}$, infer which $(x_i, y_i)$ have corrupted labels.
- This is a missing-data problem: the true label $y^*$ is unobserved, and the noise indicator $z_i = \mathbb{1}\{y_i \neq y^*\}$ is the target.
- Statistical challenge: the joint distribution of $(X, Y, \{f_m(X)\})$ is observed, but the causal decomposition into "noise" and "difficulty" is not identified.

**1.2 Insufficiency of Existing Theory**

- **Dawid-Skene (1979) and variants**: Assume global confusion matrices $\pi_m(c'|c)$ that do not depend on $x$. This is violated in modern deep learning where expert accuracy varies across input subpopulations.
- **Label-noise transition matrix methods (Menon et al., 2015; Patrini et al., 2017; Northcutt et al., 2021)**: Assume the existence of anchor points (samples where true label is known with certainty) or known noise rates. These assumptions are often unverifiable.
- **Active learning / uncertainty methods**: Cannot distinguish aleatoric uncertainty (label noise) from epistemic uncertainty (model uncertainty about a clean but hard sample).
- **Ensemble disagreement methods (Lakshminarayanan et al., 2017)**: Use predictive variance as a proxy for noise, but lack theoretical guarantees for noise *detection* as opposed to uncertainty *estimation*.

**1.3 Our Framework: State-Conditioned Expert Reliability**

- Key insight: Partition the input space into *states* $\mathcal{S}$ such that within each state, expert reliability is approximately constant.
- Noise detection via multi-expert consistency: $C(x) = \frac{1}{M}\sum_m \mathbb{1}\{\ell(f_m(x), y) > \tau\}$.
- Under minimal assumptions (B1-B3), $C(x)$ separates noise from clean samples with exponential concentration.

**1.4 Contributions (Bulleted)**

1. Relaxed assumption framework (B1-B3) replacing A1-A6
2. Sharpened Theorem 1 with Bernstein + empirical process concentration
3. Minimax lower bound proving SCX achieves optimal rate
4. Semiparametric unidentifiability theorem (Thm 3 extended)
5. Formal connections to Dawid-Skene, PAC-Bayes, coreset theory, information bottleneck
6. Adaptive bounds requiring no knowledge of $\mu_s$, $\eta$, or $K$

---

#### Section 2: Problem Formulation (~4 pages)

**2.1 Statistical Model**

- Formal state-space model with latent variables:

$$X \sim P_X, \quad S = s(X) \in \mathcal{S}, \quad Y^* = f^*(X), \quad Y \mid (X, Y^*) \sim \text{Noise}(X, Y^*)$$

- Expert models $f_m$ are trained on datasets $D_m$, conditionally independent given state and true label (B1).
- Noise process: $P(Y \neq Y^* \mid X) = \eta(X)$ (general, not assumed constant).

**2.2 Minimal Assumptions (B1-B3)**

**B1 (Conditional Expert Independence)**:
$$P(f_1, \dots, f_M \mid X, Y^*) = \prod_{m=1}^M P(f_m \mid X, Y^*)$$

This relaxes A1+A2: no longer requires disjoint training sets, only that whatever dependence exists among experts is mediated by $(X, Y^*)$. This is testable via the residual correlation test described below.

*Discussion of testability*: Given a clean validation set, one can compute the residual correlation matrix of expert predictions and test the null hypothesis of conditional independence via a permutation test or the Hilbert-Schmidt independence criterion.

**B2 (Noise-Feature Conditional Independence Given State)**:
$$Y \perp X \mid S, Y^*$$

i.e., within a state, noise rate is constant: $\eta(X) = \eta_s$ for $X \in s$. This relaxes A4 (uniform global noise) to state-conditional uniformity.

*Discussion*: This is the key structural assumption. It says that state membership captures all information about how noise varies across the input space. States themselves can have different noise rates.

**B3 (Non-Degeneracy)**:
$$\forall s \in \mathcal{S}: \mu_s < \frac{K-1}{K}, \quad \text{and} \quad |\mathcal{S}| \geq 2$$

where $\mu_s = \mathbb{E}[C(X) \mid \text{clean}, X \in s]$. This replaces A5+A6 with a single, directly testable condition. The second condition ($|\mathcal{S}| \geq 2$) ensures that state conditioning is meaningful.

**2.3 The Identifiability Challenge**

- Even under B1-B3, is the noise-difficulty decomposition identifiable?
- Preview of Theorem 3 (extended): The noise-difficulty distinction is a semiparametric identifiability problem. The tangent space of the nuisance parameter (expert error patterns) is rank-deficient exactly when B1-B3 are violated.
- This section motivates why the three assumptions are *necessary* — they correspond to the condition that the parameter of interest (noise indicator) is orthogonal to the nuisance tangent space.

**2.4 The Consistency Score**

Definition and basic properties of $C(x) = \frac{1}{M}\sum_m e_m(x,y)$:

- $C(x) \in [0,1]$
- Under B1-B3: $\mathbb{E}[C \mid \text{clean}, x] \leq \mu_s$ and $\mathbb{E}[C \mid \text{noise}, x] \geq 1 - \mu_s/(K-1)$
- Separation condition: $\mu_s < (K-1)/K$ ensures $\mathbb{E}[C \mid \text{clean}] < \mathbb{E}[C \mid \text{noise}]$

---

#### Section 3: Main Results (~14 pages)

##### 3.1 Multi-Expert Consistency Guarantee (Theorem 1') (~5 pages)

**3.1.1 Statement**

**Theorem 1 (Sharpened Noise Detection Guarantee)**. Under assumptions B1-B3, for any state $s$ with threshold $\theta$ satisfying $\mu_s < \theta < 1 - \mu_s/(K-1)$, the SCX noise detector achieves:

**(a) Bernstein concentration (variance-dependent)**:

$$\mathbb{P}(C(x) > \theta \mid \text{clean}, x \in s) \leq \exp\left(-\frac{M(\theta - \mu_s)^2}{2\mu_s(1-\mu_s) + \frac{2}{3}(\theta - \mu_s)}\right)$$

$$\mathbb{P}(C(x) \leq \theta \mid \text{noise}, x \in s) \leq \exp\left(-\frac{M(1 - \mu_s/(K-1) - \theta)^2}{2(1 - \mu_s/(K-1))(\mu_s/(K-1)) + \frac{2}{3}(1 - \mu_s/(K-1) - \theta)}\right)$$

**(b) Empirical process bound (uniform over states)**:

$$\mathbb{P}\left(\sup_{s \in \mathcal{S}} |\hat{C}_s - \mathbb{E}[C_s]| > t\right) \leq |\mathcal{S}| \cdot \exp\left(-\frac{M t^2}{2\bar{\sigma}^2 + \frac{2}{3}t}\right)$$

where $\hat{C}_s$ is the empirical mean consistency in state $s$, and $\bar{\sigma}^2$ is the average variance.

**(c) F1 lower bound**:

$$\text{F1} \geq 1 - \frac{1}{\eta}\sum_{s \in \mathcal{S}} \rho_s \cdot \exp\left(-\frac{M\Delta_s^2}{2\mu_s(1-\mu_s) + \frac{2}{3}\Delta_s}\right)$$

where $\Delta_s = \min(\theta - \mu_s,\, 1 - \mu_s/(K-1) - \theta)$.

**Proof approach**:

1. Bernstein inequality (not Hoeffding) for bounded random variables with variance-dependence
2. Local Rademacher complexity for uniform convergence over states (Koltchinskii, 2006)
3. Combine via union bound over states with state-specific variances
4. For the F1 bound, decompose false positive and false negative rates state-wise

**3.1.2 Improvement over Paper 1**

| Aspect | Paper 1 (Hoeffding) | Paper 3 (Bernstein) |
|--------|---------------------|---------------------|
| Exponent | $2M\Delta^2$ | $\frac{M\Delta^2}{2\sigma^2 + 2\Delta/3}$ |
| Variance dependence | None (worst-case $\sigma^2=1/4$) | Adaptive to $\sigma^2 = \mu_s(1-\mu_s)$ |
| When variance is small | No improvement | $\sigma^2 \ll 1/4$ gives $2\times$ to $10\times$ tighter |
| Uniform bound | Union bound over states | Talagrand + local Rademacher |
| Threshold selection | Requires $\mu_s$ known | Adaptive via empirical Bernstein |

**3.1.3 Tightness Discussion**

- Show that the Bernstein exponent cannot be improved: matching lower bound via the central limit theorem approximation.
- For $\mu_s \ll 1$ (reasonably good experts), $2\mu_s(1-\mu_s) \ll 1/2$, so Bernstein exponent is $2\times$ to $5\times$ larger than Hoeffding's worst-case.

**3.1.4 Adaptive Threshold via Empirical Bernstein**

- Without knowing $\mu_s$, estimate $\hat{\mu}_s$ from clean validation samples.
- Apply empirical Bernstein (Audibert et al., 2007; Maurer & Pontil, 2009) for data-dependent thresholding.
- Bound the penalty for estimation: $\tilde{\mu}_s = \hat{\mu}_s + \sqrt{\frac{2\hat{V}_s \log(2/\delta)}{n_s}} + \frac{7\log(2/\delta)}{3n_s}$ where $\hat{V}_s$ is empirical variance.

---

##### 3.2 Weak Feature Lower Bound (Theorem 2') (~4 pages)

**3.2.1 Statement**

**Theorem 2 (Minimax Lower Bound for Weak Feature Detection)**. Let $\phi: \mathcal{X} \to \Phi$ be a feature mapping with $I(\phi(X); S) \leq \delta$. For any noise detection algorithm $\mathcal{A}$ operating on $(\phi(X), Y, \{f_m(X)\})$, the minimax risk satisfies:

**(a) AUC**:

$$\inf_{\mathcal{A}} \sup_{P \in \mathcal{P}_\delta} \left(\text{AUC}_{\text{base}} - \text{AUC}(\mathcal{A})\right) \geq \frac{1}{2} \cdot \sqrt{\frac{\delta}{2}} \cdot \left(\frac{1}{\eta} + \frac{1}{1-\eta}\right)$$

where $\mathcal{P}_\delta$ is the set of distributions satisfying $I(\phi(X); S) \leq \delta$.

**(b) F1**:

$$\inf_{\mathcal{A}} \sup_{P \in \mathcal{P}_\delta} \left(\text{F1}_{\text{base}} - \text{F1}(\mathcal{A})\right) \geq \frac{C_F}{2} \cdot \sqrt{\frac{\delta}{2}}$$

**(c) Rate optimality**: The SCX detector achieves the above lower bound up to constant factors:

$$\text{AUC}_{\text{SCX}} - \text{AUC}_{\text{base}} \leq 2 \cdot \sqrt{\frac{\delta}{2}} \cdot \left(\frac{1}{\eta} + \frac{1}{1-\eta}\right)$$

**Proof approach (three techniques for tightness)**:

1. **Le Cam's method**: Two-point lower bound. Construct two distributions $P_1, P_2$ with $TV(P_1, P_2) \leq \sqrt{\delta/2}$ such that optimal AUC differs by at least the claimed gap. This establishes the $\sqrt{\delta}$ rate.

2. **Fano's inequality (existing)**: For the state-estimation subproblem, Fano gives $P(\hat{S} \neq S) \geq (H(S) - \delta - \log 2)/\log K$, confirming that the information-theoretic difficulty is fundamental.

3. **Assouad's lemma (for matching lower bound)**: For $K$ states, construct $2^K$ hypotheses differing in which states have high noise. Assouad gives a lower bound of $\Omega(\sqrt{K} \cdot \sqrt{\delta})$ for the multi-state case, matching the $|\mathcal{S}|$ factor in the upper bound.

**3.2.2 Rate Optimality Proof**

The key result is that the SCX detector is **minimax optimal**: no algorithm can asymptotically outperform it under the same information constraints. The proof establishes matching upper and lower bounds:

- Upper bound: Theorem 1 gives $\text{F1} \geq 1 - \mathcal{O}(e^{-2M\Delta^2})$
- Lower bound: Theorem 2 gives $\text{F1}_{\text{any}} \leq \text{F1}_{\text{base}} + \mathcal{O}(\sqrt{\delta})$

The gap between $\mathcal{O}(e^{-2M\Delta^2})$ and $\mathcal{O}(\sqrt{\delta})$ is not a contradiction: the upper bound is for expert variance $M$ (number of experts), while the lower bound is for feature information $\delta$. SCX is simultaneously optimal in both regimes:
- For large $M$: SCX achieves exponential convergence, which is optimal (matching lower bound shows $\Omega(e^{-cM})$)
- For weak features: SCX degrades gracefully, and is optimal in the minimax sense (matching $O(\sqrt{\delta})$)

**3.2.3 Practical Characterization of Weakness**

Extend the definition of $\delta$-weak features to include:

- **Computational weak features**: Features where mutual information $I(\phi; S)$ is high but clustering algorithms (k-means, spectral, GMM) fail to recover $S$ due to non-convexity or initialization. This is captured by $\varepsilon_{\text{k-means}}$ in Proposition 6.
- **Sample-limited weakness**: When $n_s$ (samples per state) is small, the empirical estimate $\hat{C}_s$ has high variance. The effective weakness is $\delta_{\text{eff}} = \delta + \mathcal{O}(1/\sqrt{n_{\min}})$.

---

##### 3.3 State-Conditioned Weighting (Proposition 3') (~3 pages)

**3.3.1 Statement**

**Proposition 1 (State-Conditioned Weighting Dominance)**. Under B1-B3, for any loss $\ell$ satisfying Lipschitz continuity:

$$R_{\text{SC}} \leq R_{\text{Global}}$$

where $R_{\text{SC}} = \mathbb{E}_s[\min_w \mathbb{E}_{x,y|s}[\ell(f_w(x), y)]]$ is the state-conditioned risk and $R_{\text{Global}} = \min_w \mathbb{E}_{x,y}[\ell(f_w(x), y)]$ is the best global risk.

**3.3.2 Jensen's Inequality Proof (Concise)**

Key insight: $\varphi(P) = \min_w \mathbb{E}_{P}[\ell(f_w)]$ is a concave functional of the distribution $P$. Jensen gives $\varphi(\mathbb{E}_S[P_{X,Y|S}]) \geq \mathbb{E}_S[\varphi(P_{X,Y|S})]$, i.e., $R_{\text{Global}} \geq R_{\text{SC}}$.

**3.3.3 Gap Quantification**

**Theorem (Gap Lower Bound)**. The state-conditioning advantage $\Delta = R_{\text{Global}} - R_{\text{SC}}$ satisfies:

$$\Delta \geq \frac{1}{\alpha} \cdot I(S; W^*)$$

where $I(S; W^*) = \mathbb{E}_S[\text{KL}(w^*(S) \| \bar{w}^*)]$ is the mutual information between states and optimal state-conditioned weights, $\bar{w}^*$ is the globally optimal weight, and $\alpha$ is the inverse-temperature parameter of the SCX weighting formula.

**Proof**: Uses the information-theoretic characterization of the SCX weighting formula $w_m(x) \propto \exp(-\alpha \hat{R}_m(s(x)))$ and the fact that the gradient of the risk with respect to weights is bounded by $\alpha$.

**3.3.4 Monotonicity in State Granularity**

For nested state partitions $\mathcal{S}_1 \subseteq \mathcal{S}_2$:

$$\Delta_{\mathcal{S}_2} \geq \Delta_{\mathcal{S}_1}$$

Proof via the Jensen perspective: finer partitions give more conditioning, which increases the concavity benefit.

---

##### 3.4 Regret Lower Bound (Proposition 1') (~2 pages)

**3.4.1 Statement**

**Proposition 2 (Regret Lower Bound)**. For any fixed global expert $m^*$:

$$\text{Regret}(m^*) \geq P(\mathcal{S}_{\text{bad}}(m^*)) \cdot \delta_{\min}$$

where $\mathcal{S}_{\text{bad}}(m^*) = \{s : m^* \notin \arg\min_m R_m(s)\}$ and $\delta_{\min} = \min_s \delta(s)$ is the minimum gap between best and second-best expert.

**3.4.2 Risk Crossing Characterization**

- **Co-monotonicity test**: Expert risk functions are co-monotonic iff $\text{Regret}=0$ for the best global expert.
- **Crossing $\implies$ positive regret**: If risk functions cross, $\Delta > 0$ for strictly convex losses.
- **Minimax regret over all experts**: $\min_{m^*} \text{Regret}(m^*) \geq \frac{K-1}{K} \cdot \delta_{\min}$ for $K$ states with uniform state masses.

---

#### Section 4: Connections to Existing Theory (~7 pages)

##### 4.1 Dawid-Skene Generalization (Theorem 4) (~2 pages)

**Theorem 4 (SCX Generalizes Dawid-Skene)**.

- Under the trivial state partition $\mathcal{S} = \{\mathcal{X}\}$, SCX weighting reduces to Dawid-Skene weighting with inverse-temperature softmax.
- For any non-trivial partition, SCX strictly dominates Dawid-Skene when expert reliability varies across states.
- The improvement is lower bounded by $\Delta R \geq \frac{1}{\alpha} I(S; W)$.

**4.1.1 Proof Structure**

1. Define Dawid-Skene model: $\pi_m(c'|c) = P(f_m(x)=c' | y^*=c)$, constant across $x$.
2. Show that SCX with $|\mathcal{S}|=1$ gives $\hat{y}(x) = \arg\max_c \sum_m w_m \cdot \mathbb{1}\{f_m(x)=c\}$ where $w_m \propto \exp(-\alpha R_m)$.
3. Show that the DS EM algorithm converges to the same fixed point as SCX with hard state assignment and $|\mathcal{S}|=1$.
4. For $|\mathcal{S}| > 1$, construct a counterexample where DS weighting is suboptimal: two states with inverse expert rankings.

**4.1.2 Comparison Table**

| Dimension | Dawid-Skene | SCX (this paper) |
|-----------|-------------|------------------|
| Expert reliability | Global $\pi_m$ | State-dependent $\pi_m(s)$ |
| Noise detection | Posterior $P(y^*|y, \{f_m\})$ | Consistency score $C(x)$ |
| Theoretical guarantee | Asymptotic consistency | Exponential convergence |
| Minimum experts | Usually $\geq 3$ | Any $M \geq 2$ |
| Feature dependence | None | Critical (state discovery) |
| Identifiability | Label permutation | Noise vs difficulty |

##### 4.2 PAC-Bayes Interpretation (Theorem 5) (~2 pages)

**Theorem 5 (PAC-Bayes Bound for Noise Detector)**. Let $\mathcal{D}$ be the data distribution, and let $\mathcal{H}$ be the hypothesis class of noise detectors of the form $h(x) = \mathbb{1}\{C(x) > \theta\}$. For any prior $\pi$ over $\mathcal{H}$ and any $\delta \in (0,1)$, with probability $\geq 1-\delta$ over the training sample $S \sim \mathcal{D}^n$:

$$\mathbb{E}_{\mathcal{D}}[\ell(h, z)] \leq \mathbb{E}_{S}[\ell(h, z)] + \sqrt{\frac{\text{KL}(Q \| \pi) + \log(2n/\delta)}{2n-1}}$$

where $Q$ is the posterior over detectors and $z$ is the noise indicator.

**4.2.1 Application to SCX**

- The SCX noise detector with data-dependent threshold $\hat{\theta}$ can be interpreted as a PAC-Bayes posterior that concentrates on thresholds separating clean and noise consistency scores.
- The KL divergence $\text{KL}(Q \| \pi)$ captures the "information cost" of learning the threshold, which is bounded by $\mathcal{O}(\log M + \log |\mathcal{S}|)$.
- This gives a generalization bound for the SCX detector that does not require A1-A6 — only that the consistency score is computed from independent experts.

**4.2.2 Relationship to Theorem 1**

- Theorem 1 gives a **distribution-specific** bound based on $\mu_s$, $\eta$, and $K$.
- The PAC-Bayes bound gives a **data-dependent** bound that holds for any data distribution.
- The two bounds are complementary: Theorem 1 is tighter when structural assumptions hold; PAC-Bayes is more general.

##### 4.3 Relationship to Coreset Theory (Theorem 6) (~1.5 pages)

**Theorem 6 (SCX-Compress and Feldman-Langberg Framework)**. The SCX-Compress algorithm is a state-conditioned variant of the Feldman-Langberg (2011) coreset construction, with:

1. Sensitivity proxy: $D_i$ (redundancy score) replaces the exact sensitivity $\sigma_i$.
2. State-level decomposition: Total sensitivity $T = \sum_s T_s$ where $T_s \leq 1$ per state due to redundancy compression.
3. Error bound: The compression fidelity error $\varepsilon(s) \leq B \cdot (1-D_{\text{eff}}(s)) \cdot (1 - n_s'/N_s) + \mathcal{O}(B\sqrt{d(1-D_{\text{eff}}(s))/n_s'})$.

**4.3.1 Key Insight**

The Feldman-Langberg framework requires computing per-sample sensitivity $\sigma_i = \sup_{f \in \mathcal{F}} \frac{|\ell_f(z_i)|}{\sum_j |\ell_f(z_j)|}$, which is typically intractable. SCX-Compress uses state-conditioned redundancy $D_i$ as a proxy, validated by Theorem 1's noise detection guarantee. The price is an additional $\mathcal{O}(1/\sqrt{M})$ error term from the consistency approximation.

**4.3.2 Comparison with Random Sampling**

- Random sampling: error $\mathcal{O}(\sqrt{d/n_s'})$ with probability $1-\delta$.
- SCX-Compress: error $\mathcal{O}(\sqrt{d(1-D_{\text{eff}})/n_s'})$ with the same probability.
- Advantage: When $D_{\text{eff}}(s) \to 1$, the VC-dimension dependence is effectively reduced to $\tilde{d} = d \cdot (1-D_{\text{eff}}) \ll d$.

##### 4.4 Information Bottleneck Perspective (~1.5 pages)

**Proposition (Information Bottleneck Interpretation of SCX)**. The SCX state discovery and noise detection procedure is equivalent to solving a two-stage information bottleneck problem:

**Stage 1 (State Discovery)**:
$$\min_{P(S|X)} I(X; S) - \beta I(S; Y)$$

where $S$ is the state variable, $X$ is the input, and $Y$ is the label. This recovers the optimal state partition.

**Stage 2 (Noise Detection)**:
$$C(x) = \frac{1}{M} \sum_m \mathbb{1}\{\ell(f_m(x), y) > \tau\}$$

is a sufficient statistic for $Z$ (noise indicator) given $S$, i.e., $I(S, C(X); Z) = I(S; Z) + \mathcal{O}(e^{-M})$.

**4.4.1 Connection to Rate-Distortion**

The relationship between the number of states $K$ and the noise detection F1 is a rate-distortion tradeoff: finer state partitions require more information (higher $I(X; S)$) but enable better noise detection (lower distortion). The optimal $K^*$ satisfies:

$$K^* = \arg\min_K \left[ \underbrace{I(X; S_K)}_{\text{information cost}} + \lambda \underbrace{D(S_K)}_{\text{distortion}} \right]$$

where $D(S_K) = 1 - \text{F1}(S_K)$ and $\lambda$ is a Lagrange multiplier determined by application requirements.

---

#### Section 5: Simulations and Case Studies (~5 pages)

**5.1 Synthetic Validation of Bound Tightness**

- **Setup**: Generate synthetic data with known $\mu_s$, $\eta$, $K$, $M$, and state structure.
- **Experiment 1 (Theorem 1 tightness)**: Vary $M$ from 2 to 100, measure empirical F1 vs. theoretical lower bound. Compute ratio $\text{F1}_{\text{empirical}} / \text{F1}_{\text{bound}}$. Show that Bernstein bound is tighter than Hoeffding by factor 2-5.
- **Experiment 2 (Theorem 2 tightness)**: Vary $\delta$ by controlling feature quality. Compute SCX AUC improvement over baseline vs. theoretical upper bound. Show that the $\mathcal{O}(\sqrt{\delta})$ rate is optimal.
- **Experiment 3 (Adaptive threshold)**: Compare fixed-threshold (Paper 1) vs. adaptive empirical-Bernstein threshold (Paper 3) across varying $\mu_s$. Show adaptive threshold closes the gap when $\mu_s$ is misspecified.

**5.2 Reference to Paper 1 Results**

Use the same experimental data as Paper 1 (AlN v3 MLIP, CIFAR-10/100, MedMNIST) but with a focus on:

- **Bound tightness analysis**: For each dataset, compute the empirical F1 and compare with the Bernstein bound and the Hoeffding bound. Show that the Bernstein bound is uniformly tighter.
- **Weak feature diagnosis**: For AlN v3 (12-dim handcrafted features) vs. ACE, compute $I(\phi; S)$ and show that Theorem 2's prediction ($\text{F1}_{\text{SCX}} \approx \text{F1}_{\text{base}}$) holds.
- **Dawid-Skene comparison**: Re-analyze the CIFAR-10 experiment with SCX vs. Dawid-Skene weighting, showing the gap $\Delta R$ and its correlation with $I(S; W)$.

**5.3 Bound Visualization Figures**

- **Figure 1**: F1 vs. $M$ for varying $\mu_s$. Three curves: empirical, Bernstein bound (Thm 1'), Hoeffding bound (Paper 1).
- **Figure 2**: SCX AUC minus baseline AUC vs. $\sqrt{\delta}$ for varying $\eta$. Show linear relationship.
- **Figure 3**: Gap $\Delta$ vs. $I(S; W)$ for varying state partitions. Show monotonic relationship.
- **Figure 4**: Decision boundary diagram: regions where SCX succeeds, fails, and is in the transition regime (function of $\delta$ and $M$).

---

#### Section 6: Discussion (~3 pages)

**6.1 When to Use SCX: A Decision Framework**

```
Input: Data (X, Y), M experts, feature mapping φ

Step 1: Is M ≥ 2?
   No → Cannot compute consistency score. Use loss-based methods.
   Yes → Continue.

Step 2: Estimate I(φ(X); S) (mutual information between features and true states)
   Low (εφ < 0.2) → SCX likely effective. Continue.
   Medium (0.2 ≤ εφ ≤ 0.5) → SCX partially effective. Strengthen features.
   High (εφ > 0.5) → Weak feature regime. SCX may not beat loss baseline.

Step 3: Estimate μs (state-level expert error rate)
   μs ≥ (K-1)/K → Noise detection impossible. Consider different approach.
   μs << (K-1)/K → SCX noise detection should work.

Step 4: Apply SCX. Monitor diagnostic:
   - State consistency variance Var(C(s)): low → good
   - Gap between SCX F1 and loss-baseline F1: large → good
```

**6.2 Open Problems**

1. **Optimal expert construction**: Given a fixed dataset and computational budget, how should experts be designed to maximize $I(S; \{f_m\})$? This is a feature learning problem for which we currently lack guarantees.

2. **Feature learning for SCX**: Can the two-layer descriptor strategy (physical descriptors + error-driven clustering be replaced by an end-to-end learned representation that directly maximizes $I(S; Z)$?

3. **Adaptive state discovery**: How to choose the optimal number of states $K$ in a data-driven way? Current methods use heuristics (elbow, silhouette); a theoretical criterion based on the rate-distortion tradeoff (Section 4.4) is possible but unproven.

4. **Beyond classification**: Extend the theory to regression settings where $K \to \infty$ and the separation condition $\mu_s < (K-1)/K$ is automatically satisfied. Is the exponential convergence rate preserved?

5. **Dependent experts**: When A1 is violated and experts share training data, can a correction term be derived? Initial results suggest a $\rho^2$ penalty where $\rho$ is the average pairwise training set overlap.

---

## 4. Existing Material Inventory

### 4.1 Ready-to-Use Content (Minimal Changes)

| File | Content | Use in Paper 3 |
|------|---------|----------------|
| `03_unidentifiability_theorem.md` | Theorem 3 complete with K=2 and K>2 proofs, 6 corollaries, literature connections | Section 2.3 (motivation) + Section 4 (Dawid-Skene connection) |
| `01_regret_lower_bound.md` | Proposition 1 (regret lower bound), co-monotonicity characterization, empirical bound | Section 3.4 |
| `03_state_conditioned_weighting_proof.md` | Proposition 3 (state-conditioned dominance), Jensen proof, gap theorem, monotonicity | Section 3.3 |
| `01_noise_detection_guarantee.md` | Theorem 1 (Hoeffding version), Lemma 1 (mean separation), Lemma 2, Lemma 3, Chernoff appendix | Section 3.1 (baseline for comparison) |
| `02_weak_feature_failure.md` | Theorem 2 (Pinsker version), Fano lemma, degeneration analysis | Section 3.2 (baseline) |

### 4.2 Content Requiring Rewriting (Major Changes)

| File | What Changes | New Content Needed |
|------|-------------|-------------------|
| `01_noise_detection_guarantee.md` | Hoeffding $\to$ Bernstein, add adaptive bound, empirical process bound, minimax lower bound | Section 3.1 entirely new proof; current Lemma 1 (mean separation) preserved |
| `02_weak_feature_failure.md` | Add Le Cam + Assouad lower bounds, rate optimality proof, matching upper bound | New: minimax framework, three lower-bound techniques, rate optimality theorem |
| `03_unidentifiability_theorem.md` | Add semiparametric formulation, tangent space analysis | New: Section 2.3 (identifiability as rank condition) |

### 4.3 Content to Create from Scratch

| Section | Content | Difficulty |
|---------|---------|------------|
| 4.1 Dawid-Skene comparison theorem | Theorem 4 (formal comparison) | Medium |
| 4.2 PAC-Bayes bound | Theorem 5 (PAC-Bayes noise detection) | Medium |
| 4.3 Coreset connection | Theorem 6 (Feldman-Langberg comparison) | Low (exists in Proposition 4) |
| 4.4 Information Bottleneck | Proposition and rate-distortion tradeoff | Medium |
| 5. Simulations | Synthetic experiments code | Low (code needs writing) |

---

## 5. New Mathematical Contributions Required

### 5.1 Minimax Lower Bound Matching Theorem 1's Upper Bound

**Status**: Draft needed  
**Importance**: Critical for JMLR acceptance  
**Content**:

- Show that the exponent $\exp(-2M\Delta_s^2)$ in Theorem 1 is optimal up to constant factors.
- Use Le Cam's two-point method: construct two distributions $P_0$ (clean) and $P_1$ (noisy) with $\chi^2$ divergence bounded by $4\Delta_s^2 M$, giving minimax error $\geq \frac{1}{2}(1 - \sqrt{2M\Delta_s^2})$ for testing $H_0$ vs $H_1$.
- Extend to F1: show that no detector can achieve $\mathbb{E}[\text{F1}] \geq 1 - c \cdot e^{-2M\Delta^2}$ for $c < 1/2$.

### 5.2 Relaxation of A1 (Disjoint Training Sets)

**Status**: Draft needed  
**Importance**: High (most practically restrictive assumption)  
**Content**:

- Replace A1 with "experts are conditionally independent given true label and state" (B1).
- Derive corrected concentration bound under dependent experts:
  - Let $\rho_{mm'} = \text{Corr}(e_m, e_{m'} \mid \text{clean}, x)$ be the residual correlation.
  - Effective sample size: $M_{\text{eff}} = M / (1 + (M-1)\bar{\rho})$ where $\bar{\rho}$ is average pairwise correlation.
  - Theorem 1 holds with $M$ replaced by $M_{\text{eff}}$.
  - Empirical estimation of $\bar{\rho}$ from validation data.

### 5.3 Relaxation of A4 (Uniform Noise)

**Status**: Draft needed  
**Importance**: High  
**Content**:

- Replace A4 with B2: noise-feature independence given state.
- Revised Lemma 1 for state-dependent noise rate $\eta_s$:
  - $\mathbb{E}[C \mid \text{noise}, X \in s] = 1 - \frac{1}{K-1} \cdot \mathbb{E}[C \mid \text{clean}, X \in s]$
  - (No change! The expectation is the same because noise, given state, is uniform over incorrect labels.)
- But the variance changes: $\text{Var}(C \mid \text{noise}, X \in s) = \frac{1}{M}\sigma_s^2$ where $\sigma_s^2$ depends on $\eta_s$.
- The F1 bound uses $\eta_s = \mathbb{P}(\text{noise} \mid X \in s)$ instead of global $\eta$.

### 5.4 Relaxation of A5 (State Homogeneity)

**Status**: Draft needed  
**Importance**: Medium  
**Content**:

- Replace A5 with a weak homogeneity condition: for each state $s$, the variance of $\mathbb{E}[C \mid \text{clean}, X]$ across $X \in s$ is bounded by $V_s$.
- Adaptive threshold: $\hat{\theta}_s = \hat{\mu}_s + \sqrt{\frac{2\hat{V}_s \log(2M/\delta)}{n_s}}$.
- The price of adaptation: an additional $\mathcal{O}(V_s)$ term in the exponent.
- When $V_s = 0$ (exact homogeneity), recover Paper 1 bound.

### 5.5 PAC-Bayes Generalization for the Noise Detector

**Status**: Draft needed  
**Importance**: Medium (strengthens theory)  
**Content**:

- Define hypothesis class $\mathcal{H} = \{h_\theta: h_\theta(x) = \mathbb{1}\{C(x) > \theta\}, \theta \in [0,1]\}$.
- Prior $\pi$ over $\mathcal{H}$: uniform over $\Theta = [\theta_{\min}, \theta_{\max}]$.
- Posterior $Q$: data-dependent threshold selection.
- PAC-Bayes bound: $\mathbb{E}_{\mathcal{D}}[\ell(h_\theta, z)] \leq \hat{R}_n(\theta) + \sqrt{\frac{\text{KL}(Q\|\pi) + \log(2n/\delta)}{2n-1}}$.
- Show $\text{KL}(Q \| \pi) \leq \log(|\mathcal{S}| \cdot M)$ for SCX's threshold selection.

### 5.6 Formal Dawid-Skene Comparison Theorem

**Status**: Draft needed  
**Importance**: Medium (positions SCX in literature)  
**Content**:

- Theorem: SCX weighting strictly dominates Dawid-Skene weighting when expert risk functions cross across states.
- Proof via Jensen's inequality and the concavity of the minimum operator.
- Gap lower bound: $\Delta R \geq \frac{1}{\alpha} I(S; W^*)$.
- Empirical identification: $\hat{I}(S; W)$ computed from estimated weights correlates with $\hat{\Delta}$.

### 5.7 Adaptive Bound Without A5 (State Homogeneity)

**Status**: Draft needed  
**Importance**: Medium (practical utility)  
**Content**:

- Use empirical Bernstein inequality (Audibert et al., 2007) for state-level thresholding.
- Bound: $\mathbb{P}(C > \hat{\theta}_s \mid \text{clean}, X \in s) \leq \exp\left(-\frac{n_s(\hat{\theta}_s - \hat{\mu}_s)^2}{2\hat{V}_s + \frac{2}{3}(\hat{\theta}_s - \hat{\mu}_s)}\right)$.
- This holds without knowing $\mu_s$ or $\sigma_s^2$, at the cost of $n_s$ samples per state.
- The price of adaptation: $\hat{\theta}_s$ requires $\mathcal{O}(1/\sqrt{n_s})$ margin to ensure the bound holds.

---

## 6. Theorem Mapping: Paper 1 to Paper 3

### 6.1 Cross-Reference Table

| Paper 1 ID | Paper 3 ID | Change | Section |
|------------|------------|--------|---------|
| Theorem 1 | Theorem 1' | Hoeffding $\to$ Bernstein, additive empirical process bound, adaptive threshold | 3.1 |
| Lemma 1 | Lemma 1 | No change (mean separation is fundamental and assumption-independent) | 3.1.1 |
| Lemma 2 | Lemma 2' | Hoeffding $\to$ Bernstein | 3.1.1 |
| Lemma 3 | Lemma 3' | Hoeffding $\to$ Bernstein, A6 $\to$ B3 | 3.1.1 |
| Theorem 2 | Theorem 2' | Add Le Cam + Assouad, minimax optimality, matching bounds | 3.2 |
| Lemma 1 (Thm 2) | Lemma 4 (Fano) | No change | 3.2 |
| Lemma 2 (Thm 2) | Lemma 5 (Degeneration) | Add computational weakness | 3.2 |
| Theorem 3 | Theorem 3' | Add semiparametric formulation, general $K$ proof | 2.3 |
| Corollaries 1-6 | Corollaries 1-6 | No change | 2.3 |
| Proposition 1 | Proposition 2 | Restructured as regret lower bound | 3.4 |
| Proposition 3 | Proposition 1 | Jensen proof, gap quantification | 3.3 |
| Proposition 4 | Theorem 6 | Feldman-Langberg connection | 4.3 |
| — | Theorem 4 | Dawid-Skene comparison | 4.1 |
| — | Theorem 5 | PAC-Bayes bound | 4.2 |
| — | Proposition 4 | Information bottleneck interpretation | 4.4 |
| — | Proposition 5 | Relaxed A1 concentration (dependent experts) | 3.1.5 |
| — | Proposition 6 | Relaxed A4 (state-dependent noise) | 3.1.5 |

### 6.2 Cumulative Dependency Graph

```
Thm 3 (Unidentifiability)
    └── motivates assumptions B1-B3
        ├── Thm 1' (Noise Detection) ─── Prop 5 (Dependent experts)
        │         └── Prop 6 (State-dependent noise)
        │         └── Thm 5 (PAC-Bayes)
        ├── Thm 2' (Weak Feature) ─── Thm 6 (Feldman-Langberg)
        ├── Prop 1 (Weighting) ─── Thm 4 (Dawid-Skene)
        │         └── Prop 4 (IB interpretation)
        └── Prop 2 (Regret)
```

Theorem 3 is foundational: it proves that without B1-B3, noise detection is impossible. Theorem 1' and Theorem 2' are the main positive and negative results under B1-B3. The propositions and connection theorems build on these.

---

## 7. Drafting Priority and Readiness

### 7.1 Status Overview

| Section | Draft Status | Estimated Effort | Dependencies |
|---------|-------------|------------------|-------------|
| 1. Introduction | Ready to draft | 1 day | None |
| 2.1-2.2 Problem + Assumptions | Ready to draft | 2 days | None |
| 2.3 Identifiability (Thm 3') | Mostly ready (from existing Thm 3) | 0.5 days | Semiparametric formalism |
| 3.1.1 Mean separation lemma | Ready (Lemma 1 unchanged) | 0 days | None |
| 3.1.2 Bernstein concentration | Needs proof work | 3 days | None |
| 3.1.3 Empirical process bound | Needs proof work | 4 days | Talagrand inequality |
| 3.1.4 Adaptive threshold | Needs proof work | 2 days | Empirical Bernstein |
| 3.1.5 Relaxed assumptions | Needs proof work | 3 days | Dependent expert bound |
| 3.2.1 Fano lemma | Ready | 0.5 days | None |
| 3.2.2 Le Cam + Assouad | Needs proof work | 4 days | Minimax framework |
| 3.2.3 Rate optimality | Needs proof work | 2 days | Matching bounds |
| 3.3 Weighting dominance | Mostly ready (from Prop 3) | 0.5 days | None |
| 3.3 Gap quantification | Needs proof work | 1 day | None |
| 3.4 Regret bound | Ready (from Prop 1) | 0.5 days | None |
| 4.1 Dawid-Skene | Needs writing | 2 days | Section 3.3 |
| 4.2 PAC-Bayes | Needs proof + writing | 3 days | None |
| 4.3 Coreset | Mostly ready (from Prop 4) | 0.5 days | None |
| 4.4 IB perspective | Needs writing | 1 day | None |
| 5. Simulations | Needs code + writing | 5 days | All proofs done |
| 6. Discussion | Ready to draft | 1 day | None |
| Appendices | Needs proof transcription | 5 days | All proofs done |

**Total estimated effort**: ~40 working days (full-time equivalent)

### 7.2 Drafting Order (Recommended)

**Phase 1 (Week 1-2): Core proofs — independent, highest impact**
1. Bernstein concentration for Theorem 1 (3.1.2)
2. Minimax lower bound via Le Cam (3.2.2)
3. Adaptive threshold + empirical Bernstein (3.1.4)

**Phase 2 (Week 3-4): Remaining proofs — some dependencies**
4. Relaxed assumptions: dependent experts + state-dependent noise (3.1.5)
5. PAC-Bayes bound (4.2)
6. Gap quantification for weighting (3.3.3)

**Phase 3 (Week 5-6): Connection theorems — require Phase 1+2**
7. Dawid-Skene comparison theorem (4.1)
8. Rate optimality proof (3.2.3) — requires both upper and lower bounds
9. Information bottleneck interpretation (4.4)

**Phase 4 (Week 7-8): Writing and figures**
10. Sections 1, 2: Introduction and problem formulation
11. Section 6: Discussion
12. Simulation code and figures
13. Appendices: all proofs

---

## 8. Timeline and Milestones

### 8.1 Relative to Paper 1 Submission

```
Paper 1 submitted to Nature        [T0]
    ↓ 2 weeks
Paper 1 on arXiv (priority date)   [T0 + 2w]
    ↓ 1 week
Begin Paper 3 drafting             [T0 + 3w]
    ↓ 2 months
Paper 3 first draft complete       [T0 + 11w]
    ↓ 2 weeks (internal review)
Paper 3 second draft               [T0 + 13w]
    ↓ 3 months (co-author feedback, polishing)
Paper 3 submission to JMLR         [T0 + 26w] (~6 months after Paper 1)

Possible accelerator: If Paper 1 is desk-rejected and resubmitted,
Paper 3 can still proceed independently since the theory is self-contained.
```

### 8.2 Key Milestones

| Milestone | Deliverable | Date (from Paper 1 submission) |
|-----------|-------------|-------------------------------|
| M1 | Bernstein concentration proof complete | T0 + 4w |
| M2 | Minimax lower bound proof complete | T0 + 6w |
| M3 | All main theorems proved | T0 + 8w |
| M4 | All connection theorems drafted | T0 + 10w |
| M5 | Full first draft | T0 + 11w |
| M6 | Simulation results complete | T0 + 12w |
| M7 | Internal review complete | T0 + 13w |
| M8 | Second draft + proofreading | T0 + 16w |
| M9 | Submission-ready | T0 + 26w |

### 8.3 Risk Factors

1. **Talagrand inequality for empirical process bound**: This is technically challenging. Fallback: use union bound over states with Bernstein (weaker but sufficient for main results).

2. **Le Cam lower bound tightness**: The matching constant may be off by a factor. Acceptable as long as rate is optimal.

3. **Simulation computational cost**: Synthetic experiments are cheap (python, no GPU). Risk is low.

4. **Length limit**: JMLR has no strict page limit. TMLR has a 36-page limit. Target: 30-40 pages including appendices.

---

## Appendix A: Suggested Notation for Paper 3

Unified notation to use throughout the paper:

| Symbol | Meaning | Equivalent in Paper 1 |
|--------|---------|-----------------------|
| $\mathcal{X}$ | Input space | Same |
| $\mathcal{Y}$ | Label space | Same |
| $K = \|\mathcal{Y}\|$ | Number of classes | Same |
| $f^*$ | True labeling function | Same |
| $\{f_m\}_{m=1}^M$ | Expert models | Same |
| $e_m(x) = \mathbb{1}\{\ell(f_m(x), y) > \tau\}$ | Expert error indicator | Same |
| $C(x) = M^{-1}\sum_m e_m(x)$ | Consistency score | Same |
| $\mathcal{S}$ | State space | Same |
| $s(x) \in \mathcal{S}$ | State assignment | Same |
| $\rho_s = P(X \in s)$ | State probability | Same |
| $\mu_s = \mathbb{E}[C \mid \text{clean}, s]$ | State clean error rate | Same |
| $\theta$ | Detection threshold | Same |
| $\eta_s = P(\text{noise} \mid s)$ | State noise rate (new: generalizes global $\eta$) | $\eta$ (global) |
| $\delta = I(\phi(X); S)$ | Feature-state mutual information | Same |
| $\phi(X)$ | Feature representation | Same |
| $\Delta_s$ | Separation gap | Same |
| $B = \{B1, B2, B3\}$ | Minimal assumptions (new) | $A = \{A1, \dots, A6\}$ |
| $M_{\text{eff}}$ | Effective expert count under dependence (new) | $M$ |
| $\bar{\rho} = \frac{2}{M(M-1)}\sum_{m<m'}\rho_{mm'}$ | Average expert correlation (new) | — |

---

## Appendix B: Key Open Questions for the Proof Drafting Phase

These questions must be resolved during the proof-drafting phase and will determine the exact form of the theorems:

1. **Bernstein vs. Bennett**: Bennett's inequality is sometimes tighter for very small probabilities. Which concentration inequality gives the best constant for our regime ($M \geq 10$, $\Delta_s \in [0.05, 0.5]$)?

2. **Empirical process uniform bound**: Should we use Talagrand's inequality (requires bounded function class) or a simpler union bound (looser but straightforward)? The answer depends on whether we need uniform convergence over thresholds $\theta$ as well as states $s$.

3. **Le Cam constants**: The exact constant in the Le Cam lower bound depends on the $\chi^2$ or Hellinger distance between $P_0$ and $P_1$. Computing this distance for the consistency score distribution requires careful calculation.

4. **Dependent expert covariance structure**: Is bounded correlation sufficient, or do we need specific correlation assumptions? We should derive the bound under general positive correlation and note that negative correlation would actually help.

5. **PAC-Bayes prior**: What is the natural prior over thresholds? A Beta prior with parameters that encode the mean separation condition seems appropriate but needs justification.

---

*End of framework document. All sections identified, existing material inventoried, new proofs specified, and drafting timeline established.*
