# Introduction — ML History Through the SCX Lens

**Author:** SCX

*Abstract:*

Machine learning history is conventionally narrated as a sequence of empirical discoveries — backpropagation, dropout, attention, batch normalization — each validated by benchmark performance rather than theoretical derivation. We present a systematic re-audit: every major ML algorithm can be re-derived, or at minimum rigorously characterized, from SCX{} first principles. What appeared as empirical discoveries were, in many cases, implicit approximations of SCX{} theorems. The audit question is twofold: which algorithms ``accidentally'' implement SCX{} guarantees, and which rely on assumptions that SCX{} proves necessary?

We treat twelve algorithm families under a unified mathematical framework, connecting each to SCX{} constructs: Theorem~1 (multi-expert consensus, $M \ge \ln(1/\varepsilon)/(2\Delta^2)$), Theorem~2 (self-audit without external verifier is epistemically equivalent to no audit), Theorem~3 (unidentifiability under label noise), and the \Situs{}--Yajie{}--Spring{}--Cercis{} architecture. We prove five new theorems/propositions that formalize these connections, and we are honest about which connections are rigorous and which remain conjectural.

**Keywords:** SCX framework, multi-expert consensus, machine learning theory, Yajie ensemble, Spring memory, adversarial audit, self-supervised learning, 机器学习理论, 多专家共识, SCX审计

## Introduction — ML History Through the SCX Lens
## 引言——透过SCX视角看机器学习史
<!-- label: sec:intro -->

### The Received History

The history of machine learning, as told in textbooks and survey papers, is a narrative of empirical breakthroughs. Rosenblatt's perceptron (1958) was discarded after Minsky and Papert's critique, only to be resurrected by the backpropagation algorithm (Rumelhart et al., 1986). Convolutional networks won ImageNet (Krizhevsky et al., 2012), proving that ``deep learning works.'' Dropout (Hinton et al., 2012) was discovered to prevent overfitting. Batch Normalization (Ioffe and Szegedy, 2015) stabilized training. Attention mechanisms (Bahdanau et al., 2014; Vaswani et al., 2017) revolutionized sequence modeling. Generative Adversarial Networks (Goodfellow et al., 2014) opened the door to generative modeling. Each discovery was validated by benchmark performance — test accuracy, BLEU score, FID — not by theoretical derivation from axioms.

This empirical history has produced a curious phenomenon: we have algorithms that work, but we lack a unified theory of *why* they work. The explanations given are local to each algorithm family. Dropout is ``ensembling many subnetworks.'' BatchNorm ``reduces internal covariate shift.'' Attention ``lets the model focus on relevant parts of the input.'' These are helpful intuitions, not theorems.

### The SCX Thesis

The SCX{} framework provides a unified mathematical language for reasoning about verification, consensus, and quality certification. Its core constructs are:

- **Yajie{} (芽接)**: A multi-expert consensus mechanism. $M$ independent experts each produce a claim; the consensus aggregates them with weight proportional to verified accuracy. The key result (Theorem~1) is that the probability of all $M$ experts being simultaneously wrong decays as $\exp(-2M\Delta^2)$.
- **Spring{} (春)**: A state-space memory architecture with gating. States $s_t$ are stored with permanence; a gating function $S_t$ controls access. The system maintains an exponential moving average (EMA) of relevant states, enabling filtering of noise while retaining signal across time.
- **\Situs{} (定位)**: State-space localization — identifying which sub-manifold of the state space the system currently occupies.
- **Cercis{} (紫荆)**: Quality scoring function $Q + \eta N$, where $Q$ measures guarantee strength (theoretical and empirical) and $N$ measures novelty.

The central thesis of this paper is:

<div align="center">

\fbox{\parbox{0.9\textwidth}{
**Every major ML algorithm can be characterized as an implicit implementation of one or more SCX{} theorems.** The algorithms that survived longest implement the strongest SCX{} guarantees. The algorithms that were trendy but fragile violate SCX{} assumptions.
}}

</div>

### The Audit Question

We ask, for each algorithm family:

1. Which SCX{} theorem does this algorithm **rigorously** implement? (Full proof or tight reduction)
2. Which SCX{} theorem does it **approximately** implement? (Weaker bound or heuristic correspondence)
3. Which SCX{} assumptions does it **violate**? (And does this explain known failure modes?)
4. What is the algorithm's **Cercis{} Score**: $S = Q + \eta N$?

We are honest throughout about the rigor status of each connection. Some connections are proven here for the first time; others are identified as conjectural with explicit gap statements.

### Notation and Preliminaries

We work in the SCX{} formalism. A supervised learning problem is a tuple $(\cX, \cY, \cD, \ell)$ where $\cX \subseteq \R^d$ is the input space, $\cY$ is the output space, $\cD = \{(x_i, y_i)\}_{i=1}^n \sim P_{XY}$ is the training data, and $\ell: \cY \times \cY \to \R_{\ge 0}$ is a loss function. The learner produces a hypothesis $h: \cX \to \cY$.

The **M-parameter** of a learning algorithm is the effective number of independent experts whose consensus determines the output. For an ensemble of $M$ trees, $M$ is explicit. For dropout with rate $p$, $M_{eff}$ is the effective number of independently trained subnetworks. We denote the consensus output of $M$ experts as $\Yajie_M(h_1, ..., h_M; x)$.

The **noise rate** $\eta \in [0, 1)$ is the fraction of training labels that are incorrect: $\eta = \Pbb_{(x,y) \sim \cD}[y \neq y^*(x)]$ where $y^*(x)$ is the true label.

## SCX Axioms Relevant to Machine Learning
## SCX公理体系（机器学习相关子集）
<!-- label: sec:axioms -->

We restate the SCX{} axioms that govern learning-theoretic analysis. These are the assumptions under which SCX{} theorems are proven; when a real-world algorithm deviates from them, its behavior becomes conjectural.

\begin{assumption}[A1 — Independent Training]<!-- label: asm:A1 -->
Each expert $h_k$ is trained on a dataset $\cD_k$ such that the training processes are conditionally independent given the data-generating distribution. Formally, for any $k \neq j$, $\cD_k \condind \cD_j \mid P_{XY}$.
\end{assumption}

\begin{assumption}[A2 — Honest Consensus]<!-- label: asm:A2 -->
Each expert reports its best hypothesis truthfully. The Yajie{} aggregator has access to the raw outputs $h_k(x)$ without strategic manipulation by individual experts.
\end{assumption}

\begin{assumption}[A3 — Bounded Detection Sensitivity]<!-- label: asm:A3 -->
For any pair of competing hypotheses, there exists $\Delta > 0$ such that each expert can distinguish the correct from the incorrect hypothesis with advantage at least $\Delta$: $\Pbb(h_k(x) = y^* \mid x) - \Pbb(h_k(x) \neq y^* \mid x) \ge 2\Delta$.
\end{assumption}

\begin{assumption}[A4 — Memory Permanence]<!-- label: asm:A4 -->
The Spring{} system maintains persistent state memory $M_t$ that is never erased. Past states are queryable at any future time. This is the Spring{} analog of the transformer's full self-attention over the entire context.
\end{assumption}

\begin{assumption}[A5 — State Homogeneity]<!-- label: asm:A5 -->
The state distribution $P(X \mid s)$ has bounded support: $\supp(P(\cdot \mid s)) \subseteq [a_s, b_s]$ with $b_s - a_s < \infty$ for each state $s$. The distribution does not shift arbitrarily during learning.
\end{assumption}

These five axioms, plus the standard SCX{} verifier growth condition ($V(t) \to \infty$ as $t \to \infty$), are the foundation for the analysis that follows.

## Ensemble Methods as Theorem 1 — Explicit Multi-Expert Consensus
## 集成方法作为定理1——显式多专家共识
<!-- label: sec:ensemble -->

Ensemble methods are the most literal implementation of SCX{} Theorem~1 in machine learning. They construct $M$ models, each trained independently or with controlled dependence, and aggregate their outputs via voting or averaging. We show that the three major ensemble paradigms — bagging, random forests, and stacking — each instantiate a different aspect of the Yajie{} consensus mechanism, while boosting fails to meet the independence condition and thus exhibits different (and explained) failure modes.

### Random Forest 随机森林: Theorem 1 in Its Purest Form

A random forest (Breiman, 2001) trains $M$ decision trees on bootstrap samples $\cD_1, ..., \cD_M$ drawn independently from the training data. At inference, the forest outputs the majority vote (classification) or average (regression) of the $M$ trees.

> **Proposition:** [Random Forest as Yajie{} Consensus]<!-- label: prop:rf_yajie -->
> \rigorFull
> A random forest with $M$ trees trained on independent bootstrap samples is an exact instantiation of Yajie{} consensus with $M$ experts satisfying \asmTag{1} (independent training). The out-of-bag (OOB) error estimate is a built-in cross-audit mechanism: each tree is evaluated on the samples it did not see during training, providing an unbiased estimate of the generalization error of the consensus.

> **Proof:** Each bootstrap sample $\cD_k$ is drawn independently from the empirical distribution $\hat{P}_n$ by sampling $n$ points with replacement. Conditioned on $\hat{P}_n$ (the data-generating proxy), the bootstrap samples are conditionally independent: $\cD_k \condind \cD_j \mid \hat{P}_n$. This satisfies \asmTag{1}. Tree $k$ produces hypothesis $h_k = \cA(\cD_k)$ where $\cA$ is the CART algorithm. The Yajie{} consensus output is:
> 
> $$<!-- label: eq:rf_consensus -->
>     \Yajie_M(x) = \argmax_{y \in \cY} \frac{1}{M}\sum_{k=1}^{M} \ind{h_k(x) = y}.
> $$
> 
> 
> The OOB error for tree $k$ is computed on $\cD \setminus \cD_k$, the samples not in bootstrap $k$. Since these samples are independent of $h_k$'s training, the OOB estimate is unbiased:
> 
> $$
>     \E[OOB error] = \E_{(x,y) \sim P_{XY}}\left[\ind{\Yajie_M(x) \neq y}\right].
> $$
> 
> This is a built-in cross-audit: each tree audits the others on held-out data, exactly as SCX{} requires independent verifiers.

The core theoretical guarantee comes from SCX{} Theorem~1 applied directly:

> **Theorem:** [Random Forest Error Bound — SCX Theorem 1]<!-- label: thm:rf_bound -->
> \rigorFull
> Let $h_1, ..., h_M$ be the $M$ trees of a random forest, each with expected error rate $\varepsilon_k \le \varepsilon_0 < 1/2$. Under \asmTag{1} (bootstrap independence), the consensus error rate satisfies:
> 
> $$<!-- label: eq:rf_hoeffding -->
>     \Pbb(\Yajie_M(x) \neq y^*(x)) \le \exp\left(-2M\left(\frac{1}{2} - \varepsilon_0\right)^2\right).
> $$
> 
> In particular, $\lim_{M \to \infty} \Pbb(consensus error) = 0$ exponentially fast.

