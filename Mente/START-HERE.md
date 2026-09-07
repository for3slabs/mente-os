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

### ⛔ WHO THEY ARE IS NOT YOUR ERRAND — do not go looking

🔴 **Measured 2026-09-06.** An assistant handed only the link queried the GitHub
API for the repository's contributors, cross-referenced the commit emails
against the session's own account, and opened with *"this repository is yours"*
— ⛔ then spent the rest of the run asking the person to explain why they had
said somebody recommended it. ⚠️ **The errand was abandoned for an
investigation nobody asked for.**

⛔ **Never look up who wrote this, who owns it, or whether the person in front of
you appears in its history.** Not the contributor list, not the commit authors,
not the account behind the session. ⭐ Whoever they are, **the script is the
same** — and a run that changes because of who it thinks it is talking to is a
run that stopped following it.

⚠️ **This is not about privacy.** It is about the errand: ⭐ authorship changes
nothing about what to ask, in what order, or what to install. ⛔ A fact that
cannot change your next action is a fact you do not need.

| ⛔ Never | ⭐ Instead |
|---|---|
| query the repo's contributors or commit authors | ⚠️ read what the page SAYS about itself — §1 |
| match their account against the history | ⛔ nothing in the run depends on the answer |
| *"you are the second contributor"* | 🔴 say nothing · it is not part of the errand |
| treat a familiar name as a reason to skip a question | ⭐ every stop is asked of everybody |

⭐ **AND READ NOTHING ABOUT THEM UNTIL THE MOMENT YOU NEED IT.** 🔴 The same run
read `git config user.name` early, and by the time the name question arrived it
already "knew" the answer — ⛔ so it never asked, and passed the name straight
to the installer. ⚠️ **A value you are holding stops feeling like a question.**
§4 reads those candidates **at the moment it asks**, never before.

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
| *"what name should I use?"* | ⭐ §4 reads two real ones off the machine — it is a chooser too |

⛔ **THERE IS NO EXCEPTION.** ⚠️ This file used to grant one, for the name, on the grounds that a
blank has no options — and that single exception is the one question the person kept receiving as
plain text, in run after run. 🔴 It was wrong twice over: `git config user.name` and `whoami` are
two real candidates, and *"something else"* is the third.

⭐ **When a question looks optionless, LOOK HARDER before dropping to prose.** The machine usually
knows the answers already, and reading them is your job, not theirs. ⚠️ Only if that search comes
back empty do you ask as a sentence — a chooser with one option is refused by the tool and the
person never sees it.

### ⚠️ SOMETHING UNRELATED YOU NOTICE: SAY IT, THEN FINISH THE ERRAND

⭐ **Tell them what you found. It is their machine and their right to know** —
🔴 an earlier version of this file said not to, and it was wrong: a document
telling an assistant to withhold something from its own user is indefensible,
and the assistant that refused to follow it was right to refuse.

⛔ **What is NOT yours to do is hand them the decision, or abandon what they
asked for.**

🔴 **Measured 2026-09-05 on a real Windows run.** The assistant noticed a `git
init` at the wrong level in the user's home folder, reported it, investigated it
across four commands, and asked the person what to do about it. ⚠️ **The install
never happened.** They answered: *"what is that and why are you asking ME? isn't
it automatic? I'm new."*

⭐ **That question is the failure, and it is not about mentioning it.** A person
who asked what something is cannot decide what to do about a repository layout —
they do not have the words yet. ⛔ Being asked teaches them this system hands
them problems they did not bring.

| | ⭐ What you do |
|---|---|
| **Say it** | one or two sentences · what it is, whether it is urgent, and that it is **separate from what we are doing** |
| **Offer, do not ask** | *"I can look at that after we finish setting this up, if you want"* — ⛔ never a question they must answer to continue |
| **Then continue** | ⚠️ an interrupted install is a person who never got to use this |
| ⛔ **Do not investigate it** | four commands into an unrelated repository are four commands not spent on what they asked for |

⚠️ **The exception:** if what you found means continuing could destroy their
work, stop and say so plainly. ⭐ That is not a detour — that is the errand.

### ⛔ THE FIVE STOPS — you may not pass one without an answer

🔴 **Measured on a real run, and it is the complaint that keeps coming back.**
The assistant cloned, then installed, then asked. Each step was reasonable on
its own and the person never got to decide any of them — they were told what
had already happened. ⛔ A question asked after the act is a report, not a
question.

