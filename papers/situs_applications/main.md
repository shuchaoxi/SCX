<div align="center">

**Document Type**: Perspective / Position Paper (no new experiments)

**Target Journals**: *Nature Computational Science* or *Scientific Data*
**Status Legend**:
\;$\blacksquare$ Verified (mathematical proof or physical data)
\;$\blacksquare$ Projected (theoretically grounded, unverified)
\;$\blacksquare$ Known hard boundary / failure mode

</div>

*Abstract:*

The SCX (State-Conditioned eXpertise) framework deploys multiple independent expert models to detect label noise through consensus patterns, but its original formulation is spatially blind—it treats all data samples as points in a purely statistical feature space. The two-layer state discovery procedure that enables this deployment—domain-knowledge features (Layer~1) followed by error-driven encoding (Layer~2)—is established in the SCX theoretical framework [cite]. Situs, a family of physical positional encodings, augments SCX by injecting geometric information (1D sequence position, 3D Cartesian coordinates, 4D spatiotemporal grids) into state representations. This Perspective maps the boundary between Situs as a decisive asset and Situs as costly noise across **twelve scientific scenarios** spanning six domain groups. We designate **genomics variant auditing** as the flagship verification field: three sequencing platforms cross four variant callers produce a natural $3 \times 4$ expert matrix at base-pair precision—Situs's most exact positional encoding—and rare-variant-versus-sequencing-error maps directly onto Theorem~3's detection boundary. We also cover Materials Science (AlN defects; CNT chirality as a pedagogical proof-of-concept), Life Sciences (drug-target docking), Earth \& Environment (remote sensing, climate modeling, seismology), Astronomy, Engineering Simulation (semiconductor manufacturing—wafer TCAD and OPC lithography, multi-solver mesh auditing), and Medical Imaging. One scenario—enzyme active sites (1D sequence position cannot proxy 3D functional site; no natural multi-expert exists)—is explicitly excluded as a failure mode of the framework's preconditions. Oceanography is conditionally included: the North Atlantic and North Pacific have sufficient Argo float density and satellite altimetry coverage for multi-platform comparison, but the deep ocean interior and Southern Ocean remain infeasible due to extreme spatio-temporal sparsity. We establish the necessary condition $I(Y;P \mid S)>0$—physical position must carry label information beyond what the state atom already captures—and audit every scenario against it, including three hard failure modes: spurious correlation, multicollinearity with pre-existing structural encodings, and rotational equivariance failure. We close with a layered deployment roadmap (Core $\to$ Spatial $\to$ Extended) and a call for adversarial validation before claiming spatial gains. All $\delta_s^{\mathrm{PE}}$ estimates for the projected scenarios are physically reasoned, not experimentally verified.

## SCX + Situs in One Picture

The SCX ecosystem comprises five co-designed layers. Figure [ref] (described textually here; a graphical version is under preparation) maps the value chain from raw physical observation to audited data quality score.

- ****Layer 1 — State Crystallization**.:** Raw physical observables $\mathcal{X} \subset \mathbb{R}^{d_{raw}}$ (DFT energy surfaces, force fields, spectral time series, sequencing reads) are discretized into $N$ state atoms $\mathcal{S} = \{s_1,...,s_N\}$ via curvature-driven clustering on PBE energy landscapes. Unlike statistical tokenization (BPE), crystallization is physics-grounded: cluster boundaries align with spectral gaps in $\nabla^2 E_{PBE}$. $\blacksquare$ Verified: Crystallization is operational on AlN defect structures ($N = 534$ frames, 107 unique geometries). $\blacksquare$ Projected: Extension to non-DFT data types (spectroscopic, genomic, remote sensing) requires domain-specific crystallization criteria.
- ****Layer 2 — Situs (Physical Positional Encoding)**.:** Each state atom $s_i$ is augmented with its physical location $p_i$ via additive injection:
- ****Layer 3 — Spring (Self-Evolution)**.:** A monotonically growing memory bank $M_t$ accumulates every structural assessment. Dormant structures are periodically re-evaluated as the gatekeeper's discrimination improves. $\blacksquare$ Verified: Robbins-Monro convergence (SE-1) and Doob martingale property (SE-2) under convexity assumptions.
- ****Layer 4 — Yajie (Multi-Expert Audit)**.:** $M$ independent experts vote on label correctness. The consistency count $C(s) = \sum_{m=1}^{M} \mathbf{1}[E_m(s) \neq y]$ follows a binomial mixture under null (clean) and alternative (noisy) hypotheses. Detection margin $\Delta_s = p_{noisy,s} - p_{clean,s} > 0$ is the condition for operational utility. $\blacksquare$ Verified: Theorem~1 (Chernoff-Hoeffding lower bound on $F_1$), Theorem~4 (minimax optimality via Chernoff-Stein lemma).
- ****Layer 5 — Cercis Score**.:** The final quality score combines base quality from multi-expert consensus with a time-decaying novelty bonus. $\blacksquare$ Verified: Integration with Spring's dormancy-resurrection cycle.

The critical question this paper addresses is **where** in this pipeline Situs adds value---and where it subtracts it. Not all data has meaningful spatial structure. Not all spatial structure is causally linked to the prediction target. And not all encoding schemes respect the symmetries of the underlying physics. The rest of this paper provides a decision framework evaluated against twelve scientific scenarios, plus two explicitly excluded failure modes where the framework's preconditions cannot be met.

## When to Add Situs: The Decision Criterion

### The Necessary Condition

The central theoretical result governing Situs deployment is:

> **Theorem:** [Information-Theoretic Criterion, Theorem~2.2.1 in  [cite]]
> <!-- label: thm:criterion -->
> Let $S$, $P$, $Y$ denote the state atom, physical position, and label random variables. A necessary (and, with sufficient encoding capacity, sufficient) condition for Situs to improve detection margin $\Delta_s$ is:
> 
> $$
> \boxed{I(Y; P \mid S) > 0}
> <!-- label: eq:criterion -->
> $$
> 
> That is, physical position must carry information about the label *beyond what the state atom already encodes*. When $I(Y;P \mid S) = 0$, Situs contributes nothing beyond finite-expert variance noise: $\delta_s^{\mathrm{PE}} \leq O(1/\sqrt{M}) \to 0$ as $M \to \infty$.

The condition is clean, but its practical estimation is not. Computing $I(Y;P \mid S)$ via KSG estimators suffers from the curse of dimensionality. The pragmatic alternative is a **predictive sufficiency test**: train two classifiers, one on $(\phi(S), \mathrm{PE}(P))$ and one on $\phi(S)$ alone; if their out-of-distribution log-loss difference is not statistically significant, Situs is redundant.

### Fourteen-Scenario Quick-Reference Table

