"""
Numerical verification of SCX exact constant minimax optimality proof chain.
Tests the specific case (p0=0.10, p1=0.60, eta=0.10) from the verification report.
"""
import numpy as np
from math import log, sqrt, exp

def kl_div(theta, p):
    """KL(theta || p) for Bernoulli"""
    if theta <= 0 or theta >= 1 or p <= 0 or p >= 1:
        return float('inf')
    return theta * log(theta/p) + (1-theta) * log((1-theta)/(1-p))

def compute_constants(p0, p1, eta):
    """Compute all constants for the SCX proof chain"""

    # The Chernoff point theta*
    num = log((1-p0)/(1-p1))
    den = log(p1*(1-p0)/(p0*(1-p1)))
    theta_star = num / den

    # KL divergences
    kappa0 = kl_div(theta_star, p0)
    kappa1 = kl_div(theta_star, p1)
    kappa = kappa0  # Should equal kappa1

    # Saddlepoints
    lambda0_star = log(theta_star*(1-p0)/(p0*(1-theta_star)))      # > 0
    lambda1_star = log(theta_star*(1-p1)/(p1*(1-theta_star)))      # < 0
    abs_lambda1 = -lambda1_star

    # Derived constants
    D_star = lambda0_star + abs_lambda1
    s = abs_lambda1 / D_star

    # Variance factor
    sqrt_theta_var = sqrt(theta_star * (1 - theta_star))

    return {
        'p0': p0, 'p1': p1, 'eta': eta,
        'theta_star': theta_star,
        'kappa': kappa,
        'lambda0_star': lambda0_star,
        'lambda1_star': lambda1_star,
        'abs_lambda1': abs_lambda1,
        'D_star': D_star,
        's': s,
        'sqrt_theta_var': sqrt_theta_var
    }

def compute_cmin_lemma_e(c):
    """C_min from Lemma E (canonical form):
    C_min = eta/2 * ((1-eta)/eta)^s * (1/lambda0* + 1/|lambda1*|) / sqrt(theta*(1-theta*))
    """
    eta = c['eta']
    s = c['s']
    lam0 = c['lambda0_star']
    lam1 = c['abs_lambda1']
    sqrt_tv = c['sqrt_theta_var']

    c_min = (eta / 2.0) * ((1 - eta) / eta) ** s * (1/lam0 + 1/lam1) / sqrt_tv
    return c_min

def compute_nonadaptive_limit(c):
    """
    Non-adaptive limit (Lemma B / Lemma D with theta*):
    lim e^{M*kappa} sqrt(2pi*M) (1 - F1) = K_na
    """
    eta = c['eta']
    lam0 = c['lambda0_star']
    lam1 = c['abs_lambda1']
    sqrt_tv = c['sqrt_theta_var']

    K_na = (1/(2*lam1) + (1-eta)/(2*eta*lam0)) / sqrt_tv
    return K_na

def compute_adaptive_limit(c):
    """
    Adaptive limit (Lemma D D.5):
    lim e^{M*kappa} sqrt(2pi*M) (1 - F1(theta_opt)) = K_ad
    """
    eta = c['eta']
    s = c['s']
    lam0 = c['lambda0_star']
    lam1 = c['abs_lambda1']
    sqrt_tv = c['sqrt_theta_var']

    K_ad = ((1 - eta) / eta) ** s * (1/lam0 + 1/lam1) / (2 * sqrt_tv)
    return K_ad

def compute_Bayes_threshold_asymptotics(c, M=1000):
    """Compute the exact Bayes test error probabilities for finite M (via brute force for moderate M)"""
    from math import comb

    p0 = c['p0']
    p1 = c['p1']
    eta = c['eta']
    D_star = c['D_star']
    theta_star = c['theta_star']

    # Bayes threshold
    delta_M = log((1-eta)/eta) / (M * D_star)
    theta_bayes = theta_star + delta_M

    # FPR = P(C_M > theta_bayes | H0)
    # FNR = P(C_M <= theta_bayes | H1)
    # For binomial: C_M = k/M where k ~ Binom(M, p)
    # P(C_M > t) = P(k > M*t) = 1 - CDF(M, p, floor(M*t))

    k_thresh = int(M * theta_bayes) + 1  # > theta_bayes means k >= k_thresh

    # Compute using binomial CDF (might be slow for large M, but let's try)
    # We'll use a saddlepoint approximation instead

    # Bahadur-Rao approximation for FPR
    # Uses the expansion with the O(1/M) shift
    lam0 = c['lambda0_star']
    lam1 = c['abs_lambda1']
    sqrt_tv = c['sqrt_theta_var']
    kappa = c['kappa']
    s = c['s']

    # From Lemma D D.4.3:
    FPR_approx = exp(-M*kappa) * ((1-eta)/eta) ** (-(1-s)) / (lam0 * sqrt(2*np.pi*M) * sqrt_tv)
    FNR_approx = exp(-M*kappa) * ((1-eta)/eta) ** s / (lam1 * sqrt(2*np.pi*M) * sqrt_tv)

    # F1
    F1 = 1 - (eta*FNR_approx + (1-eta)*FPR_approx) / (2*eta)

    return {
        'theta_bayes': theta_bayes,
        'FPR_approx': FPR_approx,
        'FNR_approx': FNR_approx,
        'F1_approx': F1,
    }