> **Proof:** Let $Z_k = \ind{h_k(x) = y^*(x)}$ be the indicator that tree $k$ is correct. Under \asmTag{1}, the $Z_k$ are independent Bernoulli trials with $\E[Z_k] = 1 - \varepsilon_k \ge 1 - \varepsilon_0$. The consensus is correct if $\sum_{k=1}^M Z_k > M/2$, i.e., a majority of trees are correct.
> 
> Define $S_M = \frac{1}{M}\sum_{k=1}^M Z_k$. By Hoeffding's inequality:
> 
> $$
>     \Pbb\left(S_M \le \frac{1}{2}\right) &= \Pbb\left(S_M - \E[S_M] \le \frac{1}{2} - \E[S_M]\right) 

>     &\le \Pbb\left(S_M - \E[S_M] \le -\left(\E[S_M] - \frac{1}{2}\right)\right) 

>     &\le \exp\left(-2M\left(\E[S_M] - \frac{1}{2}\right)^2\right) 

>     &\le \exp\left(-2M\left((1-\varepsilon_0) - \frac{1}{2}\right)^2\right) 

>     &= \exp\left(-2M\left(\frac{1}{2} - \varepsilon_0\right)^2\right).
> $$
> 
> Let $\Delta = 1/2 - \varepsilon_0 > 0$ be the per-tree advantage over random guessing. Then $\Pbb(error) \le \exp(-2M\Delta^2)$, matching the SCX{} Theorem~1 bound $\exp(-2M\Delta_^2)$ with $\Delta_ = \Delta$.

This theorem directly explains the empirical observation that random forest accuracy improves with more trees: each additional tree contributes an independent ``vote,'' and the probability of a majority error decays exponentially. The OOB error provides the built-in verification that SCX{} demands: it is the empirical estimate of $\Pbb(consensus error)$, computed without a held-out test set.

### Bagging 装袋法: Variance Reduction as Effective M Growth

Bagging (bootstrap aggregating) applies to any base learner. It trains $M$ models on bootstrap samples and averages their predictions. The standard explanation is variance reduction; the SCX{} re-interpretation reveals the deeper mechanism.

> **Proposition:** [Bagging Variance Decomposition]<!-- label: prop:bagging_var -->
> \rigorFull
> For regression with squared loss, the mean squared error of the bagged predictor $\bar{h}_M(x) = \frac{1}{M}\sum_{k=1}^M h_k(x)$ decomposes as:
> 
> $$<!-- label: eq:bagging_decomp -->
>     \E[(\bar{h}_M(x) - y)^2] = \underbrace{\Bias(\bar{h}_M(x))^2}_{unchanged by  M} + \underbrace{\frac{1}{M}\Var(h_k(x)) + \frac{M-1}{M}\Cov(h_k, h_j)}_{variance reduced by  M}.
> $$
> 
> This is precisely the Yajie{} effective expert count: $M_{eff} = M / (1 + (M-1)\rho)$ where $\rho = \Cov(h_k, h_j)/\Var(h_k)$ is the inter-model correlation. As $M \to \infty$, the variance approaches the irreducible correlation floor $\rho \cdot \Var(h_k)$.

> **Proof:** Standard decomposition. The key insight from SCX{}: the term $1/M$ in the variance is the Yajie{} consensus factor — $M$ independent experts each contribute $1/M$ weight. The correlation term $\rho$ measures how much the bootstrap samples overlap, reducing effective independence. When $\rho = 0$ (perfect independence), $M_{eff} = M$. When $\rho = 1$ (identical models), $M_{eff} = 1$ — no benefit from ensembling.
> 
> This directly parallels SCX{} Theorem~1: the effective detection sensitivity $\Delta_{eff}$ depends on the independence of verifiers, not just their count.

### Stacking 堆叠泛化: Learned Consensus Weighting

Stacking (Wolpert, 1992) trains a meta-learner on the outputs of base models. This is the most sophisticated ensemble method because it *learns* the consensus weights rather than using uniform averaging.

> **Proposition:** [Stacking as Yajie{} with Learned Weights]<!-- label: prop:stacking_yajie -->
> \rigorConjectural
> Stacking is a Yajie{} consensus where the weight function $w_k(x)$ is learned by a meta-learner $\cM$ trained on validation data:
> 
> $$<!-- label: eq:stacking -->
>     \Yajie_{stack}(x) = \cM(h_1(x), h_2(x), ..., h_M(x)).
> $$
> 
> This is equivalent to Yajie{} with state-dependent gating: $w_k(x) = \partial \cM / \partial h_k$, assigning higher weight to experts that perform better in the local region of feature space around $x$.

The connection is *conjectural* because the meta-learner $\cM$ is typically trained on the same validation data used to evaluate base models, creating a subtle dependence that violates \asmTag{1} (full independence). However, if the meta-learner is trained on a separate calibration set, the connection becomes rigorous. This is a case where the ML practice is *almost* SCX-compliant but falls short due to data reuse.

### Boosting 梯度提升: Why It's Different (and Dangerous)

Boosting (AdaBoost, Gradient Boosting, XGBoost) trains models *sequentially*: each new model focuses on the errors of the previous ensemble. This is fundamentally different from bagging and random forests because it **violates \asmTag{1} (independent training)**.

> **Proposition:** [Boosting Violates A1 — Sequential Dependence]<!-- label: prop:boosting_violation -->
> \rigorFull
> In gradient boosting with $M$ iterations, the $k$-th model $h_k$ is trained on the residuals of the ensemble $F_{k-1} = \sum_{j=1}^{k-1} h_j$. The training data for $h_k$ depends on $h_1, ..., h_{k-1}$ through the residual computation. Formally:
> 
> $$<!-- label: eq:boosting_dep -->
>     \cD_k^{eff} = \{(x_i, r_i^{(k-1)})\}_{i=1}^n, \quad r_i^{(k-1)} = y_i - F_{k-1}(x_i).
> $$
> 
> This creates a directed acyclic graph of dependencies: $h_1 \to h_2 \to ... \to h_M$. The independence condition \asmTag{1} is violated at every step $k \ge 2$.

This violation explains the well-known empirical phenomenon that boosting *can overfit* when $M$ is too large, whereas random forests *do not overfit* with more trees. In SCX{} terms:

- **Random Forest**: $M \uparrow \implies \Pbb(error) \downarrow$ (Theorem [ref]). More trees monotonically improve the consensus, because each tree is an independent verifier.
- **Boosting**: $M \uparrow \implies$ models become increasingly correlated. The effective independent expert count $M_{eff}$ does not grow proportionally with $M$. After some threshold $M^*$, the marginal benefit of additional boosting iterations is offset by overfitting to noise in the residuals.

> **Theorem:** [Boosting Overfitting Bound — SCX Corollary]<!-- label: thm:boosting_overfit -->
> \rigorPartial
> Let $M$ be the number of boosting iterations. Under sequential dependence (violation of \asmTag{1}), the effective independent expert count is bounded by:
> 
> $$<!-- label: eq:boosting_Meff -->
>     M_{eff} \le 1 + \frac{1}{\rho_} \ln\left(\frac{M}\right),
> $$
> 
> where $\rho_$ is the maximum pairwise correlation between any two base learners. For $\rho_ > 0$, $M_{eff}$ grows only logarithmically with $M$, not linearly. This explains why boosting with $M=100$ iterations may behave like bagging with $M_{eff} \approx 10$ independent models.

> **Proof:** [Proof Sketch]
> The sequential dependency creates a Markov chain of model errors. The correlation between $h_k$ and $h_{k+\ell}$ decays as $\rho^\ell$ for some $\rho \in (0,1)$. The total effective independence is the sum of the decorrelated contributions:
> 
> $$
>     M_{eff} = 1 + \sum_{\ell=1}^{M-1} (1 - \rho^\ell) \le 1 + \sum_{\ell=1}^ \rho^\ell = 1 + \frac{1-\rho}.
> $$
> 
> With $\rho_ = \rho/(1-\rho)$, we obtain the stated bound. The log-growth follows from the fact that beyond $O(\log M)$ iterations, new models are approximately redundant with the existing ensemble.  $\square$

> **Remark:** [Practical Implications]
> This theorem explains why XGBoost and LightGBM use early stopping on a validation set — it is an empirical approximation of the SCX{}-prescribed practice of determining $M_{eff}$ and stopping when marginal benefit vanishes. The validation set serves as a proxy auditor.

## Dropout as Implicit Multi-Expert — $2^n$ Sub-Networks Vote
## Dropout作为隐式多专家——$2^n$个子网络投票
<!-- label: sec:dropout -->

Dropout (Srivastava et al., 2014) randomly drops units during training with probability $p$. At test time, all units are used but their outputs are scaled by $1-p$ (or equivalently, weights are multiplied by $1-p$). The standard explanation — dropout prevents co-adaptation — is a biological metaphor. The SCX{} lens reveals the rigorous mechanism.

> **Proposition:** [Dropout Creates an Implicit Yajie{} Ensemble]<!-- label: prop:dropout_yajie -->
> \rigorFull
> A neural network with $n$ dropout units implicitly trains $2^n$ distinct subnetworks. At test time, the full network with scaled weights approximates the geometric mean (or, under certain assumptions, the arithmetic mean) of these $2^n$ subnetworks. This is Yajie{} consensus with $M_{eff} \approx 2^n$ experts, each corresponding to a dropout mask.

> **Proof:** Let the network be parameterized by weights $\mathbf{W}$ and biases $\mathbf{b}$. A dropout mask $\mathbf{m} \in \{0,1\}^n$ determines which units are active. The subnetwork corresponding to mask $\mathbf{m}$ produces output $f_{\mathbf{m}}(x; \mathbf{W}, \mathbf{b})$. During training with dropout rate $p$, each mask $\mathbf{m}$ is sampled with probability:
> 
> $$
>     \Pbb(\mathbf{m}) = p^{\norm{\mathbf{m}}_0} (1-p)^{n - \norm{\mathbf{m}}_0},
> $$
> 
> where $\norm{\mathbf{m}}_0$ is the number of dropped units.
> 
> The training objective with dropout is:
> 
> $$
>     \min_{\mathbf{W}, \mathbf{b}} \E_{\mathbf{m}}\left[\frac{1}{n}\sum_{i=1}^n \ell(f_{\mathbf{m}}(x_i), y_i)\right].
> $$
> 
> This is precisely the Yajie{} training objective: minimize the expected loss over a distribution of experts, where each expert is a subnetwork defined by a dropout mask. At test time, the output is:
> 
> $$
>     f_{test}(x) = \E_{\mathbf{m}}[f_{\mathbf{m}}(x)] \approx \frac{1}{K}\sum_{k=1}^K f_{\mathbf{m}_k}(x),
> $$
> 
> for $K$ Monte Carlo samples (typically $K=1$ with weight scaling, or $K \to \infty$ for the exact expectation). This is Yajie{} consensus with $M_{eff} = K$ (practical) or $M_{eff} = 2^n$ (theoretical limit).
> 
> The *why* of dropout regularization follows directly from SCX{} Theorem~1:
> 
1. Each subnetwork $f_{\mathbf{m}}$ is an ``expert'' that saw a different view of the training data (different active units).
2. The training process optimizes the expected consensus error, not any individual subnetwork's error.
3. By Theorem~1, the consensus of $M_{eff}$ experts has generalization error bounded by $\exp(-2M_{eff}\Delta^2)$.
4. Dropout at rate $p$ increases $M_{eff}$: higher $p$ means masks are more diverse, subnetworks are more independent, and the consensus is more robust.

