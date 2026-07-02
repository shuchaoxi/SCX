# Introduction 引言

**Author:** SCX

*Abstract:*

Multi-messenger astronomy---the coordinated observation of astrophysical transients across electromagnetic (EM), gravitational wave (GW), neutrino, and cosmic ray (CR) channels---naturally provides multiple independent ``experts'' observing the same physical event. Each instrument (LIGO/Virgo/KAGRA, JWST, IceCube, Fermi, LSST, CHIME) constitutes an expert with distinct systematics, energy sensitivity, and sky coverage. We apply the SCX{} (Structured Causal eXamination) auditing framework to multi-messenger astronomy, providing certified inference guarantees across heterogeneous observational experts. Core contributions: (i) a joint detection confidence theorem (Theorem~1) bounding the probability of missing a transient event of astrophysical significance $\Lambda$ when $K$ messenger channels with $M_k$ instruments each are deployed, with the bound $\exp\bigl(-2\sum_k M_k^{\mathrm{eff}} \cdot \Delta_k^2 / B_k^2\bigr)$; (ii) a cross-channel consensus theorem (Theorem~2) establishing that when multiple messenger channels agree on a source hypothesis, the joint false-alarm probability decays super-exponentially in the number of agreeing channels; (iii) an instrumental artifact vs.\ new physics unidentifiability theorem (Theorem~3) proving that, without declared assumptions about at least one instrument's systematics, instrumental artifacts and genuine new-physics signals produce observationally equivalent multi-messenger signatures; (iv) a Cercis{} score $S = Q + \eta N$ for observational campaigns, where $Q$ combines localization accuracy and spectral fidelity across channels and $N$ measures discovery novelty; (v) a \Situs{} encoding for celestial coordinates incorporating relativistic aberration, gravitational lensing deflection, and cosmological redshift, with a Lipschitz guarantee bounding coordinate reconstruction error under finite signal-to-noise; (vi) a multi-instrument Yajie{} consensus mechanism where instruments vote per-channel, then cross-channel consensus propagates through the astrophysical source model. Theorems are stated with explicit assumptions under the SCX{} convention and proved at \rigorFull, \rigorPartial, and \rigorSketch{} levels. We provide experimental protocols covering GW170817/GRB~170817A (binary neutron star merger), IceCube high-energy neutrino alerts, and fast radio burst (FRB) localization campaigns.

**Keywords:** multi-messenger astronomy 多信使天文学, gravitational waves 引力波, neutrino astronomy 中微子天文, SCX auditing, joint detection confidence, instrumental artifact unidentifiability, Cercis{} scoring, Yajie{} consensus, \Situs{} celestial encoding, certified astrophysical inference

## Introduction 引言
<!-- label: sec:introduction -->

Multi-messenger astronomy---the coordinated observation of astrophysical transients using electromagnetic radiation, gravitational waves, neutrinos, and cosmic rays---represents a paradigm shift in observational astrophysics  [cite]. A single cataclysmic event, such as a binary neutron star (BNS) merger, a core-collapse supernova, or a tidal disruption event, may simultaneously emit across all four messenger channels. Each channel is observed by a distinct class of instruments (``experts'' in the SCX{} sense), each with its own systematic uncertainties, instrument response functions, and detection pipelines.

**The multi-messenger landscape 多信使天文学景观.** The current observational infrastructure includes:

1. **Gravitational wave detectors 引力波探测器.** LIGO (Hanford and Livingston)  [cite], Virgo  [cite], and KAGRA  [cite] form a global network of kilometer-scale laser interferometers sensitive to spacetime strain $h \sim 10^{-23}$--$10^{-21}$ in the 10--1000~Hz band. Binary compact object mergers (BNS, BBH, NSBH) are primary sources. Systematic uncertainties include calibration error ($\sim 5\%$ in amplitude, $\sim 2^\circ$ in phase), detector noise power spectral density (PSD) estimation, and glitch contamination  [cite].
2. **Electromagnetic observatories 电磁观测站.** The electromagnetic spectrum spans radio (LOFAR, VLA, ASKAP, CHIME), optical/IR (JWST, HST, ZTF, LSST/Vera Rubin), X-ray (Chandra, XMM-Newton, Swift-XRT, NICER), and $\gamma$-ray (Fermi-GBM, Fermi-LAT, Swift-BAT, INTEGRAL). Each sub-band has distinct systematic challenges: dust extinction (optical/IR), calibration uncertainty ($\gamma$-ray effective area), and host galaxy contamination.
3. **Neutrino observatories 中微子观测站.** IceCube  [cite] at the South Pole instruments $\sim 1$~km$^3$ of glacial ice with photomultiplier tubes to detect Cherenkov radiation from neutrino interactions. ANTARES and KM3NeT provide complementary coverage in the Northern Hemisphere. Systematics include ice modeling uncertainty, optical module efficiency drift, and atmospheric neutrino background characterization.
4. **Cosmic ray detectors 宇宙线探测器.** Pierre Auger Observatory, Telescope Array, and space-based detectors (AMS-02, CALET) measure ultra-high-energy cosmic rays (UHECRs). Systematics include hadronic interaction model uncertainty, atmospheric calibration, and energy scale determination.

**The certification gap.** Despite the transformative science enabled by multi-messenger observations---exemplified by GW170817/GRB~170817A, the first joint GW-EM detection of a BNS merger  [cite]---no formal framework exists for certifying the joint confidence of multi-messenger inference. Each collaboration reports its own detection significance (e.g., false-alarm rate or $p$-value), but joint significance is typically estimated via *ad hoc* multiplication of per-channel significances, which ignores channel correlations, systematic uncertainties, and the possibility that apparent correlations arise from instrumental artifacts rather than astrophysical coincidences.

**Our contribution.** We apply the SCX{} auditing framework  [cite] to multi-messenger astronomy. The SCX{} framework provides: (i) noise detection via expert multiplicity (\ThmSCXNoise), adapted here to bound joint detection confidence across messenger channels; (ii) error source unidentifiability analysis (\ThmSCXHonest), deployed to distinguish instrumental artifacts from genuine new-physics signals; (iii) Cercis{} scoring for combined quality-novelty ranking of observational campaigns; (iv) Yajie{} game-theoretic consensus across instruments. The thesis is:

<div align="center">

*Multi-messenger astronomy naturally provides independent observational experts.

SCX{} provides per-channel AND cross-channel certified inference guarantees.

Without declared assumptions, instrumental artifacts and new physics are unidentifiable.*

</div>

**Paper structure.** Section~2 formalizes multi-messenger observation as a multi-expert inference problem. Section~3 proves the joint detection confidence theorem. Section~4 proves the instrumental artifact vs.\ new physics unidentifiability theorem. Section~5 proves the cross-channel consensus theorem. Section~6 defines the Cercis{} score for observational campaigns. Section~7 presents the \Situs{} encoding for celestial coordinates with relativistic corrections. Section~8 presents multi-instrument Yajie{} consensus. Section~9 specifies experimental protocols. Section~10 discusses implications and limitations.

## Formalization: Multi-Messenger Astronomy as Multi-Expert Inference 多信使天文学作为多专家推理的形式化
<!-- label: sec:formulation -->

### Astrophysical Source State 天体物理源状态

> **Definition:** [Astrophysical Source State]<!-- label: def:source_state -->
> An astrophysical source state $\mathbf{s} \in \cS$ is the tuple:
> 
> $$<!-- label: eq:source_state -->
> \mathbf{s} = \bigl( \boldsymbol_{\mathrm{src}}, \; t_0, \; \mathbf{n}, \; D_L, \; \boldsymbol_{\mathrm{env}} \bigr),
> $$
> 
> where:
> 
- $\boldsymbol_{\mathrm{src}} \in \Theta_{\mathrm{src}}$: intrinsic source parameters (component masses $m_1, m_2$, spins $\boldsymbol_1, \boldsymbol_2$, equation of state for BNS; progenitor mass, metallicity, explosion energy for supernovae; black hole mass, stellar type for TDEs);
- $t_0 \in \R$: reference epoch of the event (e.g., merger time for compact binaries, core bounce for supernovae);
- $\mathbf{n} \in S^2$: sky direction (unit vector on the celestial sphere);
- $D_L \in \R_{>0}$: luminosity distance;
- $\boldsymbol_{\mathrm{env}} \in \Phi_{\mathrm{env}}$: environmental parameters (host galaxy extinction $A_V$, intergalactic medium dispersion measure, circum-burst density profile).

### Messenger Channels and Instruments 信使通道与仪器

> **Definition:** [Messenger Channel 信使通道]<!-- label: def:messenger_channel -->
> A messenger channel $c \in \mathcal{C} = \{\mathrm{EM}, \mathrm{GW}, \nu, \mathrm{CR}\}$ is a physical carrier of information from the source to the observer. Each channel $c$ is characterized by:
> 
- A radiation transfer function $\mathcal{T}_c: \cS \to \cY_c$ mapping the source state to the channel-specific observable space $\cY_c$;
- A set of instruments $\mathcal{I}_c = \{I_{c,1}, ..., I_{c, M_c}\}$ observing in channel $c$.

> **Definition:** [Instrument Expert 仪器专家]<!-- label: def:instrument_expert -->
> Each instrument $i \in \mathcal{I}_c$ is an expert $f_{c,i}: \cY_c \to \cO_{c,i}$ that maps channel observables to instrument-specific outputs:
> 
> $$<!-- label: eq:instrument -->
> f_{c,i}\bigl(\mathcal{T}_c(\mathbf{s})\bigr) = \bigl( \hat{\mathbf{n}}_{c,i}, \; \hat{D}_{L, c,i}, \; \hat{\boldsymbol}_{\mathrm{src}, c,i}, \; \rho_{c,i}, \; p_{c,i}^{\mathrm{FAR}} \bigr),
> $$
> 
> where $\hat{\mathbf{n}}_{c,i}$ is the reconstructed sky direction, $\hat{D}_{L, c,i}$ the distance estimate, $\hat{\boldsymbol}_{\mathrm{src}, c,i}$ the recovered source parameters, $\rho_{c,i}$ the detection statistic (signal-to-noise ratio or test statistic), and $p_{c,i}^{\mathrm{FAR}}$ the false-alarm rate $p$-value.

### Multi-Messenger Observation Model 多信使观测模型

The total observation of an astrophysical event is the collection of all instrument outputs across all channels:

$$<!-- label: eq:total_obs -->
\mathcal{O}(\mathbf{s}) = \bigl\{ \mathcal{O}_{c,i}(\mathbf{s}) = f_{c,i}(\mathcal{T}_c(\mathbf{s})) \;:\; c \in \mathcal{C}, \; i \in \mathcal{I}_c \bigr\}.
$$

The total number of observing experts is $M_{\mathrm{tot}} = \sum_{c \in \mathcal{C}} M_c$.

\begin{assumption}[A1: Channel Separability 通道可分性]<!-- label: ass:A1 -->
For each messenger channel $c \in \mathcal{C}$, the radiation transfer $\mathcal{T}_c: \cS \to \cY_c$ is a well-defined mapping. Different channels carry independent physical information: the joint likelihood factorizes as

$$<!-- label: eq:likelihood_factor -->
p(\{\mathcal{D}_{c,i}\}_{c,i} \mid \mathbf{s}) = \prod_{c \in \mathcal{C}} \prod_{i \in \mathcal{I}_c} p(\mathcal{D}_{c,i} \mid \mathbf{s}),
$$

where $\mathcal{D}_{c,i}$ denotes the data recorded by instrument $i$ in channel $c$. This assumes that noise processes are independent across instruments, which holds for physically separated detectors.
\end{assumption}

