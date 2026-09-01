# CAPABILITIES — what the agent may run, and where the line is

**Status:** current · **Type:** entry-point · **Updated:** 2026-09-01 · **Owner:** Ada Lovelace
**Level:** 📖 reference — it grants nothing and forbids nothing on its own; it states what the
gates already enforce, so nobody has to discover a limit by hitting it.
**Scope:** ⚠️ ENGINE document — it ships identical to every clone and names no machine.

> ## ⛔ MOST OF WHAT THIS FILE NAMES DOES NOT EXIST YET
> ⚠️ **Rows marked ⬜ are planned, not built.** This document is the map of what the engine will
> enforce; ⭐ **`bin/` is the record of what it enforces today.**
>
> ⭐ **A capability map that reads as a promise of working code is the worst kind of leak** — the
> reader trusts it, runs the command, and finds nothing. **Check `bin/` before relying on a row.**


---

## Purpose

Answer two questions before the agent acts, not after: **what can I run here**, and **what must
I not touch**. Both answers are the same in every installation, which is why this file carries
no path, no repo and no name — where *your* machine is described lives in ⬜ `docs/WORKSPACE.md`, generated at install by
`bin/init`.

> ⭐ **Why a document and not a gate:** the actions that block are listed in §3, by name. Everything
> else here is a limit that no script enforces. A limit you have to discover by tripping over it
> was never declared — it was hidden. **A declared limit is engineering; a hidden one is debt.**

---

## 1 · ⛔ THE LINE — the instance is yours, the engine is not

Everything under `Mente/` belongs to one of two sides. Confusing them is the single failure this
whole system is built to prevent.

| | **THE ENGINE** | **THE INSTANCE** |
|---|---|---|
| What it is | the tool — universal | your installation — one of a kind |
| Who governs it | whoever maintains Mente OS | ⭐ **you** |
| Does it travel? | ✅ cloned identical to everyone | ⛔ **never** |
| Folders | `bin/` `hooks/` `rules/` `templates/` `memory/principles/` | `Cerebro/` `memory/` `work/` `connection/` `secrets/` `cache/` |

⛔ **The engine is not edited inside an instance.** If you have to change something under `bin/`
to make Mente OS work on your machine, that is a bug in the engine — report it, do not patch it
locally. A local patch is lost on the next update and takes its reason with it.

⛔ **The instance never travels when the engine is published.** `.gitignore` enforces this half.

> **The authority for this split is `mente.config.yml`** (`frontier_engine`, `frontier_instance`,
> `frontier_mixed`), and `piezas.tsv` must agree with it, one row per piece, in its `governance`
> column. When the two disagree, the config wins and the table is the bug.

---

## 2 · WHAT YOU CAN RUN — the validators

Every one lives in `bin/`, is written in bash or python with **no external dependency**, and
answers exactly one question. None of them decides anything: they check what is checkable.

### The ones that only READ — safe to run at any moment

| Command | The question it answers |
|---|---|
| `bin/check-health` | ⭐ **the two things no other validator watches** — are the hooks WIRED, and is this session still safe to continue |
| `bin/check-structure` | ⭐ does every row in `piezas.tsv` still have its file — the table-side check |
| `bin/check-declared` | ⭐ does every engine file have its row in `piezas.tsv` — the disk-side check |
| `bin/check-document` | does every document carry its header, its ceiling and pointers that resolve |
| `bin/check-block` | ⭐ does **every** block meet its contract — sections, states, closing · it walks them all |
| `bin/check-campaign` | does a campaign name real blocks, and does it close only when they do |
| `bin/check-work` | is the work inside a block staying inside it |
| `bin/check-inheritance` | do the three rule levels add up without a lower one loosening a higher |
| `bin/check-checks` | ⭐ **the validators themselves** — can each one actually fail |
| `bin/check-decisions` | is every decision recorded once, and never rewritten |
| `bin/check-handoff` | is a delegation granted, bounded and accounted for |
| `bin/check-shipping` | does a change leave the way the rule says it must |
| `bin/check-archive` | does a closed block leave behind what the next reader needs |
| `bin/check-pending` | is a debt written in the shape somebody else can pick up |
| `bin/check-config` | is the permission surface complete, portable and free of pasted secrets |
| `bin/check-accounts` | ⭐ does every push target declare who governs it — and does the unavoidable layer RUN |
| `bin/check-adr-wiring` | does every consequence a decision claims resolve to a rule or an artefact |
| `bin/check-gates` | ⭐ **has a gate gone quiet** — a dead gate looks exactly like one with nothing to block |
| `bin/grade-block <block>` | ⭐ **product or MVP — measured**, never opinion (layer 1) |
⬜ | `bin/check-sufficiency <block>` | can this block be resumed from disk alone (§A-E) |
| `bin/check-clear-ready` | ⭐ would resetting the context lose anything — ⛔ the files survive, the reasoning does not |
⬜ | `bin/check-all` | ⭐ the whole system · *the only thing that matters is `failed: 0`* |
| `bin/probes/run-all.py` | ⭐ **the battery** — runs every validator against planted defects · *the only thing that matters is `failed: 0`* |

### The ones that WRITE — they change files on disk

| Command | What it writes | Watch out for |
|---|---|---|
| `bin/init` | the instance files, from `templates/` · the router import · the layer-2 hook link · `secrets/` at 700 | ⭐ **refuses to overwrite** what already exists · `--force` replaces and says what it replaced |
| `bin/new-block <id> --type <t>` | a new block with its §A-D opening contract, and its row in the index | ⭐ refuses a used id, an undeclared type or lane · ⛔ opening costs four sections on purpose |
| `bin/new-campaign <id> --blocks <ids>` | a campaign with its 3 opening sections, holding blocks that EXIST | ⛔ refuses one with no blocks — that is a title, not a campaign |
| `bin/generate-index` | 🤖 `docs/INDEX.md` · `docs/STATES.md` · `docs/DECISIONS.md` | regenerated, never hand-edited · `--check` reports staleness without writing |
| `bin/generate-metrics` | 🤖 `docs/METRICS.md` | ⭐ **the only place a live number belongs** · ⛔ it READS the battery's last result, never runs it |
| `bin/secrets-lease` | the read permission for `secrets/`, and its access log | ⭐ tied to the context load, never to a clock · it hardens the folder before granting |

> ⚠️ ⬜ **`bin/check-all` is planned as the single entry point; today the battery is
> `bin/probes/run-all.py`.** ⭐ The difference matters: the battery proves each validator can
> FAIL, which is a stronger claim than running them all and seeing green.
>
> ⚠️ **The battery takes a lock.** A second run is refused on purpose: both would corrupt
> each other's probe blocks. If it dies badly the lock survives — remove it and run again.

---

## 3 · WHAT RUNS WITHOUT YOU — the gates

You do not invoke these. They fire at the moment they matter, and **most of them do not block**.

| When | What fires | Blocks? |
|---|---|---|
| session start | `hooks/session-start.sh` — runs every validator it discovers | ⬜ informs — **speaks only on 🔴** |
| before an edit | `hooks/pre-edit-standards.py` — the owning block's standards, named back to you | ⬜ injects |
| before an edit | `hooks/gate-critical.py` — destructive SQL with no rollback · an insufficient close | 🔴 **blocks** |
| before a write | `hooks/gate-secrets.py` — a secret VALUE about to reach disk | 🔴 **blocks** · ⛔ fails CLOSED |
| before a specialist | `hooks/gate-handoff.py` — one that may WRITE with no declared scope | 🔴 **blocks** |
| before a push | `hooks/gate-accounts.py` — a destination nobody declared · layer 1 | 🔴 **denies** · ⚠️ can be walked around |
| ⭐ inside the push | `hooks/pre-push.sh` — layer 2, destination already resolved | 🔴 **aborts** · ⭐ cannot be walked around |
| before a commit | `hooks/pre-commit.sh` — a commit on the base branch | 🔴 **blocks** |
| before any action | `hooks/watch-external.py` — external state moved while you were working | ⬜ informs |

⭐ **The ratio is deliberate: most inform, and only what earned it blocks.** A gate that obstructs
more than it protects gets switched off, and a switched-off gate protects nothing.

> ## ⭐ TWO OF THEM ANSWER THE SAME QUESTION IN OPPOSITE WAYS, AND THAT IS THE DESIGN
> ⛔ **`gate-secrets` fails CLOSED** when it cannot complete its check: the damage it prevents is
> a credential on disk, and there is no undo — the rule is that a leaked secret is ROTATED, never
> deleted. ⚠️ **`gate-handoff` and `gate-accounts` fail OPEN**: their worst case is visible and
> reversible, and a broken gate that blocked every delegation would push the work back inline —
> the exact behaviour those contracts exist to prevent.
>
> ⭐ **The question is never "should a gate fail open or closed". It is: is the damage
> reversible?**

⚠️ **`hooks/_beat.py` is not a gate** — it is the shared stamp each one leaves, so
`bin/check-gates` can tell a gate that stopped running from one with nothing to block.

⭐ **Every gate prints how to bypass it. A gate with no escape hatch gets deleted.** A limit you
cannot step over on a justified exception stops being a guard and becomes an obstacle to route
around — and the route around it is invisible.

---

## 4 · ⛔ WHAT YOU MUST NOT TOUCH

| Never | Why |
|---|---|
| **another Mente OS installation** without explicit permission | it is someone else's tree, and reading one costs a great deal of context. The gates that enforce this are the ones you declare in `mente.config.yml` → `gates:` |
| **a secret's value** — write it into any file | it would land in every transcript that reads that file. Say WHERE it lives, never WHAT it is. A leaked secret is **rotated**, not deleted |
| **the engine, to fix an instance problem** | see §1 |
| **a live number, copied into prose** | it is correct exactly once. Numbers live in ⬜ `docs/METRICS.md`, regenerated |
| **`git push`, without being asked** | publishing is not a step in doing the work; it is a separate decision, and it is the owner's |

---

## 5 · THE FIVE RULES YOU WILL HIT FIRST

Not the full set — `base-rules.md` (🌐) and `PROJECT-RULES.md` (🏢) carry that. These five are the
ones a newcomer trips over in the first session.

1. **Explain → approve → build.** Never build a milestone without explicit approval.
2. **Do not state — report the measurement.** *"I did not check this"* is a complete answer.
3. **The AI does not invent criterion.** Criterion is the owner's; the AI gives it form.
4. **Scope is declared, never inferred.** No match → **stop and ask.**
5. **No `/clear` without registering the session first.** `/clear` is a cut, not a save.

---

## 6 · THE LOOP — how work actually moves

```
open a block  →  work inside it  →  the gates check as you go
      │                                      │
      │                                      ▼
      │                          🔴 blocked → fix, or declare the exception
      ▼
bin/check-sufficiency   can it be resumed from disk alone?
⬜ a block grader       product or MVP — measured
      ▼
close it  →  the block moves to archive/ · never deleted
```

**Nothing happens outside a block.** That is not bureaucracy: a block is what lets the next
session pick the work up from disk instead of rebuilding your scope by inference — and sounding
just as confident while doing it.

---

Related: `base-rules.md` (🌐 the universal level) · `PROJECT-RULES.md` (🏢 this project) ·
`mente.config.yml` (the engine/instance frontier, and your gates) · `piezas.tsv` (where each
piece lives) · ⬜ `docs/WORKSPACE.md` (created at install) (⭐ where **your** machine is described) · `QUICKSTART.md`.
