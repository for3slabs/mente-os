#!/usr/bin/env python3
"""gate-protected-writes — a WRITE through Bash to a protected path asks, like an Edit would.

⭐ THE HOLE THIS CLOSES, measured 2026-09-26 on a real installation.
The `ask` rules in `.claude/settings*.json` protect `bin/`, `hooks/`, `rules/`,
`CAPABILITIES.md`, `memory/principles/` and the settings themselves — but only
from the Edit/Write TOOLS. In one session the agent wrote to all of them through
Bash instead: `cp` into `bin/`, a `python` heredoc rewriting `rules/`, `sed -i`
over docs. Not one prompt fired. A lock on the door with the window open.

WHAT IT DOES. For a Bash command it finds the paths the command WRITES —
`sed -i` · `>`/`>>` · `tee` · the destination of `cp`/`mv`/`install`/`rsync`/`ln`
· `rm`/`rmdir`/`unlink`/`touch`/`truncate`/`chmod` · `git mv`/`git rm` · an inline
python/node/perl that opens for writing or moves/removes files — and when one of
them is protected it answers `ask`, naming the path. The owner decides; nothing is
denied.

⭐ THE LIST IS NOT HERE. It is read from the `Edit(...)` entries of
`permissions.ask` in both settings files — the same rules the Edit tool obeys.
A second list would drift from the first, and the drift would be silent.

⚠️ WHAT IT DOES NOT DO. Running or reading a protected script (`bin/verify-all`,
`cat rules/x.md`, `sed -n`) passes untouched: a gate that nags on the daily path
gets switched off. And it cannot see a path built at runtime (`"$DIR/x"`,
`os.path.join(a, b)`): it reads the literal text, so it catches the direct write,
not a determined one.

⛔ NOT PAUSED by `bin/off`: it guards the guards, and `bin/off` pauses warnings,
not the locks on the system's own rules.

Exit: 0 always, with the verdict in stdout (Claude Code PreToolUse contract).
"""
import fnmatch
import json
import os
import re
import shlex
import sys

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(MENTE)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beat import beat                                          # noqa: E402

SETTINGS = (os.path.join(REPO, ".claude", "settings.json"),
            os.path.join(REPO, ".claude", "settings.local.json"))

SEP = re.compile(r"\s*(?:&&|\|\||;|\||\n)\s*")
REDIRECT = re.compile(r"(?<![<&])(?:\d?>>?|&>>?)\s*([^\s;&|)<>]+)")
INTERP = re.compile(r"(?:^|[\s;&|(])(?:python3?|node|perl|ruby)\b[^\n]*?(?:\s-c\s|\s-e\s|<<|\s-\s|\s-$)")
CODE_WRITES = re.compile(
    r"""open\([^)]*?,\s*['"][^'"]*[wax+]|\.write_(?:text|bytes)\(|shutil\.(?:copy|copy2|copyfile|move|rmtree)\("""
    r"""|os\.(?:replace|rename|remove|unlink|chmod|rmdir)\(|writeFileSync|appendFileSync""")
LITERAL = re.compile(r"""["']([^"'\n]{2,300})["']""")
ALL_ARGS = {"rm", "rmdir", "unlink", "touch", "truncate", "chmod", "chown"}
DEST_LAST = {"cp", "mv", "install", "rsync", "ln"}


def verdict(decision, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason}}))
    return 0


def protected():
    """The Edit(...) globs of permissions.ask, made absolute."""
    out = []
    for f in SETTINGS:
        try:
            with open(f, encoding="utf-8") as fh:
                rules = (json.load(fh).get("permissions") or {}).get("ask") or []
        except FileNotFoundError:
            continue    # ⬜ skipped on purpose: an absent file declares no rule (settings.local.json is optional)
        except (OSError, ValueError) as e:
            # ⛔ An UNREADABLE settings file is a gap, not an absence: its rules protect
            # nothing while the gate reports green. Said out loud, never swallowed.
            print("⬜ gate-protected-writes · %s unreadable (%s) · its ask rules NOT MEASURED"
                  % (os.path.basename(f), type(e).__name__), file=sys.stderr)
            continue
        for r in rules:
            m = re.match(r"^Edit\((.+)\)$", r.strip())
            if not m:
                continue
            g = m.group(1)
            g = re.sub(r"^\$\{?CLAUDE_PROJECT_DIR\}?", REPO, g)
            g = re.sub(r"^\$\{?HOME\}?|^~", os.path.expanduser("~"), g)
            if g.startswith("//"):
                g = g[1:]
            deep = g.endswith("/**")
            # ⚠️ normpath KEEPS a trailing `/**`: adding it back made `bin/**/**`, which matched
            # nothing — only exact files asked (caught by probe-protected-writes, 2026-09-26)
            out.append(os.path.normpath(g[:-3] if deep else g) + ("/**" if deep else ""))
    return sorted(set(out))