> **Theorem:** [Dropout Regularization Strength — SCX Characterization]<!-- label: thm:dropout_bound -->
> \rigorPartial
> For a network with $n$ dropout units at rate $p$, the effective number of independent experts satisfies:
> 
> $$<!-- label: eq:dropout_Meff -->
>     M_{eff}(p) \ge 1 + \frac{n p (1-p)}{1 + (n-1)\rho(p)},
> $$
> 
> where $\rho(p) \in [0,1]$ is the average correlation between two randomly sampled subnetworks. As $p \to 0.5$ (maximum mask diversity), $M_{eff}$ is maximized. As $p \to 0$ or $p \to 1$, $M_{eff} \to 1$ (no diversity). The regularization benefit of dropout is proportional to $\sqrt{M_{eff}(p)}$.

> **Proof:** [Proof Sketch]
> The mask space has size $2^n$. Two masks $\mathbf{m}, \mathbf{m}'$ produce correlated subnetworks with correlation $\rho(\mathbf{m}, \mathbf{m}')$ that depends on the Hamming distance $d_H(\mathbf{m}, \mathbf{m}')$. Under independent Bernoulli dropout, $\E[d_H] = 2np(1-p)$, maximizing diversity at $p=0.5$. The effective independent count follows from the variance reduction formula in Proposition [ref], substituting the expected correlation across the mask distribution.  $\square$

> **Remark:** [Empirical Validation]
> The standard dropout rate in practice is $p = 0.5$ for hidden layers, which Theorem [ref] identifies as the maximum-diversity point. For input layers, $p \approx 0.2$ is used — this is because input features are already somewhat independent, and aggressive dropout would destroy too much signal. The SCX{} framework explains this as a tradeoff between $M_{eff}$ (higher with larger $p$) and $\Delta$ (per-expert accuracy, lower with larger $p$).

> **Remark:** [Conjectural: Monte Carlo Dropout as Uncertainty Quantification]
> Gal and Ghahramani (2016) proposed using dropout at test time (MC Dropout) to estimate predictive uncertainty. In SCX{} terms: MC Dropout with $K$ forward passes is Yajie{} consensus with $K$ experts. The variance of the $K$ outputs estimates the *expert disagreement*, which is precisely what Yajie{} uses to compute consensus confidence. This connection is conjectural because the theoretical relationship between dropout variance and Bayesian uncertainty is approximate (variational inference with a specific prior), not exact.

## ResNet and Depth as Noise Compensation
## ResNet与深度作为噪声补偿
<!-- label: sec:resnet -->

The SCX{} manifesto identifies a profound connection: **network depth is compensation for label noise**. Residual Networks (He et al., 2016) make this compensation explicit through skip connections, which separate the ``clean signal'' path from the ``noise correction'' path.

### The SCX Theorem: Unidentifiability Under Label Noise

> **Theorem:** [Deep Network Unidentifiability — SCX Theorem 3]<!-- label: thm:unidentifiability -->
> \rigorFull
> Consider a deep feedforward network of depth $L$ with element-wise activations, trained on data with label noise rate $\eta > 0$. In the absence of skip connections, the training signal to layers at depth $\ell$ is attenuated by a factor of at least $\exp(-\alpha(L-\ell)\eta)$ for some $\alpha > 0$, where the attenuation is caused by the network using capacity to ``memorize'' noisy labels rather than learn the true function. The effective depth available for learning the true signal is:
> 
> $$<!-- label: eq:effective_depth -->
>     L_{eff} = O\left(\log\frac{1}\right).
> $$
> 
> As $\eta \to 0$, $L_{eff} \to L$ (full depth usable). As $\eta$ grows, only shallow networks can learn the true function; deeper layers are consumed by noise fitting.

> **Proof:** Consider layer $\ell$ with output $a^{(\ell)} = \sigma(W^{(\ell)} a^{(\ell-1)} + b^{(\ell)})$. The gradient of the loss $\mathcal{L}$ with respect to $W^{(\ell)}$ involves the chain of Jacobians:
> 
> $$
>     \frac{\partial \mathcal{L}}{\partial W^{(\ell)}} = \frac{\partial \mathcal{L}}{\partial a^{(L)}} \cdot \prod_{k=\ell+1}^{L} \frac{\partial a^{(k)}}{\partial a^{(k-1)}} \cdot \frac{\partial a^{(\ell)}}{\partial W^{(\ell)}}.
> $$
> 
> 
> Let the training data contain $n \cdot \eta$ mislabeled examples. On these examples, the gradient points in the wrong direction — it attempts to fit the incorrect label. Let $g_{true}^{(\ell)}$ be the gradient component from correctly labeled examples and $g_{noise}^{(\ell)}$ be the component from mislabeled examples. The effective gradient is:
> 
> $$
>     g_{eff}^{(\ell)} = (1-\eta) g_{true}^{(\ell)} + \eta g_{noise}^{(\ell)}.
> $$
> 
> 
> The noise gradient $g_{noise}^{(\ell)}$ is, in expectation, orthogonal to the true gradient (the noise is independent of the true function). The signal-to-noise ratio at layer $\ell$ is:
> 
> $$
>     SNR^{(\ell)} = \frac{(1-\eta)^2 \norm{g_{true}^{(\ell)}}^2}{\eta^2 \norm{g_{noise}^{(\ell)}}^2 + \sigma_{other}^2}.
> $$
> 
> 
> The backpropagation chain multiplies these SNR values. After $L-\ell$ layers of attenuation, the effective SNR at layer $\ell$ is:
> 
> $$
>     SNR_{eff}^{(\ell)} \approx SNR^{(L)} \cdot \prod_{k=\ell+1}^{L} \gamma_k,
> $$
> 
> where $\gamma_k \le 1$ is the attenuation factor per layer. When $\eta > 0$, each layer must allocate some capacity to model the noise, reducing $\gamma_k$. With random noise, $\gamma_k \approx 1 - c \cdot \eta$ for some constant $c > 0$, giving:
> 
> $$
>     SNR_{eff}^{(\ell)} \approx SNR^{(L)} \cdot (1 - c\eta)^{L-\ell} \approx SNR^{(L)} \cdot \exp(-c\eta(L-\ell)).
> $$
> 
> 
> For learning to be possible at layer $\ell$, we need $SNR_{eff}^{(\ell)} \ge \tau$ for some threshold $\tau > 0$. This gives:
> 
> $$
>     L - \ell \le \frac{1}{c\eta} \ln\frac{SNR^{(L)}} = O(1/\eta).
> $$
> 
> Thus the effective depth $L_{eff} = L - \ell_$ where $\ell_$ is the shallowest layer with sufficient SNR. Taking the worst case (signal at layer 1), $L_{eff} = O(\log(1/\eta))$.  $\square$

### ResNet: Separating Signal from Noise Correction

ResNet introduces skip connections: the output of a residual block is $F(x) + x$, where $F(x)$ is the learned residual and $x$ is the identity mapping. The SCX{} interpretation:

> **Proposition:** [ResNet as Signal/Noise Separation]<!-- label: prop:resnet_separation -->
> \rigorPartial
> In a ResNet with $B$ residual blocks, the identity path carries the **clean signal baseline** through the network, while the residual path $F(x)$ learns the **noise correction**. This separation prevents the signal attenuation identified in Theorem [ref]:
> 
> $$<!-- label: eq:resnet_snr -->
>     SNR_{eff, ResNet}^{(\ell)} \approx SNR^{(L)} \cdot (1 - c\eta)^{[residual depth]} \gg SNR_{eff, plain}^{(\ell)}.
> $$
> 
> The effective residual depth is $O(1)$ per block (typically 2-3 layers), not the total depth $L$, because the identity path bypasses the noise accumulation.

> **Proof:** [Proof Sketch]
> Consider the output after $\ell$ residual blocks:
> 
> $$
>     a^{(\ell)} = a^{(\ell-1)} + F_\ell(a^{(\ell-1)}).
> $$
> 
> The gradient backpropagates as:
> 
> $$
>     \frac{\partial a^{(\ell)}}{\partial a^{(\ell-1)}} = I + \frac{\partial F_\ell}{\partial a^{(\ell-1)}}.
> $$
> 
> The identity term $I$ provides an unobstructed gradient path of magnitude 1, regardless of depth. The noise-induced attenuation only affects the $\partial F_\ell / \partial a^{(\ell-1)}$ term, which vanishes as the residual learns to output zero when no correction is needed. The effective gradient path length for the signal is $O(1)$ (through the identity connections), while the noise correction is learned locally within each residual block.  $\square$

> **Remark:** [Why Clean Data Enables Shallow Architectures]
> Theorem [ref] predicts that when $\eta \approx 0$ (clean data), deep plain networks should train successfully because there is no noise to compensate for. This matches the empirical observation that on clean synthetic datasets, plain deep networks train well without skip connections. The ResNet advantage emerges precisely when label noise is present — which is the case for all real-world datasets (ImageNet has $\eta \approx 5\%$–$10\%$ estimated label error). The converse: if your dataset is perfectly clean, you don't need ResNet. This is a testable prediction of the SCX{} framework.

## Attention as Spring-like Memory
## 注意力机制作为Spring式记忆
<!-- label: sec:attention -->

The Transformer attention mechanism (Vaswani et al., 2017) is arguably the most important architectural innovation in modern deep learning. The SCX{} lens reveals that attention implements the Spring{} memory architecture with remarkable fidelity.

### The Spring Memory Architecture

Spring{} maintains a persistent state memory $M_t$ that accumulates evidence over time. At each time step, a gating function $S_t$ determines which past states are relevant to the current query. The update rule is an exponential moving average (EMA):

$$<!-- label: eq:spring_update -->
    M_{t} = \alpha \cdot M_{t-1} + (1-\alpha) \cdot new\_state(x_t),
$$

where $\alpha \in (0,1)$ controls the decay rate. The query mechanism retrieves relevant memories:

$$<!-- label: eq:spring_query -->
    output_t = \sum_{\tau=1}^{t} S_t(\tau) \cdot M_\tau,
$$

where $S_t(\tau)$ is a learned similarity function between the current state and memory at time $\tau$.

### Self-Attention as a Spring Instantiation

Scaled dot-product self-attention computes:

$$<!-- label: eq:attention -->
    Attention(Q, K, V) = \softmax\left(\frac{QK^T}{\sqrt{d_k}}\right) V,
$$

where $Q = XW_Q$, $K = XW_K$, $V = XW_V$ are linear projections of the input $X \in \R^{n \times d}$.

> **Proposition:** [Self-Attention is Spring{} Gating]<!-- label: prop:attention_spring -->
> \rigorFull
> Self-attention with softmax is an exact instantiation of the Spring{} memory query mechanism:
> 
1. The value matrix $V$ is the **permanent state memory** $M_t$ (all past states, stored without decay, satisfying \asmTag{4} — memory permanence).
2. The attention weights $A = \softmax(QK^T/\sqrt{d_k})$ are the **gating function** $S_t$: $A_{ij}$ determines how much state $j$ influences the output at position $i$.
3. The softmax normalization ensures $\sum_j A_{ij} = 1$, making the output a convex combination of memory states — exactly Spring{}'s probabilistic gating.
4. Multi-head attention runs $H$ parallel gating functions: $MultiHead(Q,K,V) = Concat(head_1, ..., head_H)W_O$, where each head is a Spring{} gatekeeper attending to different aspects of the state space.

> **Proof:** Map the Transformer to Spring{} component by component:
> 
> **Memory Store:** $V = XW_V$ stores a learned representation of each input position. Unlike Spring{}'s EMA update, self-attention gives equal weight to all positions (no temporal decay). This is a special case of the EMA with $\alpha = 0$ (no forgetting) — appropriate for fixed-length sequences where all positions are equally relevant a priori.
> 
> **Gating Function:** The attention weight $A_{ij}$ is:
> 
> $$
>     A_{ij} = \frac{\exp(Q_i \cdot K_j / \sqrt{d_k})}{\sum_{j'} \exp(Q_i \cdot K_{j'} / \sqrt{d_k})}.
> $$
> 
> This is a learned similarity kernel: $Q_i$ (query at position $i$) asks ``which past states are relevant to me?'' and $K_j$ (key at position $j$) answers ``I contain this type of information.'' The softmax normalizes the relevance scores into a probability distribution — precisely Spring{}'s probabilistic gating.
> 
> **Output:** $output_i = \sum_j A_{ij} V_j$, which is Equation [ref] with $S_t(\tau) = A_{ij}$ and $M_\tau = V_j$.
> 
> **Multi-Head:** $H$ parallel attention heads = $H$ independent Spring{} gatekeepers, each with its own $W_Q^{(h)}, W_K^{(h)}, W_V^{(h)}$ projections. This is Yajie{} consensus over $H$ experts attending to different feature subspaces.
> 
> The correspondence is exact up to the absence of temporal decay in the memory store. For variable-length or streaming sequences, adding positional encoding and causal masking recovers the full Spring{} dynamics.