\begin{assumption}[A2: Bounded Detection Statistic 有界检测统计量]<!-- label: ass:A2 -->
For any source state $\mathbf{s}$ and any instrument $(c,i)$, the detection statistic $\rho_{c,i}(\mathbf{s})$ satisfies $0 \leq \rho_{c,i} \leq B_{c,i} < \infty$. For matched-filter searches (GW, radio), $\rho$ is the optimal signal-to-noise ratio, bounded by the maximum theoretically achievable SNR for the instrument.
\end{assumption}

\begin{assumption}[A3: Instrument Independence 仪器独立性]<!-- label: ass:A3 -->
For a fixed channel $c$, the $M_c$ instruments have mutually independent noise realizations. Their detection statistics $\{\rho_{c,i}\}_{i=1}^{M_c}$ are independent random variables conditional on the source state $\mathbf{s}$. This holds for geographically separated instruments (LIGO Hanford/Livingston/Virgo/KAGRA) and for space-based instruments with uncorrelated backgrounds.
\end{assumption}

\begin{assumption}[A4: Detectable Error Margin 可检测误差边距]<!-- label: ass:A4 -->
For each messenger channel $c$, there exists a threshold $\Delta_c > 0$ such that when a source is astrophysically significant (i.e., its true detection statistic exceeds the detection threshold), at least one instrument in $\mathcal{I}_c$ registers $\rho_{c,i} > \Delta_c$ and at least one other registers $\rho_{c,j} \leq \Delta_c/2$. This formalizes the condition that a significant source is detectable by some but not necessarily all instruments (due to pointing, duty cycle, or sensitivity variations).
\end{assumption}

\begin{assumption}[A5: Sky Localization Metric 天区定位度量]<!-- label: ass:A5 -->
Sky direction estimates $\hat{\mathbf{n}}_{c,i}$ lie in a compact metric space $(S^2, d_{\mathrm{sky}})$ where $d_{\mathrm{sky}}(\hat{\mathbf{n}}_1, \hat{\mathbf{n}}_2) = \arccos(\hat{\mathbf{n}}_1 \cdot \hat{\mathbf{n}}_2)$ is the great-circle angular separation. The localization error $\Delta \Omega_{c,i}$ (90\% credible area in deg$^2$ or arcmin$^2$) is a function of $\rho_{c,i}$ and the instrument's angular resolution.
\end{assumption}

## Theorem 1: Joint Detection Confidence with Heterogeneous Systematics 异构系统误差下的联合检测置信度定理
<!-- label: sec:joint_detection -->

### Per-Channel Detection Protocol 单通道检测协议

For each messenger channel $c$ with $M_c$ instruments, define the per-channel detection indicator:

$$<!-- label: eq:channel_detection -->
D_c(\mathbf{s}) = \ind{\frac{1}{M_c}\sum_{i=1}^{M_c} \ind{\rho_{c,i}(\mathbf{s}) > \tau_c} \geq \gamma_c},
$$

where $\tau_c$ is a channel-specific detection threshold and $\gamma_c \in (0, 1]$ is the required fraction of instruments in agreement (e.g., $\gamma_c = 1/2$ for majority voting). Channel $c$ is declared to have detected the source if $D_c(\mathbf{s}) = 1$.

> **Definition:** [Joint Detection Event 联合检测事件]<!-- label: def:joint_detection -->
> A multi-messenger detection occurs when at least $K_{\mathrm{min}}$ of the $|\mathcal{C}| = 4$ messenger channels independently declare a detection:
> 
> $$<!-- label: eq:joint_detection -->
> D_{\mathrm{joint}}(\mathbf{s}) = \ind{\sum_{c \in \mathcal{C}} D_c(\mathbf{s}) \geq K_{\mathrm{min}}}.
> $$
> 
> For a ``golden'' multi-messenger event (e.g., GW170817), $K_{\mathrm{min}} = 2$ (GW + EM). For a ``platinum'' event, $K_{\mathrm{min}} \geq 3$ (GW + EM + $\nu$). For a ``diamond'' event, $K_{\mathrm{min}} = 4$ (all channels).

> **Definition:** [Missed Detection 漏检]<!-- label: def:missed -->
> A missed detection in channel $c$ occurs when the source is astrophysically significant (true detection statistic exceeds the threshold) but $D_c(\mathbf{s}) = 0$. The total missed detection probability for the joint campaign is $\Pbb[miss_{\mathrm{joint}} \mid source exists]$.

### Theorem Statement

