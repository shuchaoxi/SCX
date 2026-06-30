"""Base operator interfaces for the drug module.

Mirrors ``scx.operators.base`` but operates on ``TargetProfileState``
instead of ``ProcessState``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from scx_drug.state import TargetProfileState


@dataclass
class DrugStepContext:
    """Execution context passed into a DrugOperator."""

    step_index: int
    step_name: str
    step_type: str
    recipe: dict[str, Any] = field(default_factory=dict)


class DrugOperator(Protocol):
    """A drug-prediction step maps one TargetProfileState to the next."""

    name: str

    def apply(
        self,
        state: TargetProfileState,
        context: DrugStepContext,
    ) -> TargetProfileState:
        """Apply one prediction step."""


def next_state(
    state: TargetProfileState,
    context: DrugStepContext,
) -> TargetProfileState:
    """Clone state for the operator output."""
    return state.clone(
        state_id=f"{context.step_index:03d}_{context.step_name}",
        history_event={
            "step_index": context.step_index,
            "step_name": context.step_name,
            "step_type": context.step_type,
            "recipe": context.recipe,
        },
    )
