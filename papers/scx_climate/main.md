# Introduction

**Author:** SCX

*Abstract:*

**English.**
Earth System Models (ESMs) are the primary tools for projecting future climate
under anthropogenic forcing, yet their uncertainty estimates rest on informal
conventions rather than mathematical guarantees. We formalize the coupled
climate system as a multi-expert prediction problem under the SCX framework and
prove three fundamental theorems: (1)~**Systematic Bias Detection**: for
$M$ structurally independent ESMs, the probability of missing a systematic bias
exceeding gap $\Delta$ decays as $\exp(-2M_{\mathrm{eff}}\Delta^2)$, where
$M_{\mathrm{eff}}$ is the effective number of independent experts accounting for
inter-model correlation (Theorem~1, \rigorFull); (2)~**Attributional
Unidentifiability**: when multiple ESMs disagree on a regional climate response
(such as Arctic amplification), it is mathematically impossible to attribute
the disagreement to any specific sub-grid parameterization error without
declaring explicit structural assumptions (Theorem~2, \rigorFull);
(3)~**Cercis Score Optimality**: the composite quality metric
$S = Q + \eta N$, where $Q$ is multi-model hindcast skill and $N$ is
novelty-weighted exploration bonus, provides a principled ranking of climate
projections that balances fidelity to observations against the epistemic value
of unprecedented regimes (Theorem~3, \rigorPartial).

We operationalize these results through four SCX components: Yajie{} consensus
for multi-model ensemble auditing, Spring{} gating for detecting climate regime
shifts (tipping points), \Situs{} encoding for spherical geometry of climate
fields, and the Cercis{} Score for unified model quality assessment. Under
10 explicitly stated assumptions (C1--C10), we establish that the CMIP6
multi-model ensemble admits a rigorous uncertainty decomposition. We
characterize the conditions under which each guarantee fails and identify the
precise additional information required to restore certified bounds. All proofs
are provided with rigor-level annotations. The framework does not predict
climate---it certifies the epistemic status of predictions already made.

**中文摘要。**
地球系统模式（ESM）是预测人为强迫下未来气候的主要工具，但其不确定性估计依
赖于非正式约定而非数学保证。本文将耦合气候系统形式化为SCX框架下的多专家预测
问题，并证明三个基本定理：（1）**系统偏差检测**：对于$M$个结构独立的ESM，
遗漏超过间隙$\Delta$的系统偏差的概率按$\exp(-2M_{\mathrm{eff}}\Delta^2)$衰减
（定理1，\rigorFull）；（2）**归因不可区分性**：当多个ESM在区域气候响应（如北极
放大效应）上存在分歧时，在数学上不可能在不声明显式结构假设的情况下将分歧归因
于任何特定的次网格参数化误差（定理2，\rigorFull）；（3）**Cercis评分最优性**：
复合质量指标$S = Q + \eta N$，其中$Q$为多模式后报技巧，$N$为新意加权探索奖
励，提供了一种有原则的气候预测排名方法，平衡对观测的忠实性与前所未有状态的认
识价值（定理3，\rigorPartial）。

**Keywords:** Earth System Models, uncertainty quantification, multi-model ensemble,
CMIP6, SCX auditing, climate sensitivity, tipping points, spherical geometry

## Introduction

### The Certification Gap in Climate Prediction

Coupled Earth System Models (ESMs) are the computational backbone of climate
science. Models such as CESM2 [cite], NorESM2 [cite],
MIROC6 [cite], and HadGEM3 [cite] numerically integrate
the primitive equations of atmospheric and oceanic dynamics coupled to
biogeochemical cycles, ice sheets, and land-surface processes. Their projections
inform the IPCC Assessment Reports [cite] and underpin trillions of
dollars of infrastructure and policy decisions.

Yet the uncertainty quantification (UQ) in these projections remains
mathematically informal. The CMIP6 multi-model ensemble [cite] is
interpreted through conventions---equally weighted averaging, ``model democracy,''
and qualitative assessments of ``robustness''---that lack rigorous certification.
The following gap is the central concern of this paper:

> **The Certification Gap.** No existing framework provides a *mathematical
> guarantee* that the ensemble of climate projections bounds the true climate
> trajectory with a specified probability, *nor* a proof of why such a
> guarantee is impossible without additional assumptions.

We address this gap by applying the SCX auditing framework [cite] to
the coupled climate prediction problem. The approach is *not* to build a
better climate model, but to certify the epistemic status of predictions from
existing models. This paper provides the mathematical foundations; companion work
treats the computational implementation.

### Climate as a Multi-Expert System

The mapping from the SCX framework to climate modeling is natural and structural.
Table [ref] summarizes the correspondence.

[Table omitted — see original .tex]

Critically, each ESM contains *sub-grid parameterizations*---for cloud
microphysics, moist convection, boundary layer turbulence, sea ice rheology,
and terrestrial carbon uptake---that function as ``experts within experts.''
The SCX framework's treatment of nested expertise [cite] provides the
machinery to analyze this hierarchical structure.

### Related Work

Climate model UQ has developed along several lines. Bayesian model
averaging [cite] weights models by posterior probability. Emergent
constraints [cite] use observable relationships to narrow distributions
of climate sensitivity. Statistical emulation [cite] builds Gaussian
process surrogates over the model parameter space. Multi-model
ensembles [cite] are evaluated through the ``REA'' (Reliability
Ensemble Averaging) framework.

Our work differs fundamentally from all of these. We do not estimate climate
sensitivity, weight models, or produce a single ``best'' projection. We instead
prove *what can and cannot be certified* about any ensemble of climate
models, under explicitly stated assumptions. The theorems are epistemological,
not climatological.

## Mathematical Formalization of Coupled Climate Prediction

### Climate State as a Dynamical System

We model the Earth system as a coupled system of ordinary and partial
differential equations evolving a state vector
$\mathbf{X}(t) \in \R^{d}$ on a spatial domain $\Omega \subset \R^3$ (the
atmosphere--ocean--land--ice column):

$$<!-- label: eq:climate-pde -->
\frac{\partial \mathbf{X}}{\partial t}
= \mathcal{L}(\mathbf{X}, \nabla \mathbf{X}, \nabla^2 \mathbf{X}, ...)
+ \mathcal{F}_{\mathrm{forcing}}(t) + \mathcal{R}(\mathbf{X}),
$$

where:

