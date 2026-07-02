# Definition:

**Author:** SCX

*Abstract:*

Proves a finite-expert lower bound for out-of-distribution detection via Spring gatekeeper scores. Minimum detectable OOD shift: delta_min = sigma/sqrt(M). False alarm and detection power both controlled by Hoeffding bounds exponential in M.

### OOD Detection Lower Bound
<!-- label: subsec:spring_ood -->

The CUSUM statistic above monitors temporal drift across a rollout.  Spring
also induces a one-sample OOD test: a sample is suspicious when its gatekeeper
score is atypical relative to scores stored in the in-distribution memory.  To
avoid collision with the CUSUM statistic $S_t$, write $G_t(x)$ for the
per-sample Spring gatekeeper score; this is the score denoted $S_t(x)$ in the
Spring gating notes.

Let $\mathfrak{M}_t$ be the Spring memory bank of accepted in-distribution
samples.  For $M$ expert modules, let $Z_{m,t}(x) \in [0,1]$ be expert $m$'s
normalized validity score for sample $x$ at time $t$, and define the aggregate
gatekeeper score

$$
  G_t(x) = \frac{1}{M}\sum_{m=1}^{M} Z_{m,t}(x).
  <!-- label: eq:spring_gate_score -->
$$

The memory bank estimates the in-distribution score center
$\mu_{\mathrm{in},t} = \E[G_t(X)\mid X \sim P_{\mathrm{in},t}]$ by
$\widehat_{\mathrm{in},t}$.

> **Definition:** [Spring OOD Hypothesis Test]
> <!-- label: def:spring_ood_test -->
> OOD detection is the binary hypothesis test
> 
> $$
>   H_0: X \sim P_{\mathrm{in},t},
>   \qquad
>   H_1: X \sim P_{\mathrm{out},t},
> $$
> 
> with OOD shift
> 
> $$
>   \delta_{\mathrm{OOD}}
>   =
>   \left|
>   \E[G_t(X)\mid H_1]
>   -
>   \mu_{\mathrm{in},t}
>   \right|.
> $$
> 
> For a tolerance $\epsilon > 0$, the ideal calibrated Spring detector is
> 
> $$
>   \varphi_{\epsilon,t}(x)
>   =
>   \ind{\left|G_t(x)-\mu_{\mathrm{in},t}\right|>\epsilon},
>   <!-- label: eq:spring_ood_test -->
> $$
> 
> where $\varphi_{\epsilon,t}(x)=1$ means ``declare OOD.''  In deployment,
> $\mu_{\mathrm{in},t}$ is replaced by $\widehat_{\mathrm{in},t}$ from
> $\mathfrak{M}_t$; the calibration error is handled in
> Corollary [ref].

> **Theorem:** [SCX OOD Detection Lower Bound]
> <!-- label: thm:spring_ood_lower -->
> Condition on the Spring memory state $\mathfrak{M}_t$.  Assume that
> $Z_{1,t}(X),...,Z_{M,t}(X)$ are independent and take values in $[0,1]$.
> Under $H_0$, suppose $\E[G_t(X)\mid H_0]=\mu_{\mathrm{in},t}$; under $H_1$,
> suppose
> $|\E[G_t(X)\mid H_1]-\mu_{\mathrm{in},t}|=\delta_{\mathrm{OOD}}$.
> Then, writing
> $p_i(\epsilon)=\Pbb(\varphi_{\epsilon,t}(X)=1\mid H_i)$, the test
> in [ref] satisfies
> 
> $$
>   p_0(\epsilon)
>     &\le 2\exp(-2M\epsilon^2), <!-- label: eq:ood_false_alarm -->

>   p_1(\epsilon)
>     &\ge
>     1-\exp\!\left(-2M(\delta_{\mathrm{OOD}}-\epsilon)^2\right)
>     <!-- label: eq:ood_power_exact -->
> $$
> 
> for every $0<\epsilon<\delta_{\mathrm{OOD}}$.  In particular, if the OOD
> shift has margin $\delta_{\mathrm{OOD}}\ge 2\epsilon$, then
> 
> $$
>   \Pbb(detect OOD\mid \delta_{\mathrm{OOD}}\ge 2\epsilon)
>   \ge 1-\exp(-2M\epsilon^2).
>   <!-- label: eq:ood_power_margin -->
> $$

> **Proof:** The bounds follow directly from Hoeffding's inequality applied to the
> $M$ independent gatekeeper scores.