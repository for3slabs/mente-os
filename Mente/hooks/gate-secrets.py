#!/usr/bin/env python3
"""gate-secrets — the door to secrets/, and the one check that must happen BEFORE a write.

Two jobs, and they are not the same job:

  ① THE DOOR · reading secrets/ is governed, writing there always asks.
  ② THE LEAK · a secret VALUE being written into any file, anywhere, is refused.

⭐ WHY ② IS THE ONE THAT MATTERS MOST. A validator finds a secret AFTER it is
written — and by then the value is already in the session transcript, which
nobody edits. ⛔ The rule this system carries is that a leaked secret is ROTATED,
never deleted, so detecting it late does not avoid the rotation: it only
discovers it. The single moment where a leak can still be prevented is the
instant before the write.

⛔ AND ② IS WHY THIS GATE BLOCKS RATHER THAN ASKS. Everywhere else in this engine
a gate that obstructs more than it protects degrades to a warning. This is the
exception the rule allows for: the damage is irreversible, and "ask" on a leak is
a prompt that gets approved by reflex at the end of a long session.

── THE THREE ANSWERS FOR ① ─────────────────────────────────────────────────────
| situation                    | answer | why                                      |
|------------------------------|--------|------------------------------------------|
| read, with live permission   | allow  | permission was granted when context loaded |
| read, no permission          | ask    | the person decides, in the moment          |
| write / create / delete      | ask    | ⛔ changing a credential is never automatic |

⚠️ Governed access is NOT a restriction lifted for convenience. Writing still
asks every time, and every operation is recorded — which a flat block never did,
because an access that cannot happen also cannot be logged.

Contract: PreToolUse payload on stdin · exit 0 with a JSON verdict, or exit 2 to
BLOCK a leak.
"""
import json
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
import plat                                          # noqa: E402
import os
import re
import subprocess
import sys

MENTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _beat import beat                                         # noqa: E402

LEASE = os.path.join(MENTE, "bin", "secrets-lease")
# ⚠️ Compared on the RESOLVED path, never on the text. A `../` or a symlink walks
# straight past a string comparison, and the folder this guards is the one where
# that mistake is unrecoverable.
SECRETS = os.path.realpath(
    os.environ.get("MENTE_SECRETS_DIR") or os.path.join(MENTE, "secrets"))

WRITE_TOOLS = ("Write", "Edit", "NotebookEdit", "MultiEdit")

# ── ② WHAT A SECRET VALUE LOOKS LIKE ────────────────────────────────────────
# ⭐ Shape, never a list of known credentials: a list of secrets kept in the
# engine would BE a secrets file, and it would only ever catch yesterday's.
#
# ⛔ THE FALSE POSITIVE IS THE FAILURE MODE HERE. This gate BLOCKS, so a pattern
# that fires on a placeholder or an example stops real work — and a gate that
# stops real work is removed within a week, taking the real protection with it.
# Hence: an assignment to a secret-shaped NAME, with a value long enough to be
# real, that is not a reference and not obviously a placeholder.
# ⭐ The NAME half. `pass` and `pwd` are here because a shortened name is the
# one people actually type, and a pattern that only knows the formal spelling
# catches the careful writer and misses the hurried one.
NAME = (r"pass(?:word|wd)?|pwd|secret|token|api[_-]?key|access[_-]?key"
        r"|private[_-]?key|client[_-]?secret|auth[_-]?token"
        r"|credential|passphrase")
# ⚠️ A HASH is not a credential — it is the safe thing to store, and blocking it
# would punish exactly the practice this rule wants. Excluded by name.
NOT_A_SECRET_NAME = re.compile(r"(?i)(?:hash|digest|salt|checksum|fingerprint)$")

# ⚠️ THE LEFT EDGE IS NOT `\b`. A name inside JSON or a quoted key —
# `{"password":…}`, `"pass":…` — sits against a quote, and `\b` there behaves
# differently than against whitespace. ⛔ Measured: both forms walked straight
# through, and JSON is how configuration is most often pasted. An explicit
# "start, or any non-name character" edge covers every wrapper.
ASSIGN = re.compile(
    r"""(?ix)
    (?:^|[^A-Za-z0-9_])
    (?P<name>[A-Za-z0-9_]*(?:%s))
    ["']?                                          # a JSON key closes its quote
    \s*[:=]{1,2}\s*
    (?:
        (?P<q>['"])(?P<qval>[^'"\n]{8,})(?P=q)     # quoted
      | (?P<val>[^\s'"#,;()\]}]{8,})\b(?![\w.]*\()  # ⭐ or bare: KEY=value,
    )                                              #   how a .env file is written
    """ % NAME)
