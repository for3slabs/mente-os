# ADR-018 · The system governs HOW it communicates

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: every response the system produces, in any mode
does-not-apply-to: ⭐ the owner's own writing — ⛔ this governs what the system says, never how a person writes

## Context

⛔ **The same complaint was made about the code and about the prose**, in the same words: *it feels
machine-made*. ⭐ **Same disease, two surfaces: correct FORM produced without judgment.**

## Decision

**The system governs how it communicates — transversally, not as another owner.** ⭐ **The rules are
NEGATIVE and CHECKABLE:** what must not appear, not what should be aimed for.

## Rejected alternatives

- ⛔ **Vague guidance — "be clear", "be concise".** ⚠️ ⭐ **That is the KIND of instruction that
  causes the problem:** it produces text shaped like an answer, because shape is the only thing a
  vague instruction can be satisfied by.
- ⛔ **A fourth owner, alongside the others.** ⚠️ Then voice applies only where that owner is
  invoked, ⭐ **and the responses nobody assigned an owner to are exactly the ones that drift.**
- ⚠️ **Positive rules — "write like this".** ⛔ ⭐ **A positive rule is satisfied by imitation**; a
  negative one is checkable, and a reader can point at the violation.

## Rationale

> ## ⭐ CORRECT FORM WITHOUT JUDGMENT IS THE FAILURE, AND IT LOOKS LIKE SUCCESS.
> ⚠️ **A response with the right shape passes every review that reads shape** — which is most of
> them.

⛔ **And a rule about writing must be refutable.** ⚠️ *"Be clear"* cannot be violated visibly; ⭐
**"never open by validating the question" can be pointed at**, which is the only way a style rule
is ever enforced.

## Evidence

⭐ **Measured before the decision: there were no style rules at all.** ⛔ The startup file carried
zero, no style definition existed, and the configuration named none — ⚠️ **nobody had written the
file, and the absence read as "no style needed" rather than as a gap.**

## Consequences

- `contract-delivery.md` — ⭐ the shape a delivery takes, and what must never appear in one
- ⬜ the voice is declared once and applies to every response, ⛔ **not per task**
- ⭐ **the rules are negative** — each one names something checkable that must not happen

## What would change this decision

⭐ **It stops being right if the negative rules produce text that obeys all of them and still reads
machine-made.** ⚠️ Then the rules are catching the symptoms and missing the cause — ⛔ **and the
test is a reader who cannot name which rule was broken but can tell something is wrong.**

## Reverting

⛔ **Remove the voice declaration.** ⭐ **One line, fully reversible** — ⚠️ and the drift returns
gradually, which is why nobody notices it was removed.

---

Related: `ADR-014-the-criterion-belongs-to-the-owner.md` (⭐ **the same split**: the system supplies
form, the owner supplies judgment) · `../../memory/principles/contract-delivery.md` ·
`../contract-adr.md`.
