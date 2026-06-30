"""Append-only M-parameter registry for SCX audit declarations."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Literal

from .m_parameter import compute_M_min


VERIFIED = "VERIFIED"
DISCREPANCY = "DISCREPANCY"
PENDING = "PENDING"

Visibility = Literal["PUBLIC", "PRIVATE"]
VerificationStatus = Literal["VERIFIED", "DISCREPANCY", "PENDING"]


@dataclass(frozen=True)
class MRegistryEntry:
    """Single immutable declaration in the M-registry ledger."""

    sequence_id: int
    entity_id: str
    M: int
    epsilon: float
    delta: float
    domain: str
    code_hash: str
    data_manifest_hash: str
    visibility: Visibility
    commitment_hash: str


class MRegistry:
    """Public append-only ledger for M-parameter declarations."""

    def __init__(self) -> None:
        self._ledger: list[MRegistryEntry] = []

    def register(
        self,
        entity_id: str,
        M: int,
        epsilon: float,
        delta: float,
        domain: str,
        code_hash: str,
        data_manifest_hash: str,
        visibility: Visibility = "PUBLIC",
    ) -> MRegistryEntry:
        """Append a new M declaration to the registry ledger."""
        visibility = _normalise_visibility(visibility)
        if not entity_id:
            raise ValueError("entity_id must be non-empty")
        if M <= 0:
            raise ValueError(f"M must be positive, got {M}")
        if not 0.0 < epsilon < 1.0:
            raise ValueError(f"epsilon must be in (0, 1), got {epsilon}")
        if delta <= 0.0:
            raise ValueError(f"delta must be > 0, got {delta}")
        if not domain:
            raise ValueError("domain must be non-empty")
        if not code_hash:
            raise ValueError("code_hash must be non-empty")
        if not data_manifest_hash:
            raise ValueError("data_manifest_hash must be non-empty")

        commitment_hash = self.compute_hash(
            M=M,
            epsilon=epsilon,
            delta=delta,
            code=code_hash,
            data_manifest=data_manifest_hash,
        )
        entry = MRegistryEntry(
            sequence_id=len(self._ledger),
            entity_id=str(entity_id),
            M=int(M),
            epsilon=float(epsilon),
            delta=float(delta),
            domain=str(domain),
            code_hash=str(code_hash),
            data_manifest_hash=str(data_manifest_hash),
            visibility=visibility,
            commitment_hash=commitment_hash,
        )
        self._ledger.append(entry)
        return entry

    def verify(self, entity_id: str) -> VerificationStatus:
        """Verify the latest declaration for an entity."""
        entry = self._latest_entry(entity_id)
        if entry is None:
            return PENDING
        return self._entry_status(entry)

    @staticmethod
    def compute_hash(
        M: int,
        epsilon: float,
        delta: float,
        code: Any,
        data_manifest: Any,
    ) -> str:
        """Compute the SHA-256 commitment hash for an M declaration."""
        payload = [
            ("code", code),
            ("data_manifest", data_manifest),
            ("M", int(M)),
            ("epsilon", float(epsilon)),
            ("delta", float(delta)),
        ]
        digest = hashlib.sha256()
        for label, value in payload:
            digest.update(label.encode("utf-8"))
            digest.update(b"\0")
            digest.update(_canonical_bytes(value))
            digest.update(b"\0")
        return digest.hexdigest()

    def get_public_registry(self) -> list[dict[str, Any]]:
        """Return copies of PUBLIC ledger entries."""
        return [
            asdict(entry)
            for entry in self._ledger
            if entry.visibility == "PUBLIC"
        ]

    def complicity_index(self, reviewer_id: str) -> float:
        """Return the fraction of a reviewer's declarations with issues.

        In this minimal ledger, ``reviewer_id`` is matched against
        ``entity_id`` declarations. Entities with no declarations have index 0.
        """
        entries = [e for e in self._ledger if e.entity_id == reviewer_id]
        if not entries:
            return 0.0
        non_verified = sum(1 for entry in entries if self._entry_status(entry) != VERIFIED)
        return float(non_verified / len(entries))

    @property
    def ledger(self) -> tuple[MRegistryEntry, ...]:
        """Immutable view of all registry entries."""
        return tuple(self._ledger)

    def _latest_entry(self, entity_id: str) -> MRegistryEntry | None:
        for entry in reversed(self._ledger):
            if entry.entity_id == entity_id:
                return entry
        return None

    @staticmethod
    def _entry_status(entry: MRegistryEntry) -> VerificationStatus:
        required_M = compute_M_min(entry.epsilon, entry.delta)
        if entry.M < required_M:
            return DISCREPANCY
        return VERIFIED


def _normalise_visibility(visibility: str) -> Visibility:
    value = str(visibility).upper()
    if value not in {"PUBLIC", "PRIVATE"}:
        raise ValueError("visibility must be 'PUBLIC' or 'PRIVATE'")
    return value  # type: ignore[return-value]


def _canonical_bytes(value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
