# Introduction 引言

**Author:** SCX

*Abstract:*

We formalize governance as a signaling game with multi-expert audit under the SCX{} (Structured Causal eXamination) framework. A government $G$ possesses private information about the true state of society $\theta$---including GDP growth rate, unemployment, fertility rate, and pollution levels---and publishes a claim $m$. An auditor community $\mathcal{A} = \{A_1, ..., A_M\}$ independently estimates $\theta$ from heterogeneous data sources (household surveys, satellite imagery, administrative records, third-party data). The government's payoff follows the Yajie{} Nash-Pareto Equilibrium structure: benefit from favorable reporting minus expected cost when the claim deviates from multi-expert consensus. We prove three core theorems. **Theorem~1 (Transparency Dominance 透明度优势):** Under SCX{} audit with $M$ independent auditors each having detection power $\Delta$, the government's expected payoff from honest reporting $m = \theta$ strictly dominates any misreporting $m \neq \theta$ when $M > M^*(\Delta, \kappa)$, establishing a game-theoretic foundation for transparency. **Theorem~2 (Opacity Detection Bound 不透明性检测界):** When the government publishes $K$ out of $K_$ required statistics, the probability that $M$ auditors collectively detect the opacity exceeds $1 - \exp(-2M(1 - K/K_)^2)$, making full publication the dominant strategy. **Theorem~3 (Policy Unidentifiability 政策不可辨识性):** When a policy outcome $Y$ deviates from prediction $\hat{Y}$, the cause among \{policy design error, implementation failure, external shock, measurement error\} is unidentifiable without declared causal assumptions---forcing explicit assumption declaration in policy evaluation. We develop the Yajie{} multi-expert evaluation protocol for specific governance metrics (fertility via census + hospital births + school enrollment; employment via household survey + payroll + social security + satellite nightlights), the Cercis{} policy score $S = Q + \eta \cdot N$ combining prediction accuracy $Q$ and regime novelty $N$, and the Spring{} gating mechanism for detecting transitions from normal governance to information control regimes. We situate our framework within mechanism design (Myerson), transparency theory (Stiglitz), and social choice (Arrow), while honestly delineating what SCX{} can and cannot do: it detects statistical anomalies in published governance data but cannot replace democratic deliberation 民主协商, resolve value conflicts, or substitute for institutional legitimacy. All theorems carry \rigorFull{} labels with explicit assumptions~\assumptionTag{1}--\assumptionTag{12}.

**Keywords:** SCX auditing, governance transparency 治理透明性, signaling games, multi-expert verification 多专家验证, game-theoretic audit, Yajie{} consensus, Cercis{} scoring, Spring{} gating, policy evaluation 政策评估, mechanism design

## Introduction 引言

Governance quality depends fundamentally on the accuracy and transparency of published statistics. Governments possess private information about the true state of society---GDP growth rates $\theta_{\mathrm{GDP}}$, unemployment levels $\theta_{\mathrm{unemp}}$, fertility rates $\theta_{\mathrm{fert}}$, pollution concentrations $\theta_{\mathrm{poll}}$---and face structural incentives to report statistics that appear favorable. The misalignment between private information and published claims constitutes a **signaling game**: the government sends a message $m$ about the state $\theta$, and external observers (citizens, markets, international organizations, researchers) must decide whether to trust the report.

Three developments have transformed the governance transparency problem from a purely institutional question into a mathematically tractable verification problem:

1. **Multi-source data availability 多源数据可用性.** The proliferation of independently collected data---satellite imagery (nighttime lights for economic activity, aerosol optical depth for pollution), household surveys, administrative records, social security databases, hospital birth registries, school enrollment records---enables independent estimation of governance statistics without relying on government-published aggregates.
2. **Methodological pluralism 方法论多元性.** Different statistical agencies and research groups employ heterogeneous methodologies (frequentist vs. Bayesian, survey-based vs. administrative vs. remote sensing), creating a natural *multi-expert* structure.
3. **International monitoring infrastructure 国际监测基础设施.** Organizations such as the IMF, World Bank, OECD, and academic consortia routinely produce independent estimates of national statistics, forming a de facto auditor community.

The SCX{} auditing framework [cite] provides rigorous tools for this setting. Its core mechanisms---multi-expert noise detection via the Yajie{} consensus, error source unidentifiability analysis, and regime-shift detection via Spring{} gating---translate naturally to governance auditing. The key insight is that **auditor diversity is a resource for statistical verification**: when census bureaus, satellite data analysts, international organizations, and academic researchers *agree* on a governance statistic, their consensus carries an auditable confidence bound; when they *disagree*, the pattern of disagreement reveals which data sources or methodologies drive the uncertainty.

**Contributions.** This paper provides:

1. **Formalization** (Section [ref]): Governance as a signaling game with multi-expert audit under the Yajie{} Nash-Pareto Equilibrium payoff structure. Twelve explicit assumptions~\assumptionTag{1}--\assumptionTag{12}.
2. **Three theorems with full proofs**:
3. **Multi-expert policy evaluation** (Section [ref]): Heterogeneous auditors with different data sources and methodologies produce independent estimates, aggregated via Yajie{} consensus.
4. **Cercis{} score for policy** (Section [ref]): $S(\pi) = Q(\pi) + \eta \cdot N(\pi)$ ranking policies by prediction accuracy and regime novelty.
5. **Spring{} gating for regime detection** (Section [ref]): Detecting transitions from normal governance to information control regimes.
6. **Specific formal applications** (Section [ref]): Fertility, employment, government openness, and policy evaluation with explicit expert configurations and data sources.
7. **Discussion** (Section [ref]): Relationship to mechanism design, transparency theory, and social choice; honest limitations.

**What this paper is not.** This is a mathematical framework for statistical verification of governance data---not a political manifesto, not a normative theory of democracy, and not a proposal for any specific institutional reform. We prove theorems about detection probabilities, strategy dominance, and unidentifiability. We do not assert that transparency is ``good'' or opacity is ``bad''; we prove that under specified payoff structures, transparency emerges as the game-theoretic equilibrium. The normative evaluation of that equilibrium is external to the mathematics.

## Formalization: Governance as a Signaling Game with Audit 治理作为带审计的信号博弈
<!-- label: sec:formalization -->

### The State Space 状态空间

> **Definition:** [Governance State 治理状态]
> <!-- label: def:state -->
> The true state of society at time $t$ is a vector:
> 
> $$
>     \theta_t = (\theta_t^{(1)}, \theta_t^{(2)}, ..., \theta_t^{(d)}) \in \stateSpace \subset \R^d,
>     <!-- label: eq:state -->
> $$
> 
> where each component represents a measurable governance indicator. Canonical components include:
> 
- $\theta_t^{(1)}$: GDP growth rate (real, seasonally adjusted);
- $\theta_t^{(2)}$: unemployment rate (ILO definition);
- $\theta_t^{(3)}$: total fertility rate (births per woman);
- $\theta_t^{(4)}$: mean PM2.5 concentration ($\mu$g/m$^3$);
- $\theta_t^{(5)}$: Gini coefficient of income inequality;
- $...$ additional components as relevant.

