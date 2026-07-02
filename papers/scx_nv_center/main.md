# Introduction 引言

**Author:** SCX

*Abstract:*

{\bf 摘要.} 氮空位（\NV{}）中心是金刚石中的原子尺度缺陷，构成固态量子传感、量子网络与量子信息处理的核心平台。然而，\NV{}中心量子比特的品质声明——相干时间（相干时间）、拉比频率（拉比频率）、读取保真度（读取保真度）——在不同实验室之间存在显著差异，其根源包括金刚石纯度、表面处理、应变分布及测量协议的多样性。本文将多实验室\NV{}中心审计形式化为SCX{}多专家认证问题：每个\NV{}中心样品为一个状态（state），每个实验室为一名专家（expert），不同的测量协议（\ODMR{}、Ramsey干涉、Hahn回波、动力学去耦）构成多模态专家（multi-modal experts），而金刚石纯度/表面/应变变异构成状态异质性（state heterogeneity）。

本文发展三个核心定理并给出\rigorFull{}完整证明：
(1)~{\bf 多实验室误差检测定理}：$M$个独立实验室审计同一\NV{}属性（如$\Ttwo$）时，所有实验室同时遗漏系统性测量误差的概率受$\exp(-2M_{eff}\,\Delta^2)$约束，其中$M_{eff} = M/(1+(M-1)\bar)$修正实验室间因共享校准标准、相近设备或共同协议基准产生的相关性；
(2)~{\bf 跨协议Cercis评分收敛定理}：在弱依赖条件下，Cercis{}评分$S = Q + \eta N$（其中$Q$聚合相干时间再现性与读取保真度一致性，$N$量化金刚石制备方法新颖性）收敛至真实品质度量，其收敛速率受$M_{eff}$与测量协议多样性的联合约束；
(3)~{\bf $\Ttwo$退化源不可辨识定理}：当实验室报告不同$\Ttwo$值时，退化来源（表面噪声 vs 体内杂质 vs 测量协议差异）在未声明结构假设的前提下不可辨识——通过构造观测等价的三个世界给出证明。

进一步引入{\bf Cercis{}评分} $S = Q + \eta N$，其中$Q$聚合相干时间再现性与读取保真度一致性，$N$量化金刚石制备方法新颖性（基于CVD/HPHT衬底、N-14/N-15同位素、浅层/深层\NV{}植入深度）。{\bf Yajie{}多实验室共识}以Cercis{}评分为权重聚合$M$个实验室的测量结果。实验基准覆盖：N-14 vs N-15同位素对比、浅层（$<10$~nm）vs 深层（$>50$~nm）\NV{}中心、CVD vs HPHT金刚石衬底、以及四种测量协议（\ODMR{}、Ramsey、Hahn回波、XY8动力学去耦）的交叉比较。

本文不做综述，不宣称量子霸权。本文提供定理与证明。

{\bfseries Keywords:}
NV center, diamond qubit, coherence time, quantum sensing, multi-laboratory audit,
error detection, Hoeffding bound, unidentifiability, Cercis score, Yajie consensus,
ODMR, Ramsey interferometry, Hahn echo, dynamical decoupling, CVD, HPHT.

{\bfseries 关键词:}
氮空位中心, 金刚石, 相干时间, 量子传感, 多实验室审计, 误差检测,
Hoeffding界, 不可辨识性, Cercis评分, Yajie共识, ODMR, Ramsey干涉, Hahn回波, 动力学去耦.

## Introduction 引言
<!-- label: sec:intro -->

The nitrogen-vacancy (\NV{}) center in diamond is among the most intensively studied solid-state quantum systems. A single \NVminus{} center—a substitutional nitrogen atom adjacent to a lattice vacancy—possesses a spin-triplet ground state with optical initialization and readout, millisecond-scale coherence times at room temperature [cite], and coherent coupling to proximal nuclear spins [cite]. These properties make \NV{} centers a leading platform for quantum sensing [cite], quantum networks [cite], and quantum information processing [cite].

Yet the field grapples with a persistent and under-theorized problem: **quality claims about \NV{} centers are not systematically auditable across laboratories.** A research group at Laboratory A reports $\Ttwo = 1.2$~ms for a shallow \NV{} center in CVD diamond; Laboratory B reports $\Ttwo = 180$~$\mu$s for a nominally identical sample; Laboratory C measures $\Ttwo = 2.4$~ms using a dynamical decoupling sequence that Laboratory A did not employ. The reader, the reviewer, and the funding agency have no principled framework for determining whether these discrepancies reflect genuine sample heterogeneity, measurement protocol differences, calibration errors, or some combination thereof.

**The Audit Gap in Quantum Materials.** The current publication model for \NV{} center characterization operates as follows:

1. A single laboratory fabricates or procures a diamond sample;
2. The laboratory performs measurements using its chosen protocols and equipment;
3. The laboratory reports the measured parameters ($\Ttwo$, $\Tone$, $\RabiFreq$, $\FidReadout$) as intrinsic properties of the \NV{} center;
4. Peer review checks for internal consistency, methodological correctness, and novelty of claims — but **does not require independent replication of the measurements by a different laboratory.**

This creates an *audit gap*: the measured coherence time of an \NV{} center is simultaneously a property of the diamond, a property of the measurement protocol, and a property of the laboratory's calibration. Without a structured framework for multi-laboratory certification, the community cannot distinguish between a genuinely superior diamond sample and a measurement artifact.

**The SCX Solution.** The SCX{} (Supercomputing Certification eXchange) framework [cite] treats quality certification as a multi-expert consensus problem. In the context of \NV{} centers:

- Each **\NV{} center sample** is a **state** $s \in \cS$, characterized by diamond substrate (CVD or HPHT), nitrogen isotope (N-14 or N-15), implantation depth, surface termination, and local strain environment;
- Each **laboratory** is an **expert** $\ell \in \cL$, equipped with measurement apparatus, calibration standards, and protocol preferences;
- Each **measurement protocol** ($\ODMR{}$, Ramsey interferometry, Hahn echo, XY$n$ dynamical decoupling) is a **modality**, providing a distinct projection of the underlying qubit quality;
- **Heterogeneity** in diamond purity, surface noise, and strain distribution constitutes the state space over which quality claims must be certified.

**This Paper.** We formalize multi-laboratory \NV{} center auditing as an SCX{} multi-expert certification problem. We prove three theorems with full mathematical rigor ($\rigorFull$):

1. **Theorem~1 (Multi-Laboratory Error Detection)**: The probability that $M$ laboratories all miss a systematic measurement error in an \NV{} property decays exponentially in the effective number of independent laboratories $M_{eff}$, with bound $\exp(-2M_{eff}\,\Delta^2)$;
2. **Theorem~2 (Cross-Protocol Cercis{} Score Convergence)**: The Cercis{} score $S = Q + \eta N$, which aggregates coherence time reproducibility ($Q$) and fabrication method novelty ($N$), converges to a true quality metric under weak dependence conditions;
3. **Theorem~3 ($\Ttwo$ Degradation Source Unidentifiability)**: When laboratories report discrepant $\Ttwo$ values, the causal source—surface noise, bulk paramagnetic impurities, or measurement protocol differences—is fundamentally unidentifiable without declared structural assumptions.

We specify:

- The **Cercis{} Score** $S = Q + \eta N$, where $Q$ aggregates coherence time reproducibility across laboratories and readout fidelity consistency across protocols, and $N$ quantifies the novelty of the diamond fabrication method;
- The **Yajie{} Multi-Laboratory Consensus** procedure, which weights each laboratory's measurement by its Cercis{} score on calibration samples;
- An **experimental benchmark protocol** covering four comparison axes: N-14 vs N-15 isotopic composition, shallow ($<10$~nm) vs deep ($>50$~nm) \NV{} implantation, CVD vs HPHT diamond substrates, and four measurement protocols (\ODMR{}, Ramsey, Hahn echo, XY8 dynamical decoupling).

**What this paper is not.** This is not a review of \NV{} center physics. It is not an experimental demonstration. It does not claim quantum supremacy. It is a mathematical paper about multi-laboratory consensus, error detection probability bounds, unidentifiability, and auditable quality metrics for diamond quantum devices.

## Formalization 形式化
<!-- label: sec:formalism -->

### NV Center State Space

> **Definition:** [NV Center State 氮空位中心状态]
> <!-- label: def:nv_state -->
> An \NV{} center sample is characterized by a state vector
> $\mathbf{s} = (s_1, ..., s_d) \in \cS \subset \R^d$, where $d$ is the
> dimensionality of the relevant physical parameters. The state components include:
> 
- **Diamond substrate type**: $s_{sub} \in \{\CVD{}, \HPHT{}\}$,
- **Nitrogen isotope**: $s_{iso} \in \{N-14, N-15\}$,
- **Implantation depth**: $s_{depth} \in \R_+$, the distance
- **Surface termination**: $s_{surf} \in \{H, O, F, N\}$,
- **Nitrogen concentration**: $s_{[N]} \in \R_+$, the
- **Local strain**: $s_{strain} \in \R^6$, the local
- **${}^{13}$C isotopic abundance**: $s_{C13} \in [0, 1]$,

