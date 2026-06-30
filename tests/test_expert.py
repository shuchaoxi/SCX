"""Tests for the Expert module: ExpertRegistry, ExpertReliability, ExpertRouter, ExpertConflict."""

from __future__ import annotations

import numpy as np
import pytest

from scx.expert.registry import ExpertInfo, ExpertRegistry
from scx.expert.reliability import ExpertReliability
from scx.expert.router import ExpertRouter
from scx.expert.conflict import ExpertConflict


# ======================================================================
# ExpertRegistry tests
# ======================================================================


class TestExpertRegistry:
    """Register, unregister, get, list, predict_all, edge cases."""

    def test_register_and_get(self):
        reg = ExpertRegistry()
        eid = reg.register("linear", lambda x: x.sum(axis=1), cost=0.5, type="simple")
        info = reg.get(eid)
        assert info.name == "linear"
        assert info.cost == 0.5
        assert info.metadata == {"type": "simple"}
        assert callable(info.predict_fn)

    def test_register_auto_id_increment(self):
        reg = ExpertRegistry()
        e1 = reg.register("a", lambda x: x[:, 0])
        e2 = reg.register("b", lambda x: x[:, 0])
        assert e2 == e1 + 1

    def test_len(self):
        reg = ExpertRegistry()
        assert len(reg) == 0
        reg.register("a", lambda x: x[:, 0])
        reg.register("b", lambda x: x[:, 0])
        assert len(reg) == 2

    def test_unregister(self):
        reg = ExpertRegistry()
        eid = reg.register("a", lambda x: x[:, 0])
        reg.unregister(eid)
        with pytest.raises(KeyError):
            reg.get(eid)
        assert len(reg) == 0

    def test_unregister_nonexistent_raises(self):
        reg = ExpertRegistry()
        with pytest.raises(KeyError, match="not found"):
            reg.unregister(999)

    def test_get_nonexistent_raises(self):
        reg = ExpertRegistry()
        with pytest.raises(KeyError, match="not found"):
            reg.get(999)

    def test_list(self):
        reg = ExpertRegistry()
        reg.register("a", lambda x: x[:, 0])
        reg.register("b", lambda x: x[:, 1])
        experts = reg.list()
        assert len(experts) == 2
        assert all(isinstance(e, ExpertInfo) for e in experts)

    def test_predict_all_shape(self):
        reg = ExpertRegistry()
        reg.register("a", lambda x: x.sum(axis=1))
        reg.register("b", lambda x: x.mean(axis=1))
        reg.register("c", lambda x: x[:, 0])
        X = np.random.randn(5, 4)
        preds = reg.predict_all(X)
        assert preds.shape == (3, 5)

    def test_predict_all_empty_registry_raises(self):
        reg = ExpertRegistry()
        with pytest.raises(RuntimeError, match="No experts registered"):
            reg.predict_all(np.zeros((3, 2)))

    def test_predict_all_multi_output(self):
        reg = ExpertRegistry()
        reg.register("a", lambda x: np.column_stack([x[:, 0], x[:, 1]]))
        X = np.random.randn(5, 4)
        preds = reg.predict_all(X)
        # Each expert output shape (5, 2) -> stacked (1, 5, 2)
        assert preds.shape == (1, 5, 2)

    def test_repr(self):
        reg = ExpertRegistry()
        reg.register("linear", lambda x: x[:, 0])
        rep = repr(reg)
        assert "ExpertRegistry" in rep
        assert "linear" in rep

    def test_metadata_default_empty(self):
        reg = ExpertRegistry()
        eid = reg.register("a", lambda x: x[:, 0])
        assert reg.get(eid).metadata == {}


# ======================================================================
# ExpertReliability tests
# ======================================================================


