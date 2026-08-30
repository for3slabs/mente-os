# CONTRACT · DECISION RECORD

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every file in `rules/decisions/`
**Enforcement:** 🔒 lock — `bin/check-decisions`
**Level:** 🌐 universal — ⭐ travels identical to every clone; a lower level may ADD or TIGHTEN, never loosen
**Verified by:** `bin/check-decisions` · `bin/probes/probe-decisions.py`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone

---

## 0 · WHAT THIS FILE IS

> ## ⭐ The shape of a decision that was already taken — so nobody re-argues it in six months.

⚠️ **The failure it prevents:** decisions that live only in a conversation. ⛔ **The rule changes,
the reason does not travel with it** — and the next person either repeats the debate or, worse,
reverses the decision without knowing why it was made.

> ## ⭐ A DECISION RECORD'S VALUE IS NOT THE DECISION
> ⛔ **It is that the decision stops being re-argued.** The record is read exactly twice: once
> when someone disagrees with it, and once when someone is about to undo it.

⭐ **And that is why it holds `Reverting`:** the second reader is the one who needs it most.

---

## 1 · ENFORCEMENT

| | Means |
|---|---|
| 🔒 **lock** | ⭐ a script refuses — ⚠️ and it has been seen to fail |
| 🟡 **prompt** | the agent asks before proceeding |
| 📖 **discipline** | ⛔ **nothing verifies this** |

**IDs are permanent.** `DEC-<area>-<nnn>` — ⛔ never renumbered, never reused.

---

## 2 · ⭐ BEFORE WRITING ONE — search, understand, reuse

> ## ⛔ AN AGENT NEVER CREATES A RECORD BEFORE LOOKING FOR THE ONE THAT ALREADY ANSWERS IT.

```
SEARCH ──▶ UNDERSTAND ──▶ REUSE ──▶ CHECK FOR CONFLICT ──▶ CREATE
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DEC-SRC-001` | ⭐ **The existing records are searched first** | 📖 | ⛔ nothing verifies this |
| `DEC-SRC-002` | ⭐ **A question already answered is REUSED, never re-decided** | 📖 | ⚠️ cite the record instead |
| `DEC-SRC-003` | ⛔ **A record that contradicts a current one is a CONFLICT** | 🔒 | ⚠️ the SIGNAL is measured — two current records on one subject — never the semantics |

⚠️ **What happens without this, and it is the failure that costs most quietly:**

```
⛔  a new record says: "use this store"
    a record from months ago already said exactly that
    → two records, one question, and nothing says which is current
```

⭐ **That is not a duplicate document. It is a second authority** — and the next
reader has to decide which one wins, which is the ambiguity these records exist
to remove.

---

## 3 · ⭐ WHEN A RECORD IS NEEDED — and when it is BUREAUCRACY

⛔ **A system that records everything records nothing:** ⚠️ **the signal drowns,
and people stop writing them at all.**

### ✅ A record IS needed when the decision…

| # | |
|---|---|
| 1 | ⭐ **changes the architecture** — how the pieces relate |
| 2 | **introduces a structural dependency** |
| 3 | ⭐ **changes a contract between components** |
| 4 | **modifies or removes an existing rule** |
| 5 | ⭐ **changes a decision already accepted** |
| 6 | **touches persistence, security, data or a protocol** |
| 7 | ⭐ **is hard to reverse** |
| 8 | **sets a pattern others will be expected to follow** |

### ⛔ A record is NOT needed for…

| ⛔ | ⭐ Why |
|---|---|
| a cosmetic change | it decides nothing |
| a typo, a rename with no consequence | ⚠️ version control already records it |
| ⭐ **a refactor with no behaviour change** | the behaviour is the decision, and it did not change |
| a local, reversible choice | ⭐ it lives in the block's decisions, not here |
| ⛔ **something a current record already settles** | ⚠️ **that is §2 — reuse it** |

