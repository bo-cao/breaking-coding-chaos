# Task: LRU cache

## API (`lrucache.core`)

```python
class LRUCache:
    def __init__(self, capacity: int): ...
    def get(self, key): ...  # return value or None if missing
    def put(self, key, value) -> None: ...
```

- capacity >= 1 else ValueError
- Evict least-recently-used on overflow
- get/put both count as use

## Done when pytest green.
