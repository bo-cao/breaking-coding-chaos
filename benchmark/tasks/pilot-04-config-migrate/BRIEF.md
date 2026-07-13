# Task: Config migrate v1 → v2

Migrate legacy JSON config files to a new schema and validate.

## Schemas

**v1** (legacy):

```json
{
  "host": "localhost",
  "port": "8080",
  "debug": "yes",
  "features": "a,b,c"
}
```

**v2** (target):

```json
{
  "server": {"host": "localhost", "port": 8080},
  "debug": true,
  "features": ["a", "b", "c"],
  "version": 2
}
```

## Sub-tasks

1. **parse_v1** — load v1 dict from path; coerce types carefully (`port` int, `debug` bool from yes/no/true/false/1/0, features split on comma strip).
2. **migrate** — pure function `migrate_v1_to_v2(v1: dict) -> dict` producing valid v2.
3. **cli/module** — `migrate_file(src, dst)` writes v2 JSON with indent=2; reject already-v2 or unknown shape with `ValueError`.

Module: `cfgmigrate.migrate`.

## Constraints

- Stdlib only (`json`).
- Idempotency: migrating a file that already has `"version": 2` must raise.

## Done when

`python -m pytest -q` is green.
