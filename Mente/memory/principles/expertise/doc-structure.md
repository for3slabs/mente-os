# EXPERTISE · DOC-STRUCTURE

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Branch of:** `../owner-1-docs.md` — documentation form
**Level:** ⚖️ criterion · ⭐ **the engine's base standard**, extensible by the installation
**Scope:** ⚠️ ENGINE document — §0 to §2 and §4 to §7 ship identical; §3 is yours.

---

## 0 · WHAT THIS FILE IS

> ## ⭐ A document is good when it can be found, dated and trusted months later.

That is a different question from whether a plan can be executed. ⭐ **Its sibling governs whether
work is doable; this one governs where knowledge lives** — and a defect here does not produce a bad
document. ⛔ **It produces two truths, with nothing to say which one wins.**

### Two things live here, and they must never be confused

| | |
|---|---|
| **§2 · BASE STANDARD** | the engine's criterion. Ships filled in. ⛔ Do not edit it in an instance |
| **⬜ §3 · YOURS** | what this installation adds. ⭐ **Extend here, never by rewriting §2** |

### ⭐ ABOUT THIS FILE'S OWN SIZE — the rule applies to it too

⚠️ **An engine file is a standard, and a standard ships whole.** The ceiling governs a document as
it is *used*: when an installation extends it in §3 and it grows past the declared ceiling, ⭐ **it
splits then, by the rules below.**

⛔ **This is not an exemption.** The rule holds; what differs is the moment it applies. ⭐ **A
standard that arrived pre-split would ship two halves of one criterion** — and the reader would
have to reassemble it before using it.

---

## 1 · THE FOUR FIGURES — and the difference decides everything

⛔ **The original mistake is treating all written knowledge as "a document".** It is not:

| Figure | Is | ⭐ The test |
|---|---|---|
| **document** | persistent knowledge with its own identity | ⭐ **will it be read more than once?** |
| **section** | knowledge that belongs inside an existing document | is there already a document it fits in? |
| **memory** | information tied to a moment | ⛔ it will not be consulted again |
| ⭐ **source of truth** | **the document others cite to settle a disagreement** | ⚠️ see §2.1 — ⛔ **declared, never deduced** |

⭐ **Getting the figure wrong is more expensive than getting the content wrong.** Content can be
corrected; a fragment filed as a document acquires a header, an owner, a date, an index entry —
and a maintenance cost paid forever for something that had a home already.

---

## 2 · THE BASE STANDARD

### 2.1 · Where a document lives, and when it becomes two

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `DS-ARC-001` | ⭐ **Two distinct subjects → two documents** | 🟠 | can you name what it is about in one sentence, with no "and"? |
| `DS-ARC-002` | **Two different people maintain it → two documents** | 🟠 | two reasons to change it means two pieces |
| `DS-ARC-003` | ⭐ **Over its declared ceiling → it splits.** ⛔ Not a warning — a pending split | 🔴 | measure it against the ceiling its type declares |
| `DS-ARC-004` | ⭐ **The halves point at each other** | 🔴 | ⚠️ see below — this is the one that gets skipped |

⭐ **`DS-ARC-004` is not a formality.** A split that leaves an orphan trades one problem for a
worse one: **the reader finds half the answer and has no way to know the other half exists.**

#### ⭐ HOW TO SPLIT — the rule that stops a split from causing the damage it prevents

⚠️ **A bad split creates the divergence it was meant to avoid.** Cutting by size alone leaves the
same subject in two files, and they drift apart from the first edit.

| # | Rule | ⛔ Otherwise |
|---|---|---|
| 1 | ⭐ **Cut by SUBJECT, never by length** | two halves of one subject diverge |
| 2 | **Each half is complete on its own subject** | the reader has to open both to understand either |
| 3 | ⭐ **Nothing is duplicated across the halves** | ⚠️ the copied part is the part that will drift |
| 4 | **Each half declares the other, and why the cut is where it is** | the next person re-splits differently |
| 5 | ⭐ **Everything that pointed at the original now points at the right half** | a pointer that resolves to the wrong half is worse than a broken one |

⭐ **Rule 3 is the one measured to fail.** A split that leaves shared content produces two documents
saying the same thing — which is precisely what §2.3 forbids, created by the act of obeying §2.1.

#### ⛔ THE ONE EXCEPTION — a source of truth is not split by size

⭐ **A source of truth is the document others cite to settle a disagreement.** Splitting it creates
a second authority, and *"which of the two is true?"* is exactly the ambiguity it exists to remove.

| | Why size must not govern it |
|---|---|
| **splitting creates a second authority** | ⛔ the next reader has to decide which one wins |
| ⭐ **its value IS its completeness** | it is read to resolve, not to skim. A ceiling optimises reading; this optimises deciding |

