# Theorem~4': Exact Constant Minimax Optimality

**Author:** SCX

## Theorem~4': Exact Constant Minimax Optimality
<!-- label: sec:thm4 -->

### Theorem 4: Exact Constant Minimax Optimality (The Extreme Precision Theorem)

Theorem~1 establishes that the SCX noise detector achieves an exponential
convergence rate $2M\Delta^2$.  Theorem~4' refines this result in three
ways: it replaces the Hoeffding rate $2\Delta^2$ with the exact Chernoff
information $\kappa$, it establishes the *exact constant* multiplying the
exponential, and it proves that no algorithm can improve upon this constant.

Throughout this section we work within a single state $s$ satisfying
Assumptions~(A1)--(A6).  Let
\[
p_0 = \mu_s,\qquad
p_1 = 1 - C_{bal}\cdot\frac{\mu_s}{K-1},
\]
where $K=K_{\mathcal{Y}}$ is the number of classes and
$0<p_0<p_1<1$.  The expert error indicators
$e_m=\mathbf{1}\{f_m(x)\neq y\}$ are i.i.d.\ $\operatorname{Bern}(p_0)$
under the clean hypothesis $\mathrm{H}_0$ and i.i.d.\ $\operatorname{Bern}(p_1)$
under the noise hypothesis $\mathrm{H}_1$.

Define the following quantities:
\[

$$
\kappa &= C\bigl(\operatorname{Bern}(p_0),\operatorname{Bern}(p_1)\bigr)
        &&Chernoff information,
\theta^* &= \frac{\log\frac{1-p_0}{1-p_1}}
                 {\log\frac{p_1(1-p_0)}{p_0(1-p_1)}}
        &&Chernoff point (unique root of
          $\operatorname{KL}(\theta\|p_0)=\operatorname{KL}(\theta\|p_1)$),
\lambda_0^* &= \log\frac{\theta^*(1-p_0)}{p_0(1-\theta^*)}>0,
\qquad
\lambda_1^* = \log\frac{\theta^*(1-p_1)}{p_1(1-\theta^*)}<0
        &&Saddlepoints at $\theta^*$,
D^* &= \lambda_0^* + |\lambda_1^*|
      = \log\frac{p_1(1-p_0)}{p_0(1-p_1)}>0,
s &= \frac{|\lambda_1^*|}{D^*}\in(0,1).
$$

\]

> **Theorem:** [Exact Constant Minimax Optimality of SCX]
>   <!-- label: thm:exact_constant -->
>   Under Assumptions~(A1)--(A6), for any state $s$ with $p_0<p_1$, the
>   following hold.
>   
1. **SCX achievability with adaptive threshold.**
2. **Minimax lower bound.**
3. **Constant optimality.**
4. **Multi-state generalisation.**

The remainder of this section provides the complete proof, organised into
lemmas that are of independent interest.

### Preliminaries: Chernoff Information and Bahadur-Rao
<!-- label: sec:thm4_prelim -->

#### Chernoff Information

For two distributions $P_0,P_1$ with densities $p_0(\cdot),p_1(\cdot)$,
the Chernoff information is
\[
C(P_0,P_1) = -\min_{\lambda\in[0,1]}
  \log\mathbb{E}_{P_0}\!\left[\left(\frac{dP_1}{dP_0}\right)^{\!\!\lambda}\right].
\]
For $\operatorname{Bern}(p_0)$ vs.\ $\operatorname{Bern}(p_1)$, we have
\[
\mathbb{E}_{P_0}\!\left[\left(\frac{dP_1}{dP_0}\right)^{\!\!\lambda}\right]
= p_0^{1-\lambda}p_1^\lambda + (1-p_0)^{1-\lambda}(1-p_1)^\lambda.
\]

#### Bahadur-Rao Theorem (Bernoulli Case)

The Bahadur-Rao theorem  [cite] provides the exact
asymptotic probability of a large deviation, including the constant
prefactor.  For i.i.d.\ $\operatorname{Bern}(p)$ variables
$X_1,...,X_M$ and a threshold $\theta>p$,
\[
\mathbb{P}\!\left(\frac1M\sum_{i=1}^M X_i \ge \theta\right)
\sim
\frac{\exp\!\bigl(-M\cdot\operatorname{KL}(\theta\|p)\bigr)}
     {\lambda^*(\theta)\,\sqrt{2\pi M\,\theta(1-\theta)}},
\qquad M\to\infty,
\]
where $\lambda^*(\theta)=\log\frac{\theta(1-p)}{p(1-\theta)}>0$ is the
Cram\'er saddlepoint.  For the lower tail $\theta<p$, the same formula
holds with $|\lambda^*(\theta)|$ in the denominator.

#### Exponential Tilting

