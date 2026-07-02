# Extended Experimental Results

**Author:** SCX

## Extended Experimental Results
<!-- label: sec:S1 -->

### AlN MLIP: Detailed Per-State Performance

Table [ref] presents the per-state noise detection performance for the AlN v3 dataset with $M = 12$ experts and ACE descriptors. The dataset partitions into eight states via two-layer discovery, with noise concentrated in the thermal and MLMD states.

[Table omitted — see original .tex]

The theoretical F1 lower bound from Theorem~1 (Equation~1 in the main text) for these parameters is approximately 0.86 under equal state proportions and 0.77 under a conservative assumption that noise-heavy states are larger. The empirical global F1 of 0.87 lies within this range, confirming that the bound is empirically tight: the theory neither overpromises nor underdelivers.

The downstream effect of SCX cleaning on force prediction accuracy is substantial. Figure [ref] shows the force RMSE distribution before and after cleaning.

[Figure omitted — see original .tex]

### CIFAR-10: Full Noise Rate Sweep

Table [ref] shows the complete CIFAR-10 results for SCX cleaning versus architecture change across three noise rates.

[Table omitted — see original .tex]

The ratio decreases as noise increases, which is consistent with the theoretical prediction that the marginal benefit of cleaning is largest when the noise rate is low enough that the baseline model has not already been severely degraded. The architecture improvement (SimpleCNN to ResNet-18) is essentially constant at approximately 2--3\% across noise levels, consistent with the view that architecture capacity provides diminishing returns once a reasonable baseline is established.

### DermaMNIST: Weak Feature Regime

Table [ref] confirms the weak-feature regime prediction from Theorem~2.

[Table omitted — see original .tex]

The critical observation is that switching to ResNet-18 features (which increase $\delta$ to approximately 0.18 and reduce $\epsilon_\phi$ to approximately 0.35) substantially improves SCX performance without changing the detection algorithm. This confirms that the limiting factor is feature quality, not the SCX method itself. The practical implication is that investing in better feature representations--higher resolution images, stronger pretrained backbones, or data-specific descriptors--is the correct response when SCX underperforms on weak-feature domains.

### DrugBank: Tabular Domain Details

Table [ref] shows DrugBank results.

[Table omitted — see original .tex]

The DrugBank case is notable because the features are tabular (chemical fingerprints + protein descriptors) rather than learned representations. The SCX pipeline's second-layer error-driven encoder still provides substantial benefit, improving noise detection F1 from 0.29 (loss baseline) to 0.56.

## Ablation Studies
<!-- label: sec:S2 -->

### Variation in Number of Experts $M$

Figure [ref] shows how the noise detection F1 varies with the number of experts $M$ across all four domains.

[Figure omitted — see original .tex]

Key observations:

- All four domains show the characteristic exponential-improvement-then-saturation curve predicted by Theorem~1.
- The saturation point varies by feature strength: AlN (strong features) saturates around $M = 12$, while DermaMNIST (weak features) shows negligible improvement beyond $M = 5$.
- The empirical F1 consistently exceeds the Hoeffding lower bound (dashed lines), often by substantial margins. This is expected because the Hoeffding bound is conservative; the Chernoff/KL bound (Section~S2 of Paper~I) provides a tighter approximation.
- For DrugBank, the slowest improvement rate reflects the moderate feature strength of tabular descriptors.

Table [ref] provides the numerical values.

[Table omitted — see original .tex]

### Variation in Number of States $K_S$

The number of states $K_S$ in the two-layer discovery is a hyperparameter determined by the elbow method on the within-cluster sum of squares. Table [ref] shows sensitivity to this choice.

[Table omitted — see original .tex]

Performance is relatively insensitive to exact $K_S$ choice as long as $K_S \geq 4$, consistent with the theoretical requirement that states must be fine enough to homogenize error rates within each state but coarse enough to maintain statistical power. The elbow method ($K_S = 8$) is near-optimal.

## Comparison with Alternative Cleaning Methods
<!-- label: sec:S3 -->

We compare SCX against three alternative noise detection approaches on the AlN dataset (where ground truth noise labels are available) and on synthetic noise benchmarks for CIFAR-10.

### Methods Compared

