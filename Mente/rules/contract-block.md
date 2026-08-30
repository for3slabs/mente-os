# CONTRACT · BLOCK

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
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

| § | Section | Required | Ceiling | Tier |
|---|---|---|---|---|
| **A** | `Identity` | 🔴 open | ⬜ declared | 1 |
| **B** | ⭐ `Scope` — IN / OUT / Invariants | 🔴 open | ⬜ declared | 1 |
| **C** | `Connections` | 🔴 open | ⬜ declared | 1 |
| **D** | `Required standards` | 🔴 open | ⬜ declared | 1 |
| **E** | `State` | 🟡 working | ⭐ **strict** | 1 |
| **F** | `Sub-blocks` | 🟡 working | ⬜ declared | 2 |
| **G** | `Decisions` | 🟡 working | — | 2 |
| **H** | `Friction log` | 🟡 working | — | 2 |
| **I** | `Checkpoints` | 🟡 working | — | 3 |
| **J** | `Context` | 🟡 working | ⭐ **strict** | 3 |
| **K** | ⭐ `Closing` | 🔴 close | — | — |

⭐ **Tiers are the ORDER inside the file, not separate files.** Tier 1 is what a reader needs to
resume safely. ⛔ **A reader who must open three files to know where the work stands opens none.**

> ## ⭐ WHEN A CEILING IS CONSULTED — and it is NOT while writing
> ⭐ **During the work the ceiling is not consulted: you write what the contract demands.** It is
> reviewed **at close**, when you know what was essential and what was noise.
>
> ⛔ **Checking it mid-work changes WHAT gets written**, which is the opposite of the point: the
> ceiling exists to force curation over what is already written, ⚠️ **never to censor while
> writing.**

### ⬜ THE CEILINGS, DECLARED

⛔ **Three rules in this contract say "within its ceiling" and nothing said what the ceiling was.**
A limit named but never given a number is not a limit — it is a word.

| ⬜ Section | Lines | Why this one is bounded |
|---|---|---|
| ⬜ A `Identity` | 0 | ⛔ `0` = NOT MEASURED, and the rule says so |
| ⬜ B `Scope` | 0 | ⬜ declare it |
| ⬜ C `Connections` | 0 | ⬜ declare it |
| ⬜ D `Required standards` | 0 | ⬜ declare it |
| ⬜ E `State` | 0 | ⭐ the one section always read first — it stays short or it stops being read |
| ⬜ F `Sub-blocks` | 0 | ⬜ declare it |
| ⬜ J `Context` | 0 | ⚠️ a context that grows with every message is a transcript, not a context |

⭐ **`0` means NOT MEASURED — ⛔ it does not mean unlimited.** An engine that picked a number would
be sizing somebody else's work, and a number invented on the spot becomes the standard by accident.

> ## ⛔ A CEILING NAMED WITHOUT A NUMBER IS THE SAME AS NO CEILING — EXCEPT IT LOOKS LIKE ONE.
> ⚠️ **And that is worse:** a reader believes the section is bounded and never checks.

⚠️ **And a measured warning about sizing them:** ⭐ **a validator counts every non-empty line, so
the headings themselves consume part of the ceiling.** ⛔ **A block omitting an `OUT` limit for
lack of room is worse than a §B a few lines over: an OUT that is not written is a boundary that
does not exist.**

⬜ **Each installation declares its own numbers** in `PROJECT-RULES.md`. ⭐ **What the engine fixes
is that they are declared and measured, not what they are.**

---

### A · Identity — 🔴 to open

```
id: <unique>
type: code | docs | infra | data
intent: one sentence — what this block is for
status: active | blocked | closed
lane: direct | task | full-block
owner: <who>
created: <date> · updated: <date>
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-IDN-001` | ⭐ **`id` globally unique — resolution is EXACT** | 🔒 | ⛔ no match → §3 STOP |
| `BLK-IDN-002` | ⭐ **`type` present** — it decides which metrics apply | 🔒 | see below |
| `BLK-IDN-003` | **`intent` is one sentence** | 🔒 | ⚠️ if you cannot write it, you do not know what you are doing yet |
| `BLK-IDN-004` | **`status` and `lane` each one of their set** | 🔒 | ⛔ free text means nothing can read it |
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
> ⚠️ silence would let a block look like it passed a check it never ran.
>
> ⭐ **The type does not lower the bar, it changes the ruler.**

