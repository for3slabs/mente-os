"""plat — the answers this engine must not get wrong on a platform it did not
grow up on.

🔴 THE FAILURE THAT MADE THIS NECESSARY. Measured 2026-09-02, on Windows, on a
clone that had just been installed cleanly. The engine reported **43 failures**
and not one of them was real:

  · `check-declared` · *112 file(s) exist and pieces.tsv does not declare them*
    — every single engine file. ⛔ `os.path.join` built `bin\\check-block`, the
    table declares `bin/check-block`, and a string comparison called the whole
    engine undeclared.
  · `check-document` · `DOC-CAP-002` · *bin/blockread.py exists, is executable,
    and the map never names it* — ⛔ it is a helper and is NOT executable. NTFS
    has no executable bit, so `os.access(X_OK)` answers yes for every readable
    file, and five helpers were demanded as commands.
  · `check-config` · `CFG-SEC-004` · *the folder is 777* — ⛔ right after
    `bin/init` printed `secrets/ 777 → 700`. `os.chmod` on a Windows directory
    succeeds and changes nothing, so the installer announced a protection it had
    not applied.

⚠️ **The third is the one that matters.** The first two are noise that makes a
validator get switched off. The third is the engine making a SECURITY claim it
never measured — the exact failure `rules/rule-checks-must-measure.md` exists to
prevent, committed by the installer itself.

⭐ Why a module and not fifty fixes. ~50 sites build a path with the OS
separator and three remembered to normalise it. *"Remember to call
`.replace(os.sep, '/')`"* is a rule in a document, and this system measured what
those are worth: followed when remembered. ⛔ So it is not a rule. It is a function, and the ones
that must never be guessed are here together.
"""
import os
import re
import shutil
import stat
import subprocess
import sys


def rel(path, start):
    """A repo-relative path in the ONE spelling the tables use: forward slashes.

    ⭐ Every declared path in this engine — `pieces.tsv`, `CAPABILITIES.md`,
    every finding a human reads — is written with `/`. ⛔ `os.path.relpath`
    returns the platform's separator, so on Windows the comparison is against a
    spelling that appears nowhere in the repository.
    """
    return os.path.relpath(path, start).replace(os.sep, "/")


def join(*parts):
    """`os.path.join` with the engine's spelling, for a path that gets COMPARED
    or PRINTED. ⚠️ Not for one handed to `open()` — that wants the platform's."""
    return "/".join(p for p in parts if p)


# ⭐ Extensions Windows treats as runnable. Used only to answer "is this a
# command?" where the executable bit cannot.
_WIN_RUNNABLE = (".exe", ".bat", ".cmd", ".com", ".ps1")


def realpath(path):
    r"""`os.path.realpath`, but understanding the shell's OWN path notation.

    🔴 THE FAILURE, measured 2026-09-08 on a real Windows install. Git Bash
    hands a tool `/c/dev/project/site/x.txt`, and `os.path.realpath` on Windows
    reads that as a path relative to the current drive: it answers
    `C:\c\dev\project\site\x.txt` — a place that does not exist. ⛔ The gate
    then judged a file INSIDE the block's declared scope to be outside it, and
    refused legitimate work. The same path written `C:/dev/...` passed.

    ⚠️ A GATE THAT REFUSES CORRECT WORK IS A GATE THAT GETS SWITCHED OFF, and
    its documented way out is `MENTE_SCRATCH=1` — which disables it entirely.
    A frequent false positive trains people to reach for that, which is the
    outcome ADR-012 exists to prevent.

    ⭐ ONE reader (CHK-SHR-001): every caller that compares a path against a
    declared scope must resolve it the same way, or two of them disagree about
    the same file.
    """
    if not isinstance(path, str) or not path:
        return path
    # ⚠️ Only on Windows, and only the `/<letter>/` shape. ⛔ On a POSIX kernel
    # `/c/...` is a real directory somebody may have, and rewriting it there
    # would break a correct path to fix one that is not broken.
    if os.name == "nt":
        m = re.match(r"^/([A-Za-z])/(.*)$", path)
        if m:
            path = "%s:/%s" % (m.group(1).upper(), m.group(2))
    return os.path.realpath(path)


