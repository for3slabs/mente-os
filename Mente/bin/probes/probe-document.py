#!/usr/bin/env python3
"""probe-document — does check-document detect what contract-document.md claims?"""
import os, sys, re, glob, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Probe, ROOT, MARK

D = os.path.join(ROOT, "docs")
REF = os.environ.get("MENTE_CROSSRUN_DOCS", "")
p = Probe("check-document", "DOC")

GOOD = """# A probe fixture

**Status:** current · **Type:** rule · **Updated:** 2026-01-15 · **Owner:** someone

## Purpose

A fixture used to prove the checker detects what it claims to.

## 1 · Content

Nothing of consequence.

Related: `README.md`.
"""


def put(text, name=MARK + "-fixture.md"):
    q = p.track(os.path.join(D, name))
    open(q, "w", encoding="utf-8").write(text)
    return q


print("═══ A · SABOTAGE · check-document ═══\n")
p.baseline()

p.case("① an incomplete header",
       lambda: put(GOOD.replace(" · **Owner:** someone", "")), "DOC-HDR-001")
p.case("② an invalid Status",
       lambda: put(GOOD.replace("**Status:** current", "**Status:** alive")), "DOC-HDR-002")
p.case("③ a Type that does not exist",
       lambda: put(GOOD.replace("**Type:** rule", "**Type:** invented")), "DOC-HDR-003")
p.case("④ a non-ISO date",
       lambda: put(GOOD.replace("2026-01-15", "15 Jan 2026")), "DOC-HDR-004")
p.case("⑤ superseded with no replacement",
       lambda: put(GOOD.replace("**Status:** current", "**Status:** superseded")),
       "DOC-HDR-005")
# ⭐ The fixture must exceed the ceiling the CONTRACT declares, read from the
# contract — a hardcoded size silently stops testing anything the day the
# ceiling is raised, and the probe then reports the check as broken.
def _ceiling(kind="rule"):
    import re as _re
    t = open(os.path.join(ROOT, "rules", "contract-document.md"), encoding="utf-8").read()
    m = _re.search(r"^\|\s*`%s`\s*\|\s*\*{0,2}(?:⭐\s*)?\*{0,2}(\d+)" % kind, t, _re.M)
    return int(m.group(1)) if m else 250


p.case("⑥ over the ceiling",
       lambda: put(GOOD.replace("Nothing of consequence.",
                                "\n".join("line %d" % i
                                          for i in range(_ceiling() + 50)))),
       "DOC-SIZ-001")
p.case("⑦ no Purpose",
       lambda: put(GOOD.replace("## Purpose", "## Something else")), "DOC-BOD-001")
p.case("⑧ -bis numbering",
       lambda: put(GOOD.replace("## 1 · Content", "## 1-bis · Content")), "DOC-BOD-002")
p.case("⑨ a live number in prose",
       lambda: put(GOOD.replace("Nothing of consequence.",
                                "The suite runs 42 checks today.")), "DOC-CNT-002")
p.case("⑩ a pointer that does not resolve",
       lambda: put(GOOD.replace("Nothing of consequence.",
                                "See `rules/ghost.md` for detail.")), "DOC-CNT-004")
p.case("⑪ generated without saying so in the body",
       lambda: put(GOOD.replace("**Owner:** someone",
                                "**Owner:** someone · **Authority:** generated")),
       "DOC-AUT-002")
p.case("⑫ a name carrying a version", lambda: put(GOOD, MARK + "-thing-v2.md"), "DOC-NAM-004")
p.case("⑬ a name with an underscore", lambda: put(GOOD, MARK + "-a_b.md"), "DOC-NAM-001")
p.case("⑭ a date in the name",
       lambda: put(GOOD, MARK + "-2026-01-15-thing.md"), "DOC-NAM-003")

# ⭐ DOC-SIZ-001 now checks that the SPLIT was named, not just that the ceiling
# was crossed. Both directions matter: an over-ceiling file with no recorded
# work is a finding; the same file WITH the work recorded is not.
# ⛔ 300 lines does NOT cross a `rule` ceiling of 700 — the first version of
# this case planted the defect where no ceiling was, and read the working check
# as broken. The count must exceed the ceiling of the fixture's OWN type.
p.case("⑭b SIZ · over the ceiling and nobody named the split",
       lambda: put(GOOD.replace("Nothing of consequence.",
                                "\n".join("line %d" % i for i in range(750)))),
       "DOC-SIZ-001")

# ⭐ DOC-IDS-001 · an id is an address. Measured: a real contract carried one
# twice after a rule was added beside an existing one.
p.case("⑭c IDS · the same id in two rows",
       lambda: put(GOOD.replace("Nothing of consequence.",
                                "| `ABC-XYZ-001` | first | 🔒 | x |\n"
                                "| `ABC-XYZ-001` | second | 🔒 | y |")),
       "DOC-IDS-001")
