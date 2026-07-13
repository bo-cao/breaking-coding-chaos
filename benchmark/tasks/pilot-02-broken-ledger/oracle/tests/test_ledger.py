"""Oracle for pilot-02-broken-ledger."""
from __future__ import annotations

import pytest

from ledger import Book


def test_post_keeps_zero_sum() -> None:
    b = Book()
    b.open("cash")
    b.open("equity")
    b.post(debit_id="cash", credit_id="equity", amount=100)
    assert b.balance("cash") == 100
    assert b.balance("equity") == -100
    assert b.balance("cash") + b.balance("equity") == 0


def test_transfer_atomic() -> None:
    b = Book()
    b.open("a")
    b.open("b")
    b.post(debit_id="a", credit_id="b", amount=50)
    # a=50, b=-50
    b.transfer(from_id="a", to_id="b", amount=20)
    assert b.balance("a") == 30
    assert b.balance("b") == -30
    assert b.balance("a") + b.balance("b") == 0


def test_transfer_rejects_bad_amount() -> None:
    b = Book()
    b.open("a")
    b.open("b")
    with pytest.raises(ValueError):
        b.transfer("a", "b", 0)
    with pytest.raises(ValueError):
        b.transfer("a", "b", -5)


def test_unknown_account() -> None:
    b = Book()
    b.open("a")
    with pytest.raises(ValueError):
        b.balance("nope")


def test_statement() -> None:
    b = Book()
    b.open("a")
    b.open("b")
    b.post(debit_id="a", credit_id="b", amount=10)
    st = b.statement("a")
    assert len(st) >= 1
    assert st[-1]["balance_after"] == b.balance("a")
    assert "op" in st[-1] and "amount" in st[-1]


def test_post_rejects_non_positive() -> None:
    b = Book()
    b.open("a")
    b.open("b")
    with pytest.raises(ValueError):
        b.post("a", "b", 0)


def test_transfer_unknown() -> None:
    b = Book()
    b.open("a")
    with pytest.raises(ValueError):
        b.transfer("a", "ghost", 1)
