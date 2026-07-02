---

## Detailed Comparison of SCX vs.\ Existing LLM Data Filtering Methods

Table [ref] presents a detailed comparison of SCX's proposed LLM data curation framework against nine existing families of methods. For each method, we evaluate the core idea, the signal it uses, its explicit or implicit assumptions about data quality, its relationship to SCX, and its primary limitations.

\begin{table*}[t]

*Caption:* Comprehensive comparison of SCX vs.\ existing LLM data curation methods. SCX's primary differentiator is that it treats judge reliability as a learnable, state-conditioned quantity rather than assuming uniform judge quality across all data.
<!-- label: tab:comparison -->
\resizebox{!}{%
[Table omitted — see original .tex]
}
\end{table*}

### Key Differentiators

The comparison reveals three key differentiators of the SCX framework:

**1. State-conditioned reliability estimation.**
Every existing method implicitly assumes that its quality signal is uniformly reliable across all data. Rule-based filters use global thresholds; LLM-as-a-judge applies the same model uniformly; influence methods compute the same gradient metric for every sample. SCX is the only framework that explicitly learns *when* each signal is reliable and *when* it is not, and adjusts its aggregation accordingly.

**2. Multi-signal integration.**
Current methods are largely single-signal: they use one type of filter, one classifier, or one LLM judge. SCX provides a principled framework for combining multiple signals, with weights learned from data. This is particularly valuable when different judges have complementary strengths (e.g., GPT-4 for reasoning, Claude for safety, Llama for code).

**3. Redundancy-aware value.**
Most methods compute a per-sample quality score independently. SCX incorporates the dataset context through the redundancy term $R(s; \mathcal{D})$, which captures the diminishing marginal returns of adding more samples from an already-saturated state. This addresses a known pathology of single-sample scoring methods: they tend to select ``pretty but repetitive'' data.

### Where SCX Does Not Compete

We emphasize that SCX does not replace most of these methods. Rather, it integrates them:

- Rule-based filters provide inexpensive initial quality signals.
- LLM judges provide strong but expensive quality scores.
- Influence methods provide high-fidelity per-sample value estimates.
- SCX *orchestrates* these signals: it learns when to use each one, how to weight them, and how to account for redundancy.

This layering approach is intentional: SCX complements rather than competes with existing methods, which is appropriate given the high switching costs of replacing existing data curation pipelines.

## Mathematical Formalization of the Four Challenges

### Challenge 1: The Representation-Value Gap

Let $\phi: \cX \to \R^d$ be a feature map (e.g., sentence embedding) and let $V: \cX \to \R$ be the training value of a sample, defined as the marginal improvement in expected model performance on a held-out evaluation set when $x$ is added to the training set.

> **Definition:** [Representation-Value Gap]
> Define the **representation-value gap** as:
> 
> $$
> \gamma(\phi) = \inf_{g: \R^d \to \R  is  L-Lipschitz} \E[|V(x) - g(\phi(x))|],
> <!-- label: eq:rep_value_gap -->
> $$
> 
> where the infimum is over $L$-Lipschitz functions $g$ for a fixed Lipschitz constant $L < \infty$.

A large $\gamma(\phi)$ means that no Lipschitz function of the embedding can approximate the true training value---equivalently, samples with similar embeddings can have very different training value.

> **Proposition:** [Gap Lower Bound]
> For any fixed $d$, there exists a data distribution over $\cX$ and a training procedure such that:
> 
> $$
> \gamma(\phi) \geq \frac{1}{2} \cdot \max\left(0,\; 1 - \frac{L \cdot diam(\phi(\cX))}{2}\right),
> <!-- label: eq:gap_lower_bound -->
> $$
> 
> where $diam(\phi(\cX)) = \sup_{x,x' \in \cX} \|\phi(x) - \phi(x')\|_2$.

