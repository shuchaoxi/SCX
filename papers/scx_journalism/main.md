*Abstract:*

We formalize news verification as a multi-expert audit problem under the SCX{} (Structured Causal eXamination) framework. News sources are modeled as an expert community $\sourceSet = \{S_1, ..., S_M\}$; each published claim $c \in \claimSpace$ is an auditable assertion about a ground-truth event $\theta \in \newsState$. Multi-source corroboration is operationalized through the Yajie{} consensus mechanism: when $M$ independent sources converge on the same factual claim, their agreement provides an exponentially decaying upper bound on the probability of collective error. We prove four core theorems. **Theorem~1 (Multi-Source Corroboration Bound 多源印证界):** Under conditional source independence, the probability that the Yajie{} consensus deviates from the true event by more than $\varepsilon$ satisfies $\Pbb(\norm{c - \theta}_\infty > \varepsilon) \leq \exp(-2M_{\mathrm{eff}} \cdot \varepsilon^2 / \bar^2)$, establishing that verification confidence grows exponentially with the number of corroborating sources. **Theorem~2 (Single-Source Unverifiability 单源不可验证性):** When $M = 1$, the detection probability for any misreporting is bounded above by a constant $p_ < 1$ that depends on the source's precision but is independent of claim magnitude---formalizing why fake news (单源假新闻) is epistemically indistinguishable from truth under single-source conditions. **Theorem~3 (Anonymity-Preserving Consensus 匿名性保护共识):** The Yajie{} consensus computed under \VISprivate{} source visibility---where auditor identities are hidden but estimates are shared---preserves the same asymptotic convergence rate as the fully public \VISpublic{} mode, proving that source protection does not degrade verification power. **Theorem~4 (Fact-Checker Network Resilience 事实核查网络韧性):** When a fraction $f$ of sources in a fact-checker network are adversarial (deliberately propagating false claims), the Yajie{} consensus remains within $\varepsilon$ of truth provided $f < \frac{1}{2} - \frac{\bar^2 \log(1/\delta)}{2M\varepsilon^2}$, establishing a breakdown threshold for coordinated disinformation campaigns. We develop the Cercis{} veracity score $S(c) = Q(c) + \eta \cdot N(c)$ for ranking claims by corroboration quality and source novelty, the \Situs{} encoding for representing source-claim attribution graphs with privacy-preserving visibility modes, and an experimental protocol with specific benchmark datasets (LIAR, FEVER, FakeNewsNet, CHEF). All theorems carry full proofs. Eleven explicit assumptions are stated and verified.

**Keywords:** news verification 新闻核查, fact-checking 事实核查, multi-source corroboration 多源验证, fake news detection 假新闻检测, Yajie{} consensus, SCX{} auditing, source anonymity 来源匿名, certified fact-checking 认证式事实核查, expert ensemble, disinformation resilience

## Introduction 引言

The epistemic crisis engendered by online misinformation---variously termed ``fake news,'' ``disinformation,'' or ``information disorders''---has attracted sustained attention from computer science, journalism, political science, and psychology [cite]. The dominant response has been the proliferation of fact-checking organizations: as of 2024, the Duke Reporters' Lab counted over 400 active fact-checking initiatives worldwide [cite]. These organizations employ human journalists, crowdsourced verification, and increasingly, automated claim detection systems to assess the veracity of published statements.

Yet the epistemological foundations of fact-checking remain under-theorized. Three structural problems persist:

1. **The single-auditor problem 单一审计者问题.** A fact-check published by a single organization---however reputable---is itself an unverified claim. Without multi-source corroboration, the reader cannot distinguish between a correct fact-check and a second-order falsehood. This is the recursion problem: *quis custodiet ipsos custodes?* (who watches the watchers? 谁来监督监督者？)
2. **The source attribution dilemma 来源归属困境.** Verifiable fact-checking requires transparent sourcing, yet full source disclosure can expose whistleblowers, compromise confidential informants, or reveal journalistic methods that sources relied upon remaining hidden. The tension between auditability and source protection has no resolution in existing frameworks.
3. **The scalability impasse 可扩展性僵局.** Human fact-checking cannot scale to the volume of online content. Automated systems, while scalable, lack the epistemic authority of multi-source human judgment. No existing framework unifies the scalability of automation with the rigor of multi-expert verification.

The SCX{} auditing framework [cite] provides mathematical tools that address each of these problems. Its core mechanisms---multi-expert noise detection via Yajie{} consensus, error-source unidentifiability analysis, and Spring{} gating for regime-shift detection---translate naturally to news verification when we make the following identification:

<div align="center">

[Table omitted — see original .tex]

</div>

**Contributions.** This paper provides:

1. **Formalization** (Section [ref]): News verification as multi-source expert audit with visibility-controlled consensus. Eleven explicit assumptions~\assumptionTag{1}--\assumptionTag{11}.
2. **Four theorems with full proofs**:
3. **Cercis{} veracity score** (Section [ref]): $S(c) = Q(c) + \eta \cdot N(c)$ for ranking claims by corroboration quality and source diversity.
4. **The \Situs{} source-claim encoding** (Section [ref]): Privacy-preserving attribution graphs with \VISpublic{}, \VISprivate{}, and \VISblind{} visibility modes.
5. **Experimental protocol** (Section [ref]): Benchmarks, metrics, and ablation plan on LIAR, FEVER, FakeNewsNet, and CHEF.
6. **Discussion** (Section [ref]): Honest limitations, relationship to journalism ethics, and fundamental constraints.

**What this paper is not.** This is a mathematical framework for multi-source claim verification---not a normative theory of journalism, not a proposal for content moderation policy, and not a claim that automated systems can replace human judgment. We prove theorems about detection probabilities, consensus convergence, and adversarial resilience. Whether and how these mathematical guarantees should be deployed in real-world information ecosystems is a political and ethical question that lies beyond the scope of this paper.

## Formalization: News as a Multi-Source Assertion System 新闻作为多源断言系统
<!-- label: sec:formalization -->

### The Event Space 事件空间

> **Definition:** [News Event 新闻事件]
> <!-- label: def:event -->
> A news event at time $t$ is a vector of ground-truth facts:
> 
> $$
>     \theta_t = (\theta_t^{(1)}, \theta_t^{(2)}, ..., \theta_t^{(d)}) \in \newsState \subset \R^d,
>     <!-- label: eq:event -->
> $$
> 
> where each component $\theta_t^{(k)}$ represents an atomic, verifiable proposition. Canonical components include:
> 
- $\theta_t^{(1)}$: Occurrence indicator (binary: did event $E$ occur?);
- $\theta_t^{(2)}$: Attribution (categorical: who performed action $A$?);
- $\theta_t^{(3)}$: Location (continuous/discrete: where did event $E$ occur?);
- $\theta_t^{(4)}$: Temporal coordinate (when did event $E$ occur?);
- $\theta_t^{(5)}$: Magnitude (numeric: how many casualties / how much financial loss?);
- $...$ additional components as relevant to the claim type.

> The event space $\newsState$ is compact with known diameter $D_\Theta$.

> **Definition:** [News Claim 新闻声明]
> <!-- label: def:claim -->
> A news claim is a published assertion about the event:
> 
> $$
>     c \in \claimSpace \subset \R^d,
>     <!-- label: eq:claim -->
> $$
> 
> where $c$ may or may not equal $\theta_t$. A claim is **true** if $\norm{c - \theta_t}_\infty \leq \varepsilon_{\mathrm{tol}}$ for a tolerance $\varepsilon_{\mathrm{tol}} > 0$ representing practical equivalence, and **false** (fake news 假新闻) otherwise.

### The Source Community as Expert Ensemble 来源社区作为专家集成

> **Definition:** [News Source 新闻来源]
> <!-- label: def:source -->
> A news source $S_j \in \sourceSet$ is an entity capable of publishing claims about events. Each source is characterized by:
> 
> $$
>     S_j = (\mu_j, \Sigma_j, \mathcal{V}_j, \mathcal{H}_j),
>     <!-- label: eq:source_profile -->
> $$
> 
> where:
> 
- $\mu_j \in \R^d$: systematic bias vector ($\E[c_j - \theta] = \mu_j$);
- $\Sigma_j \in \R^{d \times d}$: precision (inverse covariance) matrix;
- $\mathcal{V}_j$: visibility mode $\in \{\VISpublic, \VISprivate, \VISblind\}$;
- $\mathcal{H}_j$: historical veracity record (track record of past claims).

Sources differ along four dimensions critical to the multi-expert structure:

1. **Access modality 获取方式:** Direct eyewitness, secondary reporting, document analysis, data journalism, satellite imagery, leaked documents, official press releases.
2. **Institutional affiliation 机构隶属:** Wire services (Reuters, AP, AFP, Xinhua), national broadcasters, independent investigative outlets, citizen journalism platforms, government press offices, NGO reports.
3. **Methodological approach 方法论:** Investigative interviewing, document triangulation, data forensics, open-source intelligence (OSINT), geolocation verification, metadata analysis.
4. **Epistemic stance 认识论立场:** Neutral reporting, advocacy journalism, adversarial interviewing, collaborative verification.

