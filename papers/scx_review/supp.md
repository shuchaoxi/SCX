# Supplementary Information: 
 Domain-Specific Adaptations, Mathematical Reference, and Glossary

---

## Domain-Specific Algorithm Adaptations
<!-- label: sec:adaptations -->

Table [ref] summarizes the SCX algorithm configuration for each of the six domains surveyed in the main text. The columns correspond to the SCX protocol steps: feature representation $\phi(x)$, state discovery method, number of states $K_{\mathcal{S}}$, number of experts $M$, consensus metric, threshold strategy (Tier), and validation status.

[Table omitted — see original .tex]

[Table omitted — see original .tex]

### SCX Tier Selection Guide
<!-- label: sec:tier-guide -->

The appropriate SCX tier depends on computational budget, available domain knowledge, and noise characteristics:

- **Tier 0 (Loss Baseline)**: One model, no SCX. Use when $\varepsilon_\phi > 0.5$, or when compute is insufficient for even $M=5$ experts.
- **Tier 1 (SCX + Hoeffding)**: $M+1$ models + k-means. Use for prototyping; simplest implementation. F1 guarantee from Theorem~1.
- **Tier 2 (SCX + Chernoff/KL)**: Same compute as Tier~1; tighter bound via Chernoff information $\kappa$. Use when Tier~1's $M$ requirement seems too large.
- **Tier 3 (SCX + Adaptive $\theta_{opt}$)**: Same as Tier~1/2 plus $\eta$ estimation. Use for best F1; critical when $\eta$ is extreme ($<0.05$ or $>0.5$).
- **Tier 4 (SCX + Bootstrap)**: Adds $B$ bootstrap resamples. Use when $\eta$ and $\Delta$ are unknown; provides diagnostic before full SCX commitment.

Minimum expert count: $M_ = \max(5, \lceil \ln(1/(\eta \varepsilon_{target}))/(2\Delta^2) \rceil)$ for Tier~1, or $\max(5, \lceil \ln(1/(\eta \varepsilon_{target}))/\kappa \rceil)$ for Tiers~2--3.

## Complete Mathematical Reference
<!-- label: sec:math-ref -->

This section summarizes the SCX mathematical theory, cross-referencing Paper~I (``A Fundamental Impossibility in Data Quality'') for complete proofs. All theorems are stated without proof here; the unified theorem document  [cite] serves as the single source of truth.

### Assumption Catalog (A1--A6)
<!-- label: sec:assumptions -->

All SCX theorems build on subsets of these six assumptions:

1. [A1] **Disjoint Training Sets**: Expert models are trained on disjoint data subsets $D_m \sim \mathcal{D}^{n_m}$, $D_m \cap D_{m'} = \varnothing$, $D_m \perp D_{m'}$.
2. [A2] **Conditional Independence (Clean)**: Expert errors $\{e_m(x,y)\}_{m=1}^M$ are conditionally independent given $x$ for clean samples.
3. [A3] **Bounded Loss**: The loss function $\ell(a,b) \in [0, B]$, $B < \infty$.
4. [A4] **Uniform Independent Noise**: Noise events are independent of $x$ and $D_m$; noise labels are uniform over $\mathcal{Y}\setminus\{y^*\}$.
5. [A5] **State Homogeneity**: $\sup_{x\in s} \mathbb{E}[C \mid clean, X=x] \leq \mu_s$ per state $s$.
6. [A6] **Balanced Error Distribution**: $\max_{c\neq y^*} \mu_c(x) \leq C_{bal} \cdot \mu_s/(K_{\mathcal{Y}}-1)$.

Minimal subsets that break Theorem~3's unidentifiability: $\{A1, A4, A5\}$, $\{A1, A4, A6\}$, or $\{A5, A6\}$ with $|\mathcal{S}| \geq 2$.

### Theorem Statements
<!-- label: sec:theorems -->

#### Theorem 1: Noise Detection Guarantee
Under A1--A6, the SCX noise detector with state-dependent threshold $\theta$ satisfying $\mu_s < \theta < 1 - C_{bal}\cdot\mu_s/(K_{\mathcal{Y}}-1)$ achieves:

$$
F1 \geq 1 - \frac{1}\sum_{s\in\mathcal{S}} \rho_s \cdot \exp\bigl(-2M\Delta_s^2\bigr),
$$

where $\Delta_s = \min(\theta - \mu_s,\; 1 - C_{bal}\cdot\mu_s/(K_{\mathcal{Y}}-1) - \theta) > 0$ is the state-level separation gap.

**Key corollary**: As $M \to \infty$, $F1 = 1 - O_P(\frac{1} e^{-2M\Delta_^2})$.

**Reference**: Paper~I, Section~1;  [cite], Section~1.

#### Theorem 2: Weak Feature Failure Lower Bound
Let $\phi: \mathcal{X} \to \mathbb{R}^{d_\phi}$ satisfy $I(\phi(X); S) \leq \delta$ (in nats). Then:

$$
F1_{SCX} &\leq F1_{base} + C_F\sqrt{\delta/2}, 

AUC_{SCX} &\leq AUC_{base} + \sqrt{\delta/2}(1/\eta + 1/(1-\eta)).
$$

**Key corollary**: When $\delta / \log K_{\mathcal{S}} > 0.5$, SCX cannot outperform the loss baseline.

**Reference**: Paper~I, Section~2;  [cite], Section~2.

#### Theorem 3: The Honest Person Theorem
For any $K \geq 2$, $M \geq 1$, and finite $\mathcal{S}$, there exist $\mathcal{P}_{noise}$ and $\mathcal{P}_{hard}$ with identical observable joint distributions such that any algorithm has minimax error $\geq \eta\rho/2$ on the ambiguous subset.

**Reference**: Paper~I, Section~3;  [cite], Section~3.

#### Theorem 4': Exact Constant Minimax Optimality
Let $p_0 = \mu_s$, $p_1 = 1 - C_{bal}\cdot\mu_s/(K_{\mathcal{Y}}-1)$, with Chernoff information $\kappa = C(Bern(p_0), Bern(p_1))$ and Chernoff point $\theta^*$. The SCX detector with adaptive threshold $\theta^\dagger = \theta^* + \frac{1}{M}\frac{\log((1-\eta)/\eta)}{D^*} + O(1/M^2)$ achieves:

$$
\lim_{M\to\infty} e^{M\kappa}\sqrt{2\pi M}\cdot(1-F1_{SCX}) = \frac{C_},
$$

where $C_ = \frac{2}(\frac{1-\eta})^s \frac{1/\lambda_0^* + 1/|\lambda_1^*|}{\sqrt{\theta^*(1-\theta^*)}}$, $s = |\lambda_1^*|/D^*$, and $D^* = \log\frac{p_1(1-p_0)}{p_0(1-p_1)}$.

**Matching lower bound**: For any algorithm $\mathcal{A}$, $\liminf e^{M\kappa}\sqrt{2\pi M}\cdot(1-F1_{\mathcal{A}}) \geq C_/\eta$.

**Reference**: Paper~I, Section~4;  [cite], Section~4.

#### Theorem 5: Fixed-K State Discovery Consistency
Under sub-Gaussian noise with variance proxy $\sigma^2$ and strong separation $\Delta_ = \min_{i\neq j} \|\mu_i - \mu_j\|_2 > 0$, Lloyd's k-means with $R = C_R \log n$ initializations recovers the true partition with probability:

$$
P(\hat{\mathcal{C}}^{(n)} \neq \mathcal{C}^*  up to permutation) \leq K_{\mathcal{S}} \cdot \exp\!\left(-c_1 \frac{n_ \Delta_^2}{\sigma^2 d_\phi}\right) + o(1).
$$

**Reference**: Paper~I, Section~5;  [cite], Section~5.

#### Proposition 6: Bootstrap Stability Diagnostic
For feature vectors $\{\phi(x_i)\}_{i=1}^N$ and $K_{\mathcal{S}}$ states, let $S(\Phi, K)$ be the mean ARI between full-data and bootstrap clusterings. Then:

- Strong features $\Rightarrow$ high stability: $S(\Phi, K) > 1 - \varepsilon$.
- No state structure $\Rightarrow$ low stability: $\mathbb{E}[S(\Phi, K)] = O(K/\sqrt{N})$.
- Diagnostic: $S(\Phi, K) < 0.7$ suggests features too weak for SCX to outperform baseline.

