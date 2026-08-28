# EXPERTISE · VAL-INTEGRATION

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Branch of:** `../owner-3-validation.md` — functional validation
**Level:** ⚖️ criterion · ⭐ **the engine's base standard**, extensible by the installation
**Scope:** ⚠️ ENGINE document — §0 to §2 and §4 to §7 ship identical; §3 is yours.

---

## 0 · WHAT THIS FILE IS

> ## ⭐ The criterion for the SEAMS between pieces — where the expensive failures live.

⚠️ **Every piece can pass its own test and the chain still be broken.** That is the failure this
discipline exists to catch, and no amount of testing the pieces will find it.

| | Asks |
|---|---|
| `val-functional.md` | ⭐ **does this piece work?** |
| **this file** | ⭐ **does the chain still work when every piece does?** |

### Two things live here, and they must never be confused

| | |
|---|---|
| **§2 · BASE STANDARD** | the engine's criterion. Ships filled in. ⛔ Do not edit it in an instance |
| **⬜ §3 · YOURS** | what this installation adds. ⭐ **Extend here, never by rewriting §2** |

---

## 1 · ⭐ WHAT A SEAM IS

⛔ **Without a definition, "I checked the seams" is not verifiable** — there is nothing to count
it against, and every reader draws the boundary somewhere else.

> ## ⭐ A SEAM is any boundary where one piece depends on another.

| A seam exists wherever a piece… | Example of the boundary |
|---|---|
| **consumes data another produced** | a payload, a record, a file |
| **calls another's interface** | ⭐ a function across a module, a request across a process |
| **depends on another's configuration** | ⚠️ a shared setting, an environment value |
| **transforms data for another** | ⭐ the transform itself is the seam, not either side |
| **authenticates or authorises against another** | ⚠️ identity crossing a boundary |
| **depends on something outside the system** | ⛔ an external service, a third party |

⭐ **Seams are enumerated before they are validated.** A change touching three seams is three
validations, not one — and §5's matrix is filled **once per seam**.

⚠️ **The transform row is the one that gets missed.** People look at the two pieces and skip the
translation between them, ⭐ **which is precisely where a mismatched assumption lives.**

---

## 2 · THE BASE STANDARD

### 2.1 · Before touching a piece others consume

⛔ **Four conditions. All four.**

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `VI-ARC-001` | ⭐ **Every consumer known and MEASURED, never remembered** | 🔴 | ⛔ a list from memory is a guess — ⚠️ see §2.2 |
| `VI-ARC-002` | **Deploy order: senders first, strict receiver last** | 🔴 | ⭐ a strict receiver first breaks everything not yet sending the field |
| `VI-ARC-003` | **Run the WHOLE flow, not just the piece** | 🔴 | a unit test of the piece cannot answer this |
| `VI-ARC-004` | ⭐ **Reversible without touching the consumers** | 🟠 | ⛔ see below |

⭐ **`VI-ARC-004` is the one that gets skipped, and it is what turns a bad change into an expensive
one.** If undoing it needs a coordinated edit in every dependent, **it is not one change — it is
N changes**, and you accepted that blast radius without measuring it.

⚠️ **A dependent is something that IMPORTS the piece, never something that merely mentions it.**
⭐ The two counts differ by a lot, and the mention count is the one a naive search returns.

### 2.2 · ⭐ WHEN THE CONSUMERS CANNOT BE COUNTED

⛔ **A search returning zero consumers does not mean there are none.**

| The consumer that stays invisible | ⚠️ Why the search misses it |
|---|---|
| **one in another repository** | ⭐ it is not in the tree you searched |
| **a dynamic invocation** | ⛔ the name is assembled at run time — no literal to find |
| **something outside the system entirely** | ⚠️ nobody on this side knows it exists |
| **a call through an alias or a re-export** | ⭐ the name at the call site is not the name you searched |

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `VI-ARC-005` | ⭐ **Zero found is NOT_MEASURED, not "no dependents"** | 🔴 | ⛔ can you state where a consumer could hide? |
| `VI-ARC-006` | **State which surfaces the search covered** | 🟠 | ⭐ and which it could not |

