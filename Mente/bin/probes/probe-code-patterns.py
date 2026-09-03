#!/usr/bin/env python3
"""probe-code-patterns — proves each detector FIRES on the defect and stays silent on the fix.

⭐ THIS IS THE PAIR FROM THE CATALOGUE, APPLIED TO THE DETECTORS THEMSELVES. Every
pattern ships a failing example and a passing one; this runs both through the
detector and requires the first to fire and the second not to.

🔴 IT CAUGHT ONE ON ITS FIRST RUN. The unbounded-read pattern fired on
`select * from events limit 100` — the catalogue's own PASSING example. ⛔ A
detector that flags the correct shape scores perfectly and gets switched off,
taking the four that work with it.

⚠️ AND THE HONEST HALF IS TESTED TOO: five catalogued patterns are NOT text
detectable, and the tool names them every run. ⛔ Silence about them would let a
reader conclude the code is clean of patterns nothing looked for.
"""
import os, shutil, subprocess, sys, tempfile
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-cp-")
TOOL = os.path.join(ROOT, "bin", "check-code-patterns")

# ⭐ Taken from each pattern's own `Fails` / `Passes` in the catalogue.
PAIRS = {
    "FP-SEC-001": ("user = request.body.user_id\n",
                   "user = session.verified_user\n"),
    "FP-PERF-002": ("rows = db.query('select * from events')\n",
                    "rows = db.query('select * from events limit 100')\n"),
    "FP-SILENT-001": ("save(record)\n", "await save(record)\n"),
    "FP-SILENT-003": ("if now() > expiry:\n    pass\n",
                      "if deadline > expiry:\n    pass\n"),
    "FP-STATE-002": ("await save(x)\nawait load()\n",
                     "state = await save(x)\n"),
}


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def run(src=None, args=(), env=None):
    d = tempfile.mkdtemp(dir=WORK)
    if src is not None:
        open(os.path.join(d, "x.py"), "w", encoding="utf-8").write(src)
    return subprocess.run([sys.executable, TOOL, d] + list(args),
                          capture_output=True, text=True, timeout=60,
                          env=dict(os.environ, **(env or {})))


print("═══ PROBE · check-code-patterns ═══\n")

# ── ⭐ THE PAIR, per pattern · the second half is what keeps it usable ──────
for pid, (bad, good) in PAIRS.items():
    fires = pid in run(bad).stdout
    quiet = pid not in run(good).stdout
    case("⭐ %s · fires on the defect, silent on the fix" % pid,
         fires and quiet,
         "" if fires and quiet else
         ("does not fire" if not fires else "🔴 fires on correct code"))

# ── ⛔ WHAT NOTHING LOOKED FOR IS NAMED, EVERY RUN ──────────────────────────
r = run("x = 1\n")
for pid in ("FP-SEC-002", "FP-PERF-001", "FP-SILENT-002", "FP-STATE-001"):
    pass
case("⬜ the patterns it does NOT search are named",
     all(p in r.stdout for p in ("FP-SEC-002", "FP-PERF-001",
                                 "FP-SILENT-002", "FP-STATE-001")))
case("⭐ and FP-STRUCT-001 points at where it IS found",
     "grade-block" in r.stdout)

# ── ⚠️ A FINDING IS A QUESTION, NOT A VERDICT ──────────────────────────────
# ⛔ A text matcher that BLOCKED would be wrong often enough to be switched off
# within a week, and then the five it does find go unfound too.
r = run(PAIRS["FP-SEC-001"][0])
case("⚠️ a finding does NOT fail the run — it is a question",
     r.returncode == 0, "exit=%d" % r.returncode)
case("⭐ and the output says so, rather than leaving it to be assumed",
     "not verdicts" in r.stdout)

# ── ⬜ IT NEVER GUESSES WHERE THE CODE IS ───────────────────────────────────
# ⛔ A default of "here" would scan the engine's own validators and report it.
r = subprocess.run([sys.executable, TOOL], capture_output=True, text=True,
                   timeout=60, env=dict(os.environ, MENTE_CODE_DIRS=""))
case("⬜ no directory given → NOT MEASURED, it does not scan itself",
     "does not guess" in r.stdout and r.returncode == 0)

# ⭐ and the directory can be declared instead of passed
d = tempfile.mkdtemp(dir=WORK)
open(os.path.join(d, "x.py"), "w").write(PAIRS["FP-SEC-001"][0])
r = subprocess.run([sys.executable, TOOL], capture_output=True, text=True,
                   timeout=60, env=dict(os.environ, MENTE_CODE_DIRS=d))
case("⬜ MENTE_CODE_DIRS declares it", "FP-SEC-001" in r.stdout)

# ── ⬜ WHAT IT COULD NOT READ ───────────────────────────────────────────────
r = subprocess.run([sys.executable, TOOL, "/nowhere/at/all"],
                   capture_output=True, text=True, timeout=60)
case("⬜ a directory that does not exist → named, not skipped",
     "NOT MEASURED" in r.stdout)

# ── ⭐ CHK-QUI-001 ──────────────────────────────────────────────────────────
r = run(PAIRS["FP-SEC-001"][0], args=("--quiet",))
case("⭐ --quiet prints nothing", not r.stdout.strip())

# ── ⭐ THE EXTENSIONS COME FROM THE CONTRACT ────────────────────────────────
# ⛔ A list in the code and a table in the contract are two declarations that
# drift, and the contract is the one people edit.
d = tempfile.mkdtemp(dir=WORK)
open(os.path.join(d, "x.txt"), "w").write(PAIRS["FP-SEC-001"][0])
case("⭐ a file whose extension is not declared is not scanned",
     "FP-SEC-001" not in subprocess.run(
         [sys.executable, TOOL, d], capture_output=True, text=True,
         timeout=60).stdout)

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copy"))
sys.exit(0 if good == len(results) else 1)
