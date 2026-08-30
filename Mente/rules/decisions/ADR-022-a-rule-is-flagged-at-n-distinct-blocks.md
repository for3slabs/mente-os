# ADR-022 · A rule is flagged at N frictions in DISTINCT blocks

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: deciding when a rule has earned a review
does-not-apply-to: 🔴 a rule that caused real damage — ⛔ that escalates immediately, without waiting for a count

## Context

`ADR-005` says a friction is logged and the work continues. ⛔ **Logging without a trigger is a
pile**, and a pile is read once, at the end, by nobody.

## Decision

**A rule is flagged for review at ⬜ N frictions in DISTINCT blocks.** ⭐ **It never expires**, and
⛔ **the rule is never changed automatically** — it escalates to whoever owns the criterion.

## Rejected alternatives

- ⛔ **Count raw repetitions, anywhere.** ⚠️ Any long task raises false alarms — ⭐ **the same rule
  chafing five times in one afternoon is one situation, not five**, and treating it as five is how
  the mechanism gets ignored.
- ⛔ **A threshold that expires.** ⚠️ Then a rule that chafes twice a year forever is never flagged,
  ⭐ **and slow friction is exactly the kind nobody remembers to raise.**
- ⚠️ **Let the agent judge when a rule has earned review.** ⛔ ⭐ **A mechanism that needs judgment
  to fire does not fire** — the judgment is required at the moment the rule is inconvenient.

## Rationale

> ## ⭐ DETECTION IS ARITHMETIC, NOT INTERPRETATION.
> ⛔ **Anything that requires somebody to decide "does this count?" will be decided as no**, on the
> day it matters, by the person the rule is obstructing.

⚠️ **And DISTINCT is the load-bearing word.** ⭐ **One block chafing repeatedly is evidence about
the block; three blocks chafing once each is evidence about the RULE** — which is the only thing
worth reviewing a rule over.

## Evidence

⛔ **none from a firing — the mechanism has never triggered.** ⭐ **And that is measurable rather
than assumed:** in a real installation, five blocks carry logged frictions and **no rule reaches
three distinct blocks.**

⚠️ **Which is the expected result, not a failure:** ⭐ **a threshold that fires often is a threshold
set too low.** ⛔ What would be evidence against the decision is frictions accumulating in distinct
blocks *without* the count rising — and that has not happened either.

## Consequences

- `WRK-FRI-003` 🔒 — ⭐ **the count is over DISTINCT blocks**, held as a set, verified
- `WRK-FRI-005` — ⬜ the agent never infers N; an undeclared threshold is reported as the default
- `WRK-FRI-004` 📖 — ⛔ a flagged rule is never changed automatically; it escalates
- ⬜ `friction_threshold` is declared in the rule, ⭐ **so raising it is a documented act**

## What would change this decision

⭐ **It stops being right if flagged rules are never actually reviewed.** ⚠️ The trigger is only
worth its arithmetic if something happens when it fires — ⛔ **and a flag that raises no review is
a warning with a counter attached.** The signal: a rule reaching the threshold and staying
unchanged and undiscussed through the next close.

## Reverting

⛔ **Count raw repetitions.** ⚠️ Expect false alarms, and then the mechanism gets ignored — ⭐ **and
it gets ignored as a whole, including the true positives it would have caught later.**

---

Related: `ADR-005-friction-protocol.md` (⭐ **the protocol that produces the frictions this
counts**) · `ADR-012-few-gates-block-the-rest-warn.md` (⚠️ a flag is not a block) ·
`../rule-working-in-a-block.md` `WRK-FRI-*` · `../contract-adr.md`.
