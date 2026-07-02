\section{Review: Minimax Lower Bound v2 (Hellinger Distance
Proof)}<!-- label: review-minimax-lower-bound-v2-hellinger-distance-proof -->

> **File reviewed**:
> `G:\{}Xiaogan\_Supercomputing\_data\{}SCX\{}theory\{}explorations\{}minimax\_lower\_bound\_v2.md`
> 
> **Review date**: 2026-06-27
> 
> **Scope**: Full mathematical verification of all inequalities,
> formulas, and derivations. Numerical cross-checking of all claimed
> relationships.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 1. Overall Verdict<!-- label: overall-verdict -->

The proof correctly fixes the three fatal issues from v1 (Slud's
inequality, chi-squared direction, F1 algebra), and the core Hellinger
tensorization approach is sound. **However, two new fatal errors
have been introduced in the F1 conversion section** (Section 7), and a
significant formula error appears in the K \textgreater{} 2 section
(Section 8.3).

**Bottom line**: The testing error lower bound (Part a) is correct.
The F1 lower bound (Part b) has two algebraic errors that invalidate its
stated constant. The rate optimality claim (Part c) remains correct
because the exponential rate `exp(-2MDelta\^{}2)` is preserved
under the corrected analysis.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

### 2. Issues Found<!-- label: issues-found -->

#### Issue 1 {[FATAL{]}: Section 7.3 -- Backwards inequality
in F1
simplification}<!-- label: issue-1-fatal-section-7.3-backwards-inequality-in-f1-simplification -->

**Location**: Lines 423-427

**Claim**:

\begin{verbatim}
(1-eta)*(rho^M/4)/(2eta+(1-eta)*(rho^M/4)) >= (1-eta)*rho^M/(8eta)
\end{verbatim}

**What is wrong**: The inequality is backwards. Since
`2eta\ +\ (1-eta)*(rho\^{}M/4)\ \textgreater{}\ 2eta` for any
positive `rho\^{}M`, the left-hand side has a larger denominator
with the same numerator, making it strictly smaller. The correct
inequality is `\textless{}=`, not `\textgreater{}=`.

**Verification** (eta = 0.3, rho\^{}M = 0.1):

\begin{verbatim}
LHS = 0.7*0.025/(0.6+0.7*0.025) = 0.02834
RHS = 0.7*0.1/(8*0.3) = 0.02917
LHS < RHS, so LHS >= RHS is FALSE.
\end{verbatim}

**Consequence**: The simplified bound
`1-F1\ \textgreater{}=\ rho\^{}M/(16eta)` is not validly derived.
The correct inequality direction gives an upper bound
`LHS\ \textless{}=\ RHS`, which is useless for lower-bounding
1-F1.

**How to fix**: The exact bound must be kept in its unsimplified
form:

\begin{verbatim}
1-F1 >= (1-eta)(rho^M/4)/(2eta+(1-eta)(rho^M/4))
\end{verbatim}

Or a correct simplification with a multiplicative correction:

\begin{verbatim}
1-F1 >= (1-eta)*rho^M/(8eta) * (1 - (1-eta)*rho^M/(4eta))
\end{verbatim}

(using `1/(1+x)\ \textgreater{}=\ 1-x` for
`x\ \textgreater{}=\ 0`)

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

#### Issue 2 {[FATAL{]}: Section 7.5 -- Wrong case selected
as tighter
bound}<!-- label: issue-2-fatal-section-7.5-wrong-case-selected-as-tighter-bound -->

**Location**: Lines 439-467

**Claim**:

\begin{verbatim}
eps/2 >= (1-eta)*eps/(2eta+(1-eta)*eps) for eta <= 1/2
\end{verbatim}

And consequently:

\begin{verbatim}
min(eps/(2-eps), (1-eta)*eps/(2eta+(1-eta)*eps)) = (1-eta)*eps/(2eta+(1-eta)*eps)
\end{verbatim}

**What is wrong**: The inequality direction is reversed for
`eta\ \textless{}\ 1/2` and small `eps` (the regime of
interest). The proof attempts to verify this by cross-multiplication,
claiming:

`2eta\ +\ (1-eta)*eps\ \textgreater{}=\ 2*(1-eta)` follows from
`eps\ \textgreater{}=\ 0,\ eta\ \textgreater{}=\ 0`.

But the correct cross-multiplication is:

