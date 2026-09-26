#!/usr/bin/env python3
"""gate-run — ONE interpreter per action, instead of one per gate.

🔴 THE FAILURE, measured 2026-09-09 on a real Windows installation. Seven gates
were wired as seven separate hook commands, so the host started a fresh Python
for each one. Measured on that machine:

    python -c 'pass'                     173 ms
    one gate, end to end               ~250 ms   ⛔ 70% of it is the interpreter
    one Bash command → 5 gates          2184 ms
    one Read           → 1 gate          306 ms

    a session of 40 commands, 60 reads, 20 writes:
        85 s of gates, of which 59 s is Python starting up 340 times

⛔ AND THAT IS WHY IT FEELS LIKE IT GROWS. The cost is per ACTION, so the longer
the session runs the more it accumulates — the owner reported exactly that:
"el tiempo que se está tardando está pasando factura, como que va aumentando".
⚠️ Nothing was leaking and no gate was slow: the work inside them is ~50 ms.

⭐ THE FIX IS STRUCTURAL, not an optimisation of any gate. This one command is
wired in their place, reads the payload ONCE, and calls each gate's `main()` in
this same interpreter. Seven starts become one.

⛔ WHAT IT MUST NOT CHANGE, and every one of these is a rule some gate paid for:
  · the FIRST refusal wins and the rest do not run — a gate that refuses has
    already decided, and running the others would print advice about work that
    is not going to happen
  · a gate that CRASHES never takes the work with it (ADR-012), except
    gate-secrets, which fails CLOSED on purpose: its worst case is a credential
    on disk, and that is not revertible
  · every gate still leaves its own beat, so `check-gates` sees them exactly as
    before
  · stdout, stderr and the exit code are the gate's own — the host cannot tell
    the difference. ⭐ ONE exception, and it is what keeps that promise: when
    two gates each print a decision, the host would receive two JSON objects
    and read NEITHER (measured 2026-09-26: `Extra data: line 2`). So decisions
    are held and leave as ONE — the strictest (deny > ask > allow), carrying
    every gate's reason. A single decision leaves byte-for-byte as printed.

Usage (wired by bin/init, not typed):
  gate-run.py <gate> [<gate> ...]        # payload on stdin
Exit: the first non-zero a gate returned · 0 if all allowed
"""
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
import importlib.machinery as _m                      # noqa: E402
import importlib.util as _u                           # noqa: E402
import io                                             # noqa: E402
import json                                           # noqa: E402
import os                                             # noqa: E402
import sys                                            # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# ⛔ THE ONE GATE THAT FAILS CLOSED. Every other gate exits 0 on its own crash —
# a guard that dies must not lock the person out of their machine (ADR-012).
# gate-secrets is the exception it declares itself: its worst case is a
# credential written to disk, and a leaked secret is ROTATED, never deleted.
FAILS_CLOSED = {"gate-secrets"}


def load(name):
    """Import a gate by file name, without running its __main__ guard."""
    path = os.path.join(HERE, name + ".py")
    if not os.path.exists(path):
        return None
    ld = _m.SourceFileLoader("_g_" + name.replace("-", "_"), path)
    mod = _u.module_from_spec(_u.spec_from_loader(ld.name, ld))
    ld.exec_module(mod)
    return mod


RANK = {"allow": 1, "ask": 2, "deny": 3}


def decision_of(text):
    """→ the hookSpecificOutput dict when `text` is ONE PreToolUse decision, else None."""
    try:
        d = json.loads(text)
    except ValueError:
        return None
    h = d.get("hookSpecificOutput") if isinstance(d, dict) and len(d) == 1 else None
    if isinstance(h, dict) and h.get("permissionDecision") in RANK:
        return h
    return None


def emit(held):
    """Print the held decisions as ONE: the strictest, with every reason."""
    if not held:
        return
    if len(held) == 1:
        sys.stdout.write(held[0][1])       # ⭐ alone → exactly what the gate printed
        return
    hs = sorted((h for h, _ in held), key=lambda h: -RANK[h["permissionDecision"]])
    out = {"hookEventName": hs[0].get("hookEventName", "PreToolUse"),
           "permissionDecision": hs[0]["permissionDecision"],
           "permissionDecisionReason": "\n\n".join(
               h["permissionDecisionReason"] for h in hs
               if h.get("permissionDecisionReason"))}
    ctx = [h["additionalContext"] for h in hs if h.get("additionalContext")]
    if ctx:
        out["additionalContext"] = "\n\n".join(ctx)
    print(json.dumps({"hookSpecificOutput": out}))


def run_one(mod):
    """→ (rc, what it printed). Its stdout is HELD, so decisions can be merged."""
    buf, real = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        try:
            rc = mod.main()
        except SystemExit as e:
            # ⭐ A gate that calls sys.exit() inside main() still decides.
            rc = e.code if isinstance(e.code, int) else 0
        return rc, buf.getvalue()
    finally:
        sys.stdout = real


def main():
    names = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not names:
        # ⬜ Nothing to run is not a refusal — a dispatcher with no arguments is
        # a wiring mistake, and locking the person out over it would be worse
        # than the mistake.
        print("⬜ gate-run · no gate named · nothing was checked",
              file=sys.stderr)
        return 0

    raw = sys.stdin.read()
    held = []
    for name in names:
        # ⭐ EACH GATE GETS ITS OWN stdin, rewound. ⛔ They call
        # `json.load(sys.stdin)` — a stream the previous gate already consumed
        # answers nothing, and the gate would silently allow.
        sys.stdin = io.StringIO(raw)
        try:
            mod = load(name)
            if mod is None:
                print("⬜ gate-run · %s not found · NOT MEASURED" % name,
                      file=sys.stderr)
                continue
            rc, said = run_one(mod)
        except Exception as e:                        # noqa: BLE001
            # 🔴 CHK-CAU-002 · a crash is a VERDICT, and which verdict depends
            # on what the gate protects. ⛔ Answering the same way for all of
            # them would either lock the owner out over a bug, or let a
            # credential through on one.
            print("⬜ %s could not run · %s · NOT MEASURED"
                  % (name, type(e).__name__), file=sys.stderr)
            if name in FAILS_CLOSED:
                return 2
            continue
        h = decision_of(said) if said.strip() else None
        if h is not None:
            held.append((h, said))
        elif said:
            sys.stdout.write(said)
        if rc:
            # ⛔ THE FIRST REFUSAL WINS. A gate that refused has decided; the
            # others would print advice about work that is not happening.
            emit(held)
            return rc
    emit(held)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:                            # noqa: BLE001
        print("⬜ gate-run could not run · %s · NOT MEASURED"
              % type(e).__name__, file=sys.stderr)
        sys.exit(0)
