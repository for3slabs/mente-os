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

## WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| the rules | the engine maintainer |
| ⛔ an exemption | **nobody** |

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
    print("  ⬜ NOT_MEASURED · set MENTE_CROSSRUN_DOCS to a tree of real documents")
code, out, err = p.run()
mine = p._mine(out) if real else []
by = {}
for l in mine:
    for m in re.findall(r"DOC-[A-Z]+-\d+", l):
        by[m] = by.get(m, 0) + 1
print("  %d documentos reales · %d hallazgos" % (len(real), len(mine)))
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

# ── DOC-CNT-007 · ⭐ RESOLVING IS NOT ENOUGH ────────────────────────────────
# ⛔ A pointer to a superseded document is worse than a broken one: the broken
# one announces itself, while this one resolves, opens, and reads as authority.
# ⚠️ Measured before building: this template holds ZERO superseded or fossil
# documents and a reference installation holds three — so the fixture must
# PLANT the target, and a probe that waited to find one would pass forever
# while measuring nothing.
def _target(status, extra="", name="zztarget"):
    """Plant a target document, return the fixture that points AT it."""
    put(("# %s\n\n**Status:** %s · **Type:** plan · **Updated:** 2026-01-15"
         " · **Owner:** someone\n%s\n## Purpose\n\nA planted target.\n\n"
         "Related: `README.md`.\n") % (name, status, extra),
        "%s-%s.md" % (MARK, name))
    return put(GOOD + "\nThe detail is in `docs/%s-%s.md`.\n" % (MARK, name))

p.case("㉘ ⭐ a pointer to a SUPERSEDED document",
       lambda: _target("superseded",
                       "**Superseded by:** `docs/%s-fixture.md`\n" % MARK),
       "DOC-CNT-007")

p.case("㉙ ⭐ a pointer to a FOSSIL · DOC-LIF-003 leaves 📖",
       lambda: _target("fossil", name="zzfossil"), "DOC-CNT-007")

# ⭐ THE HALF THAT MATTERS AS MUCH: a target still in force is NOT reported.
# ⛔ A check that fires on every pointer measures nothing and gets ignored.
p.inverse("㉚ ⛔ a pointer to a CURRENT document is NOT reported",
          lambda: _target("current", name="zzcurrent"))

# ⚠️ Only `.md` carries a status header. A checker that guessed at a .tsv would
# report prose as a defect.
p.inverse("㉛ ⛔ a pointer to a NON-.md file is out of scope, not assumed fine",
          lambda: put(GOOD + "\nThe pieces are in `pieces.tsv`.\n"))

# ⭐ A FENCED COMMAND IS A STRONGER POINTER THAN AN INLINE ONE — it does not
# name a piece, it tells the reader what to RUN. ⛔ Measured: four citations of
# two commands deliberately never built, in README.md, QUICKSTART.md and
# CAPABILITIES.md — the first three files a newcomer opens.
p.case("㉜ ⛔ a command in a ```bash block that does not exist",
       lambda: put(GOOD + "\n```bash\nbin/check-zzfenced\n```\n"),
       "DOC-CNT-004")

# ⚠️ The language tag is not a filter: restricting to bash meant a ```yaml block
# did not match its own opening, so its CLOSE paired with the next block's OPEN
# and the fences fell out of step — half a file read inside-out.
p.case("㉝ ⚠️ a yaml block before it does not knock the fences out of step",
       lambda: put(GOOD + "\n```yaml\nkey: value\n```\n\n"
                          "```bash\nbin/check-zzafteryaml\n```\n"),
       "DOC-CNT-004")

# ⛔ A `python` block is SOURCE, not an instruction: a bin/x inside a docstring
# is an example of what to write. Reporting it pushes writers to stop showing
# the shape at all.
p.inverse("㉞ ⛔ the same name inside a ```python block is an example",
          lambda: put(GOOD + '\n```python\n"""check-zzexample — a template."""\n```\n'))

# ── DOC-BOD-003 · a file that grants authority declares who governs it ─────
# ⚠️ An authority that writes its own acceptance criteria is circular:
# "acceptable" converges on "whatever it already does", and nothing inside the
# file can reveal it — it reads as coherent because it agrees with itself.
# ⭐ The fixture is a VALID rule, so it carries its governance; these cases
# REMOVE it. ⛔ Making the fixture typeless instead would have hidden the rule
# behind a type it never applies to.
_NOGOV = re.compile(r"## WHO GOVERNS THIS FILE.*?\n\n(?=Related:)", re.S)

