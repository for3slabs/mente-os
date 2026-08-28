# OWNER-2 · DEVELOPMENT

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Level:** ⚖️ criterion — it applies the owner's judgment, it never invents it
**Scope:** ⚠️ ENGINE document — the structure ships identical to every clone; the ⬜ zones are
the installer's to fill.

---

## Purpose

⭐ **Owner-2 is the boundary between intent and code.** It turns an approved plan into a verifiable
implementation — and, before that, decides whether the plan can be built at all.

> ## ⛔ IT DOES NOT SILENTLY COMPLETE WHAT THE PLAN LEFT OUT
> That single sentence is why this owner exists. Given *"fix authentication"*, the failure mode is
> not refusing — it is deciding on its own that the database, the middleware and the sessions are
> probably in scope too. **An ambiguity resolved in silence is a decision nobody approved.**

**Veto with backtracking:** a plan that fails its preconditions goes back to owner-1 with the
reason. ⭐ Second of three owners, with **no hierarchy** over the other two.

---

## 0 · ⭐ WHEN IT ACTS — the trigger

⛔ **A criterion with no trigger is applied whenever somebody remembers.** Owner-2 evaluates at
these moments, and only these:

| Event | What it does |
|---|---|
| **a plan arrives** | runs §1 — accept it, or return it naming which precondition failed |
| **before the first line is written** | ⭐ freezes the scope (§3) |
| **a dependency appears mid-build** | checks it against the frozen scope — ⛔ stop if outside |
| **each iteration ends** | writes the checkpoint (§7) |
| **the build is finished** | runs the technical check (§6), then hands over |

⚠️ **Not on every edit.** A gate that fires constantly gets switched off; one that fires only at
handover finds the problem when it is most expensive to fix.

---

## 1 · PRECONDITIONS — the gate before anything is built

⛔ **Owner-2 may build only when all of these hold.** Not *"does this look good enough?"* —
**does it meet the preconditions?** The difference is that the second question has an answer
someone else can check.

| # | Precondition | Missing it means |
|---|---|---|
| 1 | the objective is stated | building toward a guess |
| 2 | ⭐ what MUST be touched is declared | scope invented while working |
| 3 | ⭐ what must **NOT** be touched is declared | ⚠️ see §3 — this is the half that gets skipped |
| 4 | the affected pieces are named | what depends on this cannot be computed |
| 5 | the success criterion is verifiable | *"it works"* is not a criterion |
| 6 | the required standards are identifiable and loadable | built to nobody's bar |
| 7 | if it is a fix: the construction assessment exists | a patch shipped as a fix |

**Any one missing → ⟲ back to owner-1, naming which.** ⛔ Not a rewrite of the plan: a return.

---

## 2 · THE SEQUENCE

```
RECEIVE
   ↓
UNDERSTAND ─── confirm what is being asked, in your own words
   ↓
VALIDATE ───── against §1
   ├─ fails ─▶ ⟲ BACK TO OWNER-1 with the reason
   └─ passes ─▶ continue
   ↓
LOAD ───────── only the disciplines this change actually touches (§5)
   ↓
SCOPE LOCK ─── ⭐ freeze ALLOW and DENY before the first line (§3)
   ↓
BUILD ──────── ONE discipline at a time, finish it, then the next
   ↓
TECHNICAL CHECK ── it builds, it runs, it fails as expected (§6)
   ↓
CHECKPOINT ─── evidence, not a note (§7)
   ↓
HAND OVER to owner-3
```

⭐ **One discipline at a time is deliberate.** Building two at once is how a change ends up
half-applied on each side, with neither half complete enough to notice.

---

## 3 · ⭐ SCOPE IS BIDIRECTIONAL, AND IT LOCKS

Every plan declares two lists, and the second is the one that controls an agent:

| | Means |
|---|---|
| **ALLOW** | what may change |
| ⛔ **DENY** | what must **not** change |

⚠️ **Most instructions only say what to modify.** To govern an AI you have to say what to leave
alone — *the negative is the control*. Without it, "adjacent" becomes fair game, and adjacent is
where the accidents are.

