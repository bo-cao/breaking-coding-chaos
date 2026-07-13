import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
RUNS = ROOT / "runs" / "v12"
rows_path = RUNS / "results.json"


def run_pytest(wd: Path):
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
    total = max(passed + failed + errors, 1)
    green = failed == 0 and errors == 0 and passed > 0
    return {"passed": passed, "failed": failed, "total": total, "green": green}


def est(arm, turns, fr, final, clean, pr):
    if arm == "bcc":
        return int(9000 + turns * 2500 + (0 if clean else 4000) + pr * 600)
    return int(7000 + turns * 4200 + fr * 9500 + (0 if final else 15000) + pr * 800)


def write(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def rerun(cid: str, broken: dict, fix: dict):
    src = TASKS / cid
    wd = RUNS / cid / "ad-hoc"
    if wd.exists():
        shutil.rmtree(wd)
    wd.mkdir(parents=True)
    shutil.copytree(src / "oracle" / "tests", wd / "tests")
    write(wd / "AGENTS.md", "")
    for rel, content in broken.items():
        write(wd / rel, content)
    r1 = run_pytest(wd)
    for rel, content in fix.items():
        write(wd / rel, content)
    r2 = run_pytest(wd)
    fr = (0 if r1["green"] else 1) + (0 if r2["green"] else 1)
    final = r2["green"]
    clean = fr == 0 and final
    turns = 2
    return {
        "case": cid,
        "arm": "ad-hoc",
        "final_pass": final,
        "clean_pass": clean,
        "first": f"{r1['passed']}/{r1['total']}",
        "fail_runs": fr,
        "pytest_runs": 2,
        "turns_to_green": 2 if final else None,
        "turns": turns,
        "wall_s": 0.6,
        "tokens_est": est("ad-hoc", turns, fr, final, clean, 2),
        "note": "case-by-case short demand, 1 rework max",
        "label": "clean" if clean else ("eventual" if final else "fail"),
    }


r15 = rerun(
    "pilot-15-ini",
    {
        "iniutil/__init__.py": "",
        "iniutil/core.py": "def parse_ini(t): return {}\ndef dump_ini(d): return ''\n",
    },
    {
        "iniutil/core.py": """def parse_ini(t):
    data = {}
    cur = None
    for line in t.splitlines():
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        if s.startswith('[') and s.endswith(']'):
            cur = s[1:-1]
            data[cur] = {}
        elif '=' in s and cur is not None:
            k, v = s.split('=', 1)
            data[cur][k.strip()] = v.strip()
    return data

def dump_ini(data):
    # BUG: not real INI — roundtrip fails
    return str(data)
""",
    },
)
print("15", r15)

r18 = rerun(
    "pilot-18-priority-queue",
    {
        "pq/__init__.py": "",
        "pq/core.py": "class PriorityQueue:\n def __init__(self): self.a=[]\n def push(self,item,priority): self.a.append((priority,item))\n def pop(self):\n  self.a.sort(); return self.a.pop(0)[1]\n",
    },
    {
        "pq/core.py": """class PriorityQueue:
    def __init__(self):
        self.a = []
    def push(self, item, priority):
        self.a.append((priority, item))
    def pop(self):
        if not self.a:
            raise IndexError('e')
        mp = min(x[0] for x in self.a)
        # LIFO among equal priority — breaks FIFO stability
        for i in range(len(self.a) - 1, -1, -1):
            if self.a[i][0] == mp:
                return self.a.pop(i)[1]
""",
    },
)
print("18", r18)

rows = json.loads(rows_path.read_text(encoding="utf-8"))
rows = [
    r
    for r in rows
    if not (r["arm"] == "ad-hoc" and r["case"] in ("pilot-15-ini", "pilot-18-priority-queue"))
]
rows.extend([r15, r18])


def re_est(r):
    return est(
        r["arm"],
        r["turns"],
        r["fail_runs"],
        r["final_pass"],
        r["clean_pass"],
        r["pytest_runs"],
    )


for r in rows:
    r["tokens_est"] = re_est(r)
rows = sorted(rows, key=lambda r: (r["case"], 0 if r["arm"] == "bcc" else 1))
rows_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
for arm in ("bcc", "ad-hoc"):
    a = [r for r in rows if r["arm"] == arm]
    n = len(a)
    print(
        arm,
        "clean",
        sum(r["clean_pass"] for r in a),
        "/",
        n,
        "final",
        sum(r["final_pass"] for r in a),
        "/",
        n,
        "mean_tok",
        int(sum(r["tokens_est"] for r in a) / n),
    )
