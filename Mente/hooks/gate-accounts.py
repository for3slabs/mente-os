#!/usr/bin/env python3
"""gate-accounts — layer 1: nothing leaves toward a destination nobody declared.

⭐ WHY IT EXISTS, measured. A clone with two remotes had work pushed to one and
not the other, and the two diverged for weeks with nothing reporting it — the
alarm came from a person looking by hand. ⛔ And the worse case is not that one:
it is pushing to a repository that is not in the registry at all. The work leaves
the system and nobody knows where it went, because an undeclared repository has
no owner, no stated reason to exist, and no access guide.

── THE FOUR ANSWERS ────────────────────────────────────────────────────────────
| situation                              | answer | why                          |
|----------------------------------------|--------|------------------------------|
| push to a REGISTERED repository        | allow  | a declared, known destination |
| ⛔ push to one marked RETIRED           | deny   | it receives no work           |
| push to an UNREGISTERED repository     | deny   | fail closed: no owner declared |
| creating, deleting or exposing a repo  | ask    | ⛔ never an automatic decision |

⚠️ THIS GATE DOES NOT BLOCK READING. Fetching, cloning and status pass untouched:
reading sends work nowhere. ⛔ A gate that gets in the way of the ordinary path is
switched off, and a switched-off gate protects less than none at all.

⛔ AND IT IS ONLY LAYER 1 — IT CAN BE WALKED AROUND. It reads the TEXT of a
command, and a pattern over command text never covers every way of invoking one:
an alias, a shell function, a variable holding the verb, an `eval`, an
argument-builder. ⭐ Layer 2 (hooks/pre-push.sh) runs inside the push itself with
the destination already resolved, and cannot be avoided. This layer's job is to
EXPLAIN before anything happens — which layer 2, firing mid-push, cannot do.

⬜ MENTE_PUSH_PATTERN / MENTE_REPO_ADMIN_PATTERN · which commands send work out
and which administer a repository are the installation's, because the tool
differs. Unset means the common ones.

Contract: PreToolUse payload on stdin · exit 0 with a JSON verdict.
"""
import json
import os
import re
import sys

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beat import beat                                         # noqa: E402

REG = os.environ.get("MENTE_ACCOUNTS") or os.path.join(MENTE, "accounts.tsv")
RETIRED = "archivado"

# ⚠️ ANCHORED to the start of the command or to a separator, never loose in the
# middle. ⛔ Measured: an unanchored pattern fired on `echo "remember: git push
# origin main"` — a warning about a command nobody will run is noise, and noise
# teaches people to ignore the warnings that matter.
PUSH = re.compile(os.environ.get("MENTE_PUSH_PATTERN") or
                  r"""(?:^|[;&|(]\s*|\bbash\s+-c\s+["'])\s*\S*git\s+"""
                  r"""(?:-C\s+\S+\s+)?push\b""")
# What creates, deletes or exposes a repository — irreversible or public-facing.
ADMIN = re.compile(os.environ.get("MENTE_REPO_ADMIN_PATTERN") or
                   r"\b\w+\s+repo\s+(create|delete|edit|archive|rename|transfer)\b")


def verdict(decision, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason}}))
    return 0


def registry():
    """repo → (role, remote, account). Empty when nothing is declared."""
    out = {}
    try:
        for line in open(REG, encoding="utf-8", errors="replace"):
            if line.startswith("#") or not line.strip():
                continue
            f = [c.strip() for c in line.rstrip("\n").split("\t")]
            if len(f) < 4 or f[0] == "repo":
                continue
            out[f[0].lower()] = (f[2].lower(), f[3], f[1])
    except OSError:
        pass
    return out


def named(cmd, known):
    """Which declared repository this command targets, if any.

    ⭐ Matched against what the registry DECLARES, never against a host's URL
    shape. ⛔ Parsing an address means knowing every forge's spelling, and the
    one not covered passes silently — the registry already holds the names.

    ⚠️ THE COMMON FORM OF A PUSH NAMES NO REPOSITORY AT ALL: `git push origin
    main` names a REMOTE. ⛔ Measured on the first probe run: matching only
    repository names denied the most ordinary push there is, and a gate that
    blocks the daily path is switched off within a week. So the remote column is
    matched too — that is precisely what it is for.
    """
    low = cmd.lower()
    for repo, (_, remote, _) in known.items():
        if repo in low:
            return repo
        # `owner/name` may appear as just `name` in an address or an alias
        tail = repo.split("/")[-1]
        if len(tail) > 3 and re.search(r"\b%s\b" % re.escape(tail), low):
            return repo
    # ⭐ Second pass, and it must be second: an explicit repository name beats a
    # remote alias, or `git push backup an-org/live` would resolve to the backup.
    for repo, (_, remote, _) in known.items():
        if remote and remote != "-" and re.search(
                r"(?:^|\s)%s(?:\s|$)" % re.escape(remote.lower()), low):
            return repo
    return None


