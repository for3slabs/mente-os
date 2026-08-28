# RULE · WORKING IN A BLOCK

**Status:** current · **Type:** rule · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every change made while a block is open
**Enforcement:** 🔒 partial — `bin/check-work` · ⚠️ **several rows here are 📖**
**Governance:** `engine` in the piece table · ✅ ships identical to every clone

---

## 0 · WHAT THIS FILE IS

> ## ⭐ You are inside a block. How do you behave?

Four questions, and each one used to be a separate file:

| The question | ⭐ Answered by |
|---|---|
| **how much process does this change need?** | §2 · the lane |
| **what may I read?** | §3 · isolation |
| ⭐ **a rule is in my way — now what?** | §4 · friction |
| **there is a bug — where do I fix it?** | §5 · fix, not patch |

⚠️ **They were four files that cited each other in a closed loop.** ⭐ **They share one owner and
one moment: you are mid-change, and you need all four at once.**

### The failure this prevents

⛔ **A change made on an estimate.** ⭐ *"This looks small"* is a judgement, and a judgement that
is wrong looks exactly like one that is right — ⚠️ **until four commits later.**

---

## 1 · ENFORCEMENT

| | Means |
|---|---|
| 🔒 **lock** | ⭐ a script refuses — ⚠️ and it has been seen to fail |
| 🟡 **prompt** | the agent asks before proceeding |
| 📖 **discipline** | ⛔ **nothing verifies this** |

⚠️ **Most of this file is 📖, and it says so.** ⭐ **These are behaviours, not shapes** — a script
can check that a friction was logged; it cannot check that the work stopped to think.

**IDs are permanent.** `WRK-<area>-<nnn>` — ⛔ never renumbered, never reused.

---

## 2 · THE LANE — how much process this change needs

⛔ **Three lanes. And the lane is chosen by PROPAGATION, never by judgement.**

| Lane | When | Path |
|---|---|---|
| `direct` | ⭐ a trivial change — a string, a label, a typo | validation only |
| `task` | one loose piece, no new design | build → validate |
| `full-block` | ⭐ **something new, or it touches several pieces** | plan → build → validate |

### ⭐ How the lane is chosen

