*Abstract:*

We prove a fundamental impossibility theorem for data quality assessment: given only the observed outputs of multiple independent expert models, it is mathematically impossible to distinguish whether a label disagreement arises from label noise or from inherent sample difficulty. The two worlds — one where the label is randomly flipped, another where the sample admits multiple valid labels — produce identical joint observation distributions. No algorithm operating solely on these observations can separate them. We call this SCX's Uncertainty Principle.

We then show that this theorem applies directly to the hallucination problem in large language models: by running $M$ independent decoding passes with different random seeds, the same LLM produces $M$ conditionally independent ``expert'' opinions. From these $M$ outputs alone, one cannot distinguish a model error from essential ambiguity in the query. Hallucinations are therefore not merely an engineering limitation — they are an information-theoretic necessity with a provable lower bound of $\eta\rho/2$, where $\eta$ is the ambiguity rate and $\rho$ the proportion of ambiguous queries.

Two corollaries follow: first, any method claiming to detect hallucinations without access to external verification sources must declare its additional structural assumptions. Second, the path to reducing hallucinations is not better models alone — it is breaking the information closure of the system, through retrieval-augmented generation, human feedback, or tool use.

The theorem is self-contained: it requires only conditional independence of expert errors (a standard condition satisfied by independent random seeds) and makes no assumptions about model architecture, training data, or loss function. It can be read, verified, and applied independently of the broader SCX framework.

## The Problem

Consider $M$ experts evaluating a sample. The experts disagree. Is the label wrong, or is the sample genuinely hard?

This question underlies every data quality pipeline: medical image annotation, protein function prediction, variant calling in genomics, and — as we show — hallucination detection in language models.

We prove: **without additional structural assumptions, this question is undecidable.**

## Theorem SCX-UP (Uncertainty Principle)

### Setup

Let $\mathcal{X} \times \mathcal{Y}$ be the input-label space with $|\mathcal{Y}| = K \geq 2$. Let $f^*: \mathcal{X} \to \mathcal{Y}$ be the ground-truth oracle (unobservable). Let $\{f_m\}_{m=1}^M$ be $M$ expert models with bounded loss $\ell \in [0, B]$.

Define the consensus score: $C(x) = \frac{1}{M} \sum_{m=1}^M \mathbf{1}\{\ell(f_m(x), y) > \tau\}$.

### Theorem Statement

> **Theorem:** [Noise-Difficulty Indistinguishability]
> <!-- label: thm:scx-up -->
> For any $K \geq 2$, $M \geq 1$, there exist two data-generating processes — $\mathcal{P}_{noise}$ (World A) and $\mathcal{P}_{hard}$ (World B) — such that:
> 
1. In $\mathcal{P}_{noise}$, label errors are caused by label flipping (noise rate $\eta_{err}$ on subset of proportion $\rho$).
2. In $\mathcal{P}_{hard}$, all observed labels are correct, but samples in the same subset are inherently difficult (ambiguity rate $\eta_{amb}$).
3. **Both worlds produce identical observation distributions** if and only if $\eta_{err} = \eta_{amb} = \eta$.
4. For any algorithm $\mathcal{A}$ that takes only the observations as input, the maximum error rate satisfies:

### Construction (Binary Case, $K=2$)

**World A (Noise-Driven).** In a designated state $s_1$ with $\mathbb{P}(X \in s_1) = \rho$, the ground truth is $y^* \equiv 0$. Labels are flipped with probability $\eta_{err}$. Experts predict correctly with accuracy $1 - \varepsilon_1$ on clean labels.

**World B (Difficulty-Driven).** In state $s_1$, the ground truth is itself random: $\mathbb{P}(y^*=0) = 1-\eta_{amb}$, $\mathbb{P}(y^*=1) = \eta_{amb}$. Experts have a fixed bias toward class 0: regardless of $y^*$, $\mathbb{P}(f_m=0) = 1-\varepsilon_1$.

**Equivalence Verification.** Under $\eta_{err} = \eta_{amb} = \eta$:

- $\mathcal{P}_{noise}(y=0 \mid s_1) = 1-\eta = \mathcal{P}_{hard}(y=0 \mid s_1)$ \checkmark
- $\mathcal{P}_{noise}(f_m=0 \mid s_1) = 1-\varepsilon_1 = \mathcal{P}_{hard}(f_m=0 \mid s_1)$ \checkmark
- The full joint distributions are identical \checkmark

**Algorithmic Impossibility.** Any algorithm $\mathcal{A}$ labeling samples as ``noise'' or ``hard'' has error:

- In World A: $Error = \rho\eta_{err}(1-a)$ where $a$ is the fraction of noisy samples correctly detected.
- In World B: $Error = \rho\eta_{amb}a$ where the same $a$ now represents false alarms.

Under $\eta_{err} = \eta_{amb} = \eta$, the maximum of the two errors is minimized at $a = 1/2$, yielding the $\eta\rho/2$ lower bound.  $\square$

### Essential Nature of the Result

This is not a ``no free lunch'' theorem that requires the full SCX axiom system. The construction requires only conditional independence of expert errors (A2) — a standard condition satisfied whenever experts are trained on disjoint data or, as we show below, when they are independent random-seed decoding passes of the same model.