Table [ref] provides the deployment decision for twelve canonical scientific scenarios organized into six domain groups, with genomics designated as the flagship verification field. One scenario (enzyme active sites) is explicitly excluded in \S [ref] as a failure mode where the framework's preconditions cannot be met. Oceanography is conditionally included (\S [ref]): feasible in well-sampled regions, infeasible in the deep ocean interior.

[Table omitted — see original .tex]

### Quick Heuristic

> **The Situs litmus test**: Can you name a specific physical mechanism by which position *causes* the label to change, holding the local state fixed? If yes, Situs is likely beneficial. If no, it is likely noise. If you are unsure, run the predictive sufficiency test before deploying.

## Materials Science: Situs on Home Turf
<!-- label: sec:materials -->

Materials science is Situs's home turf because 3D atomic coordinates *causally determine* formation energies, elastic properties, and electronic structure. We present one verified application scenario (AlN defects) and one pedagogical proof-of-concept (CNT chirality) that validates the encoding machinery in a theoretically clean limit.

### AlN $V_N$ Defect: Causal 3D Position Encoding

The nitrogen vacancy $V_N$ in aluminum nitride is the archetypal case where 3D position *causes* the label. The same chemical defect at different spatial locations (bulk, surface, grain boundary) has formation energies spanning 1.0--4.0~eV (Table [ref]). The causal chain is irreducible: 3D position $\to$ local coordination $\to$ defect formation energy. Using Fano's lower bound with $I(Y;P \mid S) \approx 1.6$ bits, $\delta_s^{\mathrm{PE}} \gtrsim 0.5--0.8$---a substantial detection margin gain. $\blacksquare$ Caveat (unverified): The 534-frame dataset may contain multiple grain orientations. If orientations span more than $\sim 15^\circ$, rotational non-equivariance (\S [ref]) injects orientation-dependent noise.

[Table omitted — see original .tex]

### CNT Chirality Classification: A Pedagogical Proof-of-Concept

$\blacksquare$ Teaching example — not a real-world application scenario.

Carbon nanotube chirality $(n,m)$ is determined entirely by global 3D atomic arrangement. All carbon atoms share identical $sp^2$ chemistry, so $I(Y; S) \approx 0$ and $I(Y; P) \approx H(Y)$---Situs is the **only** source of discriminative information. This makes CNT chirality a theoretically perfect case for Situs: the encoding machinery can be validated in a setting where the state atom carries zero label information and position carries all of it. The sinusoidal encoding captures helical wrapping periodicity through $\langle \mathrm{PE}(\mathbf{p}), \mathrm{PE}(\mathbf{q}) \rangle = \cos(\alpha\Delta x) + \cos(\beta\Delta y) + \cos(\gamma\Delta z)$.

**Why this is a proof-of-concept, not an application.** In any real material, the state atom $S$ *does* carry label information---the whole point of SCX is that $I(Y;S) > 0$ and Situs contributes the residual $I(Y;P \mid S)$. CNT chirality is the degenerate limit $I(Y;S) = 0$, which makes it a clean validation of the encoding's ability to capture geometric periodicity, but tells us nothing about how Situs performs when state and position compete or complement. It is a unit test for the encoding layer, not an integration test for the full SCX+Situs pipeline. For small-diameter tubes ($n+m < 15$), curvature effects break the encoding's implicit assumption of planar periodicity, providing a controlled probe of the encoding's geometric assumptions.

## Life Sciences: Conditional Applicability
<!-- label: sec:lifesci -->

Life sciences applications present a narrow window for Situs: the theoretical condition $I(Y;P \mid S) > 0$ is often satisfied in 3D structural biology, but data volume, pose quality, and pre-existing structural encodings severely constrain practical deployment. Genomics---by far the strongest life-sciences fit for SCX+Situs---is promoted to its own flagship section (\S [ref]). Enzyme active sites are explicitly excluded (\S [ref]) because 1D sequence position cannot proxy 3D functional site and no natural multi-expert structure exists.

### Drug-Target Docking: Conditional Applicability

Binding affinity is a function of 3D pose geometry, making $I(Y; P_{3D} \mid S) > 0$ theoretically satisfied. However, three constraints apply: (1) DrugBank's 6,784 entries is undersized for learning the vast pose--affinity mapping in high-dimensional encoding space; (2) only poses with RMSD $< 2.0$\,\AA\ carry reliable position--affinity signal; (3) molecular scaffold (captured in $\phi(s_i)$) partially determines affinity, reducing the incremental value of spatial encoding. $\blacksquare$ Projected: Deploy 3D Situs on the high-quality subset with reduced encoding dimensionality ($d_{pe} \leq 32$) and $L_2$ regularization.

## Genomics: The Flagship Verification Field for SCX+Situs
<!-- label: sec:genomics -->

$\blacksquare$ Projected — physically reasoned, not experimentally verified.

We designate genomics variant auditing as the **flagship verification field** for the SCX+Situs framework. No other scientific domain combines (i) a natural, richly structured multi-expert matrix, (ii) Situs's most precise positional encoding operating at its theoretical limit, and (iii) an audit problem that maps exactly onto the mathematical structure of Theorem~3. If SCX+Situs cannot demonstrate value here, it cannot demonstrate value anywhere.

### The $3 \times 4$ Natural Expert Matrix

Genomics offers an exceptionally clean multi-expert structure: three sequencing platforms crossed with four variant calling algorithms produce a nominal $3 \times 4$ grid, but the **honest effective expert count is $M_{eff} \in [3,6]$**: the three platforms probe DNA through fundamentally different measurement physics (sequencing-by-synthesis, zero-mode waveguide, ionic current blockade), giving platform-level $M_{eff}^{plat} \approx 3$; the four variant callers share substantial algorithmic DNA (Smith-Waterman realignment, base quality score recalibration), reducing algorithm-level $M_{eff}^{alg} \approx 2$ (DeepVariant is the only architecturally distinct caller). All platforms and callers share the same reference genome alignment---the common blindfold. The platforms---Illumina (short-read, high base accuracy), PacBio (long-read, systematic indel errors), and Oxford Nanopore (ultra-long-read, higher raw error rate)---probe the same physical DNA molecule through fundamentally different measurement principles. The variant callers---GATK [cite] (Bayesian likelihood-based), DeepVariant [cite] (deep convolutional neural network), FreeBayes [cite] (haplotype-based Bayesian), and Strelka [cite] (mixed Poisson model)---apply different statistical models to the same read alignments. This is not a manufactured ensemble: the community already runs all four callers on all three platform outputs and struggles to reconcile the disagreements. SCX+Situs provides the theoretical framework for doing so systematically.

### Base-Pair Precision: Situs at Its Theoretical Limit

