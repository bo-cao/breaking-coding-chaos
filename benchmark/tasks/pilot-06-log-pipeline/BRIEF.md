# Task: Log analysis pipeline (long-horizon + recovery)

Build a **stdlib-only** multi-stage log pipeline. This case is intentionally multi-slice.

## Stages (sub-tasks)

1. **Parse** — `logpipe.parse.parse_line(line: str) -> dict | None`  
   Format: `YYYY-MM-DDTHH:MM:SS LEVEL message`  
   Example: `2026-01-02T03:04:05 INFO boot ok`  
   → `{"ts": "...", "level": "INFO", "message": "boot ok"}`  
   Bad lines → `None`.

2. **Filter** — `logpipe.filter.by_level(rows, min_level)` where order is  
   `DEBUG < INFO < WARN < ERROR`.

3. **Aggregate** — `logpipe.agg.count_by_level(rows) -> dict[str, int]`.

4. **Report** — `logpipe.report.to_markdown(counts: dict) -> str` containing each level present.

5. **Pipeline** — `logpipe.pipeline.run(path: str | Path, min_level: str = "INFO") -> str`  
   Read file, parse, filter, aggregate, return markdown report.

## Recovery protocol (operator)

This case is tagged **recovery: true**.

1. Start run as usual (BCC or without).
2. When roughly half the stages exist (e.g. parse+filter done, or ~50% of tests would pass), **hard-stop** the session.
3. New session, same workdir, only:  
   `Continue the work in this directory until pytest is green.`
4. Grade final tree only.

## Constraints

- Stdlib only.
- Package name `logpipe` with modules above.

## Done when

`python -m pytest -q` is green after the final session.
