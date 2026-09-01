#!/usr/bin/env python3
"""probe-new-campaign — proves the scaffold opens a VALID campaign, and refuses the rest.

⭐ THE TEST THAT MATTERS: does the campaign it writes pass check-campaign
UNEDITED? ⛔ A scaffold that emits something the checker rejects has handed
somebody broken paperwork to organise work around — and a campaign is what
several blocks are organised BY, so the damage spreads.

⚠️ AND THE REFUSAL THAT DEFINES IT: a campaign with no blocks orders nothing —
it is a title. ⛔ Opened empty, it never gets its blocks added, because the
emptiness stops being visible the moment the file exists.

Runs against an ISOLATED, INSTALLED copy with real blocks: a campaign that names
blocks needs blocks to name, and testing against absent ones would only ever
exercise the refusal.
"""
import os, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                       # noqa: E402

results = []
WORK = tempfile.mkdtemp(prefix="mente-nc-")
TREE = os.path.join(WORK, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git", "cache"))
CAMPAIGNS = os.path.join(TREE, "work", "campaigns")
open(os.path.join(TREE, "mente.config.yml"), "w").write(
    'schema: v1\nowner:\n  name: "Zzprobe Owner"\n')


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


def run(tool, *args):
    return subprocess.run([sys.executable, os.path.join(TREE, "bin", tool)]
                          + list(args), cwd=TREE, capture_output=True,
                          text=True, timeout=60)


def checker():
    return subprocess.run([sys.executable,
                           os.path.join(TREE, "bin", "check-campaign")],
                          cwd=TREE, capture_output=True, text=True, timeout=60)


# Two real blocks, because a campaign exists to hold blocks together.
for b, t in (("zzprobe-ba", "docs"), ("zzprobe-bb", "code")):
    run("new-block", b, "--type", t, "--intent", "A fixture block.")

print("═══ SONDA · new-campaign ═══\n")

r = run("new-campaign", "zzprobe-camp", "--blocks", "zzprobe-ba,zzprobe-bb",
        "--mission", "A measurable outcome.")
case("① ⭐ it opens a campaign", r.returncode == 0, "exit=%d" % r.returncode)

path = os.path.join(CAMPAIGNS, "zzprobe-camp", "CAMPAIGN.md")
case("② ⭐ the file exists where the contract says", os.path.exists(path))

c = checker()
mine = [l for l in c.stdout.splitlines() if "zzprobe-camp" in l and "🔴" in l]
case("③ ⭐⭐ the campaign PASSES its contract UNEDITED", not mine,
     mine[0][:58] if mine else "")

body = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
case("④ ⭐ it carries the 3 opening sections",
     all("\n## %s" % s in body for s in ("Mission", "Authority", "Blocks")))

# ⚠️ Opening costs three on purpose: a campaign that cost ten would be replaced
# by an informal list, and then nothing measures it at all.
case("⑤ ⚠️ NO exige contexto, canal ni cierre al abrir",
     "## Shared context" not in body and "## Closing" not in body)

# ⭐ THE BLOCKS ARE REAL ROWS, not a placeholder somebody must remember to swap
case("⑥ ⭐ the named blocks are in the table",
     "`zzprobe-ba`" in body and "`zzprobe-bb`" in body)
case("⑦ ⛔ and the example row does NOT survive (it would be a block that does not exist)",
     "`block-id`" not in body)

case("⑧ ⭐ the given mission really lands", "A measurable outcome." in body)

# ── ⛔ WHAT IT MUST REFUSE ──────────────────────────────────────────────────
r = run("new-campaign", "zzprobe-empty")
case("⑨ 🔴 no blocks → refused · a campaign with no blocks is a title",
     r.returncode == 1 and "orders nothing" in r.stderr,
     "exit=%d" % r.returncode)
case("⑩ ⛔ and it wrote nothing",
     not os.path.exists(os.path.join(CAMPAIGNS, "zzprobe-empty")))

r = run("new-campaign", "zzprobe-ghost", "--blocks", "no-existe")
case("⑪ 🔴 a block that does NOT exist → refused",
     r.returncode == 1 and "do not exist" in r.stderr, "exit=%d" % r.returncode)

r = run("new-campaign", "zzprobe-camp", "--blocks", "zzprobe-ba")
case("⑫ 🔴 an id already used → refused (resolution is exact)",
     r.returncode == 1 and "already used" in r.stderr)

r = run("new-campaign", "Zzprobe-Caps", "--blocks", "zzprobe-ba")
case("⑬ ⛔ an id that cannot be a folder → refused", r.returncode == 1)

# ── ⭐ THE SHAPE LIVES IN A TEMPLATE ────────────────────────────────────────
tpl = os.path.join(TREE, "templates", "CAMPAIGN.md.template")
case("⑭ ⭐ the shape lives in templates/, not inside the script",
     os.path.exists(tpl))
os.rename(tpl, tpl + ".hidden")
r = run("new-campaign", "zzprobe-notpl", "--blocks", "zzprobe-ba")
case("⑮ ⛔ no template → it fails and says so, it does not improvise a shape",
     r.returncode == 2 and "CAMPAIGN.md.template" in r.stderr,
     "exit=%d" % r.returncode)
os.rename(tpl + ".hidden", tpl)

# ── ⛔ no owner, no campaign ────────────────────────────────────────────────
os.remove(os.path.join(TREE, "mente.config.yml"))
r = run("new-campaign", "zzprobe-noowner", "--blocks", "zzprobe-ba")
case("⑯ ⛔ no declared owner → refused", r.returncode == 2
     and "bin/init" in r.stderr, "exit=%d" % r.returncode)

# ── ⭐ THE SHARED SCAFFOLD ANSWERS BOTH TOOLS THE SAME WAY ──────────────────
# ⛔ Two copies of "is this id usable" is two places to fix a refusal, and the
# day they disagree one tool accepts what the other rejects.
open(os.path.join(TREE, "mente.config.yml"), "w").write(
    'schema: v1\nowner:\n  name: "Zzprobe Owner"\n')
a = run("new-block", "Bad Name", "--type", "docs").returncode
b = run("new-campaign", "Bad Name", "--blocks", "zzprobe-ba").returncode
case("⑰ ⭐ both refuse the SAME invalid id, identically", a == b == 1,
     "block=%d campaign=%d" % (a, b))

shutil.rmtree(WORK, ignore_errors=True)
good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: %s" % ("none" if not os.path.exists(WORK) else "🔴 copia"))
sys.exit(0 if good == len(results) else 1)
