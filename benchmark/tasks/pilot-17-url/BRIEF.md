# Task: Strict URL parts

## API (`urlparts.core`)

```python
def split_url(url: str) -> dict:
    # keys: scheme, host, port, path
    # port int or None; path default "/"
    # only http/https; else ValueError
```

Examples:
- `http://ex.com` → path `/`, port None
- `https://ex.com:8443/a` → port 8443 path `/a`

## Done when pytest green.