⚠️ **A block genuinely half one type and half another is TWO blocks** — ⭐ they would not close on
the same day, for the same reason.

---

### B · Scope — 🔴 to open · ⭐ **the critical one**

```
## ✅ IN          what this block may touch
## ⛔ OUT         what is out of bounds, with its source
## 🔒 INVARIANTS  what must remain TRUE after your changes
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-SCP-001` | ⭐ **`IN` and `OUT` both present and non-empty** | 🔒 | ⛔ an empty OUT is a block with no boundary |
| `BLK-SCP-002` | ⭐ **Every `OUT` line states WHERE it comes from** | 🔒 | see the marker table |
| `BLK-SCP-003` | ⛔ **A system-wide rule is never restated as an `OUT`** | 🟡 | ⭐ see the two-levels test |
| `BLK-SCP-004` | **Scope is not widened silently** | 🟡 | ⭐ a change to scope is a decision, and decisions go in §G |

⭐ **§B is the only section that can say NO.** Everything else describes the work; this bounds it.
⚠️ **A block with no OUT grows until it cannot close.**

#### ⭐ TWO LEVELS — the block does NOT own system-wide rules

| Level | Where it lives | Applies |
|---|---|---|
| 🌐 **system-wide** | the universal and project levels | ⭐ **always** — with or without a block |
| 📦 **block-specific** | §B `OUT` | only while this block is open |

> ## ⭐ THE TEST: would this limit still hold if this block did not exist?
> **Yes → system-wide.** ⛔ Do not repeat it in `OUT` — **inherit it.**
> **No → block-specific.** It belongs in `OUT`.

⚠️ **Measured on a real block: of 4 limits written in `OUT`, 2 were system-wide** and only 2 were
actually that block's.

> ## ⛔ WHY REPEATING IS HARMFUL, NOT MERELY REDUNDANT
> ⭐ **If the system rule changes, every block that copied it now carries a stale version — and
> nothing detects the divergence.** ⚠️ It is the same failure as a table living in two documents.

⭐ **A block MAY list inherited rules under a clearly separate heading** — *"system-wide rules that
also apply"* — ⛔ **as a reading aid, never as its own `OUT`.**

#### ⭐ EVERY `OUT` LINE STATES ITS SOURCE — and how strongly

| Marker | Means | ⭐ |
|---|---|---|
| **a file path + line** | a written rule — ⭐ cite its source | |
| **a technical lock** | ⭐ **enforced by the tooling** | the strongest kind |
| ⭐ **`DERIVED:`** | ⭐ **the agent's reasoning from a rule — say so explicitly** | ⚠️ see below |
| **nothing** | 🔴 **not allowed** | ⛔ **an unsourced limit is an opinion** |

⭐ **`DERIVED:` exists because of a real slip:** an `OUT` line cited a section as if that section
stated the conclusion. ⚠️ **The section gave the test; the conclusion was the agent's.**

> ## ⛔ PRESENTING YOUR OWN REASONING AS A WRITTEN RULE IS BANNED.
> ⭐ **Reasoning is fine — it just has to be labelled as reasoning.**

> ## ⭐ WHY THIS IS THE MOST IMPORTANT FIELD IN THE CONTRACT
> ⚠️ **It is the half that exists nowhere else, and the direct cause of *"no, that is not what I
> meant"*.** ⛔ **Without a declared boundary, an agent rebuilds the scope by inference when the
> context dies — and sounds equally confident.**

#### 🔒 INVARIANTS — ⭐ different from `OUT`, and often confused

| | Says |
|---|---|
| `OUT` | ⭐ **what you may not touch** |
| 🔒 `INVARIANT` | ⭐ **what must remain TRUE after your changes** |

⭐ *"Do not change a public signature. The existing tests stay green. No new dependency without
approval."* ⛔ **None of those is a path, so none of them fits in `OUT`.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-INV-001` | ⭐ **An invariant is observable** | 🟡 | ⛔ *"keep it clean"* is not one |
| `BLK-INV-002` | **Invariants are re-checked before closing** | 🟡 | ⚠️ ⭐ an invariant nobody re-checks is a wish |

