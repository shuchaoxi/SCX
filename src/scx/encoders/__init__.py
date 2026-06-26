"""
SCX Encoders — 领域编码器, 负责将任意领域输入编码为状态空间向量。

每个编码器实现 `SCXStateEncoder` 抽象基类的三个核心方法:
- encode: 原始输入 → 特征向量
- distance: 特征空间中两点的距离
- cluster: 对编码向量聚类 → 状态划分
"""

from scx.encoders.base import SCXStateEncoder, SCXExpert
from scx.encoders.mlip import MLIPEncoder
from scx.encoders.vision import VisionEncoder
from scx.encoders.tabular import TabularEncoder
from scx.encoders.error_driven import ErrorDrivenEncoder

__all__ = [
    "SCXStateEncoder",
    "SCXExpert",
    "MLIPEncoder",
    "VisionEncoder",
    "TabularEncoder",
    "ErrorDrivenEncoder",
]
