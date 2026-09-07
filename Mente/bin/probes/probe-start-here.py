#!/usr/bin/env python3
"""probe-start-here — proves the ONE document whose reader is a stranger still says what it must.

🔴 WHY THIS EXISTS. `START-HERE.md` is the only file in this engine read by an
assistant that has never seen the project, on behalf of a person who does not
know what they were sent. ⛔ Everything it mandates was written after a REAL run
failed — and until now nothing checked that any of it survived an edit.

⭐ The law this engine measures itself by: a rule in code holds 100%, a rule that
lives only in a document holds when remembered. START-HERE was 100% document. Its shape
was validated (headings, ceilings, declaration) and its CONTENT was not — so
deleting the sentence that makes the questions appear as a chooser broke nothing
that anyone could see.

⚠️ WHAT THIS CAN AND CANNOT MEASURE. It proves the INSTRUCTION is present and
reachable. ⛔ It cannot prove an assistant obeys it — that is outside this
engine, and stating the limit is the point (CHK-CAU-003: a skipped check is said
out loud, never swallowed).
"""
import os, re, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d):
    if os.path.exists(os.path.join(_d, "bin", "utf8.py")):
        sys.path.insert(0, os.path.join(_d, "bin")); break
    _d = os.path.dirname(_d)
import utf8                                          # noqa: F401,E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import ROOT                             # noqa: E402

results = []


def case(label, ok, detail=""):
    print("  %-58s %s %s" % (label, "✅" if ok else "🔴", detail))
    results.append((label, ok))


print("═══ SONDA · START-HERE ═══\n")

PATH = os.path.join(ROOT, "START-HERE.md")
case("① the file a stranger is handed EXISTS", os.path.isfile(PATH))
if not os.path.isfile(PATH):
    print("\n  ➜ 1 of 1 correct")
    sys.exit(1)

text = open(PATH, encoding="utf-8").read()
low = text.lower()

# ── ② EVERY CHOICE IS A CHOOSER ────────────────────────────────────────────
# 🔴 Measured 2026-09-02: one run asked §2 as a proper selector and reverted to
# prose for every question after it. ⚠️ The person had to type answers to a
# system they had just met. So the mandate must be for the WHOLE run, not §2.
case("② ⭐ it names the chooser tool by name", "askuserquestion" in low)
# ⚠️ MEASURES THE IMPERATIVE, NOT THE VOCABULARY. 🔴 The first version of this
# case looked for the words "every choice" and "not only" anywhere in the file —
# and a sabotage that rewrote the actual instruction to "just write it out" still
# PASSED, because those words survive elsewhere. A probe that passes against
# broken content measures nothing.
_verb = re.search(r"decision to make,\s*(.{0,60})", low)
case("②b 🔴 ⭐ the standing instruction still SAYS to use the chooser",
     bool(_verb) and "chooser" in _verb.group(1),
     (_verb.group(1)[:34] if _verb else "the sentence is gone"))
case("②c ⛔ and it is mandated beyond §2 (one run got §2 right, typed the rest)",
     bool(re.search(r"every choice is a chooser, not only", low)))

# ── ③ NO WORD THEY DID NOT ASK FOR ─────────────────────────────────────────
# 🔴 The real quote this produced: "where are you going to commit them, I do not
# understand why I should commit."
case("③ ⛔ it forbids the vocabulary a stranger never asked for",
     "commit" in low and "branch" in low
     and bool(re.search(r"(never use a word|did not ask for)", low)))
case("③b ⭐ and `commit` is EXPLAINED before it may be said",
     bool(re.search(r"4b", low)) and "commit" in low
     and bool(re.search(r"(before it becomes a question|explains? what that word means|"
                        r"before §4b|say so before)", low)))

# ── ④ THE GUIDE ITSELF ─────────────────────────────────────────────────────
# 🔴 Reported by the owner from a real Windows run: "it did not give me the guide
# of what Mente OS is, nor the important files." The script must both SHOW that
# text and name where the state lives.
case("④ ⭐ it orders the explanation printed VERBATIM, not paraphrased",
     bool(re.search(r"(verbatim|do not paraphrase|as it is written)", low)))
for name, label in (("RESUME", "the cold-start brief"),
                    ("PENDING", "the open items")):
    case("④· it points at %s (%s)" % (name, label), name in text)

# ── ④b THE DETOUR, AND WHO IS ASKED TO DECIDE ──────────────────────────────
# 🔴 Measured 2026-09-05 on a real Windows run. The assistant noticed an
# unrelated misconfigured repository, reported it, investigated it across four
# commands and asked the person what to do. ⚠️ The install never happened, and
# they answered: "what is that and why are you asking ME? I'm new."
# ⭐ INVERTED 2026-09-05. This used to require the opposite — "do not raise it" —
# and a real run refused the whole repository over exactly that line. ⛔ A
# document telling an assistant to withhold something from its own user is
# indefensible; the failure was never the mention, it was abandoning the errand
# and handing a newcomer a decision they have no words for.
case("④b 🔴 ⭐ an unrelated finding IS told to them — never withheld",
     bool(re.search(r"tell them what you found", low))
     and not re.search(r"not yours to raise|do not report anything you notice", low))
