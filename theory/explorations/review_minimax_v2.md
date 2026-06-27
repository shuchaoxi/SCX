# Review: Minimax Lower Bound v2 (Hellinger Distance Proof)

> **File reviewed**: `G:\Xiaogan_Supercomputing_data\SCX\theory\explorations\minimax_lower_bound_v2.md`
>
> **Review date**: 2026-06-27
>
> **Scope**: Full mathematical verification of all inequalities, formulas, and derivations.
> Numerical cross-checking of all claimed relationships.

---

## 1. Overall Verdict

The proof correctly fixes the three fatal issues from v1 (Slud's inequality, chi-squared direction, F1 algebra), and the core Hellinger tensorization approach is sound. **However, two new fatal errors have been introduced in the F1 conversion section** (Section 7), and a significant formula error appears in the K > 2 section (Section 8.3).

**Bottom line**: The testing error lower bound (Part a) is correct. The F1 lower bound (Part b) has two algebraic errors that invalidate its stated constant. The rate optimality claim (Part c) remains correct because the exponential rate `exp(-2MDelta^2)` is preserved under the corrected analysis.

---

## 2. Issues Found

### Issue 1 [FATAL]: Section 7.3 -- Backwards inequality in F1 simplification

**Location**: Lines 423-427

**Claim**:
```
(1-eta)*(rho^M/4)/(2eta+(1-eta)*(rho^M/4)) >= (1-eta)*rho^M/(8eta)
```

**What is wrong**: The inequality is backwards. Since `2eta + (1-eta)*(rho^M/4) > 2eta` for any positive `rho^M`, the left-hand side has a larger denominator with the same numerator, making it strictly smaller. The correct inequality is `<=`, not `>=`.

**Verification** (eta = 0.3, rho^M = 0.1):
```
LHS = 0.7*0.025/(0.6+0.7*0.025) = 0.02834
RHS = 0.7*0.1/(8*0.3) = 0.02917
LHS < RHS, so LHS >= RHS is FALSE.
```

**Consequence**: The simplified bound `1-F1 >= rho^M/(16eta)` is not validly derived. The correct inequality direction gives an upper bound `LHS <= RHS`, which is useless for lower-bounding 1-F1.

**How to fix**: The exact bound must be kept in its unsimplified form:
```
1-F1 >= (1-eta)(rho^M/4)/(2eta+(1-eta)(rho^M/4))
```

Or a correct simplification with a multiplicative correction:
```
1-F1 >= (1-eta)*rho^M/(8eta) * (1 - (1-eta)*rho^M/(4eta))
```

(using `1/(1+x) >= 1-x` for `x >= 0`)

---

### Issue 2 [FATAL]: Section 7.5 -- Wrong case selected as tighter bound

**Location**: Lines 439-467

**Claim**:
```
eps/2 >= (1-eta)*eps/(2eta+(1-eta)*eps) for eta <= 1/2
```

And consequently:
```
min(eps/(2-eps), (1-eta)*eps/(2eta+(1-eta)*eps)) = (1-eta)*eps/(2eta+(1-eta)*eps)
```

**What is wrong**: The inequality direction is reversed for `eta < 1/2` and small `eps` (the regime of interest). The proof attempts to verify this by cross-multiplication, claiming:

`2eta + (1-eta)*eps >= 2*(1-eta)` follows from `eps >= 0, eta >= 0`.

But the correct cross-multiplication is:

```
eps/2 >= (1-eta)*eps/(2eta+(1-eta)*eps)
=> 2eta + (1-eta)*eps >= 2*(1-eta)
=> (1-eta)*eps >= 2 - 4eta
```

For `eta = 0.3`: requires `eps >= 0.8/0.7 ≈ 1.14`. Impossible since `eps <= 1` (and typically `eps << 1`).
For `eta = 0.4`: requires `eps >= 0.4/0.6 ≈ 0.667`. Possible but atypical -- rho^M would need to be >= 2.67, impossible since rho <= 1.
For `eta = 0.49`: requires `eps >= 0.04/0.51 ≈ 0.078`. Possible for some parameters.
For `eta = 0.5`: requires `eps >= 0`. True.

So the claim only holds when `(1-eta)*eps >= 2-4eta`, i.e., when `eta >= 1/(2-eps/(1-eps))` approximately. For most of the parameter space (especially small `eps` and small-to-moderate `eta`), the claim is FALSE.

**Verification** (eta = 0.3, eps = 0.1):
```
eps/2 = 0.05
(1-eta)*eps/(2eta+(1-eta)*eps) = 0.7*0.1/0.67 ≈ 0.104
So eps/2 < case2_bound, not >=.
```

The correct minimum is:
`min(eps/(2-eps), (1-eta)*eps/(2eta+(1-eta)*eps)) = eps/(2-eps)` (Case 1)

for all `eta < 1/2` and small `eps`.

**Consequence**: The claimed universal bound `1-F1 >= (1-eta)*eps/(2eta+(1-eta)*eps)` is invalid. The correct universal bound uses Case 1:

```
1-F1 >= eps/(2-eps) = rho^M/(8-rho^M)
```

which is approximately `rho^M/8` (not `rho^M/(16eta)`).

**Comparison of bounds**:
```
eta=0.1: correct=rho^M/8, claimed=rho^M/1.6  (claimed 5x too large)
eta=0.3: correct=rho^M/8, claimed=rho^M/4.8  (claimed 1.67x too large)
eta=0.5: correct=rho^M/8, claimed=rho^M/8    (match at eta=0.5)
```

**How to fix**: Use the Case 1 bound:
```
1-F1 >= eps/(2-eps) = (rho^M/4)/(2-rho^M/4) = rho^M/(8-rho^M)
```

For the simplified form (small rho^M):
```
1-F1 >= rho^M/8
```

---

### Issue 3 [MAJOR]: Section 8.3 -- Incorrect Hellinger affinity formula for K > 2

**Location**: Line 511

**Claim**:
```
rho_K = 2*sqrt(mu_s * (1 - mu_s/(K-1)))
```

**What is wrong**: This formula is only correct for K=2. The general Hellinger affinity for `Bernoulli(p)` vs `Bernoulli(q)` is:

```
rho = sqrt(p*q) + sqrt((1-p)*(1-q))
```

The proof's formula `2*sqrt(p*q)` only matches the general formula when `q = 1-p`, i.e., when `K=2` (since `1 - mu_s/(K-1) = 1 - mu_s = 1 - p` only when `K=2`).

For K > 2, the correct formula is:

```
rho_K = sqrt(mu_s * (1 - mu_s/(K-1))) + sqrt((1-mu_s) * (mu_s/(K-1)))
```

**Verification** (mu_s = 0.3, K = 3):
```
correct: sqrt(0.3*0.85) + sqrt(0.7*0.15) = 0.505 + 0.324 = 0.829
wrong:   2*sqrt(0.3*0.85) = 2*0.505 = 1.010
```

The wrong formula gives `rho > 1` for many parameter values (e.g., mu=0.3, K=3: rho=1.010; mu=0.2, K=5: rho=0.872). While `rho <= 1` should always hold for Hellinger affinity. The correct formula always satisfies `rho <= 1`.

**Consequence**: The numerical values and asymptotic expressions for K > 2 are wrong. However, the **conclusion** that K=2 is the hardest case is still correct (verified with the correct formula -- rho_K < rho_2 for K > 2, giving a weaker bound, so K=2 gives the strongest valid lower bound for all K >= 2).

**How to fix**: Replace the formula with the correct expression:
```
rho_K = sqrt(mu_s * (1 - mu_s/(K-1))) + sqrt((1-mu_s) * (mu_s/(K-1)))
```

And note that `rho_K < rho_2 = 2*sqrt(mu_s*(1-mu_s))` for all K > 2, which can be verified by squaring both sides.

---

### Issue 4 [MAJOR]: Section 11 -- Chernoff exactness claim fails for K > 2

**Location**: Lines 676-681

**Claim**:
```
-log(rho) = KL(1/2 || mu_s) = Chernoff exponent
```

**What is wrong**: This holds for K=2 because the likelihood ratio `dP1/dP0` is symmetric on the log scale (values are reciprocals). For K > 2, the optimal Chernoff exponent generally uses a tilting parameter `t != 1/2`, so `-log(rho_K) > KL(1/2 || mu_s)`. The Hellinger exponent `-log(rho_K)` is still a valid lower bound on the Chernoff exponent, but it is **not exact**.

**Verification** (mu=0.3, K=3):
```
-log(rho_K) = -log(0.829) = 0.188
KL(1/2||0.3) = 0.087
-0.188 != 0.087.
```

**Consequence**: The claim that the Hellinger approach gives "exact Chernoff exponent" is true only for K=2 (or more generally, when the two distributions are symmetric on the log-odds scale). For K > 2, the Hellinger exponent is a valid but non-exact lower bound.

**How to fix**: Clarify that the Chernoff exactness holds for K=2 and provide the general expression for K > 2, or simply note that the Hellinger bound is always valid and the exponent is bounded below by the K=2 exponent.

---

### Issue 5 [MAJOR]: Section 9 -- C_bal > 1 extension is incomplete

**Location**: Lines 536-619

**What is wrong**: The section is a sketch, not a rigorous proof. There are several gaps:

1. The convexity bound via `sqrt` concavity gives `H^2(P0, P1) <= avg H^2(P0, Q_ell)`, which is correct. But the translation to a lower bound on the testing error uses `TV <= H`, which yields `R >= (1-TV)/2 >= (1-sqrt(avg H^2))/2`. This is a valid bound but may be very weak.

2. The analysis switches between using `max H` and `min H` inconsistently. Line 605 says "the worst (largest) Hellinger distance among the mixture components gives the tightest upper bound on TV", but line 610 then says "the component with the smallest... gives the smallest Hellinger distance, and hence the weakest lower bound." These are different criteria and the presentation is confusing.

3. The claim "the exponent 2MDelta^2 is preserved" (line 618) is asserted without proof. While it's plausibly true (each component's gap is at least `Delta` times some C_bal-dependent factor), no rigorous derivation is given.

