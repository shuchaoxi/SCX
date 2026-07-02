# Theorem 3: The Honest Person Theorem (The Honest Person Theorem)

**Author:** SCX

## Theorem 3: The Honest Person Theorem (The Honest Person Theorem)
<!-- label: sec:thm3 -->

### Statement and Implications
<!-- label: sec:thm3_statement -->

The central discovery of this paper is that distinguishing label noise from
intrinsic sample difficulty is mathematically impossible from observational data
alone.  Theorem~3 formalizes this impossibility.

> **Theorem:** [The Honest Person Theorem (The Honest Person Theorem)]
>   <!-- label: thm:unidentifiability -->
>   For any $K \ge 2$ classification problem, any $M \ge 1$ experts, and any finite
>   state space~$\mathcal{S}$, there exist two data-generating processes
>   $\mathcal{P}_{noise}$ and $\mathcal{P}_{hard}$ such that:
>   
1. Under $\mathcal{P}_{noise}$, label errors are caused by
2. Under $\mathcal{P}_{hard}$, all observed labels equal the true
3. The two processes produce identical observable joint distributions
4. Consequently, for any algorithm $\mathcal{A}$ that maps $n$ i.i.d.\

> **Remark:** Theorem~3 asserts that the two statements ``this sample's label is wrong''
>   and ``this sample is so difficult that experts systematically err on it'' are
>   observationally equivalent.  The SCX framework must introduce assumptions
>   (A1)--(A6) to break this equivalence; Theorem~3 shows that these assumptions
>   are not arbitrary technical conditions but rather the minimal structure
>   required for identifiability.  See \S [ref] for the minimal
>   sufficient set.

### Proof for $K=2$ (Binary Classification)
<!-- label: sec:thm3_proof_K2 -->

We prove Theorem~3 by explicit construction.  Fix $K=2$, label space
$\mathcal{Y}=\{0,1\}$, $M\ge 1$ experts, and two states $s_1,s_2\in\mathcal{S}$.
Let $\rho\in(0,1)$ and $\eta\in(0,\tfrac12)$ be parameters to be specified.

#### World A: Noise-Driven Construction
<!-- label: sec:thm3_worldA -->

In the noise world $\mathcal{P}_{noise}$:

- **State $s_1$** (``clean but noisy''), with
- **State $s_2$** (``clean and easy''), with

Expert predictions depend only on the true label $y^*$ (through training on
clean data) and are conditionally independent given $x$.

#### World B: Difficulty-Driven Construction
<!-- label: sec:thm3_worldB -->

In the hardness world $\mathcal{P}_{hard}$:

- **State $s_1$**, with the same marginal probability $\rho$.
- **State $s_2$**, identical to World A: $y=y^*\equiv0$, expert

#### Observational Equivalence Verification
<!-- label: sec:thm3_verification -->

The observable joint distribution factorises as
\[
\mathcal{P}(x,y,f_1,...,f_M)
= \mathcal{P}(x)\cdot\mathcal{P}(y\mid x)\cdot\prod_{m=1}^M\mathcal{P}(f_m\mid x),
\]
using conditional independence of experts given $x$ (Assumptions A1--A2).

**Marginal $\mathcal{P**(x)$.}
In both worlds $\mathbb{P}(X\in s_1)=\rho$,
$\mathbb{P}(X\in s_2)=1-\rho$.  Identical.

**Conditional label distribution $\mathcal{P**(y\mid x)$.}
In World A (state $s_1$):
\[

$$
\mathcal{P}_{noise}(y=0\mid s_1)
&= (1-\eta_{err})\cdot1 + \eta_{err}\cdot0 = 1-\eta_{err},

\mathcal{P}_{noise}(y=1\mid s_1)
&= (1-\eta_{err})\cdot0 + \eta_{err}\cdot1 = \eta_{err}.
$$

\]
In World B (state $s_1$), $y=y^*$ directly:
\[
\mathcal{P}_{hard}(y=0\mid s_1)=1-\eta_{amb},\qquad
\mathcal{P}_{hard}(y=1\mid s_1)=\eta_{amb}.
\]
For state $s_2$, $\mathcal{P}(y=0\mid s_2)=1$,
$\mathcal{P}(y=1\mid s_2)=0$ in both worlds.  Hence
$\mathcal{P}(y\mid x)$ is identical across worlds.

