from __future__ import annotations
import pytest
from lrucache.core import LRUCache

def test_basic():
    c=LRUCache(2)
    c.put("a",1); c.put("b",2)
    assert c.get("a")==1
    c.put("c",3)
    assert c.get("b") is None
    assert c.get("a")==1 and c.get("c")==3

def test_update_recency():
    c=LRUCache(2)
    c.put("a",1); c.put("b",2); c.get("a"); c.put("c",3)
    assert c.get("b") is None and c.get("a")==1

def test_bad_cap():
    with pytest.raises(ValueError):
        LRUCache(0)
