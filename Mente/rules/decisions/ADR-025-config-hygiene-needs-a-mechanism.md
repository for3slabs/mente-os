# ADR-025 · Config hygiene needs a mechanism, not discipline

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: any file granting permissions or naming paths the agent may use
does-not-apply-to: ⭐ a permission granted for one session and revoked after — ⛔ nothing accumulates, so nothing degrades

## Context

⛔ **A permission surface degrades by ACCUMULATION, never by decision.** Nobody grants a bad
permission; everybody grants one more, and the surface nobody designed is the one that ends up
protecting nothing.

## Decision

**Four rules govern a configuration:**

1. ⭐ **secrets are REFERENCED, never pasted**
2. **every granted path declares its reason**
3. 🔴 **ONE MECHANISM, ONE ENTRY** — see `ADR-026`
4. **paths are portable**

## Rejected alternatives

- ⛔ **Rely on discipline.** ⚠️ ⭐ **In every measured failure the rule already existed or was
  obvious** — what was missing was the mechanism. Discipline is what produced the state being
  cleaned up.
- ⛔ **A periodic audit instead of rules.** ⚠️ It finds the accumulation after it happened, ⭐ **and
  by then the entries are load-bearing** — somebody's workflow depends on each one.
- ⚠️ **One rule: "keep it clean".** ⛔ ⭐ **Four failures with four different shapes need four
  checks** — a single instruction is satisfied by whoever reads it most generously.

## Rationale

> ## ⭐ NOBODY ADDS THE ENTRY THAT BREAKS IT.
> ⚠️ **Each addition is defensible on its own**, which is why the surface is never refused — and
> why only a mechanism, applied at each addition, can bound it.

## Evidence

⭐ **Measured across one real configuration, four distinct failures:**

| Shape | Count |
|---|---|
| ⛔ entries carrying a credential in plain text | **331** |
| absolute paths tied to one machine | **689** |
| granted paths that no longer resolve | **3 of 9** |
| ⛔ entries for a SINGLE mechanism | **234** |

⚠️ **None of the four was a bad decision.** ⭐ **All four were the sum of defensible ones.**

## Consequences

- `CFG-SEC-001` 🔒 — a secret-shaped value in a configuration is a finding
- `CFG-WHY-001` — every granted path declares its reason, and ⭐ a dead grant is one nobody audits
- `CFG-ONE-002` 🔒 — ⭐ **one entry per MECHANISM** · detailed in `ADR-026`
- `CFG-PRT-001` 🔒 — an absolute home path measures one machine
- `bin/check-config` — the mechanism the failures were missing

## What would change this decision

⭐ **It stops being right if the four checks never fire on a maintained configuration.** ⚠️ Then
the rules are describing a problem that no longer occurs — ⛔ **but the test is a configuration
maintained WITHOUT them**, because a clean surface under active checks proves the checks work, not
that they are unnecessary.

## Reverting

⛔ **Drop the rules.** ⚠️ Configuration degrades again by accumulation — ⭐ **and it degrades
invisibly, because every individual entry still looks reasonable.**

---

Related: `ADR-026-permission-granularity-is-the-mechanism.md` (⭐ **rule 3 in full**) ·
`../rule-config-hygiene.md` (the four rules and their checks) · `../contract-adr.md`.