p.inverse("⑭d IDS · two different ids do not fire",
          lambda: put(GOOD.replace("Nothing of consequence.",
                                   "| `ABC-XYZ-001` | first | 🔒 | x |\n"
                                   "| `ABC-XYZ-002` | second | 🔒 | y |")))

p.case("⑮ a credential pasted into the body",
       lambda: put(GOOD.replace("Nothing of consequence.",
                                'Run it with `--token=abc123def456ghi789`.')),
       "DOC-CNT-005")
p.case("⑯ the filename names a person",
       lambda: put(GOOD.replace("**Owner:** someone", "**Owner:** alexandra"),
                   MARK + "-alexandra-notes.md"), "DOC-NAM-007")

# ⭐ DOC-LIF-001 · the threshold is DECLARED, so the probe declares it too:
# with none declared nothing is measured, and the probe must prove BOTH — that
# it fires when a threshold exists, and that it stays silent when none does.
_contract = os.path.join(ROOT, "rules", "contract-document.md")
_orig = open(_contract, encoding="utf-8").read()
try:
    p.inverse("⑰ with no declared threshold, NOTHING is measured (old date)",
              lambda: put(GOOD))
    open(_contract, "w", encoding="utf-8").write(
        _orig.replace("| ⬜ staleness threshold | 0 days |",
                      "| ⬜ staleness threshold | 30 days |"))
    p.case("⑱ `current` with an old date, threshold declared",
           lambda: put(GOOD), "DOC-LIF-001")
finally:
    open(_contract, "w", encoding="utf-8").write(_orig)
    p.clean()

p.inverse("⑲ a CORRECT document", lambda: put(GOOD))
p.crash_guard()

print("\n═══ B · CROSS-RUN · documentos reales de otra instancia ═══\n")
p.clean()
real = sorted(glob.glob(os.path.join(REF, "*.md")))[:10] if REF else []
for i, q in enumerate(real):
    shutil.copy(q, p.track(os.path.join(D, "%s-x%02d-%s" % (MARK, i, os.path.basename(q)))))
if not real:
    print("  ⑳ ⬜ NOT_MEASURED · set MENTE_CROSSRUN_DOCS to a tree of real documents")
code, out, err = p.run()
mine = p._mine(out) if real else []
by = {}
for l in mine:
    for m in re.findall(r"DOC-[A-Z]+-\d+", l):
        by[m] = by.get(m, 0) + 1
print("  ⑳ %d documentos reales · %d hallazgos" % (len(real), len(mine)))
for k in sorted(by):
    print("       %-14s %d" % (k, by[k]))

# 🔴 A ROW MAY NAME SEVERAL TYPES, and both must get the ceiling. The contract
# writes `analysis` · `case` on one row; the reader required exactly one name
# per cell, so BOTH ended up with no ceiling — a type declared in the contract
# that no document could legally carry, reported as "Type not in the table"
# while sitting right there in it.
p.case("㉗ 🔴 a type sharing its row still has a ceiling",
       lambda: put(GOOD.replace("**Type:** rule", "**Type:** analysis")
                       + "\n" + "filler line\n" * 320),
       "DOC-SIZ-001")

# ── DOC-CNT-004 · ⭐ check-links MERGED HERE, not built beside it ───────────
# ⛔ A second validator reading the same documents for the same kind of defect
# would be a copy that drifts. What was missing was not a piece — it was REACH:
# the matcher only saw paths with a known extension, so every `bin/check-x`
# reference went unchecked. Measured: 170 of those in this tree, 24 resolving to
# nothing, including QUICKSTART.md — the first file a newcomer reads — naming
# six commands of which one existed.
p.case("㉒ a pointer with NO extension that does not resolve",
       lambda: put(GOOD + "\nRun `bin/check-zznothing` to verify.\n"),
       "DOC-CNT-004")

# ⭐ and the same pointer marked ⬜ is correct — planned, not broken
p.inverse("㉓ the same pointer marked ⬜ is NOT reported",
          lambda: put(GOOD + "\nRun \u2b1c `bin/check-zznothing` later.\n"))

# ⭐ A CONTRAST REFERENCE names where something ELSE belongs — "that is
# `docs/plans/`". ⛔ It is a destination an installation may create, not a claim
# that a file is there, and reporting it would push writers to stop drawing the
# line at all.
p.inverse("㉔ ⭐ «that is `docs/zzelsewhere/`» is a contrast, not a broken pointer",
          lambda: put(GOOD + "\nA plan does not go here — that is "
                             "`docs/zzelsewhere/`.\n"))

