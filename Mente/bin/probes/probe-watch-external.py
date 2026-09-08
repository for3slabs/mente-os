#!/usr/bin/env python3
"""probe-watch-external — proves the watcher looks when it matters and stays quiet otherwise.

⭐ Two failures, opposite and both fatal: a watcher that never fires is blind,
and one that fires on every action becomes noise — ⛔ and noise is ignored,
which is how a validator dies. The truce is what separates them, so it is what
this probe measures hardest.
"""
import os
import re, sys, json, subprocess
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

HOOK = os.path.join(ROOT, "hooks", "watch-external.py")
STAMP = os.path.join(ROOT, "cache", "watch-external.stamp")
results = []

CHANGED = "printf 'a review merged\\n'; exit 1"     # ⬜ something happened
QUIET = "exit 0"                                    # ⬜ nothing new


def run(cmd_field="", watch=None, env=None):
    e = {"MENTE_WATCH_COMMAND": watch} if watch is not None else {}
    e.update(env or {})
    payload = json.dumps({"tool_input": {"command": cmd_field}})
    return subprocess.run([sys.executable, HOOK], cwd=ROOT, input=payload,
                          capture_output=True, text=True,
                          env=dict(os.environ, **e))


def drop_stamp():
    if os.path.exists(STAMP):
        os.remove(STAMP)


def case(label, ok, detail=""):
    print("  %-54s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


print("═══ SONDA · watch-external ═══\n")

# ① ⬜ nothing declared → nothing watched, and no noise
drop_stamp()
r = run("git push", watch="")
case("① ⬜ no command declared · silence", not r.stdout.strip(),
     "it does not guess what to watch")

# ② urgent action → it looks, and reports what changed
drop_stamp()
r = run("git push origin main", watch=CHANGED)
case("② ⭐ an URGENT action · it looks and says WHAT changed",
     "External state changed" in r.stdout and "merged" in r.stdout,
     "the notice names the change")

# ③ ⛔ the truce: right after looking, a non-urgent action must NOT look again
r = run("ls -la", watch=CHANGED)
case("③ ⛔ the truce · an ordinary action does not look again",
     not r.stdout.strip(), "sin ruido")

# ④ ⭐ but an URGENT action ignores the truce
r = run("git commit -m x", watch=CHANGED)
case("④ ⭐ what is URGENT ignores the truce", "External state changed" in r.stdout,
     "the instant the notice is worth anything")

# ⑤ nothing new → silence even when it looked
drop_stamp()
r = run("git push", watch=QUIET)
case("⑤ nothing changed · silence", not r.stdout.strip(), "exit 0 sin salida")

# ⑥ ⛔ a broken command is not a reason for noise
drop_stamp()
r = run("git push", watch="no-such-command-anywhere")
case("⑥ ⛔ a broken command · silence, not noise", not r.stdout.strip(),
     "with no network or no tool, it stays quiet")

# ⑦ ⛔ a malformed urgency pattern must not make everything urgent
drop_stamp()
r = run("ls", watch=CHANGED, env={"MENTE_WATCH_URGENT": "[unclosed"})
open(STAMP, "w").close()
r2 = run("ls", watch=CHANGED, env={"MENTE_WATCH_URGENT": "[unclosed"})
case("⑦ ⛔ a MALFORMED urgency pattern · it respects the truce",
     not r2.stdout.strip(), "not everything becomes urgent")

# ⑧ 🔴 never blocks, whatever arrives
for label, raw in (("payload roto", "{not json"), ("array", "[]"), ("null", "null")):
    p = subprocess.run([sys.executable, HOOK], cwd=ROOT, input=raw,
                       capture_output=True, text=True,
                       env=dict(os.environ, MENTE_WATCH_COMMAND=CHANGED))
    if p.returncode != 0:
        case("⑧ 🔴 never blocks · %s" % label, False, "exit=%d" % p.returncode)
        break
else:
    case("⑧ 🔴 never blocks on 3 invalid payloads", True, "exit=0 en los tres")

# ⑨ ⭐ it informs, never denies — the decision field must say allow
drop_stamp()
r = run("git push", watch=CHANGED)
try:
    decision = json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"]
except Exception:
    decision = "?"
case("⑨ ⭐ it informs · permissionDecision = allow", decision == "allow", decision)

drop_stamp()
# ── ⑩ 🔴 A WIRED HOOK THAT LEAVES NO TRACE CANNOT BE AUDITED ──────────────
# 🔴 THE FAILURE, measured 2026-09-08 while auditing hooks/ one file at a time.
# This hook was wired in the shipped settings, ran on every Bash call, and left
# NOTHING behind. ⛔ `check-gates` discovers what to audit by asking "does it
# call beat()" — so a hook that never calls it is not a gate, and its silence
# is therefore never noticed. A circular definition: invisible because silent,
# silent because invisible. If it died tomorrow nothing would say so, and that
# is the exact shape of the failure that killed five gates on a real install.
# ⚠️ IT IS STILL AN OBSERVER. The beat proves it RAN; it does not make it
# block, and ⑧ above still holds it to exit 0 on every payload.
# ⚠️ A CALL, not a mention. 🔴 Caught while sabotage-testing this very case:
# the first version asked `"beat(" in src`, and the COMMENT above the call says
# the words `call beat()` — so deleting the call left the case green. ⛔ It
# measured its own prose. ⭐ Same shape `check-gates` uses to discover a gate:
# the name at the start of a line, which a comment never is.
_src = open(HOOK, encoding="utf-8").read()
_calls = re.findall(r"(?m)^\s*beat\s*\(", _src)
case("⑩ 🔴 ⭐ it leaves a beat, so check-gates can audit it at all",
     bool(_calls) and "from _beat import" in _src,
     "%d call(s)" % len(_calls))

# ⭐ AND THE BEAT IS FIRST, before any early return. ⛔ There are six of them;
# a beat at the end would only prove the paths that reach the end — and the
# common path (nothing declared to watch) returns on the first line.
# ⚠️ Also matched as a CALL, for the same reason.
_m = _src[_src.index("def main():"):]
_first = re.search(r"(?m)^\s*beat\s*\(", _m)
_ret = re.search(r"(?m)^\s*return 0", _m)
case("⑩b ⛔ and it beats BEFORE the early returns, not after",
     bool(_first) and bool(_ret) and _first.start() < _ret.start(),
     "beat@%s return@%s" % (_first.start() if _first else "—",
                            _ret.start() if _ret else "—"))

good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("\n  leftovers: %s" % ("none" if not os.path.exists(STAMP) else "🔴 sello"))
sys.exit(0 if good == len(results) else 1)
