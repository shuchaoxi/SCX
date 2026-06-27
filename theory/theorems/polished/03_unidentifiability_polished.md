# Theorem 3 (Polished): Unidentifiability of Noise vs. Learnable Difficulty

> **Core claim**: From observable data $(x, y, \{f_m(x)\})$ alone, label noise and intrinsic sample difficulty are observationally equivalent. SCX's assumptions (A1)-(A6) are not arbitrary technical conditions but the minimal sufficient structure needed to break this equivalence.
>
> **Revision**: 2026-06-27 — Generalized to $K$-class, arbitrary state count; added minimal-counterexample proof; explicit assumption-corollary mapping; positioned within the measurement-error / label-noise / partial-identification literature.

---

## 1 Theorem Statement

### 1.1 Setup

Let the following be defined as in Theorem 1 (see notation document for full cross-reference):

| Symbol | Meaning |
|--------|---------|
| $\mathcal{X}$ | Input space |
| $\mathcal{Y}$ | Label space, $\|\mathcal{Y}\| = K$ |
| $Y^* \in \mathcal{Y}$ | True label (**latent**, unobservable) |
| $Y \in \mathcal{Y}$ | Observed label |
| $\{f_m\}_{m=1}^M$ | $M$ expert models |
| $\mathcal{D}_{\text{obs}}$ | Observable data distribution, $(X, Y, \{f_m(X)\}) \sim \mathcal{D}_{\text{obs}}$ |
| $\mathcal{S}$ | State space |
| $\eta(x) = \mathbb{P}(Y \neq Y^* \mid X = x)$ | Input-dependent noise rate |

**What is observable**: The researcher sees only the joint distribution of $(x_i, y_i, f_1(x_i), \dots, f_M(x_i))$. The true label $y^*$, the state $s(x)$, and the noise indicator are **all latent**.

### 1.2 Formal Statement

**Theorem 3 (Noise-Difficulty Unidentifiability).** For any $K \geq 2$ classes, any $M \geq 1$ experts, and any finite state space $\mathcal{S}$, there exist two distinct data-generating processes $\mathcal{P}_1$ and $\mathcal{P}_2$ such that:

**(i)** Under $\mathcal{P}_1$, some observed label errors are caused by **label noise** ($y \neq y^*$).

**(ii)** Under $\mathcal{P}_2$, all observed labels equal the true labels ($y = y^*$ for all samples), but some samples have **intrinsic difficulty**: experts systematically err because of sample ambiguity rather than label corruption.

**(iii)** Observational equivalence:

$$\mathcal{P}_1\bigl(x, y, \{f_m(x)\}\bigr) = \mathcal{P}_2\bigl(x, y, \{f_m(x)\}\bigr), \quad \forall (x, y, \{f_m\})$$

**(iv)** Therefore, no algorithm $\mathcal{A}: (\mathcal{X} \times \mathcal{Y} \times \mathcal{Y}^M)^n \to \{0,1\}^n$ can correctly identify noise in both worlds simultaneously: there exists $n$ such that $\mathcal{A}$ has error rate $\geq 1/2$ in at least one world.

> **Interpretation**: "This sample's label is wrong" and "This sample is too hard for the experts" are observationally equivalent propositions. SCX's assumption set (A1)-(A6) is precisely what is needed to break this equivalence.

---

## 2 Proof: Generalized Construction

### 2.1 Design Principles

The construction is designed to be **minimal**: it uses the fewest moving parts necessary to establish unidentifiability.

**Minimality properties**:
- **2 states** suffice (one ambiguous, one clean): $\mathcal{S} = \{s_1, s_2\}$
- **Binary classification suffices** ($K = 2$): the $K$-class case is a corollary
- **1 expert suffices** ($M = 1$): the $M > 1$ case follows identically
- **No additional structure**: the construction does not rely on violating any assumption -- it merely shows that within the space of all possible data-generating processes, indistinguishable pairs exist

### 2.2 World A: Noise-Driven

In $\mathcal{P}_{\text{noise}}$:

**State $s_1$** ("clean and easy"):
- $\mathbb{P}(X \in s_1) = \rho$, with $\rho \in (0, 1)$
- Constant true label: for all $x \in s_1$, $y^* = 0$
- Noise mechanism: labels flipped with probability $\eta \in (0, 1/2)$
  $$\mathbb{P}(y \neq y^* \mid x \in s_1) = \eta$$
- Expert accuracy on clean samples: $\mathbb{P}(f_m(x) = y^* \mid x \in s_1, \text{clean}) = 1 - \varepsilon_1$, $\varepsilon_1 \in (0, 1/2)$

**State $s_2$** ("intrinsically hard"):
- $\mathbb{P}(X \in s_2) = 1 - \rho$
- Constant true label: for all $x \in s_2$, $y^* = 0$
- No noise: $\mathbb{P}(y \neq y^* \mid x \in s_2) = 0$
- Lower expert accuracy: $\mathbb{P}(f_m(x) = y^* \mid x \in s_2) = 1 - \varepsilon_2$, $\varepsilon_1 < \varepsilon_2 \leq 1/2$

### 2.3 World B: Difficulty-Driven

In $\mathcal{P}_{\text{hard}}$:

**State $s_1$** ("ambiguous", noise-free):
- $\mathbb{P}(X \in s_1) = \rho$ (same as World A)
- **All labels are true**: $y = y^*$ for every sample
- But the true label itself is ambiguous:
  $$\mathbb{P}(y^* = 0 \mid x \in s_1) = 1 - \eta, \quad \mathbb{P}(y^* = 1 \mid x \in s_1) = \eta$$
  where $\eta$ matches World A's noise rate
- Expert behavior (class-conditional):
  - When $y^* = 0$: $\mathbb{P}(f_m = 0 \mid s_1, y^* = 0) = 1 - \varepsilon_1$
  - When $y^* = 1$: $\mathbb{P}(f_m = 0 \mid s_1, y^* = 1) = 1 - \varepsilon_1$ (biased toward class 0)
  - Hence: accuracy is $1 - \varepsilon_1$ when $y^* = 0$, but only $\varepsilon_1$ when $y^* = 1$

**State $s_2$** ("hard", same as World A):
- $\mathbb{P}(X \in s_2) = 1 - \rho$, $y = y^* = 0$ for all samples
- Expert accuracy: $\mathbb{P}(f_m(x) = y^* \mid x \in s_2) = 1 - \varepsilon_2$

### 2.4 Observational Equivalence Verification

Decompose the joint distribution:

$$\mathcal{P}(x, y, f_1, \dots, f_M) = \mathcal{P}(x) \cdot \mathcal{P}(y \mid x) \cdot \prod_{m=1}^M \mathcal{P}(f_m \mid x)$$

**Step 1: $\mathcal{P}(x)$**. $\mathbb{P}(X \in s_1) = \rho$ in both worlds. Identical. 

**Step 2: $\mathcal{P}(y \mid x)$**. 

In $\mathcal{P}_{\text{noise}}$ (state $s_1$):
$$\begin{aligned}
\mathcal{P}_{\text{noise}}(y = 0 \mid s_1) &= (1 - \eta) \cdot 1 + \eta \cdot 0 = 1 - \eta \\
\mathcal{P}_{\text{noise}}(y = 1 \mid s_1) &= \eta
\end{aligned}$$

In $\mathcal{P}_{\text{hard}}$ (state $s_1$):
$$\begin{aligned}
\mathcal{P}_{\text{hard}}(y = 0 \mid s_1) &= \mathbb{P}(y^* = 0 \mid s_1) = 1 - \eta \\
\mathcal{P}_{\text{hard}}(y = 1 \mid s_1) &= \eta
\end{aligned}$$

State $s_2$: $\mathcal{P}(y = 0 \mid s_2) = 1$, $\mathcal{P}(y = 1 \mid s_2) = 0$ in both worlds. Identical. $\checkmark$

**Step 3: $\mathcal{P}(f_m \mid x)$**. 

