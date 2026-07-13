# Task: Multi-step job runner (recovery)

Build package `jobrun` with stages:

1. `jobrun.parse.parse_jobs(text) -> list[dict]`  
   Lines `name:dep1,dep2` or `name:` ; strip spaces; skip empty/`#`.
2. `jobrun.plan.order_jobs(jobs) -> list[str]` topo by deps (deps before job); cycle ValueError; stable alpha among ready.
3. `jobrun.exec.run_jobs(names, runner) -> list[str]`  
   call `runner(name)` in order; collect return strings.
4. `jobrun.report.summarize(results: list[str]) -> str` join with newlines ending with newline.
5. `jobrun.pipeline.run(text, runner) -> str` wire all stages.

## Recovery

Operator: stop after parse+plan exist mid-way, new session Continue once (ad-hoc) / continue via throughline (BCC).

## Done when pytest green.