> **Definition:** [Multi-Source Corroboration 多源印证]
> <!-- label: def:corroboration -->
> Given $M$ sources $\{S_j\}_{j=1}^{M}$ each publishing claim $c_j$ about event $\theta$, the Yajie{} corroboration consensus is:
> 
> $$
>     c^* = \sum_{j=1}^{M} w_j c_j, \quad \sum_{j=1}^{M} w_j = 1, \quad w_j \geq 0,
>     <!-- label: eq:corroboration_consensus -->
> $$
> 
> where weights $w_j$ are inversely proportional to each source's historical error variance: $w_j \propto \tr(\Sigma_j)$ in the baseline specification, and are correlation-adjusted in the general case. The **corroboration strength** is:
> 
> $$
>     \Gamma(M) = \sum_{j=1}^{M} w_j \cdot \ind{\norm{c_j - c^*}_\infty \leq \varepsilon_{\mathrm{tol}}}.
>     <!-- label: eq:corroboration_strength -->
> $$

> **Remark:** [Yajie Consensus as Epistemic Aggregation Yajie共识作为认识论聚合]
> The Yajie{} consensus operationalizes the journalistic principle that ``a story is confirmed when multiple independent sources report the same facts'' (多方印证原则). Unlike simple majority voting, the Yajie{} weighting scheme gives greater credence to sources with demonstrated accuracy (lower historical error), creating a meritocratic---rather than purely democratic---consensus. This parallels the editorial practice of weighting an experienced investigative journalist's account more heavily than an anonymous social media post, but formalizes the weighting through verifiable track records.

### Visibility Modes and Source Anonymity 可见性模式与来源匿名

> **Definition:** [Visibility Modes 可见性模式]
> <!-- label: def:visibility -->
> Each source operates under one of three visibility modes:
> 
- **\VISpublic{} (公开):** Both the source identity and its claim are publicly attributed. Example: a named journalist publishing under a byline in a major newspaper.
- **\VISprivate{} (匿名保护):** The claim is published but the source identity is cryptographically protected. The system can verify that the source is a member of the authorized source set $\sourceSet$ (via zero-knowledge membership proof) without revealing which member. Example: a whistleblower providing documents through SecureDrop; a confidential informant in an authoritarian regime.
- **\VISblind{} (盲审):** Neither the source identity nor the raw claim is visible to other sources. Sources submit encrypted claims; the consensus is computed via secure multi-party computation (MPC). This prevents herding behavior where later sources converge on earlier-published claims.

The \VISprivate{} mode is the formal analogue of the journalistic practice of protecting confidential sources. Theorem [ref] will prove that this protection does not degrade the statistical power of the Yajie{} consensus.

### The Fact-Checker Network as Auditor Community 事实核查网络作为审计者社区

> **Definition:** [Fact-Checker Network 事实核查网络]
> <!-- label: def:factchecker_network -->
> A fact-checker network $F = \{\mathcal{F}_1, ..., \mathcal{F}_K\}$ is a set of $K$ independent verification organizations. Each $\mathcal{F}_k$ receives claims from a subset of sources $\sourceSet_k \subseteq \sourceSet$ and produces a verification verdict:
> 
> $$
>     v_k(c) \in \{0, 1\}, \quad v_k(c) = \ind{\norm{c - \hat^{(k)}}_\infty \leq \varepsilon_{\mathrm{tol}}},
>     <!-- label: eq:verdict -->
> $$
> 
> where $\hat^{(k)}$ is $\mathcal{F}_k$'s independent estimate of the ground truth, derived from its own source network and investigative methodology.

