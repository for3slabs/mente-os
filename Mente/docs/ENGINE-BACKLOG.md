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

## E-01 · A criterion with no validator is invisible as such

- **Surfaced by:** writing `../memory/principles/owner-1-docs.md`
- **Affects:** every `contract-*` and every owner file
- **Closes when:** a check reports which declared criteria have no verifier

**Why it matters.** A rule enforced by code is followed every time; one that lives only in a
document, roughly half. Both look identical when read. ⭐ Until the difference is visible, a
document-only rule gets trusted like a lock — and the trust is what makes it dangerous, not the
rule.

---

## E-02 · No mechanism enforces `SCOPE LOCK`

- **Surfaced by:** writing `../memory/principles/owner-2-dev.md` §2
- **Affects:** the block contract (the scope section) · the gate that fires before an edit
- **Closes when:** editing a piece outside the declared ALLOW is reported, or blocked

**Why it matters.** ⭐ Scope creep is the characteristic failure of an agent: it discovers a
dependency and decides on its own that it is in scope. Today the boundary is written and nothing
watches it, so it holds exactly as long as attention does.

---

## E-03 · A checkpoint has no required content

- **Surfaced by:** `../memory/principles/owner-2-dev.md` §6 · measured against the block contract, where a checkpoint
  is a single line
- **Affects:** the block contract · the sufficiency check
- **Closes when:** the sufficiency check verifies a checkpoint carries its fields

**Why it matters.** *"backend done"* satisfies the current shape and records nothing anyone can
act on. ⭐ The two fields that matter most — **what did not change** and **whether the scope held**
— are the two a free-form note never contains.

---

## E-04 · The four verdicts are not a shared vocabulary

- **Surfaced by:** `../memory/principles/owner-1-docs.md` §3
- **Affects:** all three owners · the validators' exit codes
- **Closes when:** PASS / WARN / REJECT / PENDING mean the same thing in every piece that emits one

**Why it matters.** ⭐ REJECT and PENDING look similar and are opposite problems: *"this is wrong"*
versus *"nobody has decided yet"*. Collapsing them either blocks work that cannot proceed, or
files a violation as an open question — where it waits politely and forever.

---

## E-05 · Size limits have no declared unit

- **Surfaced by:** `../memory/principles/owner-1-docs.md` §6
- **Affects:** the document contract's size table · the health check
- **Closes when:** every limit states its unit, and one command measures it

**Why it matters.** *"Too long"* is an opinion. ⭐ A ceiling with no unit cannot be checked, so it
is enforced by whoever happens to notice — which is the definition of a rule that holds half the
time.

---

## E-06 · Nothing verifies that a pointer's target is still current

- **Surfaced by:** external review of `../memory/principles/owner-1-docs.md`
- **Affects:** the citation check
- **Closes when:** a pointer to a `superseded` or `fossil` document is reported

**Why it matters.** Replacing duplication with pointers is correct, and it moves the risk rather
than removing it: the target can exist and still be the wrong thing to read. ⭐ A pointer that
resolves to a superseded document is worse than a broken one — the broken one announces itself.

---

## E-07 · Evidence has no structure

- **Surfaced by:** external review — *"a claim with no evidence"* is rejected, but evidence itself
  is undefined
- **Affects:** the voice · the owners' acceptance criteria
- **Closes when:** an evidence reference states what was observed, where, and when

**Why it matters.** ⭐ *"The system has N documents"* and *"the system has N documents according to
the inventory generated on <date>"* are different claims. The first cannot be re-checked, which
means it cannot be found wrong — and a claim that cannot be found wrong is not evidence.

---

## E-08 · Governance of the governing files is undeclared

- **Surfaced by:** external review of `../memory/principles/owner-1-docs.md`
- **Affects:** the owner files · the contracts
- **Closes when:** each declares who may change it, and it is not itself

**Why it matters.** ⚠️ An owner that writes its own acceptance criteria is a circular authority:
*"acceptable"* converges on *"whatever it already does"*. ⭐ The two owner files written so far
declare this; the contracts do not.

---

## E-09 · Disciplines are loaded whole, not by relevance

- **Surfaced by:** external review of `../memory/principles/owner-2-dev.md`
- **Affects:** the gate that injects standards before an edit
- **Closes when:** only the disciplines a change actually touches are loaded

**Why it matters.** ⭐ Context is the scarce resource. Loading every discipline for a change that
touches one spends it on material that does not apply — and lets one discipline's criterion bleed
into a decision belonging to another.

---

## E-10 · No trigger contract for the owners

- **Surfaced by:** external review of `../memory/principles/owner-1-docs.md`
- **Affects:** all three owners · the gates
- **Closes when:** each owner's trigger events are wired to something that fires

