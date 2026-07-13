# Task: Stable priority queue

## API (`pq.core`)

```python
class PriorityQueue:
    def push(self, item, priority: int) -> None: ...
    def pop(self):
        # lowest priority first; ties: FIFO
        # empty → IndexError
```

## Done when pytest green.
