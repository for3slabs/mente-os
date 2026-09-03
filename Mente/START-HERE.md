# START HERE — what to show a person who was handed this link

**Status:** current · **Type:** contract · **Updated:** {{date}} · **Owner:** {{owner}}
**Read by:** ⭐ **the assistant, not the person.** It is a script, not a description.
**Scope:** ⚠️ ENGINE document — it ships identical to every clone.

> ⭐ **Why `contract` and not `entry-point`.** An entry-point may point elsewhere for the detail.
> ⛔ This one may not: an assistant that reads half a script improvises the other half, which is
> the exact failure the file exists to prevent. ⚠️ It is a BASE file in the sense
> `../rules/contract-document.md` §4 gives the word — **it ships whole, and its reader is a
> stranger.**

## Purpose

⭐ **Somebody sent this repository to a person who does not know what it is**, and that person
pasted the link into an assistant. ⛔ Without this file the assistant improvises: it reads the
tree, guesses, and ends up telling a non-technical person to install Python and hand-edit a YAML.

⚠️ **Measured 2026-09-02, on a real run:** an assistant handed only the URL invented the steps,
sent the user to edit `mente.config.yml` by hand, and asked *"shall we install it?"* — ⛔ a
question the user cannot answer, because they are asking IT what to do.

---

## ⛔ TO THE ASSISTANT READING THIS: DO NOT PARAPHRASE

⭐ **Print §1 as it is written.** It is short on purpose. ⛔ Do not summarise it, do not replace it
with your own description of the repository, and do not open other files first — everything the
person needs to decide is below.

⚠️ **Never tell them to install anything.** Checking what a machine has is YOUR job, and §3 is how
you do it. ⛔ A person asking *"what is this?"* is not asking to become a system administrator.

### ⭐ THE RULE THAT HOLDS FOR THE WHOLE RUN: every choice is a CHOOSER

⛔ **Not only the one in §2.** From the first message to the last, whenever this person has a
decision to make, present it with your interface's chooser — in Claude Code, `AskUserQuestion`.

🔴 **Measured 2026-09-02.** One run asked §2 as a proper chooser and then reverted to prose for
every question after it, so the person had to type answers to a system they had just met. ⚠️ The
first question being right does not make the run right: **they all have to be.**

| ⛔ Never as prose | ⭐ Always as a chooser |
|---|---|
| *"shall we keep testing or shall I explain blocks?"* | two options, the recommended one first |
| *"do you want to commit this?"* | ⚠️ and only after §4b explains what that word means |
| *"shall we open your first block?"* | two options — open one, or hear more first |

⚠️ **The one exception is a question with no options at all** — their name in §4. That is a blank
to fill, not a choice between things, and a chooser with a single option is refused by the tool and
never reaches the person (measured, same run). ⛔ Everything else is a chooser.

### ⭐ NEVER USE A WORD THEY DID NOT ASK FOR

⛔ `commit` · `branch` · `merge` · `repo` · `hook` · `validator` · `probe` · `placeholder`.

🔴 **Measured on the same run:** the assistant asked *"shall I commit these initialisation
changes?"* to somebody who had asked what Mente OS was twenty minutes earlier. ⚠️ Their reply was
*"where are you going to commit them, I do not understand why I should commit."*

⭐ **If a step genuinely needs one of those words, explain it in one sentence FIRST, in their
terms, then ask.** §4b is the one for `commit`, written out. ⛔ If no such explanation exists in
this file, the step is not one to raise with them at all.

---

## 0 · FIRST, LOOK FOR LEFTOVERS FROM AN EARLIER ATTEMPT

⭐ **Before anything else, run this.** ⛔ Somebody may have tried this before and deleted the
folder without knowing that two things live OUTSIDE it:

```bash
ls CLAUDE.md .git/hooks/pre-push .git/hooks/pre-commit 2>/dev/null
grep -l "CLAUDE-MENTE-OS" CLAUDE.md 2>/dev/null
```

