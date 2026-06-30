"""
Learnability Score — L(s) estimation

Core definitions:
    L(s) = C(s) * [1 - N(s)]

    C(s): state-level consistency
    N(s): state-level noise fraction

    NoiseScore(x_i) = r_i / (rho(s) + eps) * [1 - C(s)]
"""

from __future__ import annotations

from typing import Optional

import numpy as np


class LearnabilityScore:
    """State learnability L(s) = C(s) * [1 - N(s)].

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
    # Consistency
    # ------------------------------------------------------------------

    def consistency(
        self,
        X_s: np.ndarray,
        y_s: np.ndarray | None = None,
        expert_preds: np.ndarray | None = None,
    ) -> float:
        """Compute state-level consistency C(s).

        .. note::

            This C(s) is **state-level label consistency** (purity / variance
            compression), **NOT** the multi-expert consistency C(x) from
            Theorem 1.  The Theorem 1 C(x) represents the fraction of experts
            that fail on a given sample:

                C(x) = (1/M) * sum_m e_m(x, y)

            and is computed by :meth:`StateValue.noise_consistency_score()
            <scx.valuation.state_value.StateValue.noise_consistency_score>`.
            The symbol C is reused for two different concepts; treat them
            as independent measures.

        Three measurement modes:

        - **y_s only** (label-based):  ``C_label(s) = 1 - Var(y_s) / Var_total``

          For discrete (classification) labels this is implemented as
          normalised purity::

              C = (p_max - 1/K) / (1 - 1/K)

          where *K* is the number of unique classes and *p_max* the
          majority-class proportion.  This gives 1 when all labels agree
          and 0 when the distribution is uniform.

          For continuous (regression) labels::

              C = 1 / (1 + Var(y_s))

          which maps unbounded variance into the unit interval.

        - **expert_preds only** (expert-consensus)::

              C_expert(s) = 1 - mean( Var_m(f_m(x)) )

          Normalised by dividing through ``mean_var + eps`` so the
          result lies in (0, 1].

        - **both**:  equally weighted average of the two estimates.

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
            Feature matrix for samples in state *s*.  (Currently unused
            in the computation but kept in the signature for future
            feature-space consistency metrics.)
        y_s : np.ndarray, shape (N_s,), optional
            Ground-truth labels for the state.
        expert_preds : np.ndarray, shape (M, N_s), optional
            Predictions made by *M* experts on the same *N_s* samples.

        Returns
        -------
        float
            Consistency score in [0, 1].
        """
        C_label: float | None = None
        C_expert: float | None = None

        # --- Label-based consistency ---------------------------------
        if y_s is not None:
            y_s = np.asarray(y_s).ravel()
            if y_s.size == 0:
                C_label = 0.0
            elif y_s.size == 1:
                C_label = 1.0  # single sample is trivially consistent
            else:
                unique, counts = np.unique(y_s, return_counts=True)
                K = len(unique)
                if K <= 1:
                    C_label = 1.0
                elif y_s.dtype.kind in ("i", "u", "b", "O", "U"):
                    # ---- discrete labels: normalised purity ---------
                    p_max = float(counts.max()) / float(counts.sum())
                    C_label = (p_max - 1.0 / K) / (1.0 - 1.0 / K + self.eps)
                    C_label = max(0.0, min(1.0, C_label))
                else:
                    # ---- continuous labels: variance squash ---------
                    var_y = float(np.var(y_s))
                    C_label = 1.0 / (1.0 + var_y)

        # --- Expert-consensus consistency ----------------------------
        if expert_preds is not None:
            expert_preds = np.asarray(expert_preds)
            if expert_preds.ndim == 1:
                expert_preds = expert_preds[np.newaxis, :]
            M, Ns = expert_preds.shape
            if M <= 1:
                C_expert = 0.5  # single expert cannot judge consensus
            elif Ns == 0:
                C_expert = 0.0
            else:
                # per-sample variance across experts → mean
                var_across = np.var(expert_preds, axis=0, ddof=1)  # (Ns,)
                mean_var = float(np.mean(var_across))
                C_expert = 1.0 - mean_var / (mean_var + self.eps)
                C_expert = max(0.0, min(1.0, C_expert))

        # --- Fuse ----------------------------------------------------
        if C_label is not None and C_expert is not None:
            return 0.5 * C_label + 0.5 * C_expert
        if C_label is not None:
            return C_label
        if C_expert is not None:
            return C_expert
        return 0.5  # no information → neutral

    # ------------------------------------------------------------------
    # Noise score (per-sample)
    # ------------------------------------------------------------------

    def noise_score(
        self,
        residuals: np.ndarray,
        state_proportion: float,
        consistency: float,
    ) -> np.ndarray:
        """Per-sample noise score.

        .. math::

            \\text{NoiseScore}(x_i) =
                \\frac{r_i}{\\rho(s) + \\varepsilon}
                \\cdot \\bigl[1 - C(s)\\bigr]

        Parameters
        ----------
        residuals : np.ndarray, shape (N_s,)
            Per-sample residual / loss *r_i*.
        state_proportion : float
            Proportion of all data belonging to this state, ``rho(s)``.
        consistency : float
            State-level consistency ``C(s)``.

        Returns
        -------
        np.ndarray, shape (N_s,)
            Noise score for each sample.
        """
        residuals = np.asarray(residuals, dtype=float).ravel()
        ratio = residuals / (state_proportion + self.eps)
        return ratio * max(0.0, 1.0 - consistency)

    # ------------------------------------------------------------------
    # Learnability
    # ------------------------------------------------------------------

    def learnability(
        self,
        consistency: float,
        noise_score: float,
    ) -> float:
        """State-level learnability L(s).

        .. math::

            L(s) = C(s) \\cdot \\bigl[1 - N(s)\\bigr] \\quad \\text{clipped to } [0, 1]

        Parameters
        ----------
        consistency : float
            State consistency ``C(s)``.
        noise_score : float
            State-level noise score ``N(s)`` (typically the mean of
            per-sample noise scores).

        Returns
        -------
        float
            Learnability in [0, 1].
        """
        L = consistency * max(0.0, 1.0 - noise_score)
        return float(max(0.0, min(1.0, L)))

    # ------------------------------------------------------------------
    # Composite
    # ------------------------------------------------------------------

    def compute_all(
        self,
        X_s: np.ndarray,
        y_s: np.ndarray | None = None,
        residuals: np.ndarray | None = None,
        state_proportion: float = 1.0,
        expert_preds: np.ndarray | None = None,
    ) -> dict[str, float]:
        """Convenience: compute consistency, noise score, and learnability
        in one call.

        Parameters
        ----------
        X_s : np.ndarray, shape (N_s, d)
        y_s : np.ndarray, shape (N_s,), optional
        residuals : np.ndarray, shape (N_s,), optional
            Per-sample residuals.  If ``None``, a uniform residual of 1.0
            is assumed for every sample so that the noise score reflects
            only density and consistency.
        state_proportion : float
        expert_preds : np.ndarray, shape (M, N_s), optional

        Returns
        -------
        dict
            ``{'consistency': float, 'noise_score': float, 'learnability': float}``
            where ``noise_score`` is the **state-level** mean of the per-sample
            noise scores.
        """
        C = self.consistency(X_s, y_s, expert_preds)

        if residuals is not None:
            ns = self.noise_score(residuals, state_proportion, C)
            N_state = float(np.mean(ns))
        else:
            N_state = 0.0

        L = self.learnability(C, N_state)

        return {
            "consistency": C,
            "noise_score": N_state,
            "learnability": L,
        }
