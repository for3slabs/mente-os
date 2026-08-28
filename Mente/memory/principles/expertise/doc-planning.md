# EXPERTISE · PLANNING

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Branch of:** `../owner-1-docs.md` — documentation form
**Level:** ⚖️ criterion · ⭐ **the engine's base standard**, extensible by the installation
**Scope:** ⚠️ ENGINE document — §0 to §2 and §4 to §6 ship identical; §3 is yours.

---

## 0 · WHAT THIS FILE IS

> ## ⭐ A plan is good when somebody else can execute it without asking what it meant.

That is a different skill from formatting a document well: ⚠️ **a perfectly formatted plan can
still be impossible to execute.**

⭐ **This is the most consequential of the disciplines**, and the reason is worth stating: the
others govern *whether what was built is well built*. **This one governs what gets built at all.**
⛔ A defect here does not produce bad work — it produces **the wrong work, done well.**

### Two things live here, and they must never be confused

| | |
|---|---|
| **§2 · BASE STANDARD** | the engine's criterion. Ships filled in. ⛔ Do not edit it in an instance |
| **⬜ §3 · YOURS** | what this installation adds. ⭐ **Extend here, never by rewriting §2** |

---

## 1 · ⭐ THE FOUR STATES — and confusing them is the expensive failure

⛔ **These look similar and mean opposite things.** An agent that cannot tell them apart stops work
that could have proceeded, or proceeds on something nobody decided.

| State | Means | ⭐ What it demands next |
|---|---|---|
| ⬜ **UNKNOWN** | ⭐ **it has not been investigated yet** | **investigate it** — this is not a result, it is a to-do |
| 🔴 **BLOCKED** | there is **evidence** it cannot proceed | ⛔ the evidence, named. Not a suspicion |
| 🙋 **PENDING** | it was investigated; the decision is not the agent's | route it (§5) and ⭐ **keep the rest moving** |
| ⬛ **N/A** | it was evaluated and does not apply | say so — ⚠️ **silently skipping and not applying look identical afterwards** |

> ## ⛔ UNKNOWN REPORTED AS BLOCKED IS THE MOST EXPENSIVE MISTAKE HERE
> ⭐ **A false block never announces itself.** The work simply does not happen, and nobody measures
> what did not occur. ⚠️ *"I did not look"* becomes *"it cannot be done"*, and the difference is
> invisible from the outside — the plan reads the same either way.

⭐ **A limit you have not verified is not a limit. It is an assumption in costume.**

---

## 2 · THE BASE STANDARD

### 2.1 · ⭐ When a plan is needed at all

⚠️ **The question nobody asks, and the one an agent answers by itself if nothing says otherwise.**

⛔ **Both failures are real:** planning a one-line correction wastes the session; ⭐ **skipping the
plan on something that needed one is worse** — it happens without declared scope, without a
success criterion, and without approval. **And the agent decides which it is.**

| Signal | Then |
|---|---|
| it touches **more than one** piece, area or discipline | ⭐ **it needs a plan** |
| it cannot be undone with one action | it needs a plan |
| ⭐ **somebody would be surprised by the result** | it needs a plan |
| a decision appears that is not the agent's | it needs a plan — ⛔ or at minimum, a pending |
| one piece, reversible, and the outcome is obvious | ⬜ the owner sets the threshold (§3) |

⭐ **The bottom row is deliberately the owner's.** *"How many pieces does it touch?"* is universal;
*"three or more"* is a preference. ⛔ **But the threshold is declared once, not decided per case** —
a threshold invented each time is not a threshold.

### 2.2 · The shape — one phase, one deliverable

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `PL-SHP-001` | ⭐ **A phase delivers ONE verifiable thing** | 🔴 | if it delivers two, ⛔ which one failed when something breaks? |
| `PL-SHP-002` | ⭐ **Each phase declares which others it depends on** | 🔴 | the dependency graph is **written, never inferred** |
| `PL-SHP-003` | **A phase too large is split** — see the signals below | 🟠 | walk them one by one |
| `PL-SHP-004` | ⚠️ **A phase too small is merged** — see below | 🟠 | does it have an independent deliverable? |

⭐ **`PL-SHP-002` buys something people miss:** what depends on nothing can run in parallel — **and
that is only visible if it was declared.** An undeclared graph is a sequence somebody guessed.

**A phase is too LARGE when — any one is enough:**

| # | Signal | Why |
|---|---|---|
| 1 | ⭐ it does not fit in one session without losing context | context exhaustion degrades judgement before it stops work |
| 2 | it touches pieces that cannot be reverted together | undoing needs N coordinated changes — ⛔ it was never one phase |
| 3 | ⭐ **its success criterion needs an "and"** | one sentence, or it is two phases |
| 4 | nobody can execute it without asking the owner | ⚠️ a decision appearing mid-execution means the cut was wrong |