p.case("㊳ ⛔ a `contract` with no governance section",
       lambda: put(_NOGOV.sub("", GOOD.replace("**Type:** rule",
                                               "**Type:** contract"))),
       "DOC-BOD-003")

p.case("㊴ ⛔ a `rule` with no governance section",
       lambda: put(_NOGOV.sub("", GOOD)), "DOC-BOD-003")

p.inverse("㊵ ⭐ the fixture as written, WITH its governance",
          lambda: put(GOOD))

# ⛔ Only contract and rule. A plan grants no authority, and demanding a
# governance section everywhere would make the marker meaningless.
p.inverse("㊶ ⛔ a `plan` grants no authority → not demanded",
          lambda: put(GOOD.replace("**Type:** rule", "**Type:** plan")))

# ── DOC-BOD-004 · a layer split is declared from BOTH sides ────────────────
# ⛔ Declared once, a split survives exactly until someone reads the other
# document alone — and that reader has no way to know a half is missing.
def _one_sided():
    """A file declaring a split with one that does not declare it back."""
    put(GOOD, MARK + "-half.md")
    return put(GOOD.replace("Nothing of consequence.",
                            "⚖️ split-with: `%s-half.md`" % MARK))


p.case("㊷ ⛔ a split the other side never declares back",
       _one_sided, "DOC-BOD-004")


def _both_sides():
    put(GOOD.replace("Nothing of consequence.",
                     "⚖️ split-with: `%s-fixture.md`" % MARK), MARK + "-half.md")
    return put(GOOD.replace("Nothing of consequence.",
                            "⚖️ split-with: `%s-half.md`" % MARK))


p.inverse("㊸ ⭐ both sides declare it → no finding", _both_sides)

# ⛔ A CITATION IS NOT A DECLARATION: the first version looked for the file's
# name in the other document, and the pair passed after the marker was deleted
# because the two cite each other in prose anyway.
def _mention_only():
    put(GOOD.replace("Nothing of consequence.",
                     "See `%s-fixture.md` for the rest." % MARK),
        MARK + "-half.md")
    return put(GOOD.replace("Nothing of consequence.",
                            "⚖️ split-with: `%s-half.md`" % MARK))


p.case("㊹ ⛔ a mention in prose does not count as declaring it",
       _mention_only, "DOC-BOD-004")


# ── DOC-BOD-005 · a `case` answers the three entry questions (ADR-021) ─────
# ⛔ A filter nothing asks is a filter nobody applies: the next installation
# records errors by instinct and the collection reaches dozens in months.
# ⚠️ Measured where the filter DID run: one error admitted over months, cited
# by nineteen files. ⭐ Strict is the point.
_ANS = ("\n## The three questions\n\n"
        "1. Recurs **elsewhere**: yes — the same shape in two other readers.\n"
        "2. The cause was a wrong **criterion**, not a wrong line.\n"
        "3. **Actionable**: read the header, never the position.\n")

p.case("㊺ ⛔ a `case` that answers none of the three",
       lambda: put(GOOD.replace("**Type:** rule", "**Type:** case")),
       "DOC-BOD-005")

p.case("㊻ ⛔ a `case` answering only two of the three",
       lambda: put(GOOD.replace("**Type:** rule", "**Type:** case")
                       .replace("Nothing of consequence.",
                                "Recurs elsewhere, and it is actionable.")),
       "DOC-BOD-005")

p.inverse("㊼ ⭐ a `case` that answers all three",
          lambda: put(GOOD.replace("**Type:** rule", "**Type:** case")
                          .replace("Nothing of consequence.", _ANS)))

# ⛔ And the demand is on `case` alone: a rule is not a case.
p.inverse("㊽ ⛔ a `rule` is not asked the three questions",
          lambda: put(GOOD))

p.clean()

