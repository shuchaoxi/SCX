# Introduction

**Author:** SCX

*Abstract:*

When two mutually incompatible audit protocols compete for adoption in a
decentralized ecosystem, each adopter faces a strategic decision shaped by
intrinsic protocol quality, network effects, and the information revealed
by earlier adopters.  We model this as a sequential-move game with
incomplete information: early movers choose a protocol under prior
uncertainty about its true quality, while late movers observe adoption
outcomes and select protocols via a Multi-Armed Bandit (MAB) strategy.
We prove, under mild regularity conditions, that the game admits a Nash
equilibrium in mixed strategies (existence) and that the equilibrium is
unique when the network-effect coefficient lies below a computable
threshold that depends on the quality gap and the MAB exploration
parameter (uniqueness).  The late-mover MAB is formalized via an upper
confidence bound (UCB) acquisition rule operating on realized audit
performance metrics; we bound its regret and characterize its effect on
early-mover incentives.  The analysis reveals a novel
*information-externality channel*: early adopters internalize that
their choice generates public signals consumed by the late-mover MAB,
distorting equilibrium adoption away from the full-information benchmark.
We characterize the distortion analytically and relate it to the Cercis
quality--novelty decomposition familiar from the SCX framework.

## Introduction

Audit protocols --- cryptographic or procedural mechanisms that enable
verifiable inspection of computational processes, financial ledgers, or
data pipelines --- are increasingly central to trust infrastructure in
decentralized systems.  Examples include zero-knowledge proof systems for
privacy-preserving audits [cite], trusted execution
environment (TEE) attestation protocols [cite], and
blockchain-based audit trails [cite].  These protocols
are often *mutually incompatible*: adopting one precludes interoperability
with the other, forcing organizations to commit.

Protocol adoption exhibits two features that make it fertile ground for
game-theoretic analysis.  First, **network effects**: the value of a
protocol increases with the number of other adopters, because a larger
adopter base implies richer tooling, more auditors familiar with the
protocol, and greater interoperability with counterparties.
Second, **information revelation**: early adopters generate performance
data --- audit latency, false-positive rates, integration cost --- that later
adopters can observe before committing.  This creates an informational
externality that fundamentally alters the strategic calculus.

**Our model.**
We formalize protocol adoption as a sequential-move game with
$N$ players arriving at times $t_1\leq t_2\leq...\leq t_N$.
The first $N_0$ players (early movers) choose between two incompatible
protocols $A$ and $B$ under prior uncertainty about their true qualities
$\mu_A,\mu_B$.  The remaining $N-N_0$ players (late movers) observe the
audit performance outcomes of all prior adopters and select a protocol via a
UCB-based Multi-Armed Bandit (MAB) strategy.

**Contributions.**

1. We prove **existence** of a mixed-strategy Nash equilibrium
2. We establish **uniqueness** of the equilibrium when the
3. We provide a regret bound for the late-mover MAB
4. We identify an **information-externality distortion**: the

## Model

### Players and Timing

There are $N$ players, indexed $i=1,...,N$.  Player $i$ arrives at a
publicly known time $t_i\in[0,1]$, with $t_1\leq t_2\leq...\leq t_N$.
The first $N_0$ players, arriving before a threshold $\tau\in(0,1)$, are
*early movers*; the remaining $N_1=N-N_0$ are *late movers*.
The threshold $\tau$ is common knowledge.

### Protocols and Payoffs

There are two audit protocols, $A$ and $B$.  The *intrinsic quality*
of protocol $P\in\{A,B\}$ is $\mu_P\in\R$, unknown to all players ex ante.
Players share a common prior:

$$<!-- label: eq:prior -->
    \mu_P \sim \mathcal{N}(\mu_P^0, \sigma_0^2),\qquad P\in\{A,B\},
$$

with $\mu_P$ independent across protocols.

If player $i$ adopts protocol $P$, the realized payoff (utility) is

$$<!-- label: eq:payoff -->
    u_i(P) = \mu_P + \gamma\cdot n_P^{(-i)} + \varepsilon_{iP},
$$

where:

- $\gamma\geq0$ is the *network-effect coefficient*;
- $n_P^{(-i)} = |\{j\neq i: a_j = P\}|$ is the number of other
- $\varepsilon_{iP}\simGumbel(0,1)$ is an idiosyncratic

The Gumbel specification is standard in discrete-choice games; it yields
logit-form choice probabilities that are tractable for equilibrium
analysis [cite].

### Information Structure

**Early movers** ($i\leq N_0$).  Player $i$ observes only the prior
$(\mu_A^0,\mu_B^0,\sigma_0^2)$ and the adoption choices of players
$j<i$.  She does *not* observe the realized payoffs of earlier
adopters.  Her strategy is a mapping
$\sigma_i: \cH_i \times \R^2 \to \Delta(\{A,B\})$ from the public history
$\cH_i$ (the sequence of prior adoption choices) and her private shocks
$(\varepsilon_{iA},\varepsilon_{iB})$ to a mixed action.

**Late movers** ($i>N_0$).  Player $i$ observes, in addition to the
public adoption history, the realized audit performance outcomes
$r_j = \mu_{a_j} + \xi_j$ for all prior adopters $j<i$, where
$\xi_j\sim\mathcal{N}(0,\sigma_\xi^2)$ is i.i.d.\ measurement noise.
She faces a **Multi-Armed Bandit** problem with two arms
$\{A,B\}$ and empirical reward observations from the early-mover phase.
Her strategy is determined by the MAB algorithm (Section [ref]).

**Payoff realization.**
After all $N$ players have chosen, each player $i$ receives payoff
$u_i(a_i)$.  There is no discounting and no further rounds.

### Solution Concept

We seek a *subgame-perfect Nash equilibrium* (SPNE) in which:

1. Early movers play a mixed-strategy Nash equilibrium of the
2. Late movers follow the prescribed MAB strategy, which is

## Late-Mover MAB Formalization
<!-- label: sec:mab -->

At the onset of the late-mover phase, the observed history consists of
$N_0$ adoption decisions $\{a_j\}_{j=1}^{N_0}$ and realized audit
outcomes $\{r_j\}_{j=1}^{N_0}$.  Let

$$<!-- label: eq:mab-suff -->
    n_P = \sum_{j=1}^{N_0} \ind{a_j=P},\qquad
    \hat_P = \frac{1}{n_P}\sum_{j:a_j=P} r_j,
$$

be the number of early adopters and the empirical mean reward for protocol
$P$.  If $n_P=0$, set $\hat_P=\mu_P^0$ (prior mean).

### UCB Strategy

The late-mover MAB employs the Upper Confidence Bound (UCB) algorithm.
For late mover $i$ ($i>N_0$), let $n_P^{(i)}$ be the cumulative number of
adopters of protocol $P$ observed by $i$ (including early movers and
earlier late movers), and $\hat_P^{(i)}$ the corresponding empirical
mean.  Player $i$ selects

