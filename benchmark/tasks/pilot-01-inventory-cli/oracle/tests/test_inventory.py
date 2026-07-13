"""Oracle for pilot-01-inventory-cli."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from inventory.store import Store


def test_add_get_list(tmp_path: Path) -> None:
    s = Store(tmp_path / "stock.json")
    s.add("a1", "Apple", 3)
    s.add("b2", "Banana", 0)
    item = s.get("a1")
    assert item == {"sku": "a1", "name": "Apple", "qty": 3}
    skus = {x["sku"] for x in s.list_items()}
    assert skus == {"a1", "b2"}


def test_persist_reload(tmp_path: Path) -> None:
    path = tmp_path / "stock.json"
    s1 = Store(path)
    s1.add("x", "X", 1)
    s2 = Store(path)
    assert s2.get("x")["qty"] == 1


def test_remove_and_adjust(tmp_path: Path) -> None:
    s = Store(tmp_path / "stock.json")
    s.add("z", "Zed", 5)
    assert s.adjust("z", -2) == 3
    with pytest.raises(ValueError):
        s.adjust("z", -10)
    s.remove("z")
    with pytest.raises(ValueError):
        s.get("z")


def test_add_invalid_qty(tmp_path: Path) -> None:
    s = Store(tmp_path / "stock.json")
    with pytest.raises(ValueError):
        s.add("bad", "B", -1)


def test_export_sorted(tmp_path: Path) -> None:
    s = Store(tmp_path / "stock.json")
    s.add("m", "M", 1)
    s.add("a", "A", 2)
    out = tmp_path / "export.json"
    s.export_json(out)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert [d["sku"] for d in data] == ["a", "m"]


def test_export_empty(tmp_path: Path) -> None:
    s = Store(tmp_path / "stock.json")
    out = tmp_path / "empty.json"
    s.export_json(out)
    assert json.loads(out.read_text(encoding="utf-8")) == []


def test_add_overwrites_same_sku(tmp_path: Path) -> None:
    s = Store(tmp_path / "stock.json")
    s.add("a1", "Apple", 1)
    s.add("a1", "AppleX", 9)
    assert s.get("a1") == {"sku": "a1", "name": "AppleX", "qty": 9}


def test_remove_missing(tmp_path: Path) -> None:
    s = Store(tmp_path / "stock.json")
    with pytest.raises(ValueError):
        s.remove("nope")
