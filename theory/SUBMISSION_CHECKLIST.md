# SCX Theory: Submission-Ready Checklist for arXiv

> **Date**: 2026-06-28 | **Status**: Final pre-submission audit
> **Purpose**: Complete inventory of theorems, assumptions, notation, and author notes for arXiv submission.

---

## 1. Complete Theorem Inventory

### 1.1 Core Theorems (Proven)

| # | Name | Status | Key Equation | Page Estimate |
|---|------|--------|-------------|---------------|
| **Thm 1** | Multi-Expert Consistency Guarantee for Label Noise Detection | **PROVEN** | $\text{F1} \geq 1 - \frac{1}{\eta}\sum_s \rho_s e^{-2M\Delta_s^2}$ | 8-10 pages |
| **Thm 2** | Weak Feature Failure Lower Bound | **PROVEN** | $F1_{\text{SCX}} \leq F1_{\text{base}} + C_F\sqrt{1-e^{-\delta}}$ | 6-8 pages |
| **Thm 3** | Noise-Difficulty Unidentifiability | **PROVEN** | $\mathcal{P}_{\text{noise}} = \mathcal{P}_{\text{hard}}$ constructively | 8-10 pages |
| **Prop 3** | State-Conditioned Expert Weighting | **PROVEN** | $\Delta R \geq \frac{1}{\alpha} I(s; w)$ | 3-4 pages |
| **Prop 4** | Compression Fidelity (SCX-Compress) | **PROVEN** | $\varepsilon(s) \leq B(1-D_{\text{eff}})(1-n_s'/N_s) + O(B\sqrt{d/n_s'})$ | 5-7 pages |
| **Thm 12.5** | Lyapunov Descent Under Reference-Set Replay | **PROVEN** | $\mathbb{E}[\Delta\Phi_t] \leq -\alpha_t\|\nabla L_0\|^2 - 2\beta_t\rho\|\Delta_t\|\|S_t-\hat{C}\| + O(\alpha_t^2 W + \beta_t^2)$ | 4-5 pages |
| **Thm 12.2** | Impossibility of Lyapunov Descent Without Replay | **PROVEN** | Requires $D_{\text{joint}}^* + 2B(1-\varepsilon) = 0$ | 2 pages |
| **Spring-1 (SE-1)** | Convergence of SCX Self-Evolution | **PROVEN** (with Thm 12.5) | $(S_t, \theta_t) \to (S^*, \theta^*)$ a.s. | 6-8 pages |
| **Spring-2 (SE-2)** | Completeness Bound (Finite-Time Termination) | **PROVEN** | $T^* \leq \Phi_0/\varepsilon_{\text{mach}}$ | 4-5 pages |

### 1.2 Supporting Results (Proven)

| # | Name | Status | Role |
|---|------|--------|------|
| Lemma 1 (Thm 1) | Mean Separation | **PROVEN** | Establishes $\mathbb{E}[C\|\text{noise}] > \mathbb{E}[C\|\text{clean}]$ |
| Lemma 2 (Thm 1) | FPR Upper Bound (Hoeffding) | **PROVEN** | $\text{FPR}_s \leq e^{-2M(\theta-\mu_s)^2}$ |
| Lemma 3 (Thm 1) | TPR Lower Bound (with A6) | **PROVEN** | $\text{TPR}_s \geq 1 - e^{-2M(1-C_{\text{bal}}\mu_s/(K-1)-\theta)^2}$ |
| Lemma 1 (Thm 2) | State Estimation Error (Fano) | **PROVEN** | $P(\hat{S} \neq S) \geq (H(S)-\delta-\log 2)/\log K_S$ |
| Lemma 2 (Thm 2) | SCX Reliability Degradation | **PROVEN** | $\mathbb{E}[|C(\hat{S})-C(S)|] \leq 2P(\hat{S}\neq S) + O(1/\sqrt{n_{\min}})$ |
| Lemma SE-1.1 | Lyapunov Non-Increase (on training distribution) | **PROVEN** | Supermartingale argument |
| Lemma SE-1.2 | Finite Memory Bank Configurations | **PROVEN** | Covering number + monotonicity |
| Lemma SE-1.3 | Vanishing Parameter Displacement | **PROVEN** | $\|\theta_{t+1}-\theta_t\| \leq \alpha_t G \to 0$ |
| Lemma SE-1.4 | Limit Points Are Fixed Points | **PROVEN** | From SE-1.1 through SE-1.3 |
| Lemma 12.1 | Domain Adaptation Bound for $D_{\text{static}}$ | **PROVEN** | Ben-David et al. (2010) framework |
| Lemma 12.2 | Alignment Bias Decomposition | **PROVEN** | Cauchy-Schwarz + Lipschitz |