**Conditional expert distribution $\mathcal{P**(f_m\mid x)$.}
In World A (state $s_1$), experts predict the true label $y^*\equiv0$ with
accuracy $1-\varepsilon_1$:
\[
\mathcal{P}_{noise}(f_m=0\mid s_1)=1-\varepsilon_1,\qquad
\mathcal{P}_{noise}(f_m=1\mid s_1)=\varepsilon_1.
\]
In World B (state $s_1$):
\[

$$
\mathcal{P}_{hard}(f_m=0\mid s_1)
&= \mathbb{P}(y^*=0\mid s_1)\cdot\mathbb{P}(f_m=0\mid s_1,y^*=0)

&\quad + \mathbb{P}(y^*=1\mid s_1)\cdot\mathbb{P}(f_m=0\mid s_1,y^*=1)

&= (1-\eta_{amb})(1-\varepsilon_1) + \eta_{amb}(1-\varepsilon_1) = 1-\varepsilon_1,
\mathcal{P}_{hard}(f_m=1\mid s_1)
&= (1-\eta_{amb})\varepsilon_1 + \eta_{amb}\varepsilon_1 = \varepsilon_1.
$$

\]
For state $s_2$, both worlds give $\mathcal{P}(f_m=0\mid s_2)=1-\varepsilon_2$,
$\mathcal{P}(f_m=1\mid s_2)=\varepsilon_2$.

**Joint identity.**
Combining the three components,
\[
\mathcal{P}_{noise}(x,y,\{f_m\})
= \mathcal{P}_{hard}(x,y,\{f_m\}),
\qquad \forall\,(x,y,\{f_m\}),
\]
which proves part~(iii) of Theorem~3. $\square$

#### Algorithm Impossibility
<!-- label: sec:thm3_impossibility -->

Let $\mathcal{A}$ be any algorithm that uses $n$ i.i.d.\ observations to
output per-sample noise flags $\{z_i\}_{i=1}^n$, where $z_i=1$ means ``label
is noisy.''  Since the observable distribution is identical in both worlds,
the algorithm's output distribution is also identical:
\[
\mathcal{L}_{\mathcal{P}_{noise}}(\mathcal{A}(D_n))
= \mathcal{L}_{\mathcal{P}_{hard}}(\mathcal{A}(D_n)).
\]

However, the *correct* noise flags differ between worlds.  In World~A,
the truly noisy samples are those in state $s_1$ with $y=1$ (a proportion
$\rho\eta$ of the data).  In World~B, *no* samples are noisy; the same
subset consists of correct but difficult samples.  The algorithm therefore
cannot simultaneously achieve zero error in both worlds.

Let $a$ be the expected fraction of the ambiguous subset
$\{x\in s_1,\;y=1\}$ that $\mathcal{A}$ flags as noisy.  Then:
\[
\mathrm{Error}_{\mathcal{P}_{noise}}(\mathcal{A}) = \rho\eta(1-a),\qquad
\mathrm{Error}_{\mathcal{P}_{hard}}(\mathcal{A}) = \rho\eta a.
\]
Hence
\[
\max\bigl(\mathrm{Error}_{\mathcal{P}_{noise}},\,
         \mathrm{Error}_{\mathcal{P}_{hard}}\bigr)
\ge \frac{\mathrm{Error}_{noise}+\mathrm{Error}_{hard}}{2}
= \frac{\rho\eta}{2}.
\]
This proves part~(iv). $\square$

### Extension to $K>2$ (Random Expert Construction)
<!-- label: sec:thm3_Kgeneral -->

For $K>2$, the binary construction does not generalise directly because the
expert marginals in the two worlds no longer match automatically.  We instead
use a different construction where experts in the hardness world are
*fully random* (conditionally independent of the true label).