## Application: LLM Hallucinations

### Multi-Seed Independent Decoding

**Key insight.** Run the same LLM $M$ times on the same input context $c$, each time with a different random seed $r_m$. The seeds are independent by construction in all modern deep learning frameworks (PyTorch, JAX, TensorFlow).

For a fixed model $\theta$ and context $c$:

- The deterministic component $f_\theta(c)$ (the forward pass up to the logits) is identical across seeds.
- The stochastic component $\xi_m = \xi(c; r_m)$ (logit perturbation from seed-dependent dropout, sampling noise, or temperature scaling) is independent across seeds: $\xi_m \perp \xi_{m'} \mid c$.

Define the error indicator $e_m(c) = \mathbf{1}\{output of seed  m  is factually incorrect for  c\}$. Since $e_m = g(f_\theta(c), \xi_m, y^*(c))$ and $\xi_m \perp \xi_{m'}$, the error indicators are conditionally independent: $e_m \perp e_{m'} \mid c$.

Theorem [ref] applies directly. From $M$ seed outputs alone, one cannot distinguish whether disagreement arises from model error (clear question, model got it wrong) or essential ambiguity (multiple valid answers exist).

> **Theorem:** [Hallucination Lower Bound]
> <!-- label: thm:hallucination -->
> For an LLM queried $M$ times with independent random seeds, the hallucination rate on ambiguous queries satisfies:
> 
> $$
> Hallucination_{ambiguous} \geq \frac{\eta\rho}{2}
> $$
> 
> where $\eta$ is the conditional probability of model error on ambiguous queries and $\rho$ is the proportion of ambiguous queries.

### The Symmetry Condition

The theorem requires $\eta_{err} = \eta_{amb}$ — the error rate on clear queries equals the ambiguity rate on unclear ones. In the multi-seed setting, this has a natural interpretation: the perturbation distribution $\xi_m$ is the same across all queries, so the probability that $\xi_m$ pushes the output away from the correct answer on a clear question equals the probability that it pushes toward a particular valid answer on an ambiguous question. While this equality is not automatic — it depends on the geometry of the logit landscape — it is a testable condition that can be empirically verified for specific models and query distributions.

### Breaking the Bound

The theorem's premise is ``given only the $M$ seed outputs.'' Any method that introduces information beyond these outputs breaks the bound:

- **Retrieval-Augmented Generation (RAG):** Retrieved documents are external verification sources not present in the seed outputs alone.
- **RLHF:** Human preference labels introduce ground-truth anchors that break the symmetry between the two worlds.
- **Tool use / code execution:** External execution results distinguish model error (wrong answer, execution would catch it) from essential ambiguity (multiple answers, all pass execution).

The practical implication is clear: **hallucinations cannot be eliminated by scaling alone. They can only be managed by breaking the information closure of the autoregressive generation loop.**

## Discussion

### Relationship to Known Results

Theorem [ref] occupies a specific ecological niche in the theory of machine learning:

[Table omitted — see original .tex]

Where NFL says ``no universal learner'' and IB says ``optimal compression,'' SCX-UP says ``no universal noise detector.'' Together they form a triad of impossibility results spanning the full ML pipeline: learning $\to$ representation $\to$ quality assessment.

### Generality

The theorem does not depend on:

- Model architecture (transformer, CNN, RNN, or ensemble)
- Training procedure (supervised, self-supervised, or RL)
- Loss function (cross-entropy, MSE, or custom)
- Dataset scale (ImageNet, C4, or custom)

It requires only conditional independence of expert errors — a condition satisfied by independent random seeds in any modern ML framework.

### Falsifiability

The theorem makes a refutable prediction: if an independent evaluator with access to ground-truth labels can reliably distinguish ``model error'' from ``essential ambiguity'' on a held-out set of queries — doing better than the $\eta\rho/2$ lower bound without using external verification sources — then the symmetry condition $\eta_{err} = \eta_{amb}$ is violated, which itself is a measurable property of the query distribution and model behavior.

## Conclusion

We have proven a fundamental bound on data quality assessment: label noise and inherent difficulty produce observationally identical expert behavior. From this single theorem flow several consequences:

1. LLM hallucinations have an information-theoretic lower bound — they cannot be eliminated by better models or more data alone.
2. Any method claiming to detect noise or hallucinations must declare its structural assumptions.
3. The path to trustworthy AI lies not in perfect models but in architectures that break information closure through external verification.

The theorem is self-contained, requiring only the standard condition of conditionally independent experts. It can be independently read, verified, replicated, and applied — without accepting the broader SCX framework from which it emerged.

## Appendix: Mathematical Context

The full SCX axiom system — from which Theorem SCX-UP emerges as the third of four core theorems — is developed in the companion technical report ``A Taxonomic Theory of Neural Networks: Derivation of Known Machine Learning Phenomena from the SCX Axiom System'' (arXiv, 2026). That work demonstrates how five additional ML phenomena (ensemble effectiveness, depth advantage, representation learning, self-supervised pre-training, and the historical contingency of deep architectures) follow as corollaries.

**Keywords:** impossibility theorem, noise detection, hallucination, language models, data quality, uncertainty principle, information theory