> ## ⛔ THE EXCEPTION IS DECLARED, NEVER DEDUCED
> ⚠️ *"It seems important"* is not a criterion — it is the agent granting itself an exemption.
>
> ⭐ **A document claims this in its own header**, naming what it has authority over. **A file with
> no such declaration has no exception, however long or however central it looks.**

⚠️ **Narrow door, not a loophole.** Being long is not being authoritative. ⭐ **The count of files
claiming it should be countable on one hand** — if it grows, the exception has become the rule and
the rule has stopped existing.

### 2.2 · The header — four fields, and each answers a question the reader cannot

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `DS-MET-001` | ⭐ **Status · Type · Updated · Owner — all four** | 🔴 | ⛔ missing one, the document fails its own contract regardless of content |

| Field | The question it answers | ⛔ Missing it means |
|---|---|---|
| **Status** | is this still in force? | you read the whole thing and still do not know |
| ⭐ **Type** | which limits apply? | ⚠️ neither the ceiling nor the required fields can be checked |
| **Updated** | when was this last true? | it is trusted at whatever age it happens to be |
| **Owner** | who keeps it true? | ⭐ nobody updates it, and no alarm fires |

⚠️ **`Type` is the one that fails silently**, because a wrong type does not look wrong: the
document reads fine and the wrong ceiling is applied to it. ⭐ **It is a field whose value silently
changes how everything else is judged.**

### 2.3 · Pointer or copy — the rule is ownership, not shape

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `DS-ABS-001` | ⭐ **If the datum has an owner elsewhere → always a pointer** | 🔴 | who owns this value? Then read it from there |
| `DS-ABS-002` | ⛔ **A live number is never written into prose** | 🔴 | ⭐ a copied number is correct exactly once |

**What MAY be copied — two cases, both bounded:**

| Case | Why it is safe |
|---|---|
| what can no longer change — a closed decision, a historical quote | ⭐ there is no future in which it can diverge |
| ⭐ **the summary, never the detail** | one orienting sentence saves a jump; the full content stays at its source |

⚠️ **Notice what the rule is NOT.** *"Never duplicate a table"* is the obvious rule and it is the
wrong one: ⭐ **a table of things that can no longer change may be copied; a two-line list of live
values may not.** The axis is **who owns the value**, not how the content looks.

⚠️ **This is the rule the other expertise files lean on.** ⭐ When a criterion lives in one of them
and is needed in another, the second **cites it** — `dev-backend.md`, `dev-database.md` and
`val-integration.md` all do exactly that, and none of them restates the rule it borrowed.

⭐ **Why duplication is the worst failure in this discipline:** two copies of one truth diverge, and
**neither looks wrong on its own.** Each reads as correct in isolation. The defect exists only
between them — and nothing reads *between* documents.

### 2.4 · Names — findable six months later

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `DS-NAM-001` | ⭐ **The name states the SUBJECT, never the moment** | 🟠 | ⛔ nobody remembers which Monday |
| `DS-NAM-002` | **A prefix that groups the family** | 🟠 | ⭐ the family should be visible in a directory listing |
| `DS-NAM-003` | ⛔ **No `-v2`, `-final`, `-new`, `-bis`** | 🔴 | see below |

⭐ **`DS-NAM-003` is 🔴 because it is a symptom, not a style preference.** A version in a filename
means two documents exist for one subject and nobody decided which is true — ⚠️ **the divergence of
§2.3, waiting to happen, with the added cost that the reader cannot tell which to trust.**

### 2.5 · What `current` promises

⭐ **`Status: current` is a contract with four terms. Missing one, it promises nothing.**

| # | The reader may assume… | Because the header says |
|---|---|---|
| 1 | ⭐ **somebody verified it, and with what** | ⛔ without this, *current* is an opinion dressed as a state |
| 2 | its date reflects the last real change | ⚠️ an old date with `current` is the fossil signal |
| 3 | its type declares its limits | a wrong type breaks verification silently |
| 4 | someone identified keeps it true | ⭐ a document with no owner ages with no alarm |

⭐ **Term 1 is what separates this from bureaucracy.** The other three are metadata; **this one is
the measurement.** A header claiming `current` without saying who checked it is asserting, not
reporting.

**How to apply it: read only the header.** ⛔ If you cannot say who verified it, when, under which
type and who is responsible, the document fails its own contract — whatever its content says.

### 2.6 · Should it exist at all?

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `DS-NEC-001` | ⭐ **Fits in an existing document → it is a SECTION** | 🟠 | name the document it could be a section of |
| `DS-NEC-002` | ⭐ **Nobody will read it twice → it is a MEMORY** | 🟠 | will this be consulted again? |

⚠️ **The tension with §2.1, and how it resolves:** §2.1 splits what is too large; this rejects what
is too small. ⭐ **Both answer one question: does this deserve its own header, owner and date?**

