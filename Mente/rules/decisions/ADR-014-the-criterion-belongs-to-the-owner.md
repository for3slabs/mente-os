# ADR-014 · The criterion belongs to the owner, not the agent

date: {{date}}
status: accepted
implementation: in-progress
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: layer 2 of the quality verdict — the six dimensions and what each demands
does-not-apply-to: ⭐ layer 1 — a measurement needs no owner, and taking one would make it an opinion

## Context

`ADR-013` establishes that the verdict has a criterion layer. ⛔ **It does not say whose criterion
it is** — and that question has only two answers, with very different consequences.

## Decision

⭐ **The installation's owner supplies the dimensions and what each one demands. The agent APPLIES
them and brings the evidence.** ⛔ **It never issues its own opinion.**

## Rejected alternatives

- ⛔ **Agent-generated dimensions.** ⚠️ That is a linter with a longer output — ⭐ **it can only
  encode what is already common practice, and common practice is exactly what a senior criterion
  exists to disagree with.**
- ⛔ **A fixed set shipped by the engine.** ⚠️ It would be right for the project it was written in
  and wrong everywhere else, ⭐ **and being wrong-but-official is worse than being absent**: nobody
  replaces a default that looks authoritative.
- ⚠️ **The agent proposes, the owner approves.** ⛔ It sounds like a compromise and is not: ⭐ **the
  proposal anchors the answer**, and an owner reviewing a draft agrees with far more than an owner
  writing from scratch.

## Rationale

> ## ⭐ ANY LINTER HAS LAYER 1. WHAT NO LINTER HAS IS A SENIOR'S CRITERION.
> ⛔ **An agent that writes its own quality dimensions has written a linter and called it a
> review** — and it will pass its own work, not because it is dishonest, but because it graded
> itself against what it already knows.

⚠️ **The asymmetry is the point:** applying a criterion is mechanical and delegates well; ⭐
**deciding what counts as good does not**, because it encodes what this project is FOR.

## Evidence

⭐ **Four mature agent frameworks were examined, and none of them answers *"is this a product or an
MVP?"***. ⛔ **Zero quality verdicts among them** — they measure conformance, never sufficiency.

⚠️ **And the gap is not an oversight.** ⭐ **A framework cannot ship that answer**, because the
answer is specific to what the installation is building — which is the whole argument for who owns
it.

## Consequences

- `QLT-LAY-002` 📖 — ⭐ **the criterion is DECLARED by the installation**, never by the agent
- `QLT-DIM-002` 🔒 — a dimension with no declared criterion reports `⬜`, ⛔ never a pass
- ⬜ the six dimension rows ship EMPTY, and `bin/grade-block` counts how many are still unfilled
- `QLT-DIM-001` 📖 — a dimension is answered with EVIDENCE: ⛔ *"looks fine"* is not an answer

## What would change this decision

⭐ **It stops being right if an agent can be shown to produce criterion that its own work then
FAILS.** ⚠️ The test is not whether the dimensions sound sensible — ⛔ **it is whether they reject
work the agent was inclined to accept.** Until that is demonstrated, agent-written criterion is
self-assessment with extra steps.

## Reverting

⛔ **Let the agent write the dimensions.** ⚠️ Layer 2 degrades into layer 1 — ⭐ **and the
degradation is invisible, because the output still has six sections and still looks like a
review.**

---

Related: `ADR-013-the-verdict-has-two-layers.md` (⭐ **that the layer exists; this one, whose it
is**) · `../contract-quality-verdict.md` §5 (the six dimensions, shipped empty) ·
`../contract-adr.md` (⛔ `DEC-NUM-004` — why this record is not named after a person).
