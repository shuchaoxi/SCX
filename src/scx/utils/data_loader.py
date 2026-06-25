# scx/utils/data_loader.py
# DataLoader -- unified data loading interface for the SCX framework.

from __future__ import annotations

from typing import Any, Callable

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


class DataLoader:
    """Unified data loading interface for SCX.

    Provides static methods to load data from various sources (NumPy,
    pandas DataFrames, extended XYZ files for MLIP) and to inject
    controlled noise or redundancy for experiments.
    """

    @staticmethod
    def from_numpy(
        X: np.ndarray,
        y: np.ndarray | None = None,
        experts: list[Callable] | None = None,
    ) -> dict[str, Any]:
        """Wrap NumPy arrays into a standard SCX data dictionary.

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
            Feature matrix.
        y : np.ndarray, shape (N,) or None
            Target labels.
        experts : list[Callable] or None
            Optional list of expert prediction functions.

        Returns
        -------
        data : dict
            Keys: ``X``, ``y`` (if provided), ``experts`` (if provided),
            ``n_samples``, ``n_features``.
        """
        X = np.asarray(X)
        data: dict[str, Any] = {
            "X": X,
            "n_samples": X.shape[0],
            "n_features": X.shape[1] if X.ndim > 1 else 1,
        }
        if y is not None:
            data["y"] = np.asarray(y)
        if experts is not None:
            data["experts"] = experts
        return data

    @staticmethod
    def from_dataframe(
        df: pd.DataFrame,
        feature_cols: list[str],
        label_col: str | None = None,
    ) -> dict[str, Any]:
        """Load data from a pandas DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
        feature_cols : list[str]
            Column names to use as features.
        label_col : str or None
            Column name to use as target label.

        Returns
        -------
        data : dict
            Keys: ``X``, ``y`` (if label_col provided), ``feature_names``,
            ``n_samples``, ``n_features``.
        """
        X = df[feature_cols].values
        data: dict[str, Any] = {
            "X": X,
            "feature_names": feature_cols,
            "n_samples": X.shape[0],
            "n_features": len(feature_cols),
        }
        if label_col is not None and label_col in df.columns:
            data["y"] = df[label_col].values
        return data

    @staticmethod
    def from_extxyz(
        path: str,
        descriptor_fn: Callable[[Any], np.ndarray] | None = None,
    ) -> dict[str, Any]:
        """Load data from an extended XYZ file (MLIP use-case).

        Requires the ``ase`` package.  If ``descriptor_fn`` is provided,
        per-atom descriptors are computed and stored as ``phi``.

        Parameters
        ----------
        path : str
            Path to the ``.extxyz`` file.
        descriptor_fn : Callable or None
            ``descriptor_fn(atoms) -> np.ndarray, shape (n_atoms, d)``.
            If ``None``, raw atomic positions (flattened) are used.

        Returns
        -------
        data : dict
            Keys: ``structures`` (list of ``ase.Atoms``), ``X`` (descriptors
            if descriptor_fn given), ``energies``, ``forces``,
            ``n_structures``, ``n_atoms``.
        """
        try:
            from ase.io import read
        except ImportError:
            raise ImportError(
                "ASE is required for .extxyz loading. "
                "Install with: pip install ase"
            )

        structures = list(read(path, index=":"))
        energies = np.array([atoms.get_potential_energy() for atoms in structures])
        forces_list = [atoms.get_forces() for atoms in structures]

        data: dict[str, Any] = {
            "structures": structures,
            "energies": energies,
            "forces": forces_list,
            "n_structures": len(structures),
            "n_atoms": sum(len(atoms) for atoms in structures),
        }

        if descriptor_fn is not None:
            descriptors = []
            for atoms in structures:
                desc = descriptor_fn(atoms)
                descriptors.append(np.asarray(desc))
            data["phi"] = np.vstack(descriptors) if descriptors else np.array([])

        return data

    @staticmethod
    def split(
        data: dict[str, Any],
        test_size: float = 0.2,
        random_state: int = 42,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Split an SCX data dictionary into train / test subsets.

        Parameters
        ----------
        data : dict
            Must contain at least ``X`` and optionally ``y``.
        test_size : float
            Fraction of samples to use for testing (default ``0.2``).
        random_state : int
            Random seed for reproducibility.

        Returns
        -------
        train_data, test_data : dicts
        """
        X = data["X"]
        y = data.get("y", None)

        # Only use stratify for classification (integer labels with few classes)
        use_stratify = False
        if y is not None:
            unique_vals = np.unique(y)
            if y.dtype in (np.int32, np.int64, int, bool) and len(unique_vals) < 20:
                use_stratify = True

        if y is not None:
            X_tr, X_te, y_tr, y_te = train_test_split(
                X, y, test_size=test_size, random_state=random_state,
                stratify=y if use_stratify else None,
            )
        else:
            X_tr, X_te = train_test_split(
                X, test_size=test_size, random_state=random_state,
            )
            y_tr = y_te = None

        train_data: dict[str, Any] = {
            "X": X_tr,
            "n_samples": X_tr.shape[0],
            "n_features": X_tr.shape[1],
        }
        test_data: dict[str, Any] = {
            "X": X_te,
            "n_samples": X_te.shape[0],
            "n_features": X_te.shape[1],
        }

        if y_tr is not None:
            train_data["y"] = y_tr
        if y_te is not None:
            test_data["y"] = y_te

        # Pass through additional keys
        for key in data:
            if key not in ("X", "y", "n_samples", "n_features"):
                train_data[key] = data[key]
                test_data[key] = data[key]

        return train_data, test_data

    @staticmethod
    def inject_noise(
        y: np.ndarray,
        noise_ratio: float = 0.1,
        noise_std: float = 1.0,
        random_state: int | None = None,
    ) -> np.ndarray:
        """Inject Gaussian noise into labels (regression setting).

        Parameters
        ----------
        y : np.ndarray, shape (N,)
            Clean labels.
        noise_ratio : float
            Fraction of samples to corrupt (default ``0.1``).
        noise_std : float
            Standard deviation of the Gaussian noise (default ``1.0``).
        random_state : int or None
            Random seed.

        Returns
        -------
        y_noisy : np.ndarray, shape (N,)
        """
        y = np.asarray(y, dtype=float)
        rng = np.random.RandomState(random_state)
        n_noise = max(1, int(noise_ratio * len(y)))
        indices = rng.choice(len(y), size=n_noise, replace=False)
        y_noisy = y.copy()
        y_noisy[indices] += rng.normal(0, noise_std, size=n_noise)
        return y_noisy

    @staticmethod
    def inject_redundancy(
        X: np.ndarray,
        y: np.ndarray,
        redundancy_ratio: float = 0.3,
        noise_scale: float = 0.05,
        random_state: int | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Inject redundant samples by duplicating with small perturbations.

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
        y : np.ndarray, shape (N,)
        redundancy_ratio : float
            Fraction of redundant samples to add (default ``0.3``).
        noise_scale : float
            Standard deviation of the perturbation noise (default ``0.05``).
        random_state : int or None

        Returns
        -------
        X_aug : np.ndarray, shape (N + n_dup, d)
        y_aug : np.ndarray, shape (N + n_dup,)
        """
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        rng = np.random.RandomState(random_state)
        N = X.shape[0]
        n_dup = max(1, int(redundancy_ratio * N))
        indices = rng.choice(N, size=n_dup, replace=False)

        X_dup = X[indices] + rng.normal(0, noise_scale, size=(n_dup, X.shape[1]))
        y_dup = y[indices]

        X_aug = np.vstack([X, X_dup])
        y_aug = np.hstack([y, y_dup])
        return X_aug, y_aug
