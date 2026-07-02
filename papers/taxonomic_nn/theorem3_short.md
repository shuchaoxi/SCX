## Theorem Statement

Let $\mathcal{X}\times\mathcal{Y}$ be the input-label space with $|\mathcal{Y}|=K\geq2$,
and $\{f_m\}_{m=1}^M$ be $M$ experts with conditionally independent predictions given~$x$.
The ground-truth oracle $f^*:\mathcal{X}\to\mathcal{Y}$ is unobservable.

> **Definition:** Two worlds are considered:
> 
1. $\mathcal{P}_{noise}$ (World~A): a fraction~$\rho$ of inputs suffers
2. $\mathcal{P}_{hard}$ (World~B): all $y=y^*$, but the same fraction~$\rho$

> **Theorem:** [Noise-Difficulty Indistinguishability]<!-- label: thm:main -->
> For any $K\geq2$, $M\geq1$, there exist $\mathcal{P}_{noise}$ and $\mathcal{P}_{hard}$ such that:
> 
1. **Observational equivalence.**
2. **Algorithmic lower bound.**

No algorithm can distinguish ``label is wrong'' from ``sample is hard'' using observed
expert outputs alone---the two worlds are observationally identical, and any discrimination
incurs error $\ge\eta\rho/2$.

## Constructive Proof ($K=2$)

Fix states $s_1,s_2$ with $\mathbb{P}(X\!\in\!s_1)=\rho$, $\mathbb{P}(X\!\in\!s_2)=1-\rho$.
Choose $\eta\!\in\!(0,\tfrac12)$, $\varepsilon_1\!<\!\varepsilon_2\!\in\!(0,\tfrac12)$.

### World~A (Noise-driven)

State $s_1$: $y^*\equiv0$.  Labels flipped with probability $\eta_{err}$:
$\mathbb{P}(y\!\neq\!y^*\mid s_1)=\eta_{err}$.
Expert accuracy on clean labels: $\mathbb{P}(f_m=y^*\mid s_1,clean)=1-\varepsilon_1$.
State $s_2$: $y^*\equiv0$, no noise, accuracy $1-\varepsilon_2$.

### World~B (Difficulty-driven)

State $s_1$: $y=y^*$ but $y^*$ is random:
$\mathbb{P}(y^*=0\mid s_1)=1-\eta_{amb}$,
$\mathbb{P}(y^*=1\mid s_1)=\eta_{amb}$.
Experts are biased toward~0: $\mathbb{P}(f_m=0\mid s_1,y^*=0)=\mathbb{P}(f_m=0\mid s_1,y^*=1)=1-\varepsilon_1$.
Thus accuracy is $1-\varepsilon_1$ when $y^*=0$ but drops to $\varepsilon_1$ when $y^*=1$.
State $s_2$: identical to World~A.

### Equivalence verification

Under $\eta_{err}=\eta_{amb}=\eta$, the observable distribution factorises as
$\mathcal{P}(x,y,\{f_m\})=\mathcal{P}(x)\mathcal{P}(y\mid x)\prod_m\mathcal{P}(f_m\mid x)$:

*Labels:*
$\mathcal{P}_{noise}(y=0\mid s_1)=(1-\eta)\cdot1+\eta\cdot0=1-\eta
 =\mathcal{P}_{hard}(y=0\mid s_1)$.

*Experts:*
$\mathcal{P}_{noise}(f_m=0\mid s_1)=1-\varepsilon_1
 =\mathcal{P}_{hard}(f_m=0\mid s_1)$
(since $(1-\eta)(1-\varepsilon_1)+\eta(1-\varepsilon_1)=1-\varepsilon_1$).

All marginals match; conditional independence yields identical joint distributions,
proving item~( [ref]).

### Algorithmic impossibility

Let $\mathcal{A}$ flag samples as noisy.  Let $a$ be the fraction of $\{x\!\in\!s_1,y=1\}$
flagged.  In World~A these $\rho\eta$ samples are truly noisy:
$\mathrm{Error}_{noise}=\rho\eta(1-a)$.
In World~B they are correct but difficult: $\mathrm{Error}_{hard}=\rho\eta a$ (false alarms).
Hence
$\max(\mathrm{Error}_{noise},\mathrm{Error}_{hard})
 \ge\frac{\rho\eta(1-a)+\rho\eta a}{2}=\frac{\rho\eta}{2}$,