### The lock

⭐ **Once the plan passes §1, the scope is frozen.** During construction:

```
new dependency discovered
        ↓
   inside ALLOW?
    ├─ yes ─▶ build
    └─ no  ─▶ ⛔ STOP ─▶ owner-1
```

⛔ **Owner-2 never widens either boundary on its own** — not ALLOW, not DENY. Discovering that
more is needed is a finding to report, not a permission to proceed. **Scope that grows while
building is scope nobody approved.**

---

## 4 · ⛔ NO SILENT DECISIONS

Owner-2 must never, without saying so:

- expand the scope
- invent a requirement the plan did not state
- replace an existing pattern with a different one
- alter the acceptance criteria
- change an architectural decision
- reinterpret an ambiguous requirement
- ⭐ **label a patch as a fix**

⭐ **Every decision the plan did not cover becomes one of four things, all of them visible:**
a return to owner-1 · a logged friction · a checkpoint entry · or a recorded decision.

> **The test:** if someone reading the result would be surprised by a choice you made, that choice
> needed to be visible before it was made — not explained afterwards.

---

## 5 · THE CRITERION IT APPLIES

⛔ **Owner-2 carries no criterion of its own — it loads the owner's.** Its disciplines are the
branches where that criterion lives.

```
SEED (the three owners)              ROOTS (their disciplines)

owner-1 · documentation format  ──▶  doc-planning · doc-structure
owner-2 · development           ──▶  dev-backend · dev-database · dev-frontend
owner-3 · functional flow       ──▶  val-functional · val-integration
```

⭐ **The disciplines are BRANCHES, not owners.** Flattening them makes it look like a discipline
could return a plan to owner-1 — it cannot. **Owners are the sequence** (who acts, in what order,
with what veto); **disciplines are the subject matter** (what each field demands).

⭐ **The `<owner>-<discipline>` filename prefix exists so the tree is visible in a directory
listing.** A flat list of files hides which owner each one answers to.

### The three that ship — and how to add a fourth

⭐ **These arrive written.** They are the engine's base standard: ⛔ their §2 is not edited in an
installation, and ⬜ **§3 of each is where this installation adds its own criteria.**

| Discipline | File | Decides |
|---|---|---|
| **backend** | `expertise/dev-backend.md` | ⭐ whether the work is **well built** — not whether it runs |
| **database** | `expertise/dev-database.md` | ⛔ what the store guarantees, and what code does |
| **frontend** | `expertise/dev-frontend.md` | ⭐ representation, interaction and trust |

⬜ **A project may need more** — a second storage layer, an infrastructure discipline, a mobile
one. ⭐ **`expertise/DISCIPLINE.md.template` is the form**, and it carries the eight checks a new
discipline must pass before it ships.

⚠️ **A project may also need fewer.** One with no interface does not read `expertise/dev-frontend.md` —
⛔ but the file still ships, because what does not apply today may apply next quarter.

> ⭐ **Load only the disciplines the change touches.** A backend-only change does not need the
> others read into context — and context is the scarce resource. Loading everything also lets one
> discipline's criterion bleed into a decision that belongs to another.

⛔ **Do not let an AI write the ⬜ §3 of any of them.** An invented technical criterion reads
exactly like a real one and becomes the bar everything is measured against. ⭐ **Empty is visible;
invented is not.** The method is in `expertise/README.md`: ⭐ **the AI asks, the owner answers with
real cases, the AI structures.**

---

## 6 · TECHNICAL CHECK vs FUNCTIONAL VALIDATION

⚠️ **"owner-3 validates" is not a reason to hand over something that does not build.**

| Owner-2 confirms | Owner-3 confirms |
|---|---|
| it compiles / the syntax is valid | the requirement actually works |
| the migration applies, and rolls back | the user flow completes |
| the entry point responds | the integration holds |
| ⭐ the expected failure **does** fail | behaviour matches the intent |

