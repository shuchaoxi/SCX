*Abstract:*

We present a rigorous formalization of **quantum-secured audit communication**
for the SCX (Situs Consensus eXpert) framework. The core insight is that the
security of M_t\ parameter transmission and audit result delivery can be
elevated from computational hardness to **information-theoretic security**
via quantum mechanical principles. We develop four contributions:
three main theoretical results plus a practical feasibility analysis:

**(1) BB84 Protocol for M_t\ Transmission** (Section [ref]): We
formalize the Bennett--Brassard 1984 quantum key distribution protocol as the
secure channel for transmitting M_t\ parameters from the auditor (Alice) to the
audit ledger. We prove that any eavesdropping attempt by a malicious entity
introduces a detectable error rate $\varepsilon > 0$: for the simplest
intercept-resend attack, the expected error rate is $25\%$ per sifted bit,
far exceeding the protocol's abort threshold of $\sim\!11\%$. This guarantee
follows from the no-cloning theorem and the uncertainty principle, not from
unproven computational assumptions.

**(2) Audit Entanglement** (Section [ref]): We introduce
the concept of *audit entanglement*, where two auditors (e.g., Spring and
Yajie) share entangled quantum states. Measuring one auditor's state
reveals perfect correlations with the other's outcome (a non-signaling
quantum effect). We prove an **Entanglement Audit Theorem**:
if the two auditors share a maximally entangled Bell pair and an adversary
tampers with one half, the fidelity of the shared state drops as
$F \leq 1 - \delta_{tamper}$, making the tampering detectable with
probability arbitrarily close to 1 after $O(1/\delta_{tamper})$
independent measurements.

**(3) Quantum Audit Channel** (Section [ref]): We formally
define the quantum audit channel $\cN_{audit}$ and prove its capacity
theorem: the maximum rate of reliable audit information transmission is bounded
by the Holevo quantity $\chi(\cN_{audit})$, which for a depolarizing
channel with noise parameter $p$ is
$C_Q = 1 - H_2(2p/3)$
where $H_2$ is the binary entropy function and $p$ is the depolarizing
probability.

**(4) Practical Feasibility** (Section [ref]): We analyze
hardware requirements, existing quantum network infrastructure, and a phased
deployment roadmap. We conclude that while full quantum-secured audit is not
yet deployable at scale, a hybrid classical-quantum approach using
quantum-resistant post-quantum cryptography (CRYSTALS-Kyber) combined with
entanglement-based timestamping is feasible today.

**Keywords:** quantum key distribution, BB84, audit security,
entanglement, quantum channel capacity, SCX, tamper-proof auditing,
information-theoretic security

\rule{0.5pt}

<div align="center">

**摘要**

</div>

本文对SCX（位点共识专家）框架中的**量子安全审计通信**进行了严格形式化。
核心思想是：M_t\ 参数传输和审计结果交付的安全性可以从计算复杂度提升到
**信息论安全**，通过量子力学原理实现。我们发展了四项贡献：
三项主要理论结果加上一项实际可行性分析：

**(1) M_t\ 传输的BB84协议**（第 [ref]节）：我们将Bennett--Brassard 1984
量子密钥分发协议形式化为从审计者（Alice）到审计账本的M_t\ 参数安全传输通道。
我们证明任何恶意实体的窃听尝试都会引入可检测的错误率 $\varepsilon > 0$，
对于截获-重发攻击，预期错误率为 $25\%$，远超协议中止阈值 $\sim 11\%$——这一保证来自不可克隆定理和不确定性原理，
而非未经证明的计算假设。

**(2) 审计纠缠**（第 [ref]节）：我们引入*审计纠缠*概念，
即两个审计者（如Spring和Yajie）共享纠缠量子态。测量一个审计者的状态
揭示了与另一个审计者结果的完美关联（非信号的量子效应）。我们证明**纠缠审计定理**：如果两个审计者共享一个最大纠缠
Bell对且对手篡改其中一半，共享态的保真度下降为
$F \leq 1 - \delta_{tamper}$，使得篡改在经过
$O(1/\delta_{tamper})$ 次独立测量后以任意接近1的概率被检测到。

**(3) 量子审计信道**（第 [ref]节）：我们正式定义了量子审计信道
$\cN_{audit}$并证明了其容量定理：可靠审计信息传输的最大速率由Holevo量
$\chi(\cN_{audit})$ 界定，对于噪声参数为 $p$ 的去极化信道，
$C_Q = 1 - H_2(2p/3)$。

**(4) 实际可行性**（第 [ref]节）：我们分析了硬件需求、现有
量子网络基础设施和分阶段部署路线图。我们的结论是，虽然完全量子安全的审计
尚未能大规模部署，但结合抗量子后量子密码学（CRYSTALS-Kyber）和基于纠缠的
时间戳的混合经典-量子方法今天已可行。

**关键词：** 量子密钥分发，BB84，审计安全，纠缠，量子信道容量，
SCX，防篡改审计，信息论安全

## Introduction: Why Quantum for Audit Security?
<!-- label: sec:intro -->
\setcounter{page}{1}

### The Audit Security Problem
<!-- label: sec:intro_problem -->

In the SCX auditing framework, the parameter vector $M_t \in \R^d$ encodes the
audit configuration at time $t$: which data partitions to audit, which expert
models to query, the consensus threshold $\tau_t$, and the Yajie/Cercis
weighting parameters. The integrity of $M_t$ is fundamental: if a malicious
entity can intercept and modify $M_t$, the entire audit becomes compromised.

The threat model is severe. Consider a well-resourced adversary — a corporate
entity whose AI system is being audited — who wishes to manipulate audit results.
The adversary can:

1. **Intercept** $M_t$ in transit and substitute a forged $M_t'$
2. **Replay** a previously valid $M_t$ from a benign audit episode
3. **Man-in-the-middle** the audit results $\AuditResult_t$,

Traditional cryptographic solutions (RSA, ECDSA, AES-GCM) rely on
**computational hardness assumptions**: integer factorization, elliptic
curve discrete logarithm, or AES resistance to differential cryptanalysis.
All of these assumptions are vulnerable to:

- **Quantum attacks:** Shor's algorithm [cite] breaks RSA
- **Advances in classical cryptanalysis:** The history of
- **Implementation flaws:** Side-channel attacks, weak randomness,

### Information-Theoretic Security via Quantum Mechanics
<!-- label: sec:intro_quantum -->

Quantum mechanics offers a qualitatively different security guarantee:
**information-theoretic security**, also called *unconditional security*.
This means security that holds against *any* adversary, regardless of
computational resources — even against an adversary with a universal quantum
computer, infinite classical computing power, and arbitrary mathematical
breakthroughs.

The security derives from two fundamental principles of quantum mechanics:

> **Definition:** [No-Cloning Theorem [cite]]
> <!-- label: def:noclone -->
> There exists no unitary operation $U$ acting on $\cH_A \otimes \cH_B$ such that
> for all states $\ket_A \in \cH_A$,
> \[
> U(\ket_A \otimes \ket{0}_B) = \ket_A \otimes \ket_B.
> \]
> An unknown quantum state cannot be perfectly copied.
> 
> *不可克隆定理：未知量子态不能被完美复制。*

> **Definition:** [Measurement Disturbance]
> <!-- label: def:disturb -->
> Any measurement of a quantum system that does not commute with the system's
> state necessarily disturbs that state. Formally, if $[\hat{O}, \rho] \neq 0$,
> then measuring $\hat{O}$ changes $\rho$ to $\rho' \neq \rho$.
> 
> *测量扰动：任何与系统状态不对易的测量必然扰动该系统状态。*

These principles yield a profound implication for audit security:
**any eavesdropping attempt on a quantum channel inevitably leaves
detectable traces**. The adversary cannot copy the transmitted qubits
(no-cloning), and any measurement to extract information disturbs the state
(measurement disturbance), which the legitimate parties can detect through
statistical tests on a subset of the transmission.