> ## ⛔ ONE SEARCH IS NEVER PROOF OF ABSENCE
> ⭐ A single pattern never covers every way a thing can be invoked. **Absence of a match is
> absence of evidence** — which `val-functional.md` §1 already names: ⬜ **NOT_MEASURED**.

### 2.3 · What crosses the seam — and what may be assumed

> ## ⛔ NOTHING. A PIECE ASSUMES NOTHING AND VALIDATES WHAT IT RECEIVES.

⚠️ **Not even when it comes from a piece you own.** ⭐ **Trust does not cross a seam:** the
receiver checks shape and content, every time.

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `VI-DAT-001` | ⭐ **The receiver validates what crosses** | 🔴 | ⛔ *"it comes from our own code"* is not an answer |
| `VI-DAT-002` | ⛔ **Identity is verified, never assumed** | 🔴 | ⭐ see below |
| `VI-DAT-003` | **State what the receiver validates and what it delegates** | 🟠 | for each seam, both halves |

⭐ **On identity:** an identifier arriving in a request does not prove who is making it.
**Authorisation reads the verified session, never an argument** — otherwise anyone holding a
credential can act as someone else.

⚠️ **The distinction that keeps this from becoming paranoia — validating is not re-deriving.**

| | |
|---|---|
| guaranteed by a constraint at the source | ⭐ **not re-checked** — the guarantee lives where it is enforced |
| crossing a seam with no constraint behind it | ⛔ **always validated** |

### 2.4 · One concept, one name across the whole flow

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `VI-NAM-001` | ⭐ **A concept keeps one name end to end** | 🟠 | ⛔ two names for one thing, and someone will confuse them |
| `VI-NAM-002` | **The OWNER of the data sets the name** | 🟠 | consumers adopt it |
| `VI-NAM-003` | ⭐ **If two names are unavoidable, DECLARE the mapping** | 🔴 | ⚠️ in ONE place, never in each consumer |
| `VI-NAM-004` | ⛔ **No generic name at a boundary** | 🔴 | see below |

⭐ **`VI-NAM-004` is not about length.** A short name is fine when the structure justifies it. **A
generic one at a boundary is rejected because it says nothing about what distinguishes the thing**
— and forces the reader to open the other side to find out what is arriving.

### 2.5 · ⭐ What happens when the other side fails — the core

> ## ⛔ FAIL LOUDLY. NEVER SILENTLY.

⚠️ **A silent fallback is not resilience. It is a bug with a delay fuse** — it does not prevent
the failure, it **postpones and disguises** it, and the divergence it hides grows the whole time.

| # | Requirement | Sev |
|---|---|---|
| 1 | ⭐ **Fail visibly** — ⛔ nothing that swallows an error, no fallback that hides a divergence | 🔴 |
| 2 | **Declare the failure mode in the contract** | 🔴 |
| 3 | **Degrade with an EXPLICIT notice** — ⛔ never pretend everything is fine | 🔴 |
| 4 | ⭐ **Stop the whole flow** — when the rule below says so | 🔴 |

⭐ **Requirement 2 is what makes the other three possible.** Without a declared failure mode,
**every consumer invents its own reaction** — and they will not agree.

> ## ⭐ WHAT DECIDES BETWEEN 3 AND 4: is DATA involved?
>
> | If the failure can… | Then |
> |---|---|
> | ⛔ **corrupt or lose user data** | 🔴 **STOP** |
> | only degrade a function — a read, an ornament | ⭐ **continue, with the notice** |
>
> ⭐ **Availability is recoverable; a corrupted record is not.** The two options never contradict
> each other, because **the data decides, not the mood.**

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `VI-CON-001` | ⭐ **Every seam declares its failure mode** | 🔴 | which of the four, and why |
| `VI-CON-002` | **And which side of the line it falls on** | 🔴 | ⛔ data or function — a seam that does not say has not answered this |

