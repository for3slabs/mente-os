#!/usr/bin/env python3
"""probe-watch-external — proves the watcher looks when it matters and stays quiet otherwise.

⭐ Two failures, opposite and both fatal: a watcher that never fires is blind,
and one that fires on every action becomes noise — ⛔ and noise is ignored,
which is how a validator dies. The truce is what separates them, so it is what
this probe measures hardest.
"""
import os, sys, json, subprocess

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
     "el aviso nombra el cambio")

# ③ ⛔ the truce: right after looking, a non-urgent action must NOT look again
r = run("ls -la", watch=CHANGED)
case("③ ⛔ the truce · an ordinary action does not look again",
     not r.stdout.strip(), "sin ruido")

# ④ ⭐ but an URGENT action ignores the truce
r = run("git commit -m x", watch=CHANGED)
case("④ ⭐ what is URGENT ignores the truce", "External state changed" in r.stdout,
     "el instante en que el aviso sirve")

# ⑤ nothing new → silence even when it looked
drop_stamp()
r = run("git push", watch=QUIET)
case("⑤ nothing changed · silence", not r.stdout.strip(), "exit 0 sin salida")

# ⑥ ⛔ a broken command is not a reason for noise
drop_stamp()
r = run("git push", watch="no-such-command-anywhere")
case("⑥ ⛔ a broken command · silence, not noise", not r.stdout.strip(),
     "sin red o sin la herramienta, calla")

# ⑦ ⛔ a malformed urgency pattern must not make everything urgent
drop_stamp()
r = run("ls", watch=CHANGED, env={"MENTE_WATCH_URGENT": "[unclosed"})
open(STAMP, "w").close()
r2 = run("ls", watch=CHANGED, env={"MENTE_WATCH_URGENT": "[unclosed"})
case("⑦ ⛔ a MALFORMED urgency pattern · it respects the truce",
     not r2.stdout.strip(), "no todo se vuelve urgente")

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
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("\n  leftovers: %s" % ("none" if not os.path.exists(STAMP) else "🔴 sello"))
sys.exit(0 if good == len(results) else 1)
