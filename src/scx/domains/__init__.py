"""
SCX 领域配置 — 声明式 YAML 配置注册与管理。

每个领域对应一个 YAML 文件, 定义:
- encoder 类路径与参数
- 专家列表
- 状态发现配置
- 分类阈值

使用方式:
    from scx.domains.registry import DomainRegistry

    # 自动加载所有 YAML
    DomainRegistry.load_all()

    # 获取领域配置
    config = DomainRegistry.get("mlip")
"""

from scx.domains.registry import DomainRegistry

__all__ = ["DomainRegistry"]
