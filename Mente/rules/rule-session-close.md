# RULE · SESSION CLOSE

**Status:** current · **Type:** rule · **Updated:** {{date}} · **Owner:** {{owner}}
**Applies to:** ⭐ **every session that ends** — a `/clear`, a reset, a context that ran out
**Enforcement:** 🔒 `bin/check-clear-ready` refuses the cut · ⚠️ what to WRITE is 📖
**Level:** 🌐 universal — ⭐ travels identical to every clone; a lower level may ADD or TIGHTEN, never loosen
**Verified by:** `bin/check-clear-ready` · `bin/probes/probe-clear-ready.py`
**Governance:** `engine` in the piece table · ✅ ships identical to every clone

---

## Purpose

⭐ **A conversation ends and the files survive it. The reasoning does not** — why
something was decided, what was tried and rejected, what comes next. This rule
says where that goes, so nobody has to decide it in the moment.

🔴 **THE FAILURE THAT MADE THIS FILE, measured 2026-09-09 on a real install.**
Four files pointed at `rules/rule-session-close.md` and **it did not exist**. So
at the first real session close the assistant did the only thing left: it asked
the owner *"where should I keep the session record?"* — ⛔ a question about the
engine's own filing, put to somebody who had installed it two days earlier.

> ⛔ **THE OWNER'S WORDS:** *"la idea es que Mente OS sepa gobernar sobre su
> sistema, y esto demuestra que no sabe ni en dónde guardar las cosas."*

⭐ **And the answer they gave was wrong through no fault of theirs** — they chose a
Spanish-named folder beside the memory, which `.gitignore` excludes. The record of the session was
written and never saved.

---

## 1 · ⛔ THE RULE THAT DECIDES EVERY OTHER LINE HERE

> ## Where a thing goes is NOT a question. The engine knows, or the engine is not governing.

| ⛔ Never ask | ⭐ Because |
|---|---|
| *"where do I keep the session record?"* | this file answers it |
| *"should the block be versioned?"* | §3 answers it |
| *"is it safe to reset now?"* | `bin/check-clear-ready` answers it |

⚠️ **The one thing that IS asked** is whether to save at all — that is an action
on their repository, and it is theirs. ⛔ Never the filing.

---

## 2 · ⭐ WHERE EACH THING GOES — the whole answer, in one table

| What | Where | Versioned? |
|---|---|---|
| ⭐ **where we left off** | `memory/RESUME.md` | ✅ yes |
| **what was postponed** | `memory/PENDING.md` | ✅ yes |
| ⭐ **what happened in each session** | `memory/sessions/INDEX.md` | ✅ yes |
| the open work | `work/blocks/active/<id>/BLOCK.md` | ✅ yes |
| a deliverable | inside the block's own folder | ✅ yes |
| ⛔ **a credential** | `secrets/` | ⛔ **never** |
| a live number | 🤖 `docs/METRICS.md` | ⬜ generated |

⛔ **`memory/sessions/`, in English, like every other engine path.** ⚠️ An
installation may translate what it writes INSIDE; the path itself ships
identical, or a clone cannot find it.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `SES-LOC-001` | ⭐ **The session record lives at `memory/sessions/INDEX.md`** | 🔒 | ⛔ asked, it is a system that does not know itself |
| `SES-LOC-002` | ⭐ **It is versioned** — `bin/init` writes the exception | 🔒 | ⛔ a record outside git dies with the folder |
| `SES-LOC-003` | **The open work is versioned too** | 🔒 | ⚠️ see §3 |

---

## 3 · ⛔ WHY THE WORK IS VERSIONED, and why that reverses a shipped default

⭐ **`Mente/.gitignore` excludes `work/` and `memory/` on purpose** — the ENGINE
must not ship carrying somebody's blocks or somebody's name.

⛔ **Applied to the owner's OWN repository, the same rule deletes their work on
the first `git clean`.** 🔴 Measured: an installation had a block with two real
deliverables and a session record, and **not one of the three was in git.**
`check-clear-ready` said so and the reading was *"it is a warning about backups"*.

> ⭐ **"Does not travel to the published engine" and "is not saved in your own
> repository" are DIFFERENT questions.** The shipped `.gitignore` answers the
> first one for both, and `bin/init` writes the exception that separates them.

---

## 4 · WHAT A CLOSE WRITES

⭐ **Three files, in this order.** ⛔ The first is the one that never gets
skipped: without it the next session starts by asking.

1. **`memory/RESUME.md`** — the state: where we are, the ONE next step, the
   traps. ⛔ Not history. ⚠️ It is refreshed, never appended to — a brief that
   grows stops being read.
2. **`memory/sessions/INDEX.md`** — the history: a row in the index plus what
   happened, what it cost, and why it closed.
3. **`memory/PENDING.md`** — anything real but not blocking, ⛔ with what it
   costs if nobody ever fixes it.

⚠️ **Measured, never estimated.** Size, turns and peak context come from the
transcript. ⛔ A number nobody measured does not go in the record.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `SES-WRT-001` | ⭐ **RESUME is refreshed at every close** | 📖 | ⛔ a stale brief is worse than none |
| `SES-WRT-002` | **The record carries measured numbers or says ⬜** | 📖 | ⚠️ an estimate presented as a measurement |
| `SES-WRT-003` | ⭐ **RESUME holds no live number** | 🔒 | ⭐ enforced by `DOC-CNT-002` — ⛔ a number copied here is correct exactly once |

---

## 5 · ⛔ THE CUT IS A CUT, NOT A SAVE

`bin/check-clear-ready` refuses while something would be lost. ⭐ It is the
deterministic half; this file is the curated half — deciding what mattered,
which no script can do.

⚠️ **It reports what it could NOT measure too.** ⛔ A green from a check that
skipped half its questions is the failure this whole engine names first.

---

## WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ what a close WRITES into the record | ⭐ the owner of the instance — it is their history |
| the paths in §2 and their IDs | whoever maintains the engine, through a recorded decision |
| ⛔ asking the owner where a thing goes | **nobody** — ⭐ that is the failure this file exists to end |
| ⛔ a credential written into a record | **nobody** — ⚠️ what is written stays in every transcript that read it |

⭐ **The paths are the engine's and the content is the instance's.** ⛔ Confusing
the two is how one installation's session history ends up shipped to every clone.

---

Related: `contract-pending.md` (the shape of a postponed item) · `contract-document.md`
(the shape of what a close writes) · `rule-working-in-a-block.md` (the work a close records)
