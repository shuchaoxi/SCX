# -*- coding: utf-8 -*-
"""Tests for CercisScore, valuation components, and time schedules."""

import math
import sys
import os

import numpy as np
import pytest

# Ensure the package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from scx.cercis import (
    CercisScore,
    ConstantSchedule,
    ExponentialSchedule,
    InverseSchedule,
    StepSchedule,
    CosineSchedule,
    make_schedule,
)
from scx.valuation.base import ConsensusQualityScore, BaseQualityScore
from scx.valuation.noise_score import (
    NoveltyNoiseScore,
    UncertaintyNoiseScore,
    NoiseScore,
)


# ======================================================================
# Time schedules  η(t)
# ======================================================================

class TestConstantSchedule:
    def test_always_returns_eta0(self):
        sched = ConstantSchedule(eta0=0.7)
        for t in [0, 1, 10, 100, 1000]:
            assert sched.eta(t) == 0.7

    def test_callable(self):
        sched = ConstantSchedule(0.5)
        assert sched(42) == 0.5

    def test_rejects_negative(self):
        with pytest.raises(ValueError):
            ConstantSchedule(eta0=-0.1)


class TestExponentialSchedule:
    def test_decay(self):
        sched = ExponentialSchedule(eta0=1.0, lam=0.1)
        assert sched.eta(0) == 1.0
        assert sched.eta(10) == pytest.approx(math.exp(-1.0))
        assert sched.eta(100) < 1e-4

    def test_zero_lambda_is_constant(self):
        sched = ExponentialSchedule(eta0=0.5, lam=0.0)
        for t in [0, 5, 100]:
            assert sched.eta(t) == 0.5


class TestInverseSchedule:
    def test_decay(self):
        sched = InverseSchedule(eta0=1.0, lam=1.0)
        assert sched.eta(0) == 1.0
        assert sched.eta(1) == 0.5
        assert sched.eta(9) == 0.1

    def test_slow_tail(self):
        sched = InverseSchedule(eta0=1.0, lam=0.01)
        assert sched.eta(100) == pytest.approx(0.5)
        # at t=1000 it should still be noticeably > 0
        assert sched.eta(1000) > 0.05


class TestStepSchedule:
    def test_drops_at_intervals(self):
        sched = StepSchedule(eta0=1.0, gamma=0.5, tau=10.0)
        assert sched.eta(0) == 1.0
        assert sched.eta(9.9) == 1.0
        assert sched.eta(10.0) == 0.5
        assert sched.eta(19.9) == 0.5
        assert sched.eta(20.0) == 0.25
        assert sched.eta(30.0) == 0.125

    def test_gamma_bounds(self):
        with pytest.raises(ValueError):
            StepSchedule(gamma=1.0)
        with pytest.raises(ValueError):
            StepSchedule(gamma=0.0)


class TestCosineSchedule:
    def test_decay_to_zero(self):
        sched = CosineSchedule(eta0=1.0, T=100.0)
        assert sched.eta(0) == 1.0
        assert sched.eta(50) == pytest.approx(0.5)
        assert sched.eta(100) == 0.0
        assert sched.eta(200) == 0.0

    def test_monotonic(self):
        sched = CosineSchedule(eta0=1.0, T=50.0)
        vals = [sched.eta(t) for t in range(51)]
        for i in range(len(vals) - 1):
            assert vals[i] >= vals[i + 1]


class TestMakeSchedule:
    def test_factory(self):
        for kind in ["constant", "exponential", "inverse", "step", "cosine"]:
            sched = make_schedule(kind)
            assert sched is not None

    def test_unknown_raises(self):
        with pytest.raises(KeyError):
            make_schedule("nonexistent")

    def test_kwargs_forwarded(self):
        sched = make_schedule("exponential", eta0=0.3, lam=0.05)
        assert sched.eta(0) == 0.3


# ======================================================================
# Quality score  Q(s)
# ======================================================================

