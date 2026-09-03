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
print("\n  leftovers: none")
print("  ➜ %d of %d correct" % (n - len(bad), n))
sys.exit(0 if ok_all else 1)
