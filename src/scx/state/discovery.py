# scx/state/discovery.py
# StateDiscovery -- automatic state discovery from phi-space via clustering.

from __future__ import annotations

from typing import Optional

import numpy as np
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics.pairwise import pairwise_distances

# ---------------------------------------------------------------------------
# Optional dependency: HDBSCAN
# ---------------------------------------------------------------------------
try:
    import hdbscan  # noqa: F401

    _HDBSCAN_AVAILABLE = True
except ImportError:
    _HDBSCAN_AVAILABLE = False


def _softmax_dist(
    X_phi: np.ndarray, centroids: np.ndarray, temperature: float = 1.0
) -> np.ndarray:
    """Compute soft assignment via distance-based softmax.

    p(s_k | x) = exp(-d(x, c_k) / T) / sum_{j} exp(-d(x, c_j) / T)

    Parameters
    ----------
    X_phi : np.ndarray, shape (N, d)
    centroids : np.ndarray, shape (K, d)
    temperature : float
        Softmax temperature (default 1.0).

    Returns
    -------
    probs : np.ndarray, shape (N, K)
    """
    dists = pairwise_distances(X_phi, centroids, metric="euclidean")  # (N, K)
    logits = -dists / max(temperature, 1e-12)
    exp_logits = np.exp(logits - logits.max(axis=1, keepdims=True))
    return exp_logits / exp_logits.sum(axis=1, keepdims=True)


