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
case("① 🔴 the battery REFUSES to run inside itself",
     r.returncode == 2 and "REFUSED" in r.stderr, "exit=%d" % r.returncode)
case("② ⭐ and it explains each turn copies the tree",
     "copies the tree" in r.stderr)

# ── ① THE NUMBERS COME FROM THE TREE ────────────────────────────────────────
run("generate-metrics")
m = read("METRICS.md")
real = len([n for n in os.listdir(os.path.join(TREE, "bin"))
            if n.startswith("check-")])
case("③ ⭐ `validators` counts the real check-*",
     ("`validators` | %d " % real) in m, "esperado %d" % real)

before = re.search(r"`rules` \| (\d+)", m).group(1)
open(os.path.join(TREE, "rules", "zzprobe-extra.md"), "w").write("# x\n")
run("generate-metrics")
after = re.search(r"`rules` \| (\d+)", read("METRICS.md")).group(1)
case("④ ⭐ the number CHANGES when the tree changes",
     int(after) == int(before) + 1, "%s → %s" % (before, after))
os.remove(os.path.join(TREE, "rules", "zzprobe-extra.md"))

# ⭐ the battery's result is READ, never taken — that is what makes it affordable
os.makedirs(os.path.join(TREE, "cache"), exist_ok=True)
open(os.path.join(TREE, "cache", "last-battery.txt"), "w").write(
    "➜ checks: 123 · failed: 4\n")
run("generate-metrics")
m = read("METRICS.md")
case("⑤ ⭐ it reads the battery's last result, it does not run it",
     "`battery.checks` | 123 " in m and "`battery.failed` | 4 " in m)

# ⬜ and with no recorded result it is a GAP, never a zero
os.remove(os.path.join(TREE, "cache", "last-battery.txt"))
run("generate-metrics")
case("⑥ ⬜ with no recorded result → NOT MEASURED, not a 0",
     "`battery.checks` | ⬜ NOT MEASURED" in read("METRICS.md"))

# ── ② THE OUTPUT OBEYS THE DOCUMENT CONTRACT ────────────────────────────────
run("generate-index")
r = run("check-document")
bad = [l for l in r.stdout.splitlines() if "🔴" in l
       and any(k in l for k in ("METRICS", "INDEX", "STATES", "DECISIONS"))]
case("⑦ ⛔ the 4 generated files PASS check-document", not bad,
     bad[0][:55] if bad else "")

case("⑧ ⭐ each carries the DO NOT EDIT BY HAND header",
     all("DO NOT EDIT BY HAND" in read(f)
         for f in ("METRICS.md", "INDEX.md", "STATES.md", "DECISIONS.md")))

# ⭐ none indexes ITSELF — a file that changes what the next run indexes never
# converges
# ⚠️ Measured in the TABLE, not in the whole file: the Related line legitimately
# points at its sibling generated files, and treating that as self-indexing
# would forbid a document from pointing anywhere.
_rows = [l for l in read("INDEX.md").splitlines() if l.startswith("| `docs/")]
case("⑨ ⭐ the index does NOT list itself among the documents",
     not any(g in l for l in _rows
             for g in ("INDEX.md", "METRICS.md", "STATES.md", "DECISIONS.md")),
     "%d fila(s) de docs/" % len(_rows))

# ⛔ nor does it index runtime state: a fresh copy legitimately lacks cache/,
# and an index insisting the file is there breaks its own pointers
case("⑩ ⛔ it does not index `cache/` — runtime state, not documentation",
     "cache/" not in read("INDEX.md"))

# ── ③ ⬜ A GAP IS A GAP, NEVER A ZERO ────────────────────────────────────────
shutil.rmtree(os.path.join(TREE, "work", "blocks"), ignore_errors=True)
run("generate-index")
case("⑪ ⬜ no blocks → it SAYS so, not an empty table",
     "NOT MEASURED" in read("STATES.md"))

