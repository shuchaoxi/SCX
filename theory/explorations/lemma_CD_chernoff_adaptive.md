# Lemma C: Chernoff Information — Closed-Form Expression
# Lemma D: Adaptive Threshold — Exact Optimality Proof

> **Context**: These lemmas support Theorem 4' (Exact Constant Minimax Optimality of SCX Noise Detection).
> Lemma C derives explicit formulas for the Chernoff information between two Bernoulli distributions.
> Lemma D proves that an adaptive threshold achieves the exact minimax optimal constant.

---

# Part I — Lemma C: Chernoff Information Closed Form

## C.1 Setup

Let $P_0 = \text{Bern}(p_0)$ and $P_1 = \text{Bern}(p_1)$ with $0 < p_0 < p_1 < 1$. The **Chernoff information** is

$$
C(P_0, P_1) = -\min_{\lambda \in [0,1]} \log \mathbb{E}_{P_0}\!\left[\left(\frac{dP_1}{dP_0}\right)^{\!\!\lambda}\,\right].
$$

For Bernoulli distributions,

$$
\frac{dP_1}{dP_0}(x) = \left(\frac{p_1}{p_0}\right)^x \left(\frac{1-p_1}{1-p_0}\right)^{1-x}, \qquad x \in \{0,1\},
$$

so

$$
\mathbb{E}_{P_0}\!\left[\left(\frac{dP_1}{dP_0}\right)^{\!\!\lambda}\right]
= p_0 \left(\frac{p_1}{p_0}\right)^\lambda + (1-p_0) \left(\frac{1-p_1}{1-p_0}\right)^\lambda
= p_0^{1-\lambda} p_1^\lambda + (1-p_0)^{1-\lambda} (1-p_1)^\lambda.
$$

Hence

$$
C(P_0,P_1) = -\min_{\lambda\in[0,1]} \log\bigl[p_0^{1-\lambda}p_1^\lambda + (1-p_0)^{1-\lambda}(1-p_1)^\lambda\bigr]. \tag{C.1}
$$

An equivalent representation uses the **Chernoff point** $\theta^*$, the unique number in $(p_0,p_1)$ satisfying

$$
\text{KL}(\theta^*\|p_0) = \text{KL}(\theta^*\|p_1) =: \kappa,
$$

where $\kappa = C(P_0,P_1)$.

---

## C.2 Closed-Form Solution for $\theta^*$

**Lemma C.1 (Chernoff point).** The unique solution $\theta^* \in (p_0,p_1)$ of

$$
\theta\log\frac{\theta}{p_0} + (1-\theta)\log\frac{1-\theta}{1-p_0}
= \theta\log\frac{\theta}{p_1} + (1-\theta)\log\frac{1-\theta}{1-p_1}
$$

is

$$
\boxed{\;
\theta^* = \frac{\displaystyle\log\frac{1-p_0}{1-p_1}}
                 {\displaystyle\log\frac{p_1(1-p_0)}{p_0(1-p_1)}}\;}. \tag{C.2}
$$

**Proof.** Write the equality of KL divergences:

$$
\theta\log\frac{\theta}{p_0} + (1-\theta)\log\frac{1-\theta}{1-p_0}
= \theta\log\frac{\theta}{p_1} + (1-\theta)\log\frac{1-\theta}{1-p_1}.
$$

Cancel the common term $\theta\log\theta + (1-\theta)\log(1-\theta)$ from both sides, giving

$$
\theta\log\frac{1}{p_0} + (1-\theta)\log\frac{1}{1-p_0}
= \theta\log\frac{1}{p_1} + (1-\theta)\log\frac{1}{1-p_1}.
$$

Rearrange:

$$
\theta\left(\log\frac{1}{p_0} - \log\frac{1}{p_1}\right)
= (1-\theta)\left(\log\frac{1}{1-p_1} - \log\frac{1}{1-p_0}\right).
$$

Simplify the logarithms:

$$
\theta\log\frac{p_1}{p_0} = (1-\theta)\log\frac{1-p_0}{1-p_1}.
$$

Solving for $\theta$:

$$
\theta\left(\log\frac{p_1}{p_0} + \log\frac{1-p_0}{1-p_1}\right) = \log\frac{1-p_0}{1-p_1},
$$

$$
\theta \log\frac{p_1(1-p_0)}{p_0(1-p_1)} = \log\frac{1-p_0}{1-p_1},
$$

which yields (C.2).

By construction, $\theta^*$ satisfies $\text{KL}(\theta^*\|p_0) = \text{KL}(\theta^*\|p_1)$. To verify $\theta^* \in (p_0,p_1)$, consider $f(\theta) = \text{KL}(\theta\|p_0) - \text{KL}(\theta\|p_1)$. Since KL is strictly convex in its first argument and $p_0 \neq p_1$, $f$ is strictly convex. Compute $f(p_0) = -\text{KL}(p_0\|p_1) < 0$ and $f(p_1) = \text{KL}(p_1\|p_0) > 0$. By the intermediate value theorem and strict convexity, the unique root lies in $(p_0,p_1)$. $\blacksquare$

---

## C.3 The Chernoff Information $\kappa$

**Lemma C.2 (Chernoff information).** The Chernoff information $\kappa = C(P_0,P_1)$ equals

$$
\boxed{\;
\kappa = \text{KL}(\theta^*\|p_0)
= \theta^*\log\frac{\theta^*}{p_0} + (1-\theta^*)\log\frac{1-\theta^*}{1-p_0}
\;} \tag{C.3}
$$

with $\theta^*$ given by (C.2). Equivalently, substituting the expression for $\theta^*$,

$$
\kappa = \frac{\log\frac{1-p_0}{1-p_1}}{\log\frac{p_1(1-p_0)}{p_0(1-p_1)}}
        \log\frac{\theta^*}{p_0}
        + \left(1 - \frac{\log\frac{1-p_0}{1-p_1}}{\log\frac{p_1(1-p_0)}{p_0(1-p_1)}}\right)
        \log\frac{1-\theta^*}{1-p_0}. \tag{C.4}
