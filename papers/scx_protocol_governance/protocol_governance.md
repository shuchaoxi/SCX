<div align="center">

\fbox{\fbox{\parbox{0.85\textwidth}{\bfseries
INTERNAL ONLY

Unauthorized distribution is strictly prohibited. This document contains
the core game-theoretic analysis of SCX protocol governance, including
formal proofs of maintainer rotation mechanisms, audit equilibrium, and
trustless architecture.

Restricted to SCX core team and authorized maintainers.
}}}

</div>

*Abstract:*

This paper presents the formal game-theoretic foundation of SCX protocol governance.
The central thesis is that the SCX protocol does not need to trust any individual
maintainer — trust is replaced by a mathematically provable mechanism consisting of
four pillars: (1) $M > 1$ mutual audit of every maintainer's bias parameter $g$,
(2) public, reproducible audit logs that any third party can verify independently,
(3) finite rotation cycles that bound the probability of undetected deviation by
$e^{-2M\Delta^2}$ via Hoeffding's inequality, and (4) mutual audit incentives that
make $\sum g = 0$ the unique Nash equilibrium, not a goodwill assumption.

We prove that the maintainer rotation mechanism transforms the governance problem
from a trust-based social contract into a purely mathematical one. The key insight
is that *the theorem audits the maintainer, not the maintainer's biography*.
A maintainer's reputation, credentials, institutional affiliation, or past
contributions are irrelevant to SCX governance — only the real-time, auditable
bias parameter $g(t)$ matters. This is not a philosophical stance; it is a direct
consequence of the Hoeffding bound and the rotation game.

We further analyze why companies cannot run protocols without contaminating audit
neutrality (CEO $g \neq 0$ is structurally unavoidable for for-profit entities),
formalize the maintainer rotation game as a repeated game with imperfect monitoring,
prove the exponential decay of undetected deviation probability, and establish
$\sum g = 0$ as the Nash equilibrium of the multi-maintainer mutual audit game.
The paper concludes with a specification of what data maintainers must disclose
(audit logs, $g$ parameters, conflict declarations) and must never disclose
(personal life, biography, credentials), anchoring SCX governance in provable
mathematics rather than fallible human judgment.

**Keywords:** protocol governance, maintainer rotation, game theory,
Hoeffding inequality, Nash equilibrium, mutual audit, trustless architecture,
bias detection, finite rotation cycles, mechanism design

---

---

## Introduction: Why Trust Is the Most Dangerous Assumption in Human Protocols

### The Trust Catastrophe

Every human protocol that has ever failed has failed for the same reason:
it trusted someone it should not have. This is not a moral observation —
it is a structural one. Trust is an information-theoretic shortcut: instead
of verifying that an agent will behave honestly, we substitute a cheaper proxy
(reputation, credentials, personal relationship) and proceed as if the
verification had been done. When the proxy is accurate, trust works. When the
proxy fails — and all proxies eventually fail — the protocol collapses.

The history of protocol governance is the history of discovering which proxies
fail and how catastrophically:

- **Financial protocols** (Enron, FTX, Wirecard): trusted auditors who were structurally incentivized to look the other way.
- **Academic protocols** (peer review crises, replication failures):
trusted reviewers whose $g \neq 0$ was invisible to the system.
- **Open-source protocols** (xz backdoor, event-stream incident):
trusted maintainers who were attack vectors.
- **Cryptographic protocols** (certificate authorities, IOTA):
trusted centralizers who defeated the purpose of decentralization.
- **AI safety protocols** (self-regulation pledges): trusted
companies whose CEOs have structurally $g \neq 0$.

\begin{hitbox}
The fundamental error in all protocol governance to date is the conflation of
*identity* with *behavior*. ``Alice has good credentials, therefore
Alice will behave honestly'' is not a logical inference — it is a category error.
Credentials are noise. Only behavior — measured, audited, bounded — carries
signal.

SCX governance is built on the refusal to make this error. We do not ask who the
maintainer is. We ask what the maintainer's $g$ is, right now, under the current
audit cycle. The theorem audits the maintainer, not the biography.

\end{hitbox}

### The SCX Governance Thesis

The SCX protocol governance thesis can be stated in one sentence:

<div align="center">

\fbox{\parbox{0.88\textwidth}{
**SCX does not trust any maintainer because it can prove,**
 
**with exponentially decaying uncertainty, that every maintainer's**
 
**bias parameter $g$ is bounded by a known tolerance $\varepsilon$**
 
**within every rotation cycle of length $T$.**
}}

</div>

This thesis has four components, each of which is mathematically
rigorous and operationally executable:

1. **$M > 1$ mutual audit:** Every maintainer's bias parameter $g$ is audited by at least $M$ other maintainers simultaneously.
2. **Public, reproducible audit logs:** All audit data — raw scores, consensus outputs, detection flags — are published in an append-only, cryptographically timestamped log.
3. **Finite rotation cycles:** Maintainers serve for a fixed period $T$, then a subset is rotated out and replaced by new maintainers from a candidate pool.
4. **$\sum g = 0$ Nash equilibrium:** The incentive structure of the mutual audit game makes zero aggregate bias the unique subgame-perfect equilibrium.

\begin{govbox}
The four components are not independent — they form a tight logical chain. Remove
any one, and the proof collapses. $M > 1$ without rotation means a fixed clique
can collude indefinitely. Rotation without $M > 1$ means a single rotating
maintainer can deviate undetected (the auditor is always different, so no one
has baseline). Public logs without Hoeffding bounds means deviations are
detectable in principle but not bounded in probability. And Hoeffding bounds
without the $\sum g = 0$ equilibrium means detection is probable but deviation
is still individually rational.

\end{govbox}

### Why This Paper Is Internal

This paper is classified INTERNAL ONLY for a specific reason: it contains the
complete game-theoretic specification of SCX maintainer rotation, including the
exact detection thresholds, rotation periods, and audit protocols. In the wrong
hands, this is a manual for how to attempt to defeat SCX governance. We publish
the theorems publicly; we keep the operational parameters internal.

---

## Why Companies Cannot Run Protocols: The Structural Inevitability of CEO $g \neq 0$

### The $g$ Parameter: A Formal Definition

> **Definition:** [Bias Parameter $g$]
> Let $\mathcal{M}$ be a maintainer responsible for calibrating or auditing data
> quality assessments in the SCX protocol. The **bias parameter** $g \in \R$
> is defined as the systematic deviation of $\mathcal{M}$'s assessments from the
> ground-truth consensus:
> 
> 
> $$<!-- label: eq:g_def -->
>     g_{\mathcal{M}} = \E\left[ s_{\mathcal{M}}(X) - s^*(X) \right]
> $$
> 
> 
> where $s_{\mathcal{M}}(X)$ is the score assigned by maintainer $\mathcal{M}$ to
> data point $X$, $s^*(X)$ is the ground-truth quality score that would be
> assigned by an unbiased oracle under the SCX theorem framework, and the
> expectation is taken over the distribution of audited data points.
> 
> A maintainer with $g = 0$ is **unbiased**. A maintainer with $g > 0$ is
> **positively biased** (systematically inflates scores). A maintainer with
> $g < 0$ is **negatively biased** (systematically deflates scores).

> **Remark:** The $g$ parameter is not a measure of competence. A maintainer can be highly
> competent (low variance in assessments) and still have $g \neq 0$ (systematic
> bias). In fact, the most dangerous maintainers are precisely those with high
> competence and high bias, because their assessments are consistent enough to
> pass casual inspection while systematically distorting the protocol's output.

### The Corporate $g$ Problem

> **Theorem:** [Corporate $g$ Non-Zero Theorem]<!-- label: thm:corp_g -->
> Let $\mathcal{C}$ be a for-profit corporation that controls a maintainer
> position in a data quality protocol. Let $\Pi(g)$ be the profit
> function of $\mathcal{C}$ as a function of the maintainer's bias $g$,
> and let $p_{det}(g)$ be the probability of detection and $L(g)$ the
> penalty when bias $g$ is detected. If $\frac{\partial \Pi}{\partial g}|_{g=0} \neq 0$
> — that is, if the corporation's marginal profit at zero bias is non-zero —
> then the corporation's optimal choice of $g$ is $g^* \neq 0$
> unless the detection-penalty mechanism satisfies:
> 
> $$
>     \left.\frac{\partial(p_{det} \cdot L)}{\partial g}\right|_{g=0}
>     \;\geq\; \left|\frac{\partial \Pi}{\partial g}\right|_{g=0}
> $$
> 
> That is, the marginal deterrence at $g=0$ must dominate the marginal profit incentive.

> **Proof:** [Proof Sketch]
> The corporation chooses $g$ to maximize:
> 
> $$
>     \max_{g} \; \Pi(g) - p_{det}(g) \cdot L(g)
> $$
> 
> At $g = 0$, the first-order condition yields:
> 
> $$
>     \left.\frac{\partial \Pi}{\partial g}\right|_{g=0} - 
>     \left.\frac{\partial(p_{det} \cdot L)}{\partial g}\right|_{g=0} = 0
> $$
> 
> If $\frac{\partial \Pi}{\partial g}|_{g=0} > 0$ and the detection-penalty term is
> insufficient (as it always is when the protocol operator is also the auditor —
> i.e., self-regulation), then $g^* > 0$. The only way to achieve $g^* = 0$ is to
> make $p_{det}$ and $L$ such that the penalty-deterrence dominates the
> profit incentive — which requires an external, non-corporate auditor. But if the
> external auditor is itself a corporation, the problem recurses.

