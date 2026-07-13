from __future__ import annotations
import pytest
from batcher.core import Batcher

class C:
    def __init__(self): self.t=0.0
    def __call__(self): return self.t
    def adv(self,d): self.t+=d

def test_size():
    b=Batcher(2, 100.0, now_fn=C())
    assert b.add(1) is None
    assert b.add(2)==[1,2]
    assert b.add(3) is None

def test_time():
    c=C(); b=Batcher(10, 1.0, now_fn=c)
    assert b.add("a") is None
    c.adv(1.0)
    assert b.add("b")==["a","b"]

def test_bad():
    with pytest.raises(ValueError):
        Batcher(0, 1.0)
