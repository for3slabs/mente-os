#!/usr/bin/env python3
"""probe-adr-wiring — proves check-adr-wiring detects a consequence that resolves to nothing."""
import os, sys
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK          # noqa: E402

D = os.path.join(ROOT, "rules", "decisions")
p = Probe("check-adr-wiring", "DEC")

GOOD = """# 950 · A probe fixture decision

date: 2026-01-15
status: accepted
implementation: implemented
decided-by: x
supersedes: —
superseded-by: —
applies-to: the fixture
does-not-apply-to: everything else

## Context

A fixture used to prove the checker detects what it claims to.

## Decision

One thing.

## Rejected alternatives

- the other thing, which loses the graph

## Rationale

Because.

## Evidence

Measured once.

## Consequences

%(con)s

## What would change this decision

Nothing observed.

## Reverting

Undo it.
"""


def put(con):
    q = p.track(os.path.join(D, "950-" + MARK + ".md"))
    open(q, "w", encoding="utf-8").write(GOOD % {"con": con})


print("═══ SABOTAGE · check-adr-wiring ═══\n")
p.baseline()

p.case("① a consequence no rule declares",
       lambda: put("- `ZZZ-XXX-999` — a rule nobody wrote"), "DEC-CON-001")

p.case("② a cited artefact that does not exist",
       lambda: put("- `bin/no-such-tool` — a validator nobody built"), "DEC-CON-001")

# ⭐ Both inverses matter: the check must resolve REAL references silently, or
# every record with consequences becomes a finding and the check gets ignored.
p.inverse("③ a REAL rule id does not fire",
          lambda: put("- `DOC-SIZ-001` — a rule that exists"))
p.inverse("④ a REAL artefact does not fire",
          lambda: put("- `bin/check-document` — a validator that exists"))
p.inverse("⑤ no consequences section, nothing to resolve",
          lambda: put("—"))

p.crash_guard()
sys.exit(0 if p.report() else 1)
