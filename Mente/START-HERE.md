# START HERE — what to show a person who was handed this link

**Status:** current · **Type:** entry-point · **Updated:** {{date}} · **Owner:** {{owner}}
**Read by:** ⭐ **the assistant, not the person.** It is a script, not a description.
**Scope:** ⚠️ ENGINE document — it ships identical to every clone.

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
> | **The memory** | three files you will actually use — see below |
>
> **The memory, by name:**
>
> | File | ⭐ What you ask for |
> |---|---|
> | `memory/RESUME.md` | *"where did we leave off?"* — the assistant reads it first every session |
> | `memory/PENDING.md` | *"what do we still owe?"* — everything postponed, so nothing is lost by forgetting |
> | `memory/` log | *"why was this decided?"* — the reasoning, months later, when nobody remembers |
>
> **What you do with it — you delegate, in your own words:**
>
> | You say | ⭐ What happens |
> |---|---|
> | *"build me X"* | it opens a block, asks what it may and may not touch, and works inside that |
> | *"where were we?"* | it reads `RESUME.md` instead of guessing |
> | *"what's left?"* | it reads `PENDING.md` |
> | *"is this done?"* | it cannot say yes until the checks pass — ⛔ that is not its opinion to give |
>
> ⭐ **You do not learn commands and you do not remember any of this.** You ask in plain words;
> the system is what makes the assistant keep its promises.
>
> **What it needs:** three things most computers already have. ⚠️ **You do not have to check or
> install them — I will.**

---

## 2 · THEN ASK EXACTLY THIS

> **Shall I check that your computer has what Mente OS needs?**

⛔ **Stop there and wait.** ⚠️ Do not run anything yet, and do not offer a menu of options: one
question with a yes.

---

## 3 · IF THEY SAY YES — check, never instruct

```bash
python3 --version ; git --version ; bash --version | head -1
```

| Result | ⭐ What you say |
|---|---|
| all three answer | *"You have everything. Shall I set it up?"* |
| one is missing | ⛔ **Name what is missing and offer to handle it** — never *"install Python 3.8+"*. On Windows say Git Bash usually brings all three |

---

## 4 · IF THEY SAY YES AGAIN — install it yourself

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

⚠️ **Never hand them a command to type.** ⭐ They say the sentence, you run what it means — that is
the whole point of the system being on disk instead of in their head.

---

## 6 · WHAT NOT TO DO

| ⛔ | ⭐ Instead |
|---|---|
| paste the file tree at them | show §1 |
| explain blocks, campaigns and gates in detail up front | four rows, then their first block |
| say *"read QUICKSTART.md"* | ⚠️ that file is for a developer; this one is for them |
| ask *"shall we install it?"* | ⭐ they do not know — ask the yes/no in §2 |
| tell them to install Python | check it yourself in §3 |
| invent steps | ⛔ if it is not written here, say you do not know |

---

Related: `Mente/QUICKSTART.md` (the same install, written for a developer) ·
`Mente/README.md` (what the engine is, in full) · `Mente/CAPABILITIES.md` (every command).
