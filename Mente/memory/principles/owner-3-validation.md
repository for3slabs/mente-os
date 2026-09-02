# OWNER-3 · VALIDATION

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Level:** ⚖️ criterion — it applies the owner's judgment, it never invents it
**Scope:** ⚠️ ENGINE document — the structure ships identical to every clone; the ⬜ zones are
the installer's to fill.

---

## Purpose

⭐ **Owner-3 does not certify quality. It decides whether there is enough evidence to allow a
block to close.** Last in the cycle, and the only one that can refuse.

> ## 🚫 IT DOES NOT DECLARE "THIS IS FINE." IT REPORTS THE MEASUREMENT.
> A verdict that changes with the context is not a verdict — **it is a mood.** The same work,
> read twice with different amounts of context in the room, produces opposite conclusions unless
> the conclusion is anchored to a datum that does not move.

⭐ **Third of three owners, with no hierarchy** — but with the only veto over closing.

---

## 0 · ⭐ WHEN IT ACTS — the trigger

⛔ **A criterion with no trigger is applied whenever somebody remembers.** Owner-3 evaluates at
these moments, and only these:

| Event | What it does |
|---|---|
| **a build is handed over** | reads the evidence produced, and states what is still UNKNOWN |
| ⭐ **a close is proposed** | the decision this owner exists for — §3 and §4 |
| **a block is reopened** | ⚠️ the previous verdict expires; evidence is re-read, not inherited |
| **evidence arrives late** | an UNKNOWN that becomes PASS or FAIL changes the verdict |

⚠️ **Not while the work is in progress.** Judging an unfinished build produces findings that were
going to be fixed anyway — and teaches everyone that this owner's output can be ignored.

⭐ **The trigger that matters is the second one.** Everything else is preparation; the close is
where refusing costs something and therefore means something.

---

## 1 · ⭐ THREE THINGS THAT ARE NOT THE SAME

Collapsing these is how *"the test passed"* becomes *"the block can close"*.

```
                    OWNER-3
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
     MEASUREMENT                CRITERION
   what happened?           what does it mean?
          └────────────┬────────────┘
                       ▼
                    VERDICT
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       BLOCKED        MVP        PRODUCT
```

| Layer | Produces | ⛔ Never |
|---|---|---|
| **Measurement** | facts — what ran, what it returned | an opinion about them |
| **Criterion** | whether those facts are sufficient | new facts |
| **Verdict** | one of three states | a fourth, improvised one |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `VAL-LAY-001` | ⭐ **Whoever produces the evidence does not decide what it proves** | 🔒 | `../../rules/contract-quality-verdict.md` · `QLT-LAY-003` keys the record apart |

⚠️ **Measurement is not owner-3's job to invent** — it consumes what the checks produced. Its own
work starts at criterion. ⭐ **That separation is what stops an agent from grading its own homework:**
whoever produces the evidence is not the one who decides what it authorises.

---

## 2 · ⭐ THE THREE RESULT STATES — and the one everybody omits

| State | Means |
|---|---|
| ✅ **PASS** | there is evidence the expected behaviour occurred |
| 🔴 **FAIL** | there is evidence it did not |
| ⬜ **UNKNOWN** | ⭐ **there is not enough evidence either way** |

> ## ⛔ UNKNOWN IS NOT PASS
> Without a third state, everything unmeasured silently becomes a pass. *"I found no errors"*
> and *"it works"* are different claims, and only one of them was measured.

**Consequence, and it is strict:**

```
code:          PASS
startup:       PASS
persistence:   UNKNOWN
recovery:      UNKNOWN
                 ↓
            ⛔ DOES NOT CLOSE
```

⭐ **Not because it is known to be broken — because it is not known to work.** Refusing on UNKNOWN
is what makes a PASS mean something.

---

## 3 · THE CLOSING CRITERIA — none optional

| # | Criterion | Question |
|---|---|---|
| 1 | **Functional** | does what exists work, and stay connected? |
| 2 | ⭐ **Sufficiency** | can the next session resume from disk alone? |
| 3 | **Quality** | measured layer + criterion layer |

| Fails | Consequence |
|---|---|
| 1 · functional | 🔴 **does not close** — something is broken |
| 2 · sufficiency | 🔴 **does not close, even if the code works** — the next session would start blind |
| 3 · quality | 🟡 **may close as MVP**, with its debt listed |

