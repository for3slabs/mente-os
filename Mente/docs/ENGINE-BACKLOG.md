# ENGINE BACKLOG — improvements the engine owes itself

**Status:** current · **Type:** append-only · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ ENGINE document — it lists what the **tool** still lacks, never what a project lacks.

---

## Purpose

What the engine has been shown to need and does not yet have. Each entry names the gap, why it
matters, and what would close it.

> ⛔ **This is not a project's pending list.** A project's open items live in its instance and
> never travel. This file travels with the engine, so every entry must be true for **anyone** who
> installs it — not for one installation.

⭐ **Each entry says what would CLOSE it, not just what is missing.** A gap with no closing
condition is a complaint; one with a closing condition is work that can be finished.

---

## How an entry is written

```markdown
### <ID> · <the gap, in one line>

- **Surfaced by:** what revealed it
- **Affects:** which pieces
- **Closes when:** ⭐ the condition that ends it

**Why it matters.** The consequence of leaving it open.
```

---

## E-01 · ✅ CLOSED — with E-25, which reports exactly this per rule

- **Surfaced by:** writing `../memory/principles/owner-1-docs.md`
- **Affects:** every `contract-*` and every owner file
- **Closes when:** a check reports which declared criteria have no verifier

**Why it matters.** A rule enforced by code is followed every time; one that lives only in a
document, roughly half. Both look identical when read. ⭐ Until the difference is visible, a
document-only rule gets trusted like a lock — and the trust is what makes it dangerous, not the
rule.

---

## E-02 · ✅ CLOSED — an edit outside every open scope is reported, and never blocked

- **Surfaced by:** writing `../memory/principles/owner-2-dev.md` §2
- **Affects:** the block contract (the scope section) · the gate that fires before an edit
- **Closed:** 2026-09-01 — `BLK-SCP-005` declared in `../rules/contract-block-sections.md`,
  enforced by `../hooks/pre-edit-standards.py`, with two probe cases (⑧ it reports · ⑨ with no
  block open it stays quiet)

**Why it mattered.** ⭐ Scope creep is the characteristic failure of an agent: it discovers a
dependency and decides on its own that it is in scope. The boundary was written and nothing
watched it, so it held exactly as long as attention did.

⭐ **It REPORTS, it does not block** — and that was the design decision, not a shortcut. Most edits
in a tree are legitimately outside every open block; a gate that stops them stops the work, and
then it is removed, taking the real drift with it. ⚠️ The hook already read `§B IN` to find the
owning block; the gap was its **silence** when no block owned the file. ⛔ With no block open at
all it still says nothing: there is no scope to be outside of, and speaking there would be noise
on every edit.

---

## E-03 · ✅ CLOSED — a checkpoint carries its eight fields, and the checker reads them from the contract

- **Surfaced by:** `../memory/principles/owner-2-dev.md` §6 · measured against the block contract, where a checkpoint
  is a single line
- **Affects:** the block contract · the sufficiency check
- **Closed:** 2026-09-01 — `BLK-CHK-001..004` declared in `../rules/contract-block-sections.md` §I,
  enforced in `../bin/check-block` beside the sufficiency test, with eight probe cases

**Why it mattered.** *"backend done"* satisfies the current shape and records nothing anyone can
act on. ⭐ The two fields that matter most — **what did not change** and **whether the scope held**
— are the two a free-form note never contains.

⚠️ **§I was the only section of the contract with no rule table** — one sentence, *"a safe point to
resume from — not a diary"*, against §K's seven named fields. ⭐ The eight fields were not invented
here: they already existed in `../memory/principles/owner-2-dev.md` §7 with nothing able to check
them, and were brought into the contract so something could.

⭐ **The reader takes the field list FROM the contract**, so renaming one there changes what is
demanded — probe case ㉝ proves it. ⛔ Hardcoding the eight would make two places declare one thing,
and the copy is the half that goes stale.

⚠️ **It stays quiet on an empty §I.** A block that has not reached a checkpoint has no §I, which is
a state and not a defect; §I is 🟡, and demanding it exist would make every fresh block fail its
own contract.

---

## E-04 · ✅ CLOSED — the exit code carries the verdict, declared once and checked

- **Surfaced by:** `../memory/principles/owner-1-docs.md` §3
- **Affects:** all three owners · the validators' exit codes
- **Closed:** 2026-09-01 — `CHK-XIT-001` declared in `../rules/rule-checks-must-measure.md` §3,
  enforced by `../bin/check-checks`, with five probe cases

**Why it mattered.** ⭐ REJECT and PENDING look similar and are opposite problems: *"this is wrong"*
versus *"nobody has decided yet"*. Collapsing them either blocks work that cannot proceed, or
files a violation as an open question — where it waits politely and forever.

⭐ **The measurement changed what the work was.** `WARN` and `REJECT` do not appear in this
engine's code at all; what a caller actually reads is the **exit code**. And two verdict
vocabularies already exist, both correct and neither redundant: `../memory/principles/owner-1-docs.md` §3
judges the WORK (PASS/WARN/REJECT/PENDING), and this rule's §3 judges a PROBE's reading of a
validator (PASS/FAIL/WRONG_CAUSE/CRASH/SKIP). ⛔ Merging them would have broken both. What was
missing is the link between them: which number carries which verdict.

| Code | Verdict | Means |
|---|---|---|
| `0` | ✅ PASS | every contract that applies is met |
| `1` | 🔴 REJECT | a contract is violated |
| `2` | ⬜ PENDING | it could NOT measure — its rule or table is missing |
| `3` | ⚠️ WARN | ⬜ declared, no validator emits it yet |

⭐ **Twelve validators already used `2` for exactly this, with nothing declaring it.** ⛔ One did
not: `../bin/check-handoff` returned `2` for a malformed manifest — a violated contract wearing the
code for *"could not measure"*, which is E-04's failure committed in code. It returns `1` now, and
22 probe cases that were pinned to the old codes moved with it.

⚠️ **The codes are read FROM the contract table**, so removing `2` there turns the twelve into
findings — measured, not assumed.

---

## E-05 · ✅ CLOSED — the unit is `lines`, declared, verified, and published as a number

- **Surfaced by:** `../memory/principles/owner-1-docs.md` §6
- **Affects:** the document contract's size table · `../bin/check-document` · `../bin/generate-metrics`
- **Closed:** 2026-09-01 — `DOC-SIZ-003` declared and enforced, three probe cases, and
  `documents.closest_to_ceiling` published in `METRICS.md`

**Why it mattered.** *"Too long"* is an opinion. ⭐ A ceiling with no unit cannot be checked, so it
is enforced by whoever happens to notice.

⚠️ **The units were already written — and never verified.** All eight numeric rows said `lines`,
and the reader's regex captured the digits and **discarded the word beside them**. ⛔ A row saying
`250 words` would still have been measured in LINES: the table claiming one thing, the check doing
another, and both looking correct on inspection. ⭐ That is the defect one layer in from the one
the entry describes.

⭐ **The second half of the criterion — *one command measures it* — is now a live number.**
`documents.closest_to_ceiling` reports the smallest margin left, not the biggest file: a 700-line
contract under a 700 ceiling is fine, a 260-line entry-point over a 250 one is not.

🔴 **Its first run found `README.md` at exactly 250 of 250 lines** — not a violation, and with no
margin at all. Filed as E-46.

⚠️ **A stale table in the principle, found on the way.** `../memory/principles/owner-1-docs.md`
declared that the four shape contracts *"are not written yet"* and that size limits were *"not
declared anywhere yet"*. ⛔ All of them exist. The table now names each contract and the validator
that enforces it.

---

## E-06 · ✅ CLOSED — a pointer is now asked what it resolved TO, not only whether it resolved

- **Surfaced by:** external review of `../memory/principles/owner-1-docs.md`
- **Affects:** the citation check
- **Closed:** 2026-09-01 — `DOC-CNT-007` declared in `../rules/contract-document.md`, enforced
  inside the walk `DOC-CNT-004` already makes, with four probe cases (㉘ superseded · ㉙ fossil ·
  ㉚ a current target is NOT reported · ㉛ a non-`.md` is out of scope)

**Why it mattered.** Replacing duplication with pointers is correct, and it moves the risk rather
than removing it: the target can exist and still be the wrong thing to read. ⭐ A pointer that
resolves to a superseded document is worse than a broken one — the broken one announces itself.

⭐ **It also raises `DOC-LIF-003` off the page.** *A fossil MUST NOT be used as a current
authority* sat in 📖 with nothing behind it; every pointer into one is now reported.

