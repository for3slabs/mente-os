# ADR-007 · A closed block is archived, never deleted

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: every block that reaches a closing
does-not-apply-to: ⭐ a block opened by mistake and closed with nothing done — there is no experience to keep, and the record says so

## Context

When a block closes, its context, its decisions and what it learned are at their most complete —
⛔ **and that is the exact moment the usual instinct is to clear it away.**

## Decision

**A closed block is ARCHIVED as completed, detailed as consultable experience. It does not die.**

## Rejected alternatives

- ⛔ **Delete on close.** ⚠️ The learning goes with it, and the next block hits the same wall
  without knowing anybody hit it before.
- ⛔ **Keep the block, drop the detail.** ⭐ **A one-line summary answers "did it happen"; it never
  answers "what would I do differently"** — and only the second is worth reading twice.
- ⚠️ **Move it to a separate archive store.** It stops being found by the same search that finds
  live work, ⭐ **and an archive nobody stumbles into is an archive nobody consults.**

## Rationale

> ## ⭐ THE ARCHIVE IS NOT STORAGE. IT IS PRECEDENT.
> ⚠️ **A closed block answers a question the live ones cannot:** *has anybody done this before,
> and what did it cost them?*

⛔ **And the value is asymmetric in time:** the cost of writing it is paid once, at close, by
whoever already has the context. The cost of NOT writing it is paid by every future reader, none
of whom has it.

## Evidence

⭐ **Measured in a real installation: 6 archived blocks, cited 64 times across the tree** — from
7 to 17 references each. ⛔ **Not one of those citations would resolve if the blocks had been
deleted on close.**

⚠️ **When this was decided, the evidence field said `none — judgment call`.** ⭐ **The judgment was
right, and now it is measurable** — which is the only reason this record can be defended rather
than merely believed.

## Consequences

- `ARC-SHP-001` 🔒 — an archive carries all three of its files, or it is not consultable
- `ARC-LRN-001` 🔒 — ⭐ **"what was learned" is never empty**: the one section that is not a copy
- `BLK-CLS-001` 🔒 — a closing section exists before the block may be marked closed
- ⬜ `ADR-021` (planned) — an error becomes a reusable case, ⭐ which needs somewhere to live

## What would change this decision

⭐ **It stops being right when the archive stops being consulted.** ⚠️ If the citation count of
archived work falls to near zero over a long period, the archive has become storage — ⛔ **and the
answer then is to fix why nobody finds it, not to start deleting.** Only if that fix fails twice
does deletion deserve a second look.

## Reverting

⛔ **Delete closed blocks.** ⚠️ The archive stops being a source of precedent, and every rule that
points at prior work — the reusable case, the connections a closing declares — points at nothing.

---

Related: `ADR-006-work-lives-in-version-control.md` (⭐ the history that makes archiving possible) ·
`ADR-001-work-unit-is-the-block.md` · `../contract-archive.md` (the shape an archive must have) ·
`../contract-adr.md`.
