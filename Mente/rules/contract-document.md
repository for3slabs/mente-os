# CONTRACT · DOCUMENT

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every document in the system · ⭐ **including this one**
**Enforcement:** 🔒 lock — `bin/check-document`
**Level:** 🌐 universal — ⭐ travels identical to every clone; a lower level may ADD or TIGHTEN, never loosen
**Verified by:** `bin/check-document` · `bin/probes/probe-document.py`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone

---

## 0 · WHAT THIS FILE IS

> ## ⭐ A document is not trustworthy because it exists. It is trustworthy because its identity, authority, evidence, state and references can be VERIFIED.

⚠️ **The failure it prevents:** a tree of documents where nothing declares whether it is still
true. ⭐ **The modification date becomes the only signal — and a bulk edit destroys even that.**

⛔ **This is not about style.** It is about whether a reader — ⭐ **or an agent** — can tell, in
five seconds, that what they are reading still holds and who says so.

### ⭐ It absorbs three things that used to be separate

| | Why it is here |
|---|---|
| **the header and the ceilings** | the shape itself |
| **naming** | ⭐ a name is the first field a reader reads |
| **moving a file** | ⛔ a move that breaks pointers breaks the shape of every file pointing at it |

⭐ **They share one owner and one moment of change** — you rename, you move, you repoint, in one
action.

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

⭐ **A 🔒 row is written as MUST / MUST NOT** — ⚠️ **that is where ambiguity is paid for.** The
prose around it stays prose: ⛔ a document written entirely in normative capitals is one nobody
finishes.

**IDs are permanent.** `DOC-<area>-<nnn>` — ⛔ never renumbered, never reused. Something cites it.

---

## 2 · ⭐ THREE THINGS A HEADER DECLARES — and they are not the same

⚠️ **The distinction that is missing almost everywhere:** ⭐ **`current` does NOT mean
`authoritative`.** A document can be perfectly up to date and still not be the place a value
lives.

| Axis | Answers | Values |
|---|---|---|
| **Status** | ⭐ is it still in force? | draft · current · superseded · fossil |
| ⭐ **Authority** | ⭐ **may I settle a question with it?** | canonical · reference · evidence · generated |
| ⭐ **Nature** | is what it holds allowed to change? | live · static · dated |

### ⭐ THE CASE THAT FORCES THE SEPARATION

| Document | Status | Authority | Nature | ⭐ And so |
|---|---|---|---|---|
| a generated metrics file | current | **generated** | **live** | ⭐ **read it, never edit it** |
| a dated incident record | current | **evidence** | ⭐ **dated** | ⛔ **refreshing it destroys what it recorded** |

⛔ **Both are `current`. One must be regenerated and the other must never change.** ⚠️ **A single
axis cannot say that.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-AUT-001` | ⭐ **A document declaring itself canonical MUST name what it is canonical for** | 🟡 | ⛔ *"it seems important"* is not a declaration |
| `DOC-AUT-002` | ⭐ **A `generated` document MUST NOT be edited by hand** | 🔒 | ⚠️ the next regeneration silently discards the edit |
| `DOC-AUT-003` | **A `dated` document MUST NOT be refreshed** | 📖 | ⭐ it measures a moment |

⭐ **`Authority` and `Nature` are optional fields** — ⚠️ **but a document that omits them is
treated as `reference` and `static`**, which is the safe default: ⛔ **not the source of anything,
and not expected to change.**

---

## 3 · THE HEADER — four fields, no exceptions

```markdown
# TITLE

**Status:** draft | current | superseded | fossil
**Type:** <one of §4>
**Updated:** YYYY-MM-DD
**Owner:** <who keeps it true>
```

⭐ **Optional, when they apply:** `Authority:` · `Nature:` · `Supersedes:` · `Superseded by:`

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-HDR-001` | ⭐ **All four fields MUST be present** | 🔒 | ⛔ missing one, the document fails this contract whatever it says |
| `DOC-HDR-002` | **`Status` MUST be one of the four** | 🔒 | ⚠️ free text means nothing can read it |
| `DOC-HDR-003` | ⭐ **`Type` MUST be one of §4** | 🔒 | it decides which ceiling applies |
| `DOC-HDR-004` | **`Updated` MUST be `YYYY-MM-DD`** | 🔒 | ⭐ it removes the day/month ambiguity that reads as a different date |
| `DOC-HDR-005` | ⛔ **`superseded` MUST name its replacement** | 🔒 | ⭐ a superseded document with no pointer is a dead end |

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

## 4 · ⭐ TYPES AND THEIR CEILINGS

