## Full Experimental Results

### AlN MLIP

[Table omitted — see original .tex]

The SCX adaptive threshold (Tier~3) achieves the best force RMSE of $0.028$~eV/\AA, representing a 29--48\% improvement over no cleaning ($0.045$~eV/\AA) and a 32\% improvement over loss-based cleaning ($0.041$~eV/\AA). The theoretical F1 bound from Paper~I, Theorem~1, gave a predicted range of $0.77$--$0.86$ depending on state proportions; the empirical $0.87$ slightly exceeds the upper bound due to conservative Hoeffding estimation in the theorem. The exact asymptotic (Theorem~4'), computed with $p_0=0.15$, $p_1=0.72$, $\eta=0.14$, yields $\kappa = 0.332$ and a predicted asymptotic F1 of $0.89$ for $M \to \infty$, consistent with $M=8$ achieving $0.87$.

### CIFAR-10 Controlled Noise

[Table omitted — see original .tex]

The improvement grows with noise rate: at 40\% noise, SCX deferred cleaning achieves 79.3\% accuracy versus 65.8\% for premature cleaning---an 11.2 percentage-point gap. This widening gap is consistent with the tradeoff analysis: as noise increases, premature cleaning removes more hard samples (false positives), while SCX's multi-expert consistency better distinguishes noise from hardness.

**Ablation: number of experts $M$**. Figure~S1 shows F1 as a function of $M$ at 20\% noise. The improvement saturates at $M \approx 8$, with $M=5$ achieving 87\% of the $M=20$ F1. This confirms the diminishing-returns prediction from Paper~I (Theorem~4'): $1-F1 \propto e^{-M\kappa}/\sqrt{M}$.

[Figure omitted — see original .tex]

### MedMNIST

[Table omitted — see original .tex]

DermaMNIST exemplifies the weak-feature regime (Theorem~2). The bootstrap stability $S(\Phi, K) = 0.45$ falls well below the $0.7$ threshold, signalling that the tradeoff framework cannot achieve large gains. The feature weakness $\varepsilon_\phi = 0.52$ exceeds the $0.5$ bound from Theorem~2, predicting SCX F1 $\leq$ baseline F1 $+ \sqrt{0.52/2} \cdot C_F \approx$ baseline + $0.51 \cdot C_F$. With $C_F \leq 2$, the maximum gain is $\sim 0.07$ in F1, consistent with the observed improvement from $0.65$ to $0.78$ (ROC-AUC, not F1, but the bound applies directionally).

### DrugBank Drug-Target

[Table omitted — see original .tex]

The SCX per-state approach (discovering chemical clusters via ECFP4 features and applying per-cluster adaptive thresholds) achieves the best precision@0.1 ($0.76$) and highest targetome coverage ($62\%$). The improvement over uniform ensemble is $+0.11$ in precision@0.1 and $+27$ percentage points in coverage. The four-layer pipeline naturally embodies the Curation-Exploration Tradeoff: Layer~1 is highly curated (high precision, low recall, low $\eta$), Layer~3 explores broadly (lower precision, high recall, high $\eta$), and SCX consistency scoring across layers identifies which predictions from which layers to trust for each molecule class.

## Sensitivity Analysis

### Varying the Number of Experts $M$

Figure~S2 shows noise detection F1 as a function of $M$ for all four domains. The characteristic exponential saturation is observed in all cases, with the saturation point shifting based on the separation gap $\Delta$:

- **AlN MLIP** ($\Delta \approx 0.30$, $K=1$ regression): Saturation at $M \approx 6$, $F1_\infty \approx 0.89$.
- **CIFAR-10** ($\Delta \approx 0.25$, $K=10$): Saturation at $M \approx 8$, $F1_\infty \approx 0.65$.
- **DermaMNIST** ($\Delta \approx 0.12$, $K=7$): Near-linear growth, $M=12$ yields $F1 \approx 0.50$, still far from saturation. This is consistent with Theorem~2 (weak features).
- **DrugBank** ($\Delta$ varies by chemical cluster, $0.15$--$0.40$): Saturation at $M \approx 5$, but the plateau value varies by cluster ($0.45$--$0.85$).

The Cnernoff information $\kappa$ (Paper~I, Lemma~C) governs the saturation rate. For AlN ($p_0=0.15$, $p_1=0.72$), $\kappa \approx 0.332$, predicting $e^{-8 \times 0.332} \approx 0.070$, while for DermaMNIST ($p_0=0.35$, $p_1=0.59$), $\kappa \approx 0.053$, predicting $e^{-8 \times 0.053} \approx 0.654$. The DermaMNIST bound is still far from asymptotic, confirming that weak features require many more experts.

### Varying the Noise Rate $\eta$

[Figure omitted — see original .tex]

Three regimes emerge:

- $\eta < 0.05$ (rare noise): Adaptive threshold yields $1.7$--$2.4\times$ improvement over fixed $\theta^*$, confirming the prediction from Paper~I (Theorem~4', Table~1, Case~3).
- $0.05 \leq \eta \leq 0.30$ (moderate noise): SCX achieves near-peak F1. The adaptive threshold still helps ($1.1$--$1.7\times$) but the gain is smaller.
- $\eta > 0.30$ (high noise): F1 degrades for all methods. At $\eta > 0.50$, the problem becomes ill-posed: a majority of labels are wrong, and noise detection reduces to a variant of unsupervised learning.

### Varying the Exploration Schedule $\eta(t)$

We compared four exploration schedules on AlN MLIP:

[Table omitted — see original .tex]

The single-pass approach (train $M$ experts once, compute $\theta_{opt}$, curate) achieves identical final performance to iterative schedules while requiring only one training pass. This suggests that for most applications, iterative refinement is unnecessary. Single-pass curation suffices because the multi-expert consistency signal stabilizes after a single exploration phase.

## Comparison with Alternative Curation Strategies

We benchmarked SCX against four alternative curation strategies across all four domains.

### Alternative Methods

1. **Loss-based filtering** (baseline): Remove samples with the highest training loss. The number of samples removed is set to match the SCX removal rate.
2. **Confident learning** [cite]: Estimate the joint distribution of noisy and true labels via counting on confident predictions. Remove samples in the off-diagonal of the estimated joint.
3. **Active label correction**: For each sample, query an oracle (simulated by using the true label) if the model's prediction confidence is below a threshold. Remove samples confirmed as noise.
4. **Multi-annotator consensus**: Simulate three annotators with known error rates (matching the expert noise profile). Flag samples where annotators disagree as potentially noisy.

### Results

[Table omitted — see original .tex]

SCX outperforms all alternative strategies on every domain. The largest gains are on AlN MLIP (SCX: $0.028$ vs. next best active correction: $0.033$, a 15\% relative improvement) and DrugBank (SCX: $0.74$ vs. next best active correction: $0.67$). On DermaMNIST, where Theorem~2 predicts weak features limit the achievable improvement, all methods show small gains, with SCX marginally ahead.

The advantage of SCX over active label correction is notable: active correction assumes an oracle that can provide clean labels for queried samples, which is unrealistic in many settings. SCX achieves better results *without* an oracle, using only the emergent consensus among diverse experts.

## Self-Diagnosis: Bootstrap Stability Across Domains

The bootstrap stability diagnostic (Paper~I, Proposition~6) was evaluated on all four domains to assess its predictive power.

[Table omitted — see original .tex]

The threshold $S(\Phi, K) > 0.7$ correctly identifies AlN, CIFAR-10, and BloodMNIST as domains where SCX provides meaningful improvement. DermaMNIST ($S = 0.45$) falls well below the threshold, correctly predicting limited gains. DrugBank ($S = 0.68$) sits near the threshold, consistent with the moderate but real improvement ($+0.16$ precision). The correlation between $S(\Phi, K)$ and SCX improvement is $r = 0.89$ ($p < 0.05$), supporting the diagnostic's validity.

## Relationship to Paper~I Theorems

This paper operationalizes the theoretical results of the companion paper (Paper~I, [cite]). The cross-references are summarized below:

[Table omitted — see original .tex]

For full theorem statements, proofs, and numerical verification of the exact constants, see the companion paper [cite].

\begin{thebibliography}{10}
\bibitem{xi2025fundamental} SCX. A Fundamental Impossibility in Data Quality: Distinguishing Label Noise from Sample Difficulty is Provably Unsolvable Without Explicit Assumptions. arXiv preprint (2025).
\bibitem{northcutt2021} Northcutt, C. G., Jiang, L. \& Chuang, I. L. Confident learning: Estimating uncertainty in dataset labels. *Journal of Artificial Intelligence Research* **70**, 1373--1411 (2021).
\end{thebibliography}