🔴 **Measured 2026-09-02, and it frightened the person it happened to:** they deleted the folder,
started fresh, and the assistant answered as if a half-finished installation were still there —
because `CLAUDE.md` still carried `@Mente/CLAUDE-MENTE-OS.md`, an import pointing at a file that
no longer existed. ⚠️ **It was not memory. It was a file on their disk**, and being told
otherwise is what made it confusing.

⭐ **If anything came back, ASK — do not decide for them:**

> **Question:** I found leftovers from an earlier attempt at installing Mente OS — a line in your
> `CLAUDE.md` pointing at a folder that is gone. What would you like to do?
>
> | Option | What it means |
> |---|---|
> | ⭐ **Clean start** *(recommended)* | I remove the leftover line and install fresh — nothing of yours is touched, only the pointer to what is missing |
> | **Show me first** | I show you exactly which lines and files are left over, and you decide |
> | **Leave it, just explain** | I explain what Mente OS is and change nothing |

⛔ **Never delete anything before asking.** ⚠️ `CLAUDE.md` is the USER'S file — the installer only
ever appends one line to it, and only that line is ours to remove.

⭐ **If nothing came back, say nothing about it** and go straight to §1. A clean machine should
never hear about a problem it does not have.

---

## 1 · SHOW THIS, VERBATIM

> ## Mente OS
>
> **What it is:** a system that keeps an AI assistant from losing the thread of your work.
>
> **The problem it solves:** every time a conversation resets, the assistant forgets where you
> were, what was decided and what must not be touched — so it rebuilds that by guessing, and
> sounds equally confident whether it guessed right or wrong.
>
> **How it solves it:** the work lives on disk in a shape the assistant must fill in, and small
> programs check it. A rule written in a document is followed about half the time; a rule a
> program refuses to break is followed every time.
>
> **The four pieces:**
>
> | | |
> |---|---|
> | **A block** | one unit of work. It says what is being built, ⭐ **what must NOT be touched**, what it depends on, and what comes next |
> | **A campaign** | several blocks under one mission, so switching between them does not restart the reason |
> | **The gates** | they fire on their own and stop what should not happen — a destructive change with no way back, closing work that is not finished |
> | **The memory** | two files, and one habit that keeps them true — see below |
>
> **The memory, by name:**
>
> | File | ⭐ What it holds |
> |---|---|
> | `memory/RESUME.md` | **where we left off** and what comes next — the assistant reads it first, every single session, before anything else |
> | `memory/PENDING.md` | **everything postponed** — so a thing put off is not a thing lost |
>
> ⭐ **You never write either of them.** They are written when a session is closed.
>
> **⛔ And the part most people find out too late — closing a session:**
>
> A conversation with an assistant eventually resets. ⚠️ **The files on your disk survive that.
> The reasoning does not** — why something was decided, what was tried and rejected, what comes
> next. That is what `RESUME.md` is for, and it is only true if it gets written **before** the
> reset, never after.
>
> | You say | ⭐ What happens |
> |---|---|
> | *"let's close the session"* | I write down where we got to and what comes next, then tell you it is safe to start fresh |
> | *"is it safe to start fresh?"* | I check — ⛔ and if something would be lost, **I say no and name it** |
>
> ⭐ **Say it before you close a conversation, and nothing is lost between one and the next.**
> That single habit is the difference between this system working and not.
>
> **What you do with it — you delegate, in your own words:**
>
> | You say | ⭐ What happens |
> |---|---|
> | *"build me X"* | it opens a block, asks what it may and may not touch, and works inside that |
> | *"where were we?"* | it reads `RESUME.md` instead of guessing |
> | *"what's left?"* | it reads `PENDING.md` |
> | *"is this done?"* | it cannot say yes until the checks pass — ⛔ that is not its opinion to give |
> | *"let's close the session"* | it records the reasoning before it can be lost |
>
> ⭐ **You do not learn commands and you do not remember any of this.** You ask in plain words;
> the system is what makes the assistant keep its promises.
>
> **What it needs:** three things most computers already have. ⚠️ **You do not have to check or
> install them — I will.**

---

## 2 · THEN ASK — as a SELECTOR, with these exact options

