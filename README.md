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
| ⚖️ **Why programs** | a rule written in a document is followed about half the time · a rule a program refuses to break is followed every time |
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

## 🚀 Getting it

**Clone it into the folder you want it in** — the trailing `.` matters:

```bash
git clone https://github.com/for3slabs/mente-os.git .
```

> 💡 **Already standing in the folder you want?** That command puts it right
> there. **Starting from scratch?** Make the folder first, then run it inside:
> `mkdir my-project && cd my-project`
>
> ⚠️ Without the trailing `.`, git makes an extra `mente-os/` folder and buries
> everything inside it. Cloning into a folder that already has files will fail —
> use an empty one.

---

## 👋 Then say this, and nothing else

> ### *"Set up Mente OS and walk me through it."*

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
| 🪝 **Installs git hooks** | `pre-commit` and `pre-push`, **in this repository only** · they refuse a commit that breaks the rules you set · remove them by deleting the two links in `.git/hooks/` |
| 🔒 **Sends nothing** | no network calls, no telemetry, no account · everything stays on your disk |
| 📦 **Installs nothing** | no packages, no dependencies |

---

## 🧩 The four pieces

| | |
|---|---|
| 📦 **Block** | one unit of work — what is being built, ⭐ **what must NOT be touched**, what it depends on, what comes next |
| 🗺️ **Campaign** | several blocks under one mission, so switching between them does not restart the reason |
| 🚦 **Gates** | they run on their own and stop what should not happen — a destructive change with no way back, closing work that is not finished |
| 🧠 **Memory** | where you left off, and what is postponed — ⭐ you never write either by hand |

---

## 🤔 How is this different from just keeping notes?

⭐ **Notes describe. This refuses.** A note saying *"do not touch the database"*
is read about half the time. Here, a small program reads the same boundary and
**stops the change** — and it cannot be talked out of it.

| | A memory file or a notes doc | Mente OS |
|---|---|---|
| The boundary | written down, honoured when remembered | 🚦 **enforced by a program** |
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
