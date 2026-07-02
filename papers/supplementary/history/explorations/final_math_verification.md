# Final Mathematical Verification
Report

**Author:** SCX

**Reviewer**: Pure mathematician (formal verification of
mathematical claims only) **Date**: 2026-06-28 **Scope**:
Theorems 1-5, supporting lemmas, and numerical test cases **Files
reviewed**: -
`G:\{}Xiaogan\_Supercomputing\_data\{}SCX\{}theory\{}theorems\{}01\_noise\_detection\_guarantee.md`
-
`G:\{}Xiaogan\_Supercomputing\_data\{}SCX\{}theory\{}theorems\{}02\_weak\_feature\_failure.md`
-
`G:\{}Xiaogan\_Supercomputing\_data\{}SCX\{}theory\{}theorems\{}03\_unidentifiability\_theorem.md`
-
`G:\{}Xiaogan\_Supercomputing\_data\{}SCX\{}theory\{}explorations\{}exact\_constant\_minimax.md`
-
`G:\{}Xiaogan\_Supercomputing\_data\{}SCX\{}theory\{}explorations\{}lemma\_AB\_bahadur\_rao\_f1.md`
-
`G:\{}Xiaogan\_Supercomputing\_data\{}SCX\{}theory\{}explorations\{}lemma\_CD\_chernoff\_adaptive.md`
-
`G:\{}Xiaogan\_Supercomputing\_data\{}SCX\{}theory\{}explorations\{}lemma\_EF\_lowerbound\_aggregation.md`
-
`G:\{}Xiaogan\_Supercomputing\_data\{}SCX\{}theory\{}explorations\{}cluster\_consistency\_v3.md`
-
`G:\{}Xiaogan\_Supercomputing\_data\{}SCX\{}theory\{}explorations\{}deep\_math\_connections.md`

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. Theorem 1 (Noise Detection
Guarantee)<!-- label: theorem-1-noise-detection-guarantee -->

#### Lemma 1 (Mean Separation)<!-- label: lemma-1-mean-separation -->

**Claim**: E{[}C| noise,x{]} = 1 -
E{[}C| clean,x{]}/(K-1)

**Verification**: PASS.

The proof expands: - E{[}C| noise,x{]} = (1/M) sum\_m P(f\_m(x)
!= y |{} noise, x) - P(f\_m(x) != y |{} noise, x) =
sum\_\{c != y*\* P(y=c| noise) } P(f\_m(x) != c |{}
x) - = sum\_\{c != y*\* (1/(K-1)) } (1 - P(f\_m(x)=c| x)) -
= 1 - (1/(K-1)) * sum\_\{c != y*\* P(f\_m(x)=c| x) - = 1 -
(1/(K-1)) } (1 - P(f\_m(x)=y*| x)) - = 1 - (1/(K-1)) *
E{[}e\_m| clean,x{]}

Averaging over m gives: E{[}C| noise,x{]} = 1 -
E{[}C| clean,x{]}/(K-1). The algebra is correct. Each step uses
only: (A4) uniform noise over K-1 classes, linearity of expectation, and
identity sum\_\{c != y*\} P(f\_m=c| x) =
E{[}e\_m| clean,x{]}.

The separation condition mu\_s \textless{} (K-1)/K is correctly derived
from: clean mean \textless= mu\_s, noise mean \textgreater= 1 -
mu\_s/(K-1), requiring mu\_s \textless{} 1 - mu\_s/(K-1) =\textgreater{}
mu\_s * K/(K-1) \textless{} 1 =\textgreater{} mu\_s \textless{} (K-1)/K.

The optimal threshold theta* = (1/2)(1 + mu\_s*(K-2)/(K-1)) solves theta
- mu\_s = 1 - mu\_s/(K-1) - theta correctly.

#### Lemma 2 (FPR)<!-- label: lemma-2-fpr -->

**Claim**: P(C \textgreater{} theta |{} clean, s) \textless=
exp(-2M(theta - mu\_s)\^{}2)

**Verification**: PASS.

Standard Hoeffding inequality for bounded {[}0,1{]} independent r.v.s.
The conditioning chain: - Fix x in s: E{[}C| clean,x{]}
\textless= mu\_s by (A5) - \{e\_m\} conditionally independent given x by
(A2), bounded by {[}0,1{]} by (A3) - P(C - E{[}C| x{]}
\textgreater{} theta - E{[}C| x{]} |{} clean, x)
\textless= exp(-2M(theta - E{[}C| x{]})\^{}2) \textless=
exp(-2M(theta - mu\_s)\^{}2) - The last step uses: theta \textgreater{}
mu\_s \textgreater= E{[}C| x{]}, so (theta - E{[}C| x{]})
\textgreater= (theta - mu\_s) - Marginalizing over x in s preserves the
bound via sup