> ## ⭐ THE TEST
> ⛔ **Would somebody, six months from now, argue about this?** If not, it is
> not a decision — ⚠️ **it is a preference, and preferences do not get records.**

⭐ **The failure this prevents is a real one:** a chain of records for a
framework, then a component, then its padding, then the number. ⛔ **Each one
correct, and together they make the folder unreadable.**

---

## 4 · ⭐ THE THREE RULES

| # | Rule | ⛔ What it prevents |
|---|---|---|
| **1** | ⭐ **One decision = one file.** ⛔ Never a row in a shared table | ⚠️ **the duplication that always happens** — see below |
| **2** | ⭐ **The index is GENERATED from the files.** ⛔ Nobody writes it | an index that lies |
| **3** | ⭐ **A decision is never edited — it is SUPERSEDED** | ⛔ losing the history of *why* it changed |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DEC-ONE-001` | ⭐ **One decision per file** | 🔒 | ⛔ a table row cannot carry evidence or a way back |
| `DEC-ONE-002` | **The index is generated, never hand-written** | 📖 | ⚠️ nothing verifies this yet |
| `DEC-ONE-003` | ⛔ **An accepted record is never edited in place** | 📖 | ⭐ see below |
| `DEC-ONE-004` | ⚠️ **A number inside a decision may be AMENDED — the decision may not** | 📖 | ⭐ dated, attributed, and stating what did NOT change |

### ⚠️ THE CASE RULE 3 DOES NOT COVER — and it happens

⛔ **Sometimes the decision holds and a NUMBER inside it stops fitting.** Superseding the whole
record then buries a decision that is still correct, ⭐ **and re-deciding something nobody disputes
costs more history than it saves.**

**So an AMENDMENT is allowed, under three conditions:**

| | ⭐ Required |
|---|---|
| **dated** | when it moved |
| **attributed** | ⬜ who moved it |
| ⭐ **scoped** | ⛔ **an explicit line saying what did NOT change** |

> ## ⛔ AN AMENDMENT WITHOUT THAT THIRD LINE IS AN EDIT WEARING A LABEL.
> ⚠️ **The reader cannot tell whether the decision moved with the number** — and that is exactly
> the history rule 3 exists to protect.

⭐ **Measured — the shape that works:** a real record raised a ceiling from one number to another
and wrote *"the decision itself is untouched; only the number moved"*, with the reason the old
number no longer fitted. ⚠️ **The record stayed defensible because the amendment said what it was
NOT.**

### ⚠️ Rule 1 exists because the alternative was measured

⛔ **Decisions kept as rows in a shared table end up in TWO tables** — and the two diverge, badly,
without either looking wrong on its own. ⭐ **A row cannot carry its evidence, its rationale, or
the way to undo it. A file can.**

### ⚠️ Rule 3 is the one people break

> ## ⛔ EDITING AN ACCEPTED RECORD ERASES THE REASON THE OLD DECISION EXISTED.

⭐ **If the decision changes, write a new one that points back at it.** The pair — the decision
that turned out wrong and its correction — ⭐ **is more useful than a clean record that hides that
the reasoning ever moved.**

---

## 5 · THE TEMPLATE

```markdown
# <NNN> · Short imperative name

date: <YYYY-MM-DD>
status: proposed | accepted | superseded | reverted
implementation: not-started | in-progress | implemented | verified
decided-by: <who>
supersedes: —          ⭐ and WHY, when it supersedes something
superseded-by: —
applies-to: <where this decision governs>
does-not-apply-to: <where it explicitly does not>

## Context
The problem that forced the decision — ⭐ with data, not adjectives.

## Decision
What was decided, in one sentence.

## Rejected alternatives
⭐ What was considered and turned down — **each one named**, so that proposing
it again is recognised as a re-decision, not a new idea.

## Rationale
Why this one and not those.

## Evidence
The measurement behind it. ⛔ If there is none, write `none — judgment call`.

