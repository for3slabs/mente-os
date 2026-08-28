# EXPERTISE · VAL-FUNCTIONAL

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Branch of:** `../owner-3-validation.md` — functional validation
**Level:** ⚖️ criterion · ⭐ **the engine's base standard**, extensible by the installation
**Scope:** ⚠️ ENGINE document — §0 to §2 and §4 to §6 ship identical; §3 is yours.

---

## 0 · WHAT THIS FILE IS

> ## ⭐ The criterion for PROVING something works, as opposed to believing it does.

⚠️ **The failure this exists to prevent:** the same work, read twice with different amounts of
context, producing opposite verdicts. ⭐ **A verdict that changes with the context is not a
verdict — it is a mood.** This file is what makes a verdict reproducible.

### Two things live here, and they must never be confused

| | |
|---|---|
| **§2 · BASE STANDARD** | the engine's criterion. Ships filled in. ⛔ Do not edit it in an instance |
| **⬜ §3 · YOURS** | what this installation adds. ⭐ **Extend here, never by rewriting §2** |

### ⭐ Two questions, not one

| | Asks | Section |
|---|---|---|
| **validation** | does it work **now**? | §2 |
| ⭐ **detection** | ⚠️ **how will anyone know when it stops?** | §5 |

⭐ **The second matters more in a system that runs unattended.** A validation that passes today
with nothing watching tomorrow is a photograph, not a guarantee.

---

## 1 · ⭐ THE THREE VERDICTS

| Verdict | Means | ⭐ What it demands |
|---|---|---|
| ✅ **PASS** | it ran, and the evidence satisfies the criterion | nothing |
| 🔴 **FAIL** | it ran, and the evidence **contradicts** the criterion | ⭐ **fix something** |
| ⬜ **NOT_MEASURED** | ⛔ **it did not run, or had no subjects to measure** | ⭐ **measure something** |

> ## ⛔ NOT_MEASURED IS NOT A PASS — AND IT IS NOT A FAIL EITHER
> ⭐ **They are opposite problems.** A FAIL says *something is broken*; a NOT_MEASURED says
> *nothing was checked*. ⚠️ **Collapsing them sends someone to fix what only needed measuring** —
> and treating it as a pass hides the gap entirely.

⛔ **A verdict built on passes whose measured count is zero is NOT_MEASURED, never PASS.**

⚠️ **The failure that forces this:** an empty scope returns zero broken things — zero dead files,
zero broken pointers, zero duplication. **Every metric green, none of them run.** ⭐ **Absence of
evidence rendered as evidence.**

---

## 2 · THE BASE STANDARD

### 2.1 · ⭐ What counts as proof — the four conditions

⛔ **All four. Not a menu.**

| # | Condition | ⭐ Why it cannot be faked |
|---|---|---|
| 1 | **a concrete datum the system returned** | ⭐ you cannot produce it without running the system |
| 2 | **a measured BEFORE and AFTER** | ⚠️ a final number alone proves nothing changed — *"0 broken"* may always have been 0 |
| 3 | ⭐ **the check has been SEEN to fail, deliberately** | a check only ever seen green has not been tested |
| 4 | **reproducible after a context reset** | ⭐ if the result changes when the context is lost, it was an impression |

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `VF-EVI-001` | ⭐ **All four conditions hold, or it is not proof** | 🔴 | which one is missing? |
| `VF-EVI-002` | ⛔ **Absence of evidence is not evidence** | 🔴 | ⭐ what was the measured subject count? |

⭐ **Condition 3 is the one that separates a check from a hope.** A check that cannot be shown
failing is a check nobody has verified — and its green means only that it ran.

### 2.2 · ⭐ Scope integrity — did it measure what it claimed to?

⚠️ **A command can succeed perfectly and validate nothing.** The subject was never there.

```
expected subjects: 20        measured: 0
                ↓
       ⛔ NOT_MEASURED — not a pass
```

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `VF-SCP-001` | ⭐ **The check declares how many subjects it EXPECTED** | 🔴 | ⛔ without an expected count, `measured: 0` looks correct |
| `VF-SCP-002` | **It reports how many it actually measured** | 🔴 | the two numbers, side by side |
| `VF-SCP-003` | ⭐ **Expected ≠ measured is a finding**, not a detail | 🔴 | ⚠️ investigate before reading the result |

