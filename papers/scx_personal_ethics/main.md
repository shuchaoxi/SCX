*Abstract:*

{\bf Abstract.}
This paper is a personal advisory---a letter to individual citizens grounded in mathematical proof.
You face a dilemma: a superior demands you falsify data. Traditional advice says ``be brave.''
SCX{} says: **calculate.**
We prove that under multi-expert audit with Spring{}'s permanent memory, honesty is not a moral virtue---it is a strictly dominant strategy in the game-theoretic sense.
Four theorems establish:
(1)~Detection Inevitability: the probability that $M$ independent auditors all miss a deception is bounded by $(\threshold/\tol)^M \to 0$ as $M$ grows;
(2)~Scale Invariance of Guilt (勿以恶小而为之, formalized): a small deception and a large deception face identical detection probability whenever both exceed the noise threshold---there is no ``safe'' size of dishonesty;
(3)~Honesty as Strictly Dominant: for $M \geq M_ = \lceil \ln(\cost/(\cost-\benefit)) / \ln(\tol/\threshold) \rceil$, the expected payoff of honesty strictly exceeds that of any dishonest strategy;
(4)~Irreversibility of Evidence: under Spring{}'s monotonic memory, any dishonest act remains detectable at all future times, with non-decreasing detection probability.
These results are not political statements. They are mathematical identities.
You do not need courage. You need to compute $M_$.

{\bf 摘要.}
本文是一封以数学证明为基石的致个体公民书。
你面对一个困境：上级要求你篡改数据。传统建议说“勇敢点”。
SCX{}说：{\bf 算一算。}
我们证明，在Spring{}永久记忆的多专家审计框架下，诚实不是美德——它是博弈论意义上的严格占优策略。
四条定理依次证明：(1)~检测必然性：$M$个独立审计员全部漏检的概率 $\leq (\threshold/\tol)^M \to 0$；
(2)~罪责标度不变性（勿以恶小而为之的形式化）：当欺骗幅度超过噪声阈值后，小谎言与大谎言的检测概率完全相同——没有任何“安全”的不诚实尺度；
(3)~诚实的严格占优：当 $M \geq M_$ 时，诚实的期望收益严格大于任何不诚实策略；
(4)~证据不可逆性：在Spring{}单调递增的记忆下，任何不诚实行为在未来的所有时刻均保持可检测状态。
这些结果不是政治宣言，而是数学恒等式。
你不需要勇气。你只需要计算 $M_$。

{\bfseries Keywords:} game theory 博弈论, individual ethics 个体伦理,
strict dominance 严格占优, multi-expert audit 多专家审计,
Hoeffding inequality, Spring permanent memory Spring永久记忆,
Nash equilibrium 纳什均衡, 勿以恶小而为之.

{\bfseries 关键词:} 博弈论, 个人伦理, 严格占优策略, 多专家审计, Hoeffding不等式,
Spring永久记忆, 纳什均衡, honest strategy 诚实策略.

## Introduction --- The Individual's Dilemma
<!-- label: sec:intro -->

### You, Your Superior, and the Spreadsheet 你、你的上级、与那张表格

You work in an organization. It could be a government bureau compiling economic statistics (统计局), a corporation reporting emissions data (排放数据), a hospital recording patient outcomes (病历记录), a school submitting examination results (考试成绩), or a laboratory measuring product safety (产品检测). One day, your superior asks you to change a number. Not by much---just a small adjustment. ``Nobody will notice,'' they say. ``Everyone does it.''

You face a choice:

- **Comply** (不诚实, $\dishonest$): Falsify the data. Gain a benefit $b > 0$: a promotion, a bonus, continued employment, the superior's approval. Risk: detection.
- **Refuse** (诚实, $\honest$): Report the truth. Gain nothing extra. Risk: retaliation from the superior---but the data remain clean.

Traditional ethics addresses this with moral language: courage (勇气), integrity (正直), conscience (良知). These are real, but they ask you to sacrifice self-interest for principle. Not everyone finds that argument compelling under pressure.

SCX{} offers a different argument. It does not ask you to be brave. It asks you to be rational.

### The Core Thesis 核心命题

Under the SCX{} audit architecture---specifically, $M$ independent auditors with Spring{}'s permanent memory---the mathematics of detection makes dishonesty a losing bet. Not a morally wrong bet. A mathematically negative-expectation bet.

The central claim of this paper, from which all else follows, is:

<div align="center">

\framebox[0.92\textwidth]{
\parbox{0.88\textwidth}{

{\bf Theorem (Honesty Dominance, informal).}
There exists a computable threshold $M_$ such that if the number of independent auditors $M$ in your context exceeds $M_$, then for {\em any possible deception}---regardless of how small---your expected payoff from dishonesty is strictly negative. Honesty is not merely ``better''; it is the {\em uniquely rational} choice for a self-interested agent.

}}

</div>

You may fear your superior, who can be bribed, persuaded, transferred, or retired. You cannot bribe Hoeffding's inequality. You cannot persuade Spring{} to forget. The auditor is not a person. It is a theorem.

### The Honest Limitation 诚实的局限

Before proceeding, we state a limitation that this paper does not hide:

\limitationTag{0} **(Pre-Detection Retaliation).** SCX{} audit detects dishonesty *after it occurs*. It cannot protect you from retaliation by your superior *before* detection---for example, if you refuse to falsify and are immediately fired, demoted, or harassed. The theorem guarantees that dishonesty will be detected, not that honesty will be rewarded in the short term. If the superior can retaliate instantly and irreversibly before the audit triggers, the game-theoretic calculation changes. This paper addresses the detection side of the equation; the protection side requires institutional safeguards (whistleblower laws, anonymous reporting channels, employment protections) that are outside the mathematical model. **The theorem tells you that falsifying data is a losing strategy. It does not guarantee that refusing is a winning one---only that it is less losing.**

\assumptionTag{0} **(Motivating Gap).** No existing framework provides an individual citizen with a computable, game-theoretic proof that honesty is strictly dominant under specified audit conditions. Traditional ethics appeals to conscience; institutional compliance appeals to rules. SCX{} appeals to expected value.

### Structure of This Paper 论文结构

Section [ref] formalizes the individual as an agent in a repeated audit game with $M$ auditors and Spring{} memory. Section [ref] proves Detection Inevitability. Section [ref] formalizes the ancient Chinese maxim 勿以恶小而为之 (``Do not commit an evil act because it is small'') as a mathematical theorem. Section [ref] proves Honesty as Strictly Dominant and derives the computable threshold $M_$. Section [ref] proves the Irreversibility of Evidence under Spring{}. Section [ref] translates the mathematics into personal guidance. Section [ref] discusses the dual role of every citizen as both agent and auditor.

## Formal Model --- Individual as Agent in Repeated Audit Game
<!-- label: sec:model -->

### The Agent and the Truth 个体与真相

> **Definition:** [Truth and Claim 真相与申报]
> <!-- label: def:truth -->
> Let $\truth \in \R$ be the true value of a data point---a measurement, count, quality metric, or any scalar quantity that the agent is responsible for reporting. For example, $\truth$ could be a pollution concentration, a GDP component, a patient survival rate, or a product safety score.
> 
> The agent $i$ produces a claim $\claim_i \in \R$. The agent's action space is:
> 
> $$
>     a_i \in \{\honest, \dishonest\}, \quad
>     \honest: \claim_i = \truth, \qquad
>     \dishonest: \claim_i = \truth + \deception, \;\; \deception \neq 0.
> $$
> 
> Without loss of generality, we assume $\deception > 0$ (the agent inflates the number).