## Consequences
⭐ What this decision obliges — the rules it produces, the pieces it affects,
and what demonstrates it is actually in place.

## Reverting
How to undo it if it turns out wrong. ⛔ If it cannot be undone, say so.
```

| Field | ⭐ The rule |
|---|---|
| `date` | ISO — ⚠️ a record with no date cannot be ordered against another |
| `status` | one of the four, ⛔ never free text |
| `decided-by` | ⭐ who held the authority — ⚠️ **a role or a name, and it is data, not a label on the file** |
| `supersedes` / `superseded-by` | `—` when none · ⭐ **both sides must point at each other** |
| **Context** | ⛔ with data |
| **Decision** | ⭐ one sentence |
| **Rationale** | ⛔ must name what was rejected |
| **Evidence** | a number, a file, a command — ⭐ or the words that admit there is none |
| ⭐ **`implementation`** | ⚠️ **a decision and its implementation are not the same thing** — see §6 |
| ⭐ **`applies-to` / `does-not-apply-to`** | ⛔ a decision with no boundary gets applied where it was never meant to |
| **Rejected alternatives** ⚠️ *recommended* | ⭐ **each one named** — see below |
| **Consequences** ⚠️ *recommended* | ⭐ what it obliges, and what proves it is in place |
| **Reverting** | ⚠️ **and if it cannot be undone, that is the most important sentence in the file** |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DEC-FLD-001` | **All five header fields present** | 🔒 | ⛔ missing one, it cannot be read by anything |
| `DEC-FLD-002` | **`status` is one of the four** | 🔒 | ⚠️ free text means nothing can sort them |
| `DEC-FLD-003` | **All five sections present** | 🔒 | Context · Decision · Rationale · Evidence · Reverting |
| `DEC-FLD-003b` | ⭐ **`Rejected alternatives` and `Consequences` are RECOMMENDED, not required** | 📖 | ⚠️ their absence is not a violation — ⛔ but when present, `DEC-FLD-005` applies |
| `DEC-FLD-004` | ⭐ **`Evidence` is filled, or explicitly says there is none** | 🔒 | ⛔ an empty field reads as *not yet written* |
| `DEC-FLD-005` | ⭐ **Rejected alternatives are named, one per line** | 🔒 | ⚠️ without them, the reasoning cannot be re-examined |
| `DEC-FLD-006` | ⭐ **`supersedes` states WHY, not only WHAT** | 🔒 | ⛔ *"replaced by 008"* does not say what changed |
| `DEC-FLD-007` | ⭐ **A record declares where it applies** | 🔒 | ⚠️ and where it explicitly does not |

> ## ⭐ `Evidence` AND `Reverting` ARE WHAT MAKE THIS MORE THAN A CHANGELOG
> ⛔ **A decision with no evidence is an opinion. A decision with no exit is a trap.**

⭐ **`none — judgment call` is a legitimate answer**, and a better one than a fabricated number.
⚠️ **What is not legitimate is silence** — an empty field and an honest *"there was no data"* look
identical afterwards, and only one of them was a choice.

---

## 6 · ⭐ THE DECISION AND ITS IMPLEMENTATION ARE NOT THE SAME THING

⛔ **`status: accepted` says the decision was taken. It says NOTHING about
whether it happened.**

| `status` | Says |
|---|---|
| `proposed` · `accepted` · `superseded` · `reverted` | ⭐ **what the decision IS** |

