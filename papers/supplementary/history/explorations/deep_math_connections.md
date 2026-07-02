\section{Deep Mathematical Connections of the SCX
Theory}<!-- label: deep-mathematical-connections-of-the-scx-theory -->

> **Date**: 2026-06-28 |{} **Type**: Theoretical analysis
> **Status**: Contains both proven connections and speculative
> (marked ``conjectural'') extensions **Purpose**: Situate SCX within
> the broader landscape of pure and applied mathematics

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Table of Contents<!-- label: table-of-contents -->

1. 
2. 
3. 
4. 
5. 
6. 
7. 
8. 
9. 
10. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{1. What Mathematical Domain Does SCX Belong
To?}<!-- label: what-mathematical-domain-does-scx-belong-to -->

#### 1.1 The Surface Answer<!-- label: the-surface-answer -->

At first glance, SCX draws on:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2727}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2727}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4545}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Area
\end{minipage} & \begin{minipage}[b]
Role
\end{minipage} & \begin{minipage}[b]
Theorems
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**Probability (concentration)** & Hoeffding/Chernoff bounds for
FPR/FPR control & Thm 1 

**Information theory** & Mutual information, Fano inequality,
Pinsker & Thm 2 

**Statistical decision theory** & Minimax lower bounds, hypothesis
testing & Thm 3, Thm 4' 

**Large deviations theory** & Cramer's theorem, Bahadur-Rao exact
asymptotics & Thm 4' 

**High-dimensional statistics** & k-means consistency, sub-Gaussian
concentration & Thm 5, Prop 6 

**Empirical process theory** & Uniform convergence, covering
numbers & Thm 5 

\end{longtable}

A reviewer might classify it as **``theoretical machine
learning''** or **``statistical learning theory''** -- but that is a
field label, not a mathematical domain.

#### 1.2 The Deeper Answer<!-- label: the-deeper-answer -->

**SCX is fundamentally a problem in structured statistical
decision theory with information constraints.**

The reason goes beyond which tools are used. The SCX theory studies the
following irreducible structure:

> Given: (i) M conditionally independent Bernoulli observations (expert
> errors) per sample, (ii) a latent stratification variable S (state), and
> (iii) a feature representation phi(X) that partially reveals S. Goal:
> Decide whether each sample's label is corrupted, minimizing F1 risk.
> Result: The optimal decision rule is thresholding the mean of the
> Bernoulli observations, with the threshold adaptively shifted by O(1/M)
> to balance FPR and FNR, achieving the exact minimax constant governed by
> Chernoff information.

This is a **decision problem with a nuisance parameter structure
(the state) and an information-constrained side channel (the features)**.
No single subfield of statistics claims this exact structure as its own.

#### 1.3 The ``Home'' Field<!-- label: the-home-field -->

If forced to assign a single home field, the strongest claim is
**Statistical Decision Theory** (Wald paradigm), because:

- 
- 
- 
- 

**Second home**: **Large Deviations Theory**. The transition
from Theorem 1 (Hoeffding rate exp(-2M Delta\^{}2)) to Theorem 4' (exact
Chernoff rate exp(-M kappa) with kappa \textless{} 2 Delta\^{}2) is
precisely the passage from a suboptimal concentration inequality to the
true large-deviations rate. The Bahadur-Rao theorem provides the exact
prefactor. Theorem 4' is, at its heart, a large-deviations refinement of
a decision-theoretic bound.

**Third home**: **Information theory**. The chain of
inequalities in Theorem 2 (mutual information -\textgreater{} Pinsker
-\textgreater{} TV -\textgreater{} risk) is an information-theoretic
argument. The Chernoff information kappa = C(Bern(p0), Bern(p1)) is an
information-theoretic divergence. However, information theory typically
studies communication, not decision-making under latent structure.

**Verdict**: SCX lives at the intersection of **decision
theory, large deviations, and information theory**, with no single field
able to claim it entirely. This is precisely what makes it novel.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{2. What Is the Core Mathematical
Object?}<!-- label: what-is-the-core-mathematical-object -->

#### 2.1 The Surface Answer<!-- label: the-surface-answer-1 -->

The core object is the **consistency score**:

\[C(x) = \frac{1}{M}\sum_{m=1}^M \mathbf{1}\{f_m(x) \neq y\}\]

A sample mean of M conditionally independent Bernoulli indicators,
analyzed as a test statistic for the hypothesis:

\[H_0: label is clean \quadvs.\quad H_1: label is noisy\]

under the F1 risk function.

#### 2.2 The Deeper Object<!-- label: the-deeper-object -->

The core mathematical object is a **triple**:

\[(\mathcal{X}, \mathcal{F}_M, \Pi)\]

where: - \(\mathcal{X}\) is the input space (a measurable space) -
\(\mathcal{F}_M = \{f_1, ..., f_M\}\) is an ensemble of M independent
experts (functions \(\mathcal{X} \to \mathcal{Y}\)) -
\(\Pi: \mathcal{X} \to \mathcal{S}\) is a latent stratification (a
measurable partition)

The theory studies the **detectability** of a contamination in the
label distribution, where:

- 
- 
- 
- 

\item
  The separation \(\Delta_s = p_1(s) - p_0(s)\) determines the
  difficulty
\end{itemize}

\subsubsection{2.3 Is It a Special Case of a Known
Structure?}<!-- label: is-it-a-special-case-of-a-known-structure -->

**Yes, partially:**

1. 
2. 
3. 

\subsubsection{2.4 Can the Entire Theory Be Expressed as a Consequence
of a Deeper
Theorem?}<!-- label: can-the-entire-theory-be-expressed-as-a-consequence-of-a-deeper-theorem -->

**Not a single one, but a chain:**

- 
- 
- 
- 
- 
- 

**Deeper claim**: The entire theory is a **consequence of the
large deviations principle for Bernoulli sums**, applied in a structured
setting. Specifically:

- 
- 
- 
- 

This is the deepest unifying structure: **everything in SCX is
about the tension between what is detectable (via concentration of
expert consensus) and what is not (due to feature weakness or model
equivalence).**

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{3. Linear Algebra
Connections}<!-- label: linear-algebra-connections -->