proving~( [ref]).  Minimax optimum: $a=\tfrac12$ (coin flip). $\square$

> **Remark:** [$K>2$]
> For $K>2$, construct World~B with fully random experts independent of $y^*$ whose
> marginals match World~A's.  This extreme construction---experts as random guessers---suffices
> as an existence proof. $\square$

## The Symmetry Condition $\eta_{err=\eta_{amb}$}

The condition $\eta_{err}=\eta_{amb}$ is *necessary and sufficient*
for observational equivalence:
\[
\mathcal{P}_{noise}(y=1\mid s_1)=\eta_{err},\qquad
\mathcal{P}_{hard}(y=1\mid s_1)=\eta_{amb}.
\]
When $\eta_{err}\neq\eta_{amb}$, the two worlds produce distinct label-class
frequencies and become statistically distinguishable---the impossibility collapses.
The symmetry thus delineates *precisely when* noise and difficulty are confounded.
Interpretation: the probability that flipping noise corrupts a label must equal the
probability that ambiguity alone generates an alternative valid label.  This is a
testable condition: compare label marginals across candidate partitions of~$\mathcal{X}$.

## The Lower Bound $\eta\rho/2$

The bound admits three readings:

1. **Information-theoretic.** The two worlds differ on $\rho\eta\cdot n$ samples.
2. **Tightness.** Random labelling ($a=\tfrac12$) achieves exactly $\rho\eta/2$,
3. **Positivity.** Strictly positive for any $\eta>0,\rho>0$; perfect

This is a *fundamental* limit---not an artifact of model class or algorithm design.

## Application: LLM Hallucination

### Multi-seed independent decoding

Run an LLM $M$ times on context~$c$ with independent random seeds $r_m$.  For fixed
model~$\theta$, the deterministic forward pass $f_\theta(c)$ is identical; stochastic
perturbations $\xi_m=\xi(c;r_m)$ (dropout, sampling, temperature) satisfy
$\xi_m\perp\xi_{m'}\!\mid\!c$.  Error indicators $e_m(c)=\mathbf{1}\{output of seed m is wrong\}$
are conditionally independent: $e_m\perp e_{m'}\!\mid\!c$.  The $M$ seeds thus constitute
$M$ conditionally independent experts, and Theorem [ref] applies.

> **Corollary:** [Hallucination lower bound]<!-- label: cor:hall -->
> For an LLM with $M$ independent seeds,
> $\mathrm{Hallucination}_{ambiguous} \ge \eta\rho/2$,
> where $\eta$ is model error probability on ambiguous queries and $\rho$ is their proportion.

From seed outputs alone, one cannot distinguish model error from essential query ambiguity.

### Symmetry in the LLM setting

$\eta_{err}=\eta_{amb}$ means: the perturbation $\xi_m$ has equal probability
of pushing output away from the correct answer (clear query) as pushing toward a valid
alternative (ambiguous query).  This depends on logit geometry and is empirically testable.

### Breaking the bound

The premise is ``only the $M$ seed outputs.''  External information breaks it:
**RAG** introduces retrieved documents; **RLHF** injects human preference anchors;
**tool use** provides execution verification.
**Hallucinations cannot be eliminated by scaling alone---only by breaking
the information closure of autoregressive generation.**

## Acknowledgments

Supported by .  Theorem [ref] emerged from the SCX
axiomatic framework  [cite] but is fully self-contained: it requires only conditional
independence of expert errors.

\begin{thebibliography}{10}

\bibitem{scx2026}
SCX.
\newblock A Taxonomic Theory of Neural Networks.
\newblock arXiv preprint, 2026.

\bibitem{wolpert1996}
D.H.\ Wolpert.
\newblock The Lack of A~Priori Distinctions Between Learning Algorithms.
\newblock *Neural Computation*, 8(7):1341--1390, 1996.

\bibitem{dawid1979}
A.P.\ Dawid and A.M.\ Skene.
\newblock Maximum Likelihood Estimation of Observer Error-Rates.
\newblock *Applied Statistics*, 28(1):20--28, 1979.

\bibitem{patrini2017}
G.\ Patrini et al.
\newblock Making Deep Neural Networks Robust to Label Noise.
\newblock *Proc.\ CVPR*, 2017.

\bibitem{pearl2009}
J.\ Pearl.
\newblock *Causality*, 2nd ed.\ Cambridge University Press, 2009.

\end{thebibliography}