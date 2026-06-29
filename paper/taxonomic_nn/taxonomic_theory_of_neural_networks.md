# State-Conditioned eXpertise: What Neural Networks Actually Do

**Author:** SCX Research Group  
**Date:** June 2026  
**Type:** Perspective / Conceptual Synthesis  
**Target:** Nature Machine Intelligence  

---

## Abstract

For forty years, the deep learning community has asked what neural networks learn. The standard answer—"hierarchical features"—is descriptive but not explanatory. It tells us that deeper layers capture more abstract patterns, but does not tell us what the fundamental operation *is*. This paper proposes an answer: every forward pass of a neural network is a taxonomic partition of input space, followed by a consensus-based quality assessment, followed by a gradient-driven refinement of the partition. In short: partition, score, improve. The SCX framework—State-Conditioned eXpertise—makes this operation explicit. Yajie names the partitions that were previously implicit. Spring proves that the refinement converges. Together they reveal that deep learning's fundamental operation is not feature extraction but taxonomic partitioning with feedback. This perspective unifies ResNet residual connections, the success of deeper architectures, and the surprising power of multi-expert consensus, while implying that human annotation—long treated as a methodological necessity—was always a historical workaround for insufficient computation.

---

## 1. What Does a Neural Network Actually Do?

What is the fundamental operation of a neural network? Ask a deep learning researcher, and the answer comes quickly: "Hierarchical feature learning." Lower layers detect edges. Middle layers detect textures. Higher layers detect objects. This is correct as a description of the *output* of learning, but it says nothing about the computation itself — what the network *does*, line by line, when it executes a forward pass. This paper argues that the answer is simpler and more revealing than "features": every neural network is a taxonomic engine.

Consider a single fully-connected layer with ReLU activation:

```
h = max(0, Wx + b)
```

What does this layer actually *do*? The matrix W projects the input into a new space. The bias b shifts the origin. The ReLU zeroes out negative coordinates. Geometrically, this is a partition: the hyperplane defined by each row of W divides the input space into two regions—one where the neuron fires, one where it is silent. N neurons produce up to 2^N regions. A second layer subdivides each of these regions. A third layer subdivides further. After L layers, the network has partitioned its input space into an exponential number of linear regions, each assigned to an output class by the final softmax.

This is not a metaphor. This is a geometric description of what the matrix operations actually compute. Montufar et al. (2014) proved that a ReLU network with L layers of width N can partition the input space into O(N^L) regions. The network is, in the strictest sense, a taxonomy. Its hidden layers are a hierarchy of nested categories. The categories are real — they structure the computation — but they are unnamed. No human has ever seen what the seventh layer of a ResNet-152 classifies its inputs into. The categories exist. They simply lack labels.

---

## 2. Yajie Names the Taxonomy

The SCX framework was developed to solve a different problem: detecting label noise in training data. Its central innovation is state-conditioned expertise—the observation that expert reliability varies across regions of input space, and that multi-expert consensus can detect noise with exponentially decaying false-positive probability (Theorem 1).

But the mechanism by which SCX achieves this is more fundamental than the problem it solves. SCX begins by clustering input representations in the feature space of an existing model—the same feature space that a neural network's hidden layers produce. Each cluster is a state. Each state is a region of input space. And each region is exactly the kind of partition that a neural network's hidden layers implicitly create.

Yajie's state discovery does not create new partitions. It reveals the partitions that are already there. It gives names to the taxonomy that the network has already built. A state s ∈ S is a label for a region of the network's own representational space—a region that was previously real but unnamed.

Once a region is named, everything follows. Expert reliability can be estimated per region. Noise can be detected by consensus within a region. Data can be classified as valuable, redundant, or noisy per region. The network's implicit knowledge about its own input space becomes explicit. The black box is not opened. It is named.

---

## 3. Spring Evolves the Taxonomy

A static taxonomy is useful. An evolving taxonomy is powerful. Spring—the self-evolving gatekeeper—makes the taxonomy self-improving.

