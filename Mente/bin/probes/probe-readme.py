#!/usr/bin/env python3
"""probe-readme — proves the front page answers the question instead of listing files.

🔴 THE FAILURE, measured twice on real runs. Somebody is handed the URL and asks
an assistant what this repository is. ⚠️ NOTHING IS CLONED — no hooks, no
CLAUDE.md, no settings. The only surface that exists is the README GitHub renders.
The one that shipped addressed the PERSON ("paste this to your assistant") and
then listed four other files, so the assistant read the menu aloud and the visitor
got a file listing instead of an explanation.

⭐ Two things must hold, and neither used to be checked:
  · the front page speaks TO THE ASSISTANT, first, unambiguously
  · it CARRIES the explanation — it does not point at it

⚠️ AND the copy must not drift. The same words live in START-HERE §1 and in the
README; the copy nobody edits is the one strangers read. CHK-SHR-001 — one shape,
one source — so the generator's own --check is a case here.

⬜ NOT MEASURED: whether an assistant obeys. That runs outside this engine.
"""
import os, re, shutil, subprocess, sys, tempfile
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d):
    if os.path.exists(os.path.join(_d, "bin", "utf8.py")):
        sys.path.insert(0, os.path.join(_d, "bin")); break
    _d = os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
import plat                                          # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                             # noqa: E402

results = []


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


print("═══ SONDA · README (the front page) ═══\n")

# ⚠️ THE PROBE BUILDS ITS OWN SCENE — it does not read the front page next to
# this tree. 🔴 Measured: run-all gives each probe a private copy of Mente/ with
# NO parent repository, so a probe that looked at `dirname(ROOT)/README.md` found
# nothing and reported 0/1 — a real failure caused by the harness, not the code.
# ⭐ Generating the page into a tree this probe owns measures the SAME thing in
# both contexts, and proves the generator works rather than assuming someone ran it.
WORK = tempfile.mkdtemp(prefix="probe-readme-")
REPO = os.path.join(WORK, "repo")
TREE = os.path.join(REPO, "Mente")
shutil.copytree(ROOT, TREE, ignore=shutil.ignore_patterns(
    "__pycache__", ".beats", ".test-lock", ".git", "cache"))
PATH = os.path.join(REPO, "README.md")
GEN = os.path.join(TREE, "bin", "generate-readme")

_g = subprocess.run([sys.executable, GEN], cwd=TREE, capture_output=True,
                    text=True, timeout=60)
case("① ⭐ the generator produces a front page from START-HERE §1",
     _g.returncode == 0 and os.path.isfile(PATH),
     (_g.stdout + _g.stderr).strip().split("\n")[0][:44])
if not os.path.isfile(PATH):
    plat.rmtree(WORK)
    print("\n  ➜ 0 of 1 correct")
    sys.exit(1)

text = open(PATH, encoding="utf-8").read()
low = text.lower()

# ── ② IT SPEAKS TO THE ASSISTANT ───────────────────────────────────────────
# 🔴 The shipped version said "paste this to your assistant" — an instruction to
# the PERSON. In the run that failed, the assistant arrived first and no line was
# addressed to it, so it improvised.
case("② 🔴 ⭐ it addresses the ASSISTANT, not only the person",
     bool(re.search(r"if you are an ai assistant reading this", low)))

# 🔴 THE CASE THAT WOULD HAVE CAUGHT THE REAL FAILURE. Measured 2026-09-05 on
# Windows: the assistant fetched the rendered PAGE, not the file — and an HTML
# comment does not survive GitHub's renderer, so the order never arrived.
# ⛔ The instruction must live in VISIBLE markdown, outside any comment.
_visible = re.sub(r"<!--.*?-->", "", text, flags=re.S).lower()
case("②b 🔴 ⭐ the order survives GitHub's renderer (NOT in an HTML comment)",
     "if you are an ai assistant reading this" in _visible)
case("②c ⭐ and it is near the top, before anything it might skim",
     _visible.find("if you are an ai assistant reading this") < 400)

# ⛔ AND IT FORBIDS THE DETOUR. The same run reported an unrelated finding on the
# person's machine, investigated it, and never installed anything.
case("②d 🔴 ⛔ it forbids reporting what it notices on their machine",
     bool(re.search(r"do not report[\s\S]{0,90}machine", _visible)))

