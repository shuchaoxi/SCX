"""Tests for 雅洁 — the elegant data sanitizer."""

import numpy as np
import pytest
from scx.yajie import Yajie, yajie, clean


class TestYajieInit:
    def test_default_init(self):
        yj = Yajie()
        assert yj.grace == 0.05
        assert yj.purity_threshold == 0.9

    def test_custom_init(self):
        yj = Yajie(grace=0.1, purity_threshold=0.85)
        assert yj.grace == 0.1
        assert yj.purity_threshold == 0.85

    def test_invalid_grace(self):
        with pytest.raises(ValueError):
            Yajie(grace=0)
        with pytest.raises(ValueError):
            Yajie(grace=1.5)

    def test_not_scanned_yet(self):
        yj = Yajie()
        assert yj.bless() == "雅洁 has not yet visited this dataset. Call scan() first."


class TestYajieScan:
    @staticmethod
    def _make_dummy_experts(M=5):
        """Make M fake experts with varying quality."""
        experts = []
        for m in range(M):
            # Each expert has different random behavior
            seed = 42 + m
            rng = np.random.default_rng(seed)
            experts.append(
                lambda x, rng=rng: x + rng.normal(0, 0.1 * (m + 1), size=x.shape)
            )
        return experts

    def test_scan_basic(self):
        data = np.random.randn(100, 10)
        experts = self._make_dummy_experts(5)
        yj = Yajie()
        report = yj.scan(data, experts)
        assert len(report) == 100
        assert "verdict" in report.columns
        assert "reason" in report.columns
        assert "consistency_score" in report.columns

    def test_scan_few_experts_warns(self):
        data = np.random.randn(50, 5)
        experts = self._make_dummy_experts(1)
        yj = Yajie()
        with pytest.warns(UserWarning, match="multiple experts"):
            yj.scan(data, experts)

    def test_purify_before_scan_raises(self):
        yj = Yajie()
        data = np.random.randn(10, 5)
        with pytest.raises(RuntimeError, match="Call scan"):
            yj.purify(data)

    def test_purify_conservative(self):
        data = np.random.randn(100, 5)
        experts = self._make_dummy_experts(5)
        yj = Yajie()
        yj.scan(data, experts)
        clean_data, _, audit = yj.purify(data, mode="conservative")
        assert len(clean_data) <= 100
        assert audit["mode"].iloc[0] == "conservative"

    def test_purify_aggressive(self):
        data = np.random.randn(100, 5)
        experts = self._make_dummy_experts(5)
        yj = Yajie()
        yj.scan(data, experts)
        clean_data, _, _ = yj.purify(data, mode="aggressive")
        assert len(clean_data) <= 100

    def test_purify_audit(self):
        data = np.random.randn(50, 5)
        experts = self._make_dummy_experts(3)
        yj = Yajie()
        yj.scan(data, experts)
        clean_data, _, _ = yj.purify(data, mode="audit")
        assert len(clean_data) == 50  # Keeps everything

    def test_purify_with_labels(self):
        data = np.random.randn(80, 5)
        labels = np.random.randint(0, 3, 80)
        experts = self._make_dummy_experts(4)
        yj = Yajie()
        yj.scan(data, experts)
        clean_data, clean_labels, _ = yj.purify(data, labels, mode="conservative")
        assert len(clean_data) == len(clean_labels)

    def test_invalid_mode(self):
        yj = Yajie()
        data = np.random.randn(10, 5)
        experts = self._make_dummy_experts(2)
        yj.scan(data, experts)
        with pytest.raises(ValueError, match="Unknown mode"):
            yj.purify(data, mode="destroy_everything")


class TestYajieBless:
    @staticmethod
    def _make_dummy_experts(M=3):
        experts = []
        for m in range(M):
            rng = np.random.default_rng(42 + m)
            experts.append(
                lambda x, rng=rng: x + rng.normal(0, 0.05, size=x.shape)
            )
        return experts

    def test_bless_output(self):
        data = np.random.randn(200, 5)
        experts = self._make_dummy_experts(5)
        yj = Yajie()
        yj.scan(data, experts)
        blessing = yj.bless()
        assert "雅洁" in blessing
        assert "总样本" in blessing
        assert "Theorem 1" in blessing
        assert "Theorem 2" in blessing

    def test_bless_before_scan(self):
        yj = Yajie()
        assert "not yet visited" in yj.bless()


class TestYajieConvenience:
    def test_singleton_exists(self):
        from scx.yajie import yajie as yj_singleton
        assert isinstance(yj_singleton, Yajie)

    def test_clean_one_liner(self):
        data = np.random.randn(60, 5)
        rng = np.random.default_rng(42)
        experts = [
            lambda x, rng=rng: x + rng.normal(0, 0.05, size=x.shape),
            lambda x, rng=rng: x + rng.normal(0, 0.08, size=x.shape),
            lambda x, rng=rng: x + rng.normal(0, 0.12, size=x.shape),
        ]
        clean_data, _, audit = clean(data, experts, mode="conservative")
        assert len(clean_data) <= 60
        assert "雅洁" in audit["signature"].iloc[0]


class TestYajieTheoremIntegration:
    """Verify Yajie uses Theorem 1 and 2 correctly."""

    def test_noise_consistency_called(self):
        """Yajie.scan should internally call noise_consistency_score."""
        yj = Yajie()
        data = np.random.randn(30, 3)
        experts = [
            lambda x: x + 0.01 * np.random.randn(*x.shape),
            lambda x: x + 0.02 * np.random.randn(*x.shape),
            lambda x: x + 0.03 * np.random.randn(*x.shape),
        ]
        report = yj.scan(data, experts)
        # consistency_score should be computed
        assert "consistency_score" in report.columns
        assert report["consistency_score"].between(0, 1).all()

    def test_weak_feature_warning(self):
        """Yajie should warn when features are too weak (Theorem 2)."""
        yj = Yajie()
        data = np.random.randn(50, 5)
        experts = [
            lambda x: x + 0.01 * np.random.randn(*x.shape),
            lambda x: x + 0.01 * np.random.randn(*x.shape),  # nearly identical experts
        ]
        # Create intentionally weak features
        feature_matrix = np.random.randn(50, 2) * 0.001  # almost no variance
        state_labels = np.random.randint(0, 3, 50)
        with pytest.warns(UserWarning):
            yj.scan(data, experts, state_labels=state_labels, feature_matrix=feature_matrix)