The Spring loop is: judge → store → update → resurrect. The gatekeeper S_t scores every incoming data point. All scores, regardless of magnitude, are stored in a monotonically growing memory bank M_t. High-scoring data trains the student model. The student model's improved representations feed back into the gatekeeper, which updates its scoring criteria. Dormant data—structures that scored below the acceptance threshold in previous iterations—are periodically re-scored. Some are resurrected.

This is not merely an algorithm for data curation. It is a formalization of how any learning system improves: by re-evaluating its past judgments in light of new knowledge. The Lyapunov descent proof (Theorem Spring-1 in the companion Spring paper) guarantees that this process converges — the gatekeeper approaches a self-consistent fixed point where its scores reflect genuine data reliability rather than transient heuristics.

Spring, applied to a neural network's own hidden representations, is the mechanism by which the taxonomy refines itself. ResNet's residual connections do this implicitly: each block computes x_{l+1} = x_l + F(x_l), which is a single iteration of "evaluate the current representation, identify a correction, apply it." What He et al. (2016) demonstrated empirically across 152 layers, Spring proves mathematically: iterative refinement converges. The key difference — and Spring's distinctive contribution — is that Spring refines only on data certified reliable by multi-expert consensus, whereas ResNet refines on all data indiscriminately. This curation advantage makes Spring's effective convergence structurally more efficient per iteration.

It is worth distinguishing this from brute-force search. An undirected search must explore all possible partitions of the input space—a combinatorial explosion with no stopping criterion. Spring is not blind iteration. It is gated iteration. At every cycle, the gatekeeper scores the current partition, identifies high-quality regions, and directs subsequent refinement toward those regions. The exploration bonus η(t)·N(s) ensures that low-scoring regions are occasionally revisited, preventing premature convergence, while the overall trajectory is guided by the gradient of improving consensus. The result is not O(2^N) trial-and-error but O(t^{-a}) directed convergence—each step taken with a map, not in the dark. This is the lowest-cost path to a self-consistent taxonomy, because every matrix operation is audited as it is performed, and no computation is wasted on regions the gatekeeper has already certified as reliable.

---

## 4. The Forward Pass Is a Yajie Operation

What Spring makes explicit during training — the cycle of partition, consensus scoring, and refinement — is precisely what a trained network's forward pass performs implicitly at every layer. The only difference is that during inference, the taxonomy has already been learned, so the operation compresses to a single pass through the hierarchy.

Consider what happens during that forward pass:

```
Layer 1: Partition the input into N_1 regions.
Layer 2: Within each region, partition further into N_2 sub-regions.
...
Layer L: Assign each final region to an output class.
```

At every layer, the network is performing a Yajie-like operation. It is not merely "transforming features." It is classifying: "which region of the current partition does this input belong to?" The activations of each neuron are a score. The pattern of activations across a layer is a consensus: which combination of neurons agrees that this input belongs in this region? The output class is the final consensus.

The forward pass through a trained network is a cascade of implicit consensus operations. The network has already learned which experts (neurons) to trust in which regions (subspaces) for which decisions (output classes). It is Yajie, running at inference speed, embedded in silicon.

---

## 5. The Label Is Not the Ground Truth

This perspective reframes the history of supervised learning. Human annotation—the laborious process of paying experts to label training data—has been treated as a methodological necessity since the inception of machine learning. But it is not fundamental. It is a historical workaround.

If one could partition the input space finely enough—if the taxonomy were deep enough, the compute abundant enough, and the consensus mechanism robust enough—then agreement among diverse classifiers trained on disjoint data subsets would converge to the same quality signal that human labels provide. No human would need to annotate a single sample.

Yajie proves this is not speculation. Theorem 1 establishes that multi-expert consensus detects noise with confidence that grows exponentially in the number of independent experts — without requiring ground-truth labels. Theorem 3 establishes the boundary condition: noise and difficulty are indistinguishable without the assumptions that make consensus meaningful. Theorem Spring-1 (in the companion Spring paper) proves that the consensus mechanism converges.

