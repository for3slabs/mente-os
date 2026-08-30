# ADR-026 · A permission's granularity is the MECHANISM

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: every entry in a permission list
does-not-apply-to: 🔴 an irreversible action — ⭐ a destructive command stays LITERAL on purpose, so each use is granted individually

## Context

`ADR-025` names four hygiene rules. ⛔ **The third is the one that produces the volume**, and
volume is what makes a permission surface unauditable.

## Decision

⭐ **A permission is granted per MECHANISM, never per invocation.**

> ## ⭐ THE TEST: does this entry authorize something no other entry already authorizes?
> ⛔ **If not, it grants nothing and only adds a line.**

🔴 **The deliberate exception:** an irreversible command stays literal — ⭐ **there, one entry per
use is the point**, because each use deserves its own decision.

## Rejected alternatives

- ⛔ **Literal entries, one per command.** ⚠️ Measured: it produced over a thousand — ⭐ **a list
  nobody can read is a list nobody audits**, and the wrong entry hides among the right ones.
- ⛔ **One wildcard for everything.** ⚠️ Auditable and worthless: ⭐ **it grants what nobody thought
  of**, which is the whole failure the list exists to prevent.
- ⚠️ **Group by tool author or by folder.** ⛔ Those group by WHO wrote it, ⭐ **not by what it can
  do** — and capability is the only axis a permission decision is made on.

## Rationale

⭐ **The volume is not a tidiness problem, it is an AUDIT problem.** ⛔ Over a thousand entries
cannot be read by anyone, so a contradiction among them is invisible — ⚠️ **and that is exactly how
one real over-grant survived unnoticed.**

⭐ **And the exception proves the rule's logic rather than weakening it:** grouping is right when
repetition means "the same safe capability, again"; ⛔ **it is wrong when each use is its own
decision.**

## Evidence

⭐ **Measured on one real permission list: 1,341 entries reduced to 127** by applying the rule —
⛔ **a 91% cut with no capability lost**, because none of the removed entries authorized anything
the survivors did not.

⚠️ **And one command was deliberately left literal**, which is where the boundary in this record
comes from.

## Consequences

- `CFG-ONE-002` 🔒 — ⭐ grouped by the MECHANISM, and ⛔ **never by the first path segment**:
  grouping on that reported "15 entries for one tool" when it was 15 tools
- `CFG-ONE-001` 🔒 — an entry contained by another grants nothing new
- ⭐ `CFG-SUR-003` — an unbounded shell grant makes every denial below it a suggestion
- ⚠️ `CFG-LST-002` — an allowlist must fail CLOSED on the unknown

## What would change this decision

⭐ **It stops being right if grouping ever hides a capability somebody would have refused.** ⚠️ The
whole trade is auditability for precision — ⛔ **and it is a good trade only while the group means
what its name says.** The signal is a grouped entry whose members turn out to differ in what they
can reach.

## Reverting

⛔ **Approve command by command.** ⚠️ The list grows back — ⭐ **and it grows back faster than it
was cut, because each addition is one yes and the cut was one deliberate pass.**

---

Related: `ADR-025-config-hygiene-needs-a-mechanism.md` (⭐ **the four rules this is the third of**) ·
`../rule-config-hygiene.md` `§4` · `../contract-adr.md`.
