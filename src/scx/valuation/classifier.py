"""
Data Classifier — four-way data classification.

Rules (applied in order):

1. **Expert-dependent**: large expert disagreement (expert_gap > threshold)
2. **Valuable**:      high error, high density, high consistency, low redundancy
3. **Redundant**:     low error, high density, high redundancy
4. **Noisy**:         high error, low density, low consistency
5. **Default**:       valuable (conservative)

Actions:
    valuable         → acquire
    redundant        → compress
    noisy            → downweight or discard
    expert_dependent → route
"""

from __future__ import annotations

from typing import Any, Optional

import numpy as np
import pandas as pd


class DataClassifier:
    """Four-way state classifier: Valuable / Redundant / Noisy / Expert-dependent.

    .. note::

        All thresholds below are **empirical defaults** and may need
        calibration for specific datasets.  Theorem-based alternatives
        are available in :class:`~scx.valuation.state_value.StateValue`:

        * ``error_high`` → :meth:`StateValue.separation_gap()
          <scx.valuation.state_value.StateValue.separation_gap>`
          (uses Theorem 1's :math:`\\mu_s` to derive state-level
          clean-error bounds).

        * ``consistency_high`` and ``noise_high`` → :meth:`StateValue.optimal_noise_threshold()
          <scx.valuation.state_value.StateValue.optimal_noise_threshold>`
          (Theorem 1, Corollary 2)::

              theta* = 1/2 * (1 + mu_max * (K-2)/(K-1))

          replaces the ad-hoc consistency threshold with the optimal
          noise/clean separation threshold.

        * For end-to-end data-driven calibration see
          :class:`~scx.valuation.adaptive.AdaptiveThreshold`.

    Parameters
    ----------
    config : dict, optional
        Threshold overrides.  Default keys:

        ====================  =====  ==================================
        Key                   Default  Description
        ====================  =====  ==================================
        ``error_high``        0.05   Threshold for high mean residual
        ``density_high``      0.05   Threshold for high state proportion
        ``consistency_high``  0.7    Threshold for high consistency
        ``redundancy_high``   0.8    Threshold for high redundancy
        ``noise_high``        0.5    Threshold for high noise score
        ``expert_gap``        0.3    Threshold for expert disagreement
        ====================  =====  ==================================
    """

    def __init__(self, config: dict | None = None) -> None:
        self.thresholds: dict[str, float] = {
            "error_high": 0.05,
            "density_high": 0.05,
            "consistency_high": 0.7,
            "redundancy_high": 0.8,
            "noise_high": 0.5,
            "expert_gap": 0.3,
        }
        if config is not None:
            self.thresholds.update(config)

    # ------------------------------------------------------------------
    # Single-state classification
    # ------------------------------------------------------------------

    def classify_state(
        self,
        mean_residual: float,
        proportion: float,
        consistency: float,
        redundancy: float,
        noise_score: float,
        expert_gap: float | None = None,
    ) -> str:
        """Classify a single state into one of four categories.

        Parameters
        ----------
        mean_residual : float
            ``r_bar(s)`` — mean residual in this state.
        proportion : float
            ``rho(s)`` — fraction of total samples.
        consistency : float
            ``C(s)`` — within-state label/feature consistency.
        redundancy : float
            ``D(s)`` — state redundancy score.
        noise_score : float
            ``N(s)`` — state-level noise score.
        expert_gap : float, optional
            ``max_m SCX_m(s) - min_m SCX_m(s)`` — spread of expert
            reliabilities.  When provided and large (> threshold) the
            state is classified as expert-dependent.

        Returns
        -------
        str
            One of ``'valuable'``, ``'redundant'``, ``'noisy'``,
            ``'expert_dependent'``.
        """
        th = self.thresholds

        # --- Rule 1: expert-dependent ---------------------------------
        if expert_gap is not None and expert_gap > th["expert_gap"]:
            return "expert_dependent"

        # --- Rule 2: valuable -----------------------------------------
        if (
            mean_residual > th["error_high"]
            and proportion > th["density_high"]
            and consistency > th["consistency_high"]
            and redundancy < th["redundancy_high"]
        ):
            return "valuable"

        # --- Rule 3: redundant ----------------------------------------
        if (
            mean_residual < th["error_high"] / 2.0
            and proportion > th["density_high"]
            and redundancy > th["redundancy_high"]
        ):
            return "redundant"

        # --- Rule 4: noisy --------------------------------------------
        if (
            mean_residual > th["error_high"]
            and proportion < th["density_high"]
            and consistency < th["consistency_high"]
        ):
            return "noisy"

        # --- Default: valuable (conservative) -------------------------
        return "valuable"

    # ------------------------------------------------------------------
    # Batch classification
    # ------------------------------------------------------------------

    def classify_all(
        self,
        state_metrics: dict[int, dict[str, float]],
        R_matrix: np.ndarray | None = None,
    ) -> pd.DataFrame:
        """Classify all states and return a DataFrame.

        Parameters
        ----------
        state_metrics : dict of {state_id: dict}
            Each inner dict must contain at least:
            ``mean_residual``, ``proportion``, ``consistency``,
            ``redundancy``, ``noise_score``.
            May optionally contain ``expert_gap``.
        R_matrix : np.ndarray, shape (M, K), optional
            Expert risk matrix.  If provided, the expert gap for each
            state is computed as ``max(R) - min(R)`` along the expert
            axis.

        Returns
        -------
        pd.DataFrame
            Columns:
                ``state_id``, ``category``, ``mean_residual``,
                ``proportion``, ``consistency``, ``redundancy``,
                ``noise_score``, ``expert_gap``.
        """
        records: list[dict[str, Any]] = []

        for state_id, metrics in state_metrics.items():
            gap: float | None = metrics.get("expert_gap", None)
            if gap is None and R_matrix is not None and R_matrix.shape[1] > state_id:
                gap = float(np.max(R_matrix[:, state_id]) - np.min(R_matrix[:, state_id]))

            cat = self.classify_state(
                mean_residual=metrics["mean_residual"],
                proportion=metrics["proportion"],
                consistency=metrics["consistency"],
                redundancy=metrics["redundancy"],
                noise_score=metrics["noise_score"],
                expert_gap=gap,
            )

            records.append(
                {
                    "state_id": state_id,
                    "category": cat,
                    "mean_residual": metrics["mean_residual"],
                    "proportion": metrics["proportion"],
                    "consistency": metrics["consistency"],
                    "redundancy": metrics["redundancy"],
                    "noise_score": metrics["noise_score"],
                    "expert_gap": gap if gap is not None else float("nan"),
                }
            )

        return pd.DataFrame(records)

    # ------------------------------------------------------------------
    # Action recommendation
    # ------------------------------------------------------------------

    @staticmethod
    def recommend_action(state_class: str) -> str:
        """Map a classification label to a recommended action.

        ==================  ====================
        Category            Action
        ==================  ====================
        ``valuable``        ``acquire``
        ``redundant``       ``compress``
        ``noisy``           ``downweight``
        ``expert_dependent`` ``route``
        ==================  ====================

        Parameters
        ----------
        state_class : str
            One of the four classification labels.

        Returns
        -------
        str
            Recommended action.
        """
        mapping = {
            "valuable": "acquire",
            "redundant": "compress",
            "noisy": "downweight",
            "expert_dependent": "route",
        }
        return mapping.get(state_class, "acquire")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    @staticmethod
    def summary(state_classifications: pd.DataFrame) -> str:
        """Generate a human-readable summary string.

        Parameters
        ----------
        state_classifications : pd.DataFrame
            Output of :meth:`classify_all`.

        Returns
        -------
        str
            Multi-line summary with category counts and sample estimates.
        """
        if state_classifications.empty:
            return "No states to classify."

        cats = state_classifications["category"]
        total_states = len(cats)
        total_samples = int(state_classifications["proportion"].sum())

        lines: list[str] = []
        lines.append("=" * 50)
        lines.append("Data Classification Summary")
        lines.append("=" * 50)
        lines.append(f"Total states: {total_states}")

        for cat in ("valuable", "redundant", "noisy", "expert_dependent"):
            mask = cats == cat
            n_states = int(mask.sum())
            if n_states > 0:
                prop_sum = state_classifications.loc[mask, "proportion"].sum()
                lines.append(
                    f"  {cat:20s}: {n_states:3d} states  "
                    f"({prop_sum * total_samples:.0f} est. samples)"
                )
            else:
                lines.append(f"  {cat:20s}: {n_states:3d} states")

        lines.append("=" * 50)
        return "\n".join(lines)