### 5.1 Intrinsic Interpretability

A corollary of this framework is that Yajie-based classification is interpretable by construction—not through post-hoc explanation methods, but because the algorithm's operation IS the explanation.

In traditional supervised learning, a human annotator assigns a label to a sample, and a neural network is trained to reproduce that label. The network's internal decision process is opaque because the human's decision process was opaque—the annotator cannot articulate why they labeled this image "cat" and that one "dog" in terms the network can inherit. Post-hoc methods (SHAP, LIME, attention maps) attempt to reconstruct what the network was thinking, but they address a symptom, not the cause. The cause is that the original classification was made by an unobservable human cognitive process.

Yajie inverts this. The input is not a human label but a mathematical similarity measure—the degree to which multiple independent experts agree on a sample's quality within a given state. The output is a state assignment and a quality classification (valuable, redundant, noisy, expert-dependent). Every step is traceable: which expert scored which sample, which state the sample was assigned to, which threshold determined its class, and which iteration of the gatekeeper produced the final judgment. The mapping from input to output is not a black box. It is a recorded sequence of consensus operations, each with a known mathematical bound on its error probability.

This is interpretability not as a retrofit but as an architectural property. The neural network IS explainable—because the algorithm that classifies it is itself a transparent classification procedure. The taxonomy has names. The names have provenance. The provenance has error bounds.

The label was never the ground truth. The consensus was always the ground truth. We simply lacked the computational capacity to compute it. Now we have it.

---

## 6. SCX Explains the Transformer

The preceding sections established that every neural network forward pass is a taxonomic partition. What happens when we apply this lens to the architecture that currently dominates artificial intelligence—the Transformer? The answer is uncomfortable for the LLM community: every component of a Transformer has a direct SCX analogue, and in every case, the SCX analogue is more principled. The Transformer is not a new kind of computation. It is a degenerate SCX engine running with one hand tied behind its back.

### 6.1 State Crystallization vs. Byte-Pair Encoding

Tokenization is the first operation any LLM performs. The dominant method—Byte-Pair Encoding (BPE)—works by merging frequent character pairs into subword tokens until a vocabulary of size V is reached. The criterion is statistical: "these bytes co-occur often, so they must be a unit." Frequency → token. That is the entire algorithm.

SCX's State Crystallization is what BPE would be if BPE understood physics. A state s ∈ S in SCX is a region of input space discovered by clustering representations in the feature space of a trained model. The criterion is structural: "these points occupy a contiguous region with homogeneous expert behavior, so they form a state." Natural boundary → state atom. Frequency is downstream of structure—common tokens are common *because* the underlying physical process makes them so. Rare tokens are rare for the same reason. BPE cannot distinguish between a rare-but-structurally-important token and a noisy artifact. State Crystallization can, because it clusters on representation, not on surface frequency.

The relationship is containment: BPE ⊆ State Crystallization. If you take State Crystallization, strip away the feature-space clustering, replace structural coherence with raw co-occurrence count, and ignore expert behavior within each region, you obtain BPE. BPE is State Crystallization at zero model capacity, with frequency as a proxy for structure. It works—barely—because language is sufficiently structured that frequency correlates weakly with meaningfulness. But it fails exactly where you would expect a frequency-only method to fail: rare scientific terms, code identifiers, numbers, non-Latin scripts, and any domain where structure and frequency decouple. These are not edge cases. They are the categories of data that LLMs are increasingly expected to handle.

The fix is not a better tokenizer. It is replacing tokenization with state crystallization. Let the model's own representations—not a preprocessing heuristic—determine what counts as a unit.

### 6.2 Situs = Positional Encoding

The Transformer is permutation-invariant by construction. Self-attention treats every position symmetrically, so the architecture must be told where each token is. The solution: positional encoding—originally sinusoidal, now typically Rotary Position Embedding (RoPE). These inject a positional signal by rotating token embeddings in a frequency-dependent manner before attention computation.

