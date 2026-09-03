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
those are worth: 40-60%. ⛔ So it is not a rule. It is a function, and the ones
that must never be guessed are here together.
"""
import os
import stat
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
    if executable_bit_is_real():
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


def executable_bit_is_real():
    """⭐ Does this filesystem carry the POSIX executable bit at all?

    ⚠️ Answered by the platform, not by a probe of the tree: a Git-Bash clone on
    NTFS reports modes that look POSIX and are not enforced by anything.
    """
    return os.name == "posix"


def modes_are_real():
    """⭐ Does `chmod` on this platform actually restrict who can read a file?

    🔴 On Windows it does not. `os.chmod` accepts the call, returns cleanly, and
    the directory stays open to every account on the machine. ⛔ An installer
    that prints `700` there has told the owner their credentials are private
    when they are not — and a false assurance about a credential store is worse
    than no assurance, because it ends the question.
    """
    return os.name == "posix"


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
    if not modes_are_real():
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
        return ["bash", path] + list(args)
    if low.endswith((".exe", ".bat", ".cmd", ".com")):
        return [path] + list(args)
    if low.endswith(".py") or _is_python_shebang(path):
        return [sys.executable, path] + list(args)
    return [path] + list(args)


def _is_python_shebang(path):
    """⭐ Does the file itself say it is Python? ⛔ The extension cannot answer:
    every command in `bin/` is extensionless on purpose."""
    try:
        with open(path, "rb") as fh:
            first = fh.readline(120)
    except OSError:
        # ⬜ CHK-CAU-003 · unreadable is not "not Python". The caller gets the
        # path unchanged and the OS reports the real error, instead of this
        # deciding silently on its behalf.
        return False
    return first.startswith(b"#!") and b"python" in first.lower()


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
    return ["bash", "-c", command]


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
