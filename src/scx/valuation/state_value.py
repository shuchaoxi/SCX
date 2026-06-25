"""
State Value — V(s) computation.

Acquisition value:
    V_add(s) = r_bar(s) * rho(s) * L(s) * [1 - D(s)] * max_m SCX_m(s)

Compression value:
    V_remove(s) = rho(s) * (1 - r_bar(s)) * Sim(s) * (1 - Boundary(s))

High V_add  →  state is valuable for acquisition.
High V_remove  →  state is compressible (redundant).
"""

from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd


class StateValue:
    """State data value V(s).

    The acquisition value scores how beneficial it would be to obtain
    more labels from a state, while the compression value scores how
    much the state can be compressed without significant information
    loss.

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
    # Acquisition value
    # ------------------------------------------------------------------

    def acquisition_value(
        self,
        mean_residual: float,
        proportion: float,
        learnability: float,
        redundancy: float,
        best_scx: float,
    ) -> float:
        """Acquisition value V_add(s).

        .. math::

            V_\\text{add}(s) =
                \\bar{r}(s) \\cdot \\rho(s) \\cdot L(s)
                \\cdot \\bigl[1 - D(s)\\bigr]
                \\cdot \\max_m \\text{SCX}_m(s)

        Returns a non-negative float.

        Parameters
        ----------
        mean_residual : float
            ``r_bar(s)``.
        proportion : float
            ``rho(s)``.
        learnability : float
            ``L(s)``.
        redundancy : float
            ``D(s)``.
        best_scx : float
            ``max_m SCX_m(s)`` — reliability of the best expert.

        Returns
        -------
        float
        """
        return (
            max(0.0, mean_residual)
            * max(0.0, proportion)
            * max(0.0, learnability)
            * max(0.0, 1.0 - redundancy)
            * max(0.0, best_scx)
        )

    # ------------------------------------------------------------------
    # Compression value
    # ------------------------------------------------------------------

    def compression_value(
        self,
        mean_residual: float,
        proportion: float,
        similarity: float,
        boundary: float,
    ) -> float:
        """Compression value V_remove(s).

        .. math::

            V_\\text{remove}(s) =
                \\rho(s) \\cdot (1 - \\bar{r}(s))
                \\cdot \\text{Sim}(s)
                \\cdot (1 - \\text{Boundary}(s))

        A **high** value means the state is homogeneous and well-covered
        and can therefore be compressed aggressively.

        Parameters
        ----------
        mean_residual : float
        proportion : float
        similarity : float
        boundary : float

        Returns
        -------
        float
        """
        return (
            max(0.0, proportion)
            * max(0.0, 1.0 - mean_residual)
            * max(0.0, similarity)
            * max(0.0, 1.0 - boundary)
        )

    # ------------------------------------------------------------------
    # Batch compute
    # ------------------------------------------------------------------

    def compute_all(
        self,
        state_metrics: dict[int, dict[str, float]],
        scx_matrix: np.ndarray,
    ) -> pd.DataFrame:
        """Compute acquisition and compression values for all states.

        Each state's dict in *state_metrics* should contain the keys:

        ``mean_residual``, ``proportion``, ``learnability``,
        ``redundancy``, ``similarity``, ``boundary``.

        Parameters
        ----------
        state_metrics : dict of {state_id: dict}
        scx_matrix : np.ndarray, shape (M, K)
            SCX reliability matrix.

        Returns
        -------
        pd.DataFrame
            Columns:
                ``state_id``, ``V_add``, ``V_remove``, ``best_scx``.
        """
        K = scx_matrix.shape[1]
        records: list[dict] = []

        for s_id in range(K):
            metrics = state_metrics.get(s_id)
            if metrics is None:
                continue

            best_scx = float(np.max(scx_matrix[:, s_id]))

            v_add = self.acquisition_value(
                mean_residual=metrics["mean_residual"],
                proportion=metrics["proportion"],
                learnability=metrics["learnability"],
                redundancy=metrics["redundancy"],
                best_scx=best_scx,
            )

            v_remove = self.compression_value(
                mean_residual=metrics["mean_residual"],
                proportion=metrics["proportion"],
                similarity=metrics.get("similarity", 0.0),
                boundary=metrics.get("boundary", 0.0),
            )

            records.append(
                {
                    "state_id": s_id,
                    "V_add": v_add,
                    "V_remove": v_remove,
                    "best_scx": best_scx,
                }
            )

        return pd.DataFrame(records)

    # ------------------------------------------------------------------
    # Ranking
    # ------------------------------------------------------------------

    def rank_states(
        self,
        values: pd.DataFrame,
        mode: str = "acquire",
    ) -> np.ndarray:
        """Rank states by value (descending).

        Parameters
        ----------
        values : pd.DataFrame
            Must contain ``state_id`` and either ``V_add`` (mode
            ``'acquire'``) or ``V_remove`` (mode ``'compress'``).
        mode : str
            ``'acquire'`` or ``'compress'``.

        Returns
        -------
        np.ndarray
            State IDs sorted from highest to lowest value.
        """
        col = "V_add" if mode == "acquire" else "V_remove"
        if col not in values.columns:
            raise KeyError(
                f"Column '{col}' not found in values DataFrame for mode='{mode}'"
            )
        sorted_df = values.sort_values(col, ascending=False)
        return sorted_df["state_id"].values.astype(int)
