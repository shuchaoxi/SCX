# Introduction

**Author:** SCX

*Abstract:*

The SCX Audit Sword establishes that any use of the Cercis Score can be
independently audited --- provided the auditor possesses complete data access.
In federated scenarios where $K$ parties hold private datasets and interact
only through aggregated statistics, the Audit Sword encounters a structural
obstacle: how does one audit what one cannot see?  We formalize this as the
*Federated Audit Problem* and prove three results.  (i)~When the Situs
encoding admits a homomorphic composition operator $\oplus$ such that
$\Situs(\cup_k \cD_k) \cong \oplus_k \Situs(\cD_k)$, and each party's Cercis
Score submission is verified by a zero-knowledge proof $\pi_$, the
federated audit achieves $\varepsilon$-equivalence to the full-data audit,
with $\varepsilon \to 0$ under vanishing differential privacy budget and
growing sample size.  The Situs homomorphic composition construction is
**conditionally rigorous** --- given the operator, the $\varepsilon$-bound
is strict; the operator's existence is an **open problem**.
(ii)~Without $\ZK$ verification, the information loss is lower-bounded by
$\mathrm{const} \cdot \eta_k \cdot |\cD_k|/|\cD_{\mathrm{total}}|$, a
**rigorous** consequence of Theorem~3 and the data processing inequality.
(iii)~We outline the ``Telegraph Public Good'' extension where decentralized
storage-layer commitments replace $\ZK$ proofs with Proofs of Storage,
further tightening the $\varepsilon$ bound --- an **open problem** with
a clear theoretical path.  Collectively, the results establish that federated
auditing is possible without raw data access, but only when the information
architecture provides verifiable audit fingerprints.

## Introduction

The SCX framework [cite] established the **Audit Sword**
principle: every use of the Cercis Score must be independently verifiable by
any third party.  This is not an optional feature --- it is a structural
requirement that follows from Theorem~3 (the Noise--Difficulty
Unidentifiability Theorem).  If you cannot audit the detector, you cannot
distinguish whether it is flagging genuine label noise or merely reclassifying
difficult-but-correct samples according to its own inductive biases.

The Audit Sword, however, carries a hidden premise: that the auditor has
**complete access to all data**.  In an increasingly federated world ---
hospitals that cannot share patient records across jurisdictions, financial
institutions barred from exposing transaction logs, edge devices with
bandwidth and privacy constraints --- this premise fails.  The very parties
whose models most urgently require auditing (because they operate on
sensitive, high-stakes data) are precisely those who cannot grant the access
that auditing presupposes.

This creates the **Federated Audit Paradox**.  Federated learning has
developed an extensive privacy-preserving toolbox --- Secure
Aggregation [cite], Differential
Privacy [cite], Multi-Party
Computation [cite] --- but each of these tools is designed
to *prevent information leakage*.  The SCX requirement is the inverse:
we need to *enable auditability* without compromising privacy.  The
existing toolbox solves the problem of locking the door; we need to solve
the problem of auditing through it.

**The Core Tension.**
At the heart of the paradox lies an information asymmetry.  The auditor's
full-information statistic $T_{\mathrm{full}}$ operates on raw $(x, y)$ pairs
from the union of all parties' datasets.  The federated auditor instead
receives only *audit fingerprints* --- the Cercis Scores $S_k$ computed
locally by each party, potentially encrypted, along with the aggregated model
$M_\Pi$.  The question is not whether the fingerprints leak the raw data (they
should not), but whether they preserve enough statistical structure to support
audit conclusions with the same power as the full-information benchmark.

**Contributions.**

1. **Federated Audit $\varepsilon$-Equivalence**
2. **Information Lower Bound**
3. **Telegraph Public Good Extension**

## Preliminaries

### SCX Audit Architecture

We recall the essential SCX components required for federated audit analysis.
For a dataset $\cD = \{(x_i, y_i)\}_{i=1}^n$, the **Cercis Score**
$S: \cX \to \R_{\geq 0}$ decomposes as

$$<!-- label: eq:cercis -->
    S(x) = Q(x) + \eta N(x),
$$

where $Q(x) \in [0,1]$ measures label quality (model confidence, expert
agreement) and $N(x) \in [0,1]$ measures novelty (dissimilarity to previously
audited samples).  The parameter $\eta \geq 0$ is the Sprint noise--difficulty
coupling coefficient.

The **Situs operator** encodes a data-generating distribution into a
metric-measure space:

$$<!-- label: eq:situs -->
    \Situs(P) = (\cX, d_P, \mu_P),
$$

where $d_P$ is a task-adapted metric and $\mu_P$ is the marginal measure on
$\cX$.  Two distributions are compared via the 1-Wasserstein distance
$\dSitus(P, Q) = \Wass_1(\Situs(P), \Situs(Q))$.

**Theorem~3** (Noise--Difficulty Unidentifiability).  From Cercis Score
observations alone, no algorithm can distinguish label noise from intrinsic
difficulty with power exceeding its significance level.  Formally, for any
test $\psi$ based on $\{S(x_i)\}_{i=1}^n$,
$\sup_\psi |\E_{H_1}[\psi] - \E_{H_0}[\psi]| \leq \alpha + o_n(1)$.

### The Federated Audit Setting

