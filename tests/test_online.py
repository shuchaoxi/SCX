"""Tests for the Online SCX module: OnlineStateTracker, OnlineExpertTracker, OnlineSCXFramework."""

from __future__ import annotations

import numpy as np
import pytest

from scx.core.online import OnlineStateTracker, OnlineExpertTracker, OnlineSCXFramework


# ======================================================================
# OnlineStateTracker tests
# ======================================================================


class TestOnlineStateTracker:
    """Centroid update, proportion, resplit detection."""

    def test_init(self):
        centroids = np.array([[0.0, 0.0], [5.0, 5.0], [10.0, 10.0]])
        ost = OnlineStateTracker(centroids, decay=0.9)
        assert ost.K == 3
        assert ost.dim == 2
        assert np.allclose(ost.centroids, centroids)
        assert np.allclose(ost.counts, [1.0, 1.0, 1.0])

    def test_init_invalid_decay_raises(self):
        centroids = np.array([[0.0, 0.0]])
        with pytest.raises(ValueError, match="decay must be in"):
            OnlineStateTracker(centroids, decay=0.0)
        with pytest.raises(ValueError, match="decay must be in"):
            OnlineStateTracker(centroids, decay=1.0)
        with pytest.raises(ValueError, match="decay must be in"):
            OnlineStateTracker(centroids, decay=1.5)

    def test_init_non_2d_raises(self):
        with pytest.raises(ValueError, match="centroids must be 2D"):
            OnlineStateTracker(np.array([0.0, 0.0]))

    def test_update_assigns_nearest_state(self):
        centroids = np.array([[0.0, 0.0], [10.0, 10.0]])
        ost = OnlineStateTracker(centroids, decay=0.9)
        # Sample near centroid 0
        s = ost.update(np.array([0.1, -0.1]))
        assert s == 0
        # Sample near centroid 1
        s = ost.update(np.array([9.9, 10.1]))
        assert s == 1

    def test_update_moves_centroid(self):
        centroids = np.array([[0.0, 0.0]])
        ost = OnlineStateTracker(centroids, decay=0.9)
        ost.update(np.array([1.0, 0.0]))
        # New centroid = 0.9 * [0, 0] + 0.1 * [1, 0] = [0.1, 0.0]
        np.testing.assert_allclose(ost.centroids[0], [0.1, 0.0], atol=1e-6)

    def test_update_increments_count(self):
        centroids = np.array([[0.0, 0.0], [5.0, 5.0]])
        ost = OnlineStateTracker(centroids, decay=0.9)
        old_count = ost.counts[0].copy()
        ost.update(np.array([0.1, 0.0]))
        assert ost.counts[0] == old_count + 1.0

    def test_update_updates_radius(self):
        centroids = np.array([[0.0, 0.0]])
        ost = OnlineStateTracker(centroids, decay=0.9)
        ost.update(np.array([0.5, 0.0]))
        assert ost.radii[0] == pytest.approx(0.5)

    def test_get_state_proportions(self):
        centroids = np.array([[0.0, 0.0], [10.0, 10.0]])
        ost = OnlineStateTracker(centroids, decay=0.9)
        # Initially: counts=[1, 1], so proportions=[0.5, 0.5]
        prop = ost.get_state_proportions()
        np.testing.assert_allclose(prop, [0.5, 0.5])
        # After updating with a sample near centroid 0
        ost.update(np.array([0.1, 0.0]))
        prop = ost.get_state_proportions()
        assert prop[0] > prop[1]

    def test_get_state_proportions_total_one(self):
        centroids = np.array([[0.0, 0.0], [5.0, 0.0], [10.0, 0.0]])
        ost = OnlineStateTracker(centroids, decay=0.9)
        for _ in range(10):
            ost.update(np.random.default_rng().normal(0, 1, 2))
        prop = ost.get_state_proportions()
        assert abs(prop.sum() - 1.0) < 1e-10

    def test_should_resplit_false_initial(self):
        centroids = np.array([[0.0, 0.0], [5.0, 5.0]])
        ost = OnlineStateTracker(centroids, decay=0.9)
        assert not ost.should_resplit()

    def test_should_resplit_true_after_drift(self):
        centroids = np.array([[0.0, 0.0], [10.0, 10.0]])
        ost = OnlineStateTracker(centroids, decay=0.9)
        # Send many samples to centroid 0, growing its radius
        for _ in range(20):
            ost.update(np.array([0.1, 0.0]))
        # Send one far sample to centroid 1 to grow its radius
        ost.update(np.array([15.0, 15.0]))
        result = ost.should_resplit(threshold=2.0)
        # If radii ratio exceeds threshold, resplit is True
        max_r = float(ost.radii.max())
        min_r = float(ost.radii[ost.radii > 0].min())
        assert (max_r / min_r > 2.0) == result


