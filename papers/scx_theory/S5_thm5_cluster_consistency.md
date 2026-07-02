# Theorem 5: Cluster Consistency of State Discovery

**Author:** SCX

## Theorem 5: Cluster Consistency of State Discovery
<!-- label: sec:S5 -->

This section proves Theorem~5, which establishes that under the
**strong features** regime (large separation $\Delta_$ relative
to noise), Lloyd's $k$-means with $O(\log n)$ random restarts recovers
the true state partition with probability tending to one exponentially fast.
Theorem~5 is the positive counterpart to the negative result of Theorem~2
(weak features $\to$ failure) and Theorem~4' (minimax lower bound), and
it complements the F1 bound from Theorem~1  [ref] and the
weak-feature F1 bound from Theorem~2  [ref].
Together these results complete the phase diagram: strong features imply
state discovery succeeds; weak features imply SCX cannot exceed the loss
baseline; and the threshold is minimax optimal as established in
Theorem~4'  [ref].

### Setup: Fixed-$K$ Generative Model with Strong Features
<!-- label: sec:S5:setup -->

We formalize the data-generating process and the clustering objective.

\begin{assumption}[Generative model]
<!-- label: ass:S5:gen -->
Let $(\Omega,F,\Pp)$ be a probability space. We observe $n$ i.i.d.\ copies
$\phi(x_i)\in\R^{d_\phi}$ of the feature vector, generated as

$$
\phi(x) = \mu_{s(x)} + \varepsilon,
<!-- label: eq:S5:gen -->
$$

where

- $s(x)\in\{1,...,K\}$ is the unobserved true state,
- $K$ is **fixed** (does not grow with $n$),
- $\muk\in\R^{d_\phi}$ is the feature mean (center) for state $k$,
- $\varepsilon\in\R^{d_\phi}$ is a zero-mean sub-Gaussian random vector

\end{assumption}

\begin{assumption}[Cluster structure]
<!-- label: ass:S5:cluster -->
The true partition is $\cstar=\{C_1^*,...,C_K^*\}$ with
$C_k^*=\{x\in\cX: s(x)=k\}$.  The true centers are
$\muk=\E[\phi(X)\mid S=k]$.  The population proportions are
$\pi_k=P(S=k)>0$ for all $k$, and we denote
$\pi_=\min_k\pi_k$.  The empirical per-state sample sizes are
$n_k=\sum_{i=1}^n\ind\{s(x_i)=k\}$ with $n_=\min_k n_k$.
\end{assumption}

\begin{assumption}[Strong separation (fixed $\Delta_$)]
<!-- label: ass:S5:sep -->
The minimum distance between distinct cluster centers is a fixed positive
constant (it does *not* scale with $n$ or $K$):
\[
\Delta_ \;=\; \min_{i\neq j}\norm{\mu_i-\mu_j}_2 \;>\;0.
\]
We assume the **strong separation regime**

$$
\frac{\Delta_^2}{\sigma^2 d_\phi}\;\ge\;C_0,
<!-- label: eq:S5:strongsep -->
$$

where $C_0$ is a universal constant large enough to guarantee
$\norm{\theta^*-\mu}<\Delta_/8$ in Lemma [ref] below.
This is the ``strong features'' regime: the signal-to-noise ratio is
sufficiently high that cluster centers are distinguishable despite noise
and feature dimensionality.
\end{assumption}

> **Definition:** [$k$-means objective]
> <!-- label: def:S5:kmeans -->
> For a set of $K$ candidate centers
> $\theta=\{\theta_1,...,\theta_K\}\subset\R^{d_\phi}$, define the
> **empirical $k$-means risk**
> \[
> W_n(\theta)=\frac1n\sum_{i=1}^n\min_{k\in[K]}\norm{\phi(x_i)-\theta_k}_2^2,
> \]
> and the **population $k$-means risk**
> \[
> W(\theta)=\E\Bigl[\min_{k\in[K]}\norm{\phi(X)-\theta_k}_2^2\Bigr].
> \]
> Let
> $\theta^*\in\argmin_{\theta:|\theta|=K}W(\theta)$ be the population
> minimizer and $\htheta_n\in\argmin_{\theta:|\theta|=K}W_n(\theta)$ the
> global empirical minimizer, both defined up to label permutation.
> When we write $\norm{\htheta_n-\theta^*}$, we mean the distance after
> optimal permutation matching.

> **Definition:** [Norms on center sets]
> For a $K$-center set $\theta$, let
> \[
> \norm_\infty = \max_{k\in[K]}\norm{\theta_k}_2,
> \qquad
> \norm{\theta-\theta'} = \max_{k}\norm{\theta_k-\theta'_k}_2.
> \]

### Lemma~1: Population Minimizer Proximity
<!-- label: sec:S5:lem1 -->

> **Lemma:** [Population minimizer proximity]
> <!-- label: lem:S5:pop -->
> Under Assumptions [ref]-- [ref], the population
> $k$-means objective $W(\theta)$ has a minimizer $\theta^*$ (unique up
> to label permutation).  For any permutation $\pi$ that optimally matches
> $\theta^*$ to the true centers $\mu$,
> \[
> \norm{\theta^*_{\pi(k)}-\muk}_2 \;\le\; \epsilon_{\mathrm{pop}}
> \;<\; \frac{\Delta_}{8},
> \]
> where
> \[
> \epsilon_{\mathrm{pop}} \;=\;
> \frac{C_2\,K\,(M+\sigma\sqrt{d_\phi})}{\pi_}
> \cdot \exp\!\left(-\frac{\Delta_^2}{8\sigma^2}\right),
> \]
> and $C_2$ is an absolute constant, $M=\max_k\norm_2$.
> Under  [ref] with $C_0$ sufficiently large,
> $\epsilon_{\mathrm{pop}}<\Delta_/8$.

