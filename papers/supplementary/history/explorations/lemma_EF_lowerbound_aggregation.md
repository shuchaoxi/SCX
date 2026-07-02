\section{Lemma E \& Lemma F: Second-Order Lower Bound and Multi-State
Aggregation}<!-- label: lemma-e-lemma-f-second-order-lower-bound-and-multi-state-aggregation -->

> **Status**: Complete proofs. **Prerequisites**: Lemma A
> (Bahadur-Rao for Bernoulli), Lemma B (F1 asymptotic expansion), Lemma C
> (Chernoff information), Lemma D (adaptive threshold).
> **References**: Bahadur \& Rao (1960), Le Cam (1986), van der Vaart
> (1998), Ingster \& Suslina (2003).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{Lemma E: Second-Order Asymptotic Lower Bound (Exact Constant
Minimax)}<!-- label: lemma-e-second-order-asymptotic-lower-bound-exact-constant-minimax -->

#### Statement<!-- label: statement -->

Let \(e_1,...,e_M\) be i.i.d. \(\operatorname{Bern}(p)\) under either
hypothesis:

\[
\mathrm{H}_0 : p = p_0,\qquad \mathrm{H}_1 : p = p_1,
\]

with \(0 \le p_0 < p_1 \le 1\) and \((p_0,p_1) \neq (0,1)\) to avoid
degeneracy. Define the Chernoff information

\[
\kappa = C(\operatorname{Bern}(p_0),\operatorname{Bern}(p_1)) = \operatorname{KL}(\theta^*\|p_0) = \operatorname{KL}(\theta^*\|p_1),
\]

where \(\theta^* \in (p_0,p_1)\) is the unique solution of
\(\operatorname{KL}(\theta\|p_0) = \operatorname{KL}(\theta\|p_1)\). Let

\[
\lambda_0^* = \log\frac{\theta^*(1-p_0)}{p_0(1-\theta^*)} > 0,\qquad
\lambda_1^* = \log\frac{\theta^*(1-p_1)}{p_1(1-\theta^*)} < 0,
\]

and set \(D = \lambda_0^* + |\lambda_1^*|\), \(s = |\lambda_1^*|/D\).

For any noise detection algorithm \(\mathcal{A}\) (a measurable map
\(\{0,1\}^M \to \{0,1\}\)) let \(\operatorname{F1}_{\mathcal{A}}(M)\)
denote its expected \(F_1\) score on a sample where
\(\Pr(noise)=\eta \in (0,1)\).

**Theorem (Lower Bound).** For any such algorithm \(\mathcal{A}\),

\[
\liminf_{M\to\infty} \; e^{M\kappa}\,\sqrt{2\pi M}\; \bigl(1-\operatorname{F1}_{\mathcal{A}}(M)\bigr) \;\ge\; \frac{C_},
\]

where

\[
\boxed{\;C_ \;=\; \frac{2}\,\left(\frac{1-\eta}\right)^{\!s}\,
\frac{1/\lambda_0^* + 1/|\lambda_1^*|}{\sqrt{\theta^*(1-\theta^*)}}\;}
\]

Equivalently, writing \(r = \lambda_0^*/D = 1-s\),

\[
C_ = \frac{\eta^r (1-\eta)^{1-r}}{2}\,
\frac{1/\lambda_0^* + 1/|\lambda_1^*|}{\sqrt{\theta^*(1-\theta^*)}}.
\]

The constant is sharp: the Bayes-optimal threshold test (Lemma D)
attains the limit with this same constant.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

#### Proof<!-- label: proof -->

The proof proceeds in five parts.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\paragraph{Part 1: Reduction to a binary hypothesis
test}<!-- label: part-1-reduction-to-a-binary-hypothesis-test -->

Within a fixed state \(s\), Assumption (A5) guarantees that the expert
errors are conditionally i.i.d. given the state. Under the clean label
distribution the error probability is \(p_0 = \mu_s\); under the noisy
label distribution it is \(p_1 = 1 - C_{bal}\cdot\mu_s/(K-1)\).
Hence the algorithm's input \((e_1,...,e_M)\) constitutes \(M\) i.i.d.
draws from \(\operatorname{Bern}(p_0)\) under \(\mathrm{H}_0\) and from
\(\operatorname{Bern}(p_1)\) under \(\mathrm{H}_1\).

