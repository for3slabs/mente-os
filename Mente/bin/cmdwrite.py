"""cmdwrite — which paths a shell command WRITES to. One reader, for every gate.

🔴 THE FAILURE THAT MADE THIS FILE, measured 2026-09-07 on a real Windows run.
A full session built and shipped nine files of somebody's project, and NOT ONE
gate fired. ⛔ The reason was not a broken gate: the assistant wrote every file
with `cat > path <<'EOF'` from Bash, and the write gates are wired on
`Edit|Write|MultiEdit`. ⚠️ Measured in the transcript: `Bash 83 uses ·
Write/Edit 0`. The engine was watching a door nobody walked through.

⭐ CHK-SHR-001 · ONE reader. ⛔ A second copy of "what does this command write"
inside a hook would answer differently the day one is fixed, and then one gate
refuses what another allows.

⚠️ IT ANSWERS None, NEVER A GUESS. Three answers, and the difference decides
whether a person keeps the system:
  · a list of paths — these are written, and the caller may judge them
  · []              — this command writes nothing the caller must govern
  · None            — ⬜ NOT MEASURED · the shape was not recognised

⛔ None is NOT "no paths". A gate that treats an unparsed command as "writes
nothing" is a gate with a hole; one that treats it as "writes everything"
refuses `npm install` and gets switched off within a day. The caller decides,
and it must be able to tell the two apart.

Not a command. The `.py` suffix says so (bin/README).
"""
import re
import shlex

# ⭐ Commands that write where the person never asked and never reads: package
# managers, compilers, version control. ⛔ A gate that refuses `npm install`
# because it writes node_modules/ is a gate that gets removed the same day —
# and then nothing is governed at all (ADR-012).
TOOLING = {
    "npm", "npx", "pnpm", "yarn", "bun", "deno", "pip", "pip3", "pipx",
    "poetry", "uv", "cargo", "go", "gem", "bundle", "composer", "mvn",
    "gradle", "make", "cmake", "docker", "git", "gh", "astro", "vite",
    "webpack", "tsc", "node", "python", "python3", "py",
}

# ⚠️ `python -c "open('x','w')"` IS a write, and `python script.py` may be one
# too. ⛔ But refusing every `python` call would refuse this engine's own
# validators. ⭐ So the interpreters are tooling UNLESS the command line itself
# names a write — that is what WRITE_IN_CODE looks for.
WRITE_IN_CODE = re.compile(
    r"""open\s*\(\s*['"]([^'"]+)['"]\s*,\s*['"][waxWAX]"""
    r"""|\.write_text\s*\(|shutil\.(?:copy|move)""")

# ⭐ The redirections. `>` and `>>` write; `2>` and `2>&1` do not name a file
# the person authored, and `<` reads.
# ⚠️ THE TARGET MAY BE QUOTED, and a path with a space is not exotic — measured
# on the failing run, the project lived under a path with a space. ⛔ Split on
# whitespace, `> "my folder/a b.md"` yields `"my` and the gate then judges a
# file that does not exist: it allows a write it never looked at.
_REDIR = re.compile(r"""(?<![0-9&])>>?\s*("[^"]*"|'[^']*'|[^\s;|&()]+)""")

# ⚠️ Heredoc bodies are DATA, not command text. ⛔ Scanned as commands, a
# document containing the word `rm` reads as a deletion — and the gate refuses
# the very file it exists to let through.
_HEREDOC = re.compile(r"<<-?\s*[\"']?(\w+)[\"']?\n.*?^\1\s*$",
                      re.S | re.M)

# ⭐ Tools whose ARGUMENTS are destinations, not flags.
_ARG_WRITERS = {"tee": "all", "cp": "last", "mv": "last", "install": "last",
                "touch": "all", "truncate": "last", "dd": None}


_QUOTED = re.compile(r'"[^"\\]*(?:\\.[^"\\]*)*"' r"|'[^']*'")


