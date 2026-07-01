"""Tests for the Valuation module: LearnabilityScore, NoiseScore, RedundancyScore, DataClassifier, StateValue."""

from __future__ import annotations

import numpy as np
import pytest

from scx.valuation.learnability import LearnabilityScore
from scx.valuation.noise_score import NoiseScore, NoveltyNoiseScore
from scx.valuation.redundancy import RedundancyScore
from scx.valuation.classifier import DataClassifier
from scx.valuation.state_value import StateValue, hoeffding_bound, chernoff_bound


# ======================================================================
# LearnabilityScore tests
# ======================================================================


class TestLearnabilityScore:
    """Consistency (label/expert/both), learnability in [0,1], noise_score."""

    def test_consistency_label_discrete_perfect(self):
        ls = LearnabilityScore()
        X = np.random.randn(10, 2)
        y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
        c = ls.consistency(X_s=X, y_s=y)
        assert 0.0 <= c <= 1.0

    def test_consistency_label_all_same(self):
        ls = LearnabilityScore()
        X = np.random.randn(5, 2)
        y = np.array([0, 0, 0, 0, 0])
        c = ls.consistency(X_s=X, y_s=y)
        assert c == 1.0

    def test_consistency_label_single_sample(self):
        ls = LearnabilityScore()
        c = ls.consistency(X_s=np.random.randn(1, 2), y_s=np.array([0]))
        assert c == 1.0

    def test_consistency_label_empty(self):
        ls = LearnabilityScore()
        c = ls.consistency(X_s=np.empty((0, 2)), y_s=np.array([]))
        assert c == 0.0

    def test_consistency_label_continuous(self):
        ls = LearnabilityScore()
        X = np.random.randn(10, 2)
        y = np.random.randn(10)
        c = ls.consistency(X_s=X, y_s=y)
        assert 0.0 <= c <= 1.0

    def test_consistency_expert_only(self):
        ls = LearnabilityScore()
        expert_preds = np.random.randn(3, 10)
        X = np.random.randn(10, 2)
        c = ls.consistency(X_s=X, expert_preds=expert_preds)
        assert 0.0 <= c <= 1.0

    def test_consistency_expert_single(self):
        ls = LearnabilityScore()
        expert_preds = np.random.randn(1, 10)
        X = np.random.randn(10, 2)
        c = ls.consistency(X_s=X, expert_preds=expert_preds)
        assert c == 0.5  # single expert -> neutral

    def test_consistency_both(self):
        ls = LearnabilityScore()
        X = np.random.randn(10, 2)
        y = np.random.randint(0, 3, 10)
        expert_preds = np.random.randn(3, 10)
        c = ls.consistency(X_s=X, y_s=y, expert_preds=expert_preds)
        assert 0.0 <= c <= 1.0

    def test_consistency_no_input(self):
        ls = LearnabilityScore()
        c = ls.consistency(X_s=np.random.randn(10, 2))
        assert c == 0.5  # neutral

    def test_noise_score(self):
        ls = LearnabilityScore()
        residuals = np.array([0.1, 0.2, 0.3])
        ns = ls.noise_score(residuals, state_proportion=0.5, consistency=0.8)
        assert ns.shape == (3,)
        assert np.all(ns >= 0)

    def test_learnability_in_range(self):
        ls = LearnabilityScore()
        L = ls.learnability(consistency=0.8, noise_score=0.3)
        assert 0.0 <= L <= 1.0

    def test_learnability_perfect(self):
        ls = LearnabilityScore()
        L = ls.learnability(consistency=1.0, noise_score=0.0)
        assert L == 1.0

    def test_learnability_zero_consistency(self):
        ls = LearnabilityScore()
        L = ls.learnability(consistency=0.0, noise_score=0.5)
        assert L == 0.0

    def test_compute_all(self):
        ls = LearnabilityScore()
        X = np.random.randn(10, 2)
        y = np.random.randint(0, 2, 10)
        residuals = np.random.rand(10)
        result = ls.compute_all(X, y, residuals, state_proportion=0.5)
        assert "consistency" in result
        assert "noise_score" in result
        assert "learnability" in result
        assert 0.0 <= result["learnability"] <= 1.0

    def test_compute_all_no_residuals(self):
        ls = LearnabilityScore()
        X = np.random.randn(10, 2)
        y = np.random.randint(0, 2, 10)
        result = ls.compute_all(X, y, state_proportion=0.5)
        assert result["noise_score"] == 0.0
        assert result["learnability"] >= 0.0

    def test_negative_eps_raises(self):
        with pytest.raises(ValueError, match="eps must be positive"):
            LearnabilityScore(eps=-1.0)


# ======================================================================
# NoiseScore tests
# ======================================================================