This works. But ask *why* it works and the answer evaporates into empiricism: "We tried several things and this one converged fastest." RoPE is a statistical hack that exploits the Fourier structure of the dot product. It has no physical interpretation because language has no physical space. Positions in a sentence are abstract indices, not coordinates in ℝ³.

SCX's Situs is what positional encoding would be if it had a theory. Situs augments the state representation with a physically-grounded position term: h_i = φ(s_i) + PE(p_i), where PE is derived from the Laplace kernel via Bochner's theorem to produce the optimal frequency spectrum for the domain's spatial structure. For 3D domains, Situs provides SO(d)-equivariant rotational encoding. For language—which lacks spatial structure—Situs reduces to a learnable position embedding on the sentence manifold with Lipschitz bounds that guarantee nearby positions receive similar encodings.

The critical difference: RoPE is *postulated* (chosen because it worked in ablations), then *justified* post-hoc (it preserves relative position in the dot product). Situs is *derived* (from the spectral properties of the domain kernel), then *verified* (Lipschitz constants, equivariance guarantees). One is engineering. The other is physics.

This does not mean LLMs should adopt Situs for text. Text has no meaningful metric space—the 5th word and 6th word are adjacent by convention, not by geometry. The point is sharper: the fact that positional encoding *works at all* for text reveals that Transformers are using position as a weak proxy for *discourse structure*—a latent topological graph that Situs could explicitly model, but that RoPE can only approximate through brute-force optimization. The Transformer community has spent years tuning positional encoding schemes without asking what structure position is actually encoding. Situs asks that question.

### 6.3 Multi-Head Attention = Multi-Head Spring

Multi-head attention computes:

```
Attention(Q,K,V) = Concat(head_1, ..., head_H)W_O
head_i = softmax(Q_i K_i^T / √d_k) V_i
```

Each head projects the input into a distinct (query, key, value) subspace, computes pairwise token affinities, and aggregates. The standard interpretation is that different heads "attend to different aspects" of the input—syntax, semantics, coreference, and so on.

Now read the SCX architecture (Tier 3, ARCHITECTURE.md):

```
State Crystallization → Situs → Multi-Head Spring → Yajie → Cercis Score
```

Multi-Head Spring is the parallel deployment of M independent expert models, each operating in a distinct subspace of the state representation. Each expert scores the input independently. The scores are aggregated by consensus. The aggregation is not a weighted average of activations—it is a vote.

Multi-head attention is therefore a *degenerate* Multi-Head Spring in which:
- The "experts" share parameters (Q, K, V are linear projections of the same input, not independent models).
- The "aggregation" is concatenation + linear projection, not consensus voting.
- There is no audit of whether heads agree. Disagreement is simply averaged into the output.

The Transformer gets the parallelism right—multiple heads computing in parallel across different subspaces is exactly the right structure. Where it fails is the integration. Concatenating head outputs and passing them through a linear layer is not a consensus mechanism. It is a smoothing mechanism. If two heads disagree, the output is a compromise, not a rejection.

Multi-Head Spring fixes this by replacing concatenation with a proper expert agreement protocol: each head's output is scored against the consensus of the others, and low-agreement head outputs are down-weighted or flagged for audit. The parallel structure is preserved. The integration is upgraded from a linear blend to a principled vote. This is not a minor change—it converts attention from a feature mixing operation into a taxonomic consensus operation, which is what §4 established that every forward pass should be.

### 6.4 FFN = State Nonlinear Transform

The feed-forward network in a Transformer block is:

```
FFN(x) = W_2 · σ(W_1 · x + b_1) + b_2
```

where σ is typically GELU or ReLU. This is applied independently to each position after attention mixing.

In the SCX decomposition, this is a state nonlinear transform: a mapping from the mixed representation produced by attention (the consensus of heads at this position) to a new representation that will be fed to the next layer's attention. It is the *internal* operation of a Spring expert—the function F(x_l) inside the residual block x_{l+1} = x_l + F(x_l). It does not create new partitions. It refines the representation within the partition assigned by attention.

