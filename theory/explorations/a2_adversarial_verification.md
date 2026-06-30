# Adversarial Verification: Conditional Independence of Bootstrap-Trained Expert Error Indicators

**Claim under review**: If M experts are trained on independent bootstrap samples D_1, ..., D_M (drawn i.i.d. with replacement from the dataset), then their error indicators e_m(x) = 1{ℓ(f_m(x), y) > τ} are conditionally independent given the test point x.

**Reference assumptions**: The paper's A1 requires DISJOINT independent training sets (D_m ∩ D_{m'} = ∅), which differs fundamentally from bootstrap. See below.

---

## Attack 1: Bootstrap samples are NOT independent — the claim's premise is false

**Description**: The claim asserts "D_1, ..., D_M are independent by construction (bootstrap)." This is mathematically incorrect.

Bootstrap with replacement from the same finite dataset D_original = {z_1, ..., z_N} works as follows:

- D_m = {Z_{I_{m,1}}, ..., Z_{I_{m,n}}} where each index I_{m,j} is drawn uniformly from {1, ..., N} with replacement.
- D_1 and D_2 are functions of (D_original, ξ_1) and (D_original, ξ_2) respectively, where ξ_1, ξ_2 are independent index sets.

For a **fixed** D_original, D_1 and D_2 are conditionally independent given D_original. But if D_original is itself random (which is the standard statistical setting — the training data is a random sample from population D), then:

P(D_1 ∈ A, D_2 ∈ B) = E[ P(D_1 ∈ A | D_original) · P(D_2 ∈ B | D_original) ]

Since P(D_1 ∈ A | D_original) and P(D_2 ∈ B | D_original) are both functions of the same random D_original, they are generally correlated. The expectation of the product does not factor:

E[U · V] ≠ E[U] · E[V] when U, V are correlated.

Therefore, D_1 and D_2 are **not unconditionally independent**. Step 1 of the proof is wrong.

**Concrete counterexample**: Let D_original = {Z_1, Z_2} with Z_1, Z_2 ~ Bernoulli(p) i.i.d. (so N=2). Draw bootstrap samples of size n=1 (one element each). Then:

- P(D_1 = {1}) = P(Z_1=1 or Z_2=1) = 1 - (1-p)^2 = 2p - p^2
- P(D_1 = {1}, D_2 = {1}) = P(∃ i,j: Z_i=1 and Z_j=1) = 1 - P(all Z's = 0) - 2·P(exactly one Z=1, other draws that one) ... more directly:

P(D_1={1}, D_2={1}) = P(at least one Z=1)² ? No. Let me compute:

P(D_1={1} | D_original) = 1{Z_1=1 or Z_2=1}
P(D_2={1} | D_original) = 1{Z_1=1 or Z_2=1}

So P(D_1={1}, D_2={1}) = E[1{Z_1=1 or Z_2=1}²] = P(Z_1=1 or Z_2=1) = 2p - p²

And P(D_1={1})·P(D_2={1}) = (2p - p²)²

These are equal only when 2p - p² ∈ {0, 1}, i.e., p ∈ {0, 1}. For any non-degenerate p ∈ (0,1): 2p - p² ≠ (2p - p²)² because 2p - p² ∈ (0,1).

Thus D_1 and D_2 are **not independent**. They are equal with positive probability due to both depending on the same D_original.

**Verdict: FAIL** — The very first step of the proof is false.

---

## Attack 2: The proof sketch ignores the shared label y

**Description**: The proof states "e_m(x) depends only on f_m(x)." This is false. The error indicator is:

e_m(x, y) = 1{ℓ(f_m(x), y) > τ}

It depends on **both** f_m(x) and the observed label y. Since y is a single random variable shared across all M experts, it creates a common source of randomness. Even if f_m(x) are independent, the indicators e_1, ..., e_M all depend on the same y, so they are not independent unless y is degenerate.

**Resolution**: The claim can be salvaged if y is **independent** of the vector (f_1(x), ..., f_M(x)). In the paper's setting, A4 states that the label noise is independent of all D_m and x. Under the paper's A1 (disjoint datasets), combined with a proper train-test split (x not in any D_m), we have:

- f_m(x) depends only on D_m
- y is independent of {D_1, ..., D_M} (by train-test split + A4)
- Therefore, y is independent of (f_1(x), ..., f_M(x))

In that case, e_m(x,y) = g(f_m(x), y) where g(a,b) = 1{ℓ(a,b) > τ}. Since (f_1(x), ..., f_M(x), y) are independent random variables, and e_m depends only on (f_m(x), y), the indicators e_1, ..., e_M are **not** fully independent of each other (they share y), but they ARE conditionally independent given y (or given any σ-algebra that fixes y). However, the claim says "conditional independence given x" not "given x and y."

**More precise analysis**: Define e_m = 1{ℓ(f_m(x), y) > τ}. Are e_1 and e_2 independent? Let's check:

P(e_1 = 1, e_2 = 1 | x) = E[ P(e_1=1, e_2=1 | x, f_1, f_2, y) | x ]
= E[ 1{ℓ(f_1(x), y) > τ} · 1{ℓ(f_2(x), y) > τ} | x ]

If y is independent of (f_1, f_2) given x, then:
= ∫ P(ℓ(f_1(x), y) > τ, ℓ(f_2(x), y) > τ | x, f_1, f_2) dP(f_1, f_2 | x)

The inner probability involves the same y, so it does not factor as P(ℓ(f_1(x), y) > τ | f_1) · P(ℓ(f_2(x), y) > τ | f_2). The indicators are **correlated through y**.

However, if we condition on y as well (i.e., "given x and y"), then:

P(e_1=1, e_2=1 | x, y) = P(ℓ(f_1(x), y) > τ | x, y) · P(ℓ(f_2(x), y) > τ | x, y)

which factors because f_1(x) and f_2(x) are independent given x, and y is now fixed by conditioning.

**The proof's error**: The proof says "e_m(x) depends only on f_m(x)" — this is simply wrong. It depends on f_m(x) AND y. The author appears to have forgotten that e_m takes two arguments, not one.

**Verdict: FAIL** — The proof sketch contains a concrete mathematical error. The claim IS true if we condition on both x and y, but the proof as written is incorrect.

---

## Attack 3: Fatal mismatch between the claim and the paper's A1

**Description**: The paper's A1 states:

$$D_m \sim \mathcal{D}^{n_m}, \quad D_m \cap D_{m'} = \varnothing, \quad D_m \perp D_{m'} \text{ for } m \neq m'$$

This requires:
1. **Disjoint** training sets (no overlap)
2. Fresh i.i.d. draws from the population distribution

The claim substitutes "bootstrap samples drawn i.i.d. with replacement from the dataset," which is:
1. **Overlapping** (bootstrap resamples from the same data)
2. Drawn from a **single fixed dataset**, not from the population distribution

These are fundamentally different sampling regimes:

| Property | Paper (A1) | Claim |
|----------|------------|-------|
| Overlap? | Never (disjoint) | Frequent (with replacement) |
| Source | Population D | Fixed dataset |
| Independence | Unconditional | Conditional on dataset only |
| # of distinct samples | n_1 + ... + n_M | At most N (original size) |

The paper's Lemma 1, Lemma 2, and main theorem were constructed on the assumption of disjoint training sets. Swapping in bootstrap invalidates those proofs. For example, Lemma 1 computes:

E[C(x) | clean, x] = (1/M) Σ_m P(ℓ(f_m(x), y) > τ | clean, x)

Under bootstrap, f_m are **not independent**, so the average of e_m has different concentration properties than what the paper's Chernoff bounds assume.

**Verdict: FAIL** — The claim investigates a different setting than the paper's. The claim's premise (bootstrap) contradicts the paper's A1 (disjoint).

---

## Attack 4: Non-deterministic training and hidden shared randomness

**Description**: The claim assumes f_m = A(D_m) where A is deterministic. In practice:

- Deep learning uses stochastic gradient descent with random minibatch order
- Random initialization
- Data augmentation randomness (random crops, flips)
- GPU non-determinism (atomic operation ordering)
- Dropout

If A is not deterministic, then f_m = A(D_m, ξ_m) where ξ_m captures the training noise. The claim's step 2 ("f_m depends only on D_m") becomes false.

**However**: This is **fixable** if we assume the ξ_m are independent across experts and independent of D_m. Then the argument extends: f_m depends on (D_m, ξ_m), all of which are independent across m. The claim would then hold conditional on x and y (assuming the ξ_m and D_m are independent of (x, y)).

**Edge case**: If all experts use the same random seed, ξ_m = ξ for all m, creating shared randomness across experts. In this case, f_1, ..., f_M share the same ξ, breaking conditional independence. This is a real practical concern.

**Edge case**: GPU non-determinism is not "randomness" in the usual sense — it's deterministic chaos from parallel floating-point operations. It cannot be modeled as independent ξ_m without explicit intervention (e.g., forcing separate CUDA streams).

**Verdict: PASS** (with caveats) — In theory, the randomness can be made explicit and independent. In practice, shared seeds or GPU non-determinism can create subtle dependencies. This is not fatal to the mathematical claim if the independence of ξ_m is explicitly assumed.

---

## Attack 5: "Independent random functions" does not automatically imply pointwise independence for random test points

**Description**: The claim says "f_m are independent random functions, therefore f_m(x) are independent for fixed x." This is mathematically correct for a **deterministic** x. However:

- The paper's main results involve expectations over the test distribution, not a single fixed x.
- If x is random (X), the statement "e_1(X), ..., e_M(X) are independent given X" is a statement about regular conditional probabilities.
- For continuous X, the event {X = x} has measure zero, requiring careful use of regular conditional probabilities.

**This is technically standard** — the almost-sure definition of conditional independence works. So this is not a genuine flaw, merely a technical subtlety.

**Verdict: PASS** — Standard measure-theoretic conditioning handles this.

---

## Attack 6: In the bootstrap setting, overlapping training data creates dependence beyond D_original

**Description**: Even when D_original is treated as fixed (conditional inference), bootstrap samples are conditionally independent given D_original. However, there is a deeper issue:

Two bootstrap samples D_1 and D_2 can share specific training examples. For instance, if D_original contains a unique outlier z* (an image with a rare artifact), and both D_1 and D_2 include z*, both f_1 and f_2 will have seen this outlier. Their predictions on test points similar to z* will be correlated in a way that is NOT captured by the independence assumption — they share information about z*.

Formally: P(f_1(x) = c | D_original) and P(f_2(x) = c | D_original) are both influenced by the same D_original. The conditional independence given D_original is fine, but the unconditional distribution of f_1 and f_2 (integrating over D_original) reflects the fact that both experts "see" the same data generating process.

For the paper's concentration bounds, what matters is:

P(|C(x) - E[C(x)]| > ε | x)

If we use the conditional independence given D_original, we get:

P(|C(x) - E[C(x)]| > ε | x, D_original) ≤ 2 exp(-2Mε²)

But then taking expectations over D_original:

P(|C(x) - E[C(x)]| > ε | x) ≤ E[2 exp(-2Mε²) | x] = 2 exp(-2Mε²)

Wait — this works because the bound is constant! In this case, the unconditional bound is the same. But if the bound depends on D_original (e.g., if the mean μ varies with D_original), then:

P(|C(x) - E[C(x)]| > ε | x) = E[P(|C(x) - E[C(x)]| > ε | x, D_original)]
≤ E[2 exp(-2Mε²)] = 2 exp(-2Mε²) ← still OK because bound is constant

Actually, the issue is more subtle for the Chernoff bound used in the paper. The bound depends on the mean μ_s, which is an unconditional expectation. If we only have conditional independence given D_original, the Chernoff bound would involve the conditional mean given D_original, which is random.

**This attack is a variant of Attack 1** and is ultimately fatal to the bootstrap interpretation.

**Verdict: FAIL** (same root cause as Attack 1)

---

## Attack 7: The label y might come from the same distribution as the training data, creating subtle dependence

**Description**: In the paper's label noise model (A4), the observed label y is:

y = y* (true label) with probability 1-η
y = Uniform(Y \ {y*}) with probability η

The label noise is independent of D_m. But the true label y* = f*(x) depends on x, which is the test point. If x is from the test set (properly separated), then y* is independent of D_m, and the claim holds.

**But what if the claim's "bootstrap" setting includes the possibility that x comes from the training data?** In bootstrap validation (like out-of-bag estimation), some test points may have been seen in some bootstrap samples. If x ∈ D_1 (overlap between train and "test"), then:

- f_1(x) is trained on x itself, creating a data leakage
- y is not independent of D_1 (since the pair (x, y) might be in D_1)
- e_1(x) and e_2(x) now have a complex dependence structure through the shared (x, y) in D_1

This breaks the conditional independence argument entirely. For a proper test point (not in any training set), this doesn't apply. But the claim doesn't specify train-test separation.

**Verdict: FAIL** — The claim uses "test point x" language but doesn't ensure x is not in any bootstrap sample. For proper evaluation (new unseen test data), this can be assumed away, but the bootstrap framing makes it ambiguous.

---

## Final Verdict

**The claim IS NOT rigorous.** There are 4 significant issues, 3 of which are fatal:

| # | Attack | Severity | Verdict |
|---|--------|----------|---------|
| 1 | Bootstrap samples are not independent | **Fatal** — step 1 of proof is false | FAIL |
| 2 | Proof ignores the shared label y | **Fatal** — proof contains mathematical error | FAIL |
| 3 | Mismatch with paper's A1 (disjoint vs bootstrap) | **Fatal** — different sampling regime | FAIL |
| 6 | Bootstrap overlap creates dependence through D_original | **Fatal** — variant of Attack 1 | FAIL |
| 7 | Training-test leakage in bootstrap | **Fatal** — not specified | FAIL |
| 4 | Non-deterministic training | Caveat, fixable | PASS |
| 5 | Formal conditioning issues | Standard technicality | PASS |

**Bottom line**: The claim suffers from a fatal contradiction in its premises ("bootstrap" and "independent" are incompatible), a concrete mathematical error in its proof (ignoring the shared label y), and a mismatch with the paper's A1 assumption. Under the paper's actual assumption (disjoint datasets), and with a corrected proof that properly accounts for y, the conditional independence claim can be made rigorous — but the claim as stated and its proof sketch are not correct.