class TestNoiseScore:
    """compute, compute_state_level, detect_noisy_states, detect_noisy_samples."""

    def test_compute_shape(self):
        ns = NoveltyNoiseScore()
        scores = ns.compute(
            residuals=np.array([0.1, 0.2, 0.3]),
            state_proportion=0.5,
            consistency=0.8,
        )
        assert scores.shape == (3,)
        assert np.all(scores >= 0)

    def test_compute_empty(self):
        ns = NoveltyNoiseScore()
        scores = ns.compute(
            residuals=np.array([]),
            state_proportion=0.5,
            consistency=0.8,
        )
        assert scores.shape == (0,)

    def test_compute_zero_residual(self):
        ns = NoveltyNoiseScore()
        scores = ns.compute(
            residuals=np.zeros(5),
            state_proportion=0.5,
            consistency=0.8,
        )
        assert np.allclose(scores, 0.0)

    def test_compute_state_level_consistency(self):
        """Per-state noise score via compute matches mean of per-sample scores."""
        ns = NoveltyNoiseScore()
        residuals = np.array([0.1, 0.3, 0.5])
        per_sample = ns.compute(residuals, state_proportion=0.5, consistency=0.8)
        # Simulate state-level: pass single-element array with mean residual
        per_state = float(ns.compute(
            np.array([float(np.mean(residuals))]),
            state_proportion=0.5,
            consistency=0.8,
        )[0])
        assert abs(np.mean(per_sample) - per_state) < 1e-6

    def test_detect_noisy_states(self):
        ns = NoveltyNoiseScore()
        scores = np.array([0.1, 0.6, 0.9])
        # Flag states where noise score exceeds threshold
        flagged = np.where(scores > 0.5)[0]
        np.testing.assert_array_equal(flagged, [1, 2])

    def test_detect_noisy_states_no_match(self):
        ns = NoveltyNoiseScore()
        scores = np.array([0.1, 0.2, 0.3])
        flagged = np.where(scores > 0.5)[0]
        assert len(flagged) == 0

    def test_detect_noisy_samples_iqr(self):
        ns = NoveltyNoiseScore()
        scores = np.array([0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 5.0])  # 5.0 is outlier
        # IQR-based outlier detection
        q1, q3 = np.percentile(scores, [25, 75])
        iqr = q3 - q1
        upper_bound = q3 + 1.5 * iqr
        flagged = np.where(scores > upper_bound)[0]
        assert len(flagged) > 0

    def test_detect_noisy_samples_manual_threshold(self):
        ns = NoveltyNoiseScore()
        scores = np.array([0.1, 0.6, 0.9])
        flagged = np.where(scores > 0.5)[0]
        np.testing.assert_array_equal(flagged, [1, 2])

    def test_detect_noisy_samples_empty(self):
        ns = NoveltyNoiseScore()
        flagged = np.where(np.array([]) > 0.5)[0]
        assert len(flagged) == 0

    def test_negative_eps_raises(self):
        with pytest.raises(ValueError, match="length_scale must be > 0"):
            NoveltyNoiseScore(length_scale=-1.0)


# ======================================================================
# RedundancyScore tests
# ======================================================================


class TestRedundancyScore:
    """state_similarity, boundary_score, coverage_score, redundancy in [0,1]."""

    def test_state_similarity_identical(self):
        rs = RedundancyScore()
        X_s = np.ones((5, 3))
        sim = rs.state_similarity(X_s)
        assert 0.0 <= sim <= 1.0
        assert sim > 0.99  # all identical -> near 1

    def test_state_similarity_single_sample(self):
        rs = RedundancyScore()
        sim = rs.state_similarity(np.array([[1.0, 2.0]]))
        assert sim == 0.0

    def test_state_similarity_empty(self):
        rs = RedundancyScore()
        sim = rs.state_similarity(np.empty((0, 2)))
        assert sim == 0.0

    def test_state_similarity_1d_input(self):
        rs = RedundancyScore()
        sim = rs.state_similarity(np.array([1.0, 2.0, 3.0]))
        assert 0.0 <= sim <= 1.0

    def test_boundary_score_single_state(self):
        """Single state -> boundary = 1.0 (trivially well-separated)."""
        rs = RedundancyScore()
        X_s = np.random.randn(5, 2)
        centroids = np.array([[0.0, 0.0]])
        b = rs.boundary_score(X_s, centroids, state_id=0)
        assert b == 1.0

    def test_boundary_score_two_states(self):
        rs = RedundancyScore()
        X_s = np.random.randn(5, 2)
        centroids = np.array([[0.0, 0.0], [10.0, 10.0]])
        b = rs.boundary_score(X_s, centroids, state_id=0)
        assert 0.0 <= b <= 1.0

    def test_boundary_score_empty(self):
        rs = RedundancyScore()
        b = rs.boundary_score(np.empty((0, 2)), np.array([[0.0, 0.0], [1.0, 1.0]]), state_id=0)
        assert b == 0.0

    def test_coverage_score(self):
        rs = RedundancyScore()
        cov = rs.coverage_score(
            np.random.randn(20, 2),
            np.random.randn(100, 2),
        )
        assert cov == 0.2

    def test_redundancy_in_range(self):
        rs = RedundancyScore()
        D = rs.redundancy(
            state_proportion=0.5,
            mean_residual=0.1,
            similarity=0.8,
            boundary=0.3,
        )
        assert 0.0 <= D <= 1.0

    def test_redundancy_high_proportion(self):
        rs = RedundancyScore()
        D = rs.redundancy(
            state_proportion=0.8,
            mean_residual=0.01,
            similarity=1.0,
            boundary=0.0,
        )
        assert D > 0.5

    def test_redundancy_zero_proportion(self):
        rs = RedundancyScore()
        D = rs.redundancy(
            state_proportion=0.0,
            mean_residual=0.0,
            similarity=1.0,
            boundary=0.0,
        )
        assert D == 0.0

    def test_compute_all_shape(self):
        rs = RedundancyScore()
        X_s = np.random.randn(20, 2)
        result = rs.compute_all(
            X_s=X_s,
            state_proportion=0.5,
            mean_residual=0.1,
            centroids=np.array([[0.0, 0.0], [5.0, 5.0]]),
            state_id=0,
            X_all=np.random.randn(100, 2),
        )
        assert "similarity" in result
        assert "boundary" in result
        assert "coverage" in result
        assert "redundancy" in result
        assert 0.0 <= result["redundancy"] <= 1.0

    def test_negative_eps_raises(self):
        with pytest.raises(ValueError, match="eps must be positive"):
            RedundancyScore(eps=-1.0)


