# -*- coding: utf-8 -*-
"""
Base Quality Score — Q(s)
===========================

The quality component Q(s) quantifies the base reliability of a label for
state atom *s* from multi-expert consensus patterns.

In the SCX framework, M independent experts {E_1, ..., E_M} vote on label
correctness:
    v_m(s) = 1[E_m(s) != y] ∈ {0, 1}

Under the clean hypothesis:  v_m ~ Bernoulli(p_clean,s),  p_clean,s < 0.5
Under the noisy hypothesis:  v_m ~ Bernoulli(p_noisy,s),  p_noisy,s > 0.5

The detection margin Δ_s = p_noisy,s - p_clean,s > 0 quantifies how well
consensus separates clean from noisy samples.  Q(s) is a calibrated,
increasing function of this separability.

Reference
---------
Theorem 1 (SCX): F_1 ≥ 1 - (1/η) Σ_s ρ_s exp(-2M Δ_s²)
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import List, Optional, Sequence, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Abstract base
# ---------------------------------------------------------------------------

class BaseQualityScore(ABC):
    """Abstract base for quality scoring functions Q(s).

    Each subclass implements a specific mapping from multi-expert votes to
    a scalar quality score in [0, 1] (0 = worst, 1 = best).
    """

    @abstractmethod
    def score(self, votes: np.ndarray) -> float:
        """Compute quality score Q(s) for a single state atom.

        Parameters
        ----------
        votes : np.ndarray of shape (M,) and dtype int
            Expert votes v_m(s) ∈ {0, 1}.  A vote of 1 means the expert
            *disagrees* with the given label (potential noise signal).

        Returns
        -------
        float
            Quality score Q(s) ∈ [0, 1].
        """
        ...

    @abstractmethod
    def score_batch(self, votes_batch: np.ndarray) -> np.ndarray:
        """Compute quality scores Q(s_i) for a batch of state atoms.

        Parameters
        ----------
        votes_batch : np.ndarray of shape (N, M) and dtype int
            Rows are state atoms, columns are expert votes.

        Returns
        -------
        np.ndarray of shape (N,)
            Quality scores Q(s_i) ∈ [0, 1].
        """
        ...


# ---------------------------------------------------------------------------
# Consensus quality — the canonical Q(s) from Theorem 1
# ---------------------------------------------------------------------------

class ConsensusQualityScore(BaseQualityScore):
    """Quality score derived from multi-expert consensus strength.

    Q(s) = 1 - 2·C(s)/M

    where C(s) = Σ_m v_m(s) is the disagreement count.  This maps:
      - Full consensus (C=0)          → Q = 1  (label certainly clean)
      - Full disagreement (C=M)        → Q = 0  (label certainly noisy)
      - Random guessing (C ≈ M/2)      → Q ≈ 0  (no signal)

    The factor of 2 ensures Q ∈ [0, 1] for all C ∈ [0, M].

    Under Theorem 1, the Chernoff-Hoeffding bound on F_1 uses
    Δ_s = p_noisy,s - p_clean,s, and C(s)/M is the empirical estimate
    of p_noisy,s (or p_clean,s depending on the hypothesis).
    """

    def __init__(self, clip: bool = True):
        """
        Parameters
        ----------
        clip : bool
            If True, clip output to [0, 1].  Default True.
        """
        self.clip = clip

    def score(self, votes: np.ndarray) -> float:
        """Compute consensus quality for a single state atom."""
        votes = np.asarray(votes, dtype=np.float64)
        M = votes.shape[0]
        if M == 0:
            return 1.0
        C = float(np.sum(votes))
        q = 1.0 - 2.0 * C / M
        if self.clip:
            q = max(0.0, min(1.0, q))
        return q

    def score_batch(self, votes_batch: np.ndarray) -> np.ndarray:
        """Compute consensus quality for a batch of state atoms."""
        votes_batch = np.asarray(votes_batch, dtype=np.float64)
        if votes_batch.ndim != 2:
            raise ValueError(
                f"votes_batch must be 2-D (N, M), got shape {votes_batch.shape}"
            )
        N, M = votes_batch.shape
        if M == 0:
            return np.ones(N, dtype=np.float64)
        C = votes_batch.sum(axis=1)  # shape (N,)
        q = 1.0 - 2.0 * C / M
        if self.clip:
            q = np.clip(q, 0.0, 1.0)
        return q

    # ------------------------------------------------------------------
    # Detection margin estimation
    # ------------------------------------------------------------------

    def detection_margin(
        self,
        votes_batch: np.ndarray,
        clean_mask: np.ndarray,
    ) -> Tuple[float, float, float]:
        """Estimate the detection margin Δ_s from labelled data.

        Parameters
        ----------
        votes_batch : np.ndarray of shape (N, M)
            Expert votes.
        clean_mask : np.ndarray of shape (N,) and dtype bool
            True for samples known to be clean.

        Returns
        -------
        p_clean : float
            Estimated p_clean,s (average disagreement on clean samples).
        p_noisy : float
            Estimated p_noisy,s (average disagreement on noisy samples).
        delta : float
            Detection margin Δ_s = p_noisy,s - p_clean,s.
        """
        votes_batch = np.asarray(votes_batch, dtype=np.float64)
        clean_mask = np.asarray(clean_mask, dtype=bool)
        M = votes_batch.shape[1]
        if M == 0:
            return 0.0, 0.0, 0.0
        # Per-sample disagreement rate
        rates = votes_batch.mean(axis=1)  # shape (N,)
        p_clean = float(rates[clean_mask].mean()) if clean_mask.any() else 0.0
        p_noisy = float(rates[~clean_mask].mean()) if (~clean_mask).any() else 0.0
        delta = p_noisy - p_clean
        return p_clean, p_noisy, delta

    def f1_lower_bound(
        self,
        delta: float,
        M: int,
        eta: float = 1.0,
        rho: float = 1.0,
    ) -> float:
        """Chernoff-Hoeffding lower bound on F_1 (Theorem 1).

        F_1 ≥ 1 - (rho / eta) · exp(-2 M Δ²)

        Parameters
        ----------
        delta : float
            Detection margin Δ_s.
        M : int
            Number of independent experts.
        eta : float
            Noise prevalence in the dataset (fraction noisy).  Default 1.0
            gives the loosest bound.
        rho : float
            Fraction of state atoms considered.  Default 1.0.

        Returns
        -------
        float
            Lower bound on achievable F_1 score.
        """
        if eta <= 0:
            return 1.0
        exponent = -2.0 * M * delta * delta
        bound = 1.0 - (rho / eta) * math.exp(exponent)
        return max(0.0, min(1.0, bound))
