#!/usr/bin/env python3
"""probe-gate-handoff — proves the gate bounds a WRITER and stays out of a reader's way.

⭐ THE ASYMMETRY IS THE DESIGN, so it is measured from both sides. A gate that
lets an unbounded writer through has failed. ⛔ But a gate that blocks a cheap
read-only delegation has failed WORSE: it makes handing work off cost more than
doing it inline, which is the behaviour that collapsed a context in the first
place — and it does so while looking like it is protecting something.

⚠️ Runs against an ISOLATED COPY: the cases plant blocks and manifests, and a
real tree must not end up carrying a fixture that other validators would read.
"""
import json, os, shutil, subprocess, sys, tempfile
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT, MARK                 # noqa: E402
from fixtures import block_text                # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-handoff-")
TREE = os.path.join(WORK, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git"))
HOOK = os.path.join(TREE, "hooks", "gate-handoff.py")
BID = MARK + "-gh"
BDIR = os.path.join(TREE, "work", "blocks", BID)
HDIR = os.path.join(BDIR, "handoffs")

MANIFEST = """schema_version: v1
handoff_id: "2026-01-15-0900-audit"
block: "%s"
block_path: "work/blocks/%s"
role: "audit"
load:
  required:
    - BLOCK.md
  optional: []
task:
  objective: "audit the fixture"
  success_condition: "every file listed with its size"
  stop_condition: "after the listed files, or on any read error"
binding_checks:
  - block_path_exists
  - block_file_exists
  - block_id_matches
  - load_required_paths_exist
agent:
  capabilities:
    read: true
    write: false
write_back:
  artifact:
    path: "handoffs/return.md"
    mode: create-only
  artifact_schema:
    required:
      - objective
      - work
      - findings
      - open-questions
      - status
    status:
      - done
      - partial
      - blocked
      - aborted-binding-mismatch
      - failed
  also_append: []
""" % (BID, BID)


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def run(tool="Agent", env=None, **ti):
    return subprocess.run([sys.executable, HOOK], cwd=TREE,
                          input=json.dumps({"tool_name": tool, "tool_input": ti}),
                          capture_output=True, text=True,
                          env=dict(os.environ, **(env or {})))


def plant(text=MANIFEST, name="h.yml"):
    os.makedirs(HDIR, exist_ok=True)
    open(os.path.join(BDIR, "BLOCK.md"), "w", encoding="utf-8").write(
        block_text(BID))
    open(os.path.join(HDIR, name), "w", encoding="utf-8").write(text)


def clear():
    shutil.rmtree(BDIR, ignore_errors=True)


print("═══ SONDA · gate-handoff ═══\n")

# ① 🔴 THE DEFECT IT EXISTS FOR · a writer with nothing declaring its bounds
clear()
r = run(subagent_type="writer", description="refactor the module")
case("① 🔴 a writer with no scope → BLOCKS", r.returncode == 2, "exit=%d" % r.returncode)

# ② ⭐ and it says WHAT is missing and HOW to fix it. A block with no route out
# is one the reader disables rather than satisfies.
case("② ⭐ the block names the cause AND the 3 steps to fix it",
     "no declared scope" in r.stderr and "check-handoff" in r.stderr
     and "templates/handoff.yml.template" in r.stderr)

# ③ ⚠️ the two empty states are DIFFERENT · "none exists" sends you somewhere
# else than "one exists and does not bind"
case("③ ⚠️ it tells «none exists» from «one exists and does not bind»",
     "No handoff manifest exists" in r.stderr)

# ④ ⭐ a VALID manifest opens the gate
plant()
r = run(subagent_type="writer", description="audit the fixture")
case("④ ⭐ a valid, bound manifest → passes", r.returncode == 0,
     "exit=%d" % r.returncode)

# ⑤ ⚠️ and it warns the manifest may be for OTHER work — the gate cannot read
# intent, and a stale scope is a scope for a different task
case("⑤ ⚠️ it warns that a stale manifest is a different scope",
     "stale manifest" in r.stderr)

# ⑥ 🔴 PRESENCE IS NOT COMPLIANCE (HND-GAT-002) · the case that decides whether
# this gate is real. An unfilled template is a file that exists and answers
# nothing, and "a file is there" reads exactly like "the question was answered".
clear()
plant(open(os.path.join(TREE, "templates", "handoff.yml.template"),
           encoding="utf-8").read())
r = run(subagent_type="writer", description="anything")
case("⑥ 🔴 an UNFILLED template does NOT open the gate", r.returncode == 2,
     "exit=%d" % r.returncode)
case("⑦ ⭐ and it says so: presence is not compliance",
     "presence is not compliance" in r.stderr)

# ⑧ 🔴 a manifest bound to a block that does not exist must not open it either
clear()
plant(MANIFEST.replace('block_path: "work/blocks/%s"' % BID,
                       'block_path: "work/blocks/does-not-exist"'))
r = run(subagent_type="writer", description="anything")
case("⑧ 🔴 a manifest bound to a block that does not exist → BLOCKS",
     r.returncode == 2, "exit=%d" % r.returncode)

# ⑨ ⭐ ONE valid manifest is enough even beside a broken one — the gate looks for
# a scope that holds, not for the absence of bad paperwork
clear()
plant()
plant(MANIFEST.replace("schema_version: v1", "schema_version: v9"), "broken.yml")
r = run(subagent_type="writer", description="audit the fixture")
case("⑨ ⭐ a valid one beside a broken one → passes", r.returncode == 0,
     "exit=%d" % r.returncode)

# ⑩ ⬜ THE ESCAPE HATCH exists and ANNOUNCES itself (HND-GAT-003). ⛔ A gate with
# no way out is deleted; a silent bypass is a gate already gone.
clear()
r = run(subagent_type="writer", description="x", env={"MENTE_HANDOFF_BYPASS": "1"})
case("⑩ ⬜ the escape hatch lets it through", r.returncode == 0,
     "exit=%d" % r.returncode)
case("⑪ ⛔ and it SHOUTS what using it costs",
     "BYPASSED" in r.stderr and "no validator will catch it" in r.stderr)

# ⑫ · a call that is not a delegation is none of this gate's business
r = run(tool="Bash", command="ls")
case("⑫ · a call that is not a delegation is not its business",
     r.returncode == 0 and not r.stderr.strip())

# ⑬ ⬜ which tool launches a specialist is the INSTALLATION's — a host that
# names it differently must still be governed
clear()
r = run(tool="Delegate", subagent_type="writer", description="x",
        env={"MENTE_HANDOFF_TOOL": "Delegate"})
case("⑬ ⬜ the tool's name is declarable", r.returncode == 2,
     "exit=%d" % r.returncode)

# ⑭ ⛔ ROBUSTNESS · a hook that crashes protects nothing
bad = []
for p in ("not json", "[]", "null", '{"tool_input": "text"}', '{}',
          '{"tool_name": "Agent"}'):
    x = subprocess.run([sys.executable, HOOK], cwd=TREE, input=p,
                       capture_output=True, text=True)
    if "Traceback" in x.stderr:
        bad.append(p)
case("⑭ ⛔ 6 invalid payloads → no traceback", not bad, str(bad))

# ⑮ ⚠️ AND IT FAILS OPEN, unlike gate-secrets. The worst case here is an
# unbounded specialist — visible in its own output and reversible. A broken gate
# that blocked every delegation would push the work back inline, which is
# exactly what this contract exists to prevent.
broken = os.path.join(TREE, "hooks", "_beat.py")
keep = open(broken, encoding="utf-8").read()
open(broken, "w").write("def beat(*a):\n    raise RuntimeError('boom')\n")
r = run(subagent_type="writer", description="x")
case("⑮ ⚠️ if the gate crashes it fails OPEN and says so",
     r.returncode == 0 and "could not complete" in r.stderr,
     "exit=%d" % r.returncode)
open(broken, "w").write(keep)

# ── ⭐ THE LEVEL COMES FROM CAPABILITY (HND-GAT-004/005) ────────────────────
# 🔴 Found by attacking this gate: without these four cases, a READ-ONLY agent
# passed only when an unrelated manifest happened to exist, and was blocked when
# none did. ⛔ Its verdict depended on other people's paperwork rather than on
# what it could do — and blocking a cheap reader is the failure the contract
# names as worse than the one it prevents.
clear()
RO = {"MENTE_HANDOFF_READONLY": "reader,explore"}
r = run(subagent_type="reader", description="just look", env=RO)
case("⑰ ⭐ a DECLARED reader passes with no manifest", r.returncode == 0,
     "exit=%d" % r.returncode)
r = run(subagent_type="writer", description="x", env=RO)
case("⑱ 🔴 and declaring readers does not soften the writer", r.returncode == 2,
     "exit=%d" % r.returncode)
# ⭐ HND-GAT-005 · the safe reading of silence is the PERMISSION being absent
r = run(subagent_type="a-brand-new-type", description="x", env=RO)
case("⑲ ⭐ an UNDECLARED type is a writer (fails closed)",
     r.returncode == 2, "exit=%d" % r.returncode)
r = run(subagent_type="reader", description="x")
case("⑳ ⛔ with no declaration, not even «reader» is exempt", r.returncode == 2,
     "exit=%d" % r.returncode)

# ⑯ ⭐ it leaves its beat, so a dead gate becomes visible to check-gates
clear()
run(subagent_type="writer", description="x")
case("⑯ ⭐ leaves its beat for check-gates",
     os.path.exists(os.path.join(TREE, ".beats", "gate-handoff")))

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
