# CONTRACT · BLOCK

**Status:** current · **Type:** contract · **Updated:** 2026-09-01 · **Owner:** Ada Lovelace
**Applies to:** every `BLOCK.md` — open, blocked, closed or archived
**Enforcement:** 🔒 lock — `bin/check-block`
**Level:** 🌐 universal — ⭐ travels identical to every clone; a lower level may ADD or TIGHTEN, never loosen
**Verified by:** `bin/check-block` · `bin/probes/probe-block.py`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone
**Size:** ⭐ **this is a BASE file — it ships whole.** See `contract-document.md` §3: the ceiling
governs a document as it is *used*, and a standard that arrived pre-split would deliver two halves
of one criterion.

---

## 0 · WHAT THIS FILE IS

> ## ⭐ The contract that lets an agent identify, execute, recover, verify and close one unit of work — without depending on the conversation.

⚠️ **The failure it prevents:** work that exists only in a conversation. ⭐ **When the session
ends, the code is still on disk and the reasoning is not** — and the next session rebuilds what
was already decided, or worse, undoes it.

> ## ⭐ THE QUESTION THIS FILE ANSWERS IS NOT "DOES IT HAVE ALL ITS SECTIONS?"
> ⛔ **It is: can a new agent continue this work correctly?**

### ⭐ It absorbs the whole life of a block

| | Why it is here |
|---|---|
| **the shape** — the sections | what a block IS |
| **opening and closing** | ⭐ the same fields, at two different moments |
| **the blocked state** | ⚠️ a state, not a separate document |
| **the archive** | ⛔ what a block becomes — its last transition |

⭐ **One owner, one cycle of change.** Adding a section changes the shape, what closing checks,
and what gets archived — **in one edit.**

---

## 1 · ENFORCEMENT

| | Means |
|---|---|
| 🔒 **lock** | ⭐ a script refuses — ⚠️ and it has been seen to fail |
| 🟡 **prompt** | the agent asks before proceeding |
| 📖 **discipline** | ⛔ **nothing verifies this** |

**IDs are permanent.** `BLK-<area>-<nnn>` — ⛔ never renumbered, never reused.

---

## 2 · ⭐ AGENT OPERATING RULES — read this before touching anything

⛔ **These are not advice. They are the order of operations.**

| # | Rule | ⚠️ |
|---|---|---|
| 1 | **READ** — §A to §D before touching a file | ⭐ they are the authorisation to start |
| 2 | **VERIFY** — every path, id and standard resolves | ⛔ a broken one is a STOP, not a guess |
| 3 | ⭐ **SCOPE** — never modify anything outside §B `IN` | |
| 4 | **INHERIT** — system rules first, then the block's | ⚠️ ⛔ never restate them |
| 5 | ⭐ **DO NOT INFER AUTHORITY** — `DERIVED:` is reasoning, not a written rule | see §4 |
| 6 | **MEASURE** — ⛔ never trust a stale count | ⭐ re-measure before deciding |
| 7 | **UPDATE §E** immediately after a meaningful change | ⚠️ not at close |
| 8 | ⭐ **STOP** — see §3 | ⛔ the rule that prevents the rest |
| 9 | **CLOSE** only when §K and the sufficiency test pass | |

⭐ **Rule 4 has a direction:** rules ADD UP and TIGHTEN going down; ⛔ **a block never loosens what
it inherited.** The full model is in `rule-inheritance.md`.

---

## 3 · ⛔ STOP CONDITIONS — first-class, not a footnote

> ## ⭐ THE AGENT MUST STOP AND ASK WHEN:

| ⛔ Condition |
|---|
| a referenced file does not exist |
| a referenced block does not exist |
| ⭐ **a required standard cannot be found** |
| `IN` and `OUT` conflict |
| ⭐ **two authoritative sources conflict** |
| required evidence is missing |
| ⚠️ **a measurement cannot be reproduced** |
| the requested change exceeds the declared scope |
| ⛔ **the current state cannot be determined safely** |

⚠️ **The failure this prevents, and it is the shape of every expensive one:**

```
⛔ I cannot find the file → I guess where it is → I continue
   → I create another one → the architecture is broken
```

