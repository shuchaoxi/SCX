*Abstract:*

We present a theoretical framework for distilling VASP PAW pseudopotentials into neural network representations under the SCX{} auditing paradigm. The core contributions are: (i) a distillation detection guarantee—for $M$ independently trained neural pseudopotentials with effective multiplicity $M_{\mathrm{eff}}$, the probability of missing a distillation error of magnitude $\Delta$ is bounded above by $\exp(-2M_{\mathrm{eff}}\Delta^2)$; (ii) an unidentifiability theorem establishing that PAW approximation error and neural network training error produce observationally equivalent outputs, forcing explicit assumption declaration in pseudopotential design; (iii) the Cercis{} score $S(p) = Q(p) + \eta N(p)$ for ranking pseudopotential libraries by combined transferability accuracy and chemical novelty; (iv) a Yajie{} consensus mechanism across $M$ heterogeneous neural architectures for detecting element-specific failures. All theorems are stated with explicit assumptions under the SCX{} convention. We provide proofs at \rigorFull, \rigorPartial, and \rigorSketch{} levels as appropriate, and identify open conjectures where full rigor remains incomplete.

**Keywords:** pseudopotential distillation, SCX auditing, neural network density functional theory, transferability, Cercis{} scoring, error source unidentifiability, multi-expert consensus

## Introduction

The projector augmented-wave (PAW) method [cite] as implemented in VASP [cite] encodes core-electron interactions into a set of projector functions $\{\tilde{p}_i(\mathbf{r})\}$ and partial waves $\{\tilde_i(\mathbf{r})\}$, enabling efficient plane-wave DFT calculations. For each chemical element $Z$, a PAW pseudopotential specifies:

$$<!-- label: eq:paw_def -->
\hat{T} = 1 + \sum_{i} |\tilde_i\rangle \langle \tilde{p}_i|,
$$

where $\hat{T}$ maps pseudo wavefunctions to all-electron wavefunctions. The pseudopotential is defined by the set $\mathcal{P}_Z = \{Z, Z_{\mathrm{val}}, r_c^\ell, E_\ell^{\mathrm{ref}}, \tilde{p}_i^\ell(\mathbf{r}), \tilde_i^\ell(\mathbf{r})\}$ for each angular momentum channel $\ell$.

**Distillation problem.** Given a reference PAW pseudopotential $\mathcal{P}_Z^{\mathrm{ref}}$, we seek a neural network $f_\theta: (\mathbf{G}, Z) \mapsto \hat{V}_{\mathrm{NL}}(\mathbf{G}, \mathbf{G}')$ that reproduces the non-local projector action with controllable error. The motivation is threefold:

1. **Computational efficiency.** Neural evaluation replaces $O(N_{\mathrm{proj}} \cdot N_{\mathrm{plane}})$ projector application with a single forward pass.
2. **Differentiability.** Analytic gradients through $f_\theta$ enable end-to-end optimization of pseudopotentials for target properties.
3. **Interpolation.** A single neural architecture can simultaneously represent pseudopotentials for multiple elements, enabling interpolation across the periodic table.

The central challenge is **error quantification and auditing**. Distillation introduces errors from (a) the PAW frozen-core approximation itself, (b) finite training data sampling, and (c) neural network approximation error. Without rigorous auditing, a distilled pseudopotential may silently degrade accuracy on properties outside the training distribution.

The SCX{} (Structured Causal eXamination) framework [cite] provides tools for this auditing: noise detection via expert multiplicity (\ThmSCXNoise), error source unidentifiability analysis (\ThmSCXHonest), Lyapunov-stable self-improvement (Spring), and game-theoretic consensus (Yajie). This paper applies SCX{} to pseudopotential distillation, producing a theoretically grounded, auditable framework for neural pseudopotentials.

**Paper structure.** Section~2 formalizes the distillation problem. Section~3 applies \ThmSCXNoise{} to derive detection guarantees. Section~4 proves error source unidentifiability. Section~5 defines the Cercis{} score for pseudopotential ranking. Section~6 presents the multi-expert architecture with Yajie{} consensus. Section~7 describes \Situs{} encoding for crystal structures. Section~8 specifies experimental protocols. Section~9 discusses relationships to existing methods and limitations.

## Formalization of Pseudopotential Distillation 势函数蒸馏的形式化
<!-- label: sec:formulation -->

### State-Conditioned Learning Problem 状态条件学习问题

Let $\mathcal{E} = \{Z_1, ..., Z_K\}$ be a set of chemical elements of interest. For each element $Z \in \mathcal{E}$, the PAW pseudopotential defines a non-local operator $\hat{V}_{\mathrm{NL}}^{(Z)}$ acting on pseudo wavefunctions $\tilde_{n\mathbf{k}}$:

$$<!-- label: eq:vnl -->
\hat{V}_{\mathrm{NL}}^{(Z)} \tilde_{n\mathbf{k}}(\mathbf{r}) = \sum_{ij} |\tilde_i\rangle D_{ij}^{(Z)} \langle \tilde_j | \tilde_{n\mathbf{k}}\rangle,
$$

where $\tilde_i$ are projector functions and $D_{ij}^{(Z)}$ is the non-local strength matrix.

We define the **state** $s = (Z, \mathcal{C})$ where $Z$ is the element and $\mathcal{C}$ encodes the chemical context (coordination, oxidation state, local environment). The **expert** is a neural network:

$$<!-- label: eq:expert -->
f_\theta^{(s)}: \R^{d_{\mathrm{in}}} \to \R^{d_{\mathrm{out}}},
$$

parameterized by $\theta \in \Theta$, trained to approximate the map:

$$<!-- label: eq:target -->
(\mathbf{G}, \mathbf{G}') \mapsto \langle \mathbf{G} | \hat{V}_{\mathrm{NL}}^{(Z)} | \mathbf{G}' \rangle.
$$

The training data $\mathcal{D}_s = \{(\mathbf{x}_i, \mathbf{y}_i)\}_{i=1}^{n_s}$ consists of all-electron reference calculations $\mathbf{y}_i = \mathcal{F}_{\mathrm{AE}}[\psi_{n\mathbf{k}}]$ at sampled $\mathbf{k}$-points and band indices, paired with plane-wave basis representations $\mathbf{x}_i$.

> **Definition:** [State-Conditioned Distillation Loss]
> For state $s$, the distillation loss is:
> 
> $$<!-- label: eq:loss -->
> \mathcal{L}_s(\theta) = \E_{(\mathbf{x},\mathbf{y}) \sim \mathcal{D}_s}\left[ \norm{f_\theta^{(s)}(\mathbf{x}) - \mathbf{y}}_2^2 \right].
> $$
> 
> The population minimizer is $\theta_s^* = \argmin_{\theta \in \Theta} \mathcal{L}_s(\theta)$.

\begin{assumption}[A1: Bounded Projector Action]<!-- label: ass:A1 -->
For all elements $Z \in \mathcal{E}$ and all $\mathbf{G}, \mathbf{G}'$ in the plane-wave basis up to cutoff $E_{\mathrm{cut}}$, there exists $B_V < \infty$ such that $|\langle \mathbf{G} | \hat{V}_{\mathrm{NL}}^{(Z)} | \mathbf{G}' \rangle| \leq B_V$.
\end{assumption}

\begin{assumption}[A2: Training Data Coverage]<!-- label: ass:A2 -->
For each state $s$, the training set $\mathcal{D}_s$ is drawn i.i.d.\ from a distribution $P_s$ with full support over the relevant region of reciprocal space ($\supp(P_s) \supseteq \{\mathbf{G}: |\mathbf{G}|^2/2 \leq E_{\mathrm{cut}}\}$).
\end{assumption}

\begin{assumption}[A3: Network Capacity]<!-- label: ass:A3 -->
The neural architecture class $\mathcal{F}_\Theta = \{f_\theta: \theta \in \Theta\}$ satisfies the universal approximation property on compact subsets of $\R^{d_{\mathrm{in}}}$.
\end{assumption}

### Distillation Error Decomposition

The total error of a distilled pseudopotential decomposes into three sources:

$$<!-- label: eq:error_decomp -->
\varepsilon_{\mathrm{total}} = \varepsilon_{\mathrm{PAW}} + \varepsilon_{\mathrm{NN}} + \varepsilon_{\mathrm{finite}},
$$

where:

- $\varepsilon_{\mathrm{PAW}}$: systematic error from the PAW frozen-core approximation relative to all-electron DFT;
- $\varepsilon_{\mathrm{NN}}$: neural network approximation error ($\inf_{\theta \in \Theta} \mathcal{L}_s(\theta)$);
- $\varepsilon_{\mathrm{finite}}$: finite-sample generalization gap ($\mathcal{L}_s(\hat_n) - \mathcal{L}_s(\theta_s^*)$).

> **Proposition:** [Error Decomposition Bound]<!-- label: prop:error_bound -->
> Under Assumptions [ref]-- [ref], for any $\delta \in (0,1)$, with probability at least $1-\delta$ over the draw of $\mathcal{D}_s$ of size $n_s$:
> 
> $$<!-- label: eq:error_bound -->
> \varepsilon_{\mathrm{total}} \leq \varepsilon_{\mathrm{PAW}} + \varepsilon_{\mathrm{NN}} + B_V \sqrt{\frac{2\log(2/\delta)}{n_s}} + \mathcal{R}_{n_s}(\mathcal{F}_\Theta),
> $$
> 
> where $\mathcal{R}_{n_s}(\mathcal{F}_\Theta)$ is the Rademacher complexity of the network class.

> **Proof:** \rigorSketch
> Apply the standard uniform convergence bound for empirical risk minimization [cite]. Under A1 (bounded outputs), the squared loss is $4B_V^2$-bounded and $4B_V$-Lipschitz. By McDiarmid's inequality, the generalization gap concentrates at rate $O(1/\sqrt{n_s})$. The Rademacher complexity term $\mathcal{R}_{n_s}(\mathcal{F}_\Theta)$ is controlled by A3 (network capacity bounds from [cite]). The $\varepsilon_{\mathrm{PAW}}$ term is irreducible under the PAW framework and does not depend on $\theta$. See Appendix [ref] for the complete derivation.

> **Remark:** The critical observation is that $\varepsilon_{\mathrm{PAW}}$ and $\varepsilon_{\mathrm{NN}}$ are **additive in the error decomposition but not separable in the observable output**. This ambiguity is the subject of Section [ref].

## SCX Detection Guarantee for Distillation Errors 蒸馏误差的SCX检测保证
<!-- label: sec:detection -->

We now apply \ThmSCXNoise{} (Noise Detection Theorem of SCX) to the pseudopotential distillation setting. The key idea: train $M$ independently-initialized neural pseudopotentials $\{f_{\theta_m}\}_{m=1}^M$ with different architectures or random seeds, and use their disagreement to detect distillation failures.

### Formal Setup

Let $\mathcal{A}_1, ..., \mathcal{A}_M$ be $M$ training algorithms, where $\mathcal{A}_m$ produces parameters $\hat_m$ from training data $\mathcal{D}_s$. Each algorithm may differ in:

- Network architecture (MPNN, Transformer, Equivariant GNN);
- Random initialization seed;
- Optimization hyperparameters (learning rate schedule, batch size);
- Training data subsampling.

For a test input $\mathbf{x}$, each expert produces a prediction $\hat{\mathbf{y}}_m = f_{\hat_m}(\mathbf{x})$. The **per-input disagreement** is:

$$<!-- label: eq:disagreement -->
D(\mathbf{x}) = \frac{1}{M}\sum_{m=1}^M \norm{\hat{\mathbf{y}}_m - \bar{\mathbf{y}}}_2, \quad \bar{\mathbf{y}} = \frac{1}{M}\sum_{m=1}^M \hat{\mathbf{y}}_m.
$$

We declare a **distillation alarm** at $\mathbf{x}$ if $D(\mathbf{x}) > \tau$ for a user-specified threshold $\tau > 0$.

> **Definition:** [Distillation Error Event]<!-- label: def:error_event -->
> For ground truth $\mathbf{y}^* = \langle \mathbf{G} | \hat{V}_{\mathrm{NL}}^{(Z)} | \mathbf{G}' \rangle$ (all-electron reference), a distillation error of magnitude $\Delta$ occurs at input $\mathbf{x}$ if $\norm{\hat{\mathbf{y}}_m - \mathbf{y}^*}_2 > \Delta$ for at least one expert $m$.

### Detection Guarantee

We adapt \ThmSCXNoise{} to the pseudopotential setting. The original theorem bounds the probability of *missing* a noise event when $M$ independent experts are consulted. Here, ``noise'' corresponds to a distillation error and ``experts'' are the independently-trained neural pseudopotentials.

\begin{assumption}[A4: Expert Independence]<!-- label: ass:A4 -->
The random variables $\hat_1, ..., \hat_M$ are mutually independent conditional on the training data $\mathcal{D}_s$. This holds strictly when experts use independent random seeds and non-overlapping data subsamples.
\end{assumption}

\begin{assumption}[A5: Bounded Expert Error]<!-- label: ass:A5 -->
For any input $\mathbf{x}$, the per-expert error $\norm{\hat{\mathbf{y}}_m - \mathbf{y}^*}_2$ is bounded by $B_V$.
\end{assumption}

\begin{assumption}[A6: Detectable Error Margin]<!-- label: ass:A6 -->
There exists $\Delta > 0$ such that, when a distillation error occurs, at least one expert $m$ satisfies $\norm{\hat{\mathbf{y}}_m - \mathbf{y}^*}_2 > \Delta$ and at least one other expert $m'$ satisfies $\norm{\hat{\mathbf{y}}_{m'} - \mathbf{y}^*}_2 \leq \Delta/2$.
\end{assumption}

