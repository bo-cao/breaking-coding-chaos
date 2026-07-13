# Task: Minimal INI

## API (`iniutil.core`)

```python
def parse_ini(text: str) -> dict[str, dict[str, str]]:
def dump_ini(data: dict[str, dict[str, str]]) -> str:
```

- sections `[name]`, `key=value` lines
- ignore empty lines and `#` comments
- dump: sections sorted, keys sorted within section; each section ends with newline

## Done when pytest green.
