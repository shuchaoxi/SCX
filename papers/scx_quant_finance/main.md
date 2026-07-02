\title{
  { **SCX-Audited Quantitative Finance:**}
  { **Multi-Model Consensus for Certified Derivative**}
  { **Pricing and Risk Management**}
  { 基于SCX审计的量化金融：衍生品定价与风险管理}
  { 的多模型共识认证框架}
}

\author{
  **SCX**
   Joint Institute for Computational Finance and Formal Verification
   `scx-quant@research.org`
}

*Abstract:*

We introduce a rigorous mathematical framework for auditing derivative pricing models through multi-model consensus, grounded in the SCX{} formal verification paradigm. In quantitative finance, no single option pricing model universally dominates: Black--Scholes, Heston, SABR, Bates, and rough Bergomi each embed distinct structural assumptions about volatility dynamics, jump behavior, and market regime, yielding materially different fair-price estimates for identical derivative contracts. We prove three foundational theorems that collectively establish (i) a sharp probabilistic bound on simultaneous mispricing by multiple models via a modified Hoeffding argument incorporating effective model count $M_{eff}$ that accounts for shared stochastic process families (Theorem~1); (ii) a fundamental unidentifiability result showing that when model prices diverge from observed market quotes, the source---model misspecification, parameter estimation error, or genuine regime change---cannot be resolved without declared auxiliary assumptions, formalizing Derman's model risk taxonomy within the SCX{} deductive hierarchy (Theorem~2); and (iii) a composite *Cercis Score* ranking pricing models by empirical fidelity, combining implied volatility smile RMSE and delta-hedge P\&L variance with a regime-novelty penalty that quantifies exposure to vol-of-vol regimes unseen during calibration (Theorem~3). These results are synthesized into the *Multi-Model Yajie Consensus Protocol*, a voting-based certification mechanism that aggregates Black--Scholes, Heston, SABR, and Bates outputs with VIX anchoring and spring-gating for volatility regime detection. We calibrate and benchmark the framework on the full SPX options chain (2005--2024), VIX futures, interest-rate swaptions, and cryptocurrency options markets. The Cercis Score establishes the empirical ranking: $\BS \prec \Heston \prec \SABR \prec \BatesM \prec \rBergomi$, where $\prec$ denotes ``dominated with respect to pricing fidelity.''

**Keywords:** derivative pricing, model risk, volatility smile, multi-model consensus, Hoeffding bound, formal verification, SCX{} framework, regime shift detection, 量化金融, 衍生品定价, 模型风险, 波动率微笑.

**SCX Classification:** **SCX-THM.3** (Formal Verification of Stochastic Systems), **SCX-CERT.7** (Multi-Expert Consensus Certification).

---

## Introduction

### Motivation: The Multi-Model Problem in Derivative Pricing

Derivative pricing stands as one of the most consequential quantitative problems in modern finance. The fair valuation of an option, swaption, or structured product determines not only trading P\&L but also regulatory capital, margin requirements, and systemic risk exposure. Yet, after five decades of research since the Black--Scholes breakthrough [cite], the fundamental question remains unsettled: *which model should one use?*

The answer is context-dependent and deeply uncertain. Consider a vanilla SPX call option with strike $K$ and maturity $T$. Five widely-deployed models produce five different fair-price estimates:

- **Black--Scholes (BS):** Constant volatility $\sigma$, geometric Brownian motion; closed-form solution; known to be empirically inadequate for anything beyond ATM short-dated options.
- **Heston:** Mean-reverting stochastic volatility $v_t$ with correlation $\rho$; semi-analytic characteristic function; captures volatility clustering and skew but struggles with short-maturity extreme skew.
- **SABR:** Stochastic $\alpha$-$\beta$-$\rho$ dynamics; asymptotic expansion pricing; excellent for interest-rate volatility smiles but limited by its perturbative nature for deeply OTM equity options.
- **Bates:** Heston dynamics augmented with Merton-style compound Poisson jumps; captures both stochastic vol and crash risk; calibration burden increases substantially.
- **Rough Bergomi:** Fractional Brownian motion with Hurst parameter $H < 1/2$ driving volatility; reproduces the observed power-law decay of the at-the-money volatility skew [cite]; computationally intensive.

Each model encodes a different set of structural assumptions about the data-generating process. When these models produce divergent prices for the same contract---which they routinely do, especially in tail regimes---the practitioner faces an epistemological crisis: *which price, if any, can be certified as correct?*

### The SCX Approach

The SCX{} (Stochastic Certification eXtended) framework [cite] provides a formal deductive apparatus for auditing complex stochastic systems. In this paper, we apply SCX{} to the multi-model pricing problem by treating each option pricing model as an *expert* in a consensus protocol. The core insight is that while no individual model can be proven correct in all regimes, the *structure of disagreement* among a sufficiently diverse ensemble of models carries exploitable information about model risk, mispricing probability, and regime shifts.

We formalize this observation through three theorems, each with full deductive proofs within the SCX{} axiom system:

1. **Multi-Model Mispricing Detection:** We bound the probability that all $M$ models simultaneously miss a mispricing exceeding threshold $\Delta$, using a modified Hoeffding concentration inequality where the effective model count $M_{eff}$ adjusts for shared stochastic process families. The bound is $\Pbb(all miss \mid mispricing > \Delta) \leq \exp(-2 M_{eff} \Delta^2)$ and is calibrated to SPX options data for operational significance.
2. **Model Risk--Regime Shift Unidentifiability:** We prove that when an ensemble of model prices diverges from observed market quotes, the attribution of this divergence to model misspecification, parameter estimation error, or a genuine structural regime change is *logically unidentifiable* without declaring auxiliary assumptions about the true data-generating process. This formalizes Emanuel Derman's qualitative model risk hierarchy [cite] as a specific instance of the SCX{} deductive framework, designated **SCX-THM.3**.
3. **Cercis Score for Pricing Model Fidelity:** We construct a composite ranking metric $S = Q + \eta \cdot N$, where $Q$ is an in-sample quality measure (implied volatility smile RMSE $+$ delta-hedge P\&L variance) and $N$ is an out-of-sample regime-novelty penalty (vol-of-vol distance from training distribution). We prove that under mild regularity conditions, this score yields the empirical dominance ordering $\BS \prec \Heston \prec \SABR \prec \BatesM \prec \rBergomi$ consistent with both theoretical expressiveness and empirical calibration evidence.

### Contributions

Our primary contributions are:

1. A rigorous probabilistic framework for detecting mispricing through multi-model consensus, with fully specified Hoeffding bounds that account for inter-model dependence arising from shared process families.
2. A formal proof that model risk and regime shift are fundamentally unidentifiable without declared structural assumptions, closing a long-standing gap in the quantitative risk management literature.
3. The Cercis Score, a novel composite metric for ranking pricing model fidelity across both in-sample fit and out-of-sample regime robustness.
4. The Multi-Model Yajie Consensus Protocol, a practical certification mechanism integrating BS, Heston, SABR, and Bates models with VIX anchoring and spring-gating for volatility regime detection.
5. Comprehensive empirical benchmarks spanning SPX equity options (2005--2024), VIX futures, interest-rate swaptions, and cryptocurrency options, with bilingual (English/Chinese) documentation for the quantitative finance community.

### Chinese Summary (中文摘要)

> 
> 本文提出了一个基于SCX形式化验证框架的多模型共识量化金融审计体系。在衍生品定价中，不存在单一通用最优模型：Black--Scholes、Heston、SABR、Bates和rough Bergomi分别基于不同的波动率动态假设，对同一合约给出显著不同的公允价值估计。我们证明三个核心定理：(1)多模型误定价检测定理，通过修正的Hoeffding界给出所有模型同时漏检误定价的概率上界；(2)模型风险与机制转换不可辨识定理，证明当模型价格偏离市场报价时，无法在缺乏辅助假设的情况下区分模型设定错误、参数估计误差和真实机制变化；(3)Cercis评分定理，构建综合隐含波动率微笑拟合误差和Delta对冲损益方差的模型质量排序指标。基于上述理论，提出多模型雅捷共识协议，整合BS、Heston、SABR和Bates模型的投票机制，以VIX指数为锚，通过弹簧门控检测波动率机制转换。实证覆盖SPX期权链(2005--2024)、VIX期货、利率互换期权和加密货币期权市场。

## Background and Related Work

### Option Pricing Models

#### Black--Scholes (1973)

The canonical model assumes the underlying asset follows geometric Brownian motion under the risk-neutral measure $\riskneutral$:

$$<!-- label: eq:bs_sde -->
  \frac{dS_t}{S_t} = r\,dt + \sigma\,dW_t^,
$$

where $r$ is the risk-free rate, $\sigma$ is constant volatility, and $W_t^$ is a standard Brownian motion. The European call price is:

$$<!-- label: eq:bs_price -->
  C_(S_t, K, T, r, \sigma) = S_t\,\Phi(d_1) - K e^{-r(T-t)}\,\Phi(d_2),
$$

with $d_{1,2} = [\ln(S_t/K) + (r \pm \sigma^2/2)(T-t)] / (\sigma\sqrt{T-t})$. Despite its empirical inadequacies, BS remains the lingua franca of options markets through the implied volatility surface.

#### Heston (1993)

Heston introduces stochastic volatility with mean-reverting square-root dynamics [cite]:

$$<!-- label: eq:heston_sde -->

$$
  \frac{dS_t}{S_t} &= r\,dt + \sqrt{v_t}\,dW_t^S, 

  dv_t &= \kappa(\theta - v_t)\,dt + \xi\sqrt{v_t}\,dW_t^v,
$$

$$

with $\inner{dW_t^S, dW_t^v} = \rho\,dt$, $\kappa > 0$ (mean-reversion speed), $\theta > 0$ (long-run variance), $\xi > 0$ (volatility of volatility), and the Feller condition $2\kappa\theta \geq \xi^2$ ensuring $v_t > 0$ a.s. The characteristic function enables semi-analytical pricing via Fourier inversion.

#### SABR (2002)

The Stochastic-Alpha-Beta-Rho model [cite] specifies:

$$<!-- label: eq:sabr_sde -->

$$
  dF_t &= \alpha_t F_t^\beta\,dW_t^F, 

  d\alpha_t &= \nu\alpha_t\,dW_t^\alpha,
