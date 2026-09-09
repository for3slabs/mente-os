#!/usr/bin/env python3
"""probe-update-engine — the command that brings a newer engine in safely.

⛔ EVERY CASE HERE IS A DEFECT THAT WAS REAL. This command was written, tried
on a live installation, and got the answer WRONG four times before it was
right — each time in the direction that loses the person's work while
reporting success. That is why the cases below assert what is LEFT ALONE at
least as hard as what is taken.
"""
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
import plat                                          # noqa: E402
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                              # noqa: E402

WORK = tempfile.mkdtemp(prefix="mente-upd-")
results = []


def case(label, ok, detail=""):
    results.append((label, ok))
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))


def git(where, *a):
    return subprocess.run(("git",) + a, cwd=where, capture_output=True,
                          text=True, timeout=120)


def commit(where, msg):
    git(where, "add", "-A")
    git(where, "-c", "user.email=t@t", "-c", "user.name=t",
        "commit", "-q", "--no-verify", "-m", msg)


def engine():
    """A bare repository standing in for the published engine.

    ⚠️ Local, never the network: a probe that reaches the network measures the
    network. ⭐ It carries a real Mente/ tree so the .gitignore under test is
    the engine's own.
    """
    src = os.path.join(WORK, "engine-src")
    os.makedirs(src, exist_ok=True)
    shutil.copytree(ROOT, os.path.join(src, "Mente"),
                    ignore=shutil.ignore_patterns("__pycache__", ".beats",
                                                  ".git", "cache"))
    git(src, "init", "-q", ".")
    commit(src, "engine v1")
    # ⭐ A change in the ENGINE half and a template in the INSTANCE half, so
    # both halves of the question have something to measure.
    with open(os.path.join(src, "Mente", "bin", "zzprobe-new"), "w",
              encoding="utf-8", newline="") as fh:
        fh.write("#!/usr/bin/env python3\n")
    os.makedirs(os.path.join(src, "Mente", "memory"), exist_ok=True)
    with open(os.path.join(src, "Mente", "memory", "RESUME.md"), "w",
              encoding="utf-8", newline="") as fh:
        fh.write("THE ENGINE'S TEMPLATE\n")
    with open(os.path.join(src, "Mente", "memory", "principles",
                           "owner-0-voice.md"), "w",
              encoding="utf-8", newline="") as fh:
        fh.write("THE ENGINE'S NEWER VOICE\n")
    # ⛔ FORCED IN. 🔴 The engine's own .gitignore excludes memory/*, so a plain
    # `git add` never published these — and case ③ then measured a defect that
    # could not happen, staying green against a command that overwrote
    # everything. ⭐ A real published engine DOES carry the instance's shapes
    # as templates in templates/, and an installation that versioned its memory
    # carries the filled ones; either way the collision is real, and the
    # fixture has to be able to produce it.
    git(src, "add", "-f", "Mente/memory/RESUME.md",
        "Mente/memory/principles/owner-0-voice.md")
    commit(src, "engine v2")
    bare = os.path.join(WORK, "engine.git")
    subprocess.run(("git", "clone", "-q", "--bare", src, bare),
                   capture_output=True, text=True)
    return bare


def user(bare, related):
    """An installation. `related` decides whether it shares a root with the
    engine — which is the whole point: the person who does the CORRECT thing
    and replaces the clone's history is the one a merge cannot serve."""
    d = os.path.join(WORK, "user-%s" % ("related" if related else "own"))
    if related:
        subprocess.run(("git", "clone", "-q", bare, d),
                       capture_output=True, text=True)
        git(d, "reset", "-q", "--hard", "HEAD~1")
    else:
        os.makedirs(d, exist_ok=True)
        shutil.copytree(ROOT, os.path.join(d, "Mente"),
                        ignore=shutil.ignore_patterns("__pycache__", ".beats",
                                                      ".git", "cache"))
        git(d, "init", "-q", ".")
        commit(d, "their own history")
    git(d, "remote", "add", "upstream", bare)
    git(d, "fetch", "-q", "upstream")
    # ⭐ Their memory, marked so it can be recognised after the update.
    os.makedirs(os.path.join(d, "Mente", "memory"), exist_ok=True)
    for rel, body in ((("memory", "RESUME.md"), "THEIR REAL MEMORY\n"),
                      (("mente.config.yml",), 'owner:\n  name: "Them"\n')):
        with open(os.path.join(d, "Mente", *rel), "w",
                  encoding="utf-8", newline="") as fh:
            fh.write(body)
    # ⛔ TRACKED, and that is the condition the whole `--no-index` flag exists
    # for. 🔴 Measured 2026-09-08: without this the memory stays untracked, git
    # reports it ignored either way, and removing `--no-index` left case ③
    # green — while on a real installation, which DOES version its memory,
    # the same removal would overwrite every instance file. ⭐ Since bin/init
    # now versions the memory by default, tracked is the normal state.
    git(d, "add", "-f", "Mente/memory/RESUME.md", "Mente/mente.config.yml")
    commit(d, "their memory")
    return d