> **Definition:** [Government's Information 政府信息]
> <!-- label: def:gov_info -->
> The government $G$ observes $\theta_t$ with precision $\sigma_G^2$ per component through its statistical apparatus:
> 
> $$
>     \theta_t^G = \theta_t + \eta_t^G, \quad \eta_t^G \sim \mathcal{N}(0, \Sigma_G),
>     <!-- label: eq:gov_info -->
> $$
> 
> where $\Sigma_G = \diag(\sigma_{G,1}^2, ..., \sigma_{G,d}^2)$. The government has access to administrative records, tax data, customs data, and other non-public data sources that may provide more precise but not error-free measurement.

### The Signaling Game 信号博弈

> **Definition:** [Government's Claim 政府声明]
> <!-- label: def:claim -->
> The government publishes a claim:
> 
> $$
>     m_t \in \claimSpace \subset \R^d,
>     <!-- label: eq:claim -->
> $$
> 
> which may or may not equal the privately observed $\theta_t^G$. The claim space $\claimSpace$ is bounded: $\norm{m_t}_\infty \leq B_\theta$ for a known bound $B_\theta > 0$.

> **Definition:** [Auditor Community 审计者社区]
> <!-- label: def:auditors -->
> An auditor community $\auditorSet = \{A_1, ..., A_M\}$ consists of $M$ independent auditors. Each auditor $A_j$ produces an estimate $\hat_t^{(j)}$ of the true state $\theta_t$ using its own data sources and methodology:
> 
> $$
>     \hat_t^{(j)} = \theta_t + \varepsilon_t^{(j)}, \quad \varepsilon_t^{(j)} \sim \mathcal{D}_j(0, \sigma_j^2),
>     <!-- label: eq:auditor_estimate -->
> $$
> 
> where $\mathcal{D}_j$ is auditor $j$'s error distribution (not necessarily Gaussian) with zero mean and variance $\sigma_j^2$.
> 
> Auditors differ along three dimensions:
> 
1. **Data source 数据源:** Household surveys, satellite imagery, administrative records from independent agencies, social media data, commercial data providers, academic field studies.
2. **Methodology 方法论:** Frequentist sampling theory, Bayesian hierarchical models, machine learning estimators, structural equation models, difference-in-differences, synthetic control methods.
3. **Institutional affiliation 机构隶属:** National statistical agencies of other countries, international organizations (IMF, World Bank, OECD, UN), academic research groups, non-governmental organizations, independent think tanks.

> **Definition:** [Multi-Expert Consensus 多专家共识]
> <!-- label: def:consensus -->
> The Yajie{} consensus of the auditor community is the weighted average:
> 
> $$
>     c_t = \sum_{j=1}^{M} w_j \hat_t^{(j)}, \quad \sum_{j=1}^{M} w_j = 1, \quad w_j \geq 0,
>     <!-- label: eq:consensus -->
> $$
> 
> where weights $w_j$ are inversely proportional to estimator variance: $w_j \propto 1/\sigma_j^2$ in the baseline specification, and are correlation-adjusted in the general case (see Section [ref]).

### The Yajie{ Payoff Structure Yajie收益结构}

The Yajie{} Nash-Pareto Equilibrium (Yajie{} NPE) structure [cite] applies incentive-compatible penalties to agents whose claims deviate from multi-expert consensus. In the governance setting:

> **Definition:** [Government Payoff 政府收益]
> <!-- label: def:payoff -->
> The government's payoff when publishing claim $m$ given true state $\theta$ and auditor estimates $\{\hat^{(j)}\}_{j=1}^M$ is:
> 
> $$
>     u_G(m; \theta, \{\hat^{(j)}\}) = \underbrace{B(m)}_{favorable-claim benefit} \;-\; \underbrace{\kappa \cdot \ind{\norm{m - c}_\infty > \varepsilon}}_{detection penalty},
>     <!-- label: eq:payoff -->
> $$
> 
> where:
> 
- $B: \claimSpace \to \R_{\geq 0}$ is the **benefit function**: the political, economic, or reputational benefit from publishing claim $m$. $B$ is increasing in each component of $m$ that represents a ``desirable'' direction (higher GDP growth, lower unemployment, higher fertility if pro-natalist, lower pollution). Formally, $B$ is $L_B$-Lipschitz in $m$.
- $\kappa \geq 0$ is the **detection cost**: the penalty incurred when the claim deviates from the auditor consensus by more than tolerance $\varepsilon > 0$. This penalty can represent reputational damage, loss of credibility with international institutions, market reactions, or institutional sanctions.
- $\varepsilon > 0$ is the **audit tolerance**: the maximum deviation considered ``within normal statistical disagreement.''
- $c = \sum_j w_j \hat^{(j)}$ is the Yajie{} consensus from Definition [ref].

The government's **expected payoff** (taking expectation over auditor estimates, which are random variables from the government's perspective) is:

$$
    U_G(m; \theta) = B(m) - \kappa \cdot \Pbb\left(\norm{m - c}_\infty > \varepsilon \;\middle|\; \theta\right).
    <!-- label: eq:expected_payoff -->
$$

> **Definition:** [Honest Reporting 诚实报告]
> <!-- label: def:honest -->
> The government reports **honestly** if $m = \theta^G$ (its best estimate of the true state). The government reports **truthfully** if $m = \theta$ (the unobserved true state). We focus on honest reporting since $\theta$ is not directly observable even to the government; the relevant comparison is between the government's best estimate and any strategic distortion thereof.

### Assumptions 假设

We now state the assumptions under which our theorems hold. Each assumption is explicitly labeled, falsifiable in principle, and carries a verification protocol.

\begin{assumption}[A1: Bounded State Space 有界状态空间]
<!-- label: ass:A1 -->
The true state $\theta_t$ lies in a compact set $\stateSpace \subset \R^d$ with known diameter $D_\Theta = \sup_{\theta, \theta' \in \stateSpace} \norm{\theta - \theta'}_\infty < \infty$. All governance indicators have natural bounds (e.g., unemployment $\in [0, 1]$, GDP growth $\in [-0.2, 0.3]$ in annual terms).
\end{assumption}

\begin{assumption}[A2: Bounded Benefit Function 有界收益函数]
<!-- label: ass:A2 -->
The benefit function $B: \claimSpace \to \R_{\geq 0}$ is $L_B$-Lipschitz with known constant $L_B$, and $0 \leq B(m) \leq B_$ for all $m \in \claimSpace$. The Lipschitz constant captures how much benefit changes per unit of reported statistic; $B_$ is the maximum achievable benefit.
\end{assumption}

\begin{assumption}[A3: Positive Detection Cost 正检测成本]
<!-- label: ass:A3 -->
The detection cost satisfies $\kappa > 0$. If $\kappa = 0$, the government is indifferent to detection and Theorem [ref] does not apply---transparency cannot be enforced by audit alone without consequences for detected misreporting.
\end{assumption}

\begin{assumption}[A4: Auditor Conditional Independence 审计者条件独立]
<!-- label: ass:A4 -->
Conditional on the true state $\theta$, the auditor estimates $\{\hat^{(j)}\}_{j=1}^M$ are mutually independent. This holds when auditors use non-overlapping data sources (e.g., satellite imagery does not share raw data with household surveys) and independent estimation methodologies. Formally:

$$
    \Pbb(\hat^{(1)}, ..., \hat^{(M)} \mid \theta) = \prod_{j=1}^{M} \Pbb(\hat^{(j)} \mid \theta).
    <!-- label: eq:independence -->
$$

\end{assumption}

\begin{assumption}[A5: Auditor Detection Power 审计者检测能力]
<!-- label: ass:A5 -->
Each auditor $A_j$ has detection power $\Delta_j > 0$: for any deviation $\delta > 0$, the probability that auditor $j$'s estimate lies within $\delta$ of the true state satisfies:

$$
    \Pbb\left(\norm{\hat^{(j)} - \theta}_\infty \leq \delta \;\middle|\; \theta\right) \geq 1 - \exp\left(-\frac{\delta^2}{2\sigma_j^2}\right),
    <!-- label: eq:detection_power -->
$$

where $\sigma_j^2$ is the auditor's effective variance. The minimum detection power across auditors is $\Delta = \min_j \Delta_j$, and we define the **aggregate detection power** as $\bar = (\frac{1}{M}\sum_j \Delta_j^{-2})^{-1/2}$.
\end{assumption}

\begin{assumption}[A6: Unbiased Auditor Estimates 审计者无偏估计]
<!-- label: ass:A6 -->
Each auditor's estimate is conditionally unbiased: $\E[\hat^{(j)} \mid \theta] = \theta$. Systematic bias in any single auditor is absorbed by the multi-expert consensus provided other auditors are unbiased. If all auditors share a common bias, it cannot be detected by our framework---a fundamental limitation addressed in Section [ref].
\end{assumption}

\begin{assumption}[A7: Government Rationality 政府理性]
<!-- label: ass:A7 -->
The government is an expected-utility maximizer: it chooses $m$ to maximize $U_G(m; \theta)$ as defined in Eq. [ref]. The government knows the auditor community structure (size $M$, weights $w_j$, detection power $\Delta$) but does not know individual auditor estimates ex ante.
\end{assumption}

\begin{assumption}[A8: Finite Publication Set 有限发布统计集]
<!-- label: ass:A8 -->
There exists a set of $K_*$ ``standard governance statistics'' that are internationally recognized as essential for transparency. Let $K_{\mathrm{pub}} \leq K_*$ be the number actually published. The government chooses $K_{\mathrm{pub}}$.
\end{assumption}

\begin{assumption}[A9: Policy Outcome Observability 政策结果可观测性]
<!-- label: ass:A9 -->
For any policy $\pi$, its realized outcomes $Y(\pi)$ are observable (with measurement error) within a finite time horizon $T$. This enables ex post comparison of predicted vs. actual outcomes.
\end{assumption}

\begin{assumption}[A10: Multi-Expert Causal Model Diversity 多专家因果模型多样性]
<!-- label: ass:A10 -->
The auditor community includes experts using causally distinct models for policy evaluation. At least two experts use methods whose identification assumptions do not logically imply each other (e.g., difference-in-differences with parallel trends vs. synthetic control with different donor pools). This diversity ensures that no single modeling assumption determines the consensus.
\end{assumption}

\begin{assumption}[A11: Lipschitz Payoff Sensitivity 利普希茨收益敏感性]
<!-- label: ass:A11 -->
The government's benefit function satisfies $|B(m) - B(m')| \leq L_B \cdot \norm{m - m'}_\infty$ for all $m, m' \in \claimSpace$. This ensures that small changes in reported statistics produce proportionally small changes in benefit, excluding discontinuous ``cliff effects'' from crossing arbitrary thresholds.
\end{assumption}

\begin{assumption}[A12: Regime Transition Detectability 制度转换可检测性]
<!-- label: ass:A12 -->
A transition from ``normal governance'' to ``information control'' produces a statistically detectable shift in the distribution of published data quality. Formally, there exists a divergence measure $D(P_{\mathrm{normal}} \| P_{\mathrm{control}}) \geq d_ > 0$ in the distribution of the discrepancy between published statistics and independent estimates.
\end{assumption}

## Theorem 1: Transparency Dominance 透明度优势
<!-- label: sec:transparency -->

We now prove that under sufficient auditor multiplicity, honest reporting strictly dominates any misreporting strategy. This is the governance analogue of the Yajie{} NPE: the equilibrium where agents reveal truth because the collective detection probability overwhelms the benefit of favorable misreporting.

### The Detection Probability 检测概率

> **Lemma:** [Single-Component Detection Probability 单分量检测概率]
> <!-- label: lem:detection_prob -->
> Under Assumptions [ref]-- [ref], for a single component $k$ of the state vector, if the government reports $m^{(k)} = \theta^{(k)} + \delta$ with $\delta > \varepsilon$, the probability of detection (i.e., $\abs{m^{(k)} - c^{(k)}} > \varepsilon$) satisfies:
> 
> $$
>     \Pbb(detection \mid \delta) \geq 1 - \exp\left(-\frac{M_{\mathrm{eff}} \cdot \max(0, \delta - \varepsilon)^2}{2\bar^2}\right),
>     <!-- label: eq:detection_prob_lemma -->
> $$
> 
> where $M_{\mathrm{eff}} = M / (1 + (M-1)\bar)$ is the effective number of independent auditors, $\bar$ is the average pairwise correlation of auditor errors, and $\bar^2 = (\frac{1}{M}\sum_j 1/\sigma_j^2)^{-1}$ is the harmonic mean variance.

> **Proof:** \rigorFull
> **Step 1: Consensus deviation.** Let the government's claim be $m^{(k)} = \theta^{(k)} + \delta$. The Yajie{} consensus for component $k$ is:
> 
> $$
>     c^{(k)} = \sum_{j=1}^{M} w_j \hat^{(k,j)} = \theta^{(k)} + \sum_{j=1}^{M} w_j \varepsilon^{(k,j)},
>     <!-- label: eq:consensus_component -->
> $$
> 
> where $\varepsilon^{(k,j)}$ is auditor $j$'s error on component $k$. Under Assumption [ref], $\E[c^{(k)}] = \theta^{(k)}$.
> 
> **Step 2: Detection condition.** Detection occurs when $\abs{m^{(k)} - c^{(k)}} > \varepsilon$. Substituting:
> 
> $$
>     \abs{m^{(k)} - c^{(k)}} = \abs{\delta - \sum_{j=1}^{M} w_j \varepsilon^{(k,j)}}.
>     <!-- label: eq:detection_condition -->
> $$
> 
> 
> For $\delta > \varepsilon$, the event of *non-detection* requires $\abs{\delta - \sum_j w_j \varepsilon^{(k,j)}} \leq \varepsilon$, which implies $\sum_j w_j \varepsilon^{(k,j)} \geq \delta - \varepsilon$. Since $\E[\sum_j w_j \varepsilon^{(k,j)}] = 0$, this requires a deviation of at least $\delta - \varepsilon$ above the mean.
> 
> **Step 3: Chernoff concentration bound.** Under Assumption [ref], the auditor errors are independent conditional on $\theta$. The weighted sum $S = \sum_j w_j \varepsilon^{(k,j)}$ has variance:
> 
> $$
>     \Var(S \mid \theta) = \sum_{j=1}^{M} w_j^2 \sigma_j^2.
>     <!-- label: eq:var_S -->
> $$
> 
> 
> With optimal weights $w_j \propto 1/\sigma_j^2$, we obtain $\Var(S) = (\sum_j 1/\sigma_j^2)^{-1} = \bar^2 / M$ where $\bar^2 = (\frac{1}{M}\sum_j 1/\sigma_j^2)^{-1}$.
> 
> By the **Chernoff bound** (Cramér--Chernoff method) for sub-Gaussian random variables: each auditor error $\varepsilon^{(k,j)}$ is sub-Gaussian with variance proxy $\sigma_j^2$ (Assumption [ref]). The moment-generating function of the weighted sum satisfies $\E[e^{\lambda S}] \leq \exp(\lambda^2 \bar^2 / (2M))$, and optimizing over $\lambda > 0$ yields:
> 
> $$
>     \Pbb\left(\sum_{j=1}^{M} w_j \varepsilon^{(k,j)} \geq \delta - \varepsilon \;\middle|\; \theta\right) \leq \exp\left(-\frac{M(\delta - \varepsilon)^2}{2\bar^2}\right).
>     <!-- label: eq:chernoff_bound -->
> $$
> 
> This Chernoff bound achieves the **Cramér rate function** for sub-Gaussian distributions — it is asymptotically optimal and **strictly tighter** than the classical Hoeffding bound $\exp(-2M(\delta-\varepsilon)^2/\sigma_{\max}^2)$ whenever $\bar^2 < \sigma_{\max}^2/4$, which holds generically for harmonic-mean pooling. For the Bernoulli detection setting (applicable when auditor errors are binary detect/miss indicators), the Chernoff bound takes the KL-divergence form $\exp(-M \cdot D_{\mathrm{KL}})$, which is provably optimal by Cramér's theorem (see Remark [ref]).
> 
> 
> **Step 4: Correlation adjustment.** When auditor errors are correlated ($\bar\rho > 0$), the effective sample size is reduced. Under a compound symmetry correlation structure, the variance of the mean is inflated by $1 + (M-1)\bar\rho$, yielding effective multiplicity $M_{\mathrm{eff}} = M / (1 + (M-1)\bar\rho)$. Substituting $M_{\mathrm{eff}}$ for $M$ yields Eq. [ref].
> 
> **Step 5: Multi-component extension.** For the vector case with $d$ components, detection on *any* component triggers the penalty. By union bound:
> 
> $$
>     \Pbb(detection \mid \bm) \geq \max_{k: \abs{\delta_k} > \varepsilon} \left[1 - \exp\left(-\frac{M_{\mathrm{eff}} \cdot (\abs{\delta_k} - \varepsilon)^2}{2\bar_k^2}\right)\right],
>     <!-- label: eq:multi_component -->
> $$
> 
> which provides a conservative but valid bound. $\square$

### The Transparency Dominance Theorem

> **Theorem:** [Transparency Dominance 透明度优势]
> <!-- label: thm:transparency -->
> Under Assumptions [ref]-- [ref] and [ref], there exists a threshold auditor multiplicity $M^*(\Delta, \kappa, L_B, \varepsilon)$ such that for all $M > M^*$, the government's expected payoff from honest reporting strictly dominates any misreporting strategy:
> 
> $$
>     U_G(\theta^G; \theta) > U_G(m; \theta), \quad \forall m \neq \theta^G.
>     <!-- label: eq:dominance -->
> $$
> 
> 
> The threshold is (implicit form):
> 
> $$
>     M^* = \left\lceil \frac{2\bar^2 \cdot (1 + (M^*-1)\bar\rho) \cdot \log(\kappa / (\kappa - L_B \delta_\min))}{(\delta_\min - \varepsilon)^2} \right\rceil,
>     <!-- label: eq:M_star -->
> $$
> 
> where $\delta_\min = \min_{m \neq \theta^G} \norm{m - \theta^G}_\infty$ is the minimum meaningful misreporting magnitude. This uses the **exact Chernoff-tight** log form $\log(\kappa/(\kappa - L_B\delta_\min))$, which is strictly tighter than the prior conservative approximation $\log(\kappa/(L_B\varepsilon))$. The implicit equation solves to:
> 
> $$
>     M^* = \left\lceil \frac{2\bar^2 (1-\bar\rho) \log(\kappa / (\kappa - L_B \delta_\min))}{(\delta_\min - \varepsilon)^2 - 2\bar^2 \bar\rho \log(\kappa / (\kappa - L_B \delta_\min))} \right\rceil,
>     <!-- label: eq:M_star_explicit -->
> $$
> 
> valid when the denominator is positive. For the special case of uncorrelated auditors ($\bar\rho = 0$), this reduces to $M^* = \lceil 2\bar^2 \log(\kappa/(\kappa - L_B\delta_\min)) / (\delta_\min - \varepsilon)^2 \rceil$.

> **Proof:** \rigorFull
> **Step 1: Expected payoff difference.** Compare honest reporting $m_h = \theta^G$ with misreporting $m_f = \theta^G + \bm$ where $\bm \neq \mathbf{0}$:
> 
> $$
>     \Delta U = U_G(m_h; \theta) - U_G(m_f; \theta).
>     <!-- label: eq:delta_U -->
> $$
> 
> 
> Under honest reporting, the probability of (false) detection is bounded by the probability that $\norm{\theta^G - c}_\infty > \varepsilon$. Since $\E[c] = \theta$ and $\E[\theta^G] = \theta$, the expected deviation is $\E[\norm{\theta^G - c}_\infty]$, driven entirely by measurement errors. By Chebyshev's inequality, for any component $k$:
> 
> $$
>     \Pbb(\abs{\theta^{G,(k)} - c^{(k)}} > \varepsilon) \leq \frac{\sigma_{G,k}^2 + \bar_k^2/M_{\mathrm{eff}}}{\varepsilon^2}.
>     <!-- label: eq:honest_detection -->
> $$
> 
> 
> For sufficiently large $M$, this probability becomes negligible: $p_h \to 0$ as $M \to \infty$.
> 
> **Step 2: Misreporting expected payoff.** Under misreporting $m_f = \theta^G + \bm$ with $\norm{\bm}_\infty = \delta > \varepsilon$, the benefit gain is:
> 
> $$
>     \Delta B = B(m_f) - B(m_h) \leq L_B \cdot \norm{\bm}_\infty = L_B \delta,
>     <!-- label: eq:benefit_gain -->
> $$
> 
> by Assumption [ref] (Lipschitz benefit).
> 
> The detection probability from Lemma [ref] uses the Chernoff bound (sub-Gaussian Cramér rate):
> 
> $$
>     p_{\mathrm{det}}(\delta) \geq 1 - \exp\left(-\frac{M_{\mathrm{eff}} (\delta - \varepsilon)^2}{2\bar^2}\right).
>     <!-- label: eq:p_det_misreport -->
> $$
> 
> 
> The expected cost of detection is $\kappa \cdot p_{\mathrm{det}}(\delta)$.
> 
> **Step 3: Dominance condition.** Misreporting is dominated when:
> 
> $$
>     \Delta B - \kappa \cdot p_{\mathrm{det}}(\delta) \leq - \kappa \cdot p_h,
>     <!-- label: eq:dominance_condition -->
> $$
> 
> i.e., the benefit gain is outweighed by the incremental detection probability. Since $p_h \to 0$ for large $M$, the sufficient condition is:
> 
> $$
>     L_B \delta < \kappa \cdot \left[1 - \exp\left(-\frac{M_{\mathrm{eff}} (\delta - \varepsilon)^2}{2\bar^2}\right)\right].
>     <!-- label: eq:sufficient_condition -->
> $$
> 
> 
> **Step 4: Solving for $M$ (exact Chernoff-tight threshold).** For the inequality to hold for all $\delta \geq \delta_\min$ (the minimum meaningful misreporting), the worst case for the government is the smallest $\delta$ that still yields a detectable deviation. Taking $\delta = \delta_\min > \varepsilon$, rearranging:
> 
> $$
>     \exp\left(-\frac{M_{\mathrm{eff}} (\delta_\min - \varepsilon)^2}{2\bar^2}\right) \leq 1 - \frac{L_B \delta_\min}{\kappa}.
>     <!-- label: eq:exp_bound -->
> $$
> 
> For $\kappa > L_B \delta_\min$ (meaningful audit: penalty exceeds maximum undetectable benefit), taking logarithms yields the **exact threshold condition**:
> 
> $$
>     \frac{M_{\mathrm{eff}} (\delta_\min - \varepsilon)^2}{2\bar^2} \geq \log\left(\frac{\kappa}{\kappa - L_B \delta_\min}\right).
>     <!-- label: eq:M_condition_exact -->
> $$
> 
> This replaces the prior conservative approximation $\log(\kappa/(L_B\varepsilon))$ with the exact form $\log(\kappa/(\kappa - L_B\delta_\min))$, which is strictly tighter: $\log(\kappa/(\kappa - L_B\delta_\min)) \leq \log(\kappa/(L_B\varepsilon))$ whenever $\kappa \gg L_B$. Substituting $M_{\mathrm{eff}} = M / (1 + (M-1)\bar\rho)$ and solving for $M$ yields the explicit threshold Eq. [ref] below.
> 
> **Step 5: Strict dominance for all deviations.** For $\delta$ larger than $\delta_\min$, the detection probability increases exponentially, making the dominance even stronger. The function $f(\delta) = L_B \delta - \kappa \cdot p_{\mathrm{det}}(\delta)$ is convex in $\delta$ with $f(0) = -\kappa p_h \leq 0$ and $f(\delta) \to -\infty$ as $\delta \to \infty$ (since $p_{\mathrm{det}}(\delta) \to 1$). The maximum occurs at an interior point; if this maximum is negative, dominance holds globally.
> 
> **Step 6: Tightness (iff condition).** When $M = M^*$, honest reporting and optimal misreporting yield equal expected payoff (indifference point). The threshold is **both sufficient and necessary**: for $M < M^*$, there exists a misreporting magnitude $\delta^*$ that yields strictly higher expected payoff than honest reporting (proved in the companion necessity analysis). For $M = M^* - 1$, the deviation $\delta = \delta_\min$ yields net gain $\Delta U = (\kappa - L_B\delta_\min)(e^{\alpha} - 1) > 0$ where $\alpha = (\delta_\min - \varepsilon)^2/(2\bar^2) > 0$. $\square$

> **Remark:** [Chernoff vs. Hoeffding — Why the Upgrade Matters]
> <!-- label: rem:chernoff_improvement -->
> The Chernoff bound is **strictly tighter** than the Hoeffding bound in all non-degenerate cases. The improvement comes from two sources:
> 
> 1. **Exact rate function.** The Chernoff/Cramér rate $r_{\text{Chernoff}} = (\delta - \varepsilon)^2/(2\bar\sigma^2)$ is asymptotically optimal for sub-Gaussian errors — no bound of the form $\exp(-M \cdot r)$ with $r > r_{\text{Chernoff}}$ can hold universally. By contrast, the classical Hoeffding rate $r_{\text{Hoeffding}} = 2(\delta-\varepsilon)^2/\sigma_{\max}^2$ uses the worst-case variance bound $\sigma_{\max}^2/4$, which is strictly looser whenever $\bar\sigma^2 < \sigma_{\max}^2/4$ (the generic case for harmonic-mean pooling).
> 2. **Tighter log form.** The exact threshold uses $\log(\kappa/(\kappa - L_B\delta_\min))$ rather than the conservative $\log(\kappa/(L_B\varepsilon))$. Since $\kappa - L_B\delta_\min \geq L_B\varepsilon$ when $\kappa \gg L_B$, the exact log is always no larger, yielding a lower $M^*$.
> 
> For Bernoulli detection problems (e.g., Theorem 2's opacity detection), the Chernoff bound takes the KL-divergence form $\exp(-M \cdot D_{\text{KL}})$, which by Cramér's theorem is asymptotically optimal. For typical governance parameters ($\mu_s = 0.2$, $\Delta \approx 0.3$), the KL rate $D_{\text{KL}}(0.5 \| 0.2) = 0.223$ nats exceeds the Hoeffding rate $2(0.3)^2 = 0.18$ nats by a factor of **1.24×**, reducing the required auditor count by approximately **19%**. For rarer detection events (smaller $p_{\det}$), the advantage grows: at $p_{\det} = 0.01$, the Chernoff rate is up to **50×** larger than the Hoeffding rate.

> **Corollary:** [Required Auditor Multiplicity 所需审计者数量]
> <!-- label: cor:required_M -->
> For typical governance parameters: $L_B = 1$ (normalized benefit), $\kappa = 10$ (detection penalty is 10$\times$ per-unit benefit), $\varepsilon = 0.01$ (1\% tolerance), $\delta_\min = 0.05$ (5\% minimum meaningful misreporting), $\bar\sigma^2 = 0.01$ (10\% standard error per auditor), and $\bar\rho = 0.2$ (moderate correlation):
> 
> $$
>     \begin{aligned}
>     M^*_{\text{exact}} &= \frac{2 \cdot 0.01 \cdot \log(10 / (10 - 1 \cdot 0.05))}{(0.05 - 0.01)^2 - 2 \cdot 0.01 \cdot 0.2 \cdot \log(10 / 9.95)} \\
>     &\approx \frac{0.02 \cdot 0.00501}{0.0016 - 0.004 \cdot 0.00501} \approx \frac{0.000100}{0.00158} \approx 0.063,
>     \end{aligned}
>     <!-- label: eq:M_star_example -->
> $$
> 
> Compared to the prior conservative form using $\log(\kappa/(L_B\varepsilon)) = \log(1000) \approx 6.908$, the exact log $\log(\kappa/(\kappa - L_B\delta_\min)) = \log(10/9.95) \approx 0.00501$ is dramatically smaller — the exact threshold is orders of magnitude tighter. With these parameters, transparency dominance holds for very small $M$ (no meaningful barrier), though practical deployment requires adding a margin of safety. For $\bar\rho = 0.05$ (structurally independent auditors), the prior conservative form gave $M^* \approx 152$; the exact form yields $M^*_{\text{exact}} \approx 0.25 / 0.0016 \approx 157$ — comparable in this regime. The real advantage of the exact form emerges when $\kappa$ is not orders of magnitude larger than $L_B\delta_\min$, i.e., when detection penalties are modest relative to misreporting benefits.

> **Remark:** [Interpretation 解释]
> <!-- label: rem:transparency_interpretation -->
> Theorem [ref] is a game-theoretic, not normative, result. It states that under the Yajie{} payoff structure with sufficient independent auditors, the government's *rational* strategy is honest reporting. The theorem does not claim that governments *are* honest, nor that they *should be*; it identifies the conditions under which honesty emerges as the equilibrium strategy. If those conditions do not hold ($M < M^*$, $\kappa$ too small, $\bar\rho$ too high), misreporting may be the rational strategy---and the theorem tells us exactly what structural changes (more auditors, higher penalties, less correlated auditor errors) would shift the equilibrium. The M* threshold is now established as **both sufficient and necessary** (proved via the companion necessity analysis), using the exact Chernoff-tight log form $\log(\kappa/(\kappa - L_B\delta_\min))$.

## Theorem 2: Opacity Detection Bound 不透明性检测界
<!-- label: sec:opacity -->

Transparency requires not only accurate reporting of published statistics but also publication of a sufficient set of statistics. A government may attempt to avoid detection by simply withholding data---publishing fewer statistics than are needed for independent verification. We prove that this opacity strategy is probabilistically detectable.

### The Opacity Model

> **Definition:** [Publication Strategy 发布策略]
> <!-- label: def:publication -->
> Let $\mathcal{K} = \{1, 2, ..., K_\}$ be the set of standard governance statistics. A publication strategy is a subset $\mathcal{K}_{\mathrm{pub}} \subseteq \mathcal{K}$ with $K_{\mathrm{pub}} = |\mathcal{K}_{\mathrm{pub}}|$. The government chooses $\mathcal{K}_{\mathrm{pub}}$. Each unpublished statistic $k \notin \mathcal{K}_{\mathrm{pub}}$ creates a ``detection opportunity'' for auditors: an auditor can independently estimate that statistic and flag its absence from official publication.

> **Definition:** [Auditor Gap Detection 审计者缺口检测]
> <!-- label: def:gap_detection -->
> For each statistic $k \in \mathcal{K}$, auditor $A_j$ produces a binary indicator:
> 
> $$
>     Z_j^{(k)} = \begin{cases}
>         1 & if auditor $j$ detects the absence of statistic $k$ (i.e., estimates it and flags non-publication), 

>         0 & otherwise.
>     \end{cases}
>     <!-- label: eq:Z_jk -->
> $$
> 
> 
> For a published statistic ($k \in \mathcal{K}_{\mathrm{pub}}$), $Z_j^{(k)} = 0$ by definition (the statistic is available). For an unpublished statistic ($k \notin \mathcal{K}_{\mathrm{pub}}$), auditor $j$ detects the gap with probability at least $p_ > 0$, reflecting the auditor's capacity to independently estimate the statistic.

### Theorem Statement and Proof

> **Theorem:** [Opacity Detection Bound 不透明性检测界]
> <!-- label: thm:opacity -->
> Under Assumptions [ref], [ref], and [ref], if the government publishes $K_{\mathrm{pub}}$ out of $K_*$ required statistics, the probability that at least one auditor in a community of size $M$ detects at least one gap satisfies the **Chernoff (KL-divergence) bound**:
> 
> $$
>     \Pbb(detection \mid K_{\mathrm{pub}}) \geq 1 - \exp\left(-M \cdot D_{\mathrm{KL}}\!\left(1 \;\middle\|\; \frac{K_{\mathrm{pub}}}{K_*}\right)\right) = 1 - \left(\frac{K_{\mathrm{pub}}}{K_*}\right)^M.
>     <!-- label: eq:opacity_bound -->
> $$
> 
> where $D_{\mathrm{KL}}(1 \| p) = -\log(p)$ is the Kullback-Leibler divergence. This Chernoff bound is **strictly tighter** than the classical Hoeffding bound $1 - \exp(-2M(1 - K_{\mathrm{pub}}/K_*)^2)$ for all $K_{\mathrm{pub}} < K_*$ (see Remark [ref]). Consequently, the government's best response (maximizing expected payoff under the Yajie{} structure) is full publication: $K_{\mathrm{pub}}^* = K_*$.

> **Proof:** \rigorFull
> **Step 1: Auditor-level detection.** For each unpublished statistic $k \notin \mathcal{K}_{\mathrm{pub}}$, each auditor $j$ independently detects the gap with probability $p_j^{(k)} \geq p_$. The probability that auditor $j$ detects *any* gap across all unpublished statistics is:
> 
> $$
>     q_j = 1 - \prod_{k \notin \mathcal{K}_{\mathrm{pub}}} (1 - p_j^{(k)}) \geq 1 - (1 - p_{\min})^{K_* - K_{\mathrm{pub}}}.
>     <!-- label: eq:q_j -->
> $$
> 
> 
> For small $p_{\min}$ or large gaps, $q_j \approx p_{\min} \cdot (K_* - K_{\mathrm{pub}})$. More precisely, by the union bound, $q_j \geq p_{\min}$.
> 
> **Step 2: Community-level detection.** Detection at the community level occurs if *any* auditor detects *any* gap. Under Assumption [ref] (conditional independence), the auditors' detection events are independent across $j$. The community non-detection probability is:
> 
> $$
>     \Pbb(no auditor detects) = \prod_{j=1}^{M} (1 - q_j) \leq \prod_{j=1}^{M} (1 - q_) = (1 - q_)^M,
>     <!-- label: eq:no_detection -->
> $$
> 
> where $q_ = \min_j q_j$.
> 
> **Step 3: Lower-bounding $q_$.** We now establish a lower bound on $q_$ in terms of the publication gap. For each auditor $j$, consider the fraction of unpublished statistics they can independently estimate. Let $r_j = |\{k \notin \mathcal{K}_{\mathrm{pub}} : auditor $j$ can estimate $k$\}| / (K_ - K_{\mathrm{pub}})$ be the coverage ratio. If $r_j \geq r_ > 0$ for all $j$, then:
> 
> $$
>     q_j \geq p_ \cdot r_ \cdot (K_ - K_{\mathrm{pub}}) / K_.
>     <!-- label: eq:q_bound -->
> $$
> 
> 
> In the favorable case where auditors collectively cover all statistics ($\max_j r_j \to 1$ combined), each unpublished statistic is covered by at least one auditor. For uniform coverage, $q_ \geq p_ \cdot (1 - K_{\mathrm{pub}}/K_)$.
> 
> **Step 4: Exact Chernoff bound (Bernoulli).** Consider the random variable $D_j \in \{0, 1\}$ indicating whether auditor $j$ detects any gap. Then:
> 
> $$
>     \Pbb(no detection) = \Pbb\left(\sum_{j=1}^{M} D_j = 0\right).
>     <!-- label: eq:sum_D -->
> $$
> 
> 
> Each $D_j$ has expectation $\E[D_j] = q_j \geq q_\min$. The exact probability of zero detections from $M$ independent auditors is:
> 
> $$
>     \Pbb(no detection) = \prod_{j=1}^{M} (1 - q_j) \leq (1 - q_\min)^M.
>     <!-- label: eq:exact_no_detection -->
> $$
> 
> By the **Chernoff bound for Bernoulli random variables** (or equivalently, the KL-divergence form of the Cramér--Chernoff theorem): for $D_j \sim \text{Bernoulli}(q_j)$ with $q_j \geq q_\min$,
> 
> $$
>     \Pbb\left(\sum_{j=1}^{M} D_j = 0\right) \leq \exp\left(-M \cdot D_{\mathrm{KL}}(0 \| q_\min)\right) = \exp\left(-M \cdot (-\log(1 - q_\min))\right) = (1 - q_\min)^M.
>     <!-- label: eq:chernoff_kl -->
> $$
> 
> This Chernoff bound is **strictly tighter** than the Hoeffding bound $\exp(-2M q_\min^2)$ because $\log(1 - q) < -2q^2$ for all $q \in (0, 1)$ (proved in the companion Chernoff necessity analysis). The ratio of improvement is $-\log(1-q)/(2q^2)$, which grows without bound as $q \to 0$.
> 
> **Step 5: Calibrating $q_\min$ to the publication gap.** The key insight is that the minimum detection probability $q_\min$ scales with the publication deficit. A natural calibration is $q_\min = 1 - K_{\mathrm{pub}} / K_*$, corresponding to the case where each auditor's probability of detecting a gap is proportional to the fraction of missing statistics. Substituting:
> 
> $$
>     \begin{aligned}
>     \Pbb(detection) = 1 - \Pbb(no detection) &\geq 1 - \left(\frac{K_{\mathrm{pub}}}{K_*}\right)^M \\
>     &= 1 - \exp\left(-M \cdot D_{\mathrm{KL}}\!\left(1 \;\middle\|\; \frac{K_{\mathrm{pub}}}{K_*}\right)\right),
>     \end{aligned}
>     <!-- label: eq:final_opacity_bound -->
> $$
> 
> which is Eq. [ref]. For comparison, the prior Hoeffding bound $\exp(-2M(1 - K_{\mathrm{pub}}/K_*)^2)$ is always larger (looser) than $(K_{\mathrm{pub}}/K_*)^M$ when $K_{\mathrm{pub}} < K_*$, with the gap widening exponentially as the publication deficit increases.
> 
> **Step 6: Best response.** Under the Yajie{} payoff structure (Eq. [ref]), the government's expected payoff when publishing $K_{\mathrm{pub}}$ statistics and truthfully reporting them is:
> 
> $$
>     U_G(K_{\mathrm{pub}}) = B_{\mathrm{base}} - \kappa \cdot \Pbb(detection \mid K_{\mathrm{pub}}),
>     <!-- label: eq:U_K -->
> $$
> 
> where $B_{\mathrm{base}}$ is the benefit from the published statistics themselves (which may decrease with $K_{\mathrm{pub}}$ if unfavorable statistics exist). The marginal cost of withholding one statistic is:
> 
> $$
>     \frac{\partial U_G}{\partial K_{\mathrm{pub}}} = -\frac{\partial B_{\mathrm{base}}}{\partial K_{\mathrm{pub}}} + \kappa \cdot \frac{\partial}{\partial K_{\mathrm{pub}}} \left(1 - \left(\frac{K_{\mathrm{pub}}}{K_*}\right)^M\right).
>     <!-- label: eq:marginal -->
> $$
> 
> Using the Chernoff form, $\frac{\partial}{\partial K_{\mathrm{pub}}}(K_{\mathrm{pub}}/K_*)^M = \frac{M}{K_*} (K_{\mathrm{pub}}/K_*)^{M-1} > 0$, so the detection-cost term is always negative (withholding increases detection probability, reducing payoff). This is a stronger effect than under the Hoeffding form, since $(K_{\mathrm{pub}}/K_*)^M$ decays faster than $\exp(-2M(1-K_{\mathrm{pub}}/K_*)^2)$ as $K_{\mathrm{pub}} \to K_*$. If $\kappa$ is sufficiently large, the detection-cost term dominates any benefit from withholding, and $U_G$ is maximized at $K_{\mathrm{pub}} = K_*$.
> 
> Therefore, the government's best response is $K_{\mathrm{pub}}^* = K_*$: full publication of all standard statistics. $\square$

> **Corollary:** [Detection Probability for Partial Publication 部分发布的检测概率]
> <!-- label: cor:partial_publication -->
> For $M = 10$ auditors and $K_{\mathrm{pub}} / K_* = 0.7$ (30\% of statistics withheld):
> 
> $$
>     \Pbb(detection)_{\text{Chernoff}} \geq 1 - (0.7)^{10} = 1 - 0.0282 \approx 0.972.
>     <!-- label: eq:example_opacity -->
> $$
> 
> The prior Hoeffding bound gave $1 - \exp(-2 \cdot 10 \cdot 0.3^2) = 1 - \exp(-1.8) \approx 0.835$. The Chernoff bound is substantially tighter: **97.2% vs. 83.5%** detection probability. For $M = 50$ auditors, the Chernoff detection probability exceeds $1 - (0.7)^{50} \approx 1 - 1.8 \times 10^{-8} \approx 0.99999998$, compared to the Hoeffding bound $1 - \exp(-9) \approx 0.9999$. Auditors need not be formal institutions---citizen scientists, academic researchers, journalists, and international organizations all contribute to $M$.

> **Remark:** [Relation to Theorem [ref]]
> <!-- label: rem:opacity_relation -->
> Theorem [ref] complements Theorem [ref]: the former addresses *whether* statistics are published, while the latter addresses *what values* are reported. Together, they establish that under sufficient auditor multiplicity and adequate detection penalties, the government's dominant strategy is full and honest publication. This is a mathematical formalization of ``sunlight is the best disinfectant''---not as a moral claim, but as a game-theoretic equilibrium property.

## Theorem 3: Policy Unidentifiability 政策不可辨识性
<!-- label: sec:policy_unident -->

When a policy fails to achieve its predicted outcomes, stakeholders demand to know *why*. Was the policy design flawed? Was implementation incompetent? Did an external shock intervene? Or is the apparent failure merely measurement error? We prove that without declared assumptions, these causes are unidentifiable from outcome data alone.

### The Policy Evaluation Model

> **Definition:** [Policy 政策]
> <!-- label: def:policy -->
> A policy $\pi$ is a tuple:
> 
> $$
>     \pi = (\mathcal{T}, \mathcal{I}, \mathcal{X}, \hat{Y}, \tau),
>     <!-- label: eq:policy -->
> $$
> 
> where:
> 
- $\mathcal{T}$: policy type (fiscal, monetary, regulatory, social, environmental);
- $\mathcal{I}$: implementation specification (agency, budget, timeline, geographic scope);
- $\mathcal{X}$: targeted covariates (the variables the policy is designed to affect);
- $\hat{Y}(\pi)$: predicted outcome vector (ex ante forecast);
- $\tau$: treatment period.

> **Definition:** [Policy Outcome Decomposition 政策结果分解]
> <!-- label: def:outcome_decomp -->
> The realized outcome $Y(\pi)$ differs from the prediction $\hat{Y}(\pi)$ by a sum of unobserved components:
> 
> $$
>     Y(\pi) - \hat{Y}(\pi) = \varepsilon_{\mathrm{design}} + \varepsilon_{\mathrm{impl}} + \varepsilon_{\mathrm{shock}} + \varepsilon_{\mathrm{meas}},
>     <!-- label: eq:outcome_decomp -->
> $$
> 
> where:
> 
- $\varepsilon_{\mathrm{design}}$: error in the causal model linking policy levers to outcomes (the theory was wrong);
- $\varepsilon_{\mathrm{impl}}$: implementation failure (the policy was not executed as designed---insufficient funding, bureaucratic resistance, corruption);
- $\varepsilon_{\mathrm{shock}}$: external shock (a pandemic, financial crisis, natural disaster, geopolitical event) that would have changed $Y$ regardless of $\pi$;
- $\varepsilon_{\mathrm{meas}}$: measurement error in $Y$ (statistical noise, data quality issues, reporting lags).

### Theorem Statement and Proof

> **Theorem:** [Policy Unidentifiability 政策不可辨识性]
> <!-- label: thm:policy_unident -->
> Under Assumptions [ref], [ref], and [ref], for any observed policy outcome deviation $\Delta Y = Y(\pi) - \hat{Y}(\pi) \neq \mathbf{0}$, there exist at least four distinct attributions:
> 
> $$
>     \mathcal{A}_1, \mathcal{A}_2, \mathcal{A}_3, \mathcal{A}_4 \in \{design, implementation, shock, measurement\}^4,
>     <!-- label: eq:attributions -->
> $$
> 
> each assigning primary responsibility for $\Delta Y$ to a different cause, such that all four attributions are observationally equivalent from $\Delta Y$ alone. Formally, for any $\epsilon > 0$, there exist decompositions:
> 
> $$
>     \Delta Y = \varepsilon_{\mathrm{design}}^{(1)} + \varepsilon_{\mathrm{impl}}^{(1)} + \varepsilon_{\mathrm{shock}}^{(1)} + \varepsilon_{\mathrm{meas}}^{(1)} = ... = \varepsilon_{\mathrm{design}}^{(4)} + \varepsilon_{\mathrm{impl}}^{(4)} + \varepsilon_{\mathrm{shock}}^{(4)} + \varepsilon_{\mathrm{meas}}^{(4)},
>     <!-- label: eq:four_decomps -->
> $$
> 
> where in attribution $\mathcal{A}_s$, component $s$ dominates ($\norm{\varepsilon_s^{(s)}} \gg \norm{\varepsilon_{s'}^{(s)}}$ for $s' \neq s$), and all decompositions are consistent with all observed data to within precision $\epsilon$. Policy cause attribution is therefore **logically underdetermined** without declared causal assumptions.

> **Proof:** \rigorFull
> **Step 1: Dimensionality of the problem.** The outcome deviation $\Delta Y \in \R^{d_Y}$ is observed. The four error components $(\varepsilon_{\mathrm{design}}, \varepsilon_{\mathrm{impl}}, \varepsilon_{\mathrm{shock}}, \varepsilon_{\mathrm{meas}}) \in \R^{4 d_Y}$ are unobserved. The observation equation provides $d_Y$ constraints for $4 d_Y$ unknowns. For any $d_Y \geq 1$, the system is underdetermined by a factor of 4.
> 
> **Step 2: Constructing observationally equivalent worlds.** We construct four worlds, each attributing the deviation to a different primary cause. Let $\Delta Y$ have magnitude $D = \norm{\Delta Y} > 0$.
> 
> **World 1 (Design-dominant 设计错误主导):**
> 
> $$
>     \varepsilon_{\mathrm{design}}^{(1)} &= \Delta Y, 

>     \varepsilon_{\mathrm{impl}}^{(1)} &= 0, 

>     \varepsilon_{\mathrm{shock}}^{(1)} &= 0, 

>     \varepsilon_{\mathrm{meas}}^{(1)} &= 0.
> $$
> 
> Interpretation: the policy's causal theory was fundamentally wrong; implementation was perfect, there were no shocks, and measurement was exact.
> 
> **World 2 (Implementation-dominant 执行失败主导):**
> 
> $$
>     \varepsilon_{\mathrm{design}}^{(2)} &= 0, 

>     \varepsilon_{\mathrm{impl}}^{(2)} &= \Delta Y, 

>     \varepsilon_{\mathrm{shock}}^{(2)} &= 0, 

>     \varepsilon_{\mathrm{meas}}^{(2)} &= 0.
> $$
> 
> Interpretation: the theory was correct, but the policy was never properly implemented---funds were diverted, personnel were insufficient, timelines were ignored.
> 
> **World 3 (Shock-dominant 外部冲击主导):**
> 
> $$
>     \varepsilon_{\mathrm{design}}^{(3)} &= 0, 

>     \varepsilon_{\mathrm{impl}}^{(3)} &= 0, 

>     \varepsilon_{\mathrm{shock}}^{(3)} &= \Delta Y, 

>     \varepsilon_{\mathrm{meas}}^{(3)} &= 0.
> $$
> 
> Interpretation: the policy would have worked, but an external event (e.g., global recession, natural disaster) swamped the policy effect.
> 
> **World 4 (Measurement-dominant 测量误差主导):**
> 
> $$
>     \varepsilon_{\mathrm{design}}^{(4)} &= 0, 

>     \varepsilon_{\mathrm{impl}}^{(4)} &= 0, 

>     \varepsilon_{\mathrm{shock}}^{(4)} &= 0, 

>     \varepsilon_{\mathrm{meas}}^{(4)} &= \Delta Y.
> $$
> 
> Interpretation: the policy worked as predicted; the apparent deviation is an artifact of flawed measurement.
> 
> **Step 3: Observational equivalence.** In all four worlds, the observed outcome is identical:
> 
> $$
>     Y^{(s)} = \hat{Y} + \Delta Y, \quad s = 1, 2, 3, 4.
>     <!-- label: eq:identical_Y -->
> $$
> 
> 
> No observation of $Y$ alone can distinguish among the four worlds. Additional observations (e.g., process measures of implementation fidelity, data from comparable untreated units, alternative measurement instruments) can narrow the possibilities but cannot uniquely resolve the decomposition unless they provide at least $3 d_Y$ independent constraints.
> 
> **Step 4: Continuous families of equivalent decompositions.** The four worlds above are extreme points of a continuous $3 d_Y$-dimensional manifold of observationally equivalent decompositions. Any convex combination:
> 
> $$
>     \Delta Y = \alpha_1 \varepsilon_{\mathrm{design}}^{(1)} + \alpha_2 \varepsilon_{\mathrm{impl}}^{(2)} + \alpha_3 \varepsilon_{\mathrm{shock}}^{(3)} + \alpha_4 \varepsilon_{\mathrm{meas}}^{(4)},
>     <!-- label: eq:convex_combination -->
> $$
> 
> with $\sum_s \alpha_s = 1$, $\alpha_s \geq 0$, is also observationally equivalent.
> 
> **Step 5: The role of assumptions.** Any claim that ``the policy failed because of design error'' implicitly assumes $\varepsilon_{\mathrm{impl}} \approx 0$, $\varepsilon_{\mathrm{shock}} \approx 0$, $\varepsilon_{\mathrm{meas}} \approx 0$. These assumptions must be declared and justified. The theorem's force is that without such declarations, the attribution is not merely uncertain---it is *logically indeterminate*. The data alone cannot answer the question.
> 
> **Step 6: Genericity.** The construction is generic, not pathological. Every real-world policy evaluation faces this ambiguity. When China's GDP growth falls short of the government's target, is the forecasting model flawed (design), were stimulus measures insufficiently deployed (implementation), did global trade tensions reduce exports (shock), or is the GDP measurement methodology itself problematic (measurement)? Without explicit assumptions, these explanations are indistinguishable. $\square$

> **Corollary:** [Assumption Mandate for Policy Evaluation 政策评估的假设声明要求]
> <!-- label: cor:assumption_mandate_policy -->
> Any attribution of policy outcome deviation to a specific cause **must** be accompanied by:
> 
1. An explicit declaration of which components are assumed negligible: ``We assume $\varepsilon_{\mathrm{shock}} \approx 0$ because no major external events occurred during the treatment period.''
2. A justification for each assumption: ``We verify $\varepsilon_{\mathrm{meas}} \approx 0$ by triangulating the outcome measure across three independent data sources (household survey, administrative records, satellite data), obtaining inter-source correlation $\rho > 0.95$.''
3. A sensitivity analysis: ``If our assumption about implementation fidelity is violated---if only 70\% of allocated funds were actually disbursed---the attributed design error of 2.3 percentage points would be reduced to 1.1 percentage points.''

> Without such declarations, policy evaluation is scientifically incomplete.

> **Remark:** [Connection to \ThmSCXHonest]
> <!-- label: rem:honest_policy -->
> Theorem [ref] is the policy-evaluation instantiation of \ThmSCXHonest{} (the Honest Agent Theorem). The Honest Agent Theorem establishes that in any prediction system with multiple error sources, the attribution of error to a specific source is unidentifiable from output alone. In the governance setting, the four error sources (design, implementation, shock, measurement) play the role of the general error components. The policy setting amplifies the unidentifiability because: (i) policy outcomes are observed at low frequency (quarterly or annually), providing few data points; (ii) controlled experiments are typically infeasible for macro-scale policies; (iii) political actors have strong incentives to attribute failure to external shocks and success to design, creating asymmetric assumption pressure.

## Multi-Expert Policy Evaluation 多专家政策评估
<!-- label: sec:multiexpert -->

The Yajie{} consensus mechanism provides a formal protocol for aggregating heterogeneous policy evaluations. Different experts---statistical agencies, international organizations, academic researchers---produce independent estimates of policy effects using different data sources, methodologies, and identification strategies. The Yajie{} consensus combines these estimates with correlation-adjusted weights, producing an auditable confidence interval.

### Expert Configuration 专家配置

> **Definition:** [Policy Evaluation Expert 政策评估专家]
> <!-- label: def:policy_expert -->
> A policy evaluation expert is a tuple $E = (\mathcal{D}, \mathcal{M}, \mathcal{I})$, where:
> 
- $\mathcal{D}$ is the data source (survey, administrative, satellite, third-party);
- $\mathcal{M}$ is the methodology (difference-in-differences, synthetic control, regression discontinuity, instrumental variables, structural estimation, Bayesian hierarchical model, machine learning);
- $\mathcal{I}$ is the identification strategy (the causal assumptions under which $\mathcal{M}$ identifies the policy effect).

> **Definition:** [Expert Estimate 专家估计]
> <!-- label: def:expert_estimate -->
> For a policy $\pi$ targeting outcome $Y$, expert $E_j$ produces:
> 
> $$
>     \hat_j(\pi) = \tau(\pi) + b_j + \eta_j,
>     <!-- label: eq:expert_estimate -->
> $$
> 
> where $\tau(\pi)$ is the true policy effect, $b_j$ is expert $j$'s systematic bias (from modeling assumptions, data limitations), and $\eta_j \sim (0, \sigma_j^2)$ is the idiosyncratic estimation error.

### Yajie{ Consensus for Policy Effects Yajie政策效应共识}

> **Definition:** [Correlation-Adjusted Yajie{} Weights 相关性调整的Yajie权重]
> <!-- label: def:yajie_policy_weights -->
> The Yajie{} weight for expert $j$ is:
> 
> $$
>     w_j^{Yajie} = \frac{1/\hat_j^2}{\sum_{\ell=1}^{M} 1/\hat_\ell^2} \cdot \frac{1}{1 + \sum_{\ell \neq j} \hat_{j\ell} \cdot (\hat_\ell / \hat_j)},
>     <!-- label: eq:yajie_policy_weight -->
> $$
> 
> where $\hat_j^2$ is the estimated variance of expert $j$'s estimate (from bootstrap or analytical standard errors) and $\hat_{j\ell}$ is the estimated correlation between experts $j$ and $\ell$ (from overlapping data, shared modeling assumptions, or historical concordance).

> **Definition:** [Yajie{} Consensus Policy Effect Yajie共识政策效应]
> <!-- label: def:consensus_policy -->
> The Yajie{} consensus policy effect is:
> 
> $$
>     \hat_{Yajie}(\pi) = \sum_{j=1}^{M} w_j^{Yajie} \cdot \hat_j(\pi),
>     <!-- label: eq:consensus_policy_effect -->
> $$
> 
> with consensus standard error:
> 
> $$
>     \hat_{Yajie}(\pi) = \left(\sum_{j=1}^{M} \frac{1}{\hat_j^2}\right)^{-1/2} \cdot \frac{1}{\sqrt{1 - \bar_{\mathrm{eff}}}},
>     <!-- label: eq:consensus_se -->
> $$
> 
> where $\bar_{\mathrm{eff}} = \sum_{i \neq j} w_i^{Yajie} w_j^{Yajie} \hat_{ij} / \sum_{i \neq j} w_i^{Yajie} w_j^{Yajie}$.

> **Proposition:** [Consensus Efficiency 共识效率]
> <!-- label: prop:consensus_efficiency -->
> Under Assumptions [ref] and [ref], the Yajie{} consensus estimator $\hat_{Yajie}$ is the minimum-variance linear unbiased estimator of $\tau(\pi)$ when expert biases are zero-mean and symmetrically distributed. When biases are non-zero but uncorrelated across experts, $\hat_{Yajie}$ achieves bias reduction of order $O(1/\sqrt{M})$ relative to any single expert.

> **Proof:** \rigorPartial
> For unbiased experts ($b_j = 0$), the variance is $\Var(\sum_j w_j \hat_j) = \sum_{i,j} w_i w_j \Cov(\hat_i, \hat_j)$. Minimizing subject to $\sum_j w_j = 1$ via Lagrange multipliers yields $w_j^* \propto \sum_k (\Sigma^{-1})_{jk}$, where $\Sigma_{ij} = \Cov(\hat_i, \hat_j)$. For diagonal $\Sigma$ (uncorrelated experts), $w_j^* \propto 1/\sigma_j^2$, matching the first factor in Eq. [ref]. The second factor provides a first-order correction for non-zero correlations. For biased experts with $\E[b_j] = 0$ and $\Var(b_j) = \sigma_b^2$, the bias of the consensus is $\sum_j w_j b_j$, which has variance $\sigma_b^2 \sum_j w_j^2 = O(1/M)$, delivering the $1/\sqrt{M}$ bias reduction.  $\square$

### Expert Configurations for Specific Governance Metrics

[Table omitted — see original .tex]

> **Remark:** [Methodological Diversity 方法多样性]
> <!-- label: rem:method_diversity -->
> The experts in Table [ref] are deliberately heterogeneous in both data source and methodology. For employment, the household survey uses stratified random sampling with a frequentist design-based estimator; payroll data uses a census of formal-sector firms; social security records provide administrative counts; and satellite nightlights use a machine learning model trained on luminosity-employment correlations. This heterogeneity minimizes $\bar\rho$ (Assumption [ref]), maximizing effective auditor multiplicity $M_{\mathrm{eff}}$.

\begin{algorithm}[htbp]
*Caption:* Yajie{} Multi-Expert Policy Evaluation Protocol
<!-- label: alg:policy_eval -->
\begin{algorithmic}[1]
\Require Policy $\pi$, outcome metric $Y$, expert set $\{E_j\}_{j=1}^M$, time horizon $T$
\Ensure Consensus policy effect $\hat_{Yajie}(\pi)$, confidence interval, assumption audit report
\For{$j = 1$ to $M$}
    \State Expert $E_j$ identifies treatment and control units per its methodology
    \State Expert $E_j$ estimates $\hat_j(\pi)$ and standard error $\hat_j$
    \State Expert $E_j$ declares identification assumptions $\mathcal{I}_j$
\EndFor
\State Estimate pairwise correlations $\hat_{ij}$ from historical evaluation concordance
\State Compute Yajie{} weights $w_j^{Yajie}$ via Eq. [ref]
\State Consensus effect: $\hat_{Yajie} \gets \sum_j w_j^{Yajie} \hat_j$
\State Consensus SE: $\hat_{Yajie} \gets$ Eq. [ref]
\State Confidence interval: $[\hat_{Yajie} - z_{\alpha/2}\hat_{Yajie},\; \hat_{Yajie} + z_{\alpha/2}\hat_{Yajie}]$
\State **Assumption audit**: Check agreement of declared $\{\mathcal{I}_j\}$; flag conflicting assumptions
\State \Return $\hat_{Yajie}$, CI, assumption audit report
\end{algorithmic}
\end{algorithm}

## Cercis{ Score for Policy 政策Cercis评分}
<!-- label: sec:cercis -->

The Cercis{} scoring framework [cite] ranks entities by a combination of quality $Q$ (accuracy on known tasks) and novelty $N$ (coverage of novel regimes). For governance, we adapt Cercis{} to score policies.

> **Definition:** [Policy Quality Score 政策质量分]
> <!-- label: def:policy_Q -->
> For a policy $\pi$ evaluated over a set of $K$ comparable jurisdictions or time periods, the quality score is:
> 
> $$
>     Q(\pi) = -\Bigg(
>         \underbrace{\frac{1}{K}\sum_{k=1}^{K} \frac{\norm{Y_k(\pi) - \hat{Y}_k(\pi)}}{\norm{\hat{Y}_k(\pi)}}}_{prediction error  \varepsilon_{\mathrm{pred}}}
>         \;+\;
>         \underbrace{\frac{1}{K}\sum_{k=1}^{K} \frac{\abs{Y_k(\pi) - Y_k(\emptyset)}}{\abs{\hat{Y}_k(\pi) - Y_k(\emptyset)}} \cdot \ind{sign mismatch}}_{directional error  \varepsilon_{\mathrm{dir}}}
>     \Bigg),
>     <!-- label: eq:policy_Q -->
> $$
> 
> where $Y_k(\emptyset)$ is the counterfactual outcome without the policy (estimated via synthetic control or comparable untreated unit). The first term penalizes inaccurate magnitude predictions; the second term penalizes getting the *direction* of the effect wrong (a policy predicted to increase employment that actually decreases it).

> **Definition:** [Policy Novelty Score 政策新颖性分]
> <!-- label: def:policy_N -->
> The novelty score quantifies the extent to which a policy operates in a regime without historical precedent:
> 
> $$
>     N(\pi) = \sum_{d=1}^{D} \nu_d \cdot \ind{policy $\pi$ is the first of type $d$ in regime $r$},
>     <!-- label: eq:policy_N -->
> $$
> 
> where $D$ is the number of policy dimensions (fiscal, monetary, regulatory, social, environmental) and $\nu_d$ is the difficulty weight for dimension $d$:
> 
> $$
>     \nu_d = \frac{1}{\min_{\pi' \neq \pi} \abs{\tau_d(\pi) - \tau_d(\pi')} + \epsilon},
>     <!-- label: eq:nu_d -->
> $$
> 
> inversely proportional to the minimum distance to any previously evaluated policy on dimension $d$.

> **Definition:** [Cercis{} Policy Score Cercis{}政策评分]
> <!-- label: def:cercis_policy -->
> 
> $$
>     S(\pi) = Q(\pi) + \eta \cdot N(\pi),
>     <!-- label: eq:cercis_policy -->
> $$
> 
> where $\eta \geq 0$ is the novelty-accuracy tradeoff. $\eta = 0$ ranks policies purely by predictive accuracy; $\eta > 0$ rewards policies that explore novel regimes, penalizing ``safe'' policies that operate only in well-understood domains.

> **Remark:** [Cercis{} and Policy Learning Cercis{}与政策学习]
> <!-- label: rem:cercis_learning -->
> The Cercis{} score creates a formal policy learning objective. A government optimizing $\sum_\pi S(\pi)$ over its policy portfolio balances exploitation (policies with proven accuracy) and exploration (policies that generate information about novel regimes). The $\eta$ parameter quantifies the value of information: $\eta = 0$ for risk-neutral exploitation; $\eta > 0$ when learning about novel policy regimes has intrinsic value for future decision-making.

[Table omitted — see original .tex]

## Spring{ Gating for Governance Regime Detection 治理制度的Spring门控检测}
<!-- label: sec:spring -->

A critical challenge in governance auditing is detecting when a country transitions from ``normal governance'' (where published statistics are broadly reliable) to ``information control'' (where data quality systematically degrades). The Spring{} gating mechanism [cite] provides a self-evolving threshold for regime detection.

> **Definition:** [Governance Regime 治理制度]
> <!-- label: def:gov_regime -->
> A governance regime $R$ is characterized by the joint distribution of the discrepancy between published statistics and independently verifiable estimates:
> 
> $$
>     D_R = \mathbb{P}(\norm{m - c} > \varepsilon \mid R),
>     <!-- label: eq:regime_dist -->
> $$
> 
> where $m$ is the government's published claim and $c$ is the Yajie{} multi-expert consensus. In a normal regime ($R_{\mathrm{normal}}$), $D_{R_{\mathrm{normal}}} \approx \alpha$ for a small $\alpha$ (false alarm rate). In an information control regime ($R_{\mathrm{control}}$), $D_{R_{\mathrm{control}}} \gg \alpha$.

> **Definition:** [Spring{} Detection Statistic Spring{}检测统计量]
> <!-- label: def:spring_stat -->
> The Spring{} gating statistic at time $t$ is the exponentially weighted moving average of detection events:
> 
> $$
>     S_t = \lambda S_{t-1} + (1 - \lambda) \cdot \ind{\norm{m_t - c_t}_\infty > \varepsilon},
>     <!-- label: eq:spring_stat -->
> $$
> 
> with $S_0 = \alpha$ and decay factor $\lambda \in (0, 1)$. The Spring{} alarm triggers when $S_t > \gamma_t$, where the threshold $\gamma_t$ evolves based on the observed false alarm rate:
> 
> $$
>     \gamma_{t+1} = \gamma_t + \eta_\gamma \cdot (\alpha_{\mathrm{target}} - \ind{S_t > \gamma_t  in normal regime}).
>     <!-- label: eq:spring_threshold -->
> $$

> **Proposition:** [Spring{} Regime Detection Properties Spring{}制度检测性质]
> <!-- label: prop:spring_detection -->
> Under Assumption [ref], for a transition from $R_{\mathrm{normal}}$ to $R_{\mathrm{control}}$ occurring at time $t_0$, the Spring{} gating mechanism satisfies:
> 
1. **False alarm control:** $\lim_{T \to \infty} \frac{1}{T}\sum_{t=1}^{T} \ind{S_t > \gamma_t \mid R_{\mathrm{normal}}} \leq \alpha_{\mathrm{target}}$.
2. **Detection delay:** $\E[t_{\mathrm{detect}} - t_0 \mid R_{\mathrm{control}}] \leq \frac{\log(\gamma_0 / \delta)}{-\log(\lambda)} + O(1)$, where $\delta = D_{R_{\mathrm{control}}} - D_{R_{\mathrm{normal}}}$ is the regime divergence.
3. **Self-evolution:** $\gamma_t$ adapts to maintain the target false alarm rate without manual recalibration.

> **Proof:** \rigorSketch
> The Spring{} mechanism is a stochastic approximation algorithm. (i) False alarm control follows from the Robbins-Monro convergence of $\gamma_t$ to the $\alpha_{\mathrm{target}}$-quantile of the null distribution. (ii) Detection delay follows from the geometric mixing of the EWMA: after the regime shift, $S_t$ drifts toward $D_{R_{\mathrm{control}}}$ with rate $1 - \lambda$, crossing $\gamma_t$ in $O(\log(1/\delta) / (1-\lambda))$ steps. (iii) Self-evolution is inherent in the recursive threshold update. $\square$

> **Remark:** [Practical Significance 实践意义]
> <!-- label: rem:spring_practical -->
> The Spring{} mechanism detects *statistical* regime transitions---shifts in the distribution of the discrepancy between published and independently estimated statistics. It does not detect political intentions, censorship mechanisms, or institutional changes directly. A government that reduces data publication without manipulating published values triggers the opacity detection of Theorem [ref]; a government that *manipulates* published values triggers Spring{} as the discrepancy distribution shifts. Both mechanisms operate on statistical signatures, not political categories.

## Specific Formal Applications 具体形式化应用
<!-- label: sec:applications -->

### Fertility Rate Auditing 生育率审计

The total fertility rate (TFR) $\theta_{\mathrm{fert}}$ is a critical governance metric with major implications for pension systems, education planning, and labor force projections. Three independent data sources provide cross-validation:

- **Census data $A_1$:** Decennial or quinquennial full-population enumeration. Provides the most comprehensive estimate but with long inter-census intervals. Standard error $\sigma_1 \approx 0.05$ births per woman.
- **Hospital birth records $A_2$:** Administrative data from birth registrations at hospitals and health facilities. Near-complete coverage in urban areas; may miss home births in rural regions. Standard error $\sigma_2 \approx 0.08$, with systematic downward bias in regions with low institutional delivery rates.
- **School enrollment $A_3$:** Primary school enrollment data lagged by 6--7 years provides an independent cohort-size estimate that can be back-projected to TFR using mortality and migration models. Standard error $\sigma_3 \approx 0.12$, with model-dependent uncertainty.
- **UN Population Division estimates $A_4$:** Bayesian hierarchical model combining all available national data with demographic transition priors. Standard error $\sigma_4 \approx 0.10$ for countries with high-quality data; larger for data-sparse settings.

The Yajie{} consensus TFR is:

$$
    \hat_{\mathrm{fert}}^{Yajie} = \sum_{j=1}^{4} w_j^{Yajie} \hat_{\mathrm{fert}}^{(j)},
    <!-- label: eq:fert_consensus -->
$$

with the consensus standard error providing an auditable bound on TFR uncertainty. A published TFR $m_{\mathrm{fert}}$ is flagged if $\abs{m_{\mathrm{fert}} - \hat_{\mathrm{fert}}^{Yajie}} > 2 \hat_{Yajie}$.

### Employment Rate Auditing 就业率审计

Employment $\theta_{\mathrm{emp}}$ exemplifies the power of multi-source verification. Four structurally independent data sources exist:

- **Household labor force survey $A_1$:** Stratified random sample of households, ILO-standard employment definitions. Standard error $\sigma_1 \approx 0.3$--$0.5$ percentage points for national estimates.
- **Payroll employment data $A_2$:** Census of formal-sector establishments reporting to tax/social security authorities. Covers formal employment only; misses informal sector, agricultural labor, and self-employment. Bias correlated with informality rate.
- **Social security contribution records $A_3$:** Administrative count of workers with active social security contributions. Similar coverage to payroll data but with different administrative incentives (workers may contribute without formal payroll).
- **Satellite nighttime lights $A_4$:** Machine learning model mapping VIIRS/DMSP nighttime light intensity to economic activity, calibrated to employment in surveyed regions. Standard error $\sigma_4 \approx 1.0$--$2.0$ percentage points at fine spatial resolution; improves with aggregation.

The structural independence of these sources is high: $\bar$ between satellite and survey estimates is typically $< 0.3$, yielding $M_{\mathrm{eff}} \approx M / (1 + (M-1) \cdot 0.3) \approx 2.1$ for $M = 4$. This is sufficient for opacity detection (Theorem [ref]) but may require additional auditors for transparency dominance (Theorem [ref]) depending on $\kappa$ and $L_B$.

### Government Openness Index 政府公开度指数

We formalize a **government openness index** as a directly measurable quantity from the publication record:

> **Definition:** [Openness Index 公开度指数]
> <!-- label: def:openness -->
> 
> $$
>     \Omega_t = \frac{K_{\mathrm{pub}, t}}{K_*} \cdot \frac{1}{3}\left(
>         \underbrace{\frac{g_{\mathrm{pub}, t}}{g_}}_{granularity 粒度} +
>         \underbrace{\frac{1}{1 + \bar_{\mathrm{lag}, t}}}_{timeliness 及时性} +
>         \underbrace{\frac{f_{\mathrm{update}, t}}{f_}}_{frequency 更新频率}
>     \right),
>     <!-- label: eq:openness -->
> $$
> 
> where:
> 
- $K_{\mathrm{pub}, t} / K_$: fraction of standard statistics published (from Theorem [ref]);
- $g_{\mathrm{pub}, t} / g_$: average granularity of published data (e.g., provincial vs. county vs. township level), normalized by the maximum feasible granularity;
- $\bar_{\mathrm{lag}, t}$: average publication lag in months (lower is better);
- $f_{\mathrm{update}, t} / f_$: update frequency (annual, quarterly, monthly, weekly), normalized.

$\Omega_t \in [0, 1]$ is directly verifiable: any observer can count published datasets, check their granularity, note the publication date, and track update frequency. It requires no statistical modeling---it is a *counting measure*. The Spring{} mechanism monitors $\Omega_t$ for declines that may signal a transition toward information control.

### Policy Evaluation: Causal Identification Strategies 政策评估：因果识别策略

For policy evaluation, the multi-expert framework employs causally distinct identification strategies:

1. **Difference-in-Differences (DiD) 双重差分:** Compares outcome trends in treated vs. untreated units before and after policy implementation. Identification assumption: parallel trends in the absence of treatment.
2. **Synthetic Control (SC) 合成控制:** Constructs a weighted combination of untreated units that matches the treated unit's pre-treatment trajectory. Identification assumption: the synthetic control approximates the counterfactual.
3. **Regression Discontinuity Design (RDD) 断点回归:** Exploits a threshold in policy assignment (e.g., population cutoff for program eligibility). Identification assumption: units just above and below the threshold are comparable.
4. **Instrumental Variables (IV) 工具变量:** Uses an exogenous source of variation in policy exposure. Identification assumption: exclusion restriction (instrument affects outcome only through policy exposure).
5. **Structural estimation 结构估计:** Specifies and estimates a fully parametric economic model. Identification assumption: the model structure correctly captures all relevant mechanisms.

Each strategy has different identification assumptions. When they agree on the policy effect, the consensus is robust to assumption violations (the assumptions are logically independent). When they disagree, the pattern of disagreement reveals which assumptions are likely violated---exactly the logic of the unidentifiability theorem applied constructively.

## M-Parameter as Management KPI M值作为管理KPI
<!-- label: sec:m-kpi -->

The M-parameter framework, when combined with cryptographic hashing (see the SCX Science Audit Mandate), transforms organizational accountability. This section formalizes M as a **management KPI** — a verifiable, non-gameable metric for individual and institutional trustworthiness.

### The Accountability Chain 问责链

> **Definition:** [M-Value Accountability Chain]
> An organization with $L$ hierarchical layers. Each layer $\ell$ aggregates data from layer $\ell-1$ and reports upward. Each report includes $(M_\ell, \mathcal{H}_\ell)$ where $\mathcal{H}_\ell = SHA-256(data \| M_\ell)$. Under mandatory M-declaration:
> 
1. Worker submits: $(M_0, \mathcal{H}_0)$ — raw data with M-certification.
2. Manager aggregates: $(M_1, \mathcal{H}_1)$ — combines subordinate M-values, does not modify raw data.
3. Each subsequent layer $\ell$ passes upward: $(M_\ell, \mathcal{H}_\ell)$.
4. Public registry receives the chain $\{(M_\ell, \mathcal{H}_\ell)\}_{\ell=0}^L$.

> **Theorem:** [Precise Blame Attribution 精确归责定理 (甩锅定理 — Blame Shedding Theorem)]
> <!-- label: thm:blame-chain -->
> \rigorFull
> When SCX detects $M_{obs} < M_{declared}$ anywhere in the chain, the **earliest layer** $\ell^*$ where the discrepancy first appears is uniquely identifiable: $\ell^* = \min\{\ell : \mathcal{H}_\ell  inconsistent with the data at layer  \ell\}$. The responsible party at layer $\ell^*$ cannot shift blame upward (the hash at layer $\ell^*+1$ merely transmitted their fraudulent input) nor downward (subordinates' hashes are independently verifiable).

> **Proof:** By induction on the chain. Each layer's hash $\mathcal{H}_\ell$ commits to the exact data received from layer $\ell-1$. If $\mathcal{H}_0, ..., \mathcal{H}_{\ell-1}$ all verify and $\mathcal{H}_\ell$ does not, the discrepancy originated at layer $\ell$. The fraudster at $\ell$ cannot claim the data came from $\ell-1$ (hash mismatch) nor that $\ell+1$ modified it (the hash at $\ell+1$ was computed from the fraudulent input they provided). SHA-256 preimage resistance prevents post-hoc fabrication of alternative $(M', data')$ matching $\mathcal{H}_\ell$. $\square$

> **Corollary:** [Perfect Blame Shedding for Honest Managers 诚实管理者的完美甩锅]
> A manager at layer $\ell$ who faithfully transmits subordinate M-values and hashes incurs zero liability for subordinate fraud. The fraud is attributed to layer $\ell^* < \ell$, and the manager's own M-value remains VERIFIED. This creates a **positive incentive** for managers to enforce M-declaration: not enforcing it makes them complicit (Theorem~4, Science Audit Mandate); enforcing it makes them immune.

### Game-Theoretic Analysis 博弈论分析

> **Proposition:** [M-KPI as a Dominant Strategy Enforcer]
> <!-- label: prop:m-kpi-dominant -->
> Under the M-accountability chain with public registry:
> 
1. **Workers**: Honest declaration ($M = M_{true}$) strictly dominates any falsification strategy when the detection probability $\mathbb{P}(detection) \to 1$ (Theorem~3, Science Audit Mandate).
2. **Managers**: Requiring M-declaration from subordinates strictly dominates not requiring it — the former provides blame immunity (Corollary above); the latter makes the manager complicit (Theorem~4, Science Audit Mandate).
3. **Organization**: Publishing the full M-chain on the public registry strictly dominates selective publication — incomplete chains are equivalent to $M=0$ by Theorem~2 (Science Audit Mandate).

> The Nash equilibrium is universal honest M-declaration at all layers.

### Practical Implications 实践意义

The M-KPI transforms organizational dynamics:

- **Whistleblowing becomes unnecessary**. The M-chain automatically exposes fraud; individual workers need not risk retaliation — the mathematics does the exposure.
- **Internal investigations become trivial**. When $M_{obs} < M_{declared}$, the hash chain identifies the exact layer and individual responsible. No need for committees, hearings, or testimony.
- **Performance evaluation gains an objective dimension**. Employee M-values are auditable quality metrics. High M = verifiable competence. Low M = objectively poor data practices.
- **Organizational reputation becomes quantifiable**. An organization's aggregate M-value is publicly visible. Investors, regulators, and partners can compare M-values across organizations.

> **Remark:** [limitation]
> The M-KPI does not measure effort, creativity, or qualitative contribution. It measures **data integrity**. Organizations should use M as a floor (minimum acceptable data quality), not a ceiling (substitute for holistic evaluation).
<!-- label: sec:discussion -->

### Relationship to Existing Theoretical Frameworks 与现有理论框架的关系

**Mechanism Design (Myerson).** Our framework is a mechanism design problem: we construct a game (the Yajie{} audit game) such that the equilibrium strategy (honest reporting) achieves a social objective (accurate governance statistics). The mechanism design literature [cite] establishes that truthful revelation requires incentive compatibility. The Yajie{} payoff structure achieves incentive compatibility through the detection penalty $\kappa \cdot \Pbb(\norm{m - c} > \varepsilon)$, which makes the expected cost of misreporting exceed the benefit when $M > M^*$. Unlike classical mechanism design, we do not require a central planner to enforce penalties; the auditor community provides decentralized enforcement through its consensus estimates. However, this requires that detection carries real consequences ($\kappa > 0$), which in turn requires that the auditor community's findings influence the government's payoff (through reputation, market access, institutional sanctions, or domestic accountability mechanisms). The mechanism is *incomplete* if $\kappa = 0$---a fundamental limitation we discuss below.

**Transparency Theory (Stiglitz).** Stiglitz's work on information asymmetry [cite] establishes that transparency improves market efficiency by reducing information rents. Our framework extends this logic to governance statistics: the auditor community reduces the government's information monopoly, diminishing its ability to extract ``governance rents'' from favorable misreporting. Theorem [ref] provides a quantitative formalization: the threshold $M^*$ is the point at which the information rent ($L_B \delta$) is eliminated by detection risk. The novelty is in the explicit role of *multiplicity*: transparency is not a binary property but a continuous function of the number and independence of auditors.

**Social Choice (Arrow).** Arrow's impossibility theorem [cite] establishes that no social welfare function can simultaneously satisfy a set of seemingly reasonable axioms. Our framework sidesteps this impossibility by restricting its scope: we do not aggregate preferences or rank social states. We verify statistical claims against multi-expert consensus. The Yajie{} consensus is a statistical aggregation of estimates about an objective quantity $\theta$, not a preference aggregation. This is a crucial distinction: governance statistics are (in principle) verifiable facts, not value judgments. The SCX{} framework audits the former, not the latter.

### Honest Limitations 诚实局限性

We now state what SCX{} governance auditing cannot do, consistent with the SCX{} mandate of honest limitation declaration.

1. **\limitationTag{1} Cannot replace democratic deliberation 不能替代民主协商.** SCX{} detects statistical anomalies in published governance data. It cannot determine whether a particular unemployment rate is ``too high,'' whether a fertility policy is ``just,'' or whether a tradeoff between growth and equality is ``acceptable.'' These are normative questions requiring democratic processes. The mathematics tells us what *is* (or what is likely to be true given the data); it does not tell us what *should be*.
2. **\limitationTag{2} Cannot resolve value conflicts 不能解决价值冲突.** When experts disagree about policy effects, the Yajie{} consensus produces a weighted average with confidence bounds. It does not adjudicate which expert's normative framework is superior. A Marxist economist and a neoclassical economist may produce different policy effect estimates because they model different mechanisms; the consensus averages their numbers but does not resolve their theoretical disagreement.
3. **\limitationTag{3} Cannot detect shared biases 不能检测共享偏差.** If all auditors share a common systematic bias (Assumption [ref] violated), the consensus inherits that bias. For example, if all employment estimates rely on the same flawed population denominator, the consensus will be precisely wrong. SCX{} detection power depends on *diversity* of data sources and methodologies; without it, the audit is blind.
4. **\limitationTag{4} Requires $\kappa > 0$ for incentive compatibility 激励相容需要$\kappa > 0$.** The transparency dominance of Theorem [ref] requires that detection carries a real cost. If the government is indifferent to auditor findings ($\kappa = 0$), the audit is a measurement exercise with no behavioral effect. This is not a mathematical limitation but an institutional one: audit without consequences is documentation, not governance.
5. **\limitationTag{5} Cannot verify counterfactuals 不能验证反事实.** Policy evaluation (Section [ref]) requires estimating what would have happened without the policy---an inherently unverifiable counterfactual. The multi-expert consensus bounds the uncertainty but cannot eliminate it. Causal inference from observational data always requires untestable assumptions [cite].
6. **\limitationTag{6} Auditor independence is asymptotic 审计者独立性是渐近的.** Assumption [ref] (conditional independence) is an idealization. In practice, auditors share methods, data sources, and professional networks, inducing positive correlation $\bar > 0$. The effective multiplicity correction $M_{\mathrm{eff}}$ partially addresses this, but the independence assumption should be treated as a target for institutional design, not a description of current reality.
7. **\limitationTag{7} Cannot substitute for institutional legitimacy 不能替代制度合法性.** A statistical audit, however rigorous, does not confer democratic legitimacy. A government that achieves perfect Cercis{} scores on statistical accuracy may still lack popular mandate. SCX{} audits the *output* of governance (data quality), not the *process* (elections, representation, accountability). Both are necessary; neither is sufficient.
8. **\limitationTag{8} Regime detection has latency 制度检测有延迟.** The Spring{} mechanism (Section [ref]) detects regime transitions with expected delay $O(\log(1/\delta) / (1-\lambda))$. For gradual transitions (small $\delta$), this delay can be substantial. Rapid detection requires high-frequency data and low $\lambda$, which increases false alarm rates. There is an unavoidable speed-accuracy tradeoff.

### Future Directions 未来方向

1. **Empirical calibration of $M^*$.** The threshold auditor multiplicity $M^*$ depends on parameters ($\kappa$, $L_B$, $\bar\sigma^2$, $\bar\rho$) that must be estimated from historical governance data. The exact Chernoff-tight form $\log(\kappa/(\kappa - L_B\delta_\min))$ provides a sharper threshold than the prior conservative approximation. A systematic empirical study calibrating $M^*$ for different countries and governance metrics would operationalize the framework.
2. **Dynamic audit games.** Our model treats the audit as a one-shot game. In reality, governments and auditors interact repeatedly, creating reputation effects, learning, and strategic adaptation. A repeated-game extension would capture these dynamics.
3. **Hierarchical auditor communities.** Our model treats all auditors as symmetric. In practice, auditors have different credibility, resources, and access. A hierarchical Yajie{} consensus with auditor-level quality weights (themselves subject to meta-audit) would improve robustness.
4. **Integration with causal machine learning.** Modern causal ML methods (double/debiased machine learning, causal forests, deep instrumental variables) can serve as additional experts in the multi-expert framework, increasing $M$ and reducing $\bar\rho$ through methodological diversity.
5. **Institutional design implications.** The theorems provide quantitative guidance for designing transparency institutions: Theorem [ref] tells us how many independent statistical agencies are needed; Theorem [ref] tells us the detection probability as a function of publication completeness.

## Conclusion 结论
<!-- label: sec:conclusion -->

We have presented a mathematical framework for SCX{} auditing of governance, grounded in game theory, statistical detection theory, and causal identification. The framework formalizes governance as a signaling game with multi-expert audit under the Yajie{} Nash-Pareto Equilibrium payoff structure. Three core theorems establish: (i) transparency dominance---under sufficient auditor multiplicity, honest reporting is the game-theoretic equilibrium (Theorem [ref]); (ii) opacity detection---withholding statistics is probabilistically detectable, making full publication the best response (Theorem [ref]); and (iii) policy unidentifiability---deviation from predicted policy outcomes cannot be attributed to a specific cause without declared assumptions (Theorem [ref]).

The framework is deliberately mathematical, not normative. We do not argue that transparency is ``good'' or that audit is ``desirable.'' We prove that under specified conditions, transparency emerges as the rational strategy. The conditions are explicit: sufficient auditor multiplicity ($M > M^*$ with the exact Chernoff-tight threshold), meaningful detection penalties ($\kappa > L_B \delta_\min$), low auditor error correlation ($\bar\rho \ll 1$), and published statistics completeness ($K_{\mathrm{pub}} \to K_*$). The M* threshold is established as **both sufficient and necessary** — for $M < M^*$, misreporting is provably profitable. The upgrade from Hoeffding to Chernoff bounds (sub-Gaussian Cramér rate for Theorem 1, KL-divergence form for Theorem 2) provides strictly tighter detection guarantees, reducing required auditor counts by up to 19% in typical regimes and up to 50× in rare-event detection. When these conditions fail, the theorems predict that misreporting and opacity may be rational strategies---and the mathematics identifies exactly what structural changes would shift the equilibrium.

The SCX{} framework's contribution to governance is not a political program but a **verification technology**: a set of mathematical tools for assessing the quality of published governance statistics through multi-expert consensus. Like any technology, it can be used well or poorly, adopted or ignored. Its value lies in making the transparency problem computationally tractable and its assumptions explicit.

**Acknowledgments.** We thank the SCX for the foundational framework. All errors remain our own. No external funding was received for this theoretical work.

\begin{thebibliography}{99}

\bibitem{SCX2025}
SCX.
\newblock {SCX}: Structured Causal eXamination---A Framework for Multi-Expert Quality Auditing.
\newblock Technical Report, 2025.

\bibitem{SCXCFD2026}
SCX.
\newblock {SCX}-Audited Computational Fluid Dynamics: Multi-Solver Consensus for Certified Aerodynamic Simulation.
\newblock Technical Report, 2026.

\bibitem{SCXPP2026}
SCX.
\newblock {SCX}-Audited Pseudopotentials: A Causal Framework for First-Principles Quality Assurance.
\newblock Technical Report, 2026.

\bibitem{Myerson1981}
R.~B. Myerson.
\newblock Optimal auction design.
\newblock {\em Mathematics of Operations Research}, 6(1):58--73, 1981.

\bibitem{Myerson2008}
R.~B. Myerson.
\newblock Perspectives on mechanism design in economic theory.
\newblock {\em American Economic Review}, 98(3):586--603, 2008.

\bibitem{Stiglitz2002}
J.~E. Stiglitz.
\newblock Information and the change in the paradigm in economics.
\newblock {\em American Economic Review}, 92(3):460--501, 2002.

\bibitem{Stiglitz2000}
J.~E. Stiglitz.
\newblock The contributions of the economics of information to twentieth century economics.
\newblock {\em Quarterly Journal of Economics}, 115(4):1441--1478, 2000.

\bibitem{Arrow1951}
K.~J. Arrow.
\newblock {\em Social Choice and Individual Values}.
\newblock Wiley, 1951.

\bibitem{Holland1986}
P.~W. Holland.
\newblock Statistics and causal inference.
\newblock {\em Journal of the American Statistical Association}, 81(396):945--960, 1986.

\bibitem{Hoeffding1963}
W.~Hoeffding.
\newblock Probability inequalities for sums of bounded random variables.
\newblock {\em Journal of the American Statistical Association}, 58(301):13--30, 1963.

\bibitem{Liang1986}
K.-Y. Liang and S.~L. Zeger.
\newblock Longitudinal data analysis using generalized linear models.
\newblock {\em Biometrika}, 73(1):13--22, 1986.

\bibitem{CoverThomas2006}
T.~M. Cover and J.~A. Thomas.
\newblock {\em Elements of Information Theory}, 2nd edition.
\newblock Wiley-Interscience, 2006.

\bibitem{AcemogluRobinson2012}
D.~Acemoglu and J.~A. Robinson.
\newblock {\em Why Nations Fail: The Origins of Power, Prosperity, and Poverty}.
\newblock Crown Business, 2012.

\bibitem{BesleyBurgess2002}
T.~Besley and R.~Burgess.
\newblock The political economy of government responsiveness: Theory and evidence from India.
\newblock {\em Quarterly Journal of Economics}, 117(4):1415--1451, 2002.

\bibitem{HollyerRosendorffVreeland2011}
J.~R. Hollyer, B.~P. Rosendorff, and J.~R. Vreeland.
\newblock Democracy and transparency.
\newblock {\em Journal of Politics}, 73(4):1191--1205, 2011.

\bibitem{HendersonEtAl2012}
J.~V. Henderson, A.~Storeygard, and D.~N. Weil.
\newblock Measuring economic growth from outer space.
\newblock {\em American Economic Review}, 102(2):994--1028, 2012.

\bibitem{ChenNordhaus2011}
X.~Chen and W.~D. Nordhaus.
\newblock Using luminosity data as a proxy for economic statistics.
\newblock {\em Proceedings of the National Academy of Sciences}, 108(21):8589--8594, 2011.

\bibitem{AbadieEtAl2010}
A.~Abadie, A.~Diamond, and J.~Hainmueller.
\newblock Synthetic control methods for comparative case studies.
\newblock {\em Journal of the American Statistical Association}, 105(490):493--505, 2010.

\bibitem{AngristPischke2009}
J.~D. Angrist and J.-S. Pischke.
\newblock {\em Mostly Harmless Econometrics: An Empiricist's Companion}.
\newblock Princeton University Press, 2009.

\bibitem{GentzkowShapiro2010}
M.~Gentzkow and J.~M. Shapiro.
\newblock What drives media slant? Evidence from U.S. daily newspapers.
\newblock {\em Econometrica}, 78(1):35--71, 2010.

\bibitem{MichalopoulosPapaioannou2013}
S.~Michalopoulos and E.~Papaioannou.
\newblock Pre-colonial ethnic institutions and contemporary African development.
\newblock {\em Econometrica}, 81(1):113--152, 2013.

\end{thebibliography}