> ## ⛔ THE TYPE DECIDES THE CEILING. A DOCUMENT WITH NO TYPE HAS NO LIMIT.

| Type | Ceiling | On overflow |
|---|---|---|
| `entry-point` | **250 lines** | ⭐ move content out, keep pointers |
| `contract` | **700 lines** | ⭐ split by topic — ⚠️ see the base-file note below |
| `rule` | **700 lines** | ⭐ split by topic — ⚠️ a base rule ships whole, like a contract |
| `architecture` | **800 lines** | ⛔ split per area |
| `plan` | **400 lines** | move closed phases to the logbook |
| `block` | **200 lines** | see the block contract |
| `folder-readme` | **250 lines** | ⭐ the detail belongs in what it describes |
| `analysis` · `case` | **300 lines** | split or summarise |
| `append-only` | ⭐ **none** | rotate on a fixed period |
| `generated` | none | ⛔ it is generated, never written |
| `fossil` | frozen | ⚠️ does not grow |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-SIZ-001` | ⭐ **Over its ceiling → a pending split** | 🔒 | ⛔ not a warning — named work |
| `DOC-SIZ-002` | **A type with no ceiling MUST declare why** | 📖 | ⚠️ nothing checks this |
| `DOC-SIZ-003` | ⭐ **A numeric ceiling MUST state its unit, and the unit is `lines`** | 🔒 | ⛔ a number with no unit is not a limit — see below |

> ## ⭐ `DOC-SIZ-003` · THE UNIT IS PART OF THE CEILING, NOT DECORATION
> ⛔ **A ceiling with no declared unit is not a limit** — *"too long"* is an opinion, a number
> with a unit is a measurement.
>
> ⚠️ **The unit was written and never verified.** The reader captured the digits and discarded the
> word beside them, so a row reading `250 words` would still have been measured in LINES — the
> table would say one thing, the check would do another, and both would look correct.
>
> ⭐ **`lines` is the choice, and it is a choice:** countable with one command, stable across
> editors, and independent of how the text is wrapped. ⛔ Rows that declare `none` or `frozen`
> carry no unit because they carry no number — a limit that does not exist cannot be measured in
> anything.

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
that a criterion is never cut down the middle to fit a number** — which `../memory/principles/expertise/doc-structure.md` §2.1
already forbids, and a low ceiling would quietly force.

⭐ **`rule` carries the same ceiling for the same reason.** ⚠️ A base rule of this engine is not a
note about one topic: **it can govern several disciplines that share an owner and a moment** — and
splitting those apart is exactly what §2.1 forbids. ⛔ **The ceiling is the signal, and for a base
file the signal fires later.**

---

## 5 · ⭐ ONE LIVE FACT, ONE CANONICAL SOURCE

> ## A live fact MUST have exactly one canonical source.

```
canonical source  ──▶  the value
        ▲
        └── pointers ── documents ── the reader
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-CAN-001` | ⛔ **A document MUST NOT reproduce a live value when a canonical source exists** | 📖 | ⚠️ **nothing verifies this** — see below |
| `DOC-CAN-002` | ⭐ **It MAY describe what the value MEANS. It MUST point at the source** | 📖 | ⚠️ the meaning is stable; the number is not |
| `DOC-CAN-003` | ⭐ **A dated snapshot MAY be copied when the historical value IS the evidence** | 📖 | ⛔ and it is marked `dated` |

### ⭐ Why a copied number is the most reliable defect here

> ## A number copied into prose is correct exactly once.

⚠️ **And the fix is not more discipline — it is removing the copy.**

```
⛔  "the battery is N/N"
✅  "the battery is green — the count lives in the generated metrics"
```

| | Where it lives |
|---|---|
| **live state** — counts, totals, versions | ⭐ the generated metrics file |
| **dated evidence** — *"5 of 11 were missing, on this date"* | ✅ **frozen on purpose** |

⭐ **The distinction matters:** dated evidence must NOT update. ⛔ **Refreshing it destroys what it
recorded.**

---

## 6 · ⭐ WHEN TWO DOCUMENTS DISAGREE

> ## ⛔ THE AGENT MUST NOT CHOOSE BY RECENCY, PROXIMITY OR INTUITION.

**Authority, strongest first:**

| # | Source |
|---|---|
| 1 | ⭐ **an explicit canonical-source pointer** |
| 2 | a current contract or rule |
| 3 | the current architecture |
| 4 | ⭐ **generated state** — measured, not written |
| 5 | dated evidence |
| 6 | ⛔ **a fossil** — ⚠️ never an authority, only a record of what was once believed |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-CFL-001` | ⭐ **On conflict, the higher authority wins** | 📖 | ⛔ nothing verifies this |
| `DOC-CFL-002` | ⭐ **If no source owns it, the divergence is REPORTED, not resolved** | 📖 | ⚠️ declaring an owner is the owner's decision |