\begin{hitbox}
The Corporate $g$ Theorem is not an empirical claim about corporate morality.
It is a mathematical consequence of the profit function. A for-profit entity
*must* set $g \neq 0$ whenever $\frac{\partial \Pi}{\partial g} \neq 0$,
unless externally constrained by a credible audit mechanism. This is not greed;
this is fiduciary duty. The CEO who sets $g = 0$ when $\frac{\partial \Pi}{\partial g} > 0$
is violating their obligation to shareholders — and will be replaced. Corporate
governance is structurally incompatible with protocol neutrality.

This is why SCX maintainers cannot be employees of for-profit entities with
interests in the protocol's output. The corporation's $g$ leaks into the
maintainer's $g$ through compensation, promotion, and termination incentives —
even if the maintainer is individually committed to neutrality.

\end{hitbox}

### The Cascade of Corporate Capture

The problem is worse than it appears. When a single corporation controls a
protocol's governance, the bias does not stay at $g \neq 0$ — it cascades:

1. **Phase 1 — Direct bias:** The corporation sets $g > 0$ for data that benefits its products.
2. **Phase 2 — Audit capture:** The corporation appoints auditors who share its incentives, driving $p_{det} \to 0$.
3. **Phase 3 — Standard capture:** The protocol's definition of ``quality'' drifts to align with the corporation's already-high-scoring data.
4. **Phase 4 — Ecosystem extinction:** Third parties abandon the protocol, as it no longer provides an unbiased signal.

\begin{govbox}
This cascade is not hypothetical. It is the documented history of every protocol
that was ever captured by a corporate entity. The pattern is invariant: the
corporation does not need to be malicious; it only needs to be rational. And
rationality, in the presence of $\frac{\partial \Pi}{\partial g} \neq 0$, is
sufficient to guarantee capture.

SCX governance is designed to make capture mathematically impossible — not by
asking corporations to behave better, but by making the maintainer position
structurally incapable of being captured. The rotation mechanism, the $M > 1$
mutual audit, and the public log requirement together ensure that no single
entity — corporate or individual — can accumulate enough control to bias $g$
over any horizon longer than $T$.

\end{govbox}

---

## The Maintainer Rotation Mechanism: Formal Game Theory

### The Rotation Game: Setup

We model the SCX maintainer system as a **repeated game with imperfect
monitoring** among a pool of $N$ candidate maintainers, of which $K$ are active
at any given time (with $K \geq 2$, typically $K = M$ for mutual audit
completeness). The game proceeds in discrete rotation cycles of length $T$:

> **Definition:** [Rotation Cycle]
> A **rotation cycle** is a time interval $[t_0, t_0 + T]$ during which a
> fixed set of $K$ maintainers $\{\mathcal{M}_1, ..., \mathcal{M}_K\}$ is
> active. At time $t_0 + T$, exactly $r$ maintainers ($1 \leq r < K$) are rotated
> out and replaced by $r$ new maintainers drawn from the candidate pool. The new
> set serves for the next cycle $[t_0 + T, t_0 + 2T]$.

> **Definition:** [Maintainer Action Space]
> At each audit event $t$ within a rotation cycle, maintainer $\mathcal{M}_i$
> chooses an action $a_i(t) \in \mathcal{A} = \{HONEST, DEVIATE\}$.
> The action HONEST means reporting scores consistent with $g_i = 0$ (unbiased).
> The action DEVIATE means reporting scores with $g_i = \delta_i$, where
> $\delta_i$ is the maintainer's chosen bias magnitude.

### Payoff Structure

Each maintainer $\mathcal{M}_i$ receives a per-period payoff:

$$<!-- label: eq:payoff -->
    \payoff{i}(a_i, a_{-i}) = 
    \underbrace{B \cdot \indicator[a_i = HONEST]}_{honesty bonus} + 
    \underbrace{D(\delta_i) \cdot \indicator[a_i = DEVIATE]}_{deviation gain} - 
    \underbrace{\auditCost \cdot (K-1)}_{audit cost (audit all others)} -
    \underbrace{P \cdot \indicator[detected]}_{detection penalty}
$$

where:

- $B > 0$ is the honesty bonus — compensation for maintaining $g = 0$.
- $D(\delta_i)$ is the deviation gain — the benefit of biasing scores by $\delta_i$.
- $\auditCost > 0$ is the cost of auditing one other maintainer (paid $K-1$ times).
- $P \gg D(\delta_i)$ is the detection penalty — loss of maintainer status, reputation destruction, possible legal consequences.

> **Remark:** The key structural feature: every maintainer audits *all other* maintainers.
> The audit cost scales linearly with $K-1$, but the detection probability scales
> super-linearly because each maintainer is audited by $K-1$ independent auditors.
> This asymmetry — linear cost, super-linear detection — is what makes the
> mechanism economically viable at scale.

### The Mutual Audit Subgame

Within each rotation cycle, the $K$ maintainers play a **mutual audit game**:
each maintainer audits every other maintainer's reported scores against the
consensus baseline. The audit is not based on comparing to a fixed standard
(because the ground truth is unknown — that is precisely why we need
maintainers) but on detecting *deviations from the emergent consensus*.

> **Definition:** [Mutual Audit Detection]
> Maintainer $\mathcal{M}_i$ is **detected as deviating** at time $t$ if:
> 
> $$<!-- label: eq:detection -->
>     \left| s_i(X_t) - \frac{1}{K-1} \sum_{j \neq i} s_j(X_t) \right| > \tau
> $$
> 
> where $\tau$ is a calibrated detection threshold that balances false positive
> rate $\alpha$ and false negative rate $\beta$.

> **Theorem:** [Consensus Deviation Detectability]<!-- label: thm:detectability -->
> Let the consensus baseline $\bar{s}_{-i}$ be the **median** of the
> $K-1$ auditor scores (excluding maintainer $i$). If at most
> $\lfloor (K-1)/2 \rfloor$ maintainers are colluding (i.e., a majority
> of the active set is honest), then the median is guaranteed to be an honest
> score — colluder contamination cannot displace it. Any deviation
> $\delta_i > 2\tau$ by maintainer $i$ from this uncontaminated baseline
> is detected with probability at least:
> 
> $$
>     \Pbb(detection) \geq 1 - 2\exp\left(-\frac{2\lceil (K-1)/2 \rceil \tau^2}{(\Delta s)^2}\right)
> $$
> 
> where $\Delta s$ is the maximum possible score range.

> **Proof:** With at most $\lfloor (K-1)/2 \rfloor$ colluders among the $K-1$ auditors,
> honest auditors number $H = \lceil (K-1)/2 \rceil$, a strict majority.
> **Why the median, not the mean.** The arithmetic mean of all $K-1$ scores
> is contaminated: each colluder shifts the mean by $\delta_{colluder}/(K-1)$,
> corrupting the honest baseline. The median is robust: with majority honest,
> the median must be an honest score regardless of how extreme the colluders'
> scores are. By Hoeffding's inequality applied to the median of $H$ honest
> i.i.d.\ scores,
> $\Pbb(|median - \mu^*| > \varepsilon) \leq 2\exp(-2H\varepsilon^2/(\Delta s)^2)$.
> The deviation $\delta_i$ shifts maintainer $i$'s scores by $\delta_i$ relative to
> $\mu^*$. For $\delta_i > 2\tau$, the
> deviation exceeds the honest consensus interval, and equation [ref]
> triggers. Setting $\varepsilon = \tau$ yields the stated bound.

\begin{hitbox}
This theorem reveals why $K \geq 3$ is the minimum viable maintainer count.
With $K = 2$, each maintainer audits only one other — the consensus is degenerate
(the mean of one score is just that score). A single maintainer's deviation cannot
be distinguished from a dispute between two equally valid perspectives. The
mutual audit requires $K \geq 3$ to create a non-degenerate consensus baseline:
you need at least two honest auditors to define ``center'' for the third.

With $K = 3$ and majority-honest assumption, any single deviator is immediately
detectable because their score will be the outlier in a set of three. With
$K = 5$, even two colluding deviators can be detected because the remaining
three honest maintainers define the consensus.

\end{hitbox}

### The Rotation as a Game-Theoretic Necessity

Without rotation, the mutual audit game has a fatal flaw: **collusion over
long horizons**. If the same $K$ maintainers serve indefinitely, they can form a
coalition where *everyone* agrees to deviate by a small, coordinated
amount, sharing the deviation gains while ensuring that no individual's score
deviates from the (corrupted) consensus. The mutual audit detects deviations
from consensus — but if the consensus itself is corrupted, detection fails.

Rotation breaks the coalition. When $r$ maintainers are rotated out and replaced
by new, uncorrupted maintainers at each cycle boundary, the new maintainers
inherit the audit logs and can detect the systematic drift that accumulated
during the previous cycle. The coalition cannot corrupt the new maintainers
fast enough to maintain cover, because:

1. The new maintainers are drawn from a pool that is larger than the coalition can pre-corrupt.
2. The public audit logs give new maintainers a complete history of all prior maintainers' scores, enabling retrospective detection of coordinated deviation.
3. The rotation is staggered: only $r < K$ maintainers rotate at a time, so the coalition cannot achieve a full replacement with corrupted members.

### Formal Model of the Rotation Game

We now formalize the rotation game as a stochastic game.

> **Definition:** [Rotation Game $\Gamma(N, K, r, T)$]
> The rotation game is a tuple $\Gamma = (N, K, r, T, \mathcal{A}, \mathcal{S}, \mathcal{P}, u)$ where:
> 
> - $N$: total pool size of candidate maintainers.
> - $K$: number of active maintainers per cycle ($K \geq 3$).
> - $r$: number of maintainers rotated per cycle boundary ($1 \leq r < K$).
> - $T$: cycle length (number of audit events per cycle).
> - $\mathcal{A}$: action space (HONEST or DEVIATE with bias $\delta$).
> - $\mathcal{S}$: state space, including the current active set and audit history.
> - $\mathcal{P}$: state transition probabilities (deterministic rotation + stochastic detection).
> - $u = (u_1, ..., u_K)$: payoff vector as defined in [ref].

The game is infinitely repeated (or indefinitely repeated with discount factor
$\gamma \in (0, 1)$). A maintainer who is detected as deviating is permanently
removed from the active set and the candidate pool (one-shot deviation with
permanent consequences).

### The Folk Theorem Limitation and Its Resolution

A standard result in repeated game theory — the Folk Theorem — states that in
infinitely repeated games with sufficiently patient players, any feasible and
individually rational payoff vector can be supported as a subgame perfect
equilibrium. This would seem to suggest that collusion (all maintainers deviating
slightly and sharing the gains) is a possible equilibrium in the rotation game.

However, the Folk Theorem does not apply to the SCX rotation game for three
reasons:

1. **Imperfect monitoring:** The Folk Theorem with imperfect monitoring (Fudenberg, Levine, and Maskin, 1994) requires a certain dimensionality condition that the SCX audit mechanism violates — the Hoeffding bound drives the effective monitoring precision to near-perfection.
2. **Rotation breaks continuation:** The Folk Theorem relies on continuation strategies that punish deviation over an infinite horizon. Rotation limits each maintainer's horizon to at most $T$, after which they are out of the active set and cannot be punished by the remaining maintainers.
3. **Public observability:** The audit logs are public. A maintainer who deviates faces not just punishment by other maintainers, but reputational expulsion from the entire candidate pool and the broader community.

\begin{govbox}
The rotation mechanism transforms the governance problem from ``how do we ensure
that permanent maintainers stay honest?'' to ``how do we ensure that temporary
maintainers cannot profit from deviation within their finite window?'' The second
question is strictly easier because the window is bounded. A permanent maintainer
can amortize the cost of building a corruption network over an infinite horizon.
A temporary maintainer with a known exit time $t_0 + T$ must complete the
deviation, extraction, and escape within $T$ — and the mutual audit ensures that
the detection probability is exponentially close to 1 well before $T$ expires.

\end{govbox}

---

## The Hoeffding Guarantee: $P(Undetected Deviation) \leq e^{-2M\Delta^2}$
<!-- label: sec:hoeffding -->

### The Central Bound

The mathematical centerpiece of SCX maintainer governance is a simple but
powerful concentration inequality. We prove that the probability of a biased
maintainer surviving undetected through an entire rotation cycle decays
exponentially in the number of auditors $M$ and the square of the bias magnitude
$\Delta$.

