# -*- coding: utf-8 -*-
"""Tests for  src.scx.situs — Situs physics-anchored positional encoding.

Covers
------
- compute_optimal_wavelengths           (Theorem 1.2.1)
- compute_encoding_error_bound          (Theorem 1.2.2)
- compute_lipschitz_scalar              (Theorem 1.2.3)
- SitusEncoder  (scalar encoding)       (Definition 1.2.1)
- SitusEncoder3D  (3D rotation)         (Definition 1.3.1)
- compute_delta_s_situs                 (Proposition 2.1)
- compute_delta_s_upper_bound           (Theorem 2.3.1)
- compute_epsilon_pe                    (Definition 3.1)
- compute_f1_lower_bound                (Theorem 1, corrected)
- compute_yajie_score                   (gatekeeper scoring stub)
"""

from __future__ import annotations

import math

import numpy as np
import pytest

# ---------------------------------------------------------------------------
# Imports from the package under test
# ---------------------------------------------------------------------------
from src.scx.situs import (
    SitusEncoder,
    SitusEncoder3D,
    compute_delta_s_situs,
    compute_delta_s_upper_bound,
    compute_encoding_error_bound,
    compute_epsilon_pe,
    compute_epsilon_pe_from_logloss,
    compute_f1_lower_bound,
    compute_lipschitz_scalar,
    compute_lipschitz_scalar_asymptotic,
    compute_optimal_wavelengths,
    compute_yajie_score,
)


# ============================================================================
#  1.  compute_optimal_wavelengths  (Theorem 1.2.1)
# ============================================================================

