# scx/utils/helpers.py
# Pure-numpy utility functions used throughout the SCX framework.

from __future__ import annotations

from typing import Generator, Iterator, Tuple

import numpy as np


def safe_divide(
    a: np.ndarray | float,
    b: np.ndarray | float,
    eps: float = 1e-8,
) -> np.ndarray | float:
    """Element-wise division with a small epsilon to avoid division by zero.

    Parameters
    ----------
    a : array or float
        Numerator.
    b : array or float
        Denominator.
    eps : float
        Small constant added to ``b`` (default ``1e-8``).

    Returns
    -------
    result : same shape as inputs
        ``a / (b + eps)``.
    """
    return np.asarray(a, dtype=float) / (np.asarray(b, dtype=float) + eps)


def softmax(
    x: np.ndarray,
    temperature: float = 1.0,
    axis: int = -1,
) -> np.ndarray:
    """Numerically stable softmax with temperature scaling.

    Parameters
    ----------
    x : np.ndarray
        Input logits.
    temperature : float
        Temperature parameter (default ``1.0``).
        ``temperature -> 0`` approximates argmax;
        ``temperature -> inf`` flattens the distribution.
    axis : int
        Axis along which to apply softmax (default ``-1``).

    Returns
    -------
    probs : np.ndarray
        Probability distribution, same shape as ``x``.
    """
    x = np.asarray(x, dtype=float)
    t = max(temperature, 1e-12)
    x_scaled = x / t
    x_shifted = x_scaled - np.max(x_scaled, axis=axis, keepdims=True)
    exp_x = np.exp(x_shifted)
    return exp_x / (np.sum(exp_x, axis=axis, keepdims=True) + 1e-12)


def rbf_kernel(
    X: np.ndarray,
    Y: np.ndarray | None = None,
    sigma: float = 1.0,
) -> np.ndarray:
    """Compute the RBF (Gaussian) kernel matrix.

    ``K[i, j] = exp(-||X[i] - Y[j]||^2 / (2 * sigma^2))``

    Parameters
    ----------
    X : np.ndarray, shape (N, d)
    Y : np.ndarray, shape (M, d) or None
        If ``None``, ``Y = X``.
    sigma : float
        Kernel width (default ``1.0``).

    Returns
    -------
    K : np.ndarray, shape (N, M)
    """
    X = np.asarray(X, dtype=float)
    if Y is None:
        Y = X
    else:
        Y = np.asarray(Y, dtype=float)

    sq_norm = pairwise_distance(X, Y, metric="sqeuclidean")
    return np.exp(-sq_norm / (2.0 * sigma * sigma + 1e-12))


def pairwise_distance(
    X: np.ndarray,
    Y: np.ndarray | None = None,
    metric: str = "euclidean",
) -> np.ndarray:
    """Compute pairwise distance matrix between rows of ``X`` and ``Y``.

    Parameters
    ----------
    X : np.ndarray, shape (N, d)
    Y : np.ndarray, shape (M, d) or None
        If ``None``, ``Y = X``.
    metric : str
        ``"euclidean"`` or ``"sqeuclidean"`` (default ``"euclidean"``).

    Returns
    -------
    D : np.ndarray, shape (N, M)
    """
    X = np.asarray(X, dtype=float)
    if Y is None:
        Y = X
    else:
        Y = np.asarray(Y, dtype=float)

    # Squared Euclidean via (a-b)^2 = a^2 + b^2 - 2ab
    X_norm = np.sum(X ** 2, axis=1, keepdims=True)
    Y_norm = np.sum(Y ** 2, axis=1, keepdims=True)
    D_sq = X_norm + Y_norm.T - 2.0 * np.dot(X, Y.T)
    D_sq = np.clip(D_sq, 0.0, None)  # numerical safety

    if metric == "sqeuclidean":
        return D_sq
    return np.sqrt(D_sq + 1e-12)


def entropy(probs: np.ndarray, axis: int = -1) -> np.ndarray:
    """Compute Shannon entropy along an axis.

    ``H(p) = -sum(p * log(p + eps))``

    Parameters
    ----------
    probs : np.ndarray
        Probability values (should be non-negative and sum to 1 along
        the given axis).
    axis : int
        Axis along which to compute entropy (default ``-1``).

    Returns
    -------
    H : np.ndarray
        Entropy values, shape is ``probs.shape`` with ``axis`` removed.
    """
    probs = np.asarray(probs, dtype=float)
    probs = np.clip(probs, 1e-12, 1.0)
    return -np.sum(probs * np.log(probs), axis=axis)


def normalize(
    X: np.ndarray,
    method: str = "standard",
) -> np.ndarray:
    """Normalize a feature matrix.

    Parameters
    ----------
    X : np.ndarray, shape (N, d)
    method : str
        ``"standard"`` : zero-mean unit-variance (z-score).
        ``"minmax"``   : scale to ``[0, 1]``.
        ``"l2"``       : unit L2 norm per row.

    Returns
    -------
    X_norm : np.ndarray, shape (N, d)
    """
    X = np.asarray(X, dtype=float)

    if method == "standard":
        mu = np.mean(X, axis=0, keepdims=True)
        std = np.std(X, axis=0, keepdims=True)
        return (X - mu) / (std + 1e-12)

    if method == "minmax":
        xmin = np.min(X, axis=0, keepdims=True)
        xmax = np.max(X, axis=0, keepdims=True)
        return (X - xmin) / (xmax - xmin + 1e-12)

    if method == "l2":
        norm = np.linalg.norm(X, axis=1, keepdims=True)
        return X / (norm + 1e-12)

    raise ValueError(
        f"Unknown method '{method}'. Expected one of: standard, minmax, l2."
    )


def batch_iterator(
    X: np.ndarray,
    y: np.ndarray | None = None,
    batch_size: int = 32,
) -> Generator[Tuple[np.ndarray, np.ndarray | None], None, None]:
    """Generate mini-batches from feature matrix ``X`` (and optionally ``y``).

    Parameters
    ----------
    X : np.ndarray, shape (N, d)
    y : np.ndarray, shape (N,) or None
    batch_size : int
        Batch size (default ``32``). The last batch may be smaller.

    Yields
    ------
    X_batch : np.ndarray, shape (batch_size, d)
    y_batch : np.ndarray, shape (batch_size,) or None
    """
    X = np.asarray(X)
    N = X.shape[0]
    indices = np.arange(N)
    np.random.shuffle(indices)

    for start in range(0, N, batch_size):
        end = min(start + batch_size, N)
        batch_idx = indices[start:end]
        X_batch = X[batch_idx]
        y_batch = y[batch_idx] if y is not None else None
        yield X_batch, y_batch