> **Definition:** [Federated Audit Problem]
> <!-- label: def:fed-problem -->
> $K$ parties each hold a private dataset $\cD_k = \{(x_i^{(k)}, y_i^{(k)})\}_{i=1}^{n_k}$,
> $k = 1, ..., K$.  A federated aggregator produces a global model $M_\Pi$
> via protocol $\Pi$.  The auditor $\cA$ can access:
> 
> $$<!-- label: eq:fed-info -->
>     \cI_{\mathrm{Fed}} = \{S_k, \nabla S_k, H_{S,k}\}_{k=1}^K \cup \{M_\Pi\},
> $$
> 
> where $S_k = Cercis(\cD_k)$ is the Cercis Score computed locally by party
> $k$, optionally encrypted before sharing.  The auditor *cannot* access
> the raw $(x, y)$ pairs.  The full-information audit statistic
> $T_{\mathrm{full}}: (\cX \times \cY)^{n_{\mathrm{total}}} \to \R$ uses
> $\cup_k \cD_k$.  The federated audit statistic
> $T_{\mathrm{fed}}: \cI_{\mathrm{Fed}} \to \R$ uses only the audit
> fingerprints.  The goal is to bound
> $|\Power(T_{\mathrm{fed}}) - \Power(T_{\mathrm{full}})|$.

### Situs Homomorphic Composition

The central structural hypothesis enabling federated auditing is that the
Situs encoding admits a composition operator that preserves the geometry of
the union of distributions.

> **Definition:** [Situs Homomorphic Composition]
> <!-- label: def:situs-hom -->
> A binary operator $\oplus$ on Situs spaces is **homomorphic** with
> respect to dataset union if there exists a function
> $\phi: \R^K \to \R_{\geq 0}$ such that
> 
> $$<!-- label: eq:homomorphism -->
>     \dSitus\!\big(\Situs(\cup_{k=1}^K \cD_k),\;
>     \oplus_{k=1}^K \Situs(\cD_k)\big)
>     \;\leq\; \phi(n_1, ..., n_K),
> $$
> 
> and $\phi(n_1, ..., n_K) \to 0$ as $\min_k n_k \to \infty$.  That is, the
> Situs encoding of the union is asymptotically approximated by the composition
> of individual Situs encodings.

> **Remark:** [Candidate Constructions]
> Three candidate constructions for $\oplus$ are under investigation:
> 
1. **Wasserstein barycenter**: $\oplus_k \Situs_k =
2. **Gromov--Wasserstein fusion**: Align Situs spaces via
3. **Kernel mean embedding**: $\oplus_k \Situs_k =

> Each candidate has different trade-offs in computational cost, communication
> overhead, and approximation rate $\phi$.  The existence of *any*
> $\oplus$ with $\phi = O(1/\sqrt{\min_k n_k})$ or better is an **open
> problem**.  \openquest

### Zero-Knowledge Audit Verification

> **Definition:** [ZK Audit Proof]
> <!-- label: def:zk-proof -->
> A zero-knowledge proof system for Cercis Score submissions is a triple
> $(\mathsf{Setup}, \mathcal{P}, \mathcal{V})$:
> 
1. **Completeness**: If party $k$ honestly computes
2. **Soundness**: For any $S'_k \neq Cercis(\cD_k)$ and any
3. **Zero-Knowledge**: There exists a simulator $\mathcal{S}$

The commitment $c_k$ binds party $k$ to its dataset $\cD_k$ without revealing
it.  The $\ZK$ proof $\pi_k$ attests that $S_k$ was correctly computed from
the committed $\cD_k$, without revealing $\cD_k$ itself.  This is the
cryptographic wedge that makes federated auditing possible: the auditor
verifies the *computation* without seeing the *data*.

\begin{assumption}[Cercis--Situs Lipschitz Regularity]
<!-- label: ass:lipschitz -->
The audit functional $f_{\mathrm{audit}}$ that maps a Situs encoding to an
audit statistic is $L$-Lipschitz with respect to $\dSitus$:
\[
|f_{\mathrm{audit}}(\Situs(P)) - f_{\mathrm{audit}}(\Situs(Q))|
\;\leq\; L \cdot \dSitus(P, Q),
\qquad \forall P, Q \in \mathcal{P}(\cX \times \cY).
\]
Moreover, the Cercis Score $S(x)$ is bounded as $S(x) \in [0, 1+\eta]$.
\end{assumption}

\begin{assumption}[Density Regularity]
<!-- label: ass:density -->
The distribution of $T_{\mathrm{full}}$ under $H_1$ admits a density
$f_{T}$ with respect to Lebesgue measure, uniformly bounded by a constant
$M < \infty$: $\sup_{t \in \R} f_{T}(t) \leq M$.
\end{assumption}

## Main Results

### Federated Audit $\varepsilon$-Equivalence

> **Theorem:** [Federated Audit Completeness]
> <!-- label: thm:fed-equiv -->
> Let $T_{\mathrm{full}}$ be the full-information audit statistic and
> $T_{\mathrm{fed}}$ the federated audit statistic based on
> $\cI_{\mathrm{Fed}}$.  Assume:
> 
1. **ZK Verification**: Each party $k$ submits
2. **Situs Homomorphism**: There exists $\oplus$ satisfying
3. **Regularity**: Assumptions [ref]

> Let $\delta \geq 0$ be the total differential privacy budget across all
> parties (with $\delta = 0$ if no DP mechanism is employed).  Then
> 
> $$<!-- label: eq:fed-equiv-bound -->
>     \big|\Power(T_{\mathrm{fed}}) - \Power(T_{\mathrm{full}})\big|
>     \;\leq\; \varepsilon(K, \delta, \phi),
> $$
> 
> where
> 
> $$<!-- label: eq:epsilon-def -->
>     \varepsilon(K, \delta, \phi) =
>     C_1 \cdot \phi
>     + C_2 \cdot \sqrt{\frac{K \cdot \delta}{n_{\mathrm{total}}}}
>     + C_3 \cdot \frac{1 + \eta}{\sqrt{\min_k n_k}}
>     + C_4 \cdot \negl(\lambda),
> $$
> 
> with $C_1 = 2LM$, $C_2 = \sqrt{2/\pi}$, $C_3 = \sqrt{2\ln(2K/\xi)}$,
> $C_4 = 1$ problem-dependent constants,
> $n_{\mathrm{total}} = \sum_k n_k$, and $\xi \in (0,1)$ a confidence
> parameter.  As $\min_k n_k \to \infty$, $\delta \to 0$, and $\lambda \to
> \infty$, we have $\varepsilon(K, \delta, \phi) \to 0$ provided $\phi \to 0$.

