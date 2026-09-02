#!/usr/bin/env python3
"""probe-gate-critical — proves the gate blocks what it must, and NOTHING else.

⭐ For a gate, the false positive is the dangerous verdict. A gate that blocks
what it should not is removed within a week — ⛔ and then the cases it was right
about are unguarded too.

So the inverses outnumber the blocks here, deliberately.
"""
import os, sys, json, shutil, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT, MARK                 # noqa: E402

HOOK = os.path.join(ROOT, "hooks", "gate-critical.py")
BLOCKS = os.path.join(ROOT, "work", "blocks", "active")
results = []

CLOSING = """# BLOCK · %(id)s

## A · Identity

id: %(id)s
type: docs
intent: prove the gate lets a valid closing through
status: closed
lane: task
owner: x
created: 2026-01-10 · updated: 2026-01-15

## B · Scope

### ✅ IN
- `work/%(id)s-src/`

### ⛔ OUT
- ⛔ DO NOT touch `work/other-src/` · DERIVED: another block owns it

## C · Connections

- none

## D · Required standards

- `rules/contract-block.md`

## F · Sub-blocks

| # | task | piece | %(state)s |

## K · Closing

completed: the thing
not completed: nothing
acceptance: passed
evidence level: L3
sufficiency: A-E resume the work
"""


def plant(bid=MARK + "-g"):
    d = os.path.join(BLOCKS, bid)
    os.makedirs(d, exist_ok=True)
    return d


def clean():
    for n in list(os.listdir(BLOCKS)) if os.path.isdir(BLOCKS) else []:
        if n.startswith(MARK):
            shutil.rmtree(os.path.join(BLOCKS, n), ignore_errors=True)


def run(target, body="", env=None, raw=None):
    payload = raw if raw is not None else json.dumps(
        {"tool_input": {"file_path": target, "content": body}})
    return subprocess.run([sys.executable, HOOK], cwd=ROOT, input=payload,
                          capture_output=True, text=True,
                          env=dict(os.environ, **(env or {})))


def case(label, ok, detail=""):
    print("  %-54s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


print("═══ SONDA · gate-critical ═══\n")
clean()
bid = MARK + "-g"
d = plant()
path = os.path.join("work", "blocks", "active", bid, "BLOCK.md")

# ── what MUST block
body_open = CLOSING % {"id": bid, "state": "active"}
open(os.path.join(d, "BLOCK.md"), "w", encoding="utf-8").write(body_open)
r = run(path, body_open)
case("① 🔴 closing with an OPEN sub-block", r.returncode == 2,
     "exit=%d" % r.returncode)

# ⭐ a status word nobody anticipated must count as OPEN
body_new = CLOSING % {"id": bid, "state": "pendiente"}
r = run(path, body_new)
case("② 🔴 ⭐ a NEW state word counts as open",
     r.returncode == 2, "lista blanca invertida")

# ⛔ capitals must not evade the gate
body_caps = body_open.replace("status: closed", "status: CLOSED")
r = run(path, body_caps)
case("③ 🔴 ⛔ status in UPPERCASE does not evade", r.returncode == 2,
     "exit=%d" % r.returncode)

# ⬜ the declared irreversible pattern
r = run("work/x.sql", "DROP TABLE users;", env={"MENTE_IRREVERSIBLE_PATTERN": r"DROP\s+TABLE"})
case("④ 🔴 ⬜ the DECLARED irreversible pattern", r.returncode == 2, "bloquea")

# ── what must NOT block · the dangerous side
body_closed = CLOSING % {"id": bid, "state": "closed"}
open(os.path.join(d, "BLOCK.md"), "w", encoding="utf-8").write(body_closed)
# ⭐ BLK-CLS-007 · a correct close carries its machine-readable record. ⛔ A
# fixture missing it fails a rule this case was not testing, and the inverse
# then reports a false positive against the gate.
open(os.path.join(d, "close.json"), "w", encoding="utf-8").write(
    '{"block": "%s", "layer1_verdict": "MVP", "dimensions": '
    '{"architecture": "undeclared"}}' % bid)
r = run(path, body_closed)
case("⑤ ⭐ a CORRECT close passes", r.returncode == 0, "exit=0")

# 🔴 THE INVERSE, AND IT WAS SILENTLY BROKEN. The gate ran check-block with
# `--quiet` and then looked for the block's NAME in that run's output — which is
# empty by contract (CHK-QUI-001). ⛔ The condition could never be true, so every
# insufficient close went through.
# ⚠️ Found only by exercising the gates against a real installation: every probe
# here was green, because they measured the gate and not the PAIR.
_bad = body_closed.replace("type: docs", "type: invented")
open(os.path.join(d, "BLOCK.md"), "w", encoding="utf-8").write(_bad)
r = run(path, _bad)
case("⑤b 🔴 an INSUFFICIENT close is refused", r.returncode == 2,
     "exit=%d" % r.returncode)
case("⑤c ⭐ and the refusal names the block", bid in r.stderr)
open(os.path.join(d, "BLOCK.md"), "w", encoding="utf-8").write(body_closed)

r = run("work/x.sql", "DROP TABLE users;")
case("⑥ ⭐ with no declared pattern · it does NOT guess", r.returncode == 0,
     "⬜ nada declarado, nada bloqueado")

r = run("work/x.sql", "DROP TABLE users;",
        env={"MENTE_IRREVERSIBLE_PATTERN": "[unclosed"})
case("⑦ ⛔ a MALFORMED pattern does not block everything", r.returncode == 0,
     "exit=0")

r = run("docs/anything.md", "just text")
case("⑧ an ordinary edit passes", r.returncode == 0, "exit=0")

for label, raw in (("payload roto", "{not json"), ("array", "[]"),
                   ("null", "null"), ("sin file_path", '{"tool_input":{}}')):
    r = run("", raw=raw)
    if r.returncode != 0:
        case("⑨ 🔴 never blocks on an invalid payload · %s" % label, False,
             "exit=%d" % r.returncode)
        break
else:
    case("⑨ 🔴 never blocks on 4 invalid payloads", True, "exit=0 en los cuatro")

clean()
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("\n  leftovers: %s" % ("none" if not [n for n in os.listdir(BLOCKS)
                                            if n.startswith(MARK)] else "🔴 quedan"))
sys.exit(0 if good == len(results) else 1)
