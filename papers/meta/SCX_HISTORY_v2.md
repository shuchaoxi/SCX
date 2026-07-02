64|
65|\section{The SCX Story: How a Gauge-Fixing Problem Became an Uncertainty
66|Principle}<!-- label: the-scx-story-how-a-gauge-fixing-problem-became-an-uncertainty-principle -->
67|
68|
> 69|A candid intellectual history of the State-Conditioned eXpertise
> 70|framework. Written from development logs, theorem drafts, adversarial
> 71|audits, and git history. No press release. No vision statement. Just
> 72|what happened and what we learned.
> 73|

74|
75|
<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

76|
77|\subsection{Preface: On Telling the Truth About
78|Research}<!-- label: preface-on-telling-the-truth-about-research -->
79|
80|Most papers lie about how they were written. The introduction presents a
81|clean logical arc from problem to solution, as if the author woke up one
82|morning with the theorems fully formed. The real history---the dead
83|ends, the bugs in the proofs, the concepts that took weeks to name, the
84|theorems that turned out to be corollaries of theorems we hadn't proven
85|yet---gets compressed into acknowledgments or erased entirely.
86|
87|This document is the opposite. It records what actually happened in the
88|development of the SCX framework between May and June 2026: a period in
89|which a practical problem in interatomic potential merging unfolded,
90|over roughly five weeks, into a mathematical framework spanning four
91|theorems, three core algorithms, a self-evolving gatekeeper with
92|Lyapunov convergence guarantees, and---unexpectedly---an uncertainty
93|principle for label noise detection.
94|
95|The author is a Ph.D.~student at Wuhan University. All theoretical work
96|was done on a personal computer at home, using AI coding tools (AI providers)
97|and DeepSeek API as implementation tools. The Xiaogan Supercomputing
98|Center was used exclusively for DFT calculations in the EGP project
99|(Papers 1--3), not for SCX development.
100|
101|We tell this story not because it is exceptional, but because it is
102|typical of how research actually works---and because the clean
103|narratives we publish in journals train students to expect a linear path
104|that does not exist.
105|
106|
<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

