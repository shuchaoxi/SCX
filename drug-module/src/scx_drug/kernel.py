"""Molecular kernels for drug-target interaction prediction.

Extends the general ``scx.kernel`` with molecular-specific operations:
fingerprint similarity, graph-kernel metrics, and batch vectorised
computations for the drug-module pipeline.
"""

from __future__ import annotations

from typing import Any, Callable

import numpy as np

# Re-export scx.kernel functions for convenience (no duplicate implementations)
from scx.kernel import (  # type: ignore[import-untyped]  # noqa: F401
    KERNEL_REGISTRY,
    apply_kernel,
    exponential_decay,
    gaussian_rbf,
    hill_equation,
    power_law,
    quadratic_response,
    resolve_kernel,
    sigmoid,
    softplus,
)


# ── Fingerprint similarity ─────────────────────────────────────────────────

def tanimoto_score(fp_a: np.ndarray, fp_b: np.ndarray) -> float:
    """Tanimoto (Jaccard) similarity between two binary/count fingerprint vectors.

    Returns a float in [0, 1].  Works on both binary ECFP/MACCS fingerprints
    and count-based folded Morgan fingerprints.
    """
    a = np.asarray(fp_a, dtype=float).ravel()
    b = np.asarray(fp_b, dtype=float).ravel()
    inter = float(np.dot(a, b))
    denom = float(np.sum(a)) + float(np.sum(b)) - inter
    return inter / denom if denom > 1e-12 else 0.0


def dice_score(fp_a: np.ndarray, fp_b: np.ndarray) -> float:
    """Dice (Sørensen–Dice) coefficient: 2|A∩B| / (|A| + |B|).

    More sensitive to intersection size than Tanimoto for sparse fingerprints.
    """
    a = np.asarray(fp_a, dtype=float).ravel()
    b = np.asarray(fp_b, dtype=float).ravel()
    inter = float(np.dot(a, b))
    denom = float(np.sum(a)) + float(np.sum(b))
    return 2.0 * inter / denom if denom > 1e-12 else 0.0


def cosine_similarity(fp_a: np.ndarray, fp_b: np.ndarray) -> float:
    """Cosine similarity between two fingerprint vectors."""
    a = np.asarray(fp_a, dtype=float).ravel()
    b = np.asarray(fp_b, dtype=float).ravel()
    dot = float(np.dot(a, b))
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    return dot / norm if norm > 1e-12 else 0.0


def batch_tanimoto(query_fp: np.ndarray, ref_fps: np.ndarray) -> np.ndarray:
    """Vectorised Tanimoto between one query fingerprint and N references.

    Parameters
    ----------
    query_fp : np.ndarray, shape (D,)
    ref_fps : np.ndarray, shape (N, D)

    Returns
    -------
    np.ndarray, shape (N,) — Tanimoto score vs each reference row.
    """
    q = np.asarray(query_fp, dtype=float).ravel()
    R = np.asarray(ref_fps, dtype=float)
    inter = np.dot(R, q)
    sum_R = R.sum(axis=1)
    sum_q = q.sum()
    denom = sum_R + sum_q - inter + 1e-12
    return inter / denom


def pairwise_tanimoto_matrix(fps: np.ndarray) -> np.ndarray:
    """All-pairs Tanimoto similarity matrix.

    Parameters
    ----------
    fps : np.ndarray, shape (N, D)

    Returns
    -------
    np.ndarray, shape (N, N) — symmetric similarity matrix.
    """
    R = np.asarray(fps, dtype=float)
    inter = np.dot(R, R.T)                      # (N, N)
    row_sums = R.sum(axis=1, keepdims=True)     # (N, 1)
    denom = row_sums + row_sums.T - inter + 1e-12
    return inter / denom


# ── Graph kernel ───────────────────────────────────────────────────────────

def graph_rbf_kernel(
    g1_embedding: np.ndarray,
    g2_embedding: np.ndarray,
    gamma: float = 1.0,
) -> float:
    """RBF kernel on graph-level embeddings (e.g. GNN readout vectors).

    Parameters
    ----------
    g1_embedding, g2_embedding : np.ndarray, shape (E,)
    gamma : float
        Kernel bandwidth.

    Returns
    -------
    float
    """
    a = np.asarray(g1_embedding, dtype=float).ravel()
    b = np.asarray(g2_embedding, dtype=float).ravel()
    sq_dist = float(np.sum((a - b) ** 2))
    return float(np.exp(-gamma * sq_dist))


def batch_graph_rbf(
    query_embedding: np.ndarray,
    ref_embeddings: np.ndarray,
    gamma: float = 1.0,
) -> np.ndarray:
    """Batched graph RBF: query vs N reference embeddings.

    Parameters
    ----------
    query_embedding : np.ndarray, shape (E,)
    ref_embeddings : np.ndarray, shape (N, E)
    gamma : float

    Returns
    -------
    np.ndarray, shape (N,)
    """
    q = np.asarray(query_embedding, dtype=float).ravel()
    R = np.asarray(ref_embeddings, dtype=float)
    sq_dists = np.sum((R - q) ** 2, axis=1)
    return np.exp(-gamma * sq_dists)


def pairwise_graph_rbf(embeddings: np.ndarray, gamma: float = 1.0) -> np.ndarray:
    """All-pairs RBF kernel on graph embeddings.

    Parameters
    ----------
    embeddings : np.ndarray, shape (N, E)
    gamma : float

    Returns
    -------
    np.ndarray, shape (N, N)
    """
    E = np.asarray(embeddings, dtype=float)
    sq_dists = (
        np.sum(E**2, axis=1, keepdims=True)
        + np.sum(E**2, axis=1, keepdims=True).T
        - 2.0 * np.dot(E, E.T)
    )
    return np.exp(-gamma * np.maximum(sq_dists, 0.0))


# ── Target-sequence kernel ─────────────────────────────────────────────────

def sequence_identity(seq_a: str, seq_b: str) -> float:
    """Global sequence identity (fraction of identical residues after alignment).

    For pre-aligned sequences of equal length; for production use Biopython's
    ``pairwise2`` or ``SeqIO`` should be used for real alignment.
    """
    if len(seq_a) != len(seq_b):
        # Simplified: pad to equal length and compute on overlap
        min_len = min(len(seq_a), len(seq_b))
        seq_a, seq_b = seq_a[:min_len], seq_b[:min_len]
    if len(seq_a) == 0:
        return 0.0
    matches = sum(1 for a, b in zip(seq_a, seq_b) if a == b)
    return matches / len(seq_a)


# ── Unified registry ──────────────────────────────────────────────────────

MOLECULAR_KERNEL_REGISTRY: dict[str, Callable[..., Any]] = {
    **KERNEL_REGISTRY,
    "tanimoto": tanimoto_score,
    "dice": dice_score,
    "cosine": cosine_similarity,
    "graph_rbf": graph_rbf_kernel,
    "sequence_identity": sequence_identity,
}


def resolve_molecular_kernel(name: str) -> Callable[..., Any]:
    """Look up a molecular kernel by name with linear fallback and warning."""
    kernel = MOLECULAR_KERNEL_REGISTRY.get(name)
    if kernel is None:
        import warnings
        warnings.warn(
            f"Unknown molecular kernel '{name}', falling back to 'linear'. "
            f"Available: {sorted(MOLECULAR_KERNEL_REGISTRY)}"
        )
        return MOLECULAR_KERNEL_REGISTRY["linear"]
    return kernel