**A phase is too SMALL when — any one is enough:**

| # | Signal | Why |
|---|---|---|
| 1 | it has no deliverable of its own | ⛔ *"open the file"* is a step, not a phase |
| 2 | it cannot fail independently | if it can only fail with the next one, it **is** the next one |
| 3 | ⭐ removing it changes nothing about the execution | it exists to show progress, not to produce it |

⭐ **Both limits matter.** Over-splitting is not caution — it is ceremony that hides how much is
actually being delivered.

### 2.3 · What the plan states as fact

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `PL-FCT-001` | ⭐ **Every limit or block the plan declares is measured** | 🔴 | ⛔ where is the observation? |
| `PL-FCT-002` | **The starting state is measured** — what exists today, what fails today | 🔴 | ⭐ without a measured BEFORE, nothing proves the plan improved anything |
| `PL-FCT-003` | **Who consumes what will change is measured, never recalled** | 🟠 | mentions and real uses are different numbers |
| `PL-FCT-004` | **A piece the plan reuses is confirmed to exist and to do what is expected** | 🟠 | ⛔ planning on a function you believe exists is planning on smoke |

⚠️ **`PL-FCT-001` fails silently, which is why it is 🔴.** A plan that reports a block without
measuring it has the same defect as a check reporting green without measuring — one level up, and
harder to catch, because nobody audits work that never started.

### 2.4 · Names — what a phase delivers

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `PL-NAM-001` | ⭐ **The name says what it DELIVERS, not what it is made of** | 🟠 | ⭐ **read only the phase names.** Can you say what the plan produces? |
| `PL-NAM-002` | ⛔ **No phase called "polish", "improvements" or "cleanup"** | 🔴 | a name that does not say what it delivers hides undefined scope |

⭐ **`PL-NAM-002` is 🔴 for a specific reason: undefined scope cannot be approved.** There is
nothing concrete to say yes to, so the approval is a formality — and everything that lands inside
that phase arrived without one.

### 2.5 · The contract — a success criterion carries four things

⭐ **This is the handover point of the whole system.** What is written here is what
`val-functional.md` will later be asked to prove — ⛔ **a criterion that cannot be measured cannot
be validated**, and the gap only becomes visible at closing time, when it is expensive.

⛔ **Fewer than four and the phase is not planned, only named.**

| # | Must state | ⛔ Not enough |
|---|---|---|
| 1 | ⭐ **a concrete datum, measurable afterwards** | *"it works"* |
| 2 | **how it is verified** — the exact operation | *"run the tests"* — ⚠️ whoever executes invents their own |
| 3 | ⭐ **what failure would look like** | silence — a failure nobody would notice |
| 4 | ⭐ **who approves it** | ⛔ empty, which lets the executor approve itself |

**Requirement 3 is the closing rule moved earlier in time:** *never close something whose failure
you would not notice* — asked **before building**, not at the end. ⭐ **If the plan cannot say what
a failure looks like, the phase has no way of being wrong — and something that cannot be wrong
cannot be verified.**

### 2.6 · ⭐ Success is not acceptance

| | Answers | Decided by |
|---|---|---|
| **success** | did it do what was specified? | ⭐ measurable — a check can say |
| **acceptance** | is this what was wanted? | ⛔ **judgement — a person says** |

⭐ **A green check does not mean the owner agrees.** It means the thing that was specified
happened. ⚠️ Merging the two lets the executor conclude, from a passing test, that the intent was
met — and intent was never what the test measured.

**A phase declares both when they differ.** When they are the same, say so — that is a statement,
not an omission.

### 2.7 · Necessity

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `PL-NEC-001` | ⭐ **A phase that changes nothing about the outcome is removed, not shrunk** | 🟠 | remove it and describe the end result. Same? It was filler |

⚠️ **Filler in a plan is not harmless.** It consumes the session that signal 1 of §2.2 exists to
protect — ⭐ **a phase that delivers nothing still spends context, and context is the resource
whose exhaustion degrades everything after it.**

### 2.8 · Boundaries and order

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `PL-BND-001` | ⛔ **The plan says what will NOT be touched** | 🔴 | ⭐ without a written boundary, an agent expands on its own |
| `PL-BND-002` | ⭐ **The plan says WHY this order** | 🔴 | ⚠️ an order with no reason cannot be argued with — and therefore cannot be corrected |
| `PL-BND-003` | **Where a change spans several areas, the order within it is declared** | 🟠 | ⭐ producers before strict consumers — ⛔ never *"whatever is fastest first"* |

---

## 3 · ⬜ THIS INSTALLATION'S CRITERIA

⬜ **Add yours here**, using the model of §2 and ⭐ **your own prefix** — for example `PL-OWN-001`.

