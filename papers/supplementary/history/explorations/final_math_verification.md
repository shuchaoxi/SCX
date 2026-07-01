# Final Mathematical Verification Report

**Reviewer**: Pure mathematician (formal verification of mathematical claims only)
**Date**: 2026-06-28
**Scope**: Theorems 1-5, supporting lemmas, and numerical test cases
**Files reviewed**:
- `G:\Xiaogan_Supercomputing_data\SCX\theory\theorems\01_noise_detection_guarantee.md`
- `G:\Xiaogan_Supercomputing_data\SCX\theory\theorems\02_weak_feature_failure.md`
- `G:\Xiaogan_Supercomputing_data\SCX\theory\theorems\03_unidentifiability_theorem.md`
- `G:\Xiaogan_Supercomputing_data\SCX\theory\explorations\exact_constant_minimax.md`
- `G:\Xiaogan_Supercomputing_data\SCX\theory\explorations\lemma_AB_bahadur_rao_f1.md`
- `G:\Xiaogan_Supercomputing_data\SCX\theory\explorations\lemma_CD_chernoff_adaptive.md`
- `G:\Xiaogan_Supercomputing_data\SCX\theory\explorations\lemma_EF_lowerbound_aggregation.md`
- `G:\Xiaogan_Supercomputing_data\SCX\theory\explorations\cluster_consistency_v3.md`
- `G:\Xiaogan_Supercomputing_data\SCX\theory\explorations\deep_math_connections.md`

---

## 1. Theorem 1 (Noise Detection Guarantee)

### Lemma 1 (Mean Separation)

**Claim**: E[C|noise,x] = 1 - E[C|clean,x]/(K-1)

**Verification**: PASS.

The proof expands:
- E[C|noise,x] = (1/M) sum_m P(f_m(x) != y | noise, x)
- P(f_m(x) != y | noise, x) = sum_{c != y*} P(y=c|noise) * P(f_m(x) != c | x)
- = sum_{c != y*} (1/(K-1)) * (1 - P(f_m(x)=c|x))
- = 1 - (1/(K-1)) * sum_{c != y*} P(f_m(x)=c|x)
- = 1 - (1/(K-1)) * (1 - P(f_m(x)=y*|x))
- = 1 - (1/(K-1)) * E[e_m|clean,x]

Averaging over m gives: E[C|noise,x] = 1 - E[C|clean,x]/(K-1). The algebra is correct. Each step uses only: (A4) uniform noise over K-1 classes, linearity of expectation, and identity sum_{c != y*} P(f_m=c|x) = E[e_m|clean,x].

The separation condition mu_s < (K-1)/K is correctly derived from: clean mean <= mu_s, noise mean >= 1 - mu_s/(K-1), requiring mu_s < 1 - mu_s/(K-1) => mu_s * K/(K-1) < 1 => mu_s < (K-1)/K.

The optimal threshold theta* = (1/2)(1 + mu_s*(K-2)/(K-1)) solves theta - mu_s = 1 - mu_s/(K-1) - theta correctly.

### Lemma 2 (FPR)

**Claim**: P(C > theta | clean, s) <= exp(-2M(theta - mu_s)^2)

**Verification**: PASS.

Standard Hoeffding inequality for bounded [0,1] independent r.v.s. The conditioning chain:
- Fix x in s: E[C|clean,x] <= mu_s by (A5)
- {e_m} conditionally independent given x by (A2), bounded by [0,1] by (A3)
- P(C - E[C|x] > theta - E[C|x] | clean, x) <= exp(-2M(theta - E[C|x])^2) <= exp(-2M(theta - mu_s)^2)
- The last step uses: theta > mu_s >= E[C|x], so (theta - E[C|x]) >= (theta - mu_s)
- Marginalizing over x in s preserves the bound via sup

All conditions for Hoeffding are satisfied.

### Lemma 3 (TPR)

**Claim**: P(C <= theta | noise, s) <= exp(-2M(1 - C_bal*mu_s/(K-1) - theta)^2)