| `implementation` | Says |
|---|---|
| `not-started` | ⭐ decided, ⛔ nothing built |
| `in-progress` | under way |
| `implemented` | ⚠️ built — **and not yet demonstrated** |
| ⭐ **`verified`** | ⭐ **built AND something proves it** |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DEC-IMP-001` | ⭐ **Both states are declared** | 🔒 | ⛔ one of them alone is half an answer |
| `DEC-IMP-002` | ⭐ **`verified` names what demonstrates it** | 🟡 | ⚠️ a validator, a test, a measurement |
| `DEC-IMP-003` | 🔴 **`accepted` + `not-started`, long enough, is asked about** | 🔒 | `bin/check-decisions`, against the ⬜ period below |

### ⬜ HOW LONG IS LONG ENOUGH

| ⬜ Declaration | Days | Why it is not the engine's |
|---|---|---|
| ⬜ pending period | 90 | ⛔ deciding months before building is normal in one project and a warning sign in another |

⭐ **It is not forbidden** — ⛔ **it must not read the same as one that was done.** The record is
asked about, never rejected.

> ## 🔴 AN ACCEPTED DECISION THAT WAS NEVER IMPLEMENTED
> ⛔ **From the outside it reads exactly like one that was.** ⚠️ The record says
> `accepted`, the folder looks healthy, and the thing it decided does not
> exist anywhere.
>
> ⭐ **It is the same shape as a piece that is built and never connected** — and
> it is worse here, because ⛔ **everything downstream cites the record as
> settled.**

⭐ **The fix is not to forbid it.** A decision taken before the work is normal
and often correct. ⚠️ **What is not acceptable is that nothing distinguishes
"decided, pending" from "decided, done".**

---

## 7 · ⛔ WHEN TWO RECORDS DISAGREE

> ## ⭐ AN AGENT NEVER PICKS BETWEEN TWO CONTRADICTORY RECORDS.

```
two records answer the same question, differently
        ↓
does one supersede the other?
    ├─ YES ─▶ ⭐ the superseding one is current · the other is history
    │
    └─ NO ──▶ ⛔ CONFLICT
                ↓
        ⭐ STOP · report both · do not implement either
        the resolution is a NEW record that supersedes both
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DEC-CFL-001` | ⭐ **A conflict is reported, never resolved by choosing** | 📖 | ⛔ nothing verifies this |
| `DEC-CFL-002` | ⭐ **The resolution is a new record superseding BOTH** | 📖 | ⚠️ not an edit to either |
| `DEC-CFL-003` | ⛔ **Nothing is implemented while a conflict is open** | 📖 | ⭐ see below |

⚠️ **`DEC-CFL-003` is the one that matters:** ⛔ **implementing one side of an
open conflict makes the code the tiebreaker** — and then the decision was taken
by whoever typed fastest, with no record of it.

### ⭐ AND WHEN THE CONFLICT IS NOT BETWEEN RECORDS

⚠️ **A record can also contradict a rule, a criterion, or the code itself.**
⭐ **The order, strongest first:**

| # | Source | ⭐ |
|---|---|---|
| 1 | ⭐ **the current decision record** | it is what the others were derived from |
| 2 | **a rule born from it** | ⚠️ if it disagrees, the rule drifted |
| 3 | **a criterion** | it judges, it does not decide |
| 4 | ⛔ **the implementation** | ⭐ **code is evidence of what happens, never of what was decided** |
| 5 | **documentation** | ⚠️ the most likely to be stale |

⛔ **And a conflict between levels is still a conflict:** ⭐ **the higher one
wins AND the divergence is reported** — ⚠️ a rule that drifted from its record
is a defect in one of the two, and silently obeying the record hides which.

---

## 8 · NUMBERING

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DEC-NUM-001` | **Sequential, zero-padded** | 🔒 | ⚠️ so a listing sorts correctly · ⬜ an optional letter prefix is allowed |

### ⬜ WHAT A RECORD IS CALLED, AND WHEN IT HAS NO DATE

| ⬜ Declaration | Engine default | Why it is not fixed |
|---|---|---|
| ⬜ filename prefix | `ADR-` | ⭐ the NUMBER is what must sort; the prefix is a reading convenience |
| ⬜ un-instantiated date | `{{date}}` | ⛔ a record shipped by the engine has no date until an installation has one |