---

### C · Connections — 🔴 to open

```
- DEPENDS ON: <block id> (why)
- DEPENDED ON BY: <block id>
- 🔴 CRITICAL PIECE: <path> — propagates to N files
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-CON-001` | **Every dependency named** | 🔒 | the section exists and is not empty |
| `BLK-CON-002` | ⭐ **Every id cited exists** | 🔒 | ⛔ otherwise §3 STOP |
| `BLK-CON-003` | ⭐ **A critical piece forces the widest lane** | 🟡 | ⚠️ see `rule-working-in-a-block.md` §2 |
| `BLK-CON-004` | ⭐ **Undeclared means out of reach** | 📖 | ⛔ nothing checks this |

⚠️ **`BLK-CON-004` is 📖 and it matters**, because inferring a connection from a similar name is
exactly how one block's assumptions leak into another's work.

---

### D · Required standards — 🔴 to open

⭐ **Which criterion files judge this block.** ⛔ **A block declaring none is judged by whatever
the reader remembers.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-STD-001` | ⭐ **At least one standard declared** | 🔒 | ⛔ none means no basis for rejection |
| `BLK-STD-002` | **Each declared file exists** | 🔒 | ⚠️ a standard pointing at nothing is not a standard |

> ## ⭐ THIS FIELD EXISTS BECAUSE A STANDARD THAT IS MERELY FINDABLE IS NOT READ.
> ⚠️ **Measured: a method that existed, was locatable, and went unread in most sessions.**
> ⭐ **Declared here, the gate injects it before the edit** — the standard travels with the work
> instead of sitting in an index nobody opens.

---

### E · State — 🟡 · ⭐ the section read first

```
current:  <what is actually true right now>
next:     <the immediate next step>
blockers: <what stops it, or none>
progress: N of M sub-blocks closed
updated:  <date>
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-STA-001` | **Within its ceiling** | 🔒 | ⭐ its value is that it is always read in full |
| `BLK-STA-002` | ⭐ **Updated when the state changes, not at close** | 📖 | ⛔ nothing checks this |
| `BLK-STA-003` | ⭐ **`current` states what IS TRUE, never what is intended** | 🟡 | ⚠️ see below |

⚠️ **`BLK-STA-003` is the distinction that gets lost:** ⭐ *"we are working on X"* **is not**
*"X is done"*. ⛔ **The intent lives in §A; the acceptance criteria in §7; this section holds only
what is presently true.**

---

### F · Sub-blocks — 🟡

| # | task | piece | dependents | ⭐ acceptance | ⭐ evidence | status |
|---|---|---|---|---|---|---|
| 1 | ⬜ | ⬜ | ⬜ N | ⬜ what "done" means | ⬜ what proves it | open/closed |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-SUB-001` | ⭐ **`dependents` is MEASURED, never remembered** | 🟡 | see below |
| `BLK-SUB-002` | ⭐ **Each row carries its acceptance and its evidence** | 🟡 | ⛔ *"done"* with nothing behind it |
| `BLK-SUB-003` | ⛔ **The parent does not close with an open sub-block** | 🔒 | ⚠️ closing over an open task hides it |

#### ⭐ THE GRAPH IS MEASURED, NEVER WRITTEN FROM MEMORY

| Rule | ⭐ Why |
|---|---|
| **Measure it with a tool** | the count changes as the code changes |
| ⭐ **The field records WHEN it was measured** | a number with no date is not evidence |
| **Re-measure before deciding a lane** | ⛔ a stale graph picks the wrong lane |
| ⛔ **Never copy a number from another block or document** | ⚠️ that is how a design says one thing while reality says another |

⭐ **Measured proof — the same piece, three answers on the same day:**

| Source | Dependents |
|---|---|
| an example written from memory | **5** |
| an automated run counting build artifacts | **38** |
| ⭐ **the real measurement** | **16** |

> ## ⛔ BUILD ARTIFACTS AND VENDORED CODE ARE NOT DEPENDENTS: THEY ARE COPIES.
> ⭐ **A number nobody can reproduce is not evidence.**

