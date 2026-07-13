# ADR Format

Adapted from domain-modeling ADR-FORMAT for **bcc-plan-spar**.

ADRs live in `docs/adr/` as `0001-slug.md`, `0002-slug.md`, …

Create `docs/adr/` lazily — only when the first ADR is needed.

## Template

```md
# {Short title of the decision}

{1-3 sentences: context, decision, why.}
```

Short is fine. Record *that* a decision was made and *why*.

## Optional sections

Only when valuable: Status, Considered Options, Consequences.

## Numbering

Highest existing number + 1.

## When to offer an ADR

All three must hold:

1. **Hard to reverse**
2. **Surprising without context**
3. **Real trade-off** with rejected alternatives

Do **not** dump every decision into throughline `plans.md` / `findings.md` / `progress.md`.
