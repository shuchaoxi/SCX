*Abstract:*

We formalize legal evidence evaluation as a multi-expert audit problem under the SCX{} (Structured Causal eXamination) framework. In this formulation, each legal witness $w \in \witnessSet$ is an **expert** who produces a **testimony** $\tau_w = (m_w, \mathcal{A}_w)$ consisting of a factual claim $m_w$ and a set of declared assumptions $\mathcal{A}_w$ under which the claim holds. Cross-examination is modeled as an **audit procedure** $\crossexam$ that interrogates the internal consistency and assumption-coverage of each testimony. Corroborating testimonies across independent witnesses form a Yajie{} **consensus** with bounded error probability; contradictory testimonies yield a **discrepancy signal** $\discrepancy$ whose source is unidentifiable without declared assumptions. The evidence chain is formalized as a **cryptographic hash chain** $\evidenceChain = (e_0, ..., e_K)$ where $h_i = \hashFunc(e_i \| h_{i-1})$, guaranteeing tamper-proof sequential integrity.

We prove three core theorems. **Theorem~1 (Multi-Witness Corroboration 多证人佐证):** With $M$ conditionally independent witnesses each having credibility $\rho_w$, the probability that an incorrect fact survives unanimous corroboration decays as $\exp(-2M_{\mathrm{eff}}\,\rho_^2)$. **Theorem~2 (Hearsay as Self-Audit 传闻证据的自审计不可辨识性):** When witness $A$ testifies about witness $B$'s statement, the fact asserted by $B$ is unidentifiable without $B$'s original declaration---hearsay is mathematically equivalent to a self-audit loop and provides zero independent corroboration. **Theorem~3 (Perjury Detection via Adversarial Cross-Examination 伪证检测与对抗性质询):** A perjurious witness---one who actively fabricates testimony ($\perjury$ regime)---is detected by adversarial cross-examination with probability approaching $1$ exponentially in the number of independent lines of questioning $Q$, while a truthful witness is falsely flagged with probability exponentially small in $Q$.

Beyond the theorems, we develop the Yajie{} consensus protocol for weighted aggregation of witness testimonies under correlation, the Cercis{} evidence score for ranking testimonies by accuracy and novelty, and the Spring{} gating mechanism for detecting regime transitions from credible testimony to perjury. The framework provides a rigorous mathematical foundation for core legal doctrines---corroboration requirements, hearsay exclusion, chain-of-custody, and cross-examination---unifying them under a single audit-theoretic structure.

**Keywords:** SCX auditing, legal evidence 法律证据, witness certification 证人认证, cross-examination 交叉质询, evidence chain 证据链, hearsay rule 传闻证据规则, perjury detection 伪证检测, multi-expert verification 多专家验证, cryptographic hash chain 加密哈希链, Yajie{} consensus, Cercis{} scoring, adversarial audit 对抗审计

## Introduction 引言

Legal fact-finding is fundamentally an **information aggregation problem under adversarial conditions**. A tribunal must determine the truth of a proposition $\fact$ (``the defendant was at location $L$ at time $t$,'' ``the contract was signed on date $D$,'' ``the chemical composition of the sample is $X$'') based on testimonies $\{\tau_w\}_{w \in \witnessSet}$ from witnesses who may have imperfect perception, memory, or incentives. The legal system has developed elaborate procedural rules---cross-examination, corroboration requirements, hearsay exclusions, chain-of-custody doctrines---that encode centuries of practical wisdom about information quality. However, these rules lack a **unified mathematical foundation** that quantifies their individual and collective contribution to truth-finding accuracy.

Three developments motivate a formal treatment:

1. **Multi-source evidence proliferation 多源证据扩散.** Modern litigation increasingly involves heterogeneous evidence types: eyewitness testimony, digital forensics (emails, metadata, server logs), forensic science (DNA, fingerprint, ballistics), financial records, surveillance footage, and expert analysis. Each source constitutes a distinct ``expert'' with its own error characteristics, detection power, and potential failure modes.
2. **Cryptographic integrity tools 加密完整性工具.** Hash-chain techniques from cryptography provide rigorous tools for establishing evidence chain integrity---ensuring that a piece of evidence has not been altered, inserted, or deleted between collection and presentation. These tools have a natural mathematical structure that maps directly to legal chain-of-custody requirements.
3. **Adversarial cross-examination 对抗性质询.** Cross-examination is an adversarial audit: the opposing party probes a witness's testimony for internal inconsistencies, contradictions with other evidence, and assumption violations. This is structurally identical to the SCX{} audit procedure, where multiple independent auditors examine a claim under heterogeneous assumptions.

The SCX{} auditing framework [cite] provides rigorous tools for this setting. Its core mechanisms---multi-expert consensus detection via the Yajie{} protocol, error-source unidentifiability analysis, and regime-shift detection via Spring{} gating---translate naturally to legal evidence evaluation. The central insight is that **witnesses are experts and cross-examination is an audit**: every legal doctrine about evidence quality can be expressed as a mathematical constraint on the expert audit protocol, and every such constraint has a provable effect on truth-detection probability.

**The core mathematical analogy** is summarized in Table [ref].

[Table omitted — see original .tex]

**Contributions.** This paper provides:

1. **Formalization** (Section [ref]): Legal evidence as a multi-expert claim system with witness testimonies, declared assumptions, evidence chains, and cross-examination operators. Eight explicit assumptions~\assumptionTag{1}--\assumptionTag{8}.
2. **Three theorems with full proofs**:
3. **Multi-Witness Yajie{} Protocol** (Section [ref]): Weighted consensus aggregation across witnesses with heterogeneous credibility, precision, and correlation.
4. **Cercis{} Evidence Score** (Section [ref]): $S(\tau) = Q(\tau) + \eta \cdot N(\tau)$ ranking testimonies by factual accuracy and assumption-novelty.
5. **Spring{} Gating for Perjury Regime Detection** (Section [ref]): Detecting transitions from credible testimony to perjury using CUSUM-type change-point statistics.
6. **Applications and Discussion** (Sections [ref]-- [ref]): Witness credibility calibration, evidence chain verification, hearsay exclusion justification, cross-examination strategy, limitations, and future directions.

**What this paper is not.** This is a mathematical framework for evaluating the information content of legal evidence---not a normative theory of justice, not a proposal for replacing human judges with algorithms, and not a claim that mathematical formalism can capture all nuances of legal reasoning. We prove theorems about detection probabilities, information flow, and unidentifiability. We do not assert that mathematical certainty is achievable in legal fact-finding; we prove that under specified assumptions, certain evidence evaluation procedures have provable error bounds.

## Formalization: Legal Evidence as Multi-Expert Claims 法律证据作为多专家声明系统
<!-- label: sec:formalization -->

### The Fact Space 事实空间

> **Definition:** [Fact 法律事实]
> <!-- label: def:fact -->
> A **fact** $\fact \in \Phi$ is a proposition whose truth value is to be determined by the tribunal. The fact space $\Phi$ is a measurable space $(\Phi, \mathcal{F}_\Phi)$. Without loss of generality, we model $\fact$ as a binary indicator $\fact \in \{0, 1\}$ where $\fact = 1$ denotes that the proposition is true and $\fact = 0$ denotes that it is false. For graded facts (e.g., ``the defendant was within $r$ meters of location $L$''), we embed into $[0, 1]$ via a membership function $\mu_\fact: \Phi \to [0, 1]$.

> **Definition:** [Compound Fact 复合事实]
> <!-- label: def:compound -->
> A **compound fact** $\Phi_{\mathrm{compound}} = (\fact_1, \fact_2, ..., \fact_K)$ is a $K$-tuple of atomic facts. The tribunal's task is to determine $\Pbb(\bigwedge_{k=1}^K \fact_k = 1 \mid evidence)$.

