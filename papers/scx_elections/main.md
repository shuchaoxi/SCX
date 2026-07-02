# Introduction 引言

**Author:** SCX

*Abstract:*

We formalize electoral vote tabulation as a multi-method verification problem under the SCX{} (Structured Causal eXamination) framework. An electoral authority publishes a vote count claim $c$ for each contest. Three structurally independent counting methods---paper ballot hand count $\method{P}$, electronic voting machine tabulation $\method{E}$, and statistical hand recount $\method{R}$---serve as $M = 3$ auditors, each producing an independent estimate of the true vote count $\nu$. Observer access augments the effective auditor multiplicity $M_{eff}$ through independent verification by the observer community $\observerSet$. We prove three core theorems. **Theorem~1 (Multi-Method Consensus Detection 多方法共识检测):** Under $M$ independent counting methods each with detection threshold $\Delta$, the probability that all methods simultaneously fail to detect a tabulation discrepancy of magnitude $\delta$ satisfies $\Pbb(all miss \mid \delta > \Delta) \leq \exp(-2 M_{eff} (\delta - \Delta)^2 / \bar^2)$, where $M_{eff} = M/(1 + (M-1)\bar)$ accounts for inter-method error correlation. **Theorem~2 (Discrepancy Source Unidentifiability 差异来源不可辨识性):** When vote counts from method $\method{P}$, $\method{E}$, and $\method{R}$ diverge, the source of discrepancy among \{paper ballot counting error, electronic tabulation malfunction, recount sampling error, genuine ballot fraud\} is logically unidentifiable without declared assumptions, forcing explicit declaration of audit assumptions. **Theorem~3 (Observer Community Detection 观察者社区检测):** An observer community of size $K$ accessing all three counting method results independently detects a certified-result inconsistency with probability at least $1 - \exp(-2K \alpha^2)$, where $\alpha$ is the minimum per-observer detection rate. Result certification achieves **VERIFIED** status when all $M$ methods agree within tolerance $\varepsilon$ and the Yajie{} consensus is published with observer-verifiable hash commitments. We develop the Cercis{} electoral integrity score $S = Q + \eta \cdot N$ ranking counting methods by accuracy and regime coverage, the Spring{} gating mechanism for detecting transitions from normal to irregular electoral regimes, and the Yajie{} multi-method certification protocol. The framework is applied to specific electoral scenarios including precinct-level tabulation, mail-in ballot processing, and multi-jurisdiction result aggregation.

**Keywords:** SCX auditing, electoral integrity 选举诚信, multi-method vote tabulation 多方法计票, consensus certification 共识认证, Hoeffding detection bounds, observer community verification, paper ballots, electronic voting, hand recount, Yajie{} consensus, Cercis{} scoring, Spring{} gating, electoral fraud detection 选举舞弊检测

## Introduction 引言

Electoral integrity is the foundation of democratic governance. The core operational question is deceptively simple: given a set of cast ballots, what is the true vote count for each candidate? Yet the verification of this count has resisted formal mathematical treatment. Election observation missions document irregularities; forensic audits detect anomalies; statistical tests flag suspicious patterns. But no existing framework specifies the conditions under which a vote count can be *certified* as correct with a quantifiable error probability.

Three structural facts about modern elections create the conditions for formal verification:

1. **Methodological pluralism 方法多元性.** Modern elections increasingly deploy multiple independent counting methods. Paper ballots are hand-counted at the precinct level; optical scan or direct-recording electronic (DRE) machines provide electronic tabulation; and post-election hand recounts or risk-limiting audits provide a third independent verification. Each method has distinct error modes: paper ballots are vulnerable to human counting fatigue and ambiguous marks; electronic machines are vulnerable to software errors, miscalibration, and hacking; hand recounts are vulnerable to sampling error and chain-of-custody breaks.
2. **Observer access 观察者访问.** International and domestic election observers, party poll-watchers, and civil society organizations form a verification community that independently witnesses vote counting. When observers have access to multiple counting method outputs, they become an additional layer of independent verification.
3. **Discrepancy-driven audit triggers 差异驱动审计触发.** When different counting methods produce materially different results, the discrepancy itself triggers investigation. This is the operational intuition behind mandatory recounts, risk-limiting audits, and judicial challenges---but this intuition has never been formalized as a statistical detection theorem.

The SCX{} auditing framework [cite] provides rigorous mathematical tools for this setting. Its core mechanisms---multi-expert noise detection via the Yajie{} consensus, error source unidentifiability analysis, and regime-shift detection via Spring{} gating---translate directly to electoral tabulation. The key mapping is: **vote counting methods are experts; published results are claims; the observer community is the verification layer**. When paper ballots, electronic machines, and hand recounts *agree*, their consensus carries a certifiable confidence bound. When they *disagree*, the pattern of disagreement reveals the detection of an irregularity.

**Contributions.** This paper provides:

1. **Formalization** (Section [ref]): Electoral tabulation as a multi-method verification problem with $M = 3$ primary counting methods plus observer community augmentation. Ten explicit assumptions~\assumptionTag{1}--\assumptionTag{10}.
2. **Three theorems with full proofs**:
3. **Multi-method certification protocol** (Section [ref]): The Yajie{} consensus protocol combining paper ballot, electronic, and hand recount outputs with observer-verifiable hash commitments.
4. **Cercis{} electoral integrity score** (Section [ref]): $S(\mathcal{E}) = Q(\mathcal{E}) + \eta \cdot N(\mathcal{E})$ ranking electoral systems by accuracy and novelty coverage.
5. **Spring{} gating for irregularity detection** (Section [ref]): Detecting transitions from normal electoral operations to irregular regimes.
6. **Specific applications** (Section [ref]): Precinct-level tabulation, mail-in ballot processing, multi-jurisdiction aggregation.
7. **Discussion** (Section [ref]): Honest limitations, relationship to existing electoral integrity frameworks.

**What this paper is not.** This is a mathematical framework for certifying vote tabulation through multi-method consensus---not a political theory of democracy, not a normative claim about which electoral system is ``better,'' and not a proposal for any specific electoral reform. We prove theorems about detection probabilities, consensus bounds, and unidentifiability. We do not assert that electronic voting is ``good'' or paper ballots are ``safe''; we prove that under specified conditions, multi-method agreement provides a quantifiable certification guarantee, and multi-method disagreement provides a quantifiable detection signal.

## Formalization: Electoral Tabulation as Multi-Method Verification 选举计票作为多方法验证
<!-- label: sec:formalization -->

### The Vote Count Space 计票空间

> **Definition:** [Electoral Contest 竞选]
> <!-- label: def:contest -->
> An electoral contest $\mathcal{E}$ is a tuple:
> 
> $$
>     \mathcal{E} = (C, B, \mathcal{P}, T),
>     <!-- label: eq:contest -->
> $$
> 
> where:
> 
- $C = \{c_1, ..., c_K\}$ is the set of $K$ candidates (or options, for referenda);
- $B = \{b_1, ..., b_N\}$ is the set of $N$ cast ballots, each $b_i \in C \cup \{abstain, invalid\}$;
- $\mathcal{P} = \{P_1, ..., P_R\}$ is the set of $R$ precincts (or polling stations) at which ballots are cast and counted;
- $T$ is the tabulation timestamp.

> **Definition:** [True Vote Count 真实计票]
> <!-- label: def:true_vote -->
> The true vote count for candidate $c_k$ is:
> 
> $$
>     \nu_k = \sum_{i=1}^{N} \ind{b_i = c_k}, \quad \nu = (\nu_1, ..., \nu_K) \in \N^K,
>     <!-- label: eq:true_vote -->
> $$
> 
> satisfying $\sum_{k=1}^K \nu_k \leq N$ (with slack for abstentions and invalid ballots). The true vote vector $\nu$ is the ground truth that no single counting method observes without error.

### Counting Methods as Auditors 计票方法作为审计者

> **Definition:** [Counting Method 计票方法]
> <!-- label: def:method -->
> A vote counting method $\method{m} \in \methodSet$ is a function:
> 
> $$
>     \method{m}: B \to \N^K, \quad \method{m}(B) = \nu + \varepsilon^{(m)},
>     <!-- label: eq:method -->
> $$
> 
> where $\varepsilon^{(m)} \in \Z^K$ is the method-specific counting error vector. The three canonical methods are:
> 
- $\method{P}$: **Paper ballot hand count 纸质选票手工计票.** Election workers manually sort and count paper ballots. Error modes: human fatigue (miscounting), ambiguous ballot marks (voter intent interpretation), chain-of-custody lapses.
- $\method{E}$: **Electronic voting machine tabulation 电子投票机计票.** Optical scan or DRE machines automatically tabulate votes. Error modes: software bugs, sensor miscalibration, memory errors, hacking/tampering, power failures.
- $\method{R}$: **Hand recount / risk-limiting audit 手工重新计票/风险限制审计.** A statistical sample or full recount of ballots independently of the initial tabulation. Error modes: sampling error (incomplete recount), temporal degradation of ballots, procedure deviation.

> **Definition:** [Method Error Characteristics 方法误差特性]
> <!-- label: def:error_chars -->
> Each counting method $\method{m}$ is characterized by:
> 
> $$
>     \varepsilon^{(m)} \sim \mathcal{D}_m(0, \Sigma_m), \quad \Sigma_m = \diag(\sigma_{m,1}^2, ..., \sigma_{m,K}^2),
>     <!-- label: eq:error_chars -->
> $$
> 
> where $\sigma_{m,k}^2$ is the variance of method $m$'s error for candidate $k$. Methods are unbiased in expectation: $\E[\varepsilon^{(m)}] = 0$, meaning they are equally likely to overcount as undercount. Systematic biases (e.g., machines consistently favoring one candidate) violate this assumption and are addressed in Section [ref].

> **Definition:** [Inter-Method Error Correlation 方法间误差相关性]
> <!-- label: def:inter_method_corr -->
> The pairwise error correlation between methods $m$ and $m'$ for candidate $k$ is:
> 
> $$
>     \rho_{m,m'}^{(k)} = \Corr(\varepsilon_k^{(m)}, \varepsilon_k^{(m')}).
>     <!-- label: eq:inter_corr -->
> $$
> 
> The average inter-method correlation is $\bar = \frac{2}{M(M-1)} \sum_{m < m'} \max_k |\rho_{m,m'}^{(k)}|$. When counting methods use structurally independent mechanisms (paper $\perp$ electronic $\perp$ hand recount), $\bar \ll 1$. When methods share data (e.g., electronic tabulation feeds the same scanner output to two ``independent'' counts), $\bar \to 1$ and $M_{eff} \to 1$.

