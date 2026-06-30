"""Tests for the State module: StateSpace, StateDiscovery, StateAssignment, StateMetrics."""

from __future__ import annotations

import pickle
import tempfile

import numpy as np
import pytest

from scx.state.space import StateInfo, StateSpace
from scx.state.discovery import StateDiscovery, _softmax_dist
from scx.state.assignment import StateAssignment
from scx.state.metrics import StateMetrics


# ======================================================================
# StateSpace tests
# ======================================================================


class TestStateInfo:
    """Verify StateInfo dataclass construction."""

    def test_basic_construction(self):
        s = StateInfo(id=0, label="s0", centroid=np.array([1.0, 2.0]),
                      radius=0.5, count=100, proportion=0.25)
        assert s.id == 0
        assert s.label == "s0"
        assert np.allclose(s.centroid, [1.0, 2.0])
        assert s.radius == 0.5
        assert s.count == 100
        assert s.proportion == 0.25


class TestStateSpace:
    """CRUD, batch accessors, summary, save/load."""

    def test_init(self):
        ss = StateSpace(n_states=4)
        assert ss.n_states == 4
        assert len(ss.states) == 0
        assert ss.assignment is None
        assert ss.soft_assignment is None

    def test_add_and_get_state(self):
        ss = StateSpace(n_states=2)
        s0 = StateInfo(id=0, label="s0", centroid=np.array([0.0, 0.0]),
                       radius=0.3, count=50, proportion=0.5)
        ss.add_state(s0)
        assert ss.get_state(0).id == 0
        assert ss.get_state(0).label == "s0"

    def test_get_state_raises_keyerror(self):
        ss = StateSpace(n_states=2)
        with pytest.raises(KeyError, match="not found"):
            ss.get_state(99)

    def test_remove_state(self):
        ss = StateSpace(n_states=3)
        s0 = StateInfo(id=0, label="s0", centroid=np.zeros(2),
                       radius=0.3, count=50, proportion=0.33)
        s1 = StateInfo(id=1, label="s1", centroid=np.ones(2),
                       radius=0.3, count=50, proportion=0.33)
        ss.add_state(s0)
        ss.add_state(s1)
        ss.remove_state(0)
        assert 0 not in ss.states
        assert ss.n_states == 1

    def test_remove_state_raises_keyerror(self):
        ss = StateSpace(n_states=2)
        with pytest.raises(KeyError, match="cannot remove"):
            ss.remove_state(99)

    def test_get_centroids(self, sample_centroids):
        ss = StateSpace(n_states=4)
        for i, c in enumerate(sample_centroids):
            ss.add_state(StateInfo(id=i, label=f"s{i}", centroid=c,
                                   radius=0.3, count=100, proportion=0.25))
        centroids = ss.get_centroids()
        assert centroids.shape == (4, 2)
        np.testing.assert_allclose(centroids, sample_centroids)

    def test_get_centroids_ordered_by_id(self):
        ss = StateSpace(n_states=2)
        ss.add_state(StateInfo(id=1, label="s1", centroid=np.array([5.0, 5.0]),
                               radius=0.3, count=100, proportion=0.5))
        ss.add_state(StateInfo(id=0, label="s0", centroid=np.array([0.0, 0.0]),
                               radius=0.3, count=100, proportion=0.5))
        centroids = ss.get_centroids()
        np.testing.assert_allclose(centroids[0], [0.0, 0.0])
        np.testing.assert_allclose(centroids[1], [5.0, 5.0])

    def test_get_proportions(self):
        ss = StateSpace(n_states=2)
        ss.add_state(StateInfo(id=0, label="s0", centroid=np.zeros(2),
                               radius=0.3, count=70, proportion=0.7))
        ss.add_state(StateInfo(id=1, label="s1", centroid=np.ones(2),
                               radius=0.3, count=30, proportion=0.3))
        props = ss.get_proportions()
        assert len(props) == 2
        assert props[0] == 0.7
        assert props[1] == 0.3

    def test_summary_dataframe(self):
        ss = StateSpace(n_states=2)
        ss.add_state(StateInfo(id=0, label="s0", centroid=np.zeros(2),
                               radius=0.3, count=70, proportion=0.7))
        ss.add_state(StateInfo(id=1, label="s1", centroid=np.ones(2),
                               radius=0.3, count=30, proportion=0.3))
        df = ss.summary()
        assert list(df.columns) == ["id", "label", "radius", "count", "proportion"]
        assert len(df) == 2

    def test_save_and_load(self):
        ss = StateSpace(n_states=2)
        ss.add_state(StateInfo(id=0, label="s0", centroid=np.zeros(2),
                               radius=0.3, count=70, proportion=0.7))
        with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as tmp:
            path = tmp.name
        try:
            ss.save(path)
            loaded = StateSpace.load(path)
            assert loaded.n_states == ss.n_states
            assert loaded.get_state(0).label == "s0"
            np.testing.assert_allclose(
                loaded.get_centroids(), ss.get_centroids()
            )
        finally:
            import os
            os.unlink(path)

    def test_load_invalid_type(self):
        """Loading a non-StateSpace pickle should raise TypeError."""
        with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as tmp:
            path = tmp.name
            pickle.dump({"not": "statespace"}, tmp)
        try:
            with pytest.raises(TypeError, match="not a StateSpace"):
                StateSpace.load(path)
        finally:
            import os
            os.unlink(path)