**Why it matters.** ⭐ A criterion with no trigger is applied when somebody remembers. The owner
files now declare *when* they act; nothing yet acts on that declaration.

---

## E-11 · Closing produces no artefact

- **Surfaced by:** `../memory/principles/owner-3-validation.md`
- **Affects:** the closing procedure · the quality verdict
- **Closes when:** a close writes a machine-readable record — verdict, level, which dimensions
  passed, which are UNKNOWN, and the evidence behind each

**Why it matters.** ⭐ Today a close is a sentence somebody wrote. With an artefact it becomes
**state the system holds**, and a later disagreement can be settled by reading it instead of
re-arguing it. It also makes the UNKNOWN list survive the session that produced it.

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

## E-19 · Failure patterns have no regression fixtures

- **Surfaced by:** external review of the absorbed-patterns catalogue
- **Affects:** the pattern catalogue · the quality verdict
- **Closes when:** each pattern ships a failing example and a passing one, and a check runs both

**Why it matters.** ⭐ A pattern nobody can detect is a sentence, not a rule. Fixtures turn the
catalogue into something executable: the failing example proves the detection actually fires, and
the passing one proves it does not fire on correct code. ⚠️ **Without the second, a detector that
flags everything scores perfectly** — and a rule that always triggers is a rule that gets disabled.

---

## E-20 · Absorbed patterns are catalogued but not detected

- **Surfaced by:** the absorbed-patterns catalogue — each entry declares HOW it is found, and
  nothing performs the finding
- **Affects:** the quality verdict · the gate that fires before a commit
- **Closes when:** the statically-detectable patterns are checked by something that runs

**Why it matters.** ⭐ The catalogue now states detection, evidence and severity for each pattern —
which is exactly the shape a checker needs. Until one exists, these are rules followed by whoever
happens to remember them, which is the compliance rate the whole system was built to escape.

---

## E-21 · ⭐ The engine is designed further ahead than it is validated

- **Surfaced by:** the pattern this engine was built to escape, applied to itself
- **Affects:** everything in this list
- **Closes when:** ⭐ the ratio inverts — more of this backlog is **enforced** than is **written**

**Why it matters.** ⛔ **Designing a lot and validating a little is the failure mode that produces
systems nobody can trust** — and a governance engine is the easiest place in the world to commit
it, because writing a rule feels like solving the problem.

⚠️ **Measure it against this repository, not in the abstract.** Count what is written: the
principles, the folder contracts, the entries in this file. Then count what actually runs. ⭐ **If
the first number keeps growing while the second does not, the engine is proving its own diagnosis
right** — a document cannot refuse, and neither can a backlog.

**The test, stated plainly:** *how much of what this engine declares can it check?* Any answer
that has to be argued rather than measured is the answer.

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

## E-23 · No document declares which ceiling applies to it

- **Surfaced by:** `../memory/principles/expertise/doc-structure.md` — the file that makes splitting mandatory
- **Affects:** the document contract's type table · the health check · every engine document
- **Closes when:** each `Type` names its ceiling and its unit, and a check measures it

**Why it matters.** ⭐ The rule *"over its ceiling, it splits"* has no ceiling to measure against.
Every engine document declares a `Type` and no type declares a limit, so the strongest structural
rule in the system is unenforceable by construction.

⚠️ **And it is worse than a missing number.** Without a declared ceiling, whoever notices a file is
"long" applies their own threshold — which is the definition of a rule followed about half the
time. ⭐ **A ceiling nobody can measure is indistinguishable from no ceiling at all.**

---

## E-24 · Three template filenames are not in English

- **Surfaced by:** the leak scan of the rules step
- **Affects:** `templates/RETOMAR.md.template` · `templates/PENDIENTES.md.template` ·
  `templates/ARQUITECTURA.md.template` · and `piezas.tsv` itself
- **Closes when:** the owner decides — rename, or declare the names deliberate

**Why it matters.** ⭐ Every rule in this engine is written in one language, and every filename
follows it — except four. ⚠️ **A clone in another country receives file names it cannot read**,
and the naming rule this engine ships says a name must state its subject to a stranger.

⛔ **This is not decided here.** Renaming touches the piece table, every pointer, and the
installer — ⭐ **and the names may be deliberate.** The finding is that nothing declares which.

---

## E-25 · ⭐ Nothing compares a declared 🔒 against the code

⚠️ **This is `E-01` with a measurement behind it.** E-01 asked for visibility; this names the exact
comparison, what it found by hand, and the one trap that makes a naive version useless.

