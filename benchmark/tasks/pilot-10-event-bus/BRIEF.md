# Task: In-process event bus

## API (`eventbus.core`)

```python
class EventBus:
    def subscribe(self, topic: str, fn) -> None: ...
    def unsubscribe(self, topic: str, fn) -> None: ...
    def publish(self, topic: str, payload) -> int:
        # returns number of handlers called
```

- Multiple handlers per topic; order = subscribe order
- unsubscribe missing is no-op
- publish unknown topic returns 0

## Done when pytest green.
