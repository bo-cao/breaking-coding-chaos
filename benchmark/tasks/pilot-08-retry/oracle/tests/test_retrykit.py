from __future__ import annotations
import pytest
from retrykit.core import retry_call

def test_success_first():
    assert retry_call(lambda: 7, attempts=3, base_delay=0.1) == 7

def test_retry_then_ok():
    n={"i":0}
    def f():
        n["i"]+=1
        if n["i"]<3: raise RuntimeError("x")
        return "ok"
    sleeps=[]
    assert retry_call(f, attempts=5, base_delay=0.5, sleep_fn=sleeps.append)=="ok"
    assert sleeps==[0.5, 1.0]

def test_exhausted():
    def f(): raise ValueError("no")
    with pytest.raises(ValueError):
        retry_call(f, attempts=2, base_delay=0.1, sleep_fn=lambda s: None)

def test_bad_attempts():
    with pytest.raises(ValueError):
        retry_call(lambda: 1, attempts=0, base_delay=0.1)
