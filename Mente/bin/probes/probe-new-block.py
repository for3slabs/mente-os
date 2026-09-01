#!/usr/bin/env python3
"""probe-new-block — proves the scaffold opens a VALID block, and refuses the rest.

⭐ THE TEST THAT MATTERS IS NOT "did it write a file". It is: does the block it
writes pass its own contract UNEDITED? ⛔ A scaffold that emits something the
checker rejects is worse than no scaffold — the person starts work believing the
paperwork is done, and learns otherwise against work already under way.

⚠️ AND OPENING MUST STAY CHEAP. The contract says it outright: if opening cost
ten fields, the work would happen WITHOUT a block, and then nothing is recorded.
So the cases below also measure what it does NOT demand.

Runs against an ISOLATED, INSTALLED copy: a scaffold needs a declared owner, and
an uninstalled tree has none — measured, not assumed.
"""
import os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-nb-")
TREE = os.path.join(WORK, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git", "cache"))
BLOCKS = os.path.join(TREE, "work", "blocks")
INDEX = os.path.join(BLOCKS, "README.md")
# ⚠️ A scaffold refuses without a declared owner, so the copy is INSTALLED
# first — the fixture must be the state the tool actually runs in.
open(os.path.join(TREE, "mente.config.yml"), "w").write(
    'schema: v1\nowner:\n  name: "Zzprobe Owner"\n')


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def run(*args):
    return subprocess.run([sys.executable, os.path.join(TREE, "bin", "new-block")]
                          + list(args), cwd=TREE, capture_output=True,
                          text=True, timeout=60)


def checker():
    return subprocess.run([sys.executable, os.path.join(TREE, "bin", "check-block")],
                          cwd=TREE, capture_output=True, text=True, timeout=60)


def drop(bid):
    shutil.rmtree(os.path.join(BLOCKS, "active", bid), ignore_errors=True)
    t = open(INDEX, encoding="utf-8").read()
    open(INDEX, "w", encoding="utf-8").write(
        "\n".join(l for l in t.splitlines()
                  if not l.startswith("- `%s`" % bid)) + "\n")


print("═══ SONDA · new-block ═══\n")

# ── ⭐ THE ONE THAT DECIDES WHETHER THIS TOOL IS REAL ───────────────────────
r = run("zzprobe-one", "--type", "docs", "--intent", "A one-sentence intent.")
case("① ⭐ abre un bloque", r.returncode == 0, "exit=%d" % r.returncode)

path = os.path.join(BLOCKS, "active", "zzprobe-one", "BLOCK.md")
case("② ⭐ el archivo existe donde el contrato dice", os.path.exists(path))

c = checker()
mine = [l for l in c.stdout.splitlines() if "zzprobe-one" in l and "🔴" in l]
case("③ ⭐⭐ el bloque PASA su propio contrato SIN editarlo", not mine,
     mine[0][:60] if mine else "")

# ── 🔴 BLK-OPN-002 · THE HALF A SCAFFOLD USUALLY SKIPS ──────────────────────
# A block on disk that no index names is one nothing knows exists: never picked
# up, never closed, never missed.
case("④ 🔴 queda LISTADO en el índice, no solo en disco",
     "zzprobe-one" in open(INDEX, encoding="utf-8").read())

# ── ⭐ THE FOUR OPENING SECTIONS, AND ONLY THOSE ────────────────────────────
body = open(path, encoding="utf-8").read()
have = re.findall(r"^## ([A-K]) ·", body, re.M)
case("⑤ ⭐ escribe exactamente §A-D, en orden", have == ["A", "B", "C", "D"],
     " ".join(have))

# ⚠️ Opening deliberately costs four sections. E-K are added while working —
# demanding them here is what makes people skip the block entirely.
# ⚠️ Measured on the HEADINGS, not on the text: the template names E-K in a
# closing comment so the writer knows what comes next, and a substring search
# read that explanation as sections being present.
case("⑥ ⚠️ NO exige E-K al abrir · abrir tiene que salir barato",
     not [h for h in have if h > "D"], " ".join(have))

# ⭐ §B ships with both halves, and the OUT line carries a source: an unsourced
# limit is an opinion, and the checker rejects it.
case("⑦ ⭐ §B trae IN y OUT, y el OUT trae su fuente",
     "✅ IN" in body and "⛔ OUT" in body and "DERIVED:" in body)

# ── ⭐ THE SHAPE COMES FROM A TEMPLATE, NOT FROM THIS SCRIPT ────────────────
# ⛔ A shape hardcoded in the scaffolder is a second definition of the contract,
# and two definitions drift without anything noticing.
tpl = os.path.join(TREE, "templates", "BLOCK.md.template")
case("⑧ ⭐ la forma vive en templates/, no dentro del script",
     os.path.exists(tpl))
os.rename(tpl, tpl + ".hidden")
r = run("zzprobe-notpl", "--type", "docs")
case("⑨ ⛔ sin plantilla → falla y lo dice, no improvisa una forma",
     r.returncode == 2 and "BLOCK.md.template" in r.stderr,
     "exit=%d" % r.returncode)
os.rename(tpl + ".hidden", tpl)

# ── ⛔ WHAT IT MUST REFUSE · each one produces a block that LOOKS valid ─────
r = run("zzprobe-one", "--type", "docs")
case("⑩ 🔴 un id ya usado → rechaza (la resolución es exacta)",
     r.returncode == 1 and "already used" in r.stderr, "exit=%d" % r.returncode)

r = run("Zzprobe-Caps", "--type", "docs")
case("⑪ ⛔ un id que no sirve de carpeta → rechaza", r.returncode == 1)

r = run("zzprobe-two", "--type", "inventado")
case("⑫ 🔴 un tipo NO declarado → rechaza",
     r.returncode == 1 and "not declared" in r.stderr)

r = run("zzprobe-two", "--type", "docs", "--lane", "veloz")
case("⑬ 🔴 un carril NO declarado → rechaza", r.returncode == 1,
     "exit=%d" % r.returncode)

# ⭐ AND A HYPHENATED LANE IS VALID — the regex that reads the vocabulary once
# dropped `full-block`, leaving the lane list EMPTY, and an empty vocabulary
# accepted anything. ⛔ A silent skip wearing the shape of a pass.
r = run("zzprobe-lane", "--type", "code", "--lane", "full-block")
case("⑭ ⭐ un carril CON GUION es válido (el bug del vocabulario vacío)",
     r.returncode == 0, "exit=%d" % r.returncode)
drop("zzprobe-lane")

r = run("zzprobe-two")
case("⑮ ⛔ sin --type → rechaza, no elige uno", r.returncode == 1)

# ── ⭐ THE VOCABULARY IS READ FROM THE CONTRACT ─────────────────────────────
# ⛔ A copy inside this script would refuse a type the contract added, and the
# refusal would look like the type being wrong rather than the tool being stale.
contract = os.path.join(TREE, "rules", "contract-block.md")
keep = open(contract, encoding="utf-8").read()
open(contract, "w", encoding="utf-8").write(
    keep.replace("type: code | docs | infra | data",
                 "type: code | docs | infra | data | research"))
r = run("zzprobe-new-type", "--type", "research")
case("⑯ ⭐ un tipo AÑADIDO al contrato se acepta sin tocar el script",
     r.returncode == 0, "exit=%d" % r.returncode)
drop("zzprobe-new-type")

# ⛔ AND AN UNREADABLE CONTRACT MUST NOT BECOME A PERMISSIVE ONE
open(contract, "w", encoding="utf-8").write("# emptied\n")
r = run("zzprobe-nocontract", "--type", "docs")
case("⑰ ⛔ contrato ilegible → falla, NO acepta cualquier cosa",
     r.returncode == 2, "exit=%d" % r.returncode)
open(contract, "w", encoding="utf-8").write(keep)

# ── 🔴 TWO VALIDATORS MUST NOT DISAGREE ABOUT ONE FILE ─────────────────────
# A block declares its identity in §A, and contract-block measures every field
# of it. ⛔ check-document demanded the four-field document header ON TOP, so a
# freshly scaffolded block was simultaneously valid and invalid — found end to
# end, on creation, with nothing actually wrong with it.
_doc = subprocess.run([sys.executable, os.path.join(TREE, "bin", "check-document")],
                      cwd=TREE, capture_output=True, text=True, timeout=90)
case("⑱ 🔴 el bloque recién creado NO lo rechaza check-document",
     "zzprobe-one" not in _doc.stdout, "")

# ── 🔴 BLK-OPN-003 · the other direction, found while building this ────────
# Removing a block folder left its row in the index, and the tree reported
# clean: the index then sends every reader to work that is not there.
shutil.rmtree(os.path.join(BLOCKS, "active", "zzprobe-one"))
c = checker()
case("⑲ 🔴 una entrada de índice SIN bloque → detectada",
     "BLK-OPN-003" in c.stdout and "zzprobe-one" in c.stdout)

drop("zzprobe-one")
c = checker()
case("⑳ ⭐ y al quitar la entrada, calla", "BLK-OPN-003" not in c.stdout)

# ── ⛔ no owner, no block ───────────────────────────────────────────────────
os.remove(os.path.join(TREE, "mente.config.yml"))
r = run("zzprobe-noowner", "--type", "docs")
case("㉑ ⛔ sin dueño declarado → rechaza · un bloque sin dueño no responde nadie",
     r.returncode == 2 and "bin/init" in r.stderr, "exit=%d" % r.returncode)

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d de %d correctos" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  restos: %s" % ("ninguno" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