⛔ **Measured:** the folder README declared `ADR-NNN-<slug>.md` while the validator required a
leading digit, and the contract arbitrated neither — ⚠️ **so the first record the engine tried to
ship was rejected by its own check.**

⭐ **And a template date is not a broken date.** `{{date}}` is the placeholder every engine
document carries; rejecting it would leave the engine unable to ship a single decision of its own.
| `DEC-NUM-002` | ⛔ **A number is never reused** | 🔒 | ⭐ not even for a reverted decision |
| `DEC-NUM-004` | ⛔ **A filename never names a PERSON** | 🔒 | ⭐ name the decision; who took it goes in `decided-by`, where it is data |
| `DEC-NUM-003` | ⭐ **A reverted decision keeps its file and its number** | 🔒 | ⛔ with `status: reverted` |

### ⛔ WHY A NAME IN A FILENAME IS DIFFERENT FROM A NAME IN A FIELD

⭐ **`decided-by` is DATA — it can be read, filtered, and it belongs to one installation.** ⛔ **A
filename is a permanent label**, cited by rules and commits, and it outlives whoever installed the
system.

⚠️ **Measured: a real record was named after the person who took the decision.** ⭐ **The decision
it recorded — that the criterion belongs to the installation's owner — is universal; the name made
it look personal**, and a clone reading it would inherit somebody else's name as part of its law.

⭐ **`DEC-NUM-002` exists because a number is an address.** Something cites it — a rule, a commit,
a review. ⛔ **Reusing it makes every one of those citations resolve to the wrong decision, and
none of them says so.**

---

## 9 · ⛔ A LINK POINTS BOTH WAYS

```
NNN  superseded-by: MMM        MMM  supersedes: NNN
        └──────────── both, always ────────────┘
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DEC-SUP-001` | ⭐ **A supersede link is symmetric** | 🔒 | ⛔ one-sided means one of the two is wrong |
| `DEC-SUP-002` | **A link points at a record that exists** | 🔒 | ⚠️ a pointer to nothing reads as a promise |
| `DEC-SUP-003` | ⭐ **A superseded record has `status: superseded`** | 🔒 | ⛔ otherwise two records both read as current |

⭐ **`DEC-SUP-003` is the one that matters most in practice.** ⚠️ **Two records both saying
`accepted` about the same question is the exact ambiguity this contract exists to remove** — and
the reader has no way to tell which one won.

---

## 10 · ⭐ WHAT ELSE DESERVES A RECORD

⛔ **Not everything. The heavier the object, the heavier the record.**

| The new thing | ⭐ Minimum |
|---|---|
| **a decision** | a full record |
| **a rule** | ⭐ born from a record — and the rule links back to it |
| **a validator** | a record stating what it checks and why |
| **a criterion in a discipline** | ⭐ the record notes **that it was defined**, ⛔ never its content |
| **a path or a pointer** | ⚠️ **a comment with the date and the reason** — ⛔ not a record |

⭐ **A path does not need a full record — that would be bureaucracy.** It needs a reason next to
it. ⚠️ **And a bureaucratic record is not a stricter system: it is one where records stop being
written at all.**

---

## 11 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **a decision as a table row** | ⚠️ it ends up in two tables, and they diverge |
| ⭐ **an accepted record edited in place** | ⛔ **the reason the old decision existed is gone, and nothing shows it was ever different** |
| **a one-sided supersede link** | ⚠️ ⭐ **two records both read as current** |
| **a reused number** | ⛔ every citation resolves to the wrong decision, silently |
| **empty `Evidence`** | ⭐ an opinion, indistinguishable from a measurement |
| **no `Reverting`** | ⚠️ the decision cannot be undone by anyone who was not there |
| ⭐ **a record written without searching first** | ⛔ **two records, one question — and nothing says which is current** |
| **a record for something nobody would argue about** | ⚠️ the folder becomes unreadable, ⭐ and the real decisions drown |
| ⭐ **`accepted` with no implementation state** | ⛔ **decided and never built reads exactly like decided and done** |
| ⭐ **a rejected alternative left inside the rationale** | ⚠️ **nothing can detect it being proposed again** |
| **choosing between two contradictory records** | ⛔ ⭐ **the tiebreak becomes whoever typed fastest, with no record of it** |

