# Introduction 引言

**Author:** SCX

*Abstract:*

Supply chain traceability (供应链溯源) requires certifying that origin claims---organic certification (有机认证), fair-trade compliance (公平贸易), conflict-free sourcing (冲突矿产)---propagate faithfully from farm to shelf. Current approaches rely on centralized auditors or blockchain-immutable ledgers, neither of which provides formal guarantees when intermediate nodes are adversarial. We apply the SCX{} (SCX) multi-expert audit framework to supply chain traceability, treating each supply chain node as an independent auditor of upstream claims. We formalize the supply chain as a directed acyclic graph (DAG) of $K$ nodes, where node $k$ receives a claim vector $c_{k-1}$ from its immediate upstream neighbor and independently verifies it against physical inspection data $x_k$. The origin node publishes a certification claim (origin claim) that propagates downstream; every intermediate node audits the received claim against its local observations. We prove three core theorems. **Theorem~1 (Origin Certification Consensus 产地认证共识):** With $M$ independently verifying nodes, the probability that a false origin claim escapes detection decays exponentially as $\exp(-2M_{\mathrm{eff}} \Delta^2)$, where $\Delta$ is the per-node verification power and $M_{\mathrm{eff}}$ corrects for correlated verification methods. **Theorem~2 (Chain-of-Custody Unidentifiability 监管链不可辨识性):** When a discrepancy (防伪) is detected at node $k$ (i.e., $\norm{c_{k-1} - x_k} > \varepsilon$), the cause among \{upstream fraud, measurement error at $k$, environmental degradation, label switching\} is structurally unidentifiable without declared assumptions, establishing the necessity of the SCX assumption registry for supply chain forensics. **Theorem~3 (Spring Hash-Gating for Counterfeit Prevention Spring哈希门控防伪):** We construct a cryptographic hash chain $\hashChain_k = \hashFunc(\hashChain_{k-1}, x_k, \tau_k)$ where $Spring$'s gating function $M_t$ activates an incremental audit at node $k$ when the hash-chain discrepancy exceeds a dynamic threshold, enabling blockchain integration (区块链集成) over existing hash infrastructure. We define the Cercis{} traceability score $S = Q + \eta \cdot N$ combining certification accuracy ($Q$) with supply chain regime coverage ($N$) including multi-hop origin chains, cold-chain integrity (冷链完整性), and conflict-zone provenance (冲突地区来源). A full experimental protocol is specified on agricultural supply chains (coffee, cocoa, palm oil) with GPS-verified farm coordinates, spectral commodity fingerprinting, and IoT temperature logging, with explicit assumption-to-conclusion audit trails and Chinese/English bilingual terminology mappings.

**Keywords:** SCX audit, supply chain traceability, 供应链溯源, origin certification 产地认证, counterfeit detection 防伪, organic certification 有机认证, conflict minerals 冲突矿产, hash chain 哈希链, blockchain 区块链, fair trade 公平贸易, cold chain 冷链, Spring{} gating, Yajie{} consensus, Cercis{} score, multi-node verification 多节点验证

## Introduction 引言

Modern supply chains are global, multi-tiered, and opaque. A coffee bean harvested in Ethiopia may pass through a local cooperative, a regional processor, an exporter, an importer, a roaster, a distributor, and a retailer before reaching a consumer in Berlin. At each step, claims about the product's origin---organic certification, fair-trade status, geographical indication, conflict-free provenance---are asserted by the upstream node and must be trusted by the downstream node. The economic incentive to counterfeit these claims is substantial: certified organic coffee commands a 20--40\% price premium  [cite], conflict-free minerals are required by regulation (Dodd-Frank Section 1502; EU Conflict Minerals Regulation), and fair-trade labels influence \$9.8B in annual consumer spending  [cite].

The current state of supply chain traceability relies on two families of solutions, neither of which provides formal certification guarantees under adversarial conditions. **Centralized auditing** (e.g., third-party certifiers like Ecocert, Fairtrade International, or the Responsible Minerals Initiative) inspects a subset of nodes and issues certificates, but faces a fundamental sampling problem: with $K$ nodes in the chain, auditing a fraction $\alpha < 1$ leaves $(1-\alpha)K$ nodes unverified, any of which could introduce counterfeit products. **Blockchain-based traceability**  [cite] records every transaction on an immutable ledger, ensuring that *recorded* data cannot be altered post hoc, but does not guarantee that the *recorded* data corresponds to physical reality---the ``garbage-in, garbage-out'' (GIGO) problem. A fraudulent node can record a false claim on the blockchain as easily as on paper.

The SCX framework  [cite] provides a fundamentally different approach: rather than trusting a centralized auditor or an immutable but potentially false record, we treat every node in the supply chain as a potential auditor of its upstream neighbors. The key insight is that **physical inspection at node $k$ is a source of independent evidence about the claim propagated from upstream nodes**. When a coffee roaster receives a shipment labeled ``organic Ethiopian Yirgacheffe'' and performs spectral analysis, the roaster's measurement $x_k$ provides statistical evidence about the truth of the upstream origin claim $c_{k-1}$. By formalizing this multi-node verification as a distributed hypothesis test, we obtain formal detection guarantees that degrade gracefully with adversarial behavior.

**Contributions.** This paper provides:

1. **Formalization** (Section [ref]): The supply chain as a directed acyclic graph with claim propagation and physical verification. Each node is both a claimant (to downstream nodes) and an auditor (of upstream nodes). Eleven explicit assumptions~\assumptionTag{1}--\assumptionTag{11}.
2. **Three theorems with full proofs:**
3. **Multi-node Cercis{} score** (Section [ref]): A traceability score combining certification accuracy and supply chain regime coverage.
4. **Experimental protocol** (Section [ref]): Agricultural supply chains (coffee, cocoa, palm oil) with GPS verification, spectral fingerprinting, IoT temperature logging, and explicit assumption-to-conclusion audit trails.
5. **Discussion** (Section [ref]): Honest limitations including cost of per-node verification, collusion resistance bounds, and the fundamental tension between traceability and privacy.

**What this paper is not.** We do not propose a new blockchain protocol, a new certification standard, or a hardware solution for physical tagging. We provide a mathematical framework for understanding when and how multi-node verification can provide formal traceability guarantees, and we identify the structural conditions under which those guarantees fail. The framework is compatible with existing blockchain and IoT infrastructure but does not depend on them.

### Motivating Examples 应用场景

**Organic coffee 有机咖啡.** A cooperative in Colombia claims organic certification. The exporter in Bogotá can verify pesticide residue via chemical assay. The importer in Hamburg can verify via spectral fingerprinting. The roaster in Berlin can verify via cupping profile consistency. Each node provides independent evidence; their consensus (or disagreement) determines whether the organic claim is credible.

**Conflict-free tantalum 冲突矿产钽.** A mine in the Democratic Republic of Congo claims conflict-free status under the OECD Due Diligence Guidance. The smelter in Rwanda can verify ore geochemical fingerprinting against the claimed mine of origin. The capacitor manufacturer in Japan can cross-reference the smelter's claim with the Responsible Minerals Assurance Process (RMAP) database. The electronics OEM can audit the full chain. At each step, a discrepancy would flag potential conflict mineral infiltration.

**Cold-chain pharmaceuticals 冷链药品.** A vaccine manufacturer claims continuous cold-chain integrity (2--8$^\circ$C) from production to administration. Each logistics node (warehouse, truck, clinic) records temperature logs. The receiving node can verify that the cumulative temperature excursion computed from the upstream hash chain is consistent with the physical product's potency assay. A discrepancy at any node triggers a Spring{}-gated audit.

## Formalization: Supply Chain as a Multi-Node Audit Network 供应链作为多节点审计网络
<!-- label: sec:formalization -->

### The Supply Chain Graph 供应链图

