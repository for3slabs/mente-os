# hooks/ — the gates · what fires on its own, without being asked

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}} · **Scope:** ⚠️ ENGINE — travels identical to every
clone. Nothing here is edited per instance.
**Governance:** `engine` in `piezas.tsv`

---

## What this folder is

Every file here **fires by itself** at a moment the AI agent is about to do something. Nobody
types these. The agent is about to edit a file, launch a subagent, or make a commit — and a hook
runs first, decides, and either lets it through or stops it.

> ⭐ **The rule that makes this folder necessary:** *if you have to ASK for it, it is not
> automated.* A check that only runs when someone remembers to run it protects nothing on the day
> everyone is busy. That is the entire difference between this folder and `bin/`.

---

## ⛔ THE LINE AGAINST `bin/` — read this before adding anything

| | `bin/` | `hooks/` |
|---|---|---|
| How it runs | **you type it** | ⭐ **it fires on its own** |
| When | when you decide | at the exact moment it matters |
| Can it stop you? | no — it reports and exits | ✅ **yes** — three of them block |
| Wiring | none — it is a command | declared in the agent's settings |

✅ **A hook MAY call a validator from `bin/`.** That is the intended direction: the hook decides
*when*, the validator decides *what*.
⛔ **A validator must never install or trigger a hook.** That inverts the dependency, and it means
running a read-only check would silently change how the system behaves afterwards.

---

## The contract every hook obeys

A hook receives the pending action on **stdin** and answers with its **exit code**. That code is
the whole protocol:

| Exit | Meaning | Effect |
|---|---|---|
| `0` | allow | the action proceeds — **print nothing unless something is wrong** |
| `2` | 🔴 **BLOCK** | the action does **not** happen; what the hook printed is shown as the reason |

⚠️ **This is the host agent's convention, not an internal choice.** Getting it wrong does not
produce an error — it produces a gate that quietly allows everything, which looks exactly like a
gate that is working.

⭐ **Consequence worth stating plainly:** a hook that crashes must exit `0`. A broken guard that
blocks every action is worse than the risk it was written for — it makes the tool unusable, and
the first thing anyone does with an unusable guard is turn it off.

---

**Rules 1 and 2 are decided by** `../rules/decisions/ADR-024-the-system-audits-itself-unasked.md`
— ⭐ **they ship ahead of the tool they govern**, because a startup check that blocks or that
talks on every healthy run is removed within a week.

## ⛔ THE FOUR RULES THAT MUST NEVER BREAK

**1 · Never block the session at startup.**
A hook that fires when the session opens must **never** stop the user from working. If it fails,
it fails quietly and the session continues. There is no state so bad that being unable to start
is the better outcome.

**2 · Speak only when something is wrong.**
⭐ **A validator that talks every time is a validator that gets ignored.** Silence is the healthy
output. The moment a hook prints on a normal run, its warnings stop being read — and a warning
nobody reads is not a warning.

**3 · Blocking is earned by measurement, never assumed.**
Before a gate blocks, measure how often the path it guards is actually walked. The rule:
**if a gate obstructs more than it protects, it degrades to a warning.** A system that gets in the
way gets switched off, and a switched-off gate protects nothing.

**Decided by:** `../rules/decisions/ADR-030-the-block-message-is-the-receipt.md` — ⭐ **what a refusal must SAY**: piece, reason, what to assess, and the way out.
**Also decided by:** `../rules/decisions/ADR-012-few-gates-block-the-rest-warn.md` — ⭐ **why the blocking set stays small**, and what happens to the right gates when a wrong one is added.

| Measured situation | Level it earns |
|---|---|
| a mistake with **no undo** (destructive migration, irreversible delete) | 🔴 **block** |
| closing something that cannot be resumed later — the loss is silent | 🔴 **block** |
| a frequently-walked path already covered by another mechanism | ⚠️ **warn** |
| useful information with no decision attached | ⬜ **inform** |

**4 · Every block prints how to bypass it.**
⭐ **A gate with no escape hatch gets deleted.** A limit you cannot step over on a justified
exception stops being a guard: people route around it, and the route around it is invisible. An
explicit, logged bypass is safer than an implicit one nobody can see.

---

## ⭐ THE PROBLEM UNIQUE TO THIS FOLDER: a dead gate is silent

A validator in `bin/` tells you it ran, because you ran it. **A hook that stopped firing looks
exactly like a hook with nothing to block.** Both are silence.

This is the failure mode this folder must design against, and the reason a shared helper exists:
**every gate leaves a dated mark when it fires**, so its silence becomes measurable. If the mark
is old, the gate is dead — not calm.

⚠️ **And the mark must be cheap.** Edits fire dozens of times per session; stamping on every call
would put disk writes on the hot path, which violates rule 3 above — the guard would cost more
than it protects. Write the mark **only when the day changes**: one write per gate per day, and a
no-op read the rest of the time. Same signal (*did this gate fire today?*), a fraction of the cost.

⛔ **The marks are per-machine and never committed.** A committed mark would ship someone else's
date and make a dead gate on your machine look alive.

---

## Naming — the prefix declares when it fires

| Prefix | Fires | Typically |
|---|---|---|
| `session-` | when a session opens | ⬜ informs · ⛔ never blocks (rule 1) |
| `pre-edit-` | before a file is written | ⬜ injects the standards that apply |
| `gate-` | before a risky action | 🔴 **may block** |
| `pre-commit` / `pre-push` | git's own hooks, on the real operation | 🔴 **may block** |
| `watch-` | observes and records; decides nothing | ⬜ informs |
| `_` | ⚠️ **not a hook** — a shared helper other hooks import | — |

⭐ **Why `pre-push` matters more than it looks:** a gate that reads the *text* of a command can be
walked around — an alias, a shell function, a variable, `eval`, `xargs`. A git hook is executed by
git during the real operation, so none of those get past it. **Two layers, and the second is the
one that cannot be evaded.** When a rule truly matters, the text-reading layer is not enough.

---

## ⚠️ Before you add a hook — the five questions

1. **What action must it intercept?** If it is not tied to a specific action, it is a validator
   in `bin/`, not a hook.
2. **Does it block or inform?** Answer with a measurement of how often that path is walked, not
   with how bad the risk sounds.
3. **What does it print when everything is fine?** The answer must be **nothing** (rule 2).
4. **What happens if it crashes?** It must exit `0` and let the action through.
5. **How would you know it stopped firing?** If there is no answer, you are building a gate whose
   death is undetectable.

---

## Wiring — the part that is NOT in this folder

Hooks do not fire because they exist here. The host agent must be told to run them, in its
settings file, matching each hook to the tool it intercepts.

⚠️ **The wiring is instance-level**, so the installer writes it — never a file shipped from
someone else's machine. And it must **add to** the user's existing configuration, never replace
it: they may already have hooks of their own, and overwriting them trades one protection for
another.

🔴 **The failure to know about:** a rule that intercepts *every* tool instead of the intended one
turns a narrow gate into a system-wide stop. Always scope the match; an unscoped hook is how a
working system becomes unusable in one edit.

---

## Where the state goes

Nothing here stores state in this folder. Dated marks and per-machine records go to `cache/` or
to gitignored files at the engine root. Committed state would make a clone inherit another
machine's history.

---

Related: `bin/README.md` (what you invoke on purpose) · `../CAPABILITIES.md` §3 (what runs without
you) · `../rules/` (the contracts the gates enforce) · `../piezas.tsv` (where each hook is
declared) · `../.gitignore` (why the marks never travel).