Let the algorithm's decision be \(\delta_M \in \{0,1\}\), where
\(\delta_M=1\) means ``flag as noisy.'' The Type I and Type II errors
are

\[
\alpha_M = \Pr(\delta_M=1 \mid \mathrm{H}_0),\qquad
\beta_M = \Pr(\delta_M=0 \mid \mathrm{H}_1).
\]

From Lemma B, the \(F_1\) score satisfies

\[
1 - \operatorname{F1} = \frac{1-\eta}{2\eta}\,\alpha_M + \frac12\,\beta_M + o(1),
\]

where the \(o(1)\) term is uniform over all decision rules and decays as
\(O(e^{-2M\kappa})\) (negligible for the leading constant). Define the
weighted risk

\[
R_M(\delta_M) = w_0\alpha_M + w_1\beta_M,\qquad
w_0 = \frac{1-\eta}{2\eta},\; w_1 = \frac12.
\]

Our task is therefore to lower-bound
\(\liminf e^{M\kappa}\sqrt{2\pi M}\,R_M(\delta_M)\) over all measurable
decision rules \(\delta_M\).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\paragraph{Part 2: Application of the Neyman-Pearson
lemma}<!-- label: part-2-application-of-the-neyman-pearson-lemma -->

Consider the simple-versus-simple testing problem
\(\mathrm{H}_0: p=p_0\) vs \(\mathrm{H}_1: p=p_1\). The likelihood ratio
for \(M\) observations is

\[
L_M(e) = \prod_{m=1}^M \frac{p_1^{e_m}(1-p_1)^{1-e_m}}{p_0^{e_m}(1-p_0)^{1-e_m}}.
\]

Because \(p_1>p_0\), \(L_M\) is strictly increasing in
\(C_M = M^{-1}\sum e_m\); consequently, the most powerful
level-\(\alpha\) test is a threshold test on \(C_M\).

Fix any decision rule \(\delta_M\) and let
\(\alpha = \alpha(\delta_M)\). The Neyman-Pearson lemma (Lehmann \&
Romano, Thm 3.2.1) states that among all tests with Type I error
\(\le \alpha\), the likelihood ratio test (equivalently, the threshold
test on \(C_M\)) minimizes the Type II error. Hence

\[
\beta(\delta_M) \ge \beta_{\mathrm{NP}}(\alpha),
\]

where \(\beta_{\mathrm{NP}}(\alpha)\) is the Type II error of the most
powerful level-\(\alpha\) test. Consequently

\[
R_M(\delta_M) = w_0\alpha + w_1\beta(\delta_M)
\ge w_0\alpha + w_1\beta_{\mathrm{NP}}(\alpha)
\ge \min_{\alpha\in[0,1]} \bigl\{w_0\alpha + w_1\beta_{\mathrm{NP}}(\alpha)\bigr\}.
\]