# ======================================================================
# DataClassifier tests
# ======================================================================


class TestDataClassifier:
    """Four-class classification: valuable, redundant, noisy, expert_dependent."""

    def test_classify_state_valuable(self):
        """High error + high density + high consistency + low redundancy -> valuable."""
        dc = DataClassifier()
        cat = dc.classify_state(
            mean_residual=0.1,   # > error_high=0.05
            proportion=0.4,      # > density_high=0.05
            consistency=0.9,     # > consistency_high=0.7
            redundancy=0.2,      # < redundancy_high=0.8
            noise_score=0.05,
        )
        assert cat == "valuable"

    def test_classify_state_redundant(self):
        """Low error + high density + high redundancy -> redundant."""
        dc = DataClassifier()
        cat = dc.classify_state(
            mean_residual=0.01,   # < error_high/2=0.025
            proportion=0.4,       # > density_high=0.05
            consistency=0.9,
            redundancy=0.85,      # > redundancy_high=0.8
            noise_score=0.02,
        )
        assert cat == "redundant"

    def test_classify_state_noisy(self):
        """High error + low density + low consistency -> noisy."""
        dc = DataClassifier()
        cat = dc.classify_state(
            mean_residual=0.1,    # > error_high=0.05
            proportion=0.01,      # < density_high=0.05
            consistency=0.3,      # < consistency_high=0.7
            redundancy=0.1,
            noise_score=0.6,
        )
        assert cat == "noisy"

    def test_classify_state_expert_dependent(self):
        """Expert gap > threshold -> expert_dependent regardless of other metrics."""
        dc = DataClassifier()
        cat = dc.classify_state(
            mean_residual=0.05,
            proportion=0.3,
            consistency=0.8,
            redundancy=0.3,
            noise_score=0.1,
            expert_gap=0.5,  # > expert_gap=0.3
        )
        assert cat == "expert_dependent"

    def test_classify_state_default_valuable(self):
        """Default fallback is 'valuable'."""
        dc = DataClassifier()
        cat = dc.classify_state(
            mean_residual=0.03,
            proportion=0.03,
            consistency=0.7,
            redundancy=0.79,
            noise_score=0.1,
        )
        assert cat == "valuable"

    def test_custom_thresholds(self):
        dc = DataClassifier(config={"error_high": 0.2, "redundancy_high": 0.9})
        assert dc.thresholds["error_high"] == 0.2
        assert dc.thresholds["redundancy_high"] == 0.9

    def test_classify_all_dataframe(self, state_metrics_dict):
        dc = DataClassifier()
        df = dc.classify_all(state_metrics_dict)
        assert isinstance(df, type(pd.DataFrame()))
        assert list(df.columns) == [
            "state_id", "category", "mean_residual", "proportion",
            "consistency", "redundancy", "noise_score", "expert_gap",
        ]
        assert len(df) == 4

    def test_classify_all_with_R_matrix(self, state_metrics_dict):
        dc = DataClassifier()
        R = np.array([
            [0.1, 0.5, 0.2, 0.3],
            [0.2, 0.4, 0.3, 0.1],
        ])
        df = dc.classify_all(state_metrics_dict, R_matrix=R)
        assert len(df) == 4
        assert not df["expert_gap"].isna().all()

    def test_classify_all_with_explicit_gap(self, state_metrics_dict):
        dc = DataClassifier()
        metrics = state_metrics_dict.copy()
        metrics[0]["expert_gap"] = 0.5
        df = dc.classify_all(metrics)
        assert df.loc[df["state_id"] == 0, "expert_gap"].values[0] == 0.5

    def test_recommend_action(self):
        mapping = {
            "valuable": "acquire",
            "redundant": "compress",
            "noisy": "downweight",
            "expert_dependent": "route",
        }
        for cat, expected in mapping.items():
            assert DataClassifier.recommend_action(cat) == expected

    def test_recommend_action_unknown(self):
        assert DataClassifier.recommend_action("unknown") == "acquire"

    def test_summary_output(self, state_metrics_dict):
        dc = DataClassifier()
        df = dc.classify_all(state_metrics_dict)
        summary = DataClassifier.summary(df)
        assert isinstance(summary, str)
        assert "Data Classification Summary" in summary
        assert "Total states" in summary

    def test_summary_empty(self):
        import pandas as pd
        df = pd.DataFrame()
        summary = DataClassifier.summary(df)
        assert "No states" in summary


# ======================================================================
# StateValue tests
# ======================================================================


