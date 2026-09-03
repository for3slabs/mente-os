#!/usr/bin/env python3
"""probe-locks — proves a rule claiming a lock it does not have is caught, and a delegated one is not.

⭐ THE CLAIM THIS CHECK MAKES IS NARROW ON PURPOSE, and the probe holds it to
that: it measures whether a declared id is NAMED in code. ⛔ It cannot know
whether that code enforces anything — and a probe that pretended otherwise would
be asserting something the check does not do.

⚠️ THE FALSE ALARM IS THE FAILURE MODE. Several rules are delegated: their lock
is performed by another rule's check. ⛔ Counting those as gaps produces noise on
a correct tree, and a check that cries wolf is switched off — taking the real
findings with it. Half the cases below measure what it must NOT report.

Runs against an ISOLATED COPY: the cases plant rules and code.
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
WORK = tempfile.mkdtemp(prefix="mente-locks-")
TREE = os.path.join(WORK, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git", "cache"))
RULE = os.path.join(TREE, "rules", "zzprobe-rule.md")
CODE = os.path.join(TREE, "bin", "check-zzprobe")

HEAD = """# RULE · a probe fixture

**Status:** current · **Type:** rule · **Updated:** 2026-01-15 · **Owner:** x

## Purpose

A fixture used to prove the checker detects what it claims to.

## 1 · Rows

