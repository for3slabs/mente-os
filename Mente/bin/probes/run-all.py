#!/usr/bin/env python3
"""run-all — every probe, one run. ⭐ The only thing that matters is 0 failed.

A green here means each validator has been SEEN to fail on a state that
breaks what it claims to measure, with the message naming the real cause.
⛔ A validator with no probe is unproven, and this reports that too.
"""
import os, re, subprocess, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.dirname(HERE)

probes = sorted(glob.glob(os.path.join(HERE, "probe-*.py")))
# ⛔ Not every validator is named `check-*`. Filtering on that prefix left
# `grade-block` out of the count, so coverage read "13 validators, 14 probes" —
# a filter narrower than what exists, which reports a covered tree as
# inconsistent and an uncovered one as complete.
VALIDATORS = ("check-", "grade-")
checkers = sorted(f for f in os.listdir(BIN)
                  if f.startswith(VALIDATORS) and os.path.isfile(os.path.join(BIN, f)))

print("═══ TODAS LAS SONDAS ═══\n")
total = failed = 0
rows = []
for q in probes:
    name = os.path.basename(q)[:-3]
    r = subprocess.run([sys.executable, q], capture_output=True, text=True)
    m = re.search(r"➜ (\d+) de (\d+) correctos", r.stdout)
    good, all_ = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    leftovers = "restos: ninguno" not in r.stdout
    ok = r.returncode == 0 and good == all_ and not leftovers
    total += all_
    failed += all_ - good
    rows.append((name, good, all_, ok, leftovers))
    print("  %-24s %s %s/%s%s" % (name, "✅" if ok else "🔴", good, all_,
                                  "  ⚠️ deja restos" if leftovers else ""))

covered = {os.path.basename(q)[len("probe-"):-3] for q in probes}


def stem(c):
    """The probe name a validator maps to. ⛔ `grade-block` is probed by
    `probe-grade`: the mapping is per validator, never a blind prefix strip."""
    return {"grade-block": "grade"}.get(c, c[len("check-"):])


missing = [c for c in checkers
           if stem(c) not in covered and stem(c) != "s"]
print("\n  ── cobertura")
print("     validadores: %d · con sonda: %d" % (len(checkers), len(probes)))
for c in missing:
    print("     ⬜ %s · NO PROBADO — un validador sin sonda no esta demostrado" % c)

print("\n  ➜ checks: %d · failed: %d%s"
      % (total, failed, "" if not failed else "  🔴"))
sys.exit(1 if failed or missing else 0)