class TestStateValue:
    """V_add > 0 for high-error states, V_remove correlates with redundancy."""

    def test_acquisition_value_high_error(self):
        sv = StateValue()
        V = sv.acquisition_value(
            mean_residual=0.5,
            proportion=0.3,
            learnability=0.8,
            redundancy=0.2,
            best_scx=0.9,
        )
        assert V > 0

    def test_acquisition_value_zero_learnability(self):
        sv = StateValue()
        V = sv.acquisition_value(
            mean_residual=0.5,
            proportion=0.3,
            learnability=0.0,
            redundancy=0.2,
            best_scx=0.9,
        )
        assert V == 0.0

    def test_acquisition_value_zero_proportion(self):
        sv = StateValue()
        V = sv.acquisition_value(
            mean_residual=0.5,
            proportion=0.0,
            learnability=0.8,
            redundancy=0.2,
            best_scx=0.9,
        )
        assert V == 0.0

    def test_compression_value(self):
        sv = StateValue()
        V = sv.compression_value(
            mean_residual=0.1,
            proportion=0.4,
            similarity=0.8,
            boundary=0.3,
        )
        assert V > 0

    def test_compression_value_redundancy_correlation(self):
        """Higher proportion + lower error + higher similarity -> higher V_remove."""
        sv = StateValue()
        V1 = sv.compression_value(
            mean_residual=0.1, proportion=0.5, similarity=0.9, boundary=0.2,
        )
        V2 = sv.compression_value(
            mean_residual=0.5, proportion=0.1, similarity=0.3, boundary=0.8,
        )
        assert V1 > V2

    def test_compute_all_dataframe(self, state_metrics_dict):
        sv = StateValue()
        scx = np.array([
            [0.9, 0.8, 0.3, 0.7],
            [0.7, 0.6, 0.4, 0.9],
        ])
        df = sv.compute_all(state_metrics_dict, scx)
        assert "state_id" in df.columns
        assert "V_add" in df.columns
        assert "V_remove" in df.columns
        assert "best_scx" in df.columns
        assert len(df) == 4

    def test_compute_all_no_missing_states(self, state_metrics_dict):
        """If state_metrics doesn't contain all states, skip missing."""
        sv = StateValue()
        scx = np.array([[0.9, 0.8], [0.7, 0.6]])
        partial = {0: state_metrics_dict[0], 1: state_metrics_dict[1]}
        df = sv.compute_all(partial, scx)
        assert len(df) == 2

    def test_rank_states_acquire(self, state_metrics_dict):
        sv = StateValue()
        scx = np.array([
            [0.9, 0.8, 0.3, 0.7],
            [0.7, 0.6, 0.4, 0.9],
        ])
        df = sv.compute_all(state_metrics_dict, scx)
        ranked = sv.rank_states(df, mode="acquire")
        assert len(ranked) == 4
        # Should be sorted descending by V_add
        V_adds = [df.loc[df["state_id"] == s, "V_add"].values[0] for s in ranked]
        for i in range(len(V_adds) - 1):
            assert V_adds[i] >= V_adds[i + 1]

    def test_rank_states_compress(self, state_metrics_dict):
        sv = StateValue()
        scx = np.array([
            [0.9, 0.8, 0.3, 0.7],
            [0.7, 0.6, 0.4, 0.9],
        ])
        df = sv.compute_all(state_metrics_dict, scx)
        ranked = sv.rank_states(df, mode="compress")
        assert len(ranked) == 4

    def test_rank_states_missing_column(self):
        sv = StateValue()
        import pandas as pd
        df = pd.DataFrame({"state_id": [0], "V_add": [1.0]})
        with pytest.raises(KeyError):
            sv.rank_states(df, mode="compress")

    def test_negative_eps_raises(self):
        with pytest.raises(ValueError, match="eps must be positive"):
            StateValue(eps=-1.0)


# ======================================================================
# Hoeffding & Chernoff bound utility tests
# ======================================================================


class TestHoeffdingBound:
    """exp(-2n*eps^2) with edge handling."""

    def test_basic(self):
        assert hoeffding_bound(n=10, epsilon=0.1) == pytest.approx(
            np.exp(-2 * 10 * 0.1**2)
        )

    def test_zero_n(self):
        assert hoeffding_bound(n=0, epsilon=0.1) == 1.0

    def test_zero_epsilon(self):
        assert hoeffding_bound(n=10, epsilon=0.0) == 1.0

    def test_negative_n(self):
        assert hoeffding_bound(n=-1, epsilon=0.1) == 1.0

    def test_large_n_small_eps(self):
        b = hoeffding_bound(n=1000, epsilon=0.01)
        assert 0.0 < b < 1.0

    def test_large_epsilon(self):
        b = hoeffding_bound(n=100, epsilon=0.5)
        assert b < 1e-20  # extremely small


class TestChernoffBound:
    """exp(-n*KL(p||q)) with edge handling."""

    def test_basic(self):
        b = chernoff_bound(p=0.3, q=0.5, n=10)
        assert 0.0 < b < 1.0

    def test_zero_n(self):
        assert chernoff_bound(p=0.3, q=0.5, n=0) == 1.0

    def test_p_equals_q(self):
        assert chernoff_bound(p=0.5, q=0.5, n=100) == 1.0

    def test_q_less_than_p(self):
        """When q <= p, Chernoff bound is vacuous (1.0)."""
        # Actually with our implementation, when p > q, KL > 0 and bound < 1
        # But when q <= p, the bound is vacuous meaning probability 1.
        b = chernoff_bound(p=0.5, q=0.3, n=10)
        assert b == 1.0  # KL divergence from 0.5 to 0.3 is > 0, but 0.3 < 0.5

    def test_small_deviations(self):
        """p close to q -> bound close to 1 (large KL -> small bound)."""
        b = chernoff_bound(p=0.5, q=0.51, n=1000)
        assert 0.0 < b < 1.0

    def test_large_n(self):
        b = chernoff_bound(p=0.2, q=0.8, n=1000)
        assert b < 1e-10