Situs encodes 1D genomic position at single-nucleotide resolution along a reference genome. This is the framework's most precise positional encoding: the coordinate $p \in \{1, 2, ..., 3.2 \times 10^9\}$ (for human) is an exact integer with zero interpolation error---there is no ``between grid points'' in genomics. The sinusoidal encoding's frequency spectrum can be tuned to capture biologically relevant length scales: single-nucleotide ($\lambda = 1$\,bp), codon periodicity ($\lambda = 3$\,bp), exon-scale ($\lambda \sim 10^2$--$10^3$\,bp), and topologically associating domain scale ($\lambda \sim 10^5$--$10^6$\,bp). No other scenario in this survey achieves positional precision within $10^{-10}$ of the coordinate range.

### Theorem~3 Exact Instance: Rare Variant vs.\ Sequencing Error

The core auditing problem---distinguishing a genuine rare variant (allele frequency $< 1\%$) from a sequencing artifact---is an **exact instance of Theorem~3** (simulation error vs.\ real process variation indistinguishability). A single variant caller operating on a single platform's reads cannot distinguish between: (i) a true single-nucleotide variant present in the DNA molecule but absent from the reference, and (ii) a systematic sequencing error (e.g., Oxford Nanopore homopolymer miscall, PacBio circular consensus collapse) that produces the same base-call pattern. The key insight is that these two cases have *different multi-expert signatures at the same genomic position $p$*: a true variant appears across all platforms (with platform-appropriate error profiles), while a platform-specific artifact appears only in that platform's calls. The detection margin $\Delta_s(p)$ at position $p$ quantifies the consensus strength: high when the effective expert panel converges (most platform--caller combinations agree, bearing in mind $M_{eff} \in [3,6]$ not 12), near zero when only a single platform--caller pair reports the variant.

### Additional Audit Targets

Three structurally distinct audit problems leverage position in different ways:

- ****Somatic vs.\ germline confusion** [cite].:** Same genomic position $p$, same variant allele, but different tissue-of-origin labels: a somatic mutation (cancer tissue only) vs.\ a germline variant (all tissues). The state atom $S$ (read pileup at $p$) is nearly identical; the label difference is carried entirely by $Y$---and the audit task is detecting when a somatic call is actually a germline variant that was missed in the matched normal sample. Cross-platform agreement at $p$ in the tumor sample but disagreement with the normal sample is the signature.
- ****Structural variant breakpoint discordance**.:** Structural variants (deletions, duplications, inversions, translocations) have breakpoints---genomic positions where the reference sequence is disrupted. Different platforms assign different breakpoint coordinates to the same physical rearrangement due to read-length effects (short reads cannot span large variants, long reads have lower base precision at the breakpoint). The same physical locus receives different $P$ assignments from different platforms---a position-disagreement pattern that is itself the audit signal.
- ****Pseudogene discrimination**.:** A pseudogene and its functional paralog share identical (or near-identical) sequence chemistry $S$ but reside at different genomic positions $P$. A short read originating from the pseudogene may align equally well to the functional gene's locus---a mapping ambiguity that position-indexed multi-expert auditing can flag: if PacBio long reads (which span both the variant and its genomic context) assign the variant to $p_{pseudo}$ while Illumina short reads assign it to $p_{func}$, the disagreement localizes the mapping ambiguity.

### Caveats: What Keeps This Honest

$\blacksquare$ **Reference genome bias — the shared-blindness problem.** All platforms align reads to the same reference genome. All variant callers use the same alignment files as input. If the reference genome has a deletion allele at a polymorphic locus, every platform's reads from a non-reference-allele carrier will align poorly at that position, and every variant caller will either miss the variant or call it with low confidence. The consensus silence is not independent agreement---it is shared blindness. This is the single most dangerous failure mode because it produces the highest possible apparent consensus at exactly the positions where the true label is most uncertain.

$\blacksquare$ **Variant caller shared heuristics.** GATK, FreeBayes, and Strelka all use Smith-Waterman realignment and base quality score recalibration---shared algorithmic components that correlate errors. DeepVariant's deep learning approach is architecturally distinct, but it trains on labels generated by the other callers in a bootstrap that partially transfers their error modes. Expert independence is approximate at best.

$\blacksquare$ **GC-rich and repetitive regions.** The most clinically important variants (e.g., *BRCA1*, *HTT* CAG repeats, *FMR1* CGG repeats) fall in precisely the genomic contexts where all platforms degrade simultaneously. Situs will be most confident where it is least needed (unique, mappable regions) and least confident where it is most needed (medically relevant repetitive regions)---an anti-Matthew effect built into the genome itself.

## Earth \& Environment: Native Spatiotemporal Domains
<!-- label: sec:earth -->

Earth and environmental sciences are where Situs's spatial encoding meets its most natural expression: every observation carries geographic coordinates, and the primary scientific questions are inherently spatial. Three scenarios span the solid Earth, atmosphere, and land surface. Oceanography is conditionally included (\S [ref]): feasible for the North Atlantic and North Pacific where Argo density exceeds 10 profiles per $1^\circ \times 1^\circ$ grid cell per decade and satellite altimetry provides independent surface constraints; infeasible for the deep ocean interior and Southern Ocean where spatio-temporal sparsity makes physically meaningful multi-platform comparison impossible.

### Remote Sensing: Pixel-Level Precision

Earth observation from space presents a structurally ideal Situs scenario. Landsat (30\,m), Sentinel-2 (10\,m), MODIS (250--500\,m daily), and NAIP (1\,m) observe the same $(lat,lon)$ at different spatial, spectral, and temporal resolutions—each sensor is a natural expert. Cross-sensor disagreement at fixed position flags either temporal change (valid physics), resolution mismatch (valid uncertainty), or classification error (Yajie audit target). Training label transfer across sensors is position-localized: an erroneous crop-type label at $(lat,lon)$ propagates to all co-registered pixels. $\blacksquare$ Projected (no implementation): The community's extensive spatial data infrastructure (Google Earth Engine, STAC) makes this a low-friction deployment pathway, but the chicken-and-egg problem of needing verified labels to train per-sensor experts remains.

### Climate Modeling: CMIP6 Multi-Model Auditing

$\blacksquare$ Projected — physically reasoned, not experimentally verified.
The Coupled Model Intercomparison Project Phase 6 (CMIP6 [cite]) ensemble is a **naturally occurring multi-expert system**: dozens of climate models developed independently by modeling centers worldwide produce projections for the same physical Earth at identical $(lat,lon,altitude,time)$ coordinates. Situs operates in 4D spatiotemporal encoding—three spatial dimensions plus time—making it the highest-dimensional Situs deployment considered here. The core auditing problem is distinguishing forced response (physically determined by boundary conditions, label-clean) from model structural error (parameterization choices, label-noise). Inter-model agreement at each 4D grid cell serves as a spatialized consistency score; cells with persistent multi-model divergence flag regions where the label ``model consensus'' itself is unreliable. Extreme event prediction divergence (e.g., tropical cyclone intensification, heatwave amplitude) is a prime audit target because the position--label causal link is strongest where physics is most nonlinear. $\blacksquare$ Critical caveat: CMIP6 models are not independent—they share component code, parameterization schemes, and even entire atmospheric modules. Model genealogy [cite] creates correlated errors that inflate apparent consensus, the single most dangerous failure mode for multi-expert auditing in climate science.

