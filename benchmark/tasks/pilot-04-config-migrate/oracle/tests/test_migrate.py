"""Oracle for pilot-04-config-migrate."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from cfgmigrate.migrate import migrate_file, migrate_v1_to_v2, parse_v1


def test_parse_and_migrate(tmp_path: Path) -> None:
    p = tmp_path / "old.json"
    p.write_text(
        json.dumps(
            {"host": "h", "port": "90", "debug": "yes", "features": "x, y"}
        ),
        encoding="utf-8",
    )
    v1 = parse_v1(p)
    v2 = migrate_v1_to_v2(v1)
    assert v2["version"] == 2
    assert v2["server"] == {"host": "h", "port": 90}
    assert v2["debug"] is True
    assert v2["features"] == ["x", "y"]


def test_migrate_file(tmp_path: Path) -> None:
    src = tmp_path / "a.json"
    dst = tmp_path / "b.json"
    src.write_text(
        json.dumps(
            {"host": "localhost", "port": "8080", "debug": "0", "features": ""}
        ),
        encoding="utf-8",
    )
    migrate_file(src, dst)
    data = json.loads(dst.read_text(encoding="utf-8"))
    assert data["debug"] is False
    assert data["features"] == []
    assert data["server"]["port"] == 8080


def test_reject_v2(tmp_path: Path) -> None:
    src = tmp_path / "v2.json"
    src.write_text(json.dumps({"version": 2, "server": {"host": "h", "port": 1}, "debug": False, "features": []}), encoding="utf-8")
    with pytest.raises(ValueError):
        migrate_file(src, tmp_path / "out.json")


def test_debug_synonyms() -> None:
    for raw, expected in [("true", True), ("no", False), ("1", True), ("false", False)]:
        v2 = migrate_v1_to_v2(
            {"host": "h", "port": 1, "debug": raw, "features": "a"}
        )
        assert v2["debug"] is expected
