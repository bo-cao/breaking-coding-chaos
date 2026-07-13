# Task: Sliding window average

## API (`sliding.core`)

```python
class WindowAvg:
    def __init__(self, size: int): ...
    def add(self, x: float) -> float:
        # returns average of last <=size values after adding x
```

size >= 1 else ValueError.

## Done when pytest green.
