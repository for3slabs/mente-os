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
# ⭐ TWO FAMILIES, because check-block reports both: the block contract (BLK-*)
# and QLT-LAY-003, the rule that keeps the measuring layer from signing the
# closing verdict. ⛔ Filtering on BLK alone reported a working check as
# undetected — a filter narrower than what the checker emits.
p = Probe("check-block", "(?:BLK|QLT)")

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

# ── BLK-SUB-004 · evidence is a claim someone else can re-run ──────────────
# ⛔ "the system has 55 documents" and "55 documents, bin/check-document,
# 2026-09-01" are different claims: the first cannot be re-checked, so it cannot
# be found wrong — ⭐ and a claim that cannot be found wrong is not evidence.
_HDR = ("| # | task | piece | dependents | acceptance | evidence | status |\n"
        "|---|---|---|---|---|---|---|\n")


def _with_f(bid, rows):
    """Insert §F where it belongs — ⛔ appending it puts F after H, and
    BLK-SHP-002 is right to say so: a fixture that breaks a DIFFERENT rule
    reports a false positive against the check it was meant to test."""
    q = _path(bid)
    t = open(q, encoding="utf-8").read()
    block_f = "## F · Sub-blocks\n\n" + _HDR + rows + "\n\n"
    open(q, "w", encoding="utf-8").write(
        t.replace("## H · Friction log", block_f + "## H · Friction log", 1)
        if "## H · Friction log" in t else t + "\n" + block_f)
    return bid


p.case("㉞ ⛔ evidence that says «done» and nothing else",
       lambda: _with_f(block(p, "a"),
                       "| 1 | migrate it | bin/x | 3 | it runs | done | closed |"),
       "BLK-SUB-004")

p.inverse("㉟ ⭐ a datum WITH its date → no finding",
          lambda: _with_f(block(p, "a"),
                          "| 1 | migrate it | bin/x | 3 | it runs | "
                          "55 docs · bin/check-document · 2026-01-15 | closed |"))

# ⬜ A row with no evidence yet is unfinished work, not a defect — demanding one
# would make every freshly-planned row a violation.
p.inverse("㊱ ⬜ a row whose evidence is still ⬜ is not a defect",
          lambda: _with_f(block(p, "a"),
                          "| 1 | migrate it | ⬜ | ⬜ | ⬜ what done means | "
                          "⬜ what proves it | open |"))

# ⛔ THE break THAT HIDES THE REST, and it names the TASK: "sub-block 2" sends
# the reader counting rows.
p.case("㊲ ⛔ three rows, only the middle one dateless → it is named",
       lambda: _with_f(block(p, "a"),
                       "| 1 | a | bin/x | 1 | ok | ran it 2026-01-15 | closed |\n"
                       "| 2 | b | bin/y | 1 | ok | verified | closed |\n"
                       "| 3 | c | bin/z | 1 | ok | 12 hits 2026-01-14 | closed |"),
       "BLK-SUB-004")

# ── BLK-CLS-007 · a close writes a machine-readable RECORD ─────────────────
# ⛔ A verdict pasted into §K as prose cannot be re-read, compared with the next
# close, or checked against what was measured — ⚠️ and the UNKNOWN list, the
# most valuable part, dies with the session that produced it.
# ⚠️ A COMPLETE §K, because BLK-TRN-001 demands acceptance AND sufficiency: a
# fixture missing either fails a rule it was not testing.
# ⚠️ A COMPLETE §K: BLK-TRN-001 wants acceptance AND sufficiency, and
# BLK-CLS-008 wants the evidence level its lane requires. ⛔ A fixture missing
# either fails a rule it was not testing.
_KOK = ("\n## K · Closing\n\nnot completed: none\nevidence: measured\n"
        "evidence level: L3\n"
        "acceptance: the criteria were met\nsufficiency: pass\n")

p.case("㊳ ⛔ closed and no close.json",
       lambda: block(p, "a", status="closed", extra=_KOK, record=False),
       "BLK-CLS-007")