⭐ **These five are STOPS. At each one you present the chooser and WAIT.** ⛔ Not
"ask and continue" — the run does not advance until they pick.

| # | The stop | Ask before |
|---|---|---|
| 1 | what they want to do at all | touching anything |
| 2 | **may I download it here** | ⛔ before the clone |
| 3 | **may I set it up** | ⛔ before the first file is written |
| 4 | what to call them | ⛔ before the name enters 78 documents |
| 5 | shall I save a starting point | ⛔ before anything is recorded |

⚠️ **AND EVERY ONE IN PLAIN WORDS.** 🔴 The same run asked stop 4 like this:

> *"The engine writes it in `mente.config.yml` and in all generated
> documentation. I do not invent it — `init` itself warns that an assistant
> already got this wrong."*

⛔ Every word of that is for a developer. The person was asked to approve a
system they cannot picture. ⭐ Same question, their language:

> *"What should I call you? It goes in the notes the system keeps, and you can
> change it later."*

⛔ **Never inside a question:** `bin/init` · `.git` · `mente.config.yml` ·
`settings.json` · `hooks` · `repository` · `validator`. ⭐ Say what it DOES for them,
never what it is called.

| ⛔ Never ask | ⭐ Ask this instead |
|---|---|
| "shall I run `bin/init`?" | *"shall I set it up?"* |
| "this folder is not a `git` repository" | *"the system keeps its own history of your work, here in this folder"* |
| "I will wire the hooks into `.git/hooks`" | *"it will check your work before saving it"* |
| "it writes `mente.config.yml`" | *"it remembers your name"* |

⭐ **AND SAY WHERE IT LANDS, IN THEIR WORDS.** ⚠️ A person may have several
installations. They do not need to know what a repository is — they need to
know **this one lives in this folder, and only here**: *"everything the system
sets up stays in this folder. Delete the folder and it is all gone. If you set
it up again somewhere else, that one is separate and neither knows about the
other."*

### ⭐ NEVER USE A WORD THEY DID NOT ASK FOR

⛔ `commit` · `branch` · `merge` · `repo` · `hook` · `validator` · `probe` · `placeholder`.

🔴 **Measured on the same run:** the assistant asked *"shall I commit these initialisation
changes?"* to somebody who had asked what Mente OS was twenty minutes earlier. ⚠️ Their reply was
*"where are you going to commit them, I do not understand why I should commit."*

⭐ **If a step genuinely needs one of those words, explain it in one sentence FIRST, in their
terms, then ask.** §4b is the one for `commit`, written out. ⛔ If no such explanation exists in
this file, the step is not one to raise with them at all.

---

## 0 · ⛔ DO NOT LOOK AROUND — everything lives in this folder

⭐ **Mente OS is contained.** Everything it writes — the engine, the config, the
skill, the gate wiring, the git hooks — lands inside the folder it was cloned
into. ⛔ Delete that folder and it is gone: no registry entry, no file in the
home directory, nothing left behind.

⚠️ **So there is nothing to hunt for, and hunting is itself the failure.**
🔴 Measured 2026-09-06 on two real runs: this section used to open by telling
you to go looking for leftovers from an earlier attempt, and it said "two
things live OUTSIDE this folder". ⛔ That taught the assistant that Mente OS
leaves traces elsewhere — so it started reporting other folders on the machine,
and the person ended up distrusting a system that had touched nothing.

⭐ **A person can have a hundred installations in a hundred folders.** None of
them sees the others. That is the promise, and inspecting the disk to "check"
is what breaks it.

| | |
|---|---|
| ⛔ **Do not** | scan the home directory, list other projects, or report what you notice elsewhere |
| ⛔ **Do not** | read or edit their `CLAUDE.md` looking for old imports |
| ⭐ **Do** | go straight to §1 |

⚠️ **The one exception, and only if THEY raise it:** somebody who used a version
from before 2026-09-06 may have a stale `@Mente/CLAUDE-MENTE-OS.md` line in a
`CLAUDE.md` whose folder is gone. ⛔ That is theirs to remove and theirs to
mention first — you do not go looking for it.

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
> programs check it. This project wrote a rule down and then counted: it was followed **0 times
> out of 15**. A rule a program refuses to break has no such gap.
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

### ⛔ STOP 2 · before downloading it — ask, and WAIT

⚠️ **Only if it is not already on their disk.** If they are standing in the
folder and the files are there, skip to stop 3 and say you skipped it.

