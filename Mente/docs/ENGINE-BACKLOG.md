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

Related: `README.md` (folder) · `../memory/principles/README.md` (where the owners live) ·
`../rules/README.md` (where a closed entry usually lands) · `../CAPABILITIES.md`.
