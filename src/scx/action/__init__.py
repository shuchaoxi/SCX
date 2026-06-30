"""SCX Action Module

Action decision engine, acquisition strategies, and compress strategies
for the SCX (State-Conditioned eXpertise) framework.

Action space A = {acquire, relabel, downweight, discard, route, split}
"""

from scx.action.policy import ActionPolicy, ActionResult
from scx.action.acquisition import AcquisitionStrategy
from scx.action.compress import CompressStrategy

__all__ = [
    "ActionPolicy",
    "ActionResult",
    "AcquisitionStrategy",
    "CompressStrategy",
]