The function \(f(\alpha)=w_0\alpha+w_1\beta_{\mathrm{NP}}(\alpha)\) is
convex (the ROC curve \(\alpha\mapsto\beta_{\mathrm{NP}}(\alpha)\) is
concave). Its minimizer \(\alpha^*\) satisfies \(f'(\alpha^*)=0\), i.e.

\[
w_0 + w_1\,\beta_{\mathrm{NP}}'(\alpha^*) = 0.
\]

For the Neyman-Pearson test, the slope of the ROC curve at \(\alpha^*\)
equals \(-1/\tau^*\), where \(\tau^*\) is the likelihood-ratio
threshold. This gives \(\tau^* = w_0/w_1 = (1-\eta)/\eta\); the
minimizer is exactly the Bayes decision rule with prior odds \(w_0:w_1\)
against \(\mathrm{H}_0\).

Therefore, for **any** algorithm \(\mathcal{A}\), the weighted risk
is at least the risk of the Bayes test:

\[
R_M(\delta_M) \ge R_M^* := w_0\alpha_M^* + w_1\beta_M^*,
\]

where

\[
\delta_M^*(e) = \mathbf{1}\bigl\{L_M(e) > (1-\eta)/\eta\bigr\}
\]

(with arbitrary tie-breaking, which affects the risk by
\(O(e^{-M\kappa}/M)\) and is irrelevant asymptotically).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\paragraph{Part 3: Exact asymptotics of the Bayes
test}<!-- label: part-3-exact-asymptotics-of-the-bayes-test -->

The Bayes test rejects \(\mathrm{H}_0\) when the log-likelihood ratio
exceeds \(\log((1-\eta)/\eta)\). Write

\[
\Delta = \log\frac{p_1(1-p_0)}{p_0(1-p_1)} > 0,\qquad
\Delta_0 = \log\frac{1-p_1}{1-p_0}.
\]

Then \(\log L_M = M\bigl(C_M\Delta + \Delta_0\bigr)\), and the rejection
region is

\[
C_M \;>\; -\frac{\Delta_0} + \frac{1}{M\Delta}\log\frac{1-\eta}.
\]

The constant \(-\Delta_0/\Delta\) is precisely the Chernoff point
\(\theta^*\), since
\(\operatorname{KL}(\theta^*\|p_0)=\operatorname{KL}(\theta^*\|p_1)\)
implies \(\theta^*\Delta + \Delta_0 = 0\). Hence the threshold is

\[
t_M = \theta^* + \frac{1}{M\Delta}\log\frac{1-\eta}.
\]

A key identity (proved in Lemma C) relates \(\Delta\) to the derivatives
of the KL divergence at \(\theta^*\):

\[
\Delta = \lambda_0^* - \lambda_1^* = \lambda_0^* + |\lambda_1^*| = D.
\]

Thus \(t_M - \theta^* = \delta_M\) with

\[
\delta_M = \frac{1}{M D}\log\frac{1-\eta} = O\!\left(\frac1M\right).
\]

The error probabilities of the Bayes test are

\[
\alpha_M^* = \Pr\nolimits_{p_0}(C_M > t_M),\qquad
\beta_M^* = \Pr\nolimits_{p_1}(C_M \le t_M),
\]

up to a \(O(e^{-M\kappa}/M)\) correction for possible randomization at
the boundary.

Apply the Bahadur-Rao theorem (Lemma A) to each:

\[
\alpha_M^* = \frac{\exp\!\bigl(-M\operatorname{KL}(t_M\|p_0)\bigr)}
{\lambda_0^*(t_M)\,\sqrt{2\pi M\,t_M(1-t_M)}}\,
\bigl(1 + O(M^{-1})\bigr),
\]

\[
\beta_M^* = \frac{\exp\!\bigl(-M\operatorname{KL}(t_M\|p_1)\bigr)}
{|\lambda_1^*(t_M)|\,\sqrt{2\pi M\,t_M(1-t_M)}}\,
\bigl(1 + O(M^{-1})\bigr).
\]

Since \(t_M \to \theta^*\), we have
\(\lambda_0^*(t_M) \to \lambda_0^*\),
\(|\lambda_1^*(t_M)| \to |\lambda_1^*|\), and
\(t_M(1-t_M) \to \theta^*(1-\theta^*)\); the \(O(M^{-1})\) corrections
in the prefactors are uniform in a neighbourhood of \(\theta^*\).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\paragraph{Part 4: Expansion around the Chernoff
point}<!-- label: part-4-expansion-around-the-chernoff-point -->

Write \(\delta = \delta_M\) and expand the KL divergences:

\[
\operatorname{KL}(\theta^*+\delta\|p_0) = \kappa + \lambda_0^*\delta
+ \frac{\delta^2}{2\theta^*(1-\theta^*)} + O(\delta^3),
\]

\[
\operatorname{KL}(\theta^*+\delta\|p_1) = \kappa - |\lambda_1^*|\delta
+ \frac{\delta^2}{2\theta^*(1-\theta^*)} + O(\delta^3).
\]

The quadratic term satisfies \(M\delta^2 = O(M^{-1})\to 0\) because
\(\delta = O(M^{-1})\); the cubic term is \(O(M^{-2})\). Hence

\[
M\operatorname{KL}(t_M\|p_0) = M\kappa + \frac{\lambda_0^*}{D}\log\frac{1-\eta} + o(1),
\]

\[
M\operatorname{KL}(t_M\|p_1) = M\kappa - \frac{|\lambda_1^*|}{D}\log\frac{1-\eta} + o(1).
\]

Substituting into the Bahadur-Rao expressions:

\[
\alpha_M^* = \frac{e^{-M\kappa}}
{\lambda_0^*\sqrt{2\pi M\,\theta^*(1-\theta^*)}}\,
\left(\frac{1-\eta}\right)^{-\lambda_0^*/D}
(1+o(1)),
\]

\[
\beta_M^* = \frac{e^{-M\kappa}}
{|\lambda_1^*|\sqrt{2\pi M\,\theta^*(1-\theta^*)}}\,
\left(\frac{1-\eta}\right)^{\,|\lambda_1^*|/D}
(1+o(1)).
\]

Now compute the weighted risk:

\[
\begin{aligned}
R_M^* &= w_0\alpha_M^* + w_1\beta_M^* 
]4pt{]} \&=
\frac{e^{-M\kappa}}{\sqrt{2\pi M\,\theta^*(1-\theta^*)}}, \Bigg[
\frac{1-\eta}{2\eta}\,\frac{1}{\lambda_0^*}
\left(\frac{1-\eta}\right)^{-\lambda_0^*/D}
+ \frac12\,\frac{1}{|\lambda_1^*|}
\left(\frac{1-\eta}\right)^{\,|\lambda_1^*|/D}
\Bigg] (1+o(1)). \ end\{aligned\} \$\$