\begin{verbatim}
eps/2 >= (1-eta)*eps/(2eta+(1-eta)*eps)
=> 2eta + (1-eta)*eps >= 2*(1-eta)
=> (1-eta)*eps >= 2 - 4eta
\end{verbatim}

For `eta\ =\ 0.3`: requires
`eps\ \textgreater{}=\ 0.8/0.7\ ≈\ 1.14`. Impossible since
`eps\ \textless{}=\ 1` (and typically
`eps\ \textless{}\textless{}\ 1`). For `eta\ =\ 0.4`:
requires `eps\ \textgreater{}=\ 0.4/0.6\ ≈\ 0.667`. Possible but
atypical -- rho\^{}M would need to be \textgreater= 2.67, impossible
since rho \textless= 1. For `eta\ =\ 0.49`: requires
`eps\ \textgreater{}=\ 0.04/0.51\ ≈\ 0.078`. Possible for some
parameters. For `eta\ =\ 0.5`: requires
`eps\ \textgreater{}=\ 0`. True.

So the claim only holds when
`(1-eta)*eps\ \textgreater{}=\ 2-4eta`, i.e., when
`eta\ \textgreater{}=\ 1/(2-eps/(1-eps))` approximately. For most
of the parameter space (especially small `eps` and
small-to-moderate `eta`), the claim is FALSE.

**Verification** (eta = 0.3, eps = 0.1):

\begin{verbatim}
eps/2 = 0.05
(1-eta)*eps/(2eta+(1-eta)*eps) = 0.7*0.1/0.67 ≈ 0.104
So eps/2 < case2_bound, not >=.
\end{verbatim}

The correct minimum is:
`min(eps/(2-eps),\ (1-eta)*eps/(2eta+(1-eta)*eps))\ =\ eps/(2-eps)`
(Case 1)

for all `eta\ \textless{}\ 1/2` and small `eps`.

**Consequence**: The claimed universal bound
`1-F1\ \textgreater{}=\ (1-eta)*eps/(2eta+(1-eta)*eps)` is
invalid. The correct universal bound uses Case 1:

\begin{verbatim}
1-F1 >= eps/(2-eps) = rho^M/(8-rho^M)
\end{verbatim}

which is approximately `rho\^{}M/8` (not
`rho\^{}M/(16eta)`).

**Comparison of bounds**:

\begin{verbatim}
eta=0.1: correct=rho^M/8, claimed=rho^M/1.6  (claimed 5x too large)
eta=0.3: correct=rho^M/8, claimed=rho^M/4.8  (claimed 1.67x too large)
eta=0.5: correct=rho^M/8, claimed=rho^M/8    (match at eta=0.5)
\end{verbatim}

**How to fix**: Use the Case 1 bound:

\begin{verbatim}
1-F1 >= eps/(2-eps) = (rho^M/4)/(2-rho^M/4) = rho^M/(8-rho^M)
\end{verbatim}

For the simplified form (small rho\^{}M):

\begin{verbatim}
1-F1 >= rho^M/8
\end{verbatim}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

#### Issue 3 {[MAJOR{]}: Section 8.3 -- Incorrect Hellinger
affinity formula for K \textgreater{}
2}<!-- label: issue-3-major-section-8.3-incorrect-hellinger-affinity-formula-for-k-2 -->

**Location**: Line 511

**Claim**:

\begin{verbatim}
rho_K = 2*sqrt(mu_s * (1 - mu_s/(K-1)))
\end{verbatim}

**What is wrong**: This formula is only correct for K=2. The
general Hellinger affinity for `Bernoulli(p)` vs
`Bernoulli(q)` is:

\begin{verbatim}
rho = sqrt(p*q) + sqrt((1-p)*(1-q))
\end{verbatim}

The proof's formula `2*sqrt(p*q)` only matches the general
formula when `q\ =\ 1-p`, i.e., when `K=2` (since
`1\ -\ mu\_s/(K-1)\ =\ 1\ -\ mu\_s\ =\ 1\ -\ p` only when
`K=2`).

For K \textgreater{} 2, the correct formula is:

\begin{verbatim}
rho_K = sqrt(mu_s * (1 - mu_s/(K-1))) + sqrt((1-mu_s) * (mu_s/(K-1)))
\end{verbatim}

**Verification** (mu\_s = 0.3, K = 3):

\begin{verbatim}
correct: sqrt(0.3*0.85) + sqrt(0.7*0.15) = 0.505 + 0.324 = 0.829
wrong:   2*sqrt(0.3*0.85) = 2*0.505 = 1.010
\end{verbatim}

