# Task: Size/time batcher

## API (`batcher.core`)

```python
class Batcher:
    def __init__(self, max_size: int, max_interval: float, *, now_fn=None): ...
    def add(self, item) -> list | None:
        # append item; if batch full by size OR interval since first item in batch,
        # return batch list and reset; else None
```

max_size>=1, max_interval>0 else ValueError. now_fn defaults time.monotonic.

## Done when pytest green.