| ID | Rule | Enf | Verify |
|---|---|---|---|
"""


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def plant(rows, code=""):
    open(RULE, "w", encoding="utf-8").write(
        HEAD + rows + "\n\nRelated: `rules/README.md`.\n")
    if code:
        open(CODE, "w", encoding="utf-8").write("#!/usr/bin/env python3\n" + code)
        os.chmod(CODE, 0o755)
    elif os.path.exists(CODE):
        os.remove(CODE)


def run():
    return subprocess.run([sys.executable, os.path.join(TREE, "bin", "check-locks")],
                          cwd=TREE, capture_output=True, text=True, timeout=60)


def mine(out):
    return [l for l in out.splitlines() if "zzprobe" in l and "🔴" in l]


print("═══ PROBE · check-locks ═══\n")

# ── 🔴 THE LIE IT EXISTS FOR ────────────────────────────────────────────────
plant("| `ZZP-AAA-001` | a rule that claims a lock | 🔒 | nothing enforces it |\n")
r = run()
case("① 🔴 a 🔒 with no code anywhere → detected",
     r.returncode == 1 and mine(r.stdout), "exit=%d" % r.returncode)

# ⭐ and the same row, once the code names the id
plant("| `ZZP-AAA-001` | a rule that claims a lock | 🔒 | now enforced |\n",
      "# enforces ZZP-AAA-001\n")
r = run()
case("② ⭐ the same row, once code names it → silent", not mine(r.stdout))

# ── ⛔ WHAT IT MUST NOT REPORT ──────────────────────────────────────────────
# A 📖 row makes no claim of enforcement, so it is not a gap.
plant("| `ZZP-BBB-001` | a rule enforced by discipline | 📖 | nothing checks this |\n")
r = run()
case("③ ⛔ a 📖 row is not a gap — it claims no lock", not mine(r.stdout),
     "exit=%d" % r.returncode)

# ⭐ DELEGATION, in both wordings the rules already use. Counting these as gaps
# is the false alarm that gets a check switched off.
for word in ("performed", "enforced"):
    plant("| `ZZP-CCC-001` | delegated | 🔒 | ⭐ %s by `ZZP-DDD-001` |\n" % word,
          "# ZZP-DDD-001 is the one that runs\n")
    r = run()
    case("④%s ⭐ `%s by` a cited id → not a gap"
         % ("ab"[("performed", "enforced").index(word)], word), not mine(r.stdout))

# ⛔ but a delegation to an id NOTHING implements is still a gap — otherwise
# `performed by` becomes a way to declare a lock into existence.
plant("| `ZZP-EEE-001` | delegated to nothing | 🔒 | performed by `ZZP-FFF-999` |\n")
r = run()
case("⑤ ⛔ delegated to an id nothing implements → still a gap",
     bool(mine(r.stdout)), "exit=%d" % r.returncode)
case("⑥ ⭐ and it names the id the delegation pointed at",
     "ZZP-FFF-999" in r.stdout)

# ── ⛔ EXACTNESS · a check about exact claims cannot compare loosely ────────
# `ZZP-GGG-001` occurs inside `ZZP-GGG-0012`: a substring search would call the
# rule locked because a DIFFERENT id contains it.
plant("| `ZZP-GGG-001` | short id | 🔒 | nothing |\n",
      "# only ZZP-GGG-0012 appears here\n")
r = run()
case("⑦ ⛔ a LONGER id containing it does not count as citing it",
     bool(mine(r.stdout)), "exit=%d" % r.returncode)

# ── ⭐ THE CLAIM IS NARROW, AND THE OUTPUT SAYS SO ──────────────────────────
# ⛔ A reader who takes a citation for proof of enforcement has been told
# something this check cannot know.
plant("| `ZZP-HHH-001` | x | 🔒 | y |\n", "# ZZP-HHH-001\n")
r = run()
case("⑧ ⭐ every run says a citation is NOT proof of enforcement",
     "NAMED in code" in r.stdout)
case("⑨ ⭐ and reports the three counts it measured",
     "declared" in r.stdout and "cited in code" in r.stdout
     and "delegated" in r.stdout)

# ── CHK-DIS-001 · a 📖 row says WHICH of two things it is ──────────────────
# ⛔ "Nothing verifies this" hides two opposite facts: a script CANNOT check it,
# or one has not been WRITTEN yet. ⚠️ Mixed into one symbol the buildable ones
# are invisible — and a backlog nobody can see is a backlog nobody works.
plant("| `ZZP-III-001` | unbuilt | 📖 | ⚠️ nothing verifies this yet |\n")
r = run()
case("⑫ ⭐ a 📖 row saying `yet` is counted as WORK",
     "ZZP-III-001" in r.stdout and "are WORK" in r.stdout)

plant("| `ZZP-JJJ-001` | a real limit | 📖 | ⛔ a script cannot know intent |\n")
r = run()
case("⑬ ⭐ a 📖 row that EXPLAINS its limit is not counted",
     "ZZP-JJJ-001" not in r.stdout)

# ⚠️ And the ambiguous middle is reported as ambiguous — not as a finding, and
# not silently: a row a reader cannot act on is worth naming.
plant("| `ZZP-KKK-001` | unclear | 📖 | ⛔ nothing verifies this |\n")
r = run()
case("⑭ ⚠️ a 📖 row that says neither → reported as ambiguous",
     "WHICH KIND" in r.stdout)

# ⛔ and none of the three is a FAILURE: a discipline row breaks nothing
case("⑮ ⛔ none of them fails the check — 📖 is not a violation",
     r.returncode == 0, "exit=%d" % r.returncode)

# ── ⬜ WHAT IT CANNOT SEE, IT SAYS ──────────────────────────────────────────
# ⛔ With no code at all every lock looks unimplemented — reporting 199 findings
# would be technically true and completely useless.
os.remove(RULE)
keep = tempfile.mkdtemp()
shutil.move(os.path.join(TREE, "bin"), os.path.join(keep, "bin"))
shutil.move(os.path.join(TREE, "hooks"), os.path.join(keep, "hooks"))
r = subprocess.run([sys.executable, os.path.join(keep, "bin", "check-locks")],
                   cwd=TREE, capture_output=True, text=True, timeout=60)
case("⑩ ⬜ no code at all → NOT MEASURED, not 199 findings",
     "NOT MEASURED" in r.stdout, "exit=%d" % r.returncode)
shutil.move(os.path.join(keep, "bin"), os.path.join(TREE, "bin"))
shutil.move(os.path.join(keep, "hooks"), os.path.join(TREE, "hooks"))
shutil.rmtree(keep, ignore_errors=True)

# ⭐ the real tree passes: every lock it declares is cited or delegated
r = run()
case("⑪ ⭐ the real tree has no unimplemented lock", r.returncode == 0,
     "exit=%d" % r.returncode)

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copy"))
sys.exit(0 if good == len(results) else 1)