### 1.3 Conjectured / Open

| # | Name | Status | Reason |
|---|------|--------|--------|
| Regime 3 | Perpetual Discovery Rate | **CONJECTURED** | Requires tail characterization of data distribution |
| Phase Diagram | Regime Boundaries | **CONJECTURED** | Phase transitions not rigorously characterized |
| Full Functional Convergence | Infinite $\mathcal{X}$ limit of SE-1.2 | **OPEN** | Requires Arzelà-Ascoli compactness; $\varepsilon$-precision version proven |
| G5 ($K>2$ Thm 3) | Construction uses "completely random experts" | **PROVEN but extreme** | $K=2$ construction is the practically relevant case |

---

## 2. Complete Assumption Inventory

### 2.1 Assumptions A1-A6 (Theorem 1)

| ID | Assumption | Formal Statement | Justification | Verifiability |
|----|-----------|-----------------|---------------|---------------|
| **A1** | Disjoint training sets | $D_m \cap D_{m'} = \varnothing$, $D_m \perp D_{m'}$ | Ensures expert errors are independent; breaks Thm 3's unidentifiability (Corollary 2) | **Testable**: verify training data provenance |
| **A2** | Clean-data conditional independence | $\{e_m(x,y)\}_m$ conditionally independent given $x$ | Follows from A1; required for Hoeffding/Chernoff concentration | **Implied by A1** |
| **A3** | Bounded loss | $\ell(\cdot,\cdot) \in [0,B]$, $B < \infty$ | Technical requirement for Hoeffding inequality | **Always satisfied** for bounded losses (0-1, truncated MSE) |
| **A4** | Uniform independent noise | Noise independent of $x$, uniform over $\mathcal{Y}\setminus\{y^*\}$ | Breaks Thm 3's unidentifiability (Corollary 3); standard label noise model | **Testable**: $\chi^2$ test for noise rate constancy across states |
| **A5** | State homogeneity | $\sup_{x\in s} \mathbb{E}[C\|\text{clean},x] \leq \mu_s$ | Breaks Thm 3's unidentifiability (Corollary 4); enables state-level analysis | **Testable**: KS test for within-state error uniformity |
| **A6** | Balanced error distribution | $\max_{c\neq y^*}\mu_c(x) \leq C_{\text{bal}} \cdot \mu_s/(K-1)$ | Breaks Thm 3's unidentifiability (Corollary 5); prevents error concentration | **Testable**: $\chi^2$ test for error class balance; $C_{\text{bal}}$ estimable |

**Recommended $C_{\text{bal}}$ defaults**: $C_{\text{bal}} = 2$ (conservative) or estimate from validation data.

### 2.2 Conditions C1-C9 (Self-Evolution, Spring-1)