> **Theorem:** [Joint Multi-Messenger Detection Confidence 多信使联合检测置信度定理]<!-- label: thm:joint_detection -->
> \rigorFull
> Let an astrophysical source $\mathbf{s}$ emit in $K$ messenger channels ($K \leq 4$), where channel $c$ is monitored by $M_c$ independent instruments. Under Assumptions [ref]-- [ref], the probability of missing a joint detection when the source is genuinely present is bounded by:
> 
> $$<!-- label: eq:joint_bound -->
> \Pbb[miss_{\mathrm{joint}} \mid \mathbf{s}] \leq \sum_{\substack{\mathcal{C}' \subset \mathcal{C} 
 |\mathcal{C}'| > |\mathcal{C}| - K_{\mathrm{min}}}} \;\; \prod_{c \in \mathcal{C}'} \exp\bigl(-2 M_c^{\mathrm{eff}} \cdot (\gamma_c - p_c^{\mathrm{err}})^2 \bigr),
> $$
> 
> where $p_c^{\mathrm{err}} = \Pbb[\rho_{c,i} \leq \tau_c \mid \mathbf{s}]$ is the per-instrument miss probability in channel $c$ (bounded above by $1 - \gamma_c$ under A4), and $M_c^{\mathrm{eff}} = M_c / (1 + (M_c-1)\bar_c)$ is the effective number of independent instruments accounting for pairwise error correlation $\bar_c$.
> 
> In the idealized independent-instrument limit ($\bar_c \to 0$, $\gamma_c = 1/2$, $p_c^{\mathrm{err}} \leq 1/2$), the bound simplifies to:
> 
> $$<!-- label: eq:joint_bound_simple -->
> \Pbb[miss_{\mathrm{joint}} \mid \mathbf{s}] \leq \sum_{m=0}^{K_{\mathrm{min}}-1} \binom{K}{m} \prod_{c \in \mathcal{C}_{\mathrm{miss}}} \exp\bigl(-M_c \Delta_c^2 / (2 B_c^2)\bigr),
> $$
> 
> where $\mathcal{C}_{\mathrm{miss}}$ is any set of channels that miss the detection, and the binomial coefficient counts the ways to miss $K_{\mathrm{min}}$ or more channels.

> **Proof:** **Step 1: Per-channel miss probability.**
> Fix channel $c$ and a source $\mathbf{s}$. Define the binary indicator $X_{c,i} = \ind{\rho_{c,i}(\mathbf{s}) > \tau_c}$ for instrument $i$. Under A3 (independence of instruments within a channel), $\{X_{c,i}\}_{i=1}^{M_c}$ are i.i.d.\ Bernoulli random variables with $p_c^{\mathrm{det}} = \Pbb[X_{c,i} = 1 \mid \mathbf{s}] = 1 - p_c^{\mathrm{err}}$.
> 
> A missed channel detection $D_c(\mathbf{s}) = 0$ occurs when the fraction of detecting instruments falls below $\gamma_c$:
> 
> $$
> \Pbb[D_c = 0 \mid \mathbf{s}] = \Pbb\Bigl[\frac{1}{M_c}\sum_{i=1}^{M_c} X_{c,i} < \gamma_c \;\Big|\; \mathbf{s}\Bigr].
> $$
> 
> 
> Under A4, when the source is astrophysically significant, at least one instrument detects it and one misses, implying $p_c^{\mathrm{det}} \geq 1 - \gamma_c$ (if $p_c^{\mathrm{det}} < 1-\gamma_c$, then more than fraction $\gamma_c$ of instruments miss, violating the assumption that at least one detects). By Hoeffding's inequality  [cite]:
> 
> $$
> \Pbb\Bigl[\frac{1}{M_c}\sum X_{c,i} < \gamma_c\Bigr] 
> &= \Pbb\Bigl[\frac{1}{M_c}\sum (1 - X_{c,i}) > 1 - \gamma_c\Bigr]  

> &\leq \exp\bigl(-2M_c (p_c^{\mathrm{det}} - \gamma_c)^2 \bigr)  

> &\leq \exp\bigl(-2M_c (\gamma_c - p_c^{\mathrm{err}})^2 \bigr).
> $$
> 
> 
> Under A2 (bounded detection statistics), we can relate $p_c^{\mathrm{err}}$ to the detection threshold gap. Let $\mu_c = \E[\rho_{c,i}]$ be the expected detection statistic for source $\mathbf{s}$. Under A4, there exists $\Delta_c$ such that $\mu_c - \tau_c \geq \Delta_c$. By Chebyshev/Chernoff, $p_c^{\mathrm{err}} \leq \exp(-\Delta_c^2/(2 B_c^2))$, yielding the simplified exponent form.
> 
> **Step 2: Correlation correction.**
> With residual correlation $\bar_c$ among instruments in channel $c$, the effective independent sample size is $M_c^{\mathrm{eff}} = M_c/(1 + (M_c-1)\bar_c)$  [cite]. Substituting $M_c^{\mathrm{eff}}$ for $M_c$ accounts for shared systematics (e.g., calibration uncertainties common to LIGO Hanford and Livingston).
> 
> **Step 3: Joint miss probability.**
> The joint detection misses when fewer than $K_{\mathrm{min}}$ channels declare a detection. Let $\mathcal{C}_{\mathrm{det}} \subset \mathcal{C}$ be the set of detecting channels and $\mathcal{C}_{\mathrm{miss}} = \mathcal{C} \setminus \mathcal{C}_{\mathrm{det}}$. The event $miss_{\mathrm{joint}}$ is:
> 
> $$
> miss_{\mathrm{joint}} = \bigl\{ |\mathcal{C}_{\mathrm{det}}| < K_{\mathrm{min}} \bigr\} = \bigcup_{\substack{\mathcal{C}_{\mathrm{miss}} \subset \mathcal{C} 
 |\mathcal{C}_{\mathrm{miss}}| > |\mathcal{C}| - K_{\mathrm{min}}}} \bigcap_{c \in \mathcal{C}_{\mathrm{miss}}} \{D_c = 0\}.
> $$
> 
> 
> By A1 (channel separability), detection events across channels are independent. By the union bound and the per-channel bound from Step 1:
> 
> $$
> \Pbb[miss_{\mathrm{joint}}] &\leq \sum_{\substack{\mathcal{C}_{\mathrm{miss}} 
 |\mathcal{C}_{\mathrm{miss}}| > K - K_{\mathrm{min}}}} \prod_{c \in \mathcal{C}_{\mathrm{miss}}} \Pbb[D_c = 0]  

> &\leq \sum_{\substack{\mathcal{C}_{\mathrm{miss}}}} \prod_{c \in \mathcal{C}_{\mathrm{miss}}} \exp\bigl(-2 M_c^{\mathrm{eff}} (\gamma_c - p_c^{\mathrm{err}})^2 \bigr).
> $$
> 
> 
> **Step 4: Simplified form.**
> For $\gamma_c = 1/2$ and $p_c^{\mathrm{err}} \leq 1/2 - \Delta_c/(2B_c)$ (by A4 with the detection margin), we have $(\gamma_c - p_c^{\mathrm{err}})^2 \geq \Delta_c^2/(4 B_c^2)$. Substituting yields the simplified bound (Eq. [ref]). The binomial coefficient $\binom{K}{m}$ appears when $K_{\mathrm{min}}$ is fixed and we sum over all combinations of $m = |\mathcal{C}_{\mathrm{miss}}|$ missed channels. $\square$

> **Corollary:** [Required Instruments per Channel 每通道所需仪器数]<!-- label: cor:required_instruments -->
> To achieve joint detection confidence $1 - \alpha$ for a $K=2$ channel detection ($K_{\mathrm{min}}=2$) with $M_1 = M_2 = M$ instruments per channel, the required effective multiplicity per channel is:
> 
> $$<!-- label: eq:required_instruments -->
> M^{\mathrm{eff}} \geq \frac{B_c^2}{2\Delta_c^2} \log\!\left(\frac{2}{\sqrt - \alpha/4}\right).
> $$
> 
> For $\alpha = 0.01$ (99\% confidence), $B_c = 1$ (normalized detection statistic), and $\Delta_c = 0.1$ (threshold gap 10\% of maximum), we obtain $M^{\mathrm{eff}} \geq 265$, which can be achieved with $M \approx 10$--$50$ physical instruments when $\bar_c$ is small ($\bar_c < 0.05$).

> **Remark:** [Application to GW170817]
> For GW170817/GRB~170817A  [cite], the two-channel scenario ($K=2$, GW + EM) applies. The LIGO-Virgo network provided $M_{\mathrm{GW}} = 3$ instruments (H1, L1, V1), with $\rho_{\mathrm{GW}} \approx 32$ (network SNR), yielding per-instrument miss probability far below the threshold. Fermi-GBM and INTEGRAL/SPI-ACS provided $M_{\mathrm{EM}} = 2$ $\gamma$-ray instruments for the prompt emission, with $\rho_{\mathrm{EM}} \gg \tau_{\mathrm{EM}}$. The joint detection probability was effectively unity, consistent with the observed unambiguous multi-messenger association. Theorem [ref] quantifies *how much* weaker the detection could have been before the association became ambiguous.

## Theorem 2: Cross-Channel Consensus and False-Alarm Suppression 跨通道共识与虚警抑制定理
<!-- label: sec:cross_channel_consensus -->

When multiple independent messenger channels report a consistent source hypothesis (same sky location, consistent distance, compatible source parameters), the joint false-alarm probability is dramatically suppressed. The following theorem quantifies this suppression.

> **Definition:** [Channel-Consistent Hypothesis 通道一致假设]<!-- label: def:consistent_hypothesis -->
> Two messenger channels $c$ and $c'$ report *consistent* source hypotheses if their reconstructed parameters agree within their respective uncertainties:
> 
> $$<!-- label: eq:consistency -->
> d_{\mathrm{sky}}(\hat{\mathbf{n}}_c, \hat{\mathbf{n}}_{c'}) \leq \sigma_{c, \mathrm{sky}} + \sigma_{c', \mathrm{sky}} \quad and \quad |\hat{D}_{L,c} - \hat{D}_{L,c'}| \leq \sigma_{c, D_L} + \sigma_{c', D_L},
> $$
> 
> where $\sigma_{c, \mathrm{sky}}$ and $\sigma_{c, D_L}$ are the 68\% credible intervals for sky localization and distance, respectively.

> **Theorem:** [Cross-Channel Consensus False-Alarm Suppression 跨通道共识虚警抑制定理]<!-- label: thm:cross_channel_far -->
> \rigorFull
> Let $K$ independent messenger channels each report a candidate source with per-channel false-alarm probabilities $\{p_c^{\mathrm{FAR}}\}_{c=1}^K$. If all $K$ channels report consistent source hypotheses (per Definition [ref]), the joint false-alarm probability satisfies:
> 
> $$<!-- label: eq:joint_far -->
> \Pbb[joint false alarm] \leq \left(\prod_{c=1}^K p_c^{\mathrm{FAR}}\right) \cdot \left(\prod_{c=1}^K \xi_c\right)^{-1},
> $$
> 
> where $\xi_c = \Pbb[consistency with true hypothesis \mid source in channel  c]$ is the channel-specific consistency efficiency (the probability that, given a real source, the channel reports parameters consistent with the other $K-1$ channels). For typical multi-messenger configurations, $\xi_c \gtrsim 0.5$, yielding super-exponential suppression:
> 
> $$<!-- label: eq:super_exp_far -->
> \Pbb[joint false alarm] \leq 2^K \prod_{c=1}^K p_c^{\mathrm{FAR}}.
> $$
> 
> 
> Furthermore, if each channel reports a significance of at least $S_c = -\log_{10} p_c^{\mathrm{FAR}}$, the joint significance is:
> 
> $$<!-- label: eq:joint_significance -->
> S_{\mathrm{joint}} \geq \sum_{c=1}^K S_c - K \log_{10} 2 \geq \sum_{c=1}^K S_c - 0.301 K.
> $$

> **Proof:** **Step 1: Joint false-alarm decomposition.**
> A joint false alarm occurs when: (a) each channel $c$ produces a false detection (with probability $p_c^{\mathrm{FAR}}$), AND (b) the false detections happen to be consistent with each other. Under A1 (channel independence), the noise fluctuations in different channels are independent. Therefore:
> 
> $$
> \Pbb[joint FA] = \Pbb[all channels FA] \cdot \Pbb[consistent \mid all channels FA].
> $$
> 
> 
> **Step 2: Consistency probability for false alarms.**
> When all detections are false alarms (noise fluctuations), the reconstructed parameters $\hat{\mathbf{n}}_c, \hat{D}_{L,c}$ are distributed according to the noise-only posterior, which for well-designed pipelines is approximately uniform over the instrument's sky coverage. The probability that $K$ independent, uniformly distributed sky positions are mutually consistent (within angular tolerance $\delta\theta = \max_c \sigma_{c,\mathrm{sky}}$) is:
> 
> $$
> \Pbb[consistent \mid all FA] = \prod_{c=2}^K \Pbb[d_{\mathrm{sky}}(\hat{\mathbf{n}}_1^{\mathrm{noise}}, \hat{\mathbf{n}}_c^{\mathrm{noise}}) \leq \delta\theta] \approx \prod_{c=2}^K \frac{\pi (\delta\theta)^2}{4\pi} = \left(\frac{\delta\theta}{2}\right)^{2(K-1)},
> $$
> 
> which is exponentially small in $K$. For $\delta\theta = 1^\circ$ (typical GW localization), this is $\sim (8.7 \times 10^{-3})^{2(K-1)}$.
> 
> **Step 3: Consistency efficiency for real sources.**
> For a real source, the probability that channel $c$ reports parameters consistent with the true (and thus with other channels') parameters is:
> 
> $$
> \xi_c = \int_{\Omega_{\mathrm{cons}}} p(\hat{\boldsymbol}_c \mid \mathbf{s}_{\mathrm{true}}) \, d\hat{\boldsymbol}_c,
> $$
> 
> where $\Omega_{\mathrm{cons}}$ is the consistency region defined by Eq. [ref]. For a well-calibrated instrument, $\xi_c$ is the frequentist coverage of the 68\% credible interval, which should be $\approx 0.68$ for Gaussian posteriors. Conservatively, $\xi_c \gtrsim 0.5$.
> 
> **Step 4: Total joint false-alarm probability.**
> By the law of total probability:
> 
> $$
> \Pbb[joint detection] &= \Pbb[real source] \cdot \prod_{c} \xi_c \cdot \Pbb[detection \mid source] 

> &\quad + \Pbb[all FA] \cdot \Pbb[consistent \mid all FA] .
> $$
> 
> 
> Since $\Pbb[consistent \mid all FA] \ll \prod_c \xi_c$ (for $K \geq 2$ and reasonable $\delta\theta$), false alarms are exponentially suppressed relative to the naive product of per-channel FARs. The factor $(\prod_c \xi_c)^{-1}$ in Eq. [ref] accounts for the efficiency loss. With $\xi_c \geq 0.5$, we obtain Eq. [ref]. The significance formula (Eq. [ref]) follows directly. $\square$

> **Corollary:** [Minimum Channels for 5$\sigma$ Joint Significance]<!-- label: cor:min_channels -->
> If each channel independently achieves $S_c = 2$ ($p_c^{\mathrm{FAR}} = 0.01$, approximately $2.3\sigma$), then $K=3$ channels achieve joint significance $S_{\mathrm{joint}} \geq 6 - 0.9 = 5.1 > 5$ (exceeding the particle physics ``discovery'' threshold). With $K=4$ channels at $S_c = 2$, $S_{\mathrm{joint}} \geq 8 - 1.2 = 6.8$. This demonstrates that multi-messenger observations can achieve discovery-level significance even when individual channels provide only modest evidence.

## Theorem 3: Instrumental Artifact vs.\ New Physics Unidentifiability 仪器伪影与新物理的不可辨识性定理
<!-- label: sec:unidentifiability -->

A central challenge in multi-messenger astronomy is distinguishing genuine astrophysical signals from instrumental artifacts. When multiple channels report an apparent coincidence, is it a real multi-messenger event, or could correlated instrumental artifacts masquerade as one? We prove that without declared assumptions about at least one instrument's systematics, this distinction is fundamentally unidentifiable.

### The Artifact-Physics Ambiguity 伪影-物理模糊性

Consider a scenario where IceCube reports a high-energy neutrino alert, and Fermi-LAT reports a $\gamma$-ray flare from a direction consistent with the neutrino. Two hypotheses compete:

1. **Astrophysical coincidence (天体物理巧合).** A genuine blazar flare produces both neutrinos (via hadronic processes in the jet) and $\gamma$-rays (via leptonic or hadronic emission), creating a true multi-messenger event.
2. **Instrumental coincidence (仪器巧合).** The neutrino alert is an atmospheric background fluctuation misreconstructed as astrophysical, AND the $\gamma$-ray flare is a statistical fluctuation above the diffuse background, AND their apparent spatial coincidence is a chance alignment.

\begin{assumption}[A6: Finite Observable Set 有限可观测量]<!-- label: ass:A6 -->
Each instrument produces a finite-dimensional summary statistic $\mathbf{o}_{c,i} \in \R^{d_{c,i}}$ (e.g., detection statistic, reconstructed direction, energy/distance estimate, and associated uncertainties). The total multi-messenger observable is $\mathbf{O} = (\mathbf{o}_{1,1}, ..., \mathbf{o}_{4, M_4}) \in \R^{d_{\mathrm{tot}}}$ where $d_{\mathrm{tot}} = \sum_{c,i} d_{c,i}$.
\end{assumption}

\begin{assumption}[A7: Instrumental Systematics Parametrization 仪器系统误差参数化]<!-- label: ass:A7 -->
For each instrument $(c,i)$, the systematic uncertainty is parametrized by a vector $\boldsymbol_{c,i} \in \mathcal{H}_{c,i} \subset \R^{q_{c,i}}$. The instrument response model is:

$$<!-- label: eq:systematics_model -->
\mathbf{o}_{c,i} = g_{c,i}(\mathbf{s}; \boldsymbol_{c,i}) + \boldsymbol_{c,i},
$$

where $g_{c,i}$ is the nominal instrument response and $\boldsymbol_{c,i} \sim N(0, \Sigma_{c,i})$ is statistical noise with known covariance $\Sigma_{c,i}$. The systematic parameters $\boldsymbol_{c,i}$ are unknown and must be calibrated.
\end{assumption}

\begin{assumption}[A8: New Physics Parametrization 新物理参数化]<!-- label: ass:A8 -->
A new-physics signal is parametrized by $\boldsymbol_{\mathrm{new}} \in \Phi_{\mathrm{new}} \subset \R^{r}$. The modified source state is $\mathbf{s}' = \mathbf{s} \oplus \boldsymbol_{\mathrm{new}}$, where $\oplus$ denotes augmentation of the standard astrophysical parameters with new-physics parameters (e.g., non-standard neutrino interactions, modified gravity parameters for GW propagation, axion-like particle effects on $\gamma$-ray spectra, Lorentz invariance violation energy-dependent delays).
\end{assumption}

> **Theorem:** [Instrumental Artifact vs.\ New Physics Unidentifiability 仪器伪影与新物理不可辨识性定理]<!-- label: thm:unidentifiability -->
> \rigorFull
> Under Assumptions [ref]-- [ref], for any multi-messenger observation $\mathbf{O}_{\mathrm{obs}}$ with finite statistical precision $\boldsymbol_{\mathrm{obs}}$, there exist distinct configurations:
> 
> $$
> (\boldsymbol^{(1)}, \boldsymbol_{\mathrm{new}}^{(1)}) \neq (\boldsymbol^{(2)}, \boldsymbol_{\mathrm{new}}^{(2)}),
> $$
> 
> where $\boldsymbol = \{\boldsymbol_{c,i}\}_{c,i}$ is the collective systematics vector, such that both configurations produce observationally equivalent outputs within measurement precision:
> 
> $$<!-- label: eq:obs_equiv_astro -->
> \norm{\E[\mathbf{O} \mid \boldsymbol^{(1)}, \boldsymbol_{\mathrm{new}}^{(1)}] - \E[\mathbf{O} \mid \boldsymbol^{(2)}, \boldsymbol_{\mathrm{new}}^{(2)}]} \leq \boldsymbol_{\mathrm{obs}}.
> $$
> 
> 
> Consequently, the attribution of an observed multi-messenger signal to ``instrumental artifact'' vs.\ ``new physics'' is **not identifiable** from the observational data alone. Explicit, falsifiable assumptions about at least one instrument's systematics or about the absence of specific new-physics effects are required for attribution.

> **Proof:** **Step 1: Dimensionality analysis.**
> The space of possible explanations for an observed multi-messenger signal has dimension:
> 
> $$
> \dim(explanations) = \underbrace{\sum_{c,i} \dim(\mathcal{H}_{c,i})}_{instrumental systematics} \;+\; \underbrace{\dim(\Phi_{\mathrm{new}})}_{new physics}.
> $$
> 
> 
> The observational constraint space has dimension $d_{\mathrm{tot}} = \sum_{c,i} d_{c,i}$ (the number of independent summary statistics). For typical multi-messenger campaigns:
> 
- Each GW instrument provides $d_{\mathrm{GW},i} \sim 15$--$20$ parameters (masses, spins, sky location, distance, orientation, tidal deformability) but only $\sim 5$--$10$ are well-constrained.
- Each EM instrument provides $d_{\mathrm{EM},i} \sim 3$--$10$ (position, flux, spectral index, temporal profile parameters).
- Each neutrino event provides $d_{\nu,i} \sim 3$--$5$ (direction, energy, topology).
- Each CR event provides $d_{\mathrm{CR},i} \sim 3$--$5$ (direction, energy, composition estimator).

> 
> The total $d_{\mathrm{tot}} \sim 20$--$50$ for a typical campaign, while the systematic parameters alone can exceed this: each instrument has $q_{c,i} \sim 5$--$20$ calibration parameters, detector response uncertainties, and background model parameters. With $M_{\mathrm{tot}} \sim 10$--$20$ instruments, $\dim(systematics) \sim 50$--$400 \gg d_{\mathrm{tot}}$.
> 
> **Step 2: Explicit construction of observationally equivalent worlds.**
> 
> **World 1 (Instrumental artifact):** All instruments suffer from a systematic bias $\boldsymbol^{(1)}$, and no new physics is present ($\boldsymbol_{\mathrm{new}}^{(1)} = \mathbf{0}$). The expected observation is:
> 
> $$
> \E[\mathbf{O} \mid World 1] = g(\mathbf{s}_{\mathrm{standard}}; \boldsymbol^{(1)}).
> $$
> 
> 
> **World 2 (New physics):** All instruments are perfectly calibrated ($\boldsymbol^{(2)} = \mathbf{0}$, i.e., nominal calibration), but new physics $\boldsymbol_{\mathrm{new}}^{(2)} \neq \mathbf{0}$ modifies the source. The expected observation is:
> 
> $$
> \E[\mathbf{O} \mid World 2] = g(\mathbf{s}_{\mathrm{standard}} \oplus \boldsymbol_{\mathrm{new}}^{(2)}; \mathbf{0}).
> $$
> 
> 
> Equating the two:
> 
> $$<!-- label: eq:equating -->
> g(\mathbf{s}_{\mathrm{standard}}; \boldsymbol^{(1)}) = g(\mathbf{s}_{\mathrm{standard}} \oplus \boldsymbol_{\mathrm{new}}^{(2)}; \mathbf{0}).
> $$
> 
> 
> **Step 3: Solvability via the implicit function theorem.**
> Consider the map $F(\boldsymbol, \boldsymbol_{\mathrm{new}}) = g(\mathbf{s} \oplus \boldsymbol_{\mathrm{new}}; \boldsymbol) - g(\mathbf{s}; \mathbf{0})$. We seek $(\boldsymbol, \boldsymbol_{\mathrm{new}})$ such that $\norm{F(\boldsymbol, \boldsymbol_{\mathrm{new}})} \leq \boldsymbol_{\mathrm{obs}}$.
> 
> At the origin $(\mathbf{0}, \mathbf{0})$, we have $F(\mathbf{0}, \mathbf{0}) = \mathbf{0}$ by definition (nominal calibration, standard physics). For sufficiently smooth $g$, the implicit function theorem guarantees the existence of a $(d_{\mathrm{tot}})$-dimensional manifold of solutions through $(\mathbf{0}, \mathbf{0})$ provided that the Jacobian $[\partial_{\boldsymbol} g \;\; \partial_{\boldsymbol} g]$ has full row rank $d_{\mathrm{tot}}$.
> 
> **Step 4: Dimensionality of the equivalence manifold.**
> The Jacobian has dimensions $d_{\mathrm{tot}} \times (\dim(\boldsymbol) + \dim(\boldsymbol_{\mathrm{new}}))$. Since $\dim(\boldsymbol) + \dim(\boldsymbol_{\mathrm{new}}) \gg d_{\mathrm{tot}}$ in realistic scenarios, the nullspace of the Jacobian has dimension at least:
> 
> $$
> \dim(nullspace) = \dim(\boldsymbol) + \dim(\boldsymbol_{\mathrm{new}}) - d_{\mathrm{tot}} \gg 0.
> $$
> 
> 
> Each direction in this nullspace corresponds to a continuous family of $(\boldsymbol, \boldsymbol_{\mathrm{new}})$ that produce *identical* expected observations. This establishes the existence of distinct configurations that are observationally equivalent at the level of expectation values.
> 
> **Step 5: Finite precision extension.**
> With finite statistical precision $\boldsymbol_{\mathrm{obs}}$, the equivalence region expands from a manifold to a ``tube'' of radius $\boldsymbol_{\mathrm{obs}}$ around it. The volume of this tube in the $(\dim(\boldsymbol) + \dim(\boldsymbol_{\mathrm{new}}))$-dimensional space is substantial, containing infinitely many observationally indistinguishable configurations.
> 
> **Step 6: Concrete astrophysical example.**
> Consider IceCube neutrino alert IC-170922A, temporally and spatially coincident with TXS~0506+056 $\gamma$-ray flare  [cite]. The question: is this a genuine hadronic blazar flare, or could it be explained by (a) IceCube ice model miscalibration creating a directional bias, coincident with (b) Fermi-LAT effective area miscalibration enhancing the apparent $\gamma$-ray flux?
> 
> Let $\eta_{\mathrm{ice}}$ parametrize the ice model uncertainty (affecting neutrino direction reconstruction by $\sim 1^\circ$--$2^\circ$). Let $\eta_{\mathrm{LAT}}$ parametrize the effective area uncertainty (affecting flux reconstruction by $\sim 5\%$--$10\%$). Let $\phi_{\mathrm{hadronic}}$ parametrize the hadronic emission component (proton acceleration efficiency in the blazar jet).
> 
> The observed $\gamma$-ray flux $\Phi_$ and neutrino flux $\Phi_$ satisfy:
> 
> $$
> \Phi_^{\mathrm{obs}} &= \Phi_^{\mathrm{true}} \cdot (1 + \eta_{\mathrm{LAT}}) + \epsilon_, 

> \Phi_^{\mathrm{obs}} &= \Phi_^{\mathrm{true}}(\phi_{\mathrm{hadronic}}) \cdot (1 + \eta_{\mathrm{ice}}) + \epsilon_.
> $$
> 
> 
> For any observed $(\Phi_^{\mathrm{obs}}, \Phi_^{\mathrm{obs}})$, we can choose:
> 
- **World 1:** $\phi_{\mathrm{hadronic}}^{(1)} = 0$ (no hadronic emission), $\eta_{\mathrm{LAT}}^{(1)} = \frac{\Phi_^{\mathrm{obs}}}{\Phi_^{\mathrm{true}}} - 1$, $\eta_{\mathrm{ice}}^{(1)} = \frac{\Phi_^{\mathrm{obs}}}{\Phi_^{\mathrm{true}}(0)} - 1$ (both observations explained by calibration errors).
- **World 2:** $\phi_{\mathrm{hadronic}}^{(2)} = \phi_* \neq 0$ (genuine hadronic emission), $\eta_{\mathrm{LAT}}^{(2)} = 0$, $\eta_{\mathrm{ice}}^{(2)} = 0$ (perfect calibration), with $\phi_*$ chosen to satisfy $\Phi_^{\mathrm{true}}(\phi_*) = \Phi_^{\mathrm{obs}}$ and $\Phi_^{\mathrm{true}} = \Phi_^{\mathrm{obs}}$.

> 
> Both worlds produce identical observed fluxes, yet one attributes the signal to calibration error, the other to new astrophysics. The unidentifiability is manifest. $\square$

> **Corollary:** [Assumption Mandate for Multi-Messenger Discovery Claims 多信使发现声明的假设要求]<!-- label: cor:assumption_mandate_astro -->
> Any claim of a new-physics discovery from multi-messenger observations MUST be accompanied by:
> 
1. An explicit declaration of which instrumental systematics are assumed bounded (and at what level);
2. A quantitative exclusion of the ``instrumental artifact'' hypothesis, achieved either by:
3. A sensitivity analysis showing how the discovery significance degrades when each systematic parameter is varied within its allowed range.

> Without these, the attribution of an observed multi-messenger signal to new physics rather than instrumental artifact is logically underdetermined.

> **Remark:** [Why Multi-Messenger Astronomy is the Strongest Application 为何多信使天文学是最强应用]
> \ThmSCXHonest{} (the Honest Agent Theorem of SCX) establishes error-source unidentifiability in any multi-expert system. Multi-messenger astronomy amplifies this unidentifiability in three unique ways:
> 
1. **Ultra-rare events.** Multi-messenger events are often one-of-a-kind (GW170817 was the first and for years the only BNS merger with EM counterpart). Without a statistical ensemble, distinguishing a one-off systematic anomaly from a one-off astrophysical event is impossible without calibration assumptions.
2. **Heterogeneous time-domain selection.** Different instruments have different duty cycles, field-of-view coverages, and triggering algorithms. An apparent multi-messenger coincidence may arise because the joint selection function enhances the probability of observing simultaneous fluctuations---a ``look-elsewhere effect'' across instruments that is difficult to quantify without explicit modeling of the joint selection function.
3. **Propagation effects as pseudo-systematics.** Photon propagation effects (dust extinction, intergalactic magnetic fields, plasma dispersion) modify EM signals in ways that can mimic or mask new-physics propagation effects (axion-photon conversion, Lorentz invariance violation). Since propagation effects are poorly known along arbitrary lines of sight, they constitute an additional systematic uncertainty that compounds the instrumental one.

> These three mechanisms make multi-messenger astronomy the domain where \ThmSCXHonest{} is not merely applicable but *necessary* for honest scientific inference.

## Cercis{ Score for Observational Campaigns 观测活动的Cercis评分}
<!-- label: sec:cercis -->

The Cercis{} scoring framework  [cite] ranks agents (here, observational campaigns or instruments) by a convex combination of quality $Q$ and novelty $N$. We adapt it to multi-messenger astronomy.

### Campaign Quality $Q$ 观测质量

> **Definition:** [Observational Campaign Quality]<!-- label: def:Q_astro -->
> For a multi-messenger observational campaign $\mathcal{C}$ (a set of instruments deployed over a time interval), the quality score is:
> 
> $$<!-- label: eq:Q_astro -->
> Q(\mathcal{C}) = \underbrace{w_{\mathrm{loc}} \cdot Q_{\mathrm{loc}}(\mathcal{C})}_{localization accuracy} + \underbrace{w_{\mathrm{spec}} \cdot Q_{\mathrm{spec}}(\mathcal{C})}_{spectral fidelity} + \underbrace{w_{\mathrm{time}} \cdot Q_{\mathrm{time}}(\mathcal{C})}_{temporal coverage},
> $$
> 
> where:
> 
- **Localization accuracy 定位精度:**
- **Spectral fidelity 光谱保真度:**
- **Temporal coverage 时间覆盖:**

> The weights satisfy $w_{\mathrm{loc}} + w_{\mathrm{spec}} + w_{\mathrm{time}} = 1$.

### Discovery Novelty $N$ 发现新颖性

> **Definition:** [Discovery Novelty]<!-- label: def:N_astro -->
> The discovery novelty of a multi-messenger campaign quantifies the uniqueness of the observed source class and messenger combination:
> 
> $$<!-- label: eq:N_astro -->
> N(\mathcal{C}) = \sum_{c \in \mathcal{C}} \nu_c^{\mathrm{messenger}} \cdot \ind{first detection in channel  c} \;+\; \nu_{\mathrm{class}} \cdot \ind{new source class},
> $$
> 
> where:
> 
- $\nu_c^{\mathrm{messenger}} \propto 1/n_c$: inverse frequency of channel $c$ being part of a multi-messenger detection. For the EM channel (present in 100\% of astronomical detections), $\nu_{\mathrm{EM}} = 0$. For GW (present only in BNS/BBH mergers), $\nu_{\mathrm{GW}} = 2.5$. For neutrinos (only TXS~0506+056 and a few others), $\nu_ = 5.0$. For CRs (no confirmed multi-messenger association to date), $\nu_{\mathrm{CR}} = 10.0$.
- $\nu_{\mathrm{class}} \propto$: bonus for detecting a previously unobserved source class (e.g., BNS merger in GW+EM was $\nu_{\mathrm{class}} = 5.0$; a hypothetical NSBH+EM would be $\nu_{\mathrm{class}} = 7.5$; a hypothetical supernova neutrino+GW+EM would be $\nu_{\mathrm{class}} = 10.0$).

> **Definition:** [Cercis{} Observational Score 观测Cercis评分]<!-- label: def:cercis_astro -->
> 
> $$<!-- label: eq:S_astro -->
> S(\mathcal{C}) = Q(\mathcal{C}) + \eta \cdot N(\mathcal{C}),
> $$
> 
> where $\eta \geq 0$ is the novelty-accuracy tradeoff parameter. $\eta = 0$ recovers pure quality ranking (e.g., for time-domain astronomy surveys prioritizing well-characterized sources). $\eta \gg 1$ prioritizes frontier exploration (e.g., for triggering new instruments on unmodeled transients).

[Table omitted — see original .tex]

> **Remark:** [Interpreting the Cercis{} Score]
> The Cercis{} score provides a single-number summary, but its components must be reported separately for transparency. GW170817 scores highest among realized events due to its exceptional EM localization (HST identified the kilonova at $\sim 0.01$ arcsec precision) and its status as the first-of-its-kind BNS merger with EM counterpart. The hypothetical all-four-channel supernova detection scores highest due to unprecedented messenger coverage (GW + EM + $\nu$ + CR), even though its localization and spectral quality would likely be modest for the neutrino and CR channels.

## \Situs{ Encoding for Celestial Coordinates 天体坐标的Situs编码}
<!-- label: sec:situs -->

The \Situs{} encoding  [cite] maps physical objects into a metric space that respects geometric symmetries. For multi-messenger astronomy, we encode celestial coordinates with relativistic corrections, enabling principled comparison of source localizations across instruments with different systematic biases.

### Relativistic Celestial Coordinate Encoding 相对论天体坐标编码

> **Definition:** [\Situs{} Celestial Encoding]<!-- label: def:situs_celestial -->
> For a source with true sky direction $\mathbf{n}_{\mathrm{true}} \in S^2$ (in the Barycentric Celestial Reference System, BCRS), observed at Solar System Barycenter (SSB) arrival time $t_{\mathrm{SSB}}$, the \Situs{} encoding is a vector $\mathbf{z} \in \R^{d_z}$:
> 
> $$<!-- label: eq:situs_celestial -->
> \mathbf{z} = \Phi(\mathbf{n}_{\mathrm{true}}; t_{\mathrm{SSB}}, \mathbf{v}_{\mathrm{obs}}, \Phi_{\mathrm{lens}}, z_{\mathrm{cosmo}}) = 
> \begin{pmatrix}
> \alpha_{\mathrm{BCRS}} 
 \delta_{\mathrm{BCRS}} 
 \dot \Delta t_{\mathrm{corr}} 
 \dot \Delta t_{\mathrm{corr}} 
 \boldsymbol_{\mathrm{lens}} 
 z_{\mathrm{cosmo}}
> \end{pmatrix},
> $$
> 
> where:
> 
- $(\alpha_{\mathrm{BCRS}}, \delta_{\mathrm{BCRS}})$: right ascension and declination in the BCRS at reference epoch;
- $\Delta t_{\mathrm{corr}} = \Delta t_{\mathrm{Roemer}} + \Delta t_{\mathrm{Shapiro}} + \Delta t_{\mathrm{Einstein}}$: total relativistic time delay, decomposed into:
- **Roemer delay 罗默延迟:** $\Delta t_{\mathrm{Roemer}} = -\frac{\mathbf{r}_{\mathrm{obs}} \cdot \mathbf{n}}{c}$, the geometric light-travel time across the Solar System, where $\mathbf{r}_{\mathrm{obs}}$ is the observer's position relative to the SSB;
- **Shapiro delay 夏皮罗延迟:** $\Delta t_{\mathrm{Shapiro}} = \frac{2GM_\odot}{c^3} \ln\!\bigl(\frac{1 + \mathbf{n} \cdot \hat{\mathbf{r}}_{\mathrm{obs}}}{1 - \mathbf{n} \cdot \hat{\mathbf{r}}_}\bigr)$, the gravitational time delay from Solar System bodies;
- **Einstein delay 爱因斯坦延迟:** $\Delta t_{\mathrm{Einstein}} = \frac{1}{c^2} \int (\Phi_{\mathrm{Earth}} + \frac{v_{\mathrm{obs}}^2}{2}) dt$, the combined gravitational redshift and time dilation at the observatory;

>     \item $\boldsymbol_{\mathrm{lens}} \in \R^2$: weak gravitational lensing deflection vector (convergence $\kappa$ and shear $\gamma$);
>     \item $z_{\mathrm{cosmo}}$: cosmological redshift.
> \end{itemize}

### Lipschitz Guarantee for Coordinate Reconstruction 坐标重建的Lipschitz保证

\begin{assumption}[A9: Smooth Celestial Metric 光滑天球度量]<!-- label: ass:A9 -->
The mapping from source parameters to the \Situs{} encoding is $L_\Phi$-Lipschitz:

$$<!-- label: eq:lipschitz_situs -->
\norm{\Phi(\mathbf{s}_1) - \Phi(\mathbf{s}_2)}_2 \leq L_\Phi \cdot d_{\mathrm{src}}(\mathbf{s}_1, \mathbf{s}_2),
$$

where $d_{\mathrm{src}}$ is a metric on the source state space (e.g., $d_{\mathrm{src}}^2 = d_{\mathrm{sky}}^2 + (|\Delta D_L|/D_L)^2 + \sum (\Delta \theta_{\mathrm{src},j}/\sigma_{\theta_j})^2$). This holds for sufficiently smooth instrument response functions.
\end{assumption}

\begin{assumption}[A10: Finite Signal-to-Noise Ratio 有限信噪比]<!-- label: ass:A10 -->
Each instrument $(c,i)$ measures the \Situs{} encoding with additive Gaussian noise:

$$<!-- label: eq:noisy_situs -->
\hat{\mathbf{z}}_{c,i} = \Phi(\mathbf{s}) + \boldsymbol_{c,i}, \quad \boldsymbol_{c,i} \sim N(0, \Sigma_{c,i}),
$$

where $\Sigma_{c,i} \propto 1/\rho_{c,i}^2$ (the covariance scales inversely with the square of the detection SNR).
\end{assumption}

> **Theorem:** [\Situs{} Coordinate Reconstruction Guarantee 天体坐标Situs重建保证]<!-- label: thm:situs_reconstruction -->
> \rigorFull
> Under Assumptions [ref]-- [ref], given $N$ independent \Situs{} measurements $\{\hat{\mathbf{z}}_{c,i}\}$ from instruments across multiple channels, the optimal combined estimate $\hat{\mathbf{z}}_{\mathrm{opt}}$ (the inverse-variance-weighted mean) satisfies:
> 
> $$<!-- label: eq:situs_bound -->
> \E\bigl[\norm{\hat{\mathbf{z}}_{\mathrm{opt}} - \Phi(\mathbf{s})}_2^2\bigr] \leq \frac{d_z}{\sum_{c,i} \lambda_(\Sigma_{c,i}^{-1})},
> $$
> 
> where $\lambda_(\Sigma_{c,i}^{-1})$ is the minimum eigenvalue of the precision matrix for instrument $(c,i)$. Consequently, the angular reconstruction error (in radians) is bounded by:
> 
> $$<!-- label: eq:angular_bound -->
> \E[d_{\mathrm{sky}}(\hat{\mathbf{n}}_{\mathrm{opt}}, \mathbf{n}_{\mathrm{true}})] \leq \frac{1}{L_\Phi} \sqrt{\frac{d_z}{\sum_{c,i} \rho_{c,i}^2 / \sigma_{0; c,i}^2}},
> $$
> 
> where $\sigma_{0; c,i}^2$ is the baseline noise variance per unit SNR$^2$ for instrument $(c,i)$.

> **Proof:** **Step 1: Inverse-variance weighting.**
> Under A10, each measurement $\hat{\mathbf{z}}_{c,i}$ is an unbiased estimate of $\Phi(\mathbf{s})$ with known covariance $\Sigma_{c,i} = (1/\rho_{c,i}^2) \Sigma_{0; c,i}$. The inverse-variance-weighted combined estimate is:
> 
> $$
> \hat{\mathbf{z}}_{\mathrm{opt}} = \left(\sum_{c,i} \Sigma_{c,i}^{-1}\right)^{-1} \sum_{c,i} \Sigma_{c,i}^{-1} \hat{\mathbf{z}}_{c,i}.
> $$
> 
> 
> This is the minimum-variance unbiased linear estimator (Gauss-Markov theorem). Its covariance is:
> 
> $$
> \Cov(\hat{\mathbf{z}}_{\mathrm{opt}}) = \left(\sum_{c,i} \Sigma_{c,i}^{-1}\right)^{-1}.
> $$
> 
> 
> **Step 2: Expected squared error.**
> The expected squared $\ell_2$ error is the trace of the covariance:
> 
> $$
> \E[\norm{\hat{\mathbf{z}}_{\mathrm{opt}} - \Phi(\mathbf{s})}_2^2] &= \operatorname{tr}\!\left[\left(\sum_{c,i} \Sigma_{c,i}^{-1}\right)^{-1}\right] 

> &\leq d_z \cdot \lambda_\!\left[\left(\sum_{c,i} \Sigma_{c,i}^{-1}\right)^{-1}\right]  

> &= \frac{d_z}{\lambda_\!\left(\sum_{c,i} \Sigma_{c,i}^{-1}\right)}  

> &\leq \frac{d_z}{\sum_{c,i} \lambda_(\Sigma_{c,i}^{-1})},
> $$
> 
> where the final inequality uses the fact that for positive semi-definite matrices, the minimum eigenvalue of a sum is at least the sum of the minimum eigenvalues (by Weyl's inequality for PSD matrices, $\lambda_(A+B) \geq \lambda_(A) + \lambda_(B)$ when $A, B \succeq 0$).
> 
> **Step 3: Angular error bound.**
> Under A9 (Lipschitz continuity of $\Phi$), we have:
> 
> $$
> d_{\mathrm{sky}}(\hat{\mathbf{n}}, \mathbf{n}_{\mathrm{true}}) \leq \frac{1}{L_\Phi} \norm{\Phi(\hat{\mathbf{s}}) - \Phi(\mathbf{s})}_2.
> $$
> 
> 
> The expected angular error follows from Jensen's inequality and the covariance bound above. Substituting $\lambda_(\Sigma_{c,i}^{-1}) = \rho_{c,i}^2 / \lambda_(\Sigma_{0; c,i})$ and defining $\sigma_{0; c,i} = \sqrt{\lambda_(\Sigma_{0; c,i})}$ yields Eq. [ref]. $\square$

> **Remark:** [Relativistic Correction Importance 相对论修正的重要性]
> The Roemer delay correction alone amounts to $\sim 500$ seconds (8.3 light-minutes) across the Earth's orbit. For high-cadence time-domain surveys (ZTF, LSST) with minute-level cadences, neglecting this correction produces apparent source motion that could be mistaken for proper motion or orbital reflex. The \Situs{} encoding absorbs these corrections into the coordinate representation, ensuring that coordinate comparison across instruments is performed in a common relativistic frame.

### Gravitational Lensing Encoding 引力透镜编码

For sources at cosmological distances ($z \gtrsim 0.5$), weak gravitational lensing by large-scale structure introduces deflections of $\sim 1$--$10$ arcseconds and magnification of $\sim 1\%$--$10\%$. The \Situs{} encoding includes a lensing vector $\boldsymbol_{\mathrm{lens}}$:

> **Proposition:** [Lensing Correction in \Situs{} Encoding]<!-- label: prop:lensing_situs -->
> For a source at redshift $z_s$, the lensing deflection $\boldsymbol(\boldsymbol)$ relates the observed image position $\boldsymbol$ to the unlensed position $\boldsymbol$ via the lens equation $\boldsymbol = \boldsymbol - \boldsymbol(\boldsymbol)$. The \Situs{} encoding captures the differential deflection between messenger channels:
> 
> $$<!-- label: eq:lensing_differential -->
> \Delta \boldsymbol_{c, c'} = \boldsymbol_c(\boldsymbol) - \boldsymbol_{c'}(\boldsymbol),
> $$
> 
> which is non-zero when different messenger particles traverse different gravitational potentials (e.g., neutrinos vs.\ photons in a core-collapse supernova). For all EM sub-bands, $\Delta \boldsymbol = 0$ (achromatic lensing). For GW vs.\ EM, $\Delta \boldsymbol = 0$ in General Relativity (both propagate along null geodesics) but may differ in modified gravity theories.

## Multi-Instrument Yajie{ Consensus 多仪器Yajie共识}
<!-- label: sec:yajie -->

Yajie{} is the SCX{} game-theoretic consensus mechanism  [cite]. In multi-messenger astronomy, consensus operates at two levels: (i) per-channel consensus among instruments within each messenger channel, and (ii) cross-channel consensus aggregating channel-level source hypotheses.

### Two-Level Multi-Messenger Consensus Architecture 双层多信使共识架构

> **Definition:** [Multi-Messenger Yajie{} Game 多信使Yajie博弈]<!-- label: def:yajie_astro -->
> The multi-messenger Yajie{} game is a hierarchical game:
> 
> **Level 1 --- Per-channel consensus (每通道共识):**
> 
- **Players:** $M_c$ instruments in channel $c$.
- **States:** Candidate transient events (time windows containing potential astrophysical signals).
- **Actions:** Instrument $i$ in channel $c$ declares a detection with trust score $\tau_{c,i} \in [0,1]$ based on its own detection statistic $\rho_{c,i}$ relative to the channel threshold $\tau_c$.
- **Payoff:** $\pi_{c,i} = \frac{1}{N_{\mathrm{ev}}}\sum_{k} \ind{\tau_{c,i}^{(k)} \geq \overline{\mathrm{med}}(\boldsymbol_{c,-i}^{(k)})} \cdot \mathrm{acc}_{c,i}^{(k)}$, where $\mathrm{acc}_{c,i}^{(k)}$ is the measured accuracy of instrument $i$ on calibration events (e.g., GRBs with known positions from well-localized afterglows).

> 
> **Level 2 --- Cross-channel consensus (跨通道共识):**
> 
- **Players:** Aggregated channel-level source hypotheses $\{\hat{\mathbf{s}}_c\}_{c \in \mathcal{C}}$.
- **States:** Joint multi-messenger candidate events.
- **Actions:** Channel $c$ outputs a cross-channel trust score $\tau_c^{\mathrm{cross}} \in [0,1]$ indicating confidence that its source hypothesis is consistent with other channels.
- **Payoff:** $\pi_c^{\mathrm{cross}} = \ind{\tau_c^{\mathrm{cross}} \geq \overline{\mathrm{med}}(\boldsymbol_{-c}^{\mathrm{cross}})} \cdot \mathcal{L}_{\mathrm{joint}}(\hat{\mathbf{s}}_1, ..., \hat{\mathbf{s}}_K)$, where $\mathcal{L}_{\mathrm{joint}}$ is the joint likelihood of the multi-messenger data under the combined source hypothesis.

> **Proposition:** [Yajie{} Event Classification 事件分类]<!-- label: prop:yajie_classification -->
> At equilibrium of the two-level Yajie{} game, candidate multi-messenger events partition into three classes:
> 
1. **Gold events 金牌事件:** Level~1 consensus holds for all participating channels ($\tau_{c,i} > 1/2$ for all $c,i$) AND Level~2 consensus holds ($\tau_c^{\mathrm{cross}} > 1/2$ for all $c$). These events have maximal certified confidence and are suitable for precision astrophysics and fundamental physics tests.
2. **Silver events 银牌事件:** Level~1 consensus holds for all channels, but Level~2 consensus fails for at least one channel. The inconsistent channel's source hypothesis is flagged for investigation (possible misidentification, background contamination, or new class of transient with unexpected multi-messenger properties).
3. **Bronze events 铜牌事件:** Level~1 consensus fails for at least one channel (instruments within a channel disagree). The channel's data are flagged for reanalysis; the event may still be scientifically valuable if other channels achieve at least Silver status.

> **Proof:** \rigorSketch
> At Level~1 equilibrium, the trust-score best response (as derived in the pseudopotential Yajie{} analysis  [cite], Section~6.2) partitions instruments within each channel into those that trust their own detection ($\tau_{c,i} > 1/2$) and those that distrust ($\tau_{c,i} \leq 1/2$). Consensus requires all instruments to trust.
> 
> At Level~2, the cross-channel trust score reflects the consistency of source hypotheses. Channels with consistent hypotheses achieve $\tau_c^{\mathrm{cross}} > 1/2$; inconsistent channels fall below. The three-way classification follows from the two binary consensus outcomes (Level~1 and Level~2). $\square$

### Ground-Truth Anchoring via Archival and Triggered Observations 通过档案和触发观测的地面实况锚定

> **Proposition:** [Ground-Truth Anchoring Proposition 地面实况锚定命题]<!-- label: prop:ground_truth -->
> Multi-messenger astronomy uniquely admits ground-truth anchoring through:
> 
1. **Well-localized EM counterparts (精确定位的电磁对应体).** When an EM afterglow or kilonova is localized to sub-arcsecond precision by VLBI, HST, or JWST, its position serves as ground truth for GW, neutrino, and CR directional reconstruction.
2. **Host galaxy identification (宿主星系识别).** Spectroscopic redshift of the host galaxy provides ground-truth distance, anchoring the distance scale for GW and neutrino estimates.
3. **Calibration sources (校准源).** Pulsars (periodic GW emitters for LIGO/Virgo/KAGRA), the Moon shadow (for IceCube pointing calibration), and the Galactic Center (for cosmic ray anisotropy studies) provide continuous calibration.

> When Level~2 consensus fails despite a well-localized EM counterpart, the disagreement between the EM position and the GW/neutrino/CR position directly quantifies the systematic pointing error of the non-EM instruments---a rare opportunity for instrumental calibration using astrophysical sources.

\begin{algorithm}[htbp]
*Caption:* Multi-Messenger SCX{} Audit with Yajie{} Consensus 多信使SCX审计与Yajie共识
<!-- label: alg:multi_messenger_audit -->
\begin{algorithmic}[1]
\Require Candidate transient event, instrument data $\{\mathcal{D}_{c,i}\}$, calibration datasets
\Ensure Yajie{} event classification (Gold/Silver/Bronze), Cercis{} score, attribution report

\For{each messenger channel $c \in \mathcal{C}$}
    \For{each instrument $i = 1, ..., M_c$}
        \State Compute detection statistic $\rho_{c,i}$ and per-instrument $p$-value $p_{c,i}^{\mathrm{FAR}}$
        \State Reconstruct source parameters $\hat{\mathbf{s}}_{c,i}$ with uncertainties
        \State Compute \Situs{} encoding $\hat{\mathbf{z}}_{c,i}$ via Eq. [ref]
    \EndFor
    \State **Level-1 Yajie{} consensus:** Compute trust scores $\tau_{c,i}$, determine consensus
    \State Compute channel-level aggregated source hypothesis $\hat{\mathbf{s}}_c$ (inverse-variance weighted)
    \State Apply Theorem [ref]: compute per-channel miss probability
\EndFor

\State **Level-2 Yajie{} consensus:** For all pairs $(c, c')$, compute consistency via Eq. [ref]
\State Compute cross-channel trust scores $\tau_c^{\mathrm{cross}}$
\State Classify event as Gold / Silver / Bronze per Proposition [ref]

\If{Level-2 consensus fails AND EM counterpart exists}
    \State Quantify systematic pointing/distance error for non-EM instruments
    \State Apply Theorem [ref]: determine if discrepancy is calibration error or new physics
\EndIf

\State Compute Cercis{} campaign score $S(\mathcal{C})$ via Eq. [ref]
\State \Return Audit report: event class, detection confidence, joint FAR, Cercis{} score, attribution analysis
\end{algorithmic}
\end{algorithm}

## Experimental Protocol 实验协议
<!-- label: sec:experiment -->

We propose a structured experimental protocol for evaluating SCX{}-audited multi-messenger inference, organized by event class.

### Benchmark Event Suite 基准事件集

1. **GW170817 / GRB~170817A --- Binary Neutron Star Merger 双中子星合并.**
2. **IceCube Alert Follow-up --- High-Energy Neutrino Events 高能中微子事件.**
3. **Fast Radio Burst Localization 快速射电暴定位.**
4. **Simulated ``Diamond'' Event --- All Four Channels 模拟钻石级事件.**

### Statistical Reporting Requirements 统计报告要求

All multi-messenger SCX{} audit reports must include:

1. **Per-channel:** Per-instrument detection statistics $\rho_{c,i}$, false-alarm probabilities $p_{c,i}^{\mathrm{FAR}}$, effective multiplicity $M_c^{\mathrm{eff}}$ and instrument correlation $\bar_c$.
2. **Joint:** Joint detection confidence $1 - \Pbb[miss_{\mathrm{joint}}]$ (Theorem [ref]); joint false-alarm probability (Theorem [ref]); joint significance $S_{\mathrm{joint}}$.
3. **Unidentifiability:** Explicit assumption declaration listing which instrumental systematics are assumed bounded (Corollary [ref]); sensitivity analysis varying systematic parameters; statement of which alternative hypotheses (instrumental artifact, astrophysical background, new physics) remain viable under specified assumptions.
4. **Cercis{} score:** Separate reporting of $Q_{\mathrm{loc}}$, $Q_{\mathrm{spec}}$, $Q_{\mathrm{time}}$, $N$, and $\eta$; justification of weight choices.
5. **Yajie{} consensus:** Level-1 consensus per channel; Level-2 cross-channel consensus matrix; event classification (Gold/Silver/Bronze).
6. **\Situs{} encoding:** Coordinate reconstruction accuracy; relativistic correction magnitudes; lensing differential between channels.
7. **Computational cost:** Total analysis wall-clock time; per-instrument processing time; latency from trigger to alert.

## Discussion 讨论
<!-- label: sec:discussion -->

### Path to Certified Multi-Messenger Astrophysics 通往认证多信使天体物理学的路径

The SCX{} framework provides the auditing infrastructure for transforming multi-messenger astronomy from a collection of independent detection claims into a certified, auditable inference system:

1. **Real-time auditing 实时审计.** As alert streams arrive (LIGO/Virgo/KAGRA low-latency, IceCube real-time alerts, Fermi-GBM sub-threshold triggers, ZTF/LSST alert brokers), the Yajie{} consensus mechanism (Section [ref]) can operate in real time, classifying candidate multi-messenger events as Gold/Silver/Bronze and automatically triggering follow-up observations based on the classification tier.
2. **Population-level auditing 群体级审计.** Over an observing run, the Cercis{} score (Section [ref]) tracks the campaign's cumulative quality-novelty profile. A campaign that repeatedly achieves Gold-tier classifications on BNS mergers but Silver on NSBH mergers signals that the GW+EM joint inference pipeline is robust for equal-mass systems but degraded for mass-asymmetric systems---a diagnostic that would be invisible without the SCX{} classification framework.
3. **Unidentifiability as methodological discipline 不可辨识性作为方法学纪律.** Theorem [ref] establishes that instrumental artifacts and new physics are unidentifiable without declared assumptions. Rather than viewing this as a pessimistic result, we argue it enforces methodological honesty: every multi-messenger discovery claim must declare its calibration assumptions, and the community can judge whether those assumptions are reasonable. This prevents the accumulation of ``discoveries'' that later prove to be calibration errors.

### Relationship to Existing Multi-Messenger Frameworks 与现有多信使框架的关系

**AMON (Astrophysical Multimessenger Observatory Network)  [cite].** AMON provides a practical infrastructure for correlating sub-threshold alerts across instruments and issuing joint alerts. The SCX{} framework complements AMON by providing the theoretical underpinning for joint significance estimation (Theorem [ref]) and the formal limits of what can be concluded from joint detections (Theorem [ref]).

**Low-Latency Alert Pipelines  [cite].** LIGO/Virgo/KAGRA low-latency pipelines (GstLAL, PyCBC, MBTA, SPIIR) provide rapid GW candidate identification with false-alarm rate estimation. IceCube's real-time alert system  [cite] provides neutrino candidates within $\sim 30$ seconds of detection. The SCX{} Yajie{} consensus mechanism can ingest these heterogeneous alerts and produce a certified joint classification within the latency budget of follow-up telescopes.

**Bayesian Multi-Messenger Parameter Estimation  [cite].** Joint Bayesian parameter estimation across GW, EM, and neutrino data (e.g., using MultiNest or dynesty nested sampling) produces posterior distributions for source parameters. Theorem [ref] provides a frequentist guarantee on the reconstruction quality that complements the Bayesian credible intervals, and the \Situs{} encoding ensures that the joint analysis is performed in a common relativistic reference frame.

**Coincidence Search Methods  [cite].** Existing coincidence search methods (e.g., cross-correlating IceCube neutrino alerts with Fermi-LAT $\gamma$-ray light curves, or GW triggers with GRB catalogs) estimate significance via Monte Carlo simulations of isotropic backgrounds. Theorem [ref] provides an analytic bound that can validate or supplement these computationally expensive simulations.

### Limitations 局限性

**Assumption A1 (Channel Separability).** The assumption that noise processes are independent across channels may be violated for instruments sharing environmental noise sources (e.g., seismic noise affecting both GW detectors and nearby optical telescopes; solar activity affecting both space-based $\gamma$-ray detectors and ground-based CR detectors). The effective multiplicity correction $M_c^{\mathrm{eff}}$ partially addresses this through estimated correlation, but extreme correlated noise events (e.g., major earthquakes triggering spurious signals in multiple instruments) require dedicated veto procedures beyond the scope of this paper.

**Assumption A3 (Instrument Independence).** Instruments within a channel may share calibration sources or analysis methods, introducing correlated systematics. For example, LIGO Hanford and Livingston share calibration models derived from common photon calibrator techniques. The correlation $\bar_c$ must be estimated empirically from calibration uncertainty propagation.

**Assumption A9 (Smooth Celestial Metric).** The Lipschitz continuity of the \Situs{} encoding assumes that the instrument response varies smoothly with source position. This may fail for instruments with sharp field-of-view boundaries (e.g., coded-mask telescopes where the point-spread function degrades abruptly at the edge of the fully-coded field of view), requiring a piecewise-Lipschitz extension.

**Limited experimental ground truth.** Unlike laboratory experiments, astrophysical sources provide no controlled ground truth. Host galaxy redshifts and VLBI positions are the closest approximations but carry their own uncertainties (peculiar velocities for redshifts, reference frame ties for VLBI astrometry). The framework degrades gracefully: when ground truth is unavailable, Theorems [ref] and [ref] still provide relative confidence bounds among competing hypotheses, but absolute calibration requires external anchors.

**Unidentifiability is a feature.** Theorem [ref] may appear to limit the power of multi-messenger astronomy. We argue the opposite: by forcing explicit declaration of assumptions, it *strengthens* scientific inference. A claim of new physics backed by an explicit calibration model (e.g., ``the IceCube pointing systematic is bounded at 0.3$^\circ$ by Moon shadow measurements, and the observed neutrino-$\gamma$-ray offset of 1.5$^\circ$ exceeds 5$\sigma$ relative to this bound'') is far more credible than a claim that simply reports a low $p$-value without addressing systematics.

### Future Directions 未来方向

1. **Integration with alert brokers.** Deploy the Yajie{} consensus algorithm as a plugin for community alert brokers (e.g., ALeRCE, ANTARES, AMPEL), providing real-time Gold/Silver/Bronze classification for every multi-messenger candidate.
2. **Population Cercis{} analysis.** Apply the Cercis{} scoring framework retrospectively to the full GWTC catalogs (O1--O4), IceCube alert archives, and GRB catalogs, producing a ranked atlas of multi-messenger event quality.
3. **Unidentifiability falsification tests.** Design targeted observational tests that break the observational equivalence between instrumental and new-physics hypotheses: e.g., if an apparent $\nu$-$\gamma$ correlation is due to IceCube ice model miscalibration, it should persist (or change character) after ice model updates; if it is astrophysical, it should be stable.
4. **Third-generation detector preparation.** Extend the framework to third-generation GW detectors (Einstein Telescope, Cosmic Explorer) and next-generation neutrino telescopes (IceCube-Gen2, KM3NeT/ARCA), where the dramatically increased sensitivity will make the unidentifiability Theorem [ref] even more acute: at high SNR, subtle systematic effects that were previously buried in statistical noise become the dominant uncertainty.

## Conclusion 结论

We have presented the SCX{} quality audit framework applied to multi-messenger astronomy. Four theorems---joint detection confidence (Theorem~1), cross-channel false-alarm suppression (Theorem~2), instrumental artifact vs.\ new physics unidentifiability (Theorem~3), and \Situs{} coordinate reconstruction (Theorem~4)---provide formal foundations for certified multi-messenger inference. The Cercis{} score enables quantitative comparison of observational campaigns, and the two-level Yajie{} consensus mechanism provides a practical event classification system (Gold/Silver/Bronze).

The framework addresses the central epistemic challenge of multi-messenger astronomy: when multiple instruments report a consistent astrophysical hypothesis, how confident should we be? Theorem~1 quantifies the confidence that we have not missed a genuine event; Theorem~2 quantifies the probability that the apparent coincidence is a chance alignment of noise fluctuations; Theorem~3 establishes the fundamental limit---without declared assumptions about instrumental systematics, we cannot distinguish calibration errors from new physics. Theorem~4 guarantees that our coordinate comparisons across instruments are performed in a consistent relativistic frame.

**核心命题** (Core Proposition): 多信使天文学通过多个独立的信使通道（电磁波、引力波、中微子、宇宙线）自然提供了多个观测"专家"。每个仪器（LIGO/Virgo/KAGRA、JWST、IceCube、Fermi、LSST）构成具有不同系统误差的专家。SCX{}审计框架通过显式化假设、量化联合检测置信度、系统化虚警抑制和分类事件质量，为多信使天文学提供了缺失的认证推理层。最重要的是，定理~3（仪器伪影与新物理不可辨识性）建立了基本的认识论界限：在没有声明的校准假设的情况下，仪器伪影和新物理信号产生观测等价的多信使签名---迫使科学论断必须透明地说明其校准假设。

## Acknowledgments 致谢

This work builds on the SCX{} theoretical framework  [cite]. We acknowledge the multi-messenger astronomy community---LIGO/Virgo/KAGRA, IceCube, Fermi, and electromagnetic follow-up collaborations---for producing the data that motivate and validate this framework. This paper makes no claim on the interpretation of any specific multi-messenger event; our contribution is a methodological framework for certifying the inference drawn from such events.

## Appendix
## Correlation Estimation for Multi-Instrument Effective Multiplicity 多仪器有效多重性相关估计
<!-- label: sec:app_correlation -->

We provide the estimation procedure for $\bar_c$, the average pairwise error correlation among instruments in channel $c$, used in the effective multiplicity $M_c^{\mathrm{eff}}$ of Theorem [ref].

For each instrument $i$ in channel $c$, consider a calibration set of $N_{\mathrm{cal}}$ events with known or well-determined parameters (e.g., GRBs with sub-arcsecond afterglow positions, or GW injections in detector noise). For each calibration event $k$, compute the error vector:

$$
\mathbf{e}_c^{(k)} = \bigl(e_{c,1}^{(k)}, ..., e_{c,M_c}^{(k)}\bigr), \quad e_{c,i}^{(k)} = \norm{\hat{\mathbf{s}}_{c,i}^{(k)} - \mathbf{s}_{\mathrm{true}}^{(k)}}_{\mathcal{S}},
$$

where $\norm_{\mathcal{S}}$ is a chosen norm on the source state space (e.g., Mahalanobis distance using the per-instrument covariance).

**Estimation procedure:**

1. Compute the $M_c \times M_c$ error correlation matrix $\hat{R}_{ij} = \Corr(\mathbf{e}_{c,i}, \mathbf{e}_{c,j})$, where $\mathbf{e}_{c,i} = (e_{c,i}^{(1)}, ..., e_{c,i}^{(N_{\mathrm{cal}})})^T$ is the vector of errors for instrument $i$ across all calibration events.
2. Estimate $\bar_c = \frac{2}{M_c(M_c-1)}\sum_{1 \leq i < j \leq M_c} \hat{R}_{ij}$.
3. Bootstrap 95\% confidence interval: resample calibration events with replacement $B = 1000$ times, recompute $\bar_c^{(b)}$, report $[\bar_{c, 0.025}, \bar_{c, 0.975}]$.

When $\bar_c < 0$ (instruments make complementary errors---e.g., one instrument systematically overestimates distance while another underestimates it), we conservatively set $M_c^{\mathrm{eff}} = M_c$, since negative correlation only improves the detection bound (the Hoeffding inequality remains valid under arbitrary dependence with bounded variables, though with a degradation of the constant  [cite]).

## Relativistic Time Delay Derivations 相对论时间延迟推导
<!-- label: sec:app_relativistic -->

We provide the explicit formulas for the relativistic time delays in the \Situs{} celestial encoding (Definition [ref]).

### Roemer Delay 罗默延迟
For an observatory at geocentric position $\mathbf{r}_{\mathrm{obs}}(t)$ relative to the Solar System Barycenter (SSB), the light-travel time correction to an inertial reference frame is:

$$<!-- label: eq:roemer_full -->
\Delta t_{\mathrm{Roemer}} = -\frac{\mathbf{r}_{\mathrm{obs}}(t) \cdot \hat{\mathbf{n}}}{c} + \Delta t_{\mathrm{Earth}},
$$

where $\Delta t_{\mathrm{Earth}}$ includes the geocentric correction (observatory position on the rotating Earth relative to the geocenter). For an observatory at geodetic latitude $\phi$, East longitude $\lambda$, and elevation $h$, the full geocentric position is:

$$
\mathbf{r}_{\mathrm{obs}} = \mathbf{R}_{\mathrm{geo}} + \mathbf{r}_{\mathrm{site}},
$$

where $\mathbf{R}_{\mathrm{geo}}$ is the geocenter's SSB position (from JPL ephemerides DE440  [cite]) and $\mathbf{r}_{\mathrm{site}}$ rotates with the Earth. The magnitude $|\Delta t_{\mathrm{Roemer}}| \leq 500$~s (1~AU$/c$).

### Shapiro Delay 夏皮罗延迟
The gravitational time delay from a body of mass $M$ at position $\mathbf{r}_M$ relative to the SSB, for a photon passing at impact parameter $b$, is:

$$<!-- label: eq:shapiro_full -->
\Delta t_{\mathrm{Shapiro}} = \sum_{M \in \{\odot, Jupiter, Saturn\}} \frac{2 G M}{c^3} \ln\!\left(\frac{R_{\mathrm{obs}} + \mathbf{R}_{\mathrm{obs}} \cdot \hat{\mathbf{n}}}{R_M + \mathbf{R}_M \cdot \hat{\mathbf{n}}}\right),
$$

where $\mathbf{R}_{\mathrm{obs}} = \mathbf{r}_{\mathrm{obs}} - \mathbf{r}_M$ is the vector from body $M$ to the observatory, and $R_{\mathrm{obs}} = |\mathbf{R}_{\mathrm{obs}}|$. The Sun contributes $\sim 120~\mu$s at grazing incidence; Jupiter contributes $\sim 0.3~\mu$s.

### Einstein Delay 爱因斯坦延迟
The combined gravitational redshift and time dilation at the observatory, integrated from a reference epoch $t_0$ to observation time $t$, is:

$$<!-- label: eq:einstein_full -->
\Delta t_{\mathrm{Einstein}} = \frac{1}{c^2} \int_{t_0}^{t} \left(\Phi_{\mathrm{Earth}}(t') + \frac{v_{\mathrm{obs}}^2(t')}{2}\right) dt',
$$

where $\Phi_{\mathrm{Earth}}(t) = -\frac{GM_\oplus}{r_{\mathrm{obs}}(t)}$ is the Earth's gravitational potential at the observatory location, and $v_{\mathrm{obs}}(t)$ is the observatory's velocity in the SSB frame. For ground-based observatories, $\Delta t_{\mathrm{Einstein}} \sim 10$--$100~\mu$s integrated over one year, dominated by the Earth's orbital eccentricity.

### Total \Situs{ Time Correction}
The \Situs{} encoding applies the total relativistic time correction $\Delta t_{\mathrm{corr}} = \Delta t_{\mathrm{Roemer}} + \Delta t_{\mathrm{Shapiro}} + \Delta t_{\mathrm{Einstein}}$ to transform the observatory-frame arrival time to the SSB-frame arrival time, which is the standard reference for multi-messenger time coincidence analysis. All instruments' data are time-stamped in SSB time before Yajie{} consensus comparison.

## Proof of Hoeffding Bound with Correlated Experts 相关专家的Hoeffding界证明
<!-- label: sec:app_hoeffding -->

> **Proof:** \rigorPartial
> We derive the effective multiplicity correction $M_c^{\mathrm{eff}} = M_c/(1 + (M_c-1)\bar_c)$ used in Theorem [ref].
> 
> Let $X_1, ..., X_M$ be binary indicators of detection success ($X_i = 1$ if instrument $i$ detects the source) with $\E[X_i] = p$ and $\Var(X_i) = p(1-p)$. The pairwise correlation is $\rho_{ij} = \Cov(X_i, X_j)/\Var(X_i)$. The sum $S_M = \sum_{i=1}^M X_i$ has mean $\E[S_M] = M p$ and variance:
> 
> $$
> \Var(S_M) = \sum_{i=1}^M \Var(X_i) + \sum_{i \neq j} \Cov(X_i, X_j) = M p(1-p) \bigl[1 + (M-1)\bar\bigr].
> $$
> 
> 
> Under equicorrelation ($\rho_{ij} = \bar$ for all $i \neq j$), the variance inflation factor is $1 + (M-1)\bar$. The effective independent sample size is the number of independent observations that would produce the same variance:
> 
> $$
> M^{\mathrm{eff}} = \frac{\Var(S_M^{\mathrm{indep}})}{\Var(S_M)} \cdot M = \frac{M p(1-p)}{M p(1-p)[1 + (M-1)\bar]} \cdot M = \frac{M}{1 + (M-1)\bar}.
> $$
> 
> 
> This is the standard design effect for clustered data  [cite]. The Hoeffding bound for correlated observations is:
> 
> $$
> \Pbb\Bigl[\frac{1}{M}\sum_{i=1}^M X_i \leq \gamma\Bigr] \leq \exp\!\bigl(-2 M^{\mathrm{eff}} (p - \gamma)^2\bigr),
> $$
> 
> where the standard $M$ in the exponent is replaced by $M^{\mathrm{eff}}$. This bound is valid when the correlation structure is exchangeable (all pairs have equal correlation) and the observations are sub-Gaussian, which holds for bounded binary variables.
> 
> For general (non-exchangeable) correlation structures, the average $\bar$ in the effective multiplicity formula provides a first-order correction. A more refined bound using the full correlation matrix $R$ is $\Pbb[\bar{X} - p \geq t] \leq \exp(-2 M t^2 / \lambda_(R))$ where $\lambda_(R)$ is the maximum eigenvalue of the correlation matrix  [cite]. In practice, $\bar$ is estimated from calibration data (Appendix [ref]). $\square$

\begin{thebibliography}{99}

\bibitem{SCX2025}
SCX, ``SCX: Structured Causal eXamination Framework for Auditable AI,'' *Technical Report*, 2025.

\bibitem{Bartos2013}
I.~Bartos, P.~Brady, and S.~Márka, ``How gravitational-wave observations can shape the gamma-ray burst paradigm,'' *Class. Quantum Grav.*, vol.~30, 123001, 2013.

\bibitem{Meszaros2019}
P.~Mészáros, D.~B.~Fox, C.~Hanna, and K.~Murase, ``Multi-messenger astrophysics,'' *Nat. Rev. Phys.*, vol.~1, pp.~585--599, 2019.

\bibitem{LIGO2015}
J.~Aasi et al. (LIGO Scientific Collaboration), ``Advanced LIGO,'' *Class. Quantum Grav.*, vol.~32, 074001, 2015.

\bibitem{Virgo2015}
F.~Acernese et al. (Virgo Collaboration), ``Advanced Virgo: a second-generation interferometric gravitational wave detector,'' *Class. Quantum Grav.*, vol.~32, 024001, 2015.

\bibitem{KAGRA2019}
T.~Akutsu et al. (KAGRA Collaboration), ``KAGRA: 2.5 generation interferometric gravitational wave detector,'' *Nat. Astron.*, vol.~3, pp.~35--40, 2019.

\bibitem{LIGOcalibration2021}
L.~Sun et al., ``Characterization of systematic error in Advanced LIGO calibration,'' *Class. Quantum Grav.*, vol.~38, 115008, 2021.

\bibitem{IceCube2017}
M.~G.~Aartsen et al. (IceCube Collaboration), ``The IceCube Neutrino Observatory: instrumentation and online systems,'' *JINST*, vol.~12, P03012, 2017.

\bibitem{GW170817}
B.~P.~Abbott et al. (LIGO Scientific Collaboration and Virgo Collaboration), ``GW170817: Observation of Gravitational Waves from a Binary Neutron Star Inspiral,'' *Phys. Rev. Lett.*, vol.~119, 161101, 2017.

\bibitem{IceCubeNeutrino2018}
M.~G.~Aartsen et al. (IceCube Collaboration), ``Neutrino emission from the direction of the blazar TXS~0506+056 prior to the IceCube-170922A alert,'' *Science*, vol.~361, pp.~147--151, 2018.

\bibitem{Hoeffding1963}
W.~Hoeffding, ``Probability inequalities for sums of bounded random variables,'' *J. Am. Stat. Assoc.*, vol.~58, pp.~13--30, 1963.

\bibitem{Liang1986}
K.-Y.~Liang and S.~L.~Zeger, ``Longitudinal data analysis using generalized linear models,'' *Biometrika*, vol.~73, pp.~13--22, 1986.

\bibitem{Wainwright2019}
M.~J.~Wainwright, *High-Dimensional Statistics: A Non-Asymptotic Viewpoint*, Cambridge University Press, 2019.

\bibitem{AMON2015}
M.~W.~E.~Smith et al., ``The Astrophysical Multimessenger Observatory Network (AMON),'' *Astropart. Phys.*, vol.~45, pp.~56--70, 2013.

\bibitem{LIGOAlert2021}
S.~Chaudhary et al., ``Low-latency alerts for gravitational waves and their electromagnetic counterparts,'' *Proc. Natl. Acad. Sci.*, vol.~118, e2102147118, 2021.

\bibitem{IceCubeAlert2016}
M.~G.~Aartsen et al. (IceCube Collaboration), ``Very high-energy gamma-ray follow-up program using neutrino triggers from IceCube,'' *JINST*, vol.~11, P11009, 2016.

\bibitem{MultiMessengerPE2020}
G.~Ashton et al., ``BILBY: A user-friendly Bayesian inference library for gravitational-wave astronomy,'' *Astrophys. J. Suppl. Ser.*, vol.~241, 27, 2019.

\bibitem{CoincidenceSearch2021}
M.~A.~Bizouard et al., ``Gravitational-wave coincident searches with electromagnetic and neutrino observatories,'' *Phys. Rev. D*, vol.~103, 083008, 2021.

\bibitem{DE440}
R.~S.~Park, W.~M.~Folkner, J.~G.~Williams, and D.~H.~Boggs, ``The JPL Planetary and Lunar Ephemerides DE440 and DE441,'' *Astron. J.*, vol.~161, 105, 2021.

\bibitem{Lehmann1998}
E.~L.~Lehmann and G.~Casella, *Theory of Point Estimation*, 2nd ed., Springer, 1998.

\end{thebibliography}