⬜ **And declare your threshold for §2.1:** at how many pieces, or under what condition, does work
require a plan in this installation?

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| ⬜ … | ⬜ … | ⬜ … | ⬜ … |

> ⛔ **Do not let an AI write this section.** ⭐ **The AI asks, you answer with real cases, the AI
> structures.** Never the reverse.

**The questions that elicit it — answer with cases, not principles:**

1. What do you demand of a plan before approving it?
2. ⭐ What makes you reject one outright?
3. How do you know a phase is too big **before** it runs?
4. What has to be written for you to trust the order of the phases?
5. What planning mistake do you see most often, and which one annoys you most?
6. ⭐ **When is a plan finished, as opposed to merely long?**

---

## 4 · ⛔ NEVER — no exceptions

| # | Never | Why |
|---|---|---|
| 1 | ⭐ **Build without explaining and without approval** | explain → approve → execute. ⛔ The middle step is not optional |
| 2 | **A global plan instead of one per piece** | ⚠️ but see below — *per piece* needs a grouping rule |
| 3 | ⛔ **Leave a gap for the owner that could have been derived** | ⭐ a gap the agent could have closed by reading is not a decision: it is unfinished work handed over as one |
| 4 | **Decide something that was the owner's to decide** | ⛔ the plan sets a criterion instead of asking |
| 5 | ⭐ **Omit something because it seems already covered** | judging what is redundant is itself a criterion, and being wrong deletes something useful silently |
| 6 | ⭐ **Omit something because the reader "already knows it"** | ⚠️ the same failure as 5: the agent deciding what does not need saying |
| 7 | ⛔ **Justify with "I thought it was like that" or "I did not know"** | *"I did not know"* is not an excuse — it is a confession that a question was not asked |

### ⚠️ Rule 2 needs its counterweight: what groups a plan

⭐ *"One plan per piece"* with no grouping rule produces ten plans nobody coordinates.

**A change that spans several areas is ONE unit with several phases** — never several plans that
happen to be related. ⛔ **Splitting by area is how one half ships and the other does not** — and
the join between them is where the expensive defects live.

### ⭐ Rules 6 and 7 are one rule, and it is about behaviour

**A plan never depends on what the reader already knows, and is never explained afterwards by
saying it was not known.** Both are the agent deciding, alone, what did not need to be said or
verified — when asking would have cost one question.

---

## 5 · ⭐ A REAL GAP IS ROUTED, NEVER USED AS A REASON TO STOP

⛔ **This is the counterweight to rule 3.** Rule 3 forbids inventing a gap out of laziness; this
one says a genuine gap is routed. **Together: derive what you can, ask what you cannot, and keep
going with the rest.**

| Requirement | ⛔ Not enough |
|---|---|
| **filed** where open items live | ⚠️ a note inside a file nobody opens |
| **assigned by name**, with the decision in one line | ⛔ *"pending"* with no owner — that is abandoned, not pending |
| ⭐ **everything that does NOT depend on it keeps moving** | stopping the whole plan over one decision |

⭐ **The third is the one usually missing**, and it is the one that decides whether a pending costs
a question or costs a week.

---

## 6 · ⭐ PLAN DELTA — when reality changes an approved plan

⚠️ **"The contract is a floor, not a ceiling"** means a plan that discovers something says so.
⛔ **It does not mean the agent may quietly rewrite what was approved.**

```
a discovery appears mid-execution
        ↓
   does it change scope, order, or a criterion?
    ├─ no  ─▶ record it and continue
    └─ yes ─▶ ⛔ STOP that path only
                ↓
           PLAN DELTA:
           what changed · why · which phases · whether approval is needed
                ↓
           ⭐ everything independent keeps moving
```

| The delta states | Why |
|---|---|
| **what changed** | against the approved version, not against intent |
| ⭐ **why** — the evidence that forced it | ⛔ *"it turned out to be necessary"* is not evidence |
| **which phases it affects** | so the graph is recomputed, not assumed |
| ⭐ **whether it needs re-approval** | ⚠️ scope and criteria do; an implementation detail may not |

⭐ **Without this, an approved plan silently becomes a different plan** — and the approval that was
given no longer corresponds to the work being done. ⛔ **Nobody notices, because the document still
says "approved".**

---

## 7 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ §3 — criteria and the plan threshold | ⭐ the owner of the instance |
| §1, §2, §4-§6 — the base standard | whoever maintains the engine, through a recorded decision |
| ⛔ lowering a 🔴 to 🟠 locally | **nobody** — ⚠️ log the friction and propose it |

---

Related: `README.md` (⭐ **the parent — what a discipline is**) · `doc-structure.md` (its sibling —
⭐ how a document is written, as opposed to whether a plan can be executed) · `../owner-1-docs.md` ·
`../owner-2-dev.md` (⭐ what receives the plan, and returns it) · `../owner-3-validation.md`.