\begin{bilingual}
{Core Insight / 核心洞察}
{Unlike classical cryptography, which bets on the continued hardness of
certain mathematical problems, quantum audit security bets on the laws of
physics. The Heisenberg uncertainty principle and the no-cloning theorem
are not conjectures — they are experimentally verified features of our
universe. This makes quantum-secured audit fundamentally more robust than
any classical alternative.}
\end{bilingual}

### Related Work
<!-- label: sec:related -->

Our work builds on several foundations:

- **BB84 Protocol** [cite]: The original quantum key
- **Ekert91 Protocol** [cite]: Entanglement-based
- **Quantum Channel Capacity** [cite]:
- **SCX Audit Theory** [cite]: The foundational
- **Audit Instantons** [cite]: Topological
- **Quantum Measurement in SCX** [cite]:
- **Quantum Networks** [cite]: Practical
- **Post-Quantum Cryptography** [cite]: NIST

### Paper Organization
<!-- label: sec:org -->

Section [ref] formalizes the BB84 protocol for M_t\ transmission.
Section [ref] develops audit entanglement theory.
Section [ref] defines the quantum audit channel and proves its
capacity bounds. Section [ref] analyzes practical feasibility.
Section [ref] integrates quantum audit into the SCX framework.
Section [ref] concludes.

## BB84 Protocol for M_t\ Parameter Transmission
<!-- label: sec:bb84 -->

### Protocol Overview
<!-- label: sec:bb84_overview -->

\begin{bilingual}
{Protocol Intuition / 协议直觉}
{The BB84 protocol transmits a classical bit string by encoding each bit in
the polarization state of a single photon. The security comes from the fact
that the encoding uses two incompatible bases (rectilinear $\oplus$ and
diagonal $\otimes$). Without knowing which basis was used, any measurement
by an eavesdropper inevitably introduces errors.}
\end{bilingual}

In our adaptation for SCX audit, the M_t\ parameter vector is encoded as a
bit string $m \in \{0,1\}^n$ (via quantization and binary expansion of each
component), and each bit is transmitted via a single photon.

### Hardware Setup
<!-- label: sec:bb84_hardware -->

The basic hardware components are:

1. **Single-photon source** at Alice (the auditor): emits photons
2. **Quantum channel**: optical fiber or free-space link connecting
3. **Polarization analyzer** at Bob: measures photon polarization
4. **Classical authenticated channel**: for basis reconciliation

[Figure omitted — see original .tex]

### Formal Protocol Specification
<!-- label: sec:bb84_formal -->

> **Protocol:** [BB84 for M_t\ Transmission]<!-- label: prot:bb84_mt -->
> **Input:** M_t\ parameter vector, quantized to $n$-bit string
> $m = (m_1,...,m_n) \in \{0,1\}^n$.
> 
> **Output:** Shared secret key $k \in \{0,1\}^$ ($\ell \leq n/2$ expected)
> used to encrypt $M_t$ for subsequent secure classical transmission,
> or $\bot$ (abort on detected eavesdropping).
> 
> 
> **Phase 1: Quantum Transmission**
> 
> 
1. For each bit $i = 1,...,n$:
2. Alice chooses a random basis $b_i^A \in \{0,1\}$
3. If $m_i = 0$, Alice encodes $\ket{0}$ if $b_i^A = 0$
4. If $m_i = 1$, Alice encodes $\ket{1}$ if $b_i^A = 0$
5. Alice sends the resulting photon through the quantum channel.

>   
>   \item For each received photon $i = 1,...,n$:
>   
1. Bob chooses a random measurement basis $b_i^B \in \{0,1\}$.
2. Bob measures in basis $b_i^B$ and records outcome $m_i' \in \{0,1\}$.

