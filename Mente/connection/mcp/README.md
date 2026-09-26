# connection/mcp/ — third-party MCP servers, and where their config points

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ **INSTANCE** — the folder and this README travel; ⛔ the servers never do.
**Governance:** `owner` in `pieces.tsv`

## Purpose

Where the code of an MCP server that runs on this machine lives, and the rule for how it is
declared so the agent sees it. ⛔ It never holds a credential.

---

## Two pieces, two places

```
connection/mcp/<name>/      the server's CODE, when it runs locally (stdio)  ← gitignored, restored by sync
../../.mcp.json             the DECLARATION the agent reads (project scope)  ← points here
```

A remote (HTTP) server has no code here — only its declaration and its registry row.

📏 **What Claude Code does with it** (its MCP docs, read 2026-09-26):

| Scope | Stored in | Shared |
|---|---|---|
| local (default) | `~/.claude.json`, under this project | no |
| ⭐ **project** | `.mcp.json` at the project root | yes, through git |
| user | `~/.claude.json` | no — every project |

⭐ **Project scope is the one this folder uses:** the declaration travels with the repo, and a
project server **asks for approval** in an interactive session before its first use — the
install cannot switch itself on.

⚠️ **Not verified:** how Codex declares an MCP server. Nothing here claims it until it is read.

---

## ⛔ The credential rule

A declaration carries `${VAR}`, **never the value**:

```json
{ "mcpServers": { "example": { "type": "http", "url": "https://example.com/mcp",
    "headers": { "Authorization": "Bearer ${EXAMPLE_TOKEN}" } } } }
```

Where the value lives is `../../secrets/` — this folder says **which** server, never **how** to
reach it. Claude Code also reads `ANTHROPIC_API_KEY` and similar as **empty** inside a remote
`url`/`headers`, on purpose.

⚠️ **An MCP server that fetches outside content can inject instructions.** Same review as a
skill before it is exposed (`../skills/README.md` — the install path).

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| a local MCP server's code, pinned to a sha | its token, key or password — `secrets/` |
| | a server declared in `.mcp.json` with no registry row — an orphan |

---

Related: `../README.md` (the parent) · `../registry.tsv` (`type: mcp`, `exposes: .mcp.json:<name>`)
· `../skills/README.md` (the install path, shared) · `../../secrets/README.md`.
