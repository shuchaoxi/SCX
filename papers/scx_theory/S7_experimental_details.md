# Experimental Details

**Author:** SCX

## Experimental Details

This section documents the experimental configuration for all datasets used in the main text. All experiments are designed to validate the theoretical predictions of Theorems~1--4, Proposition~6, and the SCX noise detection framework under controlled conditions.

### AlN v3 MLIP: Dataset, ACE Descriptors, Expert Configuration

**Dataset.**
The AlN v3 dataset consists of 534 atomic configurations (frames) generated from thermal and molecular dynamics simulations of aluminium nitride using density functional theory (DFT). Each frame contains atomic positions, forces, and energies computed at the DFT level. Among these 534 frames, 53 carry label noise introduced by thermal fluctuations and MD trajectory artifacts, giving a noise rate $\eta = 53/534 \approx 0.099$. The noise is concentrated in frames near the melting transition where the Born--Oppenheimer surface is poorly sampled.

**ACE Descriptors.**
Feature representations are computed using the Atomic Cluster Expansion (ACE) [cite], a body-order expansion of atomic neighbourhood densities:

$$
\phi_i = \bigl\{ \langle A_i | A_{n_1 n_2 l m} \rangle \bigr\},
$$

where each feature corresponds to a correlation of radial basis functions and spherical harmonics evaluated on the atomic neighbourhood of atom $i$. The ACE descriptor yields $d_\phi = 100$ features per atom (using $N_{radial} = 8$, $l_ = 4$, and a 3-body correlation order). Per-configuration features are obtained by averaging atom-wise ACE vectors over all atoms in the frame.

**State Discovery.**
$K$-means clustering ($K = 8$ states, determined by the elbow method on the within-cluster sum of squares) is applied to the ACE feature matrix $\Phi \in \mathbb{R}^{534 \times 100}$. The discovered states correspond to physically interpretable regimes: bulk crystal, surface, near-melting, defect-rich, and several intermediate configurations.

**Expert Configuration.**
$M = 12$ expert models are trained, each on a disjoint subset of the 534 frames. Following the SCX pipeline:

- Each expert is a linear ACE model (Ridge regression on the ACE descriptors to predict per-atom energies and forces).
- Training subsets are disjoint and stratified by state to preserve state proportions: each expert sees approximately $534 / 12 \approx 44$ frames.
- Experts are trained independently and in parallel using the CPU cluster described in Section [ref].
- The consensus score $C(x)$ is the fraction of experts whose per-frame energy prediction error exceeds a threshold $\tau = 0.05$ eV/atom.

**Results.**
The empirical F1 score is $0.87$. The theoretical F1 lower bound from Theorem~1 (Hoeffding form) is $0.87$ for $M=12$, $\eta=0.099$, and a mean separation gap $\Delta \approx 0.35$ (estimated from the empirical consensus distributions). The adaptive threshold from Theorem~4' with $\eta$ estimated from the data yields $C_/\eta = 4.59$ (numerically verified), giving the asymptotic constant for the Chernoff-rate bound.

### CIFAR-10: ResNet-18 Architecture, Training Protocol

**Dataset.**
CIFAR-10 consists of 60,000 $32 \times 32$ colour images in 10 classes (50,000 training, 10,000 test). We inject synthetic label noise at rate $\eta \in \{0.05, 0.10, 0.20\}$ for controlled experiments; the main text reports $\eta = 0.10$.

**ResNet-18 Architecture.**
The expert model is a standard ResNet-18 [cite] adapted to CIFAR-10:

- Initial $3 \times 3$ convolution (stride 1) with 64 filters, batch normalisation, ReLU.
- Four residual stages with $[2, 2, 2, 2]$ blocks, feature dimensions $[64, 128, 256, 512]$.
- Global average pooling followed by a 10-way fully connected classification head.
- Approximately 11 million trainable parameters.

**Training Protocol.**

- $M = 10$ experts, each trained on a disjoint subset of 5,000 images (stratified by class).
- Optimiser: SGD with momentum 0.9, weight decay $5 \times 10^{-4}$.
- Learning rate schedule: initial $0.1$, cosine annealing to zero over 200 epochs.
- Batch size: 128.
- Data augmentation: random horizontal flip, random $32 \times 32$ crop with 4-pixel padding.
- Each expert training takes approximately 30 minutes on a single NVIDIA RTX 3090 GPU.