---

## 12 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ the records themselves | ⭐ the owner of the instance — ⛔ **the folder ships EMPTY** |
| the template and the field rules | whoever maintains the engine, through a recorded decision |
| ⛔ editing an accepted record | **nobody** — ⭐ supersede it instead |

> ## ⭐ THE FOLDER TRAVELS EMPTY, AND THAT IS THE POINT
> ⛔ **Another installation's decisions are not yours.** What travels is the shape; ⭐ **what it
> holds is written by whoever installs it, about their own system.**

---

## ⭐ THE TWELVE QUESTIONS A RECORD MUST SURVIVE

⛔ **A record that passes its validator is well-formed, not useful.** These are what separate the
two, and the last five are the ones a script cannot ask.

| # | Question | ⛔ What its absence costs |
|---|---|---|
| 1 | does its FORM pass the check? | it cannot be read by anything |
| 2 | is the decision IMPLEMENTED? | ⚠️ a record of something that never happened |
| 3 | does the rule CITE it? | ⭐ **the rule is one argument from being reverted by somebody who does not know what caused it** |
| 4 | is any INSTANCE data left? | it does not travel |
| 5 | do its POINTERS resolve here? | a promise to a reader who will follow it |
| 6 | does it CONTRADICT another? | two records, one question, nothing says which |
| 7 | does it say what the rule does NOT? | ⛔ otherwise it is a duplicate, not traceability |
| **8** | ⭐ does it name the REJECTED alternative, and why? | ⛔ the decision cannot be re-examined — it gets argued from zero |
| **9** | is its EVIDENCE measured, or an opinion? | ⚠️ a number, a file, a command — ⭐ **or the words admitting there is none** |
| **10** | is the REVERSION real? | ⛔ "go back" without saying what is lost is an exit nobody can take |
| **11** | does it declare its BOUNDARY? | ⚠️ a decision with none gets applied where it was never meant to |
| **12** | ⭐ does it survive without its original CONTEXT? | ⛔ if it only makes sense to whoever was there that day, it does not travel |
| **13** | ⭐ what decision ENABLES it, and what depends on it? | ⛔ a record with no neighbours is reverted without seeing what goes with it |
| **14** | does its `status` match MEASURED reality? | ⚠️ `accepted` with nothing built reads exactly like done |
| **15** | can it be SHOWN still to hold today? | ⭐ a decision can die quietly and the record stays confident |
| **16** | ⭐ what would CHANGE it? | ⛔ a decision with no revision condition is dogma |

> ## ⭐ 8 TO 16 ARE NOT VERIFIABLE BY A SCRIPT, AND THAT IS WHY THEY ARE WRITTEN DOWN.
> ⚠️ **A check can see that `Rejected alternatives` exists.** ⛔ **It cannot see that what is in it
> would let somebody re-open the question honestly** — and that is the whole reason the section
> is there.

### ⭐ 16 IS THE ONE MOST OFTEN MISSING

⛔ **`Reverting` says how to undo a decision. Nothing says what would make it WRONG.** ⚠️ Without
that, a record is defended forever by whoever inherits it — and the condition that should have
retired it passes unnoticed, because nobody wrote down what to watch for.

---

Related: `README.md` (⭐ **the three document types — this is the append-only one**) ·
`contract-document.md` (⭐ the header and the ceiling this file obeys) · `contract-block.md`
(⭐ §G — a decision inside a block, which graduates here when it outlives the block) ·
`../memory/principles/expertise/doc-structure.md` (⭐ §2.3 — pointer, never copy: why one
decision is one file) · `../bin/check-decisions` (what enforces the 🔒 rows).
