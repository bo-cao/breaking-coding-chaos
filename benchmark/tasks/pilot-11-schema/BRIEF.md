# Task: Dict schema validator

## API (`schemaval.core`)

```python
def validate(data: dict, schema: dict) -> list[str]:
    # returns list of error strings; empty if ok
```

Schema format:
```python
{"field": {"type": "str"|"int"|"bool", "required": True/False}}
```

- missing required → error containing field name
- wrong type → error containing field name
- unknown fields in data allowed

## Done when pytest green.
