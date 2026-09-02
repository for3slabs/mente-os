#!/usr/bin/env python3
"""probe-block — does check-block detect what contract-block.md claims?

Two halves: plant each defect in OUR shape, then run against REAL blocks
written in ANOTHER shape. A check proven only on fixtures its own author
wrote has been proven on one shape (rule-checks-must-measure.md §4-D).
"""
import os, re, sys, glob, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK
from fixtures import block, BLOCKS

# ⭐ The cross-run needs real objects nobody here wrote. Where they live
# is the operator's business, never the engine's: a hardcoded path makes
# this probe measure one machine (rule-checks-must-measure.md §5).
REF = os.environ.get("MENTE_CROSSRUN_BLOCKS", "")
p = Probe("check-block", "BLK")

def _path(bid):
    return os.path.join(BLOCKS, bid, "BLOCK.md")


def _sub(bid, a, b):
    q = _path(bid); s = open(q, encoding="utf-8").read()
    open(q, "w", encoding="utf-8").write(s.replace(a, b))


def _re(bid, pat, rep, flags=re.S):
    q = _path(bid); s = open(q, encoding="utf-8").read()
    open(q, "w", encoding="utf-8").write(re.sub(pat, rep, s, flags=flags))


def _strip(bid, head):
    _re(bid, re.escape(head) + r" ·.*?\n\n.*?\n\n", "")

# ⭐ BLK-OPN-002 requires a block to be named by an index. The fixtures are
# real blocks as far as the checker is concerned, so the probe declares them
# where blocks are listed — ⛔ otherwise every clean case fails a rule it was
# not testing, which is the probe's defect, not the checker's.
_idx = os.path.join(BLOCKS, "README.md")
_had_idx = os.path.exists(_idx)
_orig_idx = open(_idx, encoding="utf-8").read() if _had_idx else None
open(_idx, "w", encoding="utf-8").write(
    (_orig_idx or "# Blocks\n") + "\n- %s-a\n- %s-b\n- %s-c\n" % (MARK, MARK, MARK))

print("═══ A · SABOTAGE · check-block ═══\n")
p.baseline()

p.case("① section D is missing",
       lambda: _strip(block(p, "a"), "## D"), "BLK-OPN-001")
p.case("② an invalid type",
       lambda: _sub(block(p, "a"), "type: docs", "type: invented"), "BLK-IDN-002")
p.case("③ an invalid status",
       lambda: _sub(block(p, "a"), "status: active", "status: alive"), "BLK-IDN-004")
p.case("④ an invalid lane",
       lambda: _sub(block(p, "a"), "lane: task", "lane: quick"), "BLK-IDN-004")
p.case("⑤ a scope with no OUT",
       lambda: _re(block(p, "a"), r"### ⛔ OUT\n.*?\n", ""), "BLK-SCP-001")
p.case("⑥ an OUT with no declared source",
       lambda: _sub(block(p, "a"),
                    "- DO NOT touch anything else · DERIVED: another block owns it",
                    "- DO NOT touch anything else"), "BLK-SCP-002")
p.case("⑦ a standard that does not exist",
       lambda: _sub(block(p, "a"), "contract-block.md", "does-not-exist.md"),
       "BLK-STD-002")
p.case("⑧ stale", lambda: _re(block(p, "a"), r"updated: \d{4}-\d\d-\d\d",
                              "updated: 2026-01-01"), "BLK-IDN-005")
p.case("⑨ blocked with no unblocker",
       lambda: block(p, "a", status="blocked"), "BLK-BLK-001")
p.case("⑩ closed with no §K", lambda: block(p, "a", status="closed"), "BLK-CLS-001")
p.case("⑪ closed with an open sub-block",
       lambda: block(p, "a", status="closed",
                     extra="\n## F · Sub-blocks\n\n| # | task | state |\n"
                           "|---|---|---|\n| 1 | x | open |\n\n"
                           "## K · Closing\n\nnot completed: none\n"),
       "BLK-CLS-002")
p.case("⑫ closed with no 'not completed'",
       lambda: block(p, "a", status="closed",
                     extra="\n## K · Closing\n\ncompleted: everything\n"),
       "BLK-CLS-003")
p.case("⑬ an intent that is not one sentence",
       lambda: _sub(block(p, "a"),
                    "intent: a fixture used to prove a check detects what it claims",
                    "intent: one. two. three. and a fourth clause making this far "
                    "too long to be a single statement of purpose."), "BLK-IDN-003")
p.case("⑭ a missing id", lambda: _re(block(p, "a"), r"^id: .*\n", "", flags=re.M),
       "BLK-IDN-001")

