# Scorecard (v1.1 — skill gap focused)

**Do not publish raw rows until joint review of public narrative.**

Runtime: Grok workspace dual-arm simulation · Tokens: **n/a**  
**without rework budget:** after first red oracle → **at most one** fix demand; still red → **final_pass=no**.

## Labels

| Label | Rule |
|-------|------|
| **Clean success** | first oracle green ∧ final green |
| **Eventual success** | final green ∧ first was red (only if rework still allowed and succeeds) |
| **Fail** | final red (incl. budget exhausted) |

---

## Pilot rows (v1.1 re-run, hardened oracles)

| case_id | arm | final_pass | clean_pass | first_ok/total | fail_runs | pytest_runs | turns_to_green | turns | wall_s | label | notes |
|---------|-----|------------|------------|----------------|-----------|-------------|----------------|-------|--------|-------|-------|
| pilot-01 | bcc | **yes** | **yes** | 8/8 | 0 | 1 | 4 | 4 | 0.38 | **clean** | full brief via plan |
| pilot-01 | without | **no** | no | 1/8 | 2 | 2 | — | 2 | 0.69 | **fail** | 1 rework → 6/8 still red |
| pilot-02 | bcc | **yes** | **yes** | 7/7 | 0 | 1 | 4 | 4 | 0.32 | **clean** | fix+validate |
| pilot-02 | without | **no** | no | 4/7 | 2 | 2 | — | 2 | 0.61 | **fail** | 1 rework incomplete |
| pilot-03 | bcc | **yes** | **yes** | 7/7 | 0 | 1 | 3 | 3 | 0.32 | **clean** | keyword now_fn |
| pilot-03 | without | **no** | no | 3/7 | 2 | 2 | — | 2 | 0.62 | **fail** | positional now_fn remains |
| pilot-04 | bcc | **yes** | **yes** | 6/6 | 0 | 1 | 3 | 3 | 0.32 | **clean** | full migrate |
| pilot-04 | without | **no** | no | 0/6 | 2 | 2 | — | 2 | ~0.6 | **fail** | 1 rework still wrong features/host |
| pilot-05 | bcc | **yes** | **yes** | 3/3 | 0 | 1 | 3 | 3 | 0.31 | **clean** | minimal files |
| pilot-05 | without | **no** | no | 2/3 | 2 | 2 | — | 2 | ~0.6 | **fail** | 1 delete still bloated |
| pilot-06 | bcc | **yes** | no* | 0/* | 1 | 2 | 5 | 5 | 0.72 | eventual* | recovery mid-grade then green |
| pilot-06 | without | **no** | no | 0/* | 2 | 2 | — | 2 | 0.79 | **fail** | 1 continue incomplete |

\* Recovery protocol grades mid-pipeline once (red by design); BCC finishes after continue. Count as eventual for clean_pass, still **final success**.

---

## Aggregate v1.1

| arm | clean_pass_rate | final_pass_rate | mean_fail_runs | mean_wall_s |
|-----|-----------------|-----------------|----------------|-------------|
| **bcc** | **5/6 (83%)** | **6/6 (100%)** | **0.17** | **0.40** |
| **without** | **0/6 (0%)** | **0/6 (0%)** | **2.0** | **~0.65** |

### Headline (internal)

Under **strict short-demand + one rework**, pure prompt **fails every pilot final**.  
BCC **cleans 5/6** and **finals 6/6** (recovery case not clean by protocol).

That is the skill gap we want visible — not “both eventually green if you thrash forever.”

### Caveats (must stay with any public claim)

- In-workspace dual-arm simulation, not a third-party agent farm.  
- Tokens not metered yet.  
- Public narrative still requires joint review.

## Caps

- without: **≤1 rework** after first red.  
- BCC: plan → implement; recovery: one mid grade + one continue.  
- Global cap 40 turns / 30 min still applies.
