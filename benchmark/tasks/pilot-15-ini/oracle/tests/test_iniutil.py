from __future__ import annotations
from iniutil.core import dump_ini, parse_ini

def test_parse():
    t="[s]\n#c\na=1\nb=2\n"
    d=parse_ini(t)
    assert d["s"]["a"]=="1" and d["s"]["b"]=="2"

def test_roundtrip():
    data={"b":{"z":"1"},"a":{"y":"2","x":"3"}}
    d2=parse_ini(dump_ini(data))
    assert d2==data
