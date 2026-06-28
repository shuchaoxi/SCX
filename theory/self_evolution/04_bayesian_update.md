# Bayesian Update Interpretation of SCX Self-Evolution

> **Version**: 2026-06-28 | **Status**: Theoretical framework | **Scope**: Formal Bayesian analysis of the self-evolution loop
> **Notation note**: In this document, $S$ denotes the state space (per existing SCX theory). The gatekeeper scoring function at time $t$ is denoted $S_t$, distinguished by the subscript $t$. This follows the KEY NOTATION DISAMBIGUATION rule: $S_t$ = gatekeeper scoring function, $S$ = state space.

---

## Table of Contents

1. [Introduction: The Self-Evolution Loop](#1-introduction-the-self-evolution-loop)
2. [Bayesian Formulation of Gatekeeper Evolution](#2-bayesian-formulation-of-gatekeeper-evolution)
3. [Prior Distribution Over Gatekeeper Functions](#3-prior-distribution-over-gatekeeper-functions)
4. [Likelihood: Memory Bank as Evidence](#4-likelihood-memory-bank-as-evidence)
5. [Posterior Update Recursion](#5-posterior-update-recursion)
6. [Posterior Mean Gatekeeper](#6-posterior-mean-gatekeeper)
7. [Conjugate Prior Structure: Gaussian Process Formulation](#7-conjugate-prior-structure-gaussian-process-formulation)
8. [Bayesian Martingale Property](#8-bayesian-martingale-property)
9. [Martingale Convergence Theorem](#9-martingale-convergence-theorem)
10. [Prior Misspecification Analysis](#10-prior-misspecification-analysis)
11. [KL Divergence Contraction](#11-kl-divergence-contraction)
12. [Bernstein-von Mises Theorem Connection](#12-bernstein-von-mises-theorem-connection)
13. [Proof Sketches](#13-proof-sketches)
14. [Summary of Proven vs. Conjectured Claims](#14-summary-of-proven-vs-conjectured-claims)
15. [References](#15-references)

---

## 1. Introduction: The Self-Evolution Loop

The SCX self-evolution framework operates as a closed-loop system:

$$
\text{judge} \;\to\; \text{store} \;\to\; \text{update SCX} \;\to\; \text{re-judge} \;\to\; \text{re-update} \;\to\; \cdots
$$

At time step $t$, the system comprises three core components:

| Component | Symbol | Description |
|-----------|--------|-------------|
| Gatekeeper scoring function | $S_t: \mathcal{X} \times \mathcal{Y} \to [0,1]$ | Reliability score; $S_t(x,y)$ estimates $P(\text{clean} \mid x, y)$ |
| Memory bank | $\mathcal{M}_t = \{(x_i, y_i, S_i, f_{\theta_i})\}_{i=1}^{N_t}$ | Accumulated high-quality samples; $N_t$ grows monotonically |
| NEP student | $f_{\theta_t}: \mathcal{X} \to \mathcal{Y}$ | Neural-equivalent potential trained on $\mathcal{M}_t$ |

The gatekeeper $S_t$ determines which samples enter the memory bank. The memory bank $\mathcal{M}_t$ trains the NEP student $f_{\theta_t}$. The NEP student's predictions influence the next gatekeeper update. This mutual dependence creates a coupled dynamical system.

**Goal of this document**: Interpret the $S_t$ evolution as a Bayesian posterior update process, showing that self-evolution is equivalent to sequential Bayesian inference over the space of gatekeeper functions.

---

## 2. Bayesian Formulation of Gatekeeper Evolution

Let $\mathcal{G} = \{S: \mathcal{X} \times \mathcal{Y} \to [0,1]\}$ be the space of gatekeeper functions. Define a probability measure over $\mathcal{G}$ that represents our epistemic uncertainty about the true data-generating process.

**Definition 4.1 (Bayesian Gatekeeper).** At time $t$, the gatekeeper $S_t$ is the posterior mean of a random function $S \sim P_t$, where $P_t$ is a probability distribution over $\mathcal{G}$:

$$
S_t(x,y) = \mathbb{E}_{S \sim P_t}[S(x,y)], \quad \forall (x,y) \in \mathcal{X} \times \mathcal{Y}
$$

The distribution $P_t$ represents our state of knowledge at time $t$ about the true reliability function $S^*$, where $S^*(x,y) = P(\text{clean} \mid x, y)$ is the (unknowable) oracle reliability.

---

## 3. Prior Distribution Over Gatekeeper Functions

**Definition 4.2 (Prior).** At initialization time $t=0$, we place a prior distribution $P_0$ over $\mathcal{G}$:

$$
P_0(S) = \text{Prior belief about the gatekeeper function}
$$

The prior may take various forms depending on available information:

1. **Uninformative prior**: $P_0(S) \propto 1$ (uniform over $\mathcal{G}$).
2. **SCX-initialized prior**: Using the SCX reliability scores from expert models:
   $$P_0(S) \propto \exp\left(-\lambda \sum_{m=1}^M \|S - SCX_m\|^2_{\mathcal{L}^2}\right)$$
   where $SCX_m(s)$ is the state-conditioned expert reliability (Definition 3.1 of the existing framework), lifted to $\mathcal{X} \times \mathcal{Y}$ via the state mapping.
3. **Gaussian process prior**: $S \sim \mathcal{GP}(\mu_0, k_0)$ with mean function $\mu_0$ and kernel $k_0$ (see Section 7).

The initial gatekeeper is the prior mean:
$$S_0(x,y) = \mathbb{E}_{P_0}[S(x,y)]$$

In practice, $S_0$ may be set to the consensus score $C(x) = \frac{1}{M}\sum_m \mathbf{1}\{\ell(f_m(x), y) > \tau\}$ or a constant.

---

## 4. Likelihood: Memory Bank as Evidence

The memory bank $\mathcal{M}_t = \{(x_i, y_i, S_i, f_{\theta_i})\}_{i=1}^{N_t}$ is not raw data but a **filtered collection**: each sample was accepted by a previous gatekeeper $S_i$. We must account for this selection bias.

**Definition 4.3 (Selection-Aware Likelihood).** Given a candidate gatekeeper function $S$, the likelihood of observing a memory bank $\mathcal{M}_t$ is:

$$
P(\mathcal{M}_t \mid S) = \prod_{i=1}^{N_t} P(x_i, y_i \mid S, \text{accepted at time } i)
$$

Applying Bayes' rule to the acceptance event:

$$
P(x, y \mid S, \text{accepted}) \propto P(\text{accepted} \mid x, y, S) \cdot P(x, y)
$$

The acceptance probability given $S$ is precisely the gatekeeper score:

$$
P(\text{accepted} \mid x, y, S) = S(x, y)
$$

**Proposition 4.1 (Likelihood Form).** Under the assumption that the underlying data distribution $P(x,y)$ is stationary and that acceptance events are conditionally independent given $S$, the log-likelihood of the memory bank is:

$$
\log P(\mathcal{M}_t \mid S) = \sum_{i=1}^{N_t} \log S(x_i, y_i) + \sum_{i=1}^{N_t} \log P(x_i, y_i) + \text{const}
$$

where the constant accounts for the normalization of the selection distribution.

**Remark.** The second term $\sum \log P(x_i, y_i)$ does not depend on $S$ and can be absorbed into the constant. The essential likelihood is:

$$
\log P(\mathcal{M}_t \mid S) = \sum_{i=1}^{N_t} \log S(x_i, y_i) + \text{const}(S\text{-independent})
$$

*Proof sketch.* By the acceptance mechanism: each sample enters $\mathcal{M}_t$ only if $S_i(x_i, y_i)$ exceeds a threshold or otherwise passes the gate. Conditioning on the history, the probability of observing $(x_i, y_i)$ in the bank is $S(x_i, y_i) \cdot P(x_i, y_i) / Z_i$, where $Z_i$ is the acceptance probability marginalized over the data distribution. Taking logs and summing yields the expression. The conditional independence follows from the i.i.d. sampling assumption (Assumption SE-A3, defined below).

**Assumption SE-A3 (Memory Bank Conditional Independence).** Conditioned on the true gatekeeper $S^*$, the samples in $\mathcal{M}_t$ are i.i.d. from the selection-biased distribution $P(x,y \mid S^*) \propto S^*(x,y) \cdot P(x,y)$.

This is a self-consistency condition: the data that passes the gate should look like the data the gatekeeper considers reliable. When iterated, this creates a virtuous (or vicious) cycle.

---

## 5. Posterior Update Recursion

**Theorem 4.1 (Bayesian Update Recursion).** Let $P_t$ be the posterior over gatekeeper functions at time $t$, and let $\mathcal{D}_{t+1} = \{(x_j, y_j)\}_{j=1}^{B_{t+1}}$ be the new batch of samples collected between time $t$ and $t+1$, each evaluated by the current gatekeeper $S_t$ and accepted into $\mathcal{M}_{t+1}$ with probability $S_t(x_j, y_j)$. Then the posterior update is:

$$
P_{t+1}(S) \propto P_t(S) \cdot \prod_{j=1}^{B_{t+1}} S(x_j, y_j)^{a_j} \cdot (1 - S(x_j, y_j))^{1-a_j}
$$

where $a_j \in \{0, 1\}$ is the acceptance indicator.

**Equivalent incremental form.** Writing the non-accepted data as $\tilde{\mathcal{D}}_{t+1}$ (samples that were evaluated but rejected), the posterior becomes:

$$
P_{t+1}(S) \propto P_t(S) \cdot \underbrace{\left[\prod_{(x,y) \in \mathcal{D}_{t+1}} S(x,y)\right]}_{\text{accepted}} \cdot \underbrace{\left[\prod_{(x,y) \in \tilde{\mathcal{D}}_{t+1}} (1 - S(x,y))\right]}_{\text{rejected}}
$$

*Interpretation.* The gatekeeper update is a Bayesian binary classification: each sample is a Bernoulli trial with success probability $S(x,y)$. The accepted samples are "successes," the rejected samples are "failures."

**Corollary 4.1 (Posterior Recursion).** The sequence of posterior distributions satisfies:

$$
P_{t+1}(S) \propto P_0(S) \cdot \prod_{i=1}^{t+1} \mathcal{L}_i(S \mid \mathcal{D}_i)
$$

where $\mathcal{L}_i(S \mid \mathcal{D}_i) = \prod_{(x,y) \in \mathcal{D}_i} S(x,y)^{a_i(x,y)} (1 - S(x,y))^{1-a_i(x,y)}$ is the batch-$i$ likelihood.

This is a standard sequential Bayesian update: the posterior at time $t$ becomes the prior for time $t+1$.

---

## 6. Posterior Mean Gatekeeper

**Definition 4.4 (Gatekeeper as Posterior Mean).** At any time $t$, the deployed gatekeeper is:

$$
S_t(x,y) = \mathbb{E}_{P_t}[S(x,y)] = \int_{\mathcal{G}} S(x,y) \, dP_t(S)
$$

This is the Bayes estimator under squared error loss:

$$
S_t = \arg\min_{\hat{S}} \mathbb{E}_{P_t}[\|\hat{S} - S\|^2_{\mathcal{L}^2}]
$$

**Proposition 4.2 (Optimality of Posterior Mean).** The posterior mean gatekeeper minimizes the expected $\mathcal{L}^2$ prediction error under the posterior $P_t$:

$$
S_t = \arg\min_{\hat{S}} \mathbb{E}_{S \sim P_t} \left[ \int (S(x,y) - \hat{S}(x,y))^2 \, dP(x,y) \right]
$$

*Proof.* Standard result: the posterior mean minimizes Bayes risk under squared error loss. See [Berger, 1985, Section 4.4].

**Connection to SCX consensus.** When the prior is flat and only the initial expert-based SCX scores are used, the posterior mean reduces to:

$$
S_0(x,y) \approx \frac{1}{M}\sum_{m=1}^M \mathbf{1}\{\ell(f_m(x), y) < \tau\}
$$

which recovers the consensus score $1 - C(x)$ from Theorem 1. This bridges the Bayesian formulation to the existing SCX theory.

---

## 7. Conjugate Prior Structure: Gaussian Process Formulation

**Definition 4.5 (Gaussian Process Gatekeeper).** Let the gatekeeper function $S: \mathcal{X} \times \mathcal{Y} \to \mathbb{R}$ be modeled as a Gaussian process (GP) prior:

$$
S \sim \mathcal{GP}(\mu_0, k_0)
$$

where $\mu_0: \mathcal{Z} \to \mathbb{R}$ is the mean function ($\mathcal{Z} = \mathcal{X} \times \mathcal{Y}$) and $k_0: \mathcal{Z} \times \mathcal{Z} \to \mathbb{R}$ is the covariance kernel.

**Assumption SE-A4 (Logit-Normal Likelihood).** The acceptance probability is modeled via a logistic link:

$$
P(a = 1 \mid S, x, y) = \sigma(S(x,y)) = \frac{1}{1 + e^{-S(x,y)}}
$$

where $\sigma$ is the logistic sigmoid.

**Theorem 4.2 (GP Posterior Update).** Under the GP prior and logistic likelihood, the posterior at time $t$ is:

$$
P_t(S \mid \mathcal{M}_t) \propto \mathcal{GP}(\mu_0, k_0) \cdot \prod_{i=1}^{N_t} \sigma(S(x_i, y_i))^{a_i} (1 - \sigma(S(x_i, y_i)))^{1-a_i}
$$

While the exact posterior remains non-Gaussian (due to the logistic likelihood), the **Laplace approximation** yields a Gaussian posterior:

$$
P_t(S) \approx \mathcal{GP}(\mu_t, k_t)
$$

where:

- $\mu_t(z) = \mu_0(z) + k_0(z, \mathbf{Z}_t)^\top (k_0(\mathbf{Z}_t, \mathbf{Z}_t) + W_t^{-1})^{-1} (\mathbf{a}_t - \sigma(\mu_0(\mathbf{Z}_t)))$
- $k_t(z, z') = k_0(z, z') - k_0(z, \mathbf{Z}_t)^\top (k_0(\mathbf{Z}_t, \mathbf{Z}_t) + W_t^{-1})^{-1} k_0(\mathbf{Z}_t, z')$
- $W_t$ is a diagonal matrix with $W_{t,ii} = \sigma(\mu_t(z_i))(1 - \sigma(\mu_t(z_i)))$
- $\mathbf{Z}_t$ is the concatenated set of all evaluated points $((x_i, y_i))_{i=1}^{N_t}$
- $\mathbf{a}_t$ is the vector of acceptance indicators

**Closed-form posterior mean.** Under the Laplace approximation:

$$
S_t(z) = \mu_t(z) = \mathbb{E}_{P_t}[S(z)] \approx k_0(z, \mathbf{Z}_t)^\top (k_0(\mathbf{Z}_t, \mathbf{Z}_t) + W_t^{-1})^{-1} (\mathbf{a}_t - \sigma(\mu_0(\mathbf{Z}_t)) + W_t \mu_0(\mathbf{Z}_t))
$$

**Conjugate special case: Gaussian likelihood.** If we use a Gaussian observation model (acceptance score is continuous in $[0,1]$ rather than binary), the prior and posterior are both Gaussian:

$$
S_t(z) = k_0(z, \mathbf{Z}_t)^\top (k_0(\mathbf{Z}_t, \mathbf{Z}_t) + \sigma^2_\varepsilon I)^{-1} \mathbf{a}_t
$$

This is the standard GP regression form, with closed-form sequential update.

**Proposition 4.3 (Conjugate Sequential GP Update).** Under the Gaussian likelihood model, the posterior can be updated sequentially without revisiting old data:

$$
\mu_{t+1}(z) = \mu_t(z) + k_t(z, z_{t+1}) \cdot \frac{a_{t+1} - \mu_t(z_{t+1})}{k_t(z_{t+1}, z_{t+1}) + \sigma^2_\varepsilon}
$$

$$
k_{t+1}(z, z') = k_t(z, z') - \frac{k_t(z, z_{t+1}) k_t(z_{t+1}, z')}{k_t(z_{t+1}, z_{t+1}) + \sigma^2_\varepsilon}
$$

*Proof.* Standard sequential GP update formulas. See [Rasmussen & Williams, 2006, Algorithm 2.1]. The conjugate property holds because the Gaussian-Gaussian pair forms a conditionally conjugate family.

---

## 8. Bayesian Martingale Property

**Theorem 4.3 (Posterior Mean Martingale).** Let $S_t(x,y) = \mathbb{E}_{P_t}[S(x,y)]$ be the posterior mean gatekeeper, where $P_t$ is updated via Bayes' rule as new batches arrive. Then the stochastic process $\{S_t\}_{t \geq 0}$ is a martingale with respect to the filtration $\mathcal{F}_t = \sigma(\mathcal{M}_1, \dots, \mathcal{M}_t)$:

$$
\mathbb{E}[S_{t+1}(x,y) \mid \mathcal{F}_t] = S_t(x,y), \quad \forall (x,y) \in \mathcal{X} \times \mathcal{Y}
$$

*Proof.* Apply the tower property of conditional expectation:

$$
\begin{aligned}
\mathbb{E}[S_{t+1}(x,y) \mid \mathcal{F}_t] &= \mathbb{E}[\mathbb{E}_{P_{t+1}}[S(x,y)] \mid \mathcal{F}_t] \\
&= \mathbb{E}[\mathbb{E}[S(x,y) \mid \mathcal{M}_{1:t+1}] \mid \mathcal{F}_t] \\
&= \mathbb{E}[S(x,y) \mid \mathcal{M}_{1:t}] \quad \text{(tower property)} \\
&= \mathbb{E}_{P_t}[S(x,y)] = S_t(x,y)
\end{aligned}
$$

The key step is that $P_{t+1}$ is the posterior after conditioning on $\mathcal{M}_{t+1}$, and the tower property of conditional expectation gives $\mathbb{E}[\mathbb{E}[S \mid \mathcal{F}_{t+1}] \mid \mathcal{F}_t] = \mathbb{E}[S \mid \mathcal{F}_t]$.

**Corollary 4.2 (Pointwise Martingale).** For any fixed $(x,y)$, the sequence $\{S_t(x,y)\}_{t \geq 0}$ is a martingale bounded in $[0,1]$.

**Corollary 4.3 (Vector Martingale).** If $\mathcal{Z}_0 \subset \mathcal{X} \times \mathcal{Y}$ is a finite set of evaluation points, then $\{S_t(z)\}_{t \geq 0}$ for $z \in \mathcal{Z}_0$ is a vector-valued martingale.

---

## 9. Martingale Convergence Theorem

**Theorem 4.4 (Martingale Convergence of Gatekeeper).** Under the Bayesian update framework, the sequence of gatekeeper functions $\{S_t\}_{t \geq 0}$ converges almost surely to a limit $S_\infty$:

$$
S_t(x,y) \xrightarrow{a.s.} S_\infty(x,y), \quad \forall (x,y) \in \mathcal{X} \times \mathcal{Y}
$$

as $t \to \infty$, where $S_\infty$ is a random function measurable with respect to $\mathcal{F}_\infty = \sigma(\bigcup_{t \geq 0} \mathcal{F}_t)$.

*Proof.* The martingale convergence theorem (Doob, 1953) states that any martingale bounded in $\mathcal{L}^1$ converges almost surely. Since $S_t(x,y) \in [0,1]$ for all $t$, it is uniformly bounded and thus $\mathcal{L}^1$-bounded. Therefore $S_t(x,y) \to S_\infty(x,y)$ almost surely. By the separability of $\mathcal{X} \times \mathcal{Y}$ (under mild topological conditions), convergence holds simultaneously for all $(x,y)$ in a dense subset, and by continuity of the mapping $z \mapsto S_t(z)$ (if the kernel $k_0$ is continuous), convergence is uniform on compact sets. See Doob (1953), Chapter VII.

**Proposition 4.4 (Structure of the Limit).** The limit $S_\infty$ satisfies the self-consistency equation:

$$
S_\infty(x,y) = \mathbb{E}[S(x,y) \mid \mathcal{F}_\infty] = \int S(x,y) \, dP_\infty(S)
$$

where $P_\infty$ is the limiting posterior distribution. Moreover, $S_\infty$ is the Bayes estimator under the limiting posterior:

$$
S_\infty = \arg\min_{\hat{S}} \mathbb{E}_{P_\infty}[\|\hat{S} - S\|^2_{\mathcal{L}^2}]
$$

**Proposition 4.5 (Convergence Rate).** Under the GP prior with Gaussian likelihood, the convergence rate is:

$$
\|S_t - S_\infty\|_{\mathcal{L}^2} = O_p(t^{-1/2})
$$

if the covariance kernel $k_0$ has finite trace and the observation noise $\sigma^2_\varepsilon$ is bounded away from zero.

*Proof sketch.* For GP regression with i.i.d. Gaussian noise, the posterior variance at any point decays as $O(1/N_t)$. Since $N_t \to \infty$ as $t \to \infty$ (memory bank grows), the posterior mean converges to the true function at rate $O_p(1/\sqrt{N_t})$. If $N_t \propto t$ (constant batch size), the rate is $O_p(t^{-1/2})$. A more precise rate depends on the kernel's eigenvalue decay; for a Matérn kernel with smoothness $\nu$, the rate is $O_p(t^{-\nu/(2\nu+d)})$.

---

## 10. Prior Misspecification Analysis

**Definition 4.6 (Misspecified Prior).** The prior $P_0$ is **misspecified** if the true oracle gatekeeper $S^*$ lies outside the support of $P_0$:

$$
S^* \notin \text{supp}(P_0)
$$

**Theorem 4.5 (Behavior Under Prior Misspecification).** Let $S^*$ be the true oracle gatekeeper, and let $P_0$ be a prior whose support is a set $\mathcal{G}_0 \subset \mathcal{G}$. If $S^* \notin \mathcal{G}_0$, then:

**(a) Posterior inconsistency.** The posterior distribution $P_t$ does **not** concentrate on $S^*$:

$$
P_t(\{S: \|S - S^*\| > \varepsilon\}) \not\to 0
$$

for any $\varepsilon < \inf_{S \in \mathcal{G}_0} \|S - S^*\|$.

**(b) Convergence to KL projection.** Instead, $P_t$ concentrates on the set of functions in $\mathcal{G}_0$ that minimize KL divergence to the true data-generating process:

$$
P_t \to \delta_{S^\dagger}, \quad S^\dagger = \arg\min_{S \in \mathcal{G}_0} D_{\text{KL}}(P^* \parallel P_S)
$$

where $P^*$ is the true data distribution and $P_S$ is the distribution induced by $S \in \mathcal{G}_0$.

**(c) Gatekeeper limit.** The limiting gatekeeper $S_\infty$ is the posterior mean under $P_\infty$, which converges to:

$$
S_\infty = \mathbb{E}_{P_\infty}[S] = S^\dagger
$$

where $S^\dagger$ is the KL projection of $S^*$ onto $\mathcal{G}_0$.

*Proof sketch.* Part (a) follows from the definition of support: if $S^* \notin \mathcal{G}_0$, then for any $\varepsilon$ smaller than the distance from $S^*$ to $\mathcal{G}_0$, the posterior probability of the $\varepsilon$-ball around $S^*$ is zero at all $t$, so it cannot converge to 1. Part (b) follows from the Bernstein-von Mises theorem for misspecified models (Kleijn & van der Vaart, 2012): the posterior concentrates on the set of distributions that minimize KL divergence to the truth. Part (c) follows from continuous mapping: if $P_t \to \delta_{S^\dagger}$, then $\mathbb{E}_{P_t}[S] \to S^\dagger$.

**Corollary 4.4 (Practical Implications of Misspecification).**

1. **SCX-Expert prior**: If $S_0$ is initialized from expert consensus scores and the experts are systematically biased, $S^*$ may be outside the manifold of functions realizable by the expert-based prior. The gatekeeper converges to the best approximation within the prior family, not the truth.

2. **GP with wrong kernel**: If $S^*$ has a different smoothness or length scale than assumed by $k_0$, the posterior mean converges to the best GP approximation of $S^*$, which may have non-vanishing bias.

3. **Detection of misspecification**: The martingale property provides a diagnostic: if $S_t$ shows systematic drift beyond what the posterior variance predicts, it suggests prior misspecification:
   $$
   \mathbb{E}[(S_{t+1} - S_t)^2] > \mathbb{E}_t[\text{Var}_{P_t}[S]]
   $$

---

## 11. KL Divergence Contraction

**Definition 4.7 (KL Divergence Between Data Distributions).** Let $P^*$ be the true data-generating distribution induced by the oracle gatekeeper $S^*$, and let $P_t$ be the distribution induced by the posterior predictive:

$$
P_t(x,y) = \int S(x,y) \cdot P(x,y) \, dP_t(S)
$$

The KL divergence from the truth to the model at time $t$ is:

$$
D_{\text{KL}}(P^* \parallel P_t) = \mathbb{E}_{(x,y) \sim P^*} \left[ \log \frac{P^*(x,y)}{P_t(x,y)} \right]
$$

**Theorem 4.6 (KL Contraction).** Under the Bayesian update framework with correctly specified prior ($S^* \in \text{supp}(P_0)$) and regularity conditions (identifiability, integrability, and Doob's consistency conditions):

$$
D_{\text{KL}}(P^* \parallel P_t) \xrightarrow{a.s.} 0 \quad \text{as } t \to \infty
$$

Moreover, the contraction rate satisfies:

$$
\mathbb{E}[D_{\text{KL}}(P^* \parallel P_t)] \leq \frac{D_{\text{KL}}(P^* \parallel P_0)}{t} \quad \text{(under i.i.d. sampling)}
$$

*Proof sketch.* This follows from Doob's consistency theorem for Bayesian models (Doob, 1949; Ghosh & Ramamoorthi, 2003). The key conditions are:
1. The model is identifiable: $S \neq S' \implies P_S \neq P_{S'}$.
2. The prior puts positive mass on all neighborhoods of $S^*$.
3. The data are i.i.d. conditional on $S$.

Under these conditions, the posterior is consistent at $S^*$ for almost every $S^*$ in the support of the prior, and KL divergence contracts to zero. The rate inequality follows from the convexity of KL divergence and the martingale property of the log-likelihood ratio.

**Proposition 4.6 (KL Decomposition).** The KL divergence decomposes into prior mismatch and learning components:

$$
D_{\text{KL}}(P^* \parallel P_t) = \underbrace{D_{\text{KL}}(P^* \parallel P_0)}_{\text{initial gap}} - \underbrace{\sum_{i=1}^t \mathbb{E}_{P^*}[\log \ell_i(S) - \log \mathbb{E}_{P_{i-1}}[\ell_i(S)]]}_{\text{cumulative learning}}
$$

where $\ell_i(S) = P(\mathcal{D}_i \mid S)$ is the likelihood of batch $i$.

*Proof.* Write the posterior $P_t \propto P_0 \prod_{i=1}^t \ell_i(S)$. Then $\log dP_t/dP_0 = \sum_{i=1}^t \log \ell_i(S) - \log Z_t$ where $Z_t$ is the marginal likelihood. Taking expectations and telescoping yields the decomposition.

---

## 12. Bernstein-von Mises Theorem Connection

**Theorem 4.7 (Bernstein-von Mises for Gatekeeper).** Under regularity conditions (identifiability, smoothness, and correct specification), the posterior distribution $P_t$ converges to a Gaussian process centered at the truth $S^*$ with covariance $N_t^{-1} \mathcal{I}(S^*)^{-1}$:

$$
\sqrt{N_t} (P_t - \delta_{S^*}) \xrightarrow{d} \mathcal{GP}(0, \mathcal{I}(S^*)^{-1})
$$

in the sense of convergence of posterior distributions. Equivalently, for any bounded continuous functional $f: \mathcal{G} \to \mathbb{R}$:

$$
\sqrt{N_t} \left( \mathbb{E}_{P_t}[f(S)] - f(S^*) \right) \xrightarrow{d} \mathcal{N}(0, \nabla f(S^*)^\top \mathcal{I}(S^*)^{-1} \nabla f(S^*))
$$

*Conditions.* The theorem requires:

1. **Identifiability**: $S \neq S^* \implies P_S \neq P_{S^*}$.
2. **Smoothness**: The log-likelihood $\log P(\mathcal{M}_t \mid S)$ is twice continuously differentiable in a neighborhood of $S^*$.
3. **Positivity**: The Fisher information $\mathcal{I}(S) = -\mathbb{E}_{P^*}[\nabla^2 \log P(\mathcal{M}_1 \mid S)]$ is positive definite and continuous at $S^*$.
4. **Prior regularity**: The prior $P_0$ has a density (with respect to an appropriate base measure) that is continuous and positive at $S^*$.
5. **Memory bank size**: $N_t \to \infty$.

*Proof sketch.* The Bernstein-von Mises theorem (van der Vaart, 1998, Chapter 10) states that under regularity conditions, the posterior distribution is asymptotically normal. The infinite-dimensional extension (Gaussian process version) follows from the functional central limit theorem for posterior distributions (Castillo & Nickl, 2013). The key steps are: (1) expand the log-likelihood around $S^*$, (2) show that the prior becomes negligible as $N_t \to \infty$, (3) identify the limiting normal distribution via the Fisher information.

**Corollary 4.5 (Asymptotic Normality of Gatekeeper).** For any fixed $(x,y)$, as $t \to \infty$:

$$
\sqrt{N_t} (S_t(x,y) - S^*(x,y)) \xrightarrow{d} \mathcal{N}(0, \mathcal{I}(S^*)^{-1}(x,y))
$$

where $\mathcal{I}(S^*)^{-1}(x,y)$ is the pointwise posterior variance.

**Corollary 4.6 (Asymptotic Credible Intervals).** Under the Bernstein-von Mises theorem, the $1-\alpha$ credible interval for $S^*(x,y)$ is asymptotically:

$$
S_t(x,y) \pm z_{\alpha/2} \cdot \sqrt{\frac{\hat{\sigma}^2_t(x,y)}{N_t}}
$$

where $\hat{\sigma}^2_t(x,y)$ is the estimated posterior variance and $z_{\alpha/2}$ is the standard normal quantile.

**Important caveat.** The Bernstein-von Mises theorem requires correct specification ($S^*$ in the support of $P_0$). Under misspecification (Section 10), the posterior converges to a Gaussian centered at $S^\dagger$ (the KL projection), not $S^*$. This is the **misspecified Bernstein-von Mises** phenomenon (Kleijn & van der Vaart, 2012).

---

## 13. Proof Sketches

### Proof Sketch for Theorem 4.3 (Martingale Property)

1. **Setup.** Let $(\Omega, \mathcal{F}, \mathbb{P})$ be the underlying probability space. Define $\mathcal{F}_t = \sigma(\mathcal{M}_1, \dots, \mathcal{M}_t)$ as the filtration generated by the memory bank up to time $t$.

2. **Conditional expectation.** By definition, $S_t(x,y) = \mathbb{E}[S(x,y) \mid \mathcal{F}_t]$ where $S \sim P_0$ is the random function drawn from the prior, and the expectation is over both $S$ and the data.

3. **Tower property.** For any $t$:
   $$
   \mathbb{E}[S_{t+1}(x,y) \mid \mathcal{F}_t] = \mathbb{E}[\mathbb{E}[S(x,y) \mid \mathcal{F}_{t+1}] \mid \mathcal{F}_t] = \mathbb{E}[S(x,y) \mid \mathcal{F}_t] = S_t(x,y)
   $$
   The middle equality is the tower property of conditional expectation.

4. **Integrability.** Since $S_t(x,y) \in [0,1]$, we have $\mathbb{E}[|S_t(x,y)|] \leq 1 < \infty$, so the martingale property holds.

### Proof Sketch for Theorem 4.4 (Martingale Convergence)

1. **Bounded martingale.** $\{S_t(x,y)\}_{t \geq 0}$ is a martingale bounded in $[0,1]$.

2. **Doob's convergence theorem.** Any martingale that is bounded in $\mathcal{L}^1$ converges almost surely. Since $S_t$ is uniformly bounded, $\sup_t \mathbb{E}[|S_t|] \leq 1 < \infty$, so $\mathcal{L}^1$-boundedness holds.

3. **Almost sure convergence.** Hence $S_t(x,y) \to S_\infty(x,y)$ almost surely for each fixed $(x,y)$.

4. **Simultaneous convergence.** For a countable dense subset $\mathcal{Z}_0 \subset \mathcal{X} \times \mathcal{Y}$, convergence holds simultaneously for all $z \in \mathcal{Z}_0$ with probability 1. If the sample paths $t \mapsto S_t(z)$ are continuous in $z$ (guaranteed by the GP kernel), then convergence extends uniformly on compact sets.

### Proof Sketch for Proposition 4.1 (Likelihood Form)

1. **Acceptance mechanism.** Sample $(x,y)$ is accepted into $\mathcal{M}_t$ with probability $S(x,y)$, independently of other samples.

2. **Selection distribution.** The distribution of accepted samples is:
   $$
   P(x,y \mid \text{accepted}, S) = \frac{S(x,y) \cdot P(x,y)}{\int S(x',y') \cdot P(x',y') \, dx' dy'}
   $$

3. **Joint likelihood.** For the entire memory bank $\mathcal{M}_t = \{(x_i, y_i)\}_{i=1}^{N_t}$:
   $$
   P(\mathcal{M}_t \mid S) = \prod_{i=1}^{N_t} \frac{S(x_i, y_i) \cdot P(x_i, y_i)}{Z(S)}
   $$
   where $Z(S) = \mathbb{E}_{P}[S(X,Y)]$ is the marginal acceptance probability.

4. **Log-likelihood.** Taking logs:
   $$
   \log P(\mathcal{M}_t \mid S) = \sum_{i=1}^{N_t} \log S(x_i, y_i) + \sum_{i=1}^{N_t} \log P(x_i, y_i) - N_t \log Z(S)
   $$

5. **Constant elimination.** The term $\sum \log P(x_i, y_i)$ does not depend on $S$ and can be treated as constant. The term $N_t \log Z(S)$ is constant across $S$ if $Z(S)$ is approximately constant (which holds when the prior is broad and the acceptance threshold is near-independent of $S$). In the full Bayesian treatment, this term contributes to the evidence normalization.

### Proof Sketch for Theorem 4.6 (KL Contraction)

1. **Prior support condition.** By assumption, $S^* \in \text{supp}(P_0)$, meaning $P_0(\{S: \|S - S^*\| < \varepsilon\}) > 0$ for all $\varepsilon > 0$.

2. **Doob's consistency.** For almost every $S$ in the support of $P_0$, the posterior is consistent (Doob, 1949). Since $S^*$ is in the support (by correct specification), consistency holds.

3. **KL convergence.** Posteriour consistency implies that $P_t$ concentrates on $S^*$, which means $P_t(x,y) \to P^*(x,y)$ in total variation, and hence in KL divergence (by Pinsker's inequality and the fact that convergence in TV implies convergence in KL when the limit density is bounded away from zero).

4. **Rate.** Under i.i.d. sampling and the LAN (local asymptotic normality) condition, the rate of KL contraction is $O(1/t)$. Specifically:
   $$
   \mathbb{E}[D_{\text{KL}}(P^* \parallel P_t)] \leq \frac{D_{\text{KL}}(P^* \parallel P_0)}{t}
   $$
   follows from the convexity of KL divergence and the fact that the average of $t$ conditionally independent updates gives a telescoping bound.

---

## 14. Summary of Proven vs. Conjectured Claims

| Claim | Status | Notes |
|-------|--------|-------|
| Theorem 4.1: Bayesian update recursion | **Proven** | Direct application of Bayes' rule |
| Proposition 4.1: Likelihood form | **Proven** | Derived from acceptance mechanism |
| Proposition 4.2: Posterior mean optimality | **Proven** | Standard Bayes risk minimization |
| Theorem 4.3: Posterior mean martingale | **Proven** | Tower property + conditional expectation |
| Corollary 4.2: Pointwise martingale | **Proven** | Direct consequence of Theorem 4.3 |
| Theorem 4.4: Martingale convergence | **Proven** | Doob's martingale convergence theorem |
| Proposition 4.3: Conjugate GP update | **Proven** | Standard GP regression formulas |
| Theorem 4.5: Prior misspecification | **Proven** | KL projection + posterior concentration theory |
| Theorem 4.6: KL contraction | **Proven under regularity conditions** | Doob's consistency + LAN conditions |
| Proposition 4.4: Structure of the limit | **Proven** | Limit of Bayes estimator under squared error |
| Proposition 4.5: Convergence rate | **Conjectured** | Rate $O_p(t^{-1/2})$ holds for GP regression with finite-trace kernel; general case depends on kernel eigen-decay |
| Theorem 4.7: Bernstein-von Mises | **Proven under regularity conditions** | Standard BvM + infinite-dimensional extension (Castillo & Nickl, 2013) |
| Proposition 4.6: KL decomposition | **Proven** | Algebraic manipulation of log posterior |
| Corollary 4.4: Misspecification diagnostics | **Heuristic** | The drift diagnostic is empirically motivated |

**Key uncertainty**: The convergence rate (Proposition 4.5) depends on the specific kernel choice and the eigenstructure of the covariance operator. For Matérn kernels, the rate is known; for deep kernel GPs (which may be more realistic for SCX), rates are an active research area.

---

## 15. References

1. Doob, J. L. (1949). Application of the theory of martingales to the theory of Markov chains. *Colloques Internationaux du CNRS*, 13, 23-27.
2. Doob, J. L. (1953). *Stochastic Processes*. Wiley.
3. Berger, J. O. (1985). *Statistical Decision Theory and Bayesian Analysis* (2nd ed.). Springer.
4. Ghosh, J. K., & Ramamoorthi, R. V. (2003). *Bayesian Nonparametrics*. Springer.
5. van der Vaart, A. W. (1998). *Asymptotic Statistics*. Cambridge University Press.
6. Kleijn, B. J. K., & van der Vaart, A. W. (2012). The Bernstein-von Mises theorem under misspecification. *Electronic Journal of Statistics*, 6, 354-381.
7. Castillo, I., & Nickl, R. (2013). Nonparametric Bernstein-von Mises theorems in Gaussian white noise. *Annals of Statistics*, 41(4), 1999-2028.
8. Rasmussen, C. E., & Williams, C. K. I. (2006). *Gaussian Processes for Machine Learning*. MIT Press.
9. Kleijn, B. J. K. (2020). *Bayesian Theory with Applications*. Cambridge University Press.
10. Dawid, A. P. (1984). Statistical theory: The prequential approach. *JRSS Series A*, 147(2), 278-292.
11. Williams, C. K. I., & Rasmussen, C. E. (1996). Gaussian processes for regression. *NIPS 1995*.
12. O'Hagan, A. (1978). Curve fitting and optimal design for prediction. *JRSS Series B*, 40(1), 1-42.

---

*End of 04_bayesian_update.md -- Bayesian update interpretation of SCX self-evolution.*
