# OWNER-1 · DOCUMENTATION

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Level:** ⚖️ criterion — it applies the owner's judgment, it never invents it
**Scope:** ⚠️ ENGINE document — the structure ships identical to every clone; the ⬜ zones are
the installer's to fill.

---

## Purpose

Owns whether a document or a plan is **fit to be part of the system**. Not whether it is
well-written or pleasant to read — whether it can be found, executed, audited and maintained
after the session that produced it is gone.

> ⭐ **What this owner actually prevents:** not ugly documentation — **knowledge decay**. A system
> whose documents cannot be trusted has to re-derive everything from the code, and re-derivation
> is where a wrong assumption enters wearing the same confidence as a fact.

⭐ **First of three owners, with no hierarchy over the other two.** The numbering is a reading
order, not a chain of command. Each rejects within its own domain, and a piece must satisfy all
three.

---

## 1 · WHAT IT OWNS — two dimensions, not one

It is tempting to say this owner governs "form". It governs more than that, and saying so
prevents the argument *"that is not Documentation's business"* from ever being valid.

| Dimension | Question | What it covers |
|---|---|---|
| **FORM** | *is it shaped like a document of the system?* | header · type · naming · size · section structure |
| **INTEGRITY** | *can it be trusted and acted on later?* | executability · verifiability · evidence · pointers · declared limits |

| Responsibility | Contract | Enforced by |
|---|---|---|
| The shape of every document | `../../rules/contract-document.md` | `../../bin/check-document` |
| The shape of every block | `../../rules/contract-block.md` + its sections half | `../../bin/check-block` |
| The shape of every decision record | `../../rules/contract-adr.md` | `../../bin/check-decisions` |
| Naming of files and folders | ⭐ `DOC-NAM-*`, inside the document contract | `../../bin/check-document` |
| Size limits per type | ⭐ the ceiling table, `DOC-SIZ-001..003` | `../../bin/check-document` |

⭐ **Naming has no file of its own on purpose:** a name is a field of a document the way its
header is, and splitting it out would leave two contracts able to disagree about one file.

---

## 2 · ⭐ WHEN IT ACTS — the trigger contract

A criterion with no trigger is a criterion applied whenever someone remembers. This owner
evaluates a document at these moments, and only these:

| Event | Why here |
|---|---|
| **created** | the cheapest moment to fix a shape |
| **structurally modified** | sections added, removed or reordered |
| **split or merged** | ⭐ the halves must point at each other, or one becomes unreachable |
| **renamed or moved** | its pointers now lie |
| **marked `current`** | that word is a claim, and §4 defines what it claims |
| **closed / archived** | last chance before it stops being edited |

⛔ **Not on every keystroke, and not only at review time.** A gate that fires constantly gets
switched off; one that fires only at the end finds problems when they are most expensive.

---

## 3 · THE FOUR VERDICTS

⭐ **The distinction that matters most is REJECT vs PENDING.** They look similar and are opposite
problems: one says *this is wrong*, the other says *nobody knows yet*. Collapsing them either
blocks work that cannot proceed, or hides a hole as if it were resolved.

| Verdict | Means | What happens next |
|---|---|---|
| ✅ **PASS** | meets every contract that applies | it proceeds |
| ⚠️ **WARN** | an anomaly that breaks no contract | recorded, does not block |
| 🔴 **REJECT** | ⛔ violates an existing contract | it does not proceed until fixed |
| ⬜ **PENDING** | ⭐ a criterion is **missing**, not broken | filed as a pending item, assigned to whoever owns the criterion — **it never stops the work** |

⛔ **PENDING is never used to avoid a REJECT.** A violated contract is not an open question; it
is a violation. Using PENDING as a soft REJECT turns the pending list into a place where problems
go to be forgotten politely.

---

## 4 · WHAT EACH STATUS CLAIMS

`Status:` is not a label — each value is a claim someone can be held to. The values themselves and
their transitions will live in the document contract (⬜ `rules/`); what follows is what this
owner verifies
before accepting one.

| To claim | The document must |
|---|---|
| `draft` | carry a header · nothing else is demanded yet |
| ⭐ `current` | ① a complete header · ② a `Type` that exists in the table · ③ content within that type's limit · ④ every pointer resolving to something that exists |
| `superseded` | **name its replacement** — a superseded document with no successor is a dead end |
| `fossil` | be frozen, and say why it is kept |

⭐ **`current` is the only one that costs something to claim**, and that is deliberate: it is the
word that tells a reader *"act on this"*.

---

## 5 · WHAT IT REJECTS

### 5a · Structural — ship with the engine

⭐ **Owner-1 rejects; its two disciplines say on what basis.** `expertise/doc-planning.md` owns
whether a plan can be executed; `expertise/doc-structure.md` owns where knowledge lives. ⛔ **A
rejection with no discipline behind it is a preference** — see §9.