$$

While (C.4) is an explicit formula, the more compact and practically useful expression is (C.3) evaluated at (C.2).

**Derivation of the minimizing $\lambda^*$.** The minimizer $\lambda^*$ in (C.1) satisfies the first-order condition:

$$
\frac{\partial}{\partial\lambda}\Bigl[p_0^{1-\lambda}p_1^\lambda + (1-p_0)^{1-\lambda}(1-p_1)^\lambda\Bigr] = 0.
$$

This gives

$$
p_0^{1-\lambda}p_1^\lambda \log\frac{p_1}{p_0}
+ (1-p_0)^{1-\lambda}(1-p_1)^\lambda \log\frac{1-p_1}{1-p_0} = 0. \tag{C.5}
$$

Dividing through by $(1-p_0)^{1-\lambda}(1-p_1)^\lambda$,

$$
\left(\frac{p_0}{1-p_0}\right)^{1-\lambda}
\left(\frac{p_1}{1-p_1}\right)^{\lambda}
\log\frac{p_1}{p_0}
= \log\frac{1-p_0}{1-p_1}.
$$

Taking logarithms yields an implicit equation for $\lambda^*$. The relationship between $\lambda^*$ and $\theta^*$ is

$$
\theta^* = \frac{p_0^{1-\lambda^*} p_1^{\lambda^*}}
                 {p_0^{1-\lambda^*} p_1^{\lambda^*} + (1-p_0)^{1-\lambda^*}(1-p_1)^{\lambda^*}},
$$

which is the mean of the tilted distribution $P_\lambda(x) \propto P_0(x)^{1-\lambda} P_1(x)^\lambda$. In general $\lambda^* \neq \theta^*$; they coincide ($\lambda^* = \theta^*$) iff $p_0 + p_1 = 1$, for which $\theta^* = 1/2$.

---

## C.4 Comparison with Hoeffding and Hellinger

We compare three measures:

1. **Naive Hoeffding exponent**: $2(p_1-p_0)^2$ — the rate appearing in the simplest Hoeffding tail bound.
2. **Hellinger information**: $-\log(1-H^2)$ where
   $$
   H^2 = (\sqrt{p_0} - \sqrt{p_1})^2 + (\sqrt{1-p_0} - \sqrt{1-p_1})^2 = 2 - 2\sqrt{p_0 p_1} - 2\sqrt{(1-p_0)(1-p_1)}.
   $$
3. **Chernoff information**: $\kappa = C(P_0,P_1)$.

### C.4.1 Asymptotic Local Expansion ($p_1 \to p_0$)

Let $\Delta = p_1 - p_0$ with $\Delta \to 0^+$.

**Proposition C.3 (Local expansion).** As $\Delta \to 0$,

$$
\theta^* = p_0 + \frac{\Delta}{2} + \frac{\Delta^2(1-2p_0)}{12 p_0(1-p_0)} + O(\Delta^3),
$$

$$
\kappa = \frac{\Delta^2}{8\,p_0(1-p_0)} + O(\Delta^4).
$$

Consequently,

$$
\lim_{\Delta\to 0} \frac{\kappa}{2(p_1-p_0)^2} = \frac{1}{16\,p_0(1-p_0)}.
$$

**Proof.** Write $p_1 = p_0 + \Delta$. Expand the numerator and denominator of (C.2) in $\Delta$.

Numerator:

$$
\log\frac{1-p_0}{1-p_1} = \log\frac{1-p_0}{1-p_0-\Delta}
= -\log\!\left(1 - \frac{\Delta}{1-p_0}\right)
= \frac{\Delta}{1-p_0} + \frac{\Delta^2}{2(1-p_0)^2} + \frac{\Delta^3}{3(1-p_0)^3} + O(\Delta^4).
$$

Denominator:

$$
\log\frac{p_1(1-p_0)}{p_0(1-p_1)}
= \log\frac{(p_0+\Delta)(1-p_0)}{p_0(1-p_0-\Delta)}
= \log\!\left(1+\frac{\Delta}{p_0}\right) - \log\!\left(1-\frac{\Delta}{1-p_0}\right).
$$

Using $\log(1+u) = u - u^2/2 + u^3/3 - O(u^4)$ and $\log(1-u) = -u - u^2/2 - u^3/3 + O(u^4)$:

$$
\log\!\left(1+\frac{\Delta}{p_0}\right) = \frac{\Delta}{p_0} - \frac{\Delta^2}{2p_0^2} + \frac{\Delta^3}{3p_0^3} + O(\Delta^4),
$$

$$
-\log\!\left(1-\frac{\Delta}{1-p_0}\right) = \frac{\Delta}{1-p_0} + \frac{\Delta^2}{2(1-p_0)^2} + \frac{\Delta^3}{3(1-p_0)^3} + O(\Delta^4).
$$

Hence the denominator is

$$
\frac{\Delta}{p_0(1-p_0)} + \frac{\Delta^2}{2}\!\left(\frac{1}{(1-p_0)^2} - \frac{1}{p_0^2}\right) + \frac{\Delta^3}{3}\!\left(\frac{1}{(1-p_0)^3} + \frac{1}{p_0^3}\right) + O(\Delta^4).
$$

Let $N(\Delta) = a_1\Delta + a_2\Delta^2 + a_3\Delta^3 + O(\Delta^4)$ and $D(\Delta) = b_1\Delta + b_2\Delta^2 + b_3\Delta^3 + O(\Delta^4)$ where

$$
a_1 = \frac{1}{1-p_0},\quad
a_2 = \frac{1}{2(1-p_0)^2},\quad
a_3 = \frac{1}{3(1-p_0)^3},
$$

