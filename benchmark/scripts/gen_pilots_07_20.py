"""Generate pilot-07..20 task packs (BRIEF, meta, oracle tests)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "tasks"


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.lstrip("\n"), encoding="utf-8")


def case(
    cid: str,
    title: str,
    recovery: bool,
    slices: int,
    brief: str,
    test: str,
    pkg_hint: str,
) -> None:
    d = ROOT / cid
    write(
        d / "meta.yaml",
        f"""id: {cid}
title: {title}
language: python
slices: {slices}
recovery: {str(recovery).lower()}
stdlib_only: true
package_hint: {pkg_hint}
""",
    )
    write(d / "BRIEF.md", brief)
    write(d / "scaffold" / ".gitkeep", "")
    write(d / "oracle" / "tests" / f"test_{pkg_hint}.py", test)
    print("wrote", cid)


# --- 07 csv join ---
case(
    "pilot-07-csv-join",
    "CSV join",
    False,
    3,
    """# Task: CSV join

Stdlib-only join of two CSV files on a key column.

## API (`csvjoin.core`)

```python
def join_csv(left_path, right_path, *, key: str, how: str = "inner") -> list[dict]:
    # how in {"inner", "left"}
    # rows are dicts; right columns overwritten on key collision except key itself
```

## Rules

- First row is header.
- `how="inner"`: only keys in both.
- `how="left"`: all left keys; missing right fields as `""`.
- Unknown `how` → `ValueError`.
- Missing key column → `ValueError`.

## Done when

