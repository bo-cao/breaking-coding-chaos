"""Single account — intentional bugs for the benchmark scaffold."""


class Account:
    def __init__(self, account_id: str) -> None:
        self.id = account_id
        self.balance = 0
        self._history: list[dict] = []

    def apply(self, op: str, amount: int) -> None:
        # BUG: credit and debit both add
        if op not in ("credit", "debit"):
            raise ValueError(f"bad op {op}")
        self.balance += amount
        self._history.append(
            {"op": op, "amount": amount, "balance_after": self.balance}
        )

    def statement(self) -> list[dict]:
        return list(self._history)