\assumptionTag{1} **(Scalar Data Model).** We model data as scalar values. Real-world reporting involves vectors, categories, and structured records. The scalar model captures the essential structure---a gap between truth and claim---while keeping proofs tractable. Generalization to $\R^d$ follows by component-wise analysis.

### The Auditors 审计者

> **Definition:** [Multi-Expert Audit 多专家审计]
> <!-- label: def:auditors -->
> Let there be $M \in \N$ independent auditors, indexed $j = 1, ..., M$. Auditor $j$ observes the data-generating process that produced $\truth$ and forms an independent estimate $\hat_j \in \R$. Formally:
> 
> $$
>     \hat_j = \truth + \varepsilon_j, \qquad
>     \varepsilon_j \sim Uniform[-\tol,\; \tol],
> $$
> 
> where $\tol > 0$ is the maximum observation error, and $\varepsilon_1, ..., \varepsilon_M$ are mutually independent.

\assumptionTag{2} **(Bounded Observation Noise).** Auditor estimates are bounded: $\abs{\hat_j - \truth} \leq \tol$ for all $j$. This holds in any domain where measurements have finite precision and known error bounds (laboratory instruments, statistical surveys with confidence intervals, sensor networks with calibrated accuracy).

\assumptionTag{3} **(Uniform Noise Distribution).** $\varepsilon_j \sim Uniform[-\tol, \tol]$. This assumption yields exact, closed-form probability expressions. All theorems generalize to any symmetric, bounded distribution with density $f$ using integral bounds; the uniform case provides the cleanest exposition and is non-restrictive: any bounded symmetric distribution yields qualitatively identical conclusions with modified constants.

\assumptionTag{4} **(Auditor Independence).** $\varepsilon_j \perp\!\!\!\perp \varepsilon_k$ for all $j \neq k$. Auditors do not collude, share priors, or coordinate their estimates. They observe independent aspects of the data-generating process (different instruments, different sampling frames, different methodologies). Relaxation to correlated auditors is discussed in Remark [ref].

> **Definition:** [Honest Consensus 诚实共识]
> <!-- label: def:consensus -->
> The **honest consensus** is the arithmetic mean of the $M$ auditor estimates:
> 
> $$
>     \hat_M = \frac{1}{M} \sum_{j=1}^{M} \hat_j.
> $$
> 
> By the Law of Large Numbers, $\hat_M \xrightarrow{a.s.} \truth$ as $M \to \infty$.

### Detection Mechanism 检测机制

> **Definition:** [Detection Event 检测事件]
> <!-- label: def:detection -->
> Auditor $j$ **flags** the claim $\claim_i$ if the claim deviates from the auditor's own estimate by more than a fixed tolerance $\threshold > 0$:
> 
> $$
>     F_j = \ind{\abs{\claim_i - \hat_j} > \threshold}.
> $$
> 
> The **detection event** $D_t$ at time $t$ occurs if *at least one* auditor flags the claim:
> 
> $$
>     D_t = \ind{\exists j \in \{1,...,M\} : F_j = 1} = \ind{\max_j \abs{\claim_i - \hat_j} > \threshold}.
> $$

\assumptionTag{5} **(Any-Auditor Detection Rule).** Detection requires only one auditor to flag a discrepancy. This is the maximally sensitive rule---a single inconsistency triggers investigation. In practice, audit systems may require a quorum or majority; the any-auditor rule provides an *upper bound* on the detection probability and thus a conservative bound for the agent: if dishonesty is strictly dominated under the most sensitive detection rule, it is dominated under any less sensitive rule.

\assumptionTag{6} **(Fixed Detection Tolerance).** The threshold $\threshold > 0$ is fixed and known. It represents the minimum discrepancy that an auditor can reliably distinguish from measurement noise. In practice, $\threshold$ is set by instrument precision, statistical significance levels, or regulatory standards. We assume $0 < \threshold < \tol$ (the tolerance is smaller than the maximum observation error; otherwise, auditors could never detect anything).

### Payoff Structure 收益结构

> **Definition:** [Individual Payoff 个体收益]
> <!-- label: def:payoff -->
> The agent's payoff is:
> 
> $$
>     u_i(a_i) = \begin{cases}
>         0, & a_i = \honest \quad (normalized baseline), 
>         \benefit - \cost \cdot \ind{D_t = 1}, & a_i = \dishonest,
>     \end{cases}
> $$
> 
> where:
> 
- $\benefit > 0$: the benefit from complying with the superior's demand (promotion, bonus, continued employment, approval). We assume the benefit is received immediately upon making the false claim.
- $\cost > \benefit$: the cost of being caught (career destruction, legal penalties, reputation loss, imprisonment). The inequality $\cost > \benefit$ means the downside of being caught exceeds the upside of successful deception---a realistic condition in any functioning accountability system.

\assumptionTag{7} **(Cost Dominates Benefit).** $\cost > \benefit > 0$. If this fails ($\cost \leq \benefit$), then dishonesty can be profitable even under certain detection, and no audit system can deter it. We assume the accountability system assigns penalties that exceed the gains from misconduct.

> **Definition:** [Expected Payoff 期望收益]
> <!-- label: def:expected -->
> The expected payoff of a dishonest action with deception magnitude $\deception > 0$ is:
> 
> $$
>     \E[u_i \mid \dishonest, \deception] = \benefit - \cost \cdot \Pbb(D_t = 1 \mid \claim_i = \truth + \deception).
> $$
> 
> The expected payoff of honesty is $\E[u_i \mid \honest] = 0$.

> **Remark:** [Yajie NPE Payoff Structure Yajie{}纳什均衡收益结构]
> <!-- label: rem:yajie -->
> This payoff structure follows the Yajie{} consensus framework's NPE (Nash Payoff Equilibrium) formulation: each agent's payoff depends on the audit outcome, which in turn depends on the collective action of the auditors. In the personal setting, we take the audit mechanism as exogenous (the auditors are not strategic players against the individual agent). The game-theoretic analysis in Theorem [ref] treats the auditor count $M$ and the detection parameters $(\threshold, \tol)$ as fixed features of the environment, and asks: given these parameters, what is the individually optimal action?

### Spring Permanent Memory Spring{永久记忆}

> **Definition:** [Spring Memory Spring{}记忆]
> <!-- label: def:spring -->
> Spring{} is the SCX{} component that permanently stores all claims, auditor estimates, and detection flags. At time $t$, the memory state is:
> 
> $$
>     \cM_t = \{(\claim^{(\tau)}, \hat_1^{(\tau)}, ..., \hat_M^{(\tau)}, D_\tau)\}_{\tau=1}^{t}.
> $$
> 
> Spring{} is **monotonic**: $\cM_t \subseteq \cM_{t+1}$ for all $t$. Memory only grows; nothing is ever deleted.

