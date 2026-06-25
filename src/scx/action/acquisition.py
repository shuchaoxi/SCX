# scx/action/acquisition.py
# AcquisitionStrategy -- state-level active acquisition strategies.

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import pairwise_distances


class AcquisitionStrategy:
    """State-level acquisition strategy.

    Instead of point-wise uncertainty sampling, this strategy first selects
    high-value states and then picks representative samples within each
    state.

    Parameters
    ----------
    strategy : str
        Sample selection method inside a state:

        - ``"random"``       : uniform random sampling.
        - ``"coreset"``      : farthest-point / k-center greedy.
        - ``"uncertainty"``  : highest-uncertainty sampling.
        - ``"scx_value"``    : rank by SCX sample-value score.
    """

    def __init__(self, strategy: str = "coreset"):
        valid = ("random", "coreset", "uncertainty", "scx_value")
        if strategy not in valid:
            raise ValueError(
                f"Unknown strategy '{strategy}'. Expected one of {valid}."
            )
        self.strategy = strategy

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def select_samples(
        self,
        X_s: np.ndarray,
        n_samples: int,
        state_id: int = -1,
        **kwargs: Any,
    ) -> np.ndarray:
        """Select ``n_samples`` representative samples from state *s*.

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
            Feature / representation matrix for samples in state *s*.
        n_samples : int
            Number of samples to select (clipped to ``N_s``).
        state_id : int
            State identifier (used for logging / context).
        **kwargs : Any
            Strategy-specific keyword arguments:

            - ``uncertainties`` : ``(N_s,)`` array required when
              ``strategy='uncertainty'``.
            - ``sample_values`` : ``(N_s,)`` array required when
              ``strategy='scx_value'``.

        Returns
        -------
        indices : np.ndarray, shape (n_samples,)
            Local indices within ``X_s`` of the selected samples.
        """
        N_s = X_s.shape[0]
        n = min(n_samples, N_s)

        if n <= 0:
            return np.array([], dtype=int)

        dispatch = {
            "random": self._random_select,
            "coreset": self.coreset_select,
            "uncertainty": self._uncertainty_select_wrapper,
            "scx_value": self._scx_value_select_wrapper,
        }
        selector = dispatch.get(self.strategy, self._random_select)

        if self.strategy == "uncertainty":
            uncertainties = kwargs.get("uncertainties")
            if uncertainties is None:
                raise ValueError("'uncertainties' required for uncertainty strategy.")
            return selector(X_s, n, uncertainties=uncertainties)

        if self.strategy == "scx_value":
            sample_values = kwargs.get("sample_values")
            if sample_values is None:
                raise ValueError("'sample_values' required for scx_value strategy.")
            return selector(X_s, n, sample_values=sample_values)

        return selector(X_s, n)

    def coreset_select(
        self, X_s: np.ndarray, n_samples: int, **kwargs: Any
    ) -> np.ndarray:
        """Farthest-point / k-center greedy sampling.

        Iteratively picks the sample farthest from the current set.

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
        n_samples : int
        **kwargs : Any

        Returns
        -------
        indices : np.ndarray, shape (n_samples,)
        """
        N_s = X_s.shape[0]
        n = min(n_samples, N_s)
        if n <= 0:
            return np.array([], dtype=int)
        if n >= N_s:
            return np.arange(N_s, dtype=int)

        # Distance matrix
        D = pairwise_distances(X_s, metric="euclidean")

        # Greedy k-center (farthest-point traversal)
        chosen = [np.random.randint(N_s)]
        dist_to_set = D[chosen[0]].copy()

        for _ in range(1, n):
            farthest = np.argmax(dist_to_set)
            chosen.append(farthest)
            dist_to_set = np.minimum(dist_to_set, D[farthest])

        return np.array(chosen, dtype=int)

    def uncertainty_select(
        self, uncertainties: np.ndarray, n_samples: int
    ) -> np.ndarray:
        """Select the *n_samples* most uncertain samples.

        Parameters
        ----------
        uncertainties : np.ndarray, shape (N_s,)
            Uncertainty score per sample (higher = more uncertain).
        n_samples : int

        Returns
        -------
        indices : np.ndarray, shape (n_samples,)
        """
        n = min(n_samples, len(uncertainties))
        if n <= 0:
            return np.array([], dtype=int)
        return np.argsort(uncertainties)[::-1][:n]

    def scx_value_select(
        self,
        X_s: np.ndarray,
        sample_values: np.ndarray,
        n_samples: int,
    ) -> np.ndarray:
        """Select samples by SCX sample-value score.

        Higher score = higher priority for acquisition.

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
        sample_values : np.ndarray, shape (N_s,)
            Per-sample SCX value scores.
        n_samples : int

        Returns
        -------
        indices : np.ndarray, shape (n_samples,)
        """
        n = min(n_samples, len(sample_values))
        if n <= 0:
            return np.array([], dtype=int)
        return np.argsort(sample_values)[::-1][:n]

    def compare_strategies(
        self,
        X_s: np.ndarray,
        y_s: np.ndarray,
        n_samples: int,
    ) -> dict[str, Any]:
        """Compare different strategies on the same state data.

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
        y_s : np.ndarray, shape (N_s,)
            Labels (used for diversity / coverage heuristics).
        n_samples : int

        Returns
        -------
        results : dict
            Keys are strategy names, values are dicts with ``indices``
            and heuristic quality scores.
        """
        results: dict[str, Any] = {}
        strategies = ["random", "coreset"]

        for strat in strategies:
            saved = self.strategy
            self.strategy = strat
            indices = self.select_samples(
                X_s, n_samples, uncertainties=np.random.rand(len(X_s))
                if strat == "uncertainty" else None,
            )
            self.strategy = saved

            cov = self._coverage_score(X_s, indices)
            div = self._diversity_score(X_s, indices)
            results[strat] = {
                "indices": indices,
                "coverage": float(cov),
                "diversity": float(div),
            }

        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _random_select(
        self, X_s: np.ndarray, n_samples: int, **kwargs: Any
    ) -> np.ndarray:
        N_s = X_s.shape[0]
        n = min(n_samples, N_s)
        if n <= 0:
            return np.array([], dtype=int)
        return np.random.choice(N_s, size=n, replace=False).astype(int)

    def _uncertainty_select_wrapper(
        self, X_s: np.ndarray, n_samples: int, **kwargs: Any
    ) -> np.ndarray:
        uncertainties = kwargs.get("uncertainties")
        if uncertainties is None:
            raise ValueError("'uncertainties' required.")
        return self.uncertainty_select(uncertainties, n_samples)

    def _scx_value_select_wrapper(
        self, X_s: np.ndarray, n_samples: int, **kwargs: Any
    ) -> np.ndarray:
        sample_values = kwargs.get("sample_values")
        if sample_values is None:
            raise ValueError("'sample_values' required.")
        return self.scx_value_select(X_s, sample_values, n_samples)

    @staticmethod
    def _coverage_score(X_s: np.ndarray, indices: np.ndarray) -> float:
        """Compute coverage as mean distance from selected set to all points."""
        if len(indices) == 0:
            return 0.0
        selected = X_s[indices]
        D = pairwise_distances(selected, X_s, metric="euclidean")
        min_dists = D.min(axis=0)
        return float(min_dists.mean())

    @staticmethod
    def _diversity_score(X_s: np.ndarray, indices: np.ndarray) -> float:
        """Compute diversity as mean pairwise distance within selected set."""
        if len(indices) < 2:
            return 0.0
        selected = X_s[indices]
        D = pairwise_distances(selected, metric="euclidean")
        return float(D[np.triu_indices_from(D, k=1)].mean())
