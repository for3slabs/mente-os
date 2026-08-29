#!/usr/bin/env python3
"""probe-document — does check-document detect what contract-document.md claims?"""
import os, sys, re, glob, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK

D = os.path.join(ROOT, "docs")
REF = os.environ.get("MENTE_CROSSRUN_DOCS", "")
p = Probe("check-document", "DOC")

GOOD = """# A probe fixture

**Status:** current · **Type:** rule · **Updated:** 2026-01-15 · **Owner:** someone

## Purpose

A fixture used to prove the checker detects what it claims to.

## 1 · Content

Nothing of consequence.

Related: `README.md`.
"""


def put(text, name=MARK + "-fixture.md"):
    q = p.track(os.path.join(D, name))
    open(q, "w", encoding="utf-8").write(text)
    return q


print("═══ A · SABOTAJE · check-document ═══\n")
p.baseline()

p.case("① cabecera incompleta",
       lambda: put(GOOD.replace(" · **Owner:** someone", "")), "DOC-HDR-001")
p.case("② Status inválido",
       lambda: put(GOOD.replace("**Status:** current", "**Status:** alive")), "DOC-HDR-002")
p.case("③ Type inexistente",
       lambda: put(GOOD.replace("**Type:** rule", "**Type:** invented")), "DOC-HDR-003")
p.case("④ fecha no ISO",
       lambda: put(GOOD.replace("2026-01-15", "15 Jan 2026")), "DOC-HDR-004")
p.case("⑤ superseded sin reemplazo",
       lambda: put(GOOD.replace("**Status:** current", "**Status:** superseded")),
       "DOC-HDR-005")
# ⭐ The fixture must exceed the ceiling the CONTRACT declares, read from the
# contract — a hardcoded size silently stops testing anything the day the
# ceiling is raised, and the probe then reports the check as broken.
def _ceiling(kind="rule"):
    import re as _re
    t = open(os.path.join(ROOT, "rules", "contract-document.md"), encoding="utf-8").read()
    m = _re.search(r"^\|\s*`%s`\s*\|\s*\*{0,2}(?:⭐\s*)?\*{0,2}(\d+)" % kind, t, _re.M)
    return int(m.group(1)) if m else 250


p.case("⑥ techo superado",
       lambda: put(GOOD.replace("Nothing of consequence.",
                                "\n".join("line %d" % i
                                          for i in range(_ceiling() + 50)))),
       "DOC-SIZ-001")
p.case("⑦ sin Purpose",
       lambda: put(GOOD.replace("## Purpose", "## Something else")), "DOC-BOD-001")
p.case("⑧ numeración -bis",
       lambda: put(GOOD.replace("## 1 · Content", "## 1-bis · Content")), "DOC-BOD-002")
p.case("⑨ número vivo en prosa",
       lambda: put(GOOD.replace("Nothing of consequence.",
                                "The suite runs 42 checks today.")), "DOC-CNT-002")
p.case("⑩ puntero que no resuelve",
       lambda: put(GOOD.replace("Nothing of consequence.",
                                "See `rules/ghost.md` for detail.")), "DOC-CNT-004")
p.case("⑪ generated sin decirlo en el cuerpo",
       lambda: put(GOOD.replace("**Owner:** someone",
                                "**Owner:** someone · **Authority:** generated")),
       "DOC-AUT-002")
p.case("⑫ nombre con versión", lambda: put(GOOD, MARK + "-thing-v2.md"), "DOC-NAM-004")
p.case("⑬ nombre con guion bajo", lambda: put(GOOD, MARK + "-a_b.md"), "DOC-NAM-001")
p.case("⑭ fecha en el nombre",
       lambda: put(GOOD, MARK + "-2026-01-15-thing.md"), "DOC-NAM-003")

p.inverse("⑮ un documento CORRECTO", lambda: put(GOOD))
p.crash_guard()

print("\n═══ B · CORRIDA CRUZADA · documentos reales de otra instancia ═══\n")
p.clean()
real = sorted(glob.glob(os.path.join(REF, "*.md")))[:10] if REF else []
for i, q in enumerate(real):
    shutil.copy(q, p.track(os.path.join(D, "%s-x%02d-%s" % (MARK, i, os.path.basename(q)))))
if not real:
    print("  ⑯ ⬜ NOT_MEASURED · set MENTE_CROSSRUN_DOCS to a tree of real documents")
code, out, err = p.run()
mine = p._mine(out) if real else []
by = {}
for l in mine:
    for m in re.findall(r"DOC-[A-Z]+-\d+", l):
        by[m] = by.get(m, 0) + 1
print("  ⑯ %d documentos reales · %d hallazgos" % (len(real), len(mine)))
for k in sorted(by):
    print("       %-14s %d" % (k, by[k]))

sys.exit(0 if p.report() else 1)