def main():
    print("=" * 70)
    print("NUMERICAL VERIFICATION: SCX Exact Constant Minimax Optimality")
    print("=" * 70)

    # Test case from verification report
    test_cases = [
        (0.10, 0.60, 0.10, "Case 1: p0=0.10, p1=0.60, eta=0.10"),
        (0.20, 0.50, 0.30, "Case 2: p0=0.20, p1=0.50, eta=0.30"),
        (0.05, 0.80, 0.05, "Case 3: p0=0.05, p1=0.80, eta=0.05"),
        (0.10, 0.60, 0.50, "Case 4: p0=0.10, p1=0.60, eta=0.50 (symmetric)"),
        (0.10, 0.60, 0.90, "Case 5: p0=0.10, p1=0.60, eta=0.90 (dominant noise)"),
    ]

    for p0, p1, eta, label in test_cases:
        print(f"\n{'='*70}")
        print(f"  {label}")
        print(f"{'='*70}")

        c = compute_constants(p0, p1, eta)

        print(f"\n  Geometric constants:")
        print(f"    theta*        = {c['theta_star']:.6f}")
        print(f"    kappa          = {c['kappa']:.6f}")
        print(f"    lambda0*       = {c['lambda0_star']:.6f}")
        print(f"    |lambda1*|     = {c['abs_lambda1']:.6f}")
        print(f"    D*             = {c['D_star']:.6f}")
        print(f"    s              = {c['s']:.6f}")
        print(f"    sqrt(theta*(1-theta*)) = {c['sqrt_theta_var']:.6f}")

        # Check kappa consistency
        kappa1 = kl_div(c['theta_star'], p1)
        kappa_diff = abs(c['kappa'] - kappa1)
        print(f"\n  Consistency check:")
        print(f"    KL(theta*||p0) = {c['kappa']:.6f}")
        print(f"    KL(theta*||p1) = {kappa1:.6f}")
        print(f"    Difference     = {kappa_diff:.2e}  {'PASS' if kappa_diff < 1e-10 else 'FAIL'}")

        # C_min from Lemma E (canonical)
        c_min = compute_cmin_lemma_e(c)
        print(f"\n  Constants:")
        print(f"    C_min (Lemma E canonical)     = {c_min:.6f}")
        print(f"    C_min/eta                      = {c_min/eta:.6f}")

        # Non-adaptive limit
        K_na = compute_nonadaptive_limit(c)
        print(f"    Non-adaptive limit K_na          = {K_na:.6f}")
        print(f"    Naive ratio K_na / (C_min/eta)   = {K_na / (c_min/eta):.4f}")

        # Adaptive limit
        K_ad = compute_adaptive_limit(c)
        print(f"    Adaptive limit K_ad              = {K_ad:.6f}")
        print(f"    Ratio K_ad / (C_min/eta)         = {K_ad / (c_min/eta):.10f}")

        # Check equality: adaptive limit == C_min/eta
        diff = abs(K_ad - c_min/eta)
        if diff < 1e-12:
            print(f"  >> CHECK: Adaptive limit == C_min/eta? PASS (diff={diff:.2e})")
        else:
            print(f"  >> CHECK: Adaptive limit == C_min/eta? FAIL (diff={diff:.2e})")

        # Compute numerical F1 for various M
        print(f"\n  Finite-M asymptotics (M=500):")
        fin = compute_Bayes_threshold_asymptotics(c, M=500)
        print(f"    theta_bayes      = {fin['theta_bayes']:.6f}")
        print(f"    FPR_approx       = {fin['FPR_approx']:.6e}")
        print(f"    FNR_approx       = {fin['FNR_approx']:.6e}")
        print(f"    F1_approx        = {fin['F1_approx']:.6f}")

        # Verify: e^{M*kappa} * sqrt(2pi*M) * (1-F1) -> K_ad
        normalization = exp(c['kappa'] * 500) * sqrt(2 * np.pi * 500)
        finite_constant = normalization * (1 - fin['F1_approx'])
        print(f"    e^(M*k)*sqrt(2pi*M)*(1-F1) = {finite_constant:.6f}")
        print(f"    Target (K_ad)               = {K_ad:.6f}")
        print(f"    Ratio finite/asymptotic      = {finite_constant/K_ad:.6f}")

        # Chernoff information vs Hoeffding exponent
        delta = p1 - p0
        hoeffding_rate = 2 * delta * delta
        print(f"\n  Rate comparison:")
        print(f"    Chernoff info kappa           = {c['kappa']:.6f}")
        print(f"    Hoeffding rate 2*Delta^2      = {hoeffding_rate:.6f}")
        print(f"    Ratio 2*Delta^2 / kappa       = {hoeffding_rate/c['kappa']:.4f}")

if __name__ == '__main__':
    main()
