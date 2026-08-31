"""_beat — every gate leaves proof it still fired.

⭐ THE BLIND SPOT THIS CLOSES. A gate is silent in both of its states: silent
because nothing needed blocking, and silent because it stopped running. From the
inside, on the day it happens, those are the same observation — a missing
warning looks exactly like a healthy system.

It IS distinguishable afterwards. A gate that stamps a date turns "it said
nothing" into "it has said nothing since <date>", and a validator can read that.
⛔ Without a stamp, a gate can be unwired from the host's settings and every
block it would have raised is simply gone, with nothing anywhere saying so.

⭐ WHY THE STAMP IS DAILY AND NOT PER CALL. A gate runs on the hot path — once
per edit, which in a working session is hundreds of times. Writing on every call
would put two disk writes on every keystroke path, and this system's own rule is
that a guard costing more than it protects gets switched off. So the beat is
written ONLY when the date changes: one write per gate per day, and a cheap read
the rest of the time. ⚠️ The signal is unchanged — the question a reader asks is
"did this gate fire today", never "how many times".

⛔ NEVER RAISES. Telemetry that breaks the thing it measures is worse than no
telemetry: a hook that must not block would start blocking, and a gate that must
block for its own reasons would fail for someone else's.

Not a hook — a shared helper. The `_` prefix says so (hooks/README).
"""
import os
from datetime import date

DIR = ".beats"

# ⭐ LOCAL, and this is a decision, not a default. The first version stamped UTC
# while every reader compared against the local date — so west of UTC each gate
# looked a day staler than it was, and at a 7-day threshold a gate quiet for six
# days got reported dead. ⛔ The bug is not the timezone; it is USING TWO of them
# for the two halves of one subtraction.
# ⚠️ Local is the right half to standardise on because the other dates in this
# system are written by a person, in a document, in their own day.
# Found by probe-gates case ① on its first run, 2026-08-30.


def _path(mente, name):
    return os.path.join(mente, DIR, name)


def beat(mente, name):
    """Record that `name` fired today. Cheap on every call after the first."""
    try:
        today = date.today().isoformat()
        p = _path(mente, name)
        # ⭐ The read is the whole point: every call but the day's first stops
        # here without writing. Reading a ~10-byte file is what makes a daily
        # stamp affordable on a path that runs hundreds of times.
        try:
            if open(p, encoding="utf-8").read().strip() == today:
                return
        except OSError:
            pass
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(today)
    except Exception:                                          # noqa: BLE001
        return          # ⛔ telemetry never breaks the gate it is measuring


def last(mente, name):
    """The date `name` last fired, or None if it never did or cannot be read.

    ⚠️ None is deliberately ambiguous between "never fired" and "unreadable".
    The caller reports it as NOT MEASURED rather than as a pass — an unreadable
    stamp is not evidence that a gate is alive.
    """
    try:
        return date.fromisoformat(
            open(_path(mente, name), encoding="utf-8").read().strip())
    except (OSError, ValueError):
        return None


def all_beats(mente):
    """Every gate that has ever stamped here → its date. Used by the reader."""
    d = os.path.join(mente, DIR)
    try:
        names = sorted(n for n in os.listdir(d) if not n.startswith("."))
    except OSError:
        return {}
    return {n: last(mente, n) for n in names}