107|
108|\subsection{Chapter 1: Origins --- The EGP Gauge-Fixing
109|Problem}<!-- label: chapter-1-origins-the-egp-gauge-fixing-problem -->
110|
111|#### 1.1 The Practical Problem<!-- label: the-practical-problem -->
112|
113|In May 2026, the author was working on the EGP (Expert-Guided Potential)
114|project: constructing machine-learned interatomic potentials (MLIPs) for
115|III-nitride semiconductors (AlN, GaN, and eventually AlGaN) using the
116|Atomic Cluster Expansion (ACE) framework. The practical task was
117|straightforward: train separate ACE potentials on different chemical
118|domains, then merge them into a single multi-element potential.
119|
120|The appeal of this modular approach is obvious. A community could build
121|a library of specialized potentials---AlN trained by one group, GaN by
122|another, InN by a third---and combine them as needed without costly
123|joint retraining. The ACE framework's linear parameterization makes this
124|particularly natural: coefficients are just vectors, and vectors can be
125|averaged.
126|
127|\subsubsection{1.2 Why Direct Merging
128|Fails}<!-- label: why-direct-merging-fails -->
129|
130|It doesn't work. The naive merge---averaging the coefficient vectors of
131|independently trained experts---produces catastrophic errors: \(C_{33}\)
132|elastic constant deviations exceeding \(50\%\), formation energy sign
133|reversals, and force predictions worse than either expert individually.
134|
135|The failure is not a numerical accident. Four distinct sources of
136|inconsistency block safe merging:
137|
138|**(I1) Energy reference ambiguity.** Forces determine the potential
139|energy surface only up to an additive constant. Each expert's training
140|loss \({\mathcal{L}}_F\) (force RMSE) is invariant under
141|\(E \to E + C\), so the absolute energy zero is unconstrained. Two
142|experts trained on different domains end up with unrelated energy zeros,
143|producing spurious energy differences upon merging.
144|
145|**(I2) Species-shift misalignment.** The per-species constant
146|shifts \(b_Z\) absorb a significant fraction of the energy reference
147|ambiguity. When Expert A (AlN) assigns one shift to nitrogen and Expert
148|G (GaN) assigns another, the merged model inherits inconsistent shifts
149|that produce systematic formation energy errors.
150|
151|**(I3) Coefficient-level gauge freedom.** The shared-correction ACE
152|parameterization
153|\(E = \sum_i [{\mathbf{c}}_0 + {\mathbf{c}}_{Z_i}] \cdot {\mathbf{B}}({\mathbf{q}}_i) + b_{Z_i}\)
154|admits an exact gauge transformation:
155|\[{\mathbf{c}}_0 \to {\mathbf{c}}_0 + {\mathbf{g}}, \quad {\mathbf{c}}_Z \to {\mathbf{c}}_Z - {\mathbf{g}}\]
156|which leaves all physical predictions invariant for any vector
157|\({\mathbf{g}}\). Different experts explore different regions of this
158|gauge-equivalent space, making their coefficient vectors incompatible
159|for direct combination. The gauge violation in unconstrained
160|training---\(\lVert\sum_Z \pi_Z {\mathbf{c}}_Z\rVert\)---reaches
161|\(8.77\) in typical runs, confirming that the degeneracy is numerically
162|active.
163|
164|**(I4) Residual meaning incompatibility.** Domain-specific
165|corrections learned by each expert are meaningful only relative to their
166|own data distribution. Naively combining them can cancel or amplify
167|corrections in physically arbitrary ways.
168|
169|\subsubsection{1.3 The Gauge-Fixing
170|Solution}<!-- label: the-gauge-fixing-solution -->
171|
172|The first contribution of the EGP paper was a post-hoc gauge-fixing
173|procedure: after training each expert without constraints, apply the
174|orthogonal projection
175|\[{\mathbf{g}} = \sum_Z \pi_Z {\mathbf{c}}_Z, \quad {\mathbf{c}}_Z' = {\mathbf{c}}_Z - {\mathbf{g}}, \quad {\mathbf{c}}_0' = {\mathbf{c}}_0 + {\mathbf{g}}.\]
176|
177|This achieves exact gauge cancellation (residual \(4.6\times10^{-16}\),
178|machine precision) with zero change to physical predictions. The key
179|insight was *negative*: a soft penalty approach---adding
180|\(\lambda\lVert\sum_Z\pi_Z{\mathbf{c}}_Z\rVert^2\) to the training
181|loss---fundamentally fails. A systematic \(\lambda\)-sweep over six
182|orders of magnitude (\(10^{-3}\) to \(10^1\)) revealed that no
183|\(\lambda\) simultaneously achieves gauge violation below \(0.1\) and
184|accuracy degradation under \(20\%\). The gauge constraint subspace is
185|nearly orthogonal to the physical loss landscape; gradient descent
186|cannot simultaneously satisfy both.
187|
188|This negative result was more instructive than the positive one. It
189|established a principle that would recur throughout SCX development:
190|**consistency constraints must be applied post-hoc, not enforced
191|during optimization, when the constraint subspace is orthogonal to the
192|objective landscape.**
193|
194|\subsubsection{1.4 The Observation That Started
195|Everything}<!-- label: the-observation-that-started-everything -->
196|
197|During the EGP work, the author noticed a recurring phenomenon: the same
198|expert potential's prediction reliability varied dramatically across
199|different regions of configuration space. An AlN expert that achieved
200|\(0.047\) eV/Å force RMSE globally would show \(0.012\) eV/Å on bulk
201|equilibrium structures but \(0.15\) eV/Å on defect configurations and
202|\(0.30\) eV/Å on thermal snapshots far from the training distribution.
203|
204|This observation---that **expert reliability is not a global
205|constant but a state-conditioned quantity**---was the seed from which
206|everything else grew. It was not a theoretical insight. It was an
207|empirical nuisance that kept showing up in the data.
208|
209|
<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