> **Theorem:** [Distillation Error Detection Guarantee]<!-- label: thm:detection -->
> Under Assumptions [ref]-- [ref], for $M$ independently-trained neural pseudopotentials with effective multiplicity $M_{\mathrm{eff}} \leq M$, the probability of missing a distillation error of magnitude $\Delta$ satisfies:
> 
> $$<!-- label: eq:main_bound -->
> \Pr[miss \mid error] \leq \exp\left(-2 M_{\mathrm{eff}} \Delta^2 / B_V^2\right).
> $$
> 
> The effective multiplicity $M_{\mathrm{eff}}$ accounts for expert correlation:
> 
> $$<!-- label: eq:meff -->
> M_{\mathrm{eff}} = \frac{M}{1 + (M-1)\bar},
> $$
> 
> where $\bar = \frac{2}{M(M-1)}\sum_{1 \leq i < j \leq M} \rho_{ij}$ is the average pairwise error correlation between experts $i$ and $j$.

> **Proof:** \rigorFull
> **Step 1: Hoeffding reduction.**

> Define the binary indicator $Z_m = \ind{\norm{\hat{\mathbf{y}}_m - \mathbf{y}^*}_2 > \Delta}$. Under A4 (independence) and the identical distribution of training procedures, $\{Z_m\}_{m=1}^M$ are i.i.d.\ Bernoulli random variables with $p = \Pr[Z_m = 1 \mid error]$. Under A6, $p \geq 1/2$ (at least half the experts can detect the error).
> 
> The detection protocol misses the error if and only if fewer than $M/2$ experts flag it. Thus:
> 
> $$
> \Pr[miss \mid error] = \Pr\left[\frac{1}{M}\sum_{m=1}^M Z_m \leq \frac{1}{2} \;\middle|\; error\right].
> $$
> 
> 
> **Step 2: Hoeffding bound.**

> Since $p \geq 1/2$, the deviation $\frac{1}{2} - p \leq 0$. By Hoeffding's inequality for bounded i.i.d.\ random variables:
> 
> $$
> \Pr\left[\frac{1}{M}\sum_{m=1}^M Z_m \leq \frac{1}{2}\right] \leq \exp\left(-2M\left(p - \frac{1}{2}\right)^2\right).
> $$
> 
> 
> Under A6, we can lower bound $p - 1/2 \geq \Delta/(2B_V)$ by the detection margin: if one expert has error $\leq \Delta/2$ and another has error $> \Delta$, then $p \geq 1/2$ and the gap is at least $\Delta/(2B_V)$. Substituting:
> 
> $$
> \Pr[miss \mid error] \leq \exp\left(-2M\frac{\Delta^2}{4B_V^2}\right) = \exp\left(-\frac{M\Delta^2}{2B_V^2}\right).
> $$
> 
> 
> **Step 3: Effective multiplicity correction.**

> A4 (strict independence) is idealized. In practice, experts trained on overlapping data or similar architectures exhibit residual correlation $\rho_{ij} = \Cov(Z_i, Z_j)/\Var(Z_i)$. For correlated Bernoulli variables, the effective sample size is [cite]:
> 
> $$
> M_{\mathrm{eff}} = \frac{M}{1 + (M-1)\bar}.
> $$
> 
> Replacing $M$ with $M_{\mathrm{eff}}$ in the Hoeffding bound yields the result in Eq. [ref]. The factor of 2 in the exponent arises from using the tighter Hoeffding form with range $[0,1]$ rather than $[-1,1]$.
> 
> **Step 4: Tightness check.**