### 2.6 · ⭐ Should this connection exist at all?

⛔ **Ask this BEFORE writing a test for it.** ⭐ Testing a connection that should not exist means
paying maintenance forever for something whose correct fix is deletion.

| # | The connection… | ⭐ Why it goes |
|---|---|---|
| 1 | **exists "just in case"** | ⛔ a seam with no real consumer is a free failure surface |
| 2 | **is not backed by the plan** | ⭐ if the plan does not justify it, it is wrong — even working |
| 3 | **duplicates a path that already exists** | ⚠️ two paths to the same data diverge |
| 4 | ⭐ **crosses an ownership boundary without needing to** | ⛔ convenience is not a reason to couple two owners |

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `VI-NEC-001` | ⭐ **Name the real consumer and the plan that justifies it** | 🟠 | ⛔ neither one → the finding is to delete, not to test |

### 2.7 · Duplication across a seam — ownership decides, not shape

> ## ⭐ THE TEST IS WHO OWNS THE RULE — not how similar the code looks.

| Both sides implement a rule owned by… | Then |
|---|---|
| **the SAME owner** | ⭐ duplication — unify it, and fix every copy, never one |
| ⛔ **DIFFERENT owners** | ⭐ **legitimate coincidence — keep them apart**, however alike they look |

⚠️ **Why ownership and not shape:** two pieces can look identical today and diverge tomorrow,
because nothing says they must evolve together. ⭐ **Unifying by resemblance couples two rules that
were never the same rule** — and then one owner's change silently alters the other's behaviour.

⭐ **And record the decision to keep them apart**, so the next reader does not "fix" it.

---

## 3 · ⬜ THIS INSTALLATION'S CRITERIA

⬜ **Add yours here**, using the model of §2 and ⭐ **your own prefix** — for example `VI-OWN-001`.

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| ⬜ … | ⬜ … | ⬜ … | ⬜ … |

> ⛔ **Do not let an AI write this section.** ⭐ **The AI asks, you answer with real cases, the AI
> structures.** Never the reverse.

**The questions that elicit it — answer with cases, not principles:**

1. What do you require before believing two pieces actually talk to each other?
2. ⭐ **How do you know a change will not break something downstream?**
3. What must be tested with real data and never with a substitute?
4. Which integration failure has cost you most, and what would have caught it?
5. When one piece fails, what should the piece next to it do?
6. ⭐ **What must be verified in the real environment, and never locally?**

---

## 4 · ⭐ THE REAL ENVIRONMENT IS NOT YOUR ENVIRONMENT

⛔ **Testing where you build is not testing where it runs** — ⚠️ and this is the sign that costs
most, because everything looks correct while you are watching it.

| ID | Criterion | Sev | What to name |
|---|---|---|---|
| `VI-ENV-001` | ⭐ **Validated against the environment where it will actually be consumed** | 🔴 | which one, explicitly |
| `VI-ENV-002` | **Configuration comes from the same source production uses** | 🔴 | ⭐ where each value is read from |
| `VI-ENV-003` | **The deployed version is the one under test** | 🟠 | ⛔ not the working copy |
| `VI-ENV-004` | ⭐ **External dependencies are the real ones** | 🔴 | ⚠️ a substitute proves your side only |
| `VI-ENV-005` | **A neighbour was restarted and it reconnected** | 🔴 | ⭐ from configuration, not from a hardcoded address |

⭐ **`VI-ENV-005` is the reconnection test**, and it catches what nothing else does: a piece that
works right now **only because it never had to find its neighbour again.**

⛔ **Never assume two environments are equivalent.** ⚠️ **A difference you did not look for is the
one that will be there.**

---

