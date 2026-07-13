from __future__ import annotations
from linediff.core import diff_summary

def test_basic():
    s=diff_summary("a\nb\n", "a\nc\n")
    assert s["same"]==1 and s["removed"]==1 and s["added"]==1

def test_identical():
    assert diff_summary("x\n", "x\n")=={"added":0,"removed":0,"same":1}
