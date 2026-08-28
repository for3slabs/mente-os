# work/ — where the work lives

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ **INSTANCE** — the folders and their READMEs travel; ⛔ the work inside never does.
**Governance:** `owner` in `piezas.tsv`

---

## What this folder is

Every piece of work the system governs, in one of two shapes:

```
work/
├── blocks/      📦 ONE unit of work, with a contract — it EXECUTES
└── campaigns/   🎯 several blocks under one mission — it ORDERS
        │
        └── §E lists its blocks  ◄──►  each block's §C names its campaign
                    ⭐ the link is declared from BOTH sides
```

⭐ **The two are not independent folders.** A block can live alone; a campaign cannot — it exists
only to govern blocks, and it must name them while they name it back. **A link declared from one
side only is a link that silently does not load.**

Nothing happens outside a block. That is not bureaucracy — it is what lets the next session pick
the work up **from disk** instead of rebuilding your scope by inference and sounding just as
confident while doing it.

👉 **Each subfolder has its own README with the detail.** This file explains what they are, when
to use which, and the rule that governs both.

---

## The two shapes, and when each applies

| | 📦 **Block** | 🎯 **Campaign** |
|---|---|---|
| Is | **one** unit of work | a mission that needs several blocks |
| Contains | the work itself | ⛔ **no work** — it orders and gives context |
| Executes? | ✅ yes | ⛔ never |
| Size ceiling | larger | ⭐ **smaller — deliberately** |

⭐ **Why the campaign's ceiling is the lower of the two:** a campaign does not execute, it orders.
**If it needs as much room as a block to explain its mission, the mission is not clear — or it is
two campaigns.** The constraint is the check.

⚠️ **You do not start with a campaign.** Open a block. A campaign appears when a second block
turns out to serve the same mission and would otherwise repeat its whole context. Creating the
campaign first is planning a structure for work nobody has started.

---

## ⭐ THE RULE THAT GOVERNS BOTH: cheap to open, expensive to close

> **Opening costs three fields. Closing costs all of them, plus a green check.**

This asymmetry is the whole design, and it is not a convenience:

⛔ **If opening cost ten fields, the work would happen *without* a block** — and the context would
be lost, which is precisely what the block exists to prevent. A process people route around
protects nothing.

✅ **Closing is where the cost belongs**, because closing is the claim that it is done — and that
claim is what the next session will trust.

---

## ⭐ THE TEST THAT DEFINES A BLOCK

> ## Can someone resume this work reading only its first sections, with no memory of the conversation?
>
> **If not, the block does not close — even if the code works.**

That is measurable, and a validator measures it. The sections must answer, on their own:

**what is being built · what must NOT be touched · what it depends on · under which standards ·
what phase it is in · what the next step is · what is blocking it**

⚠️ **"The code works" is not the bar.** A finished piece nobody can pick up is a piece that gets
rebuilt from scratch — or worse, extended by someone guessing at its boundaries.

---

## The lifecycle

```
      new block
          ↓
   ┌──► active/ ──────► archive/     closed · ⛔ never deleted
   │       ↓
   └── blocked/                      waiting on something NAMED, with an owner
```

⛔ **`blocked/` requires naming what it waits for and who resolves it.** A block waiting on
"something" is not blocked — it is abandoned with better manners. If nobody is named, nobody
unblocks it, and it sits there looking like work in progress.

⭐ **Nothing is deleted from `archive/`.** A closed block is consultable experience: the next time
the same question comes up, the answer is written down — including the parts that went wrong,
which are the ones worth reading.

⚠️ **Several blocks may be open; one executes at a time.** Parallel open blocks are fine — that is
reality. Parallel *execution* is how two pieces of work quietly touch the same file and neither
notices.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| a unit of work with its contract | the plan for it — that is `docs/plans/` |
| the campaign that orders several blocks | a rule the work must follow — that is `rules/` |
| decisions taken **inside** a block, in the block | a decision that outlives the block — that is an ADR |
| closed work, archived | anything a script generates |

⚠️ **The line against `docs/plans/`:** a plan describes what **will** be done; a block **is** the
doing, with its state and its contract. A plan that starts tracking progress has become a block in
the wrong folder — and it will not be validated, because nothing checks a plan.

⚠️ **The line against `memory/`:** the block holds what is true **while it is open**; memory holds
what is true **across** blocks. A note that only matters inside one block belongs there — and gets
archived with it, which is correct.

---

## ⛔ Why the work never travels

Every block describes **one installation's work**: its scope, its decisions, its open threads. A
clone inheriting them would start with someone else's unfinished business declared as its own
state — and blocks are read at session start, so the contamination lands on the first decision of
every session.

The folders ship with their READMEs and their structure. **The work is yours and starts empty.**

---

Related: `blocks/README.md` (📦 the unit of work) · `campaigns/README.md` (🎯 the mission above it) ·
`../rules/README.md` (the contracts both must satisfy) · `../memory/README.md` (what outlives a
block) · `../docs/README.md` (plans, as opposed to doing) · `../.gitignore` (why the work stays).