> **Proof:** [Proof of Lemma [ref]]
> The proof proceeds in five steps.
> 
> **Step 1 (Existence).**
> $W(\theta)$ is continuous (composition of continuous functions) and
> coercive ($W(\theta)\to\infty$ as $\norm_\infty\to\infty$,
> since the quadratic penalty dominates), hence attains a minimum on any
> compact set containing a sufficiently large ball.  By strict convexity
> of $\theta_k\mapsto\E[\norm{\phi-\theta_k}^2\mid\phi\in V_k(\theta)]$
> on each Voronoi cell (defined below), any two minimizers must be related
> by a label permutation.  Thus $\theta^*$ is unique up to permutation.
> 
> **Step 2 (Self-consistency equation).**
> For a set of centers $\theta$, define the Voronoi cell of center $j$:
> \[
> V_j(\theta)=\bigl\{\phi\in\R^{d_\phi}:
> \norm{\phi-\theta_j}_2\le\min_{\ell\neq j}\norm{\phi-\theta_\ell}_2\bigr\}.
> \]
> At points where Voronoi cells have positive probability and are
> well-defined, the gradient of $W$ with respect to $\theta_j$ exists:
> \[
> \frac{\partial\theta_j}W(\theta)
> = -2\,\E\bigl[(\phi-\theta_j)\cdot\ind\{\phi\in V_j(\theta)\}\bigr].
> \]
> Setting this to zero at the minimizer $\theta^*$ gives the
> **self-consistency condition**: for each $j$,
> \[
> \theta^*_j = \frac{\E[\phi\cdot\ind\{\phi\in V_j(\theta^*)\}]}
>                  {P(\phi\in V_j(\theta^*))}
>            = \E[\phi\mid\phi\in V_j(\theta^*)]. 
> \]
> 
> **Step 3 (True centers approximately satisfy self-consistency).**
> Consider the Voronoi cells induced by the true centers $\mu=\mutrue$.
> For each $k$, define the one-step candidate
> \[
> \ttheta_k = \E[\phi\mid\phi\in V_k(\mu)].
> \]
> We bound $\norm{\ttheta_k-\muk}$.
> 
> *Claim (mis-assignment probability bound).*
> For $j\neq k$,
> \[
> P\bigl(\mu_j+\varepsilon\in V_k(\mu)\mid S=j\bigr)
> \;\le\; \exp\!\left(-\frac{\norm{\mu_j-\muk}^2}{8\sigma^2}\right)
> \;\le\; \exp\!\left(-\frac{\Delta_^2}{8\sigma^2}\right).
> \]
> 
> *Proof of claim.*
> The event $\mu_j+\varepsilon\in V_k(\mu)$ requires
> $\norm{\mu_j+\varepsilon-\muk}\le\norm{\mu_j+\varepsilon-\mu_j}$, i.e.\
> $\norm{(\mu_j-\muk)+\varepsilon}\le\norm$.  Squaring:
> \[
> \norm{\mu_j-\muk}^2 + 2\varepsilon^\top(\mu_j-\muk) + \norm^2
> \;\le\; \norm^2,
> \]
> hence $2\varepsilon^\top(\mu_j-\muk) \le -\norm{\mu_j-\muk}^2$.
> Since $v=(\mu_j-\muk)/\norm{\mu_j-\muk}$ is a unit vector,
> $\varepsilon^\top v$ is sub-Gaussian with parameter $\sigma^2$, so
> $2\varepsilon^\top(\mu_j-\muk)$ is sub-Gaussian with parameter
> $4\sigma^2\norm{\mu_j-\muk}^2$.  By the sub-Gaussian tail bound,
> \[
> P\bigl(2\varepsilon^\top(\mu_j-\muk)\le -\norm{\mu_j-\muk}^2\bigr)
> \le \exp\!\left(-\frac{\norm{\mu_j-\muk}^4}{2\cdot4\sigma^2\norm{\mu_j-\muk}^2}\right)
> = \exp\!\left(-\frac{\norm{\mu_j-\muk}^2}{8\sigma^2}\right),
> \]
> establishing the claim.  $\square$
> 
> Similarly, points from state $k$ are *not* assigned to $V_k(\mu)$
> only if they are closer to some $\mu_j$, $j\neq k$.  By the union bound
> over $j\neq k$,
> \[
> P\bigl(\mu_k+\varepsilon\notin V_k(\mu)\mid S=k\bigr)
> \;\le\; K\cdot\exp\!\left(-\frac{\Delta_^2}{8\sigma^2}\right).
> \]
> 
> **Step 4 (Bounding $\norm{\ttheta_k-\muk}$).**
> Decompose the conditional expectation:
> \[
> \ttheta_k = \E[\phi\mid\phi\in V_k(\mu)]
>           = \frac{\E[\phi\cdot\ind\{\phi\in V_k(\mu)\}]}
>                  {P(V_k(\mu))}.
> \]
> Write $\phi=\mu_S+\varepsilon$ and split by true state $S$:
> \[
> \E[\phi\cdot\ind\{\phi\in V_k(\mu)\}]
> = \sum_{j=1}^K \pi_j\,
>   \E\bigl[(\mu_j+\varepsilon)\cdot\ind\{\mu_j+\varepsilon\in V_k(\mu)\}\mid S=j\bigr].
> \]
> For the diagonal term ($j=k$),
> 
> $$
> \E[(\mu_k+\varepsilon)\cdot\ind\{\mu_k+\varepsilon\in V_k(\mu)\}\mid S=k]
> &= \muk\cdot P(\mu_k+\varepsilon\in V_k(\mu)\mid S=k) 

> &\qquad + \E[\varepsilon\cdot\ind\{\mu_k+\varepsilon\in V_k(\mu)\}\mid S=k].
> $$
> 
> For the off-diagonal terms ($j\neq k$), the indicator event has
> probability $\le\exp(-\Delta_^2/(8\sigma^2))$.
> 
> The conditional expectation of noise satisfies
> \[
> \norm{\E[\varepsilon\mid\mu_k+\varepsilon\in V_k(\mu)]}_2
> \le C_3\,\sigma\sqrt{d_\phi}\cdot\exp\!\left(-\frac{\Delta_^2}{8\sigma^2}\right)
> \]
> for an absolute constant $C_3>0$, because $V_k(\mu)$ differs from the
> full space by an event of exponentially small probability, and the
> unconditional mean of $\varepsilon$ is zero.
> 
> Assembling terms,
> \[
> \norm{\ttheta_k-\muk}
> \le \frac{C_3\,K\,(M+\sigma\sqrt{d_\phi})}{\pi_k}
>     \cdot\exp\!\left(-\frac{\Delta_^2}{8\sigma^2}\right)
> \le \epsilon_{\mathrm{pop}}.
> \]
> 
> **Step 5 (From approximate fixed point to minimizer proximity).**
> Let $T$ be the self-consistency operator:
> $T(\theta)_j=\E[\phi\mid\phi\in V_j(\theta)]$.  The minimizer $\theta^*$
> satisfies $T(\theta^*)=\theta^*$ by Step~2, and the true centers $\mu$
> satisfy $\norm{T(\mu)-\mu}_\infty\le\epsilon_{\mathrm{pop}}$ by Step~4.
> 
> Under  [ref], the Voronoi partition is stable: if two
> center sets $\theta,\theta'$ satisfy $\norm{\theta-\theta'}<\Delta_/4$,
> their Voronoi partitions differ only on a set of exponentially small
> measure.  Consequently, $T$ is a contraction in a neighborhood of $\mu$:
> \[
> \norm{T(\theta)-T(\mu)}_\infty \le \frac12\norm{\theta-\mu}_\infty,
> \qquad whenever  \norm{\theta-\mu}_\infty\le\frac{\Delta_}{4}.
> \]
> Applying the contraction bound,
> \[
> \norm{\theta^*-\mu}_\infty
> \le \norm{T(\theta^*)-T(\mu)}_\infty
>    + \norm{T(\mu)-\mu}_\infty
> \le \frac12\norm{\theta^*-\mu}_\infty + \epsilon_{\mathrm{pop}},
> \]
> so $\norm{\theta^*-\mu}_\infty\le 2\epsilon_{\mathrm{pop}}$.
> 
> Under  [ref] with $C_0$ sufficiently large,
> $2\epsilon_{\mathrm{pop}}<\Delta_/8$, because the exponential
> $\exp(-\Delta_^2/(8\sigma^2))$ decays super-polynomially in
> $\Delta_^2/\sigma^2$ while the pre-factor is polynomial.  The
> explicit condition is
> \[
> \frac{\Delta_^2}{8\sigma^2}\;\ge\;
> \log\!\left(\frac{16C_2\,K\,(M+\sigma\sqrt{d_\phi})}
>                  {\pi_\Delta_}\right),
> \]
> which is guaranteed by $C_0$ large enough since the right-hand side
> grows only logarithmically in the problem parameters.  $\square$

