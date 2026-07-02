import random, math

random.seed(42)
sigma0_sq = 0.1
alpha = 1.5   # self-ref amp factor: gamma^2 = alpha-1 = 0.5
gamma_sq = alpha - 1.0
D = 20
N_mc = 1000
tau_threshold = 1.0  # SNR >= 1

def normal(mean, std):
    u1, u2 = random.random(), random.random()
    z = math.sqrt(-2*math.log(u1))*math.cos(2*math.pi*u2)
    return mean + std*z

def simulate_bayesian(g_true, sigma_sq0, alpha, D):
    """Bayesian self-audit with coding noise"""
    gamma_sq = alpha - 1.0
    ssq = sigma_sq0
    mu = g_true + normal(0, math.sqrt(ssq))
    history = [(0, ssq, 1.0/ssq)]
    
    for n in range(1, D+1):
        obs = mu + normal(0, math.sqrt(ssq))
        post_var = ssq / (1.0 + ssq)  # prior var = 1
        mu = post_var * obs
        ssq = post_var * (1.0 + gamma_sq)  # + coding noise
        history.append((n, ssq, 1.0/ssq))
    return history

def simulate_pure_noise(g_true, sigma_sq0, alpha, D):
    """Pure additive noise: sigma_n^2 = alpha * sigma_{n-1}^2 (no Bayesian cooling)"""
    ssq = sigma_sq0
    mu = g_true + normal(0, math.sqrt(ssq))
    history = [(0, ssq, 1.0/ssq)]
    for n in range(1, D+1):
        mu = mu + normal(0, math.sqrt(ssq))
        ssq = ssq * alpha  # pure exponential
        history.append((n, ssq, 1.0/ssq))
    return history

print("="*60)
print("SCX C4 Simulation: Recursive Self-Audit Noise")
print("="*60)
print(f"sigma0_sq={sigma0_sq}, alpha={alpha}, gamma_sq={gamma_sq}")
print(f"Steady state (Bayesian): ssq* = alpha-1 = {alpha-1:.3f}, SNR* = {1/(alpha-1):.3f}")
print()

# --- Model A: Bayesian self-audit ---
print("--- Model A: Bayesian Self-Audit (with cooling) ---")
for M_label, N_entities in [("M=3", 3), ("M=5", 5), ("M=10", 10)]:
    comps = []
    for _ in range(N_mc):
        for e in range(N_entities):
            g = normal(0, 1)
            hist = simulate_bayesian(g, sigma0_sq, alpha, D)
            for n, ssq, snr in hist:
                if snr < tau_threshold or ssq >= 1.0:
                    comps.append(n)
                    break
            else:
                comps.append(D)
    mean_c = sum(comps)/len(comps)
    var_c = sum((c-mean_c)**2 for c in comps)/(len(comps)-1)
    std_c = math.sqrt(var_c)
    print(f"  {M_label}: C={mean_c:.2f}±{std_c:.2f}, range=[{min(comps)},{max(comps)}], "
          f"N_above_thresh={sum(1 for c in comps if c >= D)}/{len(comps)}")
    
    # 分布
    dist = {}
    for c in comps:
        dist[c] = dist.get(c, 0) + 1
    for c in sorted(dist)[:8]:
        print(f"    C={c}: {dist[c]} ({100*dist[c]/len(comps):.1f}%)")

print()

# --- Model B: Pure additive noise (no Bayesian cooling) ---
print("--- Model B: Pure Additive Noise (no cooling, exponential) ---")
for M_label, N_entities in [("M=3", 3), ("M=5", 5), ("M=10", 10)]:
    comps = []
    for _ in range(N_mc):
        for e in range(N_entities):
            g = normal(0, 1)
            hist = simulate_pure_noise(g, sigma0_sq, alpha, D)
            for n, ssq, snr in hist:
                if snr < tau_threshold:
                    comps.append(n)
                    break
            else:
                comps.append(D)
    mean_c = sum(comps)/len(comps)
    var_c = sum((c-mean_c)**2 for c in comps)/(len(comps)-1)
    std_c = math.sqrt(var_c)
    theory_C = math.log(1/sigma0_sq)/math.log(alpha)
    print(f"  {M_label}: C={mean_c:.2f}±{std_c:.2f}, theory_C={theory_C:.2f}")
    
    dist = {}
    for c in comps:
        dist[c] = dist.get(c, 0) + 1
    for c in sorted(dist)[:8]:
        print(f"    C={c}: {dist[c]} ({100*dist[c]/len(comps):.1f}%)")

print()

# --- SNR trajectory (single run, deterministic part) ---
print("--- SNR trajectory comparison (deterministic) ---")
ssq_b = sigma0_sq
ssq_p = sigma0_sq
for n in range(21):
    snr_b = 1.0/ssq_b if ssq_b > 0 else float('inf')
    snr_p = 1.0/ssq_p if ssq_p > 0 else float('inf')
    marker_b = " <<<" if snr_b < 1 else ""
    marker_p = " <<<" if snr_p < 1 else ""
    print(f"  n={n:2d}: Bayesian SNR={snr_b:8.4f}{marker_b} | Pure SNR={snr_p:8.4f}{marker_p} | ssq_b={ssq_b:.4f} ssq_p={ssq_p:.4f}")
    # update
    post_var = ssq_b / (1.0 + ssq_b)
    ssq_b = post_var * (1.0 + gamma_sq)
    ssq_p = ssq_p * alpha

print()

# --- Cross-audit analysis ---
print("--- Cross-Audit Enhancement ---")
rho = 0.5
for M in [3, 5, 10]:
    # In pure noise model, cross-audit can extend C
    C_indiv = math.log(1/sigma0_sq) / math.log(alpha)
    C_cross = (math.log(M) + math.log(1/sigma0_sq) + math.log(1+rho)) / math.log(alpha)
    print(f"  M={M}: C_individual={C_indiv:.2f}, C_cross={C_cross:.2f}, gain={C_cross-C_indiv:.2f}")

print("\nDone.")