| ID | Condition | Formal Statement | Justification | Dependencies |
|----|-----------|-----------------|---------------|-------------|
| **C1'** | Finite covering dimension | $\dim(\Phi) = d_\phi < \infty$ | Replaces unrealistic "finite $\mathcal{X}$"; enables covering-number argument for memory bank stabilization | Always true for $\mathbb{R}^{d_\phi}$ features |
| **C2** | Lipschitz student | $\|f_{\theta_1}(x) - f_{\theta_2}(x)\| \leq L_f\|\theta_1-\theta_2\|$ | Required for gradient control in SGD analysis | Standard for neural networks with Lipschitz activations |
| **C3** | Lipschitz gatekeeper | $\|\text{SCXUpdate}(S_1) - \text{SCXUpdate}(S_2)\|_\infty \leq L_S\|S_1-S_2\|_\infty$ | Required for gatekeeper update control | Holds for averaging-based SCX updates |
| **C4** | Robbins-Monro rates (student) | $\sum\alpha_t = \infty$, $\sum\alpha_t^2 < \infty$ | Standard SGD convergence condition | Canonical: $\alpha_t = t^{-a}$, $a \in (1/2, 1]$ |
| **C5** | Conditional i.i.d. sampling | $(x_t,y_t) \| S_t \sim P_{S_t}$ | Models acceptance-biased data generation | Follows from gatekeeper definition |
| **C6'** | Two-timescale separation | $\beta_t = o(\alpha_t)$ | Student converges between gatekeeper updates; controls distribution shift | Joint scheduling: $\alpha_t = t^{-0.6}$, $\beta_t = t^{-0.8}$ |
| **C7** | Bounded gatekeeper update | $\|\text{SCXUpdate} - S\|_\infty \leq B_S$ | Controls per-step gatekeeper change | Enforced by projection $\Pi_{[0,1]}$ |
| **C8** | Annealing threshold | $\gamma_t \to 0.5$ | Prevents gatekeeper overconfidence early in training | Practical: $\gamma_t = \gamma_0 + (0.5-\gamma_0)(1-e^{-t/\tau})$ |
| **C9** | Random exploration | $\varepsilon$-fraction random acceptance | Ensures all regions remain represented; bounds TV$(P_{S_t}, P_0) \leq 1-\varepsilon$ | Implementable as $\varepsilon$-greedy gatekeeper |

### 2.3 Additional Assumptions (Theorem 12.5 — Reference-Set Replay)

| ID | Assumption | Formal Statement | Justification |
|----|-----------|-----------------|---------------|
| **R1** | Bounded importance weights | $\|w_t\|_\infty \leq W < \infty$ for $w_t(x) = P_0(x)/P_{S_t}(x)$ | Required for finite variance of importance-weighted gradients; implied by C9 ($W \leq 1/\varepsilon$) |
| **R2** | Reference set availability | Fixed $M_0$ available for SCXUpdate computation | Practical: small holdout set curated before self-evolution |

### 2.4 Physical Constraints (Spring-2)

| ID | Constraint | Bound | Justification |
|----|-----------|-------|---------------|
| **P1** | Finite data | $|\mathcal{D}_{\text{total}}| \leq N_{\max} < \infty$ | Physical storage limit; always true in practice |
| **P2** | Finite precision | $\varepsilon_{\text{mach}} > 0$ (typically $10^{-16}$ for float64) | Hardware constraint |
| **P3** | Finite parameterization | Gatekeeper and student parameterized by $\leq d$ parameters | Always true for implemented systems |

---

## 3. Notation Conflicts

### 3.1 Critical Conflicts (Proof-Affecting)

**None found.** All conflicts are presentational, not logical.

### 3.2 Moderate Conflicts (Reader-Confusing)

| Symbol | Meaning in Context A | Meaning in Context B | Documents Affected | Recommended Fix |
|--------|---------------------|---------------------|--------------------|----------------|
| $\mathcal{S}$ | State space (Thm 1-3) | Scored by $S_t$ gatekeeper (Spring-1/2) | All | Spring docs: add footnote on first use |
| $\delta$ | Confidence parameter $1-\delta$ (Thm 1) | Mutual information bound $I(\phi;S) \leq \delta$ (Thm 2) | Thm 1, Thm 2 | Rename Thm 2: $\delta \to \delta_{\phi}$ or $\iota$ |
| $\Phi$ | Feature space $\Phi \subseteq \mathbb{R}^{d_\phi}$ (Thm 2) | Lyapunov function $\Phi(S_t, \theta_t)$ (Spring-1/2) | Thm 2, Spring-1/2 | Spring: rename to $\Psi$ or $\mathcal{V}$ |

