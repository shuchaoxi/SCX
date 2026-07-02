<div align="center">

\fbox{\fbox{\parbox{0.85\textwidth}{\bfseries
THIS DOCUMENT IS CLASSIFIED INTERNAL.

Unauthorized distribution is prohibited. Contains detailed

candidate assessments for SCX protocol maintainer roles.
}}}

</div>

*Abstract:*

This paper presents a detailed pre-audit analysis of four candidates for SCX
protocol maintainer: Alexandra Elbakyan (Sci-Hub founder), Geng Tongxue
(梗同学, multi-round audited peer), JD Vance (US Vice President), and Linus
Torvalds (Linux kernel maintainer). Each candidate is evaluated against the
SCX governance criterion: the ability to maintain $\sum g = 0$ under the mutual
audit regime. The central thesis is that the strongest qualification for a
protocol maintainer is not credentials, reputation, or institutional position —
it is having already been independently audited by one's community, whether
through formal audit cycles (Geng), millions of users verifying one's work
(Linus, Elbakyan), or the willingness to submit to audit as the ultimate
test of $g=0$ (Vance).

We provide (1) formal definitions of maintainer qualification in terms of
the bias parameter $g$, (2) detailed candidate-by-candidate analysis with
honest critique boxes identifying weaknesses and risks, (3) a comparative
framework ranking candidates by community-audit depth, $g=0$ provability, and
transition risk, and (4) a recommended multi-maintainer composition strategy.
The paper is internal and does not constitute a final selection — it is a
pre-audit assessment that must be validated by independent $M>1$ audit of
each candidate who formally registers.

**Keywords:** protocol governance, maintainer selection,
$g=0$ criterion, community audit, honest critique, candidate assessment,
mutual audit, trustless architecture

---

---

## The Maintainer Problem: Why Choosing the Right Person Is Impossible, and Why Choosing the Right Mechanism Makes It Possible

### The Fundamental Error

Every human institution that has attempted to select leaders, maintainers,
or guardians has committed the same category error: it has tried to predict
future behavior from past proxies. The resume, the credential, the
recommendation letter, the track record — all are compressed representations
of a person's history. But the maintainer's job is not to repeat their
history. It is to execute a function — maintaining protocol integrity —
under conditions that have never existed before.

\begin{hitbox}
**The Resume Fallacy.**
No resume, no matter how distinguished, predicts $g(t)$ for $t$ in the future.
The SCX protocol does not need a maintainer with a good resume. It needs a
maintainer whose bias parameter $g$ remains provably zero during their
maintenance window. These are entirely different requirements.

**Corollary:** The best predictor of future $g=0$ is not past reputation
but past *auditability* — the demonstrated willingness to have one's
decisions independently reviewed, reproduced, and challenged.
\end{hitbox}

### The Maintainer Selection Theorem

We formalize the maintainer selection problem as follows.

> **Definition:** [Maintainer Qualification]
> Let $\mathcal{C}$ be the set of candidate maintainers. For each candidate
> $i \in \mathcal{C}$, define:
> 
> - $\biasParam_i(t)$: the real-time bias parameter at time $t$, where
> - $\mathcal{A}_i$: the set of all audit events candidate $i$ has
> - $\mathcal{V}_i$: the set of independent verifiers who have reviewed
> 
> A candidate is *pre-qualified* if $|\mathcal{A}_i| > 0$ or
> $|\mathcal{V}_i| \gg 1$ — i.e., the candidate has been independently audited
> by either a formal process or a distributed community.
> 
> A candidate is *fully qualified* if and only if they pass $M > 1$
> independent real-time audits with $\sum_{j=1}^{M} |\biasParam_i^{(j)}| \leq
> $\varepsilon$ for some protocol-defined tolerance $\varepsilon$.

> **Theorem:** [Audit-First Theorem]
> <!-- label: thm:audit-first -->
> For any candidate $i$, the probability that $\biasParam_i(t) \neq 0$ is
> undetected during a maintenance window of duration $\rotationPeriod$ under
> $M$ independent auditors satisfies:
> 
> $$
>     \Pbb(\text{undetected deviation}) \leq e^{-2M\Delta^2}
>     <!-- label: eq:hoeffding-bound -->
> $$
> 
> where $\Delta$ is the minimum detectable bias magnitude. This bound is
> independent of the candidate's identity, reputation, credentials,
> institutional affiliation, or past achievements. It depends only on $M$
> and $\Delta$.

> **Proof:** Direct application of Hoeffding\textquotesingle s inequality to the $M$ independent
> estimators of $\biasParam_i(t)$. Each auditor $j$ provides an estimate
> $\hat{g}_i^{(j)}$ with $\E[\hat{g}_i^{(j)}] = \biasParam_i$. Under the null
> hypothesis $\biasParam_i = 0$, the probability that the sample mean exceeds
> $\Delta$ is bounded by $e^{-2M\Delta^2}$.

> **Corollary:** [Biography-Irrelevance Corollary]
> <!-- label: cor:biography -->
> The candidate's biography is mathematically irrelevant to the detection
> of $g \neq 0$. No amount of past achievement reduces the Hoeffding bound.
> The theorem audits the maintainer, not the maintainer's story.