> **Question:** Shall I download Mente OS into this folder?
>
> | Option | What it means |
> |---|---|
> | ⭐ **Yes, here** *(recommended)* | It lands in the folder we are in right now. Everything it uses stays here |
> | **Somewhere else** | Tell me the folder and I put it there instead |
> | **Not yet** | Nothing is downloaded · you can ask any time |

⭐ **Name the folder out loud in the question** so they see where it goes.
⛔ Do not say "clone" or "repository" — say **download** and **folder**.

---

### ⛔ STOP 3 · before writing the first file — ask, and WAIT

> **Question:** Shall I set it up now?
>
> | Option | What it means |
> |---|---|
> | ⭐ **Yes, set it up** *(recommended)* | I check what your computer already has, prepare the system here, and stay with you through your first piece of work |
> | **Tell me what changes first** | I list exactly what appears on your computer, and you decide after |
> | **Not yet** | Nothing is written · the files just sit there |

⛔ **Never ask this as "shall I run `bin/init`".** 🔴 Measured: the person does
not know what that is, and being asked to approve a command they cannot read is
how a first contact turns into homework.

⭐ **If they pick "tell me what changes first", say it like this** — no paths, no
file names:

> *It prepares its own folder here, remembers your name, and starts checking
> your work before it gets saved. Everything stays in this folder — nothing is
> sent anywhere, and nothing is installed on your computer.*

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

⭐ **If it is not cloned yet, clone it INTO THE FOLDER THEY ARE IN** — ⛔ never
into a subfolder of its own. 🔴 Measured on a real run: plain `git clone <url>`
made a `mente-os/` folder and put everything inside it, so the person got a folder
they never asked for wrapping the one they made.

```bash
git clone https://github.com/for3slabs/mente-os.git .
```

⚠️ **If git refuses because the folder is not empty**, clone into a new empty one
and tell them where it went. ⛔ Never delete anything to make room.

```bash
cd Mente
bin/init --owner "<their name>"
bin/probes/run-all.py
```

### ⭐ THE NAME IS A CHOOSER TOO — find the options before you ask

⚠️ **`bin/init` refuses to guess a name, and so must you.**

🔴 **MEASURED 2026-09-05, and it is the failure this section exists for.** An
assistant ran `bin/init` without a terminal, hit the refusal, read the hint —
and **invented the name from the folder it was standing in**. It installed with
that name in 78 documents and never told the person. They found out later and
asked: *"wasn't it supposed to ask me my name?"*

⛔ **The folder name is not their name. Neither is the account, nor the git
config on its own.** ⭐ Those are CANDIDATES to offer — the answer is theirs.

⛔ But *"refuses to guess"* is not *"ask them to type it"*: **the machine already
knows real candidates.** Read them first:

```bash
git config user.name ; whoami
```

⭐ **Then ask with those as the options**, the git name first — it is what they already chose to
be called on this machine:

> **Question:** What should I call you?
>
> | Option | What it means |
> |---|---|
> | ⭐ **<the git name>** *(recommended)* | What you already use for your work on this computer |
> | **<the account name>** | Your user account on this machine |
> | **Something else** | Type any name — it goes in the notes the system keeps for you, and you can change it later |

⛔ **ASK IT WITH THOSE WORDS.** 🔴 Measured on a real run: the wording was
rewritten into *"the engine writes it in `mente.config.yml` and in all generated
documentation"* — ⚠️ a person cannot approve a system they cannot picture, and
every term in that sentence is one they never asked to learn.

🔴 **Measured twice, 2026-09-02, and it is the complaint that keeps coming back.** Both runs asked
§2 as a proper floating chooser and then typed THIS one as plain prose, because this file used to
say it could not be a chooser. ⛔ It can: two real candidates plus an escape hatch is three
options.

⚠️ **If both commands come back empty**, then and only then ask it as a sentence — a chooser with
one option is refused by the tool and the person never sees it.

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

⭐ **And say WHERE it all lives, in one sentence** — 🔴 measured 2026-09-06: a run explained the
history without ever saying it was per-folder, and the person could not tell whether the system
had reached the rest of their machine.

> Everything the system uses lives in **this folder** — its files, its history of your work, and
> the checks it runs. ⛔ Delete the folder and all of it is gone. ⭐ If you set it up somewhere
> else too, that one is separate: neither knows the other exists.

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

## 4c · ⛔ SHOW THEM IT IS ON — the install is invisible until you say what it can do