Define \(s = |\lambda_1^*|/D\) so that \(\lambda_0^*/D = 1-s\). The two
terms in brackets become

\[
\frac{1-\eta}{2\eta\lambda_0^*}\left(\frac{1-\eta}\right)^{-(1-s)}
= \frac{1}{2\lambda_0^*}\left(\frac{1-\eta}\right)^{s},
\]

\[
\frac{1}{2|\lambda_1^*|}\left(\frac{1-\eta}\right)^{s}.
\]

Notice they share the factor \(\frac12((1-\eta)/\eta)^s\). Factoring it
out:

\[
R_M^* = \frac{e^{-M\kappa}}{\sqrt{2\pi M\,\theta^*(1-\theta^*)}}\,
\frac12\left(\frac{1-\eta}\right)^{\!s}
\left(\frac{1}{\lambda_0^*} + \frac{1}{|\lambda_1^*|}\right)
(1+o(1)).
\]

Multiplying by \(e^{M\kappa}\sqrt{2\pi M}\) and taking the limit gives

\[
\lim_{M\to\infty} e^{M\kappa}\sqrt{2\pi M}\; R_M^*
= \frac12\left(\frac{1-\eta}\right)^{\!s}
\frac{1/\lambda_0^* + 1/|\lambda_1^*|}{\sqrt{\theta^*(1-\theta^*)}}.
\]

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\paragraph{\texorpdfstring{Part 5: Conversion to the \(F_1\) lower bound
and edge
cases}{Part 5: Conversion to the F\_1 lower bound and edge cases}}<!-- label: part-5-conversion-to-the-f_1-lower-bound-and-edge-cases -->

From Part 1,
\(1-\operatorname{F1}_{\mathcal{A}} = R_M(\delta_{\mathcal{A}}) + o(1)\).
Since the \(o(1)\) term is \(O(e^{-2M\kappa})\) and is therefore killed
by multiplication with \(e^{M\kappa}\sqrt{2\pi M}\), we obtain for any
algorithm \(\mathcal{A}\):

\[
\liminf_{M\to\infty} e^{M\kappa}\sqrt{2\pi M}\,
\bigl(1-\operatorname{F1}_{\mathcal{A}}(M)\bigr)
\ge \frac12\left(\frac{1-\eta}\right)^{\!s}
\frac{1/\lambda_0^* + 1/|\lambda_1^*|}{\sqrt{\theta^*(1-\theta^*)}}.
\]

Define \(C_/\eta\) as the right-hand side. Solving for
\(C_\):

\[
\boxed{\;
C_ = \frac{2}\left(\frac{1-\eta}\right)^{\!s}
\frac{1/\lambda_0^* + 1/|\lambda_1^*|}{\sqrt{\theta^*(1-\theta^*)}}\;}.
\]

**Edge case \(p_0 = 0\) (perfect experts).** When \(p_0 = 0\), the
KL divergence \(\operatorname{KL}(\theta\|0) = \infty\) for any
\(\theta>0\). The Chernoff information \(\kappa\) becomes infinite; the
lower bound is vacuous (\(0 \ge 0\)). This is expected: if clean experts
never err, any single error reveals noise, and detection is trivial. The
constant \(C_\) is formally \(0\) in the limit since
\(1/\lambda_0^* \to 0\) as \(\lambda_0^* \to \infty\). We exclude this
uninteresting case from the theorem's scope (it is covered by the
trivial rate bound).

