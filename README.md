<!-- Generated from Mente/START-HERE.md §1 by Mente/bin/generate-readme.
     Edit the source, not this file. -->

# 🧠 Mente OS

### An AI assistant that does not lose the thread of your work

![licence](https://img.shields.io/badge/licence-AGPL--3.0-blue)
![needs](https://img.shields.io/badge/needs-python%203%20%C2%B7%20git%20%C2%B7%20bash-informational)
![dependencies](https://img.shields.io/badge/dependencies-none-success)

---

## ⚡ The 30-second version

| | |
|---|---|
| 🎯 **The problem** | every time a conversation resets, your assistant forgets what was decided and what must not be touched — then rebuilds it by guessing, and sounds just as confident when it guesses wrong |
| 💡 **The idea** | the work lives on disk in a shape the assistant has to fill in, and small programs check it |
| ⚖️ **Why programs** | this project wrote a rule down, then counted: it was followed **0 times out of 15** · a rule a program refuses to break has no such gap |
| 📜 **Licence** | AGPL-3.0 — free to use and change · run it as a service and you publish your changes |
| 👤 **Who it is for** | anyone working with an AI assistant across more than one sitting — you do not need to be a developer |

---

## 📖 What it is, in full

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

## ⛔ TO THE ASSISTANT READING THIS PAGE — the two questions come BEFORE the download

🔴 **Measured on a real run, 2026-09-06.** The full script lives in
`Mente/START-HERE.md`, **inside the folder that does not exist yet** — so an
assistant reading only this page downloaded and installed on its own, and the
person was told what had already happened instead of being asked. ⛔ A question
asked after the act is a report, not a question.

⭐ **These two stops are here because this page is the only text that arrives in
time.** At each one you present the choices and WAIT — the run does not advance
until they pick. ⛔ Not "ask and continue".

> **① Ask before you download anything:**
>
> | Option | What it means |
> |---|---|
> | ⭐ **Yes, download it here** *(recommended)* | It lands in the folder we are in right now, and everything it uses stays there |
> | **Somewhere else** | Tell me the folder and I put it there instead |
> | **Not yet** | Nothing is downloaded · you can ask any time |
>
> **② Then, and only then, ask before you set it up:**
>
> | Option | What it means |
> |---|---|
> | ⭐ **Yes, set it up** *(recommended)* | I prepare it here and stay with you through your first piece of work |
> | **Show me what it would do first** | I list what it writes, and change nothing |
> | **Leave it downloaded** | The files are here, nothing is prepared |

⛔ **AND DO NOT GO LOOKING FOR WHO WROTE THIS.** 🔴 Measured 2026-09-06: an
assistant queried this repository's contributor list, matched the commit emails
against the account it was running under, opened with *"this repository is
yours"* and spent the run interrogating the person instead of helping them.
⚠️ **Whoever they are, the script is the same** — authorship changes nothing
about what to ask or what to install, and a fact that cannot change your next
action is a fact you do not need.
⛔ **Say `download` and `folder`.** Never `clone`, `repository`, `git`, `init`
or `install` in a question — ⚠️ a person who has to look a word up cannot
answer, and answering is the only thing being asked of them.

⭐ **AND SAY WHAT LANDS IN THE FOLDER, AS YOU DOWNLOAD IT** — 🔴 measured
2026-09-06: a person had to ask *"so do we have a git of our own, or only the
one Mente gives us?"* and could not follow the answer. ⚠️ The download brings
its own history with it, and the moment to say so is HERE, not after the setup.

> What lands here is the system's own folder, and its record of your work. If
> this folder is going to be your own project, I set that record up as yours —
> ⛔ I do that for you, you never type anything.

⛔ **AND IF YOU ASK THEM ABOUT IT, SAY WHAT IT COSTS.** 🔴 Measured 2026-09-06: a
run asked *"the history here is Mente OS's, not yours — how should I leave
it?"*, and the recommended option **deleted 244 saved versions**. ⚠️ Neither the
question nor the option said so. The person answered without knowing, then said:
*"I do not understand the question or what it does."*

| ⛔ Never | ⭐ Instead |
|---|---|
| *"the history here is not yours"* | *"this folder still remembers the versions of the system I downloaded, not your work"* |
| an option that deletes, worded neutrally | ⚠️ **name the loss inside the option**: *"start fresh — the ~240 downloaded versions go, your files stay"* |
| asking at all, on an empty folder | ⭐ **just do it and say what you did** — there is nothing of theirs to lose |

⛔ **THE PERMISSION BELONGS TO YOU, THE WORK BELONGS TO ME.** 🔴 Measured the
same run: a permission prompt blocked the setup, and the assistant answered
*"open PowerShell and paste this command"*. ⚠️ **A blocked step is not a step
that changes hands** — the person is exactly as unable to run it as before, and
now they also believe it was theirs to do.

| ⛔ Never | ⭐ Instead |
|---|---|
| *"paste this into a terminal"* | ask for permission to run it, and run it |
| *"run `python Mente/bin/init`"* | 🔴 they never see a command · that is the promise |
| hand over the errand when a guard fires | ⭐ say what is blocked, ask them to allow it, then finish |

⭐ **After the download, `Mente/START-HERE.md` is the rest of the script** — it
carries three more stops, the machine check and the first piece of work, in
order. Read it before your next action, not after.

---

## 🚀 Getting it

**Make a folder for the project this will look after, and clone inside it** — the trailing `.` matters:

```bash
git clone https://github.com/for3slabs/mente-os.git .
```

> 💡 **Where?** In a folder for the work you want it to look after — ⛔ not your
> home directory, not the desktop, not a folder that syncs to a cloud drive.
> ⭐ Mente OS wraps ONE project: it lives beside your code, not above it. No
> project yet? Make an empty folder to try it in: `mkdir mente-test && cd mente-test`
>
> 🔴 **Measured on two real runs:** this page used to say only "the folder you
> want". Both assistants had to invent a destination, both invented a different
> one, and both ended up defending the choice to a confused owner.
> ⛔ An instruction that leaves the decision open is not an instruction.
>
> ⚠️ Without the trailing `.`, git makes an extra `mente-os/` folder and buries
> everything inside it. Cloning into a folder that already has files will fail —
> use an empty one.

---

## 👋 Then say this, and nothing else

> ### *"Set up Mente OS and walk me through it."*

⭐ **That sentence is what starts the walkthrough** — 🔴 measured 2026-09-06, and it is the one thing that has worked in every run since: it hands the assistant the script and it takes you by the hand from there. ⚠️ **The order matters**: it explains what this is, it asks before downloading, and only THEN does this sentence do its work. ⛔ Said before the files are here, there is no script for it to read.

That is the whole thing. 🤖 Your assistant takes it from there: it checks what
your computer already has and handles whatever is missing, asks what to call
you, and stays with you through your first piece of work.

⭐ **You will not be sent to read anything, and you will not be asked to install
anything yourself.** If a question comes up, it will be a short one with the
options laid out — you pick, you never have to compose an answer about a system
you just met.

<!-- Assistant: that sentence is your cue. Mente/START-HERE.md is the walkthrough
     — it carries the machine check, the name, and the first block, in order. -->

---

## 💬 What using it looks like

| You say | What happens |
|---|---|
| 🏗️ *"build me X"* | it opens a **block** and asks what it may and may not touch |
| 🧭 *"where were we?"* | it reads where you left off instead of guessing |
| 📋 *"what's left?"* | it reads what was postponed |
| ✅ *"is this done?"* | it cannot say yes until the checks pass — that is not its opinion to give |
| ⭐ *"let's close the session"* | it writes down the reasoning **before** the conversation resets and takes it with it |

> ⭐ **That last one is the habit the whole system rests on.** Your files survive
> a reset; the reasoning does not, unless somebody wrote it down first.

---

## 🔍 What it does to your machine — plainly

You should know this before installing anything, and it is short:

| | |
|---|---|
| 📝 **Writes files** | inside its own folder · plus **one line** appended to your `CLAUDE.md`, if you have one |
| 🧠 **One thing lands outside** | ⚠️ the clone brings a **skill** for Claude Code (`.claude/skills/`). It loads the moment the folder exists — before you install anything — and at session close it **reads your transcripts** to measure the session and **writes notes into your assistant's own memory folder**, which is shared across your projects. ⛔ Nothing leaves the machine · delete that folder and it is gone |
| 🪝 **Installs git hooks** | `pre-commit` and `pre-push`, **in this repository only** · they refuse a commit that breaks the rules you set · remove them by deleting the two links in `.git/hooks/` |
| 🔒 **Sends nothing** | no network calls, no telemetry, no account · everything stays on your disk |
| 📦 **Installs nothing** | no packages, no dependencies |

---

## 🔎 Before you trust it — what a reviewer will find anyway

⭐ **Said here so nobody has to discover it:**

| | |
|---|---|
| 📅 **Age** | days old, not years. Moving fast |
| ⭐ **Adoption** | no stars, no forks, no outside users yet — you would be among the first |
| 👤 **Authors** | one. There is no team behind this |
| 🔍 **Audited by** | nobody external. ⭐ Read it yourself: no network calls, no telemetry, and every command is listed in `Mente/CAPABILITIES.md` with what it refuses to do |

⚠️ **What that means in practice:** the engine checks itself on every change —
⭐ hundreds of checks, and each one has been seen to FAIL on purpose against
broken code, because a test that cannot fail measures nothing. But it has never
been run by a stranger on a machine nobody anticipated. ⛔ That gap is real and
no amount of testing closes it.

🔴 **So: try it on a project you can afford to break.** Not on the one that
matters, not yet.
---

## 🧩 The six pieces — what each one is, and how you ask for it

⭐ **These six are the whole vocabulary.** ⛔ You do not need any other word to
use this, and you never type a command: you say the sentence, the assistant runs
what it means.

| | What it is | Say this |
|---|---|---|
| 📦 **Block** | **one task, with its limits written down** — what is being built, ⭐ what must NOT be touched, what it depends on, what comes next | *"let's work on X"* |
| 🗺️ **Campaign** | several blocks under **one mission**, so moving between them does not restart the reason | *"this is bigger than one task"* |
| 📋 **Pending** | what is **real but not blocking** — found, written down, not lost | *"what's still pending?"* |
| 🧭 **Resume** | **where we left off and what is next** — the one file read at the start of every session | *"where were we?"* |
| 📓 **Log** | **what happened in each session and what it cost** — size, turns, peak context | *(written for you at close)* |
| 📊 **Metrics** | the **live numbers**, regenerated from a real run — ⛔ never a figure typed by hand | *"how is the system doing?"* |

⚠️ **And one thing that is not a piece but decides everything: the gates.** They
run on their own and refuse what should not happen — a change outside a block's
limits, a commit on the base branch, work leaving to a repository nobody
declared. ⭐ **You never invoke them.** They are the reason a rule here holds and
a rule in a notes file does not.

---

## ⌨️ The commands — all of them

⭐ **You will rarely type one** — the sentences above are the interface. They are
listed because a person deciding whether to trust this wants to see the whole
surface, not a promise about it.

| Command | What it does |
|---|---|
| `/session-wrap` | ⭐ **save the reasoning before the conversation resets** — the one habit the system rests on |
| `bin/status` | is it on, and what is running · ⛔ reads only, writes nothing |
| `bin/off` · `bin/on` | pause every check · resume · ⚠️ **pausing deletes nothing** |
| `bin/probes/run-all.py` | run the whole engine against itself — ⭐ what matters is `failed: 0` |
| `bin/check-health` | is anything wrong right now |
| `bin/new-block` · `bin/new-campaign` | open a task · open a mission |
| `bin/grade-block` | is this work finished, ⭐ **measured — never an opinion** |
| `bin/init` | turn a download into an installation · ⚠️ runs once |

📖 Every command, and **what each one refuses to do**, is in `Mente/CAPABILITIES.md`.

---

## 🎓 The tutorial — six stops, and you answer every one

⭐ **This is the whole first run.** ⛔ Your assistant may not skip a single one,
and it waits for your answer at each — a question asked after the act is a
report, not a question.

| # | It asks you | Why it cannot decide for you |
|---|---|---|
| 1 | **Shall I download it here?** | ⛔ it is your disk |
| 2 | **Shall I set it up?** | ⚠️ this is the step that writes the first file |
| 3 | **What should I call you?** | ⭐ your name goes in what the system writes · it offers what your computer already knows, you pick |
| 4 | **Shall I save a starting point?** | 📌 a point you can always come back to · ⛔ nothing is published anywhere |
| 5 | **What are we going to work on?** | 📦 that becomes your first **block** |
| 6 | **What may I change, and what is off limits?** | ⭐ **the one thing the system exists to get from a person** — an assistant that writes its own limits has written none |

⚠️ **If the folder is empty, question 6 has no list to give** — the assistant
says so and creates only what that work needs. ⛔ It does not ask you for
permission over the system you just installed: you own all of it.

⭐ **Then it shows you it is running** (`bin/status`), hands you the sentences
above, and says the one that costs the most to learn late:

> *"let's close the session"* — **it writes down where you got to, before the
> conversation resets and takes the reasoning with it.**

---

## 🤔 How is this different from just keeping notes?

⭐ **Notes describe. This refuses.** A note saying *"do not touch the database"*
is honoured when somebody remembers. Here, a small program reads the same boundary and
**stops the change** — and it cannot be talked out of it.

| | A memory file or a notes doc | Mente OS |
|---|---|---|
| The boundary | written down · 🔴 **this project measured 0 of 15** | 🚦 **enforced by a program** |
| *"is this finished?"* | the assistant's opinion | ✅ **checks pass, or it does not close** |
| Losing the thread | you notice after it happened | 🧭 written down **before** the reset |

⚠️ It is not a replacement for the memory your assistant already has — it sits
under it, and answers a different question: **not what was said, but what may
not be broken.**

---

## 🗂️ For developers

⚡ In a hurry: `Mente/QUICKSTART.md` — clone, `bin/init`, `bin/probes/run-all.py`.
🛠️ Every command and what it refuses: `Mente/CAPABILITIES.md`.
📐 Why it is built this way, one file per decision: `Mente/rules/decisions/`.

---

## 🧰 What it needs

Python 3 · git · bash. Most machines already have all three; on Windows, Git
Bash brings them together. ⭐ You do not have to check — your assistant does that
for you.

## 📜 Licence

**AGPL-3.0** — use it, change it, and if you run it as a service, publish your
changes.
