# RULE · WORKING IN A BLOCK

**Status:** current · **Type:** rule · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every change made while a block is open
**Enforcement:** 🔒 partial — `bin/check-work` · ⚠️ **several rows here are 📖**
**Verified by:** `bin/check-work` · `bin/probes/probe-work.py`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone
**Size:** ⭐ **a BASE file — it ships whole.** See `contract-document.md` §4.

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

## 2 · ⭐ THE THREE WORDS THIS FILE RESTS ON

⛔ **Every rule below uses them, and an undefined term is a term each reader
resolves differently** — which is the exact failure this file exists to stop.

### ⭐ DEPENDENT — what makes the lane widen

| ✅ A dependent is a piece that… | |
|---|---|
| **consumes what the target produces** | its output, its record, its file |
| **imports or calls the target** | ⭐ across a module, a process, a boundary |
| **relies on its declared contract** | a shape, a name, a guarantee |
| ⭐ **depends on its runtime behaviour** | ⚠️ it works because the target behaves that way |
| **is declared downstream of it** | in the block's connections |

| ⛔ NOT a dependent | ⭐ Why it gets counted anyway |
|---|---|
| **the same filename elsewhere** | ⚠️ a naive search finds it |
| **a nearby directory** | proximity reads as relationship |
| ⭐ **conceptual similarity** | *"it does something similar"* is not a dependency |
| **a mention in prose** | ⛔ **a mention is not an import** |
| ⭐ **a build artifact or a vendored copy** | ⚠️ **they are copies, not consumers** |

⭐ **The last row is measured:** counting build output turned a real count of
sixteen into thirty-eight. ⛔ **A number nobody can reproduce is not evidence.**

### CONSUMER · PROPAGATION

| | |
|---|---|
| **consumer** | ⭐ a dependent **that this specific change reaches** — ⚠️ not every dependent is |
| **propagation** | ⭐ the path from the target to each consumer, **written down** |

⚠️ **The difference between dependent and consumer is what §5 turns on:** ⛔ you
fix every affected **consumer**, not every piece that happens to depend on the
target.

---

## 3 · THE LANE — how much process this change needs

⛔ **Three lanes. And the lane is chosen by PROPAGATION, never by judgement.**

| Lane | When | ⭐ The path it takes |
|---|---|---|
| `direct` | ⭐ a trivial change — a string, a label, a typo | **validation only** |
| `task` | one loose piece, no new design | **build → validate** |
| `full-block` | ⭐ **something new, or it touches several pieces** | **plan → build → validate**, ⚠️ with backtracking |

### ⭐ How the lane is chosen

```
Does the target have DECLARED DEPENDENTS in the graph?
        │
   YES ─┴─▶ full-block            ⛔ no discussion
        │
    NO ─┴─▶ does it need new design?
              YES ─▶ task
               NO ─▶ direct
```

⭐ **The decision comes from the graph, not from an estimate.**

#### ⛔ `full-block` APPLIES WHEN **ANY** OF THESE IS TRUE

⚠️ *"It touches several pieces"* is still a judgement. ⭐ **These are not:**

| # | The change… |
|---|---|
| 1 | ⭐ **the target has declared dependents** |
| 2 | **it changes a declared contract** — a shape, a name, a guarantee |
| 3 | ⭐ **it changes something others read** — a schema, a shared store |
| 4 | **it changes behaviour something outside relies on** |
| 5 | ⭐ **it introduces a new integration** |
| 6 | **it creates or changes a connection between blocks** |

⭐ **Any one is enough.** ⛔ **None of them asks how big the change feels.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `WRK-LAN-001` | ⭐ **The lane comes from the dependency graph, not an estimate** | 🟡 | ⛔ *"it looks small"* is not an input |
| `WRK-LAN-002` | **Declared dependents → `full-block`, always** | 🔒 | ⚠️ count them before choosing |
| `WRK-LAN-003` | **The lane is written in the block's identity** | 🔒 | the field is present and valid |
| `WRK-LAN-004` | ⭐ **The graph is re-measured before the lane is chosen** | 📖 | ⛔ a stale graph picks the wrong lane |
| `WRK-LAN-005` | 🔴 ⭐ **NOTHING IS EDITED BEFORE THE SCOPE IS KNOWN** | 📖 | ⛔ see below |

