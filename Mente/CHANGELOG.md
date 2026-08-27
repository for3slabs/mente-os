# CHANGELOG — Mente OS

**Status:** current · **Type:** append-only · **Updated:** {{date}}
**Verified by:** `bin/test-f0-f6` — the top entry here and the `VERSION` file must match.
**Scope:** ⚠️ ENGINE document — the history of the **tool**, not of any project built with it.

---

## Purpose

What changed in the engine, version by version, so someone who installed 0.1.0 can tell what
0.2.0 gives them without reading a diff.

> ⭐ **The version lives in ONE place: `VERSION`.** Everything else reads it from there. A number
> copied by hand is correct exactly once.

> ⚠️ **This file is not yours to fill in as an installer.** It is written by whoever publishes a
> version of Mente OS. Your project's own history belongs in your instance — the logbook, the
> archived blocks, the ADRs. Mixing the two makes it impossible to tell what the tool changed
> from what you changed.

**Append-only.** New versions go on top; past entries are never rewritten. If an entry turns out
to be wrong, the correction goes in the next version, saying what was wrong — the mistake is part
of the history.

---

## How an entry is written

```markdown
## <version> — <date>

One line saying what this version is FOR — the reason to upgrade.

### <what changed, grouped by what it does for the user>
- **The change** — what it does now. Why it matters: the consequence.

### ⚠️ Breaking
- what stops working, and the exact command that fixes it.
```

⭐ **Group by what the user gains, never by folder.** *"Blocks can now be resumed from disk alone"*
is an entry; *"changes in bin/"* is a directory listing.

⛔ **A breaking change is never buried at the bottom.** If an upgrade needs an action, that action
is in the entry — the person reading it is deciding whether to upgrade right now.

---

## 0.1.0 — the first numbered version

⬜ **Replace this block with your first real entry when you cut a version.**

> ⭐ **Why numbering can start at `0.1.0` even for a system that already works:** a name like
> "v2" describes the **architecture**, not the maturity. `0.x` states something measured — built
> and verified, with no external field installation yet. The history before the first number is
> not lost: it lives in the ADRs (`rules/decisions/`) and in the instance's own logbook. This
> file starts where the *versioning* starts, not where the system started.

---

Related: `VERSION` (the single source of the number) · `rules/decisions/` (the ADRs behind each
change) · `README.md` (what the engine is) · `QUICKSTART.md` (installing it).