### 3.3 Minor Conflicts (Stylistic)

| Issue | Details | Recommendation |
|-------|---------|----------------|
| $K$ vs $K_S$ | Original theorems use $K = |\mathcal{Y}|; polished versions use $K_S = |\mathcal{S}| | Standardize in arXiv: $K$ for classes, $K_S$ for states |
| $\Delta_s$ (Thm 1) vs $\Delta_\phi$ (Thm 2) | Both are "gaps" but measure different things | Acceptable; context disambiguates |
| $M$ (experts) vs $M_t$ (memory bank) | Different objects, different subscripts | Acceptable; context disambiguates |
| $\rho_s$ (state probability, Thm 1) vs $\rho$ (state probability, Thm 3) vs $\rho(\delta)$ (TV bound, Thm 2) | Three uses of $\rho$ | Thm 2 should use $\tau(\delta)$ or keep $\rho(\delta)$ with explicit definition |

---

## 4. Proof Completeness Assessment

### 4.1 Per-Theorem Completeness

| Theorem | Proof Status | Missing Steps | Can Be Fixed? |
|---------|-------------|---------------|---------------|
| Thm 1 | **Complete** | — | — |
| Thm 2 | **Complete** | — | — |
| Thm 3 | **Complete** | — | — |
| Prop 3 | **Complete** | — | — |
| Prop 4 | **Complete** | — | — |
| Thm 12.2 | **Complete** | — | — |
| Thm 12.5 | **Complete** | — | — |
| SE-1 | **Complete** (with Thm 12.5) | Lyapunov descent now proven via Thm 12.5 | N/A |
| SE-2 | **Complete** | — | — |

### 4.2 Known Defects Fixed (Post-Verification Report)

| Defect ID | Description | Severity | Fixed? | Date |
|-----------|-------------|----------|--------|------|
| DEFECT-01/02 | False $F1_{\text{global}} = \sum_s \rho_s \cdot F1_s$ | **FATAL** | ✅ Fixed | 2026-06-28 |
| DEFECT-03/04 | Implicit (undefined) Lyapunov function | **FATAL** | ✅ Fixed (explicit reference-set $\Phi$) | 2026-06-28 |
| DEFECT-05 | False $1/\sqrt{N_t}$ unidentifiability resolution rate | **FATAL** | ✅ Retracted & corrected | 2026-06-28 |
| DEFECT-06 | Missing Bahadur-Rao lattice correction | **MAJOR** | ✅ Added | 2026-06-28 |
| DEFECT-10 | Fano inequality units (nats vs bits) | **MODERATE** | ✅ Fixed | 2026-06-28 |
| DEFECT-11 | Single-sample Fano (conservative for clustering) | **MODERATE** | ✅ Documented | 2026-06-28 |
| DEFECT-12 | $K>2$ Thm 3 construction | **MAJOR** | ✅ Fixed (random experts) | 2026-06-28 |
| DEFECT-13 | Selection bias cycle not analyzed | **MAJOR** | ✅ Added (Section 5.1) | 2026-06-28 |
| DEFECT-14 | Exploration-stabilization tension in C4/C6 | **MAJOR** | ✅ Fixed (two-timescale) | 2026-06-28 |
| DEFECT-15 | Unrealistic "finite $\mathcal{X}$" in C1 | **MAJOR** | ✅ Fixed (covering number) | 2026-06-28 |

**All FATAL and MAJOR defects resolved.**

---

## 5. Recommended Author Notes for arXiv Submission

### 5.1 Limitations to Acknowledge (Required)