210|
211|\subsection{Chapter 2: State Crystallization --- Naming the Third Core
212|Algorithm}<!-- label: chapter-2-state-crystallization-naming-the-third-core-algorithm -->
213|
214|\subsubsection{2.1 From ``PBE Operation'' to a
215|Concept}<!-- label: from-pbe-operation-to-a-concept -->
216|
217|For several weeks, a fundamental operation in the SCX pipeline existed
218|without a name. It was referred to as ``the PBE operation'' or ``Layer 2
219|discretization of the two-layer descriptor''---descriptions of
220|implementation, not of concept. The operation itself was clear: use PBE
221|(Perdew-Burke-Ernzerhof) DFT calculations to discover natural clustering
222|boundaries in continuous physical quantities (bond angles, bond lengths,
223|coordination numbers), producing discrete state atoms. But calling it
224|``the PBE operation'' was like calling a car ``the internal combustion
225|operation.''
226|
227|On June 29, 2026, in a discussion with the AI coding tools agent (designated
228|``Hermes'' in development logs), the concept was formally named
229|**State Crystallization**.
230|
231|#### 2.2 Why ``Crystallization''<!-- label: why-crystallization -->
232|
233|The metaphor is precise. In physical crystallization, a continuous
234|disordered phase (liquid/solution) spontaneously develops discrete
235|ordered structure (crystal), with boundaries determined by intrinsic
236|thermodynamic laws, not by human cutting. In State Crystallization,
237|continuous physical quantities (bond angles 109.5°, bond lengths 1.46 Å)
238|spontaneously cluster into discrete state atoms, with boundaries
239|determined by the PBE energy surface, not by statistical frequency or
240|human naming conventions.
241|
242|The naming resolved a longstanding semantic confusion. ``PBE operation''
243|described the tool. ``Two-layer descriptor Layer 2 discretization''
244|described the mechanical step. Neither captured the ontological claim:
245|**states are discovered, not defined.**
246|
247|\subsubsection{2.3 State Crystallization ≠
248|BPE}<!-- label: state-crystallization-bpe -->
249|
250|The natural LLM analogue is Byte Pair Encoding (BPE), which also
251|produces discrete tokens from a less-structured input. But the analogy
252|is instructive precisely because it breaks:
253|
254|\begin{longtable}[]{@{}
255|  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2895}}
256|  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.5789}}
257|  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.1316}}@{}}
258|\toprule\noalign{}
259|\begin{minipage}[b]
260|Dimension
261|\end{minipage} & \begin{minipage}[b]
262|State Crystallization
263|\end{minipage} & \begin{minipage}[b]
264|BPE
265|\end{minipage} 

266|\midrule\noalign{}
267|\endhead
268|\bottomrule\noalign{}
269|\endlastfoot
270|Input & Continuous physical quantities & Discrete symbol sequences 

271|Boundary criterion & Physical reality (PBE energy surface) & Statistical
272|frequency 

273|Ontology & **Discovers** natural state boundaries &
274|**Conventions** for cutting 

275|Mathematical form & \(\mathcal{D}_{phys}\) &
276|\(\mathcal{D}_{freq}\) 

277|Anchor & Physical ground truth (verifiable) & None (statistical
278|construct) 

279|\end{longtable}
280|
281|The formal relationship is inclusion: BPE is the degenerate limit of
282|State Crystallization when physical coupling approximates frequency
283|coupling. In this limit,
284|\(\mathcal{D}_{freq} \approx \mathcal{D}_{phys}\), but the
285|converse is not true---State Crystallization can handle continuous
286|physical quantities that BPE cannot even represent.
287|
288|This relationship is not merely taxonomic. It identifies what SCX does
289|that LLMs cannot: anchor state definitions in physical reality rather
290|than statistical convention. A bond angle of 109.5° is sp\(^3\)
291|hybridization regardless of how frequently it co-occurs with other
292|features in a training corpus.
293|
294|#### 2.4 Architectural Position<!-- label: architectural-position -->
295|
296|State Crystallization was established as the **third core
297|algorithm** of SCX, completing a layered architecture:
298|
299|\begin{longtable}[]{@{}
300|  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1707}}
301|  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2683}}
302|  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2439}}
303|  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3171}}@{}}
304|\toprule\noalign{}
305|\begin{minipage}[b]
306|Layer
307|\end{minipage} & \begin{minipage}[b]
308|Algorithm
309|\end{minipage} & \begin{minipage}[b]
310|Function
311|\end{minipage} & \begin{minipage}[b]
312|LLM Analogue
313|\end{minipage} 

314|\midrule\noalign{}
315|\endhead
316|\bottomrule\noalign{}
317|\endlastfoot
318|State Ontology & **State Crystallization** & Continuous → discrete
319|state atoms & BPE (but physics-driven) 

320|State Topology & **Situs** & Positional encoding of states in
321|physical space & Positional Encoding 

322|State Evolution & **Spring** & Self-evolving gating, state-atom
323|interactions & Transformer (Self-Attention) 

324|Audit Output & **Yajie** & Verification + audit + evidence chain &
325|--- (no LLM audit layer) 