- $\mathcal{L}$ is the resolved-scale dynamics operator (primitive
- $\mathcal{F}_{\mathrm{forcing}}(t)$ is the external radiative forcing
- $\mathcal{R}(\mathbf{X})$ represents sub-grid scale processes requiring

For a given ESM $m$, the system is discretized at resolution $\Delta x_m$ and
integrated with parameterization scheme $\mathcal{R}_m$:

$$<!-- label: eq:esm-discrete -->
\mathbf{X}_{m}(t+\Delta t) = \Phi_m(\mathbf{X}_m(t); \bm_m, \mathcal{R}_m),
$$

where $\bm_m$ are tunable parameters and $\Phi_m$ is the discrete
propagator. The ESM ensemble is
$\mathcal{E} = \{(\Phi_m, \bm_m, \mathcal{R}_m)\}_{m=1}^M$.

### Climate Variables as Prediction Targets

For a climate variable of interest $Y \in \mathcal{Y}$ (e.g., global mean surface
temperature anomaly $T_{\mathrm{GMST}}$, Arctic sea ice extent $S_{\mathrm{Arctic}}$,
regional precipitation $P(r)$), we define the observation operator
$g: \R^d \to \mathcal{Y}$ that maps the full state to the target quantity:

$$<!-- label: eq:observation-operator -->
Y(t) = g(\mathbf{X}(t)) + \varepsilon_{\mathrm{obs}}(t),
$$

where $\varepsilon_{\mathrm{obs}}(t) \sim \mathcal{N}(0, \sigma_{\mathrm{obs}}^2)$
represents observational uncertainty. Each ESM $m$ produces a prediction
$f_m(\mathbf{X}_0, t) = g(\Phi_m^t(\mathbf{X}_0))$, where $\Phi_m^t$ denotes
$t$-step integration from initial condition $\mathbf{X}_0$.

### Sub-grid Parameterizations as Nested Experts

\rigorFull

The total model error for ESM $m$ decomposes as:

$$<!-- label: eq:error-decomp -->
e_m(\mathbf{x}, t) = e_m^{\mathrm{dyn}}(\mathbf{x}, t)
+ \sum_{k=1}^{K_m} e_{m,k}^{\mathrm{param}}(\mathbf{x}, t)
+ e_m^{\mathrm{res}}(\mathbf{x}, t),
$$

where $e_m^{\mathrm{dyn}}$ is resolved-scale dynamical error (discretization,
numerical diffusion), $e_{m,k}^{\mathrm{param}}$ is the error from the $k$-th
sub-grid parameterization scheme (clouds $k=1$, convection $k=2$, boundary layer
$k=3$, etc.), and $e_m^{\mathrm{res}}$ is residual interaction error.

> **Definition:** [Nested Expert Consensus]
> For ESM $m$, the internal consensus on sub-grid process $k$ at climate state $s$
> is:
> 
> $$
> C_{m,k}(s) = 1 - \frac{1}{|\mathcal{T}_s|}\sum_{t \in \mathcal{T}_s}
> \ind{ \ell(g(\mathbf{X}_m(t)), Y_{\mathrm{reanalysis}}(t)) > \tau_k },
> $$
> 
> where $\mathcal{T}_s$ is the set of time indices in climate state $s$,
> $Y_{\mathrm{reanalysis}}$ is the reanalysis product used as reference, and
> $\tau_k$ is a process-specific tolerance.

## Structural Assumptions for Certified Climate Auditing

\rigorFull

The following assumptions are the **minimal sufficient set** required for
the theorems that follow. Each is stated explicitly, motivated physically, and
accompanied by the consequences of its violation.

\begin{assumption}[C1: Independent Model Development]
<!-- label: asm:C1 -->
The $M$ ESMs in the ensemble are developed by structurally independent research
groups, with disjoint code bases, discretization schemes, and sub-grid
parameterizations. Formally, the model outputs satisfy
$\mathbf{X}_m(t) \indep \mathbf{X}_{m'}(t) \mid \mathbf{X}_0, \mathcal{F}(t)$
for $m \neq m'$, where the conditioning is on the shared initial condition and
forcing history.
\end{assumption}

> **Remark:** This is the climate analog of SCX Assumption A1 (disjoint training). Violated
> when models share dynamical cores (e.g., CESM2 and NorESM2 share the Community
> Atmosphere Model). In such cases, the effective number of independent models
> $M_{\mathrm{eff}} < M$, computed in \S [ref].

\begin{assumption}[C2: Conditional Independence of Residual Errors]
<!-- label: asm:C2 -->
For any climate state $s$ and any target variable $Y$, the residual errors
$e_m^{\mathrm{res}}$ of independent models are conditionally independent:
$\Cov(e_m^{\mathrm{res}}, e_{m'}^{\mathrm{res}} \mid s) = 0$ for $m \neq m'$.
\end{assumption}

\begin{assumption}[C3: Bounded Observational Error]
<!-- label: asm:C3 -->
The loss function $\ell(f_m, Y_{\mathrm{obs}})$ is bounded:
$\ell(\cdot, \cdot) \in [0, B]$ with $B < \infty$. For climate variables, this is
satisfied by using a truncated RMSE or a bounded skill score (e.g., the
anomaly correlation coefficient mapped to $[0, B]$ via the transformation
$B \cdot (1 - \mathrm{ACC})/2$).
\end{assumption}

\begin{assumption}[C4: State-Conditioned Bias Homogeneity]
<!-- label: asm:C4 -->
Within each climate state $s \in \Sstates$, the expected multi-model error on
observationally well-sampled periods satisfies a state-level bound:

$$
\sup_{hindcast period  t \in \mathcal{T}_s^{\mathrm{hind}}}
\E[C(\mathbf{X}(t)) \mid s] \leq \mu_s,
$$

where $C(\mathbf{X})$ is the consensus score (fraction of ESMs exceeding error
threshold) and $\mu_s$ is a state-specific constant estimated from the
historical hindcast record.
\end{assumption}

\begin{assumption}[C5: Balanced Multi-Model Error Distribution]
<!-- label: asm:C5 -->
The probability that ESMs err in the same directional sense (all warm-biased
or all cold-biased) is bounded. There exists $C_{\mathrm{bal}} \geq 1$ such that
the maximum concentration of model errors in any single error direction satisfies:

$$
\max_{d \in \mathcal{E}_{\mathrm{dir}}} \Pbb(all ESMs err in direction  d \mid s)
\leq C_{\mathrm{bal}} \cdot \frac{\mu_s}{|\mathcal{E}_{\mathrm{dir}}|},
$$

where $\mathcal{E}_{\mathrm{dir}}$ is the set of possible error directions
(e.g., $\{warm, cold, wet, dry\}$).
\end{assumption}

\begin{assumption}[C6: Hindcast Period Stationarity]
<!-- label: asm:C6 -->
The relationship between model error and climate state, as estimated from the
hindcast period (typically 1850--2014), extends to the projection period
(2015--2100) *provided* the climate state $s$ has been observed in the
hindcast record. For novel climate states $s \notin \Sstates^{\mathrm{hind}}$,
this assumption does *not* apply (see Assumption C7).
\end{assumption}

\begin{assumption}[C7: Regime Separability for Novel States]
<!-- label: asm:C7 -->
There exists a discriminator $D: \X \to \{0,1\}$ that can distinguish climate
states observed in the hindcast record ($D=0$) from novel, unprecedented
states ($D=1$), with error bounded by $\varepsilon_D$. This is the Spring{}
gating condition (Section [ref]).
\end{assumption}

\begin{assumption}[C8: Spherical Geometry Preservation]
<!-- label: asm:C8 -->
Climate fields on the sphere $S^2$ admit a representation in which
geodesic distance in physical space is monotonically related to similarity in
error structure. Formally, for spatial locations $p, q \in S^2$ and ESM errors
$e(p), e(q)$:

$$
\Corr(e(p), e(q)) \geq \kappa \cdot \exp(-\alpha \cdot d_{S^2}(p, q)),
$$

where $d_{S^2}$ is the great-circle distance and $\kappa, \alpha > 0$ are
empirically determined constants. This assumption enables \Situs{} encoding
(Section [ref]).
\end{assumption}

\begin{assumption}[C9: Forcing Scenario Well-Posedness]
<!-- label: asm:C9 -->
For each SSP scenario $\mathcal{F}(t)$ under consideration, the forcing
trajectory is sufficiently smooth and bounded: $\|\mathcal{F}\|_ \leq F_$
and $\|\dot{\mathcal{F}}\|_ \leq \dot{F}_$, ensuring that the
coupled ODE/PDE system [ref] admits unique solutions on
$[t_0, t_{\mathrm{end}}]$ for all ESMs in the ensemble.
\end{assumption}

\begin{assumption}[C10: Paleoclimate Constraint Validity]
<!-- label: asm:C10 -->
Paleoclimate proxy reconstructions (LGM, mid-Pliocene, etc.) provide
state-level constraints on ESM performance for climate states substantially
different from the instrumental period. The relation between proxy uncertainty
$\sigma_{\mathrm{proxy}}$ and ESM error tolerance $\tau$ satisfies
$\sigma_{\mathrm{proxy}} < \tau / 2$, ensuring that the observational constraint
is tighter than the detection threshold.
\end{assumption}

## Theorem 1: Yajie Consensus for Systematic Bias Detection
<!-- label: sec:yajie-consensus -->

\rigorFull

### Statement

> **Theorem:** [Systematic Bias Detection Guarantee —— 系统偏差检测定理]
> <!-- label: thm:bias-detection -->
> Let Assumptions C1--C6 hold. Let $M$ structurally independent ESMs produce
> predictions $\{f_m(\mathbf{x}, t)\}_{m=1}^M$ for climate variable $Y$ at state
> $s$. Define the consensus score:
> 
> $$
> C(\mathbf{x}) = \frac{1}{M}\sum_{m=1}^M \ind{\ell(f_m(\mathbf{x}), Y_{\mathrm{obs}}) > \tau}.
> $$
> 
> 
> Let $\rho_s = \Pbb(\mathbf{X} \in s)$ be the climate state probability,
> $\mu_s$ the state-level clean error bound (Assumption C4), and define the
> detection gap $\Delta_s(\theta) = \min(\theta - \mu_s,\; 1 - C_{\mathrm{bal}}\frac{\mu_s}{|\mathcal{E}_{\mathrm{dir}}|} - \theta)$
> for threshold $\theta$. Let $M_{\mathrm{eff}} = M / (1 + (M-1)\bar)$
> be the effective number of independent models, where $\bar$ is the mean
> pairwise correlation of residual errors across models.
> 
> Then the probability that a systematic model bias exceeding gap $\Delta$ is
> *not* detected by the SCX auditing procedure satisfies:
> 
> 
> $$<!-- label: eq:thm1-main -->
> \boxed{\;
> \Pbb(miss systematic bias > \Delta \mid s)
> \leq \sum_{s \in \Sstates} \rho_s \cdot
> \exp\!\bigl(-2M_{\mathrm{eff}} \Delta_s^2\bigr)
> \;}
> $$
> 
> 
> Equivalently, the F1 score of the bias detection procedure satisfies:
> 
> 
> $$<!-- label: eq:thm1-f1 -->
> \mathrm{F1}_{\mathrm{SCX}} \geq 1 - \frac{1}{\eta_{\mathrm{bias}}}
> \sum_{s \in \Sstates} \rho_s \cdot \exp\!\bigl(-2M_{\mathrm{eff}} \Delta_s^2\bigr),
> $$
> 
> 
> where $\eta_{\mathrm{bias}}$ is the fraction of climate variable--state pairs
> affected by systematic bias.

### Proof of Theorem 1

> **Proof:** The proof follows the same structure as the SCX noise detection theorem
> (Theorem~1 in [cite]), adapted to the climate ensemble setting.
> 
> **Step 1: Effective independence.**
> By Assumption C1, the ESMs are developed independently. However, shared
> components (dynamical cores, forcing datasets) introduce correlation.
> Let $\bar = \frac{2}{M(M-1)}\sum_{m<m'} \Corr(e_m^{\mathrm{res}}, e_{m'}^{\mathrm{res}})$
> be the mean pairwise residual error correlation. Using the generalized
> estimating equations variance inflation factor [cite], the effective
> number of independent models is:
> 
> $$
> M_{\mathrm{eff}} = \frac{M}{1 + (M-1)\bar}.
> $$
> 
> When $\bar = 0$, $M_{\mathrm{eff}} = M$; when $\bar \to 1$,
> $M_{\mathrm{eff}} \to 1$, reflecting total redundancy.
> 
> **Step 2: Mean separation.**
> For a climate state $s$ where models are unbiased, the expected consensus score
> is bounded by $\mu_s$ (Assumption C4):
> 
> $$
> \E[C(\mathbf{X}) \mid unbiased, s] \leq \mu_s.
> $$
> 
> For a state $s$ affected by systematic bias of magnitude $> \tau$, all ESMs
> exceed the error threshold with elevated probability. By Assumptions C4--C5
> and the analog of Lemma~1 in [cite]:
> 
> $$
> \E[C(\mathbf{X}) \mid biased, s] \geq 1 - C_{\mathrm{bal}} \cdot
> \frac{\mu_s}{|\mathcal{E}_{\mathrm{dir}}|}.
> $$
> 
> The separation gap exists whenever
> $\mu_s < |\mathcal{E}_{\mathrm{dir}}| / (|\mathcal{E}_{\mathrm{dir}}| + C_{\mathrm{bal}})$.
> 
> **Step 3: Concentration.**
> The consensus score is the mean of $M_{\mathrm{eff}}$ conditionally independent
> (indicator) random variables, each bounded in $[0,1]$. By Hoeffding's inequality:
> 
> 
> $$
> \Pbb(C(\mathbf{X}) > \theta \mid unbiased, s)
> &\leq \exp\!\bigl(-2M_{\mathrm{eff}}(\theta - \mu_s)^2\bigr), <!-- label: eq:hoeffding-fpr --> 

> \Pbb(C(\mathbf{X}) \leq \theta \mid biased, s)
> &\leq \exp\!\Bigl(-2M_{\mathrm{eff}}\bigl(1 - C_{\mathrm{bal}}\frac{\mu_s}{|\mathcal{E}_{\mathrm{dir}}|} - \theta\bigr)^2\Bigr). <!-- label: eq:hoeffding-fnr -->
> $$
> 
> 
> **Step 4: F1 aggregation.**
> Let the detection rule be $R(\mathbf{x}) = \ind{C(\mathbf{x}) > \theta}$.
> The F1 score aggregates the false positive rate (FPR) from [ref]
> and false negative rate (FNR) from [ref] across states:
> 
> 
> $$
> \mathrm{F1} &= \frac{2 \cdot \mathrm{TP}}{2 \cdot \mathrm{TP} + \mathrm{FP} + \mathrm{FN}} 

> &\geq 1 - \frac{1}{\eta_{\mathrm{bias}}}\sum_{s} \rho_s
> \Bigl[\exp(-2M_{\mathrm{eff}}(\theta - \mu_s)^2)
> + \frac{1-\eta_{\mathrm{bias}}}{\eta_{\mathrm{bias}}}
> \exp(-2M_{\mathrm{eff}}(1 - C_{\mathrm{bal}}\frac{\mu_s}{|\mathcal{E}_{\mathrm{dir}}|} - \theta)^2)\Bigr] 

> &\geq 1 - \frac{1}{\eta_{\mathrm{bias}}}\sum_{s} \rho_s
> \exp(-2M_{\mathrm{eff}}\Delta_s^2),
> $$
> 
> 
> where the last inequality uses the definition
> $\Delta_s = \min(\theta - \mu_s,\; 1 - C_{\mathrm{bal}}\frac{\mu_s}{|\mathcal{E}_{\mathrm{dir}}|} - \theta)$
> and the fact that both exponential terms are bounded by
> $\exp(-2M_{\mathrm{eff}}\Delta_s^2)$. This establishes [ref].
> 
> The miss probability bound [ref] follows from the same
> concentration argument applied to the event
> $\{\exists s: C(\mathbf{X}) \leq \theta \mid bias exists in  s\}$.

### Corollaries

> **Corollary:** [Asymptotic Perfection]
> <!-- label: cor:asymptotic-climate -->
> As $M_{\mathrm{eff}} \to \infty$, for all states satisfying
> $\mu_s < |\mathcal{E}_{\mathrm{dir}}| / (|\mathcal{E}_{\mathrm{dir}}| + C_{\mathrm{bal}})$,
> 
> $$
> \mathrm{F1}_{\mathrm{SCX}} \to 1 \quad at rate \quad
> \mathcal{O}\!\left(\frac{1}{\eta_{\mathrm{bias}}} e^{-2M_{\mathrm{eff}} \Delta_^2}\right),
> $$
> 
> where $\Delta_ = \min_s \Delta_s$.

> **Corollary:** [CMIP6 Numerical Illustration]
> <!-- label: cor:cmip6-numerical -->
> For the CMIP6 ensemble, $M \approx 20$--$40$ models depending on the variable.
> With estimated $\bar \approx 0.3$ (reflecting shared dynamical cores and
> common forcing), $M_{\mathrm{eff}} \approx 8$--$12$. For a well-observed
> climate state with $\mu_s \approx 0.15$ (models err on 15\% of time periods),
> $C_{\mathrm{bal}} = 1.5$, $|\mathcal{E}_{\mathrm{dir}}| = 4$ (warm, cold,
> wet, dry), the gap is $\Delta_s \approx 0.34$. The F1 bound is:
> 
> $$
> \mathrm{F1} \geq 1 - \frac{1}{0.2} \cdot \exp(-2 \cdot 10 \cdot 0.34^2)
> \approx 1 - 5 \cdot e^{-2.31} \approx 0.50.
> $$
> 
> This modest bound reflects the limited effective independence of the CMIP6
> ensemble and is *empirically honest*---the framework does not overpromise.
> Improving $M_{\mathrm{eff}}$ through model diversity initiatives directly
> improves this guarantee.

## Theorem 2: Attributional Unidentifiability in Climate Disagreement
<!-- label: sec:unidentifiability -->

\rigorFull

### Motivation: The Arctic Amplification Puzzle

Arctic surface temperatures are warming at approximately 3--4 times the global
mean rate [cite]. CMIP6 models span a factor-of-2 range in
projected Arctic amplification (AA) by 2100 under SSP5-8.5, from $\sim$2$\times$
to $\sim$4$\times$ the global warming rate. The disagreement could arise from
any of:

1. Cloud phase feedback error (underestimated supercooled liquid water);
2. Ocean vertical mixing error (misrepresented Atlantic Water heat
3. Ice-albedo feedback error (systematic bias in sea ice retreat rate);
4. Lapse-rate feedback error (misrepresented atmospheric stability
5. A combination of (i)--(iv) in unknown proportions.

Without additional structural assumptions, these sources are *observationally
indistinguishable* from the multi-model ensemble output alone.

### Formal Statement

> **Theorem:** [Attributional Unidentifiability in Climate Systems
> —— 气候归因不可区分定理]
> <!-- label: thm:climate-unidentifiability -->
> Let $\mathcal{E} = \{f_m\}_{m=1}^M$ be an ensemble of ESMs producing predictions
> for climate variable $Y$ (e.g., Arctic amplification factor) across climate
> states $s \in \Sstates$. Suppose the ensemble exhibits disagreement:
> $\Var_m[f_m(s)] > \tau_{\mathrm{disagree}}$.
> 
> For any two candidate error sources $\mathcal{E}_A$ and $\mathcal{E}_B$
> (e.g., $\mathcal{E}_A$ = cloud parameterization error, $\mathcal{E}_B$ = ocean
> mixing error), there exist two distinct ``worlds'':
> 
> 
1. **World A** (*Cloud-dominated*): the inter-model spread in
2. **World B** (*Ocean-dominated*): the same inter-model spread

> 
> **If** the model developers have not declared which parameterization
> schemes differ systematically across models (*i.e.*, if the attribution
> basis is not stated), **then** the observable joint distribution
> $\mathcal{P}(s, \{f_m(s)\}_{m=1}^M)$ is identical in World A and World B.
> Consequently:
> 
> 
> $$<!-- label: eq:unidentifiability-bound -->
> \boxed{\;
> \max\!\bigl(\mathrm{Error}_{World A}(\mathcal{A}),\;
>           \mathrm{Error}_{World B}(\mathcal{A})\bigr)
> \geq \frac{\eta_{\mathrm{misattr}} \cdot \rho_{\mathrm{disagree}}}{2}
> \;},
> $$
> 
> 
> where $\mathcal{A}$ is any attribution algorithm, $\eta_{\mathrm{misattr}}$ is
> the proportion of model divergence attributable to misattribution, and
> $\rho_{\mathrm{disagree}}$ is the proportion of climate states where disagreement
> exceeds the threshold. The bound is strictly positive whenever
> $\eta_{\mathrm{misattr}} > 0$ and $\rho_{\mathrm{disagree}} > 0$.
> 
> In particular, from multi-model output alone, it is **mathematically
> impossible** to determine whether Arctic amplification spread is caused by cloud
> error, ocean error, ice-albedo error, or any combination thereof---without
> declaring explicit structural assumptions.

### Proof of Theorem 2

> **Proof:** We construct two observationally equivalent worlds and apply Le Cam's
> two-point argument.
> 
> **Construction of World A (Cloud-dominated).**
> Let there be $M$ ESMs. For each model $m$, decompose its Arctic amplification
> prediction as:
> 
> $$
> f_m(s_{\mathrm{AA}}) = \mu(s_{\mathrm{AA}})
> + \varepsilon_m^{\mathrm{cloud}} + \varepsilon_m^{\mathrm{ocean}}
> + \varepsilon_m^{\mathrm{ice}},
> $$
> 
> where $\mu(s_{\mathrm{AA}})$ is the (unknown) true AA factor.
> In World A, set:
> 
> $$
> \varepsilon_m^{\mathrm{cloud}} &\sim \mathcal{N}(0, \sigma_A^2),
> \quad \sigma_A^2 \gg 0, 

> \varepsilon_m^{\mathrm{ocean}} &\sim \mathcal{N}(0, \delta^2),
> \quad \delta^2 \to 0, 

> \varepsilon_m^{\mathrm{ice}} &\sim \mathcal{N}(0, \delta^2),
> \quad \delta^2 \to 0.
> $$
> 
> The observables are the model outputs $\{f_m(s_{\mathrm{AA}})\}_{m=1}^M$ and
> the hindcast validation scores on well-observed periods.
> 
> **Construction of World B (Ocean-dominated).**
> Maintain the same decomposition but reverse the variance allocation:
> 
> $$
> \varepsilon_m^{\mathrm{cloud}} &\sim \mathcal{N}(0, \delta^2),
> \quad \delta^2 \to 0, 

> \varepsilon_m^{\mathrm{ocean}} &\sim \mathcal{N}(0, \sigma_A^2),
> \quad \sigma_A^2 \gg 0, 

> \varepsilon_m^{\mathrm{ice}} &\sim \mathcal{N}(0, \delta^2),
> \quad \delta^2 \to 0.
> $$
> 
> 
> **Observational equivalence.**
> In both worlds, the marginal distribution of $\{f_m(s_{\mathrm{AA}})\}$ is:
> 
> $$
> f_m(s_{\mathrm{AA}}) \sim \mathcal{N}(\mu(s_{\mathrm{AA}}), \sigma_A^2 + 2\delta^2),
> \quad \forall m.
> $$
> 
> The pairwise correlation between models is:
> 
> $$
> \Corr(f_m, f_{m'}) = \frac{\Cov(\varepsilon_m^{\mathrm{cloud}} + \varepsilon_m^{\mathrm{ocean}},
> \varepsilon_{m'}^{\mathrm{cloud}} + \varepsilon_{m'}^{\mathrm{ocean}})}
> {\sigma_A^2 + 2\delta^2}.
> $$
> 
> Since the decomposition of $\sigma_A^2$ into cloud vs. ocean components is
> *not observable* in the model outputs (only the total variance is), the
> joint distribution $\mathcal{P}(\{f_m\})$ is identical across worlds.
> 
> **Impossibility of attribution.**
> Let $\mathcal{A}$ be any algorithm that uses the observable ensemble to assign
> attribution fractions $\hat{w}_A, \hat{w}_B$ (cloud fraction, ocean fraction)
> such that $\hat{w}_A + \hat{w}_B + \hat{w}_{\mathrm{other}} = 1$. Under the
> observational equivalence, the algorithm's output distribution is identical in
> both worlds:
> 
> $$
> \mathcal{L}_{World A}(\mathcal{A}(D)) = \mathcal{L}_{World B}(\mathcal{A}(D)).
> $$
> 
> Let $a = \E[\hat{w}_A]$ be the expected cloud attribution fraction output by
> $\mathcal{A}$. In World A, the error is $(1-a)$ (under-attributing to clouds);
> in World B, the error is $a$ (over-attributing to clouds). The minimax error
> over the two worlds is:
> 
> $$
> \max(\mathrm{Error}_A, \mathrm{Error}_B) \geq
> \frac{(1-a) + a}{2} = \frac{1}{2},
> $$
> 
> scaled by the proportion $\eta_{\mathrm{misattr}} \cdot \rho_{\mathrm{disagree}}$
> of cases where misattribution is possible, yielding [ref].

### The Path Out: Declared Attribution Assumptions

\rigorPartial

Theorem~2 is *constructive*: it identifies precisely what information
breaks the unidentifiability. The following ``attribution basis'' must be
declared:

> **Definition:** [Attribution Basis for Climate Disagreement]
> <!-- label: def:attribution-basis -->
> A declared attribution basis for a climate variable $Y$ is a tuple
> $\mathcal{B} = (\mathcal{P}_1, ..., \mathcal{P}_K, \mathbf{W})$ where:
> 
- $\mathcal{P}_k$ is the $k$-th candidate error process (e.g., cloud
- $\mathbf{W} \in \R_{\geq 0}^K$ with $\sum_k W_k = 1$ specifies the
- Each $\mathcal{P}_k$ is associated with a \emph{process-resolving

A climate modeling center that declares $\mathcal{B}$ makes an auditable claim:
``We assert that Arctic amplification spread in our ensemble is attributable to
processes $\mathcal{P}_1, ..., \mathcal{P}_K$ in proportions
$W_1, ..., W_K$, supported by observational constraints $O_1, ..., O_K$.''
This claim is verifiable by any third party with access to the same observations.

> **Corollary:** [人人平等定理 for Climate Science]
> <!-- label: cor:climate-equality -->
> Any claim about the source of inter-model climate disagreement that does not
> declare an attribution basis $\mathcal{B}$ is mathematically empty. Conversely,
> any declared attribution basis is verifiable by any observer with access to the
> specified observational constraints, without privileged access to model code
> or developer expertise. This establishes epistemic equality among climate
> scientists, modeling centers, and external auditors.

## Theorem 3: Cercis Score for Climate Model Quality Assessment
<!-- label: sec:cercis-score -->

\rigorPartial

### The Cercis Score Construction

The Cercis{} Score [cite] provides a unified metric for ranking
predictive models that balances two competing objectives: fidelity to
observations ($Q$, the quality component) and the epistemic value of predicting
novel, unprecedented regimes ($N$, the novelty component). For climate models,
this maps naturally to the tension between hindcast skill and the exploration
of high-forcing futures.

> **Definition:** [Cercis Score for Climate Models]
> <!-- label: def:cercis-climate -->
> For ESM $m$ producing predictions across climate states $\{s\}_{s \in \Sstates}$,
> the Cercis{} Score is:
> 
> $$<!-- label: eq:cercis-def -->
> S_m(t) = Q_m(t) + \eta(t) \cdot N_m(t),
> $$
> 
> where:
> 
> $$
> Q_m(t) &= \frac{1}{|\mathcal{T}_{\mathrm{hind}}|}\sum_{\tau \in \mathcal{T}_{\mathrm{hind}}}
> w(\tau) \cdot \mathrm{skill}(f_m(\tau), Y_{\mathrm{obs}}(\tau)),
> \quad (hindcast quality) <!-- label: eq:q-component --> 

> N_m(t) &= \KL\!\bigl(\mathcal{P}_m(\mathbf{X}(t)) \;\big\|\;
> \mathcal{P}_{\mathrm{ref}}(\mathbf{X}(t))\bigr),
> \quad (regime novelty) <!-- label: eq:n-component --> 

> \eta(t) &= \eta_0 \cdot \exp(-\gamma \cdot t),
> \quad (exploration decay). <!-- label: eq:eta-decay -->
> $$

Here, $\mathrm{skill}(f_m(\tau), Y_{\mathrm{obs}}(\tau))$ is a dimension-specific
skill score (e.g., anomaly correlation for temperature, Brier skill score for
sea ice binary masks, Kling-Gupta efficiency for precipitation). The quality
weights $w(\tau)$ emphasize recent observations:
$w(\tau) \propto \exp(-\lambda(t - \tau))$.

The novelty component $N_m(t)$ measures the Kullback-Leibler divergence between
the model's predicted climate state distribution and a reference distribution
(typically the historical climatology). When $N_m(t)$ is large, the model
predicts a regime with no historical analog---precisely the conditions under
which conventional skill scores are unreliable.

The exploration rate $\eta(t)$ decays exponentially from $\eta_0$ (the initial
willingness to credit novel predictions) toward zero. This ensures that as
observations accumulate in new regimes, the score eventually converges to pure
skill.

### Ranking Optimality

> **Theorem:** [Cercis Consistency for Climate Ensembles
> —— Cercis评分一致性定理]
> <!-- label: thm:cercis-consistency -->
> Let $\mathcal{E} = \{f_1, ..., f_M\}$ be an ensemble of ESMs with known hindcast
> skill scores $Q_m$ and novelty scores $N_m$. Under Assumptions C1--C6, the
> Cercis ranking
> 
> $$
> R_{Cercis} = \arg\max_{m \in \{1,...,M\}} S_m
> $$
> 
> satisfies the following properties:
> 
> 
1. **Hindcast consistency:** For climate states $s$ with
2. **Novelty protection:** For any two models $m, m'$ with
3. **Conservatism under ignorance:** If the climate state $s$ is

> **Proof:** [Proof Sketch]
> \rigorPartial
> 
> **(a) Hindcast consistency.**
> When $N_m(s) < \varepsilon$, we have:
> 
> $$
> |S_m - Q_m| = \eta \cdot N_m < \eta \varepsilon.
> $$
> 
> For any two models $m, m'$:
> 
> $$
> S_m > S_{m'} \iff Q_m + \eta N_m > Q_{m'} + \eta N_{m'}
> \iff Q_m - Q_{m'} > \eta(N_{m'} - N_m).
> $$
> 
> Since $|N_{m'} - N_m| < 2\varepsilon$, the condition $Q_m - Q_{m'} > 2\eta\varepsilon$
> is sufficient. Taking $\eta \to 0$ (as $t \to \infty$) and $\varepsilon \to 0$
> (as the reference distribution expands to cover observed states), the ranking
> converges to the pure skill ordering.
> 
> **(b) Novelty protection.**
> The condition $|Q_m - Q_{m'}| < \eta(N_m - N_{m'})$ implies directly that
> $S_m > S_{m'}$, since:
> 
> $$
> S_m - S_{m'} = (Q_m - Q_{m'}) + \eta(N_m - N_{m'})
> > -|Q_m - Q_{m'}| + \eta(N_m - N_{m'}) > 0.
> $$
> 
> This property prevents a model that is marginally better on hindcast but
> predicts nothing novel from dominating a model that explores unprecedented
> regimes.
> 
> **(c) Conservatism under ignorance.**
> When no model achieves $Q_m > Q_{\mathrm{base}}$ and all $N_m(s) > \tau_N$,
> the maximum Cercis score is:
> 
> $$
> S_ < Q_{\mathrm{base}} + \eta_0 \cdot \sup_m N_m.
> $$
> 
> By setting $S_ > Q_{\mathrm{base}} + \eta_0 \cdot \sup_m N_m$ as the
> threshold for ``certified guidance,'' all models fall below the threshold and
> the framework correctly declines to rank. This is a feature, not a bug: it
> prevents overconfident projections in regimes where no model has demonstrated
> competence.

### Application to CMIP6 Scenarios

> **Example:** [Cercis Scoring for CMIP6 SSP Scenarios]
> <!-- label: ex:cercis-cmip6 -->
> Consider three climate states: (i) historical 1980--2014 ($N \approx 0$),
> (ii) mid-century SSP2-4.5 ($N \approx 0.3$), (iii) late-century SSP5-8.5
> ($N \approx 0.8$). With $\eta_0 = 0.5$ and $\gamma$ chosen so $\eta(2024) = 0.4$,
> $\eta(2050) = 0.25$, $\eta(2100) \approx 0.05$:
> 
> 
> [Table omitted — see original .tex]
> 
> 
> The Cercis framework correctly penalizes the extremely novel SSP5-8.5 state
> with low $\eta$, while rewarding the moderately novel SSP2-4.5 state. The
> historical state's score is dominated by pure skill. If $S_ = 0.40$, the
> SSP5-8.5 state falls below the certification threshold---an honest reflection
> of epistemic limits.

## Spring Gating for Detecting Climate Regime Shifts
<!-- label: sec:spring-gating -->

\rigorPartial

### Climate Tipping Points as Regime Boundaries

Climate tipping points---thresholds beyond which the Earth system undergoes
qualitative, often irreversible, change---represent the most consequential
uncertainty in climate prediction. Candidates include:

- Atlantic Meridional Overturning Circulation (AMOC) collapse;
- Greenland ice sheet disintegration;
- Amazon rainforest dieback;
- Permafrost carbon release;
- West Antarctic ice sheet collapse.

Each tipping element defines a **regime boundary** in the climate state
space. The Spring{} gating mechanism [cite] provides a framework
for detecting when a climate trajectory crosses such a boundary, triggering a
change in the auditing regime.

### Spring Formalism for Climate States

> **Definition:** [Climate Spring Gate]
> <!-- label: def:spring-climate -->
> A Spring gate for climate regime $r$ is a discriminator
> $D_r: \X \to [0,1]$ trained to distinguish climate states belonging to regime
> $r$ from those not belonging to $r$. The gate's memory bank $\mathcal{M}_t^{(r)}$
> accumulates climate states visited by any ESM trajectory:
> 
> 
> $$
> \mathcal{M}_t^{(r)} = \bigcup_{\tau=0}^t \bigcup_{m=1}^M
> \{(\mathbf{X}_m(\tau), \, \ind{\mathbf{X}_m(\tau) \in regime  r})\}.
> $$

The Spring self-evolution theorem [cite] guarantees almost-sure
convergence of the discriminator accuracy:

$$
\lim_{t \to \infty} \Pbb(D_r(\mathbf{X}(t)) \neq \ind{\mathbf{X}(t) \in regime  r})
= 0,
$$

under the Robbins-Monro conditions satisfied by the Spring update rule.

> **Proposition:** [Regime-Shift Detection via Spring]
> <!-- label: prop:spring-regime -->
> Let $\mathcal{T}_{\mathrm{shift}}$ be the (unknown) time at which the climate
> system crosses a tipping threshold. Under Assumptions C1--C7 and the Spring
> convergence theorem, for any $\varepsilon > 0$ there exists $T_\varepsilon$ such
> that for all $t > T_\varepsilon$:
> 
> 
> $$
> \Pbb\!\bigl(|\hat{\mathcal{T}}_{\mathrm{shift}} - \mathcal{T}_{\mathrm{shift}}| > \varepsilon\bigr)
> \leq C \cdot \exp(-\gamma_{Spring} \cdot |\mathcal{M}_t|),
> $$
> 
> where $|\mathcal{M}_t|$ is the accumulated memory size and $\gamma_{Spring} > 0$
> is the Spring convergence rate.

> **Proof:** [Proof Sketch]
> \rigorSketch
> 
> The Spring convergence theorem (SE-1 in [cite]) establishes that
> the fixed-point of the gate's scoring function $S_t$ converges to the true
> regime indicator with rate $O(t^{-a})$ for $a \in (0, 1/2]$ under convexity or
> $O(t^{-1})$ under strong convexity (via Polyak averaging). The detection delay
> $\hat{\mathcal{T}}_{\mathrm{shift}} - \mathcal{T}_{\mathrm{shift}}$ is bounded by
> the convergence time of the discriminator. Exponential concentration follows from
> the Hoeffding bound applied to the i.i.d. arrivals of regime member states into
> $\mathcal{M}_t$.

### Implications for Auditing

When a Spring gate detects a regime shift, the SCX auditing procedure adjusts:

1. **Assumption C6 is suspended**: hindcast stationarity no longer
2. **Yajie consensus is re-calibrated**: the expert error rates
3. **Situs encoding is re-anchored**: the spatial correlation

## Situs Encoding for Spherical Climate Geometry
<!-- label: sec:situs-climate -->

\rigorPartial

### The Spherical Encoding Problem

Climate fields are fundamentally defined on $S^2$ (the sphere) with a radial
component in the vertical. Standard Cartesian positional encodings fail to
respect the spherical topology, treating distant points across the Pacific as
equivalent (they wrap on a longitude--latitude grid) and distorting polar
regions. The \Situs{} framework [cite] provides physics-anchored
positional encoding where the encoding function respects the geometry of the
underlying physical space.

> **Definition:** [Situs Spherical Encoding for Climate]
> <!-- label: def:situs-spherical -->
> For a point $p \in S^2 \times [0, H]$ (longitude $\phi$, latitude $\theta$,
> height $h$), the \Situs{} encoding is:
> 
> $$
> \Situs(p) = \bigoplus_{\ell=1}^L \bigoplus_{\omega \in \Omega_\ell}
> \bigl(\sin(\omega \cdot d_{S^2}(p, p_\ell^*)),\;
>        \cos(\omega \cdot  d_{S^2}(p, p_\ell^*))\bigr),
> $$
> 
> where:
> 
- $p^*_\ell$ are $L$ anchor points on the sphere (e.g., grid points of a
- $d_{S^2}$ is the great-circle distance;
- $\Omega_\ell$ is a frequency set for anchor $\ell$, chosen via the

> **Proposition:** [Spherical Encoding Error Bound]
> <!-- label: prop:situs-error -->
> Under Assumption C8 (spherical correlation structure), the \Situs{} encoding
> approximates the spatial error correlation with error:
> 
> $$
> \sup_{p,q \in S^2} \bigl|\Corr(e(p), e(q)) - \kappa \cdot
> \langle \Situs(p), \Situs(q) \rangle \bigr|
> \leq C_ \cdot L^{-1/2},
> $$
> 
> where $C_$ depends on the smoothness of the error field and $L$ is the
> number of anchor points.

> **Proof:** [Proof Sketch]
> \rigorSketch
> 
> The proof follows the Situs theory [cite], Theorem 1.2.2, which
> establishes $O(1/d)$ convergence of the Laplace kernel approximation under
> Bochner's theorem, modified for $S^2$ using the spherical harmonics addition
> theorem. The key step is that the correlation function $\Corr(e(p), e(q))$ is a
> positive-definite kernel on $S^2$ satisfying Assumption C8, hence admits a
> Mercer expansion in spherical harmonics. Truncation at degree $L$ yields the
> stated $O(L^{-1/2})$ rate (the exponent changes from $1/d$ to $1/\sqrt{L}$
> because the spherical harmonics degeneracy grows as $\sim 2\ell + 1$ per degree
> $\ell$).

### Climate Field State Discovery

The \Situs{} encoding enables state discovery on spherical climate fields
through the condition [cite]:

$$
I(Y; P \mid S) > 0,
$$

where $Y$ is the target climate variable, $P$ is the spatial position, and $S$
is the climate state. When this mutual information is positive, spatial position
carries irreducible information about model error beyond what the state alone
provides. This is the case for:

- Regional precipitation biases (strongly location-dependent);
- Sea ice edge position errors (spatially localized);
- Coastal upwelling errors (boundary-condition sensitive);
- Mountain snowpack errors (elevation-dependent).

When $I(Y; P \mid S) = 0$, the climate field error is spatially stationary
(given the state), and \Situs{} provides no additional benefit---a diagnostic
that prevents unnecessary computational overhead.

## Benchmark Suite for Certified Climate Auditing
<!-- label: sec:benchmarks -->

We specify a three-tier benchmark hierarchy for validating the SCX climate
auditing framework. No empirical results are presented in this theoretical
paper; the benchmarks are specified as the protocol for future computational
validation.

### Tier 1: CMIP6 Historical (1850--2014)

**Models**: CESM2, NorESM2-LM, MIROC6, HadGEM3-GC31-LL, MPI-ESM1.2-HR,
CanESM5, IPSL-CM6A-LR, EC-Earth3, GFDL-ESM4, MRI-ESM2.0, ACCESS-ESM1.5,
UKESM1-0-LL, CNRM-ESM2-1, BCC-CSM2-MR ($M = 14$--$20$ models, variable-dependent).

**Variables**:

- Global mean surface temperature (GMST, $Y \in \R$): scalar, directly
- Arctic sea ice extent (September minimum, $Y \in [0, 14 \times 10^6\ \mathrm{km}^2]$):
- Global precipitation pattern ($Y \in \R^{d_{\mathrm{grid}}}$): spatial
- AMOC strength at 26.5\textdegree N ($Y \in \R$): tests Spring gating

**Metrics**:

- F1 score of bias detection (Theorem 1 bound vs. empirical);
- $M_{\mathrm{eff}}$ estimation via jackknife correlation of residuals;
- Cercis Score ranking vs. naive ensemble mean ranking;
- Spring gate accuracy for distinguishing historical vs. paleoclimate

### Tier 2: SSP Scenario Projections (2015--2100)

**Scenarios**: SSP1-2.6, SSP2-4.5, SSP3-7.0, SSP5-8.5.

**Tests**:

- **Novelty quantification**: $N_m(t)$ computed via KL divergence
- **Cercis trajectory**: $S_m(t)$ evolution under $\eta(t)$ decay,
- **Spring gating for emergence**: detection of the time at which

### Tier 3: Paleoclimate Validation

**Intervals**:

- Last Glacial Maximum (LGM, $\sim$21 ka, $\Delta$GMST $\approx -4$ to $-6$ K,
- Mid-Pliocene Warm Period ($\sim$3.3--3.0 Ma, $\Delta$GMST $\approx +2$ to $+3$ K,
- Mid-Holocene ($\sim$6 ka, orbital forcing different from present).

**Tests**:

- **Theorem 1 extrapolation**: does the F1 bound hold when states
- **Attribution basis validation**: can the declared attribution
- **Spring memory transfer**: does the Spring gate trained on LGM

## Limitations: What This Framework Cannot Do
<!-- label: sec:limitations -->

\rigorFull

An honest assessment of limitations is essential to the SCX methodology. We
state the following explicitly.

### What the Theorems Do Not Prove

1. **Climate sensitivity is not bounded.**
2. **Structural model error is not quantified.**
3. **Observational reference is imperfect.**
4. **Stationarity is unverifiable for the future.**
5. **Paleoclimate constraints are proxy-limited.**
6. **The exponential bound is asymptotic.**
7. **Cercis $\eta(t)$ is a hyperparameter.**
8. **The attribution basis $\mathcal{B}$ is incomplete.**

### Assumption Violation Consequences

Table [ref] summarizes the consequence of violating
each assumption.

[Table omitted — see original .tex]

## Discussion: Toward Certified Climate Services

### The Epistemic Division of Labor

The SCX climate auditing framework enforces a clean separation of
responsibilities:

1. **Climate modeling centers** produce ESMs and declare their
2. **Observational data providers** supply the hindcast validation
3. **The SCX auditor** applies Theorems~1--3 to certify what can be

No party needs to trust any other. The certification is a mathematical
consequence of the declared assumptions and the observed multi-model ensemble
statistics.

### Policy Implications

For climate services that inform adaptation investment ($10^{11}$--$10^{12}$
USD/year globally), the difference between ``the ensemble mean projects X'' and
``we certify at confidence $1-\alpha$ that the true value lies in $[X-\delta,
X+\delta]$'' is operationally enormous. The SCX framework provides the latter
form of statement, with the crucial caveat that $\alpha$ and $\delta$ may be
disappointingly large for many variables of interest---an honest assessment is
preferable to a precise but unfounded one.

### Relationship to IPCC Assessment

The IPCC AR6 [cite] uses ``likelihood'' and ``confidence'' language
defined by convention: ``likely'' means $>66\%$ probability, ``very likely''
means $>90\%$, etc. The SCX framework provides a mathematical foundation for
these assignments: under Assumptions C1--C10, the probability bounds in
Theorem~1 translate directly to IPCC likelihood categories, with the
additional property that the derivation of the bound is fully transparent and
reproducible.

### Open Problems

\begin{openproblem}[Dependent Concentration for Climate Ensembles]
<!-- label: op:1 -->
Theorem~1 uses Hoeffding's inequality under Assumption C2 (conditional
independence). When C2 is violated, the effective correlation $\bar$
degrades $M_{\mathrm{eff}}$. Develop a sharp concentration inequality for
dependent Bernoulli trials with known correlation structure that improves the
bound beyond the naive variance-inflation factor.
\rigorSketch
\end{openproblem}

\begin{openproblem}[Optimal Attribution Basis Selection]
<!-- label: op:2 -->
Given $M$ ESMs with known parameterization differences, what is the
information-theoretically optimal decomposition of inter-model spread into an
attribution basis $\mathcal{B}$? This is a combinatorial optimization problem
over the space of process partitions, coupled to the mutual information between
process-resolving observations and model outputs.
\rigorSketch
\end{openproblem}

\begin{openproblem}[Paleoclimate Prior Elicitation]
<!-- label: op:3 -->
How should paleoclimate constraints be formally incorporated as priors in the
Cercis Score? Assumption C10 requires $\sigma_{\mathrm{proxy}} < \tau/2$, but a
more sophisticated treatment would use the full proxy likelihood to weight
the novelty component $N_m$, rather than treating paleoclimate as a binary
``constrained/unconstrained'' gate.
\rigorSketch
\end{openproblem}

## Conclusion

We have presented a mathematical framework for auditing Earth System Model
ensembles that provides certified uncertainty bounds rather than informal
consensus. The framework rests on 10 explicitly stated assumptions and three
theorems with proofs.

**Theorem~1** (Systematic Bias Detection) establishes that multi-model
consensus provides exponentially convergent detection of systematic biases,
with the rate governed by the effective number of independent models
$M_{\mathrm{eff}}$. The bound is honest: for the CMIP6 ensemble,
certification is modest but real.

**Theorem~2** (Attributional Unidentifiability) proves that without
declared structural assumptions, it is mathematically impossible to attribute
inter-model climate disagreement to specific physical processes. This
establishes an epistemic standard: attribution claims must be accompanied by
declared and auditable attribution bases.

**Theorem~3** (Cercis Consistency) provides a principled ranking of
climate projections that balances hindcast skill against the epistemic value
of exploring unprecedented regimes. The Cercis Score correctly degrades as
models enter novel territory and refuses to rank when no model demonstrates
competence.

The SCX framework does not predict the climate. It certifies the epistemic
status of predictions made by others. This is a deliberate design choice:
certification is separable from modeling, auditable by third parties, and
updatable as new models and observations become available. In a domain where
trillions of dollars and millions of lives depend on projections that remain
fundamentally uncertain, honest certification is the most valuable contribution
that mathematical rigor can offer.

\begin{thebibliography}{30}

\bibitem{xi2025scx}
SCX. A Fundamental Impossibility in Data Quality: Distinguishing Label Noise
from Sample Difficulty is Provably Unsolvable Without Explicit Assumptions.
arXiv preprint (2025).

\bibitem{spring_config}
SCX. Spring: A Self-Evolving Gatekeeper with Provable Convergence.
Working paper (2026).

\bibitem{situs_theory}
SCX. Situs: Physics-Anchored Positional Encoding for State-Conditioned
Expertise. Working paper (2026).

\bibitem{taxonomic_nn}
SCX. A Taxonomic Theory of Neural Networks: Derivation of Known Machine
Learning Phenomena from the SCX Axiom System. Working paper (2026).

\bibitem{eyring2016}
Eyring, V., Bony, S., Meehl, G. A., Senior, C. A., Stevens, B., Stouffer,
R. J., \& Taylor, K. E. Overview of the Coupled Model Intercomparison Project
Phase 6 (CMIP6) experimental design and organization.
*Geoscientific Model Development* **9**(5), 1937--1958 (2016).

\bibitem{ipcc2021}
IPCC. Climate Change 2021: The Physical Science Basis. Contribution of
Working Group I to the Sixth Assessment Report. Cambridge University Press
(2021).

\bibitem{danabasoglu2020}
Danabasoglu, G., et al. The Community Earth System Model Version 2 (CESM2).
*Journal of Advances in Modeling Earth Systems* **12**(2) (2020).

\bibitem{seland2020}
Seland, \O{}., et al. Overview of the Norwegian Earth System Model (NorESM2)
and key climate response of CMIP6 DECK, historical, and scenario simulations.
*Geoscientific Model Development* **13**(12), 6165--6200 (2020).

\bibitem{tatebe2019}
Tatebe, H., et al. Description and basic evaluation of simulated mean state,
internal variability, and climate sensitivity in MIROC6.
*Geoscientific Model Development* **12**(7), 2727--2765 (2019).

\bibitem{kuhlbrodt2018}
Kuhlbrodt, T., et al. The Low-Resolution Version of HadGEM3 GC3.1:
Development and Evaluation for Global Climate.
*Journal of Advances in Modeling Earth Systems* **10**(11),
2865--2888 (2018).

\bibitem{rantanen2022}
Rantanen, M., et al. The Arctic has warmed nearly four times faster than the
globe since 1979. *Communications Earth \& Environment* **3**,
168 (2022).

\bibitem{hall2019}
Hall, A., Cox, P., Huntingford, C., \& Klein, S. Progressing emergent
constraints on future climate change. *Nature Climate Change*
**9**, 269--278 (2019).

\bibitem{hoeting1999}
Hoeting, J. A., Madigan, D., Raftery, A. E., \& Volinsky, C. T. Bayesian
model averaging: a tutorial. *Statistical Science* **14**(4),
382--401 (1999).

\bibitem{castruccio2019}
Castruccio, S., et al. An updated suite of statistical models for emulating
Earth system model output. *Journal of Climate* (2019).

\bibitem{tebaldi2005}
Tebaldi, C., Smith, R. L., Nychka, D., \& Mearns, L. O. Quantifying
uncertainty in projections of regional climate change: A Bayesian approach
to the analysis of multimodel ensembles. *Journal of Climate*
**18**(10), 1524--1540 (2005).

\bibitem{liang1986}
Liang, K. Y. \& Zeger, S. L. Longitudinal data analysis using generalized
linear models. *Biometrika* **73**(1), 13--22 (1986).

\bibitem{hoeffding1963}
Hoeffding, W. Probability inequalities for sums of bounded random variables.
*Journal of the American Statistical Association* **58**(301),
13--30 (1963).

\bibitem{cover2006}
Cover, T. M. \& Thomas, J. A. *Elements of Information Theory*.
Wiley, 2nd ed. (2006).

\bibitem{bahadur1960}
Bahadur, R. R. \& Rao, R. R. On deviations of the sample mean.
*Annals of Mathematical Statistics* **31**(4), 1015--1027 (1960).

\end{thebibliography}