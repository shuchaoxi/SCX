"""
Redundancy Score — D(s) estimation.

Core definition:
    D(s) = rho(s) * (1 - r_bar(s)) * Sim(s) * (1 - Boundary(s))

where:
    Sim(s)      — within-state feature similarity
    Boundary(s) — separation from other states (0 = poor separation, 1 = well separated)
"""

from __future__ import annotations

from typing import Optional

import numpy as np


class RedundancyScore:
    """State-level redundancy D(s).

    A high D(s) means the state is well-covered (dense, low residual,
    internally similar, well-separated from other states) and therefore
    additional samples from it provide diminishing returns.

    Parameters
    ----------
    eps : float
        Small constant to avoid division by zero.
    """

    def __init__(self, eps: float = 1e-8) -> None:
        if eps <= 0:
            raise ValueError(f"eps must be positive, got {eps}")
        self.eps = eps

    # ------------------------------------------------------------------
    # State similarity
    # ------------------------------------------------------------------

    def state_similarity(self, X_s: np.ndarray) -> float:
        """Internal similarity of a state's samples.

        Two strategies (used automatically based on input size):

        1. **Pairwise cosine similarity** (preferred for N_s > 1)::

                Sim(s) = mean_{i != j}  cos(x_i, x_j)

           where ``cos(a, b) = (a . b) / (||a|| * ||b||)``.

        2. **Fallback** for N_s <= 1: returns 0.

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
            Feature matrix for samples in state *s*.

        Returns
        -------
        float
            Similarity in [0, 1].
        """
        X_s = np.asarray(X_s, dtype=float)
        if X_s.ndim == 1:
            X_s = X_s.reshape(-1, 1)
        N_s = X_s.shape[0]

        if N_s <= 1:
            return 0.0

        # Normalise rows to unit vectors
        norms = np.linalg.norm(X_s, axis=1, keepdims=True)
        # Avoid division by zero for zero-vectors
        norms = np.where(norms > self.eps, norms, 1.0)
        X_norm = X_s / norms

        # Cosine similarity matrix (upper triangle only)
        sim = X_norm @ X_norm.T  # (N_s, N_s)
        triu_vals = sim[np.triu_indices(N_s, k=1)]
        if triu_vals.size == 0:
            return 0.0

        mean_sim = float(np.mean(triu_vals))
        # Clamp to [0, 1] (numerical noise can produce tiny negatives)
        return float(np.clip(mean_sim, 0.0, 1.0))

    # ------------------------------------------------------------------
    # Boundary score
    # ------------------------------------------------------------------

    def boundary_score(
        self,
        X_s: np.ndarray,
        centroids: np.ndarray,
        state_id: int,
    ) -> float:
        """Boundary (separation) score for a state.

        .. math::

            \\text{Boundary}(s) = \\frac{d_\\text{self}}{d_\\text{nearest} + \\varepsilon}

        where *d_self* is the mean distance from samples to their own
        centroid and *d_nearest* is the mean distance to the nearest
        *other* centroid.  A higher value means the state is better
        separated from its neighbours.

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
        centroids : np.ndarray, shape (K, d)
            All state centroids.
        state_id : int
            Index of the current state in the centroids array.

        Returns
        -------
        float
            Boundary score in [0, 1].
        """
        X_s = np.asarray(X_s, dtype=float)
        centroids = np.asarray(centroids, dtype=float)
        if X_s.ndim == 1:
            X_s = X_s.reshape(-1, 1)
        if centroids.ndim == 1:
            centroids = centroids.reshape(-1, 1)

        N_s = X_s.shape[0]
        K = centroids.shape[0]

        if N_s == 0:
            return 0.0
        if K <= 1:
            return 1.0  # single state → trivially well-separated

        own_centroid = centroids[state_id]

        # Mean distance to own centroid
        dist_to_own = np.linalg.norm(X_s - own_centroid, axis=1)  # (N_s,)
        d_self = float(np.mean(dist_to_own))

        # Mean distance to the nearest *other* centroid
        other_ids = [i for i in range(K) if i != state_id]
        d_nearest = float("inf")
        for oid in other_ids:
            d = float(np.mean(np.linalg.norm(X_s - centroids[oid], axis=1)))
            if d < d_nearest:
                d_nearest = d

        boundary = d_self / (d_nearest + self.eps)
        return float(np.clip(boundary, 0.0, 1.0))

    # ------------------------------------------------------------------
    # Coverage score
    # ------------------------------------------------------------------

    def coverage_score(
        self,
        X_s: np.ndarray,
        X_all: np.ndarray,
    ) -> float:
        """Coverage of this state relative to the full dataset.

        Simple definition::

            Coverage(s) = N_s / N_total

        This is the sample proportion ``rho(s)``, which captures how
        well represented a state is in the overall dataset.

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
            Samples in this state.
        X_all : np.ndarray, shape (N, d)
            All samples across all states.

        Returns
        -------
        float
            Coverage in [0, 1].
        """
        N_s = len(X_s)
        N_total = max(len(X_all), 1)
        return N_s / N_total

    # ------------------------------------------------------------------
    # Redundancy (full formula)
    # ------------------------------------------------------------------

    def redundancy(
        self,
        state_proportion: float,
        mean_residual: float,
        similarity: float,
        boundary: float,
    ) -> float:
        """Full redundancy score D(s).

        .. math::

            D(s) = \\rho(s) \\cdot (1 - \\bar{r}(s))
                   \\cdot \\text{Sim}(s)
                   \\cdot (1 - \\text{Boundary}(s))

        All terms are in [0, 1] so D(s) is naturally in [0, 1].

        Parameters
        ----------
        state_proportion : float
            ``rho(s)``.
        mean_residual : float
            ``r_bar(s)``.
        similarity : float
            ``Sim(s)`` — within-state feature similarity.
        boundary : float
            ``Boundary(s)`` — separation from other states.

        Returns
        -------
        float
            Redundancy score clipped to [0, 1].
        """
        D = (
            state_proportion
            * max(0.0, 1.0 - mean_residual)
            * similarity
            * max(0.0, 1.0 - boundary)
        )
        return float(np.clip(D, 0.0, 1.0))

    # ------------------------------------------------------------------
    # Composite
    # ------------------------------------------------------------------

    def compute_all(
        self,
        X_s: np.ndarray,
        state_proportion: float,
        mean_residual: float,
        centroids: np.ndarray,
        state_id: int,
        X_all: np.ndarray,
    ) -> dict[str, float]:
        """Compute all redundancy components in one call.

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
        state_proportion : float
        mean_residual : float
        centroids : np.ndarray, shape (K, d)
        state_id : int
        X_all : np.ndarray, shape (N, d)

        Returns
        -------
        dict
            ``{'similarity': float, 'boundary': float, 'coverage': float, 'redundancy': float}``
        """
        sim = self.state_similarity(X_s)
        bound = self.boundary_score(X_s, centroids, state_id)
        cov = self.coverage_score(X_s, X_all)
        D = self.redundancy(state_proportion, mean_residual, sim, bound)

        return {
            "similarity": sim,
            "boundary": bound,
            "coverage": cov,
            "redundancy": D,
        }