def hit(path, globs):
    for g in globs:
        if g.endswith("/**"):
            base = g[:-3]
            if path == base or path.startswith(base + os.sep):
                return g
        elif fnmatch.fnmatch(path, g):
            return g
    return None


def resolve(tok, cwd):
    tok = tok.strip().strip("\"'")
    if not tok or tok.startswith(("-", "$", "/dev/")) or "$" in tok:
        return None
    tok = os.path.expanduser(tok)
    if not os.path.isabs(tok):
        tok = os.path.join(cwd, tok)
    return os.path.normpath(tok)


def targets(cmd, cwd):
    """(path, how) pairs this command writes."""
    found = []
    m = re.match(r"^\s*cd\s+(\S+)\s*&&", cmd)
    if m:
        d = resolve(m.group(1), cwd)
        cwd = d if d else cwd
    body = re.split(r"<<-?\s*['\"]?(\w+)['\"]?", cmd, maxsplit=1)
    shell = body[0]
    for seg in SEP.split(shell):
        for t in REDIRECT.findall(seg):
            found.append((t, "redirect >"))
        try:
            words = shlex.split(seg, comments=False)
        except ValueError:
            words = seg.split()
        if not words:
            continue
        w0 = os.path.basename(words[0])
        args = [w for w in words[1:] if not w.startswith("-")]
        if w0 == "sed" and any(w.startswith("-i") or w == "--in-place" for w in words[1:]):
            found += [(a, "sed -i") for a in args[1:]]
        elif w0 == "tee":
            found += [(a, "tee") for a in args]
        elif w0 in DEST_LAST and args:
            found.append((args[-1], w0))
        elif w0 in ALL_ARGS:
            found += [(a, w0) for a in args]
        elif w0 == "git" and len(words) > 1 and words[1] in ("mv", "rm"):
            found += [(a, "git " + words[1]) for a in args[1:]]
    if INTERP.search(cmd) and CODE_WRITES.search(cmd):
        found += [(lit, "inline code that writes") for lit in LITERAL.findall(cmd)
                  if "/" in lit or "." in lit]
    out = []
    for tok, how in found:
        p = resolve(tok, cwd)
        if p:
            out.append((p, how))
            if tok.startswith("Mente/"):
                out.append((os.path.normpath(os.path.join(REPO, tok)), how))
    return out


def main():
    beat(MENTE, "gate-protected-writes")   # proof this gate still fires (hooks/_beat.py)
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    if not isinstance(payload, dict) or payload.get("tool_name") != "Bash":
        return 0
    cmd = (payload.get("tool_input") or {}).get("command", "")
    if not isinstance(cmd, str) or not cmd.strip():
        return 0
    globs = protected()
    if not globs:
        return 0
    cwd = payload.get("cwd") or REPO
    hits = []
    for p, how in targets(cmd, cwd):
        g = hit(p, globs)
        if g and (p, how) not in [(x, y) for x, y, _ in hits]:
            hits.append((p, how, g))
    if not hits:
        return 0
    lines = ["%s  (%s)" % (os.path.relpath(p, REPO), how) for p, how, _ in hits[:6]]
    return verdict("ask",
                   "✋ This command WRITES to a path protected by the `ask` rules of "
                   "`.claude/settings*.json` — through Bash, where those rules do not reach:\n   "
                   + "\n   ".join(lines)
                   + "\nApprove it? (gate-protected-writes)")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:                                          # noqa: BLE001
        sys.exit(0)        # a broken gate must never block the session — check-gates sees it
