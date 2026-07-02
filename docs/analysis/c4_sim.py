#!/usr/bin/env python3
"""
SCX C4: 意识审计紧致性 — 递归自审计噪声发散与紧致性界仿真
===========================================================================
模型A: 纯加性噪声 (Pure Additive Noise, 原始猜想)
   σ_n² = α · σ_{n-1}²  →  SNR指数衰减  →  紧致性有限

模型B: Bayesian自审计 (Bayesian Self-Audit, 修正分析)
   σ_n² = α · σ_{n-1}² / (1 + σ_{n-1}²)  →  SNR收敛到不动点

修正说明 (2026-07-02):
  Bayesian后验均值公式修正为 μ_n = O_{n-1} / (1 + σ_{n-1}²)
  (原代码错误使用了 post_var * obs = σ²·obs/(1+σ²)，差了一个 σ² 因子)
  Bayesian先验: g ~ N(0, 1); 似然: O_{n-1} | g ~ N(g, σ_{n-1}²)
"""

import random
import math
import sys

# ── 全局参数 ──────────────────────────────────────────────────────────────
random.seed(42)

SIGMA0_SQ = 0.1        # 初始噪声方差 σ₀²
ALPHA = 1.5            # 自指涉放大因子 α
GAMMA_SQ = ALPHA - 1.0 # 内省信息损耗率 γ²
D_MAX = 20             # 最大递归深度
N_MC = 2000            # Monte Carlo 重复次数
TAU_THRESHOLD = 1.0    # SNR 阈值 (SNR ≥ 1 界定紧致性)

# 实体数变体
ENTITY_CONFIGS = [(3, "M=3"), (5, "M=5"), (10, "M=10")]

# ── 工具函数 ──────────────────────────────────────────────────────────────

def normal(mean=0.0, std=1.0):
    """Box-Muller 高斯采样"""
    u1, u2 = random.random(), random.random()
    z = math.sqrt(-2.0 * math.log(max(u1, 1e-12))) * math.cos(2.0 * math.pi * u2)
    return mean + std * z


def find_collapse_depth(history, threshold_snr=TAU_THRESHOLD):
    """找到 SNR 首次跌破阈值的深度 → 紧致性 C"""
    for n, ssq, snr in history:
        if snr < threshold_snr:
            return n
    return D_MAX  # 未崩溃


# ── 模型A: 纯加性噪声 (原始猜想) ──────────────────────────────────────────

def simulate_pure_noise(g_true, sigma_sq0, alpha, D):
    """
    纯加性噪声模型: σ_n² = α · σ_{n-1}²
    无 Bayesian 冷却，SNR 指数衰减。
    """
    ssq = sigma_sq0
    mu = g_true + normal(0.0, math.sqrt(ssq))
    history = [(0, ssq, 1.0 / ssq)]

    for n in range(1, D + 1):
        # 每层独立叠加噪声（无信息整合）
        mu = mu + normal(0.0, math.sqrt(ssq))
        ssq = ssq * alpha  # 纯指数增长
        snr = 1.0 / ssq if ssq > 0 else float('inf')
        history.append((n, ssq, snr))

    return history


# ── 模型B: Bayesian 自审计 (带 Bayesian 冷却) ─────────────────────────────