class TestExpertReliability:
    """Supervised / unsupervised / hybrid / bayesian estimation."""

    @pytest.fixture
    def reg(self):
        r = ExpertRegistry()
        r.register("a", lambda x: x[:, 0], cost=0.5)
        r.register("b", lambda x: x[:, 1], cost=1.0)
        r.register("c", lambda x: x.sum(axis=1) * 0.5, cost=1.5)
        return r

    @pytest.fixture
    def X(self):
        return np.random.randn(10, 4)

    @pytest.fixture
    def y(self):
        return np.random.randn(10)

    @pytest.fixture
    def assignments(self):
        return np.array([0, 0, 0, 0, 1, 1, 1, 2, 2, 2])

    def test_supervised_output_shapes(self, reg, X, y, assignments):
        rel = ExpertReliability(method="supervised")
        res = rel.estimate(reg, X, y, assignments, n_states=3)
        assert res["R_matrix"].shape == (3, 3)
        assert res["SCX_matrix"].shape == (3, 3)
        assert res["uncertainties"].shape == (3, 3)
        assert res["n_per_state"].shape == (3,)

    def test_supervised_no_nan(self, reg, X, y, assignments):
        rel = ExpertReliability(method="supervised", min_samples=1)
        res = rel.estimate(reg, X, y, assignments, n_states=3)
        assert not np.any(np.isnan(res["R_matrix"]))
        assert not np.any(np.isnan(res["SCX_matrix"]))

    def test_unsupervised_output_shapes(self, reg, X, assignments):
        rel = ExpertReliability(method="unsupervised")
        res = rel.estimate(reg, X, None, assignments, n_states=3)
        assert res["R_matrix"].shape == (3, 3)
        assert res["SCX_matrix"].shape == (3, 3)

    def test_unsupervised_scores_in_range(self, reg, X, assignments):
        rel = ExpertReliability(method="unsupervised")
        res = rel.estimate(reg, X, None, assignments, n_states=3)
        assert np.all((res["R_matrix"] >= 0) | np.isnan(res["R_matrix"]))
        assert np.all(res["SCX_matrix"][~np.isnan(res["SCX_matrix"])] <= 1.0)

    def test_hybrid_output_shapes(self, reg, X, y, assignments):
        rel = ExpertReliability(method="hybrid")
        res = rel.estimate(reg, X, y, assignments, n_states=3)
        assert res["R_matrix"].shape == (3, 3)

    def test_hybrid_falls_back_to_unsupervised(self, reg, X, assignments):
        rel = ExpertReliability(method="hybrid")
        res = rel.estimate(reg, X, None, assignments, n_states=3)
        assert res["R_matrix"].shape == (3, 3)

    def test_bayesian_output_shapes(self, reg, X, y, assignments):
        rel = ExpertReliability(method="bayesian")
        res = rel.estimate(reg, X, y, assignments, n_states=3)
        assert res["R_matrix"].shape == (3, 3)

    def test_bayesian_shrinkage(self, reg, X, y, assignments):
        """Bayesian method should not produce NaN anywhere."""
        rel = ExpertReliability(method="bayesian", min_samples=2)
        res = rel.estimate(reg, X, y, assignments, n_states=3)
        assert not np.any(np.isnan(res["R_matrix"]))

    def test_compute_scx_from_risk(self):
        risk = np.array([[0.0, 0.5], [0.3, 0.2]])
        scx = ExpertReliability.compute_scx_from_risk(risk)
        assert scx.shape == (2, 2)
        assert np.all(scx > 0)
        assert np.all(scx <= 1.0)

    def test_invalid_method_raises(self):
        with pytest.raises(ValueError, match="Unknown method"):
            ExpertReliability(method="invalid")

    def test_custom_loss_fn(self, reg, X, y, assignments):
        rel = ExpertReliability(
            method="supervised",
            loss_fn=lambda yp, yt: np.abs(yp - yt),
        )
        res = rel.estimate(reg, X, y, assignments, n_states=3)
        assert res["R_matrix"].shape == (3, 3)

    def test_small_state_shrinkage(self, reg, X, y):
        """States with fewer samples than min_samples trigger shrinkage."""
        assignments = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
        rel = ExpertReliability(method="supervised", min_samples=5)
        res = rel.estimate(reg, X, y, assignments, n_states=2)
        # State 1 has only 2 samples (< min_samples) -> should have NaN or shrunk
        # But with min_samples=5, state 1 will trigger shrinkage
        assert not np.any(np.isnan(res["R_matrix"]))

    def test_unsupervised_single_expert(self):
        """Single expert: no disagreement -> R=0, SCX=1."""
        reg = ExpertRegistry()
        reg.register("only", lambda x: x[:, 0])
        X = np.random.randn(20, 4)
        assignments = np.array([0]*6 + [1]*7 + [2]*7)  # >= min_samples=5 each
        rel = ExpertReliability(method="unsupervised", min_samples=1)
        res = rel.estimate(reg, X, None, assignments, n_states=3)
        # With 1 expert, mean_pred == expert's pred so deviation = 0
        # R = min(1.0, 0/(0+1)) = 0, SCX = 1 - tanh(0/alpha) = 1
        assert np.allclose(res["R_matrix"], 0.0)
        assert np.allclose(res["SCX_matrix"], 1.0)

    def test_tau_custom(self, reg, X, y, assignments):
        rel = ExpertReliability(method="supervised", tau=0.5)
        res = rel.estimate(reg, X, y, assignments, n_states=3)
        assert res["SCX_matrix"].shape == (3, 3)

    def test_update_not_implemented(self, reg, X, y):
        rel = ExpertReliability(method="supervised")
        assignments = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])
        with pytest.raises(NotImplementedError):
            rel.update(X, y, assignments)