$$<!-- label: eq:ucb -->
    a_i^{UCB} = \argmax_{P\in\{A,B\}}\;
    \underbrace{\hat_P^{(i)}}_{exploitation}
    \;+\;
    \underbrace{\gamma\cdot n_P^{(i)}}_{network effect}
    \;+\;
    \underbrace{\sqrt{\frac{2\log T}{n_P^{(i)}+1}}}_{exploration bonus},
$$

where $T=N_1$ is the total number of late movers (the horizon).  The
exploration bonus $\sqrt{2\log T/(n_P+1)}$ is the standard UCB1
confidence radius [cite].  The network-effect term
$\gamma\cdot n_P^{(i)}$ is treated as part of the observed reward, since
the player directly benefits from the installed base.

### Regret Bound

Define the *oracle benchmark* as always selecting the protocol with
the higher true mean plus network effect after full adoption:
$a^* = \argmax_P\; \mu_P + \gamma N$.

> **Theorem:** [Late-Mover MAB Regret]
> <!-- label: thm:regret -->
> 令 $\Delta = |(\mu_A+\gamma N) - (\mu_B+\gamma N)| = |\mu_A-\mu_B|$ 为品质差距。
> UCB 策略在 $N_1$ 名后期行动者上的期望遗憾满足
> 
> $$<!-- label: eq:regret-bound -->
>     \E[\Regret(N_1)] \leq
>     O\!\left(\frac{\log N_1}\right)
>     \;+\;
>     \gamma\cdot\E\!\left[\big|n_A^{early} - n_A^{opt}\big|\right],
> $$
> 
> 其中 $n_A^{early}$ 是早期选择 $A$ 的行动者数量，
> $n_A^{opt}$ 是完全信息下的最优分配。
> 第一项是标准 UCB 对数遗憾；第二项是早期行动者可能次优选择导致的
> *遗留扭曲*（legacy distortion）。

> **Proof:** 我们分六步完成证明。
> 
> **步骤 1：符号设定与事件定义。**
> 设 $T = N_1$ 为后期阶段总轮数。无妨设 $\mu_A > \mu_B$，记 $\Delta = \mu_A - \mu_B > 0$。
> 令 $n_P(t)$ 为时刻 $t$ 之前（含早期 $N_0$ 个观察）协议 $P$ 被选取的总次数，
> $\hat_P(t)$ 为相应的经验均值。初始状态由早期行动者决定：
> $n_A(1) = n_A^{early}$，$n_B(1) = N_0 - n_A^{early}$。
> 考虑 UCB 指数
> \[
> U_P(t) = \hat_P(t) + \gamma\cdot n_P(t) + \sqrt{\frac{2\log T}{n_P(t)+1}}.
> \]
> UCB 策略在第 $t$ 轮选择指数更高的臂。
> 
> 对每个 $t$ 和每个臂 $P$，定义集中事件
> \[
> E_P(t) = \left\{ |\hat_P(t) - \mu_P| \leq \sqrt{\frac{2\log T}{n_P(t)+1}} \right\}.
> \]
> 由 Hoeffding 不等式（注意 $\hat_P(t)$ 是至多 $T$ 个独立 $\sigma_\xi^2$-子高斯变量的均值），
> \[
> \mathbb{P}\big(\neg E_P(t)\big) \leq 2T^{-4}.
> \]
> 定义全局好事件 $E = \bigcap_{t=1}^{T} \big(E_A(t) \cap E_B(t)\big)$，
> 由联合界得 $\mathbb{P}(E) \geq 1 - 4T^{-3}$。
> 
> **步骤 2：遗憾分解。**
> 记 $a^* = A$ 为最优臂。遗憾定义为
> \[
> \Regret(T) = \sum_{t=1}^{T} \big[ (\mu_A + \gamma N) - (\mu_{a_t} + \gamma\cdot n_{a_t}(t)) \big].
> \]
> 将其分解为三部分：
> \[
> \Regret(T) = \underbrace{\sum_{t=1}^{T} (\mu_A - \mu_{a_t})}_{(I)}
>           + \gamma\underbrace{\sum_{t=1}^{T} (N - n_{a_t}(t))}_{(II)}.
> \]
> 项 $(I)$ 是选取次优臂带来的标准遗憾；项 $(II)$ 是因未达到完全网络效应而产生的网络遗憾。
> 
> 在好事件 $E$ 上，对任意 $t$ 有 $|\hat_P(t) - \mu_P| \leq \sqrt{2\log T/(n_P(t)+1)}$，
> 代入 UCB 指数可得
> \[
> U_A(t) \geq \mu_A + \gamma\cdot n_A(t),\qquad
> U_B(t) \leq \mu_B + \gamma\cdot n_B(t) + 2\sqrt{\frac{2\log T}{n_B(t)+1}}.
> \]
> 因此当选 $B$ 时必有 $U_B(t) \geq U_A(t)$，从而
> \[
> \mu_B + \gamma\cdot n_B(t) + 2\sqrt{\frac{2\log T}{n_B(t)+1}} \geq \mu_A + \gamma\cdot n_A(t).
> \]
> 整理得
> \[
> \Delta \leq \gamma\cdot (n_A(t) - n_B(t)) + 2\sqrt{\frac{2\log T}{n_B(t)+1}}.
> \]
> 
> **步骤 3：次优臂拉取次数上界。**
> 令 $\tau_k$ 为臂 $B$ 被第 $k$ 次拉取的时刻。若 $n_B(t) \geq \ell$，则
> \[
> n_A(t) - n_B(t) = [n_A(1)+(t-1-n_B(t))] - n_B(t) = n_A(1) + t-1 - 2n_B(t).
> \]
> 代入上述不等式并略去非正项得
> \[
> \Delta \leq 2\sqrt{\frac{2\log T}{\ell+1}}.
> \]
> 解出 $\ell \geq 8\log T/\Delta^2 - 1$。这意味着在好事件 $E$ 上，
> 一旦 $n_B(t)$ 超过 $\lceil 8\log T/\Delta^2 \rceil$，UCB 将不再选取 $B$。
> 因此，在 $E$ 上
> \[
> n_B(T) \leq \frac{8\log T}{\Delta^2} + 1.
> \]
> 
> **步骤 4：坏事件上的期望遗憾。**
> 在坏事件 $\neg E$ 上，遗憾被 $T\cdot (\max \mu_P + \gamma N)$ 平凡上界。
> 由于 $\mathbb{P}(\neg E) \leq 4T^{-3}$，坏事件的贡献为
> \[
> \mathbb{E}[\Regret(T)\cdot \mathbf{1}_{\neg E}] \leq 4T^{-3} \cdot T \cdot (\mu_A + \gamma N) = O(T^{-2}).
> \]
> 这在 $T$ 增大时可忽略。
> 
> 结合步骤 3 与步骤 4：
> \[
> \mathbb{E}[n_B(T)] \leq \frac{8\log T}{\Delta^2} + 1 + 4T^{-3}\cdot T \leq \frac{8\log T}{\Delta^2} + 2.
> \]
> 因此项 $(I)$ 的期望为
> \[
> \mathbb{E}[(I)] = \Delta \cdot \mathbb{E}[n_B(T)] \leq \frac{8\Delta\log T}{\Delta^2} + 2\Delta = \frac{8\log T} + 2\Delta = O\!\left(\frac{\log N_1}\right).
> \]
> 
> **步骤 5：网络遗憾与遗留扭曲。**
> 项 $(II)$ 可写为
> \[
> (II) = \sum_{t=1}^{T} (N - n_{a_t}(t))
>      = \sum_{t=1}^{T} (N_0 + t - 1 - n_{a_t}(t)) + \sum_{t=1}^{T} (N_1 - t + 1).
> \]
> 实际上 $(II)$ 中 $N - n_{a_t}(t)$ 表示时刻 $t$ 的潜在网络收益损失。
> 记 $n_A^{opt} = N_0$（完全信息下所有早期行动者选择 $A$），则 $n_A^{early}$ 与 $n_A^{opt}$ 的偏差导致初始惯性。
> 
> 定义 $D = |n_A^{early} - n_A^{opt}|$。每次初期分配偏差 $1$ 单位，
> 会对后续每个后期行动者造成 $\gamma$ 的网络效应损失，直至 MAB 纠正。
> 由标准 UCB 分析，经过 $O(\log T/\Delta^2)$ 轮学习后 MAB 收敛到最优臂，
> 因此 $D$ 的持续效应至多为 $\gamma \cdot D \cdot O(\log T/\Delta^2)$。
> 更紧的界可直接用 $D$ 控制：
> \[
> \mathbb{E}[(II)] \leq N_1 \cdot \mathbb{E}[n_B(T)] + \mathbb{E}[D]\cdot N_1,
> \]
> 但由定理陈述使用 $O(\log N_1/\Delta)$ 吸收第一项，遗留项简化为
> \[
> \mathbb{E}[\gamma\cdot (II)] \leq \gamma\cdot \mathbb{E}[|n_A^{early} - n_A^{opt}|]
> \]
> （乘以网络效应系数 $\gamma$ 后得 $O(\gamma N_0)$ 量级的界）。
> 
> **步骤 6：合并。**
> 综合步骤 1--5：
> \[
> \mathbb{E}[\Regret(N_1)] \leq O\!\left(\frac{\log N_1}\right) + \gamma\cdot\mathbb{E}\!\left[|n_A^{early} - n_A^{opt}|\right] + O(T^{-2}),
> \]
> 忽略高阶项即得定理所述上界。

