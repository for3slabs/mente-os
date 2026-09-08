"""scaffold — what opening a unit of work requires, whatever kind it is.

⭐ ONE READER, TWO SCAFFOLDERS. `new-block` and `new-campaign` ask the same four
questions before writing anything: is this id usable as a folder name, is it
already taken, who owns this installation, and does the template exist. ⛔ Two
copies of those answers is two places to fix a refusal — and the day they
disagree, one tool accepts what the other rejects and the tree holds both.

⚠️ Shared under `CHK-SHR-001` (rules/rule-checks-must-measure.md): ONE shape read
in several places. ⛔ What differs between a block and a campaign — their
sections, their vocabulary, their index — stays in each scaffolder, because that
is a different shape and `CHK-SHR-002` gives it its own reader.

Not a command. The `.py` suffix says so (bin/README).
"""
import os
import re
# ⭐ plat, for a path this returns to a CALLER that prints or compares it.
# ⚠️ Safe as a bare import: every importer of this helper has already put
# bin/ on sys.path — it is how they reach this file at all.
import plat
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
            out[m.group(1).strip("`* ")] = plat.rel(dp, os.path.dirname(root))
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
    # ⭐ STRIPPED HERE, not by each caller. 🔴 Measured 2026-09-08: the stripper
    # lived inside `bin/init`, so every block `new-block` opened was born with
    # `⚠️ TEMPLATE — bin/new-block copies this to …` as its first line, and the
    # assistant read it as an instruction. ⛔ Leaving it to the callers means a
    # scaffolder added tomorrow forgets it, and nothing notices for weeks.
    return strip_scaffold(body)


# ⚠️ The scaffolding comment every template opens with: an instruction to
# whoever EDITS the mould, addressed to nobody once it is stamped.
_SCAFFOLD = re.compile(r"\A<!--\s*⚠️\s*TEMPLATE\s*—.*?-->\s*\n", re.S)
# ⚠️ A YAML template cannot use an HTML comment, so its scaffolding is a run of
# `#` lines instead — 🔴 found by the probe, which reads the RESULT and does not
# care what the comment syntax was.
_SCAFFOLD_HASH = re.compile(
    r"\A(?:#[^\n]*\n)*?#[^\n]*THIS IS THE TEMPLATE[^\n]*\n(?:#[^\n]*\n)*\s*")


def strip_scaffold(text):
    """Remove the template's own instructions before it becomes a real file.

    🔴 THE FAILURE, measured 2026-09-07 on a real installation. Nine templates
    open with `<!-- ⚠️ TEMPLATE — bin/init copies this to … -->`, and the
    installer copied it through: the person's own `memory/RESUME.md` began by
    saying it was a template and that "you never write this file by hand".
    ⛔ No validator caught it — `check-document` reads the header, never
    whether a file is still its own mould.
    ⚠️ And the assistant read it as an instruction: the scaffolding was
    teaching it that the memory was not its to fill in.

    🔴 AND THE HALF THAT WAS STILL BROKEN, measured 2026-09-08 while auditing
    templates/ one file at a time. This function lived INSIDE `bin/init`, so
    only `init` stripped anything: every block `new-block` opened was born
    carrying `⚠️ TEMPLATE — bin/new-block copies this to …` as its first line.
    ⛔ The assistant reading that block read an instruction meant for whoever
    edits the mould.

    ⭐ CHK-SHR-001 · it lives HERE now, beside the other question both
    scaffolders ask, so a fix reaches every caller instead of one.
    """
    text = _SCAFFOLD.sub("", text, count=1)
    return _SCAFFOLD_HASH.sub("", text, count=1)
