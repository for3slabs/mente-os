# CONTRACT · BLOCK SECTIONS — what each of §A-K carries

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** ⭐ every block file — this is the SHAPE half of the block contract
**Enforcement:** 🔒 `bin/check-block` · the same validator that reads the other half
**Level:** 🌐 universal — ⭐ travels identical to every clone; a lower level may ADD or TIGHTEN, never loosen
**Verified by:** `bin/check-block` · `bin/probes/probe-block.py`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone
**Size:** a BASE file — it ships whole. See `contract-document.md` §4.

---

## 0 · WHAT THIS FILE IS

> ## ⭐ The eleven sections a block carries, and what each one must answer.

⛔ **This is one half of one contract, not a second contract.** `contract-block.md`
holds the LIFECYCLE — when a block opens, what stops it, when it may close.
⭐ **This holds the SHAPE** — what §A through §K contain, with the rules that
govern each.

⚠️ **Why they are apart:** together they ran past the ceiling a document of this
type declares, and `DOC-SIZ-001` says a file over its ceiling owes a SPLIT, never
a raised limit. ⛔ **The second raise is always easier than the first, which is
how a limit stops being one.**

⭐ **The letters are ADDRESSES.** Other files cite `§B` and the ids below; ⛔ they
are never renumbered, and a new section is appended, never inserted — so this
split moved the text and changed no citation.

---

## 1 · THE SECTIONS

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
| `BLK-SCP-005` | ⭐ **An edit outside every declared scope is REPORTED** | 🔒 | ⚠️ informed, never blocked — see below |

> ## ⭐ `BLK-SCP-005` · WHY IT REPORTS AND DOES NOT BLOCK
> ⛔ **Scope creep is the characteristic failure of an agent:** it discovers a dependency and
> decides on its own that it is in scope. ⚠️ Until now the boundary was written and nothing
> watched it — so it held exactly as long as attention did.
>
> ⛔ **But blocking every edit outside a scope would be unbearable**, and an unbearable guard is
> deleted: most edits in a tree are legitimately outside every open block, and a gate that stops
> them stops the work. ⭐ **What is missing is not permission — it is NOTICING**, out loud, at the
> moment it happens.

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
| `BLK-STD-003` | ⭐ **A standard MAY declare WHEN it applies** — `— for: <glob>` | 🟡 | ⛔ without it every standard is named on every edit |

> ## ⭐ `BLK-STD-003` · CONTEXT IS THE SCARCE RESOURCE, AND THE GATE SPENDS IT ON EVERY EDIT
> ⚠️ **Measured: editing one `.md` named seven disciplines**, five of which — the three `dev-*`
> and both `val-*` — had nothing to say about it. ⛔ Not merely wasteful: **one discipline's
> criterion bleeds into a decision belonging to another**, and the reader cannot tell which of
> the seven was meant for the file in front of them.
>
> ```
> - `memory/principles/expertise/dev-backend.md`   — for: *.py
> - `memory/principles/expertise/doc-structure.md` — for: *.md
> - `rules/rule-working-in-a-block.md`
> ```
>
> ⭐ **A line with no `— for:` applies to everything**, which is why this is 🟡 and not 🔒: every
> block written before this rule keeps working unchanged, and narrowing is opt-in.
>
> ⛔ **The engine does not GUESS the scope from a filename.** `dev-frontend` sounds like it means
> `.tsx` and nothing says so — ⚠️ a gate that inferred it would be right until the day it was not,
> and wrong silently.

> ## ⭐ THIS FIELD EXISTS BECAUSE A STANDARD THAT IS MERELY FINDABLE IS NOT READ.
> ⚠️ **Measured: a method that existed, was locatable, and went unread in most sessions.**
> ⭐ **Declared here, the standard travels WITH the work**, instead of sitting in an index nobody
> opens. ⭐ **The engine ships the gate too**: `../hooks/pre-edit-standards.py` names these back
> before the file is written. ⛔ It REPORTS and never blocks — an unbearable guard gets deleted,
> and a deleted guard protects nothing.
>
> ⚠️ **This paragraph said the opposite until 2026-09-01** — *"the engine ships this declaration,
> not the gate that would inject it"* — which was true when written and stopped being true without
> anything noticing. ⭐ The reasoning behind it still holds and is why the gate reports rather than
> promises: claiming a layer that is not there has a reader trust it
> (`decisions/ADR-011-four-layers-guarantee-reading.md`).

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
| `BLK-SUB-004` | ⭐ **An `evidence` field states WHAT was observed and WHEN** | 🔒 | ⛔ a claim that cannot be re-checked cannot be found wrong — see below |