\subsubsection{3.1 The Consistency Score as a Linear
Functional}<!-- label: the-consistency-score-as-a-linear-functional -->

Let \(\mathbf{e}(x) = (e_1(x), ..., e_M(x))^T \in \{0,1\}^M\) be the
vector of expert error indicators for sample x. Then:

\[C(x) = \frac{1}{M} \mathbf{1}^T \mathbf{e}(x)\]

where \(\mathbf{1} = (1,1,...,1)^T\).

**Interpretation**: \(C(x)\) is the projection of \(\mathbf{e}(x)\)
onto the direction \(\mathbf{1}/\sqrt{M}\) -- the normalized all-ones
vector -- followed by scaling back by \(1/\sqrt{M}\). That is:

\[C(x) = \frac{1}{\sqrt{M}} \cdot \langle \mathbf{e}(x), \frac{\mathbf{1}}{\sqrt{M}} \rangle\]

The kernel of the linear map \(\mathbf{e} \mapsto C\) is the
\((M-1)\)-dimensional subspace:

\[\ker(C) = \{\mathbf{e} \in \mathbb{R}^M : \sum_{m=1}^M e_m = 0\}\]

This is the hyperplane of error patterns with zero net consensus.

**Connection to ANOVA**: This is a **between-expert sum of
squares** decomposition. Let \(\bar{e} = C(x)\). Then the total variation
in expert errors is:

\[\sum_{m=1}^M (e_m - \bar{e})^2 = \|\mathbf{e} - \bar{e}\mathbf{1}\|^2 = \|\mathbf{e}\|^2 - M\bar{e}^2\]

The first term \(\|\mathbf{e}\|^2\) counts how many experts erred; the
second \(M\bar{e}^2\) is the ``explained'' variation captured by the
consensus.

\subsubsection{3.2 k-means State Discovery as Matrix
Factorization}<!-- label: k-means-state-discovery-as-matrix-factorization -->

The k-means objective minimized during state discovery is:

\[W_n = \sum_{s \in \mathcal{S}} \sum_{i: \hat{s}(x_i) = s} \|\phi(x_i) - \hat_s\|^2\]

**Theorem (Ding \& He, 2004)**: This is equivalent to PCA on the
Gram matrix \(K = \Phi\Phi^T\) where \(\Phi\) is the \(N \times d_\phi\)
feature matrix.

Specifically, let \(H = [h_1 | ... | h_K]\) be the \(N \times K\)
cluster membership matrix (with \(h_{ik} = 1/\sqrt{n_k}\) if \(x_i\)
belongs to cluster \(k\)). Then:

\[W_n = tr(K) - tr(H^T K H)\]

and minimizing \(W_n\) is equivalent to maximizing
\(tr(H^T K H)\) -- the projection of \(K\) onto the subspace
spanned by the columns of \(H\). The continuous relaxation of this
(allowing \(H\) to be any \(N \times K\) orthogonal matrix) gives PCA:
\(H\) is the top \(K\) eigenvectors of \(K\).

**Connection to spectral clustering**: The normalized graph
Laplacian of a similarity graph built from \(\phi(x)\) is:

\[L = I - D^{-1/2} W D^{-1/2}\]

where \(W_{ij} = \kappa(\phi(x_i), \phi(x_j))\) (a kernel). The
eigenvectors of \(L\) correspond to the spectral embedding, and k-means
on this embedding produces the state partition. Theorem 5's consistency
result can thus be interpreted as: under strong separation, spectral
clustering on the feature Gram matrix recovers the true state partition
with exponentially decaying error.

\subsubsection{3.3 Gauge Fixing in EGP (Paper IV) as Projection onto a
Quotient}<!-- label: gauge-fixing-in-egp-paper-iv-as-projection-onto-a-quotient -->

In the Expert Governance Protocol (Paper IV), the expert-level
corrections \((c_0, c_Z)\) transform under:

\[c_0 \to c_0 + g, \quad c_Z \to c_Z - g \quad for any  g \in \mathbb{R}\]

**Group structure**: This is an action of the additive group
\((\mathbb{R}, +)\) on \(\mathbb{R}^{Z+1}\).

Let \(\mathbf{c} = (c_0, c_1, ..., c_Z)^T\). The gauge transformation
is \(\mathbf{c} \to \mathbf{c} + g \cdot \mathbf{v}\) where
\(\mathbf{v} = (1, 0, ..., 0, -1)^T\) with +1 at position 0 and -1 at
position Z.

**Gauge condition**: The EGP fixes the gauge by imposing:

\[\sum_{Z} \pi_Z c_Z = 0\]

Let \(\pi = (\pi_0, \pi_1, ..., \pi_Z)^T\). The condition is
\(\pi^T \mathbf{c} = 0\).

**Projection interpretation**: The gauge fixing is the orthogonal
projection onto the subspace \(\{\mathbf{c}: \pi^T \mathbf{c} = 0\}\)
under the weighted inner product
\(\langle \mathbf{c}, \mathbf{c}' \rangle_\pi = \sum_Z \pi_Z c_Z c_Z'\).

The quotient space \(\mathbb{R}^{Z+1} / \mathbb{R}\mathbf{v}\) is
isomorphic to \(\mathbb{R}^Z\), with the isomorphism given by the
projection onto the constraint. This is a principal bundle with
structure group \(\mathbb{R}\) and base
\(\mathbb{R}^{Z+1}/\mathbb{R} \cong \mathbb{R}^Z\).

**Conjectural -- deeper group structure**: If the experts are
organized hierarchically (tree structure), the gauge group could be
\(\mathbb{R}^{edges}\) acting by adjusting corrections along
parent-child edges. The gauge condition would correspond to fixing a
section of this bundle.

\subsubsection{3.4 F1 Bound as Matrix
Inequality}<!-- label: f1-bound-as-matrix-inequality -->

The F1 lower bound in Theorem 1:

\[F1 \geq 1 - \frac{1}\sum_s \rho_s \exp(-2M\Delta_s^2)\]

cannot be naturally expressed as a standard matrix inequality (it is
scalar and exponential). However, the **F1-to-error conversion**
can be:

\[\begin{pmatrix} FPR & FNR \end{pmatrix} \cdot \begin{pmatrix} \frac{1-\eta}{2\eta} & \frac{1}{2} \end{pmatrix}^T \geq 1 - F1\]

This is a linear inequality relating the \((2 \times 1)\) vector of
error rates to the scalar \((1 - F1)\). If we define the
confusion matrix for state s:

\[C_s = \begin{pmatrix} TN_s & FP_s 
 FN_s & TP_s \end{pmatrix}\]

then \(FPR_s = FP_s/(FP_s + TN_s)\),
\(FNR_s = FN_s/(FN_s + TP_s)\), and the F1
bound can be expressed as a set of linear constraints on \(C_s\) after
concentration.

**Conjectural**: The multi-state F1 bound could be written as:

\[F1 \geq 1 - \frac{1} \sum_s \rho_s \cdot tr\left( \begin{pmatrix} 0 & 0 
 0 & 1 \end{pmatrix} \cdot C_s \cdot \exp\left(-2M \begin{pmatrix} (\theta - \mu_s)^2 & 0 
 0 & (1 - C_{bal}\mu_s/(K-1) - \theta)^2 \end{pmatrix}\right) \right)\]

This is not a standard matrix inequality but a trace of a product
involving the confusion matrix and an exponential damping matrix.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. Group Theory Connections<!-- label: group-theory-connections -->

\subsubsection{4.1 The Gauge Group (Paper IV) -- Proven
Connection}<!-- label: the-gauge-group-paper-iv-proven-connection -->

As established in Section 3.3, the EGP gauge transformation is an action
of \((\mathbb{R}, +)\) on the space of expert corrections. This is a
**principal \(\mathbb{R}\)-bundle**.

The gauge condition \(\sum_Z \pi_Z c_Z = 0\) picks a **global
section** of this bundle. The fiber over each equivalence class
\([\mathbf{c}]\) is \(\{g \cdot \mathbf{v} : g \in \mathbb{R}\}\), a
one-dimensional affine subspace.

**Conjectural -- non-Abelian extension**: If the corrections
interact non-trivially (e.g., \(c_0 \to c_0 + g\),
\(c_1 \to c_1 - g/2\), \(c_2 \to c_2 - g/2\)), the gauge group might be
non-Abelian, e.g., \(\mathbb{R}^k\) with a symplectic constraint. This
would map to a more complex Lie group structure, possibly
\(SO(k, 1)\) for hierarchical expert structures.

\subsubsection{4.2 The Symmetric Group S\_M Acting on Experts --
Partially
Proven}<!-- label: the-symmetric-group-s_m-acting-on-experts-partially-proven -->

**Observation**: Under Assumption A2 (conditional independence),
the expert errors \(e_1, ..., e_M\) are exchangeable within each state
if all experts share the same per-state error probability \(\mu_s\)
(i.e., experts are homogeneous within states).

**Proven**: The consistency score \(C(x)\) is symmetric under any
permutation \(\sigma \in S_M\) of the experts:

\[C(x) = \frac{1}{M}\sum_m e_m(x) \xrightarrow \frac{1}{M}\sum_m e_{\sigma(m)}(x) = C(x)\]

Thus \(C(x)\) is the **maximal invariant** of the \(S_M\) action on
the space of expert error vectors \(\{0,1\}^M\).

**Conjectural**: The decomposition of the space of error vectors
under \(S_M\):

- 
- 
- 
- 

\subsubsection{4.3 Automorphism Groups of the State
Partition}<!-- label: automorphism-groups-of-the-state-partition -->

**Definition**: Let \(\Pi = \{s_1, ..., s_K\}\) be a measurable
partition of \(\mathcal{X}\). The **automorphism group**
\(Aut(\Pi)\) is the set of bijections
\(T: \mathcal{X} \to \mathcal{X}\) such that:

1. 
2. 
3. 

If the permutation of states is always the identity (states are not
interchangeable), we have the **pointwise stabilizer**
\(Stab(\Pi) \leq Aut(\Pi)\).

**Conjectural**: For a metric space \(\mathcal{X}\) with a state
structure, the automorphism group of the empirical partition (from
k-means) converges to \(Aut(\Pi)\) as \(n \to \infty\), at a rate
governed by Theorem 5's concentration bound. This would establish a
**consistency of automorphism groups**, analogous to the
consistency of the partition itself.

\subsubsection{4.4 Galois-like Correspondence --
Conjectural}<!-- label: galois-like-correspondence-conjectural -->

**Setup**: Consider the following analogy:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.7500}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.2500}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Galois Theory
\end{minipage} & \begin{minipage}[b]
SCX
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Field \(F\) & Global expert risk vector
\(\mathbf{R} = (R_1, ..., R_M)\) 

Extension field \(E\) & State-conditioned risk matrix \(\{R_m(s)\}\) 

Galois group \(Gal(E/F)\) & Permutations of experts preserving
global ranking 

Subfields of \(E\) & Sub-partitions of the state space 

Fixed field of subgroup \(H\) & Experts indistinguishable under state
grouping 

\end{longtable}