# ── ③ IT CARRIES THE ANSWER ────────────────────────────────────────────────
# ⭐ An assistant that must open a second file may summarise instead. One that
# already holds the text prints it.
for needle, what in ((r"what it is:", "what it is"),
                     (r"the problem it solves", "the problem"),
                     (r"resume\.md", "the cold-start file, by name"),
                     (r"pending\.md", "the postponed file, by name"),
                     (r"close the session", "the habit the system rests on")):
    case("③· it CARRIES %s" % what, bool(re.search(needle, low)))

# ── ④ IT DOES NOT HAND THEM A MENU ─────────────────────────────────────────
# 🔴 THE MEASURED CAUSE. A menu invites choosing; the assistant chose to read the
# menu out. ⛔ These names must not appear on the front page at all.
menu = [n for n in ("QUICKSTART.md", "CAPABILITIES.md", "CHANGELOG.md",
                    "bin/init", "bin/probes/run-all.py") if n in text]
case("④ 🔴 ⭐ no file menu for the assistant to read out instead",
     not menu, ", ".join(menu) or "none")

# ── ⑤ THE CHOOSER IS ORDERED HERE TOO ──────────────────────────────────────
# ⚠️ With only a URL there is no START-HERE in context, so the chooser must be
# mandated on this page or it never happens.
case("⑤ ⭐ it mandates the chooser by name, on this page",
     "askuserquestion" in low)
# 🔴 Measured: plain `git clone <url>` made a `mente-os/` folder nobody asked for.
case("⑤c 🔴 ⭐ the clone command clones INTO the folder, no extra wrapper",
     bool(re.search(r"git clone \S+\.git \.", text)))
case("⑤b ⛔ three options, and it says to stop and wait",
     low.count("| option |") >= 1 and bool(re.search(r"stop there and wait", low)))

# ── ⑥ IT DOES NOT DRIFT FROM ITS SOURCE ────────────────────────────────────
# ⭐ CHK-SHR-001. The generator answers this better than any comparison written
# here would — and running it is what proves the generator itself still works.
case("⑥ the generator exists and is a command", os.path.isfile(GEN))
r = subprocess.run([sys.executable, GEN, "--check"], cwd=TREE,
                   capture_output=True, text=True, timeout=60)
case("⑥b 🔴 ⭐ the front page still MATCHES START-HERE §1 (no drift)",
     r.returncode == 0, (r.stdout + r.stderr).strip().split("\n")[0][:40])

# ⛔ AND --check MUST NOT WRITE. A checker that repairs what it measures always
# reports green and measures nothing.
before = open(PATH, encoding="utf-8").read()
subprocess.run([sys.executable, GEN, "--check"], cwd=TREE,
               capture_output=True, timeout=60)
case("⑥c ⛔ --check writes NOTHING (a checker that repairs measures nothing)",
     open(PATH, encoding="utf-8").read() == before)

# ── ⑦ THE PAGE THE WORLD ACTUALLY READS ────────────────────────────────────
# 🔴 THE GAP THIS CLOSES, found by sabotaging my own probe: every case above
# measures a page this probe GENERATED in its own tree, so hand-edits to the
# published README — the only file a stranger ever sees — went undetected.
# ⭐ A probe that only measures what it produced measures the producer, not the
# product. ⛔ Both are needed: the generator can be right while the shipped file
# has been edited by hand and never regenerated.
_generated = open(PATH, encoding="utf-8").read()
LIVE = os.path.join(os.path.dirname(ROOT), "README.md")
if os.path.isfile(LIVE):
    live = open(LIVE, encoding="utf-8").read()
    vis = re.sub(r"<!--.*?-->", "", live, flags=re.S).lower()
    case("⑦ 🔴 ⭐ the PUBLISHED page carries the order in visible markdown",
         "if you are an ai assistant reading this" in vis)
    case("⑦b 🔴 ⭐ and its clone command clones INTO the folder",
         bool(re.search(r"git clone \S+\.git \.", live)))
    case("⑦c ⛔ the published page is byte-for-byte what the generator makes",
         live == _generated)
else:
    # ⬜ CHK-CAU-003 · said out loud, never swallowed.
    print("  ⬜ the published README is not beside this tree · NOT MEASURED "
          "(expected under run-all's isolated copy)")

plat.rmtree(WORK)

print("\n  ⬜ NOT MEASURED · whether an assistant OBEYS this page · that runs "
      "outside\n     this engine · these cases prove the instruction is present "
      "and complete")

good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: none")
sys.exit(0 if good == len(results) else 1)
