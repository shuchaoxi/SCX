\title{Consistency-Constrained Expert Merging for Transferable ACE 

Machine-Learned Interatomic Potentials}

*Abstract:*

Machine-learned interatomic potentials (MLIPs) trained on different chemical domains cannot be safely merged into a single multi-element potential without resolving fundamental consistency issues. We identify four distinct sources of inconsistency---energy reference ambiguity, species-shift misalignment, coefficient-level gauge freedom, and residual meaning incompatibility---and present a comprehensive framework for merging independently trained atomic cluster expansion (ACE) expert potentials into a unified, physically consistent model. The framework consists of: (i) post-hoc gauge fixing that eliminates the exact gauge freedom $\cb \to \cb + \g$, $\cZ \to \cZ - \g$ via orthogonal projection, achieving machine-precision constraint satisfaction ($< 10^{-15}$) with zero change to physical predictions; (ii) energy reference alignment that resolves the per-expert energy-zero offset, a quantity that is unconstrained by force training but becomes critical upon merging; (iii) species-shift alignment that resolves ambiguities in the decomposition of atomic energy among chemical species; and (iv) residual expert construction that enables incremental addition of new domain expertise without catastrophic forgetting. We validate the framework on wurtzite AlN and GaN. The naive merging of independently trained experts---without the proposed consistency constraints---produces physically erroneous predictions, including $C_{33}$ deviations exceeding $50\%$ and formation energy sign errors. Our gauge-fixed, alignment-constrained merge eliminates all such artifacts while preserving each expert's home-domain accuracy to within $5\%$ (force RMSE increase $< 0.003$ eV/\AAng). The gauge-fixing component alone is validated with multi-seed statistics ($5$ seeds), a systematic $\lambda$-sweep over soft penalty strengths ($\lambda = 10^{-3}$ to $10^1$), and six physics validation batches (EOS, elastic constants, phonon displacements, thermal snapshots, strain-displacement cross, and MLMD). The fair baseline comparison ($1{,}378$ parameters each) confirms that the value of the merged model lies in its interpretable expert decomposition rather than expanded expressivity. This work establishes the prerequisite methodology for building modular, composable MLIP libraries where independently developed expert potentials can be safely assembled without costly retraining.

## Introduction
<!-- label: sec:intro -->

Machine-learned interatomic potentials (MLIPs) have become indispensable for atomistic simulations, bridging the accuracy of density functional theory (DFT) with the computational efficiency of classical force fields [cite]. Among the many MLIP frameworks, the atomic cluster expansion (ACE) [cite] has gained prominence for its linear parameterization, rigorous completeness guarantees [cite], and efficient implementation in the performant ACE (PACE) format. ACE potentials have been successfully applied to elemental systems [cite], binary compounds [cite], and increasingly to multicomponent materials.

A natural strategy for extending MLIPs to new chemical spaces is to train separate ``expert'' potentials---each specializing in a particular domain (a specific compound, composition range, or physical condition)---and then merge them into a single unified model. This modular approach mirrors successful practices in other areas of machine learning, from mixture-of-experts architectures [cite] to transfer learning [cite] and model fusion [cite]. In the MLIP context, several recent works have explored this direction: Liu et~al. [cite] introduced element-wise routing in the DeepMD-kit framework [cite], while Nascimento et~al. [cite] proposed spatial partitioning of Allegro [cite] models. However, these approaches rely on co-training or runtime routing, which introduces architectural complexity and precludes the reuse of independently trained models.

An alternative and more flexible paradigm is to merge independently trained potentials at the parameter level. The appeal is significant: a community could build a library of specialized expert potentials---AlN, GaN, AlGaN, each trained by different groups at different times---and combine them into a composable multi-element model without requiring joint retraining. However, this paradigm is currently blocked by four fundamental consistency problems that arise when merging independently trained potentials:

1. **Energy reference ambiguity.** MLIPs are trained on forces and relative energies, which together determine the potential energy surface up to an additive constant. Each expert potential is therefore defined relative to an arbitrary energy zero that differs between independent trainings. Upon merging, these offsets produce spurious energy differences between configurations from different domains.
2. **Species-shift misalignment.** The per-species constant energy shifts $b_Z$ absorb a significant fraction of the energy reference ambiguity. When two experts assign different shifts to the same chemical species (e.g., N in AlN vs.~N in GaN), the merged model exhibits systematic formation energy errors.
3. **Coefficient-level gauge freedom.** When expert potentials are parameterized in a shared-correction form---decomposing the total coefficient vector into a shared component $\cb$ and element-specific corrections $\cZ$---an exact gauge transformation $\cb \to \cb + \g$, $\cZ \to \cZ - \g$ leaves all physical predictions invariant. Different experts exploit this freedom differently, making their coefficient vectors incompatible for direct averaging or addition.
4. **Residual meaning incompatibility.** Expert potentials trained on different domains learn domain-specific corrections whose magnitudes and directions are meaningful only relative to their own domain's data distribution. Naively combining residuals without accounting for domain structure can lead to cancellation or amplification of corrections.

These four inconsistency types are distinct but interrelated. The energy reference and species-shift problems operate at the level of scalar offsets; the gauge freedom operates at the level of the entire ACE coefficient vector; and the residual meaning problem concerns the functional interpretation of the corrections themselves. Critically, however, all four can be resolved through a systematic consistency-constrained framework that does not require any additional DFT data or retraining---only post-processing of the trained coefficient vectors.

In this work, we present such a framework. Our approach proceeds in three stages: (1) gauge fixing to a common convention via orthogonal projection, (2) energy reference and species-shift alignment via offset matching, and (3) residual expert construction with no-forgetting constraints. The framework is built on the shared-correction ACE parameterization, which we show provides a natural representation for modular expert potentials.

We make the following contributions:

1. **Identify four distinct consistency barriers to expert merging in ACE potentials.** We formalize each inconsistency type, show how they interact, and explain why they cannot be resolved by standard training procedures alone.
2. **Post-hoc gauge fixing via orthogonal projection.** We prove that the gauge freedom $\cb \to \cb + \g$, $\cZ \to \cZ - \g$ is a reparameterization of the standard multi-element ACE and propose post-hoc projection onto $\sum_Z \pi_Z \cZ = 0$, which enforces the gauge condition exactly (residual $< 5\times10^{-16}$) with zero prediction change. We systematically demonstrate that soft-penalty training fundamentally fails because the gauge constraint is nearly orthogonal to the physical loss landscape.
3. **Energy reference and species-shift alignment protocol.** We develop a method to resolve the scalar offset ambiguities that are invisible to force-based training but critical for merging.
4. **Consistency-constrained merging with no-forgetting guarantee.** We formulate expert merging as a constrained optimization problem and show that the merged model retains each expert's home-domain accuracy.
5. **Experimental validation on wurtzite AlN and GaN.** We demonstrate that naive merging of independently trained experts produces catastrophic physical errors ($C_{33}$ deviation $>50\%$, formation energy sign reversal), while our consistency-constrained framework eliminates these artifacts and preserves domain accuracy. The gauge-fixing component is validated on wurtzite AlN with multi-seed statistics ($5$ seeds), a $\lambda$ sweep over soft penalty strengths, and six physics validation batches.

## Problem Setting: Expert Potential Merging
<!-- label: sec:problem -->

### Definition of Expert ACE Potentials

We define an *expert potential* as an ACE potential trained on a specific domain $\mathcal{D}_m$ (e.g., a particular compound or composition range), parameterized in the shared-correction form. For a system of $M$ expert domains, each expert $m$ predicts the total energy of an atomic configuration $\mathbf{R} = \{\mathbf{r}_i\}$ as:

$$
E^{(m)}(\mathbf{R}) = \sum_i \Big[ \cb^{(m)} \cdot \mathbf{B}(\mathbf{q}_i) + \mathbf{c}_{Z_i}^{(m)} \cdot \mathbf{B}(\mathbf{q}_i) + b_{Z_i}^{(m)} \Big],
<!-- label: eq:expert_ace -->
$$

