# RULE · INHERITANCE

**Status:** current · **Type:** rule · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every rule in the system — ⭐ **including the ones in this folder**
**Enforcement:** 🔒 partial — `bin/check-inheritance`
**Level:** 🌐 universal — ⭐ travels identical to every clone; a lower level may ADD or TIGHTEN, never loosen
**Verified by:** `bin/check-inheritance` · `bin/probes/probe-inheritance.py`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone

---

## 0 · WHAT THIS FILE IS

> ## ⭐ How an agent determines, deterministically, WHICH rules govern it — before it acts.

⚠️ **The failure it prevents: contamination.** ⛔ **One project's rules injected into every piece
of work**, forever, because nothing said which level they belonged to.

⭐ **A rule written with no declared level is not a strict rule. It is a rule that applies in the
wrong places** — and the places where it does not belong are where people learn to ignore it.

### ⭐ THREE THINGS, AND THIS FILE MUST NOT CONFUSE THEM

| | Decides |
|---|---|
| ⭐ **inheritance** | which rules the agent **KNOWS** — §2, §3 |
| ⭐ **resolution** | which of them are **ACTIVE** right now — §5, §6 |
| ⭐ **enforcement** | whether the action **MAY RUN** — the gates, and each rule's `Enf` column |

⛔ **Collapsing them is how a system ends up "having rules" that nothing applies.**

### ⭐ THE MEASUREMENT THAT PRODUCED THIS RULE

⚠️ **A set of eight rules held up as universal. Only five actually were:**

| The rule | Its real level |
|---|---|
| a gate before reading another installation | 🏢 **project** — ⛔ it names something that exists in one place |
| deploy-target-first | 🏢 **project** — ⛔ only matters where that target exists |
| the other six | 🌐 universal |

⛔ **And the router file was worse: three rules naming specific directories, injected into every
session of every project.**

> ## ⭐ THE CONSEQUENCE, STATED PLAINLY
> ⚠️ **Someone clones this engine for unrelated work and inherits a rule about a directory that is
> not theirs, on a machine that is not theirs.** ⛔ **That is contamination**, and it is why this
> file exists.

---

## 1 · ENFORCEMENT

| | Means |
|---|---|
| 🔒 **lock** | ⭐ a script refuses — ⚠️ and it has been seen to fail |
| 🟡 **prompt** | the agent asks before proceeding |
| 📖 **discipline** | ⛔ **nothing verifies this** |

**IDs are permanent.** `INH-<area>-<nnn>` — ⛔ never renumbered, never reused.

---

## 2 · THE THREE LEVELS

```
🌐 UNIVERSAL      the engine's base rules
   conduct that holds for any work, any project, any block
   ⭐ applies BEFORE any block exists — from the first response of a session
        │  inherits
        ▼
🏢 PROJECT        this installation's own rules
   ⭐ what is true here and would be false somewhere else
        │  inherits
        ▼
📦 BLOCK          the scope of one open block
   ⭐ applies only while that block is open
```

### ⭐ THE TEST THAT ASSIGNS A LEVEL

> ## Would this rule still hold if the level below did not exist?

| Answer | Level |
|---|---|
| it holds with no block open | 🏢 project or 🌐 universal |
| ⭐ **it holds in ANY project — even one that does not exist yet** | 🌐 **universal** |
| it only makes sense while this specific work is open | 📦 **block** |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `INH-LVL-001` | ⭐ **Every rule declares its level** | 🔒 | `bin/check-inheritance` · ⛔ measured: 13 of 13 declared none |
| `INH-LVL-002` | ⛔ **A universal rule never names a specific thing** | 🔒 | ⚠️ a path, a service, a repository — ⭐ then it is not universal |
| `INH-LVL-003` | **A project rule that holds anywhere belongs one level up** | 🔒 | `bin/check-inheritance` · a row marked project-level inside the universal file |

⭐ **`INH-LVL-002` is the one a script can actually catch**, and it catches the exact defect that
produced this rule: **a rule naming one place, living where every place reads it.**

⚠️ **The level IS the scope.** ⛔ A rule does not carry a separate scope field — **it carries a
location**, and adding a field that repeats the location is the duplication `../memory/principles/expertise/doc-structure.md`
§2.3 forbids.

---

## 3 · ⭐ THE INHERITANCE RULE

> ## A LOWER LEVEL MAY ONLY ADD OR TIGHTEN. IT CAN NEVER LOOSEN.

⚠️ **This is where the inheritance analogy breaks on purpose:** ⛔ **there is no override that
widens permission.** A child cannot grant itself what the parent forbade.

