# work/campaigns/ — 🎯 the mission that orders several blocks

**Status:** current · **Type:** folder-readme
**Scope:** ⚠️ **INSTANCE** — the folder and this README travel; ⛔ the campaigns inside never do.
**Governance:** `owner` in `piezas.tsv` · **Contract:** the campaign contract in `rules/`

---

## 📍 WHERE YOU ARE — read the parent first

```
Mente/
└── work/            ← all work · two shapes, and this one is the OUTER of the two
    ├── blocks/      ← 📦 ONE unit of work · it EXECUTES
    └── campaigns/   ← 🎯 YOU ARE HERE · a mission over several blocks · it ORDERS
```

👉 **Read `../README.md` first** if you have not. It explains when to use which shape and why
`blocks/` comes first. This file assumes that and goes into the campaign itself.

⭐ **This folder does not stand alone.** A campaign with no blocks is a plan; a block with no
campaign is normal. The relationship is described below, and it is the only reason this folder
exists.

---

## What a campaign is

**One campaign = ONE file**, in its own directory, with lettered sections in a fixed order —
the same shape a block has, at one level up.

> ## ⛔ A CAMPAIGN DOES NOT EXECUTE. IT ORDERS.
> No work happens inside a campaign. It holds the mission, the order of attack, and the context
> its blocks share. **The work happens in the blocks, always.**

⭐ **Its size ceiling is lower than a block's, deliberately.** A campaign that needs as much room
as a block to state its mission does not have a clear mission — or it is two campaigns. **The
constraint is the check**, not a formatting preference.

---

## ⭐ THE PROBLEM IT SOLVES: switching blocks resets the why

Without a campaign, several blocks serving one mission each carry their own copy of the
background — the reason the work exists, what was already measured, what was decided across all of
them. Two things then go wrong:

| | What happens |
|---|---|
| The copies **drift** | each block edits its own background; after a while they disagree, and none is marked wrong |
| ⭐ Switching blocks **resets the why** | an agent picking up block 4 knows what block 4 does, and nothing about what the whole thing is for |

**A campaign writes that background once.** Its blocks point at it instead of repeating it — the
same rule that governs live numbers, applied to context: **name the source, never copy the value.**

---

## ⭐ THE LINK IS DECLARED FROM BOTH SIDES

This is the part that makes the relationship real rather than implied:

```
CAMPAIGN.md  §E Blocks ──────────► lists the blocks that compose it
                                            │
BLOCK.md     §C Connections ◄───────────────┘  names the campaign it belongs to
```

⛔ **Both directions are required.** A campaign that lists a block which does not declare it back
is a campaign describing work that does not know it is enrolled — and the shared context never
gets loaded, because nothing at the block's end says to load it.

⚠️ **A campaign may only declare blocks that EXIST.** Listing planned blocks makes the context
point at nothing, and an agent following the pointer finds an empty path with no explanation. Add
the block first, then enroll it.

---

## The sections, and what each is for

| § | Section | Required | What it settles |
|---|---|---|---|
| **A** | Identity | 🔴 to open | what this campaign is |
| **B** | Mission | 🔴 to open | ⭐ what it pursues **and when it ends** |
| **C** | Authority | 🔴 to open | ⭐ **who wins when two documents contradict each other** |
| **D** | Standards | 🟡 while alive | the standards **every** block inherits |
| **E** | Blocks | 🟡 while alive | which blocks compose it |
| **F** | Shared context | 🟡 while alive | ⭐ the big context, identical for all of them |
| **G** | Channel | 🟡 while alive | facts one block needs from another |
| **H** | Closing | 🔴 to close | the verdict |

**Three sections deserve explanation, because they are the ones that do the work:**

**§B — "and when it ends" is not decoration.** A mission with no end condition never closes: every
finished block reveals another worth doing. The end condition is what turns a direction into a
campaign.

**§C — authority is declared before it is needed.** When the campaign says one thing and a block
says another, someone must already have decided which wins. Settling it during the contradiction
means settling it under pressure, in favour of whoever is speaking.

**§F — this is the section the whole figure exists for.** ⭐ It is loaded **together with any of
its blocks**, so switching blocks does not reset the why. If §F is empty, the campaign is an
index, and an index does not need a contract.

**§G — the channel exists so blocks do not read each other.** When one block needs a fact another
measured, the fact is published here. ⛔ Reading into another block's files couples them: the day
one closes, the other breaks in a way nobody predicted.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| the mission and its end condition | ⛔ **the work** — that is always a block |
| context shared by every one of its blocks | context specific to one block — that belongs in it |
| the standards all its blocks inherit | a rule for the whole system — that is `rules/` |
| facts one block publishes for another | one block reading another's files directly |

⚠️ **The line against `docs/plans/`:** a plan describes how something will be done and is not
validated by anything. A campaign has a contract, declares authority, and closes with a verdict.
**If it is not going to govern blocks, it is a plan — and it belongs in `docs/`.**

---

## ⚠️ Before you open a campaign — the four questions

1. **Do two or more blocks already exist that share this mission?** ⭐ If not, wait. A campaign
   created before its blocks is structure built for work nobody started.
2. **What is the end condition?** If you cannot state when it is finished, it is a direction, not
   a campaign.
3. **Who wins in a contradiction?** Decide it now, while nothing is at stake.
4. **What background would every block otherwise repeat?** That is exactly what §F holds — and if
   the answer is "nothing", the blocks do not need a campaign.

---

Related: `../README.md` (⭐ **the parent — read it for context**) · `../blocks/README.md`
(📦 what actually executes) · `../../rules/README.md` (the campaign contract) ·
`../../docs/README.md` (plans, as opposed to governing) · `bin/README.md` (the checks).
