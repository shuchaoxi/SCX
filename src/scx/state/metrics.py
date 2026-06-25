# scx/state/metrics.py
# StateMetrics -- quality evaluation for discovered states.

from __future__ import annotations

import numpy as np
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score


class StateMetrics:
    """Quality metrics for state discovery."""

    # ------------------------------------------------------------------
    # Individual metrics
    # ------------------------------------------------------------------

    @staticmethod
    def silhouette(X_phi: np.ndarray, labels: np.ndarray) -> float:
        """Silhouette coefficient: measure of cluster compactness & separation.

        Ranges in [-1, 1]; higher is better.

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)
        labels : np.ndarray, shape (N,)

        Returns
        -------
        score : float
        """
        unique = np.unique(labels)
        if len(unique) < 2:
            return 0.0
        return float(silhouette_score(X_phi, labels))

    @staticmethod
    def davies_bouldin(X_phi: np.ndarray, labels: np.ndarray) -> float:
        """Davies-Bouldin index: average similarity between each cluster and
        its most similar one.  Lower is better.

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)
        labels : np.ndarray, shape (N,)

        Returns
        -------
        score : float
        """
        unique = np.unique(labels)
        if len(unique) < 2:
            return 0.0
        return float(davies_bouldin_score(X_phi, labels))

    @staticmethod
    def state_purity(
        X_phi: np.ndarray | None = None,
        labels: np.ndarray | None = None,
        true_labels: np.ndarray | None = None,
        *,
        labels_pred: np.ndarray | None = None,
        labels_true: np.ndarray | None = None,
    ) -> float:
        """Purity: fraction of correctly assigned samples given ground-truth
        labels.

        Purity = (1 / N) * sum_k max_j |s_k ∩ c_j|,
        where s_k is the k-th state (predicted cluster) and c_j is the j-th
        ground-truth class.

        Parameters
        ----------
        X_phi : np.ndarray, optional
            Ignored; kept for interface consistency.
        labels : np.ndarray, optional
            Predicted state labels (alias for ``labels_pred``).
        true_labels : np.ndarray, optional
            Ground-truth labels (alias for ``labels_true``).
        labels_pred : np.ndarray, optional
            Predicted state labels.
        labels_true : np.ndarray, optional
            Ground-truth labels.

        Returns
        -------
        purity : float
            Between 0 and 1; higher is better.
        """
        # resolve aliases (backward-compatible with both naming conventions)
        pred = labels if labels_pred is None else labels_pred
        true = true_labels if labels_true is None else labels_true

        if pred is None or true is None:
            raise ValueError(
                "Provide either (labels, true_labels) or "
                "(labels_pred, labels_true)."
            )

        pred = np.asarray(pred)
        true = np.asarray(true)
        if len(pred) != len(true):
            raise ValueError("Length mismatch between labels and true_labels.")

        n = len(pred)
        # contingency matrix: rows = predicted, cols = true
        K = max(pred.max(), true.max()) + 1
        contingency = np.zeros((K, K), dtype=float)
        for p, t in zip(pred, true):
            contingency[p, t] += 1.0

        purity = contingency.max(axis=1).sum() / n
        return float(purity)

    @staticmethod
    def state_stability(
        X_phi: np.ndarray | None = None,
        labels1: np.ndarray | None = None,
        labels2: np.ndarray | None = None,
    ) -> float:
        """Stability between two state assignments measured via Adjusted Rand
        Index (ARI).

        Parameters
        ----------
        X_phi : np.ndarray, optional
            Ignored; kept for interface consistency.
        labels1 : np.ndarray, shape (N,)
            First assignment (e.g., from different initialisation).
        labels2 : np.ndarray, shape (N,)
            Second assignment.

        Returns
        -------
        ari : float
            Adjusted Rand Index in [-1, 1]; 1 = perfectly consistent.
        """
        if labels1 is None or labels2 is None:
            raise ValueError("Both labels1 and labels2 must be provided.")
        labels1 = np.asarray(labels1)
        labels2 = np.asarray(labels2)
        return float(adjusted_rand_score(labels1, labels2))

    # ------------------------------------------------------------------
    # Automated K suggestion
    # ------------------------------------------------------------------

    @staticmethod
    def suggest_n_states(
        X_phi: np.ndarray,
        max_k: int = 20,
        method: str = "silhouette",
        random_state: int = 42,
    ) -> int:
        """Suggest the optimal number of states K by evaluating a metric over
        a range of K values.

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)
        max_k : int
            Maximum K to consider (default 20).  Minimum is 2.
        method : str
            Criterion: ``'silhouette'`` (higher = better) or
            ``'davies_bouldin'`` (lower = better).
        random_state : int
            Seed for KMeans reproducibility.

        Returns
        -------
        best_k : int
            Optimal number of states.
        """
        from sklearn.cluster import KMeans

        min_k = min(2, max_k)
        max_k = max(min_k + 1, max_k)
        scores: list[float] = []

        for k in range(min_k, max_k + 1):
            km = KMeans(n_clusters=k, n_init=10, random_state=random_state)
            labels = km.fit_predict(X_phi)

            if method == "silhouette":
                sc = silhouette_score(X_phi, labels) if len(np.unique(labels)) > 1 else -1.0
                scores.append(sc)
            elif method == "davies_bouldin":
                sc = davies_bouldin_score(X_phi, labels) if len(np.unique(labels)) > 1 else 1e9
                scores.append(-sc)  # negate so we always maximise
            else:
                raise ValueError(f"Unknown method '{method}'.")

        if method == "silhouette":
            best_idx = int(np.argmax(scores))
        else:
            best_idx = int(np.argmax(scores))  # already negated

        return int(min_k + best_idx)

    # ------------------------------------------------------------------
    # Comprehensive evaluation
    # ------------------------------------------------------------------

    @staticmethod
    def evaluate_all(
        X_phi: np.ndarray,
        labels: np.ndarray,
        true_labels: np.ndarray | None = None,
    ) -> dict[str, float]:
        """Compute all available state metrics at once.

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)
        labels : np.ndarray, shape (N,)
            Predicted state assignment.
        true_labels : np.ndarray, optional, shape (N,)
            Ground-truth labels (required for purity).

        Returns
        -------
        results : dict
            Keys: ``'silhouette'``, ``'davies_bouldin'``, ``'purity'``,
            ``'n_states'``.
        """
        results: dict[str, float] = {}

        results["silhouette"] = StateMetrics.silhouette(X_phi, labels)
        results["davies_bouldin"] = StateMetrics.davies_bouldin(X_phi, labels)
        results["n_states"] = float(len(np.unique(labels)))

        if true_labels is not None:
            results["purity"] = StateMetrics.state_purity(
                labels_pred=labels, labels_true=true_labels
            )
            results["nmi"] = float(
                normalized_mutual_info_score(true_labels, labels)
            )
            results["ari"] = float(adjusted_rand_score(true_labels, labels))

        return results
