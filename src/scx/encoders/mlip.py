"""
MLIP Encoder — 机器学习原子间势函数 (MLIP) 领域的状态编码器。

使用手工描述符 (配位数、键长分布、体积等) 将 ASE Atoms 对象
编码为固定维度的特征向量, 避免对 dscribe 等重依赖。

Example
-------
>>> import ase
>>> from scx.encoders.mlip import MLIPEncoder
>>> encoder = MLIPEncoder(species=["Al", "Ga", "N"])
>>> atoms = ase.Atoms("AlN", positions=[(0,0,0), (0,0,2.0)],
...                   cell=[4,4,4], pbc=True)
>>> vec = encoder.encode(atoms)
>>> vec.shape
(12,)
"""

from __future__ import annotations

from typing import Any

import numpy as np

from scx.encoders.base import SCXStateEncoder


class MLIPEncoder(SCXStateEncoder):
    """MLIP 状态编码器: 从 ASE Atoms 提取手工描述符。

    特征向量组成 (固定 12 维):
    0:  原子数 N
    1:  平均配位数 (CN)
    2:  最短键长
    3:  最长键长
    4:  平均键长
    5:  键长标准差
    6:  体积 / 原子
    7:  密度 (原子数 / 体积)
    8:  species 数
    9:  max pairwise distance
    10: 能量 E (若 atoms.info 中有 "energy" 键, 否则 0)
    11: 力 norm 均值 (若 atoms.arrays 中有 "forces", 否则 0)

    Parameters
    ----------
    descriptor : str
        描述符类型 (当前仅支持 "ace", 保留接口兼容)
    species : list[str] | None
        元素种类列表, 默认 ["Al", "Ga", "N"]
    rcut : float
        截断半径 (A), 用于配位数计算
    """

    def __init__(
        self,
        descriptor: str = "ace",
        species: list[str] | None = None,
        rcut: float = 4.0,
    ) -> None:
        self.descriptor = descriptor
        self.species = species or ["Al", "Ga", "N"]
        self.rcut = rcut
        self._feature_dim = 12

    def encode(self, atoms: Any) -> np.ndarray:
        """将 ASE Atoms 对象编码为 12 维特征向量。

        Parameters
        ----------
        atoms : ase.Atoms
            ASE 原子构型对象

        Returns
        -------
        np.ndarray, shape (12,)
        """
        # --- Number of atoms ---
        n_atoms = len(atoms)

        # --- Cell volume ---
        try:
            volume = atoms.get_volume()
        except Exception:
            volume = 1.0
        vol_per_atom = volume / max(n_atoms, 1)

        # --- Pairwise distances ---
        try:
            positions = atoms.positions
            dists = self._pairwise_distances(positions, atoms.cell, atoms.pbc)
        except Exception:
            dists = np.array([], dtype=float)

        if len(dists) > 0:
            min_bond = float(dists.min())
            max_bond = float(dists.max())
            mean_bond = float(dists.mean())
            std_bond = float(dists.std()) if len(dists) > 1 else 0.0
        else:
            min_bond = max_bond = mean_bond = std_bond = 0.0

        # --- Coordination number (averaged) ---
        if len(dists) > 0 and n_atoms > 0:
            # Count neighbors within rcut for each atom
            cn_total = 0.0
            for i in range(n_atoms):
                # distances from atom i to all others
                row_start = i * n_atoms
                row_dists = dists[row_start : row_start + n_atoms]
                # exclude self (distance == 0)
                cn = float(np.sum((row_dists > 1e-6) & (row_dists <= self.rcut)))
                cn_total += cn
            mean_cn = cn_total / n_atoms
        else:
            mean_cn = 0.0

        # --- Number of species ---
        try:
            symbols = atoms.get_chemical_symbols()
            n_species = len(set(symbols))
        except Exception:
            n_species = 0

        # --- Max pairwise distance ---
        max_pairwise = float(dists.max()) if len(dists) > 0 else 0.0

        # --- Density ---
        density = n_atoms / max(volume, 1e-10)

        # --- Energy (if available in info dict) ---
        try:
            energy = float(atoms.info.get("energy", 0.0))
        except Exception:
            energy = 0.0

        # --- Forces (if available) ---
        try:
            if "forces" in atoms.arrays:
                forces = atoms.arrays["forces"]
                force_norm_mean = float(np.mean(np.linalg.norm(forces, axis=1)))
            else:
                force_norm_mean = 0.0
        except Exception:
            force_norm_mean = 0.0

        feature = np.array(
            [
                float(n_atoms),
                float(mean_cn),
                float(min_bond),
                float(max_bond),
                float(mean_bond),
                float(std_bond),
                float(vol_per_atom),
                float(density),
                float(n_species),
                float(max_pairwise),
                float(energy),
                float(force_norm_mean),
            ],
            dtype=np.float64,
        )
        return feature

    def batch_encode(self, atoms_list: list[Any]) -> np.ndarray:
        """批量编码 Atoms 对象。

        Parameters
        ----------
        atoms_list : list[ase.Atoms]

        Returns
        -------
        np.ndarray, shape (N, 12)
        """
        return np.stack([self.encode(a) for a in atoms_list])

    def distance(self, a: np.ndarray, b: np.ndarray) -> float:
        """Euclidean 距离。"""
        return float(np.linalg.norm(a - b))

    def cluster(
        self, X: np.ndarray, n_clusters: int, **kwargs
    ) -> tuple[np.ndarray, np.ndarray]:
        """KMeans 聚类, 带有自动 K 选择保护。

        Parameters
        ----------
        X : np.ndarray, shape (N, d)
        n_clusters : int
        **kwargs
            random_state : int

        Returns
        -------
        labels : np.ndarray, shape (N,)
        centroids : np.ndarray, shape (K, d)
        """
        from sklearn.cluster import KMeans

        n = max(min(n_clusters, len(X) - 1), 1)
        rs = kwargs.get("random_state", 42)
        km = KMeans(n_clusters=n, random_state=rs, n_init="auto")
        labels = km.fit_predict(X)
        return labels, km.cluster_centers_

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _pairwise_distances(
        positions: np.ndarray,
        cell: np.ndarray | None = None,
        pbc: list[bool] | None = None,
    ) -> np.ndarray:
        """计算所有原子对之间的 (最小镜像) 距离。"""
        n = len(positions)
        if n <= 1:
            return np.array([], dtype=float)
        dists = []
        for i in range(n):
            for j in range(n):
                if i == j:
                    dists.append(0.0)
                    continue
                vec = positions[j] - positions[i]
                # Apply minimum image convention if periodic
                if cell is not None and pbc is not None and any(pbc):
                    for d in range(3):
                        if pbc[d] and cell is not None:
                            cell_vec = cell[:, d] if cell.ndim == 2 else np.zeros(3)
                            if np.linalg.norm(cell_vec) > 0:
                                vec[d] -= round(vec[d] / cell_vec[d]) * cell_vec[d]
                dists.append(float(np.linalg.norm(vec)))
        return np.array(dists, dtype=float)
