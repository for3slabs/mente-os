# ADR-011 · Four layers, because existing is not being read

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: every standard a piece of work is supposed to follow
does-not-apply-to: ⭐ a rule the agent cannot break without a human noticing immediately — those need no layers

## Context

⛔ **Existing ≠ findable ≠ READ**, and a system that confuses the three ships standards nobody
applies while believing they are enforced.

## Decision

**Four layers, each catching what the one before it misses:**

1. the **router** names where the law lives — ⭐ catches somebody who does not know a standard exists
2. ⭐ the **block declares** the standards it is judged by — catches somebody who knows it exists and
   does not know it applies HERE
3. ⬜ a **gate injects** the standard before the edit — ⛔ catches somebody who knows it applies and
   does not open it
4. a **validator** checks at close — ⚠️ catches everything the first three let through

## Rejected alternatives

- ⛔ **Tell the router to read it.** ⭐ **It already did, and it failed** — the instruction existed
  and was not followed, which is the measurement that produced this decision.
- ⛔ **Embed every standard in the startup file.** ⚠️ The context cost goes from tens of thousands
  of tokens to hundreds of thousands, ⭐ **and a startup nobody can afford is a startup that gets
  trimmed** — beginning with the standards.
- ⚠️ **One strong layer instead of four.** ⛔ Whichever is chosen has a blind spot, and ⭐ **the
  blind spot of a single layer is invisible from inside it.**

## Rationale

> ## ⭐ EACH LAYER EXISTS BECAUSE THE ONE BEFORE IT WAS MEASURED FAILING.
> ⚠️ **This is not defence in depth by preference.** Layers 1 and 2 were in place, and the standard
> still went unread — ⛔ **layer 3 is the answer to a specific observed failure, not to a
> hypothetical one.**

## Evidence

⭐ **Measured across analysed sessions: a documented method went unread in two of five.** ⛔ **The
worst case was over a thousand requests with zero reads of it** — the file existed, was indexed,
was named in the startup, and nobody opened it once.

⚠️ **Layers 1 and 2 were both satisfied in that session.** ⭐ **That is the whole argument for
layer 3.**

## Consequences

- ⭐ layer 1 — the router points, it does not hold rules (`INH-RTR-*`)
- layer 2 — `BLK-STD-001` 🔒 · at least one standard declared, or nothing can be rejected
- ⭐ layer 3 — **`hooks/pre-edit-standards.py`**: it reads what the block declared and names it
  back before the edit · ⛔ it never blocks — an unbearable guard is deleted
- layer 4 — `BLK-CLS-*` 🔒 · the closing is checked, and it catches what the others let through

## What would change this decision

⭐ **It stops being right if layer 3 turns out unnecessary** — if standards declared in the block
are read reliably without injection, the gate is friction with no return. ⚠️ **The measurement is
the same one that produced the decision:** count reads of a declared standard over a period of
work. ⛔ **Nobody has run that count since the gate was introduced**, so the question is open, not
settled.

## Reverting

⛔ **Drop the gate layer.** ⚠️ Reading depends on the agent's judgment again — ⭐ **and the failure
is silent: nothing reports that a standard was not opened, which is exactly why it took a
thousand requests to notice the first time.**

---

Related: `ADR-012-few-gates-block-the-rest-warn.md` (⭐ **layer 3 INJECTS, it does not block** — read together, or a reader counts four gates where there are not four) ·
`ADR-001-work-unit-is-the-block.md` (the block that declares) ·
`../rule-inheritance.md` (⭐ the router layer, and why a rule written there has no level) ·
`../contract-block.md` `§D` (the declaration layer 3 would read) · `../contract-adr.md`.
