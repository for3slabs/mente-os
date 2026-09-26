# connection/tools/ — third-party CLIs and repos that are not skills

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ **INSTANCE** — the folder and this README travel; ⛔ the tools never do.
**Governance:** `owner` in `pieces.tsv`

## Purpose

Where a third-party repo or CLI lives that the agent uses but that is not a skill. Contained
here, outside the rest of Mente OS, so installing or removing it touches nothing else.

---

## What this folder is

```
connection/tools/<name>/    the third party's repo, pinned to a sha   ← gitignored, restored by sync
connection/skills/<name>/   the SKILL.md WE wrote to drive it         ← versioned (source: authored)
```

⭐ **A tool is reached through a skill.** A CLI sitting in a folder is invisible to the agent: it
does not know it exists, when to use it, or how. The authored skill is what turns it into
something the agent reaches for — so "install this repo" almost always means **both** rows.

⛔ **A tool is never put on the global `PATH`** or installed system-wide from here. It runs from
its folder, so removing it is removing one folder and one row — nothing left behind.

---

## The install path

Same as a skill (`../skills/README.md`): **pin → quarantine → review → expose → row.** A tool
with an install step (`npm install`, `pip install -e`, a build) runs it **inside its folder**,
and the step is written in the authored skill, so `sync` can redo it on a fresh clone.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| a CLI or library repo, pinned | a repo that already ships a `SKILL.md` — that is `../skills/` |
| | a local MCP server — that is `../mcp/` |
| | our own scripts — those are `../../bin/` |

---

Related: `../README.md` (the parent) · `../skills/README.md` (the install path and the authored
skill) · `../registry.tsv` (`type: tool`).
