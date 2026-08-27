# Mente OS — startup

**Status:** current · **Type:** entry-point · **Updated:** {{date}} · **Owner:** {{owner}}
**Level:** 🚪 the STARTUP — it neither inherits nor is inherited (carries no rules)
**Verified by:** `Mente/bin/check-links` · `Mente/bin/test-f0-f6` (§F6 · router + metrics)
**Scope:** ⚠️ ENGINE document — it ships with the tool and says nothing about your project.

> ## 🔌 HOW THIS FILE IS LOADED — one line in YOUR CLAUDE.md
>
> Claude Code does **not** read this file on its own: files in subfolders load only when it
> touches something in them. It arrives through an import that `bin/init` appends to your own
> `CLAUDE.md`, at the root of your project:
>
> ```
> @Mente/CLAUDE-MENTE-OS.md
> ```
>
> ⭐ **That single line is the only thing Mente OS ever writes outside `Mente/`** — and it is
> APPENDED, never overwritten. Your `CLAUDE.md` keeps every rule you already had; Claude Code
> concatenates both into context rather than picking one. If you have no `CLAUDE.md`, `bin/init`
> creates one containing just that line.

## Purpose

Route the start of a session: **where to go read**, what runs on its own, and which rule governs.
It stores no rules and no state — it points at them, so the value is read from where it is measured.

> **It is a ROUTER, not a rule store.** It points to where rules live; it does not repeat them.
> A rule written here has no declared level — and that was the bug (`Mente/rules/rule-inheritance.md`).

---

## 🚀 STARTUP (always do this, without the owner asking)

1. **READ FIRST** `Mente/memory/RETOMAR.md` (~5 KB) — the cold-start brief: where we left off +
   next step + flags + pointers. **In ~90% of cases it is ALL you need.**
2. ⛔ **Do NOT read** any large historical file unless a pointer in
   RETOMAR sends you there explicitly. Reading it "just in case" burns tokens — measured.
3. **If a block is active** → load its Tier 1 (`§A-E` of `Mente/work/blocks/active/*/BLOCK.md`).
   ⭐ **And if that block belongs to a CAMPAIGN** (`Mente/work/campaigns/*/CAMPAIGN.md` lists it in its
   `§E`) → also load the campaign's **`§F Shared context`**. It is the BIG context, the same for
   all its blocks: without it, switching blocks **resets the why**.
   If `§A-E` is not enough → **say so, do not infer.**
4. If the owner says "read RETOMAR" → that file + its pointers.

**Why:** resuming after a pause resends the whole conversation (cache miss) = expensive. Mente OS
stores everything on disk, so `/clear` is safe **when the session is registered** (§ rule below).

---

## 🧭 RULE ROUTER — 3 levels, inherited downward

```
🌐 UNIVERSAL   Mente/base-rules.md        any project · from the first response
      │ inherits (may ADD or TIGHTEN — never LOOSEN)
      ▼
🏢 PROJECT     PROJECT-RULES.md           this is {{project}}: the gate, server-first, the scope
      │ inherits
      ▼
📦 BLOCK       Mente/work/blocks/active/<n>/BLOCK.md §B    only while that block is open
```