**Conjectural correspondence**: If we coarse-grain the state space
(merge states), we get a coarser partition \(\Pi'\). This corresponds to
a **reduction** in the expert ranking information: some experts
that were distinguished under \(\Pi\) become indistinguishable under
\(\Pi'\). This is analogous to a field extension \(E/F\) where taking
the fixed field under a subgroup \(H \leq Gal(E/F)\) results in a
smaller field.

**Caveat**: This analogy is structural rather than formal. There is
no known way to make the correspondence bijective (the ``fundamental
theorem of Galois theory'' requires specific algebraic conditions not
present in SCX).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{5. Topology and Geometry
Connections}<!-- label: topology-and-geometry-connections -->

\subsubsection{5.1 State Space Decomposition as Topological
Partition}<!-- label: state-space-decomposition-as-topological-partition -->

The state partition \(\Pi = \{s_1, ..., s_K\}\) of \(\mathcal{X}\)
induces the **quotient space** \(\mathcal{X}/\Pi\) with the
quotient topology. The quotient map
\(s: \mathcal{X} \to \mathcal{X}/\Pi\) is continuous (by definition of
the quotient topology) and its fibers are the states.

**Proposition 6** (clustering stability) tests whether this
quotient structure is identifiable from finite data: if the quotient is
``stable'' (high ARI across bootstrap resamples), the quotient topology
is well-defined empirically.

**Theorem 5** shows that under strong separation
(\(\Delta_ > 0\)), the empirical quotient converges to the true
quotient with probability
\(1 - \exp(-c n_ \Delta_^2 / (\sigma^2 d_\phi))\).

\subsubsection{5.2 Theorem 3 as a Fiber Bundle -- Proven
Structure}<!-- label: theorem-3-as-a-fiber-bundle-proven-structure -->

**Model**: Let \(\mathcal{P}\) be the space of data-generating
processes satisfying the SCX assumptions. Let \(\mathcal{Q}\) be the
space of observable joint distributions over \((X, Y, \{f_m\})\).

Theorem 3 constructs two distinct processes
\(P_{noise}, P_{hard} \in \mathcal{P}\) that map to the
same \(Q \in \mathcal{Q}\).

**Fiber bundle interpretation**: The map
\(\pi: \mathcal{P} \to \mathcal{Q}\) (forgetting the internal structure)
is surjective. The fiber \(\pi^{-1}(Q)\) over any \(Q\) contains at
least the two constructed processes. The fiber dimension (in the sense
of parametric models) is at least 1: the parameter \(\eta \in (0, 1)\)
traces a curve within the fiber.

**Conjectural**: The fibers are not just two points but continuous
manifolds. For \(K_{\mathcal{Y}} > 2\), the random-expert construction
creates a family of processes parametrized by
\((\eta, \varepsilon_1, \varepsilon_2, ...)\) all mapping to the same
observable distribution. The fiber is a simplex of dimension at least
\(K_{\mathcal{Y}} - 1\).

More formally, let the set of processes that are indistinguishable from
\(P_{noise}\) be:

\[\mathcal{I}(P_{noise}) = \{P' \in \mathcal{P} : \forall  measurable  A, P_{noise}(A) = P'(A)\}\]

Theorem 3 shows \(|\mathcal{I}(P_{noise})| \geq 2\). The
conjecture is that \(\mathcal{I}(P_{noise})\) is a
**compact convex set** in the space of probability measures, with
extreme points corresponding to different allocations of ``noise
vs.~hardness'' across the ambiguous subset.

\subsubsection{\texorpdfstring{5.3 The Detection Boundary \(\Delta_s\)
as Geodesic
Distance}{5.3 The Detection Boundary \ Delta\_s as Geodesic Distance}}<!-- label: the-detection-boundary-delta_s-as-geodesic-distance -->

On the space of Bernoulli distributions
\(\{Bern(p) : p \in (0,1)\}\), the **Fisher information
metric** is:

\[g(p) = \frac{1}{p(1-p)}\]

The geodesic distance under this metric is:

\[d(p_0, p_1) = \left|\int_{p_0}^{p_1} \frac{dp}{\sqrt{p(1-p)}}\right| = 2\left|\arcsin\sqrt{p_1} - \arcsin\sqrt{p_0}\right|\]

This is the **Bhattacharyya angle** (or more precisely, twice the
Bhattacharyya angle).

The **Chernoff information**
\(\kappa = C(Bern(p_0), Bern(p_1))\) satisfies:

\[\kappa = -\log \inf_{t \in (0,1)} \int p_0^t p_1^{1-t} d\mu = -\log\left(p_0^{\theta^*} p_1^{1-\theta^*} + (1-p_0)^{\theta^*} (1-p_1)^{1-\theta^*}\right)\]

**Relationship between \(\kappa\) and the geodesic distance**:

\[\kappa \leq -\log\left(1 - \frac{H^2}{2}\right) \leq \frac{H^2}{2} \leq 1 - \sqrt{1 - H^2} \leq \frac{d(p_0, p_1)^2}{2}\]

where
\(H^2 = (\sqrt{p_0} - \sqrt{p_1})^2 + (\sqrt{1-p_0} - \sqrt{1-p_1})^2\)
is the squared Hellinger distance. The Chernoff information is
**bounded above by the geodesic distance squared** along the
statistical manifold.

**Connection to \(\Delta_s\)**: For small gaps, by Taylor
expansion:

\[\kappa = \frac{(p_1 - p_0)^2}{2p_0(1-p_0)} + O((p_1-p_0)^3)\]

Since \(\Delta_s = \min(\theta - p_0, p_1 - \theta)\) and the optimal
\(\theta = (p_0 + p_1)/2\) for symmetric thresholds, we have
\(2\Delta_s^2 = (p_1 - p_0)^2/2\). Thus:

\[\kappa \approx \frac{2\Delta_s^2}{p_0(1-p_0)}\]

For small \(p_0\), \(p_0(1-p_0) \approx p_0\), so
\(\kappa \gg 2\Delta_s^2\) -- the Chernoff rate is significantly faster
than the Hoeffding bound. This is exactly the numerical finding in
Section 4.3 of the unified document (ratio 2.46-3.41).

\subsubsection{5.4 Information Geometry of the Multi-State
Problem}<!-- label: information-geometry-of-the-multi-state-problem -->

**Conjectural**: The full SCX model (multi-state, multi-expert)
lives on a **product of statistical manifolds**:

\[\mathcal{M} = \times_{s \in \mathcal{S}} \mathcal{M}_s\]

where each \(\mathcal{M}_s\) is a 2-dimensional manifold parametrized by
\((p_0(s), p_1(s))\) with the Fisher metric. The global F1 risk is a
function on this product manifold.

The minimax optimal threshold \(\theta^\dagger\) corresponds to the
point on the product manifold that minimizes the F1 risk. The \(O(1/M)\)
threshold shift corresponds to a **geodesic deviation** from the
symmetric Chernoff point \(\theta^*\) toward the Bayes-optimal decision
boundary.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{6. Category Theory
Connections}<!-- label: category-theory-connections -->

\subsubsection{6.1 State-Conditioned Expertise as a Functor --
Conjectural}<!-- label: state-conditioned-expertise-as-a-functor-conjectural -->

Define two categories:

- 
- 

**Training functor** \(T: DataCat \to ExpertCat\):
Given a dataset \(D \sim \mathcal{D}^n\), \(T(D) = (f_1, ..., f_M)\)
where each \(f_m\) is trained on a disjoint subset \(D_m \subset D\)
(Assumption A1).

**State-conditioned restriction functor**
\(R_s: ExpertCat \to ExpertCat\):
\[R_s(\mathcal{F})(x) = \mathcal{F}(x) \cdot \mathbf{1}\{x \in s\}\]

The SCX framework studies the interplay between \(T\) and
\(\{R_s\}_{s \in \mathcal{S}}\).

**Conjectural**: The state-conditioned expert risk satisfies a
**functoriality** property:

If \(h: \mathcal{X}_1 \to \mathcal{X}_2\) is a morphism in DataCat that
preserves the state partition (\(h(s_i) = s_i\) for all \(i\)), then:

\[R_m(s)  computed on  \mathcal{X}_1 = R_m(s)  computed on  \mathcal{X}_2\]

i.e., the risk is invariant under state-preserving transformations. This
would make \(R_m(s)\) a **functor from the category of
state-marked probability spaces to the category of real numbers**.

\subsubsection{6.2 Two-Layer Architecture as a Natural
Transformation}<!-- label: two-layer-architecture-as-a-natural-transformation -->

The SCX two-layer architecture consists of:

- 
- 

Consider the category **Prob** of probability spaces. Let
\(F: Prob \to Prob\) be the ``feature extraction''
functor:

\[F(\mathcal{X}, P_X) = (\mathbb{R}^{d_\phi}, P_\phi)\]

where \(P_\phi = P_X \circ \phi^{-1}\). Let
\(G: Prob \to Set\) be the ``state assignment'' functor:

\[G(\mathcal{X}, P_X) = \mathcal{X}/\Pi\]

(the set of states under the true partition).

**Conjectural**: The two-layer architecture is a **natural
transformation** \(\eta: G \Rightarrow G \circ F\) if the following
diagram commutes for all morphisms \(h\) in Prob:

\begin{verbatim}
G(X) --η_X--> G(F(X))
 |             |
G(h)          G(F(h))
 v             v
G(Y) --η_Y--> G(F(Y))
\end{verbatim}

This would mean that the state assignment via features is consistent
under transformations of the input space. This is not formally provable
without additional assumptions, but it captures the intuition that the
two-layer architecture should be ``representation-agnostic'' -- the
state assignment should depend only on the features, not on the
representation of the input space.

\subsubsection{6.3 Curation-Exploration Tradeoff as an Adjunction --
Speculative}<!-- label: curation-exploration-tradeoff-as-an-adjunction-speculative -->

The SCX workflow cycle is:

1. 
2. 

**Conjectural**: \((C, E)\) form an **adjunction**
\(C \dashv E\) in an appropriate 2-category of datasets:

The unit \(\eta: Id_{Data} \Rightarrow E \circ C\)
reflects that curating a dataset and then exploring adds back some
samples (not the same ones).

The counit
\(\varepsilon: C \circ E \Rightarrow Id_{CleanData}\)
reflects that exploring and then curating returns a superset of the
original clean data.

**Triangle identities**:

\[C \xrightarrow{C\eta} CEC \xrightarrow{\varepsilon C} C = id_C\]
\[E \xrightarrow{\eta E} ECE \xrightarrow{E\varepsilon} E = id_E\]

The first identity says: curating, then exploring+curating again, should
not change the curation result. The second says: exploring, then
curating+exploring again, should not change the exploration result.

**Speculative**: The failure of these identities (due to imperfect
noise detection) measures the ``distance'' from a true adjunction, which
is precisely the error probability \(\exp(-2M\Delta^2)\) in Theorem 1.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{7. Analogous Mathematical
Structures}<!-- label: analogous-mathematical-structures -->

\subsubsection{7.1 Arrow's Impossibility Theorem -- PROVEN ANALOGY,
REMOVED}<!-- label: arrows-impossibility-theorem-proven-analogy-removed -->

This analogy was explored and **removed** from the theory files.
The mapping was:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5833}}
  >{\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.4167}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Arrow
