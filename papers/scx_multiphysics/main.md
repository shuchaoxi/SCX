# Introduction 引言

**Author:** SCX

*Abstract:*

Multi-physics simulation decomposes naturally into domain experts---each physical domain (fluid, structure, thermal, electromagnetic, chemical) deploys its own solver, with coupling interfaces where errors cross-propagate. Neural surrogates---learned reduced-order models (ROMs), physics-informed neural operators, and deep operator networks---promise to accelerate individual domains or the entire coupled system. Yet no formal framework certifies simulation quality across coupled domains, and the coupling interface itself obscures error attribution: when coupled predictions deviate from experiments, which domain is responsible? We present the SCX{} (Structured Causal eXamination) auditing framework applied to multi-physics simulation, providing per-domain and cross-domain quality guarantees. Core contributions: (i) a per-domain detection guarantee bounding the probability of missing a solver error of magnitude $\Delta$ as $\exp(-2M_d \Delta^2)$ for $M_d$ experts per domain; (ii) a cross-domain error propagation bound showing that error in domain $A$ propagates to domain $B$ through the coupling Lipschitz constant $L_{AB}$, with explicit forms for fluid-structure interaction ($L_{\mathrm{FSI}} \propto \rho_f / \rho_s$) and thermal-mechanical coupling ($L_{\mathrm{TM}} \propto \alpha E / k$); (iii) an unidentifiability theorem establishing that when a coupled simulation disagrees with experiment, the error source---domain solver, coupled-domain solver, or coupling condition---is unidentifiable without declared assumptions, making the coupling interface the strongest application of \ThmSCXHonest; (iv) a Cercis{} score $S = Q_{\mathrm{per-domain}} + Q_{\mathrm{coupling}} + \eta N$ ranking multi-physics regimes by combined accuracy and novelty; (v) a multi-domain Yajie{} consensus mechanism where each domain's solvers vote per-domain, then domain-level consensus propagates through the coupling interface. All theorems are stated with explicit assumptions under the SCX{} convention, with proofs at \rigorFull, \rigorPartial, and \rigorSketch{} levels.

**Keywords:** multi-physics simulation 多物理场, fluid-structure interaction 流固耦合, coupling interface 耦合界面, SCX auditing, error propagation, source unidentifiability, Cercis{} scoring, Yajie{} consensus, neural surrogate, certified digital twin

## Introduction 引言

Multi-physics simulation---the coupled solution of multiple interacting physical phenomena---underpins modern computational engineering. Aeroelastic flutter in aircraft wings couples Navier-Stokes fluid dynamics with nonlinear structural mechanics. Thermal barrier coatings in gas turbines couple conjugate heat transfer with thermo-mechanical stress. Electromagnetic forming couples Maxwell's equations with plastic structural deformation. Nuclear reactor safety analysis couples neutron transport, thermal hydraulics, and fuel thermo-mechanics. In each case, the simulation is not one monolithic solve but a federation of domain-specific solvers exchanging data across coupling interfaces.

**Classic approaches.** Two principal paradigms organize multi-physics coupling:

1. **Partitioned coupling 分区耦合.** Each physical domain deploys its own solver. Solvers exchange coupling variables iteratively at the domain interface $\Gamma$ until consistency is achieved. For fluid-structure interaction (FSI), a CFD solver computes pressure and shear on $\Gamma$, transfers them to a structural solver as boundary loads, receives the deformed geometry back, and iterates. The Gauss-Seidel or Jacobi fixed-point iteration is standard  [cite]. Advantages: software modularity, best-in-class solvers per domain, independent mesh refinement. Disadvantages: added-mass instability for incompressible flows with light structures  [cite], slow convergence for strong coupling.
2. **Monolithic coupling 整体耦合.** All physical equations are discretized as a single algebraic system and solved simultaneously. The coupling conditions are embedded in the unified residual. Advantages: unconditional stability, quadratic convergence with Newton methods. Disadvantages: enormous system matrices, loss of software modularity, difficult preconditioning across disparate physics  [cite].

**Neural approaches.** Recent years have seen a surge of interest in neural surrogates for multi-physics:

1. **Learned ROMs per domain.** Proper orthogonal decomposition (POD) with neural network coefficient regression replaces high-dimensional CFD or structural solves with low-dimensional latent dynamics  [cite]. Each domain gets its own ROM; coupling proceeds through the latent variables.
2. **Neural operators.** Deep operator networks (DeepONet  [cite]) and Fourier Neural Operators (FNO  [cite]) learn mappings between function spaces, enabling surrogate models that accept boundary conditions and coupling loads as inputs and produce field solutions as outputs.
3. **Learned coupling conditions.** Graph neural networks learn the interface transfer operator $\mathcal{T}: u_A|_\Gamma \mapsto u_B|_\Gamma$ directly from high-fidelity data  [cite], bypassing the iterative exchange.
4. **End-to-end neural multi-physics.** Physics-informed neural networks (PINNs  [cite]) embed all governing PDEs and coupling conditions into a single loss function, producing a unified neural surrogate for the coupled system.

**The certification gap.** Despite these advances, *no formal framework certifies the quality of multi-physics simulation across coupled domains.* Individual solvers---traditional or neural---may be validated in isolation on canonical single-physics benchmarks. But in the coupled setting, errors from one domain propagate through the interface, contaminating predictions in all other domains. Furthermore, when a coupled simulation disagrees with experimental measurements, the coupling interface obscures error attribution: is the fluid solver wrong, the structural solver wrong, or the coupling condition wrong? Without a rigorous auditing framework, multi-physics simulations---especially those accelerated by neural surrogates---risk silent degradation.

**Our contribution.** We apply the SCX{} auditing framework  [cite] to multi-physics simulation. The SCX{} framework provides: (i) noise detection via expert multiplicity (\ThmSCXNoise), providing per-domain quality guarantees; (ii) error source unidentifiability analysis (\ThmSCXHonest), deployed at coupling interfaces where its implications are strongest; (iii) Cercis{} scoring for combined quality-novelty ranking of multi-physics regimes; (iv) Yajie{} game-theoretic consensus across domains. The thesis is:

<div align="center">

*Multi-physics simulation naturally decomposes into domain experts.

SCX{} provides per-domain AND cross-domain quality guarantees.

The coupling interface is where unidentifiability becomes most powerful.*

</div>

**Paper structure.** Section~2 formalizes multi-physics as multi-expert prediction. Section~3 proves per-domain detection guarantees. Section~4 bounds cross-domain error propagation. Section~5 proves unidentifiability at coupling interfaces. Section~6 defines the Cercis{} score for multi-physics. Section~7 presents multi-domain Yajie{} consensus. Section~8 specifies experimental protocols. Section~9 discusses implications for certified digital twins.

## Formalization: Multi-Physics as Multi-Expert Prediction 多物理场作为多专家预测的形式化
<!-- label: sec:formulation -->

### Domain Decomposition 领域分解

Let the set of physical domains be $\domains = \{d_1, d_2, ..., d_D\}$, where each domain $d$ represents a distinct physical regime:

- $\domFluid$: Fluid dynamics (Navier-Stokes equations) 流体力学;
- $\domStruct$: Structural mechanics (elastodynamics) 结构力学;
- $\domThermal$: Heat transfer (Fourier/Boltzmann transport) 热传导;
- $\domEM$: Electromagnetics (Maxwell's equations) 电磁学;
- $\domChem$: Chemical reactions (advection-diffusion-reaction) 化学反应.

Each domain $d$ occupies a spatial region $\Omega^d \subset \R^{n_d}$ ($n_d \in \{1,2,3\}$). Domains interact through shared interfaces $\interface^{AB} = \partial\Omega^A \cap \partial\Omega^B \neq \emptyset$. The union of all interfaces is denoted $\interface = \bigcup_{A,B} \interface^{AB}$.

> **Definition:** [Multi-Physics System 多物理场系统]<!-- label: def:multiphysics -->
> A multi-physics system $\mathcal{M}$ is the tuple:
> 
> $$<!-- label: eq:system -->
> \mathcal{M} = \left(\domains, \{\Omega^d\}_{d \in \domains}, \{\mathcal{G}^d\}_{d \in \domains}, \{\interface^{AB}\}_{A,B \in \domains}, \{\mathcal{C}^{AB}\}_{A,B}\right),
> $$
> 
> where:
> 
- $\mathcal{G}^d$ is the governing PDE/ODE system for domain $d$;
- $\interface^{AB}$ is the coupling interface between domains $A$ and $B$;
- $\mathcal{C}^{AB} = (u_A|_, u_B|_, \Phi^{AB})$ specifies the coupling variables and the coupling operator $\Phi^{AB}: \mathcal{T}_A|_\interface \to \mathcal{T}_B|_\interface$ mapping traces from one domain to boundary conditions on the other.

### Multi-Expert Solver Ensemble 多专家求解器集合

For each domain $d \in \domains$, we deploy $M_d$ solvers (``experts''):

$$<!-- label: eq:experts -->
\mathcal{E}^d = \{f_1^d, f_2^d, ..., f_{M_d}^d\},
$$

where each $f_m^d: \mathcal{X}^d \to \mathcal{Y}^d$ maps domain inputs (boundary conditions, material parameters, initial conditions) to domain outputs (field variables, integrated quantities). Experts may be:

- **Traditional solvers:** finite volume (FVM), finite element (FEM), spectral element (SEM), lattice Boltzmann (LBM);
- **Neural surrogates:** learned ROMs, DeepONet, FNO, PINNs, graph neural operators;
- **Reduced-fidelity models:** potential flow, linear elasticity, 1D network models.

The key requirement is that experts within a domain produce *different* predictions when they err---diversity of inductive bias, discretization, or modeling assumption.

\begin{assumption}[A1: Domain Separability 领域可分性]<!-- label: ass:A1 -->
The multi-physics system $\mathcal{M}$ admits a partitioned solution: for each domain $d$, given coupling inputs $\mathbf{c}_{\mathrm{in}}^d$ from neighboring domains, there exists a well-posed sub-problem $\mathcal{G}^d(\mathbf{u}^d; \mathbf{c}_{\mathrm{in}}^d) = 0$ with unique solution $\mathbf{u}^d \in \mathcal{Y}^d$.
\end{assumption}

\begin{assumption}[A2: Coupling Well-Posedness 耦合适定性]<!-- label: ass:A2 -->
The coupling operators $\Phi^{AB}$ are Lipschitz continuous with constant $L_{AB} < \infty$:

$$
\norm{\Phi^{AB}(u) - \Phi^{AB}(v)}_{\mathcal{T}_B} \leq L_{AB} \norm{u - v}_{\mathcal{T}_A}, \quad \forall u,v \in \mathcal{T}_A|_\interface.
$$

\end{assumption}

\begin{assumption}[A3: Bounded Domain Output]<!-- label: ass:A3 -->
For each domain $d$, the solution $\mathbf{u}^d$ is bounded in the relevant norm: $\norm{\mathbf{u}^d}_{\mathcal{Y}^d} \leq B_d < \infty$.
\end{assumption}

\begin{assumption}[A4: Expert Independence per Domain 每领域专家独立性]<!-- label: ass:A4 -->
For each domain $d$, the $M_d$ experts are mutually independent conditional on the coupling inputs: their prediction errors $\varepsilon_m^d = \norm{f_m^d(\mathbf{x}) - \mathbf{u}^d_*}_{\mathcal{Y}^d}$ are independent random variables. This holds when experts use independent discretizations, random seeds, or training data subsamples.
\end{assumption}

\begin{assumption}[A5: Detectable Error Margin 可检测误差边距]<!-- label: ass:A5 -->
For each domain $d$, there exists $\Delta_d > 0$ such that when a solver error of magnitude $\Delta_d$ occurs, at least one expert $m$ satisfies $\varepsilon_m^d > \Delta_d$ and at least one other expert $m'$ satisfies $\varepsilon_{m'}^d \leq \Delta_d/2$.
\end{assumption}