- **Surfaced by:** the rule-by-rule audit — the same comparison run by hand thirteen times
- **Affects:** every `rules/*.md` and its validator
- **Closes when:** a check reports, per rule, how many rows declare 🔒 and how many ids the
  validator actually cites — ⭐ **closing E-01 with it**

**Why it matters.** ⛔ **Measured across the thirteen rules: 177 rows declared a lock and roughly
118 were implemented.** A rule that says 🔒 and has no lock is the one lie this system cannot
afford — ⚠️ **and it is invisible from the document, which reads exactly like an enforced one.**

⭐ **The comparison is mechanical:** the ids marked 🔒 in the table, against the ids the validator
names. It found 59 gaps by hand; a script finds them on every run.

⚠️ **It must also see DELEGATION.** Six rules are performed by another rule's check — `DOC-MOV-002`
by `DOC-CNT-004`, `BLK-ARC-001` by `ARC-DEL-002`. ⛔ **Counting those as gaps produces false
alarms, and a false alarm on a real tree is how a check gets switched off.**

---

## E-26 · ⭐ A probe filters to its own fixtures, so a validator can be green there and dirty on the tree

- **Surfaced by:** audit 8 — `check-checks` had reported four real violations for seven audits
- **Affects:** `bin/probes/run-all.py` and every probe
- **Closes when:** the suite runs each validator against the real tree as well as its fixtures,
  and reports both

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
| a scan target (`docs/architecture`) that exists nowhere and nothing creates | ⚠️ every clone printed NOT MEASURED on its first run |
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

## E-28 · 106 rules are 📖 and nothing distinguishes "cannot be checked" from "not built yet"

- **Surfaced by:** the audit tally — 106 of 315 rules carry 📖
- **Affects:** every rule file
- **Closes when:** a 📖 row declares which of the two it is, and the count of the second kind is
  reported

**Why it matters.** ⭐ **Most of those 106 are honest:** a script can check that a friction was
logged, never that the work stopped to think. ⛔ **But two say "nothing verifies this YET"**, and
those are work, not a limit. ⚠️ **Mixed into one symbol, the buildable ones are invisible** — and
a backlog nobody can see is a backlog nobody works.

---

## E-29 · ⬜ declarations have no completeness report

- **Surfaced by:** the audit — 100 ⬜ markers across the thirteen rules
- **Affects:** every rule that defers a threshold, a path or a vocabulary to the installation
- **Closes when:** a check lists the ⬜ declarations an installation has not filled

**Why it matters.** ⭐ **`⬜` is the mechanism that makes this engine portable:** thresholds,
section names, base branch, code extensions. ⛔ **An unfilled one is NOT MEASURED, and every rule
that depends on it silently measures nothing.**

⚠️ **Measured during the audit:** the staleness threshold, the section ceilings and the pending
period all default to `0`, and `0` means the rule is off. ⭐ **That is correct and honest — and
invisible unless something counts them.**

---

## E-30 · A shared reader exists for blocks and for nothing else

- **Surfaced by:** audit 4 — four copies of the same section reader, already diverged
- **Affects:** `bin/blockread.py`, and every future validator over a shared shape
- **Closes when:** a rule states when a parser is shared and when a shape earns its own

**Why it matters.** ⛔ **Two readers over one shape diverge; one cannot.** ⚠️ But the opposite
error is just as real: forcing two SHAPES into one reader made a decision record return nothing,
and "nothing" reads exactly like "the section is empty".

⭐ **The line is drawn in one comment inside one file.** A line that matters this much belongs in
a rule, not in a comment somebody has to find.

---

## E-31 · Repeated findings are grouped in one validator only

- **Surfaced by:** audit 12 — a real list produced 590 findings that were 5 distinct shapes
- **Affects:** every validator that iterates over many objects
- **Closes when:** grouping lives in one place every validator uses

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

## E-34 · `contract-block` is at its ceiling and owes a split

- **Surfaced by:** wiring ADR-011 — the file crossed its declared ceiling by one line
- **Affects:** `rules/contract-block.md`
- **Closes when:** the contract is split by topic and each part is under its own ceiling

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

## E-36 · Nothing completes what is derivable — the generators do not exist

- **Surfaced by:** ADR-019 — the second record to ship `implementation: not-started`
- **Affects:** `bin/` — the `generate-*` family that `bin/README` and `CAPABILITIES.md` both name
- **Closes when:** at least one generator exists, announces every file it touches, and derives
  nothing that requires judgment

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

Related: `README.md` (folder) · `../memory/principles/README.md` (where the owners live) ·
`../rules/README.md` (where a closed entry usually lands) · `../CAPABILITIES.md`.