# ⛔ THE BARE BRANCH MUST REACH THE END OF THE TOKEN BEFORE IT JUDGES. Written
# without the `\b`, `{8,}` stopped at exactly eight characters — so
# `token = get_token("x")` matched `get_toke`, the lookahead never saw the
# parenthesis, and a function CALL was reported as a leaked credential.
# ⚠️ A gate that blocks ordinary code is removed within a week, and takes the
# real protection with it. The `\b` is what makes the exclusion able to fire.
FLAG = re.compile(
    r"""(?ix)
    --(?:password|secret|token|api[-_]?key)[=\s]+
    (?P<val>[A-Za-z0-9!@\#$%^&*_+./-]{8,})
    """)

# ⚠️ A CONNECTION STRING carries the credential in its authority section, where
# no name appears beside it — `scheme://user:VALUE@host`. ⛔ This is the leak
# shape that a name-based pattern cannot see at all, and it is the one that
# reaches a document most often, because people paste the whole URL.
URL_CRED = re.compile(
    r"\b[a-z][a-z0-9+.-]*://[^\s:/@]+:(?P<val>[^\s:/@]{6,})@")
# ⭐ Credential formats that are unmistakable on their own, with no name beside
# them: these carry their own prefix by design, so a match is never a guess.
TOKEN_SHAPE = re.compile(
    r"\b(?:sk|pk|rk)-[A-Za-z0-9_-]{16,}"          # provider-issued api keys
    r"|\bgh[pousr]_[A-Za-z0-9]{20,}"              # forge tokens
    r"|\bxox[baprs]-[A-Za-z0-9-]{10,}"            # chat platform tokens
    r"|\bAKIA[0-9A-Z]{12,}"                       # cloud access key id
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----")       # a key file pasted inline

# ⛔ What is NOT a secret, and each entry earns its place by being a thing people
# legitimately write. A value that REFERENCES a secret is the correct behaviour
# this whole rule asks for — blocking it would punish compliance.
REFERENCE = re.compile(
    r"""(?ix)
    ^\s*(?:
        \$\{?[A-Z_][A-Z0-9_]*\}?            # $VAR  ${VAR}
      | (?:os\.)?(?:environ|getenv|env)\b   # env lookups
      | process\.env\b
      | \{\{[^}]+\}\}                       # {{placeholder}}
      | <[^>]+>                             # <your-token-here>
      | (?:x{3,}|\*{3,}|\.{3,})             # xxxx  ****  ....
      | (?:your|my|the)[-_ ]                # your-token-here
      | (?:example|sample|placeholder|redacted|changeme|dummy|fake|test)
      | (?:none|null|nil|true|false|undefined)\s*$
      | \$\(                                # $(vault read …) — a lookup, not a value
      | `                                    # `backtick lookup`
      | (?:arn|urn|spiffe|did):              # a resource identifier is public
      | (?:see|in|at|from)\s                 # "see secrets/README.md" — a pointer
      | \S+\.(?:md|txt|json|yml|yaml|env)\b  # a filename is a pointer, not a value
      | https?://                            # ⚠️ a plain URL, no credential in it
    )""")
# ⚠️ A value with no variety is a placeholder, not a credential. `password:
# "aaaaaaaa"` and `token: "12345678"` are what people type in documentation, and
# blocking those is how this gate loses its welcome.
def looks_random(v):
    return len(set(v)) >= 5


def verdict(decision, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason}}))
    return 0


def leaks(text):
    """Every secret-shaped value in this text. Empty when the text is clean."""
    if not isinstance(text, str) or not text:
        return []
    found = []
    for rx in (ASSIGN, FLAG, URL_CRED):
        for m in rx.finditer(text):
            g = m.groupdict()
            v = g.get("qval") or g.get("val")
            if not v:
                continue
            # ⚠️ A hash, digest or salt is the SAFE thing to store — blocking it
            # would punish the practice this rule asks for.
            name = g.get("name") or ""
            if name and NOT_A_SECRET_NAME.search(name):
                continue
            if REFERENCE.match(v) or not looks_random(v):
                continue
            found.append(m.group(0)[:40])
    for m in TOKEN_SHAPE.finditer(text):
        found.append(m.group(0)[:12] + "…")
    return found


def targets_secrets(ti):
    """The resolved path if this call touches secrets/, else None."""
    p = ti.get("file_path") or ti.get("notebook_path")
    if isinstance(p, str) and p:
        real = os.path.realpath(p)
        if real == SECRETS or real.startswith(SECRETS + os.sep):
            return real
    cmd = ti.get("command")
    # ⚠️ Deliberately coarse. A shell command can reach the folder in ways no
    # pattern covers — `$(...)`, a variable, an alias. ⛔ This does not pretend
    # to seal that path; it makes the NORMAL path recorded rather than silent.
    if isinstance(cmd, str) and re.search(r"(^|[\s/'\"])secrets/", cmd):
        return "(shell command)"
    return None


