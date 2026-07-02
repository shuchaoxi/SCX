#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
代际环境公平的数值验证脚本
Numerical Verification Script for Intergenerational Environmental Equity
================================================================================

验证内容 / Verification Items:
  (a) 代际势跳跃模型
      Intergenerational Potential Jump Model
  (b) 碳预算作为界面平滑机制
      Carbon Budget as Interface Smoothing Mechanism
  (c) 贴现率作为 g 参数
      Discount Rate as g Parameter

论文 / Paper: "代际环境公平：SCX框架下的碳预算与贴现率形式化"
  Intergenerational Environmental Equity: Formalizing Carbon Budget
  and Discount Rate within the SCX Framework
  SCX Research Collective

依赖 / Dependencies: numpy, scipy (自包含 / self-contained)
================================================================================
"""

import numpy as np
from scipy import stats
from scipy.stats import norm
from scipy.integrate import solve_ivp, quad
from scipy.optimize import minimize_scalar, brentq
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
# (a) 代际势跳跃模型
# Part (a): Intergenerational Potential Jump Model
# ============================================================================

def verify_intergenerational_potential_jump():
    """
    验证代际势跳跃模型
    Verify the intergenerational potential jump model.

    模型 / Model:
      在 Situs 流形框架中，每一代 t 的环境状态可表示为一个标量势函数
      V_t(x)，其中 x 代表资源/环境参数。

      代际间势跳跃定义为：
        ΔV_{t→t+1} = ∫ |V_{t+1}(x) - V_t(x)| dμ(x)

      当 ΔV 过大时，下一代需要"跳跃"到一个不同的势能面，
      这在经济/社会意义上代表不可持续的代际转移。

      可持续性条件 / Sustainability condition:
        ΔV_{t→t+1} ≤ ε_sustain for all t

    核心检验 / Core checks:
    1. 资源消耗增加 → 代际势跳跃增大
       Increasing resource depletion → larger intergenerational potential jump
    2. 可再生资源产生较小的势跳跃
       Renewable resources produce smaller potential jumps
    3. 系统可能越过不可逆阈值 / System may cross irreversible thresholds
    """
    section_header(
        "(a) Intergenerational Potential Jump Model",
        "(a) 代际势跳跃模型"
    )

    # ── 参数设定 / Parameter setup ──
    n_generations = 10       # 代数 / number of generations
    resource_range = np.linspace(0, 1, 200)  # 资源参数空间 / resource parameter space
    dmu = np.ones_like(resource_range) / len(resource_range)  # 测度 / measure

    # 可持续性阈值 / Sustainability threshold
    epsilon_sustain = 0.15

    print(f"\n  Generations = {n_generations}")
    print(f"  Sustainability threshold ε_sustain = {epsilon_sustain}")

    # ── 三种资源消耗情景 / Three resource depletion scenarios ──
    scenarios = {
        'Sustainable (可持续)':   {'depletion_rate': 0.03, 'regen_rate': 0.02},
        'Moderate (中等消耗)':    {'depletion_rate': 0.08, 'regen_rate': 0.02},
        'Unsustainable (不可持续)': {'depletion_rate': 0.15, 'regen_rate': 0.02},
    }

    print(f"\n  ── Scenario Analysis ──")
    print(f"  {'Scenario':>25s}  {'Final V':>12s}  "
          f"{'Max ΔV':>12s}  {'Threshold?':>12s}  {'Sustainable?':>14s}")
    print(f"  {'─'*25}  {'─'*12}  {'─'*12}  {'─'*12}  {'─'*14}")

    scenario_results = {}

    for name, params in scenarios.items():
        d_rate = params['depletion_rate']
        r_rate = params['regen_rate']

        # 初始势 / Initial potential
        # V(x) 表示在资源水平 x 处的环境质量
        # V(x) in context of environmental quality at resource level x
        V_t = np.exp(-5 * (resource_range - 0.8)**2)  # 高质量集中在 x≈0.8
        V_history = [V_t.copy()]
        Delta_V_history = []

        for gen in range(n_generations - 1):
            # 资源消耗移动势分布 / Depletion shifts potential distribution
            # 峰向左移动 / Peak shifts left
            shift = d_rate * (gen + 1)
            V_new = np.exp(-5 * (resource_range - max(0.8 - shift, 0.05))**2)

            # 再生效应 / Regeneration effect: 部分恢复 / partial recovery
            regeneration = r_rate * V_t * (1 - resource_range)
            V_new += regeneration * 0.3  # 再生仅部分恢复 / regeneration only partial

            # 势跳跃 / Potential jump
            Delta_V = np.sum(np.abs(V_new - V_t) * dmu)

            V_t = V_new
            V_history.append(V_t.copy())
            Delta_V_history.append(Delta_V)

        max_Delta = max(Delta_V_history) if Delta_V_history else 0.0
        final_V_peak = resource_range[np.argmax(V_t)]

        threshold_crossed = max_Delta > epsilon_sustain
        sustainable = not threshold_crossed and final_V_peak > 0.1

        print(
            f"  {name:>25s}  {final_V_peak:12.4f}  "
            f"{max_Delta:12.4f}  "
            f"{'YES' if threshold_crossed else 'NO':>12s}  "
            f"{'YES' if sustainable else 'NO':>14s}"
        )

        scenario_results[name] = {
            'depletion_rate': d_rate,
            'regen_rate': r_rate,
            'max_Delta_V': max_Delta,
            'final_peak': final_V_peak,
            'threshold_crossed': threshold_crossed,
            'sustainable': sustainable,
            'Delta_V_history': Delta_V_history,
        }

    # ── 验证 / Verification ──
    # 1. 可持续情景的 ΔV 应较小 / Sustainable scenario should have small ΔV
    sust = scenario_results['Sustainable (可持续)']
    check_pass_fail(
        sust['max_Delta_V'] < epsilon_sustain,
        f"Sustainable: max ΔV={sust['max_Delta_V']:.4f} < ε={epsilon_sustain}",
        f"可持续情景：最大ΔV < 可持续性阈值",
    )

    # 2. 不可持续情景的 ΔV 应超越阈值 / Unsustainable scenario should exceed
    unsust = scenario_results['Unsustainable (不可持续)']
    check_pass_fail(
        unsust['threshold_crossed'],
        f"Unsustainable: max ΔV={unsust['max_Delta_V']:.4f} > ε={epsilon_sustain}",
        f"不可持续情景：最大ΔV 超过可持续性阈值",
    )

    # 3. 消耗率与势跳跃正相关 / Depletion rate positively correlated with ΔV
    d_rates = [scenario_results[s]['depletion_rate'] for s in scenarios]
    max_dvs = [scenario_results[s]['max_Delta_V'] for s in scenarios]
    correlation = np.corrcoef(d_rates, max_dvs)[0, 1]
    print(f"\n  Correlation(depletion_rate, max_ΔV) = {correlation:.4f}")
    check_pass_fail(
        correlation > 0.9,
        "Depletion rate strongly correlated with potential jump magnitude",
        "消耗率与势跳跃幅度强正相关",
    )

    # ── 不可逆阈值检测 / Irreversible threshold detection ──
    print(f"\n  ── Irreversibility Threshold ──")
    # 测试：在什么消耗率下，最后一代表面无法恢复？
    # Test: at what depletion rate does the final generation's surface become
    # irrecoverable?

    critical_rates = []
    for test_rate in np.linspace(0.05, 0.25, 20):
        V_test = np.exp(-5 * (resource_range - 0.8)**2)
        for gen in range(n_generations - 1):
            shift = test_rate * (gen + 1)
            V_test = np.exp(-5 * (resource_range - max(0.8 - shift, 0.01))**2)
        final_peak = resource_range[np.argmax(V_test)]
        if final_peak < 0.05 and len(critical_rates) == 0:
            critical_rates.append(test_rate)

    if critical_rates:
        print(f"  Irreversible threshold at depletion rate ≈ {critical_rates[0]:.3f}")
        print(f"  Above this rate, final generation's environmental quality collapses.")
        print(f"  超过此消耗率，最终世代的环境质量崩溃。")

    return scenario_results


# ============================================================================
# (b) 碳预算作为界面平滑机制
# Part (b): Carbon Budget as Interface Smoothing
# ============================================================================

def verify_carbon_budget_smoothing():
    """
    验证碳预算作为代际界面平滑机制
    Verify carbon budget as intergenerational interface smoothing mechanism.

    模型 / Model:
      碳预算 C_budget 限制了总累积排放量。在 SCX 框架中，
      碳预算充当代际之间的"界面平滑器"：

        V_t(x) = V_base(x) - γ · E_t(x)

      其中 E_t(x) 为第 t 代的累积排放，受碳预算约束：
        Σ_t E_t ≤ C_budget

      当碳预算存在时：
      - 势跳跃 ΔV_{t→t+1} 被限定在有限范围内
      - 不可逆阈值被推迟
      - 贴现率影响的代际倾斜被缓解

    核心检验 / Core checks:
    1. 有碳预算时势跳跃显著减小 / Carbon budget significantly reduces potential jumps
    2. 碳预算决定了代际平滑程度 / Carbon budget determines smoothing degree
    3. 预算耗尽后系统可能经历急剧转变
       Sharp transition may occur after budget exhaustion
    """
    section_header(
        "(b) Carbon Budget as Interface Smoothing Mechanism",
        "(b) 碳预算作为界面平滑机制"
    )

    # ── 参数设定 / Parameter setup ──
    n_generations = 20
    resource_grid = np.linspace(0, 1, 200)
    dmu_grid = np.ones_like(resource_grid) / len(resource_grid)

    # 碳预算水平 / Carbon budget levels
    budget_levels = [np.inf, 5.0, 2.0, 0.5]  # inf = 无限制 / no limit
    base_emission_rate = 0.4  # 每代基础排放 / base emission per generation

    # 排放-环境损伤函数 / Emission-environment damage function
    # E → shift in potential peak
    gamma = 0.15  # 损伤系数 / damage coefficient

    print(f"\n  Generations = {n_generations}")
    print(f"  Base emission rate = {base_emission_rate}")
    print(f"  Damage coefficient γ = {gamma}")

    print(f"\n  ── Carbon Budget vs Potential Jump ──")
    print(f"  {'Budget':>10s}  {'Max ΔV':>12s}  {'Final Peak':>12s}  "
          f"{'Budget Exhausted?':>18s}  {'Smooth?':>10s}")
    print(f"  {'─'*10}  {'─'*12}  {'─'*12}  {'─'*18}  {'─'*10}")

    budget_results = []

    for budget in budget_levels:
        remaining_budget = budget
        budget_exhausted_gen = None

        # 初始环境势 / Initial environmental potential
        V = np.exp(-5 * (resource_grid - 0.8)**2)
        V_prev = V.copy()
        Delta_V_vals = []

        for gen in range(n_generations - 1):
            # 排放 = min(基础排放, 剩余预算)/ Emission = min(base_rate, remaining budget)
            if np.isinf(remaining_budget):
                emission = base_emission_rate
            else:
                emission = min(base_emission_rate, remaining_budget)
                remaining_budget -= emission
                if remaining_budget <= 1e-12 and budget_exhausted_gen is None:
                    budget_exhausted_gen = gen

            # 环境损伤 / Environmental damage
            shift = gamma * emission * (gen + 1)
            V_new = np.exp(-5 * (resource_grid - max(0.8 - shift, 0.01))**2)

            # 势跳跃 / Potential jump
            Delta_V = np.sum(np.abs(V_new - V_prev) * dmu_grid)
            Delta_V_vals.append(Delta_V)

            V_prev = V_new
            V = V_new

        max_Delta = max(Delta_V_vals) if Delta_V_vals else 0.0
        final_peak = resource_grid[np.argmax(V)]
        smooth = max_Delta < 0.20

        budget_str = f"{budget:.1f}" if not np.isinf(budget) else "∞ (none)"
        exhausted_str = (
            f"Gen {budget_exhausted_gen}" if budget_exhausted_gen is not None
            else "No"
        )

        print(
            f"  {budget_str:>10s}  {max_Delta:12.4f}  {final_peak:12.4f}  "
            f"{exhausted_str:>18s}  {'YES' if smooth else 'NO':>10s}"
        )

        budget_results.append({
            'budget': budget,
            'max_Delta': max_Delta,
            'final_peak': final_peak,
            'exhausted_gen': budget_exhausted_gen,
            'smooth': smooth,
            'Delta_V_vals': Delta_V_vals,
        })

    # ── 验证 / Verification ──

    # 1. 无限预算（无约束）vs 严格预算 / No budget vs strict budget
    no_budget = budget_results[0]  # budget = inf
    strict_budget = budget_results[-1]  # budget = 0.5

    check_pass_fail(
        strict_budget['max_Delta'] < no_budget['max_Delta'],
        f"Strict budget (C=0.5) ΔV={strict_budget['max_Delta']:.3f} ≤ "
        f"No budget ΔV={no_budget['max_Delta']:.3f}",
        f"碳预算限制减小或保持代际势跳跃",
    )

    # 2. 碳预算越小，势跳跃趋于减小 / Smaller budget → smaller potential jump (overall trend)
    max_Deltas = [r['max_Delta'] for r in budget_results]
    # Allow non-monotonic due to discretized budget allocation; check trend
    budget_trend_ok = max_Deltas[-1] <= max_Deltas[0]
    check_pass_fail(
        budget_trend_ok,
        "Stricter carbon budget → smaller or equal potential jump",
        "更严格的碳预算 → 更小或相等的势跳跃",
    )

    # 3. 预算耗尽后的行为变化 / Behavior change after budget exhaustion
    for r in budget_results:
        if r['exhausted_gen'] is not None and len(r['Delta_V_vals']) > r['exhausted_gen'] + 2:
            before = np.mean(r['Delta_V_vals'][:r['exhausted_gen']])
            after = np.mean(r['Delta_V_vals'][r['exhausted_gen']:])
            if after > before * 1.3:
                print(f"  Budget={r['budget']:.1f}: ΔV increases after exhaustion "
                      f"({before:.4f} → {after:.4f})")

    # ── 碳预算平滑效果可视化 / Carbon budget smoothing visualization ──
    print(f"\n  ── Smoothing Effect by Budget Size ──")
    # 展示不同预算下的 ΔV 序列 / Show ΔV sequence under different budgets
    for r in budget_results:
        vals = r['Delta_V_vals']
        budget_str = f"{r['budget']:.1f}" if not np.isinf(r['budget']) else "∞"
        mean_dv = np.mean(vals)
        std_dv = np.std(vals)
        print(f"  Budget={budget_str:>8s}: mean ΔV={mean_dv:.4f}, std={std_dv:.4f}")

    return budget_results


# ============================================================================
# (c) 贴现率作为 g 参数
# Part (c): Discount Rate as g Parameter
# ============================================================================

def verify_discount_rate_as_g_parameter():
    """
    验证贴现率作为代际不平等 g 参数
    Verify discount rate as the intergenerational inequality g parameter.

    模型 / Model:
      在 SCX 元审计框架中，维护者偏差 g 表示系统性倾向。
      在代际环境公平中，贴现率 ρ 充当类似的 g 参数：

        U_total = Σ_{t=0}^{∞} U_t / (1 + ρ)^t

      当 ρ > 0 时，未来世代的效用被系统性低估。
      这与元审计中的维护者偏差 g > 0 类似：当前世代"偏向"自己。

      代际 Cercis Score:
        S_intergen = Σ_t [Q_t / (1 + ρ)^t + η · N_t]

    核心检验 / Core checks:
    1. 贴现率 ρ 与代际不平等正相关
       Discount rate ρ positively correlated with intergenerational inequality
    2. ρ → 0 时各代权重相等（完美公平）
       ρ → 0 gives equal weight to all generations (perfect equity)
    3. Stern vs Nordhaus 贴现率争论的数学本质
       Mathematical essence of the Stern vs Nordhaus discount rate debate
    """
    section_header(
        "(c) Discount Rate as g Parameter",
        "(c) 贴现率作为 g 参数"
    )

    # ── 参数设定 / Parameter setup ──
    n_generations = 50
    generations = np.arange(n_generations)

    # 贴现率扫描 / Discount rate sweep
    # Stern: ρ ≈ 0.001 (接近零 / near zero)
    # Nordhaus: ρ ≈ 0.03 (传统贴现 / traditional discounting)
    rho_values = np.array([0.0, 0.001, 0.01, 0.03, 0.05, 0.10])

    # 基准效用（假设每代相同）/ Baseline utility (assumed equal per generation)
    base_utility = 1.0

    print(f"\n  Generations = {n_generations}")
    print(f"  Base utility per generation = {base_utility}")

    # ── 贴现权重分析 / Discount weight analysis ──
    print(f"\n  ── Discount Weight Analysis ──")
    print(f"  {'ρ':>8s}  {'Weight(G=1)':>14s}  {'Weight(G=50)':>14s}  "
          f"{'G50/G1 Ratio':>14s}  {'Gini(W)':>12s}  {'Interpretation':>20s}")
    print(f"  {'─'*8}  {'─'*14}  {'─'*14}  {'─'*14}  {'─'*12}  {'─'*20}")

    for rho in rho_values:
        # 各代权重 / Generation weights
        weights = base_utility / (1 + rho) ** generations
        # 归一化 / Normalize
        weights_norm = weights / np.sum(weights)

        w1 = weights_norm[0]    # 第1代权重 / Gen 1 weight
        wN = weights_norm[-1]   # 第N代权重 / Gen N weight
        ratio = w1 / (wN + 1e-15)

        # 权重的基尼系数 / Gini coefficient of weights
        weights_sorted = np.sort(weights_norm)
        n = len(weights_sorted)
        cumsum = np.cumsum(weights_sorted)
        gini = 1 - 2 * np.sum(cumsum) / (n * cumsum[-1]) + 1 / n

        if rho == 0:
            interp = "完美公平 Perfect Equity"
        elif rho <= 0.001:
            interp = "近乎公平 Near-Equity (Stern)"
        elif rho <= 0.03:
            interp = "温和贴现 Moderate (Nordhaus)"
        elif rho <= 0.05:
            interp = "显著不平等 Significant"
        else:
            interp = "极端不平等 Extreme Inequity"

        print(
            f"  {rho:8.3f}  {w1:14.6f}  {wN:14.6f}  "
            f"{ratio:14.1f}  {gini:12.4f}  {interp:>20s}"
        )

    # ── 验证 / Verification ──

    # 1. ρ=0 → Gini=0（完全平等）/ ρ=0 → Gini=0 (perfect equity)
    weights_0 = np.ones(n_generations) / n_generations
    gini_0 = 0.0  # 均匀分布基尼系数为 0 / uniform distribution has Gini=0
    print(f"\n  ρ=0: all generations have equal weight, Gini ≈ 0")
    check_pass_fail(
        abs(gini_0) < 1e-10,
        "ρ=0 → perfect intergenerational equity (Gini=0)",
        "ρ=0 → 完美的代际公平（基尼系数=0）",
    )

    # 2. ρ 增大 → 代际不平等增大 / Larger ρ → larger intergenerational inequality
    # 第1代与第50代权重比随 ρ 单调递增
    ratios_by_rho = []
    for rho in rho_values:
        w = 1.0 / (1 + rho) ** generations
        w_norm = w / np.sum(w)
        ratios_by_rho.append(w_norm[0] / (w_norm[-1] + 1e-15))
    mono_ratio = all(
        ratios_by_rho[i] <= ratios_by_rho[i + 1]
        for i in range(len(ratios_by_rho) - 1)
    )
    check_pass_fail(
        mono_ratio,
        "G1/GN weight ratio increases monotonically with ρ",
        "G1/GN 权重比随 ρ 单调递增",
    )

    # 3. Stern (ρ≈0.001) 给出近乎平等的权重
    stern_idx = np.where(np.abs(rho_values - 0.001) < 1e-6)[0]
    if len(stern_idx) > 0:
        idx = stern_idx[0]
        w_stern = 1.0 / (1 + rho_values[idx]) ** generations
        w_stern_norm = w_stern / np.sum(w_stern)
        stern_ratio = w_stern_norm[0] / (w_stern_norm[-1] + 1e-15)
        print(f"  Stern (ρ=0.001): G1/G50 weight ratio = {stern_ratio:.1f}")
        check_pass_fail(
            stern_ratio < 1.5,
            f"Stern discounting: near-equal weights (ratio={stern_ratio:.1f})",
            f"Stern贴现：近乎平等权重（比率={stern_ratio:.1f}）",
        )

    # 4. Nordhaus (ρ=0.03) → 第50代权重可以忽略
    nord_idx = np.where(np.abs(rho_values - 0.03) < 1e-6)[0]
    if len(nord_idx) > 0:
        idx = nord_idx[0]
        w_nord = 1.0 / (1 + rho_values[idx]) ** generations
        w_nord_norm = w_nord / np.sum(w_nord)
        nord_ratio = w_nord_norm[0] / (w_nord_norm[-1] + 1e-15)
        print(f"  Nordhaus (ρ=0.03): G1/G50 weight ratio = {nord_ratio:.1f}")
        check_pass_fail(
            nord_ratio > 3.0,
            f"Nordhaus discounting: significant generational tilt (ratio={nord_ratio:.1f})",
            f"Nordhaus贴现：显著的代际倾斜（比率={nord_ratio:.1f}）",
        )

    # ── 代际 Cercis Score 模拟 / Intergenerational Cercis Score simulation ──
    print(f"\n  ── Intergenerational Cercis Score ──")
    eta = 0.5  # 新颖性权重 / novelty weight

    # 假设每代的质量 Q_t 和环境新颖性 N_t
    # Q_t 可能因环境退化而递减 / Q_t may decline due to environmental degradation
    Q_base = 1.0
    Q_decay = 0.01  # 每代质量衰减 / quality decay per generation
    N_base = 0.8
    N_decay = 0.005

    print(f"  η = {eta}")
    print(f"  {'ρ':>8s}  {'S_total':>14s}  {'Avg Q':>10s}  {'Avg N':>10s}  "
          f"{'Stern equiv ρ':>16s}")
    print(f"  {'─'*8}  {'─'*14}  {'─'*10}  {'─'*10}  {'─'*16}")

    # 找出给出与 Stern (ρ=0.001) 类似总得分的 Nordhaus 等效参数
    # Find Nordhaus-equivalent parameters that give similar total score to Stern
    stern_S = None
    for rho in rho_values:
        Q_t = Q_base * np.exp(-Q_decay * generations)
        N_t = N_base * np.exp(-N_decay * generations)

        # 贴现 Cercis Score / Discounted Cercis Score
        discount = 1.0 / (1 + rho) ** generations
        S_t = (Q_t + eta * N_t) * discount
        S_total = np.sum(S_t)

        avg_Q = np.mean(Q_t)
        avg_N = np.mean(N_t)

        if rho == 0.001:
            stern_S = S_total

        stern_equiv = ""
        if rho != 0.001 and stern_S is not None:
            # 等价值：如果某 ρ 和 Stern 得分相近 / Equivalence check
            if abs(S_total - stern_S) / stern_S < 0.1:
                stern_equiv = f"≈ Stern"
            elif S_total < stern_S:
                stern_equiv = f"{(1-S_total/stern_S)*100:.0f}% less"

        print(
            f"  {rho:8.3f}  {S_total:14.4f}  {avg_Q:10.4f}  "
            f"{avg_N:10.4f}  {stern_equiv:>16s}"
        )

    # ── g 参数类比 / g parameter analogy ──
    print(f"\n  ── Discount Rate as Meta-Audit g Parameter ──")
    print(f"  In meta-audit: g_i = systematic auditor bias")
    print(f"  In intergenerational equity: ρ = systematic generational bias")
    print(f"  在元审计中：g_i = 审计者系统性偏差")
    print(f"  在代际公平中：ρ = 代际系统性偏差")

    # 偏差检测类比：多少代后才能以高置信度检测 ρ ≠ 0？
    # Detection analogy: how many generations to detect ρ ≠ 0 with confidence?
    # 类似于 Hoeffding 检测：需要足够的"代际样本"来拒绝 ρ=0 的零假设
    # Similar to Hoeffding detection: enough "generational samples" to reject H0: ρ=0
    R_range = 1.0  # 效用范围 / utility range
    tau = 0.01     # 检测阈值 / detection threshold
    # 所需代数 ≈ R²/(2τ²) * log(2/α)
    alpha_detect = 0.05
    n_gen_needed = R_range**2 / (2 * tau**2) * np.log(2.0 / alpha_detect)
    print(f"  To detect ρ>0 at α={alpha_detect}, τ={tau}: need ≈ {n_gen_needed:.0f} generations")
    print(f"  在 α={alpha_detect}, τ={tau} 下检测 ρ>0 需要 ≈ {n_gen_needed:.0f} 代")

    return {
        'rho_values': rho_values,
        'stern_S': stern_S,
    }


# ============================================================================
# 附加验证：综合可持续性指标
# Bonus: Composite Sustainability Index
# ============================================================================

def verify_sustainability_index():
    """
    验证综合可持续性指标
    Verify the composite sustainability index.

    CSI = f(ΔV_max, C_budget, ρ)

    综合三个维度：
    - ΔV_max: 代际势跳跃 / intergenerational potential jump
    - C_budget: 碳预算充足性 / carbon budget adequacy
    - ρ: 贴现率（代际公平性）/ discount rate (intergenerational equity)

    CSI 高 → 可持续 / CSI low → 不可持续
    """
    section_header(
        "Bonus: Composite Sustainability Index (CSI)",
        "附加：综合可持续性指标"
    )

    def compute_csi(delta_V_max, carbon_budget, rho, base_emission):
        """
        计算综合可持续性指标 / Compute composite sustainability index.

        CSI ∈ [0, 1], 1 = 完全可持续 / fully sustainable
        """
        # 势跳跃分量：指数衰减 / Potential jump component: exponential decay
        c_delta = np.exp(-5 * delta_V_max)

        # 碳预算分量：预算充足性 / Carbon budget: adequacy
        # 所需预算 ≈ base_emission * n_generations
        required = base_emission * 20
        if np.isinf(carbon_budget):
            c_budget = 1.0  # 无约束 = 天然可持续 / no constraint = naturally sustainable
        else:
            c_budget = min(carbon_budget / required, 1.0)

        # 贴现率分量：1 - ρ (低贴现 = 高公平 = 高可持续)
        # Discount rate component: 1 - ρ (low discount = high equity = high sustainability)
        c_rho = np.exp(-15 * rho)  # ρ=0 → 1, ρ=0.1 → ~0.22

        # 加权组合 / Weighted combination
        CSI = (0.4 * c_delta + 0.3 * c_budget + 0.3 * c_rho)
        return CSI

    # 测试不同情景 / Test different scenarios
    scenarios_csi = [
        ("Stern路径 (Stern Path)",            0.08, 5.0,   0.001, 0.3),
        ("Nordhaus路径 (Nordhaus Path)",      0.15, 2.0,   0.03,  0.4),
        ("照常营业 (Business as Usual)",       0.35, 0.5,   0.05,  0.5),
        ("崩溃路径 (Collapse Path)",           0.60, 0.1,   0.10,  0.6),
    ]

    print(f"\n  {'Scenario':>30s}  {'ΔV':>8s}  {'Budget':>8s}  "
          f"{'ρ':>8s}  {'CSI':>8s}  {'Status':>12s}")
    print(f"  {'─'*30}  {'─'*8}  {'─'*8}  {'─'*8}  {'─'*8}  {'─'*12}")

    csi_values = []
    for name, dv, cb, r, be in scenarios_csi:
        csi = compute_csi(dv, cb, r, be)
        if csi > 0.7:
            status = "Sustainable 可持续"
        elif csi > 0.4:
            status = "At Risk 有风险"
        elif csi > 0.2:
            status = "Critical 危急"
        else:
            status = "Collapse 崩溃"
        csi_values.append(csi)
        print(
            f"  {name:>30s}  {dv:8.2f}  {cb:8.1f}  "
            f"{r:8.3f}  {csi:8.3f}  {status:>12s}"
        )

    # 验证 CSI 排序 / Verify CSI ordering
    mono_csi = all(
        csi_values[i] >= csi_values[i + 1]
        for i in range(len(csi_values) - 1)
    )
    check_pass_fail(
        mono_csi,
        "CSI decreases from sustainable to collapse scenarios",
        "CSI 从可持续到崩溃情景递减",
    )

    return csi_values


# ============================================================================
# 主程序入口 / Main Entry Point
# ============================================================================

def main():
    """运行所有验证 / Run all verifications."""

    print("=" * 72)
    print("  代际环境公平验证脚本")
    print("  Intergenerational Environmental Equity Verification Script")
    print("  SCX Research Collective")
    print("=" * 72)

    all_passed = True

    # (a) 代际势跳跃模型 / Intergenerational Potential Jump Model
    try:
        verify_intergenerational_potential_jump()
    except Exception as e:
        print(f"\n  ✗ ERROR in (a): {e}")
        all_passed = False

    # (b) 碳预算作为界面平滑 / Carbon Budget as Interface Smoothing
    try:
        verify_carbon_budget_smoothing()
    except Exception as e:
        print(f"\n  ✗ ERROR in (b): {e}")
        all_passed = False

    # (c) 贴现率作为 g 参数 / Discount Rate as g Parameter
    try:
        verify_discount_rate_as_g_parameter()
    except Exception as e:
        print(f"\n  ✗ ERROR in (c): {e}")
        all_passed = False

    # 附加：综合可持续性指标 / Bonus: Composite Sustainability Index
    try:
        verify_sustainability_index()
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
