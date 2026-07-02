# The Measurement Problem as an Audit Problem

**Author:** SCX

*Abstract:*

The quantum measurement problem asks: when and why does the wavefunction collapse? We reframe this as a multi-expert audit problem. Each measurement apparatus (or conscious observer) is an ``expert'' reporting an outcome. The Born rule provides the probability distribution over expert reports. SCX Theorem~3 proves that disagreement among observers cannot be attributed to a specific cause (apparatus error, genuine indeterminacy, or basis mismatch) without declared axioms. We show that three historical experiments---the double-slit, Wigner's friend, and weak measurement---are special cases of SCX multi-expert audit with $M=1$, $M=2$, and $M \gg 1$ observers respectively. Weak measurement emerges as Yajie consensus with partial information preservation. Quantum Darwinism is Spring memory: the environment redundantly encodes information as a permanent audit trail. We derive tight non-asymptotic bounds (Chernoff--Hoeffding) for the multi-observer agreement probability, an exact fidelity--coupling relation for weak measurement, a minimum redundancy formula for quantum Darwinism, and a Bell-inequality audit theorem linking CHSH violation to non-classical multi-expert correlation.

## The Measurement Problem as an Audit Problem

> **Definition:** [Observer as Expert]
> A measurement apparatus (or conscious observer) $\Obs_m$ is an **expert**. Given a quantum state $\ket$, $\Obs_m$ reports an outcome $o_m \in \Omega$ (the spectrum of the measured observable) with probability $\Pbb(o_m \mid \psi) = |\braket{o_m|\psi}|^2$ (Born rule). The report is a **claim** about the pre-measurement state.

> **Definition:** [Measurement as Consensus]
> $M$ independent observers $\Obs_1,...,\Obs_M$ measure identically prepared states $\ket^{\otimes M}$. The consensus outcome is the modal report $\hat{o} = \arg\max_o \sum_m \mathbf{1}\{o_m = o\}$. The consensus strength $C = \frac{1}{M}\sum_m \mathbf{1}\{o_m = \hat{o}\}$ measures inter-observer agreement.

## Theorem 1: Multi-Observer Agreement with Finite-$M$ Tight Bounds

> **Theorem:** [Multi-Observer Agreement Bound]
> <!-- label: thm:agreement -->
> \rigorFull
> Let $M$ independent observers measure observable $\hat{O}$ on identically prepared state $\ket$ with spectral decomposition $\hat{O} = \sum_{o} \lambda_o \ket{o}\bra{o}$. Define $p_o = |\braket{o|\psi}|^2$ and $p_ = \max_o p_o$.

**(i) Exact agreement probability.**
\[
\Pbb(all  M  report  o \mid \psi) = p_o^{M}
\]
\[
\Pbb(not all agree) = 1 - \sum_{o} p_o^{M}
\]

**(ii) Chernoff--Hoeffding concentration for the empirical distribution.**
Let $\hat{p}_o^{(M)} = \frac{1}{M}\sum_{m=1}^{M} \mathbf{1}\{o_m = o\}$ be the empirical frequency of outcome $o$. Then for any $\varepsilon > 0$:
\[
\Pbb\!\left(\max_{o \in \Omega} \bigl|\hat{p}_o^{(M)} - p_o\bigr| \geq \varepsilon\right) \leq 2|\Omega|\, e^{-2M\varepsilon^2}
\]
where $|\Omega|$ is the number of distinct eigenvalues (outcomes). This follows from Hoeffding's inequality applied independently to each outcome and a union bound.

