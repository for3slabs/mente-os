# ENGINE BACKLOG — improvements the engine owes itself

**Status:** current · **Type:** entry-point · **Updated:** {{date}}
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

- **Surfaced by:** writing `owner-1-docs.md`
- **Affects:** every `contract-*` and every owner file
- **Closes when:** a check reports which declared criteria have no verifier

**Why it matters.** A rule enforced by code is followed every time; one that lives only in a
document, roughly half. Both look identical when read. ⭐ Until the difference is visible, a
document-only rule gets trusted like a lock — and the trust is what makes it dangerous, not the
rule.

---

## E-02 · No mechanism enforces `SCOPE LOCK`

- **Surfaced by:** writing `owner-2-dev.md` §2
- **Affects:** the block contract (the scope section) · the gate that fires before an edit
- **Closes when:** editing a piece outside the declared ALLOW is reported, or blocked

**Why it matters.** ⭐ Scope creep is the characteristic failure of an agent: it discovers a
dependency and decides on its own that it is in scope. Today the boundary is written and nothing
watches it, so it holds exactly as long as attention does.

---

## E-03 · A checkpoint has no required content

- **Surfaced by:** `owner-2-dev.md` §6 · measured against the block contract, where a checkpoint
  is a single line
- **Affects:** the block contract · the sufficiency check
- **Closes when:** the sufficiency check verifies a checkpoint carries its fields

**Why it matters.** *"backend done"* satisfies the current shape and records nothing anyone can
act on. ⭐ The two fields that matter most — **what did not change** and **whether the scope held**
— are the two a free-form note never contains.

---

## E-04 · The four verdicts are not a shared vocabulary

- **Surfaced by:** `owner-1-docs.md` §3
- **Affects:** all three owners · the validators' exit codes
- **Closes when:** PASS / WARN / REJECT / PENDING mean the same thing in every piece that emits one

**Why it matters.** ⭐ REJECT and PENDING look similar and are opposite problems: *"this is wrong"*
versus *"nobody has decided yet"*. Collapsing them either blocks work that cannot proceed, or
files a violation as an open question — where it waits politely and forever.

---

## E-05 · Size limits have no declared unit

- **Surfaced by:** `owner-1-docs.md` §6
- **Affects:** the document contract's size table · the health check
- **Closes when:** every limit states its unit, and one command measures it

**Why it matters.** *"Too long"* is an opinion. ⭐ A ceiling with no unit cannot be checked, so it
is enforced by whoever happens to notice — which is the definition of a rule that holds half the
time.

---

## E-06 · Nothing verifies that a pointer's target is still current

- **Surfaced by:** external review of `owner-1-docs.md`
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

- **Surfaced by:** external review of `owner-1-docs.md`
- **Affects:** the owner files · the contracts
- **Closes when:** each declares who may change it, and it is not itself

**Why it matters.** ⚠️ An owner that writes its own acceptance criteria is a circular authority:
*"acceptable"* converges on *"whatever it already does"*. ⭐ The two owner files written so far
declare this; the contracts do not.

---

## E-09 · Disciplines are loaded whole, not by relevance

- **Surfaced by:** external review of `owner-2-dev.md`
- **Affects:** the gate that injects standards before an edit
- **Closes when:** only the disciplines a change actually touches are loaded

**Why it matters.** ⭐ Context is the scarce resource. Loading every discipline for a change that
touches one spends it on material that does not apply — and lets one discipline's criterion bleed
into a decision belonging to another.

---

## E-10 · No trigger contract for the owners

- **Surfaced by:** external review of `owner-1-docs.md`
- **Affects:** all three owners · the gates
- **Closes when:** each owner's trigger events are wired to something that fires

**Why it matters.** ⭐ A criterion with no trigger is applied when somebody remembers. The owner
files now declare *when* they act; nothing yet acts on that declaration.

---

## E-11 · Closing produces no artefact

- **Surfaced by:** `owner-3-validation.md`
- **Affects:** the closing procedure · the quality verdict
- **Closes when:** a close writes a machine-readable record — verdict, level, which dimensions
  passed, which are UNKNOWN, and the evidence behind each

**Why it matters.** ⭐ Today a close is a sentence somebody wrote. With an artefact it becomes
**state the system holds**, and a later disagreement can be settled by reading it instead of
re-arguing it. It also makes the UNKNOWN list survive the session that produced it.

---

## E-12 · Evidence production and closure authority are the same actor

- **Surfaced by:** external review · `owner-3-validation.md` §1
- **Affects:** the validation owner · the quality dimensions
- **Closes when:** the layer that **runs** the checks is separate from the one that **decides**
  what they authorise

**Why it matters.** ⭐ Whoever produces the evidence should not be the one who decides what it
proves. A separate evidence layer answers *"this is what I observed"*; the closure authority
answers *"with this, it closes or it does not"*. ⚠️ Merged, an agent can satisfy the bar by
choosing what to measure — and the bar was the only thing stopping it from declaring itself done.

---

## E-13 · No level is declared for the evidence a block needs

- **Surfaced by:** `owner-3-validation.md` §5b
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

Related: `README.md` (folder) · `../memory/principles/README.md` (where the owners live) ·
`../rules/README.md` (where a closed entry usually lands) · `../CAPABILITIES.md`.
