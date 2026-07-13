# Pilot tasks (6)

| ID | Name | Shape | Recovery |
|----|------|-------|----------|
| [pilot-01](./pilot-01-inventory-cli/) | inventory-cli | Multi-slice stdlib CLI | no |
| [pilot-02](./pilot-02-broken-ledger/) | broken-ledger | Fix bugs + extend | no |
| [pilot-03](./pilot-03-token-bucket/) | token-bucket | Spec-hard rate limiter | no |
| [pilot-04](./pilot-04-config-migrate/) | config-migrate | Format migration + validation | no |
| [pilot-05](./pilot-05-yagni-stats/) | yagni-stats | Minimal stats tool (anti-bloat) | no |
| [pilot-06](./pilot-06-log-pipeline/) | log-pipeline | Multi-component + mid-stop | **yes** |

## How to run a case (operator)

1. Copy `scaffold/` → clean workdir (or empty dir + copy as specified in BRIEF).
2. Copy `oracle/tests` into workdir as `tests/` (agents may read tests — they are the contract).
3. Run arm:
   - **bcc**: skills on, empty project `AGENTS.md`, dual-loop; auto `APPROVE IMPLEMENT` at implement gate.
   - **without**: no BCC skills; short multi-turn demands only.
4. Grade: `cd workdir && python -m pytest -q` (and any CLI checks in BRIEF).
5. Optional: `ruff check .` if ruff installed.
6. Log row in `../scorecard.md`.

## Layout per case

```text
pilot-0N-name/
  meta.yaml      # tags, recovery flag
  BRIEF.md       # agent-facing goal (paste as task)
  scaffold/      # starting tree (may be empty marker)
  oracle/        # tests + grade notes
```
