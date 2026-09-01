#!/usr/bin/env python3
"""probe-accounts — proves the registry validator detects what rule-accounts claims.

⭐ THE ONE THIS FILE EXISTS FOR is ACC-REG-004. A role invented in a row and
never declared passes silently — and that silence is exactly how a retired
repository keeps receiving work. ⛔ A validator that only knows the roles someone
remembered to hardcode has the same hole, one layer deeper, which is why the
roles are read from the registry's own header and why that is measured here.

⚠️ Runs against an ISOLATED COPY: the registry is instance data, and planting
rows in a real one would leave a machine declaring repositories that do not
exist.
"""
import os, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-accounts-")
TREE = os.path.join(WORK, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git"))
CHECK = os.path.join(TREE, "bin", "check-accounts")
REG = os.path.join(TREE, "accounts.tsv")
HEADER = "repo\tcuenta\trol\tremoto\truta_local\tpor_que_existe\tguia\n"
# A row that is correct in every respect — every case below breaks exactly one
# thing in it, so a finding can only come from the thing that was broken.
GOOD = "an-org/a-repo\tan-account\ttaller\torigin\t-\twhere the work is built\t-\n"


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def run(rows=None, drop_registry=False):
    if drop_registry:
        if os.path.exists(REG):
            os.remove(REG)
    else:
        open(REG, "w", encoding="utf-8").write(HEADER + (rows or ""))
    return subprocess.run([sys.executable, CHECK], cwd=TREE,
                          capture_output=True, text=True)


def detects(rows, rule_id):
    r = run(rows)
    # ⭐ The verdict is not "it failed" — it is "it failed FOR THIS REASON".
    # A red for another cause proves nothing about the rule under test.
    return r.returncode == 1 and rule_id in r.stdout, r


print("═══ SONDA · check-accounts ═══\n")

# ── the two empty states, and neither is a pass ─────────────────────────────
r = run(drop_registry=True)
case("① ⬜ sin registro → NOT MEASURED, no ✅",
     r.returncode == 0 and "NOT MEASURED" in r.stdout and "✅" not in r.stdout)
r = run("")
case("② ⬜ registro vacío → NOT MEASURED (un clon nace así)",
     r.returncode == 0 and "NOT MEASURED" in r.stdout and "✅" not in r.stdout)

# ── the baseline · a correct row must NOT be reported ───────────────────────
# ⛔ Measured first, because every case below is only meaningful if the clean
# state is silent. A checker that fires on correct data gets switched off.
r = run(GOOD)
case("③ ⭐ una fila correcta NO se reporta", r.returncode == 0, "exit=%d" % r.returncode)

# ── ACC-REG-002 · a repository that cannot justify itself ───────────────────
ok, r = detects(GOOD.replace("where the work is built", "-"), "ACC-REG-002")
case("④ 🔴 sin `por_que_existe` → detectado", ok)

# ── ACC-REG-004 · THE ONE THAT MATTERS ──────────────────────────────────────
ok, r = detects(GOOD.replace("\ttaller\t", "\tinventado\t"), "ACC-REG-004")
case("⑤ 🔴 un rol NO declarado → detectado", ok)
case("⑥ ⭐ y explica que un rol invisible deja pasar un archivado",
     "retired repository keeps receiving work" in r.stdout)

# ⭐ the roles come from the TEMPLATE, not from a list inside the validator:
# every role the registry declares must be accepted without editing anything
tpl = open(os.path.join(TREE, "templates", "accounts.tsv.template"),
           encoding="utf-8").read()
declared = [w for w in ("taller", "backup", "motor", "control", "sitio",
                        "publicado", "plantilla", "archivado") if w in tpl]
rejected = [d for d in declared
            if run(GOOD.replace("\ttaller\t", "\t%s\t" % d)).returncode != 0]
case("⑦ ⭐ los %d roles de la PLANTILLA se aceptan solos" % len(declared),
     not rejected, str(rejected))

# ⛔ and if the template disappears, the role check is NOT silently skipped
tpl_path = os.path.join(TREE, "templates", "accounts.tsv.template")
shutil.move(tpl_path, tpl_path + ".hidden")
r = run(GOOD.replace("\ttaller\t", "\tinventado\t"))
case("⑧ ⬜ sin plantilla dice que NO midió los roles",
     "roles were not checked" in r.stdout)
shutil.move(tpl_path + ".hidden", tpl_path)

# ── ACC-REG-003 · the pointer, never the credential ─────────────────────────
ok, r = detects(GOOD.replace("\t-\n", "\ttoken=ghp_A1b2C3d4E5f6G7h8I9j0K1\n"),
                "ACC-REG-003")
case("⑨ 🔴 una credencial en la fila → detectada", ok)
case("⑩ ⭐ y ordena ROTAR, no borrar", "ROTATED" in r.stdout)

# ── ACC-REG-001 · a shifted row reads as another row entirely ───────────────
ok, r = detects("an-org/a-repo\tan-account\ttaller\n", "ACC-REG-001")
case("⑪ 🔴 una fila con columnas de menos → detectada", ok)

# ⚠️ separated by SPACES instead of a TAB — the mistake people actually make,
# and it silently becomes a one-column row
ok, r = detects("an-org/a-repo an-account taller origin - why -\n", "ACC-REG-001")
case("⑫ ⚠️ separada por ESPACIOS (no TAB) → detectada", ok)

# ── ACC-VRF-001 · a row is a claim until it is measured ─────────────────────
ok, r = detects(GOOD.replace("\torigin\t-\t", "\torigin\t/nowhere/at/all\t"),
                "ACC-VRF-001")
case("⑬ 🔴 una ruta local que no existe → detectada", ok)

# ⚠️ and `-` means "not cloned", which is legitimate — not a finding
r = run(GOOD)
case("⑭ ⚠️ `-` como ruta es legítimo, no un hallazgo", r.returncode == 0)

# ── ACC-ARC-001 · a retired repository is INFORMATION, not a violation ──────
# ⭐ It is meant to stay declared: one that disappears from the table becomes
# invisible again, and the reason it was retired disappears with it.
r = run(GOOD.replace("\ttaller\t", "\tarchivado\t"))
case("⑮ ⭐ un repo archivado se NOMBRA sin ser violación",
     r.returncode == 0 and "RETIRED" in r.stdout, "exit=%d" % r.returncode)

# ── the report says what it measured ────────────────────────────────────────
r = run(GOOD)
case("⑯ ⭐ el informe dice cuántos repos y cuántos roles midió",
     "declared" in r.stdout and "role(s) known" in r.stdout)

# ── ⬜ the registry's location is the installation's ─────────────────────────
alt = os.path.join(WORK, "elsewhere.tsv")
open(alt, "w", encoding="utf-8").write(HEADER + GOOD.replace(
    "where the work is built", "-"))
r = subprocess.run([sys.executable, CHECK], cwd=TREE, capture_output=True,
                   text=True, env=dict(os.environ, MENTE_ACCOUNTS=alt))
case("⑰ ⬜ el registro se puede declarar en otro sitio",
     r.returncode == 1 and "ACC-REG-002" in r.stdout, "exit=%d" % r.returncode)

# ── 🔴 ACC-LYR-004 · THE FAILURE THAT LOOKS EXACTLY LIKE SUCCESS ────────────
# The hook file exists, its code is correct, its probe passes — and if nothing
# linked it into the tool's hook directory it NEVER RUNS. ⛔ Only layer 1 remains,
# the one a pattern over command text can never fully cover.
GIT = os.path.join(WORK, ".git", "hooks")
os.makedirs(GIT, exist_ok=True)
LINK = os.path.join(GIT, "pre-push")
SRC = os.path.join(TREE, "hooks", "pre-push.sh")


def wiring_says():
    return run(GOOD).stdout


case("⑲ 🔴 la capa 2 SIN enlazar → se reporta",
     "not linked" in wiring_says())

os.symlink(SRC, LINK)
case("⑳ ⭐ enlazada correctamente → sin hallazgo",
     "ACC-LYR-004" not in wiring_says())

# ⚠️ AND A LINK TO SOMETHING ELSE IS WORSE THAN NONE: it looks wired.
os.remove(LINK)
os.symlink(os.path.join(TREE, "bin", "check-accounts"), LINK)
case("㉑ ⚠️ enlazada a OTRA cosa → se reporta (parece cableada)",
     "not to hooks/pre-push.sh" in wiring_says())
os.remove(LINK)

# ── ⛔ a crash is a finding, never a stack trace ─────────────────────────────
open(REG, "wb").write(b"\xff\xfe not text at all\n")
r = subprocess.run([sys.executable, CHECK], cwd=TREE, capture_output=True,
                   text=True)
case("⑱ ⛔ un registro ilegible no revienta la comprobación",
     "Traceback" not in r.stderr, r.stderr.strip()[:30])

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
