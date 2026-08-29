# CONTRACT · DECISION RECORD

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every file in `rules/decisions/`
**Enforcement:** 🔒 lock — `bin/check-decisions`
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

## 2 · ⭐ THE THREE RULES

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

## 3 · THE TEMPLATE

```markdown
# <NNN> · Short imperative name

date: <YYYY-MM-DD>
status: proposed | accepted | superseded | reverted
decided-by: <who>
supersedes: —
superseded-by: —

## Context
The problem that forced the decision — ⭐ with data, not adjectives.

## Decision
What was decided, in one sentence.

## Rationale
Why this and not the alternative. ⭐ Name the alternative that was rejected.

## Evidence
The measurement behind it. ⛔ If there is none, write `none — judgment call`.

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
| **Reverting** | ⚠️ **and if it cannot be undone, that is the most important sentence in the file** |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DEC-FLD-001` | **All five header fields present** | 🔒 | ⛔ missing one, it cannot be read by anything |
| `DEC-FLD-002` | **`status` is one of the four** | 🔒 | ⚠️ free text means nothing can sort them |
| `DEC-FLD-003` | **All five sections present** | 🔒 | Context · Decision · Rationale · Evidence · Reverting |
| `DEC-FLD-004` | ⭐ **`Evidence` is filled, or explicitly says there is none** | 🔒 | ⛔ an empty field reads as *not yet written* |
| `DEC-FLD-005` | ⭐ **`Rationale` names the rejected alternative** | 🟡 | ⚠️ without it, the reasoning cannot be re-examined |

> ## ⭐ `Evidence` AND `Reverting` ARE WHAT MAKE THIS MORE THAN A CHANGELOG
> ⛔ **A decision with no evidence is an opinion. A decision with no exit is a trap.**

⭐ **`none — judgment call` is a legitimate answer**, and a better one than a fabricated number.
⚠️ **What is not legitimate is silence** — an empty field and an honest *"there was no data"* look
identical afterwards, and only one of them was a choice.

---

## 4 · NUMBERING

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DEC-NUM-001` | **Sequential, zero-padded** | 🔒 | ⚠️ so a listing sorts correctly |
| `DEC-NUM-002` | ⛔ **A number is never reused** | 🔒 | ⭐ not even for a reverted decision |
| `DEC-NUM-003` | ⭐ **A reverted decision keeps its file and its number** | 🔒 | ⛔ with `status: reverted` |

⭐ **`DEC-NUM-002` exists because a number is an address.** Something cites it — a rule, a commit,
a review. ⛔ **Reusing it makes every one of those citations resolve to the wrong decision, and
none of them says so.**

---

## 5 · ⛔ A LINK POINTS BOTH WAYS

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

## 6 · ⭐ WHAT ELSE DESERVES A RECORD

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

## 7 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **a decision as a table row** | ⚠️ it ends up in two tables, and they diverge |
| ⭐ **an accepted record edited in place** | ⛔ **the reason the old decision existed is gone, and nothing shows it was ever different** |
| **a one-sided supersede link** | ⚠️ ⭐ **two records both read as current** |
| **a reused number** | ⛔ every citation resolves to the wrong decision, silently |
| **empty `Evidence`** | ⭐ an opinion, indistinguishable from a measurement |
| **no `Reverting`** | ⚠️ the decision cannot be undone by anyone who was not there |

---

## 8 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ the records themselves | ⭐ the owner of the instance — ⛔ **the folder ships EMPTY** |
| the template and the field rules | whoever maintains the engine, through a recorded decision |
| ⛔ editing an accepted record | **nobody** — ⭐ supersede it instead |

> ## ⭐ THE FOLDER TRAVELS EMPTY, AND THAT IS THE POINT
> ⛔ **Another installation's decisions are not yours.** What travels is the shape; ⭐ **what it
> holds is written by whoever installs it, about their own system.**

---

Related: `README.md` (⭐ **the three document types — this is the append-only one**) ·
`contract-document.md` (⭐ the header and the ceiling this file obeys) · `contract-block.md`
(⭐ §G — a decision inside a block, which graduates here when it outlives the block) ·
`../memory/principles/expertise/doc-structure.md` (⭐ §2.3 — pointer, never copy: why one
decision is one file) · `../bin/check-decisions` (what enforces the 🔒 rows).
