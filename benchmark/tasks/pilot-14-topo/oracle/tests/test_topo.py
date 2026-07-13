from __future__ import annotations
import pytest
from topo.core import topo_sort

def test_simple():
    g={"a":[], "b":["a"], "c":["a"]}
    out=topo_sort(g)
    assert out.index("a")<out.index("b") and out.index("a")<out.index("c")

def test_stable_alpha():
    g={"b":[], "a":[]}
    assert topo_sort(g)==["a","b"]

def test_cycle():
    with pytest.raises(ValueError):
        topo_sort({"a":["b"],"b":["a"]})
