\section{SCX Self-Evolution: Symbol System and Problem
Setup}<!-- label: scx-self-evolution-symbol-system-and-problem-setup -->

> **Version**: 2026-06-28 |{} **Status**: Foundational
> |{} **Audit**: Pre-verification **Purpose**: Define
> notation, problem structure, and formal setup for the SCX self-evolution
> framework. **Relationship to existing theory**: Extends the
> notation of THEOREMS\_UNIFIED.md (Sections 0.1-0.2) into the
> self-evolution regime.

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
11. 
12. 
13. 
14. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. Introduction and Scope<!-- label: introduction-and-scope -->

The SCX self-evolution framework extends the static SCX noise detection
pipeline into a closed-loop learning system. In the static setting
(Theorem 1-6 of the core theory), the gatekeeper function \(S\) is fixed
after initial training, and the expert models \(\{f_m\}_{m=1}^M\) remain
static. In the self-evolution setting, the gatekeeper iteratively
refines its scoring function, accumulates a memory bank, and trains a
student model (NEP) that provides delayed feedback.

The core iteration is:

\[judge \;\to\; store \;\to\; update SCX \;\to\; re-judge \;\to\; re-update \;\to\; ...\]

This document formalizes the objects, spaces, and assumptions needed to
analyze this dynamics. Subsequent documents study the dynamical system
properties (Document 02) and the online learning regret (Document 03).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{2. Preliminary: Inherited Notation from Core SCX
Theory}<!-- label: preliminary-inherited-notation-from-core-scx-theory -->

We inherit the following from THEOREMS\_UNIFIED.md. Any symbol not
redefined below retains its meaning from the core theory.

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2857}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3214}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3929}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Symbol
\end{minipage} & \begin{minipage}[b]
Meaning
\end{minipage} & \begin{minipage}[b]
Reference
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(\mathcal{X}\) & Input space & Thm 1-6 

\(\mathcal{Y}\) & Label space, \(|\mathcal{Y}| = K_{\mathcal{Y}}\) & Thm
1, 3 

\(\mathcal{S}\) & State space (index set),
\(|\mathcal{S}| = K_{\mathcal{S}}\) & Thm 1-6 

\(s(x): \mathcal{X} \to \mathcal{S}\) & True state assignment & Thm
1-6 

\(f^*: \mathcal{X} \to \mathcal{Y}\) & True oracle (unobserved) & Thm 1,
3 

\(\{f_m\}_{m=1}^M\) & Expert models, \(M\) experts & Thm 1-6 

\(\ell: \mathcal{Y} \times \mathcal{Y} \to [0,B]\) & Bounded loss,
\(B < \infty\) & Thm 1 

\(\tau > 0\) & Expert error threshold & Thm 1 

\(e_m(x,y) = \mathbf{1}\{\ell(f_m(x), y) > \tau\}\) & Expert error
indicator & Thm 1 

\(C(x) = \frac{1}{M}\sum_{m=1}^M e_m(x,y)\) & Consensus score & Thm 1 

\(\eta\) & Global noise rate & Thm 1-4' 

\(\rho_s = \mathbb{P}(X \in s)\) & State probability & Thm 1 

\(\mu_s\) & State-\(s\) clean error upper bound & Thm 1 

\(R_m(s)\) & State-conditioned expert risk & Tech report 

\(SCX_m(s)\) & Reliability score
\(\mathbb{P}(\ell(f_m(x), y) < \tau \mid x \in s)\) & Tech report 

\(\hat{s}(x)\) & Estimated state assignment & Thm 2, 5 

\(\phi: \mathcal{X} \to \mathbb{R}^{d_\phi}\) & Feature representation &
Thm 2, 5 

\(\theta\) (detection) & Detection threshold (static setting) & Thm 1,
4' 

\end{longtable}

> **Notation warning (B3 fix --- cross-reference):** \(\mathcal{S}\)
> (calligraphic) denotes the **state space** (a finite index set).
> \(S_t\) (italic with time subscript \(t\)) denotes the
> **gatekeeper scoring function**
> \(S_t: \mathcal{X} \times \mathcal{Y} \to [0,1]\) at time \(t\), defined
> in §6. These are entirely distinct objects. In the core SCX theory
> (Theorems 1-3), \(S\) refers to the state random variable; in
> self-evolution docs, \(S_t\) refers to the evolving gatekeeper.
> **Context disambiguates**: \(\mathcal{S}\) = state space; \(S_t\) =
> gatekeeper at time \(t\).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{3. New Objects for
Self-Evolution}<!-- label: new-objects-for-self-evolution -->

The self-evolution framework introduces the following new objects:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3077}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2308}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4615}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Symbol
\end{minipage} & \begin{minipage}[b]
Name
\end{minipage} & \begin{minipage}[b]
Definition
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(\mathcal{X}\) & Structure space & All possible SCX configurations
(Section 4) 

\(S_t: \mathcal{X} \times \mathcal{Y} \to [0,1]\) & Gatekeeper scoring
function at time \(t\) & Section 6 

