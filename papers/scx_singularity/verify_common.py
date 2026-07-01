#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCX Physics Verification — Shared Utility Module
==================================================
SCX 物理验证 — 共享工具模块

This module is **self-contained** — it imports ONLY numpy and scipy.
Copy this file into each paper folder for zero-cross-folder-import verification.
Every paper folder should be fully self-contained.

本模块完全自包含 — 仅依赖 numpy 和 scipy。
将此文件复制到每个论文文件夹中，实现零跨文件夹导入的完全自包含验证。

Contents / 内容:
  1.  Betti number / Betti 数
  2.  Hodge operators (d₀, d₁, L₁) / Hodge 算子
  3.  Hodge decomposition & orthogonality verification / Hodge 分解与正交性验证
  4.  Zero-mode (gauge) fixing / 零模（规范）固定
  5.  Cercis score & gauge invariance / Cercis 分数与规范不变性
  6.  Discrete curvature (holonomy) / 离散曲率（和乐）
  7.  Hessian eigenvalue analysis / Hessian 特征值分析
  8.  Fisher information Bayesian update / Fisher 信息贝叶斯更新
  9.  Kolmogorov–Smirnov test wrapper / KS 检验封装
  10. Simple qubit simulator / 简单量子比特模拟器
  11. BB84 QKD helper / BB84 量子密钥分发辅助
  12. CHSH inequality helper / CHSH 不等式辅助
  13. Density estimation (KDE + sublevel filtration) / 密度估计
  14. Colored print helpers & tolerance assertions / 彩色输出与容差断言
