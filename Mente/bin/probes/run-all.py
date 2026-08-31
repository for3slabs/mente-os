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
    leftovers = "restos: ninguno" not in r.stdout
    if not m:
        # 🔴 A PROBE THAT NEVER REPORTED ITS TALLY DID NOT RUN — it crashed, or
        # it died before its last line. ⛔ Scored as (0, 0) this passed the
        # `good == all_` test and printed "0/0", which reads as "no cases" and
        # not as "it died"; worse, it contributed NOTHING to the total, so the
        # battery's headline number shrank silently while still saying 0 failed.
        # ⚠️ Found on a clean clone: a probe assumed an instance file existed.
        # ⭐ Counted as ONE failure so the total can never quietly shrink.
        crash = (r.stderr.strip().splitlines() or ["no output"])[-1]
        total += 1
        failed += 1
        rows.append((name, 0, 1, False, leftovers))
        print("  %-24s 🔴 CRASHED · %s" % (name, crash[:60]))
        continue
    good, all_ = int(m.group(1)), int(m.group(2))
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
# ⭐ Not every probe covers a VALIDATOR. A hook has no findings of its own —
# what its probe proves is BEHAVIOUR — so counting it against the validator
# total reported "15 validators, 16 probes" and read as an inconsistency.
# ⛔ A hook may be a script in any language — looking only for `.sh` counted a
# python hook's probe against the VALIDATOR total and reported an inconsistency
# that was the counter's, not the tree's.
HOOKS = os.path.join(os.path.dirname(BIN), "hooks")
hook_probes = [q for q in probes
               if any(os.path.exists(os.path.join(HOOKS,
                       os.path.basename(q)[len("probe-"):-3] + ext))
                      for ext in (".sh", ".py"))]
print("\n  ── cobertura")
print("     validadores: %d · con sonda: %d%s"
      % (len(checkers), len(probes) - len(hook_probes),
         " · + %d sonda(s) de hook" % len(hook_probes) if hook_probes else ""))
for c in missing:
    print("     ⬜ %s · NO PROBADO — un validador sin sonda no esta demostrado" % c)

print("\n  ➜ checks: %d · failed: %d%s"
      % (total, failed, "" if not failed else "  🔴"))
sys.exit(1 if failed or missing else 0)