> ## ⭐ `BLK-SUB-004` · EVIDENCE IS A CLAIM SOMEONE ELSE CAN RE-RUN
> ⛔ **"the system has 55 documents"** and **"the system has 55 documents, `bin/check-document`,
> 2026-09-01"** are different claims. ⚠️ The first cannot be re-checked, so it cannot be found
> wrong — ⭐ **and a claim that cannot be found wrong is not evidence, it is a statement.**
>
> ⭐ **Two fields, and the second is the one that gets dropped:**
>
> | Part | ⛔ Without it |
> |---|---|
> | ⭐ **what was observed** — a number, a command, a file | *"done"* · *"works"* · *"verified"* |
> | ⭐ **when** — an ISO date | ⚠️ a number correct once, quoted forever |
>
> ⚠️ **This is the shape, not the weight.** `../memory/principles/owner-3-validation.md` §5b grades
> evidence L0-L5 and §5c lists the five fields a full record carries; ⛔ a sub-block row is one
> line, so it carries the two without which the other three cannot be checked at all.

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

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `BLK-CHK-001` | ⛔ **A checkpoint is EVIDENCE, not a note** — it carries its fields | 🔒 | ⭐ the fields are read from the table below, never hardcoded |
| `BLK-CHK-002` | ⭐ **`did not change` and `scope` are never omitted** | 🔒 | ⭐ performed by `BLK-CHK-001` — they are two of the eight, not a second check |
| `BLK-CHK-003` | **`verified` states what was run AND its result** | 🟡 | ⛔ a claim with no check is an opinion |
| `BLK-CHK-004` | ⭐ **`scope` answers held or widened — never blank** | 🔒 | ⭐ the lock of §B, made auditable |

⭐ **The eight fields, and why each is there.** ⚠️ They are not this contract's invention: they are
`memory/principles/owner-2-dev.md` §7, brought here so something can check them.

| Field | Why it is there |
|---|---|
| `changed` | the claim |
| ⭐ `did not change` | ⚠️ the half that proves the scope held |
| `pieces` | so what depends on them can be found |
| `standard` | so the bar is known, not assumed |
| `verified` | ⛔ what was run, and its result |
| `unexpected` | ⭐ the most valuable line, and the one omitted first |
| `remains` | so the next session does not re-derive it |
| ⭐ `scope` | `held` or `widened: <what>` — the lock of §B, made auditable |

> ## ⛔ *"backend done"* SATISFIES A FREE-FORM SHAPE AND RECORDS NOTHING
> ⭐ **A checkpoint is read by whoever resumes** — and what they need is not the good news. ⚠️ The
> two fields that decide whether the work can be trusted are the two nobody writes unprompted:
> **what did NOT change** (the scope held) and **what behaved unexpectedly** (the thing that will
> cost a day if it is rediscovered instead of read).
>
> ⛔ **`unexpected` and `remains` may say `none`** — that is an answer. ⚠️ Leaving them out is not:
> silence cannot be told apart from forgetting, which is the whole reason the field exists.

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
| `BLK-CLS-006` | ⭐ **The quality verdict is MEASURED, never asserted** | 🟡 | `bin/grade-block` is layer 1 · `rules/contract-quality-verdict.md` is the criterion |
| `BLK-CLS-005` | ⭐ **The invariants of §B were re-checked** | 🟡 | ⚠️ still true after the changes? |

⭐ **`BLK-CLS-003` is what makes an archive worth reading.** ⛔ **A closing that lists only
successes teaches the next reader that this kind of work always succeeds.**

---

---

## WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ the sections this installation adds beyond A-K | ⭐ the owner — ⚠️ **appended, never renumbered** |
| the rules and their IDs | whoever maintains the engine, through a recorded decision |
| ⛔ an `OUT` line with no source | **nobody** — ⚠️ ⭐ it is the field the whole scope lock rests on |
| ⛔ a checkpoint without `did not change` or `scope` | **nobody** — ⭐ they are the two a free-form note never contains |

⚠️ **This half and `contract-block.md` are ONE contract.** ⛔ A change to either that leaves them
disagreeing is a change to both — the split was for size, never for authority.

---

Related: `contract-block.md` (the lifecycle half — opening, stopping, closing) · `contract-document.md` (the ceiling this split obeys) · `../bin/check-block` (the validator that reads both halves).