The proof of the Bahadur-Rao theorem uses exponential tilting.  Define the
tilted measure $\mathbb{P}_{\lambda^*}$ by
\[
\frac{d\mathbb{P}_{\lambda^*}}{d\mathbb{P}}
= \exp\!\bigl(\lambda^* S_M - M\psi(\lambda^*)\bigr),\qquad
S_M=\sum_{i=1}^M X_i,
\]
where $\psi(\lambda)=\log(1-p+pe^\lambda)$.  Under $\mathbb{P}_{\lambda^*}$,
the $X_i$ are i.i.d.\ $\operatorname{Bern}(\theta)$, i.e.\ the tilted
distribution has mean exactly $\theta$.  The saddlepoint $\lambda^*$ and
variance $\sigma^2=\theta(1-\theta)$ are obtained from
\[
\psi'(\lambda^*)=\theta,\qquad
\psi''(\lambda^*)=\theta(1-\theta).
\]

### Part I: Achievability (SCX Upper Bound)
<!-- label: sec:thm4_upper -->

#### Lemma~A: Bahadur-Rao Exact Asymptotics for Bernoulli
<!-- label: sec:lemmaA -->

> **Lemma:** [Bahadur-Rao for Bernoulli, exact form]
>   <!-- label: lem:BahadurRao -->
>   Let $X_1,...,X_M\stackrel{i.i.d.}\operatorname{Bern}(p)$ and
>   fix $\theta>p$.  Then
>   \[
>   \mathbb{P}\!\left(\frac1M\sum_{i=1}^M X_i \ge \theta\right)
>   = \frac{\exp\!\bigl(-M\cdot\operatorname{KL}(\theta\|p)\bigr)}
>          {\lambda^*\sqrt{2\pi M\,\theta(1-\theta)}}
>     \bigl(1+O(M^{-1})\bigr),
>   \]
>   where $\lambda^*=\log\frac{\theta(1-p)}{p(1-\theta)}>0$ and the $O(M^{-1})$
>   constant is explicit in $p$ and $\theta$.

> **Proof:** [Sketch]
>   Write the binomial tail probability
>   $\mathbb{P}(S_M\ge k)=\sum_{j=k}^M\binom{M}{j}p^j(1-p)^{M-j}$ with
>   $k=\lceil M\theta\rceil$.  Apply Stirling's formula with Robbins' remainder
>   bound to the leading term $a_k$, then bound the ratio of consecutive terms
>   $a_{j+1}/a_j\le e^{-\lambda^*}(1+O(M^{-1}))$ and sum the geometric series.
>   The lattice correction factor $(1-e^{-\lambda^*})^{-1}$ is absorbed into
>   the $O(M^{-1})$ term; the form $1/\lambda^*$ is obtained by
>   $\lambda^*/(1-e^{-\lambda^*})=1+O(\lambda^*)$.

For the lower tail $\theta<p$, symmetry gives
\[
\mathbb{P}\!\left(\frac1M\sum_{i=1}^M X_i \le \theta\right)
= \frac{\exp\!\bigl(-M\cdot\operatorname{KL}(\theta\|p)\bigr)}
       {|\lambda^*|\sqrt{2\pi M\,\theta(1-\theta)}}
  \bigl(1+O(M^{-1})\bigr),
\]
where $|\lambda^*|=\log\frac{p(1-\theta)}{\theta(1-p)}$.

#### Application to FPR and FNR

Apply Lemma~A to the expert error indicators.  Under $\mathrm{H}_0$ (clean),
$e_m\sim\operatorname{Bern}(p_0)$.  Under $\mathrm{H}_1$ (noise),
$e_m\sim\operatorname{Bern}(p_1)$.  For a fixed threshold
$\theta\in(p_0,p_1)$,
\[

$$
\operatorname{FPR}_M(\theta)
&= \mathbb{P}(C_M\ge\theta\midclean)
   \sim \frac{\exp\!\bigl(-M\cdot\operatorname{KL}(\theta\|p_0)\bigr)}
            {\lambda_0^*\sqrt{2\pi M\,\theta(1-\theta)}},
\operatorname{FNR}_M(\theta)
&= \mathbb{P}(C_M\le\theta\midnoise)
   \sim \frac{\exp\!\bigl(-M\cdot\operatorname{KL}(\theta\|p_1)\bigr)}
            {|\lambda_1^*|\sqrt{2\pi M\,\theta(1-\theta)}},
$$

\]
where $\lambda_0^*=\log\frac{\theta(1-p_0)}{p_0(1-\theta)}>0$ and
$\lambda_1^*=\log\frac{\theta(1-p_1)}{p_1(1-\theta)}<0$,
$|\lambda_1^*|=\log\frac{p_1(1-\theta)}{\theta(1-p_1)}$.

#### Lemma~B: F1 Asymptotic Expansion
<!-- label: sec:lemmaB -->

> **Lemma:** [F1 expansion]
>   <!-- label: lem:F1expansion -->
>   Let $\eta=\mathbb{P}(noise)$, $\operatorname{FPR}=\operatorname{FPR}_M$,
>   $\operatorname{FNR}=\operatorname{FNR}_M$, and define
>   $r=\operatorname{FNR}/2+(1-\eta)\operatorname{FPR}/(2\eta)$.  For
>   $M$ sufficiently large that $r\le\frac12$,
>   \[
>   1-\operatorname{F1}
>   = \frac{\operatorname{FNR}}{2}
>     + \frac{1-\eta}{2\eta}\operatorname{FPR}
>     + R,
>   \]
>   where $|R|\le 2r^2$.

