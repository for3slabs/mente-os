#!/usr/bin/env python3
"""probe-conjunction — proves a gate and the validator it CALLS still agree.

🔴 THIS EXISTS BECAUSE OF A GATE THAT NEVER FIRED. `gate-critical` ran
`check-block --quiet` and looked for a block's name in that run's output — which
is empty by contract. ⛔ The condition could never be true, so every insufficient
close went straight through, and EVERY PROBE WAS GREEN.

⭐ A probe proves a PIECE works. It cannot prove two pieces still agree — that is
a different question, and nothing was asking it. Five gates call a validator;
this exercises each pair against a real installation.

⚠️ THE FAILURE SHAPE IT GUARDS: one side changes its contract — a flag stops
printing, an exit code shifts, a message is reworded — and the other keeps
reading what used to be there. ⛔ Both pass their own probe, and the pair is
dead.

Runs against an ISOLATED, INSTALLED tree with real work in it: a gate that only
ever sees fixtures is a gate that has never met the validator it depends on.
"""
import json, os, shutil, subprocess, sys, tempfile
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.abspath(__file__))
while _d != _os.path.dirname(_d):
    if _os.path.exists(_os.path.join(_d, "bin", "utf8.py")):
        _sys.path.insert(0, _os.path.join(_d, "bin")); break
    _d = _os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
