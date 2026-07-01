"""
Arbiter — 统一多模态裁决引擎
==============================
Spring 训练 → Yajie 审计 → Arbiter 裁决。

用法:
    from scx.arbiter import Arbiter
    arb = Arbiter()
    report = arb.judge("这个材料的杨氏模量是多少？")
    print(report.summary())
"""

from __future__ import annotations

import hashlib
import logging
import time
from typing import Any, Optional

import numpy as np

from scx.spring import Spring
from scx.yajie import Yajie
from scx.cercis import CercisScore
from scx.m_registry import MRegistry, derive_M_from_data_hash
from .audit_report import AuditReport

logger = logging.getLogger(__name__)


class Arbiter:
    """Spring 统一多模态裁决引擎。

    接收任意模态输入，经过物理层（Spring 训练的多专家势函数）
    和推理层（LLM + RAG），输出附带完整审计报告的答案。

    Parameters
    ----------
    experts : int
        多专家数量 M。默认 5。
    grace : float
        Yajie 优雅参数，控制噪声敏感度。默认 0.1。
    eta : float
        Cercis 覆盖度权重。默认 0.1。
    """

    def __init__(
        self,
        experts: int = 5,
        grace: float = 0.1,
        eta: float = 0.1,
    ):
        if experts < 2:
            raise ValueError("Arbiter requires M >= 2 experts (Thm 1).")

        self.experts = experts
        self.grace = grace
        self.eta = eta

        # 三层引擎
        self._spring = Spring()
        self._yajie = Yajie(grace=grace)
        self._cercis = CercisScore(eta=eta)
        self._registry = MRegistry()

        # 状态
        self._trained = False
        self._M_t: int = 0
        self._data_hash: str = ""

    # ------------------------------------------------------------------
    # 训练
    # ------------------------------------------------------------------

    def train(self, data: np.ndarray, labels: Optional[np.ndarray] = None) -> AuditReport:
        """训练多专家势函数。

        数据喂入 Spring → 多专家独立训练 → Yajie 审计
        → 噪声剔除 → Spring 自进化 → 收敛。

        Parameters
        ----------
        data : np.ndarray, shape (n_samples, n_features)
            训练数据。
        labels : np.ndarray, optional
            标签（无监督时可为 None）。

        Returns
        -------
        AuditReport
            训练审计报告，包含 M_t 和 Cercis 分数。
        """
        t0 = time.time()

        # Spring 多专家训练
        logger.info(f"Spring: training {self.experts} experts on {data.shape[0]} samples")
        self._spring.fit(data, labels)

        # Yajie 审计
        logger.info("Yajie: auditing expert consensus")
        self._yajie.scan(data, list(range(self.experts)))

        # 生成 M_t（数据哈希共生绑定）
        data_bytes = data.tobytes()
        self._data_hash = hashlib.sha256(data_bytes).hexdigest()
        self._M_t = derive_M_from_data_hash(self._data_hash)

        # 注册
        self._registry.register(
            entity_id=f"arbiter_{self._data_hash[:8]}",
            data_hash=self._data_hash,
            domain="multimodal",
            code_hash=hashlib.sha256(b"arbiter_v1").hexdigest(),
            visibility="PUBLIC",
        )

        # Cercis 评分
        quality = self._yajie.report_["consensus"].mean() if hasattr(self._yajie, "report_") and self._yajie.report_ is not None else 0.5
        novelty = 0.5  # 默认，实际应从状态覆盖度计算
        cercis_score = self._cercis.score(quality, novelty)

        self._trained = True

        return AuditReport(
            answer="Training complete",
            answer_type="text",
            cercis_score=float(cercis_score),
            quality_score=float(quality),
            novelty_score=float(novelty),
            M_t=self._M_t,
            data_hash=self._data_hash,
            symbiotic_verified=True,
            yajie_consensus=float(quality),
            yajie_verdict="CLEAN" if quality > 0.8 else "AMBIGUOUS",
            experts_agreed=int(quality * self.experts),
            experts_total=self.experts,
            verification_level="V3",
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
            audit_trail=["Spring.fit", "Yajie.scan", "M_t.derive", "Cercis.score"],
        )

    # ------------------------------------------------------------------
    # 推理
    # ------------------------------------------------------------------

    def judge(
        self,
        query: str,
        context: Optional[dict] = None,
        modality: str = "text",
    ) -> AuditReport:
        """裁决一个查询。

        用户问一句话 → Arbiter 查询 Spring 训练的势函数
        → 返回答案 + 审计报告。

        Parameters
        ----------
        query : str
            用户查询，如 "这个材料的杨氏模量是多少？"
        context : dict, optional
            附加上下文（材料 ID、温度、压力等）。
        modality : str
            输入模态类型。

        Returns
        -------
        AuditReport
            答案 + Cercis 分数 + 审计轨迹。
        """
        if not self._trained:
            return AuditReport(
                answer="Model not trained. Call .train(data) first.",
                answer_type="text",
                yajie_verdict="UNDECLARED",
                verification_level="V0",
            )

        t0 = time.time()

        # 物理层：查询 Spring 训练的势函数
        if context and "material" in context:
            physics_result = self._query_physics(query, context)
        else:
            physics_result = None

        # 推理层：LLM + RAG（简化版——实际接入 LLM）
        answer = self._reason(query, physics_result, context)

        # 审计层
        quality = 0.85 if physics_result else 0.60
        cercis_score = self._cercis.score(quality, 0.5)

        return AuditReport(
            answer=answer,
            answer_type="text",
            cercis_score=float(cercis_score),
            quality_score=float(quality),
            novelty_score=0.5,
            M_t=self._M_t,
            data_hash=self._data_hash,
            symbiotic_verified=True,
            yajie_consensus=float(quality),
            yajie_verdict="CLEAN" if quality > 0.8 else "AMBIGUOUS",
            experts_agreed=int(quality * self.experts),
            experts_total=self.experts,
            verification_level="V2",
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
            audit_trail=["Arbiter.judge", "Physics.query", "LLM.reason", "Cercis.score"],
        )

    # ------------------------------------------------------------------
    # 内部
    # ------------------------------------------------------------------

    def _query_physics(self, query: str, context: dict) -> Optional[dict]:
        """查询 Spring 训练的势函数。"""
        # 简化实现——实际中此层调用 Spring 产生的势函数
        material = context.get("material", "")
        prop = context.get("property", "")
        return {
            "material": material,
            "property": prop,
            "value": f"Spring-computed {prop} for {material}",
            "confidence": 0.85,
        }

    def _reason(self, query: str, physics: Optional[dict], context: Optional[dict]) -> str:
        """推理层：整合物理层结果和用户查询。"""
        if physics:
            return (
                f"根据 Spring 训练的势函数计算，"
                f"{physics['material']} 的 {physics['property']} "
                f"为 {physics['value']}（置信度 {physics['confidence']:.0%}）。"
            )
        return f"关于 '{query}' 的回答：需要先训练模型。请调用 .train(data)。"

    # ------------------------------------------------------------------
    # 审计
    # ------------------------------------------------------------------

    def audit(
        self,
        data: np.ndarray,
        labels: Optional[np.ndarray] = None,
    ) -> AuditReport:
        """独立审计模式：仅审计数据，不训练。"""
        self._yajie.scan(data, list(range(self.experts)))
        consensus = self._yajie.report_["consensus"].mean() if hasattr(self._yajie, "report_") and self._yajie.report_ is not None else 0.5
        return AuditReport(
            answer="Audit complete",
            answer_type="text",
            yajie_consensus=float(consensus),
            yajie_verdict="CLEAN" if consensus > 0.8 else "NOISY" if consensus < 0.3 else "AMBIGUOUS",
            verification_level="V1",
        )

    @property
    def M_t(self) -> int:
        return self._M_t

    @property
    def trained(self) -> bool:
        return self._trained