⛔ **"It would make that file long" is not a reason to create a new one.** That is §2.1's problem
and it already has its own rule — and its own way of splitting.

---

## 3 · ⬜ THIS INSTALLATION'S CRITERIA

⬜ **Add yours here**, using the model of §2 and ⭐ **your own prefix** — for example `DS-OWN-001`.

⬜ **And declare your ceilings:** which types of document exist here, and what limit each carries.
⭐ **Say the unit** — a ceiling with no unit is an opinion, not a limit.

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| ⬜ … | ⬜ … | ⬜ … | ⬜ … |

> ⛔ **Do not let an AI write this section.** ⭐ **The AI asks, you answer with real cases, the AI
> structures.** Never the reverse.

**The questions that elicit it — answer with cases, not principles:**

1. What makes a document useless to you six months later?
2. ⭐ How do you decide a file is too long — by lines, or by something else?
3. What must a header contain for you to trust what it says?
4. What documentation mistake do you see most often?
5. ⭐ **When is a document not worth writing at all?**

---

## 4 · ⛔ NEVER — no exceptions

| # | Never | Why |
|---|---|---|
| 1 | **Write a live number into prose** | ⭐ cite the metric and its source, never the value |
| 2 | ⛔ **Leave a pointer to something that does not exist** | ⭐ a pointer to nothing is worse than none: it reads as a promise |
| 3 | 🔴 **Delete history to make a check pass** | ⭐ see below |
| 4 | 🔴 **Write a secret, not even as an example** | ⚠️ what is written stays in the record — a leaked secret is **rotated**, not deleted |
| 5 | **Duplicate something owned elsewhere** | a duplicate is a pointer waiting to diverge |
| 6 | ⛔ **Grant a size exemption to a document that did not declare one** | ⭐ the exception is declared, never deduced |
| 7 | ⛔ **Resolve a conflict by picking the one that looks right** | ⭐ see §5 |

⭐ **Rule 3 protects the other six.** The moment a check can be satisfied by deleting the evidence
instead of fixing the cause, **every rule in this file becomes optional** — the system starts
measuring what is convenient instead of what is true.

---

## 5 · ⭐ WHEN TWO DOCUMENTS DISAGREE

⛔ **A divergence is not a choice. It is an UNKNOWN with two candidates.**

```
two documents state the same thing differently
        ↓
who OWNS this value?
    ├─ one of them owns it ─▶ that one is right · the other becomes a pointer
    ├─ a source of truth covers it ─▶ ⭐ it decides · both align to it
    └─ nobody owns it ─▶ ⛔ STOP
                          ↓
                    ⭐ the divergence is reported, not resolved
                    declaring an owner is the owner's decision
```

| Step | ⛔ What is not allowed |
|---|---|
| identify who owns the value | ⛔ **picking the one that looks more current** |
| align the rest to the owner | copying the winner into the loser — ⭐ **the loser becomes a pointer** |
| if nobody owns it: report it | ⚠️ **choosing anyway, and creating the third version** |

⭐ **The last row is the one that matters.** An agent that resolves an ownerless divergence is
inventing authority — and it does it invisibly, because the result looks like a fixed document.

---

## 6 · THE STATES A DOCUMENT CAN BE IN

⭐ **Not just valid or invalid** — the state says what to do next.

| State | Means | Next |
|---|---|---|
| ✅ **valid** | meets its contract | nothing |
| ⬜ **pending metadata** | a header field is missing | complete it |
| ⬜ **pending split** | over its ceiling, no declared exception | ⭐ split it by §2.1 |
| ⬜ **pending merge** | too small, belongs in another | make it a section |
| ⚠️ **stale** | claims `current`, dated long ago | re-verify or restate |
| ⚠️ **orphaned** | a pointer resolves to nothing | fix or remove the pointer |
| 🔴 **conflict** | ⭐ two documents disagree | §5 — ⛔ do not resolve alone |
| ⬛ **exempt** | declares its exception in its header | ⚠️ verify the declaration exists |

⛔ **A pending state is not a warning.** ⭐ It names work that has an owner and a next action — and
a pending with neither is just a complaint with a label.

---

## 7 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ §3 — criteria and the ceilings | ⭐ the owner of the instance |
| §1, §2, §4-§6 — the base standard | whoever maintains the engine, through a recorded decision |
| ⛔ granting itself a size exemption | **nobody** — ⚠️ ⭐ see §0: the rule applies to this file too |

---

Related: `README.md` (⭐ **the parent — what a discipline is**) · `doc-planning.md` (its sibling —
⭐ whether a plan can be executed, as opposed to where knowledge lives) · `../owner-1-docs.md` ·
`../owner-3-validation.md` · `../../rules/README.md` (⭐ where the document contract and the
ceilings live).
