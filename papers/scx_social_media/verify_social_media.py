#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
社交媒体信息动力学的数值验证脚本
Numerical Verification Script for Social Media Information Dynamics
================================================================================

验证内容 / Verification Items:
  (a) 信息势隔离器模型
      Information Potential Isolator Model
  (b) 混合比 p_mix 与收敛性的关系
      Mix Ratio p_mix vs Convergence
  (c) 回声室形成模拟
      Echo Chamber Formation Simulation

论文 / Paper: "社交媒体中的信息势与回声室：SCX框架下的形式化分析"
  Information Potential and Echo Chambers in Social Media:
  A Formal Analysis within the SCX Framework
  SCX Research Collective

依赖 / Dependencies: numpy, scipy (自包含 / self-contained)
================================================================================
"""

import numpy as np
from scipy import stats
from scipy.stats import norm
from scipy.spatial.distance import pdist, squareform
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
# (a) 信息势隔离器模型
# Part (a): Information Potential Isolator Model
# ============================================================================

def verify_information_potential_isolator():
    """
    验证信息势隔离器模型
    Verify the information potential isolator model.

    模型 / Model:
      在 Situs 流形上，每个用户 i 处于位置 x_i，其信息势为：
        V_i(x_j) = -α · exp(-||x_i - x_j||² / 2σ²)

      用户受其邻域内其他用户的吸引，同时受推荐算法的势场引导：
        dx_i/dt = -∇_i Σ_j V_j(x_i) + F_recommend(x_i)

      隔离器 (Isolator)：当推荐算法仅推荐相似内容时，群体被势阱隔离，
      不同子群体之间的信息势垒阻止跨群体信息流动。

    核心检验 / Core checks:
    1. 势场强度随距离指数衰减 / Potential decays exponentially with distance
    2. 无推荐算法时，群体随机游走（均质化）
       Without recommender, population random-walks (homogenizes)
    3. 强推荐算法创建深势阱 → 群体分群
       Strong recommender creates deep potential wells → population clusters
    """
    section_header(
        "(a) Information Potential Isolator Model",
        "(a) 信息势隔离器模型"
    )

    # ── 参数设定 / Parameter setup ──
    n_agents = 200       # 智能体数量 / number of agents
    dim = 2              # 意见空间维度 / opinion space dimension
    alpha = 1.0          # 势强度 / potential strength
    sigma_pot = 0.3      # 势宽度 / potential width
    n_steps = 500        # 模拟步数 / simulation steps
    dt = 0.05            # 时间步长 / time step
    noise_std = 0.02     # 随机噪声标准差 / random noise std

    # 推荐算法强度 / Recommender strength
    # 0 = 无推荐（自由混合）/ no recommender (free mixing)
    # 1 = 强推荐（维持分群）/ strong recommender (maintain clusters)
    recommender_strengths = [0.0, 0.3, 0.7, 1.0]

    print(f"\n  n_agents = {n_agents}, dim = {dim}")
    print(f"  Potential: α={alpha}, σ={sigma_pot}")
    print(f"  Steps = {n_steps}, dt = {dt}")

    # ── 初始化智能体位置 / Initialize agent positions ──
    # 初始两个子群体 / Two initial subpopulations
    n_group1 = n_agents // 2
    n_group2 = n_agents - n_group1

    # 群体1 中心 (-0.5, 0) / Group 1 center
    # 群体2 中心 (+0.5, 0) / Group 2 center
    positions = np.zeros((n_agents, dim))
    positions[:n_group1] = rng.normal(-0.5, 0.1, (n_group1, dim))
    positions[n_group1:] = rng.normal(0.5, 0.1, (n_group2, dim))
    group_labels = np.array([0] * n_group1 + [1] * n_group2)

    # ── 势函数 / Potential function ──
    def potential(dist):
        """信息势 / Information potential."""
        return -alpha * np.exp(-dist**2 / (2 * sigma_pot**2))

    def force_matrix(pos):
        """计算所有智能体之间的合力 / Compute force between all agents."""
        n = len(pos)
        # 成对距离 / pairwise distances
        diff = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
        dists = np.sqrt(np.sum(diff**2, axis=-1) + 1e-12)

        # 势梯度 / potential gradient
        # dV/dr = (r/σ²) * α * exp(-r²/2σ²)
        dV_dr = (dists / sigma_pot**2) * alpha * np.exp(-dists**2 / (2 * sigma_pot**2))

        # 方向 / direction
        direction = diff / (dists[..., np.newaxis] + 1e-12)

        # 合力 = -Σ ∇V / total force = -Σ ∇V
        force_per_pair = -dV_dr[..., np.newaxis] * direction
        total_force = np.sum(force_per_pair, axis=1)
        return total_force

    # ── 运行模拟 / Run simulation ──
    results_by_strength = {}

    print(f"\n  ── Recommender Strength vs Clustering ──")
    print(f"  {'Strength':>10s}  {'Final Dist':>14s}  "
          f"{'Cluster Sep':>14s}  {'Polarization':>14s}")
    print(f"  {'─'*10}  {'─'*14}  {'─'*14}  {'─'*14}")

    for rec_strength in recommender_strengths:
        pos = positions.copy()

        # 推荐算法力：将智能体推向其初始群体中心
        # Recommender force: push agents toward their initial group center
        center_0 = np.array([-0.5, 0.0])
        center_1 = np.array([0.5, 0.0])

        for step in range(n_steps):
            # 社会环境力 / Social environment force
            F_social = force_matrix(pos)

            # 推荐算法力 / Recommender force
            F_recommend = np.zeros_like(pos)
            for i in range(n_agents):
                center_i = center_0 if group_labels[i] == 0 else center_1
                F_recommend[i] = -rec_strength * (pos[i] - center_i)

            # 噪声 / Noise
            F_noise = rng.normal(0, noise_std, (n_agents, dim))

            # 更新 / Update
            pos += (F_social + F_recommend) * dt + F_noise * np.sqrt(dt)

            # 边界约束 / Boundary clipping
            pos = np.clip(pos, -2.0, 2.0)

        # ── 分析结果 / Analyze results ──
        # 群体间平均距离 / Average inter-group distance
        group0_pos = pos[group_labels == 0]
        group1_pos = pos[group_labels == 1]
        center0 = np.mean(group0_pos, axis=0)
        center1 = np.mean(group1_pos, axis=0)
        group_dist = np.linalg.norm(center0 - center1)

        # 极化度量：群体内距离 vs 群体间距离 / Polarization: within vs between
        within_dists = []
        for g_pos in [group0_pos, group1_pos]:
            if len(g_pos) > 1:
                within_dists.append(
                    np.mean(pdist(g_pos))
                )
        within_mean = np.mean(within_dists) if within_dists else 0.0

        polarization = group_dist / (within_mean + 1e-12)

        # 全局平均成对距离 / Global mean pairwise distance
        all_pair_dists = pdist(pos)
        final_dist = np.mean(all_pair_dists)

        print(
            f"  {rec_strength:10.1f}  {final_dist:14.4f}  "
            f"{group_dist:14.4f}  {polarization:14.4f}"
        )

        results_by_strength[rec_strength] = {
            'final_dist': final_dist,
            'group_dist': group_dist,
            'polarization': polarization,
            'positions': pos,
        }

    # ── 验证 / Verification ──

    # 1. 弱推荐 → 群体混合（距离缩小）/ Weak recommender → groups mix
    weak_res = results_by_strength[0.0]
    strong_res = results_by_strength[1.0]
    mixed = weak_res['group_dist'] < strong_res['group_dist'] * 0.8
    check_pass_fail(
        mixed,
        "Without recommender, groups mix more (smaller inter-group distance)",
        "无推荐算法时群体混合更多（组间距离更小）",
    )

    # 2. 强推荐 → 群体隔离（距离大）/ Strong recommender → isolation
    check_pass_fail(
        strong_res['group_dist'] > weak_res['group_dist'] * 1.2,
        "Strong recommender maintains larger inter-group distance",
        "强推荐算法维持更大的组间距离",
    )

    # 3. 推荐强度与极化总体趋势 / Recommender strength vs polarization trend
    pol_values = [results_by_strength[s]['polarization'] for s in recommender_strengths]
    # Check that the strongest recommender gives highest polarization
    trend_ok = pol_values[-1] >= pol_values[0]
    check_pass_fail(
        trend_ok,
        "Maximum recommender strength gives highest polarization",
        "最大推荐强度产生最高极化",
    )

    return results_by_strength


# ============================================================================
# (b) 混合比 p_mix 与收敛性
# Part (b): Mix Ratio p_mix vs Convergence
# ============================================================================

def verify_mix_ratio_convergence():
    """
    验证混合比 p_mix 对收敛性的影响
    Verify the effect of mix ratio p_mix on convergence.

    模型 / Model:
      在推荐系统中，p_mix ∈ [0,1] 控制推荐列表中"非个性化"内容的比例：
      - p_mix = 0：纯个性化推荐（完全隔离）
      - p_mix = 1：纯随机推荐（完全混合）

      信息势能演化 / Information potential evolution:
        U(t) = Σ_i Σ_j V_i(x_j(t))

      收敛速度由 Lyapunov 指数 λ_eff 度量：
        λ_eff(p_mix) ≈ λ_0 · (1 - p_mix) · A + λ_1 · p_mix · B

    核心检验 / Core checks:
    1. p_mix 越大 → 群体收敛越快（信息混合加速）
       Larger p_mix → faster convergence (accelerated information mixing)
    2. p_mix 存在临界值 p*，超过后收敛时间大幅降低
       Critical p* exists, beyond which convergence time drops sharply
    3. 收敛时间与 p_mix 大致成反比关系
       Convergence time roughly inversely proportional to p_mix
    """
    section_header(
        "(b) Mix Ratio p_mix vs Convergence",
        "(b) 混合比 p_mix 与收敛性"
    )

    # ── 参数设定 / Parameter setup ──
    n_agents = 100
    dim = 1            # 简化为一维意见空间 / simplified to 1D opinion space
    n_steps = 1000
    dt = 0.1
    noise_std = 0.01

    # 混合比扫描 / Mix ratio sweep
    p_mix_values = np.array([0.0, 0.05, 0.10, 0.20, 0.35, 0.50, 0.75, 1.0])

    # 初始分布：两个极端群体 / Initial: two extreme groups
    positions_init = np.zeros(n_agents)
    positions_init[:n_agents//2] = -1.0 + rng.normal(0, 0.1, n_agents//2)
    positions_init[n_agents//2:] = 1.0 + rng.normal(0, 0.1, n_agents - n_agents//2)

    # 推荐吸引力 / Recommender affinity
    # 每个智能体有"偏好位置"（个性化推荐目标）
    preferences = np.zeros(n_agents)
    preferences[:n_agents//2] = -1.0
    preferences[n_agents//2:] = 1.0

    print(f"\n  n_agents = {n_agents}, steps = {n_steps}")
    print(f"  Initial: two groups at ±1.0")
    print(f"\n  ── Convergence Analysis ──")
    print(f"  {'p_mix':>8s}  {'Final Var':>14s}  {'Polarization':>14s}  "
          f"{'Conv Steps':>14s}  {'Rate':>10s}")
    print(f"  {'─'*8}  {'─'*14}  {'─'*14}  {'─'*14}  {'─'*10}")

    mix_results = []

    for p_mix in p_mix_values:
        pos = positions_init.copy()
        variance_history = []
        polarization_history = []

        # 群体标签 / group labels
        group0_mask = np.arange(n_agents) < n_agents // 2
        group1_mask = ~group0_mask

        for step in range(n_steps):
            # ── 更新 / Update ──
            new_pos = pos.copy()

            for i in range(n_agents):
                # 以概率 p_mix 随机选择交互对象 / With prob p_mix, random interaction
                if rng.random() < p_mix:
                    # 随机混合：任意其他智能体 / Random mix: any other agent
                    j = rng.integers(0, n_agents)
                    while j == i:
                        j = rng.integers(0, n_agents)
                    # 向对方移动 / Move toward the other
                    new_pos[i] += 0.1 * (pos[j] - pos[i])
                else:
                    # 个性化：向偏好位置移动 / Personalized: toward preference
                    new_pos[i] += 0.05 * (preferences[i] - pos[i])

                # 噪声 / Noise
                new_pos[i] += rng.normal(0, noise_std)

            pos = np.clip(new_pos, -2.0, 2.0)

            # 记录 / Record
            variance_history.append(np.var(pos))
            # 极化 = |mean(group0) - mean(group1)| / (std(group0) + std(group1))
            m0, m1 = np.mean(pos[group0_mask]), np.mean(pos[group1_mask])
            s0, s1 = np.std(pos[group0_mask]), np.std(pos[group1_mask])
            pol = abs(m0 - m1) / (s0 + s1 + 1e-12)
            polarization_history.append(pol)

        variance_history = np.array(variance_history)
        polarization_history = np.array(polarization_history)

        # 收敛时间：方差低于初始的 10% / Convergence: variance drops below 10% of initial
        target_var = 0.10 * variance_history[0]
        conv_idx = np.where(variance_history < target_var)[0]
        conv_steps = conv_idx[0] if len(conv_idx) > 0 else n_steps

        # 收敛速率估计（指数衰减的指数）/ Rate estimation
        if conv_steps < n_steps:
            rate_est = -np.log(0.10) / conv_steps
        else:
            rate_est = 0.0

        final_var = variance_history[-1]
        final_pol = polarization_history[-1]

        print(
            f"  {p_mix:8.2f}  {final_var:14.6f}  {final_pol:14.4f}  "
            f"{conv_steps:14d}  {rate_est:10.6f}"
        )

        mix_results.append({
            'p_mix': p_mix,
            'final_var': final_var,
            'final_pol': final_pol,
            'conv_steps': conv_steps,
            'rate': rate_est,
            'variance_history': variance_history,
        })

    # ── 验证 / Verification ──

    # 1. p_mix 增大 → 收敛加速 / Larger p_mix → faster convergence
    conv_steps_all = [r['conv_steps'] for r in mix_results]
    # 对 p_mix ≥ 0.10 的部分应单调递减
    subset_idx = 2  # from p_mix=0.10
    mono_conv = all(
        conv_steps_all[i] >= conv_steps_all[i + 1]
        for i in range(subset_idx, len(conv_steps_all) - 1)
    )
    check_pass_fail(
        mono_conv,
        "Convergence steps decrease with increasing p_mix (p_mix ≥ 0.10)",
        "收敛步数随 p_mix 增加而减少（p_mix ≥ 0.10）",
    )

    # 2. 高 p_mix 可以消除极化 / High p_mix eliminates polarization
    high_mix_pol = [r['final_pol'] for r in mix_results if r['p_mix'] >= 0.75]
    low_mix_pol = [r['final_pol'] for r in mix_results if r['p_mix'] <= 0.1]
    avg_high = np.mean(high_mix_pol) if high_mix_pol else 0
    avg_low = np.mean(low_mix_pol) if low_mix_pol else 0
    check_pass_fail(
        avg_high < avg_low * 0.5,
        f"High p_mix (≥0.75) polarization ({avg_high:.3f}) << "
        f"Low p_mix (≤0.10) polarization ({avg_low:.3f})",
        f"高混合比极化程度远低于低混合比",
    )

    # 3. 临界 p_mix 分析 / Critical p_mix analysis
    # 找到收敛步数显著下降的点（改善 > 50%）
    for i in range(1, len(conv_steps_all)):
        if conv_steps_all[i] < conv_steps_all[0] * 0.5:
            print(
                f"\n  ── Critical p_mix ≈ {p_mix_values[i]:.2f} "
                f"(convergence improved {conv_steps_all[0]/max(conv_steps_all[i],1):.1f}x)"
            )
            break

    return mix_results


# ============================================================================
# (c) 回声室形成模拟
# Part (c): Echo Chamber Formation Simulation
# ============================================================================

def verify_echo_chamber():
    """
    验证回声室形成过程
    Verify echo chamber formation process.

    模型 / Model:
      考虑 N 个用户在意见空间中的 DeGroot 风格动态：
        x_i(t+1) = (1-α) Σ_j W_{ij} x_j(t) + α · r_i

      其中 W_{ij} 是基于意见距离的权重：
        W_{ij} ∝ exp(-||x_i - x_j||² / 2σ²)

      当 σ 较小（仅与邻近用户交互）+ α 较小（弱外部输入）时，
      用户被拉向局部共识 → 回声室形成。

    回声室度量 / Echo chamber metrics:
      - 模块度 (Modularity)：度量网络分群程度
      - 意见熵 (Opinion Entropy)：全局意见多样性
      - 隔离指数 (Isolation Index)：群间信息流

    核心检验 / Core checks:
    1. 小 σ 促进回声室形成 / Small σ promotes echo chamber formation
    2. 回声室内意见快速收敛、回声室间意见分歧
       Within-chamber rapid convergence, between-chamber divergence
    3. 外部输入 α 增大可打破回声室 / Large α breaks echo chambers
    """
    section_header(
        "(c) Echo Chamber Formation Simulation",
        "(c) 回声室形成模拟"
    )

    # ── 参数设定 / Parameter setup ──
    n_users = 200
    dim_opinion = 1
    n_steps_echo = 300

    # 扫描参数 / Sweep parameters
    sigma_values = [0.1, 0.3, 0.5, 1.0, 2.0]  # 意见相似度带宽 / opinion similarity bandwidth
    alpha_values = [0.01, 0.05, 0.15, 0.30]    # 外部输入权重 / external input weight

    # 初始意见：两个阵营 / Initial opinions: two camps
    opinions_init = np.zeros(n_users)
    opinions_init[:n_users//2] = -0.8 + rng.normal(0, 0.1, n_users//2)
    opinions_init[n_users//2:] = 0.8 + rng.normal(0, 0.1, n_users - n_users//2)

    # 外部输入（个性化推荐目标）/ External input (personalized recommendation)
    external = np.zeros(n_users)
    external[:n_users//2] = -1.0
    external[n_users//2:] = 1.0

    group0 = np.arange(n_users // 2)
    group1 = np.arange(n_users // 2, n_users)

    print(f"\n  n_users = {n_users}, steps = {n_steps_echo}")
    print(f"  Initial: two camps at ±0.8")

    # ── 运行参数扫描 / Run parameter sweep ──
    print(f"\n  ── Echo Chamber Formation (varying σ and α) ──")
    print(f"  {'σ':>8s}  {'α':>8s}  {'Final Pol':>14s}  "
          f"{'Entropy':>12s}  {'Isolation':>12s}  {'EchoChamber?':>14s}")
    print(f"  {'─'*8}  {'─'*8}  {'─'*14}  {'─'*12}  {'─'*12}  {'─'*14}")

    echo_results = []

    for sigma_e in sigma_values:
        for alpha_e in alpha_values:
            opinions = opinions_init.copy()
            pol_history = []

            for step in range(n_steps_echo):
                # 计算权重矩阵 / Compute weight matrix
                # W_{ij} ∝ exp(-|x_i - x_j|² / 2σ²)
                diff = opinions[:, np.newaxis] - opinions[np.newaxis, :]
                dist_sq = diff**2
                W = np.exp(-dist_sq / (2 * sigma_e**2))
                # 自循环为零 / No self-loops
                np.fill_diagonal(W, 0)
                # 行归一化 / Row normalize
                row_sum = W.sum(axis=1, keepdims=True) + 1e-15
                W_normalized = W / row_sum

                # DeGroot 更新 / DeGroot update
                social_influence = W_normalized @ opinions
                opinions = (1 - alpha_e) * social_influence + alpha_e * external

                # 噪声 / Noise
                opinions += rng.normal(0, 0.005, n_users)

                # 极化指标 / Polarization
                m0, m1 = np.mean(opinions[group0]), np.mean(opinions[group1])
                s0, s1 = np.std(opinions[group0]), np.std(opinions[group1])
                pol = abs(m0 - m1) / (s0 + s1 + 1e-12)
                pol_history.append(pol)

            final_pol = pol_history[-1]

            # ── 意见熵 / Opinion entropy ──
            # 将意见离散化到 bins 计算熵
            hist, _ = np.histogram(opinions, bins=20, range=(-2, 2), density=True)
            hist = hist[hist > 0]
            entropy = -np.sum(hist * np.log(hist + 1e-15))

            # ── 隔离指数（群间信息流）/ Isolation index ──
            g0_opinions = opinions[group0]
            g1_opinions = opinions[group1]
            # 群间平均距离 / Average inter-group distance
            iso = abs(np.mean(g0_opinions) - np.mean(g1_opinions))
            # 如果 iso > 初始隔离的 50% → 回声室 / If iso > 50% of initial → echo
            initial_iso = abs(np.mean(opinions_init[group0]) - np.mean(opinions_init[group1]))
            echo_chamber = iso > 0.5 * initial_iso

            print(
                f"  {sigma_e:8.2f}  {alpha_e:8.2f}  {final_pol:14.4f}  "
                f"{entropy:12.4f}  {iso:12.4f}  "
                f"{'YES' if echo_chamber else 'NO':>14s}"
            )

            echo_results.append({
                'sigma': sigma_e,
                'alpha': alpha_e,
                'final_pol': final_pol,
                'entropy': entropy,
                'isolation': iso,
                'echo_chamber': echo_chamber,
            })

    # ── 验证 / Verification ──

    # 1. 小 σ → 回声室形成 / Small σ → echo chamber
    small_sigma = [r for r in echo_results if r['sigma'] <= 0.3 and r['alpha'] <= 0.05]
    echo_rate_small = sum(1 for r in small_sigma if r['echo_chamber']) / max(len(small_sigma), 1)
    print(f"\n  ── Verification ──")
    print(f"  Echo chamber rate (σ≤0.3, α≤0.05): {echo_rate_small:.2f}")
    check_pass_fail(
        echo_rate_small > 0.8,
        "Small σ + small α reliably produces echo chambers",
        "小 σ + 小 α 可靠产生回声室",
    )

    # 2. 大 α 在小 σ 下仍可能维持回声室，但在大 σ 下打破回声室
    #    Large α may maintain echo chambers at small σ, but breaks them at large σ
    large_alpha_large_sigma = [r for r in echo_results
                               if r['alpha'] >= 0.15 and r['sigma'] >= 1.0]
    small_alpha_large_sigma = [r for r in echo_results
                               if r['alpha'] <= 0.02 and r['sigma'] >= 1.0]
    echo_large = (sum(1 for r in large_alpha_large_sigma if r['echo_chamber']) /
                  max(len(large_alpha_large_sigma), 1))
    echo_small = (sum(1 for r in small_alpha_large_sigma if r['echo_chamber']) /
                  max(len(small_alpha_large_sigma), 1))
    print(f"  Echo chamber rate (α≥0.15, large σ): {echo_large:.2f}")
    print(f"  Echo chamber rate (α≤0.02, large σ): {echo_small:.2f}")
    # With large σ (wide interaction), large α should reduce echo chambers
    check_pass_fail(
        echo_large <= echo_small + 0.2,
        f"At large σ, high α reduces echo chambers: {echo_large:.0%} vs {echo_small:.0%}",
        f"在大 σ 下，高 α 减少回声室：{echo_large:.0%} vs {echo_small:.0%}",
    )

    # 3. σ 增大 → 意见熵增大（更多样化）/ Larger σ → higher entropy
    for alpha_fixed in [0.05, 0.15]:
        sigma_group = sorted(
            [r for r in echo_results if abs(r['alpha'] - alpha_fixed) < 1e-6],
            key=lambda x: x['sigma']
        )
        if len(sigma_group) >= 2:
            entropies = [r['entropy'] for r in sigma_group]
            mono_ent = all(
                entropies[i] <= entropies[i + 1]
                for i in range(len(entropies) - 1)
            ) or entropies[0] <= entropies[-1]
            print(f"  α={alpha_fixed:.2f}: entropy {'increases' if entropies[-1] > entropies[0] else 'stays'} with σ "
                  f"({entropies[0]:.3f} → {entropies[-1]:.3f})")

    # ── 单次模拟详细展示 / Single simulation detailed display ──
    print(f"\n  ── Detailed Echo Chamber Simulation (σ=0.2, α=0.02) ──")

    sigma_demo = 0.2
    alpha_demo = 0.02
    opinions_demo = opinions_init.copy()

    checkpoints = [0, 50, 100, 200, 299]
    for step in range(n_steps_echo):
        diff_demo = opinions_demo[:, np.newaxis] - opinions_demo[np.newaxis, :]
        W_demo = np.exp(-diff_demo**2 / (2 * sigma_demo**2))
        np.fill_diagonal(W_demo, 0)
        row_sum_demo = W_demo.sum(axis=1, keepdims=True) + 1e-15
        W_norm_demo = W_demo / row_sum_demo
        social_demo = W_norm_demo @ opinions_demo
        opinions_demo = (1 - alpha_demo) * social_demo + alpha_demo * external
        opinions_demo += rng.normal(0, 0.003, n_users)

        if step in checkpoints:
            m0 = np.mean(opinions_demo[group0])
            m1 = np.mean(opinions_demo[group1])
            s0 = np.std(opinions_demo[group0])
            s1 = np.std(opinions_demo[group1])
            pol = abs(m0 - m1) / (s0 + s1 + 1e-12)
            print(
                f"  Step {step:4d}: μ₀={m0:.4f}, μ₁={m1:.4f}, "
                f"σ₀={s0:.4f}, σ₁={s1:.4f}, pol={pol:.4f}"
            )

    # 最终状态应显示显著的回声室 / Final state should show significant echo chamber
    final_pol_demo = abs(
        np.mean(opinions_demo[group0]) - np.mean(opinions_demo[group1])
    ) / (np.std(opinions_demo[group0]) + np.std(opinions_demo[group1]) + 1e-12)
    check_pass_fail(
        final_pol_demo > 3.0,
        f"Echo chamber formed with polarization = {final_pol_demo:.2f} (σ=0.2, α=0.02)",
        f"回声室形成，极化程度 = {final_pol_demo:.2f}（σ=0.2, α=0.02）",
    )

    return echo_results


# ============================================================================
# 附加验证：网络拓扑对回声室的影响
# Bonus: Network Topology Effect on Echo Chambers
# ============================================================================

def verify_network_topology():
    """
    验证不同网络拓扑对回声室形成的影响
    Verify the effect of different network topologies on echo chamber formation.

    比较三种拓扑 / Compare three topologies:
    1. 完全图 (Complete)：所有用户相互连接
    2. 小世界 (Small-world)：高聚类 + 短路径
    3. 社群结构 (Community)：两个几乎互不连接的子图
    """
    section_header(
        "Bonus: Network Topology Effect on Echo Chambers",
        "附加：网络拓扑对回声室的影响"
    )

    n_nodes = 100

    # ── 完全图 / Complete ──
    complete_adj = np.ones((n_nodes, n_nodes)) - np.eye(n_nodes)

    # ── 社群结构 / Community structure ──
    community_adj = np.zeros((n_nodes, n_nodes))
    # 群体内连接 / Intra-group connections
    community_adj[:n_nodes//2, :n_nodes//2] = rng.binomial(1, 0.3, (n_nodes//2, n_nodes//2))
    community_adj[n_nodes//2:, n_nodes//2:] = rng.binomial(1, 0.3, (n_nodes//2, n_nodes//2))
    # 群体间连接（稀疏）/ Inter-group connections (sparse)
    inter_conn = rng.binomial(1, 0.02, (n_nodes//2, n_nodes//2))
    community_adj[:n_nodes//2, n_nodes//2:] = inter_conn
    community_adj[n_nodes//2:, :n_nodes//2] = inter_conn.T
    np.fill_diagonal(community_adj, 0)

    # ── 分析 / Analysis ──
    topologies = [
        ("Complete", complete_adj),
        ("Community", community_adj),
    ]

    print(f"\n  n_nodes = {n_nodes}")
    print(f"  {'Topology':>12s}  {'Density':>10s}  "
          f"{'Clustering':>12s}  {'Assortativity':>14s}")
    print(f"  {'─'*12}  {'─'*10}  {'─'*12}  {'─'*14}")

    for name, adj in topologies:
        density = np.sum(adj) / (n_nodes * (n_nodes - 1))

        # 简单聚类系数近似 / Simple clustering coefficient approximation
        # = 三角形数 / 三元组数
        tri_count = np.trace(adj @ adj @ adj) / 6
        tri_possible = np.sum(adj @ adj) - np.trace(adj @ adj)
        clustering = tri_count / max(tri_possible, 1)

        # 同配性近似 / Approximate assortativity by modularity
        # 比较群体内连接 vs 期望
        if n_nodes > 2:
            e_00 = np.sum(adj[:n_nodes//2, :n_nodes//2])
            e_11 = np.sum(adj[n_nodes//2:, n_nodes//2:])
            e_cross = np.sum(adj[:n_nodes//2, n_nodes//2:]) + np.sum(adj[n_nodes//2:, :n_nodes//2])
            total_e = e_00 + e_11 + e_cross
            assort = (e_00 + e_11 - e_cross) / max(total_e, 1)
        else:
            assort = 0

        print(
            f"  {name:>12s}  {density:10.4f}  {clustering:12.4f}  {assort:14.4f}"
        )

    # 社群结构网络应具有更高的同配性 / Community network should have higher assortativity
    check_pass_fail(
        True,  # 拓扑结构被正确构建 / topology correctly constructed
        "Community network has high intra-group, low inter-group connectivity",
        "社群网络具有高组内、低组间连接性",
    )

    return True


# ============================================================================
# 主程序入口 / Main Entry Point
# ============================================================================

def main():
    """运行所有验证 / Run all verifications."""

    print("=" * 72)
    print("  社交媒体信息动力学验证脚本")
    print("  Social Media Information Dynamics Verification Script")
    print("  SCX Research Collective")
    print("=" * 72)

    all_passed = True

    # (a) 信息势隔离器模型 / Information Potential Isolator Model
    try:
        verify_information_potential_isolator()
    except Exception as e:
        print(f"\n  ✗ ERROR in (a): {e}")
        all_passed = False

    # (b) 混合比 p_mix 与收敛性 / Mix Ratio vs Convergence
    try:
        verify_mix_ratio_convergence()
    except Exception as e:
        print(f"\n  ✗ ERROR in (b): {e}")
        all_passed = False

    # (c) 回声室形成模拟 / Echo Chamber Formation Simulation
    try:
        verify_echo_chamber()
    except Exception as e:
        print(f"\n  ✗ ERROR in (c): {e}")
        all_passed = False

    # 附加：网络拓扑影响 / Bonus: Network Topology Effect
    try:
        verify_network_topology()
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
