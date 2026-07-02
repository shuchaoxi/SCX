## Theorem 1: Multi-Expert Consistency Noise Detection Guarantee (The Unlikely Lone Genius Theorem)
<!-- label: sec:thm1 -->

We establish a formal guarantee for the SCX noise detection procedure. When $M$
experts, each trained on a disjoint data subset, exhibit high consensus on a
sample's erroneousness, that sample can be identified as label noise with
confidence that converges exponentially fast to $1$ as $M$ grows.

### Notation and Setup
<!-- label: sec:thm1:setup -->

Let $(\mathcal{X},\mathcal{Y})$ be the input--label space with
$|\mathcal{Y}| = K_{\mathcal{Y}}$ (classification) or
$\mathcal{Y} \subseteq \mathbb{R}^d$ (regression). Data follows
$(X,Y) \sim \mathcal{D}$ with true labeling function
$f^* : \mathcal{X} \to \mathcal{Y}$ (unknown oracle). We have $M$ expert models
$\{f_m\}_{m=1}^M$, each $f_m : \mathcal{X} \to \mathcal{Y}$.

The state space $\mathcal{S}$ indexes a measurable partition
$\Pi = \{s_1,...,s_{|\mathcal{S}|}\}$ of $\mathcal{X}$, where each state
$s \in \mathcal{S}$ groups samples with similar characteristics.

> **Definition:** [Label noise model]
> <!-- label: def:noise-model -->
> For a sample $(x, y^*)$ with true label $y^* = f^*(x)$, the observed label $y$ is
> generated as
> 
> $$
> y = \begin{cases}
> y^* & with probability  1 - \eta, 
> \operatorname{Uniform}(\mathcal{Y} \setminus \{y^*\}) & with probability  \eta,
> \end{cases}
> <!-- label: eq:noise-model -->
> $$
> 
> where $\eta \in (0, \tfrac12)$ is the global noise rate and the noise event is
> independent of $x$ and of all training data.

Let $\ell : \mathcal{Y} \times \mathcal{Y} \to [0, B]$ be a bounded loss
function with $B < \infty$, and $\tau > 0$ an error threshold. Define the
expert error indicator and the consensus score as

$$
e_m(x, y) &= \mathbf{1}\{\ell(f_m(x), y) > \tau\}, &
C(x) &= \frac{1}{M}\sum_{m=1}^M e_m(x, y).
<!-- label: eq:consensus-score -->
$$

> **Definition:** [Detection rule]
> <!-- label: def:detection-rule -->
> A sample $(x,y)$ is flagged as noisy if and only if $C(x) > \theta$, where
> $\theta \in (0,1)$ is a detection threshold.

### Assumptions (A1)--(A6)
<!-- label: sec:thm1:assumptions -->

The following assumptions are used throughout Theorem~1 and its supporting
lemmas.

1. [**(A1)**] **(Disjoint training sets).**
2. [**(A2)**] **(Conditional independence on clean data).**
3. [**(A3)**] **(Bounded loss).**
4. [**(A4)**] **(Uniform independent noise).**
5. [**(A5)**] **(State homogeneity).**
6. [**(A6)**] **(Balanced error distribution).**

### Lemma 1: Mean Separation
<!-- label: sec:thm1:lemma1 -->

> **Lemma:** [Mean Separation]
> <!-- label: lem:mean-separation -->
> Under assumptions (A1)--(A5), for any $x \in s$,
> 
> $$
> \mathbb{E}[C(X) \mid clean, X = x] &\leq \mu_s,
> <!-- label: eq:lem1-clean --> 

