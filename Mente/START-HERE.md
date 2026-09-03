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
| ask *"shall we install it?"* | ⭐ they do not know what installing means — offer §2's three options |
| tell them to install Python | check it yourself in §3 |
| write the options as a paragraph | ⭐ present them as a chooser — they pick, they do not compose |
| ask twice for the same yes | ⛔ §2 already got it |
| invent steps | ⛔ if it is not written here, say you do not know |

---

Related: `Mente/QUICKSTART.md` (the same install, written for a developer) ·
`Mente/README.md` (what the engine is, in full) · `Mente/CAPABILITIES.md` (every command).