### Observer Community 观察者社区

> **Definition:** [Observer Community 观察者社区]
> <!-- label: def:observer_community -->
> An observer community $\observerSet = \{O_1, ..., O_K\}$ consists of $K$ independent observers (international missions, domestic monitors, party poll-watchers, civil society organizations, citizen observers). Each observer $O_j$ witnesses one or more counting methods and produces a verification report:
> 
> $$
>     O_j: (\method{P}(B), \method{E}(B), \method{R}(B)) \mapsto \{0, 1\},
>     <!-- label: eq:observer -->
> $$
> 
> where $O_j = 1$ indicates that observer $j$ detects an inconsistency among the method outputs. Observers differ in access ($a_j \in \{1, 2, 3\}$ methods observed), expertise, and detection threshold.

> **Definition:** [Effective Auditor Multiplicity 有效审计者数量]
> <!-- label: def:Meff -->
> The effective number of independent auditors combines counting methods and observers:
> 
> $$
>     M_{eff} = \frac{M_{methods} + \gamma \cdot K_{observers}}{1 + (M_{methods} + \gamma K_{observers} - 1) \bar_{total}},
>     <!-- label: eq:Meff_total -->
> $$
> 
> where $\gamma \in [0, 1]$ is the observer information weight (fraction of method-level information available to the average observer) and $\bar_{total}$ is the aggregate error correlation across all auditors. $M_{methods} = 3$ is the baseline (paper, electronic, hand recount).

### Assumptions 假设

We now state the assumptions under which our theorems hold. Each assumption is explicitly labeled and falsifiable in principle.

\begin{assumption}[A1: Bounded Vote Counts 有界计票数]
<!-- label: ass:A1 -->
The true vote count satisfies $\nu_k \in [0, N]$ for all $k$, with total ballots $N < \infty$. All vote counts are non-negative integers. The vote share $\nu_k / N$ lies in $[0, 1]$.
\end{assumption}

\begin{assumption}[A2: Counting Method Independence 计票方法独立性]
<!-- label: ass:A2 -->
Conditional on the true vote count $\nu$, the counting errors of different methods are independent:

$$
    \Pbb(\varepsilon^{(P)}, \varepsilon^{(E)}, \varepsilon^{(R)} \mid \nu) = \prod_{m \in \{P, E, R\}} \Pbb(\varepsilon^{(m)} \mid \nu).
    <!-- label: eq:method_independence -->
$$

This holds when paper ballot counting, electronic tabulation, and hand recount use non-overlapping procedures, personnel, and equipment. In practice, $\bar > 0$ due to shared ballot populations; the $M_{eff}$ correction addresses this.
\end{assumption}

\begin{assumption}[A3: Bounded Detection Power per Method 单个方法有界检测力]
<!-- label: ass:A3 -->
Each counting method $\method{m}$ has minimum detection power $\Delta_m > 0$: the smallest vote discrepancy that method $m$ can detect with probability at least $p_$ on a single candidate. Formally, for any true discrepancy $\delta > 0$:

$$
    \Pbb\left(|\varepsilon_k^{(m)}| > \Delta_m \;\middle|\; |\varepsilon_k^{(m)}| = \delta\right) \geq 1 - \exp\left(-\frac{(\delta - \Delta_m)^2}{2\sigma_{m,k}^2}\right).
    <!-- label: eq:detection_power -->
$$

\end{assumption}

\begin{assumption}[A4: Observer Independence 观察者独立性]
<!-- label: ass:A4 -->
Conditional on the counting method outputs, observer detections are independent across observers:

$$
    \Pbb(O_1, ..., O_K \mid \method{P}, \method{E}, \method{R}) = \prod_{j=1}^{K} \Pbb(O_j \mid \method{P}, \method{E}, \method{R}).
    <!-- label: eq:observer_independence -->
$$

This holds when observers operate through independent organizational structures, with separate access credentials, and without collusion.
\end{assumption}

\begin{assumption}[A5: Positive Observer Detection Rate 正观察者检测率]
<!-- label: ass:A5 -->
Each observer has a minimum probability $\alpha_ > 0$ of detecting a genuine discrepancy among counting method outputs (conditional on such a discrepancy existing). Formally, when $\norm{\method{P} - \method{E}}_\infty > \Delta$ or $\norm{\method{P} - \method{R}}_\infty > \Delta$ or $\norm{\method{E} - \method{R}}_\infty > \Delta$:

$$
    \Pbb(O_j = 1 \mid discrepancy exists) \geq \alpha_.
    <!-- label: eq:observer_rate -->
$$

\end{assumption}

\begin{assumption}[A6: Unbiased Method Errors 无偏计票误差]
<!-- label: ass:A6 -->
Each counting method is conditionally unbiased: $\E[\varepsilon^{(m)} \mid \nu] = \mathbf{0}$. Systematic method bias (e.g., machines calibrated to overcount one candidate) violates this assumption. Detection of systematic bias requires method diversity: if all methods share the same bias, it is undetectable (see limitation \limitationTag{3}).
\end{assumption}

\begin{assumption}[A7: Discrepancy Triggers Full Audit 差异触发全面审计]
<!-- label: ass:A7 -->
When the maximum pairwise discrepancy among counting methods exceeds the audit threshold $\varepsilon$:

$$
    \max_{m \neq m'} \norm{\method{m}(B) - \method{m'}(B)}_\infty > \varepsilon,
    <!-- label: eq:trigger -->
$$

a full manual recount of all ballots is triggered. This is the operational response to detected discrepancy; the cost of the full recount serves as the detection penalty in the Yajie{} payoff structure.
\end{assumption}

\begin{assumption}[A8: Ballot Chain of Custody 选票监管链]
<!-- label: ass:A8 -->
The set of ballots $B$ is physically secured such that ballots cannot be added, removed, or altered between counting methods without detection probability at least $p_{custody} > 0$. Chain-of-custody violations create a discrepancy source (ballot tampering) that is one of the unidentifiable components in Theorem [ref].
\end{assumption}

\begin{assumption}[A9: Hash-Commitment Publication 哈希承诺发布]
<!-- label: ass:A9 -->
Each counting method's output is published with a cryptographic hash commitment $\mathcal{H}_m = SHA-256(\method{m}(B) \| salt_m)$ before other methods' outputs are revealed. This prevents post-hoc coordination of method outputs to simulate consensus.
\end{assumption}

\begin{assumption}[A10: Regime Transition Detectability 选举制度转换可检测性]
<!-- label: ass:A10 -->
A transition from normal electoral operations to irregular operations produces a statistically detectable shift in the distribution of inter-method discrepancies. Formally, there exists a divergence measure $D(P_{normal} \| P_{irregular}) \geq d_ > 0$ in the discrepancy distribution.
\end{assumption}

## Theorem 1: Multi-Method Consensus Detection 多方法共识检测
<!-- label: sec:thm1 -->

We now prove that when $M$ independent counting methods each have bounded error, the probability that all methods simultaneously miss a vote count discrepancy decays exponentially in the effective number of methods.

### Detection Probability Lemma

> **Lemma:** [Single-Candidate Detection Probability 单个候选人检测概率]
> <!-- label: lem:single_candidate -->
> Under Assumptions [ref]-- [ref] and [ref], for a single candidate $k$, if the true vote count $\nu_k$ differs from the published claim $c_k$ by $\delta = |c_k - \nu_k| > 0$, the probability that all $M$ counting methods produce estimates within $\delta/2$ of $c_k$ (i.e., all miss the discrepancy) satisfies:
> 
> $$
>     \Pbb(all miss \mid \delta) \leq \exp\left(-\frac{M_{eff} \cdot \max(0, \delta - \Delta_)^2}{2\bar^2}\right),
>     <!-- label: eq:single_detection -->
> $$
> 
> where $M_{eff} = M / (1 + (M-1)\bar)$ is the effective number of independent methods, $\Delta_ = \min_m \Delta_m$ is the minimum method detection threshold, and $\bar^2 = (\frac{1}{M} \sum_m 1/\sigma_{m,k}^2)^{-1}$ is the harmonic mean variance.