> ## 🔴 `WRK-LAN-005` — the most dangerous order to get wrong
> ⛔ **Nothing is edited until: the lane is chosen · the dependents are
> measured · every required block resolved · the consumers found.**
>
> ⚠️ **The natural order is the opposite one:** ⛔ find the bug → open the file
> → edit → think afterwards. ⭐ **By then the estimate has already become a
> commit**, and everything after it is justification.

> ## ⭐ THIS IS THE WHOLE POINT OF THE RULE
> ⛔ **It stops an agent from declaring something trivial and being wrong** — ⚠️ **measured: one
> file ended up edited twenty-one times for what was reported as one small fix.**

### ⭐ THE SHAPE OF THE CASE THAT PROVES IT

⚠️ **Generalised from a measured incident, because the shape recurs:**

| | |
|---|---|
| **the request** | *"store this value where it really belongs, not where it is being read from"* |
| **what it looked like** | a task — one file, one line |
| ⛔ **what it was** | 🔴 **full-block** — the piece had **five declared dependents** |
| **what happened** | ⚠️ one file was fixed · three more symptoms appeared · then a full sweep of the pattern |
| ⭐ **the measured cost** | **four commits for one problem**, and **42% of that period's commits were fixes** |

⭐ **The lane would have caught it before the first line was written** — ⛔ not because anyone was
smarter, **but because the graph already knew.**

### Examples

| The request | Lane | ⭐ Why |
|---|---|---|
| *"change this label"* | `direct` | no declared dependents |
| *"this error message is unclear"* | `direct` | a string, no logic |
| *"add error handling to this isolated function"* | `task` | no dependents |
| ⭐ *"add a column that others read"* | 🔴 `full-block` | ⛔ it propagates to every reader |
| *"connect an external provider"* | 🔴 `full-block` | a new piece **plus** an outside integration |

### ⛔ WHY THREE LANES AND NOT ONE PROCESS

⚠️ **If every change went through the full path, the system becomes unbearable and gets
abandoned** — ⭐ **and an abandoned standard protects nothing.**

⛔ **That is a measured failure mode, not a hypothesis:** a method that was strict, complete and
correct went **unread in most sessions.** ⭐ **The three lanes exist so the strict path stays
credible for the cases that need it.**

---

## 4 · ISOLATION — what you may read

> ## ⛔ BLOCKS DO NOT READ EACH OTHER BY DEFAULT.

⭐ **This is the outer gate — the one that guards reading another installation — applied INSIDE
the system.**

| ⛔ Forbidden by default | ✅ Allowed |
|---|---|
| reading another block's files | ⭐ a connection **declared** in the block |
| ⭐ **scanning the whole block directory** | an **explicit request** from the owner |
| ⭐ **inferring from a similar name** | ⭐ resolution by **exact id** |
| synthesising across blocks | ⛔ explicit request only |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `WRK-ISO-001` | ⭐ **Resolution is EXACT — no match means STOP AND ASK** | 📖 | ⛔ see below |
| `WRK-ISO-002` | **A declared connection resolves to a block that exists** | 🔒 | check the id |
| `WRK-ISO-003` | ⛔ **Undeclared is out of reach** | 📖 | ⚠️ nothing verifies this |
| `WRK-ISO-004` | ⭐ **A legitimate cross happens ONLY two ways** | 📖 | ⛔ see below |

### ⭐ RESOLUTION IS EXACT

```
1 · look the block up by EXACT id
2 · match? ── YES ─▶ load its tier 1
        │
        └── NO ──▶ ⛔ STOP AND ASK
```

