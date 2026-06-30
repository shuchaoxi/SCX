"""Tests for the Utils module: helpers, DataLoader, Evaluation."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from scx.utils.helpers import (
    safe_divide,
    softmax,
    rbf_kernel,
    pairwise_distance,
    entropy,
    normalize,
    batch_iterator,
)
from scx.utils.data_loader import DataLoader
from scx.utils.evaluation import Evaluation


# ======================================================================
# Helpers tests
# ======================================================================


class TestHelpers:
    """softmax (row sum=1), rbf_kernel (symmetric positive-definite), entropy, etc."""

    # --- safe_divide ---

    def test_safe_divide_basic(self):
        result = safe_divide(np.array([1.0, 2.0, 3.0]), np.array([1.0, 2.0, 3.0]))
        np.testing.assert_allclose(result, [1.0, 1.0, 1.0])

    def test_safe_divide_by_zero(self):
        result = safe_divide(np.array([1.0]), np.array([0.0]))
        assert np.isfinite(result)

    def test_safe_divide_scalar(self):
        result = safe_divide(5.0, 2.0)
        assert result == pytest.approx(2.5, rel=1e-4)

    # --- softmax ---

    def test_softmax_row_sum(self):
        x = np.array([[1.0, 2.0, 3.0], [0.5, 0.0, -0.5]])
        probs = softmax(x, axis=-1)
        np.testing.assert_allclose(probs.sum(axis=1), np.ones(2), rtol=1e-5)

    def test_softmax_all_positive(self):
        x = np.array([[1.0, 2.0, 3.0]])
        probs = softmax(x)
        assert np.all(probs >= 0)

    def test_softmax_temperature_effect(self):
        x = np.array([[1.0, 2.0, 3.0]])
        p_low = softmax(x, temperature=0.1)
        p_high = softmax(x, temperature=10.0)
        # Low temp -> sharper (max prob higher)
        assert p_low.max() > p_high.max()

    def test_softmax_1d(self):
        x = np.array([1.0, 2.0, 3.0])
        probs = softmax(x)
        assert abs(probs.sum() - 1.0) < 1e-5

    # --- rbf_kernel ---

    def test_rbf_kernel_shape(self):
        X = np.random.randn(5, 3)
        K = rbf_kernel(X)
        assert K.shape == (5, 5)

    def test_rbf_kernel_symmetric(self):
        X = np.random.randn(5, 3)
        K = rbf_kernel(X)
        assert np.allclose(K, K.T)

    def test_rbf_kernel_positive_definite(self):
        X = np.random.randn(5, 3)
        K = rbf_kernel(X)
        eigenvalues = np.linalg.eigvalsh(K)
        assert np.all(eigenvalues > -1e-10)  # numerically PSD

    def test_rbf_kernel_diagonal(self):
        X = np.random.randn(5, 3)
        K = rbf_kernel(X)
        np.testing.assert_allclose(np.diag(K), np.ones(5), rtol=1e-5)

    def test_rbf_kernel_different_sets(self):
        X = np.random.randn(5, 3)
        Y = np.random.randn(7, 3)
        K = rbf_kernel(X, Y)
        assert K.shape == (5, 7)

    # --- pairwise_distance ---

    def test_pairwise_distance_symmetric(self):
        X = np.random.randn(5, 3)
        D = pairwise_distance(X, metric="euclidean")
        assert D.shape == (5, 5)
        assert np.allclose(D, D.T)
        assert np.allclose(np.diag(D), 0.0, atol=1e-5)

    def test_pairwise_distance_sqeuclidean(self):
        X = np.random.randn(5, 3)
        D_sq = pairwise_distance(X, metric="sqeuclidean")
        assert np.all(D_sq >= 0)
        assert np.allclose(D_sq, D_sq.T)
        assert np.allclose(np.diag(D_sq), 0.0, atol=1e-5)

    # --- entropy ---

    def test_entropy_uniform(self):
        probs = np.array([0.25, 0.25, 0.25, 0.25])
        H = entropy(probs)
        expected = -4 * 0.25 * np.log(0.25)
        assert abs(H - expected) < 1e-5

    def test_entropy_certain(self):
        probs = np.array([1.0, 0.0, 0.0])
        H = entropy(probs)
        assert abs(H) < 1e-5  # ~0

    def test_entropy_batch(self):
        probs = np.array([[0.5, 0.5], [1.0, 0.0]])
        H = entropy(probs, axis=-1)
        assert H.shape == (2,)
        assert H[1] < 1e-5    # certain -> 0
        assert H[0] > H[1]    # uncertain -> higher

    # --- normalize ---

    def test_normalize_standard(self):
        X = np.random.randn(20, 5)
        X_norm = normalize(X, method="standard")
        assert abs(np.mean(X_norm, axis=0).mean()) < 1e-10
        assert abs(np.std(X_norm, axis=0).mean() - 1.0) < 0.1

    def test_normalize_minmax(self):
        X = np.random.randn(20, 5)
        X_norm = normalize(X, method="minmax")
        assert np.all(X_norm >= 0)
        assert np.all(X_norm <= 1)

    def test_normalize_l2(self):
        X = np.random.randn(20, 5)
        X_norm = normalize(X, method="l2")
        norms = np.linalg.norm(X_norm, axis=1)
        np.testing.assert_allclose(norms, np.ones(20), rtol=1e-5)

    def test_normalize_invalid_method(self):
        with pytest.raises(ValueError, match="Unknown method"):
            normalize(np.random.randn(5, 2), method="invalid")

    # --- batch_iterator ---

    def test_batch_iterator(self):
        X = np.random.randn(50, 2)
        y = np.random.randn(50)
        batches = list(batch_iterator(X, y, batch_size=10))
        assert len(batches) == 5
        for Xb, yb in batches:
            assert Xb.shape[0] <= 10
            assert yb.shape[0] == Xb.shape[0]

    def test_batch_iterator_no_y(self):
        X = np.random.randn(37, 2)
        batches = list(batch_iterator(X, batch_size=10))
        assert len(batches) == 4
        for Xb, yb in batches:
            assert yb is None

    def test_batch_iterator_partial_batch(self):
        X = np.random.randn(37, 2)
        batches = list(batch_iterator(X, batch_size=10))
        last_X, _ = batches[-1]
        assert last_X.shape[0] == 7  # remainder


# ======================================================================
# DataLoader tests
# ======================================================================


class TestDataLoader:
    """from_numpy, from_dataframe, split, inject_noise, inject_redundancy."""

    def test_from_numpy(self):
        X = np.random.randn(20, 3)
        y = np.random.randn(20)
        data = DataLoader.from_numpy(X, y)
        assert "X" in data
        assert "y" in data
        assert data["n_samples"] == 20
        assert data["n_features"] == 3

    def test_from_numpy_no_y(self):
        X = np.random.randn(15, 4)
        data = DataLoader.from_numpy(X)
        assert "y" not in data

    def test_from_numpy_with_experts(self, sample_experts):
        X = np.random.randn(10, 2)
        data = DataLoader.from_numpy(X, experts=sample_experts)
        assert "experts" in data
        assert len(data["experts"]) == 3

    def test_from_dataframe(self):
        df = pd.DataFrame({
            "f1": np.random.randn(20),
            "f2": np.random.randn(20),
            "label": np.random.randint(0, 2, 20),
        })
        data = DataLoader.from_dataframe(df, feature_cols=["f1", "f2"], label_col="label")
        assert data["X"].shape == (20, 2)
        assert "y" in data
        assert data["n_samples"] == 20

    def test_from_dataframe_no_label(self):
        df = pd.DataFrame({"f1": np.random.randn(10), "f2": np.random.randn(10)})
        data = DataLoader.from_dataframe(df, feature_cols=["f1", "f2"])
        assert "y" not in data

    def test_split(self):
        X = np.random.randn(100, 2)
        y = np.random.randn(100)
        data = {"X": X, "y": y}
        train, test = DataLoader.split(data, test_size=0.2, random_state=42)
        assert train["X"].shape[0] == 80
        assert test["X"].shape[0] == 20
        assert "y" in train
        assert "y" in test

    def test_split_no_y(self):
        X = np.random.randn(100, 2)
        data = {"X": X}
        train, test = DataLoader.split(data, test_size=0.2)
        assert "y" not in train

    def test_inject_noise_shape(self):
        y = np.random.randn(50)
        y_noisy = DataLoader.inject_noise(y, noise_ratio=0.2, random_state=42)
        assert y_noisy.shape == (50,)

    def test_inject_noise_different(self):
        y = np.random.randn(50)
        y_noisy = DataLoader.inject_noise(y, noise_ratio=1.0, noise_std=10.0, random_state=42)
        # With 100% noise and large std, at least some values should differ
        assert not np.allclose(y, y_noisy)

    def test_inject_redundancy_shape(self):
        X = np.random.randn(50, 3)
        y = np.random.randn(50)
        X_aug, y_aug = DataLoader.inject_redundancy(
            X, y, redundancy_ratio=0.3, random_state=42
        )
        # Expect 50 + 15 = 65 samples (ceil of 0.3*50)
        expected_n = 50 + max(1, int(0.3 * 50))
        assert X_aug.shape[0] == expected_n
        assert y_aug.shape[0] == expected_n
        assert X_aug.shape[1] == 3

    def test_from_extxyz_missing_file(self):
        """Should raise an error if file doesn't exist (ASE is installed)."""
        with pytest.raises((ImportError, FileNotFoundError, OSError)):
            DataLoader.from_extxyz("/nonexistent/file.xyz")