> **Proof:** Construct two samples $x_1, x_2$ with $\phi(x_1) = \phi(x_2)$ (identical embeddings) but $V(x_1) = 1$, $V(x_2) = 0$. Since $g(\phi(x_1)) = g(\phi(x_2))$ for any function $g$, we have $\max(|V(x_1) - g(\phi(x_1))|, |V(x_2) - g(\phi(x_2))|) \geq 1/2$. The diam term accounts for the constraint that $g$ is Lipschitz (though in the case $\phi(x_1) = \phi(x_2)$, Lipschitzness imposes no restriction). The diam term matters when embeddings are pulled apart.

**Implication for SCX.** The representation-value gap is the LLM analogue of the feature weakness problem (Theorem~2 in [cite]). In the original SCX setting, $\phi$ is a physical descriptor for which $\gamma(\phi)$ is empirically small. For text embeddings, $\gamma(\phi)$ is plausibly large. This means SCX's state discovery---which clusters on $\phi$---may produce states that are not meaningful for training value, limiting the benefit of state-conditioned aggregation.

**Proposed diagnostic.** Analogous to Proposition~6 in [cite], we propose a validation diagnostic: train a small probe model on a subset of data with known quality scores, compute $\gamma(\phi)$ empirically via cross-validation of a learned predictor $g$, and reject the SCX approach if $\gamma(\phi)$ exceeds a threshold (e.g., $\gamma(\phi) > 0.3$ on a normalized scale).

### Challenge 2: Ill-Defined Error Signal

In the SCX supervised setting, the data generation process is:

$$
y^* &\sim P(Y^* \mid x) \quad (true label) 

z &\sim Bernoulli(\eta) \quad (noise indicator) 

y &= \begin{cases}
y^* & if  z = 0 

Uniform(\cY \setminus \{y^*\}) & if  z = 1
\end{cases}
<!-- label: eq:supervised_dgp -->
$$

The ground truth label $y^*$ exists (if unobserved), and the noise event $z$ is well-defined.

For LLM data, there is no analogous generative process. An instruction--response pair $(x, y)$ does not have a ``true'' label distinct from the observed $y$ in any meaningful sense. Quality is a multi-dimensional, task-dependent, and often subjective judgment.

> **Definition:** [LLM Data Quality Proxy]
> Let $\cT = \{T_1, ..., T_K\}$ be a set of evaluation tasks. Define the **proxy quality** of sample $(x, y)$ as:
> 
> $$
> q(x, y; \cT) = \frac{1}{K} \sum_{k=1}^K \mathbb{E}_{m \sim P(M \mid \mathcal{D} \cup \{(x,y)\})} [Acc_k(m)] - \mathbb{E}_{m \sim P(M \mid \mathcal{D})} [Acc_k(m)],
> <!-- label: eq:proxy_quality -->
> $$
> 
> where $P(M \mid \mathcal{D})$ is the distribution over models trained on dataset $\mathcal{D}$, and $Acc_k(m)$ is the accuracy of model $m$ on task $T_k$. This measures the expected marginal contribution of $(x,y)$ to performance on $\cT$.

This definition is theoretically principled but practically intractable (requires training many models). Current methods use tractable proxies:

- Loss on a reference model: $q_(x, y) = -\log p_{ref}(y \mid x)$.
- Judge score: $q_J(x, y) = LLM-Judge(x, y)$.
- Disagreement: $q_D(x, y) = -Var_{j \in \cJ}[Q_j(x, y)]$.

> **Proposition:** [Proxy Inconsistency]
> There exist distributions over $\cX \times \cY$ and model families such that for two samples $x_1, x_2$:
> 
> $$
> q_(x_1) < q_(x_2) \quad but \quad q(x_1; \cT) > q(x_2; \cT),
> <!-- label: eq:proxy_inconsistency -->
> $$
> 
> and vice versa. Any monotonic transformation of a single proxy fails to recover the true quality ordering.

