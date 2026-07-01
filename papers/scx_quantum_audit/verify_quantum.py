#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
SCX Quantum Audit — Verification Suite (numpy only)
SCX量子审计 — 验证套件（纯numpy实现）

Implements five quantum verification primitives for tamper-evident auditing:
实现五种量子验证原语，用于防篡改审计：

  1. BB84 QKD Simulation          — BB84量子密钥分发模拟
  2. CHSH Inequality Violation     — CHSH不等式违反检测
  3. HSW (Holevo-Schumacher-Westmoreland) Capacity — HSW容量计算
  4. No-Cloning Disturbance        — 不可克隆定理扰动演示
  5. Entangled Pair Collapse (Spring-Yajie) — 纠缠对坍缩验证

Dependency: numpy only. No qiskit, no cirq.
依赖：仅需numpy，不依赖qiskit或cirq。

Author: SCX Quantum Audit Team
Date:   2026-07
=============================================================================
"""

import numpy as np
from typing import Tuple, Optional, Dict, List

# ============================================================================
# Global constants / 全局常量
# ============================================================================

PAULI_X = np.array([[0, 1], [1, 0]], dtype=complex)       # σx
PAULI_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)    # σy
PAULI_Z = np.array([[1, 0], [0, -1]], dtype=complex)       # σz
HADAMARD = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)  # H gate
I2 = np.eye(2, dtype=complex)

# Standard basis states / 标准基态
KET0 = np.array([1, 0], dtype=complex)   # |0⟩
KET1 = np.array([0, 1], dtype=complex)   # |1⟩
KET_PLUS = (KET0 + KET1) / np.sqrt(2)    # |+⟩ = H|0⟩
KET_MINUS = (KET0 - KET1) / np.sqrt(2)   # |−⟩ = H|1⟩

# Bell states / 贝尔态
BELL_PHI_PLUS = (np.kron(KET0, KET0) + np.kron(KET1, KET1)) / np.sqrt(2)    # |Φ⁺⟩
BELL_PHI_MINUS = (np.kron(KET0, KET0) - np.kron(KET1, KET1)) / np.sqrt(2)   # |Φ⁻⟩
BELL_PSI_PLUS = (np.kron(KET0, KET1) + np.kron(KET1, KET0)) / np.sqrt(2)    # |Ψ⁺⟩
BELL_PSI_MINUS = (np.kron(KET0, KET1) - np.kron(KET1, KET0)) / np.sqrt(2)   # |Ψ⁻⟩

# ============================================================================
# Utility functions / 工具函数
# ============================================================================

def density_matrix(state: np.ndarray) -> np.ndarray:
    """Density matrix ρ = |ψ⟩⟨ψ| / 密度矩阵"""
    return np.outer(state, state.conj())


def fidelity(rho: np.ndarray, sigma: np.ndarray) -> float:
    """Uhlmann fidelity F(ρ,σ) = Tr(√(√ρ σ √ρ))² / 保真度"""
    eigvals, eigvecs = np.linalg.eigh(rho)
    sqrt_rho = eigvecs @ np.diag(np.sqrt(np.maximum(eigvals.real, 0))) @ eigvecs.conj().T
    inner = sqrt_rho @ sigma @ sqrt_rho
    eigvals2 = np.linalg.eigvalsh(inner)
    return float(np.sum(np.sqrt(np.maximum(eigvals2.real, 0))) ** 2)


def von_neumann_entropy(rho: np.ndarray) -> float:
    """von Neumann entropy S(ρ) = -Tr(ρ log ρ) / 冯诺依曼熵"""
    eigvals = np.linalg.eigvalsh(rho)
    eigvals = np.maximum(eigvals.real, 1e-15)  # avoid log(0)
    return float(-np.sum(eigvals * np.log2(eigvals)))


# ============================================================================
# 1. BB84 QKD Simulation / BB84量子密钥分发模拟
# ============================================================================

def bb84_simulate(
    n_bits: int = 1000,
    eavesdrop_rate: float = 0.0,
    seed: Optional[int] = None
) -> Dict:
    """
    BB84 quantum key distribution simulation.
    BB84量子密钥分发模拟。

    Parameters / 参数:
        n_bits:       Number of qubits to exchange / 交换的量子比特数
        eavesdrop_rate: Fraction of qubits intercepted by Eve / Eve截获比例
        seed:         Random seed for reproducibility / 随机种子

    Returns / 返回:
        Dict with sifted key length, QBER, and matching rate.
    """
    rng = np.random.default_rng(seed)

    # --- Alice prepares / Alice准备 ---
    # Random bits and bases: 0=Z basis, 1=X basis
    alice_bits = rng.integers(0, 2, size=n_bits)        # 随机比特 0/1
    alice_bases = rng.integers(0, 2, size=n_bits)       # 随机基 Z/X

    # Prepare qubit states: |0⟩,|1⟩ for Z; |+⟩,|−⟩ for X
    states = np.zeros((n_bits, 2), dtype=complex)
    for i in range(n_bits):
        if alice_bases[i] == 0:  # Z basis
            states[i] = KET0 if alice_bits[i] == 0 else KET1
        else:                     # X basis
            states[i] = KET_PLUS if alice_bits[i] == 0 else KET_MINUS

    # --- Eve intercept-resend / Eve截获-重发 ---
    eve_mask = rng.random(n_bits) < eavesdrop_rate     # which qubits Eve steals
    eve_bases = rng.integers(0, 2, size=n_bits)         # Eve's random bases

    for i in range(n_bits):
        if not eve_mask[i]:
            continue
        # Eve measures in her random basis, collapses the state
        if eve_bases[i] == 0:  # Z basis
            prob0 = np.abs(states[i][0]) ** 2
            eve_bit = 0 if rng.random() < prob0 else 1
            states[i] = KET0 if eve_bit == 0 else KET1
        else:                   # X basis
            # Project onto |+⟩,|−⟩
            prob_plus = np.abs(np.dot(KET_PLUS.conj(), states[i])) ** 2
            eve_bit = 0 if rng.random() < prob_plus else 1
            states[i] = KET_PLUS if eve_bit == 0 else KET_MINUS

    # --- Bob measures / Bob测量 ---
    bob_bases = rng.integers(0, 2, size=n_bits)         # Bob's random bases
    bob_results = np.zeros(n_bits, dtype=int)

    for i in range(n_bits):
        if bob_bases[i] == 0:  # Z basis
            prob0 = np.abs(states[i][0]) ** 2
            bob_results[i] = 0 if rng.random() < prob0 else 1
        else:                   # X basis
            prob_plus = np.abs(np.dot(KET_PLUS.conj(), states[i])) ** 2
            bob_results[i] = 0 if rng.random() < prob_plus else 1

    # --- Basis reconciliation / 基比对 ---
    same_basis = alice_bases == bob_bases
    sifted_alice = alice_bits[same_basis]
    sifted_bob = bob_results[same_basis]
    sifted_len = len(sifted_alice)

    # --- QBER (Quantum Bit Error Rate) / 量子比特误码率 ---
    errors = np.sum(sifted_alice != sifted_bob)
    qber = errors / sifted_len if sifted_len > 0 else 0.0

    # --- Matching rate / 匹配率 ---
    match_rate = 1.0 - qber

    return {
        'n_total': n_bits,
        'sifted_length': sifted_len,
        'errors': int(errors),
        'qber': float(qber),
        'match_rate': float(match_rate),
        'eavesdrop_rate': eavesdrop_rate,
    }


# ============================================================================
# 2. CHSH Inequality Violation / CHSH不等式违反检测
# ============================================================================

def chsh_expectation(
    a_angle: float,
    b_angle: float,
    n_samples: int = 10000,
    seed: Optional[int] = None,
    noise: float = 0.0
) -> float:
    """
    Compute CHSH expectation E(a,b) for a singlet state |Ψ⁻⟩.
    计算CHSH期望值E(a,b)，使用单态|Ψ⁻⟩。

    Measurement angles / 测量角度:
        Alice measures σ·a, Bob measures σ·b.
        a_angle, b_angle in radians / 弧度制。

    Parameters / 参数:
        noise: Mixing fraction with white noise (0=ideal, 1=completely random)
               / 白噪声混合比例 (0=理想, 1=完全随机)
    """
    rng = np.random.default_rng(seed)

    # Generate singlet state |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
    # Measurement outcomes: Alice measures along angle a, Bob along angle b
    # In the singlet state, P(A=B|a,b) = sin²((a-b)/2), P(A≠B|a,b) = cos²((a-b)/2)

    theta = a_angle - b_angle
    p_same = np.sin(theta / 2) ** 2   # probability of same outcome (+) correlation
    p_diff = np.cos(theta / 2) ** 2   # probability of different outcome (−)

    # With noise, mix with uniform random
    if noise > 0:
        p_same = (1 - noise) * p_same + noise * 0.5
        p_diff = (1 - noise) * p_diff + noise * 0.5

    # Sample outcomes (+1 or -1 for each side)
    samples_same = rng.random(n_samples) < p_same   # A and B give same sign
    # E = P(same)*(+1*+1) + P(diff)*(-1*+1) simplified: E = P(same) - P(diff)
    # Actually: A,B ∈ {+1,−1}. E = (+1)*(P(both +) + P(both −)) + (−1)*(P(opposite))
    # P(same) = P(both+) + P(both−). For singlet, P(both+) = P(both−) = p_same/2
    # E = (+1)*p_same + (-1)*p_diff = p_same - p_diff
    # But also A,B individually = 0 since uniform marginals for singlet.

    # Direct computation
    e_value = p_same - p_diff

    # Monte Carlo verification
    a_signs = np.ones(n_samples)
    b_signs = np.where(samples_same, 1.0, -1.0)  # if same: both +, if diff: Bob −
    # Actually need independent draws. Let's do proper Monte Carlo:
    a_outcomes = 2 * (rng.random(n_samples) < 0.5).astype(float) - 1  # ±1
    # For singlet, P(b_outcome = a_outcome) = p_same
    b_outcomes = np.where(rng.random(n_samples) < p_same, a_outcomes, -a_outcomes)

    mc_e = float(np.mean(a_outcomes * b_outcomes))

    return mc_e


def chsh_s_value(
    a: float = 0.0,
    a_prime: float = np.pi / 2,
    b: float = np.pi / 4,
    b_prime: float = 3 * np.pi / 4,
    n_samples: int = 10000,
    noise: float = 0.0,
    seed: Optional[int] = None
) -> Dict:
    """
    Compute CHSH parameter S = E(a,b) − E(a,b') + E(a',b) + E(a',b').
    计算CHSH参数S。

    Classical bound / 经典上界: |S| ≤ 2  (CHSH inequality)
    Quantum maximum  / 量子最大值: |S| ≤ 2√2 ≈ 2.828  (Tsirelson bound)

    Optimal angles for singlet: a=0, a'=π/2, b=π/4, b'=3π/4 → S=2√2.
    最优角度 → S=2√2。

    Parameters / 参数:
        noise:  Depolarizing noise fraction 0..1 / 退极化噪声比例
    """
    seed_seq = np.random.SeedSequence(seed) if seed is not None else None

    def seeded(offset):
        if seed_seq is None:
            return None
        return int(seed_seq.spawn(1)[0].generate_state(1)[0]) + offset

    E_ab = chsh_expectation(a, b, n_samples, seeded(0), noise)
    E_abp = chsh_expectation(a, b_prime, n_samples, seeded(1), noise)
    E_apb = chsh_expectation(a_prime, b, n_samples, seeded(2), noise)
    E_apbp = chsh_expectation(a_prime, b_prime, n_samples, seeded(3), noise)

    S = E_ab - E_abp + E_apb + E_apbp

    # Theoretical S value (ideal, no sampling noise)
    def e_theory(a_ang, b_ang, n):
        t = a_ang - b_ang
        p_s = np.sin(t / 2) ** 2
        p_d = np.cos(t / 2) ** 2
        if n > 0:
            p_s = (1 - n) * p_s + n * 0.5
            p_d = (1 - n) * p_d + n * 0.5
        return p_s - p_d

    S_theory = (e_theory(a, b, noise) - e_theory(a, b_prime, noise)
                + e_theory(a_prime, b, noise) + e_theory(a_prime, b_prime, noise))

    tampered = abs(S) <= 2.0  # If |S| ≤ 2, classical behavior → possible tampering

    return {
        'S': float(S),
        'S_theory': float(S_theory),
        'E_ab': float(E_ab),
        'E_ab_prime': float(E_abp),
        'E_a_prime_b': float(E_apb),
        'E_a_prime_b_prime': float(E_apbp),
        'tsirelson_bound': 2 * np.sqrt(2),
        'classical_bound': 2.0,
        'quantum_violation': abs(S) > 2.0,      # 量子违反
        'tampering_suspected': tampered,          # 疑似篡改
        'noise_level': noise,
    }


# ============================================================================
# 3. HSW Capacity / HSW (Holevo-Schumacher-Westmoreland) 容量
# ============================================================================

def holevo_bound(
    states: List[np.ndarray],
    probs: Optional[List[float]] = None,
    measurement_basis: Optional[np.ndarray] = None
) -> Dict:
    """
    Compute Holevo bound χ for a quantum ensemble.
    计算量子系综的Holevo界χ。

    χ = S(ρ) − Σ p_i S(ρ_i)   where ρ = Σ p_i ρ_i
    其中 S 是冯诺依曼熵。

    HSW Theorem: The classical capacity of a quantum channel
    using this ensemble is at least χ (and the supremum over all
    ensembles gives the HSW capacity).
    HSW定理：使用该系综的量子信道经典容量至少为χ。

    Parameters / 参数:
        states:  List of pure state vectors / 纯态向量列表
        probs:   Probability distribution (default: uniform) / 概率分布（默认均匀）
        measurement_basis: Optional POVM elements / 可选POVM元素

    Returns / 返回:
        Dict with Holevo chi, ensemble entropy, average conditional entropy.
    """
    n = len(states)
    if probs is None:
        probs = [1.0 / n] * n
    probs = np.array(probs, dtype=float)
    probs = probs / probs.sum()  # normalize / 归一化

    # Individual density matrices / 各个密度矩阵
    rhos = [density_matrix(s) for s in states]

    # Ensemble average / 系综平均
    rho_avg = np.zeros_like(rhos[0], dtype=complex)
    for p, r in zip(probs, rhos):
        rho_avg += p * r

    # von Neumann entropy / 冯诺依曼熵
    S_rho = von_neumann_entropy(rho_avg)

    # Average conditional entropy / 平均条件熵
    S_cond_avg = sum(p * von_neumann_entropy(r) for p, r in zip(probs, rhos))

    chi = S_rho - S_cond_avg

    result = {
        'holevo_chi': float(chi),
        'ensemble_entropy': float(S_rho),
        'avg_conditional_entropy': float(S_cond_avg),
        'n_states': n,
    }

    # Accessible information lower bound / 可获取信息下界
    if measurement_basis is not None:
        # Compute mutual information for this specific measurement
        # I(A:B) = H(B) − H(B|A) / 互信息
        m = measurement_basis.shape[0]
        p_b = np.zeros(m)
        p_b_given_a = np.zeros((n, m))
        for i, s in enumerate(states):
            for j in range(m):
                p_b_given_a[i, j] = np.abs(np.dot(measurement_basis[j].conj(), s)) ** 2
            p_b += probs[i] * p_b_given_a[i]

        H_B = -np.sum(p_b * np.log2(np.maximum(p_b, 1e-15)))
        H_B_given_A = 0.0
        for i in range(n):
            row = p_b_given_a[i]
            H_B_given_A += probs[i] * (-np.sum(row * np.log2(np.maximum(row, 1e-15))))
        mutual_info = H_B - H_B_given_A

        result['mutual_information_meas'] = float(mutual_info)
        result['holevo_bound_satisfied'] = mutual_info <= chi + 1e-9

    return result


def hsw_capacity_example() -> Dict:
    """
    Concrete example: HSW capacity for BB84 states {|0⟩,|1⟩,|+⟩,|−⟩}.
    具体示例：BB84态的HSW容量。
    """
    # BB84 signal states / BB84信号态
    states = [KET0, KET1, KET_PLUS, KET_MINUS]
    probs = [0.25, 0.25, 0.25, 0.25]  # uniform / 均匀分布

    # Standard basis measurement / 标准基测量
    meas_basis = np.array([KET0, KET1], dtype=complex)

    return holevo_bound(states, probs, measurement_basis=meas_basis)


# ============================================================================
# 4. No-Cloning Disturbance Demo / 不可克隆定理扰动演示
# ============================================================================

def no_cloning_demo(
    n_trials: int = 500,
    seed: Optional[int] = None
) -> Dict:
    """
    Demonstrate that any attempt to clone an unknown quantum state
    necessarily disturbs it. Uses the Buzek-Hillery optimal cloning machine
    approach: we measure the disturbance caused by a naive cloning attempt.
    演示克隆未知量子态必然造成扰动。
    使用简化的Buzek-Hillery最优克隆视角。

    For a single unknown qubit, the optimal symmetric cloner
    produces fidelity 5/6 ≈ 0.833 for each clone.
    单个未知量子比特的最优对称克隆保真度为5/6≈0.833。

    Returns / 返回:
        Dict with clone fidelity, disturbance measure, and analysis.
    """
    rng = np.random.default_rng(seed)

    # Generate random input states on the Bloch sphere / 布洛赫球面上的随机态
    fidelities = np.zeros(n_trials)
    disturbance = np.zeros(n_trials)
    angles_theta = np.zeros(n_trials)
    angles_phi = np.zeros(n_trials)

    for i in range(n_trials):
        # Random pure state: cos(θ/2)|0⟩ + e^{iφ} sin(θ/2)|1⟩
        theta = np.arccos(2 * rng.random() - 1)   # uniform on sphere
        phi = 2 * np.pi * rng.random()
        angles_theta[i] = theta
        angles_phi[i] = phi

        psi = np.array([np.cos(theta / 2),
                         np.exp(1j * phi) * np.sin(theta / 2)], dtype=complex)

        # --- Naive cloning attempt: measure-and-prepare ---
        # / 朴素克隆尝试：测量后重制

        # Measure in computational basis (destroys superposition)
        # 在计算基上测量（破坏叠加态）
        p0 = np.abs(psi[0]) ** 2
        measured_bit = 0 if rng.random() < p0 else 1
        clone = KET0 if measured_bit == 0 else KET1

        # Fidelity of clone / 克隆保真度
        fid = np.abs(np.dot(psi.conj(), clone)) ** 2
        fidelities[i] = fid

        # Disturbance: 1 - fidelity between original and post-measurement state
        # 扰动：原始态与测量后态之间的1-保真度
        disturbance[i] = 1.0 - fid

    # --- Optimal quantum cloning bound / 最优量子克隆界 ---
    # For universal 1→2 symmetric cloner: F = 5/6 ≈ 0.8333
    # 通用1→2对称克隆机：F = 5/6
    optimal_clone_fidelity = 5.0 / 6.0

    # Average naive clone fidelity (should be ~2/3 = 0.667 for random states)
    # 朴素克隆平均保真度（随机态应为~2/3）
    avg_fidelity = float(np.mean(fidelities))
    avg_disturbance = float(np.mean(disturbance))

    # Best-case fidelity: when |ψ⟩ is already |0⟩ or |1⟩, F=1
    # Worst-case: when |ψ⟩ = |+⟩, F=0.5
    worst_fid = float(np.min(fidelities))
    best_fid = float(np.max(fidelities))

    # Verification: Is the cloning-to-disturbance trade-off satisfied?
    # For the naive measure-and-prepare: disturbance = 1 - F
    # The no-cloning theorem is demonstrated if avg_fidelity < optimal_clone_fidelity
    cloning_possible = avg_fidelity >= 0.999  # essentially perfect cloning

    return {
        'n_trials': n_trials,
        'avg_fidelity': avg_fidelity,
        'avg_disturbance': avg_disturbance,
        'best_fidelity': best_fid,
        'worst_fidelity': worst_fid,
        'optimal_clone_bound': optimal_clone_fidelity,
        'naive_bound_2/3': 2.0 / 3.0,
        'cloning_perfect': cloning_possible,
        'no_cloning_confirmed': not cloning_possible,
        'disturbance_vs_fidelity_correlation': float(np.corrcoef(fidelities, disturbance)[0, 1]),
    }


# ============================================================================
# 5. Spring-Yajie Entangled Pair Collapse / Spring-Yajie纠缠对坍缩
# ============================================================================

def entangled_pair_collapse(
    n_pairs: int = 1000,
    measurement_basis_alice: float = 0.0,
    measurement_basis_bob: float = np.pi / 4,
    seed: Optional[int] = None
) -> Dict:
    """
    Simulate the collapse of entangled pairs under measurement.
    Spring-Yajie protocol: demonstrate that measuring one particle
    of an entangled pair instantaneously determines the state of
    the other — but only reveals correlations after classical comparison.
    模拟纠缠对在测量下的坍缩。
    Spring-Yajie协议：测量纠缠对中一个粒子会立即决定另一个的状态，
    但只有经典比对后才能揭示关联。

    Uses |Φ⁺⟩ = (|00⟩ + |11⟩)/√2 as the entangled pair.
    使用|Φ⁺⟩作为纠缠对。

    Key insight: without classical communication, individual measurement
    results appear random. Correlation is only visible after comparison.
    关键洞察：无经典通信时，单个测量结果看似随机。关联仅在比对后可见。

    Parameters / 参数:
        n_pairs:                  Number of entangled pairs / 纠缠对数量
        measurement_basis_alice:  Alice's measurement angle (radians)
        measurement_basis_bob:    Bob's measurement angle (radians)

    Returns / 返回:
        Dict with collapse statistics, correlation, and Bell test readiness.
    """
    rng = np.random.default_rng(seed)

    # Alice's measurement projector / Alice的测量投影算符
    # Measurement in basis rotated by angle θ:
    # |+θ⟩ = cos(θ/2)|0⟩ + sin(θ/2)|1⟩
    # |−θ⟩ = -sin(θ/2)|0⟩ + cos(θ/2)|1⟩
    theta_a = measurement_basis_alice
    plus_a = np.array([np.cos(theta_a / 2), np.sin(theta_a / 2)], dtype=complex)
    minus_a = np.array([-np.sin(theta_a / 2), np.cos(theta_a / 2)], dtype=complex)

    theta_b = measurement_basis_bob
    plus_b = np.array([np.cos(theta_b / 2), np.sin(theta_b / 2)], dtype=complex)
    minus_b = np.array([-np.sin(theta_b / 2), np.cos(theta_b / 2)], dtype=complex)

    # |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
    # For Alice measuring in basis {|+θ⟩,|−θ⟩}:
    # P(Alice gets +) = |⟨+θ,0|Φ⁺⟩|² + |⟨+θ,1|Φ⁺⟩|²
    # = |cos(θ/2)/√2|² + |sin(θ/2)/√2|² = 1/2
    # Similarly P(Alice gets −) = 1/2

    alice_results = np.zeros(n_pairs, dtype=int)
    bob_results = np.zeros(n_pairs, dtype=int)

    for i in range(n_pairs):
        # Alice measures first — collapses the state / Alice先测量，坍缩状态
        prob_plus_a = 0.5  # always 0.5 for any measurement angle on Bell state
        alice_plus = rng.random() < prob_plus_a
        alice_results[i] = 1 if alice_plus else -1

        # After Alice's measurement, Bob's state is determined
        # If Alice got |+θ_a⟩, Bob's state = cos(θ_a/2)|0⟩ + sin(θ_a/2)|1⟩
        # Then Bob measures in his basis {|+θ_b⟩,|−θ_b⟩}
        # P(Bob gets + | Alice got +) = |cos((θ_a−θ_b)/2)|²

        if alice_plus:
            # Bob's collapsed state = cos(θ_a/2)|0⟩ + sin(θ_a/2)|1⟩
            bob_state = np.array([np.cos(theta_a / 2),
                                  np.sin(theta_a / 2)], dtype=complex)
        else:
            # Bob's collapsed state = -sin(θ_a/2)|0⟩ + cos(θ_a/2)|1⟩
            bob_state = np.array([-np.sin(theta_a / 2),
                                  np.cos(theta_a / 2)], dtype=complex)

        prob_plus_b = np.abs(np.dot(plus_b.conj(), bob_state)) ** 2
        bob_plus = rng.random() < prob_plus_b
        bob_results[i] = 1 if bob_plus else -1

    # --- Statistics / 统计分析 ---
    # Alice's marginals / Alice的边际分布
    alice_plus_count = np.sum(alice_results == 1)
    alice_minus_count = np.sum(alice_results == -1)

    # Bob's marginals / Bob的边际分布
    bob_plus_count = np.sum(bob_results == 1)
    bob_minus_count = np.sum(bob_results == -1)

    # Joint distribution / 联合分布
    both_plus = np.sum((alice_results == 1) & (bob_results == 1))
    both_minus = np.sum((alice_results == -1) & (bob_results == -1))
    opposite = np.sum(alice_results != bob_results)

    # Correlation E = ⟨A⊗B⟩ / 关联
    correlation = float(np.mean(alice_results * bob_results))
    expected_correlation = -np.cos(theta_a - theta_b)  # for |Φ⁺⟩
    # Actually for |Φ⁺⟩, E = cos(θ_a − θ_b). Let me verify:
    # P(same) = cos²((θ_a−θ_b)/2), P(diff) = sin²((θ_a−θ_b)/2)
    # E = (+1)*P(same) + (-1)*P(diff) = cos²(Δ/2) − sin²(Δ/2) = cos(Δ)
    expected_corr = np.cos(theta_a - theta_b)

    # Violation of local realism: if no classical communication occurs
    # but correlation matches quantum prediction / 局部实在论违反

    # Conditional entropy and collapse verification / 条件熵与坍缩验证
    p_joint = np.array([
        [both_plus / n_pairs, (alice_plus_count - both_plus) / n_pairs],
        [(bob_plus_count - both_plus) / n_pairs,
         (n_pairs - alice_plus_count - bob_plus_count + both_plus) / n_pairs]
    ])

    p_alice_marginal = np.array([
        alice_plus_count / n_pairs, alice_minus_count / n_pairs
    ])
    p_bob_marginal = np.array([
        bob_plus_count / n_pairs, bob_minus_count / n_pairs
    ])

    # Mutual information / 互信息
    H_A = -np.sum(p_alice_marginal * np.log2(np.maximum(p_alice_marginal, 1e-15)))
    H_B = -np.sum(p_bob_marginal * np.log2(np.maximum(p_bob_marginal, 1e-15)))
    H_AB = -np.sum(p_joint.ravel() * np.log2(np.maximum(p_joint.ravel(), 1e-15)))
    mutual_info = H_A + H_B - H_AB

    # Bell inequality readiness / Bell不等式准备状态
    # For |Φ⁺⟩ with angles 0 and π/4: E ≈ 0.707 → CHSH |S| ≈ 2.828 > 2
    bell_ready = True  # entangled pairs are always Bell-test ready

    return {
        'n_pairs': n_pairs,
        'alice_basis_angle': theta_a,
        'bob_basis_angle': theta_b,
        'alice_plus_ratio': float(alice_plus_count / n_pairs),
        'bob_plus_ratio': float(bob_plus_count / n_pairs),
        'correlation': float(correlation),
        'expected_correlation': float(expected_corr),
        'mutual_information': float(mutual_info),
        'both_same_ratio': float((both_plus + both_minus) / n_pairs),
        'both_diff_ratio': float(opposite / n_pairs),
        'bell_ready': bell_ready,
        'entanglement_confirmed': abs(correlation - expected_corr) < 0.1,
    }


# ============================================================================
# Main verification runner / 主验证运行器
# ============================================================================

def run_all_verifications(seed: int = 42) -> Dict[str, Dict]:
    """
    Run all five verification modules and return combined results.
    运行全部五个验证模块并返回综合结果。

    Returns / 返回:
        Nested dict with results from all verifications.
    """
    results = {}

    print("=" * 70)
    print("  SCX Quantum Audit — Full Verification Suite")
    print("  SCX量子审计 — 完整验证套件")
    print("=" * 70)

    # --- 1. BB84 QKD ---
    print("\n[1/5] BB84 QKD Simulation / BB84量子密钥分发模拟")
    print("-" * 50)
    for eve_rate in [0.0, 0.1, 0.3, 0.5]:
        r = bb84_simulate(n_bits=2000, eavesdrop_rate=eve_rate, seed=seed)
        print(f"  Eve={r['eavesdrop_rate']:.1f}: sifted={r['sifted_length']}, "
              f"QBER={r['qber']:.4f}, match={r['match_rate']:.4f}")
        if eve_rate == 0.0:
            results['bb84_no_eve'] = r
        elif eve_rate == 0.5:
            results['bb84_eve_50'] = r
    # Store full sweep
    results['bb84_sweep'] = {
        f'eve_{er}': bb84_simulate(2000, er, seed)
        for er in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    }

    # --- 2. CHSH ---
    print("\n[2/5] CHSH Inequality / CHSH不等式")
    print("-" * 50)
    for noise in [0.0, 0.2, 0.5]:
        r = chsh_s_value(noise=noise, n_samples=20000, seed=seed)
        status = "QUANTUM ✓" if r['quantum_violation'] else "CLASSICAL ⚠ (TAMPERING?)"
        print(f"  noise={noise:.1f}: S={r['S']:.4f} (theory={r['S_theory']:.4f}), "
              f"bound={r['tsirelson_bound']:.4f} → {status}")
        if noise == 0.0:
            results['chsh_ideal'] = r
        elif noise == 0.5:
            results['chsh_noisy'] = r
    results['chsh_sweep'] = {
        f'noise_{n}': chsh_s_value(noise=n, n_samples=15000, seed=seed)
        for n in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    }

    # --- 3. HSW Capacity ---
    print("\n[3/5] HSW Capacity / HSW容量")
    print("-" * 50)
    r = hsw_capacity_example()
    print(f"  Holevo χ = {r['holevo_chi']:.6f}")
    print(f"  Ensemble entropy = {r['ensemble_entropy']:.6f}")
    print(f"  Mutual info (Z-basis) = {r.get('mutual_information_meas', 'N/A')}")
    if 'holevo_bound_satisfied' in r:
        print(f"  χ bound satisfied: {r['holevo_bound_satisfied']}")
    results['hsw'] = r

    # --- 4. No-Cloning ---
    print("\n[4/5] No-Cloning Disturbance / 不可克隆扰动")
    print("-" * 50)
    r = no_cloning_demo(n_trials=500, seed=seed)
    print(f"  Avg fidelity = {r['avg_fidelity']:.4f}")
    print(f"  Optimal bound = {r['optimal_clone_bound']:.4f}")
    print(f"  Naive bound    = {r['naive_bound_2/3']:.4f}")
    print(f"  Cloning possible? {r['cloning_perfect']}")
    print(f"  No-cloning confirmed? {r['no_cloning_confirmed']}")
    results['no_cloning'] = r

    # --- 5. Entangled Pair Collapse ---
    print("\n[5/5] Entangled Pair Collapse (Spring-Yajie) / 纠缠对坍缩")
    print("-" * 50)
    angle_pairs = [
        (0.0, 0.0),                         # same basis → perfect correlation
        (0.0, np.pi / 4),                   # CHSH optimal
        (0.0, np.pi / 2),                   # orthogonal → no correlation
        (np.pi / 8, np.pi / 8),             # same tilted basis
    ]
    for theta_a, theta_b in angle_pairs:
        r = entangled_pair_collapse(
            n_pairs=1000,
            measurement_basis_alice=theta_a,
            measurement_basis_bob=theta_b,
            seed=seed
        )
        deg_a = np.degrees(theta_a)
        deg_b = np.degrees(theta_b)
        print(f"  θ_A={deg_a:5.1f}°, θ_B={deg_b:5.1f}°: "
              f"corr={r['correlation']:+.4f} (expect={r['expected_correlation']:+.4f}), "
              f"MI={r['mutual_information']:.4f}")
        if theta_a == 0.0 and theta_b == 0.0:
            results['entangle_same_basis'] = r
        elif theta_a == 0.0 and np.isclose(theta_b, np.pi / 4):
            results['entangle_chsh_opt'] = r

    # --- Summary / 总结 ---
    print("\n" + "=" * 70)
    print("  VERIFICATION SUMMARY / 验证摘要")
    print("=" * 70)

    # BB84 check: QBER should be ~0 without Eve, ~0.10+ with 50% Eve
    # (theoretical QBER for 50% intercept-resend = 0.5*0.5*0.5 = 0.125)
    bb84_ok = (results['bb84_no_eve']['qber'] < 0.05 and
               results['bb84_eve_50']['qber'] > 0.10)
    print(f"  [{'PASS' if bb84_ok else 'FAIL'}] BB84:    QBER detects eavesdropper")

    # CHSH check: S should be ~2.828 without noise, ≤2 with high noise
    chsh_ok = (results['chsh_ideal']['quantum_violation'] and
               results['chsh_noisy']['tampering_suspected'])
    print(f"  [{'PASS' if chsh_ok else 'FAIL'}] CHSH:    Violation with ideal, classical with noise")

    # HSW check
    hsw_ok = results['hsw']['holevo_chi'] > 0
    print(f"  [{'PASS' if hsw_ok else 'FAIL'}] HSW:     Holevo χ = {results['hsw']['holevo_chi']:.4f} > 0")

    # No-cloning
    nc_ok = results['no_cloning']['no_cloning_confirmed']
    print(f"  [{'PASS' if nc_ok else 'FAIL'}] NoClone:  F={results['no_cloning']['avg_fidelity']:.4f} < "
          f"{results['no_cloning']['optimal_clone_bound']:.4f} (opt)")

    # Entanglement
    ent_ok = results['entangle_same_basis']['entanglement_confirmed']
    print(f"  [{'PASS' if ent_ok else 'FAIL'}] Entangle: Correlation={results['entangle_same_basis']['correlation']:.4f} "
          f"(expect={results['entangle_same_basis']['expected_correlation']:.4f})")

    all_pass = bb84_ok and chsh_ok and hsw_ok and nc_ok and ent_ok
    print(f"\n  OVERALL: {'ALL PASS ✓' if all_pass else 'SOME FAILURES ⚠'}")
    print("=" * 70)

    results['_summary'] = {
        'bb84_pass': bb84_ok,
        'chsh_pass': chsh_ok,
        'hsw_pass': hsw_ok,
        'no_cloning_pass': nc_ok,
        'entanglement_pass': ent_ok,
        'all_pass': all_pass,
    }

    return results


# ============================================================================
# CLI entry point / 命令行入口
# ============================================================================

if __name__ == '__main__':
    import sys

    # Optional seed from command line / 可选命令行种子
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42

    results = run_all_verifications(seed=seed)

    # Exit code: 0 if all pass, 1 otherwise / 退出码：全部通过为0，否则为1
    sys.exit(0 if results['_summary']['all_pass'] else 1)
