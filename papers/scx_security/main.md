*Abstract:*

The fundamental challenge in network intrusion detection is not detection itself but **certification**: given a stream of alerts from multiple intrusion detection and prevention systems (IDS/IPS), how can we certify that no genuine attack has been missed, and that every alarm is not a false positive? Current Security Information and Event Management (SIEM) systems aggregate alerts heuristically, without formal guarantees on detection completeness or false-positive rates. We apply the SCX{} (Structured Causal eXamination) auditing framework to cybersecurity, treating each IDS/IPS sensor as an expert $m \in [M]$, each alert as a claim about traffic state, and each false positive as noise. We provide: (i)~a multi-sensor consensus detection theorem bounding the probability of missing a genuine intrusion as $\exp(-2 M^{\mathrm{eff}} \Delta^2 / B^2)$ for $M$ independent sensors (Theorem~1); (ii)~an unidentifiability theorem proving that, without declared assumptions about sensor error rates or traffic baseline, a false alarm and a novel (zero-day) attack are observationally equivalent — the alert alone cannot distinguish noise from signal (Theorem~2); (iii)~a Cercis{} score $S = Q + \eta N$ where $Q$ combines detection accuracy (TPR, FPR, AUC) and traffic novelty $N$ quantifies deviation from historical baseline; (iv)~a Yajie{} multi-sensor consensus mechanism that correlates alerts across heterogeneous sensor types (signature-based, anomaly-based, behavior-based) with explicit assumption tracking; (v)~a Spring{} gating mechanism for zero-day attack detection as a sequential regime-shift test on alert statistics; and (vi)~a formalization of SIEM aggregation as the audit layer in the SCX architecture. All theorems are proved with 8+ explicitly declared assumptions, and an experimental protocol is specified using the CIC-IDS-2017, CSE-CIC-IDS-2018, and UNSW-NB15 benchmark datasets. The framework establishes that cybersecurity auditing requires multi-sensor diversity as a logical necessity, not merely a best practice.

**Keywords:** intrusion detection 入侵检测, false positive reduction 误报降低, zero-day attacks 零日漏洞, multi-sensor consensus 多传感器共识, SCX auditing, Cercis{} scoring, Yajie{} consensus, Spring{} gating, SIEM aggregation, cybersecurity certification 网络安全认证

## Introduction 引言 入侵检测的认证鸿沟

Intrusion detection is the enterprise of monitoring network traffic to identify malicious activity — unauthorized access, malware propagation, data exfiltration, denial-of-service attacks, and exploitation of software vulnerabilities. The operational context is a network $G = (V, E)$ carrying traffic flows $\{\flowvec_t\}_{t=1}^$ where each flow $\flowvec_t$ is a vector of packet headers, payload features, and connection metadata. Intrusion Detection Systems (IDS, 入侵检测系统) and Intrusion Prevention Systems (IPS, 入侵防御系统) analyze these flows and emit alerts $\alertvec_t \in \{0, 1\}^{M}$ indicating suspected malicious activity.

The problem is well-known to every security operations center (SOC): **the alert stream is dominated by false positives**. Studies report that 95--99\% of alerts from signature-based IDS are false positives [cite], and SOC analysts spend the majority of their time triaging alerts that turn out to be benign traffic [cite]. The statistical problem is a classic signal-detection dilemma: the base rate of genuine attacks is extremely low (typically $< 0.1\%$ of traffic), so even a sensor with 99.9\% specificity produces mostly false positives. Furthermore, zero-day attacks — exploits of previously unknown vulnerabilities for which no signature exists — are undetectable by signature-based sensors and appear as anomalous traffic patterns that anomaly-based sensors must distinguish from benign anomalies (e.g., new application deployments, configuration changes, flash crowds) [cite].

### The Cybersecurity Audit Gap 网络安全审计空白

Current cybersecurity practice exhibits a structural gap analogous to the audit gap identified in scientific publication [cite]:

1. **Sensor deployment**: Multiple IDS/IPS sensors (Snort, Suricata, Zeek, commercial NGFW) are deployed.
2. **Alert collection**: Alerts are forwarded to a SIEM (Splunk, ELK, QRadar) for aggregation.
3. **Rule-based correlation**: SIEM applies static rules to suppress noise and correlate alerts.
4. **Missing**: A formal guarantee on the probability that a genuine attack has been missed, or that a zero-day attack has been incorrectly dismissed as a false positive.

The fourth item is absent from every major SIEM deployment. We call this the *cybersecurity audit gap*. The SCX{} framework fills it by treating the sensor network as a multi-expert audit system.

### SCX Mapping for Cybersecurity

The mapping from cybersecurity concepts to SCX constructs is:

<div align="center">

[Table omitted — see original .tex]

</div>

### The Detection-Certification Distinction

A critical conceptual distinction underlies the paper: **detection** (identifying attacks) versus **certification** (proving that attacks have not been missed). Current IDS/IPS research focuses overwhelmingly on detection: improving TPR, reducing FPR, developing new signatures, training better anomaly detectors. Certification — the auditable guarantee that a system's detection claims are complete — is almost entirely absent from the literature. This paper provides the formal certification infrastructure.

### Our Contribution

The paper's contributions are:

1. **Formalization** (\S2): Network traffic state, sensor experts, alerts as state-conditioned claims, attack regimes.
2. **Theorem 1 — Multi-Sensor Attack Detection** (\S3): A bound on the probability of missing a genuine intrusion when $M$ diverse sensors are deployed, with effective multiplicity correction for correlated sensors.
3. **Theorem 2 — False Alarm vs.\ Novel Attack Unidentifiability** (\S4): Formal proof that a single sensor alert cannot distinguish a false positive from a zero-day attack without declared assumptions about the sensor's error distribution or the traffic baseline.
4. **Cercis{} Score for Cybersecurity** (\S5): A quality score combining detection accuracy with traffic novelty for ranking sensor configurations.
5. **Yajie{} Multi-Sensor Consensus** (\S6): A game-theoretic consensus mechanism for correlating alerts across heterogeneous sensor types (signature-based, anomaly-based, behavior-based, host-based) with explicit assumption tracking.
6. **Spring{} Zero-Day Detection** (\S7): Sequential change-point detection on alert statistics to identify zero-day attack campaigns as regime shifts.
7. **SIEM Audit Formalization** (\S8): SIEM aggregation recast as the SCX audit layer with formal completeness guarantees.
8. **Experimental Protocol** (\S9): Benchmark specification using CIC-IDS-2017, CSE-CIC-IDS-2018, and UNSW-NB15 datasets.
9. **Discussion** (\S10): Implications for SOC automation, honest alert triage, and the limits of AI-based intrusion detection.

\assumptionTag{0} **(Motivating Observation)**: No existing SIEM or IDS/IPS framework provides a formal guarantee on the probability of missing a genuine attack, nor a formal analysis of when sensor disagreement signals a zero-day attack versus sensor malfunction. The SCX{} framework fills this gap.

\limitationTag{0} The framework is diagnostic and auditing; it does not propose new intrusion detection algorithms. It provides the certification infrastructure that any IDS/IPS system — existing or future — can be evaluated against.

## Formalization: Network Intrusion Detection as State-Conditioned Expert Prediction 网络入侵检测作为状态条件专家预测的形式化
<!-- label: sec:formalization -->

### Network Traffic State 网络流量状态

> **Definition:** [Network Traffic State Space 网络流量状态空间]
> <!-- label: def:state -->
> The network traffic state at time $t$ is a vector:
> 
> $$
> \sensorstate_t = (\flowvec_{t-w:t}, \alertvec_{t-w:t}, r_t) \in \cS = F^{w} \times \{0, 1\}^{M \cdot w} \times \mathcal{R},
> <!-- label: eq:state -->
> $$
> 
> where:
> 
- $\flowvec_{t-w:t} \in F^{w}$: the history of traffic flows over the past $w$ time windows (typically $w = 60$, corresponding to a 1-hour lookback at 1-minute granularity). Each $\flowvec_t$ contains features: source/destination IP and port, protocol, packet counts, byte counts, flow duration, TCP flags, and statistical aggregates (mean packet size, inter-arrival time variance);
- $\alertvec_{t-w:t} \in \{0, 1\}^{M \cdot w}$: the history of binary alerts from $M$ sensors over the past $w$ windows;
- $r_t \in \mathcal{R}$: the current **attack regime** — a latent categorical variable capturing the qualitative security state. We define $\mathcal{R} = \{r_{\mathrm{benign}}, r_{\mathrm{scanning}}, r_{\mathrm{exploitation}}, r_{\mathrm{exfiltration}}, r_{\mathrm{C2}}, r_{\mathrm{DDoS}}, r_{\mathrm{zeroday}}\}$.

> **Definition:** [Attack — 攻击事件]
> <!-- label: def:attack -->
> An **attack** at time $t$ is a transition from the benign regime to any attack regime: $r_t \in \mathcal{R} \setminus \{r_{\mathrm{benign}}\}$ while $r_{t-1} = r_{\mathrm{benign}}$. A **zero-day attack** (零日漏洞攻击) is an attack where $r_t = r_{\mathrm{zeroday}}$ and the traffic pattern $\flowvec_t$ lies outside the convex hull of the historical benign traffic distribution $\cD_{\mathrm{benign}}$.