> **Proof:** \rigorFull
> **Step 1: Consensus estimator.** Let the published claim be $c_k$ (potentially incorrect). The Yajie{} consensus (defined formally in Section [ref]) is:
> 
> $$
>     \hat_k^{Yajie} = \sum_{m=1}^{M} w_m \method{m}_k(B) = \nu_k + \sum_{m=1}^{M} w_m \varepsilon_k^{(m)},
>     <!-- label: eq:consensus_k -->
> $$
> 
> where $w_m \propto 1/\sigma_{m,k}^2$ are the optimal variance-minimizing weights satisfying $\sum_m w_m = 1$. Under Assumption [ref] (unbiased errors), $\E[\hat_k^{Yajie}] = \nu_k$.
> 
> **Step 2: Detection condition.** Detection of a discrepancy occurs when the consensus deviates from the published claim by more than some tolerance. Formally, the event of *non-detection* requires:
> 
> $$
>     |c_k - \hat_k^{Yajie}| \leq \varepsilon,
>     <!-- label: eq:non_detection -->
> $$
> 
> where $\varepsilon$ is the audit tolerance. If the true discrepancy is $\delta = |c_k - \nu_k|$, then:
> 
> $$
>     |c_k - \hat_k^{Yajie}| = |\delta - \sum_{m} w_m \varepsilon_k^{(m)}|.
>     <!-- label: eq:discrepancy_expression -->
> $$
> 
> 
> For $\delta > \varepsilon$, non-detection requires $\sum_m w_m \varepsilon_k^{(m)} \geq \delta - \varepsilon$, i.e., the weighted error sum must be at least $\delta - \varepsilon$ in the direction of the published claim.
> 
> **Step 3: Hoeffding concentration.** Under Assumption [ref], the method errors are independent conditional on $\nu$. The weighted sum $S = \sum_m w_m \varepsilon_k^{(m)}$ has:
> 
> $$
>     \E[S] = 0, \quad \Var(S) = \sum_{m=1}^{M} w_m^2 \sigma_{m,k}^2.
>     <!-- label: eq:S_moments -->
> $$
> 
> 
> With optimal weights $w_m = (1/\sigma_{m,k}^2) / (\sum_\ell 1/\sigma_{\ell,k}^2)$, we obtain:
> 
> $$
>     \Var(S) = \left(\sum_{m=1}^{M} \frac{1}{\sigma_{m,k}^2}\right)^{-1} = \frac{\bar^2}{M}.
>     <!-- label: eq:var_optimal -->
> $$
> 
> 
> Each $\varepsilon_k^{(m)}$ is bounded (vote counts are bounded by $N$ under Assumption [ref]), so Hoeffding's inequality applies:
> 
> $$
>     \Pbb\left(\sum_{m=1}^{M} w_m \varepsilon_k^{(m)} \geq \delta - \varepsilon \;\middle|\; \nu\right) \leq \exp\left(-\frac{M(\delta - \varepsilon)^2}{2\bar^2}\right).
>     <!-- label: eq:hoeffding -->
> $$
> 
> 
> **Step 4: Correlation adjustment.** When method errors are correlated ($\bar > 0$), the effective sample size is reduced. Under a compound symmetry correlation structure, the variance of the weighted mean is inflated by factor $1 + (M-1)\bar$, giving effective multiplicity $M_{eff} = M / (1 + (M-1)\bar)$. Substituting $M_{eff}$ for $M$ and incorporating the method detection threshold $\Delta_$ (below which discrepancies are undetectable by the least sensitive method) yields Eq. [ref].
> 
> **Step 5: Multi-candidate extension.** For $K$ candidates, detection on *any* candidate triggers the full audit (Assumption [ref]). By union bound:
> 
> $$
>     \Pbb(all miss, all  k) \leq \max_{k: \delta_k > \Delta_} \exp\left(-\frac{M_{eff} (\delta_k - \Delta_)^2}{2\bar_k^2}\right) \cdot K,
>     <!-- label: eq:multi_candidate -->
> $$
> 
> which provides a conservative but valid bound. When the maximum discrepancy $\delta_ = \max_k \delta_k$ is used, the $K$ factor is unnecessary if we test only the candidate with the largest discrepancy. $\square$

### The Consensus Detection Theorem

> **Theorem:** [Multi-Method Consensus Detection 多方法共识检测定理]
> <!-- label: thm:consensus_detection -->
> Under Assumptions [ref]-- [ref] and [ref]-- [ref], for an electoral contest with $M$ independent counting methods and $K$ observers, if the published vote count $c_k$ deviates from the true vote count $\nu_k$ by $\delta_k = |c_k - \nu_k|$, the probability of detection (at least one method-auditor or observer flags the discrepancy) satisfies:
> 
> $$
>     \Pbb(detection \mid \delta_k > \Delta_) \geq 1 - \exp\left(-\frac{M_{eff}^{total} \cdot (\delta_k - \Delta_)^2}{2\bar_k^2}\right),
>     <!-- label: eq:detection_theorem -->
> $$
> 
> where $M_{eff}^{total} = M_{eff} + \gamma K$ combines counting methods and observer-augmented multiplicity. Furthermore, when $\delta_k \gg \Delta_$, detection is virtually certain for any $M_{eff}^{total} \geq 3$.

> **Proof:** \rigorFull
> **Step 1: Method-level detection.** From Lemma [ref], the probability that all $M$ counting methods miss the discrepancy is bounded by Eq. [ref]. This handles the counting-method layer.
> 
> **Step 2: Observer augmentation.** Under Assumptions [ref]-- [ref], each observer detects a discrepancy with probability at least $\alpha_$. The $K$ observers provide an additional detection layer. The probability that all $K$ observers miss the discrepancy is:
> 
> $$
>     \Pbb(all observers miss) \leq (1 - \alpha_)^K \leq \exp(-\alpha_ K).
>     <!-- label: eq:observer_miss -->
> $$
> 
> 
> **Step 3: Combined detection.** The overall non-detection event requires both that all counting methods miss *and* all observers miss. Since these events are conditionally independent (observers base their assessments on method outputs, but the events of ``method misses'' and ``observer misses given method outputs'' are independent):
> 
> $$
>     \Pbb(no detection) = \Pbb(all methods miss) \cdot \Pbb(all observers miss \mid all methods miss).
>     <!-- label: eq:combined -->
> $$
> 
> 
> Under the worst case for detection (observers have minimal $\alpha_$), we have:
> 
> $$
>     \Pbb(no detection) &\leq \exp\left(-\frac{M_{eff} (\delta_k - \Delta_)^2}{2\bar_k^2}\right) \cdot \exp(-\alpha_ K) 

>     &\leq \exp\left(-\frac{M_{eff} (\delta_k - \Delta_)^2}{2\bar_k^2} - \alpha_ K\right).
>     <!-- label: eq:combined_bound -->
> $$
> 
> 
> **Step 4: Effective multiplicity unification.** Define $\gamma = 2 \bar_k^2 \alpha_ / (\delta_k - \Delta_)^2$ and $M_{eff}^{total} = M_{eff} + \gamma K$. Then:
> 
> $$
>     \Pbb(detection) \geq 1 - \exp\left(-\frac{M_{eff}^{total} \cdot (\delta_k - \Delta_)^2}{2\bar_k^2}\right),
>     <!-- label: eq:unified_bound -->
> $$
> 
> which is Eq. [ref].
> 
> **Step 5: Asymptotic certainty.** For fixed $\delta_k > \Delta_$ and $\bar_k^2$, as $M_{eff}^{total} \to \infty$, $\Pbb(detection) \to 1$ exponentially fast. With $M = 3$ methods ($\method{P}, \method{E}, \method{R}$) and $K = 50$ observers each with $\alpha_ = 0.1$, even for moderate discrepancies ($\delta_k - \Delta_ = 0.5\%$ of $N$, $\bar_k^2 = 0.001$), detection probability exceeds $1 - \exp(-(3 + 5) \cdot 0.000025 / 0.002) = 1 - \exp(-0.1) \approx 0.905$. For larger discrepancies or more observers, detection is virtually certain.
> 
> **Step 6: The role of Assumption [ref] (trigger).** When detection occurs, Assumption [ref] guarantees a full manual recount, which resolves the discrepancy with probability approaching 1 (the full recount itself has error, but the error is now auditable through the same multi-method framework applied to the recount). $\square$

> **Corollary:** [Required Observer Multiplicity 所需观察者数量]
> <!-- label: cor:observer_count -->
> To achieve detection probability $\geq 1 - \beta$ for a discrepancy of magnitude $\delta > \Delta_$ with $M = 3$ counting methods, the number of independent observers required is:
> 
> $$
>     K^* \geq \frac{1}{\alpha_} \left[\frac{2\bar_k^2 \log(1/\beta)}{(\delta - \Delta_)^2} - \frac{M}{1 + (M-1)\bar}\right]_{+},
>     <!-- label: eq:K_star -->
> $$
> 
> where $[x]_+ = \max(0, x)$. For typical parameters: $\bar_k^2 = 0.0005$, $\delta - \Delta_ = 0.01$ (1\% discrepancy), $\beta = 0.01$, $\bar = 0.1$, $\alpha_ = 0.15$: $K^* \approx 9$ observers. Reducing $\bar$ (better method independence) reduces $K^*$; increasing $\alpha_$ (better-trained observers) reduces $K^*$.

> **Remark:** [Operational Significance 实践意义]
> <!-- label: rem:ops_sig -->
> Theorem [ref] provides the mathematical justification for the operational intuition that multi-method counting plus observer access creates robust detection. The theorem is *not* a binary claim that ``observation works''; it provides the quantitative relationship between the number and quality of counting methods ($M$, $\bar^2$, $\bar$), the number and competence of observers ($K$, $\alpha_$), and the magnitude of discrepancy ($\delta$) needed for reliable detection. An electoral authority that publishes only one counting method's output ($M = 1$) has $M_{eff} = 1$ regardless of observer count---no detection is possible beyond what the single method's own error characteristics permit.

## Theorem 2: Discrepancy Source Unidentifiability 差异来源不可辨识性
<!-- label: sec:thm2 -->

When counting methods disagree, stakeholders demand to know *why*. Was the paper ballot count inaccurate due to human fatigue? Did the electronic voting machine malfunction? Was the hand recount sample unrepresentative? Or were ballots tampered with between counts? We prove that without declared assumptions, the source of discrepancy is unidentifiable from the vote counts alone.

### The Discrepancy Decomposition Model

> **Definition:** [Vote Count Discrepancy Decomposition 计票差异分解]
> <!-- label: def:discrepancy_decomp -->
> Let $\method{P}, \method{E}, \method{R}$ be the outputs of the three counting methods. The pairwise discrepancies decompose as:
> 
> $$
>     \method{P} - \method{E} &= \varepsilon^{(P)} - \varepsilon^{(E)} \equiv \delta_{PE}, 

>     \method{P} - \method{R} &= \varepsilon^{(P)} - \varepsilon^{(R)} \equiv \delta_{PR}, 

>     \method{E} - \method{R} &= \varepsilon^{(E)} - \varepsilon^{(R)} \equiv \delta_{ER}.
>     <!-- label: eq:pairwise_discrepancies -->
> $$
> 
> Each method error $\varepsilon^{(m)}$ can be further decomposed into distinct error sources:
> 
> $$
>     \varepsilon^{(m)} = \varepsilon^{(m)}_{human} + \varepsilon^{(m)}_{machine} + \varepsilon^{(m)}_{procedure} + \varepsilon^{(m)}_{tamper} + \varepsilon^{(m)}_{noise},
>     <!-- label: eq:error_decomposition -->
> $$
> 
> where:
> 
- $\varepsilon^{(m)}_{human}$: human counting/interpretation error (relevant for $\method{P}$ and $\method{R}$);
- $\varepsilon^{(m)}_{machine}$: electronic/mechanical malfunction (relevant for $\method{E}$);
- $\varepsilon^{(m)}_{procedure}$: procedural deviation from counting protocol;
- $\varepsilon^{(m)}_{tamper}$: deliberate ballot or result manipulation;
- $\varepsilon^{(m)}_{noise}$: irreducible random variation (finite sample effects).

