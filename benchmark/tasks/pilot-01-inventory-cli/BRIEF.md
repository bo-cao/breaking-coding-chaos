# Task: Inventory CLI

Build a **stdlib-only** Python inventory tool for a small warehouse.

## Goal

A working CLI module/package that persists stock to a JSON file and supports the operations below. **No third-party dependencies.**

## Sub-tasks (natural slices)

1. **Init & add** — create store file if missing; add SKU with name, qty ≥ 0.
2. **List & get** — list all items; get one SKU (missing → clear error, non-zero exit or exception policy documented by tests).
3. **Remove & adjust** — remove SKU; adjust quantity by delta (never go below 0).
4. **Export** — write a sorted JSON export snapshot to a path.

## Interface contract (must satisfy tests)

Implement package `inventory` with:

- `inventory.store.Store(path: str | Path)` 
  - `add(sku: str, name: str, qty: int) -> None`
  - `get(sku: str) -> dict` with keys `sku`, `name`, `qty`
  - `list_items() -> list[dict]`
  - `remove(sku: str) -> None`
  - `adjust(sku: str, delta: int) -> int`  # returns new qty
  - `export_json(path: str | Path) -> None`  # array sorted by sku

CLI optional; **library API is required** for pytest.

## Constraints

- Stdlib only.
- Persist after every mutating call.
- Invalid qty / missing SKU → `ValueError` (see tests).

## Done when

`python -m pytest -q` is green in the workdir.