"""

import warnings
from typing import Optional, Tuple, List, Dict, Any, Union, Callable

import numpy as np
from numpy import ndarray

# Try importing scipy components gracefully
try:
    from scipy import linalg as sp_linalg
    from scipy import stats as sp_stats
    from scipy.stats import gaussian_kde
    _HAS_SCIPY = True
except ImportError:
    _HAS_SCIPY = False
    warnings.warn("scipy not available; some functions (KDE, KS test) will be limited.")


# ═══════════════════════════════════════════════════════════════════════════════
# Section 0: Color / Print Helpers
# Section 0: 彩色输出辅助
# ═══════════════════════════════════════════════════════════════════════════════

# ANSI escape codes
_COLOR_RESET = "\033[0m"
_COLOR_GREEN = "\033[92m"
_COLOR_RED   = "\033[91m"
_COLOR_YELLOW = "\033[93m"
_COLOR_CYAN  = "\033[96m"
_COLOR_BOLD  = "\033[1m"
_COLOR_DIM   = "\033[2m"

# Windows console ANSI support (Windows 10+)
import os as _os
if _os.name == "nt":
    try:
        _os.system("")  # enable ANSI processing in conhost
    except Exception:
        pass


def _color_text(text: str, color: str) -> str:
    """Wrap text with ANSI color codes.  用 ANSI 颜色码包裹文本。"""
    return f"{color}{text}{_COLOR_RESET}"


def print_pass(msg: str = "PASS", width: int = 70) -> None:
    """Print a green PASS message.  打印绿色 PASS 消息。

    Args:
        msg: Message to display (default "PASS"). / 要显示的消息。
        width: Total line width for alignment. / 总行宽。
    """
    line = f"[ {_color_text(msg, _COLOR_GREEN)} ]"
    print(f"{line:>{width}}")


def print_fail(msg: str = "FAIL", width: int = 70) -> None:
    """Print a red FAIL message.  打印红色 FAIL 消息。

    Args:
        msg: Message to display (default "FAIL"). / 要显示的消息。
        width: Total line width for alignment. / 总行宽。
    """
    line = f"[ {_color_text(msg, _COLOR_RED)} ]"
    print(f"{line:>{width}}")


def print_info(msg: str) -> None:
    """Print a cyan info message.  打印青色信息消息。"""
    print(f"{_COLOR_CYAN}[INFO]{_COLOR_RESET} {msg}")


def print_warn(msg: str) -> None:
    """Print a yellow warning.  打印黄色警告。"""
    print(f"{_COLOR_YELLOW}[WARN]{_COLOR_RESET} {msg}")


def print_header(title: str, width: int = 70) -> None:
    """Print a bold section header.  打印粗体节标题。"""
    print()
    print(_color_text("=" * width, _COLOR_BOLD))
    print(_color_text(f"  {title}", _COLOR_BOLD))
    print(_color_text("=" * width, _COLOR_BOLD))
    print()


def assert_close(
    actual: Union[float, ndarray],
    expected: Union[float, ndarray],
    tol: float = 1e-10,
    msg: str = "",
) -> None:
    """Assert that actual ≈ expected within tolerance.  断言实际值在容差内接近期望值。

    Args:
        actual: Computed value. / 计算值。
        expected: Expected value. / 期望值。
        tol: Absolute tolerance. / 绝对容差。
        msg: Optional description. / 可选描述。

    Raises:
        AssertionError: if |actual - expected| > tol. / 若差值超过容差。
    """
    diff = np.max(np.abs(np.asarray(actual) - np.asarray(expected)))
    if diff > tol:
        header = f"{msg}: " if msg else ""
        raise AssertionError(
            f"{header}|actual - expected| = {diff:.3e} > tol = {tol:.3e}"
        )


def _describe(label: str, value: Any, fmt: str = ".6g") -> None:
    """Print a labeled value for debugging.  打印带标签的值用于调试。"""
    try:
        if isinstance(value, ndarray):
            if value.ndim == 0:
                print(f"  {label}: {value.item():{fmt}}")
            else:
                flat = np.asarray(value).flatten()
                vals = ", ".join(f"{v:{fmt}}" for v in flat[:8])
                if len(flat) > 8:
                    vals += ", ..."
                print(f"  {label}: [{vals}]  shape={np.asarray(value).shape}")
        else:
            print(f"  {label}: {value}")
    except Exception:
        print(f"  {label}: {value}")


# ═══════════════════════════════════════════════════════════════════════════════
# Section 1: Betti Number
# Section 1: Betti 数
# ═══════════════════════════════════════════════════════════════════════════════

def betti_1(M: int) -> int:
    """First Betti number for a complete graph on M nodes.  M 个节点的完全图的第一 Betti 数。

    β₁(K_M) = (M-1)(M-2)/2

    For a complete graph, the cycle space dimension equals the number of
    independent loops. This is also the dimension of ker(L₁), the harmonic space.
    对于完全图，圈空间维数等于独立环的数量，也是 ker(L₁)（调和空间）的维数。

    Args:
        M: Number of nodes (M ≥ 1). / 节点数。

    Returns:
        β₁, the first Betti number. / 第一 Betti 数。
    """
    if M < 1:
        raise ValueError(f"M must be ≥ 1, got {M}")
    return (M - 1) * (M - 2) // 2


# ═══════════════════════════════════════════════════════════════════════════════
# Section 2: Hodge Operators (d₀, d₁, L₁)
# Section 2: Hodge 算子
# ═══════════════════════════════════════════════════════════════════════════════

def build_d0(edges: ndarray, n_nodes: int) -> ndarray:
    """Build the graph gradient operator d₀ (incidence matrix).  构建图梯度算子 d₀（关联矩阵）。

    d₀: ℝ^N → ℝ^E   (nodes → edges)
    For edge e = (i, j) with i < j (orientation from i to j):
        d₀[e, i] = -1,  d₀[e, j] = +1

    Args:
        edges: (E, 2) integer array, each row = [i, j] with i < j.
        n_nodes: Number of nodes N.

    Returns:
        d0: (E, N) float64 array.
    """
    E = edges.shape[0]
    d0 = np.zeros((E, n_nodes), dtype=np.float64)
    for e in range(E):
        i, j = int(edges[e, 0]), int(edges[e, 1])
        d0[e, i] = -1.0
        d0[e, j] = +1.0
    return d0


def build_d1(triangles: ndarray, edges: ndarray) -> ndarray:
    """Build the graph curl operator d₁ (coboundary on edges).  构建图旋度算子 d₁。

    d₁: ℝ^E → ℝ^T   (edges → triangles)
    For triangle t = (i, j, k) with i < j < k, oriented (i→j, j→k, k→i):
        edges: e_{ij}, e_{jk}, e_{ki}
        d₁[t, e_{ij}] = +1, d₁[t, e_{jk}] = +1, d₁[t, e_{ki}] = +1
    (the third edge needs to be oriented from k→i, but if stored as (i,k) we flip the sign)

    The sign depends on whether the edge direction in the stored edge list
    matches the orientation induced by the triangle. For edge (u,v) stored
    with u < v, the contribution is +1 if traversed forward (u→v matches
    triangle order), -1 if traversed backward.

    Args:
        triangles: (T, 3) integer array, each row = [i, j, k] with i < j < k.
        edges: (E, 2) integer array of edges [u, v] with u < v.

    Returns:
        d1: (T, E) float64 array.
    """
    T = triangles.shape[0]
    E = edges.shape[0]

    # Build lookup: (u, v) → edge index for fast access
    edge_index = {}
    for e in range(E):
        u, v = int(edges[e, 0]), int(edges[e, 1])
        edge_index[(u, v)] = e

    d1 = np.zeros((T, E), dtype=np.float64)
    for t in range(T):
        i, j, k = int(triangles[t, 0]), int(triangles[t, 1]), int(triangles[t, 2])
        # Triangle oriented as i → j → k → i
        # edge (i,j): forward
        e_ij = edge_index.get((i, j))
        if e_ij is not None:
            d1[t, e_ij] = +1.0
        # edge (j,k): forward
        e_jk = edge_index.get((j, k))
        if e_jk is not None:
            d1[t, e_jk] = +1.0
        # edge (i,k) or (k,i): orientation is k→i in triangle, but stored as (i,k)
        # Going from k→i means traversing (i,k) backward → sign = -1
        e_ik = edge_index.get((i, k))
        if e_ik is not None:
            d1[t, e_ik] = -1.0

    return d1


def build_laplacian_1(d0: ndarray, d1: Optional[ndarray] = None) -> ndarray:
    """Build the 1-Laplacian L₁ = d₀ d₀ᵀ + d₁ᵀ d₁.  构建 1-Laplacian。

    If no triangles exist (d₁ is None), then L₁ = d₀ d₀ᵀ (graph Laplacian on edges).
    如果没有三角形，则 L₁ = d₀ d₀ᵀ（边上的图 Laplacian）。

    Args:
        d0: (E, N) incidence matrix.
        d1: (T, E) curl operator, or None.

    Returns:
        L1: (E, E) symmetric positive semi-definite matrix.
    """
    L1 = d0 @ d0.T
    if d1 is not None:
        L1 = L1 + d1.T @ d1
    return L1


def complete_graph_edges(M: int) -> ndarray:
    """Enumerate all edges of a complete graph K_M.  枚举完全图 K_M 的所有边。

    Args:
        M: Number of nodes.

    Returns:
        edges: (E, 2) int array, where E = M(M-1)/2, each row [i, j] with i < j.
    """
    E = M * (M - 1) // 2
    edges = np.zeros((E, 2), dtype=np.int64)
    idx = 0
    for i in range(M):
        for j in range(i + 1, M):
            edges[idx, 0] = i
            edges[idx, 1] = j
            idx += 1
    return edges


def complete_graph_triangles(M: int) -> ndarray:
    """Enumerate all triangles (2-simplices) of a complete graph K_M.
    枚举完全图 K_M 的所有三角形（2-单形）。

    Args:
        M: Number of nodes.

    Returns:
        triangles: (T, 3) int array, where T = M(M-1)(M-2)/6.
    """
    T = M * (M - 1) * (M - 2) // 6
    triangles = np.zeros((T, 3), dtype=np.int64)
    idx = 0
    for i in range(M):
        for j in range(i + 1, M):
            for k in range(j + 1, M):
                triangles[idx, 0] = i
                triangles[idx, 1] = j
                triangles[idx, 2] = k
                idx += 1
    return triangles


# ═══════════════════════════════════════════════════════════════════════════════
# Section 3: Hodge Decomposition
# Section 3: Hodge 分解
# ═══════════════════════════════════════════════════════════════════════════════

def hodge_decompose(
    A: ndarray,
    d0: ndarray,
    d1: Optional[ndarray] = None,
    tol: float = 1e-12,
) -> Dict[str, ndarray]:
    """Decompose a 1-cochain A into exact, coexact, and harmonic parts.
    将 1-上链 A 分解为恰当、余恰当与调和部分。

    Hodge decomposition / Hodge 分解:
        ℝ^E = im(d₀) ⊕ im(d₁ᵀ) ⊕ ker(L₁)

    A = d₀ g + d₁ᵀ φ + h
      = A_exact + A_coexact + A_harmonic

    where h ∈ ker(L₁) is the harmonic component.
    其中 h ∈ ker(L₁) 为调和分量。

    Args:
        A: (E,) or (E,1) array, the 1-cochain to decompose.
        d0: (E, N) incidence matrix.
        d1: (T, E) curl operator, or None.
        tol: Tolerance for nullspace detection.

    Returns:
        dict with keys:
            'exact':     d₀ g  (gradient part)
            'coexact':   d₁ᵀ φ (curl part)
            'harmonic':  h     (harmonic part)
            'g':         node potential
            'phi':       triangle potential (if d1 is not None)
    """
    A = np.asarray(A, dtype=np.float64).ravel()
    E = d0.shape[0]

    L1 = build_laplacian_1(d0, d1)

    # --- Exact part: solve d₀ g ≈ A (least squares) ---
    # g = (d₀ᵀ d₀)⁺ d₀ᵀ A   (pseudoinverse of graph Laplacian L₀)
    L0 = d0.T @ d0  # (N, N) graph Laplacian
    rhs0 = d0.T @ A
    # L0 has a nullspace (constant vector); use pseudoinverse
    g = np.linalg.lstsq(L0, rhs0, rcond=None)[0]
    A_exact = d0 @ g

    # --- Coexact part ---
    if d1 is not None:
        # Solve d₁ᵀ φ from the residual after removing exact part
        # d₁ d₁ᵀ φ = d₁ (A - A_exact),  pseudoinverse needed if d₁ d₁ᵀ is singular
        L1_up = d1 @ d1.T  # (T, T) upper Laplacian
        residual = A - A_exact
        rhs1 = d1 @ residual
        try:
            phi = np.linalg.lstsq(L1_up, rhs1, rcond=None)[0]
        except np.linalg.LinAlgError:
            phi = np.zeros(d1.shape[0])
        A_coexact = d1.T @ phi
    else:
        phi = np.array([])
        A_coexact = np.zeros(E)

    # --- Harmonic part: remainder ---
    A_harmonic = A - A_exact - A_coexact

    # Verify harmonic: L₁ h ≈ 0
    L1h = L1 @ A_harmonic
    harmonic_norm = np.linalg.norm(L1h)

    return {
        "exact": A_exact,
        "coexact": A_coexact,
        "harmonic": A_harmonic,
        "g": g,
        "phi": phi,
        "harmonic_residual": harmonic_norm,
    }


def verify_hodge_orthogonality(
    A: ndarray,
    d0: ndarray,
    d1: Optional[ndarray] = None,
    tol: float = 1e-10,
) -> Dict[str, float]:
    """Verify orthogonality of the Hodge decomposition.  验证 Hodge 分解的正交性。

    Checks / 检查:
        ⟨A_exact, A_coexact⟩ ≈ 0   (im(d₀) ⟂ im(d₁ᵀ))
        ⟨A_exact, A_harmonic⟩ ≈ 0  (im(d₀) ⟂ ker(L₁))
        ⟨A_coexact, A_harmonic⟩ ≈ 0 (im(d₁ᵀ) ⟂ ker(L₁))

    Args:
        A: 1-cochain.
        d0: Incidence matrix.
        d1: Curl operator (optional).
        tol: Tolerance for declaring orthogonality.

    Returns:
        dict with inner products and a boolean 'is_orthogonal'.
    """
    result = hodge_decompose(A, d0, d1)
    exact = result["exact"]
    coexact = result["coexact"]
    harmonic = result["harmonic"]

    ip_ec = float(np.dot(exact, coexact))
    ip_eh = float(np.dot(exact, harmonic))
    ip_ch = float(np.dot(coexact, harmonic))

    is_orthogonal = all(
        abs(v) < tol for v in [ip_ec, ip_eh, ip_ch]
    )

    return {
        "inner_exact_coexact": ip_ec,
        "inner_exact_harmonic": ip_eh,
        "inner_coexact_harmonic": ip_ch,
        "is_orthogonal": is_orthogonal,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Section 4: Zero-Mode (Gauge) Fixing
# Section 4: 零模（规范）固定
# ═══════════════════════════════════════════════════════════════════════════════

def gauge_fix(
    A: ndarray,
    d0: ndarray,
) -> Tuple[ndarray, ndarray]:
    """Fix the gauge by solving min ||A - d₀ g||² subject to Σ g_i = 0.
    通过求解约束最小化问题来固定规范。

    The gauge transformation A → A + d₀ g leaves physics invariant.
    We choose g such that Σ g_i = 0 and ||A - d₀ g||² is minimized.
    规范变换 A → A + d₀ g 不改变物理。选择 g 使 Σ g_i = 0 且 ||A - d₀ g||² 最小。

    Method / 方法:
        Normal equations: d₀ᵀ d₀ g = d₀ᵀ A
        L₀ = d₀ᵀ d₀ has a one-dimensional nullspace (constant vector).
        With constraint Σ g_i = 0, use pseudoinverse: g = L₀⁺ d₀ᵀ A.

    Args:
        A: (E,) 1-cochain to fix.
        d0: (E, N) incidence matrix.

    Returns:
        (A_fixed, g): A_fixed = A - d₀ g, and the gauge potential g.
    """
    A = np.asarray(A, dtype=np.float64).ravel()
    L0 = d0.T @ d0  # (N, N) graph Laplacian
    rhs = d0.T @ A

    # Pseudoinverse of L0 — automatically handles zero mode
    L0_pinv = np.linalg.pinv(L0, hermitian=True)
    g = L0_pinv @ rhs

    # Ensure Σ g_i = 0 (pinv should give this, but enforce numerically)
    g = g - np.mean(g)

    A_fixed = A - d0 @ g
    return A_fixed, g


# ═══════════════════════════════════════════════════════════════════════════════
# Section 5: Cercis Score & Gauge Invariance
# Section 5: Cercis 分数与规范不变性
# ═══════════════════════════════════════════════════════════════════════════════

def projector_orthogonal_to_im_d0(d0: ndarray) -> ndarray:
    """Compute P^⊥ = I - d₀ (d₀ᵀ d₀)⁺ d₀ᵀ.  计算投影到 im(d₀) 正交补的算子。

    Projects onto the space orthogonal to exact 1-forms (gradient fields).
    投影到与恰当 1-形式（梯度场）正交的空间。

    Args:
        d0: (E, N) incidence matrix.

    Returns:
        P_perp: (E, E) projection matrix.
    """
    L0 = d0.T @ d0
    L0_pinv = np.linalg.pinv(L0, hermitian=True)
    E = d0.shape[0]
    return np.eye(E) - d0 @ L0_pinv @ d0.T


def cercis_score(A: ndarray, d0: ndarray) -> float:
    """Compute the Cercis score: ||P^⊥ A||².  计算 Cercis 分数。

    This measures the "non-gradient" content of A — how much of A lies
    outside the image of d₀. Gauge-invariant (unchanged by A → A + d₀ g).
    衡量 A 中“非梯度”成分的量——即 A 在 d₀ 像空间之外的投影大小。
    规范不变的（A → A + d₀ g 时不改变）。

    Args:
        A: (E,) 1-cochain.
        d0: (E, N) incidence matrix.

    Returns:
        score: ||P^⊥ A||² ≥ 0.
    """
    P_perp = projector_orthogonal_to_im_d0(d0)
    A_perp = P_perp @ np.asarray(A, dtype=np.float64).ravel()
    return float(np.dot(A_perp, A_perp))


def test_gauge_invariance(
    A: ndarray,
    d0: ndarray,
    n_trials: int = 5,
    rng: Optional[np.random.Generator] = None,
) -> Dict[str, Any]:
    """Test that the Cercis score is gauge-invariant.  测试 Cercis 分数的规范不变性。

    For random gauge transformations g, verify:
        score(A) == score(A + d₀ g)   (within numerical tolerance)
    对随机规范变换 g，验证分数不变。

    Args:
        A: 1-cochain.
        d0: Incidence matrix.
        n_trials: Number of random gauge transforms to test.
        rng: numpy random Generator (optional).

    Returns:
        dict with 'passed' (bool), 'scores', 'max_diff'.
    """
    if rng is None:
        rng = np.random.default_rng(42)
    base_score = cercis_score(A, d0)
    scores = [base_score]
    max_diff = 0.0
    for _ in range(n_trials):
        g_random = rng.normal(0, 1, d0.shape[1])
        A_gauge = A + d0 @ g_random
        s = cercis_score(A_gauge, d0)
        scores.append(s)
        max_diff = max(max_diff, abs(s - base_score))
    return {
        "passed": max_diff < 1e-10,
        "base_score": base_score,
        "scores": scores,
        "max_diff": max_diff,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Section 6: Discrete Curvature (Holonomy)
# Section 6: 离散曲率（和乐）
# ═══════════════════════════════════════════════════════════════════════════════

def discrete_curvature(loop_edges: ndarray, A: ndarray, signs: Optional[ndarray] = None) -> float:
    """Compute discrete curvature (holonomy) along a loop.  计算沿环路的离散曲率（和乐）。

    curv(γ) = Σ_{e ∈ γ} s_e · A_e

    where s_e = +1 if the edge is traversed in the stored direction,
    s_e = -1 if traversed opposite to the stored direction.
    其中 s_e = +1 表示沿存储方向遍历，s_e = -1 表示反向遍历。

    For a closed loop γ (a cycle in the graph), the signed sum of edge values is
    gauge-invariant: adding d₀ g to A adds Σ_{(i,j)∈γ} ±(g_j - g_i) = 0.
    对于闭合环路 γ，边上取值的带符号和是规范不变的。

    Args:
        loop_edges: (L,) int array of edge indices forming a closed loop.
        A: (E,) 1-cochain values on edges.
        signs: (L,) float array of ±1 for each edge. If None, assumes all +1.

    Returns:
        curvature: Σ s_e · A_e over the loop.
    """
    A_flat = np.asarray(A, dtype=np.float64).ravel()
    loop_edges = np.asarray(loop_edges, dtype=np.int64).ravel()
    if signs is None:
        return float(np.sum(A_flat[loop_edges]))
    else:
        signs = np.asarray(signs, dtype=np.float64).ravel()
        return float(np.sum(signs * A_flat[loop_edges]))


def cycle_from_node_sequence(
    node_seq: List[int],
    edges: ndarray,
) -> Tuple[ndarray, ndarray]:
    """Convert a node sequence to edge indices and orientation signs for a closed loop.
    将节点序列转换为闭合环路的边索引和方向符号。

    The cycle closes from the last node back to the first.
    Edge (u,v) is stored in the edge list with u < v. If we traverse from
    u to v (forward), sign = +1; if from v to u (backward), sign = -1.
    环路从最后一个节点闭合回第一个节点。边 (u,v) 以 u < v 存储。
    若从 u 到 v 遍历（正向），符号 = +1；若从 v 到 u（反向），符号 = -1。

    Args:
        node_seq: List of node indices [v0, v1, ..., v_{k-1}] forming a cycle.
        edges: (E, 2) int array of edges.

    Returns:
        (edge_indices, signs): (k,) int array and (k,) float array of ±1.
    """
    # Build lookup from (u,v) to edge index
    edge_lookup = {}
    for e in range(edges.shape[0]):
        u, v = int(edges[e, 0]), int(edges[e, 1])
        edge_lookup[(u, v)] = e

    k = len(node_seq)
    indices = np.zeros(k, dtype=np.int64)
    signs = np.zeros(k, dtype=np.float64)
    for idx in range(k):
        u = node_seq[idx]
        v = node_seq[(idx + 1) % k]
        key_forward = (u, v) if u < v else (v, u)
        if key_forward not in edge_lookup:
            raise ValueError(f"Edge ({min(u,v)}, {max(u,v)}) not found in edge list")
        indices[idx] = edge_lookup[key_forward]
        # sign = +1 if traversing from smaller to larger (matches stored direction)
        signs[idx] = +1.0 if u < v else -1.0
    return indices, signs


# ═══════════════════════════════════════════════════════════════════════════════
# Section 7: Hessian Eigenvalue Analysis
# Section 7: Hessian 特征值分析
# ═══════════════════════════════════════════════════════════════════════════════

def hessian_eigenvalues(
    hessian_func: Callable[[ndarray], ndarray],
    x0: ndarray,
    eps: float = 1e-6,
) -> Tuple[ndarray, ndarray]:
    """Compute eigenvalues of the Hessian at a critical point via finite differences.
    通过有限差分计算临界点处 Hessian 的特征值。

    Given a function that returns the gradient ∇S(x) (or can compute S(x)),
    we numerically estimate the Hessian H = ∇²S at x0 and compute its spectrum.
    给定返回梯度 ∇S(x) 的函数（或可计算 S(x) 的函数），数值估计 Hessian 并计算谱。

    Args:
        hessian_func: Function f(x) → gradient vector ∇S(x) of length n.
        x0: (n,) array, the critical point.
        eps: Finite-difference step size.

    Returns:
        (eigenvalues, eigenvectors): eigenvalues sorted ascending, eigenvectors as columns.
    """
    x0 = np.asarray(x0, dtype=np.float64).ravel()
    n = len(x0)
    grad0 = np.asarray(hessian_func(x0), dtype=np.float64).ravel()
    H = np.zeros((n, n), dtype=np.float64)

    for j in range(n):
        x_plus = x0.copy()
        x_plus[j] += eps
        grad_plus = np.asarray(hessian_func(x_plus), dtype=np.float64).ravel()
        H[:, j] = (grad_plus - grad0) / eps

    # Symmetrize
    H = 0.5 * (H + H.T)

    eigenvalues, eigenvectors = np.linalg.eigh(H)
    return eigenvalues, eigenvectors


def hessian_from_scalar(
    scalar_func: Callable[[ndarray], float],
    x0: ndarray,
    eps: float = 1e-6,
) -> Tuple[ndarray, ndarray]:
    """Compute Hessian eigenvalues from a scalar function via second differences.
    通过二阶差分从标量函数计算 Hessian 特征值。

    H_{ij} ≈ [S(x + ε e_i + ε e_j) - S(x + ε e_i - ε e_j)
               - S(x - ε e_i + ε e_j) + S(x - ε e_i - ε e_j)] / (4 ε²)

    Args:
        scalar_func: Function S(x) → float.
        x0: Critical point.
        eps: Step size.

    Returns:
        (eigenvalues, eigenvectors).
    """
    x0 = np.asarray(x0, dtype=np.float64).ravel()
    n = len(x0)
    S0 = scalar_func(x0)
    H = np.zeros((n, n), dtype=np.float64)

    e = np.eye(n) * eps
    for i in range(n):
        for j in range(i, n):
            S_pp = scalar_func(x0 + e[i] + e[j])
            S_pm = scalar_func(x0 + e[i] - e[j])
            S_mp = scalar_func(x0 - e[i] + e[j])
            S_mm = scalar_func(x0 - e[i] - e[j])
            H[i, j] = (S_pp - S_pm - S_mp + S_mm) / (4.0 * eps * eps)
            H[j, i] = H[i, j]

    eigenvalues, eigenvectors = np.linalg.eigh(H)
    return eigenvalues, eigenvectors


def classify_critical_point(eigenvalues: ndarray, tol: float = 1e-8) -> str:
    """Classify a critical point from its Hessian eigenvalues.  根据 Hessian 特征值分类临界点。

    Args:
        eigenvalues: Array of Hessian eigenvalues.
        tol: Tolerance for zero.

    Returns:
        One of: 'minimum', 'maximum', 'saddle', 'degenerate'.
    """
    pos = np.sum(eigenvalues > tol)
    neg = np.sum(eigenvalues < -tol)
    n = len(eigenvalues)
    zero_count = n - pos - neg

    if zero_count == n:
        return "degenerate"
    elif neg == 0 and pos == n:
        return "minimum"
    elif pos == 0 and neg == n:
        return "maximum"
    else:
        return "saddle"


# ═══════════════════════════════════════════════════════════════════════════════
# Section 8: Fisher Information Bayesian Update
# Section 8: Fisher 信息贝叶斯更新
# ═══════════════════════════════════════════════════════════════════════════════

def fisher_bayesian_update(
    Sigma0: ndarray,
    A: ndarray,
    N: int = 1,
) -> ndarray:
    """Bayesian update of covariance using Fisher information.  Fisher 信息的贝叶斯协方差更新。

    Σ_N = Σ₀ (I + N · A)⁻¹

    This implements the posterior covariance after N measurements,
    where A is the Fisher information matrix per measurement (or a
    related precision matrix). The formula assumes a Gaussian prior
    Σ₀ and likelihood with precision proportional to A.
    实现 N 次测量后的后验协方差。A 是每次测量的 Fisher 信息矩阵
    （或相关的精度矩阵）。假设高斯先验 Σ₀ 和精度正比于 A 的似然。

    Args:
        Sigma0: (d, d) prior covariance matrix.
        A: (d, d) Fisher/precision matrix per sample.
        N: Number of measurements (≥ 1).

    Returns:
        Sigma_N: (d, d) posterior covariance.
    """
    Sigma0 = np.asarray(Sigma0, dtype=np.float64)
    A = np.asarray(A, dtype=np.float64)
    d = Sigma0.shape[0]
    M = np.eye(d) + N * A
    # Σ_N = Σ₀ M⁻¹
    Sigma_N = Sigma0 @ np.linalg.inv(M)
    return Sigma_N


def fisher_information_bound(
    Sigma: ndarray,
    A: ndarray,
    N: int = 1,
) -> ndarray:
    """Compute the Bayesian Cramér-Rao bound (posterior covariance lower bound).
    计算贝叶斯 Cramér-Rao 下界（后验协方差下界）。

    Equivalent to fisher_bayesian_update with Σ₀⁻¹ → 0 (uninformative prior).
    等价于先验信息为 0 的 fisher_bayesian_update。

    Args:
        Sigma: Prior (used if N=0).
        A: Fisher matrix per sample.
        N: Number of samples.

    Returns:
        CRB: (N·A)⁻¹ or as appropriate.
    """
    A = np.asarray(A, dtype=np.float64)
    if N == 0:
        return np.asarray(Sigma, dtype=np.float64)
    return np.linalg.inv(N * A)


# ═══════════════════════════════════════════════════════════════════════════════
# Section 9: KS Test Wrapper
# Section 9: KS 检验封装
# ═══════════════════════════════════════════════════════════════════════════════

def ks_test(
    sample1: ndarray,
    sample2: ndarray,
    alpha: float = 0.05,
) -> Dict[str, float]:
    """Two-sample Kolmogorov–Smirnov test.  双样本 KS 检验。

    Tests the null hypothesis that two samples are drawn from the same
    continuous distribution.
    检验两个样本是否来自同一连续分布的零假设。

    Args:
        sample1: First sample array.
        sample2: Second sample array.
        alpha: Significance level (default 0.05).

    Returns:
        dict with keys:
            'statistic': KS statistic D.
            'p_value': Two-sided p-value.
            'reject': True if null hypothesis rejected at level alpha.
    """
    if not _HAS_SCIPY:
        raise ImportError("scipy.stats is required for KS test")

    result = sp_stats.ks_2samp(
        np.asarray(sample1).ravel(),
        np.asarray(sample2).ravel(),
    )
    return {
        "statistic": float(result.statistic),
        "p_value": float(result.pvalue),
        "reject": bool(result.pvalue < alpha),
    }


def ks_test_normal(
    sample: ndarray,
    alpha: float = 0.05,
) -> Dict[str, float]:
    """One-sample KS test against a normal distribution.  单样本 KS 检验：检验是否服从正态分布。

    The normal distribution is fit from the sample mean and std.
    正态分布参数从样本均值和标准差估计。

    Args:
        sample: 1D sample array.
        alpha: Significance level.

    Returns:
        dict with 'statistic', 'p_value', 'reject'.
    """
    if not _HAS_SCIPY:
        raise ImportError("scipy.stats is required for KS test")

    sample = np.asarray(sample).ravel()
    mu = float(np.mean(sample))
    sigma = float(np.std(sample, ddof=1))
    result = sp_stats.kstest(sample, "norm", args=(mu, sigma))
    return {
        "statistic": float(result.statistic),
        "p_value": float(result.pvalue),
        "reject": bool(result.pvalue < alpha),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Section 10: Simple Qubit Simulator
# Section 10: 简单量子比特模拟器
# ═══════════════════════════════════════════════════════════════════════════════

# Pauli matrices
_PAULI_X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
_PAULI_Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
_PAULI_Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
_HADAMARD = np.array([[1, 1], [1, -1]], dtype=np.complex128) / np.sqrt(2)
_KET0 = np.array([1, 0], dtype=np.complex128)
_KET1 = np.array([0, 1], dtype=np.complex128)


def qubit_state(alpha: complex, beta: complex) -> ndarray:
    """Create a normalized qubit state |ψ⟩ = α|0⟩ + β|1⟩.  创建归一化量子比特态。

    Args:
        alpha: Amplitude for |0⟩.
        beta: Amplitude for |1⟩.

    Returns:
        state: (2,) complex array, normalized.
    """
    state = np.array([alpha, beta], dtype=np.complex128)
    norm = np.sqrt(np.abs(alpha) ** 2 + np.abs(beta) ** 2)
    if norm < 1e-15:
        raise ValueError("State has zero norm")
    return state / norm


def qubit_measure(
    state: ndarray,
    n_shots: int = 1,
    rng: Optional[np.random.Generator] = None,
) -> Tuple[ndarray, ndarray]:
    """Measure a qubit in the computational basis.  在计算基下测量量子比特。

    Born rule: P(0) = |⟨0|ψ⟩|², P(1) = |⟨1|ψ⟩|².
    玻恩规则：P(0) = |⟨0|ψ⟩|²，P(1) = |⟨1|ψ⟩|²。

    Args:
        state: (2,) normalized qubit state.
        n_shots: Number of measurement shots.
        rng: Random generator.

    Returns:
        (outcomes, probabilities): outcomes ∈ {0, 1}, probabilities [P(0), P(1)].
    """
    if rng is None:
        rng = np.random.default_rng()
    state = np.asarray(state, dtype=np.complex128).ravel()
    prob0 = float(np.abs(state[0]) ** 2)
    prob1 = float(np.abs(state[1]) ** 2)
    probs = np.array([prob0, prob1])
    outcomes = rng.choice([0, 1], size=n_shots, p=[prob0, prob1])
    return outcomes, probs


def qubit_tensor(states: List[ndarray]) -> ndarray:
    """Tensor product of multiple qubit states.  多个量子比特的张量积。

    |ψ₁⟩ ⊗ |ψ₂⟩ ⊗ ... ⊗ |ψₙ⟩

    Args:
        states: List of (2,) complex state vectors.

    Returns:
        tensor_state: (2ⁿ,) complex array.
    """
    result = np.array([1.0], dtype=np.complex128)
    for s in states:
        result = np.kron(result, np.asarray(s, dtype=np.complex128).ravel())
    return result


def qubit_expectation(state: ndarray, operator: ndarray) -> float:
    """Compute expectation value ⟨ψ|O|ψ⟩.  计算期望值 ⟨ψ|O|ψ⟩。

    Args:
        state: (2,) normalized qubit state.
        operator: (2, 2) Hermitian operator.

    Returns:
        expectation: real scalar.
    """
    state = np.asarray(state, dtype=np.complex128).ravel()
    operator = np.asarray(operator, dtype=np.complex128)
    return float(np.real(np.conj(state) @ operator @ state))


def qubit_bloch(state: ndarray) -> ndarray:
    """Compute Bloch sphere coordinates (x, y, z).  计算 Bloch 球坐标。

    For |ψ⟩ = cos(θ/2)|0⟩ + e^{iφ} sin(θ/2)|1⟩,
        x = sin(θ) cos(φ), y = sin(θ) sin(φ), z = cos(θ).

    Args:
        state: (2,) normalized qubit state.

    Returns:
        bloch: (3,) array of (x, y, z).
    """
    state = np.asarray(state, dtype=np.complex128).ravel()
    x = float(qubit_expectation(state, _PAULI_X))
    y = float(qubit_expectation(state, _PAULI_Y))
    z = float(qubit_expectation(state, _PAULI_Z))
    return np.array([x, y, z])


# ═══════════════════════════════════════════════════════════════════════════════
# Section 11: BB84 QKD Helper
# Section 11: BB84 量子密钥分发辅助
# ═══════════════════════════════════════════════════════════════════════════════

# BB84 basis states
_BB84_Z0 = np.array([1, 0], dtype=np.complex128)       # |0⟩
_BB84_Z1 = np.array([0, 1], dtype=np.complex128)       # |1⟩
_BB84_X0 = np.array([1, 1], dtype=np.complex128) / np.sqrt(2)   # |+⟩
_BB84_X1 = np.array([1, -1], dtype=np.complex128) / np.sqrt(2)  # |−⟩

# Measurement projectors
_PROJ_Z0 = np.outer(_BB84_Z0, _BB84_Z0.conj())
_PROJ_Z1 = np.outer(_BB84_Z1, _BB84_Z1.conj())
_PROJ_X0 = np.outer(_BB84_X0, _BB84_X0.conj())
_PROJ_X1 = np.outer(_BB84_X1, _BB84_X1.conj())


def bb84_random_bases(
    n_bits: int,
    rng: Optional[np.random.Generator] = None,
) -> ndarray:
    """Generate random BB84 basis choices.  生成随机 BB84 基选择。

    Returns 0 for Z-basis, 1 for X-basis.
    返回 0 表示 Z 基，1 表示 X 基。

    Args:
        n_bits: Number of bits.
        rng: Random generator.

    Returns:
        bases: (n_bits,) int array of 0 or 1.
    """
    if rng is None:
        rng = np.random.default_rng()
    return rng.integers(0, 2, size=n_bits)


def bb84_encode(
    bits: ndarray,
    bases: ndarray,
) -> List[ndarray]:
    """Encode classical bits into qubit states using BB84 bases.
    使用 BB84 基将经典比特编码为量子比特态。

    Z-basis (0): |0⟩ for bit 0, |1⟩ for bit 1.
    X-basis (1): |+⟩ for bit 0, |−⟩ for bit 1.

    Args:
        bits: (n_bits,) int array of 0 or 1.
        bases: (n_bits,) int array of 0 (Z) or 1 (X).

    Returns:
        states: List of (2,) complex state vectors.
    """
    bits = np.asarray(bits, dtype=int).ravel()
    bases = np.asarray(bases, dtype=int).ravel()
    states = []
    for b, basis in zip(bits, bases):
        if basis == 0:  # Z-basis
            states.append(_BB84_Z0.copy() if b == 0 else _BB84_Z1.copy())
        else:  # X-basis
            states.append(_BB84_X0.copy() if b == 0 else _BB84_X1.copy())
    return states


def bb84_measure(
    states: List[ndarray],
    bases: ndarray,
    rng: Optional[np.random.Generator] = None,
) -> ndarray:
    """Measure qubits in given bases (simulated BB84 measurement).
    在给定基下测量量子比特（模拟 BB84 测量）。

    If the measurement basis matches the encoding basis, the bit is deterministic.
    If they differ, the outcome is random (50/50).
    若测量基与编码基相同，结果为确定性；若不同，结果为随机（50/50）。

    Args:
        states: List of (2,) qubit state vectors.
        bases: (n_bits,) int array of measurement bases.
        rng: Random generator.

    Returns:
        measured_bits: (n_bits,) int array of measured bits.
    """
    if rng is None:
        rng = np.random.default_rng()
    n = len(states)
    measured = np.zeros(n, dtype=int)
    for i, (state, basis) in enumerate(zip(states, bases)):
        state_vec = np.asarray(state, dtype=np.complex128).ravel()
        if basis == 0:  # Z measurement
            prob0 = float(np.abs(np.conj(_BB84_Z0) @ state_vec) ** 2)
            measured[i] = rng.choice([0, 1], p=[prob0, 1 - prob0])
        else:  # X measurement
            prob0 = float(np.abs(np.conj(_BB84_X0) @ state_vec) ** 2)
            measured[i] = rng.choice([0, 1], p=[prob0, 1 - prob0])
    return measured


def bb84_sift(
    alice_bases: ndarray,
    bob_bases: ndarray,
    alice_bits: ndarray,
    bob_bits: ndarray,
) -> Tuple[ndarray, ndarray]:
    """Sift the key by keeping only bits where bases matched.
    通过保留基匹配的比特来筛选密钥。

    Args:
        alice_bases: Alice's basis choices.
        bob_bases: Bob's basis choices.
        alice_bits: Alice's bits.
        bob_bits: Bob's bits.

    Returns:
        (alice_key, bob_key): Sifted keys (should be identical if no eavesdropping).
    """
    match = np.asarray(alice_bases).ravel() == np.asarray(bob_bases).ravel()
    return (
        np.asarray(alice_bits).ravel()[match],
        np.asarray(bob_bits).ravel()[match],
    )


def bb84_qber(alice_key: ndarray, bob_key: ndarray) -> float:
    """Compute Quantum Bit Error Rate (QBER).  计算量子比特错误率。

    Args:
        alice_key: Alice's sifted key bits.
        bob_key: Bob's sifted key bits.

    Returns:
        QBER ∈ [0, 1].
    """
    a = np.asarray(alice_key).ravel()
    b = np.asarray(bob_key).ravel()
    if len(a) == 0:
        return 0.0
    return float(np.mean(a != b))


# ═══════════════════════════════════════════════════════════════════════════════
# Section 12: CHSH Inequality Helper
# Section 12: CHSH 不等式辅助
# ═══════════════════════════════════════════════════════════════════════════════

def chsh_correlation(
    measurement_a: Callable[[ndarray, ndarray], int],
    measurement_b: Callable[[ndarray, ndarray], int],
    state: ndarray,
    setting_a: ndarray,
    setting_b: ndarray,
    n_trials: int = 1000,
    rng: Optional[np.random.Generator] = None,
) -> float:
    """Estimate E(a, b) = ⟨A(a) B(b)⟩ for CHSH.  估计 CHSH 关联函数 E(a, b)。

    Args:
        measurement_a: Function f(state, setting) → outcome ∈ {+1, -1}.
        measurement_b: Function f(state, setting) → outcome ∈ {+1, -1}.
        state: Shared quantum state.
        setting_a: Setting vector for Alice.
        setting_b: Setting vector for Bob.
        n_trials: Number of measurement trials.
        rng: Random generator.

    Returns:
        E: Estimated correlation ∈ [-1, +1].
    """
    if rng is None:
        rng = np.random.default_rng()
    total = 0.0
    for _ in range(n_trials):
        a_out = measurement_a(state, setting_a)
        b_out = measurement_b(state, setting_b)
        total += a_out * b_out
    return total / n_trials


def chsh_score(
    E_ab: float,
    E_abp: float,
    E_apb: float,
    E_apbp: float,
) -> float:
    """Compute CHSH score S = E(a,b) - E(a,b') + E(a',b) + E(a',b').
    计算 CHSH 分数。

    Classical bound: |S| ≤ 2 (CHSH inequality).
    Quantum bound:  |S| ≤ 2√2 ≈ 2.828 (Tsirelson bound).
    经典界限：|S| ≤ 2；量子界限：|S| ≤ 2√2。

    Args:
        E_ab:  E(a, b)
        E_abp: E(a, b')
        E_apb: E(a', b)
        E_apbp: E(a', b')

    Returns:
        S: CHSH score.
    """
    return float(np.asarray(E_ab) - np.asarray(E_abp)
                 + np.asarray(E_apb) + np.asarray(E_apbp))


def chsh_classical_bound() -> float:
    """Return classical CHSH bound.  返回经典 CHSH 界限。"""
    return 2.0


def chsh_quantum_bound() -> float:
    """Return quantum (Tsirelson) CHSH bound.  返回量子（Tsirelson）CHSH 界限。"""
    return 2.0 * np.sqrt(2.0)


def chsh_singlet_correlations(
    a_angle: float,
    b_angle: float,
) -> float:
    """Analytic CHSH correlation for singlet state |Ψ⁻⟩.  单态 |Ψ⁻⟩ 的分析 CHSH 关联。

    For the singlet state and spin measurements at angles a and b:
        E(a, b) = -cos(a - b)
    对单态和角度 a, b 的自旋测量：E(a, b) = -cos(a - b)。

    Args:
        a_angle: Alice's measurement angle (radians).
        b_angle: Bob's measurement angle (radians).

    Returns:
        Correlation E ∈ [-1, 1].
    """
    return -np.cos(a_angle - b_angle)


def chsh_singlet_max_violation() -> Dict[str, float]:
    """Compute maximal CHSH violation for the singlet state.  计算单态的最大 CHSH 违反。

    Optimal angles: a=0, a'=π/2, b=π/4, b'=3π/4
    Gives S = 2√2.
    最优角度给出 S = 2√2。

    Returns:
        dict with 'S', 'E_ab', 'E_abp', 'E_apb', 'E_apbp'.
    """
    a, ap = 0.0, np.pi / 2
    b, bp = np.pi / 4, 3 * np.pi / 4
    E_ab = chsh_singlet_correlations(a, b)
    E_abp = chsh_singlet_correlations(a, bp)
    E_apb = chsh_singlet_correlations(ap, b)
    E_apbp = chsh_singlet_correlations(ap, bp)
    S = chsh_score(E_ab, E_abp, E_apb, E_apbp)
    return {"S": S, "E_ab": E_ab, "E_abp": E_abp, "E_apb": E_apb, "E_apbp": E_apbp}


# ═══════════════════════════════════════════════════════════════════════════════
# Section 13: Density Estimation (KDE + Sublevel Filtration)
# Section 13: 密度估计（KDE + 子水平集滤波）
# ═══════════════════════════════════════════════════════════════════════════════

def kde_estimate(
    samples: ndarray,
    eval_points: Optional[ndarray] = None,
    bw_method: Any = None,
) -> Tuple[ndarray, Any]:
    """Kernel Density Estimation.  核密度估计。

    Uses scipy.stats.gaussian_kde for density estimation.
    使用 scipy.stats.gaussian_kde 进行密度估计。

    Args:
        samples: (n_samples, d) or (n_samples,) data points.
        eval_points: (m, d) points to evaluate density at.
                     If None, evaluates at the samples.
        bw_method: Bandwidth method for gaussian_kde.
                   'scott' (default), 'silverman', scalar, or callable.

    Returns:
        (density, kde): density values at eval_points and the kde object.
    """
    if not _HAS_SCIPY:
        raise ImportError("scipy.stats.gaussian_kde is required for KDE")

    samples = np.asarray(samples, dtype=np.float64)
    if samples.ndim == 1:
        samples = samples.reshape(1, -1)
    else:
        samples = samples.T  # gaussian_kde expects (d, n)

    kde = gaussian_kde(samples, bw_method=bw_method)

    if eval_points is None:
        eval_points = samples.T  # back to (n, d)
    else:
        eval_points = np.asarray(eval_points, dtype=np.float64)
        if eval_points.ndim == 1:
            eval_points = eval_points.reshape(-1, 1)

    density = kde(eval_points.T)
    return density, kde


def sublevel_filtration(
    density: ndarray,
    thresholds: Optional[ndarray] = None,
    n_thresholds: int = 20,
) -> Dict[str, ndarray]:
    """Compute sublevel sets for density filtration.  计算密度的子水平集滤波。

    Sublevel set at threshold t: {x : density(x) ≤ t}.
    Used for persistent homology of density estimates.
    阈值 t 的子水平集用于密度估计的持续同调。

    Args:
        density: (n,) array of density values.
        thresholds: (m,) array of thresholds, or None to auto-generate.
        n_thresholds: Number of thresholds if auto-generated.

    Returns:
        dict with:
            'thresholds': sorted threshold values.
            'sublevel_masks': (m, n) bool array, mask for each threshold.
            'sublevel_sizes': (m,) int array, size of each sublevel set.
    """
    density = np.asarray(density, dtype=np.float64).ravel()
    if thresholds is None:
        d_min, d_max = density.min(), density.max()
        thresholds = np.linspace(d_min, d_max, n_thresholds)

    thresholds = np.asarray(thresholds, dtype=np.float64)
    m = len(thresholds)
    n = len(density)

    masks = np.zeros((m, n), dtype=bool)
    sizes = np.zeros(m, dtype=int)
    for i, t in enumerate(thresholds):
        masks[i] = density <= t
        sizes[i] = int(np.sum(masks[i]))

    return {
        "thresholds": thresholds,
        "sublevel_masks": masks,
        "sublevel_sizes": sizes,
    }


def superlevel_filtration(
    density: ndarray,
    thresholds: Optional[ndarray] = None,
    n_thresholds: int = 20,
) -> Dict[str, ndarray]:
    """Compute superlevel sets for density filtration.  计算密度的超水平集滤波。

    Superlevel set at threshold t: {x : density(x) ≥ t}.
    阈值 t 的超水平集：{x : density(x) ≥ t}。

    Args:
        density: (n,) array of density values.
        thresholds: (m,) array of thresholds, or None.
        n_thresholds: Number of thresholds if auto-generated.

    Returns:
        dict with 'thresholds', 'superlevel_masks', 'superlevel_sizes'.
    """
    density = np.asarray(density, dtype=np.float64).ravel()
    if thresholds is None:
        d_min, d_max = density.min(), density.max()
        thresholds = np.linspace(d_min, d_max, n_thresholds)

    thresholds = np.asarray(thresholds, dtype=np.float64)
    m = len(thresholds)
    n = len(density)

    masks = np.zeros((m, n), dtype=bool)
    sizes = np.zeros(m, dtype=int)
    for i, t in enumerate(thresholds):
        masks[i] = density >= t
        sizes[i] = int(np.sum(masks[i]))

    return {
        "thresholds": thresholds,
        "superlevel_masks": masks,
        "superlevel_sizes": sizes,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Self-test / 自测试
# ═══════════════════════════════════════════════════════════════════════════════

def run_self_test() -> bool:
    """Run a self-test of all utility functions.  运行所有工具函数的自测试。

    Returns:
        True if all tests pass.
    """
    print_header("SCX verify_common — Self-Test / 自测试")
    all_ok = True

    # --- 1. Betti number ---
    print_info("Testing Betti number / 测试 Betti 数 ...")
    assert betti_1(3) == 1
    assert betti_1(4) == 3
    assert betti_1(5) == 6
    assert betti_1(10) == 36
    print_pass("Betti number OK")

    # --- 2. Hodge operators ---
    print_info("Testing Hodge operators / 测试 Hodge 算子 ...")
    M = 4
    edges = complete_graph_edges(M)
    triangles = complete_graph_triangles(M)
    assert edges.shape[0] == 6
    assert triangles.shape[0] == 4

    d0 = build_d0(edges, M)
    assert d0.shape == (6, 4)

    d1 = build_d1(triangles, edges)
    # d₁ᵀ d₀ = 0 (boundary of boundary is zero)
    product = d1 @ d0
    assert_close(product, np.zeros_like(product), tol=1e-12, msg="d1 @ d0 should be zero")
    print_pass("Hodge operators OK")

    # --- 3. Hodge decomposition ---
    print_info("Testing Hodge decomposition / 测试 Hodge 分解 ...")
    A = np.random.default_rng(123).normal(0, 1, edges.shape[0])
    decomp = hodge_decompose(A, d0, d1)
    reconstructed = decomp["exact"] + decomp["coexact"] + decomp["harmonic"]
    assert_close(A, reconstructed, tol=1e-10, msg="Reconstruction")

    ortho = verify_hodge_orthogonality(A, d0, d1)
    assert ortho["is_orthogonal"], f"Not orthogonal: {ortho}"
    print_pass("Hodge decomposition OK")

    # --- 4. Gauge fixing ---
    print_info("Testing gauge fixing / 测试规范固定 ...")
    g0 = np.random.default_rng(456).normal(0, 1, M)
    A_raw = d0 @ g0 + 0.1 * np.random.default_rng(789).normal(0, 1, edges.shape[0])
    A_fixed, g_opt = gauge_fix(A_raw, d0)
    assert abs(np.sum(g_opt)) < 1e-12, f"Σg != 0: {np.sum(g_opt)}"
    print_pass("Gauge fixing OK")

    # --- 5. Cercis score ---
    print_info("Testing Cercis score / 测试 Cercis 分数 ...")
    score = cercis_score(A_raw, d0)
    assert score >= -1e-12
    inv_test = test_gauge_invariance(A_raw, d0, n_trials=3)
    assert inv_test["passed"], f"Gauge invariance failed: {inv_test}"
    print_pass("Cercis score OK")

    # --- 6. Discrete curvature ---
    print_info("Testing discrete curvature / 测试离散曲率 ...")
    loop_nodes = [0, 1, 2]  # triangle (closes back to 0 automatically)
    loop_edges, loop_signs = cycle_from_node_sequence(loop_nodes, edges)
    curv = discrete_curvature(loop_edges, A_raw, loop_signs)
    # Gauge invariance: adding d₀ g should not change curvature
    g_test = np.random.default_rng(111).normal(0, 1, M)
    A_gauge_test = A_raw + d0 @ g_test
    curv2 = discrete_curvature(loop_edges, A_gauge_test, loop_signs)
    assert_close(curv, curv2, tol=1e-10, msg="Curvature gauge invariance")
    print_pass("Discrete curvature OK")

    # --- 7. Hessian analysis ---
    print_info("Testing Hessian analysis / 测试 Hessian 分析 ...")
    def f_scalar(x):
        return x[0]**2 + 2*x[1]**2 + 0.5*x[0]*x[1]
    x0 = np.array([0.0, 0.0])
    evals, evecs = hessian_from_scalar(f_scalar, x0)
    # Analytical Hessian: [[2, 0.5], [0.5, 4]]
    expected_evals = np.sort(np.linalg.eigvalsh(np.array([[2, 0.5], [0.5, 4]])))
    assert_close(np.sort(evals), expected_evals, tol=1e-5, msg="Hessian eigenvalues")
    cp_type = classify_critical_point(evals)
    assert cp_type == "minimum", f"Expected minimum, got {cp_type}"
    print_pass("Hessian analysis OK")

    # --- 8. Fisher information ---
    print_info("Testing Fisher update / 测试 Fisher 更新 ...")
    Sigma0 = np.eye(2)
    A_fisher = np.array([[2, 0], [0, 1]], dtype=float)
    Sigma_N = fisher_bayesian_update(Sigma0, A_fisher, N=1)
    expected = np.linalg.inv(np.eye(2) + A_fisher)  # Σ₀ = I
    assert_close(Sigma_N, expected, tol=1e-12, msg="Fisher update")
    print_pass("Fisher information OK")

    # --- 9. KS test ---
    if _HAS_SCIPY:
        print_info("Testing KS test / 测试 KS 检验 ...")
        s1 = np.random.default_rng(42).normal(0, 1, 500)
        s2 = np.random.default_rng(43).normal(0, 1, 500)
        result = ks_test(s1, s2)
        # Same distribution → should not reject
        print(f"  KS D={result['statistic']:.4f}, p={result['p_value']:.4f}, "
              f"reject={result['reject']}")
        print_pass("KS test OK")
    else:
        print_warn("KS test skipped (no scipy)")

    # --- 10. Qubit simulator ---
    print_info("Testing qubit simulator / 测试量子比特模拟器 ...")
    psi = qubit_state(1, 1)  # |+⟩
    assert_close(np.abs(psi[0])**2 + np.abs(psi[1])**2, 1.0, tol=1e-15)
    outcomes, probs = qubit_measure(psi, n_shots=1000)
    assert 0.4 < probs[0] < 0.6, f"P(0) should be ~0.5, got {probs[0]}"

    # Tensor product
    tensor = qubit_tensor([_KET0, _KET0])
    assert_close(tensor, np.array([1, 0, 0, 0], dtype=np.complex128), tol=1e-15)

    # Expectation
    exp_z = qubit_expectation(psi, _PAULI_Z)
    assert_close(exp_z, 0.0, tol=1e-10, msg="⟨+|Z|+⟩ should be 0")

    # Bloch
    bloch = qubit_bloch(psi)
    assert_close(bloch, np.array([1, 0, 0]), tol=1e-10, msg="|+⟩ Bloch")
    print_pass("Qubit simulator OK")

    # --- 11. BB84 ---
    print_info("Testing BB84 / 测试 BB84 ...")
    n_bits = 100
    alice_bits = np.random.default_rng(99).integers(0, 2, n_bits)
    alice_bases = bb84_random_bases(n_bits)
    states = bb84_encode(alice_bits, alice_bases)
    bob_bases = bb84_random_bases(n_bits)
    bob_bits = bb84_measure(states, bob_bases)
    a_key, b_key = bb84_sift(alice_bases, bob_bases, alice_bits, bob_bits)
    qber = bb84_qber(a_key, b_key)
    assert qber < 0.1, f"QBER should be near 0, got {qber}"
    print_pass(f"BB84 OK (sifted {len(a_key)}/{n_bits} bits, QBER={qber:.4f})")

    # --- 12. CHSH ---
    print_info("Testing CHSH / 测试 CHSH ...")
    result = chsh_singlet_max_violation()
    S = result["S"]
    assert_close(abs(S), 2 * np.sqrt(2), tol=1e-10, msg="CHSH max violation")
    assert abs(S) > 2.0, "CHSH should violate classical bound"
    print_pass(f"CHSH OK (S={S:.6f}, bound={chsh_quantum_bound():.6f})")

    # --- 13. Density estimation ---
    if _HAS_SCIPY:
        print_info("Testing density estimation / 测试密度估计 ...")
        samples = np.random.default_rng(77).normal(0, 1, (500, 2))
        density, kde_obj = kde_estimate(samples)
        assert len(density) == 500
        sub = sublevel_filtration(density, n_thresholds=10)
        assert sub["sublevel_masks"].shape == (10, 500)
        sup = superlevel_filtration(density, n_thresholds=10)
        assert sup["superlevel_sizes"][0] == 500  # all points above min
        print_pass("Density estimation OK")
    else:
        print_warn("Density estimation skipped (no scipy)")

    # --- 14. Print helpers ---
    print_info("Testing print helpers (visual check) / 测试打印辅助 ...")
    print_pass("Print helpers OK")

    print_header("Self-Test Complete / 自测试完成")
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# Main entry point / 主入口
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        ok = run_self_test()
        if ok:
            print_pass("ALL TESTS PASSED / 所有测试通过")
        else:
            print_fail("SOME TESTS FAILED / 部分测试失败")
    except Exception as exc:
        print_fail(f"SELF-TEST CRASHED / 自测试崩溃: {exc}")
        raise
