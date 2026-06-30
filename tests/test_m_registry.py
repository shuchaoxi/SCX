"""Tests for M-registry and M-parameter utilities."""

from __future__ import annotations

import pytest

from scx.m_parameter import compute_M_eff, compute_M_min, compute_f1_bound
from scx.m_registry import DISCREPANCY, VERIFIED, MRegistry


def test_registry_register_verify_and_public_view():
    registry = MRegistry()
    m_min = compute_M_min(epsilon=0.05, delta=0.5)

    entry = registry.register(
        entity_id="paper-1",
        M=m_min,
        epsilon=0.05,
        delta=0.5,
        domain="benchmark",
        code_hash="code-sha",
        data_manifest_hash="manifest-sha",
    )

    assert registry.verify("paper-1") == VERIFIED
    assert entry.commitment_hash == MRegistry.compute_hash(
        m_min, 0.05, 0.5, "code-sha", "manifest-sha"
    )
    assert registry.get_public_registry()[0]["entity_id"] == "paper-1"


def test_registry_flags_low_m_and_hides_private_entries():
    registry = MRegistry()
    m_min = compute_M_min(epsilon=0.05, delta=0.5)

    registry.register(
        "paper-2",
        M=m_min - 1,
        epsilon=0.05,
        delta=0.5,
        domain="benchmark",
        code_hash="code-sha",
        data_manifest_hash="manifest-sha",
        visibility="PRIVATE",
    )

    assert registry.verify("paper-2") == DISCREPANCY
    assert registry.get_public_registry() == []
    assert registry.complicity_index("paper-2") == 1.0


def test_m_parameter_formulas():
    assert compute_M_min(epsilon=0.05, delta=0.5) == 6
    assert compute_M_eff(M=10, rho_bar=0.0) == pytest.approx(10.0)
    assert compute_M_eff(M=10, rho_bar=1.0) == pytest.approx(1.0)
    assert compute_f1_bound(M=10, delta=0.5, states=[0, 0, 1, 1], eta=1.0) > 0.9
