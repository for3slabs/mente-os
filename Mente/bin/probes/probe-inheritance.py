#!/usr/bin/env python3
"""probe-inheritance — does check-inheritance detect what rule-inheritance.md claims?"""
import os, sys, re, shutil
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK
from fixtures import block, BLOCKS

BASE = os.path.join(ROOT, "base-rules.md")
ROUTER = os.path.join(ROOT, "CLAUDE-MENTE-OS.md")
REF = os.environ.get("MENTE_CROSSRUN_RULES", "")
ORIG_BASE = open(BASE, encoding="utf-8").read()
ORIG_ROUTER = open(ROUTER, encoding="utf-8").read()

# ⭐ Probe failure mode #3: a filter narrower than what the probe touches.
# Three cases EDIT rules/rule-inheritance.md, and its findings carry no marker —
# filtering on the marker alone reported a working check as undetected.
p = Probe("check-inheritance", "INH",
          also=("base-rules.md", "CLAUDE-MENTE-OS.md", "rule-inheritance.md"))
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


print("═══ A · SABOTAGE · check-inheritance ═══\n")
p.baseline()

p.case("① a universal rule naming a path",
       lambda: add_universal("| 9 | **Never read ~/other-project/Mente** | x |"),
       "INH-LVL-002")
p.case("② a universal rule naming a host",
       lambda: add_universal("| 9 | **Always deploy through deploy.example.com** | x |"),
       "INH-LVL-002")
p.case("③ a rule marked 🏢 in the universal file",
       lambda: add_universal("| 9 | 🏢 **Never push without an order** | project-level |"),
       "INH-LVL-003")
p.case("④ a rule written in the router",
       lambda: open(ROUTER, "a", encoding="utf-8").write(
           "\nNEVER build a milestone without approval from the owner\n"),
       "INH-RTR-001")
p.case("⑤ a block exempting itself from a rule",
       lambda: block(p, "a", scope="- This block is exempt from the approval rule"),
       "INH-DIR-001")
p.case("⑥ a block repeating a universal rule",
       lambda: block(p, "a",
                     scope="- **The AI does not invent criterion.** Criterion is the owner's"),
       "INH-DIR-003")
p.case("⑦ ESCALATION · the universal denies, the block allows",
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

p.inverse("⑩ a chain with NO cycle · A → B → C",
          lambda: (block(p, "a", conn="- DEPENDS ON: %s-b" % MARK),
                   block(p, "b", conn="- DEPENDS ON: %s-c" % MARK),
                   block(p, "c")))
# ── the four rules implemented in audit 7/13
_rules_dir = os.path.join(ROOT, "rules")
_victim = os.path.join(_rules_dir, "rule-inheritance.md")
_orig_rule = open(_victim, encoding="utf-8").read()

# ⭐ This probe EDITS a real rule file, so its cleaner must restore it too —
# a cleaner that misses one leaves the next case reading stale state.
_prev_clean = p.clean


def clean_with_rule():
    open(_victim, "w", encoding="utf-8").write(_orig_rule)
    _prev_clean()


p.clean = clean_with_rule

p.case("⑪ LVL · a rule with no declared level",
       lambda: open(_victim, "w", encoding="utf-8").write(
           _orig_rule.replace("**Level:** 🌐 universal", "**Scope:** the engine", 1)
                     .replace("🌐", "·").replace("🏢", "·").replace("📦", "·")
                     .replace("universal", "wide").replace("project-level", "narrow")),
       "INH-LVL-001")

p.case("⑫ PRC · a rule row that averages",
       lambda: open(_victim, "w", encoding="utf-8").write(
           _orig_rule + "\n| `INH-ZZZ-999` | a middle ground between both | 🔒 | x |\n"),
       "INH-PRC-002")

p.case("⑬ RTR · the router does not name the three levels",
       lambda: open(ROUTER, "w", encoding="utf-8").write(
           re.sub(r"(?i)block|📦", "thing", ORIG_ROUTER)), "INH-RTR-002")

def cite_in_d(conn="- none"):
    """⛔ The fixture already HAS a §D, so appending another plants the defect
    in a section body_of never reads — the case tested nothing and reported
    the check as broken. Replace the existing one instead."""
    bid = block(p, "a", conn=conn)
    q = os.path.join(BLOCKS, bid, "BLOCK.md")
    t = open(q, encoding="utf-8").read()
    open(q, "w", encoding="utf-8").write(
        t.replace("- `rules/contract-block.md`",
                  "- `work/blocks/other-block/BLOCK.md`"))
    return bid


p.case("⑭ SUM · §D cites another block without declaring it in §C",
       lambda: cite_in_d(), "INH-SUM-001")

# ⭐ the inverse: the same citation WITH the dependency declared must not fire.
p.inverse("⑮ SUM · the same citation, with the connection declared",
          lambda: cite_in_d(conn="- DEPENDS ON: other-block"))

p.crash_guard()

print("\n═══ B · CROSS-RUN · el base-rules REAL de otra instancia ═══\n")
p.clean()
if REF and os.path.exists(REF):
    # ⛔ A directory here crashed the probe with a bare traceback. A crash
    # reports nothing, and "nothing reported" reads like "nothing wrong".
    if os.path.isdir(REF):
        print("  ⬜ NOT_MEASURED · MENTE_CROSSRUN_RULES must name a "
              "base-rules FILE, not a folder: %s" % REF)
        raise SystemExit(0 if p.report() else 1)
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
    print("  ⬜ NOT_MEASURED · set MENTE_CROSSRUN_RULES to a real base-rules file")
p.clean()

print("\n  base-rules identical:", open(BASE, encoding="utf-8").read() == ORIG_BASE)
print("  router identical    :", open(ROUTER, encoding="utf-8").read() == ORIG_ROUTER)
sys.exit(0 if p.report() else 1)