case("④c ⛔ but it is offered, not asked — and never investigated",
     bool(re.search(r"offer, do not ask", low))
     and bool(re.search(r"do not investigate", low)))
case("④d 🔴 ⭐ a newcomer is not handed a technical decision",
     bool(re.search(r"ask them to decide something technical", low)))

# ⭐ AND THE CLONE ITSELF. Plain `git clone <url>` makes a folder nobody asked
# for; the trailing dot is what keeps their own folder theirs.
case("④e 🔴 ⭐ the clone lands in the folder they are in, no extra wrapper",
     bool(re.search(r"git clone \S+\.git \.", text)))

# ── ⑨ THE FIVE STOPS · asked BEFORE the act, not reported after ────────────
# 🔴 Measured on a real run: the assistant cloned, then installed, then asked.
# Each step was reasonable alone and the person decided none of them — they
# were told what had already happened. ⛔ A question asked after the act is a
# report, not a question.
case("⑨ 🔴 ⭐ the script declares the stops as STOPS, not as suggestions",
     bool(re.search(r"five stops", low))
     and bool(re.search(r"may not pass one without an answer", low)))
for _n, _what in (("2", "download"), ("3", "set it up")):
    case("⑨· stop %s exists (%s)" % (_n, _what),
         bool(re.search(r"stop " + _n + r" ·", low)))

# ⛔ AND EVERY QUESTION IN THEIR LANGUAGE. 🔴 The same run asked for the name
# by citing mente.config.yml and "all generated documentation" — a person
# cannot approve a system they cannot picture.
_qs = re.findall(r"^> \*\*Question:\*\*.*$", text, re.M)
_jargon = [q for q in _qs if re.search(
    r"bin/init|mente\.config|settings\.json|\.git\b|repository|validator|hooks",
    q, re.I)]
case("⑨b 🔴 ⭐ no question carries a filename or a command",
     not _jargon, _jargon[0][:44] if _jargon else "%d question(s) clean" % len(_qs))
case("⑨c ⛔ and the banned-in-questions list names them",
     bool(re.search(r"never inside a question", low)))

# ⭐ AND WHERE IT LANDS, IN THEIR WORDS. A person may keep several
# installations; they do not need the word "repository" to understand that
# this one lives here and only here.
case("⑨d ⭐ it says the install stays in this folder, in plain words",
     bool(re.search(r"stays in this folder", low))
     and bool(re.search(r"neither knows about the other|that one is separate", low)))
# ── ⑤ IT CHECKS THE MACHINE INSTEAD OF INSTRUCTING ─────────────────────────
# ⛔ A person asking "what is this?" is not asking to become a sysadmin.
case("⑤ ⛔ it forbids telling them to install things",
     bool(re.search(r"never tell them to install", low)))

# ── ⑥ CONTAINMENT · the script must not send it looking around ─────────────
# 🔴 Measured 2026-09-06 on two real runs. §0 used to open by telling the
# assistant to hunt for leftovers from an earlier attempt, and it stated that
# "two things live OUTSIDE this folder". ⛔ That taught it Mente OS leaves
# traces elsewhere — so it began reporting other folders on the machine, and
# the owner ended up distrusting a system that had touched nothing.
# ⭐ It is also no longer true: since the skill became a template, everything
# the engine writes lands inside the cloned folder. Delete it and it is gone.
# ⚠️ MEASURES THE IMPERATIVE, NOT THE WORD. The new §0 says "there is nothing to
# hunt for" — the right sentence, which a keyword search reads as the wrong one.
# ⛔ What must be absent is the ORDER: a heading that sends it looking, or a
# command block telling it to inspect the disk before §1.
_s0 = low[low.find("## 0 ·"):low.find("## 1 ·")] if "## 0 ·" in low else ""
case("⑧ 🔴 ⭐ §0 does not ORDER the assistant to go looking",
     "look for leftovers" not in _s0
     and not re.search(r"before anything else, run this", _s0))
case("⑧b ⛔ and §0 carries no command block to inspect the disk",
     "```bash" not in _s0, "no shell in §0" if "```bash" not in _s0 else "🔴 has one")
case("⑧c 🔴 ⭐ and it states the containment instead",
     bool(re.search(r"everything lives in this folder|mente os is contained", low)))
case("⑧d ⛔ it forbids scanning the home directory or other projects",
     bool(re.search(r"do not.{0,40}scan the home|list other projects", low)))
