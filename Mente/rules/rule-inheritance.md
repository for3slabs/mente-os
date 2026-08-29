# RULE · INHERITANCE

**Status:** current · **Type:** rule · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** every rule in the system — ⭐ **including the ones in this folder**
**Enforcement:** 🔒 partial — `bin/check-inheritance`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone

---

## 0 · WHAT THIS FILE IS

> ## ⭐ The map of WHERE a rule lives — and why a rule with no declared level is a defect.

⚠️ **The failure it prevents: contamination.** ⛔ **One project's rules injected into every piece
of work**, forever, because nothing said which level they belonged to.

⭐ **A rule written with no declared level is not a strict rule. It is a rule that applies in the
wrong places** — and the places where it does not belong are where people learn to ignore it.

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
| `INH-LVL-001` | ⭐ **Every rule declares its level** | 🔒 | ⛔ no level means it applies everywhere by accident |
| `INH-LVL-002` | ⛔ **A universal rule never names a specific thing** | 🔒 | ⚠️ a path, a service, a repository — ⭐ then it is not universal |
| `INH-LVL-003` | **A project rule that holds anywhere belongs one level up** | 🟡 | apply the test above |

⭐ **`INH-LVL-002` is the one a script can actually catch**, and it catches the exact defect that
produced this rule: **a rule naming one place, living where every place reads it.**

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

## 4 · WHEN LEVELS COMBINE — the rules ADD UP

```
effective set = universal + project + (this block) + (a block it DECLARES)
```

| Situation | Effective set |
|---|---|
| one block open | universal + project + that block |
| ⭐ **this block DECLARES another as a dependency** | + that block's rules |
| ⛔ **two blocks with no declared connection** | ⚠️ **their rules do NOT mix** |
| ⭐ **a conflict between two levels** | 🔴 **the stricter one wins** — ⛔ never the more permissive |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `INH-SUM-001` | ⭐ **Rules add up only through a DECLARED connection** | 🔒 | ⚠️ the connection exists in the block |
| `INH-SUM-002` | ⭐ **On conflict, the stricter rule wins** | 📖 | ⛔ ⭐ two rules never average out |

> ## ⭐ "THE STRICTER ONE WINS" IS NOT A TIEBREAK — IT IS THE WHOLE MODEL
> ⛔ **Averaging two rules produces a third that nobody wrote**, and it is always the weaker one.
> ⚠️ **The strict rule exists because something went wrong; the permissive one exists because
> nothing has gone wrong there yet.**

⚠️ **Why rules only add through a declared connection:** ⭐ **the isolation rule protects context,
which is the scarce resource.** ⛔ If reading another block's rules were free, *"loading the rules
for context"* becomes the way the gate stops meaning anything.

---

## 5 · ⭐ THE ROUTER IS NOT A RULE STORE

⛔ **The file an agent reads first is a ROUTER: it points at where the rules live. It does not
hold them.**

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `INH-RTR-001` | ⭐ **No rule is written in the router** | 🔒 | ⛔ a rule there has no declared level |
| `INH-RTR-002` | **The router names all three levels** | 🔒 | ⚠️ a level nobody points at is a level nobody reads |

> ## ⭐ THIS IS THE BUG THIS FILE FIXES
> ⚠️ **A rule written in the router has no level** — so it applies to everything, everywhere,
> including the projects it was never about. ⛔ **That is not strictness. That is contamination
> wearing strictness as a costume.**

---

## 6 · ⛔ WHAT IT COSTS TO BREAK IT

| Broken | ⭐ The cost |
|---|---|
| **a rule with no level** | ⛔ it contaminates every project that inherits it |
| ⭐ **a universal rule naming one place** | ⚠️ **it is meaningless everywhere else — and meaningless rules teach people to skim** |
| **a block loosening an inherited rule** | ⛔ ⭐ **the rule above stops protecting anything, invisibly** |
| **a block repeating a rule from above** | ⚠️ the two copies diverge, and neither looks wrong alone |
| **rules mixing with no declared connection** | ⭐ the gate that protects context stops meaning anything |

---

## 7 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ the project level — its rules and their content | ⭐ the owner of the instance |
| the three levels and the direction of inheritance | whoever maintains the engine, through a recorded decision |
| ⛔ allowing a level to loosen what it inherited | **nobody** — ⭐ ⚠️ **it would empty every rule above it at once** |

---

Related: `README.md` (⭐ **the three document types, and the law that rules tighten and never
loosen**) · `contract-block.md` (⭐ §B the scope, §C the declared connections that let rules add
up) · `rule-working-in-a-block.md` (⭐ §3 isolation — why rules do not mix by default) ·
`contract-document.md` · `../bin/check-inheritance` (what enforces the 🔒 rows).