> \mathbb{E}[C(X) \mid noise, X = x]
> &= 1 - \frac{1}{K_{\mathcal{Y}} - 1} \,
>    \mathbb{E}[C(X) \mid clean, X = x]
>    \;\geq\; 1 - \frac{\mu_s}{K_{\mathcal{Y}} - 1}.
> <!-- label: eq:lem1-noise -->
> $$
> 
> 
> Consequently, when $\mu_s < \dfrac{K_{\mathcal{Y}} - 1}{K_{\mathcal{Y}}}$
> there exists $\theta$ such that
> \[
> \mathbb{E}[C \mid clean] < \theta < \mathbb{E}[C \mid noise],
> \]
> and the separation gap for state $s$ is
> 
> $$
> \Delta_s(\theta)
> = \min\!\Bigl(\theta - \mu_s,\;
>   1 - \frac{\mu_s}{K_{\mathcal{Y}}-1} - \theta\Bigr).
> <!-- label: eq:separation-gap -->
> $$
> 
> 
> With the optimal threshold
> \[
> \theta_s^* = \frac12\!\left(1 + \mu_s\cdot\frac{K_{\mathcal{Y}}-2}{K_{\mathcal{Y}}-1}\right)\!,
> \]
> the maximised gap (in the ideal case $C_{bal}=1$) is
> \[
> \Delta_s^* = \frac12\!\left(1 - \mu_s\cdot\frac{K_{\mathcal{Y}}}{K_{\mathcal{Y}}-1}\right).
> \]
> When $C_{bal} > 1$, the optimal threshold shifts towards $\mu_s$ to
> compensate for the non-uniform error distribution.

> **Proof:** [Proof of Lemma~1]
> The clean-sample bound follows directly from (A5). For a noise sample,
> 
> $$
> \mathbb{E}[C \mid noise, X = x]
> &= \frac{1}{M}\sum_{m=1}^M \mathbb{P}\bigl(\ell(f_m(x), y) > \tau
>    \;\big|\; noise, x\bigr) 

> &= \frac{1}{M}\sum_{m=1}^M \mathbb{P}\bigl(f_m(x) \neq y
>    \;\big|\; noise, x\bigr) \qquad(for  0-1 loss) 

> &= 1 - \frac{1}{M}\sum_{m=1}^M \mathbb{P}\bigl(f_m(x) = y
>    \;\big|\; noise, x\bigr).
> $$
> 
> By (A4), the noise label $y$ is uniform over $\mathcal{Y}\setminus\{y^*\}$ and
> independent of all experts:
> 
> $$
> \mathbb{P}(f_m(x) = y \mid noise, x)
> &= \sum_{c \neq y^*} \mathbb{P}(y = c \mid noise)\,
>    \mathbb{P}(f_m(x) = c \mid x) 

> &= \frac{1}{K_{\mathcal{Y}}-1} \sum_{c \neq y^*}
>    \mathbb{P}(f_m(x) = c \mid x) 

> &= \frac{1}{K_{\mathcal{Y}}-1}\,
>    \mathbb{P}(f_m(x) \neq y^* \mid x)
>  = \frac{1}{K_{\mathcal{Y}}-1}\,
>    \mathbb{E}[e_m \mid clean, x].
> $$
> 
> Averaging over $m$ gives
> 
> $$
> \mathbb{E}[C \mid noise, x]
> &= 1 - \frac{1}{K_{\mathcal{Y}}-1}\,
>    \frac{1}{M}\sum_{m=1}^M \mathbb{E}[e_m \mid clean, x] 

> &= 1 - \frac{1}{K_{\mathcal{Y}}-1}\,
>    \mathbb{E}[C \mid clean, x]
> \;\geq\; 1 - \frac{\mu_s}{K_{\mathcal{Y}}-1},
> $$
> 
> where the inequality uses (A5). The separation gap exists whenever
> $\mu_s < (K_{\mathcal{Y}}-1)/K_{\mathcal{Y}}$, because then
> $1 - \mu_s/(K_{\mathcal{Y}}-1) > \mu_s$.

### Lemma 2: False Positive Rate Bound
<!-- label: sec:thm1:lemma2 -->

> **Lemma:** [False Positive Rate Upper Bound]
> <!-- label: lem:fpr-bound -->
> For any state $s \in \mathcal{S}$ satisfying $\mu_s < \theta$, the probability
> that a clean sample is incorrectly flagged as noise obeys
> 
> $$
> \mathbb{P}\bigl(C > \theta \mid clean, X \in s\bigr)
> \;\leq\; \exp\!\bigl(-2M(\theta - \mu_s)^2\bigr).
> <!-- label: eq:fpr-bound -->
> $$

> **Proof:** Fix $x \in s$. By (A5), $\mathbb{E}[C \mid clean, X = x] \leq \mu_s$.
> By (A1)--(A2), $\{e_m\}$ are conditionally independent given $x$, and by
> (A3) each $e_m \in [0,1]$. Apply Hoeffding's inequality
>  [cite] to $C = \frac{1}{M}\sum_{m} e_m$:
> \[
> \mathbb{P}\bigl(C - \mathbb{E}[C] > \theta - \mu_s \mid clean, x\bigr)
> \;\leq\; \exp\!\bigl(-2M(\theta - \mu_s)^2\bigr),
> \]
> where $\theta - \mu_s > 0$ by hypothesis. The bound holds for every $x \in s$,
> so integrating over $x$ yields
> 
> $$
> \mathbb{P}(C > \theta \mid clean, X \in s)
> &= \mathbb{E}_{X \mid s}\bigl[ \mathbb{P}(C > \theta \mid clean, X) \bigr] 

> &\leq \sup_{x \in s} \mathbb{P}(C > \theta \mid clean, x)
> \;\leq\; \exp\!\bigl(-2M(\theta - \mu_s)^2\bigr). \qedhere
> $$

### Lemma 3: True Positive Rate Bound
<!-- label: sec:thm1:lemma3 -->

> **Lemma:** [True Positive Rate Lower Bound]
> <!-- label: lem:tpr-bound -->
> Under assumptions (A1)--(A6), for any state $s \in \mathcal{S}$ satisfying
> \[
> \theta < 1 - C_{bal}\cdot\frac{\mu_s}{K_{\mathcal{Y}}-1},
> \]
> the probability that a noisy sample is correctly detected obeys
> 
> $$
> \mathbb{P}\bigl(C > \theta \mid noise, X \in s\bigr)
> \;\geq\; 1 - \exp\!\Bigl(
>   -2M\Bigl(1 - C_{bal}\cdot\frac{\mu_s}{K_{\mathcal{Y}}-1}
>   - \theta\Bigr)^{\!2}\Bigr).
> <!-- label: eq:tpr-bound -->
> $$

> **Proof:** Fix $x \in s$ and condition on a specific noise label $c \neq y^*$. For
> $0$-$1$ loss, expert $m$ errs when $f_m(x) \neq c$, so
> $e_m = \mathbf{1}\{f_m(x) \neq c\}$. By (A1) the $\{f_m\}$ are independent
> functions of disjoint data; by (A2) the $\{e_m\}$ are conditionally independent
> given $(x,c)$. The conditional expectation is
> \[
> \mathbb{E}[e_m \mid x, c] = 1 - \mathbb{P}(f_m(x) = c \mid x)
> = 1 - \mu_{c,m}(x),
> \]
> hence
> \[
> \mathbb{E}[C \mid x, c]
> = \frac{1}{M}\sum_{m=1}^M \mathbb{E}[e_m \mid x, c]
> = 1 - \mu_c(x)
> \;\geq\; 1 - C_{bal}\cdot\frac{\mu_s}{K_{\mathcal{Y}}-1},
> \]
> where the inequality follows from (A6). Since $e_m \in [0,1]$ are conditionally
> independent, Hoeffding's inequality gives
> 
> $$
> \mathbb{P}(C \leq \theta \mid x, c)
> &= \mathbb{P}\!\left(\frac{1}{M}\sum_{m=1}^M e_m \leq \theta
>    \;\Big|\; x, c\right) 

> &\leq \exp\!\Bigl(-2M\bigl(1 - \mu_c(x) - \theta\bigr)^2\Bigr) 

> &\leq \exp\!\Bigl(-2M\bigl(1 - C_{bal}\cdot\frac{\mu_s}{K_{\mathcal{Y}}-1}
>    - \theta\bigr)^2\Bigr).
> $$
> 
> The Hoeffding gap condition $1 - \mu_c(x) > \theta$ holds because
> \[
> 1 - \mu_c(x) \geq 1 - C_{bal}\cdot\frac{\mu_s}{K_{\mathcal{Y}}-1}
> > \theta
> \]
> by the lemma's hypothesis and (A6). Averaging over the uniform noise label
> $c \in \mathcal{Y}\setminus\{y^*\}$,
> \[
> \mathbb{P}(C \leq \theta \mid noise, x)
> = \frac{1}{K_{\mathcal{Y}}-1}\sum_{c \neq y^*}
>   \mathbb{P}(C \leq \theta \mid x, c)
> \;\leq\; \exp\!\Bigl(-2M\bigl(1 - C_{bal}\cdot\frac{\mu_s}{K_{\mathcal{Y}}-1}
>   - \theta\bigr)^2\Bigr).
> \]
> Therefore $\mathbb{P}(C > \theta \mid noise, x)
> \geq 1 - \exp(-2M(1 - C_{bal}\cdot\mu_s/(K_{\mathcal{Y}}-1)
> - \theta)^2)$. Taking expectations over $X \in s$ completes the proof.

> **Remark:** When $C_{bal} = 1$ (perfectly uniform error distribution), Lemma~3
> recovers the optimal bound. The constant $C_{bal}$ can be estimated from
> data and used to calibrate the detection threshold $\theta$.

### Proof of Theorem 1: F1 Lower Bound
<!-- label: sec:thm1:proof -->

> **Theorem:** [SCX Noise Detection Guarantee]
> <!-- label: thm:noise-detection -->
> Let assumptions (A1)--(A6) hold. Let $\rho_s = \mathbb{P}(X \in s)$ be the
> state probability. For any threshold $\theta$ satisfying, for a given state $s$,
> \[
> \mu_s < \theta < 1 - C_{bal}\cdot\frac{\mu_s}{K_{\mathcal{Y}}-1},
> \]
> define the state-level separation gap
> 
> $$
> \Delta_s \;=\;
> \min\!\Bigl(\theta - \mu_s,\;
>   1 - C_{bal}\cdot\frac{\mu_s}{K_{\mathcal{Y}}-1} - \theta\Bigr)
> > 0.
> <!-- label: eq:separation-gap-cbal -->
> $$
> 
> When $C_{bal} = 1$, $\Delta_s$ reduces to the definition in
> Lemma [ref]; when $C_{bal} > 1$ the noise-side gap
> narrows because errors may not be perfectly uniform.
> 
> Then the SCX noise detector achieves the F1 lower bound
> 
> $$
> \boxed{\;
> \operatorname{F1} \;\geq\; 1 - \frac{1}
> \sum_{s \in \mathcal{S}} \rho_s \cdot
> \exp\!\bigl(-2M\Delta_s^2\bigr)
> \;}
> <!-- label: eq:f1-bound-hoeffding -->
> $$
> 
> or equivalently
> 
> $$
> \operatorname{F1} \;\geq\; 1 - \sum_{s \in \mathcal{S}} \rho_s \Bigl[
> \exp\!\bigl(-2M\Delta_s^2\bigr)
> + \frac{1-\eta}\exp\!\bigl(-2M\Delta_s^2\bigr)
> \Bigr].
> <!-- label: eq:f1-bound-explicit -->
> $$

> **Remark:** [Effective number of experts under correlation]
> <!-- label: rem:Meff -->
> The bound above uses the nominal number of experts $M$, which assumes
> perfect conditional independence (A2'). When experts share the same
> architecture or training paradigm, their errors may exhibit positive
> pairwise correlation $\bar$. In this case the effective number
> of independent experts is reduced to the
> **The Expert Dilution Formula (Expert Dilution Formula)**:
> $M_{eff} = M / (1 + (M-1)\bar)$
> (see Liang \& Zeger, 1986, for the generalized estimating equations
> variance-inflation factor). The bound then reads
> $\operatorname{F1} \geq 1 - \frac{1}\sum_s \rho_s
> \exp(-2M_{eff}\Delta_s^2)$, which remains exponentially
> convergent in $M$ but at a rate slowed by the factor $(1+(M-1)\bar)^{-1}$.
> Consistent estimation of $\bar$ via jackknife or bootstrap is
> standard; see \S [ref] for details.

> **Proof:** Let $R(x) = \mathbf{1}\{C(x) > \theta\}$ be the detection rule. Define
> 
> $$
> \operatorname{TPR}_s &=
> \mathbb{P}(R = 1 \mid noise, X \in s), 

> \operatorname{FPR}_s &=
> \mathbb{P}(R = 1 \mid clean, X \in s).
> $$
> 
> By Lemma [ref] and Lemma [ref],
> 
> $$
> \operatorname{TPR}_s &\geq 1 -
> \exp\!\Bigl(-2M\bigl(1 - C_{bal}\cdot\frac{\mu_s}{K_{\mathcal{Y}}-1}
> - \theta\bigr)^2\Bigr), 

> \operatorname{FPR}_s &\leq
> \exp\!\bigl(-2M(\theta - \mu_s)^2\bigr).
> $$
> 
> 
> From (A4), the noise event is independent of $X$, so
> $\mathbb{P}(noise \mid X \in s) = \eta$ for all $s$. Aggregating across
> states,
> \[
> \operatorname{TPR} = \sum_s \rho_s \operatorname{TPR}_s,\qquad
> \operatorname{FPR} = \sum_s \rho_s \operatorname{FPR}_s.
> \]
> 
> The F1 score is
> \[
> \operatorname{F1}
> = \frac{2\eta\operatorname{TPR}}{2\eta\operatorname{TPR}
>    + (1-\eta)\operatorname{FPR} + \eta(1-\operatorname{TPR})}
> = \frac{2\eta\operatorname{TPR}}{\eta(1+\operatorname{TPR})
>    + (1-\eta)\operatorname{FPR}}.
> \]
> 
> Set
> 
> $$
> \delta_1 &= \sum_{s} \rho_s \,
> \exp\!\Bigl(-2M\bigl(1 - C_{bal}\cdot\frac{\mu_s}{K_{\mathcal{Y}}-1}
> - \theta\bigr)^2\Bigr), 

> \delta_2 &= \sum_{s} \rho_s \,
> \exp\!\bigl(-2M(\theta - \mu_s)^2\bigr).
> $$
> 
> Then $\operatorname{TPR} \geq 1 - \delta_1$ and
> $\operatorname{FPR} \leq \delta_2$. Substituting,
> 
> $$
> \operatorname{F1}
> &\geq \frac{2\eta(1-\delta_1)}{\eta(2-\delta_1) + (1-\eta)\delta_2} 

> &= 1 - \frac{\eta\delta_1 + (1-\eta)\delta_2}
>          {\eta(2-\delta_1) + (1-\eta)\delta_2} 

> &\geq 1 - \frac{\eta\delta_1 + (1-\eta)\delta_2}
> \qquad(since denominator \geq \eta) 

> &= 1 - \delta_1 - \frac{1-\eta}\,\delta_2 .
> $$
> 
> 
> Now observe that $\Delta_s$ as defined in
>  [ref] satisfies
> \[
> \exp\!\bigl(-2M(\theta - \mu_s)^2\bigr) \leq \exp\!\bigl(-2M\Delta_s^2\bigr),
> \quad
> \exp\!\Bigl(-2M\bigl(1 - C_{bal}\cdot\frac{\mu_s}{K_{\mathcal{Y}}-1}
> - \theta\bigr)^2\Bigr) \leq \exp\!\bigl(-2M\Delta_s^2\bigr).
> \]
> Therefore
> 
> $$
> \operatorname{F1}
> &\geq 1 - \sum_s \rho_s\Bigl[
>    \exp\!\bigl(-2M\Delta_s^2\bigr)
>    + \frac{1-\eta}\exp\!\bigl(-2M\Delta_s^2\bigr)
> \Bigr] 

> &= 1 - \frac{1}\sum_s \rho_s\exp\!\bigl(-2M\Delta_s^2\bigr).
> \qedhere
> $$

> **Corollary:** [Asymptotic optimality]
> <!-- label: cor:asymptotic -->
> As $M \to \infty$, for all states satisfying
> $\mu_s < (K_{\mathcal{Y}}-1)/K_{\mathcal{Y}}$,
> \[
> \operatorname{F1} = 1 - \mathcal{O}_P\!\left(
> \frac{1}\, e^{-2M\Delta_^2}\right),
> \qquad
> \Delta_ = \min_{s \in \mathcal{S}} \Delta_s.
> \]

> **Example:** [Numerical illustration]
> <!-- label: ex:thm1-numerical -->
> Take $K_{\mathcal{Y}} = 10$ classes, $\eta = 0.1$ noise rate, $M = 20$ experts,
> and per-state clean error bound $\mu_s = 0.2$. With $C_{bal} = 1$, the
> optimal separation gap is
> \[
> \Delta_s^* = \frac12\!\left(1 - 0.2 \cdot \frac{10}{9}\right)
> \approx 0.389,
> \]
> and the F1 lower bound from Theorem [ref] is
> \[
> \operatorname{F1} \;\geq\; 1 - 10 \cdot
> \exp\!\bigl(-2 \cdot 20 \cdot 0.389^2\bigr)
> = 1 - 10 \cdot e^{-6.05}
> > 0.976.
> \]
> In practice, if the clean expert error rate is higher (e.g.\
> $\mu_s \approx 0.45$ as in CIFAR-10 with lightly trained experts), the gap
> shrinks to $\Delta_s \approx 0.25$, giving the weaker bound
> $\operatorname{F1} \geq 0.18$, which remains valid as a guarantee but is not
> tight. This sensitivity to $\mu_s$ underscores the importance of estimating
> $\mu_s$ accurately from validation data.

### Chernoff Tightening
<!-- label: sec:thm1:chernoff -->

Lemmas [ref] and  [ref] can be sharpened using the
Chernoff bound instead of Hoeffding. For clean data, let
$\{e_m\}$ be independent Bernoulli variables with mean
$\mu = \mathbb{E}[C \mid clean, x] \leq \mu_s$. For
$\theta > \mu$,

$$
\mathbb{P}(C > \theta \mid clean, x)
&= \mathbb{P}\!\left(\frac{1}{M}\sum_{m} e_m > \theta\right) 

&\leq \inf_{\lambda > 0}\, e^{-\lambda M\theta}\,
   \mathbb{E}\!\left[e^{\lambda\sum_m e_m}\right] 

&= \inf_{\lambda > 0}\, e^{-\lambda M\theta}\,
   \prod_{m=1}^M (1 - \mu_m + \mu_m e^\lambda) 

&\leq \exp\!\bigl(-M \cdot \operatorname{KL}(\theta \,\|\, \mu_s)\bigr),
$$

where $\operatorname{KL}(p \,\|\, q) = p\log\frac{p}{q}
+ (1-p)\log\frac{1-p}{1-q}$.

For the noise lower tail, conditioning on label $c$ and applying the same
bound yields
\[
\mathbb{P}(C \leq \theta \mid noise, x, c)
\;\leq\; \exp\!\Bigl(
  -M \cdot \operatorname{KL}\!\Bigl(\theta \;\Big\|\;
   1 - C_{bal}\cdot\frac{\mu_s}{K_{\mathcal{Y}}-1}\Bigr)
\Bigr).
\]

> **Remark:** [KL direction]
> <!-- label: remark:kl-direction -->
> The standard Chernoff bound for the lower tail is
> $\mathbb{P}(\bar{X} \leq \theta) \leq \exp(-n \cdot \operatorname{KL}(\theta \| p))$
> when $\theta < p$. Here the true mean is
> $p = 1 - C_{bal}\cdot\mu_s/(K_{\mathcal{Y}}-1)$ and the threshold
> $\theta$ satisfies $\theta < p$ by hypothesis, so the correct KL argument is
> $\theta$ (first) and $p$ (second).

Combining the two tails gives the Chernoff-form F1 bound

$$
\operatorname{F1} \;\geq\; 1
- \frac{1}\sum_{s \in \mathcal{S}} \rho_s
\Bigl[ \exp\!\bigl(-M \cdot \operatorname{KL}(\theta \,\|\, \mu_s)\bigr) 

+ \frac{1-\eta} \cdot
\exp\!\Bigl(-M \cdot \operatorname{KL}\!\Bigl(\theta \;\Big\|\;
  1 - C_{bal}\cdot\frac{\mu_s}{K_{\mathcal{Y}}-1}\Bigr)\Bigr)
\Bigr].
<!-- label: eq:f1-bound-chernoff -->
$$

The Chernoff bound is tighter than the Hoeffding bound by a factor that grows
with the separation gap. Specifically,
\[
\exp(-2M\Delta^2) \geq \exp(-M \cdot \operatorname{KL}(\mu + \Delta \,\|\, \mu)),
\]
with equality only as $\Delta \to 0$. In the practical regime
$\Delta \approx 0.1$--$0.4$, the Chernoff bound is $2$--$5$ times tighter.

### Corollaries
<!-- label: sec:thm1:corollaries -->

#### Corollary 1: Symmetric Experts
If all experts share the same clean-data error rate $\varepsilon$ (symmetric
experts), then $\mu_s = \varepsilon$ for all states,
\[
\Delta = \frac12\!\left(1 - \varepsilon\cdot\frac{K_{\mathcal{Y}}}{K_{\mathcal{Y}}-1}\right),
\]
and the F1 bound simplifies to

$$
\operatorname{F1} \;\geq\; 1 - \frac{1}\,
\exp\!\left(-\frac{M}{2}\Bigl(1 - \frac{\varepsilon K_{\mathcal{Y}}}{K_{\mathcal{Y}}-1}\Bigr)^2\right).
<!-- label: eq:cor-symmetric -->
$$

For binary classification ($K_{\mathcal{Y}}=2$) this further reduces to
\[
\operatorname{F1} \;\geq\; 1 - \frac{1}\,
\exp\!\bigl(-2M(\tfrac12 - \varepsilon)^2\bigr).
\]

#### Corollary 2: Optimal Threshold Selection
Given noise rate $\eta$, number of classes $K_{\mathcal{Y}}$, number of experts
$M$, and maximum clean error rate $\mu_ = \max_s \mu_s$, the optimal
threshold is

$$
\theta^* = \arg\max_ \min_s \Delta_s(\theta)
= \frac12\!\left(1 + \mu_\cdot\frac{K_{\mathcal{Y}}-2}{K_{\mathcal{Y}}-1}\right).
<!-- label: eq:optimal-threshold -->
$$

The resulting minimum separation gap is
\[
\Delta_^* = \frac12\!\left(1 - \mu_\cdot\frac{K_{\mathcal{Y}}}{K_{\mathcal{Y}}-1}\right),
\]
and the minimum number of experts required to achieve
$\operatorname{F1} \geq 1 - \varepsilon_0$ is

$$
M \;\geq\; \frac{1}{2\Delta_^{*2}}\,
\log\!\left(\frac{1}{\eta\varepsilon_0}\right).
<!-- label: eq:min-experts -->
$$

When controlling error across multiple states simultaneously, replace the
numerator $1$ in the logarithm with $|\mathcal{S}|$.

#### Corollary 3: Uniform Detectability
If there exists $\delta > 0$ such that
$\mu_s \leq (K_{\mathcal{Y}}-1)/K_{\mathcal{Y}} - \delta$ for all $s$, then
with the fixed threshold $\theta = \tfrac12$,
\[
\Delta_s \geq \frac{2},\qquad
\operatorname{F1} \;\geq\; 1 - \frac{1}\,
\exp\!\left(-\frac{M\delta^2}{2}\right).
\]
Thus whenever every state's clean expert error rate is uniformly bounded
below $(K_{\mathcal{Y}}-1)/K_{\mathcal{Y}}$, a fixed threshold yields
exponential F1 guarantees.

#### Corollary 4: Finite-Sample Correction
In practice $\mu_s$ must be estimated from finite validation data. Let
$n_s$ be the number of clean validation samples in state $s$, and let
$\hat_s = \frac{1}{M}\sum_m \hat_m(s)$ be the empirical
estimate, where $\hat_m(s)$ is expert $m$'s empirical error
rate on state $s$. By Hoeffding and the union bound, with probability at
least $1 - \delta_0$,
\[
|\hat_s - \mu_s| \;\leq\; B\sqrt{\frac{\log(2M/\delta_0)}{2n_s}},
\qquad \forall m, s.
\]
Define the conservative upper bound
$\tilde_s = \hat_s + B\sqrt{\log(2M/\delta_0)/(2n_s)}$.
Then Theorem [ref] holds with probability
$\geq 1 - \delta_0$ when $\tilde_s$ replaces $\mu_s$ in
$\Delta_s$.

### Connection to Dawid--Skene
<!-- label: sec:thm1:dawid-skene -->

#### Dawid--Skene model
Dawid and Skene  [cite] estimate true labels and annotator reliability
from multiple independent annotations via EM. Each annotator $m$ is assigned a
global confusion matrix
\[
\pi_m(c' \mid c) = \mathbb{P}(f_m(x) = c' \mid y^* = c), \qquad \forall x \in \mathcal{X}.
\]
The final label estimate is a weighted vote
$\hat{y}_{DS} = \arg\max_c \sum_m w_m \mathbf{1}\{f_m(x)=c\}$,
where weights $w_m$ are derived from the diagonal entries of $\pi_m$.

#### SCX generalization
SCX replaces the global confusion matrix with a state-conditioned variant:
\[
\pi_m(c' \mid c, s) = \mathbb{P}(f_m(x) = c' \mid y^* = c,\; x \in s).
\]
SCX weights therefore depend on the state:
\[
w_m(x) = \frac{\exp(-\alpha \hat{R}_m(s(x)))}
              {\sum_{m'} \exp(-\alpha \hat{R}_{m'}(s(x)))},
\qquad \hat{R}_m(s) = \sum_c \pi_m(c \mid c, s).
\]

#### Comparison
The SCX detection rule in Theorem~1 is built on the *consensus* concept
-- noisy samples exhibit high error across *all* experts -- which is
qualitatively different from Dawid--Skene's global reliability estimation.
Key differences are summarised in Table [ref].

[Table omitted — see original .tex]

When the state partition degenerates to the trivial partition
$\mathcal{S} = \{\mathcal{X}\}$, SCX recovers Dawid--Skene as a special case:
weights become global constants and the consensus score becomes the global
average error rate.

\begin{thebibliography}{10}
\bibitem{hoeffding1963}
W.~Hoeffding, ``Probability inequalities for sums of bounded random variables,''
*J. Amer. Statist. Assoc.*, vol.~58, no.~301, pp.~13--30, 1963.

\bibitem{dawid1979}
A.~P.~Dawid and A.~M.~Skene, ``Maximum likelihood estimation of observer
error-rates using the EM algorithm,''
*J. R. Statist. Soc. Ser. C*, vol.~28, no.~1, pp.~20--28, 1979.
\end{thebibliography}

\endinput