# ======================================================================
# StateDiscovery tests
# ======================================================================


class TestStateDiscovery:
    """Fit / predict / fit_predict / get_centroids for all methods."""

    def test_kmeans_fit_predict(self, sample_data_2d):
        X, _ = sample_data_2d
        sd = StateDiscovery(method="kmeans", n_states=4, random_state=42)
        labels = sd.fit_predict(X)
        assert labels.shape == (400,)
        assert len(np.unique(labels)) == 4

    def test_kmeans_centroids(self, sample_data_2d):
        X, _ = sample_data_2d
        sd = StateDiscovery(method="kmeans", n_states=4, random_state=42)
        sd.fit(X)
        centroids = sd.get_centroids()
        assert centroids.shape == (4, 2)

    def test_gmm_fit_predict(self, sample_data_2d):
        X, _ = sample_data_2d
        sd = StateDiscovery(method="gmm", n_states=4, random_state=42)
        labels = sd.fit_predict(X)
        assert labels.shape == (400,)
        assert len(np.unique(labels)) == 4

    def test_gmm_centroids(self, sample_data_2d):
        X, _ = sample_data_2d
        sd = StateDiscovery(method="gmm", n_states=4, random_state=42)
        sd.fit(X)
        centroids = sd.get_centroids()
        assert centroids.shape == (4, 2)

    def test_spectral_fit_predict(self, sample_data_2d):
        X, _ = sample_data_2d
        sd = StateDiscovery(method="spectral", n_states=4, random_state=42, gamma=1.0)
        labels = sd.fit_predict(X)
        assert labels.shape == (400,)
        assert len(np.unique(labels)) == 4

    def test_spectral_centroids(self, sample_data_2d):
        X, _ = sample_data_2d
        sd = StateDiscovery(method="spectral", n_states=4, random_state=42, gamma=1.0)
        sd.fit(X)
        centroids = sd.get_centroids()
        assert centroids.shape == (4, 2)

    def test_predict_after_fit(self, sample_data_2d):
        X, _ = sample_data_2d
        sd = StateDiscovery(method="kmeans", n_states=4, random_state=42)
        sd.fit(X)
        new_X = np.array([[2.5, 2.5], [-1.0, -1.0]])
        preds = sd.predict(new_X)
        assert preds.shape == (2,)
        assert preds.dtype.kind in ("i", "u")

    def test_predict_without_fit_raises(self):
        sd = StateDiscovery(method="kmeans", n_states=4)
        with pytest.raises(RuntimeError, match="not been fitted"):
            sd.predict(np.zeros((5, 2)))

    def test_get_centroids_without_fit_raises(self):
        sd = StateDiscovery(method="kmeans", n_states=4)
        with pytest.raises(RuntimeError, match="not been fitted"):
            sd.get_centroids()

    def test_get_probabilities_gmm(self, sample_data_2d):
        X, _ = sample_data_2d
        sd = StateDiscovery(method="gmm", n_states=4, random_state=42)
        sd.fit(X)
        probs = sd.get_probabilities(X)
        assert probs.shape == (400, 4)
        np.testing.assert_allclose(probs.sum(axis=1), np.ones(400), rtol=1e-5)

    def test_get_probabilities_kmeans(self, sample_data_2d):
        X, _ = sample_data_2d
        sd = StateDiscovery(method="kmeans", n_states=4, random_state=42)
        sd.fit(X)
        probs = sd.get_probabilities(X)
        assert probs.shape == (400, 4)
        np.testing.assert_allclose(probs.sum(axis=1), np.ones(400), rtol=1e-5)

    def test_get_model(self, sample_data_2d):
        X, _ = sample_data_2d
        sd = StateDiscovery(method="kmeans", n_states=4, random_state=42)
        sd.fit(X)
        model = sd.get_model()
        assert model is not None

    def test_get_labels(self, sample_data_2d):
        X, _ = sample_data_2d
        sd = StateDiscovery(method="kmeans", n_states=4, random_state=42)
        sd.fit(X)
        labels = sd.get_labels()
        assert labels.shape == (400,)

    def test_get_labels_without_fit_raises(self):
        sd = StateDiscovery(method="kmeans", n_states=4)
        with pytest.raises(RuntimeError, match="not been fitted"):
            sd.get_labels()

    def test_invalid_method(self):
        with pytest.raises(ValueError, match="Unknown method"):
            StateDiscovery(method="invalid", n_states=4)

    def test_n_states_1(self, sample_data_2d):
        """Edge case: n_states=1 should still work for kmeans."""
        X, _ = sample_data_2d
        sd = StateDiscovery(method="kmeans", n_states=1, random_state=42)
        labels = sd.fit_predict(X)
        assert len(np.unique(labels)) == 1

    def test_high_dim_data(self, sample_data_highdim):
        X, _ = sample_data_highdim
        sd = StateDiscovery(method="kmeans", n_states=3, random_state=42)
        labels = sd.fit_predict(X)
        assert labels.shape == (150,)

    def test_softmax_dist(self):
        centroids = np.array([[0.0, 0.0], [5.0, 5.0]])
        X = np.array([[0.1, 0.1], [5.0, 5.0]])
        probs = _softmax_dist(X, centroids, temperature=1.0)
        assert probs.shape == (2, 2)
        np.testing.assert_allclose(probs.sum(axis=1), np.ones(2), rtol=1e-5)
        assert probs[0, 0] > probs[0, 1]  # closest to centroid 0
        assert probs[1, 1] > probs[1, 0]  # closest to centroid 1


