# scx/utils/evaluation.py
# Evaluation -- metrics and evaluation utilities for the SCX framework.

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score as sklearn_r2


class Evaluation:
    """Evaluation metrics for the SCX framework.

    Provides static methods for regression/classification metrics,
    acquisition efficiency, compression fidelity, expert routing
    accuracy, and benchmark comparison.
    """

    # ==================================================================
    # Regression metrics
    # ==================================================================

    @staticmethod
    def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Root mean squared error.

        Parameters
        ----------
        y_true : np.ndarray, shape (N,)
        y_pred : np.ndarray, shape (N,)

        Returns
        -------
        float
        """
        y_true = np.asarray(y_true, dtype=float)
        y_pred = np.asarray(y_pred, dtype=float)
        return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))

    @staticmethod
    def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Mean absolute error.

        Parameters
        ----------
        y_true : np.ndarray, shape (N,)
        y_pred : np.ndarray, shape (N,)

        Returns
        -------
        float
        """
        y_true = np.asarray(y_true, dtype=float)
        y_pred = np.asarray(y_pred, dtype=float)
        return float(np.mean(np.abs(y_true - y_pred)))

    @staticmethod
    def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """R-squared coefficient of determination.

        Parameters
        ----------
        y_true : np.ndarray, shape (N,)
        y_pred : np.ndarray, shape (N,)

        Returns
        -------
        float
        """
        y_true = np.asarray(y_true, dtype=float)
        y_pred = np.asarray(y_pred, dtype=float)
        return float(sklearn_r2(y_true, y_pred))

    # ==================================================================
    # Classification report
    # ==================================================================

    @staticmethod
    def classification_report_df(
        state_classes: np.ndarray,
        true_classes: np.ndarray | None = None,
    ) -> pd.DataFrame:
        """Generate a classification report DataFrame.

        If ``true_classes`` is provided, computes per-category precision,
        recall, F1.  Otherwise returns a simple category count summary.

        Parameters
        ----------
        state_classes : np.ndarray, shape (K,)
            Predicted or assigned state categories.
        true_classes : np.ndarray, shape (K,) or None
            Ground-truth categories (if available).

        Returns
        -------
        report : pd.DataFrame
        """
        from sklearn.metrics import classification_report

        if true_classes is not None:
            report_dict = classification_report(
                true_classes, state_classes, output_dict=True,
            )
            return pd.DataFrame(report_dict).transpose()

        # Simple count summary
        unique, counts = np.unique(state_classes, return_counts=True)
        df = pd.DataFrame({"category": unique, "count": counts})
        df["proportion"] = df["count"] / df["count"].sum()
        return df.sort_values("count", ascending=False).reset_index(drop=True)

    # ==================================================================
    # Acquisition efficiency
    # ==================================================================

    @staticmethod
    def acquisition_efficiency(
        selected_samples: np.ndarray,
        oracle_values: np.ndarray,
    ) -> float:
        """Compute acquisition efficiency as the ratio of achieved value
        to optimal (oracle) value.

        ``efficiency = sum(oracle_values[selected]) / sum(oracle_values)``

        Parameters
        ----------
        selected_samples : np.ndarray, shape (n_selected,)
            Indices of selected samples.
        oracle_values : np.ndarray, shape (N,)
            Per-sample oracle / ground-truth value scores.

        Returns
        -------
        efficiency : float
            In [0, 1]; higher is better.
        """
        oracle_values = np.asarray(oracle_values, dtype=float)
        selected = np.asarray(selected_samples, dtype=int)
        total_value = oracle_values.sum()
        if total_value <= 0:
            return 0.0
        achieved = oracle_values[selected].sum()
        return float(achieved / total_value)

    # ==================================================================
    # Compression fidelity
    # ==================================================================

    @staticmethod
    def compression_fidelity(
        y_orig: np.ndarray,
        y_compressed: np.ndarray,
        weights: np.ndarray | None = None,
    ) -> dict[str, float]:
        """Evaluate compression fidelity by comparing label distributions.

        Parameters
        ----------
        y_orig : np.ndarray, shape (N,)
            Original (full) labels.
        y_compressed : np.ndarray, shape (n,)
            Compressed-set labels.
        weights : np.ndarray, shape (n,) or None
            Sample weights for the compressed set.

        Returns
        -------
        fidelity : dict
            Keys: ``"mean_shift"``, ``"std_shift"``, ``"ks_statistic"``,
            ``"wasserstein_distance"``.
        """
        from scipy.stats import ks_2samp, wasserstein_distance

        y_orig = np.asarray(y_orig, dtype=float)
        y_comp = np.asarray(y_compressed, dtype=float)

        mean_shift = float(np.mean(y_comp) - np.mean(y_orig))
        std_shift = float(np.std(y_comp) - np.std(y_orig))

        # Weighted KS is complex; use unweighted as approximation
        ks_stat, _ = ks_2samp(y_orig, y_comp)

        if weights is not None:
            w = np.asarray(weights, dtype=float)
            w = w / w.sum()  # normalize
            # Weighted mean / std
            w_mean = np.average(y_comp, weights=w)
            w_var = np.average((y_comp - w_mean) ** 2, weights=w)
            w_std = np.sqrt(w_var)
            mean_shift = float(w_mean - np.mean(y_orig))
            std_shift = float(w_std - np.std(y_orig))

        w_dist = float(wasserstein_distance(y_orig, y_comp))

        return {
            "mean_shift": mean_shift,
            "std_shift": std_shift,
            "ks_statistic": float(ks_stat),
            "wasserstein_distance": w_dist,
        }

    # ==================================================================
    # Expert routing accuracy
    # ==================================================================

    @staticmethod
    def expert_routing_accuracy(
        routed_experts: np.ndarray,
        oracle_best_expert: np.ndarray,
    ) -> float:
        """Compute routing accuracy: fraction of samples routed to the
        oracle-best expert.

        Parameters
        ----------
        routed_experts : np.ndarray, shape (N,)
            Expert ID assigned by the routing policy.
        oracle_best_expert : np.ndarray, shape (N,)
            Ground-truth best expert ID for each sample.

        Returns
        -------
        accuracy : float
        """
        routed = np.asarray(routed_experts, dtype=int)
        oracle = np.asarray(oracle_best_expert, dtype=int)
        if len(routed) == 0:
            return 0.0
        return float(np.mean(routed == oracle))

    # ==================================================================
    # Benchmark comparison
    # ==================================================================

    @staticmethod
    def benchmark(
        baseline_results: dict[str, Any] | pd.DataFrame,
        scx_results: dict[str, Any] | pd.DataFrame,
    ) -> pd.DataFrame:
        """Compare SCX against baseline methods.

        Parameters
        ----------
        baseline_results : dict or pd.DataFrame
            Results from baseline methods. If dict, keys are method names
            and values are score arrays.
        scx_results : dict or pd.DataFrame
            Results from SCX method(s). Same format.

        Returns
        -------
        comparison : pd.DataFrame
            Index: method names. Columns include mean, std, and a
            "vs_best" column showing relative difference.
        """
        # Normalise to DataFrames
        if isinstance(baseline_results, dict):
            bl = pd.DataFrame({
                k: np.asarray(v, dtype=float).ravel()
                for k, v in baseline_results.items()
            })
        else:
            bl = baseline_results.copy()

        if isinstance(scx_results, dict):
            scx = pd.DataFrame({
                k: np.asarray(v, dtype=float).ravel()
                for k, v in scx_results.items()
            })
        else:
            scx = scx_results.copy()

        combined = pd.concat([bl, scx], axis=1)

        summary = pd.DataFrame({
            "mean": combined.mean(),
            "std": combined.std(),
            "min": combined.min(),
            "max": combined.max(),
        })

        best = summary["mean"].max()
        summary["vs_best"] = summary["mean"] / best if best != 0 else 0.0

        return summary.round(4)
