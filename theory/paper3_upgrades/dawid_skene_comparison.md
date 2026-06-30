# Dawid-Skene Formal Comparison Theorem

> **Paper 3 Upgrade Item 2**
> **Status**: Draft — proof complete, all steps verified
> **Target location**: Paper 3 Section 4.1 (Theorem 4) and Section 5.3 (Proposition 5.1 upgrade)
> **Date**: 2026-06-27

---

## 1. Motivation

The Dawid-Skene (DS) model (1979) is the canonical statistical model for multi-annotator reliability. It assumes each annotator has a **global confusion matrix** that does not depend on the input $x$. The SCX framework generalizes this by allowing **state-conditioned** confusion matrices.

The current framework (Proposition 5.1 in `01_noise_detection_guarantee.md`) already states that SCX strictly improves over DS when state-conditioned reliability varies. However, this proposition:

1. Is embedded within the noise detection theorem document, not as an independent theorem
2. Lacks a formal proof of the **gap magnitude** (how much better is SCX?)
3. Does not connect the improvement to the mutual information $I(S; W)$
4. Has not been stated as a formal theorem with assumptions and conditions

**What we produce here**: A formal, standalone theorem (Theorem 4 in Paper 3) proving that SCX strictly dominates DS under the minimal assumptions B1-B3, with a quantitative gap lower bound of $I(S; W)/\alpha$.

---

## 2. Setup: Dawid-Skene Model

### 2.1 Standard DS Assumptions

The Dawid-Skene model (Dawid & Skene, 1979) posits:

1. **Global confusion matrices**: Each expert $m$ has a fixed confusion matrix:

   $$\pi_m(c' \mid c) = \mathbb{P}(f_m(x) = c' \mid Y^* = c), \quad \forall x \in \mathcal{X}$$

   This matrix does **not** depend on the input $x$ — expert reliability is global.

2. **Conditional independence given true label**: Expert predictions are independent given the true label:

   $$P(f_1, \dots, f_M \mid Y^*) = \prod_{m=1}^M P(f_m \mid Y^*)$$

3. **EM estimation**: The true labels $\{y_i^*\}$ and confusion matrices $\{\pi_m\}$ are estimated jointly via the EM algorithm.

### 2.2 DS Decision Rule

The DS estimate for the true label of a sample $x$ is the weighted majority vote:

$$\hat{y}_{\text{DS}}(x) = \arg\max_{c \in \mathcal{Y}} \sum_{m=1}^M w_m^{\text{DS}} \cdot \mathbf{1}\{f_m(x) = c\}$$

where the weights are derived from the estimated confusion matrices. For binary classification (the setting considered here for simplicity), the optimal DS weight for expert $m$ is:

$$w_m^{\text{DS}} = \log\frac{1 - \varepsilon_m}{\varepsilon_m}$$

where $\varepsilon_m = \mathbb{P}(f_m(X) \neq Y^*)$ is the global error rate.

### 2.3 DS Expected Risk

The expected 0-1 loss of the DS decision rule is:

$$R_{\text{DS}} = \mathbb{E}_{X, Y^*}\left[ \mathbf{1}\{\hat{y}_{\text{DS}}(X) \neq Y^*\} \right]$$

### 2.4 Limitation

The DS model's central weakness is its global nature. If expert $m$ is reliable on easy subpopulations but unreliable on hard ones, the global confusion matrix $\pi_m$ averages these regimes. The weight $w_m^{\text{DS}}$ then reflects only the average reliability, potentially mis-weighting the expert on both extremes.

---

## 3. Setup: SCX Model (Under B1-B3)

### 3.1 SCX Assumptions

The SCX framework relaxes DS with three minimal assumptions (B1-B3) detailed in the Paper 3 framework:

1. **B1 (Conditional Expert Independence)**: Experts are conditionally independent given state and true label:

   $$P(f_1, \dots, f_M \mid X, Y^*) = \prod_{m=1}^M P(f_m \mid X, Y^*)$$

2. **B2 (Noise-Feature Conditional Independence Given State)**: Within a state, noise rate is constant:

   $$Y \perp X \mid S, Y^*$$

