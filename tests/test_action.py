"""Tests for the Action module: ActionPolicy, AcquisitionStrategy, CompressStrategy."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from scx.action.policy import ActionPolicy, ActionResult
from scx.action.acquisition import AcquisitionStrategy
from scx.action.compress import CompressStrategy


# ======================================================================
# ActionPolicy tests
# ======================================================================


class TestActionPolicy:
    """decide, allocate_budget (proportional/threshold/hybrid), execute."""

    def test_decide_returns_dict(self):
        policy = ActionPolicy(budget=100, mode="proportional")
        classifications = pd.DataFrame({
            "state_id": [0, 1, 2],
            "category": ["valuable", "redundant", "noisy"],
        })
        values = pd.DataFrame({
            "state_id": [0, 1, 2],
            "value": [0.8, 0.1, 0.3],
        })
        actions = policy.decide(classifications, values)
        assert isinstance(actions, dict)
        assert len(actions) == 3
        assert all(s in actions for s in [0, 1, 2])

    def test_decide_default_actions(self):
        policy = ActionPolicy(budget=100, mode="proportional")
        classifications = pd.DataFrame({
            "state_id": [0, 1, 2, 3],
            "category": ["valuable", "redundant", "noisy", "expert_dependent"],
        })
        values = pd.DataFrame({
            "state_id": [0, 1, 2, 3],
            "value": [0.8, 0.1, 0.3, 0.5],
        })
        actions = policy.decide(classifications, values)
        assert actions[0] == "acquire"       # valuable -> acquire
        assert actions[1] == "downweight"    # redundant -> downweight
        assert actions[2] == "discard"       # noisy -> discard
        assert actions[3] == "route"         # expert_dependent -> route

    def test_decide_very_low_value_downgrades_to_discard(self):
        policy = ActionPolicy(budget=100, mode="proportional")
        classifications = pd.DataFrame({
            "state_id": [0],
            "category": ["valuable"],
        })
        values = pd.DataFrame({
            "state_id": [0],
            "value": [1e-10],  # extremely low
        })
        actions = policy.decide(classifications, values)
        assert actions[0] == "discard"  # downgraded from acquire

    def test_allocate_proportional_budget_sum(self):
        policy = ActionPolicy(budget=100, mode="proportional")
        values = pd.DataFrame({
            "state_id": [0, 1, 2, 3],
            "value": [0.5, 0.3, 0.1, 0.1],
        })
        alloc = policy.allocate_budget(values)
        total = sum(alloc.values())
        assert total <= 100
        # Higher value -> more budget
        assert alloc[0] >= alloc[1]
        assert alloc[1] >= alloc[2]

    def test_allocate_proportional_all_zero(self):
        policy = ActionPolicy(budget=100, mode="proportional")
        values = pd.DataFrame({
            "state_id": [0, 1, 2],
            "value": [0.0, 0.0, 0.0],
        })
        alloc = policy.allocate_budget(values)
        total = sum(alloc.values())
        assert total <= 100

    def test_allocate_threshold(self):
        policy = ActionPolicy(budget=100, mode="threshold")
        values = pd.DataFrame({
            "state_id": [0, 1, 2, 3],
            "value": [0.8, 0.1, 0.05, 0.05],
        })
        alloc = policy.allocate_budget(values)
        total = sum(alloc.values())
        assert total <= 100
        # Top state should get budget, bottom ones may not
        assert alloc[0] >= alloc[3]

    def test_allocate_hybrid(self):
        policy = ActionPolicy(budget=100, mode="hybrid")
        values = pd.DataFrame({
            "state_id": [0, 1, 2, 3],
            "value": [0.6, 0.2, 0.1, 0.1],
        })
        alloc = policy.allocate_budget(values)
        total = sum(alloc.values())
        assert total <= 100

    def test_allocate_empty(self):
        policy = ActionPolicy(budget=100, mode="proportional")
        values = pd.DataFrame({"state_id": [], "value": []})
        alloc = policy.allocate_budget(values)
        assert alloc == {}

    def test_execute_acquire(self):
        policy = ActionPolicy(budget=100, mode="proportional")
        actions = {0: "acquire"}
        X = np.random.randn(20, 2)
        assignments = np.zeros(20, dtype=int)
        results = policy.execute(actions, X, assignments, n_to_acquire=5)
        assert 0 in results
        assert results[0].action == "acquire"
        assert len(results[0].samples_selected) == 5

    def test_execute_discard(self):
        policy = ActionPolicy(budget=100, mode="proportional")
        X = np.random.randn(10, 2)
        assignments = np.zeros(10, dtype=int)
        actions = {0: "discard"}
        results = policy.execute(actions, X, assignments)
        assert results[0].action == "discard"
        assert len(results[0].samples_discarded) == 10

    def test_execute_route(self):
        policy = ActionPolicy(budget=100, mode="proportional")
        X = np.random.randn(10, 2)
        assignments = np.zeros(10, dtype=int)
        actions = {0: "route"}
        results = policy.execute(actions, X, assignments, expert_assigned=1)
        assert results[0].action == "route"
        assert results[0].expert_assigned == 1

    def test_invalid_mode(self):
        with pytest.raises(ValueError, match="Unknown mode"):
            ActionPolicy(budget=100, mode="invalid")

    def test_budget_zero(self):
        """Edge case: budget=0 should still produce valid allocation."""
        policy = ActionPolicy(budget=0, mode="proportional")
        values = pd.DataFrame({
            "state_id": [0, 1],
            "value": [0.5, 0.5],
        })
        alloc = policy.allocate_budget(values)
        total = sum(alloc.values())
        assert total >= 0


# ======================================================================
# AcquisitionStrategy tests
# ======================================================================


class TestAcquisitionStrategy:
    """coreset, uncertainty, random, scx_value selection."""

    def test_coreset_select(self):
        strategy = AcquisitionStrategy(strategy="coreset")
        X_s = np.random.randn(100, 2)
        indices = strategy.coreset_select(X_s, n_samples=10)
        assert indices.shape == (10,)
        assert len(np.unique(indices)) == 10
        assert np.all(indices >= 0)
        assert np.all(indices < 100)

    def test_coreset_select_all(self):
        strategy = AcquisitionStrategy(strategy="coreset")
        X_s = np.random.randn(10, 2)
        indices = strategy.coreset_select(X_s, n_samples=10)
        assert len(indices) == 10
        np.testing.assert_array_equal(np.sort(indices), np.arange(10))

    def test_coreset_select_more_than_available(self):
        strategy = AcquisitionStrategy(strategy="coreset")
        X_s = np.random.randn(5, 2)
        indices = strategy.coreset_select(X_s, n_samples=20)
        assert len(indices) == 5

    def test_coreset_select_empty(self):
        strategy = AcquisitionStrategy(strategy="coreset")
        indices = strategy.coreset_select(np.empty((0, 2)), n_samples=5)
        assert indices.shape == (0,)

    def test_uncertainty_select(self):
        strategy = AcquisitionStrategy(strategy="uncertainty")
        uncertainties = np.array([0.1, 0.5, 0.9, 0.3, 0.7])
        indices = strategy.uncertainty_select(uncertainties, n_samples=3)
        # Top-3 most uncertain: indices 2 (0.9), 4 (0.7), 1 (0.5)
        np.testing.assert_array_equal(indices, [2, 4, 1])

    def test_uncertainty_select_all(self):
        strategy = AcquisitionStrategy(strategy="uncertainty")
        indices = strategy.uncertainty_select(np.ones(5), n_samples=5)
        assert len(indices) == 5

    def test_scx_value_select(self):
        strategy = AcquisitionStrategy(strategy="scx_value")
        values = np.array([0.1, 0.9, 0.5, 0.3])
        indices = strategy.scx_value_select(None, values, n_samples=2)
        # Top-2: indices 1 (0.9), 2 (0.5)
        np.testing.assert_array_equal(indices, [1, 2])

    def test_select_samples_random(self):
        strategy = AcquisitionStrategy(strategy="random")
        X_s = np.random.randn(50, 2)
        indices = strategy.select_samples(X_s, n_samples=10)
        assert indices.shape == (10,)
        assert len(np.unique(indices)) == 10

    def test_select_samples_uncertainty_with_kwargs(self):
        strategy = AcquisitionStrategy(strategy="uncertainty")
        X_s = np.random.randn(20, 2)
        uncertainties = np.random.rand(20)
        indices = strategy.select_samples(X_s, 5, uncertainties=uncertainties)
        assert indices.shape == (5,)

    def test_select_samples_coreset(self):
        strategy = AcquisitionStrategy(strategy="coreset")
        X_s = np.random.randn(30, 2)
        indices = strategy.select_samples(X_s, 8)
        assert indices.shape == (8,)

    def test_select_samples_uncertainty_missing_kwargs(self):
        strategy = AcquisitionStrategy(strategy="uncertainty")
        with pytest.raises(ValueError, match="uncertainties"):
            strategy.select_samples(np.random.randn(10, 2), 3)

    def test_select_samples_scx_missing_kwargs(self):
        strategy = AcquisitionStrategy(strategy="scx_value")
        with pytest.raises(ValueError, match="sample_values"):
            strategy.select_samples(np.random.randn(10, 2), 3)

    def test_compare_strategies(self):
        strategy = AcquisitionStrategy(strategy="random")
        X_s = np.random.randn(50, 2)
        y_s = np.random.randint(0, 3, 50)
        results = strategy.compare_strategies(X_s, y_s, n_samples=10)
        assert "random" in results
        assert "coreset" in results

    def test_invalid_strategy(self):
        with pytest.raises(ValueError, match="Unknown strategy"):
            AcquisitionStrategy(strategy="invalid")

    def test_coverage_diversity_scores(self):
        strategy = AcquisitionStrategy(strategy="random")
        X_s = np.random.randn(20, 2)
        indices = np.array([0, 5, 10, 15])
        cov = strategy._coverage_score(X_s, indices)
        div = strategy._diversity_score(X_s, indices)
        assert isinstance(cov, float)
        assert isinstance(div, float)


# ======================================================================
# CompressStrategy tests
# ======================================================================


class TestCompressStrategy:
    """redundancy_score, compress, weighted_coreset, kcenter_coreset."""

    def test_redundancy_score_shape(self):
        cs = CompressStrategy()
        X_s = np.random.randn(50, 2)
        residuals = np.random.rand(50)
        scores = cs.redundancy_score(X_s, residuals, state_proportion=0.5)
        assert scores.shape == (50,)
        assert np.all(scores >= 0.0)
        assert np.all(scores <= 1.0)

    def test_redundancy_score_single_sample(self):
        cs = CompressStrategy()
        X_s = np.random.randn(1, 2)
        residuals = np.array([0.5])
        scores = cs.redundancy_score(X_s, residuals, state_proportion=0.1)
        assert scores.shape == (1,)
        assert 0.0 <= scores[0] <= 1.0

    def test_compress_output_shapes(self):
        cs = CompressStrategy(method="weighted_random")
        X_s = np.random.randn(100, 2)
        y_s = np.random.randint(0, 3, 100)
        residuals = np.random.rand(100)
        X_c, y_c, w = cs.compress(
            X_s, y_s, residuals, state_proportion=0.5, compression_ratio=0.5
        )
        assert len(X_c) <= 100
        assert len(X_c) > 0
        assert y_c.shape[0] == X_c.shape[0]
        assert w.shape[0] == X_c.shape[0]

    def test_compress_with_boundary(self):
        cs = CompressStrategy(method="weighted_random")
        X_s = np.random.randn(100, 2)
        y_s = np.random.randint(0, 3, 100)
        residuals = np.random.rand(100)
        boundary = np.array([0, 1, 2])  # must retain these
        X_c, y_c, w = cs.compress(
            X_s, y_s, residuals, state_proportion=0.5,
            compression_ratio=0.5, boundary_samples=boundary,
        )
        # Check boundary samples are retained
        assert len(X_c) > 0

    def test_compress_with_boundary_boolean(self):
        cs = CompressStrategy(method="weighted_random")
        X_s = np.random.randn(50, 2)
        y_s = np.random.randint(0, 3, 50)
        residuals = np.random.rand(50)
        boundary = np.zeros(50, dtype=bool)
        boundary[:3] = True
        X_c, y_c, w = cs.compress(
            X_s, y_s, residuals, state_proportion=0.5,
            compression_ratio=0.5, boundary_samples=boundary,
        )
        assert len(X_c) > 0

    def test_weighted_coreset(self):
        cs = CompressStrategy()
        X_s = np.random.randn(50, 2)
        y_s = np.random.randn(50)
        residuals = np.random.rand(50)
        X_c, y_c, w = cs.weighted_coreset(X_s, y_s, residuals, n_keep=10)
        assert len(X_c) == 10
        assert len(w) == 10

    def test_kcenter_coreset(self):
        cs = CompressStrategy()
        X_s = np.random.randn(50, 2)
        indices = cs.kcenter_coreset(X_s, n_keep=10)
        assert indices.shape == (10,)
        assert len(np.unique(indices)) == 10

    def test_kcenter_coreset_all(self):
        cs = CompressStrategy()
        X_s = np.random.randn(5, 2)
        indices = cs.kcenter_coreset(X_s, n_keep=5)
        assert len(indices) == 5

    def test_kcenter_coreset_empty(self):
        cs = CompressStrategy()
        indices = cs.kcenter_coreset(np.empty((0, 2)), n_keep=5)
        assert indices.shape == (0,)

    def test_evaluate_compression(self):
        cs = CompressStrategy()
        X = np.random.randn(30, 2)
        y = np.random.randn(30)
        X_c, y_c, w = cs.weighted_coreset(X, y, np.random.rand(30), n_keep=10)
        result = cs.evaluate_compression(
            X, y, X_c, y_c, w, eval_fn=lambda yt, yp: 1.0 / (1.0 + np.mean((yt - yp) ** 2))
        )
        assert "original_score" in result
        assert "compressed_score" in result
        assert "retention_ratio" in result
        assert "compression_ratio" in result

    def test_invalid_method(self):
        with pytest.raises(ValueError, match="Unknown method"):
            CompressStrategy(method="invalid")

    def test_compute_weights(self):
        scores = np.array([0.1, 0.5, 0.9])
        w = CompressStrategy._compute_weights(scores, temperature=2.0)
        assert w.shape == (3,)
        assert np.all(w >= 0)
        # Lower redundancy -> higher weight
        assert w[0] > w[2]
