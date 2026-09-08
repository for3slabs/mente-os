#!/usr/bin/env python3
"""probe-decisions — does check-decisions detect what contract-adr.md claims?"""
import os, sys, re, glob
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import rewrite, Probe, ROOT, MARK

D = os.path.join(ROOT, "rules", "decisions")
p = Probe("check-decisions", "DEC",
          # ⭐ the folder README too: DEC-NUM-005 is reported against IT, not
          # against a fixture, so without this the finding is filtered away.
          also=("decisions/README.md",))

# ⭐ Fixtures number from 900 up: the engine now ships records of its own, and
# 001 collided with a REAL one. The collision was correctly reported — ⛔ but it
# was the probe reusing a number, not the checker misbehaving.
GOOD = """# 901 · Keep one decision in one file

date: 2026-01-15
status: accepted
implementation: verified
decided-by: the owner
supersedes: —
superseded-by: —
applies-to: every decision record in this installation
does-not-apply-to: decisions local to a single open block

## Context

Records kept as table rows ended up in two tables, and the two diverged.

## Decision

One decision is one file.

## Rejected alternatives

- a single shared table, which cannot carry evidence or a way back
- an append-only log, which cannot be superseded

## Rationale

A file carries its evidence, its boundary and its exit; a row carries none.

## Evidence

Two tables of the same decisions, with different row counts.

## Consequences

Every record is a file under this folder, and the index is generated from them.

## Reverting

Merge the files back into a table, losing evidence and reverting fields.
"""


def put(text, name="901-" + MARK + ".md"):
    q = p.track(os.path.join(D, name))
    open(q, "w", encoding="utf-8").write(text)
    return q


print("═══ SABOTAGE · check-decisions ═══\n")
p.baseline()

p.case("① a header field is missing",
       lambda: put(GOOD.replace("decided-by: the owner\n", "")), "DEC-FLD-001")
p.case("② a non-ISO date", lambda: put(GOOD.replace("2026-01-15", "15 Jan 2026")),
       "DEC-FLD-001")
p.case("③ an invalid status",
       lambda: put(GOOD.replace("status: accepted", "status: agreed")), "DEC-FLD-002")
p.case("④ a section is missing",
       lambda: put(re.sub(r"## Reverting\n.*", "", GOOD, flags=re.S)), "DEC-FLD-003")
p.case("⑤ an empty Evidence",
       lambda: put(re.sub(r"## Evidence\n\n.*?\n\n", "## Evidence\n\n\n", GOOD, flags=re.S)),
       "DEC-FLD-004")
p.case("⑥ a name with no number", lambda: put(GOOD, MARK + "-thing.md"), "DEC-NUM-001")
p.case("⑦ a reused number",
       lambda: (put(GOOD, "901-" + MARK + "-a.md"), put(GOOD, "901-" + MARK + "-b.md")),
       "DEC-NUM-002")
p.case("⑧ a one-sided supersede link",
       lambda: (put(GOOD.replace("superseded-by: —", "superseded-by: 902"),
                    "901-" + MARK + "-a.md"),
                put(GOOD.replace("# 901 ·", "# 902 ·")
                    .replace("applies-to: every decision record in this installation",
                             "applies-to: a different subject entirely"),
                    "902-" + MARK + "-b.md")),
       "DEC-SUP-001")
p.case("⑨ supersedes a record that does not exist",
       lambda: put(GOOD.replace("supersedes: —", "supersedes: 099"),
                   "901-" + MARK + "-a.md"), "DEC-SUP-002")
p.case("⑩ superseded but status accepted",
       lambda: (put(GOOD.replace("superseded-by: —", "superseded-by: 902"),
                    "901-" + MARK + "-a.md"),
                put(GOOD.replace("# 901 ·", "# 902 ·")
                    .replace("applies-to: every decision record in this installation",
                             "applies-to: a different subject entirely")
                    .replace("supersedes: —",
                                                               "supersedes: 901"),
                    "902-" + MARK + "-b.md")), "DEC-SUP-003")

# ── the 5 new rules
p.case("⑪ no implementation state",
       lambda: put(GOOD.replace("implementation: verified\n", "")), "DEC-IMP-001")
p.case("⑫ an unknown implementation state",
       lambda: put(GOOD.replace("implementation: verified", "implementation: done")),
       "DEC-IMP-001")
p.case("⑬ accepted long ago and never started",
       lambda: put(GOOD.replace("implementation: verified",
                                "implementation: not-started")), "DEC-IMP-003")
p.case("⑭ supersedes without saying why",
       lambda: put(GOOD.replace("supersedes: —", "supersedes: 099")), "DEC-FLD-006")
p.case("⑮ it never declares where it applies",
       lambda: put(re.sub(r"applies-to: .*\n", "", GOOD)), "DEC-FLD-007")
p.case("⑯ rejected alternatives left unnamed",
       lambda: put(re.sub(r"## Rejected alternatives\n\n.*?\n\n",
                          "## Rejected alternatives\n\nwe looked at some others\n\n",
                          GOOD, flags=re.S)), "DEC-FLD-005")