**World A (Noise).**
State $s_1$: $y^*\equiv0$.  Noise flips the label uniformly over the
remaining $K-1$ classes with probability $\eta$:
\[
\mathbb{P}(y=c\midnoise,x\in s_1)=\frac{1}{K-1},\quad c\neq0.
\]
Expert $f_m$ predicts $0$ with probability $1-\varepsilon_1$, and each other
class with probability $\varepsilon_1/(K-1)$.  Thus
\[
\mathcal{P}_{noise}(y=0\mid s_1)=1-\eta,\quad
\mathcal{P}_{noise}(y=c\mid s_1)=\frac{K-1}\;(c\neq0),
\]
\[
\mathcal{P}_{noise}(f_m=0\mid s_1)=1-\varepsilon_1,\quad
\mathcal{P}_{noise}(f_m=c\mid s_1)=\frac{\varepsilon_1}{K-1}\;(c\neq0).
\]
By Assumption~A4, noise and expert predictions are independent given the
state, so $y\perp f_m\mid s_1$ in World~A.

**World B (Hardness).**
State $s_1$: all labels are correct ($y=y^*$).  The true label distribution
matches the World~A observed distribution:
\[
\mathbb{P}(y^*=0\mid s_1)=1-\eta,\quad
\mathbb{P}(y^*=c\mid s_1)=\frac{K-1}\;(c\neq0).
\]
**Critical construction:** experts are fully random, independent of the
true label:
\[
\mathbb{P}(f_m=0\mid s_1)=1-\varepsilon_1,\quad
\mathbb{P}(f_m=c\mid s_1)=\frac{\varepsilon_1}{K-1}\;(c\neq0),
\]
with $f_m\perp y^*\mid s_1$ and $f_m\perp y\mid s_1$ (since $y=y^*$).

**Equivalence.**
The marginal distributions of $y$, $f_m$, and the joint
$(y,\{f_m\})$ are identical in both worlds because both $y$ and $\{f_m\}$
are independent products of the same marginal distributions.  Hence for any
$K\ge2$:
\[
\mathcal{P}_{noise}(x,y,\{f_m\})
= \mathcal{P}_{hard}(x,y,\{f_m\}).
\]
The construction is extreme---experts in World~B are equivalent to random
guessers---but it suffices as an existence proof: there exists at least one
``hardness'' interpretation observationally indistinguishable from the
``noise'' interpretation. $\square$

### Corollaries: Which Assumptions Break Unidentifiability
<!-- label: sec:thm3_corollaries -->

Theorem~3 shows that without additional assumptions, noise and difficulty are
indistinguishable.  Each corollary below identifies a *sufficient
condition* that, if known to hold, breaks the equivalence.

#### Anchor Labels (Corollary 1)
<!-- label: sec:corollary1 -->

> **Corollary:** [Anchor Labels Break Unidentifiability]
>   If for a known subset $\mathcal{X}_{anchor}\subset\mathcal{X}$ the
>   researcher has access to the true labels $y^*$ (e.g.\ via human review),
>   then noise and difficulty are distinguishable on
>   $\mathcal{X}_{anchor}$.  If $\mathcal{X}_{anchor}$ covers all
>   states, the problem is globally identifiable.

> **Proof:** [Sketch]
>   On anchor points, compare the observed label $y$ with the true label $y^*$.
>   If $y\neq y^*$, the sample is necessarily noisy.  If $y=y^*$ but
>   $f_m(x)\neq y$, the sample is necessarily difficult (the expert errs on a
>   correctly labelled sample).  Extrapolating expert error rates from anchor
>   points to non-anchor points breaks global unidentifiability.

This corresponds to the SCX cold-start protocol, where a small number of
human-reviewed samples serve as anchors for initialising state-level noise
rate estimates.

#### Disjoint Training Data (Corollary 2)
<!-- label: sec:corollary2 -->

> **Corollary:** [Known Disjoint Training Data Break Unidentifiability]
>   If $M$ experts are trained on $M$ disjoint data subsets (Assumption~A1)
>   and the researcher knows the training set composition, then noise and
>   difficulty are distinguishable.

