# CONTRACT · DOCUMENT

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every document in the system · ⭐ **including this one**
**Enforcement:** 🔒 lock — `bin/check-document`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone

---

## 0 · WHAT THIS FILE IS

> ## ⭐ The shape a document must have to be trusted six months later.

⚠️ **The failure it prevents:** a tree of documents where nothing declares whether it is still
true. ⭐ **The modification date becomes the only signal — and a bulk edit destroys even that.**

⛔ **This is not about style.** It is about whether a reader can tell, in five seconds, that what
they are reading still holds.

### ⭐ It absorbs three things that used to be separate

| | Why it is here |
|---|---|
| **the header and the ceilings** | the shape itself |
| **naming** | ⭐ a name is the first field a reader reads |
| **moving a file** | ⛔ a move that breaks pointers breaks the shape of every file pointing at it |

⭐ **They share one owner and one moment of change** — you rename, you move, you repoint, in one
action. **Three files made you open three files to do one thing.**

---

## 1 · ⭐ ENFORCEMENT — what is actually checked

⛔ **Every rule below declares whether anything verifies it.** The system's own measured law: a
rule in code is followed 100%, a rule in a document 40-60%.

| | Means |
|---|---|
| 🔒 **lock** | ⭐ a script refuses — ⚠️ and it has been seen to fail |
| 🟡 **prompt** | the agent asks before proceeding |
| 📖 **discipline** | ⛔ **nothing verifies this.** It says so on purpose |

> ## ⛔ NEVER PRESENT A 📖 AS A 🔒
> ⭐ A limit everyone believes enforced, and is not, is worse than no limit: **the belief replaces
> the vigilance.**

**IDs are permanent.** `DOC-<area>-<nnn>` — ⛔ never renumbered, never reused. Something cites it.

---

## 2 · THE HEADER — four fields, no exceptions

```markdown
# TITLE

**Status:** draft | current | superseded | fossil
**Type:** <one of §3>
**Updated:** YYYY-MM-DD
**Owner:** <who keeps it true>
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-HDR-001` | ⭐ **All four fields present** | 🔒 | ⛔ missing one, the document fails this contract whatever it says |
| `DOC-HDR-002` | **`Status` is one of the four** | 🔒 | ⚠️ a free-text status means nothing can read it |
| `DOC-HDR-003` | ⭐ **`Type` is one of §3** | 🔒 | it decides which ceiling applies |
| `DOC-HDR-004` | **`Updated` in `YYYY-MM-DD`** | 🔒 | ⭐ avoids the day/month ambiguity that silently reads as a different date |
| `DOC-HDR-005` | ⛔ **`superseded` names its replacement** | 🔒 | ⭐ a superseded document with no pointer is a dead end |

### What each field prevents

| Field | ⛔ Without it |
|---|---|
| **Status** | ⭐ **a fossil looks current** — and nothing distinguishes them |
| **Type** | ⚠️ no ceiling can be applied, so none is |
| **Updated** | nothing can be flagged stale |
| **Owner** | ⭐ **nobody updates it, and no alarm fires** |

⚠️ **`Type` is the one that fails silently:** a wrong type does not look wrong. The document reads
fine and the wrong ceiling is applied to it.

---

## 3 · ⭐ TYPES AND THEIR CEILINGS

> ## ⛔ THE TYPE DECIDES THE CEILING. A DOCUMENT WITH NO TYPE HAS NO LIMIT.