def run(d, *a):
    return subprocess.run(
        [sys.executable, os.path.join(d, "Mente", "bin", "update-engine")]
        + list(a), cwd=os.path.join(d, "Mente"), capture_output=True,
        text=True, timeout=180)


def read(d, *rel):
    p = os.path.join(d, "Mente", *rel)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


print("═══ SONDA · update-engine ═══\n")
_bare = engine()
_u = user(_bare, related=False)

# ── ⓪ ⛔ THE FIXTURE ITSELF IS MEASURED FIRST ──────────────────────────────
# 🔴 Measured 2026-09-08: sabotage that reverted this command to overwriting
# all of Mente/ left case ③ GREEN — because the fake engine's `.gitignore`
# stopped its own RESUME.md from ever reaching the published tree, so there was
# nothing to overwrite WITH. ⛔ A probe whose fixture cannot express the defect
# reports the code as safe for a reason that has nothing to do with the code.
# ⭐ So the setup is asserted before anything is concluded from it.
# ⚠️ THE BRANCH IS ASKED FOR, and this probe got it wrong the same way the
# check did. 🔴 A bare clone of a local repository carries no
# refs/remotes/upstream/HEAD, and `git init` here produces `master` — so
# `upstream/main` resolved to nothing and the assertion read "0 files
# published" about a tree holding 203. ⭐ The same three candidates the command
# itself tries.
_ref = next((c for c in
             (git(_u, "symbolic-ref", "--short",
                  "refs/remotes/upstream/HEAD").stdout.strip(),
              "upstream/main", "upstream/master")
             if c and git(_u, "rev-parse", "--verify", "--quiet",
                          c).returncode == 0), "upstream/main")
_pub = git(_u, "ls-tree", "-r", "--name-only", _ref, "Mente/").stdout.split()
print("     (fixture: ref=%s · %d file(s) published)" % (_ref, len(_pub)))
case("⓪ ⛔ the fake engine really SHIPS a RESUME.md to overwrite with",
     "Mente/memory/RESUME.md" in _pub,
     "" if "Mente/memory/RESUME.md" in _pub
     else "🔴 the fixture cannot express the defect")

# ── ① THE DRY RUN WRITES NOTHING ───────────────────────────────────────────
_before = read(_u, "memory", "RESUME.md")
r = run(_u, "--dry-run")
case("① ⭐ --dry-run reports and writes NOTHING",
     r.returncode == 0 and "dry run" in r.stdout
     and read(_u, "memory", "RESUME.md") == _before)

# ── ② 🔴 IT TAKES THE ENGINE ───────────────────────────────────────────────
r = run(_u)
case("② ⭐ it updates and exits clean", r.returncode == 0,
     "exit=%d" % r.returncode)
case("②b ⭐ a NEW engine file arrives",
     os.path.exists(os.path.join(_u, "Mente", "bin", "zzprobe-new")))

# ── ③ 🔴 AND IT LEAVES THE INSTANCE ALONE — the half that was wrong twice ──
# 🔴 Measured on a real install: `git checkout <ref> -- Mente/` replaced a
# RESUME.md holding real memory with the engine's template, in silence. ⛔ A
# command that loses the memory this system exists to keep is not an update.
case("③ 🔴 ⭐ THEIR memory is NOT overwritten",
     read(_u, "memory", "RESUME.md").strip() == "THEIR REAL MEMORY",
     read(_u, "memory", "RESUME.md").strip()[:40])
case("③b 🔴 ⭐ and neither is their config",
     'name: "Them"' in read(_u, "mente.config.yml"))

# ── ④ 🔴 BUT ENGINE DOCTRINE INSIDE AN IGNORED FOLDER DOES ARRIVE ──────────
# 🔴 Measured the first time this ran: a hand-written parse of .gitignore that
# skipped `!` lines held back 23 files — the voice, the three architects, the
# seven disciplines. ⛔ Those are marked `!` precisely because they ship, so
# nobody would ever have received an improvement to the voice, and the command
# would have reported success while doing it.
case("④ 🔴 ⭐ a `!` file IS taken — the voice is engine doctrine",
     "NEWER VOICE" in read(_u, "memory", "principles", "owner-0-voice.md"),
     read(_u, "memory", "principles", "owner-0-voice.md").strip()[:34])

# ── ⑤ ⛔ A DIRTY TREE IS REFUSED ───────────────────────────────────────────
with open(os.path.join(_u, "Mente", "memory", "RESUME.md"), "a",
          encoding="utf-8", newline="") as fh:
    fh.write("uncommitted\n")
r = run(_u)
case("⑤ ⛔ uncommitted work is REFUSED, never overwritten",
     r.returncode == 1 and "uncommitted" in (r.stdout + r.stderr))
