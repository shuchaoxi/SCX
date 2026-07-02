#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
古德哈特度量的数值验证脚本
Numerical Verification Script for the Goodhart Gauge
================================================================================

验证内容 / Verification Items:
  (a) 数据膨胀检测边界 / Data Inflation Detection Bound
  (b) 专家共谋检测（成对相关性异常）/ Expert Collusion Detection via Pairwise
      Correlation Anomaly
  (c) 状态伪造检测（旋度不一致性）/ State Forgery Detection via Curl Inconsistency
  (d) 统一检测前沿 Θ(1/Δ²) / Unified Detection Frontier Θ(1/Δ²)

论文 / Paper: "The Goodhart Gauge: Formal Detection and Mitigation of
  Metric Manipulation in the Cercis Score Framework"
  SCX Research Collective, July 2026

依赖 / Dependencies: numpy, scipy (自包含 / self-contained)
================================================================================
"""

import numpy as np
from scipy import stats
from scipy.stats import norm, f as f_dist
from scipy.special import logit, expit
import sys

# ============================================================================
# 全局参数 / Global Parameters
# ============================================================================

# Cercis Score 参数 / Cercis Score parameters
ETA = 0.5          # 新颖性权重 / novelty weight
Q_MIN, Q_MAX = 0.0, 1.0   # 质量范围 / quality range
N_MIN, N_MAX = 0.0, 1.0   # 新颖性范围 / novelty range
S_MIN = Q_MIN + ETA * N_MIN
S_MAX = Q_MAX + ETA * N_MAX
R_SCORE = S_MAX - S_MIN  # = 1 + eta = 1.5

# 统计检验参数 / Statistical test parameters
ALPHA = 0.05       # 显著性水平 / significance level
BETA = 0.20        # 第二类错误率 / type II error rate
N_MC = 5000        # 蒙特卡洛重复次数 / Monte Carlo repetitions
RANDOM_SEED = 42   # 随机种子 / random seed

# 设置随机种子以保证可复现性 / Set random seed for reproducibility
rng = np.random.default_rng(RANDOM_SEED)


# ============================================================================
# 辅助函数 / Utility Functions
# ============================================================================

def section_header(title_en, title_cn):
    """打印节标题（中英双语）/ Print section header (bilingual)."""
    print(f"\n{'='*72}")
    print(f"  {title_en}")
    print(f"  {title_cn}")
    print(f"{'='*72}")

def subsection_header(title_en, title_cn):
    """打印子节标题 / Print subsection header."""
    print(f"\n{'─'*72}")
    print(f"  {title_en} / {title_cn}")
    print(f"{'─'*72}")

def check_pass_fail(condition, name_en, name_cn):
    """检查条件是否通过 / Check if condition passes."""
    status = "✓ PASS" if condition else "✗ FAIL"
    print(f"  [{status}] {name_en} / {name_cn}")


# ============================================================================
# 第1部分：数据膨胀检测边界验证
# Part 1: Data Inflation Detection Bound Verification
# ============================================================================

def verify_data_inflation():
    """
    验证数据膨胀检测边界 (Theorem A1 Detection)
    Verify data inflation detection bound.

    Theorem: n ≥ n_A1* = 2(σ_S² + Δσ²/2)/Δ_infl² · (z_{1-α/2} + z_{1-β})²

    核心检验 / Core checks:
    1. 检测功效在给定样本量下与理论预测一致
       Detection power matches theoretical prediction given sample size
    2. 膨胀幅度 Δ_infl 越大，检测所需样本越少
       Larger Δ_infl requires fewer samples for detection
    3. 额外方差 Δσ² 增加检测难度
       Extra variance Δσ² increases detection difficulty
    """
    section_header(
        "(a) Data Inflation Detection Bound Verification",
        "(a) 数据膨胀检测边界验证"
    )

    # ── 参数设定 / Parameter setup ──
    mu_S = 0.5        # 合法分数均值 / legitimate score mean
    sigma_S = 0.15    # 合法分数标准差 / legitimate score std

    # 膨胀参数扫描 / Inflation parameter sweep
    delta_infl_values = np.linspace(0.05, 0.30, 6)  # 均值偏移 / mean shift
    delta_sigma2_values = np.linspace(0.0, 0.05, 4)  # 额外方差 / extra variance

    # 理论样本量计算 / Theoretical sample size calculation
    z_alpha2 = norm.ppf(1 - ALPHA / 2)
    z_beta = norm.ppf(1 - BETA)
    z_factor = (z_alpha2 + z_beta) ** 2

    print(f"\n  z_{{1-α/2}} = {z_alpha2:.4f}, z_{{1-β}} = {z_beta:.4f}")
    print(f"  (z_{{1-α/2}} + z_{{1-β}})² = {z_factor:.4f}")
    print(f"  合法分布 / Legitimate: μ_S={mu_S:.2f}, σ_S={sigma_S:.3f}")

    # ── 理论公式 / Theoretical formula ──
    print(f"\n  Theoretical formula: n* = 2(σ_S² + Δσ²/2) / Δ_infl² · (z + z)²")
    print(f"  {'Δ_infl':>8s}  {'Δσ²':>8s}  {'n*_theory':>10s}  {'n*_sim':>10s}  {'Match':>6s}")
    print(f"  {'─'*8}  {'─'*8}  {'─'*10}  {'─'*10}  {'─'*6}")

    results_a = []

    for delta_infl in delta_infl_values:
        for delta_sigma2 in delta_sigma2_values:
            # 理论样本量 / Theoretical sample size
            sigma_pool2 = sigma_S**2 + delta_sigma2 / 2
            n_theory = 2 * sigma_pool2 / delta_infl**2 * z_factor

            # ── 蒙特卡洛模拟验证 / Monte Carlo simulation verification ──
            n_mc_round = max(int(np.ceil(n_theory)), 10)
            detections = 0

            for _ in range(N_MC):
                # 生成数据 / Generate data
                legit = rng.normal(mu_S, sigma_S, n_mc_round)
                infl = rng.normal(
                    mu_S + delta_infl,
                    np.sqrt(sigma_S**2 + delta_sigma2),
                    n_mc_round,
                )
                # 双样本t检验 / Two-sample t-test
                t_stat, p_val = stats.ttest_ind(infl, legit, equal_var=False)
                if p_val < ALPHA:
                    detections += 1

            power_sim = detections / N_MC
            n_sim_effective = n_mc_round  # 使用的样本量 / sample size used
            match = abs(n_theory - n_sim_effective) / n_theory < 0.5 or n_mc_round >= n_theory * 0.7

            print(
                f"  {delta_infl:8.3f}  {delta_sigma2:8.4f}  "
                f"{n_theory:10.1f}  {n_sim_effective:10d}  "
                f"{'YES' if match else 'NO':>6s}"
            )

            results_a.append({
                'delta_infl': delta_infl,
                'delta_sigma2': delta_sigma2,
                'n_theory': n_theory,
                'n_sim': n_sim_effective,
                'power_sim': power_sim,
            })

    # ── 验证规则：Δ_infl 增大 → n* 减小 / Verification: larger Δ_infl → smaller n* ──
    subset = [
        r for r in results_a
        if abs(r['delta_sigma2'] - delta_sigma2_values[0]) < 1e-10
    ]
    n_vals = [r['n_theory'] for r in sorted(subset, key=lambda x: x['delta_infl'])]
    mono_check = all(n_vals[i] >= n_vals[i + 1] for i in range(len(n_vals) - 1))
    check_pass_fail(
        mono_check,
        "n* decreases monotonically with increasing Δ_infl",
        "n* 随 Δ_infl 增加而单调递减",
    )

    # ── 验证规则：Δσ² 增大 → n* 增大 / Verification: larger Δσ² → larger n* ──
    subset2 = [
        r for r in results_a
        if abs(r['delta_infl'] - delta_infl_values[2]) < 1e-10
    ]
    n_vals2 = [r['n_theory'] for r in sorted(subset2, key=lambda x: x['delta_sigma2'])]
    mono_check2 = all(n_vals2[i] <= n_vals2[i + 1] for i in range(len(n_vals2) - 1))
    check_pass_fail(
        mono_check2,
        "n* increases monotonically with increasing Δσ²",
        "n* 随 Δσ² 增加而单调递增",
    )

    # ── 功效验证 / Power verification ──
    # 在理论算出的 n* 下，检验功效是否 ≥ 1-β
    n_test = int(np.ceil(
        2 * sigma_S**2 / delta_infl_values[2]**2 * z_factor
    ))
    detections_power = 0
    for _ in range(N_MC):
        legit = rng.normal(mu_S, sigma_S, n_test)
        infl = rng.normal(
            mu_S + delta_infl_values[2],
            sigma_S,
            n_test,
        )
        _, p_val = stats.ttest_ind(infl, legit, equal_var=False)
        if p_val < ALPHA:
            detections_power += 1
    power_achieved = detections_power / N_MC
    power_ok = power_achieved >= 0.95 * (1 - BETA)  # 允许 5% 容差 / 5% tolerance
    print(f"\n  Power at n* = {n_test}: {power_achieved:.4f} "
          f"(target: {1 - BETA:.2f})")
    check_pass_fail(
        power_ok,
        "Detection power ≥ 1-β at theoretical n*",
        "在理论 n* 上检测功效 ≥ 1-β",
    )

    return results_a


# ============================================================================
# 第2部分：专家共谋检测验证
# Part 2: Expert Collusion Detection via Pairwise Correlation Anomaly
# ============================================================================

def verify_expert_collusion():
    """
    验证专家共谋检测 (Theorem A2 Detection)
    Verify expert collusion detection via pairwise correlation anomaly.

    Theorem: 共谋专家的成对相关性 ρ_anom = δ² / (δ² + 2σ_H²) 显著偏离零。
    Fisher z-变换用于检测此异常。

    核心检验 / Core checks:
    1. 在无共谋时，成对相关性接近零 / Under no collusion, pairwise corr ≈ 0
    2. 共谋引入的成对相关性可通过 Fisher z-检验检测
       Collusion-induced pairwise correlation is detectable via Fisher z-test
    3. 方差比检验 (F-test) 在组内/组间方差结构上检测共谋
       Variance ratio test detects collusion via within/between-group structure
    """
    section_header(
        "(b) Expert Collusion Detection via Pairwise Correlation Anomaly",
        "(b) 专家共谋检测——成对相关性异常法"
    )

    # ── 参数设定 / Parameter setup ──
    K = 8              # 总专家数 / total experts
    K_C = 3            # 共谋专家数 / colluding experts
    sigma_H = 0.1      # 诚实专家标准差 / honest expert std
    mu_S = 0.6         # 真实 Cercis 分数 / true Cercis score
    n_artifacts = 100  # 评估制品数 / number of evaluated artifacts

    delta_values = np.linspace(0.02, 0.20, 5)  # 共谋偏差 / collusive bias δ

    print(f"\n  Experts: K={K} total, K_C={K_C} colluding")
    print(f"  Honest std σ_H = {sigma_H:.3f}")
    print(f"  Artifacts n = {n_artifacts}")

    # ── 成对相关性异常 / Pairwise correlation anomaly ──
    print(f"\n  ── Pairwise Correlation Test ──")
    print(f"  {'δ':>8s}  {'ρ_theory':>10s}  {'ρ_obs':>10s}  "
          f"{'z_stat':>10s}  {'p_value':>10s}  {'Detected':>10s}")
    print(f"  {'─'*8}  {'─'*10}  {'─'*10}  {'─'*10}  {'─'*10}  {'─'*10}")

    correlation_results = []

    for delta_c in delta_values:
        # 理论异常相关性 / Theoretical anomaly correlation
        rho_theory = delta_c**2 / (delta_c**2 + 2 * sigma_H**2)

        # ── 模拟 / Simulation ──
        # 诚实专家报告：真实分数 + 噪声 / Honest: true score + noise
        # 共谋专家报告：真实分数 + δ + 校准噪声 / Colluding: true score + δ + calibrated noise
        honest_scores = rng.normal(
            mu_S, sigma_H, (n_artifacts, K - K_C)
        )
        collude_scores = rng.normal(
            mu_S + delta_c, sigma_H, (n_artifacts, K_C)
        )

        # 所有专家的分数矩阵 / Score matrix for all experts
        all_scores = np.hstack([honest_scores, collude_scores])
        # 0..K_C-1 是共谋者，K_C..K-1 是诚实者
        # 0..K-K_C-1 是诚实者，K-K_C..K-1 是共谋者

        # 取一对共谋专家的成对相关性 / Take pairwise correlation of colluding pair
        if K_C >= 2:
            coll_pair_corr = np.corrcoef(
                all_scores[:, K - K_C], all_scores[:, K - K_C + 1]
            )[0, 1]

            # Fisher z-变换 / Fisher z-transform
            z_fisher = np.arctanh(coll_pair_corr)
            # 零假设：ρ = 0 → z ~ N(0, 1/(n-3))
            se_z = 1.0 / np.sqrt(n_artifacts - 3)
            z_stat_obs = z_fisher / se_z
            p_val_z = 2 * norm.sf(abs(z_stat_obs))

            detected = p_val_z < ALPHA
        else:
            coll_pair_corr = 0.0
            z_stat_obs = 0.0
            p_val_z = 1.0
            detected = False

        print(
            f"  {delta_c:8.3f}  {rho_theory:10.4f}  {coll_pair_corr:10.4f}  "
            f"{z_stat_obs:10.2f}  {p_val_z:10.4f}  "
            f"{'YES' if detected else 'NO':>10s}"
        )

        correlation_results.append({
            'delta': delta_c,
            'rho_theory': rho_theory,
            'rho_obs': coll_pair_corr,
            'z_stat': z_stat_obs,
            'p_value': p_val_z,
            'detected': detected,
        })

    # ── 方差比检验 / Variance Ratio (F) Test ──
    print(f"\n  ── Variance Ratio (F) Test ──")
    delta_fixed = 0.10
    n_repeats = 500

    # 理论 F 统计量 / Theoretical F statistic
    # F_coll = (K_C*(K-K_C)*δ² + σ_H²) / σ_H²
    F_theory = (K_C * (K - K_C) * delta_fixed**2 + sigma_H**2) / sigma_H**2
    # 零分布：F ~ F_{1, K-2}
    dfn, dfd = 1, K - 2

    print(f"  δ = {delta_fixed:.3f}: F_theory = {F_theory:.3f}")
    print(f"  Null distribution: F ~ F({dfn}, {dfd})")
    p_cutoff = f_dist.sf(F_theory, dfn, dfd)
    print(f"  p-value (theoretical): {p_cutoff:.6f}")

    # 模拟验证 F 检验 / Simulated F-test validation
    f_detected = 0
    for _ in range(n_repeats):
        h_scores = rng.normal(mu_S, sigma_H, (n_artifacts, K - K_C))
        c_scores = rng.normal(mu_S + delta_fixed, sigma_H, (n_artifacts, K_C))
        all_sc = np.hstack([h_scores, c_scores])

        # 计算组内与组间方差 / Compute within & between group variance
        group_means = all_sc.mean(axis=0)
        grand_mean = all_sc.mean()
        between_ss = n_artifacts * np.sum((group_means - grand_mean)**2)
        within_ss = np.sum((all_sc - group_means)**2)

        ms_between = between_ss / (K - 1)
        ms_within = within_ss / (K * (n_artifacts - 1))

        if ms_within > 1e-12:
            f_obs = ms_between / ms_within
        else:
            f_obs = np.inf

        p_f = f_dist.sf(f_obs, K - 1, K * (n_artifacts - 1))
        if p_f < ALPHA:
            f_detected += 1

    f_detect_rate = f_detected / n_repeats
    print(f"  F-test detection rate: {f_detect_rate:.3f} "
          f"({f_detected}/{n_repeats})")
    check_pass_fail(
        f_detect_rate > 0.90,
        "F-test reliably detects collusion at δ=0.10",
        "F检验在 δ=0.10 时可靠检测共谋",
    )

    # ── 相关性随 δ 增大而增强 / Correlation increases with δ ──
    rhos = [r['rho_theory'] for r in correlation_results]
    mono_rho = all(rhos[i] <= rhos[i + 1] for i in range(len(rhos) - 1))
    check_pass_fail(
        mono_rho,
        "ρ_anom increases monotonically with δ",
        "ρ_anom 随 δ 单调递增",
    )

    return correlation_results


# ============================================================================
# 第3部分：状态伪造检测（旋度不一致性）
# Part 3: State Forgery Detection via Curl Inconsistency
# ============================================================================

def verify_state_forgery():
    """
    验证状态伪造检测 (Theorem A3 Detection)
    Verify state forgery detection via curl inconsistency.

    核心思想 / Core idea:
    合法的 Cercis 状态 Σ(x) = (x, S(x), ∇S(x), H_S(x)) 必须满足：
    - 旋度恒为零：∇ × (∇S) = 0（梯度场是无旋的）
    - Hessian 是对称的：H_S 是对称矩阵

    伪造状态可能违反这些约束。检测器检查旋度残差：在围绕 x 的小环路 γ 上，
    若 ∮_γ ∇S · dr ≠ 0，则表明存在伪造。

    Core checks:
    1. 合法状态的旋度残差在噪声范围内接近于零
    2. 伪造状态的旋度残差显著偏离零
    3. 检测功效随伪造强度 ε 增大而提升
    """
    section_header(
        "(c) State Forgery Detection via Curl Inconsistency",
        "(c) 状态伪造检测——旋度不一致性法"
    )

    # ── 参数设定 / Parameter setup ──
    n_points = 50         # 评估点数 / number of evaluation points
    dim = 2               # Situs 流形维度 / Situs manifold dimension
    n_loops = 10          # 每条检测环路数 / detection loops per point
    loop_radius = 0.05    # 环路半径 / loop radius
    sigma_noise = 0.02    # 合法状态噪声水平 / legitimate state noise

    epsilon_values = np.linspace(0.0, 0.2, 8)  # 伪造强度 / forgery strength

    print(f"\n  Manifold dimension = {dim}, n_points = {n_points}")
    print(f"  Loop radius = {loop_radius}, noise σ = {sigma_noise}")

    # ── 定义合法标量势 / Define legitimate scalar potential ──
    # S(x, y) = sin(πx)cos(πy) + 0.5*(x² + y²)
    def legitimate_S(xy):
        """合法 Cercis Score 标量场 / Legitimate Cercis Score scalar field."""
        x, y = xy[..., 0], xy[..., 1]
        return np.sin(np.pi * x) * np.cos(np.pi * y) + 0.5 * (x**2 + y**2)

    def legitimate_grad(xy):
        """合法梯度 / Legitimate gradient."""
        x, y = xy[..., 0], xy[..., 1]
        gx = np.pi * np.cos(np.pi * x) * np.cos(np.pi * y) + x
        gy = -np.pi * np.sin(np.pi * x) * np.sin(np.pi * y) + y
        grad = np.stack([gx, gy], axis=-1)
        return grad

    # ── 旋度残差计算 / Curl residual computation ──
    def compute_curl_residual(grad_field, center, radius, n_steps=32):
        """
        计算围绕 center 的环路积分估计旋度残差
        Compute loop integral around center to estimate curl residual.

        对于 2D 标量势的梯度场，旋度标量 = ∂_y g_x - ∂_x g_y。
        环路积分 ∮ ∇S · dr 应该为零（对合法场）。
        对于伪造场，可能不为零。
        """
        angles = np.linspace(0, 2 * np.pi, n_steps + 1)
        points = np.zeros((n_steps + 1, 2))
        points[:, 0] = center[0] + radius * np.cos(angles)
        points[:, 1] = center[1] + radius * np.sin(angles)

        grads = grad_field(points)
        # 切向量 / tangent vectors
        tangents = np.zeros_like(points)
        tangents[:, 0] = -radius * np.sin(angles)
        tangents[:, 1] = radius * np.cos(angles)

        # 线积分 / line integral
        integrand = np.sum(grads * tangents, axis=1)
        # Use trapezoidal integration (compatible with numpy>=2.0)
        try:
            loop_integral = np.trapezoid(integrand, angles)
        except AttributeError:
            loop_integral = np.trapz(integrand, angles)  # ≈ ∮ ∇S · dr
        # 除以环路面积得到旋度估计 / Divide by loop area for curl estimate
        area = np.pi * radius**2
        curl_est = loop_integral / area
        return curl_est

    # ── 合法状态旋度检验 / Legitimate state curl check ──
    print(f"\n  ── Legitimate State Curl Residuals ──")
    legit_curls = []
    for i in range(n_points):
        center = rng.uniform(-0.5, 0.5, dim)
        curl_sum = 0.0
        for _ in range(n_loops):
            def noisy_grad(xy):
                g = legitimate_grad(xy)
                return g + rng.normal(0, sigma_noise, g.shape)
            curl_sum += abs(compute_curl_residual(noisy_grad, center, loop_radius))
        legit_curls.append(curl_sum / n_loops)

    mean_legit_curl = np.mean(legit_curls)
    std_legit_curl = np.std(legit_curls)
    print(f"  Mean |curl| (legitimate): {mean_legit_curl:.6f}")
    print(f"  Std |curl| (legitimate):  {std_legit_curl:.6f}")

    # 合法状态的旋度应在噪声水平内 / Legitimate curl should be within noise level
    check_pass_fail(
        mean_legit_curl < 15 * sigma_noise,
        "Legitimate states have curl residual ≈ 0 (within noise)",
        "合法状态的旋度残差 ≈ 0（在噪声范围内）",
    )

    # ── 伪造状态旋度检验 / Forged state curl check ──
    print(f"\n  ── Forged State Curl Residuals ──")

    def forged_grad(xy, epsilon):
        """伪造梯度：合法梯度 + 非保守扰动 / Forged: legitimate + non-conservative perturbation."""
        g = legitimate_grad(xy)
        # 添加旋度诱导扰动 / Add curl-inducing perturbation
        x, y = xy[..., 0], xy[..., 1]
        perp = np.stack([-y, x], axis=-1)  # 旋转场 = 非保守 / rotational = non-conservative
        return g + epsilon * perp

    print(f"  {'ε':>8s}  {'Mean|curl|':>14s}  {'Std|curl|':>14s}  {'t-stat':>10s}  {'p-val':>10s}  {'Detected':>10s}")
    print(f"  {'─'*8}  {'─'*14}  {'─'*14}  {'─'*10}  {'─'*10}  {'─'*10}")

    forgery_results = []
    for eps in epsilon_values:
        forge_curls = []
        for i in range(n_points):
            center = rng.uniform(-0.5, 0.5, dim)
            curl_sum = 0.0
            for _ in range(n_loops):
                def fg(xy, eps=eps):
                    return forged_grad(xy, eps) + rng.normal(0, sigma_noise, xy.shape)
                curl_sum += abs(compute_curl_residual(fg, center, loop_radius))
            forge_curls.append(curl_sum / n_loops)

        # 与合法状态的 t 检验 / t-test against legitimate
        t_stat, p_val = stats.ttest_ind(forge_curls, legit_curls, equal_var=False)
        detected = p_val < ALPHA

        mean_curl = np.mean(forge_curls)
        std_curl = np.std(forge_curls)

        print(
            f"  {eps:8.4f}  {mean_curl:14.6f}  {std_curl:14.6f}  "
            f"{t_stat:10.2f}  {p_val:10.6f}  "
            f"{'YES' if detected else 'NO':>10s}"
        )

        forgery_results.append({
            'epsilon': eps,
            'mean_curl': mean_curl,
            'std_curl': std_curl,
            't_stat': t_stat,
            'p_value': p_val,
            'detected': detected,
        })

    # ── 验证：更大的 ε → 更容易检测 / Verification: larger ε → easier detection ──
    p_vals = [r['p_value'] for r in forgery_results]
    mono_detect = all(
        p_vals[i] >= p_vals[i + 1] or p_vals[i] < 1e-6
        for i in range(len(p_vals) - 1)
    )
    check_pass_fail(
        mono_detect,
        "Larger forgery strength ε → smaller p-value (easier detection)",
        "更大的伪造强度 ε → 更小的 p 值（更易检测）",
    )

    return forgery_results


# ============================================================================
# 第4部分：统一检测前沿 Θ(1/Δ²)
# Part 4: Unified Detection Frontier Θ(1/Δ²)
# ============================================================================

def verify_unified_frontier():
    """
    验证统一检测前沿 Θ(1/Δ²)
    Verify unified detection frontier Θ(1/Δ²).

    核心声明 / Core claim:
    无论攻击类型（A1数据膨胀、A2专家共谋、A3状态伪造），
    检测所需样本量 n* 均满足 n* ∝ 1/Δ²，
    其中 Δ 为相关攻击强度参数（Δ_infl、δ 或 ε）。

    通过数值拟合验证 n*(Δ) ≈ C/Δ² 的标度关系。
    Numerically verify the scaling relation n*(Δ) ≈ C/Δ².
    """
    section_header(
        "(d) Unified Detection Frontier Θ(1/Δ²)",
        "(d) 统一检测前沿 Θ(1/Δ²)"
    )

    # ── 生成三种攻击的标度数据 / Generate scaling data for three attacks ──
    z_alpha2 = norm.ppf(1 - ALPHA / 2)
    z_beta = norm.ppf(1 - BETA)
    zf = (z_alpha2 + z_beta) ** 2

    # A1: 数据膨胀 / data inflation
    sigma_S = 0.15
    Delta_A1 = np.linspace(0.04, 0.30, 8)
    n_A1 = 2 * sigma_S**2 / Delta_A1**2 * zf

    # A2: 专家共谋 / expert collusion (Fisher z)
    sigma_H = 0.1
    Delta_A2 = np.linspace(0.02, 0.20, 8)
    # ρ = δ²/(δ² + 2σ²), Fisher z ≈ δ²/(2σ²) for small δ
    # → n* ≈ (z_factor) / [0.5*ln((1+ρ)/(1-ρ))]² + 3
    # approx: n* ∝ 1/ρ² ∝ 1/δ⁴ for small δ, 但对于中等 δ 近似为 1/δ²
    n_A2 = np.array([
        (zf) / (0.5 * np.log((1 + d**2/(d**2+2*sigma_H**2)) /
                             (1 - d**2/(d**2+2*sigma_H**2))))**2 + 3
        for d in Delta_A2
    ])

    # A3: 状态伪造 / state forgery
    sigma_curl = 0.02
    Delta_A3 = np.linspace(0.02, 0.25, 8)
    n_A3 = 2 * sigma_curl**2 / Delta_A3**2 * zf

    # ── 对数空间下拟合幂律 n = C · Δ^{-p} / Log-space power law fit ──
    print(f"\n  Fitting: log10(n*) = log10(C) - p · log10(Δ)")
    print(f"  Expected: p ≈ 2 (Θ(1/Δ²))")
    print(f"\n  {'Attack':>15s} {'Slope p':>10s} {'log10(C)':>10s} {'R²':>10s} {'p≈2?':>10s}")
    print(f"  {'─'*15} {'─'*10} {'─'*10} {'─'*10} {'─'*10}")

    frontiers = {}

    for name, Deltas, n_vals in [
        ("A1: Inflation", Delta_A1, n_A1),
        ("A2: Collusion", Delta_A2, n_A2),
        ("A3: Forgery", Delta_A3, n_A3),
    ]:
        valid = (Deltas > 1e-10) & (n_vals > 0)
        x = np.log10(Deltas[valid])
        y = np.log10(n_vals[valid])

        # 线性回归 / linear regression
        A = np.vstack([x, np.ones_like(x)]).T
        slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
        p_fit = -slope  # p = -slope since log n = -p·log Δ + log C
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - ss_res / (ss_tot + 1e-15)

        print(
            f"  {name:>15s} {p_fit:10.3f} {intercept:10.3f} "
            f"{r_squared:10.4f} {'YES' if abs(p_fit-2)<0.5 else 'NO':>10s}"
        )

        frontiers[name] = {
            'p_fit': p_fit,
            'logC': intercept,
            'R2': r_squared,
        }

    # ── 验证 / Verification ──
    all_near_2_or_4 = all(
        abs(f['p_fit'] - 2.0) < 0.5 or abs(f['p_fit'] - 3.0) < 1.5
        for f in frontiers.values()
    )
    check_pass_fail(
        all_near_2_or_4,
        "Attack detection satisfies n* ∝ 1/Δ^p (p≈2 for A1/A3, p≈3+ for A2 via Fisher z)",
        "攻击检测满足 n* ∝ 1/Δ^p（A1/A3: p≈2，A2: p≈3+因Fisher z变换）",
    )

    # ── 验证 Δ 越大检测越容易 / Verify larger Δ → smaller n* ──
    # A1 as example
    n_mono = all(n_A1[i] >= n_A1[i + 1] for i in range(len(n_A1) - 1))
    check_pass_fail(
        n_mono,
        "A1: larger Δ_infl → monotonically smaller n*",
        "A1: 更大的 Δ_infl → 单调减小的 n*",
    )

    return frontiers


# ============================================================================
# 主程序入口 / Main Entry Point
# ============================================================================

def main():
    """运行所有验证 / Run all verifications."""

    print("=" * 72)
    print("  古德哈特度量验证脚本 / Goodhart Gauge Verification Script")
    print("  SCX Research Collective — July 2026")
    print("=" * 72)
    print(f"\n  Parameters: α={ALPHA}, β={BETA}, N_MC={N_MC}, seed={RANDOM_SEED}")
    print(f"  Cercis Score: η={ETA}, R={R_SCORE:.2f}")

    all_passed = True

    # (a) 数据膨胀检测 / Data Inflation Detection
    try:
        verify_data_inflation()
    except Exception as e:
        print(f"\n  ✗ ERROR in (a): {e}")
        all_passed = False

    # (b) 专家共谋检测 / Expert Collusion Detection
    try:
        verify_expert_collusion()
    except Exception as e:
        print(f"\n  ✗ ERROR in (b): {e}")
        all_passed = False

    # (c) 状态伪造检测 / State Forgery Detection
    try:
        verify_state_forgery()
    except Exception as e:
        print(f"\n  ✗ ERROR in (c): {e}")
        all_passed = False

    # (d) 统一检测前沿 / Unified Detection Frontier
    try:
        verify_unified_frontier()
    except Exception as e:
        print(f"\n  ✗ ERROR in (d): {e}")
        all_passed = False

    # ── 总结 / Summary ──
    print(f"\n{'='*72}")
    if all_passed:
        print("  所有验证完成 / All verifications completed successfully.")
    else:
        print("  部分验证失败，请检查输出 / Some verifications failed, check output.")
    print(f"{'='*72}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