**Reference**: Paper~I, Section~6;  [cite], Section~6.

### Theorem Dependency Graph
<!-- label: sec:dependency -->

\begin{verbatim}
Theorem 3 (Unidentifiability) ──── provides necessity for ────→ A1-A6
                                                                   │
                                                                   ▼
Theorem 1 (Noise Detection) ──── positive result under A1-A6 ──→ F1 ≥ 1 - O(e^{-2MΔ²})
        │
        │ provides error model (Bernoulli(p₀), Bern(p₁))
        ▼
Theorem 4' (Exact Constant) ──── refines Thm 1's rate ────────→ exact constant κ
        │
        │ provides expert error model
        ▼
Theorem 2 (Weak Feature) ──── limits when features δ-weak ──→ F1_SCX ≤ F1_base + O(√δ)
        │
        │ positive counterpart: strong features ⇒ state discovery succeeds
        ▼
Theorem 5 (Cluster Consistency) ──── recovery of true partition ─→ exp(-c·n_min·Δ²_min)
        │
        │ practical diagnostic for Thm 2's δ
        ▼
Proposition 6 (Stability Diag.) ──── bootstrap stability test ──→ S(Φ,K) > 0.7
\end{verbatim}

## Glossary of SCX Terminology
<!-- label: sec:glossary -->

\begin{longtable}{p{0.25\textwidth} p{0.70\textwidth}}
\toprule
**Term** & **Definition** 

\midrule
\endhead

\bottomrule
\endfoot

**State** ($s$) & A partition of the input space $\mathcal{X}$ such that samples within a state have homogeneous expert error characteristics. Discovered via k-means on feature representation $\phi(X)$. States are the fundamental unit of SCX analysis: all statistical guarantees are per-state. Denoted $s \in \mathcal{S}$, with $K_{\mathcal{S}} = |\mathcal{S}|$. 

**Consensus score** ($C(x)$) & The fraction of $M$ experts that fail to predict the given label for sample $x$: $C(x) = \frac{1}{M}\sum_{m=1}^M \mathbf{1}\{\ell(f_m(x), y) > \tau\}$. Expected value on clean samples is $\mu_s$ (low); on noisy samples is $\approx 1 - \mu_s/(K-1)$ (high). 

**Separation gap** ($\Delta_s$) & For state $s$, the minimum distance from threshold $\theta$ to the expected consensus scores of clean and noisy samples: $\Delta_s = \min(\theta - \mu_s,\; 1 - C_{bal}\mu_s/(K-1) - \theta)$. Controls the exponential rate of F1 convergence. 

**Noise rate** ($\eta$) & The global proportion of label noise in the dataset: $\eta = \mathbb{P}(label flipped)$. Critical parameter for adaptive thresholding and bound validity. Typical range: 0.05--0.30. 

**Feature weakness** ($\delta$) & The mutual information between feature representation $\phi(X)$ and true state $S$: $\delta = I(\phi(X); S)$. Normalized form: $\varepsilon_\phi = \delta / \log K_{\mathcal{S}}$. Governs whether SCX can outperform the loss baseline. 

**Chernoff information** ($\kappa$) & The asymptotic exponential rate of best achievable error probability for distinguishing $Bern(p_0)$ from $Bern(p_1)$: $\kappa = C(Bern(p_0), Bern(p_1)) = \min_{t\in[0,1]} \log \sum p_0^t p_1^{1-t}$. Always smaller than $2\Delta^2$. 

**Adaptive threshold** ($\theta^\dagger$) & The noise-rate-aware threshold $\theta^\dagger = \theta^* + \frac{1}{M}\frac{\log((1-\eta)/\eta)}{D^*} + O(1/M^2)$, where $\theta^*$ is the Chernoff point and $D^*$ is the total log-odds. Achieves minimax optimal constant. 

**Curation-Exploration Tradeoff** & The principle that premature data cleaning (curation before exploration) destroys the signal needed to distinguish noise from hardness. Formalized as $Curation(t) = f(Exploration(t))$, with exploration rate $\eta(t)$ governing the tradeoff. 

**State-conditioned expertise** & The property whereby different expert models develop distinct specializations across data states due to training on different subsets or with different seeds. The foundation for the SCX routing and noise detection mechanisms. 

