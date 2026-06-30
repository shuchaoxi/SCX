"""M-parameter computation utilities for SCX audit guarantees.

Symbiotic binding (共生绑定): M is directly derived from the training
data hash. The first 20 bits of SHA-256(data) ARE the M value.
Changing the data changes the hash, which changes M. Inseparable.
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np


# ---------------------------------------------------------------------------
# Symbiotic Binding (共生绑定) — M = first 20 bits of SHA-256(data)
# ---------------------------------------------------------------------------

M_BITS = 20  # M ∈ [0, 2^20 - 1] = [0, 1,048,575]


def derive_M_from_data_hash(data_hash: str) -> int:
    """Derive M directly from training data hash.

    M = int(first 20 bits of SHA-256(data), 2)

    No parameters. No choices. The data hash IS the M value.
    共生绑定: data and M are the same thing viewed differently.
    """
    if not data_hash or len(data_hash) != 64:
        raise ValueError("data_hash must be a 64-char SHA-256 hex digest")
    # First 20 bits = first 5 hex chars (each hex = 4 bits)
    return int(data_hash[:5], 16)


def verify_symbiotic_binding(data_hash: str, declared_M: int) -> bool:
    """Verify M matches the data hash. One-line check."""
    return derive_M_from_data_hash(data_hash) == declared_M


def hash_data_manifest(file_paths: list[str]) -> str:
    """SHA-256 of sorted (path, content_hash) pairs. This IS the M root."""
    import hashlib
    pairs = []
    for fp in sorted(file_paths):
        with open(fp, "rb") as f:
            pairs.append((fp, hashlib.sha256(f.read()).hexdigest()))
    d = hashlib.sha256()
    for path, ch in pairs:
        d.update(path.encode()); d.update(b"\x00")
        d.update(ch.encode()); d.update(b"\x00")
    return d.hexdigest()


# ---------------------------------------------------------------------------
# Standard M computations
# ---------------------------------------------------------------------------

def compute_M_min(epsilon: float, delta: float) -> int:
    """M_min = ceil(ln(1/epsilon) / (2 * delta^2)) — theoretical minimum."""
    if not 0.0 < epsilon < 1.0:
        raise ValueError(f"epsilon must be in (0, 1), got {epsilon}")
    if delta <= 0.0:
        raise ValueError(f"delta must be > 0, got {delta}")
    return int(math.ceil(math.log(1.0 / epsilon) / (2.0 * delta * delta)))


def compute_M_eff(M: int, rho_bar: float) -> float:
    """M_eff = M / (1 + (M-1)*rho_bar) — correlation-adjusted."""
    if M <= 0:
        raise ValueError(f"M must be positive, got {M}")
    if rho_bar > 1.0:
        raise ValueError(f"rho_bar must be <= 1, got {rho_bar}")
    denominator = 1.0 + (M - 1) * rho_bar
    if denominator <= 0.0:
        raise ValueError("rho_bar yields non-positive denominator")
    return float(M / denominator)


def compute_f1_bound(
    M: int,
    delta: float | Sequence[float] | np.ndarray,
    states: Sequence[object] | np.ndarray,
    eta: float,
) -> float:
    """F1 >= 1 - (1/eta) * sum_s rho_s * exp(-2*M*delta_s^2)."""
    if M <= 0:
        raise ValueError(f"M must be positive, got {M}")
    if eta <= 0.0:
        raise ValueError(f"eta must be > 0, got {eta}")
    rho_s = _state_probabilities(states)
    if rho_s.size == 0:
        return 0.0
    delta_s = np.asarray(delta, dtype=float)
    if delta_s.ndim == 0:
        delta_s = np.full(rho_s.shape, float(delta_s))
    else:
        delta_s = delta_s.reshape(-1)
    if delta_s.shape[0] != rho_s.shape[0]:
        raise ValueError(f"delta len {delta_s.shape[0]} != states {rho_s.shape[0]}")
    terms = rho_s * np.exp(-2.0 * M * delta_s**2)
    return float(np.clip(1.0 - (1.0 / eta) * float(terms.sum()), 0.0, 1.0))


def _state_probabilities(states):
    arr = np.asarray(states).reshape(-1)
    if arr.size == 0:
        return np.array([], dtype=float)
    if np.issubdtype(arr.dtype, np.number):
        vals = arr.astype(float)
        total = float(vals.sum())
        if np.all(vals >= 0) and total > 0 and np.isclose(total, 1.0):
            return vals / total
    _, counts = np.unique(arr, return_counts=True)
    return counts.astype(float) / float(counts.sum())