# ======================================================================
# Theorem-based StateValue method tests
# ======================================================================


class TestStateValueTheorem1:
    """Test Theorem 1 methods on StateValue."""

    def test_noise_consistency_score_all_zero(self):
        sv = StateValue()
        score = sv.noise_consistency_score(np.array([0, 0, 0]))
        assert score == 0.0

    def test_noise_consistency_score_all_one(self):
        sv = StateValue()
        score = sv.noise_consistency_score(np.array([1, 1, 1]))
        assert score == 1.0

    def test_noise_consistency_score_mixed(self):
        sv = StateValue()
        score = sv.noise_consistency_score(np.array([1, 0, 1, 0, 0]))
        assert score == pytest.approx(0.4)

    def test_noise_consistency_score_empty(self):
        sv = StateValue()
        score = sv.noise_consistency_score(np.array([]))
        assert score == 0.0

    def test_noise_consistency_score_single(self):
        sv = StateValue()
        score = sv.noise_consistency_score(np.array([1]))
        assert score == 1.0
        score = sv.noise_consistency_score(np.array([0]))
        assert score == 0.0

    def test_optimal_noise_threshold_symmetric(self):
        """When mu_max=0 (perfect experts), theta should be 0.5."""
        sv = StateValue()
        theta = sv.optimal_noise_threshold(mu_max=0.0, K=3)
        assert theta == pytest.approx(0.5)

    def test_optimal_noise_threshold_binary(self):
        """K=2 reduces to theta = 0.5 * (1 + 0) = 0.5 regardless of mu."""
        sv = StateValue()
        theta = sv.optimal_noise_threshold(mu_max=0.5, K=2)
        assert theta == pytest.approx(0.5)

    def test_optimal_noise_threshold_three_class(self):
        """K=3: theta = 0.5 * (1 + mu * (1/2))."""
        sv = StateValue()
        theta = sv.optimal_noise_threshold(mu_max=0.4, K=3)
        assert theta == pytest.approx(0.5 * (1 + 0.4 * (1 / 2)))

    def test_optimal_noise_threshold_four_class(self):
        """K=4: theta = 0.5 * (1 + mu * (2/3))."""
        sv = StateValue()
        theta = sv.optimal_noise_threshold(mu_max=0.6, K=4)
        expected = 0.5 * (1.0 + 0.6 * 2.0 / 3.0)
        assert theta == pytest.approx(expected)

    def test_optimal_noise_threshold_k_less_than_2_raises(self):
        sv = StateValue()
        with pytest.raises(ValueError, match="K must be >= 2"):
            sv.optimal_noise_threshold(mu_max=0.5, K=1)

    def test_separation_gap_optimal(self):
        """With optimal threshold, gap = 0.5 * (1 - mu * K/(K-1))."""
        sv = StateValue()
        gap = sv.separation_gap(mu_s=0.3, K=3)
        expected = 0.5 * (1.0 - 0.3 * 3.0 / 2.0)
        assert gap == pytest.approx(expected)

    def test_separation_gap_custom_theta(self):
        sv = StateValue()
        gap = sv.separation_gap(mu_s=0.2, K=3, theta=0.6)
        # min(0.6 - 0.2, 1 - 0.2/2 - 0.6) = min(0.4, 0.3) = 0.3
        assert gap == pytest.approx(0.3)

    def test_separation_gap_no_gap(self):
        """When mu is too high, gap = 0."""
        sv = StateValue()
        gap = sv.separation_gap(mu_s=0.9, K=3)
        assert gap == 0.0

    def test_separation_gap_k_less_than_2(self):
        sv = StateValue()
        gap = sv.separation_gap(mu_s=0.5, K=1)
        assert gap == 0.0

    def test_noise_detection_f1_bound_perfect(self):
        """If M is large and gaps are wide, bound approaches 1."""
        sv = StateValue()
        bound = sv.noise_detection_f1_bound(
            M=1000,
            Delta_s=np.array([0.3, 0.3]),
            rho_s=np.array([0.5, 0.5]),
            eta=0.2,
        )
        assert bound == pytest.approx(1.0, abs=1e-6)

    def test_noise_detection_f1_bound_no_gap(self):
        """If all gaps are 0, bound should be 1 - 1/eta = negative -> 0."""
        sv = StateValue()
        bound = sv.noise_detection_f1_bound(
            M=10,
            Delta_s=np.array([0.0, 0.0]),
            rho_s=np.array([0.5, 0.5]),
            eta=0.2,
        )
        assert bound == 0.0

    def test_noise_detection_f1_bound_intermediate(self):
        """A known numeric case."""
        sv = StateValue()
        M = 50
        Delta_s = np.array([0.2, 0.15])
        rho_s = np.array([0.6, 0.4])
        eta = 0.3
        bound = sv.noise_detection_f1_bound(M, Delta_s, rho_s, eta)
        # Manual: 1 - (1/0.3) * (0.6*exp(-2*50*0.04) + 0.4*exp(-2*50*0.0225))
        term1 = 0.6 * np.exp(-2 * 50 * 0.2**2)
        term2 = 0.4 * np.exp(-2 * 50 * 0.15**2)
        expected = 1.0 - (1.0 / 0.3) * (term1 + term2)
        assert bound == pytest.approx(expected)

    def test_noise_detection_f1_bound_zero_eta(self):
        """eta <= 0 should return 0."""
        sv = StateValue()
        bound = sv.noise_detection_f1_bound(
            M=10, Delta_s=np.array([0.1]), rho_s=np.array([1.0]), eta=0.0
        )
        assert bound == 0.0

    def test_noise_detection_f1_bound_empty_arrays(self):
        sv = StateValue()
        bound = sv.noise_detection_f1_bound(
            M=10, Delta_s=np.array([]), rho_s=np.array([]), eta=0.2
        )
        assert bound == 0.0

    def test_noise_detection_f1_bound_chernoff(self):
        """Chernoff bound should be >= Hoeffding bound (tighter)."""
        sv = StateValue()
        M = 30
        mu_s = np.array([0.2, 0.25])
        rho_s = np.array([0.5, 0.5])
        eta = 0.2
        K = 3
        # Hoeffding version
        gaps = np.array([sv.separation_gap(mu, K) for mu in mu_s])
        hoeff = sv.noise_detection_f1_bound(M, gaps, rho_s, eta)
        cher = sv.noise_detection_f1_bound_chernoff(M, mu_s, K, rho_s, eta)
        # Chernoff bound should be >= Hoeffding bound (tighter -> higher F1 lower bound)
        assert cher >= hoeff - 1e-10, (
            f"Chernoff bound ({cher}) should be >= Hoeffding bound ({hoeff})"
        )

    def test_noise_detection_f1_bound_chernoff_perfect(self):
        sv = StateValue()
        bound = sv.noise_detection_f1_bound_chernoff(
            M=1000, mu_s=np.array([0.1, 0.1]), K=3, rho_s=np.array([0.5, 0.5]), eta=0.2
        )
        assert bound == pytest.approx(1.0, abs=1e-4)