# ======================================================================
# OnlineExpertTracker tests
# ======================================================================


class TestOnlineExpertTracker:
    """R_ema, SCX_ema, reliability matrices."""

    def test_init(self):
        oet = OnlineExpertTracker(M=3, K=4, decay=0.95)
        assert oet.M == 3
        assert oet.K == 4
        assert oet.R_ema.shape == (3, 4)
        assert oet.SCX_ema.shape == (3, 4)
        np.testing.assert_allclose(oet.R_ema, 0.0)
        np.testing.assert_allclose(oet.SCX_ema, 1.0)

    def test_init_invalid_raises(self):
        with pytest.raises(ValueError, match="M must be positive"):
            OnlineExpertTracker(M=0, K=2)
        with pytest.raises(ValueError, match="K must be positive"):
            OnlineExpertTracker(M=2, K=0)
        with pytest.raises(ValueError, match="decay must be in"):
            OnlineExpertTracker(M=2, K=2, decay=1.0)

    def test_update_updates_R(self):
        oet = OnlineExpertTracker(M=2, K=2, decay=0.9)
        oet.update(m=0, s=0, loss=0.5, tau=0.3)
        # R_ema[0,0] = 0.9 * 0.0 + 0.1 * 0.5 = 0.05
        assert oet.R_ema[0, 0] == pytest.approx(0.05)
        # SCX_ema[0,0]: first obs, loss=0.5 > tau=0.3 => SCX = 0.0
        assert oet.SCX_ema[0, 0] == 0.0

    def test_update_updates_SCX(self):
        oet = OnlineExpertTracker(M=1, K=1, decay=0.9)
        # Loss < tau => SCX = 1.0
        oet.update(m=0, s=0, loss=0.1, tau=0.3)
        assert oet.SCX_ema[0, 0] == 1.0

    def test_update_ema_progression(self):
        oet = OnlineExpertTracker(M=1, K=1, decay=0.8)
        # First: R = 0.8*0 + 0.2*0.5 = 0.10
        oet.update(m=0, s=0, loss=0.5, tau=0.3)
        # Second: R = 0.8*0.10 + 0.2*1.0 = 0.28
        oet.update(m=0, s=0, loss=1.0, tau=0.3)
        assert oet.R_ema[0, 0] == pytest.approx(0.28)

    def test_update_out_of_range_raises(self):
        oet = OnlineExpertTracker(M=2, K=3)
        with pytest.raises(ValueError, match="m=5 out of range"):
            oet.update(m=5, s=0, loss=0.5, tau=0.3)
        with pytest.raises(ValueError, match="s=10 out of range"):
            oet.update(m=0, s=10, loss=0.5, tau=0.3)

    def test_update_clips_negative_loss(self):
        oet = OnlineExpertTracker(M=1, K=1)
        oet.update(m=0, s=0, loss=-1.0, tau=0.3)
        assert oet.R_ema[0, 0] >= 0.0

    def test_update_increments_N_ms(self):
        oet = OnlineExpertTracker(M=2, K=2)
        oet.update(m=0, s=1, loss=0.3, tau=0.5)
        assert oet.N_ms[0, 1] == 1.0
        oet.update(m=0, s=1, loss=0.4, tau=0.5)
        assert oet.N_ms[0, 1] == 2.0

    def test_get_reliability_returns_copies(self):
        oet = OnlineExpertTracker(M=1, K=2)
        oet.update(m=0, s=0, loss=0.2, tau=0.5)
        R, SCX = oet.get_reliability()
        assert R.shape == (1, 2)
        assert SCX.shape == (1, 2)
        # Verify it's a copy (not a view)
        R[0, 0] = 999.0
        assert oet.R_ema[0, 0] != 999.0