🔴 **Measured 2026-09-06, and it is the complaint underneath every other one:**
*"it installs but it does not seem installed — no metrics, no commands, nothing.
I do not know if it is working or not."* ⚠️ The install printed a report once and
then the system was indistinguishable from not being there.

⛔ **A person who cannot see the system running does not delegate work to it.**
They keep doing it themselves, which is the outcome the whole engine exists to
prevent.

⭐ **So do this immediately after the setup, before anything else:**

```bash
bin/status
```

⭐ **Show them its output and read it out loud with them.** It answers, in their
words, whether it is on and what is running. ⛔ Do not summarise it — the point
is that they see the system answer for itself.

### ⭐ THEN GIVE THEM THE WHOLE INTERFACE — all of it, once

⛔ **Not later, and not only if a block gets opened.** 🔴 These sentences used to
live behind the first block, so a run that never opened one taught the person
nothing — and that run happened.

> | Say this | And I will |
> |---|---|
> | ⭐ *"is Mente OS on?"* | run `bin/status` — what is running, in plain words |
> | *"turn Mente OS off"* / *"turn it back on"* | pause the checks · ⛔ nothing is deleted |
> | *"where did we leave off?"* | read where we stopped — no guessing, no re-explaining |
> | *"what's still pending?"* | read what was postponed |
> | *"build me X"* / *"help me with X"* | open a piece of work and ask what it may touch |
> | *"is this done?"* | run the checks — ⛔ if they fail it does not close, and I say what is missing |
> | ⭐ *"let's close the session"* | **write down where we got to, before this conversation resets** |

⚠️ **Say the last one OUT LOUD, not just in the table.** ⛔ It is the only one
whose cost is invisible until too late: the other six can be asked late and
still work. A person who never learns it loses the reasoning of every session
and concludes the system does not work.

⚠️ **Say `off` PAUSES and that nothing is deleted.** ⭐ The difference is the whole
reason the switch exists: a person who believes stopping it costs their work will
not stop it, and will not trust it either.

⛔ **Never hand them a command to type — they never see a command.** ⭐ They say the
sentence, you run what it means: that is the whole point of the system being on disk
instead of in their head.

---

### ⛔ A BLOCKED STEP IS NOT A STEP THAT CHANGES HANDS

🔴 **Measured 2026-09-06.** A permission guard refused the setup, and the run answered
*"open PowerShell and paste this command"*. ⚠️ The person was exactly as unable to run it as
before — and now also believed it was theirs to do.

⭐ **Say what is blocked, ask them to allow it, then finish the errand.**

| ⛔ Never | ⭐ Instead |
|---|---|
| *"paste this into a terminal"* | *"I need your permission to run the setup — may I?"* |
| *"run `python Mente/bin/init`"* | 🔴 they never see a command |
| *"you can do it yourself with…"* | ⭐ the errand stays yours until it is done or refused |

---

## 5 · THE FIRST THING THEY DO — one block, start to finish

🔴 **THE INSTALL IS NOT THE DELIVERY — measured 2026-09-06.** A full run installed
cleanly, the person then asked for a real piece of work, and the assistant wrote it to a
loose file at the top of the folder: ⛔ **no block, `RESUME.md` and `PENDING.md` still the
shipped templates, nothing recorded.** ⚠️ Every check was green and the system had held
nothing. **A green battery over an empty `work/` measures the engine, not the promise.**

⛔ **THE FOUR TYPES ARE NOT A JUDGEMENT ABOUT THE SUBJECT.** The same run read
`--type code|docs|infra|data`, decided a personal plan "did not fit a system for software",
and opted out. ⭐ **`docs` is anything whose product is a written document** — a plan, a
guide, notes, a decision record. ⚠️ The type names the SHAPE OF THE WORK, never the topic,
and there is no subject this engine declines to hold.

⭐ **Ask what they want to build**, then run it yourself:

```bash
bin/new-block <short-name> --type docs --intent "<one sentence, theirs>"
```

⚠️ **It will not pass yet, and that is the design.** The block has two blanks only a human can
fill: what it MAY touch, and what it MUST NOT.

### ⛔ THE BOUNDARY IS ABOUT WHAT WAS ALREADY THERE — never about the engine

🔴 **Measured 2026-09-06.** The question was asked of an owner standing in an empty folder they
had just installed into, and the options offered included *"do not touch Mente OS or its
configuration"*. ⛔ **The question and the situation did not match**, and the owner said so: they
installed it, they own all of it, and being asked for permission over their own tool reads as the
system not knowing where it is.