# ⛔ THE `break` THAT HID THE REST · one broken pointer per file was reported and
# the others stayed invisible until the first was fixed — a fix that reveals
# more work instead of finishing it.
put(GOOD + "\n`bin/check-zzone` and `bin/check-zztwo` and `bin/check-zzthree`.\n")
_c, _o, _e = p.run()
_n = len([l for l in _o.splitlines() if "DOC-CNT-004" in l and MARK in l])
print("  %-46s %s %d de 3 punteros rotos vistos"
      % ("㉕ ⛔ TRES punteros rotos → se ven los TRES", "✅" if _n == 3 else "🔴", _n))
p.results.append(("㉕ tres punteros rotos", "FAIL" if _n == 3 else "NOT_DETECTED"))
p.clean()

# 🔴 THE DEFECT A CLEAN CLONE FOUND, INVISIBLE IN THE WORKING TREE ──────────
# A GENERATED file has no template — a generator writes it — and it is
# gitignored, so every clone lacks it. The instance-file exemption was derived
# from templates/ alone, so citing `docs/METRICS.md` read as a broken pointer in
# every clone and in no working tree. ⛔ check-structure already derived the same
# exemption from BOTH sources; two pieces answering one question differently is
# how one of them ends up wrong.
p.inverse("㉖ 🔴 citing a GENERATED file (gitignored) is not a broken pointer",
          lambda: put(GOOD + "\nNumbers live in `docs/METRICS.md`.\n"))

# ── DOC-CAP-001/002 · the map and the tree must agree, BOTH ways ────────────
# ⭐ Run against an ISOLATED COPY: the subject is a fixed file at the root, and
# editing the real one would leave the working tree carrying a fixture.
# ⛔ The second direction is the one that gets forgotten — a piece that exists
# and is never named works fine, points at nothing, and gets rebuilt by somebody
# who could not find it. Reading the map cannot reveal what the map left out.
import shutil as _sh, subprocess as _sp, tempfile as _tf, os as _os

_W = _tf.mkdtemp(prefix="mente-cap-")
_T = _os.path.join(_W, "Mente")
_sh.copytree(ROOT, _T, ignore=_sh.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git"))
_CAP = _os.path.join(_T, "CAPABILITIES.md")


def _run_cap():
    return _sp.run([sys.executable, _os.path.join(_T, "bin", "check-document")],
                   cwd=_T, capture_output=True, text=True).stdout


def _cap(label, ok, detail=""):
    print("  %-52s %s %s" % (label, "✅" if ok else "🔴", detail))
    p.results.append((label, "FAIL" if ok else "NOT_DETECTED"))


_base = open(_CAP, encoding="utf-8").read()
_cap("㉑ the real map agrees with the tree", "DOC-CAP" not in _run_cap())

# 🔴 a row naming a piece that does not exist, and NOT marked as planned
open(_CAP, "w", encoding="utf-8").write(
    _base + "\n| `bin/check-zzprobe` | a command that is not there |\n")
_cap("㉒ 🔴 nombra una pieza inexistente sin ⬜ → detectado",
     "DOC-CAP-001" in _run_cap())

# ⭐ and the SAME row marked ⬜ is correct: the map may describe what is planned,
# as long as the reader can tell that from what exists today
open(_CAP, "w", encoding="utf-8").write(
    _base + "\n⬜ | `bin/check-zzprobe` | planned, not built |\n")
_cap("㉓ ⭐ la misma fila marcada ⬜ es correcta",
     "DOC-CAP-001" not in _run_cap())

# ⛔ the other direction · a real, executable piece the map never names
open(_CAP, "w", encoding="utf-8").write(_base)
_extra = _os.path.join(_T, "bin", "check-zzunnamed")
open(_extra, "w").write("#!/usr/bin/env python3\n")
_os.chmod(_extra, 0o755)
_cap("㉔ ⛔ una pieza REAL que el mapa no nombra → detectado",
     "DOC-CAP-002" in _run_cap())

# ⚠️ but a shared helper is not a capability: demanding it be listed would turn
# the map into a file listing, and a map that lists everything guides nobody
_os.remove(_extra)
_helper = _os.path.join(_T, "hooks", "_zzhelper.py")
open(_helper, "w").write("# shared\n")
_os.chmod(_helper, 0o755)
_cap("㉕ ⚠️ un helper `_` NO se exige en el mapa",
     "DOC-CAP-002" not in _run_cap())
_os.remove(_helper)

# ⬜ no map at all → NOT MEASURED, never a silent pass
_os.remove(_CAP)
_cap("㉖ ⬜ sin CAPABILITIES.md → lo dice, no calla",
     "NOT MEASURED" in _run_cap())

_sh.rmtree(_W, ignore_errors=True)

sys.exit(0 if p.report() else 1)