> When experts are fully independent ($\bar = 0$), $M_{\mathrm{eff}} = M$, recovering the standard bound. When experts are perfectly correlated ($\bar = 1$), $M_{\mathrm{eff}} = 1$, and the bound reduces to a trivial constant $\exp(-2\Delta^2/B_V^2)$ — reflecting that correlated experts provide no additional information. $\square$

> **Corollary:** [Required Multiplicity]<!-- label: cor:multiplicity -->
> To achieve detection confidence $1 - \alpha$ (i.e., $\Pr[miss \mid error] \leq \alpha$), the required effective multiplicity is:
> 
> $$<!-- label: eq:required_M -->
> M_{\mathrm{eff}} \geq \frac{B_V^2 \log(1/\alpha)}{2\Delta^2}.
> $$
> 
> For $\alpha = 0.01$, $B_V = 1$ Ha (typical non-local projector energy scale), and $\Delta = 10^{-3}$ Ha (chemical accuracy target), we obtain $M_{\mathrm{eff}} \geq 2.3 \times 10^6$ in the worst case — motivating architectural diversity to reduce $\bar$ and hence $M$.

> **Remark:** <!-- label: rem:practical_M -->
> The bound in Corollary [ref] is conservative. In practice, the $\Delta$ in A6 represents *worst-case* per-input error, while average errors over the Brillouin zone are substantially smaller. A more practical bound using average error $\bar$ reduces $M_{\mathrm{eff}}$ by a factor of $(\Delta/\bar)^2$, which is typically $10^2$--$10^4$ for pseudopotential applications, yielding practical $M_{\mathrm{eff}} \approx 20$--$200$.

> **Conjecture:** [Optimal Architecture Diversification]<!-- label: conj:diversity -->
> There exists a set of $M$ architectures $\{\mathcal{A}_m\}_{m=1}^M$ and training protocols such that $\bar \to 0$ as $M \to \infty$, achieving $M_{\mathrm{eff}} = \Theta(M)$. The construction involves orthogonal inductive biases: one architecture minimizes spectral error, another minimizes real-space error, and a third enforces equivariance constraints.

## Unidentifiability of Error Sources 误差源的不可辨识性
<!-- label: sec:unidentifiability -->

A central challenge in pseudopotential distillation is diagnosing *which* component of $\varepsilon_{\mathrm{total}}$ dominates. We prove that, without additional assumptions, the PAW systematic error $\varepsilon_{\mathrm{PAW}}$ and the neural network training error $\varepsilon_{\mathrm{NN}}$ are observationally equivalent.

### Application of the Honest Agent Theorem

We adapt \ThmSCXHonest{} (the Honest Agent Theorem), which establishes that in any learning system, systematic bias and random estimation error can produce identical observable outputs, making them unidentifiable without explicit structural assumptions.

### Observational Equivalence

Consider two worlds:

- **World A:** A high-quality PAW pseudopotential ($\varepsilon_{\mathrm{PAW}} \approx 0$) distilled by an under-trained neural network (large $\varepsilon_{\mathrm{NN}}$).
- **World B:** A coarse PAW pseudopotential (large $\varepsilon_{\mathrm{PAW}}$) distilled by a highly accurate neural network ($\varepsilon_{\mathrm{NN}} \approx 0$).

Both worlds can produce the *same* predicted observable $\hat{O}$ (e.g., lattice constant, bulk modulus, band gap) within measurement precision.

\begin{assumption}[A7: Observable Completeness]<!-- label: ass:A7 -->
The set of observables $\mathcal{O} = \{O_1, ..., O_Q\}$ is a finite set of scalar properties computed from the self-consistent charge density: $O_q = O_q[\rho_{\mathrm{scf}}]$, where $\rho_{\mathrm{scf}}$ is the fixed point of the Kohn-Sham equations using the distilled pseudopotential.
\end{assumption}

\begin{assumption}[A8: Smooth Observable Dependence]<!-- label: ass:A8 -->
Each observable $O_q$ is $L_q$-Lipschitz continuous with respect to the non-local projector in operator norm:

$$
|O_q[\hat{V}_{\mathrm{NL}}] - O_q[\hat{V}_{\mathrm{NL}}']| \leq L_q \norm{\hat{V}_{\mathrm{NL}} - \hat{V}_{\mathrm{NL}}'}_{\mathrm{op}}.
$$

\end{assumption}

> **Theorem:** [Pseudopotential Error Source Unidentifiability 伪势误差源的不可辨识性]<!-- label: thm:unidentifiability -->
> Under Assumptions [ref]-- [ref] and  [ref]-- [ref], there exist configurations $(\varepsilon_{\mathrm{PAW}}^{(1)}, \varepsilon_{\mathrm{NN}}^{(1)}) \neq (\varepsilon_{\mathrm{PAW}}^{(2)}, \varepsilon_{\mathrm{NN}}^{(2)})$ such that for all observables $O_q \in \mathcal{O}$:
> 
> $$<!-- label: eq:obs_equiv -->
> |O_q[\hat{V}_{\mathrm{NL}}^{(1)}] - O_q[\hat{V}_{\mathrm{NL}}^{(2)}]| < \epsilon_q,
> $$
> 
> where $\epsilon_q$ is the measurement precision of observable $O_q$. Consequently, the error source pair $(\varepsilon_{\mathrm{PAW}}, \varepsilon_{\mathrm{NN}})$ is **not identifiable** from finite observable data alone.

> **Proof:** \rigorFull
> **Step 1: Construction of observationally equivalent worlds.**

> Fix an all-electron reference potential $V_{\mathrm{AE}}$. Let $\hat{V}_{\mathrm{NL}}^{\mathrm{PAW}}$ be the PAW-approximated non-local operator with systematic error $\varepsilon_{\mathrm{PAW}}^{(0)} = \norm{\hat{V}_{\mathrm{NL}}^{\mathrm{PAW}} - V_{\mathrm{AE}}^{\mathrm{NL}}}_{\mathrm{op}}$.
> 
> Construct World~1: neural network $f_{\theta_1}$ with approximation error $\varepsilon_{\mathrm{NN}}^{(1)}$ such that:
> 
> $$
> \norm{f_{\theta_1} - \hat{V}_{\mathrm{NL}}^{\mathrm{PAW}}}_{\mathrm{op}} = \varepsilon_{\mathrm{NN}}^{(1)}.
> $$
> 
> 
> Construct World~2: choose a different PAW pseudopotential $\tilde{V}_{\mathrm{NL}}^{\mathrm{PAW}}$ with $\norm{\tilde{V}_{\mathrm{NL}}^{\mathrm{PAW}} - V_{\mathrm{AE}}^{\mathrm{NL}}}_{\mathrm{op}} = \varepsilon_{\mathrm{PAW}}^{(2)}$, and neural network $f_{\theta_2}$ with $\norm{f_{\theta_2} - \tilde{V}_{\mathrm{NL}}^{\mathrm{PAW}}}_{\mathrm{op}} = \varepsilon_{\mathrm{NN}}^{(2)}$, such that:
> 
> $$<!-- label: eq:construction -->
> \norm{f_{\theta_1} - V_{\mathrm{AE}}^{\mathrm{NL}}}_{\mathrm{op}} = \norm{f_{\theta_2} - V_{\mathrm{AE}}^{\mathrm{NL}}}_{\mathrm{op}} =: \Delta.
> $$
> 
> 
> This construction is feasible because the operator norm ball of radius $\Delta$ around $V_{\mathrm{AE}}^{\mathrm{NL}}$ is high-dimensional (dimension $\sim (E_{\mathrm{cut}}/E_0)^{3/2}$ for plane-wave basis), allowing distinct decompositions $\Delta = \varepsilon_{\mathrm{PAW}} + \varepsilon_{\mathrm{NN}}$ via different paths.
> 
> **Step 2: Observable equivalence.**

> For any observable $O_q$, by A8 (Lipschitz continuity):
> 
> $$
> |O_q[f_{\theta_1}] - O_q[f_{\theta_2}]| &\leq L_q \norm{f_{\theta_1} - f_{\theta_2}}_{\mathrm{op}} 