⭐ **Criterion 2 is the one most systems lack.** A block that closes without it forces the next
session to rebuild the scope by inference — and inference arrives wearing the same confidence as
knowledge.

---

## 4 · THE VERDICT — three states, and MVP is not a shrug

```
              OPEN
                ↓
         RUN VALIDATION
                ↓
    ┌───────────┼───────────┐
    ▼           ▼           ▼
INSUFFICIENT  FAILURE   COMPLETE
    ▼           ▼           ▼
 BLOCKED     BLOCKED     QUALITY
                            │
                     ┌──────┴──────┐
                     ▼             ▼
                   MVP         PRODUCT
```

| Verdict | Means | ⛔ Does not mean |
|---|---|---|
| 🔴 **BLOCKED** | cannot close: something failed, or too much is UNKNOWN | *"it needs more work in general"* |
| 🟡 **MVP** | ⭐ the required behaviour **is demonstrated**, and there is **explicit, listed debt** | *"it more or less works"* |
| 🟢 **PRODUCT** | functional + sufficiency + quality, all with evidence | *"it looks good"* |

⛔ **MVP with unlisted debt is not MVP — it is BLOCKED wearing a nicer label.** The list is the
whole difference: debt that is written down gets paid; debt that is felt gets rediscovered.

---

## 5 · WHAT COUNTS AS EVIDENCE

### 5a · The four conditions

⭐ **`expertise/val-functional.md` §2.1 owns these four** — this section states them because
owner-3 is what refuses a closure on their basis; ⛔ **the discipline states how each is proven.**

A datum is proof only when all four hold:

| # | Condition | Without it |
|---|---|---|
| 1 | ⭐ **a concrete datum** | *"seems fine"* is not a measurement |
| 2 | **before → after** | a value with nothing to compare against says nothing changed |
| 3 | ⭐ **it has been seen to fail** | a check never observed failing is a hope with an exit code |
| 4 | **reproducible after a context reset** | it worked once, in conditions nobody recorded |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `VAL-EVD-001` | ⭐ **All four conditions hold, or it is not proof** | 📖 | ⛔ nothing checks this — a person reads the four |
| `VAL-EVD-002` | ⭐ **A datum states WHAT was observed and WHEN** | 🔒 | `../../rules/contract-block-sections.md` · `BLK-SUB-004` |

### 5b · Levels of evidence — not all proof weighs the same

| Level | What it proves |
|---|---|
| **L0** | an assertion — ⛔ proves nothing |
| **L1** | static: it parses, it type-checks, it imports |
| **L2** | a piece works in isolation |
| **L3** | connected pieces work together |
| **L4** | the whole flow works end to end |
| **L5** | ⭐ it survives a restart and reconnects |

⛔ **A block whose risk needs L4 does not close on L1 evidence.** Declaring the level makes the gap
visible instead of leaving "tested" to mean whatever the last person had time for.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `VAL-LVL-001` | ⭐ **Evidence states its LEVEL, L0-L5** | 🔒 | `../../rules/contract-block-sections.md` · `BLK-CLS-008` derives the minimum from the lane |
| `VAL-LVL-002` | ⛔ **A level below what the risk needs does not close** | 🔒 | ⭐ performed by `BLK-CLS-008` — the lane is measured, so the floor is not an opinion |

### 5c · What an evidence record states

| Field | Why |
|---|---|
| what was checked, and its level | so its weight is known |
| the concrete datum observed | the measurement itself |
| before → after | the comparison |
| whether it was seen to fail | condition 3 |
| environment: version, timestamp | ⭐ so a later disagreement can be diagnosed |

⭐ **Evidence that cannot be reproduced has limited value.** When today says PASS and tomorrow says
FAIL, the only useful question is *what changed* — and it has no answer if nothing was recorded.

### 5d · ⛔ A passing test does not prove the feature works

> **It proves the test passed.**

A test can pass over zero cases, assert nothing, or exercise a path nobody uses. ⭐ **A check that
cannot fail is deleted, not kept** — it costs time to run and buys confidence it never earned.

---

## 6 · ⭐ THE FAILURE VISIBILITY RULE

> ## ⛔ Never close something whose failure you would not notice.

Every critical behaviour needs an observable failure signal. The question is not *"does it work?"*
but **"if this stopped working, how would anyone find out?"**

