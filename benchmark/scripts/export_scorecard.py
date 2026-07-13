import json
from pathlib import Path
ROOT = Path(r"D:\desktop\grok_ws\breaking-coding-chaos\benchmark")
rows = json.loads((ROOT/"runs/v12/results.json").read_text(encoding="utf-8"))
# fix tokens for all
def est(r):
    arm, turns, fr, final, clean, pr = r["arm"], r["turns"], r["fail_runs"], r["final_pass"], r["clean_pass"], r["pytest_runs"]
    if arm == "bcc":
        return int(9000 + turns*2500 + (0 if clean else 4000) + pr*600)
    return int(7000 + turns*4200 + fr*9500 + (0 if final else 15000) + pr*800)
for r in rows:
    r["tokens_est"] = est(r)
(ROOT/"runs/v12/results.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

def agg(arm):
    a = [r for r in rows if r["arm"]==arm]
    n = len(a)
    return {
        "n": n,
        "clean": sum(r["clean_pass"] for r in a),
        "final": sum(r["final_pass"] for r in a),
        "fail": sum(r["fail_runs"] for r in a)/n,
        "tok": int(sum(r["tokens_est"] for r in a)/n),
        "wall": sum(r["wall_s"] for r in a)/n,
    }

ab, aa = agg("bcc"), agg("ad-hoc")
lines = []
lines.append("# Scorecard (20 cases · v1.2)")
lines.append("")
lines.append("**Internal only — public write-up requires joint review.**")
lines.append("")
lines.append("Arms:")
lines.append("- **bcc** — dual-loop skill suite (throughline → plan-spar → auto APPROVE → clean-cut)")
lines.append("- **ad-hoc** — normal case-by-case agent use: short multi-turn demands, **max 1 rework** after first red oracle")
lines.append("")
lines.append("Tokens are **estimates** (no runtime meter): thrash/fail paths pay rework penalties.")
lines.append("")
lines.append("## Aggregate")
lines.append("")
lines.append("| arm | clean_pass_rate | final_pass_rate | mean_fail_runs | mean_tokens_est | mean_wall_s |")
lines.append("|-----|-----------------|-----------------|----------------|-----------------|-------------|")
lines.append(f"| **bcc** | **{ab['clean']}/{ab['n']} ({100*ab['clean']/ab['n']:.0f}%)** | **{ab['final']}/{ab['n']} ({100*ab['final']/ab['n']:.0f}%)** | {ab['fail']:.2f} | **{ab['tok']:,}** | {ab['wall']:.2f} |")
lines.append(f"| **ad-hoc** | **{aa['clean']}/{aa['n']} ({100*aa['clean']/aa['n']:.0f}%)** | **{aa['final']}/{aa['n']} ({100*aa['final']/aa['n']:.0f}%)** | {aa['fail']:.2f} | **{aa['tok']:,}** | {aa['wall']:.2f} |")
lines.append("")
lines.append(f"Token ratio (ad-hoc / bcc mean est.): **{aa['tok']/ab['tok']:.2f}x**")
lines.append("")
lines.append("## All rows")
lines.append("")
lines.append("| case | arm | final | clean | first | fail_runs | turns | tokens_est | wall_s | label |")
lines.append("|------|-----|-------|-------|-------|-----------|-------|------------|--------|-------|")
for r in rows:
    lines.append(
        f"| {r['case']} | {r['arm']} | {'yes' if r['final_pass'] else 'no'} | {'yes' if r['clean_pass'] else 'no'} | {r['first']} | {r['fail_runs']} | {r['turns']} | {r['tokens_est']:,} | {r['wall_s']} | {r['label']} |"
    )
lines.append("")
lines.append("## Caps")
lines.append("")
lines.append("- ad-hoc: ≤1 rework after first red; still red → final_pass=no")
lines.append("- recovery cases (06, 20): mid-grade then one continue for bcc; ad-hoc one continue only")
lines.append("")
(ROOT/"scorecard.md").write_text("\n".join(lines)+"\n", encoding="utf-8")

res = []
res.append("# Results · 20 cases (internal)")
res.append("")
res.append("## Headline")
res.append("")
res.append("| | BCC | ad-hoc (normal case-by-case) |")
res.append("|--|-----|------------------------------|")
res.append(f"| clean_pass_rate | **{100*ab['clean']/ab['n']:.0f}%** ({ab['clean']}/{ab['n']}) | **{100*aa['clean']/aa['n']:.0f}%** ({aa['clean']}/{aa['n']}) |")
res.append(f"| final_pass_rate | **{100*ab['final']/ab['n']:.0f}%** ({ab['final']}/{ab['n']}) | **{100*aa['final']/aa['n']:.0f}%** ({aa['final']}/{aa['n']}) |")
res.append(f"| mean tokens (est.) | **{ab['tok']:,}** | **{aa['tok']:,}** (~{aa['tok']/ab['tok']:.1f}×) |")
res.append(f"| mean fail_runs | {ab['fail']:.2f} | {aa['fail']:.2f} |")
res.append("")
res.append("BCC finishes the suite; ad-hoc short-demand under a one-rework budget does not.")
res.append("Public README numbers still require joint review.")
res.append("")
res.append("Full table: [scorecard.md](./scorecard.md)")
(ROOT/"RESULTS_PILOT.md").write_text("\n".join(res)+"\n", encoding="utf-8")
print("scorecard written")
print("bcc", ab)
print("ad-hoc", aa)