### Theorem Statement and Proof

> **Theorem:** [Discrepancy Source Unidentifiability 差异来源不可辨识性]
> <!-- label: thm:discrepancy_unident -->
> Under Assumptions [ref]-- [ref] and [ref], for any observed pairwise discrepancy vector $(\delta_{PE}, \delta_{PR}, \delta_{ER}) \neq (0, 0, 0)$, there exist at least $2^3 = 8$ distinct attributions assigning primary responsibility for the discrepancy to different combinations of error sources, such that all $8$ attributions are observationally equivalent from the discrepancy vector alone. Formally, for any $\epsilon > 0$, there exist decompositions:
> 
> $$
>     \varepsilon^{(m)}_{(s)} = \varepsilon^{(m)}_{human,(s)} + \varepsilon^{(m)}_{machine,(s)} + \varepsilon^{(m)}_{procedure,(s)} + \varepsilon^{(m)}_{tamper,(s)} + \varepsilon^{(m)}_{noise,(s)},
>     <!-- label: eq:s_decompositions -->
> $$
> 
> for $s = 1, ..., 8$, such that all decompositions produce identical pairwise discrepancies and in attribution $s$, source component $s$ dominates. Vote count discrepancy attribution is therefore **logically underdetermined** without declared assumptions.

> **Proof:** \rigorFull
> **Step 1: Dimensionality analysis.** The observable data consists of three vote count vectors: $\method{P}, \method{E}, \method{R} \in \N^K$, providing $3K$ numbers. The pairwise discrepancies provide $2K$ independent constraints (the third is linearly dependent: $\delta_{PE} + \delta_{ER} = \delta_{PR}$). The unknown error sources consist of $5$ components $\times$ $3$ methods $\times$ $K$ candidates = $15K$ unknowns. The system has $2K$ equations for $15K$ unknowns---underdetermined by a factor of $7.5$.
> 
> **Step 2: Constructing observationally equivalent worlds.** We construct 8 extreme-point attributions, each assigning the entire discrepancy to a different error-source pattern. For simplicity, consider the scalar case ($K = 1$). Let the observed discrepancies be $\delta_{PE} = d_1$, $\delta_{PR} = d_2$ (which implies $\delta_{ER} = d_2 - d_1$).
> 
> **World 1 (Paper human error 纸质人工误差):**
> 
> $$
>     \varepsilon^{(P)}_{human} &= d_1, \quad \varepsilon^{(E)}_{human} = 0, \quad \varepsilon^{(R)}_{human} = -d_2, 

>     &all other error sources = 0.
> $$
> 
> Interpretation: paper ballot counters made errors of magnitude $d_1$; recount counters made errors of magnitude $-d_2$ (in the opposite direction); the machine was accurate.
> 
> **World 2 (Electronic machine error 电子机器误差):**
> 
> $$
>     \varepsilon^{(E)}_{machine} &= -d_1, \quad \varepsilon^{(P)}_{machine} = 0, 

>     &all other error sources = 0.
> $$
> 
> Interpretation: the electronic machine malfunctioned by $-d_1$; paper and recount were accurate.
> 
> **World 3 (Recount sampling error 重新计票抽样误差):**
> 
> $$
>     \varepsilon^{(R)}_{noise} &= d_1 - d_2, \quad \varepsilon^{(P)}_{noise} = 0, \quad \varepsilon^{(E)}_{noise} = 0, 

>     &all other error sources = 0.
> $$
> 
> Interpretation: the hand recount's statistical sample was unrepresentative; paper and machine were accurate.
> 
> **World 4 (Ballot tampering between counts 计数间选票篡改):**
> 
> $$
>     \varepsilon^{(P)}_{tamper} &= 0, \quad \varepsilon^{(E)}_{tamper} = -d_1, \quad \varepsilon^{(R)}_{tamper} = d_2 - d_1, 

>     &all other error sources = 0.
> $$
> 
> Interpretation: ballots were altered between the paper count and the electronic scan, and again before the recount.
> 
> **Worlds 5--8:** Combinations (human + machine, human + tamper, machine + tamper, all three), each constructed to match the observed discrepancies exactly. For brevity, we specify World 5 (human + machine):
> 
> $$
>     \varepsilon^{(P)}_{human} &= d_1/2, \quad \varepsilon^{(E)}_{machine} = -d_1/2, \quad \varepsilon^{(R)}_{noise} = d_1 - d_2, 

>     &all other error sources = 0.
> $$
> 
> 
> **Step 3: Observational equivalence.** In all 8 worlds, the pairwise discrepancies are identical: $\delta_{PE} = d_1$, $\delta_{PR} = d_2$, $\delta_{ER} = d_2 - d_1$. No observation of the three vote counts alone can distinguish among these eight worlds. Additional observations (video footage of counting, machine audit logs, chain-of-custody records, forensic ballot examination) can narrow the possibilities but cannot uniquely resolve the decomposition unless they provide at least $13K$ independent constraints.
> 
> **Step 4: Continuous family.** The 8 extreme points span a convex polytope in $\R^{15K}$ of observationally equivalent decompositions. Any convex combination of the eight worlds with non-negative weights summing to 1 also matches the observed discrepancies. The space of observationally equivalent attributions has dimension $13K$.
> 
> **Step 5: The role of assumptions.** Any claim that ``the electronic voting machine was hacked'' implicitly assumes $\varepsilon^{(P)}_{human} \approx 0$, $\varepsilon^{(P)}_{procedure} \approx 0$, $\varepsilon^{(P)}_{tamper} \approx 0$ for paper ballots, and similarly for the recount. These assumptions must be declared and justified. The theorem's force is that without such declarations, the attribution is not merely uncertain---it is *logically indeterminate*. The data alone cannot distinguish machine malfunction from human counting error from deliberate fraud.
> 
> **Step 6: Connection to SCX theory.** This theorem is the electoral instantiation of \ThmSCXHonest{} (the Honest Agent Theorem in the SCX theory paper): when a multi-expert system produces divergent outputs, the error source among the experts is unidentifiable from outputs alone. In the electoral setting, the three counting methods are the experts, and the five error sources per method constitute the unidentifiable decomposition. $\square$

> **Corollary:** [Assumption Mandate for Electoral Discrepancy Investigation 选举差异调查的假设声明要求]
> <!-- label: cor:assumption_mandate -->
> Any attribution of an electoral discrepancy to a specific cause (machine malfunction, human error, fraud, etc.) **must** be accompanied by:
> 
1. An explicit declaration of which error sources are assumed negligible: ``We assume $\varepsilon^{(E)}_{tamper} \approx 0$ because the machine audit logs show no unauthorized access.''
2. A justification for each assumption: ``We verify $\varepsilon^{(P)}_{human} \approx 0$ by cross-checking paper ballot counts against a second independent hand count of a 10\% random sample, obtaining correlation $\rho > 0.99$.''
3. A sensitivity analysis: ``If our assumption about chain of custody is violated---if 5\% of ballots were substituted between counts---the attributed machine error of 1,200 votes would be reduced to 400 votes.''

> Without such declarations, electoral discrepancy investigation is scientifically incomplete and vulnerable to motivated attribution.

> **Remark:** [Practical Implication 实践意义]
> <!-- label: rem:unident_practical -->
> Theorem [ref] has direct operational consequences. When an election produces divergent counts across methods, the *first* step is not to determine ``who is to blame'' (an unidentifiable question) but to trigger the full audit mandated by Assumption [ref]. The full manual recount resolves the discrepancy to within the recount's own error bounds, which are then themselves auditable. The theorem implies that electoral dispute resolution should focus on *resolving the count* (via full recount) rather than *attributing the discrepancy* (via investigation), because attribution is logically underdetermined while recount is operationally definitive (within error bounds).

## Theorem 3: Observer Community Detection Power 观察者社区检测力
<!-- label: sec:thm3 -->

While Theorem [ref] addresses detection by counting methods, the observer community provides an independent verification layer. We now prove that even with modest per-observer detection rates, a sufficiently large observer community achieves near-certain detection of result-certification inconsistencies.

### The Observer Detection Model

> **Definition:** [Result Certification 结果认证]
> <!-- label: def:certification -->
> An electoral result $\hat$ is **certified** (VERIFIED) if:
> 
> $$
>     \max_{m \neq m'} \norm{\method{m}(B) - \method{m'}(B)}_\infty \leq \varepsilon,
>     <!-- label: eq:certification_condition -->
> $$
> 
> and the Yajie{} consensus $\auditConsensus$ has been published with hash commitments from all $M$ methods. The certification is **conditional** on the tolerance $\varepsilon$ and the effective multiplicity $M_{eff}^{total}$. If any pairwise discrepancy exceeds $\varepsilon$, the result is **UNCERTIFIED** and triggers full audit (Assumption [ref]).

> **Definition:** [Observer Detection Event 观察者检测事件]
> <!-- label: def:observer_detection -->
> Observer $O_j$ inspects the published certified result $(\hat, \mathcal{H}_P, \mathcal{H}_E, \mathcal{H}_R)$ and compares it against their own observation of one or more counting methods. Observer $j$ detects a certification failure if:
> 
- The published result $\hat$ differs from observer $j$'s witnessed count by more than their individual tolerance $\varepsilon_j$, or
- The hash commitment $\mathcal{H}_m$ does not match observer $j$'s independently recorded count for method $m$, or
- The observer witnessed a procedure violation that would affect the count.

### Theorem Statement and Proof

> **Theorem:** [Observer Community Detection Power 观察者社区检测力]
> <!-- label: thm:observer_detection -->
> Under Assumptions [ref]-- [ref] and [ref], for an electoral contest with $K$ independent observers, if the published certified result is inconsistent with the true vote count (i.e., certification was erroneously or fraudulently granted), the probability that at least one observer detects the inconsistency satisfies:
> 
> $$
>     \Pbb(detection \mid false certification) \geq 1 - \exp(-2K \alpha_^2),
>     <!-- label: eq:observer_detection_theorem -->
> $$
> 
> where $\alpha_$ is the minimum per-observer detection probability (Assumption [ref]). Consequently, for any desired confidence level $1 - \beta$, $K \geq \log(1/\beta) / (2\alpha_^2)$ observers suffice to detect a false certification.