326|Evaluation & **Cercis Score** & \(S = Q + \eta N\) & --- 

327|\end{longtable}
328|
329|The architecture reveals a structural gap in LLM design: LLMs have no
330|state ontology layer. Their tokens are statistical constructs with no
331|physical anchor. Yajie is more honest than an LLM not because its
332|mathematics is better, but because it audits on a physically real state
333|space, not a statistically constructed one.
334|
335|
<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

336|
337|\subsection{Chapter 3: Yajie --- Four Theorems on Label
338|Noise}<!-- label: chapter-3-yajie-four-theorems-on-label-noise -->
339|
340|#### 3.1 The Core Insight<!-- label: the-core-insight -->
341|
342|Between June 23--27, 2026, the observation that ``expert reliability
343|varies by configurational region'' was formalized into a mathematical
344|framework. The central definition:
345|
346|\[{SCX}_m(s) = P(\ell(f_m(x), y) < \tau \mid x \in s)\]
347|
348|Data value is not an intrinsic property of a sample. It is a conditional
349|quantity determined by the state \(s\), the expert's reliability
350|\({SCX}_m(s)\), and the current model's deficiencies---jointly.
351|
352|This is the insight that separates SCX from all prior work on data
353|valuation, active learning, and noise detection. Prior methods assign
354|global scores to samples. SCX assigns state-conditioned scores to
355|experts on samples. The distinction is not a refinement---it is a
356|different category of question.
357|
358|\subsubsection{3.2 Theorem 1: Consensus-Based Noise
359|Detection}<!-- label: theorem-1-consensus-based-noise-detection -->
360|
361|**Statement (informal).** Let \(M\) independently trained experts
362|vote on the correctness of a label for a sample in state \(s\). If the
363|experts are conditionally independent given the true function, then the
364|probability that a noisy label survives consensus screening decays
365|exponentially in \(M\):
366|
367|\[P(noise survives \mid {consensus}) \leq \exp(-2M\Delta_s^2)\]
368|
369|where \(\Delta_s = {SCX}(s) - 0.5\) is the expert reliability
370|advantage over random guessing in state \(s\).
371|
372|**Tools.** Chernoff bound + Hoeffding inequality, under assumptions
373|A1--A6 (conditional independence, bounded loss, state-conditional
374|calibration).
375|
376|**What it means.** Even a modest number of independent experts
377|(\(M \sim 5\)--\(10\)) can drive false-acceptance rates below
378|practically meaningful thresholds. The guarantee is exponential, not
379|asymptotic.
380|
381|**Bugs found and fixed.** Lemma 3 was restructured after an
382|adversarial audit revealed a missing assumption (A6: expert errors are
383|sub-Gaussian with state-conditional variance bound). The Chernoff KL
384|direction was corrected (the original proof minimized the wrong
385|divergence). These were not typographical errors---they were logical
386|gaps that would have been caught in review, but the adversarial audit
387|caught them first.
388|
389|\subsubsection{3.3 Theorem 2: Weak Feature Failure Lower
390|Bound}<!-- label: theorem-2-weak-feature-failure-lower-bound -->
391|
392|**Statement (informal).** If every feature \(X_j\) in state \(s\)
393|has mutual information with the label error below a threshold
394|\(\delta\), i.e., \(I(X_j; L) < \delta\) for all \(j\), then any noise
395|detector---not just SCX---has AUC bounded by:
396|
397|\[{AUC} \leq 0.5 + \epsilon(\delta, |s|)\]
398|
399|where \(\epsilon \to 0\) as \(\delta \to 0\).
400|
401|**Tools.** Fano inequality, information-theoretic lower bounds on
402|detection.
403|
404|**What it means.** SCX does not work everywhere. When features are
405|genuinely uninformative, no method works. This is not a weakness of
406|SCX---it is a fundamental limit of information theory. Theorem 2
407|provides the diagnostic: compute \(I(X_j; L)\) for each feature in each
408|state; states where all features fall below \(\delta\) are states where
409|SCX should not be deployed.
410|
411|**Bugs found and fixed.** The original proof claimed optimality of
412|\(k\)-means clustering, which is false (k-means is NP-hard; no
413|polynomial algorithm can guarantee optimal clustering). This claim was
414|removed. The AUC \(\eta\)-dependence was clarified: the bound depends on
415|the gap between the null and alternative distributions, not on the
416|absolute AUC level. A cluster balance qualifier was added (the bound
417|degrades when state populations are highly imbalanced).
418|
419|\subsubsection{3.4 Theorem 3: The Unidentifiability of Noise and
420|Difficulty}<!-- label: theorem-3-the-unidentifiability-of-noise-and-difficulty -->
421|
422|**Statement (informal).** There exist two worlds---World A (noisy
423|labels) and World B (hard-but-clean labels)---that produce identical
424|observable data distributions. No algorithm can distinguish them from
425|observations alone.
426|
427|**Proof structure.** Constructive two-world proof. In both worlds,
428|the joint distribution \(P(X, Y)\) is identical. In World A, label noise
429|generates the errors. In World B, genuine aleatoric uncertainty
430|(inherently difficult samples) generates identical error patterns. The
431|likelihood ratio is 1 for all possible observations, so no statistical
432|test has power exceeding the test's significance level.
433|
434|**What it means.** There is a **hard boundary** on what data
435|cleaning can achieve. Past this boundary, labeling errors and genuinely
436|difficult cases are observationally equivalent. Any algorithm that
437|claims to clean data beyond this boundary is either making unfalsifiable
438|claims or silently degrading into a relabeling engine---replacing one
439|set of labels with another that better matches its own inductive biases.
440|
441|This is SCX's uncertainty principle. Just as Heisenberg's principle is
442|not a measurement deficiency but a statement about what can be known in
443|principle, Theorem 3 is not an algorithmic limitation but a statement
444|about what can be distinguished from data alone.
445|
446|**We discuss Theorem 3's independence and standalone significance
447|in Chapter 8.**
448|
449|\subsubsection{3.5 Theorem 4: Minimax
450|Optimality}<!-- label: theorem-4-minimax-optimality -->
451|
452|**Statement (informal).** SCX's adaptive threshold achieves the
453|exact minimax optimal rate for noise detection. No algorithm can achieve
454|a better worst-case false-positive / false-negative tradeoff.
455|
456|**Tools.** Bahadur-Rao refinement of the Chernoff bound (exact
457|exponential rate, not just asymptotic), combined with Chernoff-Stein
458|lemma for the composite hypothesis testing problem.
459|
460|**What it means.** Theorem 1 says SCX works well. Theorem 4 says no
461|algorithm can work better in the worst case. Together they establish SCX
462|as the optimal solution to a well-defined problem, not merely one
463|heuristic among many.
464|
465|\subsubsection{\texorpdfstring{3.6 The Cercis Score:
466|\(S = Q + \eta N\)}{3.6 The Cercis Score: S = Q + \ eta N}}<!-- label: the-cercis-score-s-q-eta-n -->
467|
468|The Yajie audit engine evaluates every state-conditioned (configuration,
469|label) pair using the Cercis Score:
470|
471|\[S(s) = Q(s) + \eta(t) \cdot N(s)\]
472|
473|where: - \(Q(s)\) is the **quality** component:
474|\(1 - \overline{residual}\) across experts - \(N(s)\) is the
475|**noise** component: density-weighted + consistency-weighted
476|residual - \(\eta(t)\) is the **exploration schedule**:
477|\(\eta(0) \gg 1\), \(\eta(t) \to 0\) as \(t \to \infty\)
478|
479|The Cercis Score is named after *Cercis chinensis* (紫荆), a
480|cauliflorous tree whose flowers bloom directly from old branches. The
481|metaphor: knowledge flowers from accumulated experience (the memory
482|bank), not from new data alone. The exploration term \(\eta(t) N(s)\)
483|ensures early-stage openness to discovery; its decay ensures late-stage
484|convergence to a stable quality ranking.
485|
486|#### 3.7 What Yajie Does Not Do<!-- label: what-yajie-does-not-do -->
487|
488|The name ``Yajie'' (雅洁) means ``elegant purification'' in Chinese. But
489|the algorithm does not purify data. It **audits** data---it
490|identifies which samples are clean, which are noisy, and (critically)
491|which are **ambiguous**: samples where Theorem 3's uncertainty
492|principle applies and no determination is possible.
493|
494|The three-way classification---clean / noisy / ambiguous---is not a
495|compromise. It is the mathematically honest output. Binary clean/noisy
496|classifiers are lying about Theorem 3.
497|
498|
<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

499|
500|\subsection{Chapter 4: Situs --- From Audit to Independent
501|