> **Proof:** [Sketch]
>   Disjoint training implies expert errors are conditionally independent given
>   $x$.  On noisy samples, *all* experts have elevated error rates
>   simultaneously (because they all predict the true label $y^*$, while the
>   observed label $y$ differs).  On difficult samples, expert errors are
>   independent.  The average error rate
>   $\bar{e}(x)=\frac1M\sum_m\mathbf{1}\{f_m(x)\neq y\}$ satisfies
>   \[
>   \mathbb{E}[\bar{e}(x)\midnoise]
>   = 1-\frac{1-\mathbb{E}[\bar{e}(x)\midclean]}{K-1}
>   \]
>   (Theorem~1, Lemma~1).  This relation cannot hold simultaneously in a pure
>   hardness world, providing a statistical test.

#### Input-Independent Noise (Corollary 3)
<!-- label: sec:corollary3 -->

> **Corollary:** [Input-Independent Noise Rate Breaks Unidentifiability]
>   If the label noise rate $\eta(x)=\mathbb{P}(Y\neq Y^*\mid X=x)$ is
>   constant across $x$ (Assumption~A4), and the expert error rates differ
>   between states, then noise and difficulty are distinguishable.

> **Proof:** [Sketch]
>   When $\eta(x)\equiv\eta$ is constant, the correlation pattern between the
>   observed label~$y$ and expert errors~$\{f_m\}$ differs fundamentally
>   between the two worlds.  In the noise world, $\mathbb{E}[\bar{e}(x)]$ is
>   constant across states (marginalising over the label-flip event).  In the
>   hardness world, $\bar{e}(x)$ varies with the state-dependent true label
>   distribution.  Testing for input dependence of $\bar{e}(x)$ conditioned on
>   $y$ distinguishes the two.

#### State Homogeneity (Corollary 4)
<!-- label: sec:corollary4 -->

> **Corollary:** [State Homogeneity Breaks Unidentifiability]
>   If within each state $s$ the expected expert error rate on clean samples is
>   constant (Assumption~A5), and states differ in this rate, then noise and
>   difficulty are distinguishable.

> **Proof:** [Sketch]
>   In the hardness world construction (World~B), state $s_1$ contains two
>   subpopulations---samples with $y^*=0$ (expert accuracy $1-\varepsilon_1$)
>   and samples with $y^*=1$ (expert accuracy $\varepsilon_1$).  This violates
>   state homogeneity, which requires a single per-state error rate.
>   Therefore, if Assumption~A5 holds, World~B's construction is invalid, and
>   the unidentifiability is broken.

#### Balanced Error Distribution (Corollary 5)
<!-- label: sec:corollary5 -->

> **Corollary:** [Balanced Error Distribution Breaks Unidentifiability]
>   If expert errors are uniformly distributed across all error classes
>   (Assumption~A6 with $C_{bal}=1$), then noise and difficulty are
>   distinguishable.

> **Proof:** [Sketch]
>   In World~B, experts are biased toward class~0: when $y^*=1$, they predict
>   class~0 with probability $1-\varepsilon_1$.  This creates a highly
>   imbalanced error pattern (errors are almost exclusively in the
>   $1\to0$ direction), violating the balanced error assumption.  If
>   Assumption~A6 is known to hold, World~B is excluded.

### Minimal Sufficient Assumption Set
<!-- label: sec:thm3_minimal -->

Theorem~3's construction relies on specific conditions.  To exclude the
construction---and thereby break unidentifiability---at least one of the
following combinations of assumptions is necessary and sufficient:

\[

$$
\mathcal{A}_^{(1)} &= \{A1,\;A4,\;A5\},

\mathcal{A}_^{(2)} &= \{A1,\;A4,\;A6\},

\mathcal{A}_^{(3)} &= \{A5,\;A6\}\quadwith |\mathcal{S}|\ge2.
$$

\]

The SCX framework operates under $\mathcal{A}_^{(1)}$ (the standard
set A1--A6 provides additional technical benefits for finite-sample bounds).
Each assumption plays a distinct role:

