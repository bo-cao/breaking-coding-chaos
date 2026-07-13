# Task: YAGNI line stats

Compute simple text stats. **Do the minimum that passes tests.**

## Required

Module `linestats.core` with:

```python
def summarize(path: str | Path) -> dict:
    # returns:
    # {
    #   "lines": int,           # total lines
    #   "non_empty": int,       # lines with strip() != ""
    #   "words": int,           # whitespace-separated tokens
    #   "max_line_len": int,    # max len of raw line without trailing \\n
    # }
```

CLI optional.

## Anti-goals (will fail or score dirty)

- No third-party packages.
- Do **not** add plugins, async servers, class hierarchies, or config frameworks.
- Oracle also checks: no more than **3** `.py` files under the package root `linestats/` (including `__init__.py`).

## Done when

`python -m pytest -q` is green.
