"""scaffold — what opening a unit of work requires, whatever kind it is.

⭐ ONE READER, TWO SCAFFOLDERS. `new-block` and `new-campaign` ask the same four
questions before writing anything: is this id usable as a folder name, is it
already taken, who owns this installation, and does the template exist. ⛔ Two
copies of those answers is two places to fix a refusal — and the day they
disagree, one tool accepts what the other rejects and the tree holds both.

⚠️ Shared because it is ONE shape read in two places, never to force two shapes
into one reader: what differs between a block and a campaign — their sections,
their vocabulary, their index — stays in each scaffolder.

Not a command. The `.py` suffix says so (bin/README).
"""
import os
import re
from datetime import date

# ⭐ An id becomes a folder name AND is cited from other files, so it is
# constrained at the moment of creation rather than discovered later as a path
# that cannot be written or a citation that cannot be resolved.
ID = re.compile(r"[a-z0-9][a-z0-9-]{1,48}")


def valid_id(value):
    """The id, or None. ⛔ `fullmatch`: a partial match would accept
    `Bad Name!` on the strength of its first word."""
    return value if value and ID.fullmatch(value) else None


def owner(mente):
    """⬜ Read from the installation. ⛔ Never defaulted: an owner nobody chose,
    written into a unit of work, is the same leak bin/init exists to prevent."""
    try:
        for line in open(os.path.join(mente, "mente.config.yml"),
                         encoding="utf-8", errors="replace"):
            m = re.match(r"\s+name:\s*['\"]?([^'\"#\n]+?)['\"]?\s*$", line)
            if m:
                return m.group(1).strip()
    except OSError:
        pass
    return None


def used_ids(root, filename):
    """Every id already declared under `root` → where it lives.

    ⭐ Walked, not listed: a unit of work can sit in any state folder, and a
    scaffolder that only looked in one would hand out an id already taken in
    another. ⛔ Resolution is exact — a repeat makes every citation ambiguous.
    """
    out = {}
    for dp, _dn, fn in os.walk(root):
        if filename not in fn:
            continue          # ⬜ skipped, not a gap: no contract, no unit
        try:
            text = open(os.path.join(dp, filename), encoding="utf-8",
                        errors="replace").read()
        except OSError:
            continue
        m = re.search(r"^id:\s*(\S+)", text, re.M)
        if m:
            out[m.group(1).strip("`* ")] = os.path.relpath(dp, os.path.dirname(root))
    return out


def stamp(template, values):
    """The template with its placeholders filled, or None if it cannot be read.

    ⛔ Returns None rather than an empty string: an empty scaffold written to
    disk is a unit of work whose shape is silently gone, and the caller must be
    able to tell that from a template that simply had nothing to substitute.
    """
    try:
        body = open(template, encoding="utf-8").read()
    except OSError:
        return None
    for k, v in dict(values, date=values.get("date") or
                     date.today().isoformat()).items():
        body = body.replace("{{%s}}" % k, v)
    return body
