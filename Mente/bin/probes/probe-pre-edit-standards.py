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


def claimed(r):
    """Did a block CLAIM the file? — ⭐ not merely: did the hook speak.

    ⛔ Since BLK-SCP-005 the hook also reports an edit outside every open scope,
    so "stderr is empty" stopped meaning "nobody claimed it". The claim is the
    📦 line; the scope report is the ⚠️ line, and they are different questions.
    """
    return "📦" in r.stderr


def case(label, ok, detail=""):
    print("  %-52s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


print("═══ SONDA · pre-edit-standards ═══\n")
clean()

# ① the claimed file → the block answers, with its standards
plant()
r = run("work/%s-owner-src/a.py" % MARK)
case("① a claimed file · names the block and its §D",
     MARK + "-owner" in r.stderr and "contract-block" in r.stderr,
     r.stderr.strip().split("\n")[0][:40])

# ② ⭐ a path cited INSIDE the prose is not a claim
r = run("docs/%s-owner-foreign.md" % MARK)
case("② ⭐ cited in PROSE · does not claim it", not claimed(r),
     "not claimed" if not claimed(r) else "🔴 it claimed it")

# ③ ⛔ segment match, never substring
r = run("work/%s-owner-src-other/x.py" % MARK)
case("③ ⛔ a partial name prefix · does not match", not claimed(r),
     "not claimed")

# ④ an empty §D is a finding, not silence
clean(); plant(std="—")
r = run("work/%s-owner-src/a.py" % MARK)
case("④ an empty §D · it says so instead of staying quiet", "BLK-STD-001" in r.stderr,
     r.stderr.strip().split("\n")[-1][:40])

# ⑤ an OPEN sub-block on the same file is surfaced
clean()
plant(sub="| 1 | migrate it | `%s-owner-src/a.py` | — | active |" % MARK)
r = run("work/%s-owner-src/a.py" % MARK)
case("⑤ an OPEN sub-block over the file · it warns",
     "sub-block for this file" in r.stderr, "the fix-on-fix pattern")

# ⑥ 🔴 it must NEVER block, whatever arrives
clean()
for label, payload in (("payload roto", "{not json"),
                       ("un array, no un objeto", "[]"),
                       ("null", "null"),
                       ("sin file_path", '{"tool_input":{}}')):
    r = run("", payload=payload)
    if r.returncode != 0:
        case("⑥ never blocks · %s" % label, False, "exit=%d" % r.returncode)
        break
else:
    case("⑥ 🔴 never blocks · 4 invalid payloads", True, "exit=0 in all four")

# ⑦ ⭐ no block claims the file → it does not GUESS one
r = run("work/nobody/x.py")
case("⑦ a file nobody owns · names no block", not claimed(r), "no guess")

# ⑧ ⭐ BLK-SCP-005 · with a block OPEN, an edit outside every scope is REPORTED
# ⛔ This is the case that was missing: the boundary was written and nothing
# watched it, so it held exactly as long as attention did.
plant()
r = run("docs/%s-owner-foreign.md" % MARK)
case("⑧ ⭐ outside every open scope · it reports it",
     "BLK-SCP-004" in r.stderr and r.returncode == 0,
     "reports, exit=0 — it never blocks")

# ⑨ ⛔ with NO block open there is no scope to be outside of → no noise
clean()
r = run("docs/%s-owner-foreign.md" % MARK)
case("⑨ ⛔ no block open · no scope report", not r.stderr.strip(),
     "silence — nothing to be outside of")

clean()
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("\n  leftovers: %s" % ("none" if not [n for n in os.listdir(BLOCKS)
                                            if n.startswith(MARK)] else "🔴 quedan"))
sys.exit(0 if good == len(results) else 1)