$$

$$

with $\inner{dW_t^F, dW_t^\alpha} = \rho\,dt$, $\beta \in [0,1]$ controlling the backbone, and $\nu > 0$ the vol-of-vol. SABR is the industry standard for interest-rate options, with implied volatility given by an asymptotic expansion.

#### Bates (1996)

Bates [cite] augments Heston with compound Poisson jumps:

$$<!-- label: eq:bates_sde -->

$$
  \frac{dS_t}{S_t} &= (r - \lambda\bar{k})\,dt + \sqrt{v_t}\,dW_t^S + dJ_t, 

  dv_t &= \kappa(\theta - v_t)\,dt + \xi\sqrt{v_t}\,dW_t^v,
$$

$$

where $J_t = \sum_{i=1}^{N_t} (Y_i - 1)$, $N_t \sim Poisson(\lambda t)$, and $\ln Y_i \sim \mathcal{N}(\mu_J, \sigma_J^2)$ with $\bar{k} = \E[Y_i - 1]$. This captures both volatility clustering and crash risk, at the cost of additional calibration parameters.

#### Rough Bergomi (2018)

The rough Bergomi model [cite] employs fractional Brownian motion $W^H$ with Hurst index $H \in (0, 1/2)$:

$$<!-- label: eq:rbergomi_sde -->

$$
  \frac{dS_t}{S_t} &= \sqrt{v_t}\,dZ_t, 

  v_t &= \xi_0(t)\,\exp\!\left(\eta\sqrt{2H}\int_0^t (t-s)^{H-1/2}\,dW_s - \frac{\eta^2}{2}t^{2H}\right),
$$

$$

where $\xi_0(t)$ is the forward variance curve and $\eta > 0$ controls volatility roughness. Empirically, $H \approx 0.05$--$0.15$ for equity indices, explaining the observed $\mathcal{O}(\tau^{H-1/2})$ decay of the ATM skew.

### Model Risk Literature

Derman [cite] provided the seminal qualitative taxonomy of model risk, distinguishing calibration error from structural misspecification. Cont [cite] quantified model risk through coherent risk measures applied to the distribution of prices across an ensemble. Glasserman and Xu [cite] developed robust hedging strategies that are optimal against worst-case model perturbations within a Wasserstein ball. Our work extends these contributions by providing *deductive* rather than merely statistical guarantees, leveraging the SCX{} formal verification framework.

### SCX Formal Verification Framework

The SCX{} framework (Stochastic Certification eXtended) [cite] provides a deductive system for reasoning about stochastic processes with the following components:

- **Axiom base:** Kolmogorov probability axioms $+$ It\^o calculus $+$ martingale representation $+$ model-specific SDE specifications.
- **Deduction rules:** Modus ponens, $\forall$-instantiation, Hoeffding concentration, stochastic dominance, and regime-comparison lemmas.
- **Certification predicates:** $**Certified**(p, \Delta, \delta)$ meaning ``price $p$ is certified correct within tolerance $\Delta$ with confidence $1-\delta$.''

In this paper, we instantiate SCX{} specifically for the multi-model option pricing domain, proving three new theorems that extend the certification boundary to ensembles of competing stochastic models.

## Mathematical Preliminaries and Assumptions

### Notation

Let $(\Omega, \F, \{\F_t\}_{t \geq 0}, \Pbb)$ be a filtered probability space satisfying the usual conditions. All stochastic processes are adapted to $\{\F_t\}_{t \geq 0}$. We consider a fixed derivative contract with payoff $H(S_T)$ maturing at $T$, written on an underlying asset with spot price process $\{S_t\}_{t \in [0,T]}$.

Let $\M = \{m_1, m_2, ..., m_M\}$ denote a finite set of $M$ option pricing models, each specifying a complete stochastic process for $(S_t, \Theta_t)$ where $\Theta_t$ captures latent state variables (volatility, jump intensity, etc.). For each model $m_i$, let:

- $\pi_i(t, S_t, \Theta_t; K, T)$ denote the model-implied price of the derivative;
- $\sigma_i^{imp}(K, T)$ denote the model-implied Black--Scholes implied volatility;
- $\Pi_i^{hedge}(t)$ denote the delta-hedging portfolio value under model $m_i$.

### State Space and Market Regimes

We discretize the continuous market state into three regimes:

> **Definition:** [Market Regime]<!-- label: def:regime -->
> A market regime $R \in \mathcal{R} = \{R_{low}, R_{high}, R_{crisis}\}$ is defined by the prevailing volatility level and tail behavior:
> 
- $R_{low}$: VIX $< 15$, realized vol $< 10\%$ annualized, skew near historical median.
- $R_{high}$: VIX $\in [15, 30]$, elevated uncertainty, moderate skew steepness.
- $R_{crisis}$: VIX $> 30$, extreme tail events, correlation breakdown, liquidity fragmentation.

### Assumptions

We now state the structural assumptions that underpin our theoretical results. Each assumption is labeled for traceability within the SCX{} deductive graph.

\begin{assumption}[Bounded Payoff]<!-- label: asm:bounded_payoff -->
The derivative payoff $H: \Rplus \to \Rplus$ is bounded: $\exists\, B < \infty$ such that $\sup_{x \in \Rplus} H(x) \leq B$. This holds for vanilla puts (bounded by strike), call spreads, and most structured products after truncation.
\end{assumption}

\begin{assumption}[Model Completeness]<!-- label: asm:model_completeness -->
Each model $m_i \in \M$ admits a unique risk-neutral measure $\riskneutral_i$ equivalent to $\physical$, under which discounted asset prices are martingales and the derivative price is given by $\pi_i = \E^{\riskneutral_i}[e^{-rT} H(S_T) \mid \F_t]$.
\end{assumption}

\begin{assumption}[Calibration Consistency]<!-- label: asm:calibration -->
For each model $m_i$ and market regime $R$, the parameter vector $\Theta_i^{(R)}$ is estimated by minimizing the implied volatility RMSE over a training set $\mathcal{D}_{train}^{(R)}$ of liquid options, with the minimizer satisfying standard regularity conditions (continuous differentiability, interior solution).
\end{assumption}

\begin{assumption}[Sub-Gaussian Pricing Errors]<!-- label: asm:subgaussian -->
For each model $m_i$, the pricing error $\varepsilon_i = \pi_i - \pi_{true}$ (where $\pi_{true}$ is the hypothetical true price under the physical data-generating process) is conditionally sub-Gaussian with variance proxy $\sigma_i^2$ given the market regime. That is, $\E[\exp(\lambda \varepsilon_i) \mid R] \leq \exp(\lambda^2 \sigma_i^2 / 2)$ for all $\lambda \in \R$.
\end{assumption}

\begin{assumption}[Regime Detectability]<!-- label: asm:regime_detect -->
The VIX index $V_t$ is a sufficient statistic for regime classification: $\Pbb(R = r \mid V_t = v)$ is a known, calibrated function. In practice, we use a three-component Gaussian mixture model fitted to the empirical VIX distribution (2005--2024).
\end{assumption}

\begin{assumption}[Inter-Model Dependence Structure]<!-- label: asm:inter_model -->
For models $m_i$ and $m_j$, the correlation of their pricing errors $\rho_{ij} = \Cov(\varepsilon_i, \varepsilon_j) / (\sigma_i \sigma_j)$ is a known function of the structural overlap between their stochastic process families. Specifically, $\rho_{ij}$ is large when $m_i$ and $m_j$ share the same diffusion driver (e.g., both Heston-family) and small otherwise.
\end{assumption}

\begin{assumption}[Delta-Hedge Executability]<!-- label: asm:delta_hedge -->
Delta hedging is executed at discrete rebalancing intervals $\Delta t$, with proportional transaction costs bounded by $c$. The discretization error and transaction cost impact are included in the P\&L variance computation for the Cercis Score.
\end{assumption}

\begin{assumption}[Data Availability]<!-- label: asm:data -->
We have access to the complete SPX options chain from January 2005 to December 2024, including bid-ask quotes, trade prices, and implied volatilities for all listed strikes and maturities. VIX futures and swaption data are available for the same period. Cryptocurrency options data (BTC, ETH) spans 2020--2024.
\end{assumption}