⚠️ **`DOC-CFL-002` is the one that matters:** ⭐ **an agent that resolves an ownerless divergence
is inventing authority** — and it does it invisibly, because the result looks like a fixed
document. ⭐ **The full protocol is in `../memory/principles/expertise/doc-structure.md` §5.**

---

## 7 · 🔴 UNKNOWN IS A VALID STATE

> ## ⛔ IF IT CANNOT BE ESTABLISHED FROM AN AUTHORITATIVE SOURCE, IT IS UNKNOWN.

**The agent MUST NOT:**

| ⛔ |
|---|
| invent the value |
| ⭐ **infer it from an unrelated document** |
| copy an outdated one |
| ⚠️ **silently pick between conflicting sources** |

**The agent MUST report it as UNKNOWN, and name what evidence is missing.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-UNK-001` | ⭐ **UNKNOWN is reported, never filled in** | 📖 | ⛔ nothing verifies this |
| `DOC-UNK-002` | ⭐ **UNKNOWN names WHAT is missing** | 📖 | ⚠️ *"unclear"* is not a report |

> ## ⭐ AN AGENT'S NATURAL TENDENCY IS TO FILL THE GAP.
> ⛔ **This system does the opposite: no evidence, no fact.**

⭐ **The same third state, under three names, in three places:** `UNKNOWN` here · `UNKNOWN ≠ PASS`
in the validation owner · `NOT_MEASURED` in the functional criterion. ⭐ **One idea, consistently:
*this is wrong* and *nobody checked* are opposite problems.**

---

## 8 · BODY — the required order

| # | Part | Rule |
|---|---|---|
| 1 | **Purpose** — one paragraph | ⭐ if it needs three, the document does two things |
| 2 | **Content** | numbered `## N · TITLE`, sub-sections `### N.M ·` |
| 3 | **Related** — the last line | pointers to its siblings |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-BOD-001` | **A `Purpose` and a `Related` MUST exist** | 🔒 | both present |
| `DOC-BOD-002` | ⛔ **No `N-bis`, `N-ter`, `N-quater` numbering** | 🔒 | ⭐ see below |

⭐ **`DOC-BOD-002` is 🔒 because it is a symptom, not a style preference.** That numbering appears
when a document grew past its shape and nobody wanted to renumber. ⚠️ **It is the smell that says
*split me*, and it is mechanically detectable — which is rare for a structural defect.**

---

## 9 · CONTENT RULES

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-CNT-001` | ⭐ **A claim carries its evidence** — a number, a file, a command | 📖 | ⛔ nothing checks this |
| `DOC-CNT-002` | ⛔ **A live number MUST NOT be written into prose** | 🔒 | ⭐ §5 |
| `DOC-CNT-003` | **Point, never copy** | 📖 | ⚠️ a duplicated table desynchronises |
| `DOC-CNT-004` | ⭐ **Every path MUST be written from the system root** | 🔒 | ⛔ a bare filename cannot be resolved |
| `DOC-IDS-001` | ⭐ **An id is an ADDRESS — never used twice** | 🔒 | ⛔ measured: one contract carried the same id in two rows, and both read as correct alone |
| `DOC-IDS-002` | ⭐ **A path is declared ONCE in the piece table** | 🔒 | ⛔ measured: eight paths carried a placeholder row AND the real one — different name, class and description |
| `DOC-IDS-003` | ⭐ **The piece table and its template declare the same ENGINE pieces** | 🔒 | ⛔ they were kept in step by hand; a piece missing from the template is missing from every fresh install |
| `DOC-CAP-001` | ⭐ **A capability map marks what is NOT built** | 🔒 | ⛔ a planned row read as a working one sends the reader to run nothing |
| `DOC-CAP-002` | ⭐ **A capability map names everything that IS built** | 🔒 | ⚠️ a piece nobody can find is a piece nobody uses |
| `DOC-CNT-005` | ⛔ **No credential, not even as an example** | 🔒 | ⚠️ what is written stays in history |
| `DOC-CNT-006` | ⭐ **A quotation is verbatim, or it is not a quotation** | 📖 | ⛔ see below |
| `DOC-CNT-007` | ⭐ **A pointer to a `superseded` or `fossil` document is REPORTED** | 🔒 | ⛔ it resolves, and still sends the reader to the wrong page |

