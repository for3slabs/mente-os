# CONTRACT · ARCHIVE

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every closed block, once it moves to the archive
**Enforcement:** 🔒 lock — `bin/check-archive`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone

---

## 0 · WHAT THIS FILE IS

> ## ⭐ The block contract says what an ACTIVE block carries. This says what SURVIVES when it closes.

⚠️ **The gap it fills is a measured one:** a validator already refused an archived block missing
its files, and the design already named them — ⛔ **but nothing said what goes INSIDE them.**

> ## ⭐ A VALIDATOR THAT DEMANDS A FILE WHOSE CONTENT IS UNDEFINED PRODUCES EMPTY FILES.
> ⛔ **They satisfy the check and teach nothing** — and the check goes green over them.

### ⭐ Why an archive exists at all

⭐ **A closed block is consultable experience.** ⛔ **A closed block that cannot be consulted was
not closed: it was abandoned with paperwork.**

⚠️ **And the difference is invisible from the outside** — both look like a folder that is no
longer active.

---

## 1 · ENFORCEMENT

| | Means |
|---|---|
| 🔒 **lock** | ⭐ a script refuses — ⚠️ and it has been seen to fail |
| 🟡 **prompt** | the agent asks before proceeding |
| 📖 **discipline** | ⛔ **nothing verifies this** |

**IDs are permanent.** `ARC-<area>-<nnn>` — ⛔ never renumbered, never reused.

---

## 2 · THE SHAPE