⚠️ **Measured before building, and it decided the design:** this template holds ZERO superseded or
fossil documents while a reference installation holds three, cited from dozens of places. ⛔ So the
rule is born empty here and bites where the engine is USED — and the probe must PLANT its target,
because one that waited to find one would pass forever while measuring nothing.

---

## E-07 · ✅ CLOSED — the structure existed and nothing read it; now one rule does

- **Surfaced by:** external review — *"a claim with no evidence"* is rejected, but evidence itself
  is undefined
- **Affects:** the voice · the owners' acceptance criteria · `../bin/check-block`
- **Closed:** 2026-09-01 — `BLK-SUB-004` declared in `../rules/contract-block-sections.md` §F and
  enforced, with four probe cases

**Why it mattered.** ⭐ *"The system has N documents"* and *"the system has N documents according to
the inventory generated on <date>"* are different claims. The first cannot be re-checked, which
means it cannot be found wrong — and a claim that cannot be found wrong is not evidence.

⚠️ **The entry was out of date, and measuring said so.** Evidence is fully structured already:
`../memory/principles/owner-3-validation.md` §5a gives four conditions, §5b grades it **L0-L5**,
and §5c lists the five fields a record carries. ⛔ **No code read any of it** — the same shape as
E-03, where eight checkpoint fields sat in a principle with nothing able to check them.

⭐ **So the work was to enforce, at the one place evidence is WRITTEN**: the `evidence` cell of a
sub-block row. `BLK-SUB-002` asked for it in 🟡 and accepted any text at all; the contract said
*"a number with no date is not evidence"* three separate times, and `../bin/check-block` had no
parser for that table.

⚠️ **The row carries two of the five, deliberately** — what was observed, and when. ⛔ A sub-block
row is one line; the other three (level, before→after, seen-to-fail) cannot be checked at all
without those two, so those two are what the lock demands.

⭐ **The finding names the TASK, not the row number** — *"sub-block 2"* sends the reader counting
rows.

---

## E-08 · ✅ CLOSED — 28 of 28 authority-bearing files declare who governs them, and a lock keeps it

- **Surfaced by:** external review of `../memory/principles/owner-1-docs.md`
- **Affects:** the owner files · the contracts · `../bin/check-document`
- **Closed:** 2026-09-01 — four missing sections written, `DOC-BOD-003` declared and enforced,
  four probe cases

**Why it mattered.** ⚠️ An owner that writes its own acceptance criteria is a circular authority:
*"acceptable"* converges on *"whatever it already does"* — ⛔ and nothing inside the file can
reveal it, because it reads as coherent precisely by agreeing with itself.

⚠️ **The entry was out of date.** It said two owner files declared this and the contracts did not;
measured, **all four principles and 11 of 15 contracts** already did. The four without were
`../rules/contract-block-sections.md` (the E-34 split left it behind),
`../rules/contract-campaign.md`, `../rules/contract-quality-verdict.md` and
`../rules/rule-accounts.md`.

⭐ **Two fields share a word and nothing else**, and separating them was half the work:

| | Answers |
|---|---|
| `**Governance:**` — a header field | does this file travel identical to every clone, or does the installation write it? |
| `## WHO GOVERNS THIS FILE` — a section | ⭐ **who may change WHAT inside it** |

⭐ **The section names what NOBODY may change**, not only who may. ⚠️ A table listing only
permissions reads as *"everything is negotiable by someone"*, and the rows that carry the weight
are the ones with no holder at all.

⛔ **Only `contract` and `rule` carry it.** A plan or an analysis grants no authority, and
demanding a governance section everywhere would make the marker meaningless by making it
universal.

---

## E-09 · ✅ CLOSED — a standard may declare WHEN it applies, and the gate honours it

- **Surfaced by:** external review of `../memory/principles/owner-2-dev.md`
- **Affects:** `../hooks/pre-edit-standards.py` · `../rules/contract-block-sections.md` §D
- **Closed:** 2026-09-01 — `BLK-STD-003` declared, the gate filters own AND inherited standards,
  three probe cases

**Why it mattered.** ⭐ Context is the scarce resource. Loading every discipline for a change that
touches one spends it on material that does not apply — and lets one discipline's criterion bleed
into a decision belonging to another.

⚠️ **Measured before building:** editing one `.md` named **seven** disciplines, five of which — the
three `dev-*` and both `val-*` — had nothing to say about it. ⛔ The reader cannot tell which of
the seven was meant for the file in front of them.

⭐ **The scope is DECLARED, never inferred.** `dev-frontend` sounds like it means `.tsx` and
nothing says so; ⛔ a gate that guessed from a filename would be right until the day it was not,
and wrong silently. A line narrows itself:

```
- `memory/principles/expertise/dev-backend.md`   — for: *.py
- `memory/principles/expertise/doc-structure.md` — for: *.md
- `rules/rule-working-in-a-block.md`
```

⬜ **A line with no `— for:` applies to everything**, which is why the rule is 🟡: every block
written before it keeps working unchanged, and narrowing is opt-in. ⚠️ **Inherited standards are
filtered the same way** — filtering only the block's own would leave the gate spending context on
exactly the standards a block did not write itself.

⛔ **The expertise README says *"a file nobody reads costs nothing"***, and that is true on disk
and false in a prompt. ⭐ Which is why the answer was to narrow the LOADING, never to delete a
discipline: what is irrelevant today may not be next quarter.

⚠️ **A stale claim, corrected on the way.** §D said *"the engine ships this declaration, not the
gate that would inject it"* — true when written, false since `../hooks/pre-edit-standards.py`
exists, and nothing had noticed.

---

## E-10 · ✅ CLOSED — four hooks shipped wired to nothing, and now the wiring itself is checked

- **Surfaced by:** external review of `../memory/principles/owner-1-docs.md`
- **Affects:** `../../.claude/settings.json` · `../bin/init` · `../bin/check-health` ·
  `../templates/mente.config.yml.template`
- **Closed:** 2026-09-01 — 5 hooks wired → 9, `hooks.registry` added to the config template, and
  `../bin/check-health` taught that a git hook registers by a LINK, not by text

**Why it mattered.** ⭐ A criterion with no trigger is applied when somebody remembers.

🔴 **The measurement found something larger than the entry described.** Four hooks shipped
**registered nowhere** — they existed, their probes were green, and no event ever ran them:

| Hook | Was | Now |
|---|---|---|
| `../hooks/gate-accounts.py` | ⛔ nothing ran it | `PreToolUse` · `Bash` |
| `../hooks/watch-external.py` | ⛔ nothing ran it | `PreToolUse` · `Bash` |
| `../hooks/gate-handoff.py` | ⛔ nothing ran it | `PreToolUse` · `Agent\|Task` |
| `../hooks/pre-commit.sh` | ⛔ `../bin/init` linked only `pre-push` | linked by `../bin/init` |

⚠️ **`../hooks/pre-commit.sh` implements `SHP-LCK-001`** — the rule refusing a commit on the base
branch — and it was installed in zero repositories. ⭐ Its own docstring names the failure it fell
to: *"a hook file that is not linked never runs, and looks installed."*

⭐ **`../bin/check-health` already knew how to catch this** — it is its concern ①, deliberately
reporting ⬜ NOT MEASURED rather than guessing where a host registers hooks. ⛔ What was missing is
that no installation could DECLARE it: `hooks.registry` did not exist in the config template, and
`MENTE_HOOK_REGISTRY` was named in no document.

⚠️ **Its first true answer was still half wrong.** With the registry declared it reported the two
git hooks as unregistered — ⛔ a true statement about the wrong registry: a git hook registers by a
symlink in `.git/hooks/`, which git cannot carry and a settings file will never name. ⭐ Reporting
those teaches the reader to ignore the finding.

⚠️ **What is NOT closed:** the fourteen trigger events the owners declare are not individually
wired — several have no host event at all (*"a plan arrives"*, *"evidence arrives late"*). ⭐ What
this entry asked for is that a declared trigger reach something that fires, and every hook the
engine ships now does.

---

## E-11 · ✅ CLOSED — a close writes `close.json`, and closing without one is refused

- **Surfaced by:** `../memory/principles/owner-3-validation.md`
- **Affects:** `../bin/grade-block` · `../bin/check-block` · `../rules/contract-block-sections.md` §K
- **Closed:** 2026-09-01 — `BLK-CLS-007` declared and enforced, `--json` gained the six
  dimensions, three probe cases

**Why it mattered.** ⭐ A close was a sentence somebody wrote. As a record it becomes **state the
system holds**, and a later disagreement is settled by reading instead of re-arguing.