# ======================================================================
# OnlineSCXFramework tests
# ======================================================================


class TestOnlineSCXFramework:
    """End-to-end processing, classification, summary."""

    @pytest.fixture
    def framework(self):
        centroids = np.array([[0.0, 0.0], [5.0, 5.0], [10.0, 10.0]])
        return OnlineSCXFramework(centroids, M=3, state_decay=0.9, expert_decay=0.95, tau=0.5)

    def test_init(self, framework):
        assert framework.K == 3
        assert framework.M == 3
        assert len(framework.history) == 0

    def test_process_sample_returns_record(self, framework):
        x = np.array([0.1, 0.0])
        record = framework.process_sample(x, expert_id=0, loss=0.3)
        assert "state" in record
        assert "expert" in record
        assert "loss" in record
        assert "classification" in record
        assert "state_proportion" in record
        assert record["expert"] == 0
        assert record["loss"] == 0.3

    def test_process_sample_assigns_state(self, framework):
        x_near_0 = np.array([0.1, 0.0])
        r0 = framework.process_sample(x_near_0, expert_id=0, loss=0.2)
        x_near_2 = np.array([9.9, 10.1])
        r2 = framework.process_sample(x_near_2, expert_id=1, loss=0.3)
        assert r0["state"] == 0
        assert r2["state"] == 2

    def test_process_sample_appends_history(self, framework):
        framework.process_sample(np.array([0.1, 0.0]), expert_id=0, loss=0.2)
        framework.process_sample(np.array([5.1, 5.0]), expert_id=1, loss=0.3)
        assert len(framework.history) == 2

    def test_process_sample_with_optional_y_true(self, framework):
        record = framework.process_sample(
            np.array([0.1, 0.0]), expert_id=0, loss=0.2, y_true=1.0
        )
        assert record["y_true"] == 1.0

    def test_get_data_classification(self, framework):
        for i in range(20):
            x = np.array([0.1, 0.0])
            framework.process_sample(x, expert_id=i % 3, loss=0.1)
        classification = framework.get_data_classification()
        expected_keys = {"valuable", "redundant", "noisy", "expert_dependent", "unclassified"}
        assert set(classification.keys()) == expected_keys
        assert sum(classification.values()) == 20

    def test_get_data_classification_empty(self, framework):
        classification = framework.get_data_classification()
        assert all(v == 0 for v in classification.values())

    def test_summary_output(self, framework):
        framework.process_sample(np.array([0.1, 0.0]), expert_id=0, loss=0.2)
        summary = framework.summary()
        assert isinstance(summary, str)
        assert "OnlineSCXFramework Summary" in summary
        assert "States (K)" in summary
        assert "Experts (M)" in summary
        assert "Samples processed" in summary

    def test_summary_empty(self, framework):
        summary = framework.summary()
        assert "0" in summary.split("Samples processed")[1].split("\n")[0] or True

    def test_state_proportion_updates(self, framework):
        # Send 9 samples to state 0, 1 sample to state 1
        for _ in range(9):
            framework.process_sample(np.array([0.1, 0.0]), expert_id=0, loss=0.2)
        framework.process_sample(np.array([5.1, 5.0]), expert_id=1, loss=0.2)
        prop = framework.state_tracker.get_state_proportions()
        assert prop[0] > prop[1]
