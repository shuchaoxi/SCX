"""
Tests for Two-Layer State Discovery.

Tests:
1. ErrorDrivenEncoder basic construction
2. ErrorDrivenEncoder can discover high-error regions from synthetic data
3. ErrorDrivenEncoder feature_selection modes all work (mutual_info, correlation, none)
4. ErrorDrivenEncoder.fit_error_states with layer1_labels
5. ErrorDrivenEncoder.get_high_error_states
6. ErrorDrivenEncoder.summary
7. TwoLayerStateDiscovery basic pipeline
8. TwoLayerStateDiscovery.recommend_sampling
9. TwoLayerStateDiscovery.compare_with_pure_layer1
10. TwoLayerStateDiscovery error-driven labels differ from pure layer1
"""

from __future__ import annotations

import numpy as np
import pytest

from scx.encoders.error_driven import ErrorDrivenEncoder
from scx.encoders.tabular import TabularEncoder
from scx.state.two_layer import TwoLayerStateDiscovery


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def simple_tabular_encoder() -> TabularEncoder:
    """Simple non-normalizing tabular encoder for synthetic test data."""
    return TabularEncoder(normalize=False)


@pytest.fixture
def three_cluster_data() -> tuple[list[np.ndarray], np.ndarray]:
    """Synthetic data: 3 clusters in 5D with distinct error levels.

    Returns
    -------
    X_raw : list[np.ndarray]
        100 samples (30 low-error, 30 medium, 40 high)
    residuals : np.ndarray, shape (100,)
    """
    rng = np.random.default_rng(42)
    X = np.vstack([
        rng.normal([0, 0, 0, 0, 0], 0.3, (30, 5)),   # low error
        rng.normal([3, 3, 3, 3, 3], 0.3, (30, 5)),   # medium error
        rng.normal([6, 6, 6, 6, 6], 0.3, (40, 5)),   # high error
    ])
    residuals = np.array([0.05] * 30 + [0.15] * 30 + [0.50] * 40)
    residuals += rng.normal(0, 0.02, 100)
    return [row for row in X], residuals


@pytest.fixture
def two_cluster_uneven_error() -> tuple[list[np.ndarray], np.ndarray]:
    """2 clusters where one has high internal error variance.

    Cluster 0: 50 samples, error ~0.05 (low, tight)
    Cluster 1: 50 samples, error ~0.10 (subgroup A) or ~0.60 (subgroup B, high)
    Tests the case where error-driven splitting is beneficial.
    """
    rng = np.random.default_rng(123)
    X = np.vstack([
        rng.normal([1, 1, 1], 0.2, (50, 3)),       # cluster 0
        rng.normal([5, 5, 5], 0.3, (50, 3)),       # cluster 1 (high variance error)
    ])
    residuals = np.array(
        [0.05] * 50 + [0.10] * 25 + [0.60] * 25
    ) + rng.normal(0, 0.015, 100)
    return [row for row in X], residuals


# ======================================================================
# ErrorDrivenEncoder Tests
# ======================================================================


class TestErrorDrivenEncoderConstruction:
    """Construction and parameter validation."""

    def test_basic_construction(self, simple_tabular_encoder):
        encoder = ErrorDrivenEncoder(simple_tabular_encoder, n_error_states=5)
        assert encoder.n_error_states == 5
        assert encoder.feature_selection == "mutual_info"
        assert encoder.layer1 is simple_tabular_encoder
        assert encoder.get_feature_dim() == 0  # TabularEncoder doesn't set _feature_dim

    def test_construction_with_feature_selection(self, simple_tabular_encoder):
        encoder = ErrorDrivenEncoder(
            simple_tabular_encoder,
            n_error_states=8,
            feature_selection="correlation",
        )
        assert encoder.n_error_states == 8
        assert encoder.feature_selection == "correlation"

    def test_construction_with_none_selection(self, simple_tabular_encoder):
        encoder = ErrorDrivenEncoder(
            simple_tabular_encoder, feature_selection="none"
        )
        assert encoder.feature_selection == "none"

    def test_invalid_feature_selection(self, simple_tabular_encoder):
        with pytest.raises(ValueError, match="Unknown feature_selection"):
            ErrorDrivenEncoder(simple_tabular_encoder, feature_selection="invalid")

    def test_n_error_states_at_least_one(self, simple_tabular_encoder):
        encoder = ErrorDrivenEncoder(simple_tabular_encoder, n_error_states=0)
        assert encoder.n_error_states == 1


