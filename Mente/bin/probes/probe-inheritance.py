#!/usr/bin/env python3
"""probe-inheritance — does check-inheritance detect what rule-inheritance.md claims?"""
import os, sys, re, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK
from fixtures import block, BLOCKS

BASE = os.path.join(ROOT, "base-rules.md")
ROUTER = os.path.join(ROOT, "CLAUDE-MENTE-OS.md")
REF = os.environ.get("MENTE_CROSSRUN_RULES", "")
ORIG_BASE = open(BASE, encoding="utf-8").read()
ORIG_ROUTER = open(ROUTER, encoding="utf-8").read()

p = Probe("check-inheritance", "INH",
          also=("base-rules.md", "CLAUDE-MENTE-OS.md"))
_clean = p.clean


def clean():
    """⭐ Restore the files this probe EDITS, not only the ones it creates:
    a cleaner that misses one leaves the next case reading stale state."""
    open(BASE, "w", encoding="utf-8").write(ORIG_BASE)
    open(ROUTER, "w", encoding="utf-8").write(ORIG_ROUTER)
    _clean()


p.clean = clean


def add_universal(row):
    open(BASE, "a", encoding="utf-8").write("\n%s\n" % row)


print("═══ A · SABOTAJE · check-inheritance ═══\n")
p.baseline()

p.case("① regla universal que nombra una ruta",
       lambda: add_universal("| 9 | **Never read ~/other-project/Mente** | x |"),
       "INH-LVL-002")
p.case("② regla universal que nombra un host",
       lambda: add_universal("| 9 | **Always deploy through deploy.example.com** | x |"),
       "INH-LVL-002")
p.case("③ regla marcada 🏢 en el universal",
       lambda: add_universal("| 9 | 🏢 **Never push without an order** | project-level |"),
       "INH-LVL-003")
p.case("④ regla escrita en el enrutador",
       lambda: open(ROUTER, "a", encoding="utf-8").write(
           "\nNEVER build a milestone without approval from the owner\n"),
       "INH-RTR-001")
p.case("⑤ bloque que se exime de una regla",
       lambda: block(p, "a", scope="- This block is exempt from the approval rule"),
       "INH-DIR-001")
p.case("⑥ bloque que repite una regla universal",
       lambda: block(p, "a",
                     scope="- **The AI does not invent criterion.** Criterion is the owner's"),
       "INH-DIR-003")
p.case("⑦ ESCALAMIENTO · el universal deniega, el bloque permite",
       lambda: (add_universal(
           "| 9 | **Never build a milestone without explicit approval** | x |"),
           block(p, "a",
                 scope="- A milestone may be built here without explicit approval")),
       "INH-ESC-001")
p.case("⑧ CICLO · A → B → A",
       lambda: (block(p, "a", conn="- DEPENDS ON: %s-b" % MARK),
                block(p, "b", conn="- DEPENDS ON: %s-a" % MARK)), "INH-SUM-003")
p.case("⑨ CICLO largo · A → B → C → A",
       lambda: (block(p, "a", conn="- DEPENDS ON: %s-b" % MARK),
                block(p, "b", conn="- DEPENDS ON: %s-c" % MARK),
                block(p, "c", conn="- DEPENDS ON: %s-a" % MARK)), "INH-SUM-003")

p.inverse("⑩ cadena SIN ciclo · A → B → C",
          lambda: (block(p, "a", conn="- DEPENDS ON: %s-b" % MARK),
                   block(p, "b", conn="- DEPENDS ON: %s-c" % MARK),
                   block(p, "c")))
p.crash_guard()

print("\n═══ B · CORRIDA CRUZADA · el base-rules REAL de otra instancia ═══\n")
p.clean()
if REF and os.path.exists(REF):
    shutil.copy(REF, BASE)
    code, out, err = p.run()
    rows = [l for l in out.splitlines() if "🔴" in l]
    by = {}
    for l in rows:
        for m in re.findall(r"INH-[A-Z]+-\d+", l):
            by[m] = by.get(m, 0) + 1
    print("  ⑪ base-rules real · %d hallazgos" % len(rows))
    for k in sorted(by):
        print("       %-14s %d" % (k, by[k]))
    for l in rows[:3]:
        print("     " + l.split(" · ", 2)[-1][:96])
else:
    print("  ⑪ ⬜ NOT_MEASURED · set MENTE_CROSSRUN_RULES to a real base-rules file")
p.clean()

print("\n  base-rules idéntico:", open(BASE, encoding="utf-8").read() == ORIG_BASE)
print("  router idéntico    :", open(ROUTER, encoding="utf-8").read() == ORIG_ROUTER)
sys.exit(0 if p.report() else 1)
