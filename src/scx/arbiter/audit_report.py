"""
审计报告 — Audit Report
========================
Spring 框架的最终输出：答案 + Cercis 分数 + 审计轨迹。
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class AuditReport:
    """统一审计报告。

    Spring 框架的每个输出都附带此报告。
    回答三个问题：答案是什么？多可信？谁审计的？
    """

    # 答案
    answer: Any
    answer_type: str = "text"  # text / number / table / figure / code

    # Cercis 评分
    cercis_score: float = 0.0
    quality_score: float = 0.0   # Q — 精度
    novelty_score: float = 0.0   # N — 覆盖度 / 新颖性

    # M_t 审计参数
    M_t: int = 0
    data_hash: str = ""
    symbiotic_verified: bool = False

    # Yajie 共识
    yajie_consensus: float = 0.0       # 共识分数 ∈ [0, 1]
    yajie_verdict: str = "UNDECLARED"  # CLEAN / NOISY / AMBIGUOUS / UNDECLARED
    experts_agreed: int = 0
    experts_total: int = 0

    # 审计轨迹
    audit_trail: list = field(default_factory=list)
    verification_level: str = "V0"  # V0-V4
    cross_modal_verified: bool = False

    # 元信息
    timestamp: str = ""
    model_version: str = ""
    framework_version: str = "1.0"

    def is_audited(self) -> bool:
        """是否经过审计。"""
        return self.M_t > 0 and self.symbiotic_verified

    def confidence(self) -> str:
        """人类可读的置信度。"""
        if self.cercis_score >= 0.85:
            return "HIGH"
        elif self.cercis_score >= 0.60:
            return "MEDIUM"
        elif self.cercis_score > 0:
            return "LOW"
        return "UNAUDITED"

    def summary(self) -> str:
        """单行摘要。"""
        return (
            f"[{self.confidence()}] "
            f"Cercis={self.cercis_score:.3f} "
            f"Yajie={self.yajie_consensus:.2f} "
            f"M={self.M_t} "
            f"Experts={self.experts_agreed}/{self.experts_total}"
        )

    def to_model_card(self) -> dict:
        """导出为 Model Card 格式。"""
        return {
            "cercis_score": self.cercis_score,
            "quality_score": self.quality_score,
            "novelty_score": self.novelty_score,
            "M_t": self.M_t,
            "data_hash": self.data_hash,
            "yajie_consensus": self.yajie_consensus,
            "yajie_verdict": self.yajie_verdict,
            "verification_level": self.verification_level,
            "experts_agreed": self.experts_agreed,
            "experts_total": self.experts_total,
        }
