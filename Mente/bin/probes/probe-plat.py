#!/usr/bin/env python3
"""probe-plat — do the platform answers stay right when the platform lies?

🔴 THE GAP THIS CLOSES. On 2026-09-02 a clean Windows install reported 43
failures, every one false, and the battery here was 702 · 0 on the same commit.
⛔ Nothing in this engine measured what a DIFFERENT platform answers, so a
green battery said nothing about the only machine that was broken.

⭐ These cases do not plant a defect on disk — they replace the platform's
answer, which is the only way to reach behaviour this machine cannot produce.
⚠️ The three replaced behaviours were each MEASURED on Windows, never guessed:

  · `os.path.join` returns `\\` — so a built path never matches a declared one
  · `os.access(X_OK)` is true for every readable file — NTFS has no such bit
  · `os.chmod` on a directory is accepted and changes nothing
"""
import os, sys, ntpath
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                             # noqa: E402
sys.path.insert(0, os.path.join(ROOT, "Mente", "bin"))
sys.path.insert(0, os.path.join(ROOT, "bin"))
import plat                                          # noqa: E402

MENTE = os.path.join(ROOT, "Mente") if os.path.isdir(os.path.join(ROOT, "Mente")) else ROOT
ok_all = True
n = 0
bad = []


def case(label, got, want):
    global ok_all, n
    n += 1
    ok = got == want
    ok_all = ok_all and ok
    if not ok:
        bad.append(label)
    print("  %-52s %s %s" % (label, "✅" if ok else "🔴",
                             "" if ok else "got %r · want %r" % (got, want)))


print("═══ PLATFORM · plat ═══\n")

# ── ① the separator ──────────────────────────────────────────────────────
# ⭐ A path this engine COMPARES must read the same on every platform, because
# the tables it is compared against are written one way only.
_real = os.path.join
try:
    os.path.join = ntpath.join           # the platform now answers like Windows
    case("① plat.join under a `\\` platform", plat.join("bin", "check-block"),
         "bin/check-block")
finally:
    os.path.join = _real

# ⛔ The inverse: it must not mangle a path that was already correct.
case("② plat.join is idempotent here", plat.join("bin", "check-block"),
     "bin/check-block")

# ── ③④ the executable bit ────────────────────────────────────────────────
# ⚠️ Where the bit is not real, the shebang answers — and it must give the SAME
# verdict the bit gives here, or the two platforms disagree about what a
# command is.
# 🔴 THE BIT MUST BE FAKED TOO, not only the branch. Measured while writing
# this probe: forcing the branch alone left `os.access` telling the POSIX
# truth, so ③ passed against a plat.py sabotaged to use X_OK — ⛔ a case that
# goes green over broken code measures nothing. Windows answers YES for every
# readable file, and that is what is reproduced here.
_bit = plat.executable_bit_is_real
_access = os.access
try:
    plat.executable_bit_is_real = lambda: False
    os.access = lambda p, m: True        # ⭐ NTFS: everything looks runnable
    helpers = ["blockread.py", "findings.py", "scaffold.py", "tsvread.py",
               "utf8.py", "plat.py"]
    wrong = [h for h in helpers
             if plat.is_command(os.path.join(MENTE, "bin", h))]
    case("③ no helper is called a command", wrong, [])

    cmds = ["check-block", "check-document", "init", "new-block"]
    miss = [c for c in cmds
            if not plat.is_command(os.path.join(MENTE, "bin", c))]
    case("④ every command is still recognised", miss, [])
finally:
    plat.executable_bit_is_real = _bit
    os.access = _access