def is_command(path):
    """⭐ Is this file something a person RUNS, as opposed to a helper another
    file imports?

    ⛔ `os.access(path, os.X_OK)` is the POSIX answer and it is WRONG on
    Windows, where it is true for every readable file. Measured 2026-09-02: five
    helpers (`blockread.py`, `findings.py`, `scaffold.py`, `tsvread.py`,
    `utf8.py`) were reported as undocumented commands.

    ⭐ Where the executable bit is real, it is the answer — it is what the
    author set deliberately. Where it is not, the shebang is: a file that starts
    `#!` was written to be run, and one that does not was written to be
    imported. ⚠️ That is the same intent, recorded in the file instead of in the
    filesystem, which is why it survives a clone onto NTFS and the bit does not.
    """
    if not os.path.isfile(path):
        return False
    if executable_bit_is_real(path):
        return os.access(path, os.X_OK)
    if path.lower().endswith(_WIN_RUNNABLE):
        return True
    try:
        with open(path, "rb") as fh:
            return fh.read(2) == b"#!"
    except OSError:
        # ⬜ CHK-CAU-003 · unreadable is not "not a command". The caller gets
        # False and the file is left out of the map — said out loud there, never
        # counted as a measurement.
        return False


def _ntfs(path):
    """⚠️ Is this path on a Windows filesystem, whatever the OS says?

    🔴 MEASURED 2026-09-05 from WSL over /mnt/c: `os.name` answers "posix", so
    the engine believed modes were enforced — and `chmod 700` on that folder
    changed nothing. ⛔ The question was never "which OS am I", it is "does THIS
    filesystem enforce a mode", and only the path can answer it.
    """
    try:
        real = os.path.realpath(path or ".")
    except OSError:
        return False
    low = real.replace("\\", "/").lower()
    return low.startswith("/mnt/") and len(low) > 6 and low[6] in "/"


def executable_bit_is_real(path=None):
    """⭐ Does THIS filesystem carry the POSIX executable bit at all?

    ⚠️ A Git-Bash clone on NTFS reports modes that look POSIX and are enforced
    by nothing. 🔴 And measured 2026-09-05 from WSL over /mnt/c: `os.name` says
    "posix" while every file reads as executable, so three helpers were reported
    as undocumented COMMANDS. ⛔ The filesystem decides, not the kernel.
    """
    if os.name != "posix":
        return False
    return not _ntfs(path) if path else True


def modes_are_real(path=None):
    """⭐ Does `chmod` HERE actually restrict who can read a file?

    🔴 On Windows it does not. `os.chmod` accepts the call, returns cleanly, and
    the directory stays open to every account on the machine. ⛔ An installer
    that prints `700` there has told the owner their credentials are private
    when they are not — and a false assurance about a credential store is worse
    than no assurance, because it ends the question.

    ⚠️ `path` matters: a POSIX kernel can be looking at an NTFS mount, and there
    the mode is decoration. Called without one, it answers for the OS alone —
    which is the old behaviour and still right for a native tree.
    """
    if os.name != "posix":
        return False
    return not _ntfs(path) if path else True


def privacy(path):
    """How private is this folder, MEASURED — never assumed.

    Returns `(state, detail)`:
      `"private"`   ⭐ measured, and nothing outside the owner can enter
      `"exposed"`   🔴 measured, and it is readable beyond the owner
      `"unknown"`   ⬜ NOT MEASURED · this platform's modes decide nothing, or
                    the mode could not be read

    ⭐ `"unknown"` is the honest answer on Windows and it must reach the person
    as ⬜, never as a pass and never as a 🔴. ⛔ Reporting `777` there is a false
    alarm that gets the check switched off; reporting ✅ is a false assurance
    about credentials. Both are the same defect — a verdict over something that
    was not measured.
    """
    if not os.path.isdir(path):
        return "unknown", "the folder does not exist"
    # ⚠️ Asked ABOUT THIS PATH: a POSIX kernel over an NTFS mount enforces
    # nothing, and the folder in question is the one that decides.
    if not modes_are_real(path):
        return ("unknown",
                "this platform (%s) does not enforce file modes · chmod is "
                "accepted and changes nothing, so whether this folder is "
                "private is decided by the account's own permissions, not by "
                "the engine" % sys.platform)
    try:
        mode = stat.S_IMODE(os.stat(path).st_mode)
    except OSError as e:
        return "unknown", "the mode could not be read (%s)" % e.__class__.__name__
    if mode & 0o077:
        return "exposed", "the folder is %o · anyone on this machine can enter it" % mode
    return "private", "the folder is %o" % mode


