# -*- coding: utf-8 -*-
"""Situs: Physics-Anchored Positional Encoding for State-Conditioned Expertise.

Implements the rigorous theory from:
  - paper/situs_theory/main.tex  (Theorem 1.2.1–1.4.1, Proposition 2.1, etc.)
  - theory/self_evolution/ppe_rigorous_derivation.md  (full derivations)

Core components
---------------
1.  SitusEncoder           — scalar sinusoidal encoding with optimal frequency
                              spectrum (Bochner + Laplace kernel -> quantile sampling).
2.  SitusEncoder3D         — 3D rotational encoding  R_x·R_y·R_z·e_0.
3.  compute_lipschitz_*    — exact Lipschitz constants  (Theorems 1.2.3, 1.3.1).
4.  compute_delta_s_situs  — δ_s^Situs  information-gain test  (Proposition 2.1).
5.  compute_epsilon_pe     — ε_PE  encoding-imperfection estimate  (Definition 3.1).

References
----------
- Vaswani et al. (2017)  "Attention Is All You Need"
- Bochner's theorem:  a continuous, translation-invariant kernel is positive-definite
  iff it is the Fourier transform of a non-negative finite Borel measure.
- Laplace (exponential) correlation kernel:  k(Δ) = exp(-|Δ| / ξ).
"""

from __future__ import annotations

import math
from typing import Optional, Tuple, Union

import numpy as np
from numpy.typing import ArrayLike, NDArray


# ============================================================================
# 1.  Helper: optimal wavelengths (Theorem 1.2.1)
# ============================================================================

def compute_optimal_wavelengths(d: int, xi: float) -> NDArray[np.float64]:
    """Compute the optimal wavelength spectrum for scalar sinusoidal encoding.

    **Theorem 1.2.1** (Bochner + Laplace kernel → quantile sampling)::

        λ_j = 2πξ · cot(π(2j+1) / (2d)),   j = 0, 1, …, d/2 - 1

    where
    - ξ is the physical correlation length (e.g., bond length ≈ 1.9 Å),
    - d is the encoding dimension (even).

    Derivation sketch
    -----------------
    1. Laplace kernel  k(Δ) = exp(-|Δ|/ξ)  has Fourier transform
       ĥ(ω) = 2ξ / (1 + ξ²ω²)  (Cauchy distribution).
    2. Spectral density  S(ω) = 2ξ / [π(1 + ξ²ω²)],  total mass = 1.
    3. CDF  Q(ω) = (2/π) arctan(ξω).
    4. Quantile sampling at  (2j+1)/d  →  ω_j = (1/ξ) tan(π(2j+1)/(2d)).
    5. Wavelength  λ_j = 2π / ω_j.

    Parameters
    ----------
    d : int
        Encoding dimension (must be even and ≥ 2).
    xi : float
        Physical correlation length (> 0).

    Returns
    -------
    lambdas : ndarray of shape (d//2,)
        Optimal wavelengths  λ_0 > λ_1 > … > λ_{d/2-1}.

    Raises
    ------
    ValueError
        If *d* is not a positive even integer or *xi* ≤ 0.
    """
    if d < 2 or d % 2 != 0:
        raise ValueError(f"d must be an even integer ≥ 2, got {d}")
    if xi <= 0:
        raise ValueError(f"xi must be > 0, got {xi}")

    n_pairs = d // 2
    j = np.arange(n_pairs, dtype=np.float64)
    # cot(θ) = 1 / tan(θ);  use  tan  directly then invert
    theta = math.pi * (2 * j + 1) / (2 * d)
    lambdas = 2.0 * math.pi * xi / np.tan(theta)  # = 2πξ·cot(θ)
    return lambdas