import plat                                          # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-conj-")
REPO = os.path.join(WORK, "repo")
TREE = os.path.join(REPO, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git", "cache"))
subprocess.run(["git", "init", "-q"], cwd=REPO, capture_output=True)


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def tool(name, *args, **kw):
    return subprocess.run([sys.executable, os.path.join(TREE, "bin", name)]
                          + list(args), cwd=TREE, capture_output=True,
                          text=True, timeout=90, **kw)


def gate(name, payload):
    return subprocess.run([sys.executable, os.path.join(TREE, "hooks", name)],
                          cwd=TREE, input=json.dumps(payload),
                          capture_output=True, text=True, timeout=90)


# ⭐ A REAL INSTALLATION, not a fixture tree: the whole point is that the gate
# meets the validator over work that actually exists.
tool("init", "--owner", "Zzprobe Owner")
tool("new-block", "zzconj", "--type", "docs", "--intent", "A real block.")
BLOCK = os.path.join(TREE, "work", "blocks", "active", "zzconj", "BLOCK.md")

# ⭐ THE SCOPE IS WRITTEN, because BLK-SCP-001 requires it filled and only the
# author can write it. ⚠️ A fixture left on its ⬜ placeholders fails a rule this
# probe is not testing, and every gate case after it reads as broken.
_b = open(BLOCK, encoding="utf-8").read()
open(BLOCK, "w", encoding="utf-8").write(
    _b.replace("- ⬜ declare what this block may touch",
               "- `docs/thing.md` — the file this block writes.")
      .replace("- ⬜ declare a limit · DERIVED: replace this with a real one "
               "and its source",
               "- `bin/` — owned elsewhere, see `work/blocks/README.md`."))

print("═══ PROBE · gate ↔ validator, in conjunction ═══\n")

# ── ⭐ THE PAIR THAT WAS BROKEN ─────────────────────────────────────────────
# gate-critical asks check-block whether a block may close.
body = open(BLOCK, encoding="utf-8").read()
r = gate("gate-critical.py", {"tool_name": "Write",
                              "tool_input": {"file_path": BLOCK,
                                             "content": body + "\nstatus: closed\n"}})
case("① ⭐ a block that PASSES its contract may close", r.returncode == 0,
     "exit=%d" % r.returncode)

# 🔴 The same close, over a block the validator rejects. This is the case that
# was silently returning 0 for days.
open(BLOCK, "w", encoding="utf-8").write(body.replace("type: docs",
                                                      "type: invented"))
bad = open(BLOCK, encoding="utf-8").read() + "\nstatus: closed\n"
r = gate("gate-critical.py", {"tool_name": "Write",
                              "tool_input": {"file_path": BLOCK, "content": bad}})
case("② 🔴 a block the VALIDATOR rejects cannot close", r.returncode == 2,
     "exit=%d" % r.returncode)
case("③ ⭐ and the refusal names the block the validator named",
     "zzconj" in r.stderr)
open(BLOCK, "w", encoding="utf-8").write(body)

# ── ⭐ gate-handoff ↔ check-handoff ─────────────────────────────────────────
r = gate("gate-handoff.py", {"tool_name": "Agent",
                             "tool_input": {"subagent_type": "writer",
                                            "description": "x"}})
case("④ 🔴 no manifest → the gate refuses", r.returncode == 2,
     "exit=%d" % r.returncode)

# ⭐ and with one the validator ACCEPTS, the gate lets it through — which only
# holds if both read the manifest the same way.
hd = os.path.join(TREE, "work", "blocks", "active", "zzconj", "handoffs")
os.makedirs(hd, exist_ok=True)
tpl = open(os.path.join(TREE, "templates", "handoff.yml.template"),
           encoding="utf-8").read()
man = (tpl.replace('handoff_id: ""', 'handoff_id: "zz-1"')
          .replace('block: ""', 'block: "zzconj"')
          .replace('block_path: ""', 'block_path: "work/blocks/active/zzconj"')
          .replace('objective: ""', 'objective: "audit the fixture"')
          .replace('success_condition: ""',
                   'success_condition: "every file listed with its size"')
          .replace('stop_condition: ""',
                   'stop_condition: "after the listed files, or on any error"')
          .replace('path: ""', 'path: "handoffs/return.md"'))
open(os.path.join(hd, "zz-1.yml"), "w", encoding="utf-8").write(man)
accepted = tool("check-handoff", "--quiet").returncode == 0
r = gate("gate-handoff.py", {"tool_name": "Agent",
                             "tool_input": {"subagent_type": "writer",
                                            "description": "x"}})
case("⑤ ⭐ gate and validator agree on the SAME manifest",
     (r.returncode == 0) == accepted,
     "validator=%s gate=%s" % (accepted, r.returncode == 0))

# ── ⭐ gate-accounts ↔ check-accounts ───────────────────────────────────────
reg = os.path.join(TREE, "accounts.tsv")
open(reg, "a", encoding="utf-8").write(
    "an-org/dead\tan-account\tarchivado\told\t-\tretired\t-\n")
clean = tool("check-accounts", "--quiet").returncode == 0
r = gate("gate-accounts.py", {"tool_input": {"command": "git push old an-org/dead"}})
denied = '"deny"' in r.stdout
case("⑥ 🔴 a RETIRED repo the validator accepts is still refused by the gate",
     clean and denied, "validator clean=%s · gate deny=%s" % (clean, denied))

# ⚠️ THE DISTINCTION THAT MATTERS: the validator says the ROW is well-formed,
# the gate says the PUSH is refused. ⛔ Two different questions about one fact,
# and a reader who conflates them concludes the registry is broken.
case("⑦ ⚠️ they answer DIFFERENT questions about the same row",
     clean and denied)

# ── ⭐ pre-push ↔ check-accounts · layer 2 reads the same registry ──────────
r = subprocess.run(["bash", os.path.join(TREE, "hooks", "pre-push.sh"),
                    "old", "https://host/an-org/dead.git"], cwd=TREE,
                   capture_output=True, text=True, timeout=60,
                   env=dict(os.environ, MENTE_ACCOUNTS=reg))
case("⑧ ⭐ layer 2 refuses the same repo layer 1 denied", r.returncode == 1,
     "exit=%d" % r.returncode)

# ── ⭐ EVERY GATE LEAVES ITS BEAT, AND check-gates SEES IT ──────────────────
# ⛔ The pair that makes a dead gate visible: gates stamp, and one validator
# reads the stamps. If either side drifts, a gate can die unnoticed.
gate("gate-secrets.py", {"tool_name": "Write",
                         "tool_input": {"file_path": "x.md", "content": "hi"}})
# ⚠️ check-gates NAMES a gate only when it has gone quiet, so its silence is
# the pass. ⛔ Asserting the names appear had it backwards — the evidence is the
# STAMP each gate left, which is what the validator reads.
beats = os.path.join(TREE, ".beats")
left = sorted(os.listdir(beats)) if os.path.isdir(beats) else []
missing = [g for g in ("gate-critical", "gate-handoff", "gate-accounts",
                       "gate-secrets") if g not in left]
case("⑨ ⭐ every gate exercised above left its beat", not missing,
     "no beat: %s" % (missing or "none"))

r = tool("check-gates")
case("⑩ ⭐ and check-gates reports none of them as silent",
     r.returncode == 0 and "GATE SILENT" not in r.stdout,
     "exit=%d" % r.returncode)

plat.rmtree(WORK)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copy"))
sys.exit(0 if good == len(results) else 1)