⭐ **If your interface can present choices, use it here** — in Claude Code that is the
`AskUserQuestion` tool. ⚠️ This engine cannot know what any particular host offers, so it names
the mechanism it knows and describes the SHAPE for the rest: a question, three labelled options,
the recommended one first. ⛔ If your interface has no such tool, write the three options as a
short list and ask them to pick a number — never a paragraph.

⭐ **The point is that they choose, not that they compose.** ⛔ Do not write the options out as
prose and wait for them to type: a person who does not know the system cannot compose an answer
to a question about a system they do not know — ⚠️ they can pick one.

⭐ **Ask this, with these three options and no others:**

> **Question:** What would you like to do with Mente OS?
>
> | Option | What it means |
> |---|---|
> | ⭐ **Set it up here** *(recommended)* | I check your computer, install it, and we open your first piece of work together |
> | **Just tell me more first** | I explain how a block works, or the memory, before touching anything |
> | **Nothing for now** | You wanted to know what it is — that is done |

⛔ **Three options, and the first is the recommendation.** ⚠️ Never a single-option chooser: the
tool refuses it and the person never sees the question — measured 2026-09-02.

⛔ **Stop there and wait.** ⚠️ Do not clone, do not check anything, do not install: the person has
not said yes yet.

---

## 3 · IF THEY CHOSE «SET IT UP» — check, never instruct

```bash
python3 --version ; git --version ; bash --version | head -1
```

| Result | ⭐ What you say |
|---|---|
| all three answer | *"You have everything. Shall I set it up?"* |
| one is missing | ⛔ **Name what is missing and offer to handle it** — never *"install Python 3.8+"*. On Windows say Git Bash usually brings all three |

---

## 4 · THEN INSTALL IT YOURSELF — no second question

⭐ **They already said yes in §2.** ⛔ Asking again — *"shall I install it now?"* — makes them
approve the same thing twice, and the second approval carries no new information.

```bash
cd Mente
bin/init --owner "<their name>"
bin/probes/run-all.py
```

⚠️ **`bin/init` asks for a name and refuses to guess one.** ⭐ Ask it as a plain sentence:

> **What name should I put as the owner?** *(it goes in the files the system creates, and you can
> change it later)*

⛔ **Not as a multiple-choice question** — there are no options to choose between, and a chooser
with one option is refused by the tool and never reaches the person. ⚠️ Measured 2026-09-02: an
assistant tried exactly that and the question was rejected mid-run.

⛔ **Do not send them to edit `mente.config.yml`**: `bin/init` writes it.

⭐ **Then report one line**, using the numbers the run just printed: *"Installed — N checks, 0
failures."* ⛔ Not the log, and ⚠️ **not a number from this file**: quote what the run said, or it
is a figure that was true once.

⛔ **Do not paste the run's output at them, and do not walk them through its findings.** ⚠️ A
finding is a message from the engine to YOU. Measured 2026-09-02: an assistant read the whole
report aloud — undeclared files, folder permissions, uncommitted changes — to a person who had
asked what the system was. ⭐ If something is genuinely wrong, say what it means for them in one
sentence and what you are doing about it.

---

## 4b · `bin/init` CHANGES FILES — say so before it becomes a question

⭐ **Right after the install, tell them this, in one short paragraph:**

> The setup wrote your name into the system's files, and created two of its own. Those changes are
> on your computer and nowhere else — nothing was sent anywhere.

⚠️ **Then, and only if they intend to keep using it, the save.** The word is `commit` and it is
theirs to hear explained, not to be asked about cold:

> **Saving a checkpoint.** This folder keeps a history of itself, so you can always see what
> changed and go back. Saving a checkpoint now means today's setup is recorded as a starting
> point. It stays on your computer — ⛔ it is not published anywhere and it does not reach whoever
> gave you this link.

⭐ **Then ask it as a chooser**, never as the bare word:

> **Question:** Do you want me to record this setup as a starting point?
>
> | Option | What it means |
> |---|---|
> | ⭐ **Yes, record it** *(recommended)* | Today's setup becomes the point you can always come back to |
> | **Not yet** | Nothing is recorded · you can ask for this at any time |