> 
>   
>   **Phase 2: Basis Reconciliation** (over authenticated classical channel)
> 
>   \item Alice announces all $b_i^A$, Bob announces all $b_i^B$.
>   \item Both parties discard positions where $b_i^A \neq b_i^B$.
>         The remaining positions form the **sifted key**.
>         Expected sifted key length: $n/2$.
> 
>   
>   **Phase 3: Error Estimation**
> 
>   \item Alice and Bob publicly compare a random sample of $k$ sifted key bits.
>   \item They compute the **quantum bit error rate** (QBER):
>         $Q = \frac{\# mismatches in sample}{k}$.
>   \item **Abort condition:** If $Q > Q_$ (typically
>         $Q_ \approx 11\%$), abort the protocol — eavesdropping detected.
>         The value $Q_$ is set such that the secret-key rate remains positive:
>         $1 - 2H_2(Q_) > 0$, which holds for $Q_ \lesssim 11.0\%$
>         under one-way error correction. (Note: $Q$ denotes the quantum bit
>         error rate, which is distinct from the depolarizing-channel parameter
>         $p$ used in channel-capacity analysis.)
>   \item Discard the $k$ revealed bits.
> 
>   
>   **Phase 4: Information Reconciliation and Privacy Amplification**
> 
>   \item Error correction: Alice and Bob run a classical error-correcting code
>         (e.g., Cascade or LDPC) on the remaining sifted key.
>   \item Privacy amplification: apply a 2-universal hash function (via the
>         Leftover Hash Lemma [cite]) to reduce any residual Eve
>         information to negligible $\negl(\lambda)$. The output key length
>         $\ell$ is bounded by
>         $\ell \leq H_^(K|E) - 2\log_2(1/\epsilon)$,
>         where $H_^$ is the smooth min-entropy of the raw
>         key $K$ conditioned on Eve's quantum side-information $E$.
>   \item Output the final secret key $k$, which encodes M_t.
> \end{enumerate}

### Security Analysis
<!-- label: sec:bb84_security -->

#### Intercept-Resend Attack

The simplest attack: Eve intercepts each photon, measures it, and resends a
photon prepared in the measured state.

> **Theorem:** [Intercept-Resend Error Rate]
> <!-- label: thm:intercept_resend -->
> \rigorFull
> Let Eve perform an intercept-resend attack on every photon. Then the expected
> QBER introduced is:
> \[
> \E[Q] = \frac{1}{4} = 25\% \quad (per sifted bit).
> \]
> After basis reconciliation, on positions where Alice and Bob's bases match
> but Eve's measurement basis differs (probability $1/2$), Eve's measurement
> outcome matches Alice's encoding with probability only $1/2$.

> **Proof:** Consider a sifted bit (Alice and Bob chose the same basis). Eve independently
> chooses a measurement basis:
> 
- With probability $1/2$, Eve chooses the same basis. She measures
- With probability $1/2$, Eve chooses the wrong basis. Her measurement

> Total error probability: $\frac{1}{2} \cdot 0 + \frac{1}{2} \cdot \frac{1}{2}
> = \frac{1}{4}$.

Since the protocol aborts at $Q_ \approx 11\%$, the intercept-resend
attack is **guaranteed detectable**: with sufficient sifted key bits $s$,
the probability that $Q \leq 11\%$ when the true rate is $25\%$ decays
exponentially by Hoeffding:
\[
\Pbb(Q_{observed} \leq 0.11 \mid Q_{true} = 0.25)
\leq \exp(-2s(0.14)^2) \approx e^{-0.0392s}.
\]
For $s = 1000$, this probability is $\approx 10^{-17}$.

**Caveat:** This guarantee assumes full intercept-resend on all qubits.
A more subtle adversary may attack only a fraction $\alpha$ of the qubits,
inducing an expected QBER of $0.25\alpha$. For $\alpha = 0.4$, the expected
QBER is only $10\%$, which may fall below the abort threshold
$Q_ \approx 11\%$ while still extracting partial information.
Full security requires the Shor--Preskill bound to quantify the information
leakage vs.\ QBER trade-off (Theorem [ref]).

#### General Attacks and Unconditional Security

The full security proof of BB84 against arbitrary attacks (collective,
coherent, joint) was completed by Shor and Preskill [cite]
and further refined by Renner [cite]. The key result:

> **Theorem:** [Unconditional Security of BB84]
> <!-- label: thm:unconditional -->
> For any attack strategy by Eve, the secret key rate $R$ satisfies:
> \[
> R \geq 1 - 2H_2(Q)
> \]
> where $H_2(Q) = -Q\log_2 Q - (1-Q)\log_2(1-Q)$ is the binary entropy
> function and $Q$ is the QBER. Under one-way post-processing, the secret-key
> rate is strictly positive whenever $Q \lesssim 11.0\%$, since
> $1 - 2H_2(Q) > 0$ for $Q < 11.0\%$. With two-way classical post-processing
> (this is the commonly cited $\sim$11\% threshold), higher $Q$ values can still
> yield positive key rate (up to $\sim$12.4\% for BB84 under Cascade-type
> reconciliation).
> 
> > **Remark:** [Finite-Key Considerations]
> > The security bounds above are asymptotic. In practical implementations with
> > finite block lengths, the $\epsilon$-security framework of
> > Renner [cite] must be applied, which introduces a small security
> > parameter $\epsilon$ and reduces the effective key rate by
> > $\mathcal{O}(1/\sqrt{n})$. For $n = 10^4$ photons and $\epsilon = 10^{-10}$,
> > the finite-key overhead is approximately $5\%$--$10\%$ of the asymptotic
> > key rate.
> >

\begin{bilingual}
{Security Guarantee / 安全保障}
{The BB84 protocol provides **information-theoretic security** for
M_t\ transmission: even an adversary with unlimited computational power
(including a fault-tolerant universal quantum computer) cannot extract
the M_t\ parameters without being detected with probability arbitrarily
close to 1. This is not a conjecture — it is a theorem of quantum
information theory.}
\end{bilingual}

#### Photon-Number Splitting (PNS) Attack and Decoy States

A practical vulnerability in BB84 implementations: realistic single-photon
sources sometimes emit multi-photon pulses. Eve can split off one photon
from each multi-photon pulse without disturbing the remaining photon.

> **Proposition:** [Decoy-State BB84]
> <!-- label: prop:decoy -->
> The decoy-state method [cite] defeats PNS attacks by having Alice
> randomly intersperse ``decoy'' pulses with different mean photon numbers.
> By comparing detection statistics for signal and decoy states, Bob can
> detect PNS attacks. The secure key rate with decoy states is:
> \[
> R_{decoy} \geq q\{-Q_\mu f(E_\mu)H_2(E_\mu) + \Omega[1 - H_2(e_1)]\}
> \]
> where $q$ is the basis reconciliation factor, $Q_\mu$ and $E_\mu$ are the
> gain and QBER for signal states, $\Omega$ is the fraction of single-photon
> contributions, and $e_1$ is the single-photon error rate.

### Encoding M_t\ as a Quantum Message
<!-- label: sec:bb84_encoding -->

The M_t\ parameter vector lives in $\R^d$. To transmit it via BB84:

1. **Quantization:** Each component $M_t^{(j)} \in [M_, M_]$
2. **Binary expansion:**
3. **Concatenation:**
4. **Authentication tag (optional):** Append a MAC (Message

> **Example:** [Typical Parameter Sizes]
> For a typical SCX audit with $d = 64$ parameters, each quantized to
> $b = 16$ bits:
> 
- Total bits: $64 \times 16 = 1024$ bits.
- BB84 raw photons: $n \geq 4096$ (accounting for basis mismatch,
- At 10 MHz photon source rate: raw transmission time $< 1$ ms
- Sifted key length: $\sim 2048$ bits.
- Final key after error correction and privacy amplification: $\sim 1024$ bits.

### SCX-Specific Adaptations
<!-- label: sec:bb84_scx -->

We introduce three SCX-specific enhancements to the standard BB84 protocol:

#### Hierarchical M_t\ Encoding

Not all M_t\ components are equally security-critical. We define a
**criticality hierarchy**:

\[
M_t = (M_t^{(critical)}, M_t^{(normal)}, M_t^{(low)})
\]

- **Critical:** Consensus threshold $\tau_t$, audit subset indices
- **Normal:** Expert weights, Cercis parameters — transmitted
- **Low:** Timing metadata, version numbers — transmitted

#### Spring--Yajie Dual Verification

> **Protocol:** [Dual-Verification BB84]<!-- label: prot:dual_verify -->
> After BB84 key establishment:
> 
1. Alice (Spring auditor) computes $MAC_{Spring} =
2. Alice sends $M_t \parallel MAC_{Spring}$ to Bob.
3. Bob simultaneously receives the same $M_t$ via a separate quantum
4. Bob accepts $M_t$ only if both MACs verify and
5. This prevents single-channel compromise.

#### Audit Trail with Quantum-Certified Timestamps

Each $M_t$ transmission is bound to a quantum-derived session key
$k_{session}$ generated during the BB84 exchange. The timestamp
and session key are combined via a hash-based commitment:

\[
Commit_t = SHA3-512(M_t \parallel t \parallel k_{session} \parallel S_t)
\]

where $S_t$ is the CHSH test statistic from concurrent entanglement
verification (Section [ref]). Because $k_{session}$
is information-theoretically secret (derived from BB84), the commitment
binds $M_t$ to a specific quantum session and time $t$ with
unconditional security. Subsequent verification requires knowledge of
$k_{session}$, which only the legitimate parties possess.
This provides an immutable, quantum-certified audit trail without
requiring a physical entanglement of the timestamp with $M_t$.

## Audit Entanglement: Distributed Consensus via Quantum Correlations
<!-- label: sec:entanglement -->

### The Concept of Audit Entanglement
<!-- label: sec:ent_concept -->

\begin{bilingual}
{Audit Entanglement / 审计纠缠}
{Just as two entangled particles share a single quantum state regardless of
spatial separation, two SCX auditors can share **entangled audit states**.
If Spring and Yajie share an entangled pair and independently measure their
respective halves, their outcomes are perfectly (or near-perfectly) correlated.
Any attempt by an adversary to tamper with one auditor's state instantaneously
disturbs the entanglement — a disturbance that is detectable by the other auditor.}
\end{bilingual}

> **Definition:** [Audit Entangled State]
> <!-- label: def:audit_entangled -->
> An **audit entangled state** between two auditors $\cA_{Spring}$
> and $\cA_{Yajie}$ is a bipartite quantum state
> $\rho_{SY} \in \cD(\cH_S \otimes \cH_Y)$ (where $\cD(\cdot)$ denotes density
> operators) that cannot be written as a convex combination of product states:
> \[
> \rho_{SY} \neq \sum_i p_i \, \rho_S^{(i)} \otimes \rho_Y^{(i)}.
> \]
> Equivalently, the state is *entangled* if it violates the
> Peres--Horodecki PPT criterion, or (for pure states) if the von Neumann
> entropy of either reduced state is strictly positive while the total state
> has zero entropy: $S(\rho_S) > 0$ and $S(\rho_{SY}) = 0$.
> 
> *审计纠缠态是两个审计者之间的二分量子态，不能写成乘积态的凸组合。*

### Entanglement as a Consensus Primitive
<!-- label: sec:ent_consensus -->

The key insight: **entanglement provides an additional security primitive
for audit consensus**. While classical distributed consensus (e.g.,
PBFT, Raft) requires $O(n^2)$ message exchanges, entanglement between
auditors enables them to generate *shared, certifiably random* bits
without communication. These bits, once verified via a single round of
classical authenticated communication (comparing a subset), serve as a
shared one-time pad or common randomness source, reducing the round
complexity and providing information-theoretic tamper detection.

> **Theorem:** [Entanglement Consensus Theorem]
> <!-- label: thm:ent_consensus -->
> \rigorFull
> Let two auditors share $N$ copies of the maximally entangled Bell state
> $\bell = (\ket{00} + \ket{11})/\sqrt{2}$. They independently measure each
> copy in the computational basis $\{\ket{0}, \ket{1}\}$. Then:
> 
1. **Perfect Correlation:**
2. **Shared Randomness Generation:** The auditors can generate
3. **Tamper Detection:** If an adversary applies any CPTP map

> **Proof:** **(i)** For $\bell = (\ket{00} + \ket{11})/\sqrt{2}$, the reduced
> density matrix of either party is $\rho_S = \rho_Y = \id/2$, showing maximal
> entanglement ($S(\rho_S) = 1$). Measurement in the computational basis on
> both sides yields:
> \[
> \Pbb(0_S, 0_Y) = |\braket{00|\Phi^+}|^2 = \frac{1}{2}, \qquad
> \Pbb(1_S, 1_Y) = \frac{1}{2}, \qquad
> \Pbb(0_S, 1_Y) = \Pbb(1_S, 0_Y) = 0.
> \]
> Thus the outcomes are always equal.
> 
> **(ii)** Each measurement yields one perfectly correlated bit. With $N$
> independent Bell pairs, the auditors obtain identical $N$-bit strings without
> exchanging any classical messages. The string is uniformly random (each bit
> has entropy 1) and private (any third party measuring the entangled state
> before the auditors' measurements disturbs the correlation).
> 
> **(iii)** Let $\rho' = \cE_{adv} \otimes \id(\ketbra{\Phi^+}{\Phi^+})$.
> The fidelity $F = \bra{\Phi^+}\rho'\ket{\Phi^+}$ measures how close
> $\rho'$ is to the original Bell state. If $\cE_{adv}$ is non-trivial
> ($\cE_{adv} \neq \id$), then $F < 1$ by the monotonicity of
> fidelity under CPTP maps. For $k$ independent copies tested via a CHSH
> or fidelity-estimation protocol, the probability that all $k$ copies
> appear un-tampered decays as $F^{\alpha k}$ for some protocol-dependent
> constant $\alpha > 0$. The tamper detection probability approaches
> $1$ as $k \to \infty$, with sample complexity $k = O(1/(1-F))$.

### Entanglement-Based Tamper Detection Protocol
<!-- label: sec:ent_tamper -->

> **Protocol:** [Entanglement-Based Tamper Detection]<!-- label: prot:ent_tamper -->
> **Setup:** Spring and Yajie share $N$ Bell pairs distributed by a
> trusted quantum source (or verified via entanglement swapping).
> 
> 
> **Phase 1: Random Subset Selection**
> 
> 
1. Spring and Yajie agree (over authenticated classical channel) on

> 
> 
> **Phase 2: Bell Test (CHSH)**
> 
> 
1. For each $i \in T$:
2. Spring randomly chooses measurement setting
3. Yajie randomly chooses measurement setting
4. They measure and obtain outcomes $a_i, b_i \in \{-1, +1\}$.

>   \item They compute the CHSH statistic:
>         \[
>         S = \E[A_0 B_0] + \E[A_0 B_1] + \E[A_1 B_0] - \E[A_1 B_1].
>         \]
>   \item **Acceptance Criterion:** If $|S| \leq 2 + \varepsilon_{stat}$
>         (where $\varepsilon_{stat}$ accounts for finite-statistics
>         fluctuations, scaling as $O(1/\sqrt{t})$), the hypothesis of
>         intact entanglement is rejected with high confidence — abort audit.
>         If $|S| > 2 + \varepsilon_{stat}$, the CHSH inequality is
>         violated and entanglement is verified at the chosen significance
>         level. For $t = 1000$ test pairs and $\varepsilon_{stat} = 0.2$,
>         the false-positive rate (classical state flagged as entangled) is
>         below $10^{-6}$.
> \end{enumerate}
> 
> 
> **Phase 3: Consensus Key Generation**
> 
> 
1. For each $i \in K$, both measure in computational basis.
2. The resulting bit string $k \in \{0,1\}^{k}$ serves as a shared

> **Theorem:** [CHSH Detection Threshold]
> <!-- label: thm:chsh_threshold -->
> \rigorHigh
> For a Bell state subjected to a depolarizing channel with noise parameter
> $p$ on Spring's side:
> \[
> \cE_p(\rho) = (1-p)\rho + \frac{p}{3}(\pauliX\rho\pauliX +
> \pauliY\rho\pauliY + \pauliZ\rho\pauliZ),
> \]
> the expected CHSH value is:
> \[
> S(p) = 2\sqrt{2}(1-p).
> \]
> Tampering is detectable (i.e., $S(p) \leq 2$) when $p \geq 1 - 1/\sqrt{2}
> \approx 0.2929$. That is, when the adversary disturbs more than
> $\sim 29.3\%$ of the qubits, the CHSH test detects it.

### SCX Analog: Entangled Spring--Yajie Audit States
<!-- label: sec:ent_scx -->

In the SCX framework, Spring and Yajie are complementary auditing experts:
Spring emphasizes stability and historical consistency, while Yajie prioritizes
sensitivity to recent anomalies. When they are entangled:

1. **Correlated Judgments:** Spring's audit outcome and Yajie's
2. **Tamper-Evident Correlations:** If an adversary tampers with
3. **Non-Local Audit Verification:** Even if Spring and Yajie

> **Proposition:** [Audit Entanglement Witness]
> <!-- label: prop:ent_witness -->
> An **audit entanglement witness** is a Hermitian operator $W_{SY}$ such that:
> 
- $\Tr(W_{SY} \, \rho_S \otimes \rho_Y) \geq 0$ for all separable
- $\Tr(W_{SY} \, \rho_{ent}) < 0$ for at least one entangled

> For the Bell state, a canonical witness is:
> \[
> W = \frac{1}{2}\id \otimes \id - \ketbra{\Phi^+}{\Phi^+}.
> \]
> Measuring $\Tr(W \rho)$ provides a single-number test for whether the
> Spring--Yajie audit state remains entangled.

### Practical Entanglement Distribution
<!-- label: sec:ent_distribution -->

Distributing entanglement between Spring and Yajie requires:

1. **Entanglement Source:** A source at a central location
2. **Quantum Channels:** Two optical fibers (or free-space links),
3. **Entanglement Swapping (optional):** If direct distribution
4. **Entanglement Purification:** Noisy entangled pairs are

> **Remark:** [Decoherence and Audit Deadlines]
> Entanglement is fragile. In optical fiber, the decoherence length for
> polarization-entangled photons at 1550 nm is $\sim 100$ km without repeaters.
> For audit applications where Spring and Yajie are co-located (same data center),
> this is not a constraint. For geographically distributed auditing across
> continents, quantum repeaters or satellite-based entanglement distribution
> would be required — currently at the prototype stage.

## Quantum Audit Channel: Formal Definition and Capacity
<!-- label: sec:channel -->

### Formal Definition
<!-- label: sec:channel_def -->

> **Definition:** [Quantum Audit Channel]
> <!-- label: def:qac -->
> A **quantum audit channel** is a completely positive, trace-preserving
> (CPTP) map:
> \[
> \cN_{audit}: \cD(\cH_A) \to \cD(\cH_B)
> \]
> where:
> 
- $\cH_A$ is the Hilbert space of the auditor's transmitted quantum
- $\cH_B$ is the Hilbert space of the received state at the audit
- $\cD(H)$ denotes the set of density operators on $H$.
- $\cN_{audit}$ models all physical effects on the transmitted

> 
> *量子审计信道是一个CPTP映射，将审计者发送的编码$M_t$的量子态
> 映射到审计账本接收到的量子态。*

The general form of a quantum channel is the Kraus representation:
\[
N(\rho) = \sum_{k} E_k \rho E_k^\dagger, \qquad
\sum_k E_k^\dagger E_k = \id,
\]
where $\{E_k\}$ are the Kraus operators. For the quantum audit channel,
the Kraus operators model the combined effect of physical noise and
adversarial interference.

### Channel Models for Audit Scenarios
<!-- label: sec:channel_models -->

#### Depolarizing Channel

The most symmetric noise model: the qubit is replaced by the maximally
mixed state with probability $p$:
\[
\cN_p^{depol}(\rho) = (1-p)\rho + \frac{p}{3}(\pauliX\rho\pauliX +
\pauliY\rho\pauliY + \pauliZ\rho\pauliZ).
<!-- label: eq:depol_channel -->
\]
Kraus operators:
\[
E_0 = \sqrt{1-p}\,\id, \quad
E_1 = \sqrt{p/3}\,\pauliX, \quad
E_2 = \sqrt{p/3}\,\pauliY, \quad
E_3 = \sqrt{p/3}\,\pauliZ.
\]

**Audit interpretation:** $p$ is the probability that the channel
randomizes the transmitted qubit (modeling combined noise and adversarial
interference). The depolarizing channel serves as a tractable symmetric
noise model commonly used in capacity analysis, though it does not
capture all adversarial strategies.

#### Phase Damping Channel

Models pure dephasing (relevant for fiber transmission alongside
amplitude damping; real fiber exhibits both mechanisms):
\[
\cN_^{phase}(\rho) = (1-\gamma)\rho + \gamma\pauliZ\rho\pauliZ.
\]
This preserves populations ($\bra{0}\rho\ket{0}$, $\bra{1}\rho\ket{1}$)
but damps coherences.

#### Amplitude Damping Channel

Models photon loss in fiber:
\[
\cN_^{amp}(\rho) = E_0\rho E_0^\dagger + E_1\rho E_1^\dagger,
\]
with $E_0 = \ketbra{0}{0} + \sqrt{1-\gamma}\ketbra{1}{1}$,
$E_1 = \sqrt\ketbra{0}{1}$.

**Audit interpretation:** $\gamma$ is the photon loss probability in
the fiber. At 0.2 dB/km (standard single-mode fiber at 1550 nm),
$\gamma = 1 - 10^{-\alpha L / 10}$ where $\alpha = 0.2$ dB/km and $L$ is
distance in km.

#### Adversarial Channel

We model the worst-case adversary as having full control over the channel
within a bounded region of the parameter space:
\[
\cN_{adv} \in \{N : \norm{N - \cN_0}_ \leq \varepsilon_{adv}\}
\]
where $\cN_0$ is the nominal (no-adversary) channel and
$\norm_$ is the diamond norm. The adversary can apply
any CPTP map within diamond-norm distance $\varepsilon_{adv}$ of
the nominal channel.

### Quantum Channel Capacity for Audit
<!-- label: sec:channel_capacity -->

> **Definition:** [Classical Capacity of a Quantum Channel]
> The **classical capacity** $C(N)$ of a quantum channel $N$ is the
> maximum rate (bits per channel use) at which classical information can be
> transmitted reliably (with error probability $\to 0$ as block length $\to \infty$).

> **Theorem:** [Holevo--Schumacher--Westmoreland (HSW) Theorem]
> <!-- label: thm:hsw -->
> For a quantum channel $N$, the classical capacity is:
> \[
> C(N) = \lim_{n \to \infty} \frac{1}{n} \chi(N^{\otimes n})
> \]
> where the **Holevo quantity** is:
> \[
> \chi(N) = \max_{\{p_x, \rho_x\}} \left[
> S\left(N\left(\sum_x p_x \rho_x\right)\right) -
> \sum_x p_x \, S(N(\rho_x))
> \right]
> \]
> with $S(\rho) = -\Tr(\rho \log_2 \rho)$ the von Neumann entropy.

> **Theorem:** [Audit Channel Capacity for Depolarizing Channel]
> <!-- label: thm:audit_capacity -->
> \rigorFull
> For the depolarizing channel $\cN_p^{depol}$ acting on a single qubit
> as defined in Eq.~( [ref]), the classical capacity
> (equivalently, the Holevo quantity, which is additive for this channel) is:
> \[
> C_Q(p) = 1 - H_2\!\left(\frac{2p}{3}\right)
> \]
> where $H_2(x) = -x\log_2 x - (1-x)\log_2(1-x)$.

> **Proof:** For the depolarizing channel, the optimal ensemble is the uniform distribution
> over the six states forming three mutually unbiased bases:
> $\{\ket{0},\ket{1},\ket{+},\ket{-},\ket{+i},\ket{-i}\}$, each with probability
> $1/6$. The average input state is $\id/2$. Since the depolarizing channel is
> unital, $\cN_p(\id/2) = \id/2$, so $S(\cN_p(\id/2)) = \log_2 2 = 1$.
> 
> For a pure input $\ket\bra$, the channel output is:
> \[
> \cN_p(\ketbra) = \left(1 - \frac{4p}{3}\right)\ketbra
> + \frac{2p}{3}\id.
> \]
> (This follows from the identity
> $\frac{1}{3}(\pauliX\rho\pauliX + \pauliY\rho\pauliY + \pauliZ\rho\pauliZ)
> = \frac{2}{3}\id - \frac{1}{3}\rho$ for single-qubit states.)
> 
> The eigenvalues of this output state are
> $\lambda_0 = 1 - \frac{2p}{3}$ and $\lambda_1 = \frac{2p}{3}$,
> so $S(\cN_p(\ketbra)) = H_2\!\left(\frac{2p}{3}\right)$,
> where $H_2(x) = -x\log_2 x - (1-x)\log_2(1-x)$.
> 
> By the HSW theorem and the additivity of the Holevo quantity for the
> depolarizing channel [cite], the classical capacity is:
> \[
> C(\cN_p) = \chi(\cN_p) = 1 - H_2\!\left(\frac{2p}{3}\right).
> \]

> **Corollary:** [Audit Rate Bound]
> <!-- label: cor:audit_rate -->
> The quantum-secured audit information rate $R_{audit}$ (bits per
> channel use) satisfies:
> \[
> R_{audit} \leq C_Q(p) = 1 - H_2\!\left(\frac{2p}{3}\right).
> \]
> For a noiseless channel ($p=0$): $R_{audit} \leq 1$ bit/qubit
> (the maximum possible). For a moderately noisy channel ($p=10\%$):
> $C_Q(0.10) \approx 0.648$ bits/qubit. For a severely noisy channel
> ($p=25\%$): $C_Q(0.25) \approx 0.350$ bits/qubit. The channel capacity
> vanishes ($C_Q \leq 0$) when $p \geq 3/4$, at which point the
> channel becomes completely depolarizing.
> 
> **Important:** The depolarizing parameter $p$ is distinct from the
> BB84 QBER $Q$. For a depolarizing channel, $Q \approx 2p/3$, so the
> BB84 abort threshold $Q_ \approx 11\%$ corresponds to a much
> more favorable channel condition ($p \approx 16.5\%$), at which
> $C_Q(0.165) \approx 0.488$ bits/qubit.

### Quantum Capacity (Audit Entanglement Transmission)
<!-- label: sec:quantum_capacity -->

> **Definition:** [Quantum Capacity]
> The **quantum capacity** $Q(N)$ is the maximum rate at which
> entanglement can be reliably transmitted through $N$ (measured in
> ebits per channel use). This is the relevant capacity for audit
> entanglement distribution.

> **Theorem:** [Quantum Capacity of the Depolarizing Channel]
> For the depolarizing channel $\cN_p^{depol}$:
> \[
> Q(p) \geq \max\{0,\, 1 - H_2(p) - p\log_2 3\} \quad (coherent information lower bound).
> \]
> The exact quantum capacity is not known for all $p$, but it is zero
> for $p \geq 1/2$ (when the channel becomes entanglement-breaking;
> the condition in this parameterization~$\cN_p(\rho) = (1-p)\rho + \frac{p}{3}\sum_{\sigma\in\{X,Y,Z\}}\sigma\rho\sigma$
> reduces to $\lambda < 1/3$ with $\lambda = 1 - 4p/3$, giving $p \geq 1/2$).

### Quantum Channel Model for SCX Audit Pipeline
<!-- label: sec:channel_pipeline -->

[Figure omitted — see original .tex]

> **Proposition:** [Audit Channel Reliability]
> <!-- label: prop:reliability -->
> For the SCX quantum audit channel with block length $n$, there exists an
> encoder/decoder pair achieving error probability:
> \[
> P_e^{(n)} \leq \exp(-n E_r(R))
> \]
> where $E_r(R)$ is the random coding exponent (Gallager's error exponent):
> \[
> E_r(R) = \max_{0 \leq s \leq 1} \max_{\{p_x\}} \left[
> -\ln \Tr\left(\sum_x p_x N(\rho_x)^{1/(1+s)}\right)^{1+s} - sR
> \right].
> \]
> For rates $R < C_Q(p)$, $E_r(R) > 0$ and the error probability decays
> exponentially with block length.

## Practical Feasibility and Deployment Analysis
<!-- label: sec:practical -->

### Hardware Requirements

We analyze the hardware requirements for practical quantum-secured SCX audit.

[Table omitted — see original .tex]

### Network Topology

[Figure omitted — see original .tex]

### Feasibility Matrix

[Table omitted — see original .tex]

### Hybrid Classical-Quantum Approach
<!-- label: sec:hybrid -->

Since full quantum audit infrastructure is not yet universally deployable,
we propose a **hybrid classical-quantum approach** that is feasible
today:

> **Protocol:** [Hybrid Quantum-Secured Audit]<!-- label: prot:hybrid -->
> **Phase 1: Quantum-Resistant Key Establishment (Classical)**
> 
> 
1. Auditor and ledger perform CRYSTALS-Kyber key encapsulation
2. This provides **computational** security against quantum

> 
> 
> **Phase 2: BB84 for Critical Parameters (Quantum, where available)**
> 
> 
1. For co-located audits (same data center), transmit the most
2. This provides **information-theoretic** security for the

> 
> 
> **Phase 3: Entanglement-Based Timestamping (Quantum, where available)**
> 
> 
1. Spring and Yajie share entangled pairs for tamper-evident
2. The entanglement witnesses are recorded in the audit ledger

> 
> 
> **Phase 4: Classical Digital Signatures for Bulk Data**
> 
> 
1. Bulk audit data is signed with SPHINCS+ (NIST PQC standard,
2. All signatures reference the quantum-derived session keys from

### Cost-Benefit Analysis
<!-- label: sec:cost_benefit -->

[Table omitted — see original .tex]

### Adversary Model and Attack Surface
<!-- label: sec:adversary -->

> **Definition:** [Quantum Audit Adversary Model]
> <!-- label: def:adversary_model -->
> The adversary $\cA$ has the following capabilities:
> 
- **Classical:** Unlimited classical computation, full network
- **Quantum:** Unlimited quantum computation (fault-tolerant
- **Physical:** Access to the quantum channel (fiber tapping,
- **Limitations:** Cannot violate the laws of quantum mechanics

> 
> *量子审计对手模型：对手拥有无限经典和量子计算能力，可访问量子信道，
> 但不能违反量子力学定律。*

> **Proposition:** [Attack Surface Reduction]
> <!-- label: prop:attack_surface -->
> Quantum-secured audit reduces the attack surface from:
> \[
> Classical:  \{RSA, ECDSA, AES, SHA-3, TLS, ...\} \quad
> (surface $\sim$ all of complexity theory)
> \]
> to:
> \[
> Quantum:  \{no-cloning, uncertainty principle\} \quad
> (surface $\sim$ 2 physical principles).
> \]
> This is a reduction from an infinite-dimensional space of potential
> cryptanalytic attacks to verification of two well-tested physical laws.

## Integration with the SCX Audit Framework
<!-- label: sec:integration -->

### Quantum-Secured Audit Protocol (Full Stack)
<!-- label: sec:integration_protocol -->

We present the complete quantum-secured SCX audit protocol, integrating
all three quantum primitives into the existing SCX workflow.

> **Protocol:** [Quantum-Secured SCX Audit (Q-SCX)]<!-- label: prot:qscx -->
> 
> **Input:** Data $D_t$, previous M_t\ state, auditor configuration.
> 
> **Output:** Audit result $\AuditResult_t$ with quantum security guarantees.
> 
> 
> **Step 1: Quantum Key Establishment**
> 
> 
1. Spring and Yajie each establish BB84-derived keys with the audit ledger:
2. Spring and Yajie verify shared entanglement via CHSH test
3. They derive an entanglement-based one-time pad $k_{OTP}$.

> 
> 
> **Step 2: Quantum-Secured M_t\ Transmission**
> 
> 
1. Spring computes $M_t^{Spring}$ based on historical consensus.
2. Yajie computes $M_t^{Yajie}$ based on recent anomaly detection.
3. Both transmit their $M_t$ vectors to the ledger via BB84
4. The ledger verifies consistency: if

> 
> 
> **Step 3: Classical SCX Audit with Quantum Binding**
> 
> 
1. The SCX audit proceeds classically (Yajie consensus, Cercis verification,
2. The audit result $\AuditResult_t$ is concatenated with a quantum-derived
3. The tag binds the audit result to the quantum session keys, ensuring

> 
> 
> **Step 4: Quantum-Certified Audit Trail**
> 
> 
1. The ledger records $(M_t^{Spring}, M_t^{Yajie},
2. Each entry includes the CHSH test statistic $S_t$ as proof of
3. The entanglement witnesses $\{W_t\}$ form an immutable chain of

### Security Analysis of Q-SCX
<!-- label: sec:integration_security -->

> **Theorem:** [Q-SCX Security Guarantee]
> <!-- label: thm:qscx_security -->
> \rigorFull
> Under the quantum audit adversary model (Definition [ref]),
> the Q-SCX protocol (Protocol [ref]) provides:
> 
1. **M_t\ Integrity:** Any adversary that modifies $M_t$ in transit
2. **Audit Result Authenticity:** Any adversary that forges
3. **Tamper Evidence:** Any adversary that tampers with the audit

> where $\negl(\lambda)$ is a negligible function in the security parameter
> $\lambda$ (number of qubits transmitted).

> **Proof:** [Proof Sketch]
> **(i)** $M_t$ is transmitted via BB84 (Protocol [ref]).
> By Theorem [ref], BB84 provides information-theoretic
> security: any eavesdropping attempt that extracts non-negligible
> information introduces an elevated QBER. The protocol aborts when the
> observed QBER exceeds $Q_ \approx 11\%$; for intercept-resend
> attacks the expected QBER is $25\%$ (Theorem [ref]),
> and the detection probability is $1 - e^{-\Omega(\lambda)}$ by
> Hoeffding concentration.
> 
> **(ii)** The authentication tag binds $\AuditResult_t$ to three
> independent quantum-derived keys ($k_S$, $k_Y$, $k_{OTP}$). To
> forge a valid tag, the adversary must know all three keys. Each key
> is information-theoretically secret (BB84: Theorem [ref];
> OTP: perfect secrecy by entanglement monogamy). The probability of
> guessing all three keys is $\negl(\lambda)$.
> 
> **(iii)** The audit trail includes CHSH statistics $\{S_t\}$ and
> entanglement witnesses $\{W_t\}$. By Theorem [ref],
> any tampering that disturbs entanglement by more than $\sim 29\%$
> reduces $S \leq 2$ (classical bound). With repeated measurements,
> the probability of undetected tampering decays as $2^{-\Omega(k)}$,
> where $k$ is the number of tested Bell pairs.

### Comparison with Classical Audit Security
<!-- label: sec:comparison -->

[Table omitted — see original .tex]

### Transition Roadmap
<!-- label: sec:roadmap -->

1. **Immediate (2026--2027):** Deploy hybrid classical-quantum
2. **Near-term (2027--2029):** Extend to metro-area audits
3. **Medium-term (2029--2035):** Regional deployment contingent
4. **Long-term (2035+):** Global quantum audit network

## Future Directions and Open Problems
<!-- label: sec:future -->

### Device-Independent Quantum Audit

Current QKD protocols (including BB84) require trust in the measurement
devices. **Device-independent quantum audit** would eliminate this
requirement by using Bell inequalities to certify the quantum nature of
the devices. This is the strongest possible security model:

> **Conjecture:** [Device-Independent Audit Conjecture]
> There exists a protocol where the auditor and ledger, using uncharacterized
> devices, can establish a secure audit channel if and only if the observed
> Bell violation exceeds a threshold $S > S_{threshold}$, without
> trusting any hardware component.

### Quantum Audit Networks with Multiple Auditors
<!-- label: sec:multi_auditor -->

Generalizing from 2 to $m > 2$ auditors introduces new possibilities:

- **GHZ States:** $m$-partite entanglement
- **Quantum Byzantine Agreement:** Achieving consensus among
- **Quantum Secret Sharing for Audit Keys:** Splitting the

### Continuous-Variable Quantum Audit
<!-- label: sec:cv -->

Discrete-variable QKD (single photons) has low tolerance for loss.
**Continuous-variable quantum audit** uses coherent states and
homodyne detection, offering compatibility with standard telecom
equipment at the cost of more complex error correction:

\[
R_{CV-QKD} \geq \log_2\left(\frac{V + \chi_{tot}}
{1 + \chi_{tot}}\right) - \beta I_{AB}
\]
where $V$ is the modulation variance and $\chi_{tot}$ is the
total channel noise.

### Quantum-Secured Federated Audit
<!-- label: sec:federated -->

For federated learning scenarios where models are audited across
multiple data silos:

- **Blind Quantum Audit:** The auditor verifies model
- **Quantum Homomorphic Audit:** Performing audit computations
- **Twin-Field QKD for Star Networks:** Extending audit

### Integration with Blockchain Audit Ledgers
<!-- label: sec:blockchain -->

Quantum audit trails can be integrated with blockchain-based audit
ledgers for additional immutability guarantees:

- Each block includes a quantum-certified hash of the previous
- The no-cloning theorem prevents double-spending attacks on audit
- Quantum timestamping provides provable temporal ordering of

## Conclusion
<!-- label: sec:conclusion -->

We have presented a comprehensive formalization of quantum-secured audit
for the SCX framework, addressing three fundamental aspects:

1. **BB84 for M_t\ Transmission:** We adapted the BB84 quantum
2. **Audit Entanglement:** We introduced the concept of
3. **Quantum Audit Channel:** We formally defined the quantum

The key insight is that quantum mechanics elevates audit security from
**computational** guarantees (``this is hard to break given current
algorithms'') to **physical** guarantees (``this is impossible to
break without violating the laws of physics''). This is a qualitative
leap in security assurance.

While full quantum-secured audit is not yet deployable at global scale,
a hybrid approach combining post-quantum cryptography (CRYSTALS-Kyber,
SPHINCS+) with BB84 for critical parameters is feasible today for
co-located audit scenarios. We have provided a phased deployment roadmap
extending through 2035, aligned with the expected maturation of quantum
network infrastructure.

\begin{bilingual}
{Final Remark / 结语}
{Quantum mechanics is the strongest security foundation available.
It transforms the audit security question from ``can the adversary
solve this hard problem?'' to ``can the adversary violate the
Heisenberg uncertainty principle?'' The answer to the latter is
an emphatic no — and to the extent that quantum mechanics is a
correct description of physical reality, quantum-secured audit
is provably unforgeable.}
\end{bilingual}

\rule{0.5pt}

<div align="center">

*量子力学是现有最强的安全基础。它将审计安全问题从*

*``对手能解决这个难题吗？''转变为``对手能违反海森堡不确定性原理吗？''*

*后者的答案是一个响亮的"不能"——在量子力学是物理现实的正确描述范围内，*

*量子安全审计是可证明不可伪造的。*

</div>

## Appendix
## Mathematical Background: Quantum Information Theory
<!-- label: app:math -->

### Density Operators

A quantum state is described by a **density operator** $\rho \in \cD(H)$:
\[
\cD(H) = \{\rho : H \to H \mid \rho \geq 0,\; \rho = \rho^\dagger,\;
\Tr(\rho) = 1\}.
\]
Pure states: $\rho = \ket\bra$. Mixed states: $\rho = \sum_i p_i
\ket{\psi_i}\bra{\psi_i}$.

### Von Neumann Entropy

The von Neumann entropy $S(\rho)$ is the quantum analog of Shannon entropy:
\[
S(\rho) = -\Tr(\rho \log_2 \rho) = -\sum_i \lambda_i \log_2 \lambda_i,
\]
where $\{\lambda_i\}$ are the eigenvalues of $\rho$.

### Fidelity

The fidelity between two states $\rho$ and $\sigma$:
\[
F(\rho, \sigma) = \left(\Tr \sqrt{\sqrt \sigma \sqrt}\right)^2.
\]
For pure states: $F(\ket,\ket) = |\braket{\psi|\phi}|^2$.

### CHSH Inequality (Bell's Theorem)

For measurements $A_0, A_1$ (Alice) and $B_0, B_1$ (Bob) with outcomes
$\pm 1$, the CHSH value:
\[
S = \E[A_0 B_0] + \E[A_0 B_1] + \E[A_1 B_0] - \E[A_1 B_1].
\]
Local-hidden-variable theories satisfy $|S| \leq 2$ (CHSH inequality).
Quantum mechanics allows $|S| \leq 2\sqrt{2}$ (Tsirelson bound).
Entanglement is certified when $2 < |S| \leq 2\sqrt{2}$.

### Holevo Bound

The Holevo quantity bounds the accessible classical information in
a quantum ensemble $\{p_x, \rho_x\}$:
\[
\chi = S\left(\sum_x p_x \rho_x\right) - \sum_x p_x S(\rho_x).
\]
This is the classical capacity of a noiseless quantum channel.

## Proof of the Audit Channel Capacity Lower Bound
<!-- label: app:proof -->

> **Proof:** [Full Proof of Theorem [ref]]
> For the depolarizing channel $\cN_p$ with parameter $p \in [0, 1]$:
> \[
> \cN_p(\rho) = (1-p)\rho + \frac{p}{3}(\pauliX\rho\pauliX
> + \pauliY\rho\pauliY + \pauliZ\rho\pauliZ).
> \]
> 
> **Step 1: Channel symmetry.** The depolarizing channel is
> covariant under the Pauli group:
> \[
> \cN_p(U\rho U^\dagger) = U \cN_p(\rho) U^\dagger
> \]
> for any single-qubit unitary $U$. This implies that the optimal input
> ensemble is the uniform distribution over a complete set of mutually
> unbiased bases (e.g., the six states $\{\ket{0},\ket{1},\ket{+},\ket{-},
> \ket{+i},\ket{-i}\}$).
> 
> **Step 2: Output entropy.** For the maximally mixed input
> $\rho_{avg} = \id/2$:
> \[
> \cN_p(\id/2) = (1-p)\frac{2} + \frac{p}{3} \cdot 3 \cdot \frac{2}
> = \frac{2}.
> \]
> Thus $S(\cN_p(\id/2)) = S(\id/2) = \log_2 2 = 1$.
> 
> **Step 3: Conditional output entropy.** For a pure state input
> $\rho = \ket\bra$, choose $\ket = \ket{0}$ without
> loss of generality (by covariance):
> \[
> \cN_p(\ketbra{0}{0}) = (1-p)\ketbra{0}{0} +
> \frac{p}{3}(\ketbra{1}{1} + \ketbra{1}{1} + \ketbra{0}{0})
> = \left(1 - \frac{2p}{3}\right)\ketbra{0}{0} +
> \frac{2p}{3}\ketbra{1}{1}.
> \]
> This is a classical mixture with eigenvalues
> $\lambda_0 = 1 - 2p/3$ and $\lambda_1 = 2p/3$.
> The von Neumann entropy of this output state is therefore:
> \[
> S(\cN_p(\ketbra)) = H_2\!\left(\frac{2p}{3}\right)
> = -\frac{2p}{3}\log_2\frac{2p}{3} - \left(1-\frac{2p}{3}\right)\log_2\left(1-\frac{2p}{3}\right).
> \]
> 
> **Step 4: Holevo quantity.** The Holevo quantity for our $p$-parametrization is:
> \[
> \chi(\cN_p) = S(\cN_p(\id/2)) - S(\cN_p(\ketbra))
> = 1 - H_2\!\left(\frac{2p}{3}\right).
> \]
> 
> **Step 5: Additivity.** For the depolarizing channel, the
> Holevo quantity is additive:
> $\chi(\cN_p^{\otimes n}) = n\chi(\cN_p)$ [cite]. Hence:
> \[
> C(\cN_p) = \chi(\cN_p) = 1 - H_2\!\left(\frac{2p}{3}\right).
> \]
> 
> **Numerical check** (using our $p$-parametrization):
> 
- $p = 0$: $C_Q = 1 - H_2(0) = 1.000$ (noiseless, 1 bit/qubit).
- $p = 0.11$: $C_Q = 1 - H_2(0.0733) \approx 0.622$ bits/qubit.
- $p = 0.25$: $C_Q = 1 - H_2(0.1667) \approx 0.350$ bits/qubit.
- $p = 0.75$: $C_Q = 1 - H_2(0.5) = 0.000$ (capacity zero).

## Implementation Notes for Q-SCX Prototype
<!-- label: app:implementation -->

### Software Stack

\begin{verbatim}
Quantum-Secured SCX Audit — Software Stack
===========================================

Layer 1: Quantum Hardware Abstraction
  - Qiskit / Cirq / PennyLane for quantum circuit simulation
  - QKD vendor SDKs (ID Quantique, QuintessenceLabs, Toshiba)
  - Quantum random number generator API

Layer 2: Quantum Protocol Engine
  - BB84 state machine (prepare, transmit, measure, sift)
  - Cascade error correction (BB84 reconciliation)
  - Toeplitz hashing (privacy amplification)
  - CHSH test executor (entanglement verification)

Layer 3: SCX Audit Integration
  - Mt quantization and encoding
  - Quantum-derived key management
  - Authentication tag generation and verification
  - Audit trail entanglement witness recorder

Layer 4: Classical Fallback
  - CRYSTALS-Kyber (liboqs / OpenQuantumSafe)
  - SPHINCS+ signatures
  - Classical audit pipeline (unchanged SCX core)
\end{verbatim}

### Key Parameters

[Table omitted — see original .tex]

\begin{thebibliography}{99}

\bibitem{bb84}
C.~H.~Bennett and G.~Brassard.
\newblock Quantum cryptography: Public key distribution and coin tossing.
\newblock *Proc. IEEE Int. Conf. on Computers, Systems, and Signal
Processing*, 1984.

\bibitem{shor1994}
P.~W.~Shor.
\newblock Algorithms for quantum computation: discrete logarithms and factoring.
\newblock *Proc. 35th FOCS*, 1994.

\bibitem{wootters1982}
W.~K.~Wootters and W.~H.~Zurek.
\newblock A single quantum cannot be cloned.
\newblock *Nature*, 299:802--803, 1982.

\bibitem{ekert1991}
A.~K.~Ekert.
\newblock Quantum cryptography based on Bell's theorem.
\newblock *Phys. Rev. Lett.*, 67:661--663, 1991.

\bibitem{holevo1998}
A.~S.~Holevo.
\newblock The capacity of the quantum channel with general signal states.
\newblock *IEEE Trans. Inf. Theory*, 44(1):269--273, 1998.

\bibitem{schumacher1996}
B.~Schumacher and M.~D.~Westmoreland.
\newblock Sending classical information via noisy quantum channels.
\newblock *Phys. Rev. A*, 56:131--138, 1997.

\bibitem{shor_preskill2000}
P.~W.~Shor and J.~Preskill.
\newblock Simple proof of security of the BB84 quantum key distribution protocol.
\newblock *Phys. Rev. Lett.*, 85:441--444, 2000.

\bibitem{renner2005}
R.~Renner.
\newblock Security of quantum key distribution.
\newblock *PhD Thesis*, ETH Zurich, 2005.

\bibitem{decoy_state}
W.-Y.~Hwang.
\newblock Quantum key distribution with high loss: Toward global secure
communication.
\newblock *Phys. Rev. Lett.*, 91:057901, 2003.

\bibitem{king2003}
C.~King.
\newblock The capacity of the quantum depolarizing channel.
\newblock *IEEE Trans. Inf. Theory*, 49(1):221--229, 2003.

\bibitem{quantum_internet}
S.~Wehner, D.~Elkouss, and R.~Hanson.
\newblock Quantum internet: A vision for the road ahead.
\newblock *Science*, 362(6412), 2018.

\bibitem{nist_pqc}
NIST.
\newblock Post-Quantum Cryptography Standardization.
\newblock https://csrc.nist.gov/projects/post-quantum-cryptography, 2024.

\bibitem{scx_audit}
SCX Research Group.
\newblock SCX: Situs Consensus eXpert — A Framework for Rigorous AI Auditing.
\newblock Technical Report, Xiaogan Supercomputing Center, 2025.

\bibitem{audit_instanton}
SCX Research Group.
\newblock Audit Instantons: Non-Perturbative Topological Defects in Expert
Auditing.
\newblock Technical Report, Xiaogan Supercomputing Center, 2026.

\bibitem{quantum_measurement}
SCX Research Group.
\newblock Quantum Measurement as Multi-Observer Consensus.
\newblock Technical Report, Xiaogan Supercomputing Center, 2026.

\bibitem{gisin2002}
N.~Gisin, G.~Ribordy, W.~Tittel, and H.~Zbinden.
\newblock Quantum cryptography.
\newblock *Rev. Mod. Phys.*, 74:145--195, 2002.

\bibitem{scarani2009}
V.~Scarani, H.~Bechmann-Pasquinucci, N.~J.~Cerf, et al.
\newblock The security of practical quantum key distribution.
\newblock *Rev. Mod. Phys.*, 81:1301--1350, 2009.

\bibitem{lo2014}
H.-K.~Lo, M.~Curty, and K.~Tamaki.
\newblock Secure quantum key distribution.
\newblock *Nature Photonics*, 8:595--604, 2014.

\bibitem{pirandola2020}
S.~Pirandola, U.~L.~Andersen, L.~Banchi, et al.
\newblock Advances in quantum cryptography.
\newblock *Adv. Opt. Photon.*, 12:1012--1236, 2020.

\bibitem{xu2020}
F.~Xu, X.~Ma, Q.~Zhang, H.-K.~Lo, and J.-W.~Pan.
\newblock Secure quantum key distribution with realistic devices.
\newblock *Rev. Mod. Phys.*, 92:025002, 2020.

\end{thebibliography}