class TestConsensusQualityScore:
    def test_full_consensus_clean(self):
        qs = ConsensusQualityScore()
        # All experts agree with the label → no votes against
        assert qs.score(np.array([0, 0, 0, 0, 0])) == 1.0

    def test_full_consensus_noisy(self):
        qs = ConsensusQualityScore()
        # All experts disagree with the label
        assert qs.score(np.array([1, 1, 1, 1, 1])) == 0.0

    def test_mixed_consensus(self):
        qs = ConsensusQualityScore()
        # 2 of 5 disagree
        assert qs.score(np.array([0, 0, 1, 0, 1])) == 1.0 - 4.0 / 5.0  # 0.2

    def test_single_expert(self):
        qs = ConsensusQualityScore()
        assert qs.score(np.array([0])) == 1.0
        assert qs.score(np.array([1])) == 0.0  # clipped from -1.0

    def test_no_experts(self):
        qs = ConsensusQualityScore()
        assert qs.score(np.array([], dtype=int)) == 1.0

    def test_clip(self):
        qs = ConsensusQualityScore(clip=True)
        # Without clipping this would be -1.0
        assert qs.score(np.array([1])) == 0.0

    def test_batch(self):
        qs = ConsensusQualityScore()
        votes = np.array([
            [0, 0, 0],  # Q = 1.0
            [1, 0, 0],  # Q = 1 - 2/3 = 1/3
            [1, 1, 1],  # Q = 0.0
        ])
        expected = np.array([1.0, 1.0 / 3.0, 0.0])
        np.testing.assert_allclose(qs.score_batch(votes), expected)

    def test_batch_1d_raises(self):
        qs = ConsensusQualityScore()
        with pytest.raises(ValueError):
            qs.score_batch(np.array([0, 0, 0]))  # 1-D, not 2-D

    def test_detection_margin(self):
        qs = ConsensusQualityScore()
        votes = np.array([
            [0, 0, 0, 0],  # clean
            [0, 0, 0, 1],  # clean
            [1, 1, 1, 0],  # noisy
            [1, 1, 1, 1],  # noisy
        ])
        mask = np.array([True, True, False, False])
        p_clean, p_noisy, delta = qs.detection_margin(votes, mask)
        assert p_clean == 0.125   # (0+1)/8
        assert p_noisy == 0.875   # (3+4)/8
        assert delta == 0.75

    def test_f1_bound(self):
        qs = ConsensusQualityScore()
        bound = qs.f1_lower_bound(delta=0.3, M=5, eta=0.2, rho=0.5)
        # exp(-2*5*0.09) = exp(-0.9) ≈ 0.4066
        # 1 - (0.5/0.2)*0.4066 = 1 - 2.5*0.4066 ≈ -0.016 → clipped to 0
        assert 0.0 <= bound <= 1.0

    def test_f1_bound_strong_signal(self):
        qs = ConsensusQualityScore()
        bound = qs.f1_lower_bound(delta=0.5, M=10, eta=0.2, rho=1.0)
        # exp(-2*10*0.25) = exp(-5) ≈ 0.0067
        # 1 - (1/0.2)*0.0067 = 1 - 5*0.0067 ≈ 0.966
        assert bound > 0.9


# ======================================================================
# Noise / novelty score  N(s)
# ======================================================================

