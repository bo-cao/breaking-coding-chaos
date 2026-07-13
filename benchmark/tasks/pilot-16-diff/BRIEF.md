# Task: Line diff summary

## API (`linediff.core`)

```python
def diff_summary(a: str, b: str) -> dict:
    # splitlines; return {"added": int, "removed": int, "same": int}
    # multiset line compare: count lines only in b as added, only in a as removed,
    # min frequency as same
```

## Done when pytest green.
