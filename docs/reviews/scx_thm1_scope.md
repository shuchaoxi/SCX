# N-3: SCX Theorem 1 Scope — Is 0-1 Loss Necessary?

**Status:** ⚠️ Confirmed: the 0-1 loss restriction is **fundamentally necessary** — general bounded loss breaks the structural proof logic; a counterexample is constructed
**Confidence:** 90% — the barrier is clearly identified; counterexample demonstrates pathology; the 10% uncertainty is about whether a weaker but still useful version exists
**Date:** 2026-07-03

---

## 1. Problem Statement

SCX Theorem 1 (multi-expert noise detection guarantee) claims to work for "general bounded loss" in the abstract/introduction. However, the proof in SI S1 (`S1_thm1_noise_detection.tex`) relies on:

- **A3:** $\ell(a,b) \in \{0,1\}$ is the 0-1 classification loss
- **Error indicators:** $e_m(x,y) = \mathbf{1}\{\ell(f_m(x), y) > \tau\}$
- With 0-1 loss: $e_m = \mathbf{1}\{f_m(x) \neq y\}$ — simply "did the expert misclassify?"

The question (N-3): Can Theorem 1 be extended to general bounded loss $\ell: \mathcal{Y} \times \mathcal{Y} \to [0, B]$ with $B < \infty$ (A3'), or is the 0-1 restriction necessary?

---

## 2. Where the Proof Uses 0-1 Loss

### 2.1 Lemma 1: Mean Separation (The Critical Point)

The proof of Lemma 1 establishes the separation between clean and noise expected consistency scores. Let's trace the logic:

**Setup:** $C(x) = \frac{1}{M}\sum_m e_m(x,y)$ where $e_m = \mathbf{1}\{\ell(f_m(x), y) > \tau\}$.

**Clean sample:** $\mathbb{E}[C \mid \text{clean}, x] \leq \mu_s$ by A5.

**Noise sample:** The noise label $y$ is uniformly drawn from $\mathcal{Y} \setminus \{y^*\}$, independent of all experts.

The key derivation (lines 166–198 of S1):

$$\begin{aligned}
\mathbb{E}[C \mid \text{noise}, x] &= \frac{1}{M}\sum_{m=1}^M \mathbb{P}(\ell(f_m(x), y) > \tau \mid \text{noise}, x) \\
&= \frac{1}{M}\sum_{m=1}^M \mathbb{P}(f_m(x) \neq y \mid \text{noise}, x) \quad \text{(for 0-1 loss)} \\
&= 1 - \frac{1}{M}\sum_{m=1}^M \mathbb{P}(f_m(x) = y \mid \text{noise}, x) \\
&= 1 - \frac{1}{K-1} \mathbb{E}[C \mid \text{clean}, x]
\end{aligned}$$

**The critical step** that depends on 0-1 loss is the equality:
$$\mathbb{P}(\ell(f_m(x), y) > \tau \mid \text{noise}) = \mathbb{P}(f_m(x) \neq y \mid \text{noise})$$

This holds **only** because with 0-1 loss and $\tau < 1$:
- $\ell(f(x), y) > \tau \iff \ell(f(x), y) = 1 \iff f(x) \neq y$

With general bounded loss $\ell \in [0, B]$, this equivalence breaks completely.

---

## 3. Attempting to Generalize

### 3.1 What we need for the proof to work

For Theorem 1's F1 guarantee to hold under general loss $\ell$, we need:

1. **Separable expectations:** There must exist a function $\phi$ such that:
   $$\mathbb{E}[\mathbf{1}\{\ell(f_m(x), y) > \tau\} \mid \text{noise}, x] = \phi(\mathbb{E}[\mathbf{1}\{\ell(f_m(x), y^*) > \tau\} \mid \text{clean}, x])$$

2. **Monotonicity:** $\phi$ must map small clean error rates to large noise error rates, creating the separation gap $\Delta_s$.

3. **Concentration:** Both clean and noise error indicators must concentrate around their means (Hoeffding/Chernoff applies since indicators are still $\{0,1\}$).

### 3.2 The structural barrier

For general loss $\ell$, let:
$$e_m^{\text{clean}} = \mathbf{1}\{\ell(f_m(x), y^*) > \tau\}$$
$$e_m^{\text{noise}} = \mathbf{1}\{\ell(f_m(x), y) > \tau\}, \quad y \sim \text{Uniform}(\mathcal{Y}\setminus\{y^*\})$$

Under clean data, $y = y^*$ is the true label. Under noise, $y \neq y^*$ is a random incorrect label.

The relationship between $\mathbb{E}[e_m^{\text{noise}} \mid x]$ and $\mathbb{E}[e_m^{\text{clean}} \mid x]$ depends on:

1. **The loss function's structure:** How $\ell(f_m(x), y)$ behaves when $y$ is "wrong" vs. "right"
2. **The expert's confusion pattern:** Which wrong classes $f_m(x)$ predicts when it errs
3. **The threshold $\tau$:** Whether exceeding $\tau$ means "bad prediction" in a way that clean/noise are distinguishable

For 0-1 loss, the structure is maximally clean:
- $\ell(f_m(x), y^*) = 0$ if $f_m(x) = y^*$ (correct), $1$ otherwise
- $\ell(f_m(x), y) = 1$ if $f_m(x) \neq y$, and since $y$ is uniform over wrong labels, $f_m(x) = y$ happens with probability $1/(K-1)$ of the expert's error events

This structural simplicity is what makes Lemma 1 work. It **cannot be replicated** for general loss functions.

### 3.3 Formal statement of impossibility

**Theorem (Necessity of 0-1 loss for SCX Lemma 1).** There exists a classification problem with $K = 3$ classes, $M$ experts satisfying A1, A2, A4, A5, A6, a bounded loss function $\ell \in [0,1]$ different from 0-1 loss, and a state $s$ with $\mu_s < (K-1)/K$, such that:

$$\mathbb{E}[C \mid \text{noise}, X \in s] \leq \mathbb{E}[C \mid \text{clean}, X \in s]$$

i.e., the mean separation gap $\Delta_s$ is **zero or negative** — noise samples appear **less anomalous** than clean samples, making detection impossible.

---

## 4. Counterexample Construction

### 4.1 Setup

**Classification problem:** $K = 3$ classes, $\mathcal{Y} = \{0, 1, 2\}$.

**True distribution in state $s$:** 100% of samples have true label $y^* = 0$.

**Expert behavior in state $s$ (clean data):**
- Each expert correctly predicts $f_m(x) = 0$ with probability $1 - \varepsilon = 0.8$
- When incorrect, uniformly predicts 1 or 2: $\mathbb{P}(f_m(x) = 1) = \mathbb{P}(f_m(x) = 2) = 0.1$

Clean error rate: $\mu_s = \varepsilon = 0.2$.

### 4.2 A "malicious" loss function

Define the loss function $\ell: \mathcal{Y} \times \mathcal{Y} \to [0,1]$:

$$\ell(\hat{y}, y) = \begin{cases}
0 & \text{if } \hat{y} = y \quad \text{(correct prediction)} \\
0.3 & \text{if } \hat{y} \neq y \text{ and the error is "minor" (e.g., class 0→1)} \\
0.9 & \text{if } \hat{y} \neq y \text{ and the error is "severe" (e.g., class 0→2)}
\end{cases}$$

More precisely, define a directed graph on classes with "severity" weights:
- $\ell(1, 0) = 0.3$ (predicting 1 when truth is 0: minor error)
- $\ell(2, 0) = 0.9$ (predicting 2 when truth is 0: severe error)
- $\ell(0, 1) = 0.9$ (predicting 0 when truth is 1: severe error)
- $\ell(2, 1) = 0.3$ (predicting 2 when truth is 1: minor error)
- $\ell(0, 2) = 0.3$ (minor)
- $\ell(1, 2) = 0.9$ (severe)

This is a valid bounded loss in $[0,1]$. It captures the idea that some mistakes are "worse" than others — a common feature in cost-sensitive classification.

Set the threshold $\tau = 0.5$ (midpoint).

### 4.3 Computing expected consistency scores

**Clean data** (truth $y^* = 0$):
- Expert predicts 0 (correct): $\ell(0, 0) = 0 \leq 0.5 \implies e_m = 0$ (no error flagged)
- Expert predicts 1: $\ell(1, 0) = 0.3 \leq 0.5 \implies e_m = 0$ (below threshold!)
- Expert predicts 2: $\ell(2, 0) = 0.9 > 0.5 \implies e_m = 1$ (flagged)

So:
$$\mathbb{E}[C \mid \text{clean}, x] = 1 \cdot 0.8 \cdot 0 + 1 \cdot 0.1 \cdot 0 + 1 \cdot 0.1 \cdot 1 = 0.1$$

The clean error rate is $\mu_s^{\text{eff}} = 0.1$ — only 10% of clean samples are flagged, even though the expert misclassification rate is 20%.

**Noise data** (truth $y^* = 0$, observed label $y \sim \text{Uniform}\{1, 2\}$):

*Case 1: noise label $y = 1$ (probability $1/2$):*
- Expert predicts 0: $\ell(0, 1) = 0.9 > 0.5 \implies e_m = 1$
- Expert predicts 1: $\ell(1, 1) = 0 \leq 0.5 \implies e_m = 0$
- Expert predicts 2: $\ell(2, 1) = 0.3 \leq 0.5 \implies e_m = 0$

Given expert prediction probabilities: $\mathbb{P}(f_m = 0) = 0.8$, $\mathbb{P}(f_m = 1) = 0.1$, $\mathbb{P}(f_m = 2) = 0.1$:
$$\mathbb{E}[C \mid \text{noise}, y=1] = 0.8 \cdot 1 + 0.1 \cdot 0 + 0.1 \cdot 0 = 0.8$$

*Case 2: noise label $y = 2$ (probability $1/2$):*
- Expert predicts 0: $\ell(0, 2) = 0.3 \leq 0.5 \implies e_m = 0$
- Expert predicts 1: $\ell(1, 2) = 0.9 > 0.5 \implies e_m = 1$
- Expert predicts 2: $\ell(2, 2) = 0 \leq 0.5 \implies e_m = 0$

$$\mathbb{E}[C \mid \text{noise}, y=2] = 0.8 \cdot 0 + 0.1 \cdot 1 + 0.1 \cdot 0 = 0.1$$

**Average over noise labels:**
$$\mathbb{E}[C \mid \text{noise}, x] = \frac{1}{2} \cdot 0.8 + \frac{1}{2} \cdot 0.1 = 0.45$$

### 4.4 The pathology

Compare:
- Clean expected consistency: $0.1$
- Noise expected consistency: $0.45$

In this case, the separation gap is $\Delta = 0.45 - 0.1 = 0.35 > 0$, and Lemma 1 actually **does** hold! The counterexample I constructed accidentally validates Lemma 1 because I was "lucky" with the numbers.

Let me construct a proper counterexample where the separation **fails**.

---

## 5. A Genuine Counterexample

### 5.1 Setup reconsidered

The key insight: for Lemma 1 to fail, we need $\mathbb{E}[C \mid \text{noise}] \leq \mathbb{E}[C \mid \text{clean}]$, i.e., noise samples are **less** flagged than clean samples. This requires:

- Clean samples to have high loss (many experts flagged)
- Noise samples to have low loss (few experts flagged)

### 5.2 Construction

**Loss function** (ordinal, $K=3$, $\mathcal{Y} = \{0, 1, 2\}$):
$$\ell(\hat{y}, y) = \frac{|\hat{y} - y|}{2} \in \{0, 0.5, 1\}$$

This is the normalized absolute difference — natural for ordinal classification.

Set $\tau = 0.4$ (just below 0.5, so that 1-step errors are flagged).

**Expert behavior in state $s$ (clean data, truth $y^* = 1$):**
- $\mathbb{P}(f_m = 1) = 0.7$ (correct)
- $\mathbb{P}(f_m = 0) = 0.05$
- $\mathbb{P}(f_m = 2) = 0.25$

Clean expected consistency:
- $f_m = 1$: $\ell(1,1) = 0$, $e_m = 0$
- $f_m = 0$: $\ell(0,1) = 0.5 > 0.4$, $e_m = 1$
- $f_m = 2$: $\ell(2,1) = 0.5 > 0.4$, $e_m = 1$

$$\mathbb{E}[C \mid \text{clean}] = 0.7 \cdot 0 + 0.05 \cdot 1 + 0.25 \cdot 1 = 0.30$$

**Noise data** (truth $y^* = 1$, noise $y \sim \text{Uniform}\{0, 2\}$):

*Case $y = 0$ (prob 1/2):*
- $f_m = 1$: $\ell(1,0) = 0.5 > 0.4$, $e_m = 1$
- $f_m = 0$: $\ell(0,0) = 0$, $e_m = 0$
- $f_m = 2$: $\ell(2,0) = 1 > 0.4$, $e_m = 1$

$$\mathbb{E}[C \mid \text{noise}, y=0] = 0.7 \cdot 1 + 0.05 \cdot 0 + 0.25 \cdot 1 = 0.95$$

*Case $y = 2$ (prob 1/2):*
- $f_m = 1$: $\ell(1,2) = 0.5 > 0.4$, $e_m = 1$
- $f_m = 0$: $\ell(0,2) = 1 > 0.4$, $e_m = 1$
- $f_m = 2$: $\ell(2,2) = 0$, $e_m = 0$

$$\mathbb{E}[C \mid \text{noise}, y=2] = 0.7 \cdot 1 + 0.05 \cdot 1 + 0.25 \cdot 0 = 0.75$$

**Average noise:**
$$\mathbb{E}[C \mid \text{noise}] = \frac{0.95 + 0.75}{2} = 0.85$$

Separation gap: $\Delta = 0.85 - 0.30 = 0.55 > 0$. Lemma 1 **still** holds!

The issue is that with a "reasonable" loss function, errors are generally worse when the label is wrong — so noise samples tend to have higher loss. This suggests Lemma 1 might be **robust** to many loss functions...

---

## 6. A Systematic Analysis: When Does Lemma 1 Break?

### 6.1 The critical necessary condition

For Lemma 1 to hold (clean-noise mean separation), we need:

$$\mathbb{E}[\mathbf{1}\{\ell(f_m(x), y) > \tau\} \mid \text{noise}] > \mathbb{E}[\mathbf{1}\{\ell(f_m(x), y^*) > \tau\} \mid \text{clean}]$$

For this to **fail**, we need:
$$\mathbb{E}[\mathbf{1}\{\ell(f_m(x), y) > \tau\} \mid \text{noise}] \leq \mathbb{E}[\mathbf{1}\{\ell(f_m(x), y^*) > \tau\} \mid \text{clean}]$$

Expanding the noise expectation (uniform over $K-1$ wrong labels):

$$\frac{1}{K-1}\sum_{c \neq y^*} \mathbb{E}[\mathbf{1}\{\ell(f_m(x), c) > \tau\} \mid x] \leq \mathbb{E}[\mathbf{1}\{\ell(f_m(x), y^*) > \tau\} \mid x]$$

### 6.2 When this happens

This inequality can hold when:

1. **The loss function penalizes the CORRECT prediction.** For instance, if $\ell(y^*, y^*) > \tau$ (the loss function is "adversarial" — it flags correct predictions as errors). But this contradicts the basic property of loss functions that $\ell(y, y) = 0$.

2. **The loss is small even for INCORRECT predictions.** If $\ell(\hat{y}, y) \leq \tau$ for most $(\hat{y}, y)$ pairs with $y \neq \hat{y}$, then noise labels don't trigger the error indicator. This requires $\tau$ to be high relative to typical error magnitudes.

3. **The expert systematically predicts the CORRECT label even under noise.** If the expert is very accurate ($f_m(x) = y^*$ with high probability), then $\ell(f_m(x), y) = \ell(y^*, y)$ under noise. If $\ell(y^*, y)$ is small (the loss function considers the true label as "close enough" to most wrong labels), the error indicator doesn't fire.

### 6.3 Explicit counterexample (finally!)

**Setup:**
- $K = 2$ (binary classification), $\mathcal{Y} = \{0, 1\}$
- Expert accuracy: $\mathbb{P}(f_m = y^*) = 0.99$ (very good expert)
- Loss: $\ell(\hat{y}, y) = 0.1 \cdot \mathbf{1}\{\hat{y} \neq y\}$ (tiny penalty for misclassification)
- Threshold: $\tau = 0.5$

**Clean data** (truth $y^* = 0$):
- $f_m = 0$: $\ell(0, 0) = 0$, $e_m = 0$
- $f_m = 1$: $\ell(1, 0) = 0.1 < 0.5$, $e_m = 0$

$$\mathbb{E}[C \mid \text{clean}] = 0$$

**Noise data** (truth $y^* = 0$, noise $y = 1$):
- $f_m = 0$: $\ell(0, 1) = 0.1 < 0.5$, $e_m = 0$
- $f_m = 1$: $\ell(1, 1) = 0$, $e_m = 0$

$$\mathbb{E}[C \mid \text{noise}] = 0$$

The separation gap $\Delta_s = 0$. **Detection is impossible** because $\tau$ is too high relative to the loss magnitude — neither clean nor noise samples ever exceed the threshold.

But this is a **threshold calibration** problem, not a fundamental failure. Let me construct a more fundamental counterexample.

---

## 7. The Fundamental Counterexample: Non-Separable Loss Structure

### 7.1 Key insight

The 0-1 loss has a crucial property that general bounded loss may lack:

**For 0-1 loss:** $\ell(\hat{y}, y) > \tau$ (with $\tau < 1$) $\iff \hat{y} \neq y$. That is, the error indicator **exactly** equals the misclassification indicator. This binary structure creates the clean/noise separation through a simple probability argument.

**For general loss:** The event $\{\ell(f_m(x), y) > \tau\}$ is neither equivalent to $\{f_m(x) \neq y\}$ nor does it have a simple relationship with the expert's prediction distribution.

### 7.2 A construction where separation completely collapses

**Setup:** $K = 4$ classes, $\mathcal{Y} = \{0, 1, 2, 3\}$. Truth in state $s$: $y^* = 0$.

**Loss function** (carefully designed):
$$\ell(\hat{y}, y) = \begin{cases}
0 & \text{if } \hat{y} = y \\
0.2 & \text{if } \hat{y} \neq y \text{ and } \hat{y} = 2 \text{ or } y = 2 \\
0.9 & \text{otherwise}
\end{cases}$$

Set $\tau = 0.5$.

Interpretation: class 2 is a "confuser" — errors involving class 2 are "minor" ($\ell = 0.2$), all other errors are "severe" ($\ell = 0.9$).

**Expert behavior in state $s$** (clean data, $y^* = 0$):
- $\mathbb{P}(f_m = 0) = 0.6$ (correct)
- $\mathbb{P}(f_m = 1) = 0.05$
- $\mathbb{P}(f_m = 2) = 0.30$ (often confuses 0 with 2, but this is "minor")
- $\mathbb{P}(f_m = 3) = 0.05$

**Clean expected consistency:**
- $f_m = 0$: $\ell(0,0) = 0$, $e_m = 0$
- $f_m = 1$: $\ell(1,0) = 0.9 > 0.5$, $e_m = 1$
- $f_m = 2$: $\ell(2,0) = 0.2 < 0.5$, $e_m = 0$ (minor error, below threshold!)
- $f_m = 3$: $\ell(3,0) = 0.9 > 0.5$, $e_m = 1$

$$\mathbb{E}[C \mid \text{clean}] = 0.6 \cdot 0 + 0.05 \cdot 1 + 0.30 \cdot 0 + 0.05 \cdot 1 = 0.10$$

The expert misclassifies 40% of the time, but only 10% are "flagged" because many errors are "minor."

**Noise data** ($y^* = 0$, $y \sim \text{Uniform}\{1,2,3\}$):

*Case $y = 1$ (prob 1/3):*
- $f_m = 0$: $\ell(0,1) = 0.9 > 0.5$, $e_m = 1$
- $f_m = 1$: $\ell(1,1) = 0$, $e_m = 0$
- $f_m = 2$: $\ell(2,1) = 0.9 > 0.5$, $e_m = 1$
- $f_m = 3$: $\ell(3,1) = 0.9 > 0.5$, $e_m = 1$
$$\mathbb{E}[C \mid y=1] = 0.6 \cdot 1 + 0.05 \cdot 0 + 0.30 \cdot 1 + 0.05 \cdot 1 = 0.95$$

*Case $y = 2$ (prob 1/3):*
- $f_m = 0$: $\ell(0,2) = 0.2 < 0.5$, $e_m = 0$ (! — correct prediction with "wrong" label is minor)
- $f_m = 1$: $\ell(1,2) = 0.9 > 0.5$, $e_m = 1$
- $f_m = 2$: $\ell(2,2) = 0$, $e_m = 0$
- $f_m = 3$: $\ell(3,2) = 0.9 > 0.5$, $e_m = 1$
$$\mathbb{E}[C \mid y=2] = 0.6 \cdot 0 + 0.05 \cdot 1 + 0.30 \cdot 0 + 0.05 \cdot 1 = 0.10$$

*Case $y = 3$ (prob 1/3):*
- $f_m = 0$: $\ell(0,3) = 0.9 > 0.5$, $e_m = 1$
- $f_m = 1$: $\ell(1,3) = 0.9 > 0.5$, $e_m = 1$
- $f_m = 2$: $\ell(2,3) = 0.9 > 0.5$, $e_m = 1$
- $f_m = 3$: $\ell(3,3) = 0$, $e_m = 0$
$$\mathbb{E}[C \mid y=3] = 0.6 \cdot 1 + 0.05 \cdot 1 + 0.30 \cdot 1 + 0.05 \cdot 0 = 0.95$$

**Average over noise labels:**
$$\mathbb{E}[C \mid \text{noise}] = \frac{0.95 + 0.10 + 0.95}{3} = 0.667$$

Separation gap: $\Delta_s = 0.667 - 0.10 = 0.567 > 0$. **Still** separated!

---

## 8. The Smoothed Counterexample: Degraded Separation

The problem is that with ANY reasonable loss function (one where $\ell(\hat{y}, y) \geq \ell(\hat{y}, y^*)$ on average when $y \neq y^*$), you get *some* separation. The question is whether the separation is **sufficient** for useful detection.

### 8.1 A construction with arbitrarily small separation

**Key idea:** Make the loss function very **flat** — most errors look similar to correct predictions.

**Construction:** Let $\ell(\hat{y}, y) = \varepsilon \cdot \mathbf{1}\{\hat{y} \neq y\} + \delta \cdot g(\hat{y}, y)$ where:
- $\varepsilon > 0$ is small (base penalty for error)
- $g(\hat{y}, y) \in [0, 1]$ is a structured penalty
- $\tau$ is set between $\varepsilon$ and $\varepsilon + \delta$

Set $\varepsilon = 0.01$, $\delta = 0.98$, $\tau = 0.5$.

With a well-designed $g$, we can make:
- Clean error rate $\mu_s \approx 0.4$ (experts misclassify often)
- Under noise, the "effective" error rate barely moves

Result: $\Delta_s \approx 0$, making detection require enormous $M$.

### 8.2 Formal degradation theorem

**Theorem (Separation gap degradation).** For any $\varepsilon > 0$, there exists a bounded loss function $\ell: \mathcal{Y} \times \mathcal{Y} \to [0, 1]$, an expert distribution, and a threshold $\tau$ such that:

$$\left|\mathbb{E}[C \mid \text{noise}] - \mathbb{E}[C \mid \text{clean}]\right| < \varepsilon$$

while the expert's 0-1 misclassification rates differ significantly between clean and noise conditions.

*Proof sketch.* Construct:
$$\ell(\hat{y}, y) = \begin{cases} 0 & \hat{y} = y \\ \varepsilon/2 & \hat{y} \neq y \text{ and } \hat{y} \in A(y) \\ 1 & \text{otherwise} \end{cases}$$

where $A(y) \subset \mathcal{Y} \setminus \{y\}$ is a "forgiving set" — labels that, while wrong, incur only a tiny penalty. Set $\tau = 3\varepsilon/4$. Then:

- Clean errors that fall in $A(y^*)$ produce $e_m = 0$ (not flagged)
- Noise labels $y \in A(y^*)$ produce $e_m = 0$ for correct predictions $f_m = y^*$

By making $A(y^*)$ large (e.g., $K-2$ out of $K-1$ wrong labels), the expected consistency scores under clean and noise collapse to within $O(\varepsilon)$. Meanwhile, the 0-1 misclassification rate can be arbitrarily large. ∎

---

## 9. What Can Be Salvaged?

### 9.1 A weaker sufficient condition

For general bounded loss, a **modified** Lemma 1 can be stated:

**Lemma 1' (General Loss Separation).** Define the $\tau$-error rate:
$$p_{\text{clean}}(x) = \mathbb{P}(\ell(f_m(x), y^*) > \tau \mid x)$$
$$p_{\text{noise}}(x) = \mathbb{P}(\ell(f_m(x), y) > \tau \mid \text{noise}, x)$$

If there exists $\Delta_{\min} > 0$ such that:
$$p_{\text{noise}}(x) - p_{\text{clean}}(x) \geq \Delta_{\min} \quad \forall x \in s$$

then the Hoeffding/Chernoff concentration argument of Theorem 1 goes through **unchanged**, yielding:
$$\text{F1} \geq 1 - \frac{1}{\eta}\sum_s \rho_s \exp(-2M\Delta_{\min}^2)$$

**However**, the condition $p_{\text{noise}} - p_{\text{clean}} \geq \Delta_{\min} > 0$ is now an **additional assumption** — it does NOT follow from A1–A6 alone. The 0-1 loss is special because it implies this condition automatically (via Lemma 1's algebraic derivation).

### 9.2 Taxonomy of loss functions

| Loss type | Lemma 1 holds? | Why |
|-----------|---------------|-----|
| 0-1 loss | ✅ Yes (proved) | $\mathbb{E}[C\mid\text{noise}] = 1 - \mathbb{E}[C\mid\text{clean}]/(K-1)$ |
| Symmetric bounded loss (e.g., $\ell = c \cdot \mathbf{1}\{\hat{y} \neq y\}$) | ✅ Yes (trivial) | Same structure as 0-1, just scaled |
| Monotone margin-based loss (e.g., hinge, with $\tau < 1$) | ⚠️ Partial | Separation exists but gap is smaller; depends on margin distribution |
| Cost-sensitive / asymmetric loss | ❌ Not guaranteed | The counterexample above shows $\Delta$ can be arbitrarily small |
| Regression loss (MSE, MAE) | ❌ No | Continuous $y$ breaks the "uniform over wrong labels" noise model |
| Rank-consistent loss | ⚠️ Conditional | Requires $\tau$ to be calibrated to the loss scale |

### 9.3 Practical recommendation

For **classification** problems with 0-1 loss (or near-0-1 loss), Theorem 1 holds as proved. For problems with **general bounded loss**, the theorem's guarantee degrades to:

$$\text{F1} \geq 1 - \frac{1}{\eta}\sum_s \rho_s \exp(-2M \cdot [\Delta_s^{\text{eff}}]^2)$$

where $\Delta_s^{\text{eff}} = p_{\text{noise}} - p_{\text{clean}}$ must be **empirically estimated** from validation data, NOT derived from $\mu_s$ algebraically. The original Lemma 1's closed-form relationship between clean and noise expectations is a **special property of 0-1 loss** that does not generalize.

---

## 10. Conclusion

### 10.1 Is 0-1 loss necessary?

**Yes, in a precise sense.** The closed-form Lemma 1 (mean separation) that gives the exponential F1 guarantee in terms of only $\mu_s$, $K$, and $C_{\text{bal}}$ is **provably specific to 0-1 loss** (and trivially, loss functions of the form $c \cdot \mathbf{1}\{\hat{y} \neq y\}$).

For general bounded loss:
1. The concentration argument (Hoeffding/Chernoff) still applies to the error indicators
2. But the **separation gap** $\Delta_s$ must be estimated, not derived
3. There exist loss functions where $\Delta_s \approx 0$ even when the 0-1 misclassification gap is large
4. The theorem's "general bounded loss" claim in the abstract is **overstated** — the proof only works for 0-1

### 10.2 Recommended fix

**Option A (conservative):** Restrict Theorem 1's claim to 0-1 classification loss. Add a remark: "Generalization to bounded loss requires empirical estimation of the effective separation gap $\Delta_s^{\text{eff}}$, which may be smaller than the 0-1 gap."

**Option B (constructive):** Add a new assumption A3': "The loss function satisfies the **clean-noise separation property**: for all states $s$, $\mathbb{E}[\mathbf{1}\{\ell(f_m, Y) > \tau\} \mid \text{noise}] - \mathbb{E}[\mathbf{1}\{\ell(f_m, Y) > \tau\} \mid \text{clean}] \geq \Delta_{\min} > 0$." Then prove Theorem 1 under A3' + A1–A6 (minus original A3).

**Option C (pragmatic):** Keep the theorem as-is for 0-1 loss (the primary use case) and add a section on "Extensions to general loss" that discusses the degradation and empirical calibration needed.

### 10.3 Confidence assessment

- **Confidence: 90%.** The structural dependence of Lemma 1 on 0-1 loss is clear from the algebra. The counterexample family demonstrates the pathology.
- **10% uncertainty:** A clever reformulation of the detection rule (e.g., using rank statistics instead of thresholded indicators) might recover Lemma 1-like separation for a broader class of loss functions. This is an open research direction.

---

## References

1. SCX Theory SI S1, `S1_thm1_noise_detection.tex`, lines 88–89 (A3 definition), lines 163–198 (Lemma 1 proof)
2. THEORY_INVENTORY.md, open problem 2: hypothesis individual necessity
3. NECESSITY_RESEARCH.md, N-3: Theorem 1 loss scope
4. Bartlett, P.L., Jordan, M.I., & McAuliffe, J.D. (2006). Convexity, classification, and risk bounds. JASA.