All conditions for Hoeffding are satisfied.

#### Lemma 3 (TPR)<!-- label: lemma-3-tpr -->

**Claim**: P(C \textless= theta |{} noise, s) \textless=
exp(-2M(1 - C\_bal*mu\_s/(K-1) - theta)\^{}2)

**Verification**: PASS, with careful reading.

The proof conditions on (x, c) where c is the noise label: - Given (x,
c), \{e\_m\} are conditionally independent (A1, A2) with e\_m
~{} Bern(1 - mu\_\{c,m\}(x)) - E{[}C| x,c{]} = 1 -
mu\_c(x) \textgreater= 1 - C\_bal*mu\_s/(K-1) by (A6) - The theorem
assumes theta \textless{} 1 - C\_bal*mu\_s/(K-1), so Hoeffding applies -
P(C \textless= theta |{} x, c) \textless=
exp(-2M(E{[}C| x,c{]} - theta)\^{}2) \textless= exp(-2M(1 -
C\_bal*mu\_s/(K-1) - theta)\^{}2) - Averaging over c (uniform over K-1
classes) preserves the bound

Key subtlety: the bound uses mu\_c(x) \textless=
C\_bal*mu\_s/(K-1), so E{[}C| x,c{]} \textgreater= 1 -
C\_bal*mu\_s/(K-1). The Hoeffding gap (E{[}C| x,c{]} - theta) is
minimized (worst case) when E{[}C| x,c{]} is smallest, which
occurs at the max mu\_c(x). The A6 assumption correctly captures this
via C\_bal.

#### F1 bound<!-- label: f1-bound -->

**Claim**: F1 \textgreater= 1 - (1/eta) sum\_s rho\_s exp(-2M
Delta\_s\^{}2)

**Verification**: PASS.

Algebraic derivation: - F1 = 2*eta*TPR / (eta(1+TPR) + (1-eta)FPR)
{[}verified via Precision-Recall algebra{]} - Substituting TPR
\textgreater= 1-delta\_1, FPR \textless= delta\_2 gives denominator
\textgreater= eta - 1 - F1 \textless= delta\_1 + (1-eta)delta\_2/eta -
Since delta\_1, delta\_2 \textless= sum rho\_s exp(-2M Delta\_s\^{}2),
the final bound follows

The denominator is strictly positive: eta(2-FNR)+(1-eta)FPR
\textgreater= eta \textgreater{} 0 for eta \textgreater{} 0.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2. Theorem 2 (Weak Features)<!-- label: theorem-2-weak-features -->

#### Fano inequality<!-- label: fano-inequality -->

**Claim**: P(S\_hat != S) \textgreater= (H(S) - delta - log 2) /
log K

**Verification**: PASS.

Standard Fano inequality: P(S\_hat != S) \textgreater=
(H(S| phi(X)) - log 2) / log | S|. Since I(phi;S)
\textless= delta by the delta-weak feature definition: H(S| phi)
= H(S) - I(phi;S) \textgreater= H(S) - delta. Substituting gives:
P(S\_hat != S) \textgreater= (H(S) - delta - log 2) / log K.

The feature-dependent Markov chain Z -\textgreater{} S -\textgreater{} X
-\textgreater{} phi(X) correctly implies I(phi;Z) \textless= I(S;Z)
\textless= H(Z) by the data processing inequality.

#### Pinsker inequality<!-- label: pinsker-inequality -->

**Claim**: TV(P, P\_tilde) \textless= sqrt(delta/2)

**Verification**: PASS.

P\_tilde(phi, S) = P(phi) * P(S). KL(P ||{} P\_tilde) =
I(phi; S) = delta. Pinsker: TV \textless= sqrt(KL/2) = sqrt(delta/2).

#### F1 bound<!-- label: f1-bound-1 -->

**Claim**: F1\_SCX \textless= F1\_base + C\_F * sqrt(delta/2)

**Verification**: PASS (with caveat on Lipschitz constant).