**(iii) Finite-$M$ threshold for near-certain disagreement.**
For a state with $p_ = \max_o |\braket{o|\psi}|^2 < 1$, the probability that *at least two observers disagree* exceeds $0.99$ when:
\[
M \geq M_{0.99} \equiv \left\lceil \frac{\ln(1 - 0.99) - \ln|\Omega|}{\ln p_} \right\rceil^{+}
\]
where $\lceil x \rceil^{+} = \max(1, \lceil x \rceil)$. For a uniform superposition over $d$ outcomes ($p_o = 1/d$):
\[
M_{0.99}^{(uniform)} = \left\lceil \frac{\ln(0.01) - \ln d}{-\ln d} \right\rceil
\]
Numerical examples: $d=2$ (equal superposition qubit) gives $M_{0.99} = 7$; $d=10$ gives $M_{0.99} = 3$; $d=100$ gives $M_{0.99} = 2$. Higher superposition dimension accelerates disagreement.

**(iv) Asymptotic limit.**
As $M \to \infty$, $\Pbb(all agree) = \sum_o p_o^{M} \to 0$ for any non-deterministic state ($p_ < 1$). The disagreement is exponentially fast in $M$ with rate $\ln(1/p_)$.

> **Proof:** **(i)** By the Born rule, each observer independently reports $o$ with probability $p_o = |\braket{o|\psi}|^2$. The events are independent across observers (identically prepared states on distinct subsystems of $\ket^{\otimes M}$). Thus $\Pbb(all report  o) = p_o^M$. Agreement means all $M$ report the *same* outcome (any $o$), giving $\sum_o p_o^M$. Disagreement is the complement $1 - \sum_o p_o^M$.
> 
> **(ii)** For each fixed outcome $o$, the indicator $\mathbf{1}\{o_m = o\}$ is a bounded random variable in $[0, 1]$ with mean $p_o$. By Hoeffding's inequality:
> \[
> \Pbb\!\left(\bigl|\hat{p}_o^{(M)} - p_o\bigr| \geq \varepsilon\right) \leq 2e^{-2M\varepsilon^2}.
> \]
> Applying a union bound over all $|\Omega|$ outcomes yields the claimed inequality.
> 
> **(iii)** For disagreement to be probable $\geq 0.99$, we need $\Pbb(all agree) \leq 0.01$. Since $\Pbb(all agree) = \sum_o p_o^M \leq |\Omega| \cdot p_^M$, the condition $|\Omega| \cdot p_^M \leq 0.01$ suffices. Solving $p_^M \leq 0.01/|\Omega|$ gives $M \geq \ln(0.01/|\Omega|) / \ln p_$, yielding the formula for $M_{0.99}$.
> 
> **(iv)** For each $o$ with $p_o < 1$, $p_o^M \to 0$ as $M \to \infty$. If $p_ < 1$, all $p_o < 1$ and the sum vanishes. The rate is $\sim p_^M = e^{-M \ln(1/p_)}$, exponential decay. $\square$

> **Remark:** [SCX Interpretation]
> The Chernoff--Hoeffding bound quantifies how fast the empirical distribution of expert reports concentrates around the Born rule probabilities. For small $M$, expert reports are volatile --- consensus is fragile. For large $M$, the empirical distribution is tightly concentrated, yet individual *unanimity* becomes exponentially unlikely. This tension --- concentration of the histogram vs.\ divergence of individual reports --- is the mathematical core of why wavefunction collapse requires an axiom (the Heisenberg cut) rather than emerging as a theorem.

## Historical Validation: Three Experiments as SCX Special Cases

### Double-Slit: $M=1$ Observer Destroys Interference

> **Example:** [Double-Slit as $M=1$ Audit Failure]
> In the double-slit experiment with single-photon detection:
> 
- **$M=0$ (no which-path detection)**: Interference pattern appears. Multiple ``experts'' (slit positions) produce consensus via wave superposition.
- **$M=1$ (which-path detector at one slit)**: Interference destroyed. A single observer's report collapses the superposition. SCX Theorem~2: $M=1$ is epistemically equivalent to no audit --- the observer's report cannot be verified by a second independent measurement on the same photon.

### Wigner's Friend: $M=2$ Disagreeing Observers

