# CONTRACT · BLOCK

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every `BLOCK.md` — open, blocked, closed or archived
**Enforcement:** 🔒 lock — `bin/check-block`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone

---

## 0 · WHAT THIS FILE IS

> ## ⭐ One unit of work, one file — from the day it opens to the day it is archived.

⚠️ **The failure it prevents:** work that exists only in a conversation. ⭐ **When the session
ends, the code is still on disk and the reasoning is not** — and the next person, or the next
session, rebuilds what was already decided.

### ⭐ It absorbs the whole life of a block

| | Why it is here |
|---|---|
| **the shape** — the sections | what a block IS |
| **opening and closing** | ⭐ the same fields, at two different moments |
| **the blocked state** | ⚠️ a state, not a separate document |
| **the archive** | ⛔ what a block becomes — its last transition |

⭐ **One owner, one cycle of change.** Adding a section changes the shape, what closing checks,
and what gets archived — **in one edit.** Four files made that four edits, and they drifted.

---

## 1 · ENFORCEMENT

| | Means |
|---|---|
| 🔒 **lock** | ⭐ a script refuses — ⚠️ and it has been seen to fail |
| 🟡 **prompt** | the agent asks before proceeding |
| 📖 **discipline** | ⛔ **nothing verifies this** |

**IDs are permanent.** `BLK-<area>-<nnn>` — ⛔ never renumbered, never reused.

---

## 2 · THE SHAPE

> ## ⭐ ONE BLOCK = ONE FILE. Sections A-K, in order.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-SHP-001` | ⭐ **One file per block** | 🔒 | ⛔ splitting a short file across files adds places to desynchronise |
| `BLK-SHP-002` | **Sections in order, A to K** | 🔒 | ⭐ order is what makes the top of the file the cheap part |
| `BLK-SHP-003` | **Within its ceiling** | 🔒 | the document contract decides the number |

### ⭐ Cheap to open, expensive to close

| Moment | Required |
|---|---|
| **OPEN** | ⭐ **A · B · C · D — four fields, about two minutes** |
| **while working** | E through J, filled as they become known |
| **CLOSE** | everything, ⛔ plus the sufficiency test |

⛔ **If opening costs ten fields, work happens WITHOUT a block** — and then nothing is recorded at
all. ⭐ **A cheap open is not laxity: it is what makes the record exist.**

---

## 3 · THE SECTIONS

| § | Section | Required | Tier |
|---|---|---|---|
| **A** | `Identity` | 🔴 open | 1 |
| **B** | ⭐ `Scope` — IN / OUT | 🔴 open | 1 |
| **C** | `Connections` | 🔴 open | 1 |
| **D** | `Required standards` | 🔴 open | 1 |
| **E** | `State` | 🟡 working | 1 |
| **F** | `Sub-blocks` | 🟡 working | 2 |
| **G** | `Decisions` | 🟡 working | 2 |
| **H** | `Friction log` | 🟡 working | 2 |
| **I** | `Checkpoints` | 🟡 working | 3 |
| **J** | `Context` | 🟡 working | 3 |
| **K** | ⭐ `Closing` | 🔴 close | — |

⭐ **Tiers are the ORDER inside the file, not separate files.** Tier 1 is what a reader needs to
resume safely; tiers 2 and 3 are for whoever needs the detail. ⛔ **A reader who must open three
files to know where the work stands will not open any.**

### A · Identity — 🔴 to open

```
id: <unique-name>
type: code | docs | infra | data
intent: one sentence — what this block is for
status: active | blocked | closed
lane: direct | task | full-block
owner: <who>
created: <date> · updated: <date>
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-IDN-001` | ⭐ **`id` globally unique — resolution is EXACT** | 🔒 | ⛔ no match means stop and ask, never guess the closest |
| `BLK-IDN-002` | ⭐ **`type` present** — it decides which metrics apply | 🔒 | see below |
| `BLK-IDN-003` | **`intent` is one sentence** | 🔒 | ⚠️ if you cannot write it, you do not know what you are doing yet |
| `BLK-IDN-004` | **`status` exactly one of the three** | 🔒 | ⛔ free text means nothing can read it |
| `BLK-IDN-005` | **`updated` is a date, and recent** | 🔒 | ⭐ stale after a declared period |

#### ⭐ Why `type` exists — a validator measuring the wrong thing teaches you to ignore it

⚠️ **Run a code-shaped grader on a documentation block and it reports zero tests and zero
importers** — ⛔ **a permanent fail, for measuring what does not apply.**