⛔ **Forbidden:** a fuzzy match · inferring from a similar name · ⚠️ **picking the most recent
block "because it is probably that one".**

> ## ⭐ WHY THIS IS THE MOST IMPORTANT PART
> ⚠️ **An agent that infers sounds exactly as confident as one that knows.** That is the mechanism
> behind *"no, that is not what I meant"* — ⛔ and it is invisible from outside.
>
> ⭐ **Stopping turns a silent loss into a visible question.**

### ⭐ THE TWO WAYS A CROSS IS LEGITIMATE

| # | | ⭐ |
|---|---|---|
| 1 | **the connection is DECLARED in the block** | ⭐ then reading it is not a violation — it is the point |
| 2 | **the owner asks for it explicitly** | ⚠️ **nothing else** |

⭐ **There is no third way**, and that is deliberate: ⛔ every additional route is a route nobody
audits.

### ⚠️ AND THE COST REASON, MEASURED

⭐ **The outer gate has full measured compliance** — ⚠️ **it protects one thing, so it gets
honoured.** ⛔ **Without this rule, *"reading the other blocks for context"* reproduces INSIDE the
system the consumption problem the gate already solved OUTSIDE it.**

> ## ⭐ THE PRECEDENT THAT JUSTIFIES IT
> ⚠️ **A session that ran for weeks accumulated so much live context that a one-word greeting cost
> a day's quota.** ⛔ **Nothing was broken. The system was simply reading everything, all the
> time.**

⭐ **Context is the scarce resource, and isolation is what protects it.**

---

## 5 · ⛔ THE STOP PROTOCOL — three kinds, and each one reports differently

⚠️ **`STOP AND ASK` with no format is an instruction every agent obeys
differently.** ⭐ **What must be reported is as much the rule as the stopping.**

| Kind | ⭐ When | What follows |
|---|---|---|
| ⬜ **STOP-ASK** | ⭐ **information is missing** — a block, a path, a decision | ⚠️ the owner answers, the work resumes |
| 🔴 **STOP-SAFETY** | ⛔ **continuing causes real damage** — data, a secret, production | ⭐ raise it immediately, before anything else |
| ⚠️ **STOP-BLOCKED** | ⭐ **it cannot proceed technically** — a broken graph, a missing artifact | it becomes the block's blocker |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `WRK-STP-001` | ⭐ **A stop names WHICH of the three it is** | 📖 | ⛔ they resume differently |
| `WRK-STP-002` | ⭐ **A stop reports what is missing, not that something is** | 📖 | ⚠️ *"I could not find it"* is not a report |
| `WRK-STP-003` | ⛔ **STOP-SAFETY interrupts everything** | 📖 | ⭐ it does not wait for a good moment |

### ⭐ WHAT A STOP MUST REPORT

```
KIND:     ask | safety | blocked
BLOCK:    <the block this happened in>
ATTEMPT:  <what was being done>
MISSING:  <the exact thing that did not resolve>
LOOKED:   <the exact id or path attempted>
WHY:      <why it is required to continue>
QUESTION: <the one question that unblocks it>
```

⭐ **The `LOOKED` line is the one that saves the round trip.** ⚠️ Without it the
owner has to guess what the agent searched for, ⛔ **and half the time the
answer is that the search itself was wrong.**

> ## ⛔ A STOP IS NOT A FAILURE. IT IS THE ONLY HONEST OUTPUT WHEN THE INPUT IS MISSING.
> ⭐ **An agent that continues on an assumption produces work that looks
> finished** — and the assumption is invisible in the result.

---

## 6 · FRICTION — when a rule is in your way

