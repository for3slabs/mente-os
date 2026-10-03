# connection/skills/ — third-party skills, installed the same way every time

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ **INSTANCE** — the folder and this README travel; ⛔ the skills never do.
**Governance:** `owner` in `pieces.tsv`

## Purpose

Where every skill that comes from outside lives — from a repo, from a catalog, or written by us
for a repo that shipped none. The agent uses it like any other; this folder is only where it
lives and how it is verified.

---

## What this folder is

```
connection/skills/<name>/     ← the REAL folder: SKILL.md + scripts/ references/ assets/
        ▲
        └── ../../.claude/skills/<name>    a symlink — what Claude Code reads
        └── ../../.agents/skills/<name>    a symlink — what Codex reads
```

⭐ **The agent never knows the difference.** Claude Code and Codex both follow a symlinked skill
folder (their docs, read 2026-09-26). 📏 **Measured here the same day**, not assumed: a fresh
session listed a skill whose `.claude/skills/` entry was a link into this folder, and invoking it
loaded the body through the link.

⚠️ **Two consequences of the measurement:**

| Found | What it means |
|---|---|
| a skill added mid-session is not seen until a **new session** (or `/reload-skills`) | an install is not usable the moment it lands — the installer says so, it does not imply otherwise |
| `${CLAUDE_SKILL_DIR}` resolves to the **link** path | scripts still run; the checker validates the link's TARGET, never the link |

---

## The standard every skill here meets

The open Agent Skills spec (`agentskills.io/specification`), which both vendors read:

| Field | Rule |
|---|---|
| `SKILL.md` | the opening `---` is **line 1** — no blank line, no BOM |
| `name` | 1-64 chars, `a-z 0-9 -`, no leading/trailing/double hyphen, **equal to the folder name** |
| `description` | 1-1024 chars — what it does **and when to use it**; it is all the agent sees before loading |
| body | under 500 lines; detail goes to `references/`, one level deep |

⛔ **A name that differs from its folder does not load** — silently. That is why it is checked.

---

## ⭐ The install path — the only one

```
fetch ─► quarantine ─► REVIEW ─► expose ─► registry row ─► new session
pinned    not linked    a person    links      ../registry.tsv
to a sha  not usable    reads it
```

1. **Fetch** into `<name>/` pinned to a full commit sha — never a branch that can move under you.
   ⭐ **Only that commit** (`--depth 1`), and **never the third party's agent files** (CLAUDE.md,
   AGENTS.md, CLAUDE.local.md, GEMINI.md) — a sparse-checkout keeps them off the disk (EXT-56,
   2026-10-03). 📏 A full clone kept 380 of impeccable's 456 MB as history, and its `CLAUDE.md`
   was loaded as project instructions the moment a file beside it was read. A clone made before
   this: `bin/connection slim` shrinks it in place, keeping what was built inside it
   (measured on the instance that found it: `connection/tools/` 1.4 GB → 520 MB).
2. **Quarantine:** the folder exists, nothing links to it, `state: quarantine`.
3. ⛔ **Review before exposing.** A third-party skill is text the agent will obey and scripts it
   may run: it is a prompt-injection surface. Read `SKILL.md` and every script. Nothing is
   activated without a person's yes (`feedback_nada_se_activa_sin_permiso`).
4. **Expose:** the links in `.claude/skills/` and `.agents/skills/`, `state: active`.

### "Turn this GitHub repo into a skill"

| The repo has… | Goes to |
|---|---|
| a `SKILL.md` at its root, or `skills/*/SKILL.md` | here — one folder per skill it ships |
| no skill, it is a CLI or a library | the code to `../tools/<name>/`; **we write** a `SKILL.md` in `<name>/` that says how to drive it, `source: authored:tools/<name>` |

⭐ **What a third party wrote is never versioned — `sync` restores it; what we wrote is versioned
with `git add -f`** (`author` does it). An authored skill is our work — losing it on a fresh clone
would lose the only copy, so `check-connection` goes red if it is not tracked.

---

## ⭐ On demand — a skill is ON only while its block is the work

📏 Every linked skill puts its `description` in **every turn** (one design skill's is ~1,000
chars), and a broad one invites the agent to use it on work that never asked for it. So a skill
can be **on demand**: reviewed and on disk, but linked only while the block being worked on
declares it. ⛔ CLI, bridges, MCP and server are the exception: they are reached in very specific
cases and stay as they are.

```
activate <s> --on-demand --domain design   reviewed, on disk, NOT linked
attach <s> --block <b>                      `- SKILLS: \`s\`` in the block's §C  (a campaign: `skills:`)
focus <b>                                   link what <b> + its campaign declare · unlink the rest
```

| Piece | What it does |
|---|---|
| `hooks/focus-signal.py` (UserPromptSubmit) | the block a request NAMES becomes the focus — *"let's work on the admin panel"* → `admin-panel`. A tie moves nothing and says so. Silent when nothing moves |
| `hooks/pre-edit-standards.py` | editing a file of a domain (`.tsx` `.css`… = `design`) in a focus with no skill of it → 💡 *ask the owner once* whether to attach the on-demand one |
| `check-connection` CON-FOC-001..004 | 🔴 an on-demand skill linked outside its block · a block declaring a skill nobody installed · on-demand on a non-skill · a focus on a block that does not exist |

⚠️ A switch is seen from the **next session or after `/reload-skills`** — the hook says so every
time it changes what is linked. The focus lives in the focus file under `cache/` (this machine, never git).
⚠️ `focus-signal` fires only once its `UserPromptSubmit` entry from
`templates/claude-settings.json.template` is merged into your settings.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| skills from outside, and skills we wrote to drive something from outside | the engine's own skills — those are born from `templates/skills/` |
| | a skill with no registry row — `check-connection` reports it as an orphan |

---

Related: `../README.md` (the parent — why outward things live apart) · `../registry.tsv` (the
lockfile) · `../tools/README.md` (a repo that is not a skill) · `../../templates/skills/` (the
engine's own skills).
