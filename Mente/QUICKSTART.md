# QUICKSTART —  from clone to working in 3 steps
**Status:** current · **Type:** entry-point · **Updated:** {{date}} · **Owner:** {{owner}}
**Verified by:** every number in this file was measured by running the steps on a real clone

## Purpose

Take someone who **does not know this project** from a `git clone` to a working Mente OS.
Written for a stranger, not for its author: if anything here only makes sense once you know how
the author works, that is a defect in this file.

> ⭐ **What Mente OS is:** an engine that **governs** how things get built. It does not generate
> code: it enforces that what is built is explained before it is made, verified before it is 
> closed, and that rules hold because a script blocks them — not because someone remembers.
>
> **The law that explains everything:** *a rule in code is followed 100%; one that lives only in
> a document, 40-60%.* That is why doctrine is a document and **verification is a script**.


---

## 1 · What you need first

| | |
|---|---|
| **Python 3** and **bash** | the validators are written in them, with no external dependencies |
| **git** | the system relies on it to know what changed |
| **Claude Code** (optional) | the gates are its hooks. Without it the engine still verifies, but nothing blocks |

⛔ **There is no `npm install` and nothing to compile.** If you have Python and bash, you are ready.

---

## 2 · The 3 steps

### ① Clone

```bash
git clone <repo-url> my-mente
cd my-mente
```

### ② Install — ⚠️ in a REAL terminal

```bash
cd Mente
bin/init
```

It will **ask for your name**. That is deliberate: `ADR-003` says criteria are asked, never
guessed, and who decides in an instance is criteria.

> 🔴 **If you launch it through a pipe or from a script, it refuses:**
> *"`owner name` has no default and there is no terminal to ask on"*.
> It is not a failure — it is the refusal to invent a piece of data only you have.

`bin/init` does three things: it creates your `mente.config.yml`, generates `CLAUDE.md` and
`PROJECT-RULES.md` with your name, and wires the hooks with portable paths.

### ③ Check

```bash
bin/test-f0-f6
```

---

## 3 · What you will see, and why it is NOT an error

Here is what **actually** happens on a clean clone:

| Moment | Result |
|---|---|
| freshly cloned | most checks pass · **several fail** |
| after `bin/init` | all but one pass · **exactly 1 fails** |

> ⭐ **`bin/init` is not optional.** Without it the system does not know who you are, and several
> checks fail closed rather than assume it.

**And the one that remains does not get fixed — it is the correct answer:**

```
🔴 check-clear-ready agrees with the registry (registered=no)
```

It says **your session is not registered yet**, and that is true: you just arrived. The registry
is written before a `/clear` (`rules/rule-session-close.md`), so on a fresh clone that red is the 
system reporting accurately. A check that turned green there would be lying. It clears itself the
moment you register your first session.

**Everything else runs clean on your clone:** `check-blocks` (0 errors · 0 warnings),
`check-links` (every file, zero broken pointers), `check-health`, and **the gates block**.

---

## 4 · Your first block — the full cycle

```bash
bin/new-block my-first-task --type docs   # creates it with its §A-K contract
bin/check-sufficiency my-first-task       # can it be resumed by reading §A-E alone?
bin/grade-block my-first-task             # 🟢 product or 🔴 MVP — MEASURED, not opinion
```

A **block** is a unit of work with a contract: what goes in, what does not, what it  depends on,
under what criteria it is judged, and when it may close. `rules/block-lifecycle.md` explains it
in full.

⛔ **What the system will stop you from doing**, worth knowing before you hit it:

- closing a block with open sub-blocks  → `gate-critical` **blocks it**
- a destructive migration with no rollback → **blocked**
- committing on `master` → **blocked** (branch → verify → PR)
- reading `secrets/` without live permission → **it asks**, and it is logged

---

## 5 · The commands you will use

| You need… | Command |
|---|---|
| is the system healthy? | `bin/check-health` |
| does everything point to something that exists? | `bin/check-links` |
| do the blocks meet their contract? | `bin/check-blocks` |
| ⭐ the full verification | `bin/test-f0-f6` — *the only thing that matters is `failed: 0`* |
| the pre-release review | `bin/verify-all` (`--rapido` skips clone and demo) |
| what can I run and what not? | `Mente/CAPABILITIES.md` |

---

## 6 · If something goes wrong

| Symptom | What is happening |
|---|---|
| `bin/init` refuses to ask | you launched it with no terminal. Run it directly, no pipes |
| more than 1 failure after init | something broke: `bin/check-health` names it with its reason |
| a hook blocks everything | check `.claude/settings.json`: every `PreToolUse` group **must** carry a `matcher`. Without it, a hook runs on every tool |
| `check-links` reports broken ones | they are real: on a clean clone it runs to zero. A broken pointer is a defect, not noise |

---

Related: `CLAUDE.md` (the router Claude Code reads at startup) · `PROJECT-RULES.md` (the
project-level rules) · `Mente/CAPABILITIES.md` (what may run and what is forbidden) ·
`Mente/rules/block-lifecycle.md` (opening and closing a block) · `LICENSE` (AGPL-3.0).