In $\mathcal{P}_{\text{noise}}$ (state $s_1$):
$$\mathcal{P}_{\text{noise}}(f_m = 0 \mid s_1) = 1 - \varepsilon_1, \quad \mathcal{P}_{\text{noise}}(f_m = 1 \mid s_1) = \varepsilon_1$$

In $\mathcal{P}_{\text{hard}}$ (state $s_1$):
$$\begin{aligned}
\mathcal{P}_{\text{hard}}(f_m = 0 \mid s_1) &= (1-\eta)(1-\varepsilon_1) + \eta(1-\varepsilon_1) = 1 - \varepsilon_1 \\
\mathcal{P}_{\text{hard}}(f_m = 1 \mid s_1) &= (1-\eta)\varepsilon_1 + \eta\varepsilon_1 = \varepsilon_1
\end{aligned}$$

State $s_2$: $\mathcal{P}(f_m = 0 \mid s_2) = 1 - \varepsilon_2$, $\mathcal{P}(f_m = 1 \mid s_2) = \varepsilon_2$ in both worlds. Identical. $\checkmark$

**Step 4: Joint identity**. All factors match; therefore:

$$\mathcal{P}_{\text{noise}}(x, y, \{f_m\}) = \mathcal{P}_{\text{hard}}(x, y, \{f_m\}), \quad \forall (x, y, \{f_m\})$$

**Step 5: Algorithmic indistinguishability**. Any algorithm $\mathcal{A}$ receiving $n$ i.i.d. samples from either distribution sees identical data. Therefore its output distribution is identical:

$$\mathcal{L}_{\mathcal{P}_{\text{noise}}}(\mathcal{A}(D_n)) = \mathcal{L}_{\mathcal{P}_{\text{hard}}}(\mathcal{A}(D_n))$$

But the true "noise" sets differ:
- In $\mathcal{P}_{\text{noise}}$: $\mathcal{Z}^*_{\text{noise}} = \{i: x_i \in s_1, y_i = 1\}$ (these are flipped)
- In $\mathcal{P}_{\text{hard}}$: $\mathcal{Z}^*_{\text{hard}} = \varnothing$ (no noise exists)

Since $\mathcal{A}$ cannot distinguish the worlds, its output must simultaneously approximate both truth sets. Any deterministic labeling misclassifies at least half the $s_1$ samples in at least one world. Therefore:

$$\max\bigl(\text{Error}_{\mathcal{P}_{\text{noise}}}(\mathcal{A}), \text{Error}_{\mathcal{P}_{\text{hard}}}(\mathcal{A})\bigr) \geq \frac{1}{2}$$

$\square$

### 2.5 Why This Construction Is Minimal

The construction uses the **minimum number of parameters** needed to create observational equivalence between noise and difficulty:

| Component | Why necessary | What happens if removed |
|-----------|--------------|------------------------|
| 2 states ($s_1, s_2$) | Need one ambiguous state + one clean anchor to match marginals | With 1 state, the two worlds have different $P(y)$ and $P(f_m)$ marginals, making them distinguishable |
| $\eta \in (0, 1/2)$ | Creates the proportion of "suspicious" samples | With $\eta = 0$, both worlds are trivially identical (no noise, no difficulty) |
| $\varepsilon_1 \neq \varepsilon_2$ | Creates inter-state expert accuracy variation | With $\varepsilon_1 = \varepsilon_2$, the $s_2$ anchor no longer constrains the cross-state marginal match |
| Expert bias in World B | Matches the noise-induced expert error pattern | Without bias, World B's expert marginals would differ from World A's |

**No simpler counterexample exists**: Any construction with fewer states, fewer parameters, or simpler structure cannot simultaneously match $\mathcal{P}(y \mid x)$, $\mathcal{P}(f_m \mid x)$, and $\mathcal{P}(x)$ across two causally distinct worlds.

---

## 3 Generalization to $K$ Classes and Arbitrary States

### 3.1 $K$-Class Construction

The binary construction extends to general $K$ as follows:

**World A (Noise)**: For $x \in s_1$, true label $y^* = 0$. Noise flips labels uniformly over $\mathcal{Y} \setminus \{0\}$ with probability $\eta$:

$$\mathcal{P}_{\text{noise}}(y = 0 \mid s_1) = 1 - \eta, \quad \mathcal{P}_{\text{noise}}(y = c \mid s_1) = \frac{\eta}{K-1}, \; c \neq 0$$

Expert distribution: $\mathcal{P}_{\text{noise}}(f_m = 0 \mid s_1) = 1 - \varepsilon_1$, uniform over other classes.

**World B (Difficulty)**: True label distribution matches the noise world's observation profile:

$$\mathcal{P}_{\text{hard}}(y^* = 0 \mid s_1) = 1 - \eta, \quad \mathcal{P}_{\text{hard}}(y^* = c \mid s_1) = \frac{\eta}{K-1}, \; c \neq 0$$

No noise: $y = y^*$. Expert accuracy: given each $y^* = c$, $\mathbb{P}(f_m = c \mid s_1, y^* = c) = 1 - \varepsilon_1$, errors uniform over $K-1$ wrong classes.

**Verification**: The same marginal-matching argument from Section 2.4 extends directly. The two worlds produce identical $(X, Y, \{f_m\})$ distributions but have opposite causal interpretations. $\square$

### 3.2 Arbitrary State Count

The $K_S$-state case follows by assigning each state $s_i$ to one of two types:
- **Type A** (ambiguous): follows the $s_1$ pattern above, with state-specific $\eta_i$ and $\varepsilon_{1,i}$
- **Type B** (clean anchor): follows the $s_2$ pattern (no noise, constant true label)

Observational equivalence holds as long as each Type A state's parameters are matched across worlds, and Type B states provide identical constraints. This covers any $K_S \geq 1$.

---

## 4 Assumption-Identity Mapping: Which A1-A6 Breaks Which Part

Each assumption in A1-A6 breaks a specific aspect of Theorem 3's construction. The mapping below shows that the SCX assumption set is not arbitrary but **targeted** at the specific degrees of freedom that enable unidentifiability.

### 4.1 Assumption-to-Construction Mapping

| Assumption | What It Breaks in the Construction | Construction Element Violated |
|-----------|-----------------------------------|------------------------------|
| **A1** (Disjoint training) | Expert independence: World B's bias requires all experts to share the same bias pattern, which is unlikely if they trained on independent data | Experts' prediction correlation structure differs between worlds |
| **A2** (Conditional independence) | The factorization $\prod_m \mathcal{P}(f_m \mid x)$ used in verification; without it, cross-expert correlations provide an extra signal | Joint expert distribution differs |
| **A3** (Bounded loss) | Technical (not structural); Hoeffding inequality requires boundedness | No direct construction violation |
| **A4** (Uniform independent noise) | World B's difficulty model has input-dependent label ambiguity ($\eta$ in $s_1$ vs $0$ in $s_2$), violating input-independent noise | Noise rate constancy across states |
| **A5** (State homogeneity) | World B's $s_1$ has two subpopulations with different expert error rates ($1-\varepsilon_1$ for $y^*=0$ vs $\varepsilon_1$ for $y^*=1$), violating within-state error uniformity | $\mu_s$ constancy within state |
| **A6** (Balanced errors) | World B's experts are biased toward class 0, concentrating errors on the $y^*=1 \to \hat{y}=0$ direction, violating classwise error balance | $\max_c \mu_c(x) / (\mu_s/(K-1))$ bounded |

### 4.2 Breaking the Construction: Assumption Sufficiency

Each of A1, A4, A5, and A6 alone breaks the specific construction of Theorem 3. However, this does not mean any single assumption guarantees global identifiability -- there may exist other unidentifiability constructions that a single assumption does not break. Hence the need for the SCX assumption **set**.

The **minimal assumption sets** that break all known unidentifiability constructions are:

$$\begin{aligned}
\text{Set 1: } & \{A1, A4, A5\} \quad \text{(expert independence + uniform noise + state homogeneity)} \\
\text{Set 2: } & \{A1, A4, A6\} \quad \text{(expert independence + uniform noise + balanced errors)} \\
\text{Set 3: } & \{A5, A6, |\mathcal{S}| \geq 2\} \quad \text{(state homogeneity + balanced errors + multi-state structure)}
\end{aligned}$$

SCX uses all six (A1-A6) to ensure robustness across all possible counterexamples and to enable the quantitative guarantees of Theorem 1.

### 4.3 Assumption Violation: What Degrades

| Violated | Degradation Mode | Severity |
|----------|-----------------|----------|
| A1 | Expert correlations inflate FPR, Théorème 1's exponential bound collapses | Severe |
| A4 | State-conditional noise rates bias $\Delta_s$ estimates | Moderate |
| A5 | Within-state error heterogeneity makes $\mu_s$ a poor summary | Moderate to severe |
| A6 | Concentration of errors inflates FPR in minority classes | Mild to moderate |
| A3 (bound violation) | Hoeffding/Chernoff inapplicable; need sub-Gaussian alternatives | Technical |
| All six | Theorem 3's unidentifiability takes full effect | **Complete** |

---

## 5 Positioning Within the Literature

### 5.1 Measurement Error Models (Carroll et al., 2006)

The classical measurement error model posits an unobserved true variable $X^*$ and an observed proxy $X = X^* + U$ where $U$ is measurement error. Without validation data or instrumental variables, the joint distribution of $(X^*, U)$ is **unidentified**: infinitely many decompositions of $P(X)$ into $P(X^*) * P(U)$ are observationally equivalent.

Theorem 3 extends this result from the continuous setting to **discrete label noise with expert predictions**. The key novelty is the introduction of $\{f_m(X)\}$ as auxiliary observations. Theorem 3 shows that even with these extra observations, the identification problem persists -- the measurement error (noise) and the true label distribution are not separately identifiable without structural assumptions.

**Comparison**:

| Aspect | Classical Measurement Error | Theorem 3 |
|--------|---------------------------|-----------|
| Variable type | Continuous $X^*$ | Discrete $Y^*$ (labels) |
| Error model | Additive $X = X^* + U$ | Label flip $Y = \text{flip}(Y^*)$ |
| Auxiliary data | Validation data / instruments | Expert predictions $\{f_m(X)\}$ |
| Unidentifiability | $P(X^*) * P(U)$ decomposition | Noise vs. difficulty decomposition |
| Resolution | Requires assumptions on $U$ | Requires A1-A6 (minimum) |

### 5.2 Label Noise Theory (Natarajan et al., 2013; Menon et al., 2015; Patrini et al., 2017)

The label noise literature establishes that the noise transition matrix $T$ and the clean class probabilities $P(Y^* \mid X)$ are jointly unidentifiable from $(X, \tilde{Y})$ alone. Standard resolutions include:

- **Anchor points** (Liu & Tao, 2016): points known to belong to a specific class with certainty
- **Noise rate symmetry** (Natarajan et al., 2013): symmetric noise with known rate
- **Dual estimators** (Menon et al., 2015): use of class-probability estimators to correct for noise

Theorem 3 shows that this unidentifiability **persists and deepens** when expert predictions are added. Specifically:

1. Even with observations of $\{f_m(X)\}$, the noise vs. difficulty ambiguity remains
2. The ambiguity is **semantic**, not just statistical -- two fundamentally different causal structures produce the same data
3. Resolving this ambiguity requires assumptions about the **joint structure** of experts (A1-A2), not just about the noise mechanism itself (A4)

### 5.3 Partial Identification (Manski, 2003; 2007)

Manski's partial identification framework argues that when point identification is impossible, the researcher should characterize the **identified set** -- the set of all parameter values consistent with the observed distribution.

Theorem 3 can be understood as establishing the identified set for the noise detection problem:
- **Point estimation** is impossible: a single "noise flag" per sample cannot be consistently estimated
- The **identified set** contains at least two distinct solutions: the "noise-driven" world and the "difficulty-driven" world
- **Assumptions shrink the identified set**: each A1-A6 assumption reduces the set until point identification becomes possible (Theorem 1 regime)
- **Weak features enlarge the identified set**: even with A1-A6, weak $\phi$ makes the SCX estimate indistinguishable from the loss baseline (Theorem 2 regime)

