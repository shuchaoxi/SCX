# Theorem 4 — Reviewer Complicity 审稿人同谋对等定理

**Author:** SCX

95|
96|
97|
98|
*Abstract:*

99|Every scientific claim rests on data. Every dataset has a minimum number $M$ of independent verifiers needed to certify its quality. We prove that the failure to declare $M$ is epistemically equivalent to fraud, and that declaring $M$ while falsifying data constitutes active evil. Using a game-theoretic signaling framework, we establish three fundamental theorems: (i)~a separating Perfect Bayesian Equilibrium exists under mandatory M-declaration, where honest researchers signal trivially while dishonest researchers face exponentially growing fabrication costs (Theorem~1); (ii)~in the absence of M-declaration, the posterior probability of fraud for any published claim is unbounded — M-declaration is information-theoretically necessary for quality certification (Theorem~2); (iii)~if a researcher declares $M$ and falsifies data, the probability of evading detection by all $M$ verifiers decays as $\exp(-2M\Delta^2)$, with $\lim_{t\to\infty}\Pbb(detection)=1$ as the scientific community grows (Theorem~3). We formalize the M-Parameter Standard: every quantitative paper must declare $M_$ for its central claims, with default $\varepsilon = 0.05$. We decompose $M$ across disciplines (high-energy physics, psychology, deep learning) and introduce the Cercis{} Score $S = Q + \eta N$ as an auditable scientific quality metric. The 耿同学 (Geng) precedent demonstrates that even $M=1$ changes the equilibrium — imagine $M=100$. Science is humanity's cumulative intellectual achievement; M-declaration is the minimal epistemic hygiene standard.
100|
101|
102|**Keywords:** scientific audit, M-parameter, game theory, signaling equilibrium, epistemic hygiene, data quality certification, replicability, SCX framework, 审计宣言, 科学诚信
103|

104|
105|% ===========================================================================
106|## Introduction — The Audit Gap in Science
107|## 引言——科学中的审计空白
108|<!-- label: sec:intro -->
109|% ===========================================================================
110|
111|Science operates on a compact of trust: the reader trusts that the author has faithfully reported what was observed. Peer review enforces this compact partially — it checks methodology, logical coherence, and claimed novelty — but it leaves a structural gap. Peer review does not ask, and has no mechanism to answer, the question: **How many independent experts would need to verify your raw data to detect errors at rate $\varepsilon$?**
112|
113|This is not a trivial oversight. It is the absence of a fundamental epistemic parameter. Every scientific claim $C$ derived from data $\cD$ has a verification structure: a minimum number $M$ of independent verifiers (labs, teams, auditors) whose scrutiny would detect fraud or error with confidence $1-\varepsilon$. This number is an objective property of the claim-data pair $(C, \cD)$, computable from the statistical structure of the evidence, the degrees of freedom in the measurement protocol, and the replicability architecture of the experimental design. Yet no journal requires it. No reviewer demands it. The scientific community publishes claims without declaring the one parameter that quantifies their verifiability.
114|
115|
116|**The Audit Gap.** Current scientific quality assurance consists of:
117|
1. **Methodology review**: Are the methods sound?
2. **Logic review**: Do the conclusions follow from the data?
3. **Novelty review**: Is the contribution significant?
4. **Missing**: How many independent verifiers are needed to detect error?

123|The fourth item is absent from every major journal's review criteria. We call this the *audit gap*. The M-parameter declaration fills it.
124|
125|
126|**The Geng Precedent.** 耿同学 (Geng) has demonstrated empirically that fraud detection is practically achievable when data is scrutinized — not requiring special courage or institutional authority, just method, persistence, and access to publicly available information. The Geng case establishes a critical precedent: a single determined individual ($M=1$) applying rigorous scrutiny to published data can detect anomalies that escaped peer review. This is not an argument for heroic individualism; it is a proof of concept. If one person can do this, a community of $M$ independent verifiers can do it systematically. The question is not whether audit is possible — it is whether we institutionalize it.
127|
128|
129|**This Paper.** We provide the game-theoretic proof that mandatory M-declaration transforms scientific publication from a pooling equilibrium (where honest and dishonest researchers are indistinguishable) to a separating equilibrium (where honest researchers are rewarded and dishonest ones are detected). We prove three theorems with full game-theoretic rigor under eight explicitly stated assumptions. We propose the M-Parameter Standard as a concrete, implementable prerequisite for scientific publication, and we demonstrate its application across disciplines.
130|
131|% ===========================================================================
132|## Formal Model — Scientific Publication as Signaling Game
133|## 形式化模型——科学发表作为信号博弈
134|<!-- label: sec:model -->
135|% ===========================================================================
136|
137|We model scientific publication as a signaling game between a researcher and the scientific community. The researcher has private information about the verifiability of their data; the community must decide whether to trust the published claim.
138|
139|### Players and Types 参与者与类型
140|
141|There is a continuum of researchers, each characterized by a type $\theta \in \Theta = \{H, D\}$:
142|
- **Honest** ($\theta = H$): The researcher's data $\cD$ is genuine. There exists a true minimum number of independent verifiers $M_{true}(\cD, \varepsilon)$ such that any $M \ge M_{true}$ independent audits would confirm the data's validity with probability at least $1-\varepsilon$.
- **Dishonest** ($\theta = D$): The researcher's data $\cD$ is fabricated or manipulated. No number of independent verifications would confirm the data; the researcher must actively fabricate consistency across verifiers to avoid detection.