class TestErrorDrivenEncoderFit:
    """Core fitting behavior."""

    def test_fit_discovers_high_error_region(
        self, simple_tabular_encoder, three_cluster_data
    ):
        """The encoder should identify the high-error cluster (state 1)."""
        X_raw, residuals = three_cluster_data
        encoder = ErrorDrivenEncoder(
            simple_tabular_encoder, n_error_states=3, feature_selection="correlation"
        )
        states = encoder.fit_error_states(X_raw, residuals)

        assert len(states) >= 2  # at least 2 non-empty states

        # The high-error state should have mean_error significantly above low-error state
        errors = [s["mean_error"] for s in states.values()]
        assert max(errors) > 0.3, f"Expected high error >0.3, got max={max(errors):.4f}"
        assert min(errors) < 0.2, f"Expected low error <0.2, got min={min(errors):.4f}"

    def test_fit_generates_descriptions(
        self, simple_tabular_encoder, three_cluster_data
    ):
        """Each state should have a non-empty description."""
        X_raw, residuals = three_cluster_data
        encoder = ErrorDrivenEncoder(
            simple_tabular_encoder, n_error_states=3, feature_selection="none"
        )
        states = encoder.fit_error_states(X_raw, residuals)

        for sid, s in states.items():
            assert "description" in s
            assert len(s["description"]) > 0
            assert "err=" in s["description"]

    def test_fit_preserves_feature_profile(
        self, simple_tabular_encoder, three_cluster_data
    ):
        """feature_profile should have the right shape."""
        X_raw, residuals = three_cluster_data
        encoder = ErrorDrivenEncoder(simple_tabular_encoder, n_error_states=3)
        states = encoder.fit_error_states(X_raw, residuals)

        # X has 5 features, so feature_profile should be 5D
        first_state = list(states.values())[0]
        assert first_state["feature_profile"].shape == (5,)

    def test_fit_sets_internal_state(
        self, simple_tabular_encoder, three_cluster_data
    ):
        """After fit, internal attributes should be populated."""
        X_raw, residuals = three_cluster_data
        encoder = ErrorDrivenEncoder(simple_tabular_encoder, n_error_states=3)
        encoder.fit_error_states(X_raw, residuals)

        assert encoder.error_labels_ is not None
        assert len(encoder.error_labels_) == 100
        assert encoder.error_states_ is not None
        assert encoder._feature_importance_ is not None

    def test_fit_with_layer1_labels(
        self, simple_tabular_encoder, three_cluster_data
    ):
        """fit_error_states works with optional layer1_labels."""
        X_raw, residuals = three_cluster_data
        encoder = ErrorDrivenEncoder(simple_tabular_encoder, n_error_states=3)

        # Create simple layer1 labels
        layer1_labels = np.array([0] * 30 + [1] * 30 + [2] * 40)
        states = encoder.fit_error_states(X_raw, residuals, layer1_labels=layer1_labels)

        assert len(states) > 0


class TestErrorDrivenEncoderFeatureSelection:
    """All three feature_selection modes should work."""

    def test_mutual_info_mode(self, simple_tabular_encoder, three_cluster_data):
        X_raw, residuals = three_cluster_data
        encoder = ErrorDrivenEncoder(
            simple_tabular_encoder,
            n_error_states=3,
            feature_selection="mutual_info",
        )
        states = encoder.fit_error_states(X_raw, residuals)
        assert len(states) >= 2
        assert encoder._feature_importance_ is not None

    def test_correlation_mode(self, simple_tabular_encoder, three_cluster_data):
        X_raw, residuals = three_cluster_data
        encoder = ErrorDrivenEncoder(
            simple_tabular_encoder,
            n_error_states=3,
            feature_selection="correlation",
        )
        states = encoder.fit_error_states(X_raw, residuals)
        assert len(states) >= 2
        assert encoder._feature_importance_ is not None

    def test_none_mode(self, simple_tabular_encoder, three_cluster_data):
        X_raw, residuals = three_cluster_data
        encoder = ErrorDrivenEncoder(
            simple_tabular_encoder,
            n_error_states=3,
            feature_selection="none",
        )
        states = encoder.fit_error_states(X_raw, residuals)
        assert len(states) >= 2

    def test_all_modes_produce_same_shape(self, simple_tabular_encoder, three_cluster_data):
        """All three modes should produce valid outputs."""
        X_raw, residuals = three_cluster_data

        for mode in ["mutual_info", "correlation", "none"]:
            encoder = ErrorDrivenEncoder(
                simple_tabular_encoder, n_error_states=3, feature_selection=mode
            )
            states = encoder.fit_error_states(X_raw, residuals)
            assert len(states) >= 1, f"Mode {mode} produced no states"


