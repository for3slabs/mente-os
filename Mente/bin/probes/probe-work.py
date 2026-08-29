#!/usr/bin/env python3
"""probe-work — does check-work detect what rule-working-in-a-block.md claims?"""
import os, re, sys, glob, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK
from fixtures import block, BLOCKS, TODAY

# ⭐ The cross-run needs real objects nobody here wrote. Where they live
# is the operator's business, never the engine's: a hardcoded path makes
# this probe measure one machine (rule-checks-must-measure.md §5).
REF = os.environ.get("MENTE_CROSSRUN_BLOCKS", "")
p = Probe("check-work", "WRK")


def edit(bid, a, b):
    q = os.path.join(BLOCKS, bid, "BLOCK.md")
    s = open(q, encoding="utf-8").read()
    open(q, "w", encoding="utf-8").write(s.replace(a, b))


print("═══ A · SABOTAJE · check-work ═══\n")
p.baseline()

p.case("① sin lane", lambda: edit(block(p, "a"), "lane: task\n", ""), "WRK-LAN-003")
p.case("② lane inválido", lambda: edit(block(p, "a"), "lane: task", "lane: quick"),
       "WRK-LAN-003")
p.case("③ dependiente declarado y lane=task",
       lambda: block(p, "a", conn="- DEPENDS ON: %s-b" % MARK), "WRK-LAN-002")
p.case("④ conexión a un bloque inexistente",
       lambda: block(p, "a", lane="full-block", conn="- DEPENDS ON: ghost-block"),
       "WRK-ISO-002")
p.case("⑤ fricción sin el campo reason",
       lambda: block(p, "a", fric="- %s · rule: something" % TODAY), "WRK-FRI-002")


def three_blocks():
    for n in ("f1", "f2", "f3"):
        block(p, n, fric="- %s · rule: deploy-first · block: %s-%s · "
                         "reason: it blocked an urgent fix" % (TODAY, MARK, n))


p.case("⑥ misma regla en 3 bloques DISTINTOS", three_blocks, "WRK-FRI-003")
p.case("⑦ full-block sin declarar su propagación",
       lambda: block(p, "a", lane="full-block"), "WRK-FIX-003")

# ⭐ the inverse that separates a useful alarm from one that gets switched off
p.clean()
block(p, "r", fric="\n".join(
    "- %s · rule: deploy-first · block: %s-r · reason: chafed again" % (TODAY, MARK)
    for _ in range(3)))
code, out, err = p.run()
fired = "RULE REVIEW" in out
print("  %-46s %s %s" % ("⑧ 3 fricciones en el MISMO bloque",
                         "✅" if not fired else "🔴",
                         "NO dispara (correcto)" if not fired
                         else "falso positivo — no distingue"))
p.results.append(("⑧ mismo bloque", "PASS" if not fired else "FALSE_POSITIVE"))
p.clean()

p.inverse("⑨ un bloque CORRECTO", lambda: block(p, "a"))
p.crash_guard()

print("\n═══ B · CORRIDA CRUZADA · bloques reales de otra instancia ═══\n")
p.clean()
real = sorted(glob.glob(os.path.join(REF, "*", "*", "BLOCK.md"))) if REF else []
if real:
    for q in real:
        d = p.track(os.path.join(BLOCKS, MARK + "-" + os.path.basename(os.path.dirname(q))))
        os.makedirs(d, exist_ok=True)
        shutil.copy(q, os.path.join(d, "BLOCK.md"))
    code, out, err = p.run()
    mine = [l for l in out.splitlines() if MARK in l]
    by = {}
    for l in mine:
        for m in re.findall(r"WRK-[A-Z]+-\d+", l):
            by[m] = by.get(m, 0) + 1
    print("  ⑨ %d bloques reales · %d hallazgos" % (len(real), len(mine)))
    for k in sorted(by):
        print("       %-14s %d" % (k, by[k]))
else:
    print("  ⑨ ⬜ NOT_MEASURED · set %s to a tree of real blocks" % "MENTE_CROSSRUN_BLOCKS")

sys.exit(0 if p.report() else 1)