| Operation | | ⭐ Example |
|---|---|---|
| **ADD** a rule the parent does not have | ✅ | a block forbids touching a specific area |
| **TIGHTEN** an inherited rule | ✅ | ⭐ *"publish only on explicit order"* → *"and here, publishing is a deploy"* |
| ⛔ **LOOSEN** an inherited rule | **never** | ⚠️ a block cannot grant itself what the level above denied |
| **Grant an exception** | ⛔ only the owner — ⭐ **and it becomes a NEW rule at the parent's level**, recorded |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `INH-DIR-001` | ⛔ **No level loosens what it inherited** | 🔒 | ⚠️ compare against the level above |
| `INH-DIR-002` | ⭐ **An exception is written at the PARENT's level, never as a local carve-out** | 📖 | ⛔ nothing verifies this |
| `INH-DIR-003` | ⛔ **A block never repeats a rule that already exists above** | 🔒 | ⭐ see below |

### ⭐ WHY REPEATING IS ALSO BANNED — not only loosening

⚠️ **A repeated rule looks harmless and is not.** ⛔ **Two copies of one rule diverge, and neither
looks wrong on its own** — the defect exists only between them.

⭐ **A block inherits. It does not restate.** If a reader has to check two places to know what a
rule says, ⚠️ **they will eventually check only one.**

### ⛔ WHY LOOSENING IS BANNED — the measured reason

⭐ **A scope rule that existed and was violated repeatedly still protected something, because it
was violated visibly.** ⚠️ **A rule a block can exempt itself from protects nothing at all** — the
exemption is invisible, and it looks exactly like compliance.

| Case | ⭐ What it shows |
|---|---|
| a block adding *"and here, this action deploys"* | ✅ **tightening** — stricter, not weaker |
| ⭐ **a gate refusing even the owner** before checking permission | ⛔ some rules protect cost, and cost applies to whoever holds authority |
| something locked at the tool level | ⛔ ⭐ **a block declaring otherwise would just be lying on paper** |

---

## 4 · 🔴 NO PRIVILEGE ESCALATION

> ## ⭐ A CHILD CONTEXT MUST NOT OBTAIN AUTHORITY ITS PARENT DOES NOT HAVE.

| Inheritance… | |
|---|---|
| **MAY** remove available actions | ✅ |
| **MAY** add restrictions | ✅ |
| ⛔ **MUST NOT** increase authority | 🔴 **never** |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `INH-ESC-001` | ⭐ **No level grants an action denied above it** | 🔒 | ⛔ compare effects, not wording |
| `INH-ESC-002` | ⭐ **A dependency shares its RULES, never its AUTHORITY** | 📖 | ⚠️ see §6 |

⚠️ **This is the same idea as §3, said as what it actually is.** ⭐ *"Does not loosen"* is an
editorial rule about wording; ⛔ **"does not escalate" is a security property**, and it is what a
script can be pointed at.

---

## 5 · ⭐ WHAT "STRICTER" MEANS — declared, never judged

⛔ **Saying *"the stricter rule wins"* without defining stricter leaves the decision to whoever is
reading.** ⚠️ ***"You may not do X"* and *"you may do X with approval"* must not be compared by
interpretation.**

> ## ⭐ THE ORDER OF EFFECTS, strongest first:

| Effect | Means |
|---|---|
| 🔴 **DENY** | ⛔ the action never runs |
| 🟠 **REQUIRE_APPROVAL** | it runs only after an explicit yes |
| 🟡 **RESTRICT** | it runs, ⭐ under a stated condition |
| 🟢 **ALLOW** | it runs |
| ⬜ **INFORMATIONAL** | ⚠️ it states something, it decides nothing |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `INH-PRC-001` | ⭐ **On conflict, the strongest effect wins** | 🔒 | ⛔ by this table, never by reading |
| `INH-PRC-002` | ⛔ **Two effects never average out** | 🔒 | ⚠️ the SIGNAL is measured — hedging inside a rule row — never the reasoning |
| `INH-PRC-003` | ⭐ **A rule whose effect cannot be classified is DENY** | 📖 | see §7 |

> ## ⭐ "THE STRICTER ONE WINS" IS NOT A TIEBREAK — IT IS THE WHOLE MODEL
> ⛔ **Averaging two rules produces a third that nobody wrote**, and it is always the weaker one.
> ⚠️ **The strict rule exists because something went wrong; the permissive one exists because
> nothing has gone wrong there yet.**

---

## 6 · WHEN LEVELS COMBINE — the rules ADD UP

```
effective set = universal + project + (this block) + (a block it DECLARES)
```

| Situation | Effective set |
|---|---|
| one block open | universal + project + that block |
| ⭐ **this block DECLARES another as a dependency** | + that block's rules |
| ⛔ **two blocks with no declared connection** | ⚠️ **their rules do NOT mix** |
| ⭐ **a conflict between two levels** | 🔴 **the strongest effect wins** — §5 |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `INH-SUM-001` | ⭐ **Rules add up only through a DECLARED connection** | 🔒 | ⚠️ the connection exists in the block |
| `INH-SUM-002` | ⭐ **Conflicts resolve by §5, never by judgement** | 📖 | ⚠️ **nothing verifies this** — ⛔ a script sees the outcome, never which method produced it |
| `INH-SUM-003` | 🔴 **A dependency cycle is invalid** | 🔒 | ⭐ see below |

