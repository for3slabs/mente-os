#!/usr/bin/env python3
"""probe-campaign — proves bin/check-campaign detects what contract-campaign claims.

A · plant each defect, verify the CAUSE is named
B · cross-run against a REAL campaign nobody here wrote (MENTE_CROSSRUN_CAMPAIGNS)
"""
import os, sys, re, glob, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, MARK, ROOT          # noqa: E402
import importlib.machinery, importlib.util    # noqa: E402

_ld = importlib.machinery.SourceFileLoader(
    "_cc", os.path.join(ROOT, "bin", "check-campaign"))
_cc = importlib.util.module_from_spec(importlib.util.spec_from_loader("_cc", _ld))
_ld.exec_module(_cc)

REF = os.environ.get("MENTE_CROSSRUN_CAMPAIGNS", "")
p = Probe("check-campaign", "CMP")

CDIR = os.path.join(ROOT, "work", "campaigns")
BDIR = os.path.join(ROOT, "work", "blocks")

GOOD = """# CAMPAIGN · a probe fixture

id: cmp-%(m)s
status: %(status)s · owner: x
created: 2026-01-10
updated: 2026-01-15
%(exempt)s
## Mission

What it pursues, and the condition under which it is finished.

## Authority

The yardstick that settles a contradiction between two documents.

## Standards

%(std)s

## Blocks

| block | what it pursues | state |
|---|---|---|
| %(bid)s | one sentence | %(bstate)s |

## Shared context

%(context)s

## Channel

| fact | contributed by | needed by | date |
|---|---|---|---|
| %(fact)s | %(from)s | %(to)s | 2026-01-12 |

## Closing

%(closing)s
"""

BLOCK = """# BLOCK · %(id)s

## A · Identity

id: %(id)s
status: closed

## B · Scope

- this file

## D · Required standards

%(std)s

%(impact)s
"""


def put(name=MARK + "-camp", **kw):
    d = dict(m=MARK, status="active", exempt="", bid=MARK + "-child",
             std="- `rules/contract-block.md`",
             bstate="active", context="One paragraph of shared context.",
             fact="a fact, in one sentence", **{"from": MARK + "-child"},
             to="another block", closing="The verdict.")
    d.update(kw)
    folder = p.track(os.path.join(CDIR, name))
    os.makedirs(folder, exist_ok=True)
    open(os.path.join(folder, "CAMPAIGN.md"), "w", encoding="utf-8").write(
        GOOD % d)


def child(bid=MARK + "-child", impact="", state="active",
          std="- `rules/contract-document.md`   (its own, ADDED)"):
    d = p.track(os.path.join(BDIR, state, bid))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "BLOCK.md"), "w", encoding="utf-8").write(
        BLOCK % {"id": bid, "impact": impact, "std": std})


def drop(field):
    """Remove a required line from the fixture after writing it."""
    q = os.path.join(CDIR, MARK + "-camp", "CAMPAIGN.md")
    t = open(q, encoding="utf-8").read()
    open(q, "w", encoding="utf-8").write(
        re.sub(r"^%s:[^\n]*\n" % field, "", t, flags=re.M))


def drop_section(name):
    q = os.path.join(CDIR, MARK + "-camp", "CAMPAIGN.md")
    t = open(q, encoding="utf-8").read()
    open(q, "w", encoding="utf-8").write(
        re.sub(r"^## %s\n.*?(?=^## |\Z)" % name, "", t, flags=re.M | re.S))


def _blank_authority():
    q = os.path.join(CDIR, MARK + "-camp", "CAMPAIGN.md")
    t = open(q, encoding="utf-8").read()
    open(q, "w", encoding="utf-8").write(
        re.sub(r"(^## Authority\n).*?(?=^## )", r"\1\n", t, flags=re.M | re.S))


print("═══ A · SABOTAJE · check-campaign · con verificación de CAUSA ═══\n")
p.baseline()

p.case("① FRM · sin sección Mission",
       lambda: (child(), put(), drop_section("Mission")), "CMP-FRM-001")

p.case("② FRM · sin campo de identidad",
       lambda: (child(), put(), drop("created")), "CMP-FRM-002")

p.case("③ FRM · techo superado SIN exención declarada",
       lambda: (child(), put(context="\n".join("line %d" % i for i in range(200)))),
       "CMP-FRM-003")