# ⭐ THE INVARIANT BEHIND ③④, checked over the whole tree: the shebang and the
# bit must agree everywhere. ⛔ If they ever diverge, the Windows answer stops
# being the POSIX answer and both cases above go green while lying.
if plat.executable_bit_is_real():
    dis = []
    for d in ("bin", "hooks", os.path.join("bin", "probes")):
        full = os.path.join(MENTE, d)
        if not os.path.isdir(full):
            continue
        for name in sorted(os.listdir(full)):
            f = os.path.join(full, name)
            if not os.path.isfile(f) or name.endswith(".md"):
                continue
            try:
                sb = open(f, "rb").read(2) == b"#!"
            except OSError:
                continue      # ⬜ unreadable · counted nowhere, not as agreement
            if os.access(f, os.X_OK) != sb:
                dis.append(os.path.relpath(f, MENTE))
    case("⑤ shebang and executable bit agree everywhere", dis, [])
else:
    print("  ⑤ shebang vs bit                                     "
          "⬜ NOT MEASURED · this platform has no executable bit")

# ── ⑥⑦ the modes ─────────────────────────────────────────────────────────
# 🔴 The one that matters: where chmod decides nothing, the answer is ⬜ —
# never a pass (a false assurance about credentials) and never a 🔴 (a false
# alarm that gets the check switched off).
_modes = plat.modes_are_real
try:
    plat.modes_are_real = lambda: False
    case("⑥ privacy is ⬜ where chmod decides nothing",
         plat.privacy(os.path.join(MENTE, "secrets"))[0], "unknown")
finally:
    plat.modes_are_real = _modes

# ⛔ And an absent folder is never reported private.
case("⑦ a folder that is not there is not private",
     plat.privacy(os.path.join(MENTE, "no-such-folder-zzprobe"))[0], "unknown")

# ⭐ THE TALLY LINE run-all.py PARSES, in its exact wording. ⛔ Measured while
# writing this probe: a tally in this probe's own phrasing was read as a CRASH
# — correctly, because a probe that never reports a tally is indistinguishable
# from one that died before its last line.
# ⚠️ `leftovers` is stated too: this probe plants nothing on disk, and silence
# about residue is not the same as none.
# ── ⑧⑨⑩⑪ invoking this engine's own scripts ─────────────────────────────
# 🔴 An external audit installed this on Windows and found gate-critical and
# gate-secrets DEAD: both ran an extensionless Python script by bare path, and
# CreateProcess does not read shebangs. Neither said a word.
case("⑧ a shebang script is run by THIS interpreter",
     plat.script(os.path.join(MENTE, "bin", "check-block"), "--quiet"),
     [sys.executable, os.path.join(MENTE, "bin", "check-block"), "--quiet"])
case("⑨ a .sh goes through bash, not the OS",
     plat.script(os.path.join(MENTE, "hooks", "pre-push.sh"))[0], "bash")
# ⭐ THE INVARIANT: no production call may hand the OS a bare engine script.
# ⛔ Four sites did, and each failed in the direction that lets work through.
import ast as _ast
import glob as _glob
raw = []
for _f in sorted(_glob.glob(os.path.join(MENTE, "hooks", "*.py"))
                 + [q for q in _glob.glob(os.path.join(MENTE, "bin", "*"))
                    if os.path.isfile(q) and not q.endswith(".md")]):
    try:
        _t = open(_f, encoding="utf-8", errors="replace").read()
    except OSError:
        continue          # ⬜ unreadable · reported nowhere as agreement
    # ⭐ Read the CODE, never the text. ⛔ A grep over lines flagged two
    # comments that quote the broken call to explain it — a probe that cannot
    # tell code from prose reports the fix as the defect.
    try:
        _tree = _ast.parse(_t)
    except SyntaxError:
        continue          # ⬜ not Python · nothing measured here, said below
    for _nd in _ast.walk(_tree):
        if not (isinstance(_nd, _ast.Call)
                and isinstance(_nd.func, _ast.Attribute)
                and _nd.func.attr == "run"
                and isinstance(_nd.func.value, _ast.Name)
                and _nd.func.value.id == "subprocess"):
            continue
        if not (_nd.args and isinstance(_nd.args[0], _ast.List)
                and _nd.args[0].elts):
            continue      # ⬜ a string argv is shell=True's business, not this
        _first = _nd.args[0].elts[0]
        # ⭐ Accepted heads: sys.executable, plat.script(...), or a literal
        # command the OS genuinely knows how to start.
        if isinstance(_first, _ast.Attribute) and _first.attr == "executable":
            continue
        if isinstance(_first, _ast.Constant) and _first.value in (
                "git", "bash", "sh"):
            continue
        if (isinstance(_nd.args[0], _ast.List) and len(_nd.args[0].elts) == 1
                and isinstance(_first, _ast.Starred)):
            continue
        raw.append("%s:%d" % (plat.rel(_f, MENTE), _nd.lineno))
