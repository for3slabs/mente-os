#!/usr/bin/env python3
"""gate-critical — the few actions that BLOCK, each at the level it earned.

Implements ADR-012 · a small named set blocks, everything else warns. ⛔ A gate
that obstructs more than it protects degrades to a warning, because a system
that gets in the way gets switched off — and a switched-off gate protects
nothing, including the case it was right about.

⬜ WHICH actions block is the installation's: what is destructive depends on what
is being built. The engine ships the two it can measure from its own rules, and
a declarable slot for the third.

Contract: a PreToolUse payload on stdin · exit 0 allow · exit 2 BLOCK.
"""
import os, re, sys, json, subprocess
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
import plat                                          # noqa: E402

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beat import beat                                         # noqa: E402
sys.path.insert(0, os.path.join(MENTE, "bin"))
from blockread import body_of                                  # noqa: E402

# ⬜ CFG · what this installation considers irreversible. Unset means the engine
# guards nothing here — ⛔ and says so rather than guessing, because a pattern
# chosen elsewhere guards somebody else's idea of destructive.
IRREVERSIBLE = os.environ.get("MENTE_IRREVERSIBLE_PATTERN", "")

# ⛔ A CLOSED state is declared by a WHITELIST, inverted. Measured: a new status
# word appeared in a real block and the gate let a close through with open work
# — a vocabulary nobody had seen opened a hole in a safety gate, silently.
# ⭐ Anything that does not MEAN closed counts as open.
CLOSED_WORDS = re.compile(r"^\s*(closed|done|shipped|archived|—|-)\s*$", re.I)


def payload_target(payload):
    """The file and body an action is about — ⛔ every field type checked.
    `json.load` accepts any valid JSON: with `[]` the parse SUCCEEDS and the
    first `.get()` raises. A hook that raises prints a trace and lets the action
    through: it does not protect, it only looks like it."""
    if not isinstance(payload, dict):
        return "", ""
    ti = payload.get("tool_input")
    if not isinstance(ti, dict):
        return "", ""
    target = ti.get("file_path")
    if not isinstance(target, str) or not target:
        return "", ""
    body = ti.get("content") or ti.get("new_string") or ""
    return target, body if isinstance(body, str) else ""


def refuse(reason, way_out):
    """⭐ Every refusal prints four things (ADR-030): what, why, what to assess,
    and the documented way out. ⛔ A gate with no way out is deleted."""
    print("🔴 BLOCKED · %s\n   %s" % (reason, way_out), file=sys.stderr)
    return 2