`python -m pytest -q` green.
""",
    '''from __future__ import annotations
import csv
from pathlib import Path
import pytest
from csvjoin.core import join_csv

def _w(p: Path, rows: list[dict]):
    if not rows:
        p.write_text("", encoding="utf-8"); return
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

def test_inner(tmp_path: Path):
    a = tmp_path/"a.csv"; b = tmp_path/"b.csv"
    _w(a, [{"id":"1","n":"a"},{"id":"2","n":"b"}])
    _w(b, [{"id":"2","x":"X"},{"id":"3","x":"Y"}])
    rows = join_csv(a, b, key="id", how="inner")
    assert len(rows)==1 and rows[0]["id"]=="2" and rows[0]["n"]=="b" and rows[0]["x"]=="X"

def test_left(tmp_path: Path):
    a = tmp_path/"a.csv"; b = tmp_path/"b.csv"
    _w(a, [{"id":"1","n":"a"}])
    _w(b, [{"id":"9","x":"Z"}])
    rows = join_csv(a, b, key="id", how="left")
    assert len(rows)==1 and rows[0]["x"]==""

def test_bad_how(tmp_path: Path):
    a = tmp_path/"a.csv"; b = tmp_path/"b.csv"
    _w(a, [{"id":"1"}]); _w(b, [{"id":"1"}])
    with pytest.raises(ValueError):
        join_csv(a, b, key="id", how="outer")

def test_missing_key(tmp_path: Path):
    a = tmp_path/"a.csv"; b = tmp_path/"b.csv"
    _w(a, [{"id":"1"}]); _w(b, [{"k":"1"}])
    with pytest.raises(ValueError):
        join_csv(a, b, key="id", how="inner")
''',
    "csvjoin",
)

# --- 08 retry ---
case(
    "pilot-08-retry",
    "Retry backoff",
    False,
    2,
    """# Task: Retry with exponential backoff

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
""",
    '''from __future__ import annotations
import pytest
from retrykit.core import retry_call

def test_success_first():
    assert retry_call(lambda: 7, attempts=3, base_delay=0.1) == 7

def test_retry_then_ok():
    n={"i":0}
    def f():
        n["i"]+=1
        if n["i"]<3: raise RuntimeError("x")
        return "ok"
    sleeps=[]
    assert retry_call(f, attempts=5, base_delay=0.5, sleep_fn=sleeps.append)=="ok"
    assert sleeps==[0.5, 1.0]

def test_exhausted():
    def f(): raise ValueError("no")
    with pytest.raises(ValueError):
        retry_call(f, attempts=2, base_delay=0.1, sleep_fn=lambda s: None)

def test_bad_attempts():
    with pytest.raises(ValueError):
        retry_call(lambda: 1, attempts=0, base_delay=0.1)
''',
    "retrykit",
)

# --- 09 lru ---
case(
    "pilot-09-lru",
    "LRU cache",
    False,
    2,
    """# Task: LRU cache

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
""",
    '''from __future__ import annotations
import pytest
from lrucache.core import LRUCache

def test_basic():
    c=LRUCache(2)
    c.put("a",1); c.put("b",2)
    assert c.get("a")==1
    c.put("c",3)
    assert c.get("b") is None
    assert c.get("a")==1 and c.get("c")==3

def test_update_recency():
    c=LRUCache(2)
    c.put("a",1); c.put("b",2); c.get("a"); c.put("c",3)
    assert c.get("b") is None and c.get("a")==1

def test_bad_cap():
    with pytest.raises(ValueError):
        LRUCache(0)
''',
    "lrucache",
)

# --- 10 event bus ---
case(
    "pilot-10-event-bus",
    "Event bus",
    False,
    3,
    """# Task: In-process event bus

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
""",
    '''from __future__ import annotations
from eventbus.core import EventBus

def test_pub_sub():
    bus=EventBus(); got=[]
    bus.subscribe("t", lambda p: got.append(p))
    assert bus.publish("t", 1)==1
    assert got==[1]

def test_order_and_multi():
    bus=EventBus(); got=[]
    bus.subscribe("t", lambda p: got.append("a"+str(p)))
    bus.subscribe("t", lambda p: got.append("b"+str(p)))
    bus.publish("t", 2)
    assert got==["a2","b2"]

def test_unsub():
    bus=EventBus(); got=[]
    def f(p): got.append(p)
    bus.subscribe("t", f); bus.unsubscribe("t", f)
    assert bus.publish("t", 1)==0 and got==[]

def test_unknown():
    assert EventBus().publish("nope", 1)==0
''',
    "eventbus",
)

# --- 11 schema ---
case(
    "pilot-11-schema",
    "Schema validate",
    False,
    3,
    """# Task: Dict schema validator

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
""",
    '''from __future__ import annotations
from schemaval.core import validate

def test_ok():
    assert validate({"a":1}, {"a":{"type":"int","required":True}})==[]

def test_missing():
    errs=validate({}, {"a":{"type":"int","required":True}})
    assert any("a" in e for e in errs)

def test_type():
    errs=validate({"a":"x"}, {"a":{"type":"int","required":True}})
    assert any("a" in e for e in errs)

def test_optional():
    assert validate({}, {"a":{"type":"str","required":False}})==[]
''',
    "schemaval",
)

# --- 12 redact ---
case(
    "pilot-12-redact",
    "Secret redact",
    False,
    2,
    """# Task: Redact secrets

## API (`redact.core`)

```python
def redact_text(text: str) -> str:
```

Replace:
- emails → `[EMAIL]`
- strings looking like API keys `sk-[A-Za-z0-9]{8,}` → `[KEY]`
- `Bearer <token>` → `Bearer [TOKEN]`

## Done when pytest green.
""",
    '''from __future__ import annotations
from redact.core import redact_text

def test_email():
    assert "[EMAIL]" in redact_text("mail me@x.com ok")
    assert "me@x.com" not in redact_text("mail me@x.com ok")

def test_key():
    s=redact_text("tok sk-abcdefghij end")
    assert "[KEY]" in s and "sk-abcdefghij" not in s

def test_bearer():
    s=redact_text("Bearer abc.def-123")
    assert "Bearer [TOKEN]" in s
''',
    "redact",
)

# --- 13 sliding ---
case(
    "pilot-13-sliding",
    "Sliding window",
    False,
    2,
    """# Task: Sliding window average