⭐ **This is the cause behind the green-over-zero symptom.** Reporting the measured count exposes
it; **declaring the expected count is what makes a mismatch visible at all.**

### 2.3 · One check proves one thing

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `VF-ONE-001` | ⭐ **State in ONE sentence what the check proves** | 🟠 | ⛔ if the sentence needs an "and", it is two checks |

⭐ **Two failures come from the same defect:** a green can hide an unexercised path, and a red does
not say which of the two things broke. **The check stopped being a measurement and became a
summary.**

### 2.4 · How deep the test must go

| Level | Proves |
|---|---|
| **L0** | an assertion — ⛔ proves nothing |
| **L1** | static: it parses, it resolves |
| **L2** | a unit works in isolation |
| **L3** | connected pieces work together |
| **L4** | the whole flow works end to end |
| **L5** | ⭐ it survives a restart and reconnects |

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `VF-LVL-001` | ⭐ **Choose the minimum sufficient level — never below what the behaviour requires** | 🔴 | which level does this behaviour demand? |
| `VF-LVL-002` | **A unit test suffices for pure, deterministic logic — and only that** | 🟠 | does it touch state, a network, storage, or another process? |
| `VF-LVL-003` | ⛔ **Anything crossing a boundary needs the real thing** | 🔴 | ⭐ a unit test proves your function, not the wire |
| `VF-LVL-004` | ⛔ **Anything touching real user data is tested against reality** | 🔴 | what is at stake if the substitute behaves differently? |

> ## ⭐ THE DECISION RULE
> **Ask what the test would still prove if the substitute were wrong.** ⛔ If the answer is
> *"nothing"*, **the substitute IS what is being tested** — and the test is circular.

### 2.5 · A failing check must be actionable without opening the code

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `VF-MSG-001` | ⭐ **Name WHAT broke, not that something broke** | 🟠 | ⛔ *"validation failed"* names nothing |
| `VF-MSG-002` | **Expected versus obtained, always** | 🟠 | ⚠️ without it, you read the source to understand the failure |
| `VF-MSG-003` | ⭐ **Point at the rule that justifies it** | 🟠 | can the reader find out *why* this is required? |

⭐ **`VF-MSG-003` is what keeps a check alive.** A check whose reason nobody can find gets deleted
or weakened the first time it is inconvenient. **Citing its source turns a red from an obstacle
into a finding.**

**How to apply it: read only the error message, with no access to anything else.** ⛔ If you cannot
say what to fix, the check fails this dimension however correct its logic.

### 2.6 · ⭐ Does this check deserve to exist?

⛔ **A check meeting any of these is deleted. Not kept "just in case".**

| # | The check… | ⭐ Why it goes |
|---|---|---|
| 1 | **cannot fail — ever** | if no state of the world turns it red, ⛔ it does not measure: it decorates |
| 2 | **is fully covered by another** | two checks that always go red together — one is noise |
| 3 | ⭐ **measures the FORM, not the effect** | it confirms a file exists or a line is written, not that the rule holds |

⭐ **The reason is not tidiness: a check that cannot fail manufactures false confidence, and false
confidence is worse than a known gap.** A gap can be seen; a green that means nothing cannot.

⚠️ **The honest consequence, because it cuts both ways:** deleting reduces the check count, and the
count looks like progress. ⛔ **The count is not the metric.** ⭐ **A battery of 200 checks where 40
cannot fail is weaker than one of 160 where all can.**

**How to apply it: before defending a check, try to make it fail.** ⭐ If you cannot construct the
failure it claims to detect, **that is the finding — and the finding is to delete it.**

---

## 3 · ⬜ THIS INSTALLATION'S CRITERIA

⬜ **Add yours here**, using the model of §2 and ⭐ **your own prefix** — for example `VF-OWN-001`.

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| ⬜ … | ⬜ … | ⬜ … | ⬜ … |

> ⛔ **Do not let an AI write this section.** ⭐ **The AI asks, you answer with real cases, the AI
> structures.** Never the reverse.

**The questions that elicit it — answer with cases, not principles:**

1. What do you require before believing something works?
2. ⭐ **What makes you distrust a green?**
3. Which datum counts as proof, and which only looks like one?
4. When is a unit test enough, and when does only the real thing count?
5. What must be true before something reaches production?
6. ⭐ **What would you rather see fail loudly than pass silently?**