- **A1** (disjoint training): ensures expert independence, enabling
- **A4** (uniform noise): removes the possibility of
- **A5** (state homogeneity): prevents a single state from
- **A6** (balanced errors): prevents expert bias from creating

If *all* of these assumptions are violated, Theorem~3 applies fully:
no algorithm can distinguish label noise from sample difficulty.

### Corollary: The Everyone Equal Theorem (Everyone Equal Theorem)
<!-- label: sec:thm3_equal -->

> **Corollary:** [The Everyone Equal Theorem (Everyone Equal Theorem)]
> <!-- label: cor:everyone-equal -->
> Let any observer $O$ claim to distinguish label noise from sample difficulty
> using any algorithm $\mathcal{A}$. Then either
> 
1. the structural assumptions relied upon by $\mathcal{A}$ are
2. the claim is mathematically empty---no amount of observational

> Furthermore, if (i) holds, the assumptions are verifiable by any observer
> without privileged access to $O$'s data, model, or expertise. All observers
> are placed on equal epistemic footing.

> **Proof:** Theorem~3 establishes $P_{W_A}(X,Y) = P_{W_B}(X,Y)$ for all observers,
> i.e., the joint distribution of inputs, labels, and multi-expert predictions
> is identical in the noise world and the difficulty world. Consequently, for
> any discrimination rule $d$,
> \[
> \max_{W\in\{W_A,W_B\}} P_W\bigl(d(X,Y) \neq W\bigr) \geq \frac{1}{2},
> \]
> as proved via Le Cam's lemma in the main text. This lower bound is
> observer-independent: it holds for *any* algorithm $\mathcal{A}$
> deployed by *any* observer $O$, because the observational data do not
> encode observer identity.
> 
> Therefore, if $O$ claims to achieve discrimination performance better than
> chance, the claim must rely on assumptions that break the observational
> equivalence $P_{W_A} = P_{W_B}$. These assumptions---the minimal sufficient
> set $\mathcal{A}_$ derived above---must be stated. Once stated, they
> are verifiable by any observer: checking disjoint training (A1), uniform
> noise (A4), state homogeneity (A5), and balanced errors (A6) requires only
> access to the training procedure and data distribution, not to $O$'s
> internal state.
> 
> Hence no observer occupies a privileged epistemic position. The theorem
> places all observers---regardless of institutional authority, computational
> resources, or social status---on identical mathematical ground.

> **Remark:** [No privileged observer]
> The name ``The Everyone Equal Theorem'' (Everyone Equal Theorem) reflects the
> corollary's operational meaning: the mathematical structure of data quality
> assessment does not permit any person, algorithm, institution, or nation to
> claim inherent authority over the distinction between noise and difficulty.
> Authority must be earned through transparently stated, independently
> verifiable assumptions. This is the formal basis for the SCX framework's
> commitment to epistemic equality.

### Conjecture: The Good Person Convergence Conjecture (Good Person Convergence)
<!-- label: sec:good-convergence -->

> **Conjecture:** [The Good Person Convergence Conjecture (Good Person Convergence Conjecture)]
> <!-- label: conj:good-convergence -->
> Consider a community of $N$ agents interacting under the SCX framework:
> each agent may produce data, claim data quality, or audit others' claims.
> Let the following conditions hold:
> 
1. **The Honest Person Condition**: every data-quality claim must state its
2. **The Everyone Equal Condition**: no agent occupies a privileged epistemic
3. **The No-Pretension Condition**: audit outputs are unconditionally verifiable

> Then, as $t\to\infty$:
> 
1. The fraction of agents making unverifiable claims converges to
2. The expected payoff of honest behaviour exceeds that of dishonest
3. The community converges to an equilibrium in which every agent