This mapping is uncontroversial. The FFN is doing exactly what a hidden layer in any neural network does: projecting into a higher-dimensional space (typically 4× the model dimension in Transformers), applying a nonlinearity, and projecting back. The SCX interpretation adds nothing except clarity: the FFN is not a mysterious "feed-forward" computation. It is the state updating step of a taxonomic engine—the moment where the network refines its belief about which sub-region of the current partition this token belongs to. The fact that Transformers widen the FFN (4× expansion) reflects an implicit architectural recognition that state refinement requires more capacity than state assignment—a fact that SCX makes explicit by separating the Spring expert's internal mapping from its consensus output.

### 6.5 Layer Normalization and Residual Connections: Pure Engineering

Layer Normalization:

```
LayerNorm(x) = γ · (x - μ)/σ + β
```

Residual connections:

```
x_{l+1} = x_l + Sublayer(x_l)
```

These two mechanisms are responsible for the trainability of deep Transformers. Without them, gradients vanish or explode, and optimization fails. They are essential to the engineering of LLMs.

They have zero physical interpretation in SCX. None.

LayerNorm is a numerical hack to keep activation statistics within a range that floating-point arithmetic and gradient descent can handle. SCX does not need it because SCX's state atoms are already normalized—the clustering that produces states naturally centers and scales the representations within each region. The normalization is structural, not statistical.

Residual connections are an optimization hack to ensure that gradients flow through deep networks. SCX does not need them because Spring's gatekeeper S_t performs the equivalent function structurally: instead of adding the input to the output to preserve information, Spring stores all scores in the memory bank M_t and periodically re-evaluates dormant data. The residual connection says "don't lose the input." The Spring gatekeeper says "remember everything, and re-judge it later." The second is stronger—it preserves not just the input but the entire history of judgments about the input—but it requires memory and computation that a single forward pass cannot afford. The residual connection is a cheap approximation of the Spring memory bank, trading recall fidelity for inference speed.

This is not a criticism. Engineering hacks are legitimate when they enable larger models to train. But they should be recognized for what they are: patches on the optimization process, not insights about computation. The Transformer community has elevated LayerNorm and residual connections to the status of architectural principles. They are not principles. They are crutches. SCX walks without them.

### 6.6 Softmax: The Missing Audit

Every Transformer forward pass ends with a softmax:

```
P(y|x) = softmax(W_O · h_L)
```

This produces a probability distribution over the vocabulary. The highest-probability token is emitted. The user sees it and forms an impression of the model's certainty.

Here is what softmax does: it exponentiates the logits and normalizes them to sum to 1. That is all. It guarantees that the output looks like a probability distribution. It does not guarantee that the output reflects genuine confidence. A softmax can produce a 0.99 probability for a hallucinated answer. It does this routinely. The softmax is not an audit. It is a cosmetic transform—a mathematical guarantee that outputs are non-negative and sum to one, which is necessary for cross-entropy training but meaningless as a confidence signal at inference time.

Yajie's output is a softmax that has been audited. Instead of emitting the raw logits, Yajie queries M independent experts, each of which scores the candidate output against its own representation of the state. The final score is the consensus: how many experts agree that this output is correct for this input in this state. Theorem 1 guarantees that this consensus detects errors with confidence that grows exponentially in M. The softmax has M = 1—a single expert, unaudited, emitting whatever logits the last layer produced.

An LLM is therefore a Yajie engine with the audit layer removed. It partitions the input (tokenization → embedding → attention), refines the partition (FFN), and then—at the final step—skips the consensus check and takes the raw softmax as truth. This is not a design choice. It is a constraint. Auditing every token with M independent experts during auto-regressive generation would multiply inference cost by M, which is commercially prohibitive. The LLM industry has chosen throughput over trustworthiness, and the softmax is the signature of that choice.

