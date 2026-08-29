#!/usr/bin/env python3
"""probe-handoff — does check-handoff detect what contract-handoff.md claims?

⭐ It also verifies the EXIT CODE: 2 means fix the manifest, 3 means the
manifest describes a world that does not exist. They send you to different
places, so a probe that only checks the finding proves half of it.
"""
import os, sys, re
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
write_back:
  artifact: "handoffs/return.md"
  artifact_schema:
    - objective
    - work
    - findings
    - open-questions
    - status
  also_append: []
""" % (BID, BID)


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


print("═══ SABOTAJE · check-handoff · con código de salida ═══\n")
p.baseline()

case("① falta un campo requerido",
     GOOD.replace('handoff_id: "2026-01-15-0900-audit"\n', ""), "HND-MAN-001", 2)
case("② versión de esquema desconocida",
     GOOD.replace("schema_version: v1", "schema_version: v9"), "HND-MAN-002", 2)
case("③ stop_condition vacío",
     GOOD.replace('stop_condition: "after the listed files, or on any read error"',
                  'stop_condition: ""'), "HND-MAN-003", 2)
case("④ stop_condition no observable",
     GOOD.replace('stop_condition: "after the listed files, or on any read error"',
                  'stop_condition: "when done"'), "HND-MAN-003", 2)
case("⑤ write scope sin artefacto",
     GOOD.replace('artifact: "handoffs/return.md"', 'artifact: ""'), "HND-WRT-001", 2)
case("⑥ append a una sección del coordinador",
     GOOD.replace("also_append: []",
                  'also_append:\n    - "{target: BLOCK.md, section: state, max_lines: 5}"'),
     "HND-WRT-002", 2)
case("⑦ append sin max_lines",
     GOOD.replace("also_append: []",
                  'also_append:\n    - "{target: BLOCK.md, section: context}"'),
     "HND-WRT-003", 2)
case("⑧ esquema de retorno incompleto",
     GOOD.replace("    - open-questions\n", ""), "HND-RET-001", 2)
case("⑨ binding · el bloque no existe",
     GOOD.replace('block_path: "work/blocks/%s"' % BID,
                  'block_path: "work/blocks/ghost"'), "HND-BND-001", 3)
case("⑩ binding · el id no coincide",
     GOOD.replace('block: "%s"' % BID, 'block: "other"'), "HND-BND-001", 3)
case("⑪ binding · una ruta de lectura no resuelve",
     GOOD.replace("    - BLOCK.md", "    - MISSING.md"), "HND-BND-001", 3)

p.inverse("⑫ un manifiesto CORRECTO", lambda: put(GOOD))
p.crash_guard()

sys.exit(0 if p.report() else 1)
