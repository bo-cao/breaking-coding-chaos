# CONTEXT.md Format

Adapted from domain-modeling CONTEXT-FORMAT for **plan-spar**.

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request
```

## Rules

- **Be opinionated.** Pick the best term; list others under `_Avoid_`.
- **Keep definitions tight.** One or two sentences. What it IS, not a procedure.
- **Only project-specific terms.** General programming concepts do not belong.
- Group under subheadings when clusters emerge.

## Single vs multi-context

- Default: one `CONTEXT.md` at repo root.
- If `CONTEXT-MAP.md` exists, follow it for multiple contexts.
- Create lazily when the first term is resolved.

`CONTEXT.md` assists **`PLAN.md` formulation**. It is not an implementation checklist.