class TestNoveltyNoiseScore:
    def test_no_memory_gives_max(self):
        ns = NoveltyNoiseScore()
        assert ns.score(np.array([0.5, 0.5])) == 1.0
        assert np.all(ns.score_batch(np.array([[0.1], [0.9]])) == 1.0)

    def test_empty_memory(self):
        ns = NoveltyNoiseScore()
        assert ns.score(np.array([0.5]), np.array([]).reshape(0, 1)) == 1.0

    def test_exact_match_gives_zero(self):
        ns = NoveltyNoiseScore(length_scale=1.0)
        memory = np.array([[0.0, 0.0], [1.0, 1.0]])
        assert ns.score(np.array([0.0, 0.0]), memory) == 0.0

    def test_distance_scaling(self):
        ns = NoveltyNoiseScore(length_scale=2.0)
        memory = np.array([[0.0, 0.0]])
        # distance = sqrt(1^2 + 1^2) = sqrt(2) ≈ 1.414
        # N = min(1, 1.414/2) = 0.707
        expected = min(1.0, math.sqrt(2) / 2.0)
        assert ns.score(np.array([1.0, 1.0]), memory) == pytest.approx(expected)

    def test_k_neighbours(self):
        ns = NoveltyNoiseScore(length_scale=1.0, k=3)
        memory = np.array([[0.0], [0.1], [0.2], [5.0], [5.1]])
        # distances to [0.05]: [0.05, 0.05, 0.15, 4.95, 5.05]
        # 3 nearest: mean([0.05, 0.05, 0.15]) = 0.0833
        result = ns.score(np.array([0.05]), memory)
        assert 0.05 < result < 0.12

    def test_batch(self):
        ns = NoveltyNoiseScore(length_scale=1.0)
        memory = np.array([[0.0, 0.0]])
        states = np.array([[0.0, 0.0], [2.0, 0.0]])
        result = ns.score_batch(states, memory)
        assert result[0] == 0.0
        assert result[1] == 1.0  # distance 2 / scale 1 → clipped

    def test_rejects_invalid_params(self):
        with pytest.raises(ValueError):
            NoveltyNoiseScore(length_scale=0)
        with pytest.raises(ValueError):
            NoveltyNoiseScore(k=0)


class TestUncertaintyNoiseScore:
    def test_perfect_agreement(self):
        ns = UncertaintyNoiseScore()
        assert ns.score(np.array([0, 0, 0, 0])) == 0.0
        assert ns.score(np.array([1, 1, 1, 1])) == 0.0

    def test_max_disagreement(self):
        ns = UncertaintyNoiseScore()
        # variance = 0.25 → N = 1.0
        assert ns.score(np.array([0, 0, 1, 1])) == 1.0

    def test_mixed(self):
        ns = UncertaintyNoiseScore()
        # 3 of 4 agree → μ=0.75 → var=0.1875 → N=0.75
        assert ns.score(np.array([1, 1, 1, 0])) == pytest.approx(0.75)

    def test_single_voter(self):
        ns = UncertaintyNoiseScore()
        assert ns.score(np.array([0])) == 1.0  # max uncertainty

    def test_batch(self):
        ns = UncertaintyNoiseScore()
        votes = np.array([
            [0, 0, 0, 0],  # var=0   → N=0
            [0, 0, 1, 1],  # var=0.25 → N=1
            [0, 1, 1, 1],  # var=0.1875 → N=0.75
        ])
        expected = np.array([0.0, 1.0, 0.75])
        np.testing.assert_allclose(ns.score_batch(votes), expected)


# ======================================================================
# Cercis Score  S(s) = Q(s) + η(t)·N(s)
# ======================================================================

