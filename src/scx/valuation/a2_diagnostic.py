"""
A2' Correlation Diagnostic — Assumption A2 (conditional independence) check.

Assumption A2 states that expert errors e_m(x, y) are conditionally independent
given x for clean samples.  This follows from A1 (disjoint training sets), but
in practice residual correlations may arise from:

- Shared pre-training data
- Similar model architectures
- Feature-space correlations when the state structure is coarse

This module provides diagnostic tools to estimate the worst-case pairwise
correlation of expert errors within each state and compute the effective
expert count M_eff = M / (1 + (M-1)*rho_bar).

.. note::

    The "variance-inflated Hoeffding" formula
    exp(-2 M Delta^2 / (1 + (M-1)*rho)) is **heuristic**, not a rigorous
    theorem.  These diagnostics are intended for empirical awareness, not
    for deriving modified theoretical bounds.
"""

from __future__ import annotations

from typing import Optional

import numpy as np


class A2Diagnostic:
    """Test Assumption A2' (bounded expert error correlation).

    Estimates the worst-case pairwise correlation of expert error indicators
    within each state, and computes the effective sample size reduction due
    to correlation.

    Parameters
    ----------
    eps : float, optional
        Small constant to avoid division by zero (default 1e-8).
    """

    def __init__(self, eps: float = 1e-8) -> None:
        if eps <= 0:
            raise ValueError(f"eps must be positive, got {eps}")
        self.eps = eps

    def estimate_pairwise_correlation(
        self,
        expert_errors: np.ndarray,
        state_labels: np.ndarray,
    ) -> dict:
        """Estimate worst-case pairwise correlation :math:`\\bar{\\rho}_s`.

        For each state :math:`s`, computes the Pearson correlation between
        every pair of expert error indicators, then takes the maximum
        pairwise correlation as :math:`\\bar{\\rho}_s`.

        Parameters
        ----------
        expert_errors : np.ndarray, shape (M, N)
            Binary error indicators: ``expert_errors[m, i]`` is 1 if expert
            *m* fails on sample *i*, 0 otherwise.
        state_labels : np.ndarray, shape (N,)
            State assignment for each sample, values in {0, ..., S-1}.

        Returns
        -------
        dict
            Keys:
            ``per_state`` : dict of {state_id: float}
                Maximum pairwise correlation :math:`\\bar{\\rho}_s` per state.
            ``max_correlation`` : float
                Global maximum across all states.
            ``mean_correlation`` : float
                State-proportion-weighted mean correlation.
            ``n_states`` : int
                Number of states with sufficient samples.
            ``state_label_counts`` : dict of {state_id: int}
                Number of samples per state.
        """
        eps = self.eps
        expert_errors = np.asarray(expert_errors, dtype=float)
        state_labels = np.asarray(state_labels, dtype=int)

        if expert_errors.ndim != 2:
            raise ValueError(
                f"expert_errors must be 2-D (M, N), got shape "
                f"{expert_errors.shape}"
            )
        M, N = expert_errors.shape
        if state_labels.shape[0] != N:
            raise ValueError(
                f"state_labels length {state_labels.shape[0]} does not "
                f"match expert_errors samples {N}"
            )

        unique_states = np.unique(state_labels)
        per_state_corr: dict[int, float] = {}
        state_counts: dict[int, int] = {}

        for s in unique_states:
            mask = state_labels == s
            n_s = int(mask.sum())
            state_counts[int(s)] = n_s

            if n_s < 2 or M < 2:
                per_state_corr[int(s)] = float("nan")
                continue

            # Extract error matrix for this state: (M, n_s)
            errors_s = expert_errors[:, mask]

            # Compute pairwise correlation matrix across experts (M x M)
            # For binary data, Pearson correlation is appropriate
            corr_matrix = np.corrcoef(errors_s)

            # Mask the diagonal (self-correlation = 1)
            # Extract strict upper triangle for pairwise correlations
            triu_idx = np.triu_indices(M, k=1)
            pairwise_corr = corr_matrix[triu_idx]

            if len(pairwise_corr) == 0:
                per_state_corr[int(s)] = float("nan")
                continue

            # Maximum absolute pairwise correlation
            max_corr = float(np.max(np.abs(pairwise_corr)))
            per_state_corr[int(s)] = max_corr

        # Global statistics
        corr_values = [v for v in per_state_corr.values() if not np.isnan(v)]
        if not corr_values:
            return {
                "per_state": per_state_corr,
                "max_correlation": float("nan"),
                "mean_correlation": float("nan"),
                "n_states": 0,
                "state_label_counts": state_counts,
            }

        max_correlation = float(max(corr_values))

        # Proportion-weighted mean
        total_weighted = 0.0
        total_weight = 0.0
        for s, corr_val in per_state_corr.items():
            if not np.isnan(corr_val):
                weight = float(state_counts.get(s, 0))
                total_weight += weight
                total_weighted += weight * corr_val
        mean_correlation = (
            total_weighted / total_weight if total_weight > eps else float("nan")
        )

        return {
            "per_state": per_state_corr,
            "max_correlation": max_correlation,
            "mean_correlation": mean_correlation,
            "n_states": len(corr_values),
            "state_label_counts": state_counts,
        }

    def effective_expert_count(
        self,
        M: int,
        rho_bar: float,
    ) -> float:
        """Compute effective expert count under correlation.

        .. math::

            M_{\\text{eff}} = \\frac{M}{1 + (M - 1) \\bar{\\rho}}

        where :math:`\\bar{\\rho}` is the worst-case pairwise correlation.

        This represents the equivalent number of independent experts given
        the observed correlation.  It is a **heuristic diagnostic**, not a
        rigorous replacement for :math:`M` in concentration inequalities.

        Parameters
        ----------
        M : int
            Nominal number of experts.
        rho_bar : float
            Maximum pairwise correlation :math:`\\bar{\\rho} \\in [0, 1]`.

        Returns
        -------
        float
            Effective expert count :math:`M_{\\text{eff}}`.  Returns
            ``M`` if :math:`\\bar{\\rho} = 0`, and 1.0 if
            :math:`\\bar{\\rho} \\geq 1`.
        """
        if M < 1:
            return 0.0
        rho_bar = float(np.clip(rho_bar, 0.0, 1.0))
        denom = 1.0 + (float(M) - 1.0) * rho_bar
        if denom <= 0.0:
            return 1.0
        return float(M) / denom

    def warn_if_correlated(
        self,
        rho_bar: float,
        threshold: float = 0.2,
        M: Optional[int] = None,
    ) -> dict:
        """Warn if the pairwise correlation exceeds a safe threshold.

        Parameters
        ----------
        rho_bar : float
            Estimated maximum pairwise correlation :math:`\\bar{\\rho}`.
        threshold : float, optional
            Correlation threshold for warning (default 0.2).
        M : int, optional
            If provided, also reports the effective expert count.

        Returns
        -------
        dict
            ``correlation`` : float
                The input correlation.
            ``exceeds_threshold`` : bool
                Whether :math:`\\bar{\\rho} >` *threshold*.
            ``threshold`` : float
                The threshold used.
            ``severity`` : str
                ``'low'``, ``'moderate'``, or ``'high'``.
            ``effective_expert_count`` : float or None
                Only present if *M* is provided.
            ``message`` : str
                Human-readable diagnostic message.
        """
        rho_bar = float(rho_bar)
        exceeds = rho_bar > threshold

        if rho_bar < 0.1:
            severity = "low"
            msg = f"A2 appears satisfied (rho_bar={rho_bar:.3f} < 0.1)."
        elif rho_bar < 0.3:
            severity = "moderate"
            msg = (
                f"Mild correlation detected (rho_bar={rho_bar:.3f}). "
                f"Check that training sets are truly disjoint (A1)."
            )
        else:
            severity = "high"
            msg = (
                f"Strong correlation detected (rho_bar={rho_bar:.3f}). "
                f"A2 may be violated. Verify disjoint training sets and "
                f"consider whether shared pre-training data is inflating "
                f"expert agreement."
            )

        result: dict = {
            "correlation": rho_bar,
            "exceeds_threshold": exceeds,
            "threshold": threshold,
            "severity": severity,
            "message": msg,
        }

        if M is not None:
            M_eff = self.effective_expert_count(M, rho_bar)
            result["effective_expert_count"] = M_eff
            result["M_nominal"] = M
            result["message"] += (
                f"  M_eff = {M_eff:.1f} (out of M = {M} nominal experts)."
            )

        return result
