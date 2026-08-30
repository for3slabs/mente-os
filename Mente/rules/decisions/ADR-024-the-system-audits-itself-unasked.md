# ADR-024 · The system audits itself, unasked

date: {{date}}
status: accepted
implementation: in-progress
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: checking the system's own health, on its own initiative
does-not-apply-to: 🔴 deleting anything it finds — ⛔ an audit reports; ⭐ forensic evidence is never removed by the thing that found it

## Context

⛔ **Three real failures lived for WEEKS and were found by somebody asking.** Not by a check, not
by a report — by a question that happened to be asked.

## Decision

⭐ **A health check audits the system and runs BY ITSELF when a session opens.**

> ## ⭐ IF YOU HAVE TO ASK FOR IT, IT IS NOT AUTOMATED.

🔴 **And it never deletes what it finds.** ⛔ An audit that cleans up destroys the evidence of how
the state was reached.

## Rejected alternatives

- ⛔ **Manual audit on request.** ⚠️ ⭐ **That is exactly what failed** — the audit existed and was
  available, and three failures survived weeks because nobody thought to run it.
- ⛔ **Audit that fixes what it finds.** ⚠️ Then a recurring fault is repaired silently forever,
  ⭐ **and the pattern that produced it is never visible** — the system looks healthy precisely
  because it is being repaired every morning.
- ⚠️ **Audit on a schedule rather than at session start.** ⛔ The findings arrive when nobody is
  working, ⭐ **and a finding read hours later is read as history, not as a decision to make.**

## Rationale

⭐ **An automated check and a requestable one differ in exactly one way, and it is the one that
matters:** ⛔ **the requestable one is not run on the day it would have mattered**, because that is
the day everybody is busy with the thing it would have caught.

⚠️ **And the constraints on it are as important as its existence** — ⭐ **a startup check that
blocks the session, or that talks on every healthy run, is removed within a week.**

## Evidence

⭐ **Measured: three distinct failures, each alive for WEEKS.** ⛔ **All three were found by a
question, not by a mechanism** — a permission grant nobody revoked, an index claiming a count
twenty short of reality, and hundreds of stale files.

⚠️ **None of the three was hidden.** ⭐ **Every one was visible to a check that existed and was not
run** — which is the entire argument.

## Consequences

- ⬜ **The health check does not exist here yet** — `in-progress`, and the engine says so
- ⭐ **The principle already ships:** a validator audits the validators themselves, so the
  self-audit idea is proven even where the startup hook is not
- ⚠️ **The two constraints ship as rules, ahead of the tool they govern:** ⛔ never block the
  session at startup, and ⭐ **speak only when something is wrong** — silence is the healthy output
- 🔴 the no-deletion boundary holds regardless of what runs it

## What would change this decision

⭐ **It stops being right if the automatic run is silently disabled and nobody notices.** ⚠️ An
audit that has been switched off looks exactly like an audit finding nothing — ⛔ **and that is a
worse state than never having had one**, because the silence is now trusted. The signal is a
health check with no recorded run in a long period.

## Reverting

⛔ **Unhook it from startup.** ⚠️ The system stops watching itself — ⭐ **and it stops silently, on
a day when everything happened to be fine.**

---

Related: `ADR-012-few-gates-block-the-rest-warn.md` (⭐ **an audit warns, it never blocks**) ·
`ADR-019-a-validator-completes-what-is-derivable.md` (⚠️ and it never deletes) ·
`../../hooks/README.md` (⭐ the two constraints, shipped ahead of the tool) · `../contract-adr.md`.