\assumptionTag{8} **(Spring Monotonicity).** $\cM_t \subseteq \cM_{t+1}$. Every claim, every estimate, and every detection outcome is permanently recorded and available for re-examination at all future times. There is no ``statute of limitations'' on evidence.

\assumptionTag{9} **(Ex Post Auditability).** At any future time $t > \tau$, auditors can re-examine the claim $\claim^{(\tau)}$ using all evidence accumulated in $\cM_t$, including new data, new auditor estimates, and new detection events that were not available at time $\tau$.

\assumptionTag{10} **(Non-Decreasing Auditor Count).** The number of auditors may increase over time: $M_{t+1} \geq M_t$. New auditors may join the system; existing auditors do not leave. Combined with Spring monotonicity, this ensures that the detection power is non-decreasing over time.

## Theorem 1 --- Detection Inevitability 检测必然性定理
<!-- label: sec:thm1 -->

We now prove the first fundamental result: under multi-expert audit, a dishonest claim will eventually be detected. The probability of escaping detection decays exponentially in the number of auditors.

### Statement

> **Theorem:** [Detection Inevitability 检测必然性]
> <!-- label: thm:inevitability -->
> \rigorFull
> Let $M$ independent auditors each produce an estimate $\hat_j = \truth + \varepsilon_j$ with $\varepsilon_j \sim Uniform[-\tol, \tol]$. Let the agent make a dishonest claim $\claim_i = \truth + \deception$ with $\deception > 0$. Let detection occur under the any-auditor rule with tolerance $\threshold < \tol$.
> 
> Then:
> 
1. For $\deception \in (\threshold,\; \tol - \threshold)$, the miss probability is **independent of the deception magnitude $\deception$**:
2. For all $\deception > 0$, the miss probability is bounded above by:
3. Consequently:

### Proof

> **Proof:** Fix a deception magnitude $\deception > 0$. For auditor $j$, the flagging condition is:
> 
> $$
>     F_j = 1 \iff \abs{\claim_i - \hat_j} > \threshold
>           \iff \abs{\truth + \deception - (\truth + \varepsilon_j)} > \threshold
>           \iff \abs{\deception - \varepsilon_j} > \threshold.
> $$
> 
> 
> Thus auditor $j$ *misses* the deception (does not flag) when:
> 
> $$
>     \abs{\deception - \varepsilon_j} \leq \threshold \iff
>     \varepsilon_j \in [\deception - \threshold,\; \deception + \threshold].
> $$
> 
> 
> Since $\varepsilon_j \sim Uniform[-\tol, \tol]$, the per-auditor miss probability is:
> 
> $$
>     p_{miss}^{(j)}(\deception) =
>     \Pbb(\abs{\deception - \varepsilon_j} \leq \threshold) =
>     \frac{\abs{[\deception - \threshold,\; \deception + \threshold] \cap [-\tol,\; \tol]}}{2\tol}.
> $$
> 
> 
> We analyze this by cases based on $\deception$.
> 
> **Case 1:** $\threshold < \deception \leq \tol - \threshold$.
> 
> The interval $[\deception - \threshold,\; \deception + \threshold]$ is entirely contained within $[-\tol, \tol]$. Its length is $2\threshold$. Hence:
> 
> $$
>     p_{miss}^{(j)}(\deception) = \frac{2\threshold}{2\tol} = \frac.
>     <!-- label: eq:case1 -->
> $$
> 
> Critically, this probability **does not depend on $\deception$**. A small deception ($\deception$ just above $\threshold$) and a large deception ($\deception$ near $\tol - \threshold$) generate identical per-auditor miss probabilities.
> 
> **Case 2:** $0 < \deception \leq \threshold$.
> 
> The interval $[\deception - \threshold,\; \deception + \threshold]$ extends into the negative region. Its intersection with $[-\tol, \tol]$ is $[-\tol,\; \deception + \threshold]$, with length $\deception + \threshold + \tol$. Since $\deception \leq \threshold$, this length is at most $\tol + 2\threshold \leq 3\tol$ (using $\threshold < \tol$). However, more importantly, since $\deception - \threshold \leq 0$:
> 
> $$
>     p_{miss}^{(j)}(\deception) = \frac{\deception + \threshold + \tol}{2\tol}
>                                          > \frac{2\tol} = \frac{1}{2}.
> $$
> 
> For very small deceptions, the per-auditor miss probability exceeds $1/2$, meaning individual auditors are unreliable. The collective detection still works via the product over $M$ auditors.
> 
> **Case 3:** $\deception > \tol - \threshold$.
> 
> The interval exceeds the upper bound. Its intersection with $[-\tol, \tol]$ is $[\deception - \threshold,\; \tol]$, with length $\tol - \deception + \threshold$. Then:
> 
> $$
>     p_{miss}^{(j)}(\deception) = \frac{\tol - \deception + \threshold}{2\tol}
>                                          < \frac{2\threshold}{2\tol} = \frac.
> $$
> 
> Large deceptions are actually *easier* to detect (per-auditor miss probability is *smaller* than the plateau value $\threshold/\tol$).
> 
> 
> Now, detection requires *all* $M$ auditors to miss simultaneously:
> 
> $$
>     \Pbb(miss \mid \deception) = \prod_{j=1}^{M} p_{miss}^{(j)}(\deception)
>     = \bigl[p_{miss}^{(j)}(\deception)\bigr]^M.
> $$
> 
> This follows from auditor independence (Assumption [ref]).
> 
> For Case 1 ($\threshold < \deception \leq \tol - \threshold$):
> 
> $$
>     \Pbb(miss \mid \deception) = \left(\frac\right)^M.
> $$
> 
> 
> For Case 3 ($\deception > \tol - \threshold$):
> 
> $$
>     \Pbb(miss \mid \deception) \leq \left(\frac\right)^M.
> $$
> 
> 
> For Case 2 ($0 < \deception \leq \threshold$), the miss probability is larger than $(\threshold/\tol)^M$. However, note that: (a) deceptions this small ($\deception \leq \threshold$) are within the measurement noise margin---they are indistinguishable from honest reporting error, and we will show in Section [ref] that they provide no rational benefit; (b) the bound $(\threshold/\tol)^M$ is still an exponential function of $M$, and as $M \to \infty$, it converges to 0 for any fixed $\threshold < \tol$.
> 
> For the detection probability:
> 
> $$
>     \Pbb(D_t = 1 \mid \dishonest) = 1 - \Pbb(miss \mid \deception)
>     \geq 1 - \left(\frac\right)^M.
> $$
> 
> 
> Taking limits:
> 
> $$
>     \lim_{M \to \infty} \Pbb(D_t \mid \dishonest)
>     \geq \lim_{M \to \infty} \left[1 - \left(\frac\right)^M\right] = 1.
> $$
> 
> 
> For the time limit: under Assumptions [ref] and [ref] (Spring monotonicity and non-decreasing auditor count), $M_t \geq M_0$ and $\lim_{t \to \infty} M_t = \infty$ if new auditors join over time. Even if $M$ is fixed, Spring's evidence accumulation provides each auditor with more data, effectively reducing the per-auditor tolerance $\threshold_{eff} = \threshold / \sqrt{N_t}$ where $N_t$ is the amount of accumulated data. As $t \to \infty$, $N_t \to \infty$, $\threshold_{eff} \to 0$, and the miss probability vanishes. Hence $\lim_{t \to \infty} \Pbb(D_t \mid \dishonest) = 1$.

