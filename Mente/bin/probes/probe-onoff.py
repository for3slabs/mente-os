#!/usr/bin/env python3
"""probe-onoff — proves the pause switch is real, not a label.

🔴 THE FAILURE THIS EXISTS FOR, measured 2026-09-06. A person asked whether the
system was on and how to stop it, and neither question had an answer: the
install reported once and nothing answered afterwards. ⛔ Three commands were
added — and the dangerous outcome was never the missing command. It was a
switch the gates do not read: `bin/off` prints "paused", the hooks keep firing,
and the owner is told something untrue about their own machine.

⭐ SO THE CASES THAT MATTER RUN THE REAL HOOKS. Not a claim about the marker —
the actual scripts, with the marker in place, checked for whether they went
quiet. ⚠️ A probe that asserts `.off` exists measures the writer, not the
switch.
"""
import os, sys, subprocess
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
import plat                                          # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                              # noqa: E402

BIN = os.path.join(ROOT, "bin")
HOOKS = os.path.join(ROOT, "hooks")
OFF = os.path.join(ROOT, ".off")
CONFIG = os.path.join(ROOT, "mente.config.yml")
results = []


def case(label, ok, detail=""):
    results.append((label, ok))
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60, **kw)


def out(r):
    return (r.stdout + r.stderr).lower()


# ── ① THE THREE COMMANDS SHIP AND RUN ──────────────────────────────────────
for _i, n in zip("abc", ("status", "off", "on")):
    # ⚠️ One label per case, even inside a loop — the battery refuses a repeat,
    # and a duplicated label hides whichever of them failed.
    case("①%s bin/%s ships" % ("" if _i == "a" else _i, n),
         os.path.isfile(os.path.join(BIN, n)))

# ── ② A CLONE THAT WAS NEVER SET UP SAYS SO ────────────────────────────────
# ⭐ The honest answer on a fresh clone, and the one the engine ships in.
# ⛔ Neither command may pretend: `off` writing a marker here produced a state
# `on` refused to clear — measured while building them.
_had = os.path.isfile(CONFIG)
if not _had:
    r = run([sys.executable, os.path.join(BIN, "status")])
    case("② a clone that is not set up says so, exit 1",
         r.returncode == 1 and "not set up" in out(r), "exit=%d" % r.returncode)
    r = run([sys.executable, os.path.join(BIN, "off")])
    case("②b 🔴 ⭐ off REFUSES where there is nothing to pause",
         r.returncode == 1 and not os.path.exists(OFF), "exit=%d" % r.returncode)
    r = run([sys.executable, os.path.join(BIN, "on")])
    case("②c and on refuses too — the pair cannot trap you",
         r.returncode == 1, "exit=%d" % r.returncode)
else:
    # ⬜ CHK-CAU-003 · said out loud, never swallowed.
    print("  ⬜ ②-②c NOT MEASURED · this tree is already set up")

# ── ③ THE ROUND TRIP, OVER A TREE THAT IS SET UP ───────────────────────────
# ⚠️ The config is created for the duration and removed after — ⭐ the probe
# leaves the tree exactly as it found it, or the next probe measures its mess.
_made = False
if not _had:
    open(CONFIG, "w", encoding="utf-8").write("# probe-onoff · temporary\n")
    _made = True
