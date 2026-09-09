#!/usr/bin/env python3
"""probe-gate-run — one interpreter per action, and the same verdicts.

🔴 WHY THIS EXISTS. Seven gates were wired as seven hook commands, so the host
started a fresh Python for each. Measured 2026-09-09 on a real Windows install:
one Bash command cost 2184 ms of gates, of which the work was ~50 ms per gate
and the rest was the interpreter booting. ⛔ The cost is per ACTION, so a long
session accumulates it — the owner reported it as "va aumentando".

⭐ THE RISK OF THE FIX IS THE WHOLE POINT OF THIS FILE. A dispatcher that is
fast and stops refusing is worse than the slowness it replaced, and it would
look identical from outside: green, quiet, quick.
"""
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
import plat                                          # noqa: E402
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                              # noqa: E402

HOOKS = os.path.join(ROOT, "hooks")
RUN = os.path.join(HOOKS, "gate-run.py")
WORK = tempfile.mkdtemp(prefix="mente-grun-")
results = []


def case(label, ok, detail=""):
    results.append((label, ok))
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))


def fire(args, payload, env=None):
    e = dict(os.environ)
    e.pop("MENTE_SCRATCH", None)
    if env:
        e.update(env)
    return subprocess.run([sys.executable, RUN] + args,
                          input=json.dumps(payload), capture_output=True,
                          text=True, timeout=90, env=e)


def one(gate, payload, env=None):
    e = dict(os.environ)
    e.pop("MENTE_SCRATCH", None)
    if env:
        e.update(env)
    return subprocess.run([sys.executable, os.path.join(HOOKS, gate + ".py")],
                          input=json.dumps(payload), capture_output=True,
                          text=True, timeout=90, env=e)


print("═══ PROBE · gate-run ═══\n")

_out = os.path.join(os.path.dirname(ROOT), "zzprobe-grun.md")
_write = {"tool_name": "Write",
          "tool_input": {"file_path": _out, "content": "x"}}
_cmd = {"tool_name": "Bash", "tool_input": {"command": "ls"}}
_leak = {"tool_name": "Write",
         "tool_input": {"file_path": _out,
                        "content": "api_key: 'sk-zzprobe123456789abc'"}}

# ── ① 🔴 THE VERDICT IS IDENTICAL, gate by gate ────────────────────────────
# ⛔ NOT "it still refuses sometimes". Every gate, alone and through the
# dispatcher, must answer the SAME exit code to the SAME payload — that is what
# makes this a wiring change and not a behaviour change.
_same = []
for _g, _p in (("gate-no-block", _write), ("gate-secrets", _leak),
               ("gate-critical", _cmd), ("gate-accounts", _cmd),
               ("watch-external", _cmd), ("pre-edit-standards", _write)):
    _a, _b = one(_g, _p).returncode, fire([_g], _p).returncode
    _same.append((_g, _a, _b))
_bad = [x for x in _same if x[1] != x[2]]
case("① 🔴 ⭐ every gate answers the SAME alone and dispatched",
     not _bad, "%d gate(s) compared" % len(_same) if not _bad
     else "🔴 %s: alone=%d run=%d" % _bad[0])

# ── ② ⛔ IT STILL REFUSES ──────────────────────────────────────────────────
case("② ⛔ work with no block open is still REFUSED",
     fire(["gate-no-block", "pre-edit-standards"], _write).returncode == 2)
case("②b ⛔ a credential is still REFUSED",
     fire(["gate-secrets"], _leak).returncode == 2)
case("②c ⭐ and an honest command still passes",
     fire(["gate-critical", "gate-accounts", "watch-external"],
          _cmd).returncode == 0)

# ── ③ 🔴 THE FIRST REFUSAL WINS, and the rest do not run ───────────────────
# ⛔ A gate that refused has decided. Running the others prints advice about
# work that is not going to happen, and the person reads a wall of text where
# one refusal belonged.
_r = fire(["gate-no-block", "pre-edit-standards"], _write)
_said = _r.stdout + _r.stderr
# ⛔ AND THE EXIT CODE CARRIES IT. 🔴 Caught by sabotage: dropping the `return
# rc` left the refusal PRINTED and the exit at 0 — the host reads the code, not
# the text, so the work went through while the screen said REFUSED. A gate that
# only narrates is a decoration, and this is the exact shape of that failure.
case("③ 🔴 ⭐ the FIRST refusal wins · the rest stay silent",
     "REFUSED" in _said and "📦" not in _said and _r.returncode == 2,
     "exit=%d" % _r.returncode if _r.returncode != 2
     else ("" if "📦" not in _said else "🔴 the second gate spoke too"))