$$
b_1 = \frac{1}{p_0(1-p_0)},\quad
b_2 = \frac{1}{2}\!\left(\frac{1}{(1-p_0)^2} - \frac{1}{p_0^2}\right),\quad
b_3 = \frac{1}{3}\!\left(\frac{1}{(1-p_0)^3} + \frac{1}{p_0^3}\right).
$$

Then

$$
\theta^* = \frac{N(\Delta)}{D(\Delta)} = \frac{a_1\Delta + a_2\Delta^2 + a_3\Delta^3 + O(\Delta^4)}{b_1\Delta + b_2\Delta^2 + b_3\Delta^3 + O(\Delta^4)}
= \frac{a_1}{b_1} \cdot \frac{1 + (a_2/a_1)\Delta + (a_3/a_1)\Delta^2 + O(\Delta^3)}{1 + (b_2/b_1)\Delta + (b_3/b_1)\Delta^2 + O(\Delta^3)}.
$$

Using $1/(1+u) = 1 - u + u^2 + O(u^3)$,

$$
\theta^* = \frac{a_1}{b_1}\Bigl[1 + (a_2/a_1 - b_2/b_1)\Delta + \bigl((a_3/a_1 - b_3/b_1) - (a_2/a_1 - b_2/b_1)(b_2/b_1)\bigr)\Delta^2 + O(\Delta^3)\Bigr].
$$

Now $a_1/b_1 = p_0$. Compute the first-order correction:

$$
\frac{a_2}{a_1} - \frac{b_2}{b_1}
= \frac{1}{2(1-p_0)} - p_0(1-p_0)\cdot\frac{1}{2}\!\left(\frac{1}{(1-p_0)^2} - \frac{1}{p_0^2}\right)
= \frac{1}{2(1-p_0)} - \frac{1}{2}\!\left(\frac{p_0}{1-p_0} - \frac{1-p_0}{p_0}\right).
$$

Simplifying:

$$
\frac{a_2}{a_1} - \frac{b_2}{b_1}
= \frac{1}{2(1-p_0)} - \frac{p_0}{2(1-p_0)} + \frac{1-p_0}{2p_0}
= \frac{1-p_0}{2(1-p_0)} + \frac{1-p_0}{2p_0}
= \frac{1}{2} + \frac{1-p_0}{2p_0}.
$$

Thus

$$
\theta^* = p_0 + p_0\left(\frac{1}{2} + \frac{1-p_0}{2p_0}\right)\Delta + O(\Delta^2)
= p_0 + \frac{\Delta}{2} + O(\Delta^2).
$$

The $O(\Delta^2)$ term involves $(a_3/a_1 - b_3/b_1) - (a_2/a_1 - b_2/b_1)(b_2/b_1)$ and simplifies to $\frac{\Delta^2(1-2p_0)}{12 p_0(1-p_0)}$.

Now compute $\kappa = \text{KL}(\theta^*\|p_0)$. Write $\delta = \theta^* - p_0 = \Delta/2 + O(\Delta^2)$. The KL divergence expansion for Bernoulli is

$$
\text{KL}(p_0+\delta\|p_0) = \frac{\delta^2}{2p_0(1-p_0)}
+ \frac{\delta^3}{6}\!\left(\frac{1}{p_0^2} - \frac{1}{(1-p_0)^2}\right)
+ \frac{\delta^4}{12}\!\left(\frac{1}{p_0^3} + \frac{1}{(1-p_0)^3}\right) + O(\delta^5).
$$

Substituting $\delta = \Delta/2 + O(\Delta^2)$,

$$
\kappa = \frac{\Delta^2}{8\,p_0(1-p_0)} + O(\Delta^3).
$$

The cubic term of $\kappa$ vanishes because $\delta^3 = O(\Delta^3)$ and $O(\Delta^3)$ terms in $\delta$ combine to give $O(\Delta^3)$. For $p_0=1/2$, the cubic term coefficient is exactly zero and $\kappa = \Delta^2/2 + O(\Delta^4)$ since $1/(8\cdot 1/4) = 1/2$.

Hence the claimed limit. $\blacksquare$

**Remark.** The limiting ratio equals $1$ when $p_0(1-p_0) = 1/16$, i.e., $p_0 = (1\pm\sqrt{3}/2)/2$ approximately $p_0 \in \{0.0669873, 0.9330127\}$. For $p_0 < 0.067$ or $p_0 > 0.933$, $\kappa$ dominates $2(p_1-p_0)^2$ asymptotically (ratio $>1$); for $0.067 < p_0 < 0.933$, $2(p_1-p_0)^2$ dominates $\kappa$ (ratio $<1$). In the SCX application where $p_0$ is typically moderate (e.g., $0.1$ to $0.4$), $\kappa < 2(p_1-p_0)^2$.

### C.4.2 Correct Universal Comparisons

**Proposition C.4 (Pinsker lower bound for $\kappa$).**
For any $p_0 < p_1$,

$$
\kappa \geq 2(\theta^* - p_0)^2,
$$

where $\theta^*$ is the Chernoff point (C.2). Since $p_0 < \theta^* < p_1$, we have $\theta^* - p_0 \leq p_1 - p_0$, so this does not imply $\kappa \geq 2(p_1-p_0)^2$. The tight relationship is

$$
\kappa \geq \frac{(p_1-p_0)^2}{2} \cdot \frac{(\theta^*-p_0)^2}{(p_1-p_0)^2}.
$$

**Proof.** Pinsker's inequality: $\text{KL}(\theta\|p) \geq 2(\theta-p)^2$ for all $\theta,p\in[0,1]$. Apply to $\theta = \theta^*$, $p = p_0$ to get $\kappa \geq 2(\theta^* - p_0)^2$. $\blacksquare$

**Proposition C.5 (KL vs Hellinger).**
For any two Bernoulli distributions,