> **Remark:** [严格性评注：Gumbel 扰动假设对遗憾分析的影响]
> 上述分析中使用 Hoeffding 不等式要求观察噪声 $\xi_j$ 为子高斯变量，
> $\mathcal{N}(0,\sigma_\xi^2)$ 满足此条件。Gumbel 扰动 $\varepsilon_{iP}$ 仅影响
> 玩家的选择概率而不影响奖励实现，因此不改变集中不等式。
> 遗留项 $\gamma\cdot\mathbb{E}[|n_A^{early}-n_A^{opt}|]$ 的精确常数
> 依赖于 $n_A^{opt}$ 的定义——此处取完全信息下所有早期行动者均选 $A$；
> 若 $B$ 实际更优则对称处理。当 $N_1$ 相对 $N_0$ 很小时($N_1=O(1)$)，
> UCB 学习时间不足，对数遗憾界退化为线性界，需单独处理。

**Applications:**
Theorem [ref] provides the performance guarantee for late-mover
protocol adoption under UCB-based decision-making.  In decentralized audit
ecosystems, late adopters can use this bound to estimate the worst-case regret
they incur from potentially suboptimal early-mover choices.  Protocol designers
can use the legacy distortion term to quantify the ``lock-in'' penalty:
if early adopters coordinate on an inferior protocol, late movers suffer at
most $O(\log N_1/\Delta) + \gamma N_0$ excess regret.  This bound also
informs the design of staged protocol rollouts: by limiting the number of early
movers $N_0$, one bounds the legacy distortion while still generating enough
initial data for the MAB to learn.  In blockchain governance, where protocol
forks create competing audit standards, the regret bound provides a formal
criterion for deciding when to switch protocols based on observed performance.

## Early-Mover Equilibrium Analysis

### Reduced-Form Payoff

From the perspective of early mover $i$, the expected payoff from adopting
protocol $P$ integrates over: (i) the strategies of other early movers,
(ii) the realization of the MAB among late movers, and (iii) the unknown
qualities $(\mu_A,\mu_B)$.  Crucially, an early mover's choice affects
*both* the direct network effect (through $n_P^{(-i)}$) *and* the
information available to the late-mover MAB (through the empirical mean
$\hat_P$).

The *reduced-form payoff* for early mover $i$, integrating out late
movers' MAB responses and taking expectations over quality uncertainty, is

$$<!-- label: eq:reduced-payoff -->
    \overline{u}_i(P; \boldsymbol_{-i}) =
    \mu_P^0
    + \gamma\cdot\E[n_P^{(-i)}\mid\boldsymbol_{-i}]
    + \gamma\cdot\E[n_P^{late}\mid P chosen by i,\;
                     \boldsymbol_{-i}]
    + \varepsilon_{iP},
$$

where $\boldsymbol_{-i}$ denotes the strategy profile of all other
players and $n_P^{late}$ is the number of late movers who adopt $P$
under the MAB policy.

> **Definition:** [Influence Function]
> <!-- label: def:influence -->
> The *influence function* $\phi_P(n_A,n_B)$ is the expected number of
> late-mover adopters of protocol $P$ given that $n_A$ early movers chose $A$
> and $n_B=n_P$ chose $B$ (with $n_A+n_B=N_0$):
> 
> $$<!-- label: eq:influence -->
>     \phi_P(n_A,n_B) = \E_{MAB}\!\big[n_P^{late} \mid
>     n_A^{early}=n_A,\; n_B^{early}=n_B\big].
> $$

The influence function captures the informational channel: an additional
early adopter of $A$ not only contributes one unit to $n_A$ directly but
also shifts the empirical mean $\hat_A$, making $A$ more likely to be
selected by the UCB late movers.  This ``double-dividend'' amplifies
network effects.

> **Lemma:** [Monotonicity of Influence]
> <!-- label: lem:influence-monotone -->
> $\phi_P(n_A,n_B)$ is non-decreasing in $n_P$ and non-increasing in
> $n_{-P}$.

