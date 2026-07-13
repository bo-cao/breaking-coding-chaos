# Task: Token bucket rate limiter

Implement a **stdlib-only** token-bucket rate limiter used by an API gateway simulation.

## Sub-tasks

1. **Core bucket** — `TokenBucket(rate_per_sec: float, capacity: float)` with `allow(tokens: float = 1.0) -> bool` and deterministic refill using an injectable clock.
2. **Multi-key** — `KeyedLimiter` maps string keys → independent buckets with the same rate/capacity defaults.
3. **Snapshot** — `stats(key: str) -> dict` with `tokens` (approx remaining) and `capacity`.

## Interface

```python
class TokenBucket:
    def __init__(self, rate_per_sec: float, capacity: float, *, now_fn=None): ...
    def allow(self, tokens: float = 1.0) -> bool: ...

class KeyedLimiter:
    def __init__(self, rate_per_sec: float, capacity: float, *, now_fn=None): ...
    def allow(self, key: str, tokens: float = 1.0) -> bool: ...
    def stats(self, key: str) -> dict: ...
```

`now_fn` defaults to `time.monotonic` and must be used for all time reads so tests can freeze time.

## Rules

- Refill: tokens increase by `rate_per_sec * elapsed`, capped at `capacity`.
- `allow` consumes tokens only if enough are available; otherwise return `False` without consuming.
- Reject non-positive rate/capacity/tokens with `ValueError`.
- Stdlib only. Module path: `ratelimit.bucket`.

## Done when

`python -m pytest -q` is green.