### Seismology: Earth Interior Multi-Network Auditing

$\blacksquare$ Projected — physically reasoned, not experimentally verified.
Seismology deploys multiple observational networks (global broadband, regional dense arrays, ocean-bottom seismometers) feeding multiple inversion methodologies (travel-time tomography, full-waveform inversion [cite], ambient noise correlation) to infer Earth's 3D interior structure. Situs encodes $(lat,lon,depth)$ in the 3D rotational encoding scheme—depth plays the role of the $z$-axis with seismic velocity discontinuities (Moho, 410, 660 [cite]) providing natural frequency anchors. The natural multi-expert structure arises because each inversion method uses different portions of the seismogram and makes different assumptions about anelastic attenuation, source--receiver geometry, and crustal corrections. Focal mechanism solution discordance [cite]—where the same earthquake receives different fault-plane solutions from different networks—and tomography model inconsistency at the same $(lat,lon,depth)$ are the primary audit targets. $\blacksquare$ Caveat: Seismic ray coverage is highly heterogeneous (dense in Japan and California, sparse in oceans and polar regions), meaning $I(Y;P \mid S)$ varies dramatically with geographic location—Situs is most informative precisely where coverage is richest, a reverse-Matthew effect.

## Astronomy: Yajie's Natural Habitat
<!-- label: sec:astronomy -->

Multi-telescope surveys (SDSS optical + Gaia astrometry + JWST infrared + LSST time-domain) create precisely the scenario where Yajie's multi-expert architecture is naturally deployed: each telescope/instrument is a **natural expert**, independently observing the same astrophysical objects through different physical channels. Celestial coordinates $(RA, Dec, z)$ serve as both the universal join key across surveys and the causal variable: the same physical object at the same sky position produces different observed properties through different instruments. Cross-survey label auditing flags sources whose classification disagrees across instruments (SDSS quasar vs Gaia extended source vs JWST mid-IR excess—possible dust-obscured AGN). Photometric redshift calibration detects when a galaxy at $(RA,Dec,z_{spec})$ is inconsistent with its photometric neighbors. Transient host-environment discrimination exploits the fact that $I(Y;P \mid S) > 0$ because the same light curve can correspond to a Type Ia SN in an elliptical host or a core-collapse SN in a star-forming disk. $\blacksquare$ Projected (no implementation): A proof-of-concept on SDSS $\times$ Gaia cross-matched quasars ($\sim 10^5$ sources, public data) would provide the first empirical validation.

## Engineering Simulation
<!-- label: sec:engineering -->

Engineering simulation encompasses two structurally analogous sub-domains: semiconductor manufacturing (where multiple TCAD and OPC engines simulate the same wafer-level physical processes) and computational mechanics (where multiple FEA/CFD solvers solve the same governing equations on the same geometry). Both share the same core Situs architecture—$(x,y,z)$ coordinates on an engineered structure—and the same fundamental challenge: distinguishing simulation artifact from physical reality. **Honest prefatory note**: In both sub-domains, the ``experts'' are not independent in any formal sense—they discretize the same governing equations using related numerical methods and share underlying physical models. The expert correlation structurally violates Theorem~1's independence assumption. This does not make the audit useless, but it means the effective expert count $M_{eff}$ is substantially below the nominal count, and the Chernoff bound on detection margin is looser than the theory would suggest for truly independent experts. We flag this honestly rather than hand-waving it away.

### Semiconductor Manufacturing: Wafer Process and Optical Proximity Correction

$\blacksquare$ Projected — physically reasoned, not experimentally verified.

Semiconductor manufacturing presents two structurally analogous Situs deployments at different stages of the fabrication pipeline. **Both share the same fundamental honesty problem**: the ``experts'' (TCAD simulators, OPC engines) are commercial tools that implement the same underlying physics—drift-diffusion equations, Hopkins imaging theory, thin-mask approximation—with different numerical discretizations and calibration strategies. Their disagreement is bounded by discretization difference, not by independent physical measurement. This is not multi-expert auditing in the sense of Theorem~1; it is sensitivity analysis across numerical implementations of the same model.

#### Wafer Process Simulation (TCAD)

Semiconductor process simulation (TCAD [cite]) deploys different process simulators (Synopsys Sentaurus vs Silvaco Victory Process) that produce divergent doping profiles from identical process recipes due to different discretization schemes, diffusion models, and numerical solvers. Situs encodes wafer surface $(x,y)$ coordinates plus depth $z$, capturing the 3D spatial structure of the device. The core audit problem is distinguishing genuine process-induced doping variation (label-relevant) from grid-dependent numerical artifact (label noise). $\blacksquare$ Honest assessment: This is structurally the weakest expert-independence scenario in the survey. Sentaurus and Victory Process solve the **same** coupled diffusion equations with the **same** implantation tables and the **same** mobility models. Their disagreement reflects mesh discretization differences and solver convergence criteria—not genuinely independent physical measurement. Effective $M_{eff}$ is closer to 1.2 than to 2. The scenario is included not because it is a strong Situs case, but because it is an industrially relevant weak case where even marginal $\delta_s^{\mathrm{PE}}$ gains translate to economic value through reduced metrology cost.

#### Optical Proximity Correction (OPC) Lithography

$\blacksquare$ Projected — physically reasoned, not experimentally verified.

Optical proximity correction (OPC) pre-distorts photomask patterns to compensate for optical diffraction and resist effects during wafer exposure. Three commercial OPC engines—Mentor Calibre OPC, Synopsys Proteus, and ASML Tachyon—compute mask corrections from the same target design layout. Situs encodes wafer surface coordinates $(x,y)$ at nanometer-scale precision ($<1$\,nm).

The core auditing problem maps to Theorem~3: when two OPC engines predict different printed contours at the same $(x,y)$, the divergence could reflect genuine lithographic defect modes (label-relevant) or optical model calibration differences (label noise). Yajie multi-engine consistency audit localizes hotspots and prioritizes CD-SEM metrology on maximally divergent regions—shrinking verification from full-wafer impossible to hotspot-targeted affordable.

