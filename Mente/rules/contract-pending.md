# CONTRACT · PENDING

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every open item that outlives the session that found it
**Enforcement:** 🔒 lock — `bin/check-pending`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone

---

## 0 · WHAT THIS FILE IS

> ## ⭐ The shape of a debt that survives the session that found it — and how the file holding it rotates without losing anything.

⚠️ **The failure it prevents is measured, and it is not "we forgot something".** ⛔ **It is a
pending list that lies:**

| ⛔ Measured on a real list | |
|---|---|
| thousands of lines, ⭐ **closed sections mixed with open ones** | the file could not be read |
| ⭐ **items marked as debt that were already DONE** | ⛔ planned against, for weeks |
| a section marked closed, ⚠️ **with unticked boxes inside it** | closed by declaration, not by fact |

> ## ⭐ A PENDING ITEM THAT LIES ABOUT ITS STATE IS WORSE THAN NOT HAVING IT.
> ⛔ **Because work gets planned on top of it.**

### ⭐ THE SIZE IS SUPPOSED TO BE A METRIC

⭐ **If the list grows, the debt grew.** ⛔ **A list mixing what is resolved with what is live says
nothing at all** — and then nobody looks at it, which is the state it never recovers from.

### ⭐ It absorbs two things that used to be separate

| | Why it is here |
|---|---|
| **the shape of an item** | what a debt must answer |
| ⭐ **the rotation of the file** | ⚠️ **the same mechanism** — one describes the object, the other its life |

---

## 1 · ENFORCEMENT

| | Means |
|---|---|
| 🔒 **lock** | ⭐ a script refuses — ⚠️ and it has been seen to fail |
| 🟡 **prompt** | the agent asks before proceeding |
| 📖 **discipline** | ⛔ **nothing verifies this** |

**IDs are permanent.** `PND-<area>-<nnn>` — ⛔ never renumbered, never reused.

---

## 2 · THE SHAPE OF ONE ITEM

```markdown
### <id> · <one-line title>

- Priority:   🔴 urgent | 🟠 medium | 🟢 no rush
- State:      open | paused | closed | dropped
- Created:    <date> · Updated: <date> · Closed: <date> | —
- Carried from: <the file it arrived from> | — (born here)
- Reference files: <paths> — ⚠️ a starting point, ⛔ NOT the full list
- Plan:       <its plan> | — (small enough not to need one)
- Depends on: <another block> | —

Description. Everything needed to resume it without asking: what fails, what
was measured, what was decided and what was NOT.
```

> ## ⬜ THE FIELD NAMES ARE YOURS — the fields are not
> ⭐ **The engine fixes WHAT an item must answer, never what the labels are
> called.** ⚠️ An installation writing them in another language is not in
> violation — ⛔ **one that omits a field is.**
>
> ⬜ **Declare your label for each field** in the project rules:
> `pending_field <field> = <regex>` — ⭐ and the same for the STATE VALUES
> and the block heading: `pending_state <state> = <regex>`

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `PND-FLD-001` | ⭐ **Every field present** | 🔒 | ⛔ a missing one is not brevity, it is an unanswered question |
| `PND-FLD-002` | ⭐ **The three dates** — created, updated, closed | 🔒 | ⚠️ see below |
| `PND-FLD-003` | ⭐ **`Carried from` names the file it arrived from** | 🔒 | ⛔ §5 |
| `PND-FLD-004` | ⭐ **The description resumes the work without asking** | 🟡 | ⚠️ if the reader must reconstruct context, it is incomplete |

### ⭐ FIELD BY FIELD — and what each one prevents

| Field | ⭐ The rule |
|---|---|
| **Priority** | ⭐ **the agent proposes it; the owner corrects it.** ⛔ **It NEVER justifies skipping an item** — a block is worked whole, and the colour only helps reading |
| **State** | ⭐ **`paused` ≠ `closed`.** ⚠️ **Paused keeps rotating**; closed stays in the period it died |
| ⭐ **The three dates** | ⛔ **without a closing date, an item is not closed** however firmly the prose says so |
| ⭐ **Carried from** | ⚠️ **without it, an item alive for six months reads exactly like one from yesterday** |
| **Reference files** | ⛔ **not law** — ⭐ nobody knows how big the problem is yet; it is where to start looking |
| **Plan** | ⭐ the large ones carry it; ⛔ **the small ones must not point at an invented one** |
| **Depends on** | ⭐ **both are read before building** — ⚠️ a partial picture is how the neighbouring thing breaks |