> ## ⭐ AN AGENT THAT INFERS SOUNDS EXACTLY AS CONFIDENT AS ONE THAT KNOWS.
> ⛔ **Stopping turns a silent loss into a visible question.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-STP-001` | ⭐ **Resolution is EXACT — no match means stop** | 📖 | ⛔ nothing verifies this |
| `BLK-STP-002` | **A stop reports exactly what is missing** | 📖 | ⚠️ *"something is wrong"* is not a report |

---

## 4 · ⭐ THE AUTHORITY ORDER — where each piece of information comes from

| Information | Source | Authority |
|---|---|---|
| **system rules** | the universal level | 🌐 **highest** |
| **project rules** | this installation's rules | 🏢 |
| **block boundaries** | §B | 📦 |
| **decisions** | §G | 📦 |
| ⭐ **measurements** | ⭐ **a tool's output** | ✅ **evidence** |
| ⛔ **the agent's reasoning** | `DERIVED:` | ⚠️ **inference — the weakest** |

> ## ⭐ ON CONFLICT, THE HIGHER AUTHORITY WINS — AND THE CONFLICT IS REPORTED.
> ⛔ **Never resolved silently.** ⚠️ A conflict resolved without saying so looks identical to no
> conflict at all.

⭐ **Inference is on the list, at the bottom, on purpose.** ⛔ **Leaving it off would not stop the
agent from reasoning — it would stop the agent from labelling it.**

---

## 5 · THE SHAPE

> ## ⭐ ONE BLOCK = ONE FILE. Sections A-K, in order.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-SHP-001` | ⭐ **One file per block** | 🔒 | ⛔ splitting a short file adds places to desynchronise |
| `BLK-SHP-002` | **Sections in order, A to K** | 🔒 | ⭐ order is what makes the top of the file the cheap part |
| `BLK-SHP-003` | **Within its ceiling** | 🔒 | the document contract decides the number |

⭐ **The letters are ADDRESSES, not positions.** ⛔ Something cites `§B` from another file — **the
letters are never renumbered**, and a new section is appended, never inserted.

### ⭐ Cheap to open, expensive to close

| Moment | Required | ⭐ |
|---|---|---|
| **OPEN** | A · B · C · D | ⭐ **about two minutes — the authorisation to start** |
| **while working** | E through J | the operational memory |
| **CLOSE** | everything + §11 | ⛔ the evidence of completion |

⛔ **If opening costs ten fields, work happens WITHOUT a block** — and then nothing is recorded.

---

## 6 · THE SECTIONS

> ## ⭐ MOVED — the eleven sections live in `contract-block-sections.md`.
> ⛔ Not summarised here: a summary of a contract is a second contract that
> drifts. ⚠️ Together the two halves ran past this type's ceiling, and
> `DOC-SIZ-001` says a file over its ceiling owes a SPLIT — never a raised
> limit, because the second raise is always easier than the first.

⭐ **The split is by TOPIC, not by size:** this file holds the LIFECYCLE — when a
block opens, what stops it, when it may close. The other holds the SHAPE — what
each of §A-K carries. ⭐ **Every id kept its number**, so no citation moved.

## 7 · ⭐ ACCEPTANCE — what "finished" means, decided BEFORE the work

```
## Acceptance
The block is complete when:
- ⬜ <an observable condition>
Evidence required:
- ⬜ <what will prove each one>
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-ACC-001` | ⭐ **Acceptance is written at OPEN, never at close** | 🟡 | ⛔ written at close, it describes what happened |
| `BLK-ACC-002` | ⭐ **Every condition is observable** | 🟡 | ⚠️ *"it works"* is not a condition |
| `BLK-ACC-003` | **Each condition names what will prove it** | 🟡 | ⭐ a condition with no evidence is a hope |

> ## ⛔ *"THE FEATURE WORKS."* — YES, BUT BY WHAT CRITERION?
> ⭐ **Written at close, acceptance is a description of what happened.** Written at open, it is a
> commitment — ⚠️ **and the difference is whether the block can fail.**

⭐ **This is the handover point of the whole system:** the success criterion comes from planning
(`../memory/principles/expertise/doc-planning.md` §2.5), is committed to here, and is proven at close
(`../memory/principles/expertise/val-functional.md`). ⛔ **A criterion never made measurable cannot be validated** — and the gap
only shows at closing time, when it is expensive.

---

