#!/usr/bin/env python3
"""watch-external — notice that the world moved, before acting on a stale view.

⭐ Some state lives outside this repository and changes without telling anybody:
a review merged elsewhere, a deploy, a queue. ⛔ Working on a stale view of it
is not caught by any validator here — the tree is consistent, and wrong.

⬜ WHAT to consult is the installation's: the engine ships WHEN to look and how
to report, never which service. Unset means nothing is watched, and it says so.

Contract: a PreToolUse payload on stdin · always exit 0 · never blocks.
"""
import os, re, sys, json, time, subprocess

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ⬜ The command that answers "did anything change?" — exit 1 means yes.
WATCH_CMD = os.environ.get("MENTE_WATCH_COMMAND", "")
# ⬜ Actions a change would invalidate. ⭐ Before one of these it looks ALWAYS.
URGENT = os.environ.get("MENTE_WATCH_URGENT",
                        r"\bgit\s+(push|commit|merge|rebase|switch\s+-c|checkout\s+-b)\b")
# ⬜ Minutes between looks on everything else.
TRUCE_MIN = int(os.environ.get("MENTE_WATCH_TRUCE_MIN", "10") or 10)
STAMP = os.path.join(MENTE, "cache", "watch-external.stamp")


def is_urgent(payload):
    """⭐ Look ALWAYS before the action a change would invalidate — that is the
    only instant the warning is worth anything."""
    ti = payload.get("tool_input") if isinstance(payload, dict) else None
    cmd = ti.get("command", "") if isinstance(ti, dict) else ""
    try:
        return bool(isinstance(cmd, str) and re.search(URGENT, cmd))
    except re.error:
        return False        # ⛔ a malformed pattern must not make every action urgent


def truce_holds():
    """⚠️ The truce is not comfort. ⭐ Consulting on every action turns the
    warning into noise, and noise is ignored — which is how a validator dies.

    ⛔ But a detector that only looks before the urgent action is blind during
    all the work that is not urgent, which is most of it. Measured: a change
    landed and nothing fired, because no urgent command ran in between."""
    try:
        return time.time() - os.path.getmtime(STAMP) < TRUCE_MIN * 60
    except OSError:
        return False        # no stamp · first look of the session


def stamp():
    try:
        os.makedirs(os.path.dirname(STAMP), exist_ok=True)
        open(STAMP, "w").close()
    except OSError:
        pass                # ⬜ cannot record · looks again next time, never blocks


def ask():
    """Run the declared command. ⛔ Absent tool, no network or a timeout is not
    a reason for noise — it is a reason for silence."""
    try:
        r = subprocess.run(WATCH_CMD, shell=True, cwd=MENTE,
                           capture_output=True, text=True, timeout=20)
    except Exception:
        return None
    return r if r.returncode == 1 else None      # ⬜ 0 nothing new · other: could not tell


def main():
    if not WATCH_CMD:
        return 0            # ⬜ nothing declared · nothing watched · session-start says so
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if not isinstance(payload, dict):
        return 0

    if not is_urgent(payload) and truce_holds():
        return 0
    stamp()

    r = ask()
    if r is None:
        return 0

    detail = (r.stdout or "").strip()[:400]
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",       # ⛔ informs · a warning that cuts work is disabled
        "permissionDecisionReason":
            "🔀 External state changed since the last look:\n" + detail +
            "\n→ verify the work travelled before acting on the previous view."
    }}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("⚠️  watch-external · %s: %s" % (type(e).__name__, e), file=sys.stderr)
        sys.exit(0)