⭐ **`DOC-CNT-006` matters more than it looks.** A paraphrase presented as a quote is the agent's
reading standing in for someone's words — ⚠️ **and the reader cannot tell which they are getting.**
⛔ **Paraphrase freely; just do not put it in quotation marks.**

> ## ⭐ `DOC-CAP-001` AND `DOC-CAP-002` ARE ONE RULE FROM TWO SIDES, and the second side is
> the one that gets forgotten.
> ⛔ **A map that promises what does not exist** sends the reader to run a command that is not
> there. ⚠️ **A map that omits what DOES exist** is quieter and lasts longer: the piece works,
> nothing points at it, and it is rebuilt by somebody who could not find it.
>
> ⭐ **Both are the same failure — the map and the tree disagreeing — and only a script notices**,
> because reading the map cannot reveal what the map left out.

⭐ **`DOC-CNT-004` has a second half the checker enforces:** a path must not only carry a
directory — ⛔ **it must RESOLVE.** ⚠️ A well-formed pointer to nothing reads as a promise.

> ## ⭐ `DOC-CNT-007` · RESOLVING IS NOT ENOUGH — the target must still be IN FORCE
> Replacing duplication with pointers is correct, and it moves the risk rather than removing it:
> ⛔ **the target can exist and still be the wrong thing to read.**
>
> ⚠️ **A pointer to a superseded document is worse than a broken one** — the broken one announces
> itself, while this one resolves, opens, and reads as authority. ⭐ It is the same walk
> `DOC-CNT-004` already makes, asking one more question at the end of it: *not only did it
> resolve — what did it resolve TO?*
>
> ⭐ **This is what raises `DOC-LIF-003` off the page.** That rule — *a fossil MUST NOT be used as
> a current authority* — sat in 📖 with nothing behind it. ⚠️ A `superseded` target names its
> replacement (`DOC-HDR-005`), so the report can say where to point instead; a `fossil` names
> nobody, and the reader is told to find the current authority themselves.

---

## 10 · NAMES

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

## 11 · ⭐ DOCUMENTARY OPERATIONS — each one has a rule

⛔ **Editing is not the only thing that happens to a document.** ⭐ **The three that go wrong:**

### `SUPERSEDE`

| ⭐ Rule |
|---|
| the old document becomes `superseded` |
| ⭐ **its replacement is named, and points back** |
| ⛔ **the old document stays — and stops being edited** |

### `SPLIT`

| ⭐ Rule |
|---|
| ⭐ **the halves point at each other** |
| ⛔ **nothing is duplicated across them** |
| ⭐ everything that pointed at the original now points at the right half |

### `ARCHIVE`

| ⭐ Rule |
|---|
| ⭐ **it keeps its name** — ⛔ renaming breaks every pointer at once |
| it becomes `fossil` and stops growing |
| ⛔ **it is never deleted** |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `DOC-OPS-001` | ⭐ **A supersede link is symmetric** | 🔒 | ⛔ one-sided means one of the two is wrong |
| `DOC-OPS-002` | **A split leaves no orphan** | 📖 | ⚠️ ⭐ the reader finds half the answer and cannot know the rest exists |
| `DOC-OPS-003` | ⛔ **An archived document keeps its name** | 📖 | ⭐ nothing verifies this |

---

## 12 · LIFECYCLE

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
| `DOC-LIF-001` | ⭐ **`current` with an old `Updated` is stale, not current** | 🔒 | `bin/check-document`, against the ⬜ threshold below |
| `DOC-LIF-002` | **A fossil is archived, never removed** | 📖 | ⚠️ nothing checks this |
| `DOC-LIF-003` | ⭐ **A fossil MUST NOT be used as a current authority** | 🔒 | ⭐ enforced by `DOC-CNT-007` — every pointer into one is reported |

⭐ **What `current` promises:** somebody verified it, its date reflects the last real change, its
type declares its limits, and someone identified keeps it true. ⛔ **Missing one, it promises
nothing.**

### ⬜ HOW OLD IS TOO OLD

| ⬜ Declaration | Value | Why it is not the engine's |
|---|---|---|
| ⬜ staleness threshold | 0 days | ⛔ a fast-moving project goes stale in weeks; a stable reference does not go stale in a year |

⭐ **`0` means NOT MEASURED, and the rule says so** — ⛔ it does not mean "nothing is ever stale".
An engine that picked a number would be measuring somebody else's pace, and a threshold invented
on the spot becomes the standard by accident.