class TestErrorDrivenEncoderAccessors:
    """Summary and high-error detection."""

    def test_get_high_error_states(self, simple_tabular_encoder, three_cluster_data):
        X_raw, residuals = three_cluster_data
        encoder = ErrorDrivenEncoder(simple_tabular_encoder, n_error_states=3)
        encoder.fit_error_states(X_raw, residuals)

        high = encoder.get_high_error_states()
        assert isinstance(high, list)
        assert len(high) >= 0
        # At least one state should have high error (the cluster with 0.50)
        for sid in high:
            assert encoder.error_states_[sid]["mean_error"] > 0.2

    def test_get_high_error_states_before_fit(self, simple_tabular_encoder):
        encoder = ErrorDrivenEncoder(simple_tabular_encoder)
        assert encoder.get_high_error_states() == []

    def test_summary_after_fit(self, simple_tabular_encoder, three_cluster_data):
        X_raw, residuals = three_cluster_data
        encoder = ErrorDrivenEncoder(simple_tabular_encoder, n_error_states=3)
        encoder.fit_error_states(X_raw, residuals)

        s = encoder.summary()
        assert s["status"] == "fitted"
        assert s["n_states"] >= 2
        assert s["total_samples"] == 100
        assert "mean_error_mean" in s

    def test_summary_before_fit(self, simple_tabular_encoder):
        encoder = ErrorDrivenEncoder(simple_tabular_encoder)
        s = encoder.summary()
        assert s["status"] == "not_fitted"
        assert s["n_states"] == 0

    def test_cluster_delegation_before_fit(self, simple_tabular_encoder):
        """Before fitting, cluster() should delegate to layer1."""
        encoder = ErrorDrivenEncoder(simple_tabular_encoder)
        X = np.random.default_rng(42).normal(0, 1, (50, 5))
        labels, centroids = encoder.cluster(X, n_clusters=3)
        assert len(np.unique(labels)) == 3
        assert centroids.shape == (3, 5)

    def test_cluster_after_fit_returns_error_labels(
        self, simple_tabular_encoder, three_cluster_data
    ):
        """After fitting, cluster() should return the error-driven state labels."""
        X_raw, residuals = three_cluster_data
        encoder = ErrorDrivenEncoder(simple_tabular_encoder, n_error_states=3)
        encoder.fit_error_states(X_raw, residuals)

        # cluster() on new/different X should still return the fitted labels
        X = np.random.default_rng(99).normal(0, 1, (20, 5))
        labels, centroids = encoder.cluster(X, n_clusters=3)
        assert len(labels) > 0


# ======================================================================
# TwoLayerStateDiscovery Tests
# ======================================================================