```
<archive>/<name>_<closing period>/
├── SUMMARY.md       🔴 what was done and what was LEARNED
├── connections.md   🔴 what this leaves affected for everyone else
└── BLOCK.md         🔴 the block as it closed, ⛔ moved verbatim
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `ARC-SHP-001` | ⭐ **All three files present** | 🔒 | ⛔ one missing and the archive is not consultable |
| `ARC-SHP-002` | ⭐ **The two written files are DOCUMENTS** | 🔒 | ⚠️ header, purpose and pointers, like everything else |
| `ARC-SHP-003` | ⭐ **The folder name carries the CLOSING period, not the opening one** | 🔒 | ⛔ see below |
| `ARC-SHP-004` | ⛔ **The block file is moved verbatim** | 📖 | ⭐ §5 |

⚠️ **`ARC-SHP-002` was found on the first real close:** the validator refused the two new files
because they carried no header — ⭐ **and the contract had not said they were documents.** ⛔ A
contract that omits an obligation produces a defect on first use, not later.

⭐ **`ARC-SHP-003` matters for a reason that only shows up later:** ⚠️ **two blocks with the same
name in different periods are two entries, not a conflict** — and dating by the opening would
collide the moment a name is reused.

### ⛔ WHAT DOES NOT MOVE WITH THE BLOCK

| | ⭐ Why |
|---|---|
| **disposable working files** | ⭐ disposable by definition |
| ⚠️ **documents other work consults** | ⛔ **a document read by others stays where it is** — the summary points at it |

⭐ **Moving a shared document into an archive is how a live reference becomes a dead one** — ⚠️ and
nothing warns, because the file still exists.

---

## 3 · `SUMMARY.md` — what was done and what was learned

| Field | Req | ⭐ Rule |
|---|---|---|
| **what it was for** | 🔴 | ⭐ **the block's intent, verbatim** — ⛔ not rewritten from memory |
| **what was built** | 🔴 | the closed sub-blocks, ⭐ each with what landed it |
| **the quality verdict** | 🔴 | ⚠️ **with its numbers**, not its conclusion |
| ⭐ **what was LEARNED** | 🔴 | ⭐ **the part that makes this consultable** — §4 |
| **what was left out** | 🔴 | ⛔ **what did NOT get done, and why** |
| **debt handed over** | 🟡 | ⭐ what another block inherits, naming it |

> ## ⬜ THE FIELD NAMES ARE YOURS — the fields are not
> ⭐ **The engine fixes WHAT an archive must answer, never what the headings are
> called.** ⚠️ An installation writing its records in another language is not in
> violation — ⛔ **one that omits a field is.**
>
> ⬜ **Declare your heading for each field** in the project rules, and the check
> reads them from there.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `ARC-SUM-001` | **Every required field present** | 🔒 | ⛔ a missing one is not an omission, it is a false record |
| `ARC-SUM-002` | ⭐ **"What was left out" is never empty** | 🔒 | ⚠️ ⭐ see below |
| `ARC-SUM-003` | ⭐ **The intent is copied, not paraphrased** | 📖 | ⛔ a rewritten intent is the intent as remembered |

> ## ⭐ AN EMPTY "WHAT WAS LEFT OUT" IS A LIE
> ⚠️ **No block closes having done everything it could have.** ⛔ **Silence there does not say
> "nothing was left" — it says nobody looked**, and the next reader inherits the difference.

⭐ **And the verdict carries its numbers for the same reason a claim carries its evidence:** ⛔ *"it
passed"* cannot be re-examined; ⭐ **the measurement can.**

---

## 4 · ⭐ "WHAT WAS LEARNED" — the only section that is not a copy

⚠️ **Everything else in the summary is consolidation of what already existed.** ⭐ **This one is
written once, and it is the reason anybody opens the file.**

> ## ⭐ THE TEST
> **Would a person opening this a year from now avoid a mistake because of this line?**
> ⛔ **If not, it is a description, not a lesson.**

| ✅ A lesson | ⛔ Not a lesson |
|---|---|
| ⭐ *"a default must never point at something that has an owner"* | *"we fixed the routing bug"* |
| ⭐ *"a dependent is what IMPORTS a piece — mentions outnumbered imports three to one"* | *"we measured the dependents"* |
| ⭐ *"one value was used as if it were another, and the same bug surfaced in six files"* | *"we refactored that field"* |

⭐ **The pattern in the left column: each one states a RULE somebody can apply.** ⚠️ **The right
column states an EVENT nobody can reuse.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `ARC-LRN-001` | 🔴 **"What was learned" is never empty** | 🔒 | ⛔ the one section that is not consolidation |
| `ARC-LRN-002` | ⭐ **A lesson states a rule, not an event** | 🟡 | ⚠️ apply the test above |
| `ARC-LRN-003` | ⭐ **A lesson that repeats becomes a RULE** | 📖 | ⛔ see below |

> ## ⭐ A LESSON THAT REPEATS GENERALISES
> ⚠️ **The same lesson in three archives is not three lessons: it is a rule nobody wrote.**
> ⭐ **That is how an error becomes a FORM instead of staying an anecdote** — and it is the only
> path by which an archive changes anything.

---

## 5 · `connections.md` — what this leaves affected

⭐ **Its job is to answer, for whoever opens the NEXT block:** *"what does this closing change for
me?"*

| Field | Req | ⭐ Rule |
|---|---|---|
| **pieces this block owned** | 🔴 | ⭐ now free for another block to claim |
| **blocks that depended on it** | 🔴 | ⚠️ **each one, and whether that dependency is satisfied or ORPHANED** |
| **rules it created** | 🟡 | ⭐ what now applies beyond this block |
| **what is still open** | 🔴 | ⛔ **and where it went** |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `ARC-CON-001` | ⭐ **Every dependent named, with its dependency's fate** | 🔒 | ⛔ satisfied or orphaned — never unstated |
| `ARC-CON-002` | ⭐ **Every id named exists** | 🔒 | ⚠️ a pointer to nothing reads as a promise |
| `ARC-CON-003` | 🔴 **Anything still open names where it MOVED** | 🔒 | ⭐ see below |

> ## 🔴 A BLOCK DOES NOT CLOSE OVER AN OPEN SUB-BLOCK
> ⛔ **If one is still open it MOVES to another block first, and this file names where it went.**
> ⚠️ ⭐ **An orphaned sub-block is work that disappears silently** — and the archive is the last
> moment anybody would notice.

---

## 6 · ⛔ WHAT NEVER GOES IN AN ARCHIVE

| ⛔ Never | ⭐ Why |
|---|---|
| 🔴 **a credential** — ⚠️ **not even an expired one** | ⭐ what is written stays in the record |
| **the full conversation** | the session record holds it; ⛔ an archive is not a transcript |
| **code or diffs** | ⭐ **the archive describes, it does not duplicate** |
| 🔴 **a rewritten history** | ⚠️ ⭐ see below |

> ## 🔴 CORRECTING A BLOCK AFTER IT CLOSED TURNS A RECORD INTO A STORY.
> ⭐ **The block is moved AS IT CLOSED**, mistakes included. ⛔ **An archive that only holds
> correct decisions teaches that this kind of work is always done right** — which is the opposite
> of what it is for.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `ARC-NEV-001` | 🔴 **No credential in an archive** | 🔒 | ⛔ scan before the move |
| `ARC-NEV-002` | ⭐ **The block is not edited after closing** | 📖 | ⚠️ nothing verifies this |

---

## 7 · ⛔ NOTHING IS DELETED FROM AN ARCHIVE

⭐ **A closed block is consultable experience**, and the next time the same question appears the
answer is already written — ⭐ **including the parts that went wrong.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `ARC-DEL-001` | ⛔ **Nothing is removed from the archive** | 📖 | ⭐ not even something that turned out irrelevant |
| `ARC-DEL-002` | ⭐ **An archived block keeps its name** | 🔒 | ⛔ renaming breaks every pointer at once |

⚠️ **What looks irrelevant today is the record of why something was tried and dropped** — ⭐ and
without it, it gets tried again.

---

## 8 · ⭐ THE CLOSING TEST

> ## Would somebody who never saw this block understand — from these three files alone — what it was for, what it left behind, and what mistake not to repeat?

| Result | ⭐ Consequence |
|---|---|
| ✅ **yes** | the block is archived |
| 🔴 **no** | ⛔ **it does not close, however finished the work is** |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `ARC-TST-001` | ⭐ **The archive answers the three questions on its own** | 🟡 | ⛔ read only the three files |

⭐ **It is the same shape as the sufficiency test of an open block, pointed the other way:**
⚠️ **there it asks whether the work can be RESUMED; here whether it can be CONSULTED.**

⛔ **And an archive that fails it is worse than no archive:** ⭐ **it looks like the knowledge was
preserved.**

---

## 9 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **an empty "what was learned"** | ⛔ ⭐ **the only section worth keeping, and it says nothing** |
| **an empty "what was left out"** | ⚠️ the next reader inherits work nobody said was pending |
| ⭐ **a lesson written as an event** | ⛔ unusable — nobody can apply *"we fixed it"* |
| **an orphaned sub-block** | ⭐ **work that disappears silently** |
| **a shared document moved in** | ⚠️ a live reference becomes dead, ⛔ and the file still exists |
| ⭐ **the block corrected after closing** | ⛔ **a record becomes a story** |
| **renamed on archive** | every pointer breaks at once, and none says so |
| ⭐ **an archive that fails §8** | ⛔ **it looks like the knowledge was preserved** |

---

## 10 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ where the archive lives, how the period is written | ⭐ the owner of the instance |
| the required fields and their IDs | whoever maintains the engine, through a recorded decision |
| ⛔ archiving a block that fails §8 | **nobody** — ⭐ ⚠️ **the test has no override** |
| ⛔ deleting anything from the archive | **nobody** — ⭐ it is the record, not the workspace |

---

Related: `README.md` (⭐ the three document types) · `contract-block.md` (⭐ **§13 — the transition
that lands here, and §K whose content this consolidates**) · `contract-document.md` (⭐ the header
the two written files must carry) · `contract-adr.md` (⭐ where a repeated lesson graduates to) ·
`rule-shipping.md` (⭐ §11 — the session record, which is NOT this) ·
`../memory/principles/owner-3-validation.md` (⭐ who decides a block may close) ·
`../bin/check-archive` (what enforces the 🔒 rows).
