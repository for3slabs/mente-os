# memory/principles/ — the criterion · how the system speaks and how it judges

**Status:** current · **Type:** folder-readme
**Scope:** ⚠️ **ENGINE inside an instance folder** — read the box below before anything else.
**Governance:** declared as `engine` in the piece table · ✅ ships whole to every clone

---

## 📍 WHERE YOU ARE — read the parent first

```
Mente/
└── memory/          ← ⛔ INSTANCE · what must not be forgotten · content never travels
    └── principles/  ← ⭐ YOU ARE HERE · ENGINE · doctrine · ships identical to everyone
```

⚠️ **This folder inverts its parent's rule, and that is deliberate.** `memory/` holds what belongs
to one installation; **this subfolder holds what belongs to every installation.** Reading it
without that context leads to the exact wrong conclusion — that criterion is something each user
writes from scratch.

⭐ **It lives under `memory/` because criterion IS what must not be forgotten.** It is governed by
the engine because criterion that changes per installation is not criterion — it is preference.

👉 **Read `../README.md` first** if you have not.

---

## What this folder is

The **judgment** of the system. `rules/` says what must happen; this says **with what criterion to
decide whether it was done well**.

| Question | Answered by |
|---|---|
| *"must a block declare its scope?"* | a rule — binary, a script can check it |
| *"is this scope well written?"* | ⭐ **criterion — it needs judgment** |

⛔ **That is the line against `rules/`.** A rule is checkable. Criterion is not: no script decides
whether documentation is good. Putting criterion in `rules/` produces rules nothing can enforce;
putting rules here produces criterion nobody applies.

---

## ⭐ THE THREE ZONES — every file here is a mix, and the mix is declared

This is the distinction that makes the folder shippable at all. **Confusing them is how one
person's taste travels to everybody as if it were law.**

| Zone | What it is | Travels? |
|---|---|---|
| **DOCTRINE** | what holds in any installation | ✅ identical · nobody edits it |
| 🟡 **CALIBRATION** | ⭐ the engine states the **axis**; the owner marks the **point** | ✅ the axis · ⬜ the point |
| ⬜ **THE OWNER'S** | criterion drawn from this installation's own cases | ⬜ ships **empty**, with its questions |

⭐ **The middle zone is the one most systems lack.** Some decisions are neither universal nor
arbitrary: register, visual density, language. Both extremes fail, and the engine can say *what is
being decided and why it matters* without deciding it. ⛔ Shipping them as doctrine imposes one
person's taste; shipping them empty leaves the reader with no idea what they are choosing between.

---

## The files

| File | Governs | Zones |
|---|---|---|
| ⭐ `owner-0-voice.md` | **how the system communicates** — transversal | doctrine + 🟡 + ⬜ |
| `contract-delivery.md` | ⭐ **what a response must contain**, and its shape | doctrine + ⬜ |
| `owner-1-docs.md` | the **form and integrity** of documents and plans | doctrine + ⬜ |
| `owner-2-dev.md` | the **construction** — and whether it may start at all | doctrine + ⬜ |
| `owner-3-validation.md` | ⭐ the **closure authority** — may a block close? | doctrine + ⬜ |
| `imported-patterns.md` | ⚠️ absorbed failure patterns — ⛔ **not the owner's criterion** | doctrine + ⬜ |
| ⭐ `expertise/` | the disciplines each owner branches into — **7 ship written** | doctrine + ⬜ |

### The four owners

⭐ **The three architects are peers. There is no hierarchy between them.** The numbering is a
reading order, not a chain of command: validation does not outrank development because it comes
last. Each rejects within its own domain, and a piece must satisfy all three.

⚠️ **`owner-0` sits apart.** The voice is not a fourth domain — it governs **how every one of the
other three is expressed.** A correct verdict delivered badly is a verdict that does not land.

⭐ **The voice is split in two on purpose:** `owner-0-voice.md` governs how a sentence is written;
`contract-delivery.md` governs what a response must contain. ⛔ Merging them produces a document so
dense that the rules about density stop being followed inside it.

---

## ⭐ WHAT EVERY OWNER FILE NOW DECLARES

These four came out of building them, and they are what a new owner file must have too:

**① WHEN it acts — the trigger.** ⛔ A criterion with no trigger is applied whenever somebody
remembers. Each owner lists the events at which it evaluates.

**② WHAT VERDICT it emits.** Not *"looks fine"* — one of a shared, named set:

| | Means |
|---|---|
| ✅ **PASS** | there is evidence it holds |
| 🔴 **FAIL / REJECT** | ⛔ a contract is violated |
| ⚠️ **WARN** | an anomaly that breaks no contract |
| ⬜ **PENDING / UNKNOWN** | ⭐ **not wrong — unknown** |

> ⛔ **UNKNOWN IS NOT PASS, and PENDING IS NOT REJECT.** Without the fourth state, everything
> unmeasured silently becomes a pass, and every missing criterion becomes a violation. ⭐ *"This is
> wrong"* and *"nobody has decided yet"* are opposite problems and need opposite responses.