# ======================================================================
# Evaluation tests
# ======================================================================


class TestEvaluation:
    """rmse, mae, r2, acquisition_efficiency, compression_fidelity."""

    def test_rmse(self):
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.1, 2.1, 2.9])
        err = Evaluation.rmse(y_true, y_pred)
        assert err >= 0

    def test_rmse_perfect(self):
        y_true = np.array([1.0, 2.0, 3.0])
        err = Evaluation.rmse(y_true, y_true)
        assert err == 0.0

    def test_mae(self):
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.5, 2.5, 2.5])
        err = Evaluation.mae(y_true, y_pred)
        assert err >= 0

    def test_mae_perfect(self):
        y_true = np.array([1.0, 2.0, 3.0])
        err = Evaluation.mae(y_true, y_true)
        assert err == 0.0

    def test_r2_score(self):
        y_true = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred = np.array([1.0, 2.0, 3.0, 4.0])
        r2 = Evaluation.r2_score(y_true, y_pred)
        assert r2 == 1.0

    def test_r2_score_random(self):
        rng = np.random.default_rng(42)
        y_true = rng.normal(0, 1, 100)
        y_pred = y_true + rng.normal(0, 0.5, 100)
        r2 = Evaluation.r2_score(y_true, y_pred)
        assert 0.0 < r2 < 1.0

    def test_acquisition_efficiency(self):
        selected = np.array([0, 2, 5])
        oracle = np.array([0.1, 0.2, 0.3, 0.1, 0.05, 0.25])
        eff = Evaluation.acquisition_efficiency(selected, oracle)
        # achieved = 0.1 + 0.3 + 0.25 = 0.65, total = 1.0
        assert abs(eff - 0.65) < 1e-5

    def test_acquisition_efficiency_zero_total(self):
        eff = Evaluation.acquisition_efficiency(np.array([0]), np.array([0.0, 0.0]))
        assert eff == 0.0

    def test_classification_report_df_with_true(self):
        pred = np.array([0, 0, 1, 1, 2, 2])
        true = np.array([0, 1, 1, 1, 2, 2])
        df = Evaluation.classification_report_df(pred, true)
        assert isinstance(df, pd.DataFrame)

    def test_classification_report_df_counts(self):
        pred = np.array([0, 0, 1, 1, 2])
        df = Evaluation.classification_report_df(pred)
        assert "category" in df.columns
        assert "count" in df.columns

    def test_compression_fidelity(self):
        y_orig = np.random.randn(100)
        y_comp = np.random.randn(30)
        w = np.ones(30) / 30
        fid = Evaluation.compression_fidelity(y_orig, y_comp, weights=w)
        assert "mean_shift" in fid
        assert "std_shift" in fid
        assert "ks_statistic" in fid
        assert "wasserstein_distance" in fid

    def test_compression_fidelity_no_weights(self):
        y_orig = np.random.randn(100)
        y_comp = np.random.randn(30)
        fid = Evaluation.compression_fidelity(y_orig, y_comp)
        assert "mean_shift" in fid

    def test_expert_routing_accuracy(self):
        routed = np.array([0, 1, 0, 2, 1])
        oracle = np.array([0, 1, 0, 2, 1])
        acc = Evaluation.expert_routing_accuracy(routed, oracle)
        assert acc == 1.0

    def test_expert_routing_accuracy_empty(self):
        acc = Evaluation.expert_routing_accuracy(np.array([]), np.array([]))
        assert acc == 0.0

    def test_benchmark(self):
        baseline = {"random": np.random.randn(50)}
        scx = {"scx": np.random.randn(50)}
        comparison = Evaluation.benchmark(baseline, scx)
        assert isinstance(comparison, pd.DataFrame)
        assert "mean" in comparison.columns
        assert "std" in comparison.columns
        assert "vs_best" in comparison.columns