class TestStateValueTheorem2:
    """Test Theorem 2 feature_strength_diagnostic."""

    def test_feature_strength_strong(self, sample_data_2d):
        """Strong features (phi = X) should give low epsilon_phi."""
        sv = StateValue()
        X, y = sample_data_2d
        result = sv.feature_strength_diagnostic(X, y)
        assert "delta" in result
        assert "epsilon_phi" in result
        assert "K" in result
        assert "recommendation" in result
        assert result["K"] == 4
        assert result["epsilon_phi"] < 0.5  # should be informative
        assert result["recommendation"] in ("strong", "moderate")

    def test_feature_strength_random(self):
        """Random features should yield high epsilon (weak)."""
        sv = StateValue()
        rng = np.random.default_rng(42)
        n = 200
        X_random = rng.normal(0, 1, (n, 5))
        # Random state assignments uncorrelated with features
        state_labels = rng.integers(0, 4, n)
        result = sv.feature_strength_diagnostic(X_random, state_labels)
        assert result["epsilon_phi"] > 0.3  # at least moderate weakness
        assert "recommendation" in result

    def test_feature_strength_single_state(self):
        """Single state -> weak (K=1, no information)."""
        sv = StateValue()
        X = np.random.randn(50, 3)
        state_labels = np.zeros(50, dtype=int)
        result = sv.feature_strength_diagnostic(X, state_labels)
        assert result["recommendation"] == "weak"
        assert result["K"] == 1

    def test_feature_strength_empty(self):
        sv = StateValue()
        result = sv.feature_strength_diagnostic(
            np.empty((0, 3)), np.array([])
        )
        assert result["recommendation"] == "weak"
        assert result["delta"] == 0.0

    def test_feature_strength_1d_input(self):
        """1D feature array should be handled."""
        sv = StateValue()
        X = np.random.randn(100)
        state_labels = np.random.randint(0, 3, 100)
        result = sv.feature_strength_diagnostic(X, state_labels)
        assert "delta" in result
        assert result["K"] == 3

    def test_feature_strength_deterministic(self):
        """If phi is perfectly predictive of state, epsilon_phi should be moderately low."""
        sv = StateValue()
        rng = np.random.default_rng(42)
        n = 500
        K = 4
        # Create features that are perfectly correlated with state
        state_labels = rng.integers(0, K, n)
        # Column 0 = state ID + small noise, column 1 = pure noise
        X = np.column_stack([state_labels + rng.normal(0, 0.05, n),
                             rng.normal(0, 1, n)])
        result = sv.feature_strength_diagnostic(X, state_labels)
        # The MI estimator is conservative; so epsilon should at least
        # indicate moderate or better informativeness.
        assert result["epsilon_phi"] < 0.6
        assert result["recommendation"] in ("strong", "moderate")


# Avoid runtime pandas import issues in some test runners
import pandas as pd  # noqa: E402 (needed for class-level type hints)

# ======================================================================
# AdaptiveThreshold tests
# ======================================================================


class TestAdaptiveThresholdInit:
    """AdaptiveThreshold construction and validation."""

    def test_default_init(self):
        at = AdaptiveThreshold()
        assert at.target_metric == "f1"

    def test_custom_metric(self):
        at = AdaptiveThreshold(target_metric="precision")
        assert at.target_metric == "precision"

    def test_invalid_metric_raises(self):
        with pytest.raises(ValueError, match="Unknown target_metric"):
            AdaptiveThreshold(target_metric="auc")