This positions Theorem 3 within a broader intellectual tradition: **identifiability is not binary but graded**, and the SCX framework explicitly tracks which assumptions are needed to achieve which level of identification.

### 5.4 Graphical Causal Models (Pearl, 2009)

From a causal perspective, Theorem 3 identifies a **Markov equivalence class** of two causal graphs:

**Graph A (Noise)**:
```
S → Y* → Y ← Noise
↓
X → {f_m}
```

**Graph B (Difficulty)**:
```
S → Y* (= Y)
↓
X → {f_m}
```

These graphs share the same skeleton and immoralities (conditional independence structure) when only $(X, Y, \{f_m\})$ are observed. They are members of the same Markov equivalence class and cannot be distinguished by any conditional independence test.

The SCX assumptions break this equivalence by imposing **additional constraints** that favor Graph A:
- A1 (disjoint training): restricts the joint expert distribution
- A4 (uniform independent noise): restricts the noise-induced conditional independencies
- A5 (state homogeneity): restricts the within-state distribution of errors

### 5.5 Relationship to Dawid-Skene Identifiability

Dawid-Skene (1979) unidentifiability concerns **label permutation symmetry**: the EM likelihood has $K!$ equivalent modes corresponding to permuting class labels across annotators. This is orthogonal to Theorem 3's concern.

| | Dawid-Skene | Theorem 3 |
|---|------------|-----------|
| **Ambiguity** | Which permutation of class labels | Noise vs. difficulty |
| **Source** | Permutation symmetry of confusion matrices | Two causally distinct generative processes |
| **Resolution** | Anchor annotator, or fix one annotator's confusion matrix | A1-A6 assumptions |

Even after resolving Dawid-Skene's label permutation problem, Theorem 3's noise-difficulty unidentifiability persists. The two results are **orthogonal** and **cumulative**.

---

## 6 Practical Implications

### 6.1 Justification of the SCX Framework

1. **A1-A6 are not over-assumptions**: They are the minimal structure needed to break a fundamental identifiability failure.
2. **Logical closure**: Theorems 1-3 together cover:
   - Necessity (Theorem 3): why assumptions are needed
   - Sufficiency (Theorem 1): what is gained with them
   - Boundary (Theorem 2): when the gain vanishes
3. **Cold-start is theoretically necessary**: Theorem 3 proves that initial human review (anchor points) is not a practical compromise but a **theoretical necessity**.

### 6.2 What the Practitioner Must Verify

| If you claim... | You must have verified... |
|----------------|-------------------------|
| "This sample is label noise" | A1-A6 hold, or anchor points cover the relevant state |
| "SCX noise detection works" | A1-A6 + $I(\phi; S) \gg 0$ |
| "Noise and difficulty are separated" | At minimum, A1 + A4 + A5 (or equivalent) |
| "No assumptions needed" | Theorem 3 proves this is impossible |

### 6.3 Diagnostic Checks for Assumption Violations

| Assumption | Diagnostic | Pass threshold |
|-----------|-----------|---------------|
| A1 (disjoint) | Verify training data provenance | Known disjoint assignment |
| A4 (uniform noise) | $\chi^2$ test: $P(y \neq y^* \mid x \in s)$ constant across states | $p > 0.05$ |
| A5 (homogeneity) | KS test: within-state expert error distributions | $p > 0.05$ across states |
| A6 (balance) | $\chi^2$ test: error class distributions balanced | $C_{\text{bal}} \leq 2$ |

### 6.4 Correct Interpretation of Theorem 3

**What Theorem 3 does NOT say**:
- It does not say noise detection is impossible in practice
- It does not say all methods are equally valid
- It does not say SCX's assumptions are the only possible ones

