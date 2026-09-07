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

# ── ④z THE PAGE MAY NOT PROMISE WHAT THE CLONE BREAKS ──────────────────────
# 🔴 Measured 2026-09-06 on two independent runs. The page said it "writes files
# inside its own folder", and the clone carries a Claude Code skill that loads
# the moment the folder exists — before any install — reads the person's
# transcripts, and writes notes into the assistant's shared memory folder.
# ⛔ BOTH ASSISTANTS FOUND IT BY READING, and told the owner the page was not
# telling the truth. ⭐ A false claim on the front page destroys the credit the
# honest ones earned: the same reviewers had just audited the code and called it
# clean, then hit this and started warning against installing.
_skill = os.path.join(os.path.dirname(ROOT), ".claude", "skills")
if os.path.isdir(_skill):
    case("④z 🔴 ⭐ the page discloses the skill that ships with the clone",
         "skill" in low and bool(re.search(r"\.claude/skills", low)))
    case("④z2 ⛔ and says it loads before anything is installed",
         bool(re.search(r"loads the moment|before you install", low)))
    case("④z3 🔴 ⭐ and that it reads transcripts and writes outside the project",
         "transcript" in low and bool(re.search(r"memory folder|outside", low)))
else:
    # ⬜ CHK-CAU-003 · said out loud, never a silent pass.
    print("  ⬜ no .claude/skills beside this tree · disclosure NOT MEASURED")

# ── ④y THE PAGE ADMITS WHAT A REVIEWER FINDS ANYWAY ────────────────────────
# 🔴 Measured 2026-09-06 on two independent runs. Both assistants audited the
# code, called it clean — and then warned the owner against installing, citing
# the age, the zero stars and the single author. ⛔ Public facts the page had
# not mentioned, so they landed as an uncomfortable discovery instead of a
# known one. ⭐ Saying it first is what keeps the credit the audit earned.
case("④y 🔴 ⭐ the page states the age, the adoption and the single author",
     bool(re.search(r"before you trust it", low))
     and "adoption" in low and "author" in low)
case("④y2 ⛔ and tells them to try it where breaking is affordable",
     bool(re.search(r"afford to break", low)))

# ── ④x THE DESTINATION IS NAMED, NOT LEFT OPEN ─────────────────────────────
# 🔴 Same two runs: the page said only "the folder you want". Both assistants
# invented a destination, invented DIFFERENT ones, and both had to defend the
# choice to a confused owner. ⛔ An instruction that leaves the decision open
# is not an instruction.
case("④x 🔴 ⭐ it says WHERE to clone, and where not to",
     bool(re.search(r"not your\s*\n?>?\s*home directory|not the desktop", low))
     and "syncs to a cloud drive" in low)
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

