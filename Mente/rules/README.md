# rules/ — the law · contracts, rules, and the decisions behind them

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}} · **Scope:** ⚠️ ENGINE — travels identical to every
clone. Nothing here is edited per instance.
**Governance:** declared as `engine` in the piece table · **Enforcement:** 🔒 per document, see below

---

## What this folder is

The **written law of the system**: what shape a file must have, how work behaves, and which
decisions are already settled so nobody relitigates them. Everything a validator in `bin/` checks
is defined here first.

> ⭐ **The order that must never invert:** the rule is written here, **then** a script enforces it.
> A validator written before its contract is a judge with no law — it will measure whatever its
> author happened to assume that day, and the assumption becomes the standard by accident.

---

## ⛔ THE THREE DOCUMENT TYPES — they are not interchangeable

This folder holds three different things. Putting a file in the wrong category is the most common
mistake here, and it has a real cost: the wrong type gets read at the wrong moment.

### `contract-*` — the SHAPE a file must have

Defines the fields, sections and limits that a kind of file must satisfy. It is the only type a
script can check mechanically, field by field.

- **Answers:** *"is this file well-formed?"*
- **Always carries:** `Applies to:` (which files it governs) and `Verified by:` (which script)
- **Written as:** required fields, order, ceilings — never advice

### `rule-*` — a BEHAVIOR that must hold

Governs how work is done, not how a file looks. Some are enforceable by a script, most are not.

- **Answers:** *"how must this be done?"*
- **Always carries:** the measured failure that made it necessary
- **Written as:** the rule, then its reason, then what it costs to break it

### `decisions/ADR-*` — a DECISION already taken

An immutable record of a choice, with its context and its consequences. Never edited: a decision
that turned out wrong is **superseded** by a new ADR, and both stay.

- **Answers:** *"why is it like this, and who decided?"*
- **Always carries:** `date`, `status`, `decided-by`, `supersedes`, `superseded-by`
- ⭐ **Its value is not the decision — it is that nobody re-argues it six months later**

| If you are writing… | The type is | Filename |
|---|---|---|
| the fields a file must have | contract | `contract-<what>.md` |
| how something must be done | rule | `rule-<behavior>.md` |
| why a choice was made | ADR | `decisions/ADR-NNN-<slug>.md` |
| a standard method for large work | neither prefix — a named method | `<METHOD_NAME>.md` |

---

## ⭐ THE HONEST PART: most of this folder is NOT enforced

The system's own law says a rule in code is followed 100% and a rule that lives only in a document
is followed 40-60%. **This folder is where the 40-60% lives.** Pretending otherwise is the danger:
a document that reads like enforcement, but nothing checks it.

So every document here declares which it is:

| Level | Means | How you know |
|---|---|---|
| 🔒 **lock** | a script or gate refuses the action | it names a `Verified by:` script, and that script actually fails when you break it |
| 🟡 **prompt** | the agent asks before proceeding | wired as a confirmation, not a refusal |
| 📖 **discipline** | nothing can verify it | ⚠️ it must **say so** |

⛔ **Never present a 📖 as a 🔒.** A limit that everyone believes is enforced, and is not, is worse
than no limit: the belief replaces the vigilance.

⭐ **A rule with no validator should be assumed unenforced** — that is not cynicism, it is the
measured base rate. If a rule matters enough to write down, the next question is always
*"what would check it?"*, and the honest answer is sometimes "nothing yet".

---

## What is in here today

⛔ **No counts.** The piece table declares every file, and the generated metrics carry the numbers —
a total written here would be correct exactly once.

| Document | Governs | Enforced by |
|---|---|---|
| `contract-document.md` | the shape every document must have, and its ceiling | `bin/check-document` |
| `contract-block.md` | the unit of work: its sections, its states, its closing | `bin/check-block` |
| `contract-campaign.md` | what holds several blocks together, and how they share facts | `bin/check-campaign` |
| `contract-archive.md` | what a closed block leaves behind for whoever finds it later | `bin/check-archive` |
| `contract-pending.md` | the shape of a debt that outlives its session, and its rotation | `bin/check-pending` |
| `contract-handoff.md` | delegating work: what is granted, what is refused, what comes back | `bin/check-handoff` |
| `contract-adr.md` | a decision recorded so nobody re-argues it | `bin/check-decisions` |
| `rule-inheritance.md` | the three levels, and why a lower one may tighten but never loosen | `bin/check-inheritance` |
| `rule-working-in-a-block.md` | how work behaves inside a block: lane, isolation, friction, stop | `bin/check-work` |
| `rule-shipping.md` | how a change leaves: branch, verify, batch, merge, clean up, close | `bin/check-shipping` |
| `rule-checks-must-measure.md` | ⭐ the rule the validators are held to — a check that cannot fail | `bin/check-checks` |
| `rule-config-hygiene.md` | a permission surface: complete, portable, and free of pasted secrets | `bin/check-config` |