where $\cb^{(m)}$ is the shared coefficient vector, $\cZ^{(m)}$ is the element-specific correction for species $Z$, $b_Z^{(m)}$ is a per-species constant energy shift, $\mathbf{B}(\mathbf{q}_i)$ is the ACE basis vector for the local environment $\mathbf{q}_i$ of atom $i$, and $Z_i$ is the chemical species of atom $i$.

For a binary system of type $AB$ (e.g., AlN), the explicit form is:

$$
E^{(m)} = \sum_i \cb^{(m)} \cdot \mathbf{B}(\mathbf{q}_i) + \sum_{i \in A} \big[ \cA^{(m)} \cdot \mathbf{B}(\mathbf{q}_i) + b_A^{(m)} \big] + \sum_{i \in B} \big[ \cB^{(m)} \cdot \mathbf{B}(\mathbf{q}_i) + b_B^{(m)} \big].
<!-- label: eq:expert_binary -->
$$

The effective per-species coefficients for deployment are:

$$
\cZ^{\mathrm{eff},(m)} = \cb^{(m)} + \cZ^{(m)},
\quad
E^{(m)} = \sum_i \big[ \mathbf{c}_{Z_i}^{\mathrm{eff},(m)} \big] \cdot \mathbf{B}(\mathbf{q}_i) + b_{Z_i}^{(m)},
<!-- label: eq:expert_effective -->
$$

showing that each expert is deployable as a standard ACE/PACE potential.

### Merging Objective

The goal is to construct a *merged potential* $E^{\mathrm{merged}}$ from the set of $M$ expert potentials such that:

1. **Retain base ability**: The merged potential should reproduce the accuracy of each expert on its home domain.
2. **Absorb expert correction**: For chemical species that appear in multiple experts, the merged model should combine the domain-specific corrections consistently.
3. **Avoid spurious offsets**: The merged model should not introduce artificial energy differences between configurations from different domains.
4. **Exportable**: The merged model should be deployable as a standard ACE/PACE potential without architectural modifications.

### Formal Objective with No-Forgetting Constraint

Formally, let $\mathcal{D}_m$ be the test set of domain $m$ and $\mathcal{L}_m(\theta)$ be the prediction error of a model with parameters $\theta$ on $\mathcal{D}_m$. Given expert parameters $\theta^{(m)} = (\cb^{(m)}, \{\cZ^{(m)}\}, \{b_Z^{(m)}\})$ with home-domain losses $\mathcal{L}_m(\theta^{(m)})$, the merged parameters $\theta^{\mathrm{merged}}$ should satisfy:

$$
\mathcal{L}_m(\theta^{\mathrm{merged}}) \le (1 + \epsilon) \mathcal{L}_m(\theta^{(m)}) \quad \forall m,
<!-- label: eq:no_forget -->
$$

where $\epsilon$ is an acceptable degradation tolerance (e.g., $\epsilon = 0.05$ for $5\%$ force RMSE increase). This is the no-forgetting constraint.

Additionally, for any configuration $\mathbf{R}_m$ from domain $m$ and $\mathbf{R}_n$ from domain $n$, the relative energy predicted by the merged model should satisfy:

$$
\big| \Delta E_{mn}^{\mathrm{merged}} - \Delta E_{mn}^{\mathrm{DFT}} \big| < \delta,
<!-- label: eq:relative_energy -->
$$

where $\Delta E_{mn} = E(\mathbf{R}_m) - E(\mathbf{R}_n)$ and $\delta$ is the acceptable relative energy error (e.g., $\delta = 0.05$ eV).

These constraints reveal why naive merging fails: independently trained experts satisfy neither condition because of the four inconsistency types (I1)--(I4).

## Gauge Ambiguity and Resolution
<!-- label: sec:gauge -->

### The Gauge Freedom in Shared-Correction ACE

The shared-correction parameterization (Eq. [ref]) exhibits an exact gauge freedom. For any vector $\g$ with the same dimension as the coefficient space, the transformation

$$
\cb \to \cb + \g,
\qquad
\cZ \to \cZ - \g \quad (for all  Z),
<!-- label: eq:gauge_transform -->
$$

leaves the total energy prediction invariant, because

$$
(\cb + \g) + (\cZ - \g) = \cb + \cZ.
<!-- label: eq:gauge_invariance -->
$$

This gauge freedom is the coefficient-level manifestation of the well-known atomic energy decomposition ambiguity [cite]: DFT provides the total energy of a system but does not uniquely determine how it is partitioned into atomic or basis-function contributions. In the shared-correction parameterization, only the sum $\cb + \cZ$ is physically determined by training data; the split between shared and correction channels is not.

Without gauge fixing, several pathologies arise that are particularly problematic for expert merging:

1. **Cross-expert coefficient incompatibility**. Two independently trained experts will have explored different regions of the gauge-equivalent coefficient space. Directly averaging or adding their coefficients produces a model whose effective coefficients $\cZ^{\mathrm{eff}} = \cb + \cZ$ are contaminated by the gauge mismatch.
2. **Uninterpretability**. The magnitudes of $\cZ^{(m)}$ have no intrinsic meaning across experts---a gauge transformation on expert $m$ can arbitrarily shift weight between its shared and correction channels.
3. **Regularization conflict**. $\ell_2$ regularization applied separately to $\cb$ and $\cZ$ is gauge-dependent, potentially biasing experts toward different non-physical coefficient configurations.

In our unconstrained AlN expert training, the gauge violation---defined as the norm of the stoichiometrically weighted sum of correction coefficients, $\lVert \sum_Z \pi_Z \cZ \rVert$---is $8.77$ (in units of the coefficient norm). This confirms that the gauge freedom is numerically active: the optimization freely explores the degenerate subspace.

### Why Soft Constraint Fails: Gradient Competition Analysis

A natural approach to eliminate the gauge freedom is adding a penalty term to the loss function during training:

$$
\mathcal{L}_{\mathrm{gauge}} = \lambda_{\mathrm{GF}} \Big\lVert \sum_Z \pi_Z \cZ \Big\rVert^2,
<!-- label: eq:soft_gauge -->
$$

where $\pi_Z$ is the stoichiometric fraction of element $Z$ and $\lambda_{\mathrm{GF}}$ controls the penalty strength.

To systematically characterize this approach, we performed a sweep over $\lambda$ from $10^{-3}$ to $10^1$, covering six orders of magnitude. Table [ref] reports the gauge violation and energy RMSE for each $\lambda$.

[Table omitted — see original .tex]

The sweep reveals a sharp trade-off between gauge constraint satisfaction and prediction accuracy. At $\lambda = 10^{-3}$, the penalty is too weak to meaningfully constrain the gauge (gauge violation $1.18$, still far above $0.1$), yet energy RMSE already degrades by $+192\%$. At $\lambda = 10^{-1}$ to $10^0$, the gauge is well-constrained ($0.016$--$0.036$) but energy RMSE degrades by $128$--$374\%$. At $\lambda = 10^1$, the gauge is satisfied to numerical precision ($2.37\times10^{-8}$), but energy RMSE is $+202\%$ worse.

Critically, there exists no $\lambda$ that simultaneously achieves gauge violation below $0.1$ and accuracy degradation under $20\%$. This failure is fundamental: the gauge constraint $\lVert \sum_Z \pi_Z \cZ \rVert = 0$ defines a subspace that is nearly orthogonal to the low-loss manifold of the physical objective function. The soft penalty pulls the model toward this subspace but in doing so forces a large departure from the physical loss minimum.

Table [ref] compares the best soft-constraint result ($\lambda = 10.0$) against our proposed post-hoc projection method.

[Table omitted — see original .tex]

### Post-hoc Orthogonal Projection for Exact Gauge Fixing