⭐ **`--json` already existed** and carried the verdict, the metrics and the reds. ⛔ What it did
NOT carry is the half E-11 names explicitly: **which of the six layer-2 dimensions are still ⬜
UNKNOWN**. `../bin/grade-block` counted the undeclared rows and never said WHICH — a number
without names cannot be acted on.

⭐ **The dimensions are read FROM `../rules/contract-quality-verdict.md`**, never listed in code:
the frame travels with the engine and the criterion belongs to the installation, so a hardcoded
list would be the engine deciding what the installation judges. ⚠️ Verified by declaring one
dimension and watching only that row change.

⛔ **The record does not replace §K.** §K is what a person reads; `close.json` is what a machine
re-reads. A close writing only the record would be unreadable to the next human.

⚠️ **Three probe fixtures were closing blocks with no record**, so every closing case began
failing twice — ⛔ the second finding being the fixture's own defect, not the checker's. ⭐ A
fixture must be valid except for the thing under test: `../bin/probes/fixtures.py` writes the
record whenever it plants a closed block, and the cases that test its absence opt out.

---

## E-12 · Evidence production and closure authority are the same actor

- **Surfaced by:** external review · `../memory/principles/owner-3-validation.md` §1
- **Affects:** the validation owner · the quality dimensions
- **Closes when:** the layer that **runs** the checks is separate from the one that **decides**
  what they authorise

**Why it matters.** ⭐ Whoever produces the evidence should not be the one who decides what it
proves. A separate evidence layer answers *"this is what I observed"*; the closure authority
answers *"with this, it closes or it does not"*. ⚠️ Merged, an agent can satisfy the bar by
choosing what to measure — and the bar was the only thing stopping it from declaring itself done.

---

## E-13 · No level is declared for the evidence a block needs

- **Surfaced by:** `../memory/principles/owner-3-validation.md` §5b
- **Affects:** the block contract · the quality verdict
- **Closes when:** a block declares the evidence level its risk requires, and closing checks it

**Why it matters.** *"Tested"* means whatever the last person had time for. ⭐ A change that can
break a live flow needs end-to-end proof; one that renames a variable does not. Without a declared
level, both close on whichever was cheaper to produce.

---

## E-14 · ⭐ The delivery contract is a data model printed as a template

- **Surfaced by:** external review of the voice contract
- **Affects:** the voice · every response the agent produces
- **Closes when:** what must EXIST in a response is declared separately from how it is SHOWN

**Why it matters.** ⭐ **Rigidity for the machine, naturalness for the human.** The contract should
govern the information; the presentation layer should decide how it reaches the reader. Today they
are the same thing, so the agent exposes its internal model — printing every field of the closing
block whether or not the reader needed it. ⚠️ A protocol that feels like a protocol gets skimmed,
and a skimmed delivery is a delivery that did not land.

---

## E-15 · No progressive disclosure in a response

- **Surfaced by:** external review of the voice contract
- **Affects:** the voice · the delivery block
- **Closes when:** a response leads with orientation, and depth is available rather than imposed

**Why it matters.** A document says *read top to bottom*; ⭐ an interface says *look → identify →
go deeper only if you want to*. The engine already tiers a block's sections by reading cost — the
same idea has never been applied to a response, so every reader pays the deepest reader's price.

---

## E-16 · Emphasis is not rationed

- **Surfaced by:** external review of the voice contract
- **Affects:** the voice's graphics rules
- **Closes when:** a cap exists on how many emphasis devices one response may use

**Why it matters.** ⭐ **When everything is emphasised, nothing is.** The rules already say a
graphic replaces text rather than accompanying it, and that each one carries the prose saying why
— but nothing limits how many appear at once. A response using headings, bold, emoji, tables,
boxes, bars, quotes and rules simultaneously has no hierarchy left to signal with.

---

## E-17 · A decision is a field, not a response type

- **Surfaced by:** external review of the voice contract
- **Affects:** the response modes
- **Closes when:** *"you must choose"* is a shape of its own, not a section inside a larger one

**Why it matters.** ⭐ When the only thing that matters is that the reader chooses, everything
around the choice is noise — and burying it in a closing block is how a decision waits a turn
longer than it had to.

---

## E-18 · A rule that is read and not understood is a rule that communicates badly

- **Surfaced by:** ⭐ external review — two rules were reported as gaps and both already existed,
  stated correctly, in the file being read
- **Affects:** the voice · every contract
- **Closes when:** a rule's mechanics are visible on first read, not inferable on close reading

**Why it matters.** ⚠️ Being right is not the same as being understood. ⭐ A careful reader missing
a rule that is present and correct is evidence about the rule's form, not about the reader — and
the installer of an engine reads exactly once, with less attention than a reviewer.

---

## E-19 · ✅ CLOSED — every pattern ships both examples, and a check runs the catalogue

- **Surfaced by:** external review of the absorbed-patterns catalogue
- **Affects:** the pattern catalogue · the quality verdict
- **Closed:** 2026-09-01 — the contract gained `Fails` and `Passes`, all ten
  patterns carry both, and `bin/check-patterns` enforces it with
  `PAT-FLD-001`, `PAT-EXA-001` and `PAT-IDS-001`.
- ⭐ **The examples are minimal and stack-agnostic on purpose:** one carrying a
  second defect proves which one fired only by accident, and the reader cannot
  tell them apart.
- ⛔ **AND THE CHECK STATES ITS OWN LIMIT.** It measures that a pattern is
  described well enough to BE detected — ⚠️ it does not detect the patterns
  themselves. A check implying otherwise would let the catalogue look enforced
  while nothing scanned a line of code. That remains E-20.
- 🔴 **Found on the way in: the contract declared eight fields and every pattern
  carried seven.** `Policy` was missing from all ten — ⭐ because the ENGINE
  CANNOT WRITE IT: policy is what this installation does when the pattern is
  found, and a default shipped here would be one installation's answer wearing
  the engine's authority. ⚠️ It is now marked as the owner's and exempt, so an
  absent `Policy` reads as NOT DECLARED rather than as an oversight.

**Why it matters.** ⭐ A pattern nobody can detect is a sentence, not a rule. Fixtures turn the
catalogue into something executable: the failing example proves the detection actually fires, and
the passing one proves it does not fire on correct code. ⚠️ **Without the second, a detector that
flags everything scores perfectly** — and a rule that always triggers is a rule that gets disabled.

---

## E-20 · ✅ CLOSED — five are detected, five are named as undetectable, and one already was

- **Surfaced by:** the absorbed-patterns catalogue — each entry declares HOW it is found, and
  nothing performs the finding
- **Affects:** the quality verdict · the gate that fires before a commit
- **Closed:** 2026-09-01 — `bin/check-code-patterns` searches five; ⭐ five more
  are NAMED every run as not searched, with the reason. ⛔ Silence about those
  would let a reader conclude the code is clean of patterns nothing looked for.
- 🔴 **And one was ALREADY DETECTED with nobody knowing.** `grade-block` builds
  the import graph — that is `FP-STRUCT-001` — and cited no id. The same defect
  `check-locks` found among the locks: the behaviour existed, the traceability
  did not.
- ⚠️ **Every finding is a QUESTION, not a verdict, and the exit code says so.** A
  text pattern finds the SHAPE of a defect, never the intent: an unbounded read
  over three rows is fine. ⛔ A matcher that BLOCKED would be wrong often enough
  to be switched off within a week, and then the five it does find go unfound.
- 🔴 **The example pair caught a detector on its first run** — the unbounded-read
  pattern fired on `select * from events limit 100`, the catalogue's own PASSING
  example. ⭐ Exactly what E-19 built the pair for, working the day after.

**Why it matters.** ⭐ The catalogue now states detection, evidence and severity for each pattern —
which is exactly the shape a checker needs. Until one exists, these are rules followed by whoever
happens to remember them, which is the compliance rate the whole system was built to escape.

---

## E-21 · ✅ CLOSED — the ratio is measured on every run, and it has inverted

- **Surfaced by:** the pattern this engine was built to escape, applied to itself
- **Affects:** everything in this list
- **Closed:** 2026-09-01 — `bin/generate-metrics` publishes `rules.declared`,
  `rules.locked`, `rules.enforced_pct`, `backlog.closed` and `backlog.closed_pct`; three probe
  cases in `../bin/probes/probe-generators.py` (⑱ it publishes them · ⑲ they MOVE when the tree
  moves · ⑳ no backlog file is a gap, not a 0)

**Why it matters.** ⛔ **Designing a lot and validating a little is the failure mode that produces
systems nobody can trust** — and a governance engine is the easiest place in the world to commit
it, because writing a rule feels like solving the problem.