These do not depend on anybody's taste: each is a consequence of a contract that travels with the
engine, and each names what verifies it.

| 🔴 Rejected | Why | Verified by |
|---|---|---|
| a document with no header (`Status` · `Type` · `Updated` · `Owner`) | nothing can audit what does not identify itself | `bin/check-block` |
| a `Type` that is not in the table | nobody knows which limit applies | `bin/check-block` |
| a file over the limit for its type | ⭐ see §6 — the limit must be measurable | `bin/check-health` |
| a pointer that resolves to nothing | ⚠️ the cost of replacing duplication with references | ⬜ `bin/check-links` |
| a duplicated table instead of a pointer | ⭐ two copies of one truth diverge, and neither is marked wrong | ⛔ **nothing yet** |
| section numbering with `-bis` / `-ter` | the smell that says *split me* | ⛔ **nothing yet** |
| a claim with no evidence | `owner-0-voice.md` | ⛔ **nothing yet** |

⚠️ **The three rows with no verifier are honest, not pending work.** A criterion that no script
checks is followed roughly half the time — knowing which half is which is the point of the column.

### 5b · ⬜ YOURS — what this installation also rejects

⬜ **Add the criteria your own work has taught you.** One row each: what is rejected, why, and
what verifies it (or ⛔ nothing yet).

> ⭐ **Do not let an AI fill this in.** An invented criterion reads exactly like a real one and
> silently becomes the standard everyone is measured against. An empty row is visible and gets
> filled; an invented one never does.

**The questions that elicit it — answer with real cases, not principles:**

1. What is the last document you had to rewrite, and what was wrong with it?
2. What do you always look for first when someone hands you a plan?
3. What have you seen go wrong *because* a document was trusted?
4. What would make you say *"this cannot go in"* without hesitating?

---

## 6 · SIZE — the limit needs a unit

⛔ **A ceiling with no declared unit is not a limit.** "Too long" is an opinion; a number with a
unit is a measurement. Declare both in the size table, and use the same unit everywhere.

⭐ **The unit is `lines`, and it is declared in the ceiling table** of
`../../rules/contract-document.md` — countable with one command, stable across editors, and
independent of how the text is wrapped.

⛔ **`DOC-SIZ-003` verifies that the unit is written AND that it is the one measured.** ⚠️ It was
written for a long time and never checked: the reader took the digits and discarded the word
beside them, so a row saying `250 words` would still have been measured in lines — the table
claiming one thing and the check doing another, both looking correct.

⭐ **Over the ceiling, the answer is SPLIT, not "trim".** Trimming removes content to satisfy a
number; splitting keeps it and gives it a home. ⚠️ **And the halves must point at each other** —
a split that leaves one side unreferenced has not divided a document, it has lost half of one.

---

## 7 · A PLAN — the default sections

Every plan is born with these. **The contract is a floor, not a ceiling:** a plan that discovered
something the shape did not anticipate should say so — forcing it back hides the finding.

| # | Section | Why |
|---|---|---|
| 1 | Purpose | if it needs three paragraphs, the plan does two things |
| 2 | ⭐ Why this order | ⚠️ the one most often skipped — without it, the next person reorders the work and undoes the reasoning silently |
| 3 | Phases and deliverables | each with who carries it |
| 4 | What can go wrong | the early signal, and the response |
| 5 | What this plan does NOT do | the boundary |

⛔ **No phase called "polish".** It has no completion criterion, so it never ends and nothing
verifies it. Name what is being polished, and it becomes a phase that can close.

---

## 8 · WHAT IT DOES NOT DO

| Not this owner | Whose |
|---|---|
| judge whether the code is good | **owner-2** |
| verify the system still works | **owner-3** |
| ⛔ **invent criterion** | the owner of the instance — never the AI |
| decide how a change propagates | the propagation rule |

---

## 9 · ⭐ WHO GOVERNS THIS FILE

⚠️ **An owner that validates its own contract is a circular authority.** This file is not exempt
from the criteria it declares, and it is not the one that judges whether it meets them.

| Change | Who may make it |
|---|---|
| the criteria in §5b | ⭐ the owner of the instance |
| the structure of this file (§1-§9) | whoever maintains the engine — through a recorded decision |
| this file's own compliance with §5a | ⭐ **the same validators as any other document** |

⛔ **A criterion is never added by the party it would judge.** If this owner could write its own
acceptance criteria, "acceptable" would converge on "whatever it already does".

---

Related: `README.md` (⭐ **the parent — read it for context**) · `owner-0-voice.md` (transversal) ·
`owner-2-dev.md` · `owner-3-validation.md` · `expertise/doc-planning.md` ·
`expertise/doc-structure.md` · `../../rules/README.md` (⬜ where its four contracts will live).
