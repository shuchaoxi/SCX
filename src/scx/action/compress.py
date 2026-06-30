# scx/action/compress.py
# CompressStrategy -- state-conditioned redundancy compression.

from __future__ import annotations

from typing import Any, Callable

import numpy as np
from sklearn.metrics import pairwise_distances


class CompressStrategy:
    """SCX-Compress: state-conditioned redundancy compression.

    Compresses a state's samples by selecting a representative subset
    with weighting.  Boundary samples (e.g., decision-boundary points)
    can be forcibly retained.

    Parameters
    ----------
    method : str
        Compression method:

        - ``"weighted_random"`` : weighted random sampling.
        - ``"kcenter"``         : greedy k-center coreset.
        - ``"herding"``         : mean-preserving herding selection.
    """

    def __init__(self, method: str = "weighted_random"):
        valid = ("weighted_random", "kcenter", "herding")
        if method not in valid:
            raise ValueError(
                f"Unknown method '{method}'. Expected one of {valid}."
            )
        self.method = method

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def redundancy_score(
        self,
        X_s: np.ndarray,
        residuals: np.ndarray,
        state_proportion: float,
    ) -> np.ndarray:
        """Compute per-sample redundancy scores for a state.

        Higher score = more redundant (lower information gain).

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
            State samples in representation space.
        residuals : np.ndarray, shape (N_s,)
            Per-sample residual / error (e.g. prediction error).
        state_proportion : float
            Proportion of the full dataset belonging to this state.

        Returns
        -------
        scores : np.ndarray, shape (N_s,)
            Redundancy scores in ``[0, 1]``.
        """
        # Density-based component: dense regions are more redundant
        if len(X_s) > 1:
            D = pairwise_distances(X_s, metric="euclidean")
            # Mean distance to nearest neighbor (proxy for density)
            np.fill_diagonal(D, np.inf)
            nn_dist = D.min(axis=1)
            max_dist = nn_dist.max() + 1e-10
            density_score = 1.0 - (nn_dist / max_dist)  # dense -> high
        else:
            density_score = np.array([0.5])

        # Residual-based component: low residual can indicate redundancy
        res_max = residuals.max() if residuals.max() > 0 else 1.0
        residual_score = 1.0 - (residuals / res_max)

        # State-proportion bonus
        prop_factor = min(state_proportion * 5.0, 1.0)

        scores = 0.4 * density_score + 0.4 * residual_score + 0.2 * prop_factor
        return np.clip(scores, 0.0, 1.0)

    def compress(
        self,
        X_s: np.ndarray,
        y_s: np.ndarray,
        residuals: np.ndarray,
        state_proportion: float,
        compression_ratio: float = 0.5,
        boundary_samples: np.ndarray | None = None,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Compress a state's data by selecting a representative subset.

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
        y_s : np.ndarray, shape (N_s,)
        residuals : np.ndarray, shape (N_s,)
        state_proportion : float
        compression_ratio : float
            Fraction of samples to keep (0 < ratio <= 1).
        boundary_samples : np.ndarray | None
            Boolean mask or indices of samples that must be retained.

        Returns
        -------
        X_compressed : np.ndarray, shape (n_keep, d)
        y_compressed : np.ndarray, shape (n_keep,)
        weights : np.ndarray, shape (n_keep,)
            Sample weights for the compressed set.
        """
        N_s = X_s.shape[0]
        n_keep = max(1, int(compression_ratio * N_s))

        # Compute redundancy scores
        scores = self.redundancy_score(X_s, residuals, state_proportion)

        # Forced retention of boundary samples
        keep_mask = np.zeros(N_s, dtype=bool)
        if boundary_samples is not None:
            boundary = np.asarray(boundary_samples)
            if boundary.dtype == bool:
                keep_mask = boundary.copy()
            else:
                keep_mask[boundary] = True

        n_forced = int(keep_mask.sum())
        n_discretionary = max(0, n_keep - n_forced)
        discretionary_candidates = np.where(~keep_mask)[0]

        if n_discretionary > 0 and len(discretionary_candidates) > 0:
            # Probability inversely proportional to redundancy score
            inv_scores = 1.0 - scores[discretionary_candidates]
            inv_scores = np.clip(inv_scores, 0.0, None)
            prob = inv_scores / (inv_scores.sum() + 1e-10)

            chosen = np.random.choice(
                discretionary_candidates,
                size=min(n_discretionary, len(discretionary_candidates)),
                replace=False,
                p=prob,
            )
            keep_mask[chosen] = True
        elif n_forced > 0:
            # Only boundary samples fit; adjust n_keep
            pass

        # Ensure we have exactly n_keep (or fewer if N_s is small)
        final_n = min(n_keep, int(keep_mask.sum()))
        if int(keep_mask.sum()) > final_n:
            # Trim excess by removing highest-redundancy retained samples
            retained = np.where(keep_mask)[0]
            order = np.argsort(scores[retained])[::-1]  # most redundant first
            to_remove = retained[order[: int(keep_mask.sum()) - final_n]]
            keep_mask[to_remove] = False

        X_comp = X_s[keep_mask]
        y_comp = y_s[keep_mask]

        # Weights: inversely proportional to redundancy score
        kept_scores = scores[keep_mask]
        weights = self._compute_weights(kept_scores)

        return X_comp, y_comp, weights

    def weighted_coreset(
        self,
        X_s: np.ndarray,
        y_s: np.ndarray,
        residuals: np.ndarray,
        n_keep: int,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Weighted coreset via redundancy-weighted random sampling.

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
        y_s : np.ndarray, shape (N_s,)
        residuals : np.ndarray, shape (N_s,)
        n_keep : int

        Returns
        -------
        X_sub : np.ndarray, shape (n_keep, d)
        y_sub : np.ndarray, shape (n_keep,)
        weights : np.ndarray, shape (n_keep,)
        """
        N_s = X_s.shape[0]
        n_keep = min(n_keep, N_s)

        scores = self.redundancy_score(
            X_s, residuals, state_proportion=N_s / N_s
        )
        inv_scores = 1.0 - scores
        inv_scores = np.clip(inv_scores, 0.0, None)
        prob = inv_scores / (inv_scores.sum() + 1e-10)

        indices = np.random.choice(N_s, size=n_keep, replace=False, p=prob)
        kept_scores = scores[indices]
        weights = self._compute_weights(kept_scores)

        return X_s[indices], y_s[indices], weights

    def kcenter_coreset(
        self, X_s: np.ndarray, n_keep: int
    ) -> np.ndarray:
        """Greedy k-center coreset: maximize minimum distance to selected set.

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
        n_keep : int

        Returns
        -------
        indices : np.ndarray, shape (n_keep,)
            Local indices of selected samples.
        """
        N_s = X_s.shape[0]
        n_keep = min(n_keep, N_s)
        if n_keep <= 0:
            return np.array([], dtype=int)
        if n_keep >= N_s:
            return np.arange(N_s, dtype=int)

        D = pairwise_distances(X_s, metric="euclidean")

        chosen = [np.random.randint(N_s)]
        dist_to_set = D[chosen[0]].copy()

        for _ in range(1, n_keep):
            farthest = np.argmax(dist_to_set)
            chosen.append(farthest)
            dist_to_set = np.minimum(dist_to_set, D[farthest])

        return np.array(chosen, dtype=int)

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    def evaluate_compression(
        self,
        X_orig: np.ndarray,
        y_orig: np.ndarray,
        X_comp: np.ndarray,
        y_comp: np.ndarray,
        w_comp: np.ndarray,
        eval_fn: Callable[[np.ndarray, np.ndarray], float],
    ) -> dict[str, Any]:
        """Evaluate compression quality by comparing a metric before/after.

        Parameters
        ----------
        X_orig : np.ndarray
        y_orig : np.ndarray
        X_comp : np.ndarray
        y_comp : np.ndarray
        w_comp : np.ndarray
        eval_fn : Callable
            ``eval_fn(y_true, y_pred) -> float``, higher is better.

        Returns
        -------
        result : dict
            Keys: ``original_score``, ``compressed_score``,
            ``retention_ratio``, ``compression_ratio``.
        """
        from scx.utils.evaluation import Evaluation

        # Simple knn-based approximation for evaluation
        from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier

        is_classification = y_orig.dtype in (np.int32, np.int64, int) or (
            len(np.unique(y_orig)) < 20
        )

        if is_classification:
            model_orig = KNeighborsClassifier(n_neighbors=3)
            model_comp = KNeighborsClassifier(n_neighbors=3)
        else:
            model_orig = KNeighborsRegressor(n_neighbors=3)
            model_comp = KNeighborsRegressor(n_neighbors=3)

        # Evaluate on original full data as proxy
        model_orig.fit(X_orig, y_orig)
        y_pred_orig = model_orig.predict(X_orig)
        orig_score = eval_fn(y_orig, y_pred_orig)

        if len(X_comp) > 0:
            try:
                model_comp.fit(X_comp, y_comp, sample_weight=w_comp)
            except TypeError:
                # sklearn >= 1.4 dropped sample_weight from KNN
                model_comp.fit(X_comp, y_comp)
            y_pred_comp = model_comp.predict(X_orig)
            comp_score = eval_fn(y_orig, y_pred_comp)
        else:
            comp_score = 0.0

        cr = X_comp.shape[0] / X_orig.shape[0] if X_orig.shape[0] > 0 else 0.0

        return {
            "original_score": float(orig_score),
            "compressed_score": float(comp_score),
            "retention_ratio": float(comp_score / orig_score) if orig_score != 0 else 0.0,
            "compression_ratio": float(cr),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_weights(scores: np.ndarray, temperature: float = 2.0) -> np.ndarray:
        """Convert redundancy scores to sample weights.

        Lower redundancy -> higher weight.
        """
        w = np.exp(-temperature * scores)
        w_sum = w.sum()
        if w_sum > 0:
            w = w / w_sum * len(w)  # Normalize so mean weight = 1
        return w