commit(_u, "wip")

# ── ⑥ ALREADY CURRENT SAYS SO ──────────────────────────────────────────────
r = run(_u)
case("⑥ ⭐ run twice → says it is current, does nothing",
     "already current" in r.stdout and r.returncode == 0)

# ── ⑦ ⬜ NO upstream · it says so, it does not crash ───────────────────────
_no = os.path.join(WORK, "no-remote")
os.makedirs(_no, exist_ok=True)
shutil.copytree(ROOT, os.path.join(_no, "Mente"),
                ignore=shutil.ignore_patterns("__pycache__", ".beats", ".git",
                                              "cache"))
git(_no, "init", "-q", ".")
commit(_no, "x")
r = run(_no)
case("⑦ ⬜ no `upstream` → it says how to wire it, exit 1",
     r.returncode == 1 and "upstream" in (r.stdout + r.stderr))

# ── ⑧ IT ALSO WORKS FOR A TREE THAT DID KEEP ITS HISTORY ───────────────────
# ⚠️ The related case is the easy one and still has to pass: a command that
# only serves the broken tree is a second path nobody maintains.
_r2 = user(_bare, related=True)
r = run(_r2)
case("⑧ ⭐ a tree that kept its clone history updates too",
     r.returncode == 0 and os.path.exists(
         os.path.join(_r2, "Mente", "bin", "zzprobe-new")),
     "exit=%d" % r.returncode)
case("⑧b 🔴 ⭐ and its memory is left alone as well",
     read(_r2, "memory", "RESUME.md").strip() == "THEIR REAL MEMORY")

# ── ⑨ 🔴 THE `-z` FLAG, MEASURED — not assumed to be a Windows-only story ───
# 🔴 THE FAILURE it prevents, measured by hand on a real Windows install:
# `text=True` makes Python translate "\n" to "\r\n" on the way into a child's
# stdin, so git reads `Mente/bin/init\r` as a path of its own, answers about
# only the first line, and QUOTES every path it echoes back —
# `"Mente/memory/RESUME.md\r"`. Three defects from one missing flag, and all
# three read as "nothing here is yours", one keystroke from overwriting every
# instance file.
# ⛔ IT WAS REPORTED ⬜ NOT MEASURED "because it is a Windows path". That was
# wrong: the defect is CRLF ON STDIN, and nothing stops a probe from writing
# CRLF deliberately. ⚠️ A platform is not an excuse — the INPUT is what the
# check needs, and the input can be produced anywhere.
_zt = os.path.join(WORK, "zflag")
os.makedirs(os.path.join(_zt, "Mente", "memory"), exist_ok=True)
os.makedirs(os.path.join(_zt, "Mente", "bin"), exist_ok=True)
with open(os.path.join(_zt, "Mente", ".gitignore"), "w",
          encoding="utf-8", newline="") as fh:
    fh.write("memory/*\n!memory/README.md\n")
for _f in (("memory", "RESUME.md"), ("bin", "init")):
    with open(os.path.join(_zt, "Mente", *_f), "w",
              encoding="utf-8", newline="") as fh:
        fh.write("x\n")
git(_zt, "init", "-q", ".")
_paths = ["Mente/memory/RESUME.md", "Mente/bin/init"]


def _ask(sep, extra):
    r = subprocess.run(("git", "check-ignore", "--no-index") + extra
                       + ("--stdin",), cwd=_zt, input=sep.join(_paths),
                       capture_output=True, text=True, timeout=60)
    return r.stdout


# ⭐ THE DEFECT REPRODUCED: CRLF in, and git answers about one path and quotes
# it. This is the exact shape Windows produces without anyone asking for it.
_crlf = _ask("\r\n", ())
case("⑨ 🔴 ⭐ CRLF on stdin really does break the pairing",
     '"' in _crlf and "\\r" in _crlf and _crlf.count("\n") == 1,
     repr(_crlf)[:52])

# ⛔ AND `-z` IS WHAT SURVIVES IT: NUL cannot be translated, so neither side of
# the exchange can be reshaped by a platform's line-ending rules.
_z = _ask("\0", ("-z",))
case("⑨b ⛔ and `-z` answers cleanly, with no quoting",
     _z.split("\0")[0] == "Mente/memory/RESUME.md" and '"' not in _z,
     repr(_z)[:52])

# ⚠️ THE HALF THAT MATTERS: the command under test must be the one using it. A
# probe that proves a flag works while the code omits it has measured git.
_src = open(os.path.join(ROOT, "bin", "update-engine"),
            encoding="utf-8").read()
case("⑨c ⭐ and update-engine actually passes `-z`",
     '"-z"' in _src and '"--no-index"' in _src)

plat.rmtree(WORK)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copy"))
sys.exit(0 if good == len(results) else 1)