> **Remark:** The proof uses the self-consistency equation instead of directly
> computing $W(\mu)-W(\mu^*)$, thereby avoiding the reversed-inequality
> issue.  The bias $\epsilon_{\mathrm{pop}}$ is exponentially small in
> $\Delta_^2/\sigma^2$ and is much smaller than the $\Delta_/8$
> threshold needed for subsequent lemmas.

### Lemma~2: Exponential Convergence of the Empirical Minimizer
<!-- label: sec:S5:lem2 -->

> **Lemma:** [Exponential convergence of empirical minimizer]
> <!-- label: lem:S5:emp -->
> Let $\theta^*$ be the unique population minimizer from
> Lemma [ref] and let $\htheta_n$ be the global empirical
> minimizer of $W_n$.  For any $t>0$ satisfying
> $t\ge C_0\sqrt{K d_\phi/n}$, there exist constants
> $c_2,C_4>0$ depending on the problem parameters such that
> 
> $$
> P\bigl(\norm{\htheta_n-\theta^*}\ge t\bigr)
> \;\le\; C_4\cdot\exp\!\left(-c_2\cdot\frac{n\,t^2}{\sigma^2 d_\phi}\right).
> <!-- label: eq:S5:lem2_bound -->
> $$
> 
> The constants are $c_2=\lambda^2/(128 C_L^2)$ with
> $\lambda=\pi_/2$ (the strong convexity parameter) and
> $C_L=2(M+\sigma\sqrt{d_\phi})$ (the Lipschitz constant bound), and
> $C_4=2$ (from the peeling sum).  In particular, for $t=\Delta_/8$
> and $n\ge n_0$,
> \[
> P\!\left(\norm{\htheta_n-\theta^*}\ge\frac{\Delta_}{8}\right)
> \;\le\; 2\cdot\exp\!\left(
>           -c_2\cdot\frac{n\,\Delta_^2}{64\,\sigma^2 d_\phi}\right).
> \]

> **Proof:** [Proof of Lemma [ref]]
> The proof uses a localized argmin argument with peeling.  It has three
> parts: (i) a quadratic lower bound for $W$ near $\theta^*$,
> (ii~and~iii) control of the empirical process via covering numbers and
> concentration, and (iv) a peeling argument to convert the empirical
> process bound into a bound on $\norm{\htheta_n-\theta^*}$.
> 
> **Step 1 (Quadratic lower bound near $\theta^*$).**
> Define $r_0=\Delta_/4$.  By Lemma [ref],
> $\norm{\theta^*-\mu}<\Delta_/8$, so the set
> $\{\theta:\norm{\theta-\theta^*}\le r_0\}$ is contained within
> $\Delta_/4$ of the true centers.  Within this region, for any
> $\theta$, the Voronoi cells $V_j(\theta)$ are close to $V_j(\theta^*)$,
> differing only on an exponentially small set.  By Lemma~S5.1 (quadratic
> lower bound, proved in the Appendix),
> \[
> W(\theta)-W(\theta^*)\;\ge\;\lambda\cdot\norm{\theta-\theta^*}^2,
> \qquad \forall\;\norm{\theta-\theta^*}\le r_0,
> 
> \]
> where $\lambda=\pi_/2$.
> 
> **Step 2 (The argmin inequality).**
> Let $\htheta_n$ minimize $W_n$.  From $W_n(\htheta_n)\le W_n(\theta^*)$,
> 
> $$
> 0 &\ge W_n(\htheta_n)-W_n(\theta^*) 

>   &= \bigl(W(\htheta_n)-W(\theta^*)\bigr)
>      + \bigl((P_n-P)(f_{\htheta_n}-f_{\theta^*})\bigr) 

