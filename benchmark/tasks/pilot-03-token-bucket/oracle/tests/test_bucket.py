"""Oracle for pilot-03-token-bucket."""
from __future__ import annotations

import pytest

from ratelimit.bucket import KeyedLimiter, TokenBucket


class Clock:
    def __init__(self) -> None:
        self.t = 0.0

    def __call__(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt


def test_rejects_bad_ctor() -> None:
    with pytest.raises(ValueError):
        TokenBucket(0, 1)
    with pytest.raises(ValueError):
        TokenBucket(1, 0)


def test_allow_and_block() -> None:
    clk = Clock()
    b = TokenBucket(1.0, 2.0, now_fn=clk)
    assert b.allow(1) is True
    assert b.allow(1) is True
    assert b.allow(1) is False


def test_refill() -> None:
    clk = Clock()
    b = TokenBucket(2.0, 2.0, now_fn=clk)
    assert b.allow(2) is True
    assert b.allow(1) is False
    clk.advance(0.5)  # +1 token
    assert b.allow(1) is True


def test_keyed_independent() -> None:
    clk = Clock()
    lim = KeyedLimiter(1.0, 1.0, now_fn=clk)
    assert lim.allow("a") is True
    assert lim.allow("a") is False
    assert lim.allow("b") is True


def test_stats() -> None:
    clk = Clock()
    lim = KeyedLimiter(1.0, 5.0, now_fn=clk)
    lim.allow("k", 2)
    st = lim.stats("k")
    assert st["capacity"] == 5.0
    assert 2.5 <= st["tokens"] <= 3.5  # ~3 remaining


def test_now_fn_is_keyword_only() -> None:
    clk = Clock()
    # positional third arg must not silently become now_fn
    with pytest.raises(TypeError):
        TokenBucket(1.0, 1.0, clk)  # type: ignore[misc]


def test_no_consume_on_reject() -> None:
    clk = Clock()
    b = TokenBucket(1.0, 1.0, now_fn=clk)
    assert b.allow(1) is True
    assert b.allow(1) is False
    clk.advance(0.0)
    assert b.allow(1) is False  # still empty; no free token
    clk.advance(1.0)
    assert b.allow(1) is True