**③ WHO VERIFIES each criterion — or that nothing does.** ⚠️ A criterion no script checks is
followed about half the time. **Knowing which half is which is the point of saying so.**

**④ WHO GOVERNS the file itself.** ⭐ An owner that writes its own acceptance criteria is a
circular authority: *"acceptable"* converges on *"whatever it already does"*. ⛔ **No owner file
may lower its own bar.**

---

## `expertise/` — where each architect's criterion actually lives

The owner files declare **what** each one governs. The detail — the concrete criterion an expert
applies — lives one level down, split by discipline.

```
principles/
├── owner-1-docs.md  ──────┐
├── owner-2-dev.md   ────┐ │
├── owner-3-validation ─┐│ │
└── expertise/          ││ │
    ├── doc-*.md    ◄───┼┼─┘   branches of owner-1
    ├── dev-*.md    ◄───┼┘     branches of owner-2
    └── val-*.md    ◄───┘      branches of owner-3
```

⭐ **Every expertise file declares its parent explicitly** — a `Branch of:` line naming the owner
it belongs to. Without it the file is an orphan: readable, but with no way to know which architect
rejects on its basis, or when it is meant to be read.

**The prefix is the parent.** ⛔ A file whose prefix does not match its declared parent is a
defect — the gate that injects standards uses this to decide what to hand the editor.

⭐ **Seven disciplines ship written, and they are doctrine** — `dev-backend` · `dev-database` ·
`dev-frontend` · `doc-planning` · `doc-structure` · `val-functional` · `val-integration`. Their §2
is the engine's base standard; ⬜ **§3 of each is where the installation adds its own criteria.**

⬜ **An eighth is the owner's declaration.** A project with a second storage layer, or an
infrastructure concern, adds one — ⭐ using `expertise/DISCIPLINE.md.template`, which carries the
eight checks it must pass. ⛔ **The seven are not deleted when they do not apply**: what is not
relevant today may be next quarter, and a discipline nobody reads costs nothing.

⭐ **Load only what the change touches.** Reading every discipline for a change that touches one
spends the scarce resource — and lets one discipline's criterion bleed into a decision belonging
to another.

---

## ⭐ HOW CRITERION IS WRITTEN — the method, and it is not optional

> ## The AI asks. The person answers with real cases. The AI structures.
> **Never the reverse.**

A criterion file drafted by an AI first comes out as *"use best practices"*, *"keep it
maintainable"* — which is as empty as *"it's fine"*. It reads like criterion and decides nothing.

⛔ **This is the one place in the whole engine where the AI must not fill the blank.** Everywhere
else, a sensible default beats an empty field. Here, an invented criterion is worse than a missing
one: ⭐ **a missing criterion is visible and gets filled; an invented one silently becomes the
standard everyone is measured against.**

Each ⬜ zone therefore ships **with its interview questions already written** and its answers
empty. **What does not travel is the criterion; what does travel is the question that produces it.**

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| how to judge whether something is well done | a checkable rule — that is `rules/` |
| the voice, and what a delivery must contain | a decision already taken — that is a decision record |
| an expert discipline, branching from an owner | ⛔ a criterion invented by an AI |
| absorbed patterns, ⚠️ **labelled as absorbed** | anything specific to one project |
| the interview questions that elicit criterion | this installation's history — that is upstairs |

⚠️ **The line against the parent folder:** `memory/` records **what happened**; this records **how
to judge what happens**. History belongs upstairs; standards belong here.

⚠️ **The line against `imported-patterns.md`:** knowledge absorbed from outside is **not** the
owner's judgment, and it says so on every page. ⛔ **Moving a pattern from there into a discipline
file would relabel someone else's opinion as the owner's** — the exact failure the separation
exists to prevent.

---

## ⚠️ Before you add a file here — the five questions

1. **Is it judgment or a check?** If a script could verify it, it is a rule and belongs in `rules/`.
2. **Which zone is each part in?** Doctrine, calibration, or the owner's. ⭐ A file that does not
   say cannot be shipped safely.
3. **Which owner does it branch from?** Name it in the file, and match the prefix. An expertise
   file with no declared parent never gets injected, and nobody notices it is missing.
4. **Did a person state it, from real cases?** ⭐ If it came from an AI's idea of good practice,
   delete it. It will read fine and decide nothing.
5. **Would it hold in a different project?** No → it is that project's preference, not engine
   criterion.

---

## ⬜ WHAT THIS FOLDER STILL OWES

⭐ The owner files were written to declare their triggers, verdicts and verifiers. **Nothing yet
acts on those declarations** — the gaps, with what would close each, are in
`../../docs/ENGINE-BACKLOG.md`.

---

Related: `../README.md` (⭐ **the parent — read it for context**) · `../../rules/README.md` (what
must happen, as opposed to how to judge it) · `../../hooks/README.md` (what injects these before
an edit) · `../../docs/ENGINE-BACKLOG.md` (what this folder still owes) · `../../piezas.tsv`.
