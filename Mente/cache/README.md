# cache/ — what the validators remember between runs

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}}
**Scope:** ⚠️ **INSTANCE** — the folder ships empty. Everything written here belongs to one
machine and never travels.
**Governance:** `owner` in `pieces.tsv` · **Gitignored:** in full

---

## What this folder is

The **short-term memory of the validators**. A check in `bin/` is stateless by design: it reads
the tree and reports. But a few of them need to answer a question no single run can — *"has this
changed since the last time I looked?"* — and the answer to that has to survive between runs.

This is where that lands. Nothing else.

> ⭐ **The folder ships empty and is created on demand.** A cache with content in it is a cache
> that came from somewhere else.

---

## ⛔ WHY NOTHING HERE IS EVER COMMITTED

**A committed cache makes a clone "remember" something that happened on another computer.**

The failure is precise: a validator whose job is *"report only what changed"* compares against
what it last saw. If what it last saw arrived inside the repository, it is comparing your machine
against a stranger's state. The results are wrong in the most misleading way available:

| What the validator does | With a foreign cache |
|---|---|
| reports what changed | reports changes that never happened here |
| stays silent when nothing changed | ⭐ **stays silent about a real change** it thinks it already saw |

⭐ **The second row is the dangerous one.** A false alarm gets investigated and dismissed. A
change that never gets reported is invisible, and the validator looks like it is working the
entire time.

⛔ **So there is no "just this one file" exception here.** Not a shared baseline, not a starter
state, not an example. Every entry is a claim about one machine at one moment.

---

## The two things that live here

Both are the same idea — *do not redo what was already done* — at different resolutions.

**1 · Last-seen state** — a small structured file recording what a validator saw on its previous
run, so the next run reports **only the difference**. Without it, a check that watches something
external would repeat its whole output every time, and output that repeats gets ignored.

**2 · Stamps** — a marker saying *"this already ran"*, usually within a period. It exists to keep
an expensive operation off a path that is walked constantly. ⭐ **The engine's own rule applies:
a guard that costs more than it protects gets switched off**, and a stamp is often what keeps the
cost low enough for the guard to survive.

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| the last state a validator saw, to diff against | anything a person wrote |
| a stamp saying an operation already ran | ⛔ **any secret, token or credential** — that is `secrets/` |
| a derived index that can be rebuilt at no cost | 🤖 a generated document — that is `docs/` |
| genuinely disposable working state | ⛔ the only copy of anything |

---

## ⭐ THE TEST THAT DECIDES EVERY CASE

> ## Delete this entire folder. Does anything break?
>
> **The answer must be no.**

If deleting a file here loses something, that file was **never cache** — it was data living in
the wrong place. Cache is by definition rebuildable: the next run costs a little more and
everything continues.

⚠️ **This is also the recovery procedure.** If a validator behaves strangely — reporting changes
that make no sense, or staying quiet when it should not — **delete the folder's contents and run
it again**. A corrupted cache and a broken validator look identical from outside, and this
separates them in one step.

---

## ⚠️ Before you write to this folder — the four questions

1. **Could you recompute it instead?** ⭐ Prefer recomputing. State is the thing that goes stale,
   and a stale cache is worse than a slow check.
2. **Is it truly disposable?** Answer with the deletion test above, not with intuition.
3. **Does it contain anything about a person, a repository, or a credential?** Then it does not
   belong here — regardless of how convenient it is.
4. **What happens on the very first run, when the file does not exist?** ⭐ It must behave
   correctly with no cache at all. A validator that fails, or that stays silent, when its cache is
   missing is broken on **every fresh clone** — which is precisely where nobody is watching yet.

---

## The line against other folders

| Not to be confused with | The difference |
|---|---|
| 🤖 `docs/` generated files | those are **read by people** and rebuilt on demand; cache is read by machines and disposable at any moment |
| `memory/` | memory is what the system must **not** forget; cache is what it may forget at any time without consequence |
| `secrets/` | ⛔ nothing here is protected — treat this folder as readable by anything running as you |

⭐ **The clearest way to hold the distinction:** losing `memory/` loses knowledge. Losing `cache/`
costs one slower run.

---

Related: `bin/README.md` (the validators that write here) · `../.gitignore` (why nothing here
travels) · `../memory/README.md` (what must survive, as opposed to this) · `../docs/README.md`
(generated files, which are rebuilt but meant to be read).
