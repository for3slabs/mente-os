#!/usr/bin/env python3
"""probe-decisions — does check-decisions detect what contract-adr.md claims?"""
import os, sys, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK

D = os.path.join(ROOT, "rules", "decisions")
p = Probe("check-decisions", "DEC")

GOOD = """# 001 · Keep one decision in one file

date: 2026-01-15
status: accepted
decided-by: the owner
supersedes: —
superseded-by: —

## Context

Records kept as table rows ended up in two tables, and the two diverged.

## Decision

One decision is one file.

## Rationale

The rejected alternative was a single table, which cannot carry evidence.

## Evidence

Two tables of the same decisions, with different row counts.

## Reverting

Merge the files back into a table, losing evidence and reverting fields.
"""


def put(text, name="001-" + MARK + ".md"):
    q = p.track(os.path.join(D, name))
    open(q, "w", encoding="utf-8").write(text)
    return q


print("═══ SABOTAJE · check-decisions ═══\n")
p.baseline()

p.case("① falta un campo de cabecera",
       lambda: put(GOOD.replace("decided-by: the owner\n", "")), "DEC-FLD-001")
p.case("② fecha no ISO", lambda: put(GOOD.replace("2026-01-15", "15 Jan 2026")),
       "DEC-FLD-001")
p.case("③ status inválido",
       lambda: put(GOOD.replace("status: accepted", "status: agreed")), "DEC-FLD-002")
p.case("④ falta una sección",
       lambda: put(re.sub(r"## Reverting\n.*", "", GOOD, flags=re.S)), "DEC-FLD-003")
p.case("⑤ Evidence vacío",
       lambda: put(re.sub(r"## Evidence\n\n.*?\n\n", "## Evidence\n\n\n", GOOD, flags=re.S)),
       "DEC-FLD-004")
p.case("⑥ nombre sin número", lambda: put(GOOD, MARK + "-thing.md"), "DEC-NUM-001")
p.case("⑦ número reutilizado",
       lambda: (put(GOOD, "001-" + MARK + "-a.md"), put(GOOD, "001-" + MARK + "-b.md")),
       "DEC-NUM-002")
p.case("⑧ enlace supersede de un solo lado",
       lambda: (put(GOOD.replace("superseded-by: —", "superseded-by: 002"),
                    "001-" + MARK + "-a.md"),
                put(GOOD.replace("# 001 ·", "# 002 ·"), "002-" + MARK + "-b.md")),
       "DEC-SUP-001")
p.case("⑨ supersede a un registro inexistente",
       lambda: put(GOOD.replace("supersedes: —", "supersedes: 099"),
                   "001-" + MARK + "-a.md"), "DEC-SUP-002")
p.case("⑩ superseded pero status accepted",
       lambda: (put(GOOD.replace("superseded-by: —", "superseded-by: 002"),
                    "001-" + MARK + "-a.md"),
                put(GOOD.replace("# 001 ·", "# 002 ·").replace("supersedes: —",
                                                               "supersedes: 001"),
                    "002-" + MARK + "-b.md")), "DEC-SUP-003")

p.inverse("⑪ un registro CORRECTO", lambda: put(GOOD))
p.crash_guard()

print("\n  ⚠️ sin corrida cruzada: la carpeta de decisiones de otra instancia\n"
      "     no es comparable — sus registros son suyos. NOT_MEASURED, dicho.")
sys.exit(0 if p.report() else 1)