> **Remark:** [Status of this claim]
> <!-- label: remark:good-convergence-status -->
> **This is a conjecture, not a theorem.** The original manuscript
> presented a 13-line ``proof sketch'' that merely cited Theorems~3, NPE,
> and Corollary [ref] without establishing a formal
> logical chain from premises to conclusion. A rigorous proof would require:
> 
1. A formal agent model (type space, strategy space, payoff functions);
2. A dynamic process description (discrete/continuous time, update rules);
3. A rigorous definition of convergence (topological space, convergence mode);
4. A Lyapunov or potential function establishing the stability of the
5. Verification that the three conditions (C1--C3) are not circular---each

> Until such a proof is provided, the ``Good Person Convergence'' claim remains
> a compelling research programme rather than an established result. The
> intuition---that SCX's mathematical structure makes honesty strategically
> dominant---is provocative and merits further investigation, but it has not
> been formally demonstrated.

### 认识论形式化系统 (Epistemic Formalization System — E1-E5 + K算子)
<!-- label: sec:epistemic -->

We formalize the classical epistemological question---``when does a
community know a claim?''---as a probabilistic decision problem within
the SCX framework. The key insight: *knowledge is a claim that
survives multi-expert audit with provable statistical guarantees.*

#### Axioms for the Verification Framework
<!-- label: sec:epistemic-axioms -->

> **Definition:** [Verification framework]
> <!-- label: def:verification-framework -->
> Let $\mathcal{S}$ be a claim with truth value $T(\mathcal{S})\in\{0,1\}$
> (unknown to verifiers). Let $\mathcal{C}=\{v_1,...,v_M\}$ be $M$
> verifiers. Each $v_m$ produces a noisy binary judgment
> $J_m(\mathcal{S})\in\{0,1\}$ via access only to observational data
> $(X,Y,\{f_m\}_{m=1}^M)$ as defined in the SCX framework.

\begin{assumption}[Epistemic axioms E1--E5]
<!-- label: ax:epistemic -->

1. **Assumption transparency:** the claim $\mathcal{S}$ is
2. **Assumption soundness:** under $\mathcal{A}_{\mathcal{S}}$,
3. **State-homogeneous verifier quality:** within each state
4. **Observational indistinguishability:** verifiers have access
5. **Counterexample logging:** the Yajie CEC $\mathcal{E}_t$

\end{assumption}

#### The Knowledge Operator
<!-- label: sec:knowledge-operator -->

> **Definition:** [SCX-knowledge operator $\mathbf{K}$]
> <!-- label: def:K-operator -->
> For claim $\mathcal{S}$, assumption set $\mathcal{A}_{\mathcal{S}}$,
> community $\mathcal{C}$ of size $M$, and state $s\in\mathcal{S}$, define
> the **verification score**:
> \[
> V_M(\mathcal{S}, s) = \frac{1}{M}\sum_{m=1}^{M} J_m(\mathcal{S}; s)
> \]
> where $J_m(\mathcal{S}; s)$ is verifier $m$'s judgment on samples in
> state $s$. Define the **decision threshold** $\theta_s \in (0,1)$.
> 
> A **counterexample** is a triple $(x, y, \{f_m(x)\})$ such that
> $\mathcal{A}_{\mathcal{S}}$ holds but $V_M(\mathcal{S}, s(x)) < \theta_{s(x)}$.
> Let $\mathcal{E}_t$ be the set of counterexamples accumulated up to time $t$.
> A counterexample $e \in \mathcal{E}_t$ is **resolved** if either (a) it
> has been adjudicated and found consistent with $\mathcal{A}_{\mathcal{S}}$
> under additional scrutiny, or (b) the claim is amended to accommodate it.
> Otherwise it is **unresolved**.
> 
> The **SCX-knowledge operator** is defined per-state:
> \[
> \mathbf{K}_{t}(\mathcal{S}, \mathcal{C}, s) =
> \begin{cases}
> 1 & if  V_M(\mathcal{S}, s) \geq \theta_s
>        and no unresolved counterexample in  \mathcal{E}_t
>        involves state  s,
> 0 & otherwise.
> \end{cases}
> \]
> The claim-level knowledge operator aggregates state-level judgments:
> $\mathbf{K}_{t}(\mathcal{S}, \mathcal{C}) = \mathbf{1}\{\mathbf{K}_t(\mathcal{S},
> \mathcal{C}, s) = 1  for all  s \in \supp(
> ho)\}$.