| What you need | Where it is |
|---|---|
| **Conduct** — do not state without measuring · do not invent criterion · explain before building | `Mente/base-rules.md` |
| **This project** — scope, the gate to other Mente OS, server-first, security, identity | **`PROJECT-RULES.md`** |
| **The voice** — how Mente OS communicates | `Mente/memory/principles/owner-0-voice.md` (vehicle: `outputStyle: "{{project}}"`) |
| **Large work** — the F-phase method | `Mente/rules/ESTANDAR_Metodo_Fases_F.md` |
| **Open/close a block** | `Mente/rules/block-lifecycle.md` |
| **Which standard applies to the code I am about to touch** | 🤖 the hook `Mente/hooks/pre-edit-standards.py` injects it on its own |
| **System architecture** | the architecture pillar declared in config |
| 🤖 **WHAT I CAN RUN and what I must not touch** — the validators, the gates, the engine/instance line | ⭐ `Mente/CAPABILITIES.md` |
| 🗺️ **Where everything on THIS machine is** — repos, what is locked, where secrets live (never their value) | `Mente/docs/WORKSPACE.md` |
| 🚢 **How a PR ships** — branch → verify → PR → ⛔ do not merge (owner's discipline) | `Mente/rules/rule-shipping-flow.md` |
| ⭐ **WHICH REPO this work goes to and who governs it** | declared in `Mente/cuentas.tsv` |

> ⭐ **Rules ADD UP, they never loosen.** Two blocks share rules only if one declares the other in
> its `§C`. On conflict, **the stricter one wins.**

---

## 🤖 WHAT THE SYSTEM VERIFIES ON ITS OWN (no need to ask)

| When | What runs |
|---|---|
| at session start | `Mente/hooks/session-start.sh` → health + structure + indexes + drifting blocks. **Speaks only on 🔴** |
| before editing | `Mente/hooks/pre-edit-standards.py` → injects the owning block's `§D` |
| before editing | `Mente/hooks/gate-critical.py` → 🔴 DB with no rollback · 🔴 closing an insufficient block · ⚠️ a piece with dependents |
| before a commit | `Mente/hooks/pre-commit.sh` → 🔴 **BLOCKS** a block that violates its contract |
| is this product or MVP? | `Mente/bin/grade-block <block>` → **measured** verdict, never opinion |
| is the tree the declared one? | `Mente/bin/check-structure` → reads `Mente/piezas.tsv` |
| regenerate the indexes | `Mente/bin/generate-index` → 🤖 `docs/INDEX.md` + `docs/STATES.md` |
| before `/clear` | `Mente/bin/check-clear-ready` → 🔴 refuses if something would be lost |
| **the whole system** | `Mente/bin/test-f0-f6` → the only thing that matters is `failed: 0` · the count lives in `Mente/docs/METRICS.md` (`battery.checks`) |

⭐ **This system's measured law:** a rule in code is followed 100%; a rule only in a document is
followed 40-60%. **That is why doctrine is a document and VERIFICATION is a script.**

---

## ⛔ THE `/clear` RULE — register BEFORE closing

When the owner signals a `/clear` (or I propose one), **first** the dying session must be registered
in the session registry your instance declares: a row in the index + its autopsy.

**Verify it with `Mente/bin/check-clear-ready`** — it refuses if it is missing.
Full rule: `Mente/rules/rule-session-close.md`. Origin: a very large runaway session that had to
be recovered from disk.

> `/clear` is a **cut, not a save.** Whatever is not on disk is lost with no warning.
> That is the origin of *"before the clear it told me all was perfect, after it told me it was still broken."*

---

## 🗂️ WHERE EVERYTHING LIVES

| Folder | What |
|---|---|
| `Mente/base-rules.md` · `PROJECT-RULES.md` | 🌐 and 🏢 the rules, by level |
| `Mente/work/blocks/` | 📦 the work — `active/` `blocked/` `archive/` |
| `Mente/rules/` | contracts + rules + `decisions/` (the ADRs) |
| `Mente/memory/principles/` | the owners (owner-0..3) + `expertise/` |
| `Mente/bin/` · `Mente/hooks/` | 🤖 the validators and the gates |
| `Mente/docs/` | plans, analyses, phase logs · 🤖 `Mente/docs/INDEX.md` and `Mente/docs/STATES.md` generated |
| `Mente/piezas.tsv` | ⭐ **where each key piece lives** — moving something costs 1 line |
| `Mente/Cerebro/vision/` `Mente/work/` `Mente/memory/` `Mente/connection/bridges/` | 🆕 vision · the work · live memory · the gate |
| `Mente/Cerebro/` | your project's own thinking — the architecture pillar and the vision |

---

## 📌 STATE

> ⚠️ **This section carries NO numbers.** A router that declares state goes stale: once, the battery
> count, the product version, and the last phase's progress were frozen here — all three were
> already false. A copied number is correct **exactly once.** Only pointers go here: the value is
> read from the file that measures it, so it cannot fall out of date.

⬜ **Describe your project's state in ONE line** — or delete this line and leave only the pointer
table below. NEVER put numbers here (they belong in `Mente/docs/METRICS.md`).

**Mente OS v2** = the block system that governs this repo: validators + hooks + 3 rule levels.
**The living proof is `Mente/bin/test-f0-f6`; the only thing that matters is `failed: 0`.**

| You need… | Read it from… |
|---|---|
| ⭐ **real state + next step** | `Mente/memory/RETOMAR.md` |
| any **live number** (battery, gaps, permissions, quotes) | 🤖 `Mente/docs/METRICS.md` |
| product version · closed phases · which blocks exist | `Mente/memory/RETOMAR.md` §5 |
| open pending items | `Mente/memory/PENDIENTES.md` |

---

Related: `PROJECT-RULES.md` (🏢 the project level this router declares) · `Mente/base-rules.md` (🌐 universal) · `Mente/memory/RETOMAR.md` (the real state) · `Mente/rules/rule-inheritance.md` (why rules do NOT go here) · `Mente/rules/contract-document.md` (the form this file meets).