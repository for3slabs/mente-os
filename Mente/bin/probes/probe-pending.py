#!/usr/bin/env python3
"""probe-pending — does check-pending detect what contract-pending.md claims?

⭐ The failure this contract measures is a list that LIES, so the probe plants
lists that look maintained and are not: closed with no date, dropped with no
reason, an item pointing at a previous period instead of being rewritten.
"""
import os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK

MEMORY = os.path.join(ROOT, "memory")
REF = os.environ.get("MENTE_CROSSRUN_PENDING", "")
p = Probe("check-pending", "PND")

# ⭐ THE FIXTURE DECLARES ITSELF SUPERSEDED, and that is not cosmetic.
# PND-CNV-002 counts LIVE pending lists across the whole tree — so a fixture
# claiming `current` is a genuine second live list the moment an installation
# has its own. 🔴 Measured on a freshly installed clone: every case inherited a
# CNV-002 finding that belonged to the fixture's own existence, and two correct
# cases read as false positives.
# ⛔ The rule is right; the fixture was lying about being live. Case ⑩, which
# exists to prove CNV-002 fires, restores `current` on both of its lists.
GOOD = """# Pending · a probe fixture

**Status:** superseded · **Type:** append-only · **Updated:** 2026-01-15 · **Owner:** x

## Purpose

A fixture used to prove the checker detects what it claims to.

## BLOCK · a theme

Plan: the whole block goes through one pass, smallest first.

### p-001 · the first item

- Priority: 🟠 medium
- State: open
- Created: 2026-01-10 · Updated: 2026-01-15 · Closed: —
- Carried from: — (born here)
- Reference files: somewhere/near/here
- Plan: — (small enough)
- Depends on: —

Description. Everything needed to resume this without asking anybody.

### p-002 · the second item

- Priority: 🟢 no rush
- State: closed
- Created: 2026-01-10 · Updated: 2026-01-15 · Closed: 2026-01-15
- Carried from: — (born here)
- Reference files: somewhere/else
- Plan: —
- Depends on: —

Description. It was resolved, and the evidence is the check that now passes.

Related: `README.md`.
"""


def put(text=GOOD, name=MARK + "-pending.md"):
    q = p.track(os.path.join(MEMORY, name))
    open(q, "w", encoding="utf-8").write(text)
    return q


print("═══ SABOTAGE · check-pending ═══\n")
p.baseline()

p.case("① an item with no block",
       lambda: put(GOOD.replace("## BLOCK · a theme\n\nPlan: the whole block "
                                "goes through one pass, smallest first.\n\n", "")),
       "PND-BLK-001")
p.case("② a block with no plan",
       lambda: put(GOOD.replace("Plan: the whole block goes through one pass, "
                                "smallest first.\n", "")
                       .replace("- Plan: — (small enough)\n", "")
                       .replace("- Plan: —\n", "")), "PND-BLK-002")
p.case("③ a field is missing",
       lambda: put(GOOD.replace("- Carried from: — (born here)\n", "", 1)),
       "PND-FLD-001")
p.case("④ an unknown state",
       lambda: put(GOOD.replace("- State: open", "- State: ongoing")),
       "PND-VRB-003")
p.case("⑤ closed with no closing date",
       lambda: put(GOOD.replace("- Created: 2026-01-10 · Updated: 2026-01-15 · Closed: 2026-01-15",
                                "- Created: 2026-01-10 · Updated: 2026-01-15 · Closed: —")),
       "PND-VRB-001")
p.case("⑥ dropped with no written reason",
       lambda: put(GOOD.replace("- State: closed", "- State: dropped")
                       .replace("Description. It was resolved, and the evidence "
                                "is the check that now passes.", "Description.")),
       "PND-VRB-002")
p.case("⑦ no real creation date",
       lambda: put(GOOD.replace("- Created: 2026-01-10 · Updated: 2026-01-15 · Closed: —",
                                "- Created: recently · Updated: 2026-01-15 · Closed: —")),
       "PND-FLD-002")
p.case("⑧ a carried-from that names no file",
       lambda: put(GOOD.replace("- Carried from: — (born here)",
                                "- Carried from: the last one", 1)),
       "PND-FLD-003")
p.case("⑨ an open item pointing at the previous period",
       lambda: put(GOOD.replace("Description. Everything needed to resume this "
                                "without asking anybody.",
                                "Description. See the previous period for detail.")),
       "PND-ROT-001")
LIVE = GOOD.replace("**Status:** superseded", "**Status:** current")
p.case("⑩ two live lists",
       lambda: (put(LIVE), put(LIVE, name=MARK + "-pending-two.md")),
       "PND-CNV-002")

p.case("⑪b ROT · a CLOSED item carried across periods",
       lambda: put(GOOD.replace("- State: open", "- State: closed")
                       .replace("- Carried from: — (born here)",
                                "- Carried from: the previous period")),
       "PND-ROT-002")

# ⭐ the inverse: a closed item that stayed where it died must not fire.
# ⛔ A closed item also needs its closing date — leaving it out planted a
# DIFFERENT defect and the inverse failed for a reason it was not testing.
p.inverse("⑪c ROT · a closed item that did NOT carry",
          lambda: put(GOOD.replace("- State: open", "- State: closed")
                          .replace("Closed: —", "Closed: 2026-01-16")))

p.inverse("⑪ a CORRECT list", lambda: put())
p.crash_guard()

print("\n═══ B · CROSS-RUN · una lista real de otra instancia ═══\n")
p.clean()
# ⭐ Only files that actually hold items: copying every .md in a folder plants
# documents that are not lists, and the run then measures nothing while
# reporting a count — a cross-run that says "4 files, 0 findings" when it
# planted no list is the emptiest kind of green.
real = [q for q in sorted(glob.glob(os.path.join(REF, "*.md")))] if REF else []
real = [q for q in real
        if re.search(r"^###\s+\S+\s*·", open(q, encoding="utf-8").read(), re.M)]
if real:
    for i, q in enumerate(real[:4]):
        put(open(q, encoding="utf-8").read(),
            "%s-x%02d-%s" % (MARK, i, os.path.basename(q)))
    code, out, err = p.run()
    mine = p._mine(out)
    by = {}
    for l in mine:
        for m in re.findall(r"PND-[A-Z]+-\d+", l):
            by[m] = by.get(m, 0) + 1
    print("  ⑫ %d listas reales · %d hallazgos" % (min(len(real), 4), len(mine)))
    for k in sorted(by):
        print("       %-14s %d" % (k, by[k]))
else:
    print("  ⑫ ⬜ NOT_MEASURED · set MENTE_CROSSRUN_PENDING to a real list folder")

sys.exit(0 if p.report() else 1)
