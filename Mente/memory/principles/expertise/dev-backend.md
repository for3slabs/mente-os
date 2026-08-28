# EXPERTISE · BACKEND

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Branch of:** `../owner-2-dev.md` — development
**Level:** ⚖️ criterion · ⭐ **the engine's base standard**, extensible by the installation
**Scope:** ⚠️ ENGINE document — §1, §2 and §4 ship identical to every clone; §3 is yours.

---

## 0 · WHAT THIS FILE IS

The criterion that decides whether backend work is **well built** — not whether it runs.

> ⭐ **Two things live here, and they must never be confused:**
>
> | | |
> |---|---|
> | **§2 · BASE STANDARD** | the engine's criterion. Ships filled in. ⛔ Do not edit it in an instance |
> | **⬜ §3 · YOURS** | what this installation adds. ⭐ **Extend here, never by rewriting §2** |
>
> ⛔ **Editing §2 locally means the next engine update either overwrites your criterion or
> conflicts with it.** Adding to §3 survives every update, and stays visibly yours.

⛔ **This file does not say HOW to implement anything.** It says what makes an implementation
acceptable, and what evidence proves it.

---

## 1 · THE CRITERION MODEL

Every criterion below carries the same fields. ⭐ **Uniformity is what lets something read this
file** — a checker, a gate, or a person who has thirty seconds.

| Field | States |
|---|---|
| **ID** | ⭐ permanent — `BE-<area>-<nnn>` · never renumbered |
| **Criterion** | what must be true |
| **Severity** | 🔴 mandatory · 🟠 expert · 🟢 guidance |
| **Verify** | ⭐ **how it is checked** — the observation, not the opinion |
| **Pass / Fail** | what result each observation produces |

### The three severities

| | Means | On violation |
|---|---|---|
| 🔴 **mandatory** | security, money, or silent data loss | ⛔ **blocks** — never a matter of taste |
| 🟠 **expert** | the criterion of whoever owns this system | ⬜ its shipping effect is declared by the owner |
| 🟢 **guidance** | a preference with a reason | informs |

⭐ **Separating them matters because they are argued differently.** A 🟠 can be discussed against
context; a 🔴 cannot. Merging them makes every rule negotiable — and the ones that get negotiated
away are the expensive ones.

---

## 2 · THE BASE STANDARD

Grouped by the six quality dimensions. ⭐ **Each criterion states how it is checked** — a criterion
with no observation behind it is an opinion with an ID.

### 2.1 · Architecture — does each piece have one responsibility, in the right layer?

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `BE-ARC-001` | ⭐ **ONE implementation per rule, never copied** — authorisation, session, limits | 🔴 | count implementations of the rule · must be exactly 1 |
| `BE-ARC-002` | **The entry point orchestrates, it does not decide** — it validates input and delegates; the logic is testable without the transport | 🟠 | name the layer where the decision lives · can it be tested without HTTP? |
| `BE-ARC-003` | **Configuration enters through ONE point** | 🟠 | count the places that read configuration directly |
| `BE-ARC-004` | **A piece can fail without taking the rest down** | 🟠 | name what stops working when this piece stops |

⭐ **Why `BE-ARC-001` is the strongest:** a duplicated guard does not fail loudly, it fails
**partially**. Eleven copies check correctly and the twelfth does not, so the system looks right
until somebody finds the one door that was never locked.

### 2.2 · Data design — what does the store guarantee, and what does code guarantee?

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `BE-DAT-001` | ⭐ **An invariant that must always hold is enforced by the store, not by an `if`** | 🔴 | for each invariant: is there a constraint, or only code? |
| `BE-DAT-002` | **A real relation has a declared reference** — no orphan records by design | 🟠 | inspect the schema for the relation |
| `BE-DAT-003` | ⛔ **Content that changes without deploying does not live in code** — thresholds, lists, anything with an owner | 🟠 | find the values in code that someone would want to change without a release |
| `BE-DAT-004` | **A destructive change declares its rollback before it runs** | 🔴 | the rollback exists, and ⭐ **has been executed at least once** |

⚠️ **`BE-DAT-001` is the one people argue with**, and the argument is always *"the code already
checks it"*. Code checks the paths it was written for; a constraint checks every path, including
the one added next month by someone who never read this file.

### 2.3 · Abstraction — one problem, one solution

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `BE-ABS-001` | ⭐ **Security and money are unified, always** — never N ways to do the same check | 🔴 | count implementations · must be 1 |
| `BE-ABS-002` | **Reuse the existing pattern; do not invent a second one** | 🟠 | name the existing pattern, or state why it does not fit |
| `BE-ABS-003` | ⚠️ **An abstraction with one caller is premature** | 🟢 | count callers |

⭐ **`BE-ABS-003` cuts the other way from the rest**, and that is deliberate: duplication is a
known cost, while the wrong abstraction is a cost that spreads. **Two similar things are not yet
a pattern.**

### 2.4 · Naming — does the name say what it does?

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `BE-NAM-001` | **The name states the action and its subject** | 🟠 | can a stranger say what it does without opening it? |
| `BE-NAM-002` | ⛔ **A name never lies about its effect** — something that writes is not called `get` | 🔴 | compare the name against what it actually does |
| `BE-NAM-003` | **One concept, one word, across the whole system** | 🟠 | search for synonyms of the same concept |