⚠️ **Measure it against this repository, not in the abstract.** Count what is written: the
principles, the folder contracts, the entries in this file. Then count what actually runs. ⭐ **If
the first number keeps growing while the second does not, the engine is proving its own diagnosis
right** — a document cannot refuse, and neither can a backlog.

**The test, stated plainly:** *how much of what this engine declares can it check?* Any answer
that has to be argued rather than measured is the answer.

⭐ **So the answer is generated, never written here.** Read `METRICS.md` — `rules.enforced_pct` and
`backlog.closed_pct`. ⛔ A number copied into this paragraph would be correct exactly once, and
this entry is the last place in the engine that should get that wrong.

⚠️ **What closing this entry does NOT mean.** It does not mean the engine is finished, and it does
not freeze the ratio: ⭐ the point was never to reach a figure, it was to stop the figure from
being a matter of opinion. ⛔ If the written half starts growing again while the enforced half
does not, the metric says so on the next run — which is the only form of this promise that
survives attention moving elsewhere.

---

## E-22 · ⭐ The block contract predates the criteria that now depend on it

- **Surfaced by:** writing the owner files — three of their mechanisms have nowhere to live
- **Affects:** the block contract · the sufficiency check · the gate that fires before an edit
- **Closes when:** the block contract carries the three fields below, and something reads them

**Why it matters.** ⭐ **The owners now demand things a block cannot express.** Each is a mechanism
declared in criterion with no field to hold it, so it holds only while somebody remembers:

| The owners demand | The block contract has |
|---|---|
| ⭐ **ALLOW / DENY** — the scope stated in both directions | a scope section, with no separation between the two halves |
| ⭐ **the evidence level** the work's risk requires | ⛔ nothing |
| ⭐ **checkpoints with their fields** — what changed, what did **not**, whether the scope held | a single free-form line |

⚠️ **This is the ordering problem, not a defect in either side.** The criteria were written after
the contract, and they turned out to need more than it offers. ⛔ **Writing the checks before the
contract carries the fields would produce checks that measure nothing** — the field has to exist
before anything can read it.

⭐ **It is also the entry that unblocks three others:** E-02, E-03 and E-13 all wait on a field
this contract does not yet have.

---

## E-23 · ✅ CLOSED — every type names its ceiling AND its unit, and a check measures it

- **Surfaced by:** `../memory/principles/expertise/doc-structure.md` — the file that makes splitting mandatory
- **Affects:** the document contract's type table · the health check · every engine document
- **Closed:** 2026-09-01 — 12 types, each with its ceiling and its unit, measured
  by `DOC-SIZ-001` in `bin/check-document`.
- 🔴 **And closing it found a type nothing could use.** The contract writes two
  kinds sharing one row — `analysis` · `case` — and the ceiling reader required
  exactly one name per cell, so BOTH ended up with no ceiling. ⛔ A type declared
  in the contract that no document could legally carry: check-document reported
  *"Type not in the contract's table"* for a type sitting right there in it.
- ⚠️ **Only the first row stated its unit**; the rest inherited it implicitly.
  ⛔ A reader who lands on row six is guessing, and a limit whose unit must be
  guessed is one nobody applies confidently. All seven numeric rows say `lines`
  now.

**Why it matters.** ⭐ The rule *"over its ceiling, it splits"* has no ceiling to measure against.
Every engine document declares a `Type` and no type declares a limit, so the strongest structural
rule in the system is unenforceable by construction.

⚠️ **And it is worse than a missing number.** Without a declared ceiling, whoever notices a file is
"long" applies their own threshold — which is the definition of a rule followed about half the
time. ⭐ **A ceiling nobody can measure is indistinguishable from no ceiling at all.**

---

## E-24 · ✅ CLOSED — five filenames and twenty-two piece ids are in English now

- **Surfaced by:** the leak scan of the rules step
- **Affects:** `templates/RESUME.md.template` · `templates/PENDING.md.template` ·
  `templates/ARCHITECTURE.md.template` · and `pieces.tsv` itself
- **Closes when:** the owner decides — rename, or declare the names deliberate
- ⭐ **The criterion this was missing:** `../rules/decisions/ADR-023-instructions-are-in-one-language.md`
  — ⚠️ **a filename is an instruction**: it is resolved and cited, so it follows the instruction
  language even when the content it names is a translated thought.

- **Closed:** 2026-09-01 — the owner decided: rename, not declare deliberate.

⭐ **What moved, and it was more than the three this entry named:**

| Was | Is | Cited by |
|---|---|---|
| RETOMAR.md | `RESUME.md` | 14 files |
| PENDIENTES.md | `PENDING.md` | 9 |
| ARQUITECTURA.md | `ARCHITECTURE.md` | 8 |
| piezas.tsv | `pieces.tsv` | 30 |
| cuentas.tsv | `accounts.tsv` | 15 |

⭐ **And 22 PIECE IDS, which this entry never counted.** A piece id is an ADDRESS
— it is cited from other files exactly as a filename is — so ADR-023 governs it
the same way. tpl-piezas became `tpl-pieces`, registro-cuentas became `accounts-register`,
and so on.

⚠️ **The hazard measured before touching anything:** `pieces` appears 27 times as
an ordinary word and `accounts` 11 times. ⛔ A blind replace would have rewritten
prose. Only the full filename was substituted, and the bare word `RETOMAR` was
replaced separately, as a whole word, in the three files that used it that way.

⭐ Moved with `git mv`, so history follows the file: a plain move records a
delete and an unrelated add, and then the log on the new name starts today.

133 citations rewritten across 46 files — the battery stayed green throughout
(the count is in `docs/METRICS.md`).

🔴 **AND THE EXHAUSTIVE AUDIT REOPENED THIS ENTRY.** Verifying all eighteen closed
entries BY EXECUTION rather than by reading found two things this record had
claimed and not done: the piece table's own HEADER ROW still named its five
columns in Spanish, and the table's id was still `piezas`.

⚠️ **The header is an instruction too** — it names the columns every reader
resolves and every writer copies by hand. ⛔ And FOUR readers compared against
the literal `"pieza"`, so renaming the row alone would have made each one treat
the header as a piece and report the word as an undeclared file. They moved
together.

⭐ **This is what closing by reading misses and closing by running does not.**

**Why it matters.** ⭐ Every rule in this engine is written in one language, and every filename
follows it — except four. ⚠️ **A clone in another country receives file names it cannot read**,
and the naming rule this engine ships says a name must state its subject to a stranger.

⛔ **This is not decided here.** Renaming touches the piece table, every pointer, and the
installer — ⭐ **and the names may be deliberate.** The finding is that nothing declares which.

---

## E-25 · ✅ CLOSED — every declared 🔒 is compared against the code, on every run

⚠️ **This is `E-01` with a measurement behind it.** E-01 asked for visibility; this names the exact
comparison, what it found by hand, and the one trap that makes a naive version useless.

- **Surfaced by:** the rule-by-rule audit — the same comparison run by hand thirteen times
- **Affects:** every `rules/*.md` and its validator
- **Closed:** 2026-09-01 — `bin/check-locks`, with `bin/probes/probe-locks.py`.
  ⭐ **E-01 closes with it**, as this entry said it would.
- ⭐ **Measured on closing: 199 declared, 195 cited, 4 delegated, 0 gaps.** The
  count started at 59 gaps when somebody first ran it by hand; the work of these
  sessions had closed most of them without anything counting.
- 🔴 **And it found 7 that were REAL, three of them mine.** Every one had the
  behaviour and none had the id: `ACC-LYR-001` is enforced by the wiring check,
  `ACC-LYR-003` by the push hook failing closed, `ACC-VRF-002` by the row report.
  ⛔ A rule traceable only by reading prose is one nothing can audit — which is
  the whole point of this check.
- ⚠️ **The check sees DELEGATION in both wordings the rules already use**
  (`performed by`, `enforced by`), because counting a correctly delegated lock
  as a gap is the false alarm that gets a check switched off.
- ⭐ **And it says what it CANNOT know, every run:** a citation proves the id is
  NAMED in code — whether that code enforces it is what the rule's own probe
  measures. ⛔ A reader who takes one for the other has been told something this
  check does not know.

**Why it matters.** ⛔ **Measured across the thirteen rules: 177 rows declared a lock and roughly
118 were implemented.** A rule that says 🔒 and has no lock is the one lie this system cannot
afford — ⚠️ **and it is invisible from the document, which reads exactly like an enforced one.**

⭐ **The comparison is mechanical:** the ids marked 🔒 in the table, against the ids the validator
names. It found 59 gaps by hand; a script finds them on every run.