> **Definition:** [Supply Chain DAG 供应链有向无环图]
> <!-- label: def:chain -->
> A supply chain is a directed acyclic graph (DAG) $\chain = (\nodeSet, \mathcal{E})$ where:
> 
- $\nodeSet = \{1, 2, ..., K\}$ is the set of supply chain nodes (farm, cooperative, processor, exporter, importer, manufacturer, distributor, retailer);
- $(i \to j) \in \mathcal{E}$ indicates that physical goods flow from node $i$ to node $j$, and node $i$ asserts a claim to node $j$;
- Node $0 \notin \nodeSet$ denotes the **origin** (the physical source: farm, mine, production facility), which publishes the initial **origin claim** $c_0$;
- Node $K+1 \notin \nodeSet$ denotes the **consumer**, who receives the final claim $c_K$.

For notational simplicity, we primarily analyze the linear chain case ($i \to i+1$ for $i = 0, 1, ..., K$) and discuss DAG generalizations in Section [ref].

> **Definition:** [Node State and Claim 节点状态与声明]
> <!-- label: def:node_state -->
> At each node $k \in \{1, ..., K\}$:
> 
- **Received claim:** $c_{k-1} \in \claimSpace \subset \R^d$ is the claim vector propagated from the upstream node. Components include: origin coordinates (GPS lat/lon), certification type (organic, fair-trade, conflict-free, geographical indication), production date, batch identifier, chemical fingerprint vector.
- **Physical measurement:** $x_k \in \R^p$ is the node's independent physical inspection of the received goods. Components include: spectral reflectance, chemical assay results, weight/volume verification, temperature log summary, visual inspection features.
- **Published claim:** $\tilde{c}_k \in \claimSpace$ is the claim that node $k$ propagates to node $k+1$. This may equal $c_{k-1}$ (faithful relay), be a verified-and-augmented version, or be a fraudulent substitution.
- **Verification result:** $v_k \in \{0, 1\}$ where $v_k = 1$ indicates that node $k$ detects a discrepancy between $c_{k-1}$ and its physical measurement $x_k$.

### The Origin Claim 产地声明

> **Definition:** [Origin Claim 产地声明]
> <!-- label: def:origin_claim -->
> The origin claim $c_0$ is a vector:
> 
> $$
>     c_0 = (geo, cert, prod, batch, fp, meta) \in \claimSpace,
>     <!-- label: eq:origin_claim -->
> $$
> 
> where:
> 
- $geo \in \R^2$: GPS coordinates of origin (farm polygon centroid, mine location);
- $cert \in \{0, 1\}^{n_{\mathrm{cert}}}$: binary vector of certifications claimed (organic, fair-trade, conflict-free, rainforest alliance, geographical indication);
- $prod \in \R^{n_{\mathrm{prod}}}$: production metadata (harvest date, variety, processing method);
- $batch \in \{0, 1\}^b$: unique batch identifier (hash of origin data);
- $fp \in \R^{n_{\mathrm{fp}}}$: chemical/spectral fingerprint of the commodity at origin;
- $meta \in \R^{n_{\mathrm{meta}}}$: additional verifiable claims (yield estimate, labor conditions, environmental impact metrics).

The origin claim is the root of all downstream verification. Every subsequent node $k$ tests $H_0^{(k)}: the goods match  c_0$ against $H_1^{(k)}: the goods deviate from  c_0$, using its local measurement $x_k$.

### The Hash Chain 哈希链

> **Definition:** [Supply Chain Hash Chain 供应链哈希链]
> <!-- label: def:hash_chain -->
> The distributed hash chain $\hashChain = (\hashChain_0, \hashChain_1, ..., \hashChain_K)$ is defined recursively:
> 
> $$
>     \hashChain_0 &= \hashFunc(c_0), <!-- label: eq:hash0 --> 

>     \hashChain_k &= \hashFunc(\hashChain_{k-1} \,\|\, x_k \,\|\, \tilde{c}_k \,\|\, \tau_k), \quad k = 1, ..., K, <!-- label: eq:hash_k -->
> $$
> 
> where $\hashFunc: \{0, 1\}^* \to \{0, 1\}^{256}$ is a cryptographic hash function (SHA-256), $\|$ denotes concatenation, and $\tau_k$ is the timestamp at node $k$'s verification. The hash chain provides a tamper-evident audit trail: any alteration of $c_0$ or any intermediate $x_k$, $\tilde{c}_k$, or $\tau_k$ changes all subsequent hashes, making the alteration detectable by any node that stores the chain.

This hash chain is compatible with existing blockchain infrastructure: $\hashChain_K$ can be anchored to a public blockchain (Ethereum, Hyperledger) at any point, providing a cryptographic bridge between physical supply chain verification and immutable ledger storage.

### Verification Model 验证模型

> **Definition:** [Node Verification Function 节点验证函数]
> <!-- label: def:verification -->
> Node $k$'s verification is a statistical hypothesis test:
> 
> $$
>     v_k = \ind{\norm{\phi(c_{k-1}) - \psi(x_k)} > \varepsilon_k},
>     <!-- label: eq:verification -->
> $$
> 
> where:
> 
- $\phi: \claimSpace \to \R^q$ maps the received claim to a verification-relevant feature space;
- $\psi: \R^p \to \R^q$ maps the physical measurement to the same feature space;
- $\varepsilon_k > 0$ is node $k$'s verification threshold;
- $v_k = 1$ indicates a **discrepancy** (防伪警报).

> **Definition:** [Verification Power 验证能力]
> <!-- label: def:verification_power -->
> Node $k$'s verification power $\Delta_k$ is the minimum detectable deviation:
> 
> $$
>     \Delta_k = \inf_{\delta > 0} \left\{ \delta : \Pbb\left(\norm{\phi(c_{k-1}) - \psi(x_k)} > \varepsilon_k \;\middle|\; \norm{c_0^{true} - c_0} = \delta\right) \geq 1 - \beta \right\},
>     <!-- label: eq:verification_power -->
> $$
> 
> where $c_0^{true}$ is the true origin state and $\beta \in (0,1)$ is the target Type II error rate. $\Delta_k$ quantifies the smallest origin claim deviation that node $k$ can detect with power $1 - \beta$.

### Adversarial Model 对抗模型

> **Definition:** [Adversarial Node 对抗节点]
> <!-- label: def:adversarial -->
> A node $k$ is **adversarial** if it deliberately publishes $\tilde{c}_k \neq c_{k-1}$ when $v_k = 0$ (fabrication), or if it publishes $\tilde{c}_k = c_{k-1}$ when $v_k = 1$ (suppression). Let $\mathcal{A} \subseteq \nodeSet$ be the set of adversarial nodes, with $|\mathcal{A}| = A$. Nodes not in $\mathcal{A}$ are **honest**.

> **Definition:** [Collusion 共谋]
> <!-- label: def:collusion -->
> A coalition $\mathcal{C} \subseteq \mathcal{A}$ of adversarial nodes colludes if they coordinate their published claims $\{\tilde{c}_k\}_{k \in \mathcal{C}}$ to evade detection. The coalition's power is limited by the number and position of colluding nodes: consecutive adversarial nodes can propagate a false claim without intermediate honest verification.

### Assumptions 假设