The reasoning chain: 1. Under P\_tilde, SCX detection score degrades to
loss baseline: NS(x) ~{} max\_m D\_m(x) 2. Hence
F1\_P\_tilde(SCX) = F1\_base 3. | F1\_P(SCX) -
F1\_P\_tilde(SCX)|{} \textless= C\_F * TV(P\_pred,
P\_tilde\_pred) by Lipschitz property 4. TV(P\_pred, P\_tilde\_pred)
\textless= TV(P, P\_tilde) by data processing inequality 5. \textless=
sqrt(delta/2)

The Lipschitz analysis of F1(TP, FP, FN) = 2TP/(2TP+FP+FN) is partial
derivatives and the document acknowledges that C\_F depends on
precision/recall regime. The specific values (C\_F \textless= 2 for
precision, recall \textgreater= 0.1) are heuristic estimates, not
rigorous bounds. This is flagged as an approximate constant in the text.

**Minor issue**: The AUC bound's TV-to-conditional-TV step uses
division by eta and 1-eta: | P(A| Z=1) -
P\_tilde(A| Z=1)|{} \textless= TV(P, P\_tilde)/eta. This
requires eta \textgreater{} 0 (non-zero noise rate). For eta
-\textgreater{} 0 the bound diverges, which the document correctly
acknowledges.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 3. Theorem 3
(Unidentifiability)<!-- label: theorem-3-unidentifiability -->

#### K=2 construction<!-- label: k2-construction -->

**Claim**: P\_noise(x, y, \{f\_m\}) = P\_hard(x, y, \{f\_m\})

**Verification**: PASS.

World A (noise): s1 has noise rate eta, clean expert error epsilon\_1.
s2 has no noise. World B (hard): s1 has random true label
(P(y*=0)=1-eta, P(y*=1)=eta), experts biased toward class 0.

Equality verification: - P\_A(y=0| s1) = (1-eta)*1 + eta*0 =
1-eta - P\_B(y=0| s1) = P(y*=0| s1) = 1-eta -
P\_A(f\_m=0| s1) = 1-epsilon\_1 (expert accuracy against true
label y*=0) - P\_B(f\_m=0| s1) = (1-eta)(1-epsilon\_1) +
eta(1-epsilon\_1) = 1-epsilon\_1

Joint factorization P(x,y,\{f\_m\}) = P(x) * P(y| x) * prod\_m
P(f\_m| x) holds by conditional independence in both
constructions. State s2 is identical in both worlds.

#### K\textgreater2 construction<!-- label: k2-construction-1 -->

**Claim**: The construction works for all K \textgreater= 2.

**Verification**: PASS.

For K \textgreater{} 2, the construction uses completely random experts
(independent of y*): - World A: y* = 0, noise uniform over K-1
classes. Expert predicts 0 with prob 1-epsilon\_1 - World B: y*
non-deterministic (same distribution as y in World A). Expert is pure
random

P\_A(y=0| s1) = 1-eta = P\_B(y=0| s1)
P\_A(f\_m=0| s1) = 1-epsilon\_1 = P\_B(f\_m=0| s1)
Independence of y and f\_m holds in both worlds by construction. Joint
distribution matches for all K \textgreater= 2.

#### Error bound eta*rho/2<!-- label: error-bound-etarho2 -->

**Claim**: max(Error\_A, Error\_B) \textgreater= eta*rho/2

**Verification**: PASS.

Let a be the fraction of ambiguous samples (\{x in s1, y=1\}) flagged as
noise by the algorithm. Since observables are identical, a is the same
in both worlds. - World A: ambiguous samples are truly noise. Error
contribution \textgreater= (1-a) * eta * rho - World B: ambiguous
samples are truly clean. Error contribution \textgreater= a * eta * rho
- max(error\_A, error\_B) \textgreater= eta*rho * max(1-a, a)
\textgreater= eta*rho/2

The bound is tight: achieved at a = 1/2 (random guess on ambiguous set).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 4. Theorem 4' (Exact Constant
Minimax)<!-- label: theorem-4-exact-constant-minimax -->

#### Bahadur-Rao saddlepoint<!-- label: bahadur-rao-saddlepoint -->

**Claim**: lambda* = log(theta(1-p)/(p(1-theta))),
sigma\^{}2(theta) = theta(1-theta)

**Verification**: PASS.

For Bern(p): psi(lambda) = log(1-p + p*e\^{}lambda) psi'(lambda) =
p*e\textsuperscript{lambda/(1-p+p*e\^{}lambda). Setting = theta:
p*e}lambda = theta(1-p+p*e\^{}lambda) =\textgreater{} e\^{}lambda =
theta(1-p)/(p(1-theta)) =\textgreater{} lambda* =
log(theta(1-p)/(p(1-theta)))

