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

The label was never the ground truth. The consensus was always the ground truth. We simply lacked the computational capacity to compute it. Now we have it.

---

## 6. Why This Matters

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

## 7. Conclusion

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