\(M_t\) & Memory bank at time \(t\) & Section 7 

\(f_{\theta_t}: \mathcal{X} \to \mathcal{Y}\) & NEP student with
parameters \(\theta_t\) & Section 8 

\(\Phi\) & Update operator & Section 9 

\(L_{gate}\) & Gatekeeper loss & Section 10 

\(L_{nep}\) & NEP student loss & Section 10 

\end{longtable}

**Time index convention**: \(t = 0, 1, 2, ...\) indexes discrete
evolution rounds. \(t=0\) is the initialization round (before any
self-evolution). Time advances forward as the loop executes.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{\texorpdfstring{4. Structure Space
\(\mathcal{X}\)}{4. Structure Space \ mathcal\{X\}}}<!-- label: structure-space-mathcalx -->

#### 4.1 Definition<!-- label: definition -->

Let \(\mathcal{X}\) denote the **structure space**: the set of all
feasible SCX configurations over the input space \(\mathcal{X}_0\),
label space \(\mathcal{Y}\), and state space \(\mathcal{S}\).

**Definition 1 (Structure Space).** A configuration
\(x \in \mathcal{X}\) is a tuple:

\[x = \bigl( \mathcal{X}_0, \mathcal{Y}, \mathcal{S}, s(\cdot), \{f_m\}_{m=1}^M, \phi(\cdot), \hat{s}(\cdot), \ell, \tau \bigr)\]

where each component satisfies the standard SCX definitions from
THEOREMS\_UNIFIED.md Section 0.1.

**Remarks:** - The structure space is a product of function spaces:
\(\mathcal{X} = \mathcal{P}(\mathcal{X}_0) \times \mathcal{P}(\mathcal{Y}) \times ...\)
(abusing notation for the Cartesian product of the component spaces). -
In practice, we never enumerate \(\mathcal{X}\) explicitly; we reason
about the **support** of the data distribution's structural
parameters. - The key structural variable for the self-evolution
analysis is the pair \((\mathcal{S}, s(\cdot))\) (the state partition)
because errors in state discovery propagate to all downstream estimates.

\subsubsection{4.2 Metric on Structure
Space}<!-- label: metric-on-structure-space -->

For theoretical analysis, we endow \(\mathcal{X}\) with a metric induced
by the total variation distance between the implied consensus score
distributions.

**Definition 2 (Structure Metric).** For two configurations
\(x, x' \in \mathcal{X}\), define:

\[d_{\mathcal{X}}(x, x') = \sup_{A \subseteq \mathcal{X}_0} \bigl| \mathbb{P}_{X \sim P_x}(C(X) \in A) - \mathbb{P}_{X \sim P_{x'}}(C(X) \in A) \bigr|\]

where \(P_x\) is the implied distribution of \((X, Y, \{f_m\})\) under
configuration \(x\).

This metric captures the notion that two structures are ``close'' if
they induce similar consensus score distributions. It is relevant for
analyzing how small changes in the structure (e.g., updated state
estimates) affect gatekeeper decisions.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 5. Evolution State Space<!-- label: evolution-state-space -->

#### 5.1 Definition<!-- label: definition-1 -->

The **evolution state** at time \(t\) is the triple representing
the complete system state:

\[z_t = (S_t, M_t, \theta_t) \in \mathcal{Z}\]

where \(\mathcal{Z} = \mathcal{F} \times \mathcal{M} \times \Theta\) is
the evolution state space, with:

- 
- 
- 

\subsubsection{\texorpdfstring{5.2 Topology on
\(\mathcal{F}\)}{5.2 Topology on \ mathcal\{F\}}}<!-- label: topology-on-mathcalf -->

We equip \(\mathcal{F}\) with the topology of pointwise convergence,
equivalently the product topology. For analysis, the relevant metric is:

**Definition 3 (Gatekeeper Metric).** For
\(S, S' \in \mathcal{F}\):

\[d_{\mathcal{F}}(S, S') = \mathbb{E}_{(x,y) \sim \mathcal{D}}\bigl[ |S(x,y) - S'(x,y)| \bigr]\]

where \(\mathcal{D}\) is the data distribution.

This metric captures the average disagreement between two scoring
functions. Under standard regularity conditions (e.g., \(S\) is
Lipschitz in its parameters), \(d_{\mathcal{F}}\) is equivalent to the
\(L^1(\mathcal{D})\) distance.

\subsubsection{\texorpdfstring{5.3 Topology on
\(\mathcal{M}\)}{5.3 Topology on \ mathcal\{M\}}}<!-- label: topology-on-mathcalm -->

The memory bank \(M_t\) is a finite multiset. We equip \(\mathcal{M}\)
with the metric induced by the Hausdorff distance on the
feature-label-confidence space:

**Definition 4 (Memory Metric).** For \(M, M' \in \mathcal{M}\)
with \(|M| = N\), \(|M'| = N'\), suppose \(N = N'\) (balanced case).
Define:

\[d_{\mathcal{M}}(M, M') = \frac{1}{N} \sum_{i=1}^N \bigl\| \psi(x_i, y_i, v_i, c_i) - \psi(x'_i, y'_i, v'_i, c'_i) \bigr\|_2\]

where \(\psi\) is an embedding of the memory entry into
\(\mathbb{R}^{d_\psi}\). For unequal sizes, extend using optimal
transport (Earth Mover's Distance).

**Simplification for analysis**: In practice, we often reason about
the **empirical distribution** \(\hat{P}_t\) induced by \(M_t\)
rather than the set itself, allowing standard measure-theoretic tools.

#### 5.4 Product Space Topology<!-- label: product-space-topology -->

The evolution state space
\(\mathcal{Z} = \mathcal{F} \times \mathcal{M} \times \Theta\) is
equipped with the product metric:

\[d_{\mathcal{Z}}(z, z') = d_{\mathcal{F}}(S, S') + d_{\mathcal{M}}(M, M') + \|\theta - \theta'\|_2\]

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{\texorpdfstring{6. Scoring Function
\(S_t\)}{6. Scoring Function S\_t}}<!-- label: scoring-function-s_t -->

#### 6.1 Definition<!-- label: definition-2 -->

**Definition 5 (Gatekeeper Scoring Function).** At time \(t\), the
gatekeeper is a function:

\[S_t: \mathcal{X}_0 \times \mathcal{Y} \to [0,1]\]

that maps an input-label pair \((x, y)\) to a reliability score
\(S_t(x, y)\), interpreted as
\(\mathbb{P}(\ell(f_m(x), y) < \tau \mid x, clean)\) --- the
probability that the label \(y\) for sample \(x\) is correct (i.e., not
noise).

**Initialization (t=0).** The initial scoring function \(S_0\) is
derived from the static SCX framework:

\[S_0(x, y) = \frac{1}{M} \sum_{m=1}^M \mathbf{1}\{\ell(f_m(x), y) < \tau\}\]

i.e., the proportion of experts that agree with label \(y\) within
tolerance \(\tau\). This is the standard SCX reliability estimate.

**Evolution rule.** For \(t \geq 1\), \(S_t\) is updated using
information from \(M_{t-1}\) and \(f_{\theta_{t-1}}\):

\[S_t = Update(S_{t-1}, M_{t-1}, f_{\theta_{t-1}})\]

where \(Update\) is a learning algorithm (e.g., gradient descent
on a calibrated loss). The exact form depends on the implementation.

#### 6.2 Parameterized Form<!-- label: parameterized-form -->

For practical analysis, we often assume \(S_t\) is parameterized by
weights \(w_t \in \mathbb{R}^{d_w}\):

\[S_t(x, y) = \sigma\bigl( w_t^\top \psi(x, y) \bigr)\]

where \(\sigma: \mathbb{R} \to [0,1]\) is a sigmoid (e.g., logistic) and
\(\psi: \mathcal{X}_0 \times \mathcal{Y} \to \mathbb{R}^{d_w}\) is a
fixed feature map.

#### 6.3 Interpretation<!-- label: interpretation -->

The scoring function serves as: 1. **Noise filter**: samples with
\(S_t(x, y) < \delta\) (for some threshold \(\delta\)) are flagged as
potentially noisy 2. **Memory gatekeeper**: samples with high
\(S_t\) are stored in \(M_t\) as reliable reference data 3. **NEP
training signal**: the scoring function's decisions provide training
targets for the NEP student

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{\texorpdfstring{7. Memory Bank
\(M_t\)}{7. Memory Bank M\_t}}<!-- label: memory-bank-m_t -->

#### 7.1 Definition<!-- label: definition-3 -->

**Definition 6 (Memory Bank).** The memory bank at time \(t\) is a
collection of labeled samples with associated metadata:

\[M_t = \bigl\{ (x_i, y_i, v_i, c_i) \bigr\}_{i=1}^{N_t}\]

where: - \(x_i \in \mathcal{X}_0\): input sample -
\(y_i \in \mathcal{Y}\): observed label - \(v_i \in \{0, 1\}\):
**verdict** at time of storage (\(v_i = 1\) if the sample was
judged reliable, \(v_i = 0\) otherwise) - \(c_i \in [0,1]\):
**confidence** of the gatekeeper at time of storage
(\(c_i = S_{t_i}(x_i, y_i)\) where \(t_i\) is the storage time)

**Monotonicity property**:

\[M_t \subseteq M_{t+1} \quad \forall t \geq 0\]

Memory only grows; samples are never deleted. This is a design choice
that prevents forgetting but raises questions about staleness (see
Proposition 1 below).

#### 7.2 Empirical Distribution<!-- label: empirical-distribution -->

Define the empirical distribution over the memory bank:

\[\hat{P}_t(x, y, v, c) = \frac{1}{N_t} \sum_{i=1}^{N_t} \delta_{(x_i, y_i, v_i, c_i)}\]

As \(t \to \infty\), if the data distribution has finite support or if
we assume sufficient exploration, \(\hat{P}_t\) converges to a limiting
empirical distribution \(\hat{P}_\infty\).

#### 7.3 Memory Growth Dynamics<!-- label: memory-growth-dynamics -->

The growth of \(N_t\) depends on the gatekeeper's decisions:

**Definition 7 (Memory Flow).** Let \(q_t\) be the incoming sample
batch at time \(t\). The gatekeeper \(S_t\) selects a subset for
inclusion:

\[\Delta M_t = \bigl\{ (x, y, S_t(x,y), S_t(x,y)) \mid (x,y) \in q_t, \; S_t(x,y) > \delta_{store} \bigr\}\]

where \(\delta_{store} \in (0,1)\) is a storage threshold. Then:

\[M_{t+1} = M_t \cup \Delta M_t, \qquad N_{t+1} = N_t + |\Delta M_t|\]

**Proposition 1 (Memory Growth Rate).** Under Assumptions B1-B3
(defined in Section 13), the expected growth rate satisfies:

\[\mathbb{E}[N_{t+1} - N_t] \geq |q_t| \cdot \mathbb{P}_{(x,y) \sim \mathcal{D}}\bigl( S_t(x,y) > \delta_{store} \bigr)\]

If the scoring function \(S_t\) is improving (becoming more accurate),
the growth rate may decrease initially (more false positives filtered)
then increase (more true positives retained). The exact dynamics depend
on the noise rate \(\eta\) and the clean error rate \(\mu_s\).

*Proof sketch.* Each sample in batch \(q_t\) is included
independently with probability
\(\mathbb{P}(S_t(x,y) > \delta_{store})\), conditional on the
sample's features. The expected increment follows by linearity of
expectation. \(\square\)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{\texorpdfstring{8. NEP Student
\(f_{\theta_t}\)}{8. NEP Student f\_\{\ theta\_t\}}}<!-- label: nep-student-f_theta_t -->

#### 8.1 Definition<!-- label: definition-4 -->

**Definition 8 (NEP Student).** The NEP (Noise-Equivariant
Predictor) student at time \(t\) is a function:

\[f_{\theta_t}: \mathcal{X}_0 \to \mathcal{Y}\]

parameterized by
\(\theta_t \in \Theta \subseteq \mathbb{R}^{d_\theta}\). The student is
trained on the memory bank \(M_t\) to predict the true label given an
input.

**Training objective**:

\[\theta_{t+1} = \arg\min_{\theta \in \Theta} \frac{1}{N_t} \sum_{i=1}^{N_t} \ell_{nep}\bigl( f_\theta(x_i), y_i \bigr) + \lambda \cdot \mathcal{R}(\theta)\]

where \(\ell_{nep}\) is the NEP loss (Section 10), and
\(\mathcal{R}(\theta)\) is a regularization term.

#### 8.2 NEP as Delayed Oracle<!-- label: nep-as-delayed-oracle -->

The NEP student serves as a **delayed ground-truth oracle** for the
gatekeeper. After training on \(M_t\), the student can provide feedback
on samples that were previously ambiguous:

\[feedback_t(x) = \begin{cases}
f_{\theta_t}(x) & if  Confidence(f_{\theta_t}(x)) > \delta_{nep} 

\emptyset & otherwise (abstain)
\end{cases}\]

This feedback is used to update the scoring function \(S_{t+1}\).

#### 8.3 Initialization<!-- label: initialization -->

At \(t=0\), the NEP student is initialized with pre-trained weights
(e.g., from supervised learning on a clean subset):

\[f_{\theta_0} = pretrained model\]

If no pre-training is available, \(\theta_0\) is randomly initialized
and \(M_0\) is populated with expert consensus labels.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{\texorpdfstring{9. Update Operator
\(\Phi\)}{9. Update Operator \ Phi}}<!-- label: update-operator-phi -->

#### 9.1 Definition<!-- label: definition-5 -->

**Definition 9 (Self-Evolution Update Operator).** The update
operator is a mapping:

\[\Phi: \mathcal{Z} \to \mathcal{Z}\]

that advances the system state by one evolution round:

\[\Phi(S_t, M_t, \theta_t) = (S_{t+1}, M_{t+1}, \theta_{t+1})\]

The operator decomposes into three component updates:

\[\Phi = (\Phi_S, \Phi_M, \Phi_\theta)\]

where:

1. 
2. 
3. 

\subsubsection{9.2 Deferred Update
Variant}<!-- label: deferred-update-variant -->

In practice, updates may be applied at different frequencies. Define the
**update interval** \(\Delta_t\) as the number of evolution rounds
between NEP retraining. The gatekeeper update \(\Phi_S\) may be applied
every round (online), while \(\Phi_\theta\) is applied every
\(\Delta_t\) rounds (batch).

For the theoretical analysis in Documents 02 and 03, we primarily
consider the synchronous update where all three components update at
each round.

#### 9.3 Composition<!-- label: composition -->

Let \(\Phi^{(k)}\) denote \(k\) successive applications:

\[\Phi^{(k)}(z_0) = \underbrace{\Phi \circ \Phi \circ ... \circ \Phi}_{k  times}(z_0) = z_k\]

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 10. Loss Functions<!-- label: loss-functions -->

\subsubsection{\texorpdfstring{10.1 Gatekeeper Loss
\(L_{gate}\)}{10.1 Gatekeeper Loss L\_\{\ text\{gate\}\}}}<!-- label: gatekeeper-loss-l_textgate -->

**Definition 10 (Gatekeeper Loss).** For a scoring function \(S\)
and a sample \((x, y)\) with (possibly unknown) ground-truth noise
status \(z \in \{0,1\}\) (0 = clean, 1 = noise), the gatekeeper loss is:

\[L_{gate}(S; x, y, z) = -z \cdot \log(1 - S(x,y)) - (1-z) \cdot \log S(x,y)\]

This is the standard binary cross-entropy loss, treating \(S(x,y)\) as
the predicted probability that the sample is clean.

**Empirical risk** on a memory bank \(M_t\) (with verdict \(v_i\)
as a proxy for \(z_i\)):

\[\hat{L}_{gate}(S; M_t) = -\frac{1}{N_t} \sum_{i=1}^{N_t} \bigl[ v_i \cdot \log S(x_i, y_i) + (1-v_i) \cdot \log(1 - S(x_i, y_i)) \bigr]\]

The **expected gatekeeper loss** is:

\[L_{gate}^*(S) = \mathbb{E}_{(x,y) \sim \mathcal{D}}\bigl[ -\eta \cdot \log(1 - S(x,y)) - (1-\eta) \cdot \log S(x,y) \bigr]\]

where \(\eta\) is the global noise rate.

**Proposition 2 (Optimal Gatekeeper).** The gatekeeper \(S^*\)
minimizing \(L_{gate}^*\) satisfies:

\[S^*(x, y) = \frac{1-\eta} \cdot \frac{\mathbb{P}(y \mid x, clean)}{\mathbb{P}(y \mid x, noise)}\]

when the ratio is well-defined. Under the uniform noise assumption (A4),
this simplifies to:

\[S^*(x, y) \propto \mathbb{P}(y \mid x, clean)\]

*Proof sketch.* The binary cross-entropy optimum is the conditional
probability \(\mathbb{P}(z=0 \mid x, y)\). Applying Bayes' rule gives
the expression. Under A4, \(\mathbb{P}(y \mid x, noise)\) is
uniform, simplifying the ratio. \(\square\)

\subsubsection{\texorpdfstring{10.2 NEP Student Loss
\(L_{nep}\)}{10.2 NEP Student Loss L\_\{\ text\{nep\}\}}}<!-- label: nep-student-loss-l_textnep -->

**Definition 11 (NEP Student Loss).** The NEP student is trained
with a noise-robust loss function:

\[L_{nep}(f_\theta; x, y) = \ell_{CE}(f_\theta(x), y) + \beta \cdot \ell_{cons}(f_\theta(x), f_{expert}(x))\]

where: - \(\ell_{CE}\) is the standard cross-entropy loss -
\(\ell_{cons}\) is a consistency regularization term encouraging
agreement with expert consensus - \(\beta \geq 0\) is a trade-off
parameter - \(f_{expert}(x)\) is the expert consensus prediction
(e.g., majority vote)

The **empirical NEP loss** on memory bank \(M_t\):

\[\hat{L}_{nep}(f_\theta; M_t) = \frac{1}{N_t} \sum_{i=1}^{N_t} \ell_{CE}(f_\theta(x_i), y_i) + \frac{N_t} \sum_{i=1}^{N_t} \ell_{cons}(f_\theta(x_i), f_{expert}(x_i))\]

\subsubsection{10.3 Composite Loss for
Self-Evolution}<!-- label: composite-loss-for-self-evolution -->

The overall objective guiding self-evolution is:

\[L_{total}(z_t) = \mathbb{E}\bigl[ L_{gate}(S_t) \bigr] + \lambda \cdot \mathbb{E}\bigl[ L_{nep}(f_{\theta_t}) \bigr]\]

where \(\lambda > 0\) is a hyperparameter balancing the two components.
This composite loss serves as a Lyapunov function candidate in Document
02.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 11. Evaluation Metrics<!-- label: evaluation-metrics -->

#### 11.1 Consistency Score<!-- label: consistency-score -->

**Definition 12 (Evolutionary Consistency Score).** The consistency
score at time \(t\) is the agreement rate between the gatekeeper and the
NEP student on a held-out validation set \(V\):

\[Consistency_t = \frac{1}{|V|} \sum_{(x,y) \in V} \mathbf{1}\bigl\{ sign(S_t(x,y) - \delta_{gate}) = sign(Confidence(f_{\theta_t}(x)) - \delta_{nep}) \bigr\}\]

This measures whether the gatekeeper and NEP converge to similar
judgments.

#### 11.2 Coverage<!-- label: coverage -->

**Definition 13 (Gatekeeper Coverage).** The coverage at time \(t\)
is the proportion of samples that the gatekeeper judges with sufficient
confidence:

\[Coverage_t = \mathbb{P}_{(x,y) \sim \mathcal{D}} \bigl( S_t(x,y) > \delta_{cover} \bigr)\]

where \(\delta_{cover} \in (0,1)\) is a coverage threshold
(typically \(\delta_{cover} = 0.5\)).

**Evolutionary behavior**: As \(S_t\) improves, coverage should
increase because more samples can be confidently classified.

#### 11.3 Detection Rate<!-- label: detection-rate -->

**Definition 14 (Noise Detection Rate).** The detection rate at
time \(t\) for a fixed noise threshold \(\delta_{noise}\):

\[DetectionRate_t = \mathbb{P}_{(x,y) \sim \mathcal{D}} \bigl( S_t(x,y) < \delta_{noise} \mid z = 1 \bigr)\]

where \(z=1\) indicates the sample is noise. This is the true positive
rate (recall) of the noise detection function.

**Relationship to Theorem 1**: The detection rate is bounded below
by Theorem 1's guarantee when \(S_t\) is derived from expert consensus.
As \(S_t\) evolves, the detection rate may improve beyond the static
bound.

#### 11.4 F1 Score (Dynamic)<!-- label: f1-score-dynamic -->

**Definition 15 (Dynamic F1).** At time \(t\):

\[F1_t = \frac{2 \cdot Precision_t \cdot Recall_t}{Precision_t + Recall_t}\]

where: - \(Recall_t = DetectionRate_t\) -
\(Precision_t = \mathbb{P}(z = 1 \mid S_t(x,y) < \delta_{noise})\)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{12. Relationship to Existing
Definitions}<!-- label: relationship-to-existing-definitions -->

\subsubsection{12.1 From Static to
Dynamic}<!-- label: from-static-to-dynamic -->

The existing SCX theory (THEOREMS\_UNIFIED.md) provides guarantees for a
**static** gatekeeper \(S_{static}\) defined as:

\[S_{static}(x, y) = \frac{1}{M} \sum_{m=1}^M \mathbf{1}\{\ell(f_m(x), y) < \tau\}\]

The dynamic gatekeeper \(S_t\) generalizes this:

\[S_t(x, y) = \begin{cases}
S_{static}(x, y) & t = 0  (initialization) 

Update(S_{t-1}, M_{t-1}, f_{\theta_{t-1}}) & t \geq 1
\end{cases}\]

\subsubsection{12.2 Connection to State-Conditioned
Risk}<!-- label: connection-to-state-conditioned-risk -->

The expert risk \(R_m(s)\) and reliability score \(SCX_m(s)\)
from the static theory appear in the initialization:

\[S_0(x, y) = \frac{1}{M} \sum_{m=1}^M SCX_m(s(x)) \cdot \frac{\mathbb{P}(f_m(x) = y \mid x \in s(x))}{SCX_m(s(x))}\]

where
\(SCX_m(s) = \mathbb{P}(\ell(f_m(x), y) < \tau \mid x \in s)\).

\subsubsection{12.3 Connection to Consensus
Score}<!-- label: connection-to-consensus-score -->

The consensus score \(C(x)\) is related to \(S_0\) via:

\[S_0(x, y) = 1 - \frac{1}{M} \sum_{m=1}^M e_m(x, y) = 1 - C(x) \quad (when  y = y_{obs}  is the observed label)\]

This gives the key insight: the initial gatekeeper is the
**inverse** of the consensus score. High consensus among experts
that the sample is erroneous (\(C(x)\) near 1) means low gatekeeper
score (\(S_0\) near 0), flagging the sample as potentially noisy.

\subsubsection{12.4 Theorems 1-3 in the Dynamic
Setting}<!-- label: theorems-1-3-in-the-dynamic-setting -->

- 
- 
- 

**Conjecture 1 (Self-Evolution Breaks Unidentifiability Under
Model Correctness).** If the NEP student \(f_{\theta_t}\) converges to
the true oracle \(f^*\) as \(t \to \infty\) (i.e.,
\(\lim_{t\to\infty} \mathbb{P}(f_{\theta_t}(x) = f^*(x)) = 1\)), then
the limiting gatekeeper \(S_\infty\) can distinguish noise from
difficulty with error rate below the Theorem 3 bound. However, this
requires that the NEP's model class is well-specified and \(M_t\)
contains sufficient clean samples.

*Status: **Conjecture** --- not yet proven.*

\subsubsection{12.5 Assumption A2: Untestability and Violation
Degradation (DEFECT-07
Fix)}<!-- label: assumption-a2-untestability-and-violation-degradation-defect-07-fix -->

**Original claim.** Assumption A2 jointly requires **both**
requirements: (i) experts are trained on disjoint data (ensuring
training-set independence via A1), **and** (ii) expert errors
\(e_m(x, y)\) are conditionally independent given the input \(x\) when
the sample is clean. The original text claimed that A2 is ``testable''
{[}可检验{]} and that Assumption A1 (disjoint training sets) alone
**guarantees** A2 --- it does not; both requirements must be
independently satisfied and neither alone suffices.

**Corrected understanding.** A2 is a **structural assumption**
about the expert training process, not an empirically testable
condition:

1. 
2. 
3. 

**Degradation when A2 is violated.** When experts are positively
correlated, the consensus score \(C(x) = \frac{1}{M}\sum_m e_m(x,y)\)
behaves as if there are fewer independent experts. The effective sample
size degrades from \(M\) to \(M_{eff}\):

\[\boxed{\;M_{eff} \approx \frac{M}{1 + (M-1)\bar}\;},\]

where \(\bar\) is the average pairwise correlation of expert error
indicators. The Hoeffding concentration bound in Theorem 1 degrades from
\(\exp(-2M\Delta^2)\) to \(\exp(-2M_{eff}\Delta^2)\).

**Quantitative impact (examples):** - \(M = 10\),
\(\bar = 0.1\): \(M_{eff} \approx 10/(1+0.9) \approx 5.3\)
(moderate degradation) - \(M = 10\), \(\bar = 0.3\):
\(M_{eff} \approx 10/(1+2.7) \approx 2.7\) (severe degradation
--- effective number of experts is \textless{} 3) - \(M = 10\),
\(\bar = 0.5\): \(M_{eff} \approx 10/(1+4.5) \approx 1.8\)
(catastrophic --- barely better than 1 expert)

**Recommendation for practitioners.** When applying SCX, estimate
\(\bar\) from expert predictions on a held-out validation set via
the mutual information \(I(e_i; e_j)\) or the phi coefficient. Use
\(M_{eff}\) in place of \(M\) in Theorem 1's bound for a
conservative guarantee. If \(M_{eff} \leq 2\), the consensus
score is unreliable and SCX should be used with caution or with
additional diversity-enforcing mechanisms.

**Revised A2 statement.** A2 is now stated as: ``Expert errors are
conditionally independent given \(x\) for clean samples, as justified by
disjoint training sets (A1) and independent initialization. **This
assumption is not empirically testable from the SCX pipeline's data.**
When violated (e.g., due to shared inductive biases), replace \(M\) with
\(M_{eff}\) in all concentration bounds.''

\subsection{13. Assumption Catalog for Self-Evolution
(B1-B6)}<!-- label: assumption-catalog-for-self-evolution-b1-b6 -->

These assumptions extend the core A1-A6 into the self-evolution regime.

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.0638}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.2340}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.3617}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1915}}
  >{\arraybackslash}p{(\linewidth - 8\tabcolsep) * \real{0.1489}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
\#
\end{minipage} & \begin{minipage}[b]
Assumption
\end{minipage} & \begin{minipage}[b]
Formal Statement
\end{minipage} & \begin{minipage}[b]
Used in
\end{minipage} & \begin{minipage}[b]
Notes
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
**B1** & **Memory Monotonicity** & \(M_t \subseteq M_{t+1}\),
\(\forall t \geq 0\) & Doc 02, 03 & Design assumption; no deletion 

**B2** & **Bounded Memory Growth** &
\(\exists G_ < \infty\) s.t.
\(\mathbb{E}[N_{t+1} - N_t] \leq G_\), \(\forall t\) & Doc 02, 03
& Prevents explosion 

**B3** & **NEP Convergence** & \(\forall \varepsilon > 0\),
\(\exists T(\varepsilon)\) s.t. \(\forall t \geq T\):
\(\mathbb{E}[\ell(f_{\theta_t}(x), f^*(x))] \leq \varepsilon\) & Doc 02
& Assumes well-specified model 

**B4** & **Gatekeeper Lipschitz Continuity** &
\(|S_t(x,y) - S_t(x,y')| \leq L_S \cdot \|y - y'\|\) for some
\(L_S < \infty\) & Doc 03 & Needed for regret bound 

**B5** & **Bounded Gradient** &
\(\|\nabla_w \ell_t(S_t)\|_2 \leq G\) for all \(t\), where \(\ell_t\) is
the per-round loss & Doc 03 & Standard OGD assumption 

**B6** & **Delayed Feedback Bound** &
\(d_t \leq D_ < \infty\) almost surely, where \(d_t\) is feedback
delay & Doc 03 & For delay analysis 

\end{longtable}

\subsubsection{13.1 Relationship to Core Assumptions
A1-A6}<!-- label: relationship-to-core-assumptions-a1-a6 -->

The core assumptions A1-A6 operate at the level of individual expert
models and sample statistics. The self-evolution assumptions B1-B6
operate at the system level. They are complementary:

- 
- 
- 

**Note on A2 degradation (DEFECT-07 fix).** Assumption A2 jointly
requires: **(i) disjoint training data** (A1), and **(ii)
conditionally independent expert errors** given \(x\) for clean samples.
When requirement (ii) is violated --- as is common in practice due to
shared inductive biases --- the effective number of independent experts
degrades from \(M\) to \(M_{eff} = M/(1+(M-1)\bar)\). All
concentration bounds in both the static theory (Theorem 1) and the
self-evolution framework (Proposition SE-1.4) should use
\(M_{eff}\) in place of \(M\). See Section 12.5 for the full
analysis. Neither requirement (i) nor (ii) alone is sufficient; both
must hold for the original concentration bounds to apply at full
strength. A2 is not empirically testable from the SCX pipeline's data;
it is a structural assumption justified by the experimental design.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 14. Summary of Notation<!-- label: summary-of-notation -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1818}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2045}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2500}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3636}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Symbol
\end{minipage} & \begin{minipage}[b]
Meaning
\end{minipage} & \begin{minipage}[b]
Defined In
\end{minipage} & \begin{minipage}[b]
Existing Core?
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(x\) & SCX configuration & Section 4 & No (new) 