⭐ **Every one of them carries a `Verified by:` line naming both its validator and the probe that
proves the validator works.** A validator with no probe has never been shown to fail — and a check
that cannot fail is decoration.

> ## ⛔ THE PROBE IS NOT OPTIONAL.
> ⚠️ **A green light from an unproven validator is indistinguishable from a green light from a
> broken one** — and the second one is silent for exactly as long as nobody sabotages it on purpose.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| a contract: the fields a file must carry | a validator — that is `bin/`, it *enforces* this |
| a rule of behavior, with its measured cause | a project's own conventions — those are instance-level |
| an ADR recording a settled decision | the reasoning behind a decision — that goes in `docs/`, the ADR points at it |
| a named method for large work | anything with a live number in it |

⚠️ **The line against `memory/principles/`:** rules say **what must happen**; principles say **with
what criterion to judge**. *"A block does not close with open sub-blocks"* is a rule — binary,
checkable. *"What makes documentation good"* is criterion — it needs judgment, and it lives in
`principles/`.

⚠️ **The line against `docs/`:** a rule is the conclusion; the analysis that produced it is a
document. Keeping the analysis here makes the law long, and a law nobody finishes reading is a
law nobody applies.

---

## The shape every document here follows

```markdown
# CONTRACT · <WHAT>        or        # RULE · <BEHAVIOR>

**Status:** current · **Type:** rule · **Updated:** <date> · **Owner:** <owner>
**Applies to:** which files or situations this governs
**Verified by:** `bin/<script>` — or explicitly: nothing verifies this yet

## Purpose
What it governs and why it exists. The WHY is the measured failure, not a good intention.

## <the body: fields, or the behavior>

## What it costs to break it
The concrete consequence. A rule with no stated cost gets treated as a preference.
```

⛔ **Never write a live number into a rule.** Counts, versions, totals — they belong in the
generated metrics file. A number copied into prose is correct exactly once, and a rule that cites
a stale number teaches the reader to distrust the rest of it.

---

## ⭐ RULES EVOLVE — an immutable standard becomes a fossil

⛔ **A rule that can never change is a rule people route around.** The friction does not disappear;
it moves out of sight, and the rule keeps looking obeyed while nothing follows it.

**So the mechanism is: comply → log the friction → keep going → propose the change at close.**

| Step | Why |
|---|---|
| **comply** | ⛔ never break a rule in the moment because it is inconvenient |
| **log the friction** | one line: what the rule blocked, and what it cost |
| **keep going** | the work does not stop for a rule dispute |
| ⭐ **propose at close** | with the friction record as evidence, not as an opinion |

⭐ **A rule changes when the friction is measured, never when it is felt.** One person annoyed once
is not evidence; the same rule obstructing distinct pieces of work repeatedly is.

⚠️ **The single exception is real damage.** If following the rule would break something, stop and
raise it immediately — that is not friction, it is a defect in the rule.

---

## ⚠️ Before you add a document here — the five questions

1. **Which of the three types is it?** If it does not fit one, it is probably a document for
   `docs/` or criterion for `principles/`.
2. **What real failure caused it?** ⭐ A rule written from imagination governs a situation nobody
   is in, and gets ignored when a real one arrives.
3. **What enforces it?** Name the script, or write plainly that nothing does yet.
4. **Would it still hold in a different project?** Yes → it belongs to the engine. No → it belongs
   to that project's own rules, not here.
5. **Does it contradict an existing rule?** Rules **add up and tighten, never loosen**. Two rules
   that disagree do not average out — the stricter one wins, and the looser one must be deleted or
   scoped, not left standing.

---

## ADRs — the part that is never edited

`decisions/` is append-only and numbered in sequence. An ADR is a photograph of a decision at the
moment it was made.

⛔ **Never rewrite an ADR to match what you now think.** If the decision changed, write a new one
and mark the old `superseded-by`. The pair — the wrong decision and its correction — is more
useful than a clean record that hides the reasoning ever moved.

⚠️ **An ADR's filename must not name a person.** Name the decision, not who took it — that goes in
the `decided-by` field, where it is data instead of a permanent label on a file that will outlive
whoever installed the system.

---

Related: `bin/README.md` (what enforces these) · `hooks/README.md` (what blocks in real time) ·
`../memory/principles/README.md` (criterion, not law) · `../docs/README.md` (the analysis behind a
rule) · `../base-rules.md` (the universal level) · `../piezas.tsv` (where each contract is declared).