⚠️ **It must also see DELEGATION.** Six rules are performed by another rule's check — `DOC-MOV-002`
by `DOC-CNT-004`, `BLK-ARC-001` by `ARC-DEL-002`. ⛔ **Counting those as gaps produces false
alarms, and a false alarm on a real tree is how a check gets switched off.**

---

## E-26 · ✅ CLOSED — the suite asks both questions, and reports them apart

- **Surfaced by:** audit 8 — `check-checks` had reported four real violations for seven audits
- **Affects:** `bin/probes/run-all.py` and every probe
- **Closed:** 2026-09-01 — `bin/probes/run-all.py` gained a "the tree right now"
  section that runs every validator bare, ⭐ **reported separately and never
  merged into the check count**: a probe result and a tree finding mean
  different things, and adding them would hide both.
- ⭐ **It uses the uniform `--quiet` contract**, so it needs no knowledge of what
  any validator checks — which is what lets a new one join with no edit here.
- 🔴 **And getting the SKIP right took three wrong attempts.** A tool needing a
  subject prints its usage, and a usage banner is not a finding. Parsing the
  usage TEXT called `check-handoff` subject-only when it sweeps every manifest,
  then missed a form whose only extra token was an option. ⭐ The text describes
  the contract; RUNNING the tool measures it — which is the principle this whole
  suite exists to apply, applied to itself.
- ⚠️ **Verified by planting a defect the probes cannot see** — a broken pointer
  in a document — and watching the new section report it while the battery stayed
  green (the count lives in `docs/METRICS.md`).

**Why it matters.** ⛔ **A probe answers "does this check detect what it claims?", never "is the
tree clean right now?"** — and the second question went unasked for seven audits while four
unguarded `open()` calls sat in the code.

> ⭐ Two questions, two runs. A suite that answers one and implies the other is worse than one
> that answers neither, because it looks complete.

---

## E-27 · ✅ CLOSED — a clean clone now runs the whole suite

- **Surfaced by:** `rules/rule-checks-must-measure.md` `CHK-IND-003`, still 📖
- **Affects:** all 14 validators
- **Closed by:** running it. ⭐ **The whole suite passes on a fresh clone with `failed: 0`**, and
  the clone is left byte-identical afterwards. ⛔ The count is not repeated here — it is a live
  number, and this file would be wrong the next time a probe is added.

⚠️ **What it found, and none of it was visible in the tree where it was written:**

| Found only on the clone | Why it was invisible |
|---|---|
| 7 documents cited an instance file the clone legitimately lacks | ⛔ the files were present where the checker was written |
| a scan target (⬜ `docs/architecture`) that exists nowhere and nothing creates | ⚠️ every clone printed NOT MEASURED on its first run |
| `probe-archive` crashed and left its fixture behind | ⭐ it scored 14/14 in the working tree |
| a declared piece with no template — a clone could not create it | ⛔ nothing said so; the file was simply there |

⭐ **The exemption for instance files is DERIVED now, not listed:** if `templates/` produces it,
the file belongs to the installation and a clean clone is right not to have it. ⛔ A hand-kept
list of what is fine is a hole with a schedule.

⚠️ **What stays open:** `CHK-IND-003` is still 📖. Running the clone was manual — ⭐ **nothing
makes it happen again**, and the next piece added can break it silently.

**Why it matters.** ⚠️ **Everything verified in this audit ran in the tree where it was written.**
⛔ A validator proven only there has been proven on one instance — which is the exact family the
rule names — and the failures that appear on a clean clone are the ones nobody sees until an
outsider installs it.

⭐ **It is the highest-value gap left**, because it is the one the engine exists for.

---

## E-28 · ✅ CLOSED — a 📖 row says which of the two it is, and the second kind is counted

- **Surfaced by:** the audit tally — 106 of 315 rules carry 📖
- **Affects:** every rule file
- **Closed:** 2026-09-01 — `CHK-DIS-001` in `rules/rule-checks-must-measure.md`,
  counted by `bin/check-locks` on every run.
- ⭐ **The marker is the word `yet`, because the rules already used it** — the
  convention was there, read by nothing, which is how a distinction stops being
  one.
- ⚠️ **And the measurement corrected this entry's own numbers.** Two rows say
  `yet` — that part held. ⛔ But **27 more claim nothing checks them and never
  say WHICH KIND**, and those are the real ambiguity: from the row, a genuine
  limit and an unwritten check read identically. They are reported as ambiguous
  rather than as findings — ⭐ a 📖 row breaks nothing, and treating it as a
  violation would make the honest majority look like debt.

**Why it matters.** ⭐ **Most of those 106 are honest:** a script can check that a friction was
logged, never that the work stopped to think. ⛔ **But two say "nothing verifies this YET"**, and
those are work, not a limit. ⚠️ **Mixed into one symbol, the buildable ones are invisible** — and
a backlog nobody can see is a backlog nobody works.

---

## E-29 · ✅ CLOSED — the unfilled ⬜ are listed, and never counted as debt

- **Surfaced by:** the audit — 100 ⬜ markers across the thirteen rules
- **Affects:** every rule that defers a threshold, a path or a vocabulary to the installation
- **Closed:** 2026-09-01 — `bin/check-declarations`, over both surfaces: the
  thresholds a RULE defers (a ⬜ row whose value is `0`) and the values an
  INSTANCE declaration has not been given (`null`, `[]`, `""`).
- ⛔ **AND IT NEVER FAILS.** Every line it prints is a decision the owner may
  leave open forever. ⚠️ A check exiting non-zero over those turns a deliberate
  choice into debt, and the next person "fixes" it by inventing the very numbers
  this engine refuses to invent.
- ⭐ **It also tells an unfilled tree from an uninstalled one.** Without a config
  nothing distinguishes "the owner left these open" from "nobody installed this
  yet" — ⛔ and reporting the second as the first makes a fresh clone look
  neglected.

**Why it matters.** ⭐ **`⬜` is the mechanism that makes this engine portable:** thresholds,
section names, base branch, code extensions. ⛔ **An unfilled one is NOT MEASURED, and every rule
that depends on it silently measures nothing.**

⚠️ **Measured during the audit:** the staleness threshold, the section ceilings and the pending
period all default to `0`, and `0` means the rule is off. ⭐ **That is correct and honest — and
invisible unless something counts them.**

---

## E-30 · ✅ CLOSED — the rule states when a reader is shared, and the readers cite it

- **Surfaced by:** audit 4 — four copies of the same section reader, already diverged
- **Affects:** `bin/blockread.py`, and every future validator over a shared shape
- **Closed:** 2026-09-01 — `CHK-SHR-001`, `CHK-SHR-002` and `CHK-SHR-003` in `rules/rule-checks-must-measure.md`.
- 🔴 **And closing it caught the thing itself happening.** The criterion lived in two
  docstrings and in no rule, so when a THIRD shared reader was written
  (`bin/scaffold.py`, for what both scaffolders ask before opening a unit of work)
  it **restated the criterion a third time** instead of pointing at it. ⚠️ A
  criterion repeated is a criterion that diverges — the same failure the rule
  describes, one level up. Hence `CHK-SHR-003`, and both readers now cite.

**Why it matters.** ⛔ **Two readers over one shape diverge; one cannot.** ⚠️ But the opposite
error is just as real: forcing two SHAPES into one reader made a decision record return nothing,
and "nothing" reads exactly like "the section is empty".

⭐ **The line is drawn in one comment inside one file.** A line that matters this much belongs in
a rule, not in a comment somebody has to find.

---

## E-31 · ✅ CLOSED — grouping lives in one reader, used by eight validators

- **Surfaced by:** audit 12 — a real list produced 590 findings that were 5 distinct shapes
- **Affects:** every validator that iterates over many objects
- **Closed:** 2026-09-01 — `bin/findings.py`, shared under `CHK-SHR-001`.
  Eight validators report through it; ⭐ the rest emit too few findings to group
  and are left alone rather than migrated for uniformity.
- 🔴 **The extracted logic did not work outside where it grew.** It keyed on
  (id, FILE, shape) — right for one list with many items, wrong for many files
  with one item each: six blocks sharing one defect stayed six shapes because
  the file differed. ⛔ Measured: 18 findings reported as 18 shapes when they
  were 3. A path is a subject too, and so is a quoted value — the object a
  finding is ABOUT differs per object by definition.
- ⚠️ **And three inserted imports landed inside a docstring and inside a
  multi-line import**, breaking the files at parse time. ⛔ Both only failed when
  the file was RUN, and an exit 0 over a clean tree hid it — ⭐ which is why the
  verification plants a defect and watches the validator FAIL, rather than
  watching it pass.

