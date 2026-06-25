"""Tests for StateRobustness: misclassification impact, cross-descriptor stability,
bootstrap K suggestion, and boundary confidence."""

from __future__ import annotations

import numpy as np
import pytest

from scx.state.robustness import StateRobustness, _fraction_changed
from scx.valuation.classifier import DataClassifier


# ======================================================================
# Helper fixtures (module-level to avoid conftest dependency on new module)
# ======================================================================

@pytest.fixture
def simple_cluster_data() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Small 2D data with 3 well-separated clusters.

    Returns
    -------
    X : np.ndarray, shape (150, 2)
    y_true : np.ndarray, shape (150,)
    y_pred : np.ndarray, shape (150,)  (perfect prediction)
    """
    rng = np.random.default_rng(42)
    centers = [[0.0, 0.0], [10.0, 0.0], [0.0, 10.0]]
    X_list, y_list = [], []
    for i, c in enumerate(centers):
        X_list.append(rng.normal(c, 0.3, (50, 2)))
        y_list.append(np.full(50, i))
    X = np.vstack(X_list)
    y = np.concatenate(y_list)
    return X, y, y.copy()


@pytest.fixture
def simple_R_matrix() -> np.ndarray:
    """Expert risk matrix: 3 experts, 3 states."""
    return np.array([
        [0.1, 0.5, 0.2],
        [0.2, 0.4, 0.3],
        [0.3, 0.3, 0.1],
    ], dtype=float)


@pytest.fixture
def sample_4cluster() -> tuple[np.ndarray, np.ndarray]:
    """4 Gaussian clusters, 50 samples each, 3 features."""
    rng = np.random.default_rng(42)
    centers = [[0, 0, 0], [5, 5, 5], [10, 0, 0], [0, 10, 0]]
    X_list, y_list = [], []
    for i, c in enumerate(centers):
        X_list.append(rng.normal(c, 0.5, (50, 3)))
        y_list.append(np.full(50, i))
    return np.vstack(X_list), np.concatenate(y_list)


# ======================================================================
# Test _fraction_changed helper
# ======================================================================

class TestFractionChanged:
    """Unit tests for the internal helper."""

    def test_no_change(self):
        assert _fraction_changed({0, 1}, {0, 1}, 2) == 0.0

    def test_all_flipped(self):
        assert _fraction_changed({0, 1}, {2, 3}, 4) == 1.0

    def test_partial_change(self):
        assert _fraction_changed({0, 1}, {1, 2}, 3) == pytest.approx(2 / 3)

    def test_empty_new_K(self):
        assert _fraction_changed(set(), set(), 0) == 0.0


# ======================================================================
# Test misclassification_impact
# ======================================================================

class TestMisclassificationImpact:
    """Verify merge/split/noise simulation behaviour."""

    def test_impact_returns_dict_keys(self, simple_cluster_data, simple_R_matrix):
        X, _, y_pred = simple_cluster_data
        dc = DataClassifier()
        result = StateRobustness.misclassification_impact(
            X, y_pred, y_pred, simple_R_matrix, dc,
        )
        expected_keys = {
            "merge_impact", "split_impact", "noise_impact",
            "stable_states", "sensitive_states",
        }
        assert set(result.keys()) == expected_keys

    def test_impact_values_in_range(self, simple_cluster_data, simple_R_matrix):
        X, _, y_pred = simple_cluster_data
        dc = DataClassifier()
        result = StateRobustness.misclassification_impact(
            X, y_pred, y_pred, simple_R_matrix, dc,
        )
        assert 0.0 <= result["merge_impact"] <= 1.0
        assert 0.0 <= result["split_impact"] <= 1.0
        assert 0.0 <= result["noise_impact"] <= 1.0

    def test_stable_and_sensitive_are_lists_of_ints(
        self, simple_cluster_data, simple_R_matrix,
    ):
        X, _, y_pred = simple_cluster_data
        dc = DataClassifier()
        result = StateRobustness.misclassification_impact(
            X, y_pred, y_pred, simple_R_matrix, dc,
        )
        assert isinstance(result["stable_states"], list)
        assert isinstance(result["sensitive_states"], list)
        if result["stable_states"]:
            assert isinstance(result["stable_states"][0], int)
        if result["sensitive_states"]:
            assert isinstance(result["sensitive_states"][0], int)

    def test_invalid_classifier_raises(self, simple_cluster_data, simple_R_matrix):
        X, y_true, y_pred = simple_cluster_data
        with pytest.raises(TypeError, match="DataClassifier"):
            StateRobustness.misclassification_impact(
                X, y_true, y_pred, simple_R_matrix, classifier="not_a_classifier",
            )


# ======================================================================
# Test cross_descriptor_stability
# ======================================================================

class TestCrossDescriptorStability:
    """ARI between two label sets from different descriptor spaces."""

    def test_perfect_match(self):
        labels = np.array([0, 0, 1, 1, 2, 2])
        ari = StateRobustness.cross_descriptor_stability(
            np.empty((6, 2)), np.empty((6, 5)), labels, labels,
        )
        assert ari == 1.0

    def test_random_labels(self):
        rng = np.random.default_rng(42)
        l1 = np.array([0, 0, 1, 1, 2, 2, 0, 1, 2])
        l2 = np.array([0, 1, 0, 1, 0, 1, 2, 2, 2])
        ari = StateRobustness.cross_descriptor_stability(
            np.empty((9, 2)), np.empty((9, 3)), l1, l2,
        )
        # ARI for totally independent partitions with enough matches
        assert -1.0 <= ari <= 1.0

    def test_shape_mismatch_raises(self):
        with pytest.raises(ValueError, match="shape mismatch"):
            StateRobustness.cross_descriptor_stability(
                np.empty((5, 2)), np.empty((5, 3)),
                np.array([0, 0, 1, 1, 2]),
                np.array([0, 0, 1, 1]),
            )


# ======================================================================
# Test suggest_robust_states
# ======================================================================

class TestSuggestRobustStates:
    """Bootstrap-based robust K suggestion."""

    def test_returns_int(self, sample_4cluster):
        X, y = sample_4cluster
        k = StateRobustness.suggest_robust_states(
            X, n_trials=5, subsample_ratio=0.85,
        )
        assert isinstance(k, int)

    def test_reasonable_k(self, sample_4cluster):
        X, y = sample_4cluster
        k = StateRobustness.suggest_robust_states(
            X, n_trials=5, subsample_ratio=0.85,
        )
        # With 4 clear clusters, should suggest at least 2,
        # no more than 10 (bound set by sqrt(N) + 5 ~ 17)
        assert 2 <= k <= 17

    def test_tiny_data(self):
        """Edge case: very small dataset."""
        X = np.random.randn(5, 2)
        k = StateRobustness.suggest_robust_states(
            X, n_trials=3, subsample_ratio=0.8,
        )
        assert isinstance(k, int)
        assert k >= 2


# ======================================================================
# Test state_boundary_confidence
# ======================================================================

class TestStateBoundaryConfidence:
    """Per-sample confidence scores."""

    def test_confidence_shape(self, simple_cluster_data):
        X, _, labels = simple_cluster_data
        centroids = np.array([[0.0, 0.0], [10.0, 0.0], [0.0, 10.0]])
        conf = StateRobustness.state_boundary_confidence(X, labels, centroids)
        assert conf.shape == (150,)

    def test_confidence_in_range(self, simple_cluster_data):
        X, _, labels = simple_cluster_data
        centroids = np.array([[0.0, 0.0], [10.0, 0.0], [0.0, 10.0]])
        conf = StateRobustness.state_boundary_confidence(X, labels, centroids)
        assert np.all(conf >= 0.0)
        assert np.all(conf <= 1.0)

    def test_high_confidence_near_centroids(self):
        """Points on centroids get near-max confidence."""
        centroids = np.array([[0.0, 0.0], [5.0, 5.0]])
        X = np.array([[0.0, 0.0], [5.0, 5.0]])
        conf = StateRobustness.state_boundary_confidence(X, np.array([0, 1]), centroids)
        assert conf[0] > 0.5
        assert conf[1] > 0.5

    def test_low_confidence_at_boundary(self):
        """Points equidistant to two centroids get low confidence."""
        centroids = np.array([[0.0, 0.0], [2.0, 0.0]])
        X = np.array([[1.0, 0.0]])
        conf = StateRobustness.state_boundary_confidence(X, np.array([0]), centroids)
        # The margin between the two softmax probabilities should be tiny
        assert conf[0] < 0.1