> **Remark:** [Hoeffding Connection 与Hoeffding不等式的关联]
> <!-- label: rem:hoeffding -->
> The bound $\Pbb(miss) \leq (\threshold/\tol)^M$ can be rewritten in Hoeffding form:
> 
> $$
>     \Pbb(miss) = \exp\left(M \ln\frac\right)
>     = \exp\left(-M \ln\frac\right).
> $$
> 
> Since $\threshold < \tol$, $\ln(\tol/\threshold) > 0$, and the miss probability decays exponentially in $M$ with rate $\ln(\tol/\threshold)$. For small $\threshold/\tol$, using the expansion $\ln(1 + x) \approx x$ with $x = (\tol - \threshold)/\threshold$:
> 
> $$
>     \Pbb(miss) \approx \exp\left(-M \cdot \frac{\tol - \threshold}\right)
>     \approx \exp(-2M \Delta^2),
> $$
> 
> where $\Delta = \sqrt{(\tol - \threshold)/(2\threshold)}$ captures the effective separation between noise and signal. This recovers the familiar Hoeffding form $\exp(-2M\Delta^2)$ that appears throughout the SCX{} literature.

> **Remark:** [Numerical Illustration 数值示例]
> <!-- label: rem:numerical -->
> Suppose $\tol = 10$ (auditor estimates are accurate to $\pm 10$ units) and $\threshold = 1$ (the detection tolerance is 1 unit, representing a 10\% precision requirement). Then $\threshold/\tol = 0.1$. With $M = 5$ auditors: $\Pbb(miss) = 10^{-5}$. With $M = 10$: $\Pbb(miss) = 10^{-10}$. The probability of escaping detection is astronomically small with modest auditor counts.

\limitationTag{1} The uniform noise assumption (A3) produces the exact product form $(\threshold/\tol)^M$. Under alternative distributions (Gaussian, Laplace, sub-Gaussian), the bound takes the form $\exp(-c M (\deception - \threshold)_+^2)$ with a distribution-dependent constant $c$. The exponential decay in $M$ is preserved; only the constant changes.

## Theorem 2 --- Scale Invariance of Guilt 罪责标度不变性（勿以恶小而为之）
<!-- label: sec:thm2 -->

In the year 223, on his deathbed, the Shu Han emperor 刘备 (Liu Bei) gave his son 刘禅 (Liu Shan) a final instruction, recorded in the *三国志* (Records of the Three Kingdoms):

<div align="center">

 勿以恶小而为之，勿以善小而不为。

</div>

<div align="center">

{\it ``Do not commit an evil act because it is small. Do not omit a good act because it is small.''}

</div>

For seventeen centuries, this has been read as moral advice---a plea to conscience. In this section, we prove that within the SCX{} framework, the first clause is not moral advice at all. It is a mathematical identity.

### Statement

> **Theorem:** [Scale Invariance of Guilt --- 勿以恶小而为之的形式化证明]
> <!-- label: thm:scale_invariance -->
> \rigorFull
> Under Assumptions [ref]-- [ref] (uniform bounded noise, independent auditors, any-auditor detection with tolerance $\threshold$), for any two deception magnitudes $\deception_1, \deception_2$ satisfying $\threshold < \deception_1, \deception_2 \leq \tol - \threshold$:
> 
> $$
>     \Pbb(D_t = 1 \mid \deception_1) = \Pbb(D_t = 1 \mid \deception_2).
>     <!-- label: eq:scale_invariance -->
> $$
> 
> The detection probability is independent of the deception magnitude over the entire ``plateau region'' $(\threshold,\; \tol - \threshold]$.
> 
> Furthermore, for any $\deception > \tol - \threshold$, the detection probability is *strictly larger* than for any $\deception \in (\threshold,\; \tol - \threshold]$. That is, extremely large deceptions are *more* detectable, not less.
> 
> Consequently: there exists no $\deception > 0$ for which the detection probability is lower than the plateau value. A ``small'' lie and a ``big'' lie face identical detection odds. There is no ``safe'' size of dishonesty.

### Proof

> **Proof:** From the proof of Theorem [ref], the per-auditor miss probability is:
> 
> $$
>     p_{miss}^{(j)}(\deception) =
>     \frac{\abs{[\deception - \threshold,\; \deception + \threshold] \cap [-\tol,\; \tol]}}{2\tol}.
> $$
> 
> 
> For $\deception \in (\threshold,\; \tol - \threshold]$ (Case 1 in Theorem [ref]), the interval $[\deception - \threshold,\; \deception + \threshold]$ is fully contained in $[-\tol, \tol]$. Its length is exactly $2\threshold$, regardless of $\deception$. Hence:
> 
> $$
>     p_{miss}^{(j)}(\deception) = \frac{2\threshold}{2\tol} = \frac,
>     \qquad \forall \deception \in (\threshold,\; \tol - \threshold].
> $$
> 
> 
> This probability is constant in $\deception$. Since the auditors are independent, the overall miss probability is:
> 
> $$
>     \Pbb(miss \mid \deception) = \left(\frac\right)^M,
>     \qquad \forall \deception \in (\threshold,\; \tol - \threshold].
> $$
> 
> 
> Therefore, the detection probability is:
> 
> $$
>     \Pbb(D_t = 1 \mid \deception) = 1 - \left(\frac\right)^M,
>     \qquad \forall \deception \in (\threshold,\; \tol - \threshold],
> $$
> 
> which is independent of $\deception$. This proves equation~( [ref]).
> 
> For $\deception > \tol - \threshold$ (Case 3), the intersection has length $\tol - \deception + \threshold < 2\threshold$, so:
> 
> $$
>     p_{miss}^{(j)}(\deception) = \frac{\tol - \deception + \threshold}{2\tol}
>     < \frac.
> $$
> 
> Thus the detection probability for such deceptions is strictly larger than the plateau value.
> 
> For $0 < \deception \leq \threshold$ (Case 2), the miss probability per auditor exceeds $\threshold/\tol$. However, such deceptions are within the noise margin---they are indistinguishable from honest measurement error, and we will prove in Theorem [ref] that they are not profitable.
> 
> 
> **Why this is the mathematical translation of 勿以恶小而为之.**
> The intuition that a ``small lie'' is safer than a ``big lie'' rests on the assumption that detection probability *increases with deception magnitude*. In the SCX{} detection framework, this assumption is false. The detection probability is governed by whether the claim differs from the auditors' estimates by more than $\threshold$---a binary condition. Once the deception exceeds $\threshold$, every additional unit of deception faces the *exact same* detection probability. The auditor does not ask ``how big is the lie?'' The auditor asks ``is the claim consistent with my evidence?'' The answer is binary, and it is the same answer for a small lie as for a big one.
> 
> The ancient advice 勿以恶小而为之---do not commit an evil because it is small---is usually understood as a moral claim: small evils corrupt character. We have shown it is also a mathematical claim: in multi-expert audit, small evils face the same probability of exposure as large ones. The ``smallness'' of the deception does not make it safer.