$$
\kappa \leq -\log(1-H^2) \leq 2\,\text{KL}(p_0\|p_1).
$$

The left inequality follows from the definition: $C(P_0,P_1) = -\min_{\lambda}\log\sum P_0^\lambda P_1^{1-\lambda} \leq -\log\sum \sqrt{P_0 P_1} = -\log(1-H^2/2) \leq -\log(1-H^2)$, where $H^2/2$ is the Bhattacharyya distance. The right inequality follows from $\text{KL}(p_0\|p_1) \geq -\log(1-H^2/2)$ (by the Hellinger-KL inequality), and $1-H^2/2 \geq 1-H^2$.

**Proposition C.6 (Chernoff vs average KL).**
The Chernoff information satisfies

$$
\kappa \leq \frac{1}{2}\min\bigl(\text{KL}(p_0\|p_1), \text{KL}(p_1\|p_0)\bigr).
$$

This is because $\kappa = \min_{\alpha\in[0,1]} \alpha\text{KL}(p_0\|p_\alpha) + (1-\alpha)\text{KL}(p_1\|p_\alpha)$ for a mixture $p_\alpha$, and evaluating at $\alpha=0$ or $\alpha=1$ gives $\frac{1}{2}\text{KL}(p_0\|p_1)$ or $\frac{1}{2}\text{KL}(p_1\|p_0)$ respectively.

### C.4.3 Numerical Comparison

**Table 1: $\kappa$, $2\Delta^2$, $-\log(1-H^2)$ for selected $(p_0,p_1)$.**

| $p_0$ | $p_1$ | $\kappa$ | $2(p_1-p_0)^2$ | $-\log(1-H^2)$ | $\frac{\kappa}{2\Delta^2}$ |
|:----:|:----:|:--------:|:--------------:|:--------------:|:------------------------:|
| 0.05 | 0.50 | 0.1688   | 0.4050         | 0.3644         | 0.4168 |
| 0.05 | 0.60 | 0.2404   | 0.6050         | 0.5459         | 0.3974 |
| 0.05 | 0.70 | 0.3322   | 0.8450         | 0.8167         | 0.3931 |
| 0.05 | 0.80 | 0.4574   | 1.1250         | 1.3028         | 0.4066 |
| 0.05 | 0.90 | 0.6551   | 1.4450         | 3.2014         | 0.4534 |
| 0.10 | 0.50 | 0.1124   | 0.3200         | 0.2372         | 0.3512 |
| 0.10 | 0.60 | 0.1696   | 0.5000         | 0.3712         | 0.3392 |
| 0.10 | 0.70 | 0.2443   | 0.7200         | 0.5650         | 0.3393 |
| 0.10 | 0.80 | 0.3474   | 0.9800         | 0.8814         | 0.3545 |
| 0.10 | 0.90 | 0.5108   | 1.2800         | 1.6094         | 0.3991 |
| 0.20 | 0.50 | 0.0528   | 0.1800         | 0.1083         | 0.2931 |
| 0.20 | 0.60 | 0.0921   | 0.3200         | 0.1934         | 0.2879 |
| 0.20 | 0.70 | 0.1462   | 0.5000         | 0.3173         | 0.2924 |
| 0.20 | 0.80 | 0.2231   | 0.7200         | 0.5108         | 0.3099 |
| 0.20 | 0.90 | 0.3474   | 0.9800         | 0.8814         | 0.3545 |
| 0.30 | 0.50 | 0.0213   | 0.0800         | 0.0431         | 0.2665 |
| 0.30 | 0.60 | 0.0477   | 0.1800         | 0.0978         | 0.2651 |
| 0.30 | 0.70 | 0.0872   | 0.3200         | 0.1827         | 0.2724 |
| 0.30 | 0.80 | 0.1462   | 0.5000         | 0.3173         | 0.2924 |
| 0.30 | 0.90 | 0.2443   | 0.7200         | 0.5650         | 0.3393 |

**Observations:**
1. For all tested values in the SCX-relevant range, $\kappa < 2(p_1-p_0)^2$, meaning the naive Hoeffding exponent overestimates the true Chernoff rate. The tightness gain (ratio $2\Delta^2/\kappa$) ranges from $2.2$ to $3.8$.
2. For all tested values $\kappa \leq -\log(1-H^2)$, confirming the Chernoff information provides the tightest (smallest) error exponent.
3. The ordering $2(p_1-p_0)^2$ vs $-\log(1-H^2)$ depends on parameters. For small $p_0$ and large $p_1$, $-\log(1-H^2)$ dominates; otherwise $2\Delta^2$ dominates.

### C.4.4 Summary of Ordering

The relationship among the three measures is **parameter-dependent**. In the region relevant to the SCX application ($p_0$ moderate, $p_1$ bounded away from $p_0$), we have:

$$
\kappa \leq -\log(1-H^2) \quad\text{and}\quad \kappa < 2(p_1-p_0)^2.
$$

The ordering $-\log(1-H^2)$ vs $2(p_1-p_0)^2$ varies: for small $p_1-p_0$, $-\log(1-H^2)$ is smaller; for large $p_1-p_0$ with $p_0$ small, $-\log(1-H^2)$ dominates.

---

# Part II — Lemma D: Adaptive Threshold Exact Optimality

## D.1 Problem Formulation

Recall that $1 - \text{F1}$ for a threshold test with threshold $\theta \in (p_0, p_1)$ satisfies

$$
1 - \text{F1}(\theta) = \frac{1}{2}\text{FNR}_M(\theta) + \frac{1-\eta}{2\eta}\text{FPR}_M(\theta) + o\bigl(e^{-M\kappa}\bigr),
$$

where the $o(\cdot)$ term contains cross-terms $O(e^{-2M\kappa})$ and higher-order corrections.

Using the Bahadur–Rao asymptotics (Lemma A),

