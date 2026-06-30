1|# The SCX Story: How a Gauge-Fixing Problem Became an Uncertainty Principle
2|
3|> A candid intellectual history of the State-Conditioned eXpertise framework.
4|> Written from development logs, theorem drafts, adversarial audits, and git history.
5|> No press release. No vision statement. Just what happened and what we learned.
6|
7|---
8|
9|## Preface: On Telling the Truth About Research
10|
11|Most papers lie about how they were written. The introduction presents a clean logical arc
12|from problem to solution, as if the author woke up one morning with the theorems fully
13|formed. The real history—the dead ends, the bugs in the proofs, the concepts that took
14|weeks to name, the theorems that turned out to be corollaries of theorems we hadn't
15|proven yet—gets compressed into acknowledgments or erased entirely.
16|
17|This document is the opposite. It records what actually happened in the development of
18|the SCX framework between May and June 2026: a period in which a practical problem in
19|interatomic potential merging unfolded, over roughly five weeks, into a mathematical
20|framework spanning four theorems, three core algorithms, a self-evolving gatekeeper with
21|Lyapunov convergence guarantees, and—unexpectedly—an uncertainty principle for label
22|noise detection.
23|
24|The author is a Ph.D. student at Wuhan University. All theoretical work was done on a
25|personal computer at home, using AI coding assistants and inference APIs as
26|implementation tools. The Xiaogan Supercomputing Center was used exclusively for DFT
27|calculations in the EGP project (Papers 1–3), not for SCX development.
28|
29|We tell this story not because it is exceptional, but because it is typical of how
30|research actually works—and because the clean narratives we publish in journals train
31|students to expect a linear path that does not exist.
32|
33|---
34|
35|## Chapter 1: Origins — The EGP Gauge-Fixing Problem
36|
37|### 1.1 The Practical Problem
38|
39|In May 2026, the author was working on the EGP (Expert-Guided Potential) project:
40|constructing machine-learned interatomic potentials (MLIPs) for III-nitride
41|semiconductors (AlN, GaN, and eventually AlGaN) using the Atomic Cluster Expansion
42|(ACE) framework. The practical task was straightforward: train separate ACE potentials
43|on different chemical domains, then merge them into a single multi-element potential.
44|
45|The appeal of this modular approach is obvious. A community could build a library of
46|specialized potentials—AlN trained by one group, GaN by another, InN by a third—and
47|combine them as needed without costly joint retraining. The ACE framework's linear
48|parameterization makes this particularly natural: coefficients are just vectors, and
49|vectors can be averaged.
50|
51|### 1.2 Why Direct Merging Fails
52|
53|It doesn't work. The naive merge—averaging the coefficient vectors of independently
54|trained experts—produces catastrophic errors: $C_{33}$ elastic constant deviations
55|exceeding $50\%$, formation energy sign reversals, and force predictions worse than
56|either expert individually.
57|
58|The failure is not a numerical accident. Four distinct sources of inconsistency block
59|safe merging:
60|
61|**(I1) Energy reference ambiguity.** Forces determine the potential energy surface only
62|up to an additive constant. Each expert's training loss ${\mathcal{L}}_F$ (force RMSE)
63|is invariant under $E \to E + C$, so the absolute energy zero is unconstrained. Two
64|experts trained on different domains end up with unrelated energy zeros, producing
65|spurious energy differences upon merging.
66|
67|**(I2) Species-shift misalignment.** The per-species constant shifts $b_Z$ absorb a
68|significant fraction of the energy reference ambiguity. When Expert A (AlN) assigns one
69|shift to nitrogen and Expert G (GaN) assigns another, the merged model inherits
70|inconsistent shifts that produce systematic formation energy errors.
71|
72|**(I3) Coefficient-level gauge freedom.** The shared-correction ACE parameterization
73|$E = \sum_i [{\mathbf{c}}_0 + {\mathbf{c}}_{Z_i}] \cdot {\mathbf{B}}({\mathbf{q}}_i) + b_{Z_i}$
74|admits an exact gauge transformation:
75|$${\mathbf{c}}_0 \to {\mathbf{c}}_0 + {\mathbf{g}}, \quad {\mathbf{c}}_Z \to {\mathbf{c}}_Z - {\mathbf{g}}$$
76|which leaves all physical predictions invariant for any vector ${\mathbf{g}}$.
77|Different experts explore different regions of this gauge-equivalent space, making their
78|coefficient vectors incompatible for direct combination. The gauge violation in
79|unconstrained training—$\lVert\sum_Z \pi_Z {\mathbf{c}}_Z\rVert$—reaches $8.77$ in
80|typical runs, confirming that the degeneracy is numerically active.
81|
82|**(I4) Residual meaning incompatibility.** Domain-specific corrections learned by each
83|expert are meaningful only relative to their own data distribution. Naively combining
84|them can cancel or amplify corrections in physically arbitrary ways.
85|
86|### 1.3 The Gauge-Fixing Solution
87|
88|The first contribution of the EGP paper was a post-hoc gauge-fixing procedure: after
89|training each expert without constraints, apply the orthogonal projection
90|$${\mathbf{g}} = \sum_Z \pi_Z {\mathbf{c}}_Z, \quad {\mathbf{c}}_Z' = {\mathbf{c}}_Z - {\mathbf{g}}, \quad {\mathbf{c}}_0' = {\mathbf{c}}_0 + {\mathbf{g}}.$$
91|
92|This achieves exact gauge cancellation (residual $4.6\times10^{-16}$, machine
93|precision) with zero change to physical predictions. The key insight was *negative*: a
94|soft penalty approach—adding $\lambda\lVert\sum_Z\pi_Z{\mathbf{c}}_Z\rVert^2$ to the
95|training loss—fundamentally fails. A systematic $\lambda$-sweep over six orders of
96|magnitude ($10^{-3}$ to $10^1$) revealed that no $\lambda$ simultaneously achieves
97|gauge violation below $0.1$ and accuracy degradation under $20\%$. The gauge constraint
98|subspace is nearly orthogonal to the physical loss landscape; gradient descent cannot
99|simultaneously satisfy both.
100|
101|This negative result was more instructive than the positive one. It established a
102|principle that would recur throughout SCX development: **consistency constraints must be
103|applied post-hoc, not enforced during optimization, when the constraint subspace is
104|orthogonal to the objective landscape.**
105|
106|### 1.4 The Observation That Started Everything
107|
108|During the EGP work, the author noticed a recurring phenomenon: the same expert
109|potential's prediction reliability varied dramatically across different regions of
110|configuration space. An AlN expert that achieved $0.047$ eV/Å force RMSE globally would
111|show $0.012$ eV/Å on bulk equilibrium structures but $0.15$ eV/Å on defect
112|configurations and $0.30$ eV/Å on thermal snapshots far from the training distribution.
113|
114|This observation—that **expert reliability is not a global constant but a
115|state-conditioned quantity**—was the seed from which everything else grew. It was not a
116|theoretical insight. It was an empirical nuisance that kept showing up in the data.
117|
118|---
119|
120|## Chapter 2: State Crystallization — Naming the Third Core Algorithm
121|
122|### 2.1 From "PBE Operation" to a Concept
123|
124|For several weeks, a fundamental operation in the SCX pipeline existed without a name.
125|It was referred to as "the PBE operation" or "Layer 2 discretization of the two-layer
126|descriptor"—descriptions of implementation, not of concept. The operation itself was
127|clear: use PBE (Perdew-Burke-Ernzerhof) DFT calculations to discover natural clustering
128|boundaries in continuous physical quantities (bond angles, bond lengths, coordination
129|numbers), producing discrete state atoms. But calling it "the PBE operation" was like
130|calling a car "the internal combustion operation."
131|
132|On June 29, 2026, in a discussion with the AI coding agent (designated "Hermes" in
133|development logs), the concept was formally named **State Crystallization**.
134|
135|### 2.2 Why "Crystallization"
136|
137|The metaphor is precise. In physical crystallization, a continuous disordered phase
138|(liquid/solution) spontaneously develops discrete ordered structure (crystal), with
139|boundaries determined by intrinsic thermodynamic laws, not by human cutting. In State
140|Crystallization, continuous physical quantities (bond angles 109.5°, bond lengths
141|1.46 Å) spontaneously cluster into discrete state atoms, with boundaries determined by
142|the PBE energy surface, not by statistical frequency or human naming conventions.
143|
144|The naming resolved a longstanding semantic confusion. "PBE operation" described the
145|tool. "Two-layer descriptor Layer 2 discretization" described the mechanical step.
146|Neither captured the ontological claim: **states are discovered, not defined.**
147|
148|### 2.3 State Crystallization ≠ BPE
149|
150|The natural LLM analogue is Byte Pair Encoding (BPE), which also produces discrete
151|tokens from a less-structured input. But the analogy is instructive precisely because it
152|breaks:
153|
154|| Dimension | State Crystallization | BPE |
155||-----------|----------------------|-----|
156|| Input | Continuous physical quantities | Discrete symbol sequences |
157|| Boundary criterion | Physical reality (PBE energy surface) | Statistical frequency |
158|| Ontology | **Discovers** natural state boundaries | **Conventions** for cutting |
159|| Mathematical form | $\mathcal{D}_{\text{phys}}$ | $\mathcal{D}_{\text{freq}}$ |
160|| Anchor | Physical ground truth (verifiable) | None (statistical construct) |
161|
162|The formal relationship is inclusion: BPE is the degenerate limit of State
163|Crystallization when physical coupling approximates frequency coupling. In this limit,
164|$\mathcal{D}_{\text{freq}} \approx \mathcal{D}_{\text{phys}}$, but the converse is not
165|true—State Crystallization can handle continuous physical quantities that BPE cannot
166|even represent.
167|
168|This relationship is not merely taxonomic. It identifies what SCX does that LLMs cannot:
169|anchor state definitions in physical reality rather than statistical convention. A bond
170|angle of 109.5° is sp$^3$ hybridization regardless of how frequently it co-occurs with
171|other features in a training corpus.
172|
173|### 2.4 Architectural Position
174|
175|State Crystallization was established as the **third core algorithm** of SCX,
176|completing a layered architecture:
177|
178|| Layer | Algorithm | Function | LLM Analogue |
179||-------|-----------|----------|-------------|
180|| State Ontology | **State Crystallization** | Continuous → discrete state atoms | BPE (but physics-driven) |
181|| State Topology | **Situs** | Positional encoding of states in physical space | Positional Encoding |
182|| State Evolution | **Spring** | Self-evolving gating, state-atom interactions | Transformer (Self-Attention) |
183|| Audit Output | **Yajie** | Verification + audit + evidence chain | — (no LLM audit layer) |
184|| Evaluation | **Cercis Score** | $S = Q + \eta N$ | — |
185|
186|The architecture reveals a structural gap in LLM design: LLMs have no state ontology
187|layer. Their tokens are statistical constructs with no physical anchor. Yajie is more
188|honest than an LLM not because its mathematics is better, but because it audits on a
189|physically real state space, not a statistically constructed one.
190|
191|---
192|
193|## Chapter 3: Yajie — Four Theorems on Label Noise
194|
195|### 3.1 The Core Insight
196|
197|Between June 23–27, 2026, the observation that "expert reliability varies by
198|configurational region" was formalized into a mathematical framework. The central
199|definition:
200|
201|$${\text{SCX}}_m(s) = P(\ell(f_m(x), y) < \tau \mid x \in s)$$
202|
203|Data value is not an intrinsic property of a sample. It is a conditional quantity
204|determined by the state $s$, the expert's reliability ${\text{SCX}}_m(s)$, and the
205|current model's deficiencies—jointly.
206|
207|This is the insight that separates SCX from all prior work on data valuation, active
208|learning, and noise detection. Prior methods assign global scores to samples. SCX
209|assigns state-conditioned scores to experts on samples. The distinction is not a
210|refinement—it is a different category of question.
211|
212|### 3.2 Theorem 1: Consensus-Based Noise Detection
213|
214|**Statement (informal).** Let $M$ independently trained experts vote on the correctness
215|of a label for a sample in state $s$. If the experts are conditionally independent given
216|the true function, then the probability that a noisy label survives consensus screening
217|decays exponentially in $M$:
218|
219|$$P(\text{noise survives} \mid {\text{consensus}}) \leq \exp(-2M\Delta_s^2)$$
220|
221|where $\Delta_s = {\text{SCX}}(s) - 0.5$ is the expert reliability advantage over random
222|guessing in state $s$.
223|
224|**Tools.** Chernoff bound + Hoeffding inequality, under assumptions A1–A6 (conditional
225|independence, bounded loss, state-conditional calibration).
226|
227|**What it means.** Even a modest number of independent experts ($M \sim 5$–$10$) can
228|drive false-acceptance rates below practically meaningful thresholds. The guarantee is
229|exponential, not asymptotic.
230|
231|**Bugs found and fixed.** Lemma 3 was restructured after an adversarial audit revealed
232|a missing assumption (A6: expert errors are sub-Gaussian with state-conditional variance
233|bound). The Chernoff KL direction was corrected (the original proof minimized the wrong
234|divergence). These were not typographical errors—they were logical gaps that would have
235|been caught in review, but the adversarial audit caught them first.
236|
237|### 3.3 Theorem 2: Weak Feature Failure Lower Bound
238|
239|**Statement (informal).** If every feature $X_j$ in state $s$ has mutual information
240|with the label error below a threshold $\delta$, i.e., $I(X_j; L) < \delta$ for all
241|$j$, then any noise detector—not just SCX—has AUC bounded by:
242|
243|$${\text{AUC}} \leq 0.5 + \epsilon(\delta, |s|)$$
244|
245|where $\epsilon \to 0$ as $\delta \to 0$.
246|
247|**Tools.** Fano inequality, information-theoretic lower bounds on detection.
248|
249|**What it means.** SCX does not work everywhere. When features are genuinely
250|uninformative, no method works. This is not a weakness of SCX—it is a fundamental limit
251|of information theory. Theorem 2 provides the diagnostic: compute $I(X_j; L)$ for each
252|feature in each state; states where all features fall below $\delta$ are states where
253|SCX should not be deployed.
254|
255|**Bugs found and fixed.** The original proof claimed optimality of $k$-means clustering,
256|which is false (k-means is NP-hard; no polynomial algorithm can guarantee optimal
257|clustering). This claim was removed. The AUC $\eta$-dependence was clarified: the bound
258|depends on the gap between the null and alternative distributions, not on the absolute
259|AUC level. A cluster balance qualifier was added (the bound degrades when state
260|populations are highly imbalanced).
261|
262|### 3.4 Theorem 3: The Unidentifiability of Noise and Difficulty
263|
264|**Statement (informal).** There exist two worlds—World A (noisy labels) and World B
265|(hard-but-clean labels)—that produce identical observable data distributions. No
266|algorithm can distinguish them from observations alone.
267|
268|**Proof structure.** Constructive two-world proof. In both worlds, the joint
269|distribution $P(X, Y)$ is identical. In World A, label noise generates the errors. In
270|World B, genuine aleatoric uncertainty (inherently difficult samples) generates
271|identical error patterns. The likelihood ratio is 1 for all possible observations, so no
272|statistical test has power exceeding the test's significance level.
273|
274|**What it means.** There is a **hard boundary** on what data cleaning can achieve. Past
275|this boundary, labeling errors and genuinely difficult cases are observationally
276|equivalent. Any algorithm that claims to clean data beyond this boundary is either
277|making unfalsifiable claims or silently degrading into a relabeling engine—replacing one
278|set of labels with another that better matches its own inductive biases.
279|
280|This is SCX's uncertainty principle. Just as Heisenberg's principle is not a measurement
281|deficiency but a statement about what can be known in principle, Theorem 3 is not an
282|algorithmic limitation but a statement about what can be distinguished from data alone.
283|
284|**We discuss Theorem 3's independence and standalone significance in Chapter 8.**
285|
286|### 3.5 Theorem 4: Minimax Optimality
287|
288|**Statement (informal).** SCX's adaptive threshold achieves the exact minimax optimal
289|rate for noise detection. No algorithm can achieve a better worst-case false-positive /
290|false-negative tradeoff.
291|
292|**Tools.** Bahadur-Rao refinement of the Chernoff bound (exact exponential rate, not
293|just asymptotic), combined with Chernoff-Stein lemma for the composite hypothesis
294|testing problem.
295|
296|**What it means.** Theorem 1 says SCX works well. Theorem 4 says no algorithm can work
297|better in the worst case. Together they establish SCX as the optimal solution to a
298|well-defined problem, not merely one heuristic among many.
299|
300|### 3.6 The Cercis Score: $S = Q + \eta N$
301|
302|The Yajie audit engine evaluates every state-conditioned (configuration, label) pair
303|using the Cercis Score:
304|
305|$$S(s) = Q(s) + \eta(t) \cdot N(s)$$
306|
307|where:
308|- $Q(s)$ is the **quality** component: $1 - \overline{\text{residual}}$ across experts
309|- $N(s)$ is the **noise** component: density-weighted + consistency-weighted residual
310|- $\eta(t)$ is the **exploration schedule**: $\eta(0) \gg 1$, $\eta(t) \to 0$ as
311|  $t \to \infty$
312|
313|The Cercis Score is named after *Cercis chinensis* (紫荆), a cauliflorous tree whose
314|flowers bloom directly from old branches. The metaphor: knowledge flowers from
315|accumulated experience (the memory bank), not from new data alone. The exploration term
316|$\eta(t) N(s)$ ensures early-stage openness to discovery; its decay ensures
317|late-stage convergence to a stable quality ranking.
318|
319|### 3.7 What Yajie Does Not Do
320|
321|The name "Yajie" (雅洁) means "elegant purification" in Chinese. But the algorithm does
322|not purify data. It **audits** data—it identifies which samples are clean, which are
323|noisy, and (critically) which are **ambiguous**: samples where Theorem 3's uncertainty
324|principle applies and no determination is possible.
325|
326|The three-way classification—clean / noisy / ambiguous—is not a compromise. It is the
327|mathematically honest output. Binary clean/noisy classifiers are lying about Theorem 3.
328|
329|---
330|
331|## Chapter 4: Situs — From Audit to Independent Theory
332|
333|### 4.1 The Audit That Became a Theory
334|
335|On June 29, 2026, the author asked a practical question: could SCX be extended by
336|incorporating LLM components—specifically, positional encoding and multi-head
337|attention—to create a larger, more expressive model?
338|
339|A 50-turn, maximum-effort mathematical audit was conducted (AI coding agent + inference API)
340|on two candidate components. The audit was intended as an engineering assessment. It
341|became a theory paper.
342|
343|### 4.2 Physical Positional Encoding (PPE → Situs)
344|
345|The idea: encode physical position information (protein sequence position $i$, material
346|3D coordinates $(x,y,z)$, total atom count $N$) as a vector and add it to the state
347|atom representation:
348|$${\mathbf{h}}_i = \phi(s_i) + {\text{PE}}({\mathbf{p}}_i).$$
349|
350|The audit produced four theorems:
351|
352|| Theorem | Finding | Impact |
353||---------|---------|--------|
354|| Thm 1 (Chernoff) | $\Delta_s^{\text{PPE}} = \Delta_s + \delta_s^{\text{PE}}$, bound structure preserved | Improved if position is informative |
355|| Thm 2 (Fano) | Imperfect encoding introduces $\varepsilon_{\text{PE}}$, upper bound loosens | Degraded if encoding is poor |
356|| Thm 3 (Non-identifiability) | Fixed PE → Theorem 3 unchanged. **Learned PE → Theorem 3 broken** | Broken, but beneficially |
357|| Thm 4 (Minimax) | $\Delta D_{\text{KL}}^{\text{PE}} \geq 0$ (data processing inequality), never degrades | Unchanged or improved |
358|
359|The key finding is Theorem 3: a fixed (non-learned) positional encoding preserves the
360|uncertainty principle—noise and difficulty remain indistinguishable. But a **learned**
361|positional encoding can break Theorem 3 by injecting additional information that
362|distinguishes the two worlds. This is not a bug—it means learned position encodings
363|expand the frontier of what can be audited.
364|
365|### 4.3 The Naming: Situs
366|
367|PPE was renamed **Situs** (Latin: "position, location, site") on June 29. The naming
368|criteria:
369|- **Precision**: situs = position, no more and no less
370|- **Domain neutrality**: a protein residue's situs, a grain-boundary vacancy's situs, a
371|  drug molecule's situs—same word, same concept
372|- **Consistency**: Spring (春), Yajie (雅洁), Cercis (紫荆)—all are unique proper nouns
373|  that must be defined once
374|- **Parallelism**: State Crystallization answers "what is the state" (ontology); Situs
375|  answers "where is the state" (topology)
376|
377|### 4.4 Physical Meaning Across Domains
378|
379|Situs is not a generic trick—it maps to different physical quantities in different
380|domains:
381|
382|- **Proteins**: The same "Lys" residue at active site (position $i=37$) vs. surface loop
383|  ($i=289$) has completely different functional significance. Situs lets Spring
384|  distinguish them.
385|- **Materials defects**: A $V_{\text{N}}$ vacancy at a grain boundary vs. bulk vs.
386|  surface has different formation energies and migration barriers. Situs lets Yajie
387|  output position-conditional reliability.
388|- **System size effects**: 32-atom vs. 256-atom supercells exhibit different error
389|  characteristics. Situs lets Spring learn that "small cell = high error risk."
390|
391|### 4.5 Honest Limitations
392|
393|The audit was explicit about limitations:
394|- Situs is useful **only when** $I(Y; P \mid S) > 0$—position carries label information
395|  beyond what the state atom already encodes
396|- **Pure chemical composition classification** (no spatial structure) gains nothing
397|- **Position independent of label** ($I(Y; P \mid X) = 0$) yields zero benefit
398|- The **rotation equivariance** of 3D kernel encoding is only partially achieved
399|  (SO(3) embeddings are approximate)
400|- The **optimal frequency spectrum** derivation assumes a Laplace kernel—a specific
401|  choice justified by smoothness but not uniquely determined
402|
403|### 4.6 Multi-Head Spring: The Negative Result
404|
405|The audit's second component, Multi-Head Spring, produced a starkly negative assessment:
406|
407|- Theorem 1 (Chernoff) was **severely weakened**: heads are not independent experts;
408|  the i.i.d. assumption fails. A strict bound requires $\beta$-mixing conditions—an
409|  **open problem**.
410|- The Lyapunov step size shrinks as $O(1/\sqrt{K})$, and convergence is only to a
411|  stationary point among $K!$ symmetric stationary points.
412|- The critical capacity $K_{\text{crit}} = \lfloor(N \cdot T_{\text{eff}} / d_s^2 - 1)/3\rfloor$;
413|  on the AlN dataset, $K_{\text{crit}} = 1$, meaning **any multi-head configuration
414|  overfits**.
415|- The martingale difference variance scales as $O(K)$, potentially breaking the
416|  marginal martingale property.
417|
418|The AI agent's final judgment: *"PPE is a relatively safe bet—mathematically,
419|it's almost purely beneficial. Multi-Head Spring is a high-risk bet—it destroys the most
420|elegant part of Theorem 1. If you can only add one: add PPE."*
421|
422|**This negative result was as valuable as any positive one.** It prevented months of
423|wasted implementation effort and identified a genuine open problem (the $\beta$-mixing
424|condition for physical attention heads).
425|
426|### 4.7 Three-Tier Architecture
427|
428|The audit results were formalized into a three-tier deployment architecture:
429|
430|| Tier | Components | Applicable Data | Compute |
431||------|-----------|----------------|---------|
432|| **Core** | State Crystallization + Spring + Yajie | No spatial structure (tabular, text) | Low |
433|| **Spatial** | Core + **Situs** | Spatial/sequential structure (proteins, materials, drug docking) | Medium |
434|| **Extended** | Spatial + Multi-Head Spring | Large-scale spatial ($N > 10^4$, sufficient $K_{\text{crit}}$) | High |
435|
436|The design philosophy: the original Yajie + Spring was built for the low-resource,
437|no-spatial-information scenario. Situs is an upgrade for data with natural spatial
438|structure. Adding Situs to non-spatial data wastes parameters; omitting Situs from
439|spatial data wastes information.
440|
441|---
442|
443|## Chapter 5: Spring — Self-Evolving Gating with Lyapunov Convergence
444|
445|### 5.1 The Curation-Exploration Problem
446|
447|Static noise detection (Yajie) answers: given a fixed dataset, which samples are noisy?
448|The dynamic problem is harder: given a stream of data and a model that improves over
449|time, how should we gate which samples to train on?
450|
451|This is the **curation-exploration tradeoff**. Curate too aggressively early, and the
452|model never sees diverse data; the gatekeeper's scores are based on an immature model
453|and systematically exclude valuable outliers. Explore too broadly, and noisy samples
454|degrade training; the model's own errors contaminate the gatekeeper's future judgments.
455|
456|The problem is circular: the gatekeeper $S_t$ determines what the student $f_{\theta_t}$
457|learns from, but the student's errors inform how the gatekeeper updates. This is a
458|coupled dynamical system with potential for vicious and virtuous cycles.
459|
460|### 5.2 The Spring Algorithm
461|
462|Spring (春季, "spring season") is named for resurrection: in nature, winter dormancy is
463|not death—plants re-bloom when conditions improve. In Spring, structures that fall below
464|the training threshold $\tau_{\text{keep}}$ are not deleted; they are stored dormant
465|in the memory bank $M_t$. When the gatekeeper $S_t$ improves, dormant structures are
466|re-scored, and those crossing the threshold are **resurrected** into training.
467|
468|The algorithm loop:
469|
470|1. **Judge**: $S_t$ scores incoming data $(x, y)$; all samples stored in $M_t$, never
471|   deleted
472|2. **Train**: Only samples with score $\geq \tau_{\text{keep}}$ train the NEP student
473|   $f_{\theta_t}$
474|3. **Update**: $\theta_{t+1}$ from student training; $S_{t+1}$ from gatekeeper update
475|   (seeing through student's eyes)
476|4. **Resurrect**: Re-score all dormant structures; those crossing $\tau_{\text{keep}}$
477|   are resurrected into training
478|
479|The tagline captures the philosophy: *"Winter does not kill—it waits for spring. Every
480|discarded structure carries the seed of its own resurrection."*
481|
482|### 5.3 The Mathematical Challenge
483|
484|The Spring paper's theoretical core—the Lyapunov convergence analysis—was developed on
485|June 28, 2026, in a concentrated burst that produced 12 files, approximately 4,900 lines
486|of mathematical derivation. The development was not linear:
487|
488|- **Files 01–05** (symbol system, dynamical system, online learning regret, Bayesian
489|  update, stochastic approximation) were the standard machinery—necessary, but not the
490|  contribution.
491|- **File 06** (fixed-point convergence) contains the central result: **Theorem SE-1**.
492|- **File 09** (verification report, 676 lines) is the most honest document in the
493|  repository: it catalogs **10 proof gaps** and **5 open problems** without
494|  minimization.
495|- **Files 10–12** (Lyapunov analysis, convergence rate, edge cases) were written
496|  *after* the verification report identified the gaps, closing the ones that could be
497|  closed and honestly labeling those that could not.
498|
499|### 5.4 Theorem SE-1: Almost-Sure Convergence
500|
501|