class TestCercisScore:
    @pytest.fixture
    def cercis(self):
        return CercisScore(
            schedule=ConstantSchedule(eta0=0.5),
        )

    @pytest.fixture
    def sample_data(self):
        """Create a small toy dataset."""
        # 4 state atoms, 5 experts each
        votes = np.array([
            [0, 0, 0, 0, 0],  # full consensus clean
            [0, 0, 0, 0, 1],  # mostly clean
            [1, 1, 1, 0, 0],  # borderline
            [1, 1, 1, 1, 1],  # full consensus noisy
        ], dtype=np.float64)
        states = np.array([
            [0.0, 0.0],
            [0.1, 0.1],
            [0.5, 0.5],
            [1.0, 1.0],
        ])
        memory = np.array([
            [0.0, 0.0],
            [0.0, 0.1],
        ])
        return votes, states, memory

    # -- formula correctness --

    def test_formula_clean_sample(self, cercis, sample_data):
        votes, states, memory = sample_data
        s = cercis.score(votes[0], states[0], memory, t=0.0)
        # Q(0,0,0,0,0) = 1.0
        # N: distance to [0,0] = 0 → 0
        # η = 0.5
        # S = 1.0 + 0.5*0 = 1.0
        assert s == 1.0

    def test_formula_noisy_sample(self, cercis, sample_data):
        votes, states, memory = sample_data
        s = cercis.score(votes[3], states[3], memory, t=0.0)
        # Q(1,1,1,1,1) = 0.0
        # N: distance to [0,0] = sqrt(2) → min(1, 1.414/1) = 1.0
        # η = 0.5
        # S = 0.0 + 0.5*1 = 0.5
        assert s == 0.5

    def test_batch_output_shape(self, cercis, sample_data):
        votes, states, memory = sample_data
        scores = cercis.score_batch(votes, states, memory, t=0.0)
        assert scores.shape == (4,)
        assert np.all((scores >= 0.0) & (scores <= 1.0))

    def test_batch_dimension_mismatch(self, cercis):
        votes = np.array([[0, 0, 0]])
        states = np.array([[0.1, 0.2], [0.3, 0.4]])  # N=2 vs N=1
        with pytest.raises(ValueError):
            cercis.score_batch(votes, states)

    def test_batch_1d_votes_raises(self, cercis):
        with pytest.raises(ValueError):
            cercis.score_batch(
                np.array([0, 0, 0]),
                np.array([[0.1, 0.2]]),
            )

    # -- components decomposition --

    def test_score_with_components(self, cercis, sample_data):
        votes, states, memory = sample_data
        q, n, eta_t, s = cercis.score_with_components(
            votes, states, memory, t=0.0
        )
        np.testing.assert_allclose(s, q + eta_t * n)
        assert eta_t == 0.5

    # -- time dependence --

    def test_time_decay_reduces_noise_influence(self, sample_data):
        votes, states, memory = sample_data
        cercis = CercisScore(schedule=ExponentialSchedule(eta0=1.0, lam=0.5))

        s_early = cercis.score_batch(votes, states, memory, t=0.0)
        s_late = cercis.score_batch(votes, states, memory, t=10.0)

        # Noise influence should shrink over time →
        # scores should converge toward pure quality
        # For the noisy sample (index 3), early score > late score
        # because novelty bonus decays
        assert s_early[3] > s_late[3]

    def test_late_time_pure_quality(self, sample_data):
        votes, states, memory = sample_data
        cercis = CercisScore(schedule=ExponentialSchedule(eta0=1.0, lam=100.0))

        # At t=1, η ≈ 0
        s = cercis.score_batch(votes, states, memory, t=1.0)
        q = cercis.quality.score_batch(votes)
        np.testing.assert_allclose(s, q, atol=1e-10)

    # -- score_over_time --

    def test_score_over_time_shape(self, cercis, sample_data):
        votes, states, memory = sample_data
        t_vals = [0, 1, 2, 3, 4]
        result = cercis.score_over_time(votes, states, memory, t_vals)
        assert result.shape == (5, 4)

    def test_score_over_time_default(self, cercis, sample_data):
        votes, states, memory = sample_data
        result = cercis.score_over_time(votes, states, memory)
        assert result.shape == (100, 4)

    def test_score_over_time_monotonic(self, sample_data):
        """With decaying η, scores should be monotonic in t."""
        votes, states, memory = sample_data
        cercis = CercisScore(schedule=ExponentialSchedule(eta0=1.0, lam=0.1))
        result = cercis.score_over_time(votes, states, memory, list(range(20)))
        # For each column (state atom), check monotonicity
        # Noise component N ≥ 0, so S should decrease (or stay flat) as η decays
        for i in range(result.shape[1]):
            diffs = np.diff(result[:, i])
            assert np.all(diffs <= 1e-12)  # non-increasing

    # -- ranking --

    def test_rank_descending(self, cercis, sample_data):
        votes, states, memory = sample_data
        order = cercis.rank(votes, states, memory, t=0.0)
        scores = cercis.score_batch(votes, states, memory, t=0.0)
        # First-ranked should have highest score
        assert scores[order[0]] >= scores[order[1]]
        assert scores[order[-2]] >= scores[order[-1]]

    def test_rank_ascending(self, cercis, sample_data):
        votes, states, memory = sample_data
        order = cercis.rank(votes, states, memory, t=0.0, ascending=True)
        scores = cercis.score_batch(votes, states, memory, t=0.0)
        assert scores[order[0]] <= scores[order[-1]]

    # -- clipping --

    def test_clip_enabled(self, sample_data):
        votes, states, memory = sample_data
        cercis = CercisScore(
            schedule=ConstantSchedule(eta0=10.0),  # large η → S>1
            clip=True,
        )
        s = cercis.score_batch(votes, states, memory)
        assert np.all(s <= 1.0)

    def test_clip_disabled(self, sample_data):
        votes, states, memory = sample_data
        cercis = CercisScore(
            schedule=ConstantSchedule(eta0=10.0),
            clip=False,
        )
        s = cercis.score_batch(votes, states, memory)
        # Some values may exceed 1.0
        assert np.any(s > 1.0)

    # -- string schedule --

    def test_string_schedule(self):
        cercis = CercisScore(
            schedule="inverse",
            schedule_kwargs={"eta0": 0.8, "lam": 0.2},
        )
        assert cercis._schedule.eta(0) == 0.8

    def test_invalid_schedule_type(self):
        with pytest.raises(TypeError):
            CercisScore(schedule=42)  # neither str nor TimeSchedule

    # -- custom quality / noise --

    def test_custom_components(self):
        class FixedQuality(BaseQualityScore):
            def score(self, votes):
                return 0.75
            def score_batch(self, votes_batch):
                return np.full(votes_batch.shape[0], 0.75)

        class FixedNoise(NoiseScore):
            def score(self, state, memory=None):
                return 0.25
            def score_batch(self, states, memory=None):
                return np.full(states.shape[0], 0.25)

        cercis = CercisScore(
            quality=FixedQuality(),
            noise=FixedNoise(),
            schedule=ConstantSchedule(eta0=0.4),
        )
        s = cercis.score_batch(
            np.array([[0, 0], [1, 1]]),
            np.array([[0.0], [1.0]]),
        )
        # S = 0.75 + 0.4 * 0.25 = 0.85 for every sample
        np.testing.assert_allclose(s, [0.85, 0.85])