**Loss-based filtering (baseline):** Compute the per-sample training loss $\ell(f(x_i), y_i)$ of a single model trained on all data. Flag samples with loss exceeding the 90th percentile as noisy. This is the simplest and most widely used approach.

**Confidence learning (CL):** Implement the confident learning algorithm of Northcutt et al. [cite]. This uses the predicted class probabilities of a trained model to estimate the joint distribution of noisy and true labels, then identifies samples most likely to be mislabeled. We use the open-source cleanlab [cite] implementation with default parameters.

**Dawid-Skene (DS):** The classical Dawid-Skene model [cite] for multi-annotator agreement. We treat $M$ expert predictions as $M$ annotators and apply the EM algorithm to estimate each sample's true label. The noise score is the posterior probability that the observed label differs from the estimated true label.

**SCX (ours):** The full two-layer state discovery + multi-expert consistency pipeline described in the Methods section.

### Main Comparison

[Table omitted — see original .tex]

Several patterns emerge:

1. **SCX dominates on strong-feature domains.** On AlN, where ACE descriptors provide excellent state discrimination, SCX (F1 = 0.87) substantially outperforms all alternatives. Confidence learning (0.51) and Dawid-Skene (0.63) both fall short because they lack the state-conditioning that is critical for distinguishing thermal-difficulty from true noise.
2. **Confidence learning benefits from stronger models.** CL's performance improves when the underlying model is more accurate (CIFAR-10: F1 = 0.53), but it remains below SCX across all domains. CL's limitation is that it conflates high-loss samples irrespective of whether the loss is due to noise or difficulty.
3. **Dawid-Skene performs well only with very clean experts.** DS assumes annotators are generally correct, which holds approximately for the AlN experts (error rate $\approx 0.10$) but not for CIFAR-10 (error rate $\approx 0.45$ on the challenging subsample).
4. **On weak-feature domains, no method excels.** DermaMNIST is the great equalizer: all methods perform at or near baseline, confirming that the bottleneck is feature quality, not algorithm choice.

### SCX Ablation: With and Without Two-Layer Discovery

To isolate the contribution of the two-layer state discovery, we compare SCX with and without the second-layer error-driven encoder (i.e., using only first-layer ACE descriptors for state assignment).

[Table omitted — see original .tex]

The second layer improves F1 by 0.089 (11.4\% relative improvement), driven primarily by a substantial increase in recall (from 0.745 to 0.962). The error-driven encoder correctly identifies noisy frames in the thermal and MLMD states that the first-layer features alone misclassify as difficult-but-clean.

## Implementation Details and Hyperparameters
<!-- label: sec:S4 -->

### Software and Hardware

All experiments were conducted on a single CPU node for AlN (32 Intel Xeon cores, 128 GB RAM) and on CPUs for CIFAR-10, DermaMNIST, and DrugBank experiments. SCX code and experiment scripts are written in Python 3.8+ using PyTorch 1.12 for neural network models and scikit-learn 1.0 for clustering and evaluation. XGBoost 1.6 is used for the DrugBank tree-based experiments.

### SCX Hyperparameters

Table [ref] lists the SCX hyperparameters and their default values.

[Table omitted — see original .tex]

### Expert Training Protocols

**AlN MLIP.** Expert models are three-layer NequIP E(3)-equivariant message-passing networks with 64 latent channels, 3 interaction layers, and cutoff radius 5.0~\AA. Training uses the Adam optimizer with initial learning rate $10^{-3}$, batch size 16, and early stopping with patience 50 epochs (maximum 500 epochs). The loss function combines energy MSE (weight 1.0) and force MSE (weight 10.0). Each expert trains on approximately 45 disjoint frames. Total training time for all 12 experts: approximately 2 hours on a 32-core CPU node.

**CIFAR-10.** Expert models are SimpleCNN architectures: 3 convolutional layers (32, 64, 128 filters, 3$\times$3 kernel, stride 1, padding 1), each followed by ReLU and 2$\times$2 max pooling, then a fully-connected layer with 256 units and ReLU, then a 10-way softmax output. Training uses Adam with learning rate $10^{-3}$, cross-entropy loss, batch size 16, and 3 epochs per expert. Total training time for all 20 experts: approximately 45 minutes on CPU. We emphasize the 3-epoch constraint, which is a lower bound due to GPU budget limitations.