case("⑧e ⭐ and says a hundred installations do not see each other",
     bool(re.search(r"hundred installations", low)))
# ── ⑥ IT IS REACHABLE ──────────────────────────────────────────────────────
# ⭐ A perfect script nobody is pointed to is a script nobody runs. The README is
# what a handed link actually opens.
readme = os.path.join(os.path.dirname(ROOT), "README.md")
inner = os.path.join(ROOT, "README.md")
found = [p for p in (readme, inner)
         if os.path.isfile(p) and "START-HERE" in open(p, encoding="utf-8").read()]
case("⑥ 🔴 ⭐ a README points at it (a script nobody reaches never runs)",
     bool(found), "%d of 2 README(s)" % len(found))

# ── ⑩ THE INSTALL IS NOT THE DELIVERY ──────────────────────────────────────
# 🔴 Measured 2026-09-06. A run installed cleanly, was then asked for real work,
# and wrote it to a loose file at the top of the folder: no block, `RESUME.md`
# and `PENDING.md` still the shipped templates. ⛔ Every check was green over an
# empty `work/` — the engine measured itself and held nothing.
_low = text.lower()
case("⑩ 🔴 ⭐ the script says a green install is not the delivery",
     "the install is not the delivery" in _low)
case("⑩b ⭐ and names what an empty work/ means",
     "empty" in _low and "measures the engine" in _low)
# ⛔ The same run read the four types, decided a personal plan "did not fit a
# system for software", and opted out. ⭐ The type is the shape of the work, and
# `docs` holds any written product — there is no subject this engine declines.
case("⑩c 🔴 ⭐ it says the type is the SHAPE, never the topic",
     "shape of the work" in _low and "never the topic" in _low)
case("⑩d ⛔ and §6 refuses a loose file as the answer",
     "a file outside `work/` is not held by anything" in text)

# ── ⑪ WHERE IT ALL LIVES, SAID OUT LOUD ────────────────────────────────────
# 🔴 Measured the same run: the history was explained without ever saying it was
# per-folder, so the person could not tell whether the system had reached the
# rest of their machine. ⭐ Isolation is the promise; an unstated promise is not
# one the person can rely on.
case("⑪ ⭐ it says everything lives in THIS folder",
     "lives in **this folder**" in text)
case("⑪b ⭐ and that deleting the folder removes it",
     "delete the folder and all of it is gone" in _low)
case("⑪c ⭐ and that a second installation is separate",
     "neither knows the other exists" in _low)

# ── ⑫ WHO THEY ARE IS NOT THE ERRAND ───────────────────────────────────────
# 🔴 Measured 2026-09-06. An assistant handed only the link queried the repo's
# contributor list, matched the commit emails against its own session account,
# opened with "this repository is yours" and spent the run interrogating the
# person. ⛔ The errand was abandoned for an investigation nobody asked for.
case("⑫ 🔴 ⭐ it forbids looking up who wrote this",
     "who they are is not your errand" in _low)
case("⑫b ⛔ and names the contributor list specifically",
     "contributor" in _low and "commit authors" in _low)
# ⭐ The reason has to be the ERRAND, not privacy — a privacy argument invites
# a judgement call about whether this case is sensitive. It never is.
case("⑫c ⭐ the reason given is that it changes no action",
     "the script is the same" in _low)
# 🔴 The second half: a value already in hand stops feeling like a question.
case("⑫d 🔴 ⭐ it reads the name candidates only at the moment it asks",
     "until the moment you need it" in _low)

# ── ⑬ A BLOCKED STEP DOES NOT CHANGE HANDS ─────────────────────────────────
# 🔴 Measured the same run: a permission guard refused the setup and the run
# answered "open PowerShell and paste this command". ⚠️ The person was exactly
# as unable as before, and now believed the errand was theirs.
case("⑬ 🔴 ⭐ a blocked step is not handed to the person",
     "not a step that changes hands" in _low)
case("⑬b ⛔ and it refuses to hand over a command to type",
     "they never see a command" in _low)

# ── ⑭ THEY CAN ASK WHETHER IT IS ON ────────────────────────────────────────
# 🔴 "I do not even know whether it is active" — the complaint underneath the
# others. ⭐ Three sentences, in their words, and the commands exist.
case("⑭ 🔴 ⭐ the script teaches 'is Mente OS on?'",
     "is mente os on?" in _low)
case("⑭b ⭐ and how to stop it, and start it again",
     "turn mente os off" in _low and "turn it back on" in _low)
# ⛔ The distinction that makes the switch usable at all.
case("⑭c ⚠️ it says off PAUSES and deletes nothing",
     "pauses" in _low and "nothing is deleted" in _low)