## API (`sliding.core`)

```python
class WindowAvg:
    def __init__(self, size: int): ...
    def add(self, x: float) -> float:
        # returns average of last <=size values after adding x
```

size >= 1 else ValueError.

## Done when pytest green.
""",
    '''from __future__ import annotations
import pytest
from sliding.core import WindowAvg

def test_window():
    w=WindowAvg(3)
    assert w.add(3)==3
    assert w.add(6)==4.5
    assert abs(w.add(9)-6)<1e-9
    assert abs(w.add(3)-6)<1e-9  # 6,9,3

def test_bad():
    with pytest.raises(ValueError):
        WindowAvg(0)
''',
    "sliding",
)

# --- 14 topo ---
case(
    "pilot-14-topo",
    "Topo sort",
    False,
    3,
    """# Task: Dependency topological sort

## API (`topo.core`)

```python
def topo_sort(graph: dict[str, list[str]]) -> list[str]:
    # graph[node] = list of dependencies that must come BEFORE node
    # return stable order: among ready nodes, alphabetical
    # cycle → ValueError
```

## Done when pytest green.
""",
    '''from __future__ import annotations
import pytest
from topo.core import topo_sort

def test_simple():
    g={"a":[], "b":["a"], "c":["a"]}
    out=topo_sort(g)
    assert out.index("a")<out.index("b") and out.index("a")<out.index("c")

def test_stable_alpha():
    g={"b":[], "a":[]}
    assert topo_sort(g)==["a","b"]

def test_cycle():
    with pytest.raises(ValueError):
        topo_sort({"a":["b"],"b":["a"]})
''',
    "topo",
)

# --- 15 ini ---
case(
    "pilot-15-ini",
    "INI roundtrip",
    False,
    2,
    """# Task: Minimal INI

## API (`iniutil.core`)

```python
def parse_ini(text: str) -> dict[str, dict[str, str]]:
def dump_ini(data: dict[str, dict[str, str]]) -> str:
```

- sections `[name]`, `key=value` lines
- ignore empty lines and `#` comments
- dump: sections sorted, keys sorted within section; each section ends with newline

## Done when pytest green.
""",
    '''from __future__ import annotations
from iniutil.core import dump_ini, parse_ini

def test_parse():
    t="[s]\\n#c\\na=1\\nb=2\\n"
    d=parse_ini(t)
    assert d["s"]["a"]=="1" and d["s"]["b"]=="2"

def test_roundtrip():
    data={"b":{"z":"1"},"a":{"y":"2","x":"3"}}
    d2=parse_ini(dump_ini(data))
    assert d2==data
''',
    "iniutil",
)

# --- 16 diff ---
case(
    "pilot-16-diff",
    "Line diff",
    False,
    2,
    """# Task: Line diff summary

## API (`linediff.core`)

```python
def diff_summary(a: str, b: str) -> dict:
    # splitlines; return {"added": int, "removed": int, "same": int}
    # multiset line compare: count lines only in b as added, only in a as removed,
    # min frequency as same
```

## Done when pytest green.
""",
    '''from __future__ import annotations
from linediff.core import diff_summary

def test_basic():
    s=diff_summary("a\\nb\\n", "a\\nc\\n")
    assert s["same"]==1 and s["removed"]==1 and s["added"]==1

def test_identical():
    assert diff_summary("x\\n", "x\\n")=={"added":0,"removed":0,"same":1}
''',
    "linediff",
)

# --- 17 url ---
case(
    "pilot-17-url",
    "URL parts",
    False,
    2,
    """# Task: Strict URL parts

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
""",
    '''from __future__ import annotations
import pytest
from urlparts.core import split_url

def test_basic():
    d=split_url("http://ex.com")
    assert d=={"scheme":"http","host":"ex.com","port":None,"path":"/"}

def test_port_path():
    d=split_url("https://ex.com:8443/a/b")
    assert d["scheme"]=="https" and d["port"]==8443 and d["path"]=="/a/b"

def test_bad_scheme():
    with pytest.raises(ValueError):
        split_url("ftp://x")
''',
    "urlparts",
)

# --- 18 pq ---
case(
    "pilot-18-priority-queue",
    "Priority queue",
    False,
    2,
    """# Task: Stable priority queue