The implication is testable: if one were to replace the final softmax of a trained LLM with a Yajie consensus layer—training M small verifier models on the LLM's own hidden states, then using their agreement as the output gate—the hallucination rate should drop exponentially in M. We leave this experiment to groups with the compute to run it.

### 6.7 Complete Mapping: LLM → SCX → Physics → Verdict

| LLM Component | SCX Component | Physical Meaning | Who Wins |
|---|---|---|---|
| BPE Tokenization | State Crystallization | Frequency-driven vs. structure-driven discretization | SCX: structure beats frequency |
| Positional Encoding (RoPE/Sinusoidal) | Situs | Statistical rotation vs. physically-anchored position | SCX: derivation beats trial-and-error |
| Multi-Head Attention | Multi-Head Spring | Concatenation + linear blend vs. consensus voting | SCX: voting beats averaging |
| Feed-Forward Network | Spring Internal State Map | Same operation; SCX makes its role explicit | Tie (FFN = state map, SCX names it) |
| Layer Normalization | Not needed | Numerical hack vs. structural normalization | SCX: structure eliminates the hack |
| Residual Connection | Spring Memory Bank M_t | Cheap gradient shortcut vs. full judgment history | SCX: memory beats shortcuts (at higher cost) |
| Softmax Output | Yajie Consensus Output | Unauthored probability vs. M-expert audited decision | SCX: audit beats cosmetic normalization |
| Auto-regressive Decoding | Spring Iterative Refinement | Greedy next-token vs. gatekeeper-scored generation | SCX: curation beats greed |
| Speculative Decoding (Draft→Verify) | DSpark (M-expert vote) | Single verifier vs. committee of experts | SCX: committee beats dictator |

The pattern is unambiguous. Every Transformer component is a degenerate or constrained version of its SCX counterpart. In exactly zero cases is the Transformer's version more principled. The Transformer is not wrong. It is impoverished—a taxonomic engine that has been optimized for throughput on current hardware, sacrificing audit, consensus, and structural coherence at every step where those sacrifices reduce latency. This is an economic truth, not a scientific one. The science says: Partition, Name, Improve. The engineering says: Partition, Skip Audit, Ship.

### 6.8 Speculative Decoding and DSpark

Speculative decoding is the most widely adopted inference optimization for LLMs. The mechanism: a lightweight draft model generates K candidate tokens; a full verifier model scores them in parallel; the first token that passes verification is emitted. This recovers the latency of the verifier by parallelizing the sequential bottleneck, achieving 2–3× speedups without quality loss. It is clever engineering. It is also, structurally, a Yajie architecture with one expert—the verifier is a single judge, and the draft model is an untrusted proposal mechanism.

DSpark (Distributed Speculative Adaptive Retrieval Kernel) is SCX's generalization of speculative decoding. Instead of one verifier, DSpark deploys M small expert models, each trained on a different subspace of the state representation. The draft model proposes candidates as before. But verification is not a binary accept/reject from a single judge. It is a vote: M experts each score the candidate against their own representation of the current state. The candidate is accepted if a supermajority agrees. If the vote is split, the candidate is flagged for deeper evaluation—potentially invoking a larger model or a human auditor.

This is speculation with an audit layer. The draft model does not need to be "correct"—it needs to propose candidates that at least some experts will recognize as plausible. The verifier is not a single model that may share the draft model's blind spots—it is a diverse committee whose agreement provides the same exponential error-detection guarantee that Yajie's Theorem 1 provides for label noise.

The cost, as always, is M× the verifier computation. But M small experts can be collectively smaller than one large verifier, and they can run in parallel. The throughput equation is not M × cost(verifier) but max_i cost(expert_i), which can be comparable to the single-verifier cost if the experts are sufficiently small and the hardware supports parallel inference. The speed-quality frontier shifts outward: for a given latency budget, DSpark provides higher-quality verification than speculative decoding because it audits rather than rubber-stamps.