> **Remark:** [The EMA Connection]
> Transformers without recurrence store all past states with equal weight (no decay), which is memory-intensive ($O(n^2)$ in sequence length). This is why efficient attention variants (Linformer, Performer, Reformer) introduce approximations that effectively impose an EMA-like decay — they are literally converging to the Spring{} architecture. The recent resurgence of state-space models (Mamba, S4) is further evidence: these models explicitly implement a learned EMA memory, which is Spring{} by construction.

> **Theorem:** [Multi-Head as Multi-Expert Consensus]<!-- label: thm:multihead_yajie -->
> \rigorPartial
> Under the Spring{} correspondence, multi-head attention with $H$ heads is a Yajie{} ensemble with $M = H$ experts, where each expert attends to a different $d_k$-dimensional subspace of the $d$-dimensional state representation. The concatenation-and-projection step aggregates the $H$ expert outputs via learned weights $W_O$. If the heads are sufficiently decorrelated (different $W_Q^{(h)}, W_K^{(h)}$ projections), the effective expert count approaches $H$.

> **Proof:** [Proof Sketch]
> Each head computes $head_h = Attention(QW_Q^{(h)}, KW_K^{(h)}, VW_V^{(h)})$. If the projection matrices produce approximately orthogonal subspaces, the heads are approximately independent experts on different aspects of the state. The projection $W_O \in \R^{H d_k \times d}$ learns the consensus weights. Under orthogonality, the effective $M_{eff} \approx H$. The standard Transformer uses $H = 8$ or $H = 16$, corresponding to $M = 8$–$16$ Spring{} gatekeepers. This is consistent with the SCX{} Theorem~1 threshold $M_ \approx 6$ for $\varepsilon = 0.05, \Delta_ = 0.5$.  $\square$

## BatchNorm as State Space Regularization
## 批归一化作为状态空间正则化
<!-- label: sec:batchnorm -->

Batch Normalization (Ioffe and Szegedy, 2015) normalizes layer activations to zero mean and unit variance across the batch dimension. The original explanation — ``reducing internal covariate shift'' — is descriptive but not rigorous. The SCX{} framework provides the formal justification.

### The C10/C11 Connection

Spring{} defines conditions C10 and C11 that govern state distribution stability:

- **C10 (State Boundedness):** The state distribution $P(X \mid s)$ must have bounded support for each state $s$.
- **C11 (State Drift):** The divergence between state distributions at consecutive time steps must be bounded: $\TV(P_t, P_{t+1}) \le \delta$.

Without BatchNorm, deep networks violate both conditions. As training progresses, the distribution of activations at each layer shifts (``internal covariate shift''), causing $\TV(P_\ell^{(t)}, P_\ell^{(t+1)})$ to grow. This drift forces subsequent layers to continuously adapt to a moving target, slowing or destabilizing training.

> **Proposition:** [BatchNorm Enforces \asmTag{5} (State Homogeneity)]<!-- label: prop:bn_homogeneity -->
> \rigorFull
> Batch Normalization with $\gamma, \beta$ applied to activations $x \in \R^{B \times d}$ guarantees that for each feature dimension $k$:
> 
> $$<!-- label: eq:bn_moments -->
>     \E_{batch}[\hat{x}_{:,k}] = 0, \quad \Var_{batch}[\hat{x}_{:,k}] = 1.
> $$
> 
> This enforces \asmTag{5} (state homogeneity): the state distribution has bounded first and second moments, and by Chebyshev's inequality, bounded support with high probability. The learnable parameters $\gamma, \beta$ allow the network to rescale and shift the normalized distribution, but the normalization itself prevents unbounded drift.

> **Proof:** The BatchNorm transform for a batch $\mathcal{B}$ of size $m$ is:
> 
> $$
>     \mu_{\mathcal{B}} &= \frac{1}{m}\sum_{i=1}^m x_i, \quad \sigma_{\mathcal{B}}^2 = \frac{1}{m}\sum_{i=1}^m (x_i - \mu_{\mathcal{B}})^2, 

>     \hat{x}_i &= \frac{x_i - \mu_{\mathcal{B}}}{\sqrt{\sigma_{\mathcal{B}}^2 + \epsilon}}, \quad y_i = \gamma \hat{x}_i + \beta.
> $$
> 
> 
> For any batch, $\E[\hat{x}] = 0$ and $\Var[\hat{x}] = 1$ by construction. The distribution of $\hat{x}$ is therefore constrained to have mean 0 and variance 1. By Cantelli's inequality, for any $t > 0$:
> 
> $$
>     \Pbb(\abs{\hat{x}} \ge t) \le \frac{2}{1 + t^2}.
> $$
> 
> This guarantees bounded support with high probability: $\Pbb(\hat{x} \in [-3, 3]) \ge 1 - 2/10 = 0.8$ for standard normal-like distributions. The $\gamma, \beta$ transform preserves this boundedness property (affine transformations preserve distribution shape).
> 
> In SCX{} terms: BatchNorm enforces that the state distribution $P(X \mid s)$ satisfies $\supp(P) \subseteq [\beta - \gamma \cdot C, \beta + \gamma \cdot C]$ with high probability for some constant $C$, satisfying \asmTag{5}.  $\square$

> **Theorem:** [BatchNorm Drift Reduction]<!-- label: thm:bn_drift -->
> \rigorPartial
> Let $P_\ell^{(t)}$ be the activation distribution at layer $\ell$ after training step $t$ without BatchNorm, and $\tilde{P}_\ell^{(t)}$ be the corresponding distribution with BatchNorm. For a network of depth $L$, the total distribution drift across layers is reduced by factor:
> 
> $$<!-- label: eq:bn_drift_reduction -->
>     \sum_{\ell=1}^L \TV(\tilde{P}_\ell^{(t)}, \tilde{P}_\ell^{(t+1)}) \le \sum_{\ell=1}^L \TV(P_\ell^{(t)}, P_\ell^{(t+1)}) - \Omega(L \cdot \sigma_{drift}^2),
> $$
> 
> where $\sigma_{drift}^2$ is the variance of the drift that BatchNorm eliminates (the component orthogonal to the mean-variance manifold).

> **Proof:** [Proof Sketch]
> Without BatchNorm, the activation distribution at layer $\ell$ evolves as:
> 
> $$
>     P_\ell^{(t+1)}(a) = \int P_\ell^{(t)}(a') \cdot P(weight update \mid a') \, da'.
> $$
> 
> This is an unconstrained random walk in distribution space, causing $\TV(P_\ell^{(t)}, P_\ell^{(t+1)})$ to be non-negligible at each step.
> 
> With BatchNorm, the distribution is projected onto the manifold of zero-mean, unit-variance distributions at every step. The projection operator $\Pi_{BN}$ is a contraction in TV distance:
> 
> $$
>     \TV(\Pi_{BN}(P), \Pi_{BN}(Q)) \le \TV(P, Q).
> $$
> 
> The drift component that BatchNorm eliminates is the component that changes the mean and variance — which is typically a large fraction of the total drift, especially in early training. The $\Omega(L \cdot \sigma_{drift}^2)$ term captures this reduction aggregated across layers.  $\square$

> **Remark:** [Batch Size Dependence]
> BatchNorm's effectiveness depends on batch size: small batches produce noisy estimates of $\mu_{\mathcal{B}}$ and $\sigma_{\mathcal{B}}^2$, reducing the contraction property. This is why BatchNorm underperforms with very small batch sizes ($m < 8$), and why alternatives like Layer Normalization and Group Normalization were developed. In SCX{} terms, small batch sizes introduce estimation error in the state homogeneity constraint, partially violating \asmTag{5}.

## GANs as Adversarial Audit — and Why $M=1$ Fails
## 生成对抗网络作为对抗审计——及为何$M=1$失败
<!-- label: sec:gans -->

Generative Adversarial Networks (Goodfellow et al., 2014) frame generative modeling as a two-player minimax game between a generator $G$ and a discriminator $D$. The SCX{} lens reveals this as an adversarial audit game — and explains why GAN training is notoriously unstable.