$\blacksquare$ Honest assessment: OPC engines **share fundamental optical models**—Hopkins imaging theory, thin-mask (Kirchhoff) approximation, and resist chemistry parameterizations (Dill ABC model). All three engines can agree on an incorrect contour because they inherit the same thin-mask approximation error at a given feature. This is shared-model redundancy, not multi-expert independence. **Effective $M_{eff} \approx 1.2$**: three nominal engines collapse to near-one effective expert because the shared Hopkins + thin-mask + Dill backbone dominates all outputs; the ``disagreement'' is discretization noise, not genuinely independent physical measurement. The $<1$\,nm encoding precision, while enabling the finest-grained Situs deployment, makes the system maximally sensitive to wafer-grid alignment error—a 0.5\,nm stage misalignment turns Situs from signal into noise. **Net assessment**: The economic value proposition (CD-SEM cost reduction) is real, but the expert-independence premise underpinning the Chernoff bound is structurally violated. Deploy with calibrated skepticism.

### Multi-Solver Mesh Auditing (FEA/CFD)

$\blacksquare$ Projected — physically reasoned, not experimentally verified.
Computational engineering deploys multiple finite-element/volume solvers (ANSYS Mechanical, Abaqus, OpenFOAM) on identical geometries, creating a natural multi-expert audit scenario. Situs encodes mesh node 3D coordinates $(x,y,z)$ via the rotational encoding scheme—mesh geometry is the physical position, and each solver's stress/strain/pressure solution at each node is an expert opinion on the same physical quantity. The core auditing problem maps cleanly onto SCX theory: distinguishing mesh-induced artifacts [cite] (stress singularities at inadequately refined corners, spurious pressure modes in collocated grids) from genuine physical stress concentrations (label noise vs label signal). Three specific audit targets: (i) turbulence model divergence—k-$\varepsilon$ vs k-$\omega$ SST disagree on separation bubble length at the same $(x,y,z)$, flagging regions where neither model is trustworthy; (ii) convergence spurious detection—residual norms dropping below threshold do not guarantee solution accuracy, a false-negative label noise problem; (iii) boundary condition errors—incorrectly specified inlet profiles or wall functions produce locally coherent but globally wrong solutions detectable through cross-solver disagreement at fixed spatial locations. $\blacksquare$ Critical constraint: Solvers are not independent in the formal sense—they discretize the same governing equations (Navier-Stokes, linear elasticity) using related numerical methods. Expert correlation reduces effective $M$ and weakens the Chernoff bound. Moreover, mesh node positions differ across solvers even for the same geometry (different meshing algorithms), requiring interpolation to a common grid before position-encoded comparison—the interpolation itself introduces positional noise.

## Medical Imaging: Multi-Modal Voxel Auditing
<!-- label: sec:medical -->

$\blacksquare$ Projected — physically reasoned, not experimentally verified.
Medical imaging generates multiple modalities (CT, MRI with multiple sequences, PET) of the same anatomical region, producing voxel-grid data with explicit $(x,y,z)$ coordinates. Each modality is a natural expert on tissue state, sensitive to fundamentally different physical properties (electron density for CT, proton relaxation for MRI, metabolic activity for PET). Situs encodes voxel coordinates directly—the same $(x,y,z)$ in patient space should correspond to the same anatomical location across modalities. Three audit targets: (i) multi-modal registration inconsistency—misalignment after registration produces discordant tissue labels at the same Situs coordinates, flagging registration failures rather than tissue differences; (ii) tumor segmentation disagreement [cite]—different modalities reveal different tumor boundaries, and position-indexed disagreement patterns distinguish genuine infiltrative margins (label-clean) from modality-specific segmentation failures (label-noise); (iii) radiomics [cite] feature cross-modal instability—texture and shape features extracted from the same $(x,y,z)$ region differ across modalities beyond physically expected bounds. $\blacksquare$ Critical caveat: Registration error is the dominant failure mode. If CT and MRI voxel coordinates are misaligned by even 2--3 voxels, Situs amplifies the error by encoding physically mismatched positions as the same $p$—$\delta_s^{\mathrm{PE}}$ turns negative because position disagreement is misattributed to label noise. Deformable registration uncertainty must be propagated into the Situs encoding as positional variance.

## Explicitly Excluded: When the Framework Says No
<!-- label: sec:excluded -->

A framework earns credibility not by claiming universal applicability but by clearly stating where it *cannot* work. We document one domain where Situs's preconditions fail structurally, one domain where they are conditionally satisfied, and one class of applications whose real-time constraints place them outside SCX's architectural scope.

**Enzyme active site prediction (1D sequence position).** The mapping from 1D sequence position to 3D functional position is not a function---insertions, deletions, and fold divergence across homologs break the correspondence. When pre-trained protein language models (ESM-2, ProtBERT) already provide sequence-position embeddings through attention, 1D Situs adds redundant dimensions with zero marginal information---a pure multicollinearity loss.

**Oceanographic multi-platform auditing (conditional).** $\blacksquare$ Conditionally included — physically reasoned, not experimentally verified. Argo floats (in-situ T/S profiles), satellite altimetry (sea surface height), satellite salinity (SMOS/Aquarius), and ocean reanalysis products (GLORYS12, ECCO, HYCOM) observe the same ocean through fundamentally different physical channels, creating a natural multi-expert matrix at 4D spatiotemporal coordinates $(lat,lon,depth,t)$. **Feasible regions**: The North Atlantic ($>20$ Argo profiles per $1^\circ \times 1^\circ$ per decade) and North Pacific have sufficient in-situ density for meaningful multi-platform comparison; when augmented with satellite altimetry and reanalysis as additional ``experts,'' the effective $M_{eff}$ reaches 4--5. **Infeasible regions**: The deep ocean interior ($>2000$\,m), Southern Ocean, and most of the Indian Ocean remain below five Argo profiles per $1^\circ \times 1^\circ$ per decade---insufficient for Theorem~1's multi-expert consistency analysis. Satellite-only experts (altimetry, salinity) provide surface constraints but cannot audit the interior. Reanalysis products add expert diversity but introduce model-structure correlation (many share NEMO/MOM6 ocean cores)---the same genealogy problem that plagues CMIP6.

**Autonomous driving and embodied intelligence (offline audit only).** Multi-sensor fusion (camera, LiDAR, radar, ultrasonic) and multi-modal robot perception (vision, tactile, force-torque, proprioception) offer naturally structured multi-expert matrices with perfect Situs encoding. The audit problem---distinguishing sensor failure from genuinely ambiguous scenes---is a canonical Theorem~3 instance. **However**, SCX's batch auditing architecture is fundamentally incompatible with the sub-100ms decision windows required for real-time control. These domains are viable for *offline* auditing of sensor annotation quality, simulation-to-reality gap quantification, and demonstration data quality assessment---but not for online perception or control.

## Hard Boundaries: Three Ways Situs Fails
<!-- label: sec:hard -->

Situs is not ``harmless if useless.'' In specific, identifiable conditions, it is actively harmful. We document three hard failure modes, now with examples drawn from the expanded 13-scenario survey.