p.case("⑰b ONE · the decision is a TABLE of rows",
       lambda: put(GOOD.replace(
           "One decision is one file.",
           "| # | choice |\n|---|---|\n| 1 | this |\n| 2 | that |\n| 3 | other |")),
       "DEC-ONE-001")

p.case("⑰c NUM · reverted without saying why",
       lambda: put(GOOD.replace("status: accepted", "status: reverted")
                       .replace("## Rationale\n\nA file carries its evidence, "
                                "its boundary and its exit; a row carries none.\n", "")),
       "DEC-NUM-003")

p.case("⑰d SRC · two standing records on the same subject",
       lambda: (put(GOOD),
                put(GOOD.replace("# 901 ·", "# 902 ·"), "902-" + MARK + ".md")),
       "DEC-SRC-003")

p.case("⑰e NUM · the filename names who decided",
       lambda: put(GOOD.replace("decided-by: the owner", "decided-by: alexandra"),
                   "903-" + MARK + "-alexandra-decides.md"), "DEC-NUM-004")

# ⭐ the inverse: the same owner, a filename that names the DECISION — must not fire.
p.inverse("⑰f NUM · the same owner, a name describing the decision",
          lambda: put(GOOD.replace("decided-by: the owner", "decided-by: alexandra"),
                      "904-" + MARK + "-one-file-per-record.md"))

p.case("⑰g SUP · it cites in prose an ADR that does not exist",
       lambda: put(GOOD.replace("## Rationale",
                                "## Consequences\n\n- `ADR-777` — something\n\n## Rationale")),
       "DEC-SUP-004")

# ⭐ the inverse: the same citation marked ⬜ planned must NOT fire.
p.inverse("⑰h SUP · the same citation, marked ⬜ planned",
          lambda: put(GOOD.replace("## Rationale",
                                   "## Consequences\n\n- ⬜ `ADR-777` (planned) — something\n\n## Rationale")))

p.inverse("⑰ a CORRECT record", lambda: put(GOOD))
p.crash_guard()

# ── B · CORRIDA CRUZADA
# ⛔ This said "another instance's decisions are not comparable — their records
# are theirs". That was an excuse, not a reason: what is theirs is the CONTENT;
# the SHAPE is exactly what this contract fixes, and 30 real records carry it.
# A cross-run declined on a made-up reason is the emptiest NOT_MEASURED there is.
print("\n═══ B · CROSS-RUN · registros reales de otra instancia ═══\n")
p.clean()
REF = os.environ.get("MENTE_CROSSRUN_DECISIONS", "")
real = sorted(glob.glob(os.path.join(REF, "*.md"))) if REF else []
real = [q for q in real if not os.path.basename(q).upper().startswith("README")]
if real:
    for i, q in enumerate(real[:8]):
        put(open(q, encoding="utf-8").read(),
            "%03d-%s-x.md" % (900 + i, MARK))
    code, out, err = p.run()
    mine = [l for l in out.splitlines() if MARK in l]
    by = {}
    for l in mine:
        for m in re.findall(r"DEC-[A-Z]+-\d+", l):
            by[m] = by.get(m, 0) + 1
    print("  ⑱ %d registros REALES · %d hallazgos" % (min(len(real), 8), len(mine)))
    for k in sorted(by):
        print("       %-14s %d" % (k, by[k]))
    for l in mine[:4]:
        print("     " + l.split(" · ", 2)[-1][:94])
else:
    print("  ⬜ NOT_MEASURED · set MENTE_CROSSRUN_DECISIONS to a real decisions/ folder")
# ── 🔴 DEC-NUM-005 · A GAP IN THE SEQUENCE IS DECLARED ────────────────────
# 🔴 THE FAILURE, measured 2026-09-08 while auditing rules/ one file at a time.
# Six numbers were absent from the sequence, and this folder's own README says a
# record is NEVER deleted. ⛔ So either the rule had been broken or those
# numbers were never used — and from outside the two read identically. ⚠️ A
# reader who finds a gap starts looking for a file that may not exist.
# ⭐ The gap is fine. An UNDECLARED gap is the defect.
_readme = os.path.join(D, "README.md")
_keep = open(_readme, encoding="utf-8").read()


def _hide_a_gap():
    """⚠️ Sabotaged by REMOVING a declaration, never by deleting a record: the
    rule is about what the README says, and deleting an ADR would be testing
    the append-only rule instead.

    ⛔ NOT tracked: `track()` DELETES, and this README belongs to the engine.
    The harness refuses it, correctly — it is restored below instead."""
    rewrite(_readme, re.sub(r"`016`\s*", "", _keep, count=1))


if "`016`" in _keep:
    p.case("⑲ 🔴 ⭐ an UNDECLARED gap in the numbering is caught",
           _hide_a_gap, "DEC-NUM-005")
    rewrite(_readme, _keep)
else:
    # ⬜ CHK-CAU-003 · said out loud, never a silent skip.
    print("  ⬜ ⑲ NOT MEASURED · the README declares no gap to remove")

p.clean()
sys.exit(0 if p.report() else 1)
