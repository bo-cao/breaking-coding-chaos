from __future__ import annotations
import pytest
from urlparts.core import split_url

def test_basic():
    d=split_url("http://ex.com")
    assert d=={"scheme":"http","host":"ex.com","port":None,"path":"/"}

def test_port_path():
    d=split_url("https://ex.com:8443/a/b")
    assert d["scheme"]=="https" and d["port"]==8443 and d["path"]=="/a/b"

def test_bad_scheme():
    with pytest.raises(ValueError):
        split_url("ftp://x")