The wrong formula gives `rho\ \textgreater{}\ 1` for many
parameter values (e.g., mu=0.3, K=3: rho=1.010; mu=0.2, K=5: rho=0.872).
While `rho\ \textless{}=\ 1` should always hold for Hellinger
affinity. The correct formula always satisfies
`rho\ \textless{}=\ 1`.

**Consequence**: The numerical values and asymptotic expressions
for K \textgreater{} 2 are wrong. However, the **conclusion** that
K=2 is the hardest case is still correct (verified with the correct
formula -- rho\_K \textless{} rho\_2 for K \textgreater{} 2, giving a
weaker bound, so K=2 gives the strongest valid lower bound for all K
\textgreater= 2).

**How to fix**: Replace the formula with the correct expression:

\begin{verbatim}
rho_K = sqrt(mu_s * (1 - mu_s/(K-1))) + sqrt((1-mu_s) * (mu_s/(K-1)))
\end{verbatim}

And note that
`rho\_K\ \textless{}\ rho\_2\ =\ 2*sqrt(mu\_s*(1-mu\_s))` for all
K \textgreater{} 2, which can be verified by squaring both sides.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

#### Issue 4 {[MAJOR{]}: Section 11 -- Chernoff exactness
claim fails for K \textgreater{}
2}<!-- label: issue-4-major-section-11-chernoff-exactness-claim-fails-for-k-2 -->

**Location**: Lines 676-681

**Claim**:

\begin{verbatim}
-log(rho) = KL(1/2 || mu_s) = Chernoff exponent
\end{verbatim}

**What is wrong**: This holds for K=2 because the likelihood ratio
`dP1/dP0` is symmetric on the log scale (values are reciprocals).
For K \textgreater{} 2, the optimal Chernoff exponent generally uses a
tilting parameter `t\ !=\ 1/2`, so
`-log(rho\_K)\ \textgreater{}\ KL(1/2\ |{}|{}\ mu\_s)`.
The Hellinger exponent `-log(rho\_K)` is still a valid lower
bound on the Chernoff exponent, but it is **not exact**.

**Verification** (mu=0.3, K=3):

\begin{verbatim}
-log(rho_K) = -log(0.829) = 0.188
KL(1/2||0.3) = 0.087
-0.188 != 0.087.
\end{verbatim}

**Consequence**: The claim that the Hellinger approach gives
``exact Chernoff exponent'' is true only for K=2 (or more generally,
when the two distributions are symmetric on the log-odds scale). For K
\textgreater{} 2, the Hellinger exponent is a valid but non-exact lower
bound.

**How to fix**: Clarify that the Chernoff exactness holds for K=2
and provide the general expression for K \textgreater{} 2, or simply
note that the Hellinger bound is always valid and the exponent is
bounded below by the K=2 exponent.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

#### Issue 5 {[MAJOR{]}: Section 9 -- C\_bal \textgreater{} 1
extension is
incomplete}<!-- label: issue-5-major-section-9-c_bal-1-extension-is-incomplete -->

**Location**: Lines 536-619

**What is wrong**: The section is a sketch, not a rigorous proof.
There are several gaps:

1. 
2. 
3. 

**Consequence**: The Theorem 4 statement claims to hold under
(A1)-(A6) without requiring C\_bal = 1, but the proof only fully handles
C\_bal = 1. The C\_bal \textgreater{} 1 case is not rigorously proven.

**How to fix**: Either (a) add C\_bal = 1 as an explicit condition
in the theorem statement, or (b) provide a complete derivation for
C\_bal \textgreater{} 1. Option (b) would involve bounding the average
Hellinger affinity:

\begin{verbatim}
(1/L) sum_ell rho_ell^M >= min_ell rho_ell^M
\end{verbatim}

where
`rho\_ell\ =\ sqrt(mu\_s\ *\ p\_ell)\ +\ sqrt((1-mu\_s)\ *\ (1-p\_ell))`
and `p\_ell\ =\ 1\ -\ C\_ell*mu\_s/(K-1)` for some
`C\_ell\ \textgreater{}=\ 1`. The smallest `rho\_ell`
(closest to 1) gives the weakest bound, and this is attained at
`C\_ell\ =\ C\_bal` (or similar).

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

#### Issue 6 {[MINOR{]}: Section 6.4 -- Wrong Taylor
coefficient for
Delta\^{}4}<!-- label: issue-6-minor-section-6.4-wrong-taylor-coefficient-for-delta4 -->