\end{minipage} & \begin{minipage}[b]
SCX
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Voters i & States s 

Candidates a & Experts f\_m 

Social preference ordering & Global ranking R\_m 

Pareto optimality & State-level ranking consistency 

Independence of irrelevant alternatives & Independence of new experts 

\end{longtable}

**Why it was removed**: The conditions don't match. Arrow's theorem
requires all four conditions simultaneously to produce a contradiction.
SCX's Proposition 1 only requires the existence of a ranking crossing --
a weaker condition. The Arrow analogy inflated the mathematical depth of
the SCX result.

**Verdict**: False analogy. Notational only.

\subsubsection{7.2 No Free Lunch Theorem -- GENUINE
ANALOGY}<!-- label: no-free-lunch-theorem-genuine-analogy -->

The No Free Lunch (NFL) theorem for optimization states: for any
algorithm A, the average performance over all possible objective
functions is the same as any other algorithm (including random search).

**Parallel to SCX Theorem 2**:

- 
- 

Both are **worst-case impossibility results** that establish
fundamental limits. However, SCX's result is quantitatively graded (the
bound scales with \(\sqrt\)), whereas NFL is binary (all
algorithms are equivalent).

**Key difference**: NFL averages uniformly over all problems; SCX
bounds the worst case over a restricted class (features with bounded
mutual information). The SCX bound is tighter because the class is
smaller.

