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
import os, sys, json, glob
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


def target(payload):
    """The path an action is about. ⛔ Every field type checked: `json.load`
    accepts any valid JSON, and a hook that raises prints a trace and lets the
    action through — it does not protect, it only looks like it."""
    if not isinstance(payload, dict):
        return ""
    ti = payload.get("tool_input")
    if not isinstance(ti, dict):
        return ""
    for k in ("file_path", "path", "notebook_path"):
        v = ti.get(k)
        if isinstance(v, str) and v:
            return v
    return ""


def a_block_is_open():
    """⭐ One reader for the question. A block is open when a BLOCK.md exists
    under work/blocks/active/ — the same place `bin/status` counts."""
    d = os.path.join(MENTE, "work", "blocks", "active")
    return bool(glob.glob(os.path.join(d, "*", "BLOCK.md")))


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
        beat("gate-no-block", "scratch")
        return 0

    path = target(payload)
    if inside_engine(path):
        return 0
    if a_block_is_open():
        beat("gate-no-block", "block open")
        return 0

    beat("gate-no-block", "REFUSED")
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