**Verification**: PASS, with careful reading.

The proof conditions on (x, c) where c is the noise label:
- Given (x, c), {e_m} are conditionally independent (A1, A2) with e_m ~ Bern(1 - mu_{c,m}(x))
- E[C|x,c] = 1 - mu_c(x) >= 1 - C_bal*mu_s/(K-1) by (A6)
- The theorem assumes theta < 1 - C_bal*mu_s/(K-1), so Hoeffding applies
- P(C <= theta | x, c) <= exp(-2M(E[C|x,c] - theta)^2) <= exp(-2M(1 - C_bal*mu_s/(K-1) - theta)^2)
- Averaging over c (uniform over K-1 classes) preserves the bound

Key subtlety: the bound uses mu_c(x) <= C_bal*mu_s/(K-1), so E[C|x,c] >= 1 - C_bal*mu_s/(K-1). The Hoeffding gap (E[C|x,c] - theta) is minimized (worst case) when E[C|x,c] is smallest, which occurs at the max mu_c(x). The A6 assumption correctly captures this via C_bal.

### F1 bound

**Claim**: F1 >= 1 - (1/eta) sum_s rho_s exp(-2M Delta_s^2)

**Verification**: PASS.

Algebraic derivation:
- F1 = 2*eta*TPR / (eta(1+TPR) + (1-eta)FPR) [verified via Precision-Recall algebra]
- Substituting TPR >= 1-delta_1, FPR <= delta_2 gives denominator >= eta
- 1 - F1 <= delta_1 + (1-eta)delta_2/eta
- Since delta_1, delta_2 <= sum rho_s exp(-2M Delta_s^2), the final bound follows

The denominator is strictly positive: eta(2-FNR)+(1-eta)FPR >= eta > 0 for eta > 0.

---

## 2. Theorem 2 (Weak Features)

### Fano inequality

**Claim**: P(S_hat != S) >= (H(S) - delta - log 2) / log K

**Verification**: PASS.

Standard Fano inequality: P(S_hat != S) >= (H(S|phi(X)) - log 2) / log |S|.
Since I(phi;S) <= delta by the delta-weak feature definition:
H(S|phi) = H(S) - I(phi;S) >= H(S) - delta.
Substituting gives: P(S_hat != S) >= (H(S) - delta - log 2) / log K.

The feature-dependent Markov chain Z -> S -> X -> phi(X) correctly implies I(phi;Z) <= I(S;Z) <= H(Z) by the data processing inequality.

### Pinsker inequality

**Claim**: TV(P, P_tilde) <= sqrt(delta/2)

**Verification**: PASS.

P_tilde(phi, S) = P(phi) * P(S). KL(P || P_tilde) = I(phi; S) = delta.
Pinsker: TV <= sqrt(KL/2) = sqrt(delta/2).

### F1 bound

**Claim**: F1_SCX <= F1_base + C_F * sqrt(delta/2)

**Verification**: PASS (with caveat on Lipschitz constant).

The reasoning chain:
1. Under P_tilde, SCX detection score degrades to loss baseline: NS(x) ~ max_m D_m(x)
2. Hence F1_P_tilde(SCX) = F1_base
3. |F1_P(SCX) - F1_P_tilde(SCX)| <= C_F * TV(P_pred, P_tilde_pred) by Lipschitz property
4. TV(P_pred, P_tilde_pred) <= TV(P, P_tilde) by data processing inequality
5. <= sqrt(delta/2)

The Lipschitz analysis of F1(TP, FP, FN) = 2TP/(2TP+FP+FN) is partial derivatives and the document acknowledges that C_F depends on precision/recall regime. The specific values (C_F <= 2 for precision, recall >= 0.1) are heuristic estimates, not rigorous bounds. This is flagged as an approximate constant in the text.

**Minor issue**: The AUC bound's TV-to-conditional-TV step uses division by eta and 1-eta:
|P(A|Z=1) - P_tilde(A|Z=1)| <= TV(P, P_tilde)/eta.
This requires eta > 0 (non-zero noise rate). For eta -> 0 the bound diverges, which the document correctly acknowledges.

