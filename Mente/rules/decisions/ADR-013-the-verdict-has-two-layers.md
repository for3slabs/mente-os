# ADR-013 · The quality verdict has two layers

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: any judgment of whether work is finished to a standard
does-not-apply-to: ⭐ whether something WORKS — that is a test, and a test has one layer

## Context

⛔ **Somebody has to answer "is this finished?", and the obvious answerer is the one who did the
work.** ⚠️ That answer is worth less than it appears, and the reason is not dishonesty.

## Decision

**Two layers.** ⭐ **Layer 1 is MEASURED by a script** — no human criterion needed. ⭐ **Layer 2 is
CRITERION across six dimensions, each demanding EVIDENCE.**

> ## 🚫 THE AGENT DOES NOT DECLARE "THIS IS FINE." IT REPORTS THE MEASUREMENT.

## Rejected alternatives

- ⛔ **Trust the agent's assessment.** ⚠️ **It demonstrably flips** — not occasionally, and not
  under pressure: ⭐ **the same code produced opposite verdicts nine minutes apart, and the only
  thing that changed was context.**
- ⛔ **Layer 1 alone — measure and stop.** ⚠️ That is a linter. It sees a piece with five
  dependents; ⭐ **it cannot see whether five dependents mean the piece is well cut or badly cut.**
- ⛔ **Layer 2 alone — criterion and stop.** ⚠️ Then the verdict is an opinion with a form around
  it, ⭐ **and the form makes it harder to argue with, not easier.**

## Rationale

⭐ **The two layers fail in opposite directions, which is why neither is enough.** A measurement
with no criterion counts things nobody decided mattered; a criterion with no measurement is
whoever spoke last.

⚠️ **And the drift is directional, not random:** with the work fresh it reads finished; read cold,
the same files read halfway. ⛔ **Neither reading is dishonest** — that is what makes the problem
unsolvable by trying harder.

## Evidence

⭐ **Measured, and reproducible:**

```
21:15   "the system is complete"
06:33   "what is wrong is that this file implements it halfway"
```

⛔ **The same code. Opposite verdicts. Nine minutes apart.** The only event in between was a
context reset.

## Consequences

- `bin/grade-block` — layer 1: ⭐ **answers with numbers, and the numbers come from the tree**
- `rules/contract-quality-verdict.md` §5 — layer 2: the six dimensions and their required evidence
- `QLT-LAY-002` — ⬜ **the criterion is the installation's**, and a dimension without one reports
  `⬜`, never a pass
- `ADR-014` — who supplies that criterion, ⭐ **which is a different question from whether it exists**

## What would change this decision

⭐ **It stops being right if layer 1 ever answers the layer-2 questions.** ⚠️ If a measurement can
tell a well-cut piece from a badly-cut one, the second layer is ceremony — ⛔ **but the test is
whether two people reach the same verdict from the same numbers**, not whether the numbers look
sufficient to one of them.

## Reverting

⛔ **Return to an asserted verdict.** ⚠️ The contradiction returns with it — ⭐ **and it returns
invisibly, because each individual verdict still sounds confident.**

---

Related: `ADR-012-few-gates-block-the-rest-warn.md` (⭐ a red verdict LABELS, it does not block) ·
`ADR-014` (⬜ who supplies the criterion) ·
`../contract-quality-verdict.md` (both layers, in full) · `../contract-adr.md`.