```
1 · COMPLY              ⛔ even if it seems wrong
2 · LOG THE FRICTION    in the block
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
| `WRK-FRI-002` | **Each friction is logged with its four fields** | 🔒 | ⚠️ date · rule · block · reason |
| `WRK-FRI-003` | ⭐ **A rule is flagged at N frictions in DISTINCT blocks** | 🔒 | see below |
| `WRK-FRI-005` | ⛔ **The agent never infers N** | 🔒 | ⭐ it is declared, or it is the engine default |

### ⭐ N IS DECLARED, NEVER GUESSED

```
friction_threshold: 3
```

⬜ **The installation may change that number** — ⚠️ **once, here, in writing.**
⛔ **What it may not do is leave it undeclared and let each reader assume one.**

⚠️ **Measured in this engine's own code:** the validator carried the number as
a constant while this file said it belonged to the owner. ⭐ **A validator that
decides a number the doctrine assigns to somebody else is measuring a decision
nobody took.**
| `WRK-FRI-004` | ⛔ **A flagged rule is never changed automatically** | 📖 | ⭐ it escalates to the owner |

### ⭐ THE LOG FORMAT — four fixed fields

```
<date> · rule: <name> · block: <id> · reason: <why it got in the way>
```

⭐ **Four fields, and each one is load-bearing:** the date orders them, the rule name groups them,
⭐ **the block id is what makes the count meaningful**, and the reason is what the owner reads.

### ⭐ DETECTION IS ARITHMETIC, NOT INTERPRETATION

| Two details make it work | ⭐ Why |
|---|---|
| ⭐ **DISTINCT blocks, not repetitions** | ⛔ three frictions in the *same* block is one task chafing; in *distinct* blocks, **the rule is wrong** |
| ⭐ **It never expires** | ⚠️ **the problem is not the speed of the friction — it is its recurrence** |

⚠️ **Without the first, any long task raises a false alarm** — and then the mechanism gets
ignored, which costs more than never having it.

⭐ **And the second matters more than it looks:** if three frictions accumulate over six months,
⛔ **it is still a signal.** A window would make the mechanism forget exactly the slow, structural
problems it exists to find.

### ⭐ WHAT HAPPENS WHEN IT FIRES

⛔ **The rule is NOT changed automatically.** It escalates with the frictions and their reasons,
and the owner decides between three outcomes:

| | |
|---|---|
| **adjust** | the rule was too strict, or wrongly scoped |
| ⭐ **keep, with a documented exception** | the rule is right; this case is not it |
| **remove** | ⚠️ it was protecting something that no longer exists |

> ## ⭐ THE SYSTEM DETECTS. THE OWNER DECIDES.
> ⛔ **There are no immutable rules — there are pointers to rules, improving with the owner's
> criterion.** ⚠️ A rule that can never change is a rule people route around, and the friction
> does not disappear: **it moves out of sight.**

### ⛔ WHY NOT JUST ASK EVERY TIME?

| The alternative | ⛔ Why it fails |
|---|---|
| **ask whenever something chafes** | ⚠️ the owner becomes a bottleneck, and the system gets slow |
| ⭐ **let the agent skip rules it judges wrong** | ⛔ **in a month the rules are the agent's again** |

⭐ **Logging and accumulating is what lets the system learn without constant supervision.**

### ⭐ THE TWO SHAPES, SIDE BY SIDE

```
✅ NORMAL FRICTION — logged, work continues
   rule: publish-on-explicit-order
   reason: wanted to publish an already-verified urgent fix
   action: COMPLIED · left it unpublished · continued

⛔ THE EXCEPTION — stopped immediately
   rule: no hardcoded values
   reason: wanted to read a key from a constant, to test quickly
   ⚠️ STOPPED AND ASKED — the fallback was hiding a divergence between
      environments. Continuing would have left production broken, silently.