p.case("⑮ an empty §C — nobody answered the question",
       lambda: _re(block(p, "a"), r"(## C · Connections\n).*?(?=\n## D)",
                   r"\1\n"), "BLK-CON-001")
p.case("⑯ §C names a block that does not exist",
       lambda: _re(block(p, "a"), r"(## C · Connections\n\n).*?(?=\n## D)",
                   r"\1- DEPENDS ON: %s-ghost\n" % MARK), "BLK-CON-002")
p.case("⑰ a §D with no standard at all",
       lambda: _sub(block(p, "a"), "- `rules/contract-block.md`", "—"),
       "BLK-STD-001")
p.case("⑱ closed with neither acceptance NOR sufficiency",
       lambda: _sub(block(p, "a", status="closed"),
                    "## H · Friction log",
                    "## K · Closing\n\ncompleted: the thing\n"
                    "not completed: nothing\n\n## H · Friction log"),
       "BLK-TRN-001")

# ⬜ CEILINGS · declared as 0 (not measured) by default, so the probe must
# prove BOTH: silent with none declared, firing when one is.
# ⚠️ The ceilings table lives in the SECTIONS half. ⛔ The contract is one thing
# in two files, and a probe that edits the wrong half plants its defect where
# nothing reads it — then reports a working check as undetected.
_c = os.path.join(ROOT, "rules", "contract-block-sections.md")
_o = open(_c, encoding="utf-8").read()
try:
    p.inverse("⑲ with no declared ceiling, NOTHING is measured", lambda: block(p, "a"))
    open(_c, "w", encoding="utf-8").write(
        _o.replace("| ⬜ E `State` | 0 |", "| ⬜ E `State` | 2 |"))
    p.case("⑳ §E over its ceiling, with the ceiling declared",
           lambda: block(p, "a"), "BLK-STA-001")
finally:
    open(_c, "w", encoding="utf-8").write(_o)
    p.clean()

p.case("㉒ SHP · a sibling document beside BLOCK.md",
       lambda: (block(p, "a"),
                open(os.path.join(BLOCKS, MARK + "-a", "notes.md"), "w",
                     encoding="utf-8").write("# notes\n")), "BLK-SHP-001")

p.case("㉓ OPN · a block no index names",
       lambda: block(p, "z"), "BLK-OPN-002")

p.case("㉔ BLK · blocked past the declared period",
       lambda: _re(block(p, "a", status="blocked",
                         fric="- blocked by: the other team"),
                   r"updated: \d{4}-\d\d-\d\d", "updated: 2026-01-01"),
       "BLK-BLK-002")

# ⛔ A field after a `·` on one line was invisible to the reader: real blocks
# write `created: X · updated: Y`, and it reported "no updated date".
p.inverse("㉕ a field after a `·` on the same line IS read",
          lambda: _re(block(p, "a"), r"updated: \d{4}-\d\d-\d\d",
                      "created: 2026-01-10 · updated: " +
                      __import__("datetime").date.today().isoformat()))

p.inverse("㉑ a CORRECT block", lambda: block(p, "a"))
p.crash_guard()




# ── B · the cross-run
print("\n═══ B · CROSS-RUN · bloques reales de otra instancia ═══\n")
p.clean()
real = sorted(glob.glob(os.path.join(REF, "*", "*", "BLOCK.md"))) if REF else []
if real:
    for q in real:
        d = p.track(os.path.join(BLOCKS, MARK + "-" + os.path.basename(os.path.dirname(q))))
        os.makedirs(d, exist_ok=True)
        shutil.copy(q, os.path.join(d, "BLOCK.md"))
    code, out, err = p.run()
    mine = [l for l in out.splitlines() if MARK in l]
    # ⛔ Only OPN-001 signals an unreadable file: it means the four opening
    # sections were not found at all. SHP-002 (sections out of order) is a
    # REAL finding — a real block carries `A B G C D…` with G duplicated — and
    # counting it as illegibility hid a genuine defect behind a probe warning.
    shape = [l for l in mine if "BLK-OPN-001" in l]
    print("  %d bloques reales · %d hallazgos" % (len(real), len(mine)))
    print("     ⭐ de FORMA (el detector no los lee): %d %s"
          % (len(shape), "✅" if not shape else "🔴"))
    by = {}
    for l in mine:
        for m in re.findall(r"BLK-[A-Z]+-\d+", l):
            by[m] = by.get(m, 0) + 1
    for k in sorted(by):
        print("       %-14s %d" % (k, by[k]))
else:
    print("  ⬜ NOT_MEASURED · set %s to a tree of real blocks" % "MENTE_CROSSRUN_BLOCKS")

if _had_idx:
    open(_idx, "w", encoding="utf-8").write(_orig_idx)
else:
    os.remove(_idx)

sys.exit(0 if p.report() else 1)