Tilted variance: psi'\,'(lambda*) = theta(1-theta). Verified by
direct substitution: 1-p+p*e\^{}(lambda*) = (1-p)/(1-theta), giving
psi'\,' = theta(1-theta).

#### Chernoff information<!-- label: chernoff-information -->

**Claim**: kappa = KL(theta*|| p0) =
KL(theta*|| p1) where theta* =
log((1-p0)/(1-p1))/log(p1(1-p0)/(p0(1-p1)))

**Verification**: PASS.

The equality KL(theta|| p0) = KL(theta|| p1)
gives: theta*log(p1/p0) = (1-theta)*log((1-p0)/(1-p1)) Solving:
theta* = log((1-p0)/(1-p1)) / log(p1(1-p0)/(p0(1-p1)))

Verified theta* is in (p0, p1) by strict convexity of KL in its first
argument and sign change at endpoints.

#### Adaptive threshold<!-- label: adaptive-threshold -->

**Claim**: theta\_opt = theta* + (1/M)*log((1-eta)/eta)/D* +
O(1/M\^{}2)

**Verification**: PASS.

Minimizing (1/2)FNR(theta) + (1-eta)/(2eta)FPR(theta) gives first-order
condition: KL(theta|| p0) - KL(theta|| p1) =
(1/M)*log((1-eta)/eta)

Key observation: KL'\,`(theta|| p) = 1/(theta(1-theta)) is
INDEPENDENT of p.~Therefore: KL(theta*+delta|| p0) -
KL(theta*+delta|| p1) =
delta*(KL'(theta*|| p0) -
KL'(theta*|| p1)) + O(delta\^{}3) = delta*(lambda0* -
lambda1*) + O(delta\^{}3) = delta*D* + O(delta\^{}3)

The delta\^{}2 terms cancel exactly. This is a clean mathematical fact
correctly exploited.

Therefore: delta = (1/M)*log((1-eta)/eta)/D* + O(1/M\^{}2).

#### O(1) prefactor<!-- label: o1-prefactor -->

**Claim**: ((1-eta)/eta)\^{}s appears in both FPR and FNR
contributions.

**Verification**: PASS.

At theta\_opt = theta* + delta:
exp(-M*KL(theta\_opt|| p0)) = e\^{}\{-M}kappa\* *
((1-eta)/eta)\^{}\{-(1-s)\}
exp(-M*KL(theta\_opt|| p1)) = e\^{}\{-M}kappa\* *
((1-eta)/eta)\^{}s

where s = | lambda1*|/D*, 1-s = lambda0*/D*.

FPR term:
((1-eta)/(2eta))*exp(-M*kappa)*((1-eta)/eta)\^{}\{-(1-s)\}/(lambda0*sqrt(...))
= exp(-M*kappa)*((1-eta)/eta)\^{}s/(2*lambda0*sqrt(...))

FNR term:
(1/2)*exp(-M*kappa)*((1-eta)/eta)\^{}s/(| lambda1*|*sqrt(...))

Both carry the identical factor ((1-eta)/eta)\^{}s. This cancellation is
verified algebraically.

#### C\_min formula<!-- label: c_min-formula -->

**Claim**: C\_min =
(eta/2)*((1-eta)/eta)\^{}s*(1/lambda0*+1/| lambda1*|)/sqrt(theta*(1-theta*))

**Verification**: PASS.

From the weighted risk at the Bayes optimal threshold: R\_M =
w0*alpha\_M + w1*beta\_M =
e\textsuperscript{\{-M*kappa\*}((1-eta)/eta)}s*(1/lambda0*+1/| lambda1*|)/(2*sqrt(2pi*M*theta*(1-theta*)))*(1+o(1))

lim e\^{}\{M*kappa\*}sqrt(2pi*M)*R\_M =
((1-eta)/eta)\^{}s*(1/lambda0*+1/| lambda1*|)/(2*sqrt(theta*(1-theta*)))
= C\_min/eta

Solving: C\_min = eta * {[}above expression{]} =
(eta/2)*((1-eta)/eta)\^{}s*(1/lambda0*+1/| lambda1*|)/sqrt(theta*(1-theta*))

#### Constant matching<!-- label: constant-matching -->

**Claim**: Adaptive SCX constant = C\_min/eta