try:
    r = run([sys.executable, os.path.join(BIN, "off")])
    case("③ off pauses, and says nothing was deleted",
         r.returncode == 0 and os.path.exists(OFF)
         and "nothing was deleted" in out(r), "exit=%d" % r.returncode)

    r = run([sys.executable, os.path.join(BIN, "status")])
    case("③b status then reports PAUSED", "paused" in out(r))

    # 🔴 MEASURED FROM THE OUTPUT, NOT THE SOURCE. Found while writing this:
    # the isolation sentence is built from two adjacent string literals, so it
    # never appears whole in the file — ⛔ a probe reading the source called a
    # shipped promise missing. ⚠️ And it is asserted HERE, inside the set-up
    # tree: on a bare clone the line is never reached, and a case that passes
    # by not running measures nothing.
    r = run([sys.executable, os.path.join(BIN, "on")])
    r = run([sys.executable, os.path.join(BIN, "status")])
    _said = " ".join(out(r).split())
    case("③c ⭐ status says where it lives, and that others are separate",
         "lives in this folder" in _said
         and "neither knows the other exists" in _said)
    run([sys.executable, os.path.join(BIN, "off")])

    # ── ④ 🔴 THE CASE THAT MATTERS · the GATES read it ─────────────────────
    # ⛔ Everything above measures the writer. This runs the real hooks with
    # the marker in place: a switch the gates ignore is a lie told to the
    # owner about their own machine.
    r = run(["bash", os.path.join(HOOKS, "session-start.sh")],
            input="", env=dict(os.environ, MENTE_STARTUP_CHECKS=""))
    case("④ 🔴 ⭐ the session hook goes SILENT while paused",
         r.returncode == 0 and out(r).strip() == "", "%d byte(s)" % len(out(r)))

    # 🔴 FOUND BY SABOTAGING THIS CASE: with no accounts registry the hook
    # exits 0 for every destination, so removing the switch entirely left the
    # case green. ⛔ A case that passes against broken code measures nothing.
    # ⭐ A registry is supplied for the duration, which is what makes the hook
    # able to refuse — and therefore able to prove the pause is what stopped it.
    _reg = os.path.join(ROOT, "accounts.tsv")
    _had_reg = os.path.isfile(_reg)
    if not _had_reg:
        open(_reg, "w", encoding="utf-8").write(
            "repo\tcuenta\trol\tremoto\truta\twhy\tguia\n"
            "declared-elsewhere\tx\tactivo\torigin\t.\tprobe\t-\n")
    try:
        # ⭐ pre-push resolves its root from where the hook LIVES, so it is run
        # from the engine copy exactly as .git/hooks would invoke it.
        _url = "https://example.invalid/nobody/undeclared.git"
        r = run(["bash", os.path.join(HOOKS, "pre-push.sh"), "origin", _url])
        case("④b 🔴 ⭐ pre-push lets an UNDECLARED push through while paused",
             r.returncode == 0, "exit=%d" % r.returncode)
    finally:
        if not _had_reg and os.path.isfile(_reg):
            os.remove(_reg)

    r = run(["bash", os.path.join(HOOKS, "pre-commit.sh")], cwd=os.path.dirname(ROOT))
    case("④c 🔴 ⭐ pre-commit does not block while paused",
         r.returncode == 0, "exit=%d" % r.returncode)

    # ── ⑤ AND IT COMES BACK ────────────────────────────────────────────────
    r = run([sys.executable, os.path.join(BIN, "on")])
    case("⑤ on resumes and removes the marker",
         r.returncode == 0 and not os.path.exists(OFF), "exit=%d" % r.returncode)
    r = run([sys.executable, os.path.join(BIN, "on")])
    case("⑤b on twice is not an error", r.returncode == 0)

    # ── ⑥ THE HOOK SPEAKS AGAIN ONCE RESUMED ───────────────────────────────
    # ⛔ Without this, a hook broken by the guard would pass ④ perfectly:
    # permanently silent looks identical to correctly paused.
    # ⭐ Same registry, same destination — ⛔ the ONLY difference from ④b is
    # that the switch is gone. That is what makes the pair a measurement.
    _had_reg = os.path.isfile(_reg)
    if not _had_reg:
        open(_reg, "w", encoding="utf-8").write(
            "repo\tcuenta\trol\tremoto\truta\twhy\tguia\n"
            "declared-elsewhere\tx\tactivo\torigin\t.\tprobe\t-\n")
    try:
        r = run(["bash", os.path.join(HOOKS, "pre-push.sh"), "origin", _url])
        case("⑥ 🔴 ⭐ pre-push ABORTS the same push once resumed",
             r.returncode == 1, "exit=%d" % r.returncode)
    finally:
        if not _had_reg and os.path.isfile(_reg):
            os.remove(_reg)
finally:
    if os.path.exists(OFF):
        os.remove(OFF)
    if _made and os.path.isfile(CONFIG):
        os.remove(CONFIG)

# ── ⑦ STATUS SPEAKS TO THE OWNER, NOT TO A DEVELOPER ───────────────────────
# 🔴 The complaint was that the words meant nothing. ⛔ A status page naming
# files and flags answers the developer's question, not the owner's.
_txt = open(os.path.join(BIN, "status"), encoding="utf-8").read()
_shown = [l for l in _txt.split("\n") if l.strip().startswith("print(")]
case("⑦ ⭐ status says where it all lives, every time",
     "lives in this folder" in _txt.lower())
case("⑦c ⛔ it never tells the owner to type a command",
     not any("bin/" in l for l in _shown), "%d printed line(s)" % len(_shown))

print("\n  ⬜ NOT MEASURED · whether an assistant CALLS these when asked · that\n"
      "     runs outside this engine · these cases prove the switch is real")

good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: none")
sys.exit(0 if good == len(results) else 1)
