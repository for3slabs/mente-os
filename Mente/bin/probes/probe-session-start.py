#!/usr/bin/env python3
"""probe-session-start — proves the startup hook obeys its two constraints.

⭐ A hook is not a validator: it has no findings of its own. What must be proven
is BEHAVIOUR — silent when healthy, loud when not, and never blocking.

⛔ The third case is the one that matters most: a hook that blocks the session
is removed within a week, and then the engine has neither the hook nor its rule.
"""
import os, subprocess, sys, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT, MARK                 # noqa: E402

HOOK = os.path.join(ROOT, "hooks", "session-start.sh")
results = []


def run(payload="", env=None):
    return subprocess.run(["bash", HOOK], cwd=ROOT, input=payload,
                          capture_output=True, text=True,
                          env=dict(os.environ, **(env or {})))


def case(label, ok, detail=""):
    print("  %-48s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


print("═══ PROBE · session-start ═══\n")

# ① healthy tree → silence.
# ⚠️ An isolated copy has no `.git`, and SHP-BAS-001 then reports ⬜ NOT MEASURED
# — correctly, and loudly, because silence there would read as "the base is
# fine". ⭐ That is not noise: it is a real thing that cannot be measured, and
# the hook is right to surface it. The case asserts silence about everything
# ELSE, which is what "healthy" can mean in a tree without a repository.
r = run('{"session_id":"abc"}')
# ⛔ Filter by the BLOCK a validator emits, not by phrases: its summary line
# ("N violations · rule: …") carries neither the id nor the validator name, and
# a phrase filter kept letting it through as if it came from somewhere else.
noise, skip = [], False
for l in r.stdout.strip().split("\n"):
    if l.startswith("⚠️"):
        skip = "check-shipping" in l          # ⬜ not measurable without a repository
        continue
    if not l.strip() or "run-all" in l:
        continue
    if not skip:
        noise.append(l)
case("① a healthy tree · silence except what is NOT MEASURABLE", not noise,
     "no output" if not noise else noise[0][:44])

# ② a real defect → it speaks, naming the validator
broken = os.path.join(ROOT, "docs", MARK + "-broken.md")
try:
    open(broken, "w", encoding="utf-8").write("# broken\n\nnothing here\n")
    r = run()
    case("② a real defect · it speaks and names the validator",
         "check-document" in r.stdout, r.stdout.strip().split("\n")[0][:44])
finally:
    os.remove(broken)

# ③ ⛔ it must NEVER block — not even with a broken tree
case("③ never blocks · exit 0 with the tree broken", r.returncode == 0,
     "exit=%d" % r.returncode)

# ④ the heartbeat lands even if a validator crashes
beat = os.path.join(ROOT, ".heartbeat")
if os.path.exists(beat):
    os.remove(beat)
run()
case("④ the heartbeat is written", os.path.exists(beat),
     open(beat, encoding="utf-8").read().strip() if os.path.exists(beat) else "ausente")

# ⑤ ⬜ the declared set overrides discovery
r = run(env={"MENTE_STARTUP_CHECKS": "check-nonexistent"})
case("⑤ ⬜ a declared set replaces discovery",
     not r.stdout.strip() and r.returncode == 0, "an absent validator is skipped")

# ⑥ ⭐ discovery is real: it must NOT name validators in its own source
src = open(HOOK, encoding="utf-8").read()
named = [n for n in ("check-document", "check-block", "check-config")
         if n in src]
case("⑥ ⭐ it discovers, it does not enumerate", not named,
     "0 validators named" if not named else "names: " + " ".join(named))

# ⑦ no payload → still works
r = run("")
case("⑦ no payload · it continues and does not break", r.returncode == 0, "exit=0")

good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("\n  leftovers: %s" % ("none" if not os.path.exists(broken) else broken))
sys.exit(0 if good == len(results) else 1)