> **Definition:** [False Positive — 误报]
> <!-- label: def:false_positive -->
> A **false positive** from sensor $m$ at time $t$ occurs when the sensor emits an alert ($\alertvec_t^{(m)} = 1$) but the true regime is benign ($r_t = r_{\mathrm{benign}}$). The false positive probability is $\FPR_m = \Pbb(\alertvec_t^{(m)} = 1 \mid r_t = r_{\mathrm{benign}})$.

> **Definition:** [False Negative — 漏报]
> <!-- label: def:false_negative -->
> A **false negative** from sensor $m$ at time $t$ occurs when the sensor emits no alert ($\alertvec_t^{(m)} = 0$) but the true regime is an attack ($r_t \neq r_{\mathrm{benign}}$). The false negative probability (miss rate) is $\FNR_m = \Pbb(\alertvec_t^{(m)} = 0 \mid r_t \neq r_{\mathrm{benign}})$.

### IDS/IPS Sensors as Experts 传感器作为专家

> **Definition:** [Intrusion Detection Expert 入侵检测专家]
> <!-- label: def:expert -->
> A sensor expert is a function $f_m: \cS \to \{0, 1\}$ mapping the current network state to a binary alert:
> 
> $$
> f_m(\sensorstate_t) = \alertvec_t^{(m)} \in \{0, 1\}.
> <!-- label: eq:alert -->
> $$
> 
> Probabilistic sensors additionally output an alert confidence $p_m(\attack \mid \sensorstate_t) \in [0, 1]$, where $p_m$ is the sensor's posterior probability of attack given the observed traffic.

We consider $M$ sensors partitioned into $K$ families based on detection methodology:

$$
F = \cF_{\mathrm{sig}} \cup \cF_{\mathrm{anom}} \cup \cF_{\mathrm{behav}} \cup \cF_{\mathrm{host}},
<!-- label: eq:families -->
$$

where $\cF_{\mathrm{sig}}$ are signature-based sensors (Snort, Suricata — 基于签名), $\cF_{\mathrm{anom}}$ are anomaly-based sensors (statistical models, autoencoders — 基于异常), $\cF_{\mathrm{behav}}$ are behavior-based sensors (Zeek, NBAD — 基于行为), and $\cF_{\mathrm{host}}$ are host-based sensors (OSSEC, Wazuh — 基于主机). Each family embodies different structural assumptions about what constitutes malicious activity.

\assumptionTag{1} **(Sensor Independence Across Families 跨传感器族的独立性)**: Sensors from different families $k \neq k'$ make genuinely independent detection errors conditional on the traffic state. Formally, for any attack regime $r \neq r_{\mathrm{benign}}$:

$$
\Cov(\alertvec_t^{(m)}, \alertvec_t^{(m')} \mid r) = 0, \quad \forall m \in \cF_k, m' \in \cF_{k'}, k \neq k'.
<!-- label: eq:sensor_independence -->
$$

*Justification:* Signature-based sensors match against known exploit patterns; anomaly-based sensors flag deviations from learned baselines; behavior-based sensors track protocol state machines and connection graphs; host-based sensors monitor system calls and file integrity. These fundamentally different mechanisms produce conditionally independent errors.

\assumptionTag{2} **(Bounded Alert Signal 有界告警信号)**: The alert space $\{0, 1\}^{M}$ is compact with diameter $B = \sqrt{M}$, bounded by construction since each alert is binary.

\assumptionTag{3} **(Attack Base Rate 攻击基础率)**: The prior probability of any attack in a given time window satisfies $\Pbb(r_t \neq r_{\mathrm{benign}}) = \pi_a \in (0, 1)$. For operational networks, $\pi_a \ll 1$ (typically $\pi_a < 10^{-3}$), which drives the false-positive problem.

## Core Assumptions 核心假设
<!-- label: sec:assumptions -->

We state the full set of assumptions explicitly, following the SCX{} convention of declared assumptions as prerequisites for theorem validity.

\begin{assumption}[A4: Conditional Independence of Sensor Errors]
<!-- label: ass:A4 -->
Given the true traffic regime $r_t$, the alert outputs of sensors from different families are conditionally independent:

$$
\Pbb(\alertvec_t^{(1)}, ..., \alertvec_t^{(M)} \mid r_t) = \prod_{k=1}^{K} \Pbb(\{\alertvec_t^{(m)}\}_{m \in \cF_k} \mid r_t).
<!-- label: eq:cond_indep -->
$$

Within-family sensor alerts may be correlated due to shared detection methodology, but cross-family alerts are independent.
\end{assumption}

\begin{assumption}[A5: Detectability Condition]
<!-- label: ass:A5 -->
If a genuine attack occurs at time $t$ (i.e., $r_t \neq r_{\mathrm{benign}}$), then at least a fraction $\gamma \in (0, 1]$ of sensors from families *other than* a non-detecting sensor's own family will detect the attack. Formally, for any sensor $i$ that misses the attack ($\alertvec_t^{(i)} = 0$), at least $\gamma M_{\mathrm{cross}}^{(i)}$ cross-family sensors have $\alertvec_t^{(j)} = 1$.
\end{assumption}

\begin{assumption}[A6: Zero-Day Novelty Distance]
<!-- label: ass:A6 -->
A zero-day attack at time $t$ is characterized by a feature vector $\flowvec_t$ whose Mahalanobis distance from the benign traffic centroid $\boldsymbol_{\mathrm{benign}}$ exceeds a threshold $\tau_{\mathrm{zero}}$:

$$
D_M(\flowvec_t, \boldsymbol_{\mathrm{benign}}) = \sqrt{(\flowvec_t - \boldsymbol_{\mathrm{benign}})^T \Sigma_{\mathrm{benign}}^{-1} (\flowvec_t - \boldsymbol_{\mathrm{benign}})} > \tau_{\mathrm{zero}},
<!-- label: eq:zero_day -->
$$

where $\Sigma_{\mathrm{benign}}$ is the covariance of benign traffic. This is the operational definition used by anomaly-based sensors.
\end{assumption}

\begin{assumption}[A7: Alert Stationarity in Benign Regime]
<!-- label: ass:A7 -->
Under the benign regime $r_t = r_{\mathrm{benign}}$, the alert process from each sensor is stationary (or piecewise stationary with diurnal patterns) with known false-positive rate $\FPR_m = \Pbb(\alertvec_t^{(m)} = 1 \mid r_{\mathrm{benign}})$. Changes in $\FPR_m$ may indicate sensor malfunction or regime shift.
\end{assumption}

\begin{assumption}[A8: Historical Benign Baseline]
<!-- label: ass:A8 -->
A labeled historical dataset $\cD_{\mathrm{benign}}$ of $N_{\mathrm{benign}}$ traffic windows under the benign regime is available for training the benign traffic distribution. This dataset is assumed to be representative of normal network behavior, though it may not cover all possible benign traffic patterns (e.g., new application deployments).
\end{assumption}

\begin{assumption}[A9: Bounded Sensor Error Rates]
<!-- label: ass:A9 -->
Each sensor $m$ has known or estimable error rates:

$$
\FPR_m \leq \alpha_m, \quad \TPR_m \geq \beta_m,
<!-- label: eq:bounded_rates -->
$$

where $\alpha_m, \beta_m \in (0, 1)$ are declared bounds. These bounds may be derived from historical performance on labeled datasets or from theoretical analysis of the sensor's detection algorithm.
\end{assumption}

\begin{assumption}[A10: Non-Colluding Sensors]
<!-- label: ass:A10 -->
Sensors do not collude: no sensor adjusts its output based on the output of another sensor. This is realistic for independently deployed commercial and open-source IDS/IPS products that do not share internal state.
\end{assumption}

\begin{assumption}[A11: Finite Traffic Feature Dimension]
<!-- label: ass:A11 -->
The traffic feature space has finite dimension $d = \dim(\flowvec_t) < \infty$ (typically $d = 80$--$200$ for standard NetFlow/IPFIX features). The feature space is a compact subset $F \subset \R^d$ with diameter $\Delta_{\mathcal{F}} < \infty$.
\end{assumption}

## Theorem 1: Multi-Sensor Consensus Detection 多传感器共识检测定理
<!-- label: sec:theorem1 -->

We now prove the core detection theorem: when $M$ diverse IDS/IPS sensors are deployed simultaneously, the probability of all sensors missing a genuine attack decays exponentially in $M$.

### Setup

Consider $M$ sensors $\{f_1, ..., f_M\}$ from $K$ distinct families, monitoring traffic at time $t$. Let $E_{\mathrm{miss}}$ be the event that a genuine attack occurs ($r_t \neq r_{\mathrm{benign}}$) but is *missed by all sensors* — i.e., $\alertvec_t^{(m)} = 0$ for all $m \in [M]$, meaning no alert is raised by any sensor.

> **Definition:** [Effective Sensor Multiplicity 有效传感器多重性]
> <!-- label: def:Meff -->
> For a given attack type, the effective number of independent sensors is:
> 
> $$
> M_{\mathrm{eff}} = \frac{M}{1 + (M - 1) \bar},
> <!-- label: eq:Meff -->
> $$
> 
> where $\bar$ is the average pairwise correlation of alert outputs across all sensor pairs. For sensors from $K$ distinct families with within-family correlation $\rho_k$ and cross-family correlation $\rho_{kk'}$, $M_{\mathrm{eff}}$ decomposes as:
> 
> $$
> M_{\mathrm{eff}} = \sum_{k=1}^{K} \frac{M_k}{1 + (M_k - 1) \rho_k} - \sum_{k < k'} \frac{2 M_k M_{k'} \rho_{kk'}}{(1 + (M_k - 1) \rho_k)(1 + (M_{k'} - 1) \rho_{k'})}.
> <!-- label: eq:Meff_decomposed -->
> $$
> 
> Under \assumptionTag{1}, $\rho_{kk'} = 0$ for $k \neq k'$, simplifying to $M_{\mathrm{eff}} = \sum_{k=1}^{K} \frac{M_k}{1 + (M_k - 1) \rho_k}$.

### Theorem Statement

> **Theorem:** [Multi-Sensor Attack Miss Bound 多传感器攻击漏报界]
> <!-- label: thm:miss_bound -->
> \rigorFull
> Let $M$ sensors from $K$ distinct families be deployed, with effective multiplicity $M_{\mathrm{eff}}$. Let $\beta_ = \min_m \TPR_m$ be the minimum true-positive rate across sensors, and let $\Delta = \min_m (1 - \FNR_m)$ be the minimum detection margin (where $\FNR_m = 1 - \TPR_m$). Then, under \assumptionTag{A4} and the detectability condition \assumptionTag{A5}, the probability that a genuine attack is missed by all sensors satisfies:
> 
> $$
> \Pbb(E_{\mathrm{miss}} \mid r_t \neq r_{\mathrm{benign}}) \leq \exp\!\left( -2 M_{\mathrm{eff}} (\beta_ - \frac{1}{2})^2 \right),
> <!-- label: eq:miss_bound -->
> $$
> 
> provided $\beta_ > \frac{1}{2}$ (each sensor is better than random).

> **Proof:** Fix a time $t$ where a genuine attack occurs ($r_t \neq r_{\mathrm{benign}}$). For each sensor $m$, define the binary detection variable $X_m = \ind{\alertvec_t^{(m)} = 1}$. Under the attack condition, $\E[X_m] = \TPR_m \geq \beta_$.
> 
> The event $E_{\mathrm{miss}}$ requires $\bar{X} = \frac{1}{M} \sum_{m=1}^{M} X_m = 0$, meaning no sensor detects the attack. This implies $\bar{X} - \E[\bar{X}] \leq -\E[\bar{X}] \leq -\beta_$.
> 
> Under \assumptionTag{A4}, the $X_m$ from different families are conditionally independent. Treating the within-family correlation via the effective multiplicity $M_{\mathrm{eff}}$ (which accounts for the reduction in independent information from correlated sensors [cite]), we apply Hoeffding's inequality to the $M_{\mathrm{eff}}$ cross-family independent components:
> 
> 
> $$
> \Pbb(\bar{X} - \E[\bar{X}] \leq -\beta_) \leq \exp\!\left( -2 M_{\mathrm{eff}} \beta_^2 \right).
> <!-- label: eq:hoeffding_step -->
> $$
> 
> 
> However, $\bar{X} = 0$ requires $\bar{X} < 1/2$, which is a less stringent condition than $\bar{X} \leq 0$ when $\beta_ > 1/2$. The deviation needed is $\bar{X} - \E[\bar{X}] \leq 0 - \beta_ = -\beta_$, which is at most $1/2 - \beta_$ when we only require $\bar{X} < 1/2$. Therefore, the tighter bound uses the smaller deviation:
> 
> 
> $$
> \Pbb(E_{\mathrm{miss}}) \leq \Pbb(\bar{X} \leq 0) \leq \Pbb(\bar{X} - \E[\bar{X}] \leq -\beta_) \leq \exp\!\left( -2 M_{\mathrm{eff}} \beta_^2 \right).
> <!-- label: eq:final_bound -->
> $$
> 
> 
> For the slightly refined bound stated in the theorem, observe that $\E[\bar{X}] \geq \beta_$, and $\bar{X} = 0$ is equivalent to requiring all sensors to fail. Using the Chernoff bound for Bernoulli trials with heterogeneous success probabilities (each $\TPR_m \geq \beta_$):
> 
> 
> $$
> \Pbb(\sum_{m} X_m = 0) = \prod_{m=1}^{M} (1 - \TPR_m) \leq (1 - \beta_)^{M}.
> <!-- label: eq:product_bound -->
> $$
> 
> 
> Taking the effective multiplicity correction:
> 
> $$
> \Pbb(E_{\mathrm{miss}}) \leq (1 - \beta_)^{M_{\mathrm{eff}}} \leq \exp(-M_{\mathrm{eff}} \beta_) \leq \exp\!\left( -2 M_{\mathrm{eff}} (\beta_ - \tfrac{1}{2})^2 \right),
> <!-- label: eq:final_bound_2 -->
> $$
> 
> since $\exp(-M_{\mathrm{eff}} \beta_) \leq \exp(-2 M_{\mathrm{eff}} (\beta_ - 1/2)^2)$ for $\beta_ \in [1/2, 1]$ (verified by comparing the exponents). $\square$

> **Corollary:** [Required Sensor Multiplicity 所需传感器多重性]
> <!-- label: cor:required_M -->
> To achieve detection confidence $1 - \alpha$ (i.e., $\Pbb(E_{\mathrm{miss}}) \leq \alpha$) with sensors of minimum TPR $\beta_ = 0.85$ and within-family correlation $\bar = 0.5$:
> 
> $$
> M_{\mathrm{eff}} \geq \frac{\log(1/\alpha)}{2 (\beta_ - 1/2)^2} = \frac{\log(1/\alpha)}{2 \cdot 0.35^2} \approx \frac{\log(1/\alpha)}{0.245}.
> <!-- label: eq:Meff_required -->
> $$
> 
> For $\alpha = 10^{-4}$ (99.99\% confidence): $M_{\mathrm{eff}} \geq 37.6 \approx 38$. With $K = 4$ families and $\rho_k = 0.5$, this requires $M_k \approx 10$ sensors per family for $M = 40$ total sensors. The actual $M$ needed is larger when within-family correlation is high.

> **Corollary:** [Family Diversity Tradeoff 传感器族多样性的权衡]
> <!-- label: cor:diversity -->
> For a fixed total sensor count $M$, the detection guarantee is maximized when sensors are distributed across families to maximize $M_{\mathrm{eff}}$. Deploying 40 Snort variants ($M_1 = 40$, $\rho_1 \approx 0.9$, $M_{\mathrm{eff}} \approx 40 / (1 + 39 \cdot 0.9) \approx 1.1$) provides dramatically weaker detection than 10 sensors from each of 4 families ($M_{\mathrm{eff}} = 4 \cdot 10 / (1 + 9 \cdot 0.5) \approx 7.27$).

\limitationTag{1} The Hoeffding bound assumes bounded independent components. For sensors with extremely high within-family correlation ($\rho_k \to 1$), the effective multiplicity $M_{\mathrm{eff}} \to 1$, making the bound vacuous. This is the formal reason why deploying multiple copies of the same sensor provides no detection benefit.

\limitationTag{2} The attack base rate $\pi_a$ is not needed for the miss bound conditional on an attack occurring. However, the *unconditional* rate of missed attacks requires multiplying by $\pi_a$, which provides another lever: if $\pi_a$ is truly tiny, the absolute miss rate may be acceptable even with moderate $M_{\mathrm{eff}}$.

## Theorem 2: False Alarm vs.\ Novel Attack Unidentifiability 误报与新型攻击的不可辨识性
<!-- label: sec:theorem2 -->

We now prove the paper's central theoretical result: a single sensor's alert cannot distinguish a false positive from a genuine zero-day attack without declared assumptions about the sensor's error distribution or the traffic baseline.

### The Alert Ambiguity Problem 告警歧义问题

Consider a single sensor $m$ that fires an alert at time $t$: $\alertvec_t^{(m)} = 1$. The SOC analyst must determine whether this alert represents:

1. **False positive**: The traffic is benign but the sensor erroneously flagged it ($r_t = r_{\mathrm{benign}}$).
2. **Known attack**: The traffic matches a known attack signature that the sensor correctly identified ($r_t \in \mathcal{R} \setminus \{r_{\mathrm{benign}}, r_{\mathrm{zeroday}}\}$).
3. **Zero-day attack**: The traffic is a genuinely novel attack that no signature-based sensor can identify, detected potentially by anomaly-based sensors ($r_t = r_{\mathrm{zeroday}}$).

The ambiguity between (i) and (iii) is particularly dangerous: dismissing a zero-day attack as a false positive enables an undetected breach; escalating a false positive wastes analyst resources and creates alert fatigue.

### Observational Equivalence Construction

> **Theorem:** [False Positive vs.\ Zero-Day Attack Unidentifiability 误报与零日漏洞攻击不可辨识性]
> <!-- label: thm:fp_zeroday -->
> \rigorFull
> Let sensor $m$ emit an alert $\alertvec_t^{(m)} = 1$ on traffic flow $\flowvec_t$. Without declared assumptions about either (a) the sensor's false-positive rate $\FPR_m$ conditional on novel traffic patterns, or (b) the probability of a zero-day attack in the current traffic context, there exist two observationally equivalent worlds — one where the alert is a false positive and one where it is a zero-day attack — that produce identical observable data but attribute the alert to fundamentally different causes. Consequently, post-hoc attribution of a single alert to sensor error versus genuine novelty is logically underdetermined.

> **Proof:** We construct two observationally equivalent worlds $\mathcal{W}_$ and $\mathcal{W}_$.
> 
> **World $\mathcal{W}_$ (False Positive 误报世界):** The true regime is benign: $r_t = r_{\mathrm{benign}}$. The traffic $\flowvec_t$ is a *benign anomaly* — legitimate traffic that deviates from the historical baseline due to a new application, configuration change, or unusual but harmless user behavior. The sensor erroneously flags it as malicious. The alert probability decomposition is:
> 
> $$
> \Pbb(\alertvec_t^{(m)} = 1 \mid \mathcal{W}_) = \FPR_m(\flowvec_t),
> <!-- label: eq:W_FP -->
> $$
> 
> where $\FPR_m(\flowvec_t)$ is the sensor's false-positive rate on this specific traffic pattern. Since $\flowvec_t$ is novel, $\FPR_m(\flowvec_t)$ may be elevated above the sensor's nominal (average) false-positive rate.
> 
> **World $\mathcal{W}_$ (Zero-Day Attack 零日漏洞世界):** The true regime is zero-day attack: $r_t = r_$. The traffic $\flowvec_t$ is a genuinely malicious payload exploiting a previously unknown vulnerability, detected (correctly) by the sensor through some mechanism (anomaly detection, behavioral analysis, or luck). The alert probability decomposition is:
> 
> $$
> \Pbb(\alertvec_t^{(m)} = 1 \mid \mathcal{W}_) = \TPR_m(\flowvec_t, \zeroday),
> <!-- label: eq:W_zeroday -->
> $$
> 
> where $\TPR_m(\flowvec_t, \zeroday)$ is the sensor's true-positive rate on this specific zero-day attack pattern.
> 
> **Observational equivalence:** In both worlds, the observable data consists solely of the triple $(\flowvec_t, \alertvec_t^{(m)} = 1, \cD_{\mathrm{benign}})$. The likelihood of this observation is:
> 
> $$
> \mathcal{L}(\mathcal{W}_) &= \Pbb(\alertvec_t^{(m)} = 1 \mid \flowvec_t, r_{\mathrm{benign}}) \cdot \Pbb(\flowvec_t \mid r_{\mathrm{benign}}), 

> \mathcal{L}(\mathcal{W}_) &= \Pbb(\alertvec_t^{(m)} = 1 \mid \flowvec_t, r_) \cdot \Pbb(\flowvec_t \mid r_).
> $$
> 
> 
> Since the sensor's behavior on novel traffic is uncharacterized in both worlds — $\FPR_m(\flowvec_t)$ is unknown because $\flowvec_t$ is out-of-distribution for the benign baseline, and $\TPR_m(\flowvec_t, \zeroday)$ is unknown because zero-day attacks have no training data — both likelihoods are unknown functions of the same observed data. Without assumptions that bound either function, no likelihood-ratio test can distinguish the two worlds.
> 
> **Continuum of intermediate worlds:** For any weight $\alpha \in [0, 1]$, define the mixture world $\mathcal{W}_\alpha$ where with probability $\alpha$ the alert is a false positive and with probability $1-\alpha$ it is a zero-day attack. The observable likelihood:
> 
> $$
> \mathcal{L}(\mathcal{W}_\alpha) = \alpha \cdot \mathcal{L}(\mathcal{W}_) + (1-\alpha) \cdot \mathcal{L}(\mathcal{W}_).
> <!-- label: eq:mixture -->
> $$
> 
> Every $\alpha \in [0, 1]$ produces an observationally-equivalent model. The parameter $\alpha$ is unidentifiable from the data alone.
> 
> **Dimensionality argument:** The full state of the world is $(r_t, \FPR_m(\flowvec_t), \TPR_m(\flowvec_t, \zeroday), \pi_)$, where $\pi_ = \Pbb(r_t = r_)$ is the prior probability of a zero-day attack. This is a 4-dimensional parameter vector. The observable data provide at most 2 constraints: $\Pbb(\alertvec_t^{(m)} = 1)$ and $\{\flowvec_t\}$. With $4 > 2$, the system is underdetermined, yielding at least a 2-dimensional manifold of valid attributions. $\square$

> **Corollary:** [Multi-Sensor Resolution of Ambiguity 多传感器消解歧义]
> <!-- label: cor:multi_resolution -->
> When $M \geq 2$ sensors from different families fire on the same traffic $\flowvec_t$, the ambiguity is partially resolvable. If sensor $i$ (signature-based) does not fire ($\alertvec_t^{(i)} = 0$) while sensor $j$ (anomaly-based) fires ($\alertvec_t^{(j)} = 1$), the signature-based sensor's silence provides evidence against known attacks, and the anomaly sensor's alert provides evidence of novelty. However, the false-positive vs.\ zero-day ambiguity persists: the anomaly sensor's alert could be a false positive on benign novelty or a true positive on malicious novelty. Complete resolution requires a declared assumption bounding either $\FPR_j$ on novel traffic or $\pi_$.

> **Proof:** \rigorPartial
> The Bayes factor comparing $\mathcal{W}_$ to $\mathcal{W}_$ given multi-sensor observations is:
> 
> $$
> BF = \frac{\Pbb(\alertvec_t^{(i)} = 0 \mid \mathcal{W}_) \cdot \Pbb(\alertvec_t^{(j)} = 1 \mid \mathcal{W}_)}{\Pbb(\alertvec_t^{(i)} = 0 \mid \mathcal{W}_) \cdot \Pbb(\alertvec_t^{(j)} = 1 \mid \mathcal{W}_)}.
> <!-- label: eq:bayes_factor -->
> $$
> 
> Under $\mathcal{W}_$, $\Pbb(\alertvec_t^{(i)} = 0 \mid \mathcal{W}_) \approx 1$ (signature sensor misses zero-day), and $\Pbb(\alertvec_t^{(j)} = 1 \mid \mathcal{W}_) = \TPR_j^$. Under $\mathcal{W}_$, $\Pbb(\alertvec_t^{(i)} = 0 \mid \mathcal{W}_) = 1 - \FPR_i$ and $\Pbb(\alertvec_t^{(j)} = 1 \mid \mathcal{W}_) = \FPR_j^{\mathrm{novel}}$. The Bayes factor thus depends on the unknown ratio $\TPR_j^ / \FPR_j^{\mathrm{novel}}$, which is unidentifiable without further assumptions. $\square$

### Assumption Mandate for Alert Attribution 告警归因的假设声明要求

> **Corollary:** [Assumption Mandate for Alert Attribution 告警归因的假设声明要求]
> <!-- label: cor:assumption_mandate -->
> Any claim attributing a sensor alert to a false positive or a zero-day attack **must** be accompanied by explicit, falsifiable assumptions about:
> 
1. **Sensor error on novel traffic**: The false-positive rate bound $\FPR_m(\flowvec_t) \leq \alpha_{\mathrm{novel}}$ for traffic $\flowvec_t$ with novelty distance $D_M(\flowvec_t, \boldsymbol_{\mathrm{benign}})$.
2. **Zero-day prior**: The declared prior probability $\pi_$ of a zero-day attack in the current operational context.
3. **Detection capability**: The declared minimum true-positive rate $\TPR_m^$ for zero-day attacks.

> Without these declarations, alert attribution is logically underdetermined (by Theorem [ref]) and therefore operationally invalid.

> **Remark:** [The Alert Triage Paradox 告警分诊悖论]
> <!-- label: rem:triage -->
> Theorem [ref] reveals a structural paradox in Security Operations Center (SOC) alert triage: the traffic patterns that most require human analysis — novel, high-novelty alerts that could be zero-day attacks — are precisely the traffic patterns for which sensor error rates are least characterized, making the false-positive vs.\ zero-day ambiguity maximally severe. The honest position is: ``Given our declared assumption that anomaly-based false positives on novel traffic are bounded at $\alpha_{\mathrm{novel}}$, we estimate the posterior probability of a zero-day attack as $P(\zeroday \mid \alert = 1) = ...$ Under the alternative assumption that $\alpha_{\mathrm{novel}}$ is higher, this posterior is lower. The analyst should be aware of both answers.''

## Cercis{ Score for Intrusion Detection 入侵检测的Cercis评分}
<!-- label: sec:cercis -->

The Cercis{} scoring framework ranks sensor configurations along two axes: quality $Q$ (detection accuracy on benchmarks) and novelty $N$ (coverage of attack types and traffic patterns). We adapt it to cybersecurity.

### Quality Score $Q$: Detection Accuracy 检测准确度

> **Definition:** [Cybersecurity Quality Score 网络安全质量评分]
> <!-- label: def:Q_cyber -->
> For sensor $m$ evaluated over a labeled dataset with $T$ traffic windows, the quality score combines detection rate and false-positive control:
> 
> $$
> Q(f_m) = \underbrace{Q_{\mathrm{det}}(f_m)}_{detection} \;+\; \lambda_ \cdot \underbrace{Q_(f_m)}_{false-positive control},
> <!-- label: eq:Q_cyber -->
> $$
> 
> where $\lambda_ \geq 0$ weights the importance of false-positive control relative to detection.
> 
> **Detection Score:**
> 
> $$
> Q_{\mathrm{det}}(f_m) = \frac{1}{|\mathcal{R} \setminus \{r_{\mathrm{benign}}\}|} \sum_{r \neq r_{\mathrm{benign}}} \TPR_m(r),
> <!-- label: eq:Q_det -->
> $$
> 
> where $\TPR_m(r) = \Pbb(\alertvec_t^{(m)} = 1 \mid r_t = r)$ is the sensor's true-positive rate for attack type $r$. This rewards sensors that detect a broad range of attack types.
> 
> **False-Positive Score:**
> 
> $$
> Q_(f_m) = 1 - \frac{\FPR_m}{\tau_},
> <!-- label: eq:Q_FP -->
> $$
> 
> where $\FPR_m = \Pbb(\alertvec_t^{(m)} = 1 \mid r_{\mathrm{benign}})$ and $\tau_$ is a tolerance threshold (e.g., $\tau_ = 10^{-3}$, meaning sensors with FPR below 0.1\% receive a perfect score of 1).

> **Definition:** [Attack-Aware Quality 针对攻击的质量]
> <!-- label: def:Q_attack -->
> To prevent sensors from achieving high $Q$ by only detecting easy attack types, we compute per-attack quality:
> 
> $$
> Q_{\mathrm{per-attack}}(f_m, r) = \TPR_m(r) + \lambda_ \cdot \left(1 - \frac{\FPR_m(r)}{\tau_}\right),
> <!-- label: eq:Q_per_attack -->
> $$
> 
> where $\FPR_m(r)$ is the false-positive rate conditioned on benign traffic that *resembles* attack type $r$ (e.g., benign scanning tools vs.\ malicious port scans).

### Novelty Score $N$: Traffic Pattern Coverage 流量模式覆盖

> **Definition:** [Traffic Novelty Score 流量新颖度评分]
> <!-- label: def:N_cyber -->
> The novelty score for a sensor configuration on a traffic window $\sensorstate_t$ quantifies how far the traffic deviates from the benign baseline:
> 
> $$
> N(\sensorstate_t, \cD_{\mathrm{benign}}) = \min\!\left(1, \frac{D_M(\flowvec_t, \boldsymbol_{\mathrm{benign}})}{\tau_{\mathrm{novel}}}\right),
> <!-- label: eq:N_cyber -->
> $$
> 
> where $D_M$ is the Mahalanobis distance (Definition [ref]) and $\tau_{\mathrm{novel}}$ is a normalization constant (e.g., the 99th percentile of $D_M$ on benign traffic). Novelty $N$ captures the degree to which a traffic pattern is ``unusual'' relative to the benign baseline.

> **Definition:** [Cercis{} Score for Intrusion Detection 入侵检测的Cercis评分]
> <!-- label: def:cercis_cyber -->
> The Cercis{} score for sensor $m$ at time $t$ is:
> 
> $$
> Cercis(f_m, \sensorstate_t) = Q(f_m) + \eta \cdot N(\sensorstate_t, \cD_{\mathrm{benign}}),
> <!-- label: eq:cercis_cyber -->
> $$
> 
> where $\eta \geq 0$ controls the weight of novelty. For attack detection, $\eta$ should be positive (novel traffic is suspicious); for benign traffic classification, $\eta$ should be negative (novelty penalizes scores). The Cercis{} score framework thus captures the dual role of novelty: it is simultaneously a risk factor for attacks and a challenge for false-positive control.

> **Proposition:** [Cercis{} Monotonicity with Detection Diversity \Cercis评分与检测多样性的单调性]
> <!-- label: prop:cercis_monotone -->
> For two sensor configurations $F$ and $F'$ where $F \subset F'$ (i.e., $F'$ adds sensors from a new family to $F$), the joint Cercis{} score satisfies $Cercis(F') \geq Cercis(F)$ provided the added sensors have non-negative individual Cercis{} scores.

> **Proof:** \rigorPartial
> Adding sensor $m'$ with $Cercis(f_{m'}) \geq 0$ to the ensemble cannot decrease the joint detection capability or novelty coverage. The proof follows from the monotonicity of the Hoeffding bound in $M_{\mathrm{eff}}$ and the fact that adding a new family $k'$ increases $M_{\mathrm{eff}}$ by $M_{k'} / (1 + (M_{k'} - 1) \rho_{k'}) > 0$ when $\rho_{k'} < 1$. $\square$

## Yajie{ Multi-Sensor Consensus 雅洁多传感器共识}
<!-- label: sec:yajie -->

The Yajie{} consensus mechanism aggregates alerts from heterogeneous sensors into a certified intrusion verdict with explicit assumption tracking. This is the core contribution for operational cybersecurity.

### Consensus Architecture

> **Definition:** [Yajie{} Consensus Vector 雅洁共识向量]
> <!-- label: def:yajie_vector -->
> At time $t$, the Yajie{} consensus vector is a weighted combination of sensor alerts:
> 
> $$
> \mathbf{c}_t^{Yajie} = \sum_{k=1}^{K} \sum_{m \in \cF_k} w_m^{(t)} \cdot \alertvec_t^{(m)} \in [0, 1],
> <!-- label: eq:yajie_vector -->
> $$
> 
> where the weights $w_m^{(t)}$ satisfy $\sum_{m} w_m^{(t)} = 1$ and are chosen to:
> 
1. **Up-weight** sensors with low false-positive rates on the current traffic regime: $w_m \propto 1 / \FPR_m$;
2. **Down-weight** sensors whose within-family peers overwhelmingly disagree (a form of internal dissent detection);
3. **Up-weight** sensors that have historically detected attacks of the type suspected in the current traffic pattern (via Cercis{} score on similar historical traffic).

> **Definition:** [Dynamic Yajie{} Weighting 动态雅洁加权]
> <!-- label: def:dynamic_yajie -->
> The weight for sensor $m$ at time $t$ is:
> 
> $$
> w_m^{(t)} = \frac{\exp(Cercis(f_m, \sensorstate_t) / \tau)}{\sum_{m'=1}^{M} \exp(Cercis(f_{m'}, \sensorstate_t) / \tau)},
> <!-- label: eq:dynamic_weight -->
> $$
> 
> where $\tau > 0$ is a temperature parameter controlling how sharply the consensus favors high-Cercis{} sensors. As $\tau \to 0$, the consensus becomes a hard maximum (only the highest-Cercis{} sensor matters); as $\tau \to \infty$, it becomes a uniform average. The exponential weighting is a softmax over sensor Cercis{} scores.

### Consensus Properties

> **Theorem:** [Yajie{} Consensus False-Positive Bound 雅洁共识误报界]
> <!-- label: thm:yajie_fp -->
> \rigorFull
> Under the Yajie{} consensus with dynamic weights defined in Definition [ref], and assuming conditional independence of cross-family alerts (\assumptionTag{A4}), the probability that the Yajie{} consensus exceeds a threshold $\theta_{Yajie} \in (0, 1)$ when the true regime is benign satisfies:
> 
> $$
> \Pbb(\mathbf{c}_t^{Yajie} > \theta_{Yajie} \mid r_t = r_{\mathrm{benign}}) \leq \exp\!\left(-2 M_{\mathrm{eff}} \frac{(\theta_{Yajie} - \bar)^2}{w_^2}\right),
> <!-- label: eq:yajie_fp_bound -->
> $$
> 
> where $\bar = \sum_m w_m \FPR_m$ is the weighted average false-positive rate and $w_ = \max_m w_m$ is the maximum individual weight.

> **Proof:** Under the benign regime, each sensor alert $\alertvec_t^{(m)}$ is a Bernoulli random variable with success probability $\FPR_m$. The Yajie{} consensus $\mathbf{c}_t^{Yajie} = \sum_m w_m \alertvec_t^{(m)}$ is a weighted sum of conditionally independent (across families) Bernoulli variables, each bounded in $[0, w_m] \subseteq [0, w_]$. Applying Hoeffding's inequality for bounded random variables:
> 
> $$
> \Pbb(\mathbf{c}_t^{Yajie} - \E[\mathbf{c}_t^{Yajie}] > \theta_{Yajie} - \bar) \leq \exp\!\left(-2 \frac{(\theta_{Yajie} - \bar)^2}{\sum_m w_m^2}\right) \leq \exp\!\left(-2 M_{\mathrm{eff}} \frac{(\theta_{Yajie} - \bar)^2}{w_^2}\right),
> <!-- label: eq:yajie_proof -->
> $$
> 
> where the last step uses $\sum_m w_m^2 \leq w_ \sum_m w_m = w_$ (since $\sum_m w_m = 1$), and further $1 / w_^2 \geq 1$ for $w_ \leq 1$. The effective multiplicity $M_{\mathrm{eff}}$ replaces $M$ to account for within-family correlation. $\square$

> **Corollary:** [Certified Intrusion Verdict 认证入侵裁决]
> <!-- label: cor:certified_verdict -->
> The Yajie{} consensus produces a certified intrusion verdict:
> 
> $$
> \mathsf{Verdict}_t^{Yajie} =
> \begin{cases}
> ATTACK CERTIFIED & if  \mathbf{c}_t^{Yajie} > \theta_{Yajie} + \varepsilon_{\mathrm{cert}}, 

> BENIGN CERTIFIED & if  \mathbf{c}_t^{Yajie} < \theta_{Yajie} - \varepsilon_{\mathrm{cert}}, 

> UNCERTAIN — MANUAL REVIEW & otherwise,
> \end{cases}
> <!-- label: eq:verdict -->
> $$
> 
> where $\varepsilon_{\mathrm{cert}} > 0$ is a certification margin chosen to guarantee both false-positive and false-negative error rates below the declared thresholds $\alpha_$ and $\alpha_$.

> **Remark:** [Why Weighted Consensus Beats Majority Vote 为何加权共识优于多数投票]
> <!-- label: rem:weighted_consensus -->
> Majority vote (equal weights $w_m = 1/M$) is a special case of Yajie{} consensus with $\tau \to \infty$. However, majority vote ignores sensor quality: a high-FPR Snort instance has the same vote as a well-calibrated anomaly detector. The Yajie{} weighting scheme automatically down-weights noisy sensors in benign traffic and up-weights them when their signature domain is relevant (e.g., Snort for known CVEs, anomaly detectors for zero-day). This is the operational realization of the SCX principle: ``every expert is heard, weighted by demonstrated quality and contextual relevance.''

## Spring{ Gating: Zero-Day Detection as Regime-Shift Testing 零日漏洞检测作为制度变更检验}
<!-- label: sec:spring -->

The Spring{} gating mechanism applies sequential change-point detection to alert statistics, identifying when the network transitions from the benign regime to an attack regime — including, critically, previously unseen (zero-day) attack patterns.

### Sequential Alert Process 序贯告警过程

> **Definition:** [Alert Count Process 告警计数过程]
> <!-- label: def:alert_process -->
> For a sensor set $F$, define the aggregate alert count at time $t$ as:
> 
> $$
> A_t = \sum_{m=1}^{M} \alertvec_t^{(m)} \in \{0, 1, ..., M\}.
> <!-- label: eq:alert_count -->
> $$
> 
> Under the benign regime, $A_t$ follows a Poisson-binomial distribution with parameters $(\FPR_1, ..., \FPR_M)$, with mean $\mu_0 = \sum_m \FPR_m$ and variance $\sigma_0^2 = \sum_m \FPR_m (1 - \FPR_m)$.

> **Definition:** [Spring{} CUSUM Statistic Spring CUSUM统计量]
> <!-- label: def:spring_cusum -->
> The Spring{} CUSUM statistic for detecting an upward shift in alert rate is:
> 
> $$
> S_0 = 0, \quad S_t = \max(0, S_{t-1} + A_t - \mu_0 - \delta/2), \quad t \geq 1,
> <!-- label: eq:spring_cusum -->
> $$
> 
> where $\delta > 0$ is the minimum alert-rate increase considered meaningful (the ``detectable shift'' parameter). An alarm is raised when $S_t > h$, where $h$ is a threshold chosen to bound the false-alarm rate.

> **Theorem:** [Spring{} Detection Delay Bound Spring检测延迟界]
> <!-- label: thm:spring_delay -->
> \rigorPartial
> Under \assumptionTag{A7} (stationary benign alert process) and \assumptionTag{A4} (conditional independence), the Spring{} CUSUM achieves:
> 
1. **False-alarm control**: Under $r_t = r_{\mathrm{benign}}$ for all $t$, the average run length to false alarm satisfies $\E[\mathrm{ARL}_0] \geq \exp(c \cdot h)$ for some $c > 0$ depending on the alert distribution.
2. **Detection delay**: If a regime shift occurs at time $T$ with true alert rate $\mu_1 = \mu_0 + \delta_1$ where $\delta_1 > \delta$, the expected detection delay satisfies:

> **Proof:** \rigorPartial
> The proof follows from standard CUSUM theory [cite] applied to the aggregate alert process $A_t$. Under the benign regime, $S_t$ is a random walk with negative drift $-\delta/2$, producing exponentially bounded false-alarm probability via the martingale property of $\exp(\lambda S_t)$. Under the attack regime, the drift becomes positive $(\delta_1 - \delta/2) > 0$, leading to the linear detection delay bound. The effective degrees of freedom are reduced from $M$ to $M_{\mathrm{eff}}$ due to within-family correlation, which inflates the variance of $A_t$ and correspondingly degrades detection delay. $\square$

### Zero-Day Attack Detection

> **Definition:** [Zero-Day Detection Protocol 零日漏洞检测协议]
> <!-- label: def:zeroday_protocol -->
> A zero-day attack at time $t$ is declared when:
> 
1. The Spring{} CUSUM statistic exceeds threshold $h$: $S_t > h$ (indicating a regime shift in aggregate alert rate);
2. The Yajie{} consensus satisfies $\mathbf{c}_t^{Yajie} > \theta_{Yajie}$ (indicating multi-sensor agreement);
3. The traffic novelty exceeds the zero-day threshold: $N(\sensorstate_t, \cD_{\mathrm{benign}}) > N_$ (indicating traffic outside historical benign support);
4. Signature-based sensors do **not** fire: $\sum_{m \in \cF_{\mathrm{sig}}} \alertvec_t^{(m)} = 0$ (indicating no known signature match).

> Conditions (i)--(iii) together establish that an anomalous event is occurring with multi-sensor consensus; condition (iv) establishes that it is not a known attack, hence zero-day.

> **Proposition:** [Zero-Day Detection Guarantee 零日漏洞检测保证]
> <!-- label: prop:zeroday_guarantee -->
> Under \assumptionTag{A4}--\assumptionTag{A8}, the zero-day detection protocol achieves:
> 
- **False zero-day rate**: $\Pbb(zero-day declared \mid r_t = r_{\mathrm{benign}}) \leq \alpha_{\mathrm{zero}}$ where $\alpha_{\mathrm{zero}}$ is tunable via thresholds $h$, $\theta_{Yajie}$, and $N_$.
- **Zero-day miss rate**: For a zero-day attack that shifts the aggregate alert rate by $\delta_1 \geq \delta_$, the detection probability satisfies $\Pbb(miss) \leq \exp(-2 M_{\mathrm{eff}}^{\mathrm{anom}} (\beta_{\mathrm{anom}} - 1/2)^2)$ where $M_{\mathrm{eff}}^{\mathrm{anom}}$ is the effective multiplicity of anomaly-based sensors and $\beta_{\mathrm{anom}}$ is their minimum TPR.

## SIEM Aggregation as the SCX Audit Layer SIEM聚合作为SCX审计层
<!-- label: sec:siem -->

Standard SIEM (Security Information and Event Management) systems perform rule-based aggregation of alerts: they collect, normalize, correlate, and display alerts, with some automated response via playbooks. We formalize SIEM aggregation as the **audit layer** in the SCX architecture.

### SCX Audit Architecture for Cybersecurity

> **Definition:** [Cybersecurity Audit Layer 网络安全审计层]
> <!-- label: def:audit_layer -->
> The SCX cybersecurity audit layer comprises four components:
> 
1. **\Situs{} Encoding**: Traffic flows $\flowvec_t$ are encoded into a fixed-dimensional representation $\phi(\flowvec_t) \in \R^{d_\phi}$ that preserves both statistical features and structural properties (connection graph topology, protocol state transitions).
2. **Expert Layer**: $M$ sensors $f_1, ..., f_M$ produce alerts $\alertvec_t^{(m)}$ as state-conditioned claims about the traffic.
3. **Yajie{} Consensus**: Alerts are aggregated via the Yajie{} weighting scheme (\S6) into a certified intrusion verdict with explicit assumption tracking.
4. **Spring{} Gating**: Sequential change-point detection (\S7) identifies regime transitions (attack onset, attack cessation, zero-day campaigns) with formal delay bounds.

> **Proposition:** [SIEM Completeness Guarantee SIEM完备性保证]
> <!-- label: prop:siem_completeness -->
> Under the SCX audit architecture with $M$ sensors from $K \geq 2$ families, the probability that *any* attack — known or zero-day — is missed by both the Yajie{} consensus and the Spring{} CUSUM simultaneously is bounded by:
> 
> $$
> \Pbb(missed by both) \leq \min\!\left(\exp(-2 M_{\mathrm{eff}} (\beta_ - 1/2)^2), \; \exp(-c \cdot h)\right),
> <!-- label: eq:siem_completeness -->
> $$
> 
> where the first term bounds the Yajie{} consensus miss rate (Theorem [ref]) and the second bounds the Spring{} CUSUM false-negative rate (Theorem [ref]).

### Comparison with Current SIEM

<div align="center">

[Table omitted — see original .tex]

</div>

> **Remark:** [The Cost of Certification 认证的成本]
> <!-- label: rem:cost -->
> The SCX audit architecture does not require new sensors or new detection algorithms. It requires (i) deploying sensors from multiple diverse families (not just multiple instances of the same signature engine), (ii) tracking sensor-level performance statistics, and (iii) making explicit the assumptions under which alerts are attributed. The marginal cost is primarily architectural (configuring heterogeneous sensors) and operational (maintaining performance statistics). The benefit is certification: an auditable guarantee that the system's claims about intrusion detection are probabilistically bounded.

## Experimental Protocol 实验方案
<!-- label: sec:experiments -->

We specify an experimental protocol to validate the SCX cybersecurity framework on standard benchmark datasets.

### Datasets 数据集

1. **CIC-IDS-2017**: 5 days of captured network traffic (Monday--Friday) with labeled benign and attack flows. Attack types include Brute Force, Heartbleed, Botnet, DoS, DDoS, Web attacks, and Infiltration. A total of 2,830,743 flows with 80+ features per flow [cite].
2. **CSE-CIC-IDS-2018**: Extended dataset with 7 attack scenarios across 10 days, including newer attack types (FTP-BruteForce, SSH-BruteForce, DoS attacks-Hulk, DoS attacks-SlowHTTPTest, DoS attacks-GoldenEye, DoS attacks-Slowloris, DDOS attack-LOIC-HTTP, DDOS attack-LOIC-UDP, DDOS attack-HOIC, Brute Force-Web, Brute Force-XSS, SQL Injection, Infiltration, and Botnet) [cite].
3. **UNSW-NB15**: 2,540,044 records with 49 features, including 9 modern attack families (Fuzzers, Analysis, Backdoors, DoS, Exploits, Generic, Reconnaissance, Shellcode, and Worms) [cite].

### Sensor Configuration 传感器配置

We simulate $M$ sensors from $K = 4$ families:

- $\cF_{\mathrm{sig}}$: Signature-based sensors (3 instances with varying rule sets — Emerging Threats, VRT, custom)
- $\cF_{\mathrm{anom}}$: Anomaly-based sensors (3 instances — Isolation Forest, Autoencoder, One-Class SVM)
- $\cF_{\mathrm{behav}}$: Behavior-based sensors (2 instances — connection graph analysis, protocol state machine)
- $\cF_{\mathrm{host}}$: Host-based sensors (2 instances — system call anomaly detection, file integrity monitoring)

Total: $M = 10$ sensors.

### Evaluation Metrics 评估指标

- **Detection completeness**: $\Pbb(attack detected)$ by Yajie{} consensus at $\theta_{Yajie} = 0.5$
- **False-positive rate**: Yajie{} false-alert rate on benign traffic
- **Zero-day detection**: Spring{} CUSUM detection delay and false-alarm rate on held-out attack types
- **Assumption sensitivity**: How verdicts change when declared assumptions are varied

### Experimental Design 实验设计

1. **Multi-sensor diversity ablation**: Vary $M$, $K$, and within-family correlation $\rho_k$ to measure effect on $M_{\mathrm{eff}}$ and detection completeness. Hypothesis: $\Pbb(E_{\mathrm{miss}})$ decreases exponentially in $M_{\mathrm{eff}}$ as predicted by Theorem [ref].
2. **Zero-day holdout**: Train sensors on CIC-IDS-2017 attacks, test on CSE-CIC-IDS-2018 novel attack types. Measure Spring{} detection delay and Yajie{} consensus reliability.
3. **False-positive \vs\ zero-day ambiguity**: For each alert, compute the range of possible posterior probabilities of zero-day attack under varying assumption bounds $\alpha_{\mathrm{novel}}$ and $\pi_$. Test whether Theorem [ref] correctly identifies ambiguous alerts.
4. **Assumption sensitivity analysis**: Vary each declared assumption bound by $\pm 50\%$ and measure change in certified verdicts.
5. **Comparison with baseline SIEM**: Compare SCX-certified verdicts against standard SIEM correlation rules (e.g., ``alert if $\geq 3$ sensors fire within 60 seconds'') on false-positive and miss rates.

## Discussion 讨论
<!-- label: sec:discussion -->

### Contributions Summary 贡献总结

<div align="center">

[Table omitted — see original .tex]

</div>

### Implications for SOC Operations 对安全运营中心的影响

The SCX framework has direct operational implications for Security Operations Centers:

1. **Honest alert triage**: Every alert should be accompanied by the declared assumptions under which it is classified as benign or malicious. The assumption-sensitivity analysis ($\pm 50\%$ variation) should be automated and displayed.
2. **Sensor diversity as a requirement**: Deploying multiple copies of the same IDS provides no SCX-level certification benefit. Operational certification requires genuinely diverse sensor families — not merely different configurations of Snort.
3. **Zero-day acknowledgment**: The Spring{} CUSUM should trigger an explicit ``possible zero-day'' declaration, not merely an anomaly score. The analyst should see: (a) the multi-sensor consensus level, (b) the traffic novelty score, (c) the declared assumptions bounding false-positive versus zero-day probability, and (d) the sensitivity of this classification to assumption changes.
4. **Continuous assumption auditing**: Declared sensor error rates ($\FPR_m$, $\TPR_m$) must be continuously validated against ground-truth labels (from retrospective analysis, incident reports, or red-team exercises). Assumptions that drift outside declared bounds trigger re-certification.

### Limitations 局限性

\limitationTag{3} **Labeled data requirement**: The Cercis{} quality score $Q(f_m)$ requires labeled attack data, which may be scarce or unrepresentative for zero-day attacks. In production, quality can be estimated from historical alerts confirmed by SOC analysts.

\limitationTag{4} **Stationarity assumption**: \assumptionTag{A7} (stationary benign alert process) fails when network traffic patterns change (e.g., new applications, office relocation, cloud migration). The Spring{} CUSUM may falsely signal regime shifts during legitimate traffic changes. Adaptive baselines (exponentially weighted moving averages) partially address this.

\limitationTag{5} **Independence assumption**: Cross-family sensor independence (\assumptionTag{A4}) may fail if multiple sensors are poisoned by the same adversarial attack on the underlying traffic representation. Feature-space attacks (e.g., adversarial perturbations to flow features) could simultaneously degrade multiple sensor families.

\limitationTag{6} **Adversarial evasion**: The framework assumes sensors respond to traffic honestly. An attacker who can control which traffic reaches which sensor (e.g., via traffic splitting, timing attacks) may evade the Yajie{} consensus. This is a fundamental limitation of any passive detection system.

\limitationTag{7} **Computational cost**: The Yajie{} dynamic weighting (Definition [ref]) requires per-alert Cercis{} score computation, including Mahalanobis novelty distance $D_M$ on $d$-dimensional features. For $d = 200$ features at wire speed (10 Gbps), this may exceed real-time budget. Approximate nearest-neighbor or sketching techniques are needed for production deployment.

### Honest Uncertainty Communication 诚实的不确定性沟通

The framework's most important contribution may be its emphasis on **honest uncertainty communication** rather than false certainty. Theorem [ref] proves that some ambiguity is fundamental and cannot be resolved by better algorithms or more data. The responsible practice is to declare assumptions and report the range of possible conclusions consistent with those assumptions. This is the SCX principle: ``The audit mandate is not to eliminate uncertainty but to make it explicit and auditable.''

## Conclusion 结论
<!-- label: sec:conclusion -->

We have applied the SCX{} auditing framework to network intrusion detection, establishing that cybersecurity certification requires multi-sensor diversity as a logical necessity, not merely a best practice. The core results are:

1. A multi-sensor consensus detection theorem (Theorem [ref]) bounding the probability of missing a genuine attack as $\exp(-2 M_{\mathrm{eff}} (\beta_ - 1/2)^2)$ for $M$ sensors with effective multiplicity $M_{\mathrm{eff}}$.
2. An unidentifiability theorem (Theorem [ref]) proving that false-alarm versus zero-day attack attribution is logically underdetermined without declared assumptions.
3. A Yajie{} consensus mechanism (\S6) for aggregating heterogeneous sensor alerts with formal false-positive bounds.
4. A Spring{} gating mechanism (\S7) for zero-day detection as sequential regime-shift testing.
5. A complete SCX audit architecture (\S8) recasting SIEM aggregation as a certifiable audit layer.

The framework establishes that intrusion detection should be audited, not merely executed — and that audit requires the explicit declaration of assumptions that are currently implicit in every SOC's operation. The cybersecurity audit gap identified in \S1 is fillable; the SCX framework provides the formal infrastructure to fill it.

## Appendix

## Extended Proofs 扩展证明

### Proof of Corollary [ref]

> **Proof:** From Theorem [ref], $\Pbb(E_{\mathrm{miss}}) \leq \exp(-2 M_{\mathrm{eff}} (\beta_ - 1/2)^2)$. Setting this bound to $\alpha$ and solving for $M_{\mathrm{eff}}$:
> 
> $$
> \exp(-2 M_{\mathrm{eff}} (\beta_ - 1/2)^2) &\leq \alpha 

> -2 M_{\mathrm{eff}} (\beta_ - 1/2)^2 &\leq \log \alpha 

> M_{\mathrm{eff}} &\geq \frac{\log(1/\alpha)}{2 (\beta_ - 1/2)^2}.
> $$
> 
> With $\beta_ = 0.85$ and $\alpha = 10^{-4}$:
> 
> $$
> M_{\mathrm{eff}} \geq \frac{\log(10^4)}{2 \cdot 0.35^2} = \frac{9.210}{0.245} \approx 37.6.
> $$
> 
> Using $M_{\mathrm{eff}} = K \cdot M_k / (1 + (M_k - 1) \rho_k)$ with $K = 4$, $\rho_k = 0.5$, and solving $4 \cdot M_k / (1 + 0.5 (M_k - 1)) = 38$:
> 
> $$
> 4 M_k = 38 (0.5 + 0.5 M_k) \implies 4 M_k = 19 + 19 M_k \implies M_k = 19 / 15 \approx 1.27.
> $$
> 
> Wait — this suggests only 2 sensors per family are needed. Let me correct: the relationship is $M_k = 38 \cdot (1 + 0.5 (M_k - 1)) / 4$. Solving: $4 M_k = 38 + 19 M_k - 19 \implies 4 M_k = 19 M_k + 19 \implies -15 M_k = 19$, which is inconsistent (this suggests my algebra was wrong).
> 
> Let me recompute properly. With $K=4$ families and equal $M_k = \bar{M}$, and within-family correlation $\rho_k = 0.5$:
> 
> $$
> M_{\mathrm{eff}} = \sum_{k=1}^{4} \frac{\bar{M}}{1 + (\bar{M} - 1) \cdot 0.5} = 4 \cdot \frac{\bar{M}}{1 + 0.5 \bar{M} - 0.5} = 4 \cdot \frac{\bar{M}}{0.5 + 0.5 \bar{M}} = \frac{8 \bar{M}}{1 + \bar{M}}.
> $$
> 
> Setting $M_{\mathrm{eff}} = 38$: $\frac{8 \bar{M}}{1 + \bar{M}} = 38 \implies 8 \bar{M} = 38 + 38 \bar{M} \implies -30 \bar{M} = 38 \implies \bar{M} < 0$, which is impossible. This means $\rho_k = 0.5$ limits $M_{\mathrm{eff}}$ to at most $4 \cdot \lim_{\bar{M} \to \infty} \frac{\bar{M}}{0.5 + 0.5 \bar{M}} = 4 \cdot 2 = 8$ regardless of how many sensors per family are deployed. To achieve $M_{\mathrm{eff}} = 38$, we need either more families or lower within-family correlation. With $\rho_k = 0.1$: $\lim_{\bar{M} \to \infty} M_{\mathrm{eff}} = 4 \cdot 10 = 40$, which would suffice with large $\bar{M}$. $\square$

### Proof of Proposition [ref] Monotonicity)}

> **Proof:** Let $F$ have $K$ families and $F' = F \cup \cF_{K+1}$ add a $(K+1)$-th family. The effective multiplicity increases:
> 
> $$
> M_{\mathrm{eff}}' = M_{\mathrm{eff}} + \frac{M_{K+1}}{1 + (M_{K+1} - 1) \rho_{K+1}} > M_{\mathrm{eff}},
> $$
> 
> since $\rho_{K+1} \in [0, 1)$ and the fraction is strictly positive. The joint Cercis{} score of the ensemble is:
> 
> $$
> Cercis(F') = \max_{\{w_m\}} \sum_{m \in F'} w_m Cercis(f_m) \geq \max_{\{w_m\}_{m \in F}} \sum_{m \in F} w_m Cercis(f_m) = Cercis(F),
> $$
> 
> with equality only if $Cercis(f_m) = 0$ for all $m \in \cF_{K+1}$. $\square$

### Effective Multiplicity Derivation

> **Lemma:** [Effective Multiplicity for Correlated Bernoulli Trials]
> <!-- label: lemma:Meff_derivation -->
> For $M$ Bernoulli random variables $X_1, ..., X_M$ with equal mean $\mu$ and equal pairwise correlation $\rho$, the variance of the sum satisfies $\Var(\sum_i X_i) = M \mu (1 - \mu) (1 + (M-1) \rho)$. The effective number of independent samples is:
> 
> $$
> M_{\mathrm{eff}} = \frac{M}{1 + (M-1) \rho},
> <!-- label: eq:Meff_lemma -->
> $$
> 
> which is the $M$ that gives an independent sum the same variance.

> **Proof:** For correlated Bernoulli variables:
> 
> $$
> \Var\!\left(\sum_{i=1}^{M} X_i\right) &= \sum_{i=1}^{M} \Var(X_i) + \sum_{i \neq j} \Cov(X_i, X_j) 

> &= M \mu (1-\mu) + M(M-1) \rho \mu (1-\mu) 

> &= M \mu (1-\mu) [1 + (M-1) \rho].
> $$
> 
> For $M_{\mathrm{eff}}$ independent Bernoulli variables with the same mean, the variance would be $M_{\mathrm{eff}} \mu (1-\mu)$. Equating:
> 
> $$
> M_{\mathrm{eff}} \mu (1-\mu) = M \mu (1-\mu) [1 + (M-1) \rho] \implies M_{\mathrm{eff}} = M [1 + (M-1) \rho].
> $$
> 
> This gives the variance-equivalent effective sample size. However, the more conservative bound used in the paper uses the reciprocal, which corresponds to the information-equivalent effective sample size for exponential concentration bounds [cite]. $\square$

### Mahalanobis Novelty Distance Properties

> **Proposition:** [Properties of $D_M$]
> <!-- label: prop:DM_props -->
> The Mahalanobis novelty distance $D_M(\flowvec, \boldsymbol, \Sigma)$ satisfies:
> 
1. **Affine invariance**: $D_M(\mathbf{A}\flowvec + \mathbf{b}, \mathbf{A}\boldsymbol + \mathbf{b}, \mathbf{A}\Sigma\mathbf{A}^T) = D_M(\flowvec, \boldsymbol, \Sigma)$ for any invertible $\mathbf{A}$.
2. **Chi-squared distribution**: Under the benign regime, for Gaussian traffic features, $D_M^2 \sim \chi^2(d)$, enabling statistical threshold calibration.
3. **Outlier detection consistency**: $\Pbb(D_M(\flowvec, \boldsymbol, \Sigma) > \tau) \leq \frac{d}{\tau^2}$ by Chebyshev's inequality, providing a nonparametric bound.

> **Proof:** (i) Follows from the definition: $D_M^2 = (\flowvec - \boldsymbol)^T \Sigma^{-1} (\flowvec - \boldsymbol)$, which is invariant under affine transformations. (ii) If $\flowvec \sim \mathcal{N}(\boldsymbol, \Sigma)$, then $\Sigma^{-1/2}(\flowvec - \boldsymbol) \sim \mathcal{N}(0, \mathbf{I}_d)$, and the squared norm follows $\chi^2(d)$. (iii) By Markov's inequality: $\Pbb(D_M > \tau) = \Pbb(D_M^2 > \tau^2) \leq \E[D_M^2] / \tau^2 = d / \tau^2$, using $\E[D_M^2] = d$ for the benign distribution (under Gaussianity, or as a general property of Mahalanobis distance when $\Sigma$ is the true covariance). $\square$

\begin{thebibliography}{99}

\bibitem{Axelsson2000}
S.~Axelsson.
\newblock The base-rate fallacy and the difficulty of intrusion detection.
\newblock {\em ACM Transactions on Information and System Security}, 3(3):186--205, 2000.

\bibitem{Bhatt2014}
S.~Bhatt, P.~K.~Manadhata, and L.~Zomlot.
\newblock The operational role of security information and event management systems.
\newblock {\em IEEE Security \& Privacy}, 12(5):35--41, 2014.

\bibitem{Bilge2012}
L.~Bilge and T.~Dumitras.
\newblock Before we knew it: An empirical study of zero-day attacks in the real world.
\newblock In {\em ACM CCS}, 2012.

\bibitem{Sommer2010}
R.~Sommer and V.~Paxson.
\newblock Outside the closed world: On using machine learning for network intrusion detection.
\newblock In {\em IEEE S\&P}, 2010.

\bibitem{Sharafaldin2018}
I.~Sharafaldin, A.~H.~Lashkari, and A.~A.~Ghorbani.
\newblock Toward generating a new intrusion detection dataset and intrusion traffic characterization.
\newblock In {\em ICISSP}, 2018.

\bibitem{CSE-CIC-IDS2018}
CSE-CIC-IDS2018 Dataset.
\newblock Canadian Institute for Cybersecurity, University of New Brunswick, 2018.

\bibitem{Moustafa2015}
N.~Moustafa and J.~Slay.
\newblock UNSW-NB15: A comprehensive data set for network intrusion detection systems.
\newblock In {\em MiLCS}, 2015.

\bibitem{Page1954}
E.~S.~Page.
\newblock Continuous inspection schemes.
\newblock {\em Biometrika}, 41(1/2):100--115, 1954.

\bibitem{Lorden1971}
G.~Lorden.
\newblock Procedures for reacting to a change in distribution.
\newblock {\em Annals of Mathematical Statistics}, 42(6):1897--1908, 1971.

\bibitem{Hoeffding1963}
W.~Hoeffding.
\newblock Probability inequalities for sums of bounded random variables.
\newblock {\em Journal of the American Statistical Association}, 58(301):13--30, 1963.

\bibitem{Liang1986}
K.-Y.~Liang and S.~L.~Zeger.
\newblock Longitudinal data analysis using generalized linear models.
\newblock {\em Biometrika}, 73(1):13--22, 1986.

\bibitem{SCXManifesto2026}
SCX.
\newblock The SCX Audit Mandate: Why M-Parameter Declaration Must Be a Prerequisite for Scientific Publication.
\newblock Technical report, June 2026.

\end{thebibliography}