def _mask_quoted(cmd):
    """The command with QUOTED text replaced by placeholders of equal length.

    🔴 THE FAILURE, measured 2026-09-08 on a real install. `grep -rn "a > b" x/`
    was refused twice during an audit: the `>` lives INSIDE a quoted search
    pattern, and the redirection matcher read it as "writes to the file b".
    ⛔ A read-only `grep` rejected as a write is exactly what makes somebody
    switch the gate off — and its way out, `MENTE_SCRATCH=1`, disables the gate
    entirely (ADR-012).

    ⚠️ Length is preserved so every offset downstream still lines up; only the
    CONTENT is hidden. ⭐ A `>` inside quotes is data, never an instruction.

    ⛔ EXCEPT A QUOTED REDIRECTION TARGET. 🔴 Caught the moment this was
    written: masking every quoted string also hid `cat > "my dir/a b.md"`, so
    a legitimate write to a path WITH A SPACE came back as `xxxxxxx`. The one
    place a quoted string is not data is immediately after a `>`.
    """
    out, i = [], 0
    for m in _QUOTED.finditer(cmd):
        before = cmd[:m.start()].rstrip()
        # ⭐ Kept verbatim when it IS the destination of a redirection.
        keep = before.endswith(">")
        out.append(cmd[i:m.start()])
        out.append(m.group(0) if keep
                   else '"' + "x" * (len(m.group(0)) - 2) + '"')
        i = m.end()
    out.append(cmd[i:])
    return "".join(out)


def _strip_heredocs(cmd):
    """The command with heredoc BODIES removed, their `<<TAG` markers kept.

    ⭐ The marker stays so the redirection before it still parses; the body
    goes because it is content, and content is not instructions."""
    return _HEREDOC.sub(lambda m: "<<%s" % m.group(1), cmd)


def _segments(cmd):
    """The command split on the operators that start a NEW command.

    ⚠️ `cd x && cat > y` is two commands, and only the second writes. ⛔ Read
    as one, the leading `cd` decides the verb and the write is invisible."""
    # ⚠️ Subshell parentheses are grouping, not path text. ⛔ Left in place,
    # `(cd x && cat > y.md)` yields the target `y.md)` — a path that resolves
    # to nothing, so the gate judges a file nobody is writing.
    cmd = re.sub(r"(?<![\\\w])[()](?![\w])", " ", cmd)
    return [s for s in re.split(r"&&|\|\||;|\n|\|", cmd) if s.strip()]


_PREFIX = ("sudo", "env", "command", "exec", "time", "nohup")


def _words(seg):
    """The command's words, or None if it cannot be split. ⭐ One splitter, so
    `_verb` and the argument readers can never disagree about where the verb
    ends — the disagreement that produced `['tee', '/etc/hosts']`."""
    try:
        return shlex.split(seg, posix=True)
    except ValueError:
        return None


def _args(seg):
    """The arguments AFTER the verb, prefixes and flags removed. ⛔ Counting
    from index 1 counts `sudo` as the verb and the real verb as a path."""
    words = _words(seg)
    if words is None:
        return None
    i = 0
    while i < len(words) and (words[i] in _PREFIX
                              or re.match(r"^\w+=", words[i])):
        i += 1
    return [a for a in words[i + 1:] if not a.startswith("-")]


def _verb(seg):
    """The command word, past `sudo`, `env` and variable assignments."""
    parts = _words(seg)
    if parts is None:
        parts = seg.split()
    for p in parts:
        if "=" in p and not p.startswith("-") and re.match(r"^\w+=", p):
            continue                     # VAR=value prefix
        if p in _PREFIX:
            continue
        return p.split("/")[-1]
    return ""