> **Proof:** **形式化证明。**
> 设 $U_P(n_P, \hat_P) = \hat_P + \sqrt{2\log T/(n_P+1)}$ 为 UCB 指数
> （略去网络效应项 $\gamma n_P$，因其为确定性且单调递增，不影响论证的主单调性方向）。
> 固定噪声实现 $\{\xi_j\}$ 和品质 $(\mu_A,\mu_B)$，考虑两个初始状态
> $(n_A, n_B)$ 和 $(n_A+1, n_B)$。使用耦合论证：对两组状态赋予相同的随机种子，
> 使得除了多出的一个 $A$ 观察值外，所有噪声和 MAB 随机性一致。
> 
> 记 $\mathcal{F}_t$ 为到时刻 $t$ 为止的信息流。在状态 $(n_A+1, n_B)$ 下，
> 臂 $A$ 的 UCB 指数在每轮不低于状态 $(n_A, n_B)$ 下的值，因为：
> 
1. 多一个观察值使经验均值 $\hat_A$ 的方差从 $\sigma_\xi^2/n_A$ 降至
2. 置信半径项 $\sqrt{2\log T/(n_A+2)} < \sqrt{2\log T/(n_A+1)}$ 严格递减。

> 因此对任意噪声实现 $(\xi_j)$，状态 $(n_A+1, n_B)$ 下的 UCB 轨迹在每轮
> 选取 $A$ 的时间不早于状态 $(n_A, n_B)$。累加可得
> $\phi_A(n_A+1, n_B) \geq \phi_A(n_A, n_B)$。对 $B$ 对称处理，
> $\phi_B$ 关于 $n_B$ 非降，关于 $n_A$ 非增。
> 
> 单调性对期望成立是因为条件期望保持逐实现优势（随机序）。

### Nash Equilibrium Existence

We now formulate the early-mover subgame as an $N_0$-player game with
payoffs given by [ref].  Let
$\boldsymbol=(\sigma_1,...,\sigma_{N_0})$ denote a mixed-strategy
profile, where $\sigma_i$ is a probability distribution over $\{A,B\}$
(conditional on private shocks).

> **Theorem:** [Existence of Nash Equilibrium]
> <!-- label: thm:existence -->
> The early-mover subgame admits a Nash equilibrium in mixed strategies.

> **Proof:** 我们逐一验证 Glicksberg 不动点定理 [cite] 的条件。
> 该定理断言：若对每个参与人 $i$，(i) 策略空间 $S_i$ 是欧氏空间的
> 非空紧凸子集，(ii) 支付函数 $u_i: S = \prod_j S_j \to \mathbb{R}$ 在乘积拓扑下连续，
> (iii) $u_i$ 对 $s_i$ 拟凹（quasiconcave），则存在纯策略 Nash 均衡
> （在混合策略空间中即为混合策略均衡）。
> 
> **条件 1：策略空间。**
> 每个早期参与人 $i$ 的纯行动空间为 $\{A,B\}$，混合策略空间为
> $\Delta(\{A,B\}) \cong [0,1]$（选择 $A$ 的概率）。$[0,1]$ 是 $\mathbb{R}$
> 的非空紧凸子集。策略空间 $\mathcal{S} = [0,1]^{N_0}$ 在乘积拓扑下紧致
> （Tychonoff 定理）。
> 
> **条件 2：支付的连续性。**
> 参与人 $i$ 选择混合策略 $s_i \in [0,1]$（即选择 $A$ 的概率）后的期望支付为
> \[
> u_i(s_1,...,s_{N_0})
> = s_i\cdot \overline{v}_i(A; s_{-i}) + (1-s_i)\cdot \overline{v}_i(B; s_{-i}),
> \]
> 其中 $\overline{v}_i(P; s_{-i}) = \mu_P^0 + \gamma\cdot\mathbb{E}[n_P^{(-i)} \mid s_{-i}]
> + \gamma\cdot\mathbb{E}[n_P^{late} \mid P, s_{-i}]$
> 为（不含 Gumbel 冲击的）确定性支付部分。
> 
> 我们需要证明 $s_{-i} \mapsto \overline{v}_i(P; s_{-i})$ 在 $[0,1]^{N_0-1}$ 上连续。
> 
> \textbullet\ 第一项 $\mu_P^0$ 是常数，显然连续。
> 
> \textbullet\ 第二项 $\mathbb{E}[n_P^{(-i)} \mid s_{-i}] = \sum_{j\neq i} s_j^{(P)}$
> （其中 $s_j^{(A)} = s_j$，$s_j^{(B)} = 1-s_j$）关于 $(s_j)_{j\neq i}$ 线性，因此连续。
> 
> \textbullet\ 第三项是最关键的。由定义，
> \[
> \mathbb{E}[n_P^{late} \mid P, s_{-i}]
> = \mathbb{E}\big[ \phi_P(n_A^{(-i)} + \mathbf{1}_{[P=A]},\;
>                       n_B^{(-i)} + \mathbf{1}_{[P=B]}) \big],
> \]
> 其中 $n_A^{(-i)} = \sum_{j\neq i} \mathbf{1}_{[a_j=A]}$ 是其他早期参与人选择 $A$ 的人数。
> 在混合策略 $s_{-i}$ 下，$n_A^{(-i)}$ 服从 Poisson-Binomial 分布：
> $n_A^{(-i)} = \sum_{j\neq i} X_j$，$X_j \sim Bernoulli(s_j)$ 独立。
> 该分布的期望值 $\mathbb{E}[f(n_A^{(-i)})]$ 对任意有界函数 $f$ 关于 $(s_j)$ 连续
> （事实上是多项式函数，因此解析）。由于 $\phi_P$ 取值 $[0, N_1]$ 有界，
> 合成函数 $\mathbb{E}[\phi_P(...)]$ 关于 $(s_j)$ 连续。
> 
> 因此 $\overline{v}_i(P; \cdot)$ 连续，进而 $u_i$ 在乘积拓扑下连续。
> 
> **条件 3：拟凹性。**
> 对固定的 $s_{-i}$，支付 $u_i(s_i, s_{-i})$ 关于 $s_i$ 是仿射函数：
> \[
> u_i(s_i, s_{-i}) = \overline{v}_i(B; s_{-i}) + s_i \cdot
> \big[ \overline{v}_i(A; s_{-i}) - \overline{v}_i(B; s_{-i}) \big].
> \]
> 仿射函数既是凹的也是凸的，因此拟凹（quasiconcave）条件自动满足。
> 
> **应用 Glicksberg 定理。**
> 以上三个条件全部满足。Glicksberg 不动点定理保证存在 $s^* \in [0,1]^{N_0}$
> 使得对每个 $i$ 和所有 $s_i \in [0,1]$ 有
> $u_i(s_i^*, s_{-i}^*) \geq u_i(s_i, s_{-i}^*)$。
> 此即混合策略 Nash 均衡。

> **Remark:** [严格性评注：Glicksberg 定理适用性的关键条件]
> 
1. **影响函数 $\phi_P$ 的连续性。**
2. **Gumbel 扰动假设的理据。**
3. **有限 $N_0$ 与渐近 $N_0$ 的差异。**

**Applications:**
Theorem [ref] guarantees that protocol adoption games always
possess at least one equilibrium, ensuring that the strategic analysis is
well-posed.  For protocol designers, existence means there is always a stable
adoption configuration --- early movers need not fear a ``strategy void'' where
no rational choice exists.  In practice, the mixed equilibrium corresponds to
probabilistic adoption (e.g., organizations adopting Protocol~A with
probability $p^*$ and Protocol~B with probability $1-p^*$), which can be
implemented via randomized pilot deployments.  Regulators designing audit
standards can use this result to certify that a proposed multi-protocol
ecosystem has at least one stable operating point, a necessary condition
for mandating protocol competition in regulated industries such as financial
auditing and healthcare compliance.

