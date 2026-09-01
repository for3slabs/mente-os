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
case("① 🔴 cierra con un sub-bloque ABIERTO", r.returncode == 2,
     "exit=%d" % r.returncode)

# ⭐ a status word nobody anticipated must count as OPEN
body_new = CLOSING % {"id": bid, "state": "pendiente"}
r = run(path, body_new)
case("② 🔴 ⭐ una palabra de estado NUEVA cuenta como abierta",
     r.returncode == 2, "lista blanca invertida")

# ⛔ capitals must not evade the gate
body_caps = body_open.replace("status: closed", "status: CLOSED")
r = run(path, body_caps)
case("③ 🔴 ⛔ status en MAYÚSCULAS no evade", r.returncode == 2,
     "exit=%d" % r.returncode)

# ⬜ the declared irreversible pattern
r = run("work/x.sql", "DROP TABLE users;", env={"MENTE_IRREVERSIBLE_PATTERN": r"DROP\s+TABLE"})
case("④ 🔴 ⬜ el patrón irreversible DECLARADO", r.returncode == 2, "bloquea")

# ── what must NOT block · the dangerous side
body_closed = CLOSING % {"id": bid, "state": "closed"}
open(os.path.join(d, "BLOCK.md"), "w", encoding="utf-8").write(body_closed)
r = run(path, body_closed)
case("⑤ ⭐ un cierre CORRECTO pasa", r.returncode == 0, "exit=0")

r = run("work/x.sql", "DROP TABLE users;")
case("⑥ ⭐ sin patrón declarado · NO adivina", r.returncode == 0,
     "⬜ nada declarado, nada bloqueado")

r = run("work/x.sql", "DROP TABLE users;",
        env={"MENTE_IRREVERSIBLE_PATTERN": "[unclosed"})
case("⑦ ⛔ un patrón MALFORMADO no bloquea todo", r.returncode == 0,
     "exit=0")

r = run("docs/anything.md", "just text")
case("⑧ una edición cualquiera pasa", r.returncode == 0, "exit=0")

for label, raw in (("payload roto", "{not json"), ("array", "[]"),
                   ("null", "null"), ("sin file_path", '{"tool_input":{}}')):
    r = run("", raw=raw)
    if r.returncode != 0:
        case("⑨ 🔴 nunca bloquea con payload inválido · %s" % label, False,
             "exit=%d" % r.returncode)
        break
else:
    case("⑨ 🔴 nunca bloquea con 4 payloads inválidos", True, "exit=0 en los cuatro")

clean()
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("\n  leftovers: %s" % ("none" if not [n for n in os.listdir(BLOCKS)
                                            if n.startswith(MARK)] else "🔴 quedan"))
sys.exit(0 if good == len(results) else 1)