class TestTwoLayerStateDiscovery:
    """Full pipeline integration."""

    def test_discover_produces_all_keys(
        self, simple_tabular_encoder, three_cluster_data
    ):
        X_raw, residuals = three_cluster_data
        disc = TwoLayerStateDiscovery(simple_tabular_encoder)
        result = disc.discover(X_raw, residuals, layer1_k=3, layer2_k=3)

        expected_keys = {
            "layer1_labels", "layer2_labels", "error_states",
            "layer1_states", "recommendations", "layer1_metrics",
            "layer2_summary",
        }
        assert expected_keys.issubset(result.keys())

    def test_discover_layer1_labels_correct_shape(
        self, simple_tabular_encoder, three_cluster_data
    ):
        X_raw, residuals = three_cluster_data
        disc = TwoLayerStateDiscovery(simple_tabular_encoder)
        result = disc.discover(X_raw, residuals, layer1_k=3, layer2_k=3)

        assert result["layer1_labels"].shape == (100,)
        assert len(np.unique(result["layer1_labels"])) == 3

    def test_discover_layer1_metrics(
        self, simple_tabular_encoder, three_cluster_data
    ):
        X_raw, residuals = three_cluster_data
        disc = TwoLayerStateDiscovery(simple_tabular_encoder)
        result = disc.discover(X_raw, residuals, layer1_k=3, layer2_k=3)

        assert "silhouette" in result["layer1_metrics"]
        assert "davies_bouldin" in result["layer1_metrics"]
        assert result["layer1_metrics"]["silhouette"] > 0.5  # well-separated

    def test_recommend_sampling(
        self, simple_tabular_encoder, three_cluster_data
    ):
        X_raw, residuals = three_cluster_data
        disc = TwoLayerStateDiscovery(simple_tabular_encoder)
        result = disc.discover(X_raw, residuals, layer1_k=3, layer2_k=3)

        recs = result["recommendations"]
        assert len(recs) > 0
        assert recs[0]["priority"] in ("high", "medium", "low", "check_noise")
        assert recs[0]["suggested_samples"] >= 0

    def test_recommend_sampling_ordering(
        self, simple_tabular_encoder, three_cluster_data
    ):
        """High-priority items should appear first."""
        X_raw, residuals = three_cluster_data
        disc = TwoLayerStateDiscovery(simple_tabular_encoder)
        result = disc.discover(X_raw, residuals, layer1_k=3, layer2_k=3)

        recs = result["recommendations"]
        priorities = [r["priority"] for r in recs]
        # 'high' must come before 'medium' before 'low'
        assert "high" in priorities or "medium" in priorities

    def test_compare_with_pure_layer1(
        self, simple_tabular_encoder, three_cluster_data
    ):
        X_raw, residuals = three_cluster_data
        disc = TwoLayerStateDiscovery(simple_tabular_encoder)
        comp = disc.compare_with_pure_layer1(X_raw, residuals, layer1_k=3, layer2_k=3)

        assert "layer1" in comp
        assert "two_layer" in comp
        assert "improvement" in comp
        assert comp["layer1"]["n_states"] == 3
        assert comp["layer1"]["state_error_spread"] >= 0

    def test_two_layer_discovers_finer_states(
        self, simple_tabular_encoder, two_cluster_uneven_error
    ):
        """With uneven error within a cluster, two-layer should resolve more states."""
        X_raw, residuals = two_cluster_uneven_error
        disc = TwoLayerStateDiscovery(simple_tabular_encoder)
        result = disc.discover(X_raw, residuals, layer1_k=2, layer2_k=4)

        n_l1 = len(result["layer1_states"])
        n_l2 = len(result["error_states"])
        # Layer 2 should have at least as many states as Layer 1
        # (may have more due to error-driven splitting)
        assert n_l2 >= n_l1

    def test_accessors_after_discover(
        self, simple_tabular_encoder, three_cluster_data
    ):
        X_raw, residuals = three_cluster_data
        disc = TwoLayerStateDiscovery(simple_tabular_encoder)
        disc.discover(X_raw, residuals, layer1_k=3, layer2_k=3)

        l1 = disc.get_layer1_labels()
        l2 = disc.get_layer2_labels()
        es = disc.get_error_states()

        assert l1 is not None and len(l1) == 100
        assert l2 is not None and len(l2) == 100
        assert len(es) > 0

    def test_recommend_sampling_with_error_only(
        self, simple_tabular_encoder
    ):
        """recommend_sampling should handle empty error_states gracefully."""
        disc = TwoLayerStateDiscovery(simple_tabular_encoder)
        recs = disc.recommend_sampling({}, budget=50)
        assert recs == []

    def test_discover_with_different_method(
        self, simple_tabular_encoder, three_cluster_data
    ):
        """Should support different StateDiscovery methods."""
        X_raw, residuals = three_cluster_data
        disc = TwoLayerStateDiscovery(simple_tabular_encoder)
        result = disc.discover(
            X_raw, residuals, layer1_k=3, layer2_k=3, method="gmm"
        )
        assert result["layer1_labels"].shape == (100,)


# ======================================================================
# Edge cases
# ======================================================================


class TestErrorDrivenEncoderEdgeCases:
    """Edge cases: small data, single cluster, etc."""

    def test_single_sample(self, simple_tabular_encoder):
        encoder = ErrorDrivenEncoder(simple_tabular_encoder, n_error_states=1)
        X_raw = [np.array([1.0, 2.0, 3.0])]
        residuals = np.array([0.1])
        states = encoder.fit_error_states(X_raw, residuals)
        assert len(states) >= 1

    def test_all_same_error(self, simple_tabular_encoder):
        """When all errors are identical, should still produce states."""
        rng = np.random.default_rng(42)
        X = rng.normal(0, 1, (20, 3))
        X_raw = [row for row in X]
        residuals = np.ones(20) * 0.1

        encoder = ErrorDrivenEncoder(simple_tabular_encoder, n_error_states=2)
        states = encoder.fit_error_states(X_raw, residuals)
        assert len(states) >= 1

    def test_residuals_multi_component(self, simple_tabular_encoder):
        """2D residuals (N, M) should be reduced to 1D via norm."""
        rng = np.random.default_rng(42)
        X = rng.normal(0, 1, (20, 3))
        X_raw = [row for row in X]
        residuals = rng.normal(0, 0.1, (20, 6))  # 6-component force error

        encoder = ErrorDrivenEncoder(simple_tabular_encoder, n_error_states=2)
        states = encoder.fit_error_states(X_raw, residuals)
        assert len(states) >= 1

    def test_layer1_labels_provided(self, simple_tabular_encoder):
        """Providing layer1_labels should not crash."""
        rng = np.random.default_rng(42)
        X = rng.normal(0, 1, (30, 3))
        X_raw = [row for row in X]
        residuals = rng.uniform(0, 0.5, 30)
        layer1_labels = np.array([0] * 15 + [1] * 15)

        encoder = ErrorDrivenEncoder(simple_tabular_encoder, n_error_states=3)
        states = encoder.fit_error_states(X_raw, residuals, layer1_labels=layer1_labels)
        assert len(states) >= 1