| `type` | Measured | ⛔ Reported `n/a`, with the reason |
|---|---|---|
| `code` | dead files · duplication · tests · import cycles | — |
| `docs` | broken pointers · orphans · sizes · staleness | tests · imports · duplication |
| `infra` | a runbook exists · rollback documented · secrets referenced | everything code-shaped |
| `data` | the migration reverses · schema documented · relations declared | tests · duplication |

> ## ⛔ TWO HARD RULES
> ⭐ **`n/a` is never a pass.** A metric that does not apply prints `n/a` **with its reason** —
> silence would let a block look like it passed a check it never ran.
>
> ⭐ **The type does not lower the bar, it changes the ruler.** A `docs` block still reaches a
> verdict; it reaches it with different measurements.

⚠️ **A block genuinely half one type and half another is TWO blocks** — ⭐ they would not close on
the same day, for the same reason.

### B · Scope — 🔴 to open · ⭐ the critical one

```
## ✅ IN     what this block may touch
## ⛔ OUT    what is explicitly out of bounds, and why
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-SCP-001` | ⭐ **Both halves present — IN and OUT** | 🔒 | ⛔ an IN with no OUT is a wish, not a boundary |
| `BLK-SCP-002` | ⭐ **Each OUT states WHY** | 🟡 | ⚠️ without the reason, the next reader deletes it as arbitrary |
| `BLK-SCP-003` | ⛔ **Scope is not widened silently** | 🟡 | ⭐ a change to scope is a decision, and decisions go in §G |

⭐ **§B is the critical one because it is the only section that can say NO.** Everything else
describes the work; this one bounds it. ⚠️ **A block with no OUT grows until it cannot close.**

### C · Connections — 🔴 to open

⭐ **What this block depends on, and what depends on it.** ⛔ **Anything not declared here is out
of reach:** a block does not read another block's files on a hunch.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-CON-001` | **Every dependency named** | 🔒 | the section exists and is not empty |
| `BLK-CON-002` | ⭐ **Undeclared means forbidden** | 📖 | ⛔ nothing checks this — ⚠️ see below |

⚠️ **`BLK-CON-002` is 📖 and it matters**, because inferring a connection from a similar name is
exactly how one block's assumptions leak into another's work.

### D · Required standards — 🔴 to open

⭐ **Which criterion files this block is judged by.** ⛔ **A block that declares none is judged by
whatever the reader remembers.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-STD-001` | ⭐ **At least one standard declared** | 🔒 | ⛔ none means no basis for rejection |
| `BLK-STD-002` | **Each declared file exists** | 🔒 | ⚠️ a standard pointing at nothing is not a standard |

### E · State — 🟡 · ⭐ the section read first

⭐ **Where the work stands, right now.** It has a hard ceiling on purpose: **it is read every time
someone resumes, and a long state stops being read.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-STA-001` | **Within its ceiling** | 🔒 | ⭐ the value is that it is always read in full |
| `BLK-STA-002` | ⭐ **Updated when the state changes, not at close** | 📖 | ⛔ nothing checks this |

### F-J · While working

| § | Holds | ⭐ The rule that matters |
|---|---|---|
| **F** `Sub-blocks` | the tasks inside | ⛔ a closed block with an open sub-block does not close |
| **G** `Decisions` | ⭐ **each with its rationale** | ⚠️ a decision with no reason gets re-argued |
| **H** `Friction log` | what a rule blocked, and its cost | ⭐ this is the evidence that changes a rule |
| **I** `Checkpoints` | ⭐ a safe point to resume from | ⛔ not a diary |
| **J** `Context` | ⭐ **curated, never a log** | ⚠️ the reasoning worth keeping, not everything said |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-WRK-001` | ⭐ **Every decision in §G carries its rationale** | 🟡 | ⛔ *"we chose X"* with no why |
| `BLK-WRK-002` | **§J is curated** | 📖 | ⚠️ ⭐ a context that grows with every message is a transcript |

⭐ **§H is the one people skip, and it is the one that keeps the law alive.** ⛔ **A rule nobody
logs friction against never changes** — the friction goes somewhere else: around the rule.

### K · Closing — 🔴 to close

⭐ **What the verdict was, what was learned, and what debt this did NOT close.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-CLS-001` | ⭐ **§K present before `status: closed`** | 🔒 | ⛔ closed with no closing section |
| `BLK-CLS-002` | **No open sub-block in §F** | 🔒 | ⚠️ closing over an open task hides it |
| `BLK-CLS-003` | ⭐ **What was NOT done is stated** | 🟡 | ⛔ silence reads as completeness |
| `BLK-CLS-004` | ⭐ **The verdict cites its evidence** | 🟡 | see the validation criterion |

⭐ **`BLK-CLS-003` is what makes an archive worth reading.** A closing that lists only successes
teaches the next reader that this kind of work always succeeds.

---

## 4 · ⭐ THE SUFFICIENCY TEST

