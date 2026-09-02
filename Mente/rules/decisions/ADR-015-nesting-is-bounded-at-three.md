# ADR-015 · Nesting is bounded, and the bound is three

date: {{date}}
status: accepted
implementation: verified
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: how deep a unit of work may be subdivided
does-not-apply-to: ⛔ the three levels of RULE inheritance — ⚠️ same number, unrelated concept

## Context

`ADR-001` fixes two levels: a block, and the tasks inside it. ⛔ **Two is not always enough, and
unbounded is always too many** — this decision is about what happens between those.

## Decision

**At most three levels of nesting: the unit of work · an intermediate GROUP · the task.**

⚠️ **This is a CEILING, not a shape.** ⭐ Two levels remain the normal case; the third exists so
that large work does not have to flatten.

## Rejected alternatives

- ⛔ **Two levels, fixed.** ⚠️ Large work then arrives as a flat list of twenty tasks — ⭐ **and a
  flat list of twenty is not a structure, it is a backlog with a heading.**
- ⛔ **Free nesting.** ⚠️ Deep trees are the disorder this system exists to fix; ⭐ **and depth is
  a one-way ratchet — nobody ever flattens a tree back.**
- ⚠️ **A ceiling of four or five.** ⛔ Any number above three is the same as free in practice:
  ⭐ **nobody hits a limit they cannot reach by accident**, so the limit stops informing the shape.

## Rationale

> ## ⭐ THE THIRD LEVEL IS NOT FOR DEPTH. IT IS SO THE SECOND ONE DOES NOT OVERFLOW.
> ⚠️ **Without it, everything that does not fit in one task becomes another task** — and the
> relation between them lives nowhere.

⛔ **And the ceiling has to be low enough to be reached.** A limit nobody meets teaches nothing
about how to structure work.

## Evidence

⭐ **Measured, and it is the failure this decision predicted:** in a real installation, blocks
reach **fourteen flat sub-blocks** with no intermediate level anywhere. ⛔ **The GROUP was decided
and never built**, so large work flattened exactly as the rejected alternative said it would.

⚠️ **A mature external reference took the same path in reverse:** it shipped two levels and added
arbitrary depth in its stable release. ⭐ **The need is real. The risk is the maze.**

## Consequences

- ⬜ **Nothing enforces this yet** — the engine has no rule bounding nesting depth, and `not-started`
  says so rather than implying otherwise
- ⛔ **What it would take:** a rule that counts nesting depth in a block and refuses beyond three,
  plus a GROUP level the block contract does not currently define
- ⚠️ `BLK-SUB-003` 🔒 already prevents closing over an open sub-block — ⭐ **that is containment,
  not depth**

## What would change this decision

⭐ **It stops being right if the intermediate level is built and stays unused.** ⚠️ Fourteen flat
sub-blocks is evidence that the third level is NEEDED — ⛔ **but it is not yet evidence that it
would be USED**, and those are different claims. If the group ships and blocks stay flat, the
problem was never depth.

## Reverting

⛔ **Allow free depth.** ⚠️ Expect trees nobody can navigate — ⭐ **and the navigation cost is paid
by every future reader, while the depth was added by one.**

---

Related: `ADR-001-work-unit-is-the-block.md` (⭐ **the two levels this one bounds** — read together,
or the two records look like they disagree) · `ADR-009-one-file-per-block.md` (⚠️ depth pushes
against one file) · `../rule-inheritance.md` (⛔ **a DIFFERENT set of three levels**) ·
`../contract-adr.md`.