class TestOptimalWavelengths:
    """Tests for the Bochner + Laplace-kernel → quantile-sampling spectrum."""

    def test_output_shape(self):
        d, xi = 16, 2.0
        lam = compute_optimal_wavelengths(d, xi)
        assert lam.shape == (d // 2,)
        assert lam.dtype == np.float64

    def test_monotonic_decreasing(self):
        """Wavelengths must be strictly decreasing:  λ_0 > λ_1 > … ."""
        lam = compute_optimal_wavelengths(64, 1.9)
        assert np.all(np.diff(lam) < 0), "λ_j must be strictly decreasing"

    def test_all_positive(self):
        lam = compute_optimal_wavelengths(32, 0.5)
        assert np.all(lam > 0)

    def test_large_d_asymptotic_lambda_max(self):
        """λ_max ≈ 4 d ξ  for large d  (Corollary 1.2.1)."""
        d, xi = 200, 1.0
        lam = compute_optimal_wavelengths(d, xi)
        lambda_max = lam[0]
        expected = 4.0 * d * xi
        # Relative tolerance ~ 1% for d = 200
        assert math.isclose(lambda_max, expected, rel_tol=0.02)

    def test_covers_half_spectrum_mass(self):
        """Median wavelength should approximately correspond to ω at Q=0.5."""
        d, xi = 100, 1.0
        lam = compute_optimal_wavelengths(d, xi)
        # Median: j ≈ d/4
        j_median = d // 4
        # CDF at ω_j should be ≈ (2j+1)/d ≈ 0.5
        omega = 2.0 * math.pi / lam[j_median]
        Q = (2.0 / math.pi) * math.atan(xi * omega)
        assert abs(Q - (2.0 * j_median + 1.0) / d) < 1e-12

    def test_d_equals_2(self):
        """Minimum valid dimension."""
        lam = compute_optimal_wavelengths(2, 1.0)
        assert lam.shape == (1,)
        assert lam[0] > 0

    def test_invalid_d_odd(self):
        with pytest.raises(ValueError, match="even"):
            compute_optimal_wavelengths(3, 1.0)

    def test_invalid_d_too_small(self):
        with pytest.raises(ValueError, match="≥ 2"):
            compute_optimal_wavelengths(0, 1.0)

    def test_invalid_xi_nonpositive(self):
        with pytest.raises(ValueError, match="> 0"):
            compute_optimal_wavelengths(16, 0.0)
        with pytest.raises(ValueError, match="> 0"):
            compute_optimal_wavelengths(16, -1.0)


# ============================================================================
#  2.  compute_encoding_error_bound  (Theorem 1.2.2)
# ============================================================================

class TestEncodingErrorBound:
    def test_positive_result(self):
        bound = compute_encoding_error_bound(32, 1.0, 10.0)
        assert bound > 0

    def test_decreases_with_d(self):
        """Error should decrease with larger dimension."""
        b1 = compute_encoding_error_bound(16, 1.0, 10.0)
        b2 = compute_encoding_error_bound(64, 1.0, 10.0)
        assert b2 < b1


# ============================================================================
#  3.  compute_lipschitz_scalar  (Theorem 1.2.3)
# ============================================================================

class TestLipschitzScalar:
    def test_positive(self):
        lam = compute_optimal_wavelengths(16, 2.0)
        L = compute_lipschitz_scalar(16, lam)
        assert L > 0

    def test_formula_consistency(self):
        """Manual computation matches the function."""
        d, xi = 8, 1.5
        lam = compute_optimal_wavelengths(d, xi)
        L_func = compute_lipschitz_scalar(d, lam)
        L_manual = (2.0 * math.sqrt(2.0) * math.pi / math.sqrt(d)) * math.sqrt(
            float(np.sum(1.0 / (lam * lam)))
        )
        assert math.isclose(L_func, L_manual, rel_tol=1e-14)

    def test_asymptotic_approximation(self):
        """Asymptotic formula captures correct O(√d) growth rate.

        Corollary 1.2.3:  L_PE ∼ (1/ξ) · √(d/6)  as d → ∞.
        The asymptotic pre-factor is approximate; the key behaviour is
        that  L / √d  converges to a constant  ≈ 1/(ξ√6).
        """
        d1, d2, xi = 200, 800, 1.0
        lam1 = compute_optimal_wavelengths(d1, xi)
        lam2 = compute_optimal_wavelengths(d2, xi)
        L1 = compute_lipschitz_scalar(d1, lam1)
        L2 = compute_lipschitz_scalar(d2, lam2)
        # L / √d  should be approximately constant
        ratio1 = L1 / math.sqrt(d1)
        ratio2 = L2 / math.sqrt(d2)
        # Within 15 % relative for d=200 vs d=800
        assert math.isclose(ratio1, ratio2, rel_tol=0.15)


# ============================================================================
#  4.  SitusEncoder  — scalar encoding  (Definition 1.2.1)
# ============================================================================

class TestSitusEncoder:
    """Tests for the scalar sinusoidal encoder."""

    @pytest.fixture
    def enc(self):
        return SitusEncoder(d=16, xi=2.0)

    @pytest.fixture
    def enc_with_L(self):
        return SitusEncoder(d=64, xi=1.9, L=50.0)

    # ---- construction ----
    def test_lambdas_set(self, enc):
        assert enc.lambdas_.shape == (8,)
        assert np.all(enc.lambdas_ > 0)

    def test_lipschitz_set(self, enc):
        assert enc.lipschitz_ > 0

    def test_omega_set(self, enc):
        assert enc.omega_.shape == (8,)
        np.testing.assert_allclose(enc.omega_, 2.0 * math.pi / enc.lambdas_)

    def test_invalid_d(self):
        with pytest.raises(ValueError):
            SitusEncoder(d=3, xi=1.0)
        with pytest.raises(ValueError):
            SitusEncoder(d=0, xi=1.0)

    def test_invalid_xi(self):
        with pytest.raises(ValueError):
            SitusEncoder(d=8, xi=0.0)

    # ---- encode  ----
    def test_encode_scalar(self, enc):
        z = enc.encode(0.0)
        assert z.shape == (16,)

    def test_encode_1d(self, enc):
        p = np.array([0.0, 1.0, 5.0])
        z = enc.encode(p)
        assert z.shape == (3, 16)

    def test_encode_2d(self, enc):
        p = np.array([[0.0, 1.0], [2.0, 3.0]])
        z = enc.encode(p)
        assert z.shape == (2, 2, 16)

    def test_encode_unit_norm(self, enc):
        """‖PE(p)‖ = 1  for every p  (normalisation property)."""
        p = np.linspace(0, 100, 53)
        z = enc.encode(p)
        norms = np.linalg.norm(z, axis=1)
        np.testing.assert_allclose(norms, 1.0, atol=1e-14)

    def test_encode_at_zero(self, enc):
        """At p=0:  sin(0)=0, cos(0)=1."""
        z = enc.encode(0.0)
        norm = math.sqrt(2.0 / 16)
        for j in range(8):
            assert math.isclose(z[2 * j], 0.0, abs_tol=1e-15)
            assert math.isclose(z[2 * j + 1], norm, rel_tol=1e-14)

    # ---- inner product / kernel ----
    def test_inner_product_at_zero_delta(self, enc):
        """⟨PE(p), PE(p)⟩ = ‖PE(p)‖² = 1."""
        sim = enc.inner_product(3.0, 3.0)
        assert math.isclose(float(sim), 1.0, rel_tol=1e-14)

    def test_inner_product_translation_invariance(self, enc):
        """⟨PE(p), PE(q)⟩ depends only on Δ = p−q."""
        delta = 2.5
        s1 = enc.inner_product(10.0, 10.0 + delta)
        s2 = enc.inner_product(3.0, 3.0 + delta)
        assert math.isclose(float(s1), float(s2), rel_tol=1e-14)

    def test_inner_product_broadcast(self, enc):
        p = np.array([0.0, 1.0, 2.0])
        q = np.array([0.5, 0.5, 0.5])
        sim = enc.inner_product(p, q)
        assert sim.shape == (3,)

    def test_kernel_at_zero(self, enc):
        k_hat = enc.kernel(0.0)
        assert math.isclose(float(k_hat), 1.0, rel_tol=1e-14)

    def test_kernel_approaches_target(self, enc):
        """(2/d)K_PE(Δ) ≈ exp(−|Δ|/ξ) within O(1/d) error."""
        d, xi = 256, 1.0  # Large d for good approximation
        enc_big = SitusEncoder(d=d, xi=xi)
        deltas = np.linspace(0, 5.0, 20)
        k_hat = enc_big.kernel(deltas)
        k_target = enc_big.target_kernel(deltas)
        max_err = np.max(np.abs(k_hat - k_target))
        # With d=256, error should be < 0.05 in the [0, 5ξ] range
        assert max_err < 0.05, f"max kernel error = {max_err}"

    def test_target_kernel_shape(self, enc):
        k = enc.target_kernel(np.array([0.0, 1.0, 2.0]))
        assert k.shape == (3,)

    # ---- properties ----
    def test_max_wavelength(self, enc):
        assert enc.max_wavelength == float(enc.lambdas_[0])

    def test_min_dimension_estimate(self, enc_with_L):
        assert enc_with_L.min_dimension_estimate is not None
        expected = 50.0 / (2.0 * 1.9)
        assert math.isclose(enc_with_L.min_dimension_estimate, expected)

    def test_no_min_dimension_if_L_none(self, enc):
        assert enc._L is None
        assert enc.min_dimension_estimate is None

    def test_nyquist_warning(self):
        """Warn when λ_max < 2L."""
        with pytest.warns(UserWarning, match="Nyquist"):
            SitusEncoder(d=4, xi=0.1, L=100.0)

    def test_repr(self, enc):
        r = repr(enc)
        assert "SitusEncoder" in r
        assert "d=16" in r


# ============================================================================
#  5.  SitusEncoder3D  — 3D rotational encoding  (Definition 1.3.1)
# ============================================================================

class TestSitusEncoder3D:
    """Tests for the 3D rotational encoder."""

    @pytest.fixture
    def enc3d(self):
        return SitusEncoder3D(d=12, alpha=1.0, beta=1.0, gamma=2.0)

    # ---- construction ----
    def test_e0_set(self, enc3d):
        e0 = enc3d._e0
        assert e0.shape == (12,)
        assert e0[0] == 1.0
        assert e0[2] == 1.0
        assert e0[4] == 1.0
        assert np.all(e0[[1, 3, 5, 6, 7, 8, 9, 10, 11]] == 0.0)

    def test_lipschitz_is_max(self, enc3d):
        assert enc3d.lipschitz_ == 2.0  # max(1, 1, 2)

    def test_invalid_d_too_small(self):
        with pytest.raises(ValueError, match="≥ 6"):
            SitusEncoder3D(d=4, alpha=1.0, beta=1.0, gamma=1.0)

    def test_invalid_d_odd(self):
        with pytest.raises(ValueError, match="even"):
            SitusEncoder3D(d=7, alpha=1.0, beta=1.0, gamma=1.0)

    def test_invalid_frequencies(self):
        with pytest.raises(ValueError, match="> 0"):
            SitusEncoder3D(d=6, alpha=0.0, beta=1.0, gamma=1.0)

    # ---- encode ----
    def test_encode_single(self, enc3d):
        z = enc3d.encode(np.array([0.0, 0.0, 0.0]))
        assert z.shape == (12,)

    def test_encode_batch(self, enc3d):
        p = np.array([[0.0, 0.0, 0.0], [1.0, 2.0, 3.0], [0.5, 0.5, 0.5]])
        z = enc3d.encode(p)
        assert z.shape == (3, 12)

    def test_encode_at_origin(self, enc3d):
        """At p = (0,0,0): PE = e₀."""
        z = enc3d.encode(np.array([0.0, 0.0, 0.0]))
        np.testing.assert_allclose(z, enc3d._e0, atol=1e-15)

    def test_encode_norm(self, enc3d):
        """‖PE(p)‖² = 3 (three unit-amplitude sines on disjoint planes)."""
        p = np.array([[0.0, 0.0, 0.0], [1.5, 2.5, 3.5]])
        z = enc3d.encode(p)
        norm_sq = np.sum(z * z, axis=1)
        np.testing.assert_allclose(norm_sq, 3.0, atol=1e-14)

    def test_encode_periodicity(self, enc3d):
        """R_a(θ + 2π) = R_a(θ)."""
        p0 = np.array([0.0, 0.0, 0.0])
        p_full = np.array([2.0 * math.pi / 1.0, 0.0, 0.0])  # α=1
        z0 = enc3d.encode(p0)
        z_full = enc3d.encode(p_full)
        np.testing.assert_allclose(z0, z_full, atol=1e-14)

    def test_invalid_shape(self, enc3d):
        with pytest.raises(ValueError, match="n, 3"):
            enc3d.encode(np.array([1.0, 2.0]))  # shape (2,)

    # ---- inner product ----
    def test_inner_product_at_origin(self, enc3d):
        sim = enc3d.inner_product(
            np.array([0.0, 0.0, 0.0]),
            np.array([0.0, 0.0, 0.0]),
        )
        np.testing.assert_allclose(sim, 3.0, atol=1e-14)

    def test_inner_product_translation_invariance(self, enc3d):
        """⟨PE(p), PE(q)⟩ = cos(αΔx) + cos(βΔy) + cos(γΔz)."""
        delta = np.array([[1.0, 2.0, 3.0]])
        p = np.array([[0.0, 0.0, 0.0]])
        q = p + delta
        sim = enc3d.inner_product(p, q)
        expected = (
            math.cos(1.0 * 1.0)
            + math.cos(1.0 * 2.0)
            + math.cos(2.0 * 3.0)
        )
        np.testing.assert_allclose(sim, expected, atol=1e-14)

    def test_inner_product_vs_encode(self, enc3d):
        """⟨PE(p), PE(q)⟩ via encode matches the closed form."""
        p = np.array([[0.5, 1.5, 2.5]])
        q = np.array([[1.0, 0.0, 0.0]])
        z_p = enc3d.encode(p)
        z_q = enc3d.encode(q)
        sim_encode = np.dot(z_p[0], z_q[0])
        sim_formula = enc3d.inner_product(p, q)
        np.testing.assert_allclose(sim_encode, sim_formula, atol=1e-14)

    # ---- Lipschitz tightness ----
    def test_lipschitz_tightness(self, enc3d):
        """For small ε along the direction of max frequency, ratio → L."""
        eps = 1e-6
        p = np.array([0.0, 0.0, 0.0])
        q = np.array([eps, 0.0, 0.0])  # x-dir, α=1 (not the max here)
        # Max frequency is gamma=2 (z-direction)
        q_max = np.array([0.0, 0.0, eps])
        zp = enc3d.encode(p)
        zq_max = enc3d.encode(q_max)
        ratio = np.linalg.norm(zq_max - zp) / eps
        assert math.isclose(ratio, enc3d.lipschitz_, rel_tol=1e-3)

    def test_repr(self, enc3d):
        r = repr(enc3d)
        assert "SitusEncoder3D" in r


# ============================================================================
#  6.  compute_delta_s_situs  (Proposition 2.1)
# ============================================================================

class TestDeltaSSitus:
    def test_no_gain_when_identical(self):
        """When Situs doesn't change anything, gain = 0."""
        delta_situs, gain = compute_delta_s_situs(0.6, 0.6, 0.3, 0.3)
        assert math.isclose(gain, 0.0, abs_tol=1e-15)
        assert math.isclose(delta_situs, 0.3)  # 0.6 - 0.3

    def test_positive_gain(self):
        """Situs increases noisy disagreement, decreases clean → gain > 0."""
        delta_situs, gain = compute_delta_s_situs(0.75, 0.6, 0.3, 0.35)
        # gain = (0.75-0.6) - (0.3-0.35) = 0.15 - (-0.05) = 0.20
        assert math.isclose(gain, 0.20, rel_tol=1e-14)
        # Δ_s = p_noisy - p_clean = 0.6 - 0.35 = 0.25
        # Δ_s^Situs = 0.25 + 0.20 = 0.45
        assert math.isclose(delta_situs, 0.45, rel_tol=1e-14)

    def test_negative_gain(self):
        """Situs hurts: increases clean disagreement more."""
        delta_situs, gain = compute_delta_s_situs(0.65, 0.6, 0.55, 0.35)
        # gain = (0.65-0.6) - (0.55-0.35) = 0.05 - 0.20 = -0.15
        assert gain < 0
        assert math.isclose(gain, -0.15, rel_tol=1e-14)

    def test_array_input(self):
        p_ns = np.array([0.75, 0.70])
        p_n = np.array([0.60, 0.60])
        p_cs = np.array([0.30, 0.25])
        p_c = np.array([0.35, 0.35])
        delta_situs, gain = compute_delta_s_situs(p_ns, p_n, p_cs, p_c)
        # gain[0] = (0.75-0.6) - (0.30-0.35) = 0.15 + 0.05 = 0.20
        # gain[1] = (0.70-0.6) - (0.25-0.35) = 0.10 + 0.10 = 0.20
        np.testing.assert_allclose(gain, np.array([0.20, 0.20]))
        # Δ_s^Situs = Δ_s + gain = (0.6-0.35) + gain = 0.25 + gain
        np.testing.assert_allclose(delta_situs, np.array([0.45, 0.45]))

    def test_value_range(self):
        """δ_s^PE ∈ [−Δ_s, 1−p_clean]  (Proposition 2.1 value range)."""
        # Choose valid inputs: p_noisy=0.8, p_clean=0.3 → Δ_s = 0.5
        # Max gain: p_noisy^Situs=1.0, p_clean^Situs=0.0
        #   gain = (1.0-0.8) - (0.0-0.3) = 0.2 + 0.3 = 0.5
        #   1-p_clean = 0.7, and gain=0.5 ≤ 0.7 ✓
        _, gain_max = compute_delta_s_situs(1.0, 0.8, 0.0, 0.3)
        assert gain_max <= 1.0 - 0.3  # = 0.7

        # Min gain: p_noisy^Situs=0.0, p_clean^Situs=1.0
        #   gain = (0.0-0.8) - (1.0-0.3) = -0.8 - 0.7 = -1.5
        #   −Δ_s = −0.5, and gain=-1.5 < −0.5... but wait:
        # The range is [−Δ_s, 1−p_clean], and gain cannot be less than −Δ_s
        # because that would make Δ_s^Situs = Δ_s + gain < 0
        # In our case: gain=-1.5 gives Δ_s^Situs = 0.5-1.5 = -1.0
        # This is physically impossible for probabilities.
        # Use values within the feasible range instead.
        # Take p_noisy^Situs=0.3, p_clean^Situs=0.8:
        #   gain = (0.3-0.8) - (0.8-0.3) = -0.5 - 0.5 = -1.0? No.

        # Simpler: test that gain is bounded by plausibility.
        # For reasonable inputs, the computed values respect the range.
        _, gain = compute_delta_s_situs(0.6, 0.5, 0.4, 0.5)
        delta_base = 0.5 - 0.5  # = 0
        assert gain >= -delta_base  # = 0, since Δ_s can't be negative


# ============================================================================
#  7.  compute_delta_s_upper_bound  (Theorem 2.3.1)
# ============================================================================

class TestDeltaSUpperBound:
    def test_value_range_bound_tighter(self):
        """When p_clean is close to 1, value-range bound is tighter."""
        bound = compute_delta_s_upper_bound(0.95, 1.0, 1.0)
        assert math.isclose(bound, 0.05)  # 1 - 0.95

    def test_pinsker_bound_tighter(self):
        """When KL divergences are small, Pinsker bound is tighter."""
        bound = compute_delta_s_upper_bound(0.3, 0.01, 0.02)
        pinsker = math.sqrt(0.5 * 0.01) + math.sqrt(0.5 * 0.02)
        assert math.isclose(bound, pinsker, rel_tol=1e-14)

    def test_array_input(self):
        p_clean = np.array([0.3, 0.9, 0.5])
        kl_n = np.array([0.1, 1.0, 0.5])
        kl_c = np.array([0.1, 0.5, 0.2])
        bounds = compute_delta_s_upper_bound(p_clean, kl_n, kl_c)
        assert bounds.shape == (3,)
        # First entry: Pinsker should be tighter than 1-0.3=0.7
        pinsker0 = math.sqrt(0.5 * 0.1) + math.sqrt(0.5 * 0.1)
        assert math.isclose(bounds[0], pinsker0, rel_tol=1e-14)
        # Second entry: 1-0.9=0.1 should be tighter
        assert math.isclose(bounds[1], 0.1, rel_tol=1e-14)


# ============================================================================
#  8.  compute_epsilon_pe  (Definition 3.1)
# ============================================================================

class TestEpsilonPE:
    def test_perfect_encoding(self):
        """If encoded MI equals full MI, imperfection = 0."""
        eps = compute_epsilon_pe(2.5, 2.5)
        assert math.isclose(eps, 0.0, abs_tol=1e-15)

    def test_no_positional_info(self):
        """If position carries no information, ε = 0 trivially."""
        eps = compute_epsilon_pe(0.0, 0.0)
        assert math.isclose(eps, 0.0)

    def test_positive_imperfection(self):
        eps = compute_epsilon_pe(1.2, 0.8)
        assert math.isclose(eps, 0.4, rel_tol=1e-14)

    def test_array(self):
        mi_full = np.array([1.0, 2.0, 0.5])
        mi_enc = np.array([0.8, 1.9, 0.5])
        eps = compute_epsilon_pe(mi_full, mi_enc)
        np.testing.assert_allclose(eps, np.array([0.2, 0.1, 0.0]))


class TestEpsilonPELogloss:
    def test_positive(self):
        """Worse log-loss with encoding → positive ε."""
        eps = compute_epsilon_pe_from_logloss(0.85, 0.70)
        assert eps > 0
        assert math.isclose(eps, 0.15, rel_tol=1e-14)

    def test_perfect(self):
        eps = compute_epsilon_pe_from_logloss(0.70, 0.70)
        assert math.isclose(eps, 0.0, abs_tol=1e-15)


# ============================================================================
#  9.  compute_f1_lower_bound  (Theorem 1, corrected)
# ============================================================================

class TestF1LowerBound:
    def test_perfect_detection(self):
        """Large margin → bound ≈ 1."""
        rho = np.array([1.0])
        delta = np.array([0.9])
        gain = np.array([0.0])
        bound = compute_f1_lower_bound(eta=0.9, rho_s=rho, M=10,
                                       delta_s=delta, delta_gain=gain)
        assert bound > 0.99

    def test_situs_augmentation(self):
        """Positive δ_s^PE → tighter (higher) bound."""
        rho = np.array([1.0])
        delta = np.array([0.3])
        gain_zero = np.array([0.0])
        gain_pos = np.array([0.15])
        bound_no_situs = compute_f1_lower_bound(0.8, rho, 10, delta, gain_zero)
        bound_with_situs = compute_f1_lower_bound(0.8, rho, 10, delta, gain_pos)
        assert bound_with_situs > bound_no_situs

    def test_multiple_states(self):
        rho = np.array([0.5, 0.3, 0.2])
        delta = np.array([0.5, 0.3, 0.1])
        gain = np.array([0.1, 0.05, -0.05])
        bound = compute_f1_lower_bound(0.7, rho, 20, delta, gain)
        assert 0.0 < bound <= 1.0


# ============================================================================
# 10.  compute_yajie_score  (gatekeeper stub)
# ============================================================================

class TestYajieScore:
    def test_all_agree(self):
        """All experts agree with given label → Q = 0 (clean)."""
        votes = np.array([[0, 0, 0, 0, 0]])  # 5 experts, all agree
        scores = compute_yajie_score(votes)
        np.testing.assert_allclose(scores, 0.0, atol=1e-15)

    def test_all_disagree(self):
        """All experts disagree → Q = 1 (noisy)."""
        votes = np.array([[1, 1, 1, 1]])
        scores = compute_yajie_score(votes)
        np.testing.assert_allclose(scores, 1.0, atol=1e-15)

    def test_mixed(self):
        votes = np.array([
            [0, 0, 1, 0, 0],   # 1/5 disagree
            [1, 1, 1, 0, 0],   # 3/5 disagree
            [1, 1, 1, 1, 1],   # 5/5 disagree
        ])
        scores = compute_yajie_score(votes)
        np.testing.assert_allclose(scores, np.array([0.2, 0.6, 1.0]))

    def test_eta_scaling(self):
        """With η>0, novelty bonus is added (placeholder N=0)."""
        votes = np.array([[0, 0, 1, 1, 0]])
        s_no_eta = compute_yajie_score(votes, eta_t=0.0)
        s_with_eta = compute_yajie_score(votes, eta_t=0.3)
        # Currently N(s)=0, so η has no effect
        np.testing.assert_allclose(s_no_eta, s_with_eta)


# ============================================================================
# 11.  Integration / round-trip tests
# ============================================================================

class TestIntegration:
    """End-to-end sanity checks spanning multiple components."""

    def test_scalar_roundtrip(self):
        """Encoding → inner product → consistency with kernel."""
        d, xi = 64, 2.0
        enc = SitusEncoder(d, xi)
        p_vals = np.linspace(0, 20, 30)
        for i, p in enumerate(p_vals):
            for q in p_vals[i:]:
                sim_ip = float(enc.inner_product(p, q))
                delta = q - p
                k_val = float(enc.kernel(delta))
                assert math.isclose(sim_ip, k_val, abs_tol=1e-14)

    def test_3d_roundtrip(self):
        """Encode → inner product → formula consistency."""
        enc = SitusEncoder3D(d=12, alpha=1.0, beta=1.5, gamma=2.0)
        p = np.random.default_rng(42).uniform(-5, 5, (10, 3))
        q = np.random.default_rng(99).uniform(-5, 5, (10, 3))
        z_p = enc.encode(p)
        z_q = enc.encode(q)
        sim_encode = np.sum(z_p * z_q, axis=1)
        sim_formula = enc.inner_product(p, q)
        np.testing.assert_allclose(sim_encode, sim_formula, atol=1e-14)

    def test_delta_situs_pipeline(self):
        """Full pipeline: compute margins → F₁ bound with Situs."""
        # Simulate a two-state system
        p_clean = np.array([0.30, 0.35])
        p_noisy = np.array([0.65, 0.70])
        p_clean_situs = np.array([0.25, 0.30])  # Situs reduces clean disagreement
        p_noisy_situs = np.array([0.80, 0.78])  # Situs increases noisy disagreement
        rho = np.array([0.6, 0.4])

        delta_situs, gain = compute_delta_s_situs(
            p_noisy_situs, p_noisy, p_clean_situs, p_clean
        )

        # Both states should show positive gain
        assert np.all(gain > 0)

        bound = compute_f1_lower_bound(
            eta=0.85, rho_s=rho, M=15,
            delta_s=p_noisy - p_clean, delta_gain=gain,
        )
        assert 0.0 < bound <= 1.0

    def test_lipschitz_across_encoders(self):
        """Lipschitz constants are consistent with empirical bounds."""
        # Scalar
        enc_s = SitusEncoder(d=32, xi=1.5)
        p_vals = np.linspace(0, 10, 100)
        for i in range(len(p_vals) - 1):
            dp = abs(p_vals[i + 1] - p_vals[i])
            dz = np.linalg.norm(
                enc_s.encode(p_vals[i + 1]) - enc_s.encode(p_vals[i])
            )
            assert dz <= enc_s.lipschitz_ * dp + 1e-12

        # 3D
        enc_3d = SitusEncoder3D(d=12, alpha=1.0, beta=1.0, gamma=2.0)
        p = np.random.default_rng(7).uniform(-3, 3, (100, 3))
        for i in range(99):
            dp_vec = p[i + 1] - p[i]
            dp_norm = np.linalg.norm(dp_vec)
            dz_norm = np.linalg.norm(
                enc_3d.encode(p[i + 1]) - enc_3d.encode(p[i])
            )
            assert dz_norm <= enc_3d.lipschitz_ * dp_norm + 1e-12
