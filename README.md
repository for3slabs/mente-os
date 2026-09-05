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

## 🚀 Getting started

**1 · Make a folder for it, and clone into that folder**

```bash
mkdir mente-os && cd mente-os
git clone https://github.com/for3slabs/mente-os.git .
```

> 💡 The trailing `.` clones into the folder you just made instead of creating
> another one inside it. Cloning into a folder that already has files in it will
> fail — use an empty one.

**2 · Set it up**

```bash
cd Mente
bin/init                  # asks who you are · writes nothing until you answer
bin/probes/run-all.py     # the engine checking itself · expect 0 failures
```

**3 · Then just talk to your assistant**

You do not learn commands. 📄 `Mente/START-HERE.md` is a walkthrough written for
an assistant to follow with you the first time — point yours at it.

---

## 💬 What using it looks like

| You say | What happens |
|---|---|
| 🏗️ *"build me X"* | it opens a **block** and asks what it may and may not touch |
| 🧭 *"where were we?"* | it reads `memory/RESUME.md` instead of guessing |
| 📋 *"what's left?"* | it reads `memory/PENDING.md` |
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
| 🧠 **Memory** | `RESUME.md` (where we left off) and `PENDING.md` (what is postponed) — ⭐ you never write either by hand |

---

## 🗂️ Where to look next

| | |
|---|---|
| 📄 `Mente/START-HERE.md` | the guided first run, written for an assistant to follow with you |
| ⚡ `Mente/QUICKSTART.md` | clone → `bin/init` → tests, for a developer in a hurry |
| 🛠️ `Mente/CAPABILITIES.md` | every command, and what each one refuses to do |
| 📐 `Mente/rules/decisions/` | why it is built this way — one file per decision |

---

## 🧰 What it needs

Python 3 · git · bash. Most machines already have all three; on Windows, Git
Bash brings them together.

## 📜 Licence

**AGPL-3.0** — use it, change it, and if you run it as a service, publish your
changes.
