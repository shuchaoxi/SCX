# -*- coding: utf-8 -*-
"""
Noise / Novelty Score — N(s)
=============================

The noise component N(s) measures how "novel" or "uncertain" a state atom
is relative to the accumulated memory bank M_t (Spring layer).

A sample that has never been seen before (or whose structure is far from
all previously-seen samples) receives a high novelty score.  As the memory
bank grows and covers more of the state space, novelty scores naturally
decline — implementing the time-decaying novelty bonus described in the
Cercis Score formula.

Two concrete noise models are provided:

1. **NoveltyNoiseScore** — novelty based on distance to nearest neighbour(s)
   in the accumulated memory bank.  High distance → high noise score.

2. **UncertaintyNoiseScore** — uncertainty based on the variance of
   multi-expert votes.  High vote variance → high noise score.

Reference
---------
Layer 3 (Spring): monotonically growing memory bank M_t.
Layer 5 (Cercis): S(s) = Q(s) + η(t)·N(s).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import numpy as np


# ---------------------------------------------------------------------------
# Abstract base
# ---------------------------------------------------------------------------

class NoiseScore(ABC):
    """Abstract base for noise / novelty scoring functions N(s).

    Each subclass defines a specific measure of novelty or uncertainty.
    The score N(s) ∈ [0, 1] where 0 = well-known (low noise) and
    1 = highly novel (high noise).
    """

    @abstractmethod
    def score(
        self,
        state: np.ndarray,
        memory: Optional[np.ndarray] = None,
    ) -> float:
        """Compute noise score N(s) for a single state atom.

        Parameters
        ----------
        state : np.ndarray of shape (d,)
            Feature vector for the state atom.
        memory : np.ndarray of shape (|M_t|, d) or None
            Accumulated memory bank.  If None, maximum novelty is returned.

        Returns
        -------
        float
            Noise score N(s) ∈ [0, 1].
        """
        ...

    @abstractmethod
    def score_batch(
        self,
        states: np.ndarray,
        memory: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """Compute noise scores N(s_i) for a batch of state atoms.

        Parameters
        ----------
        states : np.ndarray of shape (N, d)
            Feature vectors.
        memory : np.ndarray of shape (|M_t|, d) or None
            Accumulated memory bank.

        Returns
        -------
        np.ndarray of shape (N,)
            Noise scores N(s_i) ∈ [0, 1].
        """
        ...


# ---------------------------------------------------------------------------
# Novelty via nearest-neighbour distance
# ---------------------------------------------------------------------------

class NoveltyNoiseScore(NoiseScore):
    """Noise score based on distance to nearest neighbours in memory.

    N(s) = min(1, d_nn(s, M_t) / τ)

    where d_nn is the distance to the k-th nearest neighbour in the memory
    bank and τ is a characteristic length scale.  When no memory is
    available, N(s) = 1 (maximum novelty).

    This implements the "novelty bonus" from the Cercis Score: samples that
    are far from anything previously seen get a higher score, encouraging
    the system to audit them more carefully.
    """

    def __init__(
        self,
        length_scale: float = 1.0,
        k: int = 1,
        p: float = 2.0,
    ):
        """
        Parameters
        ----------
        length_scale : float
            Characteristic length scale τ.  Distances ≥ τ map to N ≈ 1.
        k : int
            Number of nearest neighbours to use (default 1).
        p : float
            Minkowski norm order (2 = Euclidean).
        """
        if length_scale <= 0:
            raise ValueError(f"length_scale must be > 0, got {length_scale}")
        if k < 1:
            raise ValueError(f"k must be ≥ 1, got {k}")
        self.length_scale = length_scale
        self.k = k
        self.p = p

    # ------------------------------------------------------------------
    # Single sample
    # ------------------------------------------------------------------

    def score(
        self,
        state: np.ndarray,
        memory: Optional[np.ndarray] = None,
    ) -> float:
        state = np.asarray(state, dtype=np.float64).ravel()
        if memory is None or len(memory) == 0:
            return 1.0
        memory = np.asarray(memory, dtype=np.float64)
        distances = _minkowski_distance(state[np.newaxis, :], memory, self.p)
        # Use up to k nearest neighbours
        k_eff = min(self.k, len(distances))
        nn_dist = float(np.mean(np.partition(distances, k_eff - 1)[:k_eff]))
        return min(1.0, nn_dist / self.length_scale)

    # ------------------------------------------------------------------
    # Batch
    # ------------------------------------------------------------------

    def score_batch(
        self,
        states: np.ndarray,
        memory: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        states = np.asarray(states, dtype=np.float64)
        if states.ndim == 1:
            states = states.reshape(1, -1)
        if memory is None or len(memory) == 0:
            return np.ones(states.shape[0], dtype=np.float64)
        memory = np.asarray(memory, dtype=np.float64)

        # Pairwise distances: (N, |M_t|)
        dists = _pairwise_minkowski(states, memory, self.p)
        # For each query, take mean distance to k nearest
        k_eff = min(self.k, dists.shape[1])
        nn_dists = np.mean(np.partition(dists, k_eff - 1, axis=1)[:, :k_eff], axis=1)
        return np.minimum(1.0, nn_dists / self.length_scale)

    # ------------------------------------------------------------------
    # Yajie-compatible compute interface
    # ------------------------------------------------------------------

    def compute(
        self,
        residuals: np.ndarray,
        state_proportion: float,
        consistency: float,
    ) -> np.ndarray:
        """Compute noise scores from residuals, state proportion, and expert consistency.

        Used by Yajie.scan() and Yajie.fit() to produce per-sample or
        per-state noise scores N ∈ [0, 1].

        Parameters
        ----------
        residuals : np.ndarray
            Per-sample residual values (prediction error magnitude).
        state_proportion : float
            Proportion ρ of the dataset represented by this state/sample.
        consistency : float
            Expert consistency score ∈ [0, 1].

        Returns
        -------
        np.ndarray
            Noise scores ∈ [0, 1], same length as ``residuals``.
        """
        residuals = np.asarray(residuals, dtype=np.float64).ravel()
        # Noise combines residual magnitude with inconsistency weighting
        # and rarity (low proportion → higher novelty).
        w_consistency = np.float64(np.clip(1.0 - consistency, 0.0, 1.0))
        w_proportion = np.float64(np.clip(1.0 - state_proportion, 0.0, 1.0))
        noise = residuals * (0.5 + 0.5 * w_consistency) * (0.5 + 0.5 * w_proportion)
        return np.clip(noise, 0.0, 1.0)


# ---------------------------------------------------------------------------
# Uncertainty via expert vote variance
# ---------------------------------------------------------------------------

class UncertaintyNoiseScore(NoiseScore):
    """Noise score based on multi-expert vote variance.

    N(s) = 4 · Var[v_1(s), ..., v_M(s)]

    For binary votes with mean μ ∈ [0, 1], the maximum variance is 0.25
    (at μ = 0.5).  The factor of 4 normalises to [0, 1].

    High vote variance indicates that experts disagree strongly about
    the sample — a signal of high uncertainty / potential label noise.
    """

    def score(
        self,
        state: np.ndarray,
        memory: Optional[np.ndarray] = None,
    ) -> float:
        """Compute uncertainty noise from vote variance.

        Note: ``state`` is interpreted as the vector of expert votes
        v_m(s) ∈ {0, 1} for a single state atom.
        """
        state = np.asarray(state, dtype=np.float64).ravel()
        if len(state) <= 1:
            return 1.0  # maximum uncertainty with a single voter
        var = float(np.var(state))
        return min(1.0, 4.0 * var)

    def score_batch(
        self,
        states: np.ndarray,
        memory: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """Compute uncertainty noise for a batch.

        Note: ``states`` is interpreted as the votes matrix of shape
        (N, M) where each row is expert votes for one state atom.
        """
        states = np.asarray(states, dtype=np.float64)
        if states.ndim == 1:
            states = states.reshape(1, -1)
        M = states.shape[1]
        if M <= 1:
            return np.ones(states.shape[0], dtype=np.float64)
        var = states.var(axis=1, ddof=0)  # shape (N,)
        return np.minimum(1.0, 4.0 * var)


# ---------------------------------------------------------------------------
# Distance helpers
# ---------------------------------------------------------------------------

def _minkowski_distance(
    x: np.ndarray,
    y: np.ndarray,
    p: float,
) -> np.ndarray:
    """Minkowski distance between a single point x (1, d) and set y (m, d)."""
    return np.linalg.norm(y - x, ord=p, axis=1)


def _pairwise_minkowski(
    x: np.ndarray,
    y: np.ndarray,
    p: float,
) -> np.ndarray:
    """Pairwise Minkowski distances between two sets x (n, d) and y (m, d).

    Returns array of shape (n, m).
    """
    if p == 2.0:
        return _euclidean_pairwise(x, y)
    # General Minkowski
    n, d = x.shape
    m = y.shape[0]
    out = np.empty((n, m), dtype=np.float64)
    for i in range(n):
        out[i, :] = np.linalg.norm(y - x[i], ord=p, axis=1)
    return out


def _euclidean_pairwise(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Efficient pairwise Euclidean distance: (n, d) × (m, d) → (n, m)."""
    xx = np.sum(x * x, axis=1, keepdims=True)  # (n, 1)
    yy = np.sum(y * y, axis=1, keepdims=True)  # (m, 1) → (1, m)
    xy = x @ y.T  # (n, m)
    # clamp to handle floating-point rounding near zero
    dist2 = np.maximum(0.0, xx + yy.T - 2.0 * xy)
    return np.sqrt(dist2)
