#!/usr/bin/env python3
"""probe-gate-secrets — proves the door governs, and the leak check refuses.

⭐ THIS GATE BLOCKS, so it is measured from BOTH sides and the false-positive
side is measured harder. A leak that gets through is one rotation; a gate that
fires on a placeholder is removed within a week, and then nothing catches
anything. ⛔ The cases below therefore include every shape a person legitimately
writes: an environment reference, a template placeholder, a documentation
example, a value too uniform to be real.

⛔ ON THE VALUES IN THIS FILE. Every credential below is INVENTED — a keyboard
walk, a well-known documentation example, or a shape with the right prefix and
nothing behind it. ⚠️ None grants access to anything, and none may ever be
replaced with a real one: a probe that tests detection using a live credential
has leaked that credential into the repository in order to prove it could have
caught it. ⭐ The gate itself flags this file when scanning the tree, which is
correct behaviour — the same is true of three probes that predate it.

⚠️ Runs against an ISOLATED COPY. The subject writes an access log and a lease
file, and planting those in the working tree would leave a real installation
claiming accesses that never happened.
"""
import json, os, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-secrets-")
TREE = os.path.join(WORK, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git"))
HOOK = os.path.join(TREE, "hooks", "gate-secrets.py")
LEASE = os.path.join(TREE, "bin", "secrets-lease")
LOG = os.path.join(TREE, "secrets", ".access-log.md")


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def run(tool="Write", **ti):
    return subprocess.run([sys.executable, HOOK], cwd=TREE,
                          input=json.dumps({"tool_name": tool, "tool_input": ti}),
                          capture_output=True, text=True)


def decision(r):
    try:
        return json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"]
    except Exception:                                          # noqa: BLE001
        return None


def lease(cmd):
    return subprocess.run([sys.executable, LEASE, cmd], cwd=TREE,
                          capture_output=True, text=True)


print("═══ PROBE · gate-secrets + secrets-lease ═══\n")

# ── ② THE LEAK CHECK · what MUST be refused ─────────────────────────────────
LEAKS = [
    ('password = "Tr0ub4dor&3x"',            "a real password assigned"),
    ("api_key: 'a8Kd93jXm2Qp5vNw'",          "a named api key"),
    ('client_secret="xY9$mQ2#pL8w"',         "a client secret"),
    ("psql --password=Hunter2Real9x",        "a secret in a flag"),
    ("key = 'sk-abcd1234efgh5678ijkl'",      "a provider format"),
    ("token: 'ghp_A1b2C3d4E5f6G7h8I9j0K1'",  "a forge token"),
    ("-----BEGIN RSA PRIVATE KEY-----",      "a private key pasted inline"),
    # ⭐ Every one below walked straight through the first version, and each was
    # found by attacking the gate with a shape the probe had not been written
    # for. ⛔ A defect found once and not written down is a defect that returns.
    ("DB_PASSWORD=Xk9$mQ2pLw8n",             "unquoted, as in a .env"),
    ("export TOKEN=ghp_Zx9Kq2Lm8Pw4Rt6yAb",  "a shell export"),
    ('"pass": "Zx9Kq2Lm8Pw4Rt"',             "the shortened name people type"),
    ('{"password":"Zx9Kq2Lm8Pw4"}',          "inside JSON — how a config gets pasted"),
    ('PASSWORD = "Zx9Kq2Lm8Pw4"',            "in uppercase"),
    ("AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI",  "a cloud key"),
    ("postgres://user:Zx9Kq2Lm@host/db",     "⭐ a connection string — with no name beside it"),
]
for body, why in LEAKS:
    r = run(file_path="notes.md", content=body)
    case("🔴 refuses · %s" % why, r.returncode == 2,
         "exit=%d" % r.returncode)

# ── ⛔ AND WHAT MUST NOT BE REFUSED · the side that keeps the gate alive ────
CLEAN = [
    ('password = os.environ["DB_PASSWORD"]',  "an environment read"),
    ('token: "${GITHUB_TOKEN}"',              "a shell variable"),
    ('api_key: "{{api_key}}"',                "a template placeholder"),
    ('password: "<your-password-here>"',      "a documentation example"),
    ('secret = "xxxxxxxxxx"',                 "a redacted value"),
    ('password: "changeme"',                  "an obvious default"),
    ('token = "aaaaaaaaaaaa"',                "a value with no variety"),
    ('password: null',                        "an empty value"),
    ('const apiKey = process.env.API_KEY',    "a JS environment read"),
    ("# never write a password: value here",  "the doctrine itself, in prose"),
    # ⛔ Y estos bloqueaban trabajo correcto — el fallo que borra la puerta.
    ('password: "$(vault read key)"',         "a lookup through a manager"),
    ('secret: "arn:aws:iam::12345:role/x"',   "a public resource identifier"),
    ('api_key: "see secrets/README.md"',      "a pointer in prose · what the rule ASKS FOR"),
    ('password_hash = "$2b$12$abcdefghij"',   "⭐ a HASH — the safe thing to store"),
    ('token = get_token("service-account")',  "a function call"),
    ('secret = get_secret(name)',             "another call"),
    ('url = "https://docs.example.com/api"',  "a URL with no credential"),
]
for body, why in CLEAN:
    r = run(file_path="notes.md", content=body)
    case("⛔ does NOT refuse · %s" % why, r.returncode == 0,
         "exit=%d" % r.returncode)

# ⭐ the refusal must name WHAT it saw · a block with no cause cannot be acted on
r = run(file_path="notes.md", content='password = "Tr0ub4dor&3x"')
case("⭐ the refusal names the value AND orders a ROTATION",
     "Tr0ub4dor" in r.stderr and "ROTATED" in r.stderr)

# ⚠️ an Edit carries new_string, not content — a check that only reads one field
# is blind to the other, and both write to disk
r = run(tool="Edit", file_path="a.py", new_string='token = "Zx9Kq2Lm8Pw4Rt6y"')
case("⚠️ an Edit (new_string) is checked like a Write",
     r.returncode == 2, "exit=%d" % r.returncode)

# ── ① THE DOOR ──────────────────────────────────────────────────────────────
lease("close")
r = run(tool="Read", file_path=os.path.join(TREE, "secrets", "server.md"))
case("🔒 reading with no permission → ask", decision(r) == "ask", str(decision(r)))

lease("open")
r = run(tool="Read", file_path=os.path.join(TREE, "secrets", "server.md"))
case("🔑 reading WITH live permission → allow", decision(r) == "allow", str(decision(r)))

# ⛔ the whole point: permission opens READING, never writing
r = run(tool="Write", file_path=os.path.join(TREE, "secrets", "new.md"),
        content="where the key lives")
case("⛔ writing WITH live permission → ask all the same", decision(r) == "ask",
     str(decision(r)))

# ⚠️ a path that walks out and back in must not evade the door
r = run(tool="Read", file_path=os.path.join(TREE, "rules", "..", "secrets", "x.md"))
case("⚠️ a `..` does not walk around the gate (resolved path)", decision(r) == "allow",
     str(decision(r)))

# nothing to do with secrets/ → the gate is not involved at all
r = run(tool="Read", file_path=os.path.join(TREE, "rules", "README.md"))
case("· a file elsewhere is not its business", r.returncode == 0 and not r.stdout.strip())

# ── THE LOG ─────────────────────────────────────────────────────────────────
recorded = os.path.exists(LOG) and open(LOG, encoding="utf-8").read()
case("📓 the log recorded the accesses",
     bool(recorded) and "READ" in recorded, "%d línea(s)" % (
         recorded.count("\n| 2") + recorded.count("\n| 20") if recorded else 0))
case("⛔ the log contains NO value",
     bool(recorded) and "Tr0ub4dor" not in recorded and "ghp_" not in recorded)
case("🔐 the log is born 600, not 644",
     os.path.exists(LOG) and oct(os.stat(LOG).st_mode)[-3:] == "600",
     oct(os.stat(LOG).st_mode)[-3:] if os.path.exists(LOG) else "—")

# ── E-39 · THE GRANTOR HARDENS THE FOLDER IT GUARDS ────────────────────────
# ⭐ Git cannot carry a 700, so every clone arrives world-readable. ⛔ A report
# is not a repair: check-config names it, and the folder stays open until
# somebody reads the finding. The grantor closes it before issuing, because a
# permission granted over a world-readable folder grants nothing.
import stat as _stat
SDIR = os.path.join(TREE, "secrets")


def mode_of(p):
    return oct(_stat.S_IMODE(os.stat(p).st_mode))[-3:]


os.chmod(SDIR, 0o755)
lease("open")
case("🔐 E-39 · a 755 is closed to 700 when granting", mode_of(SDIR) == "700",
     mode_of(SDIR))

# ⚠️ AND IT ONLY TIGHTENS. An owner who hardened further made a decision this
# grantor knows nothing about — resetting it to 700 would silently undo it.
os.chmod(SDIR, 0o500)
lease("open")
case("⚠️ a 500 (stricter) is NOT loosened to 700", mode_of(SDIR) == "500",
     mode_of(SDIR))
os.chmod(SDIR, 0o700)

# ⛔ a real file left readable is closed too — that is where a credential lives
kf = os.path.join(SDIR, "key-note.md")
open(kf, "w").write("where the key lives")
os.chmod(kf, 0o644)
lease("open")
case("🔐 a 644 file inside is closed to 600", mode_of(kf) == "600",
     mode_of(kf))
os.remove(kf)

# ⛔ but README.md is left alone: it ships in git, which cannot carry a 600, so
# tightening it is undone by the next pull — and a fix that does not survive is
# noise. check-config exempts it for the same reason.
case("⛔ README.md is left alone (git cannot carry 600)",
     mode_of(os.path.join(SDIR, "README.md")) != "600")

# ── FAIL CLOSED · the case that decides whether this is real ────────────────
# 🔴 If the grantor cannot answer, permission must NOT be granted. A grant issued
# because a check broke is the exact failure the gate exists to prevent.
os.chmod(LEASE, 0o000)
r = run(tool="Read", file_path=os.path.join(TREE, "secrets", "server.md"))
case("🔴 a broken grantor → ask, NEVER allow", decision(r) == "ask",
     str(decision(r)))
os.chmod(LEASE, 0o755)

# ── ROBUSTNESS · a hook that crashes protects nothing ──────────────────────
bad = []
for payload in ("not json", "[]", "null", '{"tool_input": "text"}', '{}'):
    p = subprocess.run([sys.executable, HOOK], cwd=TREE, input=payload,
                       capture_output=True, text=True)
    if p.returncode != 0 or "Traceback" in p.stderr:
        bad.append(payload)
case("⛔ 5 invalid payloads → exit 0, no traceback", not bad, str(bad))

# ⭐ it leaves its beat, so check-gates can tell it is alive
case("💓 leaves its beat for check-gates",
     os.path.exists(os.path.join(TREE, ".beats", "gate-secrets")))

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
# ⚠️ The harness reads this line. A probe that writes an access log and a lease
# and does not account for them would leave a real installation claiming
# accesses that never happened — so the cleanup is REPORTED, not assumed.
left = [p for p in (WORK, os.path.join(ROOT, ".secrets-lease.json"),
                    os.path.join(ROOT, "secrets", ".access-log.md"))
        if os.path.exists(p)]
print("  leftovers: %s" % ("none" if not left else
                        "🔴 " + ", ".join(os.path.basename(p) for p in left)))
sys.exit(0 if good == len(results) and not left else 1)