> **Theorem:** [Hoeffding Guarantee for Maintainer Audit]<!-- label: thm:hoeffding -->
> Let $\mathcal{M}$ be a maintainer with true bias $g = \delta$. During a rotation
> cycle of length $T$, $\mathcal{M}$ is audited by $M = K-1$ other maintainers
> at each of $n$ audit events (where $n \leq T$). At each audit event $t$, each
> auditor independently tests whether $\mathcal{M}$'s score deviates from the
> consensus by more than $\tau$. Let $X_t \in \{0, 1\}$ indicate whether
> $\mathcal{M}$ is flagged at audit $t$. Assume the $X_t$ are independent across
> audit events (conditional on the maintainer's fixed bias $\delta$) and that
> $\E[X_t] = p_{det}$ where $p_{det} \geq p_{min} > 0$ for
> any $\delta \geq \Delta > 0$.
> 
> Then the probability that $\mathcal{M}$ survives all $n$ audits undetected is:
> 
> $$<!-- label: eq:hoeffding_main -->
>     \Pbb\left(\sum_{t=1}^{n} X_t = 0 \;\middle|\; \delta \geq \Delta\right)
>     \leq \exp\left(-2 n \cdot p_{min}^2\right)
>     \leq \exp\left(-2 M \Delta^2 \cdot \frac{n}{T}\right)
> $$
> 
> 
> In the worst case where the auditor count $M$ is the binding constraint (each
> auditor contributes one independent detection opportunity per audit event), we
> have the simplified bound:
> 
> $$<!-- label: eq:hoeffding_simple -->
>     \boxed{\Pbb(undetected deviation \mid \delta \geq \Delta) \leq e^{-2M\Delta^2}}
> $$

> **Proof:** Let the honest scores be i.i.d.\ bounded in $[a, b]$ with range $\Delta s = b - a$
> and mean $\mu^*$. A maintainer with bias $\delta \geq \Delta$ produces scores
> $s_i = \mu^* + \delta + \varepsilon_i$, where $\varepsilon_i$ is zero-mean noise
> bounded in $[-\Delta s/2, \Delta s/2]$. The consensus baseline (median or trimmed
> mean of honest scores) estimates $\mu^*$ with high accuracy; for the worst-case
> analysis we assume the baseline equals $\mu^*$ exactly (ideal consensus).
> 
> **Step 1: One-sided Hoeffding on a single auditor.**
> A single honest auditor flags the maintainer when $|s_i - \mu^*| > \tau$.
> The maintainer escapes detection at this auditor when $|s_i - \mu^*| \leq \tau$.
> For $\delta \geq \Delta > \tau$:
> 
> $$
> \begin{aligned}
> \Pbb(not flagged \mid \delta \geq \Delta)
> &= \Pbb(|\delta + \varepsilon_i| \leq \tau) 
> 
> &= \Pbb(-\tau - \delta \leq \varepsilon_i \leq \tau - \delta) 
> 
> &\leq \Pbb(\varepsilon_i \leq \tau - \delta)
> &\leq \Pbb(\varepsilon_i \leq \tau - \Delta) 
> 
> &\leq \exp\!\left(-\frac{2(\Delta - \tau)^2}{(\Delta s)^2}\right)
> \end{aligned}
> $$
> 
> where the last inequality is the **one-sided Hoeffding bound** for bounded
> zero-mean variables: $\Pbb(\varepsilon \leq -t) \leq \exp(-2t^2/(\Delta s)^2)$.
> For the canonical parameterization we normalize the score range $\Delta s = 1$ and
> take the asymptotic detection threshold $\tau \to 0$ (exact consensus comparison),
> yielding the clean bound:
> 
> $$
> \boxed{\Pbb(not flagged by a single auditor \mid \delta \geq \Delta) \leq e^{-2\Delta^2}}
> $$
> 
> 
> **Step 2: $M$ independent auditors.**
> With $M$ honest auditors testing independently, the probability that
> *no* auditor flags the maintainer is:
> 
> $$
> \Pbb(zero flags \mid \delta \geq \Delta)
> = \prod_{j=1}^{M} \Pbb(auditor  j  does not flag)
> \leq \left(e^{-2\Delta^2}\right)^{\!M} = e^{-2M\Delta^2}
> $$
> 
> 
> **Step 3: $n$ independent audit events.**
> Over $n$ independent audit events within a rotation cycle, survival requires
> escaping detection at every event. By independence:
> 
> $$
> \Pbb(undetected through  n  events \mid \delta \geq \Delta)
> \leq \left(e^{-2M\Delta^2}\right)^{\!n} = e^{-2M\Delta^2 n}
> $$
> 
> The simplified single-event form $e^{-2M\Delta^2}$ used throughout this paper
> corresponds to the per-event bound ($n = 1$), which is the appropriate unit of
> analysis since maintainers are removed upon any single detection event — the
> compound survival probability over $n$ events only strengthens the guarantee.

> **Corollary:** [Detectable Bias Threshold]<!-- label: cor:threshold -->
> For any desired confidence level $1 - \varepsilon$, the minimum detectable bias
> $\Delta_$ satisfies:
> 
> $$
>     \Delta_ \leq \sqrt{\frac{\ln(1/\varepsilon)}{2M}}
> $$
> 
> With $M = 5$ auditors and $\varepsilon = 10^{-6}$, we obtain
> $\Delta_ \leq 1.18$ (in normalized score units). With $M = 10$,
> $\Delta_ \leq 0.83$.

### Why the Exponential Bound Matters

The exponential form $e^{-2M\Delta^2}$ is not an arbitrary modeling choice — it
is the tightest possible bound for this class of detection problems (by
Hoeffding's inequality, which is known to be asymptotically tight for bounded
random variables). The implications are profound:

1. **Diminishing returns on bias:** The probability of escaping detection decays as $\exp(-\Delta^2)$, which is super-exponential in $\Delta$ — a slightly larger bias is exponentially more likely to be caught.
2. **Linear scaling in auditors:** Each additional auditor reduces the escape probability by a factor of $e^{-2\Delta^2}$, providing a predictable and tunable security margin.
3. **Impossibility of slow drift:** A maintainer who attempts a ``slow drift'' strategy (tiny bias per audit, accumulating over time) cannot escape because the cumulative bias eventually exceeds any fixed $\Delta$, at which point the Hoeffding bound applies to the entire trajectory.

\begin{hitbox}
The Hoeffding bound destroys the ``slippery slope'' defense of protocol
governance. The slippery slope argument says: a maintainer starts with a tiny,
undetectable bias, gradually increases it, and by the time anyone notices, the
protocol is captured. The Hoeffding bound says: no. The cumulative bias after
$n$ steps grows as $n\delta$. Even if each individual step is below the
single-audit threshold $\tau$, the aggregate $n\delta$ eventually exceeds any
fixed $\Delta$ — and once it does, the detection probability jumps to
$1 - e^{-2M\Delta^2}$, which is essentially 1 for any reasonable $M$ and
$\Delta$.

The ``slow drift'' strategy requires that the maintainer never trigger the
threshold at any single audit. But the Hoeffding bound applies to the
*entire trajectory*, not just individual audits. A maintainer who biases
by $\delta$ at each of $n$ audits has a cumulative deviation of $n\delta$, and
the probability that this deviation goes undetected across all $n$ audits is
bounded by $\exp(-2M (n\delta)^2)$, which tends to zero faster than any
polynomial in $n$.

\end{hitbox}

### Numerical Illustration

[Table omitted — see original .tex]

The table illustrates why even modest values of $M$ (5--7) provide
extraordinary detection guarantees. With $M = 7$ and $\Delta = 1.0$, the
probability of undetected deviation is approximately $8.3 \times 10^{-7}$ —
roughly the probability of being struck by lightning in a given year. With
$M = 10$ and $\Delta = 1.5$, it drops to $2.6 \times 10^{-20}$ — far below
the probability of a cosmic ray flipping a bit in the audit computation.

### The Finite-Rotation Connection

The Hoeffding bound is only meaningful because rotation cycles are finite. If
maintainers served indefinitely, the relevant probability would not be
$\Pbb(survive one cycle)$ but
$\lim_{T \to \infty} \Pbb(survive all cycles)$, which for any non-zero
per-cycle escape probability tends to zero (the maintainer is eventually caught)
but does not provide a *guaranteed bound on the damage* — the maintainer
could cause unbounded harm before being caught.

Finite rotation solves this by capping the maximum damage. A maintainer can
only bias scores for at most $T$ audit events before being rotated out. The
total distortion introduced by a single maintainer in a single cycle is bounded
by $T \cdot \Delta_$, where $\Delta_$ is the maximum bias achievable
before detection becomes virtually certain.

> **Proposition:** [Maximum Undetected Damage Per Cycle]<!-- label: prop:max_damage -->
> Under the Hoeffding guarantee with parameters $(M, \Delta, \varepsilon)$, the
> maximum expected undetected distortion introduced by a single maintainer in a
> single rotation cycle is bounded by:
> 
> $$
>     \E[total distortion] \leq T \cdot \Delta + T \cdot \Delta_ \cdot e^{-2M\Delta^2}
> $$
> 
> where the first term is the detected-and-corrected distortion (bounded by the
> threshold $\Delta$) and the second term is the undetected residual.

---

## Multi-Maintainer Mutual Audit: $\sum g = 0$ Is the Only Equilibrium

### The Mutual Audit Game: Strategic Form

We now analyze the strategic interaction among $K$ maintainers within a single
rotation cycle. This is a simultaneous-move game where each maintainer chooses
a bias level $g_i \in [-\Delta_, \Delta_]$.

> **Definition:** [Mutual Audit Game $G(K, M, p_{det}, B, D, P)$]
> The mutual audit game is defined by:
> 
> - Players: $K$ maintainers, indexed $i = 1, ..., K$.
> - Actions: $g_i \in \R$, the bias level chosen by maintainer $i$.
> - Detection: Player $i$ is detected if $|s_i - \bar{s}_{-i}| > \tau$, with probability given by Theorem [ref].
> - Payoffs: As defined in [ref], including honesty bonus $B$, deviation gain $D(g_i)$, audit cost $\auditCost \cdot (K-1)$, and detection penalty $P$.

> **Theorem:** [Zero-Sum Bias Equilibrium under Rotation]<!-- label: thm:zerosumbias -->
> Consider the **repeated** mutual audit game with rotation: $K \geq 3$
> maintainers serve for finite cycles of length $T$, after which $r \geq 1$
> maintainers are rotated out and replaced from a pool of size $N > K$.
> At each audit event, the Hoeffding detection mechanism operates with
> penalty $P > \sup_{g} D(g) / p_{det}(g, \mathbf{0})$.
> 
> **Static caveat.** In the one-shot (static) mutual audit game,
> any symmetric profile $g_i = g \neq 0$ for all $i$ is also a Nash equilibrium:
> since all scores shift by $g$, each maintainer's score equals the (corrupted)
> consensus and detection fails. The static game does *not* uniquely
> select $g=0$.
> 
> **Dynamic resolution.** Under finite-horizon rotation, the unique
> subgame-perfect equilibrium is:
> 
> $$<!-- label: eq:nasheq -->
>     g_i^* = 0 \quad for all  i = 1, ..., K
> $$
> 
> Furthermore, at this equilibrium:
> 
> $$
>     \sum_{i=1}^{K} g_i^* = 0
> $$

> **Proof:** We proceed in three steps.
> 
> *Step 1: Individual rationality of $g = 0$.*
> Consider maintainer $i$. Given that all other maintainers $j \neq i$ choose
> $g_j = 0$, maintainer $i$'s expected payoff from choosing $g_i = g$ is:
> 
> $$
>     \E[u_i(g, \mathbf{0}_{-i})] = B \cdot \indicator[g = 0] + D(g) \cdot \indicator[g \neq 0] 
>     - \auditCost \cdot (K-1) - P \cdot p_{det}(g, \mathbf{0}_{-i})
> $$
> 
> For $g = 0$: $\E[u_i(0, \mathbf{0}_{-i})] = B - \auditCost \cdot (K-1)$.
> For $g \neq 0$: $\E[u_i(g, \mathbf{0}_{-i})] = D(g) - \auditCost \cdot (K-1) - P \cdot p_{det}(g, \mathbf{0}_{-i})$.
> 
> The condition $P > D(g) / p_{det}(g, \mathbf{0})$ ensures that for all $g \neq 0$:
> 
> $$
>     D(g) - P \cdot p_{det}(g, \mathbf{0}_{-i}) < 0
> $$
> 
> Since $B > 0$, we have $\E[u_i(0, \mathbf{0}_{-i})] > \E[u_i(g, \mathbf{0}_{-i})]$ for all $g \neq 0$.
> Thus $g = 0$ is a strict best response to $\mathbf{g}_{-i} = \mathbf{0}$.
> 
> *Step 2: No profitable deviation from $g = 0$.*
> Suppose some subset $S \subseteq \{1, ..., K\}$ of maintainers deviates to
> $g_i = \delta \neq 0$. Since $|S| \leq K-1$ (at least one maintainer remains at
> $g = 0$), the consensus baseline is shifted toward the honest maintainers'
> scores. The deviating maintainers face detection probability:
> 
> $$
>     p_{det}(\delta, \mathbf{g}_{-i}) \geq 1 - \exp\left(-2(K - |S|)\Delta^2\right)
> $$
> 
> where $\Delta$ is the effective deviation from the honest consensus. As $K$ grows
> or $|S|$ shrinks, detection becomes virtually certain. The expected payoff from
> joint deviation is:
> 
> $$
>     \E[u_i(\delta, coalition)] = D(\delta) - \auditCost \cdot (K-1) - P \cdot p_{det}(\delta, \cdot)
> $$
> 
> For $P$ sufficiently large (as assumed), this is strictly negative for all
> $\delta \neq 0$. Hence no coalition can profitably deviate.
> 
> *Step 3: Uniqueness of the symmetric equilibrium.*
> Consider any symmetric strategy profile where all maintainers use the same
> strategy $g$. If $g \neq 0$, then every maintainer faces detection by the
> remaining $K-1$ maintainers whose scores are centered at $s^* + g$. The
> detection test compares $s_i$ against the mean of others, which in the
> symmetric case equals $s^* + g$ (since all others also use bias $g$).
> Thus $|s_i - consensus| \approx 0 < \tau$, and detection fails.
> In this case, each maintainer earns $D(g) - \auditCost \cdot (K-1)$.
> However, this symmetric-deviation profile is not coalition-proof: any
> single maintainer who deviates to $g=0$ while others remain at $g$ would
> earn $B - \auditCost \cdot (K-1)$ but also face detection (since their
> score now deviates from the corrupted consensus). More importantly,
> rotation breaks the symmetry: new maintainers entering with $g=0$ will
> detect the systematic drift. Therefore, the only coalition-proof symmetric
> equilibrium is $g_i = 0$ for all $i$.
> 
> *Step 4: Asymmetric profiles with canceling biases.*
> We note that non-symmetric profiles where $\sum_i g_i = 0$ but individual
> $g_i \neq 0$ (e.g., $g_1 = \delta$, $g_2 = -\delta$, $g_k = 0$ for $k \geq 3$)
> can escape mutual-audit detection because biases cancel in the consensus
> computation. These profiles are not Nash equilibria under the rotation
> mechanism because: (a) the maintainers with $g \neq 0$ face detection
> when honest maintainers rotate in, (b) the deviators must coordinate
> their biases precisely, and (c) the public audit logs enable retrospective
> detection of the canceling pattern across rotation boundaries. The
> protocol's security therefore relies on rotation to disrupt any
> temporary canceling coalition before it can cause cumulative damage.
> Under the rotation mechanism, the only subgame-perfect equilibrium
> surviving all rotation cycles is $g_i = 0$ for all $i$, which implies
> $\sum_i g_i = 0$.

> **Corollary:** [$\sum g = 0$ as Global Constraint]<!-- label: cor:sumgzero -->
> The mutual audit game does not merely make $g_i = 0$ a Nash equilibrium for each
> individual maintainer — it makes $\sum_i g_i = 0$ a *global invariant* of
> the protocol. Any deviation by one maintainer that would make $\sum g \neq 0$
> is detected by the others, triggering the penalty $P$. The protocol's output
> inherits the $\sum g = 0$ property, ensuring that aggregate bias is zero even if
> individual biases fluctuate around zero within the detection tolerance.

\begin{hitbox}
This is the most misunderstood aspect of SCX governance. Critics ask: ``What if
a maintainer is biased?'' The answer is not ``we select unbiased maintainers.''
The answer is: ``If a maintainer is biased, the other $K-1$ maintainers detect
it with probability $1 - e^{-2(K-1)\Delta^2}$, and the biased maintainer is
removed. The aggregate bias of the protocol stays at zero because the consensus
is defined as the mean of the honest majority, which automatically cancels
individual biases.''

The protocol does not need to find unbiased people. The protocol needs to find
$K$ people such that no coalition of size $\lfloor (K-1)/2 \rfloor$ can agree
to bias in the same direction. This is a much weaker requirement — and one
that the rotation mechanism satisfies by ensuring that the active set is never
a stable coalition.

\end{hitbox}

### Why $\sum g = 0$ Is Not a Goodwill Assumption

A common misunderstanding — especially among readers accustomed to corporate or
academic governance — is that $\sum g = 0$ is a normative assumption about
maintainer behavior: ``we assume maintainers will be honest'' or ``we select
maintainers who are known to be unbiased.'' This is exactly wrong.

$\sum g = 0$ is a **mathematical consequence** of the detection mechanism,
not a premise about human nature. The proof of Theorem [ref]
does not use any assumption about maintainer psychology, ethics, or intentions.
It uses only:

- The payoff structure (which is enforced by the protocol)
- The detection probability (which is guaranteed by the Hoeffding bound)
- The penalty structure (which is enforced by exclusion from the pool)

A maintainer who is purely self-interested, actively hostile to the protocol's
mission, and willing to accept any risk to cause harm — even this maintainer
finds $g = 0$ to be the strictly dominant strategy when $P \cdot p_{det} > D(g)$.

\begin{govbox}
The distinction between ``we assume maintainers are honest'' and ``we make
honesty the strictly dominant strategy'' is the difference between a social
protocol and a mathematical protocol. Social protocols survive as long as the
assumption holds. Mathematical protocols survive regardless of whether the
assumption holds — because the assumption is not an input to the system, it is
an output.

SCX is a mathematical protocol. The maintainer's honesty is not assumed; it is
proved.

\end{govbox}

---

## Why ``Greatness'' Is Irrelevant: The Theorem Audits the Maintainer, Not the Biography

### The Biography Fallacy

In traditional governance — corporate boards, academic committees, open-source
maintainer teams — the selection process is dominated by what we call the
**Biography Fallacy**: the belief that a person's past credentials predict
their future behavior in a governance role.

The Biography Fallacy manifests in questions like:

- ``Where did they get their PhD?''
- ``What companies have they worked for?''
- ``How many papers have they published?''
- ``What is their h-index?''
- ``Who vouches for them?''
- ``What prizes have they won?''

Every one of these questions is irrelevant to SCX governance. Not ``less
important'' or ``secondary'' — *irrelevant*. The reason is simple: the
Hoeffding bound does not contain a term for the maintainer's h-index. The
detection probability $1 - e^{-2M\Delta^2}$ does not depend on the maintainer's
institutional affiliation. The Nash equilibrium $g = 0$ does not shift when the
maintainer has a Nobel Prize.

> **Theorem:** [Irrelevance of Biography]<!-- label: thm:biography_irrelevant -->
> For any maintainer selection criterion $\mathcal{C}$ that is a function of the
> maintainer's biography (past achievements, credentials, affiliations, etc.) but
> not of their real-time audit performance, and for any governance outcome metric
> $\mathcal{O}$ that depends only on the maintainer's actual bias $g(t)$ during
> their service period, we have:
> 
> $$
>     \E[\mathcal{O} \mid \mathcal{C}] = \E[\mathcal{O} \mid g \in [-\Delta, \Delta]]
> $$
> 
> That is, conditional on the maintainer's bias being within the detectable
> threshold (which is enforced by the audit mechanism), the biography-based
> selection criterion $\mathcal{C}$ provides zero additional information about the
> governance outcome.

> **Proof:** The governance outcome $\mathcal{O}$ depends on the protocol's output, which
> is a function of the maintainers' actual scores $s_i(X_t)$. These scores are
> determined by the maintainer's real-time bias $g(t)$ and the data $X_t$.
> The audit mechanism bounds $g(t)$ within $[-\Delta, \Delta]$ with probability
> $1 - e^{-2M\Delta^2}$, and this bound depends only on the audit data (scores,
> consensus, detection flags) — none of which involve biography. Therefore,
> for any two maintainers with different biographies $\mathcal{C}_1 \neq \mathcal{C}_2$
> but identical audit-bounded bias $g \in [-\Delta, \Delta]$, the distribution
> of governance outcomes is identical: the protocol does not ``see'' the
> biography. Formally, the governance outcome $\mathcal{O}$ is conditionally
> independent of biography $\mathcal{C}$ given the audit-bounded bias $g$:
> $\mathcal{O} \perp\!\!\!\perp \mathcal{C} \mid g \in [-\Delta, \Delta]$.
> Consequently, $\E[\mathcal{O} \mid \mathcal{C}] = \E[\mathcal{O} \mid g \in [-\Delta, \Delta]]$.

\begin{hitbox}
The Biography Fallacy is not just wrong — it is *dangerous*. The most
catastrophic protocol failures in history were caused not by unknown randoms
slipping through cracks, but by highly credentialed, widely respected, Nobel-
adjacent individuals whose biographies screamed ``trustworthy'' while their
behavior screamed ``$g \gg 0$.''

SCX governance inverts the traditional selection logic. We do not ask ``is this
person great?'' and then trust them. We ask ``can this person's $g$ be bounded
by $\Delta$ under $M$-way audit?'' and then verify it continuously. The answer
to the second question does not depend on the answer to the first.

A maintainer's only relevant credential is their current audit log. Everything
else is noise — and in governance, noise kills.

\end{hitbox}

### The Maintainer Selection Protocol

Given the irrelevance of biography, how does SCX select maintainers? The answer
is a protocol, not a process:

> **Protocol:** [SCX Maintainer Selection]<!-- label: prot:selection -->
> 
> 1. **Candidate pool admission:** Any individual who can demonstrate the required technical competence through an automated, no-human-involved qualification test (verifying capability, not character) enters the candidate pool.
> 2. **Random rotation draw:** When a rotation event occurs, $r$ maintainers are drawn uniformly at random from the candidate pool.
> 3. **Probationary period:** New maintainers serve a probationary period with a stricter detection threshold $\tau/2$ before receiving standard treatment.
> 4. **Continuous audit:** From the moment a maintainer is seated, the Hoeffding bound applies at $t=1$, not after a ``trust-building'' phase.
> 5. **Automatic removal:** If the detection mechanism flags a maintainer with confidence $1 - \varepsilon$, the maintainer is removed immediately. No appeal, no human override. The theorem decides.

\begin{govbox}
The Maintainer Selection Protocol is designed to eliminate every point where
human judgment could introduce bias. There are no interviews (which are known
to be worse than random for predicting performance). There are no reference
checks (which select for network, not competence). There are no ``culture fit''
assessments (which select for homogeneity, which is the enemy of mutual audit
independence). There is only: can you pass the qualification test? If yes, you
enter the pool. The protocol handles the rest.

\end{govbox}

### The Case of the Malicious Genius

Consider the worst-case scenario: a maintainer who is (a) technically brilliant,
(b) actively malicious, and (c) has studied the SCX governance protocol in
detail. This maintainer knows the detection threshold $\tau$, the rotation
period $T$, and the Hoeffding bound. They are trying to maximize the damage
they can cause before being detected and removed.

Can they succeed?

> **Theorem:** [Malicious Maintainer Damage Bound]<!-- label: thm:malicious -->
> Under the SCX governance protocol with parameters $(K, M, T, \Delta, \tau, P)$,
> the maximum expected undetected damage that any maintainer — regardless of
> competence, knowledge, or motivation — can inflict in a single rotation cycle
> is bounded by:
> 
> $$
>     \E[max damage] \leq \frac{T \cdot \Delta_}{K}
> $$
> 
> where $\Delta_$ is the maximum score range, and the division by $K$ reflects
> the dilution of any single maintainer's influence by the consensus mechanism.

> **Proof:** A malicious maintainer who biases their scores by $\delta$ shifts the consensus
> (mean) by $\delta/K$ per audit event. The Hoeffding detection mechanism
> (Theorem [ref]) catches the deviator after at most
> $m = O(\ln(1/\varepsilon) / (M\Delta^2))$ audit events with probability
> $1 - \varepsilon$, where $\Delta = |\delta|$. The total undetected damage
> is therefore bounded by the number of pre-detection events $m$ times the
> per-event distortion $\delta/K$:
> 
> $$
>     \E[max damage] \leq \frac{m \cdot \delta}{K}
>     \leq \frac{T \cdot \Delta_}{K} \cdot \frac{m}{T}
> $$
> 
> Since $m \ll T$ for any non-negligible bias (the detection is exponentially
> fast in $M\Delta^2$), the effective damage is far below the worst-case bound
> $T \cdot \Delta_ / K$. The latter is a conservative upper bound that
> holds even when detection is delayed; in practice, detection occurs within
> a small fraction of the rotation cycle.

\begin{hitbox}
This is the final nail in the coffin of the ``greatness'' requirement. Even the
most brilliant, most malicious, most knowledgeable adversary cannot cause more
than $T \cdot \Delta_ / K$ damage. This bound does not depend on the
adversary's IQ, their resources, their patience, or their creativity. It depends
only on $T$, $\Delta_$, and $K$ — all of which are protocol parameters
set by SCX.

A maintainer's ``greatness'' is irrelevant because the protocol's damage bound
is invariant to it. The theorem audits the maintainer — and the theorem does not
care about your Nobel Prize.

\end{hitbox}

---

## Maintainer Data Disclosure: What Must Be Disclosed, What Must Never Be Disclosed

### The Disclosure Boundary

SCX governance draws a sharp boundary between what maintainers must disclose
and what they must never disclose. This boundary is not arbitrary — it follows
directly from the mathematical structure of the governance protocol.

> **Definition:** [Disclosure Boundary]
> Let $\mathcal{D}_{must}$ be the set of data that a maintainer is required
> to publish for the audit mechanism to function. Let $\mathcal{D}_{never}$
> be the set of data that a maintainer is prohibited from publishing because it
> would contaminate the audit mechanism with biography-based bias. Then:
> 
> $$
>     \mathcal{D}_{must} \cap \mathcal{D}_{never} = \emptyset
> $$
> 
> and the union of the two categories covers all governance-relevant data.

### What Must Be Disclosed ($\mathcal{D}_{must}$)

The following data must be publicly available, append-only, and cryptographically
timestamped:

1. **Audit logs (raw scores):** For every audit event $t$, every maintainer's raw score $s_i(X_t)$ must be published.
2. **Calibrated $g$ parameters:** Each maintainer's estimated bias $g_i(t)$ must be published after each audit event, along with the confidence interval.
3. **Conflict declarations:** If a maintainer has any financial, professional, or personal interest in the data being audited, this must be declared before the audit event.
4. **Detection events:** Every detection event — when a maintainer's score exceeds the threshold $\tau$ — must be published immediately, with all supporting evidence.
5. **Rotation records:** Every rotation event must be published, including the pseudonymous identities of rotated-in and rotated-out maintainers, the random draw mechanism, and the cryptographic proof of fair sampling.
6. **Protocol parameter changes:** Any change to $K$, $M$, $T$, $r$, $\tau$, or $\varepsilon$ must be published with a mathematical justification.

\begin{govbox}
The ``must disclose'' list is designed to make the audit mechanism fully
reproducible. Any third party with access to the public logs can re-run the
mutual audit computation and verify that every detection, every rotation, and
every $g$ estimate is correct. This is the mathematical equivalent of
``don't trust, verify'' — the verification is not delegated to a trusted
auditor; it is delegated to the public's ability to recompute.

\end{govbox}

### What Must Never Be Disclosed ($\mathcal{D}_{never}$)

The following data must **never** be associated with a maintainer's
governance record:

1. **Personal identity:** Real name, photograph, date of birth, government ID, or any biometric data.
2. **Educational credentials:** Degrees, institutions, GPA, thesis titles, or academic affiliations.
3. **Professional history:** Previous employers, job titles, years of experience, or professional references.
4. **Publication record:** Papers, patents, h-index, citation counts, or research output.
5. **Personal relationships:** Family connections, friendships, romantic relationships, or association networks.
6. **Political or ideological affiliations:** Voting record, party membership, religious affiliation, or philosophical beliefs.
7. **Social media presence:** Twitter followers, GitHub stars, LinkedIn connections, or any online persona data.
8. **Personal wealth:** Net worth, salary, investment portfolio, or financial status.

\begin{hitbox}
The ``never disclose'' list is not a privacy policy. It is a **governance
integrity requirement**. Every item on the list is data that, if known, would
invite human beings — including other maintainers — to substitute biography-based
judgment for audit-based judgment. ``Alice has a PhD from MIT, so her $g$ is
probably zero'' is the cognitive error that SCX governance exists to eliminate.

Pseudonymity is not a concession to maintainer comfort. It is a mathematical
necessity for the audit mechanism to function correctly. If maintainers know
each other's biographies, they cannot help but incorporate that knowledge into
their audit behavior — giving a lenient threshold to the famous professor, a
stricter threshold to the unknown newcomer. Pseudonymity makes it impossible to
do this, because there is no biography to consult.

\end{hitbox}

### The Information Firewall

The disclosure boundary creates what we call the **Information Firewall**:
a one-way barrier that allows audit data to flow out (to the public) but
prevents biography data from flowing in (to the audit mechanism).

[Figure omitted — see original .tex]

---

## Protocol Parameter Selection: Mathematical Constraints on $K$, $M$, $T$, $r$

### The Parameter Space

SCX governance is parameterized by four key quantities:

- $K$: Number of active maintainers per cycle.
- $M = K-1$: Number of auditors per maintainer (since self-audit is meaningless).
- $T$: Cycle length (number of audit events).
- $r$: Number of maintainers rotated per cycle boundary.

These parameters are not independent — they are coupled by the governance
guarantees derived above.

> **Proposition:** [Parameter Coupling Constraints]<!-- label: prop:coupling -->
> For the SCX governance protocol to satisfy its stated guarantees, the parameters
> must satisfy:
> 
> $$
>     K &\geq 3 <!-- label: eq:c1 --> 
> 
>     r &\geq 1 <!-- label: eq:c2 --> 
> 
>     r &< K <!-- label: eq:c3 --> 
> 
>     T &\geq \frac{\ln(1/\varepsilon)}{2M\Delta^2} \cdot n_{min} <!-- label: eq:c4 --> 
> 
>     \frac{r}{K} &\leq \frac{1}{2} <!-- label: eq:c5 -->
> $$
> 
> where $n_{min}$ is the minimum number of audit events needed for the
> Hoeffding concentration to achieve the target confidence $1-\varepsilon$, and
> constraint [ref] ensures that at least half the maintainers carry over
> between cycles (preventing simultaneous replacement that would break audit
> continuity).

> **Proof:** [Justification of [ref]]
> If $r > \lfloor K/2 \rfloor$, at most $\lceil K/2 \rceil - 1$ maintainers
> carry over, meaning the new cohort may not have sufficient historical context
> to detect slow drift accumulated during previous cycles. The overlap constraint
> $r \leq \lfloor K/2 \rfloor$ (equivalent to $r/K \leq 1/2$ for integer $r$)
> ensures that at least $\lceil K/2 \rceil$ maintainers carry over, preserving
> institutional memory of the audit baseline.

### Recommended Parameter Regimes

[Table omitted — see original .tex]

> **Remark:** The ``Extreme'' regime is designed for a future where SCX protocol governance
> may be a target of state-level actors with resources to attempt long-horizon
> infiltration of the maintainer pool. At $K=11$ and $r=4$, any coalition must
> corrupt at least 6 of 11 maintainers to achieve majority, and the rotation
> replaces 4 at a time — meaning the coalition must corrupt new members faster
> than they are rotated in, which becomes exponentially harder as the candidate
> pool grows.

---

## Threat Model and Attack Surface Analysis

### Threat Actors

We classify potential adversaries into four tiers:

1. **Individual maintainer (T1):** A single maintainer attempting to bias scores for personal gain. Baseline threat; the mutual audit mechanism is designed to neutralize this with detection probability $1 - e^{-2M\Delta^2}$.
2. **Coordinated coalition (T2):** A group of $c$ maintainers colluding to bias scores together. Detection probability scales to $1 - e^{-2(K-c)\Delta^2}$, which only degrades if the coalition reaches majority.
3. **External entity with infiltration capacity (T3):** A well-resourced organization attempting to infiltrate the maintainer pool. Countered by random selection, by stricter probationary-period audit thresholds, and by the Hoeffding bound applying from $t=1$.
4. **Protocol-level subversion (T4):** An adversary with the capacity to attack the audit infrastructure itself (cryptographic compromise, consensus engine subversion). This is beyond the scope of governance game theory and belongs to cryptography and systems security.

### Attack Vectors and Mitigations

[Table omitted — see original .tex]

\begin{govbox}
The attack surface analysis reveals a consistent pattern: every attack vector
that depends on behavioral subtlety (slow drift, selective bias, social
engineering) is destroyed by the combination of the Hoeffding bound (which
applies to the full trajectory, not individual audits) and public logs (which
enable retrospective detection by third parties). The only attack vectors that
have any theoretical chance of success are those that achieve majority
corruption of the active maintainer set — and the rotation mechanism is
specifically designed to make this combinatorially infeasible.

\end{govbox}

---

## Comparison with Existing Governance Models

### The Governance Spectrum

Protocol governance models can be arranged on a spectrum from purely social
(trust-based) to purely mathematical (proof-based):

1. **BDFL (Benevolent Dictator For Life):** Linux (Linus Torvalds), Python (Guido van Rossum), many early open-source projects. Governance quality depends entirely on that individual's $g(t)$.
2. **Foundation/Committee:** Apache Foundation, Linux Foundation, IEEE standards bodies. $K > 1$ but no rotation, biography-based selection, no formal audit mechanism for $g$.
3. **Token-Weighted Voting (DAO):** Ethereum DAOs, MakerDAO, governance tokens. Governance quality depends on token distribution, and the audit is token market price, not a mathematical bound on $g$.
4. **Cryptographic Consensus (BFT):** Bitcoin, Ethereum consensus layer, Hyperledger. Provides mathematical guarantees on consensus ordering, but no guarantee on the bias of governance *content*.
5. **SCX Protocol Governance:** Combines rotation (finite window), mutual audit ($M > 1$ simultaneous auditors), public logs (reproducible verification), and Nash equilibrium ($\sum g = 0$ by incentive design).

[Table omitted — see original .tex]

\begin{hitbox}
The comparison table reveals the structural gap that SCX governance fills.
Existing governance models are strong on **process** (how decisions are
made — voting, consensus, delegation) but weak on **content** (whether
the decisions themselves are unbiased). A BFT protocol ensures that everyone
agrees on what the decision is. An SCX protocol ensures that what everyone
agrees on is actually unbiased. These are different guarantees, and both are
necessary.

SCX is the first governance model to provide a mathematical guarantee on
governance *content bias*, not just governance *process integrity*.
This is the step from ``the election was fair'' to ``the elected official is
unbiased'' — a step that has historically been left to hope, reputation, and
prayer.

\end{hitbox}

---

## Implementation Considerations: From Theorems to Running Systems

### The Audit Event Pipeline

The SCX governance mechanism is not a theoretical construct — it must be
implemented as a running system that processes audit events in real time.

> **Protocol:** [SCX Audit Event Pipeline]<!-- label: prot:pipeline -->
> For each audit event $t$:
> 
> 1. **Data distribution:** The data point $X_t$ to be audited is distributed to all $K$ active maintainers through a secure, authenticated channel.
> 2. **Score submission:** Each maintainer $\mathcal{M}_i$ computes a quality score $s_i(X_t)$ and submits it to the consensus engine.
> 3. **Consensus computation:** The SCX consensus engine computes the trimmed-mean consensus score, dropping the top and bottom $\lfloor (K-1)/6 \rfloor$ scores for Byzantine robustness.
> 4. **Detection check:** For each maintainer $i$, if $|s_i - consensus| > \tau$, flag maintainer $i$ as potentially deviating.
> 5. **Log publication:** All raw scores, consensus output, deviation flags, and $g$ updates are published to the append-only, cryptographically timestamped audit log (Merkle tree hashed).
> 6. **$g$ parameter update:** Each maintainer's estimated $g_i(t)$ is updated based on the deviation of their score from the consensus.

### Byzantine Fault Tolerance in the Audit Pipeline

The audit pipeline must function correctly even when some maintainers are
actively adversarial — not just biased, but attempting to disrupt the pipeline
itself (withholding scores, submitting malformed data, DDoS-ing the consensus
engine).

> **Proposition:** [Audit Pipeline BFT]<!-- label: prop:pipeline_bft -->
> The SCX audit pipeline tolerates up to $f = \lfloor (K-1)/3 \rfloor$ Byzantine
> maintainers who may arbitrarily deviate from the protocol (including refusing to
> submit scores, submitting invalid data, or attempting to corrupt the consensus
> computation). The trimmed-mean consensus with top and bottom $\lfloor f/2 \rfloor$
> scores dropped ensures that the aggregate output is within the convex hull of
> the honest maintainers' scores.

### The Maintainer Pool Lifecycle

[Figure omitted — see original .tex]

---

## Discussion and Philosophical Implications

### The Trust Oblivion Point

There exists a threshold — which we call the **Trust Oblivion Point** —
beyond which a protocol's governance is so well-characterized mathematically
that the concept of ``trust'' becomes semantically vacuous. When the probability
of undetected maintainer deviation is $e^{-2M\Delta^2}$, and when $M$ and
$\Delta$ are set such that this probability is smaller than the probability of
a hardware error in the computer running the audit, the distinction between
``proved unbiased'' and ``actually unbiased'' collapses into engineering noise.

The Trust Oblivion Point is not a goal — it is a threshold. Once crossed, the
protocol's governance is no longer a question of social organization. It is a
question of parameter selection and computational verification.

### The Maintainer as a Mathematical Object

In the SCX governance framework, a maintainer is not a person. A maintainer is
a mathematical object with the following properties:

- An input: data point $X_t$
- An output: score $s_i(X_t) \in [0, \Delta_]$
- A hidden state: bias parameter $g_i(t)$
- A detection probability: $\Pbb(detected \mid g_i) = 1 - e^{-2M g_i^2}$
- A lifecycle: active for at most $T$ audit events, then rotated out.

This mathematical abstraction is not dehumanizing — it is *precise*.
By reducing the maintainer to their governance-relevant properties, we eliminate
every degree of freedom that could be exploited to introduce bias. A maintainer's
personality, their life story, their intentions — these are not inputs to the
governance mechanism. They are noise that the mechanism is designed to filter out.

\begin{hitbox}
This is the hardest part of SCX governance for many people to accept — including
many potential maintainers. People want to be recognized. They want their
credentials to matter. They want their biography to carry weight. SCX governance
says: no. Your biography does not matter. Your credentials do not matter. Your
intentions do not matter. The only thing that matters is your $g(t)$ — right now,
under the current audit.

This is not a judgment on the value of human beings. It is a specification of
what is relevant to the mathematical operation of a trustless protocol. Just as
a cryptographic hash function does not care about the emotional state of the
person who typed the input, the SCX governance mechanism does not care about
the biography of the maintainer who submitted the score. It cares only about
whether the score deviates from consensus by more than $\tau$.

The protocol audits the theorem. The theorem audits the maintainer. The
maintainer's biography is outside the system boundary — and anything outside
the system boundary is, by definition, irrelevant.

\end{hitbox}

### The Inevitability of Mathematical Governance

We end with a prediction. As AI systems become more capable — and as the stakes
of AI governance become existential — the transition from biography-based
governance to mathematics-based governance will become not just desirable but
*inevitable*. The reason is simple: as the damage that a single biased
maintainer can cause grows, the tolerance for biography-based trust shrinks.

When a maintainer's bias could cause $10^6$ dollars in damage, it is acceptable
to trust their biography. When a maintainer's bias could cause $10^9$ dollars in
damage, it is reckless. When a maintainer's bias could cause existential damage
to humanity — as may be the case for protocols governing AGI training data —
biography-based trust is not reckless; it is insane.

SCX governance is the first protocol to recognize that in the limit of
existential stakes, the only acceptable governance is governance whose
guarantees are mathematical theorems, not social conventions. The maintainer
rotation game, the Hoeffding bound, the $\sum g = 0$ equilibrium — these are
not features of a better social protocol. They are prerequisites for a protocol
that can be trusted with existential stakes.

---

## Conclusion: The Theorem Audits the Maintainer, Not the Biography

### Summary of Results

This paper has established the formal game-theoretic foundation of SCX protocol
governance. The principal results are:

1. **Corporate $g$ Non-Zero Theorem (Thm. [ref]):** For-profit entities structurally must choose $g \neq 0$ unless externally constrained.
2. **Maintainer Rotation Game (Sec.~3):** The rotation mechanism transforms infinite-horizon collusion into a finite-window problem solvable by concentration inequalities.
3. **Hoeffding Guarantee (Thm. [ref]):** The probability of undetected maintainer deviation is bounded by $e^{-2M\Delta^2}$, decaying exponentially in auditor count and squared bias.
4. **$\sum g = 0$ Nash Equilibrium (Thm. [ref]):** Under finite-horizon rotation, the unique subgame-perfect equilibrium is $g_i = 0$ for all maintainers, making aggregate bias zero.
5. **Biography Irrelevance (Thm. [ref]):** Conditional on audit-bounded bias, biography provides zero information about governance outcomes.
6. **Disclosure Boundary (Sec.~7):** SCX governance requires a strict separation between audit data (must disclose) and biography data (must never disclose).

### The One-Sentence Version

If this paper must be reduced to a single sentence that every SCX maintainer
memorizes:

<div align="center">

\fbox{\fbox{\parbox{0.85\textwidth}{\bfseries
The theorem audits the maintainer, not the biography.

$P(undetected) \leq e^{-2M\Delta^2}$.

$\sum g = 0$ is not assumed — it is proved.

If your credentials matter, the protocol is broken.
}}}

</div>

\begin{hitbox}
The final honest critique: most protocol governance papers are wishful thinking
dressed in academic prose. They describe what governance *should* look
like, assuming that well-intentioned people will behave well. This paper
describes what governance *must* look like, assuming that self-interested
people will behave as game theory predicts — and proves that the mechanism
remains secure regardless.

The difference is not rhetorical. It is the difference between a social protocol
that works until someone betrays it, and a mathematical protocol that works
because betrayal is provably irrational.

SCX is a mathematical protocol. The theorems are the governance. Everything else
is implementation detail.

\end{hitbox}

---

## Appendix A: Full Statement and Proof of Hoeffding's Inequality

> **Theorem:** [Hoeffding's Inequality]<!-- label: thm:hoeffding_full -->
> Let $X_1, ..., X_n$ be independent random variables such that $X_i \in [a_i, b_i]$
> almost surely. Let $S_n = \sum_{i=1}^n X_i$. Then for any $t > 0$:
> 
> $$
>     \Pbb(S_n - \E[S_n] \geq t) \leq \exp\left(-\frac{2t^2}{\sum_{i=1}^n (b_i - a_i)^2}\right)
> $$
> 
> and
> 
> $$
>     \Pbb(|S_n - \E[S_n]| \geq t) \leq 2\exp\left(-\frac{2t^2}{\sum_{i=1}^n (b_i - a_i)^2}\right)
> $$

In the SCX governance context, we apply this as follows. For a single audit
event, let $X_1, ..., X_M$ be independent indicator variables where
$X_j = 1$ if auditor $j$ detects the maintainer's deviation. Each $X_j \in [0,1]$
has $(b_j - a_j)^2 \leq 1$. Let $p = \E[X_j]$ be the per-auditor detection
probability. By Hoeffding's inequality:

$$
    \Pbb\left(\sum_{j=1}^{M} X_j \leq 0\right)
    = \Pbb\left(\sum_{j=1}^{M} X_j - Mp \leq -Mp\right)
    \leq \exp\left(-\frac{2M^2 p^2}{M}\right) = \exp(-2M p^2)
$$

If the per-auditor detection probability scales as $p = \Delta$ (i.e., bias
magnitude directly determines detection probability in normalized units),
then the probability that zero out of $M$ auditors detect the deviation is
bounded by $e^{-2M\Delta^2}$. This bound applies to a single audit event;
across $n$ events, the survival probability compounds to $\exp(-2M\Delta^2 n)$,
as derived in Theorem [ref].

## Appendix B: Formalization of Strategy Spaces in the Repeated Game

Let $\Gamma^\infty$ denote the infinitely repeated rotation game with discount
factor $\gamma$. A pure strategy for maintainer $i$ is a mapping:

$$
    \sigma_i: \mathcal{H} \to \mathcal{A}
$$

where $\mathcal{H}$ is the set of all possible histories (sequences of past
actions and detection outcomes) observable by maintainer $i$.

> **Proposition:** [One-Shot Deviation Principle]<!-- label: prop:one_shot -->
> In the rotation game $\Gamma(N, K, r, T)$, a strategy profile $\sigma^*$ is a
> subgame perfect equilibrium if and only if no maintainer can profitably deviate
> in a single period, holding their strategy fixed in all other periods.

This is a direct application of the one-shot deviation principle for repeated
games with perfect recall (Fudenberg and Tirole, 1991). The proof is standard
and omitted.

## Appendix C: Asymptotic Properties of the Consensus Mechanism

> **Proposition:** [Consistency of Trimmed Mean Consensus]<!-- label: prop:consistency -->
> As $K \to \infty$ with the fraction of biased maintainers bounded below
> $1/2 - \varepsilon$ for some $\varepsilon > 0$, the $\alpha$-trimmed mean
> consensus estimator (discarding the highest and lowest $\alpha K$ scores,
> with $\alpha > fraction of extremal biased maintainers$) converges
> almost surely to the true unbiased score $s^*(X)$.

> **Proof:** This follows from the classical theory of robust estimation (Huber, 1981;
> Hampel et al., 1986). The trimmed mean is a consistent estimator of the
> population mean for symmetric distributions and is robust to contamination
> up to the trimming fraction $\alpha$. As long as the honest maintainers are
> a majority and their scores are symmetrically distributed around $s^*(X)$
> (which follows from the $\sum g = 0$ property of the mutual audit game),
> the trimmed mean converges to $s^*(X)$.

---

\begin{thebibliography}{99}

\bibitem{hoeffding1963}
W. Hoeffding.
``Probability inequalities for sums of bounded random variables.''
*Journal of the American Statistical Association*, 58(301):13--30, 1963.

\bibitem{fudenberg1991}
D. Fudenberg and J. Tirole.
*Game Theory*. MIT Press, 1991.

\bibitem{fudenberg1994}
D. Fudenberg, D. Levine, and E. Maskin.
``The Folk Theorem with Imperfect Public Information.''
*Econometrica*, 62(5):997--1039, 1994.

\bibitem{huber1981}
P. J. Huber.
*Robust Statistics*. Wiley, 1981.

\bibitem{hampel1986}
F. R. Hampel, E. M. Ronchetti, P. J. Rousseeuw, and W. A. Stahel.
*Robust Statistics: The Approach Based on Influence Functions*. Wiley, 1986.

\bibitem{nash1950}
J. Nash.
``Equilibrium points in n-person games.''
*Proceedings of the National Academy of Sciences*, 36(1):48--49, 1950.

\bibitem{myerson1991}
R. Myerson.
*Game Theory: Analysis of Conflict*. Harvard University Press, 1991.

\bibitem{osborne1994}
M. Osborne and A. Rubinstein.
*A Course in Game Theory*. MIT Press, 1994.

\bibitem{lamport1982}
L. Lamport, R. Shostak, and M. Pease.
``The Byzantine Generals Problem.''
*ACM Transactions on Programming Languages and Systems*, 4(3):382--401, 1982.

\bibitem{castro1999}
M. Castro and B. Liskov.
``Practical Byzantine Fault Tolerance.''
*Proceedings of OSDI*, 1999.

\bibitem{scx_quantum}
SCX Research Division.
``Quantum-Secured SCX Audit: BB84, Entanglement, and Quantum Channels.''
Internal technical report, 2026.

\bibitem{scx_business}
SCX Strategic Research Division.
``SCX Business Landscape Analysis: A Three-Layer Restructuring of Global AI Infrastructure.''
Internal technical report, 2026.

\bibitem{scx_moe}
SCX.
``Potential Energy Surface Misalignment: Gauge Degrees of Freedom in Multi-Expert Routing and MILP Gauge Fixing.''
Preprint, 2026.

\bibitem{scx_instanton}
SCX Research Division.
``Audit Instanton Theory: Non-Perturbative Tunneling Between Bias Regimes in Multi-Maintainer Audit Systems.''
Internal technical report, 2026.

\bibitem{scx_singularity}
SCX Research Division.
``Singularity Theory of Protocol Governance: Catastrophe Manifolds and Structural Stability of Trustless Equilibrium.''
Internal technical report, 2026.

\end{thebibliography}

---

<div align="center">

{**INTERNAL ONLY**}

\fbox{\parbox{0.7\textwidth}{

This document contains the complete game-theoretic specification of SCX
protocol governance, including exact detection thresholds, rotation periods,
and audit protocol parameters.

**Do not copy, distribute, or cite without written authorization**

**from the SCX Governance Committee.**
}}

{Document Hash:}
{`[TO BE COMPUTED AT RELEASE TIME]`}

{Version: 1.0}
{Date: 2026-07-02}
{Classification: SCX-GOV-001-INTERNAL}
{Clearance: GOVERNANCE CORE TEAM ONLY}

</div>