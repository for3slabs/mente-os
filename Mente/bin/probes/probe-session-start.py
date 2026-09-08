#!/usr/bin/env python3
"""probe-session-start — proves the startup hook obeys its two constraints.

⭐ A hook is not a validator: it has no findings of its own. What must be proven
is BEHAVIOUR — silent when healthy, loud when not, and never blocking.

⛔ The third case is the one that matters most: a hook that blocks the session
is removed within a week, and then the engine has neither the hook nor its rule.
"""
import glob, os, subprocess, sys, shutil
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
import plat                                          # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT, MARK                 # noqa: E402

HOOK = os.path.join(ROOT, "hooks", "session-start.sh")
results = []


# ⭐ plat.bash(), never the bare name. 🔴 Measured 2026-09-07 on a fresh
# Windows install: `bash` on PATH resolved to `C:\WINDOWS\system32\bash.exe`,
# the WSL launcher, which cannot open a `C:\...` path — every case that runs
# the hook died with exit 127 and this probe reported 2 of 10. ⛔ The engine
# had already solved this for the INSTALLER and not for the probe that checks
# it: the same fix, missing in the place that measures it.
# ⚠️ It returns an ARGV LIST, not a name — a Git-Bash launcher may need flags.
_SHELL = plat.bash()


def run(payload="", env=None):
    if not _SHELL:
        return None                      # ⬜ no usable shell · NOT MEASURED
    return subprocess.run(list(_SHELL) + [HOOK], cwd=ROOT, input=payload,
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
# ⭐ ORIENTATION IS NOT NOISE. 🔴 Measured 2026-09-07: an install succeeded and
# the assistant "did not recognise where it goes or how to start working" —
# ⛔ because a hook that only speaks in red says nothing on the healthy tree
# that is every ordinary session. These lines are the answer to that, so they
# are expected output, not a finding.
ORIENT = ("📦", "⬜ no piece of work open", "🧭")
noise, skip = [], False
for l in r.stdout.strip().split("\n"):
    if l.startswith("⚠️"):
        skip = "check-shipping" in l          # ⬜ not measurable without a repository
        continue
    if not l.strip() or "run-all" in l or l.lstrip().startswith(ORIENT):
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
_left = [l for l in r.stdout.strip().split("\n")
         if l.strip() and not l.lstrip().startswith(ORIENT)]
case("⑤ ⬜ a declared set replaces discovery",
     not _left and r.returncode == 0, "an absent validator is skipped")

# ⑥ ⭐ discovery is real: it must NOT name validators in its own source
src = open(HOOK, encoding="utf-8").read()
named = [n for n in ("check-document", "check-block", "check-config")
         if n in src]
case("⑥ ⭐ it discovers, it does not enumerate", not named,
     "0 validators named" if not named else "names: " + " ".join(named))

# ⑦ no payload → still works
r = run("")
case("⑦ no payload · it continues and does not break", r.returncode == 0, "exit=0")

# ── ⑧ 🔴 THE FIRST THING A SESSION SEES IS WHERE IT IS ─────────────────────
# 🔴 THE FAILURE, measured 2026-09-07 on a real Windows install. The owner:
# "it is installed, it uses it now and then, but it has not read how it must
# behave, where it goes, or how to start working." ⛔ This hook only ever spoke
# in red, so on the healthy tree — which is every ordinary session — it said
# NOTHING, and the assistant began with no idea whether work was open.
# ⭐ Orientation is not a warning. It is the one line that decides the first
# move, and it must print when everything is fine.
_ac = os.path.join(ROOT, "work", "blocks", "active")
_had = sorted(glob.glob(os.path.join(_ac, "*", "BLOCK.md")))
_tmp = os.path.join(_ac, MARK + "-orient")
try:
    r = run()
    if _had:
        case("⑧ 🔴 ⭐ with work open it says so, and to stay inside its §B",
             "📦" in r.stdout and "§B" in r.stdout,
             "%d open" % len(_had))
    else:
        case("⑧ 🔴 ⭐ with NO work open it says so, and that nothing may be written",
             "⬜ no piece of work open" in r.stdout
             and "nothing may be written" in r.stdout)
        # ⭐ And the other state is measured too, not assumed: a hook that is
        # right about one half is a hook half-measured.
        os.makedirs(_tmp, exist_ok=True)
        open(os.path.join(_tmp, "BLOCK.md"), "w", encoding="utf-8",
             newline="").write("# BLOCK\n\n## A · Identity\n\nid: x\n")
        r = run()
        case("⑧b 🔴 ⭐ and with one open it says to stay inside its §B",
             "📦" in r.stdout and "§B" in r.stdout,
             r.stdout.strip().split("\n")[-1][:40])
finally:
    if os.path.isdir(_tmp):
        plat.rmtree(_tmp)

# ⭐ AND IT POINTS AT THE BRIEF, when there is one. ⛔ A session that does not
# read where it left off starts by asking — measured as the most expensive
# opening there is.
_res = os.path.join(ROOT, "memory", "RESUME.md")
_born = not os.path.exists(_res)
try:
    if _born:
        # ⚠️ A VALID document, not a stub. 🔴 Caught while sabotage-testing this
        # case: an invalid one makes check-document complain by PATH, the string
        # "RESUME.md" lands in stdout from the validator, and the case passed
        # green with the hook's pointer deleted — it was measuring the
        # complaint, never the pointer.
        open(_res, "w", encoding="utf-8", newline="").write(
            "# RESUME\n\n**Status:** current · **Type:** memory · "
            "**Updated:** 2026-09-07 · **Owner:** probe\n\n## Purpose\n\n"
            "Fixture.\n")
    r = run()
    # ⭐ Anchored on the 🧭 the hook alone emits. ⛔ Matching the filename would
    # match any validator that happens to name the same path.
    case("⑨ ⭐ it points at the brief that says where we left off",
         any(l.lstrip().startswith("🧭") and "RESUME.md" in l
             for l in r.stdout.split("\n")),
         "🧭 line present")
finally:
    if _born and os.path.exists(_res):
        os.remove(_res)

good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("\n  leftovers: %s" % ("none" if not os.path.exists(broken) else broken))
sys.exit(0 if good == len(results) else 1)
