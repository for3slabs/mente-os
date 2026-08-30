# ADR-023 · Everything read as an INSTRUCTION is in one declared language

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: anything the agent reads as an instruction — rules, contracts, block files, field names, paths
does-not-apply-to: ⭐ the owner's THINKING — ⛔ notes, reasoning, conversation and the record of a decision's origin stay in whatever language it was thought in

## Context

⛔ **An instruction and a thought are not the same artifact**, and treating them as one forces a
choice that damages whichever side loses.

## Decision

⭐ **Everything the agent reads as an INSTRUCTION is in ⬜ one declared language** — including field
names, paths, and the block file itself. ⭐ **The owner's thinking stays in theirs.**

⬜ **The engine ships in US English** and fixes that there is ONE instruction language, never which
one — ⚠️ **but a mixed set is the failure, not either choice.**

## Rejected alternatives

- ⛔ **Everything in the owner's language.** ⚠️ Field names and paths lose precision: ⭐ **an
  identifier that must be translated to be matched is an identifier that will eventually be
  mismatched.**
- ⛔ **Everything in the instruction language, thinking included.** ⚠️ The owner writes worse in a
  second language, ⭐ **and the criterion — the part no tool can supply — is exactly what degrades
  first.**
- ⚠️ **Mixed, decided case by case.** ⛔ ⭐ **Then every file is a small decision**, and the answer
  drifts by author and by mood until nothing is predictable.

## Rationale

> ## ⭐ THE SPLIT IS BY ROLE, NOT BY TASTE.
> ⛔ **An instruction is matched, resolved and cited** — it needs one spelling. ⭐ **A thought is
> read by a person** — it needs the language they think in.

⚠️ **And the cost of getting this wrong is asymmetric:** a badly-worded thought is re-read; ⛔ **a
mismatched identifier fails silently.**

## Evidence

⭐ **Measured in this engine: 39 of 39 rule and principle documents, and 47 of 47 executables and
templates, are in the instruction language.** ⛔ **The exceptions are three FILENAMES**, recorded
as a known gap rather than tolerated silently.

⚠️ **And the counter-check matters as much:** ⭐ **writing the thinking in the owner's language was
verified NOT to degrade comprehension.** The expensive failures this system has measured came from
missing structure, never from language.

## Consequences

- `DOC-NAM-001` 🔒 — the naming rule that keeps identifiers matchable
- ⬜ **the instruction language is declared once** and every document inherits it
- ⚠️ **filenames are instructions too** — ⭐ a name is resolved and cited, so it follows the
  instruction language even when its content is a translated thought

## What would change this decision

⭐ **It stops being right if identifier matching stops depending on spelling.** ⚠️ The whole
argument rests on an instruction being matched literally — ⛔ **if resolution became reliably
language-independent, the split would be costing precision it no longer buys.** Nothing observed
suggests that yet.

## Reverting

⛔ **Translate the instructions.** ⚠️ Precision in field and path resolution degrades — ⭐ **and it
degrades silently, one mismatch at a time, each of which looks like a typo rather than a policy.**

---

Related: `../contract-document.md` (⭐ the naming rule this produced) ·
`../../docs/ENGINE-BACKLOG.md` (⚠️ **E-24 — three filenames that do not follow it**, and this
record is the criterion that decision was missing) · `../contract-adr.md`.