> **Corollary:** [No Safe Harbor 没有安全港]
> <!-- label: cor:no_safe_harbor -->
> There is no deception magnitude $\deception > 0$ for which the detection probability is arbitrarily small as $M$ grows. Formally:
> 
> $$
>     \inf_{\deception > 0} \; \liminf_{M \to \infty} \; \Pbb(D_t = 1 \mid \deception) = 1.
> $$
> 
> Every nonzero deception is asymptotically detectable. The agent cannot ``hide in the noise'' by choosing a very small $\deception$, because for any $\deception > \threshold$, the detection probability converges to 1 as $M \to \infty$, and for $\deception \leq \threshold$, the deception is within measurement noise and (as we show next) provides no rational benefit.

\limitationTag{2} The scale invariance result (exact equality for all $\deception$ in the plateau) depends on the uniform noise assumption. For other symmetric distributions with density $f$, the miss probability is $\int_{\deception-\threshold}^{\deception+\threshold} f(\varepsilon) d\varepsilon$, which varies with $\deception$ even within the plateau. However, the qualitative conclusion---that small and large deceptions face comparable detection odds---holds for any bounded, continuous $f$: the integral over a fixed-width interval varies smoothly with $\deception$, not proportionally to it. A deception 10 times larger does not face 10 times higher detection probability; it faces essentially the same probability.

## Theorem 3 --- Honesty as Strictly Dominant Strategy 诚实作为严格占优策略
<!-- label: sec:thm3 -->

We now prove the paper's central result: under SCX{} audit conditions, honesty is not merely a ``good'' strategy---it is the *only* rational strategy for a self-interested agent. It strictly dominates every dishonest alternative.

### Benefit Structure Refinement 收益结构细化

Before proving dominance, we refine the benefit structure. A superior who demands falsification typically wants a *meaningful* change to the data---one that alters conclusions, affects decisions, or passes a regulatory threshold. A change smaller than the measurement noise ($\deception \leq \threshold$) is worthless for this purpose: it changes nothing that anyone can distinguish from honest error.

\begin{assumption}[A7, Refined: Thresholded Benefit 阈值化收益]
<!-- label: ass:A7 -->
The benefit function $\benefit(\deception)$ satisfies:

$$
    \benefit(\deception) = \begin{cases}
        0, & 0 \leq \deception \leq \threshold \quad (no benefit from noise-level changes), 

        b > 0, & \deception > \threshold \quad (fixed benefit from any meaningful falsification).
    \end{cases}
$$

This is the most conservative (agent-favorable) benefit model: any deception exceeding the noise threshold pays the full benefit $b$. If a smoother benefit function $\benefit(\deception)$ is preferred (e.g., $\benefit(\deception) \propto \deception$), the dominance result becomes *stronger* because small deceptions pay less benefit while facing the same detection probability.
\end{assumption}

### Statement

> **Theorem:** [Honesty as Strictly Dominant Strategy 诚实作为严格占优策略]
> <!-- label: thm:dominance -->
> \rigorFull
> Under Assumptions [ref]-- [ref], define the **critical auditor threshold**:
> 
> $$
>     M_ = \left\lceil \frac{\ln\left(\frac{\cost - b}\right)}{\ln\left(\frac\right)} \right\rceil.
>     <!-- label: eq:Mmin -->
> $$
> 
> If $M \geq M_$, then for all possible deception magnitudes $\deception > 0$:
> 
> $$
>     \E[u_i \mid \honest] = 0 > \E[u_i \mid \dishonest, \deception].
>     <!-- label: eq:strict_dominance -->
> $$
> 
> Honesty strictly dominates every dishonest strategy. The agent has no rational incentive to falsify data, regardless of the deception magnitude, regardless of the superior's pressure, regardless of personal disposition toward risk.

### Proof