### ⭐ WHAT `DEPENDS ON` MEANS — and what it does NOT

| ✅ Declaring a dependency… | ⛔ It does NOT… |
|---|---|
| inherits that block's **applicable rules** | ⛔ inherit its objective or its task |
| ⭐ lets you read what it **declared** | ⛔ **inherit its authority** |
| — | ⛔ activate it |
| — | ⚠️ **permit modifying it** |

> ## ⭐ INHERITING RULES IS NOT INHERITING AUTHORITY.
> ⛔ **A block that depends on another gains its CONSTRAINTS, not its permissions** — ⚠️ otherwise
> a dependency becomes the way to acquire access nobody granted.

### 🔴 A cycle is invalid

⭐ `A → B → C → A` **cannot be resolved**: there is no order in which the effective set is
complete. ⚠️ **And a resolver that meets one runs forever** — ⛔ **a validator stuck in a loop
reports nothing, which reads exactly like reporting no problem.**

⚠️ **Why rules only add through a declared connection:** ⭐ **isolation protects context, which is
the scarce resource.** ⛔ If reading another block's rules were free, *"loading the rules for
context"* becomes the way the gate stops meaning anything.

---

## 7 · ⛔ FAIL CLOSED — when the rules cannot be resolved

> ## ⭐ UNKNOWN IS NOT ALLOW. UNKNOWN IS STOP.

**The agent MUST stop when:**

| ⛔ Condition |
|---|
| the project cannot be identified |
| ⭐ **the active block cannot be identified** |
| a declared dependency does not resolve |
| ⚠️ **two effects conflict and neither is classifiable** |
| ⭐ **a rule declares no level** |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `INH-FCL-001` | ⭐ **An unresolvable rule set STOPS the action** | 📖 | ⛔ nothing verifies this |
| `INH-FCL-002` | ⭐ **The stop names WHICH resolution failed** | 📖 | ⚠️ *"unclear"* is not a report |

⭐ **This is the same third state the rest of the system already uses** — `UNKNOWN` in the document
contract, `NOT_MEASURED` in the functional criterion. ⛔ **Here it has teeth: an unresolved policy
does not default to permission.**

⚠️ **The failure it prevents is the quiet one:** ⭐ **an agent that cannot tell which rules apply
and proceeds anyway is an agent operating with no rules at all** — and from the outside that looks
identical to an agent following them.

---

## 8 · ⭐ THE ROUTER IS NOT A RULE STORE

⛔ **The file an agent reads first is a ROUTER: it points at where the rules live. It does not
hold them.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `INH-RTR-001` | ⭐ **No rule is written in the router** | 🔒 | ⛔ a rule there has no declared level |
| `INH-RTR-002` | **The router names all three levels** | 🔒 | `bin/check-inheritance` · ⚠️ a level nobody points at is a level nobody reads |

> ## ⭐ THIS IS THE BUG THIS FILE FIXES
> ⚠️ **A rule written in the router has no level** — so it applies to everything, everywhere,
> including the projects it was never about. ⛔ **That is not strictness. That is contamination
> wearing strictness as a costume.**

---

## 9 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **a rule with no level** | ⛔ it contaminates every project that inherits it |
| ⭐ **a universal rule naming one place** | ⚠️ **meaningless everywhere else — and meaningless rules teach people to skim** |
| **a block loosening an inherited rule** | ⛔ ⭐ **the rule above stops protecting anything, invisibly** |
| ⭐ **a dependency treated as authority** | ⛔ **access nobody granted, obtained by declaring a link** |
| **"stricter" left to interpretation** | ⚠️ ⭐ the model picks, and it picks the permissive one |
| **an unresolvable set treated as ALLOW** | ⛔ an agent running with no rules, looking compliant |
| **a block repeating a rule from above** | the two copies diverge, and neither looks wrong alone |
| **rules mixing with no declared connection** | ⭐ the gate that protects context stops meaning anything |

---

## 10 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ the project level — its rules and their content | ⭐ the owner of the instance |
| the three levels and the direction of inheritance | whoever maintains the engine, through a recorded decision |
| ⛔ allowing a level to loosen what it inherited | **nobody** — ⭐ ⚠️ **it would empty every rule above it at once** |
| ⛔ treating an unresolved set as permission | **nobody** — ⭐ §7 |

---

Related: `README.md` (⭐ **the three document types, and the law that rules tighten and never
loosen**) · `contract-block.md` (⭐ §B the scope and its two-levels test, §C the declared
connections that let rules add up) · `rule-working-in-a-block.md` (⭐ §3 isolation — why rules do
not mix by default) · `contract-document.md` (⭐ §7 — the same third state, under its own name) ·
`../bin/check-inheritance` (what enforces the 🔒 rows).