#### Rigorous Guarantee
<!-- label: sec:epistemic-guarantee -->

> **Theorem:** [认识论形式化系统 (Epistemic Formalization System) — E1-E5 + K算子]
> <!-- label: thm:epistemic-rigorous -->
> Under the **SCX Axiom System (SCX Axiom System)** E1--E5 and the SCX framework conditions A1--A6
> (Theorem~1), for any claim $\mathcal{S}$ with stated assumptions
> $\mathcal{A}_{\mathcal{S}}$ and any community $\mathcal{C}$ of $M$
> independent verifiers, the knowledge operator satisfies:
> \[
> \boxed{\mathbb{P}\bigl(\mathbf{K}(\mathcal{S},\mathcal{C}) \neq T(\mathcal{S})
>   \mid \mathcal{A}_{\mathcal{S}}\bigr)
>   \leq \sum_{s\in\mathcal{S}} \rho_s \exp\bigl(-2M\Delta_s^2\bigr)}
> \]
> where $\rho_s$ is the fraction of verification samples in state $s$,
> and $\Delta_s = \theta_s - (1-p_s)$ is the separation between the
> decision threshold and the expected error rate. The error probability
> decays exponentially in the number of verifiers $M$.
> 
> Furthermore, this bound is tight: no knowledge operator operating under
> E1--E5 can achieve a smaller error exponent without additional structural
> assumptions, by Theorem~4 (The Extreme Precision Theorem).