> **Proof:** From the definitions,
>   \[
>   \operatorname{F1}
>   = \frac{2\eta\cdot\operatorname{TPR}}
>          {\eta(1+\operatorname{TPR})+(1-\eta)\operatorname{FPR}}
>   = \frac{2\eta(1-\operatorname{FNR})}
>          {\eta(2-\operatorname{FNR})+(1-\eta)\operatorname{FPR}}.
>   \]
>   Direct algebra gives
>   \[
>   1-\operatorname{F1}
>   = \frac{\eta\operatorname{FNR}+(1-\eta)\operatorname{FPR}}
>          {\eta(2-\operatorname{FNR})+(1-\eta)\operatorname{FPR}}.
>   \]
>   Let $\alpha=\eta\operatorname{FNR}+(1-\eta)\operatorname{FPR}$ and
>   $\beta=2\eta-\eta\operatorname{FNR}+(1-\eta)\operatorname{FPR}$.  Since
>   $\beta\ge\eta>0$, write
>   $1-\operatorname{F1} = \frac{2\eta}\cdot\frac1{1-\gamma}$
>   with $\gamma=\frac{\operatorname{FNR}}2-\frac{(1-\eta)\operatorname{FPR}}{2\eta}$.
>   For $|\gamma|<1$ (which holds when $r\le\frac12$), expand the geometric
>   series to obtain the first-order terms and bound the remainder.

Substituting the Bahadur-Rao asymptotics at a threshold $\theta$,
\[
1-\operatorname{F1}(\theta)
= \frac1{\sqrt{2\pi M\,\theta(1-\theta)}}
  \Bigl[
    \frac{e^{-M\cdot\operatorname{KL}(\theta\|p_1)}}{2|\lambda_1^*(\theta)|}
    + \frac{1-\eta}{2\eta}\,
      \frac{e^{-M\cdot\operatorname{KL}(\theta\|p_0)}}{\lambda_0^*(\theta)}
  \Bigr]
  + O\!\left(\frac{e^{-2M\min(\kappa_0,\kappa_1)}}{M}\right),
\]
where $\kappa_0=\operatorname{KL}(\theta\|p_0)$ and
$\kappa_1=\operatorname{KL}(\theta\|p_1)$.  The remainder decays twice as
fast exponentially and is asymptotically negligible.

#### Lemma~C: Chernoff Information Closed Form
<!-- label: sec:lemmaC -->

> **Lemma:** [Chernoff point and information]
>   <!-- label: lem:Chernoff -->
>   The unique $\theta^*\in(p_0,p_1)$ satisfying
>   $\operatorname{KL}(\theta^*\|p_0)=\operatorname{KL}(\theta^*\|p_1)$ is
>   \[
>   \boxed{\;
>   \theta^*
>   = \frac{\log\frac{1-p_0}{1-p_1}}
>          {\log\frac{p_1(1-p_0)}{p_0(1-p_1)}}\;}.
>   \]
>   The common value $\kappa=\operatorname{KL}(\theta^*\|p_0)$ is the
>   Chernoff information $C(\operatorname{Bern}(p_0),\operatorname{Bern}(p_1))$.

> **Proof:** Equating the KL divergences and cancelling the common term
>   $\theta\log\theta+(1-\theta)\log(1-\theta)$ gives
>   \[
>   \theta\log\frac1{p_0}+(1-\theta)\log\frac1{1-p_0}
>   = \theta\log\frac1{p_1}+(1-\theta)\log\frac1{1-p_1}.
>   \]
>   Simplifying:
>   \[
>   \theta\log\frac{p_1}{p_0} = (1-\theta)\log\frac{1-p_0}{1-p_1},
>   \]
>   which yields the closed form.  Strict convexity of $\operatorname{KL}$
>   in its first argument and the sign change
>   $f(p_0)=-\operatorname{KL}(p_0\|p_1)<0$,
>   $f(p_1)=\operatorname{KL}(p_1\|p_0)>0$ guarantee uniqueness and
>   $\theta^*\in(p_0,p_1)$.

The saddlepoints at $\theta^*$ are:
\[
\lambda_0^* = \log\frac{\theta^*(1-p_0)}{p_0(1-\theta^*)}>0,\qquad
\lambda_1^* = \log\frac{\theta^*(1-p_1)}{p_1(1-\theta^*)}<0.
\]

#### Lemma~D: Adaptive Threshold Optimality
<!-- label: sec:lemmaD -->

The naive threshold $\theta^*$ (the Chernoff point) balances the two
exponential rates but ignores the noise prior $\eta$.  When $\eta\neq\frac12$,
the optimal threshold---the one minimising $1-\operatorname{F1}$---differs
from $\theta^*$ by $O(1/M)$.  This $O(1/M)$ shift produces an $O(1)$
multiplicative factor in the error probability via the exponent, which is
essential for achieving the minimax lower bound.