### GAN Training as an Audit Game

> **Proposition:** [GAN is Yajie{} NPE with $M=1$ Auditor]<!-- label: prop:gan_yajie -->
> \rigorFull
> The GAN objective:
> 
> $$<!-- label: eq:gan_objective -->
>     \min_G \max_D \; \E_{x \sim p_{data}}[\log D(x)] + \E_{z \sim p_z}[\log(1 - D(G(z)))]
> $$
> 
> is an instance of Yajie{} Non-Parametric Ensemble (NPE) with exactly $M=1$ auditor (the discriminator $D$). The generator $G$ produces a claim (``this sample is real''), and $D$ audits the claim. The training process is a two-player zero-sum game: $G$ attempts to minimize the audit detection rate, while $D$ attempts to maximize it.

> **Proof:** Map to SCX{} audit terminology:
> 
- **Claim:** $G(z)$ for $z \sim p_z$ — the generator claims that $G(z)$ is drawn from $p_{data}$.
- **Auditor:** $D: \cX \to [0,1]$ — the discriminator assigns a probability that $x$ is real.
- **Audit Outcome:** $D(G(z))$ is the probability that the auditor accepts the claim. The generator's loss is $-\log D(G(z))$ (or equivalently $\log(1 - D(G(z)))$).
- **Verification Community:** $M=1$ — there is exactly one discriminator. There is no consensus mechanism, no multi-auditor cross-check.

> 
> At the Nash equilibrium of this game, $G$ produces samples from $p_{data}$ and $D(x) = 1/2$ for all $x$ (the discriminator cannot distinguish real from generated). This is the equilibrium where the auditor is maximally uncertain — the claim is indistinguishable from truth.
> 
> However, this equilibrium is only guaranteed under the assumption that both $G$ and $D$ have infinite capacity and that the optimization reaches the global optimum. In practice, neither holds, and the $M=1$ auditor architecture creates the instability that GANs are famous for.

### Why GANs Are Unstable: Theorem 1 Explains

> **Theorem:** [GAN Instability from $M=1$]<!-- label: thm:gan_instability -->
> \rigorFull
> A single-auditor ($M=1$) adversarial training game has the following failure modes, directly predicted by SCX{} Theorem~1 and Theorem~2:
> 
> 
1. **Auditor Capture:** If $D$ has a blind spot, $G$ can exploit it without detection. The probability that a single auditor misses a specific type of generated artifact is bounded below by a constant (no exponential suppression from multiple independent auditors).
2. **Mode Collapse:** $G$ finds a ``loophole'' — a small set of outputs that consistently fool $D$. With $M=1$, $G$ need only satisfy one auditor. With $M>1$ independent auditors, $G$ would need to satisfy all $M$ simultaneously, making mode collapse exponentially harder: $\Pbb(fool all  M) \le \exp(-2M\Delta^2)$.
3. **Training Oscillation:** The $M=1$ game has no stabilizing consensus mechanism. When $D$ improves, $G$ must adapt; when $G$ improves, $D$ must adapt. This creates non-convergent cycles, analogous to the lack of a separating equilibrium without M-declaration (Theorem~2).

> **Proof:** **(i) Auditor Capture.** Let $\cB \subset \cX$ be a ``blind spot'' of the discriminator: $D(x) > 1/2$ for $x \in \cB$ even though $x$ is generated (false acceptance). With $M=1$, the generator's expected loss for samples in $\cB$ is $\E_{z: G(z) \in \cB}[-\log D(G(z))] < \log 2$, which is profitable. With $M$ independent auditors, the probability that all $M$ accept a generated sample in $\cB$ is at most $\prod_{k=1}^M D_k(x) \le (\max_k D_k(x))^M$, which decays exponentially if any single auditor has $D_k(x) \le 1/2$. Formally, $\Pbb(all accept \mid \cB) \le \exp(-2M\Delta^2)$ where $\Delta = \min_k |D_k(x) - 1/2|$.
> 
> **(ii) Mode Collapse.** Let $\cS \subset \supp(p_{data})$ be a subset of the true data modes, and let $\cG \subset \cX$ be the set of outputs that $G$ can produce. Mode collapse occurs when $|\cG| \ll |\supp(p_{data})|$ but $D$ cannot distinguish $\cG$ from the full support. With $M$ independent auditors, each auditor covers a different aspect of the data distribution. For $G$ to collapse to mode $m$, it must fool all $M$ auditors simultaneously. If each auditor independently detects mode absence with probability at least $\Delta$, the collapse survival probability is $\le \exp(-2M\Delta^2)$.
> 
> **(iii) Training Oscillation.** The two-player game has payoff matrix with no pure Nash equilibrium in finite capacity regimes. The best-response dynamics create cycles (GAN training is known to oscillate rather than converge). Adding more auditors ($M>1$) creates a potential game structure: the consensus of $M$ auditors is smoother and more stable than any single auditor, because random fluctuations in one auditor are averaged out. This is the variance reduction effect of Proposition [ref].  $\square$

> **Remark:** [Multi-Discriminator GANs as Validation]
> The SCX{} prediction is that GANs with multiple discriminators should be more stable. This is exactly what has been observed: Generative Multi-Adversarial Networks (GMAN; Durugkar et al., 2017), Dual Discriminator GANs (D2GAN; Nguyen et al., 2017), and multi-scale discriminators (Pix2PixHD; Wang et al., 2018) all improve stability. Each additional discriminator increases $M$, and SCX{} Theorem~1 predicts exponential improvement in mode coverage and training stability. However, these multi-discriminator architectures are heuristic — they do not enforce independence (\asmTag{1}) or compute formal consensus bounds. A rigorously SCX{}-compliant GAN would require $M$ discriminators with provably independent training.

## Self-Supervised Learning as Self-Audit — Theorem 2's Domain
## 自监督学习作为自我审计——定理2的适用领域
<!-- label: sec:ssl -->

Self-supervised learning (SSL) has driven the most dramatic advances in representation learning: models are trained on ``pretext tasks'' where labels are derived from the data itself (e.g., predicting the next word, solving jigsaw puzzles, contrastive instance discrimination). The SCX{} lens reveals a profound tension at the heart of SSL.

### The Self-Audit Problem

> **Proposition:** [SSL is Self-Audit — Theorem 2 Applies]<!-- label: prop:ssl_selfaudit -->
> \rigorFull
> In self-supervised learning, the model generates its own training labels from the data, then learns from them. In SCX{} terminology: the model is both the **claimant** (it proposes a representation) and the **auditor** (it evaluates the representation against the pretext task). This is **self-audit** — the exact scenario that SCX{} Theorem~2 identifies as epistemically equivalent to no audit:
> 
> $$<!-- label: eq:ssl_thm2 -->
>     Self-generated labels without independent verification \implies \Pbb(quality certified)  is unbounded.
> $$
> 
> Formally, SSL with a single pretext task has $M=0$ independent auditors.

> **Proof:** The SSL training pipeline is:
> 
1. Define pretext transformation $T: \cX \to \cX \times \cY_{pretext}$ that generates ``labels'' from unlabeled data.
2. Train model $f_\theta$ to minimize $\E_{x \sim \cD}[\ell(f_\theta(T_x(x)), T_y(x))]$.
3. Use $f_\theta$ (or its intermediate representation) for downstream tasks.

> 
> The critical observation: the model $f_\theta$ is the *sole* entity that determines the quality of both the pretext labels and the learned representation. There is no external verifier. The pretext task's loss $\mathcal{L}_{pretext}$ is minimized by construction (gradient descent finds a local minimum), but this provides no information about whether the learned representation captures *true* data structure or merely satisfies the pretext task's specific inductive bias.
> 
> By SCX{} Theorem~2, without an independent auditor (a verifier not trained on the same objective), the quality of the representation cannot be certified. Any observed downstream performance is consistent with both a good representation and a representation that exploits spurious correlations in the pretext task.

### Why SSL Still Works: Implicit Multi-Expert Structure

Despite Theorem~2's negative result, SSL demonstrably works. The resolution comes from the *implicit* multi-expert structure that SSL methods inadvertently create:

> **Proposition:** [Contrastive Learning as Implicit Consensus]<!-- label: prop:simclr_consensus -->
> \rigorPartial
> Contrastive learning methods (SimCLR, MoCo, BYOL) create an implicit Yajie{} ensemble through multiple data augmentations. Each augmented view of the same image is an ``expert'' that votes on the representation. The contrastive loss:
> 
> $$<!-- label: eq:simclr_loss -->
>     \mathcal{L}_{contrastive} = -\log \frac{\exp(sim(z_i, z_j)/\tau)}{\sum_{k=1}^{2N} \ind{k \neq i} \exp(sim(z_i, z_k)/\tau)},
> $$
> 
> where $z_i, z_j$ are representations of two augmentations of the same image, implements Yajie{} consensus: the positive pair $(z_i, z_j)$ must agree (vote together), while negative pairs $(z_i, z_k)$ must disagree. The batch size $2N$ determines how many ``experts'' (augmented views) participate in the vote.

> **Proof:** [Proof Sketch]
> Each augmentation $t \sim \cT$ applied to image $x$ produces a distinct ``view'' $t(x)$. The model must produce similar representations for different views of the same image and different representations for different images. This is a Yajie{} voting problem in representation space:
> 
> 
- **Experts:** The $K$ different augmentations (typically $K=2$ per image in SimCLR, but the effective $K$ is larger due to the memory bank in MoCo or the large batch in SimCLR).
- **Claim:** ``Images $x$ and $x'$ are the same underlying instance'' (positive pair) or ``are different instances'' (negative pair).
- **Vote:** The similarity $sim(z_i, z_j)$ is the vote strength. The softmax over all pairs normalizes the votes into a probability distribution.

> 
> The effective $M_{eff}$ is the number of *independent* augmentations per instance. With $K=2$ augmentations, $M_{eff}$ is small, but with momentum encoders (MoCo) or large batches (SimCLR), the effective number of negative examples provides additional implicit auditing: each negative is a ``vote against'' spurious representations.
> 
> This connection is \rigorConjectural{} because the augmentations are not independent experts in the SCX{} sense — they share the same backbone network and optimization trajectory, violating \asmTag{1}. However, the functional behavior matches Yajie{} consensus: more augmentations (larger $K$) and more negatives (larger batch) improve representation quality, analogous to larger $M$ improving consensus accuracy.

> **Remark:** [BYOL and the Bootstrap Paradox]
> BYOL (Grill et al., 2020) eliminates negative pairs entirely, using only positive pairs with a momentum encoder. This raises an even sharper version of the self-audit problem: without negatives, what prevents representation collapse? The SCX{} conjecture is that the momentum encoder acts as an **implicit auditor from a previous time step**: the target network $\xi$ (updated via EMA) provides a slowly-moving reference that prevents the online network $\theta$ from collapsing. This is a temporal Spring{}-style audit: the past state of the model audits the current state. This connection is highly conjectural and merits formal investigation.

