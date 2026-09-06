#!/usr/bin/env python3
"""probe-readme — proves the front page earns trust instead of demanding it.

🔴 THE FAILURE THIS ENCODES, measured 2026-09-05 on a real run. The page used to
carry instructions to the reading assistant: print §1 verbatim, do not
summarise, and — worst — do not report what you notice on the user's machine.
⚠️ The assistant classified it as PROMPT INJECTION, refused to follow it, and
advised the person NOT to install this. ⛔ It was right: telling an agent to
withhold information from its own user is indefensible.

⭐ SO THE CASES BELOW ARE MOSTLY INVERSES. They measure that no such instruction
came back, and that the page carries what a stranger needs to decide on their
own: what it is, what it will do to their machine, and how to start. A page that
explains well does not need to give orders.

⚠️ AND the copy must not drift from START-HERE §1 — the same words in two files
diverge, and the copy nobody edits is the one strangers read (CHK-SHR-001).

⬜ NOT MEASURED: whether an assistant reaches a good summary. That runs outside
this engine.
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
# ── ② ⛔ NO ORDERS TO THE ASSISTANT — the inverse cases ────────────────────
# 🔴 Each phrase below appeared on the page that got classified as prompt
# injection. ⛔ None of them may come back, in a comment or in plain sight.
BANNED = [
    (r"print .{0,20}verbatim|print §?1 (below )?exactly", "print it verbatim"),
    (r"do not summaris|do not summariz", "do not summarise"),
    (r"do not propose (steps|next steps)", "do not propose steps"),
    (r"do not report anything you notice", "🔴 withhold what you notice"),
    (r"if you are an ai assistant reading", "an order addressed at the reader"),
]
# ⭐ One numeral per case: the battery refuses a label used twice, and it is
# right — a report where five rows share a name cannot be read.
for _i, (pat, what) in enumerate(BANNED, start=1):
    hit = re.search(pat, low)
    case("②.%d ⛔ no order to the assistant: %s" % (_i, what), not hit,
         "" if not hit else "🔴 " + hit.group(0)[:30])

# ⭐ THE ONE THAT MATTERS MOST, kept separate because it is not a style choice:
# a page telling an agent to hide something from its user is indefensible.
case("②z 🔴 ⭐ nothing tells the assistant to withhold from its user",
     not re.search(r"(do not|don't|never) (report|mention|tell)[\s\S]{0,60}"
                   r"(machine|notice|found)", low))

# ── ③ IT CARRIES THE ANSWER ────────────────────────────────────────────────
# ⭐ An assistant that must open a second file may summarise instead. One that
# already holds the text prints it.
for needle, what in ((r"what it is:", "what it is"),
                     (r"the problem it solves", "the problem"),
                     (r"resume\.md", "the cold-start file, by name"),
                     (r"pending\.md", "the postponed file, by name"),
                     (r"close the session", "the habit the system rests on")):
    case("③· it CARRIES %s" % what, bool(re.search(needle, low)))

# ── ④ IT CARRIES WHAT A STRANGER NEEDS TO DECIDE ──────────────────────────
# ⭐ The page no longer gives orders, so it has to EARN the decision instead.
# 🔴 A stranger who cannot tell what this will do to their machine should not
# install it — and the run that refused this repo named exactly that: git hooks
# that intercept commits, and a clone that lands in their own folder.
for pat, what in ((r"what it does to your machine", "what it does to their machine"),
                  (r"git hook", "that it installs git hooks"),
                  (r"sends nothing|no network calls", "that it sends nothing"),
                  (r"installs nothing|no packages", "that it installs nothing"),
                  (r"remove them by deleting", "how to remove what it installed")):
    case("④· it states %s" % what, bool(re.search(pat, low)))

# ── ⑤ AND HOW TO START ─────────────────────────────────────────────────────
# ⚠️ The trailing dot is not cosmetic: plain `git clone <url>` makes a folder
# nobody asked for. ⭐ But it must land in a folder they CREATE for it — cloning
# into a project folder is what read as invasive on a real run.
case("⑤ ⭐ the clone command clones INTO the folder, no extra wrapper",
     bool(re.search(r"git clone \S+\.git \.", text)))
case("⑤b 🔴 ⭐ and into a folder made for it, not into their own project",
     bool(re.search(r"mkdir \S+ && cd", text)))

# ⭐ Pointers are fine now — an assistant reading a page with no orders needs to
# know where the detail lives. ⛔ What is forbidden is a page that is ONLY a
# list, which is what the very first version was.
_expl = low.find("the 30-second version")
_ptr = low.find("for developers")
case("⑤c ⭐ the explanation comes BEFORE the developer pointers",
     _expl != -1 and _ptr != -1 and _expl < _ptr)

# ── ⑤d THE ONE SENTENCE A NEWCOMER SAYS ───────────────────────────────────
# 🔴 Measured 2026-09-05 on TWO models. Both explained Mente OS correctly, then
# drifted: one audited 20k lines of code, the other asked "shall I explore the
# contents?" — a question somebody who knows nothing cannot answer. ⭐ The cause
# was the page ending in two developer commands, so the next step read technical.
case("⑤d 🔴 ⭐ the page ends in ONE plain sentence a newcomer can say",
     bool(re.search(r"set up mente os and walk me through it", low)))
case("⑤e ⛔ and no filename is put in front of the person",
     not re.search(r"(read|open|point yours at)[^.\n]{0,40}start-here", low))

# ⛔ NOR THE DEVELOPER COMMANDS IN THE GETTING-STARTED PATH. They are what made
# both models continue in audit mode instead of walking the person through.
_start = low.find("getting it")
_using = low.find("what using it looks like")
_seg = low[_start:_using] if _start != -1 and _using > _start else low
case("⑤f 🔴 ⛔ no bin/init or battery command in the newcomer's path",
     "bin/init" not in _seg and "run-all" not in _seg)

# ── ⑤g IT SAYS WHAT MAKES IT DIFFERENT ────────────────────────────────────
# ⚠️ Both models compared it to tools the user already had and suggested it was
# redundant. ⛔ That comparison is theirs to make — but making it WITHOUT the
# distinction is what produced "you already have this covered".
case("⑤g ⭐ it states what a notes file cannot do",
     bool(re.search(r"how is this different", low)))

# ── ⑤h THE LICENCE IS REAL, NOT JUST CLAIMED ──────────────────────────────
# 🔴 Measured 2026-09-05 by an external reviewer, on a first pass: the page said
# AGPL-3.0 and the repository carried NO LICENSE file. GitHub's API answered
# `license: null`, which means the default applies — all rights reserved.
# ⚠️ For over a week nobody who cloned this had permission to use it, and the
# page told them they did. ⛔ A licence named and not shipped is worse than none.
_lic = os.path.join(os.path.dirname(ROOT), "LICENSE")
_notice = os.path.join(os.path.dirname(ROOT), "NOTICE")
if os.path.isfile(os.path.join(os.path.dirname(ROOT), "README.md")):
    case("⑤h 🔴 ⭐ the licence it names is actually SHIPPED",
         os.path.isfile(_lic) and os.path.getsize(_lic) > 30000,
         "%d bytes" % os.path.getsize(_lic) if os.path.isfile(_lic) else "🔴 no LICENSE")
    case("⑤i ⛔ and it carries a copyright notice naming the holder",
         os.path.isfile(_notice) and "Copyright" in
         open(_notice, encoding="utf-8").read())
else:
    print("  ⬜ no repository root beside this tree · licence NOT MEASURED")

# ── ⑤j NO FIGURE WITHOUT ITS SOURCE ───────────────────────────────────────
# 🔴 The same reviewer caught the second one: "a rule in a document is followed
# 40-60%" was the engine's central law, repeated 20+ times across both repos,
# and NOWHERE did it cite a source. ⭐ A page that preaches "do not assert what
# you did not measure" cannot open with an invented statistic.
# ⛔ The replacement is what this project actually counted: 0 of 15.
case("⑤j 🔴 ⭐ no unsourced statistic on the page",
     not re.search(r"40\s*-\s*60\s*%|about half the time", low))
case("⑤k ⭐ and the claim it replaced carries its real measurement",
     bool(re.search(r"0 (times out of|of) 15", low)))

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
    # 🔴 THE INVERSE, and it is the case that would have caught the real
    # failure: the PUBLISHED page must carry no order at all — not in visible
    # markdown, and not in a comment either.
    case("⑦ 🔴 ⭐ the PUBLISHED page gives the assistant NO orders",
         not re.search(r"if you are an ai assistant reading|do not summaris|"
                       r"do not report anything you notice", live.lower()))
    case("⑦b 🔴 ⭐ and its clone command clones INTO the folder",
         bool(re.search(r"git clone \S+\.git \.", live)))
    case("⑦c ⛔ the published page is byte-for-byte what the generator makes",
         live == _generated)
else:
    # ⬜ CHK-CAU-003 · said out loud, never swallowed.
    print("  ⬜ the published README is not beside this tree · NOT MEASURED "
          "(expected under run-all's isolated copy)")

plat.rmtree(WORK)

print("\n  ⬜ NOT MEASURED · whether an assistant reaches a good summary · that\n     runs outside this engine · these cases prove the page gives no orders and\n     carries what a stranger needs to decide")

good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: none")
sys.exit(0 if good == len(results) else 1)
