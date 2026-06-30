"""Append-only M-parameter registry for SCX audit declarations.

共生绑定: M = first 20 bits of SHA-256(training data).
M is not declared — it IS the data hash, truncated. Inseparable.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from .m_parameter import derive_M_from_data_hash, verify_symbiotic_binding

VERIFIED = "VERIFIED"
DISCREPANCY = "DISCREPANCY"
PENDING = "PENDING"
Visibility = Literal["PUBLIC", "PRIVATE"]
VerificationStatus = Literal["VERIFIED", "DISCREPANCY", "PENDING"]


@dataclass(frozen=True)
class MRegistryEntry:
    """Immutable M-registry declaration. M derived from data_hash."""
    sequence_id: int
    entity_id: str
    M: int
    domain: str
    data_hash: str
    code_hash: str
    visibility: Visibility
    commitment_hash: str
    symbiotic: bool = field(default=True)

    def verify_binding(self) -> bool:
        return verify_symbiotic_binding(self.data_hash, self.M)


class MRegistry:
    """Public append-only ledger. M is derived — never declared."""

    def __init__(self) -> None:
        self._ledger: list[MRegistryEntry] = []

    def register(
        self,
        entity_id: str,
        data_hash: str,
        domain: str,
        code_hash: str,
        visibility: Visibility = "PUBLIC",
    ) -> MRegistryEntry:
        """Register with symbiotically-derived M.

        The declarer supplies the data hash. M is COMPUTED from it.
        The declarer cannot choose M — cannot 挂羊头卖狗肉.
        """
        visibility = _normalise_visibility(visibility)
        if not entity_id:
            raise ValueError("entity_id must be non-empty")
        if not data_hash or len(data_hash) != 64:
            raise ValueError("data_hash must be 64-char SHA-256 hex")
        if not domain:
            raise ValueError("domain must be non-empty")
        if not code_hash:
            raise ValueError("code_hash must be non-empty")

        M = derive_M_from_data_hash(data_hash)
        commitment = _symbiotic_hash(M, data_hash, code_hash)

        entry = MRegistryEntry(
            sequence_id=len(self._ledger),
            entity_id=str(entity_id),
            M=int(M),
            domain=str(domain),
            data_hash=str(data_hash),
            code_hash=str(code_hash),
            visibility=visibility,
            commitment_hash=commitment,
            symbiotic=True,
        )
        self._ledger.append(entry)
        return entry

    def verify(self, entity_id: str) -> VerificationStatus:
        entry = self._latest_entry(entity_id)
        if entry is None:
            return PENDING
        if not entry.verify_binding():
            return DISCREPANCY
        return VERIFIED

    def verify_data_substitution(
        self, entity_id: str, actual_data_hash: str
    ) -> VerificationStatus:
        """Theorem 5: detect 挂羊头卖狗肉."""
        entry = self._latest_entry(entity_id)
        if entry is None:
            return PENDING
        return DISCREPANCY if entry.data_hash != actual_data_hash else VERIFIED

    def get_public_registry(self) -> list[dict[str, Any]]:
        return [asdict(e) for e in self._ledger if e.visibility == "PUBLIC"]

    def complicity_index(self, entity_id: str) -> float:
        entries = [e for e in self._ledger if e.entity_id == entity_id]
        if not entries:
            return 0.0
        bad = sum(1 for e in entries if not e.verify_binding())
        return float(bad / len(entries))

    @property
    def ledger(self) -> tuple[MRegistryEntry, ...]:
        return tuple(self._ledger)

    def _latest_entry(self, entity_id: str) -> MRegistryEntry | None:
        for e in reversed(self._ledger):
            if e.entity_id == entity_id:
                return e
        return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _symbiotic_hash(M: int, data_hash: str, code_hash: str) -> str:
    d = hashlib.sha256()
    for label, val in [("data", data_hash), ("code", code_hash), ("M", str(M))]:
        d.update(label.encode()); d.update(b"\x00")
        d.update(val.encode()); d.update(b"\x00")
    return d.hexdigest()


def _normalise_visibility(v: str) -> Visibility:
    v = str(v).upper()
    if v not in {"PUBLIC", "PRIVATE"}:
        raise ValueError("visibility must be PUBLIC or PRIVATE")
    return v  # type: ignore