**Consequence**: The Theorem 4 statement claims to hold under (A1)-(A6) without requiring C_bal = 1, but the proof only fully handles C_bal = 1. The C_bal > 1 case is not rigorously proven.

**How to fix**: Either (a) add C_bal = 1 as an explicit condition in the theorem statement, or (b) provide a complete derivation for C_bal > 1. Option (b) would involve bounding the average Hellinger affinity:

```
(1/L) sum_ell rho_ell^M >= min_ell rho_ell^M
```

where `rho_ell = sqrt(mu_s * p_ell) + sqrt((1-mu_s) * (1-p_ell))` and `p_ell = 1 - C_ell*mu_s/(K-1)` for some `C_ell >= 1`. The smallest `rho_ell` (closest to 1) gives the weakest bound, and this is attained at `C_ell = C_bal` (or similar).

---

### Issue 6 [MINOR]: Section 6.4 -- Wrong Taylor coefficient for Delta^4

**Location**: Lines 340-344

**Claim**:
```
log(1-4Delta^2) = -4Delta^2 - 8Delta^4/3 - O(Delta^6)
```

**What is wrong**: The Taylor expansion of `log(1-x) = -x - x^2/2 - x^3/3 - ...` with `x = 4Delta^2` gives:

```
log(1-4Delta^2) = -4Delta^2 - (4Delta^2)^2/2 - (4Delta^2)^3/3 - ...
               = -4Delta^2 - 16Delta^4/2 - 64Delta^6/3 - ...
               = -4Delta^2 - 8Delta^4 - O(Delta^6)
```