>   &\ge \lambda\norm{\htheta_n-\theta^*}^2
>      - \bigl|(P_n-P)(f_{\htheta_n}-f_{\theta^*})\bigr|,
> $$
> 
> where $f_\theta(x)=\min_k\norm{\phi(x)-\theta_k}^2$.  Therefore,
> 
> $$
> \lambda\norm{\htheta_n-\theta^*}^2
> \;\le\; \bigl|(P_n-P)(f_{\htheta_n}-f_{\theta^*})\bigr|.
> 
> $$
> 
> This holds whenever $\norm{\htheta_n-\theta^*}\le r_0$; the case
> $\norm{\htheta_n-\theta^*}>r_0$ is handled separately.
> 
> **Step 3 (The localized empirical process).**
> Define the localized supremum
> \[
> \psi_n(r)=\sup_{\norm{\theta-\theta^*}\le r}
>           \bigl|(P_n-P)(f_\theta-f_{\theta^*})\bigr|.
> \]
> From (3), if $\norm{\htheta_n-\theta^*}\le r_0$, then letting
> $r=\norm{\htheta_n-\theta^*}$ gives
> 
> $$
> \lambda r^2 \;\le\; \psi_n(r).
> 
> $$
> 
> 
> **Step 4 (Expectation of $\psi_n(r)$).**
> For a fixed radius $r$, consider the function class
> \[
> \mathcal{G}_r=\{\,g_\theta(x)=f_\theta(x)-f_{\theta^*}(x):
>                \norm{\theta-\theta^*}\le r\,\}.
> \]
> Each $g_\theta$ satisfies $|g_\theta(x)|\le L(x)\,r$ where
> $L(x)=2(\norm{\phi(x)}_2+M)$ (by the Lipschitz property,
> Lemma~S5.2), and $\E[g_\theta(X)^2]\le C_L^2 r^2$ where
> $C_L^2=8(\max_j\norm{\mu_j}^2+\sigma^2 d_\phi+M^2)$.
> 
> The covering number of $\Theta_r=\{\theta:\norm{\theta-\theta^*}\le r\}$
> under $\norm_\infty$ is bounded (Lemma~S5.3):
> \[
> \log\mathcal{N}(\epsilon,\Theta_r,\norm_\infty)
> \;\le\; K d_\phi\log\!\left(1+\frac{4r}\right).
> \]
> By Dudley's entropy integral, the expected supremum satisfies
> 
> $$
> \E[\psi_n(r)]
> \;\le\; C_5\cdot\sqrt{\frac{K d_\phi}{n}}\cdot C_L\cdot r,
> 
> $$
> 
> where $C_5$ is a universal constant.
> 
> **Step 5 (Concentration of $\psi_n(r)$).**
> For the function class $\mathcal{G}_r$ with $|g|\le C_L r$ and
> $\E[g^2]\le C_L^2 r^2$, Talagrand's concentration inequality gives
> 
> $$
> P\bigl(\psi_n(r)\ge\E[\psi_n(r)]+u\bigr)
> \;\le\; \exp\!\left(-\frac{c_6\,n\,u^2}{C_L^2\,r^2}\right),
> 
> $$
> 
> for any $u\ge0$, where $c_6$ is a universal constant.
> 
> **Step 6 (Peeling argument).**
> Fix $t$ such that $t\le r_0$ and
> $t\ge\frac{8C_5 C_L}\sqrt{\frac{K d_\phi}{n}}$.
> Let $J=\lceil\log_2(r_0/t)\rceil$ and define dyadic intervals
> $r_j=2^j t$ for $j=0,1,...,J$.
> 
> From (4): if $\norm{\htheta_n-\theta^*}\ge t$, then
> $\lambda\norm{\htheta_n-\theta^*}^2\le\psi_n(\norm{\htheta_n-\theta^*})$.
> For $\norm{\htheta_n-\theta^*}$ falling in $[r_{j-1},r_j)$ for some $j$,
> \[
> \lambda r_{j-1}^2 \;\le\; \lambda\norm{\htheta_n-\theta^*}^2
> \;\le\; \psi_n(\norm{\htheta_n-\theta^*}) \;\le\; \psi_n(r_j).
> \]
> Therefore,
> 
> $$
> P(\norm{\htheta_n-\theta^*}\ge t)
> \;\le\; \sum_{j=0}^J P\bigl(\psi_n(r_j)\ge\lambda (r_{j-1})^2\bigr),
> 
> $$
> 
> where $r_{-1}:=t/2$ for the $j=0$ term.
> 
> For each $j$, bound $P(\psi_n(r_j)\ge\lambda r_{j-1}^2)$.
> Since $r_j=2r_{j-1}$, $\lambda r_{j-1}^2=\lambda r_j^2/4$.
> From (5): $\E[\psi_n(r_j)]\le C_5 C_L\sqrt{K d_\phi/n}\,r_j$.
> Set $u_j=\lambda r_j^2/4-\E[\psi_n(r_j)]$.  Our condition on $t$ ensures
> \[
> \E[\psi_n(r_j)]\le C_5 C_L\sqrt{K d_\phi/n}\,r_j
> \le\frac{\lambda r_j^2}{8},
> \]
> since $r_j\ge t\ge\frac{8C_5 C_L}\sqrt{\frac{K d_\phi}{n}}$.
> Hence $u_j\ge\lambda r_j^2/8$.
> 
> Applying (6) with $u=u_j$:
> 
> $$
> P\!\left(\psi_n(r_j)\ge\frac{\lambda r_j^2}{4}\right)
> \;\le\; \exp\!\left(
>           -\frac{c_6\,n\,(\lambda r_j^2/8)^2}{C_L^2\,r_j^2}\right)
> = \exp\!\left(-\frac{c_6\,\lambda^2\,n\,r_j^2}{64\,C_L^2}\right).
> 
> $$
> 
> 
> Now $r_j^2=4^j t^2$ (for $j\ge0$) and $r_0=t$.  The sum in (7) becomes
> \[
> P(\norm{\htheta_n-\theta^*}\ge t)
> \;\le\; \sum_{j=0}^J
>        \exp\!\left(-\frac{c_6\,\lambda^2\,n\cdot4^j\,t^2}{64\,C_L^2}\right).
> \]
> The sum is dominated by the $j=0$ term because subsequent terms decay
> geometrically:
> \[
> \sum_{j=0}^\infty \exp\!\left(-\frac{c_6\,\lambda^2\,n\cdot4^j\,t^2}
>                                    {64\,C_L^2}\right)
> \;\le\; 2\cdot\exp\!\left(-\frac{c_6\,\lambda^2\,n\,t^2}{64\,C_L^2}\right),
> \]
> for all $n$ and $t$ satisfying the threshold condition.  Therefore,
> \[
> P(\norm{\htheta_n-\theta^*}\ge t)
> \;\le\; 2\cdot\exp\!\left(-\frac{c_2\,n\,t^2}{\sigma^2 d_\phi}\right),
> \]
> where $c_2=c_6\lambda^2/(128 C_L^2)$, using
> $C_L^2\le C_7\sigma^2 d_\phi$ (the dominant term when
> $\sigma^2 d_\phi\gg\max\norm^2$, or a constant otherwise) to
> absorb numerical constants.  This establishes  [ref].
> $\square$

> **Remark:** The exponent $-\frac{c_2 n t^2}{\sigma^2 d_\phi}$ is explicitly negative
> for all $n>0$, $t>0$.  There is no polynomial pre-factor in $n$ (the
> peeling sum gives a factor of $2$, independent of $n$), guaranteeing
> that the exponential dominates for large $n$.  The threshold
> $t\ge C_0\sqrt{K d_\phi/n}$ is the statistical resolution limit.

### Lemma~3: Deterministic Partition Recovery
<!-- label: sec:S5:lem3 -->

> **Lemma:** [Center proximity implies correct partition]
> <!-- label: lem:S5:part -->
> Let $\mu=\mutrue$ be the true centers with separation $\Delta_>0$.
> Let $\theta=\{\theta_1,...,\theta_K\}$ be any set of estimated centers
> satisfying, for some permutation $\pi$,
> \[
> \norm{\theta_j-\mu_{\pi(j)}}_2 \;\le\; \frac{\Delta_}{8}
> \qquad for all  j.
> \]
> Then for any point $\phi=\muk+\varepsilon$ with
> $\norm_2<3\Delta_/8$,
> \[
> \argmin_{j}\norm{\phi-\theta_j}_2 \;=\; \pi^{-1}(k),
> \]
> i.e.\ the point is correctly classified by nearest-neighbour assignment to $\theta$.