> **Proof:** Take $x_1$: a common pattern (e.g., ``The capital of France is Paris'') with low perplexity but near-zero marginal value (already in the training set). Take $x_2$: a rare but correct fact (e.g., ``The capital of Kiribati is South Tarawa'') with higher perplexity but positive marginal value. The reference model has low perplexity on $x_1$ but near-zero perplexity reduction from adding it. The true quality $q(x_1; \cT) \approx 0$ while $q(x_2; \cT) > 0$, but $q_(x_1) \gg q_(x_2)$. The reverse direction follows by symmetric construction.

**Implication for SCX.** This means that SCX's consensus-based noise detection cannot rely on any single proxy as ground truth. The SCX-LLM framework must either (a) use multiple complementary proxies and cross-validate, (b) restrict to settings where a specific proxy is known to be reliable (e.g., verifiable tasks), or (c) abandon the notion of ground truth entirely and output only relative risk scores. Option (c) is the most honest and is the approach we adopt in the main text.

### Challenge 3: Non-Local Value

Let $\mathcal{D}$ be the training set and $\theta(\mathcal{D})$ be the optimal model parameters trained on $\mathcal{D}$.

> **Definition:** [Non-Local Value]
> Define the **value** of sample $x$ given dataset $\mathcal{D}$ as:
> 
> $$
> V(x \mid \mathcal{D}) = \mathbb{E}_[\ell(\theta(\mathcal{D} \cup \{x\}); \cT) - \ell(\theta(\mathcal{D}); \cT)],
> <!-- label: eq:nonlocal_value -->
> $$
> 
> where $\ell(\theta; \cT)$ is the expected loss on evaluation tasks $\cT$.

> **Proposition:** [Non-Locality Lower Bound]
> There exist datasets $\mathcal{D}_1 \subset \mathcal{D}_2$ and a sample $x$ such that:
> 
> $$
> |V(x \mid \mathcal{D}_1) - V(x \mid \mathcal{D}_2)| \geq \frac{1}{2} \max(V(x \mid \mathcal{D}_1), V(x \mid \mathcal{D}_2)),
> <!-- label: eq:nonlocality_bound -->
> $$
> 
> i.e., the value of a sample can change by at least $50\%$ depending on the dataset context.

> **Proof:** (Sketch) Let $\mathcal{D}_1$ contain no physics documents, and $\mathcal{D}_2$ contain 10,000 physics documents. Let $x$ be a physics question. Then $V(x \mid \mathcal{D}_1) > 0$ (fills a gap) while $V(x \mid \mathcal{D}_2) \approx 0$ (redundant). The minimum of the two is zero; the maximum is positive, giving $|V(x \mid \mathcal{D}_1) - V(x \mid \mathcal{D}_2)| = \max(V(x \mid \mathcal{D}_1), V(x \mid \mathcal{D}_2))$, which exceeds $\frac{1}{2}\max$.

**Implication for SCX.** This non-locality violates the state-homogeneity assumption (A5 in [cite]), which requires that within each state, the error distribution is approximately constant. In the LLM setting, a ``state'' (e.g., physics documents) can transition from high-value (when the dataset has few physics documents) to low-value (when physics is saturated), violating the assumption that $\mu_s$ is stationary.

**Proposed mitigation.** Rather than treating states as static, we propose *adaptive state occupancy tracking*: maintain an estimate of each state's representation in the current training set, and adjust the redundancy penalty $R(s; \mathcal{D})$ in [ref] accordingly. This makes the SCX value estimate context-dependent, as it should be.

### Challenge 4: Redundancy $\neq$ Similarity

