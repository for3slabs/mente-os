# ADR-010 · Cheap to open, expensive to close

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: the moment a block is created, and the moment it is closed
does-not-apply-to: ⭐ a block reopened after closing — it already has everything, and asking for four fields again teaches nothing

## Context

⛔ **A contract can be strict at one end or the other, and the choice is not symmetric.** Strict at
OPEN filters who bothers; strict at CLOSE filters what is kept.

## Decision

**Opening requires only four sections — identity, scope, connections, required standards.**
**Closing requires everything, plus the sufficiency check.**

## Rejected alternatives

- ⛔ **Strict from the start.** ⚠️ Measured elsewhere in this system: a strict method went unread
  in two sessions out of five — ⭐ **and an unread standard is indistinguishable from no standard,
  except that somebody is maintaining it.**
- ⛔ **Cheap at both ends.** ⚠️ Then nothing is ever complete, and ⭐ **the block stops being a
  record of work and becomes a record of intentions.**
- ⚠️ **Strict at open, cheap at close.** ⛔ The exact inversion: it charges for starting, which
  people avoid, and forgives finishing, which is where the value is written.

## Rationale

> ## ⭐ IF OPENING COSTS TEN FIELDS, THE WORK HAPPENS WITHOUT A BLOCK — AND EVERYTHING IS LOST.
> ⚠️ **The cost of a heavy open is not measured in the blocks that are worse. It is measured in
> the ones that never exist.**

⭐ **And the four are not a soft start.** They are exactly the questions whose absence caused the
measured failures: *what is this · what does it touch · what does it depend on · by what standard
is it judged*. ⛔ **A block missing any of them cannot be resumed by anybody else.**

## Evidence

⭐ **Observed in a real installation, and the outcome was not the one predicted.** Every open block
carries all eleven sections, not the four minimum — ⚠️ **and the validator asks for four.**

> ## ⭐ THE FLOOR BEING LOW DID NOT MAKE THE BLOCKS THINNER. IT MADE THEM EXIST.
> ⛔ **Nobody stopped at four** — the four removed the reason not to start, and the rest was
> written because it was useful, not because it was demanded.

## Consequences

- `BLK-OPN-001` 🔒 — the four sections are present at open, and only those are required
- `BLK-OPN-002` 🔒 — the block is declared where blocks are listed
- `BLK-TRN-001` 🔒 — ⭐ **closing requires acceptance AND sufficiency**, never one alone
- `BLK-CLS-003` 🔒 — what was NOT done is stated: ⛔ silence reads as completeness

## What would change this decision

⭐ **It stops being right if blocks are routinely opened and abandoned.** ⚠️ A floor this low
assumes the cost of starting is what stops people — ⛔ **if the real cost turns out to be
finishing, then a cheap open is producing abandoned records, and the floor is in the wrong
place.** The signal is a rising count of blocks open past their declared period with nothing
written after the four.

## Reverting

⛔ **Make it strict at open.** ⚠️ Expect the block to be skipped, and the work to happen beside the
system rather than inside it — ⭐ **which is invisible, because what is skipped leaves no record
of having been skipped.**

---

Related: `ADR-009-one-file-per-block.md` (⭐ **the eleven sections this decision does NOT demand at
open** — one fixes the final shape, this one fixes the entry cost) ·
`ADR-007-a-closed-block-is-archived.md` (why the close is worth charging for) ·
`../contract-block.md` · `../contract-adr.md`.