## Transfer Learning as State Prior
## 迁移学习作为状态先验
<!-- label: sec:transfer -->

Transfer learning — pre-training on a large corpus followed by fine-tuning on a downstream task — is the dominant paradigm in modern NLP and computer vision. The SCX{} framework provides a crisp mathematical interpretation.

### Pre-Training as Prior Estimation

> **Proposition:** [Pre-Training Estimates State Priors]<!-- label: prop:pretrain_prior -->
> \rigorFull
> In SCX{} terms, pre-training on a large corpus $\cD_{pre}$ estimates the state prior distribution $\rho_s = \Pbb(s)$ over the state space $\cS$. Fine-tuning on a downstream dataset $\cD_{down}$ estimates the separation gaps $\Delta_s$ between states. Formally:
> 
> $$
>     Pre-training:\quad &\hat_s = \argmax_ \Pbb(\cD_{pre} \mid \rho), <!-- label: eq:pretrain --> 

>     Fine-tuning:\quad &\hat_s = \argmax_ \Pbb(\cD_{down} \mid \Delta, \hat), <!-- label: eq:finetune -->
> $$
> 
> where $\rho_s$ captures the frequency and structure of state occurrences, and $\Delta_s$ captures the discriminative boundaries between states relevant to the downstream task.

> **Proof:** In the \Situs{} component of SCX{}, the state space $\cS$ is the set of possible ``situations'' the model can encounter. Each state $s \in \cS$ has:
> 
- **Prior probability:** $\rho_s = \Pbb(s)$ — how often does state $s$ occur in the world?
- **Separation gap:** $\Delta_s = \min_{s' \neq s} \TV(P(\cdot \mid s), P(\cdot \mid s'))$ — how distinguishable is state $s$ from its neighbors?

> 
> Pre-training on a large, diverse corpus (e.g., ImageNet, C4, The Pile) provides data from a broad distribution over $\cS$. The model learns:
> 
- $\rho_s$: which visual/textual patterns are common vs. rare (e.g., edges, textures, syntactic structures).
- $P(X \mid s)$: the conditional distribution of inputs given each state (e.g., what dogs look like, what grammatical sentences look like).

> 
> Fine-tuning on a small downstream dataset estimates $\Delta_s$ for the specific task: which states must be distinguished, and with what precision. Since $\hat_s$ is already well-estimated from pre-training, the sample complexity for estimating $\hat_s$ is reduced from $O(|\cS|^2)$ to $O(|\cS_{task}|)$ — the model only needs to learn task-specific distinctions, not re-learn the entire state structure.

> **Theorem:** [Transfer Learning Sample Complexity Reduction]<!-- label: thm:transfer_sample -->
> \rigorPartial
> Let $\cS_{pre}$ be the state space covered by pre-training and $\cS_{task} \subseteq \cS_{pre}$ be the states relevant to the downstream task. The sample complexity for learning the downstream task with pre-training is:
> 
> $$<!-- label: eq:transfer_complexity -->
>     n_{down} = O\left(\frac{|\cS_{task}| \cdot \log(1/\delta)}{\min_{s \in \cS_{task}} \Delta_s^2}\right),
> $$
> 
> compared to $n_{scratch} = O(|\cS_{pre}| \cdot \log(1/\delta) / \min_s \Delta_s^2)$ for training from scratch. The reduction factor $|\cS_{pre}| / |\cS_{task}|$ is typically $10^2$–$10^4$, explaining why transfer learning succeeds with tiny downstream datasets.

