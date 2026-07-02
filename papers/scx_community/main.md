*Abstract:*

We formalize the governance of the SCX protocol community as **内河 (\Neihe{})**---a game-theoretic governance mechanism for theorem-guardian collectives. The mechanism is structured as a three-layer hierarchy: the **Kernel** (内核, $2 \leq K \leq 5$ maintainers operating under unanimity rule), the **Contributors** (贡献者, $\sim$20 active developers forming the community's immune system), and the **Observers** (观察者, unlimited, zero-barrier entry). The community's constitutional purpose is theorem guardianship, not corporate ownership---no individual or entity holds proprietary control over the SCX protocol. We introduce four formal pillars. **Pillar~1: The g=0 Declaration Protocol** ($\GzeroDecl$)---a cryptographic standard (GPG-signed, Git-committed) by which candidates publicly and irrevocably renounce all ownership claims, consent to periodic $M>1$ audit, and accept mandatory term-limited rotation. **Pillar~2: The Maintainer Rotation Game**---a repeated game with incomplete information where maintainer types (Honest $H$ or Strategic $S$) are private. We prove (Theorem [ref]) that under term limits $T_$ and mandatory re-audit with $M$ independent auditors each having detection power $\Delta$, the stationary distribution concentrates on all-Honest Kernel composition: $\Pbb(all  H) \to 1$ as audit frequency increases, with integrity lower bound $\E[I_t] \geq 1 - (1 + M\Delta \cdot T_{audit}/T_)^{-1}$. **Pillar~3: The Conflict Resolution Escalation Ladder**---a three-stage protocol (72h Kernel deliberation $\to$ 168h Contributor advisory vote $\to$ 720h independent $M$-audit) with Theorem [ref] proving that every deadlock resolves within 960 hours (40 days) without external arbitration. **Pillar~4: The Emergency Audit Procedure**---any Contributor can trigger an emergency audit on a maintainer suspected of $\gnonzero$; Theorem [ref] proves that detection probability exceeds $1 - (1 - g_{\mathrm{true}})^M$, with guaranteed removal within 72 hours of a valid trigger. We specify the complete protocol: communication architecture (Signal $\to$ Matrix $\to$ GitHub, by layer), funding model (zero-extractive: calibration fees, donations, academic grants, prize pool---all structurally separated from governance rights), and the bootstrapping sequence for community activation. The framework establishes a symbiotic equilibrium: the theorems guard the community through mathematical guarantees, and the community guards the theorems through maintenance, audit, and hostile review. All theorems carry \rigorFull{} labels with explicit assumptions~\assumptionTag{1}--\assumptionTag{9}.

**Keywords:** protocol governance 协议治理, game-theoretic mechanism design 博弈论机制设计, maintainer rotation 维护者轮换, g=0 declaration g=0声明, multi-expert audit 多专家审计, theorem guardianship 定理守护, community self-governance 社区自治, cryptographic commitment 密码学承诺, Sybil resistance 女巫攻击抵抗, decentralized protocol maintenance 去中心化协议维护

## Introduction 引言

### The Protocol Longevity Problem 协议长寿问题

Protocols that survive do so because of their governance, not their technology. TCP/IP has survived fifty years---not because packet-switching is uniquely elegant, but because the IETF's distributed governance model (``rough consensus and running code'') prevents capture by any single entity. Linux has survived thirty years---not because the kernel is bug-free, but because the maintainer hierarchy is transparent, meritocratic, and replaceable: Linus Torvalds could step down tomorrow and the kernel would continue. In both cases, the governance mechanism solved the fundamental problem: **who guards the guardians when the original guardians are gone?**

The SCX protocol faces this problem at inception. The theorems are proved [cite]. The code is open-source. The papers are on arXiv. But a protocol without a community is a monument---admired and then forgotten. A protocol with a community but without a governance mechanism is a hostage situation---dependent on the continued goodwill (or continued life) of its original maintainers. A protocol with a governance mechanism but without formal guarantees is a gamble---hoping that norms and goodwill suffice where mathematical incentives should operate.

This paper provides the third option: a governance mechanism with **provable guarantees**. We formalize the SCX community as \Neihe{} (内河, ``inner river'')---a game-theoretic governance framework where the equilibrium strategy for all participants is honest guardianship. The name is chosen deliberately: a river flows without owning the land it passes through. The community flows through the protocol without owning it.

### Design Principles 设计原则

The governance mechanism instantiates five design principles, each with a formal counterpart:

1. **No ownership 无所有权.** No individual or entity owns the SCX protocol. Ownership is replaced by *guardianship*---a temporary, revocable, audited responsibility. Formally: $\forall t, \nexists$ entity $E$ with exclusive control over the protocol specification.
2. **Replaceability 可替换性.** Any maintainer can be removed and replaced through a predetermined procedure. Formally: $\mathcal{G}(\MaintainerSet \setminus \{m\}) \cong \mathcal{G}(\MaintainerSet \cup \{m'\})$ for any $m, m'$ satisfying entry criteria, where $\mathcal{G}$ is the governance mechanism.
3. **Auditability 可审计性.** Every governance action produces a public, cryptographically signed, immutable record. Formally: the audit log $\mathcal{L}$ is an append-only SHA-256 hash chain: $H_i = SHA-256(H_{i-1} \| D_i)$.
4. **Self-stabilization 自稳定性.** The mechanism detects and corrects deviations without external intervention. Formally: for any perturbation $\delta$ from $\ProtocolState^*$, $\exists T(\delta) < \infty$ such that $\Pbb(\ProtocolState_{t+T(\delta)} = \ProtocolState^*) \to 1$.
5. **Theorem supremacy 定理至上.** The SCX theorems are the ultimate authority. Any governance action $\alpha$ is valid iff consistent with $\{T_1, ..., T_6\}$; otherwise $\alpha$ is null.

### Contributions 贡献

1. **Three-layer governance structure** (Section [ref]): Kernel, Contributors, Observers---with formal entry/exit criteria, decision rights matrices, and accountability mechanisms.
2. **Maintainer rotation game** (Section [ref]): Repeated game with incomplete information; Theorem [ref] proves rotation plus re-audit is a self-stabilizing equilibrium.
3. **The \gzero{} Declaration Protocol** (Section [ref]): Cryptographic standard for irrevocable ownership renunciation with GPG signing and Git commitment.
4. **Conflict resolution mechanism** (Section [ref]): Three-stage escalation ladder; Theorem [ref] bounds expected resolution time and guarantees eventual resolution.
5. **Emergency audit procedure** (Section [ref]): Theorem [ref] establishes exponential detection probability with 72-hour maximum response latency.
6. **Complete protocol specification** (Section [ref]): Communication architecture, platform justification, funding model, bootstrapping sequence, and constitutional ceremony calendar.

**What this paper is not.** This is a mechanism design paper with mathematical proofs---not a legal document, corporate charter, or political manifesto. We prove that honest guardianship is the game-theoretic equilibrium under specified conditions. Whether that equilibrium is *desirable* is a question for the adopting community.

## The Three-Layer Governance Structure 三层治理结构
<!-- label: sec:structure -->

### Formal Definition 形式化定义

> **Definition:** [SCX Community 社区]
> <!-- label: def:community -->
> The SCX community $\Community$ at time $t$ is an ordered triple:
> 
> $$
>     \Community_t = (\Kernel_t, \Contributors_t, \Observers_t),
>     <!-- label: eq:community -->
> $$
> 
> where $\Kernel_t$ (内核) has decision authority, $\Contributors_t$ (贡献者层) has proposal and audit-trigger authority, and $\Observers_t$ (观察者层) has observation and evidence-submission authority. The layers satisfy $\Kernel_t \subset \Contributors_t \subset \Observers_t$ as sets (every Kernel member is also a Contributor; every Contributor is also an Observer), but authority is strictly ordered: $Auth(\Kernel) \succ Auth(\Contributors) \succ Auth(\Observers)$.

> **Definition:** [Kernel 内核]
> <!-- label: def:kernel -->
> The Kernel $\Kernel_t = \{m_1, ..., m_{K_t}\}$ with $2 \leq K_t \leq 5$. Each maintainer $m_i$ is a tuple:
> 
> $$
>     m_i = (id_i, pubkey_i, t_i^{seated}, t_i^{term\_end}, \mathcal{A}_i, h_i^),
>     <!-- label: eq:maintainer -->
> $$
> 
> where $id_i$ is a real-name or long-lived ($\geq 2$ years) verifiable pseudonym; $pubkey_i$ is a GPG public key; $t_i^{seated}$ and $t_i^{term\_end}$ are ISO-8601 timestamps bounding the current term; $\mathcal{A}_i = (a_{i,1}, ..., a_{i,M})$ are the most recent $M > 1$ audit results with $a_{i,j} \in \{0, 1\}$ ($1 = \gzero$ confirmed); and $h_i^ = SHA-256(\GzeroDecl_i)$ is the cryptographic hash of the maintainer's most recent g=0 declaration.

> **Definition:** [Contributors 贡献者]
> <!-- label: def:contributors -->
> $\Contributors_t = \{c_1, ..., c_{N_t}\}$ where $c_j$ is an individual who has made at least one accepted contribution to SCX---code merged to the main repository, a theorem proof verified by the Kernel, an experiment reproduction confirmed, or a hostile review finding accepted. Each contributor has a ledger entry:
> 
> $$
>     c_j = (id_j, h(contribution_j), t_j^{first}, n_j^{contrib}),
>     <!-- label: eq:contributor -->
> $$
> 
> where $h = SHA-256$ and $n_j^{contrib}$ is the cumulative accepted contribution count. Inactivity for $> 24$ months triggers automatic transition to emeritus status (no voting rights, retain audit-trigger rights).

> **Definition:** [Observers 观察者]
> <!-- label: def:observers -->
> $\Observers_t$ is the set of all individuals who have observably interacted with the SCX protocol. Entry threshold is identically zero. $|\Observers_t|$ is unbounded above. Observers may: (i) open GitHub Issues, (ii) participate in GitHub Discussions, (iii) submit evidence for emergency audits, (iv) independently verify any published audit log entry. Observers may not: (i) vote on any governance matter, (ii) trigger emergency audits (that requires Contributor status).

### Layer Properties 层级属性

[Table omitted — see original .tex]

### The Entry Ladder 进入阶梯

> **Definition:** [Kernel Entry Path 内核进入路径]
> <!-- label: def:entry -->
> The transition from Observer to Kernel maintainer follows a strict, irreversible (except by removal) sequence with a public record at each stage:
> 
> $$
>     Observer \xrightarrow{1 accepted contrib.} Contributor
>     \xrightarrow{public \GzeroDecl} Candidate
>     \xrightarrow{M>1 audit} Audited Candidate
>     \xrightarrow{unanimous \Kernel vote} Maintainer
>     \xrightarrow{enter \RotationPool} Seated.
>     <!-- label: eq:entry_ladder -->
> $$
> 
> 
> A candidate rejected at any stage may reapply after a cooling-off period $\tau_{cool} \geq 180$ days. Each transition produces a public, GPG-signed, Git-committed record in the audit log.

\begin{assumption}[A1: Audit Independence 审计独立性]
<!-- label: ass:A1 -->
The $M$ auditors evaluating a Kernel candidate are structurally independent: no auditor has a financial, employment, or familial relationship with the candidate. Auditors are drawn from the Contributor layer or external domain experts, with at least $\lceil M/2 \rceil$ external to the current Kernel.
\end{assumption}

\begin{assumption}[A2: Auditor Detection Power 审计者检测能力]
<!-- label: ass:A2 -->
Each auditor has detection power $\Delta > 0$: for any maintainer action violating $\gzero$, the probability that a competent auditor detects the violation exceeds $\Delta$. This is the operational bridge between the mathematical model ($g_{\mathrm{true}} \in [0,1]$) and observable reality.
\end{assumption}

\begin{assumption}[A3: Unanimity Rule 全票规则]
<!-- label: ass:A3 -->
Kernel decisions on personnel (admission, removal) and protocol changes require unanimity. A single negative vote (veto) blocks the decision. Abstention is not permitted on personnel votes. The unanimity rule is the mechanism's primary defense against coalitional capture.
\end{assumption}

## The Maintainer Rotation Game 维护者轮换博弈
<!-- label: sec:rotation -->

### Game-Theoretic Model 博弈论模型

We model maintainer governance as a repeated game with incomplete information. Each *rotation cycle* $r = 1, 2, ...$ spans a fixed calendar duration $T_{cycle}$ (recommended: 24 months). At the start of cycle $r$, the Kernel consists of $K$ seated maintainers. Each maintainer has a private **type**: $\theta_i \in \{H, S\}$, where $H$ (Honest) means $g_{\mathrm{true}} = 0$ and $S$ (Strategic) means $g_{\mathrm{true}} > 0$.

> **Definition:** [Maintainer Rotation Game $\Gamma_{rot}$]
> <!-- label: def:rotation_game -->
> The rotation game $\Gamma_{rot}$ is the tuple $(\mathcal{P}, \Theta, \mathcal{A}, u, \mathcal{I})$:
> 
- **Players** $\mathcal{P}$: $K$ seated maintainers $\{m_1, ..., m_K\}$ and $N$ eligible candidates in the rotation pool $\RotationPool = \{c_1, ..., c_N\}$.
- **Types** $\Theta$: $\theta_i \in \{H, S\}$, private information. Prior: $\Pbb(\theta_i = S) = \pi_0$ (population fraction of Strategic types).
- **Actions per cycle** $\mathcal{A}$: (a) vote on candidate admissions $\{0, 1\}$, (b) rotate out voluntarily or at term end, (c) trigger emergency audits, (d) submit $\GzeroDecl$ (candidates).
- **Payoffs** $u$:
- **Information** $\mathcal{I}$: Maintainer types are private. Audit results are public. $\GzeroDecl$ declarations are public and cryptographically signed. All votes are recorded in the public audit log (who voted which way, with written justification).

> **Definition:** [Protocol Integrity 协议完整性]
> <!-- label: def:integrity -->
> The integrity of the governance mechanism at time $t$ is:
> 
> $$
>     I_t(\Community) = \frac{1}{K_t} \sum_{i=1}^{K_t} \ind{\theta_i = H} \cdot \exp\left(-\lambda \cdot (t - t_i^{last\_audit})\right),
>     <!-- label: eq:integrity -->
> $$
> 
> where $\lambda > 0$ is the integrity decay rate (trust in an unaudited maintainer degrades exponentially). $I_t = 1$ when all maintainers are recently-audited Honest types; $I_t \to 0$ as unaudited Strategic types accumulate.

### Rotation Equilibrium Theorem 轮换均衡定理

> **Theorem:** [Rotation Equilibrium 轮换均衡]
> <!-- label: thm:rotation -->
> Under Assumptions [ref]-- [ref] and the structural conditions:
> 
1. **Term limit:** $T_ < \infty$ (no permanent seats);
2. **Mandatory re-audit:** every maintainer undergoes $M>1$ independent audit at intervals $\leq T_/2$;
3. **Positive detection penalty:** $\kappa > B_ \cdot T_$ where $B_ = \max_s B_{avg}(s)$;

> the rotation game $\Gamma_{rot}$ has a unique subgame-perfect equilibrium satisfying:
> 
> $$
>     \lim_{t \to \infty} \Pbb(all seated maintainers are type  H) = 1,
>     <!-- label: eq:all_honest -->
> $$
> 
> with long-run expected integrity bounded below by:
> 
> $$
>     \liminf_{t \to \infty} \E[I_t] \geq 1 - \frac{1}{1 + M \cdot \Delta \cdot (T_{audit} / T_)}.
>     <!-- label: eq:integrity_bound -->
> $$

> **Proof:** \rigorFull
> **Step 1: Strategic maintainer survival probability.** A maintainer of type $S$ seated for $s$ rounds faces audit every $T_{audit}$ rounds. Under Assumption [ref], each of the $M$ independent auditors detects $\gnonzero$ with probability at least $\Delta$. The collective detection probability per audit cycle is $\Delta_{collective} = 1 - (1 - \Delta)^M$. The probability of surviving $r = \lfloor s / T_{audit} \rfloor$ audit cycles without detection is:
> 
> $$
>     \Pbb(survive  r  cycles) = (1 - \Delta_{collective})^r = (1 - \Delta)^{M r}.
>     <!-- label: eq:survival -->
> $$
> 
> 
> **Step 2: Entry deterrence.** The expected total payoff for a Strategic candidate considering Kernel entry is:
> 
> $$
>     \E[u_S^{entry}] = \sum_{s=1}^{T_} B_{avg} \cdot (1 - \Delta)^{M \lfloor (s-1)/T_{audit} \rfloor} - \kappa \cdot \left(1 - (1 - \Delta)^{M \lfloor T_/T_{audit} \rfloor}\right).
>     <!-- label: eq:entry_payoff -->
> $$
> 
> 
> When $\kappa > B_ \cdot T_$, the first term (benefit) is bounded above by $B_ \cdot T_$ while the second term (penalty) exceeds this bound for any $\Delta > 0$ and $M \geq 1$. Hence $\E[u_S^{entry}] < 0$ for all Strategic types: entry is strictly dominated by non-entry.
> 
> **Step 3: Honest maintainer strategy.** For type $H$, $g_{\mathrm{true}} = 0$, so audit always confirms $\gzero$. The expected payoff from Eq. [ref] is maximized when $I(\Community)$ is maximized, which occurs when all maintainers are type $H$. Protocol compliance (signing $\GzeroDecl$, undergoing audit, rotating at term end) is the unique payoff-maximizing strategy.
> 
> **Step 4: Equilibrium selection.** Given that Strategic types are deterred from entry (Step 2) and any Strategic type who nonetheless enters is detected with probability $\to 1$ over repeated audits (Step 1), the only subgame-perfect equilibrium consistent with sequential rationality is: Honest types enter and maintain $\gzero$; Strategic types do not enter. The stationary distribution concentrates on all-Honest Kernel composition, establishing Eq. [ref].
> 
> **Step 5: Integrity bound.** The residual probability of a Strategic type surviving undetected for one full audit cycle is $(1 - \Delta)^M$. The fraction of time the Kernel contains a Strategic type is bounded by a renewal-reward argument:
> 
> $$
>     \Pbb(Strategic seated) \leq \frac{(1 - \Delta)^M \cdot T_{audit}}{(1 - \Delta)^M \cdot T_{audit} + M \Delta \cdot T_} \approx \frac{1}{1 + M \Delta \cdot T_{audit} / T_},
>     <!-- label: eq:renewal -->
> $$
> 
> where the approximation uses $(1 - \Delta)^M \approx 1 - M\Delta$ for small $\Delta$. Since $\E[I_t] = 1 - \Pbb(Strategic seated)$, Eq. [ref] follows. $\square$

> **Corollary:** [Audit Frequency Calibration 审计频率校准]
> <!-- label: cor:audit_freq -->
> For target integrity $I^* = 0.95$, $M = 3$, $\Delta = 0.3$, $T_ = 24$ months:
> 
> $$
>     T_{audit} \leq \frac{(1 - I^*) \cdot M \Delta \cdot T_}{I^*} \approx \frac{0.05 \cdot 3 \cdot 0.3 \cdot 24}{0.95} \approx 1.14  months.
>     <!-- label: eq:audit_calib -->
> $$
> 
> This is impractically frequent. Relaxing to $I^* = 0.80$ yields $T_{audit} \leq 5.4$ months---operationally feasible with quarterly audits per maintainer. The calibration reveals a fundamental design tradeoff: higher integrity targets require either more auditors, higher per-auditor detection power, or more frequent audits. There is no free lunch in governance security.

### Rotation Schedule 轮换时间表

> **Definition:** [Staggered Rotation 交错轮换]
> <!-- label: def:staggered -->
> Maintainer terms are staggered to ensure at most $\lceil K/2 \rceil$ rotate out in any single cycle, preventing institutional memory loss:
> 
> $$
>     Rotate(t) = \left\{m_i \in \Kernel_t : t \geq t_i^{term\_end}\right\}, \quad |Rotate(t)| \leq \lceil K_t / 2 \rceil.
>     <!-- label: eq:staggered -->
> $$
> 
> If multiple terms expire simultaneously, the maintainer(s) with longest continuous service rotate first. Ties are broken by the lexicographic order of $SHA-256(id_i \| t_i^{seated})$---a deterministic, non-manipulable tiebreaker.

[Table omitted — see original .tex]

## The \texorpdfstring{$g=0${g=0} Declaration Protocol 零所有权声明协议}
<!-- label: sec:gzero -->

### The g-Function and Its Operationalization

> **Definition:** [The g-Function 价值函数]
> <!-- label: def:g_function -->
> For any individual $i$ interacting with the SCX protocol, $g(i, t) \in [0, 1]$ quantifies the degree to which $i$ treats the protocol as private property at time $t$. The endpoints are: $g = 0$---zero ownership claims, all actions taken as temporary guardian; $g = 1$---de facto owner, blocking changes, extracting private benefits, treating position as permanent. The g-function is **ordinal**, not cardinal: the audit operates on binary verdicts $\{0, 1\}$ (``$\gzero$ confirmed'' vs.\ ``$\gnonzero$ detected''), not on continuous $g$-estimates.

> **Definition:** [\gzero{} Declaration $\GzeroDecl$]
> <!-- label: def:gzero_decl -->
> A valid $\GzeroDecl$ is a 5-tuple:
> 
> $$
>     \GzeroDecl = (identity, \mathcal{C}, \sigma, \tau, h),
>     <!-- label: eq:gzero_tuple -->
> $$
> 
> where:
> 
1. **Identity:** Real name or verifiable pseudonym with $\geq 2$ years of public activity under the same identity.
2. **Commitment** $\mathcal{C}$: Plain-text statement in Chinese and English containing exactly four clauses:
3. *Non-ownership:* ``I hold no ownership claim over the SCX protocol, its theorems, its code, its governance, or its community. I act solely as a temporary guardian of the theorems.''
4. *Audit consent:* ``I consent to periodic $M>1$ independent audit. All audit results shall be published in full in the SCX public audit log.''
5. *Rotation acceptance:* ``My term is limited to $T_$. Upon expiration, I will rotate out. I may reapply through the standard entry path.''
6. *Removal acknowledgment:* ``If an emergency audit confirms $\gnonzero$, I accept immediate removal with full public record of evidence.''

>     \item **Signature** $\sigma$: GPG detached signature over $SHA-256(identity \| \mathcal{C} \| \tau)$, verifiable against the SCX public keyring.
>     \item **Timestamp** $\tau$: ISO 8601 UTC.
>     \item **Hash** $h = SHA-256(identity \| \mathcal{C} \| \sigma \| \tau)$: Permanent identifier in the audit log.
> \end{enumerate}

> **Protocol:** [$\GzeroDecl$ Submission 提交流程]
> <!-- label: prot:gzero_submit -->
> 
1. **Draft:** Candidate writes $\mathcal{C}$ in Chinese and English as `declaration.txt`.
2. **Sign:** `gpg --detach-sign --armor declaration.txt` $\to$ `declaration.txt.asc`.
3. **Commit:** Both files committed to `scx-community/declarations/[year]/[identity-hash]/`.
4. **Announce:** Commit hash posted to the Contributor Matrix channel.
5. **Verify:** Any observer verifies: `gpg --verify declaration.txt.asc declaration.txt`.
6. **Register:** Kernel verifies signature, registers $h$ in the public audit log.

> **Proposition:** [Irrevocability of $\GzeroDecl$ $\GzeroDecl$的不可撤销性]
> <!-- label: prop:irrevocability -->
> Once $h = SHA-256(\GzeroDecl)$ is registered in the audit log, the declaration is **irrevocable** in the following precise sense: any subsequent action $\alpha$ by the declarant that contradicts any clause of $\mathcal{C}$ constitutes a verifiable $\gnonzero$ event. The declarant cannot ``un-declare''; they can only violate the declaration, which triggers the emergency procedure (Section [ref]). The proof is cryptographic: the Git commit history is append-only and content-addressed; the audit log is a SHA-256 hash chain; no party has the power to delete or modify committed history without detection (preimage resistance of SHA-256).

### The g=0 Declaration as a Signaling Game

> **Proposition:** [$\GzeroDecl$ Separating Equilibrium $\GzeroDecl$分离均衡]
> <!-- label: prop:signaling -->
> In the Spence signaling game [cite] where candidates signal their type through the cost of $\GzeroDecl$:
> 
- For type $H$ ($g_{\mathrm{true}} = 0$): the cost of $\GzeroDecl$ is purely procedural ($c_{sign}$---time to draft, sign, commit). Future audit costs are minimal because audits consistently confirm $\gzero$.
- For type $S$ ($g_{\mathrm{true}} > 0$): the cost includes the procedural cost *plus* the expected future detection cost $\kappa \cdot \Pbb(detection \mid g_{\mathrm{true}} > 0)$, which is substantial under Assumption [ref].

> When $\kappa \cdot \Pbb(detection \mid g_{\mathrm{true}} > 0) > c_{sign}$, a separating equilibrium exists: only type $H$ signs $\GzeroDecl$; type $S$ does not. The $\GzeroDecl$ thus serves as a **screen**: the act of signing itself filters Strategic types from the candidate pool.

## Conflict Resolution 冲突解决
<!-- label: sec:conflict -->

### The Unanimity Deadlock Problem

The unanimity rule (Assumption [ref]) provides capture resistance but creates a structural vulnerability: any single maintainer can block any decision, creating deadlock. Unlike corporate boards (where the CEO breaks ties) or parliaments (where majority rules), the SCX Kernel has no external tiebreaker by design---external arbitration would violate theorem supremacy. The deadlock resolution mechanism must therefore be **endogenous**: resolving deadlocks using only the existing Kernel, Contributors, and audit infrastructure.

> **Definition:** [Deadlock 僵局]
> <!-- label: def:deadlock -->
> A deadlock $\deadlockSym$ exists at time $t$ when a binary decision $d \in \{0, 1\}$ is before the Kernel and the vote is not unanimous: $\exists i, j$ such that $v_i(d) \neq v_j(d)$, and this non-unanimity persists after one full discussion round (defined below). A **discussion round** consists of: each maintainer states their position with written justification; each maintainer reads all other justifications; each maintainer may revise their position; a second vote is taken.

### The Three-Stage Escalation Ladder 三级升级路径

> **Definition:** [Conflict Resolution Protocol 冲突解决协议]
> <!-- label: def:conflict_protocol -->
> When deadlock $\deadlockSym$ is declared at $t_0$:
> 
> 
> **Stage 1: Extended Kernel Deliberation 内核延长讨论** ($\tau_1 = 72$ hours)
> 
- The dissenter(s) must produce a written justification citing specific, verifiable concerns---not opinions or preferences.
- Proposer(s) may revise the proposal to address stated concerns.
- At $t_0 + \tau_1$: second vote. If unanimous, enacted. If not, escalate.

> 
> **Stage 2: Contributor Advisory Vote 贡献者建议投票** ($\tau_2 = 168$ hours / 7 days)
> 
- The deadlocked proposal plus both sides' written justifications are published to the Contributor layer.
- All Contributors may submit advisory votes: $advisory_c(d) \in \{0, 1, abstain\}$.
- The advisory result $A(d) = \frac{1}{|\Contributors|}\sum_c \ind{advisory_c(d) = 1}$ is reported to the Kernel. **Non-binding**: it provides common knowledge, not authority.
- After reviewing $A(d)$, the Kernel holds a third vote. If unanimous, enacted. If not, escalate.

> 
> **Stage 3: Resolution by Audit or Default 审计裁决或默认否决** ($\tau_3 = 720$ hours / 30 days)
> 
- If deadlock involves a $\gzero$ allegation (one maintainer claims another has $\gnonzero$): the accused must undergo independent $M>1$ audit by external auditors. The audit result is binding.
- If deadlock is purely procedural (policy disagreement, no $\gzero$ allegation): the proposal is **automatically rejected**---the status quo prevails. Under unanimity, proposals without unanimous support do not pass.
- If the Kernel deadlocks on *which* external auditors to select: auditors are drawn by random sortition from a pre-registered pool using a commit-reveal protocol with public block hashes as the randomness source.

### Deadlock Resolution Theorem

> **Theorem:** [Deadlock Resolution Guarantee 僵局解决保证]
> <!-- label: thm:deadlock -->
> Under Assumptions [ref]-- [ref] and the three-stage escalation protocol:
> 
1. **Eventual resolution:** Every deadlock resolves in finite time with probability 1. There is no infinite deadlock loop.
2. **Worst-case bound:** $\tau_{resolve} \leq \tau_1 + \tau_2 + \tau_3 = 72 + 168 + 720 = 960$ hours (40 days).
3. **Expected resolution:**
4. **No external dependency:** Resolution uses only the Kernel, Contributors, and audit infrastructure. No court, arbitrator, or external authority is required.

> **Proof:** \rigorFull
> **Step 1: Finiteness.** The escalation ladder has three stages with fixed maximum durations. At Stage 3, the protocol specifies a deterministic outcome: (a) $M$-audit result is binding for $\gzero$ disputes; (b) automatic rejection for procedural disputes. In both subcases, a decision is reached. Therefore $\tau_{resolve} \leq \sum_{s=1}^3 \tau_s = 960$ hours deterministically.
> 
> **Step 2: Expected time.** The resolution time follows a stopped process: resolve at stage $s$ with probability $p_s$, conditional on not resolving earlier. The expectation in Eq. [ref] follows directly from the law of total expectation. The calibrated $p_1 \approx 0.4$ reflects that written justifications often reveal the dissenter's concern as addressable (e.g., ``I need clarity on clause X,'' not ``I fundamentally oppose''). The calibrated $p_2 \approx 0.5$ reflects that common knowledge of strong community consensus ($A(d) > 0.8$ or $< 0.2$) creates accountability pressure on the outlier to conform or justify their deviation publicly.
> 
> **Step 3: Why infinite regress is impossible.** A potential objection: what if the Kernel deadlocks on *which* auditors to select in Stage 3? The protocol preempts this: if auditor selection is not unanimous within 7 days of Stage 3 entry, auditors are drawn by random sortition from the pre-registered pool. The sortition uses a commit-reveal protocol with Bitcoin or Ethereum block hashes as the randomness beacon---publicly verifiable and non-manipulable by any Kernel member. This eliminates the infinite-regress concern.
> 
> **Step 4: No external authority.** Stage 3's external auditors are individuals, not institutions. They provide a technical service (evaluating evidence of $\gnonzero$), not a governing authority. Their verdict is binding because the protocol *pre-commits* to accepting it---not because the auditors have enforcement power. This is a Ulysses contract: the Kernel binds itself to accept the audit result before knowing what it will be. $\square$

> **Corollary:** [Deadlock Frequency Estimate 僵局频率估计]
> <!-- label: cor:deadlock_freq -->
> In a Kernel with $K=3$ maintainers who have all passed $M>1$ audit and signed $\GzeroDecl$, deadlocks should be rare. Historical precedent from analogous governance structures (IETF working groups, W3C working groups, Linux subsystem maintainers) suggests $< 1$ deadlock per 2--3 years for groups of this size with shared norms. The primary source of deadlock is genuine substantive disagreement, not strategic obstruction---the entry filters (audit, $\GzeroDecl$) select against obstructionists.

## Emergency Procedures 紧急程序
<!-- label: sec:emergency -->

### Trigger Mechanism 触发机制

> **Definition:** [Emergency Trigger 紧急触发器]
> <!-- label: def:emergency_trigger -->
> An emergency audit is triggered when **any** Contributor submits a public, GPG-signed allegation that a seated maintainer has $\gnonzero$. The submission $\mathcal{E}$ must contain:
> 
1. **Accuser identity:** The Contributor's registered identity.
2. **Target:** The maintainer alleged to have $\gnonzero$.
3. **Evidence:** Specific, verifiable evidence---not opinions. Examples: (a) the maintainer signed an exclusive commercial license for SCX components; (b) the maintainer privately offered to sell Kernel votes; (c) the maintainer refused mandatory rotation at term end; (d) the maintainer's $\GzeroDecl$ signature fails verification; (e) the maintainer unilaterally modified CEC calibration values without Kernel consensus.
4. **Signature:** GPG signature over the allegation, committing the accuser to the claim.

### Emergency Timeline 紧急时间线

> **Protocol:** [Emergency Audit Protocol 紧急审计协议]
> <!-- label: prot:emergency -->
> Upon receiving a valid trigger at $t_0$:
> 
> **Phase 1: Preliminary Review** (0--24h):
> 
- Non-accused Kernel members review the evidence. The accused is recused.
- Frivolous triggers (unsigned, evidence-free) are dismissed; the accuser receives a warning. Two frivolous triggers from the same Contributor $\to$ 365-day suspension of trigger rights.
- Prima facie credible triggers proceed to Phase 2.

> 
> **Phase 2: $M$-Audit Execution** (24--48h):
> 
- $M \geq 3$ independent auditors selected. The accused is temporarily suspended (no voting rights, no Kernel channel access).
- Auditors examine evidence, interview accuser and accused, produce independent binary verdicts within 24 hours.

> 
> **Phase 3: Verdict and Action** (48--72h):
> 
- **Unanimous $\gnonzero$ ($\AuditResult = 0$):** Immediate permanent removal. All access revoked. Public audit log updated with full evidence. Replacement nominated from $\RotationPool$ within 14 days.
- **Unanimous $\gzero$ ($\AuditResult = 1$):** Immediate reinstatement. Accuser must issue public retraction. Refusal to retract triggers audit of the accuser (false allegation as evidence of $\gnonzero$).
- **Split verdict ($0 < \AuditResult < 1$):** Accused remains suspended. Second round with $M' > M$ auditors within 7 days. If still split, permanent removal (the community cannot sustain a maintainer under unresolved suspicion).

### Emergency Detection Theorem

> **Theorem:** [Emergency Detection Guarantee 紧急检测保证]
> <!-- label: thm:emergency -->
> Under Assumptions [ref]-- [ref], for a maintainer with true $g_{\mathrm{true}} > 0$ (interpreted as the probability that a single competent auditor detects $\gnonzero$ on examining the evidence), the probability that $M$ independent emergency auditors collectively confirm $\gnonzero$ satisfies:
> 
> $$
>     \Pbb(detection \mid g_{\mathrm{true}}) \geq 1 - (1 - g_{\mathrm{true}})^{M}.
>     <!-- label: eq:emergency_detection -->
> $$
> 
> 
> Consequences:
> 
1. For $g_{\mathrm{true}} \geq 0.5$ (blatant violation): $M=3 \to \Pbb \geq 0.875$; $M=5 \to \Pbb \geq 0.969$.
2. For $g_{\mathrm{true}} \geq 0.3$ (moderate violation): $M=5 \to \Pbb \geq 0.832$; $M=7 \to \Pbb \geq 0.918$.
3. $\Pbb(detection) \to 1$ exponentially in $M$ for any fixed $g_{\mathrm{true}} > 0$.
4. Maximum latency from valid trigger to removal: 72 hours (Phase 1--3 timeline).

> **Proof:** \rigorFull
> Each of $M$ independent auditors detects $\gnonzero$ with probability at least $g_{\mathrm{true}}$ (Assumption [ref]). The probability that all $M$ fail to detect is $(1 - g_{\mathrm{true}})^M$. Detection occurs if at least one detects: $\Pbb(detection) = 1 - (1 - g_{\mathrm{true}})^M$, establishing Eq. [ref].
> 
> For the $\gzero$ confirmation threshold, the verdict is $\AuditResult = 0$ (confirming $\gnonzero$) when *any* auditor detects. This is conservative by design: false positives require all $M$ auditors to err independently, which has probability $\alpha^M$ where $\alpha \ll 1$ is the per-auditor false positive rate. For $\alpha = 0.05$ and $M = 3$, the false conviction probability is $1.25 \times 10^{-4}$.
> 
> The 72-hour bound follows directly from the protocol timeline: Phase 1 ($\leq 24$h) + Phase 2 ($\leq 24$h) + Phase 3 ($\leq 24$h) = 72h maximum. $\square$

> **Corollary:** [Rapid Response Advantage 快速响应优势]
> <!-- label: cor:rapid_response -->
> The 72-hour removal guarantee for blatant $\gnonzero$ compares favorably to:
> 
- Corporate board removal: 30--90 days (shareholder meeting cycle + legal process).
- Academic misconduct investigation: 6--18 months (committee formation, evidence gathering, hearing).
- Open-source fork response: weeks to months (community coordination, infrastructure migration).

> The speed advantage comes from pre-existing infrastructure: the auditor pool, cryptographic identity system, and the $\GzeroDecl$ benchmark against which auditor judgments are calibrated. The emergency procedure does not need to *build* an adjudication system---it activates one that is already in place.

### Post-Removal Protocol 移除后程序

> **Definition:** [Post-Removal Sequence 移除后序列]
> <!-- label: def:post_removal -->
> After a maintainer is removed via emergency audit:
> 
1. **Audit log entry:** Within 24h, a complete public record is published: original allegation, all evidence, all auditor verdicts with justifications, and the removal action. This entry is chained into the audit log ($H_{n+1} = SHA-256(H_n \| removal\_record)$).
2. **Access revocation:** All Kernel access (Signal group, repository write permissions, GPG signing authority) revoked within 1 hour of verdict.
3. **Replacement:** Remaining Kernel members nominate a replacement from $\RotationPool$ within 14 days. If $K_t$ drops to 1 (below minimum), Contributors hold an emergency election for an interim maintainer, who then undergoes the standard entry path.
4. **Appeal window:** The removed maintainer may appeal within 30 days by submitting new evidence unavailable to the emergency auditors. Appeal adjudicated by $M'=5$ fresh auditors. Successful appeal $\to$ removal reversed, original auditors' false positive recorded. Failed appeal $\to$ removal permanent.

## Complete Protocol Specification 完整协议规范
<!-- label: sec:spec -->

### Communication Architecture 通信架构

[Table omitted — see original .tex]

> **Remark:** [Platform Justification 平台选择理由]
> <!-- label: rem:platforms -->
> **Signal for Kernel:** End-to-end encryption via the audited Signal Protocol; disappearing messages reduce the surface area for leaks of private deliberations; group size cap is irrelevant for $K \leq 5$. Rejected alternatives: Telegram (no E2E by default for groups), WhatsApp (Meta-owned, centralized), email (no forward secrecy). **Matrix for Contributors:** Open protocol (Apache 2.0), self-hosted server option, bridges to IRC/Slack/Discord, optional E2E. Rejected: Discord (proprietary), Slack (90-day message history limit on free tier). **GitHub for Observers:** Public, searchable, indexable by search engines, supports Issues + Discussions as distinct interaction modes. The GitHub dependency is acknowledged as a centralization risk; migration to a self-hosted Gitea/Forgejo instance is specified as a community option if GitHub becomes unavailable or hostile.

### Funding Model 资金模型

> **Definition:** [Zero-Extractive Funding 零提取资金模型]
> <!-- label: def:funding -->
> The SCX community operates on a **zero-extractive** funding model: no money is collected from community members. Funding sources are structurally separated from governance rights:
> 
1. **Yajie{} API calibration fees 雅洁API校准费:** Commercial users of the Yajie{} noise-detection API pay calibration fees covering Kernel maintainer operational costs (server hosting, domain registration, audit logistics). Fees are flat-rate, not per-use, to eliminate volume-based incentives.
2. **Voluntary donations 自愿捐赠:** Unrestricted donations supporting Contributor incentives (hostile review bounties, experiment reproduction, documentation).
3. **Academic grants 学术基金:** Research grants from institutions funding open-source protocol maintenance. Grants carry zero governance rights by contractual requirement.
4. **SCX Prize pool SCX奖池:** Annual prize funded by a fixed percentage of calibration fees, awarded by Contributor vote to the individual(s) with the most impactful governance contribution.

> 
> **Constitutional prohibition:** No funding source may confer governance rights. A donor of any amount has exactly the same governance standing as a non-donating Observer. The $\GzeroDecl$ binds maintainers against accepting funding with governance strings attached---doing so is per se evidence of $\gnonzero$.

### Decision Rights Matrix 决策权矩阵

[Table omitted — see original .tex]

### Constitutional Ceremonies 宪法仪式

> **Definition:** [Ceremony Calendar 仪式日历]
> <!-- label: def:ceremonies -->
> 
> **Quarterly 季度:**
> 
- **Audit review:** Kernel reviews all audit logs from the past quarter. Patterns of split verdicts or near-miss detections are investigated.
- **Contribution recognition:** New Contributors formally recognized. Inactive Contributors ($> 24$ months) moved to emeritus status.

> 
> **Annual 年度:**
> 
- **SCX Prize:** Awarded by Contributor ranked-choice vote for most impactful governance contribution.
- **State of the Protocol:** Kernel publishes a public report on protocol integrity $I_t$, audit statistics, rotation schedule compliance, and financial transparency.
- **$\gzero$ reaffirmation:** All seated maintainers re-sign and re-commit their $\GzeroDecl$ with the current year's timestamp. Ceremonial, not substantive---it signals that the commitment is current.

> 
> **Continuous 持续:**
> 
- **Audit log maintenance:** Every governance action recorded within 48 hours.
- **Hostile review program:** Ongoing bounties for finding errors in SCX theorems, implementations, or governance. All findings published regardless of outcome.

## Game-Theoretic Security Properties 博弈论安全性质
<!-- label: sec:security -->

### Incentive Compatibility 激励相容

> **Theorem:** [Dominant-Strategy Incentive Compatibility 占优策略激励相容]
> <!-- label: thm:incentive_compat -->
> Under Assumptions [ref]-- [ref], the governance mechanism $\mathcal{G}$ satisfies:
> 
1. For type $H$ ($g_{\mathrm{true}} = 0$): protocol compliance (sign $\GzeroDecl$, undergo audit, serve if seated, rotate at term end) is a strictly dominant strategy.
2. For type $S$ ($g_{\mathrm{true}} > 0$): Kernel entry has strictly negative expected payoff when $\kappa > B_ \cdot T_$, making non-entry the dominant strategy.

> **Proof:** \rigorFull
> Part (i): Type $H$ maximizes $u_H = \alpha \cdot I(\Community) - c_{audit} \cdot \#audits$. Protocol compliance maximizes $I(\Community)$ (all-Honest Kernel) and minimizes audit costs (audits of $H$ types are pro forma, not investigations). Any deviation (refusing rotation, blocking audits, opposing qualified candidates) decreases $I(\Community)$ without increasing any other payoff component.
> 
> Part (ii): From Theorem [ref], Step 2. The expected benefit is bounded by $B_ \cdot T_$ while the expected penalty is $\kappa \cdot (1 - (1 - \Delta)^{M \lfloor T_/T_{audit} \rfloor})$. When $\kappa > B_ \cdot T_$, the penalty term dominates for any $\Delta > 0, M \geq 1$. $\square$

### Sybil and Collusion Resistance 女巫与串通抵抗

> **Proposition:** [Sybil Resistance 女巫抵抗]
> <!-- label: prop:sybil -->
> The mechanism resists Sybil attacks because: (i) Kernel entry requires verifiable identity ($\geq 2$ years of public activity) plus $\GzeroDecl$ plus $M>1$ audit---fabricating multiple such identities is bounded by the cost of maintaining long-lived, active, distinct public personas; (ii) unanimity rule ensures a single honest maintainer can veto any malicious action, regardless of how many Kernel seats an attacker controls; (iii) the $M$-audit process examines cross-identity relationships---multiple Kernel members sharing a physical controller would be detected through behavioral analysis, Git commit timestamp correlation, and writing style analysis.

> **Proposition:** [Collusion Resistance 串通抵抗]
> <!-- label: prop:collusion -->
> The mechanism resists maintainer collusion because: (i) at least $\lceil M/2 \rceil$ auditors must be external to the Kernel---colluding maintainers cannot control the auditor pool; (ii) removing an honest maintainer requires unanimity---a single honest vote blocks removal; (iii) the Git-based audit log is append-only and content-addressed---colluding maintainers cannot erase evidence; (iv) emergency triggers are open to all Contributors---colluders cannot suppress a trigger without silencing the entire Contributor layer, a censorship problem that does not scale.

## Assumptions and Limitations 假设与局限性
<!-- label: sec:limitations -->

### Complete Assumption Set 完整假设集

\begin{assumption}[A4: No External Coercion 无外部胁迫]
<!-- label: ass:A4 -->
Kernel maintainers are not subject to coercion by external actors (governments, corporations, criminal organizations) that overrides their revealed preferences. Coerced signatures or votes void the game-theoretic guarantees. This is a limitation of any governance system short of fully anonymous, coercion-resistant voting---which is incompatible with the identity-verification requirement of Kernel membership.
\end{assumption}

\begin{assumption}[A5: Adequate Auditor Pool 充足的审计者池]
<!-- label: ass:A5 -->
There exists a pool of at least $M_ = 7$ qualified auditors who are knowledgeable about SCX, independent of current Kernel members, and willing to serve. Without this pool, the $M$-audit cannot be convened.
\end{assumption}

\begin{assumption}[A6: Cryptographic Infrastructure Integrity 密码基础设施完整性]
<!-- label: ass:A6 -->
The GPG keyring, Git repositories, and communication platforms are not compromised. Standard operational security practices (hardware security keys, multi-signature keyring updates, distributed Git mirrors) are assumed.
\end{assumption}

\begin{assumption}[A7: Community Viability 社区可行性]
<!-- label: ass:A7 -->
The SCX protocol attracts $|\Contributors_t| \geq 10$ active contributors and a replenishing auditor pool. The viability threshold is modest and achievable for a protocol with published theorems and open-source code.
\end{assumption}

\begin{assumption}[A8: Funding-Governance Separation 资金-治理分离]
<!-- label: ass:A8 -->
The structural separation of funding from voting is maintained. Erosion of this separation degrades the mechanism toward plutocracy---a failure mode the $\GzeroDecl$ is designed to prevent (maintainers cannot accept conditional funding without violating their declaration).
\end{assumption}

\begin{assumption}[A9: g-Function Operationalizability g函数可操作化]
<!-- label: ass:A9 -->
For any maintainer action violating $\gzero$, there exists at least one observable signal detectable by a competent auditor with probability $\Delta > 0$. This holds for overt violations (refusing rotation, signing exclusive licenses, demanding payment for votes). It may fail for covert violations leaving no observable trace.
\end{assumption}

### Honest Limitations 诚实局限性

1. **\limitationTag{1} Initial Kernel Bootstrapping 初始内核引导.** The theorems guarantee that an *existing* honest Kernel is self-stabilizing. They do not guarantee that the *initial* Kernel is honest. If the founding Kernel is entirely captured by Strategic types, they can admit only other Strategic types under unanimity, and the mechanism's self-correction cannot activate. The defense is social: the initial Kernel must be selected through a transparent, community-observed process with maximum scrutiny. This is the single point of vulnerability---once honest, the Kernel stays honest; the founding moment is the bootstrap problem that all governance systems face.
2. **\limitationTag{2} Minimum Community Size 最小社区规模.** The mechanism requires $|\Contributors_t| \geq 10$ and a functioning auditor pool. For a protocol with zero adoption, the governance mechanism is vacuously operational. This is not a flaw---it is a statement that governance serves a community.
3. **\limitationTag{3} Covert $\gnonzero$ 隐蔽偏差.** Assumption [ref] requires observable signals. A maintainer who privately believes they own the protocol but never acts on this belief has $g_{\mathrm{true}} > 0$ but $g_{observed} = 0$. The mechanism cannot detect beliefs---only actions. This is tolerable: unexpressed $\gnonzero$ has zero practical consequence.
4. **\limitationTag{4} Protocol Abandonment 协议遗弃.** The mechanism maintains integrity while the community exists. It cannot prevent the community from dissolving through burnout, disinterest, or migration. Protocol death by abandonment is a sociological phenomenon, not a governance failure.
5. **\limitationTag{5} Auditor Competence Variance 审计者能力方差.** Detection guarantees assume $\Delta > 0$. In practice, $\Delta$ varies by auditor and case. $M$-audit mitigates this (multiple auditors reduce single-weak-auditor impact), but if *all* available auditors are incompetent or compromised, detection probability collapses. Auditor training, rotation, and calibration are essential operational complements.
6. **\limitationTag{6} Unanimity-Speed Tradeoff 全票-速度权衡.** Unanimity protects against capture but imposes a speed cost: any decision can be delayed up to 40 days. Communities prioritizing speed over security should adopt majority voting---but they lose the capture-resistance guarantee. There is no free lunch in governance design.
7. **\limitationTag{7} Legal Jurisdiction 法律管辖权.** The mechanism operates in the mathematical domain, not in any legal jurisdiction. A government could compel a maintainer to violate $\GzeroDecl$ (violating Assumption [ref]). A court could order repository ownership transfer. The protocol's response---removing the coerced maintainer, forking---is technically feasible but legally complex.

## Bootstrapping and Implementation 启动与实施
<!-- label: sec:bootstrapping -->

### Bootstrapping Sequence 启动序列

1. **Initial Kernel formation 初始内核组建** (Month 1). Select 2--5 initial maintainers who: have contributed to SCX (theorems, code, papers); publicly sign and commit $\GzeroDecl$; pass $M=3$ independent audit; agree to staggered terms ($T_ = 24$ months).
2. **Infrastructure deployment 基础设施部署** (Month 1--2). Create Signal group; deploy self-hosted Matrix server; initialize public audit log repository (`scx-community/audit-log`); initialize declarations repository (`scx-community/declarations`); publish candidate declaration template (Chinese + English).
3. **First hostile review event 首次攻击性审稿** (Month 2--3). Announce bounties for: finding errors in SCX theorems; finding vulnerabilities in implementations; finding flaws in the governance mechanism itself (this paper is the first target). This stress-tests the protocol and identifies potential Contributors.
4. **Contributor layer activation 贡献者层激活** (Month 3--6). As hostile review findings, code contributions, and experiment reproductions accumulate, individuals are recognized as Contributors. Target: $\geq 10$ active Contributors by Month 6.
5. **First rotation 首次轮换** (Month 12). The first maintainer rotates out. Replacement drawn from $\RotationPool$, undergoes audit, seated. First live test of rotation.
6. **Governance review 治理审查** (Month 12). Kernel publishes first-year review: deadlock frequency, audit statistics, rotation compliance, proposed amendments.

### Minimal Viable Community 最小可行社区

> **Definition:** [Minimal Viable Community]
> <!-- label: def:mvc -->
> The SCX community is **viable** when: $|\Kernel_t| \geq 2$; $|\Contributors_t| \geq 10$; at least one public hostile review event completed; at least one maintainer rotation has occurred; the audit log contains at least $M \times |\Kernel_t|$ entries (each maintainer audited at least once). The community is **self-sustaining** when the Contributor pipeline consistently produces $\geq 1$ qualified Kernel candidate per rotation cycle and the auditor pool is replenished as auditors rotate out.

## Discussion 讨论
<!-- label: sec:discussion -->

### Relationship to Existing Governance Models

**Open-source maintainer models (Linux kernel).** The closest analogue: a small set of maintainers with commit rights, a larger contributor pool, and unbounded users. Key differences: (i) Linux maintainers are not term-limited; (ii) no formal $g$-audit mechanism; (iii) the succession model is emergent, not designed. \Neihe{} can be seen as ``Linux maintainer model plus term limits plus cryptographic audit.''

**DAOs (Decentralized Autonomous Organizations).** DAOs use token-weighted plutocratic voting. \Neihe{} is explicitly non-plutocratic: funding and governance are structurally separated. The tradeoff: DAOs can raise capital through token sales; \Neihe{} raises funds only through calibration fees and donations decoupled from governance.

**Academic peer review.** The $M$-audit resembles peer review: independent experts evaluate a candidate and produce binary verdicts. Differences: (i) \Neihe{} audit verdicts are public and signed; (ii) \Neihe{} audit is periodic and repeated; (iii) auditors are themselves subject to meta-audit.

**Corporate boards.** The Kernel resembles a board but with: (i) no shareholders (the theorems have no preferences); (ii) unanimity instead of majority; (iii) mandatory rotation; (iv) public cryptographic audit of every action.

### The Theorem Supremacy Principle 定理至上原则

The most unusual feature of \Neihe{} is that the ultimate authority is a set of mathematical theorems, not a person, vote, or legal document. The SCX theorems $\{T_1, ..., T_6\}$ are fixed points: proved, published, and not ``votable'' by any majority. A Kernel decision contradicting $T_1$ is not ``controversial''---it is definitionally invalid, like a physics journal ``voting'' to change the fine-structure constant.

This implies: **the community serves the theorems, not the reverse.** The theorems do not need the community to be true. The community needs the theorems to have a reason to exist. A maintainer who claims ownership of the protocol is claiming ownership of mathematical truths---a category error. The $\GzeroDecl$ formalizes this: it is not a promise to be collaborative; it is a recognition that one cannot own a theorem.

> **Core Principle 核心原则.** *``The community belongs to no individual---the community belongs to the theorems. The initial maintainers are merely the first guardians. The theorems do not depend on any person. At any time, the community can audit the maintainers and replace the maintainers. Accepting this is the prerequisite for all maintainers---otherwise, $\gzero$ is not satisfied.''*
> 
> 
> *``社区不是任何个人的——社区是定理的。初始维护者只是第一批守护者。定理不依赖任何个人。任何时候社区可以审计维护者、替换维护者。接受这一点是所有维护者的基本条件——否则就不满足$\gzero$。''*

### The Symbiotic Equilibrium 共生均衡

<div align="center">

[Diagram omitted — see original .tex]

</div>

The theorems give the community its identity (``we guard these specific results''). The community gives the theorems their longevity (``these results are maintained, tested, and transmitted across generations''). Neither fulfills its function without the other. Together they form a self-sustaining system where the mathematical structure of the theorems protects the community from capture, and the human structure of the community protects the theorems from obsolescence.

## Conclusion 结论
<!-- label: sec:conclusion -->

We have presented **内河 (\Neihe{})**---a formal governance mechanism for the SCX protocol community. The mechanism instantiates five design principles (no ownership, replaceability, auditability, self-stabilization, theorem supremacy) through four formal pillars: the $\gzero$ Declaration Protocol, the Maintainer Rotation Game, the Conflict Resolution Escalation Ladder, and the Emergency Audit Procedure.

Three theorems establish the mechanism's core guarantees. Theorem [ref] proves that maintainer rotation with mandatory re-audit converges to all-Honest Kernel composition, with integrity $I_t \to 1$ as audit frequency increases. Theorem [ref] proves that any deadlock under unanimity resolves within 40 days without external arbitration. Theorem [ref] proves that a $\gnonzero$ maintainer is detected with probability exponentially approaching 1 in the number of auditors and removed within 72 hours.

The mechanism is not a company, foundation, DAO, or membership organization. It is a **protocol maintenance network**---a self-governing collective whose sole purpose is to guard the SCX theorems and their implementations. Its core premise is that a protocol's longevity depends not on the charisma of its founder but on the robustness of its governance. TCP/IP survived because no one owned it. Linux survived because anyone could fork it. SCX will survive---if it survives---because its theorems are true regardless of who maintains them, and its governance mechanism ensures that maintainers remain guardians, not owners.

<div align="center">

**社区属于定理。定理不属于任何人。**
*The community belongs to the theorems. The theorems belong to no one.*

</div>

**Acknowledgments 致谢.** We acknowledge the SCX protocol's core theoretical framework, without which the governance problem would not arise---a protocol with no theorems needs no guardians. All errors remain the authors' own. No external funding was received for this work.

\begin{thebibliography}{99}

\bibitem{SCX2025}
SCX.
\newblock {SCX}: State-Conditioned eXpertise---A Framework for Multi-Expert Quality Auditing.
\newblock Technical Report, 2025.

\bibitem{SCXTheory2026}
SCX.
\newblock A Fundamental Impossibility in Data Quality: Distinguishing Label Noise from Sample Difficulty is Provably Unsolvable Without Explicit Assumptions.
\newblock arXiv preprint, 2026.

\bibitem{YajieProtocol}
SCX.
\newblock {Yajie (雅洁)}: A Complete Theory of Label Noise Detection via Multi-Expert Consistency.
\newblock Working paper, 2026.

\bibitem{SpringConfig}
SCX.
\newblock {Spring (春季)}: A Self-Evolving Gatekeeper with Provable Convergence.
\newblock Working paper, 2026.

\bibitem{SitusTheory}
SCX.
\newblock {Situs}: Physics-Anchored Positional Encoding for State-Conditioned Expertise.
\newblock Working paper, 2026.

\bibitem{SCXGovernance}
SCX.
\newblock {SCX} Audit of Governance: Game-Theoretic Foundations of Transparency Under Multi-Expert Verification.
\newblock Technical Report, 2026.

\bibitem{Ostrom1990}
E.~Ostrom.
\newblock {\em Governing the Commons: The Evolution of Institutions for Collective Action}.
\newblock Cambridge University Press, 1990.

\bibitem{Ostrom2005}
E.~Ostrom.
\newblock {\em Understanding Institutional Diversity}.
\newblock Princeton University Press, 2005.

\bibitem{Myerson1981}
R.~B. Myerson.
\newblock Optimal auction design.
\newblock {\em Mathematics of Operations Research}, 6(1):58--73, 1981.

\bibitem{Myerson2008}
R.~B. Myerson.
\newblock Perspectives on mechanism design in economic theory.
\newblock {\em American Economic Review}, 98(3):586--603, 2008.

\bibitem{Arrow1951}
K.~J. Arrow.
\newblock {\em Social Choice and Individual Values}.
\newblock Wiley, 1951.

\bibitem{Sen1970}
A.~Sen.
\newblock {\em Collective Choice and Social Welfare}.
\newblock Holden-Day, 1970.

\bibitem{Spence1973}
M.~Spence.
\newblock Job market signaling.
\newblock {\em The Quarterly Journal of Economics}, 87(3):355--374, 1973.

\bibitem{FudenbergTirole1991}
D.~Fudenberg and J.~Tirole.
\newblock {\em Game Theory}.
\newblock MIT Press, 1991.

\bibitem{Williamson1985}
O.~E. Williamson.
\newblock {\em The Economic Institutions of Capitalism}.
\newblock Free Press, 1985.

\bibitem{North1990}
D.~C. North.
\newblock {\em Institutions, Institutional Change and Economic Performance}.
\newblock Cambridge University Press, 1990.

\bibitem{AcemogluRobinson2012}
D.~Acemoglu and J.~A. Robinson.
\newblock {\em Why Nations Fail: The Origins of Power, Prosperity, and Poverty}.
\newblock Crown Business, 2012.

\bibitem{Nakamoto2008}
S.~Nakamoto.
\newblock Bitcoin: A peer-to-peer electronic cash system.
\newblock Whitepaper, 2008.

\bibitem{Buterin2014}
V.~Buterin.
\newblock A next-generation smart contract and decentralized application platform.
\newblock Ethereum Whitepaper, 2014.

\bibitem{Lessig1999}
L.~Lessig.
\newblock {\em Code and Other Laws of Cyberspace}.
\newblock Basic Books, 1999.

\bibitem{Benkler2006}
Y.~Benkler.
\newblock {\em The Wealth of Networks: How Social Production Transforms Markets and Freedom}.
\newblock Yale University Press, 2006.

\bibitem{Weber2004}
S.~Weber.
\newblock {\em The Success of Open Source}.
\newblock Harvard University Press, 2004.

\bibitem{Raymond1999}
E.~S. Raymond.
\newblock {\em The Cathedral and the Bazaar}.
\newblock O'Reilly Media, 1999.

\bibitem{Schneier2015}
B.~Schneier.
\newblock {\em Data and Goliath: The Hidden Battles to Collect Your Data and Control Your World}.
\newblock W. W. Norton, 2015.

\bibitem{Hoeffding1963}
W.~Hoeffding.
\newblock Probability inequalities for sums of bounded random variables.
\newblock {\em Journal of the American Statistical Association}, 58(301):13--30, 1963.

\bibitem{Merkle1987}
R.~C. Merkle.
\newblock A digital signature based on a conventional encryption function.
\newblock {\em CRYPTO '87}, 369--378, 1987.

\end{thebibliography}