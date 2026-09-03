"""utf8 — make this engine speak UTF-8 on every platform, before anything else.

🔴 THE FAILURE THAT MADE THIS NECESSARY. Measured on Windows 2026-09-02, from a
real user's run: `bin/probes/run-all.py` crashed on its FIRST print —
`UnicodeEncodeError: 'charmap' codec can't encode characters` — because the
console defaults to cp1252 there and this engine's output is full of ⭐ ⛔ ⚠️ 🔴.

⚠️ Forcing `PYTHONIOENCODING=utf-8` by hand got further and then died again,
this time READING a child process: `subprocess.run(..., text=True)` decodes with
the locale encoding, not the child's. ⛔ The user had to discover
`PYTHONUTF8=1 PYTHONIOENCODING=utf-8` on their own — and a system that requires
two environment variables nobody documented is a system that does not run.

⭐ THE ENGINE'S OWN RULE APPLIES TO ITSELF: a rule that lives in a document is
followed 40-60% of the time. "Remember to pass encoding= on every subprocess
call" is such a rule, and there are 84 of those calls. ⛔ So it is not a rule —
it is this import.

⭐ Import it FIRST, before anything writes output:

    import utf8            # noqa: F401 — imported for its side effect

⚠️ It changes nothing on a system that is already UTF-8, which is why it is safe
to put at the top of everything.
"""
import io
import os
import subprocess
import sys

# ── ① what THIS process writes ──────────────────────────────────────────────
# ⛔ `reconfigure` exists from 3.7; a stream that is not a TextIOWrapper (a pipe
# replaced by a test harness, for instance) simply has no such method, and that
# is not an error worth raising over output encoding.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, io.UnsupportedOperation):
        pass

# ── ② what its CHILDREN write back ──────────────────────────────────────────
# ⭐ A child of this process inherits the environment, so setting these two
# means every validator, probe and hook this engine spawns speaks UTF-8 too —
# ⛔ including the ones spawned by code that never imported this module.
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
os.environ.setdefault("PYTHONUTF8", "1")

# ── ③ what THIS process reads back from them ────────────────────────────────
# 🔴 The half that bit hardest: `text=True` decodes with the LOCALE encoding,
# so a child correctly writing UTF-8 was still decoded as cp1252 and raised
# `UnicodeDecodeError` inside a reader thread — a crash with no line of ours in
# the traceback. ⭐ Defaulting encoding and errors on every call fixes all 84
# without touching one, and an explicit `encoding=` at a call site still wins.
_run = subprocess.run


def _run_utf8(*args, **kw):
    if kw.get("text") or kw.get("universal_newlines"):
        kw.setdefault("encoding", "utf-8")
        kw.setdefault("errors", "replace")
    return _run(*args, **kw)


subprocess.run = _run_utf8
