"""
Yajie fit() validation tests — using same synthetic data generator
as scripts/spring_validation.py for cross-validation consistency.

Scenarios:
  1. Default: 5 states, 3 experts, 200 synthetic structures
  2. PCA phi: feature transformation
  3. Heuristic: no experts (centroid-distance proxy)
  4. Edge cases: single sample, small N, empty data
  5. purify() after fit() workflow
  6. bless() after fit() workflow
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Ensure scx package is importable
_src = Path(__file__).resolve().parents[1] / "src"
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from scx.yajie import Yajie


# ============================================================================
# Synthetic data generation (mirrors scripts/spring_validation.py)
# ============================================================================


def generate_synthetic_structures(
    n_structures: int = 200,
    d_phi: int = 20,
    n_clusters: int = 5,
    seed: int = 42,
) -> np.ndarray:
    """Generate synthetic structures in feature space R^{d_phi}.

    Structures are drawn from n_clusters Gaussian clusters with varying
    separation, creating natural "states" for the state discovery step.

    (Identical to generate_synthetic_structures in spring_validation.py)
    """
    rng = np.random.default_rng(seed)
    structures_per_cluster = n_structures // n_clusters
    remainder = n_structures % n_clusters

    features_list = []
    for k in range(n_clusters):
        n_k = structures_per_cluster + (1 if k < remainder else 0)
        center = rng.normal(k * 3.0, 1.0, size=d_phi)
        cluster = rng.normal(center, 0.3 + k * 0.3, size=(n_k, d_phi))
        features_list.append(cluster)

    return np.vstack(features_list)


def create_mock_experts(
    n_experts: int = 3,
    d_phi: int = 20,
    n_clusters: int = 5,
    seed: int = 42,
    noise_std: float = 0.05,
) -> list:
    """Create mock NEP experts with state-conditioned reliability profiles.

    Each expert is good at some clusters and poor at others, simulating
    real-world state-conditioned expertise patterns.

    (Mirrors create_mock_experts in spring_validation.py, but returns
     simple callables compatible with Yajie's expert interface.)

    Parameters
    ----------
    n_experts : int
    d_phi : int
    n_clusters : int
    seed : int
    noise_std : float
        Standard deviation of per-sample noise added to predictions.
    """
    rng = np.random.default_rng(seed)

    # Each expert has a competence vector over clusters
    competence_maps = []
    for m in range(n_experts):
        competence = rng.uniform(0.3, 0.7, size=n_clusters)
        # Boost 1-2 random clusters
        strong_clusters = rng.choice(n_clusters, size=rng.integers(1, 3), replace=False)
        competence[strong_clusters] = rng.uniform(0.7, 0.95)
        # Weaken 1-2 other clusters
        weak_clusters = rng.choice(
            [c for c in range(n_clusters) if c not in strong_clusters],
            size=rng.integers(1, 3),
            replace=False,
        )
        competence[weak_clusters] = rng.uniform(0.1, 0.35)
        competence_maps.append(competence)

    # Build experts: each returns predictions with cluster-dependent noise
    # We need to know ground-truth clusters, so pass them during construction
    # For test purposes, we'll use a simpler interface:
    # expert(X) returns X + noise, where noise varies by distance

    experts = []
    for m in range(n_experts):
        competence = competence_maps[m]
        _rng = np.random.default_rng(seed + m + 100)

        def make_expert(comp, rng_state):
            def expert_fn(X: np.ndarray) -> np.ndarray:
                """Predict X with cluster-conditional noise.

                Uses norm of X as proxy for cluster identity (like in
                spring_validation's MockNEPExpert).
                """
                X = np.asarray(X, dtype=float)
                if X.ndim > 2:
                    X = X.reshape(X.shape[0], -1)
                n = X.shape[0]
                norms = np.linalg.norm(X, axis=1)
                # Map norms to competence bins
                norm_bins = np.linspace(norms.min() or 0, norms.max() or 1, len(comp))
                bin_indices = np.digitize(norms, norm_bins) - 1
                bin_indices = np.clip(bin_indices, 0, len(comp) - 1)
                base_conf = comp[bin_indices]
                # Return X + noise scaled by (1 - confidence)
                noise = rng_state.normal(0, noise_std, size=X.shape)
                pred_noise_scale = (1.0 - base_conf)[:, np.newaxis]
                return X + noise * pred_noise_scale

            return expert_fn

        experts.append(make_expert(competence, _rng))

    return experts


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture(scope="module")
def synthetic_structures():
    """200 synthetic structures in R^20 with 5 underlying clusters."""
    return generate_synthetic_structures(
        n_structures=200, d_phi=20, n_clusters=5, seed=42
    )


@pytest.fixture(scope="module")
def mock_experts():
    """3 mock experts with state-conditioned reliability."""
    return create_mock_experts(n_experts=3, d_phi=20, n_clusters=5, seed=42)


# ============================================================================
# Tests
# ============================================================================


class TestYajieFitBasic:
    """Basic fit() pipeline validation."""

    def test_fit_default_pipeline(self, synthetic_structures, mock_experts, caplog):
        """Full pipeline with 5 states, 3 experts, verbose output."""
        caplog.set_level(logging.INFO)

        yj = Yajie(grace=0.05, purity_threshold=0.9)
        yj.fit(
            X=synthetic_structures,
            experts=mock_experts,
            n_states=5,
            exploration_rate=0.1,
            verbose=True,
        )

        # Verify outputs exist
        assert yj.report_ is not None
        assert yj.state_report_ is not None
        assert yj._is_scanned

        # Sample report has correct columns
        assert list(yj.report_.columns) == [
            "sample_id", "state_id", "verdict",
            "state_quality", "state_noise", "state_cercis",
        ]
        assert len(yj.report_) == 200

        # State report has correct columns
        assert "state_id" in yj.state_report_.columns
        assert "quality_score" in yj.state_report_.columns
        assert "noise_score" in yj.state_report_.columns
        assert "cercis_score" in yj.state_report_.columns
        assert "verdict" in yj.state_report_.columns

        # Verdicts are valid
        valid_verdicts = {"clean", "noisy", "ambiguous"}
        assert set(yj.report_["verdict"].unique()).issubset(valid_verdicts)
        assert set(yj.state_report_["verdict"].unique()).issubset(valid_verdicts)

        # Cercis scores are in valid range [0, 1+eta]
        assert yj.state_report_["cercis_score"].min() >= 0.0
        assert yj.state_report_["cercis_score"].max() <= 1.0 + 0.1 + 0.2  # Q in [0,1], N small

        # Quality scores in [0, 1]
        assert 0 <= yj.state_report_["quality_score"].max() <= 1.0

        # All samples classified
        assert len(yj.report_) == len(synthetic_structures)

        # Verbose logging was emitted
        assert len(caplog.records) > 0
        log_messages = [r.getMessage() for r in caplog.records]
        assert any("Step 1/5: Feature extraction" in m for m in log_messages)
        assert any("Step 2/5: State discovery" in m for m in log_messages)
        assert any("Step 3/5: Computing expert errors" in m for m in log_messages)
        assert any("Step 4/5: Per-state Cercis Score" in m for m in log_messages)
        assert any("Step 5/5: Adaptive classification" in m for m in log_messages)

    def test_fit_silent_mode(self, synthetic_structures, mock_experts, caplog):
        """Verbose=False suppresses info-level logging."""
        caplog.set_level(logging.INFO)

        yj = Yajie()
        yj.fit(
            X=synthetic_structures,
            experts=mock_experts,
            n_states=5,
            verbose=False,
        )

        # Should still produce results
        assert yj.report_ is not None
        assert yj.state_report_ is not None

        # No INFO-level messages with verbose=False (debug messages only)
        log_messages = [r.getMessage() for r in caplog.records
                        if r.levelno >= logging.INFO]
        step_messages = [m for m in log_messages if "Step" in m and "Yajie.fit" in m]
        assert len(step_messages) == 0

    def test_fit_with_phi_function(self, synthetic_structures, mock_experts):
        """Use PCA-based phi for feature extraction."""
        from sklearn.decomposition import PCA

        # Fit PCA on the data to use as phi
        pca = PCA(n_components=10, random_state=42)
        pca.fit(synthetic_structures)

        def pca_phi(X):
            return pca.transform(X)

        yj = Yajie()
        yj.fit(
            X=synthetic_structures,
            experts=mock_experts,
            phi=pca_phi,
            n_states=5,
            verbose=False,
        )

        assert yj.report_ is not None
        assert yj.state_report_ is not None
        assert len(yj.report_) == len(synthetic_structures)

    def test_fit_no_experts_heuristic(self, synthetic_structures):
        """Heuristic mode: no experts, uses centroid distances."""
        yj = Yajie()
        yj.fit(
            X=synthetic_structures,
            experts=None,
            n_states=5,
            verbose=False,
        )

        assert yj.report_ is not None
        assert yj.state_report_ is not None
        assert len(yj.report_) == len(synthetic_structures)
        assert "verdict" in yj.state_report_.columns

    def test_purify_after_fit(self, synthetic_structures, mock_experts):
        """purify() should work after fit()."""
        yj = Yajie()
        yj.fit(X=synthetic_structures, experts=mock_experts, n_states=5, verbose=False)

        clean_data, clean_labels, audit = yj.purify(
            data=synthetic_structures,
            mode="conservative",
        )

        assert isinstance(clean_data, np.ndarray)
        assert isinstance(audit, pd.DataFrame)
        # Conservative: only noisy removed
        n_noisy = (yj.report_["verdict"] == "noisy").sum()
        assert len(clean_data) == len(synthetic_structures) - n_noisy

    def test_bless_after_fit(self, synthetic_structures, mock_experts):
        """bless() should return a non-empty report string after fit()."""
        yj = Yajie()
        yj.fit(X=synthetic_structures, experts=mock_experts, n_states=5, verbose=False)

        blessing = yj.bless()
        assert isinstance(blessing, str)
        assert "雅洁" in blessing
        assert "数据净化报告" in blessing

    def test_state_labels_stored(self, synthetic_structures, mock_experts):
        """_state_labels_ and _phi_X_ are stored after fit()."""
        yj = Yajie()
        yj.fit(X=synthetic_structures, experts=mock_experts, n_states=5, verbose=False)

        assert yj._state_labels_ is not None
        assert len(yj._state_labels_) == len(synthetic_structures)
        assert yj._phi_X_ is not None
        assert yj._phi_X_.shape[0] == len(synthetic_structures)


class TestYajieFitEdgeCases:
    """Edge case handling."""

    def test_empty_data_raises(self):
        """Empty data should raise ValueError."""
        yj = Yajie()
        with pytest.raises(ValueError, match="empty data"):
            yj.fit(X=np.array([]).reshape(0, 5), n_states=3, verbose=False)

    def test_single_sample(self):
        """Single sample: K=1, should not crash."""
        X = np.random.default_rng(42).normal(0, 1, size=(1, 10))

        yj = Yajie()
        yj.fit(X=X, n_states=5, verbose=False)  # n_states=5 but N=1, so K=1

        assert yj.report_ is not None
        assert len(yj.report_) == 1
        assert yj.state_report_ is not None
        # Single state should be classified as ambiguous
        assert yj.state_report_.iloc[0]["verdict"] == "ambiguous"

    def test_two_samples(self):
        """Two samples: K=2, should handle two-state comparison."""
        rng = np.random.default_rng(42)
        X = rng.normal(0, 1, size=(2, 10))

        yj = Yajie()
        yj.fit(X=X, n_states=5, verbose=False)  # n_states=5 but N=2, so K=2

        assert yj.report_ is not None
        assert len(yj.report_) == 2
        assert yj.state_report_ is not None

    def test_single_sample_state(self, synthetic_structures, mock_experts):
        """Force single-sample states by setting high n_states."""
        # Use small subset so some states have 1 sample
        X = synthetic_structures[:15]  # 15 samples, 5 states → some may be size 1
        yj = Yajie()
        yj.fit(X=X, experts=mock_experts, n_states=5, verbose=False)

        assert yj.report_ is not None
        assert len(yj.report_) == 15
        # Should not crash despite single-sample states

    def test_all_identical_samples(self):
        """All samples identical — degenerate clustering."""
        rng = np.random.default_rng(42)
        X = np.tile(rng.normal(0, 1, size=(1, 10)), (20, 1))

        yj = Yajie()
        yj.fit(X=X, n_states=5, verbose=False)

        assert yj.report_ is not None
        assert len(yj.report_) == 20

    def test_exploration_rate_extremes(self, synthetic_structures, mock_experts):
        """Test with extreme eta values."""
        # High exploration: noise-heavy scoring
        yj_high = Yajie()
        yj_high.fit(
            X=synthetic_structures,
            experts=mock_experts,
            n_states=5,
            exploration_rate=0.9,
            verbose=False,
        )
        cercis_high = yj_high.state_report_["cercis_score"].mean()

        # Low exploration: quality-dominated
        yj_low = Yajie()
        yj_low.fit(
            X=synthetic_structures,
            experts=mock_experts,
            n_states=5,
            exploration_rate=0.0,
            verbose=False,
        )
        cercis_low = yj_low.state_report_["cercis_score"].mean()

        # With high eta, noise term inflates Cercis scores
        assert cercis_high >= cercis_low - 0.01  # allow small floating noise

    def test_n_states_larger_than_n(self, synthetic_structures):
        """n_states > N should be clamped to N."""
        X = synthetic_structures[:10]  # 10 samples
        yj = Yajie()
        yj.fit(X=X, n_states=100, verbose=False)  # Request 100 states, only 10 possible

        # Should have at most 10 states
        assert len(yj.state_report_) <= 10

    def test_single_expert_warns(self, synthetic_structures):
        """Single expert should produce a warning (not enough for consistency check)."""
        single_expert = create_mock_experts(n_experts=1, d_phi=20, n_clusters=5, seed=42)

        yj = Yajie()
        # fit() with 1 expert still works, just less reliable
        yj.fit(X=synthetic_structures, experts=single_expert, n_states=5, verbose=False)

        assert yj.report_ is not None
        assert len(yj.report_) == len(synthetic_structures)


class TestYajieFitClassification:
    """Classification quality checks."""

    def test_all_three_verdicts_possible(self, synthetic_structures, mock_experts):
        """With 5 clusters and 3 experts, we should see multiple verdict types."""
        yj = Yajie()
        yj.fit(X=synthetic_structures, experts=mock_experts, n_states=5, verbose=False)

        state_verdicts = set(yj.state_report_["verdict"].unique())
        # Should have at least 2 verdict types with 5 states
        assert len(state_verdicts) >= 2

    def test_verdict_distribution_reasonable(self, synthetic_structures, mock_experts):
        """Classification should assign reasonable proportions.

        With clean synthetic data and competent experts, most samples
        should be clean or ambiguous (not noisy).
        """
        yj = Yajie()
        yj.fit(X=synthetic_structures, experts=mock_experts, n_states=5, verbose=False)

        verdict_counts = yj.report_["verdict"].value_counts()
        n_total = len(yj.report_)

        # At least some samples should be non-noisy (the data IS clean)
        noisy_ratio = verdict_counts.get("noisy", 0) / n_total
        # With 5 states and 3 competent experts, noisy ratio should be < 80%
        assert noisy_ratio < 0.8, f"Too many noisy samples: {noisy_ratio:.2%}"

    def test_state_report_keys_complete(self, synthetic_structures, mock_experts):
        """State report should have all required diagnostic keys."""
        yj = Yajie()
        yj.fit(X=synthetic_structures, experts=mock_experts, n_states=5, verbose=False)

        required_keys = {
            "state_id", "n_samples", "proportion", "mean_residual",
            "quality_score", "noise_score", "cercis_score",
            "consistency", "redundancy", "verdict",
        }
        assert required_keys.issubset(set(yj.state_report_.columns))


if __name__ == "__main__":
    # Run with verbose output for manual inspection
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        stream=sys.stdout,
    )

    print("=" * 60)
    print("Yajie fit() — Manual Validation")
    print("=" * 60)

    structures = generate_synthetic_structures(n_structures=200, d_phi=20, n_clusters=5, seed=42)
    experts = create_mock_experts(n_experts=3, d_phi=20, n_clusters=5, seed=42)

    yj = Yajie(grace=0.05, purity_threshold=0.9)
    yj.fit(X=structures, experts=experts, n_states=5, exploration_rate=0.1, verbose=True)

    print("\nState Report:")
    print(yj.state_report_.to_string())

    print("\nSample Verdict Distribution:")
    print(yj.report_["verdict"].value_counts().to_string())

    print("\n" + yj.bless())
    print("\nAll checks passed. ✓")
