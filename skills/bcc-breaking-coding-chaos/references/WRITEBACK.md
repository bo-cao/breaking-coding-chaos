# BCC throughline writeback (required)

**Global progress lives only in** `plans.md` / `progress.md` / `findings.md`.  
**`PLAN.md` is not the global log** — it is the current coding brief and is rewritten/约减 per active work.

## When writeback is mandatory

| Event | Minimum writeback |
|-------|-------------------|
| After **bcc-plan-spar** locks PLAN | `progress.md`: one session line (slice name, PLAN locked). Optionally `plans.md` hardpoint → in_progress |
| After **bcc-plan-spar** human APPROVE | `progress.md`: APPROVE implement noted |
| After **bcc-clean-cut** verify **pass** | All three files as below (full close-out) |
| After **bcc-clean-cut** verify **fail** (any attempt) | `progress.md` error row; after 2 fails force plan-spar note in progress |
| User reprioritizes | `plans.md` only (throughline skill) |

**Failing to writeback = slice incomplete.** Do not claim done until writeback finished.

## What goes where

| File | Write | Do **not** put here |
|------|--------|---------------------|
| **`plans.md`** | Goal, phases, hardpoint map status (`pending`/`in_progress`/`complete`), endeavor-level decisions | Full coding checklist, long review essays |
| **`progress.md`** | Session actions, files touched, test results table, errors | Speculative design |
| **`findings.md`** | Cross-cutting discoveries / risks worth keeping globally | Per-slice checklist items (those die in PLAN 约减 or progress) |
| **`PLAN.md`** | Current slice coding contract only — **update in place** each cycle | Global phase history (use throughline) |

## Close-out template (append to `progress.md`)

```markdown
### Slice: <name> — <date>
- **Status:** complete | blocked
- **Actions:** <bullets>
- **Files:** <paths>
- **Verify:** <command + result>
- **Next hardpoint:** <from plans.md or none>
```

## `plans.md` hardpoint row

Update the matching row to `complete` / `in_progress` / `blocked` and one-line Notes (e.g. verify metric).

## After last hardpoint completes (wrap-up — strict)

Only after normal slice writeback, evaluate **both** gates from [bcc-throughline](../../bcc-throughline/SKILL.md) *Endeavor wrap-up*:

| Gate | Pass means |
|------|------------|
| **A — Map fully complete** | Every real hardpoint in `plans.md` is `complete` (none pending/in_progress/blocked). Empty hardpoint table → every phase Status is `complete`. |
| **B — Not yet offered/closed** | No `### Wrap-up offered` / `### Endeavor close` in `progress.md`, and session `wrap_up` not in `offered`/`done`/`skipped`. |

- **Both pass** → offer wrap-up **once**: write `### Wrap-up offered` first, then ask global verify / what kind / skip.  
- **A fails** (still open work) → only note next hardpoint; **do not** mention global wrap-up.  
- **B fails** (already offered/closed) → do not re-ask; short “slice done” is enough.

```markdown
### Wrap-up offered — <date>
- Map: all throughline hardpoints complete
- Status: awaiting user (global verify / skip / add work)

### Endeavor close — <date>
- **Global verify:** skipped | <commands + result>
- **Status:** complete | blocked (verify failed)
- **Notes:** <one line>
```

## Agent checklist before saying “done”

- [ ] `progress.md` updated this turn  
- [ ] `plans.md` hardpoint/phase status updated if applicable  
- [ ] `findings.md` only if something global was learned  
- [ ] `PLAN.md` 约减 / status matches reality  
- [ ] Wrap-up offered **only if** Gate A + Gate B (not on mid-map slices)  