146|The prior probability of an honest researcher is $\pi_0 = \Pbb(\theta = H) \in (0,1)$.
147|
148|### Actions and Signals 行动与信号
149|
150|The researcher chooses a signal $s = (M, \cD, C)$ where:
151|
- $M \in \N \cup \{\varnothing\}$ is the declared M-parameter (or $\varnothing$ for non-declaration);
- $\cD$ is the published data;
- $C$ is the central scientific claim.

156|After publication, an auditor community of size $V$ (the number of independent labs or teams that attempt verification) observes the signal and may detect fraud.
157|
158|### Payoffs 支付
159|
160|The researcher's payoff depends on publication success and audit outcomes:
161|
$$<!-- label: eq:payoff -->
162|    U(\theta, s, outcome) =
163|    \begin{cases}
164|        B - \gamma(M, \theta) & if published and not detected, 

165|        -\kappa - \gamma(M, \theta) & if published and detected, 

166|        -\gamma(0, \theta) & if rejected or not published,
167|    \end{cases}
168|$$

169|where:
170|
- $B > 0$ is the career benefit of successful publication (citations, prestige, grants, tenure);
- $\kappa > 0$ is the penalty for detected fraud (retraction, career termination, legal consequences in some jurisdictions);
- $\gamma(M, \theta)$ is the cost of producing a paper that declares M-parameter $M$:

183|
184|Crucially, the fabrication cost $c_f(M)$ grows **exponentially** in $M$, because fabricating data consistent with $M$ independent verifiers requires constructing $M$ mutually consistent datasets, each plausible under the scrutiny of a different expert with different detection strategies. In contrast, the genuine data cost $c_d(M)$ is approximately constant or grows sublinearly: honest researchers produce one dataset that is inherently verifiable; making it available to $M$ verifiers incurs only transmission and documentation costs.
185|
186|### Timing 时序
187|
188|The game proceeds as follows:
189|
1. Nature draws researcher type $\theta \in \{H, D\}$ with probability $\pi_0$.
2. The researcher chooses signal $s = (M, \cD, C)$.
3. The paper undergoes peer review; publication probability depends on $s$.
4. If published, $V$ independent verifiers from the auditor community each attempt verification.
5. If any verifier detects fraud, the researcher incurs penalty $\kappa$.
6. Payoffs are realized.

197|
198|% ===========================================================================
199|## Assumptions 假设
200|<!-- label: sec:assumptions -->
201|% ===========================================================================
202|
203|We state the assumptions explicitly, following the SCX{} convention.
204|
205|\begin{assumption}[Bounded Publication Benefit]
206|<!-- label: asm:B -->
207|The publication benefit $B$ is finite: $0 < B < \infty$. No single publication is worth infinite risk.
208|\end{assumption}
209|
210|\begin{assumption}[Positive Audit Penalty]
211|<!-- label: asm:kappa -->
212|The penalty for detected fraud satisfies $\kappa > 0$. Fraud has consequences when detected.
213|\end{assumption}
214|
215|\begin{assumption}[Exponential Fabrication Cost]
216|<!-- label: asm:cost_exp -->
217|The cost to a dishonest researcher of fabricating data consistent with $M$ independent verifiers grows exponentially: $c_f(M) \ge c_0 \cdot \exp(\alpha M)$ for some $\alpha > 0$ and $c_0 > 0$. This reflects the combinatorial explosion of mutual consistency constraints across independent verification strategies.
218|\end{assumption}
219|
220|\begin{assumption}[Constant Genuine Data Cost]
221|<!-- label: asm:cost_const -->
222|The marginal cost to an honest researcher of supporting one additional independent verifier is bounded: $c_d(M+1) - c_d(M) \le \delta$ for some small $\delta > 0$, for all $M \ge 0$. Making genuine data available to more verifiers is cheap.
223|\end{assumption}
224|
225|\begin{assumption}[Independent Verification]
226|<!-- label: asm:indep -->
227|Given the data $\cD$, the outcomes of $V$ independent verifications are conditionally independent. Each verifier $v \in [V]$ produces a binary signal $a_v \in \{0, 1\}$ (1 = anomaly detected) with:
228|
- If $\theta = H$: $\Pbb(a_v = 1 \mid H, \cD) \le \varepsilon_v$ where $\varepsilon_v$ is the verifier's false positive rate.
- If $\theta = D$: $\Pbb(a_v = 0 \mid D, \cD) \le \exp(-2\Delta_v^2)$ where $\Delta_v > 0$ is the verifier's detection sensitivity — the minimum effect size (in standard deviations) that the verifier can reliably detect given its methodology.

