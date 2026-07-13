# Task: Retry with exponential backoff

## API (`retrykit.core`)

```python
def retry_call(fn, *, attempts: int, base_delay: float, exceptions=(Exception,), sleep_fn=None, now_fn=None):
    # calls fn until success or attempts exhausted
    # delay between tries: base_delay * 2**(i) for i=0.. 
    # sleep_fn(seconds) used instead of time.sleep
    # returns fn() result; if all fail, re-raises last exception
```

Rules: `attempts >= 1` else ValueError. On success do not sleep after last success.

## Done when pytest green.