> ## ⛔ A STALE `current` IS WORSE THAN NO STATUS AT ALL.
> ⚠️ **Because it is believed.** A document with no status gets verified before it is used; one
> that says `current` gets used.

---

## 13 · ⬜ WHAT AN AGENT MAY DO WITH A DOCUMENT IT DOES NOT OWN

⚠️ **`Owner` says who keeps a document true. ⛔ It does not say what somebody else may change** —
⭐ **and an undefined permission is read differently by every reader.**

⬜ **Declare it here.** The engine ships the question, not the answer: ⭐ **how much an agent may
change without asking is the owner's criterion, and it changes per installation.**

| Owner | read | fix a typo | restructure | change the criterion |
|---|---|---|---|---|
| ⬜ the agent itself | ⬜ | ⬜ | ⬜ | ⬜ |
| ⬜ a person | ⬜ | ⬜ | ⬜ | ⬜ |
| ⬜ generated | ⬜ | ⛔ **never** | ⛔ **never** | ⛔ **never** |

⭐ **Only one row ships filled, because it is not a preference:** ⛔ **a generated document is
overwritten by its generator, so an edit there is work that disappears silently.**

**⬜ The questions that settle the rest:**

1. ⬜ May an agent fix a typo in a document it does not own, without asking?
2. ⭐ ⬜ May it reorder sections, if the content does not change?
3. ⬜ What must it never touch, whatever the reason?
4. ⭐ ⬜ **What does it do when the answer is unclear?** — ⛔ the honest default is §7: STOP.

---

## 14 · MOVING A FILE

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
| `DOC-MOV-002` | **Zero orphaned pointers after a move** | 🔒 | ⭐ performed by `DOC-CNT-004` — the same check, not a second one |

⚠️ **Step 1 is the one that gets skipped**, and its cost is invisible: everything works, and the
history of that file is gone. ⭐ **Nothing fails, so nothing tells you.**

⚠️ **Step 2 is the one measured to fail.** A search that respects ignore rules skips exactly the
files nobody remembers — ⭐ **and those are the ones with the stale pointers.**

---

## 15 · MIGRATION — ⛔ never in bulk

| Case | What happens |
|---|---|
| **a new document** | ⭐ born with this contract |
| **an existing one, when touched** | gets the header then |
| ⛔ **one nobody touches** | ⭐ **left alone** |

⭐ **Reheadering what nobody reads is work with no return** — and a bulk edit destroys the
modification date, which is the only staleness signal a document without a header has.

---

## 16 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **no header** | ⛔ nothing can tell a live document from a fossil |
| ⭐ **a live number in prose** | ⭐ **it is wrong from the second read**, and it teaches distrust of the rest |
| **over the ceiling, unsplit** | ⚠️ it stops being read in full — ⛔ **and a document read in half looks complete** |
| ⭐ **a gap filled instead of reported** | ⛔ **an invented fact is indistinguishable from a measured one** |
| **a conflict resolved silently** | ⚠️ ⭐ the agent invented authority, and nothing shows it |
| **a generated file edited by hand** | ⭐ the edit disappears at the next run, with no error |
| **a move with orphaned pointers** | readers reach a dead end and rewrite what already existed |

---

## 17 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| the ceilings in §4 | ⭐ the owner of the instance, ⚠️ **once, in writing** |
| ⬜ §13 — the permission matrix | ⭐ **the owner** — the engine ships only the question |
| the rules and their IDs | whoever maintains the engine, through a recorded decision |
| ⛔ exempting a document from §3 | **nobody** — ⭐ an exemption is declared in the document, never assumed |
| ⛔ treating UNKNOWN as a value | **nobody** — ⚠️ ⭐ it is the defect §7 exists to stop |

---

**Decided by:** `decisions/ADR-027-ceilings-are-per-document-type.md` — ⭐ **why the ceiling is a SIGNAL**, why per type, and what a global limit discredits.
**Also decided by:** `decisions/ADR-023-instructions-are-in-one-language.md` — ⭐ **why identifiers live in one declared language**, and why the owner's thinking does not.

Related: `README.md` (⭐ **the three document types, and how law is written here**) ·
`contract-block.md` · `contract-adr.md` (⭐ the shape of an append-only record) ·
`../memory/principles/owner-1-docs.md` (⭐ **who applies this and rejects on it**) ·
`../memory/principles/expertise/doc-structure.md` (⭐ the criterion behind the shape — ⛔ how to
split well, and §5 the conflict protocol) · `../memory/principles/expertise/val-functional.md`
(⭐ the third state, under its other name) · `../bin/check-document` (what enforces the 🔒 rows).