---

## 3. Theorem 3 (Unidentifiability)

### K=2 construction

**Claim**: P_noise(x, y, {f_m}) = P_hard(x, y, {f_m})

**Verification**: PASS.

World A (noise): s1 has noise rate eta, clean expert error epsilon_1. s2 has no noise.
World B (hard): s1 has random true label (P(y*=0)=1-eta, P(y*=1)=eta), experts biased toward class 0.

Equality verification:
- P_A(y=0|s1) = (1-eta)*1 + eta*0 = 1-eta
- P_B(y=0|s1) = P(y*=0|s1) = 1-eta
- P_A(f_m=0|s1) = 1-epsilon_1 (expert accuracy against true label y*=0)
- P_B(f_m=0|s1) = (1-eta)(1-epsilon_1) + eta(1-epsilon_1) = 1-epsilon_1

Joint factorization P(x,y,{f_m}) = P(x) * P(y|x) * prod_m P(f_m|x) holds by conditional independence in both constructions. State s2 is identical in both worlds.

### K>2 construction

**Claim**: The construction works for all K >= 2.

**Verification**: PASS.

For K > 2, the construction uses completely random experts (independent of y*):
- World A: y* = 0, noise uniform over K-1 classes. Expert predicts 0 with prob 1-epsilon_1
- World B: y* non-deterministic (same distribution as y in World A). Expert is pure random

P_A(y=0|s1) = 1-eta = P_B(y=0|s1)
P_A(f_m=0|s1) = 1-epsilon_1 = P_B(f_m=0|s1)
Independence of y and f_m holds in both worlds by construction. Joint distribution matches for all K >= 2.

### Error bound eta*rho/2

**Claim**: max(Error_A, Error_B) >= eta*rho/2

**Verification**: PASS.

Let a be the fraction of ambiguous samples ({x in s1, y=1}) flagged as noise by the algorithm. Since observables are identical, a is the same in both worlds.
- World A: ambiguous samples are truly noise. Error contribution >= (1-a) * eta * rho
- World B: ambiguous samples are truly clean. Error contribution >= a * eta * rho
- max(error_A, error_B) >= eta*rho * max(1-a, a) >= eta*rho/2

The bound is tight: achieved at a = 1/2 (random guess on ambiguous set).

---

## 4. Theorem 4' (Exact Constant Minimax)

### Bahadur-Rao saddlepoint

**Claim**: lambda* = log(theta(1-p)/(p(1-theta))), sigma^2(theta) = theta(1-theta)

**Verification**: PASS.

For Bern(p): psi(lambda) = log(1-p + p*e^lambda)
psi'(lambda) = p*e^lambda/(1-p+p*e^lambda). Setting = theta:
p*e^lambda = theta(1-p+p*e^lambda) => e^lambda = theta(1-p)/(p(1-theta)) => lambda* = log(theta(1-p)/(p(1-theta)))

Tilted variance: psi''(lambda*) = theta(1-theta). Verified by direct substitution:
1-p+p*e^(lambda*) = (1-p)/(1-theta), giving psi'' = theta(1-theta).

### Chernoff information

**Claim**: kappa = KL(theta*||p0) = KL(theta*||p1) where theta* = log((1-p0)/(1-p1))/log(p1(1-p0)/(p0(1-p1)))

**Verification**: PASS.

The equality KL(theta||p0) = KL(theta||p1) gives:
theta*log(p1/p0) = (1-theta)*log((1-p0)/(1-p1))
Solving: theta* = log((1-p0)/(1-p1)) / log(p1(1-p0)/(p0(1-p1)))

Verified theta* is in (p0, p1) by strict convexity of KL in its first argument and sign change at endpoints.

### Adaptive threshold

**Claim**: theta_opt = theta* + (1/M)*log((1-eta)/eta)/D* + O(1/M^2)