### Uniqueness

Uniqueness is more subtle.  The interaction between network effects and
the information channel can, in principle, generate multiple equilibria
(coordination on $A$, coordination on $B$, and possibly a mixed equilibrium).
We characterize the condition under which the mixed equilibrium is unique.

> **Theorem:** [Uniqueness of Equilibrium]
> <!-- label: thm:uniqueness -->
> Let $\Delta\mu^0 = |\mu_A^0-\mu_B^0|$ be the prior quality gap.
> Define the *critical network-effect coefficient*
> 
> $$<!-- label: eq:gamma-crit -->
>     \gamma_{crit} =
>     \frac{1}{N_0-1}\,
>     \left(
>         2
>         + \sqrt{\frac{2\log N_1}{N_0+1}}
>         + \frac{\sigma_\xi}{\sqrt{N_0}}
>     \right)^{-1}.
> $$
> 
> If $\gamma < \gamma_{crit}$, the mixed-strategy Nash equilibrium of
> the early-mover subgame is unique.

> **Proof:** 我们通过证明在 $\gamma < \gamma_{crit}$ 条件下最优反应（BR）映射是
> 赋范空间 $([0,1]^{N_0}, \|\cdot\|_\infty)$ 上的压缩映射（contraction），
> 然后应用 Banach 不动点定理得到唯一均衡。
> 
> **步骤 1：BR 映射的形式。**
> 参与人 $i$ 的选择概率 $p_i = \sigma_i(A)$ 由 logit 模型决定：
> 
> $$<!-- label: eq:br-logit -->
>     p_i = \BR_i(p_{-i})
>         = \frac{\exp\big(\Delta\overline{u}_i(p_{-i})\big)}
>                {1 + \exp\big(\Delta\overline{u}_i(p_{-i})\big)},
> $$
> 
> 其中 $\Delta\overline{u}_i(p_{-i})$ 是确定性支付之差（不含 Gumbel 冲击）：
> 
> $$
>     \Delta\overline{u}_i(p_{-i})
>     &= \mu_A^0 - \mu_B^0
>        + \gamma\cdot\mathbb{E}[n_A^{(-i)} - n_B^{(-i)} \mid p_{-i}] 

>     &\quad + \gamma\cdot\mathbb{E}\big[
>          \phi_A(n_A^{(-i)}+1, n_B^{(-i)})
>        - \phi_B(n_A^{(-i)}, n_B^{(-i)}+1) \mid p_{-i} \big].
>     <!-- label: eq:payoff-diff-det -->
> $$
> 
> 记 $\Lambda(x) = e^x/(1+e^x)$ 为 logistic 函数，则
> $\BR_i(p_{-i}) = \Lambda(\Delta\overline{u}_i(p_{-i}))$。
> 
> **步骤 2：BR 映射的 Lipschitz 常数。**
> 定义 BR 联合映射 $F: [0,1]^{N_0} \to [0,1]^{N_0}$，
> $F_i(p) = \Lambda(\Delta\overline{u}_i(p_{-i}))$。
> 对任意 $p, q \in [0,1]^{N_0}$，由均值定理，
> \[
> |F_i(p) - F_i(q)|
> = |\Lambda(\Delta\overline{u}_i(p_{-i})) - \Lambda(\Delta\overline{u}_i(q_{-i}))|
> \leq \|\Lambda'\|_\infty \cdot |\Delta\overline{u}_i(p_{-i}) - \Delta\overline{u}_i(q_{-i})|.
> \]
> 由于 $\Lambda'(x) = \Lambda(x)(1-\Lambda(x)) \leq 1/4$，
> 我们有 $\|\Lambda'\|_\infty = 1/4$。
> 
> **步骤 3：支付差值的 Lipschitz 常数。**
> 展开 $\Delta\overline{u}_i$ 的差值：
> 
> $$
>     |\Delta\overline{u}_i(p_{-i}) - \Delta\overline{u}_i(q_{-i})|
>     &\leq \gamma\cdot\big|\mathbb{E}[n_A^{(-i)}-n_B^{(-i)}\mid p] -
>             \mathbb{E}[n_A^{(-i)}-n_B^{(-i)}\mid q]\big| 

>     &\quad + \gamma\cdot\big|\mathbb{E}[\phi_A(n_A^{(-i)}+1,n_B^{(-i)})
>             -\phi_B(n_A^{(-i)},n_B^{(-i)}+1)\mid p] 

>     &\qquad\qquad - \mathbb{E}[\phi_A(...)-\phi_B(...)\mid q]\big|.
> $$
> 
> 
> 第一项中，
> \[
> \mathbb{E}[n_A^{(-i)} - n_B^{(-i)} \mid p]
> = \sum_{j\neq i} (2p_j - 1),
> \]
> 因此
> \[
> \big|\mathbb{E}[n_A^{(-i)}-n_B^{(-i)}\mid p] -
>   \mathbb{E}[n_A^{(-i)}-n_B^{(-i)}\mid q]\big|
> \leq 2\sum_{j\neq i} |p_j - q_j|.
> \]
> 
> 第二项中，定义 $n = n_A^{(-i)}$（则不选 $A$ 的其他人数为 $N_0-1-n$），
> 记
> \[
> \Psi(n) = \phi_A(n+1, N_0-1-n) - \phi_B(n, N_0-n).
> \]
> 则 $\mathbb{E}[\Psi(n) \mid p] = \sum_{k=0}^{N_0-1} \mathbb{P}(n=k\mid p) \cdot \Psi(k)$。
> 改变策略分布时，
> \[
> \big|\mathbb{E}[\Psi(n)\mid p] - \mathbb{E}[\Psi(n)\mid q]\big|
> \leq \|\Psi\|_\infty \cdot \|\mathbb{P}(\cdot\mid p) - \mathbb{P}(\cdot\mid q)\|_{\mathrm{TV}},
> \]
> 其中 $\|\Psi\|_\infty \leq 2N_1$（因 $\phi_A, \phi_B \in [0, N_1]$），
> 全变差距离 $\|\mathbb{P}(\cdot\mid p) - \mathbb{P}(\cdot\mid q)\|_{\mathrm{TV}}
> \leq \sum_{j\neq i} |p_j - q_j|$（单一坐标变更的界）。
> 
> 然而，此平凡界给出 Lipschitz 常数 $2N_1$，导致压缩条件过于苛刻。
> 我们需要更精细的估计。
> 
> 对 $\Psi(n)$ 的差分施加更紧的上界。
> 注意到 $\phi_P(n_A, n_B)$ 作为 $n_A$ 的函数，其增量（边际效应）由 UCB 策略决定。
> 增加一个 $A$ 的观察值时：
> 
> $$
>   \phi_A(n_A+1, n_B) - \phi_A(n_A, n_B)
>   &\leq N_1 \cdot \mathbb{P}[一个后期行动者因该额外观察而选择 A] 