\subsubsection{7.3 Cramer-Rao Bound -- GENUINE ANALOGY (already noted in
theory)}<!-- label: cramer-rao-bound-genuine-analogy-already-noted-in-theory -->

The Cramer-Rao lower bound states: for any unbiased estimator
\(\hat\) of a parameter \(\theta\),

\[Var(\hat) \geq \frac{1}{I(\theta)}\]

where \(I(\theta)\) is the Fisher information.

**Parallel to SCX Theorem 4'**:

- 
- 

Both are **information-theoretic lower bounds** that take the form
``no method can surpass this fundamental limit.'' Both involve an
**information measure** (Fisher vs.~Chernoff) that captures the
difficulty of the underlying statistical problem.

**However**, there are important differences:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2500}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3438}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4062}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Aspect
\end{minipage} & \begin{minipage}[b]
Cramer-Rao
\end{minipage} & \begin{minipage}[b]
SCX Thm 4'
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Risk & Variance of estimator & \(1 - F1\) (misclassification
rate) 

Information & Fisher
\(I(\theta) = \mathbb{E}[(\partial_\theta \log p)^2]\) & Chernoff
\(\kappa = C(P_0, P_1)\) 

Asymptotic form & \(1/(n I(\theta))\) &
\(C_ e^{-M\kappa} / (\eta \sqrt{M})\) 

Achievability & MLE achieves CR bound under regularity & SCX adaptive
threshold achieves \(\kappa\) constant 

Regime & \(n \to \infty\) with fixed \(p\) & \(M \to \infty\) with fixed
\(p_0, p_1\) 

\end{longtable}

The C-R bound is polynomial in \(n\), while SCX's bound is exponential
in \(M\). This is because C-R is about **estimation** (smooth
parameter) while SCX is about **testing** (discrete hypothesis).

\subsubsection{7.4 Gelfand-Naimark Theorem (C*-algebras) -- SPECULATIVE
ANALOGY}<!-- label: gelfand-naimark-theorem-c-algebras-speculative-analogy -->

**Gelfand-Naimark**: Every commutative C*-algebra is
isometrically *-isomorphic to \(C_0(X)\) for some locally compact
Hausdorff space \(X\). This establishes a duality between commutative
C*-algebras and topological spaces.

**Conjectural analogy in SCX**:

- 
- 
- 
- 

**Is this deep or superficial?** It is unlikely to be deep. The
Gelfand-Naimark duality is a tool for non-commutative geometry, and the
SCX setting is purely classical (commutative). The projection
\(\mathbf{1}\{C > \theta\}\) is a spectral projection of a classical
random variable, not a quantum observable. The analogy is
**notational** at best.

**Verdict**: Weak analogy. The C*-algebra framework adds no new
insight.

\subsubsection{7.5 Shannon's Source Coding Theorem -- NUMERIC
ANALOGY}<!-- label: shannons-source-coding-theorem-numeric-analogy -->

Shannon's theorem: For a source \(X\) with rate-distortion function
\(R(D)\), the optimal compression at distortion \(D\) requires rate
\(R(D) = I(X; \hat{X})\), and there exist codes that achieve \(R(D)\) as
block length \(\to \infty\).

**Parallel to SCX Thm 4'**:

- 
- 

Both give **exact asymptotic constants** in terms of an
information-theoretic divergence. Both involve a **coding/decision
scheme** that achieves the bound asymptotically (random codes for
Shannon; thresholded consensus for SCX).

However, the mathematical structures differ:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3636}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4091}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2273}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Aspect
\end{minipage} & \begin{minipage}[b]
Shannon
\end{minipage} & \begin{minipage}[b]
SCX
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Fundamental quantity & Rate-distortion function \(R(D)\) & Chernoff
information \(\kappa\) 

Achievability proof & Random coding (existence) & Adaptive threshold
(explicit construction) 

Optimality proof & Converse: \(R(D) \geq I(X;\hat{X})\) & Minimax:
\(C_/\eta\) lower bound via Bahadur-Rao 

Asymptotic form & \(R(D) = I + O(1/\sqrt{n})\) &
\(1 - F1 = \frac{C_}{\eta\sqrt{M}} e^{-M\kappa} + o(1/\sqrt{M})\) 

\end{longtable}

\subsubsection{7.6 The Ising Model / Statistical Physics -- CONJECTURAL
ANALOGY}<!-- label: the-ising-model-statistical-physics-conjectural-analogy -->

**Conjectural**: The SCX consensus score \(C(x)\) behaves like a
**magnetization** in a Curie-Weiss model with M spins.

- 
- 
- 
- 

The SCX decision boundary \(C = \theta\) corresponds to a
**magnetization threshold**: samples with magnetization above
threshold are classified as noise.

The **large deviations** of the magnetization (Theorem 4')
correspond to the **free energy** of the Curie-Weiss model, where
the rate function \(I(\theta) = KL(\theta\|p)\) plays the role of
the large-deviations rate for the empirical mean.

**Possible extension**: If experts have correlations (breaking A2),
the spin system becomes an **Ising model** with pairwise
interactions. The detection problem becomes harder, and the optimal test
may involve the full spin configuration, not just the magnetization.

**Verdict**: Aesthetic analogy. The Curie-Weiss mapping is exact
for independent experts but adds no technical simplification. It becomes
potentially useful if A2 is relaxed (correlated experts).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{8. Is SCX a Special Case of Something
Bigger?}<!-- label: is-scx-a-special-case-of-something-bigger -->

\subsubsection{\texorpdfstring{8.1 The Exponential Bound
\(\exp(-2M\Delta^2)\) as a Special Case of
Hoeffding}{8.1 The Exponential Bound \ exp(-2M\ Delta\^{}2) as a Special Case of Hoeffding}}<!-- label: the-exponential-bound-exp-2mdelta2-as-a-special-case-of-hoeffding -->

**Proven**: The bound \(\exp(-2M\Delta^2)\) is a special case of
**Hoeffding's inequality** for sums of bounded independent random
variables. With \(e_m \in [0,1]\),
\(\mathbb{P}(|\bar{e} - \mathbb{E}[\bar{e}]| \geq t) \leq 2\exp(-2Mt^2)\).

The transition from Theorem 1 (Hoeffding rate) to Theorem 4' (Chernoff
rate) is the transition from Hoeffding's inequality to **Cramer's
theorem** (the full large deviations principle). This is a general
phenomenon:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2000}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3556}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4444}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Setting
\end{minipage} & \begin{minipage}[b]
Hoeffding bound
\end{minipage} & \begin{minipage}[b]
Exact LDP (Cramer)
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Bernoulli & \(\exp(-2Mt^2)\) &
\(\exp(-M \cdot KL(\theta\|p))\) 

