# CONTRACT · CAMPAIGN

**Status:** current · **Type:** contract · **Updated:** 2026-08-29 · **Owner:** ⬜ declare
**Applies to:** every file at `campaigns/<name>/CAMPAIGN.md`
**Enforcement:** 🔒 partial — `bin/check-campaign`
**Verified by:** `bin/check-campaign` · `bin/probes/probe-campaign.py`

## Purpose

A campaign is what holds several blocks together when **one block is not enough and one project is
too much**. It does not execute: it **orders**. This contract fixes its shape, what it may claim
authority over, and the three ways it has been measured to fail.

> ## ⭐ A BLOCK ANSWERS "WHAT AM I DOING". A CAMPAIGN ANSWERS "WHY THESE, IN THIS ORDER".
> ⛔ **Without it, switching blocks restarts the reason** — and the cost is paid on every switch,
> by whoever picks the work up cold.

---

## 1 · THE SHAPE

**One campaign = ONE file.** Sections in this order. Default ceiling: **150 lines**.

⭐ **Lower than a block's on purpose:** the campaign does not execute. ⛔ **If it needs 200 lines
to state its mission, either the mission is not clear — or it is two campaigns.**

| Moment | Required |
|---|---|
| **OPEN** | identity · `Mission` · `Authority` · `Blocks` — ⭐ four, no more |
| **While it lives** | the rest, as they become known |
| **CLOSE** | everything + the validator green |

> ⭐ **Cheap to open, expensive to close** — the same principle as the block contract. ⛔ If
> opening one costs ten fields, the work happens *without* a campaign and the context is lost,
> which is precisely what this figure exists to prevent.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CMP-FRM-001` | 🔴 **`Mission`, `Authority` and `Blocks` are required to OPEN** | 🔒 | `bin/check-campaign` |
| `CMP-FRM-002` | **The identity fields are required to OPEN** | 🔒 | `id` · `status` · `created` · `updated` |
| `CMP-FRM-003` | ⭐ **The ceiling is a DEFAULT, and it has a declared exit** | 🔒 | `exempt: size`, written in the file |

### ⚠️ THE CEILING THAT IS RAISED BY DECLARING, NEVER BY IGNORING

⭐ **Measured:** a real campaign carrying the **full cold-start context for twelve blocks** ran to
184 lines. ⛔ Splitting it would have made it useless — the context is the point.

The answer is not to delete the ceiling. It is `exempt: size`, **written in the file**:

```markdown
exempt: size

> This campaign carries the complete context its blocks need to start cold —
> the default ceiling would split it in half.
```

> ## ⭐ A LIMIT WITH A DECLARED EXIT IS STILL A LIMIT.
> ⛔ **A limit with a silent exit is a limit nobody measures** — and the difference between the
> two is one line that says who decided, and why.

---

## 2 · ⭐ HOW MANY BLOCKS — DYNAMIC, no ceiling and no floor

⛔ **This contract does NOT fix a number.** Fixing one produces exactly one of two harms:
**inventing blocks to fill the quota**, or **splitting the mission so it fits**. ⚠️ Both falsify
the work to satisfy a form.

**The only requirement: at OPEN, at least ONE declared block.** ⛔ A campaign with no blocks
orders nothing — it is a title.

```markdown
## Blocks

| block | what it pursues | state |
|---|---|---|
| blk-<id> | one sentence | active · blocked · closed |
```

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CMP-BLK-001` | 🔴 **At least one block, or it is not a campaign** | 🔒 | `bin/check-campaign` |
| `CMP-BLK-002` | ⭐ **Every named block EXISTS on disk, in some state** | 🔒 | ⛔ an orphan child is context pointing at nothing |
| `CMP-BLK-003` | **A block belongs to at most ONE campaign** | 🔒 | ⚠️ two campaigns claiming one block is two authorities |

### 🔴 THE ORPHAN CHILD

⛔ **A campaign that names a block which does not exist is worse than one that names none:** the
shared context reads as complete, the reader trusts it, and the pointer resolves to nothing. ⚠️
The failure appears at the moment somebody tries to pick that block up — cold, with no fallback.

---

## 3 · STANDARDS ARE INHERITED, NEVER COPIED

The campaign's standards section **reaches all of its blocks**. A child block may **ADD** in its
own; ⛔ **never remove** — rules add up, and in a conflict the stricter one wins.

⛔ **Inherit, do not copy.** If the standard is copied into the child, the two lists diverge — the
same defect as any duplicated table, and the divergence is silent because both sides look right.

> ## 🔬 THE TEST THAT TELLS THEM APART
> **Remove a standard from the CAMPAIGN. It must disappear from every child.**
> ⛔ **If it still arrives, it was copied** — and the copy is now the authority nobody declared.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CMP-STD-001` | ⭐ **A child ADDS standards; it never removes one** | 🟡 | ⛔ removing is privilege escalation |
| `CMP-STD-002` | **A standard copied verbatim into a child is a defect** | 📖 | 🔬 the removal test above |

---

## 4 · THE CHANNEL — a fact is written ONCE

When a block needs to know something about another, **the fact is written in the campaign's
channel** — it is not read out of the sibling.

```markdown
## Channel