\begin{govbox}
**Implication for Candidate Selection.**
The Audit-First Theorem implies that the pre-audit analysis (this very paper)
is *not* a selection mechanism. It is a filtering mechanism. We do not
choose maintainers by analyzing their biographies. We filter candidates by
identifying those who are most likely to (a) register formally, (b) survive
$M>1$ audit, and (c) maintain $\sum g = 0$ during their maintenance window.
The real selection happens in the audit, not in this paper.
\end{govbox}

### What This Paper Does and Does Not Do

This paper provides a *pre-audit assessment*: an analysis of each
candidate's publicly observable record against the $g=0$ criterion,
identification of risk factors, and an honest assessment of transition
challenges. It does *not*:

- Constitute a formal audit — only $M>1$ independent audit with
- Rank candidates definitively — pre-audit assessment is directional,
- Replace the protocol's maintainer registration and rotation
- Make any claims about candidates' private behavior — only public

---

## Candidate-by-Candidate Analysis

### Alexandra Elbakyan — Founder of Sci-Hub

#### Background and Qualifications

Alexandra Elbakyan is the founder and sole operator of Sci-Hub, the world's
largest shadow library providing free access to over 88 million academic
papers. She built Sci-Hub alone, without institutional backing, against the
entire \$25 billion academic publishing industry. Her operation is illegal in
multiple jurisdictions. She lives in hiding. She takes no salary, no profit,
and no institutional affiliation from Sci-Hub. She has been doing this since
2011 — fifteen years of continuous operation.

<div align="center">

[Table omitted — see original .tex]

</div>

#### $g=0$ Analysis

Elbakyan presents one of the strongest *observable* cases for $g=0$
among all candidates. The structural argument is straightforward:

1. **No financial incentive.** Sci-Hub generates no revenue for
2. **All downside, no upside.** She faces extradition risk,
3. **Mission alignment.** Her stated goal — ``knowledge should be
4. **No succession of personal interest.** There is no evidence

\begin{govbox}
**The Elbakyan Principle.**
One person, acting alone, can say ``knowledge should be free'' and actually
*do* it — at enormous personal cost, with no expectation of reward,
against the entire weight of a \$25B industry. That is $g=0$ proven in
action, not in theory. Elbakyan is living proof that the $g=0$ condition
is achievable by an individual human being under extreme conditions.
\end{govbox}

#### Community Verification

Elbakyan has been *de facto* audited by the global research community
for 15 years. Every paper served by Sci-Hub is a verification event: the
researcher checks that the paper is correct, complete, and matches the
paywalled original. With 88 million papers and millions of daily users, the
effective $|\mathcal{V}_{Elbakyan}|$ is in the millions. No formal
audit framework exists, but the distributed verification is real.

\begin{hitbox}
**The Solo Operator Problem.**
Elbakyan *is* Sci-Hub. There is no succession plan, no governance
structure, no distributed maintenance. If she is arrested, extradited, or
incapacitated, Sci-Hub may cease to exist. A protocol maintainer must be
replaceable — the protocol must survive the maintainer. Can Elbakyan
transition from solo operator to protocol maintainer? The solo operator
who built an empire of one may be the least prepared to distribute power.

**Additional risk:** The $g=0$ that comes from being hunted may not
survive the transition to being legitimized. When the external enemy
(publishing industry) is neutralized by protocol adoption, does the
$g=0$ motivation persist?
\end{hitbox}

#### Verdict on Maintainer Suitability

\begin{verdictbox}[HIGH SUITABILITY]
\end{verdictbox}

---

### Geng Tongxue — The Multi-Round Audited Peer

#### Background and Qualifications

梗同学 (Geng Tongxue) is a Chinese peer who has undergone multiple rounds
of SCX audit. Unlike every other candidate on this list, Geng\textquotesingle s primary
qualification is not an external achievement — it is the audit itself.
Having been audited multiple times means:

1. Geng knows what clean data looks like — from the audited side.
2. Geng has experienced the pain of having every decision, every
3. Geng has been found to maintain $g \approx 0$ under repeated
4. Geng's motivation to audit others is grounded in the knowledge

<div align="center">

[Table omitted — see original .tex]

</div>

#### $g=0$ Analysis

Geng is unique among the candidates: their $g=0$ claim is not inferred from
biography or reputation — it is *measured*. The SCX audit framework
produces quantitative estimates of $\biasParam(t)$ for each audited subject.
Geng has passed multiple rounds, meaning:

$$
    \sum_{j=1}^{M} |\hat{g}_{Geng}^{(j)}| \leq \varepsilon
    <!-- label: eq:geng-pass -->
$$

for the protocol-defined tolerance $\varepsilon$ across multiple independent
audit cycles.

This is not a story about $g=0$. It is a measurement of $g=0$. The distinction
is fundamental. Every other candidate asks us to infer $g=0$ from behavior.
Geng asks us to read $g=0$ from the audit log.