# ======================================================================
# Integration: Cercis with different schedule regimes
# ======================================================================

class TestCercisScheduleRegimes:
    """Verify CercisScore behaviour under each schedule type."""

    @pytest.fixture
    def data(self):
        N, M, d = 50, 7, 4
        rng = np.random.default_rng(42)
        votes = (rng.random((N, M)) > 0.6).astype(np.float64)
        states = rng.random((N, d))
        memory = rng.random((20, d))
        return votes, states, memory

    @pytest.mark.parametrize("kind", ["constant", "exponential", "inverse", "step", "cosine"])
    def test_all_schedules_produce_valid_range(self, kind, data):
        votes, states, memory = data
        cercis = CercisScore(schedule=kind, clip=True)
        scores = cercis.score_batch(votes, states, memory, t=5.0)
        assert scores.shape == (50,)
        assert np.all(scores >= 0.0)
        assert np.all(scores <= 1.0)

    def test_exploration_exploitation_tradeoff(self, data):
        """Early time: novelty dominates.  Late time: quality dominates."""
        votes, states, memory = data
        cercis = CercisScore(
            schedule=ExponentialSchedule(eta0=5.0, lam=0.5),
            clip=False,
        )
        _, _, _, s_early = cercis.score_with_components(
            votes, states, memory, t=0.0
        )
        _, _, _, s_late = cercis.score_with_components(
            votes, states, memory, t=20.0
        )
        # Early scores have higher variance (η large → novelty spreads scores)
        assert np.std(s_early) >= np.std(s_late) * 0.9  # allow numerical noise
