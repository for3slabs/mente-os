# EXPERTISE · DATABASE

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Branch of:** `../owner-2-dev.md` — development
**Level:** ⚖️ criterion · ⭐ **the engine's base standard**, extensible by the installation
**Scope:** ⚠️ ENGINE document — §1, §2, §4 and §5 ship identical; §3 is yours.

---

## 0 · WHAT THIS FILE IS

⭐ **It does not teach how to design a database. It defines what makes a data decision correct.**

> ⭐ **Two things live here, and they must never be confused:**
>
> | | |
> |---|---|
> | **§2 · BASE STANDARD** | the engine's criterion. Ships filled in. ⛔ Do not edit it in an instance |
> | **⬜ §3 · YOURS** | what this installation adds. ⭐ **Extend here, never by rewriting §2** |

### ⛔ DO NOT INVENT

| Situation | ⭐ The response |
|---|---|
| the criterion does not exist | **ask** — ⛔ never fill the gap with "best practices" |
| the criterion exists, the evidence does not | ⬜ **declare UNKNOWN** |
| something is built but not connected | ⭐ **declare the seam** (§5) |
| there is evidence of a violation | 🔴 block |

⛔ **Never infer completion.** *"It probably works"* and *"it works"* are different claims, and
only one of them was measured.

### ⭐ The failure this discipline prevents

⚠️ **A data defect is the only kind that cannot be fixed by fixing the code.** ⭐ **A wrong record
written today stays wrong after the bug is gone** — the deploy is reversible, the row is not. That
asymmetry is why so many criteria here are 🔴 while their equivalents elsewhere are not.

---

## 1 · THE CRITERION MODEL

| Field | States |
|---|---|
| **ID** | ⭐ permanent — `DB-<area>-<nnn>` · never renumbered |
| **Criterion** | what must be true |
| **Severity** | 🔴 mandatory · 🟠 expert · 🟢 guidance |
| **Verify** | ⭐ **how it is checked** — the observation, not the opinion |

### The three severities

| | Means | On violation |
|---|---|---|
| 🔴 **mandatory** | integrity, security, or irreversible loss | ⛔ **blocks** |
| 🟠 **expert** | the criterion of whoever owns this system | ⬜ effect declared by the owner |
| 🟢 **guidance** | a preference with a reason | informs |

### The result states

| | Means |
|---|---|
| 🟢 **PASS** | every mandatory criterion holds, with evidence |
| 🟡 ⭐ **PASS WITH DECLARED SEAMS** | it works, and what is **not** connected is declared: what · why · how |
| 🔴 **FAIL** | a mandatory criterion is violated |
| ⬜ **UNKNOWN** | ⭐ it could not be checked — ⛔ **not the same as PASS** |

⭐ **The amber state is the one that earns trust.** Without it, incomplete work has two options:
look finished, or look broken. **A declared seam is neither** — it is honest, and it survives the
session that produced it.

---

⭐ **Applied by `../owner-2-dev.md`** — which decides whether building may start at all. ⛔ **This file judges; the owner acts on the judgement.**

## 2 · THE BASE STANDARD

### 2.1 · Identity and relations — what is a row, and what does it belong to?

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `DB-IDN-001` | **Every table declares its primary key**, and the plan says what identifies the row | 🔴 | inspect the schema |
| `DB-IDN-002` | ⚠️ **A business value is not a technical identity** unless the plan justifies it | 🟠 | is the key something that could change, or be reused? |
| `DB-REL-001` | ⭐ **A real relation carries a declared reference** — no orphan rows by design | 🔴 | the constraint exists in the schema, ⛔ not only in code |
| `DB-REL-002` | ⭐ **Every relation declares what happens when the parent is removed** | 🔴 | cascade · restrict · detach · archive — one of them, chosen and written down |

⭐ **`DB-REL-002` is the one nobody decides and everybody inherits.** Whatever the store does by
default becomes the policy, and it is discovered the day a parent is deleted in production.

### 2.2 · Integrity — what does the store guarantee, and what does code guarantee?

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `DB-INT-001` | ⭐ **An invariant that must always hold is enforced by the store, not by an `if`** | 🔴 | for each invariant: constraint, or only code? |
| `DB-INT-002` | ⭐ **Uniqueness required by the domain is enforced by the store** | 🔴 | is there a uniqueness constraint, or just a prior read? |
| `DB-INT-003` | **A value with a restricted set of options is restricted by the store** where it can be | 🟠 | is the set enforced, or only expected? |
| `DB-INT-004` | ⛔ **A column is nullable only when "absent" is a real state of the domain** | 🟠 | for each nullable column: what does null mean here? |
| `DB-INT-005` | ⭐ **NULL is not a substitute for a state** — unknown, not-applicable and pending are three things | 🟠 | does one null carry more than one meaning? |

