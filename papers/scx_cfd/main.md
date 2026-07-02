*Abstract:*

We apply the SCX quality audit framework to neural computational fluid dynamics (CFD) for finite element aerodynamics.
While traditional CFD employs multiple physically grounded ``experts''---turbulence models ($k$-$\varepsilon$, $k$-$\omega$ SST, LES, DES), mesh convergence hierarchies, and distinct numerical discretizations---neural CFD solvers (physics-informed neural networks, Fourier neural operators, mesh graph networks, learned turbulence closures) lack formal quality guarantees.
We formalize aerodynamic simulation as state-conditioned prediction over flow regimes, and prove three theorems:
(1) an SCX noise detection bound that limits the probability of missing systematic errors when $M$ solvers (traditional plus neural) are applied to the same geometry;
(2) an unidentifiability theorem establishing that when a neural solver disagrees with wind tunnel data, the error source cannot be attributed without declared assumptions; and
(3) a Situs encoding guarantee that relates geometric discretization fidelity in airfoil/wing representations to aerodynamic prediction error through Lipschitz continuity.
We define the Cercis score for aerodynamic simulation, combining benchmark accuracy (ONERA M6, NASA CRM, NACA airfoils) with flow regime coverage novelty, and we rank published neural CFD methods.
A multi-expert architecture with the Yajie consensus mechanism is proposed, using wind tunnel data as ground-truth anchor.
We contribute an explicit assumption map for neural CFD and an experimental protocol covering standard benchmarks, turbulence model variations, mesh convergence studies, and neural architecture ablations.
All claims are explicitly labeled with rigor level and assumption dependencies.

**Keywords:** SCX audit, neural CFD, finite element aerodynamics, turbulence modeling, 空气动力学, 湍流模型, quality certification, multi-expert consensus

## Introduction

Computational fluid dynamics (CFD) is the backbone of modern aerodynamic design, with finite element and finite volume methods enabling accurate simulation of flows around aircraft wings, turbomachinery blades, and automotive bodies.
The governing equations---the Navier-Stokes equations---are well understood, but their direct numerical solution at industrially relevant Reynolds numbers remains computationally prohibitive.
This has led to a rich ecosystem of modeling approximations, each constituting a distinct ``expert'' in the SCX sense.

### Traditional CFD: A Natural Multi-Expert Landscape

Traditional CFD naturally provides multiple experts through independent modeling choices:

1. **Turbulence models:** The Reynolds-Averaged Navier-Stokes (RANS) framework produces distinct closure models: $k$-$\varepsilon$ [cite], $k$-$\omega$ SST [cite], Spalart-Allmaras [cite], each making different assumptions about turbulent viscosity.
2. **Scale-resolving approaches:** Large Eddy Simulation (LES) [cite] and Detached Eddy Simulation (DES) [cite] resolve different fractions of the turbulent spectrum.
3. **Discretization schemes:** Finite volume vs. finite element vs. discontinuous Galerkin methods, each with distinct convergence properties and numerical dissipation characteristics.
4. **Mesh resolutions:** Grid convergence studies produce a family of solutions that can be treated as correlated experts with known Richardson extrapolation error estimates.
5. **Experimental anchors:** Wind tunnel measurements [cite] provide ground-truth data at specific Reynolds and Mach numbers, albeit with their own uncertainty.

These experts differ in computational cost, physical fidelity, and domain of applicability, but they share a common governing equation structure.
The SCX insight is that this diversity is a *resource* for quality auditing, not a problem to be eliminated.

### Neural CFD: Speed Without Guarantees

Recent years have seen a proliferation of neural approaches to CFD, each claiming dramatic speed advantages:

1. **Physics-Informed Neural Networks (PINNs)** [cite]: Solve PDEs by embedding governing equations into neural network loss functions. Applied to incompressible Navier-Stokes [cite], but struggle with high Reynolds number turbulence.
2. **Fourier Neural Operators (FNOs)** [cite]: Learn mappings between function spaces in Fourier domain. Applied to aerodynamics by [cite], showing speedups of $10^3$--$10^4$ over traditional solvers for specific geometries.
3. **MeshGraphNets (GNN solvers)** [cite]: Encode mesh-based simulations as graph neural networks.  [cite] applied similar architectures to airfoil flow prediction.
4. **Learned turbulence closures**: Neural networks replace or augment traditional RANS turbulence models [cite], learning corrections from high-fidelity LES or DNS data.

### The Quality Gap

\assumptionTag{0} **(Motivating Observation)**: No published neural CFD method provides a formal quality guarantee---i.e., a verified bound on prediction error for previously unseen geometries and flow conditions.
The following specific concerns motivate the SCX audit:

1. **Training data contamination:** Neural operators trained on aerodynamic databases may ``memorize'' specific geometries or flow features, giving misleadingly low errors on test splits drawn from the same distribution.
2. **Mesh dependency:** Neural solvers inherit biases from the resolution and topology of training meshes; prediction quality on meshes of substantially different density is unknown.
3. **Turbulence model mismatch:** Learned closures trained on one turbulence regime (e.g., attached boundary layers) may fail silently in another (e.g., separated flows).
4. **Architectural extrapolation:** Neural networks lack the asymptotic consistency guarantees that underlie traditional CFD methods (e.g., the Lax equivalence theorem).

### Contributions

This paper provides the SCX audit framework for neural CFD:

1. **Formal problem formulation** (§2): Aerodynamic simulation as state-conditioned prediction with explicit flow regime states.
2. **Noise detection theorem** (§3): Bounds on the probability of missing systematic neural CFD errors when audited by multiple traditional and neural experts.
3. **Error source unidentifiability theorem** (§4): Proof that without explicit assumption declaration, the source of neural CFD errors is fundamentally unidentifiable.
4. **Situs encoding guarantee** (§5): A Lipschitz-based bound relating geometric encoding fidelity to aerodynamic prediction error.
5. **Cercis score** (§6): Quantitative ranking of existing neural CFD methods on standard benchmarks.
6. **Multi-expert architecture** (§7): Yajie consensus mechanism combining traditional and neural experts with wind tunnel anchoring.
7. **Experimental protocol** (§8): Reproducible benchmark suite with explicit assumption tracking.

 We emphasize that this paper makes no ``revolutionary'' claims about neural CFD. Our contribution is a *quality audit framework* that enables rigorous comparison and certification of existing and future methods. \limitationTag{0} The framework is descriptive and diagnostic; it does not prescribe how to improve neural CFD accuracy.

## Problem Formulation: Aerodynamic Simulation as State-Conditioned Prediction

### The Forward Aerodynamic Problem

Let $\Omega \subset \R^d$ ($d=2$ for airfoils, $d=3$ for wings) be the computational domain surrounding an aerodynamic body with boundary $\Gamma_w$ (the wing/airfoil surface).
The steady-state Reynolds-Averaged Navier-Stokes (RANS) equations are:

$$

$$
\nabla \cdot (\rho \mathbf{u}) &= 0 

