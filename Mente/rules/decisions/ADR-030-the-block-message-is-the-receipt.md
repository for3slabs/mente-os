# ADR-030 · The block message IS the receipt

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: ADR-020-a-block-emits-an-approval-receipt.md — ⭐ the content was right, the FORM assumed an interface that does not exist
superseded-by: —
applies-to: the text a gate prints when it refuses
does-not-apply-to: ⭐ what a gate refuses — that is `ADR-012`, and this decision changes none of it

## Context

`ADR-020` specified a receipt: a screen with the piece, its propagation, the construction
assessment, and approve / inspect / deny. ⛔ **Before building it, the question was asked the other
way round: what do the existing messages already carry?**

## Decision

⭐ **The gate's block message IS the receipt** — the piece, the reason, what to assess, and the
documented way out, **printed as TEXT.** ⛔ **No separate artifact, and no approve / inspect / deny
flow.**

## Rejected alternatives

- ⛔ **Build the receipt as originally specified.** ⚠️ It adds one element to messages that already
  work, at the cost of editing a gate — ⭐ **and a gate is the last thing to edit for a cosmetic
  gain**, because the risk is that it stops refusing what it must.
- ⛔ **Keep both — a message AND a receipt.** ⚠️ Then the two drift, ⭐ **and the reader has to
  decide which one is current** at the exact moment they are being interrupted.
- ⚠️ **Fake the interactive flow in a non-interactive surface.** ⛔ ⭐ **A prompt that cannot
  actually be answered is worse than no prompt** — it teaches that the tool's questions are
  decorative.

## Rationale

> ## ⭐ THE RECEIPT'S CONTENT WAS RIGHT. ITS FORM ASSUMED A SURFACE THAT DOES NOT EXIST.
> ⚠️ **A pre-action hook has no interface for an interactive choice**, and inventing one would be
> worse than not having it.

⭐ **And each part of the content is already owned by a piece that reports it better:** propagation
is carried by the lane, chosen from the graph rather than judgment; the construction assessment is
the fix-not-patch rule, which the message points at.

## Evidence

⭐ **Measured before deciding, not after:** searching the tooling for any receipt implementation
returned **zero files**. ⛔ **Three of the original's four elements were already present** in the
gate messages; the fourth was information the gate already computes and reports elsewhere.

⭐ **And measured in this engine:** its one real gate prints the piece, the rule id, the measured
evidence for the rule, and the way out with its trace — ⚠️ **four parts, in text, with no receipt
anywhere.**

## Consequences

- `hooks/pre-commit.sh` — ⭐ **the shipped example**: refusal, rule id, measured evidence, and a
  documented escape that leaves a trace
- `HND-GAT-003` 📖 — the escape hatch announces itself: ⛔ a silent bypass is a removed gate
- ⛔ **`ADR-020` is superseded, not deleted** — ⭐ the pair is the record: a borrowed pattern, and
  what measuring it locally changed

## What would change this decision

⭐ **It returns to the original if a gate ever runs where an interactive surface exists.** ⚠️ The
argument was never that receipts are wrong — ⛔ **it was that the interface assumed did not exist,
and interfaces change.** The signal is a gate running somewhere that can actually accept
approve / inspect / deny.

## Reverting

⛔ **Reinstate the original.** ⭐ **The work is bounded and known:** reuse the propagation the first
gate already computes, in the messages of the others — ⚠️ plus tests that the gates still refuse
what they must, which is the part that is not cosmetic.

---

Related: `ADR-020-a-block-emits-an-approval-receipt.md` (⭐ **what this supersedes, and why the
content survived**) · `ADR-012-few-gates-block-the-rest-warn.md` (which gates exist at all) ·
`ADR-005-friction-protocol.md` (where a justified bypass is logged) · `../contract-adr.md`.
