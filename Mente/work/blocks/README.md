# work/blocks/ — 📦 the unit of work

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ **INSTANCE** — the folder and this README travel; ⛔ the blocks inside never do.
**Governance:** `owner` in `piezas.tsv` · **Contract:** the block contract in `rules/`

---

## 📍 WHERE YOU ARE — read the parent first

```
Mente/
└── work/            ← where all work lives · two shapes: blocks and campaigns
    ├── blocks/      ← ⭐ YOU ARE HERE · ONE unit of work · it EXECUTES
    └── campaigns/   ← several blocks under one mission · it ORDERS
            │
            └── if this block belongs to one, its §C names it
                and the campaign's §F must be loaded WITH this block
```

👉 **Read `../README.md` first** if you have not. It explains the choice between the two shapes,
the rule they share (*cheap to open, expensive to close*), and why the work never travels. This
file assumes all of that and goes into the block itself.

⭐ **A block does not need a campaign** — most work is a single block and that is correct. But if
its §C names one, that campaign's shared context is **part of this block's tier 1**: loading the
block without it gives you what the work does and nothing about what it is for.

---

## What a block is

**One block = ONE file.** A directory per block, a single `BLOCK.md` inside it, with lettered
sections in a fixed order.

> ⭐ **One file, not several.** Splitting a short document across files saves nothing and creates
> places that fall out of sync with each other. The internal sections are the structure; the
> filesystem is not.

```
blocks/
├── active/     work in progress — several may exist, ONE executes at a time
├── blocked/    waiting on something NAMED, with someone named to resolve it
└── archive/    closed — consultable experience, ⛔ never deleted
```

---

## ⭐ THE SECTIONS ARE TIERED — that is what makes a block cheap to read

The letters are not a filing order. They are **reading order by cost**, and an agent loads only
the tier it needs:

| Tier | Sections | What it answers | When it is read |
|---|---|---|---|
| **1** | identity · scope · connections · standards · state | ⭐ what is this, what must I not touch, where is it | **always** — at session start |
| **2** | sub-blocks · decisions · friction | how it is progressing, what was already decided | while working on it |
| **3** | checkpoints · context | the long history | only when tier 1 is not enough |

⭐ **The whole design rests on tier 1 being small enough to always be loaded.** An agent that must
read the entire block to know what not to touch will, on a busy day, read none of it.

⚠️ **Every section has a line limit, and the limits are not style.** A scope that needs three
screens is a scope that was never decided — the constraint is what forces the decision. When a
section keeps overflowing, the block is too big and should be two.

---

## The completeness regime — progressive, with a hard minimum

| Moment | Required |
|---|---|
| **OPEN** | ⭐ the first four sections — a couple of minutes |
| **While working** | the middle sections, filled as they become known |
| **CLOSE** | everything, plus the sufficiency check in green |

⛔ **The four opening sections are not negotiable, and the fourth is the one people skip.**
Declaring which standards apply is what lets the editing gate hand you the right criterion before
you touch a file. A block with no declared standards gets edited **with no standards, silently** —
there is no error, just work done to nobody's bar.

---

## ⭐ THE TEST THAT DECIDES WHETHER A BLOCK MAY CLOSE

> ## Can a stranger resume this work reading only tier 1, with no memory of the conversation?

Seven questions, and tier 1 must answer all of them **on its own**:

**what is being built · what must NOT be touched · what it depends on · under which standards ·
what phase it is in · what the next step is · what is blocking it**

⛔ **If it does not, the block does not close — even if the code works.** A validator measures
this; it is not a matter of opinion. And the failure it prevents is specific: the next session
rebuilds your scope by inference and **sounds exactly as confident** as if it knew.

---

## The two sections people underestimate

**`Scope` — and its OUT half is the important one.**
What must **not** be touched is the half that prevents damage. An IN list with no OUT list reads
as *"everything adjacent is fair game"*, and adjacent is where the accidents are.

**`Decisions` — each one with its reason.**
⭐ A decision recorded without its **why** gets reversed by the next session in good faith. The
reason is what makes it hold; without it, the record is trivia.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| a unit of work with its contract | a plan for future work — that is `docs/plans/` |
| decisions taken **inside** this work | a decision that outlives it — that is an ADR |
| the friction found while doing it | a rule everyone must follow — that is `rules/` |
| what is blocking it, and who resolves it | anything true across blocks — that is `memory/` |

⚠️ **The line against `campaigns/`:** the block **executes**; the campaign **orders**. If several
blocks would each repeat the same background, that background belongs to the campaign — write it
once there and let the blocks point at it.

---

## ⚠️ Before you open a block — the four questions

1. **Is this ONE unit of work?** If the scope needs "and", it is two blocks — or one block with
   sub-blocks, which is different from one block with two purposes.
2. **What must NOT be touched?** Answer before starting. Declared afterwards, it is a description
   of what you already did rather than a limit.
3. **Which standards apply?** Name them, or the editing gate has nothing to inject.
4. **Could someone else resume it from tier 1 alone?** ⭐ If not now, then not at close either —
   and closing is where it will be enforced.

---

## Closing, and the archive

A closed block carries a final section: the verdict, what was learned, and **what debt it did not
close**. That last part is the one worth insisting on — a block that closes claiming everything is
resolved teaches the next reader to distrust every other close.

⛔ **Nothing is deleted from the archive.** The next time the same question appears, the answer is
already written — including the parts that went wrong, which are the ones actually worth reading.

---

Related: `../README.md` (⭐ **the parent — read it for context**) · `campaigns` sibling folder
(the mission above a block) · `../../rules/README.md` (the block contract and the lifecycle) ·
`../../memory/README.md` (what outlives a block) · `bin/README.md` (`new-block`, and the checks).