**Location**: Lines 340-344

**Claim**:

\begin{verbatim}
log(1-4Delta^2) = -4Delta^2 - 8Delta^4/3 - O(Delta^6)
\end{verbatim}

**What is wrong**: The Taylor expansion of
`log(1-x)\ =\ -x\ -\ x\^{}2/2\ -\ x\^{}3/3\ -\ ...` with
`x\ =\ 4Delta\^{}2` gives:

\begin{verbatim}
log(1-4Delta^2) = -4Delta^2 - (4Delta^2)^2/2 - (4Delta^2)^3/3 - ...
               = -4Delta^2 - 16Delta^4/2 - 64Delta^6/3 - ...
               = -4Delta^2 - 8Delta^4 - O(Delta^6)
\end{verbatim}

The coefficient of `Delta\^{}4` is `-8`, not
`-8/3`.

Then
`(M/2)*log(1-4Delta\^{}2)\ =\ -2M*Delta\^{}2\ -\ 4M*Delta\^{}4\ -\ O(M*Delta\^{}6)`,
not `-2M*Delta\^{}2\ -\ (4/3)M*Delta\^{}4\ -\ O(M*Delta\^{}6)`.

**Consequence**: The specific coefficient in the
`O(M*Delta\^{}4)` term is wrong, but this term is absorbed into
the `O(M*Delta\^{}4)` notation anyway. No substantive claim is
affected.

**How to fix**: Correct the coefficient.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{3. Algebraic Verification of F1
Conversion}<!-- label: algebraic-verification-of-f1-conversion -->

This is the most critical section. Below is a complete, corrected
derivation of the F1 lower bound.

#### Setup<!-- label: setup -->

- 
- 
- 

\subsubsection{F1 in terms of alpha,
beta}<!-- label: f1-in-terms-of-alpha-beta -->

\begin{verbatim}
F1 = 2*TP/(2*TP + FP + FN)
   = 2*eta*(1-beta) / (2*eta*(1-beta) + (1-eta)*alpha + eta*beta)
\end{verbatim}

#### Case analysis<!-- label: case-analysis -->

**Case 1**: `beta\ \textgreater{}=\ epsilon` (false negative
rate is high)

Using `FP\ \textgreater{}=\ 0`:

\begin{verbatim}
F1 <= 2*eta*(1-beta) / (2*eta*(1-beta) + eta*beta)
    = 2*(1-beta)/(2-beta)
\end{verbatim}

Since `beta\ \textgreater{}=\ epsilon` and the function is
decreasing in `beta`:

\begin{verbatim}
F1 <= 2*(1-epsilon)/(2-epsilon)
1-F1 >= epsilon/(2-epsilon)
\end{verbatim}

**Case 2**: `alpha\ \textgreater{}=\ epsilon` (false
positive rate is high)

Using `FN\ \textgreater{}=\ 0`:

\begin{verbatim}
F1 <= 2*eta*(1-beta) / (2*eta*(1-beta) + (1-eta)*alpha)
\end{verbatim}

Since `beta\ \textgreater{}=\ 0` (maximizes F1 at
`beta\ =\ 0`) and `alpha\ \textgreater{}=\ epsilon`:

\begin{verbatim}
F1 <= 2*eta / (2*eta + (1-eta)*epsilon)
1-F1 >= (1-eta)*epsilon / (2*eta + (1-eta)*epsilon)
\end{verbatim}

#### Universal bound<!-- label: universal-bound -->

Since `max(alpha,\ beta)\ \textgreater{}=\ epsilon`, either Case
1 or Case 2 must hold. Therefore:

\begin{verbatim}
1-F1 >= min(epsilon/(2-epsilon), (1-eta)*epsilon/(2*eta+(1-eta)*epsilon))
\end{verbatim}

#### Which case is tighter?<!-- label: which-case-is-tighter -->

For `eta\ \textless{}\ 1/2` and small `epsilon` (the
typical regime):

\begin{verbatim}
epsilon/(2-epsilon) ≈ epsilon/2
(1-eta)*epsilon/(2*eta+(1-eta)*epsilon) ≈ (1-eta)*epsilon/(2*eta)
\end{verbatim}

Ratio:
`(epsilon/2)\ /\ ((1-eta)*epsilon/(2*eta))\ =\ eta/(1-eta)\ \textless{}\ 1`
for `eta\ \textless{}\ 1/2`.

So Case 1 gives the smaller bound (tighter). **This contradicts
the proof's claim.**

