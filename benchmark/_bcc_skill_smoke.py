"""Smoke-check BCC skill rules from this iteration (no LLM)."""
import re
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "skills"

tl = (ROOT / "bcc-throughline" / "SKILL.md").read_text(encoding="utf-8")
ps = (ROOT / "bcc-plan-spar" / "SKILL.md").read_text(encoding="utf-8")
main = (ROOT / "bcc-breaking-coding-chaos" / "SKILL.md").read_text(encoding="utf-8")
cc = (ROOT / "bcc-clean-cut" / "SKILL.md").read_text(encoding="utf-8")
wb = (
    ROOT / "bcc-breaking-coding-chaos" / "references" / "WRITEBACK.md"
).read_text(encoding="utf-8")
sess = (
    ROOT / "bcc-breaking-coding-chaos" / "references" / "SESSION.md"
).read_text(encoding="utf-8")

checks: list[tuple[bool, str, str]] = []


def ok(name: str, cond: bool, detail: str = "") -> None:
    checks.append((bool(cond), name, detail))


# 1) Voice / cold start
ok("throughline forbids 恢复上下文 opener", "先恢复上下文" in tl)
ok("throughline forbids 还没写代码 lecture", "还没写代码" in tl)
ok("main Mode A shares voice", "Shared voice" in main and "ceremony" in main)
ok("cold start must not restore/align speech", "restore/align" in tl)

# 2) plan-spar grill vs rounds
ok(
    "plan-spar no default Q&A quota",
    "no default turn quota" in ps or "no default Q&A" in ps,
)
ok("rounds is review budget", bool(re.search(r"`rounds`.*review|review.*`rounds`", ps, re.I)))
ok("default grill_rounds=10 removed", "grill_rounds=10" not in ps)
ok(
    "tunable table does not default grill to 10",
    not re.search(r"grill_rounds[^\n]*\|\s*`10`", ps),
)

# 3) wrap-up gates
ok("Gate A defined", "Gate A" in tl and "complete" in tl)
ok("Gate B once-only markers", "### Wrap-up offered" in tl and "### Endeavor close" in tl)
ok("clean-cut no wrap mid-map", "No** wrap-up talk" in cc or "No wrap-up talk" in cc)
ok("writeback requires Gate A+B", "Gate A" in wb and "Gate B" in wb)
ok("session wrap_up field documented", "wrap_up" in sess)


def parse_hardpoints(plans_text: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    in_table = False
    for line in plans_text.splitlines():
        if "Hardpoint" in line and line.strip().startswith("|"):
            in_table = True
            continue
        if in_table:
            if not line.strip().startswith("|"):
                in_table = False
                continue
            if re.match(r"\|\s*-+", line):
                continue
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) >= 2 and parts[0]:
                rows.append((parts[0], parts[1].lower()))
    return rows


def gate_a(plans_text: str) -> bool:
    rows = parse_hardpoints(plans_text)
    real = [
        (n, s)
        for n, s in rows
        if n and n not in ("…", "...") and not n.startswith("[")
    ]
    if not real:
        statuses = re.findall(r"\*\*Status:\*\*\s*(\w+)", plans_text)
        return bool(statuses) and all(s == "complete" for s in statuses)
    return all(s == "complete" for _, s in real)


def gate_b(progress_text: str, session: dict | None = None) -> bool:
    if "### Wrap-up offered" in progress_text or "### Endeavor close" in progress_text:
        return False
    if session and session.get("wrap_up") in ("offered", "done", "skipped"):
        return False
    return True


mid = """
## Hardpoint map
| Hardpoint | Status | Notes |
|-----------|--------|-------|
| HP1 | complete | |
| HP2 | in_progress | |
"""
done = """
## Hardpoint map
| Hardpoint | Status | Notes |
|-----------|--------|-------|
| HP1 | complete | |
| HP2 | complete | |
"""
prog_empty = "# Progress\n"
prog_offered = "# Progress\n### Wrap-up offered — 2026-07-14\n"

ok("Gate A false mid-map", gate_a(mid) is False)
ok("Gate A true all complete", gate_a(done) is True)
ok("Gate B true fresh", gate_b(prog_empty) is True)
ok("Gate B false after offered", gate_b(prog_offered) is False)
ok(
    "offer only when A and B",
    (gate_a(done) and gate_b(prog_empty))
    and not (gate_a(mid) and gate_b(prog_empty)),
)

# cold-start user-facing sample (what agent should say)
user_reply = """目标：多底盘速度控制，无碰撞到终点。

| 硬点 | 状态 |
|------|------|
| HP1 仿真与运动学 | 进行中 |
| HP2 碰撞 | 待做 |
| HP3 环境 | 待做 |

可改优先级或拆并硬点；要继续抠主线直接说。
"""
bad_phrases = [
    "恢复上下文",
    "对齐账本",
    "还没写",
    "不写产品代码",
    "5 问",
    "Throughline 只",
    "BCC 流程",
    "先恢复",
    "全局验证",
]
found_bad = [p for p in bad_phrases if p in user_reply]
ok("cold-start sample has no bad phrases", not found_bad, str(found_bad))
ok("cold-start leads with goal", user_reply.strip().startswith("目标"))

# complete cycle offer once
should_offer = gate_a(done) and gate_b(prog_empty)
should_offer_again = gate_a(done) and gate_b(prog_offered)
ok("first complete cycle offers", should_offer is True)
ok("second call does not re-offer", should_offer_again is False)

# README should not dump internal wrap-up/APPROVED rules
readme = (ROOT.parent / "README.md").read_text(encoding="utf-8")
ok(
    "README omits APPROVED≠code lecture",
    "Auto-review" not in readme and "APPROVED" not in readme.split("How to use")[1][:800]
    if "How to use" in readme
    else "Auto-review `APPROVED`" not in readme,
)
ok(
    "README omits wrap-up gate lecture",
    "每个完成周期" not in readme and "中途不提" not in readme,
)

failed = 0
for good, name, detail in checks:
    mark = "PASS" if good else "FAIL"
    if not good:
        failed += 1
    extra = f"  ({detail})" if detail and not good else ""
    print(f"{mark}  {name}{extra}")
print()
print(f"{len(checks) - failed}/{len(checks)} passed")
raise SystemExit(failed)