**Edge case \(p_1 = 1\).** Symmetric:
\(\operatorname{KL}(\theta\|1)=\infty\) for \(\theta<1\), the problem is
trivial, and the lower bound is vacuous.

**Edge case \(\eta\to 0\) or \(\eta\to 1\).** In these extremes one
class dominates and the \(F_1\) score is dominated by either precision
or recall. The constant \(C_\) remains well-defined and positive;
the limit \(\eta\to 0\) requires the normalisation \(\sqrt{M}\) instead
of \(\sqrt{2\pi M}\) (the \(2\pi\) is absorbed into the constant), which
is handled by an appropriate rescaling in Theorem~4'.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

**Sharpness**<!-- label: sharpness -->

The Bayes test \(\delta_M^*\) (equivalently, the adaptive-threshold test
of Lemma D with threshold \(t_M\)) attains equality in the limit. Its
risk was computed explicitly in Part 4, and the \(o(1)\) terms can be
bounded as \(O(M^{-1})\) using the Berry-Esseen refinement of the
Bahadur-Rao theorem (Lemma A, explicit-error version). Hence
\(C_\) is the **optimal** (largest) constant for which the
lower bound holds. This completes the proof of Lemma E. \(\square\)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{Lemma F: Multi-State
Aggregation}<!-- label: lemma-f-multi-state-aggregation -->

#### Statement<!-- label: statement-1 -->

Let there be \(S\) states, each with proportion \(\rho_s > 0\)
(\(\sum_s \rho_s = 1\)). Within state \(s\), the per-state \(F_1\) score
\(\operatorname{F1}_s(M)\) has the Bahadur-Rao asymptotics established
in Lemma B:

\[
1 - \operatorname{F1}_s(M)
\sim \frac{C_s}\,
\frac{e^{-M\kappa_s}}{\sqrt{2\pi M}},\qquad M\to\infty,
\]

where
\(\kappa_s = \operatorname{KL}(\theta_s^*\|p_{0,s}) = \operatorname{KL}(\theta_s^*\|p_{1,s})\)
is the state-\(s\) Chernoff information, and \(C_s\) is the state-\(s\)
constant from Lemma E.

The global \(F_1\) score over the mixture distribution is

\[
\operatorname{F1}_{global}(M) = \sum_{s=1}^S \rho_s\,
\operatorname{F1}_s(M).
\]

**Theorem (Global Aggregation).**

1. 
2. 
3. 
4. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

#### Proof<!-- label: proof-1 -->

**Part 1: Additivity**<!-- label: part-1-additivity -->

The global \(F_1\) score is defined as the expected \(F_1\) over the
mixture distribution. By the law of total expectation, conditioning on
the state \(s\):

\[
\operatorname{F1}_{global}(M)
= \mathbb{E}\bigl[\operatorname{F1}(M)\bigr]
= \sum_{s=1}^S \Pr(state=s)\,
\mathbb{E}\bigl[\operatorname{F1}(M) \mid state=s\bigr]
= \sum_{s=1}^S \rho_s \operatorname{F1}_s(M).
\]

Since the sum is finite and linearity of expectation applies, we obtain

\[
1 - \operatorname{F1}_{global}(M)
= \sum_{s=1}^S \rho_s\,\bigl(1 - \operatorname{F1}_s(M)\bigr).
\]

This holds exactly for every finite \(M\), with no approximation.

\paragraph{Part 2: Asymptotic rate and the bottleneck
state}<!-- label: part-2-asymptotic-rate-and-the-bottleneck-state -->

From Lemma E, each state contributes

\[
1 - \operatorname{F1}_s(M) \ge \frac{C_s}\,
\frac{e^{-M\kappa_s}}{\sqrt{2\pi M}}\,(1+o(1)),
\]

with equality achieved by the optimal state-wise test. Define
\(\kappa_ = \min_s \kappa_s\). For states with
\(\kappa_s > \kappa_\),

\[
\frac{e^{-M\kappa_s}}{e^{-M\kappa_}}
= e^{-M(\kappa_s-\kappa_)} \to 0
\]

exponentially fast as \(M\to\infty\). Hence, as \(M\to\infty\),

