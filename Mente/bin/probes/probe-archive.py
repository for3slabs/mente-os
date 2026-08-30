#!/usr/bin/env python3
"""probe-archive — does check-archive detect what contract-archive.md claims?

⭐ The point of this contract: a validator that demands a file whose content is
undefined produces empty files that satisfy it. So the probe plants archives
that LOOK complete and are hollow.
"""
import os, re, shutil, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK

ARCHIVE = os.path.join(ROOT, "work", "blocks", "archive")
REF = os.environ.get("MENTE_CROSSRUN_ARCHIVE", "")
p = Probe("check-archive", "ARC")

HEADER = "**Status:** current · **Type:** analysis · **Updated:** 2026-01-15 · **Owner:** x\n"

SUMMARY = """# Summary · %s

""" % MARK + HEADER + """
## Purpose

What this block was and what it left behind.

## What it was for

turn one measured gap into a written standard

## What was built

- the standard, and the check that enforces it

## The quality verdict

every declared check ran · 0 failures · 12 subjects measured

## What was learned

a validator that demands a file whose content is undefined produces empty
files that satisfy it and teach nothing

## What was left out

the second half of the migration — it moved to another block

Related: `README.md`.
"""

CONNECTIONS = """# Connections · %s

""" % MARK + HEADER + """
## Purpose

What this closing changes for whoever opens the next block.

## Pieces owned

- the standard and its check — now free to claim

## Blocks that depended on it

- none declared

## What is still open

- nothing; the remainder moved to another block

Related: `README.md`.
"""

BLOCK = """# BLOCK · %s

## A · Identity

id: %s
type: docs
status: closed

## K · Closing

closed: 2026-01-20
not completed: the second half
""" % (MARK + "-block", MARK + "-block")


def plant(summary=SUMMARY, conns=CONNECTIONS, block=BLOCK, files=3):
    d = p.track(os.path.join(ARCHIVE, MARK + "-block_2026-01"))
    os.makedirs(d, exist_ok=True)
    if files >= 1 and summary is not None:
        open(os.path.join(d, "SUMMARY.md"), "w", encoding="utf-8").write(summary)
    if files >= 2 and conns is not None:
        open(os.path.join(d, "connections.md"), "w", encoding="utf-8").write(conns)
    if files >= 3 and block is not None:
        open(os.path.join(d, "BLOCK.md"), "w", encoding="utf-8").write(block)
    return d


print("═══ A · SABOTAJE · check-archive ═══\n")
p.baseline()

p.case("① falta uno de los tres archivos",
       lambda: plant(files=2), "ARC-SHP-001")
p.case("② el resumen no lleva cabecera de documento",
       lambda: plant(summary=SUMMARY.replace(HEADER, "")), "ARC-SHP-002")
p.case("③ falta un campo del resumen",
       lambda: plant(summary=re.sub(r"## The quality verdict\n\n.*?\n\n", "",
                                    SUMMARY, flags=re.S)), "ARC-SUM-001")
p.case("④ 'lo aprendido' vacío",
       lambda: plant(summary=re.sub(r"(## What was learned\n\n).*?\n\n",
                                    r"\1x\n\n", SUMMARY, flags=re.S)),
       "ARC-LRN-001")
p.case("⑤ 'lo que quedó fuera' vacío",
       lambda: plant(summary=re.sub(r"(## What was left out\n\n).*?\n\n",
                                    r"\1-\n\n", SUMMARY, flags=re.S)),
       "ARC-SUM-002")
p.case("⑥ falta un campo de conexiones",
       lambda: plant(conns=re.sub(r"## What is still open\n\n.*?\n\n", "",
                                  CONNECTIONS, flags=re.S)), "ARC-CON-001")
p.case("⑦ una credencial en el archivo",
       lambda: plant(block=BLOCK + "\napi_key: sk-abcdefghijklmnop\n"),
       "ARC-NEV-001")

p.case("⑦b DEL · la carpeta no coincide con el id del bloque",
       lambda: plant(block=BLOCK.replace("id: " + MARK + "-block",
                                         "id: something-else")),
       "ARC-DEL-002")
p.case("⑦c SHP · el periodo de la carpeta no es el del cierre",
       lambda: plant(block=BLOCK.replace("closed: 2026-01-20",
                                         "closed: 2026-07-20")),
       "ARC-SHP-003")
# ⛔ Replace the line, never add to it: the fixture already says "moved to",
# so appending a second line left the answer in place and the case planted
# nothing. A probe that adds where it should replace tests the clean state.
p.case("⑦d CON · algo sigue abierto y no dice a dónde se movió",
       lambda: plant(conns=CONNECTIONS.replace(
           "- nothing; the remainder moved to another block",
           "- the second half of the migration")),
       "ARC-CON-003")

p.inverse("⑧ un archivo COMPLETO", lambda: plant())

# ── ⬜ the alias mechanism · it existed, was documented, and never matched:
# the key pattern stopped at the first space and every field name is several
# words. Measured on a real archive: declaring three aliases changed nothing.
# These two cases keep it connected.
_pr = os.path.join(ROOT, "PROJECT-RULES.md")
_orig_pr = open(_pr, encoding="utf-8").read()
_renamed = SUMMARY.replace("## What was built", "## Qué se hizo")
try:
    p.case("⑧b ALIAS · una sección renombrada, sin alias declarado",
           lambda: plant(summary=_renamed), "ARC-SUM-001")

    open(_pr, "w", encoding="utf-8").write(
        _orig_pr + "\narchive_field what was built = (qué se hizo|what was built)\n")
    p.inverse("⑧c ALIAS · la misma sección, CON su alias declarado",
              lambda: plant(summary=_renamed))
finally:
    open(_pr, "w", encoding="utf-8").write(_orig_pr)
    p.clean()

p.crash_guard()

print("\n═══ B · CORRIDA CRUZADA · archivos reales de otra instancia ═══\n")
p.clean()
real = sorted(glob.glob(os.path.join(REF, "*"))) if REF else []
real = [d for d in real if os.path.isdir(d)]
if real:
    # ⛔ The marker cannot ride in the NAME at all: a prefix makes ARC-DEL-002
    # see a renamed block, and a suffix makes ARC-SHP-003 see an invalid
    # period. Measured: 5 false findings each way. ⭐ A cross-run copies the
    # real object VERBATIM, and the filter widens to reach it — the probe
    # adapts to the rules, never the objects to the probe.
    copied = []
    for q in real:
        d = p.track(os.path.join(ARCHIVE, os.path.basename(q)))
        shutil.copytree(q, d, dirs_exist_ok=True)
        copied.append(os.path.basename(q))
    p.also = tuple(p.also) + tuple(copied)
    code, out, err = p.run()
    mine = p._mine(out)
    by = {}
    for l in mine:
        for m in re.findall(r"ARC-[A-Z]+-\d+", l):
            by[m] = by.get(m, 0) + 1
    print("  ⑨ %d archivos reales · %d hallazgos" % (len(real), len(mine)))
    for k in sorted(by):
        print("       %-14s %d" % (k, by[k]))
else:
    print("  ⑨ ⬜ NOT_MEASURED · set MENTE_CROSSRUN_ARCHIVE to a real archive")

sys.exit(0 if p.report() else 1)