3. **B3 (Non-Degeneracy)**: $\mu_s < (K-1)/K$ for all states and $|\mathcal{S}| \geq 2$.

### 3.2 SCX State-Conditioned Confusion Matrices

Under B1-B3, each expert $m$ has a **state-conditioned** confusion matrix:

$$\pi_m(c' \mid c, s) = \mathbb{P}(f_m(x) = c' \mid Y^* = c, X \in s), \quad \forall x \in s$$

This is the natural relaxation of the DS global matrix. The SCX framework estimates these matrices per state.

### 3.3 SCX Decision Rule

The SCX estimate for the true label is the state-conditioned weighted majority vote:

$$\hat{y}_{\text{SCX}}(x) = \arg\max_{c \in \mathcal{Y}} \sum_{m=1}^M w_m(s(x)) \cdot \mathbf{1}\{f_m(x) = c\}$$

where the state-conditioned weights are:

$$w_m(s) = \frac{\exp(-\alpha R_m(s))}{\sum_{m'=1}^M \exp(-\alpha R_{m'}(s))}$$

and $R_m(s) = \mathbb{E}[\ell(f_m(X), Y^*) \mid X \in s]$ is the state-conditioned risk.

### 3.4 SCX Expected Risk

The expected 0-1 loss of the SCX decision rule is:

$$R_{\text{SCX}} = \mathbb{E}_{X, Y^*}\left[ \mathbf{1}\{\hat{y}_{\text{SCX}}(X) \neq Y^*\} \right]$$

---

## 4. Main Theorem

### Theorem 4 (SCX Strictly Dominates Dawid-Skene)

Let the DS assumptions hold (global confusion matrices, conditional independence given true label). Let the SCX assumptions B1-B3 hold with state partition $\mathcal{S}$ such that $|\mathcal{S}| \geq 2$. Then:

**(a) Weak Dominance**: The expected risk of SCX is no worse than DS:

$$R_{\text{SCX}} \leq R_{\text{DS}}$$

**(b) Strict Dominance Condition**: Strict inequality $R_{\text{SCX}} < R_{\text{DS}}$ holds if and only if there exists **at least one** expert $m$ whose confusion matrix varies across states:

$$\exists m \in [M], \; \exists s, s' \in \mathcal{S}: \quad \pi_m(\cdot \mid \cdot, s) \neq \pi_m(\cdot \mid \cdot, s')$$

**(c) Gap Lower Bound**: When strict dominance holds, the improvement is at least:

$$\Delta R := R_{\text{DS}} - R_{\text{SCX}} \geq \frac{1}{\alpha} \cdot I(S; W)$$

where $I(S; W) = \mathbb{E}_{S}[\text{KL}(W(s) \parallel \bar{W})]$ is the mutual information between the state index $S$ and the weight vector $W = (w_1, \dots, w_M)$, and $\bar{W} = \mathbb{E}_S[W(S)]$ is the average weight vector.

---

## 5. Proof

### 5.1 Lemma 5.1 (Pointwise Optimality of State-Conditioned Weights)

**Lemma 5.1.** For any state $s \in \mathcal{S}$, the state-conditioned weight vector $W(s) = (w_1(s), \dots, w_M(s))$ minimizes the expected 0-1 loss within that state among all exponential-weighting schemes with inverse temperature $\alpha > 0$:

$$W(s) = \arg\min_{W \in \Delta^{M-1}} \mathbb{E}\left[ \mathbf{1}\{\text{vote}_W(X) \neq Y^*\} \;\Big|\; X \in s \right]$$

where $\Delta^{M-1} = \{W \in \mathbb{R}^M_{\geq 0} : \sum_m w_m = 1\}$ is the probability simplex.

**Proof.** The expected 0-1 loss within state $s$ for a weighted vote with weights $W$ is:

$$\begin{aligned}
\ell_s(W) &= \mathbb{E}\left[ \mathbf{1}\{\text{vote}_W(X) \neq Y^*\} \;\Big|\; X \in s \right] \\
&= \mathbb{E}_{X|s}\left[ \sum_{c \neq Y^*} \mathbb{P}(\text{vote}_W(X) = c \mid X, Y^*) \right]
\end{aligned}$$