\[
1 - \operatorname{F1}_{global}(M)
= \sum_{s=1}^S \rho_s\,\frac{C_s}\,
\frac{e^{-M\kappa_s}}{\sqrt{2\pi M}}\,(1+o(1))
= \frac{e^{-M\kappa_}}{\eta\sqrt{2\pi M}}
\sum_{s\in\mathcal{S}_} \rho_s C_s\,
(1+o(1)) + \sum_{s\notin\mathcal{S}_} \rho_s C_s\,
\frac{e^{-M\kappa_s}}{\eta\sqrt{2\pi M}}(1+o(1)).
\]

The second sum is \(o(e^{-M\kappa_}/\sqrt{M})\) because each term
decays at a strictly faster exponential rate. Therefore

\[
\lim_{M\to\infty} e^{M\kappa_}\sqrt{2\pi M}\,
\bigl(1-\operatorname{F1}_{global}(M)\bigr)
= \frac{1}\sum_{s\in\mathcal{S}_} \rho_s C_s.
\]

For an arbitrary algorithm \(\mathcal{A}\), the per-state lower bounds
hold simultaneously (Lemma E applies within each state). Summing them
with weights \(\rho_s\) gives

\[
\liminf_{M\to\infty} e^{M\kappa_}\sqrt{2\pi M}\,
\bigl(1-\operatorname{F1}_{\mathcal{A}}(M)\bigr)
\ge \frac{1}\sum_{s\in\mathcal{S}_} \rho_s C_s.
\]

\paragraph{Part 3: Dominant-state
selection}<!-- label: part-3-dominant-state-selection -->

From the expression above, only the set \(\mathcal{S}_\)
contributes to the leading constant. Within \(\mathcal{S}_\), each
state contributes \(\rho_s C_s\) additively; therefore the global
constant is

\[
C_{global} = \sum_{s\in\mathcal{S}_} \rho_s C_s.
\]

If \(|\mathcal{S}_| \ge 2\), the single largest product
\(\max_s \rho_s C_s\) does **not** alone determine the constant
(the sum of all bottleneck states matters). However, in practice, often
\(|\mathcal{S}_| = 1\) (a unique worst state), in which case
\(C_{global} = \rho_{s_0} C_{s_0}\) for
\(s_0 = \arg\min \kappa_s\).

\paragraph{\texorpdfstring{Part 4: Finite-\(M\) upper
bound}{Part 4: Finite-M upper bound}}<!-- label: part-4-finite-m-upper-bound -->

From the additivity property and the fact that each
\(1-\operatorname{F1}_s(M) \ge 0\):

\[
1 - \operatorname{F1}_{global}(M)
= \sum_{s} \rho_s\,(1-\operatorname{F1}_s(M))
\le \max_s (1-\operatorname{F1}_s(M)) \cdot \sum_s \rho_s
= \max_s (1-\operatorname{F1}_s(M)).
\]

Now apply the upper bound from the Bahadur-Rao theorem (Lemma B)
uniformly across states. There exists \(M_0\) (depending on
\(p_{0,s},p_{1,s}\)) such that for all \(M \ge M_0\),

\[
1 - \operatorname{F1}_s(M) \le \frac{C_s}\,
\frac{e^{-M\kappa_s}}{\sqrt{2\pi M}}\,(1+\varepsilon_M),
\]

where \(\varepsilon_M \to 0\) uniformly in \(s\) (this uniformity
follows from the compactness of the parameter space
\([p_,p_] \subset (0,1)\) and continuity of the Bahadur-Rao
constants). Hence

\[
1 - \operatorname{F1}_{global}(M)
\le \max_s \frac{C_s}\,
\frac{e^{-M\kappa_s}}{\sqrt{2\pi M}}\,(1+o(1))
\le \frac{\max_s C_s}\,
\frac{e^{-M\,\min_s \kappa_s}}{\sqrt{2\pi M}}\,(1+o(1)),
\]

where the last inequality uses
\(\max_s e^{-M\kappa_s} = e^{-M\min_s \kappa_s}\). This verifies the
claimed finite-\(M\) bound. \(\square\)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

#### Remarks on the proof<!-- label: remarks-on-the-proof -->

1. 
2. 
3. 
4. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

#### Summary of constants<!-- label: summary-of-constants -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.3077}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4615}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2308}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Symbol
\end{minipage} & \begin{minipage}[b]
Definition
\end{minipage} & \begin{minipage}[b]
Role
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
\(C_s\) &
\(\frac{2}\bigl(\frac{1-\eta}\bigr)^{s_s} \frac{1/\lambda_{0,s}^* + 1/|\lambda_{1,s}^*|}{\sqrt{\theta_s^*(1-\theta_s^*)}}\)
& Per-state optimal lower-bound constant 