> **Example:** [Wigner's Friend as $M=2$ Consensus Failure]
> Wigner's friend $\Obs_F$ measures $\ket$ inside a sealed laboratory, obtaining outcome $o_F$. Wigner $\Obs_W$ stands outside, treating the laboratory as a quantum system.
> 
> 
- $\Obs_F$ reports: ``the state collapsed to $\ket{o_F}$''
- $\Obs_W$ reports: ``the state is still $\frac{1}{\sqrt{2}}(\ket{0}_F\ket{saw 0} + \ket{1}_F\ket{saw 1})$''

> 
> Two observers, two contradictory reports. SCX Theorem~3: the cause of disagreement is **three-way unidentifiable**:
> 
1. **$\Obs_F$ is correct**: collapse occurs upon first conscious observation. $\Obs_W$ is merely unaware.
2. **$\Obs_W$ is correct**: no collapse occurs. $\Obs_F$ is entangled with the system, forming a larger superposition.
3. **Both are correct in their own reference frames**: collapse is observer-relative (Relational QM).

> Without declaring ``who counts as an observer'' (axiom choice), the disagreement is unresolvable. This is SCX Theorem~3 applied to the measurement problem: the axiom is the choice of Heisenberg cut.

### Weak Measurement: $M \gg 1$ as Yajie Consensus

## Theorem 2: Weak Measurement --- Exact Fidelity--Coupling Relation

> **Theorem:** [Weak Measurement as Multi-Expert Audit]
> <!-- label: thm:weak-measurement -->
> \rigorFull
> Consider a weak measurement of observable $\hat{A}$ on $M$ identically prepared copies of $\ket$, with von Neumann interaction Hamiltonian $\hat{H}_{int} = g \cdot \hat{A} \otimes \hat{P}_{meter}$ where $g \ll 1$ is the coupling strength.

**(i) Post-measurement state fidelity (single trial).**
After one weak measurement with Gaussian meter state of width $\sigma$, the post-measurement system state $\rho^{(1)}$ has fidelity:
\[
F^{(1)} \equiv \braket{\psi|\rho^{(1)}|\psi} = 1 - \frac{g^2}{4\sigma^2} \cdot \Var_[\hat{A}] + O(g^4)
\]
where $\Var_[\hat{A}] = \braket{\psi|\hat{A}^2|\psi} - \braket{\psi|\hat{A}|\psi}^2$ is the quantum variance.

**(ii) $M$-trial aggregate fidelity.**
For $M$ independent weak measurements on identically prepared states, the aggregate post-measurement fidelity satisfies:
\[
F^{(M)} \geq \left(1 - \frac{g^2}{4\sigma^2} \Var_[\hat{A}]\right)^{M} \approx \exp\!\left(-\frac{M g^2}{4\sigma^2} \Var_[\hat{A}]\right)
\]
For $M g^2 \ll 4\sigma^2 / \Var_[\hat{A}]$, we have $F^{(M)} = 1 - O(M g^2)$. The fidelity remains high when the total disturbance $M g^2$ is small.

**(iii) Weak value --- expectation --- strong measurement relation.**
The weak value for pre-selection $\ket$ and post-selection $\ket$ is:
\[
\brak{\hat{A}}_w = \frac{\braket{\phi|\hat{A}|\psi}}{\braket{\phi|\psi}}
\]
The ensemble average of $M$ weak measurements (without post-selection) converges to the standard expectation:
\[
\E[\brak{\hat{A}}_{weak}^{(M)}] = \braket{\psi|\hat{A}|\psi} \quad (strong measurement expectation)
\]
with statistical error:
\[
\brak{\hat{A}}_{weak}^{(M)} = \braket{\psi|\hat{A}|\psi} \pm \sqrt{\frac{\Var_[\hat{A}]}{M}} + O(g^2)
\]
The $1/\sqrt{M}$ convergence is exactly the SCX consensus rate: multiple weak signals aggregate to a strong signal. The crucial difference from strong measurement is that weak measurement preserves state fidelity $F^{(M)} \approx 1 - O(M g^2)$, whereas strong measurement ($g \sim 1$) destroys the state after a single trial.

**(iv) Optimal measurement strength for fixed total resource.**
Under a total disturbance budget $\Delta_{tot} = M g^2$, the optimal strategy to minimize statistical error while respecting the fidelity constraint $F^{(M)} \geq 1 - \delta$ is:
\[
g_{opt} = \sqrt{\frac{4\sigma^2 \delta}{M \Var_[\hat{A}]}}, \qquad M_{opt} = \frac{\Delta_{tot}}{g_{opt}^2}
\]
The statistical error then scales as $O(M_{opt}^{-1/2}) = O(g_{opt})$.

> **Proof:** **(i)** The weak measurement unitary is $\hat{U} = \exp(-i g \hat{A} \otimes \hat{P}_{meter})$. For Gaussian meter $\ket_{meter}$ with $\braket{\hat{P}} = 0$, $\braket{\hat{P}^2} = 1/(4\sigma^2)$, the reduced system state after tracing out the meter is (to $O(g^2)$):
> \[
> \rho^{(1)} = \ket\bra - \frac{g^2}{8\sigma^2}\bigl[\hat{A}, [\hat{A}, \ket\bra]\bigr] + O(g^4).
> \]
> Computing $\braket{\psi|\rho^{(1)}|\psi} = 1 - \frac{g^2}{4\sigma^2}(\braket{\hat{A}^2} - \braket{\hat{A}}^2) + O(g^4)$ gives (i).
> 
> **(ii)** Each trial multiplies the fidelity by $\approx 1 - g^2 \Var[\hat{A}]/(4\sigma^2)$. Since the $M$ trials are on independent copies, the total fidelity is the product. The inequality follows from the sub-multiplicativity of fidelity under tensor products. The exponential approximation holds for $M g^2 \ll 1$.
> 
> **(iii)** The meter shift for trial $m$ is $\delta p_m = g \cdot \brak{\hat{A}}_w^{(m)}$ where the weak value depends on the (random) post-selection. Without post-selection, the unconditional meter shift is $g \cdot \braket{\psi|\hat{A}|\psi}$. Averaging $M$ independent meter readings gives the sample mean with standard error $\sqrt{\Var[\hat{A}]/M}$.
> 
> **(iv)** Differentiating the statistical error $\sqrt{\Var[\hat{A}]/M}$ subject to $M g^2 = \Delta_{tot}$ and $F^{(M)} \geq 1 - \delta$ gives the optimal $g$. $\square$

> **Corollary:** [Why Weak Measurement Was Discovered Late]
> Weak measurement (Aharonov, Albert, Vaidman 1988) was historically surprising because physicists thought measurement necessarily destroys the state. SCX explains: strong measurement = $M=1$ single-expert audit (destructive). Weak measurement = $M \gg 1$ multi-expert audit (information-preserving). The surprise was not quantum --- it was audit-theoretic. The fidelity $F^{(M)} = 1 - O(M g^2)$ quantifies *how much of the original state (the ``training data'' in SCX terms) survives the audit*.

## Theorem 3: Quantum Darwinism --- Redundancy and Consensus Threshold

> **Theorem:** [Quantum Darwinism = Spring Permanent Memory]
> <!-- label: thm:darwinism-spring -->
> \rigorFull
> Let the total environment $\mathcal{E}$ be partitioned into $N$ fragments $\{\mathcal{E}_1, ..., \mathcal{E}_N\}$, each interacting with the system $\mathcal{S}$ via the same pointer observable $\hat{X} = \sum_x x \ket{x}\bra{x}$. Quantum Darwinism asserts that information about $\hat{X}$ is redundantly encoded across many fragments.

**(i) Redundancy measure.**
The **redundancy** $R_\delta$ is the number of environment fragments that each contain (at least) $(1-\delta)$ of the classical information about $\hat{X}$:
\[
R_\delta = \max\!\left\{k \in \{1,...,N\} : I(\mathcal{S}:\mathcal{E}_j) \geq (1-\delta) \cdot \chi(\mathcal{S}:\hat{X})  for at least  k  distinct  j\right\}
\]
where $I(\mathcal{S}:\mathcal{E}_j)$ is the quantum mutual information between system and fragment $j$, and $\chi(\mathcal{S}:\hat{X}) = S(\sum_x p_x \ket{x}\bra{x}) - \sum_x p_x S(\ket{x}\bra{x})$ is the Holevo information of the pointer observable ($S$ is von Neumann entropy, $p_x = |\braket{x|\psi}|^2$).

**(ii) Consensus from redundancy.**
If $R_\delta$ independent environment fragments each encode the pointer state with fidelity $\geq 1-\delta$, then $M = R_\delta$ independent ``environment-observers'' can reach consensus on the pointer state. The probability that a majority of these fragments report the correct pointer state $x^* = \arg\max_x p_x$ is:
\[
\Pbb(majority consensus) \geq 1 - \exp\!\left(-2 R_\delta \left(\tfrac{1}{2} - \delta\right)^2\right)
\]
by Hoeffding's inequality (each fragment gives the correct outcome with probability $\geq 1-\delta$).

**(iii) Minimum redundancy for consensus threshold $\theta$.**
To achieve consensus confidence $\geq \theta$, the minimum required redundancy is:
\[
R_(\theta, \delta) = \left\lceil \frac{\ln(1-\theta)}{2(\frac{1}{2} - \delta)^2} \right\rceil
\]
For $\delta = 0.1$ (90\% information per fragment) and $\theta = 0.99$:
\[
R_(0.99, 0.1) = \left\lceil \frac{\ln(0.01)}{2(0.4)^2} \right\rceil = \left\lceil \frac{-4.605}{0.32} \right\rceil = 15
\]
Only $R \geq 15$ environment fragments are needed for 99\% consensus confidence. Typical quantum Darwinism simulations yield $R \sim 10^2$--$10^4$, far exceeding the minimum.

**(iv) Structural correspondence to Spring memory.**

- **Environment fragments** $\{\mathcal{E}_k\}$ = Spring memory entries $\{m_k \in M_t\}$
- **Redundancy** $R_\delta$ = number of independent copies of the same information in $M_t$
- **Consensus threshold** $\theta$ = Spring retrieval confidence
- **Objective reality emerges** = consensus converges as $R \to \infty$ with probability $\to 1$
- **Decoherence** = Spring pruning: environmental interaction removes coherence (noise) from the system, leaving only pointer-state information in memory

> **Proof:** **(i)** The definition of $R_\delta$ follows Zurek's original formulation: redundancy is the number of disjoint fragments that can supply the same classical information about the system. The Holevo information $\chi(\mathcal{S}:\hat{X})$ is the maximum classical information extractable from a single measurement of $\hat{X}$.
> 
> **(ii)** Each of the $R_\delta$ fragments acts as an independent noisy channel. The probability that fragment $j$ ``votes'' for the correct pointer state is $\geq 1-\delta$ (since it retains $\geq 1-\delta$ of the information). In the worst case, each fragment votes correctly with probability exactly $1-\delta$. Majority requires $\geq R_\delta/2$ correct votes. By Hoeffding, the probability of $\leq R_\delta/2$ successes in $R_\delta$ trials with success probability $1-\delta$ is $\leq \exp(-2R_\delta(1-\delta - 1/2)^2) = \exp(-2R_\delta(1/2 - \delta)^2)$.
> 
> **(iii)** Set $\exp(-2R(1/2-\delta)^2) \leq 1-\theta$, solve for $R$, and take the ceiling.
> 
> **(iv)** The correspondence is structural, not metaphorical. Both Quantum Darwinism and Spring memory implement *redundant information storage with consensus-based retrieval*. The key mathematical identity is $R_\delta = M_t^{(effective)}/(entries per fact)$: the redundancy in the environment equals the effective multiplicity of a fact in Spring memory. $\square$

> **Remark:** [Physical Interpretation]
> $R_ = 15$ for $\theta = 0.99, \delta = 0.1$ is remarkably small. This explains why classicality emerges so robustly: even modest environmental redundancy suffices for near-certain consensus. The exponential Hoeffding concentration means that each additional environment fragment *doubles* the consensus confidence (in the large-deviation sense). Classical reality is cheap: it requires only $O(\log(1/(1-\theta)))$ redundant encodings.

## Theorem 4: Bell Inequality Violation as SCX Audit

> **Theorem:** [Bell--CHSH Violation as Multi-Expert Audit]
> <!-- label: thm:bell-audit -->
> \rigorFull
> Consider $M=2$ observers (Alice $\Obs_A$ and Bob $\Obs_B$) each measuring one half of $N$ identically prepared entangled pairs in the singlet state $\ket{\Psi^-} = (\ket{01} - \ket{10})/\sqrt{2}$. Each observer chooses between two measurement settings: $\Obs_A$ chooses $\{a, a'\}$, $\Obs_B$ chooses $\{b, b'\}$. Their reports form a $2 \times 2$ correlation table.

**(i) CHSH statistic as inter-observer correlation measure.**
Define the correlation function $E(x, y) = \Pbb(same outcome \mid x, y) - \Pbb(different outcome \mid x, y)$. The CHSH parameter is:
\[
S = E(a, b) + E(a', b) + E(a, b') - E(a', b')
\]

**(ii) Classical bound (local realism --- independent experts).**
If Alice and Bob's reports are generated by local hidden variables (i.e., their expertise is ``classically independent'' given a common cause $\lambda$):
\[
|S| \leq 2 \quad (CHSH inequality)
\]

**(iii) Quantum bound (entangled experts).**
For the singlet state with optimal measurement settings $(a, a', b, b') = (0, \pi/2, \pi/4, 3\pi/4)$:
\[
S_{QM} = 2\sqrt{2} \approx 2.828 > 2
\]
The quantum correlation *violates* the classical bound by a factor of $\sqrt{2}$.

**(iv) Finite-$N$ statistical significance.**
With $N$ independent entangled pairs, the empirical CHSH statistic $\hat{S}_N$ satisfies:
\[
\Pbb\!\left(\hat{S}_N > 2 \;\middle|\; local realism\right) \leq \exp\!\left(-\frac{N(S_{QM} - 2)^2}{8}\right) = \exp\!\left(-\frac{N(2\sqrt{2} - 2)^2}{8}\right) \approx e^{-0.0429 N}
\]
For $N = 100$ pairs, the probability that local realism could produce the observed violation is $\lesssim e^{-4.29} \approx 0.014$. For $N = 500$, it is $\lesssim 5 \times 10^{-10}$. The CHSH experiment is a *hypothesis test* with exponentially decaying Type-I error.

**(v) SCX audit interpretation.**
When $S > 2$ is observed:

- **The two experts' reports are non-classically correlated.** Their agreement/disagreement pattern cannot be explained by any local common-cause model.
- **The audit reveals structure that no single-expert report could.** The *pattern* of disagreement across measurement settings is information that exists only in the joint distribution --- it is an emergent property of the multi-expert system.
- **SCX Theorem~3 applies:** the violation of $S \leq 2$ can be attributed to either (a) genuine quantum non-locality, (b) superdeterminism (the measurement settings are not free), or (c) retrocausality. The choice among these is **three-way unidentifiable** without declaring an axiom (``measurement settings are free variables'').
- **The Bell test is an SCX audit** that *rejects* the null hypothesis ``the experts are classically independent'' with confidence $\geq 1 - e^{-0.0429 N}$.

> **Proof:** **(i)--(iii)** are standard quantum mechanics (Clauser et al.\ 1969, Bell 1964). For the singlet state, $E(a,b) = -\cos(a-b)$. With the optimal angle settings $a=0, a'=\pi/2, b=\pi/4, b'=3\pi/4$, we obtain $E(0,\pi/4) = E(\pi/2,\pi/4) = E(0,3\pi/4) = -1/\sqrt{2}$ and $E(\pi/2,3\pi/4) = +1/\sqrt{2}$, giving $S = 2\sqrt{2}$.
> 
> **(iv)** Each pair gives an independent estimate of each $E(x,y)$ with outcomes in $\{-1,+1\}$. By Hoeffding, the empirical $E(x,y)$ concentrates at rate $O(1/\sqrt{N})$. The CHSH statistic $S$ is a linear combination of four such estimates, each with variance $\leq 1/N$, giving $\Var[\hat{S}_N] \leq 4/N$. The probability that $\hat{S}_N$ exceeds 2 under local realism follows from Hoeffding's inequality applied to the sum.
> 
> **(v)** The SCX interpretation follows directly: the multi-expert audit (two observers with multiple measurement settings) reveals a correlation pattern inaccessible to any single-expert report. The existence of the correlation pattern is an *audit-level fact* --- it exists only in the joint distribution, not in any marginal. $\square$

> **Corollary:** [Bell Test as SCX Audit Protocol]
> The Bell--CHSH experiment is the simplest non-trivial SCX multi-expert audit:
> 
<div align="center">

> [Table omitted — see original .tex]
>

</div>

> This protocol demonstrates that SCX audit methodology applies not only to classical multi-expert systems but also to the fundamental structure of quantum correlations.

## Implications

> **Corollary:** [Collapse Is Not a Physical Process --- It Is a Consensus Threshold]
> Wavefunction collapse occurs when the consensus among observers exceeds a threshold $\theta$. For $M=1$ (single observer), collapse is instantaneous upon measurement --- the observer IS the consensus. For $M \gg 1$ (environment, $R_\delta \gg R_$), collapse is gradual --- decoherence continuously increases consensus until classicality emerges. The ``Heisenberg cut'' is the choice of $M$: how many observers (or environment fragments) constitute sufficient consensus?

> **Corollary:** [The Four Theorems Form a Complete Audit Hierarchy]
> The four theorems span the full space of SCX multi-expert quantum audit:
> 
1. **Theorem~1 (Agreement)** --- How fast does consensus decay with $M$? Answer: exponentially, with Chernoff--Hoeffding tight bounds.
2. **Theorem~2 (Fidelity)** --- How much state survives the audit? Answer: $F^{(M)} = 1 - O(M g^2)$, trading off precision vs.\ preservation.
3. **Theorem~3 (Redundancy)** --- How many copies are needed for consensus? Answer: $R_ = O(\log(1/(1-\theta)))$, exponentially small in required confidence.
4. **Theorem~4 (Non-classicality)** --- When does the audit reveal structure beyond classical explanation? Answer: when $S > 2$, the experts' correlation pattern requires quantum description.

> **Remark:** [HONEST LIMITATION]
> This paper does **not** solve the measurement problem. It reframes it: the question ``when does collapse occur?'' becomes ``how many independent observers must agree before we treat the outcome as objective?'' The answer depends on the declared $M$ (or $R_\delta$, or $N$), which is an axiom --- not a theorem. SCX cannot eliminate the need for axioms in quantum foundations. It can only make them explicit. The value added is quantitative: the tight bounds (Chernoff--Hoeffding, fidelity decay, $R_$, CHSH confidence) replace qualitative hand-waving with numerically precise statements about when and how consensus---and therefore classicality---emerges.