**Minimax optimality** (exact constant) & An algorithm is exact constant minimax optimal if it achieves the lower bound $\liminf e^{M\kappa}\sqrt{2\pi M}(1-F1) \geq C_/\eta$ with equality---i.e., no other algorithm can achieve a smaller error constant, even asymptotically. SCX with $\theta^\dagger$ is exact constant minimax optimal. 

**Bootstrap ARI** ($S(\Phi, K)$) & Mean adjusted Rand Index (ARI) between k-means clusterings on the full data and on bootstrap resamples. Values $>0.7$ indicate strong feature structure (SCX likely beneficial); values $<0.3$ indicate weak structure (SCX likely futile). 

**Chernoff point** ($\theta^*$) & The unique threshold that equalizes the KL divergences of clean and noisy error distributions: $KL(\theta^*\|p_0) = KL(\theta^*\|p_1)$. Also called the ``minimax threshold.'' Closed form: $\theta^* = \frac{\log((1-p_0)/(1-p_1))}{\log(p_1(1-p_0)/(p_0(1-p_1)))}$. 

**Consistency score** (state) ($C(s)$) & For a state $s$, the consistency score measures label purity within the cluster. High $C(s)$ indicates that samples within a state share the same label, suggesting the state captures a meaningful data partition. 

**Noise score** ($NS(x)$) & Per-sample noise score combining residual and state-level metrics: $NS(x_i) = r_i / (\rho(s) + \varepsilon) \cdot (1 - C(s))$, where $r_i$ is the residual (loss), $\rho(s)$ is the state proportion, and $C(s)$ is the state consistency. 

**Expert noise error rate** ($p_1$) & The expected consensus score on noisy samples within a state. Under uniform noise (A4): $p_1 = 1 - C_{bal}\cdot \mu_s/(K_{\mathcal{Y}}-1)$. 

**Expert clean error rate** ($p_0$) & The expected consensus score on clean samples within a state. Equal to $\mu_s$, the state-level clean error rate upper bound (A5). 

**Chernoff constant** ($C_$) & The multiplicative factor in the exact minimax F1 lower bound: $C_ = \frac{2}(\frac{1-\eta})^s \frac{1/\lambda_0^* + 1/|\lambda_1^*|}{\sqrt{\theta^*(1-\theta^*)}}$. Aggregates over multiple bottleneck states via $C_{global} = \sum_{s: \kappa_s = \kappa_{global}} \rho_s C_s$. 

**Total log-odds** ($D^*$) & The sum of log-odds at the Chernoff point: $D^* = \lambda_0^* + |\lambda_1^*| = \log\frac{p_1(1-p_0)}{p_0(1-p_1)}$. Controls the $O(1/M)$ threshold shift. 

**Exponent fraction** ($s$) & $s = |\lambda_1^*|/D^* \in (0,1)$. Governs how the noise prior $((1-\eta)/\eta)^s$ factors into the minimax constant. When $\eta = 1/2$, $s$ determines the symmetry of the threshold adaptation. 

\end{longtable}

### Notation Quick Reference

\begin{longtable}{p{0.12\textwidth} p{0.30\textwidth} p{0.50\textwidth}}
\toprule
**Symbol** & **Meaning** & **Context** 

\midrule
\endhead

\bottomrule
\endfoot

$\mathcal{X}$ & Input space & Domain of data samples 

$\mathcal{Y}$ & Label space & $|\mathcal{Y}| = K_{\mathcal{Y}}$ classes 

$\mathcal{S}$ & State space & $|\mathcal{S}| = K_{\mathcal{S}}$ states 

$s(x)$ & True state assignment & Unobserved, estimated via clustering 

$\phi(x)$ & Feature representation & Input to state discovery 

$C(x)$ & Consensus score & Fraction of experts that err on $x$ 

$\eta$ & Noise rate & Proportion of mislabeled samples 

$\mu_s$ & State clean error bound & Expected consensus on clean samples 

$\theta$ & Detection threshold & State-dependent decision boundary 

$\Delta_s$ & Separation gap & Signal-to-noise ratio in state $s$ 

$\kappa$ & Chernoff information & Asymptotic error exponent 

