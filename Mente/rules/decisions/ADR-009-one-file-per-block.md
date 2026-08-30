# ADR-009 · One block, one file

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: the block file and everything a reader needs to resume the work
does-not-apply-to: ⭐ evidence a closing produces — long logs, reports, measurements live beside the block, not inside it

## Context

A block holds identity, scope, connections, standards, state, sub-blocks, decisions, friction,
checkpoints, context and closing. ⛔ **The obvious instinct is to split eleven concerns into
eleven files.**

## Decision

**One block = ONE file, with its sections in a fixed order.** ⭐ **Tiers are the ORDER of sections
inside it, never separate files.**

> ⚠️ **AMENDED — the ceiling moved, the decision did not.** ⭐ **What is untouched:** one file,
> the fixed sections, tiers as order. **What moved:** the line ceiling. **Why:** the original
> number was sized for an OPEN block; a CLOSED one adds a closing — verdict, what was learned,
> debt not closed — and the first real close landed above it with its long evidence already moved
> out. ⬜ **The live number is in the block contract, and validators READ it** rather than
> repeating it: ⛔ it had been hardcoded in four places, so raising it in one left the other three
> measuring the old number.

## Rejected alternatives

- ⛔ **One file per concern — a folder of seven or eleven.** ⚠️ Its premise is a different kind of
  agent, one that reads on request. ⭐ **Here nobody knows which of eleven to open, so they open
  none.**
- ⛔ **Split by tier — a file per reading depth.** ⚠️ The tiers are a READING ORDER, not a
  boundary: ⭐ **a reader who needs tier 2 needs tier 1 first, and now that is two files.**
- ⚠️ **One file, no ceiling.** The block becomes a transcript, and ⭐ **the sections that matter
  most sink below the ones written most.**

## Rationale

⛔ **Splitting a short file saves nothing and adds places that desynchronize.** ⚠️ The cost is not
the split — it is that after the split, two files can disagree and neither looks wrong alone.

> ## ⭐ A READER WHO MUST OPEN THREE FILES TO KNOW WHERE THE WORK STANDS OPENS NONE.

## Evidence

⭐ **Both directions were observed in one installation.**

| Shape | Outcome |
|---|---|
| ⭐ a single long file holding the whole cold-start context | **the most read document in the system** |
| ⛔ one subject scattered across five files | **nobody knew which to open** — the worst-served area |

⚠️ **The good case is longer than the bad one put together.** ⭐ **Length was never the problem;
scatter was.**

## Consequences

- `BLK-SHP-001` 🔒 — a sibling document beside the block file is a finding
- `BLK-SHP-002` 🔒 — the sections keep their order
- `DOC-SIZ-001` 🔒 — ⭐ the ceiling is DECLARED in the contract and READ from it, never repeated
- ⬜ `ADR-027` (planned) — ceilings per document type, ⭐ this decision generalised

## What would change this decision

⭐ **It stops being right if a block routinely needs more than a reader can hold in one pass.** ⚠️
The signal is not the line count — it is a closing whose evidence cannot be moved out because it
IS the block. ⛔ **Until then, a block that outgrows its ceiling is two blocks, not two files.**

## Reverting

⛔ **Split into multiple files.** ⚠️ The synchronisation problem returns, and with it the shape
where two files disagree and neither is wrong on its own.

---

Related: `ADR-010-cheap-to-open-expensive-to-close.md` (⭐ **the eleven sections are the FINAL shape, never the entry cost** — read together or this record reads stricter than it is) ·
`ADR-001-work-unit-is-the-block.md` (what a block IS) ·
`ADR-007-a-closed-block-is-archived.md` (the closing that made the ceiling move) ·
`../contract-block.md` (the sections and the live ceiling) · `../contract-adr.md`.