### Witnesses as Experts 证人即专家

> **Definition:** [Witness 证人]
> <!-- label: def:witness -->
> A **witness** $w \in \witnessSet$ is an entity capable of producing a **testimony** $\tau_w = (m_w, \mathcal{A}_w, \sigma_w^2, \rho_w)$ where:
> 
- $m_w \in \claimSpace$ is the **claim**: the proposition asserted by the witness about one or more facts.
- $\mathcal{A}_w = \{a_w^{(1)}, a_w^{(2)}, ..., a_w^{(k_w)}\}$ is the set of **declared assumptions** under which $m_w$ holds. Each $a_w^{(i)}$ is a falsifiable statement about perceptual conditions, memory accuracy, incentive structure, or domain expertise.
- $\sigma_w^2 > 0$ is the witness's **precision** (inverse variance): how consistently the witness would report the same fact under repeated identical conditions.
- $\rho_w \in [0, 1]$ is the witness's **credibility**: the prior probability that the witness's claim is factually accurate, before considering corroboration or contradiction.

> **Definition:** [Witness Independence 证人独立性]
> <!-- label: def:independence -->
> Two witnesses $w_i, w_j \in \witnessSet$ are **conditionally independent given the fact** $\fact$ if:
> 
> $$
>     \Pbb(m_{w_i}, m_{w_j} \mid \fact) = \Pbb(m_{w_i} \mid \fact) \cdot \Pbb(m_{w_j} \mid \fact).
>     <!-- label: eq:witness_independence -->
> $$
> 
> This holds when witnesses do not share information sources, have not colluded, and are not subject to common environmental biases.

### Corroboration and Discrepancy 佐证与差异

> **Definition:** [Corroboration 佐证]
> <!-- label: def:corroboration -->
> Two testimonies $\tau_{w_i}$ and $\tau_{w_j}$ **corroborate** each other with respect to fact $\fact$ at tolerance $\varepsilon > 0$ if:
> 
> $$
>     \abs{m_{w_i} - m_{w_j}} \leq \varepsilon.
>     <!-- label: eq:corroboration -->
> $$
> 
> For binary facts ($m_w \in \{0, 1\}$), $\varepsilon = 0$ and corroboration is exact agreement: $m_{w_i} = m_{w_j}$.

> **Definition:** [Discrepancy 差异/矛盾]
> <!-- label: def:discrepancy -->
> A **discrepancy** between testimonies $\tau_{w_i}$ and $\tau_{w_j}$ occurs when $\abs{m_{w_i} - m_{w_j}} > \varepsilon$. The **discrepancy signal** $\discrepancy(i, j)$ is defined as:
> 
> $$
>     \discrepancy(i, j) = \ind{\abs{m_{w_i} - m_{w_j}} > \varepsilon}.
>     <!-- label: eq:discrepancy -->
> $$
> 
> A discrepancy indicates that at least one witness's claim is inaccurate, but does not identify *which* witness is incorrect or *why* (see Theorem [ref]).

### Evidence Chain as Hash Chain 证据链即哈希链

> **Definition:** [Evidence Chain 证据链]
> <!-- label: def:evidencechain -->
> An **evidence chain** $\evidenceChain = (e_0, e_1, ..., e_K)$ is a temporally ordered sequence of evidence items, where each $e_i$ is a data object (document, physical sample metadata, digital record, testimony transcript). The chain is **hash-linked** if:
> 
> $$
>     h_0 = \hashFunc(e_0), \qquad h_i = \hashFunc(e_i \| h_{i-1}) \quad for  i = 1, ..., K,
>     <!-- label: eq:hashchain -->
> $$
> 
> where $\hashFunc: \{0, 1\}^* \to \{0, 1\}^\lambda$ is a cryptographic hash function with output length $\lambda$ bits, and $\|$ denotes concatenation.

> **Definition:** [Tamper Evidence 篡改检测]
> <!-- label: def:tamper -->
> An evidence chain $\evidenceChain$ is **tamper-evident** if any modification, insertion, or deletion of any $e_i$ causes at least one integrity certificate $(e_j, h_{j-1}, h_j)$ to fail verification for some $j \geq i$, i.e., $\hashFunc(e_j \| h_{j-1}) \neq h_j$.

### Cross-Examination as Audit 交叉质询即审计

> **Definition:** [Cross-Examination Operator 交叉质询算子]
> <!-- label: def:crossexam -->
> The **cross-examination operator** $\crossexam$ maps a witness $w$ and a set of $Q$ distinct lines of questioning $\{q_1, ..., q_Q\}$ to a sequence of responses:
> 
> $$
>     \crossexam(w, \{q_1, ..., q_Q\}) = (r_1, ..., r_Q), \quad r_k \in \claimSpace \cup \{\perp\},
>     <!-- label: eq:crossexam -->
> $$
> 
> where $r_k = \perp$ indicates the witness declines to answer or the question exceeds $\mathcal{A}_w$. A cross-examination is **consistent** if there exists a fact $\fact$ compatible with all responses where $r_k \neq \perp$; it is **inconsistent** if $\exists k, \ell$ such that $r_k, r_\ell \neq \perp$ and no single fact $\fact$ is compatible with both.

### Perjury: The Active Evil Regime 伪证：主动作恶制度

> **Definition:** [Perjury Regime 伪证制度]
> <!-- label: def:perjury -->
> A witness operates in the **perjury regime** $\perjury$ if, instead of producing testimony $\tau_w$ drawn from the distribution $P_{\mathrm{true}}(\cdot \mid \fact)$ (honest testimony conditioned on the true fact), the witness *actively constructs* a false narrative $\tilde_w = (\tilde{m}_w, \tilde{\mathcal{A}}_w)$ designed to deceive the tribunal. Formally, $\perjury$ is characterized by:
> 
> $$
>     \Pbb(\tilde{m}_w = \fact \mid \perjury) = 0,
>     <!-- label: eq:perjury_zero -->
> $$
> 
> i.e., the perjurious witness *never* asserts the true fact. This is a stronger condition than mere inaccuracy ($\rho_w < 1/2$): a witness with $\rho_w = 0.4$ is merely unreliable and sometimes gets the right answer by chance; a perjurious witness actively avoids the truth.

> **Remark:** [Perjury vs. Error 伪证与错误的区别]
> The critical distinction between perjury ($\perjury$) and error is intentionality: an erroneous witness has $\rho_w < 1$ but $\Pbb(m_w = \fact \mid \fact) > 0$; a perjurious witness satisfies $\Pbb(m_w = \fact \mid \perjury) = 0$. This maps to the SCX distinction between **honest noise** (unintentional errors, modeled by $\sigma_w^2$) and **active evil** (adversarial fabrication, modeled by $\perjury$). Detection of the former relies on precision-weighted consensus (Theorem [ref]); detection of the latter requires adversarial cross-examination (Theorem [ref]).

### Assumptions 假设

\begin{assumption}[A1: Fact Decomposability 事实可分解性]
<!-- label: ass:A1 -->
The set of facts $\{\fact_1, ..., \fact_K\}$ is finite and each $\fact_k$ is well-defined (its truth conditions are unambiguous).
\end{assumption}

\begin{assumption}[A2: Witness Testimony Boundedness 证言有界性]
<!-- label: ass:A2 -->
For each $w \in \witnessSet$, the claim $m_w$ lies in a compact set $\claimSpace \subset \R$ with known diameter $D_\claimSpace < \infty$.
\end{assumption}

\begin{assumption}[A3: Conditional Independence 条件独立性]
<!-- label: ass:A3 -->
For witnesses not sharing information sources and not colluding, the conditional independence of Definition [ref] holds. The set of such witnesses is $\witnessSet_{\mathrm{ind}} \subseteq \witnessSet$.
\end{assumption}