**DermaMNIST.** Expert models follow the same SimpleCNN architecture as CIFAR-10, with output dimension 7. Training protocol is identical (3 epochs, Adam, learning rate $10^{-3}$). For the ResNet-18 feature variant, we extract penultimate-layer activations from a ResNet-18 pretrained on ImageNet (frozen backbone, no fine-tuning).

**DrugBank.** Expert models are XGBoost classifiers with 100 estimators, max depth 6, learning rate 0.1, subsample 0.8, and colsample-by-tree 0.8. Each expert trains on approximately 540 disjoint drug-target pairs. The feature pipeline: Morgan fingerprints (2,048-bit, radius 2, computed with RDKit) concatenated with PseAAC protein features (50-dimensional, computed with the propy3 package), followed by PCA to 256 dimensions.

### Noise Injection Protocol

For the controlled noise experiments (CIFAR-10, DermaMNIST, DrugBank), we inject symmetric label noise at the specified rate $\eta$. For each sample in the selected subset, with probability $\eta$, we replace the true label $y^*$ with a uniformly random label from $\{1, ..., K_{\mathcal{Y}}\} \setminus \{y^*\}$. This ensures uniform noise across classes (Assumption A4). The random seed is fixed for reproducibility. For the AlN dataset, the noise labels are real (identified by domain expert consensus), not synthetically injected.

### Consistency Score Calibration

The state-dependent threshold $\tau(s)$ is calibrated as follows. For each state $s$, we compute the empirical mean $\bar{e}_s$ and standard deviation $\sigma_s$ of the consistency scores $\{C(x_i) : s_i = s\}$. The threshold is $\tau(s) = \bar{e}_s + \kappa\sigma_s$, where $\kappa = 2$ by default. This corresponds to approximately the 95th percentile of the clean-sample consistency distribution under a Normal approximation (which is justified by the Hoeffding bound when $M$ is large enough). For the adaptive threshold variant (Theorem~4'), we replace this with $\theta^\dagger$ from Equation~2 in the Methods section.

### Computational Cost Summary

[Table omitted — see original .tex]

All SCX runs complete on commodity hardware in under 2 hours. The most compute-intensive step is expert model training, which is embarrassingly parallel across workers.

### Data and Code Availability

The SCX implementation is available at [repository to be filled]. The AlN v3 dataset is available at [repository to be filled]. CIFAR-10 and DermaMNIST are publicly available benchmark datasets. DrugBank is available at https://go.drugbank.com.

### Cross-References to Companion Papers

Full theorem proofs and derivations of the bounds referenced in this work (Theorem~1: exponential detection guarantee; Theorem~2: weak feature bound; Theorem~3: The Honest Person Theorem; Theorem~4': exact constant minimax optimality; Proposition~6: bootstrap stability diagnostic) are provided in the companion Paper~I [cite], Supplementary Information Sections~S1--S8.

The Curation-Exploration Tradeoff framework, which explains why expert diversity must be allowed to develop before noise detection, is developed in the companion Paper~II [cite].

\begin{thebibliography}{10}

\bibitem{xi2025fundamental}
SCX. ``A Fundamental Impossibility in Data Quality: Distinguishing Label Noise from Sample Difficulty is Provably Unsolvable Without Explicit Assumptions.'' arXiv preprint (2025).

\bibitem{scx2025curation}
SCX. ``State-Conditioned Expertise and the Curation-Exploration Tradeoff.'' Working paper (2026).

\bibitem{northcutt2021confident}
C.~G.~Northcutt, L.~Jiang, and I.~L.~Chuang, ``Confident learning: estimating uncertainty in dataset labels,'' *Journal of Artificial Intelligence Research*, vol.~70, pp.~1373--1411, 2021.

\bibitem{cleanlab}
Cleanlab, ``cleanlab: the standard data-centric AI package for data quality and machine learning,'' https://github.com/cleanlab/cleanlab, 2022.

\bibitem{dawid1979maximum}
A.~P.~Dawid and A.~M.~Skene, ``Maximum likelihood estimation of observer error-rates using the EM algorithm,'' *Journal of the Royal Statistical Society: Series C*, vol.~28, no.~1, pp.~20--28, 1979.

\end{thebibliography}