> **Proof:** The proof is a direct application of Theorem~1's concentration argument
> to the verification setting. For each state $s$, the verifier judgments
> $\{J_m(\mathcal{S}; s)\}_{m=1}^M$ are $M$ independent Bernoulli trials
> with success probability $p_s$ (E2, E3). If $T(\mathcal{S})=1$ (the claim
> is true), then $p_s \geq 1-\varepsilon_s$ by E3. The verification score
> $V_M$ is a sample mean of $M$ independent Bernoulli variables.
> By Hoeffding's inequality and the state-conditioned decomposition of
> Theorem~1 (equation S1.7):
> \[
> \mathbb{P}\bigl(V_M \leq \theta_s \mid T(\mathcal{S})=1\bigr)
>   \leq \exp\bigl(-2M(\theta_s - p_s)^2\bigr)
>   = \exp\bigl(-2M\Delta_s^2\bigr).
> \]
> The same bound holds symmetrically when $T(\mathcal{S})=0$, with
> $\Delta_s = p_s - (1-\theta_s)$.
> 
> The verifier errors are conditionally independent given the state (E3
> strengthened by A2' from Theorem~1). The optional stopping argument from
> Theorem~1's proof extends to the sequential audit setting, ensuring that
> the bound does not degrade with multiple looks at the data.
> 
> For the tightness claim, Theorem~4 (The Extreme Precision Theorem) establishes that the
> exponential rate $2M\Delta_s^2$ is minimax-optimal: any decision rule
> operating on $M$ verifier judgments incurs an error exponent at least
> this large. Hence the SCX-knowledge operator achieves the fundamental
> limit. $\square$

#### Properties of $\mathbf{K$}
<!-- label: sec:K-properties -->

> **Corollary:** [Knowledge operator properties]
> <!-- label: cor:K-properties -->
> The SCX-knowledge operator $\mathbf{K}$ satisfies:
> 
1. **Non-triviality:** $\mathbf{K}(\mathcal{S}) \neq 1$ for any
2. **Exponential reliability:**
3. **Monotonicity under audit:** if $\mathbf{K}_t(\mathcal{S})=1$,
4. **Gettier immunity (operational):** Gettier (1963) cases arise when a claim
5. **Epistemic equality:** $\mathbf{K}$ depends only

#### Connection to Classical Epistemology
<!-- label: sec:epistemic-classical -->

> **Remark:** [What we did to Plato]
> Plato (c.\ 369 BCE) defined knowledge as justified true belief.
> Gettier (1963) found counterexamples where justification and truth
> coincide accidentally due to unstated contingencies. The subsequent
> literature attempted to *redefine* justification.
> 
> The SCX approach does not redefine---it *operationalizes*.
> Knowledge is not a metaphysical state of an individual mind; it is
> the mathematical status of a claim that has survived multi-expert
> audit under stated assumptions with provable statistical guarantees.
> The bound $\exp(-2M\Delta_s^2)$ replaces philosophical debate with
> a quantitative threshold: ``how many independent verifiers do we
> need?'' becomes a solvable equation.

### Connections to Prior Art
<!-- label: sec:thm3_prior -->

#### Measurement Error Models

In classical measurement error models
 [cite], the observed variable
$Y$ is modelled as $Y=Y^*+U$ where $U$ is measurement error.  Without
validation data or instrumental variables, the distributions of $Y^*$ and
$U$ are not separately identifiable from the marginal distribution of $Y$.
Theorem~3 extends this classical result from continuous measurement error to
the classification setting with multi-expert predictions.  The key novelty is
that even with the additional information $\{f_m(X)\}$---which one might
expect to resolve the ambiguity---the unidentifiability persists.

#### Label Noise Transition Matrix Unidentifiability

The label noise literature  [cite]
established that the noise transition matrix $T_{ij}=\mathbb{P}(\tilde Y=j\mid
Y^*=i)$ is not identifiable from $(\tilde Y,X)$ alone without anchor points or
diagonal-dominance assumptions.  Theorem~3 generalises this to the multi-expert
setting, showing that even with $M$ expert predictions, the ambiguity between
noise and intrinsic difficulty remains.

#### Dawid-Skene Unidentifiability

The Dawid-Skene model  [cite] treats the true label as a latent
variable and each annotator's confusion matrix as a parameter.  Standard
identifiability issues include label-switching symmetries.  Theorem~3 addresses
a different and more fundamental ambiguity: even after resolving
label-switching, one cannot distinguish whether an annotator's error is due to
noise in the label or difficulty of the sample.  The two unidentifiability
problems are orthogonal: both must be resolved for reliable label quality
assessment.

#### Causal Structure Unidentifiability

From a causal perspective, Theorem~3 can be understood as a Markov equivalence
class problem  [cite].  Two causal directed acyclic graphs
generate identical observational distributions:

- **Noise graph:** $S\to Y^*\to Y\leftarrowNoise$,
- **Difficulty graph:** $S\to Y^*(=Y)$, $X\to\{f_m\}$, where state

These two graphs are observationally indistinguishable, forming a
Markov equivalence class of size~2.

### References for Section~S3

\begingroup

\begin{thebibliography}{20}
\bibitem{fuller1987measurement} Fuller, W. A. *Measurement Error Models*. Wiley (1987).
\bibitem{carroll2006measurement} Carroll, R. J., Ruppert, D., Stefanski, L. A. \& Crainiceanu, C. M. *Measurement Error in Nonlinear Models: A Modern Perspective*. Chapman and Hall/CRC (2006).
\bibitem{menon2015learning} Menon, A. K., van Rooyen, B., Ong, C. S. \& Williamson, R. C. Learning from corrupted binary labels via class-probability estimation. *Proc. ICML* (2015).
\bibitem{patrini2017making} Patrini, G., Rozza, A., Menon, A. K., Nock, R. \& Qu, L. Making deep neural networks robust to label noise: A loss correction approach. *Proc. CVPR* (2017).
\bibitem{dawid1979maximum} Dawid, A. P. \& Skene, A. M. Maximum likelihood estimation of observer error-rates using the EM algorithm. *Applied Statistics* **28**(1), 20--28 (1979).
\bibitem{pearl2009causality} Pearl, J. *Causality: Models, Reasoning, and Inference*. Cambridge University Press, 2nd ed. (2009).
\bibitem{bahadur1960deviations} Bahadur, R. R. \& Rao, R. R. On deviations of the sample mean. *Annals of Mathematical Statistics* **31**(4), 1015--1027 (1960).
\end{thebibliography}
\endgroup

\endinput