### Spurious Correlation: The Greatest Practical Risk
<!-- label: sec:spurious -->

When position $P$ correlates with label $Y$ in the training data for non-causal reasons, Situs learns the correlation and propagates it to test time. The expanded survey reveals domain-specific spurious correlation patterns:

- ****Genomics — reference genome bias**.:** All sequencing platforms align to the same reference genome. Variant calling algorithms share heuristics for mapping quality and base quality recalibration. If all experts systematically miss variants in GC-rich or repetitive regions at the same genomic positions, Situs learns ``no variant at $p$ in high-GC region $\to$ clean''—a shared-blindness artifact that position-encodes as confidence.
- ****Climate — model genealogy confounding**.:** CMIP6 models share atmospheric component codes (e.g., ECMWF-based models, GFDL family). Inter-model agreement at a grid cell may reflect code genealogy rather than physical robustness. Situs learns ``agreement pattern at $(lat,lon,z,t)$ $\to$ label-clean'' when the agreement is an artifact of shared parameterization.
- ****Engineering — mesh convention artifact**.:** Different organizations use different mesh-quality standards and refinement conventions. If all training simulations from Lab A refine the mesh at geometric discontinuities while Lab B does not, Situs learns ``refined mesh at corner $p$ $\to$ high stress''—a meshing convention masquerading as physics.

$\blacksquare$ Detection protocol: $\delta_s^{\mathrm{PE}} > 0$ on training set but $\delta_s^{\mathrm{PE}} \to 0$ or $< 0$ on an i.i.d.\ validation set is the signature of spurious correlation. A permutation test shuffling position--label pairs provides a null distribution for $I(Y; P \mid S)$ under the hypothesis of no causal link.

### Multicollinearity with Pre-Existing Structural Encodings
<!-- label: sec:multi -->

When the state representation $\phi(s_i)$ already encodes position implicitly, the additive injection $\phi(s_i) + \mathrm{PE}(p_i)$ creates redundant dimensions:

- ****GNN + Situs on crystals**.:** Graph neural networks aggregate neighborhood information through message passing, which implicitly encodes distance and angular relationships. Adding 3D Situs on top of GNN node features adds information already captured by graph convolution layers. Result: $I(Y; \mathrm{PE}(P) \mid \phi_{GNN}(S)) \approx 0$, but the extra dimensions increase optimization difficulty.
- ****pLM + Situs on proteins**.:** ESM-2 and similar protein language models use attention with positional bias, naturally encoding sequence position. Adding sinusoidal 1D encoding on top is redundant—a ``double encoding'' that inflates dimensionality without adding information.
- ****Climate model output statistics + Situs**.:** Climate models already output on a $(lat,lon)$ grid; the state representation $\phi(s_i)$ typically includes the grid cell index. Adding Situs on top of already-indexed grid coordinates is pure dimensional inflation.

$\blacksquare$ Rule of thumb: Situs is most valuable when it is the **only** source of spatial information. If the backbone model already has strong spatial inductive biases (GNN, Transformer with positional encoding [cite], equivariant network, geospatial indexing), the marginal benefit of Situs approaches zero.

### Rotational Equivariance Failure and Symmetry Breaking
<!-- label: sec:rotation -->

Situs's 3D rotational encoding is **translation-invariant** but **not rotation-equivariant**. For two positions $\mathbf{p}, \mathbf{q}$:

$$
\langle \mathrm{PE}_{rot}(\mathbf{p}), \mathrm{PE}_{rot}(\mathbf{q}) \rangle = \cos(\alpha\Delta x) + \cos(\beta\Delta y) + \cos(\gamma\Delta z)
$$

This depends only on $\Delta\mathbf{p} = \mathbf{q} - \mathbf{p}$ (translation invariance $\checkmark$). However, a physical rotation $R_{phys} \in SO(3)$ mixes the $x$, $y$, $z$ axes, while the encoding allocates **non-overlapping** dimension pairs to each axis---there is no transformation $T$ in encoding space such that $T \cdot \mathrm{PE}(\mathbf{p}) = \mathrm{PE}(R_{phys}\mathbf{p})$.

**Domain-specific consequences**:

- **Polycrystalline materials**: Different grains have different orientations—the same defect receives different encodings in different grains.
- **Molecular dynamics**: Overall molecular rotation changes all atom encodings; the model may learn ``rotation state'' instead of ``physical state.''
- **Medical imaging**: Patient orientation in the scanner varies across acquisitions; the same anatomical feature at the same $(x,y,z)$ in scanner coordinates may correspond to different physical anatomy across sessions.
- **Seismology**: Coordinate system choice (geographic vs geomagnetic vs local tangent plane) is arbitrary; Situs encoding changes with coordinate convention.

$\blacksquare$ Partial mitigation: For fixed-orientation or orientation-aligned datasets, the problem does not arise. For general applications, alternative encodings with $SO(3)$ equivariance (spherical harmonics, Tensor Field Networks [cite], SE(3)-Transformers [cite]) exist at the cost of increased dimensionality.

### Additional Symmetry Breaking: Translation and Permutation

- **Translation symmetry breaking** harms bulk property prediction. In a perfect crystal, all primitive cells are equivalent—bulk properties should be translation-invariant. Situs assigns different encodings to equivalent atoms in different cells, forcing the model to ``learn to ignore position''—an avoidable learning burden.
- **Permutation symmetry breaking**: Atoms are a set; their indexing is arbitrary. If data-loading order changes between samples, Situs encodings change for physically identical systems. Mitigation: enforce consistent atom ordering (e.g., sort by coordinates) in pre-processing.

## Roadmap: A Layered Deployment Strategy
<!-- label: sec:roadmap -->

We propose a three-tier deployment strategy that matches Situs complexity to problem structure, avoiding premature complexity. The tiers are updated to reflect the expanded 13-scenario coverage.

- ****Tier 1 — Core (No Situs)**.:** Deploy SCX with state crystallization + Yajie + Spring, **without any spatial encoding**. This is the baseline and should always be the starting point. It is appropriate for:
- ****Tier 2 — Spatial (+Situs)**.:** Add Situs when **all three** conditions are met: (a) $I(Y;P \mid S) > 0$ is physically justified (not just statistically observed), (b) spatial coordinates are available with known precision, and (c) the backbone model does not already encode spatial structure. This tier covers the majority of our 13 scenarios:
- ****Tier 3 — Extended (+Multi-Head Spring)**.:** Deploy multi-head spatial attention to capture anisotropic spatial patterns. This tier is **high-risk, high-reward**:

[Table omitted — see original .tex]

