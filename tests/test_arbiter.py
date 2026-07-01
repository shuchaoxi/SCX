"""
Arbiter 测试
===========
Spring trains → Yajie audits → Arbiter judges.
"""

import numpy as np
import pytest
from scx.arbiter import Arbiter, AuditReport


class TestAuditReport:
    def test_default_report(self):
        r = AuditReport(answer="test")
        assert r.answer == "test"
        assert r.is_audited() is False
        assert r.confidence() == "UNAUDITED"

    def test_audited_report(self):
        r = AuditReport(
            answer="42",
            M_t=5,
            symbiotic_verified=True,
            cercis_score=0.92,
            yajie_consensus=0.90,
            experts_agreed=4,
            experts_total=5,
        )
        assert r.is_audited() is True
        assert r.confidence() == "HIGH"

    def test_summary(self):
        r = AuditReport(
            answer="test",
            cercis_score=0.85,
            M_t=8,
            experts_agreed=7,
            experts_total=8,
            yajie_consensus=0.88,
        )
        assert "HIGH" in r.summary()
        assert "0.850" in r.summary()

    def test_model_card(self):
        r = AuditReport(answer="test", M_t=5, cercis_score=0.80)
        card = r.to_model_card()
        assert card["cercis_score"] == 0.80
        assert card["M_t"] == 5


class TestArbiter:
    def test_init(self):
        arb = Arbiter(experts=3)
        assert arb.experts == 3
        assert arb.trained is False

    def test_init_rejects_M_1(self):
        with pytest.raises(ValueError, match="M >= 2"):
            Arbiter(experts=1)

    def test_train(self):
        arb = Arbiter(experts=3)
        data = np.random.randn(50, 4)
        report = arb.train(data)
        assert arb.trained is True
        assert arb.M_t > 0
        assert report.M_t > 0
        assert report.symbiotic_verified is True

    def test_judge_before_train(self):
        arb = Arbiter(experts=3)
        report = arb.judge("test query")
        assert report.yajie_verdict == "UNDECLARED"

    def test_judge_after_train(self):
        arb = Arbiter(experts=3)
        data = np.random.randn(50, 4)
        arb.train(data)
        report = arb.judge(
            "杨氏模量是多少？",
            context={"material": "AlN", "property": "Young's modulus"},
        )
        assert report.yajie_verdict == "CLEAN"
        assert "AlN" in str(report.answer)

    def test_audit_standalone(self):
        arb = Arbiter(experts=3)
        data = np.random.randn(50, 4)
        report = arb.audit(data)
        assert report.verification_level == "V1"
