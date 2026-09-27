#!/usr/bin/env python3
"""probe-protected-writes — does a Bash WRITE to a protected path ask, and ONLY a write?

⭐ WHAT IT MEASURES. `hooks/gate-protected-writes.py` closes the hole where the
`ask` rules guard the Edit tool but not Bash (measured 2026-09-26: `cp` into
bin/, a python heredoc over rules/, `sed -i` — no prompt fired). It can fail two
silent ways: missing a write (the hole is back) or asking on reads and runs
(noise, and a noisy gate gets removed). Every case below is a command the agent
really types; three of them are the exact shapes that slipped through that day.

Runs in a throwaway tree with its own `.claude/settings.json`, so it also proves
the list is READ from the Edit(...) rules — case ⑬ adds a rule and expects it.

Exit: 0 every case behaves · 1 one does not
"""
import json, os, shutil, subprocess, sys, tempfile
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT, report                      # noqa: E402

results = []
# 🔴 2026-09-27, the battery on a NATIVE Windows install: 10 of 17 cases here were
# silent. The gate turned the project path into a regex REPLACEMENT, and on Windows
# that path is `C:\Users\...` — `\U` is a bad escape, the gate raised, and a gate
# that breaks never blocks: every protected write went through. ⭐ A POSIX folder name
# may carry a backslash, so EVERY case below runs under one, on every platform.
WORK = tempfile.mkdtemp(prefix="mente-pw-" + ("" if os.name == "nt" else "\\Users-"))
M = os.path.join(WORK, "Mente")


def case(label, ok, detail=""):
    print("  %-62s %s %s" % (label, "✅" if ok else "\U0001f534", detail))
    results.append((label, ok))


def settings(extra=()):
    rules = ["Edit($CLAUDE_PROJECT_DIR/Mente/bin/**)", "Edit($CLAUDE_PROJECT_DIR/Mente/hooks/**)",
             "Edit($CLAUDE_PROJECT_DIR/Mente/rules/**)", "Edit($CLAUDE_PROJECT_DIR/Mente/CAPABILITIES.md)",
             "Write($CLAUDE_PROJECT_DIR/Mente/bin/**)"] + list(extra)
    os.makedirs(os.path.join(WORK, ".claude"), exist_ok=True)
    with open(os.path.join(WORK, ".claude", "settings.json"), "w") as fh:
        json.dump({"permissions": {"ask": rules}}, fh)


def gate(cmd, cwd=None, tool="Bash", env=None):
    p = {"tool_name": tool, "tool_input": {"command": cmd}, "cwd": cwd or WORK}
    r = subprocess.run([sys.executable, os.path.join(M, "hooks", "gate-protected-writes.py")],
                       input=json.dumps(p), capture_output=True, text=True, timeout=30, env=env)
    out = r.stdout.strip()
    return r.returncode, (json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else "silent"), out


try:
    os.makedirs(os.path.join(M, "hooks"))
    for f in ("gate-protected-writes.py", "_beat.py"):
        shutil.copy2(os.path.join(ROOT, "hooks", f), os.path.join(M, "hooks", f))
    settings()

    ask = lambda label, cmd, cwd=None: case(label, gate(cmd, cwd)[1] == "ask", gate(cmd, cwd)[1])
    silent = lambda label, cmd, cwd=None, tool="Bash": case(
        label, gate(cmd, cwd, tool)[1] == "silent", gate(cmd, cwd, tool)[1])

    ask("① `cp` into bin/ (the 2026-09-26 shape) → ask", "cp /tmp/x/connection Mente/bin/")
    ask("② python heredoc rewriting rules/ (the 2026-09-26 shape) → ask",
        "cd Mente && python3 - <<'EOF'\np = 'rules/contract-document.md'\n"
        "s = open(p).read()\nopen(p, 'w').write(s)\nEOF")
    ask("③ `sed -i` over a hook → ask", "sed -i 's/a/b/' Mente/hooks/session-start.sh")
    ask("④ `>>` appending to a rule → ask", "echo x >> Mente/rules/rule-x.md")
    ask("⑤ relative path resolved from `cwd` → ask", "touch bin/new", cwd=M)
    ask("⑥ `git mv` inside rules/ → ask", "git mv Mente/rules/a.md Mente/rules/b.md")
    ask("⑦ `tee` onto CAPABILITIES.md → ask", "echo x | tee Mente/CAPABILITIES.md")
    silent("⑧ RUNNING a protected script, output to /tmp → silent",
           "Mente/bin/verify-all > /tmp/out 2>&1")
    silent("⑨ reading: `cat` / `sed -n` / `grep` → silent",
           "cat Mente/rules/x.md; sed -n 1,5p Mente/bin/y; grep -n a Mente/hooks/z")
    silent("⑩ python heredoc that only READS bin/ → silent",
           "python3 - <<'EOF'\nprint(open('Mente/bin/x').read())\nEOF")
    silent("⑪ a write OUTSIDE the protected list → silent", "echo hi > Mente/docs/notes.md")
    silent("⑫ the Edit tool itself → silent (its own rule handles it)", "x", tool="Edit")
    settings(extra=["Edit($CLAUDE_PROJECT_DIR/Mente/secrets/**)"])
    ask("⑬ a NEW Edit(...) rule in settings is obeyed (single source) → ask",
        "echo x > Mente/secrets/new.md")
    settings()
    silent("   … and gone again when the rule is removed → silent", "echo x > Mente/secrets/new.md")
    ask("⑭ `rm` of a hook → ask", "rm Mente/hooks/gate-protected-writes.py")
    rc, v, out = gate("sed -i 's/a/b/' Mente/hooks/session-start.sh")
    case("⑮ the reason names the path and the verb", "hooks/session-start.sh" in out and "sed -i" in out, "")
    rc, v, _ = gate("}{ not json", tool="Bash")
    rc2 = subprocess.run([sys.executable, os.path.join(M, "hooks", "gate-protected-writes.py")],
                         input="}{", capture_output=True, text=True).returncode
    case("⑯ garbage input → exit 0, silent (a broken gate never blocks)", rc2 == 0, "exit %d" % rc2)
    # ⑰ `~` resolves through the SAME kind of replacement — a HOME carrying `\U`,
    # as `C:\Users\<name>` always does, must still be protected.
    settings(["Edit(~/zzprobe-home/**)"])
    _home = dict(os.environ, HOME=WORK, USERPROFILE=WORK)
    _, d17, _ = gate("cp /tmp/x ~/zzprobe-home/key", env=_home)
    case("⑰ a rule under `~`, with a backslash in HOME → ask", d17 == "ask", d17)
    settings()
finally:
    shutil.rmtree(WORK, ignore_errors=True)

sys.exit(report(results))
