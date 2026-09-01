#!/usr/bin/env python3
"""probe-health — proves the two system-level concerns are measured, or said to be unmeasured.

⭐ THIS VALIDATOR'S HARDEST REQUIREMENT IS NOT DETECTION — it is refusing to
print a green over a check that could not run. ⛔ A health report is trusted more
than any other output, and the one thing a healthy system and a blind one have
in common is silence.

⚠️ Both concerns depend on host-specific paths, so most cases here measure the
NOT MEASURED path: what happens when the engine cannot see.
"""
import os, shutil, subprocess, sys, tempfile

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
case("② ⛔ and it does NOT print a ✅ over what was not measured",
     "0 of 2 concern(s) measured" in r.stdout)

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

# ── ⭐ both measured and healthy → the only case that earns a green ─────────
r = run(MENTE_HOOK_REGISTRY=registry(hooks), MENTE_SESSION_DIR=SESS,
        MENTE_SESSION_ID="small")
case("⑮ ⭐ EVERYTHING measured and healthy → now a full ✅",
     "✅" in r.stdout and r.returncode == 0)

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

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