# ── invoking this engine's own scripts, on any platform ──────────────────
# 🔴 THE FAILURE THAT MADE THIS NECESSARY. An external audit installed the
# engine on Windows 2026-09-02 and found the two most important gates DEAD:
#
#   · `gate-critical` ran `subprocess.run([".../bin/check-block", "--quiet"])`
#     — a Python script with a `#!/usr/bin/env python3` line and no `.py`.
#     ⛔ CreateProcess does not read shebangs, so it raised FileNotFoundError,
#     the `except Exception: return 0` swallowed it, and EVERY insufficient
#     close went straight through. ⚠️ The gate reported nothing: it looked
#     wired in `.claude/settings.json` and enforced nothing at all.
#   · `gate-secrets` called `bin/secrets-lease` the same way, so a live
#     permission never registered and no access was ever logged.
#
# ⭐ Both failures are ONE mistake: trusting the operating system to know that
# a file is Python. Only the shebang says so, and only POSIX reads it.
# ⚠️ `sys.executable` is the interpreter ALREADY RUNNING — the same one on
# Windows, Linux and macOS, and the same one in a venv. It never guesses.
#
# ⛔ Why this is a function and not "remember to pass sys.executable": four
# call sites forgot, and each one failed silently in the direction that lets
# work through. That is the same lesson as `rel()` above.

def script(path, *args):
    """The argv that runs one of this engine's own scripts, on any platform.

    ⭐ Python is invoked by the interpreter that is already running; a `.sh`
    goes through `bash`, which Git for Windows provides and which every POSIX
    system has. ⚠️ Anything else is returned untouched — a real binary knows
    how to start itself.
    """
    low = path.lower()
    if low.endswith(".sh"):
        # ⭐ bash(), never the bare name. 🔴 Measured 2026-09-07 on a fresh
        # Windows install: `bash` on PATH is `C:\WINDOWS\system32\bash.exe`,
        # the WSL launcher, which CANNOT open a `C:\...` path — every shell
        # script died with exit 127. ⛔ This function is how the whole engine
        # runs a `.sh`, so the bare name broke every one of them at once.
        return list(bash(verify=False)) + [path] + list(args)
    if low.endswith((".exe", ".bat", ".cmd", ".com")):
        return [path] + list(args)
    if low.endswith(".py") or _shebang_says(path, b"python"):
        return [sys.executable, path] + list(args)
    # ⭐ A SHELL SCRIPT WITH NO EXTENSION IS STILL A SHELL SCRIPT. 🔴 Measured
    # 2026-09-07 on a fresh Windows install: a git hook and a launcher are
    # extensionless by convention, so this returned them bare and Windows
    # answered `WinError 193 · not a valid Win32 application` — the probe
    # CRASHED and took every case after it down with it. ⛔ The file said what
    # it was in its first line and nothing read it.
    if _shebang_says(path, b"sh"):
        return list(bash(verify=False)) + [path] + list(args)
    return [path] + list(args)


def _shebang_says(path, word):
    """⭐ Does the file's FIRST LINE name this interpreter? ⛔ The extension
    cannot answer: every command in `bin/` is extensionless on purpose, and so
    is every git hook.

    ⚠️ `word` is matched inside the shebang, so b"sh" catches `sh`, `bash` and
    `zsh` — which is what is wanted: all three read the same dialect here.
    """
    try:
        with open(path, "rb") as fh:
            first = fh.readline(120)
    except OSError:
        # ⬜ CHK-CAU-003 · unreadable is not "not this interpreter". The caller
        # gets the path unchanged and the OS reports the real error, instead of
        # this deciding silently on its behalf.
        return False
    return first.startswith(b"#!") and word in first.lower()


def shell(command):
    """The argv that runs a SHELL COMMAND the owner wrote, on any platform.

    🔴 `subprocess.run(cmd, shell=True)` runs `cmd.exe /c` on Windows and
    `/bin/sh -c` everywhere else — ⛔ two different languages for one string.
    Measured 2026-09-02: `watch-external` declared the convention
    `<command>; exit 1` to mean *something changed*; under `cmd.exe` that
    returned 0, so the watcher reported "nothing new" forever and the person
    was never told their external state had moved.

    ⭐ The owner writes ONE shell dialect — POSIX — and it runs the same on
    all three platforms, because Git for Windows ships bash.
    """
    # ⭐ Same reason as script(): the launcher on PATH answers `--version` and
    # then cannot see the filesystem the command talks about.
    return list(bash(verify=False)) + ["-c", command]