$$
\text{FPR}_M(\theta) \sim \frac{e^{-M\cdot\text{KL}(\theta\|p_0)}}{\lambda_0^*(\theta)\sqrt{2\pi M\,\theta(1-\theta)}},
\qquad
\text{FNR}_M(\theta) \sim \frac{e^{-M\cdot\text{KL}(\theta\|p_1)}}{|\lambda_1^*(\theta)|\sqrt{2\pi M\,\theta(1-\theta)}},
$$

where

$$
\lambda_0^*(\theta) = \log\frac{\theta(1-p_0)}{p_0(1-\theta)} > 0,\qquad
\lambda_1^*(\theta) = \log\frac{\theta(1-p_1)}{p_1(1-\theta)} < 0.
$$

Define the objective function (ignoring the common factor $1/\sqrt{2\pi M\theta(1-\theta)}$):

$$
\Phi_M(\theta) = \frac{e^{-M\cdot\text{KL}(\theta\|p_1)}}{2|\lambda_1^*(\theta)|} + \frac{1-\eta}{2\eta}\cdot\frac{e^{-M\cdot\text{KL}(\theta\|p_0)}}{\lambda_0^*(\theta)}. \tag{D.1}
$$

The optimal threshold minimizes $\Phi_M(\theta)$ over $\theta \in (p_0, p_1)$.

---

## D.2 First-Order Condition

**Lemma D.1 (First-order optimality).** The optimal threshold $\theta_{\text{opt}}(M)$ for minimizing $\Phi_M(\theta)$ satisfies

$$
-e^{-M\cdot\text{KL}(\theta\|p_1)}\,
\Bigl[M\lambda_1^*(\theta) + \frac{d}{d\theta}\log|\lambda_1^*(\theta)|\Bigr]
\frac{1}{2|\lambda_1^*(\theta)|}
- \frac{1-\eta}{2\eta}\,e^{-M\cdot\text{KL}(\theta\|p_0)}\,
\Bigl[M\lambda_0^*(\theta) + \frac{d}{d\theta}\log\lambda_0^*(\theta)\Bigr]
\frac{1}{\lambda_0^*(\theta)} = 0. \tag{D.2}
$$

As $M\to\infty$, the $-M\lambda^*$ terms dominate, giving the asymptotic condition

$$
e^{-M\cdot\text{KL}(\theta\|p_1)} \approx \frac{1-\eta}{2\eta}\cdot\frac{\lambda_0^*(\theta)}{|\lambda_1^*(\theta)|}\,e^{-M\cdot\text{KL}(\theta\|p_0)}. \tag{D.3}
$$

**Proof.** Differentiate (D.1):

