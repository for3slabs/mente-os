# Mente OS v2

**Status:** current · **Type:** entry-point · **Updated:** {{date}} · **Owner:** {{owner}}
**Licencia:** AGPL-3.0 — ver `LICENSE` en la raíz del repositorio

## Purpose

Start here if you just cloned this. Five minutes to a working system.

---

A work system for building with an AI without losing the thread. It does not document what you
did — it **governs how it gets done**: three gates that block, ten validators that measure, and
a quality verdict that answers *is this a product or an MVP?*

> **The law it is built on, measured:** a rule enforced by code complies 100%; a rule that lives
> only in a document complies 40-60%. **So the doctrine is a document and the verification is a
> script.**

---

## 1 · Requirements

| | |
|---|---|
| **Python 3.8+** | standard library only — **no pip install, ever** |
| **bash** | POSIX; every validator is bash or python |
| **git** | for the commit gate |

That is the whole list. A dependency you have to install is a system that does not run on clone.

---

## 2 · Install

```bash
git clone <this-repo> Mente
cd Mente
$EDITOR mente.config.yml    # 1 · put your name in `owner.name` — it is asked, never guessed
bin/init                    # 2 · ⭐ FIRST. Generates CLAUDE.md + PROJECT-RULES.md + WORKSPACE.md
bin/check-health            # 3 · tells you what is missing, in plain language
```

> ## ⭐ `bin/init` IS STEP ONE, not an optional extra
>
> **A fresh clone has no `CLAUDE.md` and no `PROJECT-RULES.md`** — those describe *an instance*,
> so they are **generated**, never inherited. Until you run `bin/init`, the AI starts with no
> instructions at all.
>
> 🔴 **Why they are not shipped — measured, not assumed:** when they travelled inside the repo, a
> clone owned by someone else arrived carrying the **previous owner's name throughout** its project
> rules and **not once** the real one — and `init` could not fix it, because it correctly refuses
> to overwrite files that already exist. The engine was handing a stranger another person's rules.
> ⭐ Same diagnosis and same cure as `docs/WORKSPACE.md`, which describes one machine.

`check-health` is the first thing that talks to you after `init`. If it says nothing, nothing is
wrong.

> ⚠️ **A consequence you will hit:** because these files are not tracked, **checking out a branch
> created before they became generated deletes them from disk**, and the battery turns red — every
> failure pointing at the missing project rules. **The cure is `bin/init`**, and it takes a second.
> It is not a defect: it is what "generated, not inherited" costs, and knowing it beats
> rediscovering it as an incident.

---

## 3 · Make it yours — one file

Everything specific to **you** lives in `mente.config.yml`. Everything else is the engine and
you never edit it.

```yaml
owner:
  name: "Your Name"

gates:                       # trees the AI must not read without permission
  - path: "~/another-project"
    why: "different project · opening it needs explicit approval"

siblings:                    # repos beside Mente/ whose uncommitted state matters
  - "my-app"
```

Then re-run `bin/check-health`. That is the whole setup.

> ⭐ **Why a config file and not code:** four validators used to hardcode one machine's paths,
> and each failed **silently** elsewhere — the session watch simply went quiet. A guard aimed at
> a path that does not exist is not a guard; it is a green light.
>
> **If you ever have to edit `bin/` to make this work, that is a bug. Report it.**

---

## 4 · The first thing to understand: the BLOCK

A **block** is one unit of work. One file, `BLOCK.md`, with sections A-K.

```bash
bin/new-block my-feature --type code
```

Its first five sections (§A-E) must answer seven questions **on their own**:

what is being built · what must NOT be touched · what it depends on · under which standards ·
what phase · what the next step is · what is blocking it

```bash
bin/check-sufficiency my-feature     # can this restart from disk alone?
```

> **If §A-E do not answer those seven, the block does not close** — even if the code works.
> The next session would rebuild your scope by inference and sound just as confident doing it.

---

## 5 · What runs on its own

You do not invoke these. They fire at the moment they matter.

| When | What happens |
|---|---|
| Session starts | health check — **silent unless something is red** |
| Before an edit | the owning block's required standards are named back to you |
| Before an edit | 🔴 **blocks** destructive SQL with no rollback · closing an insufficient block |
| Before a subagent | 🔴 **blocks** a specialist that can write and has no declared scope |
| Before a commit | 🔴 **blocks** a block that violates its contract |

**Only three actions block. Everything else informs.** That ratio is deliberate: a gate that
obstructs more than it protects gets switched off, and a switched-off gate protects nothing.

Every gate prints how to bypass it. **A gate with no escape hatch gets deleted.**

To wire the hooks into Claude Code, copy the `hooks` block from
`.claude/settings.json` in the parent repo — the four entries under `PreToolUse` and
`SessionStart`.

---

## 6 · The commands you will actually use

```bash
bin/check-health             # is anything wrong                    ← start here
bin/new-block <name> --type <code|docs|data>
bin/check-sufficiency <b>    # can it restart from disk alone
bin/grade-block <b>          # product or MVP — measured, not opinion
bin/check-clear-ready        # safe to reset context?
bin/test-f0-f6               # the whole system, end to end
bin/generate-index           # 🤖 rebuild the indexes
bin/generate-metrics         # 🤖 republish the live numbers
```

`bin/test-f0-f6` is the truth. It takes a lock, so **one run at a time** — a second is refused
on purpose, because both would corrupt each other's probe blocks.

> ⚠️ **Never write a count into a document.** Live numbers live in `docs/METRICS.md`, regenerated.
> A number copied into prose is correct exactly once — this project froze the same one twice in
> a single day before the rule existed.

---

## 7 · The one thing only you can write

The quality verdict has two layers. Layer 1 (`bin/grade-block`) is measurable and works out of
the box: dead code, duplication, tests, the import graph.

**Layer 2 is your criterion**, and no AI can write it:

| File | What goes in it |
|---|---|
| `rules/qa-dimensions.md` | the six dimensions, and what each demands |
| `principles/expertise/dev-*.md` | database · backend · frontend |
| `principles/expertise/doc-*.md` | planning · structure |
| `principles/expertise/val-*.md` | functional · integration |

Each ships with the interview questions already written. **The method is: the AI asks, you
answer with real cases, the AI structures.** Never the reverse — a draft written first comes out
as *"use best practices"*, which is as empty as *"it's fine"*.

Open holes: `docs/PENDING-{{owner}}.md` (count in `docs/METRICS.md` · `criterion.holes`).

---

## 8 · Where things live

| Folder | What |
|---|---|
| `bin/` | the validators — executables |
| `hooks/` | the gates that fire automatically |
| `rules/` | contracts · rules · ADRs |
| `principles/` | the three owners and their disciplines |
| `blocks/` | the work — `active/` `archive/` |
| `docs/` | architecture · 🤖 generated indexes |
| `memory/` | `RETOMAR.md` (read first when resuming) · pending · logbook |
| `secrets/` | ⚠️ never in git |

---

## 9 · Resuming after a context reset

Read **`memory/RETOMAR.md`**. It is the only file guaranteed to be read, capped at 200 lines on
purpose, and it should be enough to start working without asking anything.

Closing a session is the other half: run the `session-wrap` skill, or follow
`rules/rule-session-close.md`. **`/clear` is a cut, not a save** — whatever is not on disk is
lost with no warning. `bin/check-clear-ready` refuses while something would be lost.

---

Related: `docs/architecture/how-it-runs.md` (what fires when, with diagrams) ·
`rules/contract-block.md` · `principles/owner-*.md` · `docs/METRICS.md`.