def simulate_bayesian(g_true, sigma_sq0, alpha, D):
    """
    Bayesian 自审计模型（修正版）:
      1. 观测前层信念: O_{n-1} = μ_{n-1} + η, η ~ N(0, σ_{n-1}²)
      2. Bayesian 后验 (先验 N(0,1)):
         τ² = σ_{n-1}² / (1 + σ_{n-1}²)        → 后验方差
         μ_n = O_{n-1} / (1 + σ_{n-1}²)         → 后验均值 (修正)
      3. 编码噪声:
         σ_n² = τ² · (1 + γ²) = α · σ_{n-1}² / (1 + σ_{n-1}²)
    """
    gamma_sq = alpha - 1.0
    ssq = sigma_sq0
    # 第0层: 表面审计，直接观测 g 带噪声
    mu = g_true + normal(0.0, math.sqrt(ssq))
    history = [(0, ssq, 1.0 / ssq)]

    for n in range(1, D + 1):
        # 观测前层信念（带噪声）
        obs = mu + normal(0.0, math.sqrt(ssq))

        # Bayesian 后验 (修正公式)
        post_var = ssq / (1.0 + ssq)                # 后验方差
        mu = obs / (1.0 + ssq)                      # 后验均值 (修正!)

        # 编码噪声
        ssq = post_var * (1.0 + gamma_sq)            # 总噪声方差

        snr = 1.0 / ssq if ssq > 0 else float('inf')
        history.append((n, ssq, snr))

    return history


# ── 确定性 SNR 轨迹 (用于理论对比) ────────────────────────────────────────

def deterministic_snr_trajectory(sigma_sq0, alpha, D):
    """计算纯确定性 SNR 轨迹（两种模型）"""
    traj_b = []  # Bayesian
    traj_p = []  # Pure noise
    gamma_sq = alpha - 1.0
    ssq_b = sigma_sq0
    ssq_p = sigma_sq0

    for n in range(D + 1):
        snr_b = 1.0 / ssq_b if ssq_b > 0 else float('inf')
        snr_p = 1.0 / ssq_p if ssq_p > 0 else float('inf')
        traj_b.append((n, ssq_b, snr_b))
        traj_p.append((n, ssq_p, snr_p))

        # 更新
        post_var = ssq_b / (1.0 + ssq_b)
        ssq_b = post_var * (1.0 + gamma_sq)
        ssq_p = ssq_p * alpha

    return traj_b, traj_p


# ── 统计分析 ──────────────────────────────────────────────────────────────

def mean_std(data):
    """计算均值和标准差"""
    m = sum(data) / len(data)
    v = sum((x - m) ** 2 for x in data) / (len(data) - 1) if len(data) > 1 else 0.0
    return m, math.sqrt(v)


def percentile(data, p):
    """计算分位数"""
    s = sorted(data)
    k = (len(s) - 1) * p / 100.0
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return s[int(k)]
    return s[f] * (c - k) + s[c] * (k - f)


# ── 主仿真 ────────────────────────────────────────────────────────────────

