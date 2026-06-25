"""Shared pytest fixtures for SCX test suite."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pytest

# Ensure scx package is importable without pip install
_src = Path(__file__).resolve().parents[1] / "src"
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from scx.core.config import SCXConfig


# ---------------------------------------------------------------------------
# Synthetic data fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_data_2d() -> tuple[np.ndarray, np.ndarray]:
    """Synthetic 2D data: 4 Gaussian clusters, 100 samples each.

    Returns
    -------
    X : np.ndarray, shape (400, 2)
    y : np.ndarray, shape (400,)
    """
    rng = np.random.default_rng(42)
    n_per_cluster = 100
    centers = [[0, 0], [5, 0], [0, 5], [5, 5]]
    X_list, y_list = [], []
    for i, c in enumerate(centers):
        X_list.append(rng.normal(c, 0.5, (n_per_cluster, 2)))
        y_list.append(np.full(n_per_cluster, i))
    return np.vstack(X_list), np.concatenate(y_list)


@pytest.fixture
def sample_data_highdim() -> tuple[np.ndarray, np.ndarray]:
    """Synthetic high-dimensional data: 3 clusters, 10 features.

    Returns
    -------
    X : np.ndarray, shape (150, 10)
    y : np.ndarray, shape (150,)
    """
    rng = np.random.default_rng(42)
    centers = [[0] * 10, [3] * 10, [6] * 10]
    X_list, y_list = [], []
    for i, c in enumerate(centers):
        X_list.append(rng.normal(c, 0.5, (50, 10)))
        y_list.append(np.full(50, i))
    return np.vstack(X_list), np.concatenate(y_list)


@pytest.fixture
def sample_data_single_cluster() -> tuple[np.ndarray, np.ndarray]:
    """Single cluster — edge case for state discovery.

    Returns
    -------
    X : np.ndarray, shape (100, 2)
    y : np.ndarray, shape (100,)
    """
    rng = np.random.default_rng(42)
    return rng.normal(0, 0.5, (100, 2)), np.zeros(100, dtype=int)


@pytest.fixture
def sample_data_empty() -> tuple[np.ndarray, np.ndarray]:
    """Empty input — edge case."""
    return np.empty((0, 2)), np.empty((0,), dtype=int)


# ---------------------------------------------------------------------------
# Expert fixtures
# ---------------------------------------------------------------------------


def _make_expert(bias_vector: list[float]) -> Callable:
    """Create a simple synthetic expert function."""
    return lambda x: np.sin(x[:, 0]) + bias_vector[0] * x[:, 1]


@pytest.fixture
def sample_experts() -> list[Callable]:
    """3 synthetic experts, each with a bias toward different states.

    - Expert A: bias toward feature 0
    - Expert B: bias toward feature 1
    - Expert C: balanced
    """
    return [
        _make_expert([0.5, 0.1]),  # expert A
        _make_expert([0.1, 0.5]),  # expert B
        _make_expert([0.3, 0.3]),  # expert C
    ]


@pytest.fixture
def single_expert() -> list[Callable]:
    """Single expert — edge case."""
    return [lambda x: np.sin(x[:, 0]) + 0.3 * x[:, 1]]


@pytest.fixture
def identical_experts() -> list[Callable]:
    """Two experts with identical predictions — conflict = 0."""
    fn = lambda x: np.sin(x[:, 0]) + 0.3 * x[:, 1]
    return [fn, fn]


# ---------------------------------------------------------------------------
# SCX config fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scx_config() -> SCXConfig:
    """Default SCX config for testing (4 states, 3 experts, quiet)."""
    return SCXConfig(n_states=4, n_experts=3, verbose=False)


@pytest.fixture
def scx_config_small() -> SCXConfig:
    """Minimal config for fast tests."""
    return SCXConfig(n_states=2, n_experts=2, verbose=False)


# ---------------------------------------------------------------------------
# Pre-computed fixture: centoids from sample_data_2d
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_centroids() -> np.ndarray:
    """Known centroids of the 4 clusters in sample_data_2d."""
    return np.array([[0.0, 0.0], [5.0, 0.0], [0.0, 5.0], [5.0, 5.0]], dtype=float)


@pytest.fixture
def sample_state_assignments(sample_data_2d) -> np.ndarray:
    """Ground-truth state assignments for sample_data_2d (4 clusters)."""
    _, y = sample_data_2d
    return y.astype(int)


@pytest.fixture
def random_residuals() -> np.ndarray:
    """Random residuals for testing noise/redundancy scores."""
    rng = np.random.default_rng(42)
    return rng.uniform(0.0, 1.0, size=400)


# ---------------------------------------------------------------------------
# Valuation fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def state_metrics_dict() -> dict[int, dict[str, float]]:
    """State metrics suitable for DataClassifier and StateValue tests.

    4 states with varied characteristics.
    """
    return {
        0: {
            "mean_residual": 0.01,  # low error
            "proportion": 0.40,  # high density
            "consistency": 0.95,  # high consistency
            "redundancy": 0.85,  # high redundancy
            "noise_score": 0.02,
            "similarity": 0.80,
            "boundary": 0.30,
            "learnability": 0.80,
        },
        1: {
            "mean_residual": 0.20,  # high error
            "proportion": 0.35,  # high density
            "consistency": 0.85,  # high consistency
            "redundancy": 0.20,  # low redundancy
            "noise_score": 0.05,
            "similarity": 0.40,
            "boundary": 0.60,
            "learnability": 0.70,
        },
        2: {
            "mean_residual": 0.30,  # high error
            "proportion": 0.02,  # low density
            "consistency": 0.30,  # low consistency
            "redundancy": 0.10,  # low redundancy
            "noise_score": 0.60,
            "similarity": 0.20,
            "boundary": 0.70,
            "learnability": 0.20,
        },
        3: {
            "mean_residual": 0.08,  # medium error
            "proportion": 0.23,  # medium density
            "consistency": 0.75,  # medium-high consistency
            "redundancy": 0.40,  # medium redundancy
            "noise_score": 0.15,
            "similarity": 0.50,
            "boundary": 0.50,
            "learnability": 0.60,
        },
    }