```

⭐ **The difference is not how annoying the rule was.** ⛔ **It is whether complying causes damage
or merely costs time.**

---

## 7 · FIX, NOT PATCH

> ## ⭐ THE ONE QUESTION THAT CHANGES EVERYTHING
> | ⛔ A patch asks | ⭐ A fix asks |
> |---|---|
> | *"where does it fail?"* | *"**why does this failure exist, and where else does it live?**"* |

### The procedure — ⛔ mandatory

| # | Step | ⚠️ |
|---|---|---|
| 1 | ⛔ **Do not write the fix yet** | |
| 2 | **Read the piece and its surroundings** | ⭐ evaluate the construction |
| 3 | ⭐ **Find every consumer before deciding** | ⚠️ **this is the step that gets skipped** |
| 4 | **Choose the real solution** — ⭐ even if it means another route | |
| 5 | **Declare the propagation in the block** | its connections and its sub-blocks |
| 6 | ⭐ **That sequence is what gets repeated** — it is the habit, not the one-off | |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `WRK-FIX-001` | ⭐ **Every consumer measured before the fix** | 📖 | ⛔ nothing verifies this |
| `WRK-FIX-002` | ⭐ **Every AFFECTED consumer resolved — only affected copies changed** | 📖 | ⚠️ ⛔ see below |
| `WRK-FIX-003` | **The propagation is declared in the block** | 🟡 | connections and sub-blocks updated |
| `WRK-FIX-004` | ⭐ **A different route is allowed, and often correct** | 📖 | ⛔ see below |

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

### ⚠️ AND THE PRECISION `WRK-FIX-002` NEEDS

⛔ ***"All copies"* is too absolute, and following it literally does damage.**
⭐ **Some copies are supposed to differ:**

| ⛔ Not a copy to fix | ⭐ Why |
|---|---|
| a fixture or a snapshot | it records a past state on purpose |
| ⭐ **a historical migration** | ⚠️ **rewriting it changes what already happened** |
| an example in documentation | it illustrates, it does not run |
| ⭐ **a deliberately different implementation** | ⛔ §2 — different owners, legitimate coincidence |

⭐ **So the rule is: every AFFECTED consumer is resolved; only affected copies
change.** ⚠️ **And which ones are affected is the impact map's answer (§8), not
a guess.**

### ⛔ WHAT THIS RULE IS **NOT**

| ⛔ Not this | ⭐ Why |
|---|---|
| *"never fix quickly"* | ⚠️ **a typo is a typo** |
| a rule for every change | ⭐ it applies when the piece **has declared dependents** — which is what §2 detects |
| a ban on rethinking the approach | ⭐ **if the real solution means building it differently, that is the right answer** |

⭐ **`WRK-FIX-004` exists because the opposite reading is the common one.** ⚠️ *"Find the real
cause"* gets read as *"fix it where it is, properly"* — ⛔ **when sometimes the real answer is that
the piece should not exist in that shape at all.**

### ⚠️ WHEN THE GATE WARNS

⭐ **Editing a piece with declared dependents WARNS — it does not block.** ⛔ **Blocking the daily
path would be pure friction**, and the propagation is already handled by the lane: §2 sends
anything with declared dependents to `full-block`, ⭐ **chosen from the graph and never from
judgement.**

⭐ **What the gate prints IS the receipt:** the piece, why it matters, ⭐ **what to assess — which
is the procedure above** — and the documented way out.

> ## ⭐ THE GATE OPENS WHEN STEPS 2-4 ARE DEMONSTRABLY DONE.
> ⛔ Not when someone says they were.

---

## 8 · ⭐ THE IMPACT MAP — the measurement, written down

⛔ **A measurement that is not written is a measurement that gets redone or
forgotten.** ⭐ **§7 says find every consumer; this is where the finding lands.**

```
TARGET:      <the piece being changed>
DEPENDENTS:  <every piece that depends on it · measured, with the date>
CONSUMERS:   <the subset THIS change actually reaches>
PROPAGATION: <target → consumer, for each>
CHANGED:     <what was actually edited>
VALIDATED:   <each consumer, with what proves it>
UNAFFECTED:  <a dependent this change does NOT reach, and why>
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `WRK-IMP-001` | ⭐ **Dependents are measured before the first edit** | 📖 | ⛔ see §7 step 3 |
| `WRK-IMP-002` | ⭐ **The map states WHICH dependents this change does not reach** | 📖 | ⚠️ silence means *not checked*, not *unaffected* |
| `WRK-IMP-003` | **Every consumer listed is validated, or the block does not close** | 🟡 | ⭐ a consumer with no evidence is untested |