```
Does the target have DECLARED DEPENDENTS?
        │
   YES ─┴─▶ full-block            ⛔ no discussion
        │
    NO ─┴─▶ does it need new design?
              YES ─▶ task
               NO ─▶ direct
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `WRK-LAN-001` | ⭐ **The lane comes from the dependency graph, not an estimate** | 🟡 | ⛔ *"it looks small"* is not an input |
| `WRK-LAN-002` | **Declared dependents → `full-block`, always** | 🔒 | ⚠️ count them before choosing |
| `WRK-LAN-003` | **The lane is written in the block's identity** | 🔒 | the field is present and valid |

> ## ⭐ THIS IS THE WHOLE POINT OF THE RULE
> ⛔ **It stops an agent from declaring something trivial and being wrong** — which is how one
> file ends up edited twenty times for one problem.

⚠️ **Why three lanes and not one process for everything:** ⭐ **a system where every typo goes
through full planning becomes unbearable and gets abandoned — and an abandoned standard protects
nothing.** The three lanes exist so the strict path stays credible for the cases that need it.

---

## 3 · ISOLATION — what you may read

> ## ⛔ BLOCKS DO NOT READ EACH OTHER BY DEFAULT.

| ⛔ Forbidden | ✅ Allowed |
|---|---|
| reading another block's files | ⭐ a connection **declared** in §C |
| scanning the whole block directory | an explicit request from the owner |
| ⭐ **inferring from a similar name** | resolution by **exact id** |
| synthesising across blocks | ⛔ explicit request only |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `WRK-ISO-001` | ⭐ **Resolution is EXACT — no match means STOP AND ASK** | 📖 | ⛔ see below |
| `WRK-ISO-002` | **A §C connection resolves to a block that exists** | 🔒 | check the id |
| `WRK-ISO-003` | ⛔ **Undeclared is out of reach** | 📖 | ⚠️ nothing verifies this |

> ## ⭐ WHY EXACT RESOLUTION IS THE MOST IMPORTANT PART
> ⚠️ **An agent that infers sounds exactly as confident as one that knows.** That is the mechanism
> behind *"no, that is not what I meant"* — ⛔ and it is invisible from outside.
>
> ⭐ **Stopping turns a silent loss into a visible question.**

⚠️ **And there is a cost reason too:** *"reading the other blocks for context"* is how a session
grows until a single greeting costs a fortune. ⭐ **Context is the scarce resource, and isolation
is what protects it.**

---

## 4 · FRICTION — when a rule is in your way

```
1 · COMPLY              ⛔ even if it seems wrong
2 · LOG THE FRICTION    in the block, §H
3 · CONTINUE            ⭐ the work never stops
4 · AT CLOSE            frictions surface together, as proposals
5 · THE OWNER DECIDES   adjust · keep with a documented exception · remove
```

### ⚠️ The one exception — stop immediately

⛔ **If complying causes real damage** — breaking production, exposing a secret, losing data —
⭐ **that is not friction. It is a defect in the rule.** Stop and raise it.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `WRK-FRI-001` | ⭐ **Comply first. Never skip a rule in the moment** | 📖 | ⛔ nothing verifies this |
| `WRK-FRI-002` | **Each friction is logged with its reason** | 🔒 | ⚠️ the four fields present |
| `WRK-FRI-003` | ⭐ **A rule is flagged at N frictions in DISTINCT blocks** | 🔒 | see below |
| `WRK-FRI-004` | ⛔ **A flagged rule is never changed automatically** | 📖 | ⭐ it escalates to the owner |

### ⭐ DETECTION IS ARITHMETIC, NOT INTERPRETATION

| Two details make it work | ⭐ Why |
|---|---|
| ⭐ **DISTINCT blocks, not repetitions** | ⛔ three frictions in the *same* block is one task chafing; in *distinct* blocks, **the rule is wrong** |
| ⭐ **It never expires** | ⚠️ **the problem is not the speed of the friction — it is its recurrence** |

⚠️ **Without the first, any long task raises a false alarm** — and then the mechanism gets
ignored, which costs more than never having it.

### ⛔ Why not just ask every time?

| The alternative | ⛔ Why it fails |
|---|---|
| **ask whenever something chafes** | ⚠️ the owner becomes a bottleneck, and the system gets slow |
| ⭐ **let the agent skip rules it judges wrong** | ⛔ **in a month the rules are the agent's again** |

⭐ **Logging and accumulating is what lets the system learn without constant supervision.**

---

## 5 · FIX, NOT PATCH

> ## ⭐ THE ONE QUESTION THAT CHANGES EVERYTHING
> | ⛔ A patch asks | ⭐ A fix asks |
> |---|---|
> | *"where does it fail?"* | *"**why does this failure exist, and where else does it live?**"* |

| # | Step | ⚠️ |
|---|---|---|
| 1 | ⛔ **Do not write the fix yet** | |
| 2 | **Read the piece and its surroundings** | |
| 3 | ⭐ **Find every consumer before deciding** | ⚠️ **this is the step that gets skipped** |
| 4 | **Choose the real solution** — ⭐ even if it means another route | |
| 5 | **Declare the propagation in the block** | |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `WRK-FIX-001` | ⭐ **Every consumer measured before the fix** | 📖 | ⛔ nothing verifies this |
| `WRK-FIX-002` | ⭐ **All copies fixed, never one** | 📖 | ⚠️ ⛔ the copy left behind is the one that resurfaces |
| `WRK-FIX-003` | **The propagation is declared in the block** | 🟡 | §C and §F updated |

### ⭐ THE SAME BUG, BOTH WAYS

```
⛔ AS A PATCH                          ✅ AS A FIX
1 · bug reported                       1 · bug reported
2 · find WHERE it fails → one file     2 · ⭐ touch nothing yet
3 · fix it there                       3 · who else has this shape? → several
4 · a similar symptom appears          4 · ⭐ the cause is not "this file is
5 · another one                             wrong" — it is the shared assumption
6 · discover it was everywhere         5 · ONE change, every site correct
7 · a full sweep of the pattern        ⤷ one commit · ⭐ it cannot reappear
⤷ several commits, one problem
```

> ## ⭐ THE DIFFERENCE IS NOT EFFORT. IT IS STEP 3.

⚠️ **What this rule is NOT:** ⛔ it is not *"never fix quickly"*. A typo is a typo. ⭐ **It applies
when the piece has declared dependents** — which is exactly what §2 detects.

⭐ **And it does not forbid another route.** If the real solution means building something
differently, that is the right answer.

---

## 6 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **the lane chosen by estimate** | ⚠️ a change treated as trivial that propagates — ⭐ **found four commits later** |
| **reading an undeclared block** | ⛔ one block's assumptions leak into another's work, invisibly |
| ⭐ **skipping a rule instead of logging it** | ⛔ **the rule stops existing, and nothing records that it did** |
| **fixing one copy** | ⚠️ ⭐ the same bug returns wearing a different symptom |

---

## 7 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ the friction threshold, the lane names | the owner of the instance, ⚠️ **declared once** |
| the rules and their IDs | whoever maintains the engine, through a recorded decision |
| ⛔ turning a 📖 into a claim of enforcement | **nobody** — ⭐ ⛔ **that is the worst lie this system can tell** |

---

Related: `README.md` (⭐ the three document types) · `contract-block.md` (⭐ **§A the lane, §C the
connections, §H the friction log — this file writes into all three**) · `contract-document.md` ·
`../memory/principles/owner-2-dev.md` (⭐ what sequences the work) ·
`../memory/principles/expertise/dev-backend.md` (⭐ §2.1 — one implementation of a rule, which is
what §5 restores) · `../bin/check-work` (what enforces the 🔒 rows).