⭐ **`BE-NAM-002` is 🔴 and the others are not**, because a lying name causes a wrong decision by
someone who never had reason to doubt it. An ugly name only costs a second.

### 2.5 · Contracts — what does it promise, and what does it do when it cannot keep it?

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `BE-CON-001` | ⭐ **Expected failures ARE the contract** — they are declared, not improvised | 🟠 | list the declared failures · are they the ones that actually happen? |
| `BE-CON-002` | ⛔ **An internal error never leaks outward** — no stack trace, no query, no path | 🔴 | trigger the failure and read what comes back |
| `BE-CON-003` | **Before changing an existing contract, its consumers are identified** | 🟠 | ⭐ name them, measured — *"probably nobody uses it"* is not an answer |
| `BE-CON-004` | **An unhandled failure is logged with enough context to diagnose it** | 🟠 | can the failure be reconstructed from the log alone? |

⭐ **`BE-CON-001` is the one that separates a service from a script.** *"It fails"* is not a
contract; *"it returns this when the input is invalid, and this when the dependency is down"* is.

### 2.6 · Necessity — should this exist at all?

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `BE-NEC-001` | ⭐ **Something nobody calls is deleted, not kept just in case** | 🟠 | measure real usage — ⛔ *"it might be used"* is not evidence |
| `BE-NEC-002` | **Each added dependency is justified against not adding it** | 🟠 | what would it cost to do without it? |

⚠️ **Necessity is the dimension people skip**, because deleting feels riskier than keeping. ⭐ Kept
code is read, maintained, and eventually trusted by someone who assumes it is used.

---

## 3 · ⬜ THIS INSTALLATION'S CRITERIA

⬜ **Add yours here.** Same model as §1: an ID, the criterion, its severity, and how it is checked.

⭐ **Use your own prefix** so the origin is visible at a glance — for example `BE-OWN-001`. **Which
criterion came with the engine and which you added must never require reading history to answer.**

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| ⬜ … | ⬜ … | ⬜ … | ⬜ … |

> ⛔ **Do not let an AI write this section.** An invented technical criterion reads exactly like a
> real one and silently becomes the bar everything is measured against. ⭐ **The method: the AI
> asks, you answer with real cases, the AI structures.** Never the reverse.

**The questions that elicit it — answer with cases, not principles:**

1. What is the last backend defect that reached production, and what would have caught it?
2. What do you look at first when reviewing someone else's endpoint?
3. What have you had to rebuild because it was built wrong the first time?
4. What would make you refuse to merge, without discussion?
5. ⭐ What does your stack make easy that is usually a mistake?

---

## 4 · ⭐ THE DECISION PROTOCOL — before touching backend

⭐ **This is the section that does the most work.** The criteria above judge what was built; these
questions decide what to build. ⛔ **An unanswered question here is a decision made by accident.**

⚠️ **Not all apply to every change.** The ones that do not apply are stated as not applying —
⭐ **skipping silently and not applying are indistinguishable afterwards.**

### Identity and permission

1. Who is calling, and **how was that identity verified**?
2. ⛔ Does authorisation read the **verified session**, or something the caller supplied?
3. What permission does this operation require, and where is it checked?
4. ⚠️ Is there any check that exists **only** on the client side?

### Input

5. What enters from outside — parameters, body, headers, uploads, callbacks?
6. Where is it validated, and does the logic receive it already validated?

### Data

7. What is read, and what is mutated?
8. ⭐ Which guarantees belong to the **store**, and which to code?
9. Do several mutations form **one logical operation**? Then where is its boundary?

### Concurrency and repetition

10. ⭐ **Can two of these run at the same time?** What happens if they do?
11. Does it read state and then change it based on what it read?
12. ⭐ **What happens if the same request arrives twice?** Is that acceptable?

### External systems

13. Does it touch anything outside this process — another service, a queue, a chain, a provider?
14. ⭐ **Which one is the source of truth** when they disagree?
15. What happens if the external side succeeds and the local side fails? ⚠️ **And the reverse?**
16. Does every outbound call have a **timeout**?
17. ⛔ Is retrying safe — or would it duplicate a real-world effect?

### Failure

18. What failures are expected, and what does the caller receive for each?
19. ⭐ **If this silently stopped working, how would anyone find out?**

### Traces

20. What must be recorded to reconstruct this later?
21. ⛔ **What must NEVER be recorded** — credentials, tokens, keys, personal data?

### Consequences

22. Who consumes what this changes, and does the change break them?
23. How is it verified — and ⭐ **has the check been seen to fail**?
24. If it goes wrong in production, what is the way back?

---

## 5 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ §3 — this installation's criteria | ⭐ the owner of the instance |
| §2 — the base standard | whoever maintains the engine, through a recorded decision |
| ⛔ lowering a 🔴 to 🟠 locally | **nobody** — ⚠️ log the friction and propose it instead |

⭐ **A 🔴 that can be downgraded where it is inconvenient stops being mandatory** — and the places
where it is inconvenient are exactly the places it was written for.

---

Related: `README.md` (⭐ **the parent — what a discipline is**) · `../owner-2-dev.md` (what loads
this) · `../owner-3-validation.md` (what verifies the evidence) · `../imported-patterns.md`
(⚠️ absorbed failure patterns — ⛔ not criterion) · `DISCIPLINE.md.template` (to create another).