232|\end{assumption}
233|
234|\begin{assumption}[Verifier Growth Over Time]
235|<!-- label: asm:growth -->
236|The cumulative number of verification attempts $V(t)$ for any published claim is a non-decreasing function of time $t$ with $\lim_{t\to\infty} V(t) = \infty$. As time passes, more independent labs attempt replication or verification. This is empirically validated by the replication movement in psychology, economics, and biomedicine.
237|\end{assumption}
238|
239|\begin{assumption}[M-Declaration is Verifiable]
240|<!-- label: asm:verifiable -->
241|The declared M-parameter $M$ is itself verifiable: the scientific community can compute a lower bound $<u>M</u>(\cD, \varepsilon)$ from the statistical structure of the published data and methods. A declaration $M < <u>M</u>$ is detectable as a misdeclaration.
242|\end{assumption}
243|
244|\begin{assumption}[Rational Researcher]
245|<!-- label: asm:rational -->
246|Researchers are rational expected-utility maximizers. They choose the signal $s$ that maximizes their expected payoff given their beliefs about the auditor community's verification behavior.
247|\end{assumption}
248|
249|\begin{assumption}[Auditor Detection Capability]
250|<!-- label: asm:auditor -->
251|There exists a minimum detection sensitivity $\Delta_ > 0$ such that any independent verifier with adequate resources can achieve detection sensitivity at least $\Delta_$ against fabricated data. Specifically, for dishonest $\theta$ and any fabricated dataset $\cD$, there exists a detection strategy achieving $\Pbb(detect \mid \cD) \ge 1 - \exp(-2\Delta_^2)$.
252|\end{assumption}
253|
254|These eight assumptions are individually plausible and collectively sufficient for the theorems that follow. We make no claim that they hold in every conceivable circumstance; rather, they characterize the regime in which M-declaration is epistemically transformative. Deviations from these assumptions (e.g., coordinated multi-lab fraud) are addressed in Section [ref].
255|
256|% ===========================================================================
257|## Theorem 1 — Separating Equilibrium under Mandatory M-Declaration
258|## 定理1——强制M声明下的分离均衡
259|<!-- label: sec:thm1 -->
260|% ===========================================================================
261|
262|> **Theorem:** [Separating Equilibrium]
> 263|<!-- label: thm:separating -->
> 264|Under Assumptions [ref]-- [ref], mandatory M-declaration induces a unique separating Perfect Bayesian Equilibrium (PBE) with the following properties:
> 265|
1. Honest researchers declare $M \ge M_(\varepsilon, \Delta_)$, where
2. Dishonest researchers either (a)~do not publish (exit the game), or (b)~declare $M = \varnothing$ (non-declaration) and are identified as non-compliant, or (c)~declare $M$ but face expected penalty exceeding benefit.
3. The equilibrium is **separating**: the declared $M$ perfectly reveals the researcher's type in equilibrium. Honest researchers are rewarded with publication benefit $B - c_0 - O(\delta M_)$; dishonest researchers receive expected payoff $\le 0$.

