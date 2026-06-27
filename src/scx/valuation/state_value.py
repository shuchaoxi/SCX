"""
State Value — V(s) computation and theorem-based noise detection bounds.

This module provides two sets of functionality:

**Legacy V(s) formulas** (deprecated):
    Acquisition value: V_add(s) = r_bar(s) * rho(s) * L(s) * [1 - D(s)] * max_m SCX_m(s)
    Compression value: V_remove(s) = rho(s) * (1 - r_bar(s)) * Sim(s) * (1 - Boundary(s))

**Theorem-based methods** (new in v0.6):
    Theorem 1 — Noise detection guarantee via multi-expert consistency:
        C(x) = (1/M) * sum e_m(x, y)          (noise_consistency_score)
        theta* = 1/2 * (1 + mu_max * (K-2)/(K-1))   (optimal_noise_threshold)
        F1 >= 1 - (1/eta) * sum rho_s * exp(-2M * Delta_s^2)  (noise_detection_f1_bound)

    Theorem 2 — Weak feature failure bound:
        F1 <= F1_base + C_F * sqrt(2*delta)
        where delta = I(phi(X); s(X))          (feature_strength_diagnostic)
"""

from __future__ import annotations

import warnings
from typing import Optional

import numpy as np
import pandas as pd


# ======================================================================
# Utility functions — Hoeffding & Chernoff bounds (Theorem 1)
# ======================================================================


def hoeffding_bound(n: int, epsilon: float) -> float:
    """Hoeffding tail bound for a bounded random variable in [0, 1].

    .. math::

        P(\\bar{X} - \\mathbb{E}[\\bar{X}] > \\varepsilon) \\le
            \\exp(-2 n \\varepsilon^2)

    Parameters
    ----------
    n : int
        Number of independent observations.
    epsilon : float
        Deviation from the mean (must be >= 0).

    Returns
    -------
    float
        The probability bound :math:`\\exp(-2 n \\varepsilon^2)`.
    """
    if n <= 0:
        return 1.0
    if epsilon <= 0.0:
        return 1.0
    return float(np.exp(-2.0 * n * epsilon**2))


def chernoff_bound(p: float, q: float, n: int) -> float:
    """Chernoff (KL) tail bound for a Bernoulli random variable.

    .. math::

        P(\\bar{X} > q \\mid \\mathbb{E}[\\bar{X}] = p) \\le
            \\exp(-n \\cdot \\mathrm{KL}(q \\,\\|\\, p))

    where :math:`\\mathrm{KL}(q \\,\\|\\, p) = q \\log\\frac{q}{p}
    + (1-q)\\log\\frac{1-q}{1-p}`.

    Parameters
    ----------
    p : float
        True mean (expected value) of the Bernoulli, in (0, 1).
    q : float
        Threshold to exceed, in (0, 1).
    n : int
        Number of independent trials.

    Returns
    -------
    float
        The Chernoff bound :math:`\\exp(-n \\cdot \\mathrm{KL}(q \\,\\|\\, p))`.
        Returns 0.0 when edge cases produce degenerate KL divergence.
    """
    # Bound is vacuous when threshold does not exceed the mean
    if q <= p:
        return 1.0
    if n <= 0:
        return 1.0
    # Handle edge cases at distribution boundaries
    if p <= 0.0 or p >= 1.0 or q <= 0.0 or q >= 1.0:
        return 0.0  # KL divergence is infinite
    kl = q * np.log(q / p) + (1.0 - q) * np.log((1.0 - q) / (1.0 - p))
    if np.isinf(kl) or np.isnan(kl) or kl <= 0.0:
        return 1.0
    return float(np.exp(-n * kl))


# ======================================================================
# StateValue class
# ======================================================================


class StateValue:
    """State data value V(s) and theorem-based noise detection analysis.

    .. deprecated::
        The :meth:`acquisition_value` and :meth:`compression_value` methods
        are deprecated in favor of the theorem-based methods introduced in
        v0.6.  See the following replacements:

        * :meth:`noise_detection_f1_bound` — Theorem 1 F1 lower bound
          (Hoeffding form)
        * :meth:`noise_detection_f1_bound_chernoff` — Theorem 1 F1 lower
          bound (tighter Chernoff / KL form)
        * :meth:`noise_consistency_score` — Theorem 1 C(x) multi-expert
          consistency score
        * :meth:`optimal_noise_threshold` — Theorem 1, Corollary 2 optimal
          threshold theta*
        * :meth:`separation_gap` — Theorem 1 separation gap Delta_s
        * :meth:`feature_strength_diagnostic` — Theorem 2 weak-feature
          diagnostic (I(phi; S) estimation)

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
    # Acquisition value  (DEPRECATED)
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

        .. deprecated::
            Use :meth:`noise_detection_f1_bound` or
            :meth:`feature_strength_diagnostic` instead.

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
        warnings.warn(
            "StateValue.acquisition_value() is deprecated; use "
            "noise_detection_f1_bound(), noise_consistency_score(), "
            "optimal_noise_threshold(), or feature_strength_diagnostic() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return (
            max(0.0, mean_residual)
            * max(0.0, proportion)
            * max(0.0, learnability)
            * max(0.0, 1.0 - redundancy)
            * max(0.0, best_scx)
        )

    # ------------------------------------------------------------------
    # Compression value  (DEPRECATED)
    # ------------------------------------------------------------------

    def compression_value(
        self,
        mean_residual: float,
        proportion: float,
        similarity: float,
        boundary: float,
    ) -> float:
        """Compression value V_remove(s).

        .. deprecated::
            Use :meth:`noise_detection_f1_bound` or
            :meth:`feature_strength_diagnostic` instead.

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
        warnings.warn(
            "StateValue.compression_value() is deprecated; use "
            "noise_detection_f1_bound(), noise_consistency_score(), "
            "optimal_noise_threshold(), or feature_strength_diagnostic() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return (
            max(0.0, proportion)
            * max(0.0, 1.0 - mean_residual)
            * max(0.0, similarity)
            * max(0.0, 1.0 - boundary)
        )

    # ------------------------------------------------------------------
    # Batch compute  (kept for backward compatibility)
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
    # Ranking  (kept for backward compatibility)
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

    # ------------------------------------------------------------------
    # Theorem 1 — Noise detection via multi-expert consistency
    # ------------------------------------------------------------------

    def noise_consistency_score(self, expert_errors: np.ndarray) -> float:
        r"""Consistency score C(x) = fraction of experts that fail on a sample.

        From Theorem 1:

        .. math::

            C(x) = \\frac{1}{M} \\sum_{m=1}^M e_m(x, y)

        where :math:`e_m(x, y) = \\mathbf{1}\\{\\ell(f_m(x), y) > \\tau\\}`.

        Parameters
        ----------
        expert_errors : np.ndarray, shape (M,)
            Binary indicator per expert: 1 if the expert failed on the sample,
            0 otherwise.

        Returns
        -------
        float
            Consistency score C(x) in [0, 1].
        """
        if expert_errors.size == 0:
            return 0.0
        return float(np.mean(expert_errors.astype(float)))

    def optimal_noise_threshold(self, mu_max: float, K: int) -> float:
        r"""Optimal noise detection threshold (Theorem 1, Corollary 2).

        .. math::

            \\theta^* = \\frac{1}{2}\\left(
                1 + \\mu_{\\max} \\cdot \\frac{K - 2}{K - 1}
            \\right)

        This threshold maximises the separation gap :math:`\\Delta_s`
        between clean and noisy samples.

        Parameters
        ----------
        mu_max : float
            Worst-state bound on expected consistency for clean samples,
            :math:`\\mu_{\\max} = \\max_s \\mu_s`.
        K : int
            Number of classes (must be >= 2).

        Returns
        -------
        float
            Optimal threshold :math:`\\theta^*` in (0, 1).

        Raises
        ------
        ValueError
            If *K* < 2.
        """
        if K < 2:
            raise ValueError(
                f"Number of classes K must be >= 2, got {K}"
            )
        # Clamp mu_max to avoid degenerate thresholds
        mu_max = max(0.0, min(1.0, mu_max))
        return 0.5 * (1.0 + mu_max * (K - 2) / (K - 1))

    @staticmethod
    def separation_gap(
        mu_s: float,
        K: int,
        theta: Optional[float] = None,
    ) -> float:
        r"""Separation gap :math:`\\Delta_s` for a given state (Theorem 1).

        .. math::

            \\Delta_s = \\min\\bigl(
                \\theta - \\mu_s,\\;
                1 - \\frac{\\mu_s}{K - 1} - \\theta
            \\bigr)

        When *theta* is ``None``, the optimal threshold
        :math:`\\theta_s^* = \\frac{1}{2}(1 + \\mu_s \\cdot \\frac{K-2}{K-1})`
        is used, giving the maximal gap:

        .. math::

            \\Delta_s^* = \\frac{1}{2}\\left(
                1 - \\mu_s \\cdot \\frac{K}{K - 1}
            \\right)

        Parameters
        ----------
        mu_s : float
            State-level expected consistency for clean samples.
        K : int
            Number of classes.
        theta : float, optional
            Detection threshold. If ``None``, the optimal threshold is used.

        Returns
        -------
        float
            Separation gap :math:`\\Delta_s`. Returns 0 if no positive gap
            exists.
        """
        if K < 2:
            return 0.0
        mu_s = max(0.0, min(1.0, mu_s))
        if theta is None:
            # Use optimal theta for this state
            theta = 0.5 * (1.0 + mu_s * (K - 2) / (K - 1))
        gap = min(theta - mu_s, 1.0 - mu_s / (K - 1) - theta)
        return max(0.0, gap)

    def noise_detection_f1_bound(
        self,
        M: int,
        Delta_s: np.ndarray,
        rho_s: np.ndarray,
        eta: float,
    ) -> float:
        r"""F1 lower bound from Theorem 1 (Hoeffding form).

        .. math::

            \\text{F1} \\geq 1 -
                \\frac{1}{\\eta} \\sum_{s \\in \\mathcal{S}}
                \\rho_s \\cdot \\exp(-2 M \\Delta_s^2)

        where:
        - *M* = number of experts
        - :math:`\\Delta_s` = separation gap for state *s*
        - :math:`\\rho_s` = probability mass of state *s*
        - :math:`\\eta` = global noise rate

        Parameters
        ----------
        M : int
            Number of experts.
        Delta_s : np.ndarray, shape (K,)
            Separation gap :math:`\\Delta_s` per state.
        rho_s : np.ndarray, shape (K,)
            State probabilities :math:`\\rho_s` (should sum to 1).
        eta : float
            Global noise rate :math:`\\eta` in (0, 0.5).

        Returns
        -------
        float
            Lower bound on F1 score (clipped to [0, 1]).
        """
        if M <= 0 or eta <= 0:
            return 0.0
        Delta_s = np.asarray(Delta_s, dtype=float)
        rho_s = np.asarray(rho_s, dtype=float)
        # Handle empty or zero-probability cases
        if Delta_s.size == 0 or rho_s.size == 0:
            return 0.0
        # Normalise rho_s if it doesn't sum to 1 (tolerance)
        rho_sum = rho_s.sum()
        if rho_sum > 0:
            rho_s = rho_s / rho_sum
        # Hoeffding term per state
        hoeff_terms = rho_s * np.exp(-2.0 * M * Delta_s**2)
        bound = 1.0 - (1.0 / eta) * hoeff_terms.sum()
        return float(np.clip(bound, 0.0, 1.0))

    def noise_detection_f1_bound_chernoff(
        self,
        M: int,
        mu_s: np.ndarray,
        K: int,
        rho_s: np.ndarray,
        eta: float,
    ) -> float:
        r"""F1 lower bound from Theorem 1 (Chernoff/KL form, tighter).

        Uses the Chernoff bound instead of Hoeffding for a tighter
        exponential rate:

        .. math::

            \\text{F1} \\geq 1 - \\frac{1}{\\eta} \\sum_s \\rho_s \\cdot
            \\Bigl[
                \\exp(-M \\cdot \\mathrm{KL}(\\theta \\,\\|\\, \\mu_s))
                + \\frac{1-\\eta}{\\eta}
                  \\exp(-M \\cdot \\mathrm{KL}(\\tilde{\\theta} \\,\\|\\, 1 - \\frac{\\mu_s}{K-1}))
            \\Bigr]

        where :math:`\\tilde{\\theta} = 1 - \\theta`.

        Parameters
        ----------
        M : int
            Number of experts.
        mu_s : np.ndarray, shape (K,)
            State-level expected consistency :math:`\\mu_s` for clean samples.
        K : int
            Number of classes.
        rho_s : np.ndarray, shape (K,)
            State probabilities (should sum to 1).
        eta : float
            Global noise rate in (0, 0.5).

        Returns
        -------
        float
            Lower bound on F1 score (clipped to [0, 1]).
        """
        if M <= 0 or eta <= 0 or K < 2:
            return 0.0
        mu_s = np.asarray(mu_s, dtype=float)
        rho_s = np.asarray(rho_s, dtype=float)
        if mu_s.size == 0 or rho_s.size == 0:
            return 0.0
        # Normalise rho_s
        rho_sum = rho_s.sum()
        if rho_sum > 0:
            rho_s = rho_s / rho_sum

        total = 0.0
        for mu_val, rho_val in zip(mu_s, rho_s):
            if rho_val <= 0:
                continue
            # Use optimal theta for this state
            theta = self.optimal_noise_threshold(mu_val, K)
            # Ensure theta is valid
            if theta <= mu_val or theta >= 1.0 - mu_val / (K - 1):
                continue
            kl_clean = _safe_kl(theta, mu_val)
            kl_noise = _safe_kl(1.0 - theta, 1.0 - mu_val / (K - 1))
            term = np.exp(-M * kl_clean) + ((1.0 - eta) / eta) * np.exp(-M * kl_noise)
            total += rho_val * term

        bound = 1.0 - (1.0 / eta) * total
        return float(np.clip(bound, 0.0, 1.0))

    # ------------------------------------------------------------------
    # Theorem 2 — Weak feature failure diagnostic
    # ------------------------------------------------------------------

    def feature_strength_diagnostic(
        self,
        phi_features: np.ndarray,
        state_labels: np.ndarray,
    ) -> dict:
        r"""Estimate feature strength relative to state structure.

        Computes:
        - :math:`\\delta = I(\\phi(X); S)` — mutual information between
          features and state labels
        - :math:`\\varepsilon_\\phi = \\delta / \\log K` — normalised weak
          feature strength (lower is weaker)

        Returns a diagnostic dict with interpretation of whether features
        are strong enough for reliable SCX noise detection.

        Parameters
        ----------
        phi_features : np.ndarray, shape (n_samples, n_features)
            Feature representation :math:`\\phi(X)`.
        state_labels : np.ndarray, shape (n_samples,)
            State assignment per sample.

        Returns
        -------
        dict
            Keys:

            ``delta``
                Mutual information :math:`\\delta = I(\\phi; S)` (in nats).
            ``epsilon_phi``
                Normalised weakness :math:`\\varepsilon_\\phi = \\delta / \\log K`
                (0 = maximally informative, 1 = completely uninformative).
            ``K``
                Number of detected states.
            ``recommendation``
                String: ``'strong'``, ``'moderate'``, or ``'weak'``.
        """
        phi_features = np.asarray(phi_features)
        state_labels = np.asarray(state_labels)

        if phi_features.ndim == 1:
            phi_features = phi_features.reshape(-1, 1)
        if phi_features.shape[0] == 0 or state_labels.size == 0:
            return {
                "delta": 0.0,
                "epsilon_phi": 1.0,
                "K": 0,
                "recommendation": "weak",
            }

        K = int(np.max(state_labels) + 1) if state_labels.size > 0 else 0
        if K < 2:
            return {
                "delta": 0.0,
                "epsilon_phi": 1.0,
                "K": 1,
                "recommendation": "weak",
            }

        # Estimate mutual information using sklearn's mutual_info_classif
        # (or fall back to a discrete approximation if sklearn unavailable).
        delta = self._estimate_mutual_info(phi_features, state_labels, K)

        # Normalised weakness ε_φ = δ / log K
        log_k = np.log(K)
        epsilon_phi = 1.0 - (delta / log_k) if log_k > 0 else 1.0
        epsilon_phi = float(np.clip(epsilon_phi, 0.0, 1.0))

        # Heuristic recommendation based on ε_φ
        if epsilon_phi < 0.33:
            recommendation = "strong"
        elif epsilon_phi < 0.66:
            recommendation = "moderate"
        else:
            recommendation = "weak"

        return {
            "delta": float(delta),
            "epsilon_phi": epsilon_phi,
            "K": K,
            "recommendation": recommendation,
        }

    @staticmethod
    def _estimate_mutual_info(
        X: np.ndarray,
        y: np.ndarray,
        K: int,
    ) -> float:
        """Estimate I(X; y) using sklearn or a histogram fallback."""
        try:
            from sklearn.feature_selection import mutual_info_classif

            mi = mutual_info_classif(
                X, y, discrete_features="auto", random_state=42
            )
            return float(np.mean(mi))
        except ImportError:
            # Fallback: discretise each feature into K bins and compute
            # plug-in mutual information.
            return StateValue._histogram_mutual_info(X, y, K)

    @staticmethod
    def _histogram_mutual_info(
        X: np.ndarray,
        y: np.ndarray,
        K: int,
    ) -> float:
        """Plug-in mutual information via discretisation."""
        n = X.shape[0]
        if n == 0:
            return 0.0

        # Discretise each feature into K bins
        X_disc = np.zeros((n, X.shape[1]), dtype=int)
        for j in range(X.shape[1]):
            col = X[:, j]
            if np.all(col == col[0]):  # constant feature
                X_disc[:, j] = 0
            else:
                bins = np.percentile(col, np.linspace(0, 100, K + 1)[1:-1])
                X_disc[:, j] = np.digitize(col, bins)

        # Map joint bin assignments to a single integer ID per sample
        # Use a hash-based approach: combine columns
        multipliers = K ** np.arange(X.shape[1], dtype=np.int64)
        joint_ids = X_disc @ multipliers  # unique ID per bin combination
        unique_joint = np.unique(joint_ids)
        n_bins_joint = len(unique_joint)

        # P(state, joint_bin)
        p_s = np.bincount(y.astype(int), minlength=K) / n

        mi = 0.0
        for jid in unique_joint:
            mask = joint_ids == jid
            p_xy = mask.sum() / n
            if p_xy <= 0:
                continue
            # Distribution over states within this joint bin
            y_bin = y[mask]
            for s in range(K):
                p_s_given_x = (y_bin == s).sum() / mask.sum()
                if p_s_given_x > 0 and p_s[s] > 0:
                    mi += p_xy * p_s_given_x * np.log(p_s_given_x / p_s[s])
        return float(mi)


# ======================================================================
# Internal helpers
# ======================================================================


def _safe_kl(p: float, q: float) -> float:
    """Compute KL(p || q) with safe handling of edge cases.

    Returns 0 if p and q are effectively equal, inf if q is 0 or 1
    while p is not.
    """
    eps = 1e-15
    p = np.clip(p, eps, 1.0 - eps)
    q = np.clip(q, eps, 1.0 - eps)
    if abs(p - q) < eps:
        return 0.0
    return float(p * np.log(p / q) + (1.0 - p) * np.log((1.0 - p) / (1.0 - q)))
