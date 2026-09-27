# connection/cli/ — the CLIs this machine already has, and how the agent may use them

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ **INSTANCE** — the folder and this README travel; ⛔ the cards never do.
**Governance:** `owner` in `pieces.tsv`

## Purpose

Declare every command-line tool **already installed on this machine** that the agent works with —
`gh`, `vercel`, `docker`, `supabase`… — what it is for, with which account, and where its
credential lives. ⭐ A CLI the agent reaches for without a card is a CLI nobody decided it may use.

---

## `cli/` or `tools/`?

| | `cli/` | `../tools/` |
|---|---|---|
| What it is | a CLI the machine **already has** | somebody's repo, **fetched** into this installation |
| What lives in the folder | ⭐ a **card** — words, never code | the code, pinned to a commit |
| How it arrives | the person installed it on the machine | `bin/connection add` · quarantine · review |
| On the `PATH` | yes — that is the point | ⛔ never |

⛔ **A folder inside `cli/` is refused** (`CLI-DIR-001`): code here would be code nobody reviewed.

---

## One card per CLI — `cli/<name>.md`

```markdown
# cli · gh

**Binary:** `gh` · **For:** open and review pull requests on the declared repositories
**Account:** the organisation account · **Credential:** `host`
```

| Field | Required | Means |
|---|---|---|
| **Binary** | ✅ | the command as typed — `bin/check-connection` looks for it on this machine |
| **For** | ✅ | what the agent may use it for · ⭐ the limit is the point: a card that says "anything" says nothing |
| **Account** | — | which account it acts as, by role — never a password |
| **Credential** | ✅ | ⭐ WHERE it lives: `secrets/<file>` · `host` (the CLI's own login, e.g. `gh auth`) · `none` |

⛔ **The credential itself never goes in a card.** A card is versioned; a token in it is published
with the next push. `bin/check-connection` refuses a value that looks like one (`CLI-SEC-002`) and a
Credential that points anywhere but `secrets/`, `host` or `none` (`CLI-SEC-001`).

⚠️ **A card whose CLI is not installed here is 🟡, not 🔴** — the card may come from another
machine. Install the CLI, or delete the card if the agent should no longer use it.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| one card per CLI the agent may use | the CLI's code or binary — it lives where the person installed it |
| where each credential lives | ⛔ **the credential** — that is `../../secrets/` |
| | a repo to fetch — that is `../tools/` |

---

Related: `../README.md` (the parent) · `../tools/README.md` (fetched repos) · `../../secrets/README.md` (where credentials live) · `../../bin/check-connection` (what verifies the cards).
