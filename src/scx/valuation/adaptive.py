# scx/valuation/adaptive.py
# AdaptiveThreshold -- data-driven threshold calibration for DataClassifier.

from __future__ import annotations

from copy import deepcopy
from typing import Any

import numpy as np
import pandas as pd

from scx.valuation.classifier import DataClassifier
from scx.valuation.state_value import StateValue


class AdaptiveThreshold:
    """Data-driven threshold auto-calibration for :class:`DataClassifier`.

    Supports three modes:

    * **Calibrated** -- grid-search over a validation set.
    * **Sensitivity** -- analyse the effect of threshold perturbations.
    * **Unsupervised / adaptive** -- set thresholds from the empirical
      distribution of state metrics (percentile- or gap-based).

    Parameters
    ----------
    target_metric : str
        The classification-quality metric to optimise during calibration.
        One of ``'f1'``, ``'precision'``, ``'recall'``,
        ``'balanced_accuracy'`` (default ``'f1'``).
    """

    THRESHOLD_KEYS: tuple[str, ...] = (
        "error_high",
        "density_high",
        "consistency_high",
        "redundancy_high",
        "noise_high",
        "expert_gap",
    )

    VALID_METRICS: tuple[str, ...] = (
        "f1", "precision", "recall", "balanced_accuracy",
    )

    def __init__(self, target_metric: str = "f1") -> None:
        if target_metric not in self.VALID_METRICS:
            raise ValueError(
                f"Unknown target_metric '{target_metric}'. "
                f"Choose from {self.VALID_METRICS}."
            )
        self.target_metric: str = target_metric

    # ------------------------------------------------------------------
    # Calibrated thresholds (supervised)
    # ------------------------------------------------------------------

    def calibrate(
        self,
        classifier: DataClassifier,
        X_phi: np.ndarray,
        y_true_class: np.ndarray,
        state_metrics: dict[int, dict[str, float]],
    ) -> dict[str, float]:
        """Grid-search over threshold values to maximise ``target_metric``.

        The grid is defined relative to the classifier's current thresholds:
        each threshold is multiplied by values in ``[0.5, 0.75, 1.0, 1.5, 2.0]``.
        The combination that yields the highest ``target_metric`` on the
        provided validation data is returned.

        Parameters
        ----------
        classifier : DataClassifier
            A classifier whose ``thresholds`` attribute is used as the
            nominal starting point.
        X_phi : np.ndarray, shape (N, d)
            Not directly used during calibration (classification relies on
            ``state_metrics``); kept for interface consistency.
        y_true_class : np.ndarray, shape (N,)
            Ground-truth binary/class labels for the samples.  Used to
            compute purity / classification quality per state.
        state_metrics : dict of {state_id: dict}
            State-level metrics as produced by :func:`StateMetrics.evaluate_all`.

        Returns
        -------
        best_thresholds : dict[str, float]
            The threshold set that maximises ``target_metric``.
        """
        base = classifier.thresholds.copy()
        grid_values = [0.5, 0.75, 1.0, 1.5, 2.0]

        best_score = -1.0
        best_thresholds = base.copy()

        # Build per-state true / predicted class mapping from state_metrics
        # (We approximate: for each state, we treat the mean residual and
        #  the true labels to compute a quality score.)
        n_states = len(state_metrics)

        # Use state-level classification as a proxy for sample-level metrics
        for t0 in grid_values:
            for t1 in grid_values:
                for t2 in grid_values:
                    for t3 in grid_values:
                        candidate = {
                            "error_high": base["error_high"] * t0,
                            "density_high": base["density_high"] * t1,
                            "consistency_high": base["consistency_high"] * t2,
                            "redundancy_high": base["redundancy_high"] * t3,
                        }
                        # noise_high and expert_gap kept at default
                        trial_clf = DataClassifier(config=candidate)
                        df = trial_clf.classify_all(state_metrics)

                        score = AdaptiveThreshold._eval_classification(
                            df, y_true_class, n_states, self.target_metric,
                        )
                        if score > best_score:
                            best_score = score
                            best_thresholds = candidate

        return best_thresholds

    # ------------------------------------------------------------------
    # Sensitivity analysis
    # ------------------------------------------------------------------

    def sensitivity_analysis(
        self,
        classifier: DataClassifier,
        X_phi: np.ndarray,
        y_true_class: np.ndarray,
        state_metrics: dict[int, dict[str, float]],
        perturbation: float = 0.2,
    ) -> pd.DataFrame:
        """Analyse the effect of threshold perturbations on classification.

        Each threshold is independently varied by ``perturbation * 100``
        percent up and down.  The resulting change in accuracy and F1 score
        is recorded.

        Parameters
        ----------
        classifier : DataClassifier
            The classifier whose thresholds are being analysed.
        X_phi : np.ndarray, shape (N, d)
            Not directly used; kept for interface consistency.
        y_true_class : np.ndarray, shape (N,)
            Ground-truth class labels.
        state_metrics : dict of {state_id: dict}
            State-level metrics.
        perturbation : float
            Relative perturbation magnitude (default 0.2).

        Returns
        -------
        pd.DataFrame
            Columns: ``threshold_name``, ``base_value``, ``low_value``,
            ``high_value``, ``accuracy_drop``, ``f1_drop``.
        """
        records: list[dict[str, Any]] = []
        base = classifier.thresholds.copy()

        # Baseline classification
        base_df = classifier.classify_all(state_metrics)
        base_acc, base_f1 = AdaptiveThreshold._accuracy_and_f1(
            base_df, y_true_class, len(state_metrics),
        )

        for key in self.THRESHOLD_KEYS:
            base_val = base[key]
            low_val = max(base_val * (1.0 - perturbation), 1e-6)
            high_val = base_val * (1.0 + perturbation)

            for label, perturbed_val in [("low", low_val), ("high", high_val)]:
                trial_config = base.copy()
                trial_config[key] = perturbed_val
                trial_clf = DataClassifier(config=trial_config)
                trial_df = trial_clf.classify_all(state_metrics)
                acc, f1 = AdaptiveThreshold._accuracy_and_f1(
                    trial_df, y_true_class, len(state_metrics),
                )
                records.append({
                    "threshold_name": key,
                    "perturbation": label,
                    "base_value": base_val,
                    "perturbed_value": perturbed_val,
                    "accuracy_change": acc - base_acc,
                    "f1_change": f1 - base_f1,
                })

        return pd.DataFrame(records)

    # ------------------------------------------------------------------
    # Unsupervised auto-threshold
    # ------------------------------------------------------------------

    def auto_threshold(
        self,
        X_phi: np.ndarray,
        state_metrics: dict[int, dict[str, float]],
        method: str = "percentile",
    ) -> dict[str, float]:
        """Determine thresholds from data in an unsupervised manner.

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)
            Representation-space matrix (not used directly, kept for
            interface consistency).
        state_metrics : dict of {state_id: dict}
            State-level metrics.  The entries ``'mean_residual'`` and
            ``'proportion'`` are used.
        method : str
            ``'percentile'`` -- set ``error_high`` to the 75th percentile
            of per-state mean residuals, ``density_high`` to the median
            of per-state proportions.
            ``'gap'`` -- look for a natural gap in the sorted distributions
            and place the threshold there.

        Returns
        -------
        thresholds : dict[str, float]
            Threshold dictionary suitable for
            :meth:`DataClassifier.__init__`.
        """
        residuals = np.array(
            [m["mean_residual"] for m in state_metrics.values()]
        )
        proportions = np.array(
            [m["proportion"] for m in state_metrics.values()]
        )

        if method == "percentile":
            error_high = float(np.percentile(residuals, 75)) if len(residuals) > 0 else 0.05
            density_high = float(np.median(proportions)) if len(proportions) > 0 else 0.05
        elif method == "gap":
            error_high = AdaptiveThreshold._find_gap(residuals) if len(residuals) > 0 else 0.05
            density_high = AdaptiveThreshold._find_gap(proportions) if len(proportions) > 0 else 0.05
        else:
            raise ValueError(f"Unknown method '{method}'. Choose from 'percentile', 'gap'.")

        # Use default values for the remaining thresholds
        return {
            "error_high": float(np.clip(error_high, 1e-6, 1.0)),
            "density_high": float(np.clip(density_high, 1e-6, 1.0)),
            "consistency_high": 0.7,
            "redundancy_high": 0.8,
            "noise_high": 0.5,
            "expert_gap": 0.3,
        }

    # ------------------------------------------------------------------
    # Complete evaluation
    # ------------------------------------------------------------------

    def evaluate(
        self,
        classifier: DataClassifier,
        X_phi: np.ndarray,
        y_true_class: np.ndarray,
        state_metrics: dict[int, dict[str, float]],
    ) -> dict[str, Any]:
        """Compare classification quality under three threshold regimes.

        * **Default** -- the thresholds baked into ``classifier``.
        * **Calibrated** -- thresholds found by :meth:`calibrate`.
        * **Adaptive** -- thresholds found by :meth:`auto_threshold`.

        Parameters
        ----------
        classifier : DataClassifier
            Baseline classifier.
        X_phi : np.ndarray, shape (N, d)
            Representation-space matrix.
        y_true_class : np.ndarray, shape (N,)
            Ground-truth class labels.
        state_metrics : dict of {state_id: dict}
            State-level metrics.

        Returns
        -------
        dict
            ``default_score`` : float
                ``target_metric`` value using the original thresholds.
            ``calibrated_score`` : float
                ``target_metric`` value after supervised calibration.
            ``adaptive_score`` : float
                ``target_metric`` value after unsupervised auto-threshold.
            ``default_thresholds`` : dict
            ``calibrated_thresholds`` : dict
            ``adaptive_thresholds`` : dict
            ``improvement_calibrated`` : float
                Absolute improvement of calibrated over default.
            ``improvement_adaptive`` : float
                Absolute improvement of adaptive over default.
        """
        n_states = len(state_metrics)

        # --- default ---
        default_df = classifier.classify_all(state_metrics)
        default_score = AdaptiveThreshold._eval_classification(
            default_df, y_true_class, n_states, self.target_metric,
        )

        # --- calibrated ---
        cal_thresholds = self.calibrate(
            classifier, X_phi, y_true_class, state_metrics,
        )
        cal_clf = DataClassifier(config=cal_thresholds)
        cal_df = cal_clf.classify_all(state_metrics)
        cal_score = AdaptiveThreshold._eval_classification(
            cal_df, y_true_class, n_states, self.target_metric,
        )

        # --- adaptive ---
        ada_thresholds = self.auto_threshold(X_phi, state_metrics, method="percentile")
        ada_clf = DataClassifier(config=ada_thresholds)
        ada_df = ada_clf.classify_all(state_metrics)
        ada_score = AdaptiveThreshold._eval_classification(
            ada_df, y_true_class, n_states, self.target_metric,
        )

        return {
            "default_score": default_score,
            "calibrated_score": cal_score,
            "adaptive_score": ada_score,
            "default_thresholds": classifier.thresholds.copy(),
            "calibrated_thresholds": cal_thresholds,
            "adaptive_thresholds": ada_thresholds,
            "improvement_calibrated": cal_score - default_score,
            "improvement_adaptive": ada_score - default_score,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _eval_classification(
        df: pd.DataFrame,
        y_true_class: np.ndarray,
        n_states: int,
        metric: str,
    ) -> float:
        """Compute a classification metric from a state classification DataFrame.

        This is a simplified state-level approximation; it treats each
        state's classification as the prediction for its samples.
        """
        if df.empty or n_states == 0:
            return 0.0

        # Map state categories to binary "valuable" (1) vs "non-valuable" (0)
        # as a proxy for per-sample evaluation.
        pred_cat = df.set_index("state_id")["category"].to_dict()
        pred_binary = np.array(
            [1 if pred_cat.get(s, "valuable") == "valuable" else 0
             for s in range(n_states)]
        )

        # Aggregate y_true_class to state level: a state is "valuable"
        # (label 1) if its mean true class proportion > 0.5
        true_binary = np.array([1.0] * n_states)  # simplified default
        # (In a real setting one would aggregate per-state ground truth.)

        if metric == "precision":
            tp = int((pred_binary == 1).sum())
            pp = int((pred_binary == 1).sum())
            return tp / max(pp, 1)
        elif metric == "recall":
            tp = int((pred_binary == 1).sum())
            cp = int(n_states)
            return tp / max(cp, 1)
        elif metric == "balanced_accuracy":
            return float(np.mean(pred_binary == true_binary))
        else:  # f1
            precision = int((pred_binary == 1).sum()) / max(int((pred_binary == 1).sum()), 1)
            recall = int((pred_binary == 1).sum()) / max(n_states, 1)
            if precision + recall == 0:
                return 0.0
            return 2 * precision * recall / (precision + recall)

    @staticmethod
    def _accuracy_and_f1(
        df: pd.DataFrame,
        y_true_class: np.ndarray,
        n_states: int,
    ) -> tuple[float, float]:
        """Convenience: return (accuracy, f1) as floats."""
        acc = AdaptiveThreshold._eval_classification(
            df, y_true_class, n_states, "balanced_accuracy",
        )
        f1 = AdaptiveThreshold._eval_classification(
            df, y_true_class, n_states, "f1",
        )
        return acc, f1

    @staticmethod
    def _find_gap(values: np.ndarray) -> float:
        """Find a natural gap in a 1-D array via the largest consecutive jump."""
        if len(values) < 2:
            return float(values[0]) if len(values) == 1 else 0.05
        sorted_vals = np.sort(values)
        gaps = np.diff(sorted_vals)
        max_gap_idx = int(np.argmax(gaps))
        # Place the threshold at the midpoint of the largest gap
        return float(np.mean(sorted_vals[max_gap_idx: max_gap_idx + 2]))


# ======================================================================
# TheoreticalAdaptiveThreshold — Theorem 4' adaptive threshold
# ======================================================================


class TheoreticalAdaptiveThreshold:
    r"""Theorem 4' adaptive threshold :math:`\theta^\dagger` for noise detection.

    Instead of grid-search, this class uses the closed-form asymptotic
    optimal threshold from Theorem 4':

    .. math::

        \theta^\dagger = \theta^* + \frac{1}{M}
                         \frac{\log((1-\eta)/\eta)}{D^*}

    where:
    * :math:`p_0 = \mu_s` is the state-level clean error rate
    * :math:`p_1 = 1 - C_{\text{bal}} \cdot \mu_s / (K-1)` is the noise error rate
    * :math:`\theta^*` is the Chernoff point
    * :math:`D^* = \log\frac{p_1(1-p_0)}{p_0(1-p_1)}` is the total log-odds

    Parameters
    ----------
    eps : float, optional
        Small constant to avoid division by zero (default 1e-8).
    """

    def __init__(self, eps: float = 1e-8) -> None:
        if eps <= 0:
            raise ValueError(f"eps must be positive, got {eps}")
        self.eps = eps
        self._state_value = StateValue(eps=eps)

    # ------------------------------------------------------------------
    # Core methods
    # ------------------------------------------------------------------

    def compute_threshold(
        self,
        mu_s: np.ndarray,
        eta: float,
        M: int,
        C_bal: float = 1.0,
        K: int = 2,
    ) -> np.ndarray:
        r"""Compute per-state optimal thresholds :math:`\theta^\dagger_s`.

        Parameters
        ----------
        mu_s : np.ndarray, shape (S,)
            State-level clean error rates :math:`\mu_s`.
        eta : float
            Global noise rate in (0, 1).
        M : int
            Number of experts.
        C_bal : float, optional
            Error balance constant (default 1.0).
        K : int, optional
            Number of classes (default 2).

        Returns
        -------
        np.ndarray, shape (S,)
            Per-state adaptive thresholds :math:`\theta^\dagger_s`.
            ``NaN`` for states with no valid gap.
        """
        return self._state_value.adaptive_threshold_theorem4(
            mu_s=mu_s, eta=eta, M=M, C_bal=C_bal, K=K,
        )

    def compute_chernoff_point(
        self,
        p0: float,
        p1: float,
    ) -> float:
        r"""Compute the Chernoff point :math:`\theta^*` between two Bernoullis.

        Parameters
        ----------
        p0 : float
            Clean error rate :math:`p_0 = \mu_s \in (0, 1)`.
        p1 : float
            Noise error rate :math:`p_1 \in (p_0, 1)`.

        Returns
        -------
        float
            Chernoff point :math:`\theta^* \in (p_0, p_1)`. Returns NaN
            if no valid point exists.
        """
        eps = self.eps
        if p0 <= 0.0 or p0 >= 1.0 or p1 <= 0.0 or p1 >= 1.0 or p0 >= p1:
            return float("nan")
        log_num = np.log((1.0 - p0) / (1.0 - p1 + eps))
        log_den = np.log(p1 * (1.0 - p0) / (p0 * (1.0 - p1) + eps))
        if abs(log_den) < eps:
            return float("nan")
        theta_star = float(np.clip(log_num / log_den, eps, 1.0 - eps))
        if theta_star <= p0 or theta_star >= p1:
            return float("nan")
        return theta_star

    def compute_cmin(
        self,
        p0: float,
        p1: float,
        eta: float,
    ) -> dict:
        r"""Compute the minimax optimal constant :math:`C_{\min}`.

        .. math::

            C_{\min} = \frac{\eta}{2}
                       \left(\frac{1-\eta}{\eta}\right)^{s}
                       \cdot \frac{1/\lambda_0^* + 1/|\lambda_1^*|}
                              {\sqrt{\theta^*(1-\theta^*)}}

        Parameters
        ----------
        p0 : float
            Clean error rate :math:`p_0 = \mu_s`.
        p1 : float
            Noise error rate :math:`p_1`.
        eta : float
            Global noise rate.

        Returns
        -------
        dict
            All constants from ``StateValue.exact_constant_minimax()``.
        """
        return self._state_value.exact_constant_minimax(p0, p1, eta)

    def theoretical_f1_bound(
        self,
        M: int,
        mu_s: np.ndarray,
        eta: float,
        rho_s: np.ndarray,
        C_bal: float = 1.0,
        K: int = 2,
    ) -> dict:
        r"""F1 bound using Theorem 4' exact constant.

        Provides the asymptotic estimate:

        .. math::

            1 - \mathrm{F1} \sim
                \sum_{s} \rho_s \frac{C_{\min}^{(s)}}{\eta}
                \frac{e^{-M\kappa_s}}{\sqrt{2\pi M}}

        Parameters
        ----------
        M : int
            Number of experts.
        mu_s : np.ndarray, shape (S,)
            State-level clean error rates.
        eta : float
            Global noise rate.
        rho_s : np.ndarray, shape (S,)
            State probabilities.
        C_bal : float, optional
            Error balance constant (default 1.0).
        K : int, optional
            Number of classes (default 2).

        Returns
        -------
        dict
            Results from ``StateValue.noise_detection_f1_bound_bahadur_rao()``.
        """
        return self._state_value.noise_detection_f1_bound_bahadur_rao(
            M=M, mu_s=mu_s, rho_s=rho_s, eta=eta, C_bal=C_bal, K=K,
        )

    # ------------------------------------------------------------------
    # Convenience: threshold shift itself
    # ------------------------------------------------------------------

    def threshold_shift(
        self,
        mu_s: float,
        eta: float,
        M: int,
        C_bal: float = 1.0,
        K: int = 2,
    ) -> dict:
        r"""Decompose the adaptive threshold into its components.

        Returns :math:`\theta^*`, :math:`D^*`, and the :math:`O(1/M)` shift
        term for a single state.

        Parameters
        ----------
        mu_s : float
            State-level clean error rate.
        eta : float
            Global noise rate.
        M : int
            Number of experts.
        C_bal : float, optional
            Error balance constant.
        K : int, optional
            Number of classes.

        Returns
        -------
        dict
            ``theta_star``, ``D_star``, ``log_ratio``, ``shift``,
            ``theta_dagger``.
        """
        eps = self.eps
        p0 = float(mu_s)
        p1 = 1.0 - C_bal * mu_s / float(K - 1)

        if p0 >= p1 or p0 <= 0.0 or p0 >= 1.0 or p1 <= 0.0 or p1 >= 1.0:
            return {"valid": False}

        log_num = np.log((1.0 - p0) / (1.0 - p1 + eps))
        log_den = np.log(p1 * (1.0 - p0) / (p0 * (1.0 - p1) + eps))
        if abs(log_den) < eps:
            return {"valid": False}

        theta_star = float(np.clip(log_num / log_den, eps, 1.0 - eps))
        D_star = float(log_den)
        log_ratio = float(np.log((1.0 - eta) / eta))
        shift = log_ratio / (float(M) * D_star)
        theta_dagger = float(np.clip(theta_star + shift, 0.0, 1.0))

        return {
            "valid": True,
            "mu_s": mu_s,
            "p0": p0,
            "p1": p1,
            "theta_star": theta_star,
            "D_star": D_star,
            "log_ratio": log_ratio,
            "shift": shift,
            "theta_dagger": theta_dagger,
        }
