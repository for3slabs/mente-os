# memory/principles/ — the criterion · how the system speaks and how it judges

**Status:** current · **Type:** folder-readme
**Scope:** ⚠️ **ENGINE inside an instance folder** — read the box below before anything else.
**Governance:** `engine` in `piezas.tsv` · ✅ ships whole to every clone

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

👉 **Read `../README.md` first** if you have not: it explains why the parent exists, what a
context reset destroys, and why the other three things in there never travel.

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

## The four owners — one voice, three architects

| File | Owns | Answers |
|---|---|---|
| `owner-0-voice.md` | ⭐ **how the system communicates** | tone, structure, what is never said |
| `owner-1-docs.md` | the **form** of documents and plans | is this readable, findable, trustworthy? |
| `owner-2-dev.md` | the **form** of what is built | is this built or patched? |
| `owner-3-validation.md` | the **verdict** — is it done? | product or MVP, measured |

⭐ **The three architects are peers. There is no hierarchy between them.** The numbering is an
order for reading, not a chain of command: validation does not outrank development because it
comes last. Each rejects within its own domain, and a piece must satisfy all three.

⚠️ **`owner-0` sits apart.** The voice is not a fourth domain — it governs **how every one of the
other three is expressed**. A correct verdict delivered badly is a verdict that does not land.

---

## `expertise/` — where each architect's criterion actually lives

The four files above declare **what** each owner governs. The detail — the concrete criterion an
expert applies — lives one level down, split by discipline:

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
it belongs to. Without that line the file is an orphan: readable, but with no way to know which
architect rejects on its basis, or when it is supposed to be read.

**The prefix is the parent.** `doc-` belongs to owner-1, `dev-` to owner-2, `val-` to owner-3.
⛔ A file whose prefix does not match its declared parent is a defect — the hook that injects
standards uses this to decide what to hand the editor.

---

## ⭐ HOW CRITERION IS WRITTEN — the method, and it is not optional

> ## The AI asks. The person answers with real cases. The AI structures.
> **Never the reverse.**

A criterion file drafted by an AI first comes out as *"use best practices"*, *"keep it
maintainable"* — which is as empty as *"it's fine"*. It reads like criterion and decides nothing.

⛔ **This is the one place in the whole engine where the AI must not fill the blank.** Everywhere
else, a sensible default beats an empty field. Here, an invented criterion is worse than a missing
one: a missing criterion is visible and gets filled, while an invented one silently becomes the
standard everyone is measured against.

Each file therefore ships **with its interview questions already written** and its answers empty.
The empty state is honest; it says *this judgment has not been made yet*.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| how to judge whether something is well done | a checkable rule — that is `rules/` |
| the voice: how the system communicates | a decision already taken — that is an ADR |
| an expert discipline, branching from an owner | ⛔ a criterion invented by an AI |
| the interview questions that elicit criterion | anything specific to one project |

⚠️ **The line against the parent folder:** `memory/` records **what happened**; this records
**how to judge what happens**. History belongs upstairs; standards belong here.

---

## ⚠️ Before you add a file here — the four questions

1. **Is it judgment or a check?** A script can verify a check. If a script could verify it, it is
   a rule and belongs in `rules/`.
2. **Which owner does it branch from?** Name it in the file, and match the prefix. An expertise
   file with no declared parent never gets injected, and nobody notices it is missing.
3. **Did a person state it, from real cases?** ⭐ If it came from an AI's idea of good practice,
   delete it. It will read fine and decide nothing.
4. **Would it hold in a different project?** No → it is that project's preference, not engine
   criterion, and it belongs in that project's own rules.

---

Related: `../README.md` (⭐ **the parent — read it for context**) · `../../rules/README.md` (what
must happen, as opposed to how to judge it) · `../../hooks/README.md` (what injects these before
an edit) · `../../CAPABILITIES.md` · `../../piezas.tsv` (where each owner is declared).