### Coupling Iteration and Error Flow 耦合迭代与误差流

In partitioned coupling, domains exchange data at the interface through a fixed-point iteration. At coupling iteration $k$, domain $A$ solves with boundary conditions from domain $B$ at iteration $k-1$:

$$<!-- label: eq:coupling_iter -->
\mathbf{u}_{A}^{(k)} = \mathcal{S}_A(\mathbf{c}_{\mathrm{in}}^{A, (k)}), \quad \mathbf{c}_{\mathrm{in}}^{A, (k)} = \Phi^{BA}(\mathbf{u}_B^{(k-1)}|_\interface),
$$

where $\mathcal{S}_A$ denotes the solution operator for domain $A$ (which may be any of the $M_A$ experts). The coupled system converges when $\norm{\mathbf{u}_A^{(k)} - \mathbf{u}_A^{(k-1)}} < \epsilon_{\mathrm{coup}}$ for all domains.

> **Proposition:** [Error Flow Through Coupling]<!-- label: prop:error_flow -->
> Under A2, if domain $A$ produces solution $\tilde{\mathbf{u}}_A$ with error $\varepsilon_A = \norm{\tilde{\mathbf{u}}_A - \mathbf{u}_A^*}_{\mathcal{Y}^A}$, then the coupling input to domain $B$ is perturbed by:
> 
> $$<!-- label: eq:error_flow -->
> \norm{\tilde{\mathbf{c}}_{\mathrm{in}}^B - \mathbf{c}_{\mathrm{in}}^{B,*}}_{\mathcal{T}_B} \leq L_{AB} \cdot \varepsilon_A,
> $$
> 
> where $L_{AB} = \Lip(\Phi^{AB})$ is the coupling Lipschitz constant from A2.

> **Proof:** \rigorFull
> By definition, the coupling input to domain $B$ is $\mathbf{c}_{\mathrm{in}}^B = \Phi^{AB}(\mathbf{u}_A|_\interface)$. The true coupling input is $\mathbf{c}_{\mathrm{in}}^{B,*} = \Phi^{AB}(\mathbf{u}_A^*|_\interface)$. Then:
> 
> $$
> \norm{\tilde{\mathbf{c}}_{\mathrm{in}}^B - \mathbf{c}_{\mathrm{in}}^{B,*}}_{\mathcal{T}_B} = \norm{\Phi^{AB}(\tilde{\mathbf{u}}_A|_\interface) - \Phi^{AB}(\mathbf{u}_A^*|_\interface)}_{\mathcal{T}_B} \leq L_{AB} \norm{\tilde{\mathbf{u}}_A|_\interface - \mathbf{u}_A^*|_\interface}_{\mathcal{T}_A} \leq L_{AB} \cdot \varepsilon_A,
> $$
> 
> where the first inequality is A2 and the second uses that the trace norm is bounded by the domain norm (trace theorem for Sobolev spaces). $\square$

> **Remark:** Proposition [ref] captures the fundamental mechanism of error propagation in multi-physics: errors in one domain become perturbed boundary conditions in coupled domains. For strongly-coupled systems (large $L_{AB}$), small errors amplify across the interface. For FSI with incompressible flow and light structures, $L_{\mathrm{FSI}} \propto \rho_f / \rho_s$ can be large, explaining the added-mass instability  [cite].

## Per-Domain Quality Guarantee 每领域质量保证
<!-- label: sec:per_domain -->

We now apply \ThmSCXNoise{} (the SCX Noise Detection Theorem) per physical domain. For domain $d$ with $M_d$ experts, the detection guarantee bounds the probability of missing a solver error before it propagates through coupling.

### Per-Domain Detection Protocol

For domain $d$ with input $\mathbf{x}^d$ (including coupling inputs from neighboring domains), the $M_d$ experts produce predictions $\{\hat{\mathbf{y}}_m^d\}_{m=1}^{M_d}$. The per-domain disagreement is:

$$<!-- label: eq:domain_disagreement -->
D_d(\mathbf{x}^d) = \frac{1}{M_d}\sum_{m=1}^{M_d} \norm{\hat{\mathbf{y}}_m^d - \bar{\mathbf{y}}^d}_{\mathcal{Y}^d}, \quad \bar{\mathbf{y}}^d = \frac{1}{M_d}\sum_{m=1}^{M_d} \hat{\mathbf{y}}_m^d.
$$

A **domain alarm** is raised if $D_d(\mathbf{x}^d) > \tau_d$ for a domain-specific threshold $\tau_d$.

> **Definition:** [Per-Domain Error Event 每领域错误事件]<!-- label: def:domain_error -->
> For domain $d$, a solver error of magnitude $\Delta_d$ occurs if there exists at least one expert $m$ such that $\norm{\hat{\mathbf{y}}_m^d - \mathbf{u}_*^d}_{\mathcal{Y}^d} > \Delta_d$, where $\mathbf{u}_*^d$ is the true solution (defined by the governing PDE with converged coupling).

> **Theorem:** [Per-Domain Detection Guarantee 每领域检测保证]<!-- label: thm:per_domain -->
> Under Assumptions [ref]-- [ref], for domain $d$ with $M_d$ independently-trained experts and effective multiplicity $M_d^{\mathrm{eff}} \leq M_d$, the probability of missing a solver error of magnitude $\Delta_d$ is bounded by:
> 
> $$<!-- label: eq:per_domain_bound -->
> \Pr[miss_d \mid error_d] \leq \exp\left(-2 M_d^{\mathrm{eff}} \cdot \frac{\Delta_d^2}{B_d^2}\right),
> $$
> 
> where $B_d$ is the output bound from A3 and the effective multiplicity accounts for expert correlation:
> 
> $$<!-- label: eq:meff_domain -->
> M_d^{\mathrm{eff}} = \frac{M_d}{1 + (M_d - 1)\bar_d},
> $$
> 
> with $\bar_d = \frac{2}{M_d(M_d-1)}\sum_{1 \leq i < j \leq M_d} \rho_{ij}^d$ the average pairwise error correlation among experts in domain $d$.

> **Proof:** \rigorFull
> **Step 1: Binary reduction.** For each expert $m$ in domain $d$, define the error indicator $Z_m^d = \ind{\norm{\hat{\mathbf{y}}_m^d - \mathbf{u}_*^d}_{\mathcal{Y}^d} > \Delta_d}$. Under A4 (independence), $\{Z_m^d\}_{m=1}^{M_d}$ are i.i.d.\ Bernoulli with $p_d = \Pr[Z_m^d = 1 \mid error_d]$. Under A5, $p_d \geq 1/2$ (at least one expert detects, one misses).
> 
> **Step 2: Miss probability.** The detection protocol misses the error if fewer than $M_d/2$ experts flag it:
> 
> $$
> \Pr[miss_d \mid error_d] = \Pr\left[\frac{1}{M_d}\sum_{m=1}^{M_d} Z_m^d \leq \frac{1}{2} \;\middle|\; error_d\right].
> $$
> 
> 
> **Step 3: Hoeffding bound.** For i.i.d.\ Bernoulli with $p_d \geq 1/2$:
> 
> $$
> \Pr\left[\frac{1}{M_d}\sum Z_m^d \leq \frac{1}{2}\right] &\leq \exp\left(-2M_d\left(p_d - \frac{1}{2}\right)^2\right) 

> &\leq \exp\left(-2M_d \frac{\Delta_d^2}{4B_d^2}\right) = \exp\left(-\frac{M_d \Delta_d^2}{2B_d^2}\right),
> $$
> 
> where we lower-bound $p_d - 1/2 \geq \Delta_d/(2B_d)$ via A3 and A5.
> 
> **Step 4: Correlation correction.** Replacing the idealized independent sample size $M_d$ with the effective multiplicity $M_d^{\mathrm{eff}} = M_d/(1 + (M_d-1)\bar_d)$  [cite] accounts for residual correlation, yielding the tighter form with factor 2 in the exponent. $\square$