$M$ & Number of experts & Ensemble size 

$\rho_s$ & State proportion & $\mathbb{P}(X \in s)$ 

$C_{bal}$ & Error balance constant & Controls error concentration ($\geq 1$) 

$\varepsilon_\phi$ & Normalized feature weakness & $\delta / \log K_{\mathcal{S}}$ 

$\delta$ & Feature-state mutual info & $I(\phi(X); S)$ in nats 

$\theta^*$ & Chernoff point & Minimax threshold 

$\theta^\dagger$ & Adaptive threshold & $\eta$-aware optimal threshold 

$\lambda_0^*, \lambda_1^*$ & Saddlepoints & At Chernoff point 

$D^*$ & Total log-odds & $D^* = \lambda_0^* + |\lambda_1^*|$ 

$s$ & Exponent fraction & $|\lambda_1^*|/D^*$ 

$C_$ & Minimax constant & Exact constant in F1 lower bound 

$\eta(t)$ & Exploration rate & Time-dependent curation aggressiveness 

$S(\Phi, K)$ & Bootstrap ARI & Clustering stability score 

$\tau$ & Stability threshold & Heuristic $= 0.7$ for SCX reliability 

$\Delta_$ & Min cluster separation & Theorem 5's separation condition 

$n_$ & Min per-state samples & Theorem 5's sample condition 

$\sigma^2$ & Variance proxy & Sub-Gaussian noise parameter 

\end{longtable}

### Typical Parameter Values

\begin{longtable}{p{0.30\textwidth} p{0.15\textwidth} p{0.15\textwidth} p{0.30\textwidth}}
\toprule
**Scenario** & $\eta$ & $\Delta$ & **Recommended $M$** 

\midrule
\endhead

\bottomrule
\endfoot

MLIP (ACE, 500 frames) & 0.10--0.20 & 0.25--0.50 & 8--12 

Medical imaging (50K images) & 0.05--0.10 & 0.30--0.50 & 10--15 

CIFAR-10 (ResNet, 50K images) & 0.08--0.10 & 0.35--0.50 & 8--10 

Drug targetome (15K molecules) & 0.05--0.15 & 0.30--0.60 & 4--8 (pipeline layers) 

Large-scale web dataset (10M) & 0.01--0.05 & 0.40--0.60 & 20--24 

Small dataset ($N < 500$) & Unknown & Unknown & 5--8 (bootstrap) 

\end{longtable}

### Cross-Reference to Paper~I Supplementary Information

The full theoretical development with complete proofs is organized in Paper~I's Supplementary Information as follows:

\begin{longtable}{p{0.12\textwidth} p{0.40\textwidth} p{0.40\textwidth}}
\toprule
**SI Section** & **Content** & **Pages (est.)** 

\midrule
\endhead

\bottomrule
\endfoot

A.1 & Notation and Assumptions & 2 

A.2 & Theorem 1: Noise Detection (Lemmas 1--3) & 6 

A.3 & Theorem 2: Weak Feature Failure (Pinsker-TV chain) & 5 

A.4 & Theorem 3: Unidentifiability (K=2 and K$>$2 constructions) & 4 

A.5 & Theorem 4': Exact Constant (Lemmas A--F, Bahadur-Rao, Chernoff) & 12 

A.6 & Theorem 5: Cluster Consistency (Lemmas 1--4) & 8 

A.7 & Proposition 6: Bootstrap Stability & 3 

A.8 & Numerical Verification Tables & 1 

\end{longtable}

<div align="center">

\rule{0.5\textwidth}{0.5pt}

</div>

**References**

\bibliographystyle{plain}
\begin{thebibliography}{5}

\bibitem{theorems_unified}
SCX Mathematical Theory: Unified Theorem Document. *Technical report* (2026). Available at: [repository]-theory.

\bibitem{engineering_guide}
SCX Engineering Practice Guide. *Technical report* (2026).

\bibitem{paperI}
SCX. A Fundamental Impossibility in Data Quality. *arXiv preprint* (2026).

\bibitem{paperII}
SCX. The Curation-Exploration Tradeoff. *In preparation* (2026).

\bibitem{paperIII}
SCX. Training Data Quality Dominates Model Architecture. *In preparation* (2026).

\end{thebibliography}