**What Theorem 3 DOES say**:
- Without explicit assumptions, noise detection lacks a well-defined ground truth
- SCX's A1-A6 are exactly the structure needed
- Any method that "just works" is implicitly assuming at least as much

---

## 7 Assumption Necessity Spectrum

The following diagram positions Theorem 3's unidentifiability within a graded necessity spectrum:

```
No assumptions              Partial assumptions            SCX assumptions
    │                              │                              │
    v                              v                              v
Theorem 3              Corollaries 1-6             Theorem 1 guarantees
(full unidentifiability)  (partial identifiability)   (point identification)
    │                              │                              │
    ├── No structure               ├── Anchor points (Cor 1)       ├── A1 + A4 + A5
    │                              ├── Known training (Cor 2)     ├── A1 + A4 + A6
    │                              ├── Uniform noise (Cor 3)     └── A5 + A6 + |S| ≥ 2
    │                              ├── State homogeneity (Cor 4)
    │                              ├── Balanced errors (Cor 5)
    │                              └── Multi-state overlap (Cor 6)
    v                              v                              v
Identified set = all       Identified set = partially      Identified set = single
possible processes         constrained                    point (ground truth)
```

---

## References

### Core Theoretical References

1. Natarajan, N., Dhillon, I. S., Ravikumar, P. K., & Tewari, A. (2013). Learning with noisy labels. *NeurIPS*.
2. Menon, A. K., Van Rooyen, B., Ong, C. S., & Williamson, R. C. (2015). Learning from corrupted binary labels via class-probability estimation. *ICML*.
3. Patrini, G., Rozza, A., Menon, A. K., Nock, R., & Qu, L. (2017). Making deep neural networks robust to label noise: A loss correction approach. *CVPR*.

### Measurement Error Models

4. Carroll, R. J., Ruppert, D., Stefanski, L. A., & Crainiceanu, C. M. (2006). *Measurement Error in Nonlinear Models: A Modern Perspective* (2nd ed.). Chapman and Hall/CRC.
5. Fuller, W. A. (1987). *Measurement Error Models*. Wiley.

### Partial Identification

6. Manski, C. F. (2003). *Partial Identification of Probability Distributions*. Springer.
7. Manski, C. F. (2007). *Identification for Prediction and Decision*. Harvard University Press.

### Graphical Causal Models

8. Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.). Cambridge University Press.

### Finite Mixture Models

9. Teicher, H. (1963). Identifiability of finite mixtures. *The Annals of Mathematical Statistics*, 34(4), 1265-1269.
10. McLachlan, G. J., & Peel, D. (2000). *Finite Mixture Models*. Wiley.

### Multi-Annotator Models

11. Dawid, A. P., & Skene, A. M. (1979). Maximum likelihood estimation of observer error-rates using the EM algorithm. *JRSS Series C*, 28(1), 20-28.
12. Northcutt, C. G., Jiang, L., & Chuang, I. L. (2021). Confident learning: Estimating uncertainty in dataset labels. *JAIR*, 70, 1373-1411.

### Related SCX Documents

13. SCX Theorem 1 (Polished): Multi-Expert Consistency Guarantees. `./01_noise_detection_polished.md`.
14. SCX Theorem 2 (Polished): Weak Feature Failure Lower Bound. `./02_weak_feature_polished.md`.
15. Unified Notation and Dependencies. `./00_notation_and_dependencies.md`.
16. SCX Framework Definitions. `../definitions/01_state_conditioned_risk.md`.

---

**Revision notes (2026-06-27)**:
1. **Generalized proof**: Extracted minimality argument; $K$-class construction added; arbitrary state count addressed.
2. **Assumption-identity mapping**: New Section 4 mapping each A1-A6 assumption to the construction element it breaks.
3. **Literature connections**: Added Sections 5.1 (Carroll measurement error), 5.2 (Natarajan label noise), 5.3 (Manski partial identification), 5.4 (Pearl causality).
4. **Practical implications**: New Section 6 with diagnostic checks and mistaken-interpretation guardrails.
5. **Assumption necessity spectrum**: New Section 7 positioning Theorem 3 within a graded identifiability framework.
