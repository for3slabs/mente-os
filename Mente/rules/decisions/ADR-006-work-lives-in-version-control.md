# ADR-006 · The work itself lives in version control

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: every block, its closing, and the records that describe it
does-not-apply-to: ⛔ secrets and generated artefacts — those are ignored on purpose, and their absence is declared

## Context

⭐ **A unit of work whose history is not versioned cannot be audited.** Not *"is harder to
audit"* — cannot: there is no state to compare against, and no way back to one.

## Decision

**Blocks live inside the system, versioned in the same repository as the code they govern.**

## Rejected alternatives

- ⛔ **A separate store outside version control.** ⚠️ It drifts from the code it describes, and
  nothing detects the drift — ⭐ **the two are only in sync while somebody remembers to sync them.**
- ⛔ **A database.** ⚠️ It answers *what is the state now* and loses *what was the state when this
  was decided*, which is the question an audit asks.
- ⚠️ **Versioned, but in its own repository.** ⭐ **A block and the code it governs then move in
  separate histories**, so a change and the reason for it can never be seen in one diff.

## Rationale

> ## ⭐ WHAT IS NOT VERSIONED CANNOT BE REVERTED, AND WHAT CANNOT BE REVERTED CANNOT BE RISKED.
> ⚠️ **The cost is not losing the file. It is that nobody will change it boldly again.**

## Evidence

⭐ **Measured in a real installation:** the blocks and their closings are **35 files under version
control, touched by 26 commits** — every one of those a state the work can be returned to.

⛔ **And the counter-example, measured in the same installation:** its long-form memories live
OUTSIDE version control. ⚠️ **When one of them broke, there was no history to revert to** — the
only recovery was rewriting it from what somebody remembered.

## Consequences

- `SHP-LCK-001` 🔒 — a commit on the base branch is refused, with a real hook behind it
- `ADR-007` — a closed block is ARCHIVED rather than deleted, ⭐ **which is only meaningful
  because the history exists**
- `ADR-012` — the gates can refuse an action, because there is always a state to refuse back to

## What would change this decision

⭐ **It stops being right if the history stops being readable:** a repository so large that
`log` on a block is unusable, or a hosting arrangement where the work cannot be cloned by whoever
needs to audit it. ⛔ **Neither has been observed — and if either is, the answer is to split the
repository, never to leave version control.**

## Reverting

⛔ **Move the work out of version control.** ⚠️ Its history goes with it, and every rule that
assumes a previous state — the archive, the gates, the closing — loses the thing it compares
against.

---

Related: `ADR-001-work-unit-is-the-block.md` (what is being versioned) ·
`../rule-shipping.md` (how a change leaves) · `../contract-archive.md` (why closing is not
deleting) · `../contract-adr.md`.
