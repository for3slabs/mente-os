#!/usr/bin/env python3
"""probe-start-here — proves the ONE document whose reader is a stranger still says what it must.

🔴 WHY THIS EXISTS. `START-HERE.md` is the only file in this engine read by an
assistant that has never seen the project, on behalf of a person who does not
know what they were sent. ⛔ Everything it mandates was written after a REAL run
failed — and until now nothing checked that any of it survived an edit.

⭐ The law this engine measures itself by: a rule in code holds 100%, a rule that
lives only in a document holds 40-60%. START-HERE was 100% document. Its shape
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

# ── ⑤ IT CHECKS THE MACHINE INSTEAD OF INSTRUCTING ─────────────────────────
# ⛔ A person asking "what is this?" is not asking to become a sysadmin.
case("⑤ ⛔ it forbids telling them to install things",
     bool(re.search(r"never tell them to install", low)))

# ── ⑥ IT IS REACHABLE ──────────────────────────────────────────────────────
# ⭐ A perfect script nobody is pointed to is a script nobody runs. The README is
# what a handed link actually opens.
readme = os.path.join(os.path.dirname(ROOT), "README.md")
inner = os.path.join(ROOT, "README.md")
found = [p for p in (readme, inner)
         if os.path.isfile(p) and "START-HERE" in open(p, encoding="utf-8").read()]
case("⑥ 🔴 ⭐ a README points at it (a script nobody reaches never runs)",
     bool(found), "%d of 2 README(s)" % len(found))

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