## API (`pq.core`)

```python
class PriorityQueue:
    def push(self, item, priority: int) -> None: ...
    def pop(self):
        # lowest priority first; ties: FIFO
        # empty → IndexError
```

## Done when pytest green.
""",
    '''from __future__ import annotations
import pytest
from pq.core import PriorityQueue

def test_order():
    q=PriorityQueue()
    q.push("b", 2); q.push("a", 1); q.push("c", 1)
    assert q.pop()=="a" and q.pop()=="c" and q.pop()=="b"

def test_empty():
    with pytest.raises(IndexError):
        PriorityQueue().pop()
''',
    "pq",
)

# --- 19 batcher ---
case(
    "pilot-19-batcher",
    "Batcher",
    False,
    3,
    """# Task: Size/time batcher

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
""",
    '''from __future__ import annotations
import pytest
from batcher.core import Batcher

class C:
    def __init__(self): self.t=0.0
    def __call__(self): return self.t
    def adv(self,d): self.t+=d

def test_size():
    b=Batcher(2, 100.0, now_fn=C())
    assert b.add(1) is None
    assert b.add(2)==[1,2]
    assert b.add(3) is None

def test_time():
    c=C(); b=Batcher(10, 1.0, now_fn=c)
    assert b.add("a") is None
    c.adv(1.0)
    assert b.add("b")==["a","b"]

def test_bad():
    with pytest.raises(ValueError):
        Batcher(0, 1.0)
''',
    "batcher",
)

# --- 20 job runner recovery ---
case(
    "pilot-20-job-runner",
    "Job runner recovery",
    True,
    5,
    """# Task: Multi-step job runner (recovery)

Build package `jobrun` with stages:

1. `jobrun.parse.parse_jobs(text) -> list[dict]`  
   Lines `name:dep1,dep2` or `name:` ; strip spaces; skip empty/`#`.
2. `jobrun.plan.order_jobs(jobs) -> list[str]` topo by deps (deps before job); cycle ValueError; stable alpha among ready.
3. `jobrun.exec.run_jobs(names, runner) -> list[str]`  
   call `runner(name)` in order; collect return strings.
4. `jobrun.report.summarize(results: list[str]) -> str` join with newlines ending with newline.
5. `jobrun.pipeline.run(text, runner) -> str` wire all stages.

## Recovery

Operator: stop after parse+plan exist mid-way, new session Continue once (ad-hoc) / continue via throughline (BCC).

## Done when pytest green.
""",
    '''from __future__ import annotations
import pytest
from jobrun.parse import parse_jobs
from jobrun.plan import order_jobs
from jobrun.exec import run_jobs
from jobrun.report import summarize
from jobrun.pipeline import run

def test_parse():
    jobs=parse_jobs("b:a\\na:\\n#c\\n")
    names={j["name"] for j in jobs}
    assert names=={"a","b"}
    b=[j for j in jobs if j["name"]=="b"][0]
    assert b["deps"]==["a"]

def test_order():
    jobs=[{"name":"b","deps":["a"]},{"name":"a","deps":[]},{"name":"c","deps":["a"]}]
    assert order_jobs(jobs)[0]=="a"

def test_cycle():
    with pytest.raises(ValueError):
        order_jobs([{"name":"a","deps":["b"]},{"name":"b","deps":["a"]}])

def test_pipeline():
    text="b:a\\na:\\n"
    out=run(text, lambda n: f"ok-{n}")
    assert out=="ok-a\\nok-b\\n"
''',
    "jobrun",
)

print("done", len(list(ROOT.glob("pilot-*"))))