| Type | Ceiling | On overflow |
|---|---|---|
| `entry-point` | **250 lines** | ⭐ move content out, keep pointers |
| `contract` | **700** | ⭐ split by topic — ⚠️ see the base-file note below |
| `rule` | **250** | split by topic |
| `architecture` | **800** | ⛔ split per area |
| `plan` | **400** | move closed phases to the logbook |
| `block` | **200** | see the block contract |
| `folder-readme` | **250** | ⭐ the detail belongs in what it describes |
| `analysis` · `case` | **300** | split or summarise |
| `append-only` | ⭐ **none** | rotate on a fixed period |
| `generated` | none | ⛔ it is generated, never written |
| `fossil` | frozen | ⚠️ does not grow |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-SIZ-001` | ⭐ **Over its ceiling → a pending split** | 🔒 | ⛔ not a warning — named work |
| `DOC-SIZ-002` | **A type with no ceiling declares why** | 📖 | ⚠️ nothing checks this |

### ⭐ THE RULE BEHIND THE CEILING

> ## A file is not split because of its size. It is split when it holds TWO DISTINCT THINGS.
> ⭐ **The ceiling is the SIGNAL, not the cause.**

⚠️ **Measured, and it is the strongest evidence in this contract:** in a tree where exactly one
file declared a ceiling, ⭐ **that was the only file that never overflowed.** The others reached
thousands of lines. **The number did not constrain them; declaring it did.**

⛔ **Splitting is governed by `../memory/principles/expertise/doc-structure.md` §2.1** — cut by
subject, never by length, and nothing duplicated across the halves.

### ⭐ WHY `contract` CARRIES THE HIGHEST CEILING OF ANY WRITTEN TYPE

⚠️ **A contract is a BASE file: it ships whole, and its reader is a stranger.** ⭐ **Every other
type can point somewhere else for the detail; a contract IS the detail** — it is the document
people open precisely when they need the part nobody remembered to summarise.

⛔ **This is not a licence to ramble.** The ceiling still forces curation at close, and a padded
contract fails `DOC-BOD-001` long before it fails this row. ⭐ **What the raised ceiling buys is
that a criterion is never cut down the middle to fit a number** — which `doc-structure.md` §2.1
already forbids, and a low ceiling would quietly force.

---

## 4 · BODY — the required order

| # | Part | Rule |
|---|---|---|
| 1 | **Purpose** — one paragraph | ⭐ if it needs three, the document does two things |
| 2 | **Content** | numbered `## N · TITLE`, sub-sections `### N.M ·` |
| 3 | **Related** — the last line | pointers to its siblings |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-BOD-001` | **A `Purpose` and a `Related` exist** | 🔒 | both present |
| `DOC-BOD-002` | ⛔ **No `N-bis`, `N-ter`, `N-quater` numbering** | 🔒 | ⭐ see below |

⭐ **`DOC-BOD-002` is 🔒 because it is a symptom, not a style preference.** That numbering appears
when a document grew past its shape and nobody wanted to renumber. ⚠️ **It is the smell that says
*split me*, and it is mechanically detectable — which is rare for a structural defect.**

---

## 5 · CONTENT RULES

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-CNT-001` | ⭐ **A claim carries its evidence** — a number, a file, a command | 📖 | ⛔ nothing checks this |
| `DOC-CNT-002` | ⛔ **A live number is never written into prose** | 🔒 | ⭐ see below |
| `DOC-CNT-003` | **Point, never copy** | 📖 | ⚠️ a duplicated table desynchronises |
| `DOC-CNT-004` | **Every path is written from the system root** | 🔒 | ⭐ a bare filename cannot be resolved |
| `DOC-CNT-005` | ⛔ **No credential, not even as an example** | 🔒 | ⚠️ what is written stays in history |

### ⭐ `DOC-CNT-002` — why a copied number is the most reliable defect here

> ## A number copied into prose is correct exactly once.

⚠️ **And the fix is not more discipline — it is removing the copy.**

```
⛔  "the battery is N/N"
✅  "the battery is green — the count lives in the generated metrics"
```

| | Where it lives |
|---|---|
| **live state** — counts, totals, versions | ⭐ the generated metrics file |
| **dated evidence** — *"5 of 11 were missing, on this date"* | ✅ **frozen on purpose** — it measures a moment |

⭐ **The distinction matters:** dated evidence must NOT update. It is a measurement of a past
state, and refreshing it destroys what it recorded.

---