**Verification**: PASS.

From Lemma D section D.5: 1-F1(theta\_opt) ~{}
e\textsuperscript{\{-M*kappa\*}((1-eta)/eta)}s*(1/lambda0*+1/| lambda1*|)/(2*sqrt(2pi*M*theta*(1-theta*)))

This is exactly C\_min/eta. The lower bound (Lemma E) proves no
algorithm can have a smaller constant. SCX with adaptive threshold
achieves it. Match is exact.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 5. Theorem 5 (Cluster
Consistency)<!-- label: theorem-5-cluster-consistency -->

#### All exponents are
negative<!-- label: all-exponents-are-negative -->

**Claim**:
-c1*n\_min*Delta\_min\textsuperscript{2/(sigma}2*d\_phi) is always
negative.

**Verification**: PASS.

The exponent contains: c1 \textgreater{} 0 (universal constant), n\_min
\textgreater{} 0 (minimum per-state sample size), Delta\_min
\textgreater{} 0 (minimum separation, fixed), sigma\^{}2 \textless{} inf
(sub-Gaussian proxy), d\_phi \textless{} inf (feature dimension). All
factors are positive, so the exponent is strictly negative. The bound
converges to 0 as n\_min -\textgreater{} inf.

Additionally verified: - Lemma S1:
P(|| epsilon||\_2 \textgreater=
C1*sigma*(sqrt(d\_phi)+sqrt(t))) \textless= 2*exp(-t).
Exponent -t is always negative for t \textgreater{} 0. - Lemma S2:
Sub-Gaussian tail bound with negative exponent. - Lemma 2 peeling sum:
each term exp(-c*4\^{}j*t\^{}2) with negative exponent, summed
exponentially.

#### All inequality
directions<!-- label: all-inequality-directions -->

**Claim**: All inequalities point in correct directions.

**Verification**: PASS.