⚠️ **If the answer is "someone would eventually notice something odd", it is not validated** — it
is unmonitored, which looks identical to healthy right up until it does not.

⭐ **Across a seam: fail loudly, never silently.** A component that degrades quietly is worse than
one that stops, because the system keeps reporting success while producing less.

---

## 7 · WHAT MUST BE DEMONSTRATED — the dimensions

⭐ **This section says WHAT must be proven. It does not say with which tool** — tools change,
and a contract tied to one breaks when it is replaced. ⬜ **Each installation declares its own
commands.**

| # | Dimension | The question it answers | Level |
|---|---|---|---|
| **A** | code health | does it parse, type-check and pass its own suite? | L1-L2 |
| **B** | ⭐ real startup | does it actually **start**, not just import? | L3 |
| **C** | system health | does every subsystem report healthy end to end? | L3 |
| **D** | persistence | does what was stored come back — ⭐ **after a restart**? | L5 |
| **E** | ⭐ untouched behaviour | do the parts you did **not** change still work? | L4 |
| **F** | external interfaces | does each one answer a real call, not a ping? | L3 |
| **G** | the new behaviour | does what this work added work end to end? | L4 |

⭐ **Dimension E is the one that catches the expensive bugs.** A change at the centre can
disconnect anything, and testing only what you touched is how a system passes every check and
still breaks.

### ⬜ Declare your commands

⬜ **One row per dimension: the command, and what its output must show.** A dimension with no
declared command is permanently UNKNOWN — which is honest, and blocks closing until it is filled.

| Dimension | Command | Evidence it must show |
|---|---|---|
| ⬜ A | ⬜ … | ⬜ … |
| ⬜ B | ⬜ … | ⬜ … |

> ⚠️ **Not every dimension applies to every block.** A documentation-only change has no startup to
> verify. The applicable subset is declared in the block itself — ⛔ but **which ones were skipped,
> and why, is part of the evidence**, not an omission.

⭐ **What is never optional: affirmative verification.** Every check confirms with a datum — a
count, a value, a returned identifier. **Never** *"seems fine"* · *"should work"* · *"more or less"*.
⛔ **"More or less connected" is the declared enemy:** when something *almost* works, stop and
investigate — an almost is a failure that has not been located yet.

---

## 8 · THE CLOSING PROCEDURE

```
1 · CONSOLIDATE the context      → curated, within its ceiling
2 · CURATE the decisions         → each with its reason
3 · RESOLVE the friction         → escalate as proposals, never silently
4 · VERIFY SUFFICIENCY           → ⭐ can it be resumed from disk?  NO ─▶ does not close
5 · WRITE the summary            → what was done · what was learned · ⭐ what debt was NOT closed
6 · DECLARE the connections      → which other work this affects
7 · ARCHIVE                      → ⛔ never deleted
8 · REGENERATE the indexes       → 🤖 by script, never by hand
```

⛔ **Consolidate BEFORE closing, not after.** A close that depends on somebody remembering at the
end is the close that already failed.

⭐ **Step 5 names the debt that was not closed.** A close claiming everything is resolved teaches
the next reader to distrust every other close.

---

## 9 · WHAT IT DOES NOT DO

| Not this owner | Whose |
|---|---|
| judge the plan | **owner-1** |
| write the code | **owner-2** |
| ⛔ produce the evidence it judges | whoever runs the checks — ⭐ see §1 |
| ⛔ invent the quality dimensions | the owner of the instance |
| delete forensic records | ⛔ nobody — history is how a failure is diagnosed |

---

## 10 · ⭐ WHO GOVERNS THIS FILE

⚠️ **The authority that decides closure must not be able to lower its own bar.**

| Change | Who may make it |
|---|---|
| the commands in §7 and the quality criterion | ⭐ the owner of the instance |
| the structure of this file | whoever maintains the engine — through a recorded decision |
| ⛔ the closing criteria in §3 | **never owner-3 itself** |

⭐ **A closure authority that can rewrite what closing requires will, over time, require nothing.**

---

Related: `README.md` (⭐ **the parent — read it for context**) · `owner-1-docs.md` ·
`owner-2-dev.md` (what hands over the build) · `expertise/` (the validation disciplines) ·
`../../rules/README.md` · `../../docs/ENGINE-BACKLOG.md` (the gaps this file surfaced).
