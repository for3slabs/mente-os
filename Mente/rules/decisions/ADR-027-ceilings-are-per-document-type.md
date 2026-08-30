# ADR-027 · Ceilings are per document TYPE, and the limit is a signal

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: every document the system governs, not only the ones it creates
does-not-apply-to: ⭐ an append-only record — ⛔ a log is meant to grow, and capping it would delete history to satisfy a number

## Context

`ADR-009` bounds one document: the block file. ⛔ **Everything else in the system was unbounded**,
including the documents describing the system itself — which are the ones written most.

## Decision

**Size limits are declared PER DOCUMENT TYPE, across the whole system.**

> ## ⭐ A FILE IS SPLIT WHEN IT HOLDS TWO DISTINCT THINGS. THE LIMIT IS THE SIGNAL, NEVER THE CAUSE.
> ⛔ **Hitting the ceiling is not the problem** — it is the notification that the problem already
> happened.

## Rejected alternatives

- ⛔ **One global limit.** ⚠️ A log must be allowed to grow and a router must not; ⭐ **a single
  number is wrong for both**, and being wrong for the log is what gets the whole mechanism
  discredited.
- ⛔ **No limits, split by judgment.** ⚠️ ⭐ **Judgment about size is made by the person adding to
  the file**, at the moment they are adding — and it never says stop.
- ⚠️ **A limit that truncates rather than flags.** ⛔ Then content is lost to satisfy a number,
  ⭐ **which is the one outcome worse than an overlong file.**

## Rationale

⭐ **The ceiling does not decide anything — it asks a question:** *does this file hold two distinct
things?* ⛔ **If the answer is no, the ceiling was set wrong and is raised by declaring it.** If the
answer is yes, the split was already due.

⚠️ **And per-TYPE is what makes the question answerable.** ⭐ A number chosen for one kind of
document is meaningless against another, so a global limit makes every answer *"the limit is
wrong"* — and then nobody looks for the second thing.

## Evidence

⭐ **Measured, and both directions in the same system:** one architecture document went from **995
to 2,347 lines in a SINGLE session.** ⛔ **The only file with a declared limit was the only one that
never overflowed.**

⚠️ **And the mechanism has fired since, on this engine:** a contract crossed its declared ceiling
and produced a recorded split rather than a silent raise. ⭐ **That is the decision working as
designed** — the ceiling asked its question and the answer was written down.

## Consequences

- `DOC-SIZ-001` 🔒 — ⭐ over the ceiling → **a named split**, verified as recorded work
- ⬜ **the ceilings live in the contract and are READ from it**, never repeated in code — ⛔ they
  had been hardcoded in several places, so raising one left the others measuring the old number
- ⭐ **raising a ceiling is a documented act:** the new number carries its reason in the table
- `ADR-009` — the block ceiling, which this decision generalises

## What would change this decision

⭐ **It stops being right if ceilings are raised more often than splits happen.** ⚠️ Then the
numbers are tracking the files rather than bounding them — ⛔ **and a limit that moves whenever it
is reached is a limit in name only.** The signal is a ceiling raised twice for the same document
with no split between the raises.

## Reverting

⛔ **Remove the limits.** ⚠️ Expect the drift that produced files measured in hundreds of kilobytes
— ⭐ **and the drift is invisible in the moment, because no single addition is ever the one that
broke it.**

---

Related: `ADR-009-one-file-per-block.md` (⭐ **the one ceiling this generalises** — it announced
this record as ⬜ planned) · `../contract-document.md` (the ceiling table, and the rule that reads
it) · `../../docs/ENGINE-BACKLOG.md` (⚠️ E-34 — the split this mechanism produced) ·
`../contract-adr.md`.