p.case("④ FRM · el §contexto pasa su propio techo",
       lambda: (child(), put(context="\n".join("line %d" % i for i in range(60)))),
       "CMP-FRM-003")

p.case("⑤ BLK · no declara ningún bloque",
       lambda: (child(), put(), drop_section("Blocks")), "CMP-FRM-001")

p.case("⑥ BLK · nombra un bloque que no existe",
       lambda: put(bid=MARK + "-ghost"), "CMP-BLK-002")

p.case("⑦ BLK · dos campañas reclaman el mismo bloque",
       lambda: (child(), put(), put(name=MARK + "-camp2", m=MARK + "-2")),
       "CMP-BLK-003")

p.case("⑧ CLS · autoridad vacía",
       lambda: (child(), put(), _blank_authority()), "CMP-CLS-002")

p.case("⑨ CHN · un hecho sin quien lo aporta",
       lambda: (child(), put(**{"from": "—"})), "CMP-CHN-001")

p.case("⑩ CHN · un hecho que nadie necesita",
       lambda: (child(), put(to="—")), "CMP-CHN-002")

p.case("⑪ CLS · cerrada con un hijo abierto",
       lambda: (child(), put(status="closed")), "CMP-CLS-001")

p.case("⑫ IMP · un hijo cerrado sin declarar impacto",
       lambda: (child(state="archive"), put(bstate="closed")), "CMP-IMP-001")

p.case("⑬ IMP · un impacto declarado VACÍO",
       lambda: (child(state="archive", impact="### Impact on the campaign\n"),
                put(bstate="closed")), "CMP-IMP-002")

p.case("⑬b STD · el hijo COPIA literal un estándar de la campaña",
       lambda: (child(std="- `rules/contract-block.md`"), put()),
       "CMP-STD-002")

p.case("⑬c STD · el hijo declara que se exime de uno",
       lambda: (child(std="- does not apply here: `rules/contract-block.md`"),
                put()), "CMP-STD-001")

p.inverse("⑭ una campaña CORRECTA", lambda: (child(), put()))
p.crash_guard()


# ── B · cross-run
print("\n═══ B · CORRIDA CRUZADA · una campaña real de otra instancia ═══\n")
p.clean()
real = sorted(glob.glob(os.path.join(REF, "*", "CAMPAIGN.md"))) if REF else []
if real:
    # ⭐ A campaign copied WITHOUT its blocks reports every child as an orphan:
    # the finding is the probe's, not the checker's. Bring the block folders
    # the campaign names, so CMP-BLK-002 measures the campaign and not the copy.
    src_root = os.path.dirname(os.path.abspath(REF.rstrip("/")))
    for i, q in enumerate(real[:3]):
        d = p.track(os.path.join(CDIR, "%s-x%02d" % (MARK, i)))
        os.makedirs(d, exist_ok=True)
        shutil.copy(q, os.path.join(d, "CAMPAIGN.md"))
        # ⭐ Use the CHECKER's parser, never a second copy of it. A real
        # campaign wrote its block names in bold (`**name**`); the checker
        # strips the emphasis and this probe did not, so the probe reported a
        # block it had simply failed to bring. Two parsers over one table
        # diverge — one cannot.
        for name in _cc.blocks_of(open(q, encoding="utf-8").read()):
            for state in ("active", "blocked", "archive"):
                if os.path.isdir(os.path.join(src_root, "blocks", state, name)):
                    tgt = p.track(os.path.join(BDIR, state, name))
                    os.makedirs(tgt, exist_ok=True)
                    open(os.path.join(tgt, "BLOCK.md"), "w",
                         encoding="utf-8").write("# BLOCK · %s\n" % name)
    code, out, err = p.run()
    mine = p._mine(out)
    by = {}
    for l in mine:
        for m in re.findall(r"CMP-[A-Z]+-\d+", l):
            by[m] = by.get(m, 0) + 1
    print("  ⑮ %d campaña(s) REAL(es) · %d hallazgos" % (min(len(real), 3), len(mine)))
    for k in sorted(by):
        print("       %-14s %d" % (k, by[k]))
    for l in mine[:5]:
        print("     " + l.split(" · ", 2)[-1][:96])
else:
    print("  ⑮ ⬜ NOT_MEASURED · set MENTE_CROSSRUN_CAMPAIGNS to a real campaigns/ folder")

sys.exit(0 if p.report() else 1)