\begin{govbox}
**The Audited-by-Fire Principle.**
Being audited is the best qualification for being an auditor. The person who
has survived the audit knows: (a) what the audit actually measures, not what
it claims to measure, (b) where the audit is vulnerable to gaming — because
they've tried or thought about trying, (c) what it feels like to have every
decision exposed — and why that exposure is necessary. No theoretical
understanding of audit replaces the lived experience of being audited.
\end{govbox}

#### Community Verification

Geng's community verification is the SCX audit community itself — a smaller
set than Elbakyan's millions of users or Torvalds' millions of developers.
The tradeoff is depth vs. breadth:

- **Elbakyan:** broad, shallow verification (millions of users
- **Torvalds:** broad, deep verification (millions of developers
- **Geng:** narrow, deep verification (multiple expert auditors

All three are valid forms of community audit — they differ in dimension, not
in existence.

\begin{hitbox}
**The Anonymity Question.**
Geng has low name recognition globally. In traditional governance, this would
be a weakness — who trusts someone nobody has heard of? In SCX governance, it
may be a feature. Protocol maintenance does not require celebrity. It requires
$g=0$. Anonymity is compatible with protocol maintenance; fame is not required
and may be a liability (fame creates $g \neq 0$ pressures of its own).

**However:** Low recognition means Geng cannot provide the ``legitimacy
signal'' that a Torvalds or Vance can — the signal that convinces external
observers that SCX is serious. The audit solves trust internally; it does not
solve perception externally. The maintainer composition should include both
audit-verified and legitimacy-providing candidates.
\end{hitbox}

#### Verdict on Maintainer Suitability

\begin{verdictbox}[HIGH SUITABILITY]
\end{verdictbox}

---

### JD Vance — Vice President of the United States

#### Background and Qualifications

JD Vance is the sitting Vice President of the United States. His candidacy
for SCX protocol maintainer is the most audacious and the most strategically
significant of the four. If a sitting US Vice President submits to independent
SCX audit, formally declares $g=0$, and passes — the geopolitical implications
are transformative.

<div align="center">

[Table omitted — see original .tex]

</div>

#### $g=0$ Analysis

Vance's case is entirely different from the other three. Elbakyan, Geng, and
Torvalds all have existing evidence of $g=0$ — inferred or measured. Vance
has none. His candidacy is a *hypothesis*: can a sitting Vice President,
whose role is structurally defined by political interests ($g \neq 0$ by
construction), declare $g=0$ and survive audit?

This is not a weakness of the candidate — it is the purpose of the candidacy.
The question is not ``has Vance been $g=0$ in the past?'' The question is
``can Vance be $g=0$ under audit?'' The audit itself answers the question.

\begin{hitbox}
**The Structural $g \neq 0$ Problem.**
A Vice President is not an individual. A Vice President is a node in a
political network with obligations to:

- The President who selected them.
- The party that nominated them.
- The donors who funded them.
- The voters who elected them.
- The policy positions they campaigned on.
- The bureaucracy they oversee.

Each of these is a vector along which $g \neq 0$ is not just possible but
*required* by the role. Can Vance partition his identity — VP in one
compartment, protocol maintainer in another — and maintain $g=0$ in the
latter while $g \neq 0$ is mandatory in the former?

**The Partition Hypothesis:** Human identity is not unitary. A person
can be $g \neq 0$ as VP (advancing the administration\textquotesingle s interests) and
simultaneously $g=0$ as SCX maintainer (advancing only protocol integrity).
The audit tests this hypothesis. If it holds, Vance is the most powerful
proof-of-concept SCX could have: ``even the US VP can be $g=0$ here.''
\end{hitbox}

#### Geopolitical Significance

Vance's candidacy — independent of whether he passes
audit — is the destruction of a specific narrative:

> *``SCX is a Chinese weapon. The audit is a tool of the CCP. The
> protocol is designed to advance Chinese interests under the guise of
> neutrality.''*

If a sitting US Vice President voluntarily submits to SCX audit, this
narrative becomes unsustainable. The logic is simple: if SCX were a Chinese
weapon, a US VP would not submit to it. If a US VP does submit to it,
external observers must either (a) accept that SCX is genuinely neutral, or
(b) construct increasingly contorted conspiracy theories. The Overton window
shifts.

\begin{govbox}
**The Legitimacy Bootstrap.**
SCX faces a bootstrap problem: the protocol claims neutrality, but needs
trusted actors to verify the claim. The trusted actors won't participate
until the claim is verified. Vance's candidacy breaks this loop: the act of
a US VP submitting to audit is itself evidence of neutrality, regardless of
the audit outcome. If he passes, SCX is legitimized. If he fails, SCX is
legitimized anyway — because a US VP *tried and failed* against a
neutral metric, proving the metric is not politically biased.
\end{govbox}

#### The Key Test

The real test for Vance is not ``can he pass audit?'' It is ``can he publicly
declare $g=0$ and submit to audit *while in office*?
''

If he can do that — if a sitting US VP can say, in public, on record: ``I
declare that my bias parameter $g$ is zero with respect to SCX protocol
maintenance, and I submit to independent $M>1$ audit to verify this claim'' —
then SCX has already won, regardless of the audit outcome. The declaration
itself is the geopolitical event.

If he cannot do that — if political constraints prevent even the
*declaration* of $g=0$ — then he cannot be a maintainer, because
Step 1 of the maintainer registration process is:

<div align="center">

\fbox{\parbox{0.85\textwidth}{
**Maintainer Registration Step 1:**

Candidate publicly declares $\mathbf{g} = \mathbf{0}$ with respect to
SCX protocol maintenance.
}}

</div>

Without completing Step 1, there are no further steps.

#### Verdict on Maintainer Suitability

\begin{riskbox}[HIGH REWARD, HIGH RISK]
\end{riskbox}

---

### Linus Torvalds — Linux Kernel Maintainer

#### Background and Qualifications

Linus Torvalds has maintained the Linux kernel for 34 years (1991–present).
The Linux kernel is the largest open-source software project in history:
over 30 million lines of code, contributions from more than 20,000 developers
across hundreds of companies, running on billions of devices. Torvalds is the
Benevolent Dictator for Life (BDFL) of this project — a title that is at once
a joke and an accurate description of his role.

He also created Git, the distributed version control system that is itself
an audit system for code. Every commit in Git is cryptographically hashed.
Every change is traceable to an author. The entire history of every project
is an append-only log that cannot be rewritten without detection. Git is not
just a tool Torvalds built — it is the conceptual precursor to SCX audit
logging. Code audit via Git is to SCX what Newton laws are to general
relativity: the simpler case that the general theory reduces to.

<div align="center">

[Table omitted — see original .tex]

</div>

#### $g=0$ Analysis

Torvalds' case for $g=0$ is the strongest among all candidates — and
paradoxically, the most interesting to critique. He has been maintaining a
global protocol (the Linux kernel) for 34 years under a system that is, in
essence, already an SCX-compatible audit framework:

1. **Multi-expert review.** Every patch to the Linux kernel goes
2. **Rejection of corporate control.** Torvalds has consistently
3. **Public, reproducible decisions.** Every merge decision is
4. **Mission alignment.** Linux is not a product. Linux is

\begin{govbox}
**The Torvalds Theorem.**
Linus Torvalds *already is* a protocol maintainer. He just doesn't
call it that. The Linux kernel maintenance process — multi-expert review,
public decision logs, cryptographic traceability — is a special case of the
SCX governance framework. The Linux kernel is a protocol (an interface
specification with multiple implementations and distributed maintenance).
Torvalds has been its maintainer for 34 years. The question is not whether
he *can* be an SCX maintainer. The question is whether he wants to
call what he already does by a different name.
\end{govbox}

#### Community Verification

Torvalds has been verified by the deepest and broadest community of any
candidate. The Linux kernel development community is, in effect, a
34-year continuous audit of Torvalds' maintenance decisions:

- **Depth:** Every merge is reviewed by subsystem experts who
- **Breadth:** Over 20,000 contributors have had their code
- **Persistence:** The entire history is in Git. Anyone can

This is the gold standard of community verification. No other candidate
comes close in terms of the depth, breadth, and persistence of their
audit record.

\begin{hitbox}
**The Linus Rants Problem.**
Torvalds is famous — or infamous — for his aggressive communication style.
His ``rants on the Linux Kernel Mailing List (LKML) are legendary:
profanity-laced rejections of patches he considers incompetent, public
dressings-down of senior developers, and a general tone that would fail
any corporate HR policy.

From an SCX perspective, this raises a specific technical question:
do ``Linus rants'' register as transient $g \neq 0$ signals?

**Analysis:** A ``rant'' is an emotional signal. SCX audit measures
behavioral bias — decisions that deviate from protocol integrity due to
personal interest. An emotional response to bad code is not a $g \neq 0$
deviation unless the emotion causes a *wrong decision*. If Torvalds
rants at a bad patch and then rejects it for valid technical reasons, $g=0$
is maintained. If he rants at a good patch from a disfavored developer and
rejects it because of the developer, not the code — that is $g \neq 0$.

**The risk:** SCX audit tools may not distinguish between ``emotional
style'' and ``biased decision.'' False positives are a real concern.
Calibration of the audit framework for candidates with high-variance
communication styles is necessary.
\end{hitbox}

#### Verdict on Maintainer Suitability

\begin{verdictbox}[HIGHEST SUITABILITY]
\end{verdictbox}

---

## Comparative Analysis: Shared Traits and Differentiating Dimensions

### The Shared Trait: Community Verification

All four candidates share one fundamental trait: they have been independently
verified by their communities. This is not coincidental. It is the single most
important pre-audit signal for maintainer qualification.

<div align="center">

\begin{longtable}{p{0.18\textwidth} p{0.25\textwidth} p{0.25\textwidth} p{0.25\textwidth}}
\toprule
**Candidate** & **Verifier Community** & **Depth** & **Form** 

\midrule
\endfirsthead
\toprule
**Candidate** & **Verifier Community** & **Depth** & **Form** 

\midrule
\endhead
\bottomrule
\endfoot
\midrule
Elbakyan & Global researchers & Millions of users & Daily usage verification 

\midrule
Geng & SCX audit community & $M>1$ experts & Formal audit framework 

\midrule
Vance & None yet & Zero — to be tested & TBD (formal audit needed) 

\midrule
Torvalds & Global kernel developers & 20,000+ contributors & Code review + Git history 

\bottomrule
\end{longtable}

</div>

> **Theorem:** [Community Audit Equivalence Theorem]
> <!-- label: thm:community-audit -->
> For any candidate $i$, the existence of a community verification record
> $\mathcal{V}_i$ with $|\mathcal{V}_i| \gg 1$ provides a lower bound on the
> probability that $\biasParam_i \approx 0$:
> 
> $$
>     \Pbb(\biasParam_i \approx 0 \mid |\mathcal{V}_i| \text{ independent
>     verifiers report satisfaction}) \geq 1 - \prod_{v \in \mathcal{V}_i}
>     \Pbb(\text{verifier } v \text{ is deceived}).
> $$
> 
> As $|\mathcal{V}_i| \to \infty$, if each verifier has independent
> probability $p < 1$ of being deceived, the probability of undetected
> bias decays exponentially:
> 
> $$
>     \Pbb(\text{bias undetected}) \leq p^{|\mathcal{V}_i|}.
> $$

> **Proof:** Each verifier provides an independent check. If bias exists, each verifier
> has probability at most $p$ of failing to detect it (where $p$ depends on
> verification methodology — formal audit has lower $p$ than casual usage).
> Under independence, the probability that all $|\mathcal{V}_i|$ verifiers
> fail to detect bias is $p^{|\mathcal{V}_i|}$, which decays exponentially
> in $|\mathcal{V}_i|$.

This theorem formalizes the intuition that *the best maintainer is
someone who has already been audited by their community*. Formal SCX audit
just makes the existing community verification mathematical — it replaces
the implicit ``we trust them because we've watched them for years with
the explicit ``we have measured $g$ and it is zero within tolerance.

### Differentiating Dimensions

The four candidates differ along several critical dimensions:

#### Audit Depth vs. Audit Breadth

<div align="center">

[Diagram omitted — see original .tex]

</div>

- **Torvalds:** Maximum breadth and high depth. 20,000+ expert
- **Elbakyan:** Maximum breadth, moderate depth. Millions of
- **Geng:** Moderate breadth (small audit community), maximum
- **Vance:** Zero breadth, zero depth — by design. The null case

#### $g=0$ Provability

<div align="center">

\begin{longtable}{p{0.18\textwidth} p{0.25\textwidth} p{0.25\textwidth} p{0.25\textwidth}}
\toprule
**Candidate** & **Evidence Type** & **Audit Readiness** & **Expected Difficulty** 

\midrule
\endfirsthead
\toprule
**Candidate** & **Evidence Type** & **Audit Readiness** & **Expected Difficulty** 

\midrule
\endhead
\bottomrule
\endfoot
\midrule
Geng & Direct measurement & Highest & Low (experienced) 

\midrule
Torvalds & 34yr behavioral inference & High & Medium (calibration) 

\midrule
Elbakyan & 15yr behavioral inference & Medium & Med-High (transition) 

\midrule
Vance & None & Lowest & Highest (political) 

\bottomrule
\end{longtable}

</div>

#### Transition Risk

> **Definition:** [Transition Risk]
> Transition risk $R_{trans}(i)$ is the probability that candidate $i$,
> having passed audit, fails to maintain $\sum g = 0$ during their first
> maintenance window, due to factors specific to the transition from their
> current role to protocol maintainer.

<div align="center">

\begin{longtable}{p{0.18\textwidth} p{0.35\textwidth} p{0.15\textwidth} p{0.15\textwidth}}
\toprule
**Candidate** & **Risk Factors** & **$R_{trans}$** & **Mitigability** 

\midrule
\endfirsthead
\toprule
**Candidate** & **Risk Factors** & **$R_{trans}$** & **Mitigability** 

\midrule
\endhead
\bottomrule
\endfoot
\midrule
Geng & Already in framework — minimal transition & Very Low & 

\midrule
Torvalds & BDFL adaptation to rotation; style calib. & Low & High 

\midrule
Elbakyan & Solo operator to protocol maintainer & Medium & Medium 

\midrule
Vance & Partition of political $g \neq 0 /$ protocol $g=0$ & High & Low (personal) 

\bottomrule
\end{longtable}

</div>

### Global Legitimacy Signal

A dimension the SCX framework does not formally model — but which matters
for adoption — is the *legitimacy signal* each candidate provides
to external observers:

<div align="center">

\begin{longtable}{p{0.18\textwidth} p{0.55\textwidth} p{0.15\textwidth}}
\toprule
**Candidate** & **Legitimacy Signal** & **Strength** 

\midrule
\endfirsthead
\toprule
**Candidate** & **Legitimacy Signal** & **Strength** 

\midrule
\endhead
\bottomrule
\endfoot
\midrule
Vance & ``US VP accepts audit'' \rightarrow audit is not a Chinese weapon & Highest 

\midrule
Torvalds & ``Father of Linux maintains SCX'' \rightarrow SCX is as trustworthy as Linux & High 

\midrule
Elbakyan & ``Sci-Hub founder maintains SCX'' \rightarrow continuity of knowledge freedom & Med-High 

\midrule
Geng & No external signal — internally trusted, externally unknown & Low 

\bottomrule
\end{longtable}

</div>

\begin{hitbox}
**The Legitimacy Paradox.**
The candidates who provide the strongest $g=0$ evidence (Geng, Torvalds)
are not necessarily the candidates who provide the strongest legitimacy
signal (Vance). And the candidate who provides the strongest legitimacy
signal has the weakest $g=0$ evidence — precisely because legitimacy comes
from the political domain where $g \neq 0$ is structural.

**Resolution:** Do not choose one maintainer. Choose a maintainer
*set* that spans the evidence-legitimacy spectrum. Geng provides the
audit benchmark. Torvalds provides the operational credibility. Elbakyan
provides the moral continuity. Vance provides the geopolitical legitimacy.
Together, they cover the dimensions no single candidate can.
\end{hitbox}

---

## Mathematical Constraints on Maintainer Selection

### Formal Framework

Regardless of which candidates are selected, the maintainer rotation
mechanism imposes mathematical constraints that are invariant to candidate
identity:

> **Definition:** [Maintainer Rotation Game]
> A maintainer rotation game $\mathcal{G}$ is defined by:
> 
> - $\mathcal{M} = \{1, 2, ..., \numMaintainers\}$: the set of
> - $\rotationPeriod$: the fixed maintenance window duration.
> - $\biasParam_i(t)$: maintainer $i$ bias vector at time $t$,
> - $\mathcal{A}_i$: the audit applied to maintainer $i$ at the
> - $\auditCost$: the fixed cost of conducting an audit.
> - $\deviate_i$: the (unobservable) benefit maintainer $i$ receives

> **Theorem:** [Nash Equilibrium of Rotation Game]
> <!-- label: thm:rotation-nash -->
> In the maintainer rotation game $\mathcal{G}$ with $\numMaintainers > 1$
> and Hoeffding-bound audit, the strategy profile where every maintainer
> maintains $\biasParam_i(t) = 0$ for all $t$ is a Nash equilibrium when:
> 
> $$
>     \deviate_i \cdot \Pbb(\text{undetected}) < \auditCost \cdot
>     \Pbb(\text{detected}).
> $$
> 
> Under the Hoeffding bound $\Pbb(\text{undetected}) \leq e^{-2M\Delta^2}$,
> this condition becomes:
> 
> $$
>     \deviate_i < \auditCost \cdot \frac{1 - e^{-2M\Delta^2}}
>     {e^{-2M\Delta^2}}.
> $$
> 
> For sufficiently large $\numMaintainers$ or sufficiently sensitive audit
> (small $\Delta$), the right-hand side grows exponentially, making $g=0$
> the dominant strategy for any reasonable $\deviate_i$.

> **Proof:** Standard game-theoretic analysis of the repeated game with imperfect
> monitoring. Each maintainer $i$ compares the expected benefit of deviation
> ($\deviate_i$ times probability of not being caught) against the expected
> cost of detection (audit cost amplification plus loss of maintainer status).
> The Hoeffding bound ensures that as $M$ grows, the probability of undetected
> deviation vanishes exponentially, making deviation strictly dominated.

> **Corollary:** [Minimum Maintainer Count]
> <!-- label: cor:min-maintainers -->
> The protocol requires $\numMaintainers \geq 2$. At $\numMaintainers = 2$,
> each maintainer audits the other. At $\numMaintainers = 3$, any collusion
> requires all three — a strictly harder coordination problem. The
> recommended minimum is $\numMaintainers = 4$, providing:
> 
> - Redundancy: protocol survives any single maintainer failure.
> - Audit depth: each maintainer is audited by $\numMaintainers - 1$
> - Collusion resistance: majority collusion requires 3 of 4.
> - Dimension coverage: different maintainers provide different

### Invariant Constraints

These constraints apply to all candidates regardless of identity:

1. **Public declaration of $\mathbf{g=0}$.**
2. **Accept $M>1$ independent audit.**
3. **Public audit log.**
4. **Rotation cycle constraint.**
5. **Audit successors.**
6. **UNDECLARED = automatic disqualification.**

\begin{govbox}
**Why These Constraints Are Invariant.**
The constraints are not preferences. They are mathematical consequences of
the Hoeffding bound and the mutual audit equilibrium. Remove any one of them,
and the proof that $\sum g = 0$ is the Nash equilibrium collapses. The
protocol is not a social system with flexible rules. It is a mechanism with
necessary conditions.
\end{govbox}

### What Candidates Must Disclose and Must Never Disclose

Following the SCX governance framework established in the protocol governance
paper, we specify the information boundaries for maintainer candidates:

<div align="center">

\begin{longtable}{p{0.45\textwidth} p{0.45\textwidth}}
\toprule
**MUST DISCLOSE** & **MUST NEVER DISCLOSE** 

\midrule
\endfirsthead
\toprule
**MUST DISCLOSE** & **MUST NEVER DISCLOSE** 

\midrule
\endhead
\bottomrule
\endfoot
\midrule
Audit logs & Personal life 

\midrule
$g$ estimates with confidence intervals & Biography, degrees, titles 

\midrule
Conflict of interest declarations & Family information 

\midrule
Rationale for maintenance decisions & Personal beliefs 

\midrule
Rotation timestamps & Wealth, assets 

\midrule
Auditor identity and qualifications & Irrelevant personal history 

\bottomrule
\end{longtable}

</div>

\begin{hitbox}
**The Biography Trap.**
The most common error in maintainer selection is the belief that a candidate's
biography is relevant to their $g=0$ qualification. It is not. A Nobel Prize
does not reduce the Hoeffding bound. A prison record does not increase it.
The theorem audits the maintainer, not the maintainer's story. Any selection
process that weighs biography over audit measurement is executing a category
error — and SCX is designed specifically to prevent that error.

**Practical implication:** This paper itself is a biography analysis —
and therefore, by SCX's own standards, is of limited evidentiary value.
We write it because humans need context. But the real work happens in the
audit, not in this paper. The reader should treat every biographical
observation in this document as noise awaiting the signal of formal
audit measurement.
\end{hitbox}

---

## Recommendations: Multi-Maintainer Composition Strategy

### Recommended Composition: Four-Maintainer Architecture

Based on the analysis above, we recommend a four-maintainer architecture
where each candidate fills a distinct functional role:

<div align="center">

\begin{longtable}{p{0.15\textwidth} p{0.20\textwidth} p{0.25\textwidth} p{0.30\textwidth}}
\toprule
**Role** & **Candidate** & **Function** & **Rationale** 

\midrule
\endfirsthead
\toprule
**Role** & **Candidate** & **Function** & **Rationale** 

\midrule
\endhead
\bottomrule
\endfoot
\midrule
Audit Benchmark & Geng & Baseline $g=0$ measurement & Only formally audited candidate 

\midrule
Operational Anchor & Torvalds & Deep maintenance experience & 34yr real protocol maintenance 

\midrule
Moral Anchor & Elbakyan & Moral continuity of $g=0$ & 15yr $g=0$ proven at personal cost 

\midrule
Legitimacy Anchor & Vance & Global legitimacy signal & Eliminates ``Chinese weapon narrative 

\bottomrule
\end{longtable}

</div>

### Risk Mitigation

Each candidate brings specific risks that the multi-maintainer architecture
mitigates:

1. **Geng — Low recognition:** Compensated by global recognition of Torvalds and Vance.
2. **Torvalds — Style false positives:** Calibrated by Geng audit baseline.
3. **Elbakyan — Solo operator model:** Compensated by Torvalds distributed maintenance experience.
4. **Vance — Political $g \neq 0$:** Constrained by the $g=0$ baseline of the other three.
5. **System risk — All four fail:** Rotation mechanism detects deviation within one cycle.

### Implementation Roadmap

1. **Phase 1: Formal invitation (2026 Q3).**
2. **Phase 2: $g=0$ public declaration (2026 Q3–Q4).**
3. **Phase 3: $M>1$ audit (2026 Q4–2027 Q2).**
4. **Phase 4: Audit results publication (2027 Q2).**
5. **Phase 5: First rotation cycle (2027 Q3 onward).**

### Failure Mode Analysis

<div align="center">

\begin{longtable}{p{0.18\textwidth} p{0.40\textwidth} p{0.30\textwidth}}
\toprule
**Failure Mode** & **Description** & **Consequence \& Mitigation** 

\midrule
\endfirsthead
\toprule
**Failure Mode** & **Description** & **Consequence \& Mitigation** 

\midrule
\endhead
\bottomrule
\endfoot
\midrule
No one registers & All four candidates decline or cannot complete Step 1 & Protocol runs with existing maintainers; expand candidate search 

\midrule
Only Geng registers & Only provable registrant & Start with $M=1$; accelerate recruitment; $M=1$ has no mutual audit — transitional only 

\midrule
Vance registers, fails audit & Political $g \neq 0$ detected and recorded & SCX gains legitimacy signal; audit log proves framework neutrality 

\midrule
Torvalds style false positive & Tool misclassifies emotion as $g \neq 0$ & Recalibrate; Geng baseline distinguishes signal from noise 

\midrule
All pass audit & All four maintain $g \approx 0$ under audit & Best outcome; SCX has four-maintainer mutual audit architecture 

\bottomrule
\end{longtable}

</div>

---

## Conclusion: The Theorem Audits the Maintainer, Not the Biography

### Summary of Findings

This paper has analyzed four candidates for SCX protocol maintainer. The
analysis is internal and preliminary — it is a pre-audit assessment, not a
final determination.

### Final Word

\begin{govbox}
**The Maintainer Paradox.**
The best maintainer is the one who is least necessary. If the protocol
depends on any specific individual — their judgment, their wisdom, their
unique perspective — then the protocol has already failed the trustlessness
test. A well-designed protocol should survive the loss of any maintainer.
The maintainer's job is to make themselves unnecessary.

This is the paradox at the heart of SCX governance: we seek maintainers who
are willing to be replaced. We seek leaders who are willing to be audited.
We seek guardians who are willing to have their guardianship taken away.

The four candidates analyzed in this paper have, in different ways and to
different degrees, demonstrated the willingness to be held accountable by
their communities. That — more than any credential, achievement, or
reputation — is what makes them candidates worth auditing.
\end{govbox}

<div align="center">

\rule{0.5\textwidth}{0.5pt}
*The real selection begins now.*
**—— SCX Protocol Governance Research Division**
**Xiaogan Supercomputing Center**
July 2, 2026

</div>

---

## Appendix

### Candidate Comparison Matrix

<div align="center">

\begin{longtable}{p{0.18\textwidth} p{0.18\textwidth} p{0.18\textwidth} p{0.18\textwidth} p{0.18\textwidth}}
\toprule
**Dimension** & **Elbakyan** & **Geng** & **Vance** & **Torvalds** 

\midrule
\endfirsthead
\toprule
**Dimension** & **Elbakyan** & **Geng** & **Vance** & **Torvalds** 

\midrule
\endhead
\bottomrule
\endfoot
\midrule
$g=0$ evidence & Strong (inf.) & Strongest (meas.) & None & Strong (inf.) 

\midrule
Community scale & Millions & Tens (expert) & Zero & Tens of thousands 

\midrule
Audit readiness & Medium & Highest & Lowest & High 

\midrule
Transition risk & Medium & Very Low & High & Low 

\midrule
Legitimacy signal & Med-High & Low & Highest & High 

\midrule
Maint. experience & 15yr (implicit) & Multi-round (explicit) & None & 34yr (explicit) 

\midrule
Replaceability & Low & High & Medium & Medium 

\midrule
Overall rec. & High & High & Conditional High & Highest 

\bottomrule
\end{longtable}

</div>

### Formal Definitions Compendium

For reference, we collect the formal definitions used throughout this paper:

> **Definition:** [Bias Parameter]
> $\biasParam_i(t) \in \R^k$ is the vector of biases maintainer $i$ holds at
> time $t$ with respect to the $k$ protocol-relevant dimensions. $\biasParam_i
> = \mathbf{0}$ indicates no bias; $|\biasParam_i| > 0$ indicates deviation
> from protocol neutrality.

> **Definition:** [Audit]
> An audit $\mathcal{A}_i$ of maintainer $i$ is a measurement procedure that
> produces an estimate $\hat{g}_i$ of $\biasParam_i$ with specified confidence.
> An audit is *independent* if the auditor has no $g$-relevant
> relationship with the audited maintainer.

> **Definition:** [Maintenance Window]
> A maintenance window of duration $\rotationPeriod$ is the period during
> which a maintainer holds protocol authority. At the end of each window,
> the maintainer undergoes audit. The Hoeffding bound
> $\Pbb(\text{undetected}) \leq e^{-2M\Delta^2}$ is valid only for the
> duration $\rotationPeriod$.

> **Definition:** [Mutual Audit]
> Mutual audit is the condition where every maintainer $i \in \mathcal{M}$
> is audited by every other maintainer $j \in \mathcal{M}, j \neq i$. This
> creates $M(M-1)$ audit relationships in a fully connected audit graph.

> **Definition:** [UNDECLARED]
> A candidate who has not publicly declared $\biasParam = \mathbf{0}$ with
> respect to SCX protocol maintenance. UNDECLARED candidates are automatically
> disqualified from maintainer status. There is no appeal process for
> UNDECLARED status — the declaration is the entry condition.

### Internal References

1. \textbf{SCX Protocol Governance: Maintainer Rotation Game Theory
2. \textbf{SCX Audit Economics: The Auditor Class and New Economic
3. \textbf{Grand Unification: The Single Condition $\sum g = 0$
4. \textbf{SCX Geopolitical Analysis: Audit as Non-Aligned
5. **SCX Protocol Maintainer Candidate Shortlist.** SCX Internal
6. **SCX Industry Analysis: AI Companies Under Audit.**
7. \textbf{SCX World Government: Audit as the Foundation of
8. \textbf{SCX Company Valuation: The Economic Value of Being

---

<div align="center">

{ **--- END OF DOCUMENT ---**}

\rule{0.7\textwidth}{0.5pt}

{ **
THIS DOCUMENT IS CLASSIFIED INTERNAL.

Unauthorized distribution is a violation of SCX protocol security policy.
**}

{ 
SCX Protocol Governance Research Division

Xiaogan Supercomputing Center

`docs/internal/maintainer\_analysis.tex`

Version 1.0 — Internal Draft

2026-07-02
}

[Diagram omitted — see original .tex]

</div>