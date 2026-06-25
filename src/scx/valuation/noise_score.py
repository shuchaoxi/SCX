"""
Noise Score — per-sample and per-state noise estimation.

Core definition:
    NoiseScore(x_i) = (r_i * w_density / (rho(s) + eps)) * (1 - C(s)) * w_consistency
"""

from __future__ import annotations

from typing import Optional

import numpy as np


class NoiseScore:
    """Sample-level and state-level noise scoring.

    The noise score captures how likely a sample (or state) is to be
    "noisy": high residual *and* low density *and* low consistency
    produces a high noise score.

    Parameters
    ----------
    eps : float
        Small constant to avoid division by zero.
    density_weight : float
        Weight for the density term ``1 / (rho + eps)``.
    consistency_weight : float
        Weight for the consistency term ``(1 - C)``.
    """

    def __init__(
        self,
        eps: float = 1e-8,
        density_weight: float = 1.0,
        consistency_weight: float = 1.0,
    ) -> None:
        if eps <= 0:
            raise ValueError(f"eps must be positive, got {eps}")
        self.eps = eps
        self.density_weight = density_weight
        self.consistency_weight = consistency_weight

    # ------------------------------------------------------------------
    # Per-sample noise score
    # ------------------------------------------------------------------

    def compute(
        self,
        residuals: np.ndarray,
        state_proportion: float,
        consistency: float,
    ) -> np.ndarray:
        """Per-sample noise score.

        .. math::

            \\text{NoiseScore}(x_i) =
                \\frac{r_i \\cdot w_\\rho}{\\rho(s) + \\varepsilon}
                \\cdot \\bigl[1 - C(s)\\bigr] \\cdot w_C

        Parameters
        ----------
        residuals : np.ndarray, shape (N_s,)
            Per-sample residuals / losses.
        state_proportion : float
            ``rho(s)`` — fraction of all data belonging to this state.
        consistency : float
            ``C(s)`` — within-state consistency.

        Returns
        -------
        np.ndarray, shape (N_s,)
            Non-negative noise score for each sample.
        """
        residuals = np.asarray(residuals, dtype=float).ravel()
        if residuals.size == 0:
            return np.array([], dtype=float)

        density_term = self.density_weight / (state_proportion + self.eps)
        consistency_term = self.consistency_weight * max(0.0, 1.0 - consistency)

        scores = residuals * density_term * consistency_term
        # Guard against negative scores from floating point edge cases
        return np.maximum(scores, 0.0)

    # ------------------------------------------------------------------
    # State-level noise score
    # ------------------------------------------------------------------

    def compute_state_level(
        self,
        mean_residual: float,
        state_proportion: float,
        consistency: float,
    ) -> float:
        """State-level noise score (scalar).

        Equivalent to applying :meth:`compute` but with a single
        residual value (the state mean).

        Parameters
        ----------
        mean_residual : float
            ``r_bar(s)`` — mean residual in this state.
        state_proportion : float
        consistency : float

        Returns
        -------
        float
        """
        density_term = self.density_weight / (state_proportion + self.eps)
        consistency_term = self.consistency_weight * max(0.0, 1.0 - consistency)
        score = mean_residual * density_term * consistency_term
        return max(0.0, score)

    # ------------------------------------------------------------------
    # Detection helpers
    # ------------------------------------------------------------------

    def detect_noisy_states(
        self,
        state_noise_scores: np.ndarray,
        threshold: float = 0.5,
    ) -> np.ndarray:
        """Identify states whose noise score exceeds a threshold.

        Parameters
        ----------
        state_noise_scores : np.ndarray, shape (K,)
            Noise score for each state.
        threshold : float
            States with score > *threshold* are flagged.

        Returns
        -------
        np.ndarray
            1-D array of state IDs (indices) flagged as noisy.
        """
        scores = np.asarray(state_noise_scores, dtype=float).ravel()
        return np.where(scores > threshold)[0]

    def detect_noisy_samples(
        self,
        sample_noise_scores: np.ndarray,
        threshold: float | None = None,
    ) -> np.ndarray:
        """Identify samples whose noise score exceeds a threshold.

        When *threshold* is ``None``, an automatic threshold is derived
        via the **IQR rule**::

            upper_fence = Q3 + 1.5 * IQR

        Parameters
        ----------
        sample_noise_scores : np.ndarray, shape (N,)
            Per-sample noise scores.
        threshold : float, optional
            Manual threshold.  When ``None``, the IQR rule is used.

        Returns
        -------
        np.ndarray
            1-D array of sample indices flagged as noisy.
        """
        scores = np.asarray(sample_noise_scores, dtype=float).ravel()
        if scores.size == 0:
            return np.array([], dtype=int)

        if threshold is None:
            q1 = float(np.percentile(scores, 25))
            q3 = float(np.percentile(scores, 75))
            iqr = q3 - q1
            threshold = q3 + 1.5 * iqr

        return np.where(scores > threshold)[0]
