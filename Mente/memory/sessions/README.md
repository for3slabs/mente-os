# Sessions — what happened, and why each one closed

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ INSTANCE folder — ⭐ the README ships, its contents never do

---

## Purpose

⭐ **The history.** `../RESUME.md` holds the STATE — what is true now. This holds
what happened: one row per session, and why it ended.

🔴 **Why the folder ships empty and pre-named, measured 2026-09-09.** A real
install reached its first session close and the assistant asked the owner where
to keep the record — ⛔ a question about the engine's own filing, put to somebody
who had installed it two days earlier. ⚠️ Their answer was reasonable and wrong:
the path they picked was excluded by `.gitignore`, so the record was written and
never saved.

> ⛔ **Where a thing goes is not a question.** The rule is
> `../../rules/rule-session-close.md` §2, and this folder is its answer.

---

## The shape

`INDEX.md` holds an index row plus one section per session:

| Column | ⚠️ Measured, never estimated |
|---|---|
| id · start · end | from the transcript |
| size · turns · peak context | ⛔ a number nobody measured does not go in |
| verdict | 🟢 · 🟡 · 🔴 and why it closed |

⭐ **Sessions die of AGE more often than of size** — measured across three
runaway sessions: 96h, 76h and 11 days, none over 50 MB, all three red.

---

## ⛔ What does NOT go here

| | Where it goes instead |
|---|---|
| the current state | `../RESUME.md` |
| what was postponed | `../PENDING.md` |
| ⛔ a credential | `../../secrets/` — ⚠️ never in a record |
| a live number | 🤖 `../../docs/METRICS.md` |

---

Related: `../../rules/rule-session-close.md` (the rule this folder answers) ·
`../RESUME.md` (the state) · `../PENDING.md` (the debt)
