#!/usr/bin/env python3
"""probe-gates — proves the gate-liveness loop actually distinguishes the two silences.

⭐ THE WHOLE POINT OF THIS PAIR is that a gate is silent in two different states:
nothing to block, and not running. If check-gates cannot tell those apart it is
decoration — so the cases below attack exactly that boundary, from both sides.

⛔ AND THE SECOND FAILURE IS AS BAD AS THE FIRST. A reader that shouts whenever a
gate is quiet would fire after every holiday, and a validator that cries wolf is
switched off. Case ④ is the one that proves it stays quiet when it should.

⚠️ Runs against an ISOLATED COPY of the tree, never the working one: the subject
here is dated runtime state, and rewriting real stamps would leave the machine
reporting a gate silence that never happened.
"""
import os, sys, shutil, subprocess, tempfile
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-gates-")
TREE = os.path.join(WORK, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git"))


def case(label, ok, detail=""):
    print("  %-56s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def check(env=None):
    return subprocess.run([sys.executable, os.path.join(TREE, "bin", "check-gates")],
                          cwd=TREE, capture_output=True, text=True,
                          env=dict(os.environ, **(env or {})))


def stamp(name, days_ago):
    d = os.path.join(TREE, ".beats")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, name), "w") as fh:
        fh.write((date.today() - timedelta(days=days_ago)).isoformat())


def session(days_ago):
    with open(os.path.join(TREE, ".heartbeat"), "w") as fh:
        fh.write((date.today() - timedelta(days=days_ago)).isoformat())


def wipe():
    shutil.rmtree(os.path.join(TREE, ".beats"), ignore_errors=True)


print("═══ SONDA · _beat + check-gates ═══\n")

# ① ⭐ the helper records, and only once a day — the design that makes it affordable
sys.path.insert(0, os.path.join(TREE, "hooks"))
from _beat import beat, last, all_beats        # noqa: E402
wipe()
beat(TREE, "probe-x")
first = last(TREE, "probe-x")
beat(TREE, "probe-x")                      # second call must be a no-op read
n = len(os.listdir(os.path.join(TREE, ".beats")))
case("① ⭐ beat() stamps today · and does not duplicate on the 2nd call",
     first == date.today() and n == 1, "%s · %d archivo" % (first, n))

# ② ⛔ telemetry NEVER raises — a gate must fail for its own reasons, never for this
try:
    beat("/proc/impossible/nope", "x")
    last("/proc/impossible/nope", "x")
    all_beats("/proc/impossible/nope")
    ok = True
except Exception as e:                     # noqa: BLE001
    ok = False
case("② ⛔ never raises on an impossible path", ok)

# ③ ⭐ a real gate fires and leaves its proof — the loop end to end, not a stub
wipe()
subprocess.run([sys.executable, os.path.join(TREE, "hooks", "gate-critical.py")],
               cwd=TREE, input='{"tool_input":{"file_path":"a.md","content":"x"}}',
               capture_output=True, text=True)
real = os.path.exists(os.path.join(TREE, ".beats", "gate-critical"))
case("③ ⭐ firing gate-critical FOR REAL leaves its stamp", real)

# ④ ⚠️ THE CASE THAT KEEPS IT USABLE · a quiet gate over a quiet week is NOT a fault.
# Gates only fire while somebody works, so silence must be judged against the last
# LIVE session — never against today. Without this the reader nags after every break.
wipe()
stamp("gate-critical", 40)
stamp("pre-edit-standards", 40)
session(40)
r = check()
case("④ ⚠️ 40 days quiet BUT the session too → not a fault",
     r.returncode == 0 and "SILENT" not in r.stdout, "exit=%d" % r.returncode)

# ⑤ 🔴 THE DEFECT IT EXISTS FOR · quiet while the session was alive
wipe()
stamp("gate-critical", 30)
stamp("pre-edit-standards", 0)
session(0)
r = check()
case("⑤ 🔴 quiet 30 days across live sessions → detected",
     r.returncode == 1 and "gate-critical" in r.stdout, "exit=%d" % r.returncode)

# ⑥ ⭐ and it names the CAUSE, not just a red — a red without a cause is not a finding
case("⑥ ⭐ the message names the gate AND its file",
     "hooks/gate-critical.py" in r.stdout and "last fired" in r.stdout)

# ⑦ ⚠️ it must not blame the innocent one
case("⑦ ⚠️ it does not accuse the gate that DID fire",
     "pre-edit-standards" not in r.stdout.replace("2 gate", ""))

# ⑧ ⬜ no session date → NOT MEASURED, never a green. A pass with nothing to
# compare against is the exact report a fully unwired system would produce.
wipe()
stamp("gate-critical", 0)
os.remove(os.path.join(TREE, ".heartbeat"))
r = check()
case("⑧ ⬜ no .heartbeat → NOT MEASURED, not a ✅",
     r.returncode == 0 and "NOT MEASURED" in r.stdout and "✅" not in r.stdout)

# ⑨ ⬜ a gate that never fired is a GAP, not a failure — a fresh install is not broken
wipe()
session(0)
r = check()
case("⑨ ⬜ a gate that never fired → a gap (exit 0), not a fault",
     r.returncode == 0 and "never fired" in r.stdout, "exit=%d" % r.returncode)

# ⑩ ⭐ the roster is DISCOVERED · a gate added to hooks/ is watched with no edit here
wipe()
session(0)
extra = os.path.join(TREE, "hooks", "gate-zzprobe.py")
open(extra, "w").write(
    'import os,sys\n'
    'MENTE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n'
    'sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))\n'
    'from _beat import beat\n'
    'beat(MENTE,"gate-zzprobe")\n')
r = check()
case("⑩ ⭐ a NEW gate is watched without touching the reader",
     "gate-zzprobe" in r.stdout, "descubierta leyendo hooks/")
os.remove(extra)

# ⑪ ⬜ the threshold belongs to the installation, and changing it changes the verdict
wipe()
stamp("gate-critical", 10)
stamp("pre-edit-standards", 0)
session(0)
strict = check({"MENTE_GATE_SILENT_DAYS": "5"}).returncode
loose = check({"MENTE_GATE_SILENT_DAYS": "90"}).returncode
case("⑪ ⬜ the declared threshold changes the verdict (5→🔴 · 90→✅)",
     strict == 1 and loose == 0, "5:%d · 90:%d" % (strict, loose))

# ⑫ ⚠️ a malformed threshold must not disable the check — a typo is not a licence
wipe()
stamp("gate-critical", 30)
stamp("pre-edit-standards", 0)
session(0)
r = check({"MENTE_GATE_SILENT_DAYS": "not-a-number"})
case("⑫ ⚠️ a malformed threshold falls back, it does not disable the measurement",
     r.returncode == 1, "exit=%d" % r.returncode)

# ⑬ 🔴 an unreadable stamp is NOT proof of life — it must read as never-fired
wipe()
session(0)
os.makedirs(os.path.join(TREE, ".beats"), exist_ok=True)
open(os.path.join(TREE, ".beats", "gate-critical"), "w").write("garbage")
r = check()
case("⑬ 🔴 an unreadable stamp = never fired, not a ✅",
     "never fired" in r.stdout and "✅" not in r.stdout)

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