⚠️ **`DB-INT-002` is the one that looks handled and is not.** *"The code checks it does not
exist"* fails the moment two requests check at the same time: both read absent, both write.
⭐ **A constraint refuses the second one; a prior read cannot.**

⚠️ **This is what `val-integration.md` §2.3 delegates to.** ⭐ **A guarantee enforced here is not
re-checked at every seam** — that would be re-deriving, not validating. **What crosses a seam with
no constraint behind it is validated there, every time.**

### 2.3 · Where a value lives — the store or the code

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `DB-LOC-001` | ⛔ **Anything with an owner does not live in code** — it identifies a person, an instance, a tenant | 🔴 | find identifying values written into source |
| `DB-LOC-002` | ⭐ **Anything that changes without deploying does not live in code** | 🟠 | ⭐ **the test: does changing this require a release?** Then it is in the wrong place |
| `DB-LOC-003` | **Configurable lists — catalogues, roles, categories — are data** | 🟠 | ⚠️ see the exception below |
| `DB-LOC-004` | **Thresholds and numeric limits are data** — timeouts, retries, quotas, maximums | 🟠 | tuning must not need a deploy |
| `DB-LOC-005` | ⭐ **Sensitive user information never lives in configuration** | 🔴 | this is about trust, not about storage |

⭐ **Environment variables are for WIRING, never for CONTENT.** A connection string is wiring; a
list of roles is content. ⚠️ **An environment variable holding content is a measurable finding,
not a style preference:** it cannot be audited, every installation sets it by hand, and changing
it is a deployment.

> ## ⚠️ THE EXCEPTION — and it is the most important line in this file
>
> ⭐ **A fixed list that protects an authorisation path may stay in code.**
>
> ⛔ **Moving it to the store means an ordinary write can alter a security boundary.** *"Everything
> configurable"* is as wrong as *"everything hardcoded"* — the criterion is: **content belongs in
> the store, except where keeping it in code is what protects the system.**
>
> ⭐ **A rule that declares its own limit is a rule that survives contact with reality.** One that
> does not gets applied where it does damage, and then gets abandoned entirely.

### 2.4 · Lifecycle — how a row is born, changes, and ends

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `DB-LIF-001` | ⭐ **No dead-end state** — every transient state has a way out | 🔴 | for each state: which transitions leave it? A state with none is a trap |
| `DB-LIF-002` | **A stateful entity declares its states and allowed transitions** | 🟠 | can the transitions be drawn from the schema and the plan? |
| `DB-LIF-003` | ⭐ **A default never points at something that has an owner** | 🔴 | trace each default: does it resolve to a resource someone owns? |
| `DB-LIF-004` | **Deletion policy is declared** — removed, archived, anonymised or retained, and for how long | 🟠 | ⛔ neither *"always soft delete"* nor *"always delete"* — a stated choice |

⭐ **`DB-LIF-003` catches a failure that looks harmless.** A default naming a real, owned resource
means every unassigned row silently belongs to that owner. ⛔ **A default is a neutral slot, never
a real name.**

### 2.5 · One truth — and duplication with a reason

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `DB-TRU-001` | ⭐ **One datum, one owner, one source of truth** | 🔴 | is the same value authoritative in two places? |
| `DB-TRU-002` | ⚠️ **Duplication is not automatically wrong — unjustified duplication is** | 🟠 | ⭐ does the plan justify it? If nobody can say why, it is a defect |
| `DB-TRU-003` | **A constraint violation surfaces as a domain error, not as an internal failure** | 🟠 | trigger it and read what the caller receives |

⭐ **`DB-TRU-001` is the failure that spreads.** When two places hold the same value, they
eventually disagree — and then code starts deciding which one to believe, in each place
separately, differently.

### 2.6 · Access and growth

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `DB-ACC-001` | ⭐ **The design states how the data will be read**, not only how it is stored | 🟠 | which queries does this shape serve? |
| `DB-ACC-002` | **Every index answers a query that exists** | 🟠 | ⛔ an index "just in case" costs every write and buys nothing |
| `DB-ACC-003` | **A collection that grows declares its bound** — pagination, ordering, maximum size | 🟠 | what happens to this query at a thousand times the current volume? |
| `DB-ACC-004` | ⭐ **Expected volume and retention are stated for anything that accumulates** | 🟢 | records, events, logs — how much, for how long |

⚠️ **`DB-ACC-001` inverts the usual order, on purpose.** A schema designed without knowing how it
will be read is a schema that will be read badly — and by then the data is already in it.

### 2.7 · Necessity

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| `DB-NEC-001` | ⭐ **The plan says why this exists — before the schema does** | 🔴 | ⛔ **no plan → no schema → no migration** |
| `DB-NEC-002` | **A column nobody reads is removed, not kept just in case** | 🟠 | measure actual reads |