**Why it matters.** ⛔ **A report nobody finishes is a report nobody applies** — the same argument
this engine makes against long documents, applied to its own output. ⭐ **`check-pending` groups
now; the other thirteen do not**, and any of them can hit the same volume the moment a real
instance has many objects.

---

## E-32 · ⚠️ Two real archives and one real block carry defects this engine now detects

- **Surfaced by:** the cross-runs, against objects nobody wrote for this engine
- **Affects:** nothing in the engine — ⭐ recorded so the findings are not lost
- **Closes when:** the installation that owns them decides whether to fix or accept them

**Why it matters.** ⭐ **These are not engine gaps; they are proof the engine measures something
real:**

| Finding | Where |
|---|---|
| one archive is missing both its summary and its connections file | 1 of 6 real archives |
| two closed blocks declare acceptance and no sufficiency | 6 real closed blocks |
| a block's declared scope resolves to one path out of three | 1 real block |
| two rules marked project-level live in the universal file every clone inherits | a real base-rules |
| 14 commands granted twice, once as `x` and once as `./x` | a real configuration |

⛔ **The engine does not fix these** — they belong to an installation. ⚠️ **But an audit that finds
them and writes them nowhere has measured for nothing.**

---

## E-33 · ✅ CLOSED — the suite was four times slower than it needed to be

- **Surfaced by:** timing the engine end to end, because a system that works and takes too long
  is not worth running
- **Affects:** `bin/probes/run-all.py` and every probe
- **Closed by:** giving each probe a private copy of the tree and running them in parallel

⭐ **Measured, in order, before choosing:**

| Approach | Time |
|---|---|
| the 14 validators alone | 1.3s — ⛔ **not the bottleneck** |
| probes in plain sequence | 11.1s |
| ⚠️ 9 isolated in parallel + 5 sharing in series | **14.2s — worse than sequence** |
| ⭐ all 14 isolated, in parallel | **the suite runs in roughly a quarter of the time** |

⛔ **Five probes edit SHARED state** — the universal rules, a contract, the project rules — so
running them side by side in one tree does not produce a slow answer, it produces a FALSE one.
⭐ **Copying the whole tree costs 0.04s for ~100 files**, which is cheaper than the disk
contention it removes.

⬜ `MENTE_PROBES_SERIAL=1` forces the old behaviour, for debugging a probe whose failure only
appears in the real tree. ⭐ Both modes verified to give the same result.

⚠️ **And isolation surfaced a real defect:** `probe-shipping` reads the REPOSITORY, and a copy has
no `.git`. The rule correctly said ⬜ NOT MEASURED — ⛔ **and the probe counted that honest answer
as a pre-existing failure**, blaming the checker for saying what the rule requires. It declares
the dependency now, in both places that needed it.

---

## E-34 · ✅ CLOSED — split by topic, and the split exposed a hidden dependency

- **Surfaced by:** wiring ADR-011 — the file crossed its declared ceiling by one line
- **Affects:** `rules/contract-block.md`
- **Closed:** 2026-09-01 — 702 lines became 362 (`rules/contract-block.md`, the
  LIFECYCLE) and 387 (`rules/contract-block-sections.md`, the SHAPE of §A-K). ⭐ Split
  by TOPIC, not by size: §6 was half the file and described the eleven sections,
  which is a subject of its own.
- ⭐ **Every id kept its number**, so no citation moved. The letters are
  addresses; the split moved text and changed no pointer.
- 🔴 **AND THE SPLIT EXPOSED A DEPENDENCY NOTHING DECLARED.** `bin/new-block`
  reads the type and lane vocabularies out of the contract — and they left with
  §A. ⛔ It stopped creating blocks entirely, and `probe-block` planted a ceiling
  edit in the half nothing reads, reporting a working check as undetected.
- ⭐ **The lesson is the one this whole backlog keeps repeating:** two things in
  one file can depend on being together, and nothing says so until they are
  apart. Both consumers now read the contract as the two halves it is.

**Why it matters.** ⭐ **`DOC-SIZ-001` does not say "raise the ceiling" — it says a file over its
ceiling owes a SPLIT, and that the split is named work rather than a warning.**

⛔ **The ceiling was already raised once this period**, from a smaller number to the current one.
⚠️ **Raising it again for one line would be conceding to the file instead of measuring it** — and
the second raise is always easier than the first, which is how a limit stops being one.

⭐ **What was tried first, and is the right order:** compress the prose that could be compressed
(the wiring block, three lines into one), and only then record the split. ⛔ **What was NOT done
is delete content to fit** — a contract that loses a rule to satisfy its own size limit has
traded the wrong thing.

⚠️ **The candidate split is visible:** the block contract holds both the SHAPE of a block and the
LIFECYCLE of one — sections and fields on one side, opening, transitions and closing on the
other. ⭐ **Two topics, and the contract itself says `split by topic`.**

---

## E-35 · Nesting has no bound, and the intermediate level was never built

- **Surfaced by:** ADR-015 — the first decision brought in with `implementation: not-started`
- **Affects:** `rules/contract-block.md` · a rule that does not exist yet
- **Closes when:** a rule counts nesting depth and refuses beyond the declared bound, and the
  block contract defines the intermediate level

**Why it matters.** ⭐ **Measured: real blocks reach fourteen flat sub-blocks**, which is the exact
failure the decision predicted for two fixed levels. ⛔ **The intermediate level was decided and
never built**, so large work flattened instead of grouping.

⚠️ **Not urgent, and the record says why:** fourteen flat sub-blocks proves the level is NEEDED —
⛔ **it does not prove it would be USED.** ⭐ Those are different claims, and building the level is
how the second one gets tested.

---

## E-36 · ✅ CLOSED — two generators exist, and they derive nothing that needs judgment

- **Surfaced by:** ADR-019 — the second record to ship `implementation: not-started`
- **Affects:** `bin/` — the `generate-*` family that `bin/README.md` and `CAPABILITIES.md` both name
- **Closed:** 2026-09-01 — `bin/generate-index` (INDEX · STATES · DECISIONS) and
  `bin/generate-metrics` (METRICS). Both announce every file they touch, and both
  hold the line: they derive an index and a count, ⛔ never a criterion or a verdict.
- ⭐ **And the generator taught the engine something it did not know:** reading the
  battery's result by RUNNING it recursed, because the battery runs the probe that
  exercises the generator. ⚠️ It presented as slowness, not as a loop. The battery
  now refuses to run inside itself, and the metric READS the last recorded result —
  a number that costs a full verification run to read is one nobody regenerates.

**Why it matters.** ⭐ **Measured: not one of the 14 validators writes anything.** ⛔ Every check
reports and stops, so a gap it finds stays a gap until somebody acts — and the acting is the part
that was measured failing five times out of eleven.

⭐ **The naming rule already ships**, which is the right order: `check-*` and `grade-*` read,
`generate-*` writes, and each announces what it touched. ⚠️ **The rule governs tools that do not
exist yet** — ⛔ but writing it after the first generator would mean the first one set the
precedent instead of following it.

🔴 **The line that must not move:** a generator may derive a graph, an index or a draft. ⛔ **It
may never derive a criterion, a scope or a verdict** — if those could be computed, they would not
need an owner.

---

## E-37 · A reusable CASE is not a document type here

- **Surfaced by:** ADR-021 — the third record to ship `implementation: not-started`
- **Affects:** `rules/README.md` (the type table) · a shape that does not exist yet
- **Closes when:** a case has its own type with a declared shape, an entry filter, and a cap

**Why it matters.** ⭐ **Measured in a real installation: the three-question filter admitted
exactly ONE error as a case over months — and that case is cited by nineteen files.** ⛔ The filter
works, and the engine cannot offer it: a case is none of its three document types.

⚠️ **What happens without it, and it is not a disaster:** a case-shaped document is written as a
rule with a story in it. ⭐ **That works and loses the filter** — nothing asks the three questions,
so the next installation records errors by instinct.

⭐ **The cap was never tested**, because the filter was strict enough that nothing approached it.
⛔ **Worth remembering when building this:** the limit that did the work was the FILTER, not the
ceiling — building the ceiling first would protect against a problem that has never occurred.

---

## E-38 · ✅ CLOSED — the startup audit runs, and it discovers rather than lists

- **Surfaced by:** ADR-024 — no health check, and no hook that runs one at session start
- **Affects:** `hooks/session-start.sh`
- **Closed by:** the hook exists, obeys both constraints, and is verified in three states

⭐ **What it does NOT do, deliberately:** it names no validator. ⛔ Listing them would make the
hook grow with every check added, which is how a hook becomes a list nobody maintains. It
DISCOVERS every `check-*` in `bin/`, and ⬜ an installation may override the set.