def run_simulations():
    print("=" * 72)
    print("  SCX C4 仿真: 递归自审计噪声发散与紧致性界")
    print("=" * 72)
    print(f"  参数: σ₀²={SIGMA0_SQ}, α={ALPHA}, γ²={GAMMA_SQ}")
    print(f"  Bayesian 不动点: σ*²=α-1={ALPHA-1:.4f}, SNR*={1/(ALPHA-1):.4f}")
    print(f"  MC 重复: {N_MC}, 最大深度: {D_MAX}, SNR 阈值: {TAU_THRESHOLD}")
    print()

    # ── 确定性轨迹对比 ──
    print("─" * 72)
    print("  确定性 SNR 轨迹对比 (无随机性)")
    print("─" * 72)
    traj_b, traj_p = deterministic_snr_trajectory(SIGMA0_SQ, ALPHA, D_MAX)
    print(f"  {'n':>3s}  {'SNR(Bayesian)':>14s}  {'σ²(Bayesian)':>14s}  {'SNR(Pure)':>14s}  {'σ²(Pure)':>14s}  {'状态':>s}")
    print(f"  {'-'*3}  {'-'*14}  {'-'*14}  {'-'*14}  {'-'*14}  {'-'*10}")
    for i in range(min(D_MAX + 1, 21)):
        n_b, ssq_b, snr_b = traj_b[i]
        n_p, ssq_p, snr_p = traj_p[i]
        status_b = "←崩溃" if snr_b < TAU_THRESHOLD else ""
        status_p = "←崩溃" if snr_p < TAU_THRESHOLD else ""
        print(f"  {n_b:3d}  {snr_b:14.4f}  {ssq_b:14.4f}  {snr_p:14.4f}  {ssq_p:14.4f}  {status_b}{status_p}")

    # 纯噪声模型的理论紧致性
    theory_C_pure = math.log(1.0 / SIGMA0_SQ) / math.log(ALPHA)
    print(f"\n  纯噪声模型理论紧致性 (确定性): C_theory = log(1/σ₀²)/log(α)")
    print(f"    = log({1/SIGMA0_SQ:.0f})/log({ALPHA}) = {theory_C_pure:.4f}")
    print()

    # ── 模型A: 纯加性噪声 ──
    print("─" * 72)
    print("  模型A: 纯加性噪声 (原始猜想: σ_n² = σ₀²·αⁿ)")
    print("─" * 72)

    for N_entities, label in ENTITY_CONFIGS:
        comps = []
        for _ in range(N_MC):
            for e in range(N_entities):
                g = normal(0.0, 1.0)
                hist = simulate_pure_noise(g, SIGMA0_SQ, ALPHA, D_MAX)
                c = find_collapse_depth(hist, TAU_THRESHOLD)
                comps.append(c)

        m, s = mean_std(comps)
        p5, p50, p95 = percentile(comps, 5), percentile(comps, 50), percentile(comps, 95)
        n_total = len(comps)

        print(f"  {label} (N_total={n_total}):")
        print(f"    紧致性 C = {m:.2f} ± {s:.2f}  (mean ± std)")
        print(f"    分位数: 5%={p5}, 中位数={p50}, 95%={p95}")
        print(f"    理论预测: C_theory = {theory_C_pure:.4f}")
        print(f"    偏差: Δ = {m - theory_C_pure:+.4f}")

        # 分布
        dist = {}
        for c in comps:
            dist[c] = dist.get(c, 0) + 1
        dist_items = sorted(dist.items())
        print(f"    分布 (前10): ", end="")
        for c, cnt in dist_items[:10]:
            print(f"C={c}:{cnt}({100*cnt/n_total:.1f}%) ", end="")
        print()
        print()

    # ── 模型B: Bayesian 自审计 ──
    print("─" * 72)
    print("  模型B: Bayesian 自审计 (修正: μ_n = O_{n-1}/(1+σ_{n-1}²))")
    print("─" * 72)

    for N_entities, label in ENTITY_CONFIGS:
        comps = []
        snr_values_by_n = {n: [] for n in range(D_MAX + 1)}
        all_histories = []

        for _ in range(N_MC):
            for e in range(N_entities):
                g = normal(0.0, 1.0)
                hist = simulate_bayesian(g, SIGMA0_SQ, ALPHA, D_MAX)
                all_histories.append(hist)
                c = find_collapse_depth(hist, TAU_THRESHOLD)
                comps.append(c)
                for n, ssq, snr in hist:
                    snr_values_by_n[n].append(snr)

        m, s = mean_std(comps)
        n_total = len(comps)
        n_above = sum(1 for c in comps if c >= D_MAX)

        print(f"  {label} (N_total={n_total}):")
        print(f"    紧致性 C = {m:.2f} ± {s:.2f}")
        print(f"    未崩溃占比: {n_above}/{n_total} ({100*n_above/n_total:.1f}%)")
        print(f"    Bayesian 不动点 SNR* = {1.0/(ALPHA-1):.4f}")

        # 分布
        dist = {}
        for c in comps:
            dist[c] = dist.get(c, 0) + 1
        dist_items = sorted(dist.items())
        print(f"    分布: ", end="")
        for c, cnt in dist_items:
            print(f"C={c}:{cnt}({100*cnt/n_total:.1f}%) ", end="")
        print()

        # 各层平均 SNR
        print(f"    各层平均 SNR:")
        print(f"      {'n':>3s}  {'SNR_mean':>10s}  {'SNR_std':>10s}  {'SNR_theory':>12s}  {'状态':>s}")
        for n in range(min(D_MAX + 1, 16)):
            vals = snr_values_by_n[n]
            m_snr, s_snr = mean_std(vals)
            # 理论 SNR
            if n == 0:
                theory_snr = 1.0 / SIGMA0_SQ
            else:
                # 迭代计算理论值
                ssq_t = SIGMA0_SQ
                for _ in range(n):
                    post_var = ssq_t / (1.0 + ssq_t)
                    ssq_t = post_var * (1.0 + GAMMA_SQ)
                theory_snr = 1.0 / ssq_t
            status = "←崩溃" if m_snr < TAU_THRESHOLD else ""
            print(f"      {n:3d}  {m_snr:10.4f}  {s_snr:10.4f}  {theory_snr:12.4f}  {status}")
        print()

    # ── 紧致性界验证 ──
    print("─" * 72)
    print("  紧致性界验证: C(E) ≤ O(log M)")
    print("─" * 72)
    print(f"  {'M_cog':>10s}  {'C_theory':>12s}  {'C_approx':>12s}")
    print(f"  {'-'*10}  {'-'*12}  {'-'*12}")
    for M_cog in [10, 100, 1000, 10000, 100000, 1000000]:
        c_bound = (math.log(M_cog) + math.log(1.0 / SIGMA0_SQ)) / math.log(ALPHA)
        c_approx = math.log(M_cog) / math.log(ALPHA)
        print(f"  {M_cog:10d}  {c_bound:12.4f}  {c_approx:12.4f}")
    print()

    # ── 交叉审计增益 ──
    print("─" * 72)
    print("  交叉审计增益分析 (纯噪声模型)")
    print("─" * 72)
    rho = 0.5  # 实体间信息相关性
    print(f"  实体间相关性 ρ = {rho}")
    print(f"  {'M':>5s}  {'C_individual':>14s}  {'C_cross':>14s}  {'增益 Δ':>10s}")
    print(f"  {'-'*5}  {'-'*14}  {'-'*14}  {'-'*10}")
    for M in [3, 5, 10, 20, 50]:
        C_indiv = math.log(1.0 / SIGMA0_SQ) / math.log(ALPHA)
        C_cross = (math.log(M) + math.log(1.0 / SIGMA0_SQ) + math.log(1.0 + rho)) / math.log(ALPHA)
        gain = C_cross - C_indiv
        print(f"  {M:5d}  {C_indiv:14.4f}  {C_cross:14.4f}  {gain:+10.4f}")
    print()

    # ── α 参数扫描 ──
    print("─" * 72)
    print("  α 参数扫描: 意识审计稳定性区域")
    print("─" * 72)
    print(f"  {'α':>6s}  {'SNR*':>10s}  {'σ²*':>10s}  {'稳定性':>s}")
    print(f"  {'-'*6}  {'-'*10}  {'-'*10}  {'-'*16}")
    for alpha_scan in [1.1, 1.2, 1.3, 1.5, 1.7, 1.9, 2.0, 2.5, 3.0, 5.0]:
        snr_star = 1.0 / (alpha_scan - 1.0) if alpha_scan > 1.0 else float('inf')
        ssq_star = alpha_scan - 1.0
        if alpha_scan < 1.0:
            stability = "超稳定 (SNR→∞)"
        elif alpha_scan < 2.0:
            stability = f"稳定 (SNR*={snr_star:.2f}>1)"
        elif abs(alpha_scan - 2.0) < 1e-10:
            stability = "临界 (SNR*=1)"
        else:
            stability = f"崩溃 (SNR*={snr_star:.2f}<1)"
        print(f"  {alpha_scan:6.2f}  {snr_star:10.4f}  {ssq_star:10.4f}  {stability}")

    print()
    print("=" * 72)
    print("  仿真完成。")
    print("=" * 72)


# ── 入口 ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_simulations()