| fact | contributed by | needed by | date |
|---|---|---|---|
| <the fact, in one sentence> | blk-a | blk-b · blk-c | YYYY-MM-DD |
```

⛔ **The channel does NOT relax isolation:** reading another block's files stays forbidden. What
the channel permits is **reading the FACT, already written** — never the block.

> ## ⭐ WHY IT GOES THROUGH THE CAMPAIGN
> ⛔ **If two blocks read each other directly, each interprets what it sees.** Declared once, both
> read the same sentence — one wording, one interpretation.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CMP-CHN-001` | 🔴 **Every fact names the block that contributes it** | 🔒 | ⛔ an unattributed fact has no one to correct it |
| `CMP-CHN-002` | **Every fact names who needs it** | 🔒 | ⚠️ a fact nobody needs is noise in the shared context |
| `CMP-CHN-003` | ⭐ **The channel carries FACTS, never permissions** | 📖 | ⛔ it does not widen what a block may read |

---

## 5 · CLOSING A BLOCK INSIDE A CAMPAIGN

Beyond its normal closing, a campaign block declares **its impact on its siblings**:

```markdown
### Impact on the campaign

- blk-b · AFFECTED: <what changes for it>
- blk-c · no impact, because <reason>
```

⛔ **Silence does not count.** Saying *"none"* is a valid answer **with its reason**; saying
nothing is not.

> ## ⭐ A CLOSING THAT DOES NOT LOOK AT THE SIBLINGS IS WORK DONE BLIND.
> ⚠️ **And the damage only becomes visible when the sibling breaks** — by which point nobody
> connects it to a block that closed green weeks earlier.

⚠️ **A general archive record looks similar but is not the same:** it points OUTWARD, at what
consumed the block. This one points SIDEWAYS, at the siblings — and nothing else asks that
question.

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CMP-IMP-001` | 🔴 **A closed campaign block declares its impact** | 🔒 | `bin/check-campaign` |
| `CMP-IMP-002` | ⭐ **"None" is valid WITH its reason; blank is not** | 🔒 | ⛔ silence and "checked, nothing" are indistinguishable |

---

## 6 · A CAMPAIGN DOES NOT CLOSE IF…

| Condition | Why |
|---|---|
| a block is still `active` or `blocked` | the same reason a block does not close with open sub-blocks |
| a block closed **without declaring impact** | §5 was left unmet, and the gap is invisible later |
| the authority section is empty | ⛔ nobody would know which yardstick was used |
| the closing section is missing | ⛔ without a verdict there is no close, only an abandonment |

| ID | Rule | Enf | Verify |
|---|---|---|---|
| `CMP-CLS-001` | 🔴 **No open child, or the campaign stays open** | 🔒 | `bin/check-campaign` |
| `CMP-CLS-002` | 🔴 **An empty authority section blocks the close** | 🔒 | `bin/check-campaign` |
| `CMP-CLS-003` | **A closed campaign carries its verdict** | 🔒 | ⛔ closed without a verdict is abandoned, not closed |

---

## 7 · ⚠️ WHAT A CAMPAIGN IS NOT

- ⛔ **Not a replacement for the block.** The block stays the unit of work, its own contract intact.
- ⛔ **Not a way around ceilings.** Children keep theirs; the campaign's exemption is its own.
- ⛔ **Not a drawer.** It names its blocks **explicitly**: what is not listed does not belong.
- ⛔ **Not a place to decide criterion.** Authority is whatever its authority section declares.
- ⚠️ **Not the same as a pending list of the same name.** One records WHAT is missing; the campaign
  organizes HOW it is attacked. ⭐ **If they share a name, each one points at the other** — two
  things with one name and different natures is how a confusion is born.

---

## 8 · 🔴 WHAT THIS CONTRACT ITSELF GOT WRONG, MEASURED

⭐ Kept here because the defect is easy to reproduce and hard to see.

| Defect | What happened | What it cost |
|---|---|---|
| ⛔ **The contract named a section the validator never looked for** | the contract asked for an `Identity` **section**; the real file carried the identity as **header fields**, and the validator checked the fields | 🔴 a file could satisfy the code and violate the contract, or the reverse — and both read green |
| ⛔ **A per-section ceiling written only in the contract** | the shared-context section had a declared limit that no code measured; a real one ran to **112 lines against 40** | ⚠️ the number was decoration: a limit nobody measures is not a limit |
| ⚠️ **The size exemption arrived after the ceiling was already broken** | the ceiling was set, then a real campaign needed more, then the exemption was added | ⭐ the right outcome — ⛔ but it proves a ceiling set without a declared exit gets *ignored* first and *fixed* second |

### ⚠️ AND WHAT THE CROSS-RUN ADDED

⭐ **Two defects found by running this validator against a real campaign nobody wrote for it:**

| Defect | What happened |
|---|---|
| ⛔ **An identity field sharing a line was read as missing** | a real file wrote `created: … · updated: …` on ONE line; the read was anchored to start-of-line and reported `updated` absent while it sat in plain view |
| ⛔ **The block names were written in bold** | `**name**` · the validator strips the emphasis, a second parser elsewhere did not, and the same table produced two different lists |

> ## ⭐ ONE TABLE, ONE PARSER.
> ⛔ **Two readers over one table diverge; one cannot** — and the divergence surfaces as a finding
> against the document, never against the reader that got it wrong.

> ## ⭐ A CONTRACT AND ITS VALIDATOR MUST DESCRIBE THE SAME SHAPE.
> ⛔ **When they drift, the green light stops meaning anything** — and nobody notices, because
> each side is internally consistent.

---

Related: `rules/contract-block.md` (the form this one imitates) · `rules/rule-inheritance.md` (why
standards are inherited and not copied) · `rules/rule-working-in-a-block.md` (the isolation the
channel channels, never relaxes) · `rules/contract-archive.md` (the outward-facing record this
section's sideways one does not replace) · `rules/rule-checks-must-measure.md` (why §8 exists).