## 8 · ⭐ EVIDENCE — every claim answers "what proves it?"

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-EVI-001` | ⭐ **A state claim carries what demonstrates it** | 🟡 | ⛔ `progress: 4/4` because someone believes it |
| `BLK-EVI-002` | ⭐ **Evidence is reproducible** | 🟡 | ⚠️ a number nobody can re-derive is not evidence |
| `BLK-EVI-003` | ⛔ **An unreproducible measurement is a §3 STOP** | 📖 | ⭐ not a rounding error |

⭐ **The four conditions of what counts as proof live in `../memory/principles/expertise/val-functional.md` §2.1** — ⛔ this
section does not restate them; **it says that a block's claims are subject to them.**

---

## 9 · ⛔ WHAT NEVER GOES IN THIS FILE

| ⛔ Not here | ✅ Goes in | ⭐ Why |
|---|---|---|
| chronologies, session logs | the block's own documents | ⚠️ **they grow without bound** |
| ⭐ **the CONTENT of a standard** | where that standard lives | ⭐ **point at it, never copy it** |
| code, diffs | the repository | the block describes, it does not duplicate |
| ⭐ **another block's state** | that block | ⛔ isolation |
| a credential | the secrets store | ⚠️ ⛔ **never, not even as an example** |

---

## 10 · OPENING

| # | Step | ⚠️ |
|---|---|---|
| 1 | ⭐ **Is this a NEW block, or an existing one?** | ⛔ a duplicate splits the record of one job |
| 2 | **Write A, B, C, D** and the acceptance | ⭐ about two minutes |
| 3 | **Declare it where blocks are listed** | ⚠️ an undeclared block is invisible to every check |

⭐ **Step 1 has a rule:** it is a NEW block when it would **close on a different day for a
different reason.** ⛔ Otherwise it is a sub-block of one that exists.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-OPN-001` | **A, B, C, D present at open** | 🔒 | the four sections exist |
| `BLK-OPN-002` | ⭐ **The block is declared where blocks are listed** | 🔒 | ⛔ otherwise nothing knows it exists |
| `BLK-OPN-003` | ⭐ **An index names no block that does not exist** | 🔒 | ⛔ the other direction of `BLK-OPN-002` — an entry outlives the folder it named |

---

## 11 · ⭐ THE SUFFICIENCY TEST — the one that decides

> ## Do sections A-E suffice to restart this work safely, with no other context?

**They must answer:** what is being built · ⛔ **what must not be touched** · what it depends on ·
under what criterion · where it stands · what blocks it.

| Result | ⭐ Consequence |
|---|---|
| ✅ **yes** | the block is well written |
| 🔴 **no** | ⛔ **the block does not close — even if the code works** |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-SUF-001` | ⭐ **A-E suffice to resume** | 🟡 | ⚠️ read only A-E and try to state the next action |

⭐ **This is the only test here a script cannot do, and it is the most important one.** ⚠️ **A
block that passes every mechanical check and fails this one is a block whose knowledge died with
the session that wrote it.**

> ⭐ **Without this test, writing to disk is accumulating, not owning the context.** It is what
> turns *"owning the context"* from a declaration into something measurable.

---

## 12 · THE `blocked` STATE

⭐ **`blocked` is a state, not a parking space.** It says: *this cannot proceed, and here is what
would unblock it.*

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-BLK-001` | ⭐ **A blocked block names WHAT would unblock it** | 🔒 | ⛔ *"waiting"* is not a blocker |
| `BLK-BLK-002` | ⭐ **Blocked past a declared period → it is asked about** | 🔒 | `bin/check-block`, against the ⬜ period below |

### ⬜ THE PERIOD, DECLARED

| ⬜ Declaration | Days | Why it is not the engine's |
|---|---|---|
| ⬜ stale period | 14 | ⛔ a fast project goes stale in a week; a slow one does not in a month |

⭐ **The same number answers two rules:** how long a block may sit untouched (`BLK-IDN-005`) and
how long it may stay blocked before somebody is asked (`BLK-BLK-002`). ⛔ **It lived hardcoded in
the validator** — a threshold nobody knew had been chosen.

> ## ⭐ THE QUESTION IS "IS THIS STILL CURRENT?", NEVER AN ACCUSATION.
> ⚠️ **A blocked block is not a failure.** What is a failure is a block blocked for a month that
> nobody ever asks about — it stops being blocked and starts being abandoned, and the two look
> identical from outside.

