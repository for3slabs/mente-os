#!/usr/bin/env python3
"""probe-archive — does check-archive detect what contract-archive.md claims?

⭐ The point of this contract: a validator that demands a file whose content is
undefined produces empty files that satisfy it. So the probe plants archives
that LOOK complete and are hollow.
"""
import os, re, shutil, sys, glob
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK

ARCHIVE = os.path.join(ROOT, "work", "blocks", "archive")
REF = os.environ.get("MENTE_CROSSRUN_ARCHIVE", "")
p = Probe("check-archive", "ARC")

HEADER = "**Status:** current · **Type:** analysis · **Updated:** 2026-01-15 · **Owner:** x\n"

SUMMARY = """# Summary · %s

""" % MARK + HEADER + """
## Purpose

What this block was and what it left behind.

## What it was for

turn one measured gap into a written standard

## What was built

- the standard, and the check that enforces it

## The quality verdict

every declared check ran · 0 failures · 12 subjects measured

## What was learned

a validator that demands a file whose content is undefined produces empty
files that satisfy it and teach nothing

## What was left out

the second half of the migration — it moved to another block

Related: `README.md`.
"""

CONNECTIONS = """# Connections · %s

""" % MARK + HEADER + """
## Purpose

What this closing changes for whoever opens the next block.

## Pieces owned

- the standard and its check — now free to claim

## Blocks that depended on it

- none declared

## What is still open

- nothing; the remainder moved to another block

Related: `README.md`.
"""

BLOCK = """# BLOCK · %s

## A · Identity

id: %s
type: docs
status: closed

## K · Closing

closed: 2026-01-20
not completed: the second half
""" % (MARK + "-block", MARK + "-block")


def plant(summary=SUMMARY, conns=CONNECTIONS, block=BLOCK, files=3):
    d = p.track(os.path.join(ARCHIVE, MARK + "-block_2026-01"))
    os.makedirs(d, exist_ok=True)
    if files >= 1 and summary is not None:
        open(os.path.join(d, "SUMMARY.md"), "w", encoding="utf-8").write(summary)
    if files >= 2 and conns is not None:
        open(os.path.join(d, "connections.md"), "w", encoding="utf-8").write(conns)
    if files >= 3 and block is not None:
        open(os.path.join(d, "BLOCK.md"), "w", encoding="utf-8").write(block)
    return d


print("═══ A · SABOTAGE · check-archive ═══\n")
p.baseline()

p.case("① one of the three files is missing",
       lambda: plant(files=2), "ARC-SHP-001")
p.case("② the summary carries no document header",
       lambda: plant(summary=SUMMARY.replace(HEADER, "")), "ARC-SHP-002")
p.case("③ a summary field is missing",
       lambda: plant(summary=re.sub(r"## The quality verdict\n\n.*?\n\n", "",
                                    SUMMARY, flags=re.S)), "ARC-SUM-001")
p.case("④ 'what was learned' is empty",
       lambda: plant(summary=re.sub(r"(## What was learned\n\n).*?\n\n",
                                    r"\1x\n\n", SUMMARY, flags=re.S)),
       "ARC-LRN-001")
p.case("⑤ 'what was left out' is empty",
       lambda: plant(summary=re.sub(r"(## What was left out\n\n).*?\n\n",
                                    r"\1-\n\n", SUMMARY, flags=re.S)),
       "ARC-SUM-002")
p.case("⑥ a connections field is missing",
       lambda: plant(conns=re.sub(r"## What is still open\n\n.*?\n\n", "",
                                  CONNECTIONS, flags=re.S)), "ARC-CON-001")
p.case("⑦ a credential in the archive",
       lambda: plant(block=BLOCK + "\napi_key: sk-abcdefghijklmnop\n"),
       "ARC-NEV-001")

p.case("⑦b DEL · the folder does not match the block id",
       lambda: plant(block=BLOCK.replace("id: " + MARK + "-block",
                                         "id: something-else")),
       "ARC-DEL-002")
p.case("⑦c SHP · the folder period is not the closing one",
       lambda: plant(block=BLOCK.replace("closed: 2026-01-20",
                                         "closed: 2026-07-20")),
       "ARC-SHP-003")
# ⛔ Replace the line, never add to it: the fixture already says "moved to",
# so appending a second line left the answer in place and the case planted
# nothing. A probe that adds where it should replace tests the clean state.
p.case("⑦d CON · something is still open and does not say where it went",
       lambda: plant(conns=CONNECTIONS.replace(
           "- nothing; the remainder moved to another block",
           "- the second half of the migration")),
       "ARC-CON-003")

p.inverse("⑧ a COMPLETE archive", lambda: plant())

# ── ⬜ the alias mechanism · it existed, was documented, and never matched:
# the key pattern stopped at the first space and every field name is several
# words. Measured on a real archive: declaring three aliases changed nothing.
# These two cases keep it connected.
# ⛔ PROJECT-RULES.md is an INSTANCE file — born from a template at install
# time — so a clean clone does not have it. Measured: this probe crashed there
# with a bare traceback and left its fixture behind, while scoring 14/14 in the
# tree where it was written. That is CHK-TRV-002, in the probe itself.
_pr = os.path.join(ROOT, "PROJECT-RULES.md")
try:
    _orig_pr = open(_pr, encoding="utf-8").read()
    _had_pr = True
except OSError:
    _orig_pr, _had_pr = "", False
_renamed = SUMMARY.replace("## What was built", "## Qué se hizo")
try:
    p.case("⑧b ALIAS · a renamed section, with no alias declared",
           lambda: plant(summary=_renamed), "ARC-SUM-001")

    open(_pr, "w", encoding="utf-8").write(
        _orig_pr + "\narchive_field what was built = (qué se hizo|what was built)\n")
    p.inverse("⑧c ALIAS · the same section, WITH its alias declared",
              lambda: plant(summary=_renamed))
finally:
    if _had_pr:
        open(_pr, "w", encoding="utf-8").write(_orig_pr)
    elif os.path.exists(_pr):
        os.remove(_pr)        # ⬜ it did not exist here; leave the clone as found
    p.clean()

p.crash_guard()

print("\n═══ B · CROSS-RUN · archivos reales de otra instancia ═══\n")
p.clean()
real = sorted(glob.glob(os.path.join(REF, "*"))) if REF else []
real = [d for d in real if os.path.isdir(d)]
if real:
    # ⛔ The marker cannot ride in the NAME at all: a prefix makes ARC-DEL-002
    # see a renamed block, and a suffix makes ARC-SHP-003 see an invalid
    # period. Measured: 5 false findings each way. ⭐ A cross-run copies the
    # real object VERBATIM, and the filter widens to reach it — the probe
    # adapts to the rules, never the objects to the probe.
    copied = []
    for q in real:
        d = p.track(os.path.join(ARCHIVE, os.path.basename(q)))
        shutil.copytree(q, d, dirs_exist_ok=True)
        copied.append(os.path.basename(q))
    p.also = tuple(p.also) + tuple(copied)
    code, out, err = p.run()
    mine = p._mine(out)
    by = {}
    for l in mine:
        for m in re.findall(r"ARC-[A-Z]+-\d+", l):
            by[m] = by.get(m, 0) + 1
    print("  %d archivos reales · %d hallazgos" % (len(real), len(mine)))
    for k in sorted(by):
        print("       %-14s %d" % (k, by[k]))
else:
    print("  ⬜ NOT_MEASURED · set MENTE_CROSSRUN_ARCHIVE to a real archive")

sys.exit(0 if p.report() else 1)