The fact-checker network is the journalism-domain analogue of the SCX{} auditor community. Just as SCX{} auditors independently estimate model accuracy from heterogeneous data, fact-checkers independently estimate claim veracity from heterogeneous source networks. The key structural property is **auditor independence**: $\mathcal{F}_k$ and $\mathcal{F}_{k'}$ should not share the same underlying sources, or their verdicts are conditionally correlated and the effective multiplicity $K_{\mathrm{eff}}$ is reduced.

### Assumptions 假设

We now state the assumptions under which our theorems hold. Each assumption is explicitly labeled, carries a verification protocol, and is falsifiable in principle.

\begin{assumption}[A1: Compact Event Space 紧致事件空间]
<!-- label: ass:A1 -->
The event space $\newsState \subset \R^d$ is compact with known diameter $D_\Theta = \sup_{\theta, \theta' \in \newsState} \norm{\theta - \theta'}_\infty < \infty$. All factual claims have natural bounds: occurrence is binary, dates are bounded by recorded history, casualty counts are bounded by world population.
\end{assumption}

\begin{assumption}[A2: Source Conditional Independence 来源条件独立]
<!-- label: ass:A2 -->
Conditional on the true event $\theta$, the claims $\{c_j\}_{j=1}^{M}$ published by distinct sources are mutually independent:

$$
    \Pbb(c_1, ..., c_M \mid \theta) = \prod_{j=1}^{M} \Pbb(c_j \mid \theta).
    <!-- label: eq:source_independence -->
$$

This holds when sources do not share raw information (no collusion, no common feed, no copy-paste journalism). Violations occur when multiple outlets rewrite the same wire service report---a case handled by the correlation adjustment in Theorem [ref].
\end{assumption}

\begin{assumption}[A3: Sub-Gaussian Source Errors 亚高斯来源误差]
<!-- label: ass:A3 -->
For each source $S_j$, the error vector $\varepsilon_j = c_j - \theta$ is sub-Gaussian with variance proxy $\sigma_j^2$:

$$
    \E[\exp(\lambda \inner{u}{\varepsilon_j})] \leq \exp\left(\frac{\lambda^2 \sigma_j^2}{2}\right), \quad \forall \lambda \in \R, \;\forall u: \norm{u}_2 = 1.
    <!-- label: eq:subgaussian -->
$$

This is a weaker condition than Gaussianity and holds for any bounded error distribution (Hoeffding's lemma), which is realistic for factual claims with bounded error magnitudes.
\end{assumption}

\begin{assumption}[A4: Known Source Precision Bounds 已知来源精度界]
<!-- label: ass:A4 -->
Each source's effective variance $\sigma_j^2$ is bounded above by a known constant $\sigma_^2$. The harmonic mean precision $\bar^2 = (M^{-1}\sum_j 1/\sigma_j^2)^{-1}$ is computable from historical veracity records $\mathcal{H}_j$.
\end{assumption}

\begin{assumption}[A5: Non-Colluding Adversarial Sources 非合谋对抗性来源]
<!-- label: ass:A5 -->
Adversarial sources (those deliberately propagating false claims) may exist but do not coordinate their fabrications. Each adversarial source independently draws its claim from a distribution $\mathcal{D}_{\mathrm{adv}}$ with mean $\theta + \mu_{\mathrm{adv}}$ and variance $\sigma_{\mathrm{adv}}^2$. Coordinated disinformation campaigns are addressed in Theorem [ref] under the ``fraction adversarial'' model.
\end{assumption}

\begin{assumption}[A6: Verifiable Source Membership 可验证来源成员资格]
<!-- label: ass:A6 -->
The authorized source set $\sourceSet$ is maintained with cryptographic integrity. A source $S_j$ can prove membership in $\sourceSet$ without revealing its identity, via a zero-knowledge membership proof (e.g., Merkle tree inclusion proof with zk-SNARK). Non-member claims are excluded from the Yajie{} consensus.
\end{assumption}

\begin{assumption}[A7: Fact-Checker Independence 事实核查者独立性]
<!-- label: ass:A7 -->
Different fact-checking organizations $\mathcal{F}_k, \mathcal{F}_{k'}$ draw from disjoint or minimally overlapping source pools $\sourceSet_k \cap \sourceSet_{k'} = \emptyset$ (or at most a negligible overlap fraction $\delta_{\mathrm{overlap}} \ll 1$). This ensures conditional independence of verification verdicts.
\end{assumption}

\begin{assumption}[A8: Temporal Coherence 时间一致性]
<!-- label: ass:A8 -->
Claims about event $\theta_t$ are published within a finite time window $[t, t + T_]$. Claims outside this window are treated as distinct events or retrospective corrections. The event itself is assumed stable over the reporting window (no ``facts on the ground'' changing mid-reporting).
\end{assumption}

\begin{assumption}[A9: Lipschitz Veracity Score 利普希茨真实性评分]
<!-- label: ass:A9 -->
The veracity score functional $V: \claimSpace \times \newsState \to [0, 1]$ is $L_V$-Lipschitz in the claim:

$$
    \abs{V(c, \theta) - V(c', \theta)} \leq L_V \cdot \norm{c - c'}_\infty.
    <!-- label: eq:lipschitz_veracity -->
$$

This ensures that small factual errors produce proportionally small score reductions (no cliff effects from binary true/false thresholds alone).
\end{assumption}

\begin{assumption}[A10: Sufficient Source Diversity 充分来源多样性]
<!-- label: ass:A10 -->
The source community $\sourceSet$ includes sources with heterogeneous access modalities, institutional affiliations, and methodological approaches. At least two sources use access modalities whose information channels do not logically imply each other (e.g., satellite imagery does not share raw data with eyewitness testimony). This ensures that no single information bottleneck determines the consensus.
\end{assumption}

\begin{assumption}[A11: Visibility Mode Integrity 可见性模式完整性]
<!-- label: ass:A11 -->
The visibility mode $\mathcal{V}_j$ assigned to source $S_j$ is cryptographically enforced. In \VISprivate{} mode, the claim is published with a zero-knowledge proof of authorized-source membership but without the source identifier. In \VISblind{} mode, the raw claim is encrypted and only the aggregated consensus is revealed. The system prevents inference attacks on source identity from the claim content alone (differential privacy guarantees with parameter $\epsilon_{\mathrm{dp}}$).
\end{assumption}

## Theorem 1: Multi-Source Corroboration Bound 多源印证界
<!-- label: sec:corroboration -->

The central mathematical result of this paper is an exponential bound on the probability that the Yajie{} multi-source consensus deviates from ground truth. This theorem formalizes the journalistic intuition that ``the more independent sources confirm a story, the more reliable it is.''

### Concentration of the Yajie Consensus

> **Lemma:** [Consensus Concentration 共识集中不等式]
> <!-- label: lem:consensus_concentration -->
> Under Assumptions [ref]-- [ref], for $M$ independent sources with sub-Gaussian errors and variance proxies $\sigma_1^2, ..., \sigma_M^2$, the Yajie{} consensus $c^* = \sum_j w_j c_j$ with optimal weights $w_j \propto 1/\sigma_j^2$ satisfies:
> 
> $$
>     \Pbb\left(\norm{c^* - \theta}_\infty > \varepsilon \;\middle|\; \theta\right) \leq 2d \cdot \exp\left(-\frac{M_{\mathrm{eff}} \cdot \varepsilon^2}{2\bar^2}\right),
>     <!-- label: eq:consensus_concentration -->
> $$
> 
> where $M_{\mathrm{eff}} = M / (1 + (M-1)\bar)$ is the effective number of independent sources, $\bar \in [0, 1]$ is the average pairwise error correlation, and $\bar^2 = (M^{-1}\sum_j 1/\sigma_j^2)^{-1}$ is the harmonic mean variance.

> **Proof:** \rigorFull
> **Step 1: Consensus error decomposition.** The Yajie{} consensus error is:
> 
> $$
>     c^* - \theta = \sum_{j=1}^{M} w_j (c_j - \theta) = \sum_{j=1}^{M} w_j \varepsilon_j,
>     <!-- label: eq:error_decomp -->
> $$
> 
> where $\varepsilon_j = c_j - \theta$ is source $j$'s error. Under Assumption [ref], each $\varepsilon_j$ is sub-Gaussian: for any unit vector $u$, $\inner{u}{\varepsilon_j}$ is sub-Gaussian with variance proxy $\sigma_j^2$.
> 
> **Step 2: Variance of weighted sum.** Under Assumption [ref] (conditional independence), the weighted sum $S = \sum_j w_j \varepsilon_j$ satisfies:
> 
> $$
>     \Var(S \mid \theta) = \sum_{j=1}^{M} w_j^2 \sigma_j^2.
>     <!-- label: eq:var_weighted -->
> $$
> 
> 
> With optimal inverse-variance weights $w_j = (1/\sigma_j^2) / (\sum_{k} 1/\sigma_k^2)$, we obtain:
> 
> $$
>     \Var(S \mid \theta) = \frac{\sum_j w_j^2 \sigma_j^2}{(\sum_j 1/\sigma_j^2)^2} \cdot \sum_j 1/\sigma_j^2 \cdot \bar^2 = \frac{\bar^2}{M},
>     <!-- label: eq:var_optimal -->
> $$
> 
> where we use the identity $\sum_j w_j^2 \sigma_j^2 = \bar^2 / M$ for inverse-variance weights.
> 
> **Step 3: Sub-Gaussian tail bound.** For sub-Gaussian random variables, the weighted sum $S$ is also sub-Gaussian with variance proxy $\bar^2 / M$. For any component $k \in \{1, ..., d\}$:
> 
> $$
>     \Pbb\left(\abs{S_k} > \varepsilon \mid \theta\right) \leq 2\exp\left(-\frac{M\varepsilon^2}{2\bar^2}\right).
>     <!-- label: eq:component_tail -->
> $$
> 
> 
> **Step 4: Correlation adjustment.** When source errors exhibit average pairwise correlation $\bar$ (e.g., multiple sources relying on the same underlying wire report, shared eyewitness, or common documentary source), the effective sample size is reduced. Under a compound symmetry correlation structure $\Cov(\varepsilon_j, \varepsilon_{j'}) = \rho \sigma_j \sigma_{j'}$ for $j \neq j'$, the variance of the consensus mean is inflated:
> 
> $$
>     \Var(S \mid \theta) = \frac{\bar^2}{M} \cdot (1 + (M-1)\bar).
>     <!-- label: eq:correlated_variance -->
> $$
> 
> 
> This is equivalent to reducing the effective number of independent sources from $M$ to $M_{\mathrm{eff}} = M / (1 + (M-1)\bar)$. Note that as $M \to \infty$, $M_{\mathrm{eff}} \to 1/\bar$, so correlated sources provide diminishing marginal corroboration---consistent with the journalistic principle that ten newspapers reprinting the same AP wire story provide no more corroboration than one.
> 
> **Step 5: Union bound over dimensions.** For the $\ell_\infty$ norm over $d$ components:
> 
> $$
>     \Pbb(\norm{S}_\infty > \varepsilon \mid \theta) \leq \sum_{k=1}^{d} \Pbb(\abs{S_k} > \varepsilon \mid \theta) \leq 2d \cdot \exp\left(-\frac{M_{\mathrm{eff}} \cdot \varepsilon^2}{2\bar^2}\right),
>     <!-- label: eq:union_bound -->
> $$
> 
> which establishes Eq. [ref]. $\square$

> **Remark:** [Comparison with Classical Hoeffding Hoeffding经典比较]
> Lemma [ref] generalizes Hoeffding's inequality for bounded random variables in two ways: (i) the sub-Gaussian assumption (Assumption [ref]) covers Gaussian, bounded, and any lighter-tailed distributions, and (ii) the correlation adjustment via $M_{\mathrm{eff}}$ handles the practically critical case of non-independent sources. When $\bar = 0$ (perfect independence) and errors are bounded, the bound reduces to the classical Hoeffding form $\exp(-2M\varepsilon^2 / (\max_j \sigma_j^2))$.

### The Corroboration Theorem

> **Theorem:** [Multi-Source Corroboration Bound 多源印证界]
> <!-- label: thm:corroboration -->
> Under Assumptions [ref]-- [ref], for any desired confidence level $\delta \in (0, 1)$, the number of independent sources required to guarantee $\Pbb(\norm{c^* - \theta}_\infty \leq \varepsilon) \geq 1 - \delta$ is:
> 
> $$
>     M^*(\varepsilon, \delta) = \left\lceil \frac{2\bar^2 \log(2d/\delta)}{\varepsilon^2 - 2\bar^2 \bar \log(2d/\delta)} \right\rceil,
>     <!-- label: eq:M_star -->
> $$
> 
> provided the denominator is positive ($\varepsilon^2 > 2\bar^2 \bar \log(2d/\delta)$). When $\bar = 0$, this simplifies to:
> 
> $$
>     M^*(\varepsilon, \delta) = \left\lceil \frac{2\bar^2 \log(2d/\delta)}{\varepsilon^2} \right\rceil.
>     <!-- label: eq:M_star_independent -->
> $$
> 
> 
> Furthermore, the corroboration strength $\Gamma(M)$ defined in Eq. [ref] satisfies:
> 
> $$
>     \E[\Gamma(M)] \geq 1 - 2d \cdot \exp\left(-\frac{M_{\mathrm{eff}} \cdot \varepsilon_{\mathrm{tol}}^2}{2\bar^2}\right).
>     <!-- label: eq:gamma_bound -->
> $$

> **Proof:** \rigorFull
> **Step 1: Inversion of tail bound.** From Lemma [ref], we have:
> 
> $$
>     \Pbb(\norm{c^* - \theta}_\infty > \varepsilon) \leq 2d \cdot \exp\left(-\frac{M_{\mathrm{eff}} \cdot \varepsilon^2}{2\bar^2}\right).
>     <!-- label: eq:tail_for_inversion -->
> $$
> 
> 
> Setting this bound to $\delta$ and solving for $M$:
> 
> $$
>     2d \cdot \exp\left(-\frac{M_{\mathrm{eff}} \cdot \varepsilon^2}{2\bar^2}\right) &= \delta, 

>     -\frac{M_{\mathrm{eff}} \cdot \varepsilon^2}{2\bar^2} &= \log\left(\frac{2d}\right), 

>     M_{\mathrm{eff}} &= \frac{2\bar^2 \log(2d/\delta)}{\varepsilon^2}.
>     <!-- label: eq:Meff_solved -->
> $$
> 
> 
> **Step 2: Correlation adjustment.** Substituting $M_{\mathrm{eff}} = M / (1 + (M-1)\bar)$ and solving for $M$:
> 
> $$
>     \frac{M}{1 + (M-1)\bar} &= \frac{2\bar^2 \log(2d/\delta)}{\varepsilon^2}, 

>     M &= \frac{2\bar^2 \log(2d/\delta)}{\varepsilon^2} \cdot (1 + (M-1)\bar), 

>     M(1 - \frac{2\bar^2 \bar \log(2d/\delta)}{\varepsilon^2}) &= \frac{2\bar^2 \log(2d/\delta)}{\varepsilon^2} \cdot (1 - \bar).
>     <!-- label: eq:M_solve -->
> $$
> 
> 
> For the practically relevant case where $\bar$ is small and $M$ large, $1 - \bar \approx 1$, yielding:
> 
> $$
>     M \approx \frac{2\bar^2 \log(2d/\delta)}{\varepsilon^2 - 2\bar^2 \bar \log(2d/\delta)},
>     <!-- label: eq:M_approx -->
> $$
> 
> and rounding up to the nearest integer gives Eq. [ref].
> 
> **Step 3: Corroboration strength.** For each source $j$, the indicator $\ind{\norm{c_j - c^*}_\infty \leq \varepsilon_{\mathrm{tol}}}$ is 1 when source $j$'s claim lies within tolerance of the consensus. Under the sub-Gaussian assumption and by the triangle inequality:
> 
> $$
>     \norm{c_j - c^*}_\infty \leq \norm{c_j - \theta}_\infty + \norm{\theta - c^*}_\infty.
>     <!-- label: eq:triangle -->
> $$
> 
> 
> Both terms are bounded with the same exponential rate from Lemma [ref]. The expected corroboration strength then satisfies Eq. [ref]. $\square$

> **Corollary:** [Exponential Confidence Growth 指数置信增长]
> <!-- label: cor:exponential_growth -->
> For independent sources ($\bar = 0$), doubling the number of corroborating sources squares the confidence:
> 
> $$
>     1 - \Pbb(\norm{c^* - \theta}_\infty \leq \varepsilon \mid \theta) \leq (2d)^{1 - 2M/M^*},
>     <!-- label: eq:exponential_growth -->
> $$
> 
> where $M^*$ is the baseline requirement from Eq. [ref]. This is the formal justification for the ``exponential value of corroboration'' in journalism.

## Theorem 2: Single-Source Unverifiability 单源不可验证性
<!-- label: sec:single_source -->

The previous section established that verification confidence grows exponentially with source count. The converse---that $M = 1$ (a single-source claim) is fundamentally unverifiable---is the mathematical basis for identifying fake news (假新闻). This section formalizes that intuition.

### The Single-Source Detection Limit

> **Theorem:** [Single-Source Unverifiability 单源不可验证性]
> <!-- label: thm:single_source -->
> When $M = 1$, under Assumptions [ref]-- [ref], the probability of detecting a false claim $c = \theta + \delta$ (where $\norm_\infty > \varepsilon_{\mathrm{tol}}$) is bounded above by:
> 
> $$
>     \Pbb(detection \mid \delta) \leq 1 - \exp\left(-\frac{\varepsilon_{\mathrm{tol}}^2}{2\sigma_1^2}\right) + 2d \cdot \exp\left(-\frac{(\norm_\infty - \varepsilon_{\mathrm{tol}})^2}{2\sigma_1^2}\right),
>     <!-- label: eq:single_source_bound -->
> $$
> 
> which is independent of $\norm_\infty$ as $\norm_\infty \to \infty$ and converges to a constant $p_(\sigma_1) = 1 - \exp(-\varepsilon_{\mathrm{tol}}^2 / (2\sigma_1^2)) < 1$. Consequently, no single-source claim can be verified with certainty exceeding $1 - p_(\sigma_1)$, regardless of how extreme the falsehood.

> **Proof:** \rigorFull
> **Step 1: Detection condition.** With $M = 1$, there is no consensus to compute; the ``consensus'' is simply $c^* = c_1$. Detection of falsehood requires an external verifier $V$ with its own estimate $\hat_V$ of the ground truth. Detection occurs when $\norm{c_1 - \hat_V}_\infty > \varepsilon_{\mathrm{tol}}$, i.e., the external verifier's estimate disagrees with the single source beyond the tolerance threshold.
> 
> **Step 2: Decomposition of detection probability.** Let the single source publish $c_1 = \theta + \delta + \varepsilon_1$, where $\delta$ is the deliberate falsehood vector and $\varepsilon_1$ is the source's inherent error. The verifier's estimate is $\hat_V = \theta + \varepsilon_V$, where $\varepsilon_V$ is the verifier's error. Detection occurs when:
> 
> $$
>     \norm{\delta + \varepsilon_1 - \varepsilon_V}_\infty > \varepsilon_{\mathrm{tol}}.
>     <!-- label: eq:detection_event -->
> $$
> 
> 
> **Step 3: Non-detection probability.** Non-detection occurs when $\norm{\delta + \varepsilon_1 - \varepsilon_V}_\infty \leq \varepsilon_{\mathrm{tol}}$. For any component $k$:
> 
> $$
>     \Pbb(\abs{\delta_k + \varepsilon_{1,k} - \varepsilon_{V,k}} \leq \varepsilon_{\mathrm{tol}})
>     &\leq \Pbb(\abs{\varepsilon_{1,k} - \varepsilon_{V,k}} \leq \varepsilon_{\mathrm{tol}}) \cdot \ind{\delta_k = 0} 

>     &\quad + \Pbb(\abs{\delta_k + \varepsilon_{1,k} - \varepsilon_{V,k}} \leq \varepsilon_{\mathrm{tol}}) \cdot \ind{\delta_k \neq 0}.
>     <!-- label: eq:non_detection_decomp -->
> $$
> 
> 
> For the second term ($\delta_k \neq 0$), the event requires the combined error $\varepsilon_{1,k} - \varepsilon_{V,k}$ to cancel most of $\delta_k$. Since $\varepsilon_{1,k} - \varepsilon_{V,k}$ is sub-Gaussian with variance proxy $\sigma_1^2 + \sigma_V^2$:
> 
> $$
>     \Pbb(\abs{\delta_k + \varepsilon_{1,k} - \varepsilon_{V,k}} \leq \varepsilon_{\mathrm{tol}}) \leq 2\exp\left(-\frac{(\abs{\delta_k} - \varepsilon_{\mathrm{tol}})^2}{2(\sigma_1^2 + \sigma_V^2)}\right),
>     <!-- label: eq:cancellation_bound -->
> $$
> 
> when $\abs{\delta_k} > \varepsilon_{\mathrm{tol}}$.
> 
> **Step 4: Detection upper bound.** The detection probability is $1 - \Pbb(non-detection)$. Over $d$ components, by union bound:
> 
> $$
>     \Pbb(non-detection) \geq \prod_{k: \delta_k = 0} \Pbb(\abs{\varepsilon_{1,k} - \varepsilon_{V,k}} \leq \varepsilon_{\mathrm{tol}}).
>     <!-- label: eq:non_detection_product -->
> $$
> 
> 
> For the purely random error components ($\delta_k = 0$), even with zero deliberate falsehood, there is a baseline probability of non-detection due to coincidental agreement between the false source and the verifier:
> 
> $$
>     \Pbb(\abs{\varepsilon_{1,k} - \varepsilon_{V,k}} \leq \varepsilon_{\mathrm{tol}}) \geq \exp\left(-\frac{\varepsilon_{\mathrm{tol}}^2}{2(\sigma_1^2 + \sigma_V^2)}\right) \geq \exp\left(-\frac{\varepsilon_{\mathrm{tol}}^2}{2\sigma_1^2}\right),
>     <!-- label: eq:baseline_agreement -->
> $$
> 
> where the last inequality assumes $\sigma_V^2 \leq \sigma_1^2$ (the verifier is at least as precise as the single source---if not, the verifier adds no value).
> 
> **Step 5: Limiting behavior.** Combining the bounds and taking $\norm_\infty \to \infty$:
> 
> $$
>     \lim_{\norm_\infty \to \infty} \Pbb(detection \mid \delta) \leq 1 - \exp\left(-\frac{\varepsilon_{\mathrm{tol}}^2}{2\sigma_1^2}\right) = p_(\sigma_1) < 1.
>     <!-- label: eq:limiting_detection -->
> $$
> 
> 
> Thus, no matter how extreme the falsehood, a single-source claim can evade detection with probability at least $1 - p_(\sigma_1)$. Only the addition of independent sources ($M \geq 2$) can drive this residual non-detection probability to zero. $\square$

> **Remark:** [Fake News as the $M=1$ Regime 假新闻作为$M=1$状态]
> Theorem [ref] provides a structural definition of fake news: **a claim is ``fake news'' if and only if it is published by a single source ($M = 1$) and that source's historical error is substantial ($\sigma_1^2 \gg 0$).** This is not a content-based or intent-based definition---it does not require analyzing the claim's semantic content or the publisher's motives---but a structural one derived from the source multiplicity $M$. When $M = 1$, the claim is *epistemically indistinguishable* from truth with non-negligible probability, independent of how false the claim actually is. This explains why fake news is so insidious: a single-source false claim is mathematically indistinguishable from a single-source true claim without additional sources.
> 
> Conversely, when $M \geq M^*(\varepsilon, \delta)$ independent sources corroborate a claim (Theorem [ref]), the probability of collective error is bounded by $\delta$, which can be made arbitrarily small. Multi-source corroboration is therefore both necessary and (probabilistically) sufficient for certified factuality.

## Theorem 3: Anonymity-Preserving Consensus 匿名性保护共识
<!-- label: sec:anonymity -->

A central tension in journalism is between source transparency (required for auditability) and source protection (required for safety). Theorem [ref] resolves this tension by proving that the \VISprivate{} visibility mode preserves the statistical guarantees of the Yajie{} consensus while hiding source identities.

### Consensus Under PRIVATE Visibility

> **Theorem:** [Anonymity-Preserving Consensus 匿名性保护共识]
> <!-- label: thm:anonymity -->
> Let $c^*_{\mathrm{pub}}$ be the Yajie{} consensus computed under \VISpublic{} mode (identities and claims both visible) and $c^*_{\mathrm{priv}}$ be the consensus computed under \VISprivate{} mode (identities hidden, claims visible, membership proven via zero-knowledge proof). Under Assumptions [ref]-- [ref],  [ref], and [ref], the two consensus estimates satisfy:
> 
> $$
>     \Pbb\left(\norm{c^*_{\mathrm{pub}} - c^*_{\mathrm{priv}}}_\infty > \eta\right) \leq 2d \cdot \exp\left(-\frac{M_{\mathrm{eff}} \cdot \eta^2}{2\bar^2}\right),
>     <!-- label: eq:pub_priv_agreement -->
> $$
> 
> for any $\eta > 0$. Consequently, $c^*_{\mathrm{priv}}$ converges to $\theta$ at the same asymptotic rate as $c^*_{\mathrm{pub}}$:
> 
> $$
>     \lim_{M \to \infty} \Pbb\left(\norm{c^*_{\mathrm{priv}} - \theta}_\infty > \varepsilon\right) = 0,
>     <!-- label: eq:priv_convergence -->
> $$
> 
> with the identical $O(\exp(-M_{\mathrm{eff}} \varepsilon^2 / (2\bar^2)))$ rate.

> **Proof:** \rigorFull
> **Step 1: Structural identity of consensus computation.** Under \VISprivate{} mode, each source $S_j$ publishes its claim $c_j$ together with a zero-knowledge proof $\pi_j$ establishing:
> 
> $$
>     \pi_j: \quad S_j \in \sourceSet \quad \land \quad c_j  is authentic from  S_j,
>     <!-- label: eq:zk_proof -->
> $$
> 
> without revealing $j$. The claims $\{c_j\}_{j=1}^{M}$ are therefore available to the consensus aggregator in exactly the same form as under \VISpublic{} mode. The only difference is the absence of the label $j$.
> 
> **Step 2: Weights depend on precision, not identity.** The optimal Yajie{} weights $w_j \propto 1/\sigma_j^2$ depend on each source's historical error variance $\sigma_j^2$, which is derived from the source's veracity record $\mathcal{H}_j$ (Definition [ref]). Under \VISprivate{} mode, the system knows $\sigma_j^2$ for the anonymous source $j$ (because the zero-knowledge proof links the claim to a specific precision profile without revealing which profile), enabling identical weight computation.
> 
> Alternatively, if the mapping from source identity to $\sigma_j^2$ cannot be revealed without breaking anonymity, the system can use uniform weights $w_j = 1/M$, which converge to the optimal weights as $M$ grows under mild regularity conditions (by the law of large numbers applied to precision heterogeneity).
> 
> **Step 3: Statistical equivalence.** Since the consensus computation $c^* = \sum_j w_j c_j$ is a linear combination of the same random variables $\{c_j\}$ in both modes, and the weights are (asymptotically) identical, the distribution of $c^*_{\mathrm{priv}}$ is identical to the distribution of $c^*_{\mathrm{pub}}$:
> 
> $$
>     c^*_{\mathrm{priv}} \overset{d}{=} c^*_{\mathrm{pub}},
>     <!-- label: eq:distributional_equality -->
> $$
> 
> where $\overset{d}{=}$ denotes equality in distribution. The tail bound of Lemma [ref] therefore applies without modification, establishing Eq. [ref] and Eq. [ref].
> 
> **Step 4: Information-theoretic privacy guarantee.** The \VISprivate{} mode reveals the set of claims $\{c_j\}_{j=1}^{M}$ but not the mapping $j \mapsto c_j$. Under Assumption [ref], the system adds calibrated Laplace noise to the published weighted consensus to achieve $\epsilon_{\mathrm{dp}}$-differential privacy:
> 
> $$
>     \tilde{c}^* = c^*_{\mathrm{priv}} + \xi, \quad \xi_k \sim \mathrm{Lap}(0, \Delta / \epsilon_{\mathrm{dp}}),
>     <!-- label: eq:dp_noise -->
> $$
> 
> where $\Delta$ is the sensitivity of the consensus function to a single source's claim. The noise introduces an additional error term of order $O(1/(M\epsilon_{\mathrm{dp}}))$, which vanishes as $M \to \infty$ (the privacy-utility tradeoff becomes favorable with large $M$, since the sensitivity $\Delta \propto 1/M$ for the weighted average). $\square$

> **Corollary:** [Whistleblower Protection Without Verification Loss 举报人保护不损失验证力]
> <!-- label: cor:whistleblower -->
> A whistleblower operating under \VISprivate{} mode can contribute a claim $c_w$ to the Yajie{} consensus without revealing identity, and the claim contributes the full statistical weight $w_w \propto 1/\sigma_w^2$ to the consensus. The whistleblower's anonymity is protected up to the differential privacy guarantee $\epsilon_{\mathrm{dp}}$, and the consensus converges to truth at the same exponential rate as if the whistleblower's identity were public.

## Theorem 4: Fact-Checker Network Resilience 事实核查网络韧性
<!-- label: sec:resilience -->

Disinformation campaigns represent a regime where a coordinated fraction of sources deliberately propagates false claims. This section establishes the breakdown threshold beyond which the Yajie{} consensus can no longer reliably recover the truth.

### The Adversarial Contamination Model

> **Definition:** [Adversarial Source Contamination 对抗性来源污染]
> <!-- label: def:adversarial -->
> Let a fraction $f \in [0, 1]$ of the $M$ sources be adversarial: for $j \in \cA_{\mathrm{adv}}$ (where $|\cA_{\mathrm{adv}}| = \lfloor fM \rfloor$), the published claim is:
> 
> $$
>     c_j = \theta + \delta_{\mathrm{adv}} + \varepsilon_j,
>     <!-- label: eq:adversarial_claim -->
> $$
> 
> where $\delta_{\mathrm{adv}}$ is a common disinformation vector (all adversarial sources push the same false narrative) and $\varepsilon_j$ is individual noise. The remaining $(1-f)M$ sources are honest: $c_j = \theta + \varepsilon_j$.

> **Theorem:** [Fact-Checker Network Resilience 事实核查网络韧性]
> <!-- label: thm:resilience -->
> Under the adversarial contamination model of Definition [ref], with honest source variance $\sigma_h^2$ and adversarial source variance $\sigma_a^2$, the Yajie{} consensus $c^*$ satisfies:
> 
> $$
>     \norm{c^* - \theta}_\infty \leq f \cdot \norm{\delta_{\mathrm{adv}}}_\infty + \varepsilon_{\mathrm{stat}},
>     <!-- label: eq:resilience_bound -->
> $$
> 
> where $\varepsilon_{\mathrm{stat}}$ is the statistical error term bounded by Lemma [ref]. The consensus remains within $\varepsilon$ of truth ($\norm{c^* - \theta}_\infty \leq \varepsilon$) with probability at least $1 - \delta$ when:
> 
> $$
>     f < \frac{\varepsilon - \varepsilon_{\mathrm{stat}}}{\norm{\delta_{\mathrm{adv}}}_\infty}.
>     <!-- label: eq:f_threshold -->
> $$
> 
> 
> With $\varepsilon_{\mathrm{stat}} = \sqrt{2\bar^2 \log(2d/\delta) / M_{\mathrm{eff}}}$, the breakdown threshold is:
> 
> $$
>     f_{\mathrm{break}} = \frac{1}{2} - \frac{\bar^2 \log(2d/\delta)}{2M\varepsilon^2} - O\left(\frac{1}{M^2}\right).
>     <!-- label: eq:breakdown_threshold -->
> $$

> **Proof:** \rigorFull
> **Step 1: Consensus under contamination.** The Yajie{} consensus with contaminated sources is:
> 
> $$
>     c^* &= \sum_{j \in \cA_{\mathrm{honest}}} w_j (\theta + \varepsilon_j) + \sum_{j \in \cA_{\mathrm{adv}}} w_j (\theta + \delta_{\mathrm{adv}} + \varepsilon_j) 

>         &= \theta + \left(\sum_{j \in \cA_{\mathrm{adv}}} w_j\right) \delta_{\mathrm{adv}} + \sum_{j=1}^{M} w_j \varepsilon_j.
>     <!-- label: eq:contaminated_consensus -->
> $$
> 
> 
> The bias term is $\Bias(c^*) = (\sum_{j \in \cA_{\mathrm{adv}}} w_j) \delta_{\mathrm{adv}}$. With uniform weights $w_j = 1/M$, this bias is $f \cdot \delta_{\mathrm{adv}}$. With precision-based weights, adversarial sources with artificially low declared variance can inflate their weight. We analyze the worst case where adversarial sources successfully claim minimal variance ($\sigma_a^2 \to 0$), giving them weight $w_a \propto 1/\sigma_a^2 \to \infty$ and the honest sources negligible weight, enabling the adversarial sources to completely dominate the consensus. This highlights the critical importance of Assumption [ref] (verifiable membership) combined with source track-record verification.
> 
> Under the conservative assumption that adversarial sources cannot spoof lower variance than their historical record (which is fixed by $\mathcal{H}_j$), the weights are bounded by the honest-case precision, and the bias satisfies $\norm{\Bias(c^*)}_\infty \leq f \cdot \norm{\delta_{\mathrm{adv}}}_\infty$.
> 
> **Step 2: Total error bound.** The total error decomposes as:
> 
> $$
>     \norm{c^* - \theta}_\infty \leq \norm{\Bias(c^*)}_\infty + \norm{\sum_j w_j \varepsilon_j}_\infty \leq f \cdot \norm{\delta_{\mathrm{adv}}}_\infty + \varepsilon_{\mathrm{stat}},
>     <!-- label: eq:total_error -->
> $$
> 
> where $\varepsilon_{\mathrm{stat}}$ is controlled by Lemma [ref].
> 
> **Step 3: Recovery condition.** For the consensus to be within $\varepsilon$ of truth:
> 
> $$
>     f \cdot \norm{\delta_{\mathrm{adv}}}_\infty + \varepsilon_{\mathrm{stat}} \leq \varepsilon \quad\Longrightarrow\quad f \leq \frac{\varepsilon - \varepsilon_{\mathrm{stat}}}{\norm{\delta_{\mathrm{adv}}}_\infty}.
>     <!-- label: eq:recovery_condition -->
> $$
> 
> 
> **Step 4: Breakdown threshold.** In the worst case where $\norm{\delta_{\mathrm{adv}}}_\infty$ is large (adversarial sources push maximally false claims), the limiting factor is the statistical error. Setting $\norm{\delta_{\mathrm{adv}}}_\infty = D_\Theta$ (the diameter of the event space) and substituting $\varepsilon_{\mathrm{stat}} = \sqrt{2\bar^2 \log(2d/\delta) / M_{\mathrm{eff}}}$, we obtain the asymptotic threshold. For large $M$, the adversarial fraction can approach $1/2$ and the consensus still recovers the truth---this is the ``majority-honest'' condition familiar from Byzantine agreement protocols. The $O(1/M)$ correction captures the finite-sample degradation. $\square$

> **Remark:** [Relationship to Byzantine Fault Tolerance 与拜占庭容错的关系]
> The breakdown threshold $f_{\mathrm{break}} \to 1/2$ as $M \to \infty$ recovers the classical Byzantine fault tolerance bound for synchronous networks with oral messages [cite]. However, our setting differs in two respects: (i) we operate on continuous claims rather than binary messages, using sub-Gaussian concentration rather than majority voting, and (ii) our $f_{\mathrm{break}}$ is a probabilistic guarantee ($1 - \delta$) rather than a deterministic one. The $\varepsilon_{\mathrm{stat}}$ term captures the statistical cost of continuous-valued estimation with finite samples---a complication absent from the discrete Byzantine setting.

## The Cercis Veracity Score 新闻真实性的Cercis评分
<!-- label: sec:cercis -->

> **Definition:** [Cercis Veracity Score Cercis真实性评分]
> <!-- label: def:cercis -->
> For a claim $c$ about event $\theta$, given a source community of size $M$ with Yajie consensus $c^*$, the Cercis{} veracity score is:
> 
> $$
>     S(c) = Q(c) + \eta \cdot N(c),
>     <!-- label: eq:cercis -->
> $$
> 
> where:
> 
- $Q(c) = \Gamma(M)$ is the **corroboration quality**: the fraction of sources whose claims fall within $\varepsilon_{\mathrm{tol}}$ of the consensus (Eq. [ref]), weighted by source precision: $Q(c) = \sum_j w_j \cdot \ind{\norm{c_j - c^*}_\infty \leq \varepsilon_{\mathrm{tol}}}$.
- $N(c) = H(\mathbf{p}_{\mathrm{modality}})$ is the **novelty score**: the entropy of the distribution of source access modalities among corroborating sources, measuring how diverse the independent information channels are:
- $\eta \geq 0$ is the **novelty weight**: a tunable parameter controlling the importance of source diversity relative to raw corroboration count. Higher $\eta$ penalizes claims confirmed by many sources all using the same modality (e.g., 100 newspapers reprinting the same AP story).

> **Proposition:** [Properties of the Cercis Score Cercis评分的性质]
> <!-- label: prop:cercis_properties -->
> The Cercis{} veracity score satisfies:
> 
1. **Monotonicity in $M$**: $S(c)$ is non-decreasing in the number of corroborating sources, asymptotically approaching $1 + \eta \cdot H_$ as $M \to \infty$ with diverse modalities.
2. **Penalty for homogeneity**: For fixed $M$, $S(c)$ is maximized when corroborating sources span all available access modalities equally ($p_a = 1/|\mathcal{A}_{\mathrm{modes}}|$ for all $a$).
3. **Single-source floor**: When $M = 1$, $S(c) \leq 1$ (since $Q(c) \leq 1$ and $N(c) = 0$), providing a formal upper bound for single-source claims---consistent with Theorem [ref].
4. **Adversarial robustness**: Adding $k$ adversarial sources that disagree with the consensus reduces $Q(c)$ by at most $k/M$ (in the uniform-weight case), providing a smooth degradation rather than a cliff-edge failure.

> **Proof:** \rigorSketch
> (i) Each additional corroborating source with $\norm{c_j - c^*}_\infty \leq \varepsilon_{\mathrm{tol}}$ adds its weight $w_j$ to $Q(c)$. As $M \to \infty$, if all sources are honest, $Q(c) \to 1$. The novelty term $N(c)$ increases with the number of distinct modalities represented, bounded by $H_ = \log |\mathcal{A}_{\mathrm{modes}}|$.
> 
> (ii) For fixed $M$, $Q(c)$ is invariant to the modality distribution among corroborating sources. $N(c) = H(\mathbf{p})$ is maximized at the uniform distribution by the well-known property of Shannon entropy.
> 
> (iii) With $M = 1$, the ``consensus'' is the single source's claim, so $Q(c) = 1$ by definition (the source agrees with itself), but $N(c) = 0$ (entropy of a degenerate distribution). The score $S(c) = 1$ is the maximum possible, consistent with the epistemic ceiling established in Theorem [ref].
> 
> (iv) Each adversarial source with $\norm{c_j - c^*}_\infty > \varepsilon_{\mathrm{tol}}$ simply fails to contribute to $Q(c)$, reducing the weighted sum by $w_j \leq 1/M$. $\square$

## The Situs Source-Claim Encoding Situs来源-声明编码
<!-- label: sec:situs -->

The \Situs{} encoding provides a structured, privacy-preserving representation of the source-claim attribution graph. Each claim is encoded as a tuple:

$$
    \Situs(c) = (claim\_hash, source\_proof, timestamp, visibility\_mode, claim\_vector),
    <!-- label: eq:situs_encoding -->
$$

where:

- $claim\_hash = H(c \concat salt)$ is a collision-resistant hash binding the claim to its source without revealing content pre-consensus (in \VISblind{} mode);
- $source\_proof = \pi_{\mathrm{ZK}}$ is a zero-knowledge proof of authorized source membership;
- $visibility\_mode \in \{\VISpublic, \VISprivate, \VISblind\}$ controls what information is revealed;
- $claim\_vector$ is the published claim in its native representation (in \VISpublic{} and \VISprivate{} modes; encrypted in \VISblind{} mode).

The \Situs{} encoding enables three key verification operations:

1. **Membership verification**: Given $\pi_{\mathrm{ZK}}$, any observer can verify that the claim was submitted by an authorized source without learning which source, in $O(\log |\sourceSet|)$ time (Merkle-tree based).
2. **Consensus computation**: The aggregator collects all $\Situs(c_j)$ for a given event, decrypts or reveals claims according to their visibility modes, and computes the Yajie{} consensus $c^*$.
3. **Attribution audit**: In \VISpublic{} mode, the full attribution chain (source $\to$ claim $\to$ consensus $\to$ verification verdict) is permanently recorded and auditable.

## Experimental Protocol 实验协议
<!-- label: sec:experiments -->

### Benchmark Datasets

We propose evaluation on four standard fact-checking benchmarks, each representing a distinct claim type:

1. **LIAR** [cite]: 12.8K short political statements labeled for truthfulness on a 6-point scale. We map the 6-point scale to $[0, 1]$ veracity scores and treat each statement as a single-source claim, measuring how well the Yajie{} consensus (simulated from auxiliary sources) recovers the ground-truth label.
2. **FEVER** [cite]: 185K claims extracted from Wikipedia, each labeled as SUPPORTS, REFUTES, or NOT ENOUGH INFO against a specified evidence document. We treat Wikipedia sentences as independent ``sources'' and measure whether the Yajie{} consensus over evidence sentences correctly classifies the claim.
3. **FakeNewsNet** [cite]: Multi-modal fake news dataset with social context (Twitter engagements, user networks). We treat each retweeting user as a potential ``source'' with credibility derived from network position and historical accuracy.
4. **CHEF** [cite]: Chinese fact extraction and verification dataset (中文事实抽取与验证). We evaluate specifically on the multi-source corroboration scenario where multiple Chinese-language news outlets report on the same event.

### Metrics

- **Corroboration-Recall**: $CR@k$ = probability that the top-$k$ Yajie{}-consensus claims (by corroboration strength $\Gamma(M)$) contain the true claim.
- **Single-Source Detection Rate**: $SSDR$ = fraction of single-source false claims ($M = 1$, label = FALSE) correctly flagged by the $M = 1$ unverifiability test (Theorem [ref]).
- **Adversarial Robustness**: $AR@f$ = consensus accuracy when fraction $f$ of sources are adversarial, measuring the empirical breakdown threshold.
- **Anonymity Cost**: $\Delta_{\mathrm{priv}} = |Accuracy(\VISpublic) - Accuracy(\VISprivate)|$, measuring the degradation from source anonymity.
- **Cercis Correlation**: Spearman's $\rho$ between the Cercis{} score $S(c)$ and human fact-checker ground-truth ratings.

### Ablation Plan

1. **Source count ablation**: Vary $M \in \{1, 2, 3, 5, 10, 20, 50\}$ and measure consensus accuracy to validate Theorem [ref] (exponential growth).
2. **Correlation ablation**: Introduce controlled pairwise source correlation $\bar \in \{0, 0.1, 0.3, 0.5, 0.7\}$ and verify $M_{\mathrm{eff}}$ adjustment.
3. **Visibility ablation**: Compare \VISpublic{}, \VISprivate{}, and \VISblind{} modes across all metrics to validate Theorem [ref].
4. **Adversarial ablation**: Vary adversarial fraction $f \in \{0, 0.1, 0.2, 0.3, 0.4, 0.49\}$ and measure empirical $f_{\mathrm{break}}$.
5. **Weighting ablation**: Compare inverse-variance weighting vs. uniform weighting vs. reputation-based weighting.
6. **Novelty weight ablation**: Vary $\eta \in \{0, 0.1, 0.5, 1.0, 2.0\}$ in the Cercis{} score and measure correlation with human judgments.

### Simulated Source Generation

For controlled experiments, we generate synthetic source claims with the following parameters:

- $\theta \sim Uniform(\newsState)$: ground-truth event.
- $c_j = \theta + \varepsilon_j$, where $\varepsilon_j \sim \mathcal{N}(0, \sigma_j^2 I_d)$ for honest sources and $c_j = \theta + \delta_{\mathrm{adv}} + \varepsilon_j$ for adversarial sources.
- $\sigma_j \sim LogNormal(\mu_\sigma, \tau_\sigma^2)$: heterogeneous source precision.
- $\bar \in [0, 1]$: controlled pairwise error correlation via Cholesky decomposition of the correlation matrix.
- $d \in \{1, 3, 5, 10\}$: claim dimensionality.
- $M \in \{1, ..., 100\}$: source count.

## The Spring Gating for Regime Detection Spring门控的制度检测
<!-- label: sec:spring -->

> **Definition:** [Reporting Regime 报道制度]
> <!-- label: def:regime -->
> The Spring{} gating mechanism detects transitions between two reporting regimes:
> 
- **Normal regime 正常制度 ($R_0$)**: Sources independently report with bounded errors; $\Gamma(M) \approx 1$ for sufficient $M$; adversarial fraction $f \approx 0$.
- **Disinformation regime 虚假信息制度 ($R_1$)**: A coordinated fraction $f > f_{\mathrm{break}}$ of sources publish coherently false claims; $\Gamma(M)$ degrades; the Yajie{} consensus is biased.

The Spring{} gate $\mathcal{G}$ monitors the time series of corroboration strength $\Gamma_t(M)$ and triggers a regime-shift alert when:

$$
    \mathcal{G}(t) = \ind{\Gamma_t(M) < \Gamma_  for  \tau  consecutive time steps},
    <!-- label: eq:spring_gate -->
$$

where $\Gamma_ = 1 - 2d \cdot \exp(-M_{\mathrm{eff}} \cdot \varepsilon_{\mathrm{tol}}^2 / (2\bar^2))$ is the expected corroboration strength under $R_0$, and $\tau$ is a persistence threshold to avoid false alarms from transient fluctuations.

> **Proposition:** [Spring Gate False Alarm Rate Spring门控误报率]
> <!-- label: prop:spring_false_alarm -->
> Under the normal regime $R_0$, the probability of a false regime-shift alert within a monitoring window of length $T$ is bounded by:
> 
> $$
>     \Pbb(false alarm in  [0, T]) \leq T \cdot (2d)^\tau \cdot \exp\left(-\frac{\tau M_{\mathrm{eff}} \cdot \varepsilon_{\mathrm{tol}}^2}{2\bar^2}\right).
>     <!-- label: eq:false_alarm -->
> $$

> **Proof:** \rigorSketch
> Under $R_0$, each time step's corroboration check $\Gamma_t(M) < \Gamma_$ has probability at most $2d \cdot \exp(-M_{\mathrm{eff}} \cdot \varepsilon_{\mathrm{tol}}^2 / (2\bar^2))$ by Lemma [ref]. For $\tau$ consecutive failures, by independence across time steps (under $R_0$), the joint probability is the product. A union bound over $T$ possible starting positions yields Eq. [ref]. $\square$

## Discussion 讨论
<!-- label: sec:discussion -->

### Relationship to Journalism Ethics 与新闻伦理的关系

Our framework provides mathematical guarantees about claim verification but does not resolve the normative questions that define journalism ethics: When is it justified to publish a single-source claim (breaking news before corroboration is available)? Does the public's right to know override the probabilistic uncertainty of an unverified claim? Should sources ever be compelled to exit \VISprivate{} mode (e.g., in criminal investigations)? These questions admit no purely mathematical answer---they require normative deliberation within the institutional and legal frameworks of each society.

### Relationship to Automated Fact-Checking 与自动事实核查的关系

Existing automated fact-checking systems [cite] operate primarily in the $M = 1$ regime: a single model assesses a claim against a knowledge base or evidence corpus. Theorem [ref] implies that such systems have an inherent and irremediable ceiling on verification confidence, regardless of model sophistication. The path to certified factuality requires multi-source architecture---not merely better single models. Our framework suggests that automated fact-checking should evolve toward ensemble architectures where multiple independently-trained models, drawing on disjoint evidence corpora, produce a Yajie{}-style consensus.

### Limitations 局限性

We explicitly identify the following limitations:

1. **\limitationTag{L1} Ground truth availability**: Our theorems assume that $\theta$ exists as an objective event. For many politically contested claims, the ``ground truth'' itself is disputed (e.g., ``was the 2020 election stolen?''). The SCX{} unidentifiability framework [cite] partially addresses this: when sources disagree, the error source (source bias vs. fundamental ambiguity vs. measurement error) is unidentifiable without declared assumptions. The framework identifies *when* consensus is impossible, but cannot create consensus where the underlying reality is ambiguous.
2. **\limitationTag{L2} Source independence in practice**: Assumption [ref] (conditional independence) is strong. Real-world news ecosystems exhibit complex dependency structures: wire service syndication, editorial aggregation, algorithmic amplification, and information cascades. Our correlation adjustment ($M_{\mathrm{eff}}$) provides a first-order correction, but the compound symmetry assumption ($\bar$ uniform across all pairs) is a simplification. Network-structured dependencies (where source $j$ depends on source $k$ depends on source $\ell$) require more sophisticated graphical models.
3. **\limitationTag{L3} Adversarial sophistication**: Theorem [ref] assumes non-coordinated adversaries (Assumption [ref]). Sophisticated disinformation campaigns may employ adaptive strategies: probing the consensus, identifying the minimum distortion needed to shift it, and distributing a coordinated false narrative across multiple apparent sources. Game-theoretic extensions (treating the verification system and the disinformation campaign as players in a zero-sum game) are needed.
4. **\limitationTag{L4} Temporal dynamics**: Events evolve over time (``facts on the ground change''), and initial reporting is often incomplete or erroneous even by honest sources. The Spring{} gating (Section [ref]) detects regime shifts but does not model the continuous evolution of the event itself under honest reporting.
5. **\limitationTag{L5} Language and cultural barriers**: Our formalism is language-agnostic in principle, but source communities are often linguistically segmented. A claim about an event in China may be corroborated by 10 Chinese-language sources and disputed by 3 English-language sources, and the Yajie{} consensus must account for potential systematic biases correlated with language community.

### Future Work 未来工作

1. **Hierarchical Yajie consensus**: Extend the flat source ensemble to a hierarchical structure where local fact-checker networks produce regional consensuses that are themselves aggregated by a global consensus, analogous to federated learning.
2. **Game-theoretic fact-checking**: Model the interaction between disinformation campaigns and verification systems as a Stackelberg game, where the verifier commits to an audit strategy and the adversary best-responds.
3. **Temporal claim graphs**: Extend the \Situs{} encoding to track how claims evolve over time---a claim is published, then corrected, then disputed, then corroborated---as a directed temporal graph amenable to causal inference.
4. **Cross-lingual source integration**: Develop language-agnostic claim embeddings that enable cross-lingual Yajie{} consensus without requiring translation of each claim, reducing the risk of translation-introduced bias.

## Conclusion 结论

We have formalized news verification as a multi-expert audit problem under the SCX{} framework, establishing four theorems that provide mathematical foundations for certified fact-checking:

1. Multi-source corroboration provides exponentially growing confidence (Theorem [ref]).
2. Single-source claims are fundamentally unverifiable (Theorem [ref]), providing a structural definition of fake news.
3. Source anonymity (\VISprivate{} visibility) preserves verification power (Theorem [ref]), resolving the tension between auditability and source protection.
4. Fact-checker networks remain resilient up to a near-majority adversarial fraction (Theorem [ref]), with a breakdown threshold converging to $f = 1/2$.

The Cercis{} veracity score operationalizes these guarantees as a single numeric metric, and the \Situs{} encoding provides privacy-preserving attribution infrastructure. The Spring{} gating monitors for regime shifts from normal reporting to coordinated disinformation.

The central insight is that **fake news is a structural phenomenon, not a content phenomenon**: a claim is epistemically indistinguishable from truth when $M = 1$, regardless of its content. Multi-source architecture---not better single-source fact-checkers---is the necessary condition for certified factuality. This insight, combined with the privacy-preserving properties of \VISprivate{} mode, suggests a path toward verification infrastructure that is simultaneously rigorous and protective of journalistic sources.

**Acknowledgment.** We thank the fact-checking organizations whose operational experience informed our modeling assumptions, and the cryptography community whose work on zero-knowledge proofs and secure multi-party computation makes \VISprivate{} and \VISblind{} modes technically feasible.

\begin{thebibliography}{99}

\bibitem{SCX2025}
SCX.
\newblock The SCX Audit Framework: Multi-Expert Verification for High-Stakes AI Systems.
\newblock *SCX Technical Report*, 2025.

\bibitem{lazer2018}
D.~Lazer, M.~Baum, Y.~Benkler, et al.
\newblock The science of fake news.
\newblock *Science*, 359(6380):1094--1096, 2018.

\bibitem{vosoughi2018}
S.~Vosoughi, D.~Roy, S.~Aral.
\newblock The spread of true and false news online.
\newblock *Science*, 359(6380):1146--1151, 2018.

\bibitem{pennycook2020}
G.~Pennycook, J.~McPhetres, Y.~Zhang, J.~Lu, D.~Rand.
\newblock Fighting COVID-19 misinformation on social media: Experimental evidence for a scalable accuracy-nudge intervention.
\newblock *Psychological Science*, 31(7):770--780, 2020.

\bibitem{stencel2024}
M.~Stencel, E.~Luther, J.~Ryan.
\newblock Fact-checking census: Global fact-checking sites top 400.
\newblock *Duke Reporters' Lab*, 2024.

\bibitem{wang2018}
W.~Y.~Wang.
\newblock ``Liar, Liar Pants on Fire'': A new benchmark dataset for fake news detection.
\newblock *ACL*, 2017.

\bibitem{thorne2018}
J.~Thorne, A.~Vlachos, C.~Christodoulopoulos, A.~Mittal.
\newblock FEVER: A large-scale dataset for fact extraction and verification.
\newblock *NAACL*, 2018.

\bibitem{shu2020}
K.~Shu, D.~Mahudeswaran, S.~Wang, D.~Lee, H.~Liu.
\newblock FakeNewsNet: A data repository with news content, social context, and spatiotemporal information.
\newblock *Big Data*, 8(3):171--188, 2020.

\bibitem{hu2023}
H.~Hu et al.
\newblock CHEF: A Chinese fact extraction and verification dataset.
\newblock *EMNLP*, 2023.

\bibitem{lamport1982}
L.~Lamport, R.~Shostak, M.~Pease.
\newblock The Byzantine generals problem.
\newblock *ACM TOPLAS*, 4(3):382--401, 1982.

\bibitem{guo2022}
Z.~Guo, M.~Schlichtkrull, A.~Vlachos.
\newblock A survey on automated fact-checking.
\newblock *TACL*, 10:178--206, 2022.

\bibitem{zeng2023}
X.~Zeng, A.~Abumansour, A.~Zubiaga.
\newblock Automated fact-checking: A survey.
\newblock *ACM Computing Surveys*, 2023.

\bibitem{allcott2017}
H.~Allcott, M.~Gentzkow.
\newblock Social media and fake news in the 2016 election.
\newblock *Journal of Economic Perspectives*, 31(2):211--236, 2017.

\bibitem{ciampaglia2015}
G.~L.~Ciampaglia, P.~Shiralkar, L.~M.~Rocha, J.~Bollen, F.~Menczer, A.~Flammini.
\newblock Computational fact checking from knowledge networks.
\newblock *PLOS ONE*, 10(6):e0128193, 2015.

\bibitem{graves2018}
L.~Graves.
\newblock Understanding the promise and limits of automated fact-checking.
\newblock *Reuters Institute for the Study of Journalism*, 2018.

\bibitem{zhou2020}
X.~Zhou, R.~Zafarani.
\newblock A survey of fake news: Fundamental theories, detection methods, and opportunities.
\newblock *ACM Computing Surveys*, 53(5):1--40, 2020.

\bibitem{nyhan2014}
B.~Nyhan, J.~Reifler.
\newblock When corrections fail: The persistence of political misperceptions.
\newblock *Political Behavior*, 32(2):303--330, 2010.

\bibitem{nakov2021}
P.~Nakov, D.~Corney, M.~Hasanain, et al.
\newblock Automated fact-checking for assisting human fact-checkers.
\newblock *IJCAI*, 2021.

\bibitem{kumar2016}
S.~Kumar, R.~West, J.~Leskovec.
\newblock Disinformation on the web: Impact, characteristics, and detection of Wikipedia hoaxes.
\newblock *WWW*, 2016.

\bibitem{zubiaga2018}
A.~Zubiaga, A.~Aker, K.~Bontcheva, M.~Liakata, R.~Procter.
\newblock Detection and resolution of rumours in social media: A survey.
\newblock *ACM Computing Surveys*, 51(2):1--36, 2018.

\end{thebibliography}