⭐ **`WRK-IMP-002` is the row that separates a map from a list.** ⛔ **A dependent
left off the map cannot be told apart from one nobody looked at** — and the
second is the one that breaks.

### ⭐ WHAT COUNTS AS EVIDENCE HERE

| ✅ Evidence | ⛔ Not evidence |
|---|---|
| the graph output, ⭐ **with the date it was taken** | *"I checked"* |
| the list of consumers found | ⚠️ *"looks correct"* |
| a test or a run, per consumer | *"should work"* |
| ⭐ **the exact id that resolved** | ⛔ *"probably unaffected"* |

⭐ **The four on the right are the same sentence in four disguises:**
⛔ **confidence with nothing behind it.**

---

## 9 · ⭐ HOW THE FOUR CONNECT — they are one decision, taken in order

```
a change arrives
      │
      ▼
§2  WHICH LANE?          ── from the graph, never an estimate
      │                     dependents → full-block
      ▼
§3  WHAT MAY I READ?     ── only what is declared
      │                     no match → ⛔ STOP AND ASK
      ▼
§5  WHERE IS THE FIX?    ── every consumer, before the first line
      │                     all copies, never one
      ▼
§4  DID A RULE CHAFE?    ── comply · log · continue
                            N distinct blocks → the owner decides
```

⚠️ **The order is not decorative.** ⭐ **§2 decides how much process; §3 bounds what you may look
at while deciding; §5 is what you do once you have looked; §4 is what happens when one of the
three gets in your way.** ⛔ **Taken out of order, each one asks for information the previous one
was supposed to produce.**

---

## 10 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **the lane chosen by estimate** | ⚠️ a change treated as trivial that propagates — ⭐ **found four commits later** |
| ⭐ **the graph read from memory** | ⛔ the wrong lane, chosen confidently |
| **reading an undeclared block** | ⛔ one block's assumptions leak into another's work, invisibly |
| ⭐ **inferring a block from a similar name** | ⚠️ **the wrong work, done well** |
| **scanning everything "for context"** | ⭐ the cost that ends a session, and nothing warned |
| ⭐ **skipping a rule instead of logging it** | ⛔ **the rule stops existing, and nothing records that it did** |
| **counting frictions in the same block** | ⚠️ a false alarm — ⭐ and then the mechanism gets ignored |
| **fixing one copy** | ⭐ the same bug returns wearing a different symptom |
| **patching because the fix is inconvenient** | ⛔ ⭐ **the cause survives, and now it has cover** |

---

## 11 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ the friction threshold, the lane names | the owner of the instance, ⚠️ **declared once** |
| the rules and their IDs | whoever maintains the engine, through a recorded decision |
| ⛔ turning a 📖 into a claim of enforcement | **nobody** — ⭐ ⛔ **that is the worst lie this system can tell** |
| ⛔ adding a third way to cross between blocks | **nobody** — ⚠️ ⭐ every extra route is one nobody audits |

---

Related: `README.md` (⭐ the three document types) · `contract-block.md` (⭐ **the lane lives in §A,
the connections in §C, the friction log in §H — this file writes into all three**) ·
`rule-inheritance.md` (⭐ why rules add up only through a declared connection, and §4 the order of
effects) · `contract-document.md` · `../memory/principles/owner-2-dev.md` (⭐ what sequences the
work) · `../memory/principles/expertise/dev-backend.md` (⭐ §2.1 — one implementation of a rule,
which is what §5 restores) · `../bin/check-work` (what enforces the 🔒 rows).