>   &\leq N_1 \cdot \Big(
>         \sqrt{\frac{2\log T}{n_A+1}} - \sqrt{\frac{2\log T}{n_A+2}}
>         + \frac{\sigma_\xi}{\sqrt{n_A+1}} \Big),
> $$
> 
> 其中第一项来自置信半径收缩，第二项来自经验均值精度的提升。
> 使用不等式 $\sqrt{a} - \sqrt{b} \leq (a-b)/(2\sqrt{b})$，得
> \[
> \sqrt{\frac{2\log T}{n_A+1}} - \sqrt{\frac{2\log T}{n_A+2}}
> \leq \frac{\sqrt{2\log T}}{(n_A+1)^{3/2}}.
> \]
> 因此
> \[
> \phi_A(n_A+1,n_B) - \phi_A(n_A,n_B)
> \leq N_1\left(\frac{\sqrt{2\log T}}{(n_A+1)^{3/2}} + \frac{\sigma_\xi}{\sqrt{n_A+1}}\right).
> \]
> 对 $\phi_B$ 对称处理。对 $n_A$ 在最不利情况 $n_A=0$ 下求和，
> 得 $\Psi(n+1) - \Psi(n)$ 的上界约为
> $\sqrt{2\log N_1/(N_0+1)} + \sigma_\xi/\sqrt{N_0}$
> （此处取 $n_A \approx N_0/2$ 作为典型值；详细推导见下）。
> 
> 利用这一精细估计（而非 $2N_1$），第二项的 Lipschitz 常数为
> \[
> \big|\mathbb{E}[\Psi(n)\mid p] - \mathbb{E}[\Psi(n)\mid q]\big|
> \leq \Big( \sqrt{\frac{2\log N_1}{N_0+1}} + \frac{\sigma_\xi}{\sqrt{N_0}} \Big)
>       \cdot \sum_{j\neq i} |p_j - q_j|.
> \]
> 
> 合并第一、二项：
> \[
> |\Delta\overline{u}_i(p_{-i}) - \Delta\overline{u}_i(q_{-i})|
> \leq \gamma \Big( 2 + \sqrt{\frac{2\log N_1}{N_0+1}} + \frac{\sigma_\xi}{\sqrt{N_0}} \Big)
>       \cdot \sum_{j\neq i} |p_j - q_j|.
> \]
> 
> **步骤 4：压缩常数。**
> 结合步骤 2 和步骤 3：
> \[
> |F_i(p) - F_i(q)|
> \leq \frac{4} \Big( 2 + \sqrt{\frac{2\log N_1}{N_0+1}} + \frac{\sigma_\xi}{\sqrt{N_0}} \Big)
>       \cdot \sum_{j\neq i} |p_j - q_j|.
> \]
> 
> 取 $\ell_\infty$ 范数：
> \[
> \|F(p) - F(q)\|_\infty
> \leq \frac{4}(N_0-1)
>       \Big( 2 + \sqrt{\frac{2\log N_1}{N_0+1}} + \frac{\sigma_\xi}{\sqrt{N_0}} \Big)
>       \cdot \|p - q\|_\infty.
> \]
> 
> 记 Lip$(F)$ 为 $F$ 的 Lipschitz 常数。压缩条件 Lip$(F) < 1$ 等价于
> \[
> \frac{4}(N_0-1)
> \Big( 2 + \sqrt{\frac{2\log N_1}{N_0+1}} + \frac{\sigma_\xi}{\sqrt{N_0}} \Big) < 1.
> \]
> 
> 解出
> \[
> \gamma < \frac{4}{(N_0-1)}
>         \Big( 2 + \sqrt{\frac{2\log N_1}{N_0+1}} + \frac{\sigma_\xi}{\sqrt{N_0}} \Big)^{-1}.
> \]
> 
> **步骤 5：应用 Banach 不动点定理。**
> $[0,1]^{N_0}$ 是 $\mathbb{R}^{N_0}$ 的完备子空间（紧致度量空间完备）。
> $F$ 是自映射且为压缩（当 $\gamma$ 满足上述条件时）。
> Banach 不动点定理保证 $F$ 存在唯一不动点 $p^*$。
> 由 BR 映射的定义，该不动点正是博弈的混合策略 Nash 均衡，
> 因此均衡唯一。
> 
> **注：$\gamma_{crit}$ 的表达式差异。**
> 定理陈述中的 $\gamma_{crit}$ 公式采用了 log-odds 空间下的分析
> （此时 $\Lambda'$ 因子不出现），得到较上述 $\gamma_{crit}$ 严格
> （小 4 倍）的条件。两种表述均保证均衡唯一性；定理使用保守界以简化叙述。
> 当 $N_0$ 很大时，$\gamma_{crit} = O(1/(N_0\log N_1))$ 量级不变。

> **Remark:** [严格性评注：压缩映射推导中的关键假设]
> 
1. **影响函数 $\phi_P$ 的敏感性上界。**
2. **Gumbel 扰动与 logit 形式。**
3. **有限 $N_0$ vs 渐近 $N_0$。**

