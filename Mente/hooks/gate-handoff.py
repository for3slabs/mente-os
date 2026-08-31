#!/usr/bin/env python3
"""gate-handoff — a specialist that can WRITE does not launch without a declared scope.

Turns rules/contract-handoff.md from an intention into a gate: a rule enforced by
code is followed; a rule that lives only in a document is followed about half the
time, and this one is about an agent nobody is watching.

⭐ THE LEVEL WAS MEASURED, AND THE MEASUREMENT INVERTED THE DIAGNOSIS. Counting a
project's real tool calls showed shell and file operations in the thousands and
delegations in the dozens — half of those read-only. ⛔ The failure was never
delegating BADLY. It was not delegating at all, until one context collapsed under
work that should have been handed off.

| the specialist can… | level | why |
|---|---|---|
| WRITE | 🔴 **BLOCK** | an unbounded writer inside a bounded system |
| only READ | ⚠️ pass | it corrupts nothing, and this is the delegation that was MISSING |

⚠️ That asymmetry is the whole design. Blocking a cheap reader would make
delegation cost more than doing the work inline — pushing straight back toward
the behaviour that caused the collapse.

⛔ THE LEVEL IS NOT DECIDED BY THE AGENT'S NAME. A list of read-only names is
correct exactly until somebody adds another type, and then the gate is silently
permissive for the one nobody reviewed. ⭐ The manifest DECLARES its capabilities
(HND-GAT-004), and anything undeclared is assumed present (HND-GAT-005): the safe
reading of silence is the permission being absent, never the restriction.

⭐ AND PRESENCE IS NOT COMPLIANCE (HND-GAT-002). The manifest is verified by
bin/check-handoff — ⛔ never merely found on disk. An unfilled template is a file
that exists and answers nothing, and "a file is there" reads exactly like "the
question was answered".

⬜ MENTE_HANDOFF_BYPASS=1 · the escape hatch, and it announces itself
(HND-GAT-003). A gate with no way out gets deleted; a silent bypass is a gate
that was already removed and nobody noticed.

Contract: PreToolUse payload on stdin · exit 0 allow · exit 2 BLOCK.
"""
import json
import os
import subprocess
import sys

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beat import beat                                         # noqa: E402

CHECK = os.path.join(MENTE, "bin", "check-handoff")
# ⬜ Agent types this installation knows CANNOT write. ⛔ Empty by default, and
# that default is the safe one: HND-GAT-005 says an undeclared capability is
# assumed PRESENT, so an unlisted type is a writer and needs a scope.
# ⚠️ This is a declaration, not a name list the engine maintains — the engine
# shipping names would be the loose comparison the contract rejects, correct
# exactly until the host adds another type.
READ_ONLY = {t.strip().lower()
             for t in (os.environ.get("MENTE_HANDOFF_READONLY") or "").split(",")
             if t.strip()}
BLOCKS = os.path.join(MENTE, "work", "blocks")
# ⬜ Which launch tool this host uses. Unset means the common name.
LAUNCH = os.environ.get("MENTE_HANDOFF_TOOL", "Agent")


def manifests():
    """Every manifest on disk, newest first. ⭐ Newest is a starting order, not
    a verdict — each is still verified, and an old one that binds beats a new
    one that does not."""
    found = []
    for dp, dn, fn in os.walk(BLOCKS):
        if os.path.basename(dp) != "handoffs":
            continue
        for n in fn:
            if n.endswith((".yml", ".yaml")):
                found.append(os.path.join(dp, n))
    return sorted(found, key=lambda p: os.path.getmtime(p), reverse=True)