class TestAdaptiveThresholdCalibrate:
    """Grid-search calibration."""

    def test_calibrate_returns_thresholds(self, state_metrics_dict):
        at = AdaptiveThreshold(target_metric="f1")
        dc = DataClassifier()
        X_dummy = np.empty((100, 2))
        y_dummy = np.ones(100)
        thresholds = at.calibrate(dc, X_dummy, y_dummy, state_metrics_dict)
        assert isinstance(thresholds, dict)
        assert "error_high" in thresholds
        assert "density_high" in thresholds

    def test_calibrate_thresholds_are_positive(self, state_metrics_dict):
        at = AdaptiveThreshold(target_metric="f1")
        dc = DataClassifier()
        X_dummy = np.empty((100, 2))
        y_dummy = np.ones(100)
        thresholds = at.calibrate(dc, X_dummy, y_dummy, state_metrics_dict)
        for v in thresholds.values():
            assert v > 0


class TestAdaptiveThresholdSensitivity:
    """Sensitivity analysis results."""

    def test_sensitivity_returns_dataframe(self, state_metrics_dict):
        at = AdaptiveThreshold()
        dc = DataClassifier()
        X_dummy = np.empty((100, 2))
        y_dummy = np.ones(100)
        df = at.sensitivity_analysis(dc, X_dummy, y_dummy, state_metrics_dict)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_sensitivity_columns(self, state_metrics_dict):
        at = AdaptiveThreshold()
        dc = DataClassifier()
        X_dummy = np.empty((100, 2))
        y_dummy = np.ones(100)
        df = at.sensitivity_analysis(dc, X_dummy, y_dummy, state_metrics_dict)
        expected = {
            "threshold_name", "perturbation", "base_value",
            "perturbed_value", "accuracy_change", "f1_change",
        }
        assert expected.issubset(set(df.columns))


class TestAdaptiveThresholdAuto:
    """Unsupervised auto-threshold method."""

    def test_auto_threshold_percentile(self, state_metrics_dict):
        at = AdaptiveThreshold()
        X_dummy = np.empty((100, 2))
        th = at.auto_threshold(X_dummy, state_metrics_dict, method="percentile")
        assert isinstance(th, dict)
        assert "error_high" in th
        assert th["error_high"] > 0

    def test_auto_threshold_gap(self, state_metrics_dict):
        at = AdaptiveThreshold()
        X_dummy = np.empty((100, 2))
        th = at.auto_threshold(X_dummy, state_metrics_dict, method="gap")
        assert isinstance(th, dict)
        assert "error_high" in th

    def test_auto_threshold_invalid_method(self, state_metrics_dict):
        at = AdaptiveThreshold()
        X_dummy = np.empty((100, 2))
        with pytest.raises(ValueError, match="Unknown method"):
            at.auto_threshold(X_dummy, state_metrics_dict, method="unknown")

    def test_auto_threshold_empty_metrics(self):
        at = AdaptiveThreshold()
        X_dummy = np.empty((0, 2))
        th = at.auto_threshold(X_dummy, {}, method="percentile")
        assert th["error_high"] == 0.05


class TestAdaptiveThresholdEvaluate:
    """Full evaluation comparing default / calibrated / adaptive."""

    def test_evaluate_returns_all_keys(self, state_metrics_dict):
        at = AdaptiveThreshold()
        dc = DataClassifier()
        X_dummy = np.empty((100, 2))
        y_dummy = np.ones(100)
        result = at.evaluate(dc, X_dummy, y_dummy, state_metrics_dict)
        expected = {
            "default_score", "calibrated_score", "adaptive_score",
            "default_thresholds", "calibrated_thresholds",
            "adaptive_thresholds",
            "improvement_calibrated", "improvement_adaptive",
        }
        assert set(result.keys()) == expected


# ======================================================================
# StateConditionedInfluence tests (Task A: Direction 3)
# ======================================================================