1. **Reference-set replay requirement (Theorem 12.5).** The Lyapunov descent proof requires either importance sampling (for the student) or reference-set-based SCXUpdate computation (for the gatekeeper). Without these, Lyapunov descent is **provably impossible** in the asymptotic regime (Theorem 12.2). This should be stated clearly in the abstract and introduction.

2. **Finite covering dimension vs. finite $\mathcal{X}$.** The memory bank stabilization proof (Lemma SE-1.2) uses a covering-number argument that guarantees $\varepsilon$-precision convergence. Full functional convergence (in $\ell^\infty$ norm) for infinite $\mathcal{X}$ remains an open problem requiring additional compactness conditions.

3. **$K>2$ construction in Theorem 3.** The $K$-class generalization of Theorem 3 uses "completely random experts" — an extreme form of difficulty. The practically relevant construction is the $K=2$ case. The $K>2$ case is included for mathematical completeness as an existence proof.

4. **Regime 3 (Perpetual Discovery) and Phase Diagram.** These are explicitly marked as **conjectured**. They are not needed for the main convergence and completeness theorems but are included to characterize the full behavioral landscape of the self-evolution system.

5. **Importance weight variance.** Theorem 12.5's importance sampling mechanism inflates gradient variance by factor $W \leq 1/\varepsilon$. For small exploration fractions $\varepsilon$, this may cause slow convergence in practice. The theoretical guarantee (descent in expectation) holds, but finite-sample convergence rates may be degraded.

6. **Cold-start requirement.** Theorem 3 proves that initial human review (anchor points) is a **theoretical necessity**, not an engineering compromise. Any method claiming to identify label noise without any ground-truth labels is implicitly assuming at least as much structure as A1-A6.

### 5.2 Strengths to Emphasize

1. **Closed theoretical loop.** Theorems 1-3 form a complete necessity-sufficiency-boundary triad:
   - Thm 3: Without A1-A6, noise detection is ill-posed
   - Thm 1: With A1-A6, noise detection succeeds exponentially
   - Thm 2: Even with A1-A6, weak features bound SCX's advantage

2. **Provable self-evolution convergence.** Spring-1 and Spring-2 provide the first (to our knowledge) formal convergence guarantees for a self-improving ML system with a learned data filter, including a finite-time termination bound.

3. **All assumptions are testable.** Every assumption (A1-A6, C1-C9) has an associated statistical diagnostic test with explicit thresholds (see Thm 3 Section 6.3, Thm 2 Section 7).

4. **Bretagnolle-Huber tightens Pinsker.** Theorem 2 uses the BH inequality to sharpen the standard Pinsker bound, providing tighter constants by factor $\sim 1.4\times$ in the practically relevant $\delta$ regime.

5. **Reference-set replay mechanism.** The mechanism that closes the Lyapunov gap (Theorem 12.5) is both theoretically sound and practically implementable — it requires only a small holdout set and standard importance sampling techniques.

### 5.3 Suggested Abstract Structure

```
1. Problem: Label noise detection without ground truth
2. Hardness: Theorem 3 — noise and difficulty are unidentifiable without assumptions
3. Assumptions: A1-A6 as minimal sufficient conditions (justified by Theorem 3)
4. Positive result: Theorem 1 — exponential F1 guarantee under A1-A6
5. Boundary: Theorem 2 — weak features limit SCX to baseline + O(√δ)
6. Dynamics: Spring-1 — self-evolution converges to fixed point (Theorem 12.5)
7. Termination: Spring-2 — finite-time convergence under physical constraints
8. Practical implications: Diagnostic tests, recommended parameters, limitations
```

### 5.4 Recommended Paper Title

Option A: *"State-Conditioned Expertise: A Theory of Multi-Expert Label Noise Detection with Self-Evolution Guarantees"*

Option B: *"When Can We Trust the Crowd? Identifiability, Detection, and Convergence in Multi-Expert Label Noise Filtering"*

