# -*- coding: utf-8 -*-
"""
Cercis Score — S(s) = Q(s) + η(t)·N(s)
========================================

The Cercis Score is Layer 5 of the SCX framework.  It produces the final
quality score for each state atom by combining:

    S(s) = Q(s) + η(t) · N(s)

where:

* **Q(s)** — Quality component (inherited from ``valuation/``).  Base
  reliability derived from multi-expert consensus patterns (Yajie, Layer 4).
* **N(s)** — Noise / novelty component.  Measures how novel or uncertain
  a sample is relative to the accumulated memory bank.
* **η(t)** — Time-varying weight schedule.  Controls the balance between
  quality and novelty.  Early in deployment (small t), η(t) is large so the
  system explores novel samples aggressively; as the memory bank matures
  (large t), η(t) decays and the system relies primarily on consensus quality.

The score is clipped to [0, 1] before being returned.

Time Schedules
--------------
Five built-in schedules for η(t):

============  ==============================  ================================
Schedule      Formula                         Behaviour
============  ==============================  ================================
constant      η(t) = η₀                       Fixed weight (no decay).
exponential   η(t) = η₀ · exp(−λ t)           Fast initial decay, slow tail.
inverse       η(t) = η₀ / (1 + λ t)           Slow, smooth decay.
step          η(t) = η₀ · γ^{⌊t / τ⌋}         Discrete drops at interval τ.
cosine        η(t) = η₀ · ½(1+cos(π t / T))   Smooth decay to zero at t = T.
============  ==============================  ================================

Reference
---------
SCX in Space (§Layer 5): "The final quality score combines base quality from
multi-expert consensus with a time-decaying novelty bonus."
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np

from src.scx.valuation.base import BaseQualityScore, ConsensusQualityScore
from src.scx.valuation.noise_score import NoiseScore, NoveltyNoiseScore


# ======================================================================
# Time-varying weight schedule  η(t)
# ======================================================================

class TimeSchedule(ABC):
    """Abstract base for time-varying weight schedules η(t).

    η(t) ∈ [0, η₀] controls the influence of the noise / novelty term.
    """

    @abstractmethod
    def eta(self, t: float) -> float:
        """Evaluate the schedule at time t ≥ 0.

        Parameters
        ----------
        t : float
            Time step (non-negative).  t = 0 is deployment start.

        Returns
        -------
        float
            Weight η(t) ∈ [0, η₀].
        """
        ...

    def __call__(self, t: float) -> float:
        return self.eta(t)


class ConstantSchedule(TimeSchedule):
    """Constant schedule: η(t) = η₀."""

    def __init__(self, eta0: float = 1.0):
        if eta0 < 0:
            raise ValueError(f"eta0 must be ≥ 0, got {eta0}")
        self.eta0 = eta0

    def eta(self, t: float) -> float:
        return self.eta0


class ExponentialSchedule(TimeSchedule):
    """Exponential decay: η(t) = η₀ · exp(−λ t)."""

    def __init__(self, eta0: float = 1.0, lam: float = 0.1):
        if eta0 < 0:
            raise ValueError(f"eta0 must be ≥ 0, got {eta0}")
        if lam < 0:
            raise ValueError(f"lam must be ≥ 0, got {lam}")
        self.eta0 = eta0
        self.lam = lam

    def eta(self, t: float) -> float:
        return self.eta0 * math.exp(-self.lam * t)


class InverseSchedule(TimeSchedule):
    """Inverse time decay: η(t) = η₀ / (1 + λ t)."""

    def __init__(self, eta0: float = 1.0, lam: float = 0.1):
        if eta0 < 0:
            raise ValueError(f"eta0 must be ≥ 0, got {eta0}")
        if lam < 0:
            raise ValueError(f"lam must be ≥ 0, got {lam}")
        self.eta0 = eta0
        self.lam = lam

    def eta(self, t: float) -> float:
        return self.eta0 / (1.0 + self.lam * t)


class StepSchedule(TimeSchedule):
    """Step decay: η(t) = η₀ · γ^{⌊t / τ⌋}.

    Parameters
    ----------
    eta0 : float
        Initial weight.
    gamma : float
        Decay factor per step (0 < γ < 1).
    tau : float
        Step interval (number of time units between drops).
    """

    def __init__(self, eta0: float = 1.0, gamma: float = 0.5, tau: float = 10.0):
        if eta0 < 0:
            raise ValueError(f"eta0 must be ≥ 0, got {eta0}")
        if not 0 < gamma < 1:
            raise ValueError(f"gamma must be in (0, 1), got {gamma}")
        if tau <= 0:
            raise ValueError(f"tau must be > 0, got {tau}")
        self.eta0 = eta0
        self.gamma = gamma
        self.tau = tau

    def eta(self, t: float) -> float:
        steps = int(t / self.tau)
        return self.eta0 * (self.gamma ** steps)


class CosineSchedule(TimeSchedule):
    """Cosine annealing: η(t) = η₀ · ½(1 + cos(π t / T)) for t ∈ [0, T],
    and 0 for t > T.
    """

    def __init__(self, eta0: float = 1.0, T: float = 100.0):
        if eta0 < 0:
            raise ValueError(f"eta0 must be ≥ 0, got {eta0}")
        if T <= 0:
            raise ValueError(f"T must be > 0, got {T}")
        self.eta0 = eta0
        self.T = T

    def eta(self, t: float) -> float:
        if t >= self.T:
            return 0.0
        return self.eta0 * 0.5 * (1.0 + math.cos(math.pi * t / self.T))


# ------------------------------------------------------------------
# Schedule registry
# ------------------------------------------------------------------

_SCHEDULE_REGISTRY: Dict[str, type] = {
    "constant": ConstantSchedule,
    "exponential": ExponentialSchedule,
    "inverse": InverseSchedule,
    "step": StepSchedule,
    "cosine": CosineSchedule,
}


def make_schedule(kind: str = "exponential", **kwargs) -> TimeSchedule:
    """Factory for time schedules.

    Parameters
    ----------
    kind : str
        One of "constant", "exponential", "inverse", "step", "cosine".
    **kwargs
        Forwarded to the schedule constructor.

    Returns
    -------
    TimeSchedule
    """
    cls = _SCHEDULE_REGISTRY.get(kind)
    if cls is None:
        raise KeyError(
            f"Unknown schedule kind '{kind}'. "
            f"Available: {list(_SCHEDULE_REGISTRY)}"
        )
    return cls(**kwargs)


# ======================================================================
# Cercis Score
# ======================================================================

@dataclass
class CercisScore:
    """The Cercis quality score:  S(s) = Q(s) + η(t) · N(s).

    Combines base quality from multi-expert consensus with a time-decaying
    novelty bonus.

    Parameters
    ----------
    quality : BaseQualityScore
        Quality component Q(s).  Defaults to ``ConsensusQualityScore()``.
    noise : NoiseScore
        Noise / novelty component N(s).  Defaults to
        ``NoveltyNoiseScore()``.
    schedule : TimeSchedule or str
        Time-varying weight schedule η(t).  Pass a string name (e.g.
        ``"exponential"``) to use the factory, or a ``TimeSchedule``
        instance.
    schedule_kwargs : dict
        Keyword arguments forwarded to ``make_schedule`` when ``schedule``
        is a string.
    clip : bool
        If True, clip the final score to [0, 1].  Default True.

    Examples
    --------
    >>> cercis = CercisScore(
    ...     schedule="exponential",
    ...     schedule_kwargs={"eta0": 0.5, "lam": 0.05},
    ... )
    >>> # Score a batch at time t = 10
    >>> votes = np.array([[0, 0, 1], [1, 1, 1]])   # (N=2, M=3)
    >>> states = np.array([[0.1, 0.2], [0.9, 0.8]])  # (N=2, d=2)
    >>> memory = np.array([[0.0, 0.0], [0.1, 0.1]])  # (|M|, d)
    >>> scores = cercis.score_batch(votes, states, memory, t=10.0)
    """

    quality: BaseQualityScore = field(default_factory=ConsensusQualityScore)
    noise: NoiseScore = field(default_factory=NoveltyNoiseScore)
    schedule: Union[TimeSchedule, str] = "exponential"
    schedule_kwargs: dict = field(default_factory=dict)
    clip: bool = True

    # -- resolved schedule (set in __post_init__) --
    _schedule: TimeSchedule = field(init=False, repr=False)

    def __post_init__(self):
        if isinstance(self.schedule, str):
            self._schedule = make_schedule(self.schedule, **self.schedule_kwargs)
        elif isinstance(self.schedule, TimeSchedule):
            self._schedule = self.schedule
        else:
            raise TypeError(
                f"schedule must be str or TimeSchedule, got {type(self.schedule)}"
            )

    # ------------------------------------------------------------------
    # Single sample
    # ------------------------------------------------------------------

    def score(
        self,
        votes: np.ndarray,
        state: np.ndarray,
        memory: Optional[np.ndarray] = None,
        t: float = 0.0,
    ) -> float:
        """Compute Cercis score S(s) for a single state atom.

        Parameters
        ----------
        votes : np.ndarray of shape (M,)
            Expert votes v_m(s) ∈ {0, 1} for this state atom.
        state : np.ndarray of shape (d,)
            Feature vector for the state atom (used by N(s)).
        memory : np.ndarray of shape (|M_t|, d) or None
            Accumulated memory bank for novelty scoring.
        t : float
            Current time step.

        Returns
        -------
        float
            Cercis score S(s) ∈ [0, 1] (if clip=True).
        """
        q = self.quality.score(votes)
        n = self.noise.score(state, memory)
        eta_t = self._schedule.eta(t)
        s = q + eta_t * n
        if self.clip:
            s = max(0.0, min(1.0, s))
        return float(s)

    # ------------------------------------------------------------------
    # Batch
    # ------------------------------------------------------------------

    def score_batch(
        self,
        votes_batch: np.ndarray,
        states: np.ndarray,
        memory: Optional[np.ndarray] = None,
        t: float = 0.0,
    ) -> np.ndarray:
        """Compute Cercis scores S(s_i) for a batch of state atoms.

        Parameters
        ----------
        votes_batch : np.ndarray of shape (N, M)
            Expert votes.  Row i holds votes for state atom i.
        states : np.ndarray of shape (N, d)
            Feature vectors for all state atoms.
        memory : np.ndarray of shape (|M_t|, d) or None
            Accumulated memory bank.
        t : float
            Current time step.

        Returns
        -------
        np.ndarray of shape (N,)
            Cercis scores S(s_i) ∈ [0, 1] (if clip=True).
        """
        votes_batch = np.asarray(votes_batch, dtype=np.float64)
        states = np.asarray(states, dtype=np.float64)

        if votes_batch.ndim != 2:
            raise ValueError(
                f"votes_batch must be 2-D (N, M), got shape {votes_batch.shape}"
            )
        if states.ndim == 1:
            states = states.reshape(1, -1)
        if states.shape[0] != votes_batch.shape[0]:
            raise ValueError(
                f"votes_batch and states must have the same N. "
                f"Got votes_batch {votes_batch.shape} and states {states.shape}"
            )

        q = self.quality.score_batch(votes_batch)        # (N,)
        n = self.noise.score_batch(states, memory)        # (N,)
        eta_t = self._schedule.eta(t)
        s = q + eta_t * n
        if self.clip:
            s = np.clip(s, 0.0, 1.0)
        return s

    # ------------------------------------------------------------------
    # Convenience: combined batch with detection margin
    # ------------------------------------------------------------------

    def score_with_components(
        self,
        votes_batch: np.ndarray,
        states: np.ndarray,
        memory: Optional[np.ndarray] = None,
        t: float = 0.0,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float]:
        """Compute Cercis score and return all components separately.

        Returns
        -------
        q : np.ndarray of shape (N,)
            Quality component Q(s).
        n : np.ndarray of shape (N,)
            Noise component N(s).
        eta_t : float
            Current schedule weight.
        s : np.ndarray of shape (N,)
            Final score S(s) = Q + η·N.
        """
        votes_batch = np.asarray(votes_batch, dtype=np.float64)
        states = np.asarray(states, dtype=np.float64)

        q = self.quality.score_batch(votes_batch)
        n = self.noise.score_batch(states, memory)
        eta_t = self._schedule.eta(t)
        s = q + eta_t * n
        if self.clip:
            s = np.clip(s, 0.0, 1.0)
        return q, n, eta_t, s

    # ------------------------------------------------------------------
    # Bulk scoring over multiple time steps
    # ------------------------------------------------------------------

    def score_over_time(
        self,
        votes_batch: np.ndarray,
        states: np.ndarray,
        memory: Optional[np.ndarray] = None,
        t_values: Optional[Sequence[float]] = None,
    ) -> np.ndarray:
        """Evaluate Cercis scores at multiple time steps.

        Parameters
        ----------
        votes_batch : np.ndarray of shape (N, M)
        states : np.ndarray of shape (N, d)
        memory : np.ndarray or None
        t_values : sequence of float or None
            Time steps to evaluate.  If None, uses [0, 1, ..., 99].

        Returns
        -------
        np.ndarray of shape (len(t_values), N)
            Scores S(s_i, t_j) for each time step (row) and state (column).
        """
        if t_values is None:
            t_values = list(range(100))

        q = self.quality.score_batch(votes_batch)        # (N,)
        n = self.noise.score_batch(states, memory)        # (N,)

        results = np.empty((len(t_values), len(q)), dtype=np.float64)
        for j, t_val in enumerate(t_values):
            eta_t = self._schedule.eta(t_val)
            s = q + eta_t * n
            if self.clip:
                s = np.clip(s, 0.0, 1.0)
            results[j, :] = s
        return results

    # ------------------------------------------------------------------
    # Ranking helper
    # ------------------------------------------------------------------

    def rank(
        self,
        votes_batch: np.ndarray,
        states: np.ndarray,
        memory: Optional[np.ndarray] = None,
        t: float = 0.0,
        ascending: bool = False,
    ) -> np.ndarray:
        """Return indices that sort state atoms by Cercis score.

        Parameters
        ----------
        ascending : bool
            If True, lowest scores first (most likely noisy).  If False
            (default), highest scores first (most likely clean).

        Returns
        -------
        np.ndarray of shape (N,) and dtype int
            Sorted indices.
        """
        s = self.score_batch(votes_batch, states, memory, t)
        return np.argsort(s) if ascending else np.argsort(-s)
