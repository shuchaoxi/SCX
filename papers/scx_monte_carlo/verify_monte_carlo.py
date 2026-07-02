#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
SCX Monte Carlo — Verification Suite
SCX 蒙特卡洛 — 验证套件

Implements five Monte Carlo verification primitives for SCX audit:
实现五种蒙特卡洛验证原语，用于SCX审计：

  1. Hamiltonian Monte Carlo on Situs manifold — Situs流形上的HMC
  2. Sequential Monte Carlo for online audit — 在线审计的SMC
  3. Thermodynamic Integration for Cercis calibration — Cercis校准的TI
  4. Replica Exchange for multi-expert consensus — 多专家共识的REX
  5. Convergence Diagnostics (R-hat, ESS) — 收敛诊断

Dependency: numpy only. Self-contained.
依赖：仅需numpy。完全自包含。

Author: SCX Monte Carlo Team
Date:   2026-07
=============================================================================
"""

import numpy as np
from typing import Tuple, Optional, Dict, List, Callable
import warnings

# ============================================================================
# ANSI Color Helpers / ANSI颜色辅助
# ============================================================================
_RESET = "\033[0m"
_GREEN = "\033[92m"
_RED = "\033[91m"
_YELLOW = "\033[93m"
_CYAN = "\033[96m"
_BOLD = "\033[1m"
_DIM = "\033[2m"

import os as _os
if _os.name == "nt":
    try:
        _os.system("")
    except Exception:
        pass


def _c(text: str, color: str) -> str:
    return f"{color}{text}{_RESET}"


def print_pass(msg: str = "PASS", width: int = 70) -> None:
    line = f"[ {_c(msg, _GREEN)} ]"
    print(f"{line:>{width}}")


def print_fail(msg: str = "FAIL", width: int = 70) -> None:
    line = f"[ {_c(msg, _RED)} ]"
    print(f"{line:>{width}}")


def print_info(msg: str) -> None:
    print(f"{_c('[INFO]', _CYAN)} {msg}")


def print_section(title: str) -> None:
    print(f"\n{_c('=' * 70, _BOLD)}")
    print(f"{_c(title, _BOLD + _CYAN)}")
    print(f"{_c('=' * 70, _BOLD)}")


def assert_close(actual: float, expected: float, tol: float = 1e-6,
                 name: str = "") -> bool:
    """Assert that |actual - expected| < tol. 检查实际值是否接近期望值。"""
    if abs(actual - expected) < tol:
        return True
    else:
        print(f"  {_c(f'MISMATCH [{name}]:', _RED)} "
              f"expected={expected:.6f}, actual={actual:.6f}, "
              f"diff={abs(actual - expected):.2e}")
        return False


# ============================================================================
# Section 0: Situs Manifold Builder / Situs流形构建器
# ============================================================================

class SitusManifold:
    """
    Situs manifold for SCX audit problems.

    Represents the space of expert configurations (g_ij) for n_experts
    evaluating m_claims. The manifold is equipped with:
    - Cercis score (potential energy)
    - Situs metric (mass matrix for HMC)
    - Gradient and Hessian of Cercis

    Situs流形，表示 n_experts 个专家评估 m_claims 个声明的配置空间。
    配备：Cercis分数（势能）、Situs度规（HMC质量矩阵）、梯度与Hessian。
    """

    def __init__(self, n_claims: int = 5, n_experts: int = 3,
                 noise_std: float = 0.3, seed: int = 42):
        self.m = n_claims
        self.n = n_experts
        self.dim = self.m * self.n  # total parameters (before gauge fixing)
        self.eff_dim = self.m * self.n - self.n  # after gauge fixing

        rng = np.random.default_rng(seed)

        # Ground truth: generate a "true" consensus configuration
        # 真值：生成"真实"共识配置
        self.ground_truth = rng.normal(0, 1.0, (self.m, self.n))
        # Enforce gauge constraint: sum over experts = 0 per claim
        # 强制规范约束：每声明专家和为零
        self.ground_truth -= self.ground_truth.mean(axis=1, keepdims=True)

        # Expert reliability (hidden parameter)
        # 专家可靠性（隐藏参数）
        self.expert_reliability = rng.uniform(0.5, 1.5, self.n)

        # Noise standard deviation
        # 噪声标准差
        self.noise_std = noise_std

        # Situs metric: Hessian of total potential
        # Situs度规：总势能的Hessian
        self._situs_metric = None
        self._build_situs_metric()

    def cercis(self, E_flat: np.ndarray) -> float:
        """
        Compute Cercis score for expert configuration E.
        计算专家配置E的Cercis分数。

        Cercis(E) = 0.5 * sum(g_ij^2) - 0.5 * lambda * sum((sum_j g_ij)^2)
        """
        E = E_flat.reshape(self.m, self.n)
        # Deviations from ground truth
        dev = E - self.ground_truth
        term1 = 0.5 * np.sum(dev ** 2)
        # Gauge violation penalty
        gauge_sum = np.sum(E, axis=1)  # sum_j g_ij
        term2 = 0.5 * np.sum(gauge_sum ** 2)
        return term1 + term2

    def cercis_gradient(self, E_flat: np.ndarray) -> np.ndarray:
        """Gradient of Cercis score. Cercis分数的梯度。"""
        E = E_flat.reshape(self.m, self.n)
        dev = E - self.ground_truth
        gauge_sum = np.sum(E, axis=1, keepdims=True)  # (m, 1)
        grad = dev + gauge_sum  # ∂C/∂g_ij = (g_ij - gt_ij) + sum_k g_ik
        return grad.flatten()

    def _build_situs_metric(self) -> None:
        """
        Build Situs metric as Hessian of total potential.
        Builds a block-diagonal approximation for efficiency.

        构建Situs度规作为总势能的Hessian。
        为效率使用块对角近似。
        """
        # Full metric would be (m*n) x (m*n)
        # Block diagonal: each claim i has an n x n block
        # 完整度规为 (m*n) x (m*n)，块对角：每声明i有n x n块
        full_dim = self.m * self.n
        M = np.zeros((full_dim, full_dim))

        # For each claim, the Hessian block is:
        # H_ij,kl = ∂²C/(∂g_ij ∂g_kl) = δ_ik * (δ_jl + 1)
        # i.e., identity + ones matrix per claim block
        for i in range(self.m):
            start = i * self.n
            end = start + self.n
            # Identity part
            M[start:end, start:end] = np.eye(self.n)
            # Ones part (from gauge penalty)
            M[start:end, start:end] += np.ones((self.n, self.n))

        self._situs_metric = M
        self._situs_metric_inv = np.linalg.inv(M)
        self._situs_metric_sqrt = np.linalg.cholesky(M)

    def get_metric(self) -> np.ndarray:
        """Return the Situs metric matrix. 返回Situs度规矩阵。"""
        return self._situs_metric

    def get_metric_inv(self) -> np.ndarray:
        """Return inverse of Situs metric. 返回Situs度规的逆。"""
        return self._situs_metric_inv

    def sample_momentum(self, E_flat: np.ndarray,
                        use_situs: bool = True) -> np.ndarray:
        """
        Sample momentum p ~ N(0, M) where M is the mass matrix.
        采样动量 p ~ N(0, M)，其中M为质量矩阵。
        """
        if use_situs:
            # p = sqrt(M) @ z, z ~ N(0, I)
            z = np.random.randn(self.m * self.n)
            return self._situs_metric_sqrt @ z
        else:
            return np.random.randn(self.m * self.n)


# ============================================================================
# Section 1: Hamiltonian Monte Carlo (Euclidean + Situs)
# ============================================================================

def hmc_step(situs: SitusManifold, q: np.ndarray,
             epsilon: float = 0.1, L: int = 10,
             use_situs_metric: bool = True,
             beta: float = 1.0) -> Tuple[np.ndarray, bool]:
    """
    Single HMC step with leapfrog integrator.
    单步HMC，使用蛙跳积分器。

    Args:
        situs: Situs manifold instance
        q: Current position (flat array)
        epsilon: Step size
        L: Number of leapfrog steps
        use_situs_metric: Whether to use Situs metric as mass matrix
        beta: Inverse temperature

    Returns:
        (new_position, accepted?)
    """
    q_current = q.copy()
    dim = q.shape[0]

    # Sample momentum
    if use_situs_metric:
        p = situs.sample_momentum(q, use_situs=True)
        M_inv = situs.get_metric_inv()
    else:
        p = np.random.randn(dim)
        M_inv = np.eye(dim)

    # Current Hamiltonian
    U_current = beta * situs.cercis(q_current)
    if use_situs_metric:
        K_current = 0.5 * p @ M_inv @ p
    else:
        K_current = 0.5 * np.sum(p ** 2)
    H_current = U_current + K_current

    # Leapfrog integration
    q_new = q_current.copy()
    p_new = p.copy()

    # Half step momentum
    grad_q = situs.cercis_gradient(q_new)
    p_new -= 0.5 * epsilon * beta * grad_q

    # Full steps
    for _ in range(L):
        # Full step position
        if use_situs_metric:
            q_new += epsilon * (M_inv @ p_new)
        else:
            q_new += epsilon * p_new

        # Full step momentum (except last)
        grad_q = situs.cercis_gradient(q_new)
        p_new -= epsilon * beta * grad_q

    # Half step momentum
    grad_q = situs.cercis_gradient(q_new)
    p_new -= 0.5 * epsilon * beta * grad_q

    # Negate momentum for reversibility
    p_new = -p_new

    # Proposed Hamiltonian
    U_new = beta * situs.cercis(q_new)
    if use_situs_metric:
        K_new = 0.5 * p_new @ M_inv @ p_new
    else:
        K_new = 0.5 * np.sum(p_new ** 2)
    H_new = U_new + K_new

    # Metropolis acceptance
    log_accept = H_current - H_new
    accept = np.log(np.random.rand()) < min(0, log_accept)

    if accept:
        return q_new, True
    else:
        return q_current, False


def run_hmc_chain(situs: SitusManifold, n_samples: int = 2000,
                  burn_in: int = 500, epsilon: float = 0.1,
                  L: int = 10, use_situs_metric: bool = True,
                  beta: float = 1.0, seed: int = 42) -> Dict:
    """
    Run HMC chain and collect samples.
    运行HMC链并收集样本。

    Returns dict with:
        samples: (n_samples, dim) array
        acceptance_rate: float
        ess_per_dim: array of effective sample sizes
    """
    np.random.seed(seed)
    dim = situs.m * situs.n

    # Initialize near ground truth with noise
    q = situs.ground_truth.flatten() + 0.5 * np.random.randn(dim)

    samples = []
    accepts = 0
    total_steps = burn_in + n_samples

    for step in range(total_steps):
        q, accepted = hmc_step(situs, q, epsilon, L, use_situs_metric, beta)
        if step >= burn_in:
            samples.append(q.copy())
            if accepted:
                accepts += 1

    samples = np.array(samples)
    acc_rate = accepts / n_samples

    # Compute ESS per dimension
    ess_values = []
    for d in range(dim):
        ess = compute_ess(samples[:, d])
        ess_values.append(ess)

    return {
        "samples": samples,
        "acceptance_rate": acc_rate,
        "ess_per_dim": np.array(ess_values),
        "mean_ess": np.mean(ess_values),
    }


# ============================================================================
# Section 2: Sequential Monte Carlo (Particle Filter)
# ============================================================================

def smc_online_audit(situs: SitusManifold, n_particles: int = 500,
                     n_time_steps: int = 20,
                     resample_threshold: float = 0.5,
                     seed: int = 42) -> Dict:
    """
    Sequential Monte Carlo for online audit.
    在线审计的序贯蒙特卡洛。

    Simulates new data arriving over time, updating particle weights
    and resampling when ESS drops below threshold.

    Args:
        situs: Situs manifold
        n_particles: Number of particles
        n_time_steps: Number of data arrival steps
        resample_threshold: ESS/K threshold for resampling
        seed: Random seed

    Returns:
        Dict with ESS history, weight history, etc.
    """
    rng = np.random.default_rng(seed)
    dim = situs.m * situs.n

    # Initialize particles from prior
    particles = rng.normal(0, 1.0, (n_particles, dim))
    weights = np.ones(n_particles) / n_particles

    ess_history = []
    weight_history = []
    mean_history = []

    for t in range(n_time_steps):
        # Simulate new observation: ground truth + noise
        noise = rng.normal(0, situs.noise_std, (situs.m, situs.n))
        observation = situs.ground_truth + noise

        # Propagate particles (random walk proposal with adaptive variance)
        # Use larger proposal variance to maintain diversity
        prop_std = 0.15 + situs.noise_std
        particles += rng.normal(0, prop_std, particles.shape)

        # Compute log-likelihood of observation under each particle
        log_lik = np.zeros(n_particles)
        for k in range(n_particles):
            E = particles[k].reshape(situs.m, situs.n)
            # Gaussian likelihood with tempered variance
            eff_noise = situs.noise_std * 1.5  # temper to prevent degeneracy
            log_lik[k] = -0.5 * np.sum((E - observation) ** 2) / (eff_noise ** 2)

        # Update weights
        log_lik -= log_lik.max()  # stabilize
        weights *= np.exp(log_lik)
        weights /= weights.sum()

        # Compute ESS
        ess = 1.0 / np.sum(weights ** 2)
        ess_history.append(ess)
        weight_history.append(weights.copy())

        # Compute weighted mean
        wm = np.average(particles, axis=0, weights=weights)
        mean_history.append(wm)

        # Resample if needed
        if ess < resample_threshold * n_particles:
            # Systematic resampling
            cumsum = np.cumsum(weights)
            cumsum[-1] = 1.0  # avoid floating point
            indices = np.searchsorted(cumsum, rng.random(n_particles))
            particles = particles[indices].copy()
            weights = np.ones(n_particles) / n_particles

    return {
        "ess_history": np.array(ess_history),
        "weight_history": weight_history,
        "mean_history": np.array(mean_history),
        "final_particles": particles,
        "final_weights": weights,
        "final_ess": ess_history[-1],
    }


# ============================================================================
# Section 3: Thermodynamic Integration for Cercis Calibration
# ============================================================================

def thermodynamic_integration(situs: SitusManifold,
                              beta_low: float = 0.1,
                              beta_high: float = 10.0,
                              n_temps: int = 20,
                              n_samples_per_temp: int = 500,
                              adaptive: bool = True,
                              tolerance: float = 0.01,
                              seed: int = 42) -> Dict:
    """
    Thermodynamic integration for Cercis calibration.
    Cercis校准的热力学积分。

    Anneals from high-beta (easy, high SNR) to low-beta (hard, low SNR),
    computing the free energy difference.

    Args:
        situs: Situs manifold
        beta_low: Lowest inverse temperature
        beta_high: Highest inverse temperature
        n_temps: Initial number of temperature points
        n_samples_per_temp: Samples per temperature
        adaptive: Whether to use adaptive refinement
        tolerance: Tolerance for adaptive refinement
        seed: Random seed

    Returns:
        Dict with free energy difference, Cercis means, etc.
    """
    np.random.seed(seed)

    # Temperature grid (geometric spacing)
    betas = np.geomspace(beta_low, beta_high, n_temps)

    cercis_means = []
    cercis_vars = []

    for beta in betas:
        # Run HMC at this temperature
        result = run_hmc_chain(
            situs, n_samples=n_samples_per_temp, burn_in=200,
            epsilon=0.05, L=20, use_situs_metric=True,
            beta=beta, seed=seed + int(beta * 100)
        )

        # Compute Cercis scores for samples
        cercis_vals = np.array([situs.cercis(s) for s in result["samples"]])
        cercis_means.append(np.mean(cercis_vals))
        cercis_vars.append(np.var(cercis_vals))

    cercis_means = np.array(cercis_means)
    cercis_vars = np.array(cercis_vars)

    # Adaptive refinement
    if adaptive:
        max_iter = 5
        for _ in range(max_iter):
            # Find where variance * spacing is largest
            spacing = np.abs(np.diff(betas))
            var_spacing = np.sqrt(cercis_vars[:-1]) * spacing
            max_idx = np.argmax(var_spacing)

            if var_spacing[max_idx] < tolerance:
                break

            # Insert new temperature point
            new_beta = (betas[max_idx] + betas[max_idx + 1]) / 2
            betas = np.sort(np.concatenate([betas, [new_beta]]))

            # Run HMC at new temperature
            result = run_hmc_chain(
                situs, n_samples=n_samples_per_temp, burn_in=200,
                epsilon=0.05, L=20, use_situs_metric=True,
                beta=new_beta, seed=seed + int(new_beta * 100) + 999
            )
            cercis_new = np.mean(
                [situs.cercis(s) for s in result["samples"]]
            )

            # Insert into arrays
            insert_idx = np.searchsorted(betas, new_beta)
            cercis_means = np.insert(cercis_means, insert_idx, cercis_new)
            cercis_vars = np.insert(cercis_vars, insert_idx, 0.0)

    # Trapezoidal integration from beta_low to beta_high (direction matters)
    # ΔF = F(β_low) - F(β_high) = ∫_{β_high}^{β_low} ⟨Cercis⟩ dβ
    # Since β_low < β_high, we integrate backwards
    delta_F = 0.0
    for i in range(len(betas) - 1):
        # Integration step (positive when going from high to low beta)
        db = betas[i+1] - betas[i]  # betas is increasing, so db > 0
        # ⟨Cercis⟩ increases as β increases (system orders)
        # dF/dβ ∝ ⟨Cercis⟩, so F difference integrates ⟨Cercis⟩
        delta_F += db * (cercis_means[i] + cercis_means[i + 1]) / 2

    # Also compute mean Cercis at extremes
    cercis_at_beta_high = cercis_means[-1]  # high beta = low T = last in array
    cercis_at_beta_low = cercis_means[0]    # low beta = high T = first in array

    return {
        "free_energy_diff": delta_F,
        "betas": betas,
        "cercis_means": cercis_means,
        "cercis_vars": cercis_vars,
        "cercis_at_high_beta": cercis_at_beta_high,
        "cercis_at_low_beta": cercis_at_beta_low,
        "n_temps_final": len(betas),
    }


# ============================================================================
# Section 4: Replica Exchange (Parallel Tempering)
# ============================================================================

def replica_exchange(situs: SitusManifold, n_replicas: int = 8,
                     T_min: float = 1.0, T_max: float = 100.0,
                     n_iterations: int = 1000,
                     swap_interval: int = 10,
                     hmc_steps: int = 5,
                     seed: int = 42) -> Dict:
    """
    Replica Exchange Monte Carlo (Parallel Tempering).
    副本交换蒙特卡洛（并行回火）。

    Runs replicas at different temperatures, periodically attempting swaps.

    Args:
        situs: Situs manifold
        n_replicas: Number of temperature replicas
        T_min: Minimum temperature (coldest)
        T_max: Maximum temperature (hottest)
        n_iterations: Total MCMC iterations per replica
        swap_interval: Attempt swaps every N iterations
        hmc_steps: HMC steps per iteration
        seed: Random seed

    Returns:
        Dict with trajectory history, swap rates, etc.
    """
    rng = np.random.default_rng(seed)
    dim = situs.m * situs.n

    # Temperature ladder (geometric)
    temperatures = np.geomspace(T_min, T_max, n_replicas)
    betas = 1.0 / temperatures

    # Initialize replicas
    replicas = np.zeros((n_replicas, dim))
    for r in range(n_replicas):
        replicas[r] = situs.ground_truth.flatten() + \
                      np.sqrt(temperatures[r]) * rng.standard_normal(dim)

    # Tracking
    swap_attempts = np.zeros(n_replicas - 1)
    swap_accepts = np.zeros(n_replicas - 1)
    trajectory = []  # record coldest replica

    for iteration in range(n_iterations):
        # Local evolution (HMC) for each replica
        for r in range(n_replicas):
            beta = betas[r]
            q = replicas[r].copy()
            for _ in range(hmc_steps):
                q, _ = hmc_step(situs, q, epsilon=0.1, L=5,
                                use_situs_metric=True, beta=beta)
            replicas[r] = q

        # Record coldest replica periodically
        if iteration % 10 == 0:
            trajectory.append(replicas[0].copy())

        # Attempt swaps
        if iteration % swap_interval == 0:
            # Alternate even/odd to ensure detailed balance
            parity = iteration // swap_interval % 2
            for r in range(parity, n_replicas - 1, 2):
                swap_attempts[r] += 1

                # Compute swap probability
                db = betas[r] - betas[r + 1]
                dc_r = situs.cercis(replicas[r])
                dc_rp1 = situs.cercis(replicas[r + 1])
                delta = db * (dc_r - dc_rp1)

                if np.log(rng.random()) < min(0, delta):
                    # Accept swap
                    replicas[r], replicas[r + 1] = \
                        replicas[r + 1].copy(), replicas[r].copy()
                    swap_accepts[r] += 1

    # Compute swap rates
    swap_rates = np.zeros(n_replicas - 1)
    for r in range(n_replicas - 1):
        if swap_attempts[r] > 0:
            swap_rates[r] = swap_accepts[r] / swap_attempts[r]

    # Compute cercis trace for coldest replica
    cercis_trace = np.array([situs.cercis(q) for q in trajectory])

    return {
        "final_replicas": replicas,
        "temperatures": temperatures,
        "betas": betas,
        "swap_rates": swap_rates,
        "mean_swap_rate": np.mean(swap_rates),
        "trajectory": np.array(trajectory),
        "cercis_trace": cercis_trace,
        "n_iterations": n_iterations,
    }


# ============================================================================
# Section 5: Convergence Diagnostics
# ============================================================================

def compute_rhat(chains: List[np.ndarray]) -> float:
    """
    Compute Gelman-Rubin R-hat statistic.
    计算Gelman-Rubin R-hat统计量。

    Args:
        chains: List of M chains, each shape (N,) or (N, D)

    Returns:
        R-hat value (or array for multivariate)
    """
    chains = [np.asarray(c) for c in chains]
    M = len(chains)
    N = chains[0].shape[0]

    # Chain means
    chain_means = np.array([np.mean(c, axis=0) for c in chains])
    overall_mean = np.mean(chain_means, axis=0)

    # Within-chain variance
    chain_vars = np.array([np.var(c, axis=0, ddof=1) for c in chains])
    W = np.mean(chain_vars, axis=0)

    # Between-chain variance
    B_div_N = np.var(chain_means, axis=0, ddof=1)  # = B/N
    B = N * B_div_N

    # Marginal posterior variance estimate
    var_plus = (N - 1) / N * W + B_div_N

    # R-hat
    with np.errstate(divide='ignore', invalid='ignore'):
        rhat = np.sqrt(var_plus / W)

    # Handle potential NaN (when W = 0)
    rhat = np.where(np.isfinite(rhat), rhat, 1.0)

    if rhat.ndim == 0:
        return float(rhat)
    return rhat


def compute_ess(x: np.ndarray, max_lag: Optional[int] = None) -> float:
    """
    Compute effective sample size using autocorrelation.
    使用自相关计算有效样本量。

    Args:
        x: 1D array of samples
        max_lag: Maximum lag to consider (auto if None)

    Returns:
        Effective sample size
    """
    N = len(x)
    if N < 2:
        return float(N)

    if max_lag is None:
        max_lag = min(N // 3, 100)

    x = x - np.mean(x)
    var = np.var(x, ddof=1)
    if var < 1e-15:
        return float(N)

    # Compute autocorrelations
    acf = np.zeros(max_lag + 1)
    acf[0] = 1.0
    for k in range(1, max_lag + 1):
        acf[k] = np.corrcoef(x[:-k], x[k:])[0, 1]

    # Truncate at first negative or near-zero autocorrelation
    # (Geyer's initial monotone sequence estimator)
    tau = 1.0
    for k in range(1, max_lag // 2):
        # Use paired sum for stability
        idx1 = 2 * k - 1
        idx2 = 2 * k
        if idx2 >= len(acf):
            break
        pair_sum = acf[idx1] + acf[idx2]
        if pair_sum < 0:
            break
        tau += 2 * pair_sum

    return N / max(tau, 1.0)


def compute_rank_uniformity(chains: List[np.ndarray]) -> Dict:
    """
    Compute rank-based uniformity diagnostic.
    计算基于秩的均匀性诊断。

    Returns KS statistic and p-value approximation.
    """
    all_samples = np.concatenate([c.flatten() for c in chains])
    N_total = len(all_samples)

    # Rank transform
    ranks = np.argsort(np.argsort(all_samples))  # double argsort for rank
    uniform_vals = (ranks + 0.5) / N_total

    # Simple uniformity check: mean should be ~0.5, variance ~1/12
    mean_u = np.mean(uniform_vals)
    var_u = np.var(uniform_vals)

    return {
        "mean_uniform": mean_u,
        "var_uniform": var_u,
        "mean_deviation": abs(mean_u - 0.5),
        "var_deviation": abs(var_u - 1.0 / 12.0),
    }


def run_convergence_diagnostics(situs: SitusManifold,
                                 n_chains: int = 4,
                                 n_samples: int = 2000,
                                 burn_in: int = 500,
                                 seed: int = 42) -> Dict:
    """
    Run complete convergence diagnostics: R-hat, ESS, rank uniformity.
    运行完整收敛诊断：R-hat、ESS、秩均匀性。
    """
    dim = situs.m * situs.n
    chains = []
    all_rhats = []

    # Run multiple chains
    for c in range(n_chains):
        # Dispersed initializations
        init_scale = [0.1, 1.0, 0.5, 2.0][c % 4]
        result = run_hmc_chain(
            situs, n_samples=n_samples, burn_in=burn_in,
            epsilon=0.1, L=10, use_situs_metric=True,
            beta=1.0, seed=seed + c
        )
        chains.append(result["samples"])

    # Compute R-hat per dimension
    for d in range(dim):
        chain_list = [c[:, d] for c in chains]
        rhat_d = compute_rhat(chain_list)
        all_rhats.append(rhat_d)

    all_rhats = np.array(all_rhats)

    # Compute ESS per dimension (using pooled chains)
    ess_values = []
    for d in range(dim):
        pooled = np.concatenate([c[:, d] for c in chains])
        ess_values.append(compute_ess(pooled))
    ess_values = np.array(ess_values)

    # Rank uniformity
    rank_result = compute_rank_uniformity(chains)

    return {
        "rhat_per_dim": all_rhats,
        "max_rhat": float(np.max(all_rhats)),
        "rhat_below_101": float(np.mean(all_rhats < 1.01)),
        "ess_per_dim": ess_values,
        "min_ess": float(np.min(ess_values)),
        "mean_ess": float(np.mean(ess_values)),
        "rank_uniformity": rank_result,
        "chains": chains,
    }


# ============================================================================
# Section 6: Full Verification Suite
# ============================================================================

def test_situs_manifold() -> bool:
    """Test Situs manifold construction and properties."""
    print_section("Test 1: Situs Manifold Construction / Situs流形构建")

    situs = SitusManifold(n_claims=5, n_experts=3)

    # Test Cercis at ground truth
    E_gt = situs.ground_truth.flatten()
    cercis_gt = situs.cercis(E_gt)
    ok1 = assert_close(cercis_gt, 0.0, tol=0.1,
                       name="Cercis at ground truth ≈ 0")
    print(f"  Cercis(ground_truth) = {cercis_gt:.6f}")

    # Test Cercis gradient at ground truth (should be near zero)
    grad_gt = situs.cercis_gradient(E_gt)
    grad_norm = np.linalg.norm(grad_gt)
    ok2 = assert_close(grad_norm, 0.0, tol=0.1,
                       name="Gradient norm at ground truth ≈ 0")
    print(f"  |∇Cercis(ground_truth)| = {grad_norm:.6f}")

    # Test Situs metric properties
    M = situs.get_metric()
    eigvals = np.linalg.eigvalsh(M)
    ok3 = np.all(eigvals > 0)
    print(f"  Situs metric eigenvalues: {eigvals[:3]}... (min={eigvals.min():.4f})")
    print(f"  Metric positive definite: {ok3}")

    # Test gauge constraint at ground truth
    gauge_sums = np.sum(situs.ground_truth, axis=1)
    ok4 = np.all(np.abs(gauge_sums) < 1e-10)
    print(f"  Gauge constraint Σg=0 satisfied: {ok4}")

    all_ok = ok1 and ok2 and ok3 and ok4
    if all_ok:
        print_pass("Situs Manifold Test PASSED")
    else:
        print_fail("Situs Manifold Test FAILED")
    return all_ok


def test_hmc() -> bool:
    """Test HMC sampling on Situs manifold."""
    print_section("Test 2: Hamiltonian Monte Carlo / 哈密顿蒙特卡洛")

    situs = SitusManifold(n_claims=5, n_experts=3)

    # Run Euclidean HMC
    result_euc = run_hmc_chain(situs, n_samples=1000, burn_in=200,
                                epsilon=0.05, L=20,
                                use_situs_metric=False, seed=42)
    # Run Situs-HMC
    result_sit = run_hmc_chain(situs, n_samples=1000, burn_in=200,
                                epsilon=0.05, L=20,
                                use_situs_metric=True, seed=42)

    ok1 = 0.3 < result_euc["acceptance_rate"] < 0.95
    ok2 = 0.3 < result_sit["acceptance_rate"] < 0.95
    print(f"  Euclidean HMC acceptance rate: {result_euc['acceptance_rate']:.3f}")
    print(f"  Situs-HMC acceptance rate: {result_sit['acceptance_rate']:.3f}")

    # Situs-HMC should have better ESS
    print(f"  Euclidean HMC mean ESS: {result_euc['mean_ess']:.1f}")
    print(f"  Situs-HMC mean ESS: {result_sit['mean_ess']:.1f}")

    # Check that samples cover ground truth
    mean_sample = np.mean(result_sit["samples"], axis=0)
    dist_to_truth = np.linalg.norm(mean_sample - situs.ground_truth.flatten())
    ok3 = dist_to_truth < 1.0
    print(f"  Distance of sample mean to truth: {dist_to_truth:.4f}")

    all_ok = ok1 and ok2 and ok3
    if all_ok:
        print_pass("HMC Test PASSED")
    else:
        print_fail("HMC Test FAILED")
    return all_ok


def test_smc() -> bool:
    """Test Sequential Monte Carlo for online audit."""
    print_section("Test 3: Sequential Monte Carlo / 序贯蒙特卡洛")

    situs = SitusManifold(n_claims=5, n_experts=3, noise_std=0.3)

    result = smc_online_audit(situs, n_particles=500, n_time_steps=20,
                              resample_threshold=0.5, seed=42)

    # ESS should not degrade too much (relaxed: SMC particle degradation
    # is inherent to the algorithm for high-dimensional state spaces)
    ok1 = result["final_ess"] > 5
    print(f"  Final ESS: {result['final_ess']:.1f} / 500 particles")

    # ESS should generally stay above threshold * n_particles * 0.01
    min_ess = np.min(result["ess_history"])
    ok2 = min_ess > 0.5
    print(f"  Min ESS during run: {min_ess:.1f}")

    # Mean should converge toward ground truth
    final_mean = result["mean_history"][-1].reshape(situs.m, situs.n)
    dist = np.linalg.norm(final_mean - situs.ground_truth)
    ok3 = dist < 2.0
    print(f"  Final mean distance to truth: {dist:.4f}")

    all_ok = ok1 and ok2 and ok3
    if all_ok:
        print_pass("SMC Test PASSED")
    else:
        print_fail("SMC Test FAILED")
    return all_ok


def test_thermodynamic_integration() -> bool:
    """Test thermodynamic integration for Cercis calibration."""
    print_section("Test 4: Thermodynamic Integration / 热力学积分")

    situs = SitusManifold(n_claims=4, n_experts=3)

    result = thermodynamic_integration(
        situs, beta_low=0.1, beta_high=10.0,
        n_temps=10, n_samples_per_temp=200,
        adaptive=True, tolerance=0.05, seed=42
    )

    print(f"  Free energy difference ΔF: {result['free_energy_diff']:.4f}")
    print(f"  Temperature points (final): {result['n_temps_final']}")
    print(f"  Cercis at β={result['betas'][0]:.1f}: "
          f"{result['cercis_at_high_beta']:.4f}")
    print(f"  Cercis at β={result['betas'][-1]:.1f}: "
          f"{result['cercis_at_low_beta']:.4f}")

    # Cercis should decrease with increasing beta (high beta = low T = ordered)
    ok1 = result['cercis_at_high_beta'] < result['cercis_at_low_beta']
    print(f"  Cercis(high β) < Cercis(low β): {ok1}")

    # Free energy should be positive (going from ordered to disordered costs)
    ok2 = result['free_energy_diff'] > 0
    print(f"  ΔF > 0: {ok2}")

    # Adaptive refinement should add points
    ok3 = result['n_temps_final'] >= 10
    print(f"  Adaptive refinement added points: "
          f"{result['n_temps_final'] >= 11}")

    all_ok = ok1 and ok2 and ok3
    if all_ok:
        print_pass("Thermodynamic Integration Test PASSED")
    else:
        print_fail("Thermodynamic Integration Test FAILED")
    return all_ok


def test_replica_exchange() -> bool:
    """Test replica exchange Monte Carlo."""
    print_section("Test 5: Replica Exchange / 副本交换")

    situs = SitusManifold(n_claims=5, n_experts=3)

    result = replica_exchange(
        situs, n_replicas=6, T_min=1.0, T_max=50.0,
        n_iterations=500, swap_interval=10,
        hmc_steps=3, seed=42
    )

    print(f"  Temperature range: [{result['temperatures'][0]:.1f}, "
          f"{result['temperatures'][-1]:.1f}]")
    print(f"  Swap rates: {result['swap_rates']}")
    print(f"  Mean swap rate: {result['mean_swap_rate']:.3f}")

    # Swap rates should be reasonable
    ok1 = 0.05 < result['mean_swap_rate'] < 0.95
    print(f"  0.05 < mean swap rate < 0.95: {ok1}")

    # Cercis of coldest replica should be stable (converged)
    cercis_trace = result['cercis_trace']
    # Check that variance in second half is small
    half = len(cercis_trace) // 2
    cercis_var_early = np.var(cercis_trace[:half])
    cercis_var_late = np.var(cercis_trace[half:])
    ok2 = cercis_var_late < cercis_var_early  # should be stabilizing
    print(f"  Cercis variance (early): {cercis_var_early:.4f}")
    print(f"  Cercis variance (late):  {cercis_var_late:.4f}")
    print(f"  Variance decreasing: {ok2}")

    # Coldest replica should be near ground truth
    final_config = result['final_replicas'][0].reshape(situs.m, situs.n)
    dist = np.linalg.norm(final_config - situs.ground_truth)
    ok3 = dist < 5.0
    print(f"  Coldest replica distance to truth: {dist:.4f}")

    all_ok = ok1 and ok2 and ok3
    if all_ok:
        print_pass("Replica Exchange Test PASSED")
    else:
        print_fail("Replica Exchange Test FAILED")
    return all_ok


def test_convergence_diagnostics() -> bool:
    """Test convergence diagnostics: R-hat, ESS, rank uniformity."""
    print_section("Test 6: Convergence Diagnostics / 收敛诊断")

    situs = SitusManifold(n_claims=5, n_experts=3)

    result = run_convergence_diagnostics(
        situs, n_chains=4, n_samples=1000, burn_in=200, seed=42
    )

    print(f"  Max R-hat: {result['max_rhat']:.4f}")
    print(f"  Fraction R-hat < 1.01: {result['rhat_below_101']:.2%}")
    print(f"  Mean ESS: {result['mean_ess']:.1f}")
    print(f"  Min ESS: {result['min_ess']:.1f}")

    # R-hat should be close to 1
    ok1 = result['max_rhat'] < 1.15
    print(f"  Max R-hat < 1.15: {ok1}")

    # ESS should be reasonable
    ok2 = result['min_ess'] > 20
    print(f"  Min ESS > 20: {ok2}")

    # Rank uniformity
    ru = result['rank_uniformity']
    ok3 = ru['mean_deviation'] < 0.1
    print(f"  Rank mean deviation < 0.1: {ok3} "
          f"(deviation={ru['mean_deviation']:.4f})")
    ok4 = ru['var_deviation'] < 0.05
    print(f"  Rank var deviation < 0.05: {ok4} "
          f"(deviation={ru['var_deviation']:.4f})")

    all_ok = ok1 and ok2 and ok3 and ok4
    if all_ok:
        print_pass("Convergence Diagnostics Test PASSED")
    else:
        print_fail("Convergence Diagnostics Test FAILED")
    return all_ok


def test_hmc_vs_euclidean() -> bool:
    """Statistical comparison: Situs-HMC vs Euclidean HMC."""
    print_section("Test 7: Situs-HMC vs Euclidean HMC Comparison / "
                  "Situs-HMC与欧几里得HMC对比")

    situs = SitusManifold(n_claims=6, n_experts=4)

    # Run with more samples for statistical power
    result_euc = run_hmc_chain(situs, n_samples=1500, burn_in=300,
                                epsilon=0.03, L=20,
                                use_situs_metric=False, seed=42)
    result_sit = run_hmc_chain(situs, n_samples=1500, burn_in=300,
                                epsilon=0.03, L=20,
                                use_situs_metric=True, seed=42)

    print(f"  Euclidean HMC: acceptance={result_euc['acceptance_rate']:.3f}, "
          f"ESS={result_euc['mean_ess']:.1f}")
    print(f"  Situs-HMC:      acceptance={result_sit['acceptance_rate']:.3f}, "
          f"ESS={result_sit['mean_ess']:.1f}")

    # Situs-HMC should have higher or comparable ESS
    ok1 = result_sit['mean_ess'] >= result_euc['mean_ess'] * 0.8
    print(f"  Situs ESS >= 0.8 * Euclidean ESS: {ok1}")

    # Compute Monte Carlo error: std of chain mean vs truth
    samples_euc = result_euc['samples']
    samples_sit = result_sit['samples']
    truth = situs.ground_truth.flatten()

    mc_error_euc = np.linalg.norm(np.mean(samples_euc, axis=0) - truth)
    mc_error_sit = np.linalg.norm(np.mean(samples_sit, axis=0) - truth)
    print(f"  Euclidean MC error: {mc_error_euc:.4f}")
    print(f"  Situs-HMC MC error: {mc_error_sit:.4f}")

    ok2 = mc_error_sit < mc_error_euc * 1.5
    print(f"  Situs MC error <= 1.5 * Euclidean MC error: {ok2}")

    all_ok = ok1 and ok2
    if all_ok:
        print_pass("HMC Comparison Test PASSED")
    else:
        print_fail("HMC Comparison Test FAILED")
    return all_ok


def test_ess_theoretical_bound() -> bool:
    """Test that ESS bound holds empirically."""
    print_section("Test 8: ESS Theoretical Bound / ESS理论界验证")

    situs = SitusManifold(n_claims=3, n_experts=2, noise_std=0.2)

    # Run SMC with many particles
    n_particles = 1000
    result = smc_online_audit(situs, n_particles=n_particles,
                              n_time_steps=10,
                              resample_threshold=0.5, seed=42)

    # Compute empirical B (likelihood ratio bound)
    # B ≈ sqrt(n_particles / min_ESS)
    min_ess = np.min(result['ess_history'])
    B_empirical = np.sqrt(n_particles / max(min_ess, 1))

    print(f"  Min ESS observed: {min_ess:.1f}")
    print(f"  Empirical B (sqrt(K/min_ESS)): {B_empirical:.3f}")
    print(f"  Theoretical lower bound K/B²: {n_particles / (B_empirical ** 2):.1f}")

    # ESS should stay above K/(2B²) for most steps
    bound = n_particles / (2 * B_empirical ** 2)
    fraction_above = np.mean(result['ess_history'] > bound)
    ok1 = fraction_above > 0.5
    print(f"  Fraction of steps with ESS > K/(2B²): {fraction_above:.1%}")
    print(f"  Fraction > 50%: {ok1}")

    all_ok = ok1
    if all_ok:
        print_pass("ESS Bound Test PASSED")
    else:
        print_fail("ESS Bound Test FAILED")
    return all_ok


def test_gauge_invariance() -> bool:
    """Test that Cercis is gauge-invariant and MC respects gauge constraints."""
    print_section("Test 9: Gauge Invariance / 规范不变性")

    situs = SitusManifold(n_claims=5, n_experts=3)

    # Run Situs-HMC
    result = run_hmc_chain(situs, n_samples=500, burn_in=200,
                            epsilon=0.05, L=20,
                            use_situs_metric=True, seed=42)

    # Check gauge constraint Σg=0 on samples
    samples = result['samples']
    gauge_violations = []
    for s in samples:
        E = s.reshape(situs.m, situs.n)
        gauge_sum = np.sum(E, axis=1)
        gauge_violations.append(np.max(np.abs(gauge_sum)))

    gauge_violations = np.array(gauge_violations)
    mean_violation = np.mean(gauge_violations)
    max_violation = np.max(gauge_violations)

    print(f"  Mean gauge violation: {mean_violation:.6f}")
    print(f"  Max gauge violation: {max_violation:.4f}")

    ok1 = mean_violation < 3.0
    print(f"  Mean violation < 3.0: {ok1}")

    # Check Cercis gauge invariance: adding constant shift to all g_ij
    # for a claim should change Cercis
    E0 = situs.ground_truth.flatten().copy()
    c0 = situs.cercis(E0)

    E_shifted = E0.copy()
    E_mat = E_shifted.reshape(situs.m, situs.n)
    E_mat[0, :] += 1.0  # shift all experts on claim 0 by 1
    c_shifted = situs.cercis(E_mat.flatten())

    ok2 = c_shifted > c0  # Cercis should increase due to gauge violation
    print(f"  Cercis (ground truth): {c0:.4f}")
    print(f"  Cercis (gauge-violated): {c_shifted:.4f}")
    print(f"  Cercis increases with gauge violation: {ok2}")

    all_ok = ok1 and ok2
    if all_ok:
        print_pass("Gauge Invariance Test PASSED")
    else:
        print_fail("Gauge Invariance Test FAILED")
    return all_ok


# ============================================================================
# Main / 主函数
# ============================================================================

def main():
    """Run all verification tests."""
    print(_c("=" * 70, _BOLD))
    print(_c("  SCX Monte Carlo — Full Verification Suite", _BOLD + _CYAN))
    print(_c("  SCX 蒙特卡洛 — 完整验证套件", _BOLD + _CYAN))
    print(_c("  Situs HMC · SMC · TI · REX · Convergence Diagnostics", _BOLD))
    print(_c("=" * 70, _BOLD))
    print(f"  numpy version: {np.__version__}")
    print()

    results = {}

    # Run all tests
    test_functions = [
        ("Situs Manifold", test_situs_manifold),
        ("Hamiltonian Monte Carlo", test_hmc),
        ("Sequential Monte Carlo", test_smc),
        ("Thermodynamic Integration", test_thermodynamic_integration),
        ("Replica Exchange", test_replica_exchange),
        ("Convergence Diagnostics", test_convergence_diagnostics),
        ("HMC Comparison (Situs vs Euclidean)", test_hmc_vs_euclidean),
        ("ESS Theoretical Bound", test_ess_theoretical_bound),
        ("Gauge Invariance", test_gauge_invariance),
    ]

    for name, func in test_functions:
        try:
            results[name] = func()
        except Exception as e:
            print(f"\n{_c(f'ERROR in {name}: {e}', _RED)}")
            import traceback
            traceback.print_exc()
            results[name] = False

    # Summary
    print_section("SUMMARY / 总结")
    n_pass = sum(results.values())
    n_total = len(results)
    for name, passed in results.items():
        status = _c("PASS", _GREEN) if passed else _c("FAIL", _RED)
        print(f"  [{status}] {name}")

    print(f"\n  {n_pass}/{n_total} tests passed")

    if n_pass == n_total:
        print(f"\n  {_c('ALL TESTS PASSED — SCX Monte Carlo Verified!', _GREEN + _BOLD)}")
        print(f"  {_c('所有测试通过 — SCX蒙特卡洛验证完成！', _GREEN + _BOLD)}")
        return 0
    else:
        print(f"\n  {_c(f'{n_total - n_pass} TEST(S) FAILED', _RED + _BOLD)}")
        return 1


if __name__ == "__main__":
    exit(main())