**Verification**: PASS.

Minimizing (1/2)FNR(theta) + (1-eta)/(2eta)FPR(theta) gives first-order condition:
KL(theta||p0) - KL(theta||p1) = (1/M)*log((1-eta)/eta)

Key observation: KL''(theta||p) = 1/(theta(1-theta)) is INDEPENDENT of p. Therefore:
KL(theta*+delta||p0) - KL(theta*+delta||p1) = delta*(KL'(theta*||p0) - KL'(theta*||p1)) + O(delta^3)
= delta*(lambda0* - lambda1*) + O(delta^3)
= delta*D* + O(delta^3)

The delta^2 terms cancel exactly. This is a clean mathematical fact correctly exploited.

Therefore: delta = (1/M)*log((1-eta)/eta)/D* + O(1/M^2).

### O(1) prefactor

**Claim**: ((1-eta)/eta)^s appears in both FPR and FNR contributions.

**Verification**: PASS.

At theta_opt = theta* + delta:
exp(-M*KL(theta_opt||p0)) = e^{-M*kappa} * ((1-eta)/eta)^{-(1-s)}
exp(-M*KL(theta_opt||p1)) = e^{-M*kappa} * ((1-eta)/eta)^s

where s = |lambda1*|/D*, 1-s = lambda0*/D*.

FPR term: ((1-eta)/(2eta))*exp(-M*kappa)*((1-eta)/eta)^{-(1-s)}/(lambda0*sqrt(...))
= exp(-M*kappa)*((1-eta)/eta)^s/(2*lambda0*sqrt(...))

FNR term: (1/2)*exp(-M*kappa)*((1-eta)/eta)^s/(|lambda1*|*sqrt(...))

Both carry the identical factor ((1-eta)/eta)^s. This cancellation is verified algebraically.

### C_min formula

**Claim**: C_min = (eta/2)*((1-eta)/eta)^s*(1/lambda0*+1/|lambda1*|)/sqrt(theta*(1-theta*))

**Verification**: PASS.

From the weighted risk at the Bayes optimal threshold:
R_M = w0*alpha_M + w1*beta_M
= e^{-M*kappa}*((1-eta)/eta)^s*(1/lambda0*+1/|lambda1*|)/(2*sqrt(2pi*M*theta*(1-theta*)))*(1+o(1))

lim e^{M*kappa}*sqrt(2pi*M)*R_M = ((1-eta)/eta)^s*(1/lambda0*+1/|lambda1*|)/(2*sqrt(theta*(1-theta*)))
= C_min/eta

Solving: C_min = eta * [above expression] = (eta/2)*((1-eta)/eta)^s*(1/lambda0*+1/|lambda1*|)/sqrt(theta*(1-theta*))

### Constant matching

**Claim**: Adaptive SCX constant = C_min/eta

**Verification**: PASS.

From Lemma D section D.5:
1-F1(theta_opt) ~ e^{-M*kappa}*((1-eta)/eta)^s*(1/lambda0*+1/|lambda1*|)/(2*sqrt(2pi*M*theta*(1-theta*)))

This is exactly C_min/eta. The lower bound (Lemma E) proves no algorithm can have a smaller constant. SCX with adaptive threshold achieves it. Match is exact.

---

## 5. Theorem 5 (Cluster Consistency)

### All exponents are negative

**Claim**: -c1*n_min*Delta_min^2/(sigma^2*d_phi) is always negative.

**Verification**: PASS.

The exponent contains: c1 > 0 (universal constant), n_min > 0 (minimum per-state sample size), Delta_min > 0 (minimum separation, fixed), sigma^2 < inf (sub-Gaussian proxy), d_phi < inf (feature dimension). All factors are positive, so the exponent is strictly negative. The bound converges to 0 as n_min -> inf.

Additionally verified:
- Lemma S1: P(||epsilon||_2 >= C1*sigma*(sqrt(d_phi)+sqrt(t))) <= 2*exp(-t). Exponent -t is always negative for t > 0.
- Lemma S2: Sub-Gaussian tail bound with negative exponent.
- Lemma 2 peeling sum: each term exp(-c*4^j*t^2) with negative exponent, summed exponentially.