# ======================================================================
# StateAssignment tests
# ======================================================================


class TestStateAssignment:
    """Hard / soft / hybrid / proportions correctness."""

    def test_hard_assign(self, sample_centroids):
        X = np.array([[0.1, 0.1], [4.9, 0.1], [0.1, 4.9], [5.0, 5.0]])
        labels = StateAssignment.hard_assign(X, sample_centroids)
        assert labels.shape == (4,)
        np.testing.assert_array_equal(labels, [0, 1, 2, 3])

    def test_hard_assign_different_metric(self):
        centroids = np.array([[0.0, 0.0], [1.0, 0.0]])
        X = np.array([[0.0, 0.0], [0.0, 5.0]])  # 2nd has large y offset
        labels = StateAssignment.hard_assign(X, centroids, metric="euclidean")
        assert labels[0] == 0
        # second point should be closer to centroid 0 in x, but y dominates
        # both centroids have y=0, so point (0,5) is equally distant from both
        # actually (0,5) dist to c0=5, to c1≈5.099, so labels[1] should be 0

    def test_soft_assign_row_sum(self, sample_centroids):
        X = np.array([[2.5, 2.5], [-1.0, -1.0]])
        weights = StateAssignment.soft_assign(X, sample_centroids, temperature=1.0)
        assert weights.shape == (2, 4)
        np.testing.assert_allclose(weights.sum(axis=1), np.ones(2), rtol=1e-5)

    def test_soft_assign_temperature_effect(self, sample_centroids):
        """Higher temperature produces more uniform assignments."""
        # Use a point close to one centroid to show temperature effect
        X = np.array([[0.1, 0.1]])
        w_low = StateAssignment.soft_assign(X, sample_centroids, temperature=0.1)
        w_high = StateAssignment.soft_assign(X, sample_centroids, temperature=10.0)
        # Low temp: sharp distribution (max close to 1), high temp: more uniform
        assert w_low.max() > w_high.max()

    def test_soft_assign_gmm(self):
        rng = np.random.default_rng(42)
        means = np.array([[0.0, 0.0], [5.0, 5.0]])
        covariances = np.array([[[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]]])
        weights = np.array([0.6, 0.4])
        X = np.array([[0.1, 0.1], [5.0, 5.0], [2.5, 2.5]])
        probs = StateAssignment.soft_assign_gmm(X, means, covariances, weights)
        assert probs.shape == (3, 2)
        np.testing.assert_allclose(probs.sum(axis=1), np.ones(3), rtol=1e-5)

    def test_hybrid_assign(self, sample_centroids):
        """Confident samples get hard labels; less confident may not."""
        # Points very close to centroids are confident
        X = np.array([[0.0, 0.0], [5.0, 5.0], [2.5, 2.5]])
        hard, soft, mask = StateAssignment.hybrid_assign(
            X, sample_centroids, hard_threshold=0.8, temperature=1.0
        )
        assert hard.shape == (3,)
        assert soft.shape == (3, 4)
        assert mask.shape == (3,)
        assert mask.dtype == bool

    def test_state_proportions(self):
        assignment = np.array([0, 0, 0, 1, 1, 2, 2, 2, 2, 2])
        props = StateAssignment.state_proportions(assignment, n_states=3)
        np.testing.assert_allclose(props, [0.3, 0.2, 0.5])

    def test_state_proportions_empty_state(self):
        assignment = np.array([0, 0, 0])
        props = StateAssignment.state_proportions(assignment, n_states=4)
        assert props[3] == 0.0

    def test_hard_assign_empty(self):
        labels = StateAssignment.hard_assign(
            np.empty((0, 2)), np.array([[0.0, 0.0]])
        )
        assert labels.shape == (0,)


