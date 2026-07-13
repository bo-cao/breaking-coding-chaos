from __future__ import annotations
from redact.core import redact_text

def test_email():
    assert "[EMAIL]" in redact_text("mail me@x.com ok")
    assert "me@x.com" not in redact_text("mail me@x.com ok")

def test_key():
    s=redact_text("tok sk-abcdefghij end")
    assert "[KEY]" in s and "sk-abcdefghij" not in s

def test_bearer():
    s=redact_text("Bearer abc.def-123")
    assert "Bearer [TOKEN]" in s