\begin{assumption}[A1: Linear Claims with Additive Noise 线性声明加性噪声]
<!-- label: ass:A1 -->
When node $k$ honestly relays a claim, its published claim differs from the received claim only by independent verification noise: $\tilde{c}_k = c_{k-1} + \eta_k$ where $\eta_k \sim \mathcal{N}(0, \Sigma_k)$ and $\eta_k \perp \eta_{k'}$ for $k \neq k'$.
\end{assumption}

\begin{assumption}[A2: Conditionally Independent Verification 条件独立验证]
<!-- label: ass:A2 -->
Conditional on the true origin state $c_0^{true}$, the physical measurements $x_k$ are mutually independent across honest nodes. This holds when nodes use physically distinct measurement instruments, non-overlapping sample subsets, and independent calibration protocols.
\end{assumption}

\begin{assumption}[A3: Bounded Adversarial Fraction 有界对抗比例]
<!-- label: ass:A3 -->
The fraction of adversarial nodes satisfies $A/K \leq \alpha_ < 1/2$. If a majority of nodes are adversarial, no distributed verification protocol can provide non-trivial guarantees (impossibility result from distributed consensus  [cite]).
\end{assumption}

\begin{assumption}[A4: Measurement Map Identifiability 测量映射可辨识性]
<!-- label: ass:A4 -->
The composed map $\psi^{-1} \circ \phi$ is well-defined on the range of $\phi$: given a physical measurement $x_k$, the set of possible origin states consistent with $x_k$ is bounded. Formally, $\exists B > 0$ such that $\norm{\psi^{-1}(\phi(c)) - c} \leq B$ for all $c \in \claimSpace$.
\end{assumption}

\begin{assumption}[A5: Cryptographic Hash Collision Resistance 密码哈希抗碰撞性]
<!-- label: ass:A5 -->
The hash function $\hashFunc$ is collision-resistant: for any polynomial-time adversary, $\Pbb(\hashFunc(x) = \hashFunc(y) \mid x \neq y) \leq \nu(\lambda)$ where $\nu$ is negligible in the security parameter $\lambda$.
\end{assumption}

\begin{assumption}[A6: Honest Majority of Auditing Nodes 审计节点的诚实多数]
<!-- label: ass:A6 -->
For any consecutive segment of length $s$ in the supply chain, at least $\lceil s/2 \rceil$ nodes are honest. This ensures that no contiguous adversarial segment can suppress a discrepancy undetected.
\end{assumption}

\begin{assumption}[A7: Verification Threshold Calibration 验证阈值校准]
<!-- label: ass:A7 -->
Each node's threshold $\varepsilon_k$ is calibrated against its measurement noise: $\varepsilon_k \geq z_{1-\alpha_k/2} \cdot \sigma_k$ where $\sigma_k$ is the measurement standard deviation and $\alpha_k$ is the target false-positive rate. Under $H_0$ (no origin violation), $\E[v_k] = \alpha_k$.
\end{assumption}

\begin{assumption}[A8: Upstream Honesty Propagation 上游诚实传播]
<!-- label: ass:A8 -->
If node $k$ detects a discrepancy ($v_k = 1$) and is honest, it publishes an alert along with its measurement evidence. The alert propagates to all downstream nodes via the hash chain inclusion of $\tilde{c}_k \neq c_{k-1}$ in $\hashChain_k$.
\end{assumption}

\begin{assumption}[A9: Blockchain Anchoring Timeliness 区块链锚定时效性]
<!-- label: ass:A9 -->
The terminal hash $\hashChain_K$ is anchored to a public blockchain within time $T_$ of the final consumer transaction. Before anchoring, the hash chain is stored in a distributed manner across honest nodes.
\end{assumption}

\begin{assumption}[A10: Origin Fingerprint Stability 产地指纹稳定性]
<!-- label: ass:A10 -->
The chemical/spectral fingerprint $fp$ of a commodity from origin $c_0^{true}$ is stable within a batch: $\norm{fp(c_0^{true}) - fp(sample)} \leq \sigma_{fp}$ for all samples drawn from the same batch. Inter-origin separation satisfies $\norm{fp(c_0^A) - fp(c_0^B)} \geq d_ > 2\sigma_{fp}$ for distinct origins $A \neq B$.
\end{assumption}

\begin{assumption}[A11: Consumer-Side Verification 消费者端验证]
<!-- label: ass:A11 -->
The consumer (node $K+1$) can verify the full hash chain $\hashChain_0, ..., \hashChain_K$ against the blockchain-anchored $\hashChain_K$, and can optionally perform a terminal physical verification $x_{K+1}$ (e.g., QR-code-linked spectral scan, DNA barcode test).
\end{assumption}

\begin{limitationTag}{1}
If adversarial nodes control all measurement instruments (e.g., a single laboratory certifying an entire region), Assumption [ref] is violated and detection guarantees degrade to the single-auditor case.
\end{limitationTag}

\begin{limitationTag}{2}
Assumption [ref] (origin fingerprint stability) may fail for processed goods where the fingerprint is altered by roasting, refining, or blending. The fingerprinting model must be adapted per commodity type.
\end{limitationTag}

## Theorem 1: Multi-Node Origin Certification Consensus 多节点产地认证共识
<!-- label: sec:theorem1 -->

We prove that when $M$ honest nodes independently verify an origin claim, the probability that a false claim escapes detection decays exponentially in $M$. This is the traceability analogue of the Yajie{} consensus: multiple independent verifiers produce an auditable confidence bound on origin claim truth.

### Detection Probability for a Single Node

> **Lemma:** [Single-Node Detection 单节点检测]
> <!-- label: lem:single_node -->
> Under Assumptions [ref],  [ref],  [ref], and [ref], if the origin claim deviates from truth by $\delta = \norm{c_0 - c_0^{true}}$, an honest node $k$ with verification power $\Delta_k$ detects the deviation with probability:
> 
> $$
>     \Pbb(v_k = 1 \mid \delta) \geq 1 - \exp\left(-\frac{(\max(0, \delta - \varepsilon_k))^2}{2\sigma_k^2}\right),
>     <!-- label: eq:single_node_detection -->
> $$
> 
> where $\sigma_k^2$ is the measurement variance of node $k$'s verification function.

> **Proof:** \rigorFull
> **Step 1: Discrepancy signal.** The verification statistic at node $k$ is $s_k = \norm{\phi(c_{k-1}) - \psi(x_k)}$. Under honest upstream relay (Assumption [ref]), $c_{k-1} = c_0 + \sum_{j=1}^{k-1} \eta_j$. The physical measurement is $x_k = \mu(c_0^{true}) + \xi_k$ where $\mu(c)$ is the expected measurement for origin state $c$, and $\xi_k \sim \mathcal{N}(0, \Sigma_k^{meas})$ is measurement noise.
> 
> **Step 2: Signal decomposition.** When $c_0 \neq c_0^{true}$, the expected verification statistic is:
> 
> $$
>     \E[s_k \mid c_0, c_0^{true}] = \norm{\phi(c_0) - \psi(\mu(c_0^{true}))}.
> $$
> 
> Let $\delta_{\mathrm{eff}} = \norm{\phi(c_0) - \psi(\mu(c_0^{true}))}$ be the effective deviation in feature space. By Assumption [ref] (measurement map identifiability), $\delta_{\mathrm{eff}} \geq L^{-1} \delta$ for some Lipschitz constant $L > 0$ of the feature mapping.
> 
> **Step 3: Concentration.** Under Gaussian measurement noise, $s_k$ follows a non-central chi distribution. For $\delta_{\mathrm{eff}} > \varepsilon_k$, non-detection requires $s_k \leq \varepsilon_k$. By the Gaussian tail bound on the underlying normal variable:
> 
> $$
>     \Pbb(s_k \leq \varepsilon_k \mid \delta_{\mathrm{eff}}) \leq \exp\left(-\frac{(\delta_{\mathrm{eff}} - \varepsilon_k)^2}{2\sigma_k^2}\right).
> $$
> 
> 
> Substituting the Lipschitz relationship $\delta_{\mathrm{eff}} \geq L^{-1} \delta$ yields the stated bound, absorbing $L$ into the effective $\sigma_k$ for notational simplicity.  $\square$

### Multi-Node Consensus Detection

> **Definition:** [Aggregate Detection Statistic 聚合检测统计量]
> <!-- label: def:aggregate_detection -->
> Given $M$ honest verifying nodes, the aggregate detection statistic is:
> 
> $$
>     V_M = \sum_{k=1}^{M} v_k,
>     <!-- label: eq:V_M -->
> $$
> 
> the count of nodes that flag a discrepancy. Detection is declared when $V_M \geq \tau_M$ for a threshold $\tau_M$.

> **Theorem:** [Multi-Node Origin Certification Consensus 多节点产地认证共识]
> <!-- label: thm:origin -->
> Under Assumptions [ref]-- [ref], let $M$ honest nodes independently verify the origin claim $c_0$ with verification powers $\Delta_1, ..., \Delta_M$. Define the effective number of independent verifiers as $M_{\mathrm{eff}} = M / (1 + (M-1)\bar)$, where $\bar$ is the average pairwise correlation of node verification errors. Then:
> 
> 
1. **False alarm control:** Under $H_0$ ($c_0 = c_0^{true}$), setting $\tau_M = \lceil M \alpha + \sqrt{2M \alpha (1-\alpha) \log(1/\delta_{FA})} \rceil$ yields $\Pbb(V_M \geq \tau_M \mid H_0) \leq \delta_{FA}$, where $\alpha = \max_k \alpha_k$ is the maximum per-node false-positive rate.
2. **Detection power:** Under $H_1$ ($\norm{c_0 - c_0^{true}} = \delta > 0$), the probability of undetected origin violation is bounded by:
3. **Exponential decay:** As $M \to \infty$, for any fixed $\delta > \max_k \varepsilon_k$:

> \rigorFull

> **Proof:** *(i) False alarm control.* Under $H_0$, $v_k \sim Bernoulli(\alpha_k)$ independently (Assumption [ref]). By Hoeffding's inequality for bounded independent random variables:
> 
> $$
>     \Pbb\left(\frac{1}{M}\sum_{k=1}^{M} v_k - \bar \geq t \right) \leq \exp(-2M t^2),
> $$
> 
> where $\bar = \frac{1}{M}\sum_k \alpha_k$. Setting $t = \sqrt{\frac{\log(1/\delta_{FA})}{2M}}$ and $\tau_M = \lceil M(\bar + t) \rceil$ yields the stated false-alarm bound.
> 
> *(ii) Detection power.* Under $H_1$, the probability that an individual node $k$ detects is $p_k(\delta) = \Pbb(v_k = 1 \mid \delta) \geq 1 - \exp(-(\delta - \varepsilon_k)^2 / (2\sigma_k^2))$ by Lemma [ref]. The event of non-detection requires $V_M < \tau_M$.
> 
> For correlated Bernoulli variables with average correlation $\bar$, the variance of the sum is inflated: $\Var(V_M) = M\bar{p}(1-\bar{p})(1 + (M-1)\bar)$, where $\bar{p} = \bar{p}(\delta)$. Define $M_{\mathrm{eff}}$ as above. Applying Hoeffding's inequality with effective sample size:
> 
> $$
>     \Pbb\left(\frac{V_M}{M} - \bar{p} \leq -(\bar{p} - \tau_M/M)\right) \leq \exp\left(-2M_{\mathrm{eff}} (\bar{p} - \tau_M/M)^2\right).
> $$
> 
> 
> *(iii) Exponential decay.* As $M \to \infty$, $M_{\mathrm{eff}} \to 1/\bar$ if $\bar > 0$, or diverges as $M$ if $\bar = 0$. In either case, for $\delta$ bounded away from $\varepsilon_k$, Lemma [ref] gives $\bar{p}(\delta) \to 1$ exponentially fast in $\delta^2$. The worst-case per-node gap $(\bar{p} - \tau_M/M)$ is driven by the node with weakest detection power, yielding the min over $k$ in Eq. [ref].  $\square$

> **Corollary:** [Minimum Honest Verifiers 最小诚实验证者数量]
> <!-- label: cor:min_verifiers -->
> For target detection probability $1 - \gamma$ and origin deviation $\delta$, the minimum number of honest verifying nodes required is:
> 
> $$
>     M^*(\delta, \gamma) = \left\lceil \frac{2\bar^2 \log(1/\gamma) \cdot (1 + (M^*-1)\bar)}{(\delta - \bar)^2} \right\rceil,
>     <!-- label: eq:M_star -->
> $$
> 
> where $\bar^2 = (\frac{1}{M}\sum_k 1/\sigma_k^2)^{-1}$ and $\bar = \max_k \varepsilon_k$. For $\bar = 0$, this simplifies to $M^* = \lceil 2\bar^2 \log(1/\gamma) / (\delta - \bar)^2 \rceil$.

> **Remark:** [Comparison with Centralized Auditing 与集中式审计的比较]
> <!-- label: rem:centralized_comparison -->
> A centralized auditor sampling $\alpha K$ nodes detects fraud with probability at most $\alpha$ if the fraudulent node is uniformly distributed. Multi-node verification with $M$ nodes achieves detection probability $1 - \exp(-\Omega(M))$, which dominates centralized sampling for any $M \geq \lceil \log(1/(1-\alpha)) / (2\Delta^2) \rceil$. The key advantage is that every shipment-carrying node is a potential verifier, not a sampled subset.

## Theorem 2: Chain-of-Custody Unidentifiability 监管链不可辨识性
<!-- label: sec:theorem2 -->

When a discrepancy is detected at node $k$, the natural forensic question is: *where did the violation occur?* We prove that without declared assumptions, the location and nature of the violation are structurally unidentifiable from discrepancy data alone. This is the traceability instantiation of \ThmSCXHonest{} (the Honest Agent Theorem).

### The Unidentifiability Problem

Consider a linear supply chain of $K$ nodes. At node $k$, a discrepancy is detected: $v_k = 1$. The discrepancy could arise from:

1. **Upstream fraud C1 (上游欺诈):** The origin claim $c_0$ was false, and the fraud propagated undetected through nodes $1, ..., k-1$;
2. **Intermediate substitution C2 (中间替换):** An honest node $j < k$ relayed truthfully, but an adversarial node $\ell \in (j, k]$ substituted counterfeit goods and fabricated a consistent claim;
3. **Measurement error at node $k$ C3 (节点$k$测量误差):** The goods are authentic but node $k$'s physical measurement $x_k$ suffered a rare large deviation (false positive);
4. **Environmental degradation C4 (环境退化):** The goods were authentic at origin but degraded during transit (temperature excursion degrading spectral fingerprint, moisture damage altering chemical markers);
5. **Label switching C5 (标签调换):** The physical goods are authentic but the claim label $c_{k-1}$ was attached to a different batch at some upstream node.

> **Theorem:** [Chain-of-Custody Unidentifiability 监管链不可辨识性]
> <!-- label: thm:unident -->
> Let $\chain$ be a linear supply chain with $K$ nodes. Suppose node $k$ detects a discrepancy ($v_k = 1$). Under Assumptions [ref]-- [ref], the cause of the discrepancy among $\{C1, C2, C3, C4, C5\}$ is structurally unidentifiable from the observed data $(c_0, \{x_j, \tilde{c}_j, v_j\}_{j=1}^{k})$ without additional declared assumptions.
> 
> Formally, for any two distinct causes $C_a \neq C_b$, there exists a pair of supply chain configurations $\mathcal{S}_a$ and $\mathcal{S}_b$ that are observationally equivalent:
> 
> $$
>     \Pbb(data \mid \mathcal{S}_a) = \Pbb(data \mid \mathcal{S}_b),
>     <!-- label: eq:observational_equivalence -->
> $$
> 
> yet attribute the discrepancy to cause $C_a$ in $\mathcal{S}_a$ and cause $C_b$ in $\mathcal{S}_b$.
> \rigorFull

> **Proof:** We construct explicit observationally equivalent configurations for each pair of causes.
> 
> **Step 1: C1 (upstream fraud) vs. C2 (intermediate substitution).** Consider Configuration $\mathcal{S}_1$: origin claim $c_0^{(false)}$ is fraudulent; all nodes $1, ..., k-1$ relay honestly without detection because their verification powers satisfy $\Delta_j < \norm{c_0^{(false)} - c_0^{true}}$. Node $k$ detects the fraud.
> 
> Configuration $\mathcal{S}_2$: origin claim $c_0^{(true)}$ is authentic; node $k-1$ is adversarial and substitutes goods with properties matching $c_0^{(false)}$, publishing $\tilde{c}_{k-1} = c_0^{(false)}$. Node $k$ detects the discrepancy against $\tilde{c}_{k-1}$.
> 
> Both configurations produce identical observations: $c_0$ observed, $v_j = 0$ for $j < k$, $v_k = 1$, and physical measurement $x_k$. The likelihood functions are identical because the data $(c_0, x_k, \{v_j\})$ do not distinguish whether the false claim originated at node 0 or node $k-1$.
> 
> **Step 2: C1/C2 vs. C3 (measurement error).** Configuration $\mathcal{S}_3$: origin claim and all intermediate relays are truthful; goods are authentic. Node $k$'s measurement $x_k$ is a $q$-sigma outlier: $x_k = \mu(c_0^{true}) + \xi_k$ where $\norm{\xi_k} = q\sigma_k$ with $q > \varepsilon_k/\sigma_k$.
> 
> Configuration $\mathcal{S}_1$ (upstream fraud) with a specific fraud magnitude $\delta$ chosen so that $\phi(c_0^{(false)}) = \psi(x_k^{observed})$ exactly. These are observationally equivalent because the observed $x_k$ is identical, and the discrepancy signal $\norm{\phi(c_{k-1}) - \psi(x_k)}$ is identical.
> 
> **Step 3: C4 (environmental degradation).** Let $c_0^{true}$ be the authentic origin fingerprint. Environmental degradation applies a transformation $T_{env}: \R^p \to \R^p$ to the physical goods, so that the goods arriving at node $k$ have fingerprint $T_{env}(fp(c_0^{true}))$. If $\norm{\psi(T_{env}(fp(c_0^{true}))) - \phi(c_0)} > \varepsilon_k$, a discrepancy is detected.
> 
> This is observationally equivalent to upstream fraud where $c_0^{(false)}$ is chosen such that the fraudulent goods have fingerprint matching $T_{env}(fp(c_0^{true}))$. The observed $x_k$ is identical in both cases.
> 
> **Step 4: Continuous equivalence manifold.** The five causes span a continuous 4$p$-dimensional manifold of observationally equivalent configurations. Any point in this manifold is parameterized by a tuple $(\delta_{fraud}, \delta_{subst}, \delta_{meas}, \delta_{env}, \delta_{switch})$ with sum constrained by the observed discrepancy magnitude. The data alone cannot resolve this decomposition.
> 
> **Step 5: Genericity.** The construction is not pathological. Every real-world supply chain discrepancy faces this ambiguity. When a European importer detects pesticide residue in ``organic'' coffee, is the organic certificate fraudulent (C1), did a middleman blend conventional beans (C2), did the testing lab make an error (C3), did pesticide drift from a neighboring conventional farm contaminate the shipment (C4), or was the organic label swapped onto a conventional batch (C5)? Without explicit assumptions, all five are consistent with the data.
> 
> **Step 6: The necessity of assumptions.** The unidentifiability is resolved only by declaring and justifying which causes are assumed negligible. For example: ``We assume C3 (measurement error) is negligible because the discrepancy magnitude $5.2\sigma$ has probability $< 10^{-7}$ under the null.'' Or: ``We assume C4 (environmental degradation) is negligible because pesticide X is not approved for use in any neighboring farms (verified by satellite crop classification).'' The theorem's force is that these assumptions are *necessary*---without them, attribution is logically indeterminate.  $\square$

> **Corollary:** [Assumption Mandate for Supply Chain Forensics 供应链取证假设声明要求]
> <!-- label: cor:assumption_mandate -->
> Any attribution of a detected supply chain discrepancy to a specific cause **must** be accompanied by:
> 
1. An explicit declaration of which causes (C1--C5) are assumed negligible;
2. A quantitative justification for each assumption (e.g., ``probability of measurement error exceeding this threshold is $< 10^{-6}$ under instrument calibration data'');
3. A sensitivity analysis showing how the attribution changes if each assumption is relaxed.

> **Remark:** [Connection to the Honest Agent Theorem 与诚实代理定理的关联]
> <!-- label: rem:honest_connection -->
> Theorem [ref] is the supply-chain instantiation of \ThmSCXHonest{}. The Honest Agent Theorem establishes that when multiple error sources contribute to an observed discrepancy, their individual contributions are unidentifiable from output alone. In traceability, the error sources are the five causes C1--C5. The supply chain setting amplifies the unidentifiability because: (i) physical goods can be altered by adversaries, environment, and measurement error simultaneously; (ii) the chain structure means errors accumulate and interact; (iii) economic incentives create asymmetric pressure to attribute discrepancies to external causes (C3, C4) rather than internal fraud (C1, C2).

## Theorem 3: Spring Hash-Gating for Counterfeit Prevention Spring哈希门控防伪
<!-- label: sec:theorem3 -->

We now construct a cryptographic mechanism that (i) links physical verification to an immutable hash chain, (ii) uses Spring{}'s gating function $M_t$ to trigger incremental audits when discrepancies accumulate across nodes, and (iii) integrates with existing blockchain infrastructure without requiring on-chain storage of all physical measurements.

### The Spring{ Gating Function}

> **Definition:** [Spring Gating Function Spring门控函数]
> <!-- label: def:spring_gating -->
> The Spring{} gating function $M_t: \N \times \R^K \to \{0, 1\}$ determines whether a full audit is triggered after processing $t$ batches through the supply chain:
> 
> $$
>     M_t(\{v_k^{(b)}\}_{b=1}^{t}) = \ind{\sum_{b=1}^{t} \sum_{k=1}^{K} w_k \cdot v_k^{(b)} > \Theta_t},
>     <!-- label: eq:M_t -->
> $$
> 
> where:
> 
- $v_k^{(b)} \in \{0, 1\}$ is the discrepancy indicator at node $k$ for batch $b$;
- $w_k > 0$ is the **node weight**: upstream nodes have higher weight because a discrepancy early in the chain affects all downstream products;
- $\Theta_t$ is the **dynamic audit threshold**, which tightens as more data accumulates:

The intuition: $M_t = 0$ corresponds to ``normal operation'' where per-node verifications proceed automatically and only the hash chain is recorded. $M_t = 1$ triggers a ``Spring{} audit'': a human-in-the-loop investigation, re-verification of all upstream nodes, and potential quarantine of suspect batches.

### Hash Chain Security under Spring{ Gating}

> **Definition:** [Extended Hash Chain with Spring{} Audit 扩展哈希链含Spring审计]
> <!-- label: def:extended_hash -->
> The extended hash chain incorporates the Spring{} audit result:
> 
> $$
>     \hashChain_k^{(b)} &= \hashFunc(\hashChain_{k-1}^{(b)} \,\|\, x_k^{(b)} \,\|\, \tilde{c}_k^{(b)} \,\|\, \tau_k^{(b)} \,\|\, a_k^{(b)}), <!-- label: eq:extended_hash -->
> $$
> 
> where $a_k^{(b)} \in \{0, 1\}$ indicates whether node $k$ in batch $b$ was subject to a Spring{}-triggered audit ($a_k^{(b)} = 1$). The audit produces additional evidence $e_k^{(b)}$ (laboratory re-test results, witness statements, satellite imagery) that is appended to the hash chain as an audit extension block.

> **Theorem:** [Spring Hash-Gating Security Spring哈希门控安全性]
> <!-- label: thm:spring_hash -->
> Under Assumptions [ref]-- [ref], the Spring{}-gated hash chain provides three security properties:
> 
> 
1. **Tamper evidence 篡改可证性:** Any post-hoc alteration of any $c_0$, $x_k$, $\tilde{c}_k$, or $\tau_k$ for any $k$ changes $\hashChain_K$ with probability $1 - \nu(\lambda)$ (where $\nu$ is negligible), and this change is detectable by any party that stores the original $\hashChain_K$.
2. **Adversarial evasion bound 对抗逃避界:** An adversary controlling $A$ consecutive nodes can suppress a discrepancy from the hash chain only if $v_k = 0$ for all $k$ in the adversarial segment. The probability that an adversarial segment of length $A$ successfully suppresses a true-origin discrepancy $\delta > 0$ is bounded by:
3. **Cumulative detection via Spring{} gating Spring门控累积检测:** As $t \to \infty$ batches traverse the chain, the probability that a persistent origin fraud (same fraudulent $c_0$ across all batches) evades Spring{} audit indefinitely decays super-exponentially:

> \rigorFull

> **Proof:** *(i) Tamper evidence.* By the collision resistance of $\hashFunc$ (Assumption [ref]), any change to the preimage of any $\hashChain_k$ produces a different hash with overwhelming probability. Since each $\hashChain_k$ includes $\hashChain_{k-1}$ in its preimage, a change at any level propagates through all subsequent hashes. The final hash $\hashChain_K$ therefore serves as a cryptographic commitment to the entire chain. Blockchain anchoring (Assumption [ref]) provides a public, immutable record of $\hashChain_K$.
> 
> *(ii) Adversarial evasion.* For the adversarial segment to suppress a discrepancy, every node in the segment must report $v_k = 0$, i.e., all must fail to detect the true origin deviation $\delta$. Under Assumption [ref] (conditional independence) and Lemma [ref]:
> 
> $$
>     \Pbb(all  v_k = 0  for  k \in segment \mid \delta)
>     &= \prod_{k \in segment} \Pbb(v_k = 0 \mid \delta) 

>     &\leq \prod_{k \in segment} \exp\left(-\frac{(\delta - \varepsilon_k)^2}{2\sigma_k^2}\right) 

>     &= \exp\left(-\sum_{k \in segment} \frac{(\delta - \varepsilon_k)^2}{2\sigma_k^2}\right).
> $$
> 
> This is minimized when $A$ is maximized, giving Eq. [ref]. Note that adversarial nodes cannot falsify $v_k = 0$ when $\delta$ exceeds their measurement precision; they can only choose not to report a true detection.
> 
> *(iii) Cumulative detection.* Under persistent fraud, each batch $b$ provides an independent trial for each honest node. The cumulative discrepancy score $S_T = \sum_{b=1}^{T} \sum_{k=1}^{K} w_k v_k^{(b)}$ has expected value $\E[S_T] = T \cdot \sum_{k} w_k p_k(\delta)$ where $p_k(\delta) = \Pbb(v_k = 1 \mid \delta) > 0$. The Spring{} threshold $\Theta_T = \Theta_0 e^{-\lambda T}$ decreases exponentially. For $T$ sufficiently large, $\Theta_T < \E[S_T]/2$.
> 
> By Hoeffding's inequality:
> 
> $$
>     \Pbb(M_T = 0) &= \Pbb(S_T \leq \Theta_T) 

>     &\leq \Pbb\left(S_T - \E[S_T] \leq \Theta_T - \E[S_T]\right) 

>     &\leq \exp\left(-\frac{2(\E[S_T] - \Theta_T)^2}{T \cdot W^2}\right),
> $$
> 
> where $W = \sum_k w_k$. For large $T$, $\E[S_T] = \Theta(T)$ while $\Theta_T = \Theta_0 e^{-\lambda T} \to 0$, so the gap grows as $\Theta(T)$. The probability of $M_t = 0$ for all $t \leq T$ is the product of per-batch non-detection probabilities, each decaying exponentially, yielding the super-exponential bound $\exp(-\Omega(T^2))$.  $\square$

### Blockchain Integration 区块链集成

> **Definition:** [Blockchain-Anchored Traceability 区块链锚定溯源]
> <!-- label: def:blockchain -->
> The Spring{}-gated hash chain integrates with blockchain infrastructure via:
> 
1. **On-chain anchoring:** The terminal hash $\hashChain_K^{(b)}$ for each batch $b$ is posted to a smart contract as a compact 32-byte state root. Physical measurement data $\{x_k\}$ remains off-chain (stored in distributed hash tables or IPFS), referenced by content hash.
2. **Smart contract audit trigger:** When $M_t = 1$, the smart contract emits an `AuditTriggered` event containing the batch ID, the node $k$ at which the cumulative discrepancy threshold was exceeded, and the Merkle proof path from $\hashChain_k^{(b)}$ to the anchored $\hashChain_K^{(b)}$.
3. **Consumer verification:** A consumer scans a QR code to retrieve the full hash chain and verifies it against the blockchain-anchored root. The consumer's device recomputes $\hashChain_K$ from $\hashChain_0$ through all published $\{x_k, \tilde{c}_k, \tau_k\}$ and confirms the match.

\begin{algorithm}[htbp]
*Caption:* Spring{}-Gated Supply Chain Audit Protocol Spring门控供应链审计协议
<!-- label: alg:spring_audit -->
\begin{algorithmic}[1]
\Require Supply chain $\chain = (\nodeSet, \mathcal{E})$, origin claim $c_0$, batch ID $b$, node weights $\{w_k\}$, initial threshold $\Theta_0$, decay $\lambda$
\Ensure Hash chain $\{\hashChain_k\}$, Spring{} audit decisions $\{M_t\}$, blockchain anchor
\State $\hashChain_0 \gets \hashFunc(c_0)$
\State $S \gets 0$ \Comment{cumulative discrepancy score}
\For{$k = 1$ to $K$}
    \State Node $k$ receives claim $c_{k-1}$
    \State Node $k$ performs physical measurement $x_k$
    \State Node $k$ computes $v_k \gets \ind{\norm{\phi(c_{k-1}) - \psi(x_k)} > \varepsilon_k}$
    \If{$v_k = 1$ and node $k$ is honest}
        \State Node $k$ publishes alert with evidence $e_k = (\phi(c_{k-1}), \psi(x_k), \norm{diff})$
    \EndIf
    \State Node $k$ publishes $\tilde{c}_k$ (honest relay or adversarial substitution)
    \State $\hashChain_k \gets \hashFunc(\hashChain_{k-1} \,\|\, x_k \,\|\, \tilde{c}_k \,\|\, \tau_k \,\|\, \ind{audited})$
    \State $S \gets S + w_k \cdot v_k$
\EndFor
\State $\Theta \gets \Theta_0 \cdot \exp(-\lambda \cdot batch\_count)$
\If{$S > \Theta$}
    \State **Trigger Spring{} audit**: human investigation, upstream re-verification, batch quarantine
    \State $M_t \gets 1$
    \State Append audit extension block to hash chain with investigation results
\Else
    \State $M_t \gets 0$
\EndIf
\State Anchor $\hashChain_K$ to blockchain via smart contract
\State \Return $\{\hashChain_k\}_{k=0}^K$, $M_t$, blockchain transaction ID
\end{algorithmic}
\end{algorithm}

> **Corollary:** [Batch-Level Guarantees 批次级保证]
> <!-- label: cor:batch_guarantees -->
> For a supply chain processing $B$ independent batches with the same origin claim $c_0$, define the batch-level fraud detection probability $P_{batch}(B) = 1 - \prod_{b=1}^{B} \Pbb(undetected in batch  b)$. Under Assumptions [ref]-- [ref]:
> 
> $$
>     P_{batch}(B) \geq 1 - \exp\left(-B \cdot \frac{M_{\mathrm{eff}} \cdot (\delta - \bar)^2}{2\bar^2}\right),
>     <!-- label: eq:batch_detection -->
> $$
> 
> i.e., processing more batches through the same chain drives the undetected-fraud probability to zero exponentially in $B$.

## Multi-Node Cercis{ Score for Supply Chain Traceability 供应链溯源的Cercis多节点评分}
<!-- label: sec:cercis -->

The Cercis{} scoring framework ranks supply chains by traceability quality and regime coverage.

> **Definition:** [Traceability Quality Score 溯源质量分]
> <!-- label: def:traceability_Q -->
> For a supply chain $\chain$ evaluated over $N$ batches, the quality score is:
> 
> $$
>     Q(\chain) = -\Bigg(
>         \underbrace{\frac{1}{N}\sum_{b=1}^{N} \frac{1}{K}\sum_{k=1}^{K} \ind{v_k^{(b)} = 1 \mid H_0}}_{false positive rate  \alpha_{actual}}
>         \;+\;
>         \underbrace{\frac{1}{N_{fraud}}\sum_{b \in fraud} \ind{undetected}}_{false negative rate  \beta_{actual}}
>         \;+\;
>         \underbrace{\frac{1}{K}\sum_{k=1}^{K} \frac{cost(verify_k)}{value(shipment)}}_{normalized verification cost}
>     \Bigg),
>     <!-- label: eq:traceability_Q -->
> $$
> 
> where $N_{fraud}$ is the number of batches with known origin fraud (from ground-truth audits), $\alpha_{actual}$ is the realized false-positive rate, and $\beta_{actual}$ is the realized false-negative rate. The three components penalize false alarms, missed fraud, and verification overhead respectively.

> **Definition:** [Traceability Regime Coverage 溯源范围覆盖]
> <!-- label: def:traceability_N -->
> The novelty (regime coverage) score quantifies the diversity of supply chain configurations evaluated:
> 
> $$
>     N(\chain) = \sum_{d=1}^{D} \nu_d \cdot \ind{\chain  covers regime dimension  d},
>     <!-- label: eq:traceability_N -->
> $$
> 
> with regime dimensions including:
> 
- $d_1$: Multi-hop origin chains ($K > 5$);
- $d_2$: Cold-chain integrity (冷链完整性) with temperature logging;
- $d_3$: Conflict-zone provenance (冲突地区来源);
- $d_4$: Mixed-origin blending (blended commodities);
- $d_5$: Cross-border regulatory compliance (跨境合规);
- $d_6$: Consumer-side terminal verification (消费者验证).

> The weight $\nu_d$ is inversely proportional to how commonly the regime appears in existing traceability deployments.

> **Definition:** [Cercis{} Traceability Score Cercis溯源评分]
> <!-- label: def:cercis_traceability -->
> 
> $$
>     S(\chain) = Q(\chain) + \eta \cdot N(\chain),
>     <!-- label: eq:cercis_traceability -->
> $$
> 
> where $\eta \geq 0$ governs the quality-novelty tradeoff. $\eta = 0$ ranks purely by operational traceability accuracy; $\eta > 0$ rewards chains that pioneer verification in novel regimes (e.g., the first conflict-mineral traceability deployment in a new region).

[Table omitted — see original .tex]

> **Remark:** [Cercis{} and Supply Chain Selection Cercis与供应链选择]
> <!-- label: rem:cercis_selection -->
> The Cercis{} score provides a formal objective for supply chain configuration. A retailer sourcing from multiple supply chains can rank them by $S(\chain)$, preferring chains with both high accuracy and novel regime coverage. The $\eta$ parameter operationalizes the value of traceability information: $\eta = 0$ for cost-minimizing procurement; $\eta > 0$ when transparency about novel sourcing regions (e.g., post-conflict zones, new fair-trade cooperatives) has intrinsic value for brand reputation and regulatory compliance.

## Experimental Protocol 实验方案
<!-- label: sec:experiment -->

We specify a reproducible evaluation protocol for the SCX{}-audited supply chain traceability framework across three commodity types.

### Datasets and Ground Truth

1. **Coffee supply chain 咖啡供应链 (Colombia/Ethiopia $\to$ EU).** Source data from the International Coffee Organization (ICO) traceability pilots  [cite]. Ground truth: GPS-verified farm polygons via satellite imagery, organic certification records from Ecocert/BCS, pesticide residue test results from importing-country customs laboratories. Chain length: $K = 5$ (farm, cooperative, exporter, importer, roaster). $N = 500$ batches with known-fraud injection (10\% of batches have manipulated origin claims).
2. **Cocoa supply chain 可可供应链 (C\^ote d'Ivoire/Ghana $\to$ EU).** Source data from the World Cocoa Foundation traceability programs  [cite]. Ground truth: farm GPS coordinates verified against EU Deforestation Regulation (EUDR) polygon maps, fair-trade certification records from FLOCERT, child-labor monitoring reports. Chain length: $K = 6$. $N = 300$ batches with 8\% fraudulent injection.
3. **Conflict minerals 冲突矿产 (DRC $\to$ Asia).** Source data from the Responsible Minerals Initiative (RMI) and ITSCI traceability system. Ground truth: mine-of-origin geochemical fingerprinting (XRF, ICP-MS), OECD Due Diligence Guidance compliance reports. Chain length: $K = 4$ (mine, trader, smelter, manufacturer). $N = 200$ batches with 5\% conflict-mineral infiltration.

### Verification Methods per Node

[Table omitted — see original .tex]

### Evaluation Metrics

1. **Origin fraud detection rate 产地欺诈检测率:** $DR = \frac{true positives}{true positives + false negatives}$, measured per batch with injected fraud.
2. **False alarm rate 误报率:** $FAR = \frac{false positives}{false positives + true negatives}$, measured on known-authentic batches.
3. **Discrepancy localization accuracy 差异定位准确率:** For batches where fraud is detected, the fraction where the first detecting node $k^*$ correctly identifies the earliest node in the chain where the fraud occurred.
4. **Hash chain integrity 哈希链完整性:** $HCI = \frac{verifiable hash chains}{total batches}$, measuring the fraction of batches for which the consumer can successfully verify $\hashChain_K$ against the blockchain anchor.
5. **Spring{} audit efficiency Spring审计效率:** $SAE = \frac{true frauds found by Spring audit}{Spring audits triggered}$, measuring the precision of Spring{}-triggered investigations.
6. **Cost per verified batch 每批次验证成本:** Total verification cost (instrument time, reagents, personnel) per batch, normalized by batch value.

### Baselines

1. **Centralized auditor (集中式审计):** A single third-party certifier audits 10\% of nodes per batch.
2. **Blockchain-only (纯区块链):** Immutable ledger records all claims but performs no physical verification (GIGO baseline).
3. **Random spot-check (随机抽检):** Each node independently verifies with per-batch probability $p = 0.1$.
4. **SCX{} multi-node consensus (Ours):** Full multi-node verification with Yajie{} consensus and Spring{} hash-gating.

### Expected Outcomes

1. **Detection rate:** SCX{} multi-node consensus is expected to achieve $DR > 0.95$ for origin deviations $\delta > 2\bar$, compared to $DR \approx 0.10$ for centralized auditing and $DR \approx 0$ for blockchain-only (which performs no physical verification).
2. **Scaling with chain length:** As $K$ increases, the detection rate of SCX{} consensus should *increase* (more verifying nodes), while centralized auditing's detection rate remains constant (fixed $\alpha$).
3. **Spring{} audit precision:** The Spring{} gating function with $\lambda = 0.1$ is expected to achieve $SAE > 0.7$ (most triggered audits correspond to genuine fraud), compared to random audit precision $p_{fraud} = 0.05$--$0.10$.
4. **Cost tradeoff:** Per-batch verification cost is expected to be $3\times$--$5\times$ higher than centralized auditing, but the cost per *detected* fraud is expected to be $10\times$--$20\times$ lower due to the exponentially higher detection rate.

### Chinese/English Terminology Mapping 中英文术语对照

[Table omitted — see original .tex]

## Discussion 讨论
<!-- label: sec:discussion -->

### Relationship to Existing Approaches

**Centralized certification.** Our framework does not replace centralized certifiers; it augments them. A centralized certifier can serve as one of the $M$ verifying nodes, contributing its specialized expertise to the multi-node consensus. The key difference is that the certifier's verdict is weighted alongside other evidence rather than being accepted as authoritative.

**Blockchain traceability.** Our hash chain (Eq. [ref]) is compatible with any blockchain that supports 32-byte state anchoring. The framework addresses the GIGO problem that blockchain-only solutions face: the *content* of the hash chain is verified by physical measurements at honest nodes, not merely recorded immutably. The blockchain provides tamper-evidence for the record; multi-node verification provides truth-evidence for the content.

**IoT and digital twins.** Internet of Things (IoT) sensors (temperature loggers, GPS trackers, weight sensors) can automate the physical measurement $x_k$ at each node, reducing the cost of verification. Digital twin models can augment $\psi$ (the measurement-to-feature mapping) by predicting expected physical properties from the origin claim, enabling discrepancy detection without reference samples.

### Honest Limitations

1. **Cost of per-node verification.** Physical verification at every node requires instrumentation (NIR spectrometers, chemical assay equipment, GPS loggers), which may be prohibitively expensive for smallholder farmers in developing countries. The Cercis{} score's cost component makes this tradeoff explicit: supply chains with high-value goods (specialty coffee, pharmaceuticals, conflict minerals subject to regulatory penalties) can justify higher verification costs.
2. **Collusion resistance bounds.** If adversarial nodes collude and control consecutive positions in the chain (violating Assumption [ref]), they can suppress discrepancies within their segment. The probability of successful collusion is bounded by the adversarial fraction $\alpha_$ (Assumption [ref]), but detecting collusion itself requires external information beyond the chain's internal verification data.
3. **Fingerprint degradation.** For processed commodities (roasted coffee, refined metals, blended oils), the chemical fingerprint linking product to origin degrades with each processing step. The fingerprinting model (Assumption [ref]) must be commodity-specific and processing-stage-specific; a universal fingerprinting model does not exist.
4. **Consumer verification asymmetry.** While the framework assumes consumer-side verification (Assumption [ref]), in practice most consumers lack the equipment or expertise to verify a hash chain or interpret spectral data. The QR-code-to-blockchain bridge reduces this to a computational verification (checking that the displayed hash matches the blockchain anchor), but the consumer still trusts that the displayed data corresponds to the physical product.
5. **Privacy-traceability tension 隐私与溯源的矛盾.** Full traceability requires revealing the identity and location of every node in the chain, which may conflict with commercial confidentiality (supplier relationships, pricing) and personal privacy (smallholder farmer identities). Zero-knowledge proofs can verify hash-chain consistency without revealing node identities, but constructing efficient ZK-proofs for spectral and chemical verification data remains an open research problem.

### Extensions to DAG Supply Chains DAG供应链的扩展

For supply chains that are not linear (e.g., multiple farms feeding one cooperative, or one smelter sourcing from multiple mines), the DAG formulation (Definition [ref]) applies. The key modification is that node $k$ receives claims from multiple upstream nodes $c_{k-1}^{(1)}, ..., c_{k-1}^{(s)}$ and must verify each independently, producing a consensus claim $\tilde{c}_k$ that reconciles the inputs. The Yajie{} consensus mechanism (weighted averaging with correlation-adjusted weights) provides a natural framework for this reconciliation. The hash chain becomes a Merkle tree where each node's hash commits to a vector of upstream hashes.

## Conclusion 结论

We have formalized supply chain traceability as a multi-node verification problem under the SCX{} audit framework. By treating every supply chain node as a potential auditor of upstream claims, we obtain formal guarantees that false origin claims are detected with probability exponentially approaching 1 as the number of honest verifying nodes increases. The unidentifiability theorem (Theorem [ref]) establishes that rigorous forensic attribution requires explicit assumption declaration, and the Spring{} hash-gating mechanism (Theorem [ref]) provides a cryptographic bridge between physical verification and blockchain-anchored immutable records.

The framework is not a panacea. Per-node verification costs, fingerprint degradation in processed goods, collusion resistance bounds, and the privacy-traceability tension are genuine limitations that require commodity-specific engineering solutions. However, the mathematical structure reveals what is *possible*: when $M$ independently-verifying honest nodes examine a supply chain claim, the probability of undetected fraud is not $1 - \alpha$ (the single-auditor case) but $\exp(-\Omega(M))$. This exponential separation is the fundamental value proposition of multi-node traceability.

\begin{thebibliography}{99}

\bibitem{SCX2025}
SCX.
\newblock The SCX Audit Framework: Multi-Expert Quality Certification.
\newblock Technical Report, 2025.

\bibitem{jena2012organic}
P.~R. Jena, B.~B. Chichaibelu, T.~Stellmacher, and U.~Grote.
\newblock The impact of coffee certification on small-scale producers' livelihoods: a case study from the Jimma Zone, Ethiopia.
\newblock {\em Agricultural Economics}, 43(4):429--440, 2012.

\bibitem{fairtrade2023}
Fairtrade International.
\newblock Annual Report 2022--2023.
\newblock Fairtrade International, Bonn, 2023.

\bibitem{tian2016agri}
F.~Tian.
\newblock An agri-food supply chain traceability system for China based on RFID and blockchain technology.
\newblock In {\em 13th International Conference on Service Systems and Service Management (ICSSSM)}, 2016.

\bibitem{tse2020blockchain}
D.~Tse, B.~Zhang, Y.~Yang, C.~Cheng, and H.~Mu.
\newblock Blockchain application in food supply information security.
\newblock In {\em IEEE International Conference on Industrial Engineering and Engineering Management}, 2020.

\bibitem{lamport1982byzantine}
L.~Lamport, R.~Shostak, and M.~Pease.
\newblock The Byzantine Generals Problem.
\newblock {\em ACM Transactions on Programming Languages and Systems}, 4(3):382--401, 1982.

\bibitem{ico2023traceability}
International Coffee Organization.
\newblock Coffee Traceability Pilot: Technical Report.
\newblock ICO, London, 2023.

\bibitem{wcf2022traceability}
World Cocoa Foundation.
\newblock Cocoa Traceability: From Farm to First Purchase Point.
\newblock WCF, Washington DC, 2022.

\bibitem{lee1997bullwhip}
H.~L. Lee, V.~Padmanabhan, and S.~Whang.
\newblock Information distortion in a supply chain: The bullwhip effect.
\newblock {\em Management Science}, 43(4):546--558, 1997.

\bibitem{chen2000quantifying}
F.~Chen, Z.~Drezner, J.~K. Ryan, and D.~Simchi-Levi.
\newblock Quantifying the bullwhip effect in a simple supply chain: The impact of forecasting, lead times, and information.
\newblock {\em Management Science}, 46(3):436--443, 2000.

\bibitem{nakamoto2008bitcoin}
S.~Nakamoto.
\newblock Bitcoin: A Peer-to-Peer Electronic Cash System.
\newblock 2008.

\bibitem{wood2014ethereum}
G.~Wood.
\newblock Ethereum: A secure decentralised generalised transaction ledger.
\newblock {\em Ethereum Project Yellow Paper}, 2014.

\bibitem{christidis2016blockchains}
K.~Christidis and M.~Devetsikiotis.
\newblock Blockchains and smart contracts for the Internet of Things.
\newblock {\em IEEE Access}, 4:2292--2303, 2016.

\bibitem{kshetri2018blockchain}
N.~Kshetri.
\newblock Blockchain's roles in meeting key supply chain management objectives.
\newblock {\em International Journal of Information Management}, 39:80--89, 2018.

\bibitem{saberi2019blockchain}
S.~Saberi, M.~Kouhizadeh, J.~Sarkis, and L.~Shen.
\newblock Blockchain technology and its relationships to sustainable supply chain management.
\newblock {\em International Journal of Production Research}, 57(7):2117--2135, 2019.

\end{thebibliography}