from __future__ import annotations
import pytest
from pq.core import PriorityQueue

def test_order():
    q=PriorityQueue()
    q.push("b", 2); q.push("a", 1); q.push("c", 1)
    assert q.pop()=="a" and q.pop()=="c" and q.pop()=="b"

def test_empty():
    with pytest.raises(IndexError):
        PriorityQueue().pop()
