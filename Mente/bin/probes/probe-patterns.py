#!/usr/bin/env python3
"""probe-patterns — proves the catalogue is checked, and that the check knows its own limit.

⭐ THE CASE THAT MATTERS MOST IS ⑤. Without a PASSING example, a detector that
flags everything scores perfectly — ⛔ and a rule that always triggers is a rule
that gets disabled, taking the real findings with it. The failing example is the
half people write; the passing one is the half that keeps the rule usable.

⚠️ AND THE CHECK'S LIMIT IS TESTED TOO: it measures that a pattern is described
well enough to BE detected. ⛔ It does not detect the patterns themselves, and a
probe asserting otherwise would let the catalogue look enforced while nothing
scans any code.

Runs against an ISOLATED COPY: the cases edit the catalogue.
"""
import os, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-pat-")
TREE = os.path.join(WORK, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git", "cache"))
CAT = os.path.join(TREE, "memory", "principles", "imported-patterns.md")
ORIG = open(CAT, encoding="utf-8").read()


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def run(text=None):
    open(CAT, "w", encoding="utf-8").write(ORIG if text is None else text)
    return subprocess.run([sys.executable,
                           os.path.join(TREE, "bin", "check-patterns")],
                          cwd=TREE, capture_output=True, text=True, timeout=60)


print("═══ PROBE · check-patterns ═══\n")

# ── ⭐ the baseline · a correct catalogue must be silent ────────────────────
r = run()
case("① ⭐ the real catalogue is clean", r.returncode == 0,
     "exit=%d" % r.returncode)
case("② ⭐ and it says how many patterns and fields it measured",
     "pattern(s)" in r.stdout and "declared field(s)" in r.stdout)

# ── 🔴 PAT-FLD-001 · a declared field missing from an entry ─────────────────
r = run(ORIG.replace("- **Evidence:** file · line · the field it read · the "
                     "session field it should have read", "", 1))
case("③ 🔴 a declared field missing from a pattern → detected",
     r.returncode == 1 and "PAT-FLD-001" in r.stdout, "exit=%d" % r.returncode)

# ⬜ but `Policy` is the OWNER's — the engine cannot write it, and demanding it
# would force a default that is one installation's answer wearing engine
# authority.
r = run()
case("④ ⬜ `Policy` is exempt — no pattern has one and none is reported",
     "Policy" not in r.stdout and r.returncode == 0)

# ── ⭐ PAT-EXA-001 · THE PAIR, and the second half is the point ─────────────
r = run(ORIG.replace("- ⭐ **Passes:** `user = session.verified_user` → "
                     "`db.orders(user)`", "", 1))
case("⑤ ⭐⭐ a pattern with no PASSING example → detected",
     r.returncode == 1 and "PAT-EXA-001" in r.stdout, "exit=%d" % r.returncode)
case("⑥ ⭐ and it explains a detector flagging everything scores perfectly",
     "flags everything" in r.stdout)

r = run(ORIG.replace("- ⭐ **Fails:** `user = request.body.user_id` → "
                     "`db.orders(user)`", "", 1))
case("⑦ 🔴 a pattern with no FAILING example → detected",
     r.returncode == 1 and "PAT-EXA-001" in r.stdout, "exit=%d" % r.returncode)

# ── 🔴 PAT-IDS-001 · an id is an address ────────────────────────────────────
r = run(ORIG.replace("### FP-SEC-002", "### FP-SEC-001", 1))
case("⑧ 🔴 a repeated id → detected",
     r.returncode == 1 and "PAT-IDS-001" in r.stdout, "exit=%d" % r.returncode)

# ── ⭐ THE FIELDS COME FROM THE CONTRACT, not from a list in the code ───────
# ⛔ A copy in the code and a table in the document are two declarations that
# drift, and the document is the one people edit.
r = run(ORIG.replace("| **Severity** | how bad it is when present |",
                     "| **Severity** | how bad it is when present |\n"
                     "| **Zznew** | a field added to the contract |"))
case("⑨ ⭐ a field ADDED to the contract is demanded of every pattern",
     r.returncode == 1 and "Zznew" in r.stdout, "exit=%d" % r.returncode)

# ── ⬜ WHAT IT CANNOT SEE, IT SAYS ──────────────────────────────────────────
os.remove(CAT)
r = subprocess.run([sys.executable, os.path.join(TREE, "bin", "check-patterns")],
                   cwd=TREE, capture_output=True, text=True, timeout=60)
case("⑩ ⬜ no catalogue → NOT MEASURED, not a violation",
     r.returncode == 0 and "NOT MEASURED" in r.stdout, "exit=%d" % r.returncode)

r = run("# Patterns\n\nNothing here.\n")
case("⑪ 🔴 a catalogue with no contract table → exit 2, not a silent pass",
     r.returncode == 2, "exit=%d" % r.returncode)

# ── ⭐ CHK-QUI-001 ──────────────────────────────────────────────────────────
open(CAT, "w", encoding="utf-8").write(
    ORIG.replace("- ⭐ **Passes:** `user = session.verified_user` → "
                 "`db.orders(user)`", "", 1))
r = subprocess.run([sys.executable, os.path.join(TREE, "bin", "check-patterns"),
                    "--quiet"], cwd=TREE, capture_output=True, text=True,
                   timeout=60)
case("⑫ ⭐ --quiet prints nothing and still reports the failure",
     not r.stdout.strip() and r.returncode == 1, "exit=%d" % r.returncode)

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copy"))
sys.exit(0 if good == len(results) else 1)