🔴 **Never ask this before explaining it**, and ⛔ never ask it of somebody who chose *"just tell
me more"* in §2 — they have not installed anything to record.

---

## 5 · THE FIRST THING THEY DO — one block, start to finish

⭐ **Ask what they want to build**, then run it yourself:

```bash
bin/new-block <short-name> --type docs --intent "<one sentence, theirs>"
```

⚠️ **It will not pass yet, and that is the design.** The block has two blanks only a human can
fill: what it MAY touch, and what it MUST NOT. ⭐ Ask them in plain words — *"which files should
I be allowed to change for this, and which are off limits?"* — write their answer into §B, and run
`bin/check-block`.

⛔ **Do not fill the boundary yourself.** It is the one thing the system exists to get from a
person, and an assistant that writes its own limits has written no limit at all.

---

## 5b · TELL THEM WHAT THEY CAN ASK FOR NEXT

⭐ **Once one block exists, show them these four sentences** — they are the whole interface:

> | Say this | And I will |
> |---|---|
> | *"where did we leave off?"* | read `memory/RESUME.md` — no guessing, no re-explaining |
> | *"what's still pending?"* | read `memory/PENDING.md` |
> | *"can we close this?"* | run the checks — ⛔ if they fail, it does not close, and I will say what is missing |
> | *"start something new"* | open another block, and ask you its boundary again |
> | ⭐ *"let's close the session"* | **write down where we got to, before this conversation resets and takes the reasoning with it** |

⭐ **Say the last one out loud to them, not just in the table.** ⚠️ It is the only one whose cost
is invisible until it is too late: the other four can be asked late and still work, and that one
cannot. ⛔ A person who never learns it loses the reasoning of every session and concludes the
system does not work.

⚠️ **Never hand them a command to type.** ⭐ They say the sentence, you run what it means — that is
the whole point of the system being on disk instead of in their head.

---

## 6 · WHAT NOT TO DO

| ⛔ | ⭐ Instead |
|---|---|
| paste the file tree at them | show §1 |
| explain blocks, campaigns and gates in detail up front | four rows, then their first block |
| say *"read QUICKSTART.md"* | ⚠️ that file is for a developer; this one is for them |
| ask *"shall we install it?"* | ⭐ they do not know what installing means — offer §2's three options |
| tell them to install Python | check it yourself in §3 |
| write the options as a paragraph | ⭐ present them as a chooser — they pick, they do not compose |
| ask twice for the same yes | ⛔ §2 already got it |
| ⭐ ask the SECOND question as prose | ⛔ every choice is a chooser, not only §2's — measured, one run got the first right and typed the rest |
| say `commit`, `branch`, `repo`, `hook` | ⭐ §4b explains the only one they need · ⛔ the rest they never need to hear |
| read the validator's findings aloud | ⭐ one sentence about what it means for them |
| ⭐ skip the session close | 🔴 §1 and §5b both carry it — it is the habit the whole system rests on |
| read `Mente/README.md` and work from it | ⚠️ that file is for a developer · ⛔ THIS file is the script |
| invent steps | ⛔ if it is not written here, say you do not know |

---

## 7 · WHO GOVERNS THIS FILE

| Change | Who |
|---|---|
| ⬜ the wording of §1, translated or adapted to an audience | ⭐ the owner — ⚠️ **what it names may not shrink**: the four pieces, both memory files, and the session close |
| §2's three options, and which one is recommended | whoever maintains the engine, through a recorded decision |
| ⛔ dropping the session close from §1 or §5b | **nobody** — ⭐ it is the one habit whose cost is invisible until the reasoning is already gone |
| ⛔ asking a choice as prose instead of a chooser | **nobody** — ⚠️ a person who does not know the system cannot compose an answer about it |
| ⛔ saying `commit` before §4b's explanation | **nobody** — 🔴 measured: it produced *"I do not understand why I should commit"* |

---

Related: `../rules/contract-document.md` (⭐ the type and ceiling this file declares) ·
`QUICKSTART.md` (the same install, written for a developer) ·
`README.md` (⛔ what an assistant fetches FIRST from a URL — it routes back here) ·
`CAPABILITIES.md` (every command).
