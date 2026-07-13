from __future__ import annotations
from eventbus.core import EventBus

def test_pub_sub():
    bus=EventBus(); got=[]
    bus.subscribe("t", lambda p: got.append(p))
    assert bus.publish("t", 1)==1
    assert got==[1]

def test_order_and_multi():
    bus=EventBus(); got=[]
    bus.subscribe("t", lambda p: got.append("a"+str(p)))
    bus.subscribe("t", lambda p: got.append("b"+str(p)))
    bus.publish("t", 2)
    assert got==["a2","b2"]

def test_unsub():
    bus=EventBus(); got=[]
    def f(p): got.append(p)
    bus.subscribe("t", f); bus.unsubscribe("t", f)
    assert bus.publish("t", 1)==0 and got==[]

def test_unknown():
    assert EventBus().publish("nope", 1)==0