⚠️ **What remains open is smaller and was never the point of this entry:** there is no single
`check-health` that summarises. ⭐ The loop over every validator answers the same question without
one — and a summary command that repeats what the loop already reports would be the redundancy
this engine keeps removing.

**Why it matters.** ⭐ **Measured: three distinct failures each lived for WEEKS, and all three were
found by somebody ASKING.** ⛔ None was hidden — every one was visible to a check that existed and
was not run.

> ⛔ **IF YOU HAVE TO ASK FOR IT, IT IS NOT AUTOMATED.**

⭐ **The two constraints already ship as rules**, ahead of the tool: never block the session at
startup, and speak only when something is wrong. ⚠️ **That order is deliberate** — a startup check
that blocks, or that prints on every healthy run, is removed within a week, and then the engine
has neither the tool nor the rule.

🔴 **The line that must not move:** an audit REPORTS. ⛔ It never deletes what it finds — a
self-cleaning audit destroys the evidence of how the state was reached, and makes a recurring
fault look like a healthy system.

---

---

## E-39 · ✅ CLOSED — `secrets/` is hardened by its own grantor, not by a future installer

**Found and closed:** while building `gate-handoff`, 2026-08-30.

Git stores only the executable bit, so a cloned `secrets/` arrives at whatever
the umask gives — measured: `755`, world-readable, in a folder whose README
promises `700`. `CFG-SEC-004` reports it, which is right, but a report is not a
repair: the folder stays open until somebody reads the finding and acts.

⛔ FILED FIRST AS "bin/init should do it", AND THAT WAS WRONG TWICE. It defers a
live exposure to a piece that does not exist yet, and it puts the knowledge in
the installer instead of in the piece that owns the folder. ⚠️ An installer runs
once; the exposure can return any time somebody recreates the folder.

⭐ CLOSED IN `bin/secrets-lease` instead — the grantor already owns this folder
and already runs before anything reads it. It hardens on every `open`, which
makes the fix idempotent and independent of how the tree arrived.
⛔ Deliberately NOT a hook on every session: a permission reapplied constantly
would fight an owner who hardened it further, and it only tightens, never
loosens.

---

## E-40 · ✅ CLOSED — all three gaps, and the third was not the question it looked like

**Found:** while building the two layers, 2026-08-30.

The registry, its validator and both gates exist. ⭐ Three things do not — and
they are NOT equally urgent, which is the point of this entry. ⛔ A backlog that
lists three gaps without ranking them turns into three things nobody starts.

### ⭐ THE RANKING, AND WHAT DECIDES IT

⚠️ **The test is not "how much work is left". It is: while this gap is open,
what does the system CLAIM that is not true?**

| # | Gap | What is claimed while it is open | Urgency |
|---|---|---|---|
| **1** | nothing WIRES layer 2 | 🔴 **"two layers protect this"** — one of them never runs | 🔴 **now** |
| **2** | ⬜ `bin/conectar-cuenta` absent | ⚠️ a template names a piece that does not exist | 🟡 next |
| **3** | remotes never compared | ⬜ nothing — the rule already says it is unmeasured | 🟢 needs a decision first |

> ## 🔴 GAP 1 IS URGENT BECAUSE IT IS THE ONLY ONE THAT MAKES THE SYSTEM LIE.
> ⭐ Gaps 2 and 3 are **absences, and they are visible**: a missing piece cannot
> be mistaken for a working one. ⛔ Gap 1 is a **false presence** — the file is
> there, the code is correct, its probe passes, and the protection is off.

---

### 🔴 1 · Nothing WIRES layer 2 · urgent

`hooks/pre-push.sh` cannot be walked around — ⛔ **but only once something links
it into the tool's hook directory.** Until then it never runs, and layer 1 is
the only defence left: the one measured to be walked past by five ways of
writing the same command out of seven tried.

⚠️ **The exposure is not theoretical and it is not future.** It is the state of
every clone the moment it is made. `ACC-LYR-004` REPORTS it, which is the honest
half — ⛔ **a report is not a repair**, and the folder stays open until somebody
reads the finding and acts.

⭐ **Where it belongs, and the pattern is already proven here.** `bin/secrets-lease`
hardens the folder it owns, on every grant, without waiting for an installer.
That fix is idempotent and independent of how the tree arrived. ⛔ The opposite
shape — an installer that runs once and knows about everything — fails the same
way twice: it does not run again when somebody recreates the thing, and it puts
the knowledge somewhere other than the piece that owns it.

### ✅ 2 · CLOSED — `bin/connect-account` answers from the registry

The registry's own header names it as the piece that RESOLVES which account
governs a repository. ⛔ A template that ships a name for something absent is a
promise the reader cannot tell from a fact.

**Closed:** 2026-09-01. ⭐ `check-accounts` VERIFIES the registry; nothing
CONSULTED it, so the fact it holds was readable only by opening the file and
matching rows by eye — ⛔ and a person matching by eye is a FOURTH place the
truth lives, which is the drift the registry exists to end.

⚠️ It answers, it never acts: no credential is read, nothing is configured. The
`guia` column is a POINTER, and the tool prints the pointer — ⛔ printing the
guide would put access steps into a terminal and a transcript, the exact move
`secrets/` exists to prevent, made by the piece meant to respect it.

⭐ And it never guesses: an ambiguous name is REFUSED rather than resolved to
whichever row came first. An answer about which account may push is acted on
immediately, and a confident wrong one sends work somewhere nobody looks.

⚠️ Renamed on the way in: the promise said `conectar-cuenta`, in a template that
travels. ADR-023 governs it.

### ✅ 3 · CLOSED — and the decision it was waiting for had already been made three times

`ACC-VRF-001` checks a declared local path. ⛔ Nothing compares the registry with
what the machine's remotes actually say — ⚠️ **which is exactly where the drift
this rule describes happens**: the remote, the documentation and someone's
memory disagree, and none of them knows.

🔴 **THE FRONTIER WAS ALREADY CROSSED, AND NOTHING SAID SO.** Measured while
closing this: `check-clear-ready`, `check-shipping` and `hooks/pre-push.sh` all run the
host's tool, all three identically — read only, absence never a failure. ⭐ The
criterion was right and invisible, and the fourth piece would have reinterpreted
it again.

⭐ **`ADR-031` now declares it**, and the scope question it was waiting for had
also been answered already — in the registry's own template, which instructs the
reader to re-measure with the LOCAL remote listing. ⛔ The decision lived in a
template and was never promoted to a rule, which is the shape of every gap in
this backlog.

⭐ `bin/connect-account` performs the comparison inside that boundary: it reads
this clone's remotes and reports three distinct disagreements — a declared repo
that does not match the real remote, a declared remote this clone does not have,
and a clone whose remotes match no declared row at all.

---

### ⭐ WHY THIS ENTRY MATTERS MORE THAN ITS SIZE

The accounts registry is where three separate systems meet:

| File | The question it answers |
|---|---|
| `pieces.tsv` | ⭐ what a piece **IS** |
| `accounts.tsv` | ⭐ where its work **GOES** |
| the `guia` column | ⭐ where the access to it **LIVES** |

⛔ **A gap here is not local to this file.** Whatever attaches to the piece table
or to shipping arrives through this registry, and it inherits whatever is still
open in it.

---

## E-41 · ✅ CLOSED — a probe proves a PIECE; nothing proved a PAIR

**Found and closed:** 2026-09-01, by the exhaustive audit of the eighteen closed
entries.

🔴 **`gate-critical` had not fired for days, and every probe was green.** It ran
`check-block --quiet` and looked for a block's name in that run's output — empty
by contract, `CHK-QUI-001`. ⛔ The condition could never be true, so every
insufficient close went straight through.

> ## ⭐ A PROBE PROVES A PIECE WORKS. IT CANNOT PROVE TWO PIECES STILL AGREE.
> ⚠️ That is a different question, and nothing in the suite was asking it.

⛔ **The failure shape is always the same:** one side changes its contract — a
flag stops printing, an exit code shifts, a message is reworded — and the other
keeps reading what used to be there. **Both sides pass their own probe, and the
pair is dead.**

⭐ **`bin/probes/probe-conjunction.py` closes it.** Five gates call a validator;
it exercises every pair against a REAL INSTALLATION — installed, with a block
and a manifest and a registry — because a gate that only ever meets fixtures has
never met the validator it depends on.

⚠️ **Proven by reintroducing the defect:** with the old `--quiet` read restored,
the probe drops to 8 of 10 and names the case. Had it existed, the gate would
have been dead for one run rather than for days.