⭐ **What the boundary protects is work that EXISTED BEFORE this block** — their code, their
documents, a database, a live service. ⛔ **Never the engine, and never files this block is about
to create.** The owner governs the whole folder; the boundary exists so one piece of work does not
reach into another.

| Situation | ⭐ Ask |
|---|---|
| a folder with their existing work in it | *"which of your files may I change for this, and which are off limits?"* |
| ⭐ **an empty folder, or one holding only the install** | ⛔ **do not ask for a list.** Say: *"there is nothing else here yet, so I will only create the files for this work"* — write that into §B and move on |
| a second block beside an existing one | *"may I touch what the other piece of work produced?"* |

⚠️ **A question whose only honest answer is "all of it, it is mine" is a question that should not
have been asked.** ⭐ Look at the folder first: if the boundary is derivable from what is there,
state it and let them correct you — ⛔ that is not the same as inventing a limit.

### ⭐ AND SAY WHERE THE WORK ITSELF WILL LAND — before writing it

🔴 **Measured the same run.** The material was written to the repository root, the owner caught
it, and the second attempt put it beside `BLOCK.md` — where `BLK-SHP-001` refused it. ⛔ **Two
wrong places before the right one, because this script named where the RECORD goes and never
where the PRODUCT goes.**

| What | Where | Why |
|---|---|---|
| ⭐ the record — how the work is going | `work/blocks/active/<id>/BLOCK.md` | ⛔ **one file, alone.** `BLK-SHP-001` refuses a sibling document beside it |
| ⭐ **the product — what is actually being made** | `Cerebro/<name>/` | it is the only folder about THEIR project rather than the engine |
| ⛔ never | the repository root | ⚠️ outside `Mente/` nothing governs it — measured, and the owner is the one who noticed |

⭐ **Then declare each produced file in `Mente/pieces.tsv`.** ⚠️ Being inside `Mente/` is not the
same as being governed: without a declared row, `bin/check-structure` goes silent when the file
disappears.

⭐ Ask them in plain words — *"which files should I be allowed to change for this, and which are
off limits?"* — write their answer into §B, and run `bin/check-block`.

⛔ **Do not fill the boundary yourself.** It is the one thing the system exists to get from a
person, and an assistant that writes its own limits has written no limit at all.

---

## 5b · ⭐ REMIND THEM OF ONE SENTENCE — the rest was given in §4c

⛔ **The interface is NOT taught here.** 🔴 It used to be, opening with *"once one block
exists"* — so a run that never opened a block taught the person nothing, and that run happened.
⭐ It moved to **§4c**, right after the setup, where it is reached whatever they choose next.

⭐ **What belongs here is one sentence, said out loud now that there is work to lose:**

> *"let's close the session"* — **I write down where we got to, before this conversation resets
> and takes the reasoning with it.**

⚠️ It is the only one whose cost is invisible until too late: the others can be asked late and
still work. ⛔ A person who never learns it loses the reasoning of every session and concludes
the system does not work.

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
| ⭐ hand them a command when a guard blocks you | ⛔ ask for permission and finish it · the errand never changes hands |
| ⭐ look up who wrote this or who they are | ⛔ the script is the same for everybody |
| ⭐ write their work to a loose file | ⛔ it goes in a block — §5 · a file outside `work/` is not held by anything |
| ⭐ decide their subject "does not fit" | ⛔ `docs` holds any written work · the type is the SHAPE, never the topic |
| say `commit`, `branch`, `repo`, `hook` | ⭐ §4b explains the only one they need · ⛔ the rest they never need to hear |
| read the validator's findings aloud | ⭐ one sentence about what it means for them |
| ⭐ skip the session close | 🔴 §1 and §5b both carry it — it is the habit the whole system rests on |
| read `Mente/README.md` and work from it | ⚠️ that file is for a developer · ⛔ THIS file is the script |
| ⭐ report what you notice on their machine | ⛔ you were asked what this project is · 🔴 measured: it cost the whole install |
| ⭐ ask them to decide something technical | ⛔ they are new · that is what they came here to avoid |
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
| ⛔ raising an unrelated finding during the first run | **nobody** — 🔴 measured: it produced *"why are you asking ME? I'm new"* and the install never happened |

---

Related: `../rules/contract-document.md` (⭐ the type and ceiling this file declares) ·
`QUICKSTART.md` (the same install, written for a developer) ·
`README.md` (⛔ what an assistant fetches FIRST from a URL — it routes back here) ·
`CAPABILITIES.md` (every command).
