#!/usr/bin/env python3
"""probe-declarations — proves the unfilled ⬜ are counted, and never treated as faults.

⭐ `⬜` IS WHAT MAKES THIS ENGINE PORTABLE: the engine ships the rule, the
installation supplies the value. ⛔ An unfilled one switches its rule OFF — and
that is CORRECT, because a threshold nobody chose must not be invented. What is
wrong is that it is INVISIBLE: `0` reads like a number and `null` like a value.

⚠️ SO THE HARDEST REQUIREMENT IS THAT IT NEVER FAILS. Every line it prints is a
decision the owner may leave open forever. ⛔ A check that exits non-zero over
those turns a deliberate choice into debt, and the next person "fixes" it by
inventing the numbers this engine refuses to invent.

Runs against an ISOLATED COPY: the cases edit rules and a config.
"""
import os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-dec-")
TREE = os.path.join(WORK, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git", "cache"))
TOOL = os.path.join(TREE, "bin", "check-declarations")
RULE = os.path.join(TREE, "rules", "zzprobe-rule.md")
CFG = os.path.join(TREE, "mente.config.yml")

HEAD = """# RULE · a probe fixture

**Status:** current · **Type:** rule · **Updated:** 2026-01-15 · **Owner:** x

## Purpose

A fixture used to prove the checker detects what it claims to.

## 1 · Thresholds

| ⬜ Section | Lines | Why |
|---|---|---|
"""


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def run(*args):
    return subprocess.run([sys.executable, TOOL] + list(args), cwd=TREE,
                          capture_output=True, text=True, timeout=60)


def plant(rows):
    open(RULE, "w", encoding="utf-8").write(
        HEAD + rows + "\n\nRelated: `rules/README.md`.\n")


print("═══ PROBE · check-declarations ═══\n")

# ── ⭐ AN UNSET THRESHOLD IS COUNTED ────────────────────────────────────────
plant("| ⬜ Z `Zzprobe` | 0 | ⬜ declare it |\n")
r = run()
case("① ⭐ a deferred value left at 0 is counted",
     "zzprobe-rule.md" in r.stdout and "Zzprobe" in r.stdout)

# ⛔ AND IT DOES NOT FAIL. Every line is a decision the owner may leave open.
case("② ⛔ it NEVER exits non-zero — a pending decision is not debt",
     r.returncode == 0, "exit=%d" % r.returncode)

# ⭐ once given a value, it stops being counted
plant("| ⬜ Z `Zzprobe` | 40 | declared |\n")
r = run()
case("③ ⭐ once filled, it is no longer counted", "Zzprobe" not in r.stdout)

# ⚠️ a row with no ⬜ marker defers nothing — counting it would report every
# table in the engine
plant("| Z `Zzplain` | 0 | not a declaration |\n")
r = run()
case("④ ⚠️ a row with no ⬜ is not a declaration", "Zzplain" not in r.stdout)
os.remove(RULE)

# ── ⭐ THE INSTANCE SIDE · the three empty shapes the template ships ────────
open(CFG, "w", encoding="utf-8").write(
    'schema: v1\nowner:\n  name: "x"\n  never_called: []\npillars:\n'
    '  architecture: null\nsession:\n  project_dir: ""\ngates: []\n')
r = run()
# ⭐ ONE CASE PER SUBJECT, so each row is its own ADDRESS: this loop applies one
# check to four settings, and a bare "⑤ failed" would not say which.
for _i, field in enumerate(("never_called", "architecture",
                            "project_dir", "gates")):
    case("⑤%s ⭐ config · `%s` at its empty default is counted"
         % ("abcd"[_i], field), field in r.stdout)

# ⭐ and a filled value disappears from the list
open(CFG, "w", encoding="utf-8").write(
    'schema: v1\nowner:\n  name: "x"\n  never_called: ["Jon Doe"]\n'
    'pillars:\n  architecture: "Cerebro/ARCHITECTURE.md"\n')
r = run()
case("⑥ ⭐ a filled value drops off the list",
     "never_called" not in r.stdout and "architecture" not in r.stdout)
case("⑦ ⭐ and with all of them filled it says so",
     "every instance value" in r.stdout)

# ── ⬜ WHAT IT CANNOT SEE, IT SAYS ──────────────────────────────────────────
# ⛔ Without a config nothing distinguishes "the owner left these open" from
# "nobody has installed this yet" — and reporting the second as the first would
# make a fresh clone look neglected.
os.remove(CFG)
r = run()
case("⑧ ⬜ no config → says the tree is not installed, not «all unfilled»",
     "not installed" in r.stdout)

# ── ⭐ CHK-QUI-001 · the flag means the exit code, and nothing else ─────────
r = run("--quiet")
case("⑨ ⭐ --quiet prints nothing at all",
     not r.stdout.strip(), repr(r.stdout[:20]))
case("⑩ ⭐ and still exits 0 — findings here are never a failure",
     r.returncode == 0, "exit=%d" % r.returncode)

# ── ⛔ robustness ───────────────────────────────────────────────────────────
open(os.path.join(TREE, "rules", "zzbad.md"), "wb").write(b"\xff\xfe\x00")
r = run()
case("⑪ ⛔ an unreadable rule does not crash the count",
     "Traceback" not in r.stderr, r.stderr.strip()[:26])

# ── ⭐ BOTH TREES, AND BOTH SHAPES ──────────────────────────────────────────
# ⛔ Reading only `rules/` and only `| ⬜ x | 0 |` reported 7 deferred values
# when 27 exist: every discipline's §3 and every ceiling in the delivery
# contract sat unseen, and an installation was never told they were waiting.
# ⚠️ A validator whose reach is narrower than what it counts does not report a
# smaller number — it reports a WRONG one, confidently.
_pr = os.path.join(TREE, "memory", "principles")
os.makedirs(_pr, exist_ok=True)
_q = os.path.join(_pr, "zzprobe-principle.md")
_before = run().stdout

open(_q, "w", encoding="utf-8").write(
    "# zz\n\n**Status:** current · **Type:** contract · **Updated:** 2026-01-15"
    " · **Owner:** x\n\n## Purpose\n\nA planted principle.\n\n"
    "| Thing | Value |\n|---|---|\n| a ceiling | ⬜ … |\n\n"
    "Related: `README.md`.\n")
_after = run().stdout
_n = lambda t: int(re.search(r"· (\d+) rule value", t).group(1)) if \
    re.search(r"· (\d+) rule value", t) else -1
case("⑫ ⭐ a deferred value under principles/ is counted",
     _n(_after) == _n(_before) + 1,
     "%d → %d" % (_n(_before), _n(_after)))

# ⛔ THE SECOND SHAPE: the VALUE cell is the ⬜, not the row marker.
open(_q, "w", encoding="utf-8").write(
    "# zz\n\n**Status:** current · **Type:** contract · **Updated:** 2026-01-15"
    " · **Owner:** x\n\n## Purpose\n\nA planted principle.\n\n"
    "| Thing | Value |\n|---|---|\n| a ceiling | 250 lines |\n\n"
    "Related: `README.md`.\n")
case("⑬ ⭐ and a value that IS declared stops being counted",
     _n(run().stdout) == _n(_before), "back to %d" % _n(_before))
os.remove(_q)

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copy"))
sys.exit(0 if good == len(results) else 1)