Bounded r.v. & \(\exp(-2Mt^2 / (b-a)^2)\) & \(\exp(-M \cdot I(\theta))\)
where \(I\) is the rate function 

Sub-Gaussian & \(\exp(-Mt^2 / 2\sigma^2)\) & Sub-Gaussian rate
function 

\end{longtable}

**Deeper structure**: The exponential bound \(\exp(-2M\Delta^2)\)
is a **coarse estimate** for the true large-deviations rate. The
**Pinsker inequality** \(KL(\theta\|p) \geq 2(\theta-p)^2\)
gives the relationship: the Hoeffding exponent is always weaker than the
true KL exponent.

Thus Theorem 1 is a **corollary of Hoeffding's inequality plus a
union bound**, and Theorem 4' is the **sharpening** obtained by
replacing Hoeffding with Cramer + Bahadur-Rao.

\subsubsection{8.2 Theorem 3 as a Special Case of General
Unidentifiability}<!-- label: theorem-3-as-a-special-case-of-general-unidentifiability -->

**Proven**: Theorem 3 is a special case of the
**non-identifiability of mixture models**.

Consider a two-component mixture model:

\[P(y | x) = (1-\eta)P_{clean}(y | x) + \eta P_{noise}(y | x)\]

The noise model \(P_{noise}(y | x)\) is itself a mixture over the
observed label \(\tilde{y}\) given the true label \(y^*\):

\[P_{noise}(y | x) = \frac{1}{K-1}\sum_{c \neq y^*} P(y = c | y^*  flipped to  c)\]

The hardness-world is obtained by swapping the interpretation: instead
of \(y^*\) being deterministic and the label random, we make \(y^*\)
random and the label deterministic. This is a
**reparameterization** of the mixture model.

**General principle**: Any time a latent variable model has a
**symmetry** (here: swapping the roles of noise and ambiguity), the
parameters are unidentifiable. This is closely related to:

- 
- 
- 

**Theorem 3 as a concrete instance**: The specific construction
produces a **minimal** unidentifiability: exactly two
data-generating processes map to the same observable distribution. This
is the ``atomic'' unidentifiability from which larger families can be
built by convex combination.

\subsubsection{8.3 Theorem 4' as a Special Case of Exact Asymptotics
Theory}<!-- label: theorem-4-as-a-special-case-of-exact-asymptotics-theory -->

**Proven**: Theorem 4'\,'s exact constant result is a special case
of **second-order asymptotics for hypothesis testing** (also called
``refined large deviations'' or ``moderate deviations'').

Specifically:

- 
- 
- 

**General family**: Theorem 4' belongs to the class of results that
give **exact error constants for testing simple vs.~simple
hypotheses** under a specific loss function. The key elements are:

1. 
2. 
3. 
4. 
5. 

**Is it a special case of a known meta-theorem?** Not exactly.
While each step is standard, the **combination** of F1 risk with
Bernoulli tests and adaptive thresholding is engineered. There is no
general ``exact minimax theory for F1 under mixture models'' that
Theorem 4' is a special case of.

**Conjectural**: The result could be unified under a
**general theory of exact asymptotic minimax optimality for
composite hypothesis testing under weighted error rates**, where:

- 
- 
- 

Under this general theory, Theorem 4' would be the **Bernoulli
special case** with \(p_0 = \mu, p_1 = 1 - C_{bal}\mu/(K-1)\).

\subsubsection{8.4 Summary: What Larger Principles Does SCX
Exemplify?}<!-- label: summary-what-larger-principles-does-scx-exemplify -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2647}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.5000}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2353}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Theorem
\end{minipage} & \begin{minipage}[b]
Larger Principle
\end{minipage} & \begin{minipage}[b]
Status
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Thm 1 & Concentration of U-statistics + union bound & Proven special
case 

Thm 2 & Data processing + Pinsker inequality & Proven special case 

Thm 3 & Mixture model non-identifiability & Proven special case 

Thm 4' & Second-order asymptotics for hypothesis testing & Proven
special case (each step), but the combination is novel 

Thm 5 & k-means consistency under strong separation & Proven special
case 

Prop 6 & Clustering stability as feature informativeness & Proven
heuristic 

\end{longtable}

**The novel synthesis**: What makes SCX more than the sum of its
parts is the **unified treatment** of all these regimes in a single
theoretical framework, connected by a coherent set of assumptions
(A1-A6). The theory shows how:

- 
- 
- 
- 
- 

No existing theory captures this full chain.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{9. What Is ``SCX''
Mathematically?}<!-- label: what-is-scx-mathematically -->

\subsubsection{9.1 The One-Sentence
Definition}<!-- label: the-one-sentence-definition -->

**SCX is the minimax-optimal statistical decision theory of
detecting label contamination in a multi-expert system, where the
experts' conditional error probabilities are modulated by a latent state
variable, the state is discovered via spectral clustering in a feature
space with information-constrained fidelity, and the detection threshold
is adaptively shifted by O(1/M) to achieve the exact Chernoff constant
under F1 risk.**

\subsubsection{9.2 More Precisely, in Pure
Mathematics}<!-- label: more-precisely-in-pure-mathematics -->

Let us define the components formally:

- 
- 
- 
- 
- 

