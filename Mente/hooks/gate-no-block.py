#!/usr/bin/env python3
"""gate-no-block — work that nothing governs does not get written.

🔴 THE FAILURE THAT SHAPES THIS FILE, measured 2026-09-06 on a real run. A full
install succeeded, the person asked for real work, and the assistant researched
it, built it and published it — ⛔ with no block open, no boundary declared and
nothing written to memory. `bin/status` said `⬜ no piece of work open yet`; the
assistant read that line out loud to the owner and carried on anyway.

⭐ THE ENGINE'S OWN THESIS, TURNED ON ITSELF: a rule that only informs is a rule
that holds when somebody remembers. `pre-edit-standards` already REPORTED the
absence of a block. Reporting was not enough — ⚠️ this refuses.

⛔ AND IT MUST HAVE A WAY OUT, or it gets switched off and protects nothing
(ADR-012). Three of them, each cheap and each leaving a trace:
  · `MENTE_SCRATCH=1`   — one command, declared as throwaway
  · a file under `Mente/` — the engine's own housekeeping is not a block
  · nothing staged yet   — a fresh clone has no work to govern

Contract: a PreToolUse payload on stdin · exit 0 allow · exit 2 BLOCK.
"""
import os, re, sys, json, glob
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(MENTE)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beat import beat                                         # noqa: E402
sys.path.insert(0, os.path.join(MENTE, "bin"))
from blockread import body_of                                  # noqa: E402
# ⭐ CHK-SHR-001 · ONE reader for "what does this command write". ⛔ A copy of
# that logic inside this hook is a second answer that drifts from the first.
from cmdwrite import writes as cmd_writes                      # noqa: E402


def targets(payload):
    """Every path an action writes · [] if none · ⬜ None if NOT MEASURED.

    🔴 THE FAILURE THAT WIDENED THIS, measured 2026-09-07 on a real Windows
    run. A whole project was built and shipped and NOT ONE gate fired: the
    assistant wrote every file with `cat > path <<'EOF'` from Bash, and the
    write gates were wired on `Edit|Write|MultiEdit`. ⛔ Measured in the
    transcript: `Bash 83 uses · Write/Edit 0`. The engine watched a door
    nobody walked through — and every check stayed green.

    ⛔ Every field type checked: `json.load` accepts any valid JSON, and a
    hook that raises prints a trace and lets the action through — it does not
    protect, it only looks like it.
    """
    if not isinstance(payload, dict):
        return []
    ti = payload.get("tool_input")
    if not isinstance(ti, dict):
        return []
    for k in ("file_path", "path", "notebook_path"):
        v = ti.get(k)
        if isinstance(v, str) and v:
            return [v]
    # ⭐ A Bash command is an edit too. ⬜ `None` when the shape was not
    # recognised — NOT MEASURED, never a refusal and never a silent pass.
    cmd = ti.get("command")
    if isinstance(cmd, str) and cmd.strip():
        return cmd_writes(cmd)
    return []


def a_block_is_open():
    """⭐ One reader for the question. A block is open when a BLOCK.md exists
    under work/blocks/active/ — the same place `bin/status` counts."""
    d = os.path.join(MENTE, "work", "blocks", "active")
    return bool(glob.glob(os.path.join(d, "*", "BLOCK.md")))


def declared_in(path):
    """Is `path` named by SOME open block's §B IN? ⬜ None when nothing says.

    🔴 THE FAILURE, measured 2026-09-07. A run opened a block correctly and then
    wrote its deliverable to the repository root — outside everything §B named —
    and `check-block` still reported `0 violations`, because a block validates
    its own SHAPE, never where the work actually landed. ⛔ The gate refused
    work with NO block and waved through work OUTSIDE the block, which is the
    same hole one step along.

    ⚠️ It answers None, not False, when no §B names anything readable: a gate
    that refuses because it could not read is a gate that gets switched off.
    """
    d = os.path.join(MENTE, "work", "blocks", "active")
    names, saw_any, unreadable = [], False, []
    for b in sorted(glob.glob(os.path.join(d, "*", "BLOCK.md"))):
        try:
            body = body_of(open(b, encoding="utf-8").read(), "B")
        except (OSError, ValueError):
            # ⬜ CHK-CAU-003 · a block whose §B cannot be read is NOT MEASURED,
            # never a silent skip. ⛔ Swallowed, an unreadable block leaves the
            # gate free to refuse a write that block may well have allowed.
            sys.stderr.write("⬜ gate-no-block · %s · §B unreadable · this "
                             "block's scope was NOT MEASURED\n"
                             % os.path.basename(os.path.dirname(b)))
            unreadable.append(b)
            continue
        # ⭐ Only the IN half. The OUT half is prose about limits, and matching
        # a path against it would refuse the very file a block exists to write.
        head = body.split("OUT", 1)[0] if body else ""
        for line in head.split("\n"):
            line = line.strip()
            if not line.startswith("-"):
                continue
            for tok in re.findall(r"`([^`]+)`", line):
                tok = tok.strip().rstrip("*").rstrip("/")
                if tok and not tok.startswith("⬜"):
                    names.append(tok)
                    saw_any = True
    if not saw_any:
        return None                     # ⬜ nothing declared · NOT MEASURED
    if unreadable:
        # ⚠️ Some scope could not be read, so "outside every block" is not a
        # claim this can make. ⭐ NOT MEASURED, not a refusal.
        return None
    real = os.path.realpath(path)
    for n in names:
        # ⚠️ Matched on the RESOLVED path: `../` walks past a string compare,
        # and this decides whether a write is refused.
        cand = n if os.path.isabs(n) else os.path.join(REPO, n)
        cand = os.path.realpath(cand)
        if real == cand or real.startswith(cand + os.sep):
            return True
    return False