## 5 · ⭐ THE EVIDENCE MATRIX — one per seam

⛔ **Fill it per seam, never once for the change.** ⭐ Otherwise a single gap disappears among
several greens.

| Evidence | Required |
|---|---|
| consumers measured — ⭐ **with the surfaces the search covered** | ✅ |
| the contract identified, both sides | ✅ |
| ⭐ **real data, not a substitute** | ✅ |
| the whole flow run end to end | ✅ |
| ⛔ **the failure path exercised** | ✅ |
| the reconnection test | ✅ |
| ⭐ **the real environment** | ✅ |
| reversibility demonstrated | ✅ |

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `VI-EVI-001` | ⭐ **A single unmet row is the verdict** | 🔴 | ⛔ the others being green changes nothing |
| `VI-EVI-002` | **An unmet row names its next action** | 🟠 | ⭐ what exactly has to be run |

⭐ **The failure-path row is the one most often left empty**, because it is the only one that
requires deliberately breaking something. ⚠️ **A seam whose failure path was never exercised is a
seam whose failure mode is a guess.**

---

## 6 · ⛔ NEVER — no exceptions

| # | Never | ⭐ Why |
|---|---|---|
| 1 | **A fallback that HIDES a divergence** | ⚠️ it postpones and disguises — a bug with a delay fuse |
| 2 | ⛔ **Change the receiver before the senders** | ⭐ a strict receiver first breaks everything not yet sending |
| 3 | **Call a seam good without REAL DATA** | ⭐ a substitute returns what you expect; real data returns what exists |
| 4 | ⛔ **Remove a piece without measuring who imports it** | ⚠️ importers, never mentions — §2.2 |
| 5 | ⭐ **A default that points at something with an owner** | ⛔ a default is a neutral slot, never a reserved name |
| 6 | ⛔ **Treat a test from your environment as a test of production** | ⭐ §4 |

### ⭐ FOUR SIGNS IT WAS ONLY TESTED IN ISOLATION — any one is enough

| # | Sign | Why it disqualifies |
|---|---|---|
| 1 | ⭐ **verified from your environment, not the real one** | ⚠️ the costliest and least obvious — everything looks right while you watch |
| 2 | **substitutes only, no real data** | ⭐ it proves your side of the seam, never the wire |
| 3 | **nobody restarted anything** | the reconnection test never ran |
| 4 | **the evidence says "it seems to work"** | ⛔ affirmative verification or nothing |

⛔ **These are not scored.** Any one present means the integration was not verified — 🔴 however
green the unit tests are.

---

## 7 · WHEN TWO AUTHORITIES DISAGREE AT A SEAM

⭐ **Order, strongest first:**

| # | Authority |
|---|---|
| 1 | ⭐ **data integrity and security** — ⛔ never overridden |
| 2 | **a guarantee enforced at the source** |
| 3 | **the declared contract of the seam** |
| 4 | **the owner of the rule** |
| 5 | ⛔ **an implementation detail** — ⭐ never wins against anything above |

⚠️ **A precedent is not on this list.** ⭐ **A past case explains why a rule exists; it does not
outrank the rule** — and a precedent cited against a current criterion is an argument, not an
authority.

---

## 8 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ §3 — this installation's criteria | ⭐ the owner of the instance |
| §1, §2, §4-§7 — the base standard | whoever maintains the engine, through a recorded decision |
| ⛔ lowering a 🔴 to 🟠 locally | **nobody** — ⚠️ log the friction and propose it |

---

Related: `README.md` (⭐ **the parent — what a discipline is**) · `val-functional.md` (its sibling
— ⭐ whether a piece works, and the three verdicts this file uses) · `../owner-3-validation.md`
(⭐ what consumes this, and decides closure) · `dev-backend.md` (the seams seen from the side that
builds them) · `dev-database.md` (⭐ where a guarantee is enforced, which §2.3 delegates to).