class StateDiscovery:
    """Discover states from the representation space phi(X).

    Supported clustering methods:
        - 'kmeans'     : KMeans (hard, Euclidean)
        - 'gmm'        : Gaussian Mixture Model (soft)
        - 'spectral'   : Spectral clustering (hard, RBF affinity)
        - 'hdbscan'    : HDBSCAN (optional, auto-determines K)

    Parameters
    ----------
    method : str
        Clustering method (default 'kmeans').
    n_states : int
        Target number of states K (ignored by HDBSCAN when auto).
    random_state : int
        Random seed for reproducibility.
    **kwargs
        Additional keyword arguments passed to the underlying clustering
        estimator (e.g., ``n_init`` for KMeans, ``covariance_type`` for GMM).
    """

    def __init__(
        self,
        method: str = "kmeans",
        n_states: int = 10,
        random_state: int = 42,
        **kwargs,
    ):
        valid = {"kmeans", "gmm", "spectral", "hdbscan"}
        if method not in valid:
            raise ValueError(f"Unknown method '{method}'. Choose from {valid}.")
        if method == "hdbscan" and not _HDBSCAN_AVAILABLE:
            raise ImportError(
                "HDBSCAN is not installed. Install with `pip install hdbscan` "
                "or choose a different method."
            )

        self.method = method
        self.n_states = n_states
        self.random_state = random_state
        self.kwargs = kwargs

        self._model = None
        self._labels: Optional[np.ndarray] = None
        self._centroids: Optional[np.ndarray] = None
        self._gmm: Optional[GaussianMixture] = None

    # ------------------------------------------------------------------
    # Fit / predict
    # ------------------------------------------------------------------

    def fit(self, X_phi: np.ndarray) -> StateDiscovery:
        """Fit the state discovery algorithm on phi(X).

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)
            Representation-space feature matrix.

        Returns
        -------
        self : StateDiscovery
        """
        n_samples = X_phi.shape[0]
        K = self.n_states

        if self.method == "kmeans":
            n_init = self.kwargs.pop("n_init", 20)
            model = KMeans(
                n_clusters=K,
                n_init=n_init,
                random_state=self.random_state,
                **self.kwargs,
            )
            labels = model.fit_predict(X_phi)
            centroids = model.cluster_centers_
            self._model = model

        elif self.method == "gmm":
            cov_type = self.kwargs.pop("covariance_type", "full")
            gmm = GaussianMixture(
                n_components=K,
                covariance_type=cov_type,
                random_state=self.random_state,
                **self.kwargs,
            )
            gmm.fit(X_phi)
            labels = gmm.predict(X_phi)
            centroids = gmm.means_
            self._gmm = gmm
            self._model = gmm

        elif self.method == "spectral":
            gamma = self.kwargs.pop("gamma", None)
            model = SpectralClustering(
                n_clusters=K,
                affinity="rbf",
                gamma=gamma,
                random_state=self.random_state,
                **self.kwargs,
            )
            labels = model.fit_predict(X_phi)
            # compute centroids as per-cluster mean
            unique = np.unique(labels)
            centroids = np.array(
                [X_phi[labels == k].mean(axis=0) for k in unique]
            )
            self._model = model

        elif self.method == "hdbscan":
            mc = self.kwargs.pop("min_cluster_size", 10)
            ms = self.kwargs.pop("min_samples", None)
            clusterer = hdbscan.HDBSCAN(
                min_cluster_size=mc, min_samples=ms, **self.kwargs,
            )
            labels = clusterer.fit_predict(X_phi)

            # noise points (label == -1) are excluded from centroid computation
            unique = sorted(set(labels) - {-1})
            if len(unique) == 0:
                # fallback: no clusters found, treat everything as one state
                unique = [0]
                labels[:] = 0
            centroids = np.array(
                [X_phi[labels == k].mean(axis=0) for k in unique]
            )
            # map original labels to contiguous 0..K-1
            label_map = {old: new for new, old in enumerate(unique)}
            mapped = np.array(
                [label_map.get(l, -1) for l in labels], dtype=int
            )
            # noise points (-1) get assigned to nearest centroid
            for i in range(len(mapped)):
                if mapped[i] == -1:
                    dists = np.linalg.norm(centroids - X_phi[i], axis=1)
                    mapped[i] = int(np.argmin(dists))
            labels = mapped
            self._model = clusterer

        self._labels = labels
        self._centroids = centroids
        return self

    def predict(self, X_phi: np.ndarray) -> np.ndarray:
        """Assign state IDs to new phi(x) samples.

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)

        Returns
        -------
        labels : np.ndarray, shape (N,)
        """
        if self._centroids is None:
            raise RuntimeError("StateDiscovery has not been fitted yet.")

        if self.method == "gmm" and self._gmm is not None:
            return self._gmm.predict(X_phi)

        # fallback: nearest-centroid assignment
        dists = pairwise_distances(X_phi, self._centroids, metric="euclidean")
        return np.argmin(dists, axis=1)

    def fit_predict(self, X_phi: np.ndarray) -> np.ndarray:
        """Convenience: fit and return labels in one call.

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)

        Returns
        -------
        labels : np.ndarray, shape (N,)
        """
        self.fit(X_phi)
        return self._labels  # type: ignore[return-value]

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    def get_centroids(self) -> np.ndarray:
        """Return state centroids, shape (K, d)."""
        if self._centroids is None:
            raise RuntimeError("StateDiscovery has not been fitted yet.")
        return self._centroids

    def get_probabilities(self, X_phi: np.ndarray) -> np.ndarray:
        """Return soft assignment probabilities, shape (N, K).

        - For GMM: uses ``predict_proba``.
        - For other methods: uses distance-based softmax with T=1.

        Parameters
        ----------
        X_phi : np.ndarray, shape (N, d)

        Returns
        -------
        probs : np.ndarray, shape (N, K)
        """
        if self._centroids is None:
            raise RuntimeError("StateDiscovery has not been fitted yet.")

        if self.method == "gmm" and self._gmm is not None:
            return self._gmm.predict_proba(X_phi)

        return _softmax_dist(X_phi, self._centroids, temperature=1.0)

    def get_model(self):
        """Return the underlying fitted clustering model (if any)."""
        return self._model

    def get_labels(self) -> np.ndarray:
        """Return the training labels from the last fit, shape (N,)."""
        if self._labels is None:
            raise RuntimeError("StateDiscovery has not been fitted yet.")
        return self._labels

    @property
    def is_fitted(self) -> bool:
        """Return True if the model has been fitted."""
        return self._centroids is not None