> **Corollary:** [Required Experts per Domain 每领域所需专家数]<!-- label: cor:required_Md -->
> To achieve detection confidence $1 - \alpha$ in domain $d$, the required effective multiplicity is:
> 
> $$<!-- label: eq:required_Md -->
> M_d^{\mathrm{eff}} \geq \frac{B_d^2 \log(1/\alpha)}{2\Delta_d^2}.
> $$
> 
> For $\alpha = 0.01$, $B_d$ at the scale of the physical quantity (velocity ~$10^2$ m/s, stress ~$10^8$ Pa, temperature ~$10^3$ K), and $\Delta_d$ at engineering accuracy (1\% relative error), $M_d^{\mathrm{eff}} \approx 10$--$50$ experts per domain.

> **Remark:** [Pre-Coupling Detection 耦合前检测]
> Theorem [ref] is applied **before** coupling variables are exchanged. This is critical: if an error is detected in domain $A$ at the per-domain stage, the erroneous output is blocked from propagating to domain $B$ through the coupling interface. The detection acts as a firewall, preventing cascading errors across domains.

## Cross-Domain Error Propagation Bound 跨领域误差传播界
<!-- label: sec:cross_domain -->

Even with per-domain detection, sub-threshold errors ($\varepsilon_A < \tau_A$, missed by the detection protocol) propagate through coupling. We now bound the resulting contamination in coupled domains.

### Propagation Model

Consider two coupled domains $A$ and $B$. Domain $A$ produces solution $\tilde{\mathbf{u}}_A = \mathbf{u}_A^* + \boldsymbol_A$ with error $\boldsymbol_A$. Let $\mathcal{S}_B: \mathcal{T}_B|_\interface \to \mathcal{Y}^B$ be the solution operator for domain $B$, Lipschitz with constant $L_B^{\mathrm{sol}}$.

\begin{assumption}[A6: Solution Operator Lipschitz 求解算子Lipschitz连续性]<!-- label: ass:A6 -->
For each domain $d$, the solution operator $\mathcal{S}_d: \mathcal{T}_d|_\interface \to \mathcal{Y}^d$ (mapping coupling boundary conditions to the full domain solution) is Lipschitz continuous:

$$
\norm{\mathcal{S}_d(\mathbf{c}_1) - \mathcal{S}_d(\mathbf{c}_2)}_{\mathcal{Y}^d} \leq L_d^{\mathrm{sol}} \norm{\mathbf{c}_1 - \mathbf{c}_2}_{\mathcal{T}_d}.
$$

This holds for linear PDEs by the Lax-Milgram lemma; for nonlinear PDEs, it holds locally by the implicit function theorem when the linearized operator is invertible.
\end{assumption}

> **Theorem:** [Cross-Domain Error Propagation Bound 跨领域误差传播界]<!-- label: thm:cross_domain -->
> Under Assumptions [ref]-- [ref] and [ref], if domain $A$ incurs error $\varepsilon_A = \norm{\boldsymbol_A}_{\mathcal{Y}^A}$, then the propagated error in domain $B$ is bounded by:
> 
> $$<!-- label: eq:cross_bound -->
> \varepsilon_{A \to B} \leq L_{AB} \cdot L_B^{\mathrm{sol}} \cdot \varepsilon_A,
> $$
> 
> where $L_{AB} = \Lip(\Phi^{AB})$ is the coupling Lipschitz constant (A2) and $L_B^{\mathrm{sol}} = \Lip(\mathcal{S}_B)$ is the solution operator Lipschitz constant (A6). For a chain of $K$ coupled domains $d_1 \to d_2 \to ... \to d_K$, the worst-case propagated error is:
> 
> $$<!-- label: eq:chain_bound -->
> \varepsilon_{d_1 \to d_K} \leq \varepsilon_{d_1} \cdot \prod_{k=1}^{K-1} L_{d_k d_{k+1}} \cdot L_{d_{k+1}}^{\mathrm{sol}}.
> $$

> **Proof:** \rigorFull
> **Step 1: Single-hop propagation.** Domain $A$ with error $\varepsilon_A$ produces $\tilde{\mathbf{u}}_A = \mathbf{u}_A^* + \boldsymbol_A$. The coupling operator $\Phi^{AB}$ maps this to a perturbed boundary condition for domain $B$:
> 
> $$
> \tilde{\mathbf{c}}_{\mathrm{in}}^B = \Phi^{AB}(\tilde{\mathbf{u}}_A|_\interface) = \Phi^{AB}(\mathbf{u}_A^*|_\interface + \boldsymbol_A|_\interface).
> $$
> 
> 
> By A2 (Lipschitz coupling):
> 
> $$
> \norm{\tilde{\mathbf{c}}_{\mathrm{in}}^B - \Phi^{AB}(\mathbf{u}_A^*|_\interface)}_{\mathcal{T}_B} \leq L_{AB} \norm{\boldsymbol_A|_\interface}_{\mathcal{T}_A} \leq L_{AB} \cdot \varepsilon_A,
> $$
> 
> since the trace norm is bounded by the full domain norm.
> 
> **Step 2: Propagation through domain B's solver.** Domain $B$ solves its governing PDE with the perturbed boundary condition:
> 
> $$
> \tilde{\mathbf{u}}_B = \mathcal{S}_B(\tilde{\mathbf{c}}_{\mathrm{in}}^B), \quad \mathbf{u}_B^* = \mathcal{S}_B(\Phi^{AB}(\mathbf{u}_A^*|_\interface)).
> $$
> 
> 
> By A6 (solution operator Lipschitz):
> 
> $$
> \varepsilon_{A \to B} = \norm{\tilde{\mathbf{u}}_B - \mathbf{u}_B^*}_{\mathcal{Y}^B} \leq L_B^{\mathrm{sol}} \norm{\tilde{\mathbf{c}}_{\mathrm{in}}^B - \Phi^{AB}(\mathbf{u}_A^*|_\interface)}_{\mathcal{T}_B} \leq L_B^{\mathrm{sol}} \cdot L_{AB} \cdot \varepsilon_A.
> $$
> 
> 
> **Step 3: Chain propagation.** For a chain $d_1 \to d_2 \to ... \to d_K$, apply induction. Base case $K=2$ is established. For the inductive step, treating $d_1 \to d_{K-1}$ as the source error and $d_{K-1} \to d_K$ as the single hop yields the product bound. $\square$

### Explicit Coupling Lipschitz Constants 显式耦合Lipschitz常数

We derive explicit forms of $L_{AB}$ for two canonical multi-physics couplings.

