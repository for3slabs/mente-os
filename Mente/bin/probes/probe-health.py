#!/usr/bin/env python3
"""probe-health — proves the two system-level concerns are measured, or said to be unmeasured.

⭐ THIS VALIDATOR'S HARDEST REQUIREMENT IS NOT DETECTION — it is refusing to
print a green over a check that could not run. ⛔ A health report is trusted more
than any other output, and the one thing a healthy system and a blind one have
in common is silence.

⚠️ Both concerns depend on host-specific paths, so most cases here measure the
NOT MEASURED path: what happens when the engine cannot see.
"""
import os, re, shutil, subprocess, sys, tempfile
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
import plat                                          # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-health-")
TREE = os.path.join(WORK, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git"))
CHECK = os.path.join(TREE, "bin", "check-health")
SESS = os.path.join(WORK, "transcripts")
os.makedirs(SESS)
REG = os.path.join(WORK, "registry.json")


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def run(**env):
    return subprocess.run([sys.executable, CHECK], cwd=TREE,
                          capture_output=True, text=True,
                          env=dict(os.environ, **env))


def transcript(name, mb):
    p = os.path.join(SESS, name)
    with open(p, "wb") as fh:
        fh.write(b"x" * int(mb * 1024 * 1024))
    return p


def registry(names):
    import json
    open(REG, "w").write(json.dumps({"hooks": list(names)}))
    return REG


print("═══ SONDA · check-health ═══\n")

# ── ⛔ THE HARDEST REQUIREMENT · never a green over what could not run ──────
r = run()
case("① ⬜ with nothing declared → it says what it did NOT measure",
     "NOT MEASURED" in r.stdout and "✅" not in r.stdout, "exit=%d" % r.returncode)
# ⚠️ THE DENOMINATOR IS READ FROM THE PRODUCER, never written here. 🔴 Measured
# 2026-09-08: a third concern was added to check-health and this case went red
# while the validator was correct — the literal `2` lived in two places and only
# one of them moved. ⛔ A probe that has to be edited every time the thing it
# measures grows is a probe people delete.
_hc = open(os.path.join(TREE, "bin", "check-health"), encoding="utf-8").read()
_n = re.search(r"^CONCERNS = (\d+)", _hc, re.M)
case("② ⛔ and it does NOT print a ✅ over what was not measured",
     bool(_n) and "0 of %s concern(s) measured" % _n.group(1) in r.stdout,
     "" if _n else "🔴 check-health declares no CONCERNS")

# ── ① HOOK WIRING · the failure that reads as success ──────────────────────
hooks = sorted(n for n in os.listdir(os.path.join(TREE, "hooks"))
               if not n.startswith(("_", ".")) and n != "README.md")
r = run(MENTE_HOOK_REGISTRY=registry(hooks))
case("③ ⭐ every hook registered → no finding",
     "🔴" not in r.stdout, "exit=%d" % r.returncode)

r = run(MENTE_HOOK_REGISTRY=registry(hooks[:-2]))
case("④ 🔴 two hooks the registry never names → detected",
     r.returncode == 1 and "NEVER RUNS" in r.stdout, "exit=%d" % r.returncode)
case("⑤ ⭐ and it NAMES them, it does not just count", hooks[-1] in r.stdout)

# ⬜ a registry that was declared and is not there is a GAP, not a pass
r = run(MENTE_HOOK_REGISTRY="/nowhere/registry.json")
case("⑥ ⬜ a declared registry that is absent → a gap, not a ✅",
     r.returncode == 0 and "does not exist" in r.stdout)

# ── ② SESSION WEIGHT · the guard a past incident paid for ──────────────────
transcript("small.jsonl", 1)
r = run(MENTE_SESSION_DIR=SESS, MENTE_SESSION_ID="small")
case("⑦ ⭐ a small session does not nag", "🔴" not in r.stdout)

transcript("heavy.jsonl", 20)
r = run(MENTE_SESSION_DIR=SESS, MENTE_SESSION_ID="heavy")
case("⑧ ⚠️ past the warning → it says so", r.returncode == 1 and "watch it" in r.stdout,
     "exit=%d" % r.returncode)

transcript("huge.jsonl", 55)
r = run(MENTE_SESSION_DIR=SESS, MENTE_SESSION_ID="huge")
case("⑨ 🔴 past the limit → a finding", r.returncode == 1 and "past the" in r.stdout,
     "exit=%d" % r.returncode)
case("⑩ ⭐ and it explains the work degrades BEFORE anything breaks",
     "no error to notice" in r.stdout)

# ⭐ THE RESOLVER · without a named session the newest file is a GUESS, and the
# guess is wrong exactly after a reset: the new transcript is small and loses to
# the previous one. ⛔ So the guess is declared as one.
r = run(MENTE_SESSION_DIR=SESS)
case("⑪ ⭐ with no session named, it says it GUESSED", "guessed" in r.stdout)

r = run(MENTE_SESSION_DIR=SESS, MENTE_SESSION_ID="small")
case("⑫ ⭐ with the session named it measures the LIVE one, not the heaviest",
     "🔴" not in r.stdout)

# ⬜ declared and absent · a gap
r = run(MENTE_SESSION_DIR="/nowhere/at/all")
case("⑬ ⬜ a declared directory that is absent → a gap, not a ✅",
     r.returncode == 0 and "does not exist" in r.stdout)

# ⭐ an empty directory is not a healthy session — it is nothing to measure
empty = os.path.join(WORK, "empty")
os.makedirs(empty, exist_ok=True)
r = run(MENTE_SESSION_DIR=empty)
case("⑭ ⬜ an empty directory → nothing to measure, not a ✅",
     "no transcript" in r.stdout)

# ── ⭐ ALL THREE measured and healthy → the only case that earns a green ────
# ⚠️ THE THIRD ONE NEEDS A REPOSITORY. 🔴 Caught the hour `engine_updates`
# landed: this tree has no git, so that concern could not be measured and the
# full ✅ correctly stopped appearing. ⛔ The case was right and the fixture was
# short — giving it a repository with an `upstream` is what makes "everything
# measured" true again, rather than lowering what the case demands.
_up = subprocess.run(("git", "init", "-q", "."), cwd=WORK,
                     capture_output=True, text=True)
subprocess.run(("git", "-c", "user.email=t@t", "-c", "user.name=t",
                "commit", "-q", "--allow-empty", "-m", "base"),
               cwd=WORK, capture_output=True, text=True)
# ⭐ A LOCAL "engine" TO COMPARE AGAINST — no network in a probe. ⛔ A remote
# that was never fetched is an honest ⬜, so pointing at an unreachable URL
# would measure the gap, not the healthy case this asserts.
_eng = os.path.join(WORK, "engine.git")
subprocess.run(("git", "clone", "-q", "--bare", WORK, _eng),
               capture_output=True, text=True)
subprocess.run(("git", "remote", "add", "upstream", _eng),
               cwd=WORK, capture_output=True, text=True)
subprocess.run(("git", "fetch", "-q", "upstream"), cwd=WORK,
               capture_output=True, text=True)
r = run(MENTE_HOOK_REGISTRY=registry(hooks), MENTE_SESSION_DIR=SESS,
        MENTE_SESSION_ID="small")
case("⑮ ⭐ EVERYTHING measured and healthy → now a full ✅",
     "✅" in r.stdout and r.returncode == 0,
     "" if "✅" in r.stdout else r.stdout.strip().splitlines()[-1][:70])

# ── ④b 🔴 A GATE PASSED AS AN ARGUMENT IS STILL WIRED ──────────────────────
# 🔴 THE FAILURE, measured 2026-09-09. `gate-run.py` runs several gates in ONE
# interpreter — starting Python costs 173 ms on Windows and a gate's own work
# is ~50 ms, so one process per gate spent 70% of its time booting. ⛔ The
# settings file then names the DISPATCHER and passes the gates as arguments,
# and this check, matching on file names, reported five LIVE gates as
# unregistered on a machine where every one of them was firing.
# ⚠️ A red on a correct install is how a real red stops being read.
_disp = os.path.join(WORK, "dispatched.json")
open(_disp, "w", encoding="utf-8", newline="").write(
    '{"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command",'
    '"command":"python3 hooks/gate-run.py gate-critical gate-accounts"}]}]}}')
r = run(MENTE_HOOK_REGISTRY=_disp)
case("④b 🔴 ⭐ a gate DISPATCHED by argument counts as wired",
     "gate-critical" not in r.stdout and "gate-accounts" not in r.stdout,
     "" if "gate-critical" not in r.stdout else "🔴 reported as unregistered")

# ⛔ AND ONE NOBODY NAMES IS STILL REPORTED. The half that keeps it honest: if
# naming the dispatcher excused every gate, the check would have been deleted
# rather than fixed.
case("④c ⛔ and a gate NOBODY names is still reported",
     "gate-handoff" in r.stdout,
     "" if "gate-handoff" in r.stdout else "🔴 the dispatcher excused it")

# ── ⑮b 🔴 A NEWER ENGINE IS SAID, AND THE BRANCH IS ASKED FOR ──────────────
# 🔴 THE FAILURE this freezes, caught the hour the check landed: it compared
# against `upstream/main` by name. A repository created with git's older
# default is on `master`, so `rev-list` failed and the check reported "nothing
# fetched yet" about a tree that had fetched perfectly. ⛔ Every person on
# `master` would have been told they were up to date, forever, and the reason
# given would have been wrong.
# ⚠️ Measured with a LOCAL bare repository standing in for the engine — a probe
# that reaches the network measures the network.
subprocess.run(("git", "-c", "user.email=t@t", "-c", "user.name=t",
                "commit", "-q", "--allow-empty", "-m", "newer-engine"),
               cwd=WORK, capture_output=True, text=True)
subprocess.run(("git", "push", "-q", "upstream", "HEAD"), cwd=WORK,
               capture_output=True, text=True)
subprocess.run(("git", "reset", "-q", "--hard", "HEAD~1"), cwd=WORK,
               capture_output=True, text=True)
subprocess.run(("git", "fetch", "-q", "upstream"), cwd=WORK,
               capture_output=True, text=True)
r = run(MENTE_HOOK_REGISTRY=registry(hooks), MENTE_SESSION_DIR=SESS,
        MENTE_SESSION_ID="small")
case("⑮b 🔴 ⭐ a newer engine is NAMED, whatever the branch is called",
     "newer commit(s) in Mente OS" in r.stdout,
     "" if "newer commit" in r.stdout else r.stdout.strip().splitlines()[-1][:60])

# ⛔ AND IT NEVER PULLS. The half that makes the notice safe: bringing changes
# in could overwrite the person's own work, so the notice says how and stops.
case("⑮c ⛔ and it changed NOTHING — it only said so",
     subprocess.run(("git", "rev-list", "--count", "HEAD"), cwd=WORK,
                    capture_output=True, text=True).stdout.strip() == "1")

# ── ⑮d 🔴 THE ADVICE MUST WORK IN THE CASE THAT NEEDS IT MOST ──────────────
# 🔴 THE FAILURE, measured 2026-09-08 on the real install this feature came
# from. The person had deleted the clone's history to give their project its
# own — the CORRECT thing to do — so their tree shares no root with the engine.
# ⛔ `git merge upstream/<branch>` there is not an update: it is a conflict in
# every one of 171 files. Following the advice leaves them worse off than not
# reading it.
# ⛔ AND THE FIRST FIX WAS WORSE: `git checkout <ref> -- Mente/` updates the
# engine cleanly and OVERWRITES the instance inside it — measured, a RESUME.md
# holding real memory replaced by the engine's template, in silence.
_unrel = os.path.join(WORK, "unrelated")
os.makedirs(_unrel, exist_ok=True)
shutil.copytree(TREE, os.path.join(_unrel, "Mente"),
                ignore=shutil.ignore_patterns("__pycache__", ".beats", ".git"))
for _c in (("git", "init", "-q", "."),
           ("git", "-c", "user.email=t@t", "-c", "user.name=t", "commit",
            "-q", "--allow-empty", "-m", "their own history"),
           ("git", "remote", "add", "upstream", _eng),
           ("git", "fetch", "-q", "upstream")):
    subprocess.run(_c, cwd=_unrel, capture_output=True, text=True)
# ⚠️ RUN THE COPY INSIDE THAT TREE, not this one: check-health resolves the
# repository from its OWN path, so running the working tree's script would
# measure the working tree's git and prove nothing.
r = subprocess.run(
    [sys.executable, os.path.join(_unrel, "Mente", "bin", "check-health")],
    cwd=os.path.join(_unrel, "Mente"), capture_output=True, text=True,
    env=dict(os.environ, MENTE_HOOK_REGISTRY=registry(hooks),
             MENTE_SESSION_DIR=SESS, MENTE_SESSION_ID="small"))
case("⑮d 🔴 ⭐ with no shared root it does NOT advise a merge",
     "newer commit" in r.stdout and "git merge" not in r.stdout,
     "" if "git merge" not in r.stdout else "🔴 still says merge")
case("⑮e ⭐ and it names the command that leaves your memory alone",
     "update-engine" in r.stdout)

# ── 🔴 THE DEFECT THE CLEAN CLONE FOUND, INVISIBLE IN THE WORKING TREE ─────
# mente.config.yml is an INSTANCE file, so a clone legitimately lacks one. The
# first version returned early on that and ignored the environment entirely —
# ⛔ reporting "nothing declared" while the operator had declared everything,
# which is a health report wrong in the confident direction.
# ⚠️ A clean clone HAS no config — it is gitignored. Removing one that may not
# be there is the same assumption the defect was made of, so this only ensures
# the absent state rather than assuming the present one.
_cfg = os.path.join(TREE, "mente.config.yml")
if os.path.exists(_cfg):
    os.remove(_cfg)
r = run(MENTE_HOOK_REGISTRY=registry(hooks[:-1]), MENTE_SESSION_DIR=SESS,
        MENTE_SESSION_ID="huge")
case("⑰ 🔴 with NO config, the environment still governs", r.returncode == 1,
     "exit=%d" % r.returncode)
case("⑱ ⭐ and the summary can count (a NOTE is not a gap)",
     "-1 of" not in r.stdout and "of 2 concern" not in r.stdout)

# ── ⛔ robustness ───────────────────────────────────────────────────────────
open(os.path.join(TREE, "mente.config.yml"), "wb").write(b"\xff\xfe\x00")
r = run()
case("⑯ ⛔ an unreadable configuration does not crash the check",
     "Traceback" not in r.stderr)

plat.rmtree(WORK)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