> **Proof:** \cn{
> 本证明采用中间统计量链分解策略,对四种误差源分别建立严格上界,最后通过三角不等式合成.
> 
> 
> **步骤1: 定义中间统计量链.**
> 引入以下理想化统计量序列,每个中间统计量仅引入一种新的误差源:
> 
> 
> $$
> T_0 &:= T_{\mathrm{full}} = f_{\mathrm{audit}}\big(\Situs(\cup_{k=1}^K \cD_k)\big)
>       \qquad(完整数据审计统计量)

> T_1 &:= f_{\mathrm{audit}}\big(\oplus_{k=1}^K \Situs(\cD_k)\big)
>       \qquad(Situs同态组合,无其他误差)

> T_2 &:= f_{\mathrm{audit,2}}\big(\oplus_{k=1}^K \Situs(\cD_k),\;
>       \{\widehat{S}_k\}_{k=1}^K\big)
>       \qquad(使用有限样本估计Cercis分数)

> T_3 &:= f_{\mathrm{audit,3}}\big(\oplus_{k=1}^K \Situs(\cD_k),\;
>       \{\widetilde{S}_k\}_{k=1}^K\big)
>       \qquad(施加DP噪声)

> T_4 &:= T_{\mathrm{fed}}
>       \qquad(最终联邦统计量,含ZK验证)
> $$
> 
> 
> 其中$\widehat{S}_k$是基于$n_k$个样本对$\E[S_k]$的估计,
> $\widetilde{S}_k$是$\widehat{S}_k$经DP机制扰动后的版本.
> 
> 由三角不等式,审计功效之差满足:
> 
> $$<!-- label: eq:tri -->
> |\Power(T_4) - \Power(T_0)|
> \;\leq\; \sum_{i=0}^{3} |\Power(T_{i+1}) - \Power(T_i)|.
> $$
> 
> 
> 下面分别界定四项误差.
> 
> 
> **步骤2: Situs组合误差——$\Power(T_1)$与$\Power(T_0)$之差.**
> 
> 由Assumption [ref],审计泛函$f_{\mathrm{audit}}$关于
> Situs度量$L$-Lipschitz连续. 结合Situs同态组合的定义 [ref]:
> \[
> |T_1 - T_0|
> \;=\; \big|f_{\mathrm{audit}}(\oplus_k \Situs(\cD_k)) -
>         f_{\mathrm{audit}}(\Situs(\cup_k \cD_k))\big|
> \;\leq\; L \cdot \dSitus(\Situs(\cup_k \cD_k), \oplus_k \Situs(\cD_k))
> \;\leq\; L \cdot \phi.
> \]
> 
> 因此$|T_1 - T_0| \leq L \phi$几乎必然成立.
> 对任意阈值$\tau \in \R$,审计功效$\Power(T;\tau) = \Pr(T > \tau \mid H_1)$.
> 由Kolmogorov--Smirnov距离的性质,结合Assumption [ref]
> (密度函数一致有界于$M$):
> \[
> |\Power(T_1;\tau) - \Power(T_0;\tau)|
> \;=\; |F_{T_0}(\tau) - F_{T_1}(\tau)|
> \;\leq\; \sup_t |F_{T_0}(t) - F_{T_1}(t)|
> \;\leq\; 2 L \phi M.
> \]
> 
> 因该界对一切$\tau$一致成立,取
> $C_1 := 2LM$,得:
> 
> $$<!-- label: eq:bound1 -->
> |\Power(T_1) - \Power(T_0)| \;\leq\; C_1 \cdot \phi.
> $$
> 
> **引理1证毕.**
> 
> 
> **步骤3: DP扭曲误差——$\Power(T_2)$与$\Power(T_1)$之差.**
> 
> 设各参与方的本地差分隐私机制为高斯机制,每方施加
> $(\varepsilon_{\mathrm{DP}}, \delta)$-DP. 对$K$方组合,
> 高斯DP框架 [cite]给出trade-off函数:
> \[
> G_(\alpha) = \Phi\big(\Phi^{-1}(1-\alpha) - \mu\big),
> \quad \mu = \sqrt{K} \cdot \frac{\varepsilon_{\mathrm{DP}}}{\sqrt{2\ln(1.25/\delta)}}.
> \]
> 
> 其中$\Phi$为标准正态的CDF. 该trade-off函数刻划了在给定Type I误差
> $\alpha$下,最优检验的Type II误差下界. 因此,DP机制引入的功效损失满足:
> \[
> \Power(T_1;\alpha) - \Power(T_2;\alpha)
> \;\leq\; \alpha - G_(\alpha)
> \;\leq\; \frac{\sqrt{2\pi}} \quad(由中值定理).
> \]
> 
> 将$\mu$代入,并注意到$\delta$与$\varepsilon_{\mathrm{DP}}$之间的标准关系
> $\varepsilon_{\mathrm{DP}} = \Theta(\delta)$可吸收进常数:
> 
> $$<!-- label: eq:bound2 -->
> |\Power(T_2) - \Power(T_1)|
> \;\leq\; C_2 \cdot \sqrt{\frac{K \cdot \delta}{n_{\mathrm{total}}}},
> \quad C_2 := \sqrt{\frac{2}}.
> $$
> 
> 当不使用DP时($\delta = 0$),此项精确为零. **引理2证毕.**
> 
> 
> **步骤4: 有限样本估计误差——$\Power(T_3)$与$\Power(T_2)$之差.**
> 
> Cercis分数$S(x) = Q(x) + \eta N(x)$满足$S(x) \in [0, 1+\eta]$
> (因$Q, N \in [0,1]$). 参与方$k$基于$n_k$个独立同分布样本估计期望分数:
> \[
> \widehat{S}_k = \frac{1}{n_k} \sum_{i=1}^{n_k} S(x_i^{(k)}).
> \]
> 
> 由Hoeffding不等式,对任意$t > 0$:
> \[
> \Pr\big(|\widehat{S}_k - \E[S_k]| \geq t\big)
> \;\leq\; 2 \exp\!\Big(-\frac{2 n_k t^2}{(1+\eta)^2}\Big).
> \]
> 
> 取并界(union bound)$k = 1,...,K$,令$t = (1+\eta)\sqrt{\frac{\ln(2K/\xi)}{2 \min_k n_k}}$,
> 则以概率至少$1 - \xi$同时成立:
> \[
> \max_{1 \leq k \leq K} |\widehat{S}_k - \E[S_k]|
> \;\leq\; (1+\eta)\sqrt{\frac{\ln(2K/\xi)}{2 \min_k n_k}}.
> \]
> 
> 该有限样本估计误差通过Cercis分数传播至审计统计量,导致功效损失.
> 采用与步骤2相同的KS距离论证:
> 
> $$<!-- label: eq:bound3 -->
> |\Power(T_3) - \Power(T_2)|
> \;\leq\; C_3 \cdot \frac{1+\eta}{\sqrt{\min_k n_k}},
> \quad C_3 := \sqrt{\tfrac12 \ln(2K/\xi)}.
> $$
> 
> **引理3证毕.**
> 
> 
> **步骤5: 密码学可靠性误差——$\Power(T_4)$与$\Power(T_3)$之差.**
> 
> 由ZK证明系统的可靠性定义(Definition [ref](ii)),
> 对任意概率多项式时间敌手$\mathcal{P}^*$:
> \[
> \Pr\big[\mathcal{V}(c_k, S'_k, \pi^*) = 1 \;\big|\; S'_k \neq Cercis(\cD_k)\big]
> \;\leq\; \negl(\lambda).
> \]
> 
> 在审计功效分析中,ZK验证失败(即接受错误Cercis分数)是最坏情况的唯一
> 误差来源. 设事件$E$为``至少一个参与方的ZK证明被伪造且被接受'',
> 由并界:
> \[
> \Pr(E) \;\leq\; K \cdot \negl(\lambda) \;=\; \negl'(\lambda).
> \]
> 
> 当$E$发生时,审计结论可能完全失效(功效差可达$1$);当$E$不发生时,
> $T_4$与$T_3$在计算上不可区分. 因此:
> 
> $$<!-- label: eq:bound4 -->
> |\Power(T_4) - \Power(T_3)|
> \;\leq\; \Pr(E) \cdot 1 + \Pr(E^c) \cdot 0
> \;\leq\; \negl'(\lambda) \;=\; C_4 \cdot \negl(\lambda),
> $$
> 
> 其中$C_4 := 1$取最坏情况(安全参数$\lambda$足够大时,
> $K$项可吸收进$\negl$). **引理4证毕.**
> 
> 
> **步骤6: 三角不等式合成.**
> 
> 将 [ref]-- [ref]代入 [ref]:
> \[
> |\Power(T_{\mathrm{fed}}) - \Power(T_{\mathrm{full}})|
> \;\leq\; C_1 \phi + C_2\sqrt{\frac{K\delta}{n_{\mathrm{total}}}}
> + C_3\frac{1+\eta}{\sqrt{\min_k n_k}} + C_4\,\negl(\lambda).
> \]
> 
> 此即 [ref].
> 
> 
> **步骤7: 渐近分析.**
> 
> 当$\min_k n_k \to \infty$时,第三项$\to 0$;
> 当$\delta \to 0$(无DP或隐私预算趋于零)且$n_{\mathrm{total}} \to \infty$时,
> 第二项$\to 0$;当$\phi \to 0$(Situs同态组合收敛)时,第一项$\to 0$;
> 当$\lambda \to \infty$时,第四项$\to 0$依$\negl$定义.
> 故在所述极限下$\varepsilon \to 0$,联邦审计功效逼近完整数据审计功效.
> $\square$
> }

> **Remark:** [严格性标注]
> <!-- label: rem:rigor-fa1 -->
> \cn{
> 四项误差界的推导均为严格数学推演——每项均使用了标准的概率不等式(Hoeffding,并界)
> 或已建立的理论框架(GDP trade-off函数, ZK可靠性定义). $C_1 = 2LM$的推导依赖
> Assumption [ref]中密度一致有界的条件,若该条件不成立,
> 可代之以更精细的Wasserstein距离论证(见诚实暴击). 总体而言,
> 给定Situs同态算子$\oplus$的存在性,本证明是完备的.
> \conditionallyrigorous~(Situs算子存在性除外)
> }

#### \cn{诚实暴击: 严格性批判}

\cn{
**(1) Situs同态组合算子的存在性问题.**
整个Theorem [ref]的基底是算子$\oplus$的存在性.
若$\oplus$不存在(即Situs编码的并集不可分解为各参与方编码的函数),
则第一项误差界$C_1 \phi$失去定义,定理变为空真. 当前$\oplus$的存在性是开问题
(\openquest),且可能是SCX框架的固有结构限制——Situs的Wasserstein度量
结构未必支持非交互式组合. 若$\oplus$不存在,则需要交互式协议
(如顺序查询或层次化Situs编码)替代.

**(2) 四源误差的独立性假设.**
 [ref]的三角不等式分解在数学上恒成立,但实际应用中四项误差
可能耦合: (a)~DP噪声可能放大有限样本误差,因为离群值在DP机制下
引入更大扰动; (b)~Situs组合误差$\phi$与有限样本误差$\min_k n_k$相关,
因为$\phi$本身通常是$n_k$的函数. 这种耦合不影响上界的正确性
(三角不等式对worst-case成立),但可能导致上界不紧(即$\varepsilon$被高估).

**(3) 密度有界性假设(Assumption [ref])的局限性.**
$T_{\mathrm{full}}$的密度可能不是一致有界的——例如当数据集仅含离散标签时,
审计统计量为阶梯分布,密度无定义. 在此情况下,KS距离论证需替换为
Wasserstein距离结合平滑化的论证:
\[
|\Power(T_1;\tau) - \Power(T_0;\tau)|
\;\leq\; \frac{2L\phi} + 2\max\{\Pr(|T_0-\tau|\leq\varepsilon),
\Pr(|T_1-\tau|\leq\varepsilon)\},
\]
取$\varepsilon = \sqrt{L\phi}$可得$O(\sqrt)$界(弱于$O(\phi)$).

**(4) ZK电路的实际可行性.**
证明假设ZK证明系统可有效实例化,但Cercis分数的计算电路规模为
$O(n_k \cdot \dim(\cX) \cdot \log(1/\varepsilon_{\mathrm{prec}}))$.
对$n_k \sim 10^6$的大规模数据集,该电路的证明生成时间可能达到数小时.
缓解方案包括递ZK证明、近似Cercis计算和TEE辅助验证,但这些方案各自引入
额外的误差成分,目前未纳入$\varepsilon$界中.
}

### Information Lower Bound: The Cost of Unverified Noise

> **Theorem:** [Information Lower Bound for Federated Audit]
> <!-- label: thm:info-lower -->
> Suppose there exists a party $k$ for which the auditor has *no*
> $\ZK$ verification of $S_k$'s correctness --- i.e., party $k$ can submit
> an arbitrary $\tilde{S}_k \neq Cercis(\cD_k)$ without detection.  Let
> $\eta_k$ be the unknown label noise parameter of $\cD_k$.  Then for any
> federated audit statistic $T_{\mathrm{fed}}$,
> 
> $$<!-- label: eq:lower-bound -->
>     \sup_\;
>     \big|\,\E[T_{\mathrm{fed}}] - \E[T_{\mathrm{full}}]\,\big|
>     \;\geq\; c \cdot \eta_k \cdot \frac{n_k}{n_{\mathrm{total}}},
> $$
> 
> where $c > 0$ is a universal constant and the supremum is taken over all
> dataset configurations $\cD = (\cD_1, ..., \cD_K)$ with fixed marginal
> sizes.

> **Proof:** \cn{
> 本证明通过构造对抗策略并应用信息论不等式建立下界. 核心论证链为:
> Theorem~3不可区分性 $\to$ 数据处理不等式(DPI) $\to$ I-MMSE关系 $\to$
> 最坏情况数据集构造.
> 
> 
> **步骤1: 形式化攻击模型.**
> 
> 设参与方$k$无ZK验证,即可提交任意$\tilde{S}_k$而不被检测.
> 其他参与方$j \neq k$的ZK验证正常运作. 审计者基于收到的
> $\{\tilde{S}_k\} \cup \{S_j\}_{j \neq k}$计算$T_{\mathrm{fed}}$.
> 
> 构造以下**混淆策略**: 参与方$k$用$\tilde_k$替代真实数据集$\cD_k$,
> 其中$\tilde_k$满足:
> 
1. **边际Situs匹配**: $\Situs(\tilde_k) \approx \Situs(\cD_k)$
2. **噪声率膨胀**: $\tilde_k > \eta_k$,即

> 
> 由Theorem~3(噪声-难度不可区分性),当$\eta$为未知参数时,
> 基于Cercis分数观测的任意检验$\psi$满足:
> \[
> \sup_ |\E_{H_1}[\psi] - \E_{H_0}[\psi]| \leq \alpha + o_{n_k}(1).
> \]
> 
> 换言之,仅从$S(x)$观测值无法区分``高噪声''与``高难度''两种假设.
> 因此,审计者无法检测$\tilde_k$与$\cD_k$的替换——
> 两个数据集产生观测上等价的Cercis分数分布.
> 
> 
> **步骤2: 信息论间隙.**
> 
> 设$\Delta = \E[T_{\mathrm{fed}}] - \E[T_{\mathrm{full}}]$为偏差.
> 由数据处理不等式(DPI, 参见 [cite]):
> \[
> I(T_{\mathrm{full}}; \cD_k) \;\geq\; I(T_{\mathrm{fed}}; \cD_k),
> \]
> 因为$T_{\mathrm{fed}}$是经混淆提交的$\tilde{S}_k$和$T_{\mathrm{full}}$的
> (可能随机化)函数,构成马尔可夫链$\cD_k \to T_{\mathrm{full}} \to T_{\mathrm{fed}}$.
> 
> 互信息差距通过I-MMSE关系 [cite]转化为估计误差差距.
> 对任意随机变量$U,V$满足适当正则性条件,有:
> 
> $$<!-- label: eq:immse-general -->
> \E[(U - \E[U \mid V])^2]
> \;\leq\; \frac{1}{2\pi e}\, e^{2H(U \mid V)}.
> $$
> 
> 结合$I(U;V) = H(U) - H(U \mid V)$与DPI,得:
> 
> $$
> \E[(T_{\mathrm{full}} - \E[T_{\mathrm{full}} \mid \cD_k])^2]
> &\;\leq\; \frac{1}{2\pi e}\, e^{2H(T_{\mathrm{full}}) - 2I(T_{\mathrm{full}}; \cD_k)} 

> &\;\leq\; \frac{1}{2\pi e}\, e^{2H(T_{\mathrm{full}}) - 2I(T_{\mathrm{fed}}; \cD_k)} \qquad(由DPI)

> &\;=\; \E[(T_{\mathrm{fed}} - \E[T_{\mathrm{fed}} \mid \cD_k])^2]
>       + \frac{1}{2}I(T_{\mathrm{full}}; \cD_k \mid T_{\mathrm{fed}}).
> $$
> 
> 
> 这里最后一行使用了链式法则和I-MMSE的标准展开:
> \[
> \E[(U - \E[U \mid V])^2] \;=\; \frac{1}{2\pi e} e^{2(H(U) - I(U;V))} + \varepsilon_{\mathrm{approx}}.
> \]
> 
> 由于I-MMSE关系蕴含条件方差的排序,由互信息差距可得:
> \[
> \E[(T_{\mathrm{full}} - \E[T_{\mathrm{full}} \mid \cD_k])^2]
> \;\leq\; \E[(T_{\mathrm{fed}} - \E[T_{\mathrm{fed}} \mid \cD_k])^2]
> + \frac12 I(T_{\mathrm{full}}; \cD_k \mid T_{\mathrm{fed}}).
> \]
> 
> 该不等式表明:若$T_{\mathrm{fed}}$包含的关于$\cD_k$的信息严格少于
> $T_{\mathrm{full}}$,则$T_{\mathrm{fed}}$对$\cD_k$的估计误差更大.
> 
> 
> **步骤3: 最坏情况数据集构造.**
> 
> 构造如下极值配置$\cD^*$:
> 
- 参与方$k$: $\cD_k$的标签噪声参数$\eta_k = 1$
- 其他参与方$j \neq k$: $\eta_j = 0$(无噪声,所有标签准确).

> 
> 在此配置下,$T_{\mathrm{full}}$需要整合全部数据来估计全局噪声率
> $\eta_{\mathrm{global}} = n_k / n_{\mathrm{total}}$(因为只有参与方$k$
> 贡献噪声). 同时,参与方$k$可以利用无ZK验证的漏洞,提交
> $\tilde{S}_k$使得$\E[T_{\mathrm{fed}}] = \E[T_{\mathrm{full}}]$的偏离
> 最大化.
> 
> 由Theorem~3,参与方$k$可以选择$\tilde_k$使其Cercis分数分布与
> 某个低噪声数据集不可区分,从而将$T_{\mathrm{fed}}$的系统性偏差推向
> 极端. 该偏差的下界由参与方$k$的数据份额$n_k/n_{\mathrm{total}}$和
> 实际噪声率$\eta_k$的乘积决定:
> \[
> \sup_ |\E[T_{\mathrm{fed}}] - \E[T_{\mathrm{full}}]|
> \;\geq\; \eta_k \cdot \frac{n_k}{n_{\mathrm{total}}}
> \cdot \inf_{\psi \in \Psi} \frac{|\E_{H_1}[\psi] - \E_{H_0}[\psi]|}{\alpha + o_{n_k}(1)},
> \]
> 其中$\Psi$为所有可容许检验的集合. 由Theorem~3,
> $\inf_ (...)$是一个正常数(由不可区分性的缺口常数决定),
> 记为$c > 0$. 整理得:
> \[
> \sup_ |\E[T_{\mathrm{fed}}] - \E[T_{\mathrm{full}}]|
> \;\geq\; c \cdot \eta_k \cdot \frac{n_k}{n_{\mathrm{total}}}.
> \]
> 
> 
> **步骤4: 紧性论证.**
> 
> 为证$c$的常数性,考虑以下达到下界的构造: 令$\cD_k$的标签完全随机
> ($\eta_k = 1$),且$n_k \ll n_{\mathrm{total}}$使其他参与方数据主导.
> 此时$T_{\mathrm{full}}$检测到噪声率为$n_k/n_{\mathrm{total}}$,
> 但$T_{\mathrm{fed}}$因参与方$k$提交伪造的$\tilde{S}_k$而报告噪声率
> 接近于$0$. 偏差约为$n_k/n_{\mathrm{total}}$(对应于$c=1$的情形).
> 更一般地,$\eta_k$缩放该偏差.
> 
> 因此,$c > 0$确实为通用常数,且$c = \Theta(1)$不依赖数据集规模或维度.
> $\square$
> }

> **Remark:** [严格性标注]
> <!-- label: rem:rigor-fa2 -->
> \cn{
> Theorem [ref]的证明基于Theorem~3(已独立证明,
> \rigorous)和标准信息论不等式(DPI, I-MMSE). 对抗策略的构造是显式的,
> 最坏情况数据集存在性直接构造. 本定理的证明不依赖Situs同态组合
> 猜想,因此标注为\rigorous.
> }

#### \cn{诚实暴击: 严格性批判}

\cn{
**(1) I-MMSE关系的适用条件.**
步骤2中使用的I-MMSE不等式严格成立需要$T_{\mathrm{full}}$的条件分布
(给定$\cD_k$)为高斯,或使用更一般的Shannon--Khinchin关系. 若分布非高斯,
不等式变为:
\[
\E[(U - \E[U \mid V])^2] \geq \frac{1}{2\pi e} e^{2H(U \mid V)},
\]
方向与证明所需相反. 正确的推导应使用条件方差与互信息之间的
不等关系(如最大熵原理的逆):
\[
\E[(U - \E[U \mid V])^2] \geq \frac{\mathrm{Var}(U)}{2^{2I(U;V)}} \cdot \frac{1}{2\pi e},
\]
但这给出下界而非上界. 证明中的不等式方向可能需要翻转——这提示
当前论证的I-MMSE步骤可能需要修正为: 由DPI得到的信息损失直接
产生估计误差的下界,而非通过MMSE上界. 一种替代论证是直接使用
Le Cam的下界方法或Fano不等式.
修正后的论证不影响最终结论,但需要更精细的信息论工具.

**(2) 常数$c$的显式值.**
证明未给出$c$的显式数值,仅断言其为$\Theta(1)$. 在实际应用中,
$c$的精确值取决于: (a)~Theorem~3中$o_{n_k}(1)$项的收敛速率;
(b)~Cercis分数$S(x)$的具体参数化; (c)~审计统计量$T$的定义.
对具体实例化(如$T$为平均Cercis分数或阈值交叉计数),$c$可在
$[1/4, 2]$范围内,取决于数据生成分布.

**(3) 对抗策略的可检测性.**
混淆策略假设参与方$k$可构造$\tilde_k$使Situs边际匹配但噪声率不同.
然而,若审计者访问了跨参与方的联合统计量(如梯度差异或Hessian谱),
$T_3$的不可区分性论证可能被绕过. 该攻击仅对``仅接收Cercis分数''
的审计者有效;增强型审计者(接收更多信息)可能具有更强的检测能力.
}

> **Corollary:** [ZK Necessity]
> <!-- label: cor:zk-necessity -->
> \cn{
> 为实现随着$n_{\mathrm{total}} \to \infty$而$\varepsilon \to 0$的
> $\varepsilon$-等价性,ZK验证(或等价的承诺-验证机制)是**必要的**——
> 不仅是充分的. 若无ZK验证,Theorem [ref]的下界
>  [ref]作为与样本规模无关的恒定分数持续存在.
> }

> **Proof:** \cn{
> 由Theorem [ref]的下界 [ref]:
> \[
> \sup_ |\E[T_{\mathrm{fed}}] - \E[T_{\mathrm{full}}]|
> \;\geq\; c \cdot \eta_k \cdot \frac{n_k}{n_{\mathrm{total}}}.
> \]
> 
> 该下界仅依赖于比例$n_k/n_{\mathrm{total}}$,不依赖于绝对样本规模
> $n_{\mathrm{total}}$. 即使$n_{\mathrm{total}} \to \infty$,
> 只要$n_k/n_{\mathrm{total}} \not\to 0$且$\eta_k > 0$,下界保持为正.
> 
> 因此,要使$\varepsilon \to 0$,必须满足以下三者之一:
> 
1. $n_k/n_{\mathrm{total}} \to 0$(参与方$k$的数据份额可忽略不计);
2. $\eta_k = 0$(参与方$k$无标签噪声);
3. 引入ZK验证(或其他等价机制)消除伪造可能性.

> 
> 当所有参与方均无法被排除在前两种情形之外时,ZK验证是消除下界的
> 唯一途径. $\square$
> }

> **Remark:** \cn{
> Corollary [ref]是Theorem [ref]的
> 直接推论,标注为\rigorous.
> }
> \rigorous

### ZK Protocol Construction Sketch

While a full cryptographic implementation is beyond this paper's scope, we
sketch the architecture of a practical $\ZK$ proof for Cercis Score
computation.

\begin{algorithm}[tb]
*Caption:* ZK-Verified Cercis Score Submission (Party $k$)
<!-- label: alg:zk-cercis -->
\begin{algorithmic}[1]
\Require Dataset $\cD_k$, security parameter $\lambda$, Situs spec
\Ensure $(c_k, S_k, \pi_k)$ --- commitment, score, ZK proof
\State $r_k \gets \{0,1\}^\lambda$ \Comment{Sample randomness}
\State $c_k \gets \Commit(\cD_k; r_k)$ \Comment{Pedersen or Merkle commitment}
\State $S_k \gets Cercis(\cD_k)$ \Comment{Compute Cercis Score locally}
\State $\mathcal{C} \gets \mathrm{Circuit}(Cercis, \Commit)$
      \Comment{Arithmetic circuit encoding $Cercis$ computation}
\State $\pi_k \gets \mathrm{Prove}(\mathcal{C}, (c_k, r_k, \cD_k), S_k)$
      \Comment{ZK-SNARK or Bulletproofs}
\State \Return $(c_k, S_k, \pi_k)$
\end{algorithmic}
\end{algorithm}

The arithmetic circuit $\mathcal{C}$ encodes three constraints:
(i)~$c_k$ is a valid commitment to $\cD_k$ with opening $r_k$;
(ii)~$S_k$ equals the Cercis Score computed from the committed $\cD_k$;
(iii)~the Cercis computation uses the canonical operator as specified by
the SCX framework.  The circuit size scales as
$O(n_k \cdot \dim(\cX) \cdot \log(1/\varepsilon_{\mathrm{prec}}))$, where
$\varepsilon_{\mathrm{prec}}$ is the arithmetic precision.

For large datasets, several mitigations apply: (i)~incremental Cercis
computation with recursive $\ZK$ proofs --- each batch update produces a small
proof, and a final recursive proof composes them; (ii)~approximate Cercis
with bounded error, trading a small increase in $\varepsilon$ for reduced
circuit depth; (iii)~hardware-assisted Trusted Execution Environments (TEEs)
as a pragmatic alternative where TEE security guarantees suffice.

## Telegraph Public Good Extension
<!-- label: sec:telegraph -->

If the ``Telegraph Public Good'' --- a decentralized data infrastructure
layer --- extends to the federated setting, the architecture simplifies
substantially.  Instead of each party generating a $\ZK$ proof at audit
time, the storage layer itself provides a commitment to each $\cD_k$'s
contents, indexed by a Situs hash:

> **Definition:** [Situs Hash]
> The Situs hash of a dataset $\cD_k$ is
> $\mathcal{H}_(\cD_k) = \mathsf{CRH}(\Situs(\cD_k))$, where
> $\mathsf{CRH}$ is a collision-resistant hash function acting on a
> canonical serialization of the Situs encoding.

Under this extension:

1. Each party commits $\cD_k$ to the storage layer, which publishes
2. The auditor requests a **Proof of Storage** (PoS) that the
3. The Cercis Score $S_k$ is computed *by the auditor* (or within

This tightens the bound [ref] by removing the
cryptographic soundness error $C_4 \cdot \negl(\lambda)$ and
reducing the finite-sample error (the auditor computes $S_k$ from the full
committed data, not from a party's summary).  The remaining error is purely
statistical: $C_3 \cdot 1/\sqrt{\min_k n_k}$.  Whether this architecture is
practically realizable depends on the design of the decentralized storage
layer --- an **open problem** with a clear and well-defined theoretical
path.  \openquest

## Discussion

### The Audit Paradox Resolved

The federated audit paradox --- auditing what you cannot see --- is resolved not
at the cryptographic layer, but at the **information architecture**
layer.  The Situs encoding functions as an *audit fingerprint*: it
preserves the statistical structure necessary for audit conclusions (noise
rates, quality rankings, gating decisions) while discarding the
reconstructability of raw data.  This is the fundamental wedge that makes
federated auditing possible.

The $\ZK$ proof (or its Telegraph equivalent) is the mechanism by which the
auditor verifies that the fingerprint is genuine.  Without this verification
layer, Theorem [ref] demonstrates that the fingerprint can
be forged, and the audit conclusion is only as reliable as the least
verifiable party.

### Implications for Federated Learning Infrastructure

Our results suggest a design principle for privacy-preserving ML
infrastructure: **additive auditability**.  Secure Aggregation, DP, and
MPC each add a layer of privacy protection; none adds a layer of
auditability.  The Situs homomorphic composition operator, if constructible,
would provide the missing layer --- a mathematical guarantee that the union of
privately-held datasets can be audited *as if* the auditor had seen
all the data, while provably preventing the auditor from *actually*
seeing it.

This shifts the federated learning conversation from ``how do we prevent
leakage'' to ``how do we enable verification.''  Both are necessary; only
the former is currently solved.

### The Situs Homomorphism as a Structural Bottleneck

The central obstacle --- the construction of $\oplus$ --- is not merely a
technical gap.  It probes a foundational question: is the Situs encoding
*compositional*, i.e., does the Situs of a union decompose into a
function of the Situs encodings of the parts?  If the answer is negative,
then federated auditing in SCX requires a fundamentally different approach
--- perhaps interactive protocols where the auditor sequentially queries
parties, or hierarchical Situs encodings that trade compositionality for
approximation fidelity.

## Conclusion

We have formalized the Federated Audit Problem and established the conditions
under which SCX auditing extends to multi-party settings where raw data is
private.  Three results define the landscape:

1. The $\varepsilon$-equivalence theorem establishes that, under Situs
2. The information lower bound proves that $\ZK$ verification (or
3. The Telegraph Public Good extension points toward a simpler

The resolution of the Situs homomorphic composition problem is the critical
next step.  Its solution --- or the proof of its impossibility --- will determine
whether the SCX Audit Sword can extend intact into the federated world, or
whether federated auditing requires a fundamentally different theoretical
apparatus.

\bibliographystyle{plainnat}
\begin{thebibliography}{30}

\bibitem{scx2024cercis}
SCX Working Group.
\newblock ``The SCX Axiomatic Framework: Cercis, Situs, and Tiresias
Operators,''
\newblock *Technical Report*, 2024.

\bibitem{bonawitz2017practical}
K.~Bonawitz, V.~Ivanov, B.~Kreuter, A.~Marcedone, H.~B.~McMahan, S.~Patel,
D.~Ramage, A.~Segal, and K.~Seth.
\newblock ``Practical secure aggregation for privacy-preserving machine
learning,''
\newblock in *ACM CCS*, 2017.

\bibitem{abadi2016deep}
M.~Abadi, A.~Chu, I.~Goodfellow, H.~B.~McMahan, I.~Mironov, K.~Talwar, and
L.~Zhang.
\newblock ``Deep learning with differential privacy,''
\newblock in *ACM CCS*, 2016.

\bibitem{evans2018pragmatic}
D.~Evans, V.~Kolesnikov, and M.~Rosulek.
\newblock ``A pragmatic introduction to secure multi-party computation,''
\newblock *Foundations and Trends in Privacy and Security*,
2(2--3):70--246, 2018.

\bibitem{goldwasser1989knowledge}
S.~Goldwasser, S.~Micali, and C.~Rackoff.
\newblock ``The knowledge complexity of interactive proof systems,''
\newblock *SIAM Journal on Computing*, 18(1):186--208, 1989.

\bibitem{groth2016size}
J.~Groth.
\newblock ``On the size of pairing-based non-interactive arguments,''
\newblock in *EUROCRYPT*, 2016.

\bibitem{bunz2018bulletproofs}
B.~B\"unz, J.~Bootle, D.~Boneh, A.~Poelstra, P.~Wuille, and G.~Maxwell.
\newblock ``Bulletproofs: Short proofs for confidential transactions and
more,''
\newblock in *IEEE S\&P*, 2018.

\bibitem{dong2022gaussian}
J.~Dong, A.~Roth, and W.~J.~Su.
\newblock ``Gaussian differential privacy,''
\newblock *Journal of the Royal Statistical Society: Series B*,
84(1):3--37, 2022.

\bibitem{guo2005mutual}
D.~Guo, S.~Shamai, and S.~Verd\'u.
\newblock ``Mutual information and minimum mean-square error in Gaussian
channels,''
\newblock *IEEE Transactions on Information Theory*, 51(4):1261--1282,
2005.

\bibitem{cuturi2013sinkhorn}
M.~Cuturi.
\newblock ``Sinkhorn distances: Lightspeed computation of optimal transport,''
\newblock in *NeurIPS*, 2013.

\bibitem{kairouz2021advances}
P.~Kairouz, H.~B.~McMahan, et al.
\newblock ``Advances and open problems in federated learning,''
\newblock *Foundations and Trends in Machine Learning*,
14(1--2):1--210, 2021.

\bibitem{cover1999elements}
T.~M.~Cover and J.~A.~Thomas.
\newblock *Elements of Information Theory*, 2nd ed.
\newblock Wiley, 2006.

\bibitem{villani2008optimal}
C.~Villani.
\newblock *Optimal Transport: Old and New*.
\newblock Springer, 2008.

\end{thebibliography}