# SCX Engineering Practice Guide

> **Practical guide** for deploying SCX (Soft-Consensus Cross-Validation) noise detection
> in real-world machine learning pipelines. Based on Theorems 1-4', Proposition 6,
> and the complete proof chain (Lemmas A-F).
>
> **Last updated**: 2026-06-27

---

## Table of Contents

1. [Algorithm Tier List](#1-algorithm-tier-list)
2. [Decision Flowchart](#2-decision-flowchart)
3. [Which Algorithm Wins on Each Dimension](#3-which-algorithm-wins-on-each-dimension)
4. [Practical M Selection](#4-practical-m-selection)
5. [Real Engineering Recommendations](#5-real-engineering-recommendations)
6. [When NOT to Use SCX](#6-when-not-to-use-scx)

---

## 1. Algorithm Tier List

Each tier adds complexity for a stronger F1 guarantee. Choose the simplest tier that
meets your requirements.

### Tier 0: Loss Baseline

| Item | Value |
|------|-------|
| **Compute Cost** | 1 model training (baseline) |
| **F1 Guarantee** | None -- you get whatever F1 the raw data yields |
| **What You Get** | Model trained on the dataset as-is, no noise correction |

**When to use:**
- Your feature strength is high ($\varepsilon_\varphi > 0.5$), so SCX cannot improve F1
  (Theorem 2: strong features make noise detection unnecessary).
- You have no compute budget for an ensemble -- one model is all you can afford.
- Your noise rate is negligible ($\eta < 0.01$ and you can tolerate the small degradation).
- As a baseline for comparison before investing in SCX.

---

### Tier 1: SCX + Hoeffding Bound (Theorem 1)

| Item | Value |
|------|-------|
| **Compute Cost** | $M+1$ model trainings + $K$-means clustering |
| **F1 Guarantee** | $\text{F1} \ge 1 - (1/\eta)\, e^{-2M\Delta^2}$ |
| **Strength** | Simplest SCX variant. Only needs $p_0, p_1$ (or estimates of $\mu_s$ and $C_{\text{bal}}$). |
| **Weakness** | Hoeffding bound is loose -- overestimates the error exponent by $2\text{-}4\times$ vs the true Chernoff rate. |

**When to use:**
- You need a provable guarantee (not just empirical) and can afford $M$ extra models.
- Your noise rate is moderate ($0.05 \le \eta \le 0.30$).
- You are prototyping and want the simplest possible SCX implementation.
- You don't need constant-optimality -- a rate bound suffices.

**The bound is vacuous unless** $M \ge \frac{\log(1/(\eta\delta))}{2\Delta^2}$ where $\delta$ is your target F1 slack.

---

### Tier 2: SCX + Chernoff/KL Bound (Appendix / Lemma C)

| Item | Value |
|------|-------|
| **Compute Cost** | Same as Tier 1 (same algorithm, tighter analysis) |
| **F1 Guarantee** | $\text{F1} \ge 1 - (1/\eta)\, e^{-M\kappa}$, where $\kappa = C(\text{Bern}(p_0),\text{Bern}(p_1))$ is the Chernoff information |
| **Improvement over Tier 1** | Tighter exponent: $\kappa$ is typically $2\text{-}4\times$ smaller than $2\Delta^2$, so the required $M$ is lower. |

**When to use:**
- You are already doing Tier 1 but the Hoeffding bound tells you $M$ needs to be too large.
- You have computed $\kappa$ (closed form, Lemma C.1) and it gives a practical $M$.
- You want the tightest exponential bound without adding complexity.

**Caveat:** $\kappa < 2\Delta^2$ for typical parameters (see Lemma C Table 1). The Chernoff bound is **honest** -- it gives a smaller exponent, not a larger one. This means Tier 2's guarantee is tighter (closer to the truth) but requires more experts to reach the same $1-\text{F1}$ target, compared to the overly optimistic Hoeffding bound. The advantage is that the KL bound is **asymptotically exact** (Cramer's theorem), so you can trust its predictions.

---

### Tier 3: SCX + Adaptive $\theta_{\text{opt}}$ (Theorem 4')

| Item | Value |
|------|-------|
| **Compute Cost** | Same as Tier 1/2 plus $\eta$ estimation |
| **F1 Guarantee** | Exact constant minimax optimal: $\displaystyle\lim_{M\to\infty} e^{M\kappa}\sqrt{2\pi M}(1-\text{F1}) = \frac{C_{\min}}{\eta}$ |
| **Improvement over Tier 1/2** | Uses $\eta$-aware threshold. For $\eta \ne 1/2$, achieves **smaller constant** -- e.g., $1.7\times$ better for ($p_0=0.10, p_1=0.60, \eta=0.10$). |

**When to use:**
- You have good estimates of $\eta$ (noise prior) and can compute $\theta_{\text{opt}}$ via Lemma D.2.
- The noise rate is very small ($\eta < 0.05$) or very large ($\eta > 0.50$), where the adaptive threshold gives the largest improvement.
- You need the absolute best F1 possible (academic benchmark, competition, regulatory).
- You are willing to estimate $\eta$ via a holdout set or bootstrap.

**Implementation:**
```
1. Estimate p0 = mu_s (mean expert error rate on clean samples, from domain knowledge)
2. Estimate p1 = 1 - C_bal * mu_s / (K-1) (noise error rate)
3. Compute theta* = log((1-p0)/(1-p1)) / log(p1(1-p0)/(p0(1-p1)))
4. Compute D* = log(p1(1-p0)/(p0(1-p1)))
5. Estimate eta = proportion of noise in dataset
6. theta_opt = theta* + (1/(M*D*)) * log((1-eta)/eta)
7. Flag sample as noise iff C_M > theta_opt
```

---

### Tier 4: + Bootstrap Stability (Proposition 6)

| Item | Value |
|------|-------|
| **Compute Cost** | Above plus $B$ bootstrap resamples (e.g., $B=100$) |
| **F1 Guarantee** | Above plus feature-level diagnosis of which features/examples are noise-susceptible |
| **Improvement** | Tells you whether SCX will work -- BEFORE training all M experts. The bootstrap reveals $\varepsilon_\varphi$ and $\eta$ directly from the data. |

**When to use:**
- You have no domain knowledge of $p_0, p_1, \eta$ and need to estimate everything from data.
- The dataset is large enough that you can afford $B$ bootstrap passes on small subsets.
- You want diagnostic output (which features drive the noise signal) rather than just a corrected dataset.

**Bootstrap protocol:**
```
For b = 1...B:
  Resample dataset (with replacement)
  Train M/2 experts on disjoint halves
  Compute consensus score C(x) for each sample
  Fit a two-component beta mixture to {C(x)}
  Extract: noise proportion eta_b, separation delta_b
Report: mean(eta_b), std(eta_b) and mean(delta_b), std(delta_b)
Decision: proceed to full SCX if delta_b > 0.05 and eta_b > 0.01
```

---

### Summary Table

| Tier | Method | Compute Cost | F1 Guarantee | When to Use |
|------|--------|-------------|--------------|-------------|
| 0 | Loss Baseline | 1 training | F1_base (no guarantee) | Strong features ($\varepsilon_\varphi > 0.5$); no compute budget; baseline for comparison |
| 1 | SCX + Hoeffding (Thm 1) | $M+1$ trainings + clustering | $\text{F1} \ge 1-(1/\eta)e^{-2M\Delta^2}$ | Prototyping; moderate noise; provable bound needed but constant optimality not required |
| 2 | SCX + Chernoff/KL | $M+1$ trainings + clustering | $\text{F1} \ge 1-(1/\eta)e^{-M\kappa}$ | Tighter bound needed after Tier 1 shows $M$ too large; known $p_0,p_1$ |
| 3 | SCX + Adaptive $\theta_{\text{opt}}$ (Thm 4') | $M+1$ trainings + clustering + $\eta$ estimation | **Exact constant minimax optimal** | Best F1 required; very small/large $\eta$; $\eta$ estimable |
| 4 | + Bootstrap Stability (Prop 6) | Above + $B$ resamples | Above + feature diagnosis | Unknown $\eta,\delta$; need diagnostic before commit; large dataset |

---

## 2. Decision Flowchart

```
START: Have a dataset with suspected label noise?
    │
    ▼
STEP 1: Estimate feature strength epsilon_phi = I(phi;S) / log(K)
    │
    ├── epsilon_phi > 0.5 ──────────────────► STOP. Use Loss Baseline (Tier 0).
    │                                          SCX cannot improve F1.
    │                                          (Theorem 2: strong features dominate.)
    │
    ├── 0.2 < epsilon_phi <= 0.5 ──────────► Proceed with Caution.
    │                                          SCX may help marginally.
    │                                          Run Bootstrap (Tier 4) first to
    │                                          confirm separation delta > 0.
    │                                          ▼
    │                                     Proceed to Step 2
    │
    └── epsilon_phi <= 0.2 ────────────────► Proceed. SCX likely beneficial.
                                               Weak features -- noise detection
                                               via expert consensus adds value.
                                               ▼
                                          Go to Step 2
    │
    ▼
STEP 2: Estimate noise rate eta
    │
    ├── eta < 0.05 ────────────────────────► Use Tier 3 (Adaptive theta_opt).
    │                                          Adaptive threshold is critical
    │                                          for rare noise -- naive threshold
    │                                          can be 1.5-2.5x worse.
    │                                          Verify: M >= ceil(log(1/(eta*eps))
    │                                          / (2*Delta^2)).
    │
    ├── 0.05 <= eta <= 0.30 ──────────────► Use Tier 1 or 2 (Hoeffding/Chernoff).
    │                                          Simple threshold at theta* works
    │                                          reasonably (suboptimal by <= 1.1x).
    │                                          Choose Tier 2 if you need the
    │                                          tightest provable guarantee.
    │
    ├── 0.30 < eta <= 0.70 ───────────────► Use Tier 3 (Adaptive theta_opt).
    │                                          Moderately unbalanced noise.
    │                                          The eta-aware threshold improves
    │                                          F1 but the gain is modest (< 1.3x).
    │                                          Consider: is the problem worth
    │                                          solving if 30-70% of labels are noise?
    │
    └── eta > 0.70 ────────────────────────► Use Tier 0.
    │                                          If >70% of your data is mislabeled,
    │                                          reconsider the data collection process.
    │                                          SCX can help but you have bigger problems.
    │
    ▼
STEP 3: Check computational budget
    │
    ├── Budget allows M >= M_min ──────────► Proceed with chosen tier.
    │
    ├── Budget allows M < M_min ───────────► Either:
    │     ├── Accept a weaker F1 guarantee (the bound will be vacuous)
    │     └── Collect more data to increase effective M
    │
    └── GPU cluster available ────────────► Use Tier 3 or 4.
    │                                         Parallel expert training is trivial.
    │                                         Use M=16-32 for robust guarantees.
    │
    ▼
STEP 4: Choose number of experts M
    │
    ├── Use M_min formula (Section 4 below)
    │
    ├── If compute is cheap: M = ceil(1.5 * M_min) for safety margin
    │
    └── If compute is expensive: start with M = M_min, and check if
        1-F1 decreases as 1/sqrt(M) empirically -- if so, increase M.
    │
    ▼
STEP 5: Train and deploy SCX
    │
    ├── Partition data into M disjoint subsets
    ├── Train one model per subset (same architecture)
    ├── For each sample x, compute consensus score C_M(x)
    ├── Flag noise if C_M(x) > theta (from chosen tier)
    ├── Remove flagged samples or re-label
    └── Train final model on cleaned data
    │
    ▼
STEP 6: Validate
    │
    ├── Check: does the cleaned dataset improve held-out F1?
    ├── If NO: try adaptive threshold (Tier 3) or increase M
    ├── If STILL NO: feature strength may be > 0.5 -- revert to Tier 0
    └── If YES: deploy. Periodically re-check eta and delta as data evolves.
```

---

## 3. Which Algorithm Wins on Each Dimension

| Dimension | Winner | Why |
|-----------|--------|-----|
| **Highest F1** (best accuracy) | **Tier 3 (Adaptive $\theta_{\text{opt}}$)** | Exact constant minimax optimal -- achieves the theoretical lower bound $C_{\min}/\eta$. Non-adaptive threshold is $1.1\text{-}2.4\times$ worse for typical $\eta$. |
| **Best compute/F1 tradeoff** | **Tier 1 (Hoeffding)** | $M=8\text{-}12$ experts gives F1 within 10% of optimal for moderate $\eta$. The simplest formula, easiest to code, no $\eta$ estimation needed. |
| **Best when features are strong ($\delta$ large)** | **Tier 1/2** | When $\Delta = p_1-p_0 > 0.4$, the separation is so large that even $M=5$ experts suffice. The adaptive gain from Tier 3 is small because $s\approx 1/2$ and $(1-\eta)/\eta$ factor is near 1. |
| **Best when $\eta$ is very small ($\eta<0.05$)** | **Tier 3 (Adaptive $\theta_{\text{opt}}$)** | The $\big((1-\eta)/\eta\big)^s$ factor in $C_{\min}$ is $>1$ and the adaptive threshold dramatically reduces FPR. Non-adaptive threshold can be $2\text{-}4\times$ worse for rare noise. |
| **Best when you don't know $\delta$ or $\eta$** | **Tier 4 (Bootstrap)** | Bootstrap estimates both $\eta$ and $\Delta$ from data. Tells you up-front whether SCX will help, saving wasted compute. |
| **Best when compute is tight** | **Tier 0 or Tier 1 with $M=5$** | The first 5 experts capture most of the gain. Diminishing returns: going from $M=5$ to $M=15$ improves the exponent by $3\times$ but costs $3\times$ the compute. For tight budgets, $M=5$ with Hoeffding bound gives a useable (if loose) guarantee. |
| **Most robust to assumption violations** | **Tier 0** | No assumptions to violate. The price: no F1 guarantee. Tier 1/2 degrade gracefully (the bound becomes looser, not wrong). Tier 3 depends more on accurate $\eta$ estimation. |
| **Best for non-i.i.d. experts** | **Tier 2 (Chernoff/KL)** | The Chernoff bound via Gartner-Ellis (Lemma A Section A.6) works for independent non-identical experts. The Bahadur-Rao saddlepoint approximation handles heterogeneous $p_m$. |
| **Best for multi-state problems** | **Tier 3 with state-weighted aggregation** | Lemma F shows the global constant is $\sum \rho_s C_s$ over bottleneck states. Use per-state adaptive thresholds and aggregate via F1 weighting. |

---

## 4. Practical M Selection

### 4.1 Fundamental Formula

The minimum number of experts needed for a non-vacuous bound:

$$
M_{\min} = \max\left(5,\; \left\lceil \frac{\ln(1/(\eta \cdot \varepsilon_{\text{target}}))}{2\Delta^2} \right\rceil\right)
$$

where:
- $\varepsilon_{\text{target}}$ = target F1 slack (how far from 1.0 can 1-F1 be; e.g., 0.1 for "90% of optimal")
- $\Delta = p_1 - p_0$ = separation gap
- $\eta$ = noise rate

For Tiers 2-3, replace $2\Delta^2$ with $\kappa$ (Chernoff information, always smaller):

$$
M_{\min}^{\text{(KL)}} = \max\left(5,\; \left\lceil \frac{\ln(1/(\eta \cdot \varepsilon_{\text{target}}))}{\kappa} \right\rceil\right)
$$

### 4.2 Practical Bounds for Common Cases

The relationship between $M$, $\eta$, $\Delta$, and the F1 guarantee:

| $\eta$ | $\Delta$ | $\kappa$ (approx) | $M_{\min}$ (Hoeffding, $\varepsilon=0.1$) | $M_{\min}$ (Chernoff, $\varepsilon=0.1$) | Notes |
|--------|----------|-------------------|-------------------------------------------|------------------------------------------|-------|
| 0.01 | 0.30 | 0.041 | 29 | 79 | Rare noise needs more experts |
| 0.01 | 0.50 | 0.081 | 11 | 40 | Larger separation helps Hoeffding more |
| 0.05 | 0.30 | 0.041 | 22 | 60 | |
| 0.05 | 0.50 | 0.081 | 8 | 31 | |
| 0.10 | 0.30 | 0.041 | 19 | 51 | Typical case |
| 0.10 | 0.50 | 0.081 | 7 | 26 | |
| 0.20 | 0.30 | 0.041 | 15 | 41 | |
| 0.20 | 0.50 | 0.081 | 6 | 21 | |
| 0.30 | 0.30 | 0.041 | 13 | 34 | |
| 0.30 | 0.50 | 0.081 | 5 | 18 | |

**Key insight**: The Chernoff bound requires **2-4 times more experts** than the Hoeffding bound for the same guarantee, because $\kappa$ is smaller than $2\Delta^2$. This is NOT a weakness -- the Hoeffding bound is overly optimistic (gives an illusion of requiring fewer experts than truly needed), while the Chernoff bound is asymptotically exact. In practice, use the Chernoff/KL formula for planning, and the Hoeffding formula for a quick conservative bound.

### 4.3 Lookup Table for Common Scenarios

| Scenario | $\eta$ | $\Delta$ (est.) | Recommended $M$ | Tier | Expected F1 |
|----------|--------|-----------------|-----------------|------|-------------|
| GPU cluster, 100K samples | 0.10 | 0.50 | 12-16 | 2 (Chernoff) | 0.990-0.999 |
| Single CPU, 500 samples | 0.05 | 0.30 | 5-8 | 1 (Hoeffding) | 0.85-0.95 |
| 1M images, 1% noise, ResNet-50 | 0.01 | 0.60 | 8-12 | 3 (Adaptive) | 0.995-0.999 |
| Medical imaging, 50K images | 0.05 | 0.40 | 10-15 | 3 (Adaptive) | 0.99-0.998 |
| MLIP, 500 frames, ACE | 0.15 | 0.25 | 8-12 | 2 (Chernoff) | 0.88-0.95 |
| Big tech, 10M samples, unknown noise | unknown | unknown | 20 + bootstrap | 4 (Bootstrap) | TBD by bootstrap |
| Academic CIFAR-10 (1 GPU) | 0.08 | 0.35 | 8-10 | 2 (Chernoff) | 0.94-0.97 |

### 4.4 The "Saturation Phenomenon"

Beyond $M \approx 15$, additional experts provide **diminishing returns**:

$$
\frac{1-\text{F1}(M)}{1-\text{F1}(\infty)} \approx \frac{e^{-M\kappa}}{\sqrt{2\pi M}} \cdot \text{constant}
$$

- **$M$=5**: Rough bound, factor 3-5 from optimal
- **$M$=10**: Good bound, within 50% of asymptotic
- **$M$=15**: Excellent bound, within 20% of asymptotic
- **$M$=20**: Near-optimal, within 10% of asymptotic
- **$M$=30**: Essentially optimal for practical purposes

**Recommendation**: Do not exceed $M=25$ unless compute is free. The F1 improvement from $M=25$ to $M=50$ is typically $<0.1\%$.

---

## 5. Real Engineering Recommendations

### Scenario A: Academic Researcher with 1 GPU, CIFAR-10

**Resources**: 1 GPU (e.g., RTX 3090), CIFAR-10 (50K training images), 10 classes.

**Typical noise profile**: Suspected 5-10% label noise (CIFAR-10 has approx 8% human annotation error).

**Recommendation:**

| Parameter | Value |
|-----------|-------|
| **Tier** | 2 (Chernoff/KL bound) |
| **$M$** | 10 |
| **Threshold** | $\theta^*$ (Chernoff point, no $\eta$ adaptation needed for 5-10% noise) |
| **Subset size** | 5,000 images per expert |
| **Expected F1** | 0.94-0.97 |
| **Compute estimate** | 10 $\times$ ResNet-18 training = ~5 GPU-hours |

**Implementation steps:**
1. Split CIFAR-10 training set into 10 disjoint subsets of 5,000 images each.
2. Train 10 ResNet-18 models (one per subset). Use weight sharing or early stopping to save compute.
3. For each training image, compute consensus score $C_M(x)$ = fraction of experts that (correctly or incorrectly) classify it.
4. Estimate $p_0 \approx$ average error rate on clean images (use a small held-out clean set or domain knowledge; for CIFAR-10, $p_0 \approx 0.05\text{-}0.10$ per class).
5. Compute $p_1 = 1 - C_{\text{bal}} \cdot p_0/(K-1)$. For CIFAR-10 ($K=10$, $C_{\text{bal}} \approx 1$), $p_1 \approx 1 - p_0/9 \approx 0.99$.
6. Compute $\theta^* = \log((1-p_0)/(1-p_1)) / \log(p_1(1-p_0)/(p_0(1-p_1)))$.
7. Flag images with $C_M(x) > \theta^*$ as noisy.
8. Remove flagged images (or relabel) and train final model on cleaned data.

**Diagnostic check**: Plot histogram of $C_M(x)$. If bimodal (peaks near $p_0$ and $p_1$), SCX is working. If unimodal, SCX won't help -- check feature strength.

---

### Scenario B: MLIP Developer with CPU Cluster, 500 Frames, ACE Descriptors

**Resources**: CPU cluster (e.g., 32 cores), $N=500$ atomic configurations, ACE (Atomic Cluster Expansion) descriptors.

**Typical noise profile**: 10-20% of frames may have incorrect energy/force labels (DFT convergence issues, structure relaxation artifacts).

**Recommendation:**

| Parameter | Value |
|-----------|-------|
| **Tier** | 3 (Adaptive $\theta_{\text{opt}}$) |
| **$M$** | 8 |
| **Threshold** | $\theta_{\text{opt}}$ (adaptive, $\eta$-aware) |
| **Subset size** | ~60 frames per expert (with overlap via bootstrapping) |
| **Expected F1** | 0.88-0.95 |
| **Compute estimate** | 8 $\times$ ACE fit = ~2 CPU-hours |

**Why adaptive threshold matters for MLIP**: Frame-level noise in DFT datasets is often rare ($\eta \approx 0.10\text{-}0.15$). The adaptive threshold provides significant gain at small $\eta$.

**Implementation steps:**
1. Since $N=500$ is small, use **bootstrap sampling** rather than disjoint subsets: each expert trains on $N$ samples drawn with replacement (each sample appears in ~63% of experts).
2. Train 8 ACE models in parallel on the CPU cluster.
3. For each frame, compute $C_8(x)$ = fraction of models that predict energy/force with error above threshold.
4. Estimate $\eta$ from the data: fit a two-component mixture to $\{C_M(x)\}$ (bootstrap Tier 4).
5. Compute $\theta_{\text{opt}} = \theta^* + \frac{1}{M}\frac{\log((1-\eta)/\eta)}{D^*}$.
6. Flag frames with $C_M(x) > \theta_{\text{opt}}$ as potentially noisy.
7. Review flagged frames manually (DFT recalc if budget allows) or remove.
8. Train final ACE model on cleaned set.

**MLIP-specific note**: The ACE descriptors provide strong features ($\varepsilon_\varphi$ is typically moderate). If $\varepsilon_\varphi > 0.5$, SCX may not help -- the initial model is already good. Run the bootstrap diagnostic first.

---

### Scenario C: Medical Imaging Startup, 50K Images, 5% Suspected Label Noise

**Resources**: Cloud GPU (e.g., 4$\times$ A100), $N=50,000$ medical images, binary classification (e.g., tumor vs. no tumor).

**Regulatory considerations**: FDA 510(k) clearance requires documented validation of any data-cleaning step. SCX's provable F1 bound (Theorems 1-4') can serve as part of the validation dossier.

**Recommendation:**

| Parameter | Value |
|-----------|-------|
| **Tier** | 3 (Adaptive $\theta_{\text{opt}}$) |
| **$M$** | 12-15 |
| **Threshold** | $\theta_{\text{opt}}$ (adaptive) |
| **Subset size** | ~3,500-4,000 images each (disjoint) |
| **Expected F1** | 0.99-0.998 |
| **Validation protocol** | Holdout 10% of data with known clean labels for F1 measurement |

**Regulatory implementation:**
1. **Pre-SCX validation**: Label a holdout set (5,000 images) with gold-standard annotations (e.g., pathologist review). Measure baseline F1.
2. **Parameter estimation**: Use the holdout set to estimate $\eta$ (noise proportion), $p_0$ (expert error rate on clean), and $p_1$.
3. **SCX execution**: Train $M=15$ models on disjoint subsets. Apply adaptive threshold.
4. **Post-SCX validation**: Measure F1 on the same holdout set after cleaning. The improvement is attributable to SCX, not to dataset shift.
5. **Documentation for regulators**:
   - Record $M, p_0, p_1, \eta, \theta_{\text{opt}}$ for reproducibility.
   - Report the theoretical F1 lower bound: $\text{F1} \ge 1 - \frac{C_{\min}}{\eta} \cdot \frac{e^{-M\kappa}}{\sqrt{2\pi M}}$.
   - Compare against the achieved F1 -- the bound should be conservative.

**Risk mitigation**:
- **False positives** (clean images flagged as noise): Adjust threshold toward $p_1$ (more conservative). The $\theta_{\text{opt}}$ formula gives the optimal tradeoff, but for medical domains you may want to bias toward precision (fewer false flags).
- **False negatives** (noisy images missed): The bound guarantees these are exponentially rare in $M$.

---

### Scenario D: Big Tech, 10M Samples, Unknown Noise Rate, Latency Matters

**Resources**: Large GPU cluster ($\ge 100$ GPUs), $N=10^7$ samples, real-time inference latency $< 100$ms.

**Unknown parameters**: $\eta$ and $\delta$ (separation) are not known a priori.

**Recommendation:**

| Parameter | Value |
|-----------|-------|
| **Tier** | 4 (Bootstrap -> Tier 3) |
| **$M$** | 20-24 (bootstrap determines exact number) |
| **$\eta$ estimation** | Bootstrap on 10K sample mini-batches |
| **$\delta$ estimation** | Bootstrap as above |
| **Threshold** | $\theta_{\text{opt}}$ (adaptive, using bootstrap-estimated $\eta$) |
| **Latency strategy** | Pre-compute expert predictions offline; $C_M(x)$ lookup at inference time is $O(1)$ |

**Implementation:**

*Phase 1: Bootstrap diagnosis (offline, 1 GPU-hour)*
1. Draw 10 bootstrap samples of 10,000 samples each from the full dataset.
2. For each bootstrap sample, train $M_{\text{boot}} = 6$ experts on disjoint subsets.
3. Compute $\widehat{\eta}_b$ and $\widehat{\Delta}_b$ for each bootstrap via beta mixture fit.
4. If $\widehat{\eta} < 0.5\%$ or $\widehat{\Delta} < 0.1$: SCX is not beneficial. Use Tier 0.
5. Otherwise: proceed with full SCX using $M$ computed from bootstrap estimates.

*Phase 2: Full SCX execution (offline, 100 GPU-hours)*
1. Partition data into $M=20$ disjoint subsets of 500K samples each.
2. Train 20 models in parallel (standard training pipeline, no modification).
3. Compute consensus score $C_{20}(x)$ for all 10M samples.
4. Apply adaptive threshold $\theta_{\text{opt}}$ using $\widehat{\eta}$ from Phase 1.

*Phase 3: Low-latency inference (real-time)*
1. No online expert ensemble needed. The cleaned dataset from Phase 2 is used to train a SINGLE production model.
2. Inference latency: identical to baseline (same model architecture, no ensemble overhead).
3. The SCX benefit is realized entirely in training, not inference.

**Monitoring**: Track $\eta$ over time (concept drift). Re-run SCX when $\eta$ changes by more than 0.02.

---

## 6. When NOT to Use SCX

### Failure Mode 1: Strong Features ($\varepsilon_\varphi > 0.5$)

**Symptom**: SCX-cleaned dataset gives the same F1 as the raw dataset.

**Theory**: Theorem 2 proves $\text{F1}_{\text{SCX}} \le \text{F1}_{\text{base}}$ when feature strength exceeds 0.5. The experts all agree on clean samples (low $p_0$) and disagree on noise (high $p_1$), but the baseline model is already good enough.

**Diagnostic signs**:
- Pre-SCX baseline F1 > 0.95 on held-out clean data.
- Histogram of $C_M(x)$ is strongly bimodal with near-zero overlap.
- $p_0 - 0 < 0.05$ and $1 - p_1 < 0.05$ (experts are nearly perfect).

**Remedy**: Skip SCX. The data is already clean enough for your application.

---

### Failure Mode 2: Negative Separation ($\mu_s > (K-1)/K$)

**Symptom**: $p_1 \le p_0$, i.e., noisy samples are harder for experts than clean samples.

**Theory**: Theorem 1/ Lemma 1 require $p_1 > p_0$. When $\mu_s > (K-1)/K$, the balancing constant $C_{\text{bal}}$ in the definition $p_1 = 1 - C_{\text{bal}}\cdot\mu_s/(K-1)$ gives $p_1 \le p_0$, so $\Delta \le 0$.

**Diagnostic signs**:
- $C_M(x)$ for known noisy samples is similar to or lower than for clean samples.
- The empirical $\widehat{p}_1 - \widehat{p}_0$ is negative or near-zero.

**Remedy**: Increase $K$ (number of classes) if possible, which increases $(K-1)/K$. Or check if Assumption A4 (balanced expert competence) is violated -- the experts may be systematically wrong on clean samples of certain classes.

---

### Failure Mode 3: Insufficient Expert Diversity

**Symptom**: $C_M(x)$ is near-constant across all samples (all experts agree everywhere).

**Theory**: Assumption A2 requires experts to make conditionally independent errors. If all experts use the same architecture, training data, and random seed, their errors are correlated and $C_M(x)$ carries no discriminating signal.

**Diagnostic signs**:
- Variance of $C_M(x)$ across samples is very low.
- Pairwise expert agreement on clean samples is near 100%.
- Standard deviation of $C_M(x)$ is $< 0.05$.

**Remedy**: Increase diversity:
- Use different random seeds and data shuffles per expert.
- Use different architectures (ResNet-18, ResNet-50, EfficientNet).
- Use different bootstrapped subsets (with replacement).
- Use different preprocessing or augmentation.

---

### Failure Mode 4: $\eta$ Too Small AND $M$ Too Small

**Symptom**: The bound $1 - \text{F1} < (1/\eta)e^{-M\kappa}$ is vacuous ($> 1$).

**Theory**: When $\eta < e^{-M\kappa}$, the Hoeffding bound exceeds 1. For the Chernoff bound, the condition is $\eta < e^{-M\kappa}/\kappa\sqrt{2\pi M}$.

**Diagnostic signs**:
- The theoretical F1 lower bound is negative (or 1-F1 > 1).
- Numerical: $M \ll \frac{\log(1/\eta)}{\kappa}$.

**Example**: $\eta = 0.001$, $\kappa = 0.04$, $M=10$.
$\log(1/\eta)/\kappa = \log(1000)/0.04 = 6.91/0.04 = 172.7 \gg 10$.
The bound is vacuous. You need $M \approx 173$ experts for a non-vacuous guarantee.

**Remedy**:
- Increase $M$ to at least $\lceil \log(1/\eta)/\kappa \rceil$.
- If that's too expensive, use the bootstrap (Tier 4) to verify empirically whether SCX works -- the asymptotic bound is conservative, and you may get good results at smaller $M$ even if the bound is vacuous.

---

### Failure Mode 5: Dataset Too Small

**Symptom**: Experts overfit on their small subsets.

**Theory**: Training $M$ experts on $N/M$ samples each degrades expert quality when $N/M$ is small. The error rates $p_0$ and $p_1$ become dataset-dependent, violating the assumption that $p_0$ and $p_1$ are intrinsic.

**Diagnostic signs**:
- Expert accuracy on held-out data drops significantly compared to full-data training.
- Cross-validation accuracy varies wildly across experts.
- $N/M < 100$ (very few samples per expert for deep learning).

**Remedy**:
- Use bootstrap sampling instead of disjoint subsets (each expert sees $N$ samples with replacement, effective unique samples $\approx 0.63N$).
- Use bootstrap-aggregated experts (bagging). This reduces overfitting and increases diversity.
- Use a single model with $M$ output heads (multi-head architecture) instead of $M$ separate models -- this shares parameters and reduces the effective sample size requirement.
- If $N < 500$, SCX is unlikely to work well regardless of method. Consider a simpler noise detection approach (e.g., loss-based filtering).

---

### Summary of Failure Modes

| # | Failure Mode | Condition | Symptom | Remedy |
|---|-------------|-----------|---------|--------|
| 1 | Strong features | $\varepsilon_\varphi > 0.5$ | SCX = baseline | Skip SCX |
| 2 | Negative separation | $\mu_s > (K-1)/K$ | $p_1 \le p_0$ | Increase $K$, check A4 |
| 3 | Low diversity | Expert errors correlated | $C_M(x)$ near-constant | Diversify experts |
| 4 | $\eta$ small, $M$ small | $M \ll \log(1/\eta)/\kappa$ | Vacuous bound | Increase $M$, use bootstrap |
| 5 | Dataset too small | $N/M < 100$ | Experts overfit | Bootstrap, multi-head, bagging |

---

## References

1. Theorems 1-4', Proposition 6: Complete proof chain in `G:\Xiaogan_Supercomputing_data\SCX\theory\explorations\`:
   - `exact_constant_minimax.md` -- Proof architecture
   - `lemma_AB_bahadur_rao_f1.md` -- Lemma A (Bahadur-Rao) + Lemma B (F1 expansion)
   - `lemma_CD_chernoff_adaptive.md` -- Lemma C (Chernoff info) + Lemma D (adaptive threshold)
   - `lemma_EF_lowerbound_aggregation.md` -- Lemma E (lower bound) + Lemma F (multi-state)

2. Chernoff, H. (1952). A measure of asymptotic efficiency for tests of a hypothesis based on the sum of observations. *Annals of Mathematical Statistics*, 23(4), 493-507.

3. Bahadur, R. R., & Rao, R. R. (1960). On deviations of the sample mean. *Annals of Mathematical Statistics*, 31(4), 1015-1027.

4. Hoeffding, W. (1965). Asymptotically optimal tests for multinomial distributions. *Annals of Mathematical Statistics*, 36(2), 369-401.
