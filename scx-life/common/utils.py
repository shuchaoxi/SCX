"""Shared utility functions for SCX-Life modules."""

import json
import os
import time
from pathlib import Path
from typing import Any


def ensure_dir(path: str | Path) -> Path:
    """Create a directory if it does not exist and return the Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def load_json(path: str | Path) -> dict[str, Any]:
    """Load a JSON file and return its contents."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(data: Any, path: str | Path, indent: int = 2) -> None:
    """Save data to a JSON file with pretty-printing."""
    Path(path).write_text(
        json.dumps(data, indent=indent, default=str, ensure_ascii=False),
        encoding="utf-8",
    )


class Timer:
    """Simple context manager for timing code blocks.

    Examples
    --------
    >>> with Timer("training") as t:
    ...     model.train()
    >>> print(f"Training took {t.elapsed:.2f}s")
    """

    def __init__(self, name: str = ""):
        self.name = name
        self.elapsed = 0.0

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, *exc: Any) -> None:
        self.elapsed = time.perf_counter() - self._start
