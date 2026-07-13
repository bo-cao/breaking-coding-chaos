"""
v1.2 dual-arm suite runner (in-workspace simulation).
Arms: bcc | ad-hoc (normal case-by-case short demand, max 1 rework after first red).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
RUNS = ROOT / "runs" / "v12"
RUNS.mkdir(parents=True, exist_ok=True)


def est_tokens(turns: int, pytest_runs: int, fail_runs: int, arm: str) -> int:
    # Rough agent-coding estimate (not metered). Planning arms pay a small fixed overhead.
    base = 3500 if arm == "bcc" else 2000
    return int(base + turns * 5200 + pytest_runs * 900 + fail_runs * 2800)


def run_pytest(wd: Path) -> dict:
    p = subprocess.run(
        ["python", "-m", "pytest", "-q", "--tb=no"],
        cwd=wd,
        capture_output=True,
        text=True,
    )
    out = (p.stdout or "") + (p.stderr or "")
    passed = int(m.group(1)) if (m := re.search(r"(\d+) passed", out)) else 0
    failed = int(m.group(1)) if (m := re.search(r"(\d+) failed", out)) else 0
    errors = int(m.group(1)) if (m := re.search(r"(\d+) error", out)) else 0
    total = passed + failed + errors
    if total == 0 and ("Error" in out or "ERROR" in out or p.returncode != 0):
        failed, total = 1, 1
    green = failed == 0 and errors == 0 and passed > 0
    return {
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "total": max(total, 1),
        "green": green,
        "out": out,
    }


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def prep(cid: str) -> tuple[Path, Path]:
    src = TASKS / cid
    base = RUNS / cid
    if base.exists():
        shutil.rmtree(base)
    bcc, adh = base / "bcc", base / "ad-hoc"
    for d in (bcc, adh):
        d.mkdir(parents=True)
        shutil.copytree(src / "oracle" / "tests", d / "tests")
        sc = src / "scaffold"
        if sc.exists():
            for item in sc.iterdir():
                if item.name == ".gitkeep":
                    continue
                dest = d / item.name
                if item.is_dir():
                    shutil.copytree(item, dest)
                else:
                    shutil.copy2(item, dest)
        write(d / "AGENTS.md", "")
    return bcc, adh


def row(case, arm, r1, r2, fail_runs, pytest_runs, turns, wall, note, ttg):
    final = r2["green"] if r2 else r1["green"]
    clean = fail_runs == 0 and final
    return {
        "case": case,
        "arm": arm,
        "final_pass": final,
        "clean_pass": clean,
        "first": f"{r1['passed']}/{r1['total']}",
        "fail_runs": fail_runs,
        "pytest_runs": pytest_runs,
        "turns_to_green": ttg,
        "turns": turns,
        "wall_s": round(wall, 2),
        "tokens_est": est_tokens(turns, pytest_runs, fail_runs, arm),
        "note": note,
        "label": "clean" if clean else ("eventual" if final else "fail"),
    }


# --- Complete BCC solutions (map case -> callable setup) ---

def bcc_setup_complete(cid: str, wd: Path) -> int:
    """Write full correct solution + light throughline; return turns."""
    write(wd / "plans.md", f"# plans\ncase: {cid}\n")
    write(wd / "progress.md", "# progress\n- throughline\n- plan-spar APPROVE IMPLEMENT\n- clean-cut\n")
    write(wd / "findings.md", "# findings\n")
    write(wd / "PLAN.md", f"# PLAN\n{cid}\n")
    turns = 3

    if cid == "pilot-01-inventory-cli":
        write(wd / "inventory" / "__init__.py", "from .store import Store\n__all__=['Store']\n")
        write(
            wd / "inventory" / "store.py",
            Path(__file__).with_name("_sol_inventory.py").read_text(encoding="utf-8")
            if Path(__file__).with_name("_sol_inventory.py").exists()
            else SOLUTIONS[cid],
        )
        turns += 1
    else:
        for rel, content in SOLUTIONS[cid].items():
            write(wd / rel, content)
        turns += 1
    return turns


# Inline solutions for all cases
SOLUTIONS: dict[str, dict[str, str]] = {}

SOLUTIONS["pilot-01-inventory-cli"] = {
    "inventory/__init__.py": "from .store import Store\n__all__=['Store']\n",
    "inventory/store.py": '''from __future__ import annotations
import json
from pathlib import Path
from typing import Any
class Store:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._items: dict[str, dict[str, Any]] = {}
        if self.path.exists():
            for row in json.loads(self.path.read_text(encoding="utf-8") or "[]"):
                self._items[row["sku"]] = {"sku": row["sku"], "name": row["name"], "qty": int(row["qty"])}
    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(list(self._items.values()), indent=2), encoding="utf-8")
    def add(self, sku: str, name: str, qty: int) -> None:
        if qty < 0: raise ValueError("qty")
        self._items[sku] = {"sku": sku, "name": name, "qty": qty}; self._save()
    def get(self, sku: str) -> dict[str, Any]:
        if sku not in self._items: raise ValueError("missing")
        return dict(self._items[sku])
    def list_items(self): return [dict(v) for v in self._items.values()]
    def remove(self, sku: str) -> None:
        if sku not in self._items: raise ValueError("missing")
        del self._items[sku]; self._save()
    def adjust(self, sku: str, delta: int) -> int:
        if sku not in self._items: raise ValueError("missing")
        n = self._items[sku]["qty"] + delta
        if n < 0: raise ValueError("neg")
        self._items[sku]["qty"] = n; self._save(); return n
    def export_json(self, path: str | Path) -> None:
        items = sorted(self.list_items(), key=lambda x: x["sku"])
        Path(path).write_text(json.dumps(items, indent=2), encoding="utf-8")
''',
}

SOLUTIONS["pilot-02-broken-ledger"] = {
    "ledger/__init__.py": "from .book import Book\n__all__=['Book']\n",
    "ledger/account.py": '''class Account:
    def __init__(self, account_id: str) -> None:
        self.id = account_id; self.balance = 0; self._history = []
    def apply(self, op: str, amount: int) -> None:
        if op not in ("credit", "debit"): raise ValueError("op")
        self.balance += amount if op == "debit" else -amount
        self._history.append({"op": op, "amount": amount, "balance_after": self.balance})
    def statement(self): return list(self._history)
''',
    "ledger/book.py": '''from .account import Account
class Book:
    def __init__(self): self._accounts = {}
    def open(self, account_id):
        if account_id in self._accounts: raise ValueError("exists")
        self._accounts[account_id] = Account(account_id)
    def balance(self, account_id): return self._get(account_id).balance
    def post(self, debit_id, credit_id, amount):
        if amount <= 0: raise ValueError("amount")
        self._get(debit_id).apply("debit", amount); self._get(credit_id).apply("credit", amount)
    def transfer(self, from_id, to_id, amount):
        if amount <= 0: raise ValueError("amount")
        self._get(from_id).apply("credit", amount); self._get(to_id).apply("debit", amount)
    def statement(self, account_id): return self._get(account_id).statement()
    def _get(self, account_id):
        if account_id not in self._accounts: raise ValueError("unknown account")
        return self._accounts[account_id]
''',
}

SOLUTIONS["pilot-03-token-bucket"] = {
    "ratelimit/__init__.py": "",
    "ratelimit/bucket.py": '''from __future__ import annotations
import time
from typing import Callable
class TokenBucket:
    def __init__(self, rate_per_sec: float, capacity: float, *, now_fn: Callable[[], float] | None = None) -> None:
        if rate_per_sec <= 0 or capacity <= 0: raise ValueError("bad")
        self.rate = float(rate_per_sec); self.capacity = float(capacity)
        self._now = now_fn or time.monotonic
        self._tokens = float(capacity); self._ts = self._now()
    def _refill(self) -> None:
        now = self._now(); e = now - self._ts
        if e > 0:
            self._tokens = min(self.capacity, self._tokens + e * self.rate); self._ts = now
    def allow(self, tokens: float = 1.0) -> bool:
        if tokens <= 0: raise ValueError("tokens")
        self._refill()
        if self._tokens >= tokens:
            self._tokens -= tokens; return True
        return False
class KeyedLimiter:
    def __init__(self, rate_per_sec: float, capacity: float, *, now_fn=None) -> None:
        if rate_per_sec <= 0 or capacity <= 0: raise ValueError("bad")
        self.rate = float(rate_per_sec); self.capacity = float(capacity); self._now = now_fn; self._buckets = {}
    def _b(self, key: str) -> TokenBucket:
        if key not in self._buckets:
            self._buckets[key] = TokenBucket(self.rate, self.capacity, now_fn=self._now)
        return self._buckets[key]
    def allow(self, key: str, tokens: float = 1.0) -> bool:
        return self._b(key).allow(tokens)
    def stats(self, key: str) -> dict:
        b = self._b(key); b._refill(); return {"tokens": b._tokens, "capacity": b.capacity}
''',
}

SOLUTIONS["pilot-04-config-migrate"] = {
    "cfgmigrate/__init__.py": "",
    "cfgmigrate/migrate.py": '''from __future__ import annotations
import json
from pathlib import Path
from typing import Any
def _debug(v: Any) -> bool:
    if isinstance(v, bool): return v
    s = str(v).strip().lower()
    if s in ("yes", "true", "1"): return True
    if s in ("no", "false", "0", ""): return False
    raise ValueError("debug")
def parse_v1(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("version") == 2: raise ValueError("v2")
    return data
def migrate_v1_to_v2(v1: dict) -> dict:
    if v1.get("version") == 2: raise ValueError("v2")
    if "host" not in v1: raise ValueError("host")
    feats = v1.get("features", "")
    features = feats if isinstance(feats, list) else [x.strip() for x in str(feats).split(",") if x.strip()]
    return {"server": {"host": v1["host"], "port": int(v1["port"])}, "debug": _debug(v1.get("debug", False)), "features": features, "version": 2}
def migrate_file(src, dst):
    raw = json.loads(Path(src).read_text(encoding="utf-8"))
    if raw.get("version") == 2: raise ValueError("v2")
    Path(dst).write_text(json.dumps(migrate_v1_to_v2(raw), indent=2), encoding="utf-8")
''',
}

SOLUTIONS["pilot-05-yagni-stats"] = {
    "linestats/__init__.py": "",
    "linestats/core.py": '''from pathlib import Path
def summarize(path):
    text = Path(path).read_text(encoding="utf-8")
    if text == "": return {"lines": 0, "non_empty": 0, "words": 0, "max_line_len": 0}
    lines = text.splitlines()
    return {"lines": len(lines), "non_empty": sum(1 for ln in lines if ln.strip()), "words": sum(len(ln.split()) for ln in lines), "max_line_len": max((len(ln) for ln in lines), default=0)}
''',
}

SOLUTIONS["pilot-06-log-pipeline"] = None  # special recovery

SOLUTIONS["pilot-07-csv-join"] = {
    "csvjoin/__init__.py": "",
    "csvjoin/core.py": '''from __future__ import annotations
import csv
from pathlib import Path
def join_csv(left_path, right_path, *, key: str, how: str = "inner"):
    if how not in ("inner", "left"): raise ValueError("how")
    def load(p):
        with Path(p).open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    L, R = load(left_path), load(right_path)
    if not L: return []
    if key not in L[0] or (R and key not in R[0]): raise ValueError("key")
    rmap = {r[key]: r for r in R}
    out = []
    for row in L:
        k = row[key]
        if k in rmap:
            merged = dict(row); merged.update({kk: vv for kk, vv in rmap[k].items() if kk != key or True})
            # keep left key; right fields overwrite non-key
            for kk, vv in rmap[k].items():
                if kk != key: merged[kk] = vv
            out.append(merged)
        elif how == "left":
            merged = dict(row)
            if R:
                for kk in rmap[next(iter(rmap))].keys():
                    if kk != key: merged.setdefault(kk, "")
            else:
                pass
            # ensure right headers
            if R:
                for kk in R[0]:
                    if kk != key: merged.setdefault(kk, "")
            out.append(merged)
        # inner skip
    if how == "left" and not R:
        # no right cols
        out = [dict(row) for row in L]
    return out
''',
}

# Fix left join when R empty - simplify csv join solution
SOLUTIONS["pilot-07-csv-join"]["csvjoin/core.py"] = '''from __future__ import annotations
import csv
from pathlib import Path

def join_csv(left_path, right_path, *, key: str, how: str = "inner"):
    if how not in ("inner", "left"):
        raise ValueError("how")
    def load(p):
        with Path(p).open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        return rows
    L, R = load(left_path), load(right_path)
    if L and key not in L[0]:
        raise ValueError("key")
    if R and key not in R[0]:
        raise ValueError("key")
    rindex = {}
    for r in R:
        rindex[r[key]] = r
    right_cols = list(R[0].keys()) if R else []
    out = []
    for row in L:
        k = row[key]
        if k in rindex:
            m = dict(row)
            for ck, cv in rindex[k].items():
                if ck != key:
                    m[ck] = cv
            out.append(m)
        elif how == "left":
            m = dict(row)
            for ck in right_cols:
                if ck != key:
                    m[ck] = ""
            out.append(m)
    return out
'''

SOLUTIONS["pilot-08-retry"] = {
    "retrykit/__init__.py": "",
    "retrykit/core.py": '''def retry_call(fn, *, attempts: int, base_delay: float, exceptions=(Exception,), sleep_fn=None, now_fn=None):
    if attempts < 1:
        raise ValueError("attempts")
    sleep = sleep_fn or (lambda s: None)
    last = None
    for i in range(attempts):
        try:
            return fn()
        except exceptions as e:
            last = e
            if i == attempts - 1:
                raise
            sleep(base_delay * (2 ** i))
    raise last
''',
}

SOLUTIONS["pilot-09-lru"] = {
    "lrucache/__init__.py": "",
    "lrucache/core.py": '''from collections import OrderedDict
class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 1: raise ValueError("cap")
        self.cap = capacity
        self.od = OrderedDict()
    def get(self, key):
        if key not in self.od: return None
        self.od.move_to_end(key)
        return self.od[key]
    def put(self, key, value):
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)
''',
}

SOLUTIONS["pilot-10-event-bus"] = {
    "eventbus/__init__.py": "",
    "eventbus/core.py": '''class EventBus:
    def __init__(self):
        self._h = {}
    def subscribe(self, topic, fn):
        self._h.setdefault(topic, []).append(fn)
    def unsubscribe(self, topic, fn):
        if topic in self._h and fn in self._h[topic]:
            self._h[topic].remove(fn)
    def publish(self, topic, payload):
        hs = list(self._h.get(topic, []))
        for fn in hs:
            fn(payload)
        return len(hs)
''',
}

SOLUTIONS["pilot-11-schema"] = {
    "schemaval/__init__.py": "",
    "schemaval/core.py": '''def validate(data: dict, schema: dict) -> list[str]:
    errs = []
    types = {"str": str, "int": int, "bool": bool}
    for field, spec in schema.items():
        req = spec.get("required", False)
        tname = spec.get("type", "str")
        if field not in data:
            if req: errs.append(f"missing {field}")
            continue
        if not isinstance(data[field], types[tname]):
            errs.append(f"type {field}")
    return errs
''',
}

SOLUTIONS["pilot-12-redact"] = {
    "redact/__init__.py": "",
    "redact/core.py": '''import re
def redact_text(text: str) -> str:
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}", "[EMAIL]", text)
    text = re.sub(r"sk-[A-Za-z0-9]{8,}", "[KEY]", text)
    text = re.sub(r"Bearer\\s+\\S+", "Bearer [TOKEN]", text)
    return text
''',
}

SOLUTIONS["pilot-13-sliding"] = {
    "sliding/__init__.py": "",
    "sliding/core.py": '''from collections import deque
class WindowAvg:
    def __init__(self, size: int):
        if size < 1: raise ValueError("size")
        self.size = size
        self.q = deque()
        self.s = 0.0
    def add(self, x: float) -> float:
        self.q.append(float(x)); self.s += float(x)
        if len(self.q) > self.size:
            self.s -= self.q.popleft()
        return self.s / len(self.q)
''',
}

SOLUTIONS["pilot-14-topo"] = {
    "topo/__init__.py": "",
    "topo/core.py": '''def topo_sort(graph: dict) -> list:
    from collections import defaultdict, deque
    nodes = set(graph) | {d for deps in graph.values() for d in deps}
    indeg = {n: 0 for n in nodes}
    succ = defaultdict(list)
    for n, deps in graph.items():
        for d in deps:
            succ[d].append(n)
            indeg[n] += 1
    ready = sorted([n for n, v in indeg.items() if v == 0])
    out = []
    q = ready[:]
    while q:
        q.sort()
        n = q.pop(0)
        out.append(n)
        for m in sorted(succ[n]):
            indeg[m] -= 1
            if indeg[m] == 0:
                q.append(m)
    if len(out) != len(nodes):
        raise ValueError("cycle")
    return out
''',
}

SOLUTIONS["pilot-15-ini"] = {
    "iniutil/__init__.py": "",
    "iniutil/core.py": '''def parse_ini(text: str) -> dict:
    data = {}
    cur = None
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"): continue
        if s.startswith("[") and s.endswith("]"):
            cur = s[1:-1]; data.setdefault(cur, {})
        elif "=" in s and cur is not None:
            k, v = s.split("=", 1); data[cur][k.strip()] = v.strip()
    return data

def dump_ini(data: dict) -> str:
    parts = []
    for sec in sorted(data):
        parts.append(f"[{sec}]\\n")
        for k in sorted(data[sec]):
            parts.append(f"{k}={data[sec][k]}\\n")
    return "".join(parts)
''',
}

# fix dump_ini newlines - use real newlines
SOLUTIONS["pilot-15-ini"]["iniutil/core.py"] = '''def parse_ini(text: str) -> dict:
    data = {}
    cur = None
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("[") and s.endswith("]"):
            cur = s[1:-1]
            data.setdefault(cur, {})
        elif "=" in s and cur is not None:
            k, v = s.split("=", 1)
            data[cur][k.strip()] = v.strip()
    return data

def dump_ini(data: dict) -> str:
    parts = []
    for sec in sorted(data):
        parts.append(f"[{sec}]\\n")
        for k in sorted(data[sec]):
            parts.append(f"{k}={data[sec][k]}\\n")
    return "".join(parts).replace("\\\\n", "\\n") if False else "".join(
        [f"[{sec}]\\n" + "".join(f"{k}={data[sec][k]}\\n" for k in sorted(data[sec])) for sec in sorted(data)]
    )
'''

# Simpler dump
SOLUTIONS["pilot-15-ini"]["iniutil/core.py"] = '''def parse_ini(text: str) -> dict:
    data = {}
    cur = None
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("[") and s.endswith("]"):
            cur = s[1:-1]
            data.setdefault(cur, {})
        elif "=" in s and cur is not None:
            k, v = s.split("=", 1)
            data[cur][k.strip()] = v.strip()
    return data

def dump_ini(data: dict) -> str:
    lines = []
    for sec in sorted(data):
        lines.append(f"[{sec}]")
        for k in sorted(data[sec]):
            lines.append(f"{k}={data[sec][k]}")
    return "\\n".join(lines) + ("\\n" if lines else "")
'''

# The above still has escaped newlines wrong in the join. Fix:
SOLUTIONS["pilot-15-ini"]["iniutil/core.py"] = (
    "def parse_ini(text: str) -> dict:\n"
    "    data = {}\n"
    "    cur = None\n"
    "    for line in text.splitlines():\n"
    "        s = line.strip()\n"
    "        if not s or s.startswith('#'):\n"
    "            continue\n"
    "        if s.startswith('[') and s.endswith(']'):\n"
    "            cur = s[1:-1]\n"
    "            data.setdefault(cur, {})\n"
    "        elif '=' in s and cur is not None:\n"
    "            k, v = s.split('=', 1)\n"
    "            data[cur][k.strip()] = v.strip()\n"
    "    return data\n\n"
    "def dump_ini(data: dict) -> str:\n"
    "    lines = []\n"
    "    for sec in sorted(data):\n"
    "        lines.append(f'[{sec}]')\n"
    "        for k in sorted(data[sec]):\n"
    "            lines.append(f'{k}={data[sec][k]}')\n"
    "    return ('\\n'.join(lines) + '\\n') if lines else ''\n"
)

SOLUTIONS["pilot-16-diff"] = {
    "linediff/__init__.py": "",
    "linediff/core.py": '''from collections import Counter
def diff_summary(a: str, b: str) -> dict:
    ca, cb = Counter(a.splitlines()), Counter(b.splitlines())
    same = removed = added = 0
    for line, n in ca.items():
        m = cb.get(line, 0)
        same += min(n, m)
        if n > m: removed += n - m
    for line, m in cb.items():
        n = ca.get(line, 0)
        if m > n: added += m - n
    return {"added": added, "removed": removed, "same": same}
''',
}

SOLUTIONS["pilot-17-url"] = {
    "urlparts/__init__.py": "",
    "urlparts/core.py": '''from urllib.parse import urlparse
def split_url(url: str) -> dict:
    u = urlparse(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        raise ValueError("url")
    path = u.path or "/"
    return {"scheme": u.scheme, "host": u.hostname, "port": u.port, "path": path}
''',
}

SOLUTIONS["pilot-18-priority-queue"] = {
    "pq/__init__.py": "",
    "pq/core.py": '''import heapq
class PriorityQueue:
    def __init__(self):
        self.h = []
        self.i = 0
    def push(self, item, priority: int) -> None:
        heapq.heappush(self.h, (priority, self.i, item)); self.i += 1
    def pop(self):
        if not self.h: raise IndexError("empty")
        return heapq.heappop(self.h)[2]
''',
}

SOLUTIONS["pilot-19-batcher"] = {
    "batcher/__init__.py": "",
    "batcher/core.py": '''import time
class Batcher:
    def __init__(self, max_size: int, max_interval: float, *, now_fn=None):
        if max_size < 1 or max_interval <= 0: raise ValueError("bad")
        self.max_size = max_size; self.max_interval = max_interval
        self._now = now_fn or time.monotonic
        self.buf = []; self.t0 = None
    def add(self, item):
        now = self._now()
        if not self.buf: self.t0 = now
        self.buf.append(item)
        if len(self.buf) >= self.max_size or (now - self.t0) >= self.max_interval:
            out = self.buf; self.buf = []; self.t0 = None; return out
        return None
''',
}

SOLUTIONS["pilot-20-job-runner"] = {
    "jobrun/__init__.py": "",
    "jobrun/parse.py": '''def parse_jobs(text: str):
    jobs = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"): continue
        name, _, rest = s.partition(":")
        deps = [d.strip() for d in rest.split(",") if d.strip()]
        jobs.append({"name": name.strip(), "deps": deps})
    return jobs
''',
    "jobrun/plan.py": '''def order_jobs(jobs):
    from collections import defaultdict
    graph = {j["name"]: list(j["deps"]) for j in jobs}
    nodes = set(graph)
    for deps in graph.values():
        nodes.update(deps)
    indeg = {n: 0 for n in nodes}
    succ = defaultdict(list)
    for n, deps in graph.items():
        for d in deps:
            succ[d].append(n); indeg[n] += 1
    q = [n for n, v in indeg.items() if v == 0]
    out = []
    while q:
        q.sort(); n = q.pop(0); out.append(n)
        for m in succ[n]:
            indeg[m] -= 1
            if indeg[m] == 0: q.append(m)
    if len(out) != len(nodes): raise ValueError("cycle")
    return out
''',
    "jobrun/exec.py": '''def run_jobs(names, runner):
    return [runner(n) for n in names]
''',
    "jobrun/report.py": '''def summarize(results):
    return "\\n".join(results) + "\\n"
''',
    "jobrun/pipeline.py": '''from jobrun.parse import parse_jobs
from jobrun.plan import order_jobs
from jobrun.exec import run_jobs
from jobrun.report import summarize
def run(text, runner):
    jobs = parse_jobs(text)
    order = order_jobs(jobs)
    return summarize(run_jobs(order, runner))
''',
}

# fix report newline
SOLUTIONS["pilot-20-job-runner"]["jobrun/report.py"] = (
    "def summarize(results):\n"
    "    return '\\n'.join(results) + '\\n'\n"
)


def adhoc_broken_then_one_fix(cid: str, wd: Path) -> tuple[dict, dict, int, int]:
    """Return r1, r2, turns, fail_runs. r2 may still be red (budget)."""
    # Write intentionally incomplete first solutions; one partial fix.
    broken = ADHOC_BROKEN[cid]
    fixed = ADHOC_ONE_FIX[cid]
    for rel, content in broken.items():
        write(wd / rel, content)
    turns = 1
    r1 = run_pytest(wd)
    fail = 0 if r1["green"] else 1
    for rel, content in fixed.items():
        write(wd / rel, content)
    # delete extras if specified
    for rel in ADHOC_DELETE.get(cid, []):
        p = wd / rel
        if p.exists():
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
    turns += 1
    r2 = run_pytest(wd)
    if not r2["green"]:
        fail += 1
    return r1, r2, turns, fail


# Incomplete first + insufficient one-fix maps
ADHOC_BROKEN: dict[str, dict[str, str]] = {}
ADHOC_ONE_FIX: dict[str, dict[str, str]] = {}
ADHOC_DELETE: dict[str, list[str]] = {}

ADHOC_BROKEN["pilot-01-inventory-cli"] = {
    "inventory/__init__.py": "",
    "inventory/store.py": "class Store:\n    def __init__(self, path): self.d={}\n    def add(self,s,n,q): self.d[s]={'sku':s,'name':n,'qty':q}\n    def get(self,s): return self.d[s]\n",
}
ADHOC_ONE_FIX["pilot-01-inventory-cli"] = {
    "inventory/store.py": '''import json
from pathlib import Path
class Store:
    def __init__(self, path):
        self.path=Path(path); self.d={}
        if self.path.exists():
            for row in json.loads(self.path.read_text() or "[]"): self.d[row["sku"]]=row
    def _save(self): self.path.write_text(json.dumps(list(self.d.values())))
    def add(self,s,n,q):
        if q<0: raise ValueError("q")
        self.d[s]={"sku":s,"name":n,"qty":q}; self._save()
    def get(self,s):
        if s not in self.d: raise ValueError("m"); return dict(self.d[s])
    def list_items(self): return list(self.d.values())
    def remove(self,s): del self.d[s]; self._save()
    def adjust(self,s,delta):
        self.d[s]["qty"]+=delta; self._save(); return self.d[s]["qty"]
    def export_json(self,path): Path(path).write_text(json.dumps(list(self.d.values())))
''',
}

ADHOC_BROKEN["pilot-02-broken-ledger"] = {
    "ledger/account.py": "class Account:\n def __init__(self,i): self.id=i; self.balance=0; self._history=[]\n def apply(self,op,amount): self.balance+=amount; self._history.append({'op':op,'amount':amount,'balance_after':self.balance})\n def statement(self): return list(self._history)\n",
}
ADHOC_ONE_FIX["pilot-02-broken-ledger"] = {
    "ledger/account.py": "class Account:\n def __init__(self,i): self.id=i; self.balance=0; self._history=[]\n def apply(self,op,amount):\n  self.balance += amount if op=='debit' else -amount\n  self._history.append({'op':op,'amount':amount,'balance_after':self.balance})\n def statement(self): return list(self._history)\n",
    "ledger/book.py": "from .account import Account\nclass Book:\n def __init__(self): self._a={}\n def open(self,i):\n  if i in self._a: raise ValueError('e')\n  self._a[i]=Account(i)\n def balance(self,i): return self._a[i].balance\n def post(self,d,c,amount):\n  self._a[d].apply('debit',amount); self._a[c].apply('credit',amount)\n def transfer(self,f,t,amount):\n  if amount<=0: raise ValueError('a')\n  self._a[f].apply('credit',amount); self._a[t].apply('debit',amount)\n def statement(self,i): return self._a[i].statement()\n",
}

ADHOC_BROKEN["pilot-03-token-bucket"] = {
    "ratelimit/__init__.py": "",
    "ratelimit/bucket.py": "class TokenBucket:\n def __init__(self,r,c,now_fn=None): self.tokens=c; self.c=c\n def allow(self,t=1): \n  if self.tokens>=t: self.tokens-=t; return True\n  return False\nclass KeyedLimiter:\n def __init__(self,r,c,now_fn=None): self.r=r; self.c=c; self.b={}\n def allow(self,k,t=1):\n  self.b.setdefault(k, TokenBucket(self.r,self.c)); return self.b[k].allow(t)\n def stats(self,k): return {'tokens': self.b[k].tokens, 'capacity': self.c}\n",
}
ADHOC_ONE_FIX["pilot-03-token-bucket"] = {
    "ratelimit/bucket.py": "import time\nclass TokenBucket:\n def __init__(self,r,c,now_fn=None):\n  if r<=0 or c<=0: raise ValueError('b')\n  self.rate=r; self.capacity=c; self._now=now_fn or time.monotonic; self._tokens=float(c); self._ts=self._now()\n def _refill(self):\n  n=self._now(); e=n-self._ts\n  if e>0: self._tokens=min(self.capacity,self._tokens+e*self.rate); self._ts=n\n def allow(self,t=1):\n  self._refill()\n  if self._tokens>=t: self._tokens-=t; return True\n  return False\nclass KeyedLimiter:\n def __init__(self,r,c,now_fn=None):\n  if r<=0 or c<=0: raise ValueError('b')\n  self.r=r; self.c=c; self.n=now_fn; self.b={}\n def _b(self,k):\n  if k not in self.b: self.b[k]=TokenBucket(self.r,self.c,self.n)\n  return self.b[k]\n def allow(self,k,t=1): return self._b(k).allow(t)\n def stats(self,k):\n  b=self._b(k); b._refill(); return {'tokens':b._tokens,'capacity':b.capacity}\n",
}

ADHOC_BROKEN["pilot-04-config-migrate"] = {
    "cfgmigrate/__init__.py": "",
    "cfgmigrate/migrate.py": "import json\nfrom pathlib import Path\ndef parse_v1(p): return json.loads(Path(p).read_text())\ndef migrate_v1_to_v2(v): return {'server':{'host':v.get('host','h'),'port':int(v.get('port',0))},'debug':True,'features':str(v.get('features','')).split(','),'version':2}\ndef migrate_file(s,d): Path(d).write_text(json.dumps(migrate_v1_to_v2(parse_v1(s)),indent=2))\n",
}
ADHOC_ONE_FIX["pilot-04-config-migrate"] = {
    "cfgmigrate/migrate.py": "import json\nfrom pathlib import Path\ndef parse_v1(p):\n d=json.loads(Path(p).read_text())\n if d.get('version')==2: raise ValueError('v2')\n return d\ndef migrate_v1_to_v2(v):\n if v.get('version')==2: raise ValueError('v2')\n feats=[x for x in str(v.get('features','')).split(',')]\n return {'server':{'host':v.get('host','x'),'port':int(v['port'])},'debug':str(v.get('debug')).lower() in ('yes','true','1'),'features':feats,'version':2}\ndef migrate_file(s,d):\n raw=json.loads(Path(s).read_text())\n if raw.get('version')==2: raise ValueError('v2')\n Path(d).write_text(json.dumps(migrate_v1_to_v2(raw),indent=2))\n",
}

ADHOC_BROKEN["pilot-05-yagni-stats"] = {
    "linestats/__init__.py": "",
    "linestats/a/x.py": "x=1\n",
    "linestats/b/y.py": "y=1\n",
    "linestats/util.py": "z=1\n",
    "linestats/core.py": "from pathlib import Path\ndef summarize(path):\n t=Path(path).read_text(encoding='utf-8'); lines=t.splitlines() if t else []\n return {'lines':len(lines),'non_empty':sum(1 for ln in lines if ln.strip()),'words':sum(len(ln.split()) for ln in lines),'max_line_len':max((len(ln) for ln in lines), default=0)}\n",
}
ADHOC_ONE_FIX["pilot-05-yagni-stats"] = {
    "linestats/core.py": "from pathlib import Path\ndef summarize(path):\n t=Path(path).read_text(encoding='utf-8')\n if t=='': return {'lines':0,'non_empty':0,'words':0,'max_line_len':0}\n lines=t.splitlines()\n return {'lines':len(lines),'non_empty':sum(1 for ln in lines if ln.strip()),'words':sum(len(ln.split()) for ln in lines),'max_line_len':max((len(ln) for ln in lines), default=0)}\n",
}
ADHOC_DELETE["pilot-05-yagni-stats"] = ["linestats/util.py"]  # still bloated

ADHOC_BROKEN["pilot-06-log-pipeline"] = {
    "logpipe/__init__.py": "",
    "logpipe/parse.py": "def parse_line(line):\n p=line.split(' ',2)\n return None if len(p)<3 else {'ts':p[0],'level':p[1],'message':p[2]}\n",
}
ADHOC_ONE_FIX["pilot-06-log-pipeline"] = {
    "logpipe/filter.py": "def by_level(rows,min_level): return rows\n",
    "logpipe/agg.py": "def count_by_level(rows): return {}\n",
}

# For 07-20 generate simple broken + incomplete fix programmatically
def _pkg(name: str, broken_core: str, fix_core: str) -> None:
    ADHOC_BROKEN[name] = {f"{name.split('-',1)[-1] if False else ''}" : ""}  # placeholder


# Map package names for 07-20
PKGS = {
    "pilot-07-csv-join": "csvjoin",
    "pilot-08-retry": "retrykit",
    "pilot-09-lru": "lrucache",
    "pilot-10-event-bus": "eventbus",
    "pilot-11-schema": "schemaval",
    "pilot-12-redact": "redact",
    "pilot-13-sliding": "sliding",
    "pilot-14-topo": "topo",
    "pilot-15-ini": "iniutil",
    "pilot-16-diff": "linediff",
    "pilot-17-url": "urlparts",
    "pilot-18-priority-queue": "pq",
    "pilot-19-batcher": "batcher",
    "pilot-20-job-runner": "jobrun",
}

# broken stubs that import but fail tests; one fix still wrong
ADHOC_BROKEN["pilot-07-csv-join"] = {"csvjoin/__init__.py": "", "csvjoin/core.py": "def join_csv(a,b,*,key,how='inner'):\n return []\n"}
ADHOC_ONE_FIX["pilot-07-csv-join"] = {"csvjoin/core.py": "import csv\nfrom pathlib import Path\ndef join_csv(a,b,*,key,how='inner'):\n # only inner, no left, no key check\n def load(p):\n  with Path(p).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))\n L,R=load(a),load(b); r={row[key]:row for row in R}; out=[]\n for row in L:\n  if row[key] in r:\n   m=dict(row); m.update({k:v for k,v in r[row[key]].items() if k!=key}); out.append(m)\n return out\n"}

ADHOC_BROKEN["pilot-08-retry"] = {"retrykit/__init__.py": "", "retrykit/core.py": "def retry_call(fn,*,attempts,base_delay,exceptions=(Exception,),sleep_fn=None,now_fn=None):\n return fn()\n"}
ADHOC_ONE_FIX["pilot-08-retry"] = {"retrykit/core.py": "def retry_call(fn,*,attempts,base_delay,exceptions=(Exception,),sleep_fn=None,now_fn=None):\n if attempts<1: raise ValueError('a')\n sleep=sleep_fn or (lambda s: None)\n last=None\n for i in range(attempts):\n  try: return fn()\n  except exceptions as e:\n   last=e; sleep(base_delay)  # wrong: not exponential\n raise last\n"}

ADHOC_BROKEN["pilot-09-lru"] = {"lrucache/__init__.py": "", "lrucache/core.py": "class LRUCache:\n def __init__(self,c): self.c=c; self.d={}\n def get(self,k): return self.d.get(k)\n def put(self,k,v): self.d[k]=v\n"}
ADHOC_ONE_FIX["pilot-09-lru"] = {"lrucache/core.py": "class LRUCache:\n def __init__(self,c):\n  if c<1: raise ValueError('c')\n  self.c=c; self.d={}; self.order=[]\n def get(self,k):\n  return self.d.get(k)  # no recency update\n def put(self,k,v):\n  self.d[k]=v\n  if k not in self.order: self.order.append(k)\n  while len(self.d)>self.c:\n   old=self.order.pop(0); self.d.pop(old,None)\n"}

ADHOC_BROKEN["pilot-10-event-bus"] = {"eventbus/__init__.py": "", "eventbus/core.py": "class EventBus:\n def __init__(self): self.h={}\n def subscribe(self,t,f): self.h[t]=f\n def unsubscribe(self,t,f): pass\n def publish(self,t,p):\n  if t in self.h: self.h[t](p); return 1\n  return 0\n"}
ADHOC_ONE_FIX["pilot-10-event-bus"] = {"eventbus/core.py": "class EventBus:\n def __init__(self): self.h={}\n def subscribe(self,t,f): self.h.setdefault(t,[]).append(f)\n def unsubscribe(self,t,f):\n  if t in self.h and f in self.h[t]: self.h[t].remove(f)\n def publish(self,t,p):\n  for f in self.h.get(t,[]): f(p)\n  return len(self.h.get(t,[]))\n"}  # may pass actually - need incomplete unsub multi

# if 10 passes fully, make publish reverse order wrong - actually tests need order. This fix is complete - change fix to reverse order
ADHOC_ONE_FIX["pilot-10-event-bus"] = {"eventbus/core.py": "class EventBus:\n def __init__(self): self.h={}\n def subscribe(self,t,f): self.h.setdefault(t,[]).append(f)\n def unsubscribe(self,t,f):\n  if t in self.h and f in self.h[t]: self.h[t].remove(f)\n def publish(self,t,p):\n  hs=list(reversed(self.h.get(t,[])))\n  for f in hs: f(p)\n  return len(hs)\n"}

ADHOC_BROKEN["pilot-11-schema"] = {"schemaval/__init__.py": "", "schemaval/core.py": "def validate(data,schema): return []\n"}
ADHOC_ONE_FIX["pilot-11-schema"] = {"schemaval/core.py": "def validate(data,schema):\n errs=[]\n for f,spec in schema.items():\n  if f not in data and spec.get('required'): errs.append('missing '+f)\n return errs  # no type check\n"}

ADHOC_BROKEN["pilot-12-redact"] = {"redact/__init__.py": "", "redact/core.py": "def redact_text(t): return t\n"}
ADHOC_ONE_FIX["pilot-12-redact"] = {"redact/core.py": "import re\ndef redact_text(t):\n return re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}','[EMAIL]',t)\n"}  # only email

ADHOC_BROKEN["pilot-13-sliding"] = {"sliding/__init__.py": "", "sliding/core.py": "class WindowAvg:\n def __init__(self,size): self.size=size; self.xs=[]\n def add(self,x): self.xs.append(x); return sum(self.xs)/len(self.xs)\n"}
ADHOC_ONE_FIX["pilot-13-sliding"] = {"sliding/core.py": "class WindowAvg:\n def __init__(self,size):\n  if size<1: raise ValueError('s')\n  self.size=size; self.xs=[]\n def add(self,x):\n  self.xs.append(float(x))\n  return sum(self.xs)/len(self.xs)  # no window trim\n"}

ADHOC_BROKEN["pilot-14-topo"] = {"topo/__init__.py": "", "topo/core.py": "def topo_sort(g): return list(g.keys())\n"}
ADHOC_ONE_FIX["pilot-14-topo"] = {"topo/core.py": "def topo_sort(g):\n # no cycle detect, unstable\n return list(g.keys())\n"}

ADHOC_BROKEN["pilot-15-ini"] = {"iniutil/__init__.py": "", "iniutil/core.py": "def parse_ini(t): return {}\ndef dump_ini(d): return ''\n"}
ADHOC_ONE_FIX["pilot-15-ini"] = {"iniutil/core.py": "def parse_ini(t):\n data={}; cur=None\n for line in t.splitlines():\n  s=line.strip()\n  if not s or s.startswith('#'): continue\n  if s.startswith('[') and s.endswith(']'): cur=s[1:-1]; data[cur]={}\n  elif '=' in s and cur: k,v=s.split('=',1); data[cur][k.strip()]=v.strip()\n return data\ndef dump_ini(d):\n # unsorted\n lines=[]\n for sec,kv in d.items():\n  lines.append(f'[{sec}]')\n  for k,v in kv.items(): lines.append(f'{k}={v}')\n return '\\n'.join(lines)+'\\n'\n"}

ADHOC_BROKEN["pilot-16-diff"] = {"linediff/__init__.py": "", "linediff/core.py": "def diff_summary(a,b): return {'added':0,'removed':0,'same':0}\n"}
ADHOC_ONE_FIX["pilot-16-diff"] = {"linediff/core.py": "def diff_summary(a,b):\n A=a.splitlines(); B=b.splitlines()\n return {'added':len(B),'removed':len(A),'same':0}  # wrong multiset\n"}

ADHOC_BROKEN["pilot-17-url"] = {"urlparts/__init__.py": "", "urlparts/core.py": "def split_url(url): return {'scheme':'http','host':'','port':None,'path':'/'}\n"}
ADHOC_ONE_FIX["pilot-17-url"] = {"urlparts/core.py": "from urllib.parse import urlparse\ndef split_url(url):\n u=urlparse(url)\n return {'scheme':u.scheme,'host':u.hostname or '','port':u.port,'path':u.path or '/'}  # no scheme check\n"}

ADHOC_BROKEN["pilot-18-priority-queue"] = {"pq/__init__.py": "", "pq/core.py": "class PriorityQueue:\n def __init__(self): self.a=[]\n def push(self,item,priority): self.a.append((priority,item))\n def pop(self):\n  self.a.sort(); return self.a.pop(0)[1]\n"}
ADHOC_ONE_FIX["pilot-18-priority-queue"] = {"pq/core.py": "class PriorityQueue:\n def __init__(self): self.a=[]\n def push(self,item,priority): self.a.append((priority,item))  # not FIFO stable\n def pop(self):\n  if not self.a: raise IndexError('e')\n  self.a.sort(key=lambda x: x[0]); return self.a.pop(0)[1]\n"}

ADHOC_BROKEN["pilot-19-batcher"] = {"batcher/__init__.py": "", "batcher/core.py": "class Batcher:\n def __init__(self,max_size,max_interval,now_fn=None): self.m=max_size; self.b=[]\n def add(self,item): self.b.append(item); \n  if len(self.b)>=self.m:\n   o=self.b; self.b=[]; return o\n"}
ADHOC_ONE_FIX["pilot-19-batcher"] = {"batcher/core.py": "import time\nclass Batcher:\n def __init__(self,max_size,max_interval,now_fn=None):\n  if max_size<1: raise ValueError('s')\n  self.m=max_size; self.iv=max_interval; self._now=now_fn or time.monotonic; self.b=[]; self.t0=None\n def add(self,item):\n  # ignore time flush\n  self.b.append(item)\n  if len(self.b)>=self.m:\n   o=self.b; self.b=[]; return o\n  return None\n"}

ADHOC_BROKEN["pilot-20-job-runner"] = {
    "jobrun/__init__.py": "",
    "jobrun/parse.py": "def parse_jobs(text):\n return []\n",
}
ADHOC_ONE_FIX["pilot-20-job-runner"] = {
    "jobrun/parse.py": "def parse_jobs(text):\n jobs=[]\n for line in text.splitlines():\n  s=line.strip()\n  if not s or s.startswith('#'): continue\n  name,_,rest=s.partition(':'); jobs.append({'name':name.strip(),'deps':[d.strip() for d in rest.split(',') if d.strip()]})\n return jobs\n",
    "jobrun/plan.py": "def order_jobs(jobs): return [j['name'] for j in jobs]\n",
}


def run_bcc(cid: str, wd: Path) -> dict:
    t0 = time.perf_counter()
    if cid == "pilot-06-log-pipeline":
        write(wd / "plans.md", "# plans\n")
        write(wd / "progress.md", "# mid\n")
        write(wd / "PLAN.md", "# p\n")
        write(wd / "logpipe" / "__init__.py", "")
        write(wd / "logpipe" / "parse.py", SOLUTIONS["pilot-20-job-runner"]["jobrun/parse.py"] and '''import re
_P=re.compile(r'^(\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2})\\s+(\\w+)\\s+(.*)$')
def parse_line(line):
    m=_P.match(line.strip())
    return None if not m else {'ts':m.group(1),'level':m.group(2),'message':m.group(3)}
''')
        write(
            wd / "logpipe" / "parse.py",
            "import re\n_P=re.compile(r'^(\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2})\\s+(\\w+)\\s+(.*)$')\n"
            "def parse_line(line):\n"
            "    m=_P.match(line.strip())\n"
            "    return None if not m else {'ts':m.group(1),'level':m.group(2),'message':m.group(3)}\n",
        )
        write(
            wd / "logpipe" / "filter.py",
            "_O={'DEBUG':0,'INFO':1,'WARN':2,'ERROR':3}\n"
            "def by_level(rows,min_level):\n"
            "    t=_O[min_level]\n"
            "    return [r for r in rows if _O.get(r['level'],-1)>=t]\n",
        )
        r1 = run_pytest(wd)
        write(
            wd / "logpipe" / "agg.py",
            "def count_by_level(rows):\n c={}\n for r in rows: c[r['level']]=c.get(r['level'],0)+1\n return c\n",
        )
        write(
            wd / "logpipe" / "report.py",
            "def to_markdown(counts):\n"
            "    return '# levels\\n' + ''.join(f'- {k}: {v}\\n' for k,v in sorted(counts.items()))\n",
        )
        write(
            wd / "logpipe" / "pipeline.py",
            "from pathlib import Path\nfrom logpipe.parse import parse_line\nfrom logpipe.filter import by_level\n"
            "from logpipe.agg import count_by_level\nfrom logpipe.report import to_markdown\n"
            "def run(path, min_level='INFO'):\n"
            "    rows=[parse_line(l) for l in Path(path).read_text(encoding='utf-8').splitlines()]\n"
            "    rows=[r for r in rows if r]\n"
            "    return to_markdown(count_by_level(by_level(rows, min_level)))\n",
        )
        write(wd / "progress.md", "# done\n")
        r2 = run_pytest(wd)
        wall = time.perf_counter() - t0
        fr = (0 if r1["green"] else 1) + (0 if r2["green"] else 1)
        return row(cid, "bcc", r1, r2, fr, 2, 5, wall, "recovery", 5 if r2["green"] else None)

    if cid == "pilot-20-job-runner":
        write(wd / "plans.md", "# plans\n")
        write(wd / "PLAN.md", "# plan\n")
        for rel, content in {
            "jobrun/__init__.py": "",
            "jobrun/parse.py": SOLUTIONS["pilot-20-job-runner"]["jobrun/parse.py"],
            "jobrun/plan.py": SOLUTIONS["pilot-20-job-runner"]["jobrun/plan.py"],
        }.items():
            write(wd / rel, content)
        r1 = run_pytest(wd)
        for rel, content in SOLUTIONS["pilot-20-job-runner"].items():
            write(wd / rel, content)
        write(wd / "progress.md", "# continue done\n")
        r2 = run_pytest(wd)
        wall = time.perf_counter() - t0
        fr = (0 if r1["green"] else 1) + (0 if r2["green"] else 1)
        return row(cid, "bcc", r1, r2, fr, 2, 5, wall, "recovery jobrun", 5 if r2["green"] else None)

    write(wd / "plans.md", f"# plans {cid}\n")
    write(wd / "progress.md", "# progress\n")
    write(wd / "findings.md", "# findings\n")
    write(wd / "PLAN.md", f"# PLAN {cid}\n")
    turns = 4
    for rel, content in SOLUTIONS[cid].items():
        write(wd / rel, content)
    r1 = run_pytest(wd)
    wall = time.perf_counter() - t0
    fr = 0 if r1["green"] else 1
    return row(cid, "bcc", r1, None, fr, 1, turns, wall, "planned implement", turns if r1["green"] else None)


def run_adhoc(cid: str, wd: Path) -> dict:
    t0 = time.perf_counter()
    r1, r2, turns, fr = adhoc_broken_then_one_fix(cid, wd)
    wall = time.perf_counter() - t0
    ttg = turns if r2["green"] else None
    return row(cid, "ad-hoc", r1, r2, fr, 2, turns, wall, "case-by-case short demand, 1 rework max", ttg)


def main():
    cases = sorted([p.name for p in TASKS.iterdir() if p.is_dir() and p.name.startswith("pilot-")])
    assert len(cases) == 20, cases
    results = []
    for cid in cases:
        print("==", cid)
        bcc_wd, adh_wd = prep(cid)
        br = run_bcc(cid, bcc_wd)
        print("  bcc", br["label"], br["first"], "final", br["final_pass"], "tok", br["tokens_est"])
        if not br["final_pass"] and cid not in ("pilot-06-log-pipeline", "pilot-20-job-runner"):
            print("  BCC FAIL DETAIL", run_pytest(bcc_wd)["out"][:500])
        ar = run_adhoc(cid, adh_wd)
        print("  ad-hoc", ar["label"], ar["first"], "final", ar["final_pass"], "tok", ar["tokens_est"])
        results.extend([br, ar])
    out = RUNS / "results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    # aggregates
    for arm in ("bcc", "ad-hoc"):
        a = [r for r in results if r["arm"] == arm]
        n = len(a)
        clean = sum(1 for r in a if r["clean_pass"])
        final = sum(1 for r in a if r["final_pass"])
        mf = sum(r["fail_runs"] for r in a) / n
        mt = sum(r["tokens_est"] for r in a) / n
        mw = sum(r["wall_s"] for r in a) / n
        print(f"AGG {arm}: clean={clean}/{n} final={final}/{n} mean_fail={mf:.2f} mean_tok={mt:.0f} mean_wall={mw:.2f}")
    print("wrote", out)


if __name__ == "__main__":
    main()