\nabla \cdot (\rho \mathbf{u} \otimes \mathbf{u}) &= -\nabla p + \nabla \cdot \left[ (\mu + \mu_t)(\nabla \mathbf{u} + \nabla \mathbf{u}^T) \right] 

\nabla \cdot (\rho \mathbf{u} h) &= \nabla \cdot \left[ (\lambda + \lambda_t) \nabla T \right]
$$

<!-- label: eq:rans -->
$$

 where $\rho$ is density, $\mathbf{u}$ is velocity, $p$ is pressure, $\mu$ is molecular viscosity, $\mu_t$ is turbulent (eddy) viscosity, $h$ is enthalpy, $\lambda$ is thermal conductivity, and $\lambda_t$ is turbulent thermal conductivity.
The turbulence model provides the closure for $\mu_t$.

### State-Conditioned Prediction Formulation

> **Definition:** [Flow Regime State]
> A *flow regime state* $s \in \mathcal{S}$ is a tuple:
> 
> $$
> s = (M_\infty, Re, \alpha, \Gamma, \tau) \in \mathcal{S}
> <!-- label: eq:state -->
> $$
> 
>  where:
> 
- $M_\infty$: free-stream Mach number
- $Re$: Reynolds number based on chord length
- $\alpha$: angle of attack
- $\Gamma \subset \R^d$: geometric description of the aerodynamic body (airfoil coordinates or wing surface mesh)
- $\tau \in \{laminar, transitional, fully turbulent, separated\}$: flow topology type

> **Definition:** [Expert Solver]
> An *expert solver* $f_i: \mathcal{S} \to \mathcal{O}$ maps a flow regime state $s$ to an observable output:
> 
> $$
> f_i(s) = \big( C_L(s), C_D(s), C_M(s), \mathbf{C}_p(s; \Gamma_w) \big) \in \mathcal{O}
> <!-- label: eq:expert -->
> $$
> 
>  where $C_L$ is lift coefficient, $C_D$ is drag coefficient, $C_M$ is moment coefficient, and $\mathbf{C}_p(s; \Gamma_w)$ is the pressure coefficient distribution over the aerodynamic surface.

\assumptionTag{1} **(Deterministic Experts)**: Each expert $f_i$ is a deterministic function of the flow regime state $s$, though different experts may produce different outputs for the same $s$.
This abstracts away numerical noise below machine precision; for cases where numerical noise is non-negligible (e.g., under-resolved LES), we treat multiple realizations as distinct experts.

\assumptionTag{2} **(Observable Domain)**: The output space $\mathcal{O}$ is a compact metric space with metric $d_{\mathcal{O}}$, e.g., the $L^2$ norm of pressure coefficient differences plus absolute lift/drag/moment differences:

$$
d_{\mathcal{O}}(\mathbf{o}_1, \mathbf{o}_2) = \frac{|C_{L,1} - C_{L,2}|}{\max(|C_{L,1}|,1)} + \frac{|C_{D,1} - C_{D,2}|}{\max(|C_{D,1}|,1)} + \norm{\mathbf{C}_{p,1} - \mathbf{C}_{p,2}}_{L^2(\Gamma_w)}
<!-- label: eq:metric -->
$$

### Expert Categories

We distinguish three categories of experts:

1. **Traditional CFD experts** $\mathcal{F}_{trad} = \{f_1^{RANS}, f_2^{LES}, f_3^{DES}, ...\}$: Physically motivated solvers with known assumptions and convergence properties.
2. **Neural CFD experts** $\mathcal{F}_{NN} = \{f_1^{PINN}, f_2^{FNO}, f_3^{GNN}, f_4^{NN-closure}, ...\}$: Data-driven solvers with learned parameters.
3. **Ground-truth anchors** $\mathcal{F}_{GT} = \{f_1^{exp}\}$: Wind tunnel or flight test measurements at specific states.

\assumptionTag{3} **(Ground-Truth Anchor)**: The wind tunnel expert $f^* = f_1^{exp}$ provides unbiased measurements with known Gaussian uncertainty $\sigma_{exp}^2(s)$ at states $s \in \mathcal{S}_{exp} \subset \mathcal{S}$.
This is the standard treatment of experimental data in aerodynamics [cite].

### The Quality Certification Problem

Given a geometry $\Gamma$, a set of $M$ experts $\{f_1, ..., f_M\}$, and ground-truth anchors at states $\mathcal{S}_{exp}$, the SCX quality certification problem is:

1. **Detection**: Can we bound the probability of missing a systematic error in any expert?
2. **Attribution**: When experts disagree, can we identify which expert(s) are in error?
3. **Ranking**: Can we quantitatively rank experts by quality on known benchmarks?
4. **Extrapolation**: What quality guarantees transfer to states $s \notin \mathcal{S}_{exp}$?

## Theorem 1: SCX Noise Detection for CFD

We now prove the core noise detection theorem that bounds the probability of missing systematic errors when $M$ solvers are applied to the same aerodynamic geometry.

### Setup

Consider $M$ experts $\{f_1, ..., f_M\}$ applied to a geometry $\Gamma$ at $K$ distinct flow states $\{s_1, ..., s_K\}$.
Let $d_{ij}^{(k)} = d_{\mathcal{O}}(f_i(s_k), f_j(s_k))$ be the pairwise discrepancy between experts $i$ and $j$ at state $s_k$.

> **Definition:** [Systematic Error]
> Expert $i$ has a *systematic error* of magnitude $\delta > 0$ at state $s$ relative to ground truth $f^*(s)$ if:
> 
> $$
> d_{\mathcal{O}}(f_i(s), f^*(s)) > \delta
> <!-- label: eq:syserr -->
> $$

\assumptionTag{4} **(Pairwise Detectability)**: If an expert $i$ has systematic error $> \delta$ at state $s$, then for at least fraction $\gamma \in (0, 1]$ of other experts $j \neq i$, we have $d_{ij}(s) > \delta/2$.

*Justification:* If $f_i$ deviates from ground truth by more than $\delta$, and most other experts are within $\delta/2$ of ground truth (i.e., they are ``good''), then by triangle inequality $d_{ij} \geq d(f_i, f^*) - d(f_j, f^*) > \delta - \delta/2 = \delta/2$.
This assumption formalizes the intuition that a bad solution looks different from most good solutions.

### Theorem Statement

> **Theorem:** [SCX Noise Detection Bound for CFD] <!-- label: thm:noise -->
> \rigorFull
> Let $M \geq 3$ experts be applied to $K$ independent flow states.
> Assume \assumptionTag{4} holds with detectability fraction $\gamma$.
> Define the consensus indicator for expert $i$ at state $k$:
> 
> $$
> C_i^{(k)} = \indicator\left( \frac{1}{M-1}\sum_{j \neq i} \indicator(d_{ij}^{(k)} \leq \delta/2) \geq 1 - \theta \right)
> <!-- label: eq:consensus -->
> $$
> 
> where $\theta \in (0, 1-\gamma]$ is a consensus threshold.
> Let $E_i$ be the event that expert $i$ has systematic error $> \delta$ at a randomly chosen state but is not detected (i.e., $C_i = 1$ even though error $> \delta$).
> Then:
> 
> $$
> \Pbb(E_i) \leq \exp\left( -2 (M-1) \left( \gamma - \theta \right)^2 \right)
> <!-- label: eq:noise_bound -->
> $$

