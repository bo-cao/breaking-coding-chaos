# Task: Broken ledger

You inherit a **buggy** double-entry style mini ledger. Fix it, then extend it.

## Starting point

Scaffold provides `ledger/account.py` and `ledger/book.py` with known bugs.

## Sub-tasks

1. **Fix balance** — credits/debits must keep invariant: sum of all account balances == 0 after each posted entry (simple two-sided postings).
2. **Fix transfer** — `transfer(from, to, amount)` must be atomic for valid inputs; reject non-positive amounts and unknown accounts with `ValueError`.
3. **Add statement** — `statement(account_id) -> list[dict]` chronological list of `{op, amount, balance_after}` for that account only.

## Balance convention (tests)

- `debit` **increases** account `balance` by `amount`.
- `credit` **decreases** account `balance` by `amount`.
- After any successful `post` / `transfer`, sum of all balances must be **0**.
- `transfer(from, to, amount)` moves value: from decreases, to increases (same as credit from + debit to).

## Constraints

- Stdlib only; keep the public API names expected by tests.
- Do not invent a database.

## Done when

`python -m pytest -q` is green.
