# ADR-031 · The engine READS the host's tool, and never reaches the network

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: ⭐ every piece that asks the host's version-control tool a question
does-not-apply-to: what a piece DOES with the answer — that stays each rule's own

## Context

⛔ **This decision was already being made, three times, and written nowhere.**
Measured: `bin/check-clear-ready`, `bin/check-shipping` and `hooks/pre-push.sh`
all run the host's version-control tool. All three do it the same way — read
only, and its absence never fails the check — ⚠️ **which means the criterion was
right and invisible.**

⭐ **A criterion applied three times and declared zero times is the failure
`CHK-SHR-003` names**, one level up: each copy reinterprets it, and they diverge
without anything noticing. The fourth piece would have reinterpreted it again.

## Decision

⭐ **A piece MAY run the host's version-control tool to READ local state.** ⛔ It
MUST NOT reach the network, and it MUST NOT write.

⭐ **Three conditions, and they are one decision, not three.** Drop any of them
and the permission means something else entirely.

⭐ **READ ONLY** — ⛔ a validator that writes is no longer a validator.
⛔ **NEVER OVER THE NETWORK** — ⚠️ the condition that actually needed deciding,
and the rejected alternatives below say what it costs.
⭐ **ITS ABSENCE IS A GAP, NEVER A FAILURE** — ⛔ not every installation has the
tool, and a missing tool is not a broken tree.

## Rejected alternatives

- ⛔ **Never run it at all.** ⚠️ Then the registry can only be compared against
  itself, and ⭐ **the drift it exists to catch is exactly the kind that lives
  between the declaration and the machine.** A rule that can only check its own
  paperwork checks nothing.
- ⛔ **Allow network reads too** — asking the host whether a repository still
  exists. ⚠️ It answers a real question, and ⭐ **it costs three things this
  engine does not spend**: a validator that needs credentials, a validator whose
  result depends on connectivity, and a validator that is slow enough to be
  skipped. ⛔ **A check that can fail because the network is down is a check
  people learn to ignore.**
- ⚠️ **Decide per piece.** ⛔ That is the current state, and it is why this
  record exists.

## Rationale

> ## ⭐ THE LINE IS BETWEEN *THIS MACHINE* AND *SOMEBODY ELSE'S*.
> Reading what the local tool already knows costs nothing, needs no credential,
> works offline, and cannot be wrong about the machine it runs on. ⛔ Reaching a
> remote asks a question whose answer this engine cannot verify and whose
> failure it cannot distinguish from a real finding.

⭐ **And the registry's own contract already said so:** it instructs the reader
to *re-measure with the local remote listing, never trust the row alone.* ⚠️ The
decision was made in a template and never promoted to a rule — which is the
shape of every gap in this backlog.

⛔ **Condition ③ is not politeness.** A validator that fails because a tool is
absent reports a fault in the installation instead of a gap in what it could
see, and ⭐ **the reader then fixes the wrong thing.**

## Evidence

Three pieces ran the tool before this was written; all three read only, and all
three treat its absence as unmeasured rather than as a finding. The convergence
is the evidence: ⭐ **the criterion was already correct — it was only unstated.**

## Consequences

- ⭐ A piece comparing the registry against real remotes is now bounded: it reads
  the local remote listing, and reports what it could not see.
- ⛔ No piece may ask a host whether a repository exists, is renamed, or is
  reachable. ⚠️ That question stays a person's.
- ⭐ Any future piece touching the tool cites this record instead of
  re-deciding.

## What would change this decision

⭐ **An installation that needs a remote's true state as part of a gate** — not
as information, but as something that must BLOCK. ⚠️ Then the cost of
credentials and connectivity would be worth paying, and this record would be
superseded rather than bent.

## Reverting

Drop the rule; the three pieces keep working, and the fourth reinterprets the
criterion again.