def main():
    beat(MENTE, "gate-accounts")    # proof this gate still fires (bin/check-gates)
    try:
        payload = json.load(sys.stdin)
    except Exception:                                          # noqa: BLE001
        return 0
    if not isinstance(payload, dict):
        return 0
    ti = payload.get("tool_input")
    cmd = ti.get("command") if isinstance(ti, dict) else None
    if not isinstance(cmd, str) or not cmd:
        return 0

    # ⛔ Creating, deleting, renaming or exposing a repository is never automatic:
    # each is irreversible or public-facing, and neither is a machine's call.
    if ADMIN.search(cmd):
        return verdict("ask",
                       "🏗️  This creates, deletes, renames or exposes a "
                       "repository.\n"
                       "⛔ Irreversible or public-facing — it is a person's "
                       "decision, not an automatic one.")

    if not PUSH.search(cmd):
        return 0                    # reading sends work nowhere · not this gate's business

    known = registry()
    if not known:
        # ⬜ Nothing declared. ⚠️ Reported, never silent: a fresh installation
        # legitimately has an empty registry, and blocking its first push would
        # make the engine unusable before it is configured. But saying nothing
        # would let "unverified" read exactly like "verified".
        return verdict("allow",
                       "⬜ NOT MEASURED · no repository is declared in "
                       "%s.\n"
                       "This destination was NOT verified — run bin/check-accounts "
                       "and declare it."
                       % os.path.basename(REG))

    repo = named(cmd, known)

    if repo is None:
        # 🔴 FAIL CLOSED. An undeclared destination has no owner, no stated
        # reason to exist and no access guide — if the work leaves, nobody knows
        # where it went. ⭐ Denying costs nothing: the work stays local.
        return verdict("deny",
                       "🔴 This push targets a repository that is not in %s.\n\n"
                       "An undeclared destination has no owner, no reason to "
                       "exist and no access guide.\n"
                       "⛔ If the work leaves, nobody knows where it went — and "
                       "the push SUCCEEDS.\n\n"
                       "The way out:\n"
                       "  1. add its row to %s — with its `por_que_existe`\n"
                       "  2. bin/check-accounts\n"
                       "  3. push again\n\n"
                       "⚠️ Your work is still local. Nothing was lost."
                       % (os.path.basename(REG), os.path.basename(REG)))

    role, remote, account = known[repo]

    # ⭐ CHECKED BEFORE "is it registered" — and that order IS the rule. A
    # retired repository IS registered: it stays declared on purpose, because one
    # that vanishes from the table becomes invisible again and the reason it was
    # retired disappears with it. ⛔ A gate asking "registered?" first answers
    # YES and lets the push through. Measured: two layers both authorised a push
    # to a repository retired that same morning.
    if role == RETIRED:
        return verdict("deny",
                       "🔴 `%s` is RETIRED — it receives no work.\n\n"
                       "A retired repository is kept for reading, never for "
                       "writing. Pushing there leaves\n"
                       "the work somewhere the system already declared dead, and "
                       "nobody will look for it.\n\n"
                       "⚠️ Your work is still local. Push to the repository that "
                       "succeeded this one." % repo)

    # ⚠️ ACC-MUL-001 · a warning, never a block. Pushing to one remote at a time
    # is legitimate; ⛔ what is not legitimate is not KNOWING that the others fall
    # behind — the divergence is silent, and silence is what makes it last.
    others = sorted({r for k, (_, r, a) in known.items()
                     if a == account and k != repo and r and r != "-"}
                    - {remote})
    if others:
        return verdict("allow",
                       "⚠️  This clone declares more than one remote and you are "
                       "pushing to `%s`.\n"
                       "   Left behind: %s\n"
                       "   ⛔ Measured: two remotes diverged for weeks and "
                       "nothing reported it."
                       % (remote, ", ".join(others)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:                                     # noqa: BLE001
        # ⚠️ Fails OPEN, like gate-handoff and unlike gate-secrets. ⭐ This is
        # LAYER 1: layer 2 runs inside the push and cannot be walked around, so a
        # crash here loses an explanation, not the protection.
        print("⚠️  gate-accounts could not complete its check (%s: %s) — "
              "layer 2 (hooks/pre-push.sh) still applies."
              % (type(e).__name__, e), file=sys.stderr)
        sys.exit(0)
