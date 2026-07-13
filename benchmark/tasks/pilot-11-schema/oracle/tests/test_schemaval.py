from __future__ import annotations
from schemaval.core import validate

def test_ok():
    assert validate({"a":1}, {"a":{"type":"int","required":True}})==[]

def test_missing():
    errs=validate({}, {"a":{"type":"int","required":True}})
    assert any("a" in e for e in errs)

def test_type():
    errs=validate({"a":"x"}, {"a":{"type":"int","required":True}})
    assert any("a" in e for e in errs)

def test_optional():
    assert validate({}, {"a":{"type":"str","required":False}})==[]