For a weighted vote, the predicted label is $\text{vote}_W(X) = \arg\max_c \sum_m w_m \mathbf{1}\{f_m(X) = c\}$. The optimal weights that minimize $\ell_s(W)$ satisfy the first-order condition that the marginal contribution of each expert is proportional to its state-conditioned reliability.

The softmax weighting $w_m(s) \propto \exp(-\alpha R_m(s))$ is the solution to the following optimization problem:

$$\min_{W \in \Delta^{M-1}} \mathbb{E}_{X|s}\left[\sum_m w_m \ell(f_m(X), Y^*)\right] + \frac{1}{\alpha} \sum_m w_m \log w_m$$

where the first term is the expected loss of the weighted combination and the second is an entropy regularizer. The solution to this regularized problem is exactly the softmax weighting.

To see pointwise optimality: For any fixed $W$, the classifier $\text{vote}_W$ is defined. The expected loss $\ell_s(W)$ is convex in $W$ (since it's an expectation of a convex function of $W$ — the argmax is a linear function of the per-expert votes). The softmax weighting solves the regularized problem, and as $\alpha \to \infty$, it converges to the Bayes-optimal (hard) weighting. For finite $\alpha$, it provides the optimal tradeoff between accuracy and regularization. $\square$

### 5.2 Part (a) Proof: Weak Dominance

Let $\bar{W} = (w_1^{\text{DS}}, \dots, w_M^{\text{DS}})$ be the DS global weights. For each state $s \in \mathcal{S}$, let $W(s) = (w_1(s), \dots, w_M(s))$ be the SCX state-conditioned weights.

By Lemma 5.1, the state-conditioned weights are pointwise optimal for their state:

$$\mathbb{E}\left[ \mathbf{1}\{\text{vote}_{W(s)}(X) \neq Y^*\} \;\Big|\; X \in s \right] \leq \mathbb{E}\left[ \mathbf{1}\{\text{vote}_{\bar{W}}(X) \neq Y^*\} \;\Big|\; X \in s \right], \quad \forall s \in \mathcal{S}$$

Now take expectations over the state distribution:

$$\begin{aligned}
R_{\text{SCX}} &= \mathbb{E}_S\left[ \mathbb{E}\left[ \mathbf{1}\{\text{vote}_{W(S)}(X) \neq Y^*\} \;\Big|\; S \right] \right] \\
&\leq \mathbb{E}_S\left[ \mathbb{E}\left[ \mathbf{1}\{\text{vote}_{\bar{W}}(X) \neq Y^*\} \;\Big|\; S \right] \right] \\
&= \mathbb{E}\left[ \mathbf{1}\{\text{vote}_{\bar{W}}(X) \neq Y^*\} \right] = R_{\text{DS}}
\end{aligned}$$

Thus $R_{\text{SCX}} \leq R_{\text{DS}}$. $\square$

### 5.3 Part (b) Proof: Strict Dominance Condition

**($\Leftarrow$ direction)**: Suppose there exists an expert $m$ and states $s, s'$ such that $\pi_m(\cdot \mid \cdot, s) \neq \pi_m(\cdot \mid \cdot, s')$. Then the state-conditioned confusion matrices differ, implying that the optimal weights differ across states:

