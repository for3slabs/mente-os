# ADR-028 · The type changes the ruler, never the bar

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: measuring the quality of any block, whatever it contains
does-not-apply-to: ⭐ layer 2 — ⛔ criterion does not vary by type, only what can be MEASURED does

## Context

`ADR-013` gives the verdict two layers, and layer 1 measures. ⛔ **But a documentation block has no
test file to be missing, and an infrastructure block has no import graph** — measuring them by one
ruler produces reds that mean nothing.

## Decision

**A block declares a required `type`, and only the metrics that apply to it are measured.** ⭐
**Every non-applicable metric prints as `n/a` WITH the reason it was skipped.**

🔴 **Two rules that do not bend:**

1. ⛔ **`n/a` is never counted as green.**
2. ⭐ **The type changes the RULER, never the BAR** — every type still reaches a verdict.

## Rejected alternatives

- ⛔ **One ruler for everything.** ⚠️ ⭐ **A validator that can never go green is one you learn to
  ignore** — and then the doctrine is a document again, which is the failure the whole system
  exists to fix.
- ⛔ **Refuse to grade non-code blocks.** ⚠️ Then documentation and infrastructure close on an
  assertion, ⭐ **which is the original pain**: the same work called complete and half-done nine
  minutes apart.
- ⚠️ **Let the type lower the bar — fewer checks, easier verdict.** ⛔ ⭐ **Then `type` becomes the
  field you set to pass**, and every block is documentation by declaration.

## Rationale

> ## ⭐ THE RULER CHANGES. THE BAR DOES NOT.
> ⛔ **A skipped metric is not a passed metric**, and the only thing keeping those apart is that
> the report says which is which.

⚠️ **And the reason must be printed, not implied.** ⭐ **`n/a` with no reason is indistinguishable
from a metric that was forgotten** — the reader cannot tell a considered exclusion from an
oversight.

## Evidence

⭐ **Measured on this engine: nine real blocks graded across four types**, each reaching a verdict —
🟢 product, 🔴 MVP, and ⬜ nothing-measured — ⛔ **with no type left ungradeable.**

⚠️ **And the rule that `n/a` is never green is enforced, not stated:** the report prints skipped
metrics with their reason, and a probe asserts that no `n/a` row renders as a pass.

## Consequences

- `QLT-TYP-001` 🔒 — a block declares its type, or it cannot be graded
- `QLT-TYP-002` 🔒 — ⭐ **a metric that does not apply is `⬜`, never a pass**
- `QLT-TYP-003` 🔒 — 🔴 a pasted secret is red for EVERY type: ⛔ no block kind is exempt
- `QLT-EVD-001` — ⭐ zero measured files is `NOTHING MEASURED`, ⛔ never a pass

## What would change this decision

⭐ **It stops being right if `type` starts being chosen for the verdict it produces.** ⚠️ The field
is declarative and nothing verifies that a block's type matches its content — ⛔ **so the failure
mode is a code block declared as docs.** The signal is a block whose declared type does not match
what its scope actually holds.

## Reverting

⛔ **One ruler for all types.** ⚠️ Non-code blocks go permanently red, ⭐ **and a permanent red is
read as a broken validator rather than as broken work.**

---

Related: `ADR-013-the-verdict-has-two-layers.md` (⭐ **the layer this refines**) ·
`../contract-quality-verdict.md` §2 (the ruler per type) · `../contract-adr.md`.
