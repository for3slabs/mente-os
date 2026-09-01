#!/usr/bin/env python3
"""probe-generators — proves what is generated is measured, obeys the contract, and can say NOTHING.

⭐ A GENERATED FILE IS BELIEVED MORE THAN A WRITTEN ONE. It looks measured, so
nobody re-checks it — ⛔ which makes a wrong number here worse than a wrong
number anywhere else.

🔴 AND THIS PROBE'S OWN HISTORY IS THE WARNING. Its first version called
`generate-metrics`, which learned the battery's result by RUNNING the battery —
which runs this probe. Ten probes copy the whole tree first, so every turn of
the loop spawned a full suite AND a full copy: 655 processes, load average 609,
2,800 abandoned directories. ⚠️ It presented as a probe timing out, the most
ordinary failure there is.

⛔ SO THIS FILE NEVER INVOKES THE BATTERY, directly or through anything that
might. The battery now refuses to run inside itself (MENTE_BATTERY_RUNNING), and
the metric reads the last recorded result instead of taking one.

⚠️ Runs against an ISOLATED COPY: these scripts WRITE.
"""
import os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-gen-")
TREE = os.path.join(WORK, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git", "cache"))
DOCS = os.path.join(TREE, "docs")


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def run(script, *args):
    # ⛔ The guard is carried explicitly: if anything under here ever reaches for
    # the battery, it is REFUSED rather than allowed to recurse.
    return subprocess.run([sys.executable, os.path.join(TREE, "bin", script)]
                          + list(args), cwd=TREE, capture_output=True, text=True,
                          timeout=60,
                          env=dict(os.environ, MENTE_BATTERY_RUNNING="1"))


def read(name):
    try:
        return open(os.path.join(DOCS, name), encoding="utf-8").read()
    except OSError:
        return ""


print("═══ SONDA · generate-index + generate-metrics ═══\n")

# ── 🔴 THE GUARD THAT EXISTS BECAUSE OF THIS PROBE ──────────────────────────
r = subprocess.run([sys.executable, os.path.join(TREE, "bin", "probes",
                                                 "run-all.py")],
                   cwd=TREE, capture_output=True, text=True, timeout=60,
                   env=dict(os.environ, MENTE_BATTERY_RUNNING="1"))
case("① 🔴 la batería se NIEGA a correr dentro de sí misma",
     r.returncode == 2 and "REFUSED" in r.stderr, "exit=%d" % r.returncode)
case("② ⭐ y explica que cada vuelta copia el árbol",
     "copies the tree" in r.stderr)

# ── ① THE NUMBERS COME FROM THE TREE ────────────────────────────────────────
run("generate-metrics")
m = read("METRICS.md")
real = len([n for n in os.listdir(os.path.join(TREE, "bin"))
            if n.startswith("check-")])
case("③ ⭐ `validators` cuenta los check-* reales",
     ("`validators` | %d " % real) in m, "esperado %d" % real)

before = re.search(r"`rules` \| (\d+)", m).group(1)
open(os.path.join(TREE, "rules", "zzprobe-extra.md"), "w").write("# x\n")
run("generate-metrics")
after = re.search(r"`rules` \| (\d+)", read("METRICS.md")).group(1)
case("④ ⭐ el número CAMBIA cuando el árbol cambia",
     int(after) == int(before) + 1, "%s → %s" % (before, after))
os.remove(os.path.join(TREE, "rules", "zzprobe-extra.md"))

# ⭐ the battery's result is READ, never taken — that is what makes it affordable
os.makedirs(os.path.join(TREE, "cache"), exist_ok=True)
open(os.path.join(TREE, "cache", "last-battery.txt"), "w").write(
    "➜ checks: 123 · failed: 4\n")
run("generate-metrics")
m = read("METRICS.md")
case("⑤ ⭐ lee el último resultado de la batería, no la ejecuta",
     "`battery.checks` | 123 " in m and "`battery.failed` | 4 " in m)

# ⬜ and with no recorded result it is a GAP, never a zero
os.remove(os.path.join(TREE, "cache", "last-battery.txt"))
run("generate-metrics")
case("⑥ ⬜ sin resultado registrado → NOT MEASURED, no un 0",
     "`battery.checks` | ⬜ NOT MEASURED" in read("METRICS.md"))

# ── ② THE OUTPUT OBEYS THE DOCUMENT CONTRACT ────────────────────────────────
run("generate-index")
r = run("check-document")
bad = [l for l in r.stdout.splitlines() if "🔴" in l
       and any(k in l for k in ("METRICS", "INDEX", "STATES", "DECISIONS"))]
case("⑦ ⛔ los 4 archivos generados PASAN check-document", not bad,
     bad[0][:55] if bad else "")

case("⑧ ⭐ cada uno lleva la cabecera de NO EDITAR A MANO",
     all("DO NOT EDIT BY HAND" in read(f)
         for f in ("METRICS.md", "INDEX.md", "STATES.md", "DECISIONS.md")))

# ⭐ none indexes ITSELF — a file that changes what the next run indexes never
# converges
# ⚠️ Measured in the TABLE, not in the whole file: the Related line legitimately
# points at its sibling generated files, and treating that as self-indexing
# would forbid a document from pointing anywhere.
_rows = [l for l in read("INDEX.md").splitlines() if l.startswith("| `docs/")]
case("⑨ ⭐ el índice NO se lista a sí mismo entre los documentos",
     not any(g in l for l in _rows
             for g in ("INDEX.md", "METRICS.md", "STATES.md", "DECISIONS.md")),
     "%d fila(s) de docs/" % len(_rows))

# ⛔ nor does it index runtime state: a fresh copy legitimately lacks cache/,
# and an index insisting the file is there breaks its own pointers
case("⑩ ⛔ no indexa `cache/` — estado de ejecución, no documentación",
     "cache/" not in read("INDEX.md"))

# ── ③ ⬜ A GAP IS A GAP, NEVER A ZERO ────────────────────────────────────────
shutil.rmtree(os.path.join(TREE, "work", "blocks"), ignore_errors=True)
run("generate-index")
case("⑪ ⬜ sin bloques → lo DICE, no una tabla vacía",
     "NOT MEASURED" in read("STATES.md"))

keep = tempfile.mkdtemp()
shutil.move(os.path.join(TREE, "rules", "decisions"),
            os.path.join(keep, "decisions"))
run("generate-index")
case("⑫ ⬜ sin decisiones → lo DICE, no un 0 silencioso",
     "NOT MEASURED" in read("DECISIONS.md"))
shutil.move(os.path.join(keep, "decisions"),
            os.path.join(TREE, "rules", "decisions"))
shutil.rmtree(keep, ignore_errors=True)

# ⭐ an unreadable document still EXISTS — omitting it makes the index short
bad_f = os.path.join(TREE, "rules", "zzprobe-bad.md")
open(bad_f, "wb").write(b"\xff\xfe\x00")
run("generate-index")
case("⑬ ⭐ un documento ilegible aparece igual (no encoge el índice)",
     "zzprobe-bad.md" in read("INDEX.md"))
os.remove(bad_f)

# ── --check · is it current, without writing ────────────────────────────────
run("generate-index")
case("⑭ ⭐ --check dice «al día» sin escribir",
     run("generate-index", "--check").returncode == 0)

open(os.path.join(TREE, "rules", "zzprobe-new.md"), "w").write("# y\n")
case("⑮ 🔴 --check detecta que quedó viejo",
     run("generate-index", "--check").returncode == 1)
os.remove(os.path.join(TREE, "rules", "zzprobe-new.md"))

# ⚠️ AND THE DATE ALONE MUST NOT MAKE IT STALE — a check that fires every day
# without the tree changing is one nobody reads
run("generate-index")
q = os.path.join(DOCS, "INDEX.md")
t = open(q, encoding="utf-8").read()
open(q, "w", encoding="utf-8").write(
    re.sub(r"\*\*Updated:\*\* \d{4}-\d{2}-\d{2}", "**Updated:** 2020-01-01", t))
case("⑯ ⚠️ solo la FECHA distinta no cuenta como viejo",
     run("generate-index", "--check").returncode == 0)

# ── ⛔ a generator that cannot write says so ────────────────────────────────
# ⚠️ The target file must be removed first: an existing file is rewritten
# through its own inode, so a read-only DIRECTORY does not stop it. ⛔ Testing
# the wrong barrier proves nothing about the one that matters.
os.remove(os.path.join(DOCS, "METRICS.md"))
os.chmod(DOCS, 0o500)
r = run("generate-metrics")
case("⑰ ⛔ sin permiso de escritura → lo dice, no revienta",
     r.returncode == 2 and "Traceback" not in r.stderr, "exit=%d" % r.returncode)
os.chmod(DOCS, 0o755)

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