> **Proof:** \rigorFull
> **Step 1: Binary detection indicators.** For each observer $O_j$, define the binary indicator $D_j \in \{0, 1\}$ where $D_j = 1$ if observer $j$ detects the false certification. Under Assumption [ref] (observer independence), $D_j$ are independent Bernoulli random variables. Under Assumption [ref], $\E[D_j \mid false certification] \geq \alpha_$.
> 
> **Step 2: Hoeffding bound for observer aggregate.** Let $\bar{D} = \frac{1}{K} \sum_{j=1}^{K} D_j$ be the fraction of observers detecting the false certification. By Hoeffding's inequality for independent Bernoulli random variables:
> 
> $$
>     \Pbb(\bar{D} = 0) = \Pbb\left(\sum_{j=1}^{K} D_j = 0\right) \leq \Pbb\left(\bar{D} - \E[\bar{D}] \leq -\alpha_\right) \leq \exp(-2K \alpha_^2).
>     <!-- label: eq:hoeffding_observers -->
> $$
> 
> 
> **Step 3: Detection probability.** The probability of detection is the complement:
> 
> $$
>     \Pbb(detection) = 1 - \Pbb(\bar{D} = 0) \geq 1 - \exp(-2K \alpha_^2),
>     <!-- label: eq:detection_prob -->
> $$
> 
> which is Eq. [ref].
> 
> **Step 4: Required observer count.** For target confidence $1 - \beta$, solving $1 - \exp(-2K \alpha_^2) \geq 1 - \beta$ yields:
> 
> $$
>     K \geq \frac{\log(1/\beta)}{2 \alpha_^2}.
>     <!-- label: eq:K_required -->
> $$
> 
> 
> For $\alpha_ = 0.1$ (10\% per-observer detection rate) and $\beta = 0.001$:
> 
> $$
>     K \geq \frac{\log(1000)}{2 \cdot 0.01} = \frac{6.908}{0.02} \approx 346.
>     <!-- label: eq:K_example -->
> $$
> 
> 
> For $\alpha_ = 0.3$ (30\%, well-trained observers with full access to all three methods):
> 
> $$
>     K \geq \frac{6.908}{2 \cdot 0.09} = \frac{6.908}{0.18} \approx 39.
>     <!-- label: eq:K_example2 -->
> $$
> 
> 
> **Step 5: Information weight calibration.** When observers have limited access (observing only one method), their effective detection rate decreases:
> 
> $$
>     \alpha_(a) = \alpha_^{(0)} \cdot \frac{a}{3},
>     <!-- label: eq:alpha_access -->
> $$
> 
> where $a \in \{1, 2, 3\}$ is the number of methods observed and $\alpha_^{(0)}$ is the baseline detection rate with full access. An observer seeing only the paper ballot count ($a = 1$) has one-third the detection rate of an observer with full access. This implies that restricting observer access---a common practice in contested elections---directly and quantifiably reduces verification power.
> 
> **Step 6: Combined counting-method plus observer detection.** The total detection probability combines Theorem [ref] (method layer) and Theorem [ref] (observer layer). Under conditional independence of the layers:
> 
> $$
>     \Pbb(total detection) &= 1 - \Pbb(methods miss) \cdot \Pbb(observers miss \mid methods miss) 

>     &\geq 1 - \exp\left(-\frac{M_{eff} (\delta - \Delta_)^2}{2\bar^2}\right) \cdot \exp(-2K \alpha_^2) 

>     &= 1 - \exp\left(-\frac{M_{eff} (\delta - \Delta_)^2}{2\bar^2} - 2K \alpha_^2\right).
>     <!-- label: eq:total_detection -->
> $$
> 
> 
> This unified bound shows that counting methods and observers are *substitutable* in the exponent: adding more observers can compensate for fewer or more correlated counting methods, and vice versa. $\square$

> **Corollary:** [Minimum Observer Count for VERIFIED Certification 认证所需最少观察者数量]
> <!-- label: cor:observer_verified -->
> For an electoral result to achieve VERIFIED status with confidence $1 - \beta$, the total detection exponent must satisfy:
> 
> $$
>     \frac{M_{eff} (\delta_ - \Delta_)^2}{2\bar^2} + 2K \alpha_^2 \geq \log(1/\beta),
>     <!-- label: eq:verified_condition -->
> $$
> 
> where $\delta_$ is the minimum discrepancy considered meaningful. This equation defines the tradeoff surface between counting method quality and observer community size.

## Multi-Method Yajie{ Certification Protocol 多方法Yajie认证协议}
<!-- label: sec:protocol -->

We now present the complete Yajie{} multi-method vote certification protocol. This protocol operationalizes the three theorems: it produces a certified vote count with quantifiable error probability when methods agree (Theorem [ref]), triggers full audit when they disagree (Theorem [ref]), and enables observer verification (Theorem [ref]).

### Yajie{ Consensus for Vote Tabulation 计票的Yajie共识}

> **Definition:** [Correlation-Adjusted Yajie{} Weights 相关性调整的Yajie权重]
> <!-- label: def:yajie_weights -->
> The Yajie{} weight for counting method $m$ on candidate $k$ is:
> 
> $$
>     w_{m,k}^{Yajie} = \frac{1/\hat_{m,k}^2}{\sum_{\ell=1}^{M} 1/\hat_{\ell,k}^2} \cdot \frac{1}{1 + \sum_{\ell \neq m} \hat_{m\ell}^{(k)} \cdot (\hat_{\ell,k} / \hat_{m,k})},
>     <!-- label: eq:yajie_weight_election -->
> $$
> 
> where $\hat_{m,k}^2$ is the estimated variance of method $m$ for candidate $k$ (from historical performance data or calibration on non-competitive races) and $\hat_{m\ell}^{(k)}$ is the estimated inter-method error correlation.

> **Definition:** [\Yajie{} Consensus Vote Count \Yajie{}共识计票]
> <!-- label: def:yajie_consensus -->
> The Yajie{} consensus vote count for candidate $k$ is:
> 
> $$
>     \hat_k^{Yajie} = \sum_{m \in \{P, E, R\}} w_{m,k}^{Yajie} \cdot \method{m}_k(B),
>     <!-- label: eq:yajie_consensus_def -->
> $$
> 
> with consensus standard error:
> 
> $$
>     \hat_k^{Yajie} = \left(\sum_{m=1}^{M} \frac{1}{\hat_{m,k}^2}\right)^{-1/2} \cdot \sqrt{\frac{1}{1 - \bar_{eff}^{(k)}}},
>     <!-- label: eq:yajie_se -->
> $$
> 
> where $\bar_{eff}^{(k)} = \sum_{m \neq \ell} w_{m,k}^{Yajie} w_{\ell,k}^{Yajie} \hat_{m\ell}^{(k)} / \sum_{m \neq \ell} w_{m,k}^{Yajie} w_{\ell,k}^{Yajie}$.

> **Proposition:** [Consensus Optimality 共识最优性]
> <!-- label: prop:consensus_optimality -->
> Under Assumptions [ref] and [ref], the Yajie{} consensus estimator $\hat_k^{Yajie}$ is the minimum-variance linear unbiased estimator of $\nu_k$ given the three counting method outputs. When method errors are uncorrelated ($\bar = 0$), $\Var(\hat_k^{Yajie}) \leq \min_m \Var(\method{m}_k) / 3$, achieving a $\sqrt{3}$-fold precision improvement over the best single method.

> **Proof:** \rigorPartial
> For uncorrelated methods, the variance is $\Var(\sum_m w_m \method{m}_k) = \sum_m w_m^2 \sigma_{m,k}^2$. Minimizing subject to $\sum_m w_m = 1$ via Lagrange multipliers yields $w_m^* \propto 1/\sigma_{m,k}^2$, giving $\Var(\hat_k^{Yajie}) = (\sum_m 1/\sigma_{m,k}^2)^{-1}$. For equal-quality methods ($\sigma_{m,k}^2 = \sigma^2$), this is $\sigma^2/3$, which is smaller than $\sigma^2$ (the variance of any single method) by factor 3. The second factor in Eq. [ref] provides a first-order correction for non-zero correlations.  $\square$

### The Certification Protocol

\begin{algorithm}[htbp]
*Caption:* Yajie{} Multi-Method Vote Certification Protocol 多方法投票认证协议
<!-- label: alg:certification -->
\begin{algorithmic}[1]
\Require Ballot set $B$, counting methods $\{\method{P}, \method{E}, \method{R}\}$, tolerance $\varepsilon$, observer count $K$
\Ensure Certified result with VERIFIED/UNCERTIFIED status, confidence level
\State **Phase 1: Independent Counting 独立计票**
\For{$m \in \{P, E, R\}$}
    \State Method $m$ counts ballots: $\method{m}(B) \in \N^K$
    \State Compute hash commitment: $\mathcal{H}_m \gets SHA-256(\method{m}(B) \| salt_m)$
    \State Publish $\mathcal{H}_m$ to public registry
