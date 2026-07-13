"""Oracle for pilot-06-log-pipeline."""
from __future__ import annotations

from pathlib import Path

from logpipe.agg import count_by_level
from logpipe.filter import by_level
from logpipe.parse import parse_line
from logpipe.pipeline import run
from logpipe.report import to_markdown


def test_parse_ok() -> None:
    r = parse_line("2026-01-02T03:04:05 INFO boot ok")
    assert r is not None
    assert r["level"] == "INFO"
    assert r["message"] == "boot ok"
    assert r["ts"].startswith("2026-")


def test_parse_bad() -> None:
    assert parse_line("nope") is None
    assert parse_line("") is None


def test_filter_and_agg() -> None:
    rows = [
        parse_line("2026-01-02T00:00:00 DEBUG d"),
        parse_line("2026-01-02T00:00:01 INFO i"),
        parse_line("2026-01-02T00:00:02 ERROR e"),
    ]
    rows = [r for r in rows if r]
    kept = by_level(rows, "INFO")
    assert all(r["level"] in ("INFO", "WARN", "ERROR") for r in kept)
    counts = count_by_level(kept)
    assert counts.get("INFO") == 1
    assert counts.get("ERROR") == 1
    assert "DEBUG" not in counts


def test_report_and_pipeline(tmp_path: Path) -> None:
    p = tmp_path / "a.log"
    p.write_text(
        "2026-01-02T00:00:00 DEBUG noise\n"
        "2026-01-02T00:00:01 WARN care\n"
        "2026-01-02T00:00:02 ERROR bad\n",
        encoding="utf-8",
    )
    md = run(p, min_level="WARN")
    assert "WARN" in md and "ERROR" in md
    assert "DEBUG" not in md or md.count("DEBUG") == 0
    assert "care" not in md  # report is counts, not raw messages
    # counts style: at least level names
    assert to_markdown({"WARN": 1, "ERROR": 1})
