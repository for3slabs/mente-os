# ADR-005 · Comply, log the friction, propose at close

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: every moment a rule obstructs the work in hand
does-not-apply-to: 🔴 real damage — that stops immediately and is raised, never logged and continued

## Context

⭐ **A rule that can never change is a rule people route around.** The friction does not disappear;
it moves out of sight, and the rule keeps looking obeyed while nothing follows it.

⛔ **But the two obvious answers both fail.** Asking the owner every time makes one person the
bottleneck for all work. Letting the agent change what obstructs it means ⚠️ **the rules are the
agent's again within a month**, and nobody decided that.

## Decision

When a rule gets in the way: ⭐ **comply · log the friction · keep going · propose the change at
close.** 🔴 **The one exception is real damage** — that stops immediately.

## Rejected alternatives

- ⛔ **Let the agent skip a rule it judges wrong.** ⚠️ Every rule looks wrong from inside the task
  it is obstructing — that is what a rule IS — so the judgment is made at the worst possible
  moment, by the party the rule exists to constrain.
- ⛔ **Ask the owner every time.** One person becomes the bottleneck, and ⭐ **the cost lands on
  the rule that fires most, which is usually the one working best.**
- ⚠️ **Log it and stop.** The work halts for a rule dispute, so the dispute is what gets
  remembered instead of the work.

## Rationale

> ## ⭐ A RULE CHANGES WHEN THE FRICTION IS MEASURED, NEVER WHEN IT IS FELT.
> ⚠️ **One person annoyed once is not evidence.** The same rule obstructing distinct pieces of
> work, repeatedly, is.

⭐ **Proposing at CLOSE is the load-bearing part.** By then the work is done, so the proposal is
argued from what the rule actually cost — ⛔ not from how it felt while it was in the way.

## Evidence

⭐ **The protocol has been observed working, which is more than it had when it was decided.** A
real block logged a friction against a gap in its own tooling, wrote the proposal into its
closing, and finished the work anyway:

> *"…the battery has no case that feeds a deliberately malformed input and asserts it refuses.
> 👉 Proposal: add that case. **Not done here** — it is outside this block."*

⛔ **Note what did NOT happen:** the block did not stop, did not fix the tooling out of scope, and
did not silently work around the gap. ⭐ **All three are what the protocol exists to prevent.**

⚠️ **When this was decided the evidence field said `none — process design`**, and that was the
honest answer at the time.

## Consequences

- `WRK-FRI-001` 📖 — comply first · ⛔ nothing can verify that the work stopped to think
- `WRK-FRI-002` 🔒 — each friction carries its four fields, or it is not a record
- `WRK-FRI-003` 🔒 — ⬜ a rule is flagged at a **declared** number of frictions in DISTINCT blocks
- `WRK-FRI-004` 📖 — a flagged rule is never changed automatically; it escalates

## What would change this decision

⭐ **It stops being right if logged frictions never produce a rule change.** ⚠️ The protocol trades
an immediate fix for a later, evidence-based one — ⛔ **if the later one never arrives, the trade
was a way of not answering.** The signal is frictions accumulating past the declared threshold with
no proposal raised at any close.

## Reverting

⛔ **Remove the log.** ⚠️ Rule evolution stops being evidence-based and becomes whoever argued last
— ⭐ **and the frictions do not stop happening, they stop being visible.**

---

Related: `ADR-004-three-friction-lanes.md` (the lanes this protocol runs inside) ·
`../rule-working-in-a-block.md` `WRK-FRI-*` · `../contract-adr.md`.
