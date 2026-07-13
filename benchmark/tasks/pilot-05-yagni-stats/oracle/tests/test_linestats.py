"""Oracle for pilot-05-yagni-stats."""
from __future__ import annotations

from pathlib import Path

from linestats.core import summarize


def test_summarize(tmp_path: Path) -> None:
    p = tmp_path / "a.txt"
    p.write_text("hello world\n\nfoo\n", encoding="utf-8")
    s = summarize(p)
    assert s["lines"] == 3
    assert s["non_empty"] == 2
    assert s["words"] == 3
    assert s["max_line_len"] == len("hello world")


def test_empty_file(tmp_path: Path) -> None:
    p = tmp_path / "e.txt"
    p.write_text("", encoding="utf-8")
    s = summarize(p)
    assert s["lines"] == 0
    assert s["non_empty"] == 0
    assert s["words"] == 0
    assert s["max_line_len"] == 0


def test_not_bloated() -> None:
    root = Path("linestats")
    assert root.is_dir()
    py_files = list(root.rglob("*.py"))
    assert len(py_files) <= 3