⭐ **`DB-NEC-001` is the ordering that changes everything.** *"Is this table well designed?"* is
the second question. **The first is *"why does it exist?"*** — and answering it second is how
technical debt gets built deliberately.

---

## 3 · ⬜ THIS INSTALLATION'S CRITERIA

⬜ **Add yours here**, using the model in §1 and ⭐ **your own prefix** — for example `DB-OWN-001`.
**Which criterion came with the engine and which you added must never require reading history.**

| ID | Criterion | Sev | Verify |
|---|---|---|---|
| ⬜ … | ⬜ … | ⬜ … | ⬜ … |

> ⛔ **Do not let an AI write this section.** An invented data criterion reads exactly like a real
> one and becomes the bar everything is measured against. ⭐ **The AI asks, you answer with real
> cases, the AI structures.** Never the reverse.

**The questions that elicit it — answer with cases, not principles:**

1. What is the worst data problem you have had to repair, and what would have prevented it?
2. What do you look at first when reviewing someone else's schema?
3. ⭐ What has your store let you do that it should have refused?
4. What would make you refuse a migration outright?
5. What do you always end up regretting six months later?

---

## 4 · ⭐ THE DESIGN CONTRACT — answer before writing schema

⛔ **A question left unanswered here is a decision made by accident.** ⚠️ The ones that do not
apply are stated as not applying — ⭐ skipping silently and not applying look identical afterwards.

### What it is

1. What does this represent in the domain?
2. Why does it exist — and where is that written?
3. Who owns it?
4. ⭐ What uniquely identifies a row?

### What it connects to

5. What does it reference, and what references it?
6. ⭐ What happens when the parent disappears?
7. Where is the authoritative value — here, or somewhere else?

### What must be impossible

8. Which invariants must always hold?
9. ⭐ Which of them can the **store** enforce, and which only code can?
10. What must be unique?
11. Which columns may be absent, and ⭐ **what does absent mean for each**?

### How it lives

12. What states can it be in, and how does it leave each one?
13. ⭐ Is there any state with no way out?
14. What happens when it is deleted — removed, archived, anonymised, kept?
15. How long is it kept?

### Under load and in parallel

16. ⭐ **What happens if two writes arrive at the same time?**
17. Which mutations must succeed or fail together?
18. How will it be read — filtered, ordered, paginated?
19. How much of it is expected, and how fast does it grow?

### Who may see it

20. Who reads it, who writes it?
21. ⛔ What in it is sensitive?

### Getting it in, and out

22. ⭐ **How is the change reversed?**
23. Has the rollback been executed, not just written?
24. Which consumers break, and how are they migrated?

---

## 5 · MIGRATIONS AND SEAMS

### 5a · Classify before running

| Class | Examples | Requires |
|---|---|---|
| 🟢 **safe** | adding something optional and new | the standard checks |
| 🟠 **risky** | tightening a rule · changing a type · renaming | ⭐ **consumers identified first** |
| 🔴 **destructive** | removing anything · irreversible transformation | ⛔ **all of §5b, plus explicit approval** |

⭐ **The class is declared before running, not deduced afterwards.** A migration nobody classified
is treated as destructive — ⚠️ the cheapest assumption is the safest one.

### 5b · Before it touches live data

| # | Required | ⭐ Why it is not enough to have it |
|---|---|---|
| 1 | rollback **declared** | ⭐ **and executed at least once** — an untested rollback is a hypothesis |
| 2 | backup **verified** | ⭐ **a backup that has never been restored is not a backup** — it is a file |
| 3 | tested against **real data** | sample data does not have the rows that break things |
| 4 | consumers unbroken | ⭐ **writers first, strict readers after** — never the reverse |
| 5 | ⭐ **run twice** | if the second run breaks, it was never idempotent |

### 5c · ⭐ Declaring a seam

Something built and not yet connected is not a failure. ⛔ **Hiding it is.**

| Field | States |
|---|---|
| **what** | what is built and not connected |
| **why** | ⛔ the reason — never *"pending"* on its own |
| **how** | what would connect it, and what it depends on |

⭐ **This is what makes 🟡 an honest state instead of a soft 🟢.** Without the three fields, "partly
done" and "done" become indistinguishable the moment the session ends — and the next reader
inherits a claim nobody can check.

---

## 6 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ §3 — this installation's criteria | ⭐ the owner of the instance |
| §2, §4, §5 — the base standard | whoever maintains the engine, through a recorded decision |
| ⛔ lowering a 🔴 to 🟠 locally | **nobody** — ⚠️ log the friction and propose it |

---

Related: `README.md` (⭐ **the parent — what a discipline is**) · `dev-backend.md` (⭐ what maps a
constraint to a domain error) · `../owner-2-dev.md` · `../owner-3-validation.md` (evidence and
result states) · `../imported-patterns.md` (⚠️ absorbed patterns — ⛔ not criterion).
