# Task: CSV join

Stdlib-only join of two CSV files on a key column.

## API (`csvjoin.core`)

```python
def join_csv(left_path, right_path, *, key: str, how: str = "inner") -> list[dict]:
    # how in {"inner", "left"}
    # rows are dicts; right columns overwritten on key collision except key itself
```

## Rules

- First row is header.
- `how="inner"`: only keys in both.
- `how="left"`: all left keys; missing right fields as `""`.
- Unknown `how` → `ValueError`.
- Missing key column → `ValueError`.

## Done when

`python -m pytest -q` green.
