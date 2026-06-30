"""M-parameter computation utilities for SCX audit guarantees."""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np


def compute_M_min(epsilon: float, delta: float) -> int:
    """Compute the minimum verifier count from the Hoeffding bound.

    M_min = ceil(ln(1 / epsilon) / (2 * delta^2))
    """
    if not 0.0 < epsilon < 1.0:
        raise ValueError(f"epsilon must be in (0, 1), got {epsilon}")
    if delta <= 0.0:
        raise ValueError(f"delta must be > 0, got {delta}")
    return int(math.ceil(math.log(1.0 / epsilon) / (2.0 * delta * delta)))


def compute_M_eff(M: int, rho_bar: float) -> float:
    """Compute the effective independent verifier count under correlation."""
    if M <= 0:
        raise ValueError(f"M must be positive, got {M}")
    if rho_bar > 1.0:
        raise ValueError(f"rho_bar must be <= 1, got {rho_bar}")

    denominator = 1.0 + (M - 1) * rho_bar
    if denominator <= 0.0:
        raise ValueError(
            "rho_bar yields a non-positive effective-sample denominator"
        )
    return float(M / denominator)


def compute_f1_bound(
    M: int,
    delta: float | Sequence[float] | np.ndarray,
    states: Sequence[object] | np.ndarray,
    eta: float,
) -> float:
    """Compute the SCX Theorem 1 Hoeffding F1 lower bound.

    The bound is:

        F1 >= 1 - (1 / eta) * sum_s rho_s * exp(-2 * M * delta_s^2)

    ``states`` may be either state labels, state probabilities, or state
    weights. A scalar ``delta`` is broadcast across states.
    """
    if M <= 0:
        raise ValueError(f"M must be positive, got {M}")
    if eta <= 0.0:
        raise ValueError(f"eta must be > 0, got {eta}")

    rho_s = _state_probabilities(states)
    if rho_s.size == 0:
        return 0.0

    delta_s = np.asarray(delta, dtype=float)
    if delta_s.ndim == 0:
        delta_s = np.full(rho_s.shape, float(delta_s), dtype=float)
    else:
        delta_s = delta_s.reshape(-1)

    if delta_s.shape[0] != rho_s.shape[0]:
        raise ValueError(
            f"delta has {delta_s.shape[0]} entries but states imply "
            f"{rho_s.shape[0]} state probabilities"
        )

    terms = rho_s * np.exp(-2.0 * M * delta_s**2)
    bound = 1.0 - (1.0 / eta) * float(terms.sum())
    return float(np.clip(bound, 0.0, 1.0))


def _state_probabilities(states: Sequence[object] | np.ndarray) -> np.ndarray:
    arr = np.asarray(states)
    if arr.size == 0:
        return np.array([], dtype=float)
    arr = arr.reshape(-1)

    if np.issubdtype(arr.dtype, np.number):
        values = arr.astype(float)
        total = float(values.sum())
        if np.all(values >= 0.0) and total > 0.0:
            if np.isclose(total, 1.0):
                return values / total
            if not _looks_like_labels(values):
                return values / total

    _, counts = np.unique(arr, return_counts=True)
    return counts.astype(float) / float(counts.sum())


def _looks_like_labels(values: np.ndarray) -> bool:
    if not np.all(np.isfinite(values)):
        return False
    if not np.allclose(values, np.round(values)):
        return False
    unique = np.unique(values.astype(int))
    return unique.min() >= 0 and unique.max() < values.size
