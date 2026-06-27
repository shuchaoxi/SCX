"""
SCX: State-Conditioned eXpertise

A framework for state-conditioned expert reliability estimation,
data valuation, and state-wise active learning.

Version 4.0 (通用模块化架构):
- encoders/: 领域编码器 (SCXStateEncoder + 内置实现)
- domains/: 声明式领域 YAML 配置
- core/: 通用核心 (不变)
- state/: 状态管理 (不变)
- expert/: 专家系统 (不变)
- valuation/: 数据估值 (不变)
- action/: 动作策略 (不变)
"""

__version__ = "4.0.0a1"
__version_info__ = (4, 0, 0, "alpha", 1)

# --- 核心模块（向后兼容）---
from scx.core.framework import SCXFramework
from scx.core.config import SCXConfig
from scx.core.metrics import SCXMetrics

# --- 新模块（通用模块化架构）---
from scx.encoders.base import SCXStateEncoder, SCXExpert
from scx.encoders.mlip import MLIPEncoder
from scx.encoders.vision import VisionEncoder
from scx.encoders.tabular import TabularEncoder
from scx.domains.registry import DomainRegistry

# --- 雅洁: Elegant data sanitizer ---
from scx.yajie import Yajie, yajie, clean

__all__ = [
    # Core (existing, stable)
    "SCXFramework",
    "SCXConfig",
    "SCXMetrics",
    # Encoders (new in v4.0)
    "SCXStateEncoder",
    "SCXExpert",
    "MLIPEncoder",
    "VisionEncoder",
    "TabularEncoder",
    # Domains (new in v4.0)
    "DomainRegistry",
    # 雅洁 — named after the most elegant cleaner
    "Yajie",
    "yajie",
    "clean",
]