**Feature Extraction for State Discovery.**
State discovery uses the penultimate-layer embeddings (dimension 512) from a ResNet-18 trained on clean CIFAR-10. These embeddings serve as the feature representation $\phi(x) \in \mathbb{R}^{512}$. $K$-means clustering with $K = 10$ is applied to the embedding matrix.

**Results.**
At $\eta = 0.10$ noise, SCX achieves F1 $= 0.62$ versus the loss-baseline detector F1 $= 0.45$. The mutual information ratio $\delta / \log K \approx 0.15$, placing CIFAR-10 well within the regime where Theorem~2 predicts SCX can improve over the baseline. The empirical improvement of $+0.17$ is consistent with the bound $\mathrm{F1}_{\mathrm{SCX}} \leq \mathrm{F1}_{\mathrm{base}} + C_F \sqrt{\delta/2}$ with $C_F \approx 1.1$ and $\sqrt{\delta/2} \approx 0.27$.

### DermaMNIST: SimpleCNN vs ResNet-18 Comparison

**Dataset.**
DermaMNIST [cite] is a skin lesion classification dataset derived from the HAM10000 repository. It contains 10,015 dermoscopic images across 7 disease classes (train/val/test split: 7,007 / 1,003 / 2,005). We inject label noise at rate $\eta = 0.10$, matching the CIFAR-10 protocol.

**SimpleCNN Architecture (Weak Features).**
To create a deliberately weak feature regime, we use a minimal CNN:

- Two convolutional layers: $3 \times 3$ conv, 32 filters, ReLU, $2 \times 2$ max-pooling; then $3 \times 3$ conv, 64 filters, ReLU, $2 \times 2$ max-pooling.
- Two fully connected layers: 128 units (ReLU), then 7 units (classification).
- Approximately 0.4 million parameters.
- Feature dimension before classification head: 128.

**ResNet-18 Configuration (Strong Features, comparison).**
We also evaluate a ResNet-18 on DermaMNIST (same architecture as Section [ref] but with 7 output classes) to demonstrate the effect of feature quality. Input images are resized to $224 \times 224$ for the ResNet-18 (as required by the pretrained stem), or kept at $28 \times 28$ for SimpleCNN.

**Training Protocol (both architectures).**

- $M = 10$ experts, disjoint subsets stratified by class.
- SimpleCNN: Adam optimiser, learning rate $10^{-3}$, 100 epochs, batch size 64.
- ResNet-18: SGD with momentum 0.9, learning rate $10^{-2}$ (cosine annealing), 100 epochs, batch size 64.
- Data augmentation: random horizontal flip, random rotation ($\pm 15^\circ$).

**Results.**

- **SimpleCNN (weak features)**: $\delta / \log K \approx 0.52$. SCX F1 $= 0.101$, loss baseline F1 $= 0.105$. The improvement is negligible, consistent with Theorem~2's prediction that SCX cannot significantly outperform the baseline when $\delta / \log K > 0.5$. Proposition~6's bootstrap stability diagnostic gives $S(\Phi, K) < 0.5$, confirming weak features.
- **ResNet-18 (stronger features)**: $\delta / \log K \approx 0.22$. SCX F1 $= 0.48$, loss baseline F1 $= 0.38$. The improvement of $+0.10$ confirms that better features restore SCX's effectiveness.

This comparison provides a direct empirical test of Theorem~2: with everything else held constant (dataset, noise rate, $M$), varying only the feature quality transitions SCX from ineffective (SimpleCNN, $\delta/\log K > 0.5$) to effective (ResNet-18, $\delta/\log K < 0.3$).

### DrugBank: Molecular Descriptors, Targetome Screening

**Dataset.**
DrugBank [cite] is a comprehensive pharmaceutical database containing 13,557 drug entries with 5,108 approved small molecule drugs. We use the subset of 2,000 approved drugs with known protein target annotations for a drug--target interaction noise detection task.

**Molecular Descriptors.**
Feature representations are computed using three descriptor families:

- **MACCS keys**: 166-bit substructure fingerprints (binary).
- **ECFP4 (Extended Connectivity Fingerprints)**: 2,048-bit circular fingerprints with radius 2.
- **Physicochemical descriptors**: 200 continuous-valued descriptors (molecular weight, logP, H-bond donors/acceptors, rotatable bonds, polar surface area, etc.).

The full feature vector is the concatenation of all three types: $\phi(x) \in \mathbb{R}^{2414}$ (166 + 2048 + 200).