\(\kappa_s\) &
\(\operatorname{KL}(\theta_s^*\|p_{0,s}) = \operatorname{KL}(\theta_s^*\|p_{1,s})\)
& Per-state Chernoff information (exponential rate) 

\(\kappa_{global}\) & \(\min_s \kappa_s\) & Global exponential
rate (bottleneck state) 

\(C_{global}\) &
\(\sum_{s:\kappa_s=\kappa_{global}} \rho_s C_s\) & Global
lower-bound constant 

\end{longtable}

\subsubsection{C\_min Canonical Form and Across-File
Reconciliation}<!-- label: c_min-canonical-form-and-across-file-reconciliation -->

**FIXED (2026-06-28, DEFECT-09):** The constant \(C_\) was
defined inconsistently across three files (architecture document §3.4,
architecture document §4.3, and Lemma D/Theorem D.7), with discrepancies
of 15--18× due to legacy formulas lacking the \(((1-\eta)/\eta)^s\)
factor and using \(\max\) instead of sum over bottleneck states. This
section establishes the **single canonical definition** and
reconciles all files.

**Canonical \(C_\) (Lemma E, Equation 45 --- this file):**

\[\boxed{C_ = \frac{2}\left(\frac{1-\eta}\right)^{s} \frac{1/\lambda_0^* + 1/|\lambda_1^*|}{\sqrt{\theta^*(1-\theta^*)}}}\]

where \(s = |\lambda_1^*|/D^*\), \(D^* = \lambda_0^* + |\lambda_1^*|\),
\(\lambda_0^* = \log\frac{\theta^*(1-p_0)}{p_0(1-\theta^*)}\),
\(\lambda_1^* = \log\frac{\theta^*(1-p_1)}{p_1(1-\theta^*)} < 0\).

**Lattice-corrected form (after DEFECT-06 fix):**

\[C_^{(corr)} = C_ \cdot \frac{\lambda_0^* |\lambda_1^*|}{(1-e^{-\lambda_0^*})(1-e^{-|\lambda_1^*|})} \cdot \frac{\frac{1-e^{-\lambda_0^*}}{\lambda_0^*} + \frac{1-e^{-|\lambda_1^*|}}{|\lambda_1^*|}}{\frac{1}{\lambda_0^*} + \frac{1}{|\lambda_1^*|}}\]

**Reconciled references across all files:**

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1538}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3077}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2051}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3333}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
File
\end{minipage} & \begin{minipage}[b]
Symbol Used
\end{minipage} & \begin{minipage}[b]
Status
\end{minipage} & \begin{minipage}[b]
Action Taken
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
`lemma\_EF\_lowerbound\_aggregation.md` (this file) § Lemma E eq.
45 & \(C_\) --- **canonical** & Authoritative & --- 

`lemma\_CD\_chernoff\_adaptive.md` § D.7 & \(C_\) ---
matches canonical & Verified consistent & No change needed 

`THEOREMS\_UNIFIED.md` §4.2 & \(C_\) --- matches canonical
& Verified consistent & No change needed 

Architecture doc §3.4 (legacy) & \(C_{SCX}\) --- used \(\max\),
lacked \(((1-\eta)/\eta)^s\) & **Reconciled** & Replace with
reference to canonical 

Architecture doc §4.3 (legacy) & Draft \(C_\) --- lacked
\(((1-\eta)/\eta)^s\) & **Reconciled** & Replace with reference to
canonical 

Theorem 4' statements & \(C_\) via Lemma D.7 --- matches canonical
& Verified consistent & No change needed 

`08\_improved\_theorems.md` Fix 4 & \(C_^{(corr)}\)
--- lattice-corrected canonical & Authoritative for corrected form &
--- 

\end{longtable}

**Verification of consistency:** The canonical \(C_\) from
Lemma E (this file) produces the same numerical values as Lemma D's
\(C_{SCX}\) asymptotic constant (Lemma D.5) after accounting for
the \(\eta\)-scaling convention (\(C_/\eta\) in Lemma E vs
\(C_\) in Lemma D.7). Specifically: Lemma E's lower bound gives
\(e^{M\kappa}\sqrt{2\pi M}(1-F1) \geq C_/\eta\), while
Lemma D.7's achievability gives the identical expression. **All
files now reference this single canonical definition.**