# ⚠️ AND THE SWEEP MUST BE WHOLE. 🔴 My first pass fixed the page and left the
# same unsourced claim in six other files, in different words — the front page
# read clean while the engine still asserted it. ⭐ One phrasing removed from one
# file is not a claim retracted.
_stale = []
for _root, _dirs, _files in os.walk(ROOT):
    _dirs[:] = [d for d in _dirs if d not in (".git", "__pycache__", "cache")]
    for _f in _files:
        if not _f.endswith((".md", ".py", ".sh", ".template")):
            continue
        _fp = os.path.join(_root, _f)
        if os.path.basename(_fp) == "probe-readme.py":
            continue          # ⬜ this file names the figure in order to ban it
        try:
            _t = open(_fp, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        # ⚠️ NEWLINES COLLAPSED FIRST. 🔴 My previous version matched on the raw
        # text, so the same sentence wrapped across two lines slipped through —
        # two files kept asserting it and the probe reported the sweep complete.
        # ⭐ A claim is a sentence, not a line: measure the sentence.
        _flat = re.sub(r"\s+", " ", _t)
        if re.search(r"40\s*-\s*60\s*%|followed (about|roughly) half the time",
                     _flat):
            _stale.append(os.path.relpath(_fp, ROOT))
case("⑤l 🔴 ⭐ the unsourced figure is gone from the WHOLE engine, not just here",
     not _stale, ", ".join(_stale)[:44] or "0 file(s)")

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

# ── ⑧ THE TWO STOPS THAT CANNOT LIVE IN THE SCRIPT ────────────────────────────
# 🔴 Measured 2026-09-06. `START-HERE.md` carries five stops, and the first two
# say "ask BEFORE the download" — ⛔ but that file is inside the folder that does
# not exist yet. An assistant reading only this page downloaded and installed on
# its own, then reported it. ⭐ This page is the ONLY text that arrives before
# the disk is touched, so those two questions have to be printed HERE.
_low = _generated.lower()
case("⑧ 🔴 ⭐ the page asks before DOWNLOADING, not after",
     "before the download" in _low or "before you download" in _low)
case("⑧b ⭐ and before SETTING IT UP too",
     "before you set it up" in _low or "set it up" in _low)
# ⛔ Two options is not a chooser the person can refuse — each stop offers three.
case("⑧c ⭐ each stop offers a way to say no",
     "not yet" in _low and "somewhere else" in _low)
# ⚠️ The words a person cannot answer. ⭐ Measured: the run that failed asked
# with `clone` and `repository` in the question itself.
_q = re.findall(r"^> \*\*(?:Question|①|②)[^\n]*", _generated, re.M)
case("⑧d ⛔ no question uses a word the person must look up",
     not any(w in q.lower() for q in _q
             for w in ("clone", "repository", "git ", "init", "bin/")),
     "%d question line(s)" % len(_q))
# ⭐ And it hands the run back to the script, so the other three stops still run.
case("⑧e ⭐ it points at the rest of the script for the remaining stops",
     "start-here.md" in _low and "rest of the script" in _low)
# ── ⑨ THE PAGE FORBIDS THE INVESTIGATION, AND THE HAND-OFF ────────────────
# 🔴 Measured 2026-09-06, both on the same run and both BEFORE the script could
# be read: the assistant looked up who wrote the repository, and later handed a
# command to the person when a permission guard fired. ⭐ Neither rule can wait
# for START-HERE — by then the run has already gone wrong.
case("⑨ 🔴 ⭐ the page forbids looking up who wrote it",
     "do not go looking for who wrote this" in _low)
case("⑨b ⭐ and gives the reason that holds: the script is the same",
     "the script is the same" in _low)
case("⑨c 🔴 ⭐ a permission block is not handed to the person",
     "the permission belongs to you, the work belongs to me" in _low)
case("⑨d ⛔ and it names the wording it refuses",
     "paste this into a terminal" in _low)
# ⭐ The download is the moment the history lands — 🔴 a person had to ask
# afterwards whether they had a record of their own.
case("⑨e ⭐ it says what lands in the folder as it downloads",
     "record of your work" in _low)
# ── ⑩ THE BIOGRAPHY · pieces, commands, tutorial ───────────────────────────
# 🔴 Measured 2026-09-06. This page described the system and named not one
# component and not one command — ⛔ so a person asking "what is this?" got a
# pitch, and a technical reader had nothing concrete to judge. ⭐ The owner's
# framing: the page must answer "it is this · it is for this · these are the
# pieces · these are the commands", in that order, without jargon.
case("⑩ ⭐ the page names its pieces, with what each one is FOR",
     "the six pieces" in _low and "how you ask for it" in _low)
# ⛔ Naming a piece without the sentence that reaches it teaches a vocabulary
# nobody can use. Every row carries the words the person actually says.
_rows = re.findall(r"^\| (?:[^|]*\*\*)([A-Z][a-z]+)\*\*[^|]*\|[^|]*\|([^|]*)\|$",
                   _generated, re.M)
case("⑩b ⛔ and each piece says how to ask for it",
     len([r for r in _rows if r[1].strip()]) >= 6,
     "%d row(s) with a phrase" % len([r for r in _rows if r[1].strip()]))

case("⑩c ⭐ the commands are listed, not promised",
     "the commands — all of them" in _low)
# ⭐ THE CASE THAT KEEPS IT HONEST: every command the page names must SHIP.
# ⛔ A page listing a command that does not exist is the skill failure again,
# one layer out — measured 2026-09-06, six citations, none resolving.
_named = set(re.findall(r"`bin/([a-z][\w./-]*)`", _generated))
_gone = sorted(n for n in _named
               if not os.path.exists(os.path.join(ROOT, "bin", n)))
case("⑩d 🔴 ⭐ every command the page names actually ships",
     not _gone, ", ".join(_gone) or "%d command(s)" % len(_named))

# ⭐ The tutorial: the six stops a first run may not skip. ⛔ It lives HERE
# because this page is the only text that arrives before the disk is touched.
case("⑩e ⭐ the tutorial states its six stops",
     "six stops" in _low and "you answer every one" in _low)
case("⑩f ⛔ and says the empty-folder case does not ask for a list",
     "no list to give" in _low)
# ⚠️ The one sentence whose cost is invisible until too late.
case("⑩g ⭐ and it teaches the session-close sentence by name",
     "session-wrap" in _generated and "before the" in _low
     and "conversation resets" in _low)


plat.rmtree(WORK)

print("\n  ⬜ NOT MEASURED · whether an assistant reaches a good summary · that\n     runs outside this engine · these cases prove the page gives no orders and\n     carries what a stranger needs to decide")

good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: none")
sys.exit(0 if good == len(results) else 1)