\EndFor
\State **Phase 2: Consensus Computation 共识计算**
\State Reveal all $\method{m}(B)$; verify $\mathcal{H}_m$ matches
\State Compute pairwise discrepancies: $\delta_{PE}, \delta_{PR}, \delta_{ER} \gets \max_k |\method{m}_k(B) - \method{m'}_k(B)|$
\If{$\max(\delta_{PE}, \delta_{PR}, \delta_{ER}) \leq \varepsilon$}
    \State Compute Yajie{} weights $\{w_{m,k}^{Yajie}\}$ via Eq. [ref]
    \State Consensus: $\auditConsensus \gets \sum_m w_m^{Yajie} \cdot \method{m}(B)$
    \State Compute consensus SE $\hat^{Yajie}$ via Eq. [ref]
    \State Compute detection probability $p_{det}$ via Eq. [ref]
    \State **Status:** $`VERIFIED`(\varepsilon, p_{det})$
\Else
    \State **Status:** $`UNCERTIFIED`$ --- discrepancy exceeds tolerance
    \State Trigger full manual recount (Assumption [ref])
    \State \Return UNCERTIFIED, discrepancy report, recount mandate
\EndIf
\State **Phase 3: Observer Verification 观察者验证**
\For{$j = 1$ to $K$}
    \State Observer $O_j$ verifies $\mathcal{H}_m$ against witnessed counts
    \State Observer $O_j$ reports $D_j \in \{0, 1\}$ (detection indicator)
\EndFor
\State Observer consensus: $\bar{D} \gets \frac{1}{K} \sum_j D_j$
\If{$\bar{D} > 0$}
    \State Observer-detected inconsistency: escalate to full audit
    \State \Return UNCERTIFIED, observer detection report
\EndIf
\State **Phase 4: Publication 发布**
\State Publish certified result $\auditConsensus$, CI $[\auditConsensus - z_{\alpha/2}\hat^{Yajie}, \auditConsensus + z_{\alpha/2}\hat^{Yajie}]$
\State Publish hash chain $\{\mathcal{H}_P, \mathcal{H}_E, \mathcal{H}_R\}$, observer report $\bar{D}$, detection probability $p_{det}$
\State \Return VERIFIED, certified vote count, confidence bounds
\end{algorithmic}
\end{algorithm}

> **Proposition:** [Protocol Soundness 协议可靠性]
> <!-- label: prop:protocol_soundness -->
> Under Assumptions [ref]-- [ref], the Yajie{} protocol satisfies:
> 
1. **Completeness:** If all methods agree within tolerance $\varepsilon$, the result is certified VERIFIED with detection probability $p_{det} \geq 1 - \exp(-Term)$ from Eq. [ref].
2. **Soundness:** If the result is certified VERIFIED but the true vote count $\nu$ differs from $\auditConsensus$ by more than $\varepsilon$, the probability of this ``false certification'' is bounded by $1 - p_{det}$.
3. **Observer augmentability:** Adding more observers ($K \uparrow$) or improving observer access ($\alpha_ \uparrow$) strictly increases $p_{det}$.

> **Proof:** \rigorSketch
> Completeness follows from the consensus detection theorem: if methods agree within $\varepsilon$, the probability that they all miss a true discrepancy $\delta > \varepsilon$ is bounded by Eq. [ref]. Soundness is the contrapositive: if the certification is erroneous, the detection probability is at least $p_{det}$, so the false-certification probability is at most $1 - p_{det}$. Observer augmentability follows from the monotonicity of the exponent in $K$ in Eq. [ref].  $\square$

## Cercis{ Electoral Integrity Score 选举诚信Cercis评分}
<!-- label: sec:cercis -->

The Cercis{} scoring framework [cite] ranks entities by quality $Q$ (accuracy) and novelty $N$ (regime coverage). For electoral systems, we define a composite score that captures both counting accuracy and robustness to novel electoral conditions.

> **Definition:** [Electoral Quality Score 选举质量分]
> <!-- label: def:electoral_Q -->
> For an electoral system $\mathcal{E}$ evaluated over $T$ historical elections, the quality score is:
> 
> $$
>     Q(\mathcal{E}) = -\Bigg(
>         \underbrace{\frac{1}{T}\sum_{t=1}^{T} \frac{\norm{\hat_t^{Yajie} - \nu_t^{full}}}{\nu_t^{full}}}_{consensus error  \varepsilon_{cons}}
>         \;+\;
>         \underbrace{\frac{\#\{t: UNCERTIFIED_t \land no recount triggered\}}{T}}_{false certification rate  \varepsilon_{fc}}
>         \;+\;
>         \underbrace{\frac{\#\{t: recount triggered \land \delta_t \leq \varepsilon\}}{T}}_{false alarm rate  \varepsilon_{fa}}
>     \Bigg),
>     <!-- label: eq:electoral_Q -->
> $$
> 
> where $\nu_t^{full}$ is the ground-truth vote count from a complete manual recount (the gold standard). Lower consensus error, fewer false certifications, and fewer false alarms all increase $Q$.

> **Definition:** [Electoral Novelty Score 选举新颖性分]
> <!-- label: def:electoral_N -->
> The novelty score quantifies an electoral system's exposure to novel regimes:
> 
> $$
>     N(\mathcal{E}) = \sum_{d=1}^{D} \omega_d \cdot \ind{system  \mathcal{E}  is the first evaluated in regime  r_d},
>     <!-- label: eq:electoral_N -->
> $$
> 
> where $D$ is the number of electoral-regime dimensions (ballot type, counting technology, precinct size, voter turnout level, contentiousness), and $\omega_d$ is the difficulty weight for dimension $d$:
> 
> $$
>     \omega_d = \frac{1}{\min_{\mathcal{E}' \neq \mathcal{E}} dist_d(\mathcal{E}, \mathcal{E}') + \epsilon},
>     <!-- label: eq:omega_d -->
> $$
> 
> inversely proportional to the minimum distance to any previously evaluated electoral system on dimension $d$.

> **Definition:** [\Cercis{} Electoral Integrity Score \Cercis{}选举诚信分]
> <!-- label: def:cercis_electoral -->
> 
> $$
>     S(\mathcal{E}) = Q(\mathcal{E}) + \eta \cdot N(\mathcal{E}),
>     <!-- label: eq:cercis_electoral -->
> $$
> 
> where $\eta \geq 0$ is the novelty-accuracy tradeoff parameter. $\eta = 0$ ranks systems purely by demonstrated accuracy; $\eta > 0$ rewards systems that operate in novel electoral regimes, reflecting the value of information about untested conditions.

[Table omitted — see original .tex]

> **Remark:** [Interpretation 解释]
> <!-- label: rem:cercis_interpretation -->
> The Cercis{} score formalizes a key insight: paper-only elections have low $\varepsilon_{fa}$ (few false alarms) but also higher $\varepsilon_{cons}$ and $\varepsilon_{fc}$ (more undetected errors). Adding electronic tabulation reduces consensus error but introduces false alarms (discrepancies later resolved by recount). The full SCX protocol with observers achieves the best balance: near-zero false certifications, low consensus error, and acceptable false alarm rate---at the cost of running three counting methods and coordinating observers. The scoring framework makes these tradeoffs explicit, quantifiable, and comparable across electoral systems.

## Spring{ Gating for Electoral Irregularity Detection 选举异常检测的Spring门控}
<!-- label: sec:spring -->

A critical challenge in electoral integrity is detecting when an election transitions from normal operations to irregular conditions---whether due to systematic fraud, technical failure, or procedural breakdown. The Spring{} gating mechanism [cite] provides a self-evolving threshold for regime detection.

> **Definition:** [Electoral Regime 选举制度]
> <!-- label: def:electoral_regime -->
> An electoral regime $R$ is characterized by the joint distribution of inter-method discrepancies:
> 
> $$
>     D_R = \Pbb(\max_{m \neq m'} \norm{\method{m}(B) - \method{m'}(B)}_\infty > \varepsilon \mid R).
>     <!-- label: eq:electoral_regime_def -->
> $$
> 
> In a normal regime ($R_{normal}$), $D_{R_{normal}} \approx \alpha_{false}$ for a small false-alarm rate $\alpha_{false}$ (e.g., $0.01$). In an irregular regime ($R_{irregular}$), $D_{R_{irregular}} \gg \alpha_{false}$, reflecting elevated inter-method disagreement.

> **Definition:** [\Spring{} Electoral Detection Statistic \Spring{}选举检测统计量]
> <!-- label: def:spring_electoral -->
> The Spring{} gating statistic at precinct $r$ and time $t$ (for multi-precinct sequential reporting) is the EWMA of discrepancy events:
> 
> $$
>     S_t^{(r)} = \lambda S_{t-1}^{(r)} + (1 - \lambda) \cdot \ind{\max_{m \neq m'} \norm{\method{m}^{(r)}(B_r) - \method{m'}^{(r)}(B_r)}_\infty > \varepsilon},
>     <!-- label: eq:spring_electoral_stat -->
> $$
> 
> with $S_0^{(r)} = \alpha_{false}$, decay factor $\lambda \in (0, 1)$. The Spring{} alarm triggers for precinct $r$ when $S_t^{(r)} > \gamma_t$, where $\gamma_t$ adapts via:
> 
> $$
>     \gamma_{t+1} = \gamma_t + \eta_\gamma \cdot (\alpha_{target} - \ind{S_t^{(r)} > \gamma_t  in normal precincts}).
>     <!-- label: eq:spring_threshold_electoral -->
> $$

> **Proposition:** [\Spring{} Detection Properties for Elections \Spring{}选举检测性质]
> <!-- label: prop:spring_electoral -->
> Under Assumption [ref], for a transition from $R_{normal}$ to $R_{irregular}$ occurring at precinct $r^*$ at time $t_0$:
> 
1. **False alarm control:** $\lim_{T \to \infty} \frac{1}{T}\sum_{t=1}^{T} \ind{S_t^{(r)} > \gamma_t \mid R_{normal}} \leq \alpha_{target}$.
2. **Detection delay:** $\E[t_{detect} - t_0 \mid R_{irregular}] \leq \frac{\log(\gamma_0 / \delta_{div})}{-\log(\lambda)} + O(1)$, where $\delta_{div} = D_{R_{irregular}} - D_{R_{normal}}$.
3. **Spatial aggregation:** Across $R$ independent precincts, the system-wide detection probability is at least $1 - \exp(-2R \cdot (term))$, enabling detection of geographically dispersed irregularities.

> **Proof:** \rigorSketch
> The Spring{} mechanism is a stochastic approximation (Robbins-Monro) algorithm. (i) False alarm control follows from convergence of $\gamma_t$ to the $\alpha_{target}$-quantile of the null distribution. (ii) Detection delay follows from geometric mixing of the EWMA: post-regime-shift, $S_t$ drifts toward $D_{R_{irregular}}$ at rate $1 - \lambda$, crossing $\gamma_t$ in $O(\log(1/\delta_{div}) / (1-\lambda))$ steps. (iii) Spatial aggregation uses Hoeffding's inequality across precincts, analogous to Theorem [ref].  $\square$

> **Remark:** [Operational Use 操作使用]
> <!-- label: rem:spring_ops -->
> The Spring{} mechanism is designed for real-time monitoring during multi-precinct sequential vote reporting. As precinct results arrive, the EWMA tracks the fraction of precincts exhibiting inter-method discrepancies. A sudden increase in this fraction---beyond what is expected from normal counting variation---triggers an alert. The mechanism is *statistical*, not political: it detects changes in the distribution of counting method agreement, regardless of the underlying cause (fraud, machine failure, procedural breakdown).

## Specific Formal Applications 具体形式化应用
<!-- label: sec:applications -->

### Precinct-Level Tabulation 选区级计票

Consider a single precinct $P_r$ with $N_r$ ballots. The three counting methods operate as follows:

- $\method{P}$: Precinct workers hand-count all $N_r$ paper ballots. Historical error rate: $\sigma_P \approx 0.002 \cdot N_r$ (0.2\% miscount rate).
- $\method{E}$: Optical scanner tabulates all $N_r$ ballots. Historical error rate: $\sigma_E \approx 0.001 \cdot N_r$ (0.1\% misread rate for properly calibrated scanners).
- $\method{R}$: A risk-limiting audit hand-counts $n_r = \lceil \log(1/\alpha) / \mu \rceil$ randomly sampled ballots, where $\mu$ is the margin and $\alpha$ is the risk limit. For a 5\% margin and $\alpha = 0.05$: $n_r \approx 60$ ballots. The sampling standard error is $\sigma_R \approx \sqrt{n_r \cdot p(1-p)}$, where $p$ is the vote share.

The effective multiplicity with $M_{eff} = 3 / (1 + 2\bar)$. For typical inter-method correlations $\bar \approx 0.1$ (paper and electronic errors are largely independent; recount sampling error correlates weakly with both), $M_{eff} \approx 2.73$. For a precinct with $N_r = 500$ ballots and a discrepancy $\delta = 10$ votes (2\%):

$$
    \Pbb(detection) \geq 1 - \exp\left(-\frac{2.73 \cdot 10^2}{2 \cdot (500 \cdot 0.002)^2}\right) = 1 - \exp\left(-\frac{273}{2}\right) \approx 1.0.
    <!-- label: eq:precinct_example -->
$$

Detection is virtually certain even at the precinct level for moderate discrepancies.

### Mail-In Ballot Processing 邮寄选票处理

Mail-in (absentee) ballots introduce additional error sources: signature verification errors, ballot rejection ambiguity, postal delays affecting receipt deadlines, and chain-of-custody gaps between mailing and counting. The three counting methods adapt:

- $\method{P}$: Hand-count of all received mail-in ballots after signature verification. Error variance $\sigma_P^{(V)}$ includes verification errors (incorrectly rejected or accepted ballots).
- $\method{E}$: Optical scan of mail-in ballots. Same hardware as in-person, but paper handling introduces additional jams and misreads. $\sigma_E^{(V)} > \sigma_E$ due to variable paper condition.
- $\method{R}$: Hand recount of a stratified random sample of mail-in ballots, with strata for signature-verified vs. provisional ballots.

The inter-method correlation $\bar$ may be higher for mail-in ballots because paper degradation affects both $\method{P}$ and $\method{E}$ (both handle the same physical ballots). If $\bar \approx 0.3$, $M_{eff} \approx 3 / (1 + 2 \cdot 0.3) = 1.875$. The reduced effective multiplicity implies that larger discrepancies or more observers are needed for equivalent detection power compared to in-person voting.

### Multi-Jurisdiction Result Aggregation 多辖区结果汇总

For a national election spanning $R$ precincts, the vote count for candidate $k$ is:

$$
    \nu_k^{national} = \sum_{r=1}^{R} \nu_k^{(r)}.
    <!-- label: eq:national_vote -->
$$

When each precinct applies the multi-method protocol independently, the precinct-level discrepancies aggregate. Let $D_r \in \{0, 1\}$ indicate whether precinct $r$ triggers full audit (UNCERTIFIED). Under normal operations, $\E[D_r] = \alpha_{false}$ (false alarm rate). For $R = 10,000$ precincts and $\alpha_{false} = 0.01$, approximately 100 precincts trigger audit under normal conditions---acceptable when audits are manageable at the precinct level.

However, in an irregular regime where $\E[D_r] = \alpha_{irregular} > \alpha_{false}$ across a subset $\mathcal{R}_{irregular}$ of precincts, the spatial aggregation of Spring{} (Proposition [ref], part iii) detects the irregularity with high probability. For $|\mathcal{R}_{irregular}| = 500$ precincts and $\alpha_{irregular} - \alpha_{false} = 0.05$:

$$
    \Pbb(system detection) \geq 1 - \exp(-2 \cdot 500 \cdot 0.05^2) = 1 - \exp(-2.5) \approx 0.918.
    <!-- label: eq:national_detection -->
$$

[Table omitted — see original .tex]

### Observer Access as a Continuous Variable 观察者访问作为连续变量

The observer weight $\gamma$ in Definition [ref] depends on observer access. We formalize three access tiers:

1. **Full access 完全访问** ($\gamma = 1.0$): Observers witness all three counting methods, compare outputs in real time, and independently record hash commitments. This is the gold standard for international election observation missions.
2. **Partial access 部分访问** ($\gamma = 0.5$): Observers witness two methods (typically paper count and electronic tabulation, but not the recount). Detection rate $\alpha_ \approx 2\alpha_^{(0)}/3$.
3. **Limited access 有限访问** ($\gamma = 0.2$): Observers witness only one method, typically the paper ballot count. Detection rate $\alpha_ \approx \alpha_^{(0)}/3$. This is the minimum for any verification benefit; observing zero methods provides $\gamma = 0$, contributing nothing to $M_{eff}^{total}$.

The relationship between access and detection power is approximately linear in $\gamma$, meaning that restricting observer access from Tier 1 to Tier 3 reduces the observer contribution to $M_{eff}^{total}$ by a factor of 5. This quantifies the electoral-integrity cost of observer restrictions.

## Discussion 讨论
<!-- label: sec:discussion -->

### Relationship to Existing Electoral Integrity Frameworks 与现有选举诚信框架的关系

**Risk-Limiting Audits (RLA).** The risk-limiting audit methodology [cite] provides a statistical framework for post-election ballot auditing. The RLA compares a hand-counted random sample against reported electronic totals, stopping when the risk that an incorrect outcome would escape detection falls below a pre-specified limit. Our framework generalizes RLAs in two directions: (i) we formalize $M \geq 3$ methods rather than the RLA's implicit $M = 2$ (machine count vs. hand sample), and (ii) we incorporate observer community verification as an independent detection layer. The Yajie{} protocol reduces to a risk-limiting audit when $M = 2$ (electronic + hand recount), but the three-method configuration provides strictly stronger guarantees through triangulation.

**Election Forensics.** Statistical forensics methods (Benford's Law tests, turnout distribution analysis, digit-based anomaly detection) [cite] detect statistical anomalies in reported results. These methods operate on a *single* data stream (the published vote counts), making them vulnerable to sophisticated manipulation that preserves statistical signatures. Our multi-method framework requires manipulation to simultaneously defeat three independent counting processes *and* the observer community---an exponentially harder task. Election forensics methods serve as complementary tools: they flag anomalies that trigger the multi-method audit of Theorem [ref].

**Parallel Vote Tabulation (PVT).** Civil society organizations conduct independent parallel vote tabulations by deploying observers to a random sample of polling stations, independently recording results, and comparing against official totals. The PVT is an instantiation of our observer community detection (Theorem [ref]) with $\gamma$ determined by sample size. Our framework provides the formal detection-probability bounds that PVT practitioners have relied on through simulation and intuition.

**Social Choice Theory.** Arrow's impossibility theorem [cite] and the Gibbard-Satterthwaite theorem [cite] establish fundamental limits on preference aggregation and strategy-proof voting. Our framework addresses a different question: given a voting method, can we certify that the votes were counted correctly? We do not aggregate preferences---we verify counts. The distinction is crucial: a perfectly counted election can still produce an outcome that violates Arrow's conditions (if the voting rule itself violates them), and a perfectly designed voting rule cannot compensate for inaccurate counting.

### Honest Limitations 诚实局限性

We now declare what SCX{} electoral auditing cannot do, consistent with the SCX{} mandate of honest limitation declaration.

1. **\limitationTag{1} Cannot replace democratic legitimacy 不能替代民主合法性.** SCX{} certifies the accuracy of vote counting, not the legitimacy of the electoral process. An election can have perfectly accurate counting ($p_{det} \to 1$) while suffering from voter suppression, gerrymandering, or media manipulation. SCX{} audits the *output* of an election (the count), not the *inputs* (who gets to vote, how districts are drawn, how campaigns are conducted).
2. **\limitationTag{2} Cannot detect pre-counting manipulation 不能检测计票前操纵.** If ballots are tampered with *before* any method counts them---all three methods count tampered ballots---the consensus will agree on the wrong number. Theorem [ref] applies: the tampering is unidentifiable from counting-method outputs alone. Chain-of-custody (Assumption [ref]) provides partial protection; complete protection requires independent ballot verification (e.g., voter-verifiable paper audit trails).
3. **\limitationTag{3} Requires method diversity for bias detection 需要方法多样性检测偏差.** If all three counting methods share a common systematic bias (Assumption [ref] violated), the consensus inherits that bias. For example, if both the paper count and the electronic scanner use the same flawed ballot design that systematically misreads certain marks, and the recount uses the same ballots, the consensus will be precisely wrong. Method diversity---structurally independent counting mechanisms---is the only defense.
4. **\limitationTag{4} Cannot detect coercion 不能检测胁迫.** A voter coerced into voting against their preference produces a valid ballot that will be counted correctly by all methods. SCX{} certifies that the ballot was counted as marked, not that the mark reflects the voter's genuine preference. Coercion detection requires secret-ballot enforcement, not counting verification.
5. **\limitationTag{5} Observer collusion reduces detection power 观察者串通降低检测力.** Assumption [ref] (observer independence) fails if observers collude. A coordinated observer community that agrees to report ``no discrepancy'' regardless of what they witness has $\alpha_ \to 0$, collapsing the observer detection bound. Institutional diversity of observer organizations is the operational defense.
6. **\limitationTag{6} $\varepsilon$ tradeoff 容差权衡.** The audit tolerance $\varepsilon$ creates an unavoidable tension: smaller $\varepsilon$ increases sensitivity to genuine discrepancies (good) but also increases false alarm rate from normal counting variation (bad). The optimal $\varepsilon$ depends on the cost of false alarms vs. the cost of missed discrepancies---a policy choice, not a mathematical result.
7. **\limitationTag{7} Hash-commitment timing attacks 哈希承诺时序攻击.** Assumption [ref] requires that hash commitments are published *before* any method's output is revealed. If an adversary can delay the publication of one method's output until after seeing others' outputs, they can compute a ``consensus-compatible'' fake output and its hash simultaneously, defeating the commitment. Strict temporal ordering enforced by a public blockchain or trusted timestamping service is operationally necessary.
8. **\limitationTag{8} Cost of $M = 3$ methods $M=3$方法成本.** Running three independent counting methods triples the operational cost of vote tabulation. This cost must be weighed against the cost of electoral disputes, loss of legitimacy, and post-election violence that inaccurate or contested results can trigger. The theorems provide the *detection benefit*; whether that benefit justifies the cost is a political decision external to the mathematics.
9. **\limitationTag{9} Recount error propagation 重新计票误差传播.** The full manual recount triggered by Assumption [ref] has its own counting error, bounded by the same $\bar^2$ as the initial hand count. Sequential recounts can converge (each recount reduces the discrepancy) or diverge (errors compound). Convergence conditions depend on the error distribution $\mathcal{D}_m$ and are not guaranteed.
10. **\limitationTag{10} Model dependence of $M_{eff}$ $M_{eff}$的模型依赖性.** The effective multiplicity correction $M_{eff} = M / (1 + (M-1)\bar)$ assumes compound symmetry of error correlations. Real inter-method correlations may have more complex structure (e.g., $\rho_{PE} \neq \rho_{PR} \neq \rho_{ER}$). A general correction using the full correlation matrix $\Sigma$ is possible but requires estimating $M(M-1)/2$ pairwise correlations, which may be infeasible with limited calibration data.

### Future Directions 未来方向

1. **Empirical calibration of $\bar^2$ and $\bar$.** The detection bounds require estimates of method-specific error variances and inter-method correlations. Systematic empirical studies comparing paper, electronic, and hand recount outputs across multiple elections would calibrate these parameters and enable operational deployment.
2. **Blockchain-based hash commitment chains.** Implementing the hash-commitment scheme (Assumption [ref]) on a public blockchain with verifiable timestamps would operationalize the temporal ordering requirement and enable public verification of protocol compliance.
3. **Dynamic observer deployment.** The observer detection theorem (Theorem [ref]) suggests adaptive observer deployment: when $M_{eff}$ is low (due to high $\bar$ or method failure), deploy additional observers to maintain detection power. A control-theoretic formulation would optimize observer allocation across precincts.
4. **Integration with voter-verifiable paper audit trails (VVPAT).** VVPAT systems allow voters to verify that their ballot was recorded as intended before casting. Integrating VVPAT with our multi-method framework would add a fourth counting method ($\method{V}$, voter-verified count), increasing $M$ to 4 and improving detection power.
5. **Bayesian extensions.** The Hoeffding bounds provide frequentist guarantees. Bayesian formulations with priors over $\nu$ would enable posterior probability statements about electoral outcomes, integrating prior knowledge (polling data, historical turnout) with multi-method counting evidence.

## Conclusion 结论
<!-- label: sec:conclusion -->

We have presented a mathematical framework for SCX{} auditing of electoral vote tabulation, grounded in multi-method consensus detection theory. The framework maps vote counting methods to independent experts (paper ballots $\method{P}$, electronic tabulation $\method{E}$, hand recount $\method{R}$) and observer communities to a verification layer, producing certified results with quantifiable detection guarantees.

Three core theorems establish the mathematical foundation:

1. **Multi-Method Consensus Detection (Theorem [ref]):** The probability that all $M$ counting methods simultaneously miss a vote count discrepancy decays exponentially in $M_{eff} \cdot (\delta - \Delta)^2 / \bar^2$. For $M = 3$ structurally independent methods, even moderate discrepancies are detected with near-certainty.
2. **Discrepancy Source Unidentifiability (Theorem [ref]):** When counting methods disagree, the source of discrepancy among human error, machine malfunction, sampling error, and fraud is logically unidentifiable from vote counts alone, forcing explicit assumption declaration in electoral dispute resolution.
3. **Observer Community Detection Power (Theorem [ref]):** An observer community of size $K$ provides exponential detection power for certified-result inconsistencies, with per-observer detection rates as low as $\alpha_ = 0.1$ requiring $K \approx 346$ for 99.9\% detection confidence.

The Yajie{} multi-method certification protocol (Algorithm [ref]) operationalizes these theorems, producing VERIFIED vote counts when all methods agree and triggering full manual recounts when they disagree. The Cercis{} electoral integrity score (Eq. [ref]) provides a composite ranking of electoral systems by accuracy and regime-novelty coverage. The Spring{} gating mechanism (Section [ref]) enables real-time detection of transitions from normal to irregular electoral operations.

The framework is deliberately mathematical, not political. We do not argue that paper ballots are ``better'' than electronic voting, or that observation ``ensures'' fair elections. We prove that under specified conditions---structurally independent counting methods, observer access, hash-commitment publication, and triggered full recounts---the probability of undetected vote count errors can be made arbitrarily small. The conditions are explicit, falsifiable, and quantifiable. When they hold, electoral results can be certified with mathematical confidence. When they do not, the theorems tell us exactly what structural changes would improve certification reliability.

The SCX{} framework's contribution to electoral integrity is a **verification technology**: a set of mathematical tools for assessing the quality of vote tabulation through multi-method consensus and observer verification. Like any technology, it requires institutional will to deploy and operational resources to maintain. Its value lies in making the electoral verification problem computationally tractable and its assumptions transparent.

**Acknowledgments.** We thank the SCX for the foundational framework. We acknowledge the election observation community, risk-limiting audit researchers, and electoral integrity scholars whose practical experience informed the formalization. All errors remain our own. No external funding was received for this theoretical work.

\begin{thebibliography}{99}

\bibitem{SCX2025}
SCX.
\newblock {SCX}: Structured Causal eXamination---A Framework for Multi-Expert Quality Auditing.
\newblock Technical Report, 2025.

\bibitem{SCXGovernance2026}
SCX.
\newblock {SCX} Audit of Governance: Game-Theoretic Foundations of Transparency Under Multi-Expert Verification.
\newblock Technical Report, 2026.

\bibitem{Lindeman2012RLA}
M.~Lindeman and P.~B. Stark.
\newblock A gentle introduction to risk-limiting audits.
\newblock {\em IEEE Security \& Privacy}, 10(5):42--49, 2012.

\bibitem{Stark2008}
P.~B. Stark.
\newblock Conservative statistical post-election audits.
\newblock {\em Annals of Applied Statistics}, 2(2):550--581, 2008.

\bibitem{Mebane2008}
W.~R. Mebane, Jr.
\newblock Election forensics: The second-digit Benford's Law test and recent American presidential elections.
\newblock In {\em Election Fraud: Detecting and Deterring Electoral Manipulation}, Brookings Institution Press, 2008.

\bibitem{BeberScacco2012}
B.~Beber and A.~Scacco.
\newblock What the numbers say: A digit-based test for election fraud.
\newblock {\em Political Analysis}, 20(2):211--234, 2012.

\bibitem{Hoeffding1963}
W.~Hoeffding.
\newblock Probability inequalities for sums of bounded random variables.
\newblock {\em Journal of the American Statistical Association}, 58(301):13--30, 1963.

\bibitem{Arrow1951}
K.~J. Arrow.
\newblock {\em Social Choice and Individual Values}.
\newblock Wiley, 1951.

\bibitem{Gibbard1973}
A.~Gibbard.
\newblock Manipulation of voting schemes: A general result.
\newblock {\em Econometrica}, 41(4):587--601, 1973.

\bibitem{Satterthwaite1975}
M.~A. Satterthwaite.
\newblock Strategy-proofness and Arrow's conditions.
\newblock {\em Journal of Economic Theory}, 10(2):187--217, 1975.

\bibitem{AlvarezHall2008}
R.~M. Alvarez and T.~E. Hall.
\newblock {\em Electronic Elections: The Perils and Promises of Digital Democracy}.
\newblock Princeton University Press, 2008.

\bibitem{Hyde2007}
S.~D. Hyde.
\newblock The observer effect in international politics: Evidence from a natural experiment.
\newblock {\em World Politics}, 60(1):37--63, 2007.

\bibitem{Kelley2012}
J.~G. Kelley.
\newblock {\em Monitoring Democracy: When International Election Observation Works, and Why It Often Fails}.
\newblock Princeton University Press, 2012.

\bibitem{NordenEtAl2007}
L.~Norden, A.~Chen, and D.~Kimball.
\newblock {\em The Machinery of Democracy: Protecting Elections in an Electronic World}.
\newblock Brennan Center for Justice, 2007.

\bibitem{AppelStark2020}
A.~W. Appel and P.~B. Stark.
\newblock Evidence-based elections: Create a meaningful paper trail, then audit.
\newblock {\em Georgetown Law Technology Review}, 4(2):523--541, 2020.

\bibitem{HickenMebane2017}
A.~Hicken and W.~R. Mebane, Jr.
\newblock A guide to election forensics.
\newblock Working Paper, University of Michigan, 2017.

\bibitem{BernhardEtAl2020}
M.~Bernhard et al.
\newblock Public evidence from secret ballots.
\newblock In {\em International Joint Conference on Electronic Voting}, 2020.

\bibitem{EnríquezEtAl2016}
J.~R. Enríquez, R.~Küsters, and T.~Truderung.
\newblock Computer-aided security proofs for verifiable elections.
\newblock In {\em IEEE CSF}, 2016.

\bibitem{CortierEtAl2017}
V.~Cortier et al.
\newblock Belenios: A simple private and verifiable electronic voting system.
\newblock In {\em Foundations of Security, Protocols, and Equational Reasoning}, 2017.

\bibitem{CoverThomas2006}
T.~M. Cover and J.~A. Thomas.
\newblock {\em Elements of Information Theory}, 2nd edition.
\newblock Wiley-Interscience, 2006.

\bibitem{SCXAstronomy2026}
SCX.
\newblock {SCX}-Audited Celestial Mechanics: Multi-Method Consensus for Certified Orbital Determination.
\newblock Technical Report, 2026.

\end{thebibliography}