Under A1-A6: - \(f_m \perp f_{m'} \mid X\) (experts conditionally
independent given input) - \(\mathbb{P}(Z=1) = \eta\) (noise rate) -
\(\mathbb{P}(Y = c \mid Z=1, X) = 1/(K-1)\) for \(c \neq Y^*\) (uniform
noise) -
\(\mathbb{E}[\mathbf{1}\{f_m(X) \neq Y\} \mid Z=0, X \in s] \leq \mu_s\)
(state-bounded clean error) -
\(\mathbb{E}[\mathbf{1}\{f_m(X) \neq Y\} \mid Z=1, X \in s] \geq 1 - C_{bal}\mu_s/(K-1)\)
(state-bounded noise error)

**Definition**: The SCX noise detector is the function:

\[h_{SCX}(x) = \mathbf{1}\left\{\frac{1}{M}\sum_{m=1}^M \mathbf{1}\{f_m(x) \neq y\} > \theta^\dagger\right\}\]

where
\(\theta^\dagger = \theta^* + \frac{1}{M}\frac{\log((1-\eta)/\eta)}{D^*} + O(1/M^2)\),
\(\theta^* = \arg\min_\theta \{KL(\theta\|\mu_s) = KL(\theta\|1 - C_{bal}\mu_s/(K-1))\}\).

**SCX theory**: A chain of theorems establishing:

\[\lim_{M\to\infty} e^{M\kappa}\sqrt{2\pi M}(1 - F1(h_{SCX})) = \frac{C_}\]

where
\(\kappa = C(Bern(\mu_s), Bern(1 - C_{bal}\mu_s/(K-1)))\)
and \(C_\) is the unique minimax constant. This holds globally
across states (Thm 4') and degrades gracefully when features are weakly
informative (Thm 2,
\(F1 \leq F1_{base} + O(\sqrt{I(\phi;S)})\)), while
an unidentifiability gap prohibits perfect detection (Thm 3).

\subsubsection{9.3 Alternative
Characterizations}<!-- label: alternative-characterizations -->

**As a statistical decision theory**: SCX is the characterization
of the minimax-optimal Bayes decision boundary between two Bernoulli
populations with state-dependent shifts, under a ratio-of-successes risk
function, with the state discovered from side information.

**As an information theory**: SCX is the study of the Chernoff
information between two product-Bernoulli distributions with a latent
mixing parameter, and the data-processing loss incurred when the mixing
parameter must be estimated from information-constrained features.

**As a large deviations theory**: SCX is the refinement of Cramer's
theorem for the sample mean of Bernoulli variables from exponential-rate
asymptotics to exact constant asymptotics, applied to a structured
decision problem with an adaptive threshold correction.

**As an algebra**: SCX is the study of the \(S_M\)-invariant
function \(C(x) = \frac{1}{M}\sum e_m\) as the maximal invariant of the
expert ensemble, with the state partition providing a decomposition of
\(\mathcal{X}\) into regions where \(C(x)\) has approximately constant
distribution under both hypotheses.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 10. Summary Table<!-- label: summary-table -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1333}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2167}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3167}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Domain
\end{minipage} & \begin{minipage}[b]
Connection Strength
\end{minipage} & \begin{minipage}[b]
Key Insight
\end{minipage} & \begin{minipage}[b]
Theorems Involved
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**Statistical decision theory** & PROVEN (core) & Minimax optimal
testing under F1 risk; latent state structure & All 6 

**Large deviations** & PROVEN (core) & Chernoff rate is exact;
Bahadur-Rao gives constants & Thm 1, Thm 4' 

**Information theory** & PROVEN (core) & Mutual information bounds
SCX's advantage; Chernoff info & Thm 2, Thm 4' 

**Concentration inequalities** & PROVEN (used) & Hoeffding/Chernoff
bounds for FPR/FPR & Thm 1 

**U-statistics** & PROVEN (weak) & C(x) is a degree-1 U-statistic &
Thm 1 

**Linear algebra (ANOVA)** & PROVEN (weak) & C(x) = (1/M)1\^{}T
e(x); projection onto all-ones direction & Thm 1 

**Spectral clustering (PCA)** & PROVEN (medium) & k-means = PCA on
Gram matrix; state discovery via eigenvectors & Thm 5, Prop 6 

**Gauge theory (R action)** & PROVEN (medium) & EGP gauge fixing as
principal R-bundle with section & Paper IV 

**Permutation group S\_M** & PROVEN (weak) & C(x) is
S\_M-invariant; maximal invariant of expert ensemble & Thm 1 

**Automorphism groups** & Conjectural & Convergence of empirical
automorphism group of partition & Thm 5 

**Galois correspondence** & Conjectural & Coarse-graining of states
↔ subgroups of expert symmetries & --- 

**Fiber bundles** & PROVEN (medium) & Thm 3: unidentifiable
processes as fibers over observable & Thm 3 

**Information geometry** & PROVEN (medium) & Fisher metric on
Bern(p); Chernoff \textless{} geodesic distance & Thm 4' 

**Statistical physics (Ising)** & Conjectural & Magnetization
analogy for consensus; Curie-Weiss for independent & Thm 1 

**Category theory (functors)** & Conjectural & Training as functor;
state-conditioning as natural & --- 

**Adjunctions** & Speculative & Curation-Exploration as C ⊣ E &
--- 

**Arrow's theorem** & FALSE (removed) & Conditions don't match;
misleading analogy & --- 

**No Free Lunch** & GENUINE analogy & Worst-case bound over feature
representations & Thm 2 

**Cramer-Rao bound** & GENUINE analogy & Information-theoretic
lower bound on estimation & Thm 4' 

**Gelfand-Naimark** & Weak analogy & Spectral projection of
consensus operator & Thm 1 

**Shannon source coding** & GENUINE analogy & Exact asymptotic
constant; achievability + converse & Thm 4' 

**BBP phase transition** & PROVEN (medium) & Spectral transition
for weak/strong feature regime & Thm 2, Thm 5 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### References<!-- label: references -->

1. 
2. 
3. 
4. 
5. 
6. 
7. 
8. 
9. 
10. 
11. 
12. 
13. 
14. 
15. 
16. 
17. 
18. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*End of deep mathematical connections analysis.*