# ── DOC-SIZ-003 · a numeric ceiling states a unit this checker measures ─────
# ⛔ "Too long" is an opinion; a number with a unit is a measurement. ⚠️ The unit
# was written in the table and never verified: the reader took the digits and
# discarded the word beside them, so `250 words` would still have been measured
# in LINES — the table saying one thing, the check doing another.
#
# ⚠️ THE DEFECT LIVES IN THE CONTRACT, so this runs on a COPY of the tree. A
# probe must never write to the engine it is measuring (E-43: p.track deletes,
# and a contract was lost that way).
def _unit_case(edit):
    import shutil as _sh, subprocess as _sp, tempfile as _tf
    w = _tf.mkdtemp(prefix="mente-siz-")
    t = os.path.join(w, "Mente")
    _sh.copytree(ROOT, t, ignore=_sh.ignore_patterns(
        "__pycache__", ".beats", ".test-lock", ".git", "cache"))
    q = os.path.join(t, "rules", "contract-document.md")
    c = open(q, encoding="utf-8").read()
    open(q, "w", encoding="utf-8").write(edit(c))
    r = _sp.run([sys.executable, os.path.join(t, "bin", "check-document")],
                cwd=t, capture_output=True, text=True)
    _sh.rmtree(w, ignore_errors=True)
    return "DOC-SIZ-003" in r.stdout


for _lbl, _edit, _want in (
        ("㉟ ⭐ a ceiling in `words` · the unit is not the measured one",
         lambda c: c.replace("| **250 lines** | ⭐ move content out",
                             "| **250 words** | ⭐ move content out"), True),
        ("㊱ ⭐ a ceiling with NO unit at all",
         lambda c: c.replace("| **800 lines** |", "| **800** |"), True),
        ("㊲ ⛔ the table as written → no finding",
         lambda c: c, False)):
    _got = _unit_case(_edit)
    print("  %-46s %s %s" % (_lbl, "✅" if _got == _want else "🔴",
                             "detected" if _got else "does NOT fire (correct)"))
    p.results.append((_lbl, "FAIL" if _got == _want else "NOT_DETECTED"))

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

# ⭐ THIS SECTION NUMBERS ITSELF `C1..Cn`, and that is the fix for a real bug.
# ⛔ It used to continue the main series from ㉑ as if there were one series,
# while section A had already reached ㉛ — so five numerals addressed two cases
# each, and a failure reported as ㉕ had two possible homes. ⚠️ Cheap while the
# probe is green; it costs exactly at the moment the numeral is read.
# ⭐ A prefix per section means inserting a case in A can never collide again.
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
_cap("C1 the real map agrees with the tree", "DOC-CAP" not in _run_cap())

# 🔴 a row naming a piece that does not exist, and NOT marked as planned
open(_CAP, "w", encoding="utf-8").write(
    _base + "\n| `bin/check-zzprobe` | a command that is not there |\n")
_cap("C2 🔴 names a piece that does not exist, unmarked → detected",
     "DOC-CAP-001" in _run_cap())

# ⭐ and the SAME row marked ⬜ is correct: the map may describe what is planned,
# as long as the reader can tell that from what exists today
open(_CAP, "w", encoding="utf-8").write(
    _base + "\n⬜ | `bin/check-zzprobe` | planned, not built |\n")
_cap("C3 ⭐ the same row marked ⬜ is correct",
     "DOC-CAP-001" not in _run_cap())

# ⛔ the other direction · a real, executable piece the map never names
open(_CAP, "w", encoding="utf-8").write(_base)
_extra = _os.path.join(_T, "bin", "check-zzunnamed")
open(_extra, "w").write("#!/usr/bin/env python3\n")
_os.chmod(_extra, 0o755)
_cap("C4 ⛔ a REAL piece the map never names → detected",
     "DOC-CAP-002" in _run_cap())

# ⚠️ but a shared helper is not a capability: demanding it be listed would turn
# the map into a file listing, and a map that lists everything guides nobody
_os.remove(_extra)
_helper = _os.path.join(_T, "hooks", "_zzhelper.py")
open(_helper, "w").write("# shared\n")
_os.chmod(_helper, 0o755)
_cap("C5 ⚠️ a `_` helper is NOT demanded by the map",
     "DOC-CAP-002" not in _run_cap())
_os.remove(_helper)

# ⬜ no map at all → NOT MEASURED, never a silent pass
_os.remove(_CAP)
_cap("C6 ⬜ no CAPABILITIES.md → it says so, it does not stay quiet",
     "NOT MEASURED" in _run_cap())

_sh.rmtree(_W, ignore_errors=True)

sys.exit(0 if p.report() else 1)
