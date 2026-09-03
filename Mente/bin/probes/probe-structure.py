#!/usr/bin/env python3
"""probe-structure — proves the table-side check tells a STALE row from a legitimate absence.

⭐ THE WHOLE DIFFICULTY IS THAT MOST ABSENCES ARE CORRECT. A clone legitimately
lacks every instance file, and the table legitimately declares pieces before they
are built. ⛔ A checker that reported those would be red on arrival, and a
checker that is red on arrival is one nobody reads afterwards.

⚠️ So the cases below measure the CLASSIFICATION, not the detection: a defect
found among the exceptions, and each exception left alone.

Runs against an ISOLATED COPY — the subject is the piece table itself.
"""
import os, shutil, subprocess, sys, tempfile
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-struct-")
TREE = os.path.join(WORK, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git"))
CHECK = os.path.join(TREE, "bin", "check-structure")
TABLE = os.path.join(TREE, "pieces.tsv")
BASE = open(TABLE, encoding="utf-8").read()


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def run(extra=""):
    # ⭐ The instance-file classification is DERIVED from templates/, so the
    # fixture declares its own template rather than borrowing a real file whose
    # presence depends on whether this tree was installed.
    tpl = os.path.join(TREE, "templates", "zzprobe-instance.md.template")
    if not os.path.exists(tpl):
        open(tpl, "w", encoding="utf-8").write("# fixture\n")
    open(TABLE, "w", encoding="utf-8").write(BASE + extra)
    return subprocess.run([sys.executable, CHECK], cwd=TREE,
                          capture_output=True, text=True)


def row(name, path):
    return "%s\t%s\tengine\texecutable\ta fixture row\n" % (name, path)


print("═══ SONDA · check-structure ═══\n")

# ① the baseline · the real table must be silent, or nothing below means anything
r = run()
case("① ⭐ the real table has no stale rows", r.returncode == 0,
     "exit=%d" % r.returncode)

# ② 🔴 THE DEFECT IT EXISTS FOR · a row whose file was replaced and never removed
r = run(row("zzprobe-stale", "rules/a-file-that-was-merged-away.md"))
case("② 🔴 a row whose file no longer exists → detected",
     r.returncode == 1 and "STR-ROW-001" in r.stdout, "exit=%d" % r.returncode)
case("③ ⭐ and it explains the row outlived what it described",
     "the row stayed" in r.stdout)

# ── THE THREE LEGITIMATE ABSENCES · none may be reported ────────────────────
# ⬜ an instance file · a clone lacks it BY DESIGN
r = run(row("zzprobe-inst", "docs/WORKSPACE.md"))
case("④ ⬜ an INSTANCE file is not a finding", r.returncode == 0,
     "exit=%d" % r.returncode)

# ⬜ a planned piece · declared before it is built, on purpose
r = run(row("zzprobe-plan", "bin/check-health"))
case("⑤ ⬜ a PLANNED piece is not a finding", r.returncode == 0,
     "exit=%d" % r.returncode)

# ⭐ and `planned` is read from the capability map, so declaring it once is enough
cap = os.path.join(TREE, "CAPABILITIES.md")
keep = open(cap, encoding="utf-8").read()
open(cap, "w", encoding="utf-8").write(
    keep + "\n⬜ | `bin/check-zznew` | planned here and nowhere else |\n")
r = run(row("zzprobe-newplan", "bin/check-zznew"))
case("⑥ ⭐ declaring it ⬜ in the map is enough to count as planned",
     r.returncode == 0, "exit=%d" % r.returncode)
open(cap, "w", encoding="utf-8").write(keep)

# ── 🔴 THE TWO BUGS THIS VALIDATOR HAD ON ITS FIRST RUN ─────────────────────
# ⛔ `lstrip("./")` strips CHARACTERS, not a prefix — so `.gitignore` became
# `gitignore`, and the validator reported its own tree's most fundamental file
# as a stale row. ⚠️ A mistake that only appears on a name starting with one of
# those characters, which is why it survived until a dotfile was declared.
r = run()
case("⑦ 🔴 a declared DOTFILE is not reported (the lstrip bug)",
     "gitignore" not in r.stdout.replace(".gitignore", ""))

# ⛔ A gitignore pattern with a directory part was reduced to its basename, so a
# declared file INSIDE an ignored folder read as stale.
r = run(row("zzprobe-under", "connection/bridges/SOMETHING.md"))
case("⑧ ⛔ a file inside an ignored folder is not stale",
     r.returncode == 0, "exit=%d" % r.returncode)

# ── ⭐ the exceptions are DERIVED, never listed ──────────────────────────────
# ⛔ A hand-kept list of allowed absences is a hole with a schedule: add a
# generated file, forget the list, and a healthy tree reports as broken.
tdir = os.path.join(TREE, "templates")
open(os.path.join(tdir, "ZZNEW.md.template"), "w").write("x\n")
r = run(row("zzprobe-derived", "ZZNEW.md"))
case("⑨ ⭐ adding a TEMPLATE is enough to make its file legitimate",
     r.returncode == 0, "exit=%d" % r.returncode)
os.remove(os.path.join(tdir, "ZZNEW.md.template"))

# ── ⬜ what was NOT measured is said out loud ────────────────────────────────
# ⚠️ PLANTED, not assumed. The first version asserted the real tree happened to
# contain both kinds of legitimate absence — and it did, until the planned
# pieces were built and only one kind was left. ⛔ A probe that depends on the
# tree's current shape measures the tree, not the checker.
# ⭐ `check-sufficiency` is the one piece the contract decided NOT to build, so
# it stays ⬜ in the map — the only stable example of a planned absence.
# 🔴 PLANTED, AND THE PLANT MUST NOT EXIST EITHER. The first version named
# docs/WORKSPACE.md — an instance file that is absent in a template and PRESENT
# in an installation, so the case passed in one and failed in the other.
# ⛔ A probe whose fixture depends on whether the tree is installed measures the
# tree, not the checker — twice now, in this same case.
# ⭐ A template exists for it, so it is classified as an instance file whether or
# not anybody ever creates it.
r = run(row("zzprobe-inst2", "zzprobe-instance.md")
        + row("zzprobe-plan2", "bin/check-sufficiency"))
case("⑩ ⬜ the report NAMES each absence and why it is one",
     "⬜" in r.stdout and "instance file" in r.stdout and "planned" in r.stdout)
case("⑪ ⭐ and it says how many rows resolved", "resolve" in r.stdout)

# ── ⛔ robustness ───────────────────────────────────────────────────────────
os.remove(TABLE)
r = subprocess.run([sys.executable, CHECK], cwd=TREE, capture_output=True,
                   text=True)
case("⑫ ⬜ no table → exit 2, not an empty ✅", r.returncode == 2,
     "exit=%d" % r.returncode)

open(TABLE, "wb").write(b"\xff\xfe not text\n")
r = subprocess.run([sys.executable, CHECK], cwd=TREE, capture_output=True,
                   text=True)
case("⑬ ⛔ an unreadable table does not crash the check",
     "Traceback" not in r.stderr)

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