The coefficient of `Delta^4` is `-8`, not `-8/3`.

Then `(M/2)*log(1-4Delta^2) = -2M*Delta^2 - 4M*Delta^4 - O(M*Delta^6)`, not `-2M*Delta^2 - (4/3)M*Delta^4 - O(M*Delta^6)`.

**Consequence**: The specific coefficient in the `O(M*Delta^4)` term is wrong, but this term is absorbed into the `O(M*Delta^4)` notation anyway. No substantive claim is affected.

**How to fix**: Correct the coefficient.

---

## 3. Algebraic Verification of F1 Conversion

This is the most critical section. Below is a complete, corrected derivation of the F1 lower bound.

### Setup

- Testing error: `R(psi) = max(alpha, beta)` where `alpha = P0(psi=1)`, `beta = P1(psi=0)`
- Le Cam bound: `R(psi) >= (1-TV)/2 >= rho^M/4 =: epsilon`
- So `max(alpha, beta) >= epsilon`

### F1 in terms of alpha, beta

```
F1 = 2*TP/(2*TP + FP + FN)
   = 2*eta*(1-beta) / (2*eta*(1-beta) + (1-eta)*alpha + eta*beta)
```

### Case analysis

**Case 1**: `beta >= epsilon` (false negative rate is high)

Using `FP >= 0`:
```
F1 <= 2*eta*(1-beta) / (2*eta*(1-beta) + eta*beta)
    = 2*(1-beta)/(2-beta)
```

Since `beta >= epsilon` and the function is decreasing in `beta`:
```
F1 <= 2*(1-epsilon)/(2-epsilon)
1-F1 >= epsilon/(2-epsilon)
```

**Case 2**: `alpha >= epsilon` (false positive rate is high)

Using `FN >= 0`:
```
F1 <= 2*eta*(1-beta) / (2*eta*(1-beta) + (1-eta)*alpha)
```

Since `beta >= 0` (maximizes F1 at `beta = 0`) and `alpha >= epsilon`:
```
F1 <= 2*eta / (2*eta + (1-eta)*epsilon)
1-F1 >= (1-eta)*epsilon / (2*eta + (1-eta)*epsilon)
```

### Universal bound

Since `max(alpha, beta) >= epsilon`, either Case 1 or Case 2 must hold. Therefore:

```
1-F1 >= min(epsilon/(2-epsilon), (1-eta)*epsilon/(2*eta+(1-eta)*epsilon))
```

### Which case is tighter?

For `eta < 1/2` and small `epsilon` (the typical regime):

```
epsilon/(2-epsilon) ≈ epsilon/2
(1-eta)*epsilon/(2*eta+(1-eta)*epsilon) ≈ (1-eta)*epsilon/(2*eta)
```

Ratio: `(epsilon/2) / ((1-eta)*epsilon/(2*eta)) = eta/(1-eta) < 1` for `eta < 1/2`.

So Case 1 gives the smaller bound (tighter). **This contradicts the proof's claim.**

### Correct F1 lower bound

```
1-F1 >= epsilon/(2-epsilon) = (rho^M/4)/(2 - rho^M/4) = rho^M/(8 - rho^M)
```

For small `rho^M`:
```
1-F1 >= rho^M/8   (conservative simplification)
```

Compare with the claimed bound `rho^M/(16*eta)`:

| eta | Correct bound | Claimed bound | Ratio |
|-----|---------------|---------------|-------|
| 0.1 | `rho^M/8` | `rho^M/1.6` | 5x too large |
| 0.3 | `rho^M/8` | `rho^M/4.8` | 1.67x too large |
| 0.5 | `rho^M/8` | `rho^M/8` | Match |

The claimed bound is **stronger than justified** for all `eta < 1/2`, with the discrepancy growing as `eta` decreases.

### Rate optimality preserved

Both the correct bound `rho^M/8` and the claimed bound `rho^M/(16*eta)` have leading term `rho^M` = `(2*sqrt(mu_s(1-mu_s)))^M` = `exp(-2M*Delta^2 + O(M*Delta^4))`. The rate is preserved, confirming that Part (c) is unaffected.

---

## 4. Summary of Correct vs. Claimed Results

| Quantity | Claimed in v2 | Correct value | Severity |
|----------|---------------|---------------|----------|
| Testing bound | `rho^M/4` | `rho^M/4` | **OK** |
| F1 bound (const) | `rho^M/(16*eta)` | `rho^M/(8-rho^M)` | **FATAL (const wrong)** |
| F1 bound (rate) | `exp(-2M*Delta^2)` | `exp(-2M*Delta^2)` | **OK** |
| K>2 affinity | `2*sqrt(mu*(1-mu/(K-1)))` | `sqrt(mu*(1-mu/(K-1))) + sqrt((1-mu)*mu/(K-1))` | **MAJOR (formula wrong)** |
| Chernoff exactness | Holds for all K | Holds for K=2 only | **MAJOR (overclaimed)** |
| C_bal > 1 | Claimed but not proven | Needs rigorous treatment | **MAJOR (gap)** |
| Taylor coeff | `-8/3*Delta^4` | `-8*Delta^4` | **MINOR** |

---

## 5. Comparison to v1: What is Fixed, What Remains

### Fixed from v1

| Issue | v1 | v2 | Status |
|-------|----|----|--------|
| Slud's inequality | Fatal error (false bound) | Hellinger tensorization | **Fixed** |
| Chi-squared direction | Used wrong direction for K>2 | Product reduction with correct direction | **Fixed** |
| F1 algebra | Algebraic error in Lemma 8 | Case analysis (new errors introduced) | **Partially fixed, new errors** |
| Odd M ceiling | Unaddressed | Works for all M | **Fixed** |

### Remaining issues (this review)

1. **F1 constant is wrong** (Section 7.3, 7.5) -- The simplification uses backwards inequality directions. The correct bound is `1-F1 >= rho^M/(8-rho^M)`, which is approximately `rho^M/8`, not `rho^M/(16*eta)`.

2. **K > 2 affinity formula is wrong** (Section 8.3) -- The formula `2*sqrt(mu*(1-mu/(K-1)))` is incorrect and can give values > 1. The correct formula is a sum of two square roots.

3. **Chernoff exactness overclaimed** (Section 11) -- True for K=2 but not K>2.

4. **C_bal > 1 is a sketch** (Section 9) -- Not a complete proof.

### Recommendations

1. Correct the F1 bound to `1-F1 >= rho^M/(8-rho^M)` (or the conservative `rho^M/8`).
2. Correct the K>2 affinity formula.
3. Move the Chernoff exactness claim to the K=2 section only.
4. Either require C_bal = 1 explicitly in the theorem statement, or provide a complete C_bal > 1 proof.
5. Verify the corrected F1 bound still matches the numerical examples (it does: `1-F1 >= rho^M/8` gives `0.8^10/8 ≈ 0.013`, which is `<=` the direct bound `0.027` from the full expression -- this is conservative but valid).

---

*End of review.*
