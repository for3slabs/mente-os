#!/usr/bin/env python3
"""probe-pre-edit-standards — proves the injection hook names the right block.

⭐ The failure this guards against is not silence: it is the WRONG block
answering. ⛔ When that happens the editor receives standards that do not apply,
and the correct warning never arrives — which is worse than no warning.
"""
import os, sys, json, shutil, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT, MARK                 # noqa: E402

HOOK = os.path.join(ROOT, "hooks", "pre-edit-standards.py")
BLOCKS = os.path.join(ROOT, "work", "blocks", "active")
results = []

BLOCK = """# BLOCK · %(id)s

## A · Identity

id: %(id)s
type: code
status: active

## B · Scope

### ✅ IN
- `work/%(id)s-src/` — owned here, unlike `docs/%(id)s-foreign.md` which another block closed

### ⛔ OUT
- everything else

## D · Required standards

%(std)s

## F · Sub-blocks

%(sub)s
"""


def plant(std="- `rules/contract-block.md`", sub="- none", bid=MARK + "-owner"):
    d = os.path.join(BLOCKS, bid)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "BLOCK.md"), "w", encoding="utf-8").write(
        BLOCK % {"id": bid, "std": std, "sub": sub})
    return d


def clean():
    for n in os.listdir(BLOCKS) if os.path.isdir(BLOCKS) else []:
        if n.startswith(MARK):
            shutil.rmtree(os.path.join(BLOCKS, n), ignore_errors=True)


def run(path, payload=None):
    body = json.dumps({"tool_input": {"file_path": path}}) if payload is None else payload
    return subprocess.run([sys.executable, HOOK], cwd=ROOT, input=body,
                          capture_output=True, text=True)


def case(label, ok, detail=""):
    print("  %-52s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


print("═══ SONDA · pre-edit-standards ═══\n")
clean()

# ① the claimed file → the block answers, with its standards
plant()
r = run("work/%s-owner-src/a.py" % MARK)
case("① archivo reclamado · nombra el bloque y su §D",
     MARK + "-owner" in r.stderr and "contract-block" in r.stderr,
     r.stderr.strip().split("\n")[0][:40])

# ② ⭐ a path cited INSIDE the prose is not a claim
r = run("docs/%s-owner-foreign.md" % MARK)
case("② ⭐ citado en la PROSA · no lo reclama", not r.stderr.strip(),
     "silencio" if not r.stderr.strip() else "🔴 lo reclamó")

# ③ ⛔ segment match, never substring
r = run("work/%s-owner-src-other/x.py" % MARK)
case("③ ⛔ prefijo parcial del nombre · no casa", not r.stderr.strip(),
     "silencio")

# ④ an empty §D is a finding, not silence
clean(); plant(std="—")
r = run("work/%s-owner-src/a.py" % MARK)
case("④ §D vacía · lo dice en vez de callar", "BLK-STD-001" in r.stderr,
     r.stderr.strip().split("\n")[-1][:40])

# ⑤ an OPEN sub-block on the same file is surfaced
clean()
plant(sub="| 1 | migrate it | `%s-owner-src/a.py` | — | active |" % MARK)
r = run("work/%s-owner-src/a.py" % MARK)
case("⑤ sub-bloque ABIERTO sobre el archivo · avisa",
     "sub-block for this file" in r.stderr, "el patrón arreglo-sobre-arreglo")

# ⑥ 🔴 it must NEVER block, whatever arrives
clean()
for label, payload in (("payload roto", "{not json"),
                       ("un array, no un objeto", "[]"),
                       ("null", "null"),
                       ("sin file_path", '{"tool_input":{}}')):
    r = run("", payload=payload)
    if r.returncode != 0:
        case("⑥ nunca bloquea · %s" % label, False, "exit=%d" % r.returncode)
        break
else:
    case("⑥ 🔴 nunca bloquea · 4 payloads inválidos", True, "exit=0 en los cuatro")

# ⑦ ⭐ no block claims the file → silence, not a guess
r = run("work/nobody/x.py")
case("⑦ archivo de nadie · silencio", not r.stderr.strip(), "silencio")

clean()
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d de %d correctos" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("\n  restos: %s" % ("ninguno" if not [n for n in os.listdir(BLOCKS)
                                            if n.startswith(MARK)] else "🔴 quedan"))
sys.exit(0 if good == len(results) else 1)
