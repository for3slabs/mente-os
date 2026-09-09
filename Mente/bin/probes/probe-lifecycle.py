#!/usr/bin/env python3
"""probe-lifecycle — one block from open to close, with EVERY rule live at once.

🔴 THIS EXISTS BECAUSE PASSING SEPARATELY IS NOT PASSING TOGETHER. Eight rules
were added across one stretch of work, each with its own probe, each green. ⛔
None of them asked what a person actually does: open a block, edit inside it,
edit outside it, write a checkpoint, record evidence, close.

⭐ The failures this shape catches are the ones no single probe can see — a rule
that makes a legitimate step impossible, two rules demanding contradictory
things of one file, a gate refusing what its own validator accepts.

⚠️ Measured on its first run: a block written with a natural `OUT` line failed
`BLK-SCP-002`, and the checker was right twice over — the line cited a rule id
instead of a file, and it restated a system-wide limit that `BLK-SCP-003`
forbids repeating. ⭐ No single probe would have surfaced that, because no
single probe writes a block the way a person writes one.
"""
import json, os, re, shutil, subprocess, sys, tempfile
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
import plat                                          # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import rewrite, ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-life-")
REPO = os.path.join(WORK, "repo")
TREE = os.path.join(REPO, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git", "cache"))
subprocess.run(["git", "init", "-q"], cwd=REPO, capture_output=True)

BID = "zzlifecycle"
D = os.path.join(TREE, "work", "blocks", "active", BID)
B = os.path.join(D, "BLOCK.md")


def case(label, ok, detail=""):
    print("  %-56s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def tool(name, *args):
    return subprocess.run([sys.executable, os.path.join(TREE, "bin", name)]
                          + list(args), cwd=TREE, capture_output=True,
                          text=True, timeout=120)


def gate(name, payload):
    return subprocess.run([sys.executable, os.path.join(TREE, "hooks", name)],
                          cwd=TREE, input=json.dumps(payload),
                          capture_output=True, text=True, timeout=90)


def edit(path):
    return gate("pre-edit-standards.py",
                {"tool_input": {"file_path": os.path.join(TREE, path)}})


print("═══ CICLO DE VIDA · un bloque de principio a fin ═══\n")

# ── ① OPEN ─────────────────────────────────────────────────────────────────
tool("init", "--owner", "X")
# ⚠️ WIRED, NOT «SYMLINKED». 🔴 Measured on Windows: `os.symlink` needs a
# privilege a normal account lacks, so `bin/init` writes a launcher instead and
# the hook RUNS. Asking `islink` reported it dead — the mechanism measured, not
# the outcome.
def _wired(name):
    q = os.path.join(REPO, ".git", "hooks", name)
    if os.path.islink(q):
        return True
    return (os.path.isfile(q)
            and ("hooks/" + name + ".sh") in
            open(q, encoding="utf-8", errors="replace").read().replace("\\", "/"))


case("① init wires BOTH git hooks, not one",
     _wired("pre-commit") and _wired("pre-push"))

tool("new-block", BID, "--type", "code", "--intent", "A block.")
case("② new-block writes it", os.path.isdir(D))

# ⭐ A block as a PERSON writes it: a real IN, a real OUT with its source, and a
# standard narrowed to the files it judges.
s = open(B, encoding="utf-8").read()
s = s.replace("### ✅ IN",
              "### ✅ IN\n\n- `Mente/work/%s-src/` — this block's code." % BID, 1)
s = s.replace("### ⛔ OUT",
              "### ⛔ OUT\n\n- `Mente/bin/` — owned elsewhere, see "
              "`work/blocks/README.md`.", 1)
s = s.replace("- `rules/rule-working-in-a-block.md`",
              "- `rules/rule-working-in-a-block.md`\n"
              "- `rules/rule-shipping.md` — for: *.py", 1)
rewrite(B, s)
r = tool("check-block")
case("③ the block passes its own contract", r.returncode == 0,
     (r.stdout.strip().splitlines() or [""])[-1][:34])

# ── ② WORK ─────────────────────────────────────────────────────────────────
r = edit("work/%s-src/a.py" % BID)
case("④ editing .py names the *.py standard", "rule-shipping" in r.stderr
     and "📦" in r.stderr)
r = edit("work/%s-src/a.md" % BID)
case("⑤ editing .md does NOT name it", "rule-shipping" not in r.stderr
     and "📦" in r.stderr)
r = edit("docs/INDEX.md")
case("⑥ editing outside every scope is reported, never blocked",
     "BLK-SCP-004" in r.stderr and r.returncode == 0)

CHK = ("\n## I · Checkpoints\n\n- **2026-01-15 · iteration 1**\n"
       "  changed: the reader\n  did not change: the gate\n  pieces: bin/x\n"
       "  standard: rules/rule-shipping.md\n  verified: the battery, all green\n"
       "  unexpected: none\n  remains: none\n  scope: held\n")
rewrite(B, open(B, encoding="utf-8").read() + CHK)
case("⑦ a complete checkpoint passes", tool("check-block").returncode == 0)

whole = open(B, encoding="utf-8").read()
rewrite(B, 
    whole.replace("  did not change: the gate\n", ""))
case("⑧ and one missing `did not change` is refused",
     "BLK-CHK-001" in tool("check-block").stdout)
rewrite(B, whole)

# ── ③ EVIDENCE ─────────────────────────────────────────────────────────────
ROW = ("## F · Sub-blocks\n\n| # | task | piece | dependents | acceptance | "
       "evidence | status |\n|---|---|---|---|---|---|---|\n"
       "| 1 | write it | bin/x | 0 | it runs | %s | closed |\n\n")
whole = open(B, encoding="utf-8").read().replace(
    "## I · Checkpoints", ROW % "done" + "## I · Checkpoints", 1)
rewrite(B, whole)
case("⑨ evidence saying «done» is refused",
     "BLK-SUB-004" in tool("check-block").stdout)
rewrite(B, 
    whole.replace("| it runs | done |", "| it runs | ran it · 2026-01-15 |"))
case("⑩ and the same row WITH its date passes",
     tool("check-block").returncode == 0)

# ── ④ CLOSE ────────────────────────────────────────────────────────────────
whole = re.sub(r"^status: .*$", "status: closed",
               open(B, encoding="utf-8").read(), flags=re.M)
whole += ("\n## K · Closing\n\nclosed: 2026-01-15\ncompleted: the work\n"
          "not completed: nothing remains\nlearned: a lesson\n"
          "evidence: the battery, all green · 2026-01-15\n"
          # ⭐ BLK-CLS-008 · the lane this block declares needs its level named.
          "evidence level: L3\n"
          "acceptance: criteria met\nsufficiency: pass\n")
rewrite(B, whole)
case("⑪ closing with no close.json is refused",
     "BLK-CLS-007" in tool("check-block").stdout)

g = tool("grade-block", BID, "--json")
open(os.path.join(D, "close.json"), "w", encoding="utf-8").write(g.stdout)
r = tool("check-block")
case("⑫ with the record grade-block produces, it closes", r.returncode == 0,
     (r.stdout.strip().splitlines() or [""])[-1][:34])

try:
    rec = json.loads(g.stdout)
except Exception:                                              # noqa: BLE001
    rec = {}
case("⑬ and the record names all six dimensions",
     len(rec.get("dimensions", {})) == 6,
     "%d dimension(s)" % len(rec.get("dimensions", {})))

# ⭐ QLT-LAY-003 · the one who MEASURES does not sign the close.
open(os.path.join(D, "close.json"), "w", encoding="utf-8").write(
    json.dumps({"verdict": "PRODUCT",
                "dimensions": {"naming": "undeclared"}}))
case("⑮ a record whose verdict is not keyed to its layer is refused",
     "QLT-LAY-003" in tool("check-block").stdout)
open(os.path.join(D, "close.json"), "w", encoding="utf-8").write(g.stdout)

# ⭐ THE PAIR: the gate must not refuse what its own validator accepts.
r = gate("gate-critical.py",
         {"tool_name": "Write",
          "tool_input": {"file_path": B, "content": whole}})
case("⑭ the gate lets through a close the validator accepts",
     r.returncode == 0, "exit=%d" % r.returncode)

# ── ⭐ THE OTHER PRODUCER↔CONSUMER PAIR: the battery and the metric ─────────
# 🔴 Measured 2026-09-02 by auditing in conjunction: rename the field the
# battery WRITES into cache/last-battery.txt and the battery stays green at
# 695 · 0 while the metric turns ⬜ NOT MEASURED. ⛔ Two pieces stopped agreeing
# and every probe passed — the same shape as E-48, in a different pair.
# ⭐ It degrades honestly (⬜, never a made-up number), and that is exactly why
# nothing noticed: an honest gap is invisible until somebody asks for the value.
# ⚠️ THE LINE COMES FROM THE PRODUCER, never hand-written here. ⛔ The first
# version wrote the file itself in the correct format and passed while the
# agreement was broken — it was testing the consumer, not the pair. ⭐ The
# producer's own source is what has to be read.
_ra = open(os.path.join(TREE, "bin", "probes", "run-all.py"),
           encoding="utf-8").read()
_fmt = re.search(r'_line = \("([^"]+)"', _ra)
_rep = os.path.join(TREE, "cache", "last-battery.txt")
os.makedirs(os.path.dirname(_rep), exist_ok=True)
# ⚠️ FILLED BY COUNTING THE PRODUCER'S OWN PLACEHOLDERS. 🔴 Measured
# 2026-09-08: the battery's line gained a fourth field (the ⬜ count) and this
# crashed with "not enough arguments for format string" — the probe was right
# to notice a change and wrong to assume a shape. ⛔ Hardcoding the arity makes
# every future field a false alarm, and a probe that cries wolf gets edited to
# stop rather than read.
_shape = _fmt.group(1) if _fmt else "  ➜ checks: %d · failed: %d%s"
_args, _n = [], 0
for _spec in re.findall(r"%[-0-9.]*([a-z])", _shape):
    _args.append({"d": (42, 7)[min(_n, 1)], "s": ""}.get(_spec, ""))
    if _spec == "d":
        _n += 1
open(_rep, "w", encoding="utf-8").write((_shape % tuple(_args)) + "\n")
tool("generate-metrics")
try:
    _m = open(os.path.join(TREE, "docs", "METRICS.md"), encoding="utf-8").read()
except OSError:
    _m = ""
case("⑯ ⭐ the metric READS what the battery wrote",
     "`battery.checks` | 42 " in _m and "`battery.failed` | 7 " in _m,
     "42/7 round-tripped")

# ⛔ And the shape is the contract: a renamed field must not read as a value.
open(_rep, "w", encoding="utf-8").write("  ➜ total: 42 · failed: 7\n")  # noqa
tool("generate-metrics")
try:
    _m2 = open(os.path.join(TREE, "docs", "METRICS.md"), encoding="utf-8").read()
except OSError:
    _m2 = ""
case("⑰ ⛔ a renamed field degrades to ⬜, never to a wrong number",
     "`battery.checks` | ⬜ NOT MEASURED" in _m2,
     "the gap is said, not guessed")

# ── ⑱ 🔴 A COUNT OF FAILURES THAT NAMES NONE OF THEM ──────────────────────
# 🔴 THE FAILURE, measured 2026-09-08 on a real installation. The battery ended
# `failed: 6` and named not one of the six; learning what broke meant re-running
# four probes by hand and reading their tails — repeating the work the battery
# had just done. ⛔ CHK-IND-002: a count with no detail is a number nobody can
# act on. Here it cost the diagnosis, not merely the reading.
# ⚠️ AND A GREEN CASE MAY CARRY 🔴 IN ITS NAME — many do, `🔴 ⭐ the switch RUNS
# the gate` among them. ⛔ A first version matched every line beginning with the
# emoji and reported five PASSING cases as failures. Only the summary AFTER a
# probe's `➜ N of M correct` line names real ones.
_pd = os.path.join(WORK, "probes-named")
os.makedirs(_pd, exist_ok=True)
_stub = ('import sys\n'
         'print("  🔴 a green case whose NAME carries the emoji  \u2705 ok")\n'
         # ⚠️ ONE SPACE before the tick, not two — this is the shape that
         # broke the namer twice: the column split leaves the whole line in
         # the label, so every column test misreads a PASSING case as red.
         'print("  🔴 refuses \u00b7 a connection string \u2705 exit=2")\n'
         'print("\\n  \u279c {good} of 2 correct")\n'
         '{tail}\n'
         'print("  leftovers: none")\n'
         'sys.exit({rc})\n')
# ⚠️ AND A PROBE THAT PRINTS NO SUMMARY AT ALL. 🔴 Measured 2026-09-08: the
# first namer read only the `🔴 <label>` lines a probe writes under its tally —
# and 15 of 37 probes write no such summary, `probe-plat` among them. ⛔ The
# battery reported `failed: 1` and named nothing, which is the defect the namer
# exists to remove, shipped as fixed while covering under half the tree.
for _nm, _g, _tail, _rc in (("probe-zzfail", 1, 'print("     🔴 the case that fell")', 1),
                            ("probe-zzquiet", 1, 'pass', 1),
                            ("probe-zzpass", 2, 'pass', 0)):
    open(os.path.join(_pd, _nm + ".py"), "w", encoding="utf-8", newline="").write(
        _stub.format(good=_g, tail=_tail, rc=_rc))

# ⭐ THE REAL CONSUMER IS RUN, never a copy of its logic. 🔴 The first version
# re-implemented the parse here and asserted the source contained the fix as a
# STRING — so gutting `run-all`'s collector left this case green. ⛔ That is the
# defect ⑯ already names one pair over: a probe that reads the producer's text
# instead of exercising it is testing its own arithmetic.
# ⚠️ IT RUNS IN A TREE OF ITS OWN, holding two stubs and nothing else. ⛔ The
# second version planted them in the real `probes/` folder and fired the battery
# there: correct, and it never finished — a full battery copies the tree once
# per probe, and this probe runs INSIDE a battery. `run-all` finds its probes
# beside itself and walks UP for `bin/utf8.py`, so a two-file tree is enough.
# ⚠️ `MENTE_BATTERY_RUNNING` is cleared: the battery refuses to be its own
# descendant.
_mini = os.path.join(_pd, "mini", "bin")
os.makedirs(os.path.join(_mini, "probes"), exist_ok=True)
for _mod in ("utf8.py", "plat.py"):
    shutil.copy(os.path.join(TREE, "bin", _mod), os.path.join(_mini, _mod))
for _nm in ("probe-zzfail", "probe-zzquiet", "probe-zzpass"):
    shutil.copy(os.path.join(_pd, _nm + ".py"),
                os.path.join(_mini, "probes", _nm + ".py"))
shutil.copy(os.path.join(TREE, "bin", "probes", "run-all.py"),
            os.path.join(_mini, "probes", "run-all.py"))
_env = dict(os.environ)
_env.pop("MENTE_BATTERY_RUNNING", None)
_rr = subprocess.run([sys.executable,
                      os.path.join(_mini, "probes", "run-all.py")],
                     capture_output=True, text=True, encoding="utf-8", env=_env)
_named = [l.strip() for l in _rr.stdout.splitlines() if "🔴 probe-zz" in l]
case("⑱ 🔴 ⭐ the battery NAMES every failure, and only real ones",
     len(_named) == 2
     and any("probe-zzfail" in x and "the case that fell" in x for x in _named)
     and any("probe-zzquiet" in x and "prints no per-case detail" in x
             for x in _named),
     "2 named, 0 false positives" if len(_named) == 2 else _named)

plat.rmtree(WORK)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copy"))
sys.exit(0 if good == len(results) else 1)