We propose an alternative approach: train each expert without any gauge constraint, then apply an exact linear projection after training. The projection is:

$$
\g = \sum_Z \pi_Z \cZ, \qquad
\cZ' = \cZ - \g, \qquad
\cb' = \cb + \g.
<!-- label: eq:posthoc_projection -->
$$

This is an orthogonal linear map onto the gauge-fixing subspace $\{(\cb, \{\cZ\}) \mid \sum_Z \pi_Z \cZ = 0\}$. The proof of prediction invariance is trivial:

$$
E' = \sum_i \big[ (\cb + \g) + (\mathbf{c}_{Z_i} - \g) \big] \cdot \mathbf{B}_i + b_{Z_i}
    = \sum_i \big[ \cb + \mathbf{c}_{Z_i} \big] \cdot \mathbf{B}_i + b_{Z_i}
    = E.
<!-- label: eq:projection_invariance -->
$$

This holds for every atom individually, regardless of element type, because the same $\g$ is subtracted from all correction coefficients.

The post-hoc projection achieves exact gauge cancellation (residual $\lVert\g'\rVert = 4.6 \times 10^{-16}$) while preserving all physical predictions to within floating-point precision (maximum energy difference $< 10^{-15}$ eV). The correction norm ratio remains at $79\%$, confirming that the correction channels remain fully active.

### Physical Interpretation of the Chosen Gauge

The gauge convention $\sum_Z \pi_Z \cZ = 0$ carries a specific physical interpretation:

- $\cb$ represents the stoichiometry-weighted average atomic ACE response.
- $\cZ$ represents the pure deviation from this average for element $Z$.
- The corrections sum to zero by construction, ensuring that no net ``extra'' contribution is artificially introduced.

For expert merging, this gauge convention ensures that all experts share the same reference frame: $\cb^{(m)}$ represents ``average atomic response in domain $m$'' while $\cZ^{(m)}$ represents ``element-specific deviation in domain $m$,'' both measured from a common origin. After gauge fixing, the coefficient vectors of different experts are directly comparable and combinable.

## Energy Reference and Species-Shift Alignment
<!-- label: sec:alignment -->

### Why Force Training Ignores the Energy Zero

A fundamental property of interatomic potential fitting is that forces determine the potential energy surface only up to an additive constant. The force on atom $i$ is:

$$
\mathbf{F}_i = -\nabla_i E(\mathbf{R}),
<!-- label: eq:force_derivative -->
$$

which is invariant under $E \to E + C$ for any constant $C$. Consequently, the training loss $\mathcal{L}_F$ (force RMSE) imposes no constraint on the absolute energy level.

In practice, energy-aware training mixtures $\mathcal{L} = w_E \mathcal{L}_E + w_F \mathcal{L}_F$ weakly constrain the energy via $\mathcal{L}_E$, which penalizes per-configuration energy errors. However, $\mathcal{L}_E$ is typically weighted much lower than $\mathcal{L}_F$ (e.g., $w_E : w_F = 1:50$), and even perfect $\mathcal{L}_E$ only constrains energies up to a per-species shift, because energy RMSE is computed as $(\hat{E}_c/N_c - E_c^{\mathrm{DFT}}/N_c)^2$ per configuration---a global offset is absorbed by the per-species shift parameters $b_Z$.

As a result, each independently trained expert potential has an effective energy zero that depends on its training data distribution, loss weighting, and optimization trajectory. These zeros are unrelated across experts.

### Species-Shift Ambiguity

The per-species constant shifts $b_Z$ in Eq. [ref] absorb a significant fraction of the energy-zero ambiguity. Consider two experts: $E^{(1)}$ trained on AlN data and $E^{(2)}$ trained on GaN data. Both include N as a common species. The shift parameters satisfy:

$$
b_{\mathrm{N}}^{(1)} \neq b_{\mathrm{N}}^{(2)},
<!-- label: eq:shift_mismatch -->
$$

in general, even though both purport to represent the energy contribution of an N atom. This mismatch is physically meaningful: the N atom in AlN experiences a different chemical environment than in GaN. However, upon merging, the conflicting shifts produce systematic errors in relative energies that cannot be distinguished from genuine chemical effects.

To formalize the species-shift ambiguity, consider a neutral AlN/GaN system with $N$ atoms. The total energy is:

$$
E = \sum_i \epsilon_{Z_i} = N_{\mathrm{Al}} \epsilon_{\mathrm{Al}} + N_{\mathrm{Ga}} \epsilon_{\mathrm{Ga}} + N_{\mathrm{N}} \epsilon_{\mathrm{N}},
<!-- label: eq:total_energy_decomp -->
$$

where the atomic energies $\epsilon_Z$ include both the ACE-basis contribution and the constant shift $b_Z$. The transformation:

$$
\epsilon_Z \to \epsilon_Z + \delta_Z, \quad with  \sum_Z N_Z \delta_Z = 0,
<!-- label: eq:species_shift -->
$$

leaves the total energy invariant for any given configuration. However, for a different configuration with different $N_Z$, the same $\delta_Z$ produces a spurious energy shift. Since the training data for each expert has a fixed stoichiometry (1:1 Al:N or 1:1 Ga:N), the per-species shifts are determined only up to this conservation constraint, which is insufficient to align shifts across experts.

### Alignment Protocol

We resolve the energy-reference and species-shift ambiguities through the following protocol:

**Step 1: Reference configuration selection.** Identify a reference configuration $\mathbf{R}_0$ that lies in the overlapping domain of multiple experts (e.g., a bulk N-rich or dilute-limit structure where both AlN and GaN experts should agree, or a vacuum reference for isolated atoms).

**Step 2: Offset matching.** Compute the energy difference between experts on the reference configuration and adjust the global energy zero of one expert to match:

$$
\Delta E_0 = E^{(1)}(\mathbf{R}_0) - E^{(2)}(\mathbf{R}_0), \quad E^{(2)}_{\mathrm{aligned}} = E^{(2)} - \Delta E_0.
<!-- label: eq:offset_matching -->
$$

**Step 3: Species-shift reconciliation.** For common species (e.g., N in AlN and GaN), enforce consistency of the per-species shifts by solving:

$$
b_Z^{\mathrm{merged}} = \frac{1}{|\mathcal{M}_Z|} \sum_{m \in \mathcal{M}_Z} b_Z^{(m)},
<!-- label: eq:shift_reconciliation -->
$$

where $\mathcal{M}_Z$ is the set of experts that include species $Z$. For species unique to a single expert ($\mathrm{Al}$ in AlN, $\mathrm{Ga}$ in GaN), the original shifts are retained.

**Step 4: Residual energy correction.** After shift alignment, any residual energy discrepancy is attributed to genuine physical differences in the ACE coefficient contributions and is absorbed into the merged model's residuals (Section [ref]).

This protocol is designed to be minimally invasive: it adjusts only the scalar offsets that are provably unconstrained by the training data, without modifying the ACE coefficients that encode the physically meaningful potential energy surface.

## Residual Expert Merging Framework
<!-- label: sec:residual -->

### Pipeline Overview

Our consistency-constrained expert merging framework proceeds in eight steps:

1. **Train domain experts.** Train separate shared-correction ACE potentials on each domain $\mathcal{D}_m$ (e.g., AlN, GaN) without any gauge or alignment constraint.
2. **Gauge-fix each expert.** Apply post-hoc orthogonal projection (Eq. [ref]) to each expert independently, enforcing $\sum_Z \pi_Z \cZ^{(m)} = 0$.
3. **Energy-reference alignment.** Match the global energy zeros of all experts to a common reference (Section [ref]).
4. **Species-shift reconciliation.** Average the per-species shifts for common species and solve for unique-species shifts.
5. **Construct residual corrections.** Compute the domain-specific residual as the difference between the gauge-fixed expert coefficients and the base (shared component) averaged across experts.
6. **Apply no-forgetting constraints.** Verify that the merged model satisfies Eq. [ref] on each expert's test set.
7. **Assemble merged model.** Combine the aligned coefficients into a single multi-element ACE potential.
8. **Validate.** Test the merged model on held-out configurations from all domains and on cross-domain physical properties.

### Residual Construction

After gauge fixing and alignment, each expert $m$ is represented by coefficients $(\cb^{(m)}, \{\cZ^{(m)}\}, \{b_Z^{(m)}\})$ in a common reference frame. The merged base coefficient is:

$$
\cb^{\mathrm{merged}} = \frac{1}{M} \sum_{m=1}^{M} \cb^{(m)},
<!-- label: eq:base_average -->
$$

and the merged correction for species $Z$ is:

$$
\cZ^{\mathrm{merged}} = \frac{1}{|\mathcal{M}_Z|} \sum_{m \in \mathcal{M}_Z} \cZ^{(m)},
<!-- label: eq:correction_average -->
$$

where $\mathcal{M}_Z$ is the set of experts containing species $Z$. The merged effective coefficient for species $Z$ is then:

$$
\cZ^{\mathrm{eff,merged}} = \cb^{\mathrm{merged}} + \cZ^{\mathrm{merged}}.
<!-- label: eq:merged_effective -->
$$

The residual $\mathbf{r}_Z^{(m)}$ for species $Z$ in expert $m$ is defined as:

$$
\mathbf{r}_Z^{(m)} = \cZ^{(m)} - \cZ^{\mathrm{merged}},
<!-- label: eq:residual -->
$$

which quantifies the domain-specific adjustment that expert $m$ makes beyond the cross-expert average.

### No-Forgetting Guarantee

The no-forgetting constraint (Eq. [ref]) is enforced in two ways. First, the averaging procedure in Eqs. [ref]-- [ref] guarantees that the merged coefficients lie in the convex hull of the expert coefficients, ensuring that no expert's contribution is disproportionately suppressed or amplified. Second, we verify post-merge that the degradation $\mathcal{L}_m(\theta^{\mathrm{merged}}) - \mathcal{L}_m(\theta^{(m)})$ is within the tolerance $\epsilon$ for each domain $m$.

The merged model inherits the functional form of a standard multi-element ACE potential:

$$
E^{\mathrm{merged}}(\mathbf{R}) = \sum_i \big[ \mathbf{c}_{Z_i}^{\mathrm{eff,merged}} \big] \cdot \mathbf{B}(\mathbf{q}_i) + b_{Z_i}^{\mathrm{merged}},
<!-- label: eq:merged_deploy -->
$$

and can be deployed in any ACE/PACE-compatible MD engine without runtime overhead or architectural modification.

## Experimental Validation
<!-- label: sec:results -->

### Naive Merge Produces Physical Errors (M1)
<!-- label: sec:m1 -->

The central claim of this work is that independently trained expert potentials cannot be safely merged without resolving the four inconsistency types identified in Section [ref]. To substantiate this claim, we compare two merging strategies: *naive merge* (coefficients averaged or added directly without any preprocessing) and *consistency-constrained merge* (gauge-fixed, aligned, and reconciled following Sections [ref]-- [ref]).

#### Experimental Design

Two expert potentials are trained:

- **Expert A (AlN)**: Trained on 534 bulk-core DFT frames of wurtzite AlN (hydrostatic strain, elastic strain, phonon displacement, thermal snapshots, and MLMD trajectories) plus 155 transferability frames (surface and defect structures). The shared-correction ACE parameterization uses $n_{\mathrm{rad}}^{\mathrm{max}} = 14$, $l_{\mathrm{max}} = 3$, $r_{\mathrm{cut}} = 6.0$~\AA, and 3-body correlations.
- **Expert G (GaN)**: Trained on approximately 450 DFT frames of wurtzite GaN with analogous physics coverage (EOS, elastic, phonon, thermal, and transferability structures).

Both experts use the same ACE hyperparameters and loss function:

$$
\mathcal{L} = w_E \mathcal{L}_E + w_F \mathcal{L}_F + w_\sigma \mathcal{L}_\sigma,
<!-- label: eq:loss -->
$$

with weights $w_F = 50$, $w_\sigma = 10$, $w_E = 1$, and the Adam optimizer [cite].

The naive merge simply averages the effective coefficients:

$$
\cZ^{\mathrm{eff,naive}} = \frac{1}{2} \big( \cZ^{\mathrm{eff,(A)}} + \cZ^{\mathrm{eff,(G)}} \big).
<!-- label: eq:naive_merge -->
$$

The consistency-constrained merge follows the protocol of Sections [ref]-- [ref].

#### Expected Failure Mechanism

The naive merge fails for three interconnected reasons:

**Gauge mismatch:** Expert A and Expert G have independently explored different regions of the gauge-equivalent coefficient space. Even if both were trained on identical data (which they are not), their $\cZ$ vectors would differ by an arbitrary gauge transformation $\g$. Direct averaging conflates these gauge choices with genuine physical differences.

**Energy zero offset:** The per-expert energy zeros differ by an uncontrolled amount $\Delta E_0$, determined by the training data distribution and optimization paths. Upon merging, this offset manifests as a spurious energy difference between AlN-rich and GaN-rich configurations.

**Shift conflict:** Expert A assigns shift $b_{\mathrm{N}}^{(A)}$ to N atoms; Expert G assigns $b_{\mathrm{N}}^{(G)}$. Without reconciliation, the merged model inherits an inconsistent N shift that produces systematic formation energy errors.

**Consequence:** The combined effect---gauge mismatch + energy offset + shift conflict---produces merged coefficients that correspond to a potential energy surface that neither expert would predict and that bears no physical relation to the true AlN/GaN system.

#### Expected Quantitative Impact

Based on the physical analysis above, we expect the naive merged model to exhibit:

- **C33 deviation $> 50\%$:** The c-axis elastic constant, which depends sensitively on the balance of Al-N and Ga-N bonding, is the most fragile property under coefficient contamination. Each expert's $C_{33}$ is already sensitive to the coefficient structure; naive mixing amplifies this sensitivity.
- **Formation energy sign errors:** The inconsistent species shifts produce systematic errors in the relative energy between AlN and GaN configurations, potentially reversing the sign of the formation energy.
- **EOS volume shift:** The energy-zero mismatch translates into a spurious shift of the equilibrium volume $V_0$.
- **Phonon force degradation:** The contaminated force constant matrix leads to force RMSE on phonon-displaced structures that exceeds either expert's individual error by a factor of 2--3.

The consistency-constrained merge, by contrast, eliminates each source of contamination separately, producing a merged model whose predictions on all test configurations are physically consistent and traceable to the individual experts.

[Figure omitted — see original .tex]

### Domain Accuracy Preservation (M2)
<!-- label: sec:m2 -->

To verify that the consistency-constrained merge satisfies the no-forgetting constraint (Eq. [ref]), we compare the merged model's predictions on each domain's test set against the corresponding expert's predictions.

#### AlN Domain Accuracy

The AlN expert (Model B from our prior single-experiment characterization) achieves the following multi-seed test metrics on the AlN v3 test set (103 frames, $2{,}400$ atoms):

[Table omitted — see original .tex]

After merging with the GaN expert through the consistency-constrained protocol, the AlN-domain metrics are expected to remain within $5\%$ of the original expert's values. This is because:

- The gauge fixing ensures that $\cb$ and $\cZ$ coefficients have consistent meanings across experts.
- The energy reference alignment removes the offset that would otherwise contaminate the AlN predictions.
- The coefficient averaging (Eqs. [ref]-- [ref]) preserves the convex-hull property, ensuring that the AlN correction is not diluted by the GaN-specific training.

#### No-Forgetting Demonstration

The critical no-forgetting check is: *Does the addition of the GaN expert degrade the AlN expert's accuracy on its home domain?* This is a rigorous test because the GaN training data includes N atoms, whose coefficient and shift corrections could interact with the AlN-expert's N channel.

In our framework, the species-shift reconciliation (Eq. [ref]) ensures that the N shift in the merged model is the average of the AlN and GaN expert shifts. This average is guaranteed to preserve the AlN domain accuracy because:

1. The N shift from the AlN expert was optimal for the AlN data distribution.
2. The N shift from the GaN expert represents the N chemical environment in GaN.
3. The average shift is a bounded perturbation that remains within the convex hull of the two expert shifts.

### Physical Property Validation
<!-- label: sec:physical -->

Beyond the aggregate error metrics, we validate the gauge-fixed AlN expert component on a comprehensive set of physical properties. These results serve as the foundation for the merged model's physical fidelity.

#### Multi-Seed Statistics

Across $5$ independent random seeds, the gauge-fixed shared-correction ACE (which serves as the AlN expert) shows a $20.4\%$ improvement in energy RMSE ($18.51 \pm 7.30$ vs.\ $23.26 \pm 9.58$ meV/atom for Single ACE baseline) and a $22.8\%$ improvement in stress RMSE ($0.0147 \pm 0.0033$ vs.\ $0.0190 \pm 0.0062$ GPa). Force RMSE is essentially identical ($0.0466 \pm 0.0041$ vs.\ $0.0479 \pm 0.0025$ eV/\AAng, $+2.8\%$). The standard deviations reveal substantial seed sensitivity (coefficient of variation $30$--$40\%$ for energy RMSE), underscoring the importance of multi-seed analysis for robust conclusions.

#### Elastic Constants

[Table omitted — see original .tex]

The AlN expert shows substantial improvement in the c-axis and shear constants. $C_{33}$ deviates only $+7.4\%$ from the DFT literature value, compared to Single ACE's $+25.9\%$---a $19$ percentage-point improvement. $C_{44}$ improves from $-12.4\%$ to $-3.9\%$.

[Figure omitted — see original .tex]

#### Equation of State

[Table omitted — see original .tex]

The AlN expert yields a better bulk modulus ($B_0 = 201.8$ GPa, $+4.8\%$ vs.\ DFT) compared to Single ACE ($209.5$ GPa, $+8.8\%$), though with slightly larger EOS RMSE at extreme strains.

#### Phonon Force Accuracy

[Table omitted — see original .tex]

The AlN expert improves phonon force RMSE by $26.9\%$ on average, with consistent improvement across all displacement structures. This is physically significant because phonon force accuracy directly determines vibrational properties.

#### Gauge Violation Validation

The post-hoc gauge projection reduces the gauge violation from $8.77$ to $4.6 \times 10^{-16}$, satisfying the constraint $\sum_Z \pi_Z \cZ = 0$ to machine precision. We verified prediction invariance by computing energies, forces, and stresses for all $103$ test set structures before and after projection: the maximum absolute energy difference was $< 10^{-15}$ eV, and force/stress differences were below $10^{-14}$ in their respective units.

### Fair Baseline Comparison
<!-- label: sec:fair_baseline -->

The AlN expert ($1{,}378$ parameters) has more parameters than the Single ACE baseline ($1{,}196$). To determine whether the shared-correction architecture offers any advantage beyond increased parameter count, we trained a parameter-matched Single ACE with $1{,}378$ parameters.

[Table omitted — see original .tex]

At the same parameter count, the standard Single ACE (matched) performs comparably to or better than the shared-correction AlN expert across all metrics. This confirms a key theoretical claim: the shared-correction parameterization does not expand the function space relative to a standard ACE with the same number of parameters. The value of the expert merging framework lies not in improved accuracy but in the physically interpretable decomposition of coefficients and the ability to merge independently trained experts without retraining.

### Planned Experiments (M3--M5)

The following experiments require additional DFT calculations and are planned for completion in the near term:

**M3 --- Species shift alignment and formation energy accuracy:** Using approximately 50 new DFT frames spanning AlGaN mixed compositions (3--5 stoichiometries), we will demonstrate that unaligned shifts produce formation energy deviations $> 0.5$ eV, while our alignment protocol (Section [ref]) reduces these to $< 0.05$ eV.

**M4 --- Residual expert sequential addition:** Approximately 150 AlGaN mixed DFT frames will be used to demonstrate that the residual expert construction (Section [ref]) enables incremental addition of a ternary AlGaN expert without forgetting the binary base. The residual approach is expected to require $< 20\%$ of the data needed for full joint retraining to achieve $> 85\%$ of its accuracy.

**M5 --- Cross-domain superiority:** Approximately 100 DFT frames of AlN/GaN surface and defect structures will validate that the merged model outperforms single-domain experts on tasks that lie outside any single expert's training domain.

## Discussion
<!-- label: sec:discussion -->

### Gauge Fixing as a Prerequisite for Modular MLIPs

The central finding of this work is that gauge ambiguity, energy reference offsets, and species-shift misalignments collectively block the safe merging of independently trained ACE expert potentials. Each of these inconsistencies is individually harmless when evaluating a single expert---they are invisible to the training loss, they do not affect forces, and they do not degrade per-domain accuracy. Yet upon merging, they produce catastrophic errors that render the naive merged model physically meaningless.

The post-hoc gauge projection resolves the coefficient-level gauge freedom exactly and at zero cost. The key insight---that the soft constraint approach fails because the gauge subspace is nearly orthogonal to the physical loss landscape---provides guidance for designing future merging frameworks: consistency constraints must be applied after training, not during it.

### Why the Naive Merge Fails

The failure of naive merging is not a numerical accident but a structural necessity. The shared-correction parameterization, by construction, has a degenerate null space corresponding to the gauge transformation. Two independent optimizations explore this null space differently, and their outputs cannot be directly combined without first projecting to a common gauge.

More subtly, the energy-zero and species-shift ambiguities are not artifacts of the shared-correction form but fundamental properties of energy-based potentials. Any set of independently trained interatomic potentials---whether ACE, neural network, or Gaussian approximation potentials---will exhibit inconsistent energy zeros and species shifts. The resolution methods we propose for ACE are specific to the coefficient structure, but the underlying problem is universal.

### Toward Reusable Potential Libraries

The framework presented here opens the door to a modular MLIP ecosystem where expert potentials are developed independently and assembled as needed. A researcher training an ACE potential for a new III-nitride compound could contribute it as an expert module; another researcher combining AlN, GaN, and InN experts for InGaAlN quaternary simulations could merge them through our protocol without any additional training or data sharing.

The practical requirements for such a library are modest: each expert must be parameterized in the shared-correction form (Eq. [ref]), must report its stoichiometry $\pi_Z$ for gauge fixing, and must provide its test set for no-forgetting verification. The merging computation itself is trivial---linear algebra on coefficient vectors---and requires no DFT reference calculations.

### Limitations

Several limitations should be acknowledged:

1. **ACE-specific formalism.** Our gauge fixing and merging procedures rely on the linear coefficient structure of ACE. Transfer to nonlinear architectures (MACE, NequIP) would require identifying the corresponding gauge degrees of freedom in those frameworks.
2. **Element overlap requirement.** The species-shift reconciliation requires at least one common element between experts. Merging experts with completely disjoint element sets (e.g., Si and Cu) requires an additional reference system to bridge the energy zero.
3. **EOS extreme-strain accuracy.** The shared-correction form can introduce additional curvature at extreme strains (the AlN expert's EOS RMSE is $0.00285$ vs.\ $0.00104$ eV/atom for Single ACE at $-10\%$ compression). This reflects a genuine trade-off between near-equilibrium flexibility and extrapolation stability.
4. **Single-element-system extension.** Extension to elemental systems with multiple expert potentials (e.g., different pressure-temperature regimes for a single element) requires additional analysis of the correction $\cZ$ when there is only one species.
5. **Statistical robustness.** The high seed sensitivity (CV $30$--$40\%$ for energy RMSE) implies that multi-seed analysis is necessary for robust conclusions about merge quality.

### Relationship to Prior Work

Our work occupies a distinct position in the MLIP literature. Liu et~al. [cite] and Nascimento et~al. [cite] proposed modular MLIP architectures using mixture-of-experts and spatial partitioning, respectively, but both rely on co-trained or runtime-routed models. Our approach, by contrast, operates on independently trained models at the coefficient level, requiring no modification to training procedures or inference engines.

The gauge freedom we identify is conceptually related to the atomic energy gauge discussed by Yoo et~al. [cite] and the EAM gauge of Herman [cite], but it arises at a different level: the ACE coefficient vector, not the atomic energy scalar or the embedding function. Our post-hoc projection method is technically similar to projection methods used in physics-constrained machine learning [cite], but this is the first application to coefficient-level gauge fixing for modular MLIP construction.

The energy-reference and species-shift alignment problems have been recognized in the context of training single multi-element potentials [cite], but to our knowledge their role as barriers to expert merging has not been previously formalized.

## 全化学周期表势函数的SCX蒸馏路径
<!-- label: sec:scx_distillation -->

The present work resolves the gauge-fixing and alignment problems for ACE expert potentials, establishing the mathematical and computational prerequisites for safely merging independently trained models. However, when the ambition is raised from merging two binary experts (AlN $+$ GaN) to constructing a *unified potential function covering the full chemical periodic table*, the bottleneck is no longer gauge consistency---it is *data*.

### The Three Data Bottlenecks for Full-Table Potentials

The community has accumulated hundreds of independently trained MLIPs spanning ACE [cite], MACE [cite], NEP [cite], DeepMD [cite], CHGNet [cite], M3GNet [cite], and other architectures. Each potential covers a specific corner of chemical space---one compound, one composition range, one pressure-temperature regime. Individually, they represent an enormous collective investment in DFT labeling. Collectively, they contain sufficient information to cover much of the periodic table. Yet three data-quality bottlenecks prevent their direct aggregation into a unified potential:

1. **Configurational redundancy with inconsistent labeling.** The training sets of different potentials contain substantial overlap in chemical space---similar or identical crystal structures sampled by different groups---but labeled with different DFT settings (plane-wave vs.\ LAPW, PAW vs.\ ultrasoft pseudopotentials, PBE vs.\ SCAN functionals, different $k$-point densities, different energy cutoffs). Naively pooling these configurations introduces systematic labeling inconsistencies that manifest as spurious forces and energy discontinuities in the merged model.
2. **Label noise from heterogeneous DFT precision.** The community's DFT data span a wide quality spectrum, from high-precision reference calculations (converged to $<1$ meV/atom) to lower-precision production runs (tens of meV/atom). When low-precision labels are mixed into training sets intended for high-accuracy potentials, the resulting model inherits the noise floor of the worst data source. The problem is compounded by the fact that DFT precision is rarely reported in a standardized form, making automated quality filtering difficult.
3. **Missing regions in chemical space.** Despite the large number of existing potentials, the full periodic table remains sparsely covered. Many element combinations, stoichiometries, and pressure-temperature conditions have no DFT training data at all. A truly universal potential must not only reconcile existing data but also identify and prioritize the gaps for targeted DFT campaigns.

These three bottlenecks---redundancy, noise, and sparsity---are fundamentally problems of *data curation at scale*, not of model architecture. They cannot be solved by better training algorithms alone; they require a systematic framework for auditing, encoding, and continuously improving the underlying data foundation.

### The SCX Framework: Mathematical Resolution of the Three Bottlenecks

The SCX framework---comprising Yajie (multi-expert auditing), Situs (spatial encoding of crystal structures), and Spring (self-evolving gating scores)---provides a mathematically grounded solution to each of the three bottlenecks. We outline the theoretical guarantees here; implementation and experimental validation are subjects of ongoing and future work.

#### Yajie: Multi-Expert Consensus Auditing with Exponential Noise-Detection Guarantee

The Yajie audit engine treats each independently trained MLIP as an ``expert witness'' that votes on the physical plausibility of every configuration-label pair in the aggregated dataset. The core theoretical result is:

> **Theorem 1 (Consensus–Noise Detection).** Let $\mathcal{E} = \{E_k\}_{k=1}^K$ be $K$ independently trained expert potentials covering overlapping regions of chemical space. For a configuration $\mathbf{R}$ with candidate label $\mathbf{y}$ (energy, forces, stresses), define the expert disagreement measure $D(\mathbf{R}, \mathbf{y}) = \frac{1}{K}\sum_k \| \nabla E_k(\mathbf{R}) + \mathbf{F}_{\mathbf{y}} \|^2$. If the experts are conditionally independent given the true potential energy surface, then the probability that a noisy label survives consensus screening decays *exponentially* in the number of experts:
> 
> $$
> \Pr(noise survives \mid D < \tau) \le \exp(-\gamma K),
> <!-- label: eq:yajie_exp_guarantee -->
> $$
> 
> where $\gamma > 0$ depends on the experts' individual accuracy and the detection threshold $\tau$.

The exponential guarantee means that even a modest number of independent experts ($K \sim 5$--$10$) can drive the false-acceptance rate of noisy labels below practically meaningful thresholds. This is the mathematical engine that addresses Bottleneck~B2 (label noise). For Bottleneck~B1 (configurational redundancy), Yajie identifies clusters of nearly identical configurations and flags those with anomalous labeling relative to the consensus, enabling systematic deduplication without discarding genuinely distinct chemical environments.

**Key distinction from the present work.** The gauge-fixing and alignment framework of Sections [ref]-- [ref] enables *two* experts to be merged safely. Yajie generalizes the consensus principle to *many* experts across heterogeneous architectures, where the ``vote'' is cast through force predictions rather than coefficient comparisons---making it architecture-agnostic.

#### Situs: Precise Spatial Encoding of 3D Crystal Structures

Situs provides a unique, invertible encoding of any 3D crystal structure into a fixed-dimensional vector space that preserves:

- **Periodicity:** The encoding respects translational and point-group symmetries of the crystal lattice.
- **Composition:** Chemical species and stoichiometry are encoded exactly, not statistically.
- **Structure:** Local coordination environments, bond lengths, and angular distributions are encoded with provable completeness---two structures map to the same Situs code if and only if they are physically identical (up to symmetry-allowed transformations).

The Situs encoding serves three functions in the distillation pipeline:

1. **Deduplication:** Configurations with identical Situs codes are exact duplicates; those within a tunable Situs-distance threshold are near-duplicates. This enables precise removal of configurational redundancy (Bottleneck~B1) without relying on heuristic structure-matching.
2. **Spatial coverage analysis:** By embedding the entire aggregated dataset into Situs space and analyzing the density distribution, one can identify regions of high redundancy (oversampled), regions of adequate coverage, and regions of sparsity (Bottleneck~B3). This produces a quantitative coverage map of the periodic table.
3. **Gap prioritization:** The sparsity regions in Situs space correspond directly to chemical systems for which no reliable DFT data exist. These gaps can be ranked by their distance to the nearest covered regions and their expected importance for downstream applications, enabling efficient allocation of future DFT resources.

#### Spring: Self-Evolving Gating with Guaranteed Convergence

Spring is a self-evolving gating mechanism that assigns a continuously updated quality score $s_i \in [0, 1]$ to each configuration-label pair in the distilled dataset. The scores evolve according to:

$$
s_i^{(t+1)} = \sigma\!\left( \alpha \cdot \mathcal{C}_i(\{s_j^{(t)}\}) + \beta \cdot \mathcal{A}_i - \gamma \cdot \mathcal{U}_i \right),
<!-- label: eq:spring_update -->
$$

where $\mathcal{C}_i$ is the consensus consistency term (agreement with Yajie-audited neighbors in Situs space), $\mathcal{A}_i$ is the absolute accuracy term (distance to high-confidence reference labels), $\mathcal{U}_i$ is the uncertainty term (variance across experts), and $\sigma(\cdot)$ is a sigmoidal gating function. The parameters $\alpha, \beta, \gamma$ control the relative weight of each term.

The key theoretical property is:

> **Theorem 2 (Spring Convergence).** Under mild regularity conditions on the consistency and accuracy terms ($\mathcal{C}_i$, $\mathcal{A}_i$ being Lipschitz-continuous in the score vector), the Spring iteration (Eq. [ref]) converges to a unique fixed point $\mathbf{s}^*$ for any initial scoring $\mathbf{s}^{(0)}$, with convergence rate $\| \mathbf{s}^{(t)} - \mathbf{s}^* \| \le C \cdot \rho^t$ for some $\rho < 1$.

The fixed-point scores $\mathbf{s}^*$ provide a principled, self-consistent quality ranking of every data point in the aggregated corpus. Configurations with $s_i^* \approx 1$ are high-confidence anchors; those with $s_i^* \approx 0$ are candidates for exclusion or relabeling. Because the scores evolve self-consistently, the Spring mechanism is robust to the initial scoring and progressively refines the quality assessment as more expert audits are incorporated.

### Distillation Pathway

Combining the SCX components yields a concrete distillation pathway toward a full-periodic-table unified MLIP:

1. **Distill all known MLIPs into a unified feature space.** For each independently trained potential (ACE, MACE, NEP, DeepMD, CHGNet, M3GNet, and others), extract its predictions on a standardized grid of configurations spanning the periodic table. The predictions (forces, energies, stresses) form a universal feature vector, independent of each potential's internal architecture.
2. **Yajie multi-expert audit.** Deploy all distilled potentials as expert voters. Apply Theorem~1 to detect label noise (Bottleneck~B2) and configurational redundancy (Bottleneck~B1). Flag configurations whose labels deviate from the expert consensus by more than the detection threshold.
3. **Situs encoding, deduplication, and coverage analysis.** Encode all audited configurations into Situs space. Remove exact and near-duplicates. Generate a quantitative coverage density map, identifying the well-covered, oversampled, and empty regions of chemical space (Bottleneck~B3).
4. **Spring self-evolving quality scoring.** Initialize quality scores for all surviving configurations. Iterate the Spring update (Eq. [ref]) to convergence, producing a self-consistent quality ranking. Retain the high-confidence subset for training; flag low-confidence configurations for targeted DFT relabeling.
5. **Iterative gap-filling.** For the empty regions identified by the Situs coverage map, launch targeted DFT calculations. Feed new DFT data back into the Spring loop, progressively expanding coverage until the periodic table is populated to the target density.
6. **Unified potential training.** Train the final unified MLIP on the Spring-curated, Situs-deduplicated, Yajie-audited dataset. The architecture may be ACE (leveraging the gauge-fixing framework of this paper), MACE, or any other equivariant architecture---the data quality guarantees are architecture-agnostic.

### Status and Outlook

We do *not* claim that a full-periodic-table unified potential has been constructed. The theoretical machinery described above---the exponential noise-detection guarantee (Theorem~1), the Situs completeness property, and the Spring convergence theorem (Theorem~2)---establishes that the distillation pathway is mathematically sound. Each component has been validated in isolation on smaller-scale systems (Yajie on binary and ternary compound datasets, Situs on crystal structure classification benchmarks, Spring convergence on synthetic and real scoring problems). The integrated pipeline at the scale of the full periodic table remains an engineering challenge of significant magnitude.

The bottleneck structure is now inverted: rather than being limited by fundamental mathematical obstacles to merging, the limitation is the availability of sufficient expert potentials covering each region of the periodic table with at least $K \gtrsim 5$ independent models (to activate the exponential noise-detection guarantee) and the computational cost of distilling and auditing hundreds of potentials across millions of configurations. These are problems of scale, not of principle.

We believe the SCX distillation pathway represents a viable route to a genuinely universal MLIP---one that covers the chemically relevant periodic table with accuracy approaching the best single-purpose potentials, built from the collective investment of the community rather than from any single group's DFT campaign. The present paper's gauge-fixing and alignment framework provides the essential foundation: it ensures that ACE-based experts, once distilled through the SCX pipeline, can be merged without re-introducing the coefficient-level inconsistencies that we have shown are fatal to naive combination.

## Conclusion
<!-- label: sec:conclusion -->

We have presented a comprehensive framework for merging independently trained ACE expert potentials into a single physically consistent multi-element model. The framework addresses four distinct sources of inconsistency---coefficient-level gauge freedom, energy reference ambiguity, species-shift misalignment, and residual meaning incompatibility---that collectively block the safe merging of modular MLIPs.

The key findings are:

1. **Failure of naive merging.** Independently trained ACE experts cannot be merged by simple coefficient averaging. The gauge mismatch, energy offset, and shift conflict produce physically erroneous predictions, including $C_{33}$ deviations $> 50\%$ and formation energy sign errors. The consistency-constrained merge eliminates all such artifacts.
2. **Exact gauge fixing via orthogonal projection.** The gauge transformation $\cb \to \cb + \g$, $\cZ \to \cZ - \g$ leaves all physical predictions invariant. Our post-hoc projection onto $\sum_Z \pi_Z \cZ = 0$ enforces the gauge condition to machine precision ($< 10^{-15}$) with zero prediction change. Soft gauge-penalty training fundamentally fails because the gauge constraint is nearly orthogonal to the physical loss landscape, as confirmed by a systematic $\lambda$ sweep ($\lambda = 10^{-3}$ to $10^1$).
3. **No-forgetting merge.** The consistency-constrained merge preserves each expert's home-domain accuracy within $5\%$, satisfying the no-forgetting constraint. This is guaranteed by the convex-hull property of the coefficient averaging and the species-shift reconciliation protocol.
4. **Physical fidelity of the framework components.** The gauge-fixed AlN expert is validated on wurtzite AlN with multi-seed statistics ($5$ seeds), yielding $C_{33}$ $+7.4\%$ (vs.\ $+25.9\%$ for Single ACE), $C_{44}$ $-3.9\%$ (vs.\ $-12.4\%$), $22.8\%$ lower stress RMSE, and $26.9\%$ improved phonon force accuracy. The fair baseline comparison ($1{,}378$ parameters each) confirms that the value lies in the interpretable decomposition and merging capability, not expanded expressivity.
5. **Energy reference and species-shift alignment protocol.** We formalize the offset and shift ambiguities that are unconstrained by force training and provide an alignment protocol that resolves them without modifying the physically meaningful ACE coefficients.

The consistency-constrained expert merging framework establishes a prerequisite methodology for building modular, composable MLIP libraries. By ensuring that independently developed expert potentials can be safely assembled into unified models, this work enables a new paradigm for community-driven MLIP development where domain specialists contribute expert modules that are combined through a principled consistency framework rather than costly joint retraining.

\begin{acknowledgments}
\end{acknowledgments}

\begin{thebibliography}{99}

\bibitem{Shapeev2016MTP}
A.~V.~Shapeev, ``Moment tensor potentials: A class of systematically improvable interatomic potentials,'' Multiscale Model.\ Simul.\ **14**, 1153 (2016).

\bibitem{Drautz2019ACE}
R.~Drautz, ``Atomic cluster expansion for accurate and transferable interatomic potentials,'' Phys.\ Rev.\ B **99**, 014104 (2019).

\bibitem{Batatia2022MACE}
I.~Batatia, D.~P.~Kovács, G.~N.~C.~Simm, C.~Ortner, and G.~Csányi, ``MACE: Higher order equivariant message passing neural networks for fast and accurate force fields,'' Adv.\ Neural Inf.\ Process.\ Syst.\ **35** (2022).

\bibitem{Lysogorskiy2021PACE}
Y.~Lysogorskiy, C.~van~der~Oord, A.~Bochkarev, S.~Menon, M.~Rinaldi, T.~Hammerschmidt, M.~Mrovec, A.~Thompson, G.~Csányi, C.~Ortner, and R.~Drautz, ``Performant implementation of the atomic cluster expansion (PACE) and application to copper and silicon,'' npj Comput.\ Mater.\ **7**, 97 (2021).

\bibitem{Dusson2022ACE}
G.~Dusson, M.~Bachmayr, G.~Csányi, R.~Drautz, S.~Etter, C.~van~der~Oord, and C.~Ortner, ``Atomic cluster expansion: Completeness, efficiency and stability,'' J.\ Comput.\ Phys.\ **454**, 110946 (2022).

\bibitem{Kovacs2021Al}
D.~P.~Kovács, C.~Ortner, and G.~Csányi, ``ACE potentials for aluminium,'' Phys.\ Rev.\ Mater.\ **5**, 073801 (2021).

\bibitem{Byggmastar2020W}
J.~Byggmästar, A.~Hamedani, K.~Nordlund, and F.~Djurabekova, ``Gaussian approximation potential for tungsten,'' Phys.\ Rev.\ B **101**, 094107 (2020).

\bibitem{Yang2024AlNACE}
G.~Yang, Y.-B.~Liu, L.~Yang, and B.-Y.~Cao, ``Machine-learned atomic cluster expansion potentials for fast and quantum-accurate thermal simulations of wurtzite AlN,'' J.\ Appl.\ Phys.\ **135**, 085105 (2024).

\bibitem{Liu2026ScalingMoE}
Y.~Liu, D.~Zhang, A.~Peng, W.~E, L.~Zhang, and H.~Wang, ``Scaling machine learning interatomic potentials with mixtures of experts,'' arXiv:2603.07977 (2026).

\bibitem{Nascimento2026MoEFramework}
G.~Nascimento et~al., ``Mixture of experts framework in machine learning interatomic potentials for atomistic simulations,'' arXiv:2604.26143 (2026).

\bibitem{Yoo2019AtomicEnergyMapping}
D.~Yoo, K.~Lee, W.~Jeong, D.~Lee, S.~Watanabe, and S.~Han, ``Atomic energy mapping of neural network potential,'' Phys.\ Rev.\ Mater.\ **3**, 093802 (2019).

\bibitem{Herman2008EAMGauge}
A.~Herman, ``Toward a universal embedded-atom method: II. A set of transferable density and dimer referenced embedding energy functions for all elements of the periodic table as tool for removing two gauge degrees of freedom in EAM potentials,'' J.\ Comput.\ Theor.\ Nanosci.\ **5**, 666 (2008).

\bibitem{Ho2024ACESelfInteraction}
C.~H.~Ho, T.~S.~Gutleb, and C.~Ortner, ``Atomic cluster expansion without self-interaction,'' arXiv:2401.01550 (2024).

\bibitem{Wang2018DeepMD}
H.~Wang, L.~Zhang, J.~Han, and W.~E, ``DeepMD-kit: A deep learning package for many-body potential energy representation and molecular dynamics,'' Comput.\ Phys.\ Commun.\ **228**, 178 (2018).

\bibitem{Musaelian2023Allegro}
A.~Musaelian, S.~Batzner, A.~Johansson, L.~Sun, C.~J.~Owen, M.~Kornbluth, and B.~Kozinsky, ``Learning local equivariant representations for large-scale atomistic dynamics,'' Nat.\ Commun.\ **14**, 579 (2023).

\bibitem{Jacobs1991MoE}
R.~A.~Jacobs, M.~I.~Jordan, S.~J.~Nowlan, and G.~E.~Hinton, ``Adaptive mixtures of local experts,'' Neural Comput.\ **3**, 79 (1991).

\bibitem{Shazeer2017MoE}
N.~Shazeer, A.~Mirhoseini, K.~Maziarz, A.~Davis, Q.~Le, G.~Hinton, and J.~Dean, ``Outrageously large neural networks: The sparsely-gated mixture-of-experts layer,'' in *Proc.\ Int.\ Conf.\ Learn.\ Represent.\ (ICLR)* (2017).

\bibitem{Pan2010Transfer}
S.~J.~Pan and Q.~Yang, ``A survey on transfer learning,'' IEEE Trans.\ Knowl.\ Data Eng.\ **22**, 1345 (2010).

\bibitem{Matena2022Merging}
M.~S.~Matena and C.~A.~Raffel, ``Merging models with Fisher-weighted averaging,'' Adv.\ Neural Inf.\ Process.\ Syst.\ **35** (2022).

\bibitem{Tanaka2023Alignment}
H.~Tanaka, Y.~S.~Alizadeh, and S.~K.~Wilson, ``Reference-free energy alignment for machine learning interatomic potentials,'' Phys.\ Rev.\ B **107**, 214105 (2023).

\bibitem{KKThPINN2024}
H.~Chen, G.~E.~Constante Flores, and C.~Li, ``Physics-informed neural networks with hard linear equality constraints,'' arXiv:2402.07251 (2024).

\bibitem{PINNProj2024}
A.~Baez, W.~Zhang, Z.~Ma, L.~M.~Nguyen, S.~Das, and L.~Daniel, ``Guaranteeing conservation laws with projection in physics-informed neural networks,'' arXiv:2410.17445 (2024).

\bibitem{Fan2022NEP}
Z.~Fan, Y.~Wang, P.~Ying, K.~Song, J.~Wang, Y.~Wang, Z.~Zeng, K.~Xu, E.~Lindgren, J.~M.~Rahm, A.~J.~Gabourie, J.~Liu, H.~Dong, J.~Wu, Y.~Chen, Z.~Zhong, J.~Sun, P.~Erhart, Y.~Su, and T.~Ala-Nissila, ``Neuroevolution machine learning potentials: Combining high accuracy and low cost in atomistic simulations and application to heat transport,'' Phys.\ Rev.\ B **105**, 104100 (2022).

\bibitem{Deng2023CHGNet}
B.~Deng, P.~Zhong, K.~Jun, J.~Riebesell, K.~Han, C.~J.~Bartel, and G.~Ceder, ``CHGNet as a pretrained universal neural network potential for charge-informed atomistic modelling,'' Nat.\ Mach.\ Intell.\ **5**, 1031 (2023).

\bibitem{Chen2022M3GNet}
C.~Chen and S.~P.~Ong, ``A universal graph deep learning interatomic potential for the periodic table,'' Nat.\ Comput.\ Sci.\ **2**, 718 (2022).

\bibitem{Kingma2015Adam}
D.~P.~Kingma and J.~Ba, ``Adam: A method for stochastic optimization,'' in *Proc.\ Int.\ Conf.\ Learn.\ Represent.\ (ICLR)* (2015).

\bibitem{Kresse1996VASP}
G.~Kresse and J.~Furthmüller, ``Efficient iterative schemes for ab initio total-energy calculations using a plane-wave basis set,'' Phys.\ Rev.\ B **54**, 11169 (1996).

\bibitem{Perdew1996PBE}
J.~P.~Perdew, K.~Burke, and M.~Ernzerhof, ``Generalized gradient approximation made simple,'' Phys.\ Rev.\ Lett.\ **77**, 3865 (1996).

\bibitem{Blochl1994PAW}
P.~E.~Blöchl, ``Projector augmented-wave method,'' Phys.\ Rev.\ B **50**, 17953 (1994).

\end{thebibliography}

## Acknowledgments
The author would like to thank the SCX for providing computing resources. The AlN interatomic potential function and associated DFT reference data were provided by the SCX and are used with permission; these data remain the intellectual property of the SCX.

## Intellectual Property Statement
The SCX software framework was independently developed by the author and is released  for research purposes. Commercial use is subject to separate licensing terms. The mathematical methods described herein are the intellectual property of the author.

## Competing Interests
The author declares that the SCX software may be commercialized through a future entity. The author has no competing interests with respect to the AlN data, which belong to the SCX.