---

## 4 · ⭐ PROVING A CHECK CAN FAIL

⛔ **"It has been seen to fail" is a requirement, and requirements need a procedure.**

| # | Step | ⚠️ Watch out |
|---|---|---|
| 1 | **state what failure it claims to detect** | ⭐ if you cannot state it, the check has no purpose |
| 2 | **introduce exactly that failure** — the smallest version of it | ⛔ not a different one that also breaks things |
| 3 | **run the check** | it must go red |
| 4 | ⭐ **confirm the message names the real cause** | ⚠️ red for the wrong reason is not detection |
| 5 | ⛔ **restore the state, and verify it is restored** | ⭐ a sabotage left behind is a defect you introduced |
| 6 | **record that the failure was demonstrated** | otherwise the next reader repeats it |

> ## ⛔ IF THE FAILURE CANNOT BE CONSTRUCTED, THAT IS THE RESULT
> ⭐ A check whose failure cannot be produced is a check that cannot fail — §2.6, criterion 1.
> **The finding is to delete it, not to document why it is hard to test.**

---

## 5 · ⭐ DETECTION — how anyone learns it broke

⛔ **Validation proves it works now. It says nothing about tomorrow** — and tomorrow is when
nobody is looking.

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `VF-DET-001` | ⭐ **Never close something whose failure you would not notice** | 🔴 | ⛔ *"someone would eventually notice"* is not a mechanism |
| `VF-DET-002` | **Every critical behaviour has an observable failure signal** | 🟠 | what changes, visibly, when it stops? |
| `VF-DET-003` | ⭐ **Silent degradation is worse than a stop** | 🟠 | can it half-work while still reporting success? |

⭐ **`VF-DET-001` generalises everything above it.** It turns every close into one question:
**what would tell me this broke, and does that thing exist?** ⚠️ A system with no answer is not
verified — **it is unmonitored, which looks identical to healthy right until it does not.**

---

## 6 · ⛔ NEVER ACCEPTED AS PROOF

| # | Never | ⭐ Why |
|---|---|---|
| 1 | **a green from a check nobody has seen fail** | it proves the check ran, not that it measures |
| 2 | **a number from memory, or copied by hand** | ⭐ measure it and cite the source — a copied number is correct exactly once |
| 3 | ⛔ **"it compiles" / "no errors" as proof it works** | ⭐ **starting is not working** |
| 4 | **"it should work" / "more or less"** | ⚠️ *"more or less connected"* is the declared enemy — ⭐ when something **almost** works, stop and investigate |
| 5 | ⛔ **a pass whose measured count is zero** | §2.2 — that is NOT_MEASURED |
| 6 | ⭐ **"the tests pass"** with nothing else | ⛔ it answers none of the four conditions in §2.1 |

### ⭐ FOUR SIGNS IT WAS NOT ACTUALLY TESTED — any one is enough

| # | Sign | Why it disqualifies the proof |
|---|---|---|
| 1 | ⭐ **says it works without showing the datum** | it asserts a result instead of reporting a measurement |
| 2 | **tested the piece, not the flow** | ⭐ every piece passes its own test and the chain is still broken |
| 3 | **says "should work"** | when something almost works, stop |
| 4 | ⭐ **the green came from a path nobody executed** | ⚠️ the check ran and never touched what it claims to measure |

⛔ **These are not scored.** Any one present means the verification did not happen — 🔴 regardless
of how many other checks are green.

⚠️ **Sign 4 is the hardest to catch, because from the outside it looks identical to a real pass.**
⭐ That is why §2.1 condition 3 exists: **a check must have been seen to fail before its green is
worth anything.**

---

## 7 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ §3 — this installation's criteria | ⭐ the owner of the instance |
| §1, §2, §4-§6 — the base standard | whoever maintains the engine, through a recorded decision |
| ⛔ lowering a 🔴 to 🟠 locally | **nobody** — ⚠️ log the friction and propose it |

---

Related: `README.md` (⭐ **the parent — what a discipline is**) · `val-integration.md` (its sibling
— ⭐ whether the pieces are actually connected, as opposed to whether each one works) ·
`../owner-3-validation.md` (⭐ what consumes this, and decides closure) · `doc-planning.md`
(where the success criterion was written, before any of this ran).