def bound(path):
    """True only when bin/check-handoff says the manifest is well-formed AND
    bound to a real block. ⛔ Any other outcome — malformed, unbound, crashed,
    missing — is NOT a pass: a gate that opens because its checker failed is
    the paperwork version of a scope."""
    try:
        return subprocess.run([sys.executable, CHECK, path, "--quiet"],
                              capture_output=True, timeout=20).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def main():
    beat(MENTE, "gate-handoff")     # proof this gate still fires (bin/check-gates)
    try:
        payload = json.load(sys.stdin)
    except Exception:                                          # noqa: BLE001
        return 0
    if not isinstance(payload, dict):
        return 0
    if (payload.get("tool_name") or "") != LAUNCH:
        return 0                    # not a delegation — no business of this gate
    ti = payload.get("tool_input")
    if not isinstance(ti, dict):
        ti = {}

    kind = ti.get("subagent_type")
    kind = kind.strip() if isinstance(kind, str) else ""
    desc = ti.get("description")
    desc = desc.strip() if isinstance(desc, str) else ""

    # ⬜ THE ESCAPE HATCH, LOUD ON PURPOSE (HND-GAT-003). ⛔ Checked before the
    # verdict so the reason is printed even when a manifest would have blocked:
    # a bypass whose cost is invisible is one that becomes the normal path.
    if os.environ.get("MENTE_HANDOFF_BYPASS") == "1":
        print("🟡 HANDOFF GATE BYPASSED · MENTE_HANDOFF_BYPASS=1\n"
              "   Launching `%s` with NO declared scope.\n"
              "   Nothing records what it may read, where it may write, or when "
              "it must stop.\n"
              "   If it writes outside the block, no validator will catch it."
              % (kind or "a specialist"), file=sys.stderr)
        return 0

    # ⭐ THE LEVEL COMES FROM CAPABILITY, NEVER FROM THE TASK'S WORDING
    # (HND-GAT-004). A specialist that cannot write has no write scope to
    # declare, and demanding a manifest for it would make the cheapest
    # delegation the most expensive — ⛔ pushing the work back inline, which is
    # the collapse this whole contract exists to prevent.
    # ⚠️ Measured defect, found by attacking this gate: without this branch a
    # read-only agent passed only when an UNRELATED manifest happened to exist,
    # and was blocked when none did. The verdict depended on other people's
    # paperwork rather than on what the agent could do.
    if kind.lower() in READ_ONLY:
        print("⚠️  `%s` is declared read-only — no manifest required.\n"
              "   It returns a conclusion and writes nothing. ⛔ If it ever "
              "needs to WRITE,\n"
              "   it needs a scope first (rules/contract-handoff.md)." % kind,
              file=sys.stderr)
        return 0

    ok = [m for m in manifests() if bound(m)]
    if ok:
        print("✅ handoff gate · bounded by %s\n"
              "   ⚠️ Check the objective matches THIS task — a stale manifest is "
              "a scope for different work." % os.path.relpath(ok[0], MENTE),
              file=sys.stderr)
        return 0

    total = len(manifests())
    # ⭐ The two states are reported differently on purpose: "none exists" and
    # "one exists and does not bind" call for different actions, and collapsing
    # them into one message sends the reader to look in the wrong place.
    detail = ("   %d manifest(s) on disk, none passing bin/check-handoff — "
              "presence is not compliance.\n" % total if total else
              "   No handoff manifest exists for any block.\n")

    print("🔴 BLOCKED · `%s` may WRITE and has no declared scope.\n"
          "%s%s"
          "   An unbounded writer inside a bounded system is what the manifest "
          "exists to stop:\n"
          "   what it may read · what it must do · where it may write · when it "
          "must stop.\n\n"
          "   Fix (rules/contract-handoff.md):\n"
          "     1. cp templates/handoff.yml.template \\\n"
          "          work/blocks/<block>/handoffs/<id>.yml\n"
          "     2. fill it in — every placeholder is rejected\n"
          "     3. bin/check-handoff <that file>      # must exit 0\n\n"
          "   ⭐ Not worth a manifest? Then it is not worth a specialist — do it "
          "inline\n"
          "   (contract-handoff.md §12). ⬜ Bypass: MENTE_HANDOFF_BYPASS=1, and "
          "it says so."
          % (kind or "specialist",
             "   Task: %s\n" % desc[:70] if desc else "",
             detail),
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:                                     # noqa: BLE001
        # ⛔ CHK-CAU-002, answered the way gate-critical answers it and NOT the
        # way gate-secrets does. A crash here fails OPEN: the worst case is an
        # unbounded specialist, which is visible in its own output and
        # reversible. ⚠️ Failing closed would make a broken gate block every
        # delegation — pushing the work back inline, which is the exact
        # behaviour this contract exists to prevent.
        print("⚠️  gate-handoff could not complete its check (%s: %s) — "
              "letting the launch through.\n"
              "   ⛔ Nothing verified the scope of this specialist."
              % (type(e).__name__, e), file=sys.stderr)
        sys.exit(0)
