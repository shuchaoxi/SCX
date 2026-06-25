"""
SCX: State-Conditioned eXpertise

A framework for state-conditioned expert reliability estimation,
data valuation, and state-wise active learning.
"""

__version__ = "0.1.0"

from scx.core.framework import SCXFramework
from scx.core.config import SCXConfig
from scx.core.metrics import SCXMetrics

__all__ = ["SCXFramework", "SCXConfig", "SCXMetrics"]
