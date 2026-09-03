#!/usr/bin/env python3
"""probe-connect-account — proves the registry can be CONSULTED, and never guesses.

⭐ THE PIECE THAT VERIFIES A REGISTRY IS NOT THE PIECE THAT ANSWERS FROM IT.
check-accounts reports what is wrong with the table; nothing read the fact it
holds. ⛔ So the fact was readable only by opening the file and matching rows by
eye — and a person matching by eye is a FOURTH place the truth lives, which is
the drift the registry exists to end.

⚠️ AND THE HARDEST REQUIREMENT IS THAT IT NEVER GUESSES. An answer about which
account may push is acted on immediately; a confident wrong one sends work to
the wrong place, and the push succeeds.

⬜ Bounded by ADR-031: the host's tool is READ for this clone's remotes, never
written and never reached over the network.
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
WORK = tempfile.mkdtemp(prefix="mente-conn-")
TREE = os.path.join(WORK, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git", "cache"))
TOOL = os.path.join(TREE, "bin", "connect-account")
HEAD = "repo\tcuenta\trol\tremoto\truta_local\tpor_que_existe\tguia\n"


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


_seq = [0]


def registry(*rows):
    """A registry file per call.

    🔴 The first version reused ONE path, so a later case silently rewrote the
    file an earlier variable still pointed at — and four cases then measured a
    registry that no longer held what they planted. ⛔ A fixture shared between
    cases makes the ORDER of the cases part of the result, which is the one
    thing a probe must never depend on.
    """
    _seq[0] += 1
    p = os.path.join(WORK, "accounts-%d.tsv" % _seq[0])
    open(p, "w", encoding="utf-8").write(HEAD + "".join(r + "\n" for r in rows))
    return p


def run(*args, reg=None, cwd=None):
    e = dict(os.environ)
    if reg:
        e["MENTE_ACCOUNTS"] = reg
    return subprocess.run([sys.executable, TOOL] + list(args),
                          cwd=cwd or TREE, capture_output=True, text=True,
                          timeout=30, env=e)


LIVE = "an-org/live\tan-account\ttaller\torigin\t-\tthe working repo\t-"
DEAD = "an-org/dead\tan-account\tarchivado\told\t-\tretired after a leak\t-"

print("═══ PROBE · connect-account ═══\n")

# ── ⭐ IT ANSWERS THE QUESTION ──────────────────────────────────────────────
reg = registry(LIVE, DEAD)
r = run("an-org/live", reg=reg)
case("① ⭐ names the governing account", r.returncode == 0
     and "an-account" in r.stdout, "exit=%d" % r.returncode)
case("② ⭐ and why the repository exists at all",
     "the working repo" in r.stdout)

# ⛔ A retired repository is NAMED as retired: it stays declared on purpose, and
# an answer that omits that sends work to a repo the system already buried.
r = run("an-org/dead", reg=reg)
case("③ ⛔ a RETIRED repo says so in the answer", "RETIRED" in r.stdout)

# ── ⭐ THE POINTER, NEVER THE CONTENT ───────────────────────────────────────
# ⛔ Printing the guide would put access steps into a terminal and a transcript —
# the exact move secrets/ exists to prevent, made by the tool meant to respect it.
os.makedirs(os.path.join(TREE, "secrets"), exist_ok=True)
open(os.path.join(TREE, "secrets", "zzguide.md"), "w").write(
    "STEP ONE: the secret value is hunter2\n")
reg2 = registry(LIVE.replace("\t-\n", "\t-") + "",
                "an-org/g\tan-account\ttaller\t-\t-\twith a guide\tsecrets/zzguide.md")
r = run("an-org/g", reg=reg2)
case("④ ⛔ it prints the guide's PATH, never its content",
     "secrets/zzguide.md" in r.stdout and "hunter2" not in r.stdout)

# ⚠️ A guide declared and absent is a pointer resolving to nothing — reported,
# because a reader sent to a missing file concludes the access is lost.
reg3 = registry("an-org/x\tan-account\ttaller\t-\t-\twhy\tsecrets/nowhere.md")
r = run("an-org/x", reg=reg3)
case("⑤ ⚠️ a guide declared and NOT FOUND is reported",
     "NOT FOUND" in r.stdout)

# ── 🔴 IT NEVER GUESSES ─────────────────────────────────────────────────────
r = run("nope", reg=reg)
case("⑥ 🔴 an undeclared repository → refused, not guessed",
     r.returncode == 1 and "not declared" in r.stderr, "exit=%d" % r.returncode)

# ⛔ Two rows whose tail matches must not be resolved to whichever came first:
# an answer about which account may push is acted on immediately.
reg4 = registry("org-a/api\tacct-a\ttaller\t-\t-\tfirst\t-",
                "org-b/api\tacct-b\ttaller\t-\t-\tsecond\t-")
r = run("api", reg=reg4)
case("⑦ 🔴 an AMBIGUOUS name → refused, it does not pick one",
     r.returncode == 1 and "name it in full" in r.stderr,
     "exit=%d" % r.returncode)

# ⭐ but an exact name still resolves when a tail would be ambiguous
r = run("org-b/api", reg=reg4)
case("⑧ ⭐ the full name still resolves", r.returncode == 0
     and "acct-b" in r.stdout)

# ── ⭐ THE COMPARISON THE REGISTRY'S CONTRACT ASKS FOR ──────────────────────
# A row is a claim until it is measured against the machine.
repo = os.path.join(WORK, "clone")
os.makedirs(repo)
subprocess.run(["git", "init", "-q"], cwd=repo, capture_output=True)
subprocess.run(["git", "remote", "add", "origin",
                "https://host/an-org/live.git"], cwd=repo, capture_output=True)
tree2 = os.path.join(repo, "Mente")
shutil.copytree(TREE, tree2, ignore=shutil.ignore_patterns("__pycache__"))
r = subprocess.run([sys.executable, os.path.join(tree2, "bin", "connect-account")],
                   cwd=tree2, capture_output=True, text=True, timeout=30,
                   env=dict(os.environ, MENTE_ACCOUNTS=reg))
case("⑨ ⭐ with no argument it answers for THIS clone, via its remotes",
     r.returncode == 0 and "an-org/live" in r.stdout, "exit=%d" % r.returncode)
case("⑩ ⭐ and confirms the declared remote matches the real one",
     "✅ `origin`" in r.stdout)

# 🔴 THE DRIFT THE REGISTRY EXISTS TO CATCH: the row and the machine disagree.
reg5 = registry("an-org/renamed\tan-account\ttaller\torigin\t-\twhy\t-")
r = subprocess.run([sys.executable, os.path.join(tree2, "bin", "connect-account"),
                    "an-org/renamed"], cwd=tree2, capture_output=True,
                   text=True, timeout=30,
                   env=dict(os.environ, MENTE_ACCOUNTS=reg5))
case("⑪ 🔴 declared repo ≠ real remote → reported",
     "disagree" in r.stdout)
case("⑫ ⭐ and it explains a redirect makes both look alive",
     "both look alive" in r.stdout)

# ⚠️ A declared remote this clone does not have describes ANOTHER clone.
r = subprocess.run([sys.executable, os.path.join(tree2, "bin", "connect-account"),
                    "an-org/dead"], cwd=tree2, capture_output=True, text=True,
                   timeout=30, env=dict(os.environ, MENTE_ACCOUNTS=reg))
case("⑬ ⚠️ a remote this clone lacks → says the row is another clone's",
     "not this one" in r.stdout)

# ── ⬜ WHAT IT CANNOT SEE, IT SAYS ──────────────────────────────────────────
r = run("--list", reg=registry())
case("⑭ ⬜ an empty registry → says a clone starts empty, not «none governs»",
     r.returncode == 1 and "starts empty" in r.stdout, "exit=%d" % r.returncode)

r = run(reg="/nowhere/none.tsv")
case("⑮ ⬜ no registry at all → exit 2 and points at bin/init",
     r.returncode == 2 and "bin/init" in r.stderr, "exit=%d" % r.returncode)

# ⬜ ADR-031 · outside a repository the tool cannot answer, and that is a GAP.
r = run(reg=reg, cwd=WORK)
case("⑯ ⬜ ADR-031 · no tool answer → NOT MEASURED, never a wrong answer",
     "NOT MEASURED" in r.stdout or "none of the" in r.stderr,
     "exit=%d" % r.returncode)

# ⛔ robustness
open(os.path.join(WORK, "bad.tsv"), "wb").write(b"\xff\xfe not text\n")
r = run("x", reg=os.path.join(WORK, "bad.tsv"))
case("⑰ ⛔ an unreadable registry does not crash it",
     "Traceback" not in r.stderr)

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copy"))
sys.exit(0 if good == len(results) else 1)