# ======================================================================
# ExpertRouter tests
# ======================================================================


class TestExpertRouter:
    """Hard routing, soft weights (row sum=1), ensemble, cost-sensitive."""

    @pytest.fixture
    def reg(self):
        r = ExpertRegistry()
        r.register("a", lambda x: x[:, 0], cost=0.5)
        r.register("b", lambda x: x[:, 1], cost=2.0)
        r.register("c", lambda x: x.sum(axis=1), cost=1.0)
        return r

    @pytest.fixture
    def X(self):
        return np.random.randn(10, 4)

    @pytest.fixture
    def assignments(self):
        return np.array([0, 0, 0, 0, 1, 1, 1, 2, 2, 2])

    @pytest.fixture
    def R(self):
        """Risk matrix: each state has a different best expert."""
        Rmat = np.array([
            [0.1, 0.5, 0.8],  # expert 0: good for state 0
            [0.5, 0.1, 0.5],  # expert 1: good for state 1
            [0.5, 0.5, 0.1],  # expert 2: good for state 2
        ])
        return Rmat

    def test_hard_route_shape(self, reg, X, assignments, R):
        router = ExpertRouter(reg)
        assigned = router.route_hard(X, assignments, R)
        assert assigned.shape == (10,)
        assert all(a in [info.id for info in reg.list()] for a in assigned)

    def test_hard_route_argmin(self, reg, X, assignments, R):
        """State 0 should route to expert 0 (R=0.1), state 1 to expert 1, etc."""
        router = ExpertRouter(reg)
        assigned = router.route_hard(X, assignments, R)
        eids = [info.id for info in reg.list()]
        # Samples in state 0 should get eids[0]
        assert np.all(assigned[assignments == 0] == eids[0])
        # Samples in state 1 should get eids[1]
        assert np.all(assigned[assignments == 1] == eids[1])

    def test_route_weighted_shape(self, reg, X, assignments, R):
        router = ExpertRouter(reg)
        weights = router.route_weighted(X, assignments, R)
        assert weights.shape == (10, 3)

    def test_route_weighted_row_sum(self, reg, X, assignments, R):
        router = ExpertRouter(reg)
        weights = router.route_weighted(X, assignments, R)
        np.testing.assert_allclose(weights.sum(axis=1), np.ones(10), rtol=1e-5)

    def test_route_weighted_non_negative(self, reg, X, assignments, R):
        router = ExpertRouter(reg)
        weights = router.route_weighted(X, assignments, R)
        assert np.all(weights >= 0)

    def test_route_weighted_temperature_effect(self, reg, X, assignments, R):
        router = ExpertRouter(reg)
        w_low = router.route_weighted(X, assignments, R, temperature=0.1)
        w_high = router.route_weighted(X, assignments, R, temperature=10.0)
        # Low temp -> sharper distribution
        w_low_max = w_low.max(axis=1).mean()
        w_high_max = w_high.max(axis=1).mean()
        assert w_low_max > w_high_max

    def test_ensemble_predict_shape(self, reg, X, assignments, R):
        router = ExpertRouter(reg)
        preds = router.ensemble_predict(X, assignments, R)
        assert preds.shape == (10,)

    def test_cost_sensitive_route(self, reg, X, assignments, R):
        router = ExpertRouter(reg)
        assigned = router.route_cost_sensitive(X, assignments, R, lambda_cost=10.0)
        assert assigned.shape == (10,)
        # High lambda_cost favours low-cost expert
        low_cost_id = reg.get(0).id  # expert A has cost 0.5
        # With very high lambda, the cheapest expert costs dominate
        all_ids = [info.id for info in reg.list()]
        assert all(a in all_ids for a in assigned)

    def test_cost_sensitive_lambda_zero_equals_hard(self, reg, X, assignments, R):
        router = ExpertRouter(reg)
        hard = router.route_hard(X, assignments, R)
        cs = router.route_cost_sensitive(X, assignments, R, lambda_cost=0.0)
        np.testing.assert_array_equal(cs, hard)

    def test_router_repr(self, reg):
        router = ExpertRouter(reg)
        rep = repr(router)
        assert "ExpertRouter" in rep
        assert "3" in rep


