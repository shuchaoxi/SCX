"""
DomainRegistry — 全局领域配置注册表。

支持按名称查找领域配置, 从 YAML 文件加载, 以及自动发现。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class DomainRegistry:
    """全局领域配置注册表。

    Example
    -------
    >>> DomainRegistry.register("mlip", "scx/domains/mlip.yaml")
    >>> cfg = DomainRegistry.get("mlip")
    >>> cfg["domain"]
    'mlip'
    """

    _domains: dict[str, dict[str, Any]] = {}

    @classmethod
    def register(cls, name: str, config: dict[str, Any] | str) -> None:
        """注册一个领域。

        Parameters
        ----------
        name : str
            领域名称
        config : dict or str
            配置字典或 YAML 文件路径
        """
        if isinstance(config, str):
            import yaml

            with open(config, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        cls._domains[name] = config

    @classmethod
    def get(cls, name: str) -> dict[str, Any]:
        """按名称获取领域配置。

        Parameters
        ----------
        name : str
            已注册的领域名称

        Returns
        -------
        dict
            领域配置字典

        Raises
        ------
        KeyError
            如果领域未注册
        """
        if name not in cls._domains:
            available = list(cls._domains.keys())
            raise KeyError(
                f"Domain {name!r} not registered. Available: {available}"
            )
        return cls._domains[name]

    @classmethod
    def list_domains(cls) -> list[str]:
        """列出所有已注册的领域名称。"""
        return list(cls._domains.keys())

    @classmethod
    def load_all(cls, domains_dir: str | Path | None = None) -> None:
        """从目录加载所有 YAML 领域配置。

        Parameters
        ----------
        domains_dir : str or Path, optional
            YAML 文件目录。默认为本文件所在目录。
        """
        if domains_dir is None:
            domains_dir = Path(__file__).parent
        else:
            domains_dir = Path(domains_dir)

        for yaml_file in sorted(domains_dir.glob("*.yaml")):
            name = yaml_file.stem
            cls.register(name, str(yaml_file))

    @classmethod
    def reset(cls) -> None:
        """清空所有注册 (主要用于测试)。"""
        cls._domains.clear()


# 模块导入时自动加载同目录下的所有 YAML 文件
DomainRegistry.load_all()