def note(op, target, reason):
    try:
        # 🔴 plat.script: a bare path never started on Windows, so NO access
        # was ever logged there — the log file was not even created, and the
        # permission-hardening inside secrets-lease never ran either.
        subprocess.run(plat.script(LEASE, "log", op, target, reason),
                       capture_output=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        pass            # ⛔ the log never blocks the work


def permitted():
    try:
        # 🔴 Same defect, and here it failed CLOSED: a live session permission
        # never registered on Windows, so every read of secrets/ asked again.
        return subprocess.run(plat.script(LEASE, "check"), capture_output=True,
                              timeout=10).returncode == 0
    except (OSError, subprocess.SubprocessError):
        # 🔴 FAIL CLOSED. If the grantor cannot answer, permission is NOT given.
        # ⛔ A grant issued because a check broke is precisely the failure this
        # gate exists to prevent.
        return False


def main():
    beat(MENTE, "gate-secrets")     # proof this gate still fires (bin/check-gates)
    try:
        payload = json.load(sys.stdin)
    except Exception:                                          # noqa: BLE001
        return 0
    if not isinstance(payload, dict):
        return 0
    ti = payload.get("tool_input")
    if not isinstance(ti, dict):
        return 0
    tool = payload.get("tool_name") or ""

    # ── ② THE LEAK · checked FIRST, and on every write, wherever it lands ────
    # ⭐ Before the door, because a secret written into an ordinary file never
    # touches secrets/ at all — and that is the leak that actually happens.
    if tool in WRITE_TOOLS:
        body = ""
        for k in ("content", "new_string", "new_source"):
            v = ti.get(k)
            if isinstance(v, str):
                body += "\n" + v
        hits = leaks(body)
        if hits:
            where = ti.get("file_path") or ti.get("notebook_path") or "this file"
            print("🔴 BLOCKED · a secret VALUE is about to be written into %s\n"
                  "   %s\n"
                  "   Reference it — an environment variable, or a pointer to "
                  "where it lives.\n"
                  "   ⛔ If this value is real it is now ROTATED, not deleted: "
                  "removing it later\n"
                  "   leaves it in every transcript that recorded it.\n"
                  "   Bypass: none here. Change the value to a reference."
                  % (os.path.basename(str(where)), "\n   ".join(hits[:3])),
                  file=sys.stderr)
            return 2

    # ── ① THE DOOR · only from here on does secrets/ itself matter ──────────
    path = targets_secrets(ti)
    if not path:
        return 0

    if tool in WRITE_TOOLS:
        note("write?", path, "%s — awaiting approval" % tool)
        return verdict("ask",
                       "✍️  %s on `%s` in secrets/.\n"
                       "Creating or changing a credential is never automatic, "
                       "not even with live permission.\n"
                       "It is recorded in secrets/.access-log.md either way."
                       % (tool, os.path.basename(path)))

    if permitted():
        note("read", path, "live permission (granted at context load)")
        return verdict("allow",
                       "🔑 secrets permission LIVE — reading `%s`, recorded in "
                       "secrets/.access-log.md" % os.path.basename(path))

    note("read?", path, "no permission — awaiting approval")
    return verdict("ask",
                   "🔒 no live permission to read `%s`.\n"
                   "Permission is issued when the context loads "
                   "(bin/secrets-lease)." % os.path.basename(path))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:                                     # noqa: BLE001
        # 🔴 CHK-CAU-002, and this gate answers it the OPPOSITE way to every
        # other one. gate-critical fails OPEN on a crash — a guard that dies
        # must not take the work with it, because its worst case is a bad
        # migration someone can still revert.
        #
        # ⛔ Here the worst case is a credential written to disk, and that is
        # not revertible: the value is in the transcript from the moment it is
        # produced, which is why the rule says ROTATE, never delete. A leak
        # check that lets a write through because it crashed has failed at the
        # only job it had.
        # ⚠️ So this fails CLOSED, and says exactly why, because a block with no
        # reason is one the reader disables rather than understands.
        print("🔴 BLOCKED · gate-secrets could not complete its check "
              "(%s: %s).\n"
              "   Refusing rather than allowing: an unchecked write may carry a "
              "credential,\n"
              "   and a leaked value is ROTATED, never deleted — there is no "
              "undo to fall back on.\n"
              "   Fix the gate, or move the write outside this session."
              % (type(e).__name__, e), file=sys.stderr)
        sys.exit(2)