def compute_encoding_error_bound(d: int, xi: float, L: float) -> float:
    """Estimate the supremum approximation error of the normalised encoding kernel.

    **Theorem 1.2.2**::

        sup_{Δ∈[0,L]} | (2/d) K_PE(Δ) - k(Δ) | = O(1/d)

    This returns a heuristic estimate of the leading-order constant.

    Parameters
    ----------
    d : int
        Encoding dimension.
    xi : float
        Correlation length.
    L : float
        Domain length.

    Returns
    -------
    bound : float
        Estimated  O(1/d)  error bound.
    """
    # The leading constant is roughly  (L / ξ) · (1 / d).
    # For a Cauchy spectral density the Fourier-coefficient decay gives ~ 1/d.
    return (L / xi) / d


# ============================================================================
# 2.  Scalar Lipschitz constant (Theorem 1.2.3)
# ============================================================================

def compute_lipschitz_scalar(d: int, lambdas: NDArray[np.float64]) -> float:
    """Compute the exact Lipschitz constant for scalar sinusoidal encoding.

    **Theorem 1.2.3**::

                2√2 · π       ╲       1
        L_PE = ───────── ·   ╱  Σ  ──────
                  √d        ╱    j  λ_j²

    The constant is *tight*:  as  p, q → 0,  sin θ ≈ θ  and equality is approached.

    Parameters
    ----------
    d : int
        Encoding dimension.
    lambdas : ndarray of shape (d//2,)
        Wavelengths  λ_j  (see  :func:`compute_optimal_wavelengths`).

    Returns
    -------
    L : float
        Exact Lipschitz constant.
    """
    sum_inv_sq = float(np.sum(1.0 / (lambdas * lambdas)))
    return (2.0 * math.sqrt(2.0) * math.pi / math.sqrt(d)) * math.sqrt(sum_inv_sq)


def compute_lipschitz_scalar_asymptotic(d: int, xi: float) -> float:
    """Asymptotic Lipschitz constant for large *d* (Corollary 1.2.3).

        L_PE ∼ (1/ξ) · √(d/6)      as  d → ∞.

    Parameters
    ----------
    d : int
        Encoding dimension.
    xi : float
        Correlation length.

    Returns
    -------
    L_asym : float
        Asymptotic approximation of the Lipschitz constant.
    """
    return math.sqrt(d / 6.0) / xi


# ============================================================================
# 3.  SitusEncoder — scalar encoding (Definition 1.2.1)
# ============================================================================

