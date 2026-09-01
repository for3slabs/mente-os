#!/usr/bin/env python3
"""probe-grade — proves bin/grade-block measures what contract-quality-verdict claims.

⭐ This probe is different from the others: grade-block does not emit rule ids,
it emits a VERDICT. So the assertion is the verdict itself — plant a defect and
the block must drop from PRODUCT to the right state, for the right reason.

A · one planted defect per measured row, verdict AND cause verified
B · the two failures the contract records: ⬜ is not a pass, empty scope is not a pass
C · the thresholds are read from the contract, not from the script
D · cross-run against a REAL block nobody here wrote (MENTE_CROSSRUN_BLOCKS)
"""
import os, sys, re, json, glob, shutil, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import MARK, ROOT                 # noqa: E402

REF = os.environ.get("MENTE_CROSSRUN_BLOCKS", "")
REPO = os.path.dirname(ROOT)
BDIR = os.path.join(ROOT, "work", "blocks", "active", MARK + "-graded")
SCOPE = os.path.join(ROOT, "work", MARK + "-scope")
REL = os.path.relpath(SCOPE, REPO)
CONTRACT = os.path.join(ROOT, "rules", "contract-quality-verdict.md")

BLOCK = """# BLOCK · %(name)s

## A · Identity

id: %(name)s
type: %(type)s
status: active
created: 2026-01-10 · updated: 2026-01-15

## B · Scope

### ✅ IN
- `%(scope)s`

### ⛔ OUT
- everything else
"""

results = []


def clean():
    shutil.rmtree(BDIR, ignore_errors=True)
    shutil.rmtree(SCOPE, ignore_errors=True)


def plant(files, btype="code", scope=REL):
    clean()
    os.makedirs(BDIR, exist_ok=True)
    open(os.path.join(BDIR, "BLOCK.md"), "w", encoding="utf-8").write(
        BLOCK % {"name": MARK + "-graded", "type": btype, "scope": scope})
    os.makedirs(SCOPE, exist_ok=True)
    for n, body in files.items():
        q = os.path.join(SCOPE, n)
        os.makedirs(os.path.dirname(q), exist_ok=True)
        open(q, "w", encoding="utf-8").write(body)