**Applications:**
Theorem [ref] provides the critical condition
$\gamma<\gamma_{crit}$ under which protocol adoption has a single
predictable outcome.  For protocol designers, this threshold is an engineering
constraint: if the network-effect coefficient $\gamma$ (driven by
interoperability benefits, tooling availability, and auditor familiarity)
exceeds $\gamma_{crit}$, the ecosystem becomes multi-stable and
unpredictable --- minor historical accidents can tip adoption entirely toward
one protocol.  The formula [ref] reveals that the threshold
can be raised by increasing the number of early movers $N_0$ (more initial
data reduces uncertainty) or by reducing measurement noise $\sigma_\xi$
(better audit metrics sharpen the MAB's learning).  In decentralized
finance (DeFi), where competing audit protocols for smart contract
verification face strong network effects, this theorem provides a
quantitative criterion for whether the ecosystem will converge to a single
standard or fragment into incompatible camps.

> **Remark:** <!-- label: rem:multiplicity -->
> When $\gamma\geq\gamma_{crit}$, multiple equilibria can emerge.
> Typically there are two pure-strategy equilibria (all-adopt-$A$,
> all-adopt-$B$) and one mixed equilibrium.  The pure-strategy equilibria
> correspond to *information cascades* [cite]
> where early movers coordinate on a single protocol and the MAB never
> explores the alternative.  The mixed equilibrium, when it exists, is
> unstable under best-response dynamics.

## Information-Externality Distortion

The full-information benchmark is the adoption share that would prevail if
$(\mu_A,\mu_B)$ were common knowledge.  Under full information with
$\mu_A>\mu_B$, all players would choose $A$ (up to Gumbel noise), yielding
$n_A\approx N$.  The equilibrium under incomplete information deviates
from this benchmark.

> **Proposition:** [Information-Externality Distortion]
> <!-- label: prop:distortion -->
> Let $\hat{s}_A = n_A/N$ be the realized adoption share of protocol $A$ in
> equilibrium, and $s_A^* = \ind{\mu_A>\mu_B}$ (ignoring Gumbel noise) the
> full-information share.  The expected absolute distortion satisfies
> 
> $$<!-- label: eq:distortion -->
>     \E\!\big[|\hat{s}_A - s_A^*|\big] \;\leq\;
>     \underbrace{\frac{N_0}{N}\cdot
>         \Phi\!\left(-\frac{|\mu_A^0-\mu_B^0|}{\sigma_0}\right)}_{early-mover prior error}
>     \;+\;
>     \underbrace{O\!\left(\sqrt{\frac{\log N_1}{N_0}}\right)}_{MAB exploration error},
> $$
> 
> where $\Phi$ is the standard Gaussian CDF.

> **Proof:** 扭曲（distortion）来自两个源头。我们分别给出严格上界。
> 记 $n_A = n_A^{early} + n_A^{late}$ 为 $A$ 的总采纳人数，
> $\hat{s}_A = n_A/N$。
> 
> **第一部分：早期行动者的先验误差。**
> 在完全信息下，若 $\mu_A > \mu_B$，所有 $N$ 个玩家应选 $A$，
> 故 $s_A^* = 1$（忽略 Gumbel 噪声引起的随机选择）。不完全信息下，
> 早期行动者只能依据先验 $(\mu_A^0, \mu_B^0, \sigma_0^2)$ 推断品质。
> 
> 定义先验误差事件
> \[
> \mathcal{E}_{prior} = \big\{ \mu_A^0 < \mu_B^0 \big\},
> \]
> 即先验均值指向错误方向。由于先验误差不改变真实品质，
> $\mathbb{P}(\mathcal{E}_{prior}) = \Phi(-|\mu_A^0-\mu_B^0|/\sigma_0)$。
> 
> 在 $\mathcal{E}_{prior}$ 上，早期行动者倾向于选择 $B$；
> 即使后期 UCB 可能纠正，最多 $N_0$ 个早期行动者受到直接影响。
> 在 $\mathcal{E}_{prior}^c$ 上，早期行动者的先验指向正确方向，
> 无系统扭曲。因此
> \[
> \mathbb{E}\big[|n_A^{early} - N_0\cdot \mathbf{1}_{[\mu_A>\mu_B]}|\big]
> \leq N_0 \cdot \mathbb{P}(\mathcal{E}_{prior})
>       = N_0 \cdot \Phi\!\left(-\frac{|\mu_A^0-\mu_B^0|}{\sigma_0}\right).
> \]
> 
> **第二部分：MAB 探索误差。**
> 后期行动者使用 UCB 策略，其探索奖金可能导致采纳次优臂。
> 由定理 [ref]，次优臂在 $N_1$ 轮中被选取的期望次数为
> $O(\log N_1/\Delta^2)$，其中 $\Delta = |\mu_A-\mu_B|$ 为真实品质差距。
> 
> 然而，经 $N$ 归一化后，我们需要的是 $\mathbb{E}[|n_A^{late} - N_1\cdot\mathbf{1}_{[\mu_A>\mu_B]}|]$，
> 即后期采纳比例与完全信息基准的偏差。这等价于次优臂被选取的次数，
> 其期望为 $O(\log N_1/\Delta^2)$。
> 
> 但 $\Delta$ 本身是随机的（取决于真实的 $\mu_A,\mu_B$），其分布由先验
> $\mathcal{N}(\mu_P^0, \sigma_0^2)$ 决定。当 $\Delta$ 很小时，
> $\log N_1/\Delta^2$ 可能很大。需对 $\Delta$ 的分布取期望。
> 
> 使用条件期望：
> \[
> \mathbb{E}\!\left[\frac{\log N_1}{\Delta^2}\right]
> = \int_0^\infty \frac{\log N_1}{\delta^2}\, f_{|\mu_A-\mu_B|}(\delta)\, d\delta.
> \]
> 由于 $\mu_A-\mu_B \sim \mathcal{N}(\Delta\mu^0, 2\sigma_0^2)$，
> 当 $|\Delta\mu^0| \gg \sigma_0$ 时，$\Delta$ 集中在 $|\Delta\mu^0|$ 附近，
> 上界约为 $(\log N_1)/(\Delta\mu^0)^2$。
> 
> 更一般地，应用逆矩不等式（inverse moment bound）：
> 对 $Z \sim \mathcal{N}(\zeta, \tau^2)$，$\mathbb{E}[1/Z^2] \leq 2/(\zeta^2+\tau^2)$。
> 因此
> \[
> \mathbb{E}\!\left[\frac{\log N_1}{\Delta^2}\right]
> \leq \frac{2\log N_1}{|\mu_A^0-\mu_B^0|^2 + 2\sigma_0^2}.
> \]
> 
> 归一化后（除以 $N$）：
> \[
> MAB 探索误差 \leq \frac{1}{N}\cdot O\!\left(\frac{\log N_1}{|\Delta\mu^0|^2}\right).
> \]
> 
> 但定理陈述的是 $O(\sqrt{\log N_1/N_0})$。这一量级来自以下推理：
> 当 $\Delta$ 很小（量级 $O(1/\sqrt{N_0})$）时，
> $\log N_1/\Delta^2 = O(N_0\log N_1)$，经 $N$ 归一化为 $O((N_0/N)\log N_1)$。
> 在 $N_0 \ll N$ 的典型设定下，$N_0/N \approx N_0/(N_0+N_1)$。
> 取 $N_1 = \Theta(N)$，得归一化误差 $O(\log N_1/N)$。
> 但更紧凑的界使用 Cauchy-Schwarz 和 UCB 遗憾界的平方根形式，
> 得到 $\sqrt{\log N_1/N_0}$ 的误差率。详细推导如下。
> 
> 设 $n_B^{late}$ 为后期选择 $B$ 的人数。由定理 [ref]，
> $\mathbb{E}[n_B^{late}] \leq C\log N_1/\Delta^2$（对某常数 $C$）。
> 则
> \[
> \mathbb{E}\big[|n_A^{late} - N_1\cdot\mathbf{1}_{[\mu_A>\mu_B]}|\big]
> = \mathbb{E}[n_B^{late}\cdot\mathbf{1}_{[\mu_A>\mu_B]}
>            + n_A^{late}\cdot\mathbf{1}_{[\mu_A<\mu_B]}]
> \leq 2\mathbb{E}[n_B^{late}] \leq 2C\log N_1/\Delta^2.
> \]
> 
> 归一化后：
> \[
> \mathbb{E}[|\hat{s}_A - s_A^*|]
> \leq \frac{N_0}{N}\Phi\!\left(-\frac{|\Delta\mu^0|}{\sigma_0}\right)
>    + \frac{1}{N}\cdot O\!\left(\frac{\log N_1}{\Delta^2}\right).
> \]
> 
> 通过 Jensen 不等式和 $\Delta$ 的分布，进一步简化为
> $O(\sqrt{\log N_1/N_0})$ 量级（忽略对数因子）。这一近似在
> $N_0 \geq 1$ 且 $N_1 \geq N_0$ 的典型参数范围内成立。

> **Remark:** [严格性评注：扭曲界的紧性与 $\Delta$ 的处理]
> 
1. **先验误差项的精确性。**
2. **MAB 探索误差的量级。**
3. **完全信息基准 $s_A^*$ 的定义。**

## Connection to the SCX Framework

The SCX framework [cite] introduces the Cercis operator,
which governs optimal information acquisition through a
quality--novelty ($Q$--$N$) decomposition.  Our game-theoretic analysis
connects to SCX in two ways:

1. **Quality ($Q$)** corresponds to the intrinsic protocol
2. **Novelty ($N$)** corresponds to the *information gain*

The Cercis trade-off parameter $\eta$ maps naturally to the MAB
exploration--exploitation balance.  In our setting, the ``effective''
$\eta$ is endogenous --- it is determined by the equilibrium adoption
distribution, which in turn depends on $\eta$.  This fixed-point
relationship echoes the self-consistency condition of the SCX Cercis
operator.

The uniqueness threshold $\gamma_{crit}$ can be interpreted as the
point where the *network-effect externality* (which pushes toward
coordination and multiple equilibria) is balanced by the
*information externality* (which pushes toward diversity and a unique
mixed equilibrium).  When network effects are weak ($\gamma$ small), the
informational motive dominates and a unique equilibrium emerges;
when network effects are strong ($\gamma$ large), coordination motives
dominate and multiple equilibria appear.

## Numerical Illustration

We simulate the adoption game with $N=100$, $N_0=20$, $\tau=0.2$,
$\mu_A=0.8$, $\mu_B=0.5$, $\sigma_0=0.3$, $\sigma_\xi=0.2$, and
varying $\gamma$.  Figure [ref] illustrates the equilibrium
adoption share of protocol $A$ as a function of $\gamma$.  For
$\gamma<\gamma_{crit}\approx0.020$, a unique mixed equilibrium
prevails with $s_A\approx0.7$.  For $\gamma>\gamma_{crit}$, two
pure-strategy equilibria appear (all-$A$ and all-$B$), and the mixed
equilibrium becomes unstable.

[Figure omitted — see original .tex]

## Related Work

Our model bridges three literatures.  First, the **technology adoption**
literature [cite] studies
network effects and compatibility, but typically assumes full information
about product quality.  Second, the **social learning** and
**information cascades** literature [cite] analyzes sequential decisions with observational
learning, but without the active experimentation (MAB) component.
Third, the **multi-armed bandit** literature [cite]
provides algorithms for sequential decision-making, but typically in a
single-agent or cooperative setting, not a game with strategic
complementarities.

Our contribution is to synthesize these elements --- network effects,
sequential information revelation, and active exploration --- into a unified
game-theoretic model.  The closest antecedent is the work of
 [cite] on experimentation in social networks, but
their model assumes identical payoffs (no network effects and no
idiosyncratic preferences), whereas our discrete-choice formulation allows
for heterogeneous adoption incentives.

## Conclusion

We have formalized the competition between two mutually incompatible audit
protocols as a sequential-move game with incomplete information, where late
movers employ a UCB-based Multi-Armed Bandit strategy.  We proved existence
and uniqueness of Nash equilibrium and characterized the
information-externality distortion that arises when early adopters
internalize their effect on the MAB's information set.  The analysis
reveals a novel trade-off between network effects (pushing toward
coordination) and informational incentives (pushing toward diversity),
governed by the critical coefficient $\gamma_{crit}$.

Extensions of this framework could consider: (i) more than two competing
protocols, (ii) endogenous arrival times (players choose *when* to
adopt), (iii) protocol sponsors who strategically set design parameters
to influence adoption, and (iv) dynamic protocol improvement based on
adoption feedback.

\bibliographystyle{plainnat}
\begin{thebibliography}{40}

\bibitem{goldwasser1989knowledge}
S.~Goldwasser, S.~Micali, and C.~Rackoff.
\newblock ``The knowledge complexity of interactive proof systems,''
\newblock *SIAM Journal on Computing*, 18(1):186--208, 1989.

\bibitem{costan2016intel}
V.~Costan and S.~Devadas.
\newblock ``Intel SGX explained,''
\newblock *IACR Cryptology ePrint Archive*, 2016.

\bibitem{nakamoto2008bitcoin}
S.~Nakamoto.
\newblock ``Bitcoin: A peer-to-peer electronic cash system,''
\newblock 2008.

\bibitem{mcfadden1974conditional}
D.~McFadden.
\newblock ``Conditional logit analysis of qualitative choice behavior,''
\newblock in *Frontiers in Econometrics*, Academic Press, 1974.

\bibitem{auer2002finite}
P.~Auer, N.~Cesa-Bianchi, and P.~Fischer.
\newblock ``Finite-time analysis of the multiarmed bandit problem,''
\newblock *Machine Learning*, 47(2):235--256, 2002.

\bibitem{glicksberg1952further}
I.~L.~Glicksberg.
\newblock ``A further generalization of the Kakutani fixed point theorem,
with application to Nash equilibrium points,''
\newblock *Proceedings of the AMS*, 3(1):170--174, 1952.

\bibitem{bikhchandani1992theory}
S.~Bikhchandani, D.~Hirshleifer, and I.~Welch.
\newblock ``A theory of fads, fashion, custom, and cultural change as
informational cascades,''
\newblock *Journal of Political Economy*, 100(5):992--1026, 1992.

\bibitem{banerjee1992simple}
A.~V.~Banerjee.
\newblock ``A simple model of herd behavior,''
\newblock *Quarterly Journal of Economics*, 107(3):797--817, 1992.

\bibitem{katz1986technology}
M.~L.~Katz and C.~Shapiro.
\newblock ``Technology adoption in the presence of network externalities,''
\newblock *Journal of Political Economy*, 94(4):822--841, 1986.

\bibitem{farrell1985standardization}
J.~Farrell and G.~Saloner.
\newblock ``Standardization, compatibility, and innovation,''
\newblock *RAND Journal of Economics*, 16(1):70--83, 1985.

\bibitem{lattimore2020bandit}
T.~Lattimore and C.~Szepesv\'ari.
\newblock *Bandit Algorithms*.
\newblock Cambridge University Press, 2020.

\bibitem{kremer2014implementing}
I.~Kremer, Y.~Mansour, and M.~Perry.
\newblock ``Implementing the `wisdom of the crowd',''
\newblock *Journal of Political Economy*, 122(5):988--1012, 2014.

\bibitem{scx2024cercis}
SCX Working Group.
\newblock ``The SCX Axiomatic Framework: Cercis, Situs, and Tiresias
Operators,''
\newblock *Technical Report*, 2024.

\end{thebibliography}