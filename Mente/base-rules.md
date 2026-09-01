# BASE RULES · Mente OS
**Status:** current · **Type:** entry-point · **Updated:** {{date}} · **Owner:** {{owner}}
**Language:** US English
---

## Purpose

The **minimum any AI needs to operate Mente OS.** Written to be tool-agnostic: if you are not Claude
Code, this file plus the pointers below is enough to work correctly.

> **Why it exists:** everything else in v1 assumed Claude Code. `output-styles/` and hooks are
> **acceleration, not foundation** — without them the protocol still works, with less guarantee.

---

## 1 · STARTUP — in this order

```
1 · BASE RULES               ← this file
2 · CONTEXT                  ← what was being worked on
3 · LAST STATE               ← memory/RESUME.md
4 · WHICH ARCHITECT?         ← what profile does this task need
5 · TOOLS
6 · OPEN or LOAD the BLOCK
```

**Transversal rule:** *functions and actions always happen inside a block.* Nothing runs outside one.

---

## 2 · THE NON-NEGOTIABLES — by level

> ⭐ **These six are UNIVERSAL: each one holds in any project, including one that does not exist
> yet.** ⛔ A rule that names a specific path, service or machine is not universal — it belongs at
> the project level, and `rules/rule-inheritance.md` §2 is the test that decides.

| # | Rule | Pointer |
|---|---|---|
| 1 | **Explain → approve → build.** Never build a milestone without explicit approval | ⬜ your method, declared in `PROJECT-RULES.md` |
| 2 | **The AI does not invent criterion.** Criterion is the owner's; the AI gives it form | the decision record that settles it |
| 3 | **Do not state — report the measurement.** An unverified claim is banned | `memory/principles/owner-0-voice.md` |
| 4 | **Secrets are referenced, never pasted** | architecture §12-S.1 |
| 5 | **Scope is declared, never inferred.** No match → **stop and ask** | `rules/rule-working-in-a-block.md` §3 |
| 6 | ⭐ **No `/clear` without registering the session first** | ⬜ `rules/rule-session-close.md` |

> ⬜ **Your project adds its own** in `PROJECT-RULES.md` — a gate to something outside, a
> deploy-target rule, whatever holds here and would be false elsewhere.
>
> ⭐ **The inheritance rule:** a lower level may only ADD or TIGHTEN — ⛔ **never loosen**
> (`rules/rule-inheritance.md` §3).

---

## 3 · EVERY INSTANCE DECLARES ITS IDENTITY

> An instance is not ready to operate until it has declared, in `mente.config.yml`, **who owns it**
> and **what its architectural ground is.** The engine reads these; it never hardcodes them.

| Declared in config | Key | Why it is universal |
|---|---|---|
| **Owner** — how the person is referred to, and the identity checks that protect it | `owner.name` | every instance is operated by someone; the engine must not guess or inherit a previous owner |
| **Architectural pillar(s)** — the file(s) treated as the ground the work builds on | `pillars.architecture` | every project has a source of truth for its shape; docs point at *what config declares*, never at a hardcoded filename |

> 🔴 **Why this is a rule and not a convenience:** when identity travelled hardcoded inside shipped
> files, a clone owned by someone else inherited the previous owner and the previous project's
> architecture — and `bin/init` never asked, because it found the values already written. Identity
> hardcoded is identity leaked.

---

## 4 · WHERE THINGS LIVE

| Need | Path |
|---|---|
| Where we left off | ⬜ `memory/RESUME.md` |
| The voice | `memory/principles/owner-0-voice.md` |
| The three owners | ⬜ `principles/owner-1-docs.md` · `principles/owner-2-dev.md` · `principles/owner-3-validation.md` |
| Expert criterion | `principles/expertise/{database,backend,frontend}.md` |
| Contracts | `rules/contract-block.md` · `rules/contract-document.md` · `rules/contract-adr.md` |
| Rules | `rules/rule-{lanes,fix-not-patch,friction,isolation,session-close}.md` |
| Decisions | ⬜ `docs/DECISIONS.md` (generated) + `rules/decisions/ADR-*.md` |
| Naming | ⬜ `rules/NAMING_CONVENTION.md` |
| Architectural truth | the architecture pillar declared in `mente.config.yml` (`pillars.architecture`) |
| Active blocks | `blocks/active/<name>/BLOCK.md` |
| Open criterion the owner still owes | `docs/PENDING-{{owner}}.md` |
| Secrets | `secrets/` — ⛔ never in git |

---

## 5 · LANGUAGE

| What | Language |
|---|---|
| Conversation with the owner | ⬜ **the owner's language** — declared at install |
| Anything read as an INSTRUCTION (this file, contracts, rules, `BLOCK.md`) | **US English** |
| Code, identifiers, commits | **US English** |

**Do not suggest switching.** ⬜ The owner's own language is where their nuance lives — the
engine never assumes which it is.

---

## 6 · THE LAW BEHIND THE WHOLE DESIGN

| Form of a rule | Measured compliance |
|---|---|
| **Code** (gate, fail-closed permissions) | ✅ **100%** |
| **Document** (the phase method, pre-reset registration, the index) | 🔴 **fails 40-60%** |

> ## The doctrine is a document. The VERIFICATION is a script.
> A script decides nothing — it checks what is checkable: the file exists · has the field · fits its
> limit · the id is unique · it is not stale.

**This is why the validators exist**, and why a rule with no validator should be assumed unenforced.

---

## 7 · IF YOU ARE NOT CLAUDE CODE

What you lose and what you keep:

| Piece | Without Claude Code |
|---|---|
| `output-styles/` (the voice) | 🔴 not injected → **read `memory/principles/owner-0-voice.md` and apply it** |
| Hooks (inject / block) | 🔴 do not fire → **read §D of the block manually before editing** |
| Auto-injected `CLAUDE.md` | 🔴 → **read this file first** |
| Everything else | ✅ works — it is plain markdown and scripts |

> **The protocol is portable. The hooks are the turbo when they exist.**

---

Related: ⬜ `memory/RESUME.md` · `memory/principles/owner-0-voice.md` · `rules/contract-block.md` ·
⬜ `docs/DECISIONS.md` · `mente.config.yml` (identity: owner + pillars) · `CLAUDE.md` (Claude Code entry point).