def run(*extra):
    r = subprocess.run([sys.executable, "bin/grade-block", MARK + "-graded",
                        "--root", REPO, *extra],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def case(label, files, want_verdict, want_row=None, btype="code", scope=REL):
    plant(files, btype, scope)
    code, out = run()
    if "crashed ·" in out or "Traceback" in out:
        v, mark = "CRASH", "🔴"
    else:
        m = re.search(r"LAYER 1 VERDICT: \S+ ([A-Z ]+)", out)
        got = (m.group(1).strip() if m else "—")
        if got != want_verdict:
            v, mark = "WRONG_VERDICT → %s" % got, "🔴"
        elif want_row and not any(
                want_row in l and ("🔴" in l or "🟡" in l)
                for l in out.splitlines()):
            # ⭐ The verdict alone is not the cause: a block can go red for the
            # wrong row and read exactly like a correct detection.
            v, mark = "WRONG_CAUSE (row not flagged)", "⚠️"
        else:
            v, mark = "OK · %s" % want_verdict, "✅"
    print("  %-46s %s %s" % (label, mark, v))
    clean()
    results.append((label, v.startswith("OK")))
    return v.startswith("OK")


# ── the clean fixture every case mutates
CLEAN = {
    "used.py": "def helper():\n    return 1\n",
    "main.py": "from .used import helper\n\n\ndef main():\n    return helper()\n",
    "test_main.py": "from .main import main\n\n\ndef test_main():\n    assert main() == 1\n",
}

print("═══ A · SABOTAJE · grade-block · veredicto Y causa ═══\n")

case("⓪ a CLEAN block", CLEAN, "PRODUCT")

case("① a file nobody imports",
     dict(CLEAN, orphan_thing="", **{"orphan.py": "def x():\n    return 1\n"}),
     "MVP", "files nobody imports")

case("② with no test file at all",
     {k: v for k, v in CLEAN.items() if not k.startswith("test_")},
     "MVP", "test files")

case("③ a secret written into the code",
     dict(CLEAN, **{"cfg.py": 'from .used import helper\n'
                              'password = "hunter2supersecret"\n'}),
     "MVP", "secret values written down")

case("④ an import cycle",
     {"a.py": "from .b import gb\n\n\ndef ga():\n    return gb()\n",
      "b.py": "from .a import ga\n\n\ndef gb():\n    return 1\n",
      "main.py": "from .a import ga\nfrom .b import gb\n",
      "test_main.py": "from .main import ga\n\n\ndef test_x():\n    assert ga\n"},
     "MVP", "import cycles")

_dup = "\n".join("    step_%d = %d" % (i, i) for i in range(10))
case("⑤ a duplicated block",
     dict(CLEAN,
          **{"one.py": "from .used import helper\n\n\ndef f():\n%s\n" % _dup,
             "two.py": "from .used import helper\n\n\ndef g():\n%s\n" % _dup,
             "main.py": "from .one import f\nfrom .two import g\n"
                        "from .used import helper\n"}),
     "MVP", "duplicated blocks")

# 🔴 QLT-SCP-001 · a test OUTSIDE the scope must not count for this block
OUTSIDE = os.path.join(ROOT, "work", MARK + "-outside")
try:
    os.makedirs(OUTSIDE, exist_ok=True)
    open(os.path.join(OUTSIDE, "test_other.py"), "w", encoding="utf-8").write(
        "def test_other():\n    assert True\n")
    case("⑤b SCOPE · a test from ANOTHER block does not count",
         {k: v for k, v in CLEAN.items() if not k.startswith("test_")},
         "MVP", "test files")
finally:
    shutil.rmtree(OUTSIDE, ignore_errors=True)

print()
case("⑥ docs · a broken link",
     {"a.md": "See [the other](./ghost.md).\n", "b.md": "[a](./a.md)\n"},
     "MVP", "broken links", btype="docs")

case("⑦ infra · no documented rollback",
     {"runbook.md": "## How to run\n\nStart the thing.\n"},
     "MVP", "rollback documented", btype="infra")

case("⑧ data · a migration with no way back",
     {"migrations/001_add.sql": "CREATE TABLE t (id INT);\n"},
     "MVP", "migrations WITHOUT a rollback", btype="data")

# ── B · the two failures the contract records
print()
case("⑧b EVD · a scope that only HALF resolves",
     CLEAN, "MVP", "scope paths that do not resolve",
     scope="%s\n- `work/%s-nowhere`" % (REL, MARK))

case("⑨ ⛔ an EMPTY scope is not a pass", {}, "NOTHING MEASURED",
     btype="docs", scope="work/%s-nowhere" % MARK)

plant(CLEAN, "docs")
code, out = run()
na_rows = re.findall(r"^\s+(.+?) \.+\s+n/a\s+⬜", out, re.M)
green = re.findall(r"^\s+(.+?) \.+\s+\d+\s+🟢", out, re.M)
ok = bool(na_rows) and not (set(na_rows) & set(green))
print("  %-46s %s %s" % ("⑩ ⬜ y 🟢 se distinguen en el reporte",
                         "✅" if ok else "🔴",
                         "%d filas ⬜, ninguna como verde" % len(na_rows) if ok
                         else "una fila n/a se renderiza como verde"))
results.append(("⬜ is not a green", ok))
clean()

# ── C · the thresholds come from the contract
orig = open(CONTRACT, encoding="utf-8").read()
try:
    open(CONTRACT, "w", encoding="utf-8").write(
        orig.replace("| ⬜ code file extensions | `.py .js .ts .tsx .jsx` |",
                     "| ⬜ code file extensions | `.zz` |"))
    plant(CLEAN, "code")
    code, out = run()
    # ⭐ With no matching extension nothing is code, so the .py files stay
    # unmeasured — the verdict must change without a line of the script moving.
    moved = "NOTHING MEASURED" in out or "test files ...." in out
    ok = "🔴" in out or "NOTHING" in out
    print("  %-46s %s %s" % ("⑪ el umbral se LEE del contrato",
                             "✅" if ok else "🔴",
                             "editar la tabla cambió la medición" if ok
                             else "la tabla no gobierna nada"))
    results.append(("threshold from contract", ok))
finally:
    open(CONTRACT, "w", encoding="utf-8").write(orig)
    clean()

# QLT-VRD-001 · an MVP names the debt it closes with. ⛔ A verdict printed
# without the rows behind it leaves a debt nobody inherits — the same as never
# having found it.
plant(dict(CLEAN, **{"orphan.py": "def x():\n    return 1\n"}), "code")
_c, _out = run()
_ok = "Closing as MVP requires" in _out and "dead code" in _out
print("  %-46s %s %s" % ("⑫b VRD · el MVP nombra su deuda",
                         "✅" if _ok else "🔴",
                         "listada en el reporte" if _ok else "el veredicto no la nombra"))
results.append(("MVP names its debt", _ok))
clean()

# ── the criterion counter must MOVE when a dimension is declared
orig2 = open(CONTRACT, encoding="utf-8").read()
try:
    plant(CLEAN, "code")
    _, before = run()
    b = re.search(r"(\d+) dimension\(s\) still", before)
    open(CONTRACT, "w", encoding="utf-8").write(
        orig2.replace("| 1 | architecture | ⬜ undeclared |",
                      "| 1 | architecture | one thing, one layer |", 1))
    _, after = run()
    a = re.search(r"(\d+) dimension\(s\) still", after)
    ok = bool(b and a) and int(a.group(1)) == int(b.group(1)) - 1
    print("  %-46s %s %s" % ("⑬ el contador de criterio BAJA al declarar",
                             "✅" if ok else "🔴",
                             "%s → %s" % (b.group(1) if b else "?",
                                          a.group(1) if a else "?")))
    results.append(("criterion counter moves", ok))
finally:
    open(CONTRACT, "w", encoding="utf-8").write(orig2)
    clean()

# ── crash guard
src = open(os.path.join(ROOT, "bin", "grade-block"), encoding="utf-8").read()
cp = os.path.join(ROOT, "bin", MARK + "-grade-crash")
open(cp, "w", encoding="utf-8").write(
    src.replace("def main():", 'def main():\n    raise RuntimeError("boom")', 1))
r = subprocess.run([sys.executable, cp, "x"], cwd=ROOT, capture_output=True, text=True)
ok = "crashed ·" in r.stdout and "Traceback" not in r.stdout
print("  %-46s %s %s" % ("⑫ CRASH · sale como hallazgo", "✅" if ok else "🔴",
                         "reportado, no un trace" if ok
                         else (r.stdout or r.stderr).strip()[:60]))
results.append(("crash guard", ok))
os.remove(cp)

# ── D · cross-run
print("\n═══ B · CORRIDA CRUZADA · un bloque real de otra instancia ═══\n")
real = sorted(glob.glob(os.path.join(REF, "*", "*", "BLOCK.md"))) if REF else []
if real:
    shown = 0
    for q in real:
        name = os.path.basename(os.path.dirname(q))
        # …/<repo>/<engine>/work?/blocks/<state>/<name>/BLOCK.md — walk up to
        # the REPO, never to the engine folder. ⚠️ Getting this off by one
        # dirname makes every scope unresolvable and every real block report
        # NOTHING MEASURED — a probe defect that looks exactly like a checker
        # that measures nothing. (Second time this exact slip appeared.)
        src_repo = os.path.abspath(q)
        for _ in range(4):
            src_repo = os.path.dirname(src_repo)
        while src_repo != "/" and not os.path.isdir(
                os.path.join(src_repo, ".git")):
            src_repo = os.path.dirname(src_repo)
        d = os.path.join(ROOT, "work", "blocks", "active", MARK + "-x")
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d, exist_ok=True)
        shutil.copy(q, os.path.join(d, "BLOCK.md"))
        r = subprocess.run([sys.executable, "bin/grade-block", MARK + "-x",
                            "--root", src_repo, "--json"],
                           cwd=ROOT, capture_output=True, text=True)
        try:
            j = json.loads(r.stdout)
            print("  %-30s type %-6s %-17s %d archivos medidos"
                  % (name[:30], j["type"], j["verdict"], j["measured_files"]))
            if j["reds"]:
                print("       reds: %s" % ", ".join(j["reds"]))
        except Exception:
            print("  %-30s ⛔ %s" % (name[:30],
                                    (r.stdout or r.stderr).strip().splitlines()[0][:60]))
        shutil.rmtree(d, ignore_errors=True)
        shown += 1
        # ⛔ No cap. Capping at four was the short-reach family: the blocks that
        # are alphabetically last are not the least interesting, and a
        # cross-run that stops early reports a partial measurement as a full one.
else:
    print("  ⬜ NOT_MEASURED · set MENTE_CROSSRUN_BLOCKS to a real blocks/ folder")

clean()
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
leftovers = glob.glob(os.path.join(ROOT, "**", MARK + "*"), recursive=True)
print("\n  leftovers: %s" % (leftovers or "none"))
sys.exit(0 if good == len(results) and not leftovers else 1)