# ======================================================================
# ExpertConflict tests
# ======================================================================


class TestExpertConflict:
    """detect, conflict_matrix, arbitrate, conflict_score, pairwise_disagreement."""

    @pytest.fixture
    def reg(self):
        r = ExpertRegistry()
        r.register("a", lambda x: x[:, 0], cost=0.5)
        r.register("b", lambda x: x[:, 1], cost=1.0)
        r.register("c", lambda x: x.sum(axis=1) * 0.5, cost=1.0)
        return r

    @pytest.fixture
    def X(self):
        return np.random.randn(10, 4)

    @pytest.fixture
    def assignments(self):
        return np.array([0, 0, 0, 0, 1, 1, 1, 2, 2, 2])

    @pytest.fixture
    def R(self):
        return np.ones((3, 3)) * 0.5

    def test_conflict_matrix_shape(self, reg, X, assignments):
        cm = ExpertConflict.conflict_matrix(X, reg, assignments, n_states=3)
        assert cm.shape == (3, 3, 3)

    def test_conflict_matrix_symmetric(self, reg, X, assignments):
        cm = ExpertConflict.conflict_matrix(X, reg, assignments, n_states=3)
        for k in range(3):
            assert np.allclose(cm[:, :, k], cm[:, :, k].T), f"State {k} not symmetric"

    def test_conflict_matrix_diagonal_zero(self, reg, X, assignments):
        cm = ExpertConflict.conflict_matrix(X, reg, assignments, n_states=3)
        for k in range(3):
            assert np.allclose(np.diag(cm[:, :, k]), 0.0), f"State {k} diagonal not zero"

    def test_conflict_score_range(self, reg, X):
        score = ExpertConflict.conflict_score(X, reg)
        assert 0.0 <= score <= 1.0

    def test_conflict_score_single_expert(self, X):
        reg = ExpertRegistry()
        reg.register("only", lambda x: x[:, 0])
        score = ExpertConflict.conflict_score(X, reg)
        assert score == 0.0

    def test_conflict_score_empty_x(self, reg):
        score = ExpertConflict.conflict_score(np.empty((0, 4)), reg)
        assert score == 0.0

    def test_detect(self, reg, X):
        result = ExpertConflict.detect(0, reg, X, threshold=0.1)
        assert isinstance(result, bool)

    def test_arbitrate_lowest_risk(self, reg, X, R):
        arb = ExpertConflict.arbitrate(X, reg, R, state_id=0, method="lowest_risk")
        assert arb in [info.id for info in reg.list()]

    def test_arbitrate_weighted_vote(self, reg, X, R):
        arb = ExpertConflict.arbitrate(X, reg, R, state_id=0, method="weighted_vote")
        assert arb == -1

    def test_arbitrate_average(self, reg, X, R):
        arb = ExpertConflict.arbitrate(X, reg, R, state_id=0, method="average")
        assert arb == -1

    def test_arbitrate_invalid_method(self, reg, X, R):
        with pytest.raises(ValueError, match="Unknown arbitrate method"):
            ExpertConflict.arbitrate(X, reg, R, state_id=0, method="invalid")

    def test_pairwise_disagreement(self, reg, X):
        preds = reg.predict_all(X)
        D = ExpertConflict.pairwise_disagreement(preds)
        assert D.shape == (3, 3)
        assert np.allclose(D, D.T)
        assert np.allclose(np.diag(D), 0.0)
        assert np.all(D >= 0)

    def test_identical_experts_no_conflict(self, identical_experts):
        reg = ExpertRegistry()
        reg.register("a", identical_experts[0])
        reg.register("b", identical_experts[1])
        X = np.random.randn(10, 2)
        score = ExpertConflict.conflict_score(X, reg)
        # Identical predictions -> near-zero disagreement
        assert score < 0.01