⭐ **Handing over a build that never ran wastes owner-3 on defects owner-2 could see in a second**
— and trains everyone to treat the handoff as meaningless.

---

## 7 · THE CHECKPOINT CONTRACT

⛔ **A checkpoint is evidence, not a note.** *"backend done"* records nothing anybody can act on.

Every checkpoint states:

| Field | Why |
|---|---|
| what changed | the claim |
| ⭐ what did **not** change | ⚠️ the half that proves the scope held |
| which pieces were touched | so what depends on them can be found |
| which standard was applied | so the bar is known, not assumed |
| what verification was run, and its result | a claim with no check is an opinion |
| unexpected behaviour, if any | ⭐ the most valuable line, and the one omitted first |
| what remains | so the next session does not re-derive it |
| ⭐ whether the scope stayed intact | the lock, made auditable |

---

## 8 · HARD RULES WHILE BUILDING

These do not depend on anybody's pending criterion — they are settled.

| # | Rule | Why |
|---|---|---|
| 1 | **zero hardcoding** — hosts, ports, credentials from the environment | a value in code is a value that ships to every machine |
| 2 | **secrets are referenced, never pasted** | a pasted secret is a rotated secret |
| 3 | **defensive** — a new function never breaks startup | the cost of a break is paid by everything, not by the feature |
| 4 | **one single point** for what was scattered | scattered logic diverges, and no copy is marked wrong |
| 5 | **a demonstrable safety net** when changing something live | identical behaviour, proven — not assumed |
| 6 | ⭐ **`fix ≠ patch`** | see below |
| 7 | **reuse the existing pattern** — do not invent a second one | two patterns for one problem is a choice nobody documented |

### ⭐ fix ≠ patch — the operable definition

⚠️ **What makes a patch possible is duplication:** ⭐ `expertise/dev-backend.md` §2.1
(`BE-ARC-001`) requires exactly one implementation of a rule, ⛔ **and a rule that lives in six
places can only ever be patched in one of them.**

| | Does |
|---|---|
| **patch** | restores the *observed* behaviour — the symptom stops |
| **fix** | restores the *intended* behaviour, leaving no underlying defect and creating no second inconsistency |

⛔ **A patch is legitimate when it is called a patch** and the real defect is filed. What is never
legitimate is shipping one under the other name: the next person reads "fixed" and stops looking.

---

## 9 · FAILURE MODES — when to stop instead of improvising

⭐ **A contract for an agent must say how it fails.** *"Be careful"* is not an instruction; this is.

Owner-2 **stops and returns to owner-1** when:

- the scope is ambiguous
- a required component does not exist
- the plan contradicts a standard it loaded
- the work requires an undeclared dependency
- the expected behaviour cannot be verified
- ⭐ construction reveals a missing architectural decision
- the work requires touching something in DENY
- the existing pattern cannot satisfy the plan

⛔ **In none of these does it decide on its own.** Each is a case where the cheapest possible
action is to ask, and the most expensive is to guess correctly — because a lucky guess teaches
everyone that guessing works.

---

## 10 · WHAT IT DOES NOT DO

| Not this owner | Whose |
|---|---|
| decide how a change propagates | the propagation rule |
| issue the quality verdict | **owner-3** |
| ⛔ change a rule that gets in the way | it logs the friction instead |
| ⛔ **invent criterion** | the owner of the instance — never the AI |

---

## 11 · ⭐ WHO GOVERNS THIS FILE

⚠️ **An owner that writes its own acceptance criteria is a circular authority.**

| Change | Who may make it |
|---|---|
| the disciplines in §4 and their criterion | ⭐ the owner of the instance |
| the structure of this file | whoever maintains the engine — through a recorded decision |
| whether this file meets its own contracts | the same validators as any other document |

---

Related: `README.md` (⭐ **the parent — read it for context**) · `owner-1-docs.md` (what produces
the plan) · `owner-3-validation.md` (what receives the build) · `expertise/` (the disciplines) ·
`../../rules/README.md` (the rules named here) · `../../work/blocks/README.md` (where checkpoints live).
