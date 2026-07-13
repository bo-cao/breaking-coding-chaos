from __future__ import annotations
import pytest
from sliding.core import WindowAvg

def test_window():
    w=WindowAvg(3)
    assert w.add(3)==3
    assert w.add(6)==4.5
    assert abs(w.add(9)-6)<1e-9
    assert abs(w.add(3)-6)<1e-9  # 6,9,3

def test_bad():
    with pytest.raises(ValueError):
        WindowAvg(0)
