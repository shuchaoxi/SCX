# scx/state/robustness.py
# StateRobustness -- robustness analysis of state discovery results.

from __future__ import annotations

from typing import Any

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score


class StateRobustness:
    """Robustness and stability analysis for state discovery.

    Provides static methods to evaluate the sensitivity of state assignments
    to perturbations (merge, split, label noise), cross-descriptor consistency,
    bootstrap-based K selection, and boundary confidence estimation.
    """

    # ------------------------------------------------------------------
    # Misclassification impact analysis
    # ------------------------------------------------------------------

    @staticmethod
    def misclassification_impact(
        X_phi: np.ndarray,
        y_true_states: np.ndarray,
        y_pred_states: np.ndarray,
        R_matrix: np.ndarray,
        classifier: Any,  # DataClassifier (avoid circular import type)
    ) -> dict[str, Any]:
        """Analyse the impact of state misclassification on SCX classification.

        Simulates three perturbations of the state assignment:
        1. **Merge** two adjacent states (by centroid proximity) and reclassify.
        2. **Split** a single state into two and reclassify.
        3. **Noise** -- randomly swap 10 % of the assignments and reclassify.

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)
            Representation-space feature matrix.
        y_true_states : np.ndarray, shape (N,)
            Ground-truth state labels.
        y_pred_states : np.ndarray, shape (N,)
            Predicted state labels.
        R_matrix : np.ndarray, shape (M, K)
            Expert risk matrix (M experts, K states).
        classifier : DataClassifier
            A fitted :class:`~scx.valuation.classifier.DataClassifier` instance
            used to produce classification labels before and after perturbation.

        Returns
        -------
        dict
            ``merge_impact`` : float
                Fraction of states whose class label changed after merge.
            ``split_impact`` : float
                Fraction of states whose class label changed after split.
            ``noise_impact`` : float
                Fraction of states whose class label changed after noise.
            ``stable_states`` : list[int]
                State IDs that were never reclassified in any perturbation.
            ``sensitive_states`` : list[int]
                State IDs that changed class in at least one perturbation.
        """
        from scx.valuation.classifier import DataClassifier

        if not isinstance(classifier, DataClassifier):
            raise TypeError("classifier must be a DataClassifier instance.")

        K = int(y_pred_states.max()) + 1
        state_ids = list(range(K))

        # --- Build original state metrics from data ---
        def _build_state_metrics(labels: np.ndarray) -> dict[int, dict[str, float]]:
            metrics: dict[int, dict[str, float]] = {}
            # R_matrix has shape (M, K); column s corresponds to state s.
            # If labels contain states that exceed K, we use the global mean.
            global_residual = float(np.mean(R_matrix))
            for s in np.unique(labels):
                s_int = int(s)
                mask = labels == s
                n = int(mask.sum())
                resid = (
                    float(np.mean(R_matrix[:, s_int]))
                    if s_int < R_matrix.shape[1]
                    else global_residual
                )
                metrics[s_int] = {
                    "mean_residual": resid,
                    "proportion": n / len(labels),
                    "consistency": 0.8,
                    "redundancy": 0.5,
                    "noise_score": 0.1,
                }
            return metrics

        def _classify_states(labels: np.ndarray) -> set[int]:
            """Return set of state IDs per classification category."""
            metrics = _build_state_metrics(labels)
            df = classifier.classify_all(metrics, R_matrix=R_matrix)
            return set(df.loc[df["category"] != "valuable", "state_id"].tolist())

        original_non_valuable = _classify_states(y_pred_states)

        # ---- 1. Merge ----
        # Compute centroids and merge the two closest states
        centroids = np.array(
            [X_phi[y_pred_states == s].mean(axis=0) for s in state_ids]
        )
        dists = cdist(centroids, centroids, metric="euclidean")
        np.fill_diagonal(dists, np.inf)
        i_merge, j_merge = np.unravel_index(np.argmin(dists), dists.shape)

        merged_labels = y_pred_states.copy()
        # Relabel all samples of the higher state ID to the lower one
        merge_target = int(min(i_merge, j_merge))
        merge_source = int(max(i_merge, j_merge))
        merged_labels[merged_labels == merge_source] = merge_target
        # Compact labels
        unique_new = sorted(set(merged_labels))
        remap = {old: new for new, old in enumerate(unique_new)}
        merged_labels = np.array([remap[l] for l in merged_labels])

        merge_non_valuable = _classify_states(merged_labels)
        merge_impact = _fraction_changed(
            original_non_valuable, merge_non_valuable, new_K=len(unique_new)
        )

        # ---- 2. Split ----
        # Pick the largest state (most samples) and run 2-means within it.
        # The two sub-clusters get new unique state IDs beyond current K.
        state_sizes = {s: int((y_pred_states == s).sum()) for s in state_ids}
        split_candidate = max(state_sizes, key=state_sizes.get)
        split_mask = y_pred_states == split_candidate
        sub_X = X_phi[split_mask]

        # Find two unused state IDs
        next_id = K
        new_id_1, new_id_2 = next_id, next_id + 1

        if len(sub_X) >= 4:
            km = KMeans(n_clusters=2, n_init=5, random_state=42)
            sub_labels = km.fit_predict(sub_X)
        else:
            # Too few points; label both as the same new state (no split)
            sub_labels = np.zeros(len(sub_X), dtype=int)

        split_labels = y_pred_states.copy()
        # Assign sub-cluster 0 -> new_id_1, sub-cluster 1 -> new_id_2
        split_labels[split_mask] = np.where(sub_labels == 0, new_id_1, new_id_2)
        split_non_valuable = _classify_states(split_labels)
        split_impact = _fraction_changed(
            original_non_valuable, split_non_valuable,
            new_K=int(split_labels.max()) + 1,
        )

        # ---- 3. Noise ----
        rng = np.random.default_rng(42)
        n_noise = max(1, int(0.1 * len(y_pred_states)))
        noise_indices = rng.choice(len(y_pred_states), size=n_noise, replace=False)
        noise_labels = y_pred_states.copy()
        # Swap each selected sample's label to a uniformly random different state
        for idx in noise_indices:
            old = noise_labels[idx]
            candidates = [s for s in state_ids if s != old]
            noise_labels[idx] = int(rng.choice(candidates))

        noise_non_valuable = _classify_states(noise_labels)
        noise_impact = _fraction_changed(
            original_non_valuable, noise_non_valuable, new_K=K,
        )

        # ---- Stable / sensitive ----
        all_perturbed_non_valuable = (
            merge_non_valuable | split_non_valuable | noise_non_valuable
        )
        sensitive = sorted(all_perturbed_non_valuable)
        stable = sorted(set(state_ids) - all_perturbed_non_valuable)

        return {
            "merge_impact": merge_impact,
            "split_impact": split_impact,
            "noise_impact": noise_impact,
            "stable_states": stable,
            "sensitive_states": sensitive,
        }

    # ------------------------------------------------------------------
    # Cross-descriptor stability
    # ------------------------------------------------------------------

    @staticmethod
    def cross_descriptor_stability(
        X_phi1: np.ndarray,
        X_phi2: np.ndarray,
        labels1: np.ndarray,
        labels2: np.ndarray,
    ) -> float:
        """Evaluate clustering consistency across two descriptor sets.

        Uses the Adjusted Rand Index (ARI) between the two label
        assignments.  A value close to 1 indicates that both descriptor
        sets lead to similar state partitions.

        Parameters
        ----------
        X_phi1 : np.ndarray, shape (N, d1)
            Representation from descriptor set 1 (e.g. ACE).
        X_phi2 : np.ndarray, shape (N, d2)
            Representation from descriptor set 2 (e.g. SOAP).
        labels1 : np.ndarray, shape (N,)
            State labels from descriptor set 1.
        labels2 : np.ndarray, shape (N,)
            State labels from descriptor set 2.

        Returns
        -------
        ari : float
            Adjusted Rand Index in ``[-1, 1]``.
        """
        if labels1.shape != labels2.shape:
            raise ValueError(
                f"Label shape mismatch: {labels1.shape} vs {labels2.shape}."
            )
        return float(adjusted_rand_score(labels1, labels2))

    # ------------------------------------------------------------------
    # Bootstrap-based K suggestion
    # ------------------------------------------------------------------

    @staticmethod
    def suggest_robust_states(
        X_phi: np.ndarray,
        n_trials: int = 10,
        subsample_ratio: float = 0.9,
    ) -> int:
        """Suggest a robust number of states *K* via bootstrap subsampling.

        At each trial a random subset (``subsample_ratio``) of the data is
        clustered for each candidate *K*, and the Adjusted Rand Index
        between the full-data and subsample assignments is computed.
        The *K* with the highest mean ARI across trials is returned.

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)
            Representation-space feature matrix.
        n_trials : int
            Number of bootstrap replicates (default 10).
        subsample_ratio : float
            Fraction of samples to use in each trial (default 0.9).

        Returns
        -------
        best_k : int
            The most robust number of states.
        """
        rng = np.random.default_rng(42)
        N = X_phi.shape[0]
        n_subsample = max(2, int(N * subsample_ratio))
        max_candidate = min(21, int(np.sqrt(N)) + 5, N)  # cap at N for KMeans
        n_states_candidates = list(range(2, max_candidate))

        if len(n_states_candidates) == 0 or max_candidate <= 2:
            return 2

        # Full-data reference labels for each K
        full_labels: dict[int, np.ndarray] = {}
        for K in n_states_candidates:
            km = KMeans(n_clusters=K, n_init=10, random_state=42)
            full_labels[K] = km.fit_predict(X_phi)

        # Bootstrap: for each trial, subsample and compute ARI for each K
        mean_aris: list[float] = []
        for K in n_states_candidates:
            aris: list[float] = []
            for _ in range(n_trials):
                idx = rng.choice(N, size=n_subsample, replace=False)
                sub_X = X_phi[idx]
                sub_labels = KMeans(n_clusters=K, n_init=5, random_state=42).fit_predict(sub_X)
                ari = adjusted_rand_score(full_labels[K][idx], sub_labels)
                aris.append(ari)
            mean_aris.append(float(np.mean(aris)))

        best_k = n_states_candidates[int(np.argmax(mean_aris))]
        return best_k

    # ------------------------------------------------------------------
    # State boundary confidence
    # ------------------------------------------------------------------

    @staticmethod
    def state_boundary_confidence(
        X_phi: np.ndarray,
        labels: np.ndarray,
        centroids: np.ndarray,
    ) -> np.ndarray:
        """Compute per-sample state-assignment confidence.

        Confidence is defined as the **margin** between the top two
        softmax-normalised inverse distances to the centroids.  Samples
        near a boundary have a small margin and therefore low confidence.

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)
            Representation-space feature matrix.
        labels : np.ndarray, shape (N,)
            Hard state assignments (ignored for the margin computation).
        centroids : np.ndarray, shape (K, d)
            State centroids.

        Returns
        -------
        confidence : np.ndarray, shape (N,)
            Per-sample confidence values in ``[0, 1]``.  Values near 1
            indicate unambiguous assignment; values near 0 indicate
            boundary / uncertain samples.
        """
        # Inverse-distance softmax (temperature = 1.0)
        dists = cdist(X_phi, centroids, metric="euclidean")  # (N, K)
        probs = np.exp(-dists)
        probs /= probs.sum(axis=1, keepdims=True)

        # Confidence = P(top) - P(second), which lies in [0, ~1]
        sorted_probs = np.sort(probs, axis=1)
        margins = sorted_probs[:, -1] - sorted_probs[:, -2]
        # Clip to [0, 1] for safety
        confidence = np.clip(margins, 0.0, 1.0)
        return confidence


# ------------------------------------------------------------------
# Internal helper
# ------------------------------------------------------------------

def _fraction_changed(
    original: set[int],
    perturbed: set[int],
    new_K: int,
) -> float:
    """Fraction of states whose classification category changed."""
    # The set difference approximates the count of states that flipped.
    # We normalise by new_K to obtain a fraction.
    if new_K == 0:
        return 0.0
    n_flipped = len(original ^ perturbed)
    return n_flipped / new_K