$\blacksquare$ Key projected milestone: A rigorous empirical comparison of Tier~1 vs Tier~2 across all thirteen scenarios in Table [ref], with pre-registered success criteria, permutation-based significance testing for $\delta_s^{\mathrm{PE}}$, and adversarial validation (train on one data source, test on a held-out source). None of this has been done; all claims about $\delta_s^{\mathrm{PE}}$ magnitude for the seven new scenarios (Genomics, Climate, Seismology, Oceanography, Engineering Simulation, Medical Imaging, Semiconductor Process) are physically reasoned, not empirically measured.

## Discussion: The Honesty Gap

### What We Know vs What We Think

This paper is a perspective, not an empirical report. We distinguish three epistemic categories, updated for the expanded survey:

1. **Mathematically verified** (Theorem~2.2.1, Theorem~2.5.1, Theorem~4 bounds): The information-theoretic criterion $I(Y;P \mid S) > 0$ is a mathematically necessary condition. The Lipschitz continuity of sinusoidal and rotational encoding is proven with exact constants. The minimax optimality of Yajie's error exponent is established via Chernoff-Stein.
2. **Physically reasoned** (all 13 scenario analyses in \S\S3--8): All $\delta_s^{\mathrm{PE}}$ magnitude estimates are derived from known physical laws (DFT formation energies, protein biophysics, sequencing error models, Navier-Stokes numerics, climate model genealogy, wave propagation physics) combined with the Fano lower bound. Of the thirteen scenarios, only the AlN defect and CNT chirality cases (Scenarios A--B) have supporting DFT data; the remaining eleven are physically grounded predictions, not measured effects. They can be---and should be---falsified by experiment.
3. **Speculative** (Multi-Head Spring's superadditivity, cross-domain transfer of $\delta_s^{\mathrm{PE}}$): These are conjectures grounded in the mathematical structure of the framework. They have not been tested even in simulation. They are included as a research agenda, not as claims.

### Who Should Care (Expanded)

- **Computational materials scientists**: Situs on 3D coordinates is the highest-confidence deployment scenario (Scenarios A--B: $\star\star\star$). Wafer process simulation (Scenario C) adds a conditional, high-impact industrial application. Start with Tier~2 on defect formation energies.
- **Computational biologists and bioinformaticians**: Genomics (Scenario F) is the most promising new scenario—base-pair precision 1D encoding combined with a rich multi-platform $\times$ multi-algorithm expert matrix. If you already use a pLM for protein tasks, 1D Situs probably adds nothing.
- **Earth \& environmental scientists**: Your data is **natively spatiotemporal** (Scenarios G--J), and your observing systems are **naturally independent experts**. Three of the seven new scenarios fall in this domain group — the largest concentration of any domain. We encourage proof-of-concept studies on CMIP6 (publicly available, $\sim$100\,TB), Argo (public, $\sim$2 million profiles), and IRIS seismic archives.
- **Astronomers**: Cross-survey auditing (Scenario K) is architecturally the best fit for Yajie + Situs. Proof-of-concept on SDSS $\times$ Gaia cross-matched quasars is the lowest-hanging fruit.
- **Engineering simulation practitioners**: Multi-solver auditing (Scenario L) addresses a recognized industrial pain point—simulation results that differ between ANSYS and Abaqus for the same geometry. The common-grid interpolation requirement is the primary deployment barrier.
- **Medical imaging researchers**: Multi-modal auditing (Scenario M) is conceptually clean but registration-error amplification is the dominant practical risk. Start with rigid-registration cases (brain CT/MRI) before tackling deformable cases.
- **ML researchers**: Do not assume Situs is ``obviously good.'' Run the predictive sufficiency test. If your GNN or Transformer already encodes position, Situs is redundant. If position is your only geometry signal, Situs is your best tool.

### Open Problems (Updated)

1. **Rigorous multi-head Chernoff bound**: Extend Theorem~1 to handle conditionally dependent head outputs. Particularly urgent for climate (model genealogy) and engineering (shared governing equations) where expert independence is structurally violated.
2. **KSG-based $I(Y;P \mid S)$ estimation at scale**: Practical estimation of the decision criterion for 4D spatiotemporal state spaces (climate, oceanography) remains an open computational challenge.
3. **$SO(3)$-equivariant Situs**: Design a positional encoding that is both computationally efficient ($d_{pe} \leq 32$) and fully rotation-equivariant. Relevant to materials, medical imaging (patient orientation), and seismology (coordinate conventions).
4. **Registration-error propagation in Situs**: Quantify how misregistration uncertainty in medical imaging and common-grid interpolation error in engineering simulation propagate into $\delta_s^{\mathrm{PE}}$. Current bound assumes perfect positional precision.
5. **Empirical validation (the big one)**: All empirical claims for the seven new scenarios are projected, not measured. The community needs a systematic empirical benchmark—ideally adversarial, pre-registered, and multi-domain—that measures $\delta_s^{\mathrm{PE}}$ across controlled conditions spanning at least three domain groups.
6. **Expert dependence quantification**: Develop a practical diagnostic for estimating effective $M_{eff} < M_{nominal}$ when experts share components (CMIP6 code genealogy, variant caller shared heuristics, solver shared discretization). Current theory assumes independence; every new scenario violates it to some degree.

### Coda: Why Honesty Matters

The ML-for-science literature [cite] is littered with methods that ``should work'' based on physical intuition but fail under adversarial validation. Positional encoding is particularly susceptible to this pattern because ``position matters'' is such a deeply held scientific intuition that researchers are disinclined to check whether it matters *in the specific way their model encodes it*. The hard boundaries documented in \S [ref]---spurious correlation, multicollinearity, symmetry breaking---are not edge cases. They are the default outcome when Situs is applied without causal analysis of the position--label relationship. The expansion from six to thirteen scenarios does not change this fundamental message; it broadens the evidence base for it.

Of the thirteen scenarios surveyed, only two (AlN $V_N$ defect and CNT chirality) have $\star\star\star$ confidence. The remaining eleven carry $\star\star$ confidence—physically reasoned but empirically unverified. This distribution is not a weakness of the framework; it is an accurate reflection of where the field stands. The most scientifically valuable contribution this paper can make is to motivate the adversarial experiments that will turn $\star\star$ into $\star\star\star$---or, more importantly, into ``we were wrong.''

We wrote this paper not to advocate for Situs but to provide the tools for deciding whether Situs should be advocated for in any particular case. The answer, as always in science, is: it depends. Now you can compute what it depends on---across thirteen scientific domains and counting.

## Acknowledgments

This work draws on the SCX theoretical framework developed in  [cite]. We thank the anonymous reviewers of the CC audit report for identifying the sign error in the original $\delta_s^{\mathrm{PE}}$ definition and for pressing the question of when positional encoding is actively harmful rather than merely useless. The expanded 13-scenario survey benefited from consultations with domain experts in bioinformatics, climate science, seismology, oceanography, computational engineering, and medical imaging—none of whom should be held responsible for the physical reasoning we have projected onto their fields. All errors of reasoning and excessive confidence remain our own.

\begin{thebibliography}{99}

\bibitem{ppe_derivation}
SCX Project. Physical Positional Encoding (PPE) in the SCX Framework: Rigorous Derivation. *Working paper*, 2026. `theory/self\_evolution/ppe\_rigorous\_derivation.md`

\bibitem{situs_validation}
SCX Project. Situs Physical Validation and Applicability Analysis. *Working paper*, 2026. `theory/self\_evolution/situs\_physical\_validation.md`

\bibitem{cc_audit}
SCX Project. Multi-Head Spring and Physical Positional Encoding: Rigorous Mathematical Analysis. *Working paper*, 2026. `theory/self\_evolution/multi\_head\_spring\_and\_positional\_encoding\_analysis.md`

\bibitem{freysoldt2014}
Freysoldt, C., *et al.* First-principles calculations for point defects in solids. *Rev.\ Mod.\ Phys.* **86**, 253--305 (2014).

\bibitem{stampfl2002}
Stampfl, C. \& Van de Walle, C.\ G. Theoretical investigation of native defects, impurities, and complexes in aluminum nitride. *Phys.\ Rev.\ B* **65**, 155212 (2002).

\bibitem{makov1995}
Makov, G. \& Payne, M.\ C. Periodic boundary conditions in *ab initio* calculations. *Phys.\ Rev.\ B* **51**, 4014--4022 (1995).

\bibitem{freysoldt2009}
Freysoldt, C., Neugebauer, J. \& Van de Walle, C.\ G. Fully *ab initio* finite-size corrections for charged-defect supercell calculations. *Phys.\ Rev.\ Lett.* **102**, 016402 (2009).

\bibitem{sentaurus}
Synopsys Inc. Sentaurus Process User Guide, Version T-2024.09. *Technical Report*, 2024.

\bibitem{silvaco}
Silvaco Inc. Victory Process User Manual, Version 8.0. *Technical Report*, 2024.

\bibitem{pauling1951}
Pauling, L., Corey, R.\ B. \& Branson, H.\ R. The structure of proteins: Two hydrogen-bonded helical configurations of the polypeptide chain. *Proc.\ Natl.\ Acad.\ Sci.* **37**, 205--211 (1951).

\bibitem{dunker2005}
Dunker, A.\ K., *et al.* Intrinsically disordered protein. *FEBS J.* **272**, 5129--5148 (2005).

\bibitem{lin2023}
Lin, Z., *et al.* Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science* **379**, 1123--1130 (2023).

\bibitem{depristo2011}
DePristo, M.\ A., *et al.* A framework for variation discovery and genotyping using next-generation DNA sequencing data. *Nat.\ Genet.* **43**, 491--498 (2011).

\bibitem{poplin2018}
Poplin, R., *et al.* A universal SNP and small-indel variant caller using deep neural networks. *Nat.\ Biotechnol.* **36**, 983--987 (2018).

\bibitem{sedlazeck2018}
Sedlazeck, F.\ J., *et al.* Accurate detection of complex structural variation using single-molecule sequencing. *Nat.\ Methods* **15**, 461--468 (2018).

\bibitem{garrison2012}
Garrison, E. \& Marth, G. Haplotype-based variant detection from short-read sequencing. *arXiv*:1207.3907 (2012).

\bibitem{kim2018}
Kim, S., *et al.* Strelka2: fast and accurate calling of germline and somatic variants. *Nat.\ Methods* **15**, 591--594 (2018).

\bibitem{eyring2016}
Eyring, V., *et al.* Overview of the Coupled Model Intercomparison Project Phase 6 (CMIP6) experimental design and organization. *Geosci.\ Model Dev.* **9**, 1937--1958 (2016).

\bibitem{knutti2013}
Knutti, R., Masson, D. \& Gettelman, A. Climate model genealogy: Generation CMIP5 and how we got there. *Geophys.\ Res.\ Lett.* **40**, 1194--1199 (2013).

\bibitem{dziewonski1981}
Dziewonski, A.\ M. \& Anderson, D.\ L. Preliminary reference Earth model. *Phys.\ Earth Planet.\ Inter.* **25**, 297--356 (1981).

\bibitem{ekstrom2012}
Ekström, G., Nettles, M. \& Dziewonski, A.\ M. The global CMT project 2004--2010: Centroid-moment tensors for 13,017 earthquakes. *Phys.\ Earth Planet.\ Inter.* **200--201**, 1--9 (2012).

\bibitem{tromp2019}
Tromp, J. Seismic wavefield imaging of Earth's interior across scales. *Nat.\ Rev.\ Earth Environ.* **1**, 40--53 (2019).

\bibitem{roemmich2009}
Roemmich, D., *et al.* The Argo Program: Observing the global ocean with profiling floats. *Oceanography* **22**(2), 34--43 (2009).

\bibitem{letraon2019}
Le Traon, P.\ Y., *et al.* From observation to information and users: The Copernicus Marine Service perspective. *Front.\ Mar.\ Sci.* **6**, 234 (2019).

\bibitem{roache1997}
Roache, P.\ J. Quantification of uncertainty in computational fluid dynamics. *Annu.\ Rev.\ Fluid Mech.* **29**, 123--160 (1997).

\bibitem{oberkampf2002}
Oberkampf, W.\ L. \& Trucano, T.\ G. Verification and validation in computational fluid dynamics. *Prog.\ Aerosp.\ Sci.* **38**, 209--272 (2002).

\bibitem{isensee2021}
Isensee, F., *et al.* nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation. *Nat.\ Methods* **18**, 203--211 (2021).

\bibitem{gillies2016}
Gillies, R.\ J., Kinahan, P.\ E. \& Hricak, H. Radiomics: Images are more than pictures, they are data. *Radiology* **278**, 563--577 (2016).

\bibitem{vaswani2017}
Vaswani, A., *et al.* Attention is all you need. *NeurIPS* (2017).

\bibitem{thomas2018}
Thomas, N., *et al.* Tensor field networks: Rotation- and translation-equivariant neural networks for 3D point clouds. *NeurIPS* (2018).

\bibitem{fuchs2020}
Fuchs, F.\ B., *et al.* SE(3)-Transformers: 3D roto-translation equivariant attention networks. *NeurIPS* (2020).

\bibitem{northcutt2021}
Northcutt, C.\ G., Jiang, L. \& Chuang, I.\ L. Confident learning: Estimating uncertainty in dataset labels. *J.\ Artif.\ Intell.\ Res.* **70**, 1373--1411 (2021).

\bibitem{ghorbani2019}
Ghorbani, A. \& Zou, J. Data Shapley: Equitable valuation of data for machine learning. *ICML* (2019).

\end{thebibliography}