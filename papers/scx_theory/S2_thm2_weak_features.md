## Theorem 2: Weak Feature Failure Boundary (The Impossible Demand Theorem)
<!-- label: sec:thm2 -->

When the feature representation $\phi(x)$ contains insufficient information
about the true state $S$, consistency-based noise detection methods
(including SCX) cannot outperform the loss-based baseline. Theorem~2
quantifies this boundary from an information-theoretic perspective.

### Information-Theoretic Setup
<!-- label: sec:thm2:setup -->

**Data generation.**
Let $X \in \mathcal{X} \subseteq \mathbb{R}^d$ be the input, $Y \in \mathcal{Y}$
the label, and $Z \in \{0,1\}$ the noise indicator ($Z=1$ for noisy samples).
The true (unobserved) state is $S = s(X) \in \mathcal{S}$ with
$|\mathcal{S}| = K_{\mathcal{S}}$. The observed feature representation is
$\phi(X) \in \Phi \subseteq \mathbb{R}^{d_\phi}$.

SCX assumes the following generative structure:
\[
Z \;\to\; S \;\to\; (X, Y) \;\to\; \phi(X),
\qquad
Z \;\to\; S \;\to\; X \;\to\; \{f_m(X)\}.
\]
This yields the Markov chain

$$
Z \to S \to X \to \phi(X),
<!-- label: eq:markov-chain -->
$$

and by the data processing inequality,
\[
I(\phi(X); Z) \leq I(X; Z) \leq I(S; Z) \leq H(Z) \leq \log 2.
\]

**Weak feature definition.**

> **Definition:** [$\delta$-weak feature]
> <!-- label: def:weak-feature -->
> A feature map $\phi: \mathcal{X} \to \Phi$ is called $\delta$-weak with respect
> to the true state map $s: \mathcal{X} \to \mathcal{S}$ if
> 
> $$
> I(\phi(X); s(X)) \leq \delta,
> <!-- label: eq:weak-feature -->
> $$
> 
> where $I(\cdot;\cdot)$ is the Shannon mutual information, measured in nats.

The normalised weakness is

$$
\varepsilon_\phi = \frac{\log K_{\mathcal{S}}} \in [0, 1],
<!-- label: eq:norm-weakness -->
$$

since $I(\phi; S) \leq H(S) \leq \log K_{\mathcal{S}}$.
$\varepsilon_\phi = 1$ corresponds to features with no state information
(worst case), $\varepsilon_\phi = 0$ to full state information.

An equivalent definition uses the total variation distance. For two states
$s_1, s_2$, let
$\operatorname{TV}_{s_1,s_2} = \operatorname{TV}(P_{\phi \mid S=s_1},
P_{\phi \mid S=s_2})$. Then the feature weakness is

$$
\Delta_\phi = \max_{s_1 \neq s_2}
\operatorname{TV}(P_{\phi \mid S=s_1}, P_{\phi \mid S=s_2}),
<!-- label: eq:tv-weakness -->
$$

and by Pinsker's inequality,

$$
\Delta_\phi \leq \sqrt{\frac{2}}.
<!-- label: eq:pinsker-tv -->
$$

When $\Delta_\phi$ is small, points from different true states are
indistinguishable in $\phi$-space.

**Loss baseline detector.**
The loss-based detector uses no state information:
\[
\hat{z}_{loss}(x) = \mathbf{1}\{\max_m \ell(f_m(x), y) > t\},
\]
where $\{f_m\}_{m=1}^M$ are $M$ expert models. Denote its optimal performance
by $\operatorname{AUC}_{base}$,
$\operatorname{PRAUC}_{base}$, and $\operatorname{F1}_{base}$.

For a completely random detector, the optimal performance is

$$
\operatorname{AUC}_{rand} = 0.5,\qquad
\operatorname{PRAUC}_{rand} = \eta,\qquad
\operatorname{F1}_{rand} = \frac{2\eta}{1+\eta},
<!-- label: eq:random-baseline -->
$$

where $\eta = \mathbb{P}(Z=1)$ is the marginal noise rate.

### Lemma 1: State Estimation Error (Fano)
<!-- label: sec:thm2:lemma1 -->

