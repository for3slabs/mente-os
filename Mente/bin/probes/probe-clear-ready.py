#!/usr/bin/env python3
"""probe-clear-ready — proves the cut is refused while something would be lost.

⭐ THE HARD PART IS NOT DETECTING UNCOMMITTED WORK. It is refusing to say "safe"
when the check could not look: a context reset is irreversible, and a green over
an unmeasured tree is the one answer that costs the work.

⚠️ Runs against ISOLATED throwaway repositories — the subject is git state, and
measuring the real tree would make the result depend on whatever is in flight.
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
WORK = tempfile.mkdtemp(prefix="mente-clear-")


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def git(*a, cwd):
    return subprocess.run(("git",) + a, cwd=cwd, capture_output=True, text=True)


def make_repo(name, with_git=True):
    """A tree with Mente/ inside it, the shape the checker expects."""
    repo = os.path.join(WORK, name)
    tree = os.path.join(repo, "Mente")
    shutil.copytree(ROOT, tree, ignore=shutil.ignore_patterns(
        "__pycache__", ".beats", ".test-lock", ".git", "work"))
    os.makedirs(os.path.join(tree, "work", "blocks"), exist_ok=True)
    cfg = os.path.join(tree, "mente.config.yml")
    if os.path.exists(cfg):
        os.remove(cfg)
    if with_git:
        git("init", "-q", cwd=repo)
        git("config", "user.email", "probe@example.invalid", cwd=repo)
        git("config", "user.name", "probe", cwd=repo)
        git("add", "-A", cwd=repo)
        git("-c", "commit.gpgsign=false", "commit", "-qm", "base", cwd=repo)
    return repo, tree


def run(tree, **env):
    return subprocess.run(
        [sys.executable, os.path.join(tree, "bin", "check-clear-ready")],
        cwd=tree, capture_output=True, text=True,
        env=dict(os.environ, **env))


print("═══ SONDA · check-clear-ready ═══\n")

# ① ⭐ a clean tree is safe to cut — the baseline every other case depends on
repo, tree = make_repo("clean")
r = run(tree)
case("① ⭐ a clean tree → safe to cut", r.returncode == 0,
     "exit=%d" % r.returncode)

# ② 🔴 THE DEFECT IT EXISTS FOR · an edit that only exists as an edit
open(os.path.join(tree, "README.md"), "a").write("\nan unsaved thought\n")
r = run(tree)
case("② 🔴 an uncommitted change → it refuses", r.returncode == 1,
     "exit=%d" % r.returncode)

# ③ ⭐ and it says WHAT would be lost, not just that something would
case("③ ⭐ it names the file, not just the count", "README.md" in r.stdout)

# ④ ⛔ and it says the reasoning is the loss, not the file
case("④ ⛔ it explains the WHY is lost, not the file",
     "WHY they changed" in r.stdout)

# ⑤ ⭐ committed → the edit is no longer at risk
git("add", "-A", cwd=repo)
git("-c", "commit.gpgsign=false", "commit", "-qm", "saved", cwd=repo)
r = run(tree)
case("⑤ ⭐ once committed, that risk is gone",
     r.returncode == 0 and "🔴" not in r.stdout, "exit=%d" % r.returncode)

# ⛔ AND THE GREEN MUST NOT CLAIM WHAT WAS NOT MEASURED. The first version
# printed "nothing unpushed" directly above a gap saying pushing was NOT
# measured — ⚠️ two contradictory statements in one output, and a reader who
# stops at the ✅ acts on the wrong one.
case("⑤b ⛔ with gaps, it does NOT declare a clean ✅",
     "not a clean bill" in r.stdout or "✅" not in r.stdout)

# ── ⚠️ AN OPEN BLOCK IS SEEN BEFORE THE CUT ────────────────────────────────
# ⛔ Not a refusal for its own sake — work legitimately spans sessions. But
# after the cut the only record is the file, and the file does not say what was
# about to happen.
bd = os.path.join(tree, "work", "blocks", "zzprobe-open")
os.makedirs(bd, exist_ok=True)
open(os.path.join(bd, "BLOCK.md"), "w").write(
    "# BLOCK\n\n## A · Identity\n\nid: zzprobe-open\nstatus: active\n")
r = run(tree)
case("⑥ ⚠️ an open block is SEEN before the cut",
     r.returncode == 1 and "still open" in r.stdout, "exit=%d" % r.returncode)
shutil.rmtree(bd)

# ── 🔴 UNPUSHED WORK · one machine away from being the only copy ────────────
bare = os.path.join(WORK, "remote.git")
git("init", "--bare", "-q", bare, cwd=WORK)
git("remote", "add", "origin", bare, cwd=repo)
git("push", "-q", "-u", "origin", "HEAD", cwd=repo)
r = run(tree)
case("⑦ ⭐ everything pushed → no risk", "not been pushed" not in r.stdout)

open(os.path.join(tree, "README.md"), "a").write("\nmore\n")
git("add", "-A", cwd=repo)
git("-c", "commit.gpgsign=false", "commit", "-qm", "local only", cwd=repo)
r = run(tree)
case("⑧ 🔴 a commit that never left → detected",
     r.returncode == 1 and "not been pushed" in r.stdout, "exit=%d" % r.returncode)

# ── ⛔ THE HARDEST REQUIREMENT · never "safe" over what could not be measured ─
nrepo, ntree = make_repo("nogit", with_git=False)
r = run(ntree)
case("⑨ ⛔ no repository → it says it did NOT measure, not that it is safe",
     "NOT MEASURED" in r.stdout)
case("⑩ ⛔ and any ✅ carries the number of gaps",
     "✅" not in r.stdout or "gap(s)" in r.stdout)

# ⬜ siblings · declared, never guessed
r = run(ntree)
case("⑪ ⬜ with no siblings declared it says so · it does not assume that is all",
     "only this tree was measured" in r.stdout)

cfg = os.path.join(ntree, "mente.config.yml")
open(cfg, "w").write('siblings:\n  - "nowhere-at-all"\n')
r = run(ntree)
case("⑫ ⬜ a declared sibling that does not exist → a named gap",
     "does not exist" in r.stdout)

# ⭐ a REAL sibling with uncommitted work is caught too
sib, _ = make_repo("neighbour")
open(cfg, "w").write('siblings:\n  - "neighbour"\n')
open(os.path.join(sib, "loose.txt"), "w").write("x\n")
r = run(ntree)
case("⑬ ⭐ loose work in a declared sibling → detected",
     "neighbour" in r.stdout, "exit=%d" % r.returncode)

# ── ⛔ robustness ───────────────────────────────────────────────────────────
open(cfg, "wb").write(b"\xff\xfe\x00")
r = run(ntree)
case("⑭ ⛔ an unreadable configuration does not crash the check",
     "Traceback" not in r.stderr)

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