def gate_close(target, body):
    """🔴 BLOCKS · a block that closes without passing its own contract.

    ⭐ The engine does not JUDGE sufficiency — contract-block §11 says that is
    the one test a script cannot do. It verifies the judgement was RECORDED,
    which check-block already measures (BLK-TRN-001)."""
    if not target.endswith("BLOCK.md"):
        return 0
    # ⛔ re.I: a status in capitals evaded a case-sensitive guard entirely.
    # Markdown is written by people; a case-sensitive gate has a typo-sized hole.
    if not re.search(r"^status:\s*closed", body, re.M | re.I):
        return 0

    name = os.path.basename(os.path.dirname(target))
    # 🔴 CHK-QUI-001 · `--quiet` is the EXIT CODE ONLY, and this used to read the
    # NAME out of a quiet run's output — which is empty by contract. ⛔ The
    # condition could never be true, so this gate silently let every
    # insufficient close through. ⚠️ Found only by exercising the gates against
    # a real installation; every probe was green, because a probe measures the
    # gate and not the pair.
    # ⭐ Two calls: the quiet one decides whether anything is wrong, the second
    # says WHICH block — and only that second answer can name this one.
    checker = os.path.join(MENTE, "bin", "check-block")
    # 🔴 plat.script, NEVER the bare path. Measured on Windows 2026-09-02 by an
    # external audit: `subprocess.run([checker, "--quiet"])` raised
    # FileNotFoundError because CreateProcess does not read the `#!` line, the
    # except below swallowed it, and THIS GATE LET EVERY INSUFFICIENT CLOSE
    # THROUGH — while looking wired in `.claude/settings.json`.
    try:
        if subprocess.run(plat.script(checker, "--quiet"), capture_output=True,
                          timeout=30).returncode == 0:
            return 0        # nothing is wrong with any block
        r = subprocess.run(plat.script(checker), capture_output=True, text=True,
                           timeout=30)
    except Exception as e:
        # 🔴 A GATE THAT CANNOT MEASURE MUST SAY SO. ⛔ This returned 0 in
        # silence, which is indistinguishable from "I checked and it is fine" —
        # the exact shape `rules/rule-checks-must-measure.md` forbids, and how
        # a dead gate stayed invisible on an entire platform.
        # ⭐ It still does not BLOCK: refusing on a broken validator would stop
        # work over a defect that is ours. But it is never again silent.
        print("⬜ NOT MEASURED · gate-critical could not run check-block (%s) · "
              "⚠️ whether this close is sufficient was NOT checked"
              % e.__class__.__name__, file=sys.stderr)
        return 0
    if name in r.stdout:
        return refuse(
            "block `%s` does not meet its contract and cannot close" % name,
            "run: Mente/bin/check-block — it names what is missing")

    # ⚠️ An open child is measured on the file BEING WRITTEN, not on disk: the
    # edit is what would close it, and disk still holds the previous state.
    for row in re.findall(r"^\|[^|]*\|[^|]*\|[^|]*\|\s*([^|]+?)\s*\|",
                          body_of(body, "F") or "", re.M):
        # ⚠️ `estado` is not engine language — it is a HEADER an owner may have
        # typed in their own. ⛔ Reading a table's header row as a sub-block
        # would refuse every close on a table written that way, and the refusal
        # would be impossible to understand. Input tolerance, never doctrine:
        # what this engine WRITES is English, what it READS may not be.
        if row and not CLOSED_WORDS.match(row) and row.lower() not in ("state", "estado"):
            return refuse(
                "block `%s` still has an open sub-block: `%s`" % (name, row[:24]),
                "⛔ a parent does not close over unfinished children — close it, "
                "move it, or say where it went")
    return 0


def gate_irreversible(target, body):
    """🔴 BLOCKS · ⬜ an action this installation declared irreversible."""
    if not IRREVERSIBLE:
        return 0            # ⬜ nothing declared · nothing guarded, and it is said at startup
    try:
        if re.search(IRREVERSIBLE, body or "", re.I):
            return refuse(
                "%s matches the declared irreversible pattern"
                % os.path.basename(target),
                "⭐ a mistake with no undo is the one case worth blocking · "
                "state in the block why it must happen here, or make it reversible")
    except re.error:
        pass                # ⛔ a malformed pattern must not block every edit
    return 0


def warn_propagation(target):
    """⚠️ WARNS, deliberately. Measured elsewhere: blocking the daily path is
    pure friction, and the lane rule already forces the ceremony up."""
    blocks = os.path.join(MENTE, "work", "blocks")
    for root, _, files in os.walk(blocks):
        if "BLOCK.md" not in files:
            continue
        try:
            text = open(os.path.join(root, "BLOCK.md"),
                        encoding="utf-8", errors="replace").read()
        except OSError:
            continue        # ⬜ unreadable · skipped, never treated as clean
        for row in re.finditer(r"^\|[^|]*\|([^|]*)\|[^|]*\|\s*(\d+)\s*\|", text, re.M):
            piece, deps = row.group(1).strip().strip("`"), int(row.group(2))
            if piece and len(piece) > 4 and piece in target and deps >= 5:
                print("⚠️  %s propagates to %d files — lane `full-block`.\n"
                      "   ⛔ A fix that ignores %d consumers is a patch."
                      % (piece, deps, deps), file=sys.stderr)
                return


def main():
    # ⭐ Proof this gate still fires. A gate is silent both when it has nothing
    # to block and when it stopped running; the stamp is what separates those.
    # Read by bin/check-gates — ⛔ never by this file, which must not depend on
    # its own telemetry (hooks/_beat.py).
    beat(MENTE, "gate-critical")
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0            # malformed input never blocks
    target, body = payload_target(payload)
    if not target:
        return 0

    for gate in (gate_close, gate_irreversible):
        code = gate(target, body)
        if code:
            return code
    warn_propagation(target)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        # ⛔ Even a crash must not block: a guard that dies must not take the
        # work with it. It reports and lets the action through.
        print("⚠️  gate-critical · %s: %s" % (type(e).__name__, e), file=sys.stderr)
        sys.exit(0)