def writes(command):
    """Paths this command writes · [] if none · ⬜ None if not recognised."""
    if not isinstance(command, str) or not command.strip():
        return []                        # nothing to run, nothing to write
    # ⭐ Heredoc bodies first. ⚠️ Then TWO views of the same command, because
    # the two searches below need opposite things from a quoted string:
    #   · REDIRECTIONS read the masked text — a `>` inside quotes is data
    #   · AN INTERPRETER'S CODE reads the raw text — `python -c "open('z','w')"`
    #     keeps its destination INSIDE the quotes
    # 🔴 Measured while fixing this: masking for both broke the interpreter
    # case, and a fix that breaks the case beside it is not a fix.
    raw = _strip_heredocs(command)
    text = _mask_quoted(raw)

    # ⬜ UNBALANCED QUOTING · NOT MEASURED, and never a partial path.
    # 🔴 Caught while probing the boundaries: `cat > "unterminated` returned
    # `['unterminated']` — a path missing its tail. ⛔ The gate would then judge
    # a file nobody writes and wave through the one that IS written, which is
    # worse than not looking: it produces a green that was never earned.
    try:
        shlex.split(text, posix=True)
    except ValueError:
        return None
    found, unknown = [], False

    for seg, seg_raw in zip(_segments(text), _segments(raw)):
        seg = seg.strip()
        if not seg:
            continue
        verb = _verb(seg)

        # ① redirections — they write whatever follows, whoever the verb is
        for m in _REDIR.finditer(seg):
            tok = m.group(1).strip("'\"")
            if tok and not tok.startswith("&") and tok not in (
                    "/dev/null", "NUL", "nul"):
                found.append(tok)

        # ② tools whose arguments are destinations
        if verb in _ARG_WRITERS:
            args = _args(seg)
            if args is None:
                unknown = True
                continue
            how = _ARG_WRITERS[verb]
            if how == "all":
                found.extend(args)
            elif how == "last" and args:
                found.append(args[-1])
            else:
                # ⬜ dd and friends: the destination is a `of=` style argument
                # this reader does not parse. NOT MEASURED, never assumed safe.
                unknown = True

        # ③ in-place editors
        elif verb in ("sed", "perl") and re.search(r"(?<!\w)-i", seg):
            args = _args(seg)
            if args is None:
                unknown = True
                continue
            # ⚠️ The first argument is the SCRIPT, the rest are files.
            found.extend(args[1:] if len(args) > 1 else [])

        # ④ interpreters — tooling, unless the line itself names a write
        elif verb in TOOLING:
            # ⚠️ The RAW segment: an interpreter's destination lives inside
            # the quotes the masking hides.
            for m in WRITE_IN_CODE.finditer(seg_raw):
                if m.group(1):
                    found.append(m.group(1))
                else:
                    # ⬜ A write whose destination is a variable. The engine
                    # cannot name the path — and saying so is the point.
                    unknown = True

        # ⑤ anything else that is not a known reader
        elif verb and verb not in (
                "cat", "echo", "printf", "ls", "grep", "find", "head", "tail",
                "wc", "sed", "awk", "cut", "sort", "uniq", "diff", "file",
                "stat", "which", "cd", "pwd", "test", "true", "false", "date",
                "sleep", "curl", "wget", "chmod", "chown", "mkdir", "rmdir",
                "export", "source", "read", "set", "unset", "for", "if",
                "while", "do", "done", "then", "fi", "esac", "case", "rm"):
            # ⬜ An unknown verb may or may not write. ⛔ Guessing either way
            # is how a gate becomes wrong in one of the two dangerous
            # directions — so it says it did not measure.
            unknown = True

    # ⬜ A DESTINATION THE ENGINE CANNOT NAME is NOT MEASURED. 🔴 Caught on the
    # boundaries: `cat > "$DEST"` returned the literal `$DEST`, which resolves
    # to nothing — so the gate compares a non-path against the block's scope,
    # decides it is outside, and refuses a write it never actually located.
    # ⛔ Worse in the other direction: a variable expanding INSIDE the scope
    # would be refused, and a gate that refuses correct work gets switched off.
    if any("$" in f or "`" in f for f in found):
        return None
    if found:
        return found
    return None if unknown else []