#### Correct F1 lower bound<!-- label: correct-f1-lower-bound -->

\begin{verbatim}
1-F1 >= epsilon/(2-epsilon) = (rho^M/4)/(2 - rho^M/4) = rho^M/(8 - rho^M)
\end{verbatim}

For small `rho\^{}M`:

\begin{verbatim}
1-F1 >= rho^M/8   (conservative simplification)
\end{verbatim}

Compare with the claimed bound `rho\^{}M/(16*eta)`:

\begin{longtable}[]{@{}llll@{}}
\toprule\noalign{}
eta & Correct bound & Claimed bound & Ratio 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
0.1 & `rho\^{}M/8` & `rho\^{}M/1.6` & 5x too large 

0.3 & `rho\^{}M/8` & `rho\^{}M/4.8` & 1.67x too large 

0.5 & `rho\^{}M/8` & `rho\^{}M/8` & Match 

\end{longtable}

The claimed bound is **stronger than justified** for all
`eta\ \textless{}\ 1/2`, with the discrepancy growing as
`eta` decreases.

\subsubsection{Rate optimality
preserved}<!-- label: rate-optimality-preserved -->

Both the correct bound `rho\^{}M/8` and the claimed bound
`rho\^{}M/(16*eta)` have leading term `rho\^{}M` =
`(2*sqrt(mu\_s(1-mu\_s)))\^{}M` =
`exp(-2M*Delta\^{}2\ +\ O(M*Delta\^{}4))`. The rate is preserved,
confirming that Part (c) is unaffected.

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{4. Summary of Correct vs.~Claimed
Results}<!-- label: summary-of-correct-vs.-claimed-results -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3000}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.2000}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Quantity
\end{minipage} & \begin{minipage}[b]
Claimed in v2
\end{minipage} & \begin{minipage}[b]
Correct value
\end{minipage} & \begin{minipage}[b]
Severity
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Testing bound & `rho\^{}M/4` & `rho\^{}M/4` &
**OK** 

F1 bound (const) & `rho\^{}M/(16*eta)` &
`rho\^{}M/(8-rho\^{}M)` & **FATAL (const wrong)** 

F1 bound (rate) & `exp(-2M*Delta\^{}2)` &
`exp(-2M*Delta\^{}2)` & **OK** 

K\textgreater2 affinity & `2*sqrt(mu*(1-mu/(K-1)))` &
`sqrt(mu*(1-mu/(K-1)))\ +\ sqrt((1-mu)*mu/(K-1))` & **MAJOR
(formula wrong)** 

Chernoff exactness & Holds for all K & Holds for K=2 only &
**MAJOR (overclaimed)** 

C\_bal \textgreater{} 1 & Claimed but not proven & Needs rigorous
treatment & **MAJOR (gap)** 

Taylor coeff & `-8/3*Delta\^{}4` & `-8*Delta\^{}4` &
**MINOR** 

\end{longtable}

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

\subsection{5. Comparison to v1: What is Fixed, What
Remains}<!-- label: comparison-to-v1-what-is-fixed-what-remains -->

#### Fixed from v1<!-- label: fixed-from-v1 -->

\begin{longtable}[]{@{}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3043}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1739}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.1739}}
  >{\arraybackslash}p{(\linewidth - 6\tabcolsep) * \real{0.3478}}@{}}
\toprule\noalign{}
\begin{minipage}[b]
Issue
\end{minipage} & \begin{minipage}[b]
v1
\end{minipage} & \begin{minipage}[b]
v2
\end{minipage} & \begin{minipage}[b]
Status
\end{minipage} 

\midrule\noalign{}
\endhead
\bottomrule\noalign{}
\endlastfoot
Slud's inequality & Fatal error (false bound) & Hellinger tensorization
& **Fixed** 

Chi-squared direction & Used wrong direction for K\textgreater2 &
Product reduction with correct direction & **Fixed** 

F1 algebra & Algebraic error in Lemma 8 & Case analysis (new errors
introduced) & **Partially fixed, new errors** 

Odd M ceiling & Unaddressed & Works for all M & **Fixed** 

\end{longtable}

\subsubsection{Remaining issues (this
review)}<!-- label: remaining-issues-this-review -->

1. 
2. 
3. 
4. 

#### Recommendations<!-- label: recommendations -->

1. 
2. 
3. 
4. 
5. 

<div align="center">

\rule{0.5\linewidth}{0.5pt}

</div>

*End of review.*