# Mente OS

**Status:** current · **Type:** entry-point · **Updated:** {{date}} · **Owner:** {{owner}}
**License:** AGPL-3.0 — see `LICENSE` at the repository root

## Purpose

Start here if you just cloned this. Five minutes to a working system.

---

A work system for building with an AI without losing the thread. It does not document what you
did — it **governs how it gets done**: gates that block, validators that measure, and a quality
verdict that answers *is this a product or an MVP?* ⭐ The counts live in the generated metrics
file, never in prose — a number written here is correct exactly once.

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
> ⭐ Same diagnosis and same cure as ⬜ `docs/WORKSPACE.md` (created at install), which describes one machine.

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

### And when several blocks serve one mission: the CAMPAIGN

A **campaign** is the figure above a block. Same shape — one file, lettered sections — one level up.

> ## ⛔ A campaign does not execute. It ORDERS.
> No work happens inside one. It holds the mission, the order of attack, and the context its
> blocks share. **The work always happens in the blocks.**

⭐ **The problem it solves:** without it, several blocks serving one mission each carry their own
copy of the background — why the work exists, what was already measured, what was decided across
all of them. Two things then go wrong: the copies **drift** until they disagree and none is marked
wrong, and **switching blocks resets the why** — an agent picking up the fourth block knows what
that block does and nothing about what the whole thing is for.

A campaign writes that background **once**. Its blocks point at it instead of repeating it — the
same rule that governs live numbers, applied to context: *name the source, never copy the value.*

⭐ **The link is declared from both sides:** the campaign lists its blocks, and each block names
its campaign. ⛔ A link declared from one side only is a link that silently never loads.

⚠️ **You do not start with a campaign.** Open a block. A campaign appears when a *second* block
turns out to serve the same mission and would otherwise repeat its whole context. Creating one
first is building structure for work nobody has started.

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
| Reading `secrets/` | ⚠️ **asks** — and writing there asks every time |

**Only three actions block. Everything else informs.** That ratio is deliberate: a gate that
obstructs more than it protects gets switched off, and a switched-off gate protects nothing.

Every gate prints how to bypass it. **A gate with no escape hatch gets deleted.**

**To wire the gates into Claude Code**, merge the `hooks` block from `.claude/settings.json` into
your own. ⭐ **Merge — never replace.** Settings combine across levels, but two files at the same
level do not: the one that wins silently drops the other's rules, and you would lose whatever you
had configured. ⛔ Every `PreToolUse` group needs its `matcher`; without one the hook fires on
every tool call, and a narrow gate becomes a system-wide stop.

---

## 6 · The commands you will actually use

```bash
bin/check-health             # are the hooks wired · is this session still safe  ← start here
bin/probes/run-all.py        # ⭐ the whole system · the only thing that matters is failed: 0
bin/check-block              # do the blocks meet their contract — it walks them all
bin/check-campaign           # do the campaigns, and do their blocks declare them back
bin/grade-block <block>      # product or MVP — measured, never opinion
bin/check-structure          # does every declared piece still have its file
bin/check-declared           # does every engine file have its row
bin/secrets-lease status     # is the secrets permission open, and what did it record
```

⬜ **Planned, not built:** `bin/check-clear-ready` ·
`bin/generate-index` · ⬜ `bin/generate-metrics`. ⛔ They are named in `CAPABILITIES.md` with the
same marker — ⚠️ **a command list that mixes what runs with what is planned sends the reader to
a shell prompt to find out which is which.**

`bin/probes/run-all.py` is the truth. It takes a lock, so **one run at a time** — a second is
refused on purpose, because both would corrupt each other's probe fixtures.

> ⚠️ **Never write a count into a document.** Live numbers live in ⬜ `docs/METRICS.md`, regenerated.
> A number copied into prose is correct exactly once — this project froze the same one twice in
> a single day before the rule existed.

---

## 7 · The one thing only you can write

The quality verdict has two layers. Layer 1 (⬜ a block grader) is measurable and works out of
the box: dead code, duplication, tests, the import graph.

**Layer 2 is your criterion**, and no AI can write it:

| File | What goes in it |
|---|---|
| ⬜ `rules/qa-dimensions.md` | the quality dimensions, and what each demands |
| `memory/principles/expertise/dev-*.md` | database · backend · frontend |
| `memory/principles/expertise/doc-*.md` | planning · structure |
| `memory/principles/expertise/val-*.md` | functional · integration |

Each ships with the interview questions already written. **The method is: the AI asks, you
answer with real cases, the AI structures.** Never the reverse — a draft written first comes out
as *"use best practices"*, which is as empty as *"it's fine"*.

Open holes: `docs/PENDING-{{owner}}.md` (count in ⬜ `docs/METRICS.md` · `criterion.holes`).

---

## 8 · Where things live

| Folder | What |
|---|---|
| `bin/` | the validators — executables |
| `hooks/` | the gates that fire automatically |
| `rules/` | contracts · rules · ADRs |
| `memory/principles/` | the voice and the three architects — their criterion |
| `work/blocks/` | 📦 the work — `active/` `blocked/` `archive/` · one unit each |
| `work/campaigns/` | 🎯 the mission above several blocks — it orders, it never executes |
| `docs/` | architecture · 🤖 generated indexes |
| `memory/` | where you left off · pending items · the logbook |
| `Cerebro/` | your project's own thinking — the pillar and the vision |
| `connection/` | the gate to other installations |
| `secrets/` | ⚠️ never in git |

⭐ **Every folder carries its own README** explaining what goes in it, what does not, and why.
Read that one before adding a file — it is the shortest path to getting the placement right.

---

## 9 · Resuming after a context reset

Read **⬜ `memory/RETOMAR.md`**. It is the only file guaranteed to be read, and its ceiling is
declared on purpose — ⭐ **it should be enough to start working without asking anything.**

Closing a session is the other half: run the `session-wrap` skill, or follow
⬜ `rules/rule-session-close.md`. **`/clear` is a cut, not a save** — whatever is not on disk is
lost with no warning. ⬜ `bin/check-clear-ready` refuses while something would be lost.

---

Related: `CAPABILITIES.md` (what may run and what must not be touched) · `QUICKSTART.md`
(from clone to working) · `rules/README.md` (the contracts) · `memory/principles/README.md`
(the criterion) · `piezas.tsv` (where every piece is declared).