keep = tempfile.mkdtemp()
shutil.move(os.path.join(TREE, "rules", "decisions"),
            os.path.join(keep, "decisions"))
run("generate-index")
case("⑫ ⬜ no decisions → it SAYS so, not a silent 0",
     "NOT MEASURED" in read("DECISIONS.md"))
shutil.move(os.path.join(keep, "decisions"),
            os.path.join(TREE, "rules", "decisions"))
shutil.rmtree(keep, ignore_errors=True)

# ⭐ an unreadable document still EXISTS — omitting it makes the index short
bad_f = os.path.join(TREE, "rules", "zzprobe-bad.md")
open(bad_f, "wb").write(b"\xff\xfe\x00")
run("generate-index")
case("⑬ ⭐ an unreadable document still appears (it does not shrink the index)",
     "zzprobe-bad.md" in read("INDEX.md"))
os.remove(bad_f)

# ── --check · is it current, without writing ────────────────────────────────
run("generate-index")
case("⑭ ⭐ --check says «current» without writing",
     run("generate-index", "--check").returncode == 0)

open(os.path.join(TREE, "rules", "zzprobe-new.md"), "w").write("# y\n")
case("⑮ 🔴 --check detects it went stale",
     run("generate-index", "--check").returncode == 1)
os.remove(os.path.join(TREE, "rules", "zzprobe-new.md"))

# ⚠️ AND THE DATE ALONE MUST NOT MAKE IT STALE — a check that fires every day
# without the tree changing is one nobody reads
run("generate-index")
q = os.path.join(DOCS, "INDEX.md")
t = open(q, encoding="utf-8").read()
open(q, "w", encoding="utf-8").write(
    re.sub(r"\*\*Updated:\*\* \d{4}-\d{2}-\d{2}", "**Updated:** 2020-01-01", t))
case("⑯ ⚠️ only a different DATE does not count as stale",
     run("generate-index", "--check").returncode == 0)

# ── ⛔ a generator that cannot write says so ────────────────────────────────
# ⚠️ The target file must be removed first: an existing file is rewritten
# through its own inode, so a read-only DIRECTORY does not stop it. ⛔ Testing
# the wrong barrier proves nothing about the one that matters.
os.remove(os.path.join(DOCS, "METRICS.md"))
os.chmod(DOCS, 0o500)
r = run("generate-metrics")
case("⑰ ⛔ with no write permission → it says so, it does not crash",
     r.returncode == 2 and "Traceback" not in r.stderr, "exit=%d" % r.returncode)
os.chmod(DOCS, 0o755)

# ── ⭐ E-21 · the engine measuring how much of itself it can check ──────────
# ⛔ Designing a lot and validating a little is the failure mode a governance
# engine is likeliest to commit, because writing a rule feels like solving the
# problem. ⚠️ A ratio only ever stated in prose is the symptom, so the ratio is
# GENERATED — and these cases prove it is read from the tree, not asserted.
run("generate-metrics")
m = read("METRICS.md")
_dec = re.search(r"`rules\.declared` \| (\d+)", m)
_loc = re.search(r"`rules\.locked` \| (\d+)", m)
_pct = re.search(r"`rules\.enforced_pct` \| ([\d.]+)%", m)
case("⑱ ⭐ it publishes declared / locked / the percentage",
     bool(_dec and _loc and _pct),
     "%s reglas · %s 🔒 · %s%%" % (_dec.group(1) if _dec else "—",
                                   _loc.group(1) if _loc else "—",
                                   _pct.group(1) if _pct else "—"))

# ⭐ THE HALF THAT MAKES IT A MEASUREMENT: it moves when the tree moves.
# ⛔ A ratio that stays put while rules are added is a constant wearing a
# measured face — which is the exact defect E-21 describes.
_qq = os.path.join(TREE, "rules", "zzprobe-rules.md")
open(_qq, "w", encoding="utf-8").write(
    "# zz\n\n| id | rule | level | why |\n|---|---|---|---|\n"
    "| `ZZQ-AAA-001` | one | 📖 | x |\n| `ZZQ-AAA-002` | two | 📖 | y |\n")