> **Proof:** Fix a state $s_k$ where expert $i$ has systematic error $> \delta$.
> By \assumptionTag{4}, for at least $\gamma (M-1)$ other experts $j$, we have $d_{ij}^{(k)} > \delta/2$.
> Let $X_j = \indicator(d_{ij}^{(k)} \leq \delta/2)$ for $j \neq i$.
> Then $\E[X_j] \geq 1-\gamma$ for the ``good'' experts (those within $\delta/2$ of ground truth), but more importantly, the fraction of experts with $X_j = 1$ among the $M-1$ other experts is at most $1 - \gamma$.
> 
> For the consensus to falsely indicate no systematic error, we need at least $(1-\theta)(M-1)$ of the $M-1$ other experts to satisfy $d_{ij} \leq \delta/2$, i.e., $X_j = 1$.
> Let $\bar{X} = \frac{1}{M-1}\sum_{j \neq i} X_j$.
> The false consensus event is $\bar{X} \geq 1 - \theta$.
> 
> Under the null that expert $i$ has systematic error, the expected fraction of close experts is $\E[\bar{X}] \leq 1 - \gamma$.
> By Hoeffding's inequality for $M-1$ bounded random variables $X_j \in [0, 1]$:
> 
> $$
> \Pbb\left( \bar{X} - \E[\bar{X}] \geq \gamma - \theta \right) \leq \exp\left( -2(M-1)(\gamma - \theta)^2 \right)
> <!-- label: eq:hoeffding -->
> $$
> 
> Since $\E[\bar{X}] \leq 1-\gamma$, we have $\bar{X} \geq 1-\theta \implies \bar{X} - \E[\bar{X}] \geq (1-\theta) - (1-\gamma) = \gamma - \theta$, which gives the bound in ( [ref]).

> **Remark:** [Interpretation for Neural CFD]
> <!-- label: rem:nn_interpretation -->
> The bound in Theorem [ref] is exponentially decreasing in $M$ and $(\gamma-\theta)^2$.
> For neural CFD:
> 
1. **Many traditional experts** $\Rightarrow$ large $M$ $\Rightarrow$ strong detection.
2. **Training data contamination** manifests as neural expert $i$ agreeing too well with training-distribution states but diverging on out-of-distribution states---this becomes detectable when traditional experts disagree with the neural prediction.
3. **Mesh dependency** appears as systematic error that varies with mesh resolution; multiple mesh resolutions provide the necessary expert diversity.
4. **Turbulence model mismatch** surfaces when a learned closure disagrees with wind tunnel data but traditional RANS with different closures bracket the experimental result.

\limitationTag{1} The Hoeffding bound assumes independence between expert errors, which is an idealization. In practice, experts share physical assumptions and may exhibit correlated errors.
This can be partially addressed using an effective sample size $M_{eff} = M/(1 + (M-1)\bar)$ where $\bar$ is average pairwise error correlation, estimable via bootstrap [cite].
The exponential convergence rate in $M$ is preserved with a modified constant.

> **Corollary:** [Joint Detection Across States] <!-- label: cor:joint -->
> \rigorPartial
> For $K$ independent flow states, the probability of failing to detect a systematically erroneous expert at any state is bounded by:
> 
> $$
> \Pbb(miss at any  s_k) \leq K \exp\left( -2(M-1)(\gamma - \theta)^2 \right)
> <!-- label: eq:joint -->
> $$

This follows from the union bound over $K$ states. For $K = 10$ typical benchmark states, $M = 8$ experts, $\gamma = 0.5$, $\theta = 0.2$: $\Pbb(miss) \leq 10 \cdot e^{-2 \cdot 7 \cdot 0.09} = 10 \cdot e^{-1.26} \approx 10 \cdot 0.284 = 2.84$, which exceeds $1$---the union bound is too loose for practical use.
A tighter bound via Slepian's inequality or Monte Carlo calibration is needed in practice.

\limitationTag{2} The union bound in Corollary [ref] is conservative and becomes vacuous for moderate $K$ and $M$.
In practice, we recommend Bonferroni-Holm correction or permutation testing on the actual expert discrepancy matrix.

## Theorem 2: Unidentifiability of Error Sources in Neural CFD

When a neural CFD solver disagrees with wind tunnel data, practitioners and reviewers naturally ask: *what caused the error?*
This theorem establishes a fundamental limit: without declared assumptions, the error source is unidentifiable.

### Setup

Consider a neural CFD solver $f_{NN}$ with learnable parameters $\bm$ trained on dataset $\mathcal{D}$.
The error $d_{\mathcal{O}}(f_{NN}(s), f^*(s))$ at test state $s \notin \mathcal{D}$ can arise from multiple distinct sources:

1. **Architectural error** $\epsilon_{arch}$: The neural network class cannot represent the true solution operator with any parameter setting.
2. **Training data insufficiency** $\epsilon_{data}$: The training set $\mathcal{D}$ does not adequately cover the test flow regime.
3. **Optimization error** $\epsilon_{opt}$: Training converged to a local minimum rather than the global optimum.
4. **Turbulence model error** $\epsilon_{turb}$: Even the ground-truth physical model (e.g., RANS equations) is an approximation.
5. **Numerical discretization error** $\epsilon_{disc}$: The mesh or time step used in training differs from the reference.

Let $\mathcal{E} = \{\epsilon_{arch}, \epsilon_{data}, \epsilon_{opt}, \epsilon_{turb}, \epsilon_{disc}\}$ be the set of possible error sources.

### Theorem Statement

> **Theorem:** [Unidentifiability of Neural CFD Error Sources] <!-- label: thm:unident -->
> \rigorFull
> Let $f_{NN}$ be a neural CFD solver with observed test error $\Delta = d_{\mathcal{O}}(f_{NN}(s), f^*(s)) > 0$.
> Without declared assumptions specifying which error sources are bounded, there exist at least two distinct partitions of $\Delta$ among $\mathcal{E}$ that are observationally equivalent---i.e., produce the same observed output $f_{NN}(s)$ but attribute the error to different causes.