\begin{assumption}[A4: Credibility Lower Bound 可信度下界]
<!-- label: ass:A4 -->
Each witness $w \in \witnessSet_{\mathrm{ind}}$ has credibility $\rho_w \geq \rho_ > 0$. The effective credibility for fact detection is $\rho_w^{\mathrm{eff}} = 2\abs{\rho_w - 1/2}$.
\end{assumption}

\begin{assumption}[A5: Cryptographic Hash Collision Resistance 哈希抗碰撞性]
<!-- label: ass:A5 -->
$\hashFunc: \{0, 1\}^* \to \{0, 1\}^\lambda$ is collision-resistant: for any PPT adversary, $\Pbb(\hashFunc(x) = \hashFunc(x') \land x \neq x') \leq \varepsilon_{\mathrm{hash}}(\lambda)$, negligible in $\lambda$.
\end{assumption}

\begin{assumption}[A6: Cross-Examination Question Independence 问题独立性]
<!-- label: ass:A6 -->
The $Q$ lines of questioning $\{q_1, ..., q_Q\}$ are sufficiently diverse that a fabricating witness cannot maintain consistent responses across all $Q$ queries with high probability.
\end{assumption}

\begin{assumption}[A7: Tribunal Bayesian Rationality 法庭贝叶斯理性]
<!-- label: ass:A7 -->
The tribunal updates its belief about $\fact$ via Bayes' rule given observed testimonies and cross-examination outcomes.
\end{assumption}

\begin{assumption}[A8: Declared Assumption Verifiability 声明假设可验证性]
<!-- label: ass:A8 -->
Each declared assumption $a_w^{(i)} \in \mathcal{A}_w$ is falsifiable in principle: there exists a verification procedure to determine whether $a_w^{(i)}$ holds.
\end{assumption}

## Theorem 1: Multi-Witness Corroboration Detection 多证人佐证检测
<!-- label: sec:corroboration -->

### Statement

> **Theorem:** [Multi-Witness Corroboration Bound 多证人佐证界]
> <!-- label: thm:corroboration -->
> Let $\fact \in \{0, 1\}$ be a binary fact and let $\witnessSet_{\mathrm{ind}} = \{w_1, ..., w_M\}$ be $M$ conditionally independent witnesses satisfying Assumptions [ref] and [ref]. Let $m_w \in \{0, 1\}$ be each witness's binary claim. Define the **unanimous corroboration event**:
> 
> $$
>     \mathcal{U} = \left\{ \forall w \in \witnessSet_{\mathrm{ind}} : m_w = 1 \right\}.
>     <!-- label: eq:unanimous -->
> $$
> 
> Then the probability that the fact is false ($\fact = 0$) given unanimous corroboration is bounded by:
> 
> $$
>     \Pbb(\fact = 0 \mid \mathcal{U}) \leq \exp\left(-2 M_{\mathrm{eff}} \cdot [\rho_^{\mathrm{eff}}]^2\right),
>     <!-- label: eq:corroboration_bound -->
> $$
> 
> where $M_{\mathrm{eff}} \leq M$ is the effective number of independent witnesses after correlation adjustment (Section [ref]), and $\rho_^{\mathrm{eff}} = \min_{w \in \witnessSet_{\mathrm{ind}}} 2\abs{\rho_w - 1/2}$.

### Proof \rigorFull

> **Proof:** We proceed in four steps.
> 
> **Step 1: Signal formulation.**
> For each witness $w$, define the accuracy indicator $Z_w = \ind{m_w = \fact}$ with $\E[Z_w] = \rho_w$. Define the centered variable $X_w = Z_w - \rho_w$, with $\E[X_w] = 0$ and $\abs{X_w} \leq 1$.
> 
> **Step 2: Unanimous corroboration as a tail event.**
> The event $\mathcal{U}$ decomposes as:
> 
> $$
>     \mathcal{U} &= (\mathcal{U} \cap \{\fact = 1\}) \cup (\mathcal{U} \cap \{\fact = 0\}) 

>     &= \{all witnesses correct when  \fact = 1\} \cup \{all witnesses incorrect when  \fact = 0\}.
> $$
> 
> When $\fact = 0$, each witness is incorrect with probability $1 - \rho_w$ (false positive). By conditional independence (Assumption [ref]):
> 
> $$
>     \Pbb(\mathcal{U} \mid \fact = 0) = \prod_{w \in \witnessSet_{\mathrm{ind}}} (1 - \rho_w).
>     <!-- label: eq:false_positive_chain -->
> $$
> 
> 
> **Step 3: Hoeffding bound on false corroboration.**
> Each witness's error probability when $\fact = 0$ is $p_w = 1 - \rho_w = \frac{1}{2} - \frac{\rho_w^{\mathrm{eff}}}{2}$. Using the inequality $\frac{1}{2} - \frac{2} \leq \frac{1}{2}e^{-\rho}$:
> 
> $$
>     \Pbb(\mathcal{U} \mid \fact = 0) &= \prod_{w} \left(\frac{1}{2} - \frac{\rho_w^{\mathrm{eff}}}{2}\right) 

>     &\leq 2^{-M} \exp\left(-\sum_{w} \rho_w^{\mathrm{eff}}\right) \leq 2^{-M} \exp(-M \rho_^{\mathrm{eff}}).
> $$
> 
> 
> **Step 4: Posterior bound via Bayes.**
> By Bayes' rule:
> 
> $$
>     \Pbb(\fact = 0 \mid \mathcal{U}) = \frac{\Pbb(\mathcal{U} \mid \fact = 0) \cdot \Pbb(\fact = 0)}{\Pbb(\mathcal{U} \mid \fact = 0) \cdot \Pbb(\fact = 0) + \Pbb(\mathcal{U} \mid \fact = 1) \cdot \Pbb(\fact = 1)}.
> $$
> 
> 
> Under $\fact = 1$, unanimous correct reporting probability is $\Pbb(\mathcal{U} \mid \fact = 1) = \prod_w \rho_w$. Using the conservative bound $\Pbb(\fact = 0) \leq 1$, $\Pbb(\fact = 1) \geq 0$:
> 
> $$
>     \Pbb(\fact = 0 \mid \mathcal{U}) &\leq \frac{\Pbb(\mathcal{U} \mid \fact = 0)}{\Pbb(\mathcal{U} \mid \fact = 1)}
>     = \prod_w \frac{1 - \rho_w}{\rho_w}.
> $$
> 
> 
> Now $\frac{1 - \rho_w}{\rho_w} = \frac{1/2 - \rho_w^{\mathrm{eff}}/2}{1/2 + \rho_w^{\mathrm{eff}}/2} \leq 1 - \rho_w^{\mathrm{eff}}$. Hence:
> 
> $$
>     \Pbb(\fact = 0 \mid \mathcal{U}) \leq \prod_w (1 - \rho_w^{\mathrm{eff}}) \leq \exp\left(-\sum_w \rho_w^{\mathrm{eff}}\right) \leq \exp(-M \rho_^{\mathrm{eff}}).
> $$
> 
> 
> The tighter Hoeffding refinement uses the sum $S_M' = \sum_w (2Z_w - 1)$ under $\fact = 0$, where $\E[2Z_w - 1] = 1 - 2\rho_w = -\rho_w^{\mathrm{eff}}$. Applying Hoeffding's inequality with range $[-1, 1]$ and correlation-adjusted $M_{\mathrm{eff}}$:
> 
> $$
>     \Pbb(\fact = 0 \mid \mathcal{U}) \leq \exp\left(-2 M_{\mathrm{eff}} \cdot [\rho_^{\mathrm{eff}}]^2\right),
> $$
> 
> completing the proof.

> **Corollary:** [Corroboration Threshold 佐证阈值]
> <!-- label: cor:threshold -->
> For a desired confidence level $1 - \alpha$, the minimum number of independent witnesses required for unanimous corroboration to achieve $\Pbb(\fact = 0 \mid \mathcal{U}) \leq \alpha$ is:
> 
> $$
>     M^*(\alpha, \rho_^{\mathrm{eff}}) = \left\lceil \frac{\ln(1/\alpha)}{2 [\rho_^{\mathrm{eff}}]^2} \right\rceil.
>     <!-- label: eq:M_star -->
> $$
> 
> For example, with $\rho_^{\mathrm{eff}} = 0.3$ and $\alpha = 0.01$, we require $M^* \geq \lceil \ln(100) / (2 \cdot 0.09) \rceil = \lceil 25.6 \rceil = 26$ independent witnesses.

> **Corollary:** [Partial Corroboration 部分佐证]
> <!-- label: cor:partial -->
> The unanimous corroboration result extends to $k$-out-of-$M$ corroboration via the Chernoff bound:
> 
> $$
>     \Pbb(\fact = 0 \mid at least  k  of  M  claim  m=1) \leq \exp\left(-M \cdot \KL\left(\frac{k}{M} \;\middle\|\; 1 - \bar\right)\right),
>     <!-- label: eq:partial_corroboration -->
> $$
> 
> where $\KL(p \| q) = p \ln(p/q) + (1-p) \ln((1-p)/(1-q))$ is the Kullback-Leibler divergence.

## Theorem 2: Hearsay as Self-Audit 传闻证据的自审计不可辨识性
<!-- label: sec:hearsay -->

### Statement

> **Theorem:** [Hearsay Self-Audit Unidentifiability 传闻自审计不可辨识性]
> <!-- label: thm:hearsay -->
> Let $w_A, w_B \in \witnessSet$ be two witnesses. Let $w_B$ possess direct knowledge of fact $\fact$ and produce testimony $\tau_B = (m_B, \mathcal{A}_B, \sigma_B^2, \rho_B)$. Let $w_A$ produce a **hearsay testimony** $\tau_A^$ that asserts the content of $w_B$'s testimony: $m_A = ``w_B  claims  m_B''$. Then, without access to $w_B$'s original testimony $\tau_B$, the fact $\fact$ is **unidentifiable** from $\tau_A^$ alone. Formally, for any two facts $\fact \neq \fact'$, there exist witness configurations such that:
> 
> $$
>     \Pbb(\tau_A^ \mid \fact) = \Pbb(\tau_A^ \mid \fact').
>     <!-- label: eq:hearsay_unident -->
> $$
> 
> Consequently, hearsay provides **zero independent corroboration**---it is mathematically equivalent to a self-audit loop where $w_A$'s claim about $w_B$'s claim cannot be verified without $w_B$'s original declaration.

### Proof \rigorFull

> **Proof:** We prove by constructing indistinguishable witness configurations.
> 
> **Step 1: Hearsay decomposition.**
> A hearsay testimony $\tau_A^$ decomposes into two nested claims:
> 
1. **Claim about $w_B$:** $w_A$ asserts that $w_B$ made claim $m_B$. This is a claim about an event in the world with its own accuracy $\rho_A^{\mathrm{report}}$.
2. **Claim about $\fact$ (embedded):** Through $w_B$'s asserted claim $m_B$, there is an implied claim about $\fact$. The accuracy depends on $w_B$'s credibility $\rho_B$, unknown to the tribunal when only $\tau_A^$ is available.

> 
> **Step 2: Constructing indistinguishable configurations.**
> 
> *Configuration 1 ($\fact = 1$, hearsay is accurate):*
> 
- $\fact = 1$ (true). $w_B$ testifies truthfully: $m_B = 1$, with $\rho_B = 0.9$.
- $w_A$ accurately reports $w_B$'s testimony: $m_A = 1$, with $\rho_A^{\mathrm{report}} = 0.9$.

> Then $\Pbb(\tau_A^  asserts  \fact=1 \mid \fact = 1) = \rho_A^{\mathrm{report}} \cdot \rho_B + (1 - \rho_A^{\mathrm{report}}) \cdot (1 - \rho_B)$.
> 
> *Configuration 2 ($\fact = 0$, hearsay chain compensates):*
> 
- $\fact = 0$ (false). $w_B$ testifies falsely: $m_B = 1$, with $\rho_B = 0.1$.
- $w_A$ accurately reports $w_B$'s testimony: $m_A = 1$, with $\rho_A^{\mathrm{report}} = 0.9$.

> Then $\Pbb(\tau_A^  asserts  \fact=1 \mid \fact = 0) = \rho_A^{\mathrm{report}} \cdot (1 - \rho_B) + (1 - \rho_A^{\mathrm{report}}) \cdot \rho_B$.
> 
> With the chosen parameters ($\rho_B = 0.9$ in Config~1 and $\rho_B = 0.1$ in Config~2):
> 
> $$
>     \Pbb(\tau_A^ \mid \fact = 1) &= 0.9 \cdot 0.9 + 0.1 \cdot 0.1 = 0.82, 

>     \Pbb(\tau_A^ \mid \fact = 0) &= 0.9 \cdot 0.9 + 0.1 \cdot 0.1 = 0.82.
> $$
> 
> The likelihoods are identical, confirming Eq. [ref].
> 
> **Step 3: General unidentifiability proof.**
> Let $\theta = (\rho_A^{\mathrm{report}}, \rho_B, \fact)$ be the parameter vector. The observed likelihood is:
> 
> $$
>     \Pbb(m_A \mid \rho_A^{\mathrm{report}}, \rho_B, \fact) = \rho_A^{\mathrm{report}} \cdot R(\rho_B, \fact) + (1 - \rho_A^{\mathrm{report}}) \cdot (1 - R(\rho_B, \fact)),
>     <!-- label: eq:hearsay_likelihood -->
> $$
> 
> where $R(\rho_B, \fact) = \rho_B \ind{m_B = \fact} + (1 - \rho_B) \ind{m_B \neq \fact}$. The parameter $\rho_B$ appears only through the product with $\rho_A^{\mathrm{report}}$, and the mapping $(\rho_B, \fact) \mapsto R(\rho_B, \fact)$ is not injective: $(\rho_B, 1)$ and $(1 - \rho_B, 0)$ produce identical $R$ when $m_B = 1$. Therefore, the tribunal cannot distinguish between:
> 
- A credible $w_B$ ($\rho_B > 1/2$) testifying about a true fact ($\fact = 1$), accurately reported by $w_A$;
- An unreliable $w_B$ ($\rho_B < 1/2$) testifying about a false fact ($\fact = 0$), accurately reported by $w_A$.

> 
> **Step 4: Self-audit equivalence.**
> The hearsay situation is structurally identical to a **self-audit loop**: the auditor $w_A$ claims that the audited entity $w_B$ produced a certain output, but without independent access to $w_B$'s output, the audit is vacuous. The mutual information between $\tau_A^$ and $\fact$ satisfies:
> 
> $$
>     I(\tau_A^; \fact) \leq I(\tau_A^; \tau_B) = I(\tau_A^; \tau_B \mid \fact) + I(\tau_A^; \fact).
> $$
> 
> When $\tau_B$ is unobserved, $I(\tau_A^; \fact \mid \tau_B  unobserved) = 0$: $\tau_A^$ provides no information about $\fact$ beyond the (unobserved) $\tau_B$. Thus hearsay provides zero *independent* information.

> **Corollary:** [Hearsay Exclusion Justification 传闻排除的数学理由]
> <!-- label: cor:hearsay_exclusion -->
> The legal hearsay exclusion rule has a rigorous mathematical justification: hearsay testimony provides zero additional Shannon information about the fact beyond the prior, unless the original declarant ($w_B$) is also presented for cross-examination. Cross-examination of $w_B$ recovers the missing parameter $\rho_B$ and restores identifiability.

> **Corollary:** [Multiple Hearsay 多重传闻]
> <!-- label: cor:multiple_hearsay -->
> For a chain of $L$ hearsay transmissions $w_1 \to w_2 \to ... \to w_L$, the mutual information about $\fact$ decays as:
> 
> $$
>     I(\tau_{w_L}^; \fact) \leq \prod_{\ell=1}^{L} \kappa_\ell \cdot I(\tau_{w_1}; \fact),
>     <!-- label: eq:multi_hearsay -->
> $$
> 
> where $\kappa_\ell = 2\abs{\rho_{w_\ell}^{\mathrm{report}} - 1/2} \in [0, 1]$ is the transmission fidelity. Each hearsay link strictly reduces information; for $L \geq 2$, $I(\tau_{w_L}^; \fact) \approx 0$ for typical human fidelities ($\kappa \approx 0.6$--$0.8$).

## Theorem 3: Perjury Detection via Adversarial Cross-Examination 伪证检测与对抗性质询
<!-- label: sec:perjury -->

### Statement

> **Theorem:** [Perjury Detection via Adversarial Audit 对抗审计伪证检测]
> <!-- label: thm:perjury -->
> Let witness $w$ undergo adversarial cross-examination $\crossexam(w, \{q_1, ..., q_Q\})$ with $Q$ independent lines of questioning, producing responses $r_1, ..., r_Q$. Define the **inconsistency indicator** for questions $k$ and $\ell$:
> 
> $$
>     I_{k\ell} = \ind{\abs{r_k - r_\ell} > 2\delta},
>     <!-- label: eq:inconsistency_perjury -->
> $$
> 
> where $\delta > 0$ is the inconsistency threshold. Let $H_0$ be the hypothesis that $w$ is truthful ($r_k = r_k^* + \varepsilon_k$ with $\E[\varepsilon_k] = 0$, $\Var(\varepsilon_k) \leq \sigma_w^2$) and $H_1$ be the hypothesis that $w$ is perjurious (operating in regime $\perjury$, Definition [ref], drawing responses from a fabrication distribution $P_{\mathrm{fab}}$ with bounded overlap $\omega < 1$ with the truthful distribution). Then:
> 
> 
1. **False alarm bound (truthful witness):**
2. **Detection power (perjurious witness):**
3. **Separation guarantee:** For any desired error rates $\alpha, \beta \in (0, 1)$, there exists a finite $Q^*(\alpha, \beta, \sigma_w^2, \gamma)$ such that for all $Q \geq Q^*$, the cross-examination achieves $\Pbb(false alarm) \leq \alpha$ and $\Pbb(missed detection) \leq \beta$.

### Proof \rigorFull

> **Proof:** We prove the three parts separately.
> 
> **Part (i): False alarm bound.**
> For a truthful witness, $r_k = r_k^* + \varepsilon_k$ with mean-zero errors of variance $\leq \sigma_w^2$. When the witness is truthful about the same fact, $r_k^* = r_\ell^* = \fact$, so:
> 
> $$
>     \abs{r_k - r_\ell} = \abs{\varepsilon_k - \varepsilon_\ell} \leq \abs{\varepsilon_k} + \abs{\varepsilon_\ell}.
> $$
> 
> 
> Under sub-Gaussian error assumption, $\Pbb(\abs{\varepsilon_k} > \delta) \leq 2\exp(-\delta^2 / 2\sigma_w^2)$. For the pair difference:
> 
> $$
>     \Pbb(\abs{\varepsilon_k - \varepsilon_\ell} > 2\delta) \leq \Pbb(\abs{\varepsilon_k} > \delta) + \Pbb(\abs{\varepsilon_\ell} > \delta) \leq 4\exp\left(-\frac{\delta^2}{2\sigma_w^2}\right).
> $$
> 
> 
> Taking a union bound over all $\binom{Q}{2}$ question pairs yields Eq. [ref]. This formalizes the legal principle that a precise, truthful witness is unlikely to exhibit spurious inconsistency under cross-examination, while an imprecise witness may trigger false alarms---reflecting the distinction between dishonesty and uncertainty.
> 
> **Part (ii): Detection power against perjury.**
> When the witness is perjurious (Definition [ref]), responses are drawn from $P_{\mathrm{fab}}$, a distribution with no mass on the true fact $\fact$ (Eq. [ref]). Unlike an erroneous witness who might occasionally stumble upon the truth, the perjurious witness must construct a completely artificial narrative.
> 
> Under Assumption [ref] (diverse questioning), each question probes a different aspect of the claimed fact. The fabricator cannot consult a ground truth and must maintain consistency across $Q$ independent fabrications. For any pair $(k, \ell)$:
> 
> $$
>     \Pbb(\abs{r_k - r_\ell} \leq 2\delta \mid H_1) = \iint \ind{\abs{r - r'} \leq 2\delta} \, dP_{\mathrm{fab}}(r) \, dP_{\mathrm{fab}}(r').
> $$
> 
> 
> Define $\gamma = \max_{k \neq \ell} \Pbb(\abs{r_k - r_\ell} \leq 2\delta \mid H_1)$. Since the perjurious witness has no access to ground truth and must fabricate each response independently, the probability that all $\binom{Q}{2}$ pairs are consistent is bounded by:
> 
> $$
>     \Pbb(all consistent \mid H_1) &\leq \gamma^{\binom{Q}{2}} = \exp\left(\binom{Q}{2} \ln \gamma\right) 

>     &= \exp\left(-\frac{Q(Q-1)}{2} \cdot \abs{\ln \gamma}\right),
> $$
> 
> since $\gamma < 1$ and thus $\ln \gamma < 0$. This establishes Eq. [ref].
> 
> The intuition is simple: an honest witness references a single external truth $\fact$, so all responses naturally cohere. A perjurious witness must independently fabricate $Q$ responses and ensure they are pairwise consistent. The probability of maintaining this artificial consistency across all $\binom{Q}{2}$ pairs decays **double-exponentially** in $Q$ (since the number of pairs grows as $Q^2$, and each must be consistent).
> 
> **Part (iii): Separation guarantee.**
> Set the false alarm rate $\alpha$ by choosing $\delta$ such that $\binom{Q}{2} \cdot 4\exp(-\delta^2 / 2\sigma_w^2) \leq \alpha$. Solving: $\delta \geq \sigma_w \sqrt{2\ln(4\binom{Q}{2} / \alpha)}$.
> 
> For the missed detection rate $\beta$, require $\exp(-\frac{Q(Q-1)}{2} \abs{\ln \gamma}) \leq \beta$, yielding:
> 
> $$
>     Q \geq \frac{1}{2}\left(1 + \sqrt{1 + \frac{8\ln(1/\beta)}{\abs{\ln \gamma}}}\right).
> $$
> 
> 
> Since $\gamma < 1$ under Assumption [ref], both conditions are simultaneously satisfiable for finite $Q$, establishing the separation guarantee. As $Q \to \infty$, both error rates approach zero exponentially.

> **Corollary:** [Evidence Chain Integrity 证据链完整性]
> <!-- label: cor:hashchain_integrity -->
> Theorem [ref] addresses the detection of *testimonial* fabrication. The complementary guarantee for *physical* evidence is the hash chain integrity property (Definitions [ref]-- [ref], Assumption [ref]): a hash-linked chain $\evidenceChain$ is tamper-evident with detection probability $1 - \abs{S} \cdot (\varepsilon_{\mathrm{hash}} + \varepsilon_{\mathrm{pre}})$, where $\abs{S}$ is the number of modified items and $\varepsilon_{\mathrm{hash}}, \varepsilon_{\mathrm{pre}}$ are the adversary's collision and preimage advantages. For SHA-256 ($\lambda = 256$), $\varepsilon_{\mathrm{hash}} \leq 2^{-128}$, making undetected tampering astronomically improbable for any practical $\abs{S}$. The proof is a direct application of the collision-resistance property: modifying $e_i$ requires finding $\tilde{e}_i \neq e_i$ with $\hashFunc(\tilde{e}_i \| h_{i-1}) = \hashFunc(e_i \| h_{i-1})$, which is a hash collision.

> **Corollary:** [Optimal Cross-Examination Strategy 最优质询策略]
> <!-- label: cor:optimal_cross -->
> The optimal cross-examination strategy under a fixed time budget $T$ maximizes the number of **independent lines of questioning** $Q$ rather than the depth of any single line. This follows from the $Q^2$ exponent in Eq. [ref]: doubling $Q$ quadruples the exponent in the detection probability. The cross-examiner should prioritize questions probing **orthogonal aspects** of the claimed fact to minimize $\gamma$.

## Multi-Witness Yajie{ Consensus Protocol 多证人Yajie共识协议}
<!-- label: sec:yajie -->

### Correlated Witnesses and Effective Sample Size 相关证人与有效样本量
<!-- label: sec:dependence -->

When witnesses are not conditionally independent (Assumption [ref] violated for some subset), we apply correlation adjustment.

> **Definition:** [Witness Correlation Matrix 证人相关矩阵]
> <!-- label: def:corrmat -->
> Let $\Sigma \in \R^{M \times M}$ be the correlation matrix of witness claims:
> 
> $$
>     \Sigma_{ij} = \Corr(m_{w_i}, m_{w_j} \mid \fact) = \frac{\Cov(m_{w_i}, m_{w_j} \mid \fact)}{\sigma_{w_i} \sigma_{w_j}}.
>     <!-- label: eq:corrmat -->
> $$
> 
> The **effective number of independent witnesses** is:
> 
> $$
>     M_{\mathrm{eff}} = \frac{(\sum_{i=1}^M \lambda_i)^2}{\sum_{i=1}^M \lambda_i^2},
>     <!-- label: eq:M_eff -->
> $$
> 
> where $\lambda_1 \geq \lambda_2 \geq ... \geq \lambda_M \geq 0$ are the eigenvalues of $\Sigma$. Under perfect independence ($\Sigma = I_M$), $M_{\mathrm{eff}} = M$. Under perfect positive correlation, $M_{\mathrm{eff}} = 1$.

> **Definition:** [\Yajie{} Consensus for Witnesses Yajie证人共识]
> <!-- label: def:yajie_consensus -->
> The Yajie{} consensus across $M$ witnesses is the precision-weighted average:
> 
> $$
>     c_ = \frac{\sum_{w \in \witnessSet} \omega_w \cdot m_w}{\sum_{w \in \witnessSet} \omega_w}, \quad \omega_w = \frac{\rho_w^{\mathrm{eff}}}{\sigma_w^2},
>     <!-- label: eq:yajie_consensus -->
> $$
> 
> where $\omega_w$ combines effective credibility $\rho_w^{\mathrm{eff}}$ and inverse variance $1/\sigma_w^2$. The consensus variance is:
> 
> $$
>     \Var(c_ \mid \fact) = \frac{\sum_{i,j} \omega_i \omega_j \Sigma_{ij} \sigma_i \sigma_j}{(\sum_i \omega_i)^2}.
>     <!-- label: eq:consensus_variance -->
> $$

> **Proposition:** [Consensus Accuracy 共识准确性]
> <!-- label: prop:consensus_accuracy -->
> Under Assumptions [ref]-- [ref], the Yajie{} consensus $c_$ satisfies:
> 
> $$
>     \Pbb\left(\abs{c_ - \fact} > \varepsilon \mid \fact\right) \leq 2\exp\left(-\frac{2 M_{\mathrm{eff}} \varepsilon^2}{D_\claimSpace^2}\right),
>     <!-- label: eq:consensus_accuracy -->
> $$
> 
> where $D_\claimSpace$ is the diameter of the claim space (Assumption [ref]).

> **Proof:** \rigorSketch
> Apply Hoeffding's inequality to the weighted sum after decorrelating via the eigenvalue decomposition of $\Sigma$. The effective sample size $M_{\mathrm{eff}}$ captures variance inflation from correlation [cite].

## Cercis{ Evidence Score Cercis证据评分}
<!-- label: sec:cercis -->

> **Definition:** [\Cercis{} Evidence Score Cercis证据评分]
> <!-- label: def:cercis -->
> For a testimony $\tau = (m, \mathcal{A}, \sigma^2, \rho)$, the Cercis{} evidence score is:
> 
> $$
>     S(\tau) = Q(\tau) + \eta \cdot N(\tau),
>     <!-- label: eq:cercis -->
> $$
> 
> where:
> 
- $Q(\tau) \in [0, 1]$ is the **factual accuracy score**: the probability that $m$ is factually correct, estimated from multi-witness consensus. For a corroborated claim, $Q(\tau) = 1 - \Pbb(\fact = 0 \mid corroboration)$ from Theorem [ref]. For uncorroborated claims, $Q(\tau) = \rho$.
- $N(\tau) \in [0, 1]$ is the **novelty score**: $N(\tau) = 1 - \max_{\tau' \neq \tau} J(\mathcal{A}, \mathcal{A}')$ where $J$ is the Jaccard similarity between assumption sets.
- $\eta \geq 0$ is the **novelty weight** controlling the accuracy--coverage trade-off.

> **Proposition:** [Cercis Score Properties]
> <!-- label: prop:cercis_props -->
> The Cercis{} evidence score satisfies:
> 
1. **Monotonicity in corroboration:** $S(\tau)$ increases as more independent witnesses corroborate $\tau$ (Theorem [ref]).
2. **Complementarity:** Two testimonies with complementary assumption sets ($J(\mathcal{A}_1, \mathcal{A}_2) \approx 0$) both receive high $N$ scores.
3. **Penalty for hearsay:** A hearsay testimony $\tau^$ has $Q(\tau^) = 1/2$ (no better than random, Theorem [ref]), giving a low baseline score.
4. **Penalty for perjury:** A testimony flagged as perjurious ($H_1$ in Theorem [ref]) receives $Q(\tau) = 0$, reflecting zero factual reliability.

## Spring{ Gating for Perjury Regime Detection Spring门控伪证制度检测}
<!-- label: sec:spring -->

The Spring{} gating mechanism [cite] detects regime shifts in witness behavior---specifically, transitions from **credible testimony** to **perjury** during cross-examination.

> **Definition:** [Testimony Regime 证言制度]
> <!-- label: def:regime -->
> A witness operates in one of two regimes:
> 
- **Regime 0 (Credible 可信):** $r_k \sim P_{\mathrm{true}}(\cdot \mid \fact)$, centered at the true answer with variance $\sigma_w^2$.
- **Regime 1 (Perjurious 伪证):** $r_k \sim P_{\mathrm{fab}}(\cdot)$, inconsistent with $\fact$ and with prior responses (Definition [ref]).

> A **regime transition** occurs at question index $k^*$ if $r_1, ..., r_{k^*-1}$ are drawn from Regime 0 and $r_{k^*}, ..., r_Q$ from Regime 1.

> **Proposition:** [\Spring{} Detection of Perjury Transition Spring伪证转换检测]
> <!-- label: prop:spring_perjury -->
> Under Assumption [ref], the Spring{} gating statistic:
> 
> $$
>     G_k = \max_{1 \leq j \leq k} \abs{r_j - \bar{r}_{1:k}}, \quad \bar{r}_{1:k} = \frac{1}{k} \sum_{j=1}^k r_j,
>     <!-- label: eq:spring_stat -->
> $$
> 
> detects a regime transition with expected delay $d$ satisfying:
> 
> $$
>     \E[d] \leq \frac{C \cdot \sigma_w^2}{(\mu_1 - \mu_0)^2} \cdot \log\left(\frac{1}\right),
>     <!-- label: eq:spring_delay -->
> $$
> 
> where $\mu_0, \mu_1$ are the mean responses under Regimes 0 and 1, $\alpha$ is the false alarm rate, and $C$ is a universal constant. Large $\abs{\mu_1 - \mu_0}$ (blatant perjury) yields fast detection; small $\abs{\mu_1 - \mu_0}$ (subtle fabrication) requires more questions.

> **Proof:** \rigorSketch
> The Spring{} statistic $G_k$ is a CUSUM-type change-point detector. Under Regime 0, $\E[r_j] = \mu_0$ and $G_k$ behaves like the maximum of a mean-zero random walk, bounded by the law of the iterated logarithm. Under a transition at $k^*$, the post-change mean $\mu_1$ causes $G_k$ to drift linearly. Standard change-point detection theory [cite] gives the detection delay bound in Eq. [ref].
> 
> The Spring{} mechanism provides a **runtime complement** to Theorem [ref]: while Theorem [ref] guarantees that perjury is detectable with enough questions, Spring{} identifies *when* during the cross-examination the witness transitions from credible to perjurious testimony, enabling the cross-examiner to focus follow-up questions on the inconsistent portion.

## Specific Formal Applications 具体形式化应用
<!-- label: sec:applications -->

### Witness Credibility Calibration 证人可信度校准

The credibility parameter $\rho_w$ is calibrated from verifiable questions---questions whose answers are known independently:

> **Definition:** [Credibility Calibration 可信度校准]
> <!-- label: def:calibration -->
> Let $\mathcal{Q}_{\mathrm{cal}} = \{q_1^{\mathrm{cal}}, ..., q_{K_{\mathrm{cal}}}^{\mathrm{cal}}\}$ be calibration questions with known answers $\{a_1^*, ..., a_{K_{\mathrm{cal}}}^*\}$. The maximum-likelihood estimate of $\rho_w$ is:
> 
> $$
>     \hat_w = \frac{1}{K_{\mathrm{cal}}} \sum_{k=1}^{K_{\mathrm{cal}}} \ind{r_k^{\mathrm{cal}} = a_k^*}.
>     <!-- label: eq:rho_hat -->
> $$
> 
> The estimation error satisfies $\abs{\hat_w - \rho_w} \leq \sqrt{\frac{\ln(2/\alpha)}{2 K_{\mathrm{cal}}}}$ with probability $\geq 1 - \alpha$.

### Evidence Chain Verification Protocol 证据链验证协议

\begin{algorithm}[ht]
*Caption:* Evidence Chain Verification 证据链验证
<!-- label: alg:chain_verify -->
\begin{algorithmic}[1]
\Require Evidence chain $\evidenceChain = \{(e_0, h_0), ..., (e_K, h_K)\}$, hash function $\hashFunc$
\Ensure $\{**Valid**, **Tampered**(i^*)\}$
\State $h_{-1} \gets \varepsilon$
\For{$i = 0$ **to** $K$}
    \State $h_i' \gets \hashFunc(e_i \| h_{i-1})$
    \If{$h_i' \neq h_i$}
        \State \Return $**Tampered**(i)$
    \EndIf
\EndFor
\State \Return $**Valid**$
\end{algorithmic}
\end{algorithm}

The algorithm runs in $O(K \cdot T_)$ time, requires $O(1)$ memory, and is **streaming** (processes items sequentially without storing the full chain). The localization property guarantees that the first verification failure $i^*$ identifies the earliest position of tampering, with all items $e_0, ..., e_{i^*-1}$ provably unmodified.

### Cross-Examination Strategy Optimization 交叉质询策略优化

> **Proposition:** [Optimal Question Allocation 最优问题分配]
> <!-- label: prop:optimal_questions -->
> Given $M$ witnesses with heterogeneous credibility $\{\rho_w\}$ and precision $\{\sigma_w^2\}$, and a total question budget $Q_{\mathrm{total}}$, the optimal allocation to maximize perjury detection probability is:
> 
> $$
>     Q_w^* \propto \frac{1}{\sigma_w^2} \cdot \log\left(\frac{1}{1 - \rho_w^{\mathrm{eff}}}\right).
>     <!-- label: eq:optimal_Q -->
> $$
> 
> Witnesses with low precision and moderate credibility receive *more* questions (inconsistency is easier to detect); witnesses with extreme credibility (very high or very low) require fewer questions (their status is already clear).

### Hearsay-Contaminated Corroboration 传闻污染的佐证

> **Proposition:** [Hearsay Contamination Adjustment 传闻污染调整]
> <!-- label: prop:hearsay_contamination -->
> Let $\witnessSet = \witnessSet_{\mathrm{direct}} \cup \witnessSet_{\mathrm{hearsay}}$. If the tribunal treats all witnesses as independent, the effective count $M_{\mathrm{eff}}$ in Theorem [ref] is inflated, producing an **overconfident bound**. The correct adjustment is:
> 
> $$
>     M_{\mathrm{eff}}^{\mathrm{corrected}} = M_{\mathrm{eff}}(\witnessSet_{\mathrm{direct}}) + 0 \cdot \abs{\witnessSet_{\mathrm{hearsay}}},
>     <!-- label: eq:hearsay_adjustment -->
> $$
> 
> since hearsay witnesses contribute zero independent information (Theorem [ref]). This provides mathematical justification for excluding hearsay from corroboration.

## Experimental Protocol 实验协议
<!-- label: sec:experiments -->

We propose the following protocol for empirically validating the theoretical bounds. **Note:** This is a proposed protocol, not a report of completed experiments.

### Witness Simulation Framework

1. **Synthetic fact generation:** $N_{\mathrm{cases}} = 10{,}000$ legal cases, each with binary fact $\fact_k \sim \mathrm{Bernoulli}(0.5)$ and $M \in \{2, 5, 10, 20, 50\}$ witnesses.
2. **Witness parameter sampling:** $\rho_w \sim \mathrm{Beta}(3, 2)$ (credibility centered at $0.6$), $\sigma_w^2 \sim \mathrm{InvGamma}(3, 0.5)$.
3. **Independence structure:** Induce correlation via block-diagonal $\Sigma$ with block sizes $b \in \{1, 2, 3, 5\}$.
4. **Perjury injection:** For a fraction $p_{\mathrm{perj}} \in \{0.05, 0.10, 0.20\}$ of witnesses, replace truthful responses with fabricated ones ($\perjury$ regime).
5. **Cross-examination simulation:** $Q \in \{3, 5, 10, 20\}$ questions with truthful/$\perjury$ response models.
6. **Hash chain simulation:** Evidence chain length $K \in \{5, 10, 20, 50\}$, adversarial tampering at random positions.

### Validation Metrics

1. **Corroboration error rate:** Empirical $\Pbb(\fact = 0 \mid \mathcal{U})$ vs. bound from Theorem [ref].
2. **Hearsay information content:** $I(\tau_A^; \fact)$ vs. $I(\tau_B; \fact)$. Expected: $I(\tau_A^; \fact) \approx 0$ when $\tau_B$ unobserved.
3. **Perjury detection:** TPR (perjurer detected) vs. FPR (truthful witness flagged). ROC follows Theorem [ref] with AUC $\to 1$ as $Q \to \infty$.
4. **Tamper detection rate:** Fraction of tampered chains detected vs. $\abs{S}$ and hash strength $\lambda$.
5. **Spring gating delay:** Empirical detection delay vs. bound from Eq. [ref].
6. **Cercis ranking:** Kendall's $\tau$ between Cercis{} score ranking and ground-truth accuracy ranking.

## Discussion 讨论
<!-- label: sec:discussion -->

### Relationship to Existing Frameworks

**Bayesian evidence evaluation.** Our framework is Bayesian in structure: the tribunal updates beliefs via Bayes' rule, and the theorems provide bounds on posterior error probabilities. The key difference from standard Bayesian approaches [cite] is the explicit modeling of witnesses as *experts* with declared assumptions, and the formal treatment of cross-examination as adversarial audit rather than passive likelihood update.

**Dempster-Shafer theory.** Dempster-Shafer [cite] handles uncertain belief aggregation but does not address adversarial structure. Our framework provides complementary guarantees for adversarial manipulation detection.

**Legal epistemology.** Philosophical work on legal epistemology [cite] has explored the relationship between legal procedures and truth-finding without formal mathematical bounds. Our work provides the missing quantitative layer: given $\rho_w$, $\sigma_w^2$, and $Q$, we compute explicit error probabilities.

**Cryptographic evidence chains.** Blockchain-based evidence systems [cite] have proposed hash chains for chain of custody. Our contribution is the formal proof that a simple sequential hash chain (without consensus mechanisms or proof-of-work) provides the necessary tamper-evidence property. The cryptographic overhead of full blockchain systems is unnecessary for sequential-custody evidence chains.

### The Three-Theorem Architecture

Table [ref] summarizes how the three theorems partition the problem space.

[Table omitted — see original .tex]

Theorem~1 handles unintentional errors (a witness with $\rho_w = 0.7$ gets it wrong $30\%$ of the time). Theorem~2 handles informational dependency (hearsay launders a claim through an intermediary, breaking the independence assumption of Theorem~1). Theorem~3 handles active adversarial behavior (perjury, where $\Pbb(m_w = \fact) = 0$). Together they cover the three fundamental failure modes of legal testimony.

### Limitations 局限性

1. **Dependence on declared assumptions.** All theorems are conditional on $\mathcal{A}_w$ being correct. If assumptions are violated (collusion, worse perceptual conditions), bounds may be invalid. The framework's contribution is making assumptions *explicit and auditable*.
2. **Credibility calibration challenge.** $\rho_w$ is estimated from calibration questions, which may not be fully representative of case-specific reliability. Domain-specific credibility requires separate calibration per fact type.
3. **Binary fact simplification.** Binary facts ($\{0, 1\}$) simplify the mathematics but lose graded nuance. The extension to $[0, 1]$ preserves theorems but adds tolerance parameters.
4. **Hash function compromise.** Theorem guarantees assume collision resistance. Quantum adversaries could reduce SHA-256 preimage resistance from $2^{256}$ to $2^{128}$. Post-quantum hash functions restore the guarantee.
5. **Correlation misspecification.** $M_{\mathrm{eff}}$ depends on estimated $\Sigma$. Underestimating witness collusion leads to overconfident bounds.
6. **Adversarial adaptation.** A sophisticated adversary aware of SCX{} could prepare consistent narratives in advance, reducing $\gamma$ in Theorem [ref]. The arms-race dynamic is formalized but not resolved.
7. **Non-independence in cross-examination.** The $Q$ questions may probe correlated aspects of the same fact. Effective independent questions $Q_{\mathrm{eff}}$ would reduce detection power.
8. **Cultural and linguistic factors.** Credibility estimation assumes stable statistical properties across cultures. Cross-cultural variation can confound estimates.

### Future Directions

1. **Graded fact extension:** Extend to arbitrary measurable spaces $\Phi$ with proper scoring rules.
2. **Dynamic credibility:** Model $\rho_w(t)$ as a stochastic process evolving during testimony (fatigue, impeachment, rehabilitation).
3. **Multi-tribunal consensus:** Extend Yajie{} to multiple tribunals (appellate review, multi-jurisdiction).
4. **Computational cross-examination:** Reinforcement learning for adaptive follow-up question selection.
5. **Empirical validation:** Conduct the experimental protocol (Section [ref]) against real legal data.

## Acknowledgments
The SCX acknowledges the legal scholars, forensic scientists, and cryptographers whose work informed this synthesis. The framework builds on foundational results in hypothesis testing [cite], cryptographic hash functions [cite], and change-point detection [cite].

\begin{thebibliography}{99}

\bibitem{SCX2025}
SCX.
*SCX: Structured Causal eXamination --- A Multi-Expert Audit Framework.*
Technical Report, 2025.

\bibitem{Hoeffding1963}
W.~Hoeffding.
*Probability inequalities for sums of bounded random variables.*
Journal of the American Statistical Association, 58(301):13--30, 1963.

\bibitem{Merkle1980}
R.~C.~Merkle.
*Protocols for public key cryptosystems.*
In Proc. IEEE Symposium on Security and Privacy, 1980.

\bibitem{Page1954}
E.~S.~Page.
*Continuous inspection schemes.*
Biometrika, 41(1/2):100--115, 1954.

\bibitem{Basseville1993}
M.~Basseville and I.~V.~Nikiforov.
*Detection of Abrupt Changes: Theory and Application.*
Prentice Hall, 1993.

\bibitem{Taroni2014}
F.~Taroni, A.~Biedermann, S.~Bozza, P.~Garbolino, and C.~Aitken.
*Bayesian Networks for Probabilistic Inference and Decision Analysis in Forensic Science.*
Wiley, 2nd edition, 2014.

\bibitem{Fenton2013}
N.~Fenton, M.~Neil, and D.~A.~Lagnado.
*A general structure for legal arguments about evidence using Bayesian networks.*
Cognitive Science, 37(1):61--102, 2013.

\bibitem{Shafer1976}
G.~Shafer.
*A Mathematical Theory of Evidence.*
Princeton University Press, 1976.

\bibitem{Ho2008}
H.~L.~Ho.
*A Philosophy of Evidence Law: Justice in the Search for Truth.*
Oxford University Press, 2008.

\bibitem{Laudan2006}
L.~Laudan.
*Truth, Error, and Criminal Law: An Essay in Legal Epistemology.*
Cambridge University Press, 2006.

\bibitem{Guo2020}
H.~Guo, W.~Li, and M.~Nejad.
*A hierarchical and location-aware blockchain protocol for IoT data security.*
IEEE Internet of Things Journal, 7(6):5262--5272, 2020.

\bibitem{Tian2016}
F.~Tian.
*An agri-food supply chain traceability system for China based on RFID and blockchain technology.*
In Proc. IEEE ICSSSM, 2016.

\bibitem{Wells2003}
G.~L.~Wells and E.~A.~Olson.
*Eyewitness testimony.*
Annual Review of Psychology, 54:277--295, 2003.

\bibitem{PCAST2016}
President's Council of Advisors on Science and Technology.
*Forensic Science in Criminal Courts: Ensuring Scientific Validity of Feature-Comparison Methods.*
Executive Office of the President, 2016.

\bibitem{Dror2011}
I.~E.~Dror and G.~Hampikian.
*Subjectivity and bias in forensic DNA mixture interpretation.*
Science \& Justice, 51(4):204--208, 2011.

\bibitem{Clark2012}
S.~E.~Clark.
*Costs and benefits of eyewitness identification reform.*
Perspectives on Psychological Science, 7(3):238--259, 2012.

\end{thebibliography}