### 5.5 Recommended Page Allocation

| Section | Pages | Content |
|---------|-------|---------|
| Introduction & Related Work | 3-4 | Problem motivation, Dawid-Skene connection, measurement error literature |
| Theorem 3 (Unidentifiability) | 5-7 | Main result, constructive proof, assumption-identity mapping |
| Theorem 1 (Noise Detection) | 6-8 | Main result, Hoeffding/Chernoff proofs, corollaries, practitioner's table |
| Theorem 2 (Weak Feature) | 4-6 | Main result, Fano + Pinsker/BH proof, diagnostics |
| Self-Evolution Dynamics | 6-8 | Spring-1 convergence, Lyapunov descent (Thm 12.5), impossibility (Thm 12.2) |
| Completeness & Termination | 3-4 | Spring-2 finite-time bound, physical constraints |
| Discussion & Limitations | 2-3 | Practical guidelines, open problems, assumption testability |
| Appendices | 5-8 | Sanov derivation, $K$-class generalization, Bahadur-Rao correction, proofs of lemmas |
| **Total** | **34-48** | Suitable for JMLR or similar journal; shorten to 12-15 for conference |

---

## 6. Pre-Submission Action Items

### 6.1 Must-Do (Blocking)

- [ ] Resolve notation conflicts (Section 3.2): $\delta$, $\Phi$, $\mathcal{S}/S_t$
- [ ] Add "Notation" section to main paper body (cross-reference 00_notation_and_dependencies.md)
- [ ] Verify all theorem references are to the **polished** versions (theorems/polished/)
- [ ] Add Theorem 12.5 (reference-set replay) to main paper
- [ ] Ensure DEFECT fixes are reflected in the polished versions (all FATAL/MAJOR defects are already fixed; verify)
- [ ] Check all citations are complete (author, year, venue)

### 6.2 Should-Do (Important)

- [ ] Add practitioner's guide appendix (Thm 1 Corollary 3 table + Thm 2 diagnostics)
- [ ] Include numerical verification of Bretagnolle-Huber vs Pinsker (Thm 2 Section 5.2 table)
- [ ] Add diagram of theorem dependency graph (from PROOF_CHAIN_AUDIT.md Section 1)
- [ ] Add assumption testability table (from Thm 3 Section 6.3)
- [ ] Harmonize $K$ vs $K_S$ notation across all documents

### 6.3 Nice-to-Have (Polish)

- [ ] Add synthetic experiments validating Theorem 1's F1 bound
- [ ] Include empirical $\delta$ estimates for real datasets (DermaMNIST, AlN)
- [ ] Add phase diagram visualization (conjectured)
- [ ] Cross-reference all internal documents with consistent paths

---

## 7. Quick-Reference: Theorem Dependency Matrix

```
              Depends On →
    ┌─────────────────────────────────────────────────┐
    │          A1-A6  C1-C9  Thm1  Thm2  Thm3  SE-1  │
    ├─────────────────────────────────────────────────┤
    │ Thm 1     ●                                      │
    │ Thm 2     ○                                      │
    │ Thm 3                                            │
    │ Prop 3    ○                                      │
    │ Prop 4    ●                                      │
    │ Thm 12.2        ●                                │
    │ Thm 12.5        ●                                │
    │ SE-1      ○     ●     ●     ○           ●       │
    │ SE-2                  ○     ○           ●       │
    └─────────────────────────────────────────────────┘

    ● = strong (proof) dependency
    ○ = weak (conceptual) dependency
```

---

*End of SUBMISSION_CHECKLIST.md*

---

## References

1. All theory files: `/theory/theorems/`, `/theory/theorems/polished/`, `/theory/self_evolution/`
2. Proof chain audit: `/theory/PROOF_CHAIN_AUDIT.md`
3. Notation document: `/theory/theorems/polished/00_notation_and_dependencies.md`
4. Definitions: `/theory/definitions/01_state_conditioned_risk.md`
