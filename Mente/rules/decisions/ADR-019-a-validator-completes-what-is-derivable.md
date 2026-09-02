# ADR-019 · A validator completes what is derivable — and only that

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: anything a check could compute instead of asking for
does-not-apply-to: 🔴 criterion, scope and verdict — ⛔ those are decided, never derived

## Context

⛔ **A check that only warns is a check that gets ignored, and the ignoring is invisible.** The
warning fires, the work continues, and nothing records that the gap is still there.

## Decision

**What a validator can DERIVE, it completes.** ⭐ A graph, an index, a draft marked as generated.
🔴 **What it cannot derive — criterion, scope, a verdict — it never touches.**

⚠️ **And the completion is announced, never silent:** ⭐ **a read-only command that quietly
modified something would make the whole set untrustworthy**, including the checks that did behave.

## Rejected alternatives

- ⛔ **Verify only.** ⚠️ Measured: a rule warned and was broken five times out of eleven — ⭐ **it
  would have warned five times and left five gaps**, because a warning is a request and the work
  is always more urgent than the request.
- ⛔ **Complete everything the validator can compute, including drafts of judgment.** ⚠️ A derived
  verdict is a verdict nobody took, ⭐ **and it is harder to disagree with than a blank**, because
  it arrives already written.
- ⚠️ **Let each check decide whether it writes.** ⛔ Then no command can be trusted to be
  read-only, ⭐ **and the cost is paid by every check, not just the ones that write.**

## Rationale

> ## ⭐ WHAT CAN BE DERIVED AND IS ASKED FOR INSTEAD IS A QUESTION WITH A KNOWN ANSWER.
> ⚠️ **Asking it costs attention every time**, and attention spent on a known answer is attention
> not spent on the ones that are open.

⛔ **But the line is not "what is convenient".** It is **what is DERIVABLE** — computable from what
already exists, with no judgment added. ⭐ **Criterion, scope and verdict fail that test by
definition:** if they could be computed, they would not need an owner.

## Evidence

⭐ **Measured: a rule requiring a record before a context reset was broken five times out of
eleven.** ⛔ **It existed, it was documented, and it warned** — the failure was not ignorance.

⚠️ **And the cure it eventually received is worth recording, because it was NOT completion:** the
same rule is now a lock with a validator behind it. ⭐ **Completion and blocking are two answers to
the same failure** — this decision says which cases deserve which, and that a warning alone
deserves neither.

## Consequences

- ⭐ **Two generators complete what they derive, and announce it** —
  `../../bin/generate-index` and `../../bin/generate-metrics`, each writing exactly ONE file and
  printing what it wrote. ⚠️ Measured 2026-09-02; this line read *"nothing completes anything
  yet"* until then, and had been false since the generators shipped
- ⭐ **The engine already ships the sharper half of this rule:** a validator never writes unless
  its NAME says so, so `check-*` and `grade-*` read while `generate-*` writes
- ⭐ **The generators exist and the naming rule governs them** — ⚠️ the rule landed first, which
  is the order this decision wantedverns
- 🔴 the exclusion holds regardless: ⛔ **no generator may derive a criterion, a scope or a verdict**

## What would change this decision

⭐ **It stops being right if a completion is ever wrong and nobody notices.** ⚠️ A derived value
carries the authority of the tool that wrote it — ⛔ **so a wrong derivation is trusted longer than
a wrong human entry.** The signal is a generated file whose content is corrected by hand: ⭐ **that
is the derivation admitting it was not derivable.**

## Reverting

⛔ **Restrict validators to reporting.** ⚠️ The omissions persist and stay invisible — ⭐ **the
system reports them at exactly the rate it always did, which reads like stability.**

---

Related: `ADR-012-few-gates-block-the-rest-warn.md` (⭐ **blocking is the other answer** to the same
failure — read together, or completion looks like the only option) ·
`../../bin/README.md` (the naming rule that keeps read-only commands trustworthy) ·
`../contract-adr.md`.