\(z_t = (S_t, M_t, \theta_t)\) & Evolution state & Section 5 & No
(new) 

\(\mathcal{Z} = \mathcal{F} \times \mathcal{M} \times \Theta\) &
Evolution state space & Section 5 & No (new) 

\(S_t: \mathcal{X} \times \mathcal{Y} \to [0,1]\) & Gatekeeper scoring
function & Section 6 & No (new) 

\(M_t\) & Memory bank & Section 7 & No (new) 

\(f_{\theta_t}: \mathcal{X} \to \mathcal{Y}\) & NEP student & Section 8
& No (new) 

\(\Phi: \mathcal{Z} \to \mathcal{Z}\) & Update operator & Section 9 & No
(new) 

\(L_{gate}\) & Gatekeeper loss & Section 10 & No (new) 

\(L_{nep}\) & NEP student loss & Section 10 & No (new) 

\(Consistency_t\) & Evolutionary consistency & Section 11 & No
(new) 

\(Coverage_t\) & Gatekeeper coverage & Section 11 & No (new) 

\(DetectionRate_t\) & Noise detection rate & Section 11 & No
(new) 

\(d_{\mathcal{X}}, d_{\mathcal{F}}, d_{\mathcal{M}}, d_{\mathcal{Z}}\) &
Metrics & Sections 4-5 & No (new) 