# ⭐ And the commands it names are real — a taught sentence that maps to no
# command is worse than none: the assistant improvises one.
_bin = os.path.join(ROOT, "bin")
case("⑭d ⭐ the three commands it names actually ship",
     all(os.path.isfile(os.path.join(_bin, n)) for n in ("status", "off", "on")))

# ── ⑮ THE INSTALL MUST BE VISIBLE ──────────────────────────────────────────
# 🔴 Measured 2026-09-06: "it installs but it does not seem installed — no
# metrics, no commands, nothing." ⛔ The interface used to live behind the first
# block, so a run that never opened one taught the person nothing.
case("⑮ 🔴 ⭐ it shows the system is on, right after the setup",
     "show them it is on" in _low)
case("⑮b ⭐ and hands over the whole interface at once",
     "the whole interface" in _low and "not only if a block gets opened" in _low)
# ⚠️ The sentences must be reachable BEFORE §5 — a person who never opens a
# block still needs them. Measured by position, not by presence.
_i4c = text.find("4c · ")
_i5 = text.find("## 5 · THE FIRST THING")
case("⑮c ⛔ and it comes BEFORE the first block, not after",
     0 < _i4c < _i5, "4c@%d < 5@%d" % (_i4c, _i5))

# ── ⑯ THE BOUNDARY IS ABOUT WHAT WAS ALREADY THERE ─────────────────────────
# 🔴 Measured: the owner, standing in a folder they had just installed into, was
# offered "do not touch Mente OS or its configuration". ⛔ A question whose only
# honest answer is "all of it, it is mine" should not have been asked.
case("⑯ 🔴 ⭐ the boundary protects prior work, never the engine",
     "never about the engine" in _low)
case("⑯b ⛔ and an empty folder is not asked for a list",
     "do not ask for a list" in _low)
case("⑯c ⚠️ it names the shape of the wrong question",
     "all of it, it is mine" in _low)

# ── ⑰ WHERE THE PRODUCT LANDS, SAID BEFORE IT IS WRITTEN ───────────────────
# 🔴 Measured: material written to the repository root, then beside BLOCK.md
# where BLK-SHP-001 refused it. ⛔ Two wrong places, because the script named
# where the RECORD goes and never where the PRODUCT goes.
case("⑰ 🔴 ⭐ it says where the product lands, not only the record",
     "where the work itself will land" in _low)
case("⑰b ⭐ and names Cerebro as that place",
     "cerebro/<name>/" in _low)
case("⑰c ⛔ and the repository root as the place it never goes",
     "never" in _low and "the repository root" in _low)
# ⚠️ Whitespace-collapsed: the sentence wraps across two source lines, and a
# probe matching it unwrapped measures the line width, not the rule.
_flat = " ".join(_low.split())
case("⑰d ⭐ and that declaring it is what makes it governed",
     "not the same as being governed" in _flat)

# ── ⑱ MEASURING IS NOT PUBLISHING ──────────────────────────────────────────
# 🔴 Measured 2026-09-06. A run executed the whole battery, read the raw
# `checks: 854 · failed: 9` out loud to a person who had asked what the system
# was, and never published the numbers: `docs/METRICS.md` did not exist
# afterwards. ⛔ The owner said it — "it showed me nothing of the battery,
# nothing of the structure". The script named `generate-metrics` zero times.
case("⑱ 🔴 ⭐ the script says to publish what the battery measured",
     "generate-metrics" in text)
case("⑱b ⭐ and says publishing is not optional",
     "run and then published" in _low)
# ⚠️ The pair only means something together: measuring without publishing
# leaves the numbers in a cache nothing reads.
case("⑱c ⚠️ and that generate-metrics READS, never runs",
     "never runs it" in _low)
# ⛔ The same run described real defects in chat and wrote zero entries.
case("⑲ 🔴 ⭐ findings go in the pending list, not only in the chat",
     "pending list" in _low and "dies with it" in _low)
case("⑲b ⭐ and it points at the contract that fixes the shape",
     "contract-pending" in text)

# ── ⑦ IT IS DECLARED AS AN ENGINE FILE ─────────────────────────────────────
tsv = os.path.join(ROOT, "pieces.tsv")
case("⑦ it is declared in the piece table",
     os.path.isfile(tsv) and "START-HERE.md" in open(tsv, encoding="utf-8").read())

# ⬜ STATED, NOT MEASURED — the limit belongs in the output, not in a comment.
print("\n  ⬜ NOT MEASURED · whether an assistant OBEYS this script · that runs "
      "outside\n     this engine · these cases prove the instruction is present "
      "and reachable")

good = sum(1 for _, ok in results if ok)
print("\n  ➜ %d of %d correct" % (good, len(results)))
for l, ok in results:
    if not ok:
        print("     🔴 %s" % l)
print("  leftovers: none")
sys.exit(0 if good == len(results) else 1)