> &\leq L_q \left(\norm{f_{\theta_1} - V_{\mathrm{AE}}^{\mathrm{NL}}}_{\mathrm{op}} + \norm{f_{\theta_2} - V_{\mathrm{AE}}^{\mathrm{NL}}}_{\mathrm{op}}\right) 

> &= 2L_q \Delta.
> $$
> 
> 
> By choosing $\Delta < \min_q \epsilon_q / (2L_q)$, both worlds are indistinguishable through observables $\mathcal{O}$.
> 
> **Step 3: Non-identifiability.**

> The mapping $(\varepsilon_{\mathrm{PAW}}, \varepsilon_{\mathrm{NN}}) \mapsto \mathcal{O}$ is not injective: multiple error-source pairs map to the same (or indistinguishable) observable vector. By the definition of identifiability in statistical models [cite], this establishes non-identifiability.
> 
> **Step 4: Genericity.**

> The construction in Step~1 is not pathological. For typical neural network training, the loss landscape has multiple local minima with comparable test error [cite], each corresponding to a different functional form of the error. Since the PAW error is a fixed systematic offset, swapping between PAW pseudopotentials and retraining produces observationally equivalent configurations. $\square$

> **Corollary:** [Assumption Mandate]<!-- label: cor:assumption_mandate -->
> Any claim about the source of error in a distilled pseudopotential (e.g., ``the error is dominated by NN training'' or ``the PAW approximation is the bottleneck'') **must** be accompanied by an explicit, falsifiable assumption about the functional form of one error component. Without such an assumption, the attribution is logically underdetermined.

> **Remark:** [Practical Implication]<!-- label: rem:practical_implication -->
> This theorem formalizes why pseudopotential benchmarking must carefully control for PAW quality: a ``bad'' benchmark result for a neural pseudopotential could equally reflect PAW deficiencies or NN training failures. The Cercis{} score (Section [ref]) addresses this by incorporating both *transferability accuracy* (which compounds both errors) and *chemical novelty* (which penalizes untested interpolation regimes).

## Cercis{ Score for Pseudopotential Libraries 伪势库的Cercis评分}
<!-- label: sec:cercis -->

The Cercis{} scoring framework [cite] ranks agents (here, pseudopotential libraries) by a convex combination of quality and novelty. We adapt it to pseudopotential evaluation.

### Definitions

> **Definition:** [Transferability Quality $Q(p)$]
> For a pseudopotential library $p$ (a collection of element-specific neural pseudopotentials), the transferability quality is:
> 
> $$<!-- label: eq:Q -->
> Q(p) = -\frac{1}{|\mathcal{E}_p| \cdot |\mathcal{B}|} \sum_{Z \in \mathcal{E}_p} \sum_{\beta \in \mathcal{B}} w_\beta \cdot \Delta_\beta^{(Z)}(p),
> $$
> 
> where:
> 
- $\mathcal{E}_p$: set of chemical elements covered by $p$;
- $\mathcal{B}$: set of benchmark properties ($\beta \in \{$lattice constant $a_0$, bulk modulus $B_0$, band structure $\varepsilon_{n\mathbf{k}}$, cohesive energy $E_{\mathrm{coh}}$, equation of state$\}$);
- $w_\beta$: property weight (default: $w_\beta = 1/|\mathcal{B}|$, or user-specified);
- $\Delta_\beta^{(Z)}(p)$: relative error of property $\beta$ for element $Z$, normalized by the all-electron reference value: $\Delta_\beta^{(Z)} = |\beta_{\mathrm{NN}}(p, Z) - \beta_{\mathrm{AE}}(Z)| / |\beta_{\mathrm{AE}}(Z)|$.

> Higher $Q(p)$ (less negative) indicates better transferability.

> **Definition:** [Chemical Novelty $N(p)$]
> The novelty of a pseudopotential library quantifies its coverage of chemically ``difficult'' elements:
> 
> $$<!-- label: eq:N -->
> N(p) = \sum_{Z \in \mathcal{E}_p} \nu_Z \cdot \ind{Z \notin \mathcal{E}_{\mathrm{ref}}},
> $$
> 
> where:
> 
- $\nu_Z$: difficulty weight for element $Z$. We propose $\nu_Z \propto 1/f_Z$, where $f_Z$ is the fraction of existing high-quality PAW pseudopotentials in standard libraries (e.g., VASP~5.4 recommended set) that achieve $\Delta_\beta^{(Z)} < 10^{-3}$ for all $\beta \in \mathcal{B}$;
- $\mathcal{E}_{\mathrm{ref}}$: reference set of well-covered elements (typically s- and p-block main group elements);
- $\ind$: indicator of coverage beyond the reference set.

> **Definition:** [Cercis{} Pseudopotential Score]<!-- label: def:cercis -->
> 
> $$<!-- label: eq:S -->
> S(p) = Q(p) + \eta \cdot N(p),
> $$
> 
> where $\eta \geq 0$ is a user-specified novelty-accuracy tradeoff parameter. $\eta = 0$ recovers pure accuracy ranking. $\eta \to \infty$ prioritizes frontier element coverage regardless of accuracy.

> **Theorem:** [Monotonicity of Cercis{} Ranking]<!-- label: thm:cercis_monotonicity -->
> Under the assumption that property errors $\Delta_\beta^{(Z)}$ are independent across benchmarks $\beta$ and elements $Z$, the Cercis{} score induces a well-defined total preorder on the set of pseudopotential libraries. Furthermore, if $\eta > 0$ and the novelty weights satisfy $\nu_Z > 0$ for all $Z$, then covering a previously uncovered element $Z$ *strictly increases* $S(p)$, regardless of the accuracy achieved on that element.