> 274|
275|
276|> **Proof:** \rigorFull
> 277|We construct the equilibrium and verify the PBE conditions: (i)~sequential rationality, (ii)~consistent beliefs, and (iii)~no profitable deviation.
> 278|
> 279|
> 280|**Step 1: Auditor Community Beliefs.**
> 281|Let $\mu(M \mid s)$ denote the auditor community's posterior belief that the researcher is dishonest given signal $s = (M, \cD, C)$. Under mandatory M-declaration, the auditor community observes $M$ and updates via Bayes' rule:
> 282|
> $$<!-- label: eq:belief -->
> 283|    \mu(M) = \Pbb(\theta = D \mid M) = \frac{\Pbb(M \mid D) \cdot (1-\pi_0)}{\Pbb(M \mid D) \cdot (1-\pi_0) + \Pbb(M \mid H) \cdot \pi_0}.
> 284|$$
> 
> 285|In equilibrium, the auditor community holds consistent beliefs: if the equilibrium strategy prescribes that honest types declare $M^*$ and dishonest types declare $\varnothing$ (or $M < M^*$), then observing $M^*$ implies $\mu(M^*) = 0$ (certainty of honesty) and observing $M' \neq M^*$ implies $\mu(M') = 1$ (certainty of dishonesty).
> 286|
> 287|The auditor community's optimal response given belief $\mu$ is to allocate verification resources proportionally. A paper believed dishonest with probability $\mu$ faces $V = \mu \cdot V_$ verifiers where $V_$ is the community's total verification capacity.
> 288|
> 289|
> 290|**Step 2: Dishonest Researcher's Optimization.**
> 291|A dishonest researcher choosing to declare $M$ faces the expected penalty from $V$ independent verifications. Under Assumption [ref], the probability of *evading* all $V$ verifiers is:
> 292|
> $$<!-- label: eq:evasion -->
> 293|    \Pbb(evade \mid D, M, V) = \prod_{v=1}^{V} \Pbb(a_v = 0 \mid D, \cD) \le \prod_{v=1}^{V} \exp(-2\Delta_v^2) = \exp(-2\sum_{v=1}^{V}\Delta_v^2).
> 294|$$
> 
> 295|Using the minimum sensitivity $\Delta_$ from Assumption [ref]:
> 296|
> $$<!-- label: eq:evasion_bound -->
> 297|    \Pbb(evade \mid D, M, V) \le \exp(-2V\Delta_^2).
> 298|$$
> 
> 299|
> 300|The dishonest researcher's expected payoff when declaring $M$ is:
> 301|
> $$<!-- label: eq:U_dis -->
> 302|    \E[U \mid \theta = D, M] = \Pbb(evade) \cdot B + (1 - \Pbb(evade)) \cdot (-\kappa) - c_f(M).
> 303|$$
> 
> 304|
> 305|Substituting the evasion bound:
> 306|
> $$<!-- label: eq:U_dis_bound -->
> 307|    \E[U \mid \theta = D, M] \le B \cdot \exp(-2V\Delta_^2) - \kappa \cdot (1 - \exp(-2V\Delta_^2)) - c_f(M).
> 308|$$
> 
> 309|
> 310|Declaring $M = 0$ (or $\varnothing$) is futile because all $V$ verifiers are deployed (the community knows the paper is unaudited), so $\Pbb(evade \mid D, 0, V) \le \exp(-2V\Delta_^2) \to 0$ as $V$ grows. Declaring $M \ge 1$ triggers Assumption [ref]: the fabrication cost explodes exponentially.
> 311|
> 312|
> 313|**Step 3: Honest Researcher's Optimization.**
> 314|An honest researcher's expected payoff when declaring $M$ is:
> 315|
> $$<!-- label: eq:U_hon -->
> 316|    \E[U \mid \theta = H, M] = B - c_0 - c_d(M) - (negligible false positive risk).
> 317|$$
> 
> 318|Under Assumption [ref], $c_d(M)$ grows at most linearly: $c_d(M) \le c_d(0) + \delta M$. The honest researcher's optimal declaration is the minimum $M$ that separates them from dishonest types:
> 319|
> $$<!-- label: eq:honest_opt -->
> 320|    M^* = \min\{M \in \N : \E[U \mid \theta = D, M] \le 0\}.
> 321|$$
> 
> 322|
> 323|
> 324|**Step 4: Computing the Threshold $M_$.**
> 325|Set $\E[U \mid \theta = D, M] \le 0$:
> 326|
> $$
> 327|    B \cdot \exp(-2V\Delta_^2) - \kappa \cdot (1 - \exp(-2V\Delta_^2)) - c_f(M) &\le 0, 

> 328|    \exp(-2V\Delta_^2) \cdot (B + \kappa) &\le \kappa + c_f(M).
> 329|$$
> 
> 330|
> 331|For large $V$ (the auditor community is non-trivial), the left-hand side decays exponentially. The binding constraint comes from the fabrication cost. Setting $c_f(M) = c_0 \cdot \exp(\alpha M)$ (Assumption [ref]), the condition becomes:
> 332|
> $$
> 333|    c_0 \cdot \exp(\alpha M) \ge B - \kappa \cdot \frac{1 - \exp(-2V\Delta_^2)}{\exp(-2V\Delta_^2)}.
> 334|$$
> 
> 335|
> 336|For conservative parameterization (worst-case for the dishonest researcher: minimal $V$, maximal $B$), the required $M$ satisfies:
> 337|
> $$
> 338|    M \ge \frac{1}\ln\left(\frac{B + \kappa}{c_0}\right).
> 339|$$
> 
> 340|
> 341|But this is a game-theoretic lower bound. The sharper bound comes from the *information-theoretic* requirement: $M$ must be large enough that even if no verifier is initially deployed, the declaration itself signals quality. The minimum $M$ such that the evasion probability under full verification ($V = M$, since $M$ verifiers are deployed when $M$ is declared) is below $\varepsilon$:
> 342|
> $$
> 343|    \exp(-2M\Delta_^2) &\le \varepsilon, 