Let $sim(x, x')$ be a similarity measure (e.g., cosine similarity of embeddings).

> **Definition:** [Capability-Based Redundancy]
> For a set of tasks $\cT$, define the **capability redundancy** of state $s$ with respect to dataset $\mathcal{D}$ as:
> 
> $$
> R_(s; \mathcal{D}) = 1 - \frac{\mathbb{E}[\ell(\theta(\mathcal{D} \setminus \mathcal{D}_s); \cT) - \ell(\theta(\mathcal{D}); \cT)]}{\mathbb{E}[\ell(\theta(\mathcal{D}_s); \cT) - \ell(\theta(\emptyset); \cT)]},
> <!-- label: eq:capability_redundancy_formal -->
> $$
> 
> where $\mathcal{D}_s = \{x \in \mathcal{D}: s(x) = s\}$ and $\ell(\theta; \cT)$ is expected loss on $\cT$. $R_(s; \mathcal{D}) \approx 1$ means removing state $s$ causes minimal degradation (high redundancy); $R_(s; \mathcal{D}) \approx 0$ means removing $s$ causes maximal degradation (low redundancy).

> **Proposition:** [Similarity $\neq$ Redundancy]
> There exist $x_1, x_2, x_3 \in \cX$ such that:
> 
> $$
> sim(x_1, x_2) &\gg sim(x_1, x_3) \quad (embeddings similar) 

> R_(\{x_1, x_2\}; \mathcal{D}) &\gg R_(\{x_1, x_3\}; \mathcal{D}) \quad (different redundancy)
> <!-- label: eq:sim_neq_redundancy -->
> $$
> 
> i.e., similarity-based redundancy measures misclassify samples with respect to capability-based redundancy.

> **Proof:** (Sketch) Let $x_1 = $``The square of (a+b) equals $a^2 + 2ab + b^2$'' (algebra), $x_2 = $``The derivative of $x^2$ is $2x$'' (calculus), $x_3 = $``$(a+b)^2 = a^2 + 2ab + b^2$'' (same algebra, different wording). Then $sim(x_1, x_2) < sim(x_1, x_3)$ (surface similarity), but for a capability $\cT$ measuring mathematical reasoning, $R_(\{x_1, x_2\}; \emptyset) < R_(\{x_1, x_3\}; \emptyset)$ (two algebra problems offer less new reasoning capability than one algebra plus one calculus).

**Implication for SCX.** The SCX compression theorem [cite] relies on the assumption that within each state, removing ``similar'' samples does not harm performance. If similarity does not correspond to redundancy, aggressive compression will remove valuable samples. The proposed remedy (\S [ref] of the main text) is to define redundancy at the *state* level rather than the *sample* level: compress entire states that are saturated, rather than compressing individual similar samples.

## Reformulation of SCX Core Equations for LLM Setting

We provide a self-contained reformulation of the key SCX equations adapted for the LLM data curation context.

### State-Conditioned Judge Aggregation

Given $J$ judges with per-state reliability estimates $\{A_j(s)\}_{j=1}^J$ and sample $x$ with state $s(x)$:

$$
Q_{SCX}(x) &= \sum_{j=1}^J w_j(s(x)) \cdot Q_j(x) <!-- label: eq:supp_aggregation --> 

w_j(s) &= \frac{\exp(\alpha \cdot A_j(s) - \lambda \cdot C_j)}{\sum_{j'=1}^J \exp(\alpha \cdot A_{j'}(s) - \lambda \cdot C_{j'})} <!-- label: eq:supp_weights -->
$$

 where $C_j$ is the per-sample evaluation cost of judge $j$ and $\alpha, \lambda \geq 0$ are hyperparameters.

### Redundancy-Corrected Value

$$
V_{SCX}(x) &= Q_{SCX}(x) \cdot \bigl(1 - \beta \cdot R(s(x); \mathcal{D})\bigr) <!-- label: eq:supp_value --> 

R(s; \mathcal{D}) &= \frac{|\mathcal{D}_s|}{N} \cdot \left(1 - \frac{1}{|\mathcal{D}_s|^2} \sum_{x,x' \in \mathcal{D}_s} \frac{\phi(x)^\top \phi(x')}{\|\phi(x)\|\|\phi(x')\|}\right)^{-1} <!-- label: eq:supp_redundancy -->
$$

 where $\mathcal{D}_s = \{x \in \mathcal{D}: s(x) = s\}$, $N = |\mathcal{D}|$, and $\beta \in [0, 1]$ controls the strength of the redundancy penalty. The redundancy measure in [ref] combines data quantity (first term) with within-state diversity (second term, inverted).

### Multi-Judge Risk Score

$$
\rho(x) = \frac{1}{J} \sum_{j=1}^J \mathbf{1}\{Q_j(x) < \tau_j(s(x))\},
<!-- label: eq:supp_risk -->
$$

 where $\tau_j(s)$ is the $\alpha$-quantile (e.g., $\alpha = 0.2$) of judge $j$'s scores on a held-out calibration set for state $s$. The risk score $\rho(x) \in [0, 1]$ represents the fraction of judges that assign low quality to $x$.

### Contextual Bandit Objective for Judge Selection

$$
\max_ &\quad \sum_{x \in \mathcal{D}} Q_{SCX}(x; \pi) <!-- label: eq:supp_bandit_obj --> 

s.t. &\quad \sum_{x \in \mathcal{D}} Cost(\pi(x), x) \leq B, 
$$

 where $\pi: \mathcal{X} \to \{1, ..., J\}$ maps samples to judges, $Q_{SCX}(x; \pi)$ is the quality estimate using only judge $\pi(x)$ (weighted by the state-conditioned reliability of that judge), and $B$ is the total evaluation budget. This is a contextual bandit with state context $s(x)$ and $J$ actions.

### State Discovery Stability Validation

Following Proposition~6 of [cite], we validate the discovered state partition $\hat{\mathcal{S}}$ via bootstrap stability:

$$
S(\Phi, K) = \frac{1}{B} \sum_{b=1}^B ARI\bigl(k-means(\Phi, K),\; k-means(\Phi^{(b)}, K)\bigr),
<!-- label: eq:supp_stability -->
$$

 where $\Phi$ is the $N \times d$ embedding matrix, $\Phi^{(b)}$ is a bootstrap resample, and ARI is the adjusted Rand index between the two clusterings. We adopt the heuristic threshold: $S(\Phi, K) > 0.7$ indicates reliable state discovery; $S(\Phi, K) < 0.5$ indicates the features are too weak for SCX to provide meaningful benefit.

## Additional Experiment Design Details

### Noise Injection Protocol

For the minimal viable experiment (\S [ref]), we inject known noise into three categories:

- **Factual errors** (40\% of injected noise): Replace named entities (people, locations, dates) with incorrect alternatives in factual text. Example: ``The CEO of NVIDIA is Jen-Hsun Huang'' $\to$ ``The CEO of NVIDIA is Satya Nadella.''
- **Reasoning errors** (35\%): Introduce subtle logical flaws in step-by-step reasoning. Example: Change ``If $x > 5$, then $x + 2 > 7$'' to ``If $x > 5$, then $x + 2 > 5$'' (true but weaker claim) graded as correct.
- **Response corruption** (25\%): For instruction-following data, replace the correct response with a plausible but incorrect one. Example: ``Summarize the water cycle'' $\to$ response about the carbon cycle.

Each sample receives exactly one type of noise (or none if it is in the clean subset). The noise injection is calibrated to produce a 10\% overall noise rate, with noise proportionally distributed across the four domain states.

### Evaluation Metrics

Beyond the primary F1 metric, we track:

- **Calibration error** (ECE): Whether the SCX risk score $\rho(x)$ is well-calibrated with respect to known noise, measured as expected calibration error.
- **State-conditional F1**: F1 per state, to detect whether SCX benefits are concentrated in specific domains.
- **Judge agreement rate**: $\frac{2}{J(J-1)} \sum_{i<j} \mathbb{P}(Q_i(x) \approx Q_j(x))$ where $\approx$ indicates both are above/below their state-specific thresholds. High agreement suggests the state structure is informative.
- **Total cost**: API query costs for each method, enabling cost-effectiveness analysis.

### Statistical Significance

All comparisons use bootstrapped 95\% confidence intervals (1,000 resamples). The null hypothesis test uses a paired permutation test: for each sample, the F1 contributions of SCX and the best single judge are paired, and the null distribution of the F1 difference is estimated by randomly flipping signs.

## Connections to SCX Theoretical Framework

For completeness, we document which SCX theorems from [cite] apply (with modifications) and which do not.

[Table omitted — see original .tex]

The key observation is that SCX's *negative* results (unidentifiability, weak feature failure) transfer cleanly to the LLM setting, while its *positive* results (detection guarantees, optimality) do not. This asymmetry is precisely why we position SCX as a meta-evaluation layer rather than a direct noise detection method for LLM data.

## Summary of Open Problems

We conclude this supplementary material by listing the open problems that must be resolved for the SCX-LLM framework to be practically impactful:

1. **Representation-value gap**: Can we construct text representations that are more aligned with training value than current sentence embeddings? This is the most fundamental problem.
2. **Noise-free reliability estimation**: How can we estimate per-state judge reliability $A_j(s)$ without ground truth data? Consensus-based approaches have identifiability problems; calibration sets are expensive.
3. **Adaptive state tracking**: States are not stationary---as the training set evolves, the value distribution across states shifts. How can state occupancy and redundancy be tracked efficiently at scale?
4. **Scalable orchestration**: The contextual bandit formulation requires learning per-state judge reliability, which requires samples. How can we achieve reasonable cold-start performance when a new state is encountered?
5. **Causality of data selection**: Does selecting data via SCX-induced scores actually cause better model performance, or does it merely correlate with other selection criteria? Causal identification of data selection effects is an open problem.
6. **Goodhart resilience**: Can SCX's multi-state, multi-judge structure be made robust to strategic gaming by data producers? This requires understanding the incentive structure of the data curation ecosystem.

These open problems define the research agenda for the SCX-LLM program. Progress on any one would be a significant contribution; progress on a combination would be transformative.

\begin{thebibliography}{10}

\bibitem{penedo2023refinedweb}
Penedo, G. *et al.* RefinedWeb: A high-quality web dataset for LLM pretraining. *arXiv preprint arXiv:2306.01116* (2023).

\bibitem{scx2026}
SCX. A fundamental impossibility in data quality: Distinguishing label noise from sample difficulty is provably unsolvable without explicit assumptions. *arXiv preprint* (2026).

\bibitem{wenzek2020quality}
Wenzek, G. *et al.* Quality at a glance: An audit of web-crawled multilingual datasets. *Transactions of the ACL* **8**, 688--703 (2020).

\bibitem{lin2024rho}
Lin, J. *et al.* Rho-1: Not all tokens are what you need. *arXiv preprint arXiv:2404.07965* (2024).

\bibitem{carlini2023quantifying}
Carlini, N. *et al.* Quantifying memorization across neural language models. *International Conference on Learning Representations* (2023).

\bibitem{xie2023dsir}
Xie, S. M. *et al.* Data selection for language models via importance resampling. *Advances in Neural Information Processing Systems* **36** (2023).

\bibitem{xia2024less}
Xia, M. *et al.* LESS: Selecting influential data for targeted instruction tuning. *International Conference on Machine Learning* (2024).

\bibitem{choe2024loga}
Choe, S. *et al.* LoGra: Local gradient analysis for data selection. *arXiv preprint arXiv:2405.18260* (2024).

\bibitem{zheng2024judging}
Zheng, L. *et al.* Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *Advances in Neural Information Processing Systems* **36** (2024).

\bibitem{abbas2023semdedup}
Abbas, A. *et al.* SemDeDup: Data-efficient learning at web-scale through semantic deduplication. *arXiv preprint arXiv:2303.09540* (2023).

\bibitem{li2024dclm}
Li, J. *et al.* DataComp-LM: In search of the next generation of training sets for language models. *arXiv preprint arXiv:2406.11794* (2024).

\end{thebibliography}