run("generate-metrics")
_m2 = read("METRICS.md")
_d2 = re.search(r"`rules\.declared` \| (\d+)", _m2)
_p2 = re.search(r"`rules\.enforced_pct` \| ([\d.]+)%", _m2)
case("⑲ ⭐ two 📖 rules added → declared rises, the percentage FALLS",
     bool(_d2 and _dec and int(_d2.group(1)) == int(_dec.group(1)) + 2
          and _p2 and _pct and float(_p2.group(1)) < float(_pct.group(1))),
     "%s→%s reglas · %s%%→%s%%" % (_dec.group(1) if _dec else "—",
                                   _d2.group(1) if _d2 else "—",
                                   _pct.group(1) if _pct else "—",
                                   _p2.group(1) if _p2 else "—"))
os.remove(_qq)

# ⭐ E-49 · THE RATIO SAYS WHAT IT DOES NOT COVER. ⛔ enforced_pct is computed
# over rows already in a rule table, so a contract declaring none contributes to
# neither half — ⚠️ doctrine can grow without enforcement and the percentage
# cannot fall, which is the drift it exists to detect.
_before = re.search(r"`rules\.unenforceable_docs` \| (\d+)", read("METRICS.md"))
_q = os.path.join(TREE, "rules", "zzprobe-doctrine.md")
open(_q, "w", encoding="utf-8").write(
    "# zz\n\n**Status:** current · **Type:** contract · **Updated:** 2026-01-15"
    " · **Owner:** x\n\n## Purpose\n\nProse with no rule table at all.\n\n"
    "Related: `README.md`.\n")
run("generate-metrics")
_after = re.search(r"`rules\.unenforceable_docs` \| (\d+)", read("METRICS.md"))
case("㉑ ⭐ a contract with no rule table raises `unenforceable_docs`",
     bool(_before and _after
          and int(_after.group(1)) == int(_before.group(1)) + 1),
     "%s → %s" % (_before.group(1) if _before else "—",
                  _after.group(1) if _after else "—"))
os.remove(_q)

# ⭐ DECISIONS are counted, not FILES. ⛔ count_files counted the folder's own
# README as a decision — 26 where 25 exist — and a number inflated by a readme
# is a number nobody can reconcile with the tree. ⚠️ The count also hid the
# useful half: how many decisions are still waiting to be built.
_d = re.search(r"`decisions` \| (\d+)", read("METRICS.md"))
_p = re.search(r"`decisions\.pending` \| (\d+)", read("METRICS.md"))
_real = len([f for f in os.listdir(os.path.join(TREE, "rules", "decisions"))
             if f.startswith("ADR-") and f.endswith(".md")])
case("㉒ ⭐ `decisions` counts ADRs, not the folder's README",
     bool(_d) and int(_d.group(1)) == _real, "%s = %d ADR(s)"
     % (_d.group(1) if _d else "—", _real))
case("㉓ ⬜ and `decisions.pending` says how many are unbuilt",
     bool(_p), _p.group(1) + " pending" if _p else "—")

# ⬜ and with no backlog to read it is a GAP, never a 0 — the same rule the
# battery result obeys: an absent row and a zero look identical in a table.
_bk = os.path.join(DOCS, "ENGINE-BACKLOG.md")
_keep = open(_bk, encoding="utf-8").read() if os.path.exists(_bk) else None
if _keep is not None:
    os.remove(_bk)
run("generate-metrics")
case("⑳ ⬜ no backlog file → NOT MEASURED, not a 0",
     "`backlog.closed` | ⬜ NOT MEASURED" in read("METRICS.md"))
if _keep is not None:
    open(_bk, "w", encoding="utf-8").write(_keep)

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