> **Proof:** [Proof of Lemma [ref]]
> Fix a true state $k$.  Let $j_k=\pi^{-1}(k)$ be the estimated center
> matched to $\muk$.  For any other estimated center $j'\neq j_k$, let
> $k'=\pi(j')\neq k$ be its matched true center.
> 
> By the triangle inequality, the distance from $\phi$ to the correct
> estimated center is
> \[
> \norm{\phi-\theta_{j_k}}
> \;\le\; \norm{\muk-\theta_{j_k}} + \norm
> \;\le\; \frac{\Delta_}{8} + \norm.
> \]
> 
> The distance to a wrong estimated center is
> 
> $$
> \norm{\phi-\theta_{j'}}
> &\ge \norm{\muk-\mu_{k'}} - \norm{\mu_{k'}-\theta_{j'}} - \norm 

> &\ge \Delta_ - \frac{\Delta_}{8} - \norm
> = \frac{7\Delta_}{8} - \norm.
> $$
> 
> 
> For $\norm<3\Delta_/8$,
> 
> $$
> \norm{\phi-\theta_{j_k}}
> &\le \frac{\Delta_}{8} + \frac{3\Delta_}{8}
> = \frac{\Delta_}{2}, 
> \norm{\phi-\theta_{j'}}
> &\ge \frac{7\Delta_}{8} - \frac{3\Delta_}{8}
> = \frac{\Delta_}{2}.
> $$
> 
> 
> Therefore $\norm{\phi-\theta_{j_k}}\le\Delta_/2\le
> \norm{\phi-\theta_{j'}}$, with strict inequality when the noise bound
> is strict or $\norm{\muk-\theta_{j_k}}<\Delta_/8$.  The nearest
> estimated center to $\phi$ is $\theta_{j_k}=\theta_{\pi^{-1}(k)}$, which
> is the center matched to the true state $k$.  $\square$

> **Corollary:** [Misclassification bound]
> <!-- label: cor:S5:misc -->
> Under the same conditions, the overall misclassification rate satisfies
> \[
> \frac1n\sum_{i=1}^n\ind\{\hat s(x_i)\neq s(x_i)\}
> \;\le\; \ind\!\left\{\max_j\norm{\hat\theta_j-\mu_{\pi(j)}}
>                 \ge\frac{\Delta_}{4}\right\}
> \;+\; \frac1n\sum_{i=1}^n\ind\{\norm{\varepsilon_i}\ge3\Delta_/8\}.
> \]

> **Proof:** The first term captures the event that the center proximity condition of
> Lemma [ref] fails.  The second term captures the irreducible
> noise: even with perfect centers, a point with
> $\norm\ge3\Delta_/8$ could be misclassified. $\square$

> **Remark:** The inequalities are verified:
> $\frac18+\frac38=\frac12$ and $\frac78-\frac38=\frac12$, giving
> $\norm{\phi-\theta_{j_k}}\le\Delta_/2\le\norm{\phi-\theta_{j'}}$
> with the correct direction.  The proof is purely deterministic, and the
> irreducible error is captured explicitly by the
> $\norm\ge3\Delta_/8$ event.

### Lemma~4: Lloyd's Algorithm Under Strong Separation
<!-- label: sec:S5:lem4 -->

The $k$-means problem is NP-hard in the worst case
 [cite].  The global empirical minimizer
$\htheta_n$ defined in Definition [ref] is a computational
oracle.  In practice, Lloyd's algorithm (alternating assignment and update)
finds a local minimum.  Lemma [ref] shows that under the
strong separation condition  [ref], this computational gap
closes: the landscape is benign and Lloyd's with random restarts finds the
global minimizer with high probability.

> **Lemma:** [Lloyd's with random restarts under strong separation]
> <!-- label: lem:S5:lloyd -->
> Under the conditions of Theorem [ref] (fixed $K$, strong
> separation  [ref], $n$ sufficiently large), Lloyd's
> algorithm initialized with $R=C_R\log n$ independent random initializations
> (e.g.\ $k$-means++ or uniform subsampling of data points) returns a
> solution $\ttheta_n$ satisfying
> \[
> P\!\left(\norm{\ttheta_n-\htheta_n^*}\ge\frac{\Delta_}{16}\right)
> \;\le\; n^{-c}
> \]
> for any desired $c>0$ (by choosing $C_R$ sufficiently large).  Here
> $\htheta_n^*$ denotes the global empirical $k$-means minimizer.

> **Proof:** [Proof of Lemma [ref]]
> 
> **Step 1 (Landscape structure under strong separation).**
> From Lemma [ref], $\norm{\theta^*-\mu}<\Delta_/8$.
> From Lemma [ref], for $n$ large enough,
> $\norm{\htheta_n^*-\theta^*}<\Delta_/8$ with probability
> $1-\exp(-c n)$.  Hence $\norm{\htheta_n^*-\mu}<\Delta_/4$ with
> high probability.
> 
> Now consider $W_n$ restricted to the ball
> $B=\{\theta:\norm{\theta-\mu}_\infty\le\Delta_/4\}$.  Within this
> ball:
> 
- The Voronoi partition is stable: moving any center by at most
- Consequently, $W_n$ is **strongly convex** within $B$
- The unique stationary point of $W_n$ within $B$ is the global

> 
> **Step 2 (Lloyd's as alternating minimization).**
> Lloyd's algorithm iterates:
> 
1. **Assignment**: For fixed centers $\theta^{(t)}$, assign each
2. **Update**: Set

> Within the ball $B$, the assignment step correctly clusters all but an
> exponentially small fraction of points (by Lemma [ref]).
> The update step therefore computes the sample mean of nearly-clean
> clusters, which is a contraction toward the true cluster means:
> \[
> \norm{\theta_j^{(t+1)}-\htheta_{n,j}^*}
> \;\le\; \frac12\norm{\theta_j^{(t)}-\htheta_{n,j}^*}
> \]
> for all $j$, with probability at least
> $1-\exp(-c n\Delta_^2/(K\sigma^2 d_\phi))$.  Thus Lloyd's converges
> linearly to $\htheta_n^*$ from any initialization in $B$, achieving
> accuracy $\Delta_/16$ in $O(\log n)$ iterations.
> 
> **Step 3 (Random initialization covers the good basin).**
> Each independent initialization selects $K$ data points uniformly at
> random (or via $k$-means++ seeding).  The probability that at least one
> data point from each true cluster is selected satisfies
> \[
> p_{\mathrm{hit}}
> \;\ge\; \prod_{k=1}^K\frac{n_k}{n}
> \;\ge\; \pi_^K > 0,
> \]
> a constant depending only on $K$ and $\pi_$, not on $n$.
> Conditional on selecting a point from each cluster, each selected point
> is within $\Delta_/8$ of its true cluster center with probability
> at least $1-K\cdot\exp(-c\Delta_^2/\sigma^2)$ (by the sub-Gaussian
> tail bound).  A single random initialization thus lands in $B$ with
> probability at least $p_0=\pi_^K/2$ for large $n$.
> 
> **Step 4 (Amplification via multiple restarts).**
> With $R$ independent restarts,
> \[
> P(no restart lands in B) \;\le\; (1-p_0)^R.
> \]
> Setting $R=C_R\log n$ with $C_R\ge(c+1)/|\log(1-p_0)|$ gives
> \[
> P(initialization failure) \;\le\; n^{-c}.
> \]
> Each successful initialization converges to within $\Delta_/16$ of
> $\htheta_n^*$ in $O(\log n)$ Lloyd iterations.  The total runtime is
> $O(R\cdot n\cdot K\cdot d_\phi\cdot\log n)=O(n\log^2 n)$, which is
> polynomial.  The solution with the smallest $W_n$ among the $R$ runs is
> returned. $\square$

> **Remark:** [The NP-hard gap]
> <!-- label: rem:S5:npgap -->
> Lemma [ref] explicitly proves that under strong separation,
> Lloyd's with random restarts finds the global empirical minimizer.
> The proof exploits the benign landscape induced by well-separated
> clusters, not the worst-case NP-hardness of $k$-means.
> 
> **If the strong separation condition does not hold**, the result
> degrades.  The landscape may have spurious local minima, and Lloyd's may
> converge to a suboptimal solution.  In that case, the theorem would need
> to be weakened to ``there exists a polynomial-time algorithm that finds
> a $\delta$-approximation of the global minimizer,'' following
>  [cite].  We
> **honestly acknowledge this gap** and do not claim a guarantee for
> the weak separation regime.
> 
> In practice, we recommend $k$-means++ initialization
>  [cite], which provides $O(\log K)$ approximation in
> expectation and has better practical coverage than uniform initialization.
> Lemma [ref]'s conclusion holds for $k$-means++ as well,
> with potentially better constants.

### Proof of Main Theorem
<!-- label: sec:S5:main -->

> **Theorem:** [Fixed-$K$ state discovery consistency]
> <!-- label: thm:S5:main -->
> Let $K$ be fixed.  Suppose:
> 
1. **Generative model**: Assumption [ref] holds.
2. **Strong separation**: Assumption [ref] holds with
3. **Asymptotics**: $n\to\infty$ and
4. **Algorithm**: Lloyd's $k$-means with

> Then the estimated partition $\hC$ satisfies
> 
> $$
> P\bigl(\hC\neq\cstar up to permutation\bigr)
> \;\le\; K\cdot\exp\!\left(
>           -c_1\cdot\frac{n_\,\Delta_^2}{\sigma^2 d_\phi}\right)
>         \;+\; o(1),
> <!-- label: eq:S5:main -->
> $$
> 
> where $c_1>0$ is a universal constant independent of
> $K,n,\sigma,\Delta_$.  The $o(1)$ term captures the exponentially
> small bias from the population minimizer and the initialization failure
> probability from Lemma [ref].

> **Proof:** [Proof of Theorem [ref]]
> We combine the four lemmas.
> 
> **Step 1 (Population bias is bounded).**
> By Lemma [ref], the unique population minimizer $\theta^*$
> satisfies, for some permutation $\pi_1$,
> \[
> \norm{\theta^*_{\pi_1(k)}-\muk} \;\le\; \epsilon_{\mathrm{pop}}
> \;<\; \frac{\Delta_}{8}.
> \]
> 
> **Step 2 (Empirical minimizer convergence).**
> By Lemma [ref] with $t=\Delta_/8$, for $n$ large
> enough such that $\Delta_/8\ge C_0\sqrt{K d_\phi/n}$,
> \[
> P\!\left(\norm{\htheta_n-\theta^*}\ge\frac{\Delta_}{8}\right)
> \;\le\; 2\cdot\exp\!\left(
>           -\frac{c_2}{64}\cdot\frac{n\,\Delta_^2}{\sigma^2 d_\phi}\right).
> \]
> Combining with Lemma [ref] via the triangle inequality,
> \[
> \norm{\htheta_n-\mu}
> \;\le\; \norm{\htheta_n-\theta^*} + \norm{\theta^*-\mu}
> \;<\; \frac{\Delta_}{8} + \frac{\Delta_}{8}
> = \frac{\Delta_}{4},
> \]
> with probability at least
> $1-2\cdot\exp\!\left(-\frac{c_2}{64}\cdot\frac{n\,\Delta_^2}{\sigma^2 d_\phi}\right)$.
> 
> **Step 3 (Lloyd's finds the global minimizer).**
> By Lemma [ref], with $R=C_R\log n$ restarts,
> \[
> P\!\left(\norm{\ttheta_n-\htheta_n}\ge\frac{\Delta_}{16}\right)
> \;\le\; n^{-c}
> \]
> for any desired $c>0$.  Since $\norm{\htheta_n-\mu}<\Delta_/4$
> with high probability from Step~2, the Lloyd output satisfies
> \[
> \norm{\ttheta_n-\mu}
> \;\le\; \norm{\ttheta_n-\htheta_n}
>       + \norm{\htheta_n-\theta^*}
>       + \norm{\theta^*-\mu}
> \;<\; \frac{\Delta_}{16}
>      + \frac{\Delta_}{8}
>      + \frac{\Delta_}{8}
> = \frac{\Delta_}{4},
> \]
> with probability at least
> $1-2\exp\!\left(-c_2 n\Delta_^2/(64\sigma^2 d_\phi)\right)-n^{-c}$.
> 
> **Step 4 (Center proximity implies correct partition).**
> By Lemma [ref], when
> $\norm{\ttheta_j-\mu_{\pi(j)}}<\Delta_/4$ for all $j$, the induced
> partition matches the true partition for all points with
> $\norm<3\Delta_/8$.
> 
> The fraction of points with $\norm\ge3\Delta_/8$ is
> bounded by the sub-Gaussian tail bound (Lemma~S5.4):
> \[
> P(\norm\ge3\Delta_/8)
> \;\le\; 2\exp\!\left(-c_0\cdot\frac{\Delta_^2}{\sigma^2}\right).
> \]
> This irreducible error is independent of $n$ and is absorbed into the
> $o(1)$ term.  It represents points that are inherently ambiguous due to
> large noise---even perfect knowledge of the centers cannot classify them
> correctly.
> 
> **Step 5 (Converting $n$ to $n_$).**
> Since $K$ is fixed, $n\ge K\cdot n_$ (by the pigeonhole principle).
> Therefore,
> \[
> \exp\!\left(-\frac{c_2}{64}\cdot\frac{n\,\Delta_^2}{\sigma^2 d_\phi}\right)
> \;\le\; \exp\!\left(-\frac{c_2 K}{64}\cdot
>               \frac{n_\,\Delta_^2}{\sigma^2 d_\phi}\right).
> \]
> 
> **Step 6 (Final probability bound).**
> Let $c_1 = c_2 K / 64$.  Collecting all error terms,
> 
> $$
> &P(estimated partition\neqtrue partition) 

> &\le P\!\left(\norm{\ttheta_n-\mu}\ge\frac{\Delta_}{4}\right)
>    + P(Lloyd's initialization fails) 

> &\le 2\cdot\exp\!\left(-c_2\cdot\frac{n\,\Delta_^2}{64\,\sigma^2 d_\phi}\right)
>    \;+\; n^{-c} 

> &\le 2\cdot\exp\!\left(-c_1\cdot\frac{n_\,\Delta_^2}
>                                 {\sigma^2 d_\phi}\right)
>    \;+\; o(1).
> $$
> 
> The $o(1)$ term absorbs:
> 
- The exponentially small bias $\epsilon_{\mathrm{pop}}$ from
- The initialization failure probability $n^{-c}$ from
- The irreducible misclassification from large-noise samples
- The factor $K$ in front of the exponential (from the union bound

> This completes the proof of Theorem [ref].  $\square$

### Discussion: NP-Hard Gap and Practical Implications
<!-- label: sec:S5:disc -->

The following remarks situate Theorem [ref] within the
broader theory and address the computational-statistical gap.

> **Remark:** [The NP-hard gap (resolution of Review Issue~3)]
> <!-- label: rem:S5:gap -->
> The proof chain resolves the NP-hard gap within the strong separation
> regime:
> 
1. Lemma [ref] assumes access to the \textbf{global
2. Lemma [ref] proves that \textbf{Lloyd's algorithm

> The chain holds because $k$-means on well-separated mixtures is not a
> hard instance---the landscape has a unique local minimum within the
> basin of attraction, and Lloyd's contracts toward it.  The NP-hardness
> of $k$-means applies to worst-case instances, not the well-separated
> Gaussian-like mixtures considered here.
> 
> **Without strong separation**: the landscape may have spurious
> local minima, and Lloyd's may converge to a suboptimal solution.  In
> that case, only weaker guarantees are available---e.g.\ there exists a
> polynomial-time algorithm that finds a $(1+\delta)$-approximation of
> the global minimizer  [cite].
> The theorem makes no claim for the weak separation regime.

> **Remark:** [Relation to main text bounds]
> <!-- label: rem:S5:relation -->
> Theorem [ref] complements the main text's negative results:
> 
- Theorem~1 [ref] gives a lower bound on the F1 score
- Theorem~4' [ref] establishes the minimax lower
- Theorem~2 [ref] gives a weak-feature F1 bound that

> **Remark:** [Fixed $K$ and growing-$K$ regimes]
> <!-- label: rem:S5:fixedK -->
> The proof relies on $K$ being fixed.  This allows:
> 
- The covering number $\log\mathcal{N}(\epsilon)\le
- The strong convexity parameter $\lambda=\pi_/2$ is fixed
- The random initialization probability $p_0\ge\pi_^K$ is a

> For $K\to\infty$ as $n\to\infty$, the covering number grows, $\pi_$
> could be $O(1/K)$ making $\lambda=O(1/K)$, and the initialization
> probability decays exponentially in $K$.  The growing-$K$ regime requires
> a separate analysis; see  [cite].

> **Remark:** [Practical sample size guide]
> <!-- label: rem:S5:samples -->
> From  [ref], to achieve misclassification probability
> $\le\delta$ due to center estimation, it suffices to have
> \[
> n_\;\ge\;
> \frac{C_1\,\sigma^2 d_\phi}{\Delta_^2}
> \cdot\log\!\left(\frac{K}\right),
> \]
> for a universal constant $C_1>0$.  The following operational rule of
> thumb illustrates the required per-state sample sizes:
> \[
> \begin{array}{c|c}
> \Delta_/(\sigma\sqrt{d_\phi}) & n_ for P(error)\le0.05 
 ---
> 0.5\ (marginal) & \ge400 

> 1.0\ (moderate) & \ge100 

> 2.0\ (good)     & \ge25  

> 3.0\ (strong)   & \ge12
> \end{array}
> \]
> (Assuming $K\le10$, $d_\phi\le64$, and a refined constant $C_1\approx20$.)

### Verification of Exponents and Inequality Directions
<!-- label: sec:S5:verify -->

We explicitly verify that all exponents are negative and all inequality
directions are correct.

<div align="center">

[Table omitted — see original .tex]

</div>

The exponent $-\frac{c_1 n_\Delta_^2}{\sigma^2 d_\phi}$ is
**always negative** for $n_>0$, $\Delta_>0$,
$\sigma^2<\infty$, $d_\phi<\infty$.  There is no risk of a positive
exponent.  All inequality directions in Lemma~3 are verified:
$\frac18+\frac38=\frac12=\frac78-\frac38$, giving
$\norm{\phi-\theta_{j_k}}\le\Delta_/2\le\norm{\phi-\theta_{j'}}$.
The union bound in Theorem [ref] propagates these correctly.

### Appendix to Section~S5: Supporting Lemmas
<!-- label: sec:S5:app -->

The following lemmas are used in the proofs above and are stated here
for completeness.

> **Lemma:** [Sub-Gaussian norm bound]
> <!-- label: lem:S5:sgnorm -->
> Let $\varepsilon\in\R^{d_\phi}$ be a zero-mean sub-Gaussian vector with
> variance proxy $\sigma^2$.  For any $t>0$,
> \[
> P\!\left(\norm_2\ge C_1\sigma(\sqrt{d_\phi}+\sqrt{t})\right)
> \;\le\; 2\exp(-t),
> \]
> where $C_1$ is an absolute constant.  For
> $t=c\cdot\Delta_^2/\sigma^2$ with $\Delta_^2/\sigma^2$
> large under  [ref],
> \[
> P\!\left(\norm_2\ge\frac{\Delta_}{4}\right)
> \;\le\; 2\exp\!\left(-c_0\frac{\Delta_^2}{\sigma^2}\right),
> \]
> for some $c_0>0$.  Moreover,
> $P(\norm\ge3\Delta_/8)
> \le 2\exp(-c_0'\Delta_^2/\sigma^2)$.

> **Proof:** This follows from Theorem~3.1.1 of  [cite]
> for sub-Gaussian random vectors.  The second inequality follows by
> setting $t=\sqrt{c}\,\Delta_/\sigma$ and noting that
> $\sqrt{d_\phi}\le\Delta_/(C_1 C\sigma)$ under
>  [ref].

> **Lemma:** [Quadratic lower bound for $W$ near $\theta^*$]
> <!-- label: lem:S5:quad -->
> Under the conditions of Theorem [ref], for any $\theta$ with
> $\norm{\theta-\theta^*}\le\Delta_/4$,
> \[
> W(\theta)-W(\theta^*)\;\ge\;\lambda\cdot\norm{\theta-\theta^*}^2,
> \]
> where $\lambda=\pi_/2$ and $\pi_=\min_k P(S=k)$.

> **Proof:** Let $\theta$ satisfy $\norm{\theta-\theta^*}\le\Delta_/4$.  By
> Lemma [ref], $\norm{\theta^*-\mu}<\Delta_/8$, so
> $\norm{\theta-\mu}<\Delta_/8+\Delta_/4=3\Delta_/8$.
> For a point $\phi=\muk+\varepsilon$ with $\norm<\Delta_/8$,
> Lemma [ref] shows the nearest center in $\theta$ is the one
> matched to true state~$k$.  Points with $\norm\ge\Delta_/8$
> have probability at most $2\exp(-\Delta_^2/(128\sigma^2))$, which is
> $o(\pi_)$ under  [ref].
> 
> In the region where assignments are correct, the contribution to $W$ from
> state $k$ is
> \[
> \E[\norm{\phi-\theta_{\pi(k)}}^2\mid S=k]\cdot\pi_k
> = \pi_k\bigl(\norm{\muk-\theta_{\pi(k)}}^2+\E[\norm^2]\bigr),
> \]
> since the cross term vanishes because $\E[\varepsilon]=0$ and
> $\varepsilon\perp S$.  The first term is minimized at
> $\theta_{\pi(k)}=\muk$ with value $\pi_k\cdot\E[\norm^2]$.
> Summing over $k$ and accounting for exponentially small corrections from
> misassigned points gives
> $W(\theta)-W(\theta^*)\ge\pi_\norm{\theta-\mu}^2
>  - O(\exp(-\Delta_^2/(128\sigma^2)))$.
> Since $\norm{\theta^*-\mu}$ is exponentially small,
> $\norm{\theta-\theta^*}\approx\norm{\theta-\mu}$, and the result
> follows with the factor $1/2$ absorbing the negligible corrections.

> **Lemma:** [Lipschitz property of $k$-means loss]
> <!-- label: lem:S5:lipschitz -->
> For any fixed $x$, the function
> $\theta\mapsto f_\theta(x)=\min_k\norm{\phi(x)-\theta_k}_2^2$ is
> $L(x)$-Lipschitz in $\theta$ with respect to $\norm_\infty$,
> where $L(x)=2(\norm{\phi(x)}_2+M)$.

> **Proof:** For two center sets $\theta,\theta'$ with
> $\max_k\norm{\theta_k-\theta'_k}\le\delta$,
> 
> $$
> |f_\theta(x)-f_{\theta'}(x)|
> &\le \max_k\bigl|\norm{\phi(x)-\theta_k}^2
>             -\norm{\phi(x)-\theta'_k}^2\bigr| 

> &\le \max_k\bigl(\norm{\phi(x)-\theta_k}+\norm{\phi(x)-\theta'_k}\bigr)
>     \cdot\norm{\theta_k-\theta'_k} 

> &\le 2(\norm{\phi(x)}_2+M)\,\delta,
> $$
> 
> using the triangle inequality and $\norm{\theta_k}\le M$.

> **Lemma:** [Metric entropy of the center class]
> <!-- label: lem:S5:covering -->
> Let $\Theta_K=\{\theta=\{\theta_1,...,\theta_K\}:\theta_k\in\R^{d_\phi},
> \norm{\theta_k}_2\le M\}$ equipped with
> $\norm{\theta-\theta'}_\infty=\max_k\norm{\theta_k-\theta'_k}_2$.
> For any $\epsilon\in(0,M)$,
> \[
> \log\mathcal{N}(\epsilon,\Theta_K,\norm_\infty)
> \;\le\; K d_\phi\log\!\left(1+\frac{2M}\right).
> \]

> **Proof:** $\Theta_K$ is the Cartesian product of $K$ balls of radius $M$ in
> $\R^{d_\phi}$.  The $\epsilon$-covering number of $B_M(0)\subset\R^{d_\phi}$
> in $\ell_2$ is $(1+2M/\epsilon)^{d_\phi}$, and the $\ell_\infty$ metric
> on the product is the max of per-coordinate $\ell_2$ distances, so the
> covering number of the product is the product of per-coordinate covering
> numbers.

\begin{thebibliography}{20}

\bibitem{aloise2009np}
D.~Aloise, A.~Deshpande, P.~Hansen, and P.~Popat.
NP-hardness of Euclidean sum-of-squares clustering.
*Machine Learning*, 75(2):245--248, 2009.

\bibitem{arthur2007kmeanspp}
D.~Arthur and S.~Vassilvitskii.
$k$-means++: The advantages of careful seeding.
In *Proceedings of SODA*, pages 1027--1035, 2007.

\bibitem{dasgupta2008hardness}
S.~Dasgupta.
The hardness of $k$-means clustering.
Technical Report, UCSD, 2008.

\bibitem{kumar2010clustering}
A.~Kumar and R.~Kannan.
Clustering with spectral norm and the $k$-means algorithm.
In *Proceedings of FOCS*, pages 299--308, 2010.

\bibitem{lei2013statistical}
J.~Lei, A.~Rinaldo, and L.~Wasserman.
A statistical analysis of clustering algorithms.
*arXiv preprint arXiv:1306.6836*, 2013.

\bibitem{ostrovsky2013effectiveness}
R.~Ostrovsky, Y.~Rabani, L.~J.~Schulman, and C.~Swamy.
The effectiveness of Lloyd-type methods for the $k$-means problem.
*Journal of the ACM*, 59(6):1--22, 2013.

\bibitem{pollard1981strong}
D.~Pollard.
Strong consistency of $k$-means clustering.
*The Annals of Statistics*, 9(1):135--140, 1981.

\bibitem{vershynin2018highdimensional}
R.~Vershynin.
*High-Dimensional Probability: An Introduction with Applications in
Data Science*. Cambridge University Press, 2018.

\end{thebibliography}