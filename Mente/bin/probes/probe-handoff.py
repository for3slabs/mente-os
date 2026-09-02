#!/usr/bin/env python3
"""probe-handoff — does check-handoff detect what contract-handoff.md claims?

⭐ It also verifies the EXIT CODE: 2 means fix the manifest, 3 means the
manifest describes a world that does not exist. They send you to different
places, so a probe that only checks the finding proves half of it.
"""
import os, sys, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK
from fixtures import block, BLOCKS

p = Probe("check-handoff", "HND")
BID = MARK + "-hb"

GOOD = """schema_version: v1
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

# ⭐ A return artifact names the handoff it answers. Without it, an artifact
# from another delegation is indistinguishable from this one's.
RETURN = """# return · 2026-01-15-0900-audit

## objective

audit the fixture

## work

listed every file

## findings

- claim: "nothing of consequence"
  evidence: "the fixture itself"
  confidence: high

## open-questions

none

## status

done
"""


def put(text):
    block(p, "hb")                      # the block the manifest binds to
    d = os.path.join(BLOCKS, BID, "handoffs")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, MARK + ".yml"), "w", encoding="utf-8").write(text)


def case(label, text, want_id, want_code):
    p.clean()
    put(text)
    code, out, err = p.run()
    v, ids, detail = p.verdict(want_id)
    ok = v == "FAIL" and code == want_code
    mark = "✅" if ok else ("⚠️" if v == "FAIL" else "🔴")
    print("  %-44s %s %-14s exit=%d (esperado %d) %s"
          % (label, mark, v, code, want_code, " ".join(ids)))
    p.clean()
    p.results.append((label, "FAIL" if ok else v + "/exit"))
    return ok


print("═══ SABOTAGE · check-handoff · with its exit code ═══\n")
p.baseline()

case("① a required field is missing",
     GOOD.replace('handoff_id: "2026-01-15-0900-audit"\n', ""), "HND-MAN-001", 1)
case("② an unknown schema version",
     GOOD.replace("schema_version: v1", "schema_version: v9"), "HND-MAN-002", 1)
case("③ an empty stop_condition",
     GOOD.replace('stop_condition: "after the listed files, or on any read error"',
                  'stop_condition: ""'), "HND-MAN-003", 1)
case("④ a stop_condition that is not observable",
     GOOD.replace('stop_condition: "after the listed files, or on any read error"',
                  'stop_condition: "when done"'), "HND-MAN-003", 1)
case("⑤ a write scope with no artefact",
     GOOD.replace('    path: "handoffs/return.md"', '    path: ""'), "HND-WRT-001", 1)
case("⑤b an undeclared write mode",
     GOOD.replace("    mode: create-only\n", ""), "HND-WRT-004", 1)
case("⑤c no declared capabilities",
     GOOD.replace("agent:\n  capabilities:\n    read: true\n    write: false\n", ""),
     "HND-GAT-004", 1)
case("⑤d an incomplete status set",
     GOOD.replace("      - failed\n", ""), "HND-RET-002", 1)
case("⑥ an append to a coordinator section",
     GOOD.replace("also_append: []",
                  'also_append:\n    - "{target: BLOCK.md, section: state, max_lines: 5}"'),
     "HND-WRT-002", 1)
case("⑦ an append with no max_lines",
     GOOD.replace("also_append: []",
                  'also_append:\n    - "{target: BLOCK.md, section: context}"'),
     "HND-WRT-003", 1)
case("⑧ an incomplete return schema",
     GOOD.replace("      - open-questions\n", ""), "HND-RET-001", 1)
case("⑨ binding · the block does not exist",
     GOOD.replace('block_path: "work/blocks/%s"' % BID,
                  'block_path: "work/blocks/ghost"'), "HND-BND-001", 1)
case("⑩ binding · the id does not match",
     GOOD.replace('block: "%s"' % BID, 'block: "other"'), "HND-BND-001", 1)
case("⑪ binding · a read path does not resolve",
     GOOD.replace("    - BLOCK.md", "    - MISSING.md"), "HND-BND-001", 1)

case("⑪b GATE · an UNDECLARED capability",
     GOOD.replace("    read: true\n", ""), "HND-GAT-005", 1)
case("⑪c GATE · an unknown agent type",
     GOOD.replace("agent:\n  capabilities:",
                  "agent:\n  type: auditor\n  capabilities:")
         .replace("    write: false", "    write: true"), "HND-GAT-001", 1)
case("⑪d GATE · a field still carrying the template placeholder",
     GOOD.replace('block: "%s"' % BID, "block: ⬜"), "HND-GAT-002", 1)

p.inverse("⑫ a CORRECT manifest", lambda: put(GOOD))


# ── POST-FLIGHT · lo que valida el RETORNO
def post(label, ret, want_id, want_code):
    """⭐ Validating before the specialist runs is half the problem."""
    p.clean()
    put(GOOD)
    if ret is not None:
        open(os.path.join(BLOCKS, BID, "handoffs", "return.md"), "w",
             encoding="utf-8").write(ret)
    r = subprocess.run([sys.executable, "bin/check-handoff", "--postflight",
                        "--quiet"], cwd=ROOT, capture_output=True, text=True)
    ids = sorted(set(re.findall(r"HND-[A-Z]+-\d+", r.stdout)))
    # ⭐ CHK-XIT-001 · a violated contract is REJECT, and REJECT is exit 1.
    # ⛔ These cases expected 2 and 3, and 2 is the code every other validator
    # uses for "I could NOT measure" — a rejection wearing the code for a gap,
    # which is the exact collapse the verdict vocabulary exists to prevent.
    ok = want_id in ids and r.returncode == want_code
    print("  %-44s %s %-14s exit=%d (esperado %d) %s"
          % (label, "✅" if ok else "🔴", "FAIL" if ids else "NOT_DETECTED",
             r.returncode, want_code, " ".join(ids)))
    p.clean()
    p.results.append((label, "FAIL" if ok else "NOT_DETECTED"))
    return ok


print("\n── POST-FLIGHT · valida lo que devolvio el especialista\n")
post("⑬ done sin artefacto de retorno", None, "HND-PST-002", 1)
post("⑭ artefacto con una seccion ausente",
     RETURN.replace("## open-questions\n\nnone\n\n", ""), "HND-PST-001", 1)
post("⑮ status fuera del conjunto",
     RETURN.replace("done\n", "finished\n"), "HND-PST-001", 1)
post("⑯ secciones fuera de orden",
     RETURN.replace("## work", "## zz").replace("## findings", "## work")
           .replace("## zz", "## findings"), "HND-PST-001", 1)

post("⑯b STP · a boundary stop that never says what was missing",
     RETURN.replace("## status\n\ndone\n",
                    "## status\n\nblocked\n\nI could not continue.\n"),
     "HND-STP-003", 1)
# ⭐ the inverse: a boundary stop that DOES name what it lacked must not fire.
# Without it the rule is only proven on broken input, and a check that fires on
# every blocked return is a check that gets switched off.
p.clean()
put(GOOD)
open(os.path.join(BLOCKS, BID, "handoffs", "return.md"), "w",
     encoding="utf-8").write(
    RETURN.replace("## status\n\ndone\n",
                   "## status\n\nblocked\n\nneeds the schema at "
                   "db/schema.sql, outside the read scope\n"))
_r = subprocess.run([sys.executable, "bin/check-handoff", "--postflight", "--quiet"],
                    cwd=ROOT, capture_output=True, text=True)
_ok = "HND-STP-003" not in _r.stdout
print("  %-44s %s %s" % ("⑯c STP · a stop that DOES name what was missing",
                         "✅" if _ok else "🔴",
                         "NO dispara (correcto)" if _ok else _r.stdout.strip()[:70]))
p.results.append(("boundary stop names it", "PASS" if _ok else "FALSE_POSITIVE"))
p.clean()

# ⭐ la prueba inversa del post-flight
p.clean()
put(GOOD)
open(os.path.join(BLOCKS, BID, "handoffs", "return.md"), "w",
     encoding="utf-8").write(RETURN)
r = subprocess.run([sys.executable, "bin/check-handoff", "--postflight", "--quiet"],
                   cwd=ROOT, capture_output=True, text=True)
ok = r.returncode == 0 and "🔴" not in r.stdout
print("  %-44s %s %s" % ("⑰ un retorno CORRECTO", "✅" if ok else "🔴",
                         "NO dispara (correcto)" if ok
                         else r.stdout.strip()[:80]))
p.results.append(("⑰ retorno correcto", "PASS" if ok else "FALSE_POSITIVE"))
p.clean()
p.crash_guard()

sys.exit(0 if p.report() else 1)