## 6 · NAMES

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-NAM-001` | **lowercase, hyphens — ⛔ never underscores or spaces** | 🔒 | inspect the name |
| `DOC-NAM-002` | ⭐ **The name states the SUBJECT, never the moment** | 📖 | ⛔ nobody remembers which week |
| `DOC-NAM-003` | ⛔ **No date or version in a filename** | 🔒 | ⭐ version control already knows |
| `DOC-NAM-004` | ⛔ **No `-v2`, `-final`, `-new`, `-old`** | 🔒 | ⚠️ see below |
| `DOC-NAM-005` | **A type prefix when the type matters for retrieval** | 📖 | `rule-` · `contract-` · `case-` · `plan-` |
| `DOC-NAM-006` | ⭐ **UPPERCASE only for entry points** | 🔒 | ⛔ a name shouting for no reason is noise |
| `DOC-NAM-007` | ⛔ **A filename never names a person** | 🔒 | ⭐ it outlives whoever installed the system |

⭐ **`DOC-NAM-004` is 🔒 because a version in a filename means two documents exist for one subject
and nobody decided which is true** — the divergence of `DOC-CNT-003`, already happened.

⭐ **One concept, one word, everywhere.** Two names for one thing means somebody will eventually
treat them as two things.

---

## 7 · MOVING A FILE

⛔ **A move is not a rename. It is a rename plus every pointer that resolved to the old place.**

| # | Step | ⚠️ What goes wrong |
|---|---|---|
| 1 | ⭐ **Is it tracked? Move it with version control, not the shell** | ⛔ **the file's history stops at the move** |
| 2 | **Find who points at it** | search the whole tree, ⭐ **including ignored files** |
| 3 | **Repoint every hit** | ⚠️ memories and configuration too |
| 4 | ⭐ **Verify: zero orphaned pointers** | ⛔ a pointer to nothing reads as a promise |
| 5 | **Commit with the reason, not just the what** | the next reader asks why |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-MOV-001` | ⭐ **A tracked file is moved by version control** | 📖 | ⛔ nothing checks this |
| `DOC-MOV-002` | **Zero orphaned pointers after a move** | 🔒 | ⭐ every reference resolves |

⚠️ **Step 1 is the one that gets skipped**, and its cost is invisible: everything works, and the
history of that file is gone. ⭐ **Nothing fails, so nothing tells you.**

⚠️ **Step 2 is the one measured to fail.** A search that respects ignore rules skips exactly the
files nobody remembers — ⭐ **and those are the ones with the stale pointers.**

---

## 8 · LIFECYCLE

```
draft ──▶ current ──▶ superseded ──▶ fossil
                          │              │
                 names its replacement   └─▶ archived, keeps its name
```

| Status | Means | Editable? |
|---|---|---|
| `draft` | being written | ✅ |
| `current` | in force | ✅ ⭐ with `Updated` bumped |
| `superseded` | replaced — ⛔ **must name its replacement** | only to add the pointer |
| `fossil` | historical | ⛔ frozen |

> ## ⭐ A FOSSIL IS MARKED, NEVER DELETED
> ⚠️ **Deleting history is how you lose the ability to diagnose.** The incident nobody can explain
> is the one whose record was tidied away.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-LIF-001` | ⭐ **`current` with an old `Updated` is stale, not current** | 🔒 | ⛔ re-verify or restate |
| `DOC-LIF-002` | **A fossil is archived, never removed** | 📖 | ⚠️ nothing checks this |

⭐ **What `current` promises:** somebody verified it, its date reflects the last real change, its
type declares its limits, and someone identified keeps it true. ⛔ **Missing one, it promises
nothing.**

---

## 9 · MIGRATION — ⛔ never in bulk

| Case | What happens |
|---|---|
| **a new document** | ⭐ born with this contract |
| **an existing one, when touched** | gets the header then |
| ⛔ **one nobody touches** | ⭐ **left alone** |

⭐ **Reheadering what nobody reads is work with no return** — and a bulk edit destroys the
modification date, which is the only staleness signal a document without a header has.

---

## 10 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **no header** | ⛔ nothing can tell a live document from a fossil |
| **a live number in prose** | ⭐ **it is wrong from the second read**, and it teaches distrust of the rest |
| **over the ceiling, unsplit** | ⚠️ it stops being read in full — ⛔ **and a document read in half looks complete** |
| **a move with orphaned pointers** | ⭐ readers reach a dead end and rewrite what already existed |

---

## 11 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| the ceilings in §3 | ⭐ the owner of the instance, ⚠️ **once, in writing** |
| the rules and their IDs | whoever maintains the engine, through a recorded decision |
| ⛔ exempting a document from §2 | **nobody** — ⭐ an exemption is declared in the document, never assumed |

---

Related: `README.md` (⭐ **the three document types, and how law is written here**) ·
⬜ the block contract and the decision-record contract (⭐ not written yet — see the backlog) ·
`../memory/principles/owner-1-docs.md` (⭐ **who applies this and rejects on it**) ·
`../memory/principles/expertise/doc-structure.md` (⭐ the criterion behind the shape — ⛔ how to
split well) · `../bin/check-document` (what enforces the 🔒 rows).