\(\mathcal{D}\) & Data distribution & Inherited & Yes 

\(C(x)\) & Consensus score & Inherited & Yes 

\(\eta\) & Noise rate & Inherited & Yes 

\(\mu_s\) & State-\(s\) clean error bound & Inherited & Yes 

\(\mathcal{S}, s(x)\) & State space, assignment & Inherited & Yes 

\(\{f_m\}_{m=1}^M\) & Expert models & Inherited & Yes 

\(\rho_s\) & State probability & Inherited & Yes 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*End of Document 01: Symbol System and Problem Setup*

*Preparation for Document 02: The next document will formalize the
iteration \(z_{t+1} = \Phi(z_t)\) as a discrete dynamical system,
analyze fixed points, Lyapunov functions, and attractors.*

*Preparation for Document 03: The following document will analyze
the gatekeeper's online learning regret under delayed feedback from the
NEP student.*

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Changelog<!-- label: changelog -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1875}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2500}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2500}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3125}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Date
\end{minipage} & \begin{minipage}[b]
Defect
\end{minipage} & \begin{minipage}[b]
Change
\end{minipage} & \begin{minipage}[b]
Severity
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
2026-06-28 & DEFECT-07 & **Added A2 untestability and degradation
analysis** (Section 12.5). Acknowledged that Assumption A2 (conditional
independence of expert errors given \(x\)) is not empirically testable
from SCX pipeline data --- for continuous \(\mathcal{X}\), each \(x\)
appears at most once. A1 (disjoint training) does not guarantee A2 when
experts share inductive biases. Added quantitative degradation:
effective sample size \(M_{eff} = M/(1+(M-1)\bar)\) where
\(\bar\) is average pairwise error correlation. For \(M=10\),
\(\bar=0.3\), \(M_{eff} \approx 2.7\) (severe).
Recommendation: estimate \(\bar\) on held-out validation set and
use \(M_{eff}\) in Theorem 1. & MAJOR 

2026-06-28 & --- & **Updated Assumption Catalog** (Section 13.1)
with cross-reference to A2 degradation analysis. & --- 

2026-06-28 & B1 & **A2 statement now consistently states BOTH
requirements** (§12.5, §13.1): (i) experts trained on disjoint data, AND
(ii) conditionally independent errors. Previously some references
mentioned only one requirement. & MAJOR 

2026-06-28 & B3 & **Added explicit notation note** (§2):
\(\mathcal{S}\) (calligraphic) = state space (finite index set)
vs.~\(S_t\) (italic with subscript) = gatekeeper scoring function at
time \(t\). These are entirely distinct objects; context disambiguates.
& MINOR 

\end{longtable}