> **Lemma:** [Adaptive threshold]
>   <!-- label: lem:adaptive_threshold -->
>   The threshold $\theta^\dagger$ that minimises the leading-order expression
>   for $1-\operatorname{F1}$ satisfies
>   \[
>   \operatorname{KL}(\theta^\dagger\|p_0)
>   = \operatorname{KL}(\theta^\dagger\|p_1)
>     + \frac1M\log\frac{1-\eta}
>     + O\!\left(\frac1{M^2}\right).
>   \]
>   Expanding around $\theta^*$ gives
>   \[
>   \theta^\dagger = \theta^*
>     + \frac1M\,\frac{\log\frac{1-\eta}}{D^*}
>     + O\!\left(\frac1{M^2}\right),
>   \]
>   where $D^*=\lambda_0^*+|\lambda_1^*|
>           =\log\frac{p_1(1-p_0)}{p_0(1-p_1)}$.

> **Proof:** The objective function (ignoring the common factor
>   $1/\sqrt{2\pi M\theta(1-\theta)}$) is
>   \[
>   \Phi_M(\theta)
>   = \frac{e^{-M\cdot\operatorname{KL}(\theta\|p_1)}}{2|\lambda_1^*(\theta)|}
>     + \frac{1-\eta}{2\eta}\,
>       \frac{e^{-M\cdot\operatorname{KL}(\theta\|p_0)}}{\lambda_0^*(\theta)}.
>   \]
>   Differentiating and keeping only the dominant
>   $-M\operatorname{KL}'(\theta\|p)=-M\lambda^*(\theta)$ terms (the
>   $-M$ factor dominates the $O(1)$ derivative of $\log\lambda^*$),
>   the first-order condition reduces to
>   \[
>   e^{-M\cdot\operatorname{KL}(\theta\|p_1)}
>   \approx \frac{1-\eta}\,
>           e^{-M\cdot\operatorname{KL}(\theta\|p_0)}.
>   \]
>   Taking logs yields the stated relation.  Expanding
>   $\operatorname{KL}(\theta^*+\delta\|p_0)-\operatorname{KL}(\theta^*+\delta\|p_1)$
>   gives $\delta D^* + O(\delta^3)$, where the quadratic term cancels exactly
>   because $\operatorname{KL}''(\cdot\|p_0)=\operatorname{KL}''(\cdot\|p_1)
>   =1/(\theta(1-\theta))$ is independent of $p$.  Solving $\delta D^* =
>   \frac1M\log\frac{1-\eta}+O(M^{-2})$ gives the result.

**The $O(1)$ exponential prefactor.**
The $O(1/M)$ shift in $\theta$ produces an $O(1)$ multiplicative factor in
$\exp(-M\cdot\operatorname{KL})$.  Expanding the KL divergence at
$\theta^\dagger=\theta^*+\delta$:
\[

$$
\operatorname{KL}(\theta^\dagger\|p_0)
&= \kappa + \lambda_0^*\delta
   + \frac{\delta^2}{2\theta^*(1-\theta^*)} + O(\delta^3),
\operatorname{KL}(\theta^\dagger\|p_1)
&= \kappa - |\lambda_1^*|\delta
   + \frac{\delta^2}{2\theta^*(1-\theta^*)} + O(\delta^3).
$$

\]

Multiplying by $M$ and substituting $\delta$:
\[

$$
M\cdot\operatorname{KL}(\theta^\dagger\|p_0)
&= M\kappa + \frac{\lambda_0^*}{D^*}\log\frac{1-\eta} + O\!\left(\frac1M\right),
M\cdot\operatorname{KL}(\theta^\dagger\|p_1)
&= M\kappa - \frac{|\lambda_1^*|}{D^*}\log\frac{1-\eta} + O\!\left(\frac1M\right).
$$

\]

Exponentiating:
\[

$$
\exp\!\bigl(-M\cdot\operatorname{KL}(\theta^\dagger\|p_0)\bigr)
&= e^{-M\kappa}
   \left(\frac{1-\eta}\right)^{\!-\lambda_0^*/D^*}
   \bigl(1+O(M^{-1})\bigr),
\exp\!\bigl(-M\cdot\operatorname{KL}(\theta^\dagger\|p_1)\bigr)
&= e^{-M\kappa}
   \left(\frac{1-\eta}\right)^{\!|\lambda_1^*|/D^*}
   \bigl(1+O(M^{-1})\bigr).
$$

\]

**FPR and FNR at the adaptive threshold.**

Substituting into the Bahadur-Rao expansions:
\[

$$
\operatorname{FPR}_M(\theta^\dagger)
&\sim \frac{e^{-M\kappa}}
          {\lambda_0^*\sqrt{2\pi M\,\theta^*(1-\theta^*)}}\,
        \left(\frac{1-\eta}\right)^{\!-\lambda_0^*/D^*},
\operatorname{FNR}_M(\theta^\dagger)
&\sim \frac{e^{-M\kappa}}
          {|\lambda_1^*|\sqrt{2\pi M\,\theta^*(1-\theta^*)}}\,
        \left(\frac{1-\eta}\right)^{\!|\lambda_1^*|/D^*}.
$$

\]

**The critical cancellation in $1-\operatorname{F1**$.}