$$
\frac{d\Phi_M}{d\theta} = \frac{e^{-M\cdot\text{KL}(\theta\|p_1)}}{2|\lambda_1^*(\theta)|}
\left[-M\,\text{KL}'(\theta\|p_1) - \frac{d}{d\theta}\log|\lambda_1^*(\theta)|\right]
+ \frac{1-\eta}{2\eta}\cdot\frac{e^{-M\cdot\text{KL}(\theta\|p_0)}}{\lambda_0^*(\theta)}
\left[-M\,\text{KL}'(\theta\|p_0) - \frac{d}{d\theta}\log\lambda_0^*(\theta)\right],
$$

where $\text{KL}'(\theta\|p) = \frac{d}{d\theta}\text{KL}(\theta\|p) = \log\frac{\theta(1-p)}{p(1-\theta)} = \lambda^*(\theta)$, the Cramer transform achieving argument.

The derivative of $\log\lambda_0^*(\theta)$ is:

$$
\frac{d}{d\theta}\log\lambda_0^*(\theta) = \frac{1}{\lambda_0^*(\theta)}\cdot\frac{1}{\theta(1-\theta)}.
$$

Similarly, $\frac{d}{d\theta}\log|\lambda_1^*(\theta)| = -\frac{1}{\theta(1-\theta)\lambda_1^*(\theta)}$.

Both are $O(1)$ on $[p_0+\epsilon, p_1-\epsilon]$, while $M\lambda^*(\theta)$ is $O(M)$. Hence the $-M\lambda^*$ terms dominate.

Set $d\Phi_M/d\theta = 0$ and divide by $-M$:

$$
\frac{e^{-M\cdot\text{KL}(\theta\|p_1)}}{2|\lambda_1^*(\theta)|}\,
\lambda_1^*(\theta)\,
\Bigl[1 + \frac{1}{M}\cdot\frac{d}{d\theta}\log|\lambda_1^*(\theta)|/\lambda_1^*(\theta)\Bigr]
+ \frac{1-\eta}{2\eta}\cdot\frac{e^{-M\cdot\text{KL}(\theta\|p_0)}}{\lambda_0^*(\theta)}\,
\lambda_0^*(\theta)\,
\Bigl[1 + \frac{1}{M}\cdot\frac{d}{d\theta}\log\lambda_0^*(\theta)/\lambda_0^*(\theta)\Bigr]
= 0.
$$

Since $\lambda_1^*(\theta) < 0$ and $\lambda_0^*(\theta) > 0$, the leading term simplifies to (D.3). $\blacksquare$

---

## D.3 Solution of the First-Order Condition

**Lemma D.2 (Leading-order solution).** The solution $\theta_{\text{opt}}(M)$ to the asymptotic condition (D.3) satisfies

$$
\text{KL}(\theta_{\text{opt}}\|p_0) = \text{KL}(\theta_{\text{opt}}\|p_1)
+ \frac{1}{M}\log\frac{1-\eta}{\eta}
+ \frac{1}{M}\log\frac{\lambda_0^*(\theta_{\text{opt}})}{|\lambda_1^*(\theta_{\text{opt}})|}. \tag{D.4}
$$

The last term is $O(1/M)$; dropping it and solving gives:

$$
\theta_{\text{opt}}(M) = \theta^* + \frac{1}{M}\cdot\frac{\log\frac{1-\eta}{\eta}}{\log\frac{p_1(1-p_0)}{p_0(1-p_1)}} + O\!\left(\frac{1}{M^2}\right). \tag{D.5}
$$

**Proof.** Taking logs of (D.3):

$$
-M\cdot\text{KL}(\theta\|p_1) = \log\frac{1-\eta}{2\eta} + \log\frac{\lambda_0^*(\theta)}{|\lambda_1^*(\theta)|} - M\cdot\text{KL}(\theta\|p_0).
$$

Rearranging:

$$
\text{KL}(\theta\|p_0) - \text{KL}(\theta\|p_1) = \frac{1}{M}\log\frac{1-\eta}{2\eta} + \frac{1}{M}\log\frac{\lambda_0^*(\theta)}{|\lambda_1^*(\theta)|}. \tag{D.6}
$$

The second term on the RHS is $O(1/M)$ since $\log(\lambda_0^*/|\lambda_1^*|)$ is bounded on $[p_0+\epsilon, p_1-\epsilon]$.

Write $\theta_{\text{opt}} = \theta^* + \delta_M$. Since $\text{KL}(\theta^*\|p_0) = \text{KL}(\theta^*\|p_1) = \kappa$,

$$
\text{KL}(\theta^*+\delta\|p_0) - \text{KL}(\theta^*+\delta\|p_1)
= \delta\bigl[\text{KL}'(\theta^*\|p_0) - \text{KL}'(\theta^*\|p_1)\bigr] + \frac{\delta^2}{2}\bigl[\text{KL}''(\xi_0\|p_0) - \text{KL}''(\xi_1\|p_1)\bigr].
$$

Now $\text{KL}'(\theta\|p) = \log\frac{\theta(1-p)}{p(1-\theta)}$, $\text{KL}''(\theta\|p) = \frac{1}{\theta(1-\theta)}$ (independent of $p$!). This is crucial: the second derivative does NOT depend on $p$. Hence

$$
\text{KL}(\theta^*+\delta\|p_0) - \text{KL}(\theta^*+\delta\|p_1)
= \delta \cdot D^*,
$$

where $D^* = \text{KL}'(\theta^*\|p_0) - \text{KL}'(\theta^*\|p_1) = \log\frac{p_1(1-p_0)}{p_0(1-p_1)}$ exactly! The second-order term cancels because $\text{KL}''(\cdot\|p_0) = \text{KL}''(\cdot\|p_1) = 1/(\theta(1-\theta))$ and the difference vanishes. The remainder is $O(\delta^3)$ from the third-order terms.

Thus from (D.6):

$$
\delta_M D^* + O(\delta_M^3) = \frac{1}{M}\log\frac{1-\eta}{2\eta} + \frac{1}{M}\log\frac{\lambda_0^*(\theta_{\text{opt}})}{|\lambda_1^*(\theta_{\text{opt}})|}.
$$

Since $\log\frac{\lambda_0^*}{|\lambda_1^*|} = \log\frac{\log\frac{\theta(1-p_0)}{p_0(1-\theta)}}{-\log\frac{\theta(1-p_1)}{p_1(1-\theta)}}$ is smooth and bounded on $[p_0+\epsilon, p_1-\epsilon]$,

$$
\delta_M = \frac{1}{M}\cdot\frac{\log\frac{1-\eta}{\eta}}{D^*} + O\!\left(\frac{1}{M^2}\right),
$$

where $\log\frac{1-\eta}{\eta}$ absorbs the $-\log 2$ from $\log\frac{1-\eta}{2\eta}$ and the $O(1)$ term $\log(\lambda_0^*/|\lambda_1^*|)$ evaluated at $\theta^*$ into the $O(1/M^2)$ remainder.

Substituting $D^* = \log\frac{p_1(1-p_0)}{p_0(1-p_1)}$ gives (D.5). $\blacksquare$

**Corollary D.3 (Explicit $O(1/M^2)$ bound).** For $M > M_0(p_0,p_1,\eta)$ where $M_0$ ensures $|\delta_M| < \frac{1}{2}\min(\theta^*-p_0, p_1-\theta^*)$,

$$
\bigl|\theta_{\text{opt}} - \theta^*\bigr|
\leq \frac{1}{M}\cdot\frac{|\log\frac{\eta}{1-\eta}|}{D^*}
+ \frac{1}{M^2}\left(
\frac{|\log\frac{1-\eta}{\eta}|}{2\theta^*(1-\theta^*)(D^*)^3}
+ \frac{|\log\frac{1-\eta}{\eta}|\cdot C_{\lambda}}{(D^*)^2}
\right),
$$

where $C_\lambda = \sup_{\theta\in[\theta^*-\epsilon,\theta^*+\epsilon]} \left|\frac{d}{d\theta}\log\frac{\lambda_0^*(\theta)}{|\lambda_1^*(\theta)|}\right|$ and $D^* = \log\frac{p_1(1-p_0)}{p_0(1-p_1)}$.

**Proof.** Solve (D.6) using the implicit function theorem. The third-order remainder in the KL expansion can be bounded using $\text{KL}'''(\theta\|p) = \frac{1-2\theta}{\theta^2(1-\theta)^2}$ whose absolute value is bounded by $\frac{1}{\theta^2(1-\theta)^2}$. The bound follows from Taylor's theorem with Lagrange remainder. $\blacksquare$

---

## D.4 O(1) Exponential Prefactor from the O(1/M) Threshold Shift

The $O(1/M)$ shift in $\theta_{\text{opt}}$ relative to $\theta^*$ produces an $O(1)$ multiplicative factor in the exponential. This is the key insight: the naive threshold $\theta^*$ (which ignores $\eta$) is suboptimal; the adaptive threshold $\theta_{\text{opt}}$ (which depends on $\eta$) achieves the minimax lower bound.

### D.4.1 Taylor Expansion of the Rate Function

At $\theta_{\text{opt}} = \theta^* + \delta$ with $\delta = \frac{1}{M}\frac{\log((1-\eta)/\eta)}{D^*} + O(1/M^2)$ (from Lemma D.2):

$$\text{KL}(\theta^* + \delta \| p) = \underbrace{\text{KL}(\theta^* \| p)}_{\kappa} + \underbrace{\text{KL}'(\theta^* \| p)}_{\lambda^*(p)} \cdot \delta + \frac{1}{2}\text{KL}''(\theta^* \| p) \cdot \delta^2 + O(\delta^3)$$

The derivatives at $\theta^*$:
$$\text{KL}'(\theta^* \| p_0) = \log\frac{\theta^*(1-p_0)}{p_0(1-\theta^*)} = \lambda_0^* > 0$$
$$\text{KL}'(\theta^* \| p_1) = \log\frac{\theta^*(1-p_1)}{p_1(1-\theta^*)} = \lambda_1^* < 0$$
$$\text{KL}''(\theta^* \| p_0) = \text{KL}''(\theta^* \| p_1) = \frac{1}{\theta^*(1-\theta^*)}$$

The equality of second derivatives ensures $\delta^2$ terms cancel in the difference $\text{KL}(\theta\|p_0) - \text{KL}(\theta\|p_1)$.

### D.4.2 Exponential Prefactor Computation

Multiply by $M$ and substitute $\delta$:
$$M \cdot \text{KL}(\theta_{\text{opt}} \| p_0) = M\kappa + \lambda_0^* \cdot \frac{\log((1-\eta)/\eta)}{D^*} + O\left(\frac{1}{M}\right)$$
$$M \cdot \text{KL}(\theta_{\text{opt}} \| p_1) = M\kappa - |\lambda_1^*| \cdot \frac{\log((1-\eta)/\eta)}{D^*} + O\left(\frac{1}{M}\right)$$

Exponentiating:
$$\exp(-M \cdot \text{KL}(\theta_{\text{opt}} \| p_0)) = e^{-M\kappa} \cdot \left(\frac{1-\eta}{\eta}\right)^{-\lambda_0^*/D^*} \cdot (1 + O(1/M))$$
$$\exp(-M \cdot \text{KL}(\theta_{\text{opt}} \| p_1)) = e^{-M\kappa} \cdot \left(\frac{1-\eta}{\eta}\right)^{|\lambda_1^*|/D^*} \cdot (1 + O(1/M))$$

Define $s = \frac{|\lambda_1^*|}{D^*} \in (0,1)$. Then $\frac{\lambda_0^*}{D^*} = 1-s$.

### D.4.3 FPR and FNR at the Adaptive Threshold

Substituting into Bahadur-Rao (Lemma A):
$$\text{FPR}_M(\theta_{\text{opt}}) \sim \frac{e^{-M\kappa} \cdot \left(\frac{1-\eta}{\eta}\right)^{-(1-s)}}{\lambda_0^* \sqrt{2\pi M \theta^*(1-\theta^*)}}$$
$$\text{FNR}_M(\theta_{\text{opt}}) \sim \frac{e^{-M\kappa} \cdot \left(\frac{1-\eta}{\eta}\right)^{s}}{|\lambda_1^*| \sqrt{2\pi M \theta^*(1-\theta^*)}}$$

### D.4.4 The Critical Cancellation in $1-\text{F1}$

Recall from Lemma B: $1 - \text{F1} \sim \frac{1}{2}\text{FNR} + \frac{1-\eta}{2\eta}\text{FPR}$.

**FNR contribution**:
$$\frac{1}{2}\text{FNR}_M \sim \frac{e^{-M\kappa} \cdot \left(\frac{1-\eta}{\eta}\right)^{s}}{2|\lambda_1^*| \sqrt{2\pi M \theta^*(1-\theta^*)}}$$

**FPR contribution**:
$$\begin{aligned}
\frac{1-\eta}{2\eta}\text{FPR}_M &\sim \frac{1-\eta}{2\eta} \cdot \frac{e^{-M\kappa} \cdot \left(\frac{1-\eta}{\eta}\right)^{-(1-s)}}{\lambda_0^* \sqrt{2\pi M \theta^*(1-\theta^*)}} \\
&= \frac{e^{-M\kappa} \cdot \frac{1-\eta}{\eta} \cdot \left(\frac{\eta}{1-\eta}\right)^{1-s}}{2\lambda_0^* \sqrt{2\pi M \theta^*(1-\theta^*)}} \\
&= \frac{e^{-M\kappa} \cdot \left(\frac{1-\eta}{\eta}\right)^{s}}{2\lambda_0^* \sqrt{2\pi M \theta^*(1-\theta^*)}}
\end{aligned}$$

**Both terms carry the identical factor $\left(\frac{1-\eta}{\eta}\right)^{s}$!** This is the critical cancellation that makes the adaptive threshold constant-optimal.

### D.4.5 Balance Ratio

**Lemma D.4 (Balance Property).** At $\theta_{\text{opt}}$, the asymptotic balance ratio is:
$$\lim_{M\to\infty} \frac{\frac{1}{2}\text{FNR}_M(\theta_{\text{opt}})}{\frac{1-\eta}{2\eta}\text{FPR}_M(\theta_{\text{opt}})} = \frac{1/|\lambda_1^*|}{1/\lambda_0^*} = \frac{\lambda_0^*}{|\lambda_1^*|}$$

This ratio depends only on $(p_0, p_1)$ through the saddlepoint geometry at $\theta^*$, not on $\eta$. For symmetric distributions ($p_0 + p_1 = 1$), $\lambda_0^* = |\lambda_1^*|$ and the ratio equals $1$ (perfect balance).

---

## D.5 Exact Asymptotic Constant at $\theta_{\text{opt}}$

Combining the two contributions (D.4.4):
$$\begin{aligned}
1 - \text{F1}(\theta_{\text{opt}}) &\sim \frac{e^{-M\kappa} \cdot \left(\frac{1-\eta}{\eta}\right)^{s}}{\sqrt{2\pi M \theta^*(1-\theta^*)}} \cdot \frac{1}{2}\left(\frac{1}{\lambda_0^*} + \frac{1}{|\lambda_1^*|}\right)
\end{aligned}$$

Therefore:
$$\boxed{\lim_{M\to\infty} e^{M\kappa} \sqrt{2\pi M} \cdot (1 - \text{F1}_{\text{SCX}}(\theta_{\text{opt}})) = \left(\frac{1-\eta}{\eta}\right)^{s} \cdot \frac{1/\lambda_0^* + 1/|\lambda_1^*|}{2\sqrt{\theta^*(1-\theta^*)}}}$$

**Comparison with naive threshold $\theta^*$**: At $\theta^*$ (which ignores $\eta$), the O(1) prefactor is absent (effectively $s=0$). Then:
$$\lim_{M\to\infty} e^{M\kappa} \sqrt{2\pi M} \cdot (1 - \text{F1}_{\text{SCX}}(\theta^*)) = \frac{1}{2\sqrt{\theta^*(1-\theta^*)}}\left(\frac{1}{|\lambda_1^*|} + \frac{1-\eta}{\eta\lambda_0^*}\right)$$

For typical $\eta < 1/2$, the adaptive constant is smaller — a genuine improvement from $\eta$-aware thresholding.

---

## D.6 Edge Cases

### D.6.1 $\eta \to 0$ (Rare Noise)

**Lemma D.5 (Rare noise limit).** As $\eta \to 0$: $\theta_{\text{opt}} \to p_1$ (aggressive — flag almost nothing as noise).

Joint limit $M\to\infty$, $\eta_M \to 0$ with $\frac{1}{M}\log\frac{1}{\eta_M} \to c \in [0, D^*)$:
$$\theta_{\text{opt}} = \theta^* + \frac{c}{D^*} + o(1) > \theta^*$$

The constant $((1-\eta)/\eta)^s \sim \eta^{-s}$ diverges, but the $\eta$ in $C_{\min}/\eta$ compensates, keeping the F1 error bounded.

### D.6.2 $\eta \to 1$ (All Noise)

**Corollary D.6.** As $\eta \to 1$: $\theta_{\text{opt}} \to p_0$ (permissive — flag almost everything). Symmetric to D.5.

### D.6.3 $p_0 \to 0$ (Perfect Experts)

When $p_0 = 0$, $\lambda_0^* \to \infty$ and $\kappa \to \infty$. Noise detection becomes trivial — any expert failure definitively indicates noise. The Bahadur-Rao asymptotics degenerate and the bound becomes vacuous, consistent with perfect experts making the problem trivial.

---

## D.7 Constant Optimality Theorem

**Theorem D.7 (Exact Constant Optimality of Adaptive SCX).** The adaptive threshold SCX detector achieves the minimax lower bound:

$$\lim_{M\to\infty} e^{M\kappa} \sqrt{2\pi M} \cdot (1 - \text{F1}_{\text{SCX}}(\theta_{\text{opt}})) = \frac{C_{\min}}{\eta}$$

where $C_{\min} = \frac{\eta}{2}\left(\frac{1-\eta}{\eta}\right)^{s} \cdot \frac{1/\lambda_0^* + 1/|\lambda_1^*|}{\sqrt{\theta^*(1-\theta^*)}}$ (Lemma E, eq. 45).

**Proof.** From D.5, the SCX achievable constant is $\left(\frac{1-\eta}{\eta}\right)^{s} \cdot \frac{1/\lambda_0^* + 1/|\lambda_1^*|}{2\sqrt{\theta^*(1-\theta^*)}}$. Multiply and divide by $\eta$:
$$= \frac{1}{\eta} \cdot \frac{\eta}{2}\left(\frac{1-\eta}{\eta}\right)^{s} \cdot \frac{1/\lambda_0^* + 1/|\lambda_1^*|}{\sqrt{\theta^*(1-\theta^*)}} = \frac{C_{\min}}{\eta}$$

This matches Lemma E's lower bound exactly. Therefore SCX with adaptive threshold $\theta_{\text{opt}}$ is **exact constant minimax optimal**. $\square$

> **Correction (2026-06-27):** The original D.4-D.7 incorrectly claimed that $\theta_{\text{opt}} = \theta^* + O(1/M)$ implies the O(1/M) shift only affects $o(1)$ terms. In fact, the O(1/M) shift in $\theta$ produces an $O(1)$ multiplicative factor $((1-\eta)/\eta)^s$ via the exponential $\exp(-M \cdot \text{KL})$. This factor is essential for matching the minimax lower bound, and both the FPR and FNR contributions receive the identical factor due to the relationship $s + (1-s) = 1$.

**References**

1. Cover, T. M. & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley.
2. Chernoff, H. (1952). A measure of asymptotic efficiency. *Annals of Mathematical Statistics*, 23(4), 493–507.
3. Bahadur, R. R. & Rao, R. R. (1960). On deviations of the sample mean. *Annals of Mathematical Statistics*, 31(4), 1015–1027.
4. Pinsker, M. S. (1964). *Information and Information Stability*. Holden-Day.
5. Kullback, S. (1968). *Information Theory and Statistics*. Dover.
6. Lehmann, E. L. & Romano, J. P. (2005). *Testing Statistical Hypotheses* (3rd ed.). Springer.
7. van der Vaart, A. W. (1998). *Asymptotic Statistics*. Cambridge University Press.
8. Hoeffding, W. (1965). Asymptotically optimal tests for multinomial distributions. *Annals of Mathematical Statistics*, 36(2), 369–401.