---

### G · Decisions — 🟡 · ⭐ each one with its rationale

```
- <date> · <what was decided>
  Rationale: <why this and not the alternative>
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-DEC-001` | ⭐ **A decision with no rationale does not count** | 🟡 | ⛔ *"we chose X"* with no why |
| `BLK-DEC-002` | ⭐ **A decision affecting the system also needs a decision record** | 📖 | ⚠️ see `contract-adr.md` |

⭐ **This is the *why* that dies at a context reset.** The *what* survives in the code; ⛔ **the
*why* does not survive anywhere else.**

---

### H · Friction log — 🟡

```
- <date> · rule: <name> · block: <id> · reason: <why it got in the way>
```

⭐ **Four fixed fields.** N frictions with the same rule in **distinct** blocks escalates —
⚠️ see `rule-working-in-a-block.md` §4.

⭐ **§H is the section people skip, and it is the one that keeps the law alive.** ⛔ **A rule
nobody logs friction against never changes** — the friction goes around the rule instead.

---

### I · Checkpoints — 🟡

⭐ **A safe point to resume from** — ⛔ not a diary.

---

### J · Context — 🟡 · ⭐ **curated, never a log**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-CTX-001` | **Within its ceiling** | 🔒 | ⚠️ a context that grows with every message is a transcript |
| `BLK-CTX-002` | ⭐ **If it would not change a future decision, delete it** | 📖 | ⛔ nothing checks this |

| ⛔ Not context | ✅ Context |
|---|---|
| *"on Tuesday we looked at… then we tried…"* | ⭐ *"the signing authority must stay server-side, because the client cannot be trusted with it"* |

⭐ **The first is history — it belongs in the block's own documents.** ⛔ **The second changes what
the next agent does.**

---

### K · Closing — 🔴 to close

```
closed: <date>
completed:            <what was done>
⭐ not completed:      <what was NOT, and why>
learned:              <what the next block should know>
evidence:             <what proves it>
connections affected: <who inherits something>
quality verdict:      <the measured table — `bin/grade-block <name>` produces it>
sufficiency:          pass | fail
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-CLS-001` | ⭐ **§K present before `status: closed`** | 🔒 | ⛔ closed with no closing section |
| `BLK-CLS-002` | **No open sub-block in §F** | 🔒 | ⚠️ closing over an open task hides it |
| `BLK-CLS-003` | ⭐ **What was NOT done is stated** | 🔒 | ⛔ silence reads as completeness |
| `BLK-CLS-004` | ⭐ **The verdict cites its evidence** | 🟡 | see `../memory/principles/expertise/val-functional.md` §2.1 |
| `BLK-CLS-005` | ⭐ **The quality verdict is MEASURED, never asserted** | 🟡 | `bin/grade-block` is layer 1 · `rules/contract-quality-verdict.md` is the criterion |
| `BLK-CLS-005` | ⭐ **The invariants of §B were re-checked** | 🟡 | ⚠️ still true after the changes? |

⭐ **`BLK-CLS-003` is what makes an archive worth reading.** ⛔ **A closing that lists only
successes teaches the next reader that this kind of work always succeeds.**

---

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

## 15 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ the ceilings, and the sections this installation adds | ⭐ the owner — ⚠️ **appended, never inserted into A-K** |
| the rules and their IDs | whoever maintains the engine, through a recorded decision |
| ⛔ closing a block that fails §11 | **nobody** — ⭐ the sufficiency test has no override |
| ⛔ an `OUT` line with no source | **nobody** — ⚠️ ⭐ it is the field the whole contract rests on |

---

**Decided by:** `decisions/ADR-010-cheap-to-open-expensive-to-close.md` — ⭐ **why only four sections are required at open**, and what a heavy open costs in blocks that never exist.
**Also decided by:** `decisions/ADR-009-one-file-per-block.md` — ⭐ **why ONE file**, why tiers are an order and not a boundary, and why the ceiling is read from here instead of repeated.
**Also decided by:** `decisions/ADR-001-work-unit-is-the-block.md` — ⭐ **why there are TWO levels**, what a single level loses, and how the decision is undone.

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