**Targetome Screening Task.**
For each drug, the task is to predict its set of protein targets (multi-label classification over 500 target classes). Noise is injected by flipping a fraction $\eta$ of the drug--target interaction labels. Expert models are $M = 8$ random forest classifiers (100 trees each, max depth 20), trained on disjoint subsets of the 2,000 drugs stratified by therapeutic area.

**Results.**
The DrugBank dataset exhibits moderate feature strength ($\delta / \log K \approx 0.31$), placing it in the regime where SCX provides modest but measurable improvement. SCX F1 $= 0.34$ versus loss baseline F1 $= 0.28$ at $\eta = 0.10$ noise.

### Noise Injection Protocol (All Datasets)

All synthetic noise injections follow a uniform-label-flip protocol (consistent with Assumption A4):

1. Select a fraction $\eta$ of training samples uniformly at random.
2. For each selected sample: replace the true label $y^*$ with a label drawn uniformly from $\mathcal{Y} \setminus \{y^*\}$.
3. For multi-state datasets (AlN), noise injection is stratified so that each state $s$ receives noise at rate $\eta$ (preserving $\rho_s$).
4. The noise injection is applied *before* expert training, so experts see noisy labels in their training subsets.
5. The ground truth (clean labels) is retained for evaluation but never revealed to the SCX pipeline.

For AlN v3, the noise is organic (not synthetically injected), arising from thermal and MD simulation artifacts. The noise detection task is to identify these naturally occurring noisy frames.

### Evaluation Metrics

**Precision, Recall, F1 Score.**
Let $\hat{Z}(x) \in \{0,1\}$ be the SCX noise flag for sample $x$, and $Z(x) \in \{0,1\}$ be the ground truth (1 = noise). On a per-state basis:

$$
Precision_s &= \frac{|\{x \in s: \hat{Z}=1, Z=1\}|}{|\{x \in s: \hat{Z}=1\}|}, 

Recall_s &= \frac{|\{x \in s: \hat{Z}=1, Z=1\}|}{|\{x \in s: Z=1\}|}, 

F1_s &= \frac{2 \cdot Precision_s \cdot Recall_s}{Precision_s + Recall_s}.
$$

The global F1 is the weighted average over states: $\mathrm{F1} = \sum_s \rho_s \cdot F1_s$, where $\rho_s$ is the proportion of data in state $s$.

**Loss Baseline.**
The loss baseline detector flags a sample as noise if the minimum expert loss $\min_m \ell(f_m(x), y)$ exceeds a threshold $\theta_{base}$, without using state information or feature representations. The threshold $\theta_{base}$ is chosen to maximise F1 on a held-out validation set (10\% of training data). This baseline represents the best achievable performance of a method that does not exploit state structure.

**Stability Score (Proposition~6).**
The clustering stability $S(\Phi, K)$ is the mean adjusted Rand index (ARI) between $k$-means clusterings on the full data and on $B = 50$ bootstrap resamples, using $k$-means++ initialization and $n_{init} = 10$ random starts per run. See Supplementary Information S6 for the algorithm.

### Computational Resources
<!-- label: sec:compute -->

Table [ref] summarizes the computational resources used for each dataset.

[Table omitted — see original .tex]

All experiments use $M \in \{8, 10, 12\}$ experts depending on the dataset. The bootstrap stability diagnostic (Proposition~6) adds $B = 50$ additional $k$-means runs per dataset, which is negligible compared to expert training time. The SCX pipeline is implemented in Python 3.10 using PyTorch 2.0 (GPU experiments) and scikit-learn 1.2 (CPU experiments).

\begin{thebibliography}{99}

\bibitem{drautz2019ace}
R. Drautz, ``Atomic cluster expansion for accurate and transferable interatomic potentials,'' *Phys. Rev. B* **99**, 014104 (2019).

\bibitem{he2016resnet}
K. He, X. Zhang, S. Ren, and J. Sun, ``Deep residual learning for image recognition,'' in *Proc. IEEE CVPR*, pp.~770--778 (2016).

\bibitem{yang2023medmnist}
J. Yang *et al.*, ``MedMNIST v2: A large-scale lightweight benchmark for 2D and 3D biomedical image classification,'' *Sci. Data* **10**, 41 (2023).

\bibitem{wishart2018drugbank}
D. S. Wishart *et al.*, ``DrugBank 5.0: A major update to the DrugBank database for 2018,'' *Nucleic Acids Res.* **46**, D1074--D1082 (2018).

\end{thebibliography}