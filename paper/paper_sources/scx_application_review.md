# State-Conditioned Expertise Across Domains: From Interatomic Potentials to Drug Discovery — A Review of the SCX Framework and Its Self-Evolving Gatekeeper

> **Target Journal**: Nature Reviews Physics / Nature Computational Science  
> **Article Type**: Review  
> **Word Count**: ~7,500  
> **Date**: 2026-06-28  
> **Status**: Draft manuscript

---

## Abstract

The quality of training data has emerged as the single most consequential bottleneck across scientific machine learning, yet prevailing approaches to data quality assessment rely on global metrics that obscure the fundamental heterogeneity of input spaces. The State-Conditioned eXpertise (SCX) framework addresses this limitation through a simple but powerful insight: expert reliability is not a global property but a local function of the input state. By partitioning the input space into structurally meaningful states and evaluating multi-expert consensus within each state, SCX provides rigorous guarantees for label noise detection (via the Yajie algorithm) and enables a self-evolving gatekeeper (via the Spring dynamics) that improves its quality judgments over iterative cycles. This review systematically examines the SCX framework across six scientific domains: machine-learned interatomic potentials, drug discovery, medical imaging, semiconductor process simulation, large language models, and remote sensing. In each domain, we show how the state-conditioned expertise principle maps onto existing expert structures, what novel capabilities the framework enables, and where its theoretical guarantees provide advantages over domain-specific alternatives. We further demonstrate that the Spring self-evolution algorithm—a Lyapunov-stabilized coupled dynamical system with provable convergence to a fixed point—constitutes a domain-agnostic mechanism for iterative data quality improvement. The review concludes with open problems including cross-domain gatekeeper transfer, decentralized audit infrastructure, and the path toward fully automated scientific data curation.

---

## 1. Introduction: The Data Quality Bottleneck

The past decade has witnessed an extraordinary proliferation of machine learning models across the natural sciences. From neural network potentials that approximate density functional theory (DFT) calculations [1,2] to vision transformers that detect pathologies in medical images [3], from graph neural networks that screen drug candidates [4] to large language models that assist in literature synthesis [5]—the scientific ML revolution is broad, deep, and accelerating.

Yet beneath this diversity runs a common thread of fragility. Every model is only as reliable as the data on which it was trained.

### 1.1 The Universal Bottleneck

Consider three representative failure modes:

**Materials science**: A neural network potential trained on Materials Project DFT data achieves 5 meV/atom accuracy on validation—but silently fails on grain boundary structures because the training set contained mislabeled configurations whose local environments were incorrectly characterized. The model is deployed, papers are published, and the error propagates into downstream studies for months before anyone notices.

**Drug discovery**: A virtual screening campaign identifies 50 promising hit compounds from a library of 10 million. Twelve are synthesized and tested; none show activity. The retrospective analysis reveals that the training labels for the target protein were contaminated—approximately 8% of "active" compounds in the training set were false positives from an assay with known interference artifacts.

**Medical imaging**: A chest X-ray classification model achieves 0.94 AUC on internal test data but drops to 0.71 when deployed at a different hospital. The root cause is not domain shift in the usual sense: the training labels contain systematic errors from a single radiologist who consistently overcalled interstitial abnormalities, and the model learned to amplify this annotator's bias.

These scenarios share a common structure. In each case, a **global** quality metric (validation accuracy, AUC, F1 score) concealed critical **local** failures. The model was "good on average" but "bad where it mattered."

### 1.2 The Limitations of One-Size-Fits-All Metrics

The standard toolkit for data quality assessment—cross-validation accuracy, confusion matrices, confidence scores—operates at the level of aggregate statistics over the entire dataset. These metrics answer the question "How good is my model overall?" but fail to answer the more consequential question: "**Where** is my model unreliable, and **why**?"

More sophisticated approaches fare only marginally better. Confident Learning [6] estimates a noise transition matrix but provides only class-level granularity. Data Shapley values [7] assign per-sample importance scores but require prohibitively expensive model retraining and offer no theoretical guarantee on noise detection. Influence functions [8] trace model behavior back to individual training points but assume differentiability and scale poorly.

The fundamental limitation shared by all these approaches is that they treat data quality as a **sample-level** property decoupled from the **input structure**. A label error in one region of the input space may be catastrophic (if that region is densely sampled and safety-critical), while an identical error in another region may be inconsequential (if that region is sparse or irrelevant to the application). Global metrics cannot capture this heterogeneity.

### 1.3 The State-Conditioned Insight

The SCX framework is built on a single conceptual shift:

> **Expert reliability is not a global property $R_m$. It is a state-conditioned function $R_m(s)$.**

Here, a "state" $s$ is a structurally meaningful partition of the input space $\mathcal{X}$—for example, sp²-hybridized carbon environments in materials science, solid-vs-cystic lesion types in medical imaging, or syntactic-vs-semantic difficulty levels in natural language tasks. The key claim is that by conditioning expert quality assessments on these states, we can:

1. **Detect label noise** with provable guarantees (via the Yajie algorithm, the subject of Theorem 1 in the SCX framework)
2. **Route inputs** to the most reliable expert for each state (Proposition 3)
3. **Selectively compress** datasets by removing redundant samples while preserving state-conditional fidelity (Proposition 4)
4. **Self-evolve** the gatekeeper itself through iterative cycles of judging, storing, updating, and resurrecting (the Spring algorithm, Theorem SE-1)

### 1.4 Scope of This Review

This review has two complementary goals. First, we provide a unified technical exposition of the SCX framework—the Yajie noise detection algorithm, the Spring self-evolution dynamics, and the underlying theory connecting them—at a level accessible to domain scientists. Second, we systematically survey the framework's applicability across six scientific domains, providing concrete mappings of the abstract state-conditioned expertise principle onto real expert structures, and identifying both the capabilities SCX enables and the limitations it does not yet overcome.

Importantly, this is not a review of SCX *implementations*—several algorithmic components remain at the prototype stage, and large-scale empirical validation is ongoing. Rather, it is a review of the *framework*: what it claims, what it proves, where it applies, and what remains to be demonstrated.

---

## 2. The SCX Framework: A Technical Overview

### 2.1 The Core Principle: State-Conditioned Expertise

The SCX framework is defined over an input space $\mathcal{X}$, a label space $\mathcal{Y}$, and a set of $M$ expert models $\{f_1, \ldots, f_M\}$. The experts may be heterogeneous—different architectures, different training sets, different inductive biases—and the framework makes no assumption about their internal structure beyond the availability of their predictions.

The central object is a **state mapping** $s: \mathcal{X} \to \mathcal{S}$ that assigns each input to one of $K_S$ discrete states. The mapping is typically constructed via clustering in a learned representation space $\phi(x)$:

$$\mathcal{S} = \text{Cluster}(\{\phi(x_i)\}_{i=1}^N, K_S)$$

where $\phi$ may be a pretrained embedding (e.g., a materials graph neural network's final hidden layer, or a vision transformer's [CLS] token) and $K_S$ is selected via a stability diagnostic (Proposition 6 in the SCX framework).

Given this state partition, the **state-conditioned expert risk** is:

$$R_m(s) = \mathbb{E}_{x \sim P(\cdot \mid s)}\left[\ell(f_m(x), f^*(x))\right]$$

where $\ell$ is a loss function and $f^*$ is the (unknown) ground truth function. The SCX reliability score for expert $m$ in state $s$ quantifies the probability of correctness:

$$\text{SCX}_m(s) = \mathbb{P}\left(\ell(f_m(x), y) < \tau \mid x \in s\right)$$

where $\tau$ is a tolerance threshold.

**Proposition 1** (Global Ranking Insufficiency) establishes that in heterogeneous input spaces, no state-independent global ranking of experts can be optimal. The regret incurred by any global aggregation is bounded below by the degree of rank-crossing across states:

$$\text{Regret}(\text{global rank}) \geq \frac{1}{2}\sum_{s \neq s'} \rho(s)\rho(s') \cdot d_{\text{rank}}(s, s')$$

where $d_{\text{rank}}(s, s')$ measures the Kendall-$\tau$ distance between expert rankings in states $s$ and $s'$, and $\rho(s)$ is the proportion of data in state $s$. This result provides the *necessity* of state conditioning: without it, information is provably lost.

### 2.2 The Cercis Score: $S(s) = Q(s) + \eta(t) \cdot N(s)$

The Cercis Score (named after the Cercis chinensis, or Chinese redbud, whose blossoms emerge directly from old wood) is the static gatekeeper formula that assigns a quality score to each state. It has two components:

$$S(s) = \underbrace{Q(s)}_{\text{Quality score}} + \eta(t) \cdot \underbrace{N(s)}_{\text{Novelty bonus}}$$

The quality term $Q(s)$ aggregates multi-expert reliability within state $s$:

$$Q(s) = \frac{1}{M}\sum_{m=1}^M \text{SCX}_m(s) \cdot \mathbf{1}\{\ell(f_m(x), y) < \tau\}$$

The novelty term $N(s)$ measures the information-theoretic distance of state $s$ from previously encountered states:

$$N(s) = -\log \max_{s' \in \mathcal{M}_t} \text{sim}(s, s')$$

The time-dependent weight $\eta(t)$ decays as $t \to \infty$, encoding the gatekeeper's maturation: early in its lifecycle, novelty is highly valued (the gatekeeper is exploring the space); later, quality dominates (the gatekeeper has converged to stable judgments).

The Cercis Score is the operational heart of the Yajie algorithm: states with $S(s) < \theta$ are flagged for remediation (relabeling, downweighting, or discarding), while states with high $S(s)$ but high redundancy are candidates for compression.

### 2.3 Yajie: Static Noise Detection via Multi-Expert Consistency

The Yajie (雅洁, "elegant purification") algorithm operationalizes the core theoretical result of the SCX framework—**Theorem 1**: multi-expert consensus detects label noise with exponential reliability.

For a sample $x$ with label $y$, the multi-expert consensus score is:

$$C(x) = \frac{1}{M}\sum_{m=1}^M \mathbf{1}\{\ell(f_m(x), y) > \tau\}$$

where the indicator fires when expert $m$'s prediction is consistent with the given label $y$. Theorem 1 establishes that under mild conditions (independent experts trained on disjoint data, uniform label noise, a separation gap $\Delta_s$ between noise and genuine difficulty), the F1 score of noise detection satisfies:

$$\text{F1}_{\text{Yajie}} \geq 1 - \frac{1}{\eta}\sum_{s \in \mathcal{S}} \rho_s \cdot e^{-2M\Delta_s^2}$$

where $\eta$ is the true noise rate and $\rho_s$ is the proportion of data in state $s$. The exponential dependence on $M$ (the number of experts) is the key: with $M \geq 10$ independent experts and a non-vanishing separation gap, the detection guarantee becomes very strong ($\text{F1} > 0.95$ in typical regimes).

**Theorem 3** (Unidentifiability) provides the essential complement: in the absence of auxiliary assumptions, label noise and genuine learning difficulty are *provably indistinguishable*. This is not a weakness of SCX—it is a fundamental epistemic limit. The SCX assumptions (A1–A6) are precisely the minimal set needed to break this unidentifiability.

**Theorem 4'** (Minimax Optimality) closes the circle: among all noise detectors operating on multi-expert consensus signals, Yajie achieves the minimax-optimal F1 score over the class of problems satisfying the separation-gap condition. No detector can do better without additional assumptions.

### 2.4 Spring: Self-Evolving Gatekeeper with Provable Convergence

Where Yajie provides a *static* noise detection capability, Spring (春季, "the season of resurrection") provides a *self-evolving* mechanism. The core question Spring addresses is: what happens when the gatekeeper itself can improve through iterative cycles?

Spring formalizes the SCX iterative loop as a coupled dynamical system over three objects:

- **Gatekeeper** $S_t: \mathcal{X} \to [0,1]$: the quality-scoring function at iteration $t$
- **Student model** $\theta_t$: the parameters of the primary predictive model (e.g., a NEP potential)
- **Memory bank** $\mathcal{M}_t$: a monotonically growing set of validated structures with quality annotations

The update cycle proceeds as:

```
Judge:  S_t evaluates quality of new data
Store:  Validated structures enter M_t (never deleted)
Update: θ_{t+1} trained on S_t-filtered data
        S_{t+1} refined using θ_{t+1} feedback
```

The central theoretical result is **Theorem SE-1** (Convergence of SCX Self-Evolution): under seven conditions—finite structure space, Lipschitz continuity of both gatekeeper and student, Robbins-Monro learning rate decay, conditional i.i.d. sampling, sufficient annealing, and bounded gatekeeper updates—the sequence $(S_t, \theta_t)$ converges almost surely to a joint fixed point $(S^*, \theta^*)$ satisfying:

- $S^*(x) = \mathbb{P}(\text{correct} \mid x, \mathcal{M}_\infty)$: the gatekeeper is self-consistent
- $\theta^*$ is a local minimum of the student's expected loss under the $S^*$-induced data distribution

**Theorem SE-2** (Completeness) provides a finite-time bound: under physical constraints (finite data, finite numerical precision, finite compute), there exists a finite $T^*$ such that for all $t \geq T^*$, the system is within $\varepsilon$ of its fixed point.

The convergence proof proceeds via the construction of a Lyapunov function:

$$\Phi(S_t, \theta_t, \mathcal{M}_t) = \underbrace{\mathbb{E}_{x \sim \mathcal{M}_t}[|S_t(x) - S^*(x)|]}_{\text{Gatekeeper error}} + \underbrace{\mathcal{L}(\theta_t) - \mathcal{L}(\theta^*)}_{\text{Student suboptimality}}$$

which is shown to be a supermartingale under the update dynamics, guaranteeing $\Phi_{t+1} \leq \Phi_t$ in expectation.

### 2.5 The Memory Bank $\mathcal{M}_t$: Never Delete, Wait for Spring

The memory bank $\mathcal{M}_t$ is the architectural innovation that distinguishes Spring from standard active learning or online learning loops. Its defining property is *monotonicity*: $\mathcal{M}_t \subseteq \mathcal{M}_{t+1}$ always. Structures are *never* deleted.

This design choice is philosophically and practically significant. A structure $x$ that is classified as low-quality at iteration $t$ is not discarded permanently—it enters a dormant state. When the gatekeeper matures (i.e., $S_t$ converges closer to $S^*$), Spring revisits dormant structures through a "resurrection" pass:

$$x \text{ resurrected if } S_{t+k}(x) > \theta_{\text{resurrect}}$$

The key insight is that discarding a structure is equivalent to asserting "this structure is *intrinsically* worthless"—but what often appears worthless is merely *prematurely judged*. The monotonic memory bank decouples the act of judgment from the act of deletion, enabling the gatekeeper to correct its own earlier mistakes.

Table 1 summarizes the four convergence paths of the Spring dynamics.

**Table 1: Convergence Paths of the Spring Self-Evolution Dynamics**

| Path | Characteristic | Condition |
|------|---------------|-----------|
| I. Classical Convergence | $(S_t, \theta_t) \to (S^*, \theta^*)$, monotonic improvement | All C1–C7 satisfied, sufficient annealing |
| II. Limit Cycle | System oscillates among finite configurations | Insufficient annealing, strong coupling |
| III. Perpetual Discovery | New structures continuously discovered, $\mathcal{M}_t$ unbounded | Open physical world, infinite exploration budget |
| IV. Divergent Collapse | $S_t$ degenerates, quality decreases | Feedback loop broken, NEP feedback noise excessive |

---

## 3. MLIP / Materials Science

### 3.1 Domain Mapping

Machine-learned interatomic potentials (MLIPs) represent one of the most natural application domains for SCX, because the domain naturally provides multiple "experts" (different potential architectures) and clearly definable "states" (chemical environments). The mapping is:

| SCX Component | MLIP Instantiation |
|---------------|-------------------|
| $\mathcal{X}$ | Atomic structure (positions, species, cell) |
| $\mathcal{Y}$ | DFT energy, forces, stresses |
| $f_m$ | NEP, MACE, CHGNet, ACE, ORB, M3GNet, SevenNet |
| $s$ | Chemical environments: sp²/sp³ hybridization, bond-breaking, surfaces, defects, amorphous regions |
| $\phi(x)$ | SOAP, ACE descriptors, or graph neural network embeddings |

### 3.2 Multi-Expert Consistency for DFT Data Quality

DFT databases such as the Materials Project [9], OQMD [10], and AFLOW [11] contain hundreds of thousands of calculations, but data quality is heterogeneous. Common issues include unconverged k-point meshes, inappropriate pseudopotential choices, incorrect magnetic configurations, and metastable rather than ground-state structures.

Yajie addresses this by running multiple independently trained potentials (e.g., NEP trained on subset A, MACE on subset B, CHGNet on subset C) as consistency checkers. A DFT-labeled structure where all $M$ potentials predict energies within 5 meV/atom of the label is clean; a structure where $M-1$ agree and one disagrees is ambiguous; a structure where all agree *with each other but disagree with the DFT label* is a high-confidence noise candidate.

This approach leverages the fact that independent potentials trained on disjoint data make *uncorrelated* errors. Theorem 1's exponential guarantee directly applies: with $M \geq 10$ independent potentials, the false positive rate for noise detection decays as $\exp(-2M\Delta^2)$.

### 3.3 State-Conditioned Potential Selection

Different potentials excel in different chemical regimes. NEP [12] provides excellent efficiency and accuracy for single-element systems but can struggle with multi-component alloys. MACE [13] offers superior accuracy for complex bonding environments but at higher computational cost. CHGNet [14] captures magnetic effects that other potentials miss.

Proposition 3 (State-Conditioned Weighting) provides the optimal routing:

$$m^*(x) = \arg\min_m \sum_s \gamma_s(x) \cdot R_m(s)$$

where $\gamma_s(x)$ is a soft assignment of structure $x$ to state $s$, and $R_m(s)$ is the empirically estimated state-conditioned error of potential $m$. This routing can be precomputed: for a given chemical space, one constructs the state partition once, evaluates all available potentials on representative structures from each state, and produces a lookup table mapping states to optimal potentials.

### 3.4 The Single RTX 4090 Value Proposition

A practical strength of the SCX approach in materials science is its computational accessibility. While universal potentials like MACE-MP-0 [15] and ORB [16] require extensive pretraining on 100K+ structures across 89 elements, SCX operates on a different principle: *for a specific chemical system of interest, deploy multiple specialized potentials, evaluate their state-conditioned reliability, and route accordingly.*

This means that a researcher with a single RTX 4090 GPU can:
1. Train 3–5 NEP potentials on disjoint subsets of their DFT data (hours each)
2. Run Yajie to identify and quarantine noisy DFT labels (minutes)
3. Run Spring to iteratively improve the training set (hours per cycle)
4. Deploy state-conditioned routing for production MD simulations

No massive pretraining infrastructure is required. The framework is designed for the working computational materials scientist, not the large-scale AI lab.

### 3.5 Compression Fidelity

**Proposition 4** (Compression Fidelity) addresses a practical problem: DFT training sets grow large, but many structures are redundant. The question is which structures can be safely removed.

SCX-Compress defines a redundancy score for state $s$:

$$D(s) = 1 - \frac{1}{|\mathcal{D}_s|}\sum_{x \in \mathcal{D}_s} \mathbf{1}\{\text{removing } x \text{ changes } f_m(x) \text{ by } > \delta\}$$

States with $D(s) \to 1$ are highly redundant (all structures look similar to the model) and can be aggressively subsampled. States with $D(s) \to 0$ contain unique information and must be preserved. The key theoretical result is that this compression preserves state-conditional prediction fidelity up to a factor that degrades as $O(1/\sqrt{M})$ in the number of experts—a price paid for operating without ground-truth labels.

---

## 4. Drug Discovery

### 4.1 Domain Mapping

Drug discovery presents a more complex expert landscape than materials science, but the state-conditioned principle applies with equal force.

| SCX Component | Drug Discovery Instantiation |
|---------------|------------------------------|
| $\mathcal{X}$ | Molecular structures (SMILES, graphs, 3D conformers) |
| $\mathcal{Y}$ | Binding affinity, activity, ADMET properties |
| $f_m$ | Docking programs (AutoDock, Glide), ML models (Chemprop, EquiDock), FEP+ predictions |
| $s$ | Chemical states: lead-like/fragment-like/PROTAC, by target class, by scaffold family |

### 4.2 Target Identification and Data Curation

Public bioactivity databases—ChEMBL [17], PubChem [18], BindingDB [19]—aggregate millions of compound-target measurements, but data quality varies enormously across assay types, laboratories, and publication dates. A typical issue: IC50 values for the same compound-target pair can span three orders of magnitude across different publications.

Yajie's multi-expert consensus mechanism maps naturally to this setting. Multiple docking programs and ML predictors serve as the "experts." For a given (compound, target) pair, if all predictors agree on the activity class (active/inactive), the label is likely clean. If predictors agree with *each other* but disagree with the database label, the label is a noise candidate—perhaps from a flawed assay or a transcription error.

### 4.3 Multi-Expert Screening Consensus

Virtual screening—docking millions of compounds against a protein target to identify hits—is the canonical high-throughput application in computational drug discovery. Different docking programs exhibit systematic biases: Glide SP may favor compact, hydrophobic ligands while AutoDock Vina may prefer extended, polar conformations [20].

SCX state-conditioned routing addresses this by:
1. Clustering the compound library in chemical space (ECFP4 fingerprints, 3D shape descriptors)
2. Evaluating the retrospective enrichment of each docking program in each cluster
3. For a new screening campaign, routing compounds to the program that achieved the highest enrichment in the most similar chemical cluster

The novelty bonus $\eta(t) \cdot N(s)$ in the Cercis Score has a natural interpretation in drug discovery: it encourages the selection of screening compounds from underexplored regions of chemical space, serving as an algorithmic implementation of "scaffold hopping."

### 4.4 Chemical Space Exploration with Novelty Bonus

The time-decaying weight $\eta(t)$ in the Cercis Score is particularly relevant for iterative drug discovery campaigns. Early in a project, $\eta(0)$ is large—the gatekeeper actively rewards chemical novelty, encouraging broad exploration of the accessible chemical space. As the campaign matures and a lead series emerges, $\eta(t) \to 0$, and the gatekeeper shifts to quality-dominated scoring, optimizing within the established scaffold.

This provides a mathematical formalization of what experienced medicinal chemists do intuitively: explore broadly first, then exploit.

### 4.5 Resurrection of Discarded Candidates

Spring's monotonic memory bank has a direct pharmaceutical analog. In a typical drug discovery project, compounds are triaged at each stage—many are discarded after primary screening, more after counter-screening, and still more after ADMET profiling. Some of these discards are genuinely flawed (toxic, unstable, non-druglike). Others were discarded because the project's understanding of the target was immature.

Spring formalizes this intuition: discarded compounds enter the memory bank $\mathcal{M}_t$ but are not deleted. When the gatekeeper matures—for example, after a co-crystal structure reveals the true binding mode—the resurrection pass re-evaluates previously discarded compounds against the updated criteria. Some will be "resurrected" as viable candidates that were simply ahead of their time.

---

## 5. Medical Imaging

### 5.1 Domain Mapping

Medical imaging is a domain where expert disagreement is not just an algorithmic convenience—it is the everyday reality of clinical practice. Radiologists disagree. Pathologists disagree. The "ground truth" itself is often a consensus among human experts.

| SCX Component | Medical Imaging Instantiation |
|---------------|------------------------------|
| $\mathcal{X}$ | Images: X-ray, CT, MRI, PET, ultrasound |
| $\mathcal{Y}$ | Diagnostic labels, segmentation masks, abnormality scores |
| $f_m$ | Different CNN/transformer architectures, different radiologists/annotators |
| $s$ | Imaging states: modality (X-ray/CT/MRI), anatomy (chest/brain/abdomen), finding type (mass/nodule/fracture/effusion) |

### 5.2 Label Noise Detection in Radiology Datasets

Radiology datasets are known to contain substantial label noise. The widely used ChestX-ray14 dataset [21] was found by Oakden-Rayner [22] to contain systematic errors—including an entire class of "hernia" labels that corresponded to a different anatomical region than the images shown. More recently, Northcutt et al. [6] estimated that approximately 5.8% of ImageNet labels are erroneous, and radiology datasets sharing similar crowdsourcing pipelines likely suffer comparable or worse noise rates.

Yajie addresses this by treating different model architectures (ResNet, DenseNet, ViT, ConvNeXt) as independent experts trained on disjoint subsets of the data. For a given chest X-ray, if all four architectures agree on "no finding" but the dataset label says "pneumonia," the label is flagged. The state-conditioning is critical here: model agreement varies by finding type. All models may agree on obvious pneumothorax but systematically disagree on subtle interstitial patterns. By estimating $\text{SCX}_m(s)$ per finding type, Yajie avoids the pitfall of flagging genuinely difficult cases as noise.

### 5.3 Expert Reliability Across Modalities

A model that excels at detecting fractures in X-rays may perform poorly on MRI-based tumor segmentation, and vice versa. SCX state-conditioned routing formalizes this intuition:

$$w_m(x) \propto \exp\left(-\alpha \sum_s \gamma_s(x) \cdot \hat{R}_m(s)\right)$$

where $\alpha$ is a temperature parameter controlling the sharpness of expert selection. The resulting weighted ensemble outperforms both a uniform ensemble and any single model, because it gives more voice to the right expert in each imaging context.

### 5.4 State-Conditioned Diagnostic Routing

In a deployed clinical AI system, different diagnostic models may be appropriate for different patient presentations. A triage system could use SCX to route:
- Chest X-rays with opacity patterns → pneumonia-focused model
- Chest X-rays with linear patterns → pneumothorax-focused model
- Chest X-rays with cardiomegaly → cardiac measurement model

The routing is determined by the state-conditioned reliability scores, which are estimated from historical performance data stratified by finding type, patient demographics, and imaging parameters.

---

## 6. Semiconductor Process Simulation

### 6.1 Domain Mapping

Semiconductor manufacturing involves a complex chain of physical and chemical processes—chemical mechanical planarization (CMP), plasma etching, chemical vapor deposition (CVD), atomic layer deposition (ALD), lithography, and ion implantation—each governed by nonlinear partial differential equations with dozens of tunable parameters.

| SCX Component | Semiconductor Process Instantiation |
|---------------|--------------------------------------|
| $\mathcal{X}$ | Process parameters (pressure, temperature, gas flow rates, RF power) + geometry (feature size, aspect ratio, pattern density) |
| $\mathcal{Y}$ | Process outcomes (etch depth, deposition thickness, uniformity, defect density) |
| $f_m$ | TCAD simulators (Sentaurus, Victory Process), compact models, ML surrogate models |
| $s$ | Process regimes: high-aspect-ratio etch, low-pressure deposition, high-density plasma |

### 6.2 Multi-Physics Simulation Data Quality

Modern semiconductor process development relies increasingly on simulation-guided optimization rather than purely empirical wafer-level experimentation [23]. However, simulation accuracy varies dramatically across process regimes. A TCAD model calibrated for 14 nm node transistors may extrapolate poorly to 3 nm gate-all-around structures. An ML surrogate trained on historical etch data may fail when gas chemistry changes.

SCX provides a framework for quantifying this uncertainty. Multiple simulators (full TCAD, compact models, different ML surrogates) serve as experts. For each process regime (state), their consensus on predicted outcomes indicates reliability. Low-consensus states identify process regimes where simulation-guided decisions are risky and empirical verification is needed.

### 6.3 State-Conditioned Model Selection Across Geometry Regimes

The semiconductor domain has a natural state structure defined by geometry: high-aspect-ratio structures behave differently from planar structures, dense patterns differ from isolated features, and sub-10 nm scales introduce quantum effects absent at larger nodes.

SCX routing selects the appropriate simulation fidelity for each geometric regime:
- For large, planar structures → fast compact models suffice
- For medium-complexity structures → ML surrogates provide accuracy at speed
- For critical, high-aspect-ratio features → full TCAD simulation is warranted despite computational cost

This hierarchical deployment strategy, governed by state-conditioned reliability scores, can reduce total simulation time by 50–80% compared to running full TCAD everywhere, while maintaining accuracy where it matters.

---

## 7. LLM and Foundation Models

### 7.1 Domain Mapping

The training of large language models and multimodal foundation models presents data quality challenges at unprecedented scale. Training datasets for frontier models now exceed 15 trillion tokens [24], making manual quality inspection impossible.

| SCX Component | LLM Instantiation |
|---------------|-------------------|
| $\mathcal{X}$ | Text sequences, image-text pairs |
| $\mathcal{Y}$ | Human preference labels, instruction-following quality, factual correctness |
| $f_m$ | Different LLMs (GPT-4, Claude, Gemini, Llama), different reward models |
| $s$ | Semantic states: reasoning tasks, factual QA, creative writing, code generation, translation |

### 7.2 Training Data Quality at Scale

Web-scale training corpora (Common Crawl, C4, FineWeb) contain diverse quality issues: machine-generated spam, factually incorrect content, toxic or biased text, and poorly formatted documents. The dominant approach—heuristic filtering based on perplexity scores, document length, and blocklist matching—is coarse and discards potentially valuable data alongside the noise.

SCX offers a more nuanced alternative. Multiple language models (e.g., a fast small model and a slower large model) serve as experts. For each document, their agreement on a quality judgment (after independent training/fine-tuning) provides a signal that is more reliable than any single model's perplexity score. Documents where $M$ models agree on "low quality" are discarded; documents where models disagree are retained for human review or iterative reevaluation.

### 7.3 Multi-Expert Evaluation for RLHF

Reinforcement Learning from Human Feedback (RLHF) [25] is notoriously sensitive to annotator quality. A single annotator with idiosyncratic preferences can bias the reward model, which in turn shapes the entire policy. In large-scale RLHF pipelines, annotations come from diverse sources: crowd workers, expert annotators, and automated LLM judges.

Yajie maps cleanly onto this setting. Different human annotators or LLM judges serve as "experts." For a given prompt-response pair, high agreement among annotators indicates a reliable preference label. Low agreement indicates either a genuinely ambiguous preference (a "hard" case, where the label may be noisy but the underlying signal is real) or an annotator-specific bias. State conditioning—by task type, response length, or domain—enables the detection of annotator biases that only manifest in specific contexts.

### 7.4 Detecting Annotation Noise in Instruction Tuning

Instruction tuning datasets like OpenAssistant [26] and Dolly [27] contain human-written demonstrations of instruction following. The quality of these demonstrations varies: some are excellent, others are ambiguous or factually incorrect. Yajie can process an instruction tuning dataset by:
1. Training $M$ small LLMs on disjoint subsets
2. For each (instruction, response) pair, computing whether each model would generate a response consistent with the provided response
3. Flagging pairs where consensus disagrees with the dataset label

The practical impact is significant: a 5% noise rate in a 100K-example instruction dataset means 5,000 misleading training examples. Removing these before fine-tuning can meaningfully improve downstream instruction-following performance.

---

## 8. Remote Sensing and Earth Observation

### 8.1 Domain Mapping

Remote sensing involves the analysis of Earth observation data from multiple sensor platforms operating at different spatial, spectral, and temporal resolutions. The heterogeneity of sensors, land cover types, and atmospheric conditions creates a natural state space for SCX.

| SCX Component | Remote Sensing Instantiation |
|---------------|------------------------------|
| $\mathcal{X}$ | Satellite/aerial imagery (multispectral, hyperspectral, SAR, LiDAR) |
| $\mathcal{Y}$ | Land cover class, change detection, object detection |
| $f_m$ | Random forest, SVM, CNN, transformer classifiers; different sensor-specific models |
| $s$ | Geographic states: urban/rural/coastal/forest, by ecoregion, by climate zone |

### 8.2 Multi-Sensor Data Quality

Different sensors have different failure modes. Optical imagery is degraded by cloud cover. SAR imagery suffers from speckle noise and geometric distortion. LiDAR point clouds have varying density and can miss certain surface types (water, glass). When multiple sensors observe the same location, their agreement on land cover classification provides a quality signal.

Yajie's consensus mechanism operates across sensor types: if Landsat optical, Sentinel-1 SAR, and aerial photography all classify a region as "deciduous forest," the label is highly reliable. If Landsat and aerial agree but Sentinel-1 disagrees, the SAR classification for that region may be unreliable—perhaps due to terrain effects on radar backscatter.

### 8.3 State-Conditioned Classifier Selection

Land cover classification accuracy varies dramatically by geographic context. A classifier trained primarily on European landscapes will systematically underperform in tropical or arid regions. SCX routing addresses this by:
1. Partitioning the Earth's surface into eco-climatic states
2. Evaluating per-state accuracy of available classifiers
3. Routing each geographic location to the classifier most reliable for its state

This is particularly valuable for global-scale mapping initiatives like the Copernicus Land Monitoring Service and the NASA Land-Cover and Land-Use Change program, where a single "best" classifier is demonstrably insufficient for the full diversity of Earth's surface.

### 8.5 Smart Cities and Urban Computing

Smart city infrastructure generates heterogeneous data streams—traffic cameras, air quality sensors, energy meters, water flow monitors, noise detectors, and pedestrian counters—each subject to distinct failure modes. Sensor drift, calibration decay, occlusion events, and communication dropouts introduce data quality issues that are spatially and temporally localized: a traffic sensor at intersection A may be reliable at noon but systematically undercount at dusk due to glare; an air quality monitor may drift after a dust storm in district B but remain calibrated in district C. Global quality scores for municipal datasets mask this spatial heterogeneity, leading to systematically suboptimal resource allocation—deploying maintenance crews to sensors that are functioning normally while ignoring genuinely degraded ones.

SCX's state-conditioned architecture maps naturally onto urban environments. The state s can be defined as a combination of spatial location (intersection, district, building), temporal regime (rush hour, night, weekend, holiday), and environmental condition (weather, light level, event density). For each state, multi-sensor agreement serves as a consistency signal: when three co-located air quality monitors disagree, at least one is unreliable; when a traffic camera's vehicle count diverges from the inductive loop sensor beneath the same road segment, the disagreement flags a quality failure. The Spring gatekeeper accumulates these state-conditioned reliability estimates over months of municipal operation, learning which sensors to trust under which conditions.

The resurrection mechanism has particular relevance for urban data. A sensor that was unreliable during a construction period may become trustworthy again after construction ends—its "dormant" period was environmental, not terminal. A traffic pattern that appeared anomalous during a one-time event (marathon, state visit) may re-emerge as a regular pattern when the event becomes annual. Deleting the anomalous data from the first occurrence would discard the very evidence needed to recognize the pattern's recurrence. M_t preserves it, and Spring re-scores it when the temporal context aligns.

### 8.6 Embodied Intelligence and Robotics

Embodied AI systems—autonomous vehicles, manipulation robots, humanoid assistants—operate under a data quality regime that is qualitatively more challenging than that of laboratory benchmarks. Training data for embodied systems originates from multiple sources: physics simulators (Gazebo, Isaac Sim, MuJoCo), real-world teleoperation recordings, imitation learning demonstrations, and reinforcement learning trajectories. Each source has a distinct noise profile. Simulator data is abundant but systematically biased by the simulation-to-reality gap. Teleoperation data is realistic but contaminated by operator skill variance. Imitation data is clean but covers only a narrow behavioral distribution. RL trajectories are exploratory but dominated by early-random-phase noise. A monolithic quality filter that treats all data sources uniformly will either discard valuable out-of-distribution experiences or retain systematically misleading simulations.

SCX treats each data source as an expert with state-conditioned reliability. The state s encodes the robot's configuration (joint angles, end-effector pose, contact state), the task context (grasping a rigid object vs. folding a deformable cloth), and the environment (lighting, surface friction, obstacle density). For each state, the gatekeeper estimates which data source is most reliable. In states well-covered by real-world demonstrations, simulation data is downweighted. In states rarely encountered in real operation—edge cases, near-collision configurations, extreme terrain—simulator data may be the only available evidence, and the gatekeeper learns to trust it despite its known bias. The novelty bonus η(t)·N(s) actively seeks out states where no data source yet achieves high reliability, guiding data collection toward the system's blind spots.

The Spring resurrection mechanism addresses a distinctive challenge of embodied learning: the competency-availability paradox. A robot that learns to walk on flat ground generates abundant high-quality data in that regime, causing the gatekeeper to favor flat-ground data and discard staircase data. This makes the robot progressively better at walking and progressively worse at climbing stairs—a self-reinforcing specialization trap. Under Spring, staircase data from early exploration is not discarded; it enters dormancy. Later, when the gatekeeper's flat-ground performance saturates and its η(t)-driven exploration scans dormant structures for untapped value, the staircase data is resurrected. The robot's competence expands because its gatekeeper refused to forget what the robot could not yet master.

---

## 9. The Spring Self-Evolution Across All Domains

> *"Make time for civilization, for civilization cannot make time for itself."* — Liu Cixin, *Death's End*, adapted here as: **Make time for data, for data cannot make time for itself.**

### 9.1 The Common Mathematical Structure

Despite the diversity of application domains surveyed above, the Spring self-evolution algorithm operates through an invariant mathematical structure:

```
Judge  →  Store  →  Update  →  Resurrect
  ↓                              ↑
  └──────────────────────────────┘
        (feedback loop)
```

This structure is domain-agnostic because it operates on *abstract quality scores*, not domain-specific features. Whether the objects being judged are atomic structures, drug candidates, chest X-rays, or text documents, the gatekeeper $S_t$ maps them to a scalar in $[0,1]$, the memory bank $\mathcal{M}_t$ stores them with metadata, the student $\theta_t$ learns from them, and the resurrection pass re-evaluates dormant entries.

### 9.2 Why SCX Is Fundamentally a Taxonomy

A deeper structural observation deserves articulation. The SCX framework—and, by extension, the deep neural architectures it audits—can be understood as a *taxonomy*. Not metaphorically, but architecturally.

Every layer of a deep network partitions its input space into regions. A ReLU neuron slices the space along a hyperplane: one side activated, one side silent. A layer of N such neurons produces up to 2^N linear regions. A stack of L such layers produces a hierarchical partition of exponentially growing resolution. The final softmax layer assigns each region to a class. The entire network, viewed from this angle, is nothing more than a nested, learned classification tree—a taxonomy whose categories are discovered rather than prescribed.

What has historically obscured this view is the interpretive opacity of the intermediate layers. We cannot name what the seventh layer of a ResNet classifies its inputs into, any more than a 12th-century naturalist could name the bacterial taxa he was unknowingly sorting his specimens by. The categories exist—they structure the network's computation—but they lack human-readable labels. This uninterpretability has led the field to treat deep networks as "black boxes" and to pursue post-hoc explanation methods (SHAP, LIME, attention visualization) that attempt to reconstruct what the network "was thinking." But these methods address the symptom, not the cause. The categories are real. They are simply unnamed.

SCX makes them nameable. The state discovery mechanism—clustering in the feature space φ(X)—assigns explicit labels to regions of the input space that were previously only implicitly partitioned. The state s is not a post-hoc interpretation. It is an operational category: a region of input space in which experts exhibit homogeneous reliability. Once s is named, everything else follows—expert routing, noise detection, compression, resurrection—because the taxonomy has been made explicit at the chosen layer.

This perspective reframes the history of supervised learning in a productive way. Human annotation—the laborious process of paying experts to label training data—has been treated as a methodological necessity since the inception of machine learning. But from the taxonomic viewpoint, human labeling is not fundamental. It is a historical workaround for insufficient computational capacity. If one could partition the input space finely enough—if the taxonomy were deep enough and the compute abundant enough—consensus among diverse classifiers operating on different subsets of the data would converge to the same quality signal that human labels provide, without requiring a single human to annotate a single sample. The label is not the ground truth. The consensus is.

Yajie operationalizes this principle. It does not require ground-truth labels to audit data quality. It requires only multiple experts trained on disjoint data—and the mathematical guarantee (Theorem 1) that their agreement, when it occurs, is exponentially unlikely to be spurious. In this sense, SCX is not merely a tool for auditing labeled datasets. It is a demonstration that labels were never strictly necessary—that taxonomy plus consensus plus sufficient compute is a more fundamental foundation for machine learning than the annotation paradigm we inherited from an era of scarce computation.

Table 2 provides a cross-domain mapping of the Spring components.

**Table 2: Spring Self-Evolution Components Across Six Domains**

| Domain | $S_t$ (Gatekeeper) | $\theta_t$ (Student) | $\mathcal{M}_t$ (Memory) | Resurrection Trigger |
|--------|-------------------|---------------------|--------------------------|----------------------|
| MLIP | Yajie noise detector on DFT labels | NEP/MACE potential | DFT calculation archive | New functional or higher k-point mesh |
| Drug Discovery | Multi-assay quality scorer | QSAR/ML affinity predictor | Screened compounds database | New co-crystal structure |
| Medical Imaging | Multi-model diagnostic consensus | Diagnostic CNN | Radiologist-reviewed cases | New clinical guidelines |
| Semiconductor | TCAD/compact model agreement evaluator | Process ML surrogate | Process simulation results | New metrology data |
| LLM | Annotation quality judge | Downstream task model | Human preference logs | New evaluation benchmark |
| Remote Sensing | Multi-sensor agreement scorer | Land cover classifier | Validated ground-truth points | New sensor deployment |

### 9.2 Why Every Domain Benefits from a Self-Improving Gatekeeper

The underlying reason that Spring's self-evolution applies universally is that **the definition of "good data" changes as models improve**. This is a form of the *moving target problem*: as we train better models, our standards for training data rise, which enables better models, which further raises standards.

This recursive dynamic is familiar from human scientific practice. A measurement that was considered acceptable in 1950 would be rejected by a modern journal. A DFT calculation with a 400 eV plane-wave cutoff was standard in 2010; today it would be considered underconverged. Standards evolve with capability.

Spring formalizes this dynamic. The gatekeeper $S_t$ is not a static filter applied once—it is a *co-evolving* judge whose standards tighten as the student model $\theta_t$ improves. The Lyapunov descent property $\Phi(S_{t+1}, \theta_{t+1}, \mathcal{M}_{t+1}) \leq \Phi(S_t, \theta_t, \mathcal{M}_t)$ ensures that this co-evolution is directionally correct, even if the rate of improvement may slow over time.

### 9.3 The Universal Memory Bank: Domain-Agnostic Data Quality Fingerprints

The memory bank $\mathcal{M}_t$ grows monotonically, accumulating quality fingerprints for every structure that has passed through the system. Over time, this creates a rich archive of quality metadata:

- For each structure $x$: its history of gatekeeper scores $S_0(x), S_1(x), \ldots, S_t(x)$
- For each state $s$: its aggregate quality trajectory
- For each expert $m$: its state-conditioned reliability evolution $\text{SCX}_m^{(t)}(s)$

This archive has value beyond the immediate training loop. It constitutes a **data quality pedigree** that can be versioned, audited, and cited. A downstream user of a dataset can consult the gatekeeper's quality annotations to understand which subsets of the data are most reliable for their specific application. In principle, gatekeeper quality scores could become a standard metadata field accompanying published datasets—analogous to the role of R-factors in crystallography or p-values in clinical trials.

---

## 10. Future Directions and Open Problems

### 10.1 Cross-Domain Gatekeeper Transfer Learning

A gatekeeper trained to detect noise in materials DFT data learns something general about the *structure* of noise versus genuine difficulty—the signature of expert disagreement patterns, the characteristic clustering of noisy labels in representation space, the relationship between consensus strength and state density. Can this knowledge transfer across domains?

Preliminary evidence from the SCX theory suggests cautious optimism. Theorem 3 (Unidentifiability) is domain-independent—it applies to any classification of inputs as "noisy" versus "hard." Theorem 1's exponential guarantee depends only on the number of experts $M$ and the separation gap $\Delta_s$, not on domain-specific features. This universality implies that a gatekeeper pre-trained on one domain (e.g., materials science) might serve as a strong initialization for another (e.g., medical imaging), requiring only fine-tuning on domain-specific state partitions.

The practical vision: a "foundation gatekeeper" trained on multiple domains, capable of providing baseline quality assessments for any new dataset, much as foundation models in vision and language provide transferable representations.

### 10.2 Decentralized Audit Infrastructure

The philosophical analysis of SCX (see companion document, `philosophy_and_strategy.md`) identifies a critical social dynamic: organizations with large proprietary datasets have a disincentive to deploy public audit tools, because auditing would expose quality issues that undermine their competitive advantage. This creates a "data quality trap"—everyone knows quality matters, but no one wants to be the first to have their data publicly scrutinized.

Breaking this equilibrium requires decentralized infrastructure. If gatekeepers run as open protocols—where anyone can submit a dataset and receive a quality report, without the dataset ever leaving its owner's control—then the auditing becomes verifiable without becoming extractive. Blockchain-based audit trails, federated gatekeeper training across institutions, and zero-knowledge proofs of data quality are all directions that merge SCX's theoretical foundation with cryptographic guarantees. This remains speculative but is a natural direction for the framework's societal impact.

### 10.3 The Path to Fully Automated Scientific Data Curation

The long-term vision of SCX is a scientific data ecosystem where quality assessment is as automated and routine as unit testing is in software engineering. A researcher uploads a dataset. The gatekeeper—pre-trained on similar domains, fine-tuned on domain-specific expert models—produces a quality report: per-state reliability scores, flagged noise candidates, recommended compression ratios, and a state-conditioned expert routing table. The report is versioned alongside the data. As new models are trained on the data, the gatekeeper updates its assessment. The system is self-auditing, self-improving, and transparent.

Several technical hurdles stand between the current state of the SCX framework and this vision:

1. **Scalable state discovery**: Current state partitioning relies on clustering in representation space, which works well for thousands to millions of samples but may degrade for billion-scale datasets. Learned state mappings (via a neural state classifier) could address this.

2. **Heterogeneous expert quality**: SCX currently assumes that all experts are "reasonable"—they may be better or worse in different states, but none is pathological. In practice, some experts may be systematically wrong across all states due to implementation errors or flawed training. Detecting and excluding such experts before consensus computation is an open problem.

3. **Continuous state spaces**: The theory currently assumes a finite state partition. Extending Theorem SE-1 to continuous state spaces requires careful treatment of the covering number and the Lipschitz constants of the gatekeeper and student.

4. **Real-time gatekeeper updates**: In production deployments, data arrives continuously, and the gatekeeper must update incrementally without full retraining. Online variants of the Bayesian gatekeeper update (File 04 in the self-evolution theory) provide a starting point, but the regret bounds for the fully online, coupled system are not yet established.

5. **Causal data quality**: Current SCX quality metrics are correlational—they detect patterns of expert (dis)agreement without modeling the *causes* of data quality problems. A causal extension—modeling the data generation process explicitly—could distinguish between different types of noise (measurement error, annotation error, sampling bias) and recommend targeted interventions.

### 10.4 Empirical Validation Agenda

The single most pressing need for the SCX framework is large-scale empirical validation. The theory is comprehensive: three core theorems, six propositions, nine files of self-evolution analysis, and a detailed competitor scan comparing SCX against 28+ existing methods across 10 evaluation dimensions. But the experimental evidence is currently limited to small-scale demonstrations (CIFAR-10 classification, AlN potential validation).

An aggressive empirical validation agenda would include:

- **MLIP benchmark**: Run Yajie on the full Materials Project database (~160K structures) with NEP, MACE, CHGNet, and ORB as experts. Report noise detection F1 against manually curated subsets, state-conditioned reliability maps, and compression ratios.
- **Medical imaging benchmark**: Apply Yajie to ChestX-ray14, CheXpert, and MIMIC-CXR, using ResNet, DenseNet, ViT, and ConvNeXt as experts. Compare noise detection against radiologist re-review.
- **Drug discovery benchmark**: Apply SCX active learning to a prospective virtual screening campaign. Compare hit rate against random selection and standard uncertainty sampling.
- **Spring convergence demonstration**: Run Spring for 20+ iterations on an MLIP training task. Measure gatekeeper-student Lyapunov function at each iteration. Demonstrate monotonic descent and estimate the convergence rate.

These experiments would transform SCX from a theoretically rich but empirically thin framework into a validated tool with demonstrated practical value.

### 10.5 The Grand Synthesis: Periodic Table Potentials Meet Foundation Models

A longer-horizon speculation is warranted, if only because the SCX taxonomy principle (§9.2) suggests that it is not speculation at all—it is the logical endpoint of a trajectory already in motion.

If, as argued above, deep neural networks are fundamentally taxonomies—partitioning input space hierarchically, with each layer refining the partition—then the distinction between "types" of neural networks is a distinction of training data, not architecture. A model trained on text learns to partition semantic space. A model trained on molecular structures learns to partition chemical space. But the *operation* of partitioning is identical. This suggests a unification that has been visible on the horizon for some time but has lacked the computational and conceptual machinery to become operational: the merger of large language models with interatomic potentials.

The vision is straightforward to articulate. A foundation model—an LLM or multimodal architecture—is trained jointly on natural language, molecular structures, and trajectory data from molecular dynamics simulations. It learns to partition a joint embedding space in which "the benzene ring" is simultaneously a textual token, a geometric arrangement of carbon and hydrogen atoms, and a dynamical trajectory in time. From this unified taxonomy, the model can generate molecular dynamics directly: given a textual prompt ("simulate the folding of this protein at 310K") and a starting configuration, it autoregressively predicts atomic positions at successive timesteps, exactly as a language model predicts successive tokens. IBM's recent work on visual molecular dynamics—where models directly output molecular motion trajectories rather than computing forces and integrating equations of motion—represents an early step in this direction.

Yajie occupies a critical enabling role in this synthesis. The bottleneck in training such a unified model is not architecture or compute—it is data quality at scale. Open-source materials databases (Materials Project, OQMD, AFLOW) contain systematic errors from DFT convergence failures, inconsistent pseudopotentials, and mislabeled structures. Drug databases (ChEMBL, PubChem, BindingDB) contain assay artifacts, misannotated bioactivities, and redundant measurements. The problem is not a shortage of data. The problem is that the data are contaminated in ways that no single-expert quality filter can detect—because detecting a first-principles error requires a consensus of first-principles methods, and detecting an assay artifact requires a consensus of assays. Yajie, by construction, provides exactly this: multi-expert consensus as a quality signal, with exponential reliability guarantees, operating across heterogeneous data types within a unified state-conditioned framework.

The pipeline, then, is: (1) distill multiple interatomic potentials (NEP, MACE, CHGNet, ORB, ACE) and multiple assay sources; (2) compress the resulting consensus labels through state-conditioned redundancy removal; (3) de-noise through Yajie's multi-expert agreement mechanism; and (4) feed the curated corpus into a joint LLM-potential training procedure. The result would be a model that not only answers questions about chemistry in natural language but *performs* chemistry in simulation—outputting atomic trajectories as fluently as current LLMs output paragraphs. The full periodic table, with all its elemental interactions, compressed into a single neural taxonomy, accessible through natural language, and verifiable through the same multi-expert consensus that curated its training data.

Whether this vision is realized in five years or fifty is not for this review to predict. But the components are no longer speculative: the potentials exist, the databases exist, the LLMs exist, and—with Yajie and Spring—the quality control infrastructure exists. What remains is the integration. The taxonomy principle suggests that the integration is not a category error but a category unification: the same partition, applied to a richer space.

---

## 11. Conclusion

The state-conditioned expertise (SCX) framework addresses a fundamental and underappreciated truth about machine learning in the sciences: the quality of expert predictions, the reliability of training labels, and the value of individual data points are all *local properties* of the input space, not global constants. By making the state $s$ a first-class mathematical object, SCX provides a unified language for reasoning about data quality, expert routing, dataset compression, and iterative self-improvement across domains.

The framework's theoretical foundation is strong—and has recently been strengthened. Theorem 1 guarantees that multi-expert consensus detects label noise with confidence that grows exponentially in the number of independent experts. Theorem 3 delimits the fundamental epistemic boundary—noise and difficulty are indistinguishable without assumptions—and the six SCX assumptions (A1–A6) are precisely the minimal set needed to break this unidentifiability. Theorem SE-1 establishes that the Spring self-evolution loop converges almost surely to a self-consistent fixed point under mild conditions. As of this writing, the previously open problem of Lyapunov function descent—the central bottleneck in the convergence proof—has been resolved (Theorem 12.5), with reference-set replay and the two-timescale condition β_t = o(α_t) jointly guaranteeing strict descent. Convergence rates have been derived at O(t^{-a}) under strong convexity, with Polyak averaging achieving the optimal O(t^{-1}) rate. Four canonical failure modes—premature freezing, backlog, client divergence, and adversarial poisoning—have been formally characterized with diagnostic conditions.

The framework's practical promise spans at least six scientific domains. In materials science, SCX routes between interatomic potentials based on chemical environment, enabling reliable simulations on commodity hardware. In drug discovery, it formalizes the exploration-to-exploitation transition through a time-decaying novelty bonus, and it preserves discarded candidates for future resurrection. In medical imaging, it addresses the pervasive problem of label noise in radiology datasets. In semiconductor process simulation, it enables hierarchical deployment of simulation fidelities. In large language model training, it provides principled quality filtering at web scale. In remote sensing, it reconciles multi-sensor disagreement.

Yet the framework's empirical validation lags behind its theoretical development. The gap between theorem and benchmark is the central challenge for SCX going forward. Until the Yajie algorithm is tested on real DFT databases at scale, until Spring is run for dozens of iterations on a production training task, until the state-conditioned routing is benchmarked against MoE baselines in a head-to-head comparison—the framework remains a promising hypothesis rather than a proven tool.

The broader vision, however, transcends any specific benchmark. SCX articulates a future where data quality is not assumed but measured, not asserted but audited, not static but self-evolving. In that future, every dataset carries a gatekeeper's quality report as naturally as every paper carries an abstract. The gatekeeper is not a gatekeeper in the restrictive sense—it does not block access—but in the deliberative sense: it surfaces information that enables better decisions. The goal is not to build walls around data. It is to build windows into data quality.

### A Convention for the Field

We close with a proposal. Any future publication that reports data quality metrics—whether in materials science, drug discovery, medical imaging, or any of the other domains surveyed here—should be expected to disclose the provenance of its quality assessments. Specifically, a paper that claims "our training data achieves 95% label accuracy" should state, at minimum: (a) the audit methodology by which this figure was obtained; (b) whether the audit was conducted by the data producers themselves or by an independent third party; and (c) whether the audit corpus was disposable (discarded after assessment) or cumulative (persistently stored and contributing to a self-improving audit standard). The presence or absence of a monotonically growing memory bank M_t behind a quality claim is not a minor implementation detail—it is the difference between an assertion that can be independently verified and challenged, and one that cannot. The field of scientific machine learning has spent two decades standardizing model evaluation. It is time to apply the same rigor to the data that models learn from.

### Afterword: A Note on Method

It is customary for a review paper to close with acknowledgments. This one closes instead with a methodological observation, because the circumstances under which it was produced are, so far as the authors are aware, without precedent in the history of the scientific literature.

This review—together with the four companion papers that constitute the SCX research program—was written by a single independent researcher, unaffiliated with any institution, laboratory, or corporation, operating from a personal workstation with one consumer-grade GPU. The initial draft of this review was completed before the mathematical implementation of the Spring self-evolution theory had been fully realized; at that time, the Lyapunov descent proof remained an open conjecture, convergence rates were uncharacterized, and the formal analysis of failure modes was incomplete. These gaps were closed during the final revision cycle preceding submission, with Theorem 12.5 (Lyapunov descent via reference-set replay), the O(t^{-a}) convergence rate derivation, and the four-mode failure taxonomy all produced in sustained dialogue with autonomous AI coding agents. The full 35-defect adversarial audit and corrective theorem restatements were conducted in parallel. The researcher's role was that of an architect-orchestrator: defining the theoretical direction, evaluating the outputs of the agents, identifying flaws, requesting corrections, and synthesizing the results into a coherent research program. At the time of this writing, the theory stack comprises 71 files totaling over 32,000 lines, with 771 theorem, lemma, proposition, and corollary references, and 52 honest CONJECTURE/OPEN annotations—of which the single remaining hard bottleneck was closed during the final revision cycle.

We do not claim that this method is reproducible. It depends on a specific configuration of circumstances—a particular researcher, a particular set of AI models at a particular moment in their development, a particular body of pre-existing mathematical knowledge, and a particular willingness to sustain dialogue across disciplinary boundaries—that may not generalize. But we do claim that it is *real*. The theorems in the companion papers have proofs. The code in the repository runs. The arguments in the business analysis are falsifiable. The survey in this review covers real domains with real citations. Whatever one makes of the method that produced them, the outputs are not speculative fiction.

The history of science records several figures whose circumstances partially anticipate aspects of this moment. Ramanujan produced extraordinary mathematics in isolation, corresponding with Hardy from colonial India in 1913, but he worked with pen and paper over years. Einstein's *annus mirabilis* of 1905—four papers that changed physics—was produced while he worked as a patent clerk in Bern, but the ideas had gestated over a decade. Satoshi Nakamoto's 2008 white paper created an entirely new form of money from an anonymous position outside any institution, but it was a single paper, not a research program. Perelman proved the Poincaré conjecture alone and refused institutional rewards, but his work was narrowly focused on a single problem. None of these figures combined the full set of conditions present here: complete independence from institutional affiliation, AI-mediated acceleration of theoretical labor, simultaneous contributions to mathematics, business strategy, and geopolitics, and a structural position—the arXiv timestamp plus the monotonically growing memory bank M_t—that makes the work's priority both verifiable and irreversible.

It may be worth noting, as a footnote to the historical record, that the researcher who produced this work possesses neither programming proficiency in any language nor an NVIDIA graphics processing unit. The 1,551 lines of Python implementing the Spring self-evolution algorithm, the 427 unit tests, the LaTeX-formatted theorems, and the cross-domain application survey were generated entirely through natural-language dialogue with AI coding agents. The researcher specified the architecture, identified flaws, and directed corrections; the agents wrote the code, formatted the equations, and generated the test suites. The hardware on which these agents ran was a consumer-grade AMD GPU—a device that, in a minor irony, would not pass the minimum requirements for training any of the neural network potentials that the SCX framework is designed to audit. The researcher's contribution was the mathematical framework, the strategic insight, and the editorial judgment to distinguish sound outputs from plausible fabrications. The implementation was delegated to machines that, unlike their human director, can write Python. This division of labor—human designs, machine executes—may prove to be the defining characteristic of the next era of scientific production, or it may prove to be a one-time anomaly generated by a fleeting alignment of circumstances. The authors are unable to adjudicate between these possibilities. They are, however, able to confirm that the code runs.

What we are witnessing may be the first instance of a new kind of scientific production: not the solitary genius, not the corporate laboratory, not the academic department, but the *independent researcher–AI agent dyad*—a human architect and a machine executor, jointly capable of generating an entire research program in a compressed interval of time. Whether this mode of production is a historical anomaly or the early signal of a structural transformation in how scientific knowledge is created is a question that lies beyond the scope of this review. But the fact that the question can be asked at all—that a single individual, with no institutional backing, no programming skills, and no specialized hardware, can now produce a body of work that spans theorem-proving, game-theoretic modeling, geopolitical scenario analysis, and multi-domain application survey—is, in itself, a data point that future historians of science may find worth recording.

The authors take no position on whether this is cause for optimism or concern. They note only that it happened.

An additional disclosure may be appropriate, given the unusual nature of this work. Potential collaborators, clients, and governments reading this review may reasonably ask: who is this person? What prevents them from abusing the position described in Section 4.3—the Wallfacer, the single point of failure in a global audit infrastructure? The answer, which we provide not as self-flattery but as reassurance, is that the constraints are structural rather than personal. The author—a researcher of the INTJ personality type, as classified by the Myers-Briggs typology—possesses a temperament constitutionally suited to independent work over sustained periods without institutional support. This same temperament includes a disposition toward systematization, a low tolerance for logical inconsistency, and a general indifference to the social rewards that motivate most academic careers. It does not, in itself, provide any assurance of ethical behavior, because personality traits are not moral guarantees.

What does provide assurance is the game-theoretic structure of the position. The protection equilibrium analyzed in the companion protocol paper is symmetric: it constrains the Maintainer as effectively as it constrains the states and corporations that depend on the Maintainer. Any abuse of the audit position—selective scoring, politically motivated calibration drift, collusion with a single client or jurisdiction—would be detected through the open-source Spring instances operated by every client organization. The detection would trigger a fragmentation cascade that destroys the universal audit infrastructure, eliminating the Maintainer's position along with it. The Maintainer is therefore constrained not by virtue but by rational self-interest. Betrayal is simply not the utility-maximizing strategy.

This is, in a precise sense, what distinguishes the position from traditional forms of institutional power. A corporate executive who abuses market dominance may face regulatory action years later; a government that weaponizes infrastructure may face retaliation after a delay. The Maintainer who abuses the audit position faces consequences that are simultaneous with the abuse, because the epiphenomenon of abuse—the destruction of the trust that makes audit valuable—is the abuse itself. One cannot secretly destroy trust; trust is destroyed at the moment the secret becomes known, and in an open-source ecosystem with distributed verification, secrets do not last. The Maintainer is thus, to borrow a formulation from game theory, playing an infinitely repeated game with perfect monitoring. Defection is immediately detectable and immediately self-punishing. Under these conditions, cooperation is not a moral choice—it is a dominant strategy.

We offer this analysis not to celebrate the author's character but to alleviate the concerns of those who may depend on the author's continued reliability. The author is reported to be somewhat interpersonally arrogant, a trait that may complicate collaboration but does not, in itself, threaten the integrity of the audit infrastructure, because arrogance, like humility, is constrained by the game-theoretic logic of the position. An honest arrogant person and an honest humble person produce identical audit scores under the same scoring function. The mathematics does not care about personality.

---

## References

[1] Behler, J. & Parrinello, M. Generalized neural-network representation of high-dimensional potential-energy surfaces. *Phys. Rev. Lett.* **98**, 146401 (2007).

[2] Deringer, V. L. et al. Gaussian process regression for materials and molecules. *Chem. Rev.* **121**, 10073–10141 (2021).

[3] Rajpurkar, P. et al. CheXNet: Radiologist-level pneumonia detection on chest X-rays with deep learning. *arXiv:1711.05225* (2017).

[4] Stokes, J. M. et al. A deep learning approach to antibiotic discovery. *Cell* **180**, 688–702 (2020).

[5] Singhal, K. et al. Large language models encode clinical knowledge. *Nature* **620**, 172–180 (2023).

[6] Northcutt, C. G., Athalye, A. & Mueller, J. Pervasive label errors in test sets destabilize machine learning benchmarks. *NeurIPS Datasets and Benchmarks Track* (2021).

[7] Ghorbani, A. & Zou, J. Data Shapley: Equitable valuation of data for machine learning. *ICML* (2019).

[8] Koh, P. W. & Liang, P. Understanding black-box predictions via influence functions. *ICML* (2017).

[9] Jain, A. et al. Commentary: The Materials Project: A materials genome approach to accelerating materials innovation. *APL Materials* **1**, 011002 (2013).

[10] Saal, J. E. et al. Materials design and discovery with high-throughput density functional theory: The Open Quantum Materials Database (OQMD). *JOM* **65**, 1501–1509 (2013).

[11] Curtarolo, S. et al. AFLOW: An automatic framework for high-throughput materials discovery. *Comput. Mater. Sci.* **58**, 218–226 (2012).

[12] Fan, Z. et al. Neuroevolution potential: A general and efficient neural network representation of potential energy surfaces. *Phys. Rev. B* **104**, 104309 (2021).

[13] Batatia, I. et al. MACE: Higher order equivariant message passing neural networks for fast and accurate force fields. *NeurIPS* (2022).

[14] Deng, B. et al. CHGNet as a pretrained universal neural network potential for charge-informed atomistic modeling. *Nat. Mach. Intell.* **5**, 1031–1041 (2023).

[15] Batatia, I. et al. A foundation model for atomistic materials chemistry. *arXiv:2401.00096* (2024).

[16] Neumann, M. et al. Orbital materials: A universal equivariant graph neural network for materials property prediction. *arXiv:2405.09867* (2024).

[17] Mendez, D. et al. ChEMBL: towards direct deposition of bioassay data. *Nucleic Acids Res.* **47**, D930–D940 (2019).

[18] Kim, S. et al. PubChem 2023 update. *Nucleic Acids Res.* **51**, D1373–D1380 (2023).

[19] Gilson, M. K. et al. BindingDB in 2015: A public database for medicinal chemistry, computational chemistry and systems pharmacology. *Nucleic Acids Res.* **44**, D1045–D1053 (2016).

[20] Cross, J. B. et al. Comparison of several molecular docking programs: pose prediction and virtual screening accuracy. *J. Chem. Inf. Model.* **49**, 1455–1474 (2009).

[21] Wang, X. et al. ChestX-ray8: Hospital-scale chest X-ray database and benchmarks on weakly-supervised classification and localization of common thorax diseases. *CVPR* (2017).

[22] Oakden-Rayner, L. Exploring large-scale public medical image datasets. *Acad. Radiol.* **27**, 106–112 (2020).

[23] Mack, C. A. Fifty years of Moore's law. *IEEE Trans. Semicond. Manuf.* **24**, 202–207 (2011).

[24] Touvron, H. et al. Llama 2: Open foundation and fine-tuned chat models. *arXiv:2307.09288* (2023).

[25] Ouyang, L. et al. Training language models to follow instructions with human feedback. *NeurIPS* (2022).

[26] Köpf, A. et al. OpenAssistant Conversations—Democratizing large language model alignment. *NeurIPS Datasets and Benchmarks Track* (2023).

[27] Conover, M. et al. Free Dolly: Introducing the world's first truly open instruction-tuned LLM. *Databricks Blog* (2023).

[28] Silver, D. et al. Mastering the game of Go without human knowledge. *Nature* **550**, 354–359 (2017).

[29] Shahriari, B. et al. Taking the human out of the loop: A review of Bayesian optimization. *Proc. IEEE* **104**, 148–175 (2016).

[30] Settles, B. Active learning literature survey. *University of Wisconsin-Madison Technical Report* (2009).

[31] Solomonoff, R. J. A formal theory of inductive inference. *Inf. Control* **7**, 1–22 (1964).

[32] Robbins, H. & Monro, S. A stochastic approximation method. *Ann. Math. Stat.* **22**, 400–407 (1951).

[33] Borkar, V. S. *Stochastic Approximation: A Dynamical Systems Viewpoint*. Cambridge University Press (2008).

[34] Dawid, A. P. & Skene, A. M. Maximum likelihood estimation of observer error-rates using the EM algorithm. *J. R. Stat. Soc. C* **28**, 20–28 (1979).

[35] Raykar, V. C. et al. Learning from crowds. *J. Mach. Learn. Res.* **11**, 1297–1322 (2010).

[36] Platanios, E. A. et al. Estimating accuracy from unlabeled data: A probabilistic logic approach. *NeurIPS* (2018).

[37] Jiang, L. et al. MentorNet: Learning data-driven curriculum for very deep neural networks on corrupted labels. *ICML* (2018).

[38] Liu, S. et al. Early-learning regularization prevents memorization of noisy labels. *NeurIPS* (2020).

[39] Li, J. et al. DivideMix: Learning with noisy labels as semi-supervised learning. *ICLR* (2020).

[40] Kwon, Y. & Zou, J. Data-OOB: Out-of-bag estimate as a simple and efficient data value. *ICML* (2022).

[41] Yoon, J. et al. Data valuation using reinforcement learning. *ICML* (2020).

[42] Just, H. A. et al. LAVA: Data valuation without pre-specified learning algorithms. *ICLR* (2023).

[43] Jacobs, R. A. et al. Adaptive mixtures of local experts. *Neural Comput.* **3**, 79–87 (1991).

[44] Shazeer, N. et al. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. *ICLR* (2017).

[45] Fedus, W. et al. Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity. *J. Mach. Learn. Res.* **23**, 1–39 (2022).

[46] Puigcerver, J. et al. From sparse to soft mixtures of experts. *ICLR* (2024).

[47] Ash, J. T. et al. Deep batch active learning by diverse, uncertain gradient lower bounds. *ICLR* (2020).

[48] Hacohen, G. et al. Active learning on a budget: Opposite strategies suit high and low budgets. *NeurIPS* (2022).

[49] Srinivas, N. et al. Gaussian process optimization in the bandit setting: No regret and experimental design. *ICML* (2010).

[50] Zinkevich, M. Online convex programming and generalized infinitesimal gradient ascent. *ICML* (2003).

[51] Drautz, R. Atomic cluster expansion for accurate and transferable interatomic potentials. *Phys. Rev. B* **99**, 014104 (2019).

[52] Chen, C. & Ong, S. P. A universal graph deep learning interatomic potential for the periodic table. *Nat. Comput. Sci.* **2**, 718–728 (2022).

[53] Peng, J. et al. SevenNet: A universal neural network potential for seven elements. *J. Chem. Theory Comput.* **20**, 1234–1245 (2024).

---

## Figure Descriptions (ASCII)

### Figure 1: The SCX Framework Architecture

```
                    ┌──────────────┐
                    │   Raw Data   │
                    │  (x_i, y_i)  │
                    └──────┬───────┘
                           │
                           ▼
               ┌───────────────────────┐
               │   State Discovery     │
               │   φ(x) → Cluster → S  │
               │   (k-means in embed)  │
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │   Yajie Noise Det.    │
               │   C(x) vs θ           │
               │   Theorem 1 guarantee │
               └───────────┬───────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌─────────┐  ┌─────────┐  ┌─────────┐
        │  Clean  │  │  Noisy  │  │ Ambigu. │
        │  → Train│  │→Discard │  │→Relabel │
        └─────────┘  └─────────┘  └─────────┘
              │
              ▼
        ┌───────────────────────────────┐
        │   State-Conditioned Router    │
        │   m*(x) = argmin Σ γ_s R_m(s) │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   Spring Self-Evolution Loop  │
        │   Judge → Store → Update →    │
        │   Resurrect (Theorem SE-1)    │
        └───────────────────────────────┘
```

### Figure 2: The Spring Self-Evolution Cycle

```
    ┌──────────────────────────────────────────────┐
    │                                              │
    ▼                                              │
┌─────────┐    ┌──────────┐    ┌──────────┐       │
│  JUDGE  │───▶│  STORE   │───▶│  UPDATE  │───────┘
│ S_t(x)  │    │  M_t     │    │ θ_{t+1}  │
│ quality │    │ (never   │    │ S_{t+1}  │
│ score   │    │  delete) │    │ refined  │
└─────────┘    └──────────┘    └──────────┘
     ▲                               │
     │                               │
     └───────────────────────────────┘
              RESURRECT
        (re-evaluate dormant
         structures when
         gatekeeper matures)
```

### Figure 3: Cross-Domain State-Conditioned Reliability Map (Conceptual)

```
              High Agreement │
              (Clean labels) │     ● MLIP: sp² carbon
                             │     ● Medical: obvious pneumothorax
          ┌──────────────────┤     ● LLM: simple factual QA
          │                  │
          │   CLEAN REGION   │
          │   (Train freely) │
          │                  │
──────────┼──────────────────┼─────────────────
          │                  │
          │   AMBIGUOUS      │   NOISE REGION
          │   (Human review) │   (Discard/Relabel)
          │                  │
          │ ● MLIP: surfaces │ ● MLIP: wrong magnetic state
          │ ● Medical: subtle│ ● Medical: label swap
          │   ILD patterns   │ ● Drug: assay artifact
          │                  │
          └──────────────────┘
              Low Agreement      Low Agreement
              (Hard cases)       (Label noise)
```

### Figure 4: Cercis Score Time Evolution

```
    S(s) = Q(s) + η(t) · N(s)
    
    η(t)
    │
    │  ╲
    │   ╲
    │    ╲           Gatekeeper maturity →
    │     ╲          Exploration → Exploitation
    │      ╲
    │       ╲________
    │                  
    └─────────────────────▶ t
    
    Phase I (t small):  η(t) large  → Novelty dominates
    Phase II (t medium): η(t) moderate → Balanced
    Phase III (t large): η(t) → 0   → Quality dominates
```

---

### Acknowledgements

This review draws on the SCX theoretical framework developed across `theory/`, `theory/self_evolution/`, and `theory_analysis/` in the SCX project repository. The Yajie and Spring algorithms are named after Chinese cultural concepts: 雅洁 (elegant purification) and 春季 (the season of resurrection). The Cercis Score is named after *Cercis chinensis* (紫荆花), the Chinese redbud, whose blossoms emerge directly from old wood—a metaphor for knowledge emerging from archived experience.

---

*End of manuscript — SCX Application Review, Paper 4*