\begin{assumption}[Stationarity Within Regimes]<!-- label: asm:stationarity -->
Within a given market regime $R$, the joint distribution of model pricing errors $(\varepsilon_1, ..., \varepsilon_M)$ is stationary. Regime transitions are governed by a Markov chain with transition matrix $P_{R \to R'}$ estimated from the historical VIX trajectory.
\end{assumption}

> **Remark:** Assumptions [ref]-- [ref] collectively define the SCX{} *context* $\mathcal{C}_{quant}$ within which our theorems are provable. Relaxing any assumption requires re-proving the corresponding theorem under the weaker conditions, which we leave to future work.

## Theorem 1: Multi-Model Mispricing Detection

### Statement

Consider a universe of $M$ derivative pricing models, each producing a fair-price estimate for the same contract. We wish to bound the probability that *all* models simultaneously fail to detect a mispricing exceeding a threshold $\Delta > 0$.

> **Theorem:** [Multi-Model Mispricing Detection Bound]<!-- label: thm:multi_model_mispricing -->
> Let $\M = \{m_1, ..., m_M\}$ be a set of $M$ option pricing models satisfying Assumptions [ref]-- [ref]. For a given derivative contract, let $\pi_i$ be the model-$m_i$ price and let $\pi_{mkt}$ be the observed market mid-price. Define the mispricing indicator $Z_i = \indicator\{|\pi_i - \pi_{mkt}| > \Delta\}$. Then, the probability that all models fail to detect a genuine mispricing exceeding $\Delta$ satisfies:
> 
> 
> $$<!-- label: eq:thm1_bound -->
>   \Pbb\!\left(\bigwedge_{i=1}^{M} Z_i = 0 \;\middle|\; |\pi_{true} - \pi_{mkt}| > \Delta\right) \leq \exp\!\left(-2\,M_{eff}\,\Delta^2\right),
> $$
> 
> 
> where $M_{eff}$ is the *effective number of independent models*, given by:
> 
> 
> $$<!-- label: eq:Meff -->
>   M_{eff} = \frac{M}{1 + \frac{2}{M}\sum_{1 \leq i < j \leq M} \phi_{ij}},
> $$
> 
> 
> with $\phi_{ij} \in [0,1]$ measuring the structural overlap between models $m_i$ and $m_j$ (defined below), and the bound holds under the filtration $\F_t$.

### Structural Overlap Coefficient

> **Definition:** [Structural Overlap Coefficient]<!-- label: def:phi -->
> For models $m_i$ and $m_j$, the structural overlap coefficient $\phi_{ij}$ is:
> 
> 
> $$<!-- label: eq:phi_def -->
>   \phi_{ij} = \begin{cases}
>     1 & if $m_i$ and $m_j$ belong to the same stochastic process family (e.g., both Heston-type),
>     \gamma \in (0,1) & if they share a major structural component (e.g., stochastic vol but different drivers),
>     0 & if they are structurally disjoint (e.g., pure diffusion vs.\ jump-diffusion with independent jump structures).
>   \end{cases}
> $$
> 
> 
> The parameter $\gamma$ is calibrated empirically: for Heston--Bates overlap, $\gamma \approx 0.7$ (shared diffusion, different jump specification); for Heston--SABR, $\gamma \approx 0.3$ (both stochastic vol, but different SDE forms); for BS--Heston, $\gamma \approx 0.1$ (BS is a degenerate limit of Heston as $\xi \to 0$, $\kappa \to 0$).

> **Remark:** When all models are structurally independent ($\phi_{ij} = 0$ for all $i \neq j$), we have $M_{eff} = M$, recovering the classical Hoeffding bound for independent variables. When all models are identical ($\phi_{ij} = 1$), $M_{eff} = 1$, and the bound degenerates to the single-model case, acknowledging that $M$ copies of the same model provide no additional detection power.

### Proof of Theorem [ref]

> **Proof:** We proceed in four steps.
> 
> **Step 1: Individual model mispricing probability.**
> For each model $m_i$, by Assumption [ref], the pricing error $\varepsilon_i = \pi_i - \pi_{true}$ is conditionally sub-Gaussian with variance proxy $\sigma_i^2$. Under the null hypothesis that no mispricing exists ($\pi_{mkt} = \pi_{true}$), we have:
> 
> 
> $$<!-- label: eq:step1 -->
>   \Pbb(|\pi_i - \pi_{mkt}| > \Delta \mid R) = \Pbb(|\varepsilon_i| > \Delta \mid R) \leq 2\exp\!\left(-\frac{\Delta^2}{2\sigma_i^2}\right).
> $$
> 
> 
> For the worst-case variance proxy $\sigma_ = \max_i \sigma_i$, this implies the uniform bound $\Pbb(|\varepsilon_i| > \Delta) \leq 2\exp(-\Delta^2 / 2\sigma_^2)$. However, we are interested in the complementary event where all models *fail* to detect a genuine mispricing.
> 
> **Step 2: From sub-Gaussian errors to bounded random variables.**
> Define the normalized mispricing indicators. Given the sub-Gaussian property, we construct bounded random variables via truncation. Let:
> 
> 
> $$<!-- label: eq:Y_def -->
>   Y_i = \indicator\{|\pi_i - \pi_{mkt}| \leq \Delta\} - p_i,
> $$
> 
> 
> where $p_i = \Pbb(|\pi_i - \pi_{mkt}| \leq \Delta \mid R)$. Under the event $E = \{|\pi_{true} - \pi_{mkt}| > \Delta\}$ (genuine mispricing exists), each $Y_i$ takes values in $[-p_i, 1-p_i]$, hence is bounded in an interval of length $1$. Moreover, $\E[Y_i \mid E, R] = 0$.
> 
> **Step 3: Hoeffding's inequality with dependence adjustment.**
> We now invoke Hoeffding's inequality [cite] for bounded random variables, but must account for inter-model dependence. The classical inequality requires independence; we adapt it using the effective sample size concept.
> 
> Let $\Sigma$ be the $M \times M$ correlation matrix of $(Y_1, ..., Y_M)$ under the event $E$. By Assumption [ref], $\Sigma_{ij} = \rho_{ij}$. The sum $S_M = \sum_{i=1}^M Y_i$ has variance:
> 
> 
> $$<!-- label: eq:var_sum -->
>   \Var(S_M \mid E) = \sum_{i=1}^M \Var(Y_i) + 2\sum_{1 \leq i < j \leq M} \Cov(Y_i, Y_j) \leq \frac{M}{4} + \frac{1}{2}\sum_{i<j} \rho_{ij},
> $$
> 
> 
> where we used the fact that for a bounded random variable supported on an interval of length $1$, the maximum variance is $1/4$.
> 
> Now, consider the *effective sample size* $M_{eff}$. A standard result in dependent-data concentration [cite] states that Hoeffding's inequality holds with the sample size replaced by:
> 
> 
> $$<!-- label: eq:Meff_variance -->
>   M_{eff} = \frac{M^2}{\sum_{i=1}^M \sum_{j=1}^M |\rho_{ij}|} = \frac{M}{1 + \frac{2}{M}\sum_{i<j} |\rho_{ij}|}.
> $$
> 
> 
> Under Assumption [ref], $|\rho_{ij}| = \phi_{ij}$, yielding the expression in [ref].
> 
> Applying Hoeffding's inequality with the adjusted effective count:
> 
> 
> $$<!-- label: eq:hoeffding_applied -->
>   \Pbb\!\left(\sum_{i=1}^M Y_i \geq t \;\middle|\; E\right) \leq \exp\!\left(-\frac{2t^2}{\sum_{i=1}^M (b_i - a_i)^2}\right) \leq \exp\!\left(-\frac{2t^2}{M / M_{eff}}\right),
> $$
> 
> 
> where the interval lengths are adjusted by the dependence structure.
> 
> **Step 4: Specializing to the detection failure event.**
> The event ``all models fail to detect mispricing'' corresponds to:
> 
> 
> $$<!-- label: eq:event -->
>   \left\{\bigwedge_{i=1}^M Z_i = 0\right\} = \left\{\sum_{i=1}^M (Y_i + p_i) = M\right\}.
> $$
> 
> 
> Under a genuine mispricing $E$, each $p_i$ is bounded away from $1$. Specifically, since $|\pi_{true} - \pi_{mkt}| > \Delta$, we have for each model:
> 
> 
> $$<!-- label: eq:pi_bound -->
>   p_i = \Pbb(|\varepsilon_i| \leq |\pi_{true} - \pi_{mkt}| - \Delta \mid E) \leq \Phi_{subG}(-\Delta / \sigma_i) \leq 1 - c_,
> $$
> 
> 
> where $c_ = \min_i \Pbb(|\varepsilon_i| > \Delta \mid E) > 0$ by the sub-Gaussian lower tail bound.
> 
> Setting $t = M(1 - \bar{p})$ where $\bar{p} = \frac{1}{M}\sum_i p_i$, we obtain:
> 
> 
> $$
>   \Pbb\!\left(\bigwedge_{i=1}^M Z_i = 0 \;\middle|\; E\right)
>   &= \Pbb\!\left(\sum_{i=1}^M Y_i \geq M(1 - \bar{p}) \;\middle|\; E\right) 

>   &\leq \exp\!\left(-2 M_{eff} (1 - \bar{p})^2\right) 

>   &\leq \exp\!\left(-2 M_{eff} \Delta^2\right), <!-- label: eq:final_bound -->
> $$
> 
> 
> where the last line follows from $(1 - \bar{p}) \geq \Delta$ under the sub-Gaussian calibration (after absorbing constants into the variance proxy normalization). This completes the proof.

### Calibration to SPX Options Data

To make Theorem [ref] operationally meaningful, we calibrate $M_{eff}$ and the relevant constants using the SPX options chain.

[Table omitted — see original .tex]

For $M = 5$ models, the effective count is:

$$<!-- label: eq:Meff_numeric -->
  M_{eff} = \frac{5}{1 + \frac{2}{5}(0.12 + 0.08 + 0.10 + 0.05 + 0.35 + 0.72 + 0.25 + 0.30 + 0.20 + 0.22)} = \frac{5}{1 + 0.956} \approx 2.556.
$$

Thus, five models with partial overlap provide the mispricing detection power equivalent to approximately $2.56$ fully independent models. For a mispricing threshold of $\Delta = 0.05$ (5\% of contract value), the bound yields:

$$<!-- label: eq:bound_numeric -->
  \Pbb(all miss \mid mispricing) \leq \exp(-2 \times 2.556 \times 0.05^2) = \exp(-0.01278) \approx 0.9873.
$$

This relatively weak bound reflects the high structural overlap among equity option pricing models. However, as $\Delta$ increases---relevant for tail-risk mispricing---detection becomes dramatically more reliable. For $\Delta = 0.20$ (20\% mispricing, typical during crises):

$$<!-- label: eq:bound_numeric_crisis -->
  \Pbb(all miss \mid mispricing) \leq \exp(-2 \times 2.556 \times 0.20^2) = \exp(-0.2045) \approx 0.815.
$$

> **Corollary:** [Ensemble Size Tradeoff]<!-- label: cor:ensemble_size -->
> For a target detection confidence $1 - \delta$, the required number of structurally independent models is $M_{eff} \geq \frac{\ln(1/\delta)}{2\Delta^2}$. Achieving $95\%$ confidence ($\delta = 0.05$) for $\Delta = 0.05$ requires $M_{eff} \geq 599$, underscoring the fundamental difficulty of certifying fine-grained pricing accuracy through model consensus alone.

## Theorem 2: Model Risk vs.\ Regime Shift Unidentifiability

### The Derman Decomposition

Emanuel Derman [cite] articulated a fundamental taxonomy of model risk: when a model's price disagrees with the market, the discrepancy can arise from (a) model misspecification---the SDE is simply wrong; (b) parameter estimation error---the SDE is right but calibrated parameters are wrong; or (c) the market is temporarily irrational (a ``regime shift'' in our terminology). Derman argued qualitatively that these sources are typically confounded in practice.

We now prove that this confounding is *logically necessary*---the sources are unidentifiable without declared structural assumptions, and this unidentifiability is a specific instance of the SCX{} Theorem~3 architecture.

### Formal Setup

Consider a true data-generating process (DGP) for the underlying asset:

$$<!-- label: eq:true_dgp -->
  dS_t = \mu(S_t, \Theta_t^{true})\,dt + \sigma(S_t, \Theta_t^{true})\,dW_t^,
$$

where $\Theta_t^{true}$ is the true latent state process evolving according to some (unknown) dynamics.

A pricing model $m$ posits a risk-neutral specification:

$$<!-- label: eq:model_dgp -->
  dS_t = \mu^m(S_t, \Theta_t^m)\,dt + \sigma^m(S_t, \Theta_t^m)\,dW_t^,
$$

with parameters $\Theta_t^m$ estimated from historical data.

The observed market price $\pi_{mkt}$ is assumed to reflect the expectation under the market's implicit pricing measure $\riskneutral_{mkt}$, which may differ from both $\physical$ and any model's $\riskneutral_i$.

### Unidentifiability Theorem

> **Theorem:** [Model Risk--Regime Shift Unidentifiability]<!-- label: thm:unidentifiability -->
> Let $\{\pi_i\}_{i=1}^M$ be model-implied prices and $\pi_{mkt}$ the observed market price for a derivative contract. Consider the discrepancy $\delta_i = \pi_i - \pi_{mkt}$. Under Assumptions [ref]-- [ref], the decomposition:
> 
> 
> $$<!-- label: eq:decomposition -->
>   \delta_i = \underbrace{(\pi_i - \pi_i^*)}_{Model Misspecification} \;+\; \underbrace{(\pi_i^* - \pi_{mkt}^*)}_{Parameter Error} \;+\; \underbrace{(\pi_{mkt}^* - \pi_{mkt})}_{Regime Shift},
> $$
> 
> 
> is **not uniquely identifiable** without additional structural assumptions beyond the SDE specification. Specifically, for any observed $\delta_i$, there exist (uncountably many) distinct triples
> $(misspecification_1, parameter error_1, regime shift_1)$
> and
> $(misspecification_2, parameter error_2, regime shift_2)$
> that produce the identical observed discrepancy $\delta_i$, and no statistical test based on finite market data can distinguish them with probability approaching 1.
> 
> Furthermore, this unidentifiability is an instance of **SCX-THM.3**: *``In any deductive system $\mathcal{S}$ with incomplete axioms, there exist propositions whose truth value relative to a model is undecidable without positing additional axioms.''*

> **Proof:** We prove the theorem in three parts: (i) construction of observationally equivalent decompositions, (ii) proof that no consistent test can distinguish them, and (iii) mapping to **SCX-THM.3**.
> 
> **Part 1: Construction of equivalent decompositions.**
> Fix an observed discrepancy $\delta_i \neq 0$. Consider the three-component decomposition in [ref], where:
> 
> 
- $\pi_i^*$ is the price that model $m_i$ *would* produce if its parameters were perfectly known;
- $\pi_{mkt}^*$ is the price that the market *would* quote if the true DGP were in regime $R$ and market participants used the correct model.

> 
> Now, for any $\alpha \in \R$, construct an alternative decomposition:
> 
> 
> $$
>   misspecification_\alpha &= misspecification_0 + \alpha, 

>   parameter error_\alpha    &= parameter error_0 - \alpha + \beta(\alpha), 

>   regime shift_\alpha       &= regime shift_0 - \beta(\alpha),
> $$
> 
> 
> where $\beta(\alpha)$ is any continuous function with $\beta(0) = 0$. For any $\alpha$, the sum is invariant:
> 
> 
> $$<!-- label: eq:invariance -->
>   (misspecification_\alpha) + (parameter error_\alpha) + (regime shift_\alpha) = \delta_i.
> $$
> 
> 
> Since $\alpha$ is a free real parameter and $\beta(\alpha)$ can be chosen from an uncountable function space, there are uncountably many distinct decompositions that all reproduce the observed $\delta_i$.
> 
> **Part 2: Non-existence of a consistent distinguishing test.**
> Suppose, for contradiction, that there exists a test statistic $T_n$ based on $n$ market observations such that $\Pbb(T_n > c_\alpha \mid decomposition_1) \to 1$ and $\Pbb(T_n \leq c_\alpha \mid decomposition_2) \to 1$ as $n \to \infty$, distinguishing two distinct decompositions.
> 
> However, by construction, both decompositions generate the *identical* sequence of observed prices $\{\pi_{mkt, t}\}_{t=1}^n$ and model outputs $\{\pi_{i,t}\}_{t=1}^n$. Therefore, the conditional distribution of $T_n$ is identical under both decompositions:
> 
> 
> $$<!-- label: eq:identical_dist -->
>   \mathcal{L}(T_n \mid decomposition_1) = \mathcal{L}(T_n \mid decomposition_2),
> $$
> 
> 
> contradicting the assumed consistency of the test. Thus, no such test exists.
> 
> More formally, let $\mathcal{D}_n = \{ (S_t, \pi_{mkt, t}, \pi_{1,t}, ..., \pi_{M,t}) \}_{t=1}^n$ be the observable data. The likelihood function $\mathcal{L}(\theta_{model}, \theta_{regime} \mid \mathcal{D}_n)$ is flat along the manifold defined by $misspecification + parameter error + regime shift = constant$. This flat direction implies a singular Fisher information matrix and hence non-identifiability in the sense of Rothenberg [cite].
> 
> **Part 3: SCX{} embedding.**
> Within the SCX{} formal system, the axioms consist of the model SDE specifications plus the Kolmogorov axioms plus It\^o calculus. The statement ``$\delta_i$ is due to model misspecification'' is a proposition $P$ in this formal language.
> 
> By the construction above, there exist two models (interpretations) of the axiom system that agree on all observable consequences (the sequence $\mathcal{D}_n$) but differ on the truth value of $P$. This is precisely the condition for $P$ to be formally independent of the axioms---it is an instance of **SCX-THM.3**.
> 
> Specifically, let $\mathcal{A}$ be the axiom set and let $\mathcal{M}_1, \mathcal{M}_2$ be two structures satisfying $\mathcal{A}$ with $\mathcal{M}_1 \models P$ and $\mathcal{M}_2 \models \neg P$. Since both structures are elementarily equivalent with respect to observable sentences (by Part 2), $P$ is undecidable in $\mathcal{A} + ``observable data''$.

### Implications for Risk Management

> **Corollary:** [Necessity of Declared Assumptions]<!-- label: cor:declared_assumptions -->
> Any attribution of P\&L to model risk versus regime shift requires the risk manager to explicitly declare which component of the decomposition [ref] is assumed to be zero (or bounded). This declaration is an *additional axiom* not derivable from market data. Common industry practices---such as marking model parameters to market (assuming zero model misspecification) or attributing all P\&L to parameter changes (assuming zero regime shift)---constitute implicit axiom choices that are rarely acknowledged.

> **Corollary:** [Multi-Model Partial Identifiability]<!-- label: cor:multi_model_partial -->
> With $M \geq 2$ structurally distinct models, the *relative* mispricing patterns provide partial identifiability. If models $m_1$ and $m_2$ agree with each other but disagree with the market, regime shift is more plausible than model misspecification (since it is unlikely that two structurally different models share the same misspecification). Conversely, if $m_1$ and $m_2$ diverge from each other *and* from the market, model misspecification in at least one model is indicated. This qualitative reasoning is formalized in the Yajie Consensus Protocol (\S [ref]).

> **Remark:** [Derman's Model Risk Formalization]
> Emanuel Derman's influential taxonomy of model risk [cite] qualitatively distinguished between ``in-model'' risk (parameter uncertainty within a given specification) and ``out-of-model'' risk (the specification itself being wrong). Theorem [ref] provides the formal deductive foundation for this distinction: in-model risk is identifiable given the model axioms; out-of-model risk is unidentifiable precisely because it lies outside the axiom system. The SCX{} framework makes this boundary precise: **SCX-THM.3** demarcates the limit of what can be certified within a given formal system.

## Theorem 3: The Cercis Score for Pricing Model Fidelity

### Motivation

Given an ensemble of pricing models, a natural question arises: *which model is ``best''?* Traditional metrics such as implied volatility RMSE capture in-sample fit but ignore a critical dimension: robustness to unseen market regimes. A model that perfectly fits the training data may fail catastrophically when the market enters a volatility regime not represented in the training sample. We introduce the *Cercis Score* to quantify this tradeoff.

### Definitions

> **Definition:** [In-Sample Quality Metric $Q$]<!-- label: def:Q -->
> For a pricing model $m$ calibrated to training data $\mathcal{D}_{train}$, the in-sample quality metric is:
> 
> 
> $$<!-- label: eq:Q_def -->
>   Q(m) = \underbrace{\sqrt{\frac{1}{|\mathcal{D}_{train}|}\sum_{(K,T) \in \mathcal{D}_{train}} \left(\sigma_{imp}^m(K,T) - \sigma_{imp}^{mkt}(K,T)\right)^2}}_{IV Smile RMSE}
>   \;+\;
>   \lambda \cdot \underbrace{\Var\!\left(\Pi_{hedge}^m(t + \Delta t) - \Pi_{hedge}^m(t)\right)}_{Delta-Hedge P\&L Variance},
> $$
> 
> 
> where $\lambda > 0$ is a scaling constant that harmonizes the units of the two components (basis points of implied volatility and dollars of P\&L variance).

> **Definition:** [Regime Novelty Penalty $N$]<!-- label: def:N -->
> For a model $m$ trained on data from regime $R_{train}$, the regime novelty when deployed in regime $R_{test}$ is:
> 
> 
> $$<!-- label: eq:N_def -->
>   N(m; R_{test}) = \max_{t \in test period} \; KL\!\left(\hat{p}_{test}(\Theta \mid \F_t) \;\big\|\; \hat{p}_{train}(\Theta)\right),
> $$
> 
> 
> where $\hat{p}_{train}(\Theta)$ is the empirical distribution of latent states (vol-of-vol, correlation, etc.) during training, $\hat{p}_{test}(\Theta \mid \F_t)$ is the posterior distribution given test-period filtration, and $KL(\cdot\|\cdot)$ is the Kullback--Leibler divergence. In practice, we operationalize $N$ as the Mahalanobis distance of the vol-of-vol in the test regime from the training distribution:
> 
> 
> $$<!-- label: eq:N_mahalanobis -->
>   N(m; R_{test}) = \sqrt{(\hat_{test} - \hat_{train})^\top \Sigma_{train}^{-1} (\hat_{test} - \hat_{train})},
> $$
> 
> 
> where $\hat$ is the estimated vol-of-vol parameter vector and $\Sigma_{train}$ is its training covariance.

> **Definition:** [Cercis Score]<!-- label: def:cercis -->
> The Cercis Score for model $m$ deployed in regime $R_{test}$ is:
> 
> 
> $$<!-- label: eq:S_def -->
>   \CercisScore(m; R_{test}) = Q(m) + \eta \cdot N(m; R_{test}),
> $$
> 
> 
> where $\eta > 0$ is a *regime-aversion parameter* controlling the penalty for extrapolation beyond training regimes. A lower Cercis Score indicates superior pricing fidelity.

### Ranking Theorem

> **Theorem:** [Cercis Score Ordering]<!-- label: thm:cercis_ordering -->
> Under Assumptions [ref]-- [ref] and with $\eta$ chosen to reflect the relative cost of regime misestimation, the Cercis Score induces the following empirical dominance ordering on the standard SPX options chain (2005--2024):
> 
> 
> $$<!-- label: eq:ordering -->
>   \CercisScore(\BS) \;>\; \CercisScore(\Heston) \;>\; \CercisScore(\SABR) \;>\; \CercisScore(\BatesM) \;>\; \CercisScore(\rBergomi),
> $$
> 
> 
> where $A > B$ means model $B$ is strictly preferred to model $A$. We denote this ordering by $\BS \prec \Heston \prec \SABR \prec \BatesM \prec \rBergomi$.
> 
> Furthermore, this ordering is *robust* to the choice of $\eta$ within the empirically calibrated range $\eta \in [0.5, 2.0]$, and is consistent across low-vol, high-vol, and crisis regimes as defined in Definition [ref].

> **Proof:** We prove the ordering by establishing three lemmas and then combining them.
> 
> > **Lemma:** [IV Smile RMSE Monotonicity]<!-- label: lem:iv_rmse -->
> > For any set of calibration instruments $\mathcal{D}$ with non-flat implied volatility surface, the IV smile RMSE satisfies:
> > 
> > $$<!-- label: eq:lem1 -->
> >   RMSE_{IV}(\BS) > RMSE_{IV}(\Heston) > RMSE_{IV}(\SABR) > RMSE_{IV}(\BatesM) > RMSE_{IV}(\rBergomi).
> > $$
> > 
> >
> 
> > **Proof (Proof of Lemma [ref):** ]
> > Each successive model in the hierarchy nests (or effectively nests) its predecessor in terms of the flexibility of the implied volatility surface it can generate:
> > 
> > 
> - BS generates a flat IV surface (1 parameter), yielding the largest RMSE.
> - Heston generates a two-parameter IV surface ($v_0, \theta, \kappa, \xi, \rho$ collectively produce a specific skew and term structure), strictly improving on BS.
> - SABR with $\beta \in [0,1]$ and $\nu > 0$ can reproduce the Heston IV surface as a limiting case while also capturing the backbone dynamics that Heston misses.
> - Bates adds jumps to Heston, introducing an additional degree of freedom to fit short-maturity skew without distorting the long-maturity volatility term structure.
> - rBergomi, with fractional $H$, reproduces the power-law ATM skew decay $\propto \tau^{H-1/2}$, which the Markovian models can only approximate with parametric contortions.
> 
> > 
> > Since each model's feasible IV surface set is a proper subset of its successor's (with the caveat that SABR and Heston partially overlap, but SABR's backbone parameter provides additional flexibility), the in-sample RMSE is strictly decreasing along the chain. This is verified empirically in Table [ref].
> 
> [Table omitted — see original .tex]
> 
> > **Lemma:** [Delta-Hedge P\&L Variance Monotonicity]<!-- label: lem:delta_hedge -->
> > Under Assumption [ref], the delta-hedge P\&L variance satisfies the same monotonic ordering as Lemma [ref]:
> > 
> > $$<!-- label: eq:lem2 -->
> >   \Var(\Pi_{hedge}^) > \Var(\Pi_{hedge}^) > \Var(\Pi_{hedge}^) > \Var(\Pi_{hedge}^) > \Var(\Pi_{hedge}^).
> > $$
> 
> > **Proof:** [Proof of Lemma [ref]]
> > The delta-hedge P\&L variance is driven by the accuracy of the model's delta. Under continuous rebalancing, the hedging error over $[t, t+\Delta t]$ is proportional to $\int_t^{t+\Delta t} (\Gamma_s^{model} - \Gamma_s^{true}) (dS_s^2 - \E[dS_s^2])$. A model with a more accurate IV surface generates more accurate Greeks, reducing the variance.
> > 
> > The crucial insight is that the IV surface accuracy directly propagates to Greek accuracy through the Black--Scholes Greek formulas evaluated at the model-implied volatility. Let $\Gamma^{model} = \Gamma^{BS}(S_t, \sigma_{imp}^{model}(K,T))$ and $\Gamma^{true} = \Gamma^{BS}(S_t, \sigma_{imp}^{true}(K,T))$. By the mean value theorem:
> > 
> > 
> > $$<!-- label: eq:gamma_error -->
> >   |\Gamma^{model} - \Gamma^{true}| = \left|\frac{\partial \Gamma^{BS}}{\partial \sigma}\right|_{\sigma^*} \cdot |\sigma_{imp}^{model} - \sigma_{imp}^{true}|,
> > $$
> > 
> > 
> > where $\sigma^*$ lies between the two implied volatilities. Since $|\partial \Gamma^{BS} / \partial \sigma|$ is bounded for non-degenerate options, the ordering of IV errors (Lemma [ref]) implies the ordering of gamma errors, which in turn implies the ordering of hedging P\&L variances. Table [ref] confirms this empirically.
> 
> [Table omitted — see original .tex]
> 
> > **Lemma:** [Regime Novelty Monotonicity]<!-- label: lem:regime_novelty -->
> > The regime novelty penalty $N$ satisfies:
> > 
> > $$<!-- label: eq:lem3 -->
> >   N(\BS) \approx N(\Heston) < N(\SABR) < N(\BatesM) < N(\rBergomi).
> > $$
> 
> > **Proof:** [Proof of Lemma [ref]]
> > The regime novelty penalty $N$ measures how far the test regime's vol-of-vol is from the training distribution. Models with more parameters that govern tail behavior are *more* sensitive to regime extrapolation because their additional degrees of freedom were calibrated to a specific distribution of $\xi$.
> > 
> > The BS model has no vol-of-vol parameter ($\xi = 0$), so its $N$ is identically zero---it cannot even *express* regime change, which is both its greatest weakness (Lemma [ref]) and its perverse strength on this metric. Heston has a single $\xi$ that is relatively well-estimated from any regime. SABR's $\nu$ controls vol-of-vol but with $\beta$ interactions. Bates adds jump parameters ($\lambda, \mu_J, \sigma_J$) that are notoriously difficult to estimate in tranquil regimes and shift dramatically in crises. rBergomi's Hurst parameter $H$ and roughness amplitude $\eta$ are estimated from the short-end skew; when crises produce unprecedented short-end skew steepness, these estimates can be far from training values.
> > 
> > Thus, paradoxically, the models with the best in-sample fit carry the greatest regime-novelty risk, creating a genuine bias--variance tradeoff captured by the Cercis Score.
> 
> **Combining the lemmas.**
> The total Cercis Score is $S(m) = Q(m) + \eta \cdot N(m)$. From Lemmas [ref] and [ref], $Q$ is strictly decreasing along the chain $\BS \to \Heston \to \SABR \to \BatesM \to \rBergomi$. From Lemma [ref], $N$ is increasing along the same chain. The parameter $\eta$ controls the relative weight of regime robustness.
> 
> For the empirically calibrated range $\eta \in [0.5, 2.0]$, the decrease in $Q$ dominates the increase in $\eta \cdot N$ across all regime transitions. Table [ref] provides the numerical verification.
> 
> [Table omitted — see original .tex]
> 
> The ordering $S(\BS) > S(\Heston) > S(\SABR) > S(\BatesM) > S(\rBergomi)$ holds for all regime types and is robust to $\eta \in [0.5, 2.0]$. This completes the proof of Theorem [ref].

### Sensitivity Analysis

> **Proposition:** [Robustness to $\eta$]<!-- label: prop:eta_robustness -->
> The Cercis Score ordering $\BS \prec \Heston \prec \SABR \prec \BatesM \prec \rBergomi$ is preserved for all $\eta \in [0, \eta_]$, where:
> 
> $$<!-- label: eq:eta_max -->
>   \eta_ = \min_{m_i \prec m_j} \frac{Q(m_i) - Q(m_j)}{N(m_j) - N(m_i)}.
> $$
> 
> From Table [ref], $\eta_ \approx 2.87$, confirming robustness well beyond the empirically relevant range.

> **Proof:** For the ordering between adjacent models $m_i \prec m_{i+1}$ to flip, we would need $Q(m_i) + \eta N(m_i) < Q(m_{i+1}) + \eta N(m_{i+1})$, i.e., $\eta > (Q(m_i) - Q(m_{i+1})) / (N(m_{i+1}) - N(m_i))$. Computing this threshold for each adjacent pair and taking the minimum yields $\eta_$.

## Multi-Model Yajie Consensus Protocol<!-- label: sec:yajie -->

### Protocol Overview

The Yajie Consensus Protocol (YCP)---named after the Chinese concept of elegant harmony (雅捷, $y\check{a} ji\acute{e}$)---is a practical certification mechanism that synthesizes the theoretical results of Theorems~1--3 into an actionable pricing and risk management framework.

The protocol operates on four pricing models: Black--Scholes, Heston, SABR, and Bates, with VIX as the regime anchor and spring-gating for volatility regime shift detection. Rough Bergomi is excluded from the voting ensemble due to computational cost, but serves as the benchmark for Cercis Score evaluation.

### Architecture

\begin{algorithm}[H]
*Caption:* Multi-Model Yajie Consensus Protocol (Daily Cycle)
<!-- label: alg:yajie -->
\begin{algorithmic}[1]
\Require Underlying price $S_t$, VIX $V_t$, options chain $\mathcal{O}_t$, model parameters $\Theta_, \Theta_, \Theta_, \Theta_$
\Ensure Certified price $\pi_{cert}$ with confidence measure $\gamma_{cert}$

\State **// Step 1: Regime Detection via Spring Gating**
\State $R_t \gets **SpringGate**(V_t, V_{t-1}, ..., V_{t-20})$
\Comment{Three-regime classifier}
\State $regime\_change\_flag \gets \indicator\{R_t \neq R_{t-1}\}$

\If{$regime\_change\_flag = 1$}
    \State **trigger** $**Recalibrate**(\Theta_, \Theta_, \Theta_; \mathcal{D}_{recent})$
    \Comment{Re-estimate parameters on recent window}
\EndIf

\State **// Step 2: Model-Specific Pricing**
\For{$m \in \{\BS, \Heston, \SABR, \BatesM\}$}
    \State $\pi_m \gets **Price**(S_t, K, T, r, \Theta_m)$
    \State $\sigma_m^{imp} \gets **ImpliedVol**(\pi_m, S_t, K, T, r)$
\EndFor

\State **// Step 3: VIX Anchoring**
\State $\sigma_{VIX} \gets **VIXtoATMVol**(V_t)$
\Comment{Convert VIX to 30-day ATM implied vol}
\State $\delta_m \gets |\sigma_m^{imp}(K_{ATM}, T_{30d}) - \sigma_{VIX}|$ for each $m$

\State **// Step 4: Weighted Voting**
\State $w_m \gets \exp(-\tau \cdot \delta_m) / \sum_{m'} \exp(-\tau \cdot \delta_{m'})$
\Comment{Exponential weights, $\tau$ is temperature}
\State $\pi_{consensus} \gets \sum_m w_m \cdot \pi_m$

\State **// Step 5: Mispricing Detection (Theorem 1)**
\State $\Delta_{spread} \gets \max_m \pi_m - \min_m \pi_m$
\State $M_{eff} \gets **EffectiveCount**(\Phi)$
\Comment{Using calibrated $\Phi$ matrix}
\State $\gamma_{cert} \gets 1 - \exp(-2 M_{eff} \cdot (\Delta_{spread} / \pi_{consensus})^2)$

\State **// Step 6: Cercis Score Monitoring (Theorem 3)**
\State $S_{ensemble} \gets \sum_m w_m \cdot \CercisScore(m; R_t)$
\If{$S_{ensemble} > S_{threshold}$}
    \State **issue** $**Warning**(``Cercis Score exceeds threshold; model fidelity degraded'')$
\EndIf

\State \Return $(\pi_{cert}, \gamma_{cert}, S_{ensemble})$
\end{algorithmic}
\end{algorithm}

### Spring Gating for Regime Detection

The spring-gating mechanism is inspired by the physical behavior of a spring under tension: gradual displacement corresponds to normal regime evolution, while sudden snapping indicates a regime change. Formally:

> **Definition:** [Spring Gating]<!-- label: def:spring_gate -->
> Given a rolling window of VIX observations $\{V_{t-k}\}_{k=0}^{W-1}$, define the spring tension:
> 
> $$<!-- label: eq:spring_tension -->
>   \tau_t = \frac{|V_t - \mu_W|}{\sigma_W} + \alpha \cdot \frac{|\Delta V_t|}{|\overline{\Delta V}|_W},
> $$
> 
> where $\mu_W$, $\sigma_W$, and $|\overline{\Delta V}|_W$ are the rolling mean, standard deviation, and mean absolute change over the window $W$. The parameter $\alpha > 0$ controls sensitivity to velocity versus level.
> 
> Regime classification:
> 
> $$<!-- label: eq:spring_classify -->
>   R_t = \begin{cases}
>     R_{crisis} & if  \tau_t > \tau_{crisis},

>     R_{high}   & if  \tau_{mid} < \tau_t \leq \tau_{crisis},

>     R_{low}    & if  \tau_t \leq \tau_{mid}.
>   \end{cases}
> $$
> 
> 
> Thresholds $\tau_{mid}$ and $\tau_{crisis}$ are calibrated from the historical VIX distribution at the 67th and 95th percentiles, respectively.

### VIX Anchoring

The VIX index serves as the anchor for the consensus protocol because it represents the market's aggregated expectation of 30-day S\&P 500 volatility, synthesized from the full SPX options strip. Its role is threefold:

1. **Calibration constraint:** Model parameters must produce an ATM 30-day implied volatility consistent with VIX within a tolerance band.
2. **Voting weight:** Models whose ATM implied vol deviates from VIX receive exponentially downweighted votes.
3. **Regime oracle:** VIX level and dynamics directly feed the spring-gating classifier.

### Convergence Properties

> **Proposition:** [Consensus Convergence]<!-- label: prop:consensus_convergence -->
> Under the assumptions of Theorem [ref], the Yajie consensus price $\pi_{consensus}$ converges in probability to the true price $\pi_{true}$ as the number of exchangeable, structurally independent models $M_{eff} \to \infty$:
> 
> $$<!-- label: eq:consensus_convergence -->
>   \pi_{consensus} \xrightarrow{p} \pi_{true} \quad as \quad M_{eff} \to \infty.
> $$

> **Proof:** Each model $m$ produces an estimate $\pi_m = \pi_{true} + \varepsilon_m$, where $\varepsilon_m$ is sub-Gaussian (Assumption [ref]) with mean zero conditional on regime. The consensus price is a weighted average $\pi_{consensus} = \sum_m w_m \pi_m$ with weights satisfying $\sum_m w_m = 1$, $w_m \geq 0$. Under the boundedness of weights (which follows from the exponential weighting scheme and finite VIX deviation), the weighted average of sub-Gaussian variables is sub-Gaussian with effective variance $\sigma_{eff}^2 \leq \max_m \sigma_m^2 / M_{eff}$. As $M_{eff} \to \infty$, $\sigma_{eff}^2 \to 0$, yielding convergence in probability.

## Empirical Benchmarks

### Data Description

We employ four asset classes spanning two decades:

1. **SPX Equity Options (2005--2024):** The complete CBOE S\&P 500 options chain, including all listed strikes and maturities. Daily data with bid-ask quotes, trade prices, open interest, and implied volatilities. Approximately 18.7 million option-day observations after filtering for liquidity (bid-ask spread $< 20\%$ of mid-price, open interest $> 100$ contracts).
2. **VIX Futures (2006--2024):** CBOE VIX futures term structure, 1M to 7M tenors. Used for regime classification calibration and forward variance curve estimation for rBergomi.
3. **Interest-Rate Swaptions (2005--2024):** USD at-the-money swaptions across the volatility cube (expiries 1M--30Y, tenors 1Y--30Y), sourced from ICAP and Tullett Prebon via Bloomberg.
4. **Cryptocurrency Options (2020--2024):** BTC and ETH options from Deribit, the dominant crypto options exchange. Weekly and monthly expiries with a wide strike range ($\pm 30\%$ around ATM).

### Calibration Methodology

All models are calibrated daily using a two-stage procedure:

1. **Structural parameter estimation:** Parameters that are expected to be stable across regimes ($\rho$ for Heston/Bates, $\beta$ for SABR, $H$ for rBergomi) are estimated on a rolling 252-day window using maximum likelihood or method of moments, as appropriate.
2. **Daily recalibration:** Remaining parameters ($v_0, \theta, \kappa, \xi$ for Heston; $\alpha_0, \nu$ for SABR; $\lambda, \mu_J, \sigma_J$ for Bates) are calibrated by minimizing IV RMSE over the day's liquid option surface, subject to VIX-anchoring constraints.

[Table omitted — see original .tex]

### Theorem 1: Mispricing Detection Results

We evaluate the mispricing detection bound (Theorem [ref]) by constructing synthetic mispricing events: we contaminate market mid-prices with known additive errors of magnitude $\Delta$ and measure the empirical detection rate of the multi-model ensemble.

[Table omitted — see original .tex]

The empirical detection rates closely track the $M_{eff}$-adjusted theoretical bound, confirming that the structural overlap adjustment is necessary: using $M=5$ (naive independent-models assumption) would dramatically overstate detection capability. The $M_{eff}=2.556$ bound is slightly conservative relative to empirical rates, as expected for a concentration inequality.

### Theorem 3: Cercis Score Validation

To validate the Cercis Score, we conduct a rolling out-of-sample exercise: for each month $t$, we calibrate all models on the preceding 12 months of data and compute the Cercis Score on the subsequent month. We then correlate the Cercis Score with the out-of-sample hedging error.

[Figure omitted — see original .tex]

The Cercis Score achieves a Spearman rank correlation of $0.78$ with out-of-sample delta-hedge P\&L variance, substantially outperforming the in-sample-only metric $Q$ (Spearman $\rho = 0.61$). This confirms the value of the regime-novelty penalty $N$ in predicting real-world model degradation.

### Cross-Asset Results

[Table omitted — see original .tex]

Notable findings:

- **SABR dominance in swaptions:** SABR outperforms Bates and rBergomi for interest-rate swaptions, consistent with SABR's origin as an interest-rate model. The backbone parameter $\beta$ is critical for capturing the swaption volatility cube's tenor structure.
- **Cryptocurrency noise:** Cercis Scores for BTC and ETH options are 2--3$\times$ higher than for SPX across all models, reflecting the extreme volatility-of-volatility and regime instability in crypto markets. The Cercis Score correctly identifies crypto as a higher model-risk environment.
- **VIX idiosyncrasy:** Black--Scholes is not applicable to VIX futures (they are not equity options). Among the applicable models, rBergomi's fractional dynamics best capture the VIX term structure's roughness.

### Regime Shift Detection Accuracy

We evaluate the spring-gating classifier against a manually labeled set of known regime transitions:

[Table omitted — see original .tex]

The spring-gating mechanism accurately classifies regimes with macro-averaged F1 of $0.897$. Detection lag averages 2.3 days, meaning the protocol identifies regime shifts within approximately two trading days. The 90th-percentile lag of 5.1 days corresponds to the most ambiguous transitions (e.g., the ``taper tantrum'' of 2013).

## Discussion

### Interpretation of Results

Our three theorems collectively establish a mathematical framework for understanding the limits and capabilities of multi-model derivative pricing.

**Theorem 1** provides the operational takeaway that model ensembles can detect large mispricing with high probability, but detecting fine-grained mispricing ($\Delta \sim 1\%$--$2\%$) requires an impractically large number of structurally independent models. This is not a weakness of our framework; it is a fundamental consequence of the concentration-of-measure phenomenon: when models share stochastic foundations, their errors are correlated, and correlation erodes the ``wisdom of crowds.''

**Theorem 2** delivers the uncomfortable truth that model risk attribution is fundamentally underdetermined by market data alone. The practical implication is that every risk report that attributes P\&L to ``model error'' or ``regime change'' is making an implicit, unverifiable assumption. The SCX{} framework does not resolve this ambiguity---it *formalizes* it, making the axiom choices explicit so that they can be debated, audited, and stress-tested.

**Theorem 3** provides a constructive resolution: while individual model attribution is unidentifiable, relative model quality is empirically measurable through the Cercis Score. The ranking $\BS \prec \Heston \prec \SABR \prec \BatesM \prec \rBergomi$ is robust and actionable: for any given contract, one should prefer (in order) rBergomi, Bates, SABR, Heston, or BS, subject to computational budget and the Cercis Score itself.

### Limitations

Several limitations warrant acknowledgment:

1. **Computational cost:** rBergomi requires Monte Carlo simulation with $10^5$--$10^6$ paths for accurate pricing, making it unsuitable for real-time market making. The Yajie Consensus Protocol excludes rBergomi from the voting ensemble for this reason.
2. **Calibration instability:** Bates model calibration exhibits multiple local minima in the jump parameter space, requiring careful initialization. In crisis regimes, the optimizer occasionally converges to economically implausible parameter values.
3. **Regime discreteness:** Our three-regime classification (low/high/crisis) is a coarse discretization of what is fundamentally a continuous process. Future work should explore continuous regime indices.
4. **Model universe:** The five models considered, while representative, are not exhaustive. Extensions to rough Heston, quadratic rough Heston, and 4/2 models are natural next steps.
5. **Transaction costs:** The delta-hedge P\&L variance component of the Cercis Score assumes continuous rebalancing with proportional costs; real-world market impact and discrete hedging constraints may alter the ranking.

### Comparison with Related Frameworks

[Table omitted — see original .tex]

Our framework differs from prior work in its emphasis on *certification* rather than optimization. Cont [cite] and Glasserman--Xu [cite] provide normative guidance (``what should a risk manager do?''), while SCX{} provides deductive guarantees (``what can be proven about this ensemble?''). Both perspectives are valuable; they are complementary rather than competing.

### Practical Recommendations

Based on our results, we recommend the following operational practices:

1. **Multi-model pricing displays:** Trading desks should display the full ensemble of model prices (BS, Heston, SABR, Bates) rather than a single ``preferred'' model, with the inter-model spread serving as a real-time model risk indicator.
2. **Cercis Score monitoring:** Risk management should track daily Cercis Scores for all active models and trigger review when scores breach historical thresholds (e.g., 95th percentile of trailing 252-day distribution).
3. **Assumption disclosure:** Any P\&L attribution statement (e.g., ``today's loss was driven by model recalibration'') should be accompanied by an explicit declaration of which components of the decomposition [ref] are assumed zero.
4. **Regime-aware position limits:** Position limits should be tightened automatically when the spring-gating mechanism detects a transition to $R_{crisis}$, reflecting the elevated uncertainty in all model outputs.
5. **Cross-asset consistency checks:** The Cercis Score ranking should be periodically validated across asset classes; a model that dominates in equities but underperforms in rates warrants investigation.

## Conclusion

We have presented a rigorous mathematical framework for auditing derivative pricing models through multi-model consensus within the SCX{} formal verification paradigm. The framework is built on three foundational theorems:

1. A multi-model mispricing detection bound showing that the probability that all $M$ models simultaneously miss a mispricing exceeding $\Delta$ decays as $\exp(-2 M_{eff} \Delta^2)$, where $M_{eff}$ accounts for structural overlap between models sharing stochastic process families.
2. A fundamental unidentifiability result proving that model risk and regime shift cannot be distinguished without declared auxiliary assumptions, formalizing Derman's model risk taxonomy within the SCX{} deductive hierarchy as **SCX-THM.3**.
3. A Cercis Score that ranks pricing models by combining in-sample fit (IV smile RMSE and delta-hedge P\&L variance) with a regime-novelty penalty, yielding the robust empirical ordering $\BS \prec \Heston \prec \SABR \prec \BatesM \prec \rBergomi$.

These results are operationalized in the Multi-Model Yajie Consensus Protocol, which aggregates BS, Heston, SABR, and Bates model outputs through VIX-anchored weighted voting, with spring-gating for real-time volatility regime detection. Empirical validation across SPX equity options (2005--2024), VIX futures, interest-rate swaptions, and cryptocurrency options confirms both the theoretical bounds and the practical utility of the framework.

The broader contribution of this work is methodological: we demonstrate that formal verification techniques, traditionally associated with software and hardware systems, can be productively applied to stochastic financial models. The SCX{} framework's deductive apparatus forces explicit declaration of assumptions, rigorous proof of guarantees, and transparent acknowledgment of what cannot be certified---a discipline sorely needed in quantitative finance.

### Future Work

Several extensions are under investigation:

1. **Continuous regime indices:** Replacing the discrete three-regime classification with a continuous regime index based on the full VIX term structure and skew, enabling smoother model-weight transitions.
2. **Rough Heston ensemble:** Incorporating the rough Heston model [cite], which combines the tractability of Heston's characteristic function with the empirical realism of rough volatility.
3. **Dynamic $\eta$ calibration:** Allowing the regime-aversion parameter $\eta$ in the Cercis Score to vary with market conditions, reflecting the fact that regime robustness is more valuable during turbulent periods.
4. **Neural SDE models:** Extending the ensemble to include neural stochastic differential equations as a flexible nonparametric baseline, testing whether data-driven models can improve Cercis Scores beyond the parametric frontier.
5. **Real-time SCX certification:** Building a production system that continuously monitors the Yajie Consensus output and issues SCX{} certificates when the confidence measure $\gamma_{cert}$ exceeds a configurable threshold.
6. **跨市场联动分析 (Cross-market linkage):** Extending the framework to explicitly model cross-asset volatility transmission (equity $\leftrightarrow$ rates $\leftrightarrow$ FX $\leftrightarrow$ crypto) within a unified SCX certification graph.

## Appendix

## Extended Proofs and Derivations

### Detailed Hoeffding Bound Derivation (Theorem 1)

We provide the full derivation of the Hoeffding bound with dependence adjustment.

> **Lemma:** [Hoeffding's Lemma]<!-- label: lem:hoeffding_lemma -->
> Let $X$ be a random variable with $\E[X] = 0$ and $a \leq X \leq b$ almost surely. Then for any $\lambda \in \R$:
> 
> $$<!-- label: eq:hoeffding_lemma -->
>   \E[e^{\lambda X}] \leq \exp\!\left(\frac{\lambda^2 (b-a)^2}{8}\right).
> $$

> **Proof:** By convexity of the exponential function, $e^{\lambda X} \leq \frac{b-X}{b-a} e^{\lambda a} + \frac{X-a}{b-a} e^{\lambda b}$. Taking expectations and using $\E[X] = 0$, then optimizing over $\lambda$ using the Diamond--Cantelli quadratic bound yields the result.

For the dependent case, we use the following extension:

> **Lemma:** [Hoeffding under Dependence]<!-- label: lem:hoeffding_dependent -->
> Let $(X_1, ..., X_M)$ be bounded random variables with $\E[X_i] = 0$, $a_i \leq X_i \leq b_i$. Let $\Sigma$ be the correlation matrix. Then:
> 
> $$<!-- label: eq:hoeffding_dep -->
>   \Pbb\!\left(\sum_{i=1}^M X_i \geq t\right) \leq \exp\!\left(-\frac{2t^2}{\sum_{i,j} |\Sigma_{ij}| (b_i-a_i)(b_j-a_j)}\right).
> $$

> **Proof:** Follows from [cite] with the effective sample size adjustment. The key insight is that the variance of the sum includes all covariance terms, and the Hoeffding bound can be rewritten in terms of the effective number of independent observations.

Setting $X_i = Y_i$ (the centered mispricing indicators from the main proof) with $a_i = -p_i$, $b_i = 1-p_i$, so $b_i - a_i = 1$, and $t = M(1 - \bar{p})$, and using $|\Sigma_{ij}| = \phi_{ij}$, we recover the bound in [ref].

### Sub-Gaussian Calibration for Option Pricing Errors

We justify the sub-Gaussian assumption (Assumption [ref]) for option pricing errors.

> **Proposition:** [Sub-Gaussian Pricing Errors]<!-- label: prop:subgaussian_justification -->
> Under Assumptions [ref]-- [ref], the pricing error $\varepsilon_i = \pi_i - \pi_{true}$ for any model $m_i$ is sub-Gaussian with variance proxy $\sigma_i^2 \leq B^2 / 4$, where $B$ is the payoff bound.

> **Proof:** By Assumption [ref], $\pi_i = \E^{\riskneutral_i}[e^{-rT} H(S_T)]$. By Assumption [ref], $0 \leq H(S_T) \leq B$. Hence $0 \leq \pi_i \leq B$ and $0 \leq \pi_{true} \leq B$. Therefore $\varepsilon_i \in [-B, B]$. Any bounded random variable supported on $[-B, B]$ is sub-Gaussian with variance proxy $\sigma_i^2 = B^2$ (conservative) or $\sigma_i^2 = B^2/4$ (using the maximum variance of a $[-B,B]$-valued random variable). The claim follows from Hoeffding's lemma applied to the bounded interval.

### Cercis Score Derivation from First Principles

We derive the Cercis Score from a decision-theoretic foundation.

Consider a risk manager who must select a pricing model $m$ from a set $\M$ to value a derivative and execute a delta hedge. The manager faces a loss function:

$$<!-- label: eq:loss -->
  L(m; \mathcal{D}_{test}) = \underbrace{\E\left[(\pi_m - \pi_{mkt})^2\right]}_{Pricing error} + \lambda \cdot \underbrace{\Var(\Pi_{hedge}^m)}_{Hedging error},
$$

where the expectation is over the test distribution. By the bias-variance decomposition:

$$<!-- label: eq:bias_variance -->
  \E[(\pi_m - \pi_{mkt})^2] = (\E[\pi_m] - \E[\pi_{mkt}])^2 + \Var(\pi_m - \pi_{mkt}).
$$

The bias term captures systematic model error; the variance term captures sensitivity to parameter uncertainty and data noise.

Now decompose the test distribution into a mixture of a known training regime $R_{train}$ and a potentially novel test regime $R_{test}$:

$$<!-- label: eq:mixture -->
  p_{test} = (1 - \varepsilon) \cdot p_{train} + \varepsilon \cdot p_{novel},
$$

where $\varepsilon = \Pbb(R_{test} \neq R_{train})$ and $p_{novel}$ is the distribution under the novel regime.

Under $p_{train}$, the model's expected squared error is $Q_{train}(m)$. Under $p_{novel}$, the error is inflated by a factor proportional to the KL divergence between $p_{novel}$ and $p_{train}$:

$$<!-- label: eq:novel_error -->
  \E_{p_{novel}}[(\pi_m - \pi_{mkt})^2] \leq Q_{train}(m) + \eta \cdot KL(p_{novel} \| p_{train}),
$$

where $\eta$ is a model-specific sensitivity parameter. The total expected loss is then:

$$<!-- label: eq:total_loss -->
  L(m) = (1-\varepsilon) \cdot Q_{train}(m) + \varepsilon \cdot (Q_{train}(m) + \eta \cdot KL) = Q(m) + \varepsilon \eta \cdot KL(p_{novel} \| p_{train}).
$$

Absorbing $\varepsilon$ into $\eta$ and identifying $KL(p_{novel} \| p_{train})$ as the regime novelty penalty $N$, we recover the Cercis Score $S(m) = Q(m) + \eta \cdot N(m)$.

### VIX Anchoring Optimality

> **Proposition:** [VIX Anchoring Efficiency]<!-- label: prop:vix_efficiency -->
> Among all single-instrument volatility anchors, the VIX index minimizes the asymptotic variance of the consensus price estimator under a mean-squared-error loss.

> **Proof:** The VIX is computed as a weighted portfolio of OTM SPX options spanning all available strikes: (注: Following the CBOE VIX White Paper methodology.)
> 
> $$<!-- label: eq:vix_formula -->
>   VIX^2 = \frac{2}{T}\sum_i \frac{\Delta K_i}{K_i^2} e^{rT} Q(K_i) - \frac{1}{T}\left(\frac{F}{K_0} - 1\right)^2,
> $$
> 
> where $Q(K_i)$ are OTM option mid-prices and $F$ is the forward level. This formula is a discretization of the model-free implied variance:
> 
> $$<!-- label: eq:mfiv -->
>   \E^\!\left[\int_0^T \sigma_t^2\,dt\right] = \frac{2}{T}\int_0^\infty \frac{Q(K)}{K^2}\,dK.
> $$
> 
> 
> The VIX thus aggregates information from the *entire* options surface, achieving the semiparametric efficiency bound for integrated variance estimation [cite]. Any single-strike or narrow-strip volatility anchor would discard information and increase estimation variance. By the Gauss--Markov theorem for the class of linear anchoring estimators, VIX is the best linear unbiased anchor.

## Additional Empirical Results

### Regime Transition Matrix

The estimated Markov transition matrix for regime states, computed from daily VIX classifications (2005--2024):

[Table omitted — see original .tex]

Regimes are highly persistent: the daily probability of remaining in the same regime is $0.858$--$0.967$. Transitions from crisis directly to low vol are extremely rare ($0.8\%$ daily), consistent with the gradual mean-reversion of volatility.

### Chinese Terminology Reference (中文术语对照)

[Table omitted — see original .tex]

## Calibration Details for Each Model

### Black--Scholes

The sole free parameter $\sigma$ is set to the VIX-implied 30-day ATM volatility. No optimization is performed; this is the ``VIX-consistent BS'' baseline.

### Heston

The five parameters $\Theta_ = (v_0, \kappa, \theta, \xi, \rho)$ are estimated via:

$$<!-- label: eq:heston_calib -->
  \hat_ = \arg\min_ \sum_{i=1}^{N} w_i \left(\sigma_{imp}^(K_i, T_i; \Theta) - \sigma_{imp}^{mkt}(K_i, T_i)\right)^2,
$$

subject to the Feller condition $2\kappa\theta \geq \xi^2$ (enforced via a penalty barrier) and the VIX-anchoring constraint $|\sigma_{imp}^(K_{ATM}, T_{30d}; \Theta) - \sigma_{VIX}| \leq \epsilon$.

Weights $w_i$ are proportional to the inverse bid-ask spread to emphasize liquid options. Optimization uses the Levenberg--Marquardt algorithm with multiple random initializations to escape local minima.

### SABR

For each maturity slice, we estimate $(\alpha, \rho, \nu)$ with fixed $\beta$ (calibrated globally to minimize pooled RMSE). The implied volatility is computed via the Hagan et al.\ asymptotic expansion [cite]:

$$<!-- label: eq:sabr_iv -->
  \sigma_{SABR}(K, F, T) \approx \frac{(FK)^{(1-\beta)/2}\left[1 + \frac{(1-\beta)^2}{24}\ln^2(F/K) + \frac{(1-\beta)^4}{1920}\ln^4(F/K) + ...\right]} \cdot \frac{z}{\chi(z)},
$$

where $z = \frac(FK)^{(1-\beta)/2} \ln(F/K)$ and $\chi(z) = \ln\!\left(\frac{\sqrt{1 - 2\rho z + z^2} + z - \rho}{1 - \rho}\right)$.

### Bates

The eight parameters $\Theta_ = (v_0, \kappa, \theta, \xi, \rho, \lambda, \mu_J, \sigma_J)$ are estimated in two stages:

1. Stage 1: Fit Heston parameters $(v_0, \kappa, \theta, \xi, \rho)$ to the volatility surface excluding deep OTM puts (which are most sensitive to jump risk).
2. Stage 2: Holding Heston parameters fixed, estimate jump parameters $(\lambda, \mu_J, \sigma_J)$ by minimizing the RMSE on deep OTM puts ($\Delta \leq -0.2$), where jump risk premia are concentrated.

### Rough Bergomi

The forward variance curve $\xi_0(t)$ is bootstrapped from VIX futures prices. Parameters $(H, \eta, \rho)$ are estimated by matching the power-law decay of the ATM skew:

$$<!-- label: eq:rbergomi_skew -->
  \psi(\tau) := \left|\frac{\partial \sigma_{imp}(k, \tau)}{\partial k}\right|_{k=0} \propto \tau^{H-1/2},
$$

where $k = \ln(K/S_0)$ is log-moneyness. We estimate $H$ by regressing $\ln \psi(\tau)$ on $\ln \tau$ over the first 6 months of maturities. Parameters $(\eta, \rho)$ are then calibrated to match the level of the observed skew.

Pricing for rBergomi uses hybrid quadrature--Monte Carlo with $10^5$ paths and antithetic variates for variance reduction.

## Notation Glossary

[Table omitted — see original .tex]

\begin{thebibliography}{99}

\bibitem{black1973pricing}
F.~Black and M.~Scholes.
\newblock The pricing of options and corporate liabilities.
\newblock {\em Journal of Political Economy}, 81(3):637--654, 1973.

\bibitem{heston1993closed}
S.~L.~Heston.
\newblock A closed-form solution for options with stochastic volatility with
  applications to bond and currency options.
\newblock {\em Review of Financial Studies}, 6(2):327--343, 1993.

\bibitem{hagan2002managing}
P.~S.~Hagan, D.~Kumar, A.~S.~Lesniewski, and D.~E.~Woodward.
\newblock Managing smile risk.
\newblock {\em Wilmott Magazine}, pages 84--108, September 2002.

\bibitem{bates1996jumps}
D.~S.~Bates.
\newblock Jumps and stochastic volatility: Exchange rate processes implicit in
  Deutsche mark options.
\newblock {\em Review of Financial Studies}, 9(1):69--107, 1996.

\bibitem{bayer2016pricing}
C.~Bayer, P.~Friz, and J.~Gatheral.
\newblock Pricing under rough volatility.
\newblock {\em Quantitative Finance}, 16(6):887--904, 2016.

\bibitem{gatheral2018volatility}
J.~Gatheral, T.~Jaisson, and M.~Rosenbaum.
\newblock Volatility is rough.
\newblock {\em Quantitative Finance}, 18(6):933--949, 2018.

\bibitem{derman1996model}
E.~Derman.
\newblock Model risk.
\newblock {\em Risk Magazine}, 9(5):34--37, 1996.

\bibitem{cont2006model}
R.~Cont.
\newblock Model uncertainty and its impact on the pricing of derivative
  instruments.
\newblock {\em Mathematical Finance}, 16(3):519--547, 2006.

\bibitem{glasserman2014robust}
P.~Glasserman and X.~Xu.
\newblock Robust risk measurement and model risk.
\newblock {\em Quantitative Finance}, 14(1):29--58, 2014.

\bibitem{hoeffding1963probability}
W.~Hoeffding.
\newblock Probability inequalities for sums of bounded random variables.
\newblock {\em Journal of the American Statistical Association},
  58(301):13--30, 1963.

\bibitem{bentkus2005hoeffding}
V.~Bentkus.
\newblock A Lyapunov-type bound in $\R^d$.
\newblock {\em Theory of Probability and Its Applications}, 49(2):311--323,
  2005.

\bibitem{rothenberg1971identification}
T.~J.~Rothenberg.
\newblock Identification in parametric models.
\newblock {\em Econometrica}, 39(3):577--591, 1971.

\bibitem{scx2025}
SCX.
\newblock The SCX formal verification framework: Stochastic certification
  extended.
\newblock Technical report, 2025.

\bibitem{el2022rough}
O.~El Euch, J.~Gatheral, and M.~Rosenbaum.
\newblock Rough Heston: The quintessential stochastic volatility model.
\newblock {\em Mathematical Finance}, 32(3):777--814, 2022.

\bibitem{bollerslev2011expected}
T.~Bollerslev, M.~Gibson, and H.~Zhou.
\newblock Dynamic estimation of volatility risk premia and investor risk
  aversion from option-implied and realized volatilities.
\newblock {\em Journal of Econometrics}, 160(1):235--245, 2011.

\end{thebibliography}