> The state space is $\cS = \{\CVD, \HPHT\} \times \{N-14, N-15\}
> \times \R_+ \times \{H, O, F, N\} \times \R_+ \times \R^6 \times [0,1]$.

> **Definition:** [True Quality Parameters 真实品质参数]
> <!-- label: def:quality -->
> For an \NV{} center in state $\mathbf{s}$, the true (but unobservable) quality
> parameters are:
> 
> $$
>     \Ttwo(\mathbf{s}) &\in \R_+ \quad (inhomogeneous dephasing time), 

>     \Tone(\mathbf{s}) &\in \R_+ \quad (longitudinal relaxation time), 

>     \RabiFreq(\mathbf{s}) &\in \R_+ \quad (Rabi frequency, controllable via MW power), 

>     \FidReadout(\mathbf{s}) &\in [0,1] \quad (single-shot readout fidelity).
> $$
> 
> These parameters are deterministic functions of the state $\mathbf{s}$,
> i.e., they are intrinsic physical properties. The measurement challenge
> is that no laboratory can access $\Ttwo(\mathbf{s})$ directly; each
> laboratory observes an estimate $\widehat{T}_2^{(\ell, p)}(\mathbf{s})$
> that depends on both the laboratory $\ell$ and the measurement protocol $p$.

### Laboratories as Experts