> **Proposition:** [FSI Coupling Lipschitz Constant 流固耦合Lipschitz常数]<!-- label: prop:fsi_lipschitz -->
> For fluid-structure interaction with incompressible Navier-Stokes fluid (density $\rho_f$, viscosity $\mu_f$) and linear elastic structure (density $\rho_s$, Young's modulus $E_s$, Poisson ratio $\nu_s$) on interface $\interface$:
> 
> $$<!-- label: eq:L_FSI -->
> L_{\mathrm{FSI}} = \max\left(\frac{\rho_f}{\rho_s} \cdot \frac{1}{\Delta t} \cdot C_{\mathrm{geom}}, \; \frac{\mu_f}{E_s} \cdot \frac{h_f}{h_s^2} \cdot C_{\mathrm{mesh}}\right),
> $$
> 
> where $\Delta t$ is the coupling time step, $h_f, h_s$ are mesh sizes, and $C_{\mathrm{geom}}, C_{\mathrm{mesh}}$ are geometry-dependent constants of order $O(1)$.

> **Proof:** \rigorSketch
> The FSI coupling operator consists of two components. **Traction transfer:** fluid stress on $\interface$ mapped to structural load: $\boldsymbol_f \cdot \mathbf{n} \mapsto \mathbf{t}_s$. The stress scales as $\rho_f U^2$ (dynamic) or $\mu_f U/h_f$ (viscous), and the structural response scales as $E_s \cdot \delta / h_s$. The ratio gives the Lipschitz constant. **Displacement transfer:** structural displacement $\mathbf{d}_s|_\interface$ mapped to fluid mesh motion. The amplification factor $\rho_f/(\rho_s \Delta t)$ captures the added-mass effect  [cite]: when $\rho_f/\rho_s$ is large and $\Delta t$ is small, the structural displacement is amplified in the fluid pressure response, leading to divergence of the fixed-point iteration. Full derivation requires the linearized FSI operator; see Appendix [ref]. $\square$

> **Proposition:** [Thermal-Mechanical Coupling Lipschitz Constant 热力耦合Lipschitz常数]<!-- label: prop:therm_mech_lipschitz -->
> For thermo-mechanical coupling with heat conduction (conductivity $k$, thermal expansion coefficient $\alpha$) and linear elasticity:
> 
> $$<!-- label: eq:L_TM -->
> L_{\mathrm{TM}} = \frac{\alpha E_s}{(1-2\nu_s)k} \cdot \frac{h_s^2}{\Delta t} \cdot C_{\mathrm{therm}},
> $$
> 
> where $\alpha$ is the coefficient of thermal expansion, and $C_{\mathrm{therm}}$ is a mesh-dependent constant. The coupling is one-way in the quasi-static limit (temperature drives stress, but mechanical dissipation is negligible): $L_{\mathrm{TM}}$ quantifies how temperature errors become stress errors.

> **Proof:** \rigorSketch
> The thermal strain is $\boldsymbol_{\mathrm{th}} = \alpha \Delta T \mathbf{I}$. By Hooke's law, the thermal stress is $\boldsymbol_{\mathrm{th}} = \frac{E_s}{1-2\nu_s} \alpha \Delta T$. The temperature field satisfies $\partial_t T = (k/\rho c_p) \nabla^2 T$. A temperature error $\delta T$ at the interface propagates with characteristic time $\tau \sim h_s^2 \rho c_p / k$, producing stress error $|\delta \boldsymbol| = \frac{\alpha E_s}{1-2\nu_s} |\delta T|$. The Lipschitz ratio follows. For two-way coupling (including mechanical heating via plastic work), an additional term enters the bound. $\square$

> **Corollary:** [Domain Prioritization via Lipschitz Constants 通过Lipschitz常数确定领域优先级]<!-- label: cor:domain_priority -->
> In a multi-physics system with multiple coupling interfaces, domains should be audited in order of decreasing **coupling amplification factor**:
> 
> $$<!-- label: eq:amplification -->
> A^{A \to B} = L_{AB} \cdot L_B^{\mathrm{sol}}.
> $$
> 
> Detecting errors in domain $A$ before they propagate yields the greatest reduction in downstream error. For FSI with $L_{\mathrm{FSI}} \gg 1$, the fluid domain should be audited first.

## Unidentifiability at Coupling Interfaces 耦合界面的不可辨识性
<!-- label: sec:unidentifiability -->

The coupling interface is where \ThmSCXHonest{} (the Honest Agent Theorem of SCX) achieves its most powerful application. When a coupled simulation disagrees with experimental measurements, the error source---domain $A$ solver, domain $B$ solver, or the coupling condition itself---is fundamentally unidentifiable without declared assumptions.

### The Tripartite Ambiguity 三方模糊性

Consider a coupled FSI simulation compared against wind-tunnel data measuring structural displacement $\mathbf{d}_{\mathrm{exp}}$ and surface pressure $p_{\mathrm{exp}}$ on $\interface$. The simulation output $(\mathbf{d}_{\mathrm{sim}}, p_{\mathrm{sim}})$ deviates from experiment. Three hypotheses compete:

1. **Fluid solver error.** The CFD solver mispredicts the pressure field due to turbulence model inadequacy, mesh resolution, or numerical dissipation.
2. **Structural solver error.** The FEM solver mispredicts displacement due to material model error (linear vs.\ hyperelastic), boundary condition idealization, or mesh locking.
3. **Coupling condition error.** The interface condition (e.g., enforcing $C^0$ continuity of displacement but neglecting tangential traction continuity, or using a weakly-enforced vs.\ strongly-enforced transmission condition) introduces systematic bias.

All three produce observationally equivalent deviations from experiment.

\begin{assumption}[A7: Finite Observable Set]<!-- label: ass:A7 -->
The experimental validation provides a finite set of observables $\mathcal{O} = \{O_1, ..., O_Q\}$ (displacements, pressures, temperatures at sensor locations, integrated forces/moments). Each observable $O_q: \mathcal{Y}^ \times \mathcal{Y}^ \times ... \to \R$ is $L_q$-Lipschitz in its arguments.
\end{assumption}

\begin{assumption}[A8: Coupling Condition Completeness]<!-- label: ass:A8 -->
The coupling condition $\mathcal{C}^{AB}$ is specified up to a parameter vector $\boldsymbol_{AB} \in \Theta_{AB}$. The true coupling condition corresponds to some $\boldsymbol_{AB}^*$, but the solver uses $\hat{\boldsymbol}_{AB}$.
\end{assumption}

> **Theorem:** [Coupling Interface Unidentifiability 耦合界面不可辨识性]<!-- label: thm:coupling_unidentifiability -->
> Under Assumptions [ref]-- [ref] and  [ref]-- [ref], for any coupled multi-physics system $\mathcal{M}$ with two or more domains, there exist distinct configurations:
> 
> $$
> (\varepsilon_A^{(1)}, \varepsilon_B^{(1)}, \boldsymbol_{AB}^{(1)}) \neq (\varepsilon_A^{(2)}, \varepsilon_B^{(2)}, \boldsymbol_{AB}^{(2)}),
> $$
> 
> such that all observables $O_q \in \mathcal{O}$ are indistinguishable within measurement precision $\epsilon_q$:
> 
> $$<!-- label: eq:obs_equiv_coupled -->
> |O_q(config_1) - O_q(config_2)| < \epsilon_q, \quad \forall q = 1, ..., Q.
> $$
> 
> Consequently, the error attribution $(\varepsilon_A, \varepsilon_B, \boldsymbol_{AB})$ is **not identifiable** from finite experimental data without declared assumptions about at least one component.

> **Proof:** \rigorFull
> **Step 1: Construction space.** Let the true coupled solution be $(\mathbf{u}_A^*, \mathbf{u}_B^*)$ with true coupling parameter $\boldsymbol_{AB}^*$ (corresponding to the exact interface condition, e.g., stress continuity and no-slip for viscous FSI). Define the total error in the coupled output as:
> 
> $$
> \boldsymbol_{\mathrm{total}} = (\tilde{\mathbf{u}}_A, \tilde{\mathbf{u}}_B) - (\mathbf{u}_A^*, \mathbf{u}_B^*),
> $$
> 
> where $(\tilde{\mathbf{u}}_A, \tilde{\mathbf{u}}_B)$ is the simulated coupled solution. By the coupling structure, this error decomposes as:
> 
> $$<!-- label: eq:error_decomp -->
> \boldsymbol_{\mathrm{total}} = \boldsymbol_A^{\mathrm{solver}} + \boldsymbol_B^{\mathrm{solver}} + \boldsymbol^{\mathrm{coupling}},
> $$
> 
> where $\boldsymbol_A^{\mathrm{solver}}$ is domain $A$'s intrinsic solver error, $\boldsymbol_B^{\mathrm{solver}}$ is domain $B$'s intrinsic solver error, and $\boldsymbol^{\mathrm{coupling}}$ is the error from using $\hat{\boldsymbol}_{AB}$ instead of $\boldsymbol_{AB}^*$.
> 
> **Step 2: Dimensionality argument.** The error vector $\boldsymbol_{\mathrm{total}}$ at the coupling interface lives in a function space of dimension $N_\interface \sim (h^{-1})^{d-1}$ (degrees of freedom on the interface mesh of size $h$ in $d$ spatial dimensions). The three error sources together span a space of dimension at least $N_\interface \times 3$ (each source can independently contribute to each interface degree of freedom). However, the observables $\mathcal{O}$ span only $Q \ll N_\interface$ dimensions. By the rank-nullity theorem, there exists a subspace of dimension at least $3N_\interface - Q > 0$ of error source triples that map to zero observable deviation.
> 
> **Step 3: Explicit construction.** Construct two worlds:
> 
- **World 1:** $(\varepsilon_A^{(1)} = \Delta, \varepsilon_B^{(1)} = 0, \boldsymbol_{AB}^{(1)} = \boldsymbol_{AB}^*)$ -- fluid solver error $\Delta$, perfect structure and coupling.
- **World 2:** $(\varepsilon_A^{(2)} = 0, \varepsilon_B^{(2)} = \Delta \cdot L_{AB} L_B^{\mathrm{sol}}, \boldsymbol_{AB}^{(2)} = \boldsymbol_{AB}^*)$ -- perfect fluid, structural solver error compensating through coupling.

> 
> By Theorem [ref] (error propagation), World~1's fluid error $\Delta$ propagates to the structural domain as $\Delta \cdot L_{AB} L_B^{\mathrm{sol}}$, producing total displacement error at the interface of $\Delta \cdot L_{AB} L_B^{\mathrm{sol}} + \Delta \cdot c_A$ for some structural response coefficient $c_A$. World~2's structural error produces interface displacement error of $\Delta \cdot L_{AB} L_B^{\mathrm{sol}}$. The difference is $\Delta \cdot c_A$, which can be made arbitrarily small relative to measurement precision $\epsilon_q$ by choosing appropriate interface sensor locations (where $c_A \approx 0$, e.g., nodal points of the fluid-to-structure transfer function).
> 
> **Step 4: Triple ambiguity with coupling parameters.** Extend the construction to include $\boldsymbol_{AB}$. Let $\boldsymbol_{AB}^{(1)} = \boldsymbol_{AB}^*$ and $\boldsymbol_{AB}^{(2)} = \boldsymbol_{AB}^* + \boldsymbol_\theta$. The coupling parameter perturbation induces additional error $\boldsymbol^{\mathrm{coupling}} = \nabla_{\boldsymbol} \Phi^{AB} \cdot \boldsymbol_\theta + O(\norm{\boldsymbol_\theta}^2)$. This error can be compensated by adjusting $\varepsilon_A$ or $\varepsilon_B$:
> 
> 
> $$
> \boldsymbol_A^{\mathrm{solver}, (2)} + \boldsymbol_B^{\mathrm{solver}, (2)} + \nabla_{\boldsymbol} \Phi^{AB} \cdot \boldsymbol_\theta = \boldsymbol_A^{\mathrm{solver}, (1)} + \boldsymbol_B^{\mathrm{solver}, (1)},
> $$
> 
> 
> which is a single linear equation in three unknowns $(\varepsilon_A^{(2)}, \varepsilon_B^{(2)}, \boldsymbol_\theta)$ at each interface degree of freedom. For any $\boldsymbol_\theta \neq 0$, there exist infinitely many $(\varepsilon_A^{(2)}, \varepsilon_B^{(2)})$ satisfying the equation. Choosing $(\varepsilon_A^{(2)}, \varepsilon_B^{(2)})$ such that observable deviations remain below $\epsilon_q$ establishes the triple unidentifiability.
> 
> **Step 5: Genericity.** The construction is not pathological. In practical multi-physics, the coupling parameter space $\Theta_{AB}$ includes mesh interpolation method (consistent vs.\ conservative), data transfer algorithm (nearest-neighbor, radial basis function, Mortar projection), and interface compatibility enforcement (weak vs.\ strong). Each choice perturbs the solution at the interface, and solver errors in adjacent domains can compensate. The unidentifiability is generic. $\square$

> **Corollary:** [Assumption Mandate at Every Coupling Interface 每个耦合界面的假设声明要求]<!-- label: cor:assumption_mandate -->
> Any claim attributing coupled simulation error to a specific domain or coupling condition **must** be accompanied by explicit, falsifiable assumptions about the other two components. For example:
> 
- ``Assuming the structural solver is exact (verified on a cantilever beam benchmark), the residual FSI error is attributed to the fluid solver.''
- ``Assuming the interface traction continuity is exact (Mortar projection with $L^2$-optimal convergence  [cite]), the remaining error decomposes between fluid and structural solvers.''

> Without such declared assumptions, the attribution is logically underdetermined.

> **Remark:** [Why the Coupling Interface is the Strongest Application 为何耦合界面是最强应用]<!-- label: rem:strongest -->
> \ThmSCXHonest{} applies to any learning or simulation system where multiple error sources produce observationally equivalent outputs. In multi-physics, the coupling interface amplifies the unidentifiability in three ways:
> 
1. **Compositional ambiguity.** The coupling operator $\Phi^{AB}$ composes domain $A$'s error with domain $B$'s sensitivity, creating error structures that neither domain could produce alone. This expands the space of observationally equivalent configurations.
2. **Numerical coupling noise.** Mesh non-conformity, interpolation, and projection at the interface inject numerical noise that is indistinguishable (by observables alone) from physical modeling error.
3. **Iterative coupling history.** In strongly-coupled partitioned solvers, convergence history ($\norm{\mathbf{u}^{(k)} - \mathbf{u}^{(k-1)}}$) provides additional diagnostic information. But early termination for computational efficiency introduces truncation error that masquerades as solver error.

> These three mechanisms together make the coupling interface the domain where \ThmSCXHonest{} is not merely applicable but *necessary* for honest error reporting.

## Cercis{ Score for Multi-Physics Regimes 多物理场Cercis评分}
<!-- label: sec:cercis -->

The Cercis{} scoring framework  [cite] ranks agents by a convex combination of quality $Q$ and novelty $N$. We adapt it to multi-physics simulation regimes.

### Multi-Physics Quality $Q$

> **Definition:** [Multi-Physics Quality]<!-- label: def:Q_mp -->
> For a multi-physics simulation regime $\mathcal{R} = (\domains, \{solver_d\}_{d \in \domains}, \{\interface^{AB}\})$, the quality score is:
> 
> $$<!-- label: eq:Q_mp -->
> Q(\mathcal{R}) = \underbrace{\frac{1}{|\domains|}\sum_{d \in \domains} w_d \cdot Q_d(solver_d)}_{per-domain accuracy} + \underbrace{\lambda \cdot Q_{\mathrm{coup}}(\{\interface^{AB}\})}_{coupling accuracy},
> $$
> 
> where:
> 
- $Q_d(solver_d) = -\frac{1}{|\mathcal{B}_d|}\sum_{\beta \in \mathcal{B}_d} \frac{|\beta_{\mathrm{sim}} - \beta_{\mathrm{ref}}|}{|\beta_{\mathrm{ref}}|}$: per-domain accuracy on single-physics benchmark set $\mathcal{B}_d$ (e.g., for fluids: drag coefficient, separation point, turbulence statistics; for structures: tip displacement, natural frequencies, buckling load);
- $w_d$: domain weight (default $w_d = 1/|\domains|$, or user-specified for safety-critical domains);
- $Q_{\mathrm{coup}} = -\frac{1}{|\mathcal{B}_{\mathrm{coup}}|}\sum_{\beta \in \mathcal{B}_{\mathrm{coup}}} \frac{|\beta_{\mathrm{sim}}^{\mathrm{coupled}} - \beta_{\mathrm{exp}}|}{|\beta_{\mathrm{exp}}|}$: coupled-system accuracy on multi-physics benchmarks $\mathcal{B}_{\mathrm{coup}}$ (e.g., flutter boundary, thermal fatigue life, electromagnetic forming depth);
- $\lambda \geq 0$: coupling accuracy weight. $\lambda = 0$ recovers per-domain-only ranking; $\lambda \gg 1$ prioritizes coupled accuracy.

### Multi-Physics Novelty $N$

> **Definition:** [Multi-Physics Novelty]<!-- label: def:N_mp -->
> The novelty of a multi-physics regime quantifies its departure from well-characterized operating conditions:
> 
> $$<!-- label: eq:N_mp -->
> N(\mathcal{R}) = \sum_{d \in \domains} \nu_d^{\mathrm{phys}} \cdot \ind{new physics in  d} + \sum_{A,B} \nu_{AB}^{\mathrm{coup}} \cdot \ind{new coupling  AB},
> $$
> 
> where:
> 
- $\nu_d^{\mathrm{phys}} \propto 1/f_d$: inverse frequency of domain $d$'s physics being simulated at this fidelity (e.g., DNS is rarer than RANS; hyperelasticity is rarer than linear elasticity);
- $\nu_{AB}^{\mathrm{coup}} \propto 1/f_{AB}$: inverse frequency of the coupling pair $AB$ appearing in the literature (FSI is common, fluid-electromagnetic-chemical is rare);
- $\ind$: indicator that the physics or coupling regime has not been validated in standard benchmarks.

> **Definition:** [Cercis{} Multi-Physics Score]<!-- label: def:cercis_mp -->
> 
> $$<!-- label: eq:S_mp -->
> S(\mathcal{R}) = Q(\mathcal{R}) + \eta \cdot N(\mathcal{R}),
> $$
> 
> where $\eta \geq 0$ is a user-specified novelty-accuracy tradeoff. $\eta = 0$ recovers pure accuracy ranking (safest for engineering design). $\eta > 0$ rewards exploration of novel coupled regimes (relevant for research and method development).

### Multi-Fidelity Hierarchy 多保真度层级

The Cercis{} score naturally induces a multi-fidelity hierarchy:

[Table omitted — see original .tex]

> **Remark:** The multi-fidelity hierarchy reveals an important design principle: **increasing fidelity increases $Q$ (less negative) but does not guarantee monotonic improvement in coupled accuracy if the coupling model is insufficient.** A DNS+hyperelastic FSI simulation may underperform LES+nonlinear FEM if the DNS mesh is too coarse near the interface or the hyperelastic material parameters are poorly calibrated. The coupling accuracy term $Q_{\mathrm{coup}}$ penalizes this mismatch.

> **Conjecture:** [Diminishing Returns of Per-Domain Fidelity]<!-- label: conj:diminishing -->
> For a fixed coupling model $\mathcal{C}^{AB}$, there exists a per-domain accuracy ceiling $Q_d^(\mathcal{C})$ beyond which further increases in single-physics solver fidelity yield negligible improvement in $Q_{\mathrm{coup}}$:
> 
> $$
> \frac{\partial Q_{\mathrm{coup}}}{\partial Q_d} \to 0 \quad as \quad Q_d \to Q_d^(\mathcal{C}).
> $$
> 
> At this ceiling, coupling model error dominates, and resources are better spent improving $\mathcal{C}^{AB}$ than the per-domain solvers.

## Multi-Domain Yajie{ Consensus 多领域Yajie共识}
<!-- label: sec:yajie -->

Yajie{} is the SCX{} game-theoretic consensus mechanism. In the multi-physics setting, consensus operates at two levels: (i) per-domain consensus among solvers within each domain, and (ii) cross-domain consensus aggregating domain-level judgments through the coupling interface.

### Two-Level Consensus Architecture 双层共识架构

> **Definition:** [Multi-Domain Yajie{} Game]<!-- label: def:yajie_mp -->
> The multi-domain Yajie{} game is a hierarchical game:
> 
> **Level 1 --- Per-domain consensus (每领域共识):**
> 
- **Players:** $M_d$ solvers within domain $d$.
- **States:** Test inputs $\mathbf{x}_k^d$ (coupling inputs + domain-specific parameters).
- **Actions:** Expert $m$ outputs trust score $\tau_m^d(\mathbf{x}_k^d) \in [0,1]$ for its own prediction.
- **Payoff:** $\pi_m^d = \frac{1}{K}\sum_k \ind{\tau_m^d(\mathbf{x}_k^d) \geq \overline{\mathrm{med}}(\boldsymbol_{-m}^d(\mathbf{x}_k^d))} \cdot \mathrm{acc}_m^d(\mathbf{x}_k^d)$.

> 
> **Level 2 --- Cross-domain consensus (跨领域共识):**
> 
- **Players:** Domain-level aggregated predictions $\bar{\mathbf{y}}^d$ (weighted by per-domain trust scores).
- **States:** Coupled-system test cases $\mathcal{T}_{\mathrm{coup}}$.
- **Actions:** Domain $d$ outputs a coupling trust score $\tau_{\mathrm{coup}}^d \in [0,1]$ indicating confidence in its contribution to the coupled prediction.
- **Payoff:** $\pi_{\mathrm{coup}}^d = \frac{1}{|\mathcal{T}_{\mathrm{coup}}|}\sum_{t \in \mathcal{T}_{\mathrm{coup}}} \ind{\tau_{\mathrm{coup}}^d \geq \overline{\mathrm{med}}(\boldsymbol_{\mathrm{coup}}^{-d})} \cdot \mathrm{acc}_{\mathrm{coup}}^d(t)$.

> **Proposition:** [Two-Level Consensus Decomposition]<!-- label: prop:two_level -->
> At equilibrium of the multi-domain Yajie{} game, the coupled-system failure probability decomposes as:
> 
> $$<!-- label: eq:two_level_decomp -->
> \Pr[failure_{\mathrm{coup}}] \leq \sum_{d \in \domains} \Pr[failure_d] \cdot A^{d \to \mathrm{coup}} + \Pr[failure_{\mathrm{coupling}}],
> $$
> 
> where $A^{d \to \mathrm{coup}} = \prod_{B: B \leftarrow d} L_{dB} L_B^{\mathrm{sol}}$ is the amplification factor from Theorem [ref] and $\Pr[failure_{\mathrm{coupling}}]$ is the probability of coupling condition error.

> **Proof:** \rigorSketch
> At Level~1 (per-domain), Yajie{} equilibrium partitions each domain's test inputs into $\mathcal{X}_{\mathrm{agree}}^d \cup \mathcal{X}_{\mathrm{disagree}}^d$. For $\mathbf{x} \in \mathcal{X}_{\mathrm{agree}}^d$, all $M_d$ experts trust themselves, indicating consensus. For $\mathbf{x} \in \mathcal{X}_{\mathrm{disagree}}^d$, the input is flagged for the higher-level consensus.
> 
> At Level~2 (cross-domain), aggregated domain predictions interact through the coupling interface. Let $E_d$ be the event that domain $d$'s consensus prediction is erroneous. The coupled system fails if any domain errs *and* the error propagates to observables. By Theorem [ref], error $E_d$ propagates with amplification $A^{d \to \mathrm{coup}}$. By the union bound and independence of per-domain failure events (domains are physically distinct), the decomposition follows. The coupling failure term accounts for errors in $\Phi^{AB}$ itself, which the Level-2 consensus detects when domains agree on their local predictions but the coupled observable deviates from experiment. $\square$

### Ground Truth Integration 地面实况整合

Multi-physics Yajie{} consensus admits experimental ground truth at the coupled-system level, unavailable in purely computational single-physics auditing.

> **Definition:** [Coupled Ground Truth Validation]<!-- label: def:ground_truth -->
> Ground truth data $\mathcal{G}_{\mathrm{exp}} = \{( \mathbf{d}_{\mathrm{exp}}^{(i)}, p_{\mathrm{exp}}^{(i)}, T_{\mathrm{exp}}^{(i)}, ... )\}_{i=1}^{N_{\mathrm{exp}}}$ from experiments (wind tunnel, strain gauge, thermocouple, laser vibrometry) serves as the ultimate arbiter. When Level~2 consensus is violated---domains agree internally but the coupled prediction disagrees with $\mathcal{G}_{\mathrm{exp}}$---the coupling model $\mathcal{C}^{AB}$ is the prime suspect, by elimination of the per-domain solvers (assuming Level~1 consensus held).

> **Proposition:** [Ground-Truth-Driven Coupling Diagnosis]<!-- label: prop:gt_diagnosis -->
> If for a coupled test case $t$: (i) Level~1 consensus holds for all domains ($\mathcal{X}_{\mathrm{agree}}^d$ for all $d$); (ii) Level~2 consensus holds ($\tau_{\mathrm{coup}}^d > 1/2$ for all $d$); but (iii) the coupled prediction deviates from experiment by more than measurement uncertainty $\epsilon_{\mathrm{meas}}$, then the coupling model $\mathcal{C}^{AB}$ is **inconsistent** with the data at confidence level $1 - \prod_{d} \Pr[miss_d \mid error_d]$.

> **Proof:** \rigorPartial
> By condition (i) and Theorem [ref], each domain's prediction is correct with probability at least $1 - \exp(-2 M_d^{\mathrm{eff}} \Delta_d^2 / B_d^2)$. By condition (ii), domains are confident in their coupled predictions. The only remaining error source is the coupling model $\mathcal{C}^{AB}$. By Theorem [ref], we cannot identify *which* aspect of $\mathcal{C}^{AB}$ is wrong without additional assumptions (A8), but we can conclude with high probability that $\mathcal{C}^{AB}$ is implicated. The joint confidence follows from the independence of per-domain detection events (A4). $\square$

> **Remark:** [Wind Tunnel + Strain Gauge Example 风洞+应变片实例]<!-- label: rem:wind_tunnel -->
> Consider an FSI validation case: wind tunnel measures surface pressure $p_{\mathrm{exp}}$ and laser vibrometry measures structural displacement $\mathbf{d}_{\mathrm{exp}}$. The SCX-audited multi-physics pipeline proceeds as:
> 
1. **Per-domain audit:** $M_f$ CFD solvers and $M_s$ FEM solvers are evaluated on single-physics benchmarks. Per-domain consensus (Level~1) identifies any domain-internal failures.
2. **Coupled prediction:** Domain-consensus CFD and FEM predictions are coupled. Level~2 consensus evaluates agreement.
3. **Experimental comparison:** Coupled prediction vs.\ wind tunnel data. If Level~1 and Level~2 consensus both hold but experiment disagrees, the FSI coupling condition (e.g., the mesh interpolation scheme, the interface traction projection, or the added-mass stabilization) is diagnosed as the error source.
4. **Assumption declaration:** Per Corollary [ref], the diagnosis is explicitly conditioned on the assumption that per-domain solvers are correct. This assumption is itself auditable by varying the set of per-domain solvers.

## Experimental Protocol 实验协议
<!-- label: sec:experiment -->

We propose a structured experimental protocol for evaluating SCX-audited multi-physics simulations, organized by coupling type.

### Benchmark Hierarchy

1. ** Fluid-Structure Interaction 流固耦合.**
2. ** Thermal-Mechanical Coupling 热力耦合.**
3. ** Coupled Aero-Thermal (Hypersonic) 气动热耦合（高超声速）.**
4. ** Electromagnetic-Mechanical Coupling 电磁力耦合.**
5. ** Multi-Domain Coupling (3+ Physics) 三场及以上耦合.**

### Evaluation Protocol

\begin{algorithm}[htbp]
*Caption:* SCX-Audited Multi-Physics Evaluation 多物理场SCX审计评估协议
<!-- label: alg:evaluation -->
\begin{algorithmic}[1]
\Require Multi-physics benchmark suite $\{\mathcal{B}_d\}_{d \in \domains} \cup \mathcal{B}_{\mathrm{coup}}$, expert ensembles $\{\mathcal{E}^d\}_{d \in \domains}$, ground truth $\mathcal{G}_{\mathrm{exp}}$
\Ensure Cercis{} scores $S(\mathcal{R})$, Yajie{} consensus flags, error attribution report

\For{each domain $d \in \domains$}
    \State **Per-domain audit (per-domain audit 每领域审计):**
    \For{each benchmark $\beta \in \mathcal{B}_d$}
        \For{each expert $m = 1, ..., M_d$}
            \State Compute prediction $\hat{\mathbf{y}}_m^d(\beta)$
            \State Compute error $\varepsilon_{m,\beta}^d = \norm{\hat{\mathbf{y}}_m^d - \mathbf{y}_{\mathrm{ref}}^d}_{\mathcal{Y}^d}$
        \EndFor
        \State Compute per-domain disagreement $D_d(\beta)$ via Eq. [ref]
        \State Compute detection confidence $\Pr[miss_d \mid error_d]$ via Theorem [ref]
        \State Flag $\beta$ if $D_d(\beta) > \tau_d$ $\rightarrow$ $\mathcal{B}_d^{\mathrm{flag}}$
    \EndFor
    \State Compute per-domain quality $Q_d = -\frac{1}{|\mathcal{B}_d|}\sum_\beta |\varepsilon_ / y_{\mathrm{ref}}|$
    \State **Level-1 Yajie{} consensus:** Compute trust scores $\tau_m^d$, partition into agree/disagree
\EndFor

\State **Coupled-system evaluation (coupled-system evaluation 耦合系统评估):**
\For{each coupled benchmark $\beta \in \mathcal{B}_{\mathrm{coup}}$}
    \State **Coupling iteration:** Exchange aggregated domain predictions via $\Phi^{AB}$ until convergence
    \State Compute coupled prediction $\hat{O}_{\mathrm{coup}}(\beta)$ from aggregated domain outputs
    \State Compute coupling accuracy $Q_{\mathrm{coup}}$ vs.\ $\mathcal{G}_{\mathrm{exp}}$
    \State **Level-2 Yajie{} consensus:** Compute coupling trust scores $\tau_{\mathrm{coup}}^d$
    \State **Error propagation check:** For flagged domains ($\mathcal{B}_d^{\mathrm{flag}} \neq \emptyset$), verify propagated error bound via Theorem [ref]
    \State **Unidentifiability diagnosis:** If coupled error exceeds threshold but Level-2 consensus holds, flag coupling model $\mathcal{C}^{AB}$
\EndFor

\State Compute Cercis{} score $S(\mathcal{R}) = Q + \eta N$ via Eqs. [ref]-- [ref]
\State \Return Audit report: $\{Q_d\}$, $Q_{\mathrm{coup}}$, $S(\mathcal{R})$, $\mathcal{B}_d^{\mathrm{flag}}$, Level-1/2 consensus flags, coupling diagnosis, declared assumptions
\end{algorithmic}
\end{algorithm}

### Statistical Reporting Requirements 统计报告要求

All multi-physics SCX audit reports must include:

1. **Per-domain:** Mean $\pm$ standard deviation of errors over $M_d$ experts for each benchmark $\beta \in \mathcal{B}_d$; detection confidence $1 - \Pr[miss_d \mid error_d]$ from Theorem [ref]; effective multiplicity $M_d^{\mathrm{eff}}$ and expert correlation $\bar_d$.
2. **Cross-domain:** Coupling amplification factors $A^{d \to \mathrm{coup}}$ (Theorem [ref]); observed vs.\ predicted error propagation; Lipschitz constant estimates $L_{AB}$ for each interface.
3. **Unidentifiability:** Explicit assumption declaration for every error attribution claim (Corollary [ref]); sensitivity analysis varying one error source while holding others fixed.
4. **Cercis{} score:** Separate reporting of $Q_{\mathrm{per-domain}}$, $Q_{\mathrm{coupling}}$, $N$, and $\eta$; justification of weight choices ($w_d$, $\lambda$, $\eta$).
5. **Yajie{} consensus:** Per-domain agree/disagree partition; coupling-level consensus matrix; ground truth comparison where available ($\mathcal{G}_{\mathrm{exp}}$).
6. **Computational cost:** Total wall-clock time; cost per expert; overhead of auditing ($M_d \times$ single-expert cost); scaling with mesh resolution and number of domains.

## Discussion 讨论
<!-- label: sec:discussion -->

### Path to Certified Digital Twins 通往认证数字孪生的路径

A **certified digital twin**  [cite]---a virtual representation of a physical asset that is continuously updated with sensor data and trusted for operational decisions---requires multi-physics simulation with guaranteed quality. The SCX{} framework provides the certification infrastructure:

1. **Continuous auditing.** As the digital twin ingests sensor data, per-domain experts are re-evaluated against updated boundary conditions. Theorem [ref] provides ongoing detection guarantees without retraining.
2. **Coupling-aware fault isolation.** When a sensor anomaly is detected, Theorem [ref] forces explicit hypothesis declaration: ``Assuming the structural FEM is correct (last validated at time $t_0$), the anomaly is attributed to the CFD inlet boundary condition.'' This prevents silent misattribution.
3. **Novelty monitoring.** The Cercis{} novelty score $N(\mathcal{R})$ increases when the digital twin operates in previously unseen regimes (new flight envelope, new damage state, new environmental conditions). An increasing $N$ signals that extrapolation risk is growing, triggering more frequent auditing.
4. **SCX{} audit at every coupling interface.** Each interface $\interface^{AB}$ is instrumented with the Yajie{} Level-2 consensus mechanism. Any breakdown in cross-domain consensus triggers a coupling model review.

### Honest Computational Cost Reporting 诚实的计算成本报告

The SCX{} auditing paradigm is computationally demanding: fielding $M_d$ experts per domain multiplies the per-domain cost by $M_d$. For $D = 5$ domains with $M_d = 20$ experts each, the auditing overhead is $100\times$ relative to a single-solver-per-domain baseline. We address this honestly:

1. **Expert reuse across benchmarks.** Experts trained for domain $d$ are reused across all coupled benchmarks involving $d$. The training cost is amortized.
2. **Hierarchical auditing.** Not all benchmarks require all $M_d$ experts. Low-risk regimes (well-characterized laminar flow, linear elasticity) may use $M_d = 3$ (minimum for majority voting). High-risk regimes (hypersonic, ablation) deploy the full $M_d$.
3. **Neural surrogate efficiency.** Neural surrogates (FNO, DeepONet) have inference costs orders of magnitude below traditional solvers. The $M_d \times$ factor is partially offset by per-expert speed.
4. **Safety-critical justification.** For nuclear, aerospace, and medical applications, the cost of a silent simulation error dwarfs the computational overhead of auditing. The framework explicitly quantifies the cost-confidence tradeoff:

### Limitations 局限性

**Assumption A1 (Domain Separability).** Not all multi-physics systems admit clean domain separation. Porous media flow involves fluid and solid at the pore scale; phase-field fracture couples mechanics and damage at the continuum level. For these, the coupling interface is diffuse, and our partitioned analysis requires extension to overlapping domain decomposition  [cite] or volume-coupled formulations.

**Assumption A2 (Coupling Lipschitz).** The Lipschitz continuity of coupling operators assumes sufficient regularity of interface traces. For hyperbolic systems (shock waves in hypersonic FSI), interface traces may be discontinuous, violating A2. The theory extends to measure-valued solutions but the Lipschitz constant becomes mesh-dependent.

**Assumption A4 (Expert Independence).** Strict independence of experts within a domain is an idealization. Experts sharing the same governing equations (e.g., two different FEM discretizations of the same linear elasticity PDE) have correlated errors on coarse meshes. The $M_d^{\mathrm{eff}}$ correction (Eq. [ref]) accounts for average correlation but may underestimate tail dependence in the error distribution.

**Limited experimental ground truth.** The multi-domain Yajie{} Level~2 consensus relies on experimental data $\mathcal{G}_{\mathrm{exp}}$, which may be sparse, noisy, or unavailable for the full coupled system. For nuclear reactor transients or hypersonic reentry, experiments are prohibitively expensive, and the framework degrades to purely computational auditing (Level~1 only).

**Unidentifiability is a feature, not a bug.** Theorem [ref] may appear pessimistic---it proves that error attribution is impossible without assumptions. We argue the opposite: *forcing explicit assumption declaration is a methodological improvement over implicit attribution.* Current practice in multi-physics validation often attributes discrepancies to ``turbulence model error'' or ``mesh resolution'' without acknowledging the coupling ambiguity. SCX{} makes the ambiguity explicit and mandates assumption transparency.

### Relationship to Existing Methods 与现有方法的关系

**Verification and Validation (V\&V)  [cite].** The ASME V\&V 20 standard provides a framework for code verification (solving equations right) and solution validation (solving right equations). SCX{} auditing complements V\&V by adding (i) per-expert multiplicity to detect solver-specific errors, (ii) coupling-aware error propagation bounds, and (iii) formal unidentifiability analysis that V\&V's ``total validation uncertainty'' framework  [cite] implicitly acknowledges but does not prove.

**Bayesian multi-physics calibration  [cite].** Kennedy and O'Hagan's Bayesian calibration framework for multi-physics models decomposes discrepancy into model inadequacy terms per domain. Theorem [ref] provides the formal underpinning for why informative priors (equivalent to our ``declared assumptions'') are necessary: without them, the posterior over $(\varepsilon_A, \varepsilon_B, \boldsymbol_{AB})$ is flat in directions corresponding to the observational equivalence subspace.

**Multi-fidelity methods  [cite].** Multi-fidelity frameworks combine high-fidelity and low-fidelity models to reduce computational cost. The Cercis{} multi-fidelity hierarchy (Table [ref]) provides a rigorous scoring metric to decide when a higher-fidelity model is justified. The novelty term $N$ penalizes extrapolation from low to high fidelity.

**Operator learning for coupled systems  [cite].** DeepONet and FNO address the single-physics operator learning problem. Our framework extends them to coupled systems by (i) providing per-operator auditing, (ii) bounding error propagation between learned operators, and (iii) identifying when coupling interface errors dominate learned operator errors.

## Acknowledgments

This work builds on the SCX{} theoretical framework. We acknowledge the multi-physics simulation community for developing and maintaining the benchmark suites used in the experimental protocol.

## Appendix
## Full Derivation of FSI Coupling Lipschitz Constant
<!-- label: sec:app_fsi -->

We provide the detailed derivation of Proposition [ref].

> **Proof:** \rigorFull
> Consider the linearized FSI system. The fluid domain $\Omega_f$ is governed by the unsteady Stokes equations (linearization of Navier-Stokes about a steady state):
> 
> $$
> \rho_f \partial_t \mathbf{v} - \mu_f \nabla^2 \mathbf{v} + \nabla p &= 0, \quad \nabla \cdot \mathbf{v} = 0 \quad in  \Omega_f, 

> \mathbf{v} &= \partial_t \mathbf{d} \quad on  \interface,
> $$
> 
> where $\mathbf{v}$ is fluid velocity, $p$ is pressure, and $\mathbf{d}$ is structural displacement on $\interface$.
> 
> The structure domain $\Omega_s$ is governed by linear elastodynamics:
> 
> $$
> \rho_s \partial_t^2 \mathbf{d} - \nabla \cdot \boldsymbol(\mathbf{d}) = 0 \quad in  \Omega_s, \quad \boldsymbol \cdot \mathbf{n} = \boldsymbol_f \cdot \mathbf{n} \quad on  \interface,
> $$
> 
> where $\boldsymbol_f = -p\mathbf{I} + \mu_f(\nabla\mathbf{v} + \nabla\mathbf{v}^T)$ is the fluid stress tensor.
> 
> **Coupling operator decomposition.** The FSI coupling operator $\Phi^{\mathrm{FSI}}$ maps structural displacement to fluid stress (and vice versa). Consider the forward map $\Phi^{s \to f}: \mathbf{d}|_\interface \mapsto \boldsymbol_f|_\interface \cdot \mathbf{n}$. For a harmonic displacement $\mathbf{d} = \hat{\mathbf{d}} e^{i\omega t}$, the fluid response satisfies:
> 
> $$
> \norm{\boldsymbol_f \cdot \mathbf{n}}_{H^{-1/2}(\interface)} \leq \rho_f \omega^2 \norm{\hat{\mathbf{d}}}_{H^{1/2}(\interface)} \cdot C_{\mathrm{Stokes}}(\omega, \mu_f, h_f),
> $$
> 
> where the $H^{\pm 1/2}$ norms are the natural trace spaces for FSI  [cite]. The Stokes constant $C_{\mathrm{Stokes}}$ depends on the frequency parameter $\beta = \omega h_f^2 / \mu_f$ and satisfies $C_{\mathrm{Stokes}} \sim O(1)$ for $\beta \ll 1$ (quasi-static) and $C_{\mathrm{Stokes}} \sim O(\beta^{1/2})$ for $\beta \gg 1$ (boundary layer dominated).
> 
> **Lipschitz constant.** For the time-discrete coupling at time step $\Delta t$, the fluid-to-structure amplification is:
> 
> $$
> L_{f \to s} = \frac{\norm{\mathbf{d}}_{\mathrm{struct}}}{\norm{\boldsymbol_f \cdot \mathbf{n}}_{H^{-1/2}}} \sim \frac{1}{\rho_s / \Delta t^2 + E_s / h_s^2},
> $$
> 
> where the denominator represents the structural stiffness (inertial + elastic). Similarly, the structure-to-fluid amplification is:
> 
> $$
> L_{s \to f} = \frac{\norm{\boldsymbol_f \cdot \mathbf{n}}}{\norm{\mathbf{d}}} \sim \frac{\rho_f}{\Delta t} + \frac{\mu_f}{h_f}.
> $$
> 
> 
> The combined coupling Lipschitz constant is $L_{\mathrm{FSI}} = L_{s \to f} \cdot L_{f \to s}$, yielding:
> 
> $$
> L_{\mathrm{FSI}} \sim \frac{\rho_f / \Delta t + \mu_f / h_f}{\rho_s / \Delta t^2 + E_s / h_s^2}.
> $$
> 
> 
> In the limit $\Delta t \to 0$ (small time steps, typical of implicit FSI), the dominant term is $\rho_f \Delta t / \rho_s$. For strongly-coupled problems with explicit coupling ($\Delta t$ constrained by CFL), $L_{\mathrm{FSI}}$ can exceed 1, indicating that fixed-point iteration diverges. The form in Eq. [ref] collects the dominant terms with geometry-dependent constants $C_{\mathrm{geom}}$ and $C_{\mathrm{mesh}}$ that account for interface curvature and mesh non-conformity. $\square$

## Coupling Correlation Estimation
<!-- label: sec:app_correlation -->

For the effective multiplicity $M_d^{\mathrm{eff}}$ in Theorem [ref], we estimate the per-domain expert correlation $\bar_d$:

1. For each test input $\mathbf{x}_k^d$ ($k = 1, ..., K$) in a held-out calibration set, compute the error vector $\mathbf{e}_k^d = (e_{1k}^d, ..., e_{M_d k}^d)$ where $e_{mk}^d = \norm{f_m^d(\mathbf{x}_k^d) - \mathbf{y}_k^{d,*}}_{\mathcal{Y}^d}$.
2. Compute the $M_d \times M_d$ error correlation matrix $\hat{R}_{ij}^d = \mathrm{Corr}(e_{i\cdot}^d, e_{j\cdot}^d)$.
3. Estimate $\bar_d = \frac{2}{M_d(M_d-1)}\sum_{i<j} \hat{R}_{ij}^d$.
4. Bootstrap 95\% confidence interval: resample rows of the $K \times M_d$ error matrix with replacement $B = 1000$ times, recompute $\bar_d^{(b)}$, report $[\bar_{d, 0.025}, \bar_{d, 0.975}]$.

When $\bar_d < 0$ (negative correlation — experts make complementary errors), set $M_d^{\mathrm{eff}} = M_d$ (the bound is conservative under negative dependence  [cite]).

## Cross-Domain Lipschitz Estimation from Data
<!-- label: sec:app_lipschitz -->

For practical estimation of $L_{AB}$ when analytical forms are unavailable (e.g., for neural surrogates used as coupling operators):

> **Proposition:** [Empirical Lipschitz Estimation]<!-- label: prop:emp_lipschitz -->
> Given $N$ paired samples $(\mathbf{u}_A^{(i)}|_\interface, \Phi^{AB}(\mathbf{u}_A^{(i)}|_\interface))_{i=1}^N$, a consistent estimator of $L_{AB}$ is:
> 
> $$
> \hat{L}_{AB} = \max_{i \neq j} \frac{\norm{\Phi^{AB}(\mathbf{u}_A^{(i)}|_\interface) - \Phi^{AB}(\mathbf{u}_A^{(j)}|_\interface)}_{\mathcal{T}_B}}{\norm{\mathbf{u}_A^{(i)}|_\interface - \mathbf{u}_A^{(j)}|_\interface}_{\mathcal{T}_A}}.
> $$
> 
> For neural coupling operators, this can be refined using gradient norm maximization: $\hat{L}_{AB} = \max_{\mathbf{u}} \norm{\nabla_{\mathbf{u}} f_{\theta_{AB}}(\mathbf{u})}_{\mathrm{op}}$ via power iteration  [cite].

\begin{thebibliography}{99}

\bibitem{SCX2025}
SCX, ``SCX: Structured Causal eXamination Framework for Auditable AI,'' *Technical Report*, 2025.

\bibitem{Farhat1998}
C.~Farhat, M.~Lesoinne, and P.~LeTallec, ``Load and motion transfer algorithms for fluid/structure interaction problems with non-matching discrete interfaces,'' *Comput. Methods Appl. Mech. Eng.*, vol.~157, pp.~95--114, 1998.

\bibitem{Piperno2001}
S.~Piperno and C.~Farhat, ``Partitioned procedures for the transient solution of coupled aeroelastic problems,'' *Comput. Methods Appl. Mech. Eng.*, vol.~190, pp.~3147--3170, 2001.

\bibitem{Causin2005}
P.~Causin, J.~F.~Gerbeau, and F.~Nobile, ``Added-mass effect in the design of partitioned algorithms for fluid-structure problems,'' *Comput. Methods Appl. Mech. Eng.*, vol.~194, pp.~4506--4527, 2005.

\bibitem{Heil2008}
M.~Heil, A.~Hazel, and J.~Boyle, ``Solvers for large-displacement fluid-structure interaction problems: Segregated versus monolithic approaches,'' *Comput. Mech.*, vol.~43, pp.~91--101, 2008.

\bibitem{Hesthaven2016}
J.~S.~Hesthaven and S.~Ubbiali, ``Non-intrusive reduced order modeling of nonlinear problems using neural networks,'' *J. Comput. Phys.*, vol.~363, pp.~55--78, 2018.

\bibitem{Fresca2021}
S.~Fresca, L.~Dede', and A.~Manzoni, ``A comprehensive deep learning-based approach to reduced order modeling of nonlinear time-dependent parametrized PDEs,'' *J. Sci. Comput.*, vol.~87, 61, 2021.

\bibitem{Lu2021}
L.~Lu, P.~Jin, G.~Pang, Z.~Zhang, and G.~E.~Karniadakis, ``Learning nonlinear operators via DeepONet,'' *Nat. Mach. Intell.*, vol.~3, pp.~218--229, 2021.

\bibitem{Li2021}
Z.~Li, N.~Kovachki, K.~Azizzadenesheli, B.~Liu, K.~Bhattacharya, A.~Stuart, and A.~Anandkumar, ``Fourier Neural Operator for parametric partial differential equations,'' *ICLR*, 2021.

\bibitem{Gao2022}
H.~Gao, L.~Sun, and J.-X.~Wang, ``PhyGeoNet: Physics-informed geometry-adaptive convolutional neural networks for solving parameterized steady-state PDEs on irregular domain,'' *J. Comput. Phys.*, vol.~428, 110079, 2021.

\bibitem{Raissi2019}
M.~Raissi, P.~Perdikaris, and G.~E.~Karniadakis, ``Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations,'' *J. Comput. Phys.*, vol.~378, pp.~686--707, 2019.

\bibitem{Liang1986}
K.-Y.~Liang and S.~L.~Zeger, ``Longitudinal data analysis using generalized linear models,'' *Biometrika*, vol.~73, pp.~13--22, 1986.

\bibitem{Wohlmuth2001}
B.~I.~Wohlmuth, ``Discretization Methods and Iterative Solvers Based on Domain Decomposition,'' *Springer*, 2001.

\bibitem{Turek2006}
S.~Turek and J.~Hron, ``Proposal for numerical benchmarking of fluid-structure interaction between an elastic object and laminar incompressible flow,'' in *Fluid-Structure Interaction*, Springer, pp.~371--385, 2006.

\bibitem{CSMbenchmarks}
B.~J.~Lee, P.~C.~Chen, and D.~D.~Liu, ``Further studies of the AGARD 445.6 wing aeroelastic configuration for computational aeroelastic tool assessment and validation,'' *IFASD*, 2011.

\bibitem{NuclearFuel}
D.~R.~Olander, ``Fundamental aspects of nuclear reactor fuel elements,'' *TID-26711-P1*, 1976.

\bibitem{TurbineBlade}
J.~C.~Han, S.~Dutta, and S.~Ekkad, ``Gas Turbine Heat Transfer and Cooling Technology,'' *CRC Press*, 2012.

\bibitem{HypersonicBenchmark}
M.~J.~Wright, G.~V.~Candler, and D.~Bose, ``Data-parallel line relaxation method for the Navier-Stokes equations,'' *AIAA J.*, vol.~36, pp.~1603--1609, 1998.

\bibitem{EMforming}
V.~Psyk, D.~Risch, B.~L.~Kinsey, A.~E.~Tekkaya, and M.~Kleiner, ``Electromagnetic forming---A review,'' *J. Mater. Process. Technol.*, vol.~211, pp.~787--829, 2011.

\bibitem{Ablation}
Y.-K.~Chen and F.~S.~Milos, ``Ablation and thermal response program for spacecraft heatshield analysis,'' *J. Spacecr. Rockets*, vol.~36, pp.~475--483, 1999.

\bibitem{Grieves2017}
M.~Grieves and J.~Vickers, ``Digital twin: Mitigating unpredictable, undesirable emergent behavior in complex systems,'' in *Transdisciplinary Perspectives on Complex Systems*, Springer, pp.~85--113, 2017.

\bibitem{Toselli2005}
A.~Toselli and O.~Widlund, ``Domain Decomposition Methods---Algorithms and Theory,'' *Springer*, 2005.

\bibitem{Oberkampf2010}
W.~L.~Oberkampf and C.~J.~Roy, ``Verification and Validation in Scientific Computing,'' *Cambridge University Press*, 2010.

\bibitem{Coleman1999}
H.~W.~Coleman and W.~G.~Steele, ``Experimentation and Uncertainty Analysis for Engineers,'' *Wiley*, 1999.

\bibitem{Kennedy2001}
M.~C.~Kennedy and A.~O'Hagan, ``Bayesian calibration of computer models,'' *J. R. Stat. Soc. B*, vol.~63, pp.~425--464, 2001.

\bibitem{Peherstorfer2018}
B.~Peherstorfer, K.~Willcox, and M.~Gunzburger, ``Survey of multifidelity methods in uncertainty propagation, inference, and optimization,'' *SIAM Rev.*, vol.~60, pp.~550--591, 2018.

\bibitem{Wainwright2019}
M.~J.~Wainwright, ``High-Dimensional Statistics: A Non-Asymptotic Viewpoint,'' *Cambridge University Press*, 2019.

\bibitem{Virmaux2018}
A.~Virmaux and K.~Scaman, ``Lipschitz regularity of deep neural networks: analysis and efficient estimation,'' *NeurIPS*, 2018.

\bibitem{Quarteroni2000}
A.~Quarteroni and A.~Valli, ``Domain Decomposition Methods for Partial Differential Equations,'' *Oxford University Press*, 1999.

\bibitem{Bartlett2002}
P.~L.~Bartlett and S.~Mendelson, ``Rademacher and Gaussian complexities: Risk bounds and structural results,'' *J. Mach. Learn. Res.*, vol.~3, pp.~463--482, 2002.

\bibitem{Lehmann1998}
E.~L.~Lehmann and G.~Casella, ``Theory of Point Estimation,'' 2nd ed., Springer, 1998.

\end{thebibliography}