case("⑩ no engine script is run by bare path", raw, [])

# 🔴 shell=True is `cmd.exe /c` on Windows and `/bin/sh -c` elsewhere — two
# languages for one string. The watcher's `; exit 1` convention returned 0
# there, so it reported "nothing new" forever.
case("⑪ an owner's shell command runs under bash",
     plat.shell("echo hi; exit 1"), ["bash", "-c", "echo hi; exit 1"])

# ── ⑫⑬ deleting a tree git has written into ─────────────────────────────
# 🔴 git writes .git/objects/** at 0o444. On POSIX the directory's mode decides
# and they go anyway; on Windows a read-only file cannot be removed, and
# ignore_errors=True gave up in silence — a whole repo left in %TEMP%, per run.
import subprocess as _sp, tempfile as _tf
_d = _tf.mkdtemp(prefix="zzprobe-rm-")
_r = os.path.join(_d, "repo"); os.makedirs(_r)
for _c in (["git", "init", "-q"], ["git", "config", "user.email", "a@b.c"],
           ["git", "config", "user.name", "a"]):
    _sp.run(_c, cwd=_r, capture_output=True)
open(os.path.join(_r, "f.txt"), "w").write("x")
_sp.run(["git", "add", "-A"], cwd=_r, capture_output=True)
_sp.run(["git", "-c", "commit.gpgsign=false", "commit", "-qm", "x"],
        cwd=_r, capture_output=True)
# ⭐ The precondition, asserted: without a read-only object there is nothing
# to prove, and the case would pass over a tree that never had the problem.
_ro = [1 for _root, _, _fs in os.walk(os.path.join(_r, ".git", "objects"))
       for _n in _fs
       if not os.stat(os.path.join(_root, _n)).st_mode & 0o200]
case("⑫ git really wrote read-only objects", bool(_ro), True)

# 🔴 THE DELETE MUST BE MADE TO FAIL, not merely attempted. On POSIX the
# directory's mode decides, so a read-only file is removed even with no retry
# at all — measured while writing this: ⑬ passed against a plat.rmtree whose
# retry was gutted. ⛔ A case that goes green over broken code measures
# nothing. Windows refuses the unlink itself, and that is reproduced here.
_real_unlink = os.unlink
def _nt_unlink(_p, *a, **k):
    """⭐ Refuse exactly what Windows refuses: unlinking a read-only file.

    ⚠️ `shutil.rmtree` calls `os.unlink(name, dir_fd=...)` with a RELATIVE
    name, so the mode has to be read through that same descriptor — measured:
    stat-ing the bare name looked at the wrong file and the simulation never
    fired, leaving ⑬ green over a gutted retry.
    """
    try:
        _st = os.stat(_p, dir_fd=k.get("dir_fd"), follow_symlinks=False)
        _writable = _st.st_mode & 0o200
    except (OSError, TypeError, ValueError):
        _writable = True          # ⬜ cannot tell · never invents a refusal
    if not _writable:
        raise PermissionError(13, "read-only (simulated NT)", str(_p))
    return _real_unlink(_p, *a, **k)
try:
    os.unlink = _nt_unlink
    _gone = plat.rmtree(_d)
finally:
    os.unlink = _real_unlink
case("⑬ plat.rmtree removes them where NT would refuse", _gone, True)
if os.path.exists(_d):
    import shutil as _sh; _sh.rmtree(_d, ignore_errors=True)

print("\n  leftovers: none")
print("  ➜ %d of %d correct" % (n - len(bad), n))
sys.exit(0 if ok_all else 1)