> ## Do sections A-E suffice to restart this work safely, with no other context?

⛔ **If the answer is no, the block does not close** — whatever else is filled in.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-SUF-001` | ⭐ **A-E suffice to resume** | 🟡 | ⚠️ read only A-E and try to state the next action |

⭐ **This is the only test in this contract that a script cannot do**, and it is the most
important one. ⚠️ **A block that passes every mechanical check and fails this one is a block whose
knowledge died with the session that wrote it.**

---

## 5 · OPENING

| # | Step | ⚠️ What goes wrong |
|---|---|---|
| 1 | ⭐ **Is this a NEW block, or an existing one?** | ⛔ a duplicate splits the record of one job |
| 2 | **Write A, B, C, D** | ⭐ about two minutes — ⛔ no more |
| 3 | **Declare it where blocks are listed** | ⚠️ an undeclared block is invisible to every check |

⭐ **Step 1 has a rule:** it is a NEW block when it would close on a different day for a different
reason. ⛔ **Otherwise it is a sub-block of one that already exists.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-OPN-001` | **A, B, C, D present at open** | 🔒 | the four sections exist |
| `BLK-OPN-002` | ⭐ **The block is declared where blocks are listed** | 🔒 | ⛔ otherwise nothing knows it exists |

---

## 6 · THE `blocked` STATE

⭐ **`blocked` is a state, not a parking space.** It says: *this cannot proceed, and here is what
would unblock it.*

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-BLK-001` | ⭐ **A blocked block names WHAT would unblock it** | 🔒 | ⛔ *"waiting"* is not a blocker |
| `BLK-BLK-002` | ⭐ **Blocked past a declared period → it is asked about** | 🔒 | ⚠️ see below |

> ## ⭐ AT THE THRESHOLD: ASK, DO NOT ACCUSE
> ⚠️ **A block sitting blocked for weeks is not necessarily neglect** — it may be waiting on
> something real. ⭐ **The prompt asks whether it is still current**, and the answer is one of
> three: still waiting, unblock it, or close it. ⛔ **What is not allowed is silence.**

⭐ **A stale-blocked check that accuses gets ignored; one that asks gets answered.** The
difference is measured in whether anyone ever responds to it.

---

## 7 · CLOSING AND ARCHIVING

```
active ──▶ closed ──▶ archived
   └──▶ blocked ──▶ active | closed
```

| # | Step |
|---|---|
| 1 | ⭐ **§K written** — verdict, what was learned, what debt remains |
| 2 | **The sufficiency test passes** (§4) |
| 3 | ⛔ **No open sub-block** |
| 4 | **Move it to the archive, keeping its name** |
| 5 | ⭐ **Repoint whatever pointed at it** |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-ARC-001` | ⭐ **An archived block keeps its name** | 🔒 | ⛔ renaming on archive breaks every pointer at once |
| `BLK-ARC-002` | **The archive carries a summary and what it affects** | 🔒 | both present |
| `BLK-ARC-003` | ⛔ **Nothing is deleted from the archive** | 📖 | ⭐ a closed block is consultable experience |

> ## ⭐ WHAT WAS LEARNED IS THE ONLY PART THAT IS NOT A COPY
> ⚠️ Everything else in an archive already existed somewhere. **This section is written once, at
> the moment the knowledge is still fresh — and it is the reason anyone opens an archive at all.**

⛔ **What never goes in an archive:** a credential, a live number, or a pointer to something that
moved. ⭐ **An archive is read years later, and it cannot be corrected then.**

---

## 8 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **no §B OUT** | ⚠️ the block grows until it cannot close |
| **closed with an open sub-block** | ⛔ the task disappears — ⭐ **nobody knows it was dropped** |
| **§K with no "what was not done"** | the next reader assumes this kind of work always succeeds |
| ⭐ **fails the sufficiency test** | ⛔ **the knowledge died with the session that wrote it** |
| **renamed on archive** | every pointer breaks at once, and none of them says so |

---

## 9 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ which sections this installation adds | the owner, ⚠️ **as a new section, never by editing A-K** |
| the rules and their IDs | whoever maintains the engine, through a recorded decision |
| ⛔ closing a block that fails §4 | **nobody** — ⭐ the sufficiency test has no override |

---

Related: `README.md` (⭐ **the three document types**) · `contract-document.md` (⭐ the shape and
the ceiling this file obeys) · ⬜ the decision-record contract (not written yet — see the backlog) ·
`../memory/principles/owner-3-validation.md` (⭐ **who decides a block may close**) ·
`../memory/principles/expertise/val-functional.md` (⭐ what counts as evidence in §K) ·
`../bin/check-block` (what enforces the 🔒 rows).
