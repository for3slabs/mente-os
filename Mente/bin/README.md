# bin/ — the validators · every executable the engine offers

**Status:** current · **Type:** folder-readme · **Updated:** {{date}} · **Owner:** {{owner}} · **Scope:** ⚠️ ENGINE — travels identical to every
clone. Nothing here is edited per instance.
**Governance:** declared as `engine` in the piece table

---

## What this folder is

Every file here is an **executable that answers exactly one question**, measured against the tree
on disk. Nothing here decides anything, recommends anything, or holds an opinion: a validator
checks what is checkable — the file exists · it has the field · it fits the limit · the id is
unique · it is not stale — and reports.

> ⭐ **The law this folder exists to serve:** a rule enforced by code is followed 100%; a rule that
> lives only in a document is followed 40-60%. **The doctrine is a document. The verification is
> a script.** Every file here is one rule that stopped being a suggestion.

---

## ⛔ THE THREE RULES THAT MUST NEVER BREAK

**1 · No external dependency. Ever.**
Python 3 standard library and bash, nothing else. No `pip install`, no `requirements.txt`, no
vendored package. A validator that needs an install is a validator that does not run on a fresh
clone — and the first thing a new user does is clone.

**2 · A validator never writes, unless its name says so.**  
⭐ Decided in `../rules/decisions/ADR-019-a-validator-completes-what-is-derivable.md` — **what is derivable gets completed; criterion, scope and verdict never are.**
`check-*` and `grade-*` read the tree and report. Only `init`, `new-block` and `generate-*` write,
and each announces every file it touches. A read-only command that silently modified something
would make the whole set untrustworthy.

**3 · Never hardcode a path from one machine.**
⬜ Read it from a shared config reader (`bin/mente_config.py`, not yet written). Measured: four validators once carried an absolute path from a single
computer, and every one of them **failed silently** elsewhere (`if not found: return`). The guard
that existed because of a past incident simply went quiet on any other machine.
⭐ **A guard aimed at a path that does not exist is not a guard; it is a green light.**

---

## What goes in here, and what does not

| ✅ Belongs here | ⛔ Does not |
|---|---|
| a check that can PASS or FAIL against the tree | anything that needs human judgment to conclude |
| a generator that rebuilds a file from measured data | a document — that is `rules/` or `docs/` |
| an installer or scaffolder (`init`, `new-block`) | a hook — automatic firing lives in `hooks/` |
| a command a person types on purpose | anything that stores state — that is `cache/` |

⚠️ **The line against `hooks/`:** what lives here is **invoked**; what lives in `hooks/` **fires on
its own**. A hook may call a validator from here — that is the intended direction. The reverse
(a validator that installs or triggers a hook) inverts the dependency and is a defect.

---

## The shape every executable follows

Copy this. It is not style — three checks in the battery read these fields.

```python
#!/usr/bin/env python3
"""check-something — one line saying what question it answers.

Why it exists: the concrete failure that made it necessary. Not "for quality" —
the actual event. A validator with no cause tends to be a validator nobody trusts.

Usage:
  bin/check-something            everything
  bin/check-something --quiet    exit code only (for hooks)

Exit codes: 0 PASS · 1 REJECT · 2 PENDING (could not measure) · 3 WARN
            rules/rule-checks-must-measure.md §3 · CHK-XIT-001
"""
import os
import sys

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(MENTE, "bin"))
⬜ import mente_config as cfg       # planned · no validator imports it yet


def walk(root):
    """⭐ THE SHAPE FOR READING A TREE — copy this one too.

    ⛔ `except OSError: continue` is the defect this engine writes most often:
    it compiles, it never crashes, and it silently drops a file from a count.
    ⚠️ Measured three times in one session, twice by an author who had just
    fixed it — CHK-CAU-003 caught every one.
    """
    seen, unread = [], []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__", "cache")]
        for f in fn:
            try:
                seen.append(open(os.path.join(dp, f), encoding="utf-8",
                                 errors="replace").read())
            except OSError:
                unread.append(os.path.join(dp, f))   # ⬜ SAID, never swallowed
    return seen, unread                              # ⭐ the caller reports both
```

| Element | Rule | Why |
|---|---|---|
| shebang | `#!/usr/bin/env python3` or `#!/usr/bin/env bash` | never a fixed interpreter path |
| docstring | what it answers · **why it exists** · Usage · Exit codes | the "why" is what stops it from being deleted in a cleanup nobody understands |
| `MENTE` | derived from `__file__`, never a literal | rule 3 above |
| config | through `mente_config` **whenever it needs an instance value** | one parser, one place to fix it |
| `chmod` | `755` — it must be executable | a validator you cannot run is a document with a shebang |

⚠️ **The one file here that is NOT an executable: ⬜ `bin/mente_config.py` (not written yet).** It is a module — imported,
never run — so it carries no shebang and no exit code. It is the single place that knows what is
instance-specific, and every validator that needs an instance value imports it instead of reading
`mente.config.yml` on its own. ⛔ **It parses the config directly rather than using a YAML
library**, on purpose: a dependency that must be installed is a system that does not run on clone,
and this file exists precisely so cloning works. Only scripts that need an instance value import
it; one that only inspects the tree does not have to.

⭐ **Exit codes are a contract, not a convention** — `CHK-XIT-001`, and the table lives in
`../rules/rule-checks-must-measure.md` §3, never here: ⛔ this paragraph said `1 warnings · 2
errors` until 2026-09-01, which had `2` meaning the opposite of what twelve validators use it
for. ⚠️ A template contradicting the rule it teaches is worse than no template.

⭐ `0` PASS · `1` REJECT · `2` PENDING (⬜ could not measure) · `3` WARN. Hooks
and the battery branch on them. A script that returns `0` while printing a red line **is the worst
possible failure**: it looks like it is protecting you and it is not.

---

## Naming — the prefix declares the behavior

| Prefix | Behavior | Example |
|---|---|---|
| `check-` | reads · reports · **never writes** | `check-health`, `check-links` |
| `generate-` | ⚠️ **writes** a file that is rebuilt, never hand-edited | `generate-index` |
| `grade-` | reads · emits a **measured verdict** | `grade-block` |
| `new-` | ⚠️ **creates** something from a contract | `new-block` |
| `test-` | runs the whole battery | `check-all` |
| `verify-` | a composite pre-release pass | `verify-all` |

⛔ **Do not invent a prefix.** Someone reading `pieces.tsv` must be able to tell whether a command
writes to disk without opening it. A new prefix is a new promise nobody knows about.

---

## ⚠️ Before you add a file here — the four questions

Answer all four, or it does not belong here yet.

1. **What single question does it answer?** If it needs "and", it is two validators.
2. **What real failure caused it?** A validator with no incident behind it usually measures
   something nobody acts on, and gets ignored until it is removed.
3. **Can it be verified by sabotage?** ⭐ Break the thing on purpose and confirm it turns red.
   **A check that has never been seen failing is not evidence** — it is a hope with an exit code.
4. **Is it declared in `pieces.tsv`?** A piece written but not declared is a piece
   `check-structure` goes **silent** about the day it disappears.

---

## Where the state goes

Nothing here stores state. A validator that needs to remember what it saw writes to `cache/`,
which is gitignored: committed state would make a clone "remember" something that happened on
somebody else's computer.

---

## The starting point when something is wrong

`bin/check-health` — it names what is wrong in plain language and points at it. If it says
nothing, nothing is wrong.

---

Related: `hooks/README.md` (what fires on its own) · `../pieces.tsv` (where each piece is
declared) · `../CAPABILITIES.md` §2 (what may be run) · `../rules/` (the contracts these verify) ·
`../docs/README.md` (where the generated output lands).
