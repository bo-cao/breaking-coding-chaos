from __future__ import annotations
import csv
from pathlib import Path
import pytest
from csvjoin.core import join_csv

def _w(p: Path, rows: list[dict]):
    if not rows:
        p.write_text("", encoding="utf-8"); return
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

def test_inner(tmp_path: Path):
    a = tmp_path/"a.csv"; b = tmp_path/"b.csv"
    _w(a, [{"id":"1","n":"a"},{"id":"2","n":"b"}])
    _w(b, [{"id":"2","x":"X"},{"id":"3","x":"Y"}])
    rows = join_csv(a, b, key="id", how="inner")
    assert len(rows)==1 and rows[0]["id"]=="2" and rows[0]["n"]=="b" and rows[0]["x"]=="X"

def test_left(tmp_path: Path):
    a = tmp_path/"a.csv"; b = tmp_path/"b.csv"
    _w(a, [{"id":"1","n":"a"}])
    _w(b, [{"id":"9","x":"Z"}])
    rows = join_csv(a, b, key="id", how="left")
    assert len(rows)==1 and rows[0]["x"]==""

def test_bad_how(tmp_path: Path):
    a = tmp_path/"a.csv"; b = tmp_path/"b.csv"
    _w(a, [{"id":"1"}]); _w(b, [{"id":"1"}])
    with pytest.raises(ValueError):
        join_csv(a, b, key="id", how="outer")

def test_missing_key(tmp_path: Path):
    a = tmp_path/"a.csv"; b = tmp_path/"b.csv"
    _w(a, [{"id":"1"}]); _w(b, [{"k":"1"}])
    with pytest.raises(ValueError):
        join_csv(a, b, key="id", how="inner")