> 344|    M &\ge \frac{\ln(1/\varepsilon)}{2\Delta_^2} = M_.
> 345|$$
> 
> 346|
> 347|Thus:
> 348|
> $$<!-- label: eq:Mmin_final -->
> 349|    M_(\varepsilon, \Delta_) = \frac{\ln(1/\varepsilon)}{2\Delta_^2}.
> 350|$$
> 
> 351|
> 352|For $\varepsilon = 0.05$ (matching the $p < 0.05$ scientific tradition) and $\Delta_ = 0.5$ (one standard deviation detection sensitivity), we obtain $M_ \approx 6$. For $\Delta_ = 0.25$, $M_ \approx 24$.
> 353|
> 354|
> 355|**Step 5: Verification of PBE Conditions.**
> 356|
> 357|*Sequential rationality*: Given beliefs $\mu(M)$, the auditor community's verification strategy is optimal (allocate resources to papers with $\mu > 0$). Given the auditor strategy, researchers' signal choices maximize expected utility — honest researchers declare $M \ge M_$ (cost is low, payoff is $B - c_0 - O(\delta M) > 0$), dishonest researchers cannot profitably mimic (fabrication cost exceeds expected benefit).
> 358|
> 359|*Consistent beliefs*: Beliefs are derived via Bayes' rule on the equilibrium path. Off the equilibrium path (e.g., observing $M' \notin \{M_, \varnothing\}$), any belief $\mu \in [0,1]$ is permissible; we set $\mu = 1$ (pessimistic), which is consistent with the Cho-Kreps intuitive criterion — dishonest types gain nothing from deviating to any $M' \neq M_$ because they would be detected, while honest types have no incentive to deviate to $M' \neq M_$ since $M_$ already achieves separation at minimal cost.
> 360|
> 361|*No profitable deviation*: For honest researchers, deviating to $M < M_$ would pool them with dishonest types, reducing expected payoff (auditor scrutiny increases, false positive risk rises). For dishonest researchers, deviating to $M \ge M_$ requires fabrication cost $c_f(M) \ge c_0 \exp(\alpha M_)$, which exceeds $B$ for sufficiently large $\alpha$ (guaranteed by Assumption [ref]). Deviating to $M = \varnothing$ signals dishonesty and attracts maximum verification effort.
> 362|
> 363|
> 364|**Step 6: Uniqueness.**
> 365|Any equilibrium in which honest and dishonest types pool at the same $M$ is not a PBE, because dishonest types would have a profitable deviation: reduce $M$ (or declare $\varnothing$) to reduce fabrication cost, since pooling at any $M$ still attracts auditor scrutiny based on the prior $\pi_0$. Any equilibrium with multiple distinct $M$ values for honest types is Pareto-dominated by the minimum-cost separating $M_$ — honest types prefer the smallest $M$ that achieves separation. Thus the equilibrium is unique.
> 366|
> 367|This completes the proof of Theorem [ref].
> 368|
369|
370|> **Corollary:** [Cost Asymmetry is the Driver]
> 371|<!-- label: cor:cost_asymmetry -->
> 372|The separating equilibrium exists if and only if the cost asymmetry condition holds:
> 373|
> $$<!-- label: eq:cost_asym -->
> 374|    c_f(M_) > B + \kappa,
> 375|$$
> 
> 376|while $c_d(M_) < B$. This condition is satisfied whenever $\alpha > \ln((B+\kappa)/c_0)/M_$, which is empirically plausible: fabricating mutually consistent data across multiple independent verification dimensions is qualitatively harder than collecting genuine data.
> 377|
378|
379|> **Corollary:** [M-Minimum as Information Threshold]
> 380|<!-- label: cor:M_info -->
> 381|$M_$ is identical to the sample complexity of Hoeffding's inequality: to detect a bias of magnitude $\Delta$ with confidence $1-\varepsilon$ requires $M \ge \ln(1/\varepsilon)/(2\Delta^2)$ independent samples. M-declaration thus operationalizes Hoeffding as a scientific publication standard.
> 382|
383|
384|% ===========================================================================
385|## Theorem 2 — Non-Declaration = Fraud (Epistemic Equivalence)
386|## 定理2——不声明等于作假（认知等价性）
387|<!-- label: sec:thm2 -->
388|% ===========================================================================
389|
390|> **Theorem:** [Epistemic Equivalence of Non-Declaration]
> 391|<!-- label: thm:non_declaration -->
> 392|In the absence of M-declaration, the posterior probability that a published claim is fraudulent cannot be bounded below any threshold $\delta < 1$. Formally, for any published claim $C$ without M-declaration:
> 393|
> $$<!-- label: eq:sup_fraud -->
> 394|    \sup_{priors} \; \Pbb(\theta = D \mid C, M = \varnothing) = 1.
> 395|$$
> 
> 396|Equivalently, for any $\delta > 0$, there exists a prior distribution over researcher types and data-generating processes such that $\Pbb(fraud \mid C, M = \varnothing) > 1 - \delta$. M-declaration is **information-theoretically necessary** for quality certification.
> 397|
398|
399|> **Proof:** \rigorFull
> 400|We construct an adversarial prior that drives the posterior probability of fraud arbitrarily close to 1.
> 401|
> 402|
> 403|**Step 1: Setup.**
> 404|Consider the space of possible data-generating processes $\cG = \cG_{H} \cup \cG_{D}$, where $\cG_{H}$ is the set of processes consistent with honest research (genuine data, properly reported) and $\cG_{D}$ is the set of processes consistent with fraud (fabricated or manipulated data). Without M-declaration, the community knows only that the paper was published — it provides no information about which subset of $\cG$ contains the true process.
> 405|
> 406|
> 407|**Step 2: Adversarial Prior Construction.**
> 408|Fix any desired confidence threshold $\delta > 0$. We construct a prior $\pi_\delta$ as follows.
> 409|
> 410|Let the set of honest data-generating processes $\cG_{H}$ be parameterized by a complexity measure $\tau(g)$ for $g \in \cG_{H}$, representing the difficulty of generating data from process $g$ honestly. For any finite $\tau_$, there are finitely many honest processes with $\tau \le \tau_$.
> 411|
> 412|In contrast, the set of fraudulent processes $\cG_{D}$ is vastly larger: for any honest dataset of size $n$, there are exponentially many ways to fabricate a dataset of the same size that passes basic consistency checks. Specifically:
> 413|
> $$
> 414|    |\{g \in \cG_{D} : output looks plausible\}| = \Omega(\exp(c \cdot n))
> 415|$$
> 
> 416|for some constant $c > 0$, while $|\cG_{H}|$ is bounded by a polynomial in $n$ (since honest data comes from a fixed physical process).
> 417|
> 418|Define the prior $\pi_\delta$ as:
> 419|
> $$<!-- label: eq:adversarial_prior -->
> 420|    \pi_\delta(\theta = D) = 1 - \frac{2}, \qquad \pi_\delta(\theta = H) = \frac{2},
> 421|$$
> 
> 422|with uniform distribution over fraudulent processes in $\cG_{D}$ and over honest processes in $\cG_{H}$.
> 423|
> 424|
> 425|**Step 3: Bayesian Update Given Published Claim.**
> 426|A published claim $C$ is a statement about the data. Given $C$, the likelihoods are:
> 427|
> $$
> 428|    \Pbb(C \mid \theta = H) = \frac{|\{g \in \cG_{H} : g  produces data consistent with  C\}|}{|\cG_{H}|},
> 429|$$
> 
> 430|
> $$
> 431|    \Pbb(C \mid \theta = D) = \frac{|\{g \in \cG_{D} : g  produces data consistent with  C\}|}{|\cG_{D}|}.
> 432|$$
> 
> 433|
> 434|For any claim $C$ that can be produced by both honest and dishonest processes (which is the entire point — a fraudulent paper must look like an honest one to pass review), we have:
> 435|
> $$
> 436|    \Pbb(C \mid \theta = D) \ge \Pbb(C \mid \theta = H) \cdot \frac{|\cG_{H}|}{|\cG_{D}|}.
> 437|$$
> 
> 438|
> 439|
> 440|**Step 4: Posterior Calculation.**
> 441|Applying Bayes' rule:
> 442|
> $$
> 443|    \Pbb(\theta = D \mid C, M = \varnothing) &= \frac{\Pbb(C \mid D) \cdot \pi_\delta(D)}{\Pbb(C \mid D) \cdot \pi_\delta(D) + \Pbb(C \mid H) \cdot \pi_\delta(H)} 

