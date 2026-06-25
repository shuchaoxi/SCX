# scx/state/assignment.py
# StateAssignment -- hard / soft / hybrid assignment strategies.

from __future__ import annotations

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.mixture import GaussianMixture


class StateAssignment:
    """State assigner: map samples to states (hard / soft / hybrid)."""

    # ------------------------------------------------------------------
    # Hard assignment
    # ------------------------------------------------------------------

    @staticmethod
    def hard_assign(
        X_phi: np.ndarray,
        centroids: np.ndarray,
        metric: str = "euclidean",
    ) -> np.ndarray:
        """Hard assignment: each sample goes to the nearest centroid.

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)
            Representation-space samples.
        centroids : np.ndarray, shape (K, d)
            State centroids.
        metric : str
            Distance metric passed to ``scipy.spatial.distance.cdist``.

        Returns
        -------
        labels : np.ndarray, shape (N,)
            Integer label for each sample (0 .. K-1).
        """
        dists = cdist(X_phi, centroids, metric=metric)  # (N, K)
        return np.argmin(dists, axis=1).astype(int)

    # ------------------------------------------------------------------
    # Soft assignment (distance-based)
    # ------------------------------------------------------------------

    @staticmethod
    def soft_assign(
        X_phi: np.ndarray,
        centroids: np.ndarray,
        temperature: float = 1.0,
        metric: str = "euclidean",
    ) -> np.ndarray:
        """Soft assignment via distance-based softmax.

        .. math::

            p(s_k | x) = \\frac{\\exp(-d(x, c_k)^2 / T)}
                              {\\sum_j \\exp(-d(x, c_j)^2 / T)}

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)
        centroids : np.ndarray, shape (K, d)
        temperature : float
            Softmax temperature (default 1.0). Higher values produce more
            uniform assignments.
        metric : str
            Distance metric (default 'euclidean').

        Returns
        -------
        weights : np.ndarray, shape (N, K)
            Each row sums to 1.
        """
        dists = cdist(X_phi, centroids, metric=metric)  # (N, K)
        squared = dists ** 2
        logits = -squared / max(temperature, 1e-12)

        # numerical stability: subtract row-wise max
        logits -= logits.max(axis=1, keepdims=True)
        exp_logits = np.exp(logits)
        return exp_logits / exp_logits.sum(axis=1, keepdims=True)

    # ------------------------------------------------------------------
    # GMM soft assignment
    # ------------------------------------------------------------------

    @staticmethod
    def soft_assign_gmm(
        X_phi: np.ndarray,
        means: np.ndarray,
        covariances: np.ndarray,
        weights: np.ndarray,
    ) -> np.ndarray:
        """GMM posterior probability assignment.

        Constructs a ``GaussianMixture`` with the given parameters and returns
        ``predict_proba``.

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)
        means : np.ndarray, shape (K, d)
            Component means.
        covariances : np.ndarray, shape (K, d, d)
            Component covariance matrices (full).
        weights : np.ndarray, shape (K,)
            Component mixing weights (sum to 1).

        Returns
        -------
        probs : np.ndarray, shape (N, K)
            Posterior probabilities.
        """
        K = means.shape[0]
        gmm = GaussianMixture(n_components=K, covariance_type="full")
        gmm.means_ = means
        gmm.covariances_ = covariances
        gmm.weights_ = weights
        gmm.precisions_cholesky_ = np.linalg.cholesky(
            np.linalg.inv(covariances)
        )
        # valid GaussianMixture requires fitted flag
        gmm.fit(np.zeros((max(2, X_phi.shape[0]), X_phi.shape[1])))  # dummy to set internal state
        # manually set remaining internals
        gmm.means_ = means
        gmm.covariances_ = covariances
        gmm.weights_ = weights
        gmm.precisions_cholesky_ = np.linalg.cholesky(
            np.linalg.inv(covariances)
        )
        # directly compute using scipy to avoid fit gymnastics:
        from scipy.stats import multivariate_normal

        N, d = X_phi.shape
        probs = np.zeros((N, K))
        for k in range(K):
            rv = multivariate_normal(mean=means[k], cov=covariances[k])
            probs[:, k] = weights[k] * rv.pdf(X_phi)
        probs /= probs.sum(axis=1, keepdims=True)
        return probs

    # ------------------------------------------------------------------
    # Hybrid assignment
    # ------------------------------------------------------------------

    @staticmethod
    def hybrid_assign(
        X_phi: np.ndarray,
        centroids: np.ndarray,
        hard_threshold: float = 0.8,
        temperature: float = 1.0,
        metric: str = "euclidean",
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Hybrid assignment: hard for confident samples, soft for others.

        For each sample, if the maximum soft weight exceeds
        ``hard_threshold``, a hard label is assigned.  Otherwise, the full
        soft vector is kept.

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)
        centroids : np.ndarray, shape (K, d)
        hard_threshold : float
            Confidence threshold in (0, 1).  Samples whose highest soft
            weight >= threshold receive a hard label; the rest keep the
            full soft vector.
        temperature : float
            Softmax temperature (default 1.0).
        metric : str
            Distance metric (default 'euclidean').

        Returns
        -------
        hard_labels : np.ndarray, shape (N,)
            Hard labels (always returned, even for low-confidence samples
            where the argmax is used as the hard label).
        soft_weights : np.ndarray, shape (N, K)
            Full soft assignment matrix.
        confidence_mask : np.ndarray, shape (N,), bool
            True where the sample was confident enough for a hard assignment.
        """
        soft = StateAssignment.soft_assign(
            X_phi, centroids, temperature=temperature, metric=metric
        )
        max_weights = soft.max(axis=1)
        hard_labels = np.argmax(soft, axis=1).astype(int)
        confidence_mask = max_weights >= hard_threshold
        return hard_labels, soft, confidence_mask

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @staticmethod
    def state_proportions(
        assignment: np.ndarray, n_states: int
    ) -> np.ndarray:
        """Compute the sample proportion rho(s) for each state.

        Parameters
        ----------
        assignment : np.ndarray, shape (N,)
            Hard state labels (0 .. K-1).
        n_states : int
            Total number of states K.

        Returns
        -------
        proportions : np.ndarray, shape (K,)
            rho(s_k) = count_k / N
        """
        counts = np.bincount(assignment, minlength=n_states).astype(float)
        return counts / counts.sum()
