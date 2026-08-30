#!/usr/bin/env python3
"""probe-config — proves bin/check-config detects what rule-config-hygiene claims.

A · plant each defect, verify the CAUSE is named (not just that something went red)
B · cross-run against a REAL configuration nobody here wrote (MENTE_CROSSRUN_CONFIG)
"""
import os, sys, re, json, glob, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, MARK, ROOT          # noqa: E402

REF = os.environ.get("MENTE_CROSSRUN_CONFIG", "")
p = Probe("check-config", "CFG")

# ⭐ The fixture folder carries the marker, so the harness filter cannot be
# narrower than what this probe plants.
FIXDIR = os.path.join(ROOT, "work", MARK + "-config")
FIX = os.path.join(FIXDIR, "settings.json")
LOCAL = os.path.join(FIXDIR, "settings.local.json")

CLEAN = {
    "permissions": {
        "allow": ["Bash(git status)", "Bash(git diff:*)", "Read(docs/**)"],
        "deny": ["Read(.env)", "Bash(cat:*)", "Bash(strings:*)",
                 "Bash(xxd:*)", "Bash(cp:*)"],
        "additionalDirectories": [],
    }
}


def put(mutate=None, local=None):
    cfg = json.loads(json.dumps(CLEAN))
    if mutate:
        mutate(cfg)
    os.makedirs(p.track(FIXDIR), exist_ok=True)
    open(FIX, "w", encoding="utf-8").write(json.dumps(cfg, indent=2))
    if local is not None:
        open(LOCAL, "w", encoding="utf-8").write(json.dumps(local, indent=2))


print("═══ A · SABOTAJE · check-config · con verificación de CAUSA ═══\n")
p.baseline()

p.case("① SEC · un secreto pegado en un permiso",
       lambda: put(lambda c: c["permissions"]["allow"].append(
           "Bash(psql --password=hunter2supersecret)")), "CFG-SEC-001")

p.case("② SUR · permiso al intérprete de shell",
       lambda: put(lambda c: c["permissions"]["allow"].append("Bash(bash:*)")),
       "CFG-SUR-003")

p.case("③ SUR · borrado recursivo sin límite",
       lambda: put(lambda c: c["permissions"]["allow"].append("Bash(rm -rf *)")),
       "CFG-SUR-003")

p.case("④ WHY · una ruta concedida que no existe",
       lambda: put(lambda c: c["permissions"]["additionalDirectories"].append(
           "/nonexistent/" + MARK + "/path")), "CFG-WHY-003")

p.case("⑤ ONE · muchas entradas para un mecanismo",
       lambda: put(lambda c: c["permissions"]["allow"].extend(
           ["Bash(git log)", "Bash(git show)", "Bash(git blame)",
            "Bash(git stash)", "Bash(git tag)"])), "CFG-ONE-002")

p.case("⑥b ONE · el MISMO comando escrito de dos formas",
       lambda: put(lambda c: c["permissions"]["allow"].extend(
           ["Bash(bin/a:*)", "Bash(./bin/a:*)",
            "Bash(bin/b:*)", "Bash(./bin/b:*)",
            "Bash(bin/c:*)", "Bash(./bin/c:*)"])), "CFG-ONE-001")

p.case("⑥ ONE · una ruta ya contenida por otra",
       lambda: put(lambda c: c["permissions"]["additionalDirectories"].extend(
           [ROOT, os.path.join(ROOT, "docs")])), "CFG-ONE-001")

p.case("⑦ PRT · ruta absoluta al home de alguien",
       lambda: put(lambda c: c["permissions"]["additionalDirectories"].append(
           "/home/someone/projects/thing")), "CFG-PRT-001")

# CFG-SUR-001 · claimed protected, but another channel still reaches it
p.case("⑧ SUR · protegido POR HERRAMIENTA, con puerta trasera",
       lambda: put(lambda c: c["permissions"].__setitem__(
           "deny", ["Read(.env)"])), "CFG-SUR-001")

p.case("⑨ SHR · una negación que vive solo en el archivo local",
       lambda: put(local={"permissions": {"deny": ["Read(private/**)"]}}),
       "CFG-SHR-001")

p.inverse("⑩ una configuración CORRECTA", lambda: put())
p.crash_guard()

# ── B · cross-run
print("\n═══ B · CORRIDA CRUZADA · una configuración real de otra instancia ═══\n")
p.clean()
if REF and os.path.exists(REF):
    os.makedirs(p.track(FIXDIR), exist_ok=True)
    shutil.copy(REF, FIX)
    code, out, err = p.run()
    mine = p._mine(out)
    by = {}
    for l in mine:
        for m in re.findall(r"CFG-[A-Z]+-\d+", l):
            by[m] = by.get(m, 0) + 1
    print("  ⑪ 1 configuración REAL · %d hallazgos" % len(mine))
    for k in sorted(by):
        print("       %-14s %d" % (k, by[k]))
    for l in mine[:4]:
        print("     " + l.split(" · ", 2)[-1][:96])
else:
    print("  ⑪ ⬜ NOT_MEASURED · set MENTE_CROSSRUN_CONFIG to a real settings.json")

sys.exit(0 if p.report() else 1)