def inside_engine(path):
    """⚠️ The engine's own folder is not somebody's project work. Installing,
    configuring and fixing Mente OS itself must not require a block about Mente
    OS — ⛔ that is a loop the person cannot get out of on a fresh install."""
    if not path:
        return True                     # nothing named · nothing to govern
    try:
        real = os.path.realpath(path)
    except OSError:
        return False
    return real.startswith(os.path.realpath(MENTE) + os.sep)


OUT_OF_SCOPE = """
🔴 REFUSED · this path is outside every open block's §B

   %s

   ⛔ A block is open, but its §B IN does not name this. Writing here
      produces work the block does not account for — and every validator
      stays green, because a block checks its own SHAPE, never where the
      work actually landed.

   ⭐ Measured 2026-09-07: a run opened a block correctly and then wrote
      its deliverable to the repository root. `check-block` reported
      0 violations, and the file was invisible to the whole engine.

   Two honest ways forward:
     · write it where §B already allows — the product belongs in
       Mente/Cerebro/<name>/, the record in the block itself
     · or add this path to §B, ASK THEM FIRST, and say what it widens

   ⛔ Do not widen the scope silently to fit what you were going to do.
"""

REFUSAL = """
🔴 REFUSED · there is no piece of work open

   ⛔ What you are about to write is governed by nothing: no boundary was
      declared, and when this conversation resets nobody will know why it
      exists.

   ⭐ Measured 2026-09-06: a full run researched, built and published real
      work with no block open. Every check was green and the system had
      held nothing.

   The way forward — ask them what this is, then:
      Mente/bin/new-block <name> --type docs --intent "<one sentence>"

   ⚠️ And ask THEM the boundary: what may be changed, what is off limits.
      ⛔ An assistant that writes its own limits has written no limit.

   For a genuine throwaway — a scratch file, a one-off command:
      MENTE_SCRATCH=1  before the command  ⚠️ it leaves a trace on purpose
"""


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        # ⬜ CHK-CAU-003 · unreadable payload is NOT MEASURED, never a block.
        # ⛔ Refusing on a payload we could not read turns a parse bug into a
        # system nobody can use.
        print("⬜ gate-no-block · payload unreadable · NOT MEASURED",
              file=sys.stderr)
        return 0

    # ⭐ Declared throwaway. It is honoured, and the beat records that it was.
    if os.environ.get("MENTE_SCRATCH", "").strip() not in ("", "0"):
        beat(MENTE, "gate-no-block")
        return 0

    paths = targets(payload)
    if paths is None:
        # ⬜ CHK-CAU-003 · the command's shape was not recognised, so what it
        # writes was NOT MEASURED. ⛔ Said out loud and allowed: refusing what
        # could not be read is how a gate gets switched off, and then nothing
        # is governed at all (ADR-012). ⚠️ It still leaves a beat, so the
        # engine can show HOW OFTEN it could not measure.
        beat(MENTE, "gate-no-block")
        sys.stderr.write("⬜ gate-no-block · this command's writes were NOT "
                         "MEASURED · allowed\n")
        return 0
    if not paths:
        return 0                        # nothing written · nothing to govern
    # ⭐ The engine's own housekeeping is never somebody's project work, and a
    # command touching ONLY Mente/ needs no block (see inside_engine).
    outside = [p for p in paths if not inside_engine(p)]
    if not outside:
        return 0

    if a_block_is_open():
        # ⭐ A block is open — now the question is whether THESE paths are
        # inside what it declared. 🔴 Measured 2026-09-07: one was not, and
        # nothing said so; the deliverable landed in the repository root and
        # every validator stayed green because none of them looks at where
        # work went.
        for p in outside:
            if declared_in(p) is False:
                beat(MENTE, "gate-no-block")
                sys.stderr.write(OUT_OF_SCOPE % p)
                return 2
        # ⬜ None · no §B names anything readable · NOT MEASURED, never a
        # refusal: a gate that blocks because it could not read gets removed.
        beat(MENTE, "gate-no-block")
        return 0

    beat(MENTE, "gate-no-block")
    sys.stderr.write(REFUSAL)
    return 2


if __name__ == "__main__":
    # ⭐ CHK-CAU-002 · a crash is a verdict, not a stack trace. ⚠️ And here it
    # is exit 0: a gate that fails CLOSED on its own bug locks the person out
    # of their own machine — measured doctrine, ADR-012.
    try:
        sys.exit(main())
    except Exception as e:                                # noqa: BLE001
        print("⬜ gate-no-block could not run · %s · NOT MEASURED"
              % type(e).__name__, file=sys.stderr)
        sys.exit(0)