def rmtree(path):
    """Delete a tree on any platform — ⭐ including one git has written into.

    🔴 THE FAILURE THAT MADE THIS NECESSARY. Measured 2026-09-02: git writes
    its own objects under `.git/objects/**` with mode `0o444`. On POSIX the
    DIRECTORY's permission decides, so they delete anyway; ⛔ on Windows a
    read-only file cannot be removed at all, and `shutil.rmtree(...,
    ignore_errors=True)` silently gave up — every probe run left a whole
    temporary git repository behind in `%TEMP%`, accumulating forever.

    ⚠️ `ignore_errors=True` is what made it invisible: the failure was
    swallowed by the very flag that was supposed to make cleanup harmless.
    ⭐ Here the read-only bit is cleared and the delete retried, so cleanup
    either succeeds or the caller finds out.

    Returns True when nothing is left, False when something survived — ⛔ never
    silence, because a probe reports its own residue.
    """
    import shutil

    def _retry(func, target, _exc):
        # ⭐ The documented `onerror` contract: clear what blocks the delete and
        # call the same operation again. ⛔ A bare `pass` here is the silent
        # give-up this function exists to replace.
        try:
            os.chmod(target, stat.S_IWRITE | stat.S_IREAD)
            func(target)
        except OSError:
            pass          # ⬜ said out loud by the return value below

    if not os.path.exists(path):
        return True
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=lambda f, t, e: _retry(f, t, e))
    else:
        shutil.rmtree(path, onerror=_retry)
    return not os.path.exists(path)


def _runs(argv):
    """True when `argv` actually starts and answers. ⛔ Never `os.path.exists`.

    🔴 THE FAILURE THIS ANSWERS, measured 2026-09-07 on a real Windows install.
    `sys.executable` pointed at
    `WindowsApps/PythonSoftwareFoundation.Python.../python.exe` — a Microsoft
    Store EXECUTION ALIAS: a 2-byte stub that works when a terminal invokes it
    and fails when a hook does. It was stamped into every gate, ⛔ so not one
    gate ever ran: `Mente/.beats/` was never created. The install reported
    success and the whole enforcement layer was dead.
    ⚠️ The file existed. Existence was never the question.
    """
    try:
        r = subprocess.run(argv + ["--version"], capture_output=True,
                           timeout=15)
        return r.returncode == 0 and bool((r.stdout or r.stderr).strip())
    except (OSError, subprocess.SubprocessError):
        return False


def python(verify=True):
    """The interpreter to write into a hook — one that has been SEEN to run.

    ⭐ Candidates in order of trust: the one running this, then the launcher,
    then the names on PATH. ⬜ Returns None when none of them answers, and the
    caller says so rather than stamping a guess.
    """
    seen, out = set(), []
    for c in ([sys.executable] if sys.executable else []) + \
             [shutil.which(n) for n in ("py", "python3", "python")]:
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    for c in out:
        # ⚠️ `py` is the Windows launcher: it needs -3 to name a version.
        argv = [c, "-3"] if os.path.basename(c).lower().startswith("py.") else [c]
        if not verify or _runs(argv):
            return argv
    return None


def bash(verify=True):
    """The shell to write into a hook — ⛔ never the bare name on Windows.

    🔴 MEASURED 2026-09-07 on a real Windows install. `bash` on PATH resolved to
    `C:\\WINDOWS\\system32\\bash.exe`, the WSL launcher, which cannot see a
    `C:\\...` path: every shell hook died with `exit 127`, and the battery
    reported 9 failures that were the interpreter, not the engine.
    ⭐ Git for Windows ships a bash that does understand those paths, so it is
    preferred over whatever PATH happens to answer first.
    """
    cands = []
    if os.name == "nt":
        cands += [r"C:\Program Files\Git\bin\bash.exe",
                  r"C:\Program Files\Git\usr\bin\bash.exe",
                  r"C:\Program Files (x86)\Git\bin\bash.exe"]
    w = shutil.which("bash")
    # ⛔ The WSL launcher is excluded by NAME, not by trying it: it answers
    # `--version` perfectly well and still cannot open a Windows path.
    if w and "system32" not in w.replace("/", "\\").lower():
        cands.append(w)
    for c in cands:
        if os.path.isfile(c) and (not verify or _runs([c])):
            return [c]
    # ⬜ Nothing verified. The caller reports it rather than stamping a name
    # that will fail silently on every hook for the life of the install.
    return None
