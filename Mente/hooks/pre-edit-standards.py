#!/usr/bin/env python3
"""pre-edit-standards — name a block's standards before its files are touched.

Implements layer 3 of ADR-011 · a standard that is merely findable is not read.
Touch a file a block claims, and that block's standards are named back in the
same turn — ⛔ before the edit, because after it they are a review, not a guide.

⛔ It NEVER blocks. Blocking on a path match would make editing unbearable, and
an unbearable guard is deleted — which protects nothing at all.

Contract: a PreToolUse payload on stdin · always exit 0.
"""
import os, re, sys, glob, json

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beat import beat                                         # noqa: E402
sys.path.insert(0, os.path.join(MENTE, "bin"))
from blockread import body_of                                  # noqa: E402

BLOCKS = os.path.join(MENTE, "work", "blocks")
CAMPAIGNS = os.path.join(MENTE, "work", "campaigns")


def read(path):
    """⛔ Never raises. A hook that dies leaves the editor with NO standards —
    worse than injecting too few, because the failure is silent and reads as
    'there was nothing to say'."""
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def declared_paths(scope):
    """The paths a scope section CLAIMS.

    ⭐ Mentioning a path is not claiming it. Only the part of an item BEFORE the
    prose counts — ⛔ otherwise the block that explains most steals the files of
    the one that owns them, and the editor gets the wrong standards. The damage
    is not an extra warning: it is the CORRECT warning that no longer arrives."""
    out = []
    for line in scope.splitlines():
        m = re.match(r"\s*[-*]\s*(.*)", line)
        if not m:
            continue                       # a continuation line claims nothing
        for tok in re.findall(r"[\w./-]+/[\w./*-]*", m.group(1).split("—")[0]):
            p = tok.split("*")[0].rstrip("/")
            if len(p) > 4:
                out.append(p)
    return out


def owns(scope, target):
    """⛔ Compared by SEGMENTS, never as a substring: `lib/demo` matches inside
    `other-lib/demo-old/x.ts` and the wrong block answers."""
    seg = [s for s in target.split("/") if s]
    for p in declared_paths(scope):
        parts = [s for s in p.split("/") if s]
        if any(seg[i:i + len(parts)] == parts for i in range(len(seg))):
            return True
    return False


def listed(section):
    """The entries of a bullet list — the shape both §D and a campaign use."""
    return [m.group(1) for m in re.finditer(r"^\s*[-*]\s*`?([^`\s]+)`?", section, re.M)]


def campaign_of(block):
    """⭐ Membership is declared by the CAMPAIGN, never by the block: a block
    cannot adopt itself into looser standards, nor be orphaned by forgetting to
    declare one. Returns (name, [inherited])."""
    for path in sorted(glob.glob(os.path.join(CAMPAIGNS, "*", "CAMPAIGN.md"))):
        text = read(path)
        if block not in (body_of(text, "F") or "") and block not in text:
            continue
        return os.path.basename(os.path.dirname(path)), listed(body_of(text, "D") or "")
    return None, []


def main():
    # ⭐ Proof this hook still fires — see bin/check-gates. An injector that
    # stops running looks exactly like a session where nothing was owned.
    beat(MENTE, "pre-edit-standards")
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0                           # malformed input never blocks
    # ⛔ `json.load` accepts any valid JSON, not only an object: with `[]` the
    # parse SUCCEEDS and `.get()` raises. A hook that raises prints a traceback
    # and lets the action through — it does not protect, it only looks like it.
    if not isinstance(payload, dict):
        return 0
    ti = payload.get("tool_input")
    target = ti.get("file_path", "") if isinstance(ti, dict) else ""
    if not target:
        return 0

    open_blocks = []
    for bpath in sorted(glob.glob(os.path.join(BLOCKS, "**", "BLOCK.md"),
                                  recursive=True)):
        text = read(bpath)
        # ⭐ BLK-SCP-005 needs to know which blocks were OPEN, not only which
        # one owns the file — "outside every scope" means nothing when there is
        # no scope to be outside of.
        if re.search(r"^status:\s*(active|open)\b", text, re.M | re.I):
            open_blocks.append(os.path.basename(os.path.dirname(bpath)))
        if not owns(body_of(text, "B") or "", target):
            continue

        name = os.path.basename(os.path.dirname(bpath))
        own = listed(body_of(text, "D") or "")
        camp, inherited = campaign_of(name)

        # ⭐ INHERITED, never copied: the campaign's standards are READ on every
        # edit. Copying them into the child makes the two lists diverge, and a
        # child may ADD but never remove (ADR-025 · rule-inheritance).
        head = "📦 %s → block `%s`" % (target, name)
        lines = [head + (" · campaign `%s` — standards apply:" % camp if camp
                         else " — §D standards apply:")]
        lines += ["   · %s   ⬅ from the campaign" % s for s in inherited]
        lines += ["   · %s" % s for s in own if s not in inherited]
        if not own and not inherited:
            lines.append("   🔴 §D declares no standard — nothing can be "
                         "rejected on any basis (BLK-STD-001)")

        # ⚠️ An OPEN sub-block covering this file is the fix-over-fix shape the
        # block exists to stop: work already in progress on the same piece.
        for row in re.findall(r"^\|[^|]*\|([^|]*)\|([^|]*)\|[^|]*\|\s*(\w+)\s*\|",
                              body_of(text, "F") or "", re.M):
            piece, state = row[1].strip().strip("`"), row[2].strip()
            if piece and len(piece) > 4 and piece in target and state != "closed":
                lines.append("   ⚠️  a sub-block for this file is `%s`: %s"
                             % (state, row[0].strip()))

        print("\n".join(lines), file=sys.stderr)
        return 0

    # ── ⭐ BLK-SCP-005 · an edit outside every declared scope ────────────────
    # ⛔ Scope creep is the characteristic failure of an agent: it discovers a
    # dependency and decides on its own that it is in scope. ⚠️ The boundary was
    # written and nothing watched it, so it held exactly as long as attention
    # did.
    #
    # ⛔ IT REPORTS, IT DOES NOT BLOCK. Most edits in a tree are legitimately
    # outside every open block, and a gate that stops them stops the work — then
    # it is removed, and the real drift goes unnoticed too. ⭐ What was missing
    # is not permission; it is NOTICING, out loud, at the moment it happens.
    if open_blocks:
        print("⚠️  %s is outside the scope of every open block (%s).\n"
              "   ⭐ If this edit belongs to one, its §B IN should say so — "
              "widening a scope\n"
              "   is a decision, and it goes in §G (BLK-SCP-004).\n"
              "   ⛔ If it does not belong to any, that is the answer: this is "
              "work nobody opened."
              % (os.path.relpath(target, os.path.dirname(MENTE))
                 if target.startswith(os.path.dirname(MENTE)) else target,
                 ", ".join(open_blocks[:3])), file=sys.stderr)
    # ⬜ With no block open there is no scope to be outside of, and saying
    # anything would be noise on every edit in a tree nobody has opened work in.
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        # ⛔ Even the guard must not block: report and let the edit through.
        print("⚠️  pre-edit-standards · %s: %s" % (type(e).__name__, e),
              file=sys.stderr)
        sys.exit(0)
