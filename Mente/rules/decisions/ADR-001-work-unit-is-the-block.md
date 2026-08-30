# ADR-001 · The unit of work is the BLOCK

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: every piece of work this system governs
does-not-apply-to: ⬜ declare — work an installation deliberately keeps outside

## Context

The first decision the system makes about itself: what a unit of work IS. Everything downstream —
scope, isolation, closing, the quality verdict — needs one answer to that, and needs it before
anything else can be defined.

## Decision

A **BLOCK** is a unit of work grouping tasks that share one relation. A **SUB-BLOCK** is one task
attacking one piece.

## Rejected alternatives

- **A single level.** ⛔ It loses the propagation graph: with only one level, "what work depends
  on what work" and "what do I touch" collapse into the same field, and neither is answerable.
- **A level per piece, with no grouping.** ⚠️ Every piece becomes its own unit, and nothing states
  which pieces must move together.

## Rationale

⭐ **One level cannot answer both questions.** The block answers *what work depends on what work*;
the sub-block answers *what do I touch*.

> ## ⛔ THE SECOND LEVEL IS WHERE THE PROPAGATION GRAPH LIVES.
> ⚠️ **Without it, an estimate is made from the file you opened, not from the files that change
> with it** — and the estimate is always the smaller one.

## Evidence

⭐ **Measured:** a change described as *"move where one value is stored"* looked like one file and
was six. ⛔ **The fix-over-fix that followed came from the missing second level**, not from the
change being hard.

## Consequences

- `rules/contract-block.md` — the shape a block must have, and its sections
- `BLK-SUB-*` — a sub-block belongs to exactly one block
- ⭐ `rules/rule-working-in-a-block.md` `WRK-IMP-*` — dependents are measured BEFORE the first
  edit, which is only possible because the two levels exist

## Reverting

⛔ **Collapse to a single level. The propagation graph is lost** — and with it every rule that
reads it: the lane, the impact map, and the closing that names who inherits what.

---

Related: `../contract-block.md` (the shape this decision produced) ·
`../rule-working-in-a-block.md` (the propagation it makes possible) · `../contract-adr.md`.