class SitusEncoder:
    """Scalar sinusoidal position encoding with optimal frequency spectrum.

    Implements **Definition 1.2.1**::

        PE_scalar(p, 2j)   = √(2/d) · sin(2π p / λ_j)
        PE_scalar(p, 2j+1) = √(2/d) · cos(2π p / λ_j)

    where  λ_j  are the optimal wavelengths from **Theorem 1.2.1**.

    Properties
    ----------
    - ‖PE(p)‖ = 1  for every  p  (encoding lives on the unit sphere).
    - Translation-invariant inner product:
        ⟨PE(p), PE(q)⟩ = (2/d) Σ_j cos(2π(p−q) / λ_j).
    - Lipschitz continuous with exact constant  L_PE  (Theorem 1.2.3).

    Parameters
    ----------
    d : int
        Encoding dimension (even, ≥ 2).
    xi : float
        Physical correlation length  ξ > 0.
    L : float or None
        Physical domain length.  If given, the encoder validates the
        Nyquist coverage condition  λ_max ≥ 2L.

    Attributes
    ----------
    d : int
    xi : float
    lambdas_ : ndarray of shape (d//2,)
    lipschitz_ : float
        Exact Lipschitz constant  L_PE  (Theorem 1.2.3).
    omega_ : ndarray of shape (d//2,)
        Angular frequencies  ω_j = 2π / λ_j.

    Examples
    --------
    >>> enc = SitusEncoder(d=32, xi=1.9, L=50.0)
    >>> p = np.array([0.0, 2.5, 10.0])
    >>> z = enc.encode(p)
    >>> z.shape
    (3, 32)
    >>> np.allclose(np.linalg.norm(z, axis=1), 1.0)
    True
    """

    def __init__(self, d: int, xi: float, L: Optional[float] = None) -> None:
        if d < 2 or d % 2 != 0:
            raise ValueError(f"d must be an even integer ≥ 2, got {d}")
        if xi <= 0:
            raise ValueError(f"xi must be > 0, got {xi}")

        self.d = d
        self.xi = xi
        self._L = L

        # Optimal wavelengths  (Theorem 1.2.1)
        self.lambdas_ = compute_optimal_wavelengths(d, xi)
        self.omega_ = 2.0 * math.pi / self.lambdas_

        # Exact Lipschitz constant  (Theorem 1.2.3)
        self.lipschitz_ = compute_lipschitz_scalar(d, self.lambdas_)

        # Nyquist coverage check  (Corollary 1.2.1)
        self._lambda_max = float(self.lambdas_[0])
        self._d_min_est = None
        if L is not None:
            self._d_min_est = L / (2.0 * xi)
            if self._lambda_max < 2.0 * L:
                import warnings
                warnings.warn(
                    f"λ_max = {self._lambda_max:.2f} < 2L = {2*L:.2f}. "
                    f"Nyquist coverage may be insufficient. "
                    f"Consider d ≥ {int(math.ceil(L / (2*xi)))}.",
                    UserWarning, stacklevel=2,
                )

    def encode(self, p: ArrayLike) -> NDArray[np.float64]:
        """Encode scalar position(s).

        Parameters
        ----------
        p : array-like
            Scalar position(s).  Shape  ()  or  (n,).

        Returns
        -------
        z : ndarray of shape (…, d)
            Encoded vectors.  Each row satisfies  ‖z_i‖ = 1.
        """
        p_arr = np.asarray(p, dtype=np.float64)
        scalar_input = p_arr.ndim == 0
        p_arr = np.atleast_1d(p_arr)
        flat = p_arr.ravel()
        n = flat.size
        d = self.d

        z = np.empty((n, d), dtype=np.float64)
        norm = math.sqrt(2.0 / d)

        for j in range(d // 2):
            phase = self.omega_[j] * flat  # 2π p / λ_j
            z[:, 2 * j] = norm * np.sin(phase)
            z[:, 2 * j + 1] = norm * np.cos(phase)

        # Reshape to match input + encoding dimension, squeeze scalar back
        z = z.reshape(p_arr.shape + (d,))
        if scalar_input:
            z = z.squeeze(axis=0)
        return z

    def inner_product(self, p: ArrayLike, q: ArrayLike) -> NDArray[np.float64]:
        """Compute the translation-invariant inner product ⟨PE(p), PE(q)⟩.

        Because the encoding lives on the unit sphere, this is also the
        cosine similarity::

            ⟨PE(p), PE(q)⟩ = (2/d) Σ_{j=0}^{d/2-1} cos(2π(p−q) / λ_j).

        Parameters
        ----------
        p, q : array-like
            Position arrays of compatible shapes.

        Returns
        -------
        sim : ndarray
            Pairwise inner products  (broadcast-compatible).
        """
        p = np.asarray(p, dtype=np.float64)
        q = np.asarray(q, dtype=np.float64)
        delta = p - q
        delta_flat = np.atleast_1d(delta).ravel()
        n = delta_flat.size
        d = self.d

        sim_flat = np.zeros(n, dtype=np.float64)
        for j in range(d // 2):
            sim_flat += np.cos(self.omega_[j] * delta_flat)
        sim_flat *= 2.0 / d

        return sim_flat.reshape(np.broadcast_shapes(p.shape, q.shape))

    def kernel(self, delta: ArrayLike) -> NDArray[np.float64]:
        """Evaluate the normalised encoding kernel  (2/d)·K_PE(Δ).

        This approximates the target Laplace kernel  k(Δ) = exp(-|Δ|/ξ).

        Parameters
        ----------
        delta : array-like
            Pairwise distance(s).

        Returns
        -------
        k_hat : ndarray
            Kernel values.
        """
        delta_arr = np.asarray(delta, dtype=np.float64)
        scalar_input = delta_arr.ndim == 0
        delta_flat = np.atleast_1d(delta_arr).ravel()
        k_hat = np.zeros_like(delta_flat)
        for j in range(self.d // 2):
            k_hat += np.cos(self.omega_[j] * delta_flat)
        k_hat *= 2.0 / self.d
        if scalar_input:
            return float(k_hat[0])
        return k_hat

    def target_kernel(self, delta: ArrayLike) -> NDArray[np.float64]:
        """Evaluate the target Laplace kernel  k(Δ) = exp(-|Δ|/ξ).

        Parameters
        ----------
        delta : array-like
            Pairwise distance(s).

        Returns
        -------
        k : ndarray
            Exact Laplace kernel values.
        """
        delta = np.asarray(delta, dtype=np.float64)
        return np.exp(-np.abs(delta) / self.xi)

    @property
    def max_wavelength(self) -> float:
        """Maximum wavelength  λ_max = λ_0  (longest spatial correlation captured)."""
        return self._lambda_max

    @property
    def min_dimension_estimate(self) -> float:
        """Estimated minimum dimension for Nyquist coverage  d_min ≈ L/(2ξ)."""
        return self._d_min_est

    def __repr__(self) -> str:
        return (
            f"SitusEncoder(d={self.d}, ξ={self.xi:.4g}, "
            f"L_PE={self.lipschitz_:.4g}, λ_max={self._lambda_max:.4g})"
        )


# ============================================================================
# 4.  SitusEncoder3D — 3D rotational encoding (Definition 1.3.1)
# ============================================================================

class SitusEncoder3D:
    """3D rotational position encoding via  SO(d)  embedding.

    Implements **Definition 1.3.1**::

        PE_rot(p) = R_x(α x) · R_y(β y) · R_z(γ z) · e₀

    where
    -  p = (x, y, z) ∈ ℝ³  is the physical position,
    -  α, β, γ > 0  are frequency parameters  (rad / Å),
    -  R_a(θ)  rotates the plane  (2a, 2a+1)  by  θ,
    -  e₀ ∈ ℝᵈ  is the fixed reference unit vector.

    Properties
    ----------
    - Lie-group homomorphism  ℝ³ → SO(d)  (Proposition 1.3.1).
    - Translation-invariant:
        ⟨PE(p), PE(q)⟩ = cos(α Δx) + cos(β Δy) + cos(γ Δz).
    - Lipschitz constant  L_PE = max(α, β, γ)  (Theorem 1.3.1).

    Parameters
    ----------
    d : int
        Encoding dimension  (≥ 6, even).
    alpha : float
        x-axis frequency  (rad / length-unit).
    beta : float
        y-axis frequency  (rad / length-unit).
    gamma : float
        z-axis frequency  (rad / length-unit).

    Attributes
    ----------
    d : int
    alpha, beta, gamma : float
    lipschitz_ : float
        Exact Lipschitz constant  max(α, β, γ).

    Examples
    --------
    >>> enc = SitusEncoder3D(d=12, alpha=1.0, beta=1.0, gamma=1.5)
    >>> p = np.array([[0.0, 0.0, 0.0], [1.0, 0.5, 0.0]])
    >>> z = enc.encode(p)
    >>> z.shape
    (2, 12)
    >>> enc.lipschitz_
    1.5
    """

    def __init__(
        self, d: int, alpha: float, beta: float, gamma: float
    ) -> None:
        if d < 6 or d % 2 != 0:
            raise ValueError(f"d must be an even integer ≥ 6, got {d}")
        if alpha <= 0 or beta <= 0 or gamma <= 0:
            raise ValueError("Frequency parameters must be > 0")

        self.d = d
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        # Reference vector  e₀: 1 in the first dimension of each rotation plane
        self._e0 = np.zeros(d, dtype=np.float64)
        self._e0[0] = 1.0  # x-plane, first component
        self._e0[2] = 1.0  # y-plane, first component
        self._e0[4] = 1.0  # z-plane, first component

        # Exact Lipschitz constant  (Theorem 1.3.1)
        self.lipschitz_ = max(alpha, beta, gamma)

    def encode(self, positions: ArrayLike) -> NDArray[np.float64]:
        """Encode 3D position(s).

        Parameters
        ----------
        positions : array-like
            Shape  (3,)  or  (n, 3).  Columns:  x, y, z.

        Returns
        -------
        z : ndarray of shape (…, d)
            Rotated encoding vectors.
        """
        pos = np.atleast_2d(np.asarray(positions, dtype=np.float64))
        if pos.ndim != 2 or pos.shape[1] != 3:
            raise ValueError(f"positions must have shape (n, 3), got {pos.shape}")
        n = pos.shape[0]
        d = self.d

        # Broadcast  e₀  to all positions
        z = np.tile(self._e0[np.newaxis, :], (n, 1))  # (n, d)

        for i in range(n):
            x, y, z_coord = pos[i, 0], pos[i, 1], pos[i, 2]
            # Apply R_z(γ z) on dims (4, 5)
            self._rotate_plane(z[i], 4, self.gamma * z_coord)
            # Apply R_y(β y) on dims (2, 3)
            self._rotate_plane(z[i], 2, self.beta * y)
            # Apply R_x(α x) on dims (0, 1)
            self._rotate_plane(z[i], 0, self.alpha * x)

        return z.squeeze() if positions is not None and np.ndim(positions) == 1 else z

    @staticmethod
    def _rotate_plane(vec: NDArray[np.float64], start: int, theta: float) -> None:
        """In-place 2D rotation on dimension pair (start, start+1)."""
        c = math.cos(theta)
        s = math.sin(theta)
        a = vec[start]
        b = vec[start + 1]
        vec[start] = c * a - s * b
        vec[start + 1] = s * a + c * b

    def inner_product(
        self, p: ArrayLike, q: ArrayLike
    ) -> NDArray[np.float64]:
        """Compute  ⟨PE(p), PE(q)⟩ = cos(αΔx) + cos(βΔy) + cos(γΔz).

        Parameters
        ----------
        p, q : array-like of shape (3,) or (n, 3)
            Position arrays.

        Returns
        -------
        sim : ndarray
            Inner products.
        """
        p = np.atleast_2d(np.asarray(p, dtype=np.float64))
        q = np.atleast_2d(np.asarray(q, dtype=np.float64))
        delta = p - q  # (n, 3)
        return (
            np.cos(self.alpha * delta[:, 0])
            + np.cos(self.beta * delta[:, 1])
            + np.cos(self.gamma * delta[:, 2])
        )

    def __repr__(self) -> str:
        return (
            f"SitusEncoder3D(d={self.d}, α={self.alpha:.4g}, "
            f"β={self.beta:.4g}, γ={self.gamma:.4g}, "
            f"L_PE={self.lipschitz_:.4g})"
        )


# ============================================================================
# 5.  δ_s^Situs  information-gain test (Proposition 2.1)
# ============================================================================

def compute_delta_s_situs(
    p_noisy_situs: Union[float, NDArray[np.float64]],
    p_noisy: Union[float, NDArray[np.float64]],
    p_clean_situs: Union[float, NDArray[np.float64]],
    p_clean: Union[float, NDArray[np.float64]],
) -> Tuple[Union[float, NDArray[np.float64]], Union[float, NDArray[np.float64]]]:
    """Compute the Situs-augmented detection margin and gain.

    **Proposition 2.1** (corrected sign)::

        Δ_s^Situs = Δ_s + δ_s^PE

        δ_s^PE = (p_noisy^Situs - p_noisy) - (p_clean^Situs - p_clean)

    where
    -  Δ_s = p_noisy - p_clean  is the baseline detection margin,
    -  δ_s^PE > 0  means Situs encoding *helps* distinguish noisy from clean.

    The value range of δ_s^PE is  [−Δ_s, 1 − p_clean].

    Parameters
    ----------
    p_noisy_situs : float or ndarray
        Disagreement probability for noisy samples **with** Situs encoding.
    p_noisy : float or ndarray
        Disagreement probability for noisy samples **without** encoding.
    p_clean_situs : float or ndarray
        Disagreement probability for clean samples **with** Situs encoding.
    p_clean : float or ndarray
        Disagreement probability for clean samples **without** encoding.

    Returns
    -------
    delta_situs : float or ndarray
        Augmented detection margin  Δ_s^Situs.
    delta_gain : float or ndarray
        Situs information gain  δ_s^PE.

    Notes
    -----
    The **sufficient condition** for  δ_s^PE > 0  is  I(Y; P | S) > 0
    (Theorem 2.2.1) — the physical position carries label information
    beyond what the state atom already provides.
    """
    delta_base = p_noisy - p_clean
    delta_gain = (p_noisy_situs - p_noisy) - (p_clean_situs - p_clean)
    return delta_base + delta_gain, delta_gain


def compute_delta_s_upper_bound(
    p_clean: Union[float, NDArray[np.float64]],
    kl_noisy: Union[float, NDArray[np.float64]],
    kl_clean: Union[float, NDArray[np.float64]],
) -> Union[float, NDArray[np.float64]]:
    """Upper bound on δ_s^PE via DPI + Pinsker (Theorem 2.3.1).

        δ_s^PE ≤ min(1 − p_clean,  √(½ KL_noisy) + √(½ KL_clean))

    The two terms in the min are **independently valid** bounds:
    - The first comes from the value-range constraint  (δ_s^PE ≤ 1 − p_clean).
    - The second comes from Pinsker's inequality applied to the KL divergences
      of the conditional distributions with and without positional information.

    Parameters
    ----------
    p_clean : float or ndarray
        Baseline clean disagreement probability.
    kl_noisy : float or ndarray
        KL divergence  D_KL(P_{PE|S, noisy} ‖ P_{PE|S}).
    kl_clean : float or ndarray
        KL divergence  D_KL(P_{PE|S, clean} ‖ P_{PE|S}).

    Returns
    -------
    bound : float or ndarray
        Upper bound on  δ_s^PE.
    """
    pinsker_bound = np.sqrt(0.5 * kl_noisy) + np.sqrt(0.5 * kl_clean)
    value_range_bound = 1.0 - p_clean
    return np.minimum(value_range_bound, pinsker_bound)


# ============================================================================
# 6.  ε_PE  encoding-imperfection estimate (Definition 3.1)
# ============================================================================

def compute_epsilon_pe(
    mi_full: Union[float, NDArray[np.float64]],
    mi_encoded: Union[float, NDArray[np.float64]],
) -> Union[float, NDArray[np.float64]]:
    """Compute the encoding imperfection  ε_PE.

    **Definition 3.1**::

        ε_PE = I(Y; P | X) − I(Y; PE(P) | X)

    Properties
    ----------
    - ε_PE ≥ 0  (data-processing inequality).
    - ε_PE = 0  iff  PE(P)  is a sufficient statistic for  P  w.r.t. Y.
    - ε_PE ≤ I(Y; P | X) ≤ H(Y).

    Parameters
    ----------
    mi_full : float or ndarray
        Conditional mutual information  I(Y; P | X)  using the full position.
    mi_encoded : float or ndarray
        Conditional mutual information  I(Y; PE(P) | X)  using the encoded position.

    Returns
    -------
    epsilon : float or ndarray
        Encoding imperfection.  Smaller is better.
    """
    return mi_full - mi_encoded


def compute_epsilon_pe_from_logloss(
    logloss_enc: Union[float, NDArray[np.float64]],
    logloss_full: Union[float, NDArray[np.float64]],
) -> Union[float, NDArray[np.float64]]:
    """Estimate  ε_PE  from predictive log-loss difference (Proposition 3.3.1).

        ε̂_PE^pred = (1/n) Σ_i [log 1/p_enc(y_i|x_i,PE(p_i)) − log 1/p_full(y_i|x_i,p_i)]

    When both classifiers are consistent,  ε̂_PE^pred → ε_PE.

    This is often more practical than KSG-based MI estimation for high-dim  X.

    Parameters
    ----------
    logloss_enc : float or ndarray
        Mean log-loss of the classifier using encoded positions.
    logloss_full : float or ndarray
        Mean log-loss of the classifier using full (raw) positions.

    Returns
    -------
    epsilon_hat : float or ndarray
        Estimated encoding imperfection.
    """
    return logloss_enc - logloss_full


# ============================================================================
# 7.  Utility: Chernoff-Hoeffding F₁ bound (Theorem 1, Situs-augmented)
# ============================================================================

def compute_f1_lower_bound(
    eta: float,
    rho_s: NDArray[np.float64],
    M: int,
    delta_s: NDArray[np.float64],
    delta_gain: NDArray[np.float64],
) -> float:
    """Compute the Situs-augmented  F₁  lower bound.

    **Corrected Theorem 1** (Situs-enhanced)::

        F₁^Situs ≥ 1 − (1/η) Σ_s ρ_s · exp(−2M (Δ_s + δ_s^PE)²)

    Parameters
    ----------
    eta : float
        Proportion of clean samples in the dataset.
    rho_s : ndarray
        Proportion of each state  s  in the dataset  (Σ ρ_s = 1).
    M : int
        Number of independent expert models.
    delta_s : ndarray
        Baseline detection margins  Δ_s = p_noisy_s − p_clean_s.
    delta_gain : ndarray
        Situs information gains  δ_s^PE  (from  :func:`compute_delta_s_situs`).

    Returns
    -------
    f1_bound : float
        Lower bound on  F₁  score.
    """
    margin = delta_s + delta_gain  # Δ_s^Situs
    error = np.sum(rho_s * np.exp(-2.0 * M * margin * margin))
    return float(1.0 - error / eta)


# ============================================================================
# 8.  Spring/Yajie-compatible gatekeeper scoring stub
# ============================================================================

def compute_yajie_score(
    expert_votes: NDArray[np.float64],
    eta_t: float = 0.0,
) -> NDArray[np.float64]:
    """Compute the Yajie noise score from multi-expert votes.

        S(s) = Q(s) + η(t) · N(s)

    where  Q(s) = 1 − (1/M) Σ_m v_m(s)  (fraction of agreeing experts)
    and  η(t)  is a time-decaying exploration weight.

    This is a stub that computes the base quality score  Q(s).

    Parameters
    ----------
    expert_votes : ndarray of shape (n_samples, M)
        Expert votes  v_m ∈ {0, 1}.  1 = disagreement, 0 = agreement.
    eta_t : float
        Exploration weight  η(t)  (≥ 0).  The novelty bonus  N(s)  is not yet
        implemented; set  η(t) = 0  to use pure quality scoring.

    Returns
    -------
    scores : ndarray of shape (n_samples,)
        Yajie scores  ∈ [0, 1].  Higher → more likely to be noisy.
    """
    n_samples, M = expert_votes.shape
    # Q(s): fraction of experts that disagree (i.e., v_m = 1)
    Q = np.mean(expert_votes, axis=1)  # ∈ [0, 1]
    # Novelty bonus  N(s)  placeholder — requires Spring memory bank M_t
    N = np.zeros(n_samples, dtype=np.float64)
    return Q + eta_t * N


# ============================================================================
# 9.  Module-level convenience
# ============================================================================

__all__ = [
    "SitusEncoder",
    "SitusEncoder3D",
    "compute_optimal_wavelengths",
    "compute_encoding_error_bound",
    "compute_lipschitz_scalar",
    "compute_lipschitz_scalar_asymptotic",
    "compute_delta_s_situs",
    "compute_delta_s_upper_bound",
    "compute_epsilon_pe",
    "compute_epsilon_pe_from_logloss",
    "compute_f1_lower_bound",
    "compute_yajie_score",
]
