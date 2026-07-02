# Adversarial Verification: Conditional Independence of
Bootstrap-Trained Expert Error
Indicators

**Author:** SCX

**Claim under review**: If M experts are trained on independent
bootstrap samples D\_1, ..., D\_M (drawn i.i.d. with replacement from
the dataset), then their error indicators e\_m(x) = 1\{ℓ(f\_m(x), y)
\textgreater{} τ\} are conditionally independent given the test point x.

**Reference assumptions**: The paper's A1 requires DISJOINT
independent training sets (D\_m ∩ D\_\{m'\} = ∅), which differs
fundamentally from bootstrap. See below.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Attack 1: Bootstrap samples are NOT independent --- the
claim's premise is
false<!-- label: attack-1-bootstrap-samples-are-not-independent-the-claims-premise-is-false -->

**Description**: The claim asserts ``D\_1, ..., D\_M are
independent by construction (bootstrap).'' This is mathematically
incorrect.

Bootstrap with replacement from the same finite dataset D\_original =
\{z\_1, ..., z\_N\} works as follows:

- 
- 

For a **fixed** D\_original, D\_1 and D\_2 are conditionally
independent given D\_original. But if D\_original is itself random
(which is the standard statistical setting --- the training data is a
random sample from population D), then:

P(D\_1 ∈ A, D\_2 ∈ B) = E{[} P(D\_1 ∈ A |{} D\_original) · P(D\_2
∈ B |{} D\_original) {]}

Since P(D\_1 ∈ A |{} D\_original) and P(D\_2 ∈ B |{}
D\_original) are both functions of the same random D\_original, they are
generally correlated. The expectation of the product does not factor:

E{[}U · V{]} ≠ E{[}U{]} · E{[}V{]} when U, V are correlated.

Therefore, D\_1 and D\_2 are **not unconditionally independent**.
Step 1 of the proof is wrong.

**Concrete counterexample**: Let D\_original = \{Z\_1, Z\_2\} with
Z\_1, Z\_2 ~{} Bernoulli(p) i.i.d. (so N=2). Draw
bootstrap samples of size n=1 (one element each). Then:

- 
- 

P(D\_1=\{1\}, D\_2=\{1\}) = P(at least one Z=1)² ? No.~Let me compute:

P(D\_1=\{1\} |{} D\_original) = 1\{Z\_1=1 or Z\_2=1\}
P(D\_2=\{1\} |{} D\_original) = 1\{Z\_1=1 or Z\_2=1\}

So P(D\_1=\{1\}, D\_2=\{1\}) = E{[}1\{Z\_1=1 or Z\_2=1\}²{]} = P(Z\_1=1
or Z\_2=1) = 2p - p²

And P(D\_1=\{1\})·P(D\_2=\{1\}) = (2p - p²)²

These are equal only when 2p - p² ∈ \{0, 1\}, i.e., p ∈ \{0, 1\}. For
any non-degenerate p ∈ (0,1): 2p - p² ≠ (2p - p²)² because 2p - p² ∈
(0,1).

Thus D\_1 and D\_2 are **not independent**. They are equal with
positive probability due to both depending on the same D\_original.

**Verdict: FAIL** --- The very first step of the proof is false.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Attack 2: The proof sketch ignores the shared label
y<!-- label: attack-2-the-proof-sketch-ignores-the-shared-label-y -->

**Description**: The proof states ``e\_m(x) depends only on
f\_m(x).'' This is false. The error indicator is:

e\_m(x, y) = 1\{ℓ(f\_m(x), y) \textgreater{} τ\}

It depends on **both** f\_m(x) and the observed label y. Since y is
a single random variable shared across all M experts, it creates a
common source of randomness. Even if f\_m(x) are independent, the
indicators e\_1, ..., e\_M all depend on the same y, so they are not
independent unless y is degenerate.

**Resolution**: The claim can be salvaged if y is
**independent** of the vector (f\_1(x), ..., f\_M(x)). In the
paper's setting, A4 states that the label noise is independent of all
D\_m and x. Under the paper's A1 (disjoint datasets), combined with a
proper train-test split (x not in any D\_m), we have:

- 
- 
- 

In that case, e\_m(x,y) = g(f\_m(x), y) where g(a,b) = 1\{ℓ(a,b)
\textgreater{} τ\}. Since (f\_1(x), ..., f\_M(x), y) are independent
random variables, and e\_m depends only on (f\_m(x), y), the indicators
e\_1, ..., e\_M are **not** fully independent of each other
(they share y), but they ARE conditionally independent given y (or given
any σ-algebra that fixes y). However, the claim says ``conditional
independence given x'' not ``given x and y.''

**More precise analysis**: Define e\_m = 1\{ℓ(f\_m(x), y)
\textgreater{} τ\}. Are e\_1 and e\_2 independent? Let's check:

P(e\_1 = 1, e\_2 = 1 |{} x) = E{[} P(e\_1=1, e\_2=1 |{} x,
f\_1, f\_2, y) |{} x {]} = E{[} 1\{ℓ(f\_1(x), y) \textgreater{}
τ\} · 1\{ℓ(f\_2(x), y) \textgreater{} τ\} |{} x {]}

If y is independent of (f\_1, f\_2) given x, then: = ∫ P(ℓ(f\_1(x), y)
\textgreater{} τ, ℓ(f\_2(x), y) \textgreater{} τ |{} x, f\_1,
f\_2) dP(f\_1, f\_2 |{} x)

The inner probability involves the same y, so it does not factor as
P(ℓ(f\_1(x), y) \textgreater{} τ |{} f\_1) · P(ℓ(f\_2(x), y)
\textgreater{} τ |{} f\_2). The indicators are **correlated
through y**.

However, if we condition on y as well (i.e., ``given x and y''), then:

P(e\_1=1, e\_2=1 |{} x, y) = P(ℓ(f\_1(x), y) \textgreater{} τ
|{} x, y) · P(ℓ(f\_2(x), y) \textgreater{} τ |{} x, y)

which factors because f\_1(x) and f\_2(x) are independent given x, and y
is now fixed by conditioning.

**The proof's error**: The proof says ``e\_m(x) depends only on
f\_m(x)'' --- this is simply wrong. It depends on f\_m(x) AND y. The
author appears to have forgotten that e\_m takes two arguments, not one.

**Verdict: FAIL** --- The proof sketch contains a concrete
mathematical error. The claim IS true if we condition on both x and y,
but the proof as written is incorrect.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Attack 3: Fatal mismatch between the claim and the paper's
A1<!-- label: attack-3-fatal-mismatch-between-the-claim-and-the-papers-a1 -->

**Description**: The paper's A1 states:

\[D_m \sim \mathcal{D}^{n_m}, \quad D_m \cap D_{m'} = \varnothing, \quad D_m \perp D_{m'}  for  m \neq m'\]

This requires: 1. **Disjoint** training sets (no overlap) 2. Fresh
i.i.d. draws from the population distribution

The claim substitutes ``bootstrap samples drawn i.i.d. with replacement
from the dataset,'' which is: 1. **Overlapping** (bootstrap
resamples from the same data) 2. Drawn from a **single fixed
dataset**, not from the population distribution

These are fundamentally different sampling regimes:

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
Property & Paper (A1) & Claim 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Overlap? & Never (disjoint) & Frequent (with replacement) 

Source & Population D & Fixed dataset 

Independence & Unconditional & Conditional on dataset only 

\# of distinct samples & n\_1 + ...{} + n\_M & At most N (original
size) 

\end{longtable}

The paper's Lemma 1, Lemma 2, and main theorem were constructed on the
assumption of disjoint training sets. Swapping in bootstrap invalidates
those proofs. For example, Lemma 1 computes:

E{[}C(x) |{} clean, x{]} = (1/M) Σ\_m P(ℓ(f\_m(x), y)
\textgreater{} τ |{} clean, x)

Under bootstrap, f\_m are **not independent**, so the average of
e\_m has different concentration properties than what the paper's
Chernoff bounds assume.

**Verdict: FAIL** --- The claim investigates a different setting
than the paper's. The claim's premise (bootstrap) contradicts the
paper's A1 (disjoint).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Attack 4: Non-deterministic training and hidden shared
randomness<!-- label: attack-4-non-deterministic-training-and-hidden-shared-randomness -->

**Description**: The claim assumes f\_m = A(D\_m) where A is
deterministic. In practice:

- 
- 
- 
- 
- 

If A is not deterministic, then f\_m = A(D\_m, ξ\_m) where ξ\_m captures
the training noise. The claim's step 2 (``f\_m depends only on D\_m'')
becomes false.

**However**: This is **fixable** if we assume the ξ\_m are
independent across experts and independent of D\_m. Then the argument
extends: f\_m depends on (D\_m, ξ\_m), all of which are independent
across m. The claim would then hold conditional on x and y (assuming the
ξ\_m and D\_m are independent of (x, y)).

**Edge case**: If all experts use the same random seed, ξ\_m = ξ
for all m, creating shared randomness across experts. In this case,
f\_1, ..., f\_M share the same ξ, breaking conditional independence.
This is a real practical concern.

**Edge case**: GPU non-determinism is not ``randomness'' in the
usual sense --- it's deterministic chaos from parallel floating-point
operations. It cannot be modeled as independent ξ\_m without explicit
intervention (e.g., forcing separate CUDA streams).

**Verdict: PASS** (with caveats) --- In theory, the randomness can
be made explicit and independent. In practice, shared seeds or GPU
non-determinism can create subtle dependencies. This is not fatal to the
mathematical claim if the independence of ξ\_m is explicitly assumed.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Attack 5: ``Independent random functions'' does not
automatically imply pointwise independence for random test
points<!-- label: attack-5-independent-random-functions-does-not-automatically-imply-pointwise-independence-for-random-test-points -->

**Description**: The claim says ``f\_m are independent random
functions, therefore f\_m(x) are independent for fixed x.'' This is
mathematically correct for a **deterministic** x. However:

- 
- 
- 

**This is technically standard** --- the almost-sure definition of
conditional independence works. So this is not a genuine flaw, merely a
technical subtlety.

**Verdict: PASS** --- Standard measure-theoretic conditioning
handles this.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Attack 6: In the bootstrap setting, overlapping training
data creates dependence beyond
D\_original<!-- label: attack-6-in-the-bootstrap-setting-overlapping-training-data-creates-dependence-beyond-d_original -->

**Description**: Even when D\_original is treated as fixed
(conditional inference), bootstrap samples are conditionally independent
given D\_original. However, there is a deeper issue:

Two bootstrap samples D\_1 and D\_2 can share specific training
examples. For instance, if D\_original contains a unique outlier z* (an
image with a rare artifact), and both D\_1 and D\_2 include z*,
both f\_1 and f\_2 will have seen this outlier. Their predictions on
test points similar to z* will be correlated in a way that is NOT
captured by the independence assumption --- they share information about
z*.

Formally: P(f\_1(x) = c |{} D\_original) and P(f\_2(x) = c
|{} D\_original) are both influenced by the same D\_original. The
conditional independence given D\_original is fine, but the
unconditional distribution of f\_1 and f\_2 (integrating over
D\_original) reflects the fact that both experts ``see'' the same data
generating process.

For the paper's concentration bounds, what matters is:

P(| C(x) - E{[}C(x){]}|{} \textgreater{} ε |{} x)

If we use the conditional independence given D\_original, we get:

P(| C(x) - E{[}C(x){]}|{} \textgreater{} ε |{} x,
D\_original) ≤ 2 exp(-2Mε²)

But then taking expectations over D\_original:

P(| C(x) - E{[}C(x){]}|{} \textgreater{} ε |{} x) ≤
E{[}2 exp(-2Mε²) |{} x{]} = 2 exp(-2Mε²)

Wait --- this works because the bound is constant! In this case, the
unconditional bound is the same. But if the bound depends on D\_original
(e.g., if the mean μ varies with D\_original), then:

P(| C(x) - E{[}C(x){]}|{} \textgreater{} ε |{} x) =
E{[}P(| C(x) - E{[}C(x){]}|{} \textgreater{} ε |{}
x, D\_original){]} ≤ E{[}2 exp(-2Mε²){]} = 2 exp(-2Mε²) ← still OK
because bound is constant

Actually, the issue is more subtle for the Chernoff bound used in the
paper. The bound depends on the mean μ\_s, which is an unconditional
expectation. If we only have conditional independence given D\_original,
the Chernoff bound would involve the conditional mean given D\_original,
which is random.

**This attack is a variant of Attack 1** and is ultimately fatal to
the bootstrap interpretation.

**Verdict: FAIL** (same root cause as Attack 1)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Attack 7: The label y might come from the same distribution
as the training data, creating subtle
dependence<!-- label: attack-7-the-label-y-might-come-from-the-same-distribution-as-the-training-data-creating-subtle-dependence -->

**Description**: In the paper's label noise model (A4), the
observed label y is:

y = y* (true label) with probability 1-η y = Uniform(Y ~\{y*\}) with
probability η

The label noise is independent of D\_m. But the true label y* =
f*(x) depends on x, which is the test point. If x is from the test
set (properly separated), then y* is independent of D\_m, and the claim
holds.

**But what if the claim's ``bootstrap'' setting includes the
possibility that x comes from the training data?** In bootstrap
validation (like out-of-bag estimation), some test points may have been
seen in some bootstrap samples. If x ∈ D\_1 (overlap between train and
``test''), then:

- 
- 
- 

This breaks the conditional independence argument entirely. For a proper
test point (not in any training set), this doesn't apply. But the claim
doesn't specify train-test separation.

**Verdict: FAIL** --- The claim uses ``test point x'' language but
doesn't ensure x is not in any bootstrap sample. For proper evaluation
(new unseen test data), this can be assumed away, but the bootstrap
framing makes it ambiguous.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### Final Verdict<!-- label: final-verdict -->

**The claim IS NOT rigorous.** There are 4 significant issues, 3 of
which are fatal:

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2667}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3333}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
\#
\end{minipage} & \begin{minipage}[b]
Attack
\end{minipage} & \begin{minipage}[b]
Severity
\end{minipage} & \begin{minipage}[b]
Verdict
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
1 & Bootstrap samples are not independent & **Fatal** --- step 1 of
proof is false & FAIL 

2 & Proof ignores the shared label y & **Fatal** --- proof contains
mathematical error & FAIL 

3 & Mismatch with paper's A1 (disjoint vs bootstrap) & **Fatal**
--- different sampling regime & FAIL 

6 & Bootstrap overlap creates dependence through D\_original &
**Fatal** --- variant of Attack 1 & FAIL 

7 & Training-test leakage in bootstrap & **Fatal** --- not
specified & FAIL 

4 & Non-deterministic training & Caveat, fixable & PASS 

5 & Formal conditioning issues & Standard technicality & PASS 

\end{longtable}

**Bottom line**: The claim suffers from a fatal contradiction in
its premises (``bootstrap'' and ``independent'' are incompatible), a
concrete mathematical error in its proof (ignoring the shared label y),
and a mismatch with the paper's A1 assumption. Under the paper's actual
assumption (disjoint datasets), and with a corrected proof that properly
accounts for y, the conditional independence claim can be made rigorous
--- but the claim as stated and its proof sketch are not correct.