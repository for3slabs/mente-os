"""findings — one way to report many findings, shared by every validator.

⛔ A REPORT NOBODY FINISHES IS A REPORT NOBODY APPLIES — the same argument this
engine makes against long documents, applied to its own output. ⭐ One defect
repeated across a hundred objects is ONE defect: it gets shown once, with its
count and an example.

⚠️ Measured on a real instance: a pending list produced 590 finding lines that
were 5 distinct shapes. ⛔ Nobody reads 590 lines, so nobody fixed the 5.

⭐ Shared under `CHK-SHR-001` (rules/rule-checks-must-measure.md): ONE shape —
a list of `(id, where, message)` — read in several places. ⛔ Thirteen validators
each inventing a grouping is thirteen report formats, and a reader who must
learn a new one per validator learns none.

Not a command. The `.py` suffix says so (bin/README.md).
"""
import re

# ⭐ What makes two findings "the same shape": the id, the file, and the message
# with its subject removed. ⛔ The subject is what differs — item 7 versus item
# 8 — and keeping it would make every finding unique, which is the state this
# module exists to leave.
SUBJECT = re.compile(r"\b[A-Z][\w-]*\d+\b")
# ⭐ A path is a subject too, and that is what the first version missed. It
# grouped by (id, FILE, shape) — so six blocks with one defect each read as six
# distinct shapes, because the file differed. 🔴 Measured: 18 findings reported
# as 18 shapes when they were 3.
# ⚠️ Two different validators produce two different volumes: one list with many
# items, and many files with one item each. Grouping must collapse both.
PATH = re.compile(r"[\w./-]*[\w-]+/[\w./-]+")
# ⭐ A QUOTED VALUE IS A SUBJECT TOO — it is the object the finding is about, and
# it differs per object by definition. 🔴 Measured: six blocks reporting the same
# missing-index defect stayed six shapes because each named its own id in
# quotes. ⚠️ Only short values: a quoted SENTENCE is the finding's wording, not
# its subject, and blanking it would merge defects that are genuinely different.
QUOTED = re.compile(r"'[^'\n]{1,40}'|\"[^\"\n]{1,40}\"|`[^`\n]{1,40}`")


def shape_of(where, msg):
    """What makes two findings the same defect: the message and the path with
    their SUBJECTS removed. ⛔ Keeping the subject makes every finding unique,
    which is the state this module exists to leave."""
    return SUBJECT.sub("<item>", QUOTED.sub("<name>", PATH.sub("<path>", msg)))


def group(findings):
    """(id, shape) → [(where, message)], in order.

    ⚠️ Order is preserved: the first entry becomes the example, and an example
    from the middle reads like a different defect.
    """
    out = {}
    for cid, where, msg in findings:
        out.setdefault((cid, shape_of(where, msg)), []).append((where, msg))
    return out


def report(findings, rule, quiet=False, examined=None, subject="thing"):
    """Print the findings grouped, and return the exit code.

    ⭐ CHK-QUI-001 · `--quiet` is the exit code ONLY — a caller that asked for a
    number gets a number, and nothing is printed at all.

    ⭐ `examined` is HOW MANY things the caller looked at, and it decides the
    clean-run verdict: a count means ✅, a zero means ⬜ NOT MEASURED.
    ⛔ CHK-TRV-002 · an empty collection is a SKIP, never a pass — and the caller
    is the only one that knows what it was counting, which is why the number
    comes in rather than being inferred here.
    ⚠️ `None` prints nothing, for the callers that still write their own line.
    """
    if not findings:
        if not quiet and examined is not None:
            print("✅ 0 violations" if examined else
                  "⬜ NOT MEASURED · no %s to check · nothing was verified here"
                  % subject)
        return 0
    if quiet:
        return 1
    for (cid, shape), hits in group(findings).items():
        if len(hits) == 1:
            where, msg = hits[0]
            print("🔴 %s · %s · %s" % (where, cid, msg))
        else:
            # ⭐ The count comes first: a reader deciding what to fix needs to
            # know a shape hit forty objects before reading what it says.
            # ⚠️ And WHERE is named by example, because "×40" with no place to
            # start is a number nobody can act on.
            print("🔴 %s · ×%d · %s" % (cid, len(hits), shape))
            print("      e.g. %s · %s" % (hits[0][0], hits[0][1][:80]))
    n, shapes = len(findings), len(group(findings))
    # ⚠️ BOTH numbers, always. The total alone hides that forty lines are one
    # defect; the shape count alone hides how much of the tree is affected.
    print("\n%d violation(s) in %d distinct shape(s) · rule: %s"
          % (n, shapes, rule))
    return 1