Related: `README.md` (folder) · `../memory/principles/README.md` (where the owners live) ·
`../rules/README.md` (where a closed entry usually lands) · `../CAPABILITIES.md`.

---

## E-42 · ✅ CLOSED — a case numeral is an address, and the battery now refuses a repeated one

- **Surfaced by:** adding the `DOC-CNT-007` cases (E-06) — ㉒㉓㉔㉕ were already duplicated
- **Affects:** `../bin/probes/run-all.py` · `../bin/probes/harness.py` · 12 probes
- **Closed:** 2026-09-01 — the battery reports a repeated numeral as one failure, proved by
  planting a duplicate in a copy: `probe-locks 🔴 case label used twice: ④`

**Why it mattered.** A failure reported as ㉕ had two possible homes. ⚠️ Cheap while a probe is
green; ⛔ it costs exactly when the numeral is read, which is when something broke.

⭐ **It was bigger than the entry said.** Measured across the battery: **fifteen** probes carried a
repeated numeral, not one — and three separate causes hid behind the same symptom.

| Cause | Reach | Fix |
|---|---|---|
| the shared harness printed its crash case as a fixed `⑨` | 11 probes | ⭐ it is NAMED, not numbered — one hand-written number in a shared piece collided eleven ways |
| a section notice reused the last case's numeral | 9 probes | it carries no numeral, the way `probe-grade` already did it |
| one case applied to several subjects printed one row each | 2 probes | ⭐ a suffix per subject (`⑤a`…`⑤d`), so a failure names WHICH |

⛔ **The guard lives in the battery, not the harness.** 23 of the 30 probes print their own results
and never construct a `Probe`, so a harness-side guard would cover seven while reading as though it
covered all thirty. ⚠️ It was written there first and moved — two pieces answering one question is
how one of them ends up wrong.

⚠️ **Its first version cried wolf on prose:** it counted any non-ascii token opening a line, so ⬜
notices and ⭐ headings read as colliding cases — 7 of the 15 were false. ⭐ It reads numerals only,
and a lettered suffix counts as part of the address.

---

## E-43 · ✅ CLOSED — `p.track()` deleted a contract, and its name did not say it could

- **Surfaced by:** closing E-03 — a probe case edited the real contract and marked it with
  `track()` so it would be tidied up
- **Affects:** `../bin/probes/harness.py` · every probe
- **Closed:** 2026-09-01 — `track()` refuses any path that is not this probe's own fixture

**Why it mattered.** 🔴 `track()` registers a path for `clean()`, and `clean()` calls `os.remove` —
⛔ **it deletes, it does not restore.** ⚠️ The name reads like bookkeeping, and the file was gone:
`../rules/contract-block-sections.md`, recovered from the last commit, with the `BLK-CHK-*` declaration
written since then lost and rewritten by hand.

⭐ **A probe must never write to the engine it is measuring.** To measure against a modified engine,
copy the tree and edit the copy — which is what case ㉝ does now. ⛔ The guard is a refusal rather
than a comment because *"the probe cleans up after itself"* is precisely the assumption that made
the deletion possible.

---

## E-44 · ✅ CLOSED — 23 of 23 emit a verdict, and the battery refuses a silent one

- **Surfaced by:** measuring symbol-vs-exit-code across all 23 validators while closing E-04
- **Affects:** `../bin/check-archive` · `../bin/check-campaign` · `../bin/check-handoff` ·
  `../bin/check-patterns` · `../bin/check-pending` · `../bin/probes/run-all.py`
- **Closed:** 2026-09-01 — the five now say ⬜ or ✅, and the battery counts a mute validator as a
  failure, proved by silencing one in a copy

**Why it mattered.** ⭐ The exit code is unambiguous since `CHK-XIT-001`, and a person reading the
terminal does not see it. ⚠️ These five printed a summary line and fell silent when their
collection was empty — ⛔ and silence after a summary reads exactly like a tick to anyone skimming
a battery run.

⭐ **No new rule was needed: `CHK-TRV-002` already said it** — *when the instance is absent, the
check SKIPS and SAYS SO, never a pass*. ⚠️ Its implementation measured something narrower than its
wording (an unguarded `open()`), so the rule was right and its reach was short. The battery closes
that gap rather than a second rule being declared beside it.

⚠️ **The first count was wrong and measuring fixed it.** Reading "does a verdict symbol appear
anywhere in the output" gave five; reading "does the LAST line carry one" gave eight. ⭐ The extra
three (`../bin/check-code-patterns`, `../bin/check-declarations`, `../bin/check-health`) do say ⬜
out loud and then close with explanatory prose — they never committed the defect. ⛔ The stricter
reading would have sent three correct validators to be "fixed".

---

## E-45 · ✅ CLOSED — the reporter owns the clean-run verdict, and six validators stopped writing it

- **Surfaced by:** closing E-44 — `../bin/check-patterns` was the one `report()` caller that never
  printed it
- **Affects:** `../bin/findings.py` · six validators
- **Closed:** 2026-09-01 — `report()` takes `examined` and `subject`; six callers pass them and
  deleted their own line

**Why it mattered.** ⭐ `report()` printed nothing when there was nothing to report, so every caller
wrote its own `✅ 0 violations`. ⚠️ Fifteen copies of one line, and one had forgotten it — which is
precisely how a duplicated line fails: not all at once, but one straggler at a time.

⭐ **The caller passes HOW MANY things it examined**, because it is the only one that knows what it
was counting; the reporter turns `0` into ⬜ and anything else into ✅. ⛔ Inferring it inside the
reporter would mean guessing at the caller's collection.

🔴 **A worse defect surfaced while migrating.** `../bin/check-work` and `../bin/check-block` printed
`✅ 0 violations` over a tree with **zero blocks** — not silence, an assertion that it passed.
⚠️ That is more dangerous than the five mute ones E-44 fixed: a false tick is more convincing than
an absence.

⭐ **Nine local ticks remain and are correct**: their subject always exists — documents, validators,
the engine's own rules — so an unconditional ✅ is the true verdict there. ⛔ Migrating them for
symmetry would have made three correct validators say ⬜ over a subject that was never missing.

---

## E-46 · ✅ CLOSED — the README points at the campaign contract instead of restating it

- **Surfaced by:** the first run of `documents.closest_to_ceiling` (E-05)
- **Affects:** `../README.md`
- **Closed:** 2026-09-01 — 250 → 239 lines, by condensing §4's campaign half to a pointer

**Why it mattered.** ⭐ 250 of 250 is not a violation — `DOC-SIZ-001` fires above the ceiling, not
at it. ⚠️ It is also zero margin: the next line breaks it, and whoever adds that line will be doing
something else at the time.

⭐ **The answer was POINT, not trim.** The 24 lines on campaigns restated what
`../rules/contract-campaign.md` already says — it does not execute, it orders, and switching blocks
resets the why. ⛔ That is `DOC-CNT-003` (*point, never copy*) broken in the engine's own front
door: two texts able to disagree about one concept, in the file a newcomer reads first.

⚠️ **Trimming would have been the wrong fix** and it was available: eleven lines of prose could
have been cut anywhere. ⭐ Removing a duplication takes the same eleven lines and leaves the
document more correct, not merely shorter.

---

## E-47 · ✅ CLOSED — a command inside a code block is now checked, and four were phantoms

- **Surfaced by:** reading `../README.md` while closing E-46 — it told the reader to run a command
  that was deliberately never built
- **Affects:** `../bin/check-document` · `../README.md` · `../QUICKSTART.md` · `../CAPABILITIES.md`
- **Closed:** 2026-09-01 — `DOC-CNT-004` now walks fenced blocks, with three probe cases

**Why it mattered.** ⭐ A fenced command is a **stronger** pointer than an inline one: it does not
name a piece, it tells the reader what to RUN. ⛔ `DOC-CNT-004` only saw backticks, so four
citations of two never-built commands — ⬜ `bin/check-all` and ⬜ `bin/check-sufficiency` — sat
unreported in the first three files a newcomer opens.

⚠️ **`check-sufficiency` will never exist**, and that is on the record: whether §A-E would let
someone restart is the one test a script cannot run. The three documents now say so instead of
promising a command. ⭐ `bin/grade-block` DOES exist and `CAPABILITIES.md` marked it ⬜ — the
marker was as stale as the phantom beside it.

⚠️ **The matcher took three attempts, and each failure was measured.** Pairing fences without
anchoring the close to a line start made one block's close pair with the next block's open;
filtering by language tag meant a `yaml` block never matched its own opening and knocked every
fence after it out of step — 4 "blocks" captured on one README, two of them paragraphs. ⛔ A
`python` block is exempt: source inside a docstring is an example of what to write, not a command.