# ── ④ 🔴 EACH GATE GETS ITS OWN stdin ──────────────────────────────────────
# ⛔ They call `json.load(sys.stdin)`. A stream the previous gate consumed
# answers nothing — and a gate that cannot read its payload ALLOWS. That is the
# failure mode of this design: silent, green, and total.
_r = fire(["gate-critical", "gate-accounts", "watch-external"], _cmd)
case("④ 🔴 ⭐ a later gate still receives the payload",
     _r.returncode == 0 and "could not run" not in (_r.stdout + _r.stderr),
     "3 gates, none starved")

# ⚠️ And proven the hard way: a gate that WOULD refuse, placed LAST.
_r = fire(["gate-critical", "gate-accounts", "gate-no-block"], _write)
case("④b 🔴 ⭐ the LAST gate can still refuse — it was not starved",
     _r.returncode == 2, "exit=%d" % _r.returncode)

# ── ⑤ ⛔ A CRASH DOES NOT TAKE THE WORK WITH IT — except where it must ─────
# ADR-012: a guard that dies must not lock the person out of their machine.
# ⛔ gate-secrets is the declared exception: its worst case is a credential on
# disk, and that is not revertible.
_broken = os.path.join(HOOKS, "zzprobe-broken.py")
open(_broken, "w", encoding="utf-8", newline="").write(
    "def main():\n    raise RuntimeError('boom')\n")
try:
    _r = fire(["zzprobe-broken"], _cmd)
    case("⑤ ⛔ a crashing gate does NOT block the work (ADR-012)",
         _r.returncode == 0 and "NOT MEASURED" in (_r.stdout + _r.stderr),
         "exit=%d" % _r.returncode)
    # ⛔ AND THE CRASH IS SAID. A gate that dies silently is a gate nobody
    # knows stopped working — the failure the whole heartbeat exists to end.
    case("⑤b ⬜ and the crash is SAID, never swallowed",
         "zzprobe-broken" in (_r.stdout + _r.stderr))
finally:
    os.remove(_broken)

# ⛔ gate-secrets fails CLOSED, and the dispatcher must honour that.
_sec = os.path.join(HOOKS, "zzprobe-secrets-like.py")
case("⑤c ⛔ gate-secrets is named as failing CLOSED",
     "FAILS_CLOSED" in open(RUN, encoding="utf-8").read()
     and '"gate-secrets"' in open(RUN, encoding="utf-8").read())

# ── ⑥ ⭐ THE BEATS STILL LAND · check-gates depends on them ────────────────
# ⛔ A gate that stops leaving its beat reads as DEAD to check-gates, and the
# dispatcher would have silently unwired the audit while speeding it up.
_beats = os.path.join(ROOT, ".beats")
_before = set(os.listdir(_beats)) if os.path.isdir(_beats) else set()
fire(["gate-critical", "gate-accounts", "watch-external"], _cmd)
_after = set(os.listdir(_beats)) if os.path.isdir(_beats) else set()
case("⑥ 🔴 ⭐ every dispatched gate still leaves its beat",
     {"gate-critical", "gate-accounts", "watch-external"} <= _after,
     "%d beat(s)" % len(_after))

# ── ⑦ ⬜ AN UNKNOWN GATE IS SAID, never a silent pass ──────────────────────
_r = fire(["zzprobe-nonexistent"], _cmd)
case("⑦ ⬜ a gate that is not there is NAMED, not skipped",
     _r.returncode == 0 and "NOT MEASURED" in (_r.stdout + _r.stderr))

# ── ⑧ ⚡ AND IT IS ACTUALLY FASTER — the reason it exists ──────────────────
# ⚠️ Measured as a RATIO, never against a fixed millisecond count: a threshold
# in ms is a probe that fails on a slow machine and passes on a fast one.
import time                                           # noqa: E402
_t0 = time.time()
for _g in ("gate-critical", "gate-accounts", "watch-external"):
    one(_g, _cmd)
_apart = time.time() - _t0
_t0 = time.time()
fire(["gate-critical", "gate-accounts", "watch-external"], _cmd)
_together = time.time() - _t0
case("⑧ ⚡ ⭐ three gates in one interpreter beat three processes",
     _together < _apart,
     "%.0f ms → %.0f ms (%.0f%% less)"
     % (_apart * 1000, _together * 1000,
        100 - _together * 100 / max(_apart, 1e-9)))

# ── ⑨ ⛔ AND THE WIRING USES IT — a dispatcher nothing calls saves nothing ─
_tpl = open(os.path.join(ROOT, "templates",
                         "claude-settings.json.template"),
            encoding="utf-8").read()
case("⑨ ⛔ the shipped wiring actually calls gate-run",
     _tpl.count("gate-run.py") >= 3,
     "%d matcher(s) dispatched" % _tpl.count("gate-run.py"))

plat.rmtree(WORK)
if os.path.exists(_out):
    os.remove(_out)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copy"))
sys.exit(0 if good == len(results) else 1)