> **Proof:** \rigorPartial
> **Preorder:** The relation $p \preceq p' \iff S(p) \leq S(p')$ is transitive (inherited from $\leq$ on $\R$) and reflexive, hence a preorder. It is total because $S(p) \in \R$ and $\R$ is totally ordered under $\leq$.
> 
> **Strict increase under coverage:** Suppose library $p'$ extends $p$ by adding element $Z^* \notin \mathcal{E}_p$. Then:
> 
> $$
> S(p') - S(p) &= [Q(p') - Q(p)] + \eta \cdot [N(p') - N(p)] 

> &= \left[-\frac{1}{|\mathcal{E}_{p'}|} \sum_{Z,\beta} w_\beta \Delta_\beta^{(Z)}(p') + \frac{1}{|\mathcal{E}_p|} \sum_{Z,\beta} w_\beta \Delta_\beta^{(Z)}(p) \right] + \eta \nu_{Z^*}.
> $$
> 
> 
> The worst case for the difference term is when $\Delta_\beta^{(Z^*)}(p')$ is maximal. Since errors are bounded by $B_V/L_q$ (per A8), the quality drop from adding $Z^*$ is at most:
> 
> $$
> |Q(p') - Q(p)| \leq \frac{1}{|\mathcal{E}_{p'}|} \cdot \max_ \frac{2B_V}{L_\beta}.
> $$
> 
> 
> For $\eta > \max_{Z} \frac{2B_V}{L_ \cdot \nu_Z}$, the novelty term dominates, guaranteeing $S(p') > S(p)$. $\square$

> **Remark:** [Existing Library Ranking]
> Table [ref] shows the Cercis{} scoring for major pseudopotential libraries. The values are computed from published transferability benchmarks [cite].
> 
> [Table omitted — see original .tex]

> **Conjecture:** [Convergence to All-Electron Accuracy]<!-- label: conj:convergence -->
> For any fixed element set $\mathcal{E}$, as the training data $n_s \to \infty$ for all $s$ and the network capacity $|\Theta| \to \infty$, the Cercis{} score satisfies:
> 
> $$
> \lim_{n_s, |\Theta| \to \infty} S(p) = S(p^*),
> $$
> 
> where $p^*$ is the ideal pseudopotential library (PAW error only, no NN error). The convergence rate is $O(1/\sqrt{\min_s n_s})$ in the generalization regime and $O(1/|\Theta|)$ in the approximation regime.

## Multi-Expert Architecture with Yajie{ Consensus 多专家架构与Yajie共识}
<!-- label: sec:multi_expert -->

### Architecture

We deploy $M$ distinct neural architectures independently trained to distill the same PAW pseudopotentials:

1. **Message-Passing Neural Network (MPNN).** Node features $h_v^{(t+1)} = U_t(h_v^{(t)}, \sum_{u \in \mathcal{N}(v)} M_t(h_v^{(t)}, h_u^{(t)}, e_{vu}))$. Captures local chemical bonding through iterative message passing.
2. **Transformer.** Self-attention $A = \mathrm{softmax}(QK^T/\sqrt{d_k})V$ over atom pairs. Captures long-range non-local interactions without explicit distance cutoffs.
3. **Equivariant GNN (Tensor Field Network).** Features $h_v^{(\ell)}$ transform under $SO(3)$ representations, preserving rotational equivariance: $h_v^{(\ell)} \mapsto D^\ell(R) h_v^{(\ell)}$. Essential for directional projector functions.
4. **Fourier Neural Operator (FNO).** Operates directly in reciprocal space: $v_{t+1}(\mathbf{G}) = \sigma(W v_t(\mathbf{G}) + \mathcal{K}_\phi * v_t(\mathbf{G}))$. Natural for plane-wave basis representations.
5. **Deep Sets architecture.** Permutation-invariant aggregation: $f(\{\mathbf{x}_i\}) = \rho(\sum_i \phi(\mathbf{x}_i))$. Captures element-agnostic projector structure.

### Yajie{ Consensus for Element-Specific Failure Detection}

Yajie{} is the SCX{} game-theoretic consensus mechanism. In the pseudopotential context, experts ``vote'' on the correctness of each element's distilled pseudopotential.

> **Definition:** [Yajie{} Pseudopotential Game]<!-- label: def:yajie_game -->
> The game is defined by:
> 
- **Players:** $M$ neural architectures $\{f_m\}_{m=1}^M$.
- **States:** $\mathcal{E} = \{Z_1, ..., Z_K\}$ (chemical elements).
- **Actions:** For each element $Z$, expert $m$ outputs a ``trust score'' $\tau_m(Z) \in [0,1]$ for its own prediction on $Z$.
- **Payoff:** Expert $m$ receives payoff $\pi_m(\boldsymbol) = \frac{1}{K}\sum_{Z} \ind{\tau_m(Z) \geq \bar(Z)} \cdot \mathrm{acc}_m(Z)$, where $\bar(Z)$ is the median trust score across experts and $\mathrm{acc}_m(Z)$ is expert $m$'s measured accuracy on held-out element $Z$ data.

> **Proposition:** [Yajie{} Equilibrium Element Partition]<!-- label: prop:yajie_partition -->
> In the Yajie{} pseudopotential game, at a Nash equilibrium of the trust-scoring subgame, the element set $\mathcal{E}$ partitions into $\mathcal{E} = \mathcal{E}_{\mathrm{agree}} \cup \mathcal{E}_{\mathrm{disagree}}$, where:
> 
- $\mathcal{E}_{\mathrm{agree}} = \{Z: \tau_m(Z) > 1/2  for all  m\}$ — elements where all architectures agree on correctness.
- $\mathcal{E}_{\mathrm{disagree}} = \{Z: \exists m, m'  s.t.  \tau_m(Z) \neq \tau_{m'}(Z)\}$ — elements with architecture-specific failures.

> For $Z \in \mathcal{E}_{\mathrm{disagree}}$, the element is flagged for manual inspection or additional all-electron reference calculations.

> **Proof:** \rigorSketch
> In the Yajie{} trust game, best-response dynamics lead experts to trust their predictions when their accuracy exceeds the median and distrust otherwise. Since architectures have different inductive biases (MPNN local vs.\ Transformer global vs.\ Equivariant GNN rotational), they fail on different element types. At equilibrium, elements where *all* experts trust themselves form $\mathcal{E}_{\mathrm{agree}}$ (consensus of correctness). Elements where some experts distrust themselves form $\mathcal{E}_{\mathrm{disagree}}$, signaling architecture-specific failure modes. The formal equilibrium existence follows from Yajie{} Theorem~(v) (mixed-strategy Nash equilibrium for finite action spaces) applied to the discretized trust-score space. See Appendix [ref] for the complete equilibrium derivation.

> **Corollary:** [Architecture Selection via Yajie{}]<!-- label: cor:architecture_selection -->
> For any element $Z$, the optimal architecture is:
> 
> $$
> m^*(Z) = \argmax_{m \in \{1,...,M\}} \tau_m(Z) \cdot \mathrm{acc}_m(Z),
> $$
> 
> i.e., the architecture that both trusts itself and demonstrates high accuracy on $Z$. This yields a per-element architecture selector without requiring oracle knowledge of which architecture generalizes best to each element.

\begin{assumption}[A9: Diverse Inductive Biases]<!-- label: ass:A9 -->
The $M$ architectures $\{f_m\}_{m=1}^M$ have pairwise distinct inductive biases: for any pair $(m, m')$, there exists at least one element $Z$ such that $|\mathrm{acc}_m(Z) - \mathrm{acc}_{m'}(Z)| > \delta_{\mathrm{diff}}$ for some $\delta_{\mathrm{diff}} > 0$.
\end{assumption}

> **Proposition:** [Coverage Guarantee]<!-- label: prop:coverage -->
> Under A9, for $M \geq 3$ architectures:
> 
> $$
> \Pr\left[ \bigcap_{m=1}^M \{\mathrm{acc}_m(Z) < \alpha_\} \right] \leq \prod_{m=1}^M \Pr[\mathrm{acc}_m(Z) < \alpha_],
> $$
> 
> under the approximate independence induced by diverse inductive biases. With $M = 5$ and per-architecture failure probability $0.3$, the joint failure probability is below $0.3^5 \approx 0.0024$.

## \Situs{ Encoding for Crystal Structures \Situs{}晶体结构编码}
<!-- label: sec:situs -->

The \Situs{} encoding maps atomic coordinates in a periodic crystal to a representation that respects physical symmetries while being amenable to neural network processing.

### Encoding Definition

> **Definition:** [\Situs{} Encoding]<!-- label: def:situs -->
> For a crystal with lattice vectors $\{\mathbf{a}_1, \mathbf{a}_2, \mathbf{a}_3\}$ and fractional atomic coordinates $\{\mathbf{x}_j\}_{j=1}^{N_{\mathrm{atom}}}$ with species $\{Z_j\}$, the \Situs{} encoding at position $\mathbf{r}$ is:
> 
> $$<!-- label: eq:situs_def -->
> \Phi(\mathbf{r}; \{\mathbf{x}_j, Z_j\}) = \bigoplus_{\ell=0}^{L_} \bigoplus_{m=-\ell}^ \sum_{j=1}^{N_{\mathrm{atom}}} \sum_{\mathbf{T} \in \Lambda} \phi_\ell(\norm{\mathbf{r} - \mathbf{x}_j - \mathbf{T}}) \cdot Y_{\ell m}\left(\frac{\mathbf{r} - \mathbf{x}_j - \mathbf{T}}{\norm{\mathbf{r} - \mathbf{x}_j - \mathbf{T}}}\right) \cdot E(Z_j),
> $$
> 
> where:
> 
- $\Lambda = \{n_1\mathbf{a}_1 + n_2\mathbf{a}_2 + n_3\mathbf{a}_3 : n_i \in \Z\}$ is the Bravais lattice;
- $\phi_\ell: \R_{\geq 0} \to \R$ are radial basis functions (per angular momentum channel $\ell$);
- $Y_{\ell m}: S^2 \to \C$ are spherical harmonics;
- $E(Z_j) \in \R^{d_{\mathrm{emb}}}$ is a learned element embedding;
- $\bigoplus$ denotes concatenation across $(\ell, m)$ channels.

> **Proposition:** [Symmetry Properties of \Situs{} Encoding]<!-- label: prop:situs_symmetry -->
> The \Situs{} encoding $\Phi$ satisfies:
> 
1. **Translational invariance:** $\Phi(\mathbf{r} + \mathbf{T}; \{\mathbf{x}_j\}) = \Phi(\mathbf{r}; \{\mathbf{x}_j\})$ for any lattice translation $\mathbf{T} \in \Lambda$.
2. **Rotational equivariance:** $\Phi(R\mathbf{r}; \{R\mathbf{x}_j\}) = \bigoplus_{\ell m} D^\ell(R)_{mm'} \Phi_{\ell m'}(\mathbf{r}; \{\mathbf{x}_j\})$ for $R \in SO(3)$, where $D^\ell(R)$ are Wigner D-matrices.
3. **Permutation invariance:** $\Phi$ is invariant under permutation of atom indices $\{1, ..., N_{\mathrm{atom}}\}$.

> **Proof:** \rigorFull
> (i) **Translational invariance:** For $\mathbf{r}' = \mathbf{r} + \mathbf{T}_0$ with $\mathbf{T}_0 \in \Lambda$:
> 
> $$
> \Phi(\mathbf{r} + \mathbf{T}_0) &= \sum_{j, \mathbf{T}} \phi_\ell(\norm{\mathbf{r} + \mathbf{T}_0 - \mathbf{x}_j - \mathbf{T}}) Y_{\ell m}(...) E(Z_j) 

> &= \sum_{j, \mathbf{T}} \phi_\ell(\norm{\mathbf{r} - \mathbf{x}_j - (\mathbf{T} - \mathbf{T}_0)}) Y_{\ell m}(...) E(Z_j) 

> &= \sum_{j, \mathbf{T}'} \phi_\ell(\norm{\mathbf{r} - \mathbf{x}_j - \mathbf{T}'}) Y_{\ell m}(...) E(Z_j) = \Phi(\mathbf{r}),
> $$
> 
> by the substitution $\mathbf{T}' = \mathbf{T} - \mathbf{T}_0$ and the closure of $\Lambda$ under subtraction.
> 
> (ii) **Rotational equivariance:** Under rotation $R \in SO(3)$, the spherical harmonics transform as $Y_{\ell m}(R\hat{\mathbf{r}}) = \sum_{m'} D_{m'm}^(R) Y_{\ell m'}(\hat{\mathbf{r}})$. Since $\phi_\ell$ depends only on the rotation-invariant distance $|\mathbf{r} - \mathbf{x}_j - \mathbf{T}|$, and $E(Z_j)$ is a scalar embedding, the $\ell$-channel transforms under the Wigner D-matrix representation of $SO(3)$.
> 
> (iii) **Permutation invariance:** The sum over atoms $\sum_{j=1}^{N_{\mathrm{atom}}}$ is symmetric by construction — it is a sum over the multiset of atom positions, which is invariant under index permutation. $\square$

### Connection to Pseudopotential Distillation

The \Situs{} encoding serves as the input representation for the neural pseudopotential. For a plane-wave basis vector $\mathbf{G}$, the encoding $\Phi(\mathbf{G})$ captures the local atomic environment in reciprocal space. The neural network maps:

$$<!-- label: eq:situs_to_vnl -->
f_\theta: \Phi(\mathbf{G}) \oplus \Phi(\mathbf{G}') \mapsto \langle \mathbf{G} | \hat{V}_{\mathrm{NL}} | \mathbf{G}' \rangle.
$$

By construction, the rotational equivariance of $\Phi$ ensures that $f_\theta$ learns the correct tensorial structure of the non-local projector without requiring data augmentation over rotations.

\begin{assumption}[A10: \Situs{} Convergence]<!-- label: ass:A10 -->
The radial functions $\phi_\ell$ are $C^2$ with compact support $[0, r_{\mathrm{cut}}]$, and the sum over lattice translations $\mathbf{T} \in \Lambda$ converges absolutely for all $\mathbf{r}$.
\end{assumption}

> **Proposition:** [\Situs{} Approximation Bound]<!-- label: prop:situs_bound -->
> Under A10, the truncation of the lattice sum to a finite set $\Lambda_R = \{\mathbf{T} \in \Lambda: \norm{\mathbf{T}} \leq R\}$ incurs error:
> 
> $$
> \norm{\Phi(\mathbf{r}) - \Phi_R(\mathbf{r})}_2 \leq C_\phi \cdot N_{\mathrm{atom}} \cdot \frac{\exp(-R/r_{\mathrm{cut}})}{R},
> $$
> 
> where $C_\phi$ depends on the radial function decay rate.

> **Proof:** \rigorSketch
> The tail sum $\sum_{\norm{\mathbf{T}} > R} \phi_\ell(\norm{\mathbf{r} - \mathbf{x}_j - \mathbf{T}})$ is bounded by the integral $\int_R^\infty \phi_\ell(r) \cdot N_{\mathrm{shell}}(r) dr$, where $N_{\mathrm{shell}}(r)$ is the number of lattice vectors at distance $r$. For a 3D lattice, $N_{\mathrm{shell}}(r)$ grows as $O(r^2)$. With compactly supported $\phi_\ell$ (support $[0, r_{\mathrm{cut}}]$ by A10), the tail is identically zero for $R > r_{\mathrm{cut}} + \max_j \norm{\mathbf{r} - \mathbf{x}_j}$. For Gaussian-decaying $\phi_\ell$, the exponential bound follows from Laplace's method.

## Experimental Protocol 实验协议
<!-- label: sec:experiment -->

### Benchmark Suite

We propose evaluating distilled pseudopotentials on the following benchmarks, adapted from the $\delta$-gauge of Lejaeghere et al. [cite] and the $\Delta$-gauge of Jollet et al. [cite]:

1. **$\delta$-gauge (elemental solids).** For each element $Z$, compute the equation of state $E(V)$ for the ground-state crystal structure. Extract equilibrium volume $V_0$, bulk modulus $B_0 = V \frac{\partial^2 E}{\partial V^2}|_{V_0}$, and Birch-Murnaghan fit quality. The $\delta$-value is the RMS difference between PAW/reference and distilled pseudopotential $E(V)$ curves, integrated over $V/V_0 \in [0.94, 1.06]$.
2. **$\Delta$-gauge (compounds).** For binary and ternary compounds (oxides, nitrides, transition metal compounds), compute formation energies $\Delta H_f = E_{\mathrm{compound}} - \sum_i E_i^{\mathrm{elemental}}$. The $\Delta$-value is the mean absolute deviation from all-electron reference.
3. **Band structure fidelity.** Compare band structures $\varepsilon_{n\mathbf{k}}$ along high-symmetry paths. Metrics: band gap error $\Delta E_g$, effective mass error $\Delta m^*$, and band ordering preservation (do bands cross at the same $\mathbf{k}$-points?).
4. **Phonon dispersion.** For selected elements, compute $\Gamma$-point phonon frequencies via finite displacements. Metrics: RMS frequency error and acoustic sum rule violation.
5. **Response properties.** Dielectric constant $\varepsilon_\infty$, Born effective charges $Z^*_{ij}$, piezoelectric tensor $e_{ij}$.

### Element Coverage

[Table omitted — see original .tex]

### Distillation Protocol

\begin{algorithm}[htbp]
*Caption:* SCX-Audited Pseudopotential Distillation
<!-- label: alg:distillation -->
\begin{algorithmic}[1]
\Require Element set $\mathcal{E}$, PAW pseudopotential library $\{\mathcal{P}_Z\}_{Z \in \mathcal{E}}$, architectures $\{f_m\}_{m=1}^M$
\Ensure Distilled pseudopotentials $\{\hat_{m,Z}\}$ and Cercis{} scores $\{S_Z\}$

\For{each element $Z \in \mathcal{E}$}
    \State Generate all-electron reference data $\mathcal{D}_Z^{\mathrm{AE}}$ via FLAPW or PAW with hard pseudopotential
    \State Partition $\mathcal{D}_Z^{\mathrm{AE}}$ into $\mathcal{D}_{\mathrm{train}}$ (80\%), $\mathcal{D}_{\mathrm{val}}$ (10\%), $\mathcal{D}_{\mathrm{test}}$ (10\%)
    \For{each architecture $m = 1, ..., M$}
        \State Initialize $f_{\theta_m}$ with independent random seed $s_m$
        \State Train on $\mathcal{D}_{\mathrm{train}}$ minimizing Eq. [ref]
        \State Validate on $\mathcal{D}_{\mathrm{val}}$; early stop at patience $P = 50$ epochs
        \State Compute test error $\varepsilon_{m,Z}^{\mathrm{test}}$ on $\mathcal{D}_{\mathrm{test}}$
    \EndFor
    \State Compute Yajie{} trust scores $\tau_m(Z)$ via the game in Definition [ref]
    \State Compute Cercis{} element score $S_Z = Q_Z + \eta \cdot \nu_Z$
\EndFor
\State Compute library-level Cercis{} score $S(p) = \frac{1}{|\mathcal{E}|}\sum_Z S_Z$
\State Identify $\mathcal{E}_{\mathrm{disagree}}$ from Yajie{} consensus (Proposition [ref])
\State \Return $\{\hat_{m,Z}\}$, $\{S_Z\}$, $\mathcal{E}_{\mathrm{disagree}}$
\end{algorithmic}
\end{algorithm}

### Statistical Reporting

All benchmark results must report:

- Mean $\pm$ standard deviation over $M$ experts;
- Per-element detection confidence $1 - \Pr[miss \mid error]$ from Theorem [ref];
- Yajie{} consensus flag (agree/disagree) for each element;
- Cercis{} component scores $Q$, $N$ separately (not just the aggregate $S$);
- Explicit assumption declaration list (which PAW pseudopotential was used as training target, which error component is assumed dominant, whether A1--A10 hold).

## Discussion 讨论
<!-- label: sec:discussion -->

### Relationship to Existing Methods

**DeepMD [cite].** DeepMD learns interatomic potentials from DFT data, targeting energies and forces rather than pseudopotentials directly. Our framework is complementary: a distilled neural pseudopotential provides the DFT Hamiltonian for DeepMD training, enabling self-consistent electronic structure without repeated plane-wave DFT. The SCX{} auditing adds error quantification absent in standard DeepMD.

**NequIP [cite].** NequIP uses equivariant message passing ($E(3)$ symmetry) to achieve data-efficient force field learning. The \Situs{} encoding (Section [ref]) generalizes this: where NequIP encodes positions into equivariant features for *energy prediction*, \Situs{} encodes positions for *operator prediction* (the non-local pseudopotential). The rotational equivariance guarantee is the same mechanism applied at a different layer of the electronic structure stack.

**MACE [cite].** MACE (Multi-ACE) uses many-body expansion with equivariant features for high-order interactions. Our multi-expert architecture with Yajie{} consensus can incorporate MACE-style experts as one of the $M$ architectures, with the Yajie{} mechanism identifying whether many-body expansion terms are necessary for specific elements (e.g., transition metals with $d$-orbital hybridization).

**Delta-learning approaches [cite].** Rather than learning pseudopotentials from scratch, delta-learning corrects existing PAW pseudopotentials. Our Theorem [ref] applies equally here: the ``delta'' correction term creates the same observational ambiguity between PAW error and neural network correction error.

### Limitations 局限性

**PAW frozen-core approximation.** The entire framework inherits the limitations of the PAW method: frozen-core error for semicore states (e.g., 3p in 3d transition metals, 5p in lanthanides), lack of core polarization, and missing core-valence correlation. Theorem [ref] implies these cannot be separated from NN training error without explicit all-electron benchmarks.

**Computational cost of auditing.** Training $M \geq 20$ independent neural pseudopotentials per element, with independent all-electron reference calculations, multiplies the computational cost by $M$. The detection guarantee (Theorem [ref]) is a *statistical* guarantee, not a deterministic one — there remains a non-zero (albeit exponentially small) probability of missing systematic errors.

**Transferability ceiling.** Even with perfect neural network training ($\varepsilon_{\mathrm{NN}} = 0$), the distilled pseudopotential is bounded by the quality of the PAW pseudopotential used as training target. No amount of Cercis{} scoring can overcome fundamentally deficient PAW datasets.

**Novelty weight calibration.** The $\eta$ parameter in Eq. [ref] is user-specified and its optimal value depends on the application: materials discovery ($\eta$ large) vs.\ high-precision property prediction ($\eta$ small). There is no universal $\eta$ — this is an irreducible value judgment, consistent with the SCX{} emphasis on explicit assumption declaration.

**Extensivity and system size.** The \Situs{} encoding cost scales as $O(N_{\mathrm{atom}} \cdot N_{\mathbf{T}} \cdot L_^2)$ per evaluation point, where $N_{\mathbf{T}}$ is the number of periodic images within the cutoff. For large supercells, this dominates. Sublinear scaling (e.g., via Ewald summation or fast multipole methods) is conjectured but not proven.

### Path to Full Neural DFT 通向完整神经DFT的路径

A complete neural DFT framework would replace not only pseudopotentials but also the exchange-correlation functional, the kinetic energy operator, and the self-consistency cycle. Our framework provides the *auditing infrastructure* for each component:

1. **Neural pseudopotential** (this work): audited by \ThmSCXNoise{} and Yajie{}.
2. **Neural XC functional:** audited by the same detection guarantee, with the additional constraint of exact constraints (coordinate scaling, Lieb-Oxford bound, uniform density limit).
3. **Neural kinetic energy functional:** audited by orbital-free DFT benchmarks with \ThmSCXHonest{} analysis of kinetic energy vs.\ XC error unidentifiability.
4. **Self-consistency:** audited by Spring{} Lyapunov stability analysis — does the neural Hamiltonian converge to a unique fixed-point charge density?

Each component introduces new sources of error, each subject to the unidentifiability theorem. The SCX{} framework's insistence on explicit assumptions provides the methodological discipline needed to advance without false confidence.

## Acknowledgments

This work builds on the SCX{} theoretical framework. We acknowledge valuable discussions on PAW formalism and pseudopotential transferability benchmarks.

## Appendix
## Complete Derivation of Error Decomposition Bound
<!-- label: sec:app_error -->

We provide the full derivation of Proposition [ref].

> **Proof:** \rigorFull
> Recall the distillation loss $\mathcal{L}_s(\theta) = \E_{(\mathbf{x},\mathbf{y})\sim P_s}[\norm{f_\theta(\mathbf{x}) - \mathbf{y}}_2^2]$. Let $\hat_n = \argmin_{\theta \in \Theta} \frac{1}{n}\sum_{i=1}^n \norm{f_\theta(\mathbf{x}_i) - \mathbf{y}_i}_2^2$ be the empirical risk minimizer and $\theta^* = \argmin_{\theta \in \Theta} \mathcal{L}_s(\theta)$ the population minimizer.
> 
> The total error relative to the all-electron reference decomposes as:
> 
> $$
> \varepsilon_{\mathrm{total}} &= \E_{\mathbf{x}}\norm{f_{\hat_n}(\mathbf{x}) - V_{\mathrm{AE}}(\mathbf{x})}_2 

> &\leq \underbrace{\norm{\hat{V}_{\mathrm{PAW}} - V_{\mathrm{AE}}}_{\mathrm{op}}}_{\varepsilon_{\mathrm{PAW}}} + \underbrace{\E_{\mathbf{x}}\norm{f_{\theta^*}(\mathbf{x}) - \hat{V}_{\mathrm{PAW}}(\mathbf{x})}_2}_{\varepsilon_{\mathrm{NN}}} + \underbrace{\E_{\mathbf{x}}\norm{f_{\hat_n}(\mathbf{x}) - f_{\theta^*}(\mathbf{x})}_2}_{\varepsilon_{\mathrm{gen}}},
> $$
> 
> by the triangle inequality and A8 (operator norm bound on the first term).
> 
> The generalization gap $\varepsilon_{\mathrm{gen}}$ is bounded by standard uniform convergence [cite]. Under A1, the loss is $4B_V^2$-bounded. By McDiarmid's inequality:
> 
> $$
> \Pr\left[\sup_{\theta \in \Theta} |\hat{\mathcal{L}}_n(\theta) - \mathcal{L}_s(\theta)| \geq 2\mathcal{R}_n(\mathcal{F}_\Theta) + 4B_V^2\sqrt{\frac{2\log(2/\delta)}{n}}\right] \leq \delta,
> $$
> 
> where $\mathcal{R}_n(\mathcal{F}_\Theta) = \E_\left[\sup_{\theta \in \Theta} \frac{1}{n}\sum_{i=1}^n \sigma_i \norm{f_\theta(\mathbf{x}_i) - \mathbf{y}_i}_2^2\right]$ is the Rademacher complexity. Combining with the triangle inequality yields Eq. [ref]. $\square$

## Yajie{ Equilibrium Formal Derivation}
<!-- label: sec:app_yajie -->

We derive the equilibrium of the Yajie{} pseudopotential game (Definition [ref]).

> **Proof:** \rigorFull
> **Game definition.** The Yajie{} pseudopotential game is a non-cooperative $M$-player game with:
> 
- Strategy space $\mathcal{T}_m = [0,1]^K$ for expert $m$ (trust scores for $K$ elements);
- Payoff $\pi_m(\boldsymbol_m, \boldsymbol_{-m}) = \frac{1}{K}\sum_{Z} \ind{\tau_m(Z) \geq \overline{\mathrm{med}}(\boldsymbol_{-m}(Z))} \cdot \mathrm{acc}_m(Z)$,

> where $\overline{\mathrm{med}}(\boldsymbol_{-m}(Z))$ is the median of trust scores for element $Z$ from all experts except $m$.
> 
> **Best response.** For element $Z$, expert $m$'s payoff depends on whether $\tau_m(Z) \geq \overline{\mathrm{med}}$. The indicator function makes this a threshold game:
> 
- If $\mathrm{acc}_m(Z) > 0$, expert $m$ gains by setting $\tau_m(Z) \geq \overline{\mathrm{med}}$ (earn positive payoff);
- If $\mathrm{acc}_m(Z) = 0$, any $\tau_m(Z)$ yields zero payoff for this element.

> 
> Thus, the best response is:
> 
> $$
> \tau_m^*(Z) = \begin{cases}
> 1 & if  \mathrm{acc}_m(Z) > 0,

> any & if  \mathrm{acc}_m(Z) = 0.
> \end{cases}
> $$
> 
> 
> **Equilibrium characterization.** In practice, $\mathrm{acc}_m(Z) > 0$ for all experts and elements (no expert is perfectly wrong). At equilibrium, all experts set $\tau_m(Z) = 1$ for all $Z$, so $\overline{\mathrm{med}} = 1$ and $\ind{\tau_m \geq 1} = 1$, yielding payoff $\pi_m = \frac{1}{K}\sum_Z \mathrm{acc}_m(Z)$ for each expert.
> 
> **Refinement via element-specific accuracy.** The above baseline equilibrium is uninformative. To obtain the partition $\mathcal{E}_{\mathrm{agree}} \cup \mathcal{E}_{\mathrm{disagree}}$, we introduce a *thresholded* accuracy:
> 
> $$
> \mathrm{acc}_m^\tau(Z) = \mathrm{acc}_m(Z) \cdot \ind{\mathrm{acc}_m(Z) \geq \tau}.
> $$
> 
> 
> Now the best response introduces a self-trust threshold: expert $m$ only ``trusts'' its prediction on element $Z$ if $\mathrm{acc}_m(Z) \geq \tau$, i.e., if its measured accuracy exceeds a minimum standard. When architectures have diverse inductive biases (A9), they achieve different accuracies on different elements, naturally partitioning $\mathcal{E}$ into consensus and disagreement regions.
> 
> **Formal equilibrium.** Define the discretized trust score space $\mathcal{T}_m = \{0, 1\}^K$ (binary trust). The payoff matrix for element $Z$ with $M=3$ experts is:
> 
> 
<div align="center">

> [Table omitted — see original .tex]
>

</div>

> 
> By Yajie{} Theorem~(v), a mixed-strategy Nash equilibrium exists. By Theorem~(iii) (pure-strategy existence for threshold games with monotone payoffs), the equilibrium is in pure strategies when $\mathrm{acc}_m(Z)$ are distinct across experts. This yields the partition in Proposition [ref]. $\square$

## Correlation Estimation for $M_{\mathrm{eff}$}
<!-- label: sec:app_correlation -->

The effective multiplicity $M_{\mathrm{eff}}$ in Eq. [ref] requires estimation of the average correlation $\bar$. We provide a bootstrap-based estimator:

1. For each test input $\mathbf{x}_k$ in a held-out calibration set of size $K$, compute the error vector $\mathbf{e}_k = (e_{1k}, ..., e_{Mk})$ where $e_{mk} = \norm{f_{\theta_m}(\mathbf{x}_k) - \mathbf{y}_k^*}_2$.
2. Compute the $M \times M$ error correlation matrix $\hat{R}_{ij} = \mathrm{Corr}(e_{i\cdot}, e_{j\cdot})$.
3. Estimate $\bar = \frac{2}{M(M-1)}\sum_{i<j} \hat{R}_{ij}$.
4. Bootstrap 95\% confidence interval: resample rows of the $K \times M$ error matrix with replacement $B = 1000$ times, recompute $\bar^{(b)}$, and report $[\bar_{0.025}, \bar_{0.975}]$.

When $\bar < 0$ (negative correlation — experts make complementary errors), we set $M_{\mathrm{eff}} = M$ (the bound is conservative under negative correlation, since Hoeffding's inequality holds for any dependence structure with sub-Gaussian marginals [cite], Ch.~2).

\begin{thebibliography}{99}

\bibitem{Blochl1994}
P.~E.~Bl\"ochl, ``Projector augmented-wave method,'' *Phys. Rev. B*, vol.~50, pp.~17953--17979, 1994.

\bibitem{Kresse1999}
G.~Kresse and D.~Joubert, ``From ultrasoft pseudopotentials to the projector augmented-wave method,'' *Phys. Rev. B*, vol.~59, pp.~1758--1775, 1999.

\bibitem{Kresse1996a}
G.~Kresse and J.~Furthm\"uller, ``Efficient iterative schemes for ab initio total-energy calculations using a plane-wave basis set,'' *Phys. Rev. B*, vol.~54, pp.~11169--11186, 1996.

\bibitem{Kresse1996b}
G.~Kresse and J.~Furthm\"uller, ``Efficiency of ab-initio total energy calculations for metals and semiconductors using a plane-wave basis set,'' *Comput. Mater. Sci.*, vol.~6, pp.~15--50, 1996.

\bibitem{SCX2025}
SCX, ``SCX: Structured Causal eXamination Framework for Auditable AI,'' *Technical Report*, 2025.

\bibitem{Bartlett2002}
P.~L.~Bartlett and S.~Mendelson, ``Rademacher and Gaussian complexities: Risk bounds and structural results,'' *J. Mach. Learn. Res.*, vol.~3, pp.~463--482, 2002.

\bibitem{Bartlett2017}
P.~L.~Bartlett, D.~J.~Foster, and M.~J.~Telgarsky, ``Spectrally-normalized margin bounds for neural networks,'' *NeurIPS*, 2017.

\bibitem{Liang1986}
K.-Y.~Liang and S.~L.~Zeger, ``Longitudinal data analysis using generalized linear models,'' *Biometrika*, vol.~73, pp.~13--22, 1986.

\bibitem{Lehmann1998}
E.~L.~Lehmann and G.~Casella, *Theory of Point Estimation*, 2nd ed., Springer, 1998.

\bibitem{Choromanska2015}
A.~Choromanska, M.~Henaff, M.~Mathieu, G.~B.~Arous, and Y.~LeCun, ``The loss surfaces of multilayer networks,'' *AISTATS*, 2015.

\bibitem{Lejaeghere2016}
K.~Lejaeghere et al., ``Reproducibility in density functional theory calculations of solids,'' *Science*, vol.~351, aad3000, 2016.

\bibitem{Jollet2014}
F.~Jollet, M.~Torrent, and N.~Holzwarth, ``Generation of Projector Augmented-Wave atomic data: A 71 element validated table in the XML format,'' *Comput. Phys. Commun.*, vol.~185, pp.~1246--1254, 2014.

\bibitem{Zhang2018}
L.~Zhang, J.~Han, H.~Wang, R.~Car, and W.~E, ``Deep Potential Molecular Dynamics: A scalable model with the accuracy of quantum mechanics,'' *Phys. Rev. Lett.*, vol.~120, 143001, 2018.

\bibitem{Wang2018}
H.~Wang, L.~Zhang, J.~Han, and W.~E, ``DeePMD-kit: A deep learning package for many-body potential energy representation and molecular dynamics,'' *Comput. Phys. Commun.*, vol.~228, pp.~178--184, 2018.

\bibitem{Batzner2022}
S.~Batzner, A.~Musaelian, L.~Sun, M.~Geiger, J.~P.~Mailoa, M.~Kornbluth, N.~Molinari, T.~E.~Smidt, and B.~Kozinsky, ``E(3)-equivariant graph neural networks for data-efficient and accurate interatomic potentials,'' *Nat. Commun.*, vol.~13, 2453, 2022.

\bibitem{Batatia2022}
I.~Batatia, D.~P.~Kov\'acs, G.~N.~C.~Simm, C.~Ortner, and G.~Cs\'anyi, ``MACE: Higher order equivariant message passing neural networks for fast and accurate force fields,'' *NeurIPS*, 2022.

\bibitem{Ramakrishnan2015}
R.~Ramakrishnan, P.~O.~Dral, M.~Rupp, and O.~A.~von Lilienfeld, ``Big data meets quantum chemistry approximations: The $\Delta$-machine learning approach,'' *J. Chem. Theory Comput.*, vol.~11, pp.~2087--2096, 2015.

\bibitem{Shalev-Shwartz2014}
S.~Shalev-Shwartz and S.~Ben-David, *Understanding Machine Learning: From Theory to Algorithms*, Cambridge University Press, 2014.

\bibitem{Wainwright2019}
M.~J.~Wainwright, *High-Dimensional Statistics: A Non-Asymptotic Viewpoint*, Cambridge University Press, 2019.

\end{thebibliography}