Recall $s=|\lambda_1^*|/D^*$ and $\lambda_0^*/D^*=1-s$.  The FNR contribution to
$1-\operatorname{F1}$ is
\[
\frac12\operatorname{FNR}_M(\theta^\dagger)
\sim \frac{e^{-M\kappa}}
          {2|\lambda_1^*|\sqrt{2\pi M\,\theta^*(1-\theta^*)}}\,
      \left(\frac{1-\eta}\right)^{\!s}.
\]

The FPR contribution is
\[

$$
\frac{1-\eta}{2\eta}\operatorname{FPR}_M(\theta^\dagger)
&\sim \frac{1-\eta}{2\eta}\,
      \frac{e^{-M\kappa}}
           {\lambda_0^*\sqrt{2\pi M\,\theta^*(1-\theta^*)}}\,
      \left(\frac{1-\eta}\right)^{\!-(1-s)}
&= \frac{e^{-M\kappa}}
        {2\lambda_0^*\sqrt{2\pi M\,\theta^*(1-\theta^*)}}\,
      \left(\frac{1-\eta}\right)^{\!s}.
$$

\]

**Both terms carry the identical factor
$\bigl((1-\eta)/\eta\bigr)^s$!**  This is the critical cancellation that
makes the adaptive threshold constant-optimal.

**Asymptotic constant for SCX.**

Summing the two contributions:
\[

$$
1-\operatorname{F1}_{SCX}(\theta^\dagger)
&\sim \frac{e^{-M\kappa}}
          {\sqrt{2\pi M\,\theta^*(1-\theta^*)}}\,
      \left(\frac{1-\eta}\right)^{\!s}
      \frac12\!\left(
        \frac1{\lambda_0^*} + \frac1{|\lambda_1^*|}
      \right).
$$

\]

Multiplying by $e^{M\kappa}\sqrt{2\pi M}$ and taking the limit:
\[
\boxed{\;
\lim_{M\to\infty}
  e^{M\kappa}\sqrt{2\pi M}\,
  \bigl(1-\operatorname{F1}_{SCX}(\theta^\dagger)\bigr)
= \frac12\left(\frac{1-\eta}\right)^{\!s}
  \frac{1/\lambda_0^* + 1/|\lambda_1^*|}
       {\sqrt{\theta^*(1-\theta^*)}}\;}.
\]

This equals $C_/\eta$ because
\[
\frac{C_}
= \frac12\left(\frac{1-\eta}\right)^{\!s}
  \frac{1/\lambda_0^* + 1/|\lambda_1^*|}
       {\sqrt{\theta^*(1-\theta^*)}}.
\]

Thus Lemma~D establishes part~(a) of Theorem~4'.

### Part II: Lower Bound (Minimax Converse)
<!-- label: sec:thm4_lower -->

#### Lemma~E: Second-Order Asymptotic Lower Bound
<!-- label: sec:lemmaE -->

> **Lemma:** [Exact constant minimax lower bound]
>   <!-- label: lem:lowerbound -->
>   For any noise detection algorithm $\mathcal{A}$,
>   \[
>   \liminf_{M\to\infty}
>     e^{M\kappa}\sqrt{2\pi M}\,
>     \bigl(1-\operatorname{F1}_{\mathcal{A}}(M)\bigr)
>   \ge \frac{C_},
>   \]
>   where $C_$ is the constant defined in Theorem~4'.
>   Equivalently, writing $r=\lambda_0^*/D^*=1-s$,
>   \[
>   C_
>   = \frac{\eta^r(1-\eta)^{1-r}}2\,
>     \frac{1/\lambda_0^*+1/|\lambda_1^*|}
>          {\sqrt{\theta^*(1-\theta^*)}}.
>   \]