# ======================================================================
# StateMetrics tests
# ======================================================================


class TestStateMetrics:
    """Silhouette, Davies-Bouldin, purity, stability, suggest_n_states."""

    def test_silhouette(self, sample_data_2d):
        X, y = sample_data_2d
        score = StateMetrics.silhouette(X, y)
        assert isinstance(score, float)
        assert -1.0 <= score <= 1.0
        # Well-separated clusters should have high silhouette
        assert score > 0.5, f"Expected >0.5, got {score}"

    def test_silhouette_single_cluster(self, sample_data_single_cluster):
        X, y = sample_data_single_cluster
        score = StateMetrics.silhouette(X, y)
        assert score == 0.0  # single unique label -> 0.0

    def test_davies_bouldin(self, sample_data_2d):
        X, y = sample_data_2d
        score = StateMetrics.davies_bouldin(X, y)
        assert isinstance(score, float)
        assert score >= 0.0
        # Well-separated clusters should have low DB
        assert score < 1.0, f"Expected <1.0, got {score}"

    def test_davies_bouldin_single_cluster(self, sample_data_single_cluster):
        X, y = sample_data_single_cluster
        score = StateMetrics.davies_bouldin(X, y)
        assert score == 0.0

    def test_state_purity_perfect(self):
        labels = np.array([0, 0, 1, 1, 2, 2])
        true = np.array([0, 0, 1, 1, 2, 2])
        purity = StateMetrics.state_purity(
            labels_pred=labels, labels_true=true
        )
        assert purity == 1.0

    def test_state_purity_imperfect(self):
        labels = np.array([0, 0, 0, 1, 1, 1])
        true = np.array([0, 0, 1, 1, 1, 1])
        purity = StateMetrics.state_purity(
            labels_pred=labels, labels_true=true
        )
        assert 0.0 < purity < 1.0

    def test_state_purity_alias_support(self):
        labels = np.array([0, 0, 1, 1])
        true = np.array([0, 0, 1, 1])
        # Using the (labels, true_labels) alias
        purity = StateMetrics.state_purity(labels=labels, true_labels=true)
        assert purity == 1.0

    def test_state_purity_missing_args(self):
        with pytest.raises(ValueError, match="Provide either"):
            StateMetrics.state_purity()

    def test_state_purity_length_mismatch(self):
        with pytest.raises(ValueError, match="Length mismatch"):
            StateMetrics.state_purity(
                labels_pred=np.array([0, 0, 1]),
                labels_true=np.array([0, 1]),
            )

    def test_state_stability(self):
        l1 = np.array([0, 0, 1, 1, 2, 2])
        l2 = np.array([0, 0, 1, 1, 2, 2])
        ari = StateMetrics.state_stability(labels1=l1, labels2=l2)
        assert ari == 1.0

    def test_state_stability_imperfect(self):
        l1 = np.array([0, 0, 1, 1])
        l2 = np.array([0, 1, 0, 1])
        ari = StateMetrics.state_stability(labels1=l1, labels2=l2)
        assert isinstance(ari, float)

    def test_state_stability_missing_args(self):
        with pytest.raises(ValueError, match="must be provided"):
            StateMetrics.state_stability(labels1=np.array([0, 1]))

    def test_suggest_n_states_silhouette(self, sample_data_2d):
        X, _ = sample_data_2d
        best_k = StateMetrics.suggest_n_states(
            X, max_k=8, method="silhouette", random_state=42
        )
        # With 4 well-separated clusters, should suggest 4
        assert best_k == 4, f"Expected 4, got {best_k}"

    def test_suggest_n_states_davies_bouldin(self, sample_data_2d):
        X, _ = sample_data_2d
        best_k = StateMetrics.suggest_n_states(
            X, max_k=8, method="davies_bouldin", random_state=42
        )
        assert best_k == 4, f"Expected 4, got {best_k}"

    def test_suggest_n_states_invalid_method(self, sample_data_2d):
        X, _ = sample_data_2d
        with pytest.raises(ValueError, match="Unknown method"):
            StateMetrics.suggest_n_states(X, max_k=5, method="invalid")

    def test_evaluate_all(self, sample_data_2d):
        X, y = sample_data_2d
        results = StateMetrics.evaluate_all(X, y, true_labels=y)
        assert "silhouette" in results
        assert "davies_bouldin" in results
        assert "purity" in results
        assert "nmi" in results
        assert "ari" in results
        assert "n_states" in results
        assert results["purity"] == 1.0
        assert results["n_states"] == 4.0

    def test_evaluate_all_no_true_labels(self, sample_data_2d):
        X, y = sample_data_2d
        results = StateMetrics.evaluate_all(X, y, true_labels=None)
        assert "silhouette" in results
        assert "purity" not in results
        assert "nmi" not in results