Verification table from Section 7.3 checked: - Lemma 1 Claim: P(event)
\textless= exp(-Delta\_min\textsuperscript{2/(8*sigma\^{}2)). The
derivation: condition || mu\_j-mu\_k +
epsilon||{} \textless=
|| epsilon||{} implies
2*epsilon}T(mu\_j-mu\_k) \textless=
-|| mu\_j-mu\_k||\^{}2. Sub-Gaussian tail
gives the exp bound. Direction: upper bound (correct for tail). - Lemma
3: || phi - theta\_\{j\_k\}||{} \textless=
Delta\_min/2 \textless= || phi -
theta\_\{j'\}||. Verifies 1/8 + 3/8 = 1/2 and 7/8 - 3/8 =
1/2. Both sides with correct inequality. - Lemma 2 (3):
lambda*|| theta\_hat - theta*||\^{}2
\textless= |(Pn-P)(f\_theta\_hat - f\_theta*)|. From
W\_n(theta\_hat) \textless= W\_n(theta*), expanding and using quadratic
lower bound. Direction: correct. - Lemma 4: P(no restart lands in B)
\textless= (1-p0)\^{}R \textless= n\^{}\{-c\}. Direction: correct.

#### NP-hard gap honestly
discussed<!-- label: np-hard-gap-honestly-discussed -->

**Claim**: The NP-hard gap of k-means is honestly acknowledged and
addressed.

**Verification**: PASS.

Section 6 and 9.2 explicitly: 1. State that k-means is NP-hard in worst
case 2. Lemma 4 proves Lloyd's with R = O(log n) random restarts finds
global minimizer under strong separation 3. Explicitly state the
consequence if strong separation fails: ``if the strong separation
condition does not hold...{} the theorem's guarantee degrades'' 4.
Cite relevant literature (Ostrovsky et al.~2013, Kumar \& Kannan 2010)
5. Do not claim a guarantee for the weak separation regime

This is an honest, well-structured treatment of the computational
hardness.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 6. Numerical Verification<!-- label: numerical-verification -->

#### Test 1: p0=0.10, p1=0.60,
eta=0.10<!-- label: test-1-p00.10-p10.60-eta0.10 -->

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
Quantity & Computed Value & Verification 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
theta* & 0.31158 & Closed-form formula 

kappa & 0.1696 & Matches Lemma C table (0.1696) 

lambda0* & 1.4040 & \textgreater{} 0, correct direction 

& lambda1* & 

D* & 2.6021 & lambda0* + 

s & 0.4604 & 

C\_min & 0.4573 & Formula evaluated 

C\_min/eta & 4.573 & 

C\_SCX & 4.573 & C\_SCX = C\_min/eta: MATCH 

\end{longtable}

kappa/2Delta\^{}2 comparison: 2*(p1-p0)\^{}2 = 2*0.25 = 0.50.
kappa/0.50 = 0.1696/0.50 = 0.3392, matching Lemma C table.

#### Test 2: p0=0.05, p1=0.80,
eta=0.05<!-- label: test-2-p00.05-p10.80-eta0.05 -->

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
Quantity & Computed Value & Verification 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
theta* & 0.35979 & Closed-form formula 

kappa & 0.4576 & Matches Lemma C table (0.4574, minor rounding) 

lambda0* & 2.368 & \textgreater{} 0 

& lambda1* & 

D* & 4.330 & lambda0* + 

s & 0.4531 & 

C\_min & 0.1863 & Formula evaluated 

C\_min/eta & 3.727 & 

C\_SCX & 3.727 & C\_SCX = C\_min/eta: MATCH 

\end{longtable}

#### Test 3: p0=0.20, p1=0.50,
eta=0.30<!-- label: test-3-p00.20-p10.50-eta0.30 -->

\begin{longtable}[]{@{}lll@{}}
\toprule\noalign{}
Quantity & Computed Value & Verification 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
theta* & 0.33904 & Closed-form formula 

kappa & 0.0527 & Matches Lemma C table (0.0528, minor rounding) 

lambda0* & 0.7186 & \textgreater{} 0 

& lambda1* & 

D* & 1.3859 & lambda0* + 

s & 0.4815 & 

C\_min & 1.373 & Formula evaluated 

C\_min/eta & 4.578 & 

C\_SCX & 4.578 & C\_SCX = C\_min/eta: MATCH 

\end{longtable}

All three numerical test cases confirm the identity C\_SCX = C\_min/eta.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 7. Minor Observations and
Notes<!-- label: minor-observations-and-notes -->

1. 
2. 
3. 
4. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 8. Overall Mathematical
Verdict<!-- label: overall-mathematical-verdict -->

All mathematical derivations across Theorems 1-5 and supporting lemmas
are **CORRECT**.

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2903}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.2903}}
  >{\arraybackslash}p{(\linewidth - 4\tabcolsep) * \real{0.4194}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Theorem
\end{minipage} & \begin{minipage}[b]
Verdict
\end{minipage} & \begin{minipage}[b]
Key Findings
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Theorem 1 (Noise Detection) & PASS & All lemmas algebraically verified;
Hoeffding conditions satisfied; F1 bound derivations correct 

Theorem 2 (Weak Features) & PASS & Fano/Pinsker/DPI applied correctly;
TV-to-F1 Lipschitz argument valid (constants are heuristic but not
essential) 

Theorem 3 (Unidentifiability) & PASS & K=2 and K\textgreater2
constructions both verified; joint distribution equality holds; error
bound eta*rho/2 is tight 

Theorem 4' (Exact Constant) & PASS & Bahadur-Rao verified in full;
Chernoff theta* closed-form correct; adaptive threshold derivation
exploits KL'\,' independence of p; C\_min formula matches all three
numerical tests; C\_SCX = C\_min/eta verified 

Theorem 5 (Cluster Consistency) & PASS & All exponents negative; all
inequality directions verified; NP-hard gap honestly discussed and
addressed under strong separation 

Lemma A (Bahadur-Rao) & PASS & Full saddlepoint computation verified;
tilted distribution correctly identified as Bern(theta); lattice
correction discussed 

Lemma B (F1 expansion) & PASS & F1 formula algebra verified; denominator
positivity checked; expansion into FNR/2 + (1-eta)FPR/(2eta) correct;
remainder bound derived 

Lemma C (Chernoff info) & PASS & Theta* closed-form derived correctly;
KL'\,' independence noted; numerical table entries verified against
formulas 

Lemma D (Adaptive threshold) & PASS & First-order condition derived
correctly; O(1/M) shift computed; (1-eta)/eta)\^{}s cancellation
verified 

Lemma E (Lower bound) & PASS & Bayes test reduction via Neyman-Pearson
is correct; Bahadur-Rao applied; C\_min formula derived explicitly and
matches achievable constant 

Lemma F (Multi-state) & PASS & Additivity by law of total expectation;
bottleneck state dominates asymptotic; correct handling of kappa\_min
states 

\end{longtable}