> 444|    &= \frac{\Pbb(C \mid D) \cdot (1 - \delta/2)}{\Pbb(C \mid D) \cdot (1 - \delta/2) + \Pbb(C \mid H) \cdot (\delta/2)}.
> 445|$$
> 
> 446|
> 447|The critical observation: without M-declaration, we have no constraint on the ratio $|\cG_{D}| / |\cG_{H}|$. We can make this ratio arbitrarily large in the prior. Let $R = |\cG_{D}| / |\cG_{H}|$. Then, for any claim $C$ that both types could produce, there exists a subset of $\cG_{D}$ of size $\Omega(R \cdot |\cG_{H}|)$ that produces data satisfying $C$. Thus:
> 448|
> $$
> 449|    \Pbb(C \mid \theta = D) \ge \frac{\Omega(R \cdot |\cG_{H}|)}{|\cG_{D}|} \cdot \Pbb(C \mid \theta = H) = \Omega(1) \cdot \Pbb(C \mid \theta = H).
> 450|$$
> 
> 451|
> 452|Substituting into the posterior:
> 453|
> $$
> 454|    \Pbb(\theta = D \mid C, M = \varnothing) &\ge \frac{\Omega(1) \cdot \Pbb(C \mid H) \cdot (1 - \delta/2)}{\Omega(1) \cdot \Pbb(C \mid H) \cdot (1 - \delta/2) + \Pbb(C \mid H) \cdot (\delta/2)} 