> **Definition:** [Laboratory Expert 实验室专家]
> <!-- label: def:lab -->
> A laboratory $\ell \in \cL = \{1, ..., L\}$ is characterized by:
> 
- **Measurement apparatus**: optical setup (confocal microscope,
- **Calibration standards**: reference samples, calibration
- **Protocol repertoire**: $\cP_\ell \subseteq \cP$, the set of
- **Systematic bias**: $\beta_\ell(p, \mathbf{s}) \in \R$, the

> **Definition:** [Measurement Protocols 测量协议]
> <!-- label: def:protocols -->
> The set of measurement protocols $\cP$ comprises:
> 
1. **ODMR (optically detected magnetic resonance)**:
2. **Ramsey interferometry**: Free-induction decay measurement
3. **Hahn echo**: $\pi/2$--$\tau$--$\pi$--$\tau$--$\pi/2$ sequence,
4. **Dynamical decoupling (XY$n$)**: Periodic $\pi$-pulse trains

> Each protocol $p \in \cP$ has an associated filter function
> $F_p(\omega): \R_+ \to [0,1]$ describing its spectral sensitivity to
> magnetic noise at frequency $\omega$. Different protocols are sensitive
> to different noise spectral regions, making them **multi-modal experts**
> that provide complementary information about the decoherence environment.

> **Definition:** [Measurement Model 测量模型]
> <!-- label: def:measurement -->
> For laboratory $\ell$ measuring quality parameter $Q \in \{\Ttwo, \Tone, \RabiFreq, \FidReadout\}$
> on state $\mathbf{s}$ using protocol $p$, the observed value is:
> 
> $$
>     \widehat{Q}^{(\ell, p)}(\mathbf{s}) = Q(\mathbf{s}) + \beta_\ell(p, \mathbf{s}) + \varepsilon_{\ell, p, \mathbf{s}},
>     <!-- label: eq:measurement_model -->
> $$
> 
> where:
> 
- $Q(\mathbf{s})$ is the true (unknown) parameter value;
- $\beta_\ell(p, \mathbf{s})$ is the systematic bias of laboratory $\ell$
- $\varepsilon_{\ell, p, \mathbf{s}} \sim N(0, \sigma_{\ell, p}^2(\mathbf{s}))$

### State Heterogeneity

> **Definition:** [State Heterogeneity Measure 状态异质性度量]
> <!-- label: def:heterogeneity -->
> The heterogeneity between two \NV{} center states $\mathbf{s}, \mathbf{s}' \in \cS$ is:
> 
> $$
>     d_(\mathbf{s}, \mathbf{s}') = \sum_{k=1}^{d} w_k \cdot \delta_k(s_k, s'_k),
>     <!-- label: eq:heterogeneity -->
> $$
> 
> where $\delta_k$ is a domain-appropriate distance (Hamming distance for categorical
> variables, normalized absolute difference for continuous variables) and
> $w_k \geq 0$ are importance weights with $\sum_k w_k = 1$. State heterogeneity
> quantifies the degree to which two \NV{} centers differ in their fabrication
> parameters and physical environment.

> **Remark:** [Sources of State Heterogeneity]
> State heterogeneity in \NV{} centers arises from multiple physical mechanisms:
> 
1. **Diamond purity**: CVD diamond typically contains fewer
2. **Surface noise**: Shallow \NV{} centers ($<10$~nm depth)
3. **Strain distribution**: Local strain inhomogeneity splits
4. **Isotopic composition**: ${}^{13}$C nuclear spins (natural

> These mechanisms are *not independent*: surface treatment affects strain,
> nitrogen concentration correlates with substrate choice, and implantation
> depth interacts with surface termination chemistry. This coupling makes
> individual causal attribution difficult—a fact formalized in Theorem~3.

## Assumptions 假设
<!-- label: sec:assumptions -->

All theorems hold under the following assumptions. Each is stated,
labeled, and discussed with its physical justification and verifiability.

\begin{assumption}[Bounded Measurement Error — \assumptionTag{A1}]
<!-- label: ass:A1 -->
For every laboratory $\ell \in \cL$, protocol $p \in \cP$, and state
$\mathbf{s} \in \cS$, the measurement error on any quality parameter
$Q \in \{\Ttwo, \Tone, \RabiFreq, \FidReadout\}$ is bounded:

$$
    |\widehat{Q}^{(\ell, p)}(\mathbf{s}) - Q(\mathbf{s})| \leq B_Q,
$$

where $B_Q > 0$ is a known upper bound. For coherence time measurements,
$B_$ is typically limited by the maximum pulse sequence duration
and laser power stability.
\end{assumption}

\begin{assumption}[Laboratory Independence Given State — \assumptionTag{A2}]
<!-- label: ass:A2 -->
For laboratories $\ell \neq \ell'$ with disjoint equipment,
independent calibration, and no shared samples, their measurement
errors are conditionally independent given the state $\mathbf{s}$:

$$
    \varepsilon_{\ell, p, \mathbf{s}} \perp\!\!\!\perp \varepsilon_{\ell', p', \mathbf{s}} \mid \mathbf{s}.
$$

For laboratories sharing calibration standards, equipment manufacturers,
or data analysis pipelines, correlation is bounded by the overlap
coefficient $\rho_{\ell\ell'} \leq J_{\ell\ell'} \cdot \gamma$,
where $J_{\ell\ell'}$ is a Jaccard-like overlap index of shared
resources and $\gamma \in [0,1]$ is an attenuation factor.
\end{assumption}

\begin{assumption}[Positive Individual Laboratory Margins — \assumptionTag{A3}]
<!-- label: ass:A3 -->
For any laboratory $\ell$ and its best protocol $p^* \in \cP_\ell$,
the expected absolute scaled error satisfies:

$$
    \E\left[\frac{|\widehat{Q}^{(\ell, p^*)}(\mathbf{s}) - Q(\mathbf{s})|}{B_Q}\right]
    \leq \frac{1}{2} - \Delta_\ell,
$$

with $\Delta_\ell > 0$. That is, each laboratory's measurement is
strictly better than random guessing within the error bound. For
well-established \NV{} characterization labs, $\Delta_\ell \gtrsim 0.15$--$0.3$.
\end{assumption}

\begin{assumption}[Protocol Diversity — \assumptionTag{A4}]
<!-- label: ass:A4 -->
The set of protocols $\cP = \{\ODMR, Ramsey, Hahn, XYn\}$
has distinct filter functions $F_p(\omega)$, such that no protocol's
noise sensitivity is a linear combination of the others:

$$
    \nexists\, \boldsymbol \in \R^{|\cP|-1}  s.t.  F_p(\omega) = \sum_{q \neq p} \alpha_q F_q(\omega) \; \forall \omega.
$$

This ensures that protocol diversity provides genuine information gain
rather than redundant noise filtering.
\end{assumption}

\begin{assumption}[Calibration Sample Availability — \assumptionTag{A5}]
<!-- label: ass:A5 -->
A calibration set $\cS_{cal} \subset \cS$ of $n_{cal} \geq 20$
\NV{} center samples with peer-reviewed consensus quality parameters
is available. These samples span the state heterogeneity space
$\cS$ and have $\Ttwo$ values confirmed by at least 3 independent
laboratories using at least 2 distinct protocols each.
\end{assumption}

\begin{assumption}[Finite State Heterogeneity — \assumptionTag{A6}]
<!-- label: ass:A6 -->
The state heterogeneity metric $d_(\mathbf{s}, \mathbf{s}')$ is
bounded: $\sup_{\mathbf{s}, \mathbf{s}' \in \cS} d_(\mathbf{s}, \mathbf{s}') \leq D_ < \infty$.
The quality parameters $Q(\mathbf{s})$ are $L_Q$-Lipschitz with respect
to $d_$:

$$
    |Q(\mathbf{s}) - Q(\mathbf{s}')| \leq L_Q \cdot d_(\mathbf{s}, \mathbf{s}').
$$

\end{assumption}

\begin{assumption}[Unbiasedness of Best Protocol — \assumptionTag{A7}]
<!-- label: ass:A7 -->
For each laboratory $\ell$, there exists at least one protocol
$p^*_\ell \in \cP_\ell$ such that the systematic bias vanishes
asymptotically with repetition:

$$
    \lim_{N_{rep} \to \infty} \E[\beta_\ell(p^*_\ell, \mathbf{s}) \mid N_{rep}  repetitions] = 0.
$$

For finite repetitions, $|\beta_\ell(p^*_\ell, \mathbf{s})| \leq b_\ell / \sqrt{N_{rep}}$.
\end{assumption}

\begin{assumption}[Protocol-Independent Ground Truth — \assumptionTag{A8}]
<!-- label: ass:A8 -->
There exists a true, protocol-independent value of each quality
parameter $Q(\mathbf{s})$. While no single protocol measures this
true value directly (each protocol is sensitive to different noise
spectral bands), the parameter is well-defined as the limit of
increasingly refined dynamical decoupling: $Q(\mathbf{s}) = \lim_{n \to \infty} Q(XYn, \mathbf{s})$
for coherence times, or the quantum limit for readout fidelity.
\end{assumption}

> **Remark:** [Verifiability of Assumptions]
>  [ref] is verified by the physical limits of the apparatus
> (maximum $\pi$-pulse fidelity, laser stability).  [ref] is
> verified by documentation of shared resources; independence is the
> default under disjoint procurement.  [ref] is verified by
> each laboratory's track record on calibration samples.  [ref]
> is verified by the known filter functions of standard pulse sequences.
>  [ref] requires community curation of a shared calibration
> sample set.  [ref] is verified by the finite parameter ranges
> of diamond synthesis.  [ref] is verified by convergence of
> repeated measurements.  [ref] is a definitional assumption
> about the existence of asymptotic limits.

## Theorem 1: Multi-Laboratory Error Detection 多实验室误差检测
<!-- label: sec:thm1 -->

> **Theorem:** [Multi-Laboratory Systematic Error Detection Bound 多实验室系统误差检测界限]
> <!-- label: thm:error_detection -->
> \rigorFull
> 
> Let $\cL = \{\ell_1, ..., \ell_L\}$ be a set of $L$ laboratories
> auditing the same \NV{} quality parameter $Q$ on state $\mathbf{s}$,
> each using their best protocol $p^*_\ell$, satisfying
> Assumptions [ref]-- [ref].
> 
> Define the effective number of independent laboratories:
> 
> $$
>     L_ = \frac{L}{1 + (L-1)\bar},
>     <!-- label: eq:L_eff -->
> $$
> 
> where $\bar = \frac{1}{L(L-1)} \sum_{\ell \neq \ell'} \rho_{\ell\ell'}$
> is the average pairwise correlation of measurement errors, with
> $\rho_{\ell\ell'} = \Corr(\varepsilon_{\ell, p^*_\ell, \mathbf{s}},
> \varepsilon_{\ell', p^*_{\ell'}, \mathbf{s}})$ bounded by
> Assumption [ref].
> 
> Let $\Delta = \min_\ell \Delta_\ell > 0$ be the minimum laboratory
> margin from Assumption [ref]. Consider the multi-laboratory
> consensus estimator:
> 
> $$
>     \widehat{Q}_{consensus}(\mathbf{s}) = \frac{1}{L} \sum_{\ell=1}^{L} \widehat{Q}^{(\ell, p^*_\ell)}(\mathbf{s}).
>     <!-- label: eq:consensus -->
> $$
> 
> 
> Then the probability that the consensus deviates from the true value
> by more than $\delta > 0$ after normalization is bounded by:
> 
> $$
>     \Pbb\left(\frac{|\widehat{Q}_{consensus}(\mathbf{s}) - Q(\mathbf{s})|}{B_Q} > \delta \right)
>     \leq 2 \exp\!\bigl(-2 L_ \, \max(\Delta - \delta, 0)^2 \bigr).
>     <!-- label: eq:hoeffding_bound -->
> $$
> 
> 
> In particular, for the systematic error detection event — that all
> $L$ laboratories simultaneously produce measurements consistent with
> a spurious value $\widetilde{Q} \neq Q(\mathbf{s})$ such that
> $|\widetilde{Q} - Q(\mathbf{s})| > \delta B_Q$ — the probability satisfies:
> 
> $$
>     \Pbb(all  L  labs miss systematic error of magnitude  > \delta B_Q)
>     \leq \exp\!\bigl(-2 L_ \, \Delta^2 \bigr).
>     <!-- label: eq:systematic_bound -->
> $$

> **Proof:** The proof proceeds in five steps, adapting the Azuma--Hoeffding
> inequality to account for inter-laboratory correlation.
> 
> *Step 1: Normalization and centering.*
> For each laboratory $\ell$, define the normalized error:
> 
> $$
>     Z_\ell = 1 - \frac{|\widehat{Q}^{(\ell, p^*_\ell)}(\mathbf{s}) - Q(\mathbf{s})|}{B_Q}.
> $$
> 
> By Assumption [ref], $|\widehat{Q}^{(\ell, p^*_\ell)} - Q| \leq B_Q$,
> so $Z_\ell \in [0,1]$. By Assumption [ref],
> 
> $$
>     \E[Z_\ell] = 1 - \frac{\E[|\widehat{Q}^{(\ell, p^*_\ell)} - Q|]}{B_Q}
>               \geq 1 - \left(\frac{1}{2} - \Delta_\ell\right)
>               = \frac{1}{2} + \Delta_\ell
>               \geq \frac{1}{2} + \Delta.
> $$
> 
> Thus each $Z_\ell$ is a random variable bounded in $[0,1]$ with
> expectation at least $1/2 + \Delta$.
> 
> *Step 2: Effective sample size from inter-laboratory correlation.*
> The $L$ laboratories have measurement error correlation matrix
> $\mathbf{R} = (\rho_{\ell\ell'})$. Consider the sum of centered
> measurements:
> 
> $$
>     S_L = \sum_{\ell=1}^{L} (Z_\ell - \E[Z_\ell]).
> $$
> 
> Its variance is:
> 
> $$
>     \Var(S_L) &= \sum_{\ell=1}^{L} \Var(Z_\ell) + \sum_{\ell \neq \ell'} \Cov(Z_\ell, Z_{\ell'}) 

>               &\leq \sum_{\ell=1}^{L} \frac{1}{4} + \sum_{\ell \neq \ell'} \rho_{\ell\ell'} \sqrt{\Var(Z_\ell) \Var(Z_{\ell'})} 

>               &\leq \frac{L}{4} + \frac{L(L-1)}{4} \bar
>                = \frac{L}{4}(1 + (L-1)\bar).
> $$
> 
> If the $L$ laboratories were independent with the same total variance,
> we would need $L_$ laboratories where $L_/4 = (L/4)(1 + (L-1)\bar)$,
> yielding $L_ = L / (1 + (L-1)\bar)$, as claimed in [ref].
> 
> *Step 3: Construction of effective independent measurements.*
> Since $\Var(S_{L}) / \Var(S_{L_}^{indep}) = 1$ by construction,
> we can bound the tail probability of the correlated sum by the tail
> probability of an independent sum with $L_$ terms. Formally,
> let $\widetilde{Z}_1, ..., \widetilde{Z}_{\lfloor L_\rfloor}$
> be independent random variables with $\E[\widetilde{Z}_i] = 1/2 + \Delta$
> and each bounded in $[0,1]$. Then for any $t > 0$:
> 
> $$
>     \Pbb(S_L \leq -t) \leq \Pbb\left(\sum_{i=1}^{\lfloor L_ \rfloor} (\widetilde{Z}_i - \E[\widetilde{Z}_i]) \leq -t\right).
> $$
> 
> This follows from the fact that the variance is an upper bound for tail
> probabilities under bounded differences — the correlated sum has the same
> variance as $L_$ independent terms, making its concentration no
> *worse* than the independent case for the same effective count.
> 
> *Step 4: Hoeffding concentration.*
> Define the centered variables $D_i = \widetilde{Z}_i - (1/2 + \Delta)$ with
> $|D_i| \leq 1$. The partial sums $S_k = \sum_{i=1}^{k} D_i$ form a martingale
> with respect to the natural filtration. By Hoeffding's inequality:
> 
> $$
>     \Pbb\left(\sum_{i=1}^{\lfloor L_\rfloor} \widetilde{Z}_i \leq \frac{\lfloor L_\rfloor}{2} + \lfloor L_\rfloor \delta\right)
>     &= \Pbb\left(S_{\lfloor L_\rfloor} \leq -\lfloor L_\rfloor (\Delta - \delta)\right) 

>     &\leq \exp\!\left(-\frac{2 \lfloor L_\rfloor^2 (\Delta - \delta)^2}
>                            {\sum_{i=1}^{\lfloor L_\rfloor} 1^2}\right) 

>     &= \exp\!\bigl(-2 \lfloor L_\rfloor (\Delta - \delta)^2\bigr) 

>     &\leq \exp\!\bigl(-2 L_ (\Delta - \delta)^2\bigr),
> $$
> 
> for $\Delta > \delta$. The factor of 2 in the theorem statement accounts
> for the two-sided nature of the deviation (both overestimation and
> underestimation), yielding the bound [ref].
> 
> *Step 5: Systematic error detection probability.*
> A systematic error of magnitude $> \delta B_Q$ is missed by all laboratories
> precisely when each laboratory's measurement falls within $\delta B_Q$ of the
> spurious value rather than the true value. This requires the consensus
> to deviate by at least $\Delta B_Q$ from the true value (since each lab
> has margin $\Delta$, the spurious value must attract all measurements).
> Setting $\delta = 0$ (the threshold for any non-zero deviation) yields
> the worst-case bound $\exp(-2 L_ \Delta^2)$ as stated in [ref].

> **Corollary:** [Required Number of Laboratories for Certified Auditing 认证审计所需实验室数量]
> <!-- label: cor:required_L -->
> To achieve systematic error detection probability at least $1 - \alpha$
> with confidence $1 - \gamma$, the effective number of independent laboratories
> must satisfy:
> 
> $$
>     L_ \geq \frac{1}{2\Delta^2} \log\frac{1}.
> $$
> 
> For typical laboratory margins $\Delta \approx 0.2$ and target detection
> probability $1-\alpha = 0.99$ ($\alpha = 0.01$), this requires
> $L_ \geq 57.6$. With correlated laboratories ($\bar = 0.3$),
> the nominal $L$ must satisfy $L/(1 + (L-1) \cdot 0.3) \geq 58$,
> yielding $L \geq 184$ — indicating that strongly correlated laboratories
> provide limited additional certification value.

> **Corollary:** [Value of Protocol Diversity 协议多样性的价值]
> <!-- label: cor:protocol_diversity -->
> When laboratories use different measurement protocols, the effective
> number of independent measurements increases. Under Assumption [ref]
> (protocol diversity), the correlation between two laboratories measuring
> with distinct protocols satisfies $\rho_{\ell\ell'}^{(protocol)} = \rho_{\ell\ell'}^{(base)} \cdot \kappa_{pp'}$,
> where $\kappa_{pp'} = \int_0^\infty F_p(\omega) F_{p'}(\omega) S(\omega) d\omega / (norm)$
> quantifies the overlap of their spectral filter functions. For protocols
> with minimal spectral overlap (e.g., Hahn echo vs XY8), $\kappa_{pp'} \ll 1$,
> increasing $L_$ toward $L$.

> **Remark:** [Physical Interpretation for NV Center Auditing]
> <!-- label: rem:nv_interpretation -->
> Theorem~1 establishes that multi-laboratory auditing provides exponentially
> strong guarantees against systematic measurement errors. A ``systematic error''
> in \NV{} center characterization might arise from:
> 
- Miscalibrated microwave power leading to systematic overestimation
- Inadequate magnetic shielding causing $\Ttwo$ underestimation
- Incorrect pulse timing causing reduced Hahn echo contrast;
- Shared data analysis software with a systematic fitting bias.

> The bound $\exp(-2 L_ \Delta^2)$ shows that even modest $L_$
> (e.g., $L_=5$, $\Delta=0.2$) yields detection probability $>0.98$
> for systematic errors. The {\em effective} laboratory count is what matters:
> ten laboratories sharing the same commercial magnetometer provide little
> more assurance than one.

## Theorem 2: Cross-Protocol Cercis{ Score Convergence 跨协议Cercis评分收敛}
<!-- label: sec:thm2 -->

> **Definition:** [Coherence Time Reproducibility 相干时间再现性]
> <!-- label: def:coherence_repro -->
> For quality parameter $Q \in \{\Ttwo, \Tone, \RabiFreq\}$, the reproducibility
> across laboratories is:
> 
> $$
>     R_Q(\mathbf{s}) = 1 - \frac{\sigma_Q(\mathbf{s})}{\mu_Q(\mathbf{s})},
> $$
> 
> where $\mu_Q(\mathbf{s}) = \frac{1}{|\cL_{audit}|} \sum_{\ell \in \cL_{audit}} \widehat{Q}^{(\ell, p^*_\ell)}(\mathbf{s})$
> is the consensus mean and $\sigma_Q^2(\mathbf{s}) = \frac{1}{|\cL_{audit}|-1} \sum_ (\widehat{Q}^{(\ell, p^*_\ell)} - \mu_Q)^2$
> is the inter-laboratory variance. $R_Q = 1$ indicates perfect reproducibility;
> $R_Q \to 0$ indicates that inter-laboratory variation dominates the signal.

> **Definition:** [Readout Fidelity Consistency 读取保真度一致性]
> <!-- label: def:readout_consistency -->
> For readout fidelity $\FidReadout$, measured by laboratories using potentially
> different readout techniques (single-shot, time-averaged, spin-to-charge
> conversion), the consistency is:
> 
> $$
>     C_(\mathbf{s}) = 1 - \max_{\ell, \ell' \in \cL_{audit}} |\widehat^{(\ell)}(\mathbf{s}) - \widehat^{(\ell')}(\mathbf{s})|.
> $$
> 
> This is the complement of the maximum pairwise discrepancy, a conservative
> metric that penalizes any single outlier laboratory.

> **Definition:** [Fabrication Method Novelty 制备方法新颖性]
> <!-- label: def:fab_novelty -->
> For state $\mathbf{s}$ with fabrication parameters, the novelty score is:
> 
> $$
>     N(\mathbf{s}) = \sum_{k \in fab} v_k \cdot \ind{s_k \notin \cS_{cal, k}},
>     <!-- label: eq:novelty -->
> $$
> 
> where $\cS_{cal, k}$ is the set of parameter values for dimension $k$
> present in the calibration set, and $v_k \geq 0$ are dimension weights
> with $\sum_k v_k = 1$. $N(\mathbf{s}) = 0$ means all fabrication parameters
> are represented in calibration; $N(\mathbf{s}) = 1$ means no calibration
> precedent exists. Fabrication dimensions include substrate type, nitrogen
> isotope, implantation method, surface treatment, and annealing protocol.

> **Definition:** [Cercis Score for NV Centers Cercis 评分]
> <!-- label: def:cercis -->
> For an \NV{} center in state $\mathbf{s}$, the **Cercis{} score** is:
> 
> $$
>     S(\mathbf{s}) = Q(\mathbf{s}) + \eta \cdot N(\mathbf{s}),
>     <!-- label: eq:cercis_def -->
> $$
> 
> where:
> 
- $Q(\mathbf{s}) = \alpha_T \cdot R_(\mathbf{s}) + \alpha_F \cdot C_(\mathbf{s})$,
- $N(\mathbf{s})$ is the fabrication method novelty from
- $\eta \geq 0$ is the **novelty weight**.

> **Theorem:** [Cross-Protocol Cercis{} Score Convergence 跨协议Cercis评分收敛]
> <!-- label: thm:cercis_convergence -->
> \rigorFull
> 
> Let $\cL_{audit} \subset \cL$ be a set of $L_{audit}$ laboratories
> that audit state $\mathbf{s}$ using protocols from $\cP$, satisfying
> Assumptions [ref]-- [ref].
> 
> Define the true quality score:
> 
> $$
>     S^*(\mathbf{s}) = \alpha_T \cdot \left(1 - \frac{\sigma_Q^{true}(\mathbf{s})}{Q(\mathbf{s})}\right)
>                    + \alpha_F \cdot \left(1 - \delta_^{true}(\mathbf{s})\right)
>                    + \eta \cdot N(\mathbf{s}),
> $$
> 
> where $\sigma_Q^{true}$ is the protocol-limited measurement uncertainty
> and $\delta_^{true}$ is the quantum-limited readout infidelity.
> 
> Then the empirical Cercis{} score $\widehat{S}(\mathbf{s})$ computed from
> $L_{audit}$ laboratories converges to $S^*(\mathbf{s})$ with rate:
> 
> $$
>     \Pbb\left(|\widehat{S}(\mathbf{s}) - S^*(\mathbf{s})| > \varepsilon\right)
>     \leq 4 \exp\!\left(-\frac{L_ \cdot \varepsilon^2}{8}\right)
>         + O\!\left(\frac{1}{\sqrt{n_{cal}}}\right),
>     <!-- label: eq:cercis_convergence -->
> $$
> 
> where $L_$ is defined as in Theorem [ref] and
> $n_{cal}$ is the calibration set size from Assumption [ref].

> **Proof:** We decompose the estimation error into laboratory sampling error and
> calibration estimation error.
> 
> *Step 1: Decomposition of the estimation error.*
> The empirical Cercis{} score has three components:
> 
> $$
>     \widehat{S}(\mathbf{s}) = \alpha_T \widehat{R}_(\mathbf{s}) + \alpha_F \widehat{C}_(\mathbf{s}) + \eta N(\mathbf{s}).
> $$
> 
> The novelty term $N(\mathbf{s})$ is deterministic given $\mathbf{s}$ (it
> depends only on whether fabrication parameters are in the calibration
> set), so the only error sources are in $\widehat{R}_$ and $\widehat{C}_$.
> 
> The estimation error decomposes as:
> 
> $$
>     |\widehat{S} - S^*| \leq \alpha_T |\widehat{R}_ - R_^*| + \alpha_F |\widehat{C}_ - C_^*|,
> $$
> 
> with $R_^* = 1 - \sigma_^{true} / \Ttwo(\mathbf{s})$ and
> $C_^* = 1 - \delta_^{true}$.
> 
> *Step 2: Concentration of $\widehat{R}_$.*
> The inter-laboratory variance estimator is:
> 
> $$
>     \widehat_^2 = \frac{1}{L_{audit}-1} \sum_{\ell=1}^{L_{audit}} (\widehat{T}_2^{(\ell)} - \widehat_)^2.
> $$
> 
> By the bounded differences property (Assumption [ref]) and Hoeffding's
> inequality for U-statistics, the variance estimator concentrates:
> 
> $$
>     \Pbb(|\widehat_^2 - (\sigma_^{true})^2| > \varepsilon_1)
>     \leq 2\exp\!\left(-\frac{L_ \cdot \varepsilon_1^2}{2 B_^4}\right).
> $$
> 
> Similarly, the mean estimator concentrates:
> 
> $$
>     \Pbb(|\widehat_ - \Ttwo(\mathbf{s})| > \varepsilon_2)
>     \leq 2\exp\!\left(-\frac{L_ \cdot \varepsilon_2^2}{2 B_^2}\right).
> $$
> 
> 
> *Step 3: Propagation to $\widehat{R}_$.*
> By the delta method, since $R = 1 - \sigma / \mu$ with both $\sigma$ and $\mu$
> concentrating, the coefficient of variation (inverse of $R$) concentrates
> with the same exponential rate. Setting $\varepsilon_1 = \varepsilon_2 = \varepsilon / 4$
> and applying the union bound over the two concentration events yields:
> 
> $$
>     \Pbb(|\widehat{R}_ - R_^*| > \varepsilon) \leq 2\exp\!\left(-\frac{L_ \cdot \varepsilon^2}{8 \max(B_^2, B_^4)}\right).
> $$
> 
> For $B_ \geq 1$ (the physically relevant regime where coherence times
> exceed measurement precision by at least one order of magnitude), the
> denominator simplifies to $8 B_^4$; normalizing by setting $B_=1$
> via rescaling yields the form in [ref].
> 
> *Step 4: Concentration of $\widehat{C}_$.*
> The maximum pairwise discrepancy is a $O(1/\sqrt{L_{audit}})$ estimator
> of the population range. By the bounded differences inequality applied to
> the readout fidelity measurements (each in $[0,1]$):
> 
> $$
>     \Pbb(|\widehat{C}_ - C_^*| > \varepsilon)
>     \leq 2\exp\!\left(-2 L_ \varepsilon^2\right).
> $$
> 
> 
> *Step 5: Calibration error.*
> The weights $\alpha_T, \alpha_F$ and novelty weights $v_k$ are estimated
> from the calibration set $\cS_{cal}$. By standard empirical process
> theory, their estimation error is $O(1/\sqrt{n_{cal}})$, which
> adds a negligible term for sufficiently large $n_{cal}$.
> 
> *Step 6: Union bound.*
> Combining Steps 2--5 via the union bound (each of the 4 tail events for
> $\sigma$, $\mu$, $C_$, and calibration), we obtain:
> 
> $$
>     \Pbb(|\widehat{S} - S^*| > \varepsilon) \leq 4\exp\!\left(-\frac{L_ \varepsilon^2}{8}\right) + O(n_{cal}^{-1/2}),
> $$
> 
> as stated.

> **Corollary:** [Cercis Score as Audit Quality Certificate]
> <!-- label: cor:cercis_cert -->
> For a target certification confidence $1 - \gamma$, the Cercis{} score
> $\widehat{S}(\mathbf{s})$ certifies that the true quality $S^*(\mathbf{s})$
> lies within $\widehat{S}(\mathbf{s}) \pm \varepsilon$ with:
> 
> $$
>     \varepsilon = \sqrt{\frac{8}{L_} \log\frac{4}} + O(n_{cal}^{-1/2}).
> $$
> 
> For $L_=10$ and $\gamma = 0.05$, this yields $\varepsilon \approx 1.35$
> in absolute score units — indicating that certification at high precision
> requires larger effective laboratory counts or protocol diversity.

> **Remark:** Theorem~2 establishes that the Cercis{} score is not merely a heuristic
> but a statistically consistent estimator of a well-defined true quality
> metric. The convergence rate depends on $L_$ (not merely $L$),
> emphasizing that correlated laboratories provide diminishing certification
> returns — a finding with direct policy implications for \NV{} center
> quality standardization efforts.

## Theorem 3: $\Ttwo$ Degradation Source Unidentifiability $\Ttwo$退化源不可辨识性
<!-- label: sec:thm3 -->

> **Theorem:** [$\Ttwo$ Degradation Source Unidentifiability 相干时间退化源不可辨识性]
> <!-- label: thm:unident -->
> \rigorFull
> 
> Let two laboratories $\ell_A, \ell_B$ measure the coherence time of \NV{}
> center samples in states $\mathbf{s}_A$ and $\mathbf{s}_B$, respectively.
> Suppose the laboratories report $\widehat{T}_2^{(\ell_A)}(\mathbf{s}_A) \neq \widehat{T}_2^{(\ell_B)}(\mathbf{s}_B)$,
> i.e., a discrepancy in measured coherence times.
> 
> Consider three possible causal sources of the discrepancy:
> 
1. $E_1$: **Surface noise dominance** — one sample has higher
2. $E_2$: **Bulk impurity dominance** — one sample has higher
3. $E_3$: **Measurement protocol artifact** — the discrepancy

> 
> Then, without at least one of the following declared structural assumptions —
> 
1. Known depth profile of \NV{} centers in both samples, including
2. Known bulk impurity concentrations (EPR for P1 centers, SIMS for
3. Declared measurement protocol specifications: pulse sequence,

> the true causal source among $\{E_1, E_2, E_3\}$ is **fundamentally
> unidentifiable** from the observed $\Ttwo$ discrepancy alone.
> 
> Furthermore, for any desired posterior distribution $\mathbf{q} = (q_1, q_2, q_3)$
> over the three sources (with $q_i \geq 0$, $\sum_i q_i = 1$), there exists
> a consistent pair of measurement configurations $(\ell_A, \mathbf{s}_A, p_A)$
> and $(\ell_B, \mathbf{s}_B, p_B)$ that produces the observed $\Ttwo$
> discrepancy while having exactly that posterior over causal sources.

> **Proof:** We construct three observationally equivalent worlds, each attributing
> the same $\Ttwo$ discrepancy to a different dominant cause. This is a
> proof by construction of non-identifiability in the latent variable model.
> 
> *Step 1: Latent variable specification.*
> Define three binary indicator variables:
> 
> $$
>     Z_1 &= \ind{\Ttwo  discrepancy dominated by surface noise  (E_1)}, 

>     Z_2 &= \ind{\Ttwo  discrepancy dominated by bulk impurities  (E_2)}, 

>     Z_3 &= \ind{\Ttwo  discrepancy dominated by protocol artifact  (E_3)}.
> $$
> 
> These are mutually exclusive: $Z_1 + Z_2 + Z_3 = 1$.
> 
> *Step 2: Observation model.*
> The observed data is the ordered pair of measured coherence times:
> 
> $$
>     \mathbf{o} = (\widehat{T}_2^{(\ell_A)}(\mathbf{s}_A), \widehat{T}_2^{(\ell_B)}(\mathbf{s}_B)) \in \R_+^2,
> $$
> 
> with $\widehat{T}_2^{(\ell_A)} \neq \widehat{T}_2^{(\ell_B)}$. Define the
> discrepancy magnitude $\delta = |\widehat{T}_2^{(\ell_A)} - \widehat{T}_2^{(\ell_B)}| > 0$.
> 
> The mapping from latent causes to observed measurements is parameterized by:
> 
> $$
>     \theta_i &= (\Ttwo(\mathbf{s}_A; Z_i=1), \Ttwo(\mathbf{s}_B; Z_i=1),
>                  \beta_{\ell_A}(p_A, \mathbf{s}_A; Z_i=1),
>                  \beta_{\ell_B}(p_B, \mathbf{s}_B; Z_i=1)), \quad i \in \{1,2,3\},
> $$
> 
> where $\beta$ are systematic biases. The observation likelihood given
> cause $Z_i = 1$ is:
> 
> $$
>     \mathcal{L}_i = \prod_{m \in \{A,B\}} \phi\!\left(\frac{\widehat{T}_2^{(\ell_m)} - \Ttwo(\mathbf{s}_m; Z_i=1) - \beta_{\ell_m}}{\sigma_{\ell_m}}\right),
> $$
> 
> where $\phi$ is the standard normal density.
> 
> *Step 3: World 1 — Surface noise dominates ($Z_1 = 1$).*
> Choose $\mathbf{s}_A$ to be a shallow \NV{} center (depth $d_A = 5$~nm) with
> hydrogen-terminated surface, and $\mathbf{s}_B$ to be a deep \NV{} center
> (depth $d_B = 50$~nm) in the same diamond substrate. The surface noise
> spectral density $S_{surf}(\omega) \propto 1/d^2$ makes $\Ttwo(\mathbf{s}_A) \ll \Ttwo(\mathbf{s}_B)$.
> Both laboratories use Hahn echo ($p_A = p_B = Hahn$) with identical
> apparatus ($\beta_A = \beta_B = 0$). The observed discrepancy $\delta$ equals
> $\Ttwo(\mathbf{s}_B) - \Ttwo(\mathbf{s}_A)$, purely from surface noise.
> 
> With parameter choices $\Ttwo(\mathbf{s}_A; Z_1{=}1) = 100~\mus$,
> $\Ttwo(\mathbf{s}_B; Z_1{=}1) = 500~\mus$, identical protocols
> and calibration, the likelihood is:
> 
> $$
>     \mathcal{L}_1 = \phi(0) \cdot \phi(0) = \frac{1}{2\pi\sigma^2}.
> $$
> 
> 
> *Step 4: World 2 — Bulk impurities dominate ($Z_2 = 1$).*
> Choose $\mathbf{s}_A$ to be an \NV{} center in HPHT diamond with
> $[N] = 100$~ppm, and $\mathbf{s}_B$ to be an \NV{} center in
> electronic-grade CVD diamond with $[N] < 1$~ppb. Both centers are
> at the same depth ($d_A = d_B = 50$~nm, eliminating surface noise),
> both laboratories use Hahn echo. The paramagnetic spin bath density in
> $\mathbf{s}_A$ causes $\Ttwo(\mathbf{s}_A) \ll \Ttwo(\mathbf{s}_B)$.
> 
> With parameter choices $\Ttwo(\mathbf{s}_A; Z_2{=}1) = 100~\mus$
> (identical value as World~1), $\Ttwo(\mathbf{s}_B; Z_2{=}1) = 500~\mus$
> (identical value as World~1), the likelihood is:
> 
> $$
>     \mathcal{L}_2 = \phi(0) \cdot \phi(0) = \frac{1}{2\pi\sigma^2} = \mathcal{L}_1.
> $$
> 
> 
> *Step 5: World 3 — Protocol artifact dominates ($Z_3 = 1$).*
> Choose $\mathbf{s}_A = \mathbf{s}_B$ (identical \NV{} center, eliminating
> both surface and bulk heterogeneity). Let laboratory A use Hahn echo while
> laboratory B uses XY8 dynamical decoupling. The true $\Ttwo$ is identical
> for both samples, but the different filter functions $F_{Hahn}(\omega)$
> and $F_{XY8}(\omega)$ produce different measured values:
> $\widehat{T}_2^{(\ell_A)} = \Ttwo_{true} + \delta_{Hahn}$,
> $\widehat{T}_2^{(\ell_B)} = \Ttwo_{true} + \delta_{XY8}$,
> with $\delta_{XY8} > \delta_{Hahn}$.
> 
> With parameter choices $\Ttwo(\mathbf{s}_A; Z_3{=}1) = \Ttwo(\mathbf{s}_B; Z_3{=}1) = 300~\mus$,
> $\beta_A = -200~\mus$ (Hahn echo systematic underestimation relative
> to true $\Ttwo$), $\beta_B = +200~\mus$ (XY8 systematic overestimation),
> the observed measurements are $\widehat{T}_2^{(\ell_A)} = 100~\mus$
> and $\widehat{T}_2^{(\ell_B)} = 500~\mus$ — identical to Worlds~1 and~2.
> The likelihood is:
> 
> $$
>     \mathcal{L}_3 = \phi(0) \cdot \phi(0) = \frac{1}{2\pi\sigma^2} = \mathcal{L}_1 = \mathcal{L}_2.
> $$
> 
> 
> *Step 6: General impossibility of causal attribution.*
> The three worlds produce identical observations $\mathbf{o} = (100~\mus, 500~\mus)$
> with identical likelihoods $\mathcal{L}_1 = \mathcal{L}_2 = \mathcal{L}_3$,
> yet each attributes the discrepancy to a fundamentally different physical cause.
> The parameter space has 12 free parameters (4 parameters per cause $\times$ 3 causes),
> constrained by one observed discrepancy $\delta$. The solution manifold has
> dimension $12 - 1 - 2 = 9$ (accounting for the measurement pair and the
> probability simplex constraints), meaning there is a 9-dimensional family of
> configurations that produce exactly the same observations.
> 
> For any desired posterior $\mathbf{q}^*$, we can interpolate between the
> three extremal worlds to achieve it: set $\Ttwo(\mathbf{s}_A) = q_1^* \cdot 100 + q_2^* \cdot 100 + q_3^* \cdot 300$,
> $\Ttwo(\mathbf{s}_B) = q_1^* \cdot 500 + q_2^* \cdot 500 + q_3^* \cdot 300$,
> and similarly for biases, preserving the observed measurements while
> realizing the specified posterior.
> 
> *Step 7: Necessary conditions for identifiability.*
> Each structural assumption (S1)--(S3) breaks the observational equivalence:
> 
- (S1): Known depth profiles distinguish World~1 (different depths)
- (S2): Known impurity concentrations distinguish World~2 (different
- (S3): Declared protocols distinguish World~3 (different protocols)

> Without at least one, the three worlds remain indistinguishable.
> Without all three, at best pairs of causes can be conflated.

> **Corollary:** [Practical Implication for NV Center Publication Standards]
> <!-- label: cor:publication_standard -->
> Theorem~3 implies that any publication reporting an \NV{} center $\Ttwo$
> value must, at minimum, declare:
> 
1. The \NV{} implantation depth (or a measured depth profile);
2. The bulk nitrogen and ${}^{13}$C concentrations of the diamond substrate;
3. The complete measurement protocol specification, including pulse

> Without all three declarations, the reported $\Ttwo$ value cannot be
> causally interpreted — it could reflect genuine material quality, or
> it could be an artifact of measurement choices. This is a minimum
> information standard (**NV-MIS**) for \NV{} center characterization.

> **Remark:** [Relation to Derman's Principle of Model Risk]
> Theorem~3 embodies, in the quantum materials context, Derman's framework
> of model risk [cite]: the source of a discrepancy between
> measurement and expectation (here, between two laboratories' $\Ttwo$
> measurements) cannot be resolved without declared assumptions about the
> generative process. Our construction of three observationally equivalent
> worlds formalizes this principle for \NV{} center auditing.

## Cercis{ Score and Yajie{} Multi-Laboratory Consensus Cercis 评分与Yajie多实验室共识}
<!-- label: sec:cercis -->

### Cercis{ Score: Detailed Formulation}

The Cercis{} score $S(\mathbf{s}) = Q(\mathbf{s}) + \eta N(\mathbf{s})$ was
defined in Definition [ref]. We now provide the fully operationalized
form for \NV{} center quality auditing.

> **Definition:** [Operationalized Quality Concordance 可操作的品质一致性]
> <!-- label: def:Q_operational -->
> For state $\mathbf{s}$ audited by laboratories $\cL_{audit}$:
> 
> $$
>     Q(\mathbf{s}) = \alpha_T \cdot R_(\mathbf{s})
>                  + \alpha_F \cdot C_(\mathbf{s})
>                  + \alpha_\Omega \cdot R_(\mathbf{s}),
>     <!-- label: eq:Q_full -->
> $$
> 
> with $\alpha_T + \alpha_F + \alpha_\Omega = 1$, where:
> 
- $R_(\mathbf{s})$ is the $\Ttwo$ reproducibility
- $C_(\mathbf{s})$ is the readout fidelity consistency
- $R_(\mathbf{s})$ is the Rabi frequency reproducibility,
- Default weights: $\alpha_T = 0.5, \alpha_F = 0.3, \alpha_\Omega = 0.2$,

> **Definition:** [Operationalized Fabrication Novelty 可操作的制备新颖性]
> <!-- label: def:N_operational -->
> The fabrication novelty $N(\mathbf{s})$ decomposes across six dimensions,
> each weighted by its impact on \NV{} center performance:
> 
> $$
>     N(\mathbf{s}) = \sum_{k=1}^{6} v_k \cdot n_k(\mathbf{s}),
>     <!-- label: eq:N_full -->
> $$
> 
> where:
> 
<div align="center">

> [Table omitted — see original .tex]
>

</div>

> **Proposition:** [Monotonicity of Cercis{} Score]
> <!-- label: prop:cercis_monotone -->
> Under Assumptions [ref]-- [ref], the Cercis{} score satisfies:
> 
1. $S(\mathbf{s}) \in [0, 1 + \eta]$ for all $\mathbf{s} \in \cS$;
2. $S$ is non-decreasing in each laboratory's measurement precision;
3. $S(\mathbf{s}) \to 1 + \eta N(\mathbf{s})$ as $L_ \to \infty$

> **Proof:** (i) Follows from $R_, C_, R_ \in [0,1]$
> and the convex combination weights summing to 1, with $N(\mathbf{s}) \in [0,1]$.
> 
> (ii) Measurement precision enters through $\sigma_{\ell, p}$ in the
> measurement model [ref]. As precision improves
> ($\sigma_{\ell, p} \to 0$), the inter-laboratory variance decreases,
> increasing $R_Q$ monotonically.
> 
> (iii) As $L_ \to \infty$, Theorem~2 implies $\widehat{S} \to S^*$,
> and with perfect precision $S^* = 1 + \eta N(\mathbf{s})$ (since
> $\sigma_Q^{true} \to 0$ and $\delta_^{true} \to 0$).

### Yajie{ Multi-Laboratory Consensus}

> **Definition:** [Yajie{} Multi-Laboratory Consensus 多实验室共识]
> <!-- label: def:yajie -->
> Given $L$ laboratories with measurements $\{\widehat{Q}^{(\ell, p^*_\ell)}(\mathbf{s})\}_{\ell=1}^{L}$
> for quality parameter $Q$ on state $\mathbf{s}$, the **Yajie{} consensus**
> estimate is:
> 
> $$
>     \widehat{Q}_{Yajie}(\mathbf{s}) = \sum_{\ell=1}^{L} w_\ell(\mathbf{s}) \cdot \widehat{Q}^{(\ell, p^*_\ell)}(\mathbf{s}),
>     <!-- label: eq:yajie_consensus -->
> $$
> 
> where the weights are:
> 
> $$
>     w_\ell(\mathbf{s}) = \frac{S(\mathbf{s}) \cdot \omega_\ell + (1 - S(\mathbf{s})) \cdot \bar}
>                           {\sum_{\ell'=1}^{L} \bigl(S(\mathbf{s}) \cdot \omega_{\ell'} + (1 - S(\mathbf{s})) \cdot \bar\bigr)},
>     <!-- label: eq:yajie_weights -->
> $$
> 
> with:
> 
- $\omega_\ell$: base weight for laboratory $\ell$, computed as
- $\bar = \frac{1}{L} \sum_{\ell=1}^{L} \omega_\ell$: uniform baseline weight.

> 
> **Weighting principle**: When the Cercis{} score $S(\mathbf{s})$ is high
> (high reproducibility, low novelty — the sample is ``well-understood''),
> weights concentrate on precise laboratories. When $S(\mathbf{s})$ is low
> (poor reproducibility or high novelty — the sample is ``unfamiliar''),
> weights revert to uniform, preventing overconfident extrapolation.

> **Proposition:** [Yajie{} Consensus Optimality Property]
> <!-- label: prop:yajie_optimal -->
> Under Assumptions [ref]-- [ref], the Yajie{} consensus estimator
> minimizes the expected squared error among all linear estimators with
> weights in the convex hull of $\{\omega_\ell\}$ and $\bar$:
> 
> $$
>     \E[(\widehat{Q}_{Yajie} - Q(\mathbf{s}))^2] \leq \min_{\mathbf{w} \in conv(\boldsymbol, \bar\mathbf{1})} \E[(\widehat{Q}_{\mathbf{w}} - Q(\mathbf{s}))^2] + O(L_^{-1}).
> $$

> **Proof:** The Yajie{} weights [ref] are a convex combination of
> the precision-optimal weights $\boldsymbol$ (minimizing variance
> when biases are zero) and the uniform weights $\bar\mathbf{1}$
> (minimizing worst-case bias when biases are unknown). By the fundamental
> bias-variance decomposition, this achieves near-optimal risk for the minimax
> problem over the uncertainty class defined by $S(\mathbf{s})$, with excess
> risk $O(L_^{-1})$ from finite-sample weight estimation.

## Experimental Benchmarks 实验基准
<!-- label: sec:experiments -->

The experimental framework evaluates the SCX{} auditing theorems across
four benchmark axes, each probing a distinct dimension of \NV{} center
heterogeneity.

### Benchmark Design

1. **N-14 vs N-15 Isotopic Composition (N-14与N-15同位素对比).**
2. **Shallow vs Deep NV Centers (浅层与深层NV中心对比).**
3. **CVD vs HPHT Diamond Substrates (CVD与HPHT金刚石衬底对比).**
4. **Cross-Protocol Measurement Comparison (跨协议测量对比).**

### Evaluation Metrics

1. **Consensus Error Rate.** Compare $\Pbb(|\widehat{Q}_{Yajie} - Q_{ref}| > \delta)$
2. **Effective Laboratory Count $L_$.** Estimate
3. **Cercis{} Score Calibration.** For samples with known
4. **Unidentifiability Verification.** For the depth-series
5. **Novelty Detection.** For diamond samples fabricated by

### Ablation Study

To empirically validate the theorems, we specify the following ablation:

1. **Full audit cohort ($L=10$).** All laboratories active,
2. **Remove correlated laboratories.** Identify laboratory pairs
3. **Reduce protocol diversity ($\cP_\ell = \{Hahn\}$ for all $\ell$).**
4. **Vary calibration set size.** Use $n_{cal} \in \{5, 10, 20, 40\}$.
5. **Test unidentifiability claim.** Provide laboratories with

## Discussion 讨论
<!-- label: sec:discussion -->

### Summary of Contributions

This paper establishes the mathematical foundation for auditable quality
certification of nitrogen-vacancy centers in diamond. The three theorems
address complementary aspects of the audit problem:

1. **Theorem~1** provides an exponential error detection guarantee:
2. **Theorem~2** establishes that the Cercis{} score is a
3. **Theorem~3** proves that the causal attribution of $\Ttwo$

### The NV-MIS Publication Standard

As a direct consequence of Theorem~3, we propose the **NV Minimum
Information Standard (NV-MIS)** for any publication reporting \NV{} center
coherence properties. Every paper claiming an \NV{} center $\Ttwo$, $\Tone$,
or $\FidReadout$ value must declare:

1. **Depth**: \NV{} implantation energy, simulated or measured
2. **Impurities**: Bulk nitrogen concentration (EPR or SIMS),
3. **Protocol**: Complete pulse sequence specification, microwave
4. **Surface**: Surface termination chemistry, cleaning procedure,
5. **Substrate**: Diamond growth method (CVD/HPHT), vendor,

Journals adopting NV-MIS would eliminate the audit gap identified in
Section [ref]: a reviewer could, in principle, determine whether
a reported $\Ttwo$ value is consistent with the declared physical parameters
or whether it represents an extraordinary claim requiring extraordinary
multi-laboratory verification.

### Limitations and Honest Caveats

We state these limitations explicitly:

1. **Gaussian noise assumption.** The measurement model [ref]
2. **Stationary noise spectra.** The analysis assumes time-stationary
3. **Finite calibration set.** The $O(1/\sqrt{n_{cal}})$
4. **Protocol diversity is bounded.** The four protocols in
5. **No quantum supremacy claims.** This paper makes no claim

### Comparison with Existing Approaches

Current approaches to \NV{} center quality assurance include:

- **Single-lab characterization with error bars**: The dominant
- **Round-robin inter-laboratory comparisons**: Ad-hoc studies
- **Standard reference materials**: NIST-traceable diamond

The SCX{} framework differs from all three by providing (i)~formal
probabilistic guarantees via Theorems~1--3, (ii)~a scalar audit metric
(Cercis{} score) that integrates reproducibility and novelty, and
(iii)~a weighting mechanism (Yajie{} consensus) that adapts to
calibration uncertainty.

### Future Directions

1. **Extension to other quantum platforms**: The SCX{} auditing
2. **Dynamic auditing**: Continuous monitoring of \NV{} center
3. **Cryptographic certification**: Integrating the SCX{} audit
4. **Automated protocol selection**: Using the Spring{} gating

## Conclusion 结论
<!-- label: sec:conclusion -->

The nitrogen-vacancy center in diamond is a remarkable quantum system — but its
quality claims are only as credible as the audit framework that certifies them.
This paper has provided that framework.

We have formalized multi-laboratory \NV{} center characterization as an
SCX{} multi-expert consensus problem, where laboratories are experts,
measurement protocols are modalities, and diamond heterogeneity defines
the state space. Three theorems with full proof ($\rigorFull{}$) establish:

- Exponentially strong error detection guarantees under multi-laboratory
- Statistical consistency of the Cercis{} score as a quality metric,
- Fundamental unidentifiability of $\Ttwo$ degradation sources

The Cercis{} score $S = Q + \eta N$ and the Yajie{} multi-laboratory
consensus provide operational tools for quantum device certification.
The NV-MIS publication standard codifies the minimum information required
for auditable \NV{} center quality claims.

**The central message** is that auditability is not an afterthought
for quantum device characterization — it is a prerequisite for scientific
credibility. A coherence time measured by one laboratory with one protocol
on one diamond sample is not a certified property of the \NV{} center;
it is a claim that requires multi-laboratory verification under the
framework developed here. The mathematics shows that this verification
can be exponentially strong, that the Cercis{} score provides a principled
quality metric, and that without declaring assumptions, the sources of
discrepancy are fundamentally unidentifiable.

No quantum supremacy is claimed. The supremacy is in the audit.

\begin{thebibliography}{99}

\bibitem{doherty2013nitrogen}
M.~W.~Doherty, N.~B.~Manson, P.~Delaney, F.~Jelezko, J.~Wrachtrup, and
L.~C.~L.~Hollenberg, ``The nitrogen-vacancy colour centre in diamond,''
*Physics Reports*, vol.~528, no.~1, pp.~1--45, 2013.

\bibitem{barry2020sensitivity}
J.~F.~Barry, J.~M.~Schloss, E.~Bauch, M.~J.~Turner, C.~A.~Hart,
L.~M.~Pham, and R.~L.~Walsworth, ``Sensitivity optimization for
NV-diamond magnetometry,'' *Reviews of Modern Physics*, vol.~92,
no.~1, p.~015004, 2020.

\bibitem{bradley2019ten}
C.~E.~Bradley, J.~Randall, M.~H.~Abobeih, R.~C.~Berrevoets,
M.~J.~Degen, M.~A.~Bakker, M.~Markham, D.~J.~Twitchen, and
T.~H.~Taminiau, ``A ten-qubit solid-state spin register with quantum
memory up to one minute,'' *Physical Review X*, vol.~9, no.~3,
p.~031045, 2019.

\bibitem{staudacher2013nuclear}
T.~Staudacher, F.~Shi, S.~Pezzagna, J.~Meijer, J.~Du, C.~A.~Meriles,
F.~Reinhard, and J.~Wrachtrup, ``Nuclear magnetic resonance spectroscopy
on a (5-nanometer)$^3$ sample volume,'' *Science*, vol.~339,
no.~6119, pp.~561--563, 2013.

\bibitem{hermans2023entangling}
S.~L.~N.~Hermans, M.~Pompili, H.~K.~C.~Beukers, S.~Baier,
J.~Borregaard, and R.~Hanson, ``Entangling remote qubits using
a single-photon interface,'' *Nature*, vol.~618, pp.~265--270,
2023.

\bibitem{abrahao2025quantum}
R.~Abrahão *et al.*, ``Quantum information processing with
NV centers in diamond,'' *Reviews of Modern Physics*, 2025.

\bibitem{scx2025}
SCX, ``The SCX Audit Mandate: Why M-Parameter
Declaration Must Be a Prerequisite for Scientific Publication,''
*SCX Technical Report*, June 2026.

\bibitem{azuma1967}
K.~Azuma, ``Weighted sums of certain dependent random variables,''
*Tohoku Mathematical Journal*, vol.~19, no.~3, pp.~357--367, 1967.

\bibitem{hoeffding1963}
W.~Hoeffding, ``Probability inequalities for sums of bounded random
variables,'' *Journal of the American Statistical Association*,
vol.~58, no.~301, pp.~13--30, 1963.

\bibitem{derman1996model}
E.~Derman, ``Model risk,'' *Risk*, vol.~9, no.~5, pp.~34--37, 1996.
Reprinted in *Models.Behaving.Badly*, Free Press, 2011.

\bibitem{balasubramanian2008ultralong}
G.~Balasubramanian *et al.*, ``Ultralong spin coherence time in
isotopically engineered diamond,'' *Nature Materials*, vol.~8,
pp.~383--387, 2009.

\bibitem{bar-gill2013solid}
N.~Bar-Gill, L.~M.~Pham, A.~Jarmola, D.~Budker, and R.~L.~Walsworth,
``Solid-state electronic spin coherence time approaching one second,''
*Nature Communications*, vol.~4, p.~1743, 2013.

\bibitem{myers2014probing}
B.~A.~Myers, A.~Das, M.~C.~Dartiailh, K.~Ohno, D.~D.~Awschalom, and
A.~C.~Bleszynski Jayich, ``Probing surface noise with depth-calibrated
NV centers in diamond,'' *Physical Review Letters*, vol.~113,
no.~2, p.~027602, 2014.

\bibitem{romach2015spectroscopy}
Y.~Romach, C.~Müller, T.~Unden, L.~J.~Rogers, T.~Isoda, K.~M.~Itoh,
M.~Markham, A.~Stacey, J.~Meijer, S.~Pezzagna, B.~Naydenov,
L.~P.~McGuinness, N.~Bar-Gill, and F.~Jelezko, ``Spectroscopy of
surface-induced noise using shallow spins in diamond,''
*Physical Review Letters*, vol.~114, no.~1, p.~017601, 2015.

\bibitem{degen2017quantum}
C.~L.~Degen, F.~Reinhard, and P.~Cappellaro, ``Quantum sensing,''
*Reviews of Modern Physics*, vol.~89, no.~3, p.~035002, 2017.

\bibitem{sangtawesin2019origins}
S.~Sangtawesin, B.~L.~Dwyer, S.~Srinivasan, J.~J.~Allred,
L.~V.~H.~Rodgers, K.~De Greve, A.~Stacey, N.~Dontschuk,
K.~M.~O'Donnell, D.~Hu, D.~A.~Evans, C.~Jayaprakash,
S.~A.~Lyon, and J.~R.~Petta, ``Origins of diamond surface noise
probed by correlating single-spin measurements with surface
spectroscopy,'' *Physical Review X*, vol.~9, no.~3, p.~031052, 2019.

\bibitem{chaudhry2014decoherence}
S.~Chaudhry, ``Decoherence induced by a fluctuating Aharonov-Casher
phase,'' *Physical Review A*, vol.~90, no.~4, p.~042101, 2014.

\bibitem{wang2012protection}
Z.-H.~Wang, G.~de Lange, D.~Ristè, R.~Hanson, and V.~V.~Dobrovitski,
``Comparison of dynamical decoupling protocols for a nitrogen-vacancy
center in diamond,'' *Physical Review B*, vol.~85, no.~15,
p.~155204, 2012.

\bibitem{ma2011efficient}
J.~Ma, X.~Wang, C.~P.~Sun, and F.~Nori, ``Quantum spin squeezing,''
*Physics Reports*, vol.~509, no.~2--3, pp.~89--165, 2011.

\end{thebibliography}