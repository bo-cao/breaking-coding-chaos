"""Ledger book — intentional bugs for the benchmark scaffold."""

from .account import Account


class Book:
    def __init__(self) -> None:
        self._accounts: dict[str, Account] = {}

    def open(self, account_id: str) -> None:
        if account_id in self._accounts:
            raise ValueError("exists")
        self._accounts[account_id] = Account(account_id)

    def balance(self, account_id: str) -> int:
        return self._get(account_id).balance

    def post(self, debit_id: str, credit_id: str, amount: int) -> None:
        # BUG: does not validate amount; order of apply wrong for invariant helpers
        d = self._get(debit_id)
        c = self._get(credit_id)
        d.apply("debit", amount)
        c.apply("credit", amount)

    def transfer(self, from_id: str, to_id: str, amount: int) -> None:
        # BUG: only credits destination
        self._get(to_id).apply("credit", amount)

    def statement(self, account_id: str) -> list[dict]:
        return self._get(account_id).statement()

    def _get(self, account_id: str) -> Account:
        if account_id not in self._accounts:
            raise ValueError("unknown account")
        return self._accounts[account_id]