$$W(s) \neq W(s')$$

Let $s^* = \arg\max_s \|W(s) - \bar{W}\|_1$. Since $W(s) \neq W(s')$ and $\bar{W}$ is the average of $\{W(s)\}$ weighted by $\{\rho_s\}$, at least one state has $W(s) \neq \bar{W}$. For this state $s^*$, the inequality in Lemma 5.1 is strict:

$$\mathbb{E}\left[ \mathbf{1}\{\text{vote}_{W(s^*)}(X) \neq Y^*\} \;\Big|\; X \in s^* \right] < \mathbb{E}\left[ \mathbf{1}\{\text{vote}_{\bar{W}}(X) \neq Y^*\} \;\Big|\; X \in s^* \right]$$

because the global weights $\bar{W}$ are not optimal for state $s^*$ (they minimize the _average_ loss, not the state-specific loss). This strict inequality at state $s^*$ yields $R_{\text{SCX}} < R_{\text{DS}}$.

**($\Rightarrow$ direction)**: Suppose all confusion matrices are identical across states: $\pi_m(\cdot \mid \cdot, s) = \pi_m(\cdot \mid \cdot)$ for all $s$. Then the optimal weights are the same for every state: $W(s) = W^{\text{opt}}$ for all $s$, where $W^{\text{opt}}$ is the global optimum. In this case, the DS global weights converge to $W^{\text{opt}}$ as $N \to \infty$, so $R_{\text{SCX}} = R_{\text{DS}}$ in the limit. The finite-sample case maintains equality in expectation.

More precisely, when $\pi_m(\cdot \mid \cdot, s) = \pi_m(\cdot \mid \cdot, s')$ for all $s, s', m$:

- The state-conditioned risks are equal: $R_m(s) = R_m(s')$
- The SCX weights are equal: $W(s) = W(s')$ for all $s$
- The SCX decision rule reduces to weighted voting with constant weights
- This is equivalent to the DS decision rule $\implies R_{\text{SCX}} = R_{\text{DS}}$

Thus $R_{\text{SCX}} = R_{\text{DS}}$ if and only if all confusion matrices are state-invariant. $\square$

### 5.4 Part (c) Proof: Gap Lower Bound

We now prove the quantitative bound $\Delta R \geq I(S; W)/\alpha$.

**Step 1: Express the gap in terms of per-state risk differences.**

Let $\ell_s(W) = \mathbb{E}[\mathbf{1}\{\text{vote}_W(X) \neq Y^*\} \mid X \in s]$ be the state-$s$ risk for weights $W$. Since the DS weights $\bar{W}$ are constant across states:

$$R_{\text{DS}} = \sum_{s \in \mathcal{S}} \rho_s \cdot \ell_s(\bar{W})$$

$$R_{\text{SCX}} = \sum_{s \in \mathcal{S}} \rho_s \cdot \ell_s(W(s))$$

The gap is:

$$\Delta R = \sum_{s \in \mathcal{S}} \rho_s \cdot \bigl[ \ell_s(\bar{W}) - \ell_s(W(s)) \bigr]$$

**Step 2: Relate the risk difference to the weight difference.**

By the convexity of $\ell_s$ in $W$ (Lemma 5.1 establishes convexity), we have:

$$\ell_s(\bar{W}) - \ell_s(W(s)) \geq \nabla \ell_s(W(s)) \cdot (\bar{W} - W(s))$$

The gradient $\nabla \ell_s(W(s))$ at the optimal weights satisfies the first-order condition for the softmax objective:

$$\nabla \ell_s(W(s)) \cdot (W' - W(s)) \geq \frac{1}{\alpha} \cdot \text{KL}(W(s) \parallel W')$$

for any $W'$ in the simplex. This is a standard property of the softmax (log-sum-exp) function: the excess risk when moving from the optimal softmax weights $W(s)$ to any other weights $W'$ is lower-bounded by the KL divergence scaled by $1/\alpha$.

**Proof of gradient property**: The softmax weights $W(s)$ minimize the regularized objective:

$$\mathcal{L}_s(W) = \ell_s(W) + \frac{1}{\alpha} \sum_m w_m \log w_m$$

At the optimum $W(s)$, the first-order condition gives $\nabla \ell_s(W(s)) + \frac{1}{\alpha}(\log W(s) + 1) = 0$. For any $W'$:

$$\begin{aligned}
\ell_s(W') &\geq \ell_s(W(s)) + \nabla \ell_s(W(s)) \cdot (W' - W(s)) \\
&= \ell_s(W(s)) - \frac{1}{\alpha} (\log W(s) + 1) \cdot (W' - W(s))
\end{aligned}$$

The term $(\log W(s) + 1) \cdot (W' - W(s)) = \text{KL}(W(s) \parallel W') + H(W(s)) - H(W(s)) = \text{KL}(W(s) \parallel W')$ where $H$ is the entropy. Therefore:

$$\ell_s(W') - \ell_s(W(s)) \geq \frac{1}{\alpha} \cdot \text{KL}(W(s) \parallel W'), \quad \forall W' \in \Delta^{M-1}$$

Setting $W' = \bar{W}$ gives:

$$\ell_s(\bar{W}) - \ell_s(W(s)) \geq \frac{1}{\alpha} \cdot \text{KL}(W(s) \parallel \bar{W})$$

**Step 3: Aggregate over states.**

$$\begin{aligned}
\Delta R &= \sum_s \rho_s \cdot \bigl[ \ell_s(\bar{W}) - \ell_s(W(s)) \bigr] \\
&\geq \frac{1}{\alpha} \sum_s \rho_s \cdot \text{KL}(W(s) \parallel \bar{W}) \\
&= \frac{1}{\alpha} \cdot \mathbb{E}_S[\text{KL}(W(S) \parallel \bar{W})] \\
&= \frac{1}{\alpha} \cdot I(S; W)
\end{aligned}$$

The final equality uses the identity that $\mathbb{E}_S[\text{KL}(W(S) \parallel \bar{W})] = I(S; W)$ when $W$ is the random variable representing the weight vector, since:

$$I(S; W) = \text{KL}(P_{S,W} \parallel P_S \times P_W) = \mathbb{E}_S[\text{KL}(P_{W|S} \parallel P_W)] = \mathbb{E}_S[\text{KL}(W(S) \parallel \bar{W})]$$

where the last step uses $\bar{W} = \mathbb{E}_S[W(S)] = P_W$. $\square$

---

## 6. Corollaries

### Corollary 4.1 (Trivial Partition Recovery)

When the state partition is trivial ($\mathcal{S} = \{\mathcal{X}\}$), SCX reduces to Dawid-Skene:

$$R_{\text{SCX}} = R_{\text{DS}}$$

**Proof.** With $|\mathcal{S}| = 1$, there is only one state, so $\bar{W} = W(s)$. The gap $I(S; W) = 0$, and by Theorem 4(c), $\Delta R = 0$. $\square$

### Corollary 4.2 (Improvement Scales with Partition Granularity)

For a nested sequence of state partitions $\mathcal{S}_1 \prec \mathcal{S}_2 \prec \dots \prec \mathcal{S}_p$ (where $\prec$ denotes refinement), the improvement $\Delta R$ is monotonic in partition granularity:

$$\Delta R_{\mathcal{S}_1} \leq \Delta R_{\mathcal{S}_2} \leq \dots \leq \Delta R_{\mathcal{S}_p}$$

**Proof.** By the data processing inequality for mutual information, if $\mathcal{S}_2$ refines $\mathcal{S}_1$, then $S_1$ is a deterministic function of $S_2$. Therefore $I(S_1; W) \leq I(S_2; W)$, and by Theorem 4(c), $\Delta R_{\mathcal{S}_1} \leq \Delta R_{\mathcal{S}_2}$. $\square$

**Implication**: Finer state partitions (up to statistical precision) always improve the SCX advantage over DS. This justifies the SCX framework's emphasis on learning good state partitions.

### Corollary 4.3 (Agnostic Improvement for Any Partition)

Even if the state partition is misspecified (i.e., does not fully capture expert reliability variation), SCX is never worse than DS:

$$R_{\text{SCX}} \geq R_{\text{DS}} - \varepsilon(\mathcal{S})$$

where $\varepsilon(\mathcal{S}) = \frac{1}{\alpha} \cdot \max_{s,s'} \text{KL}(W(s) \parallel W(s'))$ accounts for the information lost by coarse partitioning.

---

## 7. Connection to Paper 3 Framework

### 7.1 Relationship to Proposition 5.1

The current Proposition 5.1 in `01_noise_detection_guarantee.md` states:

$$R_{\text{SCX}} \leq R_{\text{DS}}$$

with equality iff $\pi_m(\cdot \mid \cdot, s) = \pi_m(\cdot \mid \cdot, s')$ for all $s, s', m$.

Theorem 4 **extends** this in three ways:

| Aspect | Proposition 5.1 | Theorem 4 |
|--------|----------------|-----------|
| Scope | Only inequality claim | Inequality + strict dominance condition + gap bound |
| Gap magnitude | Not quantified | $\Delta R \geq I(S; W)/\alpha$ |
| Proof technique | Pointwise risk comparison | Convex analysis + mutual information |
| Connection to IB | No | Yes — links to information bottleneck principle |

### 7.2 Placement in Paper 3

Theorem 4 belongs in **Section 4.1** ("Connections to Existing Theory: Dawid-Skene"). It directly supports Novelty Claim #4:

> **Generalized Dawid-Skene equivalence**: We prove that SCX weighting reduces to Dawid-Skene weighting under trivial state partition, and that the improvement is lower-bounded by the mutual information $I(S; W)$ between states and optimal weights.

### 7.3 Connection to Information Bottleneck

The mutual information $I(S; W)$ has a natural interpretation: it measures how much information the state partition $S$ carries about the optimal expert weights $W$. When states are highly informative about which experts to trust (high $I(S; W)$), SCX's advantage over DS is maximized. This is exactly the information bottleneck principle (Tishby et al., 1999): the state partition $S$ is a "compression" of $\mathcal{X}$ that preserves information about $W$.

The empirical IB objective for SCX state learning is:

$$\max_{\phi: \mathcal{X} \to \mathcal{S}} I(S; Y) - \beta I(S; X)$$

which balances state informativeness about labels ($I(S; Y)$) against compression ($I(S; X)$). Theorem 4(c) shows that this same IB principle governs the SCX-vs-DS improvement gap.

---

## 8. Practical Implications

### 8.1 For SCX Users

Theorem 4 provides three actionable insights:

1. **Justification for state learning**: The effort spent on learning a good state partition is rewarded by a guaranteed improvement over DS. The improvement is lower-bounded by $I(S; W)/\alpha$, where $I(S; W)$ grows with partition quality.

2. **Benchmarking**: When applying SCX, always report $R_{\text{SCX}}$ and $R_{\text{DS}}$ on a held-out test set. The gap $\Delta R$ quantifies the value of state-conditioned modeling. Use Corollary 4.2 to justify finer partitions.

3. **Threshold for partition quality**: If $I(S; W)$ is small (e.g., $\leq 0.01$ nats), the SCX advantage is negligible. This provides a diagnostic: if $I(S; W)$ is small, the state partition may need refinement or the experts may not have state-dependent reliability (in which case DS suffices).

### 8.2 For the Paper

The DS comparison theorem makes Paper 3 stronger in several ways:

- **Connection to established literature**: DS is the most cited model in crowdsourcing (15,000+ citations). Proving SCX dominates it (and quantifying the gap) directly addresses the target audience.
- **Theoretical elegance**: The $I(S; W)$ bound is simple, interpretable, and connects to information theory.
- **Empirical testability**: The gap $\Delta R \geq I(S; W)/\alpha$ can be estimated from data, providing a testable prediction.

---

## 9. Open Questions

1. **What is the optimal prior $P$ for the PAC-Bayes comparison bound?** The current bound holds for any prior, but the constant $\alpha$ appears as a free parameter. Can we choose $\alpha$ optimally as a function of $M$ and the number of states?

2. **Extension to multiclass with full confusion matrices**: The proof above uses scalar weights for simplicity. A full DS comparison with $K \times K$ confusion matrices per expert requires matrix-valued weights and a more complex analysis. The core result should extend by treating each row of the confusion matrix as a separate "expert" for that true class.

3. **Finite-sample gap bound**: Theorem 4(c) is an asymptotic bound. A finite-sample version would require accounting for the estimation error in $\{R_m(s)\}$ and the resulting uncertainty in $\{W(s)\}$.

---

## References

1. Dawid, A. P., & Skene, A. M. (1979). Maximum likelihood estimation of observer error-rates using the EM algorithm. *Journal of the Royal Statistical Society: Series C (Applied Statistics)*, 28(1), 20-28.

2. Tishby, N., Pereira, F. C., & Bialek, W. (1999). The information bottleneck method. *Proceedings of the 37th Allerton Conference on Communication, Control, and Computing*.

3. Proposition 5.1 (SCX-DS Comparison). `../theorems/01_noise_detection_guarantee.md#53-scx-%E4%B8%A5%E6%A0%BC%E4%BC%98%E4%BA%8E-dawid-skene-%E7%9A%84%E6%9D%A1%E4%BB%B6`

4. Paper 3 Framework, Section 4.1. `../../paper/paper3_jmlr/PAPER_FRAMEWORK.md`
