# Numerical Verification of Theoretical Constants

**Author:** SCX

## Numerical Verification of Theoretical Constants

This section provides numerical verification of the exact constant minimax optimality result (Theorem~4' in Supplementary Information S4). All computations are performed using the Python script `numerical\_verify.py` with standard double-precision arithmetic.

### Verification Protocol

For a given parameter set $(p_0, p_1, \eta)$, we compute the following theoretical quantities:

1. **Chernoff point** $\theta^*$: the unique solution to $\mathrm{KL}(\theta\|p_0) = \mathrm{KL}(\theta\|p_1)$,
2. **Chernoff information** $\kappa = \mathrm{KL}(\theta^*\|p_0) = \mathrm{KL}(\theta^*\|p_1)$,
3. **Saddlepoints** $\lambda_0^* > 0$, $\lambda_1^* < 0$ defined by the log-odds at $\theta^*$,
4. **Total log-odds** $D^* = \lambda_0^* + |\lambda_1^*|$ and exponent fraction $s = |\lambda_1^*|/D^*$,
5. **Canonical minimax constant** $C_$ (Lemma~E form):
6. **Non-adaptive limit** $K_{\mathrm{na}}$ (Lemma~B, using $\theta^*$ without $\eta$ adaptation):
7. **Adaptive limit** $K_{\mathrm{ad}}$ (Lemma~D, using $\eta$-aware threshold $\theta^\dagger$):

The verification criterion is the machine-precision equality $K_{\mathrm{ad}} = C_/\eta$, which confirms that the adaptive threshold achieves the minimax lower bound exactly (up to the asymptotic limit).

### Test Case 1: Standard Parameters

Parameters: $p_0 = 0.10$, $p_1 = 0.60$, $\eta = 0.10$. This is the canonical case studied in the main text (AlN v3 MLIP regime), with moderate separation and moderately rare noise.

[Table omitted — see original .tex]

- **Adaptive limit $=$ $C_/\eta$**: `PASS` (difference $< 10^{-15}$).
- **Chernoff $\kappa$ vs Hoeffding $2\Delta^2$**: $\kappa = 0.1696$, $2\Delta^2 = 0.5000$, ratio $= 2.95$. The Chernoff rate is substantially slower (more honest) than the Hoeffding bound.
- **Non-adaptive penalty**: The naive threshold $\theta^*$ (which ignores $\eta$) is $1.70\times$ worse than the adaptive threshold.

### Test Case 2: Weak Separation

Parameters: $p_0 = 0.20$, $p_1 = 0.50$, $\eta = 0.30$. This case has a smaller separation gap ($\Delta = 0.30$ versus $\Delta = 0.50$ in Case~1) and moderate noise.

[Table omitted — see original .tex]

- **Adaptive limit $=$ $C_/\eta$**: `PASS` (difference $< 10^{-15}$).
- **Chernoff $\kappa$ vs Hoeffding $2\Delta^2$**: $\kappa = 0.0528$, $2\Delta^2 = 0.1800$, ratio $= 3.41$. The Hoeffding bound is $3.4\times$ more optimistic than the Chernoff rate.
- **Non-adaptive penalty**: Only $1.09\times$ worse --- for $\eta$ near $1/2$, the adaptive gain is small (confirming the theory).

### Test Case 3: Strong Separation

Parameters: $p_0 = 0.05$, $p_1 = 0.80$, $\eta = 0.05$. This case has a large separation gap ($\Delta = 0.75$), rare noise, and very low clean error.

[Table omitted — see original .tex]

- **Adaptive limit $=$ $C_/\eta$**: `PASS` (difference $< 5 \times 10^{-16}$).
- **Chernoff $\kappa$ vs Hoeffding $2\Delta^2$**: $\kappa = 0.4574$, $2\Delta^2 = 1.1250$, ratio $= 2.46$. The Chernoff rate is the fastest among all cases (largest $\kappa$), reflecting the strong separation.
- **Non-adaptive penalty**: The naive threshold is $2.41\times$ worse --- the largest penalty of all cases, because $\eta = 0.05$ is far from $1/2$, making the $\eta$-aware threshold critical.

### Test Case 4: Symmetric Noise

Parameters: $p_0 = 0.10$, $p_1 = 0.60$, $\eta = 0.50$. The geometric constants are identical to Case~1 (same $p_0, p_1$); only $\eta$ changes. At $\eta = 0.50$, the noise is symmetric (noise prior equals the clean prior).

[Table omitted — see original .tex]

- **Adaptive limit $=$ $C_/\eta$**: `PASS` (difference $< 10^{-15}$).
- **Adaptive $=$ non-adaptive**: At $\eta = 1/2$, the correction term $\frac{1}{M}\frac{\log((1-\eta)/\eta)}{D^*} = 0$, so $\theta^\dagger = \theta^*$. The two limits coincide exactly.
- **Theoretical prediction confirmed**: Lemma~D states that the $O(1/M)$ threshold shift vanishes when $\eta = 1/2$. Numerical verification confirms this.

### Test Case 5: Dominant Noise

Parameters: $p_0 = 0.10$, $p_1 = 0.60$, $\eta = 0.90$. This is the reciprocal of Case~1: noise dominates the dataset. The geometric constants are identical to Case~1 and Case~4 (same $p_0, p_1$).

[Table omitted — see original .tex]

- **Adaptive limit $=$ $C_/\eta$**: `PASS` (difference $< 10^{-15}$).
- **Non-adaptive penalty**: The naive threshold is $1.62\times$ worse. The penalty is slightly smaller than in Case~1 ($1.70\times$), reflecting the asymmetry of the $((1-\eta)/\eta)^s$ factor: the penalty for $\eta=0.90$ is the reciprocal of the penalty for $\eta=0.10$ under the mapping $\eta \mapsto 1-\eta$, and the constants account for this via the $s$ exponent.

### Finite-$M$ Convergence Analysis

The Bahadur--Rao asymptotic expansion predicts that for finite $M$,

$$
e^{M\kappa} \sqrt{2\pi M} \bigl(1 - \mathrm{F1}(M)\bigr) \longrightarrow \frac{C_} \quad as  M\to\infty.
$$

Table [ref] shows the finite-$M$ convergence for Case~2 (the only case where $M=500$ produces non-zero $1-\mathrm{F1}$ within double precision; for the other cases, the error probabilities are below machine epsilon at $M=500$).

[Table omitted — see original .tex]

The convergence is monotonic and rapid: at $M=100$, the normalized constant is within $0.12\%$ of the asymptotic limit; at $M=500$, it matches to $0.02\%$.

### Summary Table: All Cases

Table [ref] collects the key verification metrics across all five test cases. The central result is that the adaptive limit $K_{\mathrm{ad}}$ matches $C_/\eta$ to machine precision in every case, confirming that the SCX adaptive threshold achieves the minimax lower bound exactly.

\begin{table*}[htbp]

*Caption:* Summary of numerical verification across all five test cases.
<!-- label: tab:summary -->
[Table omitted — see original .tex]
\end{table*}

**Key findings.**

1. **Machine-precision equality** ($K_{\mathrm{ad}} = C_/\eta$) holds across all five cases, confirming the algebraic equivalence of the adaptive achievability limit and the minimax lower bound.
2. **Chernoff information is always slower than the Hoeffding bound**: $2\Delta^2 / \kappa > 1$ in all cases (range $2.46$--$3.41$). This confirms that the Hoeffding bound overestimates the rate of convergence.
3. **Non-adaptive penalty is case-dependent**: The naive threshold $\theta^*$ (ignoring $\eta$) is suboptimal by factors $1.00$--$2.41$. The penalty is largest when $\eta$ is far from $1/2$ (Cases~1,~3,~5) and disappears at $\eta = 1/2$ (Case~4).
4. **All constants satisfy theoretical consistency checks**: $\mathrm{KL}(\theta^*\|p_0) = \mathrm{KL}(\theta^*\|p_1)$ holds to $\pm 10^{-16}$; $C_ > 0$ in all cases; $K_{\mathrm{ad}} > 0$; the exponent fraction $s \in (0,1)$.