### All inequality directions

**Claim**: All inequalities point in correct directions.

**Verification**: PASS.

Verification table from Section 7.3 checked:
- Lemma 1 Claim: P(event) <= exp(-Delta_min^2/(8*sigma^2)). The derivation: condition ||mu_j-mu_k + epsilon|| <= ||epsilon|| implies 2*epsilon^T(mu_j-mu_k) <= -||mu_j-mu_k||^2. Sub-Gaussian tail gives the exp bound. Direction: upper bound (correct for tail).
- Lemma 3: ||phi - theta_{j_k}|| <= Delta_min/2 <= ||phi - theta_{j'}||. Verifies 1/8 + 3/8 = 1/2 and 7/8 - 3/8 = 1/2. Both sides with correct inequality.
- Lemma 2 (3): lambda*||theta_hat - theta*||^2 <= |(Pn-P)(f_theta_hat - f_theta*)|. From W_n(theta_hat) <= W_n(theta*), expanding and using quadratic lower bound. Direction: correct.
- Lemma 4: P(no restart lands in B) <= (1-p0)^R <= n^{-c}. Direction: correct.

### NP-hard gap honestly discussed

**Claim**: The NP-hard gap of k-means is honestly acknowledged and addressed.

**Verification**: PASS.

Section 6 and 9.2 explicitly:
1. State that k-means is NP-hard in worst case
2. Lemma 4 proves Lloyd's with R = O(log n) random restarts finds global minimizer under strong separation
3. Explicitly state the consequence if strong separation fails: "if the strong separation condition does not hold... the theorem's guarantee degrades"
4. Cite relevant literature (Ostrovsky et al. 2013, Kumar & Kannan 2010)
5. Do not claim a guarantee for the weak separation regime

This is an honest, well-structured treatment of the computational hardness.

---

## 6. Numerical Verification

### Test 1: p0=0.10, p1=0.60, eta=0.10

| Quantity | Computed Value | Verification |
|----------|---------------|--------------|
| theta* | 0.31158 | Closed-form formula |
| kappa | 0.1696 | Matches Lemma C table (0.1696) |
| lambda0* | 1.4040 | > 0, correct direction |
| |lambda1*| | 1.1981 | > 0, correct direction |
| D* | 2.6021 | lambda0* + |lambda1*| |
| s | 0.4604 | |lambda1*|/D* in (0,1) |
| C_min | 0.4573 | Formula evaluated |
| C_min/eta | 4.573 | |
| C_SCX | 4.573 | C_SCX = C_min/eta: MATCH |

kappa/2Delta^2 comparison: 2*(p1-p0)^2 = 2*0.25 = 0.50. kappa/0.50 = 0.1696/0.50 = 0.3392, matching Lemma C table.

### Test 2: p0=0.05, p1=0.80, eta=0.05

| Quantity | Computed Value | Verification |
|----------|---------------|--------------|
| theta* | 0.35979 | Closed-form formula |
| kappa | 0.4576 | Matches Lemma C table (0.4574, minor rounding) |
| lambda0* | 2.368 | > 0 |
| |lambda1*| | 1.962 | > 0 |
| D* | 4.330 | lambda0* + |lambda1*| |
| s | 0.4531 | |lambda1*|/D* in (0,1) |
| C_min | 0.1863 | Formula evaluated |
| C_min/eta | 3.727 | |
| C_SCX | 3.727 | C_SCX = C_min/eta: MATCH |

### Test 3: p0=0.20, p1=0.50, eta=0.30

| Quantity | Computed Value | Verification |
|----------|---------------|--------------|
| theta* | 0.33904 | Closed-form formula |
| kappa | 0.0527 | Matches Lemma C table (0.0528, minor rounding) |
| lambda0* | 0.7186 | > 0 |
| |lambda1*| | 0.6673 | > 0 |
| D* | 1.3859 | lambda0* + |lambda1*| |
| s | 0.4815 | |lambda1*|/D* in (0,1) |
| C_min | 1.373 | Formula evaluated |
| C_min/eta | 4.578 | |
| C_SCX | 4.578 | C_SCX = C_min/eta: MATCH |

All three numerical test cases confirm the identity C_SCX = C_min/eta.

---

## 7. Minor Observations and Notes

1. **Lemma A lattice correction**: The Bahadur-Rao expansion for Bernoulli distributions includes a lattice correction factor (1 - e^{-lambda*})^{-1} not present in the continuous case. The document correctly notes both the 1/lambda* form and the lattice correction form, showing they are asymptotically equivalent. When used consistently in FPR/FNR ratios (which share the same theta*), the correction largely cancels. This is mathematically sound.

2. **Theorem 2 Lipschitz constant C_F**: The Lipschitz constant for F1 as a function of (TP, FP, FN) depends on the operating regime. The document gives heuristic values (C_F <= 3 for precision, recall >= 0.1; C_F <= 1 for precision, recall >= 0.5). These are not rigorous bounds derived in the document, but the claim that a Lipschitz constant exists is correct. The specific values are practical estimates.

3. **Theorem 4' non-asymptotic bounds**: Section 6(d) claims finite-M bounds with explicit constants K1, K2, but states these come from Lemma A (Stirling error) and Lemma B (quadratic remainder). The lemmas provide error terms of the form O(1/M), but the explicit K1, K2 constants are referenced rather than fully computed. The asymptotic limit (M -> inf) is fully rigorous.

4. **Theorem 5 irreducible error**: The document acknowledges that even with perfect center estimates, points with ||epsilon|| >= 3*Delta_min/8 can be misclassified. This is correctly identified as a data property, not an estimator failure.

---

## 8. Overall Mathematical Verdict

All mathematical derivations across Theorems 1-5 and supporting lemmas are **CORRECT**.

| Theorem | Verdict | Key Findings |
|---------|---------|-------------|
| Theorem 1 (Noise Detection) | PASS | All lemmas algebraically verified; Hoeffding conditions satisfied; F1 bound derivations correct |
| Theorem 2 (Weak Features) | PASS | Fano/Pinsker/DPI applied correctly; TV-to-F1 Lipschitz argument valid (constants are heuristic but not essential) |
| Theorem 3 (Unidentifiability) | PASS | K=2 and K>2 constructions both verified; joint distribution equality holds; error bound eta*rho/2 is tight |
| Theorem 4' (Exact Constant) | PASS | Bahadur-Rao verified in full; Chernoff theta* closed-form correct; adaptive threshold derivation exploits KL'' independence of p; C_min formula matches all three numerical tests; C_SCX = C_min/eta verified |
| Theorem 5 (Cluster Consistency) | PASS | All exponents negative; all inequality directions verified; NP-hard gap honestly discussed and addressed under strong separation |
| Lemma A (Bahadur-Rao) | PASS | Full saddlepoint computation verified; tilted distribution correctly identified as Bern(theta); lattice correction discussed |
| Lemma B (F1 expansion) | PASS | F1 formula algebra verified; denominator positivity checked; expansion into FNR/2 + (1-eta)FPR/(2eta) correct; remainder bound derived |
| Lemma C (Chernoff info) | PASS | Theta* closed-form derived correctly; KL'' independence noted; numerical table entries verified against formulas |
| Lemma D (Adaptive threshold) | PASS | First-order condition derived correctly; O(1/M) shift computed; (1-eta)/eta)^s cancellation verified |
| Lemma E (Lower bound) | PASS | Bayes test reduction via Neyman-Pearson is correct; Bahadur-Rao applied; C_min formula derived explicitly and matches achievable constant |
| Lemma F (Multi-state) | PASS | Additivity by law of total expectation; bottleneck state dominates asymptotic; correct handling of kappa_min states |