def _thin_record():
    """A record that exists and says nothing about the six dimensions."""
    bid = block(p, "a", status="closed", extra=_KOK, record=False)
    open(os.path.join(BLOCKS, bid, "close.json"), "w",
         encoding="utf-8").write('{"verdict": "PRODUCT"}')
    return bid


p.case("㊴ ⛔ a record with no `dimensions` · the half prose loses",
       _thin_record, "BLK-CLS-007")

p.inverse("㊵ ⭐ closed WITH a record carrying its dimensions",
          lambda: block(p, "a", status="closed", extra=_KOK))


# ⭐ QLT-LAY-003 · the one who MEASURES is not the one who DECIDES.
# ⛔ A bare `verdict` in the record reads as THE verdict, and it is measurement
# alone: with the six dimensions undeclared it cannot be a closing verdict at
# all, and a script does not sign one.
def _bare_verdict():
    bid = block(p, "a", status="closed", extra=_KOK, record=False)
    open(os.path.join(BLOCKS, bid, "close.json"), "w", encoding="utf-8").write(
        '{"verdict": "PRODUCT", "dimensions": {"naming": "undeclared"}}')
    return bid


p.case("㊶ ⛔ a record whose verdict is not keyed to its layer",
       _bare_verdict, "QLT-LAY-003")


# ── BLK-CLS-008 · the close names the evidence LEVEL its lane requires ─────
# ⛔ "Tested" means whatever the last person had time for. ⭐ The lane is already
# MEASURED from the dependency graph, so the minimum is derived from it rather
# than being a second opinion.
def _lane_close(lane, level=""):
    """⚠️ The lane goes through the fixture's own parameter. ⛔ Substituting it
    into the text afterwards silently did nothing — the fixture already writes
    a `lane:` line — and the case then measured the DEFAULT lane while its
    label claimed another."""
    def go():
        # ⭐ The shared §K declares L3; these cases REPLACE that line, so
        # each one measures the level it names and nothing else.
        k = re.sub(r"evidence level: L\d\n",
                   ("evidence level: %s\n" % level) if level else "", _KOK)
        return block(p, "a", status="closed", lane=lane, extra=k)
    return go


p.case("㊷ ⛔ a full-block closing with no evidence level",
       _lane_close("full-block"), "BLK-CLS-008")

p.case("㊸ ⛔ a full-block claiming L1 · its dependents are unproven",
       _lane_close("full-block", "L1"), "BLK-CLS-008")

p.inverse("㊹ ⭐ the same block at L3 · the lane's minimum",
          _lane_close("full-block", "L3"))

# ⭐ A minimum, never a ceiling: above it is fine and says something real.
p.inverse("㊺ ⭐ L5 on a full-block · above the minimum",
          _lane_close("full-block", "L5"))

# ⛔ And `direct` does NOT inherit the strictest floor: nothing depends on it.
p.inverse("㊻ ⛔ `direct` at L1 · its own minimum, not full-block's",
          _lane_close("direct", "L1"))

# ── BLK-SUB-005 · at most three levels of nesting (ADR-015) ────────────────
# ⛔ The decision fixed three and only two were built, so large work arrived
# flat — measured at fourteen sub-blocks in one real block.
_ROW = "| %s | %s | bin/x | 0 | ok | ran it 2026-01-15 | closed |"


def _nest(*nums):
    def go():
        return _with_f(block(p, "a"),
                       "\n".join(_ROW % (n, "task " + n) for n in nums))
    return go


p.case("㊼ ⛔ a fourth level of nesting", _nest("2.1.1"), "BLK-SUB-005")

# ⭐ Three is a CEILING, not a shape: two levels stay the normal case.
p.inverse("㊽ ⭐ two levels · the normal case", _nest("1", "2"))
p.inverse("㊾ ⭐ a GROUP and its task · three levels", _nest("2", "2.1"))

# ⛔ And among rows, only the deep one is named.
p.case("㊿ ⛔ three rows, only the deep one is reported",
       _nest("1", "2.1", "3.1.1"), "BLK-SUB-005")

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
    print("     ⭐ by SHAPE (the detector cannot read them): %d %s"
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
