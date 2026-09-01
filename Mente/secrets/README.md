# secrets/ — where credentials live · ⛔ never their values, never in git

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ **INSTANCE** — the folder ships empty. Everything you put here stays on your machine.
**Governance:** `owner` in `pieces.tsv` · **Permissions:** the folder `700`, every file `600`

---

## What this folder is

The one place credentials are allowed to exist on disk: access guides, connection notes, the
location of a key. It is **gitignored in full** — it is the only folder in the engine whose
content never, under any circumstance, enters version control.

> ## ⛔ THE RULE THAT DEFINES THIS FOLDER
> **A document says WHERE a credential lives. It never says WHAT it is.**
>
> Everywhere else in the system, that rule points *here*. Inside here, the rule is narrower: a
> guide explains how to connect and which file holds the key — the value itself belongs in the
> password manager, the environment, or the key file, and nowhere a document can quote it.

⚠️ **This README is the only file in this folder that travels.** It ships to explain what goes
here. Everything beside it is yours and stays.

---

## ⭐ WHY A LEAKED SECRET IS ROTATED, NOT DELETED

This is the single most important thing to understand before touching anything here.

**Deleting a leaked secret does not un-leak it.** Once a value has been written somewhere it did
not belong, assume it has been read:

| Where it went | Why deleting is not enough |
|---|---|
| a git commit | the object survives history rewriting and stays reachable by its hash |
| a session transcript | the file is on disk, and it is the kind of file that gets copied around |
| a chat, a screenshot, a log | out of your control the instant it was rendered |
| a published repository | ⭐ cloned, cached and indexed before you noticed |

⭐ **So the only real remedy is to make the value worthless: rotate it.** Change the credential at
its source, then clean up. Cleaning up first and calling it fixed leaves a live secret in the wild
and a false sense that it was handled.

⛔ **Corollary that decides everyday behaviour:** if a secret ever appears in a tool's output, in
a log, or in a document, it is **rotated** — not edited out. Editing it out is housekeeping;
rotating it is the fix.

---

## Permissions — and why they are checked, not trusted

| Target | Mode | Meaning |
|---|---|---|
| the folder | `700` | only the owner may enter it |
| every file | `600` | only the owner may read it |

⭐ **The battery measures the real modes** — it does not take the documentation's word for it.
A permission that is written down but not applied is exactly the class of rule that gets followed
40-60% of the time, and this is not a folder where those odds are acceptable.

⛔ **No `!README.md` exception in the ignore rules.** It is tempting to un-ignore one harmless
file in here so the folder shows up in the repository. Do not: an exception inside a secrets rule
is one edit away from letting a real file through, and the failure would be silent.

---

## How an agent is allowed to read this folder

Blocking it outright fails in practice: the agent then cannot connect to anything or record a new
credential's location, and the workaround is asking a human to paste values by hand — which puts
the value in the conversation, the exact outcome the block was meant to prevent.

So access is governed rather than forbidden, along three lines:

| Situation | Response | Why |
|---|---|---|
| **read**, with live permission | allow | permission was granted when the context loaded |
| **read**, no permission | ⚠️ ask | the human decides, in the moment |
| ⛔ **write, create or delete** | ⚠️ **always ask** | changing a credential is never automatic |

⭐ **Permission is tied to the context, not to a clock.** A "valid for 60 minutes" grant is
arbitrary — it corresponds to nothing real. **Permission is born when the context loads and dies
when the context reloads**, which makes it part of startup, like the rules themselves: read once,
valid while that load lasts, renewed on the next one.

⛔ **This is not lifting the restriction for convenience.** Writing still asks, every time. What
governed access changes is *impossible* into *possible, with permission and with a record*.

---

## The access log

Every read of this folder is recorded: **which file, when, and why** — ⛔ never the content.

⭐ **The point is not catching an intruder — it is being able to answer "was this opened?" later.**
Without a record, a leak investigation has no starting point, and the honest answer to *"did
anything read that file?"* is *"there is no way to know"*, which is the worst answer to have.

The log lives in this folder, so it is gitignored like everything else here.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| an access guide: how to connect, which file holds the key | ⛔ **the key, the password, the token, the connection string** |
| where a credential lives (path, manager, vault entry) | a credential pasted "just while I test something" |
| the access log | anything another folder could hold safely |
| notes about rotation: when, and what triggers it | 🤖 anything a script generates |

⚠️ **The "just while I test" case is the one that actually happens.** A value pasted temporarily
is a value that was on disk, and the temporary file gets committed by a wildcard, backed up, or
copied. There is no safe temporary secret; there is only a secret and a rotation.

---

## ⚠️ Before you put a file here — the four questions

1. **Does this file contain a value, or a location?** A value does not belong on disk here — only
   the pointer to where it lives.
2. **Could it live outside the repository entirely?** ⭐ Prefer that. A key in a key file outside
   the tree cannot be committed by accident, and accidents are what this folder is defending
   against.
3. **If this leaked, what would you rotate?** If you cannot answer, you do not know what the file
   grants — and you cannot contain a breach you cannot describe.
4. **Does anything reference it from outside?** Point at the file, never quote from it. A
   quotation is a copy, and a copy is a second place to leak from.

---

## ⛔ If a secret has already leaked

1. **Rotate it at the source.** Before anything else — the old value is compromised from the
   moment it was exposed, not from the moment you noticed.
2. **Then clean up** the file, commit or log that carried it.
3. **Then write down what happened** and what triggered it, where the team will see it — not in
   this folder, which nobody reads by design.

⭐ **In that order.** Cleaning up first hides the evidence while the live credential is still out
there, and the incident then looks resolved to everyone including you.

---

Related: `../CAPABILITIES.md` §4 (what must never be touched) · `../.gitignore` (why nothing here
travels) · `../docs/WORKSPACE.md` (which says WHERE credentials live, never what) ·
`../rules/` (the config-hygiene rule this folder implements) · `bin/README.md`.