> ## ⭐ PRIORITY IS FOR READING, NOT FOR SKIPPING
> ⛔ **A 🟢 is not permission to leave it out.** ⚠️ **A block is worked whole**, and a colour used
> as a filter turns the list into a list of the urgent — which is where the rest goes to die.

---

## 3 · ⭐ EVERY ITEM LIVES IN A BLOCK

⛔ **A loose pending item does not exist.** ⭐ **It belongs to a block of pending items**, and the
block is the unit of reading.

### To open a block, three things

| # | Requirement | ⭐ Why |
|---|---|---|
| 1 | **an analysis of what is going to be done** | ⛔ a block with no analysis is a folder with a name |
| 2 | ⭐ **at least two items** | ⚠️ one alone is not a theme, it is an item |
| 3 | **a plan for the block as a whole** | ⭐ what happens to it entire, and in what order |

⭐ **The exception to rule 2: a genuinely NEW theme.** ⚠️ If nothing knows where to classify it,
**one is enough** — ⛔ forcing a second invents work to satisfy a threshold.

### ⭐ THE DECLARED DRAWER

⭐ **What fits in no block goes in a block declared for exactly that.** ⛔ **It is not a dump: it
is the honest statement of *"this exists and I do not yet know what it belongs to".***

> ## ⚠️ AND THE ORDER MATTERS
> ⛔ **If an item does not satisfy this contract, INVESTIGATE FIRST — something is wrong.**
> ⭐ **Only once you confirm there is no defect does it go to the drawer.** ⚠️ Never the reverse:
> **the drawer used first is how a defect becomes an entry nobody reads.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `PND-BLK-001` | ⭐ **Every item belongs to a block** | 🔒 | ⛔ a loose item has no subject |
| `PND-BLK-002` | **A block declares its analysis and its plan** | 🔒 | ⚠️ ⭐ a named folder is not a block |
| `PND-BLK-003` | ⭐ **Two items, or a genuinely new theme** | 🟡 | ⛔ never a second one invented to reach the number |

---

## 4 · ⭐ THE FOUR VERBS

| Verb | What it does | ⭐ Rotates? |
|---|---|---|
| **pause** | ⭐ still alive, not worked now | ✅ **yes** |
| **close** | resolved, ⭐ **with its date and its evidence** | ⛔ no — it stays where it died |
| **finish** | ⭐ the same as close | ⛔ no |
| **drop** | ⚠️ **it stopped making sense — and WHY is written** | ⛔ no |

> ## ⛔ DROPPING WITHOUT A WRITTEN REASON IS FORBIDDEN
> ⭐ **An item that disappears with no explanation is reborn in three months as a new finding** —
> ⚠️ and then it is investigated again, from zero.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `PND-VRB-001` | ⭐ **`closed` requires a closing date** | 🔒 | ⛔ prose is not a state |
| `PND-VRB-002` | ⭐ **`dropped` requires a written reason** | 🔒 | ⚠️ ⭐ see above |
| `PND-VRB-003` | ⛔ **`paused` is not `closed`** | 🔒 | ⭐ one rotates, the other does not |

---

## 5 · ⭐ ROTATION — the FILE rotates, never the item

> ## ⭐ AN ITEM FOUND IN ONE PERIOD MAY STILL BE OPEN A YEAR LATER. What rotates is the FILE that holds it.

```
<period N>  ──rotates──▶  <period N+1>
     │                          │
     │ closed items STAY here   │ open and paused items are
     │ with their date          │ REWRITTEN in full
```

| What happens to… | ⭐ Destination |
|---|---|
| **open** or **paused** | ✅ **rewritten in full** in the new period |
| **closed** / **finished** | ⛔ stays where it died, with its date |
| **dropped** | ⛔ stays, ⭐ with its reason |

⭐ **The periodic file IS the metric:** ⛔ **if the number does not go down, the debt did not go
down.**

### ⭐ THEY ARE REWRITTEN, NOT POINTED AT

> ## ⛔ ROTATING WITH POINTERS IS FORBIDDEN.
> ⭐ **Every period's file is self-sufficient: it reads alone, without opening the previous ones.**

⚠️ **And this is not redundancy for its own sake.** ⛔ **A broken pointer makes an item invisible,
and an invisible item is neither planned nor closed — it disappears.**

> ⭐ **Duplication costs bytes. Loss costs work nobody knows is missing.**

⚠️ **The price, accepted deliberately:** ⭐ **an item is edited in the LIVE period.** ⛔ **Previous
periods are frozen history and are not corrected** — the trail must show what was known then.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `PND-ROT-001` | ⭐ **Open and paused items are rewritten in full** | 🔒 | ⛔ never a pointer to a previous period |
| `PND-ROT-002` | ⭐ **A closed item does not travel** | 🔒 | ⚠️ it stays in the period it died |
| `PND-ROT-003` | ⛔ **A previous period is never edited** | 📖 | ⭐ frozen history |