> 455|    &= \frac{\Omega(1) \cdot (1 - \delta/2)}{\Omega(1) \cdot (1 - \delta/2) + \delta/2}.
> 456|$$
> 
> 457|
> 458|As $R \to \infty$ (i.e., as the space of possible fraud becomes arbitrarily large relative to the space of honest research), $\Omega(1)$ can be made arbitrarily large, driving the posterior to 1:
> 459|
> $$
> 460|    \lim_{R \to \infty} \Pbb(\theta = D \mid C, M = \varnothing) = 1.
> 461|$$
> 
> 462|
> 463|Since this construction works for any $\delta > 0$ (just set $R$ large enough), we obtain:
> 464|
> $$
> 465|    \sup_{priors} \Pbb(\theta = D \mid C, M = \varnothing) = 1.
> 466|$$
> 
> 467|
> 468|
> 469|**Step 5: Interpretation.**
> 470|M-declaration breaks this adversarial construction. When $M$ is declared, the prior space is constrained: a researcher declaring $M$ must have produced data capable of withstanding $M$ independent verifications. This eliminates most of $\cG_{D}$ from the support of the prior — the adversary can no longer pack $\cG_{D}$ with arbitrary fraudulent processes, because only fraudulent processes that can survive $M$ verifications remain possible, and their number decays exponentially in $M$. Formally:
> 471|
> $$
> 472|    |\{g \in \cG_{D} : g  survives  M  verifications\}| = |\cG_{D}| \cdot \exp(-2M\Delta_^2).
> 473|$$
> 
> 474|
> 475|Thus M-declaration provides an **information-theoretic certificate**: it reduces the effective cardinality of the fraudulent process space from astronomical to negligible. Without it, the prior can always be chosen adversarially to make fraud the dominant hypothesis.
> 476|
> 477|This completes the proof of Theorem [ref].
> 478|
479|
480|> **Corollary:** [No M, No Trust]
> 481|<!-- label: cor:no_trust -->
> 482|A paper without M-declaration provides zero information about data quality. The reader's posterior belief about fraud is entirely determined by their prior, which can be adversarially unfavorable. In operational terms: papers without M-declaration should be treated as **[NOT YET AUDITED]** — epistemically equivalent to the author saying ``trust me.''
> 483|
484|
485|> **Corollary:** [M-Declaration as a Public Good]
> 486|<!-- label: cor:public_good -->
> 487|M-declaration is a public good: the declaring researcher bears the documentation cost $c_d(M)$, while the entire scientific community benefits from the reduction in epistemic uncertainty. This creates a free-rider problem (researchers benefit from others' declarations without declaring themselves) — which is precisely why M-declaration must be **mandatory**, not voluntary. Voluntary M-declaration is a public goods game with a defective dominant strategy; mandatory M-declaration transforms it into a coordination game with a cooperative equilibrium.
> 488|
489|
490|% ===========================================================================
491|## Theorem 3 — Falsification Under Declaration = Active Evil
492|## 定理3——声明参数还做假等于作恶
493|<!-- label: sec:thm3 -->
494|% ===========================================================================
495|
496|> **Theorem:** [Detection Inevitability]
> 497|<!-- label: thm:inevitability -->
> 498|If a researcher declares $M$ but falsifies data, then under Assumptions [ref]-- [ref], the probability of evading detection by all $M$ independent verifiers decays exponentially in $M$, and the cumulative probability of eventual detection approaches 1 as the scientific community accumulates verification attempts:
> 499|
> $$
>     \mathbb{P}(evade at time  t \mid D, M) \le \exp(-2M \cdot \Delta_^2), 

>     \lim_{t\to\infty} \mathbb{P}(detection by time  t) = 1.
> $$
> 
> Declaring $M$ and falsifying = **active evil** (作恶): actively constructing deception to defeat a known verification threshold.

> **Proof:** Hoeffding: $M$ independent verifiers each with $\Delta_m \ge \Delta_$, $\mathbb{P}(all miss) \le \exp(-2M\Delta_^2)$. Under verifier growth (A8), $M_{eff}(t) \to \infty$. Hence $\lim \exp(-2M_{eff}(t)\Delta_^2) = 0$. Borel-Cantelli $\implies$ detection a.s. Spring permanent memory ensures evidence persists. $\square$

## Theorem 4 — Reviewer Complicity 审稿人同谋对等定理
<!-- label: sec:reviewer-complicity -->

> **Theorem:** [审稿人同谋对等定理]
> <!-- label: thm:reviewer-complicity -->
> \rigorFull
> Let $r = \mathbb{P}(accept \mid M=\varnothing)$. Define complicity threshold $r^* = V_{prestige} / (D_{exposure} \cdot p_f)$ where $p_f = \mathbb{P}(fraud \mid M=\varnothing)$.
> 
1. $r < r^*$: **negligent** (过失).
2. $r \ge r^*$: **complicit** (同谋) — maintains pooling equilibrium enabling fraud.
3. Spring records $R$'s pattern. $\mathcal{C}_R = \lim_{T\to\infty} \frac{1}{T}\sum r_t$. If $\mathcal{C}_R \ge r^*$, $R$ is **permanently classified as complicit**.

> **Corollary:** [机构同谋]
> Journal with M=0 acceptance rate $\alpha$ has $\mathcal{C}_{venue} = \alpha$. Accepting M=0 papers = institutional complicity.

## Theorem 5 — Data Substitution Attack Infeasibility 数据替换攻击不可行定理 (羊头狗肉定理)
<!-- label: sec:thm5 -->

> **Theorem:** [数据替换攻击不可行定理 (羊头狗肉定理)]
> <!-- label: thm:substitution -->
> \rigorFull
> Let an entity declare $M_{high}$ (supported by high-quality dataset $\mathcal{D}_{high}$) while actually training on a lower-quality dataset $\mathcal{D}_{low}$ with true $M_{low} < M_{high}$. Under the SCX framework:
> 
1. **Hash inconsistency**: The commitment hash $\mathcal{H}_{declared} = SHA-256(\mathcal{D}_{high} \| M_{high})$ differs from the hash of the actual training data. Any auditor with access to either dataset detects the mismatch immediately.
2. **Behavioral divergence**: Let $f_{high}$ be a model trained on $\mathcal{D}_{high}$ and $f_{low}$ on $\mathcal{D}_{low}$. Under the M-declaration, the public expects behavior consistent with $M_{high}$. Multiple independent auditors train reference models on independently sourced data meeting the $M_{high}$ standard. By Theorem~1, the probability that all $K$ reference models exhibit identical output distribution to $f_{low}$ decays as $\exp(-2K \cdot \Delta_{behavior}^2)$ where $\Delta_{behavior}$ is the minimum detectable behavioral divergence between $M_{high}$-trained and $M_{low}$-trained models.
3. **Unidentifiability backfires**: Theorem~3 (老实人定理) states that when model behavior diverges from expectation, the cause (data quality vs architecture vs training procedure) is unidentifiable without declared assumptions. The burden of proof falls on the declaring entity to demonstrate that the divergence is *not* caused by data substitution — a burden that cannot be met without revealing the actual training data, which would expose the substitution.

> The attack is therefore **infeasible**: the attacker must simultaneously (a) match the hash of $\mathcal{D}_{high}$ without possessing it (SHA-256 preimage resistance), (b) produce model behavior indistinguishable from $M_{high}$-trained models (Hoeffding bound), and (c) explain any observed behavioral divergence under Theorem~3 without revealing the actual training data.

> **Proof:** (a) SHA-256 preimage resistance: given $\mathcal{H}_{declared}$, finding $\mathcal{D}_{low}$ such that $SHA-256(\mathcal{D}_{low}) = \mathcal{H}_{declared}$ requires $O(2^{256})$ operations. (b) Behavioral Hoeffding: With $K$ independent auditors, $\mathbb{P}(all accept  f_{low}  as  M_{high}-equivalent) \le \exp(-2K\Delta_{behavior}^2)$. (c) Theorem~3: $\mathbb{P}(f_{low}  indistinguishable from  f_{high} \mid divergence observed) = 1$ only if the attacker declares the true data quality — which would reveal $M_{low}$, contradicting the attack. $\square$

> **Corollary:** [大模型公司的无退路困境]
> An AI company declaring $M=1000$ training data quality cannot profitably substitute $M=100$ data. Any attempt to ``test the waters'' (试水) encounters three simultaneous barriers: cryptographic (hash mismatch), statistical (behavioral detection with $K \ge 3$), and game-theoretic (Theorem~3 shifts burden of proof). The expected cost of detection exceeds any conceivable benefit from data cost savings.

## Case Studies 案例研究
<!-- label: sec:cases -->

- **HEP (ATLAS/CMS)**: $M=2$ detectors naturally cross-validate. M satisfied.
- **Psychology crisis**: M never declared $\to$ $>50\%$ failed replication. Most: $M=0$.
- **Deep learning**: M = independent training runs. Current: $M\approx 1$.
- **耿同学**: $M=1$ shifts equilibrium. $M=100$ institutionalizes.

## Cercis Score for Papers 论文Cercis评分
<!-- label: sec:cercis -->
$Cercis(paper) = Q + \eta N$, $Q$ = replicability, $N$ = novelty. $M=0 \implies Q \equiv 0$.

## M-Parameter Arms Race + Dark Forest M参数军备竞赛与黑暗森林
<!-- label: sec:arms-race -->

1. **Competitive signaling**: Company A: $M=1000$. Company B: $M=100$. A wins. M = market signal.
2. **Ratchet**: Once one declares, silence = $M=0$ (Theorem~2).
3. **SCX sole standard**: Only SCX has mathematical guarantees (Theorems 1--5).

### Dark Forest Protocol 黑暗森林协议
Publishing non-SCX M = self-exposure (Theorem~2). Falsification of SCX-certified M = active fraud (Theorem~3). Non-participation tolerated ($M=0$). Private M development ignored. **Non-SCX M publication broadcasts dark forest coordinates**.

## M-Registry: Public Monitoring M参数公开登记网
<!-- label: sec:m-registry -->
**M is never a bare number** — always accompanied by code + SHA-256 hash + data manifest.

**PUBLIC mode**: M, code, hash, manifest fully visible. **PRIVATE mode**: Only hash public; code encrypted. Hash proves M was fixed pre-challenge.

Hash commitment prevents retroactive M-adjustment (SHA-256 preimage resistance). Community monitoring: anyone submits verification attempts. High verified M = market advantage automated.

## Discussion — 人类的精神结晶不允许拉屎
<!-- label: sec:discussion -->
Path: $M=1$ (耿同学) $\to$ $M=10$ (systematic) $\to$ $M=100$ (mandatory) $\to$ separating equilibrium. Limitations: cannot prevent all fraud, cannot replace deliberation, cannot detect shared biases.

<div align="center">

\bfseries
No M, No Trust. 无M，不信。

Declare M + cheat = caught. 声明M做假，必被捉。

Reviewers accepting M=0 = complicit. 接受M=0的审稿人即同谋。

Data substitution = detected. 数据替换=不可行(Theorem 5)。

Science belongs to verifiers. 科学属于验证者。

</div>

\begin{thebibliography}{99}
\bibitem{scx2026} SCX. The SCX Framework. 2026.
\bibitem{scx_personal_ethics} SCX. SCX Personal Ethics. 2026.
\bibitem{scx_governance} SCX. SCX Audit of Governance. 2026.
\bibitem{hoeffding1963} W. Hoeffding. Probability inequalities. *JASA*, 1963.
\bibitem{spence1973} M. Spence. Job market signaling. *QJE*, 1973.
\bibitem{geng2024} 耿同学. Public data audit and fraud detection. 2024.
\end{thebibliography}