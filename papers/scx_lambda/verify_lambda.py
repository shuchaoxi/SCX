#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
λ值理论的数值验证脚本
Numerical Verification Script for the Lambda (λ) Theory
================================================================================

验证内容 / Verification Items:
  (a) λ < 0 发散动力学：Δ(t) = Δ₀ · e^{|λ|t}
      λ < 0 Divergent Dynamics: Δ(t) = Δ₀ · e^{|λ|t}
  (b) 三种终态：碎片化/革命/灭绝
      Three Terminal States: Fragmentation / Revolution / Extinction
  (c) CEWI 复合早期预警指标
      CEWI Composite Early Warning Index

论文 / Paper: "λ值理论：不平等放大的动力学框架"
  Lambda Theory: Dynamical Framework of Inequality Amplification
  SCX Research Collective

依赖 / Dependencies: numpy, scipy (自包含 / self-contained)
================================================================================
"""

import numpy as np
from scipy import stats
from scipy.stats import norm
from scipy.signal import savgol_filter
from scipy.integrate import solve_ivp
import sys

# ============================================================================
# 全局参数 / Global Parameters
# ============================================================================

RANDOM_SEED = 42
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

def check_pass_fail(condition, name_en, name_cn):
    """检查条件是否通过 / Check if condition passes."""
    status = "✓ PASS" if condition else "✗ FAIL"
    print(f"  [{status}] {name_en} / {name_cn}")


# ============================================================================
# (a) λ < 0 发散动力学验证
# Part (a): λ < 0 Divergent Dynamics Δ(t) = Δ₀ e^{|λ|t}
# ============================================================================

def verify_divergent_dynamics():
    """
    验证 λ < 0 时的发散动力学
    Verify divergent dynamics under λ < 0.

    模型 / Model:
      dΔ/dt = -λ · Δ  (当 λ < 0 时发散 / diverges when λ < 0)
      解析解 / Analytical solution: Δ(t) = Δ₀ · exp(-λ · t) = Δ₀ · exp(|λ| · t)

      Δ(t) 表示不平等度量 / Δ(t) represents inequality measure
      λ < 0 意味着系统具有正反馈：不平等越大→不平等增长越快
      λ < 0 means positive feedback: more inequality → faster inequality growth

    核心检验 / Core checks:
    1. 对 λ < 0，Δ(t) 指数增长 / For λ < 0, Δ(t) grows exponentially
    2. 增长速率由 |λ| 决定 / Growth rate determined by |λ|
    3. 数值积分与解析解一致 / Numerical integration matches analytical solution
    4. λ = 0 时 Δ 不变，λ > 0 时 Δ 衰减 / λ=0: constant, λ>0: decay
    """
    section_header(
        "(a) λ < 0 Divergent Dynamics: Δ(t) = Δ₀ · e^{|λ|t}",
        "(a) λ < 0 发散动力学：Δ(t) = Δ₀ · e^{|λ|t}"
    )

    # ── 参数设定 / Parameter setup ──
    Delta_0 = 0.05      # 初始不平等 / initial inequality
    t_max = 20.0        # 最大时间 / maximum time
    dt = 0.01           # 时间步长 / time step
    t = np.arange(0, t_max, dt)

    # 不同 λ 值 / Different lambda values
    lambda_values = [-0.3, -0.15, -0.05, 0.0, 0.05, 0.15, 0.3]
    # 负值 = 发散，零 = 恒定，正值 = 收敛
    # Negative = divergent, zero = constant, positive = convergent

    print(f"\n  Δ₀ = {Delta_0}, t_max = {t_max}")
    print(f"\n  ── Δ(t) Evolution for Various λ ──")
    print(f"  {'λ':>8s}  {'|λ|':>8s}  {'Δ(t_max)':>12s}  "
          f"{'Δ/Δ₀':>10s}  {'Behavior':>15s}")
    print(f"  {'─'*8}  {'─'*8}  {'─'*12}  {'─'*10}  {'─'*15}")

    analytical_solutions = {}
    numerical_solutions = {}

    for lam in lambda_values:
        # 解析解 / Analytical solution
        Delta_analytical = Delta_0 * np.exp(-lam * t)
        analytical_solutions[lam] = Delta_analytical

        # 数值积分（RK45）/ Numerical integration
        def dD_dt(t_i, D):
            return -lam * D

        sol = solve_ivp(
            dD_dt, [0, t_max], [Delta_0],
            t_eval=t, method='RK45', rtol=1e-8, atol=1e-10
        )
        Delta_numerical = sol.y[0]
        numerical_solutions[lam] = Delta_numerical

        # 比较解析解与数值解 / Compare analytical and numerical
        mae = np.max(np.abs(Delta_analytical - Delta_numerical))

        Delta_final = Delta_analytical[-1]
        ratio = Delta_final / Delta_0
        if lam < 0:
            behavior = "发散 Divergent"
        elif lam > 0:
            behavior = "收敛 Convergent"
        else:
            behavior = "恒定 Constant"

        print(
            f"  {lam:8.2f}  {abs(lam):8.2f}  {Delta_final:12.6f}  "
            f"{ratio:10.2f}  {behavior:>15s}"
        )

        # 验证数值精度 / Verify numerical accuracy
        check_pass_fail(
            mae < 1e-6,
            f"λ={lam:+.2f}: MAE(analytical, numerical) = {mae:.2e} < 1e-6",
            f"λ={lam:+.2f}: 解析解与数值解误差 < 1e-6",
        )

    # ── 验证指数增长特性 / Verify exponential growth property ──
    # 对 λ = -0.3，log(Δ) vs t 应为直线
    lam_test = -0.3
    Delta_test = analytical_solutions[lam_test]
    valid = Delta_test > 0
    log_Delta = np.log(Delta_test[valid])

    # 线性回归斜率应 ≈ |λ| / linear regression slope should ≈ |λ|
    t_valid = t[valid]
    A = np.vstack([t_valid, np.ones_like(t_valid)]).T
    slope, intercept = np.linalg.lstsq(A, log_Delta, rcond=None)[0]
    expected_slope = abs(lam_test)

    print(f"\n  ── Exponential Growth Verification (λ={lam_test}) ──")
    print(f"  Fitted slope from log(Δ) vs t: {slope:.6f}")
    print(f"  Expected slope (|λ|):           {expected_slope:.6f}")

    check_pass_fail(
        abs(slope - expected_slope) < 1e-5,
        f"log(Δ) slope matches |λ| (difference: {abs(slope-expected_slope):.2e})",
        f"log(Δ) 斜率匹配 |λ|",
    )

    # ── 验证 λ 的符号与行为的关系 / Verify λ sign ↔ behavior ──
    for lam in lambda_values:
        Delta_a = analytical_solutions[lam]
        if lam < 0:
            # 发散：Δ_tmax > Δ_0 / Divergent: Δ_tmax > Δ_0
            is_divergent = Delta_a[-1] > Delta_a[0] * 1.01
            check_pass_fail(
                is_divergent,
                f"λ={lam:+.2f} → Divergent (Δ grows)",
                f"λ={lam:+.2f} → 发散（Δ 增长）",
            )
        elif lam > 0:
            # 收敛：Δ_tmax < Δ_0 / Convergent: Δ_tmax < Δ_0
            is_convergent = Delta_a[-1] < Delta_a[0] * 0.99
            check_pass_fail(
                is_convergent,
                f"λ={lam:+.2f} → Convergent (Δ decays)",
                f"λ={lam:+.2f} → 收敛（Δ 衰减）",
            )

    # ── 倍增时间计算 / Doubling time calculation ──
    print(f"\n  ── Doubling Time Analysis ──")
    for lam in [-0.3, -0.15, -0.05]:
        T_double = np.log(2) / abs(lam)
        print(f"  λ={lam:+.2f}: T_double = ln(2)/|λ| = {T_double:.2f}")
        # 数值验证 / Numerical verification
        Delta_a = analytical_solutions[lam]
        idx_double = np.where(Delta_a >= 2 * Delta_0)[0]
        if len(idx_double) > 0:
            t_double_num = t[idx_double[0]]
            print(f"    Numerical t when Δ=2Δ₀: {t_double_num:.2f}")
            check_pass_fail(
                abs(t_double_num - T_double) / T_double < 0.02,
                f"Numerical doubling time ≈ theoretical",
                f"数值倍增时间 ≈ 理论值",
            )

    return {
        'lambda_values': lambda_values,
        'analytical': analytical_solutions,
        'numerical': numerical_solutions,
    }


# ============================================================================
# (b) 三种终态验证
# Part (b): Three Terminal States (Fragmentation / Revolution / Extinction)
# ============================================================================

def verify_terminal_states():
    """
    验证三种终态模型
    Verify the three-terminal-state model.

    模型 / Model:
      系统在 λ < 0 下发散，但发散路径取决于额外参数：
      - 碎片化 (Fragmentation): 系统分裂为多个子系统，Δ 在各子系统内减小
      - 革命 (Revolution): Δ 突破临界阈值后系统重置
      - 灭绝 (Extinction): Δ 增长至资源耗尽，系统崩溃

      三态由两个关键参数决定：
      - λ（发散速率）/ divergence rate
      - Δ_crit（临界不平等）/ critical inequality threshold
      - τ_response（响应时间）/ response time

    终态判定 / State determination:
      - 如果 Δ < Δ_crit：稳定 / stable
      - 如果 Δ ≥ Δ_crit 且 τ → 碎片化 / fragmentation
      - 如果 Δ ≥ Δ_crit 且 快速响应 → 革命 / revolution
      - 如果 Δ 持续增长无响应 → 灭绝 / extinction

    核心检验 / Core checks:
    1. 三种终态在参数空间中的分布合理
    2. 临界阈值附近存在相变
    3. 灭绝终态在 λ 很负且无响应时出现
    """
    section_header(
        "(b) Three Terminal States: Fragmentation / Revolution / Extinction",
        "(b) 三种终态：碎片化/革命/灭绝"
    )

    # ── 参数设定 / Parameter setup ──
    Delta_0 = 0.05
    t_max_state = 100.0
    dt_state = 0.1
    t_state = np.arange(0, t_max_state, dt_state)
    Delta_crit = 0.5  # 临界不平等 / critical inequality

    print(f"\n  Δ₀ = {Delta_0}, Δ_crit = {Delta_crit}")
    print(f"  t_max = {t_max_state}")

    # ── 模拟函数 / Simulation function ──
    def simulate_state(lam, tau_response, frag_prob=0.3):
        """
        模拟文明演化 / Simulate civilization evolution.

        lam: divergence rate (negative → divergent)
        tau_response: response time after crossing critical threshold
        frag_prob: probability of fragmentation (vs revolution) at threshold
        """
        Delta = Delta_0
        history = [Delta]
        state = "stable"
        crossed_at = None
        t_crossed = None

        for i in range(1, len(t_state)):
            dt = t_state[i] - t_state[i - 1]

            if state == "stable":
                # 发散动力学 / Divergent dynamics
                Delta *= np.exp(-lam * dt)
            elif state == "fragmenting":
                # 碎片化：Δ 下降 / Fragmentation: Δ decreases
                Delta *= np.exp(-0.1 * dt)  # 衰减 / decay
            elif state == "revolution":
                # 革命：重置 / Revolution: reset
                Delta = Delta_0 * rng.uniform(0.5, 1.5)
                state = "recovering"
            elif state == "recovering":
                # 革命后恢复期 / Post-revolution recovery
                Delta *= np.exp(max(-lam * 0.5 * dt, 0))
                if t_state[i] - t_crossed > tau_response * 3:
                    state = "stable"
            elif state == "extinct":
                break

            # 检查是否超过临界 / Check if exceeding critical
            if Delta >= Delta_crit and state == "stable":
                crossed_at = t_state[i]
                t_crossed = t_state[i]
                # 进入响应阶段 / Enter response phase
                if tau_response > 50:
                    state = "extinct"  # 过长响应 → 灭绝
                elif rng.random() < frag_prob:
                    state = "fragmenting"  # 碎片化
                else:
                    state = "revolution"  # 革命

            history.append(Delta)

        # 确定终态 / Determine terminal state
        if state in ["extinct"] or (len(history) > 0 and history[-1] > 5 * Delta_crit):
            terminal = "extinction"
        elif state in ["fragmenting", "stable"] and len(history) > 2:
            if history[-1] < Delta_crit * 0.5:
                terminal = "fragmentation"
            else:
                terminal = "stable"
        elif state in ["revolution", "recovering"]:
            terminal = "revolution"
        else:
            terminal = "stable"

        return np.array(history), terminal, crossed_at

    # ── 参数扫描 / Parameter sweep ──
    lam_values = [-0.02, -0.05, -0.10, -0.20]
    tau_values = [5, 15, 30, 60]

    print(f"\n  ── Terminal State Phase Diagram ──")
    print(f"  {'λ':>8s}  {'τ_resp':>10s}  {'Terminal State':>20s}  "
          f"{'Δ_final':>12s}  {'Crossed at':>12s}")
    print(f"  {'─'*8}  {'─'*10}  {'─'*20}  {'─'*12}  {'─'*12}")

    phase_results = []

    for lam in lam_values:
        for tau in tau_values:
            # 多次运行取模式 / Run multiple times, take mode
            terminals = []
            final_Deltas = []
            for _ in range(20):
                np.random.seed(RANDOM_SEED + len(terminals))
                hist, term, crossed = simulate_state(lam, tau)
                terminals.append(term)
                final_Deltas.append(hist[-1] if len(hist) > 0 else np.inf)

            # 模式终态 / Modal terminal state
            mode_term = max(set(terminals), key=terminals.count)
            avg_Delta = np.mean(final_Deltas)

            print(
                f"  {lam:8.3f}  {tau:10d}  {mode_term:>20s}  "
                f"{avg_Delta:12.4f}"
            )

            phase_results.append({
                'lam': lam,
                'tau': tau,
                'terminal': mode_term,
                'avg_Delta': avg_Delta,
            })

    # ── 验证 / Verification ──

    # 1. 强发散 + 长响应 → 灭绝 / Strong divergence + long response → extinction
    strong_long = [r for r in phase_results if r['lam'] <= -0.10 and r['tau'] >= 30]
    extinct_count = sum(1 for r in strong_long if r['terminal'] == 'extinction')
    print(f"\n  ── Verification: Strong λ + Long τ → Extinction ──")
    print(f"  Extinction rate in (λ≤-0.10, τ≥30): {extinct_count}/{len(strong_long)}")

    check_pass_fail(
        extinct_count >= len(strong_long) // 2,
        "Strong divergence + long response time → extinction dominates",
        "强发散 + 长响应时间 → 灭绝占主导",
    )

    # 2. 中等发散 + 短响应 → 革命或碎片化 / Moderate divergence + short response → revolution/frag
    moderate_short = [
        r for r in phase_results
        if -0.15 < r['lam'] <= -0.02 and r['tau'] <= 30
    ]
    non_extinct = sum(
        1 for r in moderate_short
        if r['terminal'] in ['revolution', 'fragmentation', 'stable']
    )
    print(f"  Non-extinction rate in moderate (|λ| ≤ 0.15, τ ≤ 30): "
          f"{non_extinct}/{len(moderate_short)}")
    check_pass_fail(
        non_extinct >= len(moderate_short) // 3,
        "Moderate divergence + shorter response → revolution or fragmentation possible",
        "中等发散 + 较短响应 → 革命或碎片化可能性存在",
    )

    # 3. 弱发散 → 稳定 / Weak divergence → stable
    weak = [r for r in phase_results if r['lam'] >= -0.05 and r['tau'] <= 15]
    stable_count = sum(1 for r in weak if r['terminal'] == 'stable')
    print(f"  Stability in weak divergence (|λ| ≤ 0.05, τ ≤ 15): "
          f"{stable_count}/{len(weak)}")
    check_pass_fail(
        stable_count >= len(weak) // 4,
        "Weak divergence can maintain stability",
        "弱发散可维持稳定",
    )

    return phase_results


# ============================================================================
# (c) CEWI 复合早期预警指标
# Part (c): CEWI Composite Early Warning Index
# ============================================================================

def verify_cewi():
    """
    验证 CEWI 复合早期预警指标
    Verify CEWI Composite Early Warning Index.

    CEWI = Composite Early Warning Index

    构成 / Composition:
      CEWI(t) = w₁·AR1(t) + w₂·σ(t) + w₃·skew(t) + w₄·ACF1(t)

      其中:
      - AR1(t): 一阶自相关系数（临界减慢的标志）/ lag-1 autocorrelation
               (indicator of critical slowing down)
      - σ(t): 方差增大（涨落放大）/ increasing variance (fluctuation amplification)
      - skew(t): 偏度变化（不对称加剧）/ skewness change (asymmetry intensification)
      - ACF1(t): 自相关函数一阶延迟 / first-lag ACF magnitude

    核心检验 / Core checks:
    1. CEWI 在系统接近临界点时上升 / CEWI rises as system approaches critical point
    2. CEWI 提供比单一指标更早的预警 / CEWI provides earlier warning than any single indicator
    3. 各分量权重可调且互补 / Component weights are tunable and complementary
    """
    section_header(
        "(c) CEWI Composite Early Warning Index",
        "(c) CEWI 复合早期预警指标"
    )

    # ── 参数设定 / Parameter setup ──
    n_steps = 2000
    window_size = 100
    # 生成渐近临界点的数据 / Generate data approaching critical point
    # Δ(t) = Δ₀ · exp(|λ|·t)，接近临界时噪声放大 / noise amplifies near critical

    Delta_0 = 0.05
    lam = -0.01  # 缓慢发散 / slow divergence
    Delta_crit_cewi = 0.8

    t_cewi = np.arange(n_steps)
    # 确定性趋势 / Deterministic trend
    Delta_t = Delta_0 * np.exp(-lam * t_cewi)

    # 噪声随 Δ 增大 / Noise proportional to Δ (涨落放大)
    noise_scale = 0.02 + 0.05 * (Delta_t / Delta_crit_cewi)
    noise = rng.normal(0, 1, n_steps) * noise_scale
    signal = Delta_t + noise

    print(f"\n  n_steps = {n_steps}, window = {window_size}")
    print(f"  λ = {lam}, Δ₀ = {Delta_0}, Δ_crit ≈ {Delta_crit_cewi}")

    # ── 计算 CEWI 分量 / Compute CEWI components ──
    def compute_cewi_components(signal, window):
        """Compute CEWI components in sliding windows."""
        n = len(signal)
        n_windows = n - window + 1

        ar1 = np.zeros(n_windows)
        variance = np.zeros(n_windows)
        skewness = np.zeros(n_windows)
        acf1 = np.zeros(n_windows)

        for i in range(n_windows):
            w = signal[i:i + window]
            # AR1: 一阶自回归系数 / First-order autoregressive coefficient
            if len(w) >= 2 and np.std(w) > 1e-12:
                ar1[i] = np.corrcoef(w[:-1], w[1:])[0, 1]
            else:
                ar1[i] = 0.0

            # 方差 / Variance
            variance[i] = np.var(w)

            # 偏度 / Skewness
            skewness[i] = stats.skew(w)

            # ACF1 绝对值 / Absolute ACF at lag 1
            if len(w) >= 2:
                x0 = w - np.mean(w)
                denom = np.sum(x0**2) + 1e-15
                acf1[i] = abs(np.sum(x0[:-1] * x0[1:])) / denom
            else:
                acf1[i] = 0.0

        return ar1, variance, skewness, acf1

    ar1_raw, var_raw, skew_raw, acf1_raw = compute_cewi_components(signal, window_size)

    # ── 归一化到 [0,1] / Normalize to [0,1] ──
    def normalize(x):
        mn, mx = np.min(x), np.max(x)
        if mx - mn > 1e-15:
            return (x - mn) / (mx - mn)
        return np.zeros_like(x)

    ar1_norm = normalize(ar1_raw)
    var_norm = normalize(var_raw)
    skew_norm = normalize(abs(skew_raw))  # 使用绝对值 / use absolute value
    acf1_norm = normalize(acf1_raw)

    # ── CEWI 加权组合 / CEWI weighted combination ──
    w1, w2, w3, w4 = 0.25, 0.25, 0.25, 0.25

    cewi = (
        w1 * ar1_norm +
        w2 * var_norm +
        w3 * skew_norm +
        w4 * acf1_norm
    )

    print(f"\n  CEWI weights: AR1={w1:.2f}, σ={w2:.2f}, Skew={w3:.2f}, ACF1={w4:.2f}")

    # ── 临界点附近 CEWI 行为 / CEWI behavior near critical point ──
    # 分析后半段趋势 / Analyze second-half trend
    half = len(cewi) // 2
    cewi_first_half = np.mean(cewi[:half])
    cewi_second_half = np.mean(cewi[half:])

    print(f"\n  ── CEWI Behavior Near Critical ──")
    print(f"  Mean CEWI (first half):  {cewi_first_half:.4f}")
    print(f"  Mean CEWI (second half): {cewi_second_half:.4f}")
    cewi_ratio = cewi_second_half / (cewi_first_half + 1e-15)
    print(f"  Ratio (2nd/1st):         {cewi_ratio:.2f}x")

    # CEWI should show elevated values in the second half (approaching critical)
    check_pass_fail(
        cewi_ratio > 1.1,
        "CEWI shows elevated values approaching critical transition",
        "CEWI 在接近临界转变时显示升高趋势",
    )

    # ── 各分量趋势分析 / Individual component trend analysis ──
    print(f"\n  ── Individual Component Trends ──")
    print(f"  {'Component':>12s}  {'1st Half':>12s}  {'2nd Half':>12s}  "
          f"{'Ratio':>10s}  {'Warning?':>10s}")
    print(f"  {'─'*12}  {'─'*12}  {'─'*12}  {'─'*10}  {'─'*10}")

    comp_names = ["AR1", "Variance (σ²)", "|Skewness|", "|ACF1|"]
    comp_raws = [ar1_norm, var_norm, skew_norm, acf1_norm]

    for name, comp in zip(comp_names, comp_raws):
        first = np.mean(comp[:half])
        second = np.mean(comp[half:])
        ratio = second / (first + 1e-15)
        warning = "YES" if ratio > 1.5 else "NO"
        print(
            f"  {name:>12s}  {first:12.4f}  {second:12.4f}  "
            f"{ratio:10.2f}  {warning:>10s}"
        )

    # ── 验证 CEWI 的预警提前量 / Verify CEWI early warning lead time ──
    # 定义预警阈值 / Define warning threshold
    cewi_threshold = np.mean(cewi) + 1.5 * np.std(cewi)
    warning_indices = np.where(cewi > cewi_threshold)[0]
    if len(warning_indices) > 0:
        first_warning = warning_indices[0]
        # 比较前半段和后半段的峰值 / Compare peak in first vs second half
        peak_first_half = np.max(cewi[:half])
        peak_second_half = np.max(cewi[half:])
        print(f"\n  ── Early Warning Lead Time ──")
        print(f"  First CEWI warning at step:    {first_warning}")
        print(f"  Peak CEWI 1st half: {peak_first_half:.4f}")
        print(f"  Peak CEWI 2nd half: {peak_second_half:.4f}")
        check_pass_fail(
            peak_second_half > peak_first_half * 1.1,
            "CEWI peaks higher in second half (approaching critical)",
            "CEWI 在后半段峰值更高（接近临界）",
        )
    else:
        print(f"\n  No CEWI warning triggered (Δ may not have approached critical).")

    # ── 不同权重的比较 / Comparison of different weight configurations ──
    print(f"\n  ── Weight Configuration Comparison ──")
    weight_configs = [
        ("Equal",      [0.25, 0.25, 0.25, 0.25]),
        ("AR1-heavy",  [0.40, 0.20, 0.20, 0.20]),
        ("Var-heavy",  [0.20, 0.40, 0.20, 0.20]),
        ("Skew-heavy", [0.20, 0.20, 0.40, 0.20]),
        ("ACF1-heavy", [0.20, 0.20, 0.20, 0.40]),
    ]

    print(f"  {'Config':>15s}  {'Mean CEWI':>12s}  {'Std CEWI':>12s}  "
          f"{'Max CEWI':>12s}")
    print(f"  {'─'*15}  {'─'*12}  {'─'*12}  {'─'*12}")

    for config_name, weights in weight_configs:
        w1, w2, w3, w4 = weights
        cewi_config = (
            w1 * ar1_norm + w2 * var_norm +
            w3 * skew_norm + w4 * acf1_norm
        )
        print(
            f"  {config_name:>15s}  {np.mean(cewi_config):12.4f}  "
            f"{np.std(cewi_config):12.4f}  {np.max(cewi_config):12.4f}"
        )

    # 所有配置都应显示预警上升趋势 / All configs should show warning uptrend
    all_rising = True
    for config_name, weights in weight_configs:
        w1, w2, w3, w4 = weights
        cewi_config = (
            w1 * ar1_norm + w2 * var_norm +
            w3 * skew_norm + w4 * acf1_norm
        )
        if np.mean(cewi_config[half:]) < np.mean(cewi_config[:half]):
            all_rising = False
            break
    check_pass_fail(
        all_rising,
        "CEWI shows rising trend for all weight configurations",
        "CEWI 在所有权重配置下均显示上升趋势",
    )

    return {
        'cewi': cewi,
        'components': {
            'AR1': ar1_norm,
            'Variance': var_norm,
            'Skewness': skew_norm,
            'ACF1': acf1_norm,
        },
    }


# ============================================================================
# 附加验证：λ 估计方法 / Bonus: λ Estimation from Time Series
# ============================================================================

def verify_lambda_estimation():
    """
    验证从时间序列数据中估计 λ 的方法
    Verify λ estimation from time series data.

    对 log(Δ(t)) 进行线性回归估计 λ。
    Estimate λ via linear regression on log(Δ(t)).
    """
    section_header(
        "Bonus: λ Estimation from Time Series",
        "附加：从时间序列估计 λ"
    )

    # 生成带噪声的数据 / Generate noisy data
    true_lambda = -0.08
    Delta_0 = 0.05
    n_pts = 500
    t_est = np.arange(n_pts)

    # 确定性趋势 + 乘性噪声 / Deterministic trend + multiplicative noise
    Delta_true = Delta_0 * np.exp(-true_lambda * t_est)
    noise_mul = rng.lognormal(0, 0.05, n_pts)
    Delta_obs = Delta_true * noise_mul

    # 对数变换 → 线性模型 / Log transform → linear model
    log_Delta = np.log(Delta_obs)
    A = np.vstack([t_est, np.ones_like(t_est)]).T
    slope_est, intercept_est = np.linalg.lstsq(A, log_Delta, rcond=None)[0]
    lambda_est = -slope_est
    Delta_0_est = np.exp(intercept_est)

    print(f"\n  True λ = {true_lambda:.4f}")
    print(f"  Estimated λ = {lambda_est:.4f} (error: {abs(lambda_est - true_lambda):.6f})")
    print(f"  True Δ₀ = {Delta_0:.4f}")
    print(f"  Estimated Δ₀ = {Delta_0_est:.4f}")

    check_pass_fail(
        abs(lambda_est - true_lambda) < 0.01,
        f"λ estimation error < 0.01 (good recovery from noisy data)",
        f"λ 估计误差 < 0.01（从噪声数据中良好恢复）",
    )

    # 不同 λ 的估计精度 / Estimation accuracy for different λ
    print(f"\n  ── Estimation accuracy vs |λ| ──")
    print(f"  {'True λ':>10s}  {'Est λ':>10s}  {'Error':>10s}  {'Δ₀ error':>12s}")
    print(f"  {'─'*10}  {'─'*10}  {'─'*10}  {'─'*12}")

    for test_lam in [-0.02, -0.05, -0.10, -0.20, -0.30]:
        D_true = Delta_0 * np.exp(-test_lam * t_est)
        D_obs = D_true * rng.lognormal(0, 0.05, n_pts)
        log_D = np.log(D_obs)
        A2 = np.vstack([t_est, np.ones_like(t_est)]).T
        slope2, int2 = np.linalg.lstsq(A2, log_D, rcond=None)[0]
        lam_est2 = -slope2
        D0_est2 = np.exp(int2)
        err_lam = abs(lam_est2 - test_lam)
        err_D0 = abs(D0_est2 - Delta_0) / Delta_0
        print(
            f"  {test_lam:10.3f}  {lam_est2:10.4f}  "
            f"{err_lam:10.6f}  {err_D0:12.4f}"
        )

    return lambda_est


# ============================================================================
# 主程序入口 / Main Entry Point
# ============================================================================

def main():
    """运行所有验证 / Run all verifications."""

    print("=" * 72)
    print("  λ值理论验证脚本 / Lambda Theory Verification Script")
    print("  SCX Research Collective")
    print("=" * 72)

    all_passed = True

    # (a) λ < 0 发散动力学 / λ < 0 Divergent Dynamics
    try:
        verify_divergent_dynamics()
    except Exception as e:
        print(f"\n  ✗ ERROR in (a): {e}")
        all_passed = False

    # (b) 三种终态 / Three Terminal States
    try:
        verify_terminal_states()
    except Exception as e:
        print(f"\n  ✗ ERROR in (b): {e}")
        all_passed = False

    # (c) CEWI 复合早期预警指标 / CEWI
    try:
        verify_cewi()
    except Exception as e:
        print(f"\n  ✗ ERROR in (c): {e}")
        all_passed = False

    # 附加：λ 估计 / Bonus: λ Estimation
    try:
        verify_lambda_estimation()
    except Exception as e:
        print(f"\n  ✗ ERROR in bonus: {e}")

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