> ## ⭐ AT THE THRESHOLD: ASK, DO NOT ACCUSE
> ⚠️ **A block sitting blocked for weeks is not necessarily neglect.** ⭐ **The prompt asks whether
> it is still current**, and the answer is one of three: still waiting, unblock it, or close it.
> ⛔ **What is not allowed is silence.**

⭐ **A stale check that accuses gets ignored; one that asks gets answered** — and the difference is
measured in whether anyone ever responds.

---

## 13 · ⭐ THE STATE MACHINE — and `closed` is a transition, not a field

```
      ┌──────────┐   blocker found    ┌───────────┐
      │  ACTIVE  │ ─────────────────▶ │  BLOCKED  │
      └────┬─────┘ ◀───────────────── └───────────┘
           │            resolved
   acceptance passes
           │
   sufficiency passes
           │
      ┌────▼─────┐        ┌────────────┐
      │  CLOSED  │ ─────▶ │  ARCHIVED  │
      └──────────┘        └────────────┘
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-TRN-001` | ⭐ **`closed` requires acceptance AND sufficiency** | 🔒 | ⛔ neither one alone |
| `BLK-TRN-002` | ⭐ **`closed` is irreversible by default** | 📖 | ⚠️ reopening is an explicit act, recorded in §G |
| `BLK-ARC-001` | ⭐ **An archived block keeps its name** | 🔒 | ⛔ renaming breaks every pointer at once |
| `BLK-ARC-002` | **The archive carries a summary and what it affects** | 🔒 | both present |
| `BLK-ARC-003` | ⛔ **Nothing is deleted from the archive** | 📖 | ⭐ a closed block is consultable experience |

> ## ⭐ WHAT WAS LEARNED IS THE ONLY PART OF AN ARCHIVE THAT IS NOT A COPY
> ⚠️ Everything else already existed somewhere. **This is written once, while the knowledge is
> fresh — and it is the reason anyone opens an archive at all.**

---

## 14 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **no §B OUT** | ⚠️ the block grows until it cannot close |
| ⭐ **an OUT with no source** | ⛔ **an opinion enforced as a rule** |
| **a system rule restated in OUT** | ⭐ it goes stale, and nothing detects the divergence |
| **a dependent count from memory** | ⚠️ ⭐ **the wrong lane, chosen confidently** |
| **closed with an open sub-block** | ⛔ the task disappears — nobody knows it was dropped |
| **§K with no "not completed"** | the next reader assumes this work always succeeds |
| ⭐ **fails the sufficiency test** | ⛔ **the knowledge died with the session that wrote it** |
| **renamed on archive** | every pointer breaks at once, and none of them says so |

---

⚖️ split-with: `contract-block-sections.md`

## 15 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ the ceilings, and the sections this installation adds | ⭐ the owner — ⚠️ **appended, never inserted into A-K** |
| the rules and their IDs | whoever maintains the engine, through a recorded decision |
| ⛔ closing a block that fails §11 | **nobody** — ⭐ the sufficiency test has no override |
| ⛔ an `OUT` line with no source | **nobody** — ⚠️ ⭐ it is the field the whole contract rests on |

---

**Decided by:** `decisions/ADR-001` (⭐ why TWO levels) · `ADR-009` (why ONE file) · `ADR-010`
(⭐ why only four sections at open) — ⛔ **each names what is lost if it is reverted.**

Related: `contract-quality-verdict.md` (⭐ **the §K verdict, measured — `bin/grade-block` is
its layer 1**) · `README.md` (⭐ **the three document types**) · `contract-document.md` (⭐ the shape and
the ceilings this file obeys) · `contract-adr.md` (⭐ where a §G decision graduates to when it
outlives the block) · `contract-handoff.md` (⭐ what binds to a block, and the only sections a
specialist may append to) · `rule-inheritance.md` (⭐ **the three levels behind §B's two-levels
test**) · `rule-working-in-a-block.md` (⭐ the lane, isolation and friction this file records) ·
`../memory/principles/owner-3-validation.md` (⭐ **who decides a block may close**) ·
`../memory/principles/expertise/val-functional.md` (⭐ what counts as evidence in §8 and §K) ·
`../memory/principles/expertise/doc-planning.md` (⭐ where the acceptance criterion is born) ·
`../bin/check-block` (what enforces the 🔒 rows).
