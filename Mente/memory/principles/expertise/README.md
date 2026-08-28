# memory/principles/expertise/ — the disciplines · where criterion becomes concrete

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ **ENGINE** — ⭐ seven disciplines ship written; an eighth is yours.
**Governance:** declared as `engine` in the piece table · ✅ ships whole to every clone

---

## 📍 WHERE YOU ARE — read the parent first

```
Mente/
└── memory/              ← ⛔ INSTANCE · content never travels
    └── principles/      ← ENGINE · the criterion — who judges, and with what verdict
        └── expertise/   ← ⭐ YOU ARE HERE · what each judgement is actually made of
```

⭐ **The owner files say WHO rejects and WHEN. These say ON WHAT BASIS.** An owner with no
discipline behind it rejects on taste; ⛔ a discipline with no owner is criterion nobody applies.

👉 **Read `../README.md` first** if you have not.

---

## What a discipline is

A field of work with **its own criterion for what is well done**. Not a topic — a judgement.

| ⛔ A topic | ⭐ A discipline |
|---|---|
| *"about testing"* | *"decides whether something is proven to work"* |
| can be read | ⭐ **can reject something** |

⚠️ **The test:** if it cannot refuse anything, it is documentation, not a discipline.

---

## ⭐ THE SEVEN THAT SHIP — and what each one decides

| Discipline | Owner | ⭐ Decides |
|---|---|---|
| `doc-planning.md` | owner-1 | ⭐ **whether a plan can be executed** — before anything is built |
| `doc-structure.md` | owner-1 | ⭐ **where knowledge lives** — and which document is the truth |
| `dev-backend.md` | owner-2 | whether the work is **well built** — ⛔ not whether it runs |
| `dev-database.md` | owner-2 | ⭐ **what the store guarantees**, and what code guarantees |
| `dev-frontend.md` | owner-2 | representation, interaction and **trust** |
| `val-functional.md` | owner-3 | ⭐ **proving something works**, as opposed to believing it |
| `val-integration.md` | owner-3 | ⛔ **the seams** — whether the chain still works when every piece does |

⭐ **They ship written because they are the engine's base standard.** ⛔ **Their §2 is not edited
in an installation** — ⬜ **§3 of each is where you add your own criteria**, with your own prefix,
so what came with the engine and what you added never requires reading history to tell apart.

⚠️ **A discipline that does not apply to your project still ships.** A project with no interface
does not read `dev-frontend.md` — ⭐ **but what is irrelevant today may not be next quarter, and a
file nobody reads costs nothing.**

---

## ⭐ HOW THEY CONNECT — this is what makes them a system

```
       owner-1 ──▶ doc-planning ──▶ writes the success criterion
                                          │
       owner-2 ──▶ dev-* ────────▶ builds against it
                                          │
       owner-3 ──▶ val-* ────────▶ proves it   ◀── reads that same criterion
```

⭐ **Each file cites the others where a rule already has an owner.** ⛔ It never restates it:

| The rule | ⭐ Owned by | Cited from |
|---|---|---|
| **authorisation reads the verified session** | `dev-backend.md` §2.5 | `val-integration.md` |
| **fail loudly, never silently** | `val-integration.md` §2.5 | `dev-backend.md` |
| **one implementation of a rule** | `dev-backend.md` §2.1 | `val-integration.md` |
| **a default never points at something owned** | `dev-database.md` §2.2 | `val-integration.md` |
| ⭐ **a check must be seen to fail** | `val-functional.md` §4 | `dev-backend.md` · `dev-frontend.md` |
| **where a guarantee is enforced** | `dev-database.md` §2.2 | `val-integration.md` |
| ⭐ **the success criterion** | `doc-planning.md` §2.5 | `val-functional.md` |
| **pointer, never copy** | `doc-structure.md` §2.3 | ⭐ **all of them** |

> ## ⛔ TWO COPIES OF ONE RULE DIVERGE, AND NEITHER LOOKS WRONG ALONE
> ⭐ The defect exists only **between** them — and nothing reads between files. **That is why a
> shared rule has exactly one owner and everyone else cites it.**

---

## The shared vocabulary

⭐ **All seven use the same words for the same things.** ⛔ Two vocabularies in sibling files is
the divergence above, wearing a different hat.

| | Means |
|---|---|
| ✅ **PASS** | there is evidence it holds |
| 🔴 **FAIL** | ⛔ it ran and the evidence contradicts the criterion |
| ⬜ **NOT_MEASURED / UNKNOWN / PENDING** | ⭐ **it did not run, or nobody decided yet** |

> ⛔ **UNKNOWN IS NOT PASS.** ⭐ *"This is wrong"* and *"nobody measured this"* are opposite
> problems needing opposite responses — and collapsing them sends someone to fix what only needed
> measuring.

**Severity is the same everywhere too:** 🔴 mandatory · 🟠 expert · 🟢 guidance. ⭐ **A 🔴 is
never lowered locally** — the places where it is inconvenient are the places it was written for.

---

## ⭐ THE ID IS AN ADDRESS

Every criterion carries a permanent `XX-AAA-nnn`. The seven prefixes in use:

```
BE  dev-backend      DB  dev-database     FE  dev-frontend
PL  doc-planning     DS  doc-structure
VF  val-functional   VI  val-integration
```

⛔ **Never renumber.** Something cites `BE-ARC-001` from another file, a commit, or a review —
⭐ **renumbering breaks every citation silently: they still resolve, to the wrong criterion.**
**Deprecate an ID; never reuse it.**

---

## ⬜ ADDING AN EIGHTH

⭐ **`DISCIPLINE.md.template` is the form**, extracted from the seven rather than invented. It
carries the eight checks a new discipline passes before it ships — ⭐ **including the one that is
easiest to skip: at least one citation into another discipline.**

⚠️ **A discipline written in isolation duplicates what its neighbours already decided, and the
duplication is only found once the two copies have diverged.**

> ## ⛔ THE ONE PLACE AN AI MUST NOT FILL THE BLANK
> ⚠️ **An invented criterion reads exactly like a real one** and silently becomes the bar
> everything is measured against. ⭐ **A missing criterion is visible and gets filled; an invented
> one is not.**
>
> ⭐ **The method: the AI asks, the owner answers with real cases, the AI structures.** Never the
> reverse. **Every ⬜ zone ships with its interview questions already written.**

---

## ⚠️ Before you add a file here — five questions

1. **Can it reject something?** ⛔ If not, it is documentation, not a discipline.
2. ⭐ **Which owner does it branch from?** Name it in the header, and match the prefix — the gate
   that injects standards uses this to decide what to hand an editor.
3. **Does one of the seven already own its rules?** ⭐ Then cite them, and say what yours adds.
4. **Does your prefix collide?** ⛔ Two criteria at one address.
5. ⭐ **Does §0 name a failure, not a topic?** A discipline with no failure behind it will not
   survive its first inconvenient verdict.

---

Related: `../README.md` (⭐ **the parent — the three zones, and why criterion ships**) ·
`../owner-1-docs.md` · `../owner-2-dev.md` · `../owner-3-validation.md` (⭐ the three that act on
these judgements) · `../imported-patterns.md` (⚠️ detectors, ⛔ not criterion) ·
`DISCIPLINE.md.template` (to add an eighth).