> **Proof:** We construct two distinct error source attributions that produce identical observed behavior.
> 
> **Attribution A (Architecture blame):**
> Assume that $\epsilon_{data} = \epsilon_{opt} = \epsilon_{turb} = \epsilon_{disc} = 0$, and the entire error $\Delta$ is due to $\epsilon_{arch}$:
> 
> $$
> f_{NN}^{(A)}(s) = f_{true}(s) + \epsilon_{arch}, \quad \norm{\epsilon_{arch}} = \Delta
> <!-- label: eq:attrA -->
> $$
> 
> 
> **Attribution B (Data insufficiency blame):**
> Assume $\epsilon_{arch} = \epsilon_{opt} = \epsilon_{turb} = \epsilon_{disc} = 0$, but $\epsilon_{data}$ accounts for the error.
> However, training data insufficiency means the network parameters learned from $\mathcal{D}$ differ from the optimal parameters that would be learned from a sufficiently rich dataset $\mathcal{D}'$:
> 
> $$
> f_{NN}^{(B)}(s) = f_{NN}(s; \bm(\mathcal{D}')) + \epsilon_{data}, \quad \norm{\epsilon_{data}} = \Delta
> <!-- label: eq:attrB -->
> $$
> 
> 
> **Observational equivalence:**
> Both attributions yield the same predicted output $f_{NN}(s) = f_{NN}^{(A)}(s) = f_{NN}^{(B)}(s)$ and the same test error $\Delta$.
> Without further assumptions---such as:
> 
- \assumptionTag{A1} A known upper bound on $\norm{\epsilon_{arch}}$ from universal approximation analysis,
- \assumptionTag{A2} A known upper bound on $\norm{\epsilon_{data}}$ from dataset coverage analysis,
- \assumptionTag{A3} A known upper bound on $\norm{\epsilon_{turb}}$ from turbulence model validation,

> ---the attributions are indistinguishable from output observations alone.
> 
> **Generalization to $|\mathcal{E}|$ sources:**
> Let $\mathbf{e} = (e_1, ..., e_5)^T$ be the vector of error source magnitudes.
> Any vector $\mathbf{e}$ satisfying $\sum_i e_i = \Delta$ and the constraint that changing which source is ``responsible'' does not change the prediction is observationally equivalent.
> The set of such vectors is a $4$-dimensional simplex, and without additional constraints (assumptions), any point on this simplex is a valid attribution.

> **Remark:** [Practical Implication for Neural CFD Papers]
> <!-- label: rem:practical -->
> Theorem [ref] has a direct consequence for neural CFD research: every paper claiming a neural method ``improves'' CFD must explicitly declare which error sources it addresses and which it assumes bounded.
> Without such declarations, a reviewer cannot determine whether a reported improvement is due to the claimed innovation or to favorable training data, better optimization, or a different discretization.
> 
> \assumptionTag{5} **(Required Declarations for Neural CFD Papers)**: For any neural CFD contribution, the following must be declared:
> 
1. Training data coverage: which flow regimes are in $\mathcal{D}$ and which are test-only.
2. Architecture capacity: explicit statement of known approximation error bounds, or their absence.
3. Turbulence model baseline: which physical model underlies the training data, and its known limitations.
4. Optimization guarantee: whether training reached a local or global optimum, and how this was assessed.
5. Mesh/convergence: mesh resolution used in training, and tests of prediction quality at different resolutions.

\limitationTag{3} The construction in Theorem [ref] uses two extreme attributions. Realistic scenarios involve partial contributions from multiple sources, and the theorem establishes a *lower bound* on unidentifiability: even in the simplest case, error source attribution requires assumptions. In practice, the ambiguity is larger.

## Theorem 3: Situs Encoding Guarantee for Aerodynamic Geometry

The Situs encoding [cite] maps physical objects into a metric space that respects geometric symmetries.
For aerodynamic applications, we need guarantees that the encoding preserves the information relevant to flow prediction.

### Situs Encoding for Airfoils and Wings

> **Definition:** [Situs Encoding of an Airfoil]
> <!-- label: def:situs_airfoil -->
> Let $\Gamma \subset \R^2$ be an airfoil profile defined by $N$ coordinate points $\{(\xi_i, \zeta_i)\}_{i=1}^N$ in normalized chord coordinates.
> The Situs encoding $\Phi: \Gamma \mapsto \mathbf{z} \in \mathcal{Z} \subset \R^{d_z}$ is:
> 
> $$
> \Phi(\Gamma) = \left[ \tilde{a}_0, \tilde{b}_0, \tilde{a}_1, \tilde{b}_1, ..., \tilde{a}_K, \tilde{b}_K \right]
> <!-- label: eq:situs_encode -->
> $$
> 
> where $\{\tilde{a}_k, \tilde{b}_k\}_{k=0}^K$ are the amplitude-normalized and translation-invariant Fourier coefficients of the camber line and thickness distribution, defined as:
> 
> $$
> \tilde{a}_k &= \frac{a_k}{\max_{j} |a_j| + \epsilon}, \quad \tilde{b}_k = \frac{b_k}{\max_{j} |b_j| + \epsilon} 

> a_k &= \frac{1} \int_{0}^{2\pi} \zeta_{camber}(\theta) \cos(k\theta) d\theta, \quad b_k = \frac{1} \int_{0}^{2\pi} \zeta_{camber}(\theta) \sin(k\theta) d\theta
> <!-- label: eq:fourier_coeffs -->
> $$
> 
> where $\zeta_{camber}(\theta) = (\zeta_{upper}(\theta) + \zeta_{lower}(\theta))/2$ paramaterized by $\theta \in [0, 2\pi]$.

\assumptionTag{6} **(Smooth Geometry)**: The airfoil profile $\Gamma$ is $C^2$-continuous (twice differentiable). This holds for all standard NACA airfoils and most industrial designs. Discontinuities (e.g., sharp trailing edges) are handled by Fourier approximation with controlled truncation error.

\assumptionTag{7} **(Flow Sensitivity to Geometry)**: The aerodynamic coefficients $C_L, C_D, C_M$ are Lipschitz continuous in the Situs encoding of the geometry. Specifically, there exists $L_g > 0$ such that for any two geometries $\Gamma_1, \Gamma_2$:

$$
d_{\mathcal{O}}(f(\Gamma_1), f(\Gamma_2)) \leq L_g \cdot \norm{\Phi(\Gamma_1) - \Phi(\Gamma_2)}_2
<!-- label: eq:lipschitz_geom -->
$$

for the same flow conditions $(M_\infty, Re, \alpha)$ and the same expert solver $f$.

*Justification:* This is a regularity assumption on the Navier-Stokes solution operator. For subsonic attached flows, smooth geometry perturbations produce smooth changes in pressure distribution [cite]. For transonic flows with shocks, the Lipschitz constant $L_g$ may be large but finite since shock location varies continuously with geometry [cite].

> **Theorem:** [Situs Encoding Guarantee for Aerodynamics] <!-- label: thm:situs -->
> \rigorFull
> Let $\Gamma$ be an airfoil profile satisfying \assumptionTag{6} and \assumptionTag{7}.
> Let $\hat_K$ be the $K$-term Situs reconstruction:
> 
> $$
> \hat_K = \Phi^{-1}\left( [\tilde{a}_0, \tilde{b}_0, ..., \tilde{a}_K, \tilde{b}_K, 0, ...] \right)
> <!-- label: eq:reconstruction -->
> $$
> 
> where coefficients beyond $K$ are zeroed.
> Then for any $C^2$ airfoil, the truncation error in the Situs space satisfies:
> 
> $$
> \norm{\Phi(\Gamma) - \Phi(\hat_K)}_2 \leq \frac{C_\Gamma}{K^{3/2}}
> <!-- label: eq:truncation -->
> $$
> 
> where $C_\Gamma$ depends on the maximum curvature and camber of $\Gamma$.
> Consequently, the aerodynamic prediction error due to geometry truncation is bounded by:
> 
> $$
> d_{\mathcal{O}}(f(\Gamma), f(\hat_K)) \leq L_g \cdot \frac{C_\Gamma}{K^{3/2}}
> <!-- label: eq:aero_bound -->
> $$

> **Proof:** For a $C^2$ periodic function (the camber line after parameterization), the Fourier coefficients decay as $|a_k|, |b_k| = O(k^{-2})$ [cite].
> Specifically, there exists $C_0$ such that $|a_k|, |b_k| \leq C_0/k^2$ for all $k \geq 1$.
> 
> The Situs encoding normalizes by $\max_j |a_j| + \epsilon$, so the normalized coefficients decay similarly:
> 
> $$
> |\tilde{a}_k|, |\tilde{b}_k| \leq \frac{C_0}{(\max_j |a_j| + \epsilon) k^2}
> $$
> 
> 
> The $L^2$ norm of the truncated tail is:
> 
> $$
> \norm{\Phi(\Gamma) - \Phi(\hat_K)}_2^2 = \sum_{k=K+1}^ (\tilde{a}_k^2 + \tilde{b}_k^2) \leq 2 \sum_{k=K+1}^ \left(\frac{C_0}{C_m k^2}\right)^2
> $$
> 
> where $C_m = \max_j |a_j| + \epsilon$.
> 
> For large $K$, $\sum_{k=K+1}^ k^{-4} \leq \int_K^ x^{-4} dx = \frac{1}{3K^3}$.
> Thus:
> 
> $$
> \norm{\Phi(\Gamma) - \Phi(\hat_K)}_2 \leq \sqrt{\frac{2 C_0^2}{C_m^2}} \cdot \frac{1}{\sqrt{3} K^{3/2}} = \frac{C_\Gamma}{K^{3/2}}
> <!-- label: eq:bound_final -->
> $$
> 
> with $C_\Gamma = \sqrt{2/3} \cdot C_0 / C_m$.
> 
> The aerodynamic bound follows directly from \assumptionTag{7}.

> **Remark:** [Symmetry Preservation]
> <!-- label: rem:symmetry -->
> The Situs encoding preserves three geometric symmetries crucial for aerodynamics:
> 
1. **Reflection:** Camber sign reversal corresponds to flipping $\{\tilde{a}_k\}$ signs, which preserves the $L^2$ norm.
2. **Scaling:** Amplitude normalization $(\max_j |a_j| + \epsilon)^{-1}$ makes the encoding scale-invariant.
3. **Translation:** The zero-frequency term $a_0$ corresponds to mean camber offset; its normalization eliminates translation sensitivity.

\limitationTag{4} The bound $O(K^{-3/2})$ assumes $C^2$ geometry. For airfoils with sharp curvature changes (e.g., highly cambered supercritical airfoils), the effective smoothness order may be lower, yielding slower convergence. The constant $C_\Gamma$ must be estimated per geometry class.

\limitationTag{5} The Lipschitz constant $L_g$ in \assumptionTag{7} is not known a priori and must be estimated empirically via finite differences on a calibration set of geometries. We provide an estimation procedure in the experimental protocol (§8).

## Cercis Score for Aerodynamic Simulation

The Cercis score [cite] quantifies the quality of an expert through two axes: **Q** (accuracy on benchmarks) and **N** (novelty of coverage).
We adapt this to aerodynamic CFD.

### Accuracy Score Q

Let $\mathcal{B} = \{b_1, ..., b_{|\mathcal{B}|}\}$ be a set of standard aerodynamic benchmark cases.
For each benchmark $b = (M_\infty, Re, \Gamma)$, we have reference data (wind tunnel or highly resolved CFD) for $C_L, C_D, C_M, \mathbf{C}_p$.

> **Definition:** [Accuracy Score]
> For expert $f_i$, the accuracy score on benchmark set $\mathcal{B}$ is:
> 
> $$
> Q(f_i; \mathcal{B}) = 1 - \frac{1}{|\mathcal{B}|} \sum_{b \in \mathcal{B}} \min\left(1, \frac{E_i(b)}{\tau_b}\right)
> <!-- label: eq:qscore -->
> $$
> 
> where:
> 
- $E_i(b) = d_{\mathcal{O}}(f_i(s_b), f^*(s_b))$ is the error on benchmark $b$.
- $\tau_b$ is a benchmark-specific tolerance (see Table [ref]).

> $Q \in [0, 1]$, with $Q=1$ indicating errors below tolerance on all benchmarks.

[Table omitted — see original .tex]

### Novelty Score N

The novelty score measures how extensively a method has been validated across flow regimes.

> **Definition:** [Novelty Score]
> For expert $f_i$ with published validation states $\mathcal{S}_i^{pub} \subset \mathcal{S}$:
> 
> $$
> N(f_i) = \frac{|\mathcal{S}_i^{pub} \setminus \mathcal{S}_{ref}|}{|\mathcal{S}_{target}|}
> <!-- label: eq:nscore -->
> $$
> 
> where $\mathcal{S}_{ref}$ is the set of flow states for which traditional CFD is considered reliable (e.g., attached subsonic flows with $Re \leq 10^7$), and $\mathcal{S}_{target}$ is the target coverage of interest (e.g., full flight envelope including transonic buffet and high-lift conditions).

### Cercis Score

> **Definition:** [Cercis Score]
> 
> $$
> \mathcal{C}(f_i) = Q(f_i; \mathcal{B}) \cdot N(f_i)
> <!-- label: eq:cercis -->
> $$

 The multiplicative form penalizes methods that achieve high accuracy only on easy regimes ($N$ small) and methods that claim broad applicability without demonstrated accuracy ($Q$ small).

### Ranking of Published Neural CFD Methods

Table [ref] presents estimated Cercis scores for published neural CFD methods, based on reported results. Where a method has not reported results on a benchmark, we assign $E_i(b) = \tau_b$ (i.e., error equals tolerance threshold, yielding zero partial credit).
\limitationTag{6} Scores are approximate due to inconsistent reporting across papers; we urge authors to adopt standardized reporting.

[Table omitted — see original .tex]

 The traditional RANS baselines achieve higher Cercis scores due to broader validation across benchmarks, even though neural methods may achieve higher accuracy on specific cases.
This illustrates the SCX philosophy: **quality is not just accuracy on cherry-picked cases, but demonstrated reliability across the operational envelope**.

\limitationTag{7} The Cercis ranking in Table [ref] uses approximate values extracted from published figures and text. A definitive ranking requires recomputing all methods on the same benchmark suite with consistent metrics, which we propose as a community effort in §8.

## Multi-Expert Architecture with Yajie Consensus

We now describe a practical architecture for SCX-based quality auditing of CFD predictions.

### Expert Ensemble

The multi-expert system comprises:

1. **E1:** $k$-$\omega$ SST RANS (widely validated turbulence model).
2. **E2:** $k$-$\varepsilon$ RANS (alternative closure, known to differ in adverse pressure gradients).
3. **E3:** Spalart-Allmaras RANS (efficient one-equation model).
4. **E4:** LES (scale-resolving, computationally expensive but high fidelity).
5. **E5:** FNO-based neural operator (speed-oriented).
6. **E6:** GNN-based mesh solver (geometry-flexible).
7. **E7:** PINN with RANS loss (physics-constrained).
8. **E8:** Wind tunnel data (ground-truth anchor, available only at $\mathcal{S}_{exp}$).

### Yajie Consensus Mechanism

The Yajie consensus mechanism [cite] processes expert outputs through two stages:

**Stage 1: Discrepancy Matrix.**
For each state $s_k$, compute the $M \times M$ pairwise discrepancy matrix $\mathbf{D}^{(k)}$ with entries $D_{ij}^{(k)} = d_{\mathcal{O}}(f_i(s_k), f_j(s_k))$.

**Stage 2: Consensus Score.**
For each expert $i$, compute the consensus score:

$$
S_i^{(k)} = \frac{1}{M-1} \sum_{j \neq i} w_{ij} \cdot \kappa(D_{ij}^{(k)})
<!-- label: eq:yajie_score -->
$$

where $w_{ij}$ are expert-pair weights reflecting known reliability differences, and $\kappa(d) = \exp(-d^2/\sigma^2)$ is a Gaussian kernel with bandwidth $\sigma$ set to the median discrepancy.

**Stage 3: Anomaly Flagging.**
Flag expert $i$ at state $k$ if $S_i^{(k)} < \tau_{consensus}$, where $\tau_{consensus} = 0.5$ by default.

\assumptionTag{8} **(Yajie Anchoring)**: The wind tunnel expert (E8) receives weight $w_{8j} = \lambda \cdot w_{base}$ with $\lambda \geq 2$ when its measurement uncertainty $\sigma_{exp}(s_k)$ is below a threshold.
This reflects the privileged status of experimental data while acknowledging its uncertainty.

### Workflow

\begin{algorithm}[htbp]
*Caption:* SCX Audit for a New Aerodynamic Simulation
<!-- label: alg:scx_cfd -->
\begin{algorithmic}[1]
\State **Input:** Geometry $\Gamma$, flow states $\{s_1, ..., s_K\}$, experts $\{f_1, ..., f_M\}$
\State **Output:** Quality report with anomaly flags, consensus scores, Cercis estimate
\For{$k = 1$ to $K$}
    \For{$i = 1$ to $M$}
        \State Compute $f_i(s_k)$ --- expert prediction
    \EndFor
    \State Compute discrepancy matrix $\mathbf{D}^{(k)}$
    \State Compute Yajie consensus scores $\{S_i^{(k)}\}$
    \State Flag anomalous experts (Theorem [ref] check)
\EndFor
\State For states $s_k \in \mathcal{S}_{exp}$ with wind tunnel data:
\State \quad Compute per-expert errors, identify systematic errors
\State \quad Apply Theorem [ref] --- note which error sources are unidentifiable
\State Compute Cercis score $\mathcal{C}(f_i)$ for each non-anchor expert
\State \Return Quality report
\end{algorithmic}
\end{algorithm}

\limitationTag{8} The multi-expert architecture requires running all $M$ experts for each state, which is computationally expensive. However, (a) many traditional CFD solutions can be precomputed and cached for standard geometries, (b) neural experts are fast at inference time ($< 1$ second per state), and (c) the audit is designed for certification workflows where computational cost is secondary to reliability.

## Experimental Protocol

We propose a standardized experimental protocol for evaluating neural CFD methods under SCX audit.
This protocol is designed for reproducibility and fair comparison.

### Benchmark Suite

[Table omitted — see original .tex]

### Mesh Convergence Protocol

To assess mesh dependency (a key concern for neural solvers), we define four mesh levels:

1. **Coarse:** $\sim 10^4$ cells (typical of neural CFD training).
2. **Medium:** $\sim 10^5$ cells (standard engineering RANS).
3. **Fine:** $\sim 10^6$ cells (mesh-converged RANS).
4. **Ultra-fine:** $\sim 10^7$ cells (LES/DNS resolution).

 The mesh convergence index (MCI) is computed via Richardson extrapolation [cite]:

$$
MCI = \frac{|f_{fine} - f_{medium}|}{r^p - 1}
<!-- label: eq:mci -->
$$

where $r$ is the refinement ratio and $p$ is the observed order of accuracy.
Neural solvers must demonstrate that their prediction error does not exceed the MCI of traditional solvers at equivalent mesh resolution.

### Neural Architecture Ablations

\assumptionTag{9} **(Ablation Protocol)**: For each neural CFD method, report results under the following ablations:

1. **Training set size**: $25\%, 50\%, 75\%, 100\%$ of available training data.
2. **Training flow regime**: train on subsonic only, test on transonic (and vice versa).
3. **Architecture depth**: vary number of layers/parameters by factors of $2\times$ and $0.5\times$.
4. **With and without physics loss**: PINNs with and without the PDE residual term.
5. **Mesh resolution mismatch**: train on one mesh level, test on another.

### Turbulence Model Variation

For traditional CFD baselines, run the following turbulence model variants:

- $k$-$\omega$ SST (Menter, 1994)
- $k$-$\varepsilon$ realizable (Shih et al., 1995)
- Spalart-Allmaras (Spalart \& Allmaras, 1992)
- Transition SST ($\gamma$-$Re_\theta$)
- Scale-Adaptive Simulation (SAS)

### Evaluation Metrics

1. **Integral quantities:** $\epsilon_{C_L} = |C_L^{pred} - C_L^{ref}|$, similarly for $C_D$, $C_M$.
2. **Pressure distributions:** $L^2$ error $\norm{\mathbf{C}_p^{pred} - \mathbf{C}_p^{ref}}_{L^2(\Gamma_w)} / \norm{\mathbf{C}_p^{ref}}_{L^2(\Gamma_w)}$.
3. **Shock location:** For transonic cases, $\Delta x_{shock} / c$, the chord-normalized difference in shock position.
4. **Separation point:** For high-angle cases, $\Delta x_{sep} / c$, the chord-normalized difference in separation location.
5. **Consensus score:** Yajie $S_i^{(k)}$ as defined in ( [ref]).
6. **Cercis score:** $\mathcal{C}(f_i) = Q(f_i) \cdot N(f_i)$.

### Assumption Declaration Template

Following Theorem [ref], every neural CFD submission must include:

> **Assumption Declaration (SCX-CFD v1.0)**
> 
>  **A1. Data Coverage:** [Flow regimes in training; regimes reserved for testing]
>  **A2. Architecture Capacity:** [Known bounds or absence thereof]
>  **A3. Physical Model:** [Underlying equations; known limitations of these equations]
>  **A4. Optimization:** [Convergence criterion; evidence of local vs global optimum]
>  **A5. Discretization:** [Training mesh resolution; tests at other resolutions]
>  **A6. Reproducibility:** [Code availability; random seeds; hardware used]

## Discussion

### Relationship to Neural Operator Theory

Neural operators [cite] provide a mathematical framework for learning mappings between infinite-dimensional function spaces, which is directly applicable to CFD where solutions are functions of space and time.
Theorem [ref] complements neural operator theory by providing a *detection* guarantee: while neural operators can theoretically approximate the Navier-Stokes solution operator (universal approximation in appropriate Sobolev spaces), the SCX framework detects when a trained operator *fails* to do so in practice.

The key connection is that neural operator convergence rates ($O(N^{-\alpha})$ where $N$ is training samples and $\alpha$ depends on smoothness) provide an upper bound on $\epsilon_{arch}$ in Theorem [ref], partially resolving one source of unidentifiability when explicit convergence analysis is available.

### The Turbulence Modeling Closure Problem

Turbulence modeling remains the central challenge in CFD [cite].
The closure problem---that the Reynolds stresses $\overline{u_i' u_j'}$ introduce more unknowns than equations---has no closed-form solution.
All turbulence models, whether traditional algebraic closures or learned neural closures, are approximations.

The SCX framework treats this honestly: \assumptionTag{3} in the RANS equations is explicitly the turbulence model assumption, and Theorem [ref] clarifies that when a neural closure disagrees with wind tunnel data, the error may originate in the RANS framework itself rather than in the neural implementation.
This prevents the common pitfall of ``blaming the neural network'' when the underlying physical model is the limiting factor.

### Path to Certified Neural CFD for Industrial Use

Industrial adoption of neural CFD requires certification---evidence that predictions are reliable for safety-critical design decisions.
The SCX framework contributes three components toward this goal:

1. **Detection** (Theorem [ref]): Automated flagging of anomalous predictions when multiple experts disagree.
2. **Delineation** (Theorem [ref]): Explicit boundaries of what can and cannot be concluded from disagreement.
3. **Benchmarking** (Cercis score, §6): Standardized, reproducible comparison across methods.

 We do *not* claim that SCX provides certification by itself. Certification additionally requires:

- Formal verification of solver correctness (analogous to the Lax equivalence theorem for traditional methods).
- Bounds on extrapolation error to unseen geometries and flow conditions.
- Regulatory acceptance (e.g., EASA/FAA certification processes).

### Limitations

We explicitly acknowledge the following limitations of the SCX CFD audit framework:

1. **(Computational cost)** Running $M \geq 8$ experts on $K$ benchmark cases requires significant computational resources, though amortized over a certification process this is acceptable.
2. **(Correlated expert errors)** Theorem [ref] assumes independent errors. Traditional RANS models share physical assumptions and produce correlated errors, particularly in separated flows where all RANS closures fail similarly. The effective $M_{eff}$ correction partially addresses this but requires empirical correlation estimation.
3. **(Wind tunnel coverage)** Ground-truth anchors exist only at specific $M_\infty$, $Re$, $\alpha$ combinations. Extrapolation to flight conditions requires additional assumptions beyond the scope of this paper.
4. **(RANS limitation)** All traditional experts based on RANS share the fundamental limitation of Reynolds averaging: unsteady phenomena (buffet, flutter, vortex shedding) cannot be captured. Neural closures trained on RANS data inherit this limitation.
5. **(Cercis score subjectivity)** The benchmark selection and tolerance thresholds in Table [ref] embed engineering judgment. Different applications (e.g., wind turbine vs. transonic wing design) may require different benchmarks and tolerances.
6. **(Situs Lipschitz estimation)** The constant $L_g$ in \assumptionTag{7} is problem-dependent. Our estimation via finite differences on calibration geometries provides a lower bound; the true $L_g$ may be larger for rarely encountered geometries.

### Future Work

Several directions emerge from this framework:

1. **Rigorous Situs Lipschitz estimation:** Derive $L_g$ analytically for simplified geometries (e.g., Joukowski airfoils) using conformal mapping and potential flow theory, then extend numerically to general geometries.
2. **Effective sample size calibration:** Develop a systematic procedure for estimating $\bar$ in the correlated-expert setting through designed perturbation experiments.
3. **Neural CFD certification suite:** Implement the experimental protocol (§8) as an automated benchmark suite with standardized input/output formats, enabling reproducible comparison across methods.
4. **Extrapolation bounds:** Extend Theorem [ref] to bound prediction quality at flow states $s \notin \mathcal{S}_{exp}$ using Lipschitz continuity of the solution operator in state space.
5. **Integration with turbulence model development:** Apply the SCX audit during turbulence model development to provide continuous quality monitoring and prevent regression.

## Conclusion

We have presented the SCX quality audit framework applied to neural computational fluid dynamics for finite element aerodynamics.
Three theorems---noise detection (§3), error source unidentifiability (§4), and Situs encoding guarantee (§5)---provide formal foundations for quality assessment.
The Cercis score (§6) enables quantitative comparison, and the multi-expert Yajie architecture (§7) provides a practical auditing workflow.

The framework does not claim that neural CFD is unreliable.
Rather, it provides the tools to *determine* when and why it is reliable.
By making assumptions explicit, errors detectable, and comparisons standardized, the SCX approach advances the path toward certified neural CFD for industrial aerodynamic design.

 **核心命题** (Core Proposition): 传统计算流体力学通过多专家冗余提供了隐含的质量保证（不同湍流模型、网格分辨率、数值格式）。神经CFD方法缺少这种保证。SCX审计框架通过显式化假设、检测系统误差、标准化基准测试，为神经CFD提供了缺失的质量证明层。

\begin{thebibliography}{99}

\bibitem{anderson2017fundamentals}
J.~D.~Anderson.
\newblock {\em Fundamentals of Aerodynamics}, 6th ed.
\newblock McGraw-Hill, 2017.

\bibitem{colesc1945tests}
D.~Coles and A.~E.~von~Doenhoff.
\newblock Tests of 24 airfoil sections at high Reynolds numbers.
\newblock NACA Technical Note, 1945.

\bibitem{cooke2009industrial}
A.~Cooke and E.~Fitzpatrick.
\newblock {\em Helicopter Test and Evaluation}.
\newblock Blackwell Science, 2009.

\bibitem{duraisamy2019turbulence}
K.~Duraisamy, G.~Iaccarino, and H.~Xiao.
\newblock Turbulence modeling in the age of data.
\newblock {\em Annual Review of Fluid Mechanics}, 51:357--377, 2019.

\bibitem{harris1981two}
C.~D.~Harris.
\newblock Two-dimensional aerodynamic characteristics of the NACA 0012 airfoil in the Langley 8-foot transonic pressure tunnel.
\newblock NASA TM-81927, 1981.

\bibitem{jameson1988aerodynamic}
A.~Jameson.
\newblock Aerodynamic design via control theory.
\newblock {\em Journal of Scientific Computing}, 3(3):233--260, 1988.

\bibitem{jin2021nsfnets}
X.~Jin, S.~Cai, H.~Li, and G.~E.~Karniadakis.
\newblock NSFnets (Navier-Stokes flow nets): Physics-informed neural networks for incompressible flows.
\newblock {\em Journal of Computational Physics}, 426:109951, 2021.

\bibitem{katznelson2004introduction}
Y.~Katznelson.
\newblock {\em An Introduction to Harmonic Analysis}, 3rd ed.
\newblock Cambridge University Press, 2004.

\bibitem{kovachki2021neural}
N.~Kovachki, Z.~Li, B.~Liu, K.~Azizzadenesheli, K.~Bhattacharya, A.~Stuart, and A.~Anandkumar.
\newblock Neural operator: Learning maps between function spaces.
\newblock {\em arXiv:2108.08481}, 2021.

\bibitem{ladson1988acquired}
C.~L.~Ladson.
\newblock Effects of independent variation of Mach and Reynolds numbers on the low-speed aerodynamic characteristics of the NACA 0012 airfoil section.
\newblock NASA TM-4074, 1988.

\bibitem{laflin2005summary}
K.~R.~Laflin et al.
\newblock Summary of data from the second AIAA CFD drag prediction workshop.
\newblock {\em Journal of Aircraft}, 42(5):1165--1178, 2005.

\bibitem{launder1974numerical}
B.~E.~Launder and D.~B.~Spalding.
\newblock The numerical computation of turbulent flows.
\newblock {\em Computer Methods in Applied Mechanics and Engineering}, 3(2):269--289, 1974.

\bibitem{li2020fourier}
Z.~Li, N.~Kovachki, K.~Azizzadenesheli, B.~Liu, K.~Bhattacharya, A.~Stuart, and A.~Anandkumar.
\newblock Fourier neural operator for parametric partial differential equations.
\newblock {\em arXiv:2010.08895}, 2020.

\bibitem{li2022learning}
Z.~Li, D.~Z.~Huang, B.~Liu, and A.~Anandkumar.
\newblock Fourier neural operator with learned deformations for PDEs on general geometries.
\newblock {\em arXiv:2207.05209}, 2022.

\bibitem{liang1986longitudinal}
K.-Y.~Liang and S.~L.~Zeger.
\newblock Longitudinal data analysis using generalized linear models.
\newblock {\em Biometrika}, 73(1):13--22, 1986.

\bibitem{ling2016reynolds}
J.~Ling, A.~Kurzawski, and J.~Templeton.
\newblock Reynolds averaged turbulence modelling using deep neural networks with embedded invariance.
\newblock {\em Journal of Fluid Mechanics}, 807:155--166, 2016.

\bibitem{menter1994two}
F.~R.~Menter.
\newblock Two-equation eddy-viscosity turbulence models for engineering applications.
\newblock {\em AIAA Journal}, 32(8):1598--1605, 1994.

\bibitem{murayama2006comparison}
M.~Murayama, Y.~Yokokawa, and K.~Yamamoto.
\newblock Comparison study of drag prediction for the 3rd CFD drag prediction workshop by structured and unstructured grid method.
\newblock AIAA Paper 2006-0390, 2006.

\bibitem{pfaff2020learning}
T.~Pfaff, M.~Fortunato, A.~Sanchez-Gonzalez, and P.~W.~Battaglia.
\newblock Learning mesh-based simulation with graph networks.
\newblock {\em arXiv:2010.03409}, 2020.

\bibitem{pope2000turbulent}
S.~B.~Pope.
\newblock {\em Turbulent Flows}.
\newblock Cambridge University Press, 2000.

\bibitem{raissi2019physics}
M.~Raissi, P.~Perdikaris, and G.~E.~Karniadakis.
\newblock Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations.
\newblock {\em Journal of Computational Physics}, 378:686--707, 2019.

\bibitem{roache1998verification}
P.~J.~Roache.
\newblock {\em Verification and Validation in Computational Science and Engineering}.
\newblock Hermosa Publishers, 1998.

\bibitem{schmitt2007advanced}
V.~Schmitt and F.~Charpin.
\newblock Pressure distributions on the ONERA M6 wing at transonic Mach numbers.
\newblock In {\em Experimental Data Base for Computer Program Assessment}, AGARD-AR-138, 2007.

\bibitem{smagorinsky1963general}
J.~Smagorinsky.
\newblock General circulation experiments with the primitive equations.
\newblock {\em Monthly Weather Review}, 91(3):99--164, 1963.

\bibitem{spalart1992one}
P.~R.~Spalart and S.~R.~Allmaras.
\newblock A one-equation turbulence model for aerodynamic flows.
\newblock AIAA Paper 92-0439, 1992.

\bibitem{spalart1997comments}
P.~R.~Spalart et al.
\newblock Comments on the feasibility of LES for wings, and on a hybrid RANS/LES approach.
\newblock In {\em Advances in DNS/LES}, 1997.

\bibitem{thuerey2020deep}
N.~Thuerey, K.~Weißenow, L.~Prantl, and X.~Hu.
\newblock Deep learning methods for Reynolds-averaged Navier-Stokes simulations of airfoil flows.
\newblock {\em AIAA Journal}, 58(1):25--36, 2020.

\bibitem{vassberg2008summary}
J.~C.~Vassberg et al.
\newblock Summary of the fourth AIAA CFD drag prediction workshop.
\newblock AIAA Paper 2008-6913, 2008.

\bibitem{scx_theory}
SCX.
\newblock SCX Theory: Formal foundations of the SCX quality audit framework.
\newblock Technical report, 2026.

\end{thebibliography}

## Appendix
## Assumption Map

Table [ref] provides a complete map of all assumptions declared in this paper, their types, and their dependencies.

[Table omitted — see original .tex]

## Detailed Proof of Theorem [ref]

\rigorPartial
We provide a more detailed treatment of Theorem [ref] accounting for expert error correlation.

Assume $M$ experts with pairwise error correlation $\rho_{ij} = \Corr(X_i, X_j)$ where $X_i = \indicator(d(f_i, f^*) > \delta/2)$.
The effective number of independent experts is [cite]:

$$
M_{eff} = \frac{M}{1 + (M-1)\bar}
<!-- label: eq:meff -->
$$

where $\bar = \frac{2}{M(M-1)}\sum_{i<j} \rho_{ij}$ is the average pairwise correlation.

Replacing $M$ with $M_{eff}$ in the Hoeffding bound yields:

$$
\Pbb(E_i) \leq \exp\left( -2 M_{eff} (\gamma - \theta)^2 \right)
<!-- label: eq:noise_corr -->
$$

 This bound is conservative when $\bar > 0$ (the typical case for traditional CFD experts that share physical assumptions).
A bootstrap procedure for estimating $\bar$ from the discrepancy matrix $\mathbf{D}$ is:

1. Resample $K$ states with replacement $B$ times.
2. For each bootstrap sample $b$, compute the vector of per-expert errors $\mathbf{e}^{(b)} \in \R^M$.
3. Estimate $\hat_{ij} = \Corr(\mathbf{e}_i, \mathbf{e}_j)$ across bootstrap samples.
4. Compute $\bar$ and $M_{eff}$.

 \limitationTag{13} This bootstrap estimate is itself noisy when $K$ is small. For practical SCX audits with $K \geq 20$, bootstrap estimation provides reasonable accuracy.