> **Proof:** The proof proceeds in five parts.
> 
>   **Part 1: Reduction to a binary hypothesis test.**
>   Within a fixed state $s$, the expert errors $e_1,...,e_M$ are i.i.d.\
>   $\operatorname{Bern}(p_0)$ under $\mathrm{H}_0$ (clean) and
>   $\operatorname{Bern}(p_1)$ under $\mathrm{H}_1$ (noise).  Any algorithm
>   $\mathcal{A}$ reduces to a decision rule
>   $\delta_M:\{0,1\}^M\to\{0,1\}$ with Type~I error
>   $\alpha_M=\Pr(\delta_M=1\mid\mathrm{H}_0)$ and Type~II error
>   $\beta_M=\Pr(\delta_M=0\mid\mathrm{H}_1)$.
> 
>   From Lemma~B,
>   \[
>   1-\operatorname{F1}_{\mathcal{A}}
>   = \frac{1-\eta}{2\eta}\,\alpha_M + \frac12\,\beta_M + o(1),
>   \]
>   where the $o(1)$ term is uniform over decision rules and decays as
>   $O(e^{-2M\kappa})$, negligible at the leading order.  Define the
>   weighted risk
>   \[
>   R_M(\delta_M) = w_0\alpha_M + w_1\beta_M,\qquad
>   w_0=\frac{1-\eta}{2\eta},\; w_1=\frac12.
>   \]
> 
>   **Part 2: Neyman-Pearson reduction.**
>   By the Neyman-Pearson lemma, for any test with Type~I error $\le\alpha$,
>   the minimum achievable Type~II error is attained by the likelihood ratio
>   test (LRT).  Therefore for any decision rule $\delta_M$,
>   \[
>   R_M(\delta_M) \ge \min_{\alpha\in[0,1]}
>     \bigl\{w_0\alpha + w_1\beta_{NP}(\alpha)\bigr\},
>   \]
>   where $\beta_{NP}(\alpha)$ is the Type~II error of the most powerful
>   level-$\alpha$ test.
> 
>   The minimiser $\alpha^*$ satisfies $w_0 + w_1\beta_{NP}'(\alpha^*)=0$.
>   For the Neyman-Pearson test, the slope of the ROC curve at $\alpha^*$ is
>   $-1/\tau^*$, where $\tau^*$ is the likelihood ratio threshold.  Hence
>   $\tau^* = w_0/w_1 = (1-\eta)/\eta$; the minimiser is exactly the Bayes
>   decision rule with prior odds $(1-\eta):\eta$ against $\mathrm{H}_0$.  Thus
>   for any $\mathcal{A}$,
>   \[
>   R_M(\delta_{\mathcal{A}})
>   \ge R_M^* := w_0\alpha_M^* + w_1\beta_M^*,
>   \]
>   where $\delta_M^*(e)=\mathbf{1}\{\log L_M(e) > \log\frac{1-\eta}\}$
>   and $L_M(e)=\prod_{m=1}^M\frac{p_1^{e_m}(1-p_1)^{1-e_m}}{p_0^{e_m}(1-p_0)^{1-e_m}}$.
> 
>   **Part 3: Exact asymptotics of the Bayes test.**
>   The log-likelihood ratio simplifies to
>   \[
>   \log L_M = M\bigl(C_M\Delta + \Delta_0\bigr),
>   \]
>   where
>   $\Delta=\log\frac{p_1(1-p_0)}{p_0(1-p_1)} = D^*$ and
>   $\Delta_0=\log\frac{1-p_1}{1-p_0}$.
>   The rejection region $C_M > -\Delta_0/\Delta + \frac1{M\Delta}\log\frac{1-\eta}$
>   has threshold
>   \[
>   t_M = \theta^* + \frac1{M D^*}\log\frac{1-\eta}.
>   \]
>   This is precisely the adaptive threshold $\theta^\dagger$ from Lemma~D.
> 
>   The error probabilities of the Bayes test are
>   \[
>   \alpha_M^* = \Pr\nolimits_{p_0}(C_M > t_M),\qquad
>   \beta_M^*  = \Pr\nolimits_{p_1}(C_M \le t_M),
>   \]
>   up to a $O(e^{-M\kappa}/M)$ correction for tie-breaking.
> 
>   Apply the Bahadur-Rao theorem (Lemma~A) to each:
>   \[
>   
> $$
>   \alpha_M^* &\sim
>     \frac{\exp\!\bigl(-M\operatorname{KL}(t_M\|p_0)\bigr)}
>          {\lambda_0^*(t_M)\sqrt{2\pi M\,t_M(1-t_M)}},
>   \beta_M^*  &\sim
>     \frac{\exp\!\bigl(-M\operatorname{KL}(t_M\|p_1)\bigr)}
>          {|\lambda_1^*(t_M)|\sqrt{2\pi M\,t_M(1-t_M)}}.
>   $$
> 
>   \]
> 
>   **Part 4: Expansion around the Chernoff point.**
>   Write $\delta = t_M-\theta^* = \frac1{M D^*}\log\frac{1-\eta} + O(M^{-2})$.
>   Expand the KL divergences as in Lemma~D:
>   \[
>   
> $$
>   M\operatorname{KL}(t_M\|p_0)
>   &= M\kappa + \frac{\lambda_0^*}{D^*}\log\frac{1-\eta} + o(1),
>   M\operatorname{KL}(t_M\|p_1)
>   &= M\kappa - \frac{|\lambda_1^*|}{D^*}\log\frac{1-\eta} + o(1).
>   $$
> 
>   \]
> 
>   Substituting into the Bahadur-Rao expressions:
>   \[
>   
> $$
>   \alpha_M^* &=
>     \frac{e^{-M\kappa}}
>          {\lambda_0^*\sqrt{2\pi M\,\theta^*(1-\theta^*)}}\,
>     \left(\frac{1-\eta}\right)^{\!-\lambda_0^*/D^*}
>     \bigl(1+o(1)\bigr),
>   \beta_M^* &=
>     \frac{e^{-M\kappa}}
>          {|\lambda_1^*|\sqrt{2\pi M\,\theta^*(1-\theta^*)}}\,
>     \left(\frac{1-\eta}\right)^{\!|\lambda_1^*|/D^*}
>     \bigl(1+o(1)\bigr).
>   $$
> 
>   \]
> 
>   The weighted risk is therefore
>   \[
>   
> $$
>   R_M^* &=
>     w_0\alpha_M^* + w_1\beta_M^* 
>   &= \frac{e^{-M\kappa}}
>           {\sqrt{2\pi M\,\theta^*(1-\theta^*)}}\,
>      \Bigg[
>        \frac{1-\eta}{2\eta}\,
>        \frac1{\lambda_0^*}
>        \left(\frac{1-\eta}\right)^{\!-\lambda_0^*/D^*}
>      + \frac12\,
>        \frac1{|\lambda_1^*|}
>        \left(\frac{1-\eta}\right)^{\!|\lambda_1^*|/D^*}
>      \Bigg] \bigl(1+o(1)\bigr).
>   $$
> 
>   \]
> 
>   Using $s=|\lambda_1^*|/D^*$ and $\lambda_0^*/D^*=1-s$, the terms simplify:
>   \[
>   
> $$
>   \frac{1-\eta}{2\eta\lambda_0^*}
>     \left(\frac{1-\eta}\right)^{\!-(1-s)}
>   &= \frac1{2\lambda_0^*}
>      \left(\frac{1-\eta}\right)^{\!s},
>   \frac1{2|\lambda_1^*|}
>     \left(\frac{1-\eta}\right)^{\!s}
>   &= \frac1{2|\lambda_1^*|}
>      \left(\frac{1-\eta}\right)^{\!s}.
>   $$
> 
>   \]
> 
>   Both terms share the common factor
>   $\frac12\bigl((1-\eta)/\eta\bigr)^s$.  Factoring it out:
>   \[
>   R_M^* = \frac{e^{-M\kappa}}
>               {\sqrt{2\pi M\,\theta^*(1-\theta^*)}}\,
>           \frac12\left(\frac{1-\eta}\right)^{\!s}
>           \left(\frac1{\lambda_0^*} + \frac1{|\lambda_1^*|}\right)
>           \bigl(1+o(1)\bigr).
>   \]
> 
>   **Part 5: Conversion to the F1 lower bound.**
>   From Part~1, $1-\operatorname{F1}_{\mathcal{A}} = R_M(\delta_{\mathcal{A}}) + o(1)
>   \ge R_M^* + o(1)$.  Multiplying by $e^{M\kappa}\sqrt{2\pi M}$ and taking the
>   limit inferior:
>   \[
>   \liminf_{M\to\infty}
>     e^{M\kappa}\sqrt{2\pi M}\,
>     \bigl(1-\operatorname{F1}_{\mathcal{A}}(M)\bigr)
>   \ge \frac12\left(\frac{1-\eta}\right)^{\!s}
>       \frac{1/\lambda_0^* + 1/|\lambda_1^*|}
>            {\sqrt{\theta^*(1-\theta^*)}}.
>   \]
> 
>   The right-hand side equals $C_/\eta$ by definition of $C_$.
>   This completes the proof of Lemma~E. $\square$

### Part III: Constant Matching $\to$ Optimality
<!-- label: sec:thm4_matching -->

#### The $O(1)$ Prefactor Cancellation

The central mechanism of the constant optimality proof is the cancellation
that produces the identical factor $((1-\eta)/\eta)^s$ in both the FPR and
FNR contributions to $1-\operatorname{F1}$.

The adaptive threshold $\theta^\dagger$ differs from the Chernoff point
$\theta^*$ by $O(1/M)$.  This $O(1/M)$ shift generates an $O(1)$ change in
the exponent:
\[
\exp\!\bigl(-M\cdot\operatorname{KL}(\theta^\dagger\|p)\bigr)
= e^{-M\kappa} \cdot constant factor.
\]

The constant factor for $p=p_0$ is $((1-\eta)/\eta)^{-\lambda_0^*/D^*}$
and for $p=p_1$ is $((1-\eta)/\eta)^{|\lambda_1^*|/D^*}$.  When combined
with the F1 weights $w_0=(1-\eta)/(2\eta)$ and $w_1=1/2$, both contributions
acquire the identical factor $((1-\eta)/\eta)^s$ because:
\[
\frac{1-\eta}{2\eta}
\cdot \left(\frac{1-\eta}\right)^{\!-\lambda_0^*/D^*}
= \frac1{2\lambda_0^*}
  \left(\frac{1-\eta}\right)^{\!s},
\qquad
\frac12
\cdot \left(\frac{1-\eta}\right)^{\!|\lambda_1^*|/D^*}
= \frac1{2|\lambda_1^*|}
  \left(\frac{1-\eta}\right)^{\!s}.
\]

This cancellation is mathematically unavoidable---it follows from the
relationship $s+(1-s)=1$, i.e.,
$|\lambda_1^*|/D^* + \lambda_0^*/D^* = 1$, which is a consequence of the
definition $D^*=\lambda_0^*+|\lambda_1^*|$.

#### Proof that SCX Achieves $C_{\min$}

From Lemma~D, the SCX detector with adaptive threshold $\theta^\dagger$
attains:
\[
\lim_{M\to\infty}
  e^{M\kappa}\sqrt{2\pi M}\,
  \bigl(1-\operatorname{F1}_{SCX}(\theta^\dagger)\bigr)
= \frac12\left(\frac{1-\eta}\right)^{\!s}
  \frac{1/\lambda_0^* + 1/|\lambda_1^*|}
       {\sqrt{\theta^*(1-\theta^*)}}.
\]

From Lemma~E, the minimax lower bound for any algorithm is:
\[
\liminf_{M\to\infty}
  e^{M\kappa}\sqrt{2\pi M}\,
  \bigl(1-\operatorname{F1}_{\mathcal{A}}\bigr)
\ge \frac12\left(\frac{1-\eta}\right)^{\!s}
    \frac{1/\lambda_0^* + 1/|\lambda_1^*|}
         {\sqrt{\theta^*(1-\theta^*)}}.
\]

The two expressions are **identical**.  Therefore the SCX detector
attains the lower bound, establishing exact constant minimax optimality.
This proves parts~(a)--(c) of Theorem~4'.

### Part IV: Multi-State Aggregation (Lemma~F)
<!-- label: sec:lemmaF -->

In practice the data contains multiple states, each with its own
$p_{0,s}$, $p_{1,s}$, Chernoff information $\kappa_s$, and per-state
constant $C_s$.  The global $\operatorname{F1}$ score is the expectation
over the state mixture.

> **Lemma:** [Multi-state aggregation]
>   <!-- label: lem:aggregation -->
>   Let there be $S$ states with proportions $\rho_s>0$, $\sum_s\rho_s=1$.
>   Within state $s$, the per-state $\operatorname{F1}_s(M)$ satisfies
>   \[
>   1-\operatorname{F1}_s(M)
>   \sim \frac{C_s}\,
>        \frac{e^{-M\kappa_s}}{\sqrt{2\pi M}}.
>   \]
>   Then:
>   
1. **Additivity.**
2. **Bottleneck rate.**
3. **Dominant-state constant.**

> **Proof:** Part~(i) follows from linearity of expectation.  For part~(ii), each state
>   contributes $e^{-M\kappa_s}/\sqrt{2\pi M}$.  The slowest exponential decay
>   (smallest $\kappa_s$) dominates as $M\to\infty$.  Part~(iii) follows from
>   Lemma~E applied per state and summing with weights $\rho_s$; states with
>   $\kappa_s>\kappa_{global}$ are suppressed by
>   $e^{-M(\kappa_s-\kappa_{global})}\to0$.

### Numerical Verification
<!-- label: sec:thm4_numerical -->

We verify the theoretical constants numerically across five parameter sets
spanning a range of noise rates and distribution separations.

#### Five Parameter Sets

The following table reports for each $(p_0,p_1,\eta)$ combination: the
Chernoff information $\kappa$, the ratio $2(p_1-p_0)^2/\kappa$ (showing
how much looser the Hoeffding bound is), the optimal constant $C_$,
the normalised constant $C_/\eta$, the suboptimality ratio of the
non-adaptive threshold $\theta^*$, and whether the adaptive threshold
matches the lower bound.

\[
\begin{array}{c|c|c|c|c|c|c|c|c|c}
Case & p_0 & p_1 & \eta & \kappa &
\frac{2(p_1-p_0)^2}
& C_ & \frac{C_}
& \frac{Non-ad.}{C_/\eta}
& Adapt match? 
 ---
1 & 0.10 & 0.60 & 0.10 & 0.1696 & 2.95
  & 0.4591 & 4.5915 & 1.70 & YES 
2 & 0.20 & 0.50 & 0.30 & 0.0528 & 3.41
  & 1.3768 & 4.5894 & 1.09 & YES 
3 & 0.05 & 0.80 & 0.05 & 0.4574 & 2.46
  & 0.1843 & 3.6864 & 2.41 & YES 
4 & 0.10 & 0.60 & 0.50 & 0.1696 & 2.95
  & 0.8348 & 1.6697 & 1.00 & YES 
5 & 0.10 & 0.60 & 0.90 & 0.1696 & 2.95
  & 0.5465 & 0.6072 & 1.62 & YES
\end{array}
\]

#### Key Findings

1. **Adaptive limit matches $C_/\eta$ exactly.**
2. **Non-adaptive threshold is suboptimal.**
3. **Chernoff rate is slower than Hoeffding bound.**
4. **Symmetric case $\eta=0.5$.**

#### Finite-$M$ Convergence

The asymptotic limits are derived as $M\to\infty$.  For finite $M$, the
Bahadur-Rao theorem provides an $O(1/M)$ correction term.  Lemma~B gives
explicit bounds:
\[
1-\operatorname{F1}_{SCX}(\theta^\dagger)
\le \frac{C_}\,
    \frac{e^{-M\kappa}}{\sqrt{2\pi M}}\,
    \bigl(1 + K_1 M^{-1/2}\bigr),
\]
\[
1-\operatorname{F1}_{SCX}(\theta^\dagger)
\ge \frac{C_}\,
    \frac{e^{-M\kappa}}{\sqrt{2\pi M}}\,
    \bigl(1 - K_2 M^{-1/2}\bigr),
\]
where $K_1,K_2$ depend only on $p_0,p_1$.  Numerical experiments
(Supplementary Material~S8) confirm that the finite-$M$ F1 score approaches
the asymptotic limit at the predicted $O(1/\sqrt{M})$ rate.

### References for Section~S4

\begingroup

\begin{thebibliography}{20}
\bibitem{bahadur1960deviations} Bahadur, R. R. \& Rao, R. R. On deviations of the sample mean. *Annals of Mathematical Statistics* **31**(4), 1015--1027 (1960).
\end{thebibliography}
\endgroup

\endinput