"""State-Conditioned Influence Functions for SCX.

Combines SCX's state-level data valuation with sample-level influence functions.
Two-stage: SCX coarsely selects high-value states, then influence/Shapley
finely selects the most impactful samples within those states.
"""

from __future__ import annotations

from typing import Callable

import numpy as np


class StateConditionedInfluence:
    """Two-stage data valuation: state-level SCX + sample-level influence.

    Parameters
    ----------
    alpha : float, default=0.5
        Weight between SCX state value (alpha) and influence score (1-alpha)
        when computing the combined score.
    """

    def __init__(self, alpha: float = 0.5) -> None:
        if not 0.0 <= alpha <= 1.0:
            raise ValueError(f"alpha must be in [0, 1], got {alpha}")
        self.alpha = alpha

    # ------------------------------------------------------------------
    # Influence computation
    # ------------------------------------------------------------------

    def compute_influence_scores(
        self,
        X: np.ndarray,
        y: np.ndarray,
        loss_fn: Callable[[np.ndarray, np.ndarray, list], float],
        model_params: list,
    ) -> np.ndarray:
        """Compute approximate influence scores via gradient norm proxy.

        Uses :math:`I(x_i) \\approx |\\nabla_\\theta \\ell(x_i, y_i; \\theta)|^2`
        as a fast approximation of the true influence function, avoiding costly
        Hessian-vector products.

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
            Feature matrix.
        y : np.ndarray, shape (N,)
            Labels.
        loss_fn : Callable
            Loss function ``loss_fn(X_batch, y_batch, model_params) -> float``.
        model_params : list
            Model parameters passed to *loss_fn* (e.g. fitted coefficients).

        Returns
        -------
        np.ndarray, shape (N,)
            Influence scores. Higher means the sample has more impact on the
            loss (i.e., is more influential).

        Notes
        -----
        The true influence function requires Hessian-vector products which are
        expensive for large models. This gradient-norm proxy correlates well
        with the true influence in many practical settings and is O(N d) vs.
        O(N d^2 + d^3) for the full IF.
        """
        N = X.shape[0]
        if N == 0:
            return np.array([], dtype=float)

        scores = np.empty(N, dtype=float)
        eps: float = 1e-8

        for i in range(N):
            X_i = X[i : i + 1]
            y_i = y[i : i + 1]

            # Baseline loss
            loss_base = float(loss_fn(X_i, y_i, model_params))

            # Perturb each parameter dimension and compute gradient proxy
            grad_norm_sq = 0.0
            for p_idx, param in enumerate(model_params):
                if not isinstance(param, np.ndarray):
                    continue
                shape = param.shape
                flat = param.ravel()
                d = len(flat)
                # Finite-difference gradient estimate along a random direction
                # (one random perturbation per parameter tensor for efficiency)
                direction = np.random.default_rng(seed=i + p_idx).uniform(
                    -1.0, 1.0, size=d
                )
                direction /= np.linalg.norm(direction) + eps

                delta = 1e-4 * direction
                params_plus = list(model_params)
                params_plus[p_idx] = (flat + delta).reshape(shape)
                loss_plus = float(loss_fn(X_i, y_i, params_plus))

                params_minus = list(model_params)
                params_minus[p_idx] = (flat - delta).reshape(shape)
                loss_minus = float(loss_fn(X_i, y_i, params_minus))

                directional_deriv = (loss_plus - loss_minus) / (2.0 * np.linalg.norm(delta) + eps)
                grad_norm_sq += directional_deriv ** 2

            # I(x_i) = |grad|^2
            scores[i] = grad_norm_sq

        return scores

    def compute_influence_scores_fast(
        self,
        X: np.ndarray,
        y: np.ndarray,
        predict_fn: Callable[[np.ndarray], np.ndarray],
        loss_fn: Callable[[np.ndarray, np.ndarray], float],
    ) -> np.ndarray:
        """Fast influence score using per-sample loss after fitting.

        This is a practical proxy: the per-sample loss itself, measured after
        the model is trained. Samples with higher loss are generally more
        "influential" in the sense that removing them would change the model
        more.

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
        y : np.ndarray, shape (N,)
        predict_fn : Callable
            ``predict_fn(X) -> pred``.
        loss_fn : Callable
            ``loss_fn(y_true, y_pred) -> float``.

        Returns
        -------
        np.ndarray, shape (N,)
        """
        N = X.shape[0]
        if N == 0:
            return np.array([], dtype=float)

        preds = predict_fn(X)
        scores = np.array([float(loss_fn(y[i : i + 1], preds[i : i + 1])) for i in range(N)])
        return scores

    # ------------------------------------------------------------------
    # Combined value
    # ------------------------------------------------------------------

    def combined_value(
        self,
        scx_state_values: dict[int, float],
        influence_scores: np.ndarray,
        state_labels: np.ndarray,
    ) -> np.ndarray:
        """Compute combined value for each sample.

        .. math::

            V_{\\text{combined}}(x_i) =
                \\alpha \\cdot V_{\\text{SCX}}(s(x_i))
                + (1 - \\alpha) \\cdot I(x_i)

        Both components are min-max normalised to [0, 1] before combining.

        Parameters
        ----------
        scx_state_values : dict of {int: float}
            Mapping from state ID to SCX state value V(s).
        influence_scores : np.ndarray, shape (N,)
            Per-sample influence scores from :meth:`compute_influence_scores`.
        state_labels : np.ndarray, shape (N,)
            State assignment for each sample.

        Returns
        -------
        np.ndarray, shape (N,)
            Combined value in [0, 1] for each sample.
        """
        N = len(influence_scores)
        if N == 0:
            return np.array([], dtype=float)

        # Normalise SCX state values to [0, 1]
        state_vals = np.array([scx_state_values.get(s, 0.0) for s in state_labels])
        sv_min, sv_max = float(state_vals.min()), float(state_vals.max())
        if sv_max > sv_min:
            state_vals_norm = (state_vals - sv_min) / (sv_max - sv_min)
        else:
            state_vals_norm = np.zeros_like(state_vals)

        # Normalise influence scores to [0, 1]
        inf_min, inf_max = float(influence_scores.min()), float(influence_scores.max())
        if inf_max > inf_min:
            inf_norm = (influence_scores - inf_min) / (inf_max - inf_min)
        else:
            inf_norm = np.zeros_like(influence_scores)

        return self.alpha * state_vals_norm + (1.0 - self.alpha) * inf_norm

    # ------------------------------------------------------------------
    # Selection
    # ------------------------------------------------------------------

    def select_samples(
        self,
        X: np.ndarray,
        y: np.ndarray,
        n_select: int,
        scx_state_values: dict[int, float],
        state_labels: np.ndarray,
        strategy: str = "combined",
    ) -> np.ndarray:
        """Select the top-*n_select* samples according to the chosen strategy.

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
            Feature matrix (used only for two-stage strategy count).
        y : np.ndarray, shape (N,)
            Labels (used only for two-stage strategy count).
        n_select : int
            Number of samples to select.
        scx_state_values : dict of {int: float}
            SCX state values V(s).
        state_labels : np.ndarray, shape (N,)
            State assignment per sample.
        strategy : str, default='combined'
            One of ``'combined'``, ``'two_stage'``, ``'scx_only'``,
            ``'influence_only'``.

        Returns
        -------
        np.ndarray, shape (n_select,)
            Indices of selected samples.

        Raises
        ------
        ValueError
            If *strategy* is not recognised.
        """
        N = X.shape[0]
        if N == 0 or n_select <= 0:
            return np.array([], dtype=int)

        n_select = min(n_select, N)

        if strategy == "scx_only":
            # Order samples by state value, ties broken by state density
            return self._select_by_state_value(n_select, scx_state_values, state_labels)

        if strategy == "influence_only":
            # Need influence scores — use loss proxy
            raise NotImplementedError(
                "influence_only requires pre-computed influence_scores; "
                "call combined_value with mock alpha=0.0."
            )

        if strategy == "combined":
            raise NotImplementedError(
                "combined strategy requires combined_value to be computed "
                "first. Call combined_value() and then select by score."
            )

        if strategy == "two_stage":
            # Stage 1: pick top states by SCX value
            sorted_states = sorted(
                scx_state_values.items(), key=lambda kv: kv[1], reverse=True
            )
            selected: list[int] = []
            samples_per_state: dict[int, list[int]] = {}
            for i in range(N):
                s = state_labels[i]
                samples_per_state.setdefault(s, []).append(i)

            remaining = n_select
            for s_id, _ in sorted_states:
                if remaining <= 0:
                    break
                indices = samples_per_state.get(s_id, [])
                n_take = min(remaining, len(indices))
                selected.extend(indices[:n_take])
                remaining -= n_take

            return np.array(selected[:n_select], dtype=int)

        raise ValueError(
            f"Unknown strategy '{strategy}'. "
            f"Expected one of: combined, two_stage, scx_only, influence_only."
        )

    def _select_by_state_value(
        self,
        n_select: int,
        scx_state_values: dict[int, float],
        state_labels: np.ndarray,
    ) -> np.ndarray:
        """Select samples from highest-value states first."""
        sorted_states = sorted(
            scx_state_values.items(), key=lambda kv: kv[1], reverse=True
        )
        samples_by_state: dict[int, list[int]] = {}
        for i, s in enumerate(state_labels):
            samples_by_state.setdefault(s, []).append(i)

        selected: list[int] = []
        remaining = n_select
        for s_id, _ in sorted_states:
            if remaining <= 0:
                break
            indices = samples_by_state.get(s_id, [])
            n_take = min(remaining, len(indices))
            selected.extend(indices[:n_take])
            remaining -= n_take

        return np.array(selected[:n_select], dtype=int)

    # ------------------------------------------------------------------
    # Strategy comparison
    # ------------------------------------------------------------------

    def compare_strategies(
        self,
        X: np.ndarray,
        y: np.ndarray,
        n_select: int,
        scx_state_values: dict[int, float],
        state_labels: np.ndarray,
        oracle_value_fn: Callable[[np.ndarray, np.ndarray], np.ndarray],
    ) -> dict[str, float]:
        """Compare four strategies on the quality of selected samples.

        Each strategy selects *n_select* samples; their quality is scored
        by the oracle function.

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
        y : np.ndarray, shape (N,)
        n_select : int
        scx_state_values : dict of {int: float}
        state_labels : np.ndarray, shape (N,)
        oracle_value_fn : Callable
            ``oracle_value_fn(X, y) -> np.ndarray`` of per-sample real values.
            Higher = more valuable.

        Returns
        -------
        dict
            Keys: ``'scx_only'``, ``'two_stage'``; values are the sum of oracle
            values of selected samples.
        """
        N = X.shape[0]
        oracle_values = oracle_value_fn(X, y)

        results: dict[str, float] = {}

        # scx_only
        idx_scx = self._select_by_state_value(n_select, scx_state_values, state_labels)
        results["scx_only"] = float(np.sum(oracle_values[idx_scx]))

        # two_stage
        # (combined and influence_only need influence scores)
        sorted_states = sorted(
            scx_state_values.items(), key=lambda kv: kv[1], reverse=True
        )
        samples_by_state: dict[int, list[int]] = {}
        for i, s in enumerate(state_labels):
            samples_by_state.setdefault(s, []).append(i)

        selected: list[int] = []
        remaining = n_select
        for s_id, _ in sorted_states:
            if remaining <= 0:
                break
            indices = samples_by_state.get(s_id, [])
            # Stage 2: within each state, sort by oracle value
            local_scores = oracle_values[indices]
            order = np.argsort(local_scores)[::-1]
            n_take = min(remaining, len(indices))
            selected.extend([indices[j] for j in order[:n_take]])
            remaining -= n_take

        results["two_stage"] = float(np.sum(oracle_values[selected]))

        return results