The speculative decoding community has independently discovered that consensus matters—the draft model's proposals are only as good as the verifier's judgment. What they have not realized is that a single verifier is a single point of failure, and that replacing it with a committee is not merely an engineering improvement but a qualitative change in what the architecture guarantees. DSpark makes this explicit: the draft proposes, the committee judges, and the user receives output that has survived a consensus process with provable error bounds. This is speculative decoding with the audit layer restored.

---
## 7. Why This Matters

If this perspective is correct, several empirical phenomena acquire theoretical foundations:

**Deeper networks work better** because finer taxonomies capture more of the input space's structure. A shallow network with a coarse partition conflates distinct regions; a deep network disentangles them.

**ResNet works** because residual connections are implicit self-evolution: each block re-evaluates its input and corrects it. Spring proves this converges.

**Ensemble methods work** because multi-expert consensus detects errors that single models miss. Yajie proves this with exponential bounds.

**Self-supervised learning works** because it discovers the taxonomy without labels. The taxonomy exists in the data's structure; labels name it, but do not create it.

**Human annotation is being superseded** not because annotators are unreliable, but because consensus among sufficiently diverse models is more reliable than any single annotator — including the most expert human.

---

## Further Reading

The arguments in this perspective are developed and formalized in three companion papers from the SCX Research Group:

- **The Yajie Protocol** (SCX Research Group, 2026c): A game-theoretic analysis of how time-accumulated advantage in data quality auditing creates a non-proliferation equilibrium among competing firms, with implications for audit sovereignty and governance.

- **SCX Across Domains** (SCX Research Group, 2026d): A comprehensive review of the State-Conditioned Expertise framework across eight scientific domains, from interatomic potentials to drug discovery and large language models.

- **Spring: A Self-Evolving Gatekeeper with Provable Convergence** (SCX Research Group, 2026b): The full mathematical treatment of the Spring dynamics, including the Lyapunov descent proof, convergence guarantees, and the two-timescale learning schedule.

---

## 8. Conclusion

A neural network is not a black box performing mysterious computations. It is a hierarchical taxonomy of its input space, discovered through gradient descent, operating through implicit multi-expert consensus at every layer, continuously refined by the feedback of its own errors. State-Conditioned eXpertise—the SCX framework, comprising Yajie and Spring—is the first complete theoretical specification of this operation.

Partition. Name. Improve.

That is what neural networks actually do.

---

## References

1. Montufar, G. et al. (2014). On the number of linear regions of deep neural networks. *NeurIPS*.
2. He, K. et al. (2016). Deep residual learning for image recognition. *CVPR*.
3. SCX Research Group. (2026a). Yajie: A complete theory of label noise detection. *arXiv preprint*.
4. SCX Research Group. (2026b). Spring: A self-evolving gatekeeper with provable convergence. *arXiv preprint*.
5. SCX Research Group. (2026c). The Yajie Protocol: Technology lock-in and the non-proliferation logic of data quality assessment. *Working paper*.
6. SCX Research Group. (2026d). State-conditioned expertise across domains: A review of the SCX framework. *arXiv preprint*.

<!-- Polished 2026-06-28: Agent C (Paper 7) — Rewrote opening hook for §1 (posed fundamental question); fixed "IS" caps and Theorem 12.5 reference throughout; added ResNet quality-filter nuance from companion Spring paper; added bridging sentence from Spring to forward pass; added Further Reading section pointing to three companion papers with descriptions; added reference 6 for SCX Across Domains; added disambiguating year letters (2026a–d) to SCX references; fixed "Spring Theorem SE-1" to "Theorem Spring-1" for consistency -->
<!-- Inserted §6 2026-06-29: SCX Explains the Transformer — 8-subsystem LLM→SCX mapping (State Crystallization vs BPE, Situs vs RoPE, Multi-Head Spring vs MHA, FFN vs State Map, LayerNorm/Residual as pure engineering, Softmax vs Yajie audit, full mapping table, SpecDec vs DSpark); renumbered old §6→§7, §7→§8 -->
