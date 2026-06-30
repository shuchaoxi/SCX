"""Tests for symbiotic M-parameter binding (共生绑定)."""

import hashlib

import pytest

from scx.m_parameter import (
    compute_M_min,
    compute_M_eff,
    compute_f1_bound,
    derive_M_from_data_hash,
    verify_symbiotic_binding,
    hash_data_manifest,
)
from scx.m_registry import (
    MRegistry,
    VERIFIED,
    DISCREPANCY,
)


# ---------------------------------------------------------------------------
# Symbiotic binding tests
# ---------------------------------------------------------------------------

def test_symbiotic_derivation_is_deterministic():
    dh = hashlib.sha256(b"training-data-v1").hexdigest()
    m1 = derive_M_from_data_hash(dh, epsilon=0.05, delta=0.5)
    m2 = derive_M_from_data_hash(dh, epsilon=0.05, delta=0.5)
    assert m1 == m2
    assert m1 > 0


def test_different_data_yields_different_M():
    dh1 = hashlib.sha256(b"high-quality-data").hexdigest()
    dh2 = hashlib.sha256(b"low-quality-data").hexdigest()
    m1 = derive_M_from_data_hash(dh1, epsilon=0.05, delta=0.5)
    m2 = derive_M_from_data_hash(dh2, epsilon=0.05, delta=0.5)
    # Different data should produce different M
    assert m1 != m2


def test_verify_symbiotic_binding():
    dh = hashlib.sha256(b"real-data").hexdigest()
    M = derive_M_from_data_hash(dh, epsilon=0.05, delta=0.5)
    assert verify_symbiotic_binding(dh, M, epsilon=0.05, delta=0.5)
    assert not verify_symbiotic_binding(dh, M + 1, epsilon=0.05, delta=0.5)


def test_data_substitution_detected():
    """挂羊头卖狗肉 — detected by symbiotic binding."""
    registry = MRegistry()
    dh_declared = hashlib.sha256(b"high-quality-data").hexdigest()
    dh_actual = hashlib.sha256(b"low-quality-substitute").hexdigest()

    registry.register_symbiotic(
        "company-a", dh_declared, epsilon=0.05, delta=0.5,
        domain="llm-training", code_hash="code-sha",
    )

    # Symbiotic binding should verify with declared hash
    assert registry.verify("company-a") == VERIFIED

    # But data substitution is detected
    assert registry.verify_data_substitution("company-a", dh_actual) == DISCREPANCY


def test_register_symbiotic_derives_M_from_data():
    registry = MRegistry()
    dh = hashlib.sha256(b"training-data").hexdigest()
    entry = registry.register_symbiotic(
        "paper-1", dh, epsilon=0.05, delta=0.5,
        domain="benchmark", code_hash="code-hash",
    )
    # M should be derived, not supplied
    expected_M = derive_M_from_data_hash(dh, epsilon=0.05, delta=0.5)
    assert entry.M == expected_M
    assert entry.symbiotic is True
    assert entry.verify_binding()


def test_public_private_visibility():
    registry = MRegistry()
    dh1 = hashlib.sha256(b"data-1").hexdigest()
    dh2 = hashlib.sha256(b"data-2").hexdigest()

    registry.register_symbiotic(
        "public-entity", dh1, 0.05, 0.5, "test", "code", visibility="PUBLIC",
    )
    registry.register_symbiotic(
        "private-entity", dh2, 0.05, 0.5, "test", "code", visibility="PRIVATE",
    )
    pub = registry.get_public_registry()
    assert len(pub) == 1
    assert pub[0]["entity_id"] == "public-entity"


def test_complicity_index():
    registry = MRegistry()
    dh = hashlib.sha256(b"data").hexdigest()

    # All VERIFIED -> complicity 0
    for i in range(3):
        registry.register_symbiotic(
            "good-reviewer", dh, 0.05, 0.5, "test",
            f"code-{i}", visibility="PUBLIC",
        )
    assert registry.complicity_index("good-reviewer") == 0.0

    # No entries -> 0
    assert registry.complicity_index("unknown") == 0.0


# ---------------------------------------------------------------------------
# Legacy tests (still valid)
# ---------------------------------------------------------------------------

def test_m_parameter_formulas():
    assert compute_M_min(epsilon=0.05, delta=0.5) == 6
    assert compute_M_eff(M=10, rho_bar=0.0) == pytest.approx(10.0)
    assert compute_M_eff(M=10, rho_bar=1.0) == pytest.approx(1.0)
    assert compute_f1_bound(M=10, delta=0.5, states=[0, 0, 1, 1], eta=1.0) > 0.9


def test_hash_data_manifest():
    import tempfile, os
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        f.write(b"test data")
        tmp = f.name
    try:
        h = hash_data_manifest([tmp])
        assert len(h) == 64
    finally:
        os.unlink(tmp)
