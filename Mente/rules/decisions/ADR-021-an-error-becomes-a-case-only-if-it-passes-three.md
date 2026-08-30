# ADR-021 · An error becomes a case only if it passes three questions

date: {{date}}
status: accepted
implementation: not-started
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: an error worth writing down for somebody who has not made it yet
does-not-apply-to: ⭐ a fix — ⛔ a wrong line corrected is not a case, however expensive it was

## Context

⛔ **Every error looks worth recording at the moment it is understood**, and that moment is the
worst one to judge from: the cost is fresh and the recurrence is imagined.

## Decision

**An error becomes a reusable case only if it passes three questions:**

1. ⭐ **would it recur ELSEWHERE** — not "could it", but is there a second place with the same shape
2. ⭐ **was the cause a wrong CRITERION** — ⛔ not a wrong line, a wrong way of deciding
3. ⭐ **can it be written as an ACTIONABLE rule** — something a reader does differently tomorrow

⬜ **Plus two declared limits:** an automatic threshold at N repetitions, and a cap on active cases.

## Rejected alternatives

- ⛔ **No filter — every error becomes a case.** ⚠️ Measured elsewhere in this system: unbounded
  collections reach dozens in months, ⭐ **and a collection nobody finishes is a collection nobody
  consults** — including the three entries that were worth it.
- ⛔ **A filter with one question ("was it expensive?").** ⚠️ Cost measures the past; ⭐ **the three
  questions measure whether the future changes.** An expensive one-off teaches nothing.
- ⚠️ **A filter with no cap.** ⛔ The questions bound what ENTERS, never what accumulates — ⭐ and a
  set that only grows eventually fails the same way an unfiltered one does, just later.

## Rationale

> ## ⭐ A CASE IS NOT A RECORD OF WHAT WENT WRONG. IT IS AN INSTRUCTION FOR SOMEBODY WHO HAS NOT DONE IT YET.
> ⛔ **The three questions all test the same thing from different sides:** does this change what
> the next person does?

⚠️ **Question 2 is the one that rejects most:** ⭐ **a wrong line is a fix; a wrong way of deciding
is a case.** The first is corrected once, the second recurs until the criterion changes.

## Evidence

⭐ **Measured, and the filter proved sharper than expected:** in a real installation the three
questions admitted **exactly one** error as a case over months of work — ⛔ **and that one case is
cited by nineteen files.**

⚠️ **The cap was never tested**, because the filter was strict enough that nothing approached it.
⭐ **That is the result the decision wanted**, and it is worth recording that the limit which did
the work was the FILTER, not the ceiling.

## Consequences

- ⬜ **Nothing implements this yet** — ⛔ the engine's document types are contract, rule and
  decision; **a case is none of the three**, and the type table says so
- ⬜ **What it would take:** a fourth type with its own shape, plus the two declared limits
- ⚠️ ⭐ **Until then, a case-shaped document is a rule with a story in it** — which works, and
  loses the filter

## What would change this decision

⭐ **It stops being right if the filter admits nothing over a long period while the same errors
keep recurring.** ⚠️ Then the questions are not selecting, they are refusing — ⛔ **and the signal
is not the count of cases, it is repeated errors that never became one.**

## Reverting

⛔ **Remove the filter, or the cap.** ⚠️ The case folder becomes the long file nobody reads — ⭐
**and it does so gradually, so no single addition is ever the one that broke it.**

---

Related: `ADR-007-a-closed-block-is-archived.md` (⭐ **where a case's raw material comes from** —
it announced this record as ⬜ planned) · `../README.md` (⛔ **the three document types a case is
not**) · `../contract-adr.md`.
