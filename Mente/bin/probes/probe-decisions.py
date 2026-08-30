#!/usr/bin/env python3
"""probe-decisions — does check-decisions detect what contract-adr.md claims?"""
import os, sys, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK

D = os.path.join(ROOT, "rules", "decisions")
p = Probe("check-decisions", "DEC")

# ⭐ Fixtures number from 900 up: the engine now ships records of its own, and
# 001 collided with a REAL one. The collision was correctly reported — ⛔ but it
# was the probe reusing a number, not the checker misbehaving.
GOOD = """# 901 · Keep one decision in one file

date: 2026-01-15
status: accepted
implementation: verified
decided-by: the owner
supersedes: —
superseded-by: —
applies-to: every decision record in this installation
does-not-apply-to: decisions local to a single open block

## Context

Records kept as table rows ended up in two tables, and the two diverged.

## Decision

One decision is one file.

## Rejected alternatives

- a single shared table, which cannot carry evidence or a way back
- an append-only log, which cannot be superseded

## Rationale

A file carries its evidence, its boundary and its exit; a row carries none.

## Evidence

Two tables of the same decisions, with different row counts.

## Consequences

Every record is a file under this folder, and the index is generated from them.

## Reverting

Merge the files back into a table, losing evidence and reverting fields.
"""


def put(text, name="901-" + MARK + ".md"):
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
       lambda: (put(GOOD, "901-" + MARK + "-a.md"), put(GOOD, "901-" + MARK + "-b.md")),
       "DEC-NUM-002")
p.case("⑧ enlace supersede de un solo lado",
       lambda: (put(GOOD.replace("superseded-by: —", "superseded-by: 902"),
                    "901-" + MARK + "-a.md"),
                put(GOOD.replace("# 901 ·", "# 902 ·")
                    .replace("applies-to: every decision record in this installation",
                             "applies-to: a different subject entirely"),
                    "902-" + MARK + "-b.md")),
       "DEC-SUP-001")
p.case("⑨ supersede a un registro inexistente",
       lambda: put(GOOD.replace("supersedes: —", "supersedes: 099"),
                   "901-" + MARK + "-a.md"), "DEC-SUP-002")
p.case("⑩ superseded pero status accepted",
       lambda: (put(GOOD.replace("superseded-by: —", "superseded-by: 902"),
                    "901-" + MARK + "-a.md"),
                put(GOOD.replace("# 901 ·", "# 902 ·")
                    .replace("applies-to: every decision record in this installation",
                             "applies-to: a different subject entirely")
                    .replace("supersedes: —",
                                                               "supersedes: 901"),
                    "902-" + MARK + "-b.md")), "DEC-SUP-003")

# ── las 5 reglas nuevas
p.case("⑪ sin estado de implementación",
       lambda: put(GOOD.replace("implementation: verified\n", "")), "DEC-IMP-001")
p.case("⑫ estado de implementación desconocido",
       lambda: put(GOOD.replace("implementation: verified", "implementation: done")),
       "DEC-IMP-001")
p.case("⑬ aceptado hace mucho y nunca empezado",
       lambda: put(GOOD.replace("implementation: verified",
                                "implementation: not-started")), "DEC-IMP-003")
p.case("⑭ supersedes sin decir por qué",
       lambda: put(GOOD.replace("supersedes: —", "supersedes: 099")), "DEC-FLD-006")
p.case("⑮ sin declarar dónde aplica",
       lambda: put(re.sub(r"applies-to: .*\n", "", GOOD)), "DEC-FLD-007")
p.case("⑯ alternativas rechazadas sin nombrar",
       lambda: put(re.sub(r"## Rejected alternatives\n\n.*?\n\n",
                          "## Rejected alternatives\n\nwe looked at some others\n\n",
                          GOOD, flags=re.S)), "DEC-FLD-005")

p.case("⑰b ONE · la decisión es una TABLA de filas",
       lambda: put(GOOD.replace(
           "One decision is one file.",
           "| # | choice |\n|---|---|\n| 1 | this |\n| 2 | that |\n| 3 | other |")),
       "DEC-ONE-001")

p.case("⑰c NUM · revertida sin decir por qué",
       lambda: put(GOOD.replace("status: accepted", "status: reverted")
                       .replace("## Rationale\n\nA file carries its evidence, "
                                "its boundary and its exit; a row carries none.\n", "")),
       "DEC-NUM-003")

p.case("⑰d SRC · dos registros vigentes sobre el mismo asunto",
       lambda: (put(GOOD),
                put(GOOD.replace("# 901 ·", "# 902 ·"), "902-" + MARK + ".md")),
       "DEC-SRC-003")

p.case("⑰e NUM · el nombre del archivo nombra a quien decidió",
       lambda: put(GOOD.replace("decided-by: the owner", "decided-by: alexandra"),
                   "903-" + MARK + "-alexandra-decides.md"), "DEC-NUM-004")

# ⭐ the inverse: the same owner, a filename that names the DECISION — must not fire.
p.inverse("⑰f NUM · el mismo dueño, nombre que describe la decisión",
          lambda: put(GOOD.replace("decided-by: the owner", "decided-by: alexandra"),
                      "904-" + MARK + "-one-file-per-record.md"))

p.case("⑰g SUP · cita en prosa un ADR que no existe",
       lambda: put(GOOD.replace("## Rationale",
                                "## Consequences\n\n- `ADR-777` — something\n\n## Rationale")),
       "DEC-SUP-004")

# ⭐ the inverse: the same citation marked ⬜ planned must NOT fire.
p.inverse("⑰h SUP · la misma cita, marcada ⬜ planned",
          lambda: put(GOOD.replace("## Rationale",
                                   "## Consequences\n\n- ⬜ `ADR-777` (planned) — something\n\n## Rationale")))

p.inverse("⑰ un registro CORRECTO", lambda: put(GOOD))
p.crash_guard()

# ── B · CORRIDA CRUZADA
# ⛔ This said "another instance's decisions are not comparable — their records
# are theirs". That was an excuse, not a reason: what is theirs is the CONTENT;
# the SHAPE is exactly what this contract fixes, and 30 real records carry it.
# A cross-run declined on a made-up reason is the emptiest NOT_MEASURED there is.
print("\n═══ B · CORRIDA CRUZADA · registros reales de otra instancia ═══\n")
p.clean()
REF = os.environ.get("MENTE_CROSSRUN_DECISIONS", "")
real = sorted(glob.glob(os.path.join(REF, "*.md"))) if REF else []
real = [q for q in real if not os.path.basename(q).upper().startswith("README")]
if real:
    for i, q in enumerate(real[:8]):
        put(open(q, encoding="utf-8").read(),
            "%03d-%s-x.md" % (900 + i, MARK))
    code, out, err = p.run()
    mine = [l for l in out.splitlines() if MARK in l]
    by = {}
    for l in mine:
        for m in re.findall(r"DEC-[A-Z]+-\d+", l):
            by[m] = by.get(m, 0) + 1
    print("  ⑱ %d registros REALES · %d hallazgos" % (min(len(real), 8), len(mine)))
    for k in sorted(by):
        print("       %-14s %d" % (k, by[k]))
    for l in mine[:4]:
        print("     " + l.split(" · ", 2)[-1][:94])
else:
    print("  ⑱ ⬜ NOT_MEASURED · set MENTE_CROSSRUN_DECISIONS to a real decisions/ folder")
p.clean()
sys.exit(0 if p.report() else 1)