### ⭐ `Carried from` — why it is a function, not decoration

⚠️ **Without it, an item alive for six months reads exactly like one from yesterday.**

> ## ⭐ AGE IS INFORMATION.
> ⚠️ **An item that has rotated five times without closing is saying something** — ⛔ usually that
> it was never a real priority, or that it lacks a plan.

---

## 6 · ⭐ THE FIRST ROTATION — converting an existing list

⚠️ **A list that grew unmanaged does not rotate. It gets converted, once.**

| # | Step | ⛔ What goes wrong without it |
|---|---|---|
| 1 | **Separate closed from open** | ⚠️ ⭐ **and do not trust the markers**: a section marked closed had unticked boxes inside |
| 2 | 🔴 **Verify each item AGAINST REALITY before carrying it** | ⛔ see below |
| 3 | **Group what is open into blocks** | what fits nowhere goes to the declared drawer |
| 4 | ⭐ **The old file becomes history and stops receiving writes** | ⚠️ two live lists is how the next divergence starts |

> ## 🔴 CARRYING WITHOUT VERIFYING PROPAGATES FALSE DEBT
> ⚠️ **Measured: of nine items carried forward, two were already DONE.** ⛔ **They had been counted
> as debt, and planned against, for weeks.**
>
> ⭐ **The check is not "does the item still read as true?" — it is "does the thing it describes
> still exist?"**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `PND-CNV-001` | ⭐ **Each item is verified against reality before carrying** | 📖 | ⛔ nothing verifies this |
| `PND-CNV-002` | ⭐ **Only one list receives writes** | 🔒 | ⚠️ two live lists diverge |

---

## 7 · ⭐ HOW THEY ARE SHOWN

⭐ **With the shape of a delivery block, applied to debt:**

```
📋 PENDING · <period>          🔴 N urgent · 🟠 N medium · 🟢 N no rush

## BLOCK · <name>              N open · N closed this period
  🔴 <id> · <title>            carried from <period> · plan: yes/no
  🟠 <id> · <title>            born here

### ✅ CLOSED THIS PERIOD
### 🙋 NEEDS YOUR DECISION     — or the word "nothing"
### 👉 WHAT IS NEXT            — the ONE next action
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `PND-SHW-001` | ⛔ **Never a flat list** | 📖 | ⭐ the block is the unit of reading |
| `PND-SHW-002` | ⭐ **The decision field is never omitted** | 📖 | ⚠️ silence cannot be told from forgetting |

⭐ **`PND-SHW-001` matters because a flat list loses the subject:** ⛔ **an item without its block
does not say what it is about**, and a reader scanning fifty of them retains none.

---

## 8 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **closed and open mixed** | ⛔ ⭐ **the size stops being a metric, and nobody reads the list again** |
| ⭐ **carried without verifying** | ⛔ **false debt, planned against** |
| **no closing date** | ⚠️ closed by declaration, not by fact |
| ⭐ **dropped with no reason** | ⛔ **reborn in three months as a new finding** |
| **rotated with a pointer** | ⭐ one broken link and the item is invisible — ⛔ **and invisible is gone** |
| ⭐ **no `carried from`** | ⚠️ **six months old reads like yesterday** |
| **priority used as a filter** | ⛔ the list becomes a list of the urgent, ⭐ and the rest dies there |
| **a previous period edited** | ⚠️ the trail stops showing what was known then |
| **a loose item** | ⭐ nobody knows what it is about |

---

## 9 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ the rotation period, the block names, where the list lives | ⭐ the owner of the instance |
| the fields, the four verbs, the rotation mechanism | whoever maintains the engine, through a recorded decision |
| ⛔ dropping an item with no written reason | **nobody** — ⭐ it comes back as a new finding |
| ⛔ carrying an item without verifying it | **nobody** — ⚠️ ⭐ that is how false debt spreads |

---

Related: `README.md` (⭐ the three document types) · `contract-block.md` (⭐ **the shape this
imitates: cheap to open, expensive to close** — and where an item graduates when it becomes work) ·
`contract-archive.md` (⭐ where debt handed over at closing goes) · `contract-document.md` ·
`../memory/principles/contract-delivery.md` (⭐ the delivery shape §7 applies) ·
`../memory/principles/expertise/val-functional.md` (⭐ what a plan must say about how it verifies) ·
`../bin/check-pending` (what enforces the 🔒 rows).
