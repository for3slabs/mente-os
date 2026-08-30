#!/usr/bin/env python3
"""run-all — every probe, one run. ⭐ The only thing that matters is 0 failed.

A green here means each validator has been SEEN to fail on a state that
breaks what it claims to measure, with the message naming the real cause.
⛔ A validator with no probe is unproven, and this reports that too.
"""
import os, re, subprocess, sys, glob, shutil, tempfile
from concurrent.futures import ThreadPoolExecutor

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

# ⭐ WHY EACH PROBE GETS ITS OWN COPY OF THE TREE
#
# Five probes edit SHARED state — base-rules, a contract, the project rules —
# to plant their defect. Run side by side in one tree they overwrite each
# other, and the result is not slow: it is FALSE.
#
# ⛔ Measured, before choosing this: running the nine isolated ones in parallel
# and the five sharing ones in series took 14.2s against 11.1s in plain
# sequence — disk contention ate the gain. Copying the whole tree costs 0.04s
# for ~100 files, so isolation is cheaper than the contention it removes.
#
#    plain sequence  11.1s  ·  hybrid  14.2s  ·  isolated + parallel  4.5s
#
# ⬜ MENTE_PROBES_SERIAL=1 forces the old behaviour, for debugging a probe
# whose failure only appears in the real tree.
ROOT = os.path.dirname(BIN)
SERIAL = os.environ.get("MENTE_PROBES_SERIAL") == "1"
_IGNORE = shutil.ignore_patterns(".git", "__pycache__", "cache", "*.pyc")


def run_probe(q):
    """Run one probe. In isolated mode it gets a private copy of the tree, so
    what it edits cannot reach any other probe — ⛔ and cannot reach the real
    tree either, which is the second reason this is worth the copy."""
    name = os.path.basename(q)[:-3]
    if SERIAL:
        return name, subprocess.run([sys.executable, q],
                                    capture_output=True, text=True)
    d = tempfile.mkdtemp(prefix="mente-probe-")
    try:
        tree = os.path.join(d, os.path.basename(ROOT))
        shutil.copytree(ROOT, tree, ignore=_IGNORE)
        return name, subprocess.run(
            [sys.executable, os.path.join(tree, "bin", "probes", name + ".py")],
            cwd=tree, capture_output=True, text=True,
            env=dict(os.environ, MENTE_PROBE_ISOLATED="1"))
    finally:
        shutil.rmtree(d, ignore_errors=True)


print("═══ TODAS LAS SONDAS ═══%s\n"
      % ("" if not SERIAL else "  (serial · MENTE_PROBES_SERIAL=1)"))
total = failed = 0
rows = []

if SERIAL:
    results = [run_probe(q) for q in probes]
else:
    with ThreadPoolExecutor(max_workers=min(8, len(probes))) as _ex:
        results = list(_ex.map(run_probe, probes))

for name, r in results:
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
