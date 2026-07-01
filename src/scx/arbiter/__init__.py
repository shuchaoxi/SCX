"""
Arbiter — Spring 统一多模态裁决框架
=====================================
Spring trains. Yajie audits. Arbiter judges.

四层架构：
    Input → Physics → Reasoning → Audit → Output
    输入层   物理层     推理层      审计层   输出

用法:
    from scx.arbiter import Arbiter
    arb = Arbiter(experts=5)
    arb.train(data)
    report = arb.judge("这个材料的杨氏模量是多少？")
    print(report.summary())  # [HIGH] Cercis=0.850 M=5 Experts=4/5
"""

from .arbiter import Arbiter
from .audit_report import AuditReport

__all__ = [
    "Arbiter",
    "AuditReport",
]