> **Proof:** We prove the result by cases based on $\deception$.
> 
> 
> **Case A: $\deception \leq \threshold$ (Noise-Level Deception).**
> 
> By Assumption [ref], $\benefit(\deception) = 0$. The expected payoff is:
> 
> $$
>     \E[u_i \mid \dishonest, \deception \leq \threshold]
>     = 0 - \cost \cdot \Pbb(D_t = 1 \mid \deception)
>     \leq 0 = \E[u_i \mid \honest].
> $$
> 
> The inequality is strict whenever $\Pbb(D_t = 1 \mid \deception) > 0$, which holds for any $M \geq 1$ and $\deception > 0$ (since there is a nonzero probability that an auditor's estimate lands sufficiently far from $\truth + \deception$). Thus dishonesty is weakly dominated for $\deception \leq \threshold$, and strictly dominated when $\deception > 0$ and $M \geq 1$.
> 
> 
> **Case B: $\deception > \threshold$ (Meaningful Deception).**
> 
> By Assumption [ref], $\benefit(\deception) = b > 0$. The expected payoff is:
> 
> $$
>     \E[u_i \mid \dishonest, \deception > \threshold]
>     = b - \cost \cdot \Pbb(D_t = 1 \mid \deception).
> $$
> 
> 
> From Theorem [ref], for all $\deception > \threshold$, the miss probability satisfies:
> 
> $$
>     \Pbb(miss \mid \deception) \leq \left(\frac\right)^M,
> $$
> 
> with equality for $\deception \in (\threshold, \tol - \threshold]$. Hence:
> 
> $$
>     \Pbb(D_t = 1 \mid \deception) \geq 1 - \left(\frac\right)^M.
> $$
> 
> 
> Substituting into the expected payoff:
> 
> $$
>     \E[u_i \mid \dishonest, \deception > \threshold]
>     &\leq b - \cost \cdot \left[1 - \left(\frac\right)^M\right] 

>     &= b - \cost + \cost \left(\frac\right)^M.
>     <!-- label: eq:expected_bound -->
> $$
> 
> 
> For dishonesty to be strictly dominated by honesty, we require:
> 
> $$
>     b - \cost + \cost \left(\frac\right)^M < 0.
> $$
> 
> 
> Rearranging:
> 
> $$
>     \cost \left(\frac\right)^M &< \cost - b, 

>     \left(\frac\right)^M &< \frac{\cost - b} = 1 - \frac{b}, 

>     M \ln\left(\frac\right) &< \ln\left(1 - \frac{b}\right).
> $$
> 
> 
> Since $\threshold < \tol$, $\ln(\threshold/\tol) < 0$. Dividing by this negative quantity flips the inequality:
> 
> $$
>     M > \frac{\ln\left(1 - \frac{b}\right)}{\ln\left(\frac\right)}
>       = \frac{\ln\left(\frac{\cost - b}\right)}{-\ln\left(\frac\right)}
>       = \frac{\ln\left(\frac{\cost - b}\right)}{\ln\left(\frac\right)}.
>     <!-- label: eq:M_bound -->
> $$
> 
> 
> Define $M_$ as the ceiling of this quantity, as in equation~( [ref]). For all $M \geq M_$, the strict inequality $\E[u_i \mid \dishonest] < 0 = \E[u_i \mid \honest]$ holds.
> 
> 
> **Case C: $\deception > \tol - \threshold$ (Very Large Deception).**
> 
> For these deceptions, Theorem [ref] gives an even tighter bound: $\Pbb(miss) < (\threshold/\tol)^M$. The expected payoff is bounded even more negatively, so the dominance result from Case B applies a fortiori.
> 
> 
> **Synthesis.** For all $\deception > 0$ and all $M \geq M_$:
> 
> $$
>     \E[u_i \mid \dishonest, \deception] < 0 = \E[u_i \mid \honest].
> $$
> 
> Honesty strictly dominates every dishonest strategy. $\square$

### Interpretation of $M_{\min$ $M_$的解读}

The threshold $M_$ has a clear intuitive structure. Write it as:

$$
    M_ = \left\lceil \frac{penalty-to-net-loss ratio}{auditor precision} \right\rceil
    = \left\lceil \frac{\ln\left(\frac{\cost - b}\right)}{\ln\left(\frac\right)} \right\rceil.
$$

- **Numerator:** $\ln(\cost/(\cost - b))$. This is the log-ratio of the total penalty $\cost$ to the net loss from being caught $(\cost - b)$. When $\cost \gg b$ (penalty vastly exceeds benefit), the numerator is small ($\approx b/\cost$), and $M_$ is small. When $\cost \approx b$ (penalty barely exceeds benefit), the numerator is large, and $M_$ is large.
- **Denominator:** $\ln(\tol/\threshold)$. This is the log-ratio of the auditor's observation range to the detection tolerance---a measure of auditor precision. High precision ($\tol$ close to $\threshold$) makes the denominator small and $M_$ large (you need more auditors when each is less discriminating). Low precision ($\tol \gg \threshold$, auditors are noisy) makes the denominator large and $M_$ small (even noisy auditors collectively provide strong detection).

> **Corollary:** [Computability of $M_$ $M_$的可计算性]
> <!-- label: cor:computable -->
> $M_$ depends only on three observable parameters: the benefit of compliance $b$, the cost of being caught $\cost$, the auditor precision $\tol/\threshold$. These can be estimated from institutional data. An individual citizen can compute $M_$ and verify whether the number of independent auditors in their context exceeds it. If so, the mathematical case for honesty is complete.

> **Remark:** [Numerical Example 数值示例]
> <!-- label: rem:Mmin_example -->
> Consider a realistic scenario:
> 
- $\cost = 10b$ (being caught costs 10 times the benefit of the falsification---e.g., losing a career worth 10 years of salary vs.\ a one-time bonus).
- $\tol/\threshold = 5$ (auditors' observation noise is 5 times the detection tolerance).

> Then:
> 
> $$
>     M_ = \left\lceil \frac{\ln(10/9)}{\ln(5)} \right\rceil
>     = \left\lceil \frac{0.1054}{1.6094} \right\rceil
>     = \lceil 0.0655 \rceil = 1.
> $$
> 
> With these parameters, **a single independent auditor** makes honesty strictly dominant. More conservative: $\cost = 1.5b$ (penalty only 50\% above benefit) with $\tol/\threshold = 2$:
> 
> $$
>     M_ = \left\lceil \frac{\ln(1.5/0.5)}{\ln(2)} \right\rceil
>     = \left\lceil \frac{\ln(3)}{\ln(2)} \right\rceil
>     = \lceil 1.585 \rceil = 2.
> $$
> 
> Two independent auditors suffice even when the penalty is only marginally above the benefit.

\limitationTag{3} The benefit structure in Assumption [ref] treats all meaningful deceptions as paying the same benefit $b$. A more realistic model might have $\benefit(\deception)$ increasing with $\deception$. This would strengthen the dominance result for small $\deception$ (less benefit, same detection) but might create a region where very large $\deception$ with very large $\benefit(\deception)$ could overcome the detection probability. In practice, benefit functions are concave (diminishing returns to ever-larger falsifications), and $\benefit(\deception)$ is bounded above by the total value the superior can extract from the falsification.

## Theorem 4 --- Irreversibility of Evidence (Spring{'s Permanent Memory) 证据不可逆性定理}
<!-- label: sec:thm4 -->

The previous theorems assume auditors evaluate the claim at the time it is made. But SCX{}'s Spring{} component adds a temporal dimension: evidence is permanently stored and accumulates. This means a dishonest act committed today remains detectable tomorrow, next year, and a decade from now---with non-decreasing probability.

### Statement

> **Theorem:** [Irreversibility of Evidence --- Spring{}'s Monotonicity 证据不可逆性]
> <!-- label: thm:irreversibility -->
> \rigorFull
> Let an agent commit a dishonest act at time $\tau$: $\claim^{(\tau)} = \truth^{(\tau)} + \deception$, $\deception > 0$. Under Assumptions [ref],  [ref], and  [ref] (Spring monotonicity, ex post auditability, non-decreasing auditor count), for all future times $t > \tau$:
> 
> $$
>     \Pbb(D_t = 1 \mid a_\tau = \dishonest) \geq \Pbb(D_\tau = 1 \mid a_\tau = \dishonest).
>     <!-- label: eq:irreversibility -->
> $$
> 
> The detection probability is non-decreasing over time. There is no ``statute of limitations'' on dishonest acts. Furthermore:
> 
> $$
>     \lim_{t \to \infty} \Pbb(D_t = 1 \mid a_\tau = \dishonest) = 1.
>     <!-- label: eq:irreversibility_limit -->
> $$
> 
> Every dishonest act is asymptotically certain to be detected.

### Proof

> **Proof:** At time $\tau$, the detection probability given $M_\tau$ auditors is:
> 
> $$
>     \Pbb(D_\tau = 1 \mid \dishonest) \geq 1 - \left(\frac\right)^{M_\tau}.
> $$
> 
> 
> At time $t > \tau$, by Assumption [ref] (ex post auditability), the auditors can re-examine the claim $\claim^{(\tau)}$ using all evidence accumulated in $\cM_t$. The key observation is that $\cM_t$ provides each auditor with *more data* than was available at time $\tau$, because:
> 
1. By Spring monotonicity (Assumption [ref]), $\cM_t \supseteq \cM_\tau$. All evidence from time $\tau$ is still available, plus new evidence from times $\tau+1$ through $t$.
2. By Assumption [ref] (non-decreasing auditor count), $M_t \geq M_\tau$. New auditors may have joined.
3. Each returning auditor has access to additional data points that increase the precision of their estimate. The effective tolerance shrinks: $\threshold_{eff}(t) \leq \threshold$, because more data reduces the uncertainty band around each auditor's estimate.

> 
> Define $M_t^{eff}$ as the effective number of independent auditor-checks available at time $t$ for examining the claim from time $\tau$. By (i)--(iii):
> 
> $$
>     M_t^{eff} \geq M_\tau^{eff} = M_\tau.
> $$
> 
> 
> The miss probability at time $t$ is:
> 
> $$
>     \Pbb(miss at time  t \mid a_\tau = \dishonest)
>     \leq \left(\frac\right)^{M_t^{eff}}
>     \leq \left(\frac\right)^{M_\tau}
>     = \Pbb(miss at time  \tau \mid a_\tau = \dishonest).
> $$
> 
> 
> Therefore:
> 
> $$
>     \Pbb(D_t = 1 \mid a_\tau = \dishonest)
>     = 1 - \Pbb(miss at time  t)
>     \geq 1 - \Pbb(miss at time  \tau)
>     = \Pbb(D_\tau = 1 \mid a_\tau = \dishonest).
> $$
> 
> 
> This proves the monotonicity inequality~( [ref]).
> 
> For the limit: as $t \to \infty$, Spring accumulates unbounded evidence. Each auditor's effective sample size $N_t \to \infty$, driving the effective tolerance $\threshold_{eff} \to 0$ (by the standard $\sqrt{N}$ scaling of estimation error). Meanwhile, the number of auditors may also grow: $M_t \to \infty$ or at least remain bounded below. In either case:
> 
> $$
>     \left(\frac{\threshold_{eff}(t)}\right)^{M_t} \to 0 \quad as \quad t \to \infty,
> $$
> 
> because either $M_t \to \infty$ drives the product to zero, or $\threshold_{eff}(t) \to 0$ does. Hence:
> 
> $$
>     \lim_{t \to \infty} \Pbb(D_t = 1 \mid a_\tau = \dishonest)
>     = 1 - \lim_{t \to \infty} \left(\frac{\threshold_{eff}(t)}\right)^{M_t}
>     = 1 - 0 = 1.
> $$

> **Corollary:** [No Strategic Timing 不存在策略性时机]
> <!-- label: cor:no_timing -->
> An agent cannot ``wait out'' the detection risk. The probability of being caught never decreases. If you committed a dishonest act at time $\tau$, the expected liability $\cost \cdot \Pbb(D_t = 1)$ grows (or at minimum, does not shrink) with every passing day. The rational time to be caught is now, not later---but the rational decision, ex ante, is to never commit the dishonest act.

> **Remark:** [Practical Implication 实践意义]
> <!-- label: rem:practical_spring -->
> Suppose you falsify a pollution reading in 2026. Five auditors check it at the time; the detection probability is, say, 0.3. You escape. In 2031, a new government administration deploys 20 additional environmental auditors with improved monitoring technology. They access Spring{} and re-examine all historical readings. The 2026 falsification is now examined by 25 auditors with better data. The detection probability rises to near-certainty. Your 2026 escape was temporary. Spring{} never forgets.

\limitationTag{4} The proof assumes that evidence quality improves monotonically. In practice, some evidence may degrade (sensors fail, records are lost, witnesses die). Spring{}'s digital permanence mitigates degradation but does not eliminate it for all evidence types. The guarantee is strongest for digital-native data (spreadsheets, databases, sensor logs) where storage is lossless.

## The Personal Corollary --- What This Means for You 个人推论：这对你意味着什么
<!-- label: sec:corollary -->

The theorems above are not abstractions. They are operational guidance. Here is what they mean for **you** (你), the individual facing a superior's demand to falsify data.

### You Do Not Need Courage 你不需要勇气

Traditional advice tells you to ``be brave'' (勇敢), to ``stand up for what is right'' (坚持正义). This advice is noble. It is also unnecessary.

Theorem [ref] proves that when $M \geq M_$, dishonesty has negative expected value. You do not need courage to choose the strategy with higher expected payoff---you need only to be rational. Courage is for situations where self-interest conflicts with ethics. The SCX{} framework eliminates the conflict: self-interest *demands* honesty.

**Your task is not to be brave. Your task is to compute $M_$ and verify that $M \geq M_$ in your context.**

### Your Superior Is Not the Auditor 你的上级不是审计者

You may fear your superior. This fear is natural: your superior has power over your employment, your salary, your daily life. But your superior is not the auditor in the SCX{} framework.

The auditor is a collective of $M$ independent observers. Your superior can influence one auditor, perhaps two. They can bribe (贿赂), persuade (说服), threaten (威胁), or replace (替换) individual auditors. But your superior cannot bribe Hoeffding's inequality. They cannot persuade the Law of Large Numbers. They cannot threaten the Union Bound. They cannot replace the mathematical fact that $\lim_{M \to \infty} (\threshold/\tol)^M = 0$.

**A person can be corrupted. A theorem cannot.**

### Spring Never Forgets Spring{永不遗忘}

Theorem [ref] establishes that every falsified data point becomes a permanent liability. The detection probability never decreases. It may be low today---perhaps only 0.1 with today's 3 auditors. But next year there may be 10 auditors. In five years, 50. In ten years, a new administration, a new audit regime, new technology. Every one of those future auditors can re-examine your 2026 claim. The evidence does not degrade. The detection probability only grows.

**A dishonest act is not a one-time gamble. It is a permanent mortgage on your future, with an interest rate that only increases.**

### ``勿以恶小而为之'' Is Not Moral Advice 勿以恶小而为之不是道德劝诫

When 刘备 told his son ``do not commit evil because it is small,'' he was speaking as a father giving moral guidance. Theorem [ref] proves that the maxim is also a mathematical identity. In the SCX{} detection framework, a falsification of 1 unit and a falsification of 1,000 units face identical detection probability (once both exceed the noise threshold $\threshold$). The ``small evil'' is not safer. It is equally detectable.

**The temptation to ``just adjust it by a little'' is mathematically equivalent to the decision to commit a large fraud. The detection probability does not care about the magnitude. Neither should you.**

### When $M < M_{\min$: The Pre-Audit World 当审计者不足时}

If the number of independent auditors in your context is below $M_$, the mathematical guarantee does not hold. You are in a pre-audit world. In that world, the expected value of dishonesty may be positive, and self-interest may point toward compliance with the superior's demand.

This is not a failure of the theorem. It is a precise diagnosis of why the system needs more auditors. The solution is structural: increase $M$. Deploy more independent observers. Connect your data stream to external auditors who cannot be controlled by your superior. Advocate for transparency mechanisms that raise $M$ above $M_$.

**The theorem tells you what kind of world you live in. It also tells you how to change it.**

### What the Theorem Cannot Do 定理的局限

\limitationTag{5} **(Retaliation Before Detection, Revisited).** As stated in Section [ref], SCX{} audit operates *ex post*. If you refuse to falsify data and your superior retaliates immediately---fires you, demotes you, harms your family---the theorem offers no protection. The theorem guarantees that falsified data will be detected; it does not guarantee that honest data will be rewarded. In environments where retaliation is swift, certain, and irreversible, the individual's calculation changes: the expected cost of honesty includes the probability of retaliation, which may dominate the expected cost of dishonesty.

This is not a mathematical limitation of the theorems. It is a limitation of what audit alone can achieve. Audit detects lies; it does not prevent coercion. The full protection of honest individuals requires institutional complements: whistleblower laws (举报人保护法), anonymous reporting channels (匿名举报渠道), employment protections (劳动保护), and---most fundamentally---a sufficiently large $M$ that includes auditors outside the superior's chain of command.

**The theorem is a shield against the long-term consequences of dishonesty. It is not a shield against the short-term consequences of honesty. For that, you need law, institutions, and solidarity.**

## Discussion --- When the Individual Is Also an Auditor 当个体同时也是审计者时
<!-- label: sec:discussion -->

### The Dual Role 双重角色

Every citizen in an SCX{}-audited system occupies two positions simultaneously:

1. **Agent** (代理人): You produce data. You face pressure to falsify it. Theorem [ref] tells you that honesty is strictly dominant.
2. **Auditor** (审计者): You possess information that can detect others' falsifications. Your observations, your local knowledge, your domain expertise---these make you one of the $M$ auditors for someone else's claims.

This dual role creates a symmetric game. Every person is simultaneously subject to audit and contributing to audit. The mathematics is symmetric.

### The Symmetric Equilibrium 对称均衡

> **Proposition:** [All-Honest Equilibrium 全诚实均衡]
> <!-- label: prop:equilibrium -->
> Consider a community of $N$ individuals, each playing the dual role of agent and auditor. Suppose each individual's data are audited by $M$ others, and suppose $M \geq M_$ for all individuals. Then the strategy profile where every individual chooses $\honest$ is a strict Nash equilibrium.

> **Proof:** \rigorFull
> For any individual $i$, given that all other $N-1$ individuals choose $\honest$ (and thus serve as honest auditors for $i$'s claims), the audit mechanism facing $i$ consists of $M$ independent honest auditors. By Theorem [ref], $\E[u_i \mid \honest] > \E[u_i \mid \dishonest]$ for any $\deception > 0$. Therefore, $\honest$ is a strict best response for $i$. Since this holds for all $i$, the all-honest profile is a strict Nash equilibrium.
> 
> Furthermore, this equilibrium does not require an external enforcer. The audit mechanism itself---the mathematics of multi-expert detection---provides the enforcement. No police, no prosecutor, no judge is needed to make honesty individually rational. The theorem enforces.

> **Remark:** [The Theorem Enforces 定理即执法]
> <!-- label: rem:theorem_enforces -->
> Traditional enforcement relies on a central authority with a monopoly on legitimate violence (the state, the regulator, the compliance department). SCX{} replaces the enforcer with a theorem. As long as $M \geq M_$, the expected-value calculation alone drives rational agents to honesty. This is a profound shift: from ``you must be honest because you will be punished if caught'' to ``you should be honest because dishonesty is a negative-expectation bet.'' The former requires a credible threat from an authority. The latter requires only arithmetic.

### The Convergence Argument 收敛论证

What if not everyone understands Theorem [ref]? What if some individuals initially choose $\dishonest$? The system still converges:

1. Dishonest agents are detected (Theorem [ref]), incur the penalty $\cost$, and are removed or reformed.
2. Honest agents observe that dishonest peers are caught, reinforcing their belief in the detection mechanism.
3. As the number of detected dishonest acts grows, the *perceived* $M$ (the number of known auditors) increases, further strengthening the dominance of honesty.
4. In the limit, the community converges to the all-honest equilibrium.

This convergence is not driven by moral education, cultural change, or political reform---though these may accelerate it. It is driven by the mathematics of detection and the self-interest of rational agents.

### You Are the Auditor 你就是审计者

This paper has addressed you as an agent facing pressure. But you are also an auditor. Your knowledge of local conditions, your access to data, your professional expertise---these are precisely the independent observations that the SCX{} framework relies on.

When you refuse to falsify data, you are not only protecting yourself. You are serving as one of the $M$ auditors for your peers. You are contributing to the detection probability for every other dishonest agent in your domain. Your honesty is not a private virtue; it is a public good that raises $M$ for everyone.

**Every honest individual makes honesty more rational for every other individual. The mathematics is viral.**

### Open Problems 开放问题

Several theoretical questions remain open:

1. **Correlated Auditors.** Assumption [ref] requires auditor independence. In practice, auditors within the same institution may share biases, training, or incentives. The effective auditor count $M_{eff} \leq M$ under correlation. Quantifying $M_{eff}$ for realistic correlation structures is an open statistical problem.
2. **Strategic Auditors.** We modeled auditors as mechanical (producing estimates with fixed noise distribution). In reality, auditors are also agents who may face their own pressures. The game where every player is simultaneously an agent and an auditor, with possible auditor dishonesty, is a richer game-theoretic structure.
3. **Dynamic Benefit Functions.** The benefit $b$ from falsification may depend on whether *other* agents also falsify (if everyone inflates, the norm shifts). This introduces strategic complementarities that can produce multiple equilibria.
4. **Retaliation-Proof Mechanisms.** The pre-detection retaliation problem (Limitation [ref]) requires institutional design beyond the audit framework. Cryptographic commitment schemes, delayed revelation, and anonymous reporting are candidate solutions that deserve formal analysis.

### Closing 结语

You picked up this paper, perhaps, looking for a reason to do the right thing. You may have expected moral exhortation. You found mathematics instead.

The four theorems in this paper prove, from first principles and with full rigor, that under SCX{} audit conditions, honesty is not a sacrifice of self-interest. It is the maximization of self-interest. You are not being asked to be a hero. You are being shown that the rational calculation---the cold, self-interested, expected-value-maximizing calculation---points in exactly one direction.

**Compute $M_$. Count your auditors. If $M \geq M_$, the math has already made your decision.**

The ancient instruction 勿以恶小而为之 was wise, but incomplete. The fuller truth is:

<div align="center">

\framebox[0.92\textwidth]{
\parbox{0.88\textwidth}{

{\bf 勿以恶小而为之 —— 因为小恶与大恶的检测概率相等。}

{\it Do not commit an evil because it is small --- because the probability of detecting a small evil equals that of detecting a large one.}

}}

</div>

This is not a moral claim. It is Theorem [ref]. And it is true.

\begin{thebibliography}{99}

\bibitem{Hoeffding1963}
W.~Hoeffding.
\newblock Probability inequalities for sums of bounded random variables.
\newblock {\em Journal of the American Statistical Association}, 58(301):13--30, 1963.

\bibitem{SCX2025}
SCX.
\newblock {SCX}: Structured Causal eXamination --- A multi-expert audit framework.
\newblock Technical Report, 2025.

\bibitem{Spring2025}
SCX.
\newblock {Spring}: Permanent memory architecture for irreversible audit trails.
\newblock Technical Report, 2025.

\bibitem{Yajie2025}
SCX.
\newblock {Yajie}: Game-theoretic consensus with Nash payoff equilibrium.
\newblock Technical Report, 2025.

\bibitem{Sanguozhi}
陈寿 (Chen Shou).
\newblock {\em 三国志 (Records of the Three Kingdoms)}, Book 32, Biography of the Former Lord (先主传).
\newblock 3rd century CE.

\bibitem{FudenbergTirole1991}
D.~Fudenberg and J.~Tirole.
\newblock {\em Game Theory}.
\newblock MIT Press, 1991.

\bibitem{OsborneRubinstein1994}
M.~J.~Osborne and A.~Rubinstein.
\newblock {\em A Course in Game Theory}.
\newblock MIT Press, 1994.

\bibitem{Arrow1963}
K.~J.~Arrow.
\newblock Uncertainty and the welfare economics of medical care.
\newblock {\em American Economic Review}, 53(5):941--973, 1963.

\bibitem{Akerlof1970}
G.~A.~Akerlof.
\newblock The market for ``lemons'': Quality uncertainty and the market mechanism.
\newblock {\em Quarterly Journal of Economics}, 84(3):488--500, 1970.

\bibitem{Myerson1991}
R.~B.~Myerson.
\newblock {\em Game Theory: Analysis of Conflict}.
\newblock Harvard University Press, 1991.

\end{thebibliography}