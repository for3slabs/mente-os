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

# ── BLK-CHK-001..004 · a checkpoint is EVIDENCE, not a note ────────────────
# ⛔ "backend done" satisfies a free-form shape and records nothing anybody can
# act on. ⭐ The two fields that decide whether the work can be trusted are the
# two nobody writes unprompted: what did NOT change, and whether the scope held.
_CHK = ("- **2026-01-15 · iteration 1**\n"
        "  changed: the reader\n"
        "  did not change: the gate, the template\n"
        "  pieces: bin/check-block\n"
        "  standard: rules/rule-checks-must-measure.md\n"
        "  verified: bin/probes/run-all.py → all green\n"
        "  unexpected: none\n"
        "  remains: none\n"
        "  scope: held\n")


def _with_i(bid, body):
    """Append a §I to a fixture block — ⚠️ the fixture writes none, which is
    itself correct: a block that has not reached a checkpoint has no §I."""
    q = _path(bid)
    open(q, "a", encoding="utf-8").write("\n## I · Checkpoints\n\n%s\n" % body)
    return bid


p.case("㉖ ⛔ the note E-03 names: «backend done»",
       lambda: _with_i(block(p, "a"), "- **backend done**"), "BLK-CHK-001")

p.case("㉗ ⭐ `did not change` omitted — the half that proves the scope held",
       lambda: _with_i(block(p, "a"),
                       _CHK.replace("  did not change: the gate, the template\n", "")),
       "BLK-CHK-001")

p.case("㉘ ⭐ `scope` present but blank answers nothing",
       lambda: _with_i(block(p, "a"), _CHK.replace("scope: held", "scope:")),
       "BLK-CHK-004")

# ⛔ THE `break` THAT HIDES THE REST — DOC-CNT-004 already paid for this one.
p.case("㉙ ⛔ three checkpoints, the middle one incomplete → it is named",
       lambda: _with_i(block(p, "a"),
                       _CHK + "- **2026-01-16 · iteration 2**\n  changed: x\n"
                       + _CHK.replace("iteration 1", "iteration 3")),
       "BLK-CHK-001")

p.inverse("㉚ ⭐ the eight fields present → no finding",
          lambda: _with_i(block(p, "a"), _CHK))

# ⭐ `widened: <what>` is an ANSWER, not a violation: scope may widen, and
# BLK-SCP-004 requires the decision be visible — which is what this records.
p.inverse("㉛ ⭐ `widened: the parser` is a valid answer",
          lambda: _with_i(block(p, "a"),
                          _CHK.replace("scope: held", "scope: widened: the parser")))

# ⬜ A block with no §I has not reached a checkpoint — a state, not a defect.
# ⛔ §I is 🟡; demanding it exist would make every fresh block fail its contract.
p.inverse("㉜ ⬜ no §I at all → silence, not a demand", lambda: block(p, "a"))

# ⭐ THE CASE THAT KEEPS THE FIELDS IN ONE PLACE: rename one in the CONTRACT and
# the checker must demand the new name. ⛔ Without this, someone "simplifies" the
# reader by hardcoding the eight, and the copy is the half that goes stale.
#
# 🔴 IT RUNS ON A COPY OF THE TREE, NEVER THIS ONE. The first version edited the
# real contract and marked it with p.track() to be tidied up — ⛔ but track()
# DELETES its fixtures, and the contract was deleted. ⚠️ A probe that writes to
# the engine it is measuring can destroy it, and "the probe cleans up after
# itself" is exactly the assumption that made it possible.
def _contract_follows():
    import shutil as _sh, subprocess as _sp, tempfile as _tf
    w = _tf.mkdtemp(prefix="mente-chk-")
    t = os.path.join(w, "Mente")
    _sh.copytree(ROOT, t, ignore=_sh.ignore_patterns(
        "__pycache__", ".beats", ".test-lock", ".git", "cache"))
    d = os.path.join(t, "work", "blocks", "active", "zzchk")
    os.makedirs(d, exist_ok=True)
    _sh.copy(_path(block(p, "a")), os.path.join(d, "BLOCK.md"))
    p.clean()
    open(os.path.join(d, "BLOCK.md"), "a", encoding="utf-8").write(
        "\n## I · Checkpoints\n\n%s\n" % _CHK)
    q = os.path.join(t, "rules", "contract-block-sections.md")
    c = open(q, encoding="utf-8").read()
    open(q, "w", encoding="utf-8").write(
        c.replace("| `remains` |", "| `zzremains` |", 1))
    r = _sp.run([sys.executable, os.path.join(t, "bin", "check-block")],
                cwd=t, capture_output=True, text=True)
    _sh.rmtree(w, ignore_errors=True)
    return "zzremains" in r.stdout


_ok = _contract_follows()
print("  %-46s %s %s"
      % ("㉝ ⭐ a field renamed IN THE CONTRACT is demanded", "✅" if _ok else "🔴",
         "the reader follows the contract" if _ok
         else "🔴 it is hardcoded somewhere"))
p.results.append(("㉝ contract follows", "FAIL" if _ok else "NOT_DETECTED"))

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