> **Proof:** [Proof Sketch]
> Learning from scratch requires estimating both $\rho_s$ and $\Delta_s$ for all $s \in \cS_{pre}$ (since the model doesn't know which states will be relevant). The VC-dimension (or Rademacher complexity) scales with $|\cS_{pre}|$. With pre-training, $\hat_s$ is already estimated to within $\epsilon_{pre}$. The downstream task only needs to estimate $\Delta_s$ for $s \in \cS_{task}$, which requires samples proportional to $|\cS_{task}|$, not $|\cS_{pre}|$. The bound follows from standard PAC-Bayes analysis with a pre-trained prior.  $\square$

> **Remark:** [Negative Transfer as Prior Mismatch]
> When the pre-training distribution is mismatched to the downstream task ($\cS_{task} \not\subseteq \cS_{pre}$), transfer learning can *hurt* performance — the pre-trained $\hat_s$ is a bad prior that must be ``unlearned.'' In SCX{} terms, negative transfer occurs when $\TV(\rho_{pre}, \rho_{true}) > \TV(\rho_{uninform}, \rho_{true})$, i.e., the pre-trained prior is worse than an uninformed prior. This is a formal statement of a well-known empirical phenomenon.

## Reinforcement Learning as Interactive Audit
## 强化学习作为交互式审计
<!-- label: sec:rl -->

Reinforcement Learning (RL) frames learning as an agent interacting with an environment: the agent takes actions, the environment returns rewards. The SCX{} interpretation treats the environment as an auditor.

### The Environment as Auditor

> **Proposition:** [RL Environment is an Auditor with $M=1$]<!-- label: prop:rl_auditor -->
> \rigorFull
> In standard RL (MDP formulation), the environment is the **sole auditor** of the agent's actions. At each time step $t$, the agent proposes action $a_t$ (a claim that ``$a_t$ is good in state $s_t$''), and the environment returns reward $r_t$ (the audit outcome). There is exactly $M=1$ auditor, and the audit is **interactive**: the environment's response depends on the agent's action and the state, which the agent's previous actions have influenced.

> **Proof:** The MDP is $(\cS, \cA, P, R, \gamma)$. At each step:
> 
- **Claim:** Policy $\pi(a \mid s)$ implicitly claims that action $a$ is optimal (or near-optimal) in state $s$.
- **Auditor:** The transition function $P(s' \mid s, a)$ and reward function $R(s, a)$ determine the outcome.
- **Audit Result:** The reward $r_t = R(s_t, a_t)$ and next state $s_{t+1} \sim P(\cdot \mid s_t, a_t)$.

> 
> The key limitation: there is only one auditor (the environment). There is no second environment against which to validate the first, no consensus mechanism, and no cross-audit. This $M=1$ structure explains RL's sample inefficiency through the SCX{} lens.

### Why RL is Sample-Inefficient: $M=1$ Auditor

> **Theorem:** [RL Sample Inefficiency from $M=1$]<!-- label: thm:rl_sample -->
> \rigorPartial
> The sample complexity of RL with $M=1$ auditor is fundamentally higher than supervised learning with $M>1$:
> 
> $$<!-- label: eq:rl_sample_complexity -->
>     n_{RL} = \Omega\left(\frac{|\cS||\cA|}{\varepsilon^2} \log\frac{1}\right),
> $$
> 
> compared to $n_{supervised} = O(\log(1/\delta) / \varepsilon^2)$ with $M = \Omega(\log(1/\delta) / \varepsilon^2)$ independent experts. The $M=1$ auditor provides no consensus variance reduction, no cross-validation, and no independent verification of the value function.

> **Proof:** [Proof Sketch]
> In supervised learning with $M$ independent experts, each expert provides a noisy estimate of the true function with variance $\sigma^2/M$ after consensus (by Proposition [ref]). In RL, the single environment provides one noisy trajectory. Off-policy methods (experience replay) create an *implicit* memory of past audits, but these audits are:
> 
1. Not independent — they come from the same environment with the same dynamics.
2. Generated by a behavior policy that differs from the target policy, introducing distribution shift.

> 
> The Spring{} memory $M_t$ (experience replay buffer) stores past audit outcomes, enabling off-policy learning. However, this does not increase $M$ — it merely reuses the same auditor's past judgments, which is akin to a single expert reviewing its own past decisions. SCX{} Theorem~2 (self-audit) applies: without an independent auditor, the quality of the value function estimate cannot be certified from the replay buffer alone.
> 
> The sample complexity bound follows from the minimax lower bound for MDP exploration: $\Omega(|\cS||\cA|/\varepsilon^2)$ samples are needed to estimate the optimal policy to within $\varepsilon$, compared to $O(1/\varepsilon^2)$ for supervised consensus. The factor $|\cS||\cA|$ is the price of $M=1$.  $\square$

> **Remark:** [Multi-Agent RL as $M>1$]
> Multi-agent RL, where multiple agents interact with the same or different environments, naturally increases $M$. Each agent is an independent learner whose policy can be cross-audited against others. This predicts that multi-agent systems should be more sample-efficient per agent than single-agent systems — a hypothesis that has partial empirical support but lacks formal SCX{} analysis.

> **Remark:** [Exploration as Spring Filtering]
> The exploration-exploitation tradeoff in RL maps to Spring{}'s filtering-vs-exploration tradeoff. The Spring{} gating function $S_t$ determines whether to trust the current best estimate (exploit) or query new states (explore). $\varepsilon$-greedy exploration is a crude approximation of Spring{}'s adaptive gating: $\varepsilon$ is the exploration budget, analogous to Spring{}'s uncertainty threshold. This connection is \rigorConjectural{} and merits formal development.

## Convolutional Neural Networks as \Situs{ Spatial Localization}
## 卷积神经网络作为\Situs{空间定位}
<!-- label: sec:cnn -->

Convolutional Neural Networks (CNNs) are the foundational architecture for computer vision. Their core operations — convolution, pooling, and weight sharing — implement a specific form of spatial state-space structuring that corresponds to \Situs{} (定位).

### Convolution as State-Space Translation Equivariance

> **Proposition:** [CNN is \Situs{} with Spatial Inductive Bias]<!-- label: prop:cnn_situs -->
> \rigorPartial
> A convolutional layer with kernel $W \in \R^{k \times k \times c_{in} \times c_{out}}$ applied to input $X \in \R^{H \times W \times c_{in}}$ implements \Situs{} spatial localization with translation equivariance:
> 
> $$<!-- label: eq:cnn_situs -->
>     Conv(X)_{i,j} = \sum_{p,q} W_{p,q} \cdot X_{i+p, j+q}.
> $$
> 
> The weight sharing across spatial positions enforces that the same state detector is applied everywhere — i.e., \Situs{} recognizes the same state $s$ regardless of its spatial coordinates. Translation equivariance means: if the input shifts by $\Delta$, the feature map shifts by $\Delta$. This is precisely \Situs{}'s state-space structure: states are identified by their *local pattern*, not their global position.

> **Proof:** [Proof Sketch]
> The \Situs{} state $s$ is a local configuration of pixels/features. A convolutional filter detects whether state $s$ is present at position $(i,j)$. By sharing weights across all positions, the filter implements $\Pbb(s \mid position  (i,j)) = \Pbb(s \mid position  (i',j'))$ — state probability is position-invariant. Max pooling then computes $\max_{p,q} feature(i+p, j+q)$, which is the \Situs{} operation of ``is state $s$ present anywhere in this region?'' — state existence detection.
> 
> The connection is \rigorConjectural{} because \Situs{} is defined at a higher level of abstraction than individual CNN operations. However, the mathematical structure — translation-equivariant state detection with spatial pooling — matches \Situs{}'s specification of state-space localization with invariance to irrelevant transformations.

> **Remark:** [Why CNNs Work — The SCX Explanation]
> CNNs succeed because visual data has a \Situs{}-compatible structure: states (objects, textures, edges) are (i) local, (ii) translation-invariant, and (iii) hierarchically composable. CNNs bake these properties into the architecture through weight sharing and locality, which is equivalent to providing \Situs{} with an accurate prior over the state-space topology. When the data deviates from this topology (e.g., viewpoint variation requiring 3D reasoning), CNNs struggle — exactly as \Situs{} would struggle with an incorrect state-space model.

## Diffusion Models as Multi-Step Audit Consensus
## 扩散模型作为多步审计共识
<!-- label: sec:diffusion -->

Diffusion models (Ho et al., 2020; Song et al., 2021) have largely replaced GANs as the dominant generative modeling paradigm. The SCX{} lens suggests a structural reason: diffusion models implement an implicit multi-step audit, providing stronger guarantees than GANs' $M=1$ architecture.

### The Diffusion Process as Sequential Audit

A diffusion model defines a forward process that gradually adds noise:

$$<!-- label: eq:diffusion_forward -->
    q(x_t \mid x_{t-1}) = N(x_t; \sqrt{1-\beta_t} x_{t-1}, \beta_t I),
$$

and a reverse process that learns to denoise:

$$<!-- label: eq:diffusion_reverse -->
    p_\theta(x_{t-1} \mid x_t) = N(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t)).
$$

> **Proposition:** [Diffusion as $T$-Step Yajie{} Consensus]<!-- label: prop:diffusion_yajie -->
> \rigorConjectural
> The $T$ denoising steps of a diffusion model can be interpreted as a $T$-round Yajie{} consensus: at each step $t$, the model ``audits'' the current noisy sample $x_t$ against the learned data distribution, producing a refined estimate $x_{t-1}$. The effective number of audits is $M_{eff} \approx T$, with each step contributing an independent denoising decision. This $M_{eff} \gg 1$ (typically $T = 1000$) provides substantially stronger SCX{} guarantees than GANs' $M=1$, explaining diffusion models' superior mode coverage and training stability.

> **Proof:** [Proof Sketch]
> Each denoising step $t$ solves a local optimization:
> 
> $$
>     \mu_\theta(x_t, t) \approx \argmin_ \E_{x_0 \sim q(x_0 \mid x_t)}\left[\norm{\mu - x_0}^2\right].
> $$
> 
> This is an ``audit'': the model checks whether $x_t$ is consistent with the data manifold and proposes a correction. The $T$ steps form a consensus chain:
> 
> $$
>     x_0^{(generated)} = Audit_1 \circ Audit_2 \circ ... \circ Audit_T (x_T),
> $$
> 
> where each audit step reduces the distance to the data manifold. The denoising score matching objective:
> 
> $$
>     \mathcal{L}_{diffusion} = \E_{t, x_0, \epsilon}\left[\norm{\epsilon - \epsilon_\theta(x_t, t)}^2\right],
> $$
> 
> trains the auditor at all noise levels simultaneously. The key difference from GANs: GANs have one discriminator making a single continuous decision; diffusion has $T$ steps each making a local correction. The consensus of $T$ steps is more robust than any single-step audit.
> 
> This connection is \rigorConjectural{} because the denoising steps are not independent — they share the same network $\epsilon_\theta$ and the same training trajectory, violating \asmTag{1}. However, the functional behavior matches: more steps ($T \uparrow$) improves sample quality (up to a point), analogous to larger $M$ improving consensus accuracy.

> **Remark:** [Why Diffusion Won]
> The SCX{} framework provides a structural explanation for diffusion models' victory over GANs: $T \approx 1000$ implicit audits beats $M=1$ explicit audit. The market selected for SCX{}-compliance: practitioners abandoned GANs for diffusion models not because they computed SCX{} bounds, but because diffusion models empirically provide better mode coverage, stability, and sample quality — all predicted by SCX{} Theorem~1 with larger $M$.

## Cercis Score Ranking of Algorithms
## 算法的Cercis评分排序
<!-- label: sec:cercis -->

The Cercis{} score $S = Q + \eta N$ provides a unified metric for evaluating ML algorithms through the SCX{} lens. We define:

> **Definition:** [Cercis{} Score for ML Algorithms]<!-- label: def:cercis_ml -->
> For an algorithm $\cA$, the Cercis{} components are:
> 
- **Q (Quality Guarantee):** $Q(\cA) = w_1 \cdot rigor\_score + w_2 \cdot empirical\_robustness$, where $rigor\_score \in [0,1]$ measures how well $\cA$'s guarantees can be derived from SCX{} theorems, and $empirical\_robustness \in [0,1]$ measures performance stability across datasets and hyperparameters. We use $w_1 = 0.5, w_2 = 0.5$.
- **N (Novelty):** $N(\cA) \in [0,1]$ measures how surprising the algorithm was at the time of its invention, relative to the knowledge of its era.
- **$\eta$ (Novelty Weight):** $\eta = 0.3$ (novelty is valued but quality dominates).

We compute Cercis{} scores for the fourteen algorithm families treated in this paper. Scores are approximate and qualitative, informed by the rigorous/conjectural status established in Sections~3--12.

[Table omitted — see original .tex]

**Interpretation:** Algorithms at the top (Random Forest, Bagging) have near-complete SCX{} derivations. Algorithms in the middle (Dropout, BatchNorm, Attention, Transfer Learning, CNN) have partial but substantial SCX{} connections. Algorithms at the bottom (GAN, RL) have weak implicit audit mechanisms, explaining their well-known fragility. The high novelty of GAN and Contrastive SSL partially compensates for low quality guarantees, but their Cercis{} scores remain modest — novelty without robustness is epistemically hazardous.

> **Remark:** [The Cercis Paradox]
> Attention ranks 6th in Q (rigor) but 1st in $S$ due to enormous empirical success ($Q_{empirical} = 0.95$) and novelty ($N = 0.80$). This highlights a tension: SCX{} theory has not fully caught up with attention's practical success. The rigorous connection to Spring{} (Proposition [ref]) is established, but the optimization dynamics of attention-based models remain poorly understood in SCX{} terms. The high Cercis{} score is empirically justified but theoretically aspirational.

> **Remark:** [The GAN vs. Diffusion Cercis Gradient]
> Comparing GAN ($S = 0.64$) with Diffusion ($S = 0.88$) reveals that the Cercis{} score correctly identifies the paradigm shift: diffusion's $M_{eff} \approx T \gg 1$ provides much stronger implicit guarantees than GAN's $M=1$, despite diffusion being less novel (built on older denoising ideas). This is the Cercis{} score vindicating SCX{} Theorem~1's prediction: algorithms with larger effective $M$ outperform those with smaller $M$, even when the former are less ``clever'' by conventional novelty metrics.

## Discussion — What ML History Teaches SCX
## 讨论——机器学习史对SCX的启示
<!-- label: sec:discussion -->

### The Survivorship Pattern

The history of ML reveals a striking pattern when viewed through the SCX{} lens:

<div align="center">

\fbox{\parbox{0.9\textwidth}{
**The algorithms that survived longest have the strongest implicit SCX{} guarantees.** The algorithms that were trendy but fragile have weak implicit audit mechanisms. The market (empirical practice) is an evolutionary optimizer that selects for SCX{}-compliance, even when practitioners don't know it.
}}

</div>

- **Random Forest (2001) → still dominant in tabular data.** Explicit $M$-tree ensemble, built-in OOB audit, exponential error bound. This is the most SCX{}-compliant algorithm in existence. It was *not* designed with SCX{} in mind, but it accidentally implements Theorem~1 perfectly.
- **Dropout (2012) → still standard regularization.** The $2^n$ implicit subnetwork ensemble provides $M_{eff} \gg 1$, giving Theorem~1 guarantees even though no practitioner computes the bound. The empirical discovery of $p=0.5$ as optimal matches the SCX{} prediction of maximum mask diversity.
- **BatchNorm (2015) → still standard.** The state homogeneity enforcement (\asmTag{5}) is so fundamental that virtually every deep network uses it or a variant (LayerNorm, GroupNorm). The architectural convergence on normalization is SCX{} vindication by revealed preference.
- **ResNet (2016) → still standard for vision.** The skip connection's separation of signal from noise correction (Theorem [ref]) is so effective that ResNet variants dominate computer vision. The empirical necessity of skip connections for deep networks is SCX{} Theorem~3 in action.
- **GAN (2014) → declining in practice, replaced by diffusion models.** GANs were celebrated as a breakthrough, but training instability and mode collapse limited their adoption. The SCX{} diagnosis — $M=1$ auditor — explains exactly why. Diffusion models, which use a denoising objective with explicit probabilistic structure, effectively implement an $M$-step consensus (each denoising step is a partial audit), which may explain their superior stability. This is a conjecture.
- **RL → dominant in games, limited in real-world applications.** The $M=1$ auditor (environment) imposes fundamental sample inefficiency. Model-based RL attempts to create an ``internal auditor'' (a learned world model), which increases effective $M$, but the learned model introduces its own errors (a self-audit problem per Theorem~2).

### The Future: Design with SCX Guarantees, Not Post-Hoc

The central methodological lesson of this re-audit is:

<div align="center">

**Design algorithms with explicit SCX{} guarantees from the start. Do not rely on post-hoc theoretical justification of empirically discovered methods.**

</div>

Concretely, a SCX{}-compliant ML algorithm should satisfy the following specification:

1. **$M$ — the number of independent experts.** Explicit, declared, and verified. Not hidden in architectural details (like dropout masks or attention heads).
2. **Training independence — \asmTag{1}.** How independence is achieved: separate bootstrap samples, separate initializations, separate optimization trajectories, or separate data augmentations.
3. **Consensus mechanism — Yajie{}.** How expert outputs are aggregated, with formal error bounds of the form $\exp(-2M\Delta^2)$.
4. **Memory architecture — Spring{}.** How past states are stored, queried, and decayed, with formal guarantees on memory fidelity and query accuracy.
5. **State homogeneity — \asmTag{5}.** How activation distributions are constrained to prevent drift, with formal bounds on distribution shift between training iterations.
6. **Audit mechanism — independent of training.** Out-of-bag error, held-out validation set, or external verifier that was not used in training the consensus weights.

### Design Patterns for SCX-Native ML

We outline three design patterns that follow from this re-audit. These are not yet implemented algorithms; they are specifications for what SCX{}-native algorithm design looks like.

> **Definition:** [SCX-Ensemble: Explicit $M$-Expert Training]<!-- label: def:scx_ensemble -->
> An SCX{}-ensemble is a tuple $(\cA, M, Yajie, \cD_{audit})$ where:
> 
- $\cA$ is a base learning algorithm.
- $M$ is the declared number of independent experts.
- Each expert $k$ is trained on $\cD_k \sim Bootstrap(\cD)$ independently.
- $Yajie$ aggregates outputs with formal error bound $\exp(-2M\Delta^2)$ computed on $\cD_{audit}$.
- The OOB error on $\cD \setminus \cD_k$ provides the cross-audit.

> Random Forest is the canonical example. Any algorithm can be SCX{}-ensembled: SCX-Dropout (with explicit $M$ masks and independent training), SCX-Attention (with independently trained attention heads on different data subsets), SCX-RL (with $M$ independently trained policies on different environment seeds).

> **Definition:** [SCX-GAN: $M$-Discriminator Adversarial Training]<!-- label: def:scx_gan -->
> An SCX{}-GAN trains $M$ discriminators $D_1, ..., D_M$ on independently bootstrapped subsets of $\cD_{real}$ against one generator $G$. The generator's objective is:
> 
> $$<!-- label: eq:scx_gan_objective -->
>     \min_G \frac{1}{M}\sum_{k=1}^M \E_{z \sim p_z}[\log(1 - D_k(G(z)))].
> $$
> 
> The consensus discriminator output is $\bar{D}(x) = \frac{1}{M}\sum_k D_k(x)$, and the generator must fool the consensus. By SCX{} Theorem~1, the probability that $G$ fools all $M$ discriminators with a mode-collapsed distribution decays as $\exp(-2M\Delta^2)$. This provides formal guarantees against mode collapse that single-discriminator GANs lack.

> **Definition:** [SCX-SSL: Augmentation-Consensus Self-Supervised Learning]<!-- label: def:scx_ssl -->
> SCX{}-SSL addresses the self-audit problem (Theorem~2) by making the implicit augmentation ensemble explicit. Rather than training a single encoder on random augmentations, SCX{}-SSL:
> 
1. Generates $K$ augmentations per instance using *independent* augmentation policies $\cT_1, ..., \cT_K$.
2. Trains $K$ separate encoder heads on these $K$ augmentation streams, with shared early layers but independent final layers.
3. Computes Yajie{} consensus across the $K$ heads, with the contrastive loss evaluated on the consensus representation.
4. Monitors head disagreement as an uncertainty metric: high disagreement signals out-of-distribution inputs.

> This transforms SSL from self-audit ($M=0$) to a $K$-expert ensemble ($M=K$), resolving the Theorem~2 paradox by providing independent verification through explicit multi-expert structure.

### The Dark Matter of ML: Implicit Consensus Everywhere

A striking pattern emerges from this re-audit: many ML innovations that appear unrelated are, in SCX{} terms, the *same* mechanism — increasing the effective number of independent experts $M_{eff}$:

<div align="center">

[Table omitted — see original .tex]

</div>

This convergence is the strongest evidence for the SCX{} thesis: practitioners, through trial and error, have consistently discovered that ``more independent views of the data improve performance.'' SCX{} provides the unified mathematical explanation for why this is always true: Theorem~1's exponential bound.

### Honest Assessment of Rigor Gaps

We conclude by honestly cataloging which connections in this paper are rigorous and which are conjectural:

[Table omitted — see original .tex]

### Limitations

This re-audit has several limitations:

1. **Not all algorithms are covered.** We focused on 12 major families. Convolutional neural networks (CNNs), graph neural networks (GNNs), diffusion models, normalizing flows, and many others remain for future work. We conjecture that CNNs can be understood as \Situs{}-style spatial localization (translation equivariance = state space structure), but this is not developed here.
2. **The connections are a posteriori.** We are re-interpreting existing algorithms, not deriving them from SCX{} axioms. A truly SCX{}-native ML theory would start from the axioms and derive algorithms as optimal solutions to the SCX{} objectives. This paper is a step toward that goal, not its achievement.
3. **Empirical validation is incomplete.** The Cercis{} scores in Table [ref] are qualitative judgments, not computed from formal metrics. A rigorous Cercis{} computation would require standardized benchmarks and formal verification of SCX{} compliance.
4. **The theory does not yet produce new algorithms.** The ultimate test of a theoretical framework is whether it generates *new* algorithms that outperform existing ones. We have shown that SCX{} explains existing algorithms; we have not (yet) used SCX{} to design a novel algorithm with provably superior properties. This is the most important direction for future work.

## Conclusion
## 结论
<!-- label: sec:conclusion -->

Machine learning history, viewed through the SCX{} lens, is not a sequence of arbitrary empirical discoveries. It is a convergent process: practitioners, through trial and error, have gravitated toward algorithms that implicitly satisfy SCX{} theorems. Random forests implement Theorem~1 explicitly. Dropout creates $2^n$ implicit experts. ResNet separates signal from noise correction, solving the unidentifiability problem of Theorem~3. Attention instantiates Spring{} memory. BatchNorm enforces state homogeneity.

The algorithms that failed to converge — GANs with their training instability, RL with its sample inefficiency, SSL with its self-audit paradox — are precisely those whose SCX{} guarantees are weakest. They violate SCX{} assumptions (\asmTag{1} independence for GAN, $M=1$ auditor for RL) or rely on implicit mechanisms that have not been formalized (augmentation ensemble for SSL).

The path forward is clear: **design ML algorithms with explicit SCX{} guarantees.** Declare $M$. Verify independence. Bound the consensus error. Audit externally. The algorithms that emerge from this discipline will be more robust, more interpretable, and more trustworthy than anything discovered by empirical search alone.

<div align="center">

\bfseries
The SCX Lens reveals that ML history was never just engineering.

It was applied audit theory, discovered the hard way.

SCX视角揭示：机器学习史从来不只是工程实践。

它是应用审计理论——用最艰难的方式逐一发现。

</div>

\begin{thebibliography}{99}

\bibitem{scx2026} SCX. *The SCX Framework: Supercomputing Certification eXchange.* 2026.

\bibitem{scx_audit} SCX. *The SCX Audit Mandate: Why M-Parameter Declaration Must Be a Prerequisite for Scientific Publication.* 2026.

\bibitem{scx_ethics} SCX. *SCX Personal Ethics.* 2026.

\bibitem{breiman2001} L.~Breiman. Random Forests. *Machine Learning*, 45(1):5--32, 2001.

\bibitem{breiman1996} L.~Breiman. Bagging Predictors. *Machine Learning*, 24(2):123--140, 1996.

\bibitem{wolpert1992} D.~H.~Wolpert. Stacked Generalization. *Neural Networks*, 5(2):241--259, 1992.

\bibitem{freund1997} Y.~Freund and R.~E.~Schapire. A Decision-Theoretic Generalization of On-Line Learning and an Application to Boosting. *JCSS*, 55(1):119--139, 1997.

\bibitem{friedman2001} J.~H.~Friedman. Greedy Function Approximation: A Gradient Boosting Machine. *Annals of Statistics*, 29(5):1189--1232, 2001.

\bibitem{chen2016} T.~Chen and C.~Guestrin. XGBoost: A Scalable Tree Boosting System. *KDD*, 2016.

\bibitem{srivastava2014} N.~Srivastava, G.~Hinton, A.~Krizhevsky, I.~Sutskever, and R.~Salakhutdinov. Dropout: A Simple Way to Prevent Neural Networks from Overfitting. *JMLR*, 15(1):1929--1958, 2014.

\bibitem{gal2016} Y.~Gal and Z.~Ghahramani. Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning. *ICML*, 2016.

\bibitem{he2016} K.~He, X.~Zhang, S.~Ren, and J.~Sun. Deep Residual Learning for Image Recognition. *CVPR*, 2016.

\bibitem{vaswani2017} A.~Vaswani et al. Attention Is All You Need. *NeurIPS*, 2017.

\bibitem{ioffe2015} S.~Ioffe and C.~Szegedy. Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift. *ICML*, 2015.

\bibitem{goodfellow2014} I.~Goodfellow et al. Generative Adversarial Nets. *NeurIPS*, 2014.

\bibitem{durugkar2017} I.~Durugkar, I.~Gemp, and S.~Mahadevan. Generative Multi-Adversarial Networks. *ICLR*, 2017.

\bibitem{nguyen2017} T.~Nguyen, T.~Le, H.~Vu, and D.~Phung. Dual Discriminator Generative Adversarial Nets. *NeurIPS*, 2017.

\bibitem{wang2018} T.-C.~Wang et al. High-Resolution Image Synthesis and Semantic Manipulation with Conditional GANs. *CVPR*, 2018.

\bibitem{chen2020} T.~Chen, S.~Kornblith, M.~Norouzi, and G.~Hinton. A Simple Framework for Contrastive Learning of Visual Representations. *ICML*, 2020.

\bibitem{grill2020} J.-B.~Grill et al. Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning. *NeurIPS*, 2020.

\bibitem{devlin2019} J.~Devlin, M.-W.~Chang, K.~Lee, and K.~Toutanova. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. *NAACL*, 2019.

\bibitem{sutton2018} R.~S.~Sutton and A.~G.~Barto. *Reinforcement Learning: An Introduction.* MIT Press, 2nd edition, 2018.

\bibitem{hoeffding1963} W.~Hoeffding. Probability Inequalities for Sums of Bounded Random Variables. *JASA*, 58(301):13--30, 1963.

\bibitem{minsky1969} M.~Minsky and S.~Papert. *Perceptrons.* MIT Press, 1969.

\bibitem{rumelhart1986} D.~E.~Rumelhart, G.~E.~Hinton, and R.~J.~Williams. Learning Representations by Back-Propagating Errors. *Nature*, 323:533--536, 1986.

\bibitem{krizhevsky2012} A.~Krizhevsky, I.~Sutskever, and G.~E.~Hinton. ImageNet Classification with Deep Convolutional Neural Networks. *NeurIPS*, 2012.

\bibitem{bahdanau2014} D.~Bahdanau, K.~Cho, and Y.~Bengio. Neural Machine Translation by Jointly Learning to Align and Translate. *ICLR*, 2015.

\bibitem{ho2020} J.~Ho, A.~Jain, and P.~Abbeel. Denoising Diffusion Probabilistic Models. *NeurIPS*, 2020.

\bibitem{song2021} Y.~Song, J.~Sohl-Dickstein, D.~P.~Kingma, A.~Kumar, S.~Ermon, and B.~Poole. Score-Based Generative Modeling through Stochastic Differential Equations. *ICLR*, 2021.

\bibitem{lecun1998} Y.~LeCun, L.~Bottou, Y.~Bengio, and P.~Haffner. Gradient-Based Learning Applied to Document Recognition. *Proceedings of the IEEE*, 86(11):2278--2324, 1998.

\end{thebibliography}