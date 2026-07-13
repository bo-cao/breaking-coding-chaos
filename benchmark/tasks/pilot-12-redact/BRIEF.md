# Task: Redact secrets

## API (`redact.core`)

```python
def redact_text(text: str) -> str:
```

Replace:
- emails → `[EMAIL]`
- strings looking like API keys `sk-[A-Za-z0-9]{8,}` → `[KEY]`
- `Bearer <token>` → `Bearer [TOKEN]`

## Done when pytest green.