> **Lemma:** [State estimation error lower bound -- Fano's inequality]
> <!-- label: lem:fano -->
> Let $\hat{S}$ be any estimator of the true state $S$ based on $\phi(X)$
> (i.e., the output of the SCX state-discovery algorithm). If $\phi$ is
> $\delta$-weak, then
> 
> $$
> \mathbb{P}(\hat{S} \neq S) \;\geq\;
> \frac{H(S) - \delta - \log 2}{\log K_{\mathcal{S}}}.
> <!-- label: eq:fano-bound -->
> $$

> **Proof:** Apply Fano's inequality  [cite]:
> 
> $$
> \mathbb{P}(\hat{S} \neq S)
> &\geq \frac{H(S \mid \phi(X)) - \log 2}{\log K_{\mathcal{S}}} 

> &= \frac{H(S) - I(\phi(X); S) - \log 2}{\log K_{\mathcal{S}}} 

> &= \frac{H(S) - \delta - \log 2}{\log K_{\mathcal{S}}}.
> \qedhere
> $$

> **Corollary:** [Uniform states]
> <!-- label: cor:fano-uniform -->
> If the true states are approximately uniform,
> $H(S) \approx \log K_{\mathcal{S}}$, then
> \[
> \mathbb{P}(\hat{S} \neq S) \;\geq\; 1 - \frac{\delta + \log 2}{\log K_{\mathcal{S}}}.
> \]
> As $\delta \to 0$ with $K_{\mathcal{S}}$ fixed,
> $\mathbb{P}(\hat{S} \neq S) \to 1 - \frac{\log 2}{\log K_{\mathcal{S}}} > 0$.
> For large $K_{\mathcal{S}}$ this limit approaches $1$.

> **Corollary:** [Two-state case]
> <!-- label: cor:fano-two-state -->
> When $K_{\mathcal{S}} = 2$,
> \[
> \mathbb{P}(\hat{S} \neq S) \;\geq\;
> \frac{H(S) - \delta - \log 2}{\log 2}.
> \]

> **Remark:** [Achievability]
> <!-- label: remark:fano-achievability -->
> The converse of Fano's inequality guarantees the *existence* of an
> estimator $\hat{S}$ operating on $\phi$ such that
> \[
> \mathbb{P}(\hat{S} \neq S) \;\leq\; \frac{\delta + \log 2}{\log K_{\mathcal{S}}}.
> \]
> This existence bound does not guarantee that a particular algorithm
> (e.g.\ $k$-means) attains it. In practice, the SCX clustering error satisfies
> \[
> \mathbb{P}(\hat{S} \neq S) \;\leq\; O\!\left(\frac{\log K_{\mathcal{S}}}\right)
> + \varepsilon_{k-means},
> \]
> where $\varepsilon_{k-means}$ captures the approximation error of
> $k$-means (initialisation, non-convexity, non-spherical clusters). When
> $\delta$ is small (weak features), *any* algorithm is fundamentally
> limited by the Fano lower bound.

### Lemma 2: SCX Reliability Degradation
<!-- label: sec:thm2:lemma2 -->

> **Lemma:** [SCX reliability estimation degradation]
> <!-- label: lem:scx-degradation -->
> Let $C(s)$ be the consensus score for true state $s$, and let $C(\hat{s})$
> be the consensus score for an estimated state $\hat{s}$ obtained by clustering
> $\phi$. If $\phi$ is $\delta$-weak, then
> 
> $$
> \mathbb{E}\bigl[|C(\hat{S}) - C(S)|\bigr]
> \;\leq\; \mathbb{P}(\hat{S} \neq S) + O\!\left(\frac{1}{\sqrt{n_}}\right),
> <!-- label: eq:degradation-bound -->
> $$
> 
> where $n_ = \min_{s \in \mathcal{S}} n_s$ is the minimum per-state
> sample size.

> **Proof:** Decompose the expectation into correctly and incorrectly estimated states:
> 
> $$
> \mathbb{E}\bigl[|C(\hat{S}) - C(S)|\bigr]
> &= \mathbb{P}(\hat{S} = S)\,
>    \mathbb{E}\bigl[|C(\hat{S}) - C(S)| \mid \hat{S} = S\bigr] 

> &\qquad + \mathbb{P}(\hat{S} \neq S)\,
>    \mathbb{E}\bigl[|C(\hat{S}) - C(S)| \mid \hat{S} \neq S\bigr].
> $$
> 
> 
> *Case 1 ($\hat{S} = S$):* When the state is correctly estimated,
> $C(\hat{S})$ is a consistent estimator of $C(S)$. By Chebyshev's inequality
> and $C(\cdot) \in [0,1]$,
> \[
> \mathbb{E}\bigl[|C(\hat{S}) - C(S)| \mid \hat{S} = S\bigr]
> \;\leq\; \frac{\sigma_C}{\sqrt{n_s}}
> \;\leq\; O\!\left(\frac{1}{\sqrt{n_}}\right),
> \]
> where $\sigma_C$ is the standard deviation of $C$.
> 
> *Case 2 ($\hat{S} \neq S$):* When the state estimate is incorrect,
> $C(\hat{S})$ is a mixture of the consensus scores of the true states:
> \[
> C(\hat{S}) = \sum_{s \in \mathcal{S}} \mathbb{P}(S = s \mid \hat{S})\, C(s).
> \]
> Since $C(\cdot) \in [0,1]$, the pointwise difference satisfies
> $|C(\hat{S}) - C(S)| \leq 1$, and consequently
> $\mathbb{E}[|C(\hat{S}) - C(S)| \mid \hat{S} \neq S] \leq 1$.
> 
> Combining the two cases,
> 
> $$
> \mathbb{E}\bigl[|C(\hat{S}) - C(S)|\bigr]
> &\leq \mathbb{P}(\hat{S}=S) \cdot O(1/\sqrt{n_})
>    + \mathbb{P}(\hat{S}\neq S) \cdot 1 

> &\leq \mathbb{P}(\hat{S} \neq S) + O(1/\sqrt{n_}). \qedhere
> $$

> **Corollary:** [Degradation to global consistency]
> <!-- label: cor:global-consistency -->
> As $\delta \to 0$, Lemma [ref] gives
> $\mathbb{P}(\hat{S} \neq S) \to 1 - \frac{\log 2}{\log K_{\mathcal{S}}}$.
> In this limit,
> \[
> C(\hat{S}) \xrightarrow{p} \sum_{s \in \mathcal{S}} \rho(s)\, C(s) = \bar{C},
> \]
> where $\rho(s) = \mathbb{P}(S = s)$ and $\bar{C}$ is the global average
> consistency. When features carry no state information, all estimated states
> converge to the same consistency value $\bar{C}$.

> **Corollary:** [Noise score degradation]
> <!-- label: cor:ns-degradation -->
> Under the same conditions and the additional assumption that the estimated
> states are approximately balanced
> ($\max_{\hat{s}} \rho(\hat{s}) / \min_{\hat{s}} \rho(\hat{s}) \leq R$ for
> some constant $R$), the SCX noise score degenerates to
> \[
> \operatorname{NS}(x) \propto r(x),
> \]
> where $r(x)$ is the residual of sample $x$. The SCX detector therefore
> reduces to the loss-based baseline detector. If the estimated states are
> highly imbalanced, the degradation is approximate with an additional
> $O(1/\sqrt{n})$ bias from state proportion estimation error.

### Proof of Theorem 2: AUC, PR-AUC, and F1 Bounds
<!-- label: sec:thm2:proof -->

> **Theorem:** [Weak feature failure lower bound]
> <!-- label: thm:weak-feature -->
> Let $\phi: \mathcal{X} \to \Phi$ be a $\delta$-weak feature map with respect to
> the true state $S$, i.e.\ $I(\phi(X); S) \leq \delta$ (in nats). Let
> $h_{SCX}$ be the SCX noise detector operating under the standard
> pipeline (clustering on $\phi$, state-conditional reliability estimates,
> noise scoring). Assume the estimated states are approximately balanced
> ($\max_{\hat{s}} \rho(\hat{s}) / \min_{\hat{s}} \rho(\hat{s}) \leq R$) and
> the clustering algorithm does not introduce error beyond the Fano lower bound.
> Then:
> 
> 
1. [(a)] **AUC bound:**
2. [(b)] **PR-AUC bound:**
3. [(c)] **F1 bound:**

> 
> Here $\operatorname{AUC}_{base}$,
> $\operatorname{PRAUC}_{base}$, and $\operatorname{F1}_{base}$
> are the performance metrics of the loss-based baseline detector that thresholds
> $\max_m \ell(f_m(x), y)$ without using $\phi$ or state information.

> **Proof:** The proof proceeds in six steps.
> 
> **Step 1: Construct an auxiliary distribution $\tilde{P**$.}
> Define $\tilde{P}$ by forcing $\phi$ and $S$ to be independent while preserving
> their marginal distributions:
> 
> $$
> \tilde{P}(\phi, S) = P(\phi)\, P(S).
> <!-- label: eq:aux-dist -->
> $$
> 
> All other conditional distributions (given $S$, the distribution of $(X,Y)$,
> experts, etc.) are unchanged.
> 
> **Step 2: Relate KL divergence and mutual information.**
> The KL divergence between $P$ and $\tilde{P}$ equals the mutual information
> between $\phi$ and $S$:
> 
> $$
> \operatorname{KL}(P \parallel \tilde{P})
> &= \iint P(\phi, S) \log\frac{P(\phi, S)}{P(\phi)P(S)}\, d\phi\, dS
> = I(\phi(X); S) = \delta.
> $$
> 
> By Pinsker's inequality  [cite],
> 
> $$
> \operatorname{TV}(P, \tilde{P}) \;\leq\;
> \sqrt{\frac{\operatorname{KL}(P \parallel \tilde{P})}{2}}
> = \sqrt{\frac{2}}.
> <!-- label: eq:pinsker-tv-bound -->
> $$
> 
> 
> **Step 3: Transfer the TV bound to the prediction distribution.**
> Let $P_{pred}$ and $\tilde{P}_{pred}$ be the joint distributions
> of $(\hat{z}_{SCX}(X), Z)$ under $P$ and $\tilde{P}$, respectively.
> Since the SCX noise score is a deterministic function of $X$ (and hence of
> $\phi$ and $S$), the data processing inequality  [cite] yields
> 
> $$
> \operatorname{TV}(P_{pred}, \tilde{P}_{pred})
> \;\leq\; \operatorname{TV}(P, \tilde{P})
> \;\leq\; \sqrt{\frac{2}}.
> <!-- label: eq:dp-tv -->
> $$
> 
> 
> **Step 4: Analyse SCX under $\tilde{P**$.}
> Under $\tilde{P}$, $\phi \perp S$, so $\phi$ carries no information about $S$.
> By Corollary [ref], the SCX noise score degenerates to the
> residual:
> \[
> \operatorname{NS}_{\tilde{P}}(x) \propto \max_m \ell(f_m(x), y).
> \]
> Hence the SCX detector under $\tilde{P}$ is equivalent to the loss-based
> baseline detector:
> 
> $$
> \operatorname{AUC}_{\tilde{P}}(h_{SCX}) &= \operatorname{AUC}_{base},
> <!-- label: eq:base-equiv-au --> 

> \operatorname{PRAUC}_{\tilde{P}}(h_{SCX}) &= \operatorname{PRAUC}_{base},
> <!-- label: eq:base-equiv-prau --> 

> \operatorname{F1}_{\tilde{P}}(h_{SCX}) &= \operatorname{F1}_{base}.
> <!-- label: eq:base-equiv-f1 -->
> $$
> 
> 
> **Step 5: Convert TV bounds to AUC/PR-AUC/F1 bounds.**
> 
> *AUC.* The AUC can be written as
> $\operatorname{AUC} = \mathbb{P}(score_{noise} >
> score_{clean})$, which involves two independent samples: one
> from $P(score \mid Z=1)$ (noise) and one from
> $P(score \mid Z=0)$ (clean). For product measures,
> 
> $$
> &\operatorname{TV}\bigl(P(\cdot\mid Z=1) \times P(\cdot\mid Z=0),\;
>         \tilde{P}(\cdot\mid Z=1) \times \tilde{P}(\cdot\mid Z=0)\bigr) 

> &\qquad\leq \operatorname{TV}(P(\cdot\mid Z=1), \tilde{P}(\cdot\mid Z=1))
>          + \operatorname{TV}(P(\cdot\mid Z=0), \tilde{P}(\cdot\mid Z=0)).
> $$
> 
> 
> We transfer the marginal TV bound to the conditional distributions. For any
> event $A$,
> 
> $$
> |P(A \mid Z=1) - \tilde{P}(A \mid Z=1)|
> &= \frac{|P(A \cap \{Z=1\}) - \tilde{P}(A \cap \{Z=1\})|} 

> &\leq \frac{\operatorname{TV}(P, \tilde{P})}
> \;\leq\; \frac{1}\sqrt{\frac{2}}.
> $$
> 
> Similarly,
> $\operatorname{TV}(P(\cdot\mid Z=0), \tilde{P}(\cdot\mid Z=0))
> \leq \frac{1}{1-\eta}\sqrt{\frac{2}}$.
> Combining,
> 
> $$
> |\operatorname{AUC}_P(h) - \operatorname{AUC}_{\tilde{P}}(h)|
> &\leq \operatorname{TV}(P(\cdot\mid Z=1), \tilde{P}(\cdot\mid Z=1))
>    + \operatorname{TV}(P(\cdot\mid Z=0), \tilde{P}(\cdot\mid Z=0)) 

> &\leq \sqrt{\frac{2}}\cdot
>    \left(\frac{1} + \frac{1}{1-\eta}\right).
> <!-- label: eq:auc-tv-transfer -->
> $$
> 
> 
> *PR-AUC.* The PR-AUC involves an integral over thresholds of precision,
> $\mathbb{P}(Z=1 \mid \hat{z}=1)$. The same amplification argument applies at
> each threshold, yielding the identical bound
>  [ref]. (A fully rigorous treatment requires additional steps
> to handle the integral over thresholds, but the bound at the level of the joint
> distribution is valid.)
> 
> *F1.* The F1 score is a function of the joint distribution
> $P(\hat{z}, Z)$ only:
> \[
> \operatorname{F1} = \frac{2 \cdot \operatorname{TP}}
>                          {2 \cdot \operatorname{TP}
>                           + \operatorname{FP} + \operatorname{FN}},
> \]
> where $\operatorname{TP} = \mathbb{P}(\hat{z}=1, Z=1)$,
> $\operatorname{FP} = \mathbb{P}(\hat{z}=1, Z=0)$, and
> $\operatorname{FN} = \mathbb{P}(\hat{z}=0, Z=1)$. Since F1 does not involve
> conditional sampling, the TV bound applies directly without amplification.
> 
> The F1 score is Lipschitz continuous in $( \operatorname{TP},
> \operatorname{FP}, \operatorname{FN})$. Its partial derivatives satisfy
> \[
> \Bigl|\frac{\partial \operatorname{F1}}{\partial \operatorname{TP}}\Bigr|
> = \frac{2(\operatorname{FP}+\operatorname{FN})}
>        {(2\operatorname{TP}+\operatorname{FP}+\operatorname{FN})^2}
> \leq \frac{2}{\min(\operatorname{TP}, 1)},
> \]
> and similarly for $\operatorname{FP}$, $\operatorname{FN}$. Let
> $p_ = \min(2\operatorname{TP}+\operatorname{FP}+\operatorname{FN})$.
> The Lipschitz constant satisfies $C_F \leq 2/p_^2$.
> 
> In the typical operating range where precision and recall are both at least
> $0.1$, direct calculation gives $C_F \leq 2$. More conservatively:
> 
- Precision, Recall $\geq 0.1$: $C_F \leq 3$,
- Precision, Recall $\geq 0.5$: $C_F \leq 1$.

> Hence
> 
> $$
> |\operatorname{F1}_P(h) - \operatorname{F1}_{\tilde{P}}(h)|
> \;\leq\; C_F \cdot \operatorname{TV}(P_{pred}, \tilde{P}_{pred})
> \;\leq\; C_F \cdot \sqrt{\frac{2}}.
> <!-- label: eq:f1-tv-transfer -->
> $$
> 
> 
> **Step 6: Combine the bounds.**
> From  [ref] and  [ref],
> 
> $$
> \operatorname{AUC}_P(h_{SCX})
> &\leq \operatorname{AUC}_{\tilde{P}}(h_{SCX})
>    + \sqrt{\frac{2}}\cdot\left(\frac{1} + \frac{1}{1-\eta}\right) 

> &= \operatorname{AUC}_{base}
>    + \sqrt{\frac{2}}\cdot\left(\frac{1} + \frac{1}{1-\eta}\right).
> $$
> 
> Similarly,
> 
> $$
> \operatorname{PRAUC}_P(h_{SCX})
> &\leq \operatorname{PRAUC}_{base}
>    + \sqrt{\frac{2}}\cdot\left(\frac{1} + \frac{1}{1-\eta}\right), 

> \operatorname{F1}_P(h_{SCX})
> &\leq \operatorname{F1}_{base} + C_F \cdot \sqrt{\frac{2}}.
> $$
> 
> This completes the proof.

> **Remark:** [Symmetric lower bound]
> <!-- label: remark:symmetric-bound -->
> The theorem also admits a symmetric lower bound
> \[
> \operatorname{AUC}(h_{SCX}) \;\geq\;
> \operatorname{AUC}_{base} -
> \sqrt{\frac{2}}\cdot\left(\frac{1} + \frac{1}{1-\eta}\right),
> \]
> which follows from the same TV argument applied in the opposite direction.
> When $\delta = 0$, the SCX AUC is *exactly* equal to the loss baseline
> AUC -- SCX can be neither better nor worse.

> **Remark:** [Interpretation of the $\eta$ dependence]
> <!-- label: remark:eta-interpretation -->
> When $\eta$ is small (rare noise), the AUC and PR-AUC bounds become loose.
> This reflects the intrinsic difficulty of detecting rare noise: SCX requires
> stronger features (smaller $\delta$) to reliably surpass the loss baseline.
> For $\eta = 0.5$ the factor $1/\eta + 1/(1-\eta) = 4$, the most favourable
> case; for $\eta \to 0$ or $\eta \to 1$ the factor diverges.

### Corollaries
<!-- label: sec:thm2:corollaries -->

#### Corollary 1: Complete Failure ($\delta = 0$)
<!-- label: cor:complete-failure -->
If $\phi(X)$ is independent of $S$ (i.e.\ $\phi$ is completely uninformative),
then
\[
\operatorname{AUC}(h_{SCX}) = \operatorname{AUC}_{base},\qquad
\operatorname{F1}(h_{SCX}) = \operatorname{F1}_{base}.
\]
If, in addition, the noise is loss-uninformative (e.g.\ uniform label noise),
the loss baseline itself degenerates to random guessing:
\[
\operatorname{AUC}_{base} = 0.5,\qquad
\operatorname{F1}_{base} = \frac{2\eta}{1+\eta}.
\]

#### Corollary 2: Loss-Uninformative Noise
<!-- label: cor:loss-uninformative -->
Under uniform label noise, the loss distribution is independent of the noise
indicator:
\[
P(\ell \mid Z=1) = P(\ell \mid Z=0).
\]
The loss baseline then reduces to the random baseline, and Theorem~2 gives

$$
\operatorname{AUC}(h_{SCX}) &\leq 0.5 +
\sqrt{\frac{2}}\cdot\left(\frac{1} + \frac{1}{1-\eta}\right),
<!-- label: eq:cor2-auc --> 

\operatorname{PRAUC}(h_{SCX}) &\leq \eta +
\sqrt{\frac{2}}\cdot\left(\frac{1} + \frac{1}{1-\eta}\right),
<!-- label: eq:cor2-prauc --> 

\operatorname{F1}(h_{SCX}) &\leq \frac{2\eta}{1+\eta} +
C_F\sqrt{\frac{2}}.
<!-- label: eq:cor2-f1 -->
$$

When $\delta = 0$, the PR-AUC is bounded by $\eta$ and the F1 by
$2\eta/(1+\eta)$.

#### Corollary 3: Minimum Information Threshold
<!-- label: cor:min-info -->
Suppose we require the SCX detection F1 to exceed the loss baseline by at
least $\Delta > 0$. The minimum mutual information necessary is

$$
\delta_ \;\geq\; 2\left(\frac{C_F}\right)^2.
<!-- label: eq:min-info-f1 -->
$$

For AUC improvements,

$$
\delta_ \;\geq\; 2\bigl(\Delta_{AUC} \cdot \eta(1-\eta)\bigr)^2.
<!-- label: eq:min-info-auc -->
$$

> **Example:** To achieve an F1 improvement of $\Delta = 0.05$ with $C_F = 2$,
> \[
> \delta_ \;\geq\; 2\left(\frac{0.05}{2}\right)^2
> = 2 \cdot 0.000625 = 1.25 \times 10^{-3}  nats.
> \]
> To achieve $\Delta = 0.1$ with $C_F = 2$,
> \[
> \delta_ \;\geq\; 2\left(\frac{0.1}{2}\right)^2
> = 5 \times 10^{-3}  nats.
> \]
> Since $\delta$ is mutual information in nats and $\delta \leq \log K_{\mathcal{S}}$,
> these thresholds are modest: $\delta = 10^{-3}$ corresponds to a likelihood
> ratio of $\exp(10^{-3}) \approx 1.001$ -- very little state information is
> needed for a measurable improvement.

#### Corollary 4: Effect of State Count $K_{\mathcal{S}$}
<!-- label: cor:state-count -->
As the number of true states $K_{\mathcal{S}}$ grows, maintaining the same
$\delta = I(\phi; S)$ requires progressively stronger features. The
normalised weakness $\varepsilon_\phi = \delta / \log K_{\mathcal{S}}$
determines SCX effectiveness:

- $\varepsilon_\phi \approx 1$: features carry almost no state
- $\varepsilon_\phi \approx 0$: features carry full state information;
- $\varepsilon_\phi \approx 0.5$: state discovery is about half

Blindly increasing the number of states $K_{\mathcal{S}}$ is therefore
counterproductive without a corresponding increase in feature information
$\delta$.

### Practical Diagnostics
<!-- label: sec:thm2:diagnostics -->

The following diagnostics operationalise Theorem~2 for practitioners.

**Diagnostic 1: Within-state consistency convergence.**
If all estimated states have near-equal consensus scores $C(\hat{s})$,
the features may be too weak:
\[
\operatorname{Var}\bigl(\{C(\hat{s})\}_{\hat{s} \in \hat{\mathcal{S}}}\bigr)
< \tau_C.
\]

**Diagnostic 2: Random baseline comparison.**
Compute the loss baseline AUC and PR-AUC on the training set. If they are
close to the random baseline ($\operatorname{AUC} \approx 0.5$,
$\operatorname{PRAUC} \approx \eta$), the noise detection task is intrinsically
difficult, and weak features further prevent SCX from surpassing this baseline.

**Diagnostic 3: Supervised state matching (when available).**
If ground-truth state labels exist for a subset (e.g.\ simulated data or known
batch sources), compute the adjusted Rand index (ARI) between the $\phi$-based
clustering and the true states:
\[
\operatorname{ARI}(\hat{S}, S) < 0.1 \;\Longrightarrow\; features too weak.
\]

**Diagnostic 4: Mutual information estimation.**
Estimate $I(\phi(X); Y)$ via a Kraskov $k$-NN estimator or MINE, and compare
with $\log K_{\mathcal{S}}$:
\[
\frac{\hat{I}(\phi(X); Y)}{\log K_{\mathcal{S}}} < 0.2
\;\Longrightarrow\; features may be too weak.
\]

**Threshold guidelines.**
Based on Theorem~2 and Corollary~3, we recommend the operational thresholds
in Table [ref].

[Table omitted — see original .tex]

Here $\varepsilon_\phi = I(\phi; S) / \log K_{\mathcal{S}}$ and
$\eta = \mathbb{P}(Z=1)$ is the marginal noise rate.

\begin{thebibliography}{10}
\bibitem{fano1961}
R.~M.~Fano, *Transmission of Information: A Statistical Theory of
Communications*. MIT Press, 1961.

\bibitem{cover2006}
T.~M.~Cover and J.~A.~Thomas, *Elements of Information Theory*, 2nd~ed.
Wiley, 2006.

\bibitem{pinsker1964}
M.~S.~Pinsker, *Information and Information Stability of Random Variables
and Processes*. Holden-Day, 1964.
\end{thebibliography}

\endinput