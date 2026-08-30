# ADR-020 · A block emits an approval receipt

date: {{date}}
status: superseded
implementation: not-started
decided-by: ⬜ declare
supersedes: —
superseded-by: ADR-030-the-block-message-is-the-receipt.md
applies-to: the moment a gate refuses an action
does-not-apply-to: a warning — ⭐ nothing is being refused, so there is nothing to approve

## Context

⛔ **Blocking without an exit is pure friction**, and pure friction is what gets a gate switched
off. The question is not whether to block — `ADR-012` answers that — but what the block must SAY.

## Decision

⚠️ **When a gate blocks, it emits an APPROVAL RECEIPT:** one screen carrying the piece, its
propagation, the construction assessment, and an **approve / inspect / deny** choice.

## Rejected alternatives

- ⛔ **Block with a bare error message.** ⚠️ The reader learns that something was refused and not
  why, ⭐ **so the only available response is to retry or to disable the gate.**

## Rationale

⭐ **A refusal is a conversation the tool starts.** ⛔ Starting it without saying what would satisfy
the objection makes the tool the obstacle rather than the check.

## Evidence

⛔ **none — adopted from an external reference.** ⚠️ The pattern was borrowed, not measured here,
and ⭐ **that is exactly what its successor found**: three of its four elements already existed in
the messages, and the fourth was unreachable in the interface it assumed.

## Consequences

⛔ **Superseded before implementation.** ⭐ See `ADR-030`, which keeps the CONTENT and drops the
form.

## What would change this decision

⭐ **It would return if a gate ever runs somewhere with a real interactive surface.** ⚠️ The
successor's argument is not that receipts are wrong — ⛔ **it is that the interface assumed did not
exist**, and an interface is a thing that can change.

## Reverting

⛔ **Remove the receipt; gates become walls.** ⚠️ Which is what the successor had to prevent while
removing the receipt — ⭐ **and it did, by moving the content into the message.**

---

Related: `ADR-030-the-block-message-is-the-receipt.md` (⭐ **what replaced it, and what it kept**) ·
`ADR-012-few-gates-block-the-rest-warn.md` (when to block at all) · `../contract-adr.md`.
