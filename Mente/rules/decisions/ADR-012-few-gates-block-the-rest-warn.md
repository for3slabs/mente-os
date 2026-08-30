# ADR-012 · Few things block. Everything else warns.

date: {{date}}
status: accepted
implementation: implemented
decided-by: ⬜ declare
supersedes: —
superseded-by: —
applies-to: every automated check that can interrupt work
does-not-apply-to: ⭐ a check nobody can act on — that is information, and information never blocks

## Context

⛔ **A gate is not free.** Every one of them spends the same budget: how much interruption the work
will tolerate before somebody turns the mechanism off.

## Decision

**Only a small, named set of actions BLOCK. Everything else warns.** ⬜ **Which actions belong to
that set is the installation's** — ⭐ the engine fixes that the set is SMALL and NAMED, never what
is in it.

⭐ **The criterion that decides membership, and it is not a list:**

- ⛔ a mistake with **no undo** — a destructive migration, an irreversible delete
- ⛔ **closing something that cannot be resumed later** — the loss is silent
- ⚠️ everything else, including frequently-walked paths already covered elsewhere, **warns**

## Rejected alternatives

- ⛔ **Block twenty things.** ⚠️ The system becomes friction and gets disabled — ⭐ **and disabling
  is all-or-nothing: the twentieth gate takes the first three with it.**
- ⛔ **Block nothing, warn everything.** ⚠️ A warning nobody must answer is a warning nobody reads,
  ⭐ **and the reds then arrive indistinguishable from the yellows.**
- ⚠️ **Let each check decide its own level.** ⛔ Every author believes their check is the important
  one, so the set grows by one every time — ⭐ **and nobody is ever the person who added the
  twentieth.**

## Rationale

> ## ⭐ PROTECT FEW THINGS AND THEY ARE HONOURED EVERY TIME.
> ⚠️ **The failure of a gate is not that it lets something through. It is that it gets switched
> off** — and a switched-off gate protects nothing, including the case it was right about.

⛔ **The budget is spent whether the gate is right or not.** A correct gate on a frequent, harmless
path costs the same tolerance as a correct gate on a destructive one.

## Evidence

⭐ **Measured: a gate protecting exactly ONE thing had 100% compliance** over its observed life.
⛔ **No gate protecting many things has ever matched that** in the same system.

⚠️ **And the counter-evidence is structural rather than observed:** ⭐ **nobody has ever reported
disabling a mechanism because it warned too much** — the reports are always about blocking.

## Consequences

- `BLK-TRN-001` 🔒 — ⭐ closing requires acceptance AND sufficiency: **the "cannot be resumed"
  case, enforced**
- `SHP-LCK-001` 🔒 — a commit on the base branch is refused, with a real hook behind it
- ⭐ **`hooks/gate-critical.py`** — the gate itself · ⬜ `MENTE_IRREVERSIBLE_PATTERN` names the
  no-undo case, because what is destructive depends on what is being built
- ⚠️ `WRK-IMP-001` 📖 — measuring dependents before editing is discipline here, not a gate

## What would change this decision

⭐ **It stops being right if the warnings turn out to be ignored at the same rate as blocks are
honoured.** ⚠️ Then the choice is not "few gates versus many" but "gates versus nothing", and the
set would have to grow. ⛔ **That measurement has never been taken** — warnings are counted when
they fire, never when they are read past.

## Reverting

⛔ **Add gates freely.** ⚠️ Adoption falls, and the fall is not gradual: ⭐ **the mechanism is
disabled whole, so the three that were right disappear with the seventeen that were not.**

---

Related: `ADR-019-a-validator-completes-what-is-derivable.md` (⭐ **completion is the OTHER answer to a warning that gets ignored** — read together, or blocking looks like the only option) ·
`ADR-011-four-layers-guarantee-reading.md` (⭐ **its layer 3 INJECTS, it does not block** —
the two decisions govern different budgets and do not compete) ·
`../contract-block.md` (the closing gate) · `../rule-shipping.md` (the shipping gate) ·
`../contract-adr.md`.
