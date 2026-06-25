"""SyntheticDataGenerator — generates 4-state + 3-expert synthetic data with noise and redundancy.

The generator creates:
- 4 Gaussian clusters in 2D (states S0-S3)
- 3 experts with systematic bias patterns
- 5% label noise (random flip in classification, Gaussian in regression)
- 20% redundant samples (duplicates near the first cluster)
"""

from __future__ import annotations

from typing import Any, Callable

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances


class SyntheticDataGenerator:
    """Generate synthetic multi-state data with controlled noise and redundancy.

    Parameters
    ----------
    n_states : int
        Number of Gaussian clusters (states). Default 4.
    n_experts : int
        Number of synthetic experts. Default 3.
    n_samples : int
        Total samples (before redundancy injection). Default 500.
    noise_ratio : float
        Fraction of labels to corrupt with noise (0..1). Default 0.05.
    redundancy_ratio : float
        Fraction of redundant samples to add near S0. Default 0.2.
    random_state : int
        Random seed for reproducibility. Default 42.
    """

    def __init__(
        self,
        n_states: int = 4,
        n_experts: int = 3,
        n_samples: int = 500,
        noise_ratio: float = 0.05,
        redundancy_ratio: float = 0.2,
        random_state: int = 42,
    ) -> None:
        self.n_states = n_states
        self.n_experts = n_experts
        self.n_samples = n_samples
        self.noise_ratio = noise_ratio
        self.redundancy_ratio = redundancy_ratio
        self.random_state = random_state

        self.rng: np.random.Generator | None = None
        self.X: np.ndarray | None = None
        self.y_true: np.ndarray | None = None
        self.state_labels: np.ndarray | None = None
        self.expert_predictions: np.ndarray | None = None
        self.noisy_mask: np.ndarray | None = None
        self.redundant_mask: np.ndarray | None = None

        self._centers: list[list[float]] = []
        self._expert_fns: list[Callable] = []

    def _build_clusters(self) -> tuple[np.ndarray, np.ndarray]:
        """Generate 2D Gaussian cluster data.

        Returns
        -------
        X : np.ndarray, shape (n_states * per_state, 2)
        state_labels : np.ndarray, shape (n_states * per_state,)
        """
        self.rng = np.random.default_rng(self.random_state)
        self._centers = [
            [0.0, 0.0],
            [5.0, 0.0],
            [0.0, 5.0],
            [5.0, 5.0],
        ][: self.n_states]

        per_state = self.n_samples // self.n_states
        X_list: list[np.ndarray] = []
        labels_list: list[np.ndarray] = []

        for i, center in enumerate(self._centers):
            X_list.append(
                self.rng.normal(loc=center, scale=0.5, size=(per_state, 2))
            )
            labels_list.append(np.full(per_state, i, dtype=int))

        return np.vstack(X_list), np.concatenate(labels_list)

    def _build_experts(self) -> list[Callable]:
        """Create expert functions with systematic bias patterns.

        Expert A: accurate on S0, S1; biased on S2, S3.
        Expert B: accurate on S2; biased elsewhere.
        Expert C: accurate on S3; biased elsewhere.

        Returns
        -------
        list[Callable]
            Expert prediction functions.
        """
        centers = np.array(self._centers)  # (K, 2)

        def _expert_a(x: np.ndarray) -> np.ndarray:
            """Good at S0 (0,0) and S1 (5,0); biased at S2 (0,5) and S3 (5,5)."""
            # True label is based on nearest center
            dists = pairwise_distances(x, centers)
            base = np.argmin(dists, axis=1).astype(float)
            # Add bias: over-predict S0 for ambiguous points
            bias = 0.3 * np.exp(-((x[:, 0] - 2.5) ** 2) / 5.0)
            return base + bias

        def _expert_b(x: np.ndarray) -> np.ndarray:
            """Good at S2 (0,5); biased by x[:,0] in other regions."""
            dists = pairwise_distances(x, centers)
            base = np.argmin(dists, axis=1).astype(float)
            # Systematic shift for points far from S2
            bias = 0.4 * np.sin(x[:, 1] / 2.0)
            return base + bias

        def _expert_c(x: np.ndarray) -> np.ndarray:
            """Good at S3 (5,5); biased by x[:,1] in other regions."""
            dists = pairwise_distances(x, centers)
            base = np.argmin(dists, axis=1).astype(float)
            bias = 0.4 * np.sin(x[:, 0] / 2.0)
            return base + bias

        return [_expert_a, _expert_b, _expert_c]

    def _inject_noise(self, y: np.ndarray) -> np.ndarray:
        """Randomly flip a fraction of labels.

        Parameters
        ----------
        y : np.ndarray, shape (N,)
            Clean labels (discrete 0..K-1).

        Returns
        -------
        y_noisy : np.ndarray, shape (N,)
        """
        if self.rng is None:
            self.rng = np.random.default_rng(self.random_state)
        y_noisy = y.copy().astype(int)
        n_noise = max(1, int(self.noise_ratio * len(y)))
        indices = self.rng.choice(len(y), size=n_noise, replace=False)
        for idx in indices:
            possible = [c for c in range(self.n_states) if c != y[idx]]
            y_noisy[idx] = self.rng.choice(possible)
        self.noisy_mask = np.zeros(len(y), dtype=bool)
        self.noisy_mask[indices] = True
        return y_noisy.astype(float)

    def _inject_redundancy(
        self, X: np.ndarray, y: np.ndarray, state_labels: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Duplicate samples from S0 (first cluster) with small perturbations.

        Parameters
        ----------
        X : np.ndarray, shape (N, 2)
        y : np.ndarray, shape (N,)
        state_labels : np.ndarray, shape (N,)

        Returns
        -------
        X_aug : np.ndarray
        y_aug : np.ndarray
        state_aug : np.ndarray
        """
        if self.rng is None:
            self.rng = np.random.default_rng(self.random_state)
        s0_mask = state_labels == 0
        s0_indices = np.where(s0_mask)[0]
        n_dup = max(1, int(self.redundancy_ratio * len(X)))
        chosen = self.rng.choice(s0_indices, size=min(n_dup, len(s0_indices)), replace=True)

        noise = self.rng.normal(0, 0.1, size=(len(chosen), X.shape[1]))
        X_dup = X[chosen] + noise
        y_dup = y[chosen]
        state_dup = state_labels[chosen]

        self.redundant_mask = np.zeros(len(X) + len(chosen), dtype=bool)
        self.redundant_mask[len(X):] = True

        X_aug = np.vstack([X, X_dup])
        y_aug = np.hstack([y, y_dup])
        state_aug = np.hstack([state_labels, state_dup])
        return X_aug, y_aug, state_aug

    def generate(self) -> dict[str, Any]:
        """Run the full data generation pipeline.

        Returns
        -------
        dict
            ``X``, ``y_true``, ``state_labels``, ``expert_predictions``,
            ``noisy_mask``, ``redundant_mask``, ``centers``.
        """
        # 1. Build clusters
        X, state_labels = self._build_clusters()

        # 2. Build experts
        self._expert_fns = self._build_experts()

        # 3. Expert predictions (before noise — experts see clean data)
        predictions_list = []
        for fn in self._expert_fns:
            predictions_list.append(fn(X))
        self.expert_predictions = np.array(predictions_list)  # (M, N)

        # 4. Inject label noise
        y_clean = state_labels.astype(float)
        y_noisy = self._inject_noise(y_clean)

        # 5. Inject redundancy (from S0)
        X_aug, y_aug, state_aug = self._inject_redundancy(X, y_noisy, state_labels)

        # Also add expert predictions for augmented data
        preds_aug_list = []
        for fn in self._expert_fns:
            preds_aug_list.append(fn(X_aug))
        expert_preds_aug = np.array(preds_aug_list)

        self.X = X_aug
        self.y_true = y_aug
        self.state_labels = state_aug

        return {
            "X": X_aug,
            "y_true": y_aug,
            "state_labels": state_aug,
            "expert_predictions": expert_preds_aug,
            "noisy_mask": self.noisy_mask,
            "redundant_mask": self.redundant_mask,
            "centers": np.array(self._centers),
            "n_states": self.n_states,
            "n_experts": self.n_experts,
        }

    def plot(self, save_path: str | None = None) -> None:
        """Visualise the generated data: states, noise, redundancy, expert bias.

        Parameters
        ----------
        save_path : str, optional
            If provided, save the figure to this path.
        """
        if self.X is None:
            raise RuntimeError("Call generate() before plot().")

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # --- Panel 1: State map ---
        ax = axes[0, 0]
        if self.state_labels is not None:
            scatter = ax.scatter(
                self.X[:, 0], self.X[:, 1],
                c=self.state_labels, cmap="viridis", s=15, alpha=0.7,
            )
            ax.set_title("State Assignment")
            fig.colorbar(scatter, ax=ax, label="State ID")
        ax.set_xlabel("x0")
        ax.set_ylabel("x1")
        ax.grid(True, alpha=0.3)

        # --- Panel 2: Noisy vs clean samples ---
        ax = axes[0, 1]
        if self.noisy_mask is not None:
            clean = ~self.noisy_mask
            ax.scatter(
                self.X[clean, 0], self.X[clean, 1],
                c="blue", s=10, alpha=0.4, label="Clean",
            )
            ax.scatter(
                self.X[self.noisy_mask, 0], self.X[self.noisy_mask, 1],
                c="red", s=30, alpha=0.8, marker="x", label="Noisy",
            )
            ax.set_title(f"Noise Injection ({self.noise_ratio*100:.0f}%)")
            ax.legend()
        ax.set_xlabel("x0")
        ax.set_ylabel("x1")
        ax.grid(True, alpha=0.3)

        # --- Panel 3: Redundant samples ---
        ax = axes[1, 0]
        if self.redundant_mask is not None:
            orig = ~self.redundant_mask
            ax.scatter(
                self.X[orig, 0], self.X[orig, 1],
                c="blue", s=10, alpha=0.4, label="Original",
            )
            ax.scatter(
                self.X[self.redundant_mask, 0], self.X[self.redundant_mask, 1],
                c="orange", s=15, alpha=0.7, marker="s", label="Redundant",
            )
            ax.set_title(f"Redundancy Near S0 ({self.redundancy_ratio*100:.0f}%)")
            ax.legend()
        ax.set_xlabel("x0")
        ax.set_ylabel("x1")
        ax.grid(True, alpha=0.3)

        # --- Panel 4: Expert predictions (example) ---
        ax = axes[1, 1]
        if self.expert_predictions is not None:
            for m in range(min(3, self.expert_predictions.shape[0])):
                ax.scatter(
                    self.X[:, 0], self.X[:, 1],
                    c=self.expert_predictions[m],
                    cmap="coolwarm", s=10, alpha=0.5,
                )
                ax.set_title(f"Expert {chr(65+m)} Predictions")
        ax.set_xlabel("x0")
        ax.set_ylabel("x1")
        ax.grid(True, alpha=0.3)

        fig.suptitle("Synthetic Data for SCX Framework", fontsize=14)
        fig.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
            plt.close(fig)
        else:
            plt.show()


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    gen = SyntheticDataGenerator(n_states=4, n_experts=3, n_samples=500,
                                 noise_ratio=0.05, redundancy_ratio=0.2,
                                 random_state=42)
    data = gen.generate()
    print(f"Generated data: X={data['X'].shape}, states={len(np.unique(data['state_labels']))}")
    print(f"  Expert predictions: {data['expert_predictions'].shape}")
    print(f"  Noisy samples: {data['noisy_mask'].sum()}")
    print(f"  Redundant samples: {data['redundant_mask'].sum()}")
    print("Data generation successful.")
