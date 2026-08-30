# ADR-004 · Three lanes, chosen by propagation

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: every change made inside a block
does-not-apply-to: ⭐ a change with no consumers anywhere — nothing propagates, so nothing to weigh

## Context

Once the block exists as a unit of work (`ADR-001`), every change needs an answer to *how much
ceremony does this deserve*. ⛔ **One answer for everything is wrong in both directions:** heavy
enough to protect the dangerous change is unbearable for the trivial one, and light enough for the
trivial one protects nothing.

## Decision

**Three lanes — `direct`, `task`, `full-block`** — and ⭐ **the lane is chosen by PROPAGATION, not
by judgment.**

## Rejected alternatives

- ⛔ **The agent estimates the lane.** It mislabels work as trivial — ⚠️ **and it mislabels in one
  direction only**, because the estimate is made from the file that was opened, never from the
  files that change with it.
- ⛔ **A single lane for everything.** ⚠️ Either unbearable friction on every change, or no
  protection on any.
- ⚠️ **Two lanes.** Nothing separates *"one piece, no consumers"* from *"one piece, many
  consumers"* — ⭐ and that gap is exactly where the expensive changes hide.

## Rationale

> ## ⭐ THE LANE IS A MEASUREMENT, NOT AN OPINION.
> ⛔ **An estimate is always the smaller one**, because it is made before the graph is read.

⚠️ **And the cost of getting it wrong is asymmetric:** too much ceremony on a trivial change is
annoying; too little on a propagating one is a fix over a fix over a fix.

## Evidence

⭐ **Measured:** a change described as *"store one value where it really belongs"* was labelled a
task. The piece it touched had **five dependents**. ⛔ **It produced 21 edits, and 42% of the
commits in that period were fixes** — of the fix.

## Consequences

- `WRK-LAN-001` — the lane comes from the dependency graph, never an estimate
- `WRK-LAN-002` — declared dependents → `full-block`, always
- `WRK-LAN-003` — the lane is written in the block's identity, so it can be argued with
- ⭐ `WRK-LAN-005` — **nothing is edited before the scope is known**: the lane must be chosen
  first, which is only possible because the graph is measured first

## What would change this decision

⭐ **It stops being right if the lane never changes the work.** ⚠️ If `full-block` and `task`
produce the same behaviour in practice — same measurement, same care — then the lanes are labels,
not lanes. ⛔ **The test is not how often each is chosen; it is whether choosing differently
changed what was done.**

## Reverting

⛔ **Collapse to one lane.** ⚠️ Whichever weight is chosen is wrong for half the work: heavy means
the standard is abandoned, light means it protects nothing — ⭐ **and an abandoned standard
protects nothing either, so the light choice only looks safer.**

---

Related: `ADR-001-work-unit-is-the-block.md` (the two levels this decision reads) ·
`../rule-working-in-a-block.md` (the lane rules it produced) · `../contract-adr.md`.