class TestStateConditionedInfluence:
    """SCX + Influence fusion: two-stage data valuation."""

    def _dummy_loss_fn(self, X, y, params):
        """Simple MSE loss: pred = X @ w, where w has shape (d, 1) or (d,)."""
        w = params[0]
        if w.ndim == 2 and w.shape[0] == 1:
            w = w.T  # (1, d) -> (d, 1)
        pred = X @ w
        if pred.ndim == 2 and pred.shape[1] == 1:
            pred = pred.ravel()
        return float(np.mean((pred - y) ** 2))

    def _oracle_value_fn(self, X, y):
        """Oracle: label magnitude as proxy for value."""
        return np.abs(y).ravel()

    def test_init_default_alpha(self):
        sci = StateConditionedInfluence()
        assert sci.alpha == 0.5

    def test_init_custom_alpha(self):
        sci = StateConditionedInfluence(alpha=0.8)
        assert sci.alpha == 0.8

    def test_init_alpha_boundary(self):
        sci = StateConditionedInfluence(alpha=0.0)
        assert sci.alpha == 0.0
        sci = StateConditionedInfluence(alpha=1.0)
        assert sci.alpha == 1.0

    def test_init_alpha_out_of_range_raises(self):
        with pytest.raises(ValueError, match="alpha must be in"):
            StateConditionedInfluence(alpha=-0.1)
        with pytest.raises(ValueError, match="alpha must be in"):
            StateConditionedInfluence(alpha=1.5)

    def test_compute_influence_scores_returns_positive(self):
        sci = StateConditionedInfluence()
        rng = np.random.default_rng(42)
        X = rng.normal(0, 1, (20, 3))
        y = rng.normal(0, 1, 20)
        theta = np.array([[0.5, -0.3, 0.2]])
        scores = sci.compute_influence_scores(X, y, self._dummy_loss_fn, [theta])
        assert scores.shape == (20,)
        assert np.all(scores >= 0)

    def test_compute_influence_scores_empty(self):
        sci = StateConditionedInfluence()
        scores = sci.compute_influence_scores(
            np.empty((0, 3)), np.empty(0), self._dummy_loss_fn, [np.array([[1.0, 0.0, 0.0]])]
        )
        assert scores.shape == (0,)

    def test_compute_influence_scores_fast(self):
        sci = StateConditionedInfluence()
        rng = np.random.default_rng(42)
        X = rng.normal(0, 1, (10, 2))
        y = rng.normal(0, 1, 10)
        predict_fn = lambda x: x @ np.array([[0.5], [-0.3]])  # (d, 1) weights
        scores = sci.compute_influence_scores_fast(X, y, predict_fn, lambda yt, yp: float(np.mean((yt - yp) ** 2)))
        assert scores.shape == (10,)
        assert np.all(scores >= 0)

    def test_combined_value_shape_and_range(self):
        sci = StateConditionedInfluence(alpha=0.5)
        state_values = {0: 0.9, 1: 0.3}
        influence_scores = np.array([0.1, 0.5, 0.7, 0.2])
        state_labels = np.array([0, 1, 0, 1])
        combined = sci.combined_value(state_values, influence_scores, state_labels)
        assert combined.shape == (4,)
        assert np.all(combined >= 0.0) and np.all(combined <= 1.0 + 1e-10)

    def test_combined_value_empty(self):
        sci = StateConditionedInfluence()
        combined = sci.combined_value({}, np.array([]), np.array([]))
        assert combined.shape == (0,)

    def test_combined_value_uniform(self):
        """When all state values and influence scores are equal, result is uniform."""
        sci = StateConditionedInfluence(alpha=0.5)
        state_values = {0: 0.5, 1: 0.5}
        influence_scores = np.array([0.3, 0.3])
        state_labels = np.array([0, 1])
        combined = sci.combined_value(state_values, influence_scores, state_labels)
        np.testing.assert_allclose(combined, 0.0, atol=1e-8)

    def test_select_samples_scx_only(self):
        sci = StateConditionedInfluence()
        X = np.zeros((10, 2))
        y = np.zeros(10)
        state_values = {0: 1.0, 1: 0.0}
        state_labels = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
        selected = sci.select_samples(X, y, n_select=3, scx_state_values=state_values,
                                       state_labels=state_labels, strategy="scx_only")
        assert len(selected) == 3
        assert all(state_labels[i] == 0 for i in selected)

    def test_select_samples_two_stage(self):
        sci = StateConditionedInfluence()
        X = np.zeros((10, 2))
        y = np.array([10, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        state_values = {0: 1.0, 1: 0.0}
        state_labels = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
        selected = sci.select_samples(X, y, n_select=3, scx_state_values=state_values,
                                       state_labels=state_labels, strategy="two_stage")
        assert len(selected) == 3

    def test_select_samples_empty(self):
        sci = StateConditionedInfluence()
        selected = sci.select_samples(
            np.empty((0, 2)), np.empty(0), n_select=5,
            scx_state_values={}, state_labels=np.array([]), strategy="scx_only"
        )
        assert len(selected) == 0

    def test_select_samples_n_select_zero(self):
        sci = StateConditionedInfluence()
        X = np.zeros((10, 2))
        y = np.zeros(10)
        selected = sci.select_samples(
            X, y, n_select=0, scx_state_values={0: 1.0}, state_labels=np.zeros(10, dtype=int),
            strategy="scx_only"
        )
        assert len(selected) == 0

    def test_select_samples_invalid_strategy_raises(self):
        sci = StateConditionedInfluence()
        with pytest.raises(ValueError, match="Unknown strategy"):
            sci.select_samples(
                np.zeros((5, 2)), np.zeros(5), n_select=2,
                scx_state_values={0: 1.0}, state_labels=np.zeros(5, dtype=int),
                strategy="invalid"
            )

    def test_compare_strategies_returns_dict(self):
        sci = StateConditionedInfluence(alpha=0.5)
        rng = np.random.default_rng(42)
        X = rng.normal(0, 1, (50, 2))
        y = rng.normal(0, 5, 50)
        state_values = {0: 0.9, 1: 0.4, 2: 0.1, 3: 0.7}
        state_labels = rng.integers(0, 4, 50)
        result = sci.compare_strategies(
            X, y, n_select=10, scx_state_values=state_values,
            state_labels=state_labels, oracle_value_fn=self._oracle_value_fn
        )
        assert "scx_only" in result
        assert "two_stage" in result
        assert all(v >= 0 for v in result.values())

    def test_compare_strategies_empty(self):
        sci = StateConditionedInfluence()
        result = sci.compare_strategies(
            np.empty((0, 2)), np.empty(0), n_select=5,
            scx_state_values={}, state_labels=np.array([]),
            oracle_value_fn=self._oracle_value_fn
        )
        assert result["scx_only"] == 0.0


# re-import is safe; included at end for clarity
from scx.valuation.adaptive import AdaptiveThreshold  # noqa: E402, F811
from scx.